# Automation reference: `.github/` scripts and workflows

This directory holds CI workflows, validation scripts, and contributor templates. Everything here exists to keep the repo's content honest at scale (160+ cert dirs, 1000+ markdown files).

## At a glance

```
.github/
├── README.md                 # this file
├── PULL_REQUEST_TEMPLATE.md  # auto-applied to new PRs
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   ├── cert_request.md
│   └── content_suggestion.md
├── site/                     # site chrome (not repo content)
│   ├── extra.css             # site-only styling
│   ├── home.md               # the site's landing page, rendered over the staged README
│   └── indexnow-key.txt      # IndexNow ownership key, served at the site root as <key>.txt
├── site-overrides/           # Material template overrides (head tags, JSON-LD, nav partial)
├── workflows/                # GitHub Actions CI gates
│   ├── cspell.yml
│   ├── docs-site.yml
│   ├── link-check.yml
│   ├── markdown-lint.yml
│   └── structure-validate.yml
└── scripts/                  # local-runnable validators + helpers
    ├── build-certs-index.py
    ├── build-flashcards.py
    ├── build-site.py
    ├── build-freshness-ledger.sh
    ├── build-lab-map.py
    ├── build-provider-indexes.py
    ├── check-cert-freshness.py
    ├── check-code-fences.py
    ├── check-internal-links.py
    ├── check-orphan-links.sh
    ├── glossary-add-anchors.py
    ├── glossary-autolink.py
    ├── glossary-upgrade-existing-links.py
    ├── notify-indexnow.py
    ├── site_hooks.py
    ├── validate-cert-structure.sh
    └── validate-frontmatter.sh
```

The root `CODEOWNERS` and `.editorconfig` files complement this directory.

## Workflows

GitHub Actions run on PR, push to main, and a weekly schedule. All four are designed to be informative rather than punitive - the structure validator and link-check are the only ones that gate merging.

| Workflow | Triggers | What it does | Strict? |
|---|---|---|---|
| `link-check.yml` | PR, push, weekly Mondays | Two jobs. **Internal** runs `check-internal-links.py` and blocks the merge. **External** runs lychee (`cloud.ibm.com` excluded: its docs answer lychee with bot-wall 404s but load in a browser) and, on the weekly run, opens one rolling auto-issue or updates the open `link-check` issue in place. | Internal: yes. External: no (vendor URL rot is not a contributor's fault) |
| `markdown-lint.yml` | PR, push | Runs `markdownlint-cli2` against `.markdownlint.json` config | Yes |
| `structure-validate.yml` | PR, push | Runs `validate-cert-structure.sh`, `validate-frontmatter.sh`, `--check` on the generators, `check-code-fences.py`, and `check-internal-links.py` (links plus heading anchors) | Yes (fails on missing required files, malformed frontmatter, or stale generated files; warns are advisory) |
| `cspell.yml` | PR, push to `**/*.md` | Spell-checks against `.cspell.json` | No (currently non-strict; will flip once dictionary is tuned) |
| `docs-site.yml` | PR, push to main, manual | Builds the published site with `build-site.py --strict`. Deploys to GitHub Pages on push to main, then sends the changed page URLs to IndexNow (`notify-indexnow.py`, continue-on-error). | Yes (fails on a broken relative link, a missing heading anchor, or a page no nav entry reaches) |

> **One-time setup for deployment.** Settings > Pages > Build and deployment > Source must be set to **GitHub Actions**. Until then the build job passes and the deploy job fails.

## Scripts

All scripts are runnable locally. They print human-readable output and exit non-zero on failure. None of them mutate files except where noted.

### Validators (also run in CI)

**`validate-cert-structure.sh`**
Walks `exams/<provider>/<cert>/` directories, discovered by the presence of `fact-sheet.md`. Discovery deliberately does not key off a `notes/` subdir: that skipped every cert whose notes were still undrafted, which are the ones most likely to be incomplete. Hard-fails on missing `README.md`. Warns on missing `fact-sheet.md`, `practice-plan.md`, and (for senior-tier certs only) `scenarios.md` + `strategy.md`. Tier classification: senior = path contains `/professional/`, `/specialty/`, `/expert/`, OR matches a curated cert-basename list. Junior tiers don't get scenarios + strategy warnings.

```bash
bash .github/scripts/validate-cert-structure.sh
```

**`validate-frontmatter.sh`**
Validates YAML frontmatter on a defined set of file groups: concept pages, day-one pages, top-level learn pages, hands-on projects, cert fact-sheets, topic indexes, architecture patterns, networking deep dives, and decision-matrix / postmortem / playlist files. Fails on malformed YAML or bad date format. Warns on missing `last-updated` or stale (>180 days) entries.

```bash
bash .github/scripts/validate-frontmatter.sh
```

**`build-freshness-ledger.sh`**
Regenerates `docs/freshness.md` from `last-updated` frontmatter across the same file groups. Sections: cert fact-sheets, concept pages, hands-on projects, topic indexes. Run after meaningful content updates.

```bash
bash .github/scripts/build-freshness-ledger.sh > docs/freshness.md
```

**`check-orphan-links.sh`**
Lists `.md` files with zero inbound links from other markdown. Useful before retiring or moving a file. Manual one-shot, not a workflow gate. Recognizes that cert `notes/*.md` are covered by their parent cert dir's links.

```bash
bash .github/scripts/check-orphan-links.sh
```

### Index generators (also run in CI)

**`build-certs-index.py`**
Parses every `exams/**/fact-sheet.md` into `docs/certs.json`: exam code, level, status, duration, cost, passing score, notes count, and which standard files exist. This file is the source of truth for anything that counts or lists certs. Fields that cannot be parsed are `null` rather than guessed, because a wrong value would propagate into every generated table.

```bash
python3 .github/scripts/build-certs-index.py            # write docs/certs.json
python3 .github/scripts/build-certs-index.py --report   # per-field fill rates
python3 .github/scripts/build-certs-index.py --check    # CI mode: fail if stale
```

Status is derived: `retired` and `anticipated` from the README banner, `outline` when no notes are drafted, otherwise `active`.

**`build-provider-indexes.py`**
Generates the per-provider index tables in `exams/<provider>/README.md`, the provider table in `STUDY-HUB.md`, and the "Browse Certifications" table in `README.md`, all from `docs/certs.json`. Only the block between the `<!-- BEGIN GENERATED: ... -->` markers is replaced, so the hand-written editorial content in the six curated provider READMEs survives regeneration.

Two things stay curated in the script: the one-line "Highlights" blurb per provider (`PROVIDER_HIGHLIGHTS`, shared by both tables so they cannot describe a provider differently) and the row icon (`PROVIDER_EMOJI`). The script refuses to run if a provider in `certs.json` is missing either, so a new provider fails CI instead of rendering as a blank row - which is how the README table came to be missing five providers for five days.

```bash
python3 .github/scripts/build-provider-indexes.py
python3 .github/scripts/build-provider-indexes.py --check
```

**`check-readme-counts.py`**
Verifies every counted claim in `README.md` against the tree: the badge counts, the "What's Inside" list, the Repository Statistics block, the repository-structure comments, the word count (within a 0.2M tolerance), and the doc-link floor. Counts come from `git ls-files`, never a filesystem walk - a local site build leaves a full staged copy of the tree in `.site-src/`, and walking the working directory counts every page twice.

The per-provider table is deliberately out of scope: it is generated by `build-provider-indexes.py` and checked there. One table, one owner.

`.github/site/home.md`, the site's landing page, is filled from the same `gather()` function, so the site and the README cannot disagree.

```bash
python3 .github/scripts/check-readme-counts.py           # report drift
python3 .github/scripts/check-readme-counts.py --fix     # rewrite the numbers
python3 .github/scripts/check-readme-counts.py --check   # CI mode: fail on drift
```

Add an entry to `CLAIMS` whenever the README gains a counted claim. A number no script checks is a number that will be wrong within a month.

**`check-internal-links.py`**
Verifies every relative markdown link (and every plain HTML `<a href="...">` anchor, as used in the concept pages' "Check yourself" answers) resolves on disk, and that a `#fragment` (also a bare same-page `#fragment`) names a heading id that exists on the target page. Heading ids are computed with the site's rules, not GitHub's guess: `pymdownx.slugs.slugify(case="lower")`, Python-Markdown's `_1` duplicate suffix, explicit `{: #id }` ids (which toc reserves first) and `<a id>` ids (a raw id inside a heading is not reserved), `pymdownx.smartsymbols` (`1/4` becomes a fraction character in the slug), and `build-site.py`'s emoji handling (a non-H1 heading keeps its pinned emoji-hyphen slug; an H1 is slugged from the stripped text). Anchors on the root `README.md` are not checked, because the site renders it from `.github/site/home.md`. Skips fenced code blocks, inline code spans (also for HTML anchors), external schemes, and `<placeholder>` targets. Blocking in CI (`link-check.yml` and `structure-validate.yml`). The strict site build stays the ground truth: when the two disagree, fix the checker (`--self-test` holds fixture cases).

```bash
python3 .github/scripts/check-internal-links.py
python3 .github/scripts/check-internal-links.py --self-test
```

**`check-code-fences.py`**
Fails on any tracked `.md` file with an unclosed ``` or ~~~ fence and prints `file:line` of the opening fence. Follows CommonMark: a closer must use the same character and be at least as long as the opener, fences may be indented (list items) or sit in blockquotes, and a line such as ```` ```code``` ```` is inline code. Skips `site/`, `.site-src/`, `node_modules/`. Blocking in CI.

```bash
python3 .github/scripts/check-code-fences.py
python3 .github/scripts/check-code-fences.py --self-test
```

**`build-lab-map.py`**
Reads the `certs:` frontmatter list from each `resources/hands-on-projects/*.md` and generates two views: a lab-to-cert table in the projects README, and the reverse index at `resources/hands-on-projects/labs-by-cert.md`. Cert IDs are validated against `docs/certs.json`, so a typo fails the run instead of producing a dead link. Blocking in CI.

**`build-flashcards.py`**
Writes `flashcards.csv` (Anki-importable) into each cert dir. Cards are extracted, never invented: exam logistics come from `docs/certs.json`, and term-definition cards come from the `- **Term** - definition` lines the notes already use. Certs yielding fewer than 15 cards get no deck and are listed in the report. Decks are capped at 300 cards with an explicit in-deck note when truncated. Blocking in CI.

```bash
python3 .github/scripts/build-flashcards.py --report   # counts, no writes
```

**`check-cert-freshness.py`**
Advisory. Reports which cert guides are due for re-verification, using a per-provider monthly rotation so the whole repo does not fall due on one day. Also warns when a fact-sheet declares `exam-version:` / `exam-retires:` frontmatter and the retirement date is near.

```bash
python3 .github/scripts/check-cert-freshness.py --due     # just this month's batch
python3 .github/scripts/check-cert-freshness.py --month 3 # preview another month
```

### Site build (also runs in CI)

**`build-site.py`**
Builds the published MkDocs Material site from the markdown tree without restructuring it. Stages the content into `.site-src/`, renders `.github/site/home.md` over the staged root `README.md` as the site's landing page, generates a landing page for any directory holding markdown but no `README.md`, rewrites directory-style links (`](../notes/)`) to point at that directory's `README.md`, and generates the entire navigation from the staged tree using `docs/certs.json` for cert and provider labels.

Fails if any staged page is unreachable from the navigation, which is what stops a new top-level directory from silently vanishing from the site. `--strict` additionally turns every MkDocs link and anchor warning into an error.

Requires the pinned toolchain in `requirements-docs.txt`. Writes `.site-src/`, `mkdocs.generated.yml`, and `site/`, all gitignored.

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r requirements-docs.txt

.venv-docs/bin/python .github/scripts/build-site.py --serve    # live preview
.venv-docs/bin/python .github/scripts/build-site.py --strict   # what CI runs
```

**`site_hooks.py`** (MkDocs hook, loaded via `hooks:` in `mkdocs.yml`)
Sets per-page search metadata at build time, without touching the markdown: a `<meta name="description">` from the page's first prose paragraph (or, for cert landing pages, fact sheets, plans, scenarios and strategy pages, a summary built from `docs/certs.json`), a `<title>` of the page's H1 with the exam code appended inside a cert directory, schema.org BreadcrumbList JSON-LD on every page, and `noindex` on working files (`TODO.md`, `CLAUDE.md`, dated reports). Until 2026-09-28 all ~2,000 pages shared one description. A frontmatter `description:` on a page overrides the generated one.

**`notify-indexnow.py`**
Runs after each deploy. Maps the markdown files changed in the push to their site URLs and submits them to IndexNow (Bing, Yandex, and through Bing, DuckDuckGo and ChatGPT search). A change to anything rendered on every page (`mkdocs.yml`, the overrides, the hooks, `build-site.py`, `extra.css`) submits every URL in the sitemap. `--all` does the same by hand; `--dry-run` prints without sending. It diffs git rather than sitemaps because MkDocs stamps every sitemap `lastmod` with the build date.

Configuration lives in the root `mkdocs.yml`, which deliberately has no `nav` key. See [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md#the-published-site) for the design and its conventions.

### Glossary autolink (mutates files)

These three scripts work as a pipeline. Run them in order when the glossary gains new terms or when adding a new content directory to the autolink scope.

**`glossary-add-anchors.py`** - prepends `<a id="term-slug"></a>` to each bolded term in `learn/glossary.md` so links can target individual terms (not just section headers). Idempotent; safe to re-run.

**`glossary-autolink.py`** - parses the glossary for bolded terms (335 found) and links the first occurrence in scoped pages. Caps at 5 links per file. Skips code blocks, headings, existing links. Scope (`TARGET_DIRS` + `TARGET_FILES`):
- `learn/concepts/`
- `topics/`
- `resources/hands-on-projects/`
- `resources/architecture-patterns/`
- `resources/networking-deep-dives/`
- `resources/decision-matrix-*.md`
- `resources/postmortem-*.md`
- `resources/playlist-*.md`

**`glossary-upgrade-existing-links.py`** - upgrades old section-level glossary links (`glossary.md#cloud-fundamentals`) to per-term anchors (`glossary.md#term-availability-zone`) when a term anchor is available. Run after `glossary-add-anchors.py` adds new anchors.

```bash
python3 .github/scripts/glossary-add-anchors.py
python3 .github/scripts/glossary-autolink.py
python3 .github/scripts/glossary-upgrade-existing-links.py
```

## Templates

- `PULL_REQUEST_TEMPLATE.md` - auto-applied to new PRs. Matches the "in scope / out of scope" framing from `CONTRIBUTING.md`. Contributors edit it down to a checklist of what they actually verified.
- `ISSUE_TEMPLATE/bug_report.md` - for broken links, factual errors, doc drift.
- `ISSUE_TEMPLATE/content_suggestion.md` - for proposing new pages, expanded coverage, missing cross-links.
- `ISSUE_TEMPLATE/cert_request.md` - for proposing a new cert scaffold (open before doing the work, to confirm scope).

## Conventions

- **Scripts are bash or python3**. No external runtime deps (no Node, no npm). The CI workflows install whatever the underlying linter needs (lychee binary, cspell via npx, etc.).
- **Validators print path + reason on failure** so you can grep the output and fix in order.
- **Mutating scripts are idempotent**. Re-running them is always safe.
- **Output is plain text**, not JSON. These scripts are meant to be read by humans.

## When to update what

| Trigger | What to update |
|---|---|
| New cert added | Add `fact-sheet.md`, then run `build-certs-index.py`, `build-provider-indexes.py`, `build-flashcards.py`, and `check-readme-counts.py --fix` so counts, tables, and decks regenerate. If it's a new senior tier, add it to the curated senior-cert list in `validate-cert-structure.sh` |
| Any counted content added or removed | Run `check-readme-counts.py --fix`. If you added a *new* counted claim to the README, add a matching `CLAIMS` entry first |
| New hands-on project | Add a `certs:` list to its frontmatter, then run `build-lab-map.py` |
| Cert notes edited | Re-run `build-flashcards.py`; the deck is derived from the notes |
| New provider added | Add a display name to `PROVIDER_NAMES`, a highlights line to `PROVIDER_HIGHLIGHTS`, and an icon to `PROVIDER_EMOJI`, then regenerate. Both provider tables and the provider index pick it up automatically. The generator refuses to run until all three exist |
| Cert renamed, retired, or its fact-sheet edited | Re-run both generators. `structure-validate.yml` fails with the exact command if you forget |
| New concept / hands-on / topic page | Add `last-updated` frontmatter; rerun `build-freshness-ledger.sh` |
| New content shape (matrix / postmortem / playlist / etc.) | Add the file path glob to `validate-frontmatter.sh` and `glossary-autolink.py` |
| New glossary term | Run `glossary-add-anchors.py` then `glossary-autolink.py` |
| New common false positive in cspell | Add to `.cspell.json` words list |
