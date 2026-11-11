# AGENTS.md

Guidance for an AI assistant (Claude Code, Codex, etc.) working in this repo. The most common job here is **pulling the latest upstream `humanizer` and re-applying the UK conversion** — this file is the recipe for that, and it holds the **UK Customisation Manifest**.

## What this repo is

A UK-English fork of [`blader/humanizer`](https://github.com/blader/humanizer), an agent skill implemented entirely as Markdown. The runtime artifact is `SKILL.md` (YAML frontmatter + the editor prompt). There is no build step and no code to run. **`SKILL.md` is the source of truth for the skill.**

This fork is intended to be a *minimal, well-documented delta* over upstream: the same skill, with British spellings, one example's outlets swapped, a short update check, a few extra AI-vocabulary words, and a line on invisible characters. Every intended difference is listed in the **UK Customisation Manifest** below (sections A–I). Do not introduce UK-specific changes that aren't captured there — add them to the manifest first.

The manifest lives here rather than in `SKILL.md` because every word of `SKILL.md` is read on each use of the skill. Maintenance instructions do not belong in the prompt.

## Key files

- `SKILL.md` — the skill, plus one short fork-only section near the top, **"Step 0: Update check"**. Source of truth.
- `AGENTS.md` — this file: the sync recipe and the manifest.
- `README.md` — for humans: what it does, install, usage, how to update.
- `.claude-plugin/plugin.json` — the Claude plugin manifest. Its `"version"` must match `SKILL.md`.
- `.claude-plugin/marketplace.json` — lets users add this repo as a Claude plugin marketplace.
- `.cursor-plugin/plugin.json` — the Cursor plugin manifest. Its `"version"` must match too. It has no `skills` path, so Cursor loads the root `SKILL.md`.
- `package.json` — makes the repo a pi package; `pi.skills` points at the repo root. It has no `version` field because pi installs from git.
- `agents/openai.yaml` — display name, short description and default prompt for OpenAI-compatible agents such as Codex.
- `scripts/sync-upstream.py` — applies the manifest to upstream's `SKILL.md` mechanically. `--check` verifies that the current `SKILL.md` is exactly upstream plus the manifest. Standard library only.
- `scripts/check-fork.py` — checks the fork after a sync: versions agree, no US spellings or US dates leaked, README pattern names match, and `SKILL.md` has not grown past upstream. Standard library only.
- `.github/workflows/check.yml` — runs `scripts/check-fork.py` on GitHub for every push to `main` and every pull request.
- `LICENSE` — MIT.

## Versioning

`X.Y.Z-uk.N`:
- `X.Y.Z` mirrors the upstream `humanizer` version this fork is synced against (stored in `SKILL.md` frontmatter as `metadata.upstream-version`).
- `-uk.N` increments when fork content changes without an upstream bump.

`metadata.version` in `SKILL.md` and `"version"` in `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json` are all `X.Y.Z-uk.N`; `metadata.upstream-version` is the plain `X.Y.Z`.

## How to update from upstream (the main task)

1. **Fetch upstream `SKILL.md`.** This repo already has a pull-only `upstream` remote configured (`https://github.com/blader/humanizer.git`, tracking `main`, push URL disabled), so:
   ```
   git fetch upstream && git show upstream/main:SKILL.md
   ```
   (or read the raw file directly: `https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md`).

2. **Compare versions.** Read upstream's `metadata.version` and this fork's `metadata.upstream-version`. Equal → nothing to do. Different → continue.

3. **Re-apply the UK Customisation Manifest.** Run:
   ```
   python3 scripts/sync-upstream.py
   ```
   It fetches upstream, rebuilds `SKILL.md` from the *fresh upstream content* with manifest sections A–H applied, carries Step 0 and the extra AI-words line over from the current `SKILL.md`, and sets the versions in `SKILL.md` and `plugin.json` (so step 4 is done for you). Each `REVIEW:` line it prints is a manifest item it could not apply, usually because upstream reworded the passage or adopted a fork word. Resolve each one by hand, following the manifest below, and update the script so the next sync handles it. If the script cannot run, apply sections A–H by hand.

4. **Bump the version.** Set `metadata.upstream-version` to the new upstream `X.Y.Z` and `metadata.version` to `X.Y.Z-uk.1` (use `-uk.N+1` if only fork content changed without an upstream bump).

   **Also bump `"version"` in `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json` to the same `X.Y.Z-uk.N`.** Plugin installs only treat the skill as updated when this field changes, so skipping it leaves every plugin install on the old version even after you push.

5. **Sanity-check the diff.** Read `git diff SKILL.md`: the script converts spellings it knows, so look for new US spellings, new US outlets or examples, and new sections that need a manifest decision. Then run `python3 scripts/check-fork.py` and fix anything it reports; it also confirms `SKILL.md` is exactly upstream plus the manifest. Spelling subs are mechanical, but larger upstream rewrites (new pattern sections, restructures) deserve a read. Diff the result against upstream and confirm the only differences are manifest ones: no US spellings leaked into the body and no UK changes leaked into excluded content.

6. **Update `README.md`.** Bump the version line, add a version-history entry, and bring the pattern table, the full example (upstream's README example, UK-spelt) and any behaviour summary into line with the new upstream.

7. **Commit and push.** Then refresh the installed copies: `git pull` in each cloned skill directory (`~/.claude/skills/humaniser` for Claude Code), re-run `npx skills add JeevanDamalcheruvuHO/humaniser-uk --global --agent <name>` for each copy the Skills CLI installed (those are plain copies, not clones), and update the plugin wherever it was installed from the marketplace. A copy uploaded to the Claude app by hand must be re-uploaded.

> The skill's built-in "Step 0: Update check" only *detects* staleness — it flags when upstream has moved and defers the actual sync to this repo protocol. It deliberately does **not** rewrite the running skill in place (that caused drift and stray edits). So the real update always happens here, in the repo, exactly as above.

## UK Customisation Manifest

These are the only intended differences from upstream. Upstream renumbers and regroups patterns between releases, so the entries below name patterns by title, with the current section number as a hint only.

### A. Frontmatter

Upstream uses the Agent Skills frontmatter shape: `name`, `description`, `license`, and a `metadata:` block holding `version`. Re-apply on top of that:

- `name: humanizer` → `name: humaniser`
- Add a sentence to the `description` block noting it is a UK English variant.
- Under `metadata:`, keep or set these fields:
  - `version: "X.Y.Z-uk.N"` — the upstream version number with a `-uk.N` suffix
  - `upstream-version: "X.Y.Z"` — the upstream version this fork was synced against
  - `upstream-repo: https://github.com/blader/humanizer`
  - `upstream-source: https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md`
- Do **not** re-add `allowed-tools` or `compatibility`. Upstream dropped them for cross-agent portability, and Step 0's fetch needs no whitelist.

### B. Spelling substitutions (global, case-preserving)

Apply these as whole-word replacements. Preserve case (e.g. `Color` → `Colour`, `COLOR` → `COLOUR`).

| US | UK |
|---|---|
| humanize / humanizer / humanized / humanizing | humanise / humaniser / humanised / humanising |
| analyze / analyzed / analyzing | analyse / analysed / analysing |
| emphasize / emphasized / emphasizing | emphasise / emphasised / emphasising |
| symbolize / symbolizing | symbolise / symbolising |
| decentralize / decentralization | decentralise / decentralisation |
| categorize / categorized / categorizing | categorise / categorised / categorising |
| regularize | regularise |
| organize / organization / organizational / organizations | organise / organisation / organisational / organisations |
| realize / realized / realizing | realise / realised / realising |
| optimize / optimized / optimizing | optimise / optimised / optimising |
| capitalize | capitalise |
| memoization | memoisation |
| colonization | colonisation |
| color / colors / colored | colour / colours / coloured |
| behavior / behaviors / behavioral | behaviour / behaviours / behavioural |
| humor | humour |
| favor / favored / favoring / favorable / favorite | favour / favoured / favouring / favourable / favourite |
| judgment | judgement |
| acknowledgment | acknowledgement |
| artifact / artifacts | artefact / artefacts (in non-technical senses; leave Claude Code "Artifacts" feature name alone if encountered) |
| skeptical | sceptical |
| mislabeling | mislabelling |
| totaling | totalling |
| toward (preposition, when not part of "towards" already) | towards |
| backward (adverb) | backwards |
| neighborhood / neighborhoods | neighbourhood / neighbourhoods |
| traveler / travelers / traveling | traveller / travellers / travelling |
| savor / savoring | savour / savouring |
| story / stories (building floor sense, e.g. six-story) | storey / storeys |
| candor | candour |
| defense | defence |
| labeled / labeling | labelled / labelling |
| centimeter / meter (unit of length) and similar `-meter` units | centimetre / metre |
| other unlisted `-ize`/`-ization` verbs (recognize, specialize, prioritize, standardize, …) | `-ise`/`-isation` (recognise, specialise, prioritise, standardise, …) |

Do **not** change:
- `license: MIT` (a standard term)
- `program` (in software contexts; "programme" only for broadcast/event senses, which don't appear here)
- Straight-vs-curly quote example content (it's about typography, not dialect)
- Proper nouns, code identifiers, URLs, the word "behaviors" inside YAML keys if any appear

### C. Targeted phrase swaps

- In the **dashes pattern** (currently §8, "Dashes as the universal connector"), change the replacement-preference phrase "Replace each dash with a period, comma, colon, or parentheses" → "Replace each dash with a full stop, comma, colon, or parentheses". Treat any other punctuation-sense "period(s)" the same way ("full stop(s)"), such as "with periods between words" in the one-line-closers pattern (currently §2).
- Write dates day first. In "When not to act", "November 30, 2022" → "30 November 2022". Treat any other month-day-year date in the skill's own prose the same way.

### D. Example outlet swaps

In the **prestige-list example** (currently the "Borrowed authority" pattern, §17):
- "Before" block: `The New York Times` → `The Times`, and `The Hindu` → `The Guardian`.
- "After" block: replace any surviving US/Indian outlet with its Before-block UK counterpart (e.g. `New York Times` → `Times`), so the After stays consistent with the swapped Before.

If any other example names a US/Indian outlet as the illustration's own voice, swap it to *The Guardian* / *The Times* too.

Leave genuine Wikipedia-style geographic/cultural examples (Catalonia, Korattur / Chennai, the Texas temple, Ethiopia, Somali cuisine, Gallery 825, the Haolai River, Rajhans Orchestra / Pakistan) **unchanged** — altering them would distort the source material.

### E. Title change

- `# Humanizer: remove AI writing patterns` → `# Humaniser: remove AI writing patterns` (match upstream's current casing; earlier upstreams used Title Case, so adjust to whatever upstream currently ships).

### F. Preserve the Step 0 section

"Step 0: Update check" is a fork addition. Copy it from the current fork `SKILL.md` and place it after the intro line, before "Why AI text sounds the way it does". Keep it short: it is read on every use. Do not move the manifest back into `SKILL.md`.

### G. Leave upstream's own em dashes alone

Upstream's explanatory prose may use an em dash in its own sentences. The dashes pattern's "no em dashes" rule is guidance for *humanised output*, not for the skill file — keep upstream's own punctuation verbatim rather than rewriting it.

### H. Fork additions — extra AI-vocabulary words and invisible characters

Unlike A–G (which only re-shape upstream), these are the fork's deliberate **content** additions. Each is a line starting `**Also (UK fork additions):**`, placed after the "Watch for" line of the pattern it belongs to. `sync-upstream.py` carries every such line over from the current `SKILL.md` and finds its pattern by title, so edit the lines there.

**H1. Extra AI words.** After upstream's overused-AI-words list (currently §12, "Overused AI words"), append a separate **"Also (UK fork additions):"** line with these extra words, each with its carve-out. Copy the line from the current fork `SKILL.md`; it holds:

> seamless; harness (verb); streamline; empower; holistic; utilise/utilize (where "use" would do; keep the metric noun *utilisation*); navigate (figurative "navigating the complexities of…", not literal "navigate to the page"); unlock (figurative "unlock your potential/insights", not "unlock a feature/account"); elevate (figurative "elevate your brand/writing", not literal/medical "elevated"); leverage (verb, where "use" would do; keep financial leverage); moreover/furthermore (as sentence openers).

The first nine were proposed upstream in [blader/humanizer#241](https://github.com/blader/humanizer/issues/241), which was closed as not planned on 6 September 2026, so they are a standing fork addition. Upstream adopted `robust` on its own in 3.0.0, and it was dropped from this line. `leverage` and `moreover`/`furthermore` were added on 11 November 2026 after comparing the fork with the unrelated [ModernOps888/humaniser](https://github.com/ModernOps888/humaniser) word lists; they have not been proposed upstream. Keep the line separate and labelled so upstream's own list stays a clean diff; drop any word upstream later adopts (the sync script reports those).

**H2. Invisible characters.** In the "Chatbot residue" pattern (currently §22), a fork line tells the editor to delete zero-width characters and replace stray non-breaking spaces, with carve-outs for code, emoji, scripts that need joiners, and number-unit spacing. Upstream covers curly quotes but not these. Added on 11 November 2026 from the same comparison.

### I. Package files for other agents

Upstream ships manifests so several agents can install the skill. The fork keeps its own copies; they are not rebuilt from upstream, so compare them with upstream's when a release changes its packaging (`git diff <last-synced-commit> upstream/main -- .claude-plugin .cursor-plugin package.json agents`). In each one the name is `humaniser`, the description starts "UK English fork of humanizer", the links point at this repository, and the keyword is `humanise`.

## Editing rules

- Preserve valid YAML frontmatter (formatting and indentation).
- The prompt below the frontmatter is the product — edit it like a careful instruction document, not code.
- Keep `SKILL.md` close to upstream's size. Upstream caps its own at 5,500 words; anything about maintaining the fork goes in this file.
- The manifest is the specification and `scripts/sync-upstream.py` is its mechanical form. Change them together: a UK change made only in `SKILL.md` is lost at the next sync, and `check-fork.py` will fail until the script reproduces it. Step 0 and the extra AI-words line are the exception; edit those in `SKILL.md` and the script carries them over.
- Keep the fork a thin layer over upstream. If you find yourself wanting to change wording beyond the manifest, reconsider — or capture it as a new manifest item so the next sync re-applies it.
- **Never `git merge upstream/main` into `main`.** This is a manual re-apply fork, not a merge fork: upstream and this fork diverge by design (spelling + the fork-only section), so a merge would produce conflicts and US spellings. The `upstream` remote is for fetching and diffing only.
