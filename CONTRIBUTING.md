# Contributing

Thanks for your interest in improving this repo. It's a markdown knowledge base for cloud - AWS, Azure, GCP, OCI, Kubernetes, Linux, networking, Terraform, DevOps, SRE and FinOps: concepts, hands-on builds, references, and certification prep. The goal is accurate, well-linked, exam-aligned material that respects readers' time. Plain-English, no fluff.

## What kinds of contributions are welcome

- **Typo / grammar fixes** in any markdown file.
- **Broken-link repairs** when AWS, Azure, GCP, or other vendors reorganize their docs.
- **Doc-link additions**: high-quality vendor documentation links that strengthen an existing section.
- **Domain-weight or exam-detail updates** when a vendor publishes a refreshed exam blueprint.
- **New cert scaffolds** for missing in-demand certifications (open an issue first to confirm scope and naming).
- **Resource updates**: better practice questions, scenarios, or hands-on lab walkthroughs.
- **Roadmap additions** for under-served career paths.
- **`learn/` content**: new concept pages (`learn/concepts/<topic>.md`), day-one onramp expansions, glossary additions. Keep concept pages 5-10 minute reads, plain English, no exam framing.
- **Wrong-site content goes to the sibling repo.** Data, security and AI material belongs in [data-zero-to-hero](https://github.com/PatrickWiloak/data-zero-to-hero), [security-zero-to-hero](https://github.com/PatrickWiloak/security-zero-to-hero) or [ai-zero-to-hero](https://github.com/PatrickWiloak/ai-zero-to-hero). Link to it from here with an absolute URL rather than copying it in.
- **Diagrams**: inline Mermaid in the page that needs it (the default), or a PNG under `assets/diagrams/<topic>/` when the diagram is too dense to read inline. See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md#visual-content-standards).

## What is out of scope

- **Marketing / SEO content** or affiliate links.
- **Paid course advertising** beyond what is already in `resources/recommended-courses.md`.
- **Verbatim copies** of vendor exam questions (legal and ethical violation - do not submit, do not request).
- **Generated/AI-written notes** that don't match the structured pattern below.

## Repository layout

```
exams/<provider>/<cert-dir>/
    README.md           # cert overview, who it's for, prereqs, study time
    fact-sheet.md       # exam details, domains, key services, doc links
    notes/              # numbered topic files: 01-foo.md, 02-bar.md, ...
    practice-plan.md    # weekly study schedule with checkboxes
    scenarios.md        # exam-style scenarios with explanations (optional but recommended)
    strategy.md         # exam day approach, time allocation (optional)
learn/
    concepts/           # bite-size topic pages (5-10 min reads), cloud primitives
    day-one/            # strict beginner on-ramp (terminal, git, HTTP, servers)
    cloud-from-scratch.md  # 8-phase non-cert cloud path
    glossary.md         # term reference
    youtube.md          # curated video resources
resources/
    architecture-patterns/      # multi-cloud architecture write-ups
    certification-roadmap-*.md  # career-focused learning paths
    cli-cheat-sheet-*.md        # tool quick references
    cost-optimization/          # per-cloud cost playbooks
    decision-matrix-*.md        # score-driven product picks (IaC tool)
    hands-on-projects/          # guided builds
    interview-prep/             # role-based interview prep
    migration-guides/           # cloud migration playbooks
    networking-deep-dives/      # hybrid, multi-cloud, DNS, load balancing
    playlist-*.md               # persona reading sequences (SRE, etc.)
    postmortem-*.md             # real-incident study guides mapped to cert domains
    practice-questions/         # per-cert question banks
    service-comparison-*.md     # cross-cloud service comparisons
    troubleshooting/            # per-platform troubleshooting
    well-architected/           # AWS, Azure, GCP frameworks
topics/                 # cross-pillar topic indexes (one per major subject area)
assets/diagrams/        # PNG diagrams (draw.io exports), organized by topic
README.md           # top-level overview and provider table
STUDY-HUB.md        # navigation hub with decision tree and roadmaps
CLAUDE.md           # project-level guidance for AI-assisted edits
```

## Cert directory template

When scaffolding a new cert, use this structure:

- `README.md` - 1-page overview. Include exam code, level (Associate / Professional / Specialty / etc.), brief audience description, prerequisites, recommended study time, and a "Study Materials in This Guide" table linking to the other files in the dir.
- `fact-sheet.md` - dense reference. Lead with a Quick Reference table (exam code, duration, questions, passing score, cost, validity, prerequisites, delivery format), then domain breakdown with weights, then deep service / topic coverage with embedded vendor doc links.
- `notes/` - one numbered file per major exam domain or topic cluster. Aim for 4-7 files. File names are kebab-case with a `NN-` prefix (e.g. `01-data-ingestion.md`).
- `practice-plan.md` - week-by-week schedule (typically 4-12 weeks depending on tier) with checkbox milestones.
- `scenarios.md` - 10-25 exam-style scenarios with full explanations. Map each to a domain.
- `strategy.md` (optional, recommended for Professional/Specialty) - exam-day timing, common traps, how to pace.

Keep early files (`README.md`, `fact-sheet.md`) compact and accurate. Depth lives in `notes/`.

## New content shapes

The repo has a few specialized content shapes beyond the core cert dirs and concept pages. Each follows a stable template - if you author a new one, match the existing pattern.

- **`resources/decision-matrix-*.md`** - score-driven product picks. Lead paragraph (when you'd reach for this matrix), criteria-by-product table, per-product strengths / limitations, default pick, alternatives by use case. Examples: `decision-matrix-vector-database.md`, `decision-matrix-iac-tool.md`, `decision-matrix-llm-serving.md`.
- **`resources/postmortem-*.md`** - real-incident study guides. Lead paragraph (incident summary in one sentence), timeline, root cause, what would have caught it, mapped cert exam domains, lessons cross-linked to repo concepts. Examples: `postmortem-aws-s3-2017.md`, `postmortem-cloudflare-regex-2019.md`, `postmortem-gcp-networking-2019.md`.
- **`resources/playlist-*.md`** - persona reading sequences. Frontmatter with `persona` + `time-budget`, ordered list of repo links with one-sentence justifications, "what you'll be able to do at the end" summary. Examples: `playlist-ai-engineer-30min.md`, `playlist-sre-1hour.md`.
- **`topics/<topic>.md`** - cross-pillar topic index. Mermaid "topic at a glance" diagram, then sections linking Learn / Compare / Reference / Build / Certify pages relevant to that topic. Existing topics: finops, kubernetes, networking, observability, platform-engineering, serverless, sre-and-reliability.

## Documentation link format

Always prefer **official vendor documentation** over third-party tutorials. The standard format used throughout the repo is:

```
**[📖 Link Text](URL)** - Optional short description
```

For example:

```markdown
**[📖 RDS Documentation](https://docs.aws.amazon.com/rds/)** - Complete RDS guide
```

Other conventions:

- Use markdown links, not bare URLs.
- For internal repo links, use relative paths: `[fact-sheet](./fact-sheet.md)` or `[Solutions Architect Roadmap](../../resources/certification-roadmap-solutions-architect.md)`.
- Don't link to URL-shorteners. Link to the canonical URL so readers can see where they're going.
- When a vendor doc URL changes, fix all references in one PR (use `grep -rn "old-path"` to find them).

## Style and tone

- **No em dashes (-)**. Use regular dashes (-) instead. This is a global house style.
- **Avoid emojis** in body text. The repo uses a small set of section-marker emojis (☁️, 🔒, 📖, etc.) but body content stays plain.
- **Plain English, short sentences.** Aim for the reader who is mid-study at midnight on a Sunday.
- **Don't write fluffy intros.** Lead with the substance.
- **No trailing summaries** that repeat what was just said.
- **Cite, don't paraphrase**, when a vendor doc says it best. Link the doc.

## Diagrams

- Default: Mermaid in fenced ` ```mermaid ` code blocks, written inline in the page. GitHub renders it natively, it stays editable in the markdown, and it diffs as text in review.
- Mermaid carries no alt text, so add a caption or a sentence of prose saying what the diagram shows.
- Exception: PNG under `assets/diagrams/<topic>/<slug>.png` for diagrams too dense to read inline. Always include descriptive alt text.
- See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md#visual-content-standards) for the full convention.

## Frontmatter (new and refreshed pages)

Add YAML frontmatter to new pages. `last-updated` is the only required field; others are optional but useful.

```yaml
---
last-updated: YYYY-MM-DD
applies-to: AWS console as of 2026-Q2          # optional
difficulty: beginner | intermediate | advanced  # optional
reading-time: 10 min                            # optional
---
```

Backfilling existing files is opportunistic - do it when you touch a file, don't open a frontmatter-only PR for thousands of files.

The optional `tags:` field draws from a fixed vocabulary. See [docs/tag-taxonomy.md](./docs/tag-taxonomy.md) before adding tags, and propose new ones there first rather than inventing them inline.

## YouTube tie-in (optional)

When a topic has a companion video on [@patrickwiloak](https://youtube.com/@patrickwiloak), add a single-line callout near the top:

```markdown
> 📺 **Watch:** [Video title](https://youtube.com/...)
```

Keep these to one per page. Topic stays the source of truth; the video is a companion, not a replacement.

## What to do with retired exams

When a vendor retires a cert:

1. Add a clear "RETIRED [DATE]" banner to the top of `README.md` and `fact-sheet.md` for that cert. See [exams/aws/associate/sysops-administrator-soa-c02/](./exams/aws/associate/sysops-administrator-soa-c02/) for the canonical pattern.
2. Link to the replacement cert (if any).
3. Keep the original content intact for credential holders.
4. Remove the cert from active counts in `README.md` and `STUDY-HUB.md`.
5. Update any roadmap docs that reference the retired cert.

## Local validation

Several scripts live under `.github/scripts/`. The validators run in CI on every PR; the autolink helpers are run by a maintainer when content changes warrant it.

**Validators (CI gates):**

- `validate-cert-structure.sh` - confirms every `exams/<provider>/<cert>/` has a `README.md`. Tier-aware: senior-tier certs (Pro / Specialty / Expert and a curated cert list) also get warnings for missing `scenarios.md` and `strategy.md`. Run locally with `bash .github/scripts/validate-cert-structure.sh`.
- `validate-frontmatter.sh` - validates YAML frontmatter on concept pages, top-level learn pages, day-one pages, hands-on projects, cert fact-sheets, topic indexes, architecture patterns, networking deep dives, and decision-matrix / postmortem / playlist files. Fails on malformed YAML or bad date format; warns on missing or stale (>180d) `last-updated`. Run with `bash .github/scripts/validate-frontmatter.sh`.
- `build-freshness-ledger.sh` - regenerates [docs/freshness.md](./docs/freshness.md) from each file's `last-updated:` frontmatter. Run locally with `bash .github/scripts/build-freshness-ledger.sh > docs/freshness.md`.
- `check-code-fences.py` - fails on a markdown file with an unclosed ``` or ~~~ fence and names the line. Run with `python3 .github/scripts/check-code-fences.py`.
- `check-internal-links.py` - fails on a relative link whose file or `#heading` anchor does not exist. Run with `python3 .github/scripts/check-internal-links.py`.
- `check-orphan-links.sh` - lists `.md` files with no inbound links from other markdown. Manual one-shot, not a workflow gate. Useful before retiring or moving a file.

**Glossary autolink (one-shot maintenance scripts):**

- `glossary-autolink.py` - parses `learn/glossary.md` for bolded terms and links the first occurrence in scoped pages. Caps at 5 links per file; skips code blocks, headings, and existing links. Currently scopes: `learn/concepts/`, `topics/`, `resources/hands-on-projects/`, `resources/architecture-patterns/`, `resources/networking-deep-dives/`, plus decision-matrix / postmortem / playlist files.
- `glossary-add-anchors.py` - prepends `<a id="term-slug"></a>` to each bolded term in the glossary so links can target individual terms (not just sections). Idempotent. Run when the glossary gains new terms.
- `glossary-upgrade-existing-links.py` - upgrades old section-level glossary links to per-term anchors when an anchor is available.

- `check-repo-metadata.py` - checks the GitHub repository description, homepage and topics against the tree. The description is generated from `docs/certs.json`, never typed. `--fix` patches it, and needs admin rights, so it runs locally rather than in CI.
- `assets/brand/social-preview.html` - the social preview card template (same layout on all four Zero to Hero sites); screenshot it at 1280x640 into `assets/brand/social-preview-1280x640.png`, used both as GitHub's social preview and the site's Open Graph image.

**CI workflows under `.github/workflows/`:**

- `link-check.yml` - two jobs. **Internal links** (`check-internal-links.py`) block the merge, because a broken relative link is always our bug. **External vendor URLs** (lychee) are advisory and file an issue on the weekly Monday run, since vendor rot is nobody's fault here. The external job also fails loudly if lychee itself could not run: it spent months passing in 0.2 seconds because it was still passing a flag lychee had removed, so a guard now checks lychee's own exit code and that the report counted a non-zero number of links.
- `markdown-lint.yml` - markdownlint-cli2 against `.markdownlint.json`.
- `structure-validate.yml` - runs the cert-structure and frontmatter validators.
- `cspell.yml` - spell-checks markdown changes against `.cspell.json`. Currently non-strict (won't fail builds while the dictionary tunes); will flip to strict once noise is acceptable.
- `docs-site.yml` - builds the published site with `--strict` on every PR, and deploys to GitHub Pages on push to `main`.

See [.github/AUTOMATION.md](./.github/AUTOMATION.md) for a one-page map of every script and workflow.

## Previewing the documentation site

The repo is published at **[cloud.noblerworks.com](README.md)**. The site is generated from the markdown tree by `.github/scripts/build-site.py`, so there is no second copy of any page: write markdown as normal and the site picks it up.

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r requirements-docs.txt

# Live-reload preview on http://127.0.0.1:8000
.venv-docs/bin/python .github/scripts/build-site.py --serve

# What CI runs. Fails on broken links, bad anchors, or pages missing from the nav.
.venv-docs/bin/python .github/scripts/build-site.py --strict
```

A full build takes about two minutes and writes to `site/`. Three paths are generated and gitignored - `.site-src/`, `mkdocs.generated.yml`, and `site/` - so never edit them by hand.

Three things worth knowing when adding content:

- **New pages appear in the nav automatically**, labelled with their H1. A brand-new *top-level directory* is the exception: add it to the `TABS` table in `build-site.py`, or the build fails with the list of pages it could not reach.
- **Anchor links are checked.** The site uses GitHub's exact heading-slug algorithm, so `#section-name` behaves the same in both places. If the build reports a missing anchor, the link is genuinely broken on GitHub too.
- **The site's home page is `.github/site/home.md`**, not `README.md` - a repo front page and a website landing page want different things. Editing the README changes GitHub's front page, not the site's. The exception is the "What's new" list, which the build lifts from the README so it only has to be written once.

## Submitting a change

1. Fork the repo and make your changes on a branch.
2. **Run a spot-check before opening a PR**:
   - `bash .github/scripts/validate-cert-structure.sh` to confirm structure is intact.
   - `find exams -name "*.md" | xargs -I {} grep -l "broken-pattern" {}` for any cleanup you're doing.
   - Open the affected cert dir and visually confirm that links resolve to existing files.
   - Verify any updated counts (e.g. provider totals) match what's actually on disk.
3. Open a PR with:
   - A short title (under 70 chars) describing the change.
   - A description that explains the **why** as well as the **what**.
   - A test-plan checklist: which files changed, which links you verified, which counts you reconciled.

## PR checklist (copy into your description)

```
- [ ] Style: no em dashes (-); regular dashes (-) only
- [ ] All new vendor doc links use the **[📖 Title](URL)** format
- [ ] Internal links resolve (relative paths checked)
- [ ] If counts changed: README.md and STUDY-HUB.md totals reconciled
- [ ] If a cert was retired: banner added, replacement linked, counts updated
- [ ] If a new cert was added: README.md and STUDY-HUB.md provider tables updated
- [ ] No verbatim vendor exam questions
```

## Questions

Open an issue with the `question` label and one of the maintainers will respond. For broader proposals (new provider sections, new resource categories), open a discussion or issue first so we can scope it together.
