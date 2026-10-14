#!/usr/bin/env bash
# Install skills from this repo into a project or the user profile, for Claude Code and/or Codex.
#
#   ./install.sh --project ~/Projects/foo                 # all portable skills into foo/.claude/skills and foo/.agents/skills
#   ./install.sh --project ~/Projects/foo spec-sizing     # just one skill
#   ./install.sh --user --agent claude --link herd        # symlink into ~/.claude/skills (edits in the repo apply live)
#   ./install.sh --list
#
# Options:
#   --project DIR | --user   where to install (one is required unless --list)
#   --agent claude|codex|both   default both. claude: .claude/skills; codex: .agents/skills (project) or ~/.codex/skills (user)
#   --link     symlink instead of copy (keeps one source of truth; the repo must stay where it is)
#   --force    replace an existing skill directory of the same name (it is moved to a .bak-<timestamp> first)
#   --all      include machine-bound skills (see MACHINE_BOUND below) when no skill names are given
#   --dry-run  print what would happen
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$REPO/skills"
# Skills that only work on Oscar's machine setup (herdr, ~/.local/state/herd, codex CLI + Mobbin MCP).
MACHINE_BOUND=(herd herd-side directions)

target="" agent="both" mode="copy" force=0 all=0 dry=0 names=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) target="project"; project_dir="$(cd "$2" && pwd)"; shift 2 ;;
    --user) target="user"; shift ;;
    --agent) agent="$2"; shift 2 ;;
    --link) mode="link"; shift ;;
    --force) force=1; shift ;;
    --all) all=1; shift ;;
    --dry-run) dry=1; shift ;;
    --list)
      for d in "$SKILLS_DIR"/*/; do
        n="$(basename "$d")"; desc="$(sed -n 's/^description: *//p' "$d/SKILL.md" | head -1 | cut -c1-90)"
        tag=""; for m in "${MACHINE_BOUND[@]}"; do [[ "$m" == "$n" ]] && tag=" [machine-bound]"; done
        printf '%-16s%s %s\n' "$n" "$tag" "$desc"
      done; exit 0 ;;
    -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
    -*) echo "unknown option $1" >&2; exit 2 ;;
    *) names+=("$1"); shift ;;
  esac
done
[[ -z "$target" ]] && { echo "choose --project DIR or --user (or --list)" >&2; exit 2; }
[[ "$agent" =~ ^(claude|codex|both)$ ]] || { echo "--agent must be claude, codex or both" >&2; exit 2; }

if [[ ${#names[@]} -eq 0 ]]; then
  for d in "$SKILLS_DIR"/*/; do
    n="$(basename "$d")"; skip=0
    if [[ $all -eq 0 ]]; then for m in "${MACHINE_BOUND[@]}"; do [[ "$m" == "$n" ]] && skip=1; done; fi
    [[ $skip -eq 0 ]] && names+=("$n")
  done
fi

dests=()
if [[ "$target" == "project" ]]; then
  [[ "$agent" != "codex" ]] && dests+=("$project_dir/.claude/skills")
  [[ "$agent" != "claude" ]] && dests+=("$project_dir/.agents/skills")
else
  [[ "$agent" != "codex" ]] && dests+=("$HOME/.claude/skills")
  [[ "$agent" != "claude" ]] && dests+=("$HOME/.codex/skills")
fi

run() { if [[ $dry -eq 1 ]]; then echo "+ $*"; else "$@"; fi; }

for n in "${names[@]}"; do
  src="$SKILLS_DIR/$n"
  [[ -f "$src/SKILL.md" ]] || { echo "no skill named $n" >&2; exit 1; }
  for dest in "${dests[@]}"; do
    run mkdir -p "$dest"
    out="$dest/$n"
    if [[ -e "$out" || -L "$out" ]]; then
      if [[ -L "$out" && "$(readlink -f "$out")" == "$(readlink -f "$src")" ]]; then echo "ok    $out (already linked)"; continue; fi
      if [[ $force -eq 0 ]]; then echo "skip  $out exists (use --force to replace; a backup is kept)"; continue; fi
      run mv "$out" "$out.bak-$(date +%Y%m%d%H%M%S)"
    fi
    if [[ "$mode" == "link" ]]; then run ln -s "$src" "$out"; else run cp -r "$src" "$out"; fi
    echo "$mode  $n -> $out"
  done
done
