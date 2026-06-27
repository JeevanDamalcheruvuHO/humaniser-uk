# humaniser-uk

Paste in text that sounds like it was written by an AI, and this skill rewrites it so it reads like a real person wrote it — in **British English**.

It's a UK-spelling fork of the excellent [`humanizer`](https://github.com/blader/humanizer) skill for Claude. Same job, same patterns, just `colour` instead of `color`.

---

## What it actually does

AI writing has tics. It over-eggs how *important* everything is, loves the word "vibrant", stacks things in threes, sprinkles em dashes everywhere, and ends on a cheery "the future looks bright!". Most readers can feel it even if they can't name it.

This skill spots those tics and rewrites them out. A few examples of what it changes:

| It sees this (AI-ish) | It gives you this (human) |
|---|---|
| "marking a pivotal moment in the evolution of…" | "was set up in 1989 to collect regional statistics" |
| "nestled within the breathtaking region of…" | "is a town in the Gonder region" |
| "Great question! I hope this helps! Let me know if…" | *(gone — that's chatbot chatter, not content)* |
| "It's not just a song, it's a statement." | "The heavy beat adds to the aggressive tone." |
| "institutions—not the people—yet this continues—" | "institutions, not the people, yet this continues" |

It also does a second pass on its own work, asking *"what still sounds AI here?"* and fixing what's left. Full details and all the patterns live in [`SKILL.md`](SKILL.md).

---

## Get it on your devices

You use Claude in more than one place, so there are two ways in. Do whichever ones you use.

### On your computer (Claude Code in the terminal)

Copy the skill into Claude Code's skills folder with one command:

```bash
git clone https://github.com/JeevanDamalcheruvuHO/humaniser-uk.git ~/.claude/skills/humaniser
```

That's it. Claude Code now knows the `humaniser` skill. To get newer versions later:

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

Want it to sound like *you* rather than generically "clean"? Give it a sample of your own writing first:

```
Here are a couple of paragraphs I wrote, for the style:
[paste your writing]

Now humanise this:
[paste the AI text]
```

It studies your rhythm and word choices and matches them.

---

## Keeping it current

The original `humanizer` gets better over time. Pulling those improvements into this UK version is meant to be painless. Two ways:

- **The easy way:** just use the skill and, now and then, ask it to **"check for updates from upstream."** It fetches the latest original, re-applies the British-spelling changes automatically, and tells you what's new. Say yes and it updates itself.
- **The repo way (for keeping several machines in step):** in `~/code/humaniser-uk` (or wherever you keep this), run `git pull` to get the newest version, and `git push` after you've updated it.

Behind the scenes, every difference between this fork and the original is written down as a tidy checklist (the "UK Customisation Manifest" inside `SKILL.md`), so updates stay clean instead of drifting. If you ever ask an AI assistant to do the update for you, point it at [`AGENTS.md`](AGENTS.md) — that's the step-by-step recipe.

**Version numbers** look like `2.8.0-uk.1`: the `2.8.0` is the original version this is built from, and `-uk.1` is the UK revision on top of it.

---

## Credits & licence

- Original skill: **[`blader/humanizer`](https://github.com/blader/humanizer)** by Siqi Chen, based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- British-English version: this fork.

[MIT licensed](LICENSE), same as the original.
