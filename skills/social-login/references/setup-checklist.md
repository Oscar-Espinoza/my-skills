# Dev OAuth app setup checklist

Who does what: **the human** creates the apps, accepts each provider's terms, and pastes the secrets into an env
file. **The agent** writes the redirect URIs to register, the env var names and the smoke steps, and loads the env
file only inside the process that needs it. The agent never opens, `cat`s, greps or prints the file, never puts a
secret in a command line, log, test or commit, and never clicks "accept" on a provider's terms.

## Before the human starts (agent prepares)
- [ ] Fix the callback paths in code first, e.g. `/oauth/google/callback` and `/oauth/github/callback`, derived from
      the app origin config (`ADMIN_ORIGIN` / port). One central callback host per provider for multi-tenant apps.
- [ ] List the exact dev redirect URIs from that config, scheme, host, port and path, byte for byte
      (`http://localhost:<port>/oauth/<provider>/callback`). Decide `localhost` vs `127.0.0.1` once and use it
      everywhere; the browser must open the app on the same host.
- [ ] Name the env vars: `AUTH_<PROVIDER>_CLIENT_ID`, `AUTH_<PROVIDER>_CLIENT_SECRET` (set both or neither), plus
      dev/test-only base-URL overrides for fakes. Register them in the project's env example/schema with the secret
      flag, and make sure only the backend process receives them.
- [ ] Hand the human this list and the target env file path (outside the repo).

## Google (human)
- [ ] Create a Google Cloud project for dev (separate from production).
- [ ] Configure the OAuth consent screen: app name, support email, scopes `openid` and `email` only.
- [ ] Leave it in **Testing** mode and add every person who will try it as a **test user** (others are refused).
- [ ] Create an OAuth client of type **Web application**; add each exact redirect URI from the list.
- [ ] Copy client id and secret into the env file.
- [ ] Before launch (human, at deploy): a production client with production URIs and the app out of Testing
      mode; Google's branding guidelines are part of its app verification.

## GitHub (human)
- [ ] Create an **OAuth App** (not a GitHub App) per environment, e.g. "MyApp (dev)".
- [ ] Homepage URL = the app origin; **Authorization callback URL** = the exact GitHub callback; add more redirect URIs only if needed (form allowed up to 10 on 2026-10-19); leave wildcard matching off.
- [ ] Generate a client secret; copy id and secret into the env file.
- [ ] No extra scopes are configured on the app; the code asks for `user:email` at authorize time.

## After (agent)
- [ ] Confirm the variables are present without printing values, e.g. a script that prints only
      `AUTH_GOOGLE_CLIENT_ID: set`.
- [ ] Start only the API with the file loaded in a subshell (`( set -a; . <file>; set +a; <start api> )`), unsetting
      unrelated secrets that share the file. Remove any fake base-URL overrides from the env first.
- [ ] Write the owner smoke steps (do not run live sign-ins yourself unless asked):
  1. Open the sign-in page on the registered host; Continue with Google; pick a test user; expect the callback and
     a session. A new email shows the terms step; a 2FA account shows the MFA page.
  2. Sign out; Continue with GitHub with the same verified primary email; expect the **same** account.
  3. Settings lists both; disconnecting the last remaining method is refused.
  4. Per-tenant flow: start from one tenant, return to that tenant's page.
  5. Warn: a seeded account whose email was never verified gets linked **and reset** (password cleared, sessions
     revoked) by the takeover defense. Use a verified account or expect to set a password again.
  6. Check the server log has no `code=`, access token, binding, state or client secret.
  7. Check the Google button renders in Safari too if no WebKit check ran.
- [ ] Production OAuth apps are registered at deploy time, by the human, with production URIs.
