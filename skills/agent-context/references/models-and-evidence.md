# Model guidance and evidence

Checked 2026-10-02. Recheck sources before changing settings. These are conditional notes, not universal project policy.

## Contents

- [Opus 5.5](#opus-55)
- [Sonnet 5.5](#sonnet-55)
- [Evidence limitations](#evidence-limitations)
- [Optional authoring tools](#optional-authoring-tools)

## Opus 5.5

The model overview lists a 1M-token API context window for Opus 5.5 and Sonnet 5.5. A maximum window describes input capacity, not guaranteed use of every rule. Client overhead, tool output, conversation, memory and compacted state compete for that input; verify what the actual session supplies.

Anthropic documents adaptive thinking always on and medium as default effort. Effort labels are not equal reasoning amounts across models. In unattended runs, a progress report can end a turn before the task ends. Define completion and have the runner evaluate it; text alone does not prove success. Preserve current effort caps. A larger window cannot fix missing input.

Sources: [Opus prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5), [model overview](https://platform.claude.com/docs/en/models/overview).

## Sonnet 5.5

Anthropic recommends medium for well-specified agentic work and high for harder or longer work. Lower effort can cause early check-ins; low can skip meaningful checks. Higher effort can expand scope with supporting files or review rounds. Give bounded scope, a real relevant check, and a stopping condition; do not add universal test rituals or review teams. API and Claude Code defaults can differ. Use the actual client's settings.

Source: [Sonnet prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5).

## Evidence limitations

No controlled study found here establishes a 100-line or three-document reliability cliff for either 5.5 model. Separate loader documentation, vendor findings, older model studies, and local measurements.

[Evaluating AGENTS.md](https://arxiv.org/html/2602.11988v3) evaluated Sonnet 4.5 and other models; generated files increased cost without significant overall success gains. [Two-agent ablation](https://arxiv.org/html/2607.27250v1) evaluated Sonnet 4.6 with few tasks and delivery/content confounds. Neither proves current models ignore useful safety rules. [Configuration smells](https://arxiv.org/html/2606.15828v5) supplies maintenance vocabulary, not optimal budgets.

[Lost in the Middle](https://arxiv.org/abs/2307.03172) and [Chroma context rot](https://www.trychroma.com/research/context-rot) studied position and length effects on older models. Use them as motivation to evaluate relevance, not measurements of Opus/Sonnet 5.5.

## Optional authoring tools

[claude-md-management](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-md-management) contains a CLAUDE.md improver and session-learning command. It is optional and targets Claude filenames; do not install it automatically. The [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) adds built-in `/doctor prompt-audit` in 2.1.283. Treat findings as suggestions and explicitly name AGENTS.md scope. No audit score proves adherence.
