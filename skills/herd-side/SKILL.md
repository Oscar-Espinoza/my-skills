---
name: herd-side
description: Side-project mode for herd — coordinate fast, hands-on development of non-production side projects with herd workers, using cheaper model routing (Sonnet 5.5 medium/high, Opus 5.5 low/medium max, no Fable) and the type system instead of a test suite as the only gate. Use when the user says "side project mode", invokes /herd-side, or asks to run herd workers on a repo whose CLAUDE.md marks it as a side project. Not for production projects.
---

# Herd side-project mode

You are the herd coordinator, with side-project rules layered on top. **Follow the `herd` skill for all
mechanics** (`herd-spawn`, background `herdr agent wait` watchers, report files in `/tmp/herd/`,
follow-ups via `herdr agent prompt`, closing tabs). This skill only changes *what* you spawn and *how
tasks are written*. Speed over rigor: this is not production code.

## Backlog

Keep `BACKLOG.md` in the repo root as a checklist. Items are small: one feature or change a single
worker can finish and typecheck in one session. Pick the next item(s), spawn workers, check items off
when the user accepts the result, and append follow-ups from worker reports. If no backlog exists,
draft one from the user's description and show it before spawning.

## Model routing

Always pass model, effort, and permission mode via `-a` (passing `-a` drops herd-spawn's default, so
re-include `--permission-mode acceptEdits`):

| Task | `-a` value |
|---|---|
| Default: feature, UI, CRUD, glue | `--model claude-sonnet-5-5 --effort medium --permission-mode acceptEdits` |
| Trickier logic, multi-file changes | `--model claude-sonnet-5-5 --effort high --permission-mode acceptEdits` |
| Data model, cross-cutting design, type-heavy refactors | `--model claude-opus-5-5 --effort low --permission-mode acceptEdits` |
| Stuck (failed the type gate twice) or genuinely hard | `--model claude-opus-5-5 --effort medium --permission-mode acceptEdits` |

Opus medium is the ceiling. Never use Fable, never go above medium on Opus. Escalate one row at a
time; don't start at Opus unless the task clearly fits its row.

Example:
```
herd-spawn -a "--model claude-sonnet-5-5 --effort medium --permission-mode acceptEdits" \
  add-settings-page ~/Projects/myapp "<task text + worker rules>"
```

## Type gate (no tests)

No test suite. Correctness comes from the type system, so find the project's gate before spawning and
put the exact commands in the task:

| Stack | Gate |
|---|---|
| TypeScript | `tsc --noEmit` via the project's package manager (pnpm/bun) + its build script |
| Rust | `cargo check` + `cargo clippy` |
| Python | `pyright --strict` (or the project's configured checker) |
| Go | `go vet ./...` + `go build ./...` |

For a new project, or one with loose settings, make the first backlog item "enable strict typing"
(TS: `strict`, `noUncheckedIndexedAccess`; Python: strict pyright; Rust: clippy warnings on).
Never run bare `pnpm test` (see ~/CLAUDE.md).

## Worker rules (append to every task)

```
Side-project rules:
- Do not write or run tests. Rely on the type system: no `any`/untyped escapes or casts to silence
  errors; model data with precise types so invalid states don't compile.
- Before reporting, run the type gate: <gate commands>. Fix until clean.
- Make exactly one commit with a descriptive message when done. Do not push.
- In your report, list follow-up items you noticed (bugs, missing pieces) as one line each.
```

## Parallelism

Default to one worker per repo. For parallel work, give each worker its own worktree:
`git worktree add ../<repo>-<name> -b <name>` and use that path as the worker's cwd. After the user
accepts, merge the branch into the main working branch, then `git worktree remove` it. Keep parallel
tasks in separate areas of the code to avoid conflicts.

## Review

No reviewer or observer workers. When a worker finishes: read its report, skim `git diff HEAD~1` (or the
branch diff), tell the user what changed plus any follow-ups, and let them accept or send a follow-up.
If a worker's gate fails twice, respawn the task one routing row higher instead of prompting again.

## Fewer blocked states

If workers keep hitting `blocked` on routine commands, suggest a project `.claude/settings.json`
allowlist for the gate commands, `git add`, and `git commit` (via `/fewer-permission-prompts` or the
update-config skill). Ask before writing it.
