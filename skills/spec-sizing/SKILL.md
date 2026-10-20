---
name: spec-sizing
description: Size and split the tickets of a spec, epic or feature list against the real code before anyone builds them, so no run stops mid-way at a size check. Use whenever a spec or epic is being turned into tickets, a ticket list needs estimates (pieces, files), a ticket "split mid-run" or failed a size cap, someone asks "how big is this", "re-size the tickets", "split this epic", "is this ticket too big", or tickets need dependencies, acceptance lines or a quickcode/ultracode-style flow assigned. Also use when writing the ticket table of a new SPEC, even if nobody says "sizing".
---

# Spec sizing

Size every ticket by **listing the files it will create or edit in the real code**, then split anything over the
cap before a build starts. Intuition-based estimates miss the platform work around each feature: on one 24-ticket
epic, spec estimates were **1.73x too low on files** while piece counts were roughly right. The file cap, not the
piece cap, is what forces splits, and a split discovered mid-run costs a full planning pass (≈20 min each).

Read `references/hidden-work-checklist.md` before sizing anything. If the project has a calibration file (look for
`references/calibration-<project>.md` here, or `docs/sizing-calibration.md` / `.sizing/calibration.md` in the repo),
read it too; it holds measured per-primitive file costs for that codebase.

## Inputs to gather first
- The spec (screens, server/data sections, the ticket table and its estimates).
- The tickets in their tracker format (ids, description, acceptance lines, deps, flow/route, group, status).
- The size rule (e.g. "≈8 build pieces, ≈40 files, or holds deliverables that can merge on their own") and the flow
  rule that decides light vs heavy process. Find them in the repo or the coordinator docs; ask only if absent.
- Root `AGENTS.md`/`CLAUDE.md` and the nested ones of every module you size against.
- Any earlier worked split (a run that stopped at the size check): it shows the expected file-list style.

## Workflow

### 1. Inventory each ticket from the code
For each ticket, as a planning step would:
- **Pieces**: numbered build pieces.
- **Files**: every file created (C) or edited (E), grouped by piece, **including the hidden platform work** from the
  checklist and generated output, fixtures, barrels and docs. Total them: hand-written vs generated/docs.
- **Patterns**: the existing code each piece must follow, cited `path:line`. Open the file and check the line exists;
  a wrong citation sends the builder the wrong way.
- **Upstream not yet built**: when the ticket builds on another unbuilt ticket, size against that ticket's planned
  files and name them as assumptions, so the integration pass (step 4) can reconcile them.

Large epics: split the inventory across parallel agents (one per related cluster of tickets, so a cluster's
dependencies stay coherent), each writing one file per ticket. A second model can size half the tickets
independently; it later reviews the whole set.

### 2. Decide KEEP or SPLIT
Split when the ticket is over the piece or file cap, **or** holds parts that can merge and be verified on their own.
Good cuts, in order of preference:
1. **Server/data, then UI.** If the server half adds an API operation, table or privileged SQL, it is almost always
   its own ticket (a new operation alone is ~15-20 files once contracts and fixtures are counted).
2. **Foundation, then consumers** (event store before emitters, registry before screens).
3. **By section** for sweeps (labels, translations): each slice moves a whole section, so no intermediate state
   breaks an invariant test (e.g. "label = page title").
Keep a ticket whole when its acceptance can only be verified over the integrated result, and say so.

A slice slightly over the file cap is acceptable only when it is one cohesive deliverable that cannot split without
separating something from its only consumer; record that reason.

### 3. Write the sub-tickets
Follow the tracker's existing shape (copy an existing split entry's fields). For each sub-ticket:
- **Id**: original prefix + `-A`, `-B`, … (if `-A` is taken by an existing sibling, start at the next free letter).
  Check the project's id pattern first: tooling often derives task/DB/migration names from it. In ecommerce-builder it
  is `Fnn-nn(-X)?`, with one letter. Splitting an already-lettered ticket (`F23-12-A`) must use free single letters of its
  parent (`F23-12-D`, `-E`, …), never `F23-12-A-A`. Dry-run the start script on every new id.
- **Description**: the original description unchanged, plus a `SPLIT (<date>): …` note with the slice's scope, the
  files/patterns it owns, defaults it takes, and a pointer to the sizing evidence.
- **Acceptance**: redistribute the original lines **unchanged**, in order. The final "checks/gate pass" line goes on
  every sub-ticket. A line may sit on two slices only when each slice's note names the part it verifies. Never
  invent new acceptance; scope with no covering line goes to the spec gaps or another ticket's note.
- **Deps per slice, by what it consumes**: an API slice depends on the data it reads, not on the UI the original
  depended on. Whole-ticket deps copied onto every slice serialize the graph needlessly (one epic's critical chain
  went 20 → 14 just by doing this). Keep an edge only when the slice really uses it, and write why when it is
  non-obvious.
- **Flow**: re-check each slice against the flow rule; a small copy-only slice may drop to the light flow (then do not
  inherit heavy process text such as mandatory design-critique steps; say so in its description).
- Mark the original superseded (`paused`, "SUPERSEDED: split into …") and rewire **every** dependent, including any
  umbrella ticket.

### 4. Integration pass across tickets
Independently sized tickets disagree. Before review, check across the whole set:
- **Shared files and tables have one owner** (two slices creating the same migration or catalogue, a later ticket
  re-editing a control another ticket owns).
- **Every analytics/audit event has a server-side producer** with a named owner slice; a UI slice may only trigger it.
- **Paths agree**: a consumer cites the paths its upstream slice will create, not a parallel invention.
- **Late screens are covered**: a cross-cutting UI (assistant panel, help, nav) that must cover every screen depends
  on the last screen, or some later ticket is explicitly scoped to add its entry.
- **Integrated checks run last**: a ticket whose acceptance verifies the integrated product depends on every slice
  that check covers.

### 5. Spec-vs-code gaps
List each missing or contradicted value (copy, limits, behaviour, an API that doesn't exist, a seed that lacks data,
an upstream that ships a different shape) with a proposed default, so builders don't block. **Never let a default
silently override something the spec states explicitly** (a security design, an acceptance line): keep the spec's
version and list the alternative as a decision for the owner.

### 6. Cross-model review, then apply
Have a different model review the full candidate before writing it: sizes against the evidence, acceptance coverage
(nothing lost, moved unchanged, shared parts named), deps (no cycles, nothing on a superseded id, missing edges,
needlessly serial edges), flow, shape. Answer each finding (accept, or deviate with a reason), regenerate, and run a
second round until it approves. Expect real findings: in practice round 1 caught a default that overrode the spec's
security design and two defaults that contradicted acceptance lines.

Apply mechanically, not by hand-editing JSON. `scripts/apply_splits.py` applies a splits file to a tracker JSON and
refuses on any lost/duplicated acceptance line, unknown or superseded dep, or cycle; `scripts/ticket_graph.py`
prints the critical chain and the parallel waves. Back the tracker up first and confirm it did not change between
backup and apply (another session may write it).

### 7. Report
Write a result document:
- per original ticket: spec estimate, re-sized estimate, kept or split, and each slice (pieces / files, flow, deps);
- the new dependency order: critical chain plus the waves that can run in parallel, and external blockers;
- spec gaps with defaults, the decisions that need the owner first, and any defaults the review replaced;
- the reviewer's final verdict; totals before and after.
Then update the spec's ticket table from the tracker (generate it; don't retype it) and add a calibration entry.

## Calibrate after every sizing or build
Record, per project, measured file costs per primitive (new API operation, table with access control, privileged
query, new route group, UI screen with browser tests) and the estimate-to-actual ratio. Use the template in
`references/calibration-template.md`. Measured numbers beat this skill's defaults; an example from a real epic is in
`references/calibration-example.md`.
