# Writing instructions that change useful decisions

## Contents

- [Place information by scope](#place-information-by-scope)
- [Make references actionable](#make-references-actionable)
- [Preserve constraints when shortening](#preserve-constraints-when-shortening)
- [Choose a budget](#choose-a-budget)
- [Adapt a minimal template](#adapt-a-minimal-template)
- [Validate the result](#validate-the-result)

## Place information by scope

| Information | Usual home |
| --- | --- |
| Authorization, safety boundaries, unusual check commands | Root instructions |
| Module tenant, transaction, export, state-machine rules | Nested instructions |
| Feature behavior, migrations, source maps | Module references |
| Task intent and acceptance | Task prompt or existing task document |
| Historical workflow | Clearly labeled historical reference |
| Cross-project context-writing method | This personal skill |

Use the project's names and layout. Do not require both instruction filenames, task records, or extra files when the setup already works. Keep established references if callers or anchors depend on them.

## Make references actionable

Weak: `See architecture/security.md.`

Better: `Before changing generated-code execution or publication, read architecture/security.md for capability boundaries and artifact approval requirements.`

Weak: `Run tests.`

Better: `Run the affected package check and one named test file for changed payment state transitions. Report a check that could not start as not run.`

Weak: `Continue until done.`

Better: `Complete the requested change and its relevant checks. Ask only for an unresolved dependency or an action requiring approval. Stop after the requested outcome passes; do not add adjacent features.`

These are patterns, not commands for every project. Preserve different approved test, review, and authorization workflows.

## Preserve constraints when shortening

Read the source completely before summarizing. Keep tenant isolation, identity, money, secrets, provider boundaries, protected resources, and important transitions explicit. Move feature detail with its constraints, directly linked from the relevant instructions. Do not replace an imperative with vague background.

For a large move, retain original rule paragraphs in the reference, add searchable headings and contents, then compare original and destination. Separately inspect short instructions for invariants that must apply before opening the reference. Preserve a rule whose scope is still uncertain.

Replace superseded active policy with the current decision; a banner does not remove competing instructions underneath. Historical material must state that it is not current authority. Keep tuning and volatile status out of universal rules unless needed.

## Choose a budget

Use the repository's budget first. Otherwise start with rules that prevent actual mistakes; measure bytes or available tokens and tune from evidence. A 200-line guideline is not a target to fill. Giant paragraphs evade line checks while retaining tokens.

Do not load every module for one-module work or claim eager imports reduce context. Index long references and put prerequisites before optional explanations. Retain an exception preventing real harm even when it exceeds a cosmetic target.

## Adapt a minimal template

Replace placeholders with verified project facts. Remove sections that add no useful constraint; do not impose this exact structure on an established project.

```markdown
# Working in <project>

- Scope: <current implementation and protected boundaries>.
- Before editing, read <exact applicable nested instruction paths> and
  <the relevant reference, with a concrete trigger for reading it>.
- Preserve <unusual invariants or user changes>.
- Use <verified setup/check commands>; <critical execution caveat>.
- Complete <observable requested behavior and proportionate validation>.
- Stop after the requested result; report blockers and checks not run.
```

An instruction file should correct something the agent would otherwise get wrong. Prefer a precise command, an important exception or an authority boundary over broad slogans such as "write clean code." Link architecture detail directly when a task needs it. Keep transient TODOs, session logs and long feature inventories elsewhere.

## Validate the result

Check commands, links/anchors, preserved rules, changed paths and active chain sizes. Use existing docs checks where practical. Attribute pre-existing failures separately and preserve others' files. Avoid broad app suites for wording changes.

For productivity claims, compare representative tasks at the same snapshot and client/model/version/effort. Measure completion, correctness, checks, unnecessary edits and context use. Do not invent metrics or run costly benchmarks without authorization. Structural cleanup supports size claims, not quality claims.

Primary guidance: [Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
