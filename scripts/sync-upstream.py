#!/usr/bin/env python3
"""Rebuild the fork's SKILL.md from upstream by applying the UK manifest.

    python3 scripts/sync-upstream.py            # fetch upstream, rewrite SKILL.md
    python3 scripts/sync-upstream.py --check    # verify SKILL.md == rebuilt upstream

The manifest in AGENTS.md is the specification; this script is its
mechanical form. Change the two together. The script takes the fork-only
text (Step 0 and the extra AI-words line) from the current SKILL.md, so
edit those there.

After a sync it prints what is left for a person or an assistant to do.
Uses only the standard library.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = "https://github.com/blader/humanizer"
UPSTREAM_SOURCE = "https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md"
UK_DESCRIPTION = ("  UK English variant: British spellings, one example adapted, "
                  "and a few extra AI-vocabulary words; otherwise tracks upstream.\n")

# Manifest B. Lower-case stems, so "Organiz" and "organiz" both convert.
SPELLINGS = [
    (r"umaniz", "umanis"), (r"nalyz", "nalys"), (r"mphasiz", "mphasis"),
    (r"ymboliz", "ymbolis"), (r"ecentraliz", "ecentralis"),
    (r"ategoriz", "ategoris"), (r"egulariz", "egularis"), (r"rganiz", "rganis"),
    (r"\b([Rr])ealiz", r"\1ealis"), (r"ptimiz", "ptimis"),
    (r"apitaliz", "apitalis"), (r"emoiz", "emois"), (r"oloniz", "olonis"),
    (r"ecogniz", "ecognis"), (r"pecializ", "pecialis"),
    (r"rioritiz", "rioritis"), (r"tandardiz", "tandardis"),
    (r"\b([Cc])olor", r"\1olour"), (r"\b([Bb])ehavior", r"\1ehaviour"),
    (r"\b([Hh])umor\b", r"\1umour"), (r"\b([Ff])avor", r"\1avour"),
    (r"\b([Jj])udgment", r"\1udgement"),
    (r"\b([Aa])cknowledgment", r"\1cknowledgement"),
    (r"\b([Ss])keptic", r"\1ceptic"),
    (r"\b((?:[Mm]is)?[Ll])abel(ed|ing)\b", r"\1abell\2"),
    (r"\b([Tt])otal(ed|ing)\b", r"\1otall\2"),
    (r"\b([Tt])oward\b", r"\1owards"),
    (r"\b([Nn])eighbor", r"\1eighbour"),
    (r"\b([Tt])ravel(er|ers|ed|ing)\b", r"\1ravell\2"),
    (r"\b([Ss])avor", r"\1avour"), (r"\b([Cc])andor\b", r"\1andour"),
    (r"\b([Dd])efense\b", r"\1efence"),
    (r"\b(centi|milli|kilo)meter", r"\1metre"),
]

# Manifest C and D. Each must match upstream at least once, or the script
# reports it: upstream reworded the passage and the manifest needs a look.
PHRASES = [
    ("C: dashes rule, 'period' -> 'full stop'",
     r"with a period, comma", "with a full stop, comma"),
    ("C: one-line closers, 'periods' -> 'full stops'",
     r"with periods between words", "with full stops between words"),
    ("D: prestige list, Before block outlets",
     r"The New York Times, BBC, Financial Times, and The Hindu",
     "The Times, BBC, Financial Times, and The Guardian"),
]
# Applied wherever they still appear after the swaps above.
OUTLETS = [(r"\b(?:The )?New York Times\b", "Times"), (r"\bThe Hindu\b", "The Guardian")]

MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")
US_DATE = re.compile(rf"\b({MONTHS}) (\d{{1,2}}), (\d{{4}})\b")

# Code, link targets and URLs keep their spelling.
PROTECTED = re.compile(r"(```.*?```|`[^`\n]*`|\]\([^)]*\)|https?://\S+)", re.S)

problems = []


def die(message):
    sys.exit(f"sync-upstream: {message}")


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True)


def split_frontmatter(text, label):
    parts = text.split("---\n", 2)
    if len(parts) < 3 or parts[0] != "":
        die(f"{label} has no YAML frontmatter")
    return parts[1], parts[2]


def value(frontmatter, key):
    match = re.search(rf'^\s*{re.escape(key)}:\s*"?([^"\n]+)"?\s*$', frontmatter, re.M)
    return match.group(1).strip() if match else None


def outside_code(text, function):
    pieces = PROTECTED.split(text)
    return "".join(piece if index % 2 else function(piece)
                   for index, piece in enumerate(pieces))


def convert_prose(text):
    for pattern, replacement in SPELLINGS:
        text = re.sub(pattern, replacement, text)
    for label, pattern, replacement in PHRASES:
        text = re.sub(pattern, replacement, text)
    for pattern, replacement in OUTLETS:
        text = re.sub(pattern, replacement, text)
    return US_DATE.sub(r"\2 \1 \3", text)


def build(upstream, fork, uk_revision):
    up_front, up_body = split_frontmatter(upstream, "upstream SKILL.md")
    fork_front, fork_body = split_frontmatter(fork, "fork SKILL.md")
    upstream_version = value(up_front, "version")
    if not upstream_version:
        die("upstream frontmatter has no metadata.version")

    # A. Frontmatter
    front = up_front
    for old, new, what in [
        (r"^name: humanizer$", "name: humaniser", "name: humanizer"),
        (r"^(license:)", UK_DESCRIPTION + r"\1", "license: (to place the UK sentence)"),
        (r'^(\s*)version:.*$',
         rf'\g<1>version: "{upstream_version}-uk.{uk_revision}"\n'
         rf'\g<1>upstream-version: "{upstream_version}"\n'
         rf'\g<1>upstream-repo: {UPSTREAM_REPO}\n'
         rf'\g<1>upstream-source: {UPSTREAM_SOURCE}', "metadata.version"),
    ]:
        front, count = re.subn(old, new, front, count=1, flags=re.M)
        if not count:
            problems.append(f"A: upstream frontmatter has no '{what}' line")
    for banned in ("allowed-tools", "compatibility"):
        if re.search(rf"^{banned}:", front, re.M):
            problems.append(f"A: upstream frontmatter has {banned}; the manifest says to drop it")

    # B, C, D and the date rule
    for label, pattern, _ in PHRASES:
        if not re.search(pattern, up_body):
            problems.append(f"{label}: phrase not found in upstream; review the manifest")
    body = outside_code(up_body, convert_prose)

    # E. Title
    if not body.lstrip().startswith("# Humaniser:"):
        problems.append("E: title does not start with '# Humaniser:'")

    # H. Extra AI-vocabulary line, taken from the current fork
    words_line = re.search(r"^\*\*Also \(UK fork additions\):\*\*.*$", fork_body, re.M)
    watch = re.search(r"(^### \d+\. Overused AI words\n\n\*\*Watch for:\*\*([^\n]*)\n)", body, re.M)
    if not words_line:
        problems.append("H: current SKILL.md has no 'Also (UK fork additions):' line to carry over")
    elif not watch:
        problems.append("H: upstream has no 'Overused AI words' watch list to append to")
    else:
        body = body.replace(watch.group(1), watch.group(1) + "\n" + words_line.group(0) + "\n", 1)
        upstream_words = {w.strip().split(" ")[0].split("/")[0].lower()
                          for w in watch.group(2).split(",")}
        fork_words = {w.strip().split(" ")[0].split("/")[0].lower()
                      for w in words_line.group(0).split(":**", 1)[1].split(",")}
        for word in sorted(upstream_words & fork_words):
            problems.append(f"H: upstream now lists '{word}'; drop it from the fork line")

    # F. Step 0, taken from the current fork, before the first section
    step0 = re.search(r"^## Step 0: Update check\n.*?(?=^## )", fork_body, re.M | re.S)
    first_section = re.search(r"^## ", body, re.M)
    if not step0:
        problems.append("F: current SKILL.md has no 'Step 0: Update check' section to carry over")
    elif not first_section:
        problems.append("F: upstream has no '## ' section to place Step 0 before")
    else:
        body = body[:first_section.start()] + step0.group(0) + body[first_section.start():]

    return f"---\n{front}---\n{body}", upstream_version


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true",
                        help="compare the rebuild with SKILL.md and change nothing")
    parser.add_argument("--no-fetch", action="store_true", help="do not run git fetch upstream")
    parser.add_argument("--ref", default="upstream/main", help="upstream git ref to build from")
    parser.add_argument("--upstream-file", help="read upstream SKILL.md from this file instead of git")
    parser.add_argument("--output", help="write the result here instead of SKILL.md (and leave plugin.json alone)")
    args = parser.parse_args()

    if args.upstream_file:
        upstream = Path(args.upstream_file).read_text(encoding="utf-8")
    else:
        if not (args.no_fetch or args.check):
            fetched = git("fetch", "upstream")
            if fetched.returncode:
                die(f"git fetch upstream failed: {fetched.stderr.strip()}")
        shown = git("show", f"{args.ref}:SKILL.md")
        if shown.returncode:
            die(f"cannot read {args.ref}:SKILL.md (run: git fetch upstream)")
        upstream = shown.stdout

    skill_path = ROOT / "SKILL.md"
    fork = skill_path.read_text(encoding="utf-8")
    fork_front, _ = split_frontmatter(fork, "fork SKILL.md")
    current_version = value(fork_front, "version") or ""
    tracked = value(fork_front, "upstream-version")
    latest = value(split_frontmatter(upstream, "upstream SKILL.md")[0], "version")
    same_upstream = latest == tracked
    current_revision = int((re.search(r"-uk\.(\d+)$", current_version) or [0, 1])[1])
    built, upstream_version = build(upstream, fork, current_revision if same_upstream else 1)

    if args.check:
        if not same_upstream:
            die(f"upstream is at {latest}, fork tracks {tracked}; sync first")
        for problem in problems:
            print(f"FAIL: {problem}")
        if built != fork:
            import difflib
            diff = list(difflib.unified_diff(built.splitlines(), fork.splitlines(),
                                             "upstream + manifest", "SKILL.md", lineterm="", n=0))
            print("FAIL: SKILL.md is not upstream plus the manifest:")
            print("\n".join(line[:160] for line in diff[:60]))
        if problems or built != fork:
            sys.exit(1)
        print(f"OK: SKILL.md is exactly upstream {upstream_version} plus the manifest.")
        return

    target = Path(args.output) if args.output else skill_path
    target.write_text(built, encoding="utf-8")
    new_version = value(split_frontmatter(built, "result")[0], "version")
    if not args.output:
        plugin_path = ROOT / ".claude-plugin" / "plugin.json"
        plugin = plugin_path.read_text(encoding="utf-8")
        old = json.loads(plugin)["version"]
        plugin_path.write_text(plugin.replace(f'"version": "{old}"', f'"version": "{new_version}"', 1),
                               encoding="utf-8")

    print(f"Wrote {target} as {new_version} (upstream {tracked} -> {upstream_version}).")
    for problem in problems:
        print(f"REVIEW: {problem}")
    if same_upstream:
        print("Upstream has not moved; this was a rebuild of the same version.")
    else:
        print("Still to do by hand (see AGENTS.md):\n"
              "  1. Read the diff: git diff SKILL.md\n"
              "  2. Update README.md: version line, history entry, pattern table, full example\n"
              "  3. python3 scripts/check-fork.py\n"
              "  4. Commit, push, refresh installed copies")
    if problems:
        sys.exit(2)


if __name__ == "__main__":
    main()
