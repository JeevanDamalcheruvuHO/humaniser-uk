# AGENTS.md

Guidance for an AI assistant (Claude Code, Codex, etc.) working in this repo. The most common job here is **pulling the latest upstream `humanizer` and re-applying the UK conversion** — this file is the recipe for that.

## What this repo is

A UK-English fork of [`blader/humanizer`](https://github.com/blader/humanizer), a Claude Code / OpenCode skill implemented entirely as Markdown. The runtime artifact is `SKILL.md` (YAML frontmatter + the editor prompt). There is no build step and no code to run. **`SKILL.md` is the source of truth.**

This fork is intended to be a *minimal, well-documented delta* over upstream: the same skill, with British spellings and one example outlet swapped. Every intended difference is listed inside `SKILL.md` under **"UK Customisation Manifest" (sections A–G)**. Do not introduce UK-specific changes that aren't captured there — add them to the manifest first.

## Key files

- `SKILL.md` — the skill, plus two fork-only sections near the top: **"Step 0: Upstream Self-Update Check"** and the **"UK Customisation Manifest."** Source of truth.
- `README.md` — for humans: what it does, install, usage, how to update.
- `AGENTS.md` — this file.
- `LICENSE` — MIT.

## Versioning

`X.Y.Z-uk.N`:
- `X.Y.Z` mirrors the upstream `humanizer` version this fork is synced against (stored in `SKILL.md` frontmatter as `upstream-version`).
- `-uk.N` increments when fork content/manifest changes without an upstream bump.

The frontmatter `version:` is `X.Y.Z-uk.N`; `upstream-version:` is the plain `X.Y.Z`.

## How to update from upstream (the main task)

1. **Fetch upstream `SKILL.md`:**
   ```
   https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md
   ```
   (or `git fetch` a clone of `https://github.com/blader/humanizer.git` and read `origin/main:SKILL.md`).

2. **Compare versions.** Read upstream's frontmatter `version:` and this fork's `upstream-version:`. Equal → nothing to do. Different → continue.

3. **Re-apply the UK Customisation Manifest.** Start from the *fresh upstream content* and work through manifest sections A–G in order:
   - **A. Frontmatter** — `name: humaniser`; keep `upstream-source` / `upstream-repo` / `upstream-version`; ensure `WebFetch` + `Bash` in `allowed-tools`; add the "UK English variant" line to `description`.
   - **B. Spelling table** — apply the US→UK whole-word, case-preserving substitutions (colour, analyse, organisation, judgement, colonisation, memoisation, etc.). Do **not** touch the exclusions (`license: MIT`, code identifiers, URLs, the curly-quote typography example).
   - **C. Targeted phrase swaps** — e.g. in §14, "a period (start a new sentence)" → "a full stop (...)".
   - **D. Example outlet swaps** — §2 and the Full Example: US/Indian papers → *The Guardian* / *The Times*.
   - **E. Title** — `# Humaniser: ...`.
   - **F. Preserve** the Step 0 section and the manifest itself.
   - **G.** Leave upstream's *own* prose em dashes alone (the no-em-dash rule is for humanised output, not this file).

4. **Bump the version.** Set `upstream-version:` to the new upstream `X.Y.Z` and `version:` to `X.Y.Z-uk.1` (use `-uk.N+1` if only the manifest changed without an upstream bump).

5. **Sanity-check the diff.** Spelling subs are mechanical, but larger upstream rewrites (new pattern sections, restructures) deserve a read. Confirm no US spellings leaked into the body and no UK changes leaked into excluded content.

6. **Update `README.md`** if the user-facing summary or version number should change.

7. **Commit and push.** Then other machines `git pull`; the Claude app copy gets re-uploaded.

> The skill's built-in "Step 0: Upstream Self-Update Check" performs exactly this flow interactively. Invoking the skill and choosing "update now" is the same thing as steps 1–4; this file just lets you do it deliberately from the repo.

## Editing rules

- Preserve valid YAML frontmatter (formatting and indentation).
- The prompt below the frontmatter is the product — edit it like a careful instruction document, not code.
- Keep the fork a thin layer over upstream. If you find yourself wanting to change wording beyond the manifest, reconsider — or capture it as a new manifest item so the next sync re-applies it.
