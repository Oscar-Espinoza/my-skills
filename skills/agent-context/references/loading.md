# Loading and context delivery

Research checked 2026-10-02. Recheck primary documentation before relying on a version-specific setting. These notes describe local coding clients, not Claude web chat or a custom API harness.

## Contents

- [Separate failure stages](#separate-failure-stages)
- [Claude Code](#claude-code)
- [Codex](#codex)
- [Portable skill installation](#portable-skill-installation)
- [Limits and recommendations](#limits-and-recommendations)

## Separate failure stages

Check discovery, delivery, application, and later retention separately. A file may never load; a preview may omit the rule; a supplied rule may conflict with another; a delegated agent or compacted conversation may lack earlier context. Inspect tool reads and client context reporting instead of calling every failure forgetting.

## Claude Code

AGENTS.md support was added in 2.1.277. Default `claude-md-or-agents-md` falls back to AGENTS.md only when no project/ancestor CLAUDE.md or CLAUDE.local.md claims the instruction tree. The special user file `~/.claude/CLAUDE.md` does not suppress fallback. A home-directory `~/CLAUDE.md` can.

For an AGENTS-only project with ancestor Claude instructions, the user-wide built-in setting can load both without adding a project shim:

```json
{
  "pluginConfigs": {
    "agents-md@builtin": {
      "options": { "instructionFiles": "claude-md-and-agents-md" }
    }
  }
}
```

Set this only when authorized; merge with existing keys. Project-local settings do not control this option. Check `/config` and `/context` in the actual session. Nested AGENTS.md attachments use text Read calls; Bash reads do not provide the same trigger. After compaction, repeat relevant scoped reads before relying on nested context. Some subagents omit project instructions; supply required scope explicitly.

Sources: [memory documentation](https://code.claude.com/docs/en/memory), [built-in loader notes](https://github.com/anthropics/claude-code/blob/main/mods/agents-md/README.md), [subagent context](https://code.claude.com/docs/en/sub-agents), [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md).

## Codex

Inspect installed discovery behavior and configuration. Codex has a global-to-project instruction chain, AGENTS.override.md behavior, and a configurable project-document byte budget (documented default 32 KiB). Instructions below the startup working directory may need explicit reading. These are not universal Claude rules.

Source: [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Portable skill installation

Use one real directory with SKILL.md and relative links. Here `~/.codex/skills/agent-context` is canonical and `~/.claude/skills/agent-context` points to that directory. Claude supports symlinked personal skill folders. Verify Codex's actual skill list when available; discovery locations can change. Do not symlink only SKILL.md or replace an entire discovery directory. Never import unrelated skills automatically.

Invoke `$agent-context` in Codex and `/agent-context` in Claude Code. A new session may refresh discovery. This is local availability, not publication or account synchronization.

Sources: [Claude skills](https://code.claude.com/docs/en/skills), [OpenAI skill authoring](https://learn.chatgpt.com/docs/build-skills).

## Limits and recommendations

Current Claude documentation separates these limits: MEMORY.md startup content is 200 lines or 25 KB; CLAUDE.md loads up to 4 MiB and larger files are skipped; recursive imports have four hops. None means every Markdown file stops at line 100. Anthropic's skill guide warns that nested references can prompt a `head -100` preview and recommends direct references and contents lists above 100 lines. This is a behavioral warning.

Directory nesting, import recursion, reference navigation, and subagent depth are separate mechanisms. Automatic imports split organization but still load eagerly. Keep critical paths shallow without inventing a fixed model failure depth.

Sources: [memory limits and imports](https://code.claude.com/docs/en/memory), [skill reference guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#avoid-deeply-nested-references).
