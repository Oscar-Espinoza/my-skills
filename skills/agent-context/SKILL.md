---
name: agent-context
description: Audit, write, or streamline AGENTS.md, CLAUDE.md, and their referenced context files for Claude Code and Codex. Use when the user asks to improve agent instructions, diagnose missed context, or apply context-writing practices to a project.
---

# Agent Context

Make the project's instructions easy to discover, relevant to the task, and consistent with the user's current workflow. Apply to the named project, not every project on the machine.

## Scope and authority

- Follow the user's request and applicable instruction files. Preserve project-specific safety rules, authorization boundaries, and existing user changes.
- For research or audit, report findings without changing files. For implementation, carry authorized edits through validation; routine reversible edits do not need another confirmation.
- A repository that forbids CLAUDE.md, project skills, or configuration changes keeps those restrictions. This personal skill does not authorize extensions, hooks, accounts, deployment, or model spending.
- Improve instruction delivery and wording; do not refactor application code or invent a new workflow.

## Inspect before editing

1. Read root and applicable nested instructions completely, plus current workflow documents. Check the actual working tree.
2. Run `python3 <skill-directory>/scripts/audit_context.py <project>` for a read-only size and discovery inventory. Substitute the absolute directory containing this SKILL.md. The script prints metadata, not file contents or secrets. It does not prove runtime loading or compute tokens.
3. If loading, imports, memory, symlinks, or compaction matter, read [loading.md](references/loading.md). Verify version-sensitive claims against its primary sources and the installed client; do not copy an old workaround automatically.
4. Identify current requirements, historical policies, module invariants, feature notes, and task references. Resolve contradictions from explicit user decisions and documented precedence. Ask only if a consequential conflict cannot be resolved.

## Write and organize

Read [writing.md](references/writing.md) when drafting or restructuring; it includes placement criteria and examples.

- Keep universal operational boundaries in root instructions and local deviations in nested files. Move lengthy feature descriptions into ordinary references, preserving their constraints and source paths.
- Put required rules directly within reach of the task prompt or relevant instruction file. Explain when and why each reference must be read. A path alone is not a reading instruction.
- Read required instructions completely; read relevant sections of large references. If a read is truncated, continue before claiming compliance. Add a contents list to long references.
- Avoid unconditional imports as a size fix: eager imports still consume context. Use conditional references for information needed only on certain tasks.
- Measure bytes and, when exposed, actual context tokens alongside lines. Do not compress paragraphs into giant lines to pass a budget. Size targets are project choices, not proven model thresholds.
- Retain exact commands and significant caveats. Check manifests and real paths; omit descriptions cheaply derived from code. Distinguish planned, implemented, locally validated, and externally verified behavior.
- Describe current policy in active instructions. Historical notes must be explicitly non-authoritative; do not archive a still-required rule accidentally.

## Model behavior and verification

Read [models-and-evidence.md](references/models-and-evidence.md) when tuning Opus/Sonnet execution guidance or discussing evidence. Keep changing model/provider facts out of universal project rules where possible.

Give concrete scope, completion conditions, and relevant validation. Preserve existing effort and test policies. Do not raise effort, spawn review teams, repeat passing checks, or run paid comparisons just because a model can do so.

## Complete the work

- Verify local links, reference discoverability, preserved safety rules, sizes, and relevant docs checks. Run changed helpers against realistic temporary fixtures; no application suite is needed for wording-only changes.
- Inspect the diff for lost constraints and new contradictions. Keep configuration changes minimal and preserve unrelated keys; back up user configuration outside discovery directories when changing it.
- Use independent review when the project requires it and delegation is available and authorized. Bind evidence to the exact artifact or diff examined.
- Report changes, before/after size, checks, and limitations. Distinguish structural validation from observed performance; do not claim improved adherence without a representative behavioral comparison.
- Stop after the requested result and relevant checks. Propose further work without performing unrelated changes.
