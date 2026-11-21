"""MkDocs hooks: per-page search metadata for the published site.

Loaded through `hooks:` in mkdocs.yml. Everything here is site-only: it sets
keys on `page.meta` at build time and never touches the repo's markdown (see
CLAUDE.md - no frontmatter is added to satisfy the site build).

Why this exists. Until 2026-09-28 every one of the ~2,000 pages shipped the
same `<meta name="description">` - the site-wide `site_description` - and a
`<title>` that ended in the 45-character site name, so an exam code near the
end of a long cert title was cut off in search results. Google treats a
repeated description as boilerplate and writes its own snippet. So:

- `description`: a page's own first prose paragraph, or for cert landing
  pages and fact sheets a summary built from `docs/certs.json` (those pages
  open with a fact list, not prose, and they are the pages people search for
  by exam code). A frontmatter `description:` always wins.
- `seo_title`: the full `<title>` text, rendered by the `htmltitle` override in
  `.github/site-overrides/main.html`. Pages inside a cert directory whose own
  title lacks the exam code get it appended ("Core Data Concepts - DP-900").
- `jsonld`: schema.org BreadcrumbList for every page, plus WebSite on the home
  page, emitted as JSON-LD by the same override.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

SITE_SHORT = "Zero to Hero"

# Working files published for transparency, not written for search visitors.
NOINDEX = ("TODO.md", "CLAUDE.md", "docs/improvement-roadmap.md", "docs/link-rot-")
DESC_MAX = 160
DESC_MIN = 50

_CERTS_JSON = Path(__file__).resolve().parents[2] / "docs" / "certs.json"
_certs: dict[str, dict] = {}


def _load_certs() -> None:
    if _certs or not _CERTS_JSON.is_file():
        return
    data = json.loads(_CERTS_JSON.read_text(encoding="utf-8"))
    for cert in data.get("certs", []):
        if cert.get("path"):
            _certs[cert["path"].rstrip("/")] = cert


def _cert_for(src_uri: str) -> tuple[dict | None, str]:
    """The cert a page belongs to, and the page's path inside the cert dir."""
    parts = src_uri.split("/")
    for i in range(len(parts) - 1, 0, -1):
        cert = _certs.get("/".join(parts[:i]))
        if cert:
            return cert, "/".join(parts[i:])
    return None, ""


# --------------------------------------------------------------------------- #
# Text cleanup
# --------------------------------------------------------------------------- #

_EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍←-⇿⌀-⏿]"
)
_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_REF_LINK_RE = re.compile(r"\[([^\]]*)\]\[[^\]]*\]")
_HTML_RE = re.compile(r"<[^>]+>")
_ATTR_LIST_RE = re.compile(r"\{:?[^}]*\}")


def _plain(text: str) -> str:
    text = _IMAGE_RE.sub("", text)
    text = _LINK_RE.sub(r"\1", text)
    text = _REF_LINK_RE.sub(r"\1", text)
    text = _HTML_RE.sub("", text)
    text = _ATTR_LIST_RE.sub("", text)
    text = _EMOJI_RE.sub("", text)
    text = re.sub(r"(\*\*|__|\*|`|~~)", "", text)
    # Attribute-safe: templates render these unescaped inside content="...".
    text = text.replace('"', "'").replace("<", "").replace(">", "")
    return re.sub(r"\s+", " ", text).strip()


def _clip(text: str, limit: int = DESC_MAX) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit - 3].rsplit(" ", 1)[0].rstrip(",;:-(")
    return cut + "..."


def _title_text(title: str | None) -> str:
    title = _plain(title or "")
    return re.sub(r"^[^\w(]+\s*", "", title)


# --------------------------------------------------------------------------- #
# Description from the page body
# --------------------------------------------------------------------------- #

_FENCE_RE = re.compile(r"^\s{0,3}(```+|~~~+)")
_NON_PROSE_START = ("#", "|", "- ", "* ", "+ ", ">", "<", "!", "---", "***", "___", "[!", ":::", "{")
# "**Duration:** 130 minutes" fact lines, and short bold-only lines.
_LABEL_LINE_RE = re.compile(r"^\*\*[^*]{1,60}(:\*\*|\*\*:)|^\*\*[^*]{1,60}\*\*.{0,40}$")
_NUMBERED_RE = re.compile(r"^\d+[.)]\s")


def _blocks(markdown: str) -> list[list[str]]:
    """Split the body into blank-line separated blocks, skipping code fences."""
    blocks, cur, fence = [], [], None
    for line in markdown.splitlines():
        m = _FENCE_RE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            continue
        if m:
            fence = m.group(1)
            if cur:
                blocks.append(cur)
                cur = []
            continue
        if line.lstrip().startswith("#"):
            if cur:
                blocks.append(cur)
                cur = []
            blocks.append([line.rstrip()])
        elif line.strip():
            cur.append(line.rstrip())
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return blocks


def _prose_lines(block: list[str]) -> list[str]:
    """A paragraph that runs straight into a list or table keeps only its lead-in."""
    out = []
    for line in block:
        l = line.lstrip()
        if out and (l.startswith(_NON_PROSE_START) or _NUMBERED_RE.match(l)):
            break
        out.append(line)
    return out


def _is_prose(block: list[str]) -> bool:
    first = block[0].lstrip()
    if first.startswith(_NON_PROSE_START) or _NUMBERED_RE.match(first):
        return False
    if all(_LABEL_LINE_RE.match(l.strip()) for l in block):
        return False
    return bool(re.search(r"[A-Za-z]{3,}", _plain(" ".join(block))))


def description_from_body(markdown: str) -> str:
    blocks = _blocks(markdown)
    quote = ""
    for block in blocks[:40]:
        if _is_prose(block):
            text = _plain(" ".join(_prose_lines(block)))
            if len(text) >= DESC_MIN:
                return _clip(text)
        elif not quote and block[0].lstrip().startswith(">"):
            lines = [re.sub(r"^\s*>\s?", "", l) for l in block]
            text = _plain(" ".join(l for l in lines if not _LABEL_LINE_RE.match(l.strip())))
            text = re.sub(r"^\[![A-Z]+\]\s*", "", text)
            if len(text) >= DESC_MIN:
                quote = _clip(text)
    return quote


# --------------------------------------------------------------------------- #
# Cert pages: built from certs.json
# --------------------------------------------------------------------------- #

def _code(cert: dict) -> str:
    return cert.get("exam_code") or cert.get("name", "")


def _exam_facts(cert: dict) -> str:
    facts = []
    if cert.get("duration"):
        facts.append(cert["duration"])
    if cert.get("questions"):
        q = str(cert["questions"])
        facts.append(q if "question" in q.lower() else f"{q} questions")
    if cert.get("passing_score"):
        facts.append(f"{cert['passing_score']} to pass")
    return ", ".join(facts)


def cert_description(cert: dict, inner: str) -> str:
    code, name = _code(cert), cert.get("name", "")
    facts = _exam_facts(cert)
    notes = cert.get("notes_count") or 0
    if inner == "README.md":
        parts = [f"Free {name} study guide"]
        extras = []
        if notes:
            extras.append(f"{notes} study notes")
        extras += ["a practice plan", "scenarios", "exam-day strategy"]
        text = f"{parts[0]}: {', '.join(extras[:-1])} and {extras[-1]}."
        if facts:
            text += f" {code}: {facts}."
        return _clip(text)
    if inner == "fact-sheet.md":
        text = f"{code} fact sheet for {name}: cost, format, domains and official links."
        if facts:
            text += f" {facts}."
        if cert.get("cost"):
            text += f" Costs {cert['cost']}."
        return _clip(text)
    if inner == "notes/README.md":
        return _clip(f"{code} study notes: every topic note for {name}, in study order.")
    # These three open with a fact list or straight into week 1, so their first
    # paragraph is a poor summary and near-identical across certs.
    if inner == "practice-plan.md":
        return _clip(f"{code} study plan: a week-by-week schedule for {name} that covers every exam domain.")
    if inner == "scenarios.md":
        return _clip(f"{code} practice scenarios: exam-style situations for {name}, with worked answers.")
    if inner == "strategy.md":
        return _clip(f"{code} exam strategy for {name}: time management, question patterns and final review.")
    return ""


def _title_tag(cert: dict, title: str) -> str:
    """What to append to a cert page's title so it names its exam, or "" if it already does.

    A plain code ("DP-900") when the cert has one. Otherwise the cert's short
    name ("CompTIA A+" for 220-1201 + 220-1202), unless the title already
    carries it without the provider prefix ("Vault Associate - Scenarios").
    """
    low = title.lower()
    code = cert.get("exam_code") or ""
    if code and " " not in code:
        return "" if code.lower() in low else code
    if code and code.lower() in low:
        return ""
    short = cert.get("name", "").split(" (")[0].split(" - ")[0].strip()
    bare = short.removeprefix(cert.get("provider_name", "")).strip()
    if not bare or bare.lower() in low:
        return ""
    return short


_KIND = {
    "practice-plan.md": "study plan",
    "scenarios.md": "practice scenarios",
    "strategy.md": "exam strategy",
}


def _kind_of(inner: str) -> str:
    if inner.startswith("notes/"):
        return "notes"
    return _KIND.get(inner, "")


# --------------------------------------------------------------------------- #
# Hooks
# --------------------------------------------------------------------------- #

def on_config(config, **kwargs):
    _load_certs()
    return config


def on_page_markdown(markdown, page, config, files, **kwargs):
    meta = page.meta
    src = page.file.src_uri
    cert, inner = _cert_for(src)
    # The page's own H1, not page.title: nav labels are clipped to 72 chars and
    # can carry a provider emoji.
    h1 = re.search(r"^#\s+(.+?)\s*#*\s*$", markdown, re.MULTILINE)
    title = _title_text(h1.group(1) if h1 else page.title)

    if not meta.get("description") and not page.is_homepage:
        desc = cert_description(cert, inner) if cert else ""
        if not desc:
            desc = description_from_body(markdown)
        if desc and cert and _code(cert) not in desc:
            kind = _kind_of(inner)
            lead = f"{_code(cert)} {kind}" if kind else _code(cert)
            desc = _clip(f"{lead}: {desc}")
        elif desc and not cert and title and len(desc) < 90 and title.lower() not in desc.lower():
            desc = _clip(f"{title}: {desc}")
        if not desc and title:
            desc = _clip(f"{title} - free study notes from {config.site_name}.")
        if desc:
            meta["description"] = desc

    if src.startswith(NOINDEX):
        meta["robots"] = "noindex, follow"

    if page.is_homepage:
        meta["seo_title"] = config.site_name
    elif title:
        if cert and inner == "README.md":
            seo = f"{title} Study Guide"
        elif cert and inner == "notes/README.md":
            seo = f"{_code(cert)} Study Notes"
        elif cert and (tag := _title_tag(cert, title)):
            seo = f"{title} - {tag}"
        else:
            seo = title
        # The brand suffix only while the whole title still fits a result line.
        meta["seo_title"] = f"{seo} | {SITE_SHORT}" if len(seo) <= 50 else seo
    return markdown


def _section_url(section) -> str | None:
    for child in getattr(section, "children", None) or []:
        if getattr(child, "is_page", False) and getattr(child, "is_index", False):
            return child.canonical_url
    return None


def on_page_context(context, page, config, nav, **kwargs):
    site = config.site_url
    crumbs = [{"name": "Home", "item": site}]
    for section in reversed(page.ancestors):
        url = _section_url(section)
        if url and url != site:
            crumbs.append({"name": _title_text(section.title), "item": url})
    if not page.is_homepage and page.canonical_url not in {c["item"] for c in crumbs}:
        crumbs.append({"name": _title_text(page.title), "item": page.canonical_url})

    graph = []
    if len(crumbs) > 1:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, **c} for i, c in enumerate(crumbs)
            ],
        })
    if page.is_homepage:
        graph.append({
            "@type": "WebSite",
            "name": config.site_name,
            "alternateName": SITE_SHORT,
            "url": site,
            "description": config.site_description.strip(),
            "inLanguage": "en",
            "author": {"@type": "Person", "name": config.site_author, "url": "https://patricklukewilson.com"},
            "publisher": {"@type": "Organization", "name": "Nobler Works", "url": "https://noblerworks.com/"},
        })
    if graph:
        doc = {"@context": "https://schema.org", "@graph": graph}
        # "</" inside a <script> would end it early.
        page.meta["jsonld"] = json.dumps(doc, ensure_ascii=False).replace("</", "<\\/")
    return context


# Renamed paths (2026-11-21): old URL prefix -> new prefix. Search engines and old links
# still hit the old URLs, so every built page under a new prefix gets a stub at the
# old one: a meta refresh plus a canonical link (GitHub Pages has no server redirects).
MOVED = {
    "exams/hashicorp/packer-associate/": "exams/hashicorp/packer/",
    "exams/hashicorp/nomad-associate/": "exams/hashicorp/nomad/",
    "resources/practice-questions/hashicorp-packer-associate/": "resources/practice-questions/hashicorp-packer/",
    "resources/practice-questions/hashicorp-nomad-associate/": "resources/practice-questions/hashicorp-nomad/",
}

_STUB = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title>'
    '<link rel="canonical" href="{url}"><meta name="robots" content="noindex">'
    '<meta http-equiv="refresh" content="0; url={url}"></head>'
    '<body><p>This page moved to <a href="{url}">{url}</a>.</p></body></html>'
)


def redirect_stubs(site_dir: Path, site_url: str) -> list[Path]:
    """Write a stub at each old path for every index.html under a moved prefix. Returns the stubs."""
    base = site_url.rstrip("/") + "/"
    written = []
    for old, new in MOVED.items():
        root = site_dir / new
        if not root.is_dir():
            raise RuntimeError(f"redirect target {new} was not built - update MOVED in site_hooks.py")
        for page in root.rglob("index.html"):
            rel = page.relative_to(root).parent.as_posix()
            tail = "" if rel == "." else rel + "/"
            stub = site_dir / old / tail / "index.html"
            if stub.exists():
                raise RuntimeError(f"{old}{tail} is a real page again - drop it from MOVED")
            stub.parent.mkdir(parents=True, exist_ok=True)
            stub.write_text(_STUB.format(url=base + new + tail), encoding="utf-8")
            written.append(stub)
    return written


def on_post_build(config, **kwargs):
    redirect_stubs(Path(config["site_dir"]), config["site_url"] or "/")
