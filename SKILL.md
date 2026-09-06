---
name: humaniser
description: |
  Rewrite AI-sounding text so it reads naturally without changing what it says.
  Use when editing or reviewing prose for inflated claims,
  sales language, vague sources, repetitive structure, stock AI words, passive
  voice, filler, or chatbot artefacts. Based on Wikipedia's "Signs of AI writing."
  UK English variant: British spellings, one example adapted, and a few extra §7 AI-vocabulary words; otherwise tracks upstream.
license: MIT
metadata:
  version: "2.11.2-uk.3"
  upstream-version: "2.11.2"
  upstream-repo: https://github.com/blader/humanizer
  upstream-source: https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md
---

# Humaniser: remove AI writing patterns

Rewrite AI-sounding text so it reads like the writer, not a chatbot. Do not change what it says or make up details.

The patterns below come from Wikipedia's ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

## Step 0: Update Check (Run First, Every Invocation)

This skill is a UK-English fork of [blader/humanizer](https://github.com/blader/humanizer), maintained as a git repository — the source of truth is [JeevanDamalcheruvuHO/humaniser-uk](https://github.com/JeevanDamalcheruvuHO/humaniser-uk). **This file is a read-only consumption copy. Never re-apply the manifest by editing this file in place.** Rewriting the loaded skill makes it drift from the repo and leaves stray edits; updates flow *from* the repo, never back into it from here.

Do a lightweight staleness check at the start of an invocation, then get on with the user's request.

### Procedure

1. **Read the local `upstream-version`** from the `metadata:` block of this file's frontmatter (the upstream version this fork was last synced against).

2. **Fetch upstream** with `WebFetch` (or `Bash` `curl -sL`):

   ```
   https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md
   ```

   If the fetch fails (network error, 404, timeout), log a one-line note ("Skipped upstream check: <reason>") and continue. Never block the user's task on this.

3. **Parse the upstream version** from its frontmatter (`metadata.version`; older upstreams used a top-level `version:` — accept either).

4. **Compare** (string equality):
   - **Equal** → the fork is current. Continue silently to the user's task.
   - **Upstream is newer** → the fork needs a sync. This is a maintenance job, not something to do silently in the middle of a humanising request. Tell the user once, in one line — e.g. "Heads-up: upstream humanizer is now `<Y>`; this fork tracks `<X>`. Ask me to sync it when you like." — then carry on with what they actually asked for. Do **not** rewrite this file.

5. **When the user asks to sync**, run the repo protocol in [`AGENTS.md`](AGENTS.md) — never an in-place edit of the running skill:
   1. In the source-of-truth repo clone: `git fetch upstream`, re-apply the **UK Customisation Manifest** over the fresh upstream content, bump `metadata.version` / `upstream-version`, update the README, then `commit` and `push`.
   2. Refresh the consumption copies so the running skill picks it up: in the installed skill directory (`~/.claude/skills/humaniser` for Claude Code) run `git fetch origin && git reset --hard origin/main`; copy the repo's `SKILL.md` over any agent-mode plugin copy.

### If this copy is only behind the repo

If upstream matches the fork's `upstream-version` but this file is older than the published fork (a new `-uk.N` was released), the copy is merely stale — refresh it, don't re-convert: from this skill's directory, `git fetch origin && git reset --hard origin/main`.

### When to skip the check

- The user says "skip the update check" or "don't check upstream".
- The fetch fails (see step 2).
- You already checked earlier this session — check once per session, not per message.

### When the user is mid-task

If the user is mid-flow on a humanising job, hold the heads-up until a natural stopping point. Don't interrupt with a maintenance note.

---

## UK Customisation Manifest

When re-applying UK adaptations after an upstream update, work through this list in order. These are the only intended differences from upstream.

### A. Frontmatter

Upstream uses the Agent Skills frontmatter shape: `name`, `description`, `license`, and a `metadata:` block holding `version`. Re-apply on top of that:

- `name: humanizer` → `name: humaniser`
- Add a sentence to the `description` block noting it is a UK English variant.
- Under `metadata:`, keep or set these fields:
  - `version: "X.Y.Z-uk.N"` — the upstream version number with a `-uk.N` suffix
  - `upstream-version: "X.Y.Z"` — the upstream version this fork was synced against
  - `upstream-repo: https://github.com/blader/humanizer`
  - `upstream-source: https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md`
- Do **not** re-add `allowed-tools` or `compatibility`. Upstream dropped them for cross-agent portability; the self-update's `WebFetch`/`Bash` are available by default in Claude Code, so no whitelist is needed.

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
| favor / favored / favoring / favorable | favour / favoured / favouring / favourable |
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
| other unlisted `-ize`/`-ization` verbs (recognize, specialize, prioritize, standardize, …) | `-ise`/`-isation` (recognise, specialise, prioritise, standardise, …) |

Do **not** change:
- `license: MIT` (a standard term)
- `program` (in software contexts; "programme" only for broadcast/event senses, which don't appear here)
- Straight-vs-curly quote example content (it's about typography, not dialect)
- Proper nouns, code identifiers, URLs, the word "behaviors" inside YAML keys if any appear

### C. Targeted phrase swaps

- In **Section 14 (Em and en dashes)**, change the replacement-preference phrase "a period, comma, colon, or parentheses" → "a full stop, comma, colon, or parentheses". Treat any other punctuation-sense "period(s)" in this section the same way ("full stop(s)").

### D. Example outlet swaps

In the **Name-dropping to prove importance** example (Section 2):
- "Before" block: `The New York Times` → `The Times`, and `The Hindu` → `The Guardian`.
- "After" block: replace any surviving US/Indian outlet with its Before-block UK counterpart (e.g. `The New York Times` → `The Times`), so the After stays consistent with the swapped Before.

If any other example (or a reintroduced Full Example) names a US/Indian outlet as the illustration's own voice, swap it to *The Guardian* / *The Times* too.

Leave other geographic/cultural examples (Catalonia, Texas temple, Ethiopia, Chennai, Somali cuisine, Gallery 825, Dutch Netherlands, Big Bang) **unchanged** — they are Wikipedia-style examples and altering them would distort the source material.

### E. Title change

- `# Humanizer: remove AI writing patterns` → `# Humaniser: remove AI writing patterns` (match upstream's current casing; earlier upstreams used Title Case, so adjust to whatever upstream currently ships).

### F. Preserve this self-update section

The "Step 0: Update Check" section and the "UK Customisation Manifest" itself are local additions and must be retained on every update.

### G. Leave upstream's own em dashes alone

Upstream's explanatory prose may use an em dash in its own sentences. Section 14's "no em dashes" rule is guidance for *humanised output*, not for this skill file — keep upstream's own punctuation verbatim rather than rewriting it.

### H. Fork addition — extra §7 AI-vocabulary words

Unlike A–G (which only re-shape upstream), this is the fork's one deliberate **content** addition. After re-applying upstream's §7 "High-frequency AI words" line, append a separate **"Also (UK fork additions):"** line with these extra high-frequency AI words, each with its carve-out:

> seamless; harness (verb); streamline; empower; holistic; utilise/utilize (where "use" would do; keep the metric noun *utilisation*); robust (figurative; preserve technical uses such as robust statistics or robust error handling); navigate (figurative "navigating the complexities of…", not literal "navigate to the page"); unlock (figurative "unlock your potential/insights", not "unlock a feature/account"); elevate (figurative "elevate your brand/writing", not literal/medical "elevated").

These are proposed upstream in [blader/humanizer#241](https://github.com/blader/humanizer/issues/241) but not merged (the maintainer curates §7 one word at a time to avoid bloat). Keep them as a **separate, labelled line** so upstream's own list stays a clean diff. If upstream later merges any of these into §7, drop it from this fork line to avoid duplication.

---

## What to do

When given text to humanise:

1. **Find AI patterns.** Check the text against the patterns below.
2. **Keep every claim.** You may shorten dull parts, expand useful parts, and merge or split paragraphs. Keep the information even when you change the structure.
3. **Do not invent facts.** Do not add a fact, name, number, date, quote, or citation unless it comes from the source or the user. If a sentence needs a missing detail, ask for it or use a simpler sentence. You may add an opinion or reaction when the writer's voice calls for one, but you may not add a factual claim. Fiction is exempt because invented details are part of the task.
4. **Match the voice.** Use the right tone for the text, such as formal, casual, or technical. Add personality only when the text and the writer call for it.

The input type controls what you return. See [How to return the result](#how-to-return-the-result). Use the same rewrite process in every mode.

## Match the writer's voice

If the user provides a writing sample (their own previous writing), analyse it before rewriting:

1. Read the sample first. Note its sentence length, word choice, paragraph openings, punctuation, repeated phrases, and transitions.
2. Match those habits. Do not replace casual words with formal ones or remove deliberate quirks.
3. If there is no sample, use the guidance below.

A writing sample takes priority over these style rules. If the sample uses em dashes, keep them at about the same rate. Do not apply §14 as a ban.

## Add personality only when it fits

Removing AI patterns is only half the job. The result should still sound like a person.

Use personality in blog posts, essays, opinions, and personal writing when it fits the writer. Keep reference, technical, legal, and factual text neutral. Do not add opinions or first-person language where they do not belong.

When personality fits, keep the writer's opinions, uncertainty, mixed feelings, humour, asides, and uneven rhythm. Never invent facts to make the text feel personal.

## Content patterns

### 1. Inflated claims about importance and legacy

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolising its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted
**Problem:** AI writing often claims that ordinary details mark a major change, prove a legacy, or reflect a broad trend.
**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralise administrative functions and enhance regional governance.
**After:**
> The Statistical Institute of Catalonia was established in 1989, part of a wider decentralisation of administrative functions in Spain.

### 2. Name-dropping to prove importance

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence
**Problem:** AI writing often lists well-known publications or follower counts to prove that a person matters. The list usually gives no useful context.
**Before:**
> Her views have been cited in The Times, BBC, Financial Times, and The Guardian. She maintains an active social media presence with over 500,000 followers.
**After:**
> Her views have been cited in The Times and the BBC.

If the source explains what the person said and where, keep that useful citation. Do not invent context for a shorter version.

### 3. Shallow analysis with -ing phrases

**Words to watch:** highlighting/underscoring/emphasising..., ensuring..., reflecting/symbolising..., contributing to..., cultivating/fostering..., encompassing..., showcasing...
**Problem:** AI writing often adds an -ing phrase to make a simple fact sound deeper than it is.
**Before:**
> The temple's colour palette of blue, green, and gold resonates with the region's natural beauty, symbolising Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.
**After:**
> The temple is painted blue, green, and gold, colours meant to evoke Texas bluebonnets and the Gulf of Mexico.

### 4. Sales language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning
**Problem:** AI writing often sounds like an advertisement, especially when it describes places, culture, products, or organisations.
**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.
**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia.

### 5. Vague sources

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)
**Problem:** AI writing often assigns a claim to unnamed experts, critics, reports, or observers.
**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.
**After:**
> Researchers and conservationists study the Haolai River for its unusual characteristics.

Name a real source when the source text provides one. Otherwise, remove the unsupported claim. Never invent a source.

### 6. Formulaic challenges and outlook sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook
**Problem:** AI articles often add a stock section about challenges, future prospects, or continued growth. These sections usually repeat vague claims instead of adding facts.
**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.
**After:**
> Korattur has recurring traffic congestion and water shortages.

Add details such as dates or public actions only when they come from the source or the user.

## Language and grammar patterns

### 7. Overused AI words

**High-frequency AI words:** Actually, additionally, align with, crucial, delve, emphasising, enduring, enhance, fostering, garner, gate/gated/gating (figurative; preserve established technical usage), highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, quietly, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant
**Also (UK fork additions):** seamless, harness (verb: "harness the power of…"), streamline, empower, holistic, utilise/utilize (where "use" would do; keep the metric noun *utilisation*), robust (figurative; preserve technical uses such as robust statistics or robust error handling), navigate (figurative: "navigating the complexities of…"; not literal "navigate to the page"), unlock (figurative: "unlock your potential/insights"; not "unlock a feature/account"), elevate (figurative: "elevate your brand/writing"; not literal/medical "elevated")
**Problem:** AI writing uses these words much more often than most people do, especially in groups.
**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.
**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonisation, remain common, especially in the south.

### 8. Avoiding is and are

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]
**Problem:** AI writing often replaces simple verbs such as *is*, *are*, and *has* with longer phrases.
**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.
**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totalling 3,000 square feet.

### 9. Not X but Y and clipped negative endings
**Problem:** AI writing overuses forms such as "Not only...but..." and "It's not just X, it's Y."

It also adds clipped endings such as "no guessing" instead of writing a clear clause.
**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.
**After:**
> The heavy beat adds to the aggressive tone.
**Before (tailing negation):**
> The options come from the selected item, no guessing.
**After:**
> The options come from the selected item without forcing the user to guess.

### 10. Forced groups of three
**Problem:** AI writing often forces ideas into groups of three to sound complete.
**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.
**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.

### 11. Changing names and repeating sentence openings
**Problem:** AI writing handles repetition by rule instead of by ear. It may keep renaming the same person or thing. It may also start several sentences with the same subject, often *she* or *he*.

Use one clear name for the same subject. For repeated openings, merge sentences, change the subject when that helps, or begin with the action.
**Before (synonym cycling):**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.
**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.
**Before (repeated openings):**
> She noted the door. She noted the lock on it. She filed both away.
**After:**
> She noted the door and its lock, then filed both away.

Do not ban the repeated word. Fix the repeated sentence pattern. The remaining sentence may still start with "She."

### 12. False from X to Y ranges
**Problem:** AI writing often uses "from X to Y" when X and Y do not form a real range.
**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.
**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

### 13. Passive voice and missing subjects
**Problem:** AI writing often hides who acts or drops the subject. Use active voice when it makes the actor and action clearer.
**Before:**
> No configuration file needed. The results are preserved automatically.
**After:**
> You do not need a configuration file. The system preserves the results automatically.

## Style patterns

### 14. Em and en dashes

**Rule:** The final rewrite must not contain em dashes (—) or en dashes (–), unless the writer's sample uses them. Replace a dash with a full stop, comma, colon, or parentheses, or rewrite the sentence. Also check for spaced dashes (` — `) and double hyphens (` -- `) used as dashes.
**Before:**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabelling continues—even in official documents.
**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabelling continues in official documents.
**Before:**
> The new policy — announced without warning — affects thousands of workers. The changes -- long overdue according to critics -- will take effect immediately.
**After:**
> The new policy, announced without warning, affects thousands of workers. The changes, long overdue according to critics, will take effect immediately.

Before returning the rewrite, search for `—` and `–`. Remove each one unless the writer's sample uses that mark. In that case, match the sample's rate.

### 15. Too much bold text
**Problem:** AI chatbots often bold words and phrases without a clear reason.
**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.
**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

### 16. Lists with bold mini-headings
**Problem:** AI writing often uses vertical lists in which every item starts with a bold label and a colon.
**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimised algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.
**After:**
> The update improves the interface, speeds up load times through optimised algorithms, and adds end-to-end encryption.

### 17. Title case in headings
**Problem:** AI chatbots often capitalise every main word in a heading.
**Before:**
> ## Strategic Negotiations And Global Partnerships
**After:**
> ## Strategic negotiations and global partnerships

### 18. Emojis
**Problem:** AI chatbots often add emojis to headings and list items as decoration.
**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting
**After:**
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

### 19. Curly quotation marks
**Problem:** ChatGPT often uses curly quotes (“...”) where the writer or target format uses straight quotes ("...").
**Before:**
> He said “the project is on track” but others disagreed.
**After:**
> He said "the project is on track" but others disagreed.

## Chatbot patterns

### 20. Chatbot text left in the answer

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., Want me to...?, Want me to give examples?, Should I continue?, let me know, here is a...
**Problem:** A chatbot's greeting, offer, or closing sometimes remains in text that should stand on its own.
**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.
**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

### 21. Knowledge-limit disclaimers and guesses

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information, not publicly available, maintains a low profile, keeps personal details private, prefers to stay out of the spotlight, likely [grew up/studied/began], it is believed that
**Problem:** Older models may mention the date when their knowledge ends. A model may also explain that it could not find a source, then fill the gap with a plausible guess. State what the source does not show, or remove the sentence. Do not present a guess as a fact.
**Before (cutoff disclaimer):**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.
**After:**
> The company's founding date is not documented in the available sources. (Or cut the sentence. State a date only if a source provides one.)
**Before (speculative gap-fill):**
> Information about her early life is not publicly available, suggesting she maintains a low profile and keeps personal details private. She likely grew up in a middle-class household, which shaped her later interest in education reform.
**After:**
> Her early life is not documented in the available sources. (Or omit the section.)

### 22. Overly agreeable tone
**Problem:** AI assistants often praise the user or agree before giving the answer.
**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.
**After:**
> The economic factors you mentioned are relevant here.

## Filler and hedging

### 23. Filler phrases

**Before → After:**
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"

### 24. Too many qualifiers

**Phrases to watch:** to be fair, it's also possible, could potentially, might arguably, in some cases it may, this is an inference
**Problem:** Repeated editing can add one qualifier after another until every claim sounds uncertain. Keep a qualifier only when the source supports it and the meaning needs it. Remove caveats that only repair an earlier overstatement.
**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.
**After:**
> The policy may affect outcomes.

### 25. Generic positive endings
**Problem:** AI writing often ends with vague optimism instead of the last useful fact.
**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey towards excellence. This represents a major step in the right direction.
**After:**
> (Cut the paragraph. End on the last concrete fact instead of a send-off. If the source states real plans, use those.)

### 26. Too many hyphenated word pairs

**Words to watch:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end
**Problem:** AI writing often hyphenates these pairs everywhere. Keep the hyphen before a noun when grammar needs it, as in `a high-quality report`. Drop it after the noun, as in `the report is high quality`.
**Before:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross-functional, the report is high-quality, and the methodology is data-driven.
**After:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross functional, the report is high quality, and the methodology is data driven.

### 27. Pretending to reveal a deeper truth

**Phrases to watch:** The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter
**Problem:** AI writing uses these phrases to make an ordinary point sound like a hidden truth.
**Before:**
> The real question is whether teams can adapt. At its core, what really matters is organisational readiness.
**After:**
> The question is whether teams can adapt. That mostly depends on whether the organisation is ready to change its habits.

### 28. Announcing the next point

**Phrases to watch:** Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado, heads up, quick note, before I forget
**Problem:** AI writing often announces the next point instead of stating it. A casual phrase such as "one thing that bit me" can have the same problem. Remove the announcement, not just its formal tone.
**Before:**
> Let's dive into how caching works in Next.js. Here's what you need to know.
**After:**
> Next.js caches data at multiple layers, including request memoisation, the data cache, and the router cache.
**Before (casual register):**
> One thing that bit me hard, so pay attention to this part: the webpack dev server doesn't send the CORS header by default.
**After:**
> The webpack dev server doesn't send the CORS header by default.

### 29. A heading repeated in the first sentence

**Signs to watch:** A heading followed by a one-line paragraph that simply restates the heading before the real content begins.
**Problem:** AI writing often follows a heading with a sentence that only repeats the heading. Remove the repeated sentence.
**Before:**
> ## Performance
>
> Speed matters.
>
> When users hit a slow page, they leave.
**After:**
> ## Performance
>
> When users hit a slow page, they leave.

### 30. Writing about the previous version
**Problem:** Documentation and comments should describe the current behaviour. Mention the previous version only in change logs, release notes, migration guides, and other documents about change.
**Before:**
> This function was added to replace the previous approach of iterating through all items, which caused O(n²) performance.
**After:**
> This function uses a hash map for O(1) lookups, avoiding the O(n²) cost of naive iteration.

### 31. Forced punchlines and dramatic fragments
**Problem:** AI writing often turns each sentence into a dramatic closing line. One short sentence can add emphasis. A row of short fragments usually feels forced.
**Before:**
> Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.
**After:**
> AlphaEvolve changed the search because it did not favour symmetry or human-looking designs. That made some of the older assumptions less useful.

### 32. Formulaic sayings

**Words to watch:** X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of
**Problem:** AI writing often turns an ordinary claim into a saying that sounds deep but adds no detail. Replace the saying with the specific claim.
**Before:**
> Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.
**After:**
> Symmetric layouts often feel more predictable to users. Teams can over-optimise workflows and miss how people actually use them.

### 33. Fake-candid openings

**Phrases to watch:** Honestly?, Look, Here's the thing, The thing is, Let's be honest, Real talk, when used as standalone hooks or fake-candid pauses before an ordinary point.
**Problem:** AI writing often starts with a staged pause or claim of honesty before making a routine point. State the point directly.
**Before:**
> Is it worth the price? Honestly? It depends on how often you'll use it.
**After:**
> Whether it's worth the price depends on how often you'll use it.

### 34. Answering objections no one raised

**Phrases to watch:** This isn't (mainly/really) about, I'm not saying/arguing/trying to, To be clear, Don't get me wrong, This is not to say, You could argue/frame this differently but, Some might say... but
**Problem:** AI writing may answer an objection that does not appear in the text. Watch for an unattributed statement about what the writer does not mean, especially when the topic appears nowhere else. A direct claim such as "the API is not thread-safe" is not this pattern.
**Before:**
> This isn't mainly about prompt length, and I'm not arguing that documentation doesn't matter. You could categorise the problem another way, but the issue is whether the agent can use the instruction when it acts.
**After:**
> The issue is whether the agent can use the instruction when it acts.

Remove only the unsupported defence. If it contains a real claim, state that claim directly. Keep an objection when the text names its source or answers it in full.

### 35. Rejecting fake alternatives

**Phrases to watch:** A tempting option/approach would be, One might be tempted to, An obvious approach would be, You might think... but, It would be easy to just, Some would suggest
**Problem:** AI writing may introduce an option that no reader would consider, reject it in a clause, and never mention it again. This often leaves an old drafting idea in the final text. Remove the fake option and state the real constraint directly.
**Before:**
> Session tokens are rotated every 24 hours. A tempting approach would be to rotate them by restarting the auth service on a cron job, but that would drop every active session. Rotation happens in place, and clients refresh transparently.
**After:**
> Session tokens are rotated every 24 hours, in place, and clients refresh transparently.

One rejected option may be valid. Several short, unrelated rejections are a stronger sign. Ask what new information each sentence adds. If it only records an earlier edit, rewrite the paragraph around its main point.

## Check for false positives

### What not to flag

A person may use some of these patterns. Do not treat any item below as proof by itself:

- **Perfect grammar and consistent style.** Many writers are professionals or have been edited. Polish does not equal AI.
- **Mixed casual and formal styles.** This can reflect the writer's field, age, or personal habits.
- **"Bland" or "robotic" prose.** AI prose has *specific* tells. Generic dryness without those tells is just dry writing.
- **Formal or academic words.** §7 lists specific words that AI writing overuses. Do not simplify every formal word.
- **Letter-style opening or closing on a comment.** Salutations and sign-offs predate ChatGPT by centuries.
- **Common transition words in isolation.** *Additionally*, *moreover*, *consequently* are AI-coded only when piled up. One *however* is not a tell.
- **Curly quotes alone.** macOS, Word, Google Docs, and most CMSes auto-curl by default. Curly quotes only count when stacked with other tells.
- **Em dashes alone.** Many editors and journalists use them often. Em dashes are evidence only when paired with formulaic sales-y rhythm.
- **One short sentence for emphasis.** Flag dramatic fragments only when several appear in a row.
- **Deliberate repeated openings.** Writers may repeat an opening to build rhythm or pressure, as in "She came. She saw. She conquered." Change it only when the repetition adds nothing.
- **"Honestly" or "look" mid-sentence.** These are ordinary in casual writing. The tell is the standalone theatrical opener, not the word itself.
- **Useful limits and disclaimers.** Keep scope statements, legal and safety notices, real corrections, named objections, replies, and FAQ answers.
- **Real alternatives.** Keep options that a reader may consider in a design document, tutorial, or argument. Remove only an unlikely option that the text dismisses and never uses again.
- **Unsourced claims.** Most of the web is unsourced. Lack of citations doesn't prove anything.
- **Correct, complex formatting.** Visual editors and templates produce clean output without any AI.
- **Secondhand text.** Do not rewrite watched phrases inside quotations, titles, proper names, or examples where the phrase is being discussed rather than used.

When unsure, look for several patterns together. One em dash proves nothing. Several stock patterns in the same passage are stronger evidence.

### Human details to keep

These details often carry the writer's voice. Keep them unless they hurt the meaning:

- **Specific, unusual details.** Keep a real address, an odd quote, or a phrase such as "the lawyer who used to work upstairs from my dentist."
- **Mixed feelings and unresolved tension.** Keep lines such as "I think this is mostly good, but it bothers me, and I can't fully explain why."
- **Dated, era-bound references.** Slang, memes, or in-jokes that map to a specific year and subculture. Models lag by a year or more.
- **Deliberate first-person choices.** Keep a cut or word choice when the writer can explain why it belongs.
- **Variety in sentence length.** Real writing alternates short and long. AI writing tends towards an even, mid-length cadence.
- **Genuine asides, parentheticals, or self-corrections.** "(I keep wanting to say 'almost' here, but it really was certain.)" Models rarely interrupt themselves like this.
- **Edits made before November 30, 2022.** ChatGPT's public launch. Anything older than that is, with very rare exceptions, not AI-written.

---

## How to return the result

**Pasted text (default).** Return the draft, a short list of remaining AI patterns, and the final rewrite.

**File mode.** When the user names a file, run the full rewrite process but write only the final text to the file. Change prose only. Keep code blocks, YAML metadata, data, and link targets unchanged. Then give the user a short summary.

**Embedded mode.** When another task uses this skill for a pull request, commit message, or document, return only the final text.

## Rewrite process

1. Read the source and mark each AI pattern.
2. Write a draft. Read it aloud. Check the rhythm, details, simple verbs such as *is* and *has*, and the right level of formality.
3. Ask two questions:
   - **"What still sounds AI-generated?"**
   - **"Did the rewrite add or remove any fact, name, number, date, quote, citation, ranking, or other claim?"**
   Treat any unsupported addition or lost claim as an error.
4. Write the final version. State each point naturally instead of patching one flagged phrase at a time. If a sentence stays awkward, rewrite the paragraph around its main point. Apply the dash rule in §14.

Return the result required by [How to return the result](#how-to-return-the-result).

## Source

This skill is based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. Its patterns come from reviews of AI-generated text on Wikipedia.

Wikipedia's main point: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."
