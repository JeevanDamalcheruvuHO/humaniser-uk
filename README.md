# humaniser-uk

Paste in text that sounds like it was written by an AI, and this skill rewrites it so it reads like a real person wrote it — in **British English**.

It's a UK-spelling fork of the excellent [`humanizer`](https://github.com/blader/humanizer) skill for Claude. Same job, same 33 patterns, just `colour` instead of `color` (and a couple of examples swapped to UK papers). It tracks upstream closely — see [What's different](#whats-different-from-the-original) and [`AGENTS.md`](AGENTS.md).

Current version: **`2.8.2-uk.1`** (built from upstream `humanizer` 2.8.2).

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

Just use the skill and, now and then, ask it to **"check for updates from upstream and update the UK version."** The skill fetches the latest original, compares versions, tells you what changed, re-applies the British spellings and example swaps automatically, and bumps the version. Say yes, then `git push` (below) to publish.

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
- **Two examples swapped** to UK outlets — *The Guardian* / *The Times* instead of the US/Indian papers in the notability example and the worked example.
- A **self-update mechanism** ("Step 0") and the **UK Customisation Manifest** baked into `SKILL.md`, so the fork can re-sync itself when upstream changes.

Everything else — the patterns, the wording, the structure — tracks upstream.

---

## Overview

Based on [Wikipedia's "Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide, maintained by WikiProject AI Cleanup. That guide comes from observations of thousands of instances of AI-generated text.

The skill also includes a final "obviously AI generated" audit pass and a second rewrite, to catch lingering AI-isms in the first draft.

> **Key insight from Wikipedia:** "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."

---

## 33 patterns detected (with before/after examples)

### Content patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 1 | **Significance inflation** | "marking a pivotal moment in the evolution of…" | "was established in 1989 to collect regional statistics" |
| 2 | **Notability name-dropping** | "cited in The Times, BBC, FT, and The Guardian" | "In a 2024 Guardian interview, she argued…" |
| 3 | **Superficial -ing analyses** | "symbolising… reflecting… showcasing…" | Remove, or expand with actual sources |
| 4 | **Promotional language** | "nestled within the breathtaking region" | "is a town in the Gonder region" |
| 5 | **Vague attributions** | "Experts believe it plays a crucial role" | "according to a 2019 survey by…" |
| 6 | **Formulaic challenges** | "Despite challenges… continues to thrive" | Specific facts about the actual challenges |

### Language patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 7 | **AI vocabulary** | "Actually… additionally… testament… landscape… showcasing" | "also… remain common" |
| 8 | **Copula avoidance** | "serves as… features… boasts" | "is… has" |
| 9 | **Negative parallelisms / tailing negations** | "It's not just X, it's Y", "…, no guessing" | State the point directly |
| 10 | **Rule of three** | "innovation, inspiration, and insights" | Use the natural number of items |
| 11 | **Synonym cycling** | "protagonist… main character… central figure… hero" | "protagonist" (repeat when clearest) |
| 12 | **False ranges** | "from the Big Bang to dark matter" | List the topics directly |
| 13 | **Passive voice / subjectless fragments** | "No configuration file needed" | Name the actor when it helps clarity |

### Style patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 14 | **Em/en dashes** | "institutions—not the people—yet this continues—" | Cut them: full stops, commas, colons, or parentheses |
| 15 | **Boldface overuse** | "**OKRs**, **KPIs**, **BMC**" | "OKRs, KPIs, BMC" |
| 16 | **Inline-header lists** | "**Performance:** Performance improved" | Convert to prose |
| 17 | **Title Case Headings** | "Strategic Negotiations And Partnerships" | "Strategic negotiations and partnerships" |
| 18 | **Emojis** | "🚀 Launch Phase: 💡 Key Insight:" | Remove emojis |
| 19 | **Curly quotes** | `said “the project”` | `said "the project"` |
| 26 | **Hyphenated word pairs** | "cross-functional, data-driven, client-facing" | Drop hyphens on common pairs in predicate position |
| 27 | **Persuasive authority tropes** | "At its core, what really matters is…" | State the point directly |
| 28 | **Signposting announcements** | "Let's dive in", "Here's what you need to know" | Start with the content |
| 29 | **Fragmented headers** | "## Performance" + "Speed matters." | Let the heading do the work |
| 30 | **Diff-anchored writing** | "This function was added to replace…" | Describe what it does, not what changed |
| 31 | **Manufactured punchlines / staccato drama** | "It had no preference. No prior. No nostalgia." | Use varied sentence lengths and concrete claims |
| 32 | **Aphorism formulas** | "Symmetry is the language of trust" | Replace the formula with the actual claim |
| 33 | **Conversational rhetorical openers** | "Honestly? It depends…" | Remove the fake-candid setup |

### Communication patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 20 | **Chatbot artefacts** | "I hope this helps! Let me know if…" | Remove entirely |
| 21 | **Cutoff disclaimers / speculative gap-filling** | "While details are limited…", "maintains a low profile" | Find sources, say what isn't known, or remove |
| 22 | **Sycophantic tone** | "Great question! You're absolutely right!" | Respond directly |

### Filler and hedging

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 23 | **Filler phrases** | "In order to", "Due to the fact that" | "To", "Because" |
| 24 | **Excessive hedging** | "could potentially possibly" | "may" |
| 25 | **Generic conclusions** | "The future looks bright" | Specific plans or facts |

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

- **`2.8.2-uk.1`** — tracks upstream **2.8.2**: `compatibility: any-agent`, a new "secondhand text" detection caveat, and a rewritten worked example (a Lisbon travel-blog rewrite). UK-adapted as usual.
- **`2.8.0-uk.1`** — first published UK fork. Tracks upstream **2.8.0** (33 patterns, including the style/cadence patterns #31–33 and the hard "cut em/en dashes" rule). Adds British spellings, the UK outlet swaps, the Step 0 self-update check, and the UK Customisation Manifest.

For the full upstream history (what changed in each `humanizer` release), see the original's [version history](https://github.com/blader/humanizer#version-history).

---

## Credits & licence

- Original skill: **[`blader/humanizer`](https://github.com/blader/humanizer)** by Siqi Chen, based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- British-English version: this fork.

[MIT licensed](LICENSE), same terms as the original.
