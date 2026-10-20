# Review checklist (defect classes found in a real build)

Each item is a defect an independent reviewer actually found, with the probe that exposes it. Run the probe; do not
just read the code. Ids in brackets point to `evidence.md`.

## Blocking classes (found as P1/P2 blockers)
1. **Mutation after async work without a live-session recheck** [F6]. Probe: revoke the session while the provider
   exchange or password hash is in flight, and while the request waits for the user lock; the mutation must fail
   and write nothing. Check every credential mutation: connect start, connect completion, disconnect, add password.
   The recent-auth helper must check `revoked_at` and `expires_at` too, not just age.
2. **Connect completion trusts the account id in the state** [F7]. Probe: start connect, sign out (keep another
   session live), complete the callback; it must be refused. Check expiry and tenant/account mismatch as well.
3. **A new caller omits the idempotency key** the API requires [F12]. Probe: the real API (not a mock) with the app
   server's exact request; check every new mutation call site.
4. **Terms version substituted** [F13]. Probe: show v1, change the server to v2, submit; must be refused, not
   silently accepted as v2.
5. **Linking stricter or looser than the agreed policy** [L3]. A verified provider email vs a locally unverified
   account must link-with-reset, not refuse and not plain-link. Compare the decision function with the acceptance
   text line by line.
6. **An audience with no audit trail** [F11]. Probe: grep the new service code for audit/security-event writes per
   action (sign-in, auto-link, connect, disconnect) for every audience, including tenant customers.
7. **MFA completion drops the provider** [L7]. Probe: social sign-in on a 2FA account, complete with TOTP and with a
   recovery code; the audit method must be the provider.
8. **Outdated or unserved brand assets** [G6, G7]. Probe: compare marks and font with the provider's current
   guideline page (dated); screenshot the real pages, not a component harness; check the production build output.
9. **Guards that no test protects** [T7]. Probe: remove recent-auth checks, state expiry, binding checks, each
   explicit tenant predicate, each audit write; at least one test must fail for each.

## Guard and policy classes (found in the guard review)
10. **Audit-layer list branch untested** [W2]: both allowed silent outcomes pass, an unlisted one fails, an
    authenticated success without its event fails.
11. **Allowance declarations unpinned** [W2]: blank entries, an extra status, or the list copied to another route
    must fail a test.
12. **Public-path pattern broadening undetected** [W3]: siblings and typos of the new public paths must be refused.
13. **Session-owned OAuth routes in the wrong rate bucket** [F14]: connect start/callback must hit the auth limit,
    not the generic signed-in limit; probe request N+1.

## Process classes
14. **Test weakened to pass** [T5]: an exemption added to a cross-route test. Fix the fixture instead.
15. **Docs stale after a policy ruling** [L3]: package instructions and smoke steps still describe the old rule.
16. **Contract/fixture examples that contradict behaviour** (e.g. "password: false" after adding a password).
17. **Shared rate counters across test runs** [T6]: repeated runs fail with RATE_LIMITED; isolate per run.
18. **Unbounded prune batch** [F15]: `in (select … limit n for update skip locked)` can delete more than n.

## Non-blocking notes worth a follow-up
- Expired tenant state rows with no sweep; a defensive `session.user_id` binding no test exercises; non-2xx provider
  responses with valid JSON; malformed flow-token shapes; Safari/WebKit rendering of the mark.
