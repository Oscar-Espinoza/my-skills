# agent-skills

Oscar's own agent skills for Claude Code and Codex, in one place so they can be installed into any project or
machine. Each skill is a folder under `skills/` with a `SKILL.md` (frontmatter `name` and `description`) and
optional `references/`, `scripts/` and `agents/` files.

| Skill | What it does | Portable? |
|---|---|---|
| `spec-sizing` | Size and split spec/epic tickets against the real code before building (hidden-work checklist, split rules, cross-model review, `apply_splits.py` / `ticket_graph.py`). | yes |
| `agent-routing` | Choose model, agent type and effort per piece of delegated work, and how to brief it (`findings.md` is the evidence log). | yes (model names are current as of 2026-10) |
| `agent-context` | Audit and streamline AGENTS.md / CLAUDE.md and their referenced context files. | yes |
| `herd` | Coordinate worker agents in herdr tabs. | needs `herdr` and `herd-spawn` |
| `herd-side` | Side-project mode for herd: cheaper routing, types as the gate. | needs `herd` |
| `directions` | Build N design directions from references, Mobbin and a Codex opinion (manual: `/directions`). | needs the `codex` CLI and the Mobbin MCP |

Third-party skills Oscar uses are not copied here; see `external-skills.md` for how to install them from their source.

## Install

```bash
./install.sh --list                                   # what is here
./install.sh --project ~/Projects/foo                 # portable skills into foo/.claude/skills and foo/.agents/skills
./install.sh --project ~/Projects/foo spec-sizing     # one skill
./install.sh --user --agent claude --link spec-sizing # symlink into ~/.claude/skills; repo edits apply live
./install.sh --project ~/Projects/foo --dry-run       # show what would happen
```

- `--agent claude|codex|both` (default both). Claude Code reads `.claude/skills/` (project) and `~/.claude/skills/`
  (user). Codex reads `.agents/skills/` (project) and, on this machine, `~/.codex/skills/` (user).
- Machine-bound skills are skipped unless named or `--all` is passed.
- Existing skills are never overwritten unless `--force`, which moves the old folder to `<name>.bak-<timestamp>`.
- Copy (default) when the project should own its copy, e.g. to commit it into that repo. Use `--link` for your own
  profile so there is one source of truth.

## Editing a skill
Edit it here, commit, then reinstall (copies) or do nothing (links). Keep `SKILL.md` under ~500 lines and move detail
into `references/`. The description is what makes a skill trigger: say what it does and when to use it.
