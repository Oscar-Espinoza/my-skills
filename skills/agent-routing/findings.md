# Agent routing findings

Evidence log, organised by kind of work. Each entry gives model and effort, source and date.

**Sources, most trusted first:**
- [ours]: from our own runs;
- [tester]: from practitioners who tested the model on real work;
- [anthropic]: from the vendor's docs.

Mark wrong entries ~~superseded~~ instead of deleting them.

## Design and frontend
- Sonnet 5.5 at high: design taste close to Opus, "its own taste", ranked a close second. Fewer animations and
  lighter ARIA work than Opus. [tester: thomas-wiegold.com] (2026-10)
- Opus 5.5 at high: ranked first in a web-design test, with 9 animations and more accessibility work. [tester: Wiegold]
  (2026-10)
- Both fall back on a house style on open briefs, and "avoid the generic look" only swaps the default. What works:
  named ban lists, concrete specs, proposing directions first. [anthropic, tester: muz.li] (2026-10)
- Opus 5.5: "better at looking right than at being right about your brand". It used the wrong logo and replaced a
  brand's green with purple. [tester: muz.li] (2026-10)
- Opus 5.5 brief pattern that worked:
  - a brief under 200 words covering audience, mood, type, the one memorable thing, sections, motion and a quality
    floor;
  - one bold moment per page;
  - "fade-up on every section is the tell";
  - screenshots at 1440 and 390;
  - name the 3 weakest things and fix only those;
  - replay motion in slow motion.

  [tester: muz.li] (2026-10)
- Models can't judge how scroll or springs feel on a real phone; that needs human review. [tester: muz.li]
- Opus 5.5 at high with no design brief built F19-01 to F19-16 (UI restyles). Functionally fine; Oscar judged the look
  poor. [ours] (2026-10-09)

## Coding
- Sonnet 5.5 at high wrote a correct chess engine at about half Opus's cost, but invented test values that no source
  gave, and 2 were wrong. Opus 5.5's run was "the only one I could accept without review". [tester: Wiegold] (2026-10)
- Sonnet 5.5 suits work you can specify and check, and finished about 2x faster (28 vs 52 minutes). Opus is better on
  vague or strategic goals. [tester: X "7 use cases"] (2026-10)
- Sonnet at low and medium scopes to exactly what was asked and does not generalise instructions. At low it may skip
  verification. [anthropic] (2026-10)
- Sonnet 5.5 at max scored lower on FrontierCode than at xhigh (46.2% vs 52.1%) because of out-of-scope edits and
  reviewer-subagent fan-out. [anthropic launch post] (2026-10)
- Opus 5.5 at medium matches or beats Opus 5 at high; low comes close on several coding evals. [anthropic] (2026-10)

## Code review
- On 13 hard known bugs: Sonnet 5.5 caught 6 (41.2% actionable precision, about 2x faster); Opus 5.5 caught 8 in the
  standard config and 10 at max. [tester: CodeRabbit] (2026-10)
- Codex as an independent reviewer caught real issues across our F19 merges: a stale seed spec, NORTE's product limit,
  ci-plan dependencies. [ours] (2026-10-09)

## Cost and effort
- Prices per million input/output tokens: Sonnet 5.5 $2 / $10; Opus 5.5 $4 / $20. [anthropic]
- One Opus max run took about 20 minutes, cost $2.56 and returned nothing. [tester: Simon Willison, via muz.li]

## Our runs
(The coordinator appends each run's "Agent routing outcomes" here.)

### F16-09-admin-help-assistant (2026-10-09, effort medium) [ours]
The task fixed every agent at medium effort; all agents used the session model (Opus 5.5).
| Piece | Agents | Outcome |
|---|---|---|
| Plan | 4 Explore-style scouts + 1 planner | FEASIBLE in one pass, with three spec decisions |
| Build | 4 parallel builders, then the API module builder, then an integrator | The help-path bug (admin proxy vs API prefix) slipped through and was caught by the verification panel |
| Verify | 5 lens agents | Found 1 blocking issue and 8 should-fix issues |
| Fixes | Round 0: 2 fixers + system-map + check; round 1: 2 fixers + check; round 2: 1 fixer | No escalation needed. The permission-history leak took 2 Codex rounds: the first fix covered tool data only, not data copied from history |
| Review | Codex (`codex-review`) for all 3 rounds and the evidence check | Exit 0 every time; no fallback used |

### F20-02-profit-settlement-ledger (2026-10-09, effort medium) [ours]
| Piece | Agent / model / effort | Rounds to pass | What failed | Escalation |
|---|---|---|---|---|
| Explore (3 lenses) + feasibility/plan | workflow subagents, Opus 5.5, medium | 1 | — | none |
| P1 foundation (migration, grants, contracts, lifecycle, audit ops) | Opus 5.5 medium | 1 | migration number drift vs main (left to merge hook) | none |
| P2 orders backend + API import + worker | Opus 5.5 medium | 1 build + 1 fix | no terminal failed state; cross-source reimport dupes (panel) | none |
| P3 metric + loader + report route | Opus 5.5 medium | 1 build + 1 fix | refund subtracted pass-through tax (panel) | none |
| P4 admin UI + system map | Sonnet 5.5 medium | 1 | — (doc note fixed with B) | none |
| Integrator | Opus 5.5 medium | 1 | fixed stale audit plugin.db.test registration; added API route DB test | none |
| Skeptic panel (5 lenses) | Opus 5.5 medium | — | found 2 major, several minor | — |
| Panel fixes | Opus 5.5 medium | 1 | — | none |
| Code review | Codex (codex-review) | round 1 PASS; fix-limited round PASS | 1 doc note | — |
| OpenAPI doc fix | orchestrator (Opus 5.5) | 1 | — | — |

### F22-01-admin-library-research (2026-10-10, effort medium) [ours]
| Piece | Agent type / model / effort | Rounds to pass | What failed | Escalation |
|---|---|---|---|---|
| Feasibility plan | workflow default (Opus 5.5) / medium | 1 | — | none |
| Admin audit | Opus 5.5 / medium | 1 internal + Codex notes in r1/r2 | polling claim, tú count, approval wording | none |
| API inventory | Opus 5.5 / medium | needed fixes r1–r3 | wrong response type, "covered" B2B rejection, pct wording | none |
| Differentiators | Opus 5.5 / medium | r1–r2 | Shopify setup-tasks claim contradicted by primary doc; unqualified absence claims | none |
| Mobbin references ×16 (+error-states in fix) | Opus 5.5 / medium | 1 (+fixes: 1 mislabeled image, 1 duplicate, folder added) | Square row described a Rox image; duplicate Pinterest | none |
| SPEC writer (taste/direction) | Opus 5.5 / medium | did not fully pass (4 Codex rounds) | data semantics and feed algorithm, not taste | none (stayed Opus) |
| Skeptic panels/verifiers | Opus 5.5 / medium | — | caught most issues; missed the N-summary wording in round 3 | none |
| Fixers | Opus 5.5 / medium; orchestrator for small r3 follow-ups | — | — | none |
| Code review | Codex gpt-6.1-sol (codex-review) | 4 reviews + evidence | — | no fallback needed |

### F20-01-cuotas-engine (2026-10-10, effort medium, risky) [ours]
| Piece | Agent / model / effort | Rounds to pass | What failed / escalation |
|---|---|---|---|
| Scouts (3) | workflow agents, Opus 5.5, medium | 1 | — |
| PLAN | workflow agent, Opus 5.5, high | 1 | — |
| Build WP-A, B, C1, D1, E, C2, D2, integrator | workflow agents, Opus 5.5, medium | 1 build plus fixes | The integrator missed stale retention grants (gate receipt 1). The builders' local-schedule design was later superseded by Oscar's decision. |
| Skeptic panel (5 lenses) | workflow agents, Opus 5.5, high | 1 | 3 blocking findings: an unprotected connected-status guard, an orphaned pending attempt, a copied destination helper |
| Fix rounds 1–3 (fixers plus integrators) | workflow agents, Opus 5.5, medium | Codex rounds 1–3 failed | MP terms recurred every round. The real issue was a spec ambiguity, not effort; it was resolved by Oscar's decision, not by escalation. The round-3 workflow was killed mid-integrate (commit landed, responses missing). |
| Provider research plus dispatch-orphan fix | Codex partner pane, GPT-6.1-Sol, xhigh | 1 (passed review-4) | Early pane `send-text` drafts confused Oscar; coordination then moved to files. |
| Terms rework (core, surfaces, integrator) | workflow agents, Opus 5.5, medium | 1 (passed review-4) | — |
| Review-5 test fix (shardSessions) | coordinator, Opus 5.5 | 1 | Caught only by the full gate |
| Reviews 1–5 and the evidence check | `codex-review --xhigh` (Codex) | review-4 full pass, review-5 limited pass | — |

### F21-01-storefront-library-research (2026-10-10, effort medium) [ours]
| Piece | Agent type / model / effort | Rounds to pass | What failed | Escalation |
|---|---|---|---|---|
| Feasibility + audit (4) | workflow subagents, Opus 5.5, medium | 1 | none | no |
| Mobbin research (30 sections) | workflow subagents, Opus 5.5, medium; verifier per folder | 1–2 | 9 folders had takeaways that didn't match their images; preorder had one off-topic image (removed). Fixed by a fix agent and a later fix pass | no |
| SPEC foundation (audit, tokens, motion, themes) | Opus 5.5 medium writer + Opus 5.5 medium critic each | 1 + critic | cross-part id mismatches (memorable-moment ids, motion numbering) | reconciled by integration agents |
| Section catalogue (6×5 entries) | Opus 5.5 medium writer + critic | 1 + critic | stale motion ids, provisional variant names | integration pass |
| Integration, editor, 6-lens panel, fixer | Opus 5.5 medium | 1 | 48 panel findings (46 fixed, 2 disputed) | no |
| Codex review | `codex-review` (Codex), no fallback needed | round 1 fail → round 2 pass → fix-only pass | 4 blocking: token cycle, type-math infeasibility, CMS adapter, invented API field | sweep agents for same error classes, then skeptic verify |
| Final evidence check | `codex-review` | 1 | none | no |
| Orchestration and taste decisions | this session, Opus 5.5 | n/a | n/a | n/a |

### F21-02-theme-token-engine (2026-10-11, effort medium, delegated builders) [ours]
Planning, direction, integration and the critique loop: the orchestrator (Opus 5.5). Code review was Codex only (gpt-6.1-sol xhigh via codex-review). The critic was fable-high (Fable 5.1, high), as acceptance 7 names it.
**Effort deviations from "every agent() at medium":**
- Builders ran at high, as the builder rule allows.
- Critics ran at fable-high, as acceptance 7 requires.
- Commit agents ran at medium.
- Escalated Opus builders used the opus-medium agent type at effort high.
**Oscar's sonnet-high rule overrode the SPEC's Opus owners:** P3 (validator), P4 (merge), P8 (provider) and P9 (admin) went to Sonnet.
Per Sonnet piece, all `sonnet-high` (Sonnet 5.5, high). "Codex findings" counts blocking findings in verify-1 and reviews 1-3, plus the gate failure, traced to the piece's files:
| Piece | Scope | Codex findings attributable (severity) | Critique rounds | Rounds to pass | Invented values caught | Escalated |
|---|---|---|---|---|---|---|
| P1 contracts schema | theme.schema.json, brand fields, fixtures, regen | 1 (P2): acceptance 6, durations/easings not in schema. This was my plan decision (motion tokens global per SPEC 5.4), not a builder error; fixed by F3 | — | 2 (F3, F5) | 0. P1 self-reported its chosen bounds (id pattern, maxLengths) as non-SPEC | no |
| P2 fonts | 8 woff2, fonts.css, FONT_PAIRS | 1 (P2, docs): LICENSES.md opsz 40 went stale after the Opus opsz change | Bodoni hairlines (r3, r4) | 2 (fixed by Opus r4) | 0. It reported the Bodoni fit15 7.96 vs SPEC 7.94 contradiction instead of adjusting | Bodoni part: yes, critique r4 to Opus |
| P3 theme core | types, derive, scale, moments, validate | 1 (P2): derive.ts copied brand's toHsl and blend | — | 3 (G2 extraction changed legacy output, review 2 → H1 Opus) | 0. It flagged its own C6 section-reach table as a judgement call | colour helper: yes, to Opus after 2 rounds |
| P4 css + brand merge | css.ts, themed brand pass | 2: P1 AA (validated ≠ emitted); P2 invalid-theme fallback | dark CTA (r1, r2) | 2 (F1) | 1 noted, not caught: the linear tracking curve between h3 and display-l was invented and flagged as such; no reviewer objected | no |
| P5 starter themes | vitrina, bloque, sereno, stress | 0 | all rounds | 1 | 0 caught. It flagged 5 unspecified fields (sereno frame, stress fields, rationale language) and took open-question defaults | no |
| P6 base.css | token layer, reduced motion, global rules | 2 (P2): unthemed compatibility in verify-1, and again in review 1 | r1 density, r5/r6 border weights | 3 (F2 Sonnet partial → G1 Opus) | 1: it invented no-theme defaults for button tokens and image ratios and flagged them; review 1 then showed the unthemed path drifted | yes, to Opus (G1) after 2 rounds |
| P7 component migration + check-motion | components, scripts/check-motion.ts | 3 (P2): check-motion gaps (verify-1); copied traversal (review 1); hard-coded 1px borders (verify-1, also critique r6) | r1-r6 (buttons, density, quick-add, labels) | 3 | 0 | no |
| P8 provider wiring | StorefrontProvider, layout, theme-init, USAGE.md | 1 (P2, docs): USAGE.md wrong command and claims; part of the invalid-theme fallback | — | 2 | 0 | no |
| P9 admin + personalization | brand editor, CONTEXT_SHAPES, prompts | 0. It shipped partial: routing.ts tsc break outside its files, fixed by I1 | — | 2 (I1) | 0 | no |
| P10 evidence + CLI + specs | theme-cli, specs, seeds, system map | 1 (gate): a11y spec reads unmapped in ci-plan (found by full gate receipt 4); plus the dev:reset hint missing --task (note) | — | 2 | 0 | no |
| Critique fixers r1-r3 (P11, Sonnet) | storefront visual fixes | — | 3 rounds, did not converge | escalated | 1: a price-weight proxy (`--sf-button-weight`) chosen without a SPEC value, flagged | yes, r4-r5 to Opus |
| Fix pieces I1, I2, F1-F5, G2, H2, J1, K1 (Sonnet) | review fixes | review 2 caught G2's rounding change (P2) and H2's helper copy was itself flagged once; all others passed their next review | — | 1 each, except G2 (→ H1 Opus) | 0 | G2 only |
**Opus escalations, each after 2 failed Sonnet rounds on the same item:**
1. Critique r4-r5: the Bodoni crossbars repeated r3 → r4.
2. G1, unthemed compatibility: verify-1 B3, then review 1.
3. H1, shared colour module: review 1, then review 2.
Each Opus piece passed its next review or critique on that item.
**Timeline gap, round-1 critique (≈15:00) to round-1 fixes (19:47):** the machine was suspended, not an agent stall. `journalctl` shows `The system will suspend now!` at 15:17:18 and `System returned from sleep operation 'suspend'` at 19:40:25 (Argentina time).
- The round-1 fixer was in the middle of a `themes.spec.ts` run when it started at 15:15. The tool call returned at 19:40, and the fixer finished at 19:46.
- Its active work was about 45 minutes. The rest (≈4h25m) was sleep.
- The same happened from 21:41 to 01:47, which looked like a hung round-6 critic.
- From 01:55 the run held a `systemd-inhibit` idle/sleep lock, which expires on its own. No config was changed.
**Why the Sonnet fixes in rounds 1-3 did not converge:**
1. **Each round fixed exactly the named items, and the critic then found the next layer.** r1 named dark CTA, button tokens and density. r2 found the CTA still dark-on-dark, because the fixer kept the SPEC's literal "fill never swapped" rule and added a ring. r3 found new issues the r2 fixes exposed: quick-add rendered as primary, Bodoni hairlines, and the price step. That is Sonnet's literal reading: it does what is named and doesn't generalise to the root cause.
2. **Where the root cause sat in files or SPEC text outside the brief's ownership, Sonnet worked around it or reported it instead of fixing it.** Examples: the SPEC 3.4 fill rule (SPEC not editable in r1/r2), the Bodoni opsz (fonts.ts not owned in r3; it applied the critic's opsz 40 pin and reported it insufficient), and the price weight (no SPEC field, so it used a proxy). Part of that is my brief scoping: I kept fonts.ts and the SPEC out of the visual fixers' files.
3. **When Opus was given the wider scope (fonts.ts, SPEC, base.css), the repeats closed in one round each.** It derived a principled opsz rule, amended SPEC 3.4, and rounded border widths to device pixels. That matches the agent-routing finding that a better agent fixes repeated misses where a longer brief rarely does.

### F22-02-admin-data-components (2026-10-12, effort medium, delegated builders) [ours]
Minutes and peak context come from the subagent transcripts: the span of transcript timestamps, and the peak input + cache tokens per call. They are approximate.
| Piece | Agent / model / effort | Min | Peak ctx | Rounds to pass | What failed | Escalated |
|---|---|---|---|---|---|---|
| Scouts ×3 + PLAN | workflow agents, Opus 5.5, medium | — | — | 1 | — | no |
| P0 types | Opus 5.5 medium | 1 | 52k | 1 | — | no |
| P1 tokens + Skeleton | sonnet-high (Sonnet 5.5, high) | 3* | 122k | 1 | none. It added `viz-seq-4-ink` and moved `ex-tech-2` (both flagged) | no |
| P2 geometry | sonnet-mid (Sonnet 5.5, medium) | 2* | 68k | 1 | review 1, B2 (count ticks), fixed by Opus | no |
| P3 format/metrics/period/feed/state | sonnet-high | 7 | 147k | 1 | review 1: B5 (duplicated date parsing), B4-class cheating note in feed.test, fixed by Opus | no |
| P4 motion + guard | sonnet-high | 4* | 111k | 1 | its scoped-styles FOLDERS edit was reverted by an integrator (folders empty at that point) and re-added later; review 1: B6 (copied parser) | no |
| P5 fixtures | Opus 5.5 medium | 16 | 254k | 1 | — | no |
| P6 chart primitives | sonnet-high | 21 | 344k | 1 | review 1: B2 (summary ticks) | no |
| P7 states | sonnet-high | 15 | 272k | 1 | critique r1: the error slab | → Opus fixer |
| P8 Kpi/Sparkline | sonnet-high | 25 | 398k | 1 | critique r1: figure separators (cross-cutting) | → Opus fixer |
| P9 Line/Area | sonnet-high | 16 | 294k | 1 | critique r2: axis labels at 360 (open) | open |
| P10 BarChart | sonnet-high | 26 | 367k | 1 | critique r2: empty state and x labels (open) | open |
| P11 Funnel | sonnet-high | 25 | 363k | 1 | nits only | no |
| P12 CohortGrid | sonnet-high | 17 | 273k | 1 | critique r1: unreadable at 360 (fixed by Opus in r1); review 1: B3 (Svelte easing) | → Opus |
| P13 DataTable | sonnet-high | 38 | 444k | 1 | review 1: B4 (footer sum precision) | no |
| P14 PeriodControl | sonnet-high | 21 | 300k | 1 | axe contrast in pending state (fixed by the integrator) | no |
| P15 Insight/LiveFeed | sonnet-high | 19 | 356k | 1 | critique: figures and retry (open) | open |
| P16 Approvals/OpsAlert | sonnet-high | 22 | 341k | 1 | critique: no retry, uniform CTA (open) | open |
| P17 Leaderboard/Attribution | sonnet-high | 16 | 312k | 1 | critique: empty state (open) | open |
| P18 gallery + harness | sonnet-high | 76 | 220k | 1 | axe findings in other files, fixed by the integrator | no |
| P19–P21 report migrations | sonnet-high | 11 / 18 / 14 | 281k / 375k / 341k | 1 | review 1: B1 (sales AOV legend, P19) | no |
| Integrators ×7, guard fixers ×3 (sonnet-mid) | Opus 5.5 medium; sonnet-mid medium | 1–11 | 50–129k | 1 | reverted a guard edit once (see P4) | no |
| Critique fixers r1 (×3), r2 (×3, interrupted) | Opus 5.5 medium | — | — | r1: cohort fixed, figures and states half fixed | per-component patches instead of one primitive | already Opus |
| Review-1 fixers ×5 | Opus 5.5 medium | ~10 | — | 1 (review 2 pass) | — | no |
| Critic r1, r2 | fable-high (Fable 5.1, high) | — | — | — | — | — |
| Code review | Codex `codex-review --xhigh` | — | — | review 1 fail → review 2 pass | — | — |
\* Very short spans (P1, P2, P4) probably mean only part of the transcript was captured. Treat them as lower bounds.
Lessons:
- Sonnet-high built every component in one pass, and all of them passed type and lint checks.
- Each review-1 defect was a cross-module issue: a wrong aggregation, a reuse violation, an edge of the type range. Literal briefs don't catch these.
- On critique, cross-cutting visual defects such as the figure separators were fixed per component, so they recurred. Make the shared primitive first.

### F21-03-core-sections (2026-10-12, effort medium, delegated builders) [ours]
Builder rule: `--builder sonnet`. Every buildable piece went to `sonnet-high` (Sonnet 5.5, high effort).
- Critics were `fable-high` (Fable 5.1, high effort). Deviation: task.md's "medium on every agent()" was not applied to critics.
- Planning, scouting and Mobbin reference agents were Opus 5.5.
- Code review was Codex only.
- Minutes and peak context are measured from each agent's transcript (first to last message; peak = input + cache tokens of the largest turn).
- "Codex findings" are attributed to the piece whose files they hit.
| Piece | Scope | Min | Peak ctx | Codex findings attributable | Critique rounds | Rounds to pass | Invented values caught | Escalated |
|---|---|---|---|---|---|---|---|---|
| P0a contracts | schemas, content validation | 10 | 230k | R1 minor ×1 (explicit `store_id` predicate had no test) | 0 | 1 | none; it stopped on missing copy maxLengths (resolved by D9b) | no |
| P0b shell | layout plumbing, theme-init | 6 | 177k | 0 | 0 | 1 | none (process slip: `git checkout` of its own file) | no |
| P0c literals | check-ui-literals detector | 5 | 139k | R1 major (custom-property gap); R2 major (layout gap); R3 major (decoration/ratio gap): the root of the failed acceptance | 0 | not passed | none | no |
| P0d seed | fixtures, seed | 4 | 147k | 0 | 0 | 1 | none | no |
| P0e motion reader | check-motion on shared reader | 1 | 54k | R1 major (missing `Comment` type broke root tsc) | 0 | 2 | none | no |
| P1 ProductCard v2 | card, CardAction | 14 | 279k | R2 major (part of the 53 layout literals) | 1 (round-2 #3, unfixed) | not passed (critique) | none | no |
| P2 BuyBox | buy block | 26 | 408k | R1 major (shared alert ids, with I1); R2 major (0.5rem, 24rem); R3 major (underline em values) | 1 (round-2 #2, unfixed) | not passed | none | no |
| P3 Header | 3 header variants | 37 | 485k | R2 major (layout literals); R3 major (2px floor) | 0 | not passed | none | no |
| P4 Hero | 3 hero layouts | 39 | 420k | R2 major (85svh); R3 major (`aspect-ratio: 4 / 5`) | 2 (scrim) | not passed | none | yes: scrim went to Opus after 2 failed rounds (P4, then C1); the fix was interrupted |
| P5 Product grid | grid, FLIP | 24 | 427k | R2 major (layout literals) | 1 (story tile) | not passed (critique) | none | no |
| P6 Featured product | 3 variants | 19 | 362k | R1 major (Stage clamp) | 0 | 2 | none | no |
| P7 Image+text | 3 variants | 13 | 270k | R1 major (clamp min-block) | 1 (colour-panel, fixed by C3) | 2 | none | no |
| P8 Footer | 2 variants | 22 | 308k | R1 major (1px, 12.5rem); R3 major (LinkGroup underline) | 0 | not passed | none | no |
| P9 Gallery | /dev/sections | 12 | 256k | R1 minor (route guard untested) | 0 | 2 | none | no |
| I1 integration | cart add, BuyBox options, footer, USAGE | 17 | 316k | R1 major (BuyBox not passing the new idPrefix, shared with P2) | 0 | 2 | none | no |
| P10 live mount | +layout.svelte | 14 | 159k | 0 | 0 | 1 | none | no |
| P11 browser specs | 5 specs + evidence | 54 | 408k | R1 minor (ring contrast Infinity) | 0 | 2 | none | no |
| P12 system map | feature-steps, story | 5 | 183k | 0 | 0 | 1 | none | no |
| F1 M35 + h1 | reveal.ts, gallery | 4 | 65k | 0 | 0 | 1 | none | no |
| F2 perf | code splitting | 49 | 314k | R1 minor ×2 (unthemed chrome guard untested; USAGE boolean props) | 0 | 2 | own values: a 6000-byte split threshold in vite.config.ts | no |
| H1 harness | full-width shots | 5 | 103k | 0 | 0 | 1 | none | no |
| C1 hero scrim | round-1 fix | 39 | 175k | 0 | 1 (partial) | failed (round 2) | own feather values (96/144px) | yes (to Opus E1) |
| C2 story tile | round-1 fix | 8 | 107k | 0 | 1 | partial (type coverage) | none; it stopped on the unreachable one-third rule | no |
| C3 colour panel | round-1 fix | 22 | 130k | 0 | 1 | 1 (critic confirmed) | none | no |
| R2b BuyBox / R2c card action | round-2 fixes | 14 / 14 | 158k / 117k | n/a (interrupted by the pause; dropped) | — | — | — | no |
| K1 types, ids, tokens | review-1 fixes | 4 | 103k | R2 major (its token sweep covered only custom properties) | 0 | 1 | none | no |
| K2 guard tests, docs | review-1 fixes | 4 | 91k | 0 | 0 | 1 | none | no |
| K3 sizing tokens | review-2 fixes | 5 | 100k | R3 major (detector still a property allowlist) | 0 | 1 (for its scope) | none | no |
Opus pieces:
| Piece | Min | Peak ctx | Outcome |
|---|---|---|---|
| E1 hero scrim (escalation, high) | 14 | 157k | Interrupted by the pause; dropped unverified |
| feasibility plan | 13 | 247k | FEASIBLE |
| refs ×6, scouts ×3 | 1-5 each | — | — |
Fable critics:
| Round | Min | Peak ctx | Verdict |
|---|---|---|---|
| 1 | 12 | 279k | majors-remain |
| 2 | 13 | 274k | majors-remain |
Sonnet observations:
- Sonnet builders were reliable on fully specified logic and tests: every red-to-green test written first held, and Codex found
  no cheating.
- Sonnet missed in two places:
  - **Detectors as the definition of done.** Builders treated "the detector passes" as "tokens only" (P0c, P2, P3, P4, P8).
  - **The one open-ended taste piece.** The hero scrim needed the Opus escalation.
- Concurrent Playwright runs in one worktree clashed: a shared outputDir, and specs flipping the shared demo store's theme.
  Serialize specs per worktree.

### F23-02-private-draft-stores (2026-10-14, effort medium, risky) [ours]
Wall-clock is each subagent transcript's first-to-last timestamp span. Peak context is the largest cache_read_input_tokens + input_tokens. No compactions occurred.
| Piece | Agent type / model / effort | Rounds to pass | What failed | Escalation | Wall-clock (min) | Peak context |
|---|---|---|---|---|---|---|
| Plan (feasibility + plan) | default / Opus 5.5 / high | 1 | — | — | 13.3 | 219k |
| Plan critic | default / Opus 5.5 / high | 1 | It found the shared test-file conflict, regen command, missing re-entry tests and route-registry assertion; all were adopted | — | 9.3 | 170k |
| P1 migration + launch.ts | default / Opus 5.5 / medium | 1 (verify panel and Codex found no P1 defect) | Its `updatedAt` comment went stale (verify panel minor) | — | 4.1 | 96k |
| P2 checkout guards + tests | default / Opus 5.5 / medium | 2 | Codex r1: vacuous `launchEvents` store forwarding in the shared test helper | No (an Opus fixer fixed the class) | 4.1 | 107k |
| P3 launch route + contracts + admin | sonnet-high / Sonnet 5.5 / medium | 1 | It extended the same shared helpers, where the r1 defect sat; P2/P3 share it | — | 5.9 | 84k |
| P4 storefront draft gate | default / Opus 5.5 / medium | 2 | It broke the offline abuse harness (500s); I fixed it inline with an injectable dep. Verify panel: storeSelector missing from the leak scan | — | 4.6 | 117k |
| P5 seed draft option | sonnet-mid / Sonnet 5.5 / medium | 1 | — | — | 1.2 | 52k |
| P6 system map | sonnet-mid / Sonnet 5.5 / medium | 4 | Stale refs (verify panel), 29 new-feature warnings (Codex r2), journey-null class (Codex r3) | Yes: the r3 repeat went to Codex gpt-6.1-sol high as executor, which passed review 4 | 1.3 (+0.6 r2 fix, Sonnet) | 97k (r2 fixer 58k) |
| Verify panel (5 lenses) | default / Opus 5.5 / high | — | — | — | 3.3–9.8 | 91k–150k |
| Verify-panel fixer | default / Opus 5.5 / medium | 1 | — | — | 10.2 | 173k |
| Codex r1 fixer | default / Opus 5.5 / medium | 1 | — | — | 6.7 | 117k |
| Code review, rounds 1-4 + evidence | Codex (`codex-review --xhigh`) | — | — | — | — | — |
Takeaways:
- Sonnet for system-map journey judgement missed README's "null only for…" rule twice. Brief the rule's scope explicitly, or route it straight to Opus or Codex.
- Opus builders writing test helpers with optional store parameters left one forward unpassed, and only Codex's RLS-aware mutation caught it. Future briefs should ask for every absence assertion to be mutation-proven before reporting.

### F23-02-B-private-draft-assets (2026-10-14, effort medium, risky) [ours]
Wall-clock and peak context come from the subagent transcripts (peak = max `cache_read_input_tokens` + `input_tokens`); none compacted.
| Piece | Agent type / model / effort | Rounds to pass | What failed / escalation | Wall-clock | Peak ctx |
|---|---|---|---|---|---|
| Plan (feasibility + size) | opus-medium / Opus 5.5 / high | 1 | none | 17.0 min | 242k |
| P1 API gate core | sonnet-high / Sonnet 5.5 / medium | 3 (guard review, R1) | HEAD/early-route enumeration; account runtime coverage | 2.7 min (+F1 4.9, R1 api 3.0, R2 2.4) | 88k (109k) |
| P2 route-walk test | sonnet-high / Sonnet 5.5 / medium | 2 | observer-based enumeration (guard review) | 2.4 min | 73k |
| P3 contracts | sonnet-mid / Sonnet 5.5 / medium | 1 | none | 1.2 min | 72k |
| P4 merchant asset route | sonnet-high / Sonnet 5.5 / medium | 3 | visibility filter unpinned; duplicated serve logic and fixture (R1) | 1.9 min (+F2 1.3) | 77k |
| P5 admin proxy | sonnet-mid / Sonnet 5.5 / medium | 3 | overlapping guards untested; body check and storeOf pin (R1 notes) | 1.7 min (+R1 admin 1.8) | 73k |
| P6 admin consumers | sonnet-mid / Sonnet 5.5 / medium | 2 | tautological wiring test; src moved into server load (F3 1.9) | 2.1 min | 69k |
| P7 system map | sonnet-mid / Sonnet 5.5 / medium | 3 | stale refs after contract and code shifts (verify, R1) | 2.1 min (+F4 7.1, R1 docs 1.9) | 95k (107k) |
| Verify panel ×5 | opus-medium / Opus 5.5 / high | n/a | 13 confirmed findings | 4.4–9.1 min | 102–137k |
| Reviews | Codex Sol (`codex-review --xhigh`) | guard FAIL, R1 FAIL, R2 PASS, fix-limited PASS, evidence PASS | no fallback to fable-high | n/a | n/a |
