#!/usr/bin/env python3
"""Fail on any markdown file with an unclosed code fence.

An unclosed ``` or ~~~ fence swallows the rest of the page into a code block. The
site build only notices as a pile of missing anchors; this names the file and the
line of the opening fence.

Rules (CommonMark):
  - a fence is 3+ backticks or tildes, indented any amount (fences inside list
    items and blockquotes are indented or prefixed with `>`)
  - a backtick fence's info string may not contain a backtick, so a line like
    ```code``` is inline code, not a fence
  - a closing fence uses the same character, is at least as long as the opener,
    and has nothing after it but whitespace

Checks tracked *.md files (git ls-files); falls back to walking the tree. Generated
and vendored directories (site/, .site-src/, node_modules/) are never checked.

Run: python3 .github/scripts/check-code-fences.py
     python3 .github/scripts/check-code-fences.py --self-test
Exits 1 if any fence is unclosed.
"""

import os
import re
import subprocess
import sys

SKIP_DIRS = {"site", ".site-src", "node_modules", ".git", "__pycache__"}
QUOTE_PREFIX = re.compile(r"^(?:\s*>)+")
FENCE = re.compile(r"^\s*(?P<marker>`{3,}|~{3,})(?P<rest>.*)$")


def unclosed_fences(text):
    """Return [(lineno, marker)] for every fence still open at end of file."""
    open_fence = None  # (char, length, lineno)
    for lineno, line in enumerate(text.splitlines(), 1):
        body = QUOTE_PREFIX.sub("", line)
        m = FENCE.match(body)
        if open_fence is None:
            if not m:
                continue
            marker, rest = m.group("marker"), m.group("rest")
            if marker[0] == "`" and "`" in rest:
                continue  # inline code that happens to start a line
            open_fence = (marker[0], len(marker), lineno)
        elif m and m.group("marker")[0] == open_fence[0] \
                and len(m.group("marker")) >= open_fence[1] \
                and not m.group("rest").strip():
            open_fence = None
    if open_fence:
        return [(open_fence[2], open_fence[0] * open_fence[1])]
    return []


def markdown_files():
    try:
        out = subprocess.run(
            ["git", "ls-files", "*.md"], capture_output=True, text=True, check=True
        ).stdout.split("\n")
        files = [f for f in out if f]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for root, dirs, names in os.walk("."):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            files += [os.path.join(root, n) for n in names if n.endswith(".md")]
    return sorted(
        f for f in files
        if not (set(f.replace("\\", "/").split("/")) & SKIP_DIRS) and os.path.isfile(f)
    )


def self_test():
    cases = [
        ("```\ncode\n```\n", 0),
        ("```\ncode\n", 1),
        ("````\n```\ninner\n```\n````\n", 0),   # longer outer fence holds a shorter one
        ("````\n```\ninner\n```\n", 1),         # inner ``` cannot close a ```` fence
        ("~~~\ncode\n~~~\n", 0),
        ("~~~\n```\n~~~\n", 0),                 # other character is content
        ("```\n~~~\n", 1),
        ("```python\nx\n```\n", 0),
        ("```\nx\n``` trailing\n", 1),          # closer cannot carry text
        ("- item\n\n    ```bash\n    ls\n    ```\n", 0),
        ("- item\n\n    ```bash\n    ls\n", 1),
        ("> ```\n> x\n> ```\n", 0),
        ("see ```inline``` here\n", 0),         # inline, not a fence
        ("```inline``` at line start\n", 0),
        ("text\n\n```\nopen\n\nmore text\n", 1),
    ]
    bad = 0
    for text, expected in cases:
        got = len(unclosed_fences(text))
        if got != expected:
            bad += 1
            print(f"SELF-TEST FAIL: expected {expected}, got {got} for {text!r}")
    print(f"check-code-fences self-test: {len(cases) - bad}/{len(cases)} passed.")
    return 1 if bad else 0


def main():
    if "--self-test" in sys.argv:
        return self_test()
    failures = 0
    files = markdown_files()
    for path in files:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            for lineno, marker in unclosed_fences(fh.read()):
                failures += 1
                print(f"UNCLOSED FENCE  {path}:{lineno}  opens {marker}")
    print(f"\nSummary: {len(files)} markdown files checked. Unclosed fences: {failures}.")
    if failures:
        print("\nClose the fence (same character, at least as long as the opener).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
