# Calibration example: ecommerce-builder, F23 onboarding epic (2026-10-14)

TypeScript monorepo: Fastify API, SvelteKit admin and storefront, ~25 packages, contract-first OpenAPI with
per-operation fixtures, Postgres with RLS and a policy checker. Size rule: ≈8 pieces / ≈40 files, or separately
mergeable deliverables. Two tickets had already stopped mid-run (planned 49 and 74 files against spec estimates of
~30 and ~38).

## Estimate vs counted (24 tickets, counted from code, nothing built)
- Files: spec 650 → counted ~1125 (**1.73x**). Pieces: roughly as estimated.
- Server-heavy tickets ~2.0-2.6x (template registry 32 → 83 with 36 generated screenshots; activation events 38 → ~80;
  private preview 38 → 78; companion tickets 30-34 → 62-69).
- UI on existing APIs 1.0-1.5x (metrics modules 26-28 → 27-35; journey evidence 12 → 12). One overestimate
  (section editor 26 → 17: the server types already existed).
- Outcome: 18 of 24 split into 46 slices; 6 kept. Open tickets 29 → 57.

## Measured costs
| Primitive | Files |
|---|---|
| One session-owned GET operation (contract, fixtures, regen, policy, two-user DB test) | ~17 |
| One member-readable store read (contract, fixtures, regen, policy, notes, map) | ~20 |
| One POST endpoint with dedupe (contract, fixtures, policy, audit exclusion, layout calls) | ~22 |
| Reviewed SECURITY DEFINER with marker policies and checker allowlist entries | ~18 |
| Dedicated NOLOGIN aggregator role (provisioning/setup/reset, checker identities, negative tests) | +7 on top |
| Label sweep: one h1 + title rename per page | 1 per page, plus pinned tests |

## What the review caught (round 1, 16 findings)
- A sizing default replaced the spec's explicit security design (dedicated role) with a smaller pattern.
- Defaults contradicted unchanged acceptance lines (navigation not set; a changed document left off a list;
  "real seeded data" proven with fakes only; label = h1 with four exemptions).
- Events placed in UI files with no server producer.
- Two slices creating the same preferences migration; a control edited by two tickets with different targets.
- A cross-cutting panel slice scheduled before the screens it must cover.
- Inherited whole-ticket deps that serialized server slices (critical chain 20 → 14 after fixing).
