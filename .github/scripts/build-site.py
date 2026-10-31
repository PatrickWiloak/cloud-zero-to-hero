#!/usr/bin/env python3
"""Build the MkDocs Material site from the repository's markdown tree.

The repository is a browsable knowledge base first and a website second, so the
markdown tree at the repo root stays exactly as it is. This script adapts it to
MkDocs at build time instead of restructuring it:

1.  Stage every content file into `.site-src/`, mirroring the repo layout so that
    relative links, `edit_uri`, and the on-GitHub reading experience all keep
    working unchanged.
2.  Render `.github/site/home.md` over the staged root `README.md`. A repo front
    page and a website landing page want different things, and MkDocs treats
    README.md as the index, so the swap happens in the stage and the repo's own
    README is left alone.
3.  Generate an index page for any directory that has markdown children but no
    `README.md`, so that the ~1,200 directory-style links (`](../foo/)`) resolve
    and every nav section has a landing page.
4.  Generate the whole `nav` from the staged tree, with human-readable labels
    pulled from each page's H1 and cert labels pulled from `docs/certs.json`.
5.  Append that nav to a copy of `mkdocs.yml` and build from the copy.

Nothing here is hand-maintained per page: add a markdown file to the repo and it
appears in the site nav on the next build.

Usage:
    python3 .github/scripts/build-site.py            # build into site/
    python3 .github/scripts/build-site.py --strict   # warnings become errors (CI)
    python3 .github/scripts/build-site.py --serve    # stage, then live-reload
    python3 .github/scripts/build-site.py --stage-only
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
STAGE = REPO / ".site-src"
# Site chrome lives outside the content tree: `assets/` is the repo's diagram
# store and should stay that way. Copied into the stage at `assets/site/`, which
# is what `extra_css` in mkdocs.yml points at.
SITE_CHROME = REPO / ".github" / "site"
SITE_CHROME_DEST = "assets/site"
# The site's landing page. Rendered over the staged copy of README.md, so the
# repo keeps a repo front page and the site gets a website one.
HOME_TEMPLATE = SITE_CHROME / "home.md"
COUNTS_SCRIPT = Path(__file__).with_name("check-readme-counts.py")
BASE_CONFIG = REPO / "mkdocs.yml"
GENERATED_CONFIG = REPO / "mkdocs.generated.yml"
CERTS_JSON = REPO / "docs" / "certs.json"

# Top-level directories and files that make up the site, in tab order. Anything
# not listed is not staged. Keeping this explicit means adding a new top-level
# directory is a deliberate choice rather than an accident.
ROOT_FILES = ["README.md", "STUDY-HUB.md"]
CONTENT_DIRS = ["learn", "resources", "exams", "topics", "docs", "assets", ".templates"]
# TODO.md and CLAUDE.md are repo-internal (task list, agent instructions): not site pages (Patrick, 2026-10-31).
ABOUT_FILES = ["CONTRIBUTING.md", "CHANGELOG.md"]

# MkDocs ignores dot-directories inside docs_dir, but `.templates/` holds three
# real pages (the shared per-provider resource lists) that cert guides link to
# 144 times. Stage it under a visible name and rewrite the inbound links.
# The name must not be `templates`: MkDocs reserves a root `/templates/` and
# silently drops it from the build.
STAGE_RENAMES = {".templates": "provider-resources"}

# Never staged at any depth: VCS and tooling clutter.
EXCLUDED_DIR_NAMES = {".git", "__pycache__", "node_modules", ".ipynb_checkpoints"}

# Never staged, but only where they actually live, at the repo root. Matching
# these by bare name at any depth would silently drop legitimate content
# directories that happen to share a name (`assets/site/`, for instance).
EXCLUDED_ROOT_DIRS = {
    REPO / ".git",
    REPO / ".github",
    REPO / ".claude",
    REPO / ".venv-docs",
    STAGE,
    REPO / "site",
}

# Files copied as static assets rather than rendered as pages.
STATIC_SUFFIXES = {".csv", ".json", ".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".pdf", ".css"}

# Where each top-level path hangs in the navigation. Order here is tab order.
TABS: list[tuple[str, list[str]]] = [
    ("Learn", ["learn"]),
    (
        "Build",
        [
            "resources/hands-on-projects",
            "resources/architecture-patterns",
            "resources/cli-cheat-sheets",
            "resources/well-architected",
            "resources/troubleshooting",
        ],
    ),
    (
        "Certify",
        [
            "STUDY-HUB.md",
            "exams",
            "resources/practice-questions",
            "resources/certification-roadmaps",
            "resources/exam-prep",
        ],
    ),
    (
        "Reference",
        [
            "resources/README.md",
            "resources/service-comparisons",
            "resources/interview-prep",
            "resources/decision-matrices",
            "resources/ai-security",
            "resources/compliance-guides",
            "resources/cost-optimization",
            "resources/networking-deep-dives",
            "resources/migration-guides",
            "resources/postmortems",
            "resources/playlists",
            "resources/misc",
            "provider-resources",
        ],
    ),
    ("Topics", ["topics"]),
    ("About", ["docs"] + ABOUT_FILES),
]

# `resources/` is a flat drawer of ~90 files. These patterns sort them into the
# virtual groups referenced in TABS above. First match wins; the fallback is
# `resources/misc`.
RESOURCE_GROUPS: list[tuple[str, str]] = [
    (r"^cli-cheat-sheet-", "resources/cli-cheat-sheets"),
    (r"^certification-roadmap-", "resources/certification-roadmaps"),
    (r"^service-comparison-", "resources/service-comparisons"),
    (r"^decision-matrix-", "resources/decision-matrices"),
    (r"^postmortem-", "resources/postmortems"),
    (r"^playlist-", "resources/playlists"),
    (r"^(exam-day-checklist|study-strategies|practice-resources|budget-study-plan|recommended-courses)", "resources/exam-prep"),
]

# Sidebar icons.
#
# A 2,000-entry navigation where every row has identical weight is a wall of
# text. Sections and providers get an emoji so the tree can be scanned rather
# than read; individual pages deliberately do not, or the column goes back to
# being noise. The leading emoji a page's own H1 may carry is still stripped in
# title_of() for the same reason.
#
# Provider emoji are imported, not restated. build-provider-indexes.py already
# curates one per provider for the README and STUDY-HUB tables, and two hand-kept
# copies of the same mapping is how a provider ends up with a cloud in one place
# and a shield in another.
TAB_EMOJI = {
    "Learn": "🎓", "Build": "🛠️", "Certify": "🎯",
    "Reference": "📚", "Topics": "🗺️", "About": "ℹ️",
}


def _load_provider_emoji() -> dict[str, str]:
    """PROVIDER_EMOJI from build-provider-indexes.py, which is not importable by
    name because of the hyphens. Falls back to no icons rather than failing the
    build - a sidebar without emoji is a cosmetic loss, not a broken site."""
    import importlib.util

    src = Path(__file__).resolve().parent / "build-provider-indexes.py"
    try:
        spec = importlib.util.spec_from_file_location("_provider_indexes", src)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return dict(module.PROVIDER_EMOJI)
    except Exception as exc:  # noqa: BLE001 - never fail the build over an icon
        print(f"  note: provider emoji unavailable ({exc}); sidebar icons skipped")
        return {}


PROVIDER_EMOJI = _load_provider_emoji()

# Human labels for the virtual groups and for directories whose basename does not
# make a good title.
GROUP_LABELS = {
    "resources/cli-cheat-sheets": "CLI Cheat Sheets",
    "resources/certification-roadmaps": "Career Roadmaps",
    "resources/service-comparisons": "Service Comparisons",
    "resources/decision-matrices": "Decision Matrices",
    "resources/postmortems": "Postmortems",
    "resources/playlists": "Video Playlists",
    "resources/exam-prep": "Exam Prep",
    "resources/misc": "More Reference",
    "resources/hands-on-projects": "Hands-on Projects",
    "resources/architecture-patterns": "Architecture Patterns",
    "resources/well-architected": "Well-Architected",
    "resources/troubleshooting": "Troubleshooting",
    "resources/ai-security": "AI Security",
    "resources/compliance-guides": "Compliance Guides",
    "resources/cost-optimization": "Cost Optimization",
    "resources/networking-deep-dives": "Networking Deep Dives",
    "resources/practice-questions": "Practice Questions",
    "resources/interview-prep": "Interview Prep",
    "resources/migration-guides": "Migration Guides",
    "learn/day-one": "Day One",
    "learn/concepts": "Concepts",
    "provider-resources": "Provider Resource Lists",
    "exams": "All Certifications",
    "docs": "Project Docs",
    "assets": "Assets",
}

# Certification level directories sort by exam progression, not alphabetically.
LEVEL_ORDER = {
    "foundational": 0,
    "associate": 1,
    "professional": 2,
    "specialty": 3,
    "expert": 4,
    "shared": 9,
}

# Within a cert directory, the study materials have a natural reading order.
CERT_FILE_ORDER = {
    "README.md": 0,
    "fact-sheet.md": 1,
    "practice-plan.md": 2,
    "notes": 3,
    "scenarios.md": 4,
    "strategy.md": 5,
}

H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)


# --------------------------------------------------------------------------- #
# Staging
# --------------------------------------------------------------------------- #

def iter_source_files() -> list[Path]:
    """Every repo-relative path that should be staged."""
    found: list[Path] = []
    for name in ROOT_FILES + ABOUT_FILES:
        p = REPO / name
        if p.is_file():
            found.append(p)
    for d in CONTENT_DIRS:
        root = REPO / d
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(
                n
                for n in dirnames
                if n not in EXCLUDED_DIR_NAMES and (Path(dirpath) / n) not in EXCLUDED_ROOT_DIRS
            )
            for fn in sorted(filenames):
                p = Path(dirpath) / fn
                if p.suffix.lower() in STATIC_SUFFIXES or p.suffix == ".md":
                    found.append(p)
    return found


def stage() -> list[str]:
    """Copy sources into .site-src/. Returns staged paths relative to the stage."""
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    staged: list[str] = []
    for src in iter_source_files():
        rel = src.relative_to(REPO)
        parts = list(rel.parts)
        if parts[0] in STAGE_RENAMES:
            parts[0] = STAGE_RENAMES[parts[0]]
            rel = Path(*parts)
        dest = STAGE / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        staged.append(rel.as_posix())

    if SITE_CHROME.is_dir():
        for src in sorted(SITE_CHROME.rglob("*")):
            # Assets only. The chrome directory also holds home.md, which is a
            # template rendered into the stage root, not a page of its own -
            # staging it would put an orphan copy at assets/site/home.md.
            if not src.is_file() or src.suffix.lower() not in STATIC_SUFFIXES:
                continue
            rel = Path(SITE_CHROME_DEST) / src.relative_to(SITE_CHROME)
            dest = STAGE / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            staged.append(rel.as_posix())

    # IndexNow proves site ownership with /<key>.txt holding the key. The key
    # lives in the chrome dir (a .txt, so the loop above skips it) and is
    # written at the site root, the directory every page URL sits under.
    key_file = SITE_CHROME / "indexnow-key.txt"
    if key_file.is_file():
        key = key_file.read_text(encoding="utf-8").strip()
        (STAGE / f"{key}.txt").write_text(key, encoding="utf-8")
        staged.append(f"{key}.txt")

    # robots.txt at the domain root - possible since the move to the
    # cloud.noblerworks.com custom domain (2026-10-21); a github.io project page
    # has no root of its own. Sitemap URL follows site_url.
    m = re.search(r"^site_url:\s*(\S+)", (REPO / "mkdocs.yml").read_text(encoding="utf-8"), re.MULTILINE)
    if m:
        base = m.group(1).rstrip("/") + "/"
        (STAGE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n", encoding="utf-8")
        staged.append("robots.txt")
    return staged


# --------------------------------------------------------------------------- #
# Landing page
# --------------------------------------------------------------------------- #

def load_counts() -> dict[str, int]:
    """Reuse the README count checker's counting code.

    The landing page advertises the same figures the README does. Counting them
    a second time here is exactly how the two would come to disagree, so import
    the one implementation CI already runs against the README.
    """
    spec = importlib.util.spec_from_file_location("check_readme_counts", COUNTS_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.gather()


def extract_section(text: str, heading_contains: str, *, bullets: int | None = None) -> str:
    """Pull the body of one `## ...` section out of a markdown page.

    Used for "What's new": the release notes are maintained in the README and
    the CHANGELOG, and a third hand-maintained copy on the landing page would be
    the one nobody remembers to update. The heading itself is dropped - the
    landing page writes its own, without the README's decorative emoji.

    `bullets` truncates to the first N top-level list items. The README lists
    every batch; a landing page wants the recent ones and a link to the rest.
    """
    pattern = re.compile(
        rf"^##\s+[^\n]*{re.escape(heading_contains)}[^\n]*$\n(?P<body>.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return ""
    # README sections are separated by horizontal rules; the trailing one
    # belongs to the boundary, not to the section.
    body = re.sub(r"\n+---\s*$", "", match.group("body").strip())

    if bullets is None:
        return body
    kept: list[str] = []
    seen = 0
    for line in body.splitlines():
        if line.startswith("- "):
            seen += 1
            if seen > bullets:
                break
        kept.append(line)
    return "\n".join(kept).strip()


def provider_chips() -> str:
    """One list item per certification provider, busiest first."""
    data = json.loads(CERTS_JSON.read_text(encoding="utf-8"))
    providers = sorted(
        (m for m in data.get("providers", {}).values() if m.get("path")),
        key=lambda m: (-m.get("count", 0), m.get("name", "")),
    )
    return "\n".join(
        f'- [{m["name"]} <span class="n">{m.get("count", 0)}</span>]({m["path"]})'
        for m in providers
    )


def write_home_page() -> None:
    """Render the landing page over the staged copy of README.md.

    MkDocs treats a directory's README.md as its index, so replacing the staged
    copy swaps the site's home page without touching the repo's README, adding
    a second page, or changing a single link: nothing in the tree links to the
    root README anyway.

    Runs before index generation and link rewriting, so the landing page's
    directory links (`](learn/day-one/)`) are resolved by the same pass that
    handles every other page.
    """
    staged_readme = STAGE / "README.md"
    readme_text = staged_readme.read_text(encoding="utf-8") if staged_readme.is_file() else ""

    counts = load_counts()
    tokens: dict[str, object] = {
        "certifications": counts["certifications"],
        "providers": counts["providers"],
        "study_tracks": counts["study_tracks"],
        "concept_pages": counts["concept_pages"],
        "topic_indexes": counts["topic_indexes"],
        "service_comparisons": counts["service_comparisons"],
        "cli_cheat_sheets": counts["cli_cheat_sheets"],
        "architecture_patterns": counts["architecture_patterns"],
        "hands_on_projects": counts["hands_on_projects"],
        "roadmaps": counts["roadmaps"],
        "interview_prep": counts["interview_prep"],
        "words": f"{counts['words'] / 1_000_000:.1f}M",
        # A floor, like the README's, so removing a handful of links never makes
        # the page overstate itself.
        "doc_links": f"{counts['doc_links'] // 1000 * 1000:,}+",
        "provider_chips": provider_chips(),
        "whats_new": extract_section(readme_text, "What's new", bullets=3),
    }

    text = HOME_TEMPLATE.read_text(encoding="utf-8")
    for key, value in tokens.items():
        text = text.replace("{{" + key + "}}", str(value))

    unfilled = sorted(set(re.findall(r"\{\{(\w+)\}\}", text)))
    if unfilled:
        raise KeyError(f"home.md uses tokens nothing fills: {', '.join(unfilled)}")

    staged_readme.write_text(text, encoding="utf-8")


def generate_missing_indexes() -> list[str]:
    """Give every directory holding markdown a landing page.

    Directory-style links (`](../notes/)`) are used ~1,200 times across the repo
    and resolve to a directory listing on GitHub. On the site they need a real
    page. Any directory that already ships a README.md is left alone.
    """
    created: list[str] = []
    for dirpath, dirnames, filenames in os.walk(STAGE):
        dirnames[:] = sorted(dirnames)
        d = Path(dirpath)
        if d == STAGE:
            continue
        if "README.md" in filenames or "index.md" in filenames:
            continue
        md_children = sorted(f for f in filenames if f.endswith(".md"))
        # Only link subdirectories that will themselves have a landing page.
        # A directory holding nothing but static assets gets no index, so
        # linking it would emit a dead link into a generated page.
        subdirs = sorted(sd for sd in dirnames if any((d / sd).rglob("*.md")))
        if not md_children and not subdirs:
            continue

        rel = d.relative_to(STAGE)
        title = label_for_dir(rel.as_posix(), d.name)
        lines = [f"# {title}", ""]
        if subdirs:
            lines.append("## Sections")
            lines.append("")
            for sd in subdirs:
                lines.append(f"- [{label_for_dir((rel / sd).as_posix(), sd)}]({sd}/)")
            lines.append("")
        if md_children:
            if subdirs:
                lines.append("## Pages")
                lines.append("")
            for f in md_children:
                lines.append(f"- [{title_of(d / f)}]({f})")
            lines.append("")
        lines.append(
            "<!-- Generated by .github/scripts/build-site.py because this directory "
            "has no README.md. Add one to replace this page. -->"
        )
        (d / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        created.append((rel / "README.md").as_posix())
    return created


# --------------------------------------------------------------------------- #
# Link rewriting
# --------------------------------------------------------------------------- #

LINK_RE = re.compile(r"(?<=\])\(\s*(?P<target>[^)\s]+)(?P<title>\s+\"[^\"]*\")?\s*\)")
FENCE_RE = re.compile(r"^\s{0,3}(?P<marker>```+|~~~+)")
INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)*?\1", re.DOTALL)

SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "//", "/")

# Repo tooling that is deliberately not part of the site. Links to it are sent to
# GitHub rather than dropped, because the pages they point at are real.
GITHUB_BLOB = "https://github.com/PatrickWiloak/cloud-zero-to-hero/blob/main/"
OFF_SITE_PREFIXES = (".github/", ".gitignore", ".markdownlint.json", ".cspell.json", "CODEOWNERS")


def _rewrite_target(target: str, page_dir: Path) -> str:
    """Adapt one link target to how MkDocs resolves links.

    Two shapes need help. `.templates/` was staged as `templates/`, and MkDocs
    only resolves links that name a file, so the repo's ~1,200 directory links
    (`](../notes/)`, which GitHub renders as a directory listing) have to point
    at that directory's README.md instead.
    """
    if not target or target.startswith(SKIP_PREFIXES):
        return target

    anchor = ""
    if "#" in target:
        target, _, anchor_part = target.partition("#")
        anchor = "#" + anchor_part
        if not target:
            return target + anchor

    for original, staged_as in STAGE_RENAMES.items():
        if f"{original}/" in target:
            target = target.replace(f"{original}/", f"{staged_as}/")

    # Point at GitHub for the repo-tooling files the site does not publish.
    normalised = target
    while normalised.startswith(("./", "../")):
        normalised = normalised.split("/", 1)[1]
    for prefix in OFF_SITE_PREFIXES:
        if normalised.startswith(prefix):
            return GITHUB_BLOB + normalised + anchor

    # Directory links appear both with and without a trailing slash. Anything
    # that is not obviously a file gets probed against the staged tree.
    last = target.rsplit("/", 1)[-1]
    if target.endswith("/") or "." not in last:
        try:
            resolved = (page_dir / target).resolve()
            resolved.relative_to(STAGE.resolve())
        except (ValueError, OSError):
            return target + anchor
        if resolved.is_dir() and (resolved / "README.md").is_file():
            target = target.rstrip("/") + "/README.md"

    return target + anchor


def rewrite_links() -> int:
    """Fence-aware link rewrite across the staged tree. Returns files changed."""
    changed = 0
    for md_path in sorted(STAGE.rglob("*.md")):
        original = md_path.read_text(encoding="utf-8", errors="replace")
        page_dir = md_path.parent
        out_lines: list[str] = []
        fence: str | None = None

        for line in original.splitlines(keepends=True):
            m = FENCE_RE.match(line)
            if fence is not None:
                # Inside a fence: only a matching closing marker ends it.
                if m and m.group("marker")[0] == fence[0] and len(m.group("marker")) >= len(fence):
                    fence = None
                out_lines.append(line)
                continue
            if m:
                fence = m.group("marker")
                out_lines.append(line)
                continue

            # Mask inline code so link-like text inside backticks is untouched.
            spans: list[str] = []

            def _mask(mo: re.Match) -> str:
                spans.append(mo.group(0))
                return f"\x00{len(spans) - 1}\x00"

            masked = INLINE_CODE_RE.sub(_mask, line)
            masked = LINK_RE.sub(
                lambda mo: "(" + _rewrite_target(mo.group("target"), page_dir) + (mo.group("title") or "") + ")",
                masked,
            )
            restored = re.sub(r"\x00(\d+)\x00", lambda mo: spans[int(mo.group(1))], masked)
            out_lines.append(restored)

        updated = "".join(out_lines)
        if updated != original:
            md_path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


# Emoji blocks that lead this repo's headings: pictographs, dingbats and misc
# symbols, flags, plus the variation selector and ZWJ that compose them.
# Deliberately narrow - box-drawing (U+2500s) and arrows (U+2190s) can carry
# meaning, so they stay.
EMOJI_PREFIX_RE = re.compile(
    "^["
    "\U0001F000-\U0001FAFF"  # pictographs, emoticons, transport, symbols
    "\u2600-\u27BF"          # misc symbols + dingbats (warning, cloud, scales, check)
    "\u2B00-\u2BFF"          # star and friends
    "\u2139"                  # information source
    "\u23E9-\u23FA"          # timers and playback
    "\uFE0F\u200D"           # variation selector-16, zero-width joiner
    "\U0001F1E6-\U0001F1FF"  # regional indicator pairs (flags)
    "]+[ \t]+"
)
ATX_HEADING_RE = re.compile(r"^(?P<hashes>#{1,6}) +(?P<text>.+?) *$")


def strip_heading_emoji() -> int:
    """Site-only: drop the leading emoji a heading may carry, keeping its anchor.

    On GitHub an emoji-led heading is house style; on the site it reads like a
    rendered README, so the staged copy loses the prefix. The catch is anchors:
    the toc slugifier is configured to match GitHub's, where "## 🎯 Quick
    Navigation" slugs to `#-quick-navigation` (the emoji leaves a leading
    hyphen), and ~960 inbound links across the tree were written against that.
    So each stripped heading pins its ORIGINAL slug as an explicit attr_list id
    - computed with the same pymdownx slugifier mkdocs.yml hands to toc - and
    no anchor changes. toc de-duplicates explicit ids in document order exactly
    as it does generated ones, so repeated headings on a page keep today's
    suffixes too. The sidebar's section and provider landmarks are nav labels,
    not headings, and are unaffected.

    Headings containing links, attr_lists or raw HTML are left alone: their
    rendered text (which is what toc slugs) diverges from the source text, so
    the pinned id could be wrong. None of them lead with emoji today.
    """
    from pymdownx.slugs import slugify

    slug = slugify(case="lower")
    changed = 0
    for md_path in sorted(STAGE.rglob("*.md")):
        original = md_path.read_text(encoding="utf-8", errors="replace")
        out_lines: list[str] = []
        fence: str | None = None
        dirty = False

        for line in original.splitlines(keepends=True):
            m = FENCE_RE.match(line)
            if fence is not None:
                if m and m.group("marker")[0] == fence[0] and len(m.group("marker")) >= len(fence):
                    fence = None
                out_lines.append(line)
                continue
            if m:
                fence = m.group("marker")
                out_lines.append(line)
                continue

            hm = ATX_HEADING_RE.match(line.rstrip("\n"))
            if hm and "](" not in hm.group("text") and "{" not in hm.group("text") and "<" not in hm.group("text"):
                text = hm.group("text")
                stripped = EMOJI_PREFIX_RE.sub("", text)
                if stripped and stripped != text:
                    anchor = slug(text, "-")
                    eol = "\n" if line.endswith("\n") else ""
                    # An H1 becomes the page's nav label, and MkDocs keeps the
                    # attr_list text in that label ("Glossary {: -glossary }"), so
                    # page titles get no pinned id - nothing links to an H1 anchor.
                    pin = "" if hm.group("hashes") == "#" else f" {{: #{anchor} }}"
                    out_lines.append(f"{hm.group('hashes')} {stripped}{pin}{eol}")
                    dirty = True
                    continue
            out_lines.append(line)

        if dirty:
            md_path.write_text("".join(out_lines), encoding="utf-8")
            changed += 1
    return changed


# --------------------------------------------------------------------------- #
# Labels
# --------------------------------------------------------------------------- #

_title_cache: dict[Path, str] = {}
_cert_labels: dict[str, str] = {}
_provider_labels: dict[str, str] = {}


def load_cert_labels() -> None:
    """Use certs.json for cert and provider display names in the nav."""
    if not CERTS_JSON.is_file():
        return
    data = json.loads(CERTS_JSON.read_text(encoding="utf-8"))
    for cert in data.get("certs", []):
        path, name = cert.get("path"), cert.get("name")
        if path and name:
            _cert_labels[path.rstrip("/")] = name
    for meta in data.get("providers", {}).values():
        path, name = meta.get("path"), meta.get("name")
        if path and name:
            _provider_labels[path.rstrip("/")] = name


def prettify(stem: str) -> str:
    words = stem.replace("_", "-").split("-")
    small = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "with"}
    acronyms = {
        "ai", "api", "aws", "cd", "ci", "cli", "cncf", "dns", "gcp", "genai", "gpu", "iam",
        "iac", "k8s", "llm", "llms", "mcp", "ml", "nvidia", "rag", "sre", "sql", "ssl", "tls", "vpc",
    }
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if lw in acronyms:
            out.append(lw.upper())
        elif i > 0 and lw in small:
            out.append(lw)
        else:
            out.append(w[:1].upper() + w[1:] if w else w)
    return " ".join(out)


def title_of(path: Path) -> str:
    """Prefer the page's H1; fall back to a prettified filename."""
    if path in _title_cache:
        return _title_cache[path]
    title = ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        body = FRONTMATTER_RE.sub("", text)
        m = H1_RE.search(body)
        if m:
            title = m.group(1)
    except OSError:
        pass
    if not title:
        title = prettify(path.stem)
    # Nav labels are one line in a narrow column: drop decoration and trailing
    # parentheticals that only repeat the exam code already shown on the page.
    title = re.sub(r"[#*`]", "", title).strip()
    title = re.sub(r"^[^\w(]+\s*", "", title)  # leading emoji or symbols
    title = re.sub(r"\s+", " ", title)
    if len(title) > 72:
        title = title[:69].rstrip() + "..."
    _title_cache[path] = title
    return title


def label_for_dir(rel_posix: str, basename: str) -> str:
    label = _label_for_dir(rel_posix, basename)
    emoji = PROVIDER_EMOJI.get(rel_posix.removeprefix("exams/")) if rel_posix.startswith("exams/") else None
    return f"{emoji} {label}" if emoji else label


def _label_for_dir(rel_posix: str, basename: str) -> str:
    if rel_posix in GROUP_LABELS:
        return GROUP_LABELS[rel_posix]
    if rel_posix in _cert_labels:
        return _cert_labels[rel_posix]
    if rel_posix in _provider_labels:
        return _provider_labels[rel_posix]
    if basename in LEVEL_ORDER:
        return basename.capitalize()
    return prettify(basename)


# --------------------------------------------------------------------------- #
# Navigation
# --------------------------------------------------------------------------- #

def sort_key_for(rel_posix: str, basename: str, is_dir: bool) -> tuple:
    """Reading order: level dirs by progression, cert files by study order."""
    if basename in LEVEL_ORDER:
        return (0, LEVEL_ORDER[basename], basename.lower())
    if basename in CERT_FILE_ORDER:
        return (0, CERT_FILE_ORDER[basename], basename.lower())
    if basename.rstrip(".md") in CERT_FILE_ORDER:
        return (0, CERT_FILE_ORDER[basename.rstrip(".md")], basename.lower())
    # Numbered notes (01-foo.md) sort naturally by their prefix.
    m = re.match(r"^(\d+)[-_]", basename)
    if m:
        return (1, int(m.group(1)), basename.lower())
    return (2, 0, label_for_dir(rel_posix, basename).lower() if is_dir else basename.lower())


def build_dir_nav(dirpath: Path) -> list:
    """Recursively turn a staged directory into a MkDocs nav list."""
    rel_dir = dirpath.relative_to(STAGE).as_posix()
    entries: list[tuple[tuple, object]] = []

    readme = dirpath / "README.md"
    children: list = []
    if readme.is_file():
        # navigation.indexes renders a bare path first in a section as its landing page.
        children.append((readme.relative_to(STAGE)).as_posix())

    for child in sorted(dirpath.iterdir()):
        name = child.name
        if name in EXCLUDED_DIR_NAMES:
            continue
        rel = child.relative_to(STAGE).as_posix()
        if child.is_dir():
            sub = build_dir_nav(child)
            if sub:
                entries.append((sort_key_for(rel, name, True), {label_for_dir(rel, name): sub}))
        elif child.suffix == ".md":
            if name == "README.md":
                continue
            entries.append((sort_key_for(rel, name, False), {title_of(child): rel}))

    entries.sort(key=lambda e: e[0])
    children.extend(item for _, item in entries)
    return children


def resource_group_of(filename: str) -> str:
    for pattern, group in RESOURCE_GROUPS:
        if re.match(pattern, filename):
            return group
    return "resources/misc"


def build_resource_groups() -> dict[str, list]:
    """Bucket the flat files directly inside resources/ into virtual groups."""
    groups: dict[str, list[tuple[str, str]]] = {}
    res = STAGE / "resources"
    if not res.is_dir():
        return {}
    for child in sorted(res.iterdir()):
        if not child.is_file() or child.suffix != ".md":
            continue
        if child.name == "README.md":
            continue
        group = resource_group_of(child.name)
        groups.setdefault(group, []).append((title_of(child), child.relative_to(STAGE).as_posix()))
    return {g: [{t: p} for t, p in sorted(items)] for g, items in groups.items()}


def build_nav() -> list:
    resource_groups = build_resource_groups()
    nav: list = ["README.md"]

    for tab_name, members in TABS:
        section: list = []
        for member in members:
            if member in resource_groups:
                section.append({GROUP_LABELS.get(member, prettify(Path(member).name)): resource_groups[member]})
                continue
            path = STAGE / member
            if path.is_dir():
                sub = build_dir_nav(path)
                if not sub:
                    continue
                # A tab with a single directory member (Learn, Topics) reads better
                # flattened than nested one level deeper under its own name.
                if len(members) == 1:
                    section.extend(sub)
                else:
                    section.append({label_for_dir(member, path.name): sub})
            elif path.is_file() and path.suffix == ".md":
                section.append({title_of(path): member})
        if section:
            emoji = TAB_EMOJI.get(tab_name)
            nav.append({f"{emoji} {tab_name}" if emoji else tab_name: section})
    return nav


def dump_nav(nav: list, indent: int = 2) -> str:
    """Emit nav as YAML. Written by hand so the base config's `!!python/name:`
    tags survive: the config is treated as text and never round-tripped."""
    lines: list[str] = []

    def quote(s: str) -> str:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

    def walk(items: list, depth: int) -> None:
        pad = " " * (depth * indent)
        for item in items:
            if isinstance(item, str):
                lines.append(f"{pad}- {item}")
            elif isinstance(item, dict):
                (title, value), = item.items()
                if isinstance(value, str):
                    lines.append(f"{pad}- {quote(title)}: {value}")
                else:
                    lines.append(f"{pad}- {quote(title)}:")
                    walk(value, depth + 1)

    lines.append("nav:")
    walk(nav, 1)
    return "\n".join(lines) + "\n"


# Pages deliberately built and searchable but kept out of the nav: they document
# the asset directories for contributors rather than teaching anything.
NAV_EXEMPT = {"assets/README.md", "assets/diagrams/README.md"}


def nav_coverage(nav: list) -> list[str]:
    """Staged pages that no nav entry points at.

    Without this, adding a directory the TABS table does not mention drops its
    pages out of the navigation silently: MkDocs only reports the first few and
    only at INFO level, so it never fails a build.
    """
    referenced: set[str] = set()

    def walk(items: list) -> None:
        for item in items:
            if isinstance(item, str):
                referenced.add(item)
            elif isinstance(item, dict):
                (_, value), = item.items()
                if isinstance(value, str):
                    referenced.add(value)
                else:
                    walk(value)

    walk(nav)
    staged = {p.relative_to(STAGE).as_posix() for p in STAGE.rglob("*.md")}
    return sorted(staged - referenced - NAV_EXEMPT)


def count_entries(nav: list) -> int:
    n = 0
    for item in nav:
        if isinstance(item, str):
            n += 1
        elif isinstance(item, dict):
            (_, value), = item.items()
            n += 1 if isinstance(value, str) else count_entries(value)
    return n


# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true", help="treat MkDocs warnings as errors")
    ap.add_argument("--serve", action="store_true", help="stage, then run mkdocs serve")
    ap.add_argument("--stage-only", action="store_true", help="stage and generate config, skip the build")
    args = ap.parse_args()

    load_cert_labels()

    print("Staging content into .site-src/ ...")
    staged = stage()
    md = sum(1 for p in staged if p.endswith(".md"))
    print(f"  staged {len(staged)} files ({md} markdown, {len(staged) - md} static)")

    if not HOME_TEMPLATE.is_file():
        print(f"ERROR: missing landing page template {HOME_TEMPLATE.relative_to(REPO)}", file=sys.stderr)
        return 1
    write_home_page()
    print(f"  rendered the landing page from {HOME_TEMPLATE.relative_to(REPO)}")

    created = generate_missing_indexes()
    print(f"  generated {len(created)} directory index pages")

    de_emojied = strip_heading_emoji()
    print(f"  stripped leading heading emoji in {de_emojied} pages (anchors pinned)")

    rewritten = rewrite_links()
    print(f"  rewrote links in {rewritten} pages")

    print("Generating navigation ...")
    nav = build_nav()
    print(f"  {count_entries(nav)} nav entries")

    orphans = nav_coverage(nav)
    if orphans:
        print(f"ERROR: {len(orphans)} staged pages are not reachable from the nav.", file=sys.stderr)
        print("Add the directory to TABS in this script, or to NAV_EXEMPT if that is intended:", file=sys.stderr)
        for o in orphans[:20]:
            print(f"  - {o}", file=sys.stderr)
        if len(orphans) > 20:
            print(f"  ... and {len(orphans) - 20} more", file=sys.stderr)
        return 1

    base = BASE_CONFIG.read_text(encoding="utf-8")
    if re.search(r"^nav:", base, re.MULTILINE):
        print("ERROR: mkdocs.yml defines `nav`; it must be generated here.", file=sys.stderr)
        return 1
    banner = (
        "\n# ---------------------------------------------------------------------\n"
        "# GENERATED by .github/scripts/build-site.py. Do not edit; edit the\n"
        "# generator or mkdocs.yml instead. This file is gitignored.\n"
        "# ---------------------------------------------------------------------\n"
    )
    GENERATED_CONFIG.write_text(base + banner + dump_nav(nav), encoding="utf-8")
    print(f"  wrote {GENERATED_CONFIG.relative_to(REPO)}")

    if args.stage_only:
        return 0

    mkdocs = REPO / ".venv-docs" / "bin" / "mkdocs"
    cmd = [str(mkdocs) if mkdocs.exists() else "mkdocs"]
    cmd += ["serve"] if args.serve else ["build", "--clean"]
    cmd += ["-f", str(GENERATED_CONFIG)]
    if args.strict:
        cmd.append("--strict")

    print(f"Running: {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=REPO)


if __name__ == "__main__":
    sys.exit(main())
