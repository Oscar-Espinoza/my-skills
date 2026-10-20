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

### F21-04-flagship-themes (2026-10-15, effort medium, delegated builders) [ours]
All agent() calls ran at medium effort, except: the builders, set per piece (sonnet-high is high effort by its type; executors were chosen per the run's delegated-builder rule); the fable-high critics, at high effort (the acceptance names fable-high); and the Codex executors, at high effort. No transcript compacted (0 compactions in every subagent transcript). Wall-clock minutes and peak context (largest cache_read + input tokens) come from the subagent transcripts under `~/.claude/projects/<worktree>/<session>/subagents/`.
### Pieces
| Piece | Agent / model / effort | Rounds to pass | What failed | Escalation | Wall min | Peak ctx |
|---|---|---|---|---|---|---|
| Feasibility plan | Opus 5.5 / medium | 1 | — | — | 10 | 231k |
| Mobbin references | Opus 5.5 / medium | 1 | the preferred brands (Aesop, COS, Hay…) were not on Mobbin | — | 5 | 162k |
| P0 direction (4 directions × 3 homes, specs) | Opus 5.5 / medium | 1 | 3 SPEC copy lines amended (no coffee in the seed) | — | 21 | 404k |
| P1 contract | sonnet-high | 2 | guard-1: schema constraints that no fixture exercised (surviving mutants) | — | 2 | 75k |
| P2 template validator | sonnet-high, then Codex gpt-6.1-sol / high | 4 (guard 1, 2 failed; Codex fixes; VERIFY closed guard 3) | content shapes, moment hosts, hostile JSON, invisible-character bypass, surviving mutants; then renderer agreement and raw IDs | to the Codex executor after the same kind came back (guard 2) | 5 + 19 | 146k / 257k |
| P3 seed landing pages | sonnet-high | 1 | — | — | 2 | 65k |
| P4 dev template routes | sonnet-high | 1 | VERIFY note: cookie never-read was untested (added) | — | 5 | 126k |
| P5 moments M39/M40 | sonnet-high | 2 | motion spec unrun at build time; 10/27 failed later (spec drove the old cart markup; 1 real bug: missing space in "Total:") | — | 11 | 214k |
| Motion spec fix | sonnet-high | 1 | — | — | 10 | 112k |
| P6a cards/listing | sonnet-high | 2 | raw `1.5rem` literal; the "false choice" class came back in critic round 2 | that class to Opus | 5 | 127k |
| P6b theme/sections | sonnet-high | — | hero scrim shape not landed (critic round 1) | hero to Opus | 5 | 137k |
| P6c product (BuyBox, M11, PDP) | sonnet-high | 1 | transient unclosed `<div>` mid-edit | — | 7 | 198k |
| P7 evidence harness | sonnet-high | 2 | VERIFY: copied axe helpers (blocking); escapeHtml copy | — | 5 | 122k |
| P8 system map | sonnet-mid | 1 | — | — | 0 | 46k |
| I1 brand snapshot re-record | sonnet-mid | 1 | — | — | 1 | 46k |
| R1 cart lines | sonnet-high | 2 | review 1: cart DB test regression (cart page read `data.brand`), fixed by the orchestrator | — | 17 | 221k |
| R1 hero scrim | Opus 5.5 / medium | 2 | strength still too dark (critic round 3, review 1) | already Opus | 12 | 167k |
| R1 editorial-mix tile | sonnet-high | 1 | — | — | 26 | 139k |
| R2 PDP buy column + M47 | sonnet-high | 2 | review 1: M47 reduced path untested (blocking); added an unrequested 4s add-result swap | — | 12 | 191k |
| R2 false choice (option plan) | Opus 5.5 / medium | 1 | — | escalated from P6a | 14 | 205k |
| R2 media frames | sonnet-high | 1 | edited BuyBox.svelte outside its ownership (bar rules only) | — | 4 | 111k |
| VERIFY fixes | sonnet-high | 1 | — | — | 56 | 233k |
| RV1 hero (scrim strength, copy) | Opus 5.5 / medium | 1 | stopped once by accident and resumed | — | 20 | 212k |
| RV1 controls (QuantityStepper, sort) | sonnet-high | 1 | — | — | 17 | 157k |
| RV1 grid/gallery/count | sonnet-high | 1 | — | — | 8 | 168k |
| M47 test fix + mutation proofs | sonnet-high | 1 | the Codex-written test (unrunnable in its sandbox) read the tokens before the reduced branch | — | 8 | 78k |
| Gate fixes (ci-plan, literals) | Opus 5.5 / medium | 1 | — | — | 10 | n/a |
| Critic rounds 1–3 | Fable 5.1 (fable-high) / high | 3 (cap) | majors every round | — | 10 / 10 / 12 | 261k / 191k / 296k |
| Codex executors (guard 2, guard 3, review 1 tests, review 2 ×2, review 3 ×2) | gpt-6.1-sol / high | 1 each | browsers could not run in the Codex sandbox (mutation proofs redone by sonnet-high) | — | n/a | n/a |
### Sonnet pieces: Codex findings and critique
| Sonnet piece | Codex findings attributable (count, severity) | Critique rounds touching it | Rounds to pass | Invented values caught | Escalated |
|---|---|---|---|---|---|
| P1 contract | guard-1: 1 blocking (unexercised schema constraints); guard-2: 2 (version min, layout extra keys) | — | 2 | its own bounds (id ≤60, home ≤12, assets ≤20), reported as not from the spec | no |
| P2 validator | guard-1: 5 blocking; guard-2: 5 blocking (duplicated SECTION_CONTENT copy, hostile JSON, renderer agreement) | — | not by Sonnet | none | yes, to the Codex executor |
| P3 seed | 0 | — | 1 | none (copied by script from direction.md) | no |
| P4 routes | 0 blocking; 1 note (cookie read untested) | — | 1 | none | no |
| P5 moments | 0 Codex; 10 browser failures (9 spec drift, 1 real) | — | 2 | none | no |
| P6a cards/listing | 0 Codex; critic round 2 major (false choice) | rounds 1, 2 | — | changed a fallback label to "Elegí una opción" (reported) | yes, class to Opus |
| P6b theme/sections | gate: 1 (literal exemption, later Opus code) | round 1 (hero) | — | none | yes, hero to Opus |
| P6c product | 0 | round 1 (BuyBox states) | 1 | none | no |
| P7 harness | VERIFY: 1 blocking (copied axe helpers); review 1: escapeHtml copy (orchestrator) | — | 2 | none | no |
| P8 system map (sonnet-mid) | 0 | — | 1 | none | no |
| I1 snapshot (sonnet-mid) | 0 | — | 1 | none (every diff explained against direction.md) | no |
| R1 cart | review 1: 1 blocking (cart DB regression) + 1 note (catalogue scan cost) | round 1 item 1 resolved in round 2 | 2 | none; found the stale "no title" comment | no |
| R1 grid tile | review 1: 1 design (open ruled cell, a different defect) | round 1 item 3 resolved in round 2 | 1 | none | no |
| R2 PDP | review 1: 1 blocking (M47 coverage) | round 2 item 1 resolved in round 3 | 2 | added an unrequested 4s add-result message | no |
| R2 media | 0 | round 2 item 3 resolved in round 3 | 1 | none | no |
| VERIFY fixes | review 1: 0 new | — | 1 | none | no |
| RV1 controls | 0 | — | 1 | none | no |
| RV1 grid | review 2: 1 blocking (duplicated fixture selection in grid.test.ts) | — | 2 (via Codex) | none | reuse class to Codex |
| Motion fix, M47 test fix | 0 | — | 1 | none | no |

### F23-01-A-sign-up-server (2026-10-15, effort medium, risky) [ours]
| Piece | Agent / model / effort | Rounds | What failed / escalation | Wall-clock | Peak context |
|---|---|---|---|---|---|
| PLAN (delta + feasibility) | workflow subagent, Opus 5.5, high | 1 | — | 8 min | 188k |
| P1+P2 data + service | workflow subagent, Opus 5.5, medium | 3 (verify, R1, R2) | Burn/dedupe and budget defects (R1), reuse (R1) | 5 min | 124k |
| P3 contract | workflow subagent, Opus 5.5, medium | 2 | Fixture password tripped the secrets scan in the full gate | 4 min | 118k |
| P4 API wiring | workflow subagent, Opus 5.5, medium | 1 (verify) | Wiring untested (verify) | 9 min | 161k |
| P5 tests | workflow subagent, Opus 5.5, medium | 3 | Coverage gaps (verify), helper duplication (R1, R2) | 11 min | 152k |
| P8 system map | workflow subagent, Opus 5.5, medium | 3 | Stale gap and citations (R1); mis-mapped citations (R2) | 2 min | 76k |
| Verify: reproduce / guards / wiring / cheating / docs | workflow subagents, Opus 5.5, high | 1 | — | 11 / 12 / 7 / 6 / 5 min | 130k / 154k / 131k / 109k / 137k |
| Verify fixer | workflow subagent, Opus 5.5, medium | 1 | — | 14 min | 160k |
| Round 1 fixer | workflow subagent, Opus 5.5, medium | 1 | — | 9 min | 159k |
| Round 2 fixer | Codex gpt-6.1-sol, high (escalated: same kinds a second time) | 1 | Its sandbox blocked the DB tests and `pnpm check`; the coordinator re-ran them (pass) | not measured | not measured |
| Reviews | Codex (`codex-review --xhigh`): 3 full rounds, 2 fix-limited reviews, 1 evidence check | — | Codex was available every time; no fallback was used | — | — |
- No subagent was compacted.
- Wall-clock is the first-to-last timestamp in each subagent transcript.
- Peak context is the largest `cache_read_input_tokens + input_tokens`.

### F23-03-A-create-store-api (2026-10-15, effort medium, risky) [ours]
| Piece | Agent type / model / effort | Rounds | What failed / escalation | Wall clock | Peak context |
|---|---|---|---|---|---|
| PLAN (feasibility, delta) | workflow subagent / Opus 5.5 / high | 1 | none | 9.4 min | 237,827, no compaction |
| P1 platform + migration + lifecycle | workflow subagent / Opus 5.5 / medium | 2 (fixed in round 1) | regression: createStore validated after opening its transaction (direct gate 1). Missing tests: grants, storeDb guards, slug race. No escalation | 6.0 min | 137,175, none |
| P2 contracts + audit ops | sonnet-mid / Sonnet 5.5 / medium | 1 (+1 orchestrator fix) | wrong 409 fixture code (`ATTEMPT_REUSED`), yaml text said another caller gets 409; fixed inline by the orchestrator | 2.2 min | 79,358, none |
| P3 API module + tests | workflow subagent / Opus 5.5 / medium | 3 | the guards were weak (intermittent cross-principal replay, no real audit failure injection, serial-passable concurrency, Δ2 blind spots), no merchantUserId reuse, then a duplicated polling loop (fixed by the orchestrator) | 9.1 min | 185,444, none |
| P4 system map | sonnet-mid / Sonnet 5.5 / medium | 2 | out-of-range citations (it cited lines from an older file layout) | 1.1 min | 84,674, none |
| Verify panel (5 lenses) | workflow subagents / Opus 5.5 / high | 1 | n/a | 3.3–8.5 min each | 95,222–131,473, none |
| Fixer round 1 | workflow subagent / Opus 5.5 / medium | 1 (one item left over, see review-1) | none | 19.2 min | 243,567, none |
| Merge system-map resolver | workflow subagent / Opus 5.5 / medium | 1 | none | 3.9 min | 106,636, none |
| Reviews (guards, 1, 2, 3, evidence) | Codex `codex-review --xhigh` | 5 calls | none unavailable (no exit 75) | not measured | n/a |

### Shop canvas build, Cardón store (2026-10-15) [ours]
- **Setup:** an Opus-medium planner wrote 44 piece specs. The workflow gave each piece a fresh sonnet-high builder (opus-medium for 3 taste pieces) and an opus-medium screenshot critic, up to 3 rounds, escalating to Opus in round 3. Codex `gpt-6.1-sol` high reviewed each flow, with one fix round.
- **Outcome:**
  - Critic: 39/44 passed. Rounds: 5 pieces passed in 1, 18 in 2, 16 in 3; 5 were capped (gallery, cart-summary, product-grid, listing page, PDP page).
  - Codex: every flow still FAIL after its fix round, on should-fix items only (a11y, duplicate ids, 15px mobile text).
  - `check.js`: 0 fails across 73 files.
- **Cost:** 229 agents, about 16.0M subagent tokens, 50 minutes. The single stopped sonnet-high attempt used 0.63M for 40 sections and no pages.
- **Lessons:**
  1. A critic bar of "pass only when nothing above nit remains" sends most pieces to 3 rounds. Use "no major issues", 2 rounds max, and record nits without fixing them.
  2. Every round re-reads big screenshot sets with Opus. Critique per flow, or per page in batches, not per section, and cap the number of crops.
  3. Escalating to Opus in round 3 rarely closed the capped items, which were spec conflicts (filter counts, sticky bar over the price). Route those to the planner, not a stronger builder.
  4. This pattern buys quality per piece at about 25x the tokens. Size the critique budget before launching.

### F23-12-D-live-product-sources (2026-10-16, effort medium) [ours]
Peak context = largest `cache_read_input_tokens` + `input_tokens` in the subagent transcript. No piece had a compaction.
| Piece | Agent type | Model | Effort | Rounds to pass | What failed / escalation | Wall-clock min | Peak context |
|---|---|---|---|---|---|---|---|
| Feasibility plan | Plan | Opus 5.5 | medium | 1 | It could not write `plan.md` because it is read-only; I wrote it from the agent's output | 7.9 | 163k |
| P1 contract | sonnet-mid | Sonnet 5.5 | medium | 1 | The plan's schema form failed AJV strict; the builder found the `if`/`else` form | 1.9 | 73k |
| P2 content + API | sonnet-high | Sonnet 5.5 | medium | 2 (with the verify fix) | The DB length assertion was loose (2..4); made exact in the fix | 2.7 | 87k |
| P3 SDK + storefront | sonnet-mid | Sonnet 5.5 | medium | 3 | Guard gaps found by the verify panel; then the dropped fallback (Codex round 1), fixed by the coordinator | 1.4 | 77k |
| P4 system map | sonnet-mid | Sonnet 5.5 | medium | 1 | none | 0.6 | 65k |
| Verify panel (5 lenses) | sonnet-high | Sonnet 5.5 | medium | n/a | The reproduce lens's scratch copy shared the gitdir and altered the index; it ended clean | 0.8 / 0.8 / 0.8 / 6.3 / 1.1 | 50–95k |
| Verify fix | sonnet-high | Sonnet 5.5 | medium | 1 | It introduced the slot-0 regression that Codex caught | 3.7 | 82k |
| Codex round 1 fix | coordinator (main loop) | Opus 5.5 | session | 1 | none; it passed Codex round 2 | ~10 | n/a |
| Reviews | codex-review (Codex Sol 6.1) | — | — | round 1 fail, round 2 pass, evidence pass | Codex was available (no exit 75), so no fallback | — | — |

### F23-06-A-preferences-api (2026-10-16, effort medium, risky) [ours]
Measured from subagent transcripts (first to last timestamp; peak = largest `cache_read_input_tokens` + `input_tokens`). No compaction anywhere.
| Piece | Agent / model / effort | Rounds to pass | Failed / escalation | Wall-clock | Peak context |
|---|---|---|---|---|---|
| PLAN (feasibility + plan.md) | workflow agent, Opus 5.5, high | 1 | — | 11 min | 235k |
| B1 data + platform | workflow agent, Opus 5.5, medium | 1 | — | 3 min* | 104k |
| B2 contracts | workflow agent, Opus 5.5, medium | 1 | one contract test (403 wording on PUT) fixed in-piece | 3 min* | 86k |
| B3 API + system map | workflow agent, Opus 5.5, medium | 1 | — | 7 min* | 148k |
| Verify: reproduce / guards / wiring / cheating / docs | workflow agents, Opus 5.5, high | 1 | no blocking; notes only | 6 / 12 / 8 / 4 / 3 min | 92k / 127k / 120k / 83k / 90k |
| Verify-panel fixes | workflow agent, Opus 5.5, medium | 1 | — | 6 min | 97k |
| Codex round 1 fix | workflow agent, Opus 5.5, medium | 1 (but missed a test duplicate) | duplicate-helper kind recurred in round 2 | 5 min | 93k |
| Codex round 2 fix | Codex gpt-6.1-sol, high (executor) | 1 (missed another test duplicate) | recurred in round 3 | ~6 min | n/a (Codex, 209k tokens used) |
| Codex round 3 fix | Codex gpt-6.1-sol, high (executor) | 1 | review 3b PASS | ~8 min | n/a (Codex, 159k tokens used) |
| Admin date-test fix | coordinator (Opus 5.5) | 1 | review 4 PASS | ~3 min | — |
| Reviews 1, 2, 3, 3b, 4, evidence | Codex `codex-review --xhigh` | — | — | — | — |
\* The transcript timestamps cover only the agent's active span; the B pieces ran inside a 23-min workflow that also included the verify panel.
Coordinator mistake: after receipt 3 I first scheduled a 3-hour wait for midnight ART instead of fixing the time-of-day test bug. Oscar called it out, and I replaced it with the fix in 4a4dc5bfd.

### F99-53-catalog-declaration-build (2026-10-17, effort medium, risky) [ours]
- P1 (type annotation) and P2 (proof builds): built by me (Claude Opus 5.5, main session), 1 attempt, nothing failed.
- Review: Codex gpt-6.1-sol xhigh, 1 attempt, pass.

### F99-52-sandbox-app-test-hook-speed (2026-10-17, effort medium, delegated builders) [ours]
| Piece | Agent / model / effort | Rounds to pass | Failures / escalation | Wall min | Peak context |
|---|---|---|---|---|---|
| A: fixtures helper, sandbox-app, seed-fixtures test, app.test it.each | sonnet-mid / Sonnet 5.5 / medium | 1 build + guard-fix round (shared) | none; guard gaps fixed by sonnet-mid | 1.4 | 65.6k, no compaction |
| B: runner timeouts, check default, pin test, system map | Opus 5.5 subagent / medium | 1 build + guard-fix round | none | 2.2 | 83.3k, no compaction |
| Guard fixes (verify review) | sonnet-mid / Sonnet 5.5 / medium | 1 | none (one self-caught wrong assertion, fixed before reporting) | 1.8 | 64.3k, no compaction |
Reviews: Codex gpt-6.1-sol xhigh (verify-1, review-1). No Claude reviewers.

### F99-58-hosted-build-once (2026-10-17, effort medium, risky) [ours]
- P1-P6 (all pieces): built by the run owner, Claude Opus 5.5 (medium), 1 review attempt, passed; nothing failed.
- Review: Codex gpt-6.1-sol xhigh, attempt 1 pass.

### F99-68-fixture-role-restore (2026-10-17, effort medium, risky, delegated builders) [ours]
Wall-clock is from the first to the last transcript timestamp. Peak context is the largest `cache_read_input_tokens` + `input_tokens`. None of the agents compacted.
| Piece | Agent / model / effort | Rounds to pass | What failed / escalation | Wall-clock | Peak context |
|---|---|---|---|---|---|
| PLAN | workflow default (Opus 5.5), high | 1 | none | 10.7 min | 168.6k |
| B1 helper + unit test + check-ci | opus-medium (Opus 5.5), medium | 3 | Guard review: PG verifier fidelity, unlock-after-commit, failure coverage → B1-fix (opus-medium, 10.5 min, 145.1k). VERIFY: recovery outside the lock (same class a second time) → escalated to Codex exec gpt-6.1-sol high | 4.5 min, plus 10.5 min (fix), plus Codex exec (time not measured) | 100.2k (fix 145.1k) |
| B2 jobs fixtures | sonnet-mid (Sonnet 5.5), medium | 1 | none | 1.0 min | 81.8k |
| B3 connectors fixtures | sonnet-high (Sonnet 5.5), medium | 1 | none | 1.3 min | 82.8k |
| B4 worker precondition | sonnet-mid (Sonnet 5.5), medium | 1 | none | 0.6 min | 63.2k |
| B5 gate text, docs, map | sonnet-mid (Sonnet 5.5), medium | 1 | none | 0.6 min | 74.9k |

### F99-70-ship-policy-docs (2026-10-17, effort medium, delegated builders) [ours]
| piece | ticket | agent type | model | effort | rounds to pass | failed / escalation | wall min | peak context (tokens) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| plan F99-70 | F99-70 | workflow default | Opus 5.5 | medium | 1 | – | 5.2 | 181,553 |
| plan F99-69 | F99-69 | workflow default | Opus 5.5 | medium | 1 | – | 4.1 | 121,199 |
| B1 policy docs | F99-70 | opus-medium | Opus 5.5 | medium | 2 | VERIFY B2 (gate mode unqualified) | 2.0 | 96,381 |
| B1-fix B2 docs mode | F99-70 | opus-medium | Opus 5.5 | medium | 1 | – | 1.9 | 64,782 |
| B2 attrs + required wording | F99-70 | sonnet-mid | Sonnet 5.5 | medium | 1 | – | 0.4 | 48,326 |
| B3 gate summary + test | F99-70 | sonnet-mid | Sonnet 5.5 | medium | 1 | – | 1.0 | 55,577 |
| B4 sign-in matcher | F99-69 | sonnet-high | Sonnet 5.5 | high | 1 | – | 3.5 | 55,200 |
| B5 credit-note move | F99-69 | sonnet-high | Sonnet 5.5 | high | 2 | VERIFY B1 (masked by shared claim) → fix moved up to Opus | 0.4 | 58,394 |
| B5-fix B1 | F99-69 | opus-medium | Opus 5.5 | medium | 1 | – | 1.8 | 59,145 |
| B6 --migrations-base | F99-69 | sonnet-high | Sonnet 5.5 | high | 1 | – | 1.9 | 70,635 |
| B7 system map | F99-70, F99-69 | sonnet-mid | Sonnet 5.5 | low | 1 | – | 0.3 | 44,292 |
| VERIFY review | both | codex-review | Codex Sol 6.1 | xhigh | – | found B1, B2 | 4 (prompt-file mtime to JSON mtime) | unavailable |
| Codex round 1 | both | codex-review | Codex Sol 6.1 | xhigh | pass | – | 4 (prompt-file mtime to JSON mtime) | unavailable |
No compaction in any subagent transcript. Peak = largest cache_read_input_tokens + input_tokens. Workflow totals (harness): plan 306k subagent tokens / 5.4 min; build 438k / 4.3 min; fix 125k / 2.0 min.

### F99-71-A-shared-selector-plan (2026-10-17, effort medium, delegated builders) [ours]
Peak context = largest `cache_read_input_tokens + input_tokens` in each subagent transcript (~/.claude/projects/<worktree>/…/subagents/). Codex executor token counts come from the "tokens used" line of the `codex exec` log. No compactions were observed.
| piece | ticket | agent type / model / effort | rounds until passed | what failed | escalation | wall min | peak context |
| --- | --- | --- | --- | --- | --- | --- | --- |
| plan (read-only) | both | opus-medium / Opus 5.5 / medium | 1 | none | - | 11.1 | 217,948 |
| A1 selection + check:ci json + golden | F99-71-A | opus-medium / Opus 5.5 / medium | guards review then fixed | G1, G4, G5 guard gaps | - | 5.6 | 130,023 |
| A2 gate --plan + CLI test + docs | F99-71-A | opus-medium / Opus 5.5 / medium | guards review, VERIFY-1, R1-R2 | G2, G3 gaps; .git/index write | - | 4.2 | 106,920 |
| B1 required rules/protected data | F99-71-B | opus-medium / Opus 5.5 / medium | guards review, VERIFY-1 | G6-G9 gaps; R3, R4 | - | 13.3 | 217,611 |
| fix A guards G1-G5 | F99-71-A | opus-medium / Opus 5.5 / medium | 1 | - | - | 23.4 | 148,719 |
| fix B guards G6-G9 | F99-71-B | opus-medium / Opus 5.5 / medium | 1 | - | - | 27.6 | 171,177 |
| B2 --required plumbing + DB case + docs | F99-71-B | opus-medium / Opus 5.5 / medium | VERIFY-1 (R5) then pass | exit verdict unguarded | - | 11.0 | 190,538 |
| fix VERIFY-1 R1-R5 | both | opus-medium / Opus 5.5 / medium | round 1 found P2 (split index) | partial read-only fix | - | 12.3 | 162,885 |
| fix round-1 P2 split index | F99-71-A | opus-medium / Opus 5.5 / medium | round 2 found 2 more read-only escapes | inherited config; sweep ownership | moved to Codex (same kind recurred) | 11.7 | 129,598 |
| fix round-2 / FR3 / FR4 / FR5 | F99-71-A | Codex exec / gpt-6.1-sol / high | 4 fix passes; approved in focused review 7 | parity, GIT_DEFAULT_HASH, TMPDIR edge cases | - | ~10, 7, 5, 4 (file mtimes) | tokens used 225,986 / 133,196 / 139,889 / 108,876 |
| reviews (guards, VERIFY-1, R1, R2, FR3-FR7) | both | codex-review --xhigh / gpt-6.1-sol | 9 reviews | - | - | unavailable | unavailable |

### F99-72-no-any-type-safety (2026-10-17, effort medium, delegated builders) [ours]
Wall-clock is first to last transcript timestamp. Peak context is the largest `cache_read_input_tokens` + `input_tokens`. No agent compacted.
| Piece | Agent / model / effort | Rounds to pass | What failed / escalation | Wall min | Peak ctx |
|---|---|---|---|---|---|
| PLAN draft | workflow default / Opus 5.5 / medium | 1 (+ Codex challenge/converge) | none | 17.6 | 240.1k |
| P1 checker | workflow default / Opus 5.5 / medium | failed guard 1 (13) and guard 2 (9) | Fix 1 by Opus medium (32.2 min, 252.9k). Recurred → Codex gpt-6.1-sol high (guard 2), then ultra (reviews 1 and 2, owner decision). The review-2 ultra fix was reverted after focused review 3. | 24.9 | 244.5k |
| P2 admin core | Opus 5.5 / medium | 1 (seams fixed in integration) | none | 29.0 | 275.6k |
| P3a admin lib | sonnet-high / Sonnet 5.5 / medium | 1 | none | 7.5 | 216.3k |
| P3b admin routes | sonnet-high / Sonnet 5.5 / medium | 1 | none | 16.9 | 342.4k |
| P3c admin settings | sonnet-high / Sonnet 5.5 / medium | 1 | blocked on the contract type gap (fixed in integration) | 12.8 | 297.4k |
| P3d admin rest | sonnet-high / Sonnet 5.5 / medium | 1 | blocked on the `$defs` generator bug (fixed in integration); it edited the P2-owned operator registry (accepted) | 13.6 | 276.7k |
| P3z remove old surface | sonnet-high / Sonnet 5.5 / medium | 1 | none | 2.9 | 96.6k |
| P4 SDK decoders | Opus 5.5 / medium | VERIFY found 10 guards untested → sonnet-high fixer (1.5 min, 74.0k) | none | 24.9 | 229.5k |
| P5 sample-app | sonnet-high / Sonnet 5.5 / medium | 1 | none | 2.6 | 56.6k |
| P6a ranks 2, 8 | sonnet-high / Sonnet 5.5 / medium | 1 | none | 1.1 | 58.1k |
| P6b ranks 5, 6 | Opus 5.5 / medium | VERIFY found the identifier guard untested → sonnet-mid fixer (0.9 min, 51.7k) | none | 7.4 | 91.8k |
| P7a api helper | Opus 5.5 / medium | 1 | none | 26.9 | 316.1k |
| P7b api Json files | sonnet-high / Sonnet 5.5 / medium | 1 | none | 16.1 | 235.6k |
| P7c Svelte helpers | sonnet-high / Sonnet 5.5 / medium | 1 | none | 3.3 | 85.7k |
| P7d MCP tools | Opus 5.5 / medium | 1 | import cycle fixed in integration | 10.3 | 111.5k |
| P7e storage/perf | Opus 5.5 / medium | 1 | broke scripts/launch/check.ts (fixed in integration) | 4.1 | 87.2k |
| Integration seams | Opus 5.5 / medium | 1 | none | 14.4 | 161.2k |
| P8 wiring | sonnet-high / Sonnet 5.5 / medium | 1 | 3 storefront casts re-fingerprinted → sonnet-mid fixer (1.4 min, 48.7k); a checker test assumed git history → sonnet-mid fixer (4.1 min, 46.8k) | 9.0 | 129.1k |
Reviews: all Codex gpt-6.1-sol xhigh (plan challenge, converge, guard 1, guard 2, VERIFY 1, review 1, review 2, focused review 3). No Claude reviewers.
Lesson for the large-run log: the checker piece consumed most of the rounds. Precise syntactic modelling invites an endless chase after the next bypass shape, and the conservative over-approximation of round 4 produced realistic false positives. A scope stop rule up front, plus a false-positive corpus, would have saved about 3 rounds.

### F99-73-system-map-per-feature-files (2026-10-17, effort medium) [ours]
- Whole change (loader, tools, migration, test, docs): main session, Claude Opus 5.5, default effort. Passed review on attempt 2. Attempt 1 failed because map-features.mjs did not validate the feature files.
- Review: Codex gpt-6.1-sol, medium effort, 2 attempts.

### F99-71-C-required-build-and-demos (2026-10-17, effort medium, risky, delegated builders) [ours]
Token usage per agent: not available. Workflow-level subagent totals were plan 487,939, stage A 464,450, stage B + guard fixes 837,680. Codex token usage: not available. Peak context = max(cache_read_input_tokens + input_tokens) from each subagent transcript; no compaction in any agent. Wall minutes = first to last transcript timestamp.
| ticket | piece | agent type / model / effort | rounds until pass | what failed | escalation | wall min | peak context |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F99-71-C | plan | workflow agent / Opus 5.5 / high | 1 | — | — | 14.8 | 271,373 |
| F99-60 | plan | workflow agent / Opus 5.5 / high | 1 | — | — | 15.0 | 196,569 |
| F99-71-C | P1 builds selector | sonnet-high / Sonnet 5.5 / high | 2 (guard review, then fix) | launcher inputs; imported excluded TS; 5 mutation survivors | none (fix by sonnet-high, 1.7 min, 77,712) | 3.7 | 114,274 |
| F99-71-C | P4+P5 demo runner | opus-medium type / Opus 5.5 / high | 2 (guard review, then fix) | assertion provenance; timeout/signal; untested orchestration guards | none (fix by Opus high, 16.1 min, 178,957) | 9.4 | 159,733 |
| F99-71-C | P6 docs + map | sonnet-mid / Sonnet 5.5 / medium | 1 | — | — | 1.6 | 53,603 |
| F99-71-C | P2 wiring + banner | opus-medium / Opus 5.5 / medium | 1 | — | — | 11.6 | 129,435 |
| F99-71-C | P3 golden cells | sonnet-mid / Sonnet 5.5 / medium | 1 | — | — | 1.0 | 69,610 |
| F99-60 | P1 shards + weights | sonnet-high / Sonnet 5.5 / high | 2 (guard review, then fix) | weak longest-first and weight tests | none (fix by sonnet-high, 1.3 min, 62,686, shared with P3) | 1.0 | 75,940 |
| F99-60 | P3 aggregator | sonnet-high / Sonnet 5.5 / high | 2 (guard review, then fix) | skip/cancel cases untested | none (same fix agent) | 0.8 | 55,913 |
| F99-60 | P2 check:ci lanes | opus-medium / Opus 5.5 / medium | 1 | — | — | 4.3 | 90,026 |
| F99-60 | P4 composite + ci.yml | opus-medium / Opus 5.5 / medium | 1 | — | — | 3.0 | 78,785 |
| F99-60 | P5 pins + manifest | sonnet-high / Sonnet 5.5 / high | 1 (coordinator renamed one manifest case in expected-gates.test.ts) | — | — | 1.8 | 82,357 |
| F99-60 | P6+P7 docs + map | sonnet-mid / Sonnet 5.5 / medium | 1 | — | — | 1.2 | 54,827 |
| both | reviews | Codex Sol 6.1 xhigh (codex-review) | guard ×3 fail → fixed; VERIFY pass; round 1 pass | round-1 attempt 1 exit 75 (/tmp quota) | — | unavailable | unavailable |
Coordinator seams (not builder code): a test-only type annotation in scripts/ci-aggregate.test.ts (TS2345), and the committed-manifest case in scripts/expected-gates.test.ts (check → gates).

### F99-74-checkout-validated-responses (2026-10-18, effort medium, risky) [ours]
Peak context is the largest `cache_read_input_tokens + input_tokens` in each subagent transcript (`~/.claude/projects/<worktree>/f3a6ee63-.../subagents/workflows/*/agent-*.jsonl`). No compaction occurred. Wall-clock comes from the transcript timestamps, or from run-dir file mtimes for Codex pieces.
| piece | ticket | agent type | model | effort | rounds | failed | escalation | wall-clock min | peak context |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| plan verification (attempt 2) | F99-74-checkout-validated-responses, F99-63-layer-port-rules, F99-64-preview-mkdtemp-leak | coordinator (main session) | Opus 5.5 | inherited | 1 | none | none | ~3 | not measured |
| F99-74 core (P1-P6) | F99-74-checkout-validated-responses | workflow subagent | Opus 5.5 | medium | 2 (VERIFY added guard tests) | VERIFY: operationFor and malformed-problem guards unpinned | none | 9.3 | 169,200 |
| F99-74 docs + map (P7-P8) | F99-74-checkout-validated-responses | workflow subagent | Sonnet 5.5 | medium | 1 (wording fixed in VERIFY fix) | coupon step 7 missing (note) | none | 2.4 | 78,031 |
| F99-74 VERIFY fix | F99-74-checkout-validated-responses | workflow subagent | Opus 5.5 | medium | 1 | none | none | 5.1 | 110,607 |
| F99-63 checkers | F99-63-layer-port-rules | workflow subagent | Opus 5.5 | medium | guard review: 9 misses | L1-L4, E1-E5 | none | 18.5 | 160,858 |
| F99-63 guard review | F99-63-layer-port-rules | workflow subagent driving Codex `codex-review` | Opus 5.5 + Codex gpt-6.1-sol | medium / high | 1 | n/a | none | 11.1 (Codex ~6.2) | 58,244 (subagent); Codex tokens unavailable |
| F99-63 guard fixes + docs + map | F99-63-layer-port-rules | workflow subagent | Opus 5.5 | medium | 1 | none | none | 25.6 | 206,459 |
| F99-63 VERIFY fix | F99-63-layer-port-rules | workflow subagent | Opus 5.5 | medium | 1 | none | none | 8.9 | 122,930 |
| F99-63 round-1 fix (B2, B3) | F99-63-layer-port-rules | workflow subagent | Opus 5.5 | medium | B3 failed review 2 | B3 incomplete (shorthand, containers) | to Codex executor (same kind twice) | 5.4 | 95,784 |
| F99-63 B3 class fix | F99-63-layer-port-rules | `codex exec` | Codex gpt-6.1-sol | high | failed focused 1 | container-root exemption | stayed Codex (narrow fix) | ~7.1 | 135,065 tokens used (Codex log) |
| F99-63 B3 narrow fix | F99-63-layer-port-rules | `codex exec` | Codex gpt-6.1-sol | high | passed focused 2 | none | none | ~2.6 | 92,282 tokens used (Codex log) |
| F99-64 fix + test + map | F99-64-preview-mkdtemp-leak | workflow subagent | Sonnet 5.5 | medium | 1 | none | none | 1.7 | 60,441 |
| VERIFY reproduce | all three | workflow subagent | Opus 5.5 | high | 1 | n/a | none | 3.4 | 93,133 |
| VERIFY guards | all three | workflow subagent | Opus 5.5 | high | 1 | n/a | none | 17.5 | 167,212 |
| VERIFY wiring | all three | workflow subagent | Opus 5.5 | high | 1 | n/a | none | 8.2 | 149,234 |
| VERIFY cheating | all three | workflow subagent | Opus 5.5 | high | 1 | n/a | none | 5.0 | 116,825 |
| VERIFY docs | all three | workflow subagent | Opus 5.5 | high | 1 | n/a | none | 4.7 | 139,811 |
| Codex review round 1 | all three | `codex-review --xhigh` | Codex gpt-6.1-sol | xhigh | 1 | n/a | none | ~13.5 | unavailable |
| Codex review round 2 | all three | `codex-review --xhigh` | Codex gpt-6.1-sol | xhigh | 1 | n/a | none | ~5.6 | unavailable |
| Codex focused 1 and 2 | F99-63-layer-port-rules | `codex-review --xhigh` | Codex gpt-6.1-sol | xhigh | 2 | n/a | none | ~6.2 and ~3.7 | unavailable |

### F99-75-type-aware-unsafe-any-lint (2026-10-18, effort medium) [ours]
| Piece | Agent type / model / effort | Rounds to pass | What failed | Escalation | Wall (min) | Peak context |
|---|---|---|---|---|---|---|
| Plan (feasibility, measurements, design) | workflow agent / claude-opus-5-5 / medium | 1 | – | none | 23.1 | 202,820 |
| Build | workflow agent / claude-opus-5-5 / medium | 2 (round 1 Codex fail, round 2 pass) | local rule missed any through type arguments, signatures and spreads; no runner exit-code test | none (different finding kinds, no repeat) | 10.2 | 152,158 |
| Verify panel (reproduce, guards, wiring, cheating, docs) | 5 workflow agents / claude-opus-5-5 / medium | 1 | guards found the missing runner exit-code test | none | 2.3–9.3 each (9.4 for the panel) | 64,276–71,456 |
| Fix round 1 | workflow agent / claude-opus-5-5 / medium | 1 (Codex round 2 pass) | – | none | 16.1 | 179,642 |
| Code review | Codex via codex-review (rounds 1, 2) | – | – | Codex was available both rounds, no fallback | – | – |
No compactions in any subagent transcript.

### F99-76-mvp-merchant-journey (2026-10-19, effort high, delegated builders) [ours]
Source: run dir routing-metrics.md (collected read-only from the subagent transcripts, journals and Codex logs).
Definitions
- wall min: first to last transcript timestamp of the workflow agent (minutes). For Codex pieces the table shows the Opus driver agent's wall and, in brackets, the Codex wall (Codex log file birth time to its mtime; the logs carry no timestamps).
- peak ctx: largest over assistant messages (deduplicated by message id) of input_tokens + cache_read_input_tokens + cache_creation_input_tokens. For Codex pieces this is the Opus DRIVER's context, not Codex's. "Codex tokens used" is the total printed at the end of the Codex log, a cumulative spend, not a context size.
- effort: agent types sonnet-high, sonnet-mid and opus-medium carry the effort in the name. workflow-subagent agents (Opus 5.5 drivers, guards, shots, integration) have no effort field in meta or journal: effort n/a. Codex logs show "reasoning effort: high" for executor runs. Guard reviews ran through the codex-review CLI (the guard transcript mentions xhigh nine times; the exact CLI flag was not verified).
- compaction: none found. No compact_boundary or isCompactSummary marker in any agent transcript, and no real context shrink in any transcript when cache creation is counted.
- [plan X] = label of the piece in plan.md section 2. Plan section 9 re-routed every opus-low/medium/high piece to Codex (Opus only for integration and as fallback); Sonnet pieces stayed Sonnet.
- Commits: git log c41767d4f..HEAD trailers agree: Codex pieces carry Codex GPT-6.1 Sol, Sonnet pieces Claude Sonnet 5.5, Opus fallback/integration Claude Opus 5.5, and W8-P1 pacing fix, W8-P2, W8-P3, W5-P7 call 1, VF1 carry both Codex and Opus.

### F99-77-social-login-linking (2026-10-19, effort high, risky, delegated builders) [ours]
The full per-piece table is in `routing-metrics.md`, collected read-only from the subagent transcripts. It has wall minutes, peak context (input + cache read + cache creation) and Codex tokens; no compaction occurred in any transcript. Summary:
| Piece | Agent / model / effort | Rounds to pass | What failed | Escalation | Wall min | Peak ctx |
|---|---|---|---|---|---|---|
| 5 area planners + synthesizer | workflow-subagent / Opus 5.5 / high | 1 | The synthesizer missed the `sign-up.db.test.ts:318` nullable-hash reader | - | 10.0–15.3 | 196k–300k |
| P1 core | Opus driver high → Codex gpt-6.1-sol high | 1 | - | - | 7.4 (Codex 5.1) | 104k |
| P2 db | Codex high | 1 | Left an unowned seam (fixed in G1) | - | 6.1 (2.8) | 88k |
| P3 contracts | Codex high | 2 calls | r1 stopped: no schema name given in the plan | run-lead decision | 9.2 | 87k |
| P4 merchant service | Codex high | 1 | - | - | 8.1 (5.2) | 98k |
| P5 shopper core | Codex high | 1 | - | - | 3.4 (2.2) | 72k |
| P6 app servers | Codex high | 2 calls | r1 blocked on a pinned test outside ownership | run-lead decision | 13.8 | 90k |
| P7 api | Codex high + Opus driver | 2 calls + driver | `auth.sign_in.failed` undeclared on 2 routes | Opus driver completed it | 21.0 | 134k |
| P8 admin UI | sonnet-high / Sonnet 5.5 | 1 (+ polish r1) | Canvas polish F1–F6 | - | 16.6 | 228k |
| P9 checkout UI | sonnet-high / Sonnet 5.5 | 1 (+ polish r1) | Disconnect button style | - | 12.1 | 179k |
| P10 journey/map/docs | Opus 5.5 high | 1 | 2 in-piece journey attempts (429; draft-store 404) | - | 23.0 | 331k |
| G1-guards | Codex high | 2 calls | r1: wrong run-lead brief (401 vs 404) | - | 20.8 | 118k |
| UI-polish-1 | sonnet-high | 1 | - | - | 7.9 | 160k |
| FX1 merchant | Codex high | 2 calls | One missing audit assertion found by the driver's mutation run | - | 22.5 | 125k |
| FX2 shopper | Codex high | 1 | - | - | 12.4 | 85k |
| FX3 apps | Codex high | 1 | - | - | 9.2 | 82k |
| FX4 → FX5 → FX6 branding | sonnet-high ×3 (research: Opus high) | 3 pieces | FX4 partial (ownership too narrow); FX5 passed its checks but the G was not served (Vite `fs.allow`), caught only by journey shots and critic r3 | stayed on Sonnet; the defined Opus round was not needed | 5.0 / 4.7 / 8.5 | 92k / 119k / 142k |
| Visual critics r1–r4 | opus-medium / Opus 5.5 | FIX, PASS, FAIL, PASS | - | - | 0.9–2.1 | 71k–98k |
| map-repin, map-2 | Opus high | 1 each | - | - | 4.8 / 6.0 | 175k / 151k |
| G2-draft-gate (superseded) | Codex high, run-lead driven | 2 calls | r1 objected to its brief; r2 added an exemption, which coordinator ruling 2 rejected | → G3 | ~1.3 Codex | n/a (main session) |
| G3-draft-gate-fixture | Codex high, run-lead driven | 1 | - | - | ~6 Codex | n/a (main session) |
| Codex reviews | codex-review --xhigh via Opus drivers | guard 2, full 2, VERIFY 1, focused 3 | see Rounds | - | 7–15 each | 45k–74k (driver) |
Routing lessons:
- 5 of 13 Codex pieces stopped on their first call with no files written, all on brief or ownership gaps; each finished on its second call. The Opus fallback was never needed.
- Branding needed three Sonnet pieces because the first piece's file ownership was too narrow, and because no check rendered the real page. Page-level screenshots caught what the unit and package checks missed.
- Run wall-clock: 2026-10-19T19:11:14Z (start) to about 2026-10-20T00:25Z.
