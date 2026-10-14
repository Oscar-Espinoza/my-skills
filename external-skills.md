# External skills (not vendored)

Installed on Oscar's machine from their own sources. Install them from upstream so they stay current and keep their
licences. Sources are from `~/.agents/.skill-lock.json` (installed with the `skills` CLI, `npx skills`).

| Skill | Source | Install |
|---|---|---|
| `find-skills` | github.com/vercel-labs/skills (`skills/find-skills`) | `npx skills add vercel-labs/skills --skill find-skills` |
| `anatomy` | github.com/wheresryan22/anatomy (MIT) | `npx skills add wheresryan22/anatomy` |
| `fframes-video` | fframes.studio well-known skill | `npx skills add https://fframes.studio` |
| `playwright` (Codex) | OpenAI-curated Codex skill (`~/.codex/skills/playwright`, Apache-2.0 NOTICE) | install from Codex's skill catalogue |

Plugin skills (Impeccable, anthropic-skills, claude.ai synced skills) come with their plugins or accounts and are
not listed here.
