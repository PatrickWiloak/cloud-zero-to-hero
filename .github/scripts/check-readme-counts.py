#!/usr/bin/env python3
"""Verify the counts advertised in README.md against the actual tree.

Why this exists: on 2026-08-14 the README claimed "37 concept pages" when there
were 46, and "8 cross-pillar topic indexes" when there were 13. TODO.md had
recorded the jump to 46 five days earlier - the number was known and the README
was simply never updated. The same pass copied "~2.6M words" out of
docs/improvement-roadmap.md, which is an explicitly dated 2026-07-28 snapshot,
into the README, CHANGELOG and TODO as a current fact. It had since grown to
3.0M - a smaller error than the concept-page one, but the same failure: a number
nothing recomputed, restated as if it were current.

Cert and provider counts were already safe, because build-certs-index.py
regenerates them from docs/certs.json and CI runs it with --check. Everything
else in the README was hand-maintained, so this closes that gap the same way.

    python3 .github/scripts/check-readme-counts.py           # report drift
    python3 .github/scripts/check-readme-counts.py --check    # exit 1 on drift
    python3 .github/scripts/check-readme-counts.py --fix      # rewrite README

Add a claim here whenever you add a counted claim to the README. A number no
script checks is a number that will be wrong within a month.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
README = REPO / "README.md"
LEARN_README = REPO / "learn" / "README.md"

# The word count moves with every content edit, so an exact match would fail CI
# constantly. Wide enough to absorb ordinary editing, tight enough that a figure
# left to rot across a release cycle trips it.
WORD_TOLERANCE_MILLIONS = 0.2


def md_files():
    """Every markdown file that is actually part of the repo.

    Deliberately `git ls-files` and not a filesystem walk. A local site build
    leaves a complete staged copy of the tree in .site-src/ (2,034 files), and
    walking the working directory counts every page twice - which is exactly how
    this script's first version reported 6.1M words against a real 3.0M. Asking
    git means no build artifact, vendored directory, or future generated tree
    can ever inflate a count again.
    """
    out = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z", "*.md"],
        capture_output=True,
        check=True,
    )
    for name in out.stdout.decode("utf-8").split("\0"):
        if name:
            yield REPO / name


def count_pages(directory: str, *, exclude: set[str] = frozenset()) -> int:
    """Markdown pages directly inside a directory, minus its index and any
    generated companions."""
    base = REPO / directory
    skip = {"README.md", "index.md"} | set(exclude)
    return sum(1 for p in base.glob("*.md") if p.name not in skip)


def count_glob(pattern: str) -> int:
    return len(list(REPO.glob(pattern)))


def total_words() -> int:
    total = 0
    for path in md_files():
        try:
            total += len(path.read_text(encoding="utf-8", errors="ignore").split())
        except OSError:
            pass
    return total


def doc_links() -> int:
    """Bolded external links - the repo's documented citation format,
    `**[📖 Title](URL)** - description`."""
    pattern = re.compile(r"\*\*\[[^\]]*\]\(https?://[^)]*\)\*\*")
    total = 0
    for path in md_files():
        try:
            total += len(pattern.findall(path.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            pass
    return total


def gather() -> dict[str, int]:
    certs = json.loads((REPO / "docs" / "certs.json").read_text(encoding="utf-8"))
    totals = certs["totals"]

    return {
        "certifications": totals["certifications"],
        "providers": totals["certification_providers"],
        "study_tracks": totals["study_tracks"],
        "concept_pages": count_pages("learn/concepts"),
        "topic_indexes": count_pages("topics"),
        "service_comparisons": count_glob("resources/service-comparison-*.md"),
        "cli_cheat_sheets": count_glob("resources/cli-cheat-sheet-*.md"),
        "architecture_patterns": count_pages("resources/architecture-patterns"),
        "hands_on_projects": count_pages(
            "resources/hands-on-projects", exclude={"labs-by-cert.md"}
        ),
        "roadmaps": count_glob("resources/certification-roadmap-*.md"),
        "interview_prep": count_pages("resources/interview-prep"),
        "migration_guides": count_pages("resources/migration-guides"),
        "words": total_words(),
        "doc_links": doc_links(),
    }


# Each claim is (label, regex with ONE capturing group for the number, key).
# The regex must match the README exactly once.
CLAIMS: list[tuple[str, str, str]] = [
    ("certifications badge", r"badge/Certifications-(\d+)-blue", "certifications"),
    ("providers badge", r"badge/Providers-(\d+)-orange", "providers"),
    ("pillars table certs", r"\| (\d+) cert study guides across \d+ providers", "certifications"),
    ("pillars table providers", r"\| \d+ cert study guides across (\d+) providers", "providers"),
    ("concept pages", r"\*\*\[(\d+) concept pages\]", "concept_pages"),
    ("topic indexes", r"\*\*\[(\d+) cross-pillar topic indexes\]", "topic_indexes"),
    ("cert study guides", r"\*\*(\d+) certification study guides\*\*", "certifications"),
    # Unchecked until 2026-11-24, when it still said 16 providers against 18.
    ("cert study guides providers", r"\*\*\d+ certification study guides\*\* across (\d+) providers", "providers"),
    ("service comparisons", r"\*\*(\d+) cross-cloud service comparisons\*\*", "service_comparisons"),
    ("CLI cheat sheets", r"\*\*(\d+) CLI cheat sheets\*\*", "cli_cheat_sheets"),
    ("architecture patterns", r"\*\*(\d+) architecture patterns\*\*", "architecture_patterns"),
    ("hands-on projects", r"\*\*(\d+) hands-on projects\*\*", "hands_on_projects"),
    ("certification roadmaps", r"\*\*(\d+) certification roadmaps\*\*", "roadmaps"),
    ("interview prep guides", r"\*\*(\d+) interview prep guides\*\*", "interview_prep"),
    # The "Repository Statistics" block. Unchecked until 2026-08-14, by which
    # point it claimed 37 concept pages against 46 and 8 topic indexes against
    # 13 - the same drift the rest of this script exists to stop, in the one
    # section of the README that is nothing but counts.
    ("stats certifications", r"\*\*Certifications:\*\* (\d+)", "certifications"),
    ("stats providers", r"\*\*Providers:\*\* (\d+)", "providers"),
    ("stats concept pages", r"\*\*Concept pages:\*\* (\d+)", "concept_pages"),
    ("stats service comparisons", r"\*\*Service comparisons:\*\* (\d+)", "service_comparisons"),
    ("stats CLI cheat sheets", r"\*\*CLI cheat sheets:\*\* (\d+)", "cli_cheat_sheets"),
    ("stats architecture patterns", r"\*\*Architecture patterns:\*\* (\d+)", "architecture_patterns"),
    ("stats hands-on projects", r"\*\*Hands-on projects:\*\* (\d+)", "hands_on_projects"),
    ("stats topic indexes", r"\*\*Topic indexes:\*\* (\d+)", "topic_indexes"),
    ("stats career roadmaps", r"\*\*Career roadmaps:\*\* (\d+)", "roadmaps"),
    ("stats interview prep", r"\*\*Interview prep guides:\*\* (\d+)", "interview_prep"),
    ("stats migration guides", r"\*\*Migration guides:\*\* (\d+)", "migration_guides"),
    # The repository-structure code block restates three of them again.
    ("tree concept pages", r"# (\d+) bite-size concept pages", "concept_pages"),
    ("tree certifications", r"# (\d+) certs across \d+ providers", "certifications"),
    ("tree providers", r"# \d+ certs across (\d+) providers", "providers"),
]

# The same treatment for learn/README.md, which advertises its own count of
# concept pages. It was outside this script until 2026-09-17, so adding six data
# pages left it reading 46 against 52 - a drift of exactly the kind the README
# claims were locked down to prevent, one directory down.
LEARN_CLAIMS: list[tuple[str, str, str]] = [
    ("learn concept pages", r"\*\*\[Concepts\]\(\./concepts/\)\*\* - (\d+) topic pages", "concept_pages"),
]

# Every file this script owns, and the claims it owns in each. The word count and
# the doc-link floor are README-only, so they are keyed off the path below.
GUARDED: list[tuple[Path, list[tuple[str, str, str]]]] = [
    (README, CLAIMS),
    (LEARN_README, LEARN_CLAIMS),
]


# Not checked here: the per-provider table under "Browse Certifications". It is
# generated from docs/certs.json by build-provider-indexes.py, between markers,
# and verified by that script's --check. Two scripts owning the same table would
# be worse than one - this one's --fix would happily correct a count inside a
# generated block and leave the generator reporting it stale.


def check(
    text: str,
    actual: dict[str, int],
    claims: list[tuple[str, str, str]],
    *,
    prose_claims: bool = True,
) -> tuple[list[str], str]:
    """Return (problems, corrected text).

    `prose_claims` covers the word count and the doc-link floor, which are stated
    in README.md only. Every other guarded file gets the numeric claims alone.
    """
    problems: list[str] = []
    fixed = text

    for label, pattern, key in claims:
        matches = list(re.finditer(pattern, fixed))
        if not matches:
            problems.append(f"{label}: nothing matched /{pattern}/ - claim removed or reworded?")
            continue
        if len(matches) > 1:
            problems.append(f"{label}: matched {len(matches)} times, expected exactly one")
            continue

        match = matches[0]
        claimed = int(match.group(1))
        want = actual[key]
        if claimed != want:
            problems.append(f"{label}: file says {claimed}, tree has {want}")
            start, end = match.span(1)
            fixed = fixed[:start] + str(want) + fixed[end:]

    if not prose_claims:
        return problems, fixed

    # Word count, stated as a rounded "N.NM words" figure.
    want_m = actual["words"] / 1_000_000
    word_matches = list(re.finditer(r"([\d.]+)M words", fixed))
    if not word_matches:
        problems.append("word count: no 'N.NM words' claim found in README")
    else:
        for match in word_matches:
            claimed_m = float(match.group(1))
            if abs(claimed_m - want_m) > WORD_TOLERANCE_MILLIONS:
                problems.append(
                    f"word count: README says {claimed_m}M, tree has {want_m:.1f}M "
                    f"(tolerance {WORD_TOLERANCE_MILLIONS}M)"
                )
        fixed = re.sub(r"[\d.]+M words", f"{want_m:.1f}M words", fixed)

    # Doc links are advertised as a floor ("12,000+"), so only a shortfall is drift.
    floor_match = re.search(r"([\d,]+)\+ embedded vendor doc links", fixed)
    if not floor_match:
        problems.append("doc links: no 'N+ embedded vendor doc links' claim found")
    else:
        floor = int(floor_match.group(1).replace(",", ""))
        if actual["doc_links"] < floor:
            problems.append(
                f"doc links: README advertises {floor:,}+, tree has only "
                f"{actual['doc_links']:,}"
            )

    return problems, fixed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="exit 1 if the README has drifted")
    parser.add_argument("--fix", action="store_true", help="rewrite README.md with correct counts")
    args = parser.parse_args()

    actual = gather()

    problems: list[str] = []
    rewritten: list[str] = []
    for path, claims in GUARDED:
        text = path.read_text(encoding="utf-8")
        found, fixed = check(text, actual, claims, prose_claims=(path == README))
        rel = path.relative_to(REPO)
        problems += [f"{rel}: {problem}" for problem in found]
        if found and args.fix and fixed != text:
            path.write_text(fixed, encoding="utf-8")
            rewritten.append(str(rel))

    if not problems:
        print(f"README counts are up to date ({actual['certifications']} certs, "
              f"{actual['concept_pages']} concepts, {actual['words'] / 1e6:.1f}M words).")
        return 0

    for problem in problems:
        print(f"  drift: {problem}")

    if args.fix:
        print(f"\nRewrote {', '.join(rewritten) if rewritten else 'nothing'}. "
              "Re-run without --fix to confirm.")
        return 0

    print(f"\n{len(problems)} problem(s). Run with --fix to correct the numeric ones.")
    return 1 if args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
