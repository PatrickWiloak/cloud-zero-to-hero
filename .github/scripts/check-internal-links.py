#!/usr/bin/env python3
"""Check that every relative markdown link resolves to a file on disk.

Complements the lychee workflow, which checks external URLs. External URLs rot for
reasons outside a contributor's control, so that check is advisory. Internal links
are fully under our control, so this check is blocking.

Skips, because these are not real links:
  - fenced code blocks (``` and ~~~)
  - inline code spans (`like this`)
  (HTML <a href="..."> anchors are validated exactly like markdown links)
  - external schemes (http, https, mailto, tel)
  - image and link targets containing < > placeholders, e.g. <topic>/<slug>.png

Anchors: a link with a #fragment (and a bare same-page #fragment) must name an id
that exists on the target page, so a broken anchor is reported with file:line and
no site build. The ids are the ones the MkDocs build produces, because the strict
build is the ground truth (validation.anchors: warn in mkdocs.yml):
  - headings are slugged with pymdownx.slugs.slugify(case="lower") (GitHub style:
    "Security & Identity" is #security--identity; a leading emoji leaves a leading
    hyphen), duplicates get Python-Markdown's _1, _2 suffix, and explicit ids
    ({: #id }, <a id="...">) are never renamed
  - build-site.py strips a leading emoji from non-H1 headings and PINS the original
    slug, so those anchors keep the emoji hyphen; an H1 is stripped without a pin,
    so its anchor is the slug of the stripped text
  - anchors on files that are not markdown (or are outside the tree) are not checked

Run locally: python3 .github/scripts/check-internal-links.py
             python3 .github/scripts/check-internal-links.py --self-test
Exits 1 if any internal link or anchor is broken.
"""

import html
import os
import re
import sys
import unicodedata
from urllib.parse import unquote

SKIP_DIRS = {".git", "node_modules", ".github/scripts/__pycache__"}

# Build output. Present after a local site build, absent in CI, and a complete
# second copy of the tree - so walking it double-counts every link and reports a
# different total depending on whether someone has run the site build.
SKIP_PATHS = {os.path.join(".", ".site-src"), os.path.join(".", "site"),
              # Loop drafts (nobler-os content-refill, 2026-11-13): never built, and their links are written
              # for where they will live once published, so they resolve only after the move. See drafts/README.md.
              os.path.join(".", "drafts")}

# The site's landing page template. Its links are written relative to the stage
# root, where the build renders it as README.md, not relative to the directory it
# is stored in. The `--strict` site build validates them there.
SKIP_FILES = {os.path.join(".", ".github", "site", "home.md")}
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:)")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
# Plain HTML anchors, as used in the "Check yourself" answers: <a href="#frag">.
HTML_LINK = re.compile(r"""<a\s[^>]*?\bhref\s*=\s*(["'])(.*?)\1""", re.IGNORECASE)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
QUOTE_PREFIX = re.compile(r"^(?:\s*>)+")
INLINE_CODE = re.compile(r"`[^`]*`")

# --- heading ids: must mirror mkdocs.yml (toc + pymdownx slugify) and build-site.py
RE_TAGS = re.compile(r"</?[^>]*>")
RE_INVALID_SLUG_CHAR = re.compile(r"[^\w\- ]")
# Same emoji set build-site.py strips (strip_heading_emoji); keep the two in step.
EMOJI_PREFIX_RE = re.compile(
    "^["
    "\U0001F000-\U0001FAFF"
    "☀-➿"
    "⬀-⯿"
    "ℹ"
    "⏩-⏺"
    "️‍"
    "\U0001F1E6-\U0001F1FF"
    "]+[ \t]+"
)
ATX = re.compile(r"^ {0,3}(?P<hashes>#{1,6})(?:[ \t]+(?P<text>.*?))?(?:[ \t]+#+)?[ \t]*$")
SETEXT = re.compile(r"^ {0,3}(=+|-{2,})[ \t]*$")
ATTR_TAIL = re.compile(r"\s*\{:?\s*([^{}]*)\}\s*$")
ATTR_ID = re.compile(r"#([^\s}]+)")
RAW_ID = re.compile(r"""\b(?:id|name)\s*=\s*["']([^"']+)["']""")
RAW_ID_ONLY = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""")
ATTR_LIST_ANY = re.compile(r"\{:?\s*[^{}]*?#([^\s{}]+)[^{}]*\}")


# pymdownx.smartsymbols (enabled in mkdocs.yml) rewrites these in rendered text before
# toc slugs it. Only the fractions survive slugify (they are word characters); the rest vanish.
SMART_FRACTIONS = {
    "1/4": "\u00bc", "1/2": "\u00bd", "3/4": "\u00be", "1/3": "\u2153", "2/3": "\u2154",
    "1/5": "\u2155", "2/5": "\u2156", "3/5": "\u2157", "4/5": "\u2158", "1/6": "\u2159",
    "5/6": "\u215a", "1/8": "\u215b", "3/8": "\u215c", "5/8": "\u215d", "7/8": "\u215e",
}
RE_SMART_FRACTION = re.compile(r"(?<!\d)(" + "|".join(SMART_FRACTIONS) + r")(?!\d)")
RE_SMART_OTHER = re.compile(r"\((?:c|r|tm)\)|\+/-|=/=|<-->|(?<!-)-{2}>|<-{2}(?!-)")


def slugify(text):
    """pymdownx.slugs.slugify(case="lower") with sep "-" (what mkdocs.yml configures)."""
    slug = RE_TAGS.sub("", unicodedata.normalize("NFC", text)).strip().lower()
    return RE_INVALID_SLUG_CHAR.sub("", slug).replace(" ", "-")


def unique(ident, used):
    """Python-Markdown toc.unique: append _1, _2 ... until the id is free."""
    while ident in used or not ident:
        m = re.match(r"^(.*)_([0-9]+)$", ident)
        ident = f"{m.group(1)}_{int(m.group(2)) + 1}" if m else f"{ident}_1"
    used.add(ident)
    return ident


def rendered_text(raw):
    """Approximate the text of a heading after inline markdown is rendered."""
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", raw)      # links and images
    t = re.sub(r"\[([^\]]*)\]\[[^\]]*\]", r"\1", t)         # reference links
    parts = re.split(r"(`+.+?`+)", t)                       # code spans are literal
    for n, part in enumerate(parts):
        if n % 2:
            parts[n] = re.sub(r"^(`+)(.+?)\1$", r"\2", part)
            continue
        part = re.sub(r"(\*{1,3})(?=\S)(.+?)(?<=\S)\1", r"\2", part)  # *x* and **x**; a lone * stays
        part = re.sub(r"(?<!\w)_+(.+?)_+(?!\w)", r"\1", part)  # _x_, not snake_case
        part = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|<>])", r"\1", part)
        part = RE_SMART_FRACTION.sub(lambda m: SMART_FRACTIONS[m.group(1)], part)
        parts[n] = RE_SMART_OTHER.sub("", part)
    t = "".join(parts)
    return html.unescape(RE_TAGS.sub("", t)).strip()


def code_state(lines):
    """Yield (lineno, line, in_code) where in_code covers fenced blocks and fences."""
    fence = None
    for i, line in enumerate(lines, 1):
        body = QUOTE_PREFIX.sub("", line.rstrip("\n"))
        m = FENCE.match(body)
        if fence is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)))
                yield i, line, True
                continue
            yield i, line, False
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] \
                    and not m.group(2).strip():
                fence = None
            yield i, line, True


def strip_code(lines):
    """Yield (lineno, text) with fenced blocks blanked and inline code removed."""
    for i, line, in_code in code_state(lines):
        yield i, "" if in_code else INLINE_CODE.sub("", line)


def link_targets(text):
    """Return the raw link targets on one code-stripped line: markdown and <a href>."""
    return [m.group(1) for m in LINK.finditer(text)] + [
        m.group(2) for m in HTML_LINK.finditer(text)
    ]


def heading_ids(lines):
    """Return the set of anchors the site build gives this page."""
    headings = []   # (level, source_text, explicit_id, setext) in document order
    explicit = set()
    raw_in_heading = set()  # <a id> inside a heading: in the page, but toc never sees it
    lines = list(lines)
    if lines and lines[0].strip() == "---":  # YAML frontmatter is not page content
        for end in range(1, len(lines)):
            if lines[end].strip() == "---":
                lines = [""] * (end + 1) + lines[end + 1:]
                break
    prose = [(i, line) for i, line, in_code in code_state(lines) if not in_code]
    prev = None
    for i, line in prose:
        text_line = line.rstrip("\n")
        m = ATX.match(text_line)
        if m:
            headings.append((len(m.group("hashes")), m.group("text") or "", True))
            prev = None
            continue
        sm = SETEXT.match(text_line)
        if sm and prev is not None and not re.match(r"^\s*([-*+>|]|\d+[.)])\s", prev):
            level = 1 if sm.group(1)[0] == "=" else 2
            headings.append((level, prev.strip(), False))
            prev = None
            continue
        prev = text_line if text_line.strip() else None
        clean = INLINE_CODE.sub("", text_line)
        explicit.update(RAW_ID.findall(clean))
        explicit.update(ATTR_LIST_ANY.findall(clean))
    # Raw html ids anywhere in a heading line also count.
    items = []
    for level, text, atx in headings:
        eid = None
        am = ATTR_TAIL.search(text)
        if am and ATTR_ID.search(am.group(1)):
            eid = ATTR_ID.search(am.group(1)).group(1)
            text = text[: am.start()]
        else:
            raw_in_heading.update(RAW_ID.findall(text))
        items.append((level, text.strip(), eid, atx))
        if eid:
            explicit.add(eid)
    used = set(i for i in explicit if i)  # toc pre-seeds every explicit id it can see
    ids = set(explicit) | raw_in_heading
    for level, text, eid, atx in items:
        if eid:
            continue
        simple = "](" not in text and "{" not in text and "<" not in text
        stripped = EMOJI_PREFIX_RE.sub("", text) if atx and simple else text
        if atx and simple and stripped and stripped != text:
            if level == 1:
                # H1: emoji stripped, no pin; slugged from the stripped text.
                ids.add(unique(slugify(rendered_text(stripped)), used))
            else:
                # build-site.py pins slug(original raw text) as an explicit id.
                ids.add(slugify(text))
            continue
        ids.add(unique(slugify(rendered_text(text)), used))
    return ids


def split_dest(link):
    """Split a markdown link target into (path, fragment); title is dropped."""
    link = link.strip()
    if " " in link:  # [text](path "Title")
        link = link.split(" ", 1)[0]
    path, _, frag = link.partition("#")
    return path.strip(), unquote(frag).strip()


def target_path(link):
    """Strip the optional title and the anchor from a markdown link target."""
    return split_dest(link)[0]


_ids_cache = {}


def ids_for(path):
    path = os.path.normpath(path)
    if path not in _ids_cache:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            _ids_cache[path] = heading_ids(fh.readlines())
    return _ids_cache[path]


def main():
    if "--self-test" in sys.argv:
        return self_test()
    broken = []
    checked = 0
    anchors = 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [
            d for d in dirs
            if d not in SKIP_DIRS and os.path.join(root, d) not in SKIP_PATHS
        ]
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            if path in SKIP_FILES:
                continue
            with open(path, encoding="utf-8", errors="ignore") as fh:
                lines = fh.readlines()
            for lineno, text in strip_code(lines):
                for raw in link_targets(text):
                    dest, frag = split_dest(raw)
                    if EXTERNAL.match(dest) or "<" in dest or "<" in frag:
                        continue
                    if not dest and not frag:
                        continue
                    if dest:
                        checked += 1
                        resolved = os.path.normpath(os.path.join(root, dest))
                        if not os.path.exists(resolved):
                            broken.append(("BROKEN", path, lineno, dest))
                            continue
                    else:
                        resolved = os.path.normpath(path)
                    if (
                        frag
                        and not frag.startswith(":~:")
                        and resolved.endswith(".md")
                        and os.path.isfile(resolved)
                        and os.path.join(".", resolved) not in SKIP_FILES
                        and resolved != "README.md"  # site root is rendered from home.md
                    ):
                        anchors += 1
                        if frag not in ids_for(resolved):
                            broken.append(("NO ANCHOR", path, lineno, f"{dest}#{frag}"))

    for kind, path, lineno, dest in broken:
        print(f"{kind:9} {path}:{lineno}  ->  {dest}")

    print(
        f"\nSummary: {checked} internal links checked, {anchors} anchors checked. "
        f"Broken: {len(broken)}."
    )
    if broken:
        print(
            "\nFix by repointing the link, or drop the link and mark the target "
            "_(planned)_ if it has not been written yet. For NO ANCHOR, the heading "
            "was renamed or the slug is wrong (GitHub-style: lowercase, punctuation "
            "dropped, spaces to hyphens, a leading emoji leaves a leading hyphen)."
        )
        return 1
    return 0


def self_test():
    def ids(text):
        return heading_ids(text.splitlines(True))

    cases = [
        ("## Security & Identity\n", {"security--identity"}),
        ("## Plain Heading\n", {"plain-heading"}),
        ("## \U0001F3AF Quick Navigation\n", {"-quick-navigation"}),          # pinned
        ("# \U0001F3AF Title Here\n", {"title-here"}),                          # H1 not pinned
        ("## A\n\n## A\n\n## A\n", {"a", "a_1", "a_2"}),
        ("## Has `code` and **bold**\n", {"has-code-and-bold"}),
        ("## See [the docs](x.md) now\n", {"see-the-docs-now"}),
        ("## snake_case word\n", {"snake_case-word"}),
        ("## Closed ##\n", {"closed"}),
        ("## Custom {: #my-id }\n", {"my-id"}),
        ('<a id="term-x"></a>\n\n## H\n', {"term-x", "h"}),
        ("```\n## Not a heading\n```\n", set()),
        ("Setext\n======\n", {"setext"}),
        ("## Same\n\n## Same {: #same }\n", {"same", "same_1"}),  # explicit ids pre-seed toc
        ("## Q&A: What's new?\n", {"qa-whats-new"}),
        ("## 3. Avoid `SELECT *`\n", {"3-avoid-select-"}),
        ("## SELECT *\n", {"select-"}),                         # a lone star is not emphasis
        ("## T (Z^(1/4)) and 11/12\n", {"t-z\u00bc-and-1112"}),      # smartsymbols fraction survives
        ("## Copy (c) and a --> b\n", {"copy--and-a--b"}),         # other smart symbols vanish
        ("### Track <a id=\"track\"></a>\n\n### Track\n", {"track", "track_1"}),  # raw id in a heading does not pre-seed
        ("---\ntitle: x\n---\n\n## After\n", {"after"}),    # frontmatter is not a setext heading
    ]
    bad = 0
    for text, expected in cases:
        got = ids(text)
        if got != expected:
            bad += 1
            print(f"SELF-TEST FAIL: {text!r}: expected {sorted(expected)}, got {sorted(got)}")
    link_cases = [
        ("a [x](#frag) and `[y](#no)`", ["#frag"]),
        ("[t](other.md#a-b \"Title\")", ["other.md#a-b"]),
    ]
    for text, expected in link_cases:
        got = [m.group(1).split(" ", 1)[0] for m in LINK.finditer(INLINE_CODE.sub("", text))]
        if got != expected:
            bad += 1
            print(f"SELF-TEST FAIL: links in {text!r}: expected {expected}, got {got}")
    html_cases = [
        ('<a href="#how-a-lookup-works">x</a>', ["#how-a-lookup-works"]),           # same page
        ("<a href='#bad-one'>x</a>", ["#bad-one"]),                                  # single quotes
        ('<a class="c" href="other.md#sec">x</a>', ["other.md#sec"]),               # path + fragment
        ('<a href="../x/y.md">x</a>', ["../x/y.md"]),                               # plain path
        ('see `<a href="#no">x</a>` here', []),                                      # inline code
        ('<a href="https://e.com/#a">x</a>', ["https://e.com/#a"]),                  # extracted, skipped by EXTERNAL
    ]
    for text, expected in html_cases:
        got = link_targets(INLINE_CODE.sub("", text))
        if got != expected:
            bad += 1
            print(f"SELF-TEST FAIL: html links in {text!r}: expected {expected}, got {got}")
    fenced = ["```html\n", '<a href="#in-fence">x</a>\n', "```\n", '<a href="#out">x</a>\n']
    got = [t for _, line in strip_code(fenced) for t in link_targets(line)]
    if got != ["#out"]:
        bad += 1
        print(f"SELF-TEST FAIL: html href in a fence: expected ['#out'], got {got}")
    # End to end: line numbers and anchor verdicts for good and bad same-page anchors.
    page = ["## Real Heading\n", "\n", '<a href="#real-heading">ok</a>\n', '<a href="#nope">bad</a>\n']
    known = heading_ids(page)
    verdicts = [
        (n, t[1:] in known) for n, line in strip_code(page) for t in link_targets(line)
    ]
    if verdicts != [(3, True), (4, False)]:
        bad += 1
        print(f"SELF-TEST FAIL: html anchor verdicts: got {verdicts}")
    total = len(cases) + len(link_cases) + len(html_cases) + 2
    print(f"check-internal-links self-test: {total - bad}/{total} passed.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
