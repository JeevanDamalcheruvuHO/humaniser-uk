#!/usr/bin/env python3
"""Check the UK fork after a sync or an edit.

Run from anywhere:  python3 scripts/check-fork.py [--require-current] [repo-root]

--require-current also fails when upstream has released a version the fork
does not track yet. The weekly "Upstream watch" workflow uses it.

Exits 1 if any check fails. Uses only the standard library. When the
`upstream` git remote has been fetched, it also compares the fork with
upstream/main; without it those checks are skipped.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ARGS = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
REQUIRE_CURRENT = "--require-current" in sys.argv[1:]
ROOT = Path(ARGS[0] if ARGS else Path(__file__).resolve().parent.parent)

# How many words the fork-only text (the 'Also (UK fork additions)' lines, the
# description sentence) may add on top of upstream's SKILL.md.
FORK_WORD_ALLOWANCE = 200

# US spellings from manifest section B in AGENTS.md. Each is a regex.
US_SPELLINGS = [
    r"\w+izations?", r"\w+izational",   # -ization
    r"\w+iz(?:e|es|ed|ing|er|ers)",      # -ize verbs and "humanizer"
    r"\w+yz(?:e|es|ed|ing)",             # analyze
    r"colors?", r"colored", r"behaviors?", r"behavioral", r"humor",
    r"favor\w*", r"judgment", r"acknowledgment", r"skeptic\w*",
    r"(?:mis)?label(?:ed|ing)", r"totaling", r"toward",
    r"neighbor\w*", r"travel(?:er|ers|ing|ed)", r"savor\w*",
    r"candor", r"defense", r"(?:centi|milli|kilo)meters?",
]
# Words the patterns above match that are correct in British English, or
# that the fork keeps on purpose ("utilise/utilize" in the fork's word line).
ALLOWED = {
    "size", "sizes", "sized", "sizing", "resize", "resized", "prize", "prizes",
    "seize", "seized", "capsize", "citizen", "utilize",
}
# Text quoted from another source keeps its own spelling.
QUOTED = ["The result tends toward the most statistically likely result"]
US_OUTLETS = ["New York Times", "The Hindu"]
MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")
US_DATE = re.compile(rf"\b(?:{MONTHS}) \d{{1,2}}, \d{{4}}\b")

failures = []
notes = []


def fail(message):
    failures.append(message)


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def prose(text):
    """Drop the parts spelling rules do not apply to: code and link targets."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"https?://\S+", " ", text)
    for quote in QUOTED + ["blader/humanizer"]:
        text = text.replace(quote, " ")
    return text


def us_spellings(text):
    found = set()
    for pattern in US_SPELLINGS:
        for match in re.finditer(rf"\b(?:{pattern})\b", text, flags=re.I):
            word = match.group(0)
            if word.lower() not in ALLOWED:
                found.add(word)
    return sorted(found)


def frontmatter_value(frontmatter, key):
    match = re.search(rf'^\s*{re.escape(key)}:\s*"?([^"\n]+)"?\s*$', frontmatter, flags=re.M)
    return match.group(1).strip() if match else None


def pattern_headings(text):
    return re.findall(r"^### (\d+)\. (.+)$", text, flags=re.M)


def upstream_skill():
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "show", "upstream/main:SKILL.md"],
            capture_output=True, text=True, check=True,
        )
        return result.stdout
    except (OSError, subprocess.CalledProcessError):
        return None


skill = read("SKILL.md")
readme = read("README.md")

# --- Frontmatter and versions -------------------------------------------
parts = skill.split("---\n", 2)
if len(parts) < 3 or parts[0] != "":
    fail("SKILL.md: frontmatter is missing or not closed with ---")
    frontmatter, body = "", skill
else:
    frontmatter, body = parts[1], parts[2]

name = frontmatter_value(frontmatter, "name")
version = frontmatter_value(frontmatter, "version")
upstream_version = frontmatter_value(frontmatter, "upstream-version")

if name != "humaniser":
    fail(f"SKILL.md: name is {name!r}, expected 'humaniser'")
if "UK English variant" not in frontmatter:
    fail("SKILL.md: description lacks the 'UK English variant' sentence")
for banned in ("allowed-tools", "compatibility"):
    if re.search(rf"^{banned}:", frontmatter, flags=re.M):
        fail(f"SKILL.md: frontmatter must not contain {banned}")
for key in ("upstream-repo", "upstream-source"):
    if not frontmatter_value(frontmatter, key):
        fail(f"SKILL.md: metadata.{key} is missing")

version_match = re.fullmatch(r"(\d+\.\d+\.\d+)-uk\.(\d+)", version or "")
if not version_match:
    fail(f"SKILL.md: metadata.version is {version!r}, expected X.Y.Z-uk.N")
elif version_match.group(1) != upstream_version:
    fail(f"SKILL.md: version {version} does not match upstream-version {upstream_version}")

try:
    plugin_version = json.loads(read(".claude-plugin/plugin.json")).get("version")
    json.loads(read(".claude-plugin/marketplace.json"))
except (OSError, ValueError) as error:
    plugin_version = None
    fail(f".claude-plugin: {error}")
if plugin_version != version:
    fail(f"plugin.json version is {plugin_version!r}, SKILL.md has {version!r}")

# --- Manifests for other agents ------------------------------------------
try:
    cursor = json.loads(read(".cursor-plugin/plugin.json"))
    if cursor.get("version") != version:
        fail(f".cursor-plugin/plugin.json version is {cursor.get('version')!r}, SKILL.md has {version!r}")
    if cursor.get("name") != "humaniser":
        fail(".cursor-plugin/plugin.json: name must be 'humaniser'")
    if "skills" in cursor:
        fail(".cursor-plugin/plugin.json: omit 'skills' so Cursor loads the root SKILL.md")
    package = json.loads(read("package.json"))
    if package.get("pi", {}).get("skills") != ["./"]:
        fail("package.json: pi.skills must be ['./'] so pi loads the root SKILL.md")
    if "version" in package:
        fail("package.json: do not add a version; pi installs from git")
    if "$humaniser" not in read("agents/openai.yaml"):
        fail("agents/openai.yaml: default_prompt must call $humaniser")
    for label, text in ((".cursor-plugin/plugin.json", json.dumps(cursor)),
                        ("package.json", json.dumps(package)),
                        ("agents/openai.yaml", read("agents/openai.yaml"))):
        if re.search(r"humanizer", text.replace("fork of humanizer", "")):
            fail(f"{label}: says 'humanizer' where it should say 'humaniser'")
except (OSError, ValueError) as error:
    fail(f"other-agent manifests: {error}")

if version and f"Current version: **`{version}`**" not in readme:
    fail(f"README.md: 'Current version' line does not say {version}")
if version and f"- **`{version}`**" not in readme:
    fail(f"README.md: version history has no entry for {version}")

# --- Fork-only content ----------------------------------------------------
if re.search(r"^## Step 0", body, flags=re.M) or "raw.githubusercontent.com" in body:
    fail("SKILL.md: the skill must not fetch anything; the weekly Upstream watch "
         "workflow checks for new upstream releases instead")
if "**Also (UK fork additions):**" not in body:
    fail("SKILL.md: the 'Also (UK fork additions):' word line is missing")
if "UK Customisation Manifest" in body:
    fail("SKILL.md: the manifest belongs in AGENTS.md, not in the skill")
if not body.lstrip().startswith("# Humaniser:"):
    fail("SKILL.md: title must start with '# Humaniser:'")

# --- Spellings, dates, outlets -------------------------------------------
for label, text in (("SKILL.md", body), ("README.md", readme)):
    words = us_spellings(prose(text))
    if words:
        fail(f"{label}: US spellings: {', '.join(words)}")
    dates = US_DATE.findall(prose(text))
    if dates:
        fail(f"{label}: month-first dates: {', '.join(dates)}")

for outlet in US_OUTLETS:
    if outlet in body:
        fail(f"SKILL.md: US/Indian outlet left in an example: {outlet}")
for phrase in ("with a period,", "periods between words"):
    if phrase in body:
        fail(f"SKILL.md: punctuation 'period' should be 'full stop': {phrase!r}")

# --- Patterns -------------------------------------------------------------
headings = pattern_headings(body)
numbers = [int(number) for number, _ in headings]
if numbers != list(range(1, len(numbers) + 1)):
    fail("SKILL.md: patterns are not numbered from 1 without gaps")
for reference in set(re.findall(r"§(\d+)", body)):
    if int(reference) > len(numbers):
        fail(f"SKILL.md: §{reference} points past the last pattern ({len(numbers)})")

readme_names = dict(re.findall(r"^\| (\d+) \| \*\*(.+?)\*\*", readme, flags=re.M))
for number, title in headings:
    if readme_names.get(number) != title:
        fail(f"README.md: pattern {number} is {readme_names.get(number)!r}, SKILL.md has {title!r}")
if len(readme_names) != len(headings):
    fail(f"README.md: table lists {len(readme_names)} patterns, SKILL.md has {len(headings)}")
for count in re.findall(r"\b(\d+) patterns\b", readme.split("## Version history")[0]):
    if int(count) != len(headings):
        fail(f"README.md: says '{count} patterns', SKILL.md has {len(headings)}")

# --- Against upstream, when it has been fetched ---------------------------
words = len(skill.split())
upstream = upstream_skill()
if upstream is None:
    missing = ("upstream/main not available; skipped the upstream comparison "
               "(run: git fetch upstream)")
    (fail if REQUIRE_CURRENT else notes.append)(missing)
else:
    upstream_frontmatter = upstream.split("---\n", 2)[1]
    latest = frontmatter_value(upstream_frontmatter, "version")
    if latest != upstream_version:
        behind = (f"upstream is at {latest}; this fork tracks {upstream_version}. "
                  "Sync it by following AGENTS.md.")
        (fail if REQUIRE_CURRENT else notes.append)(behind)
    else:
        upstream_headings = pattern_headings(upstream)
        if len(upstream_headings) != len(headings):
            fail(f"SKILL.md has {len(headings)} patterns, upstream has {len(upstream_headings)}")
        sync = ROOT / "scripts" / "sync-upstream.py"
        if sync.exists():
            rebuilt = subprocess.run([sys.executable, str(sync), "--check"],
                                     capture_output=True, text=True)
            if rebuilt.returncode:
                fail("SKILL.md is not upstream plus the manifest "
                     "(run: python3 scripts/sync-upstream.py --check)")
        limit = len(upstream.split()) + FORK_WORD_ALLOWANCE
        if words > limit:
            fail(f"SKILL.md is {words} words; upstream is {len(upstream.split())} "
                 f"and the fork may add {FORK_WORD_ALLOWANCE}")

# --- Report ---------------------------------------------------------------
for note in notes:
    print(f"note: {note}")
if failures:
    for message in failures:
        print(f"FAIL: {message}")
    print(f"\n{len(failures)} check(s) failed.")
    sys.exit(1)
print(f"OK: humaniser {version}, {len(headings)} patterns, SKILL.md {words} words.")
