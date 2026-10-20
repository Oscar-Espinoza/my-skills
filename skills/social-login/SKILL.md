---
name: social-login
description: Implement "sign in with Google / GitHub / another OAuth provider" with account linking in any web app, correctly the first time. Covers the owner decisions to settle first, linking rules (verified-email auto-link, pre-account-takeover defense, last-method rule, 2FA), flow security (PKCE, single-use state bound to a cookie, exact redirect URIs, session rechecks, audit), provider and framework gotchas, fake-provider testing, the dev OAuth app setup checklist and a review checklist. Use whenever someone adds social sign-in, "Continue with Google", OAuth login, account linking or a "sign-in methods" settings page, or reviews such a change, even if they only say "add Google login".
---

# Social login with account linking

Every rule here was proved on a real build: merchant Google + GitHub and per-store shopper Google sign-in, linked by
verified email (guard, verify, two full and three focused reviews; every blocking finding fixed). Tags like `[L3]` map each rule
to the finding or commit behind it in `references/evidence.md`. Read `references/review-checklist.md` before you call
the work done, and `references/setup-checklist.md` before anyone creates OAuth apps.

## 1. When to use
- Adding a provider button to sign-in or sign-up, or a settings page that lists, connects and disconnects methods.
- Changing how a provider identity finds or creates a local account.
- Reviewing any of the above. Not for being an OAuth *provider*, or for API-access OAuth (connecting a store
  to a payment provider); those keep provider tokens and have different rules.

## 2. Decide with the owner first
Ask these before planning; each changes the schema or the flow. Write the answers into the ticket.
1. **Linking policy.** Recommended, and what the real build used: one account per verified email. A provider
   identity auto-links to the account with the same email only when the provider says the email is verified;
   otherwise the user signs in the old way and connects from settings. The alternative ("never auto-link") is safer
   but produces the "this email is linked to Google, not GitHub" dead end users hate. [D1]
2. **Which providers for which audience.** Admins/merchants and shoppers rarely need the same set (real build:
   Google + GitHub for merchants, Google only for shoppers). Each provider is a separate OAuth app, callback and
   review. [D2]
3. **Is a password optional?** If provider-created accounts have no password, the password column becomes nullable,
   every reader must handle null, and recovery or settings must be able to add one. [D3]
4. **Per-tenant accounts?** If customers are per store/tenant, identities are unique per (tenant, provider, subject),
   and one fixed callback must route back to the right tenant (see §5). [D4]
5. **Sign-up through a provider:** allowed? Does it still need a terms step? What does closed sign-up answer? [D5]

## 3. Linking rules
Write the decision as **one pure function** (facts in, decision out) and unit-test it exhaustively; keep DB and HTTP
out of it. Facts: intent (sign-in or connect), email verified?, owner of this identity, owner of this email (and
whether they verified it and already have this provider), the signed-in account, sign-up open/closed. [L0]

- **Key identities by (provider, provider subject id)**, never by email. An email change at the provider keeps the
  link. Shopper/tenant tables add the tenant to the unique key. [L1]
- **Known identity → sign in** to its owner, whatever the email says now. [L1]
- **Auto-link only on a provider-verified email.** Google: `email_verified === true` (strictly). GitHub: a verified
  address from `GET /user/emails`, primary first, else the first verified one. Unverified → no auto-link, no lookup
  by email at all. [L2]
- **Pre-account-takeover defense.** Provider-verified email + local account whose email was *never verified*: an
  attacker may have pre-registered that address. Link, mark the email verified, and in the **same transaction**
  revoke all sessions, pending MFA challenges and recovery tokens, clear the password, and audit a distinct event
  (e.g. `identity.linked_reset`). Do not refuse instead (it contradicts the linking policy), and never plain-link.
  Test: the pre-registered password, recovery token and old session all stop working. [L3]
- **Never weaken verification state:** set `email_verified_at` with `coalesce` (keep the earlier timestamp). [L3]
- **The email owner already has this provider** (another subject) → reject generically; do not add a second one. [L4]
- **One identity per provider per account.** Connecting a provider the account already has → "already connected".
  An identity owned by *another* account → generic error; never move it (that is a takeover). [L4]
- **Connect works with a different email**: the identity binds to the signed-in account, not to its email. [L5]
- **Last-method rule.** Never remove the last way in: for admins, password or any provider; disconnect is allowed only
  while another method remains. Accounts with a permanent method (email code) can always disconnect. Enforce it in
  the service under the user row lock, not only in the UI. [L6]
- **2FA still applies.** A social sign-in on an account with 2FA returns "MFA required" and opens the normal challenge;
  it never mints a session directly. Keep the provider on the challenge so the final audit says "google", not just
  "totp". [L7]
- **New verified email, no account:** sign-up only when sign-up is open, through a terms step (short-lived single-use
  sign-up token); closed sign-up answers the same generic error as any other refusal. [L8]
- **Generic errors.** Unverified email, closed sign-up and "identity belongs to someone else" give the *same* message
  and code, so nothing reveals whether an account exists. Specific messages are fine for state expired, cancelled at
  the provider, provider unavailable, rate limited, and (when signed in) already connected / re-auth needed. [L9]

## 4. Flow security
- **Authorization code + PKCE (S256)** for every provider, including confidential server clients. [F1]
- **Single-use state, stored as a digest**, 10-minute TTL, provider and intent recorded with it. Consume it
  atomically first (delete/update ... returning), then validate; every failure returns the same "expired" outcome.
  Compare digests with a constant-time compare. Use purpose-separated digests (`state`, `binding`, `sign-up`). [F2]
- **Bind the state to the browser**: at start, set a random `binding` in a short (10 min) host-only cookie (`__Host-`
  prefix, httpOnly, Secure, **SameSite=Lax**; Strict drops the cross-site return). Store only its digest
  server-side. Deriving the PKCE verifier from the binding means no verifier is stored or round-tripped. [F3]
- **Exact redirect URIs derived from config** (app origin + fixed path), never from the request Host or a query
  parameter. Send the same value at authorize and token exchange. [F4]
- **No open redirect.** Where the user lands after the callback is decided server-side: a stored return path validated
  as same-origin relative, or a fixed page per tenant. Nothing from the callback URL chooses it. Answer callbacks with
  303 + `Cache-Control: no-store` + `Referrer-Policy: no-referrer` (the code is in the URL). [F5]
- **Recheck the live session after any async work, before mutating.** Provider HTTP and password hashing take
  seconds; the session can be revoked or expire meanwhile. Inside the mutation transaction: take the user row lock,
  then re-read the session (not revoked, not expired, belongs to this user, MFA-verified), then write. Applies to
  connect completion, disconnect, add-password and connect start. [F6]
- **Bind connect completion to the initiating session.** A connect state records the session that started it; the
  callback refuses unless that exact session is still live and owns the same account/tenant. A public callback that
  trusts only the account id in the state lets a stolen, then revoked, session attach an attacker's identity. [F7]
- **Recent auth for credential changes**: connecting a provider or adding a password needs a fresh session (≈10 min)
  and verified MFA; disconnect needs verified MFA. [F8]
- **No provider tokens kept.** Exchange code → access token → read profile → drop the token. Store only provider,
  subject, timestamps. Provider HTTP: timeout, `redirect: 'error'`, and never put response bodies in errors or logs. [F9]
- **Secrets env-only, backend-only.** Client id/secret in env vars, set as a pair or not at all; the frontend
  processes never receive them; never logged, printed or committed. Test base-URL overrides are accepted only in
  dev/test and only as an exact origin. [F10]
- **Audit**: provider sign-in (method = provider), link, unlink, linked-with-reset, password added. Ids and enums
  only, never the email. The provider survives the MFA step (see L7). Tenant accounts with no audit actor need their
  own append-only per-tenant security-event table; "the identity rows are the record" is not an audit. [F11]
- **Idempotency keys on mutations** (disconnect, add password) if the API requires them; check every new caller
  actually sends one. [F12]
- **Record the terms version the user saw**: the terms page posts the version it displayed; the server rejects a
  stale one. Never re-fetch "current terms" at submit and accept that. [F13]
- **Rate limits**: per-IP limits on start and callback plus the auth bucket. Session-owned connect routes belong in
  the auth bucket too, not the general signed-in bucket. [F14]
- **Prune expired state rows** in maintenance, with a truly bounded batch delete (`with v as (select … limit n for
  update skip locked) delete … using v`); `delete … where id in (select … limit n)` can overshoot under a rescan
  plan. [F15]

## 5. Provider gotchas
- **Google redirect URIs are fixed and exact**: no wildcards, no per-tenant hosts. A multi-domain or multi-tenant app
  uses **one central callback** on one host; the state names the tenant (a signed or stored selector), and the
  return target is fixed per tenant. [G1]
- **Google Testing mode**: only listed test users can sign in; everyone else gets an error page from Google. Real
  users need the app published (and possibly verified) before launch. [G2]
- **Google profile**: after a server-side code exchange, read `sub`, `email`, `email_verified` from the OpenID
  userinfo endpoint with the access token; no JWKS needed. If you read the `id_token` instead, you must verify its
  signature (JWKS), `aud`, `iss` and `exp`. Scope `openid email`; `prompt=select_account` helps multi-account users. [G3]
- **GitHub**: register every callback URL exactly (the OAuth app form observed 2026-10-19 allowed up to 10 redirect
  URIs, plus an opt-in wildcard you should leave off); the `redirect_uri` you send must match one. Still keep a
  separate app per environment (dev vs production). Scope `user:email`; the `/user` email may be null or unverified, so verified
  addresses come only from `GET /user/emails`. Subject = numeric `id` as a string, never the login (renamable). [G4]
- **Use `localhost`, not `127.0.0.1`,** if that is what was registered: the redirect URI must match byte for byte. [G5]
- **Official button branding** (Google's guidelines are a verification requirement): current gradient "G" (the
  flat four-colour G is outdated), Google Sans Medium 14/20 self-hosted under its OFL licence, 40 px height, 12/10/12
  spacing, Google's light/dark fill and stroke colours; GitHub's current Invertocat in black or white. Wording
  "Continue with Google" (localised is fine), never "Google" alone. Read the provider's current page and asset
  bundle, not its sample HTML (Google's configurator still emitted the old G). [G6]
- **Check the asset is actually served.** One real build passed every unit and package check and still shipped an
  empty slot where the G belonged: the dev server refused to serve the SVG from a package folder (Vite
  `server.fs.allow`), and another app never loaded the font. Screenshot the real pages, and check the production
  build emits the SVG and font. [G7]
- **Unconfigured provider**: hide its button (a "providers available" call), and keep the route answering a clear
  "not available". Buttons show progress immediately on click. [G8]

## 6. Web-framework gotchas
- **CSP `form-action 'self'` blocks a form POST whose response redirects to the provider.** Make provider buttons
  plain GET links to your own `/oauth/<provider>/start`, which sets the cookie and 303s to the provider. [W1]
- If your audit layer fails a 2xx that recorded no event, declare the non-session outcomes (`mfa_required`,
  `sign_up_required`) explicitly and test both, plus an unlisted outcome failing. [W2]
- Route-policy patterns for the new public paths must be exact; widening `google/start` to `google/[a-z]+` silently
  makes siblings public. Pin them with negative tests (typos, siblings, other providers). [W3]
- Broad "every route" tests (e.g. a walk that expects 404 on an unpublished tenant) will hit the new routes; that is
  the test working. [W4]

## 7. Testing
Few, meaningful tests (details and the exact cases in `references/testing.md`):
- **Fake providers via base-URL env vars** (dev/test only): a loopback server that implements authorize, token,
  userinfo, `/user`, `/user/emails`, checks the client secret, `redirect_uri`, PKCE and single-use code, and shows a
  consent page with an email field and a "verified" checkbox. No live provider calls in any automated test. [T1]
- **Unit**: the linking decision (verified / unverified / new / existing / unverified-local / 2FA / last method /
  connect cases) and state validation (expired, wrong provider, wrong binding, reused). [T2]
- **The DB tests that caught real bugs**: session revoked during provider exchange; revoked during hashing; revoked
  while queued for the user lock; connect completed after the initiating session signed out; MFA keeps provider
  attribution; takeover reset (old password, recovery token, session all dead); terms version mismatch; disconnect
  sends an idempotency key; an explicit tenant predicate on every query. Write each red before the fix. [T3]
- **One browser journey**: sign up with fake Google, then sign in with fake GitHub (same verified email) in a fresh
  context; assert one account with two identities. Take page screenshots there. [T4]
- **Never weaken an existing test** with an exemption to make a new route pass; fix the fixture (e.g. give the
  control user a linked identity). [T5]
- **DB tests never run concurrently with a gate** or with each other on one database: serialize them with a lock,
  and give rate-limited tests a per-run IP so repeated runs do not share counters. [T6]
- **Mutation-check guards**: remove each guard in a scratch copy and name the test that fails. [T7]

## 8. Setup (humans create the apps)
The human creates the dev OAuth apps, accepts the providers' terms, copies the secrets into an env file outside the
repo and tells the agent the file path and the exact registered redirect URIs. The agent never reads, prints or
commits the secrets, and never accepts terms or creates apps for the human. Full steps:
`references/setup-checklist.md`. [S1]

## 9. Review
Before calling it done, run every item in `references/review-checklist.md`: these are the defect classes reviewers
actually found, in the order they cost the most.
