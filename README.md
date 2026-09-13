# humaniser-uk

Paste in text that sounds like it was written by an AI, and this skill rewrites it so it reads like a real person wrote it — in **British English**.

It's a UK-spelling fork of the excellent [`humanizer`](https://github.com/blader/humanizer) skill for Claude. Same job, same 25 patterns, just `colour` instead of `color` (and one example swapped to UK papers). It tracks upstream closely — see [What's different](#whats-different-from-the-original) and [`AGENTS.md`](AGENTS.md).

Current version: **`3.0.0-uk.1`** (built from upstream `humanizer` 3.0.0).

---

## What it actually does

AI writing has tics. It over-eggs how *important* everything is, loves the word "vibrant", stacks things in threes, sprinkles em dashes everywhere, and ends on a cheery "the future looks bright!". Most readers can feel it even if they can't name it.

This skill spots those tics and rewrites them out, then does a second pass on its own draft — asking *"what still sounds AI here?"* and fixing what's left. The full pattern list with before/after examples is below, and the canonical version lives in [`SKILL.md`](SKILL.md).

---

## Get it on your devices

You use Claude in more than one place, so there are two ways in. Do whichever ones you use.

### On your computer (Claude Code in the terminal)

Copy the skill into Claude Code's skills folder with one command:

```bash
git clone https://github.com/JeevanDamalcheruvuHO/humaniser-uk.git ~/.claude/skills/humaniser
```

That's it — Claude Code now knows the `humaniser` skill. To get newer versions later:

```bash
cd ~/.claude/skills/humaniser && git pull
```

*(Use OpenCode too? It reads the same `~/.claude/skills/` folder, so this single clone covers both.)*

### On the Claude app (web, desktop, phone)

Skills you add to your account follow you to every device you sign in on — you only do this once:

1. Download this repo: green **Code** button on GitHub → **Download ZIP**, then unzip.
2. In the Claude app, open **Settings → Capabilities** (it may say **Skills**) and **add a skill**, pointing it at the unzipped folder (the one with `SKILL.md` inside).
3. Done — it's now on web, desktop, and mobile. Re-add it after an update to refresh.

---

## How to use it

Just ask, in plain English:

```
Humanise this for me:

[paste your text]
```

### Match your own voice (optional)

Want it to sound like *you* rather than generically "clean"? Give it a sample of your own writing first:

```
Here are a couple of paragraphs I wrote, for the style:
[paste 2-3 paragraphs of your own writing]

Now humanise this:
[paste the AI text]
```

It studies your sentence rhythm, word choices, and quirks, then applies them to the rewrite instead of producing generic output.

---

## Keeping it current

The original `humanizer` gets better over time. This fork is built to pull those improvements in, re-apply the British-English changes, and publish the result — so every device stays on the latest content. There are two ways to do it.

### The easy way (let the assistant do it)

Just use the skill and, now and then, ask the assistant to **"check for updates from upstream and sync the UK version."** The skill's built-in check tells you when upstream has moved; the assistant then runs the repo sync below (pull upstream → re-apply the UK changes → commit → push) and refreshes your installed copy. The skill flags staleness — it does **not** silently rewrite itself, so updates always go through the repo where you can see the diff.

### The manual way (pull → convert → push)

Everything that makes this a UK fork is a tidy checklist — the **UK Customisation Manifest** inside [`SKILL.md`](SKILL.md) — so an update is always: take the new upstream file, re-apply that checklist, push.

**One-time setup** (the maintainer's clone already has this; a fresh clone needs it):

```bash
cd ~/code/humaniser-uk
git remote add upstream https://github.com/blader/humanizer.git
git remote set-url --push upstream DISABLED   # never push to the original by accident
```

**Each time you want the latest:**

```bash
# 1. Get the latest original and see if it moved
git fetch upstream
git show upstream/main:SKILL.md | grep '^version:'      # upstream's version
grep '^upstream-version:' SKILL.md                      # what this fork is built from

# 2. If they differ, see exactly what changed upstream
git diff <last-synced-upstream-commit> upstream/main -- SKILL.md
```

**3. Convert to the UK version.** Apply the new upstream changes to `SKILL.md`, then walk the **UK Customisation Manifest** (sections A–G) so the British spellings, the *Guardian/Times* example swap, and the fork-only sections are re-applied. This is fiddly by hand, so the simplest path is to ask an AI assistant — *"update this fork to the latest upstream and re-apply the UK manifest"* — and point it at [`AGENTS.md`](AGENTS.md), which is the exact step-by-step recipe. Then bump the frontmatter: `version: X.Y.Z-uk.1` and `upstream-version: X.Y.Z`, and add a line to this README's version history.

**4. Publish it:**

```bash
git add SKILL.md README.md
git commit -m "humaniser X.Y.Z-uk.1: sync upstream A.B.C -> X.Y.Z"
git push
```

**5. Refresh your other devices:** on each computer running Claude Code, `git pull` (or nothing, if it's symlinked to this clone); in the Claude app, re-upload the skill.

> Tip: never `git merge upstream/main` — this fork diverges from the original on purpose (spelling + the extra sections), so a merge just causes conflicts. Always *re-apply the manifest* instead.

---

## What's different from the original

This fork is deliberately a thin layer over [`blader/humanizer`](https://github.com/blader/humanizer). The only intended differences:

- **British spellings** throughout (`humanise`, `colour`, `analyse`, `organisation`, `judgement`, `optimise`, …).
- **One example swapped** to UK outlets — *The Times* / *The Guardian* instead of the US/Indian papers in the "Borrowed authority" example.
- A **staleness check** ("Step 0") and the **UK Customisation Manifest** baked into `SKILL.md` — Step 0 flags when upstream has moved and defers the actual sync to the repo, so the loaded skill never rewrites itself out of step with the source.
- A few **extra AI-vocabulary words** in the "Overused AI words" pattern (seamless, harness, streamline, empower, holistic, utilise, navigate, unlock, elevate — with figurative/technical carve-outs). These are proposed upstream in [blader/humanizer#241](https://github.com/blader/humanizer/issues/241), carried on a separate, clearly-labelled line, and the fork drops any that upstream adopts — as it did with `robust`, which upstream added in 3.0.0.

Everything else — the patterns, the wording, the structure — tracks upstream.

---

## Overview

Based on [Wikipedia's "Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide, maintained by WikiProject AI Cleanup. That guide comes from observations of thousands of instances of AI-generated text.

The skill also includes a final "obviously AI generated" audit pass and a second rewrite, to catch lingering AI-isms in the first draft.

> **Key insight from Wikipedia:** "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."

---

## 25 patterns detected (with before/after examples)

Upstream 3.0.0 rebuilt the skill around **25 patterns ordered strongest-first** in five groups. §1–§5 justify an edit on a single sighting; patterns marked *weak alone* need company from other tells before you act. The names below match the current `SKILL.md`.

### A. Staging instead of stating (act on one sighting)

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 1 | **Not X but Y** | "It's not merely a song, it's a statement" | State the point directly |
| 2 | **One-line closers and dramatic fragments** | "No aesthetic prior. No nostalgia." / repeated "That is the real win." | Merge into a sentence with a real claim; cut the repeat |
| 3 | **Sayings that sound deep** | "At its core, what really matters is…" / "Symmetry is the language of trust" | Replace the saying with the specific claim |
| 4 | **Staged run-up before the point** | "Let's dive in", "Honestly?" | Start with the content |
| 5 | **Arguing with no one** | "I'm not saying documentation doesn't matter, but…" / "A tempting approach would be…" | Cut the unraised objection or fake option |

### B. Rhythm by rule

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 6 | **Forced triads** | "innovation, inspiration, and insights" | Keep three only when the meaning has three parts |
| 7 | **Repeated sentence openings** | "She… She… She…" | Merge, change subject, or begin with the action |
| 8 | **Dashes as the universal connector** | "institutions—not the people—yet this continues—" | Full stops, commas, colons, or parentheses |
| 9 | **Stacked qualifiers** *(weak alone)* | "could potentially possibly… might…" | Keep only qualifiers the source supports |
| 10 | **Hyphenated pairs everywhere** *(weak alone)* | "the report is high-quality" | "the report is high quality" (keep it before a noun) |
| 11 | **Passive voice and missing subjects** *(weak alone)* | "No configuration file needed" | Name the actor when it helps clarity |

### C. Inflation and borrowed authority

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 12 | **Overused AI words** (+ [UK fork additions](#whats-different-from-the-original)) | "Actually… enduring testament… landscape, showcasing" | "also… remain common" |
| 13 | **Inflated significance** | "marking a pivotal moment…" / "Despite these challenges… continues to thrive" / "the future looks bright" | Keep the fact, drop the significance; end on the last concrete fact |
| 14 | **Vague connection or association** | "He is associated with the Rajhans Orchestra" | Name the real relationship ("He founded and conducts…") |
| 15 | **Shallow -ing riders** | "symbolising… reflecting…" | Keep the fact, drop the -ing padding |
| 16 | **Sales language** | "nestled within the breathtaking region" | "is a town in the Gonder region" |
| 17 | **Borrowed authority** | "Experts believe…" / "cited in The Times, BBC, FT, and The Guardian" | Name the real source, or cut the claim/list |
| 18 | **Avoiding is, are, and has** | "serves as… features… boasts" | "is… has" |

### D. Formatting by rule

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 19 | **Bold as decoration** | "**Performance:** Performance improved" | Remove the bold; turn labelled lists into prose |
| 20 | **Decorative headings** | "Strategic Negotiations And Partnerships", 🚀 emojis, → arrows, rules | Sentence case, no decoration |
| 21 | **Curly quotation marks** *(weak alone)* | `said “the project”` | `said "the project"` |

### E. Leftovers from the chat and the draft (remove outright)

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 22 | **Chatbot residue** | "Great question!… I hope this helps!" | Remove the wrapper, keep the content |
| 23 | **Knowledge-limit disclaimers and guesses** | "While details are limited…", "maintains a low profile" | Say what the source doesn't show, or cut it |
| 24 | **A heading repeated in the first sentence** | "## Performance" + "Speed matters." | Let the heading do the work |
| 25 | **Writing about the previous version** | "This function was added to replace…" | Describe what it does now |

---

## Full example

**Before (AI-sounding):**
> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools—nestled at the intersection of research and practice—are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
>
> At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale, ensuring that organisations can remain agile while delivering seamless, intuitive, and powerful experiences to users. The tool serves as a catalyst. The assistant functions as a partner. The system stands as a foundation for innovation.
>
> Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts, from solo developers to cross-functional teams. The technology has been featured in The Guardian, Wired, and The Verge. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgement.
>
> - 💡 **Speed:** Code generation is significantly faster, reducing friction and empowering developers.
> - 🚀 **Quality:** Output quality has been enhanced through improved training, contributing to higher standards.
> - ✅ **Adoption:** Usage continues to grow, reflecting broader industry trends.
>
> While specific details are limited based on available information, it could potentially be argued that these tools might have some positive effect. Despite challenges typical of emerging technologies—including hallucinations, bias, and accountability—the ecosystem continues to thrive. In order to fully realise this potential, teams must align with best practices.
>
> In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey towards excellence. Let me know if you'd like me to expand on any section!

**After (humanised):**
> AI coding assistants can speed up the boring parts of the job. They're great at boilerplate: config files and the little glue code you don't want to write. They can also help you sketch a test, but you still have to read it.
>
> The dangerous part is how confident the suggestions look. I've accepted code that compiled and passed lint, then discovered later it missed the point because I stopped paying attention.
>
> If you treat it like autocomplete and review every line, it's useful. If you use it to avoid thinking, it will help you ship bugs faster.
>
> The only real backstop is tests. Without them, you're mostly judging vibes.

(`SKILL.md` walks through this in more detail, including the intermediate draft and the "what still sounds AI?" audit pass.)

---

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — primary source
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) — the maintaining group
- [`blader/humanizer`](https://github.com/blader/humanizer) — the upstream skill this forks

---

## Version history

Versions look like `X.Y.Z-uk.N`: the `X.Y.Z` is the upstream `humanizer` version this is built from, and `-uk.N` is the UK revision on top of it.

- **`3.0.0-uk.1`** — tracks upstream **3.0.0**, a major rebuild: the skill was reorganised into **25 patterns ordered strongest-first** in five groups (A Staging, B Rhythm, C Inflation, D Formatting, E Leftovers), realigned with the current Wikipedia article, and reworded throughout. Two patterns are new relative to the old set (vague connection/association; forced triads at paragraph scale). Upstream also adopted **`robust`** into its own AI-words list, so it was dropped from the fork line (nine fork words remain). UK-adapted as usual.
- **`2.11.2-uk.3`** — fork-only change: added ten extra §7 AI-vocabulary words (seamless, harness, streamline, empower, holistic, utilise, robust, navigate, unlock, elevate) on a separate labelled line, with figurative/technical carve-outs. Mirrors upstream issue [#241](https://github.com/blader/humanizer/issues/241) (open, unmerged); the fork carries them until/unless upstream adopts them. First deliberate content divergence from upstream. No upstream change.
- **`2.11.2-uk.2`** — fork-only change: reworked **Step 0** from a self-updater into a *staleness check*. It now flags when upstream has moved and defers the actual sync to the repo, instead of rewriting the running skill in place (which had let installed copies drift from the repo). No upstream change.
- **`2.11.2-uk.1`** — tracks upstream **2.11.2**. Upstream's "Rewrite in Plain Language" reworded every pattern into plainer English and restructured the sections; adds two patterns — **#34 answering objections no one raised** and **#35 rejecting fake alternatives** (33 → 35). UK-adapted as usual.
- **`2.9.1-uk.1`** — tracks upstream **2.9.1**. Adds a "never invent facts" rule (the audit now also checks for fabricated names, numbers, and citations), **Invocation Modes** (pasted text / file / embedded), and a condensed personality section; the internal worked example was dropped upstream and several pattern examples were tightened. Frontmatter moved to the Agent Skills shape (version now under `metadata:`). UK-adapted as usual.
- **`2.8.2-uk.1`** — tracks upstream **2.8.2**: `compatibility: any-agent`, a new "secondhand text" detection caveat, and a rewritten worked example. UK-adapted as usual.
- **`2.8.0-uk.1`** — first published UK fork. Tracks upstream **2.8.0** (33 patterns, including the style/cadence patterns #31–33 and the hard "cut em/en dashes" rule). Adds British spellings, the UK outlet swaps, the Step 0 self-update check, and the UK Customisation Manifest.

For the full upstream history (what changed in each `humanizer` release), see the original's [version history](https://github.com/blader/humanizer#version-history).

---

## Credits & licence

- Original skill: **[`blader/humanizer`](https://github.com/blader/humanizer)** by Siqi Chen, based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- British-English version: this fork.

[MIT licensed](LICENSE), same terms as the original.
