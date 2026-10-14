# Sizing calibration: <project>

Keep this file in the project (e.g. `docs/sizing-calibration.md`) and update it after every sizing pass or build.

## Size rule
- Cap: <pieces> pieces / <files> files per ticket, or split when it holds separately mergeable deliverables.
- Flow rule: <where it lives; what sends a ticket to the heavy process>.

## Measured costs per primitive (files, all-in)
| Primitive | Files | Evidence (ticket, date) |
|---|---|---|
| New API operation (contract + fixtures + generated + policy + test) | | |
| New table with access control (migration + grants + lifecycle + types) | | |
| Privileged cross-tenant read (definer + checker entries) | | |
| New route group / layout | | |
| UI screen with browser and a11y tests | | |
| Event producer | | |

## Estimate vs actual
| Date | Scope | Spec estimate (files) | Counted/built | Ratio |
|---|---|---|---|---|

## Project-specific hidden work
- <files or registries that every change of a kind must touch, with paths>
