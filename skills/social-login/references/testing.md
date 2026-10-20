# Testing social login

Owner rule from the real build: few and meaningful tests; no long DB suites. These are the ones that earned their
place (each caught a real defect or pins a security property).

## Fake providers
- One loopback-only test server implements both providers by path: Google authorize / token / userinfo, GitHub
  authorize / access_token / `/user` / `/user/emails`. It checks client id + secret, `redirect_uri` equality,
  PKCE (S256), and that each code is used once. Tokens and secrets are synthetic and never look like real ones
  (avoid `gh*_` prefixes and `eyJ` JWT shapes, or secret scanners fire).
- Its consent page has an email field and a "verified" checkbox (checked by default), so the browser journey can
  drive verified and unverified cases. A `deny()` path returns `error=access_denied&state=…`.
- The app picks it up through dev/test-only env overrides (`AUTH_GOOGLE_AUTH_BASE_URL`, `…_API_BASE_URL`, same for
  GitHub). The provider factory refuses those overrides outside dev/test and unless they are an exact origin.
- Give the fake a port that nothing else in the journey uses (the real build's default collided with a sample app
  port that the journey happened not to start).

## Unit
- Linking decision table: known identity; verified email + verified local account; verified email + unverified local
  account (link with reset); unverified email (reject, no lookup); email owner already has this provider; new email
  with sign-up open / closed; connect: not signed in, identity on another account, identity already here, account
  already has the provider, different email OK; 2FA flags; last-method rule.
- State checks: expired, wrong provider, wrong binding, reused (second consume finds nothing), wrong session for
  connect. All return one "invalid" outcome.
- App server: flow cookie set at start with the right attributes; callback deletes it; MFA hand-off sets the
  challenge cookie; sign-up hand-off; terms page posts the displayed version; disconnect sends an idempotency key.

## DB (short, serialized)
- Revocation during provider exchange, during password hashing, and while queued for the user lock → refused, and
  no identity, password or state written.
- Connect after the initiating session signed out (with another session live) → refused; expired and wrong-tenant
  variants too.
- Takeover reset: pre-registered password → invalid credentials; recovery token → invalid; old session revoked;
  distinct audit event.
- MFA social sign-in: no session before the second factor; audit method is the provider for TOTP and recovery code.
- Tenant tables: an explicit tenant predicate on every identity/state/event query (a query-builder plugin that
  asserts it on compiled SQL works well) in addition to row-level security; another tenant sees nothing.
- Per-tenant security events written once per action.
- Use a per-run client IP in request metadata so rate-limit counters are not shared across runs.
- Serialize all DB tests on one database with a file lock, and never run them (or mutation runs) while a gate is using
  the same database.

## Browser journey (one)
- Sign up with fake Google through the terms step; in a fresh context sign in with fake GitHub using the same
  verified email; land in the same account; the settings page lists both as connected and "no password".
- Assert from the DB: one user, identities {github, google}, password null.
- Raise the auth rate limit for the journey backend only if page views spend auth-bucket calls.
- Take desktop and phone screenshots of every provider page here; they caught a missing logo that every unit and
  package check passed.

## Rules
- Write each regression test red before the fix and keep the red output.
- Never weaken, skip or exempt an existing test to make the new routes pass; fix the fixture.
- For each guard, remove it in a scratch copy and name the failing test (mutation check).
