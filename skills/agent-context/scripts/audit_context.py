#!/usr/bin/env python3
"""Read-only instruction inventory. Sizes are bytes, not model context tokens."""
import argparse
import json
import os
from pathlib import Path

SKIP = {".git", "node_modules", ".venv", "venv", "dist", "build", ".svelte-kit",
        ".next", "coverage", ".worktrees", "worktrees", "__pycache__"}
NAMES = {"AGENTS.md", "AGENTS.override.md", "CLAUDE.md", "CLAUDE.local.md"}


def metadata(path):
    data = path.read_bytes()
    lines = data.splitlines()
    return {"path": str(path), "bytes": len(data), "lines": len(lines),
            "max_line_bytes": max(map(len, lines), default=0)}


def inventory(root, file_budget, chain_budget, settings_path):
    files, errors = [], []
    for current, directories, names in os.walk(root, followlinks=False):
        directories[:] = sorted(d for d in directories if d not in SKIP
                                and (not d.startswith(".") or d == ".claude"))
        for name in sorted(names):
            path = Path(current) / name
            is_rule = name.endswith(".md") and ".claude/rules/" in str(path) + "/"
            if name not in NAMES and not is_rule:
                continue
            # Do not follow instruction symlinks out of the requested project.
            if path.is_symlink() and not path.resolve().is_relative_to(root):
                errors.append({"path": str(path), "error": "external symlink skipped"})
                continue
            try:
                files.append(metadata(path))
            except OSError as error:
                errors.append({"path": str(path), "error": type(error).__name__})

    ancestors = []
    for directory in reversed(root.parents):
        for name in NAMES:
            path = directory / name
            if path.is_file():
                try:
                    ancestors.append(metadata(path))
                except OSError as error:
                    errors.append({"path": str(path), "error": type(error).__name__})
        path = directory / ".claude" / "CLAUDE.md"
        if path.is_file() and path != Path.home() / ".claude" / "CLAUDE.md":
            try:
                ancestors.append(metadata(path))
            except OSError as error:
                errors.append({"path": str(path), "error": type(error).__name__})

    mode = "claude-md-or-agents-md"
    try:
        settings = json.loads(settings_path.read_text()) if settings_path.is_file() else {}
        mode = settings.get("pluginConfigs", {}).get("agents-md@builtin", {}).get(
            "options", {}).get("instructionFiles", mode)
    except (OSError, ValueError, AttributeError):
        mode = "unknown (user settings could not be read)"

    agents = [item for item in files + ancestors if Path(item["path"]).name == "AGENTS.md"]
    chains = []
    for item in files:
        if Path(item["path"]).name != "AGENTS.md":
            continue
        leaf = Path(item["path"]).parent
        members = [entry for entry in agents if leaf.is_relative_to(Path(entry["path"]).parent)]
        chains.append({"leaf": item["path"], "bytes": sum(entry["bytes"] for entry in members),
                       "files": [entry["path"] for entry in members]})
    chains.sort(key=lambda item: item["bytes"], reverse=True)
    claude_candidates = [entry["path"] for entry in files + ancestors
                         if Path(entry["path"]).name in {"CLAUDE.md", "CLAUDE.local.md"}]
    return {
        "root": str(root), "user_settings_instruction_mode": mode,
        "instruction_files": sorted(files, key=lambda item: item["path"]),
        "ancestor_instructions": sorted(ancestors, key=lambda item: item["path"]),
        "claude_suppression_candidates": claude_candidates,
        "largest_plain_agents_chain": chains[0] if chains else None,
        "advisory_budgets": {"file_bytes": file_budget, "plain_agents_chain_bytes": chain_budget},
        "over_file_budget": [item["path"] for item in files if item["bytes"] > file_budget],
        "over_chain_budget": [item["leaf"] for item in chains if item["bytes"] > chain_budget],
        "read_errors": errors,
        "limitations": [
            "Metadata only: no model invocation, writes, token estimates, or proof of runtime loading.",
            "Plain AGENTS chains include ancestors; override/fallback selection is not simulated.",
            "Imports, global memory, skills, exclusions, launch settings and managed policy are not included.",
            "Claude suppression candidates are paths to inspect, not proof of suppression for a particular launch.",
            "Budgets are adjustable recommendations, not universal client or model limits.",
            "Hidden directories except .claude, dependency/build directories and external symlinks are skipped."
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--json", action="store_true", help="emit structured metadata")
    parser.add_argument("--file-budget", type=int, default=6144, help="advisory bytes per file")
    parser.add_argument("--chain-budget", type=int, default=32768, help="advisory plain AGENTS chain bytes")
    args = parser.parse_args()
    root = args.project.expanduser().resolve()
    if not root.is_dir():
        parser.error("project must be an existing directory")
    if args.file_budget < 1 or args.chain_budget < 1:
        parser.error("budgets must be positive byte counts")
    report = inventory(root, args.file_budget, args.chain_budget, Path.home() / ".claude/settings.json")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Project: {root}\nUser Claude instruction mode: {report['user_settings_instruction_mode']}")
        for item in report["instruction_files"]:
            print(f"{item['bytes']:>7} bytes  {item['lines']:>4} lines  "
                  f"max line {item['max_line_bytes']:>5} bytes  {Path(item['path']).relative_to(root)}")
        chain = report["largest_plain_agents_chain"]
        if chain:
            print(f"Largest plain AGENTS chain (including ancestors): {chain['bytes']} bytes ({chain['leaf']})")
        print(f"Above advisory budgets: {len(report['over_file_budget'])} files; "
              f"{len(report['over_chain_budget'])} plain AGENTS chains")
        for candidate in report["claude_suppression_candidates"]:
            print(f"Inspect Claude discovery candidate: {candidate}")
        for error in report["read_errors"]:
            print(f"Read issue: {error['path']}: {error['error']}")
        for limitation in report["limitations"]:
            print(f"Note: {limitation}")


if __name__ == "__main__":
    main()
