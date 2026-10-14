# Hidden work checklist

Spec authors count the feature; builders count everything around it. For each ticket, walk this list and add the
files each item really touches in this codebase. Typical costs are from one TypeScript monorepo (API + admin app +
packages, contract-first, Postgres with row-level security); replace them with your project's calibration.

| Area | Ask | Typical extra files |
|---|---|---|
| **Database migration** | New table, column, index, constraint? Migration + generated DB types + a grants/permissions module + its barrel line. | 4-6 |
| **Row-level access control** | Does the table need tenant isolation policies? Is a cross-tenant read needed (a SECURITY DEFINER or service role)? Does a policy/definer checker or allowlist have to learn about it? | 3-8 (a reviewed definer with checker entries ≈ 18 files all-in) |
| **Retention / lifecycle** | Must the table be classified for export, purge or retention (registry + docs)? | 2-3 |
| **API contract** | Each new operation: spec entry, schemas, **one fixture per operation (often both success and error)**, regenerated client/types, change note. | 5-8 per operation |
| **Route registration and policy** | Route file, plugin/module wiring, route-policy or public-routes entry, auth mode, rate limits. | 2-4 |
| **Audit** | Audit operation names, inventory, pinned tests, exclusions for unauthenticated routes, test-fixture declarations. | 2-5 |
| **Config / env** | New env vars: schema, example file, docs, deployment note. | 2-3 |
| **Docs and maps** | System map / architecture entries, user stories, stale references in other docs, CONTEXT or AGENTS notes. | 2-4 |
| **App routing** | A new route group or layout (focus layout, account scope), guards, redirects, route-id catalogues. | 3-6 |
| **Shared UI** | Is a needed component really generic, or commerce-/domain-specific so you need a local variant? | 1-3 |
| **Tests** | DB tests, API tests, unit tests, browser/a11y specs, motion/reduced-motion guards, fake-API fixtures, seed data for "real data" claims. | 3-8 |
| **Process evidence** | Design references, direction file, critique screenshots (usually run evidence, not repo files; say which). | 0-2 repo files |
| **Events / analytics** | Each event needs a catalogue entry and a server-side producer in the transaction that commits the outcome, plus a dedupe key and a test. | 2-4 per producer site |
| **Generated assets** | Screenshots, images, icons the ticket generates and commits. | count each file |

## Rules of thumb
- One new API operation ≈ 15-20 files once contracts, fixtures, generated output, policy and tests are counted.
  Two operations plus a screen is already near a 40-file cap.
- Server surface (migrations, new ops, privileged SQL, credentials) runs ~2x the naive estimate; UI on existing APIs
  runs 1.0-1.5x.
- "Can merge on its own" is a split trigger even under the caps: an API slice that is safe alone (closed by default,
  no reader yet, verified by DB/API tests) should ship before its UI.
- Check the spec's premises in the code while you count: missing APIs, triggers that already do part of the work,
  upstream packages shipping a different shape, seeds without the data an acceptance line needs.
