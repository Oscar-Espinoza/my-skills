# Evidence map

Every rule tag in `SKILL.md` and the checklists, mapped to what motivated it. Source: one real build, ticket
`F99-77-social-login-linking` in Oscar's ecommerce-builder repo (merged at `4d401f42a`, commits
`b8acc2420..4d401f42a`). Run-dir files are from `~/.local/state/herd/ultracode/runs/F99-77-social-login-linking/`.
"Ticket" = the feature text in `.shipyard/features.json` (identical to `task.md`), "PDF" = its PRE-DISPATCH FACTS.
Plan defaults `D1`–`D13` are in `plan.md` §4; review findings are numbered in the order they appear in the JSON
`blocking` array.

| Tag | Rule (short) | Motivated by |
|---|---|---|
| D1 | Linking policy: one account per verified email | Ticket "LINKING RULE (owner decision)"; owner's "never says linked to Google, not GitHub" |
| D2 | Providers per audience | Ticket (merchants Google+GitHub, shoppers Google only; out of scope list) |
| D3 | Password optional → nullable column, readers handle null | PDF (password_hash NOT NULL, owner decision); the plan synthesizer missed the `sign-up.db.test.ts:318` reader (`result.md` routing table); commit `26e2b2227` (P2) |
| D4 | Per-tenant identities, central callback | Ticket (shopper accounts per store; ONE callback); PDF (unique (store_id, provider, subject), explicit predicate on RLS) |
| D5 | Sign-up via provider: terms step, closed = generic | Acceptance 2; plan D5; commit `251c4af26` (P4) |
| L0 | Pure decision function, unit-tested | Plan D2; `packages/platform/src/social-oauth/linking.ts` (`decideProviderLink`), commit `26b74d798` (P1) |
| L1 | Key by (provider, subject); known identity signs in | Ticket ("keyed by provider subject id"); acceptance 2 |
| L2 | Auto-link only on provider-verified email; GitHub /user/emails, primary first | Ticket; plan D7; `github.ts`, `google.ts` in commit `26b74d798` |
| L3 | Pre-account-takeover: link, verify, revoke sessions/challenges/recovery, clear password, distinct audit; coalesce verified-at | `review-verify-1.json` #3 and `review-1.json` #5 (refusal contradicted acceptance); `coordinator-ruling-1.md`; fix commit `4386cc61a` (FX1); `responses-1.md` #5; docs commit `f895b94f2` after `review-2.json` note (stale AGENTS.md); PDF (`users_email_verified_guard`, coalesce) |
| L4 | Email owner already has provider → reject; one identity per provider per account; foreign identity → generic | Acceptance 2 ("cannot be connected … no takeover"); plan D6; `linking.ts` connect branch |
| L5 | Connect works with a different email | Ticket; acceptance 3; journey in commit `c1cc8d6f9` (P10) |
| L6 | Last-method rule, enforced in service | Ticket; acceptance 3; `mayRemoveMethod` in `linking.ts`; commit `251c4af26` |
| L7 | 2FA enforced; provider kept through MFA | Ticket; PDF (`#createChallenge`, `/mfa`); `review-verify-1.json` #5, `review-1.json` #7; fix `4386cc61a` (migration 0156 `mfa_challenges.provider`) |
| L8 | New verified email → terms step if open | Acceptance 2; plan D5 |
| L9 | Generic errors, no account enumeration | Ticket ("never reveal whether an email has an account"); acceptance 2; admin `noticeFor` in commit `f7e741302` (P6) |
| F1 | Code + PKCE S256 | Ticket SECURITY; acceptance 4; commit `26b74d798` |
| F2 | Single-use digest state, 10 min, consume then validate, constant-time | Acceptance 4; `flow.ts` (`flowDigest`, `checkConsumedFlow`) in `26b74d798` |
| F3 | `__Host-` httpOnly Lax binding cookie; verifier derived from binding | Acceptance 4; plan D4 (Strict drops the return); admin `lib/server/oauth.ts` in `f7e741302` |
| F4 | Exact redirect URIs from config | Acceptance 4; `apps/api/src/modules/auth/social-redirects.ts` in `334ef37fd` (P7) |
| F5 | No open redirect; 303 no-store no-referrer | Ticket; plan D8; admin `oauthRedirect` in `f7e741302` |
| F6 | Recheck live session after async work, under the user lock | `review-verify-1.json` #1, `review-1.json` #1; fix `4386cc61a`; `responses-1.md` #1 (red tests at social.db.test.ts :370/:396/:417); PDF (`#lockUser` first) |
| F7 | Bind connect completion to initiating session | `review-verify-1.json` #2, `review-1.json` #2; fix `dc3e1f166` (FX2, migration 0157 `initiating_session_id`) |
| F8 | Recent auth for credential changes | Plan D6 |
| F9 | Keep no provider tokens; safe provider HTTP | Ticket ("do not keep provider access tokens"); `providers.ts` `providerJson` in `26b74d798` |
| F10 | Secrets env-only, backend-only; overrides dev/test exact origin | Ticket; `scripts/launch.ts` backend-only in `26b74d798`; `providers.ts` `baseUrl`; `result.md` owner smoke step 3 |
| F11 | Audit provider sign-in/link/unlink/reset, ids only; per-tenant event table | Ticket; PDF (ids/enums only); `review-verify-1.json` #6, `review-1.json` #6 (plan D1 had excluded shoppers); fix `dc3e1f166` (`customer_security_events`) |
| F12 | Idempotency keys on mutations | `review-1.json` #3; fix `d1d1a41b4` (FX3) |
| F13 | Record the terms version shown | `review-verify-1.json` #4, `review-1.json` #4; fix `d1d1a41b4`; PDF (`acceptedTermsVersion`) |
| F14 | Rate limits; connect routes in auth bucket | Ticket; plan D11; `review-guard-1.json` #4; fix `af6bc19dd` (G1-guards) |
| F15 | Prune states; bounded CTE delete | Plan D12; `housekeeping-flake-repro.md`; `result.md` gate receipt 2 and Follow-ups |
| G1 | Google fixed URIs → central callback for multi-tenant | Ticket ("Google needs fixed redirect URIs, so … ONE callback"); plan D8 |
| G2 | Google Testing mode needs test users | Ticket (project in Testing mode, owner as test user); `plan.md` §5 smoke |
| G3 | Google userinfo, no JWKS (else verify id_token) | PDF ("Read Google profile from userinfo (no JWKS)"); `google.ts` |
| G4 | GitHub exact callbacks (form: up to 10 redirect URIs, wildcard opt-in; observed while registering 'Tendo (dev)' 2026-10-19), `user:email`, emails from /user/emails, subject = id | Ticket (registered URIs; GitHub verified address from GET /user/emails); PDF (scope `user:email`); `github.ts` |
| G5 | localhost vs 127.0.0.1 | `plan.md` §5 / `result.md` owner smoke step 4 ("localhost, not 127.0.0.1") |
| G6 | Official branding: gradient G, Google Sans Medium, sizes, Invertocat, wording | Ticket ("official mark and wording rules"); `review-verify-1.json` #8, `review-1.json` #8; `branding/branding-research.md` §1.2–1.7; commits `e0c2b68c7` (FX4), `1bde0f14d` (FX5) |
| G7 | Check assets are actually served | `visual-critique-3.md` R1/R2 (Vite `fs.allow`, checkout never loaded the font); fix `2ac40443d` (FX6); `visual-critique-4.md`; `result.md` routing lessons |
| G8 | Hide unconfigured provider; immediate progress | Plan D9; ticket ("buttons show progress immediately"); `result.md` follow-up (shopper page shows the button and answers 503) |
| W1 | CSP form-action → GET links to /start | PDF ("Admin CSP form-action 'self': … GET links"); `result.md` "What was built" |
| W2 | Declare and test silent audit outcomes | Plan feasibility row 4; `review-guard-1.json` #1, #2; fix `af6bc19dd`; `responses-guard-1.md` |
| W3 | Exact public-path patterns with negative tests | `review-guard-1.json` #3; fix `af6bc19dd` |
| W4 | Cross-route tests hit new routes | `result.md` gate receipt 1 (`draft-gate.db.test.ts`) |
| T1 | Fake providers via base-URL env | Ticket DEV/TEST; PDF (`AUTH_*_BASE_URL`); `fake-server.ts` in `26b74d798`; `result.md` follow-up (port collision) |
| T2 | Unit tests: linking decision, state | Ticket TESTS; acceptance 5; plan D13 |
| T3 | The DB tests that caught bugs | `responses-1.md` #1–#7 and `responses-verify-1.md` #7 (red/green, mutation kill counts) |
| T4 | One journey: fake Google then fake GitHub → same account | Acceptance 5; commit `c1cc8d6f9`; `journey-final.txt` |
| T5 | Never weaken a test; fix the fixture | `coordinator-ruling-2.md`; superseded `4970efe08`; fix `4d401f42a` (G3); `responses-gate-1.md`; `review-focused-3.json` |
| T6 | Serialize DB tests; not during gates; per-run IP | `task.md` "How to work" step 6 (no DB access during the gate); `plan.md` §1 DB lane (`db.lock`); `review-guard-1.json` note (shared rate counters) |
| T7 | Mutation-check every guard | `review-verify-1.json` #7; `review-1.json` and `review-2.json` notes; `responses-verify-1.md` #7 (27/28, 15/15 killed) |
| S1 | Human creates apps and secrets, accepts terms; agent never reads secrets | Ticket (owner-created credentials; live smoke is an owner action); `plan.md` §1 Secrets ("never source" the env file); `result.md` owner smoke |

Defect classes 16–17 in `review-checklist.md`: `review-1.json` note (misleading setPassword / disconnect fixtures,
fixed in `4386cc61a` / `dc3e1f166`) and `review-guard-1.json` note (rate counters). Branding/visual rounds:
`visual-critique-1.md`–`-4.md`.
