---
name: agent-routing
description: Choose which model, agent type and effort level should do each piece of work, and how to brief it. Use whenever you delegate or split work to subagents (agent()/Agent tool, workflows, ultracode builders), pick between Sonnet and Opus or an effort level, or write a brief for a builder subagent.
---

# Agent routing

The goal is the best result per piece at a sensible cost. No builder model is mandatory; pick by fit and write the choice and
the reason in your plan. Two things are fixed: code review is always Codex, independent of whoever wrote the code; and
your task template's rules (e.g. a run-wide effort) apply unless it allows per-piece choices, as delegated-builder runs
do. Before choosing, skim `findings.md` in this skill's folder. It is the evidence log, and our own run
results there outrank vendor claims.

## 1. Classify each piece

| Piece | Default pick | Move it when |
|---|---|---|
| Open-ended judgment: architecture, design direction, taste calls, motion choreography, the page's one memorable moment, final polish, spec writing | Opus at medium; high for flagship or taste-critical work | — |
| Fully specified UI or visual building (layout per breakpoint, states, tokens, references given) | `sonnet-high` | it keeps failing the critic → Opus |
| Fully specified logic or feature code | `sonnet-high`, or Opus at medium if it touches money, permissions, tenancy, migrations or concurrency | — |
| Mechanical wiring, data loading, routes, straightforward tests | `sonnet-mid` or Opus at low | — |
| Read-only search or exploration | the Explore agent | — |
| Code review | Codex (`codex-review`), never the agent that wrote the code | — |
| Judging screenshots (the look) | `fable-high` critic | — |

Where your task template allows per-piece choices, escalate after 2 failed rounds on the same piece: Sonnet → Opus, or medium → high. A better agent fixes repeated
misses; a longer brief rarely does. When an agent keeps missing a rule (the same kind of finding comes back), make Codex
(`gpt-6.1-sol`, medium or high) the executor for that fix. It is the most rule-precise executor for mechanical sweeps.
Briefs for review fixes ask for the whole class of a finding, never only the cited examples. Agents read cited examples
as the full scope, Sonnet most of all. (Evidence: F21-03, 2026-10-12.)

Avoid xhigh and max unless a measured gain justifies them. At max, testers saw scope creep, self-started reviewer
fan-out, and one run that returned nothing after 20 minutes.

## 2. Brief for the model you picked

**Sonnet** reads instructions literally, does not generalise them, and at medium effort or below does only what was asked.
It also invents values that aren't given.
- **Ownership:** list the files it owns and what it must not touch.
- **Scope:** state the scope of every rule ("every interactive element in every variant, not just the first").
- **Data:** give it every value, copy string, fixture and expected test result. Say "if a value isn't given, stop and
  report it, never guess".
- **Reasons:** give the reason behind each rule, so it generalises correctly.
- **The finish:** for UI work, ask for it outright ("refine spacing, alignment and states until it would ship in a top
  brand").
- **Checks:** name the checks to run, and require real test or build output before it reports done.

**Opus** gets to work fast and, on open briefs, falls back on a house style. It is better at looking right than at being
right about a brand.
- **Design:** name specific patterns to ban (not "avoid generic"), and extend the list after each result. Ask for 3 or 4
  distinct directions first, then pick one.
- **Brand:** state the brand constraints (the logo, colours and copy it must keep) and test them.
- **Scope:** say when to stop. It can over-extend its scope.

**Every brief** names the goal and why it matters, the definition of done, and the checks.

## 3. Record the outcome
At the end of a run, write an `## Agent routing outcomes` section in your result. For each piece give the agent type,
model and effort; the rounds until it passed review or critique; what failed; and whether you escalated. The coordinator
appends it to `findings.md`.
