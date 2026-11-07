#!/usr/bin/env python3
"""Report cert guides and concept pages whose last-updated date is old or missing.

Advisory by default: prints a table and exits 0. Nothing here opens issues or pings anyone.

Scope (kept narrow on purpose: the pages a reader trusts for facts that move):
  - cert guides: exams/<provider>/<cert>/README.md and fact-sheet.md
  - concept pages: learn/concepts/*.md (README.md excluded)

A page's date is the newest of these, so either style counts:
  - frontmatter `last-updated:` or `last-verified:` (YYYY-MM-DD)
  - a header line `**Last updated:** YYYY-MM-DD` or `**Last reviewed:** YYYY-MM-DD`

Usage:
  python3 .github/scripts/check-freshness.py                  # table, exit 0
  python3 .github/scripts/check-freshness.py --days 365       # change the threshold (default 120)
  python3 .github/scripts/check-freshness.py --strict         # exit 1 if any page is older than --days
  python3 .github/scripts/check-freshness.py --strict --fail-undated   # undated pages fail too
  python3 .github/scripts/check-freshness.py --report out.md  # also write the table as Markdown
  python3 .github/scripts/check-freshness.py --self-test
"""

import argparse
import datetime
import os
import re
import sys
import tempfile

DEFAULT_DAYS = 120

# (directory, glob-style regex relative to the repo root)
SCOPES = [
    re.compile(r"^exams/[^/]+/[^/]+/(README|fact-sheet)\.md$"),
    re.compile(r"^learn/concepts/(?!README\.md$)[^/]+\.md$"),
]
SKIP_DIRS = {".git", ".site-src", "site", "node_modules", "__pycache__"}

FRONT_KEY = re.compile(r"^(last-updated|last-verified):\s*['\"]?(\d{4}-\d{2}-\d{2})", re.M)
HEADER = re.compile(
    r"^[>*_ ]*\**(?:last[ -](?:updated|reviewed|verified))\**\s*:?\**\s*(\d{4}-\d{2}-\d{2})",
    re.I | re.M,
)


def page_date(text):
    """Newest valid date found in the frontmatter or the first 40 lines, else None."""
    found = []
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            found += [m.group(2) for m in FRONT_KEY.finditer(text[:end])]
    head = "\n".join(text.split("\n")[:40])
    found += [m.group(1) for m in HEADER.finditer(head)]
    dates = []
    for value in found:
        try:
            dates.append(datetime.date.fromisoformat(value))
        except ValueError:
            pass
    return max(dates) if dates else None


def in_scope(rel):
    return any(p.match(rel) for p in SCOPES)


def scan(root, today, days):
    """Return (stale, undated, total). stale rows are (age_days, rel, date), oldest first."""
    stale, undated, total = [], [], 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/")
            if not in_scope(rel):
                continue
            total += 1
            with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
                date = page_date(fh.read())
            if date is None:
                undated.append(rel)
            elif (today - date).days > days:
                stale.append(((today - date).days, rel, date))
    stale.sort(key=lambda r: (-r[0], r[1]))
    return stale, sorted(undated), total


def render(stale, undated, total, days, today):
    lines = [
        f"Freshness report for {today.isoformat()}: {total} pages in scope, "
        f"{len(stale)} older than {days} days, {len(undated)} with no date.",
        "",
    ]
    if stale:
        lines += ["| Age (days) | Last date | Page |", "|---:|---|---|"]
        lines += [f"| {age} | {d.isoformat()} | {rel} |" for age, rel, d in stale]
        lines.append("")
    if undated:
        lines += ["No date found:", ""] + [f"- {rel}" for rel in undated] + [""]
    if not stale and not undated:
        lines.append("Nothing stale and nothing undated.")
    return "\n".join(lines)


def self_test():
    today = datetime.date(2026, 11, 7)
    cases = {
        "exams/aws/saa/fact-sheet.md": "---\nlast-updated: 2026-11-01\n---\n# x\n",
        "exams/aws/saa/README.md": "---\nlast-updated: 2026-01-01\n---\n# old\n",
        "exams/aws/saa/notes/01.md": "---\nlast-updated: 2020-01-01\n---\n# out of scope\n",
        "learn/concepts/a.md": "# A\n\n**Last reviewed:** 2025-01-01\n",
        "learn/concepts/b.md": "# B\n\nno date here\n",
        "learn/concepts/c.md": "---\nlast-updated: 2026-13-45\n---\n# bad date\n",
        "learn/concepts/d.md": "---\nlast-updated: 2024-01-01\nlast-verified: 2026-10-30\n---\n# newest wins\n",
        "learn/concepts/README.md": "# index, ignored\n",
    }
    with tempfile.TemporaryDirectory() as tmp:
        for rel, body in cases.items():
            path = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
        stale, undated, total = scan(tmp, today, 120)
    assert total == 6, total
    assert [r[1] for r in stale] == ["learn/concepts/a.md", "exams/aws/saa/README.md"], stale
    assert undated == ["learn/concepts/b.md", "learn/concepts/c.md"], undated
    assert page_date("---\nlast-updated: 2026-11-01\n---\n") == datetime.date(2026, 11, 1)
    assert page_date("# T\n**Last Updated:** 2026-02-03\n") == datetime.date(2026, 2, 3)
    print("self-test ok")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--days", type=int, default=DEFAULT_DAYS)
    ap.add_argument("--strict", action="store_true", help="exit 1 if any page is older than --days")
    ap.add_argument("--fail-undated", action="store_true", help="with --strict, undated pages also fail")
    ap.add_argument("--report", help="also write the report to this file")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    stale, undated, total = scan(root, today, args.days)
    if total == 0:
        print("No pages matched the freshness scope; the path patterns are out of date.")
        return 1
    report = render(stale, undated, total, args.days, today)
    print(report)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(report + "\n")
    if args.strict and (stale or (args.fail_undated and undated)):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
