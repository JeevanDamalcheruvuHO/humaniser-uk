# humaniser-uk

A **UK English** fork of the [`humanizer`](https://github.com/blader/humanizer) skill for Claude — it removes the tells of AI-generated writing (inflated significance, promotional language, em-dash overuse, rule-of-three, AI vocabulary, sycophancy, and so on) so text reads as if a person wrote it.

This fork tracks upstream closely. The only intended differences are:

- **British spellings** throughout (`humanise`, `colour`, `analyse`, `organisation`, `judgement`, …).
- **One example swapped** to a UK outlet (*The Guardian* / *The Times* instead of US/Indian papers).
- A self-contained **"Step 0" self-update mechanism** and a **UK Customisation Manifest** baked into `SKILL.md`, so the fork can re-sync itself when upstream changes.

Current version: **`2.8.0-uk.1`** (tracks upstream `humanizer` **2.8.0**).

The whole skill is the single file [`SKILL.md`](SKILL.md).

---

## Using it across your devices

Claude stores skills differently depending on the surface, so there are two paths. You can use either or both.

### Claude Code (CLI) — per machine, synced with git

Personal skills live in `~/.claude/skills/<name>/`. Clone this repo straight into that folder on each machine you use:

```bash
git clone git@github.com:JeevanDamalcheruvuHO/humaniser-uk.git ~/.claude/skills/humaniser
```

(or with HTTPS: `git clone https://github.com/JeevanDamalcheruvuHO/humaniser-uk.git ~/.claude/skills/humaniser`)

That's it — Claude Code discovers it as the `humaniser` skill. To pull later updates on any machine:

```bash
cd ~/.claude/skills/humaniser && git pull
```

If you'd rather keep the repo elsewhere and symlink it (so one `git pull` updates every checkout on the machine):

```bash
git clone git@github.com:JeevanDamalcheruvuHO/humaniser-uk.git ~/code/humaniser-uk
ln -s ~/code/humaniser-uk ~/.claude/skills/humaniser
```

### Claude apps (web, desktop, mobile) — synced via your account

Skills uploaded to your Anthropic account follow you across claude.ai, the desktop app, and mobile automatically — you upload once.

1. Download this repo (clone it, or use **Code → Download ZIP** on GitHub).
2. In the Claude app, open **Settings → Capabilities** (the section may be labelled *Skills*) and **add / upload a skill**, pointing it at the folder that contains `SKILL.md`.
3. It's now available on every device where you're signed in. Re-upload after a version bump to refresh it.

### How to invoke it

Once installed, just ask, e.g.:

```
Humanise this text: <paste text>
```

Optionally give it a writing sample to match your voice:

```
Humanise this. Match my style from notes/my-writing.md
```

---

## Keeping it up to date with upstream

The original `humanizer` skill is actively maintained, so new pattern sections and refinements land upstream regularly. There are two ways to bring those in. They stack: use **A** to do the transformation, **B** to distribute the result to all your devices.

### Option A — built-in self-update (easiest)

`SKILL.md` contains a **"Step 0: Upstream Self-Update Check"** that runs when the skill is invoked. It:

1. fetches upstream `SKILL.md` from `blader/humanizer`,
2. compares the upstream `version:` against this fork's `upstream-version:`,
3. if upstream is newer, summarises what changed and offers to **re-apply the UK Customisation Manifest** and rewrite the file.

So in practice: invoke the skill now and then, and when it reports a new upstream version, say **"update now"**. It re-applies the British spellings, the example swap, and the manifest, then bumps the version (e.g. `2.8.0-uk.1` → `2.9.0-uk.1`).

> Sanity-check the result before committing. The spelling substitutions are mechanical, but larger upstream rewrites deserve a quick read of the `git diff` — which is exactly why keeping this in a repo (rather than editing the live skill in place) is worth it.

### Option B — git workflow (reproducible, multi-device)

Treat this repo as the single source of truth and track upstream as a remote:

```bash
# one-time
git remote add upstream https://github.com/blader/humanizer.git

# whenever you want to check for updates
git fetch upstream
git log --oneline HEAD..upstream/main -- SKILL.md   # what changed upstream?
```

If there's a new upstream version:

1. Regenerate the UK file — let Option A's self-update do the re-application, **or** apply the **UK Customisation Manifest** (the section near the top of `SKILL.md`) by hand. The manifest is the canonical list of every intended difference from upstream: frontmatter tweaks, the spelling table, the targeted phrase swaps, the example outlet swaps, and the title change.
2. Commit the regenerated file with the new version number:
   ```bash
   git add SKILL.md && git commit -m "humaniser X.Y.Z-uk.1 (track upstream X.Y.Z)"
   git push
   ```
3. On your other machines: `git pull`. In the Claude apps: re-upload.

### The UK Customisation Manifest

Everything that makes this a UK fork is documented as an explicit, repeatable checklist inside `SKILL.md` under **"UK Customisation Manifest"** (sections A–G): frontmatter, the US→UK spelling table, targeted phrase swaps, the example outlet swaps, the title change, and the rule to preserve the self-update section. As long as you re-apply that manifest after each upstream pull, the fork stays a clean, minimal delta over upstream rather than drifting.

### Versioning

`X.Y.Z-uk.N` where:

- `X.Y.Z` mirrors the upstream `humanizer` version this fork was synced against.
- `-uk.N` increments when the manifest or fork-specific content changes without an upstream bump.

---

## Credits & licence

- Original skill: **[`blader/humanizer`](https://github.com/blader/humanizer)** by Siqi Chen, based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- UK English adaptations: this fork.

Licensed under the [MIT License](LICENSE), the same terms as upstream.
