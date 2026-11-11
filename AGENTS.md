# AGENTS.md

Guidance for an AI assistant (Claude Code, Codex, etc.) working in this repo. The most common job here is **pulling the latest upstream `humanizer` and re-applying the UK conversion** — this file is the recipe for that.

## What this repo is

A UK-English fork of [`blader/humanizer`](https://github.com/blader/humanizer), a Claude Code / OpenCode skill implemented entirely as Markdown. The runtime artifact is `SKILL.md` (YAML frontmatter + the editor prompt). There is no build step and no code to run. **`SKILL.md` is the source of truth.**

This fork is intended to be a *minimal, well-documented delta* over upstream: the same skill, with British spellings and one example outlet swapped. Every intended difference is listed inside `SKILL.md` under **"UK Customisation Manifest" (sections A–H)**. Do not introduce UK-specific changes that aren't captured there — add them to the manifest first.

## Key files

- `SKILL.md` — the skill, plus two fork-only sections near the top: **"Step 0: Update Check"** and the **"UK Customisation Manifest."** Source of truth.
- `README.md` — for humans: what it does, install, usage, how to update.
- `AGENTS.md` — this file.
- `LICENSE` — MIT.

## Versioning

`X.Y.Z-uk.N`:
- `X.Y.Z` mirrors the upstream `humanizer` version this fork is synced against (stored in `SKILL.md` frontmatter as `upstream-version`).
- `-uk.N` increments when fork content/manifest changes without an upstream bump.

The frontmatter `version:` is `X.Y.Z-uk.N`; `upstream-version:` is the plain `X.Y.Z`.

## How to update from upstream (the main task)

1. **Fetch upstream `SKILL.md`.** This repo already has a pull-only `upstream` remote configured (`https://github.com/blader/humanizer.git`, tracking `main`, push URL disabled), so:
   ```
   git fetch upstream && git show upstream/main:SKILL.md
   ```
   (or read the raw file directly: `https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md`).

2. **Compare versions.** Read upstream's frontmatter `version:` and this fork's `upstream-version:`. Equal → nothing to do. Different → continue.

3. **Re-apply the UK Customisation Manifest.** Start from the *fresh upstream content* and work through manifest sections A–H in order. The manifest names patterns by title because upstream renumbers them; where this summary and the manifest differ, the manifest wins:
   - **A. Frontmatter** — `name: humaniser`; keep `upstream-source` / `upstream-repo` / `upstream-version` under `metadata:`; add the "UK English variant" line to `description`. Do **not** re-add `allowed-tools` or `compatibility` (upstream dropped them for cross-agent portability).
   - **B. Spelling table** — apply the US→UK whole-word, case-preserving substitutions (colour, analyse, organisation, judgement, colonisation, memoisation, etc.). Do **not** touch the exclusions (`license: MIT`, code identifiers, URLs, the curly-quote typography example).
   - **C. Targeted phrase swaps** — in the dashes pattern, "Replace each dash with a period, ..." → "... a full stop, ..."; treat any other punctuation-sense "period(s)" the same way.
   - **D. Example outlet swaps** — the prestige-list example in the "Borrowed authority" pattern (Before and After): US/Indian papers → *The Times* / *The Guardian*.
   - **E. Title** — `# Humaniser: ...`.
   - **F. Preserve** the Step 0 section and the manifest itself.
   - **G.** Leave upstream's *own* prose em dashes alone (the no-em-dash rule is for humanised output, not this file).
   - **H. Fork addition** — after upstream's overused-AI-words list, re-append the labelled "Also (UK fork additions):" line; drop any word upstream has since adopted.

4. **Bump the version.** Set `upstream-version:` to the new upstream `X.Y.Z` and `version:` to `X.Y.Z-uk.1` (use `-uk.N+1` if only the manifest changed without an upstream bump).

   **Also bump `.claude-plugin/plugin.json` `"version"` to the same `X.Y.Z-uk.N`.** Plugin installs only treat the skill as updated when this field changes, so skipping it leaves every plugin install on the old version even after you push.

5. **Sanity-check the diff.** Spelling subs are mechanical, but larger upstream rewrites (new pattern sections, restructures) deserve a read. Confirm no US spellings leaked into the body and no UK changes leaked into excluded content.

6. **Update `README.md`** if the user-facing summary or version number should change.

7. **Commit and push.** Then other machines `git pull`; the Claude app copy gets re-uploaded.

> The skill's built-in "Step 0: Update Check" only *detects* staleness — it flags when upstream has moved and defers the actual sync to this repo protocol. It deliberately does **not** rewrite the running skill in place (that caused drift and stray edits). So the real update always happens here, in the repo, exactly as above.

## Editing rules

- Preserve valid YAML frontmatter (formatting and indentation).
- The prompt below the frontmatter is the product — edit it like a careful instruction document, not code.
- Keep the fork a thin layer over upstream. If you find yourself wanting to change wording beyond the manifest, reconsider — or capture it as a new manifest item so the next sync re-applies it.
- **Never `git merge upstream/main` into `main`.** This is a manual re-apply fork, not a merge fork: upstream and this fork diverge by design (spelling + the fork-only sections), so a merge would produce conflicts and US spellings. The `upstream` remote is for fetching and diffing only.
