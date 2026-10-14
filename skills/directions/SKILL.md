---
name: directions
description: Build N distinct, fully working design directions (landing pages or screens) from references, Mobbin and a Codex design opinion, verified with screenshots and published together as one artifact project. Only when Oscar types /directions.
disable-model-invocation: true
argument-hint: "<count> <what to design> [refs: urls] [keep: what to keep] [avoid: what to avoid] [mix: combinations of earlier directions]"
---

# Directions

Oscar asked for **$ARGUMENTS**. Produce that many distinct directions as **real, working HTML pages**, not canvas mockups. Put them in **one** published artifact project with a front page, and check every page before he sees it.

This process exists because of a failure: the first mockups were generated blind on a canvas, drifted from the reference, used grey placeholder boxes and square buttons, and nobody looked at them before Oscar did. Every rule below prevents a repeat.

## Ground rules

- **Each direction is its own identity.** That means palette, type pairing, and one signature layout or motion device. Never a 1:1 copy of a reference site: take structure and quality, not colours, fonts or section order verbatim.
- **Respect what he already rejected.** Read the project's design history first (for Tendo: `design/landing/BRIEF.md` and `design/landing/v*/`) and avoid rejected looks and palettes.
- **Honesty.** No invented stats, testimonials or real-looking merchant names. Example data is labelled ("Tienda de ejemplo", "Datos de ejemplo"). Unbuilt or undecided features and prices are labelled ("a confirmar"). Check claims against the product, e.g. the ecommerce-builder system map.
- **Real imagery.** Licensed stock only: Unsplash, Mixkit (and Pexels if reachable). Credit every file in `assets/CREDITS.md`. No logos or watermarks, no grey placeholder panels.
- **Language and motion.** Spanish (es-AR voseo) by default with a working ES/EN toggle, unless Oscar says otherwise. No scroll hijacking, no pinned or scrubbed sections, no typed or rotating headlines.
- **Layout.** Height-aware heroes: both CTAs fully visible at 1336×647, 1280×720 and 360×640. No horizontal scroll at 360px.
- **Codex.** Use Codex as the design advisor and critic, through `codex exec` with `-m gpt-6.1-sol`, high effort, `--search` when it needs the web, and screenshots passed with `-i`.
- **No /design canvas.** It can't play video, cuts frames at 8000px and gets no visual check. If Oscar wants a canvas copy afterwards, he runs `/design` himself on a finished direction.

## Steps

Keep the progress dashboard updated as usual if the task is long.

1. **Brief.** Restate in 3 lines: what is being designed, for whom, the count, what to keep, what to avoid. Ask at most 4 questions with AskUserQuestion, only ones that change the design: audience, pricing model, imagery, overall look. Skip any he already answered.
2. **Reference audit**, if reference URLs were given:
   - Run `python3 ~/.claude/skills/directions/scripts/capture.py name=https://url …` from a scratch folder. It writes `refs-out/`: screenshots at 1336×647, 1440×900, 1920×1080 and 390×844, full pages, text, and `report.json` with H1 and CTA positions, fonts and header styles.
   - Slice the full pages with PIL and look at them.
   - Measure exact values (button radius and padding, type scale, container width, section radii) with a small Playwright `evaluate`.
3. **Mobbin.** Run `mcp__mobbin__search_sections` once per section (hero, statement/gallery, features, AI, stories, pricing/fee, integrations, closing/footer, plus any the brief needs), with `limit` 6–8 and `image_format` jpg.
   - Keep 3–4 strong references per section.
   - Download them with `curl -sL <image_url>` to `mobbin/<section>-<name>.jpg`.
   - Record `section, name, short, id, site, note` in `mobbin/refs.tsv`.
4. **Codex directions.** Give Codex the brief, the rejected looks, `refs.tsv`, about 16 key reference images and screenshots of the current version.
   - Ask for N directions, each with:
     - name and one-line idea;
     - 5–6 hex palette tokens with roles and section rhythm;
     - a Google Fonts pairing with a size scale;
     - one signature device;
     - per-section reference filenames and how to adapt them;
     - hero copy in ES and EN.
   - Then ask for a recommendation and what to graft from the others.
   - Read it critically. Fix anything that collides with a competitor or a rejected look, and say so.
   - **For a `mix:` request:** instead of new directions, ask Codex for N combinations of named earlier directions. For each combination: which direction supplies the palette, type, hero and each section, and why the mix holds together.
5. **Build in parallel.** Set up one project folder:
   - shared `assets/`;
   - `mobbin/`;
   - `scripts/shoot.py`, copied from this skill;
   - the previous version as `base.html` if one exists;
   - an `AGENT-BRIEF.md` holding the ground rules above plus the shoot.py hooks: the hero has class `hero`, the CTAs sit inside `.ctas`, the header is `#hdr` and gets class `solid` on scroll.

   Spawn one `general-purpose` agent per direction, all in one message, in the background. Each builds `dir-<x>.html` as a full HTML document and may add prefixed stock assets. Each must run `python3 shoot.py dir-<x>.html shots-<x>`, look at its own screenshots and fix them, at most 3 passes, before reporting.
6. **Review.** Contact-sheet each `1440x900-full.png` with PIL (columns of about 3000px at 0.4 scale) and look at each one. Send a direction back to its agent with specific fixes if it is misaligned, cheap-looking, clipped, or drifts from its spec. Re-run shoot.py yourself to confirm the CTA and overflow numbers.
7. **Front page.** Write `index.html` without doctype/html/head/body tags, following the artifact contract:
   - a title;
   - one card per direction: name, idea, palette swatches, link to `dir-<x>.html`, and a "Codex recommends" badge on the pick;
   - a card for the previous version, for comparison;
   - every Mobbin reference grouped by section, tagged with which direction uses it and linking to its `mobbin_url`;
   - light and dark tokens.
8. **Publish.** Publish one artifact with `index.html` as the page and `files` covering every `dir-*.html`, `base.html`, `assets/*` and `mobbin/*`. Copy the project into the repo's design folder (Tendo: `design/landing/v<next>/`), uncommitted.
9. **Report.** One table: direction, idea, look, signature device. Add any risk you see, the verification numbers, where the files are, and one question: which direction is closest, and what to take from the others.

## Revisions

When Oscar picks or mixes directions, edit the same project files and republish to the same artifact path. Re-run shoot.py on every changed page and look before republishing.
