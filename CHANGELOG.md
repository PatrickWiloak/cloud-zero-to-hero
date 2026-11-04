# Changelog

All notable changes to the cloud certification study guides repository.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project uses calendar-based dating.

---

## [2026-11-04] - Dark mode by default

### Changed

- The site opens in dark mode for everyone instead of following the visitor's system setting. The header toggle still switches to light and remembers the choice.

## [2026-10-22] - "Which site should I start with?" page

### Added

- [Which Zero to Hero site should I start with?](./learn/which-site.md): who each of the four sites is for, a pick-by-goal table with the exact starting page on each site, a suggested order for all four, where they overlap, and a decision flowchart. The same page is published on all four sites; linked from the home page and the learn hub.

## [2026-10-21] (2) - Concept gap fill

### Added

- 14 concept pages in `learn/concepts/`: object, block and file storage; high availability and fault tolerance; disaster recovery (RPO and RTO); API gateways; message queues and pub/sub; multi-account strategy and landing zones; infrastructure as code; GitOps; service mesh; platform engineering; cloud identity for builders; Well-Architected; managed databases; edge computing. Short pages link the deep dives here and on the Data and Security sites.
- 3 Day One pages: environment variables and config, Linux processes and services (systemd), your first Docker container.
- 2 hands-on projects: build a landing zone (AWS Organizations, SCPs, org trail, budgets, with Azure and GCP equivalents) and GitOps with Argo CD (kind, Kustomize overlays, promotion and rollback by Git).
- All wired into the concept and Day One indexes, Cloud from Scratch, the hands-on index, labs-by-cert and the topic indexes.

## [2026-10-21] - Cloud Zero to Hero

### Changed

- The all-in-one Zero to Hero repo was split by subject into four sibling sites. This repo keeps the cloud subject and is now **Cloud Zero to Hero** (`cloud-zero-to-hero`, https://cloud.noblerworks.com/). Data, security and AI guides moved to [Data](https://data.noblerworks.com/), [Security](https://security.noblerworks.com/) and [AI](https://ai.noblerworks.com/) Zero to Hero; links into them are absolute URLs.
- README, Study Hub (decision tree, career tracks, popular certs, timelines), the site home page, CONTRIBUTING, docs/ARCHITECTURE.md, the learn and topic indexes, the social card and the repository description template now describe the cloud site only. Every page carries the shared Zero to Hero family bar, and the home page and README link the three sibling sites.

## [2026-10-16] (2) - Seven more exams flagged from a vendor check of all providers

### Fixed

- Checked the other 26 providers against vendor pages. Three guides describe exams that have ended and are now marked RETIRED: AWS Security Specialty SCS-C02 (ended 2025-12-01, replaced by SCS-C03), AWS Machine Learning Engineer Associate MLA-C01 (English ended 2026-09-28, MLA-C02 in beta) and HashiCorp Consul Associate 003 (retired July 2026). Four more carry `exam-retires:` and a "retires on" notice: AWS SAP-C02 (2026-11-16), DVA-C02 (2026-11-30), ANS-C01 (2026-12-31) and CompTIA CySA+ CS0-003 (2026-12-22). Findings that rest on a search snippet or third-party sites, and those that need a rewrite, are in TODO.md with a confidence level instead of in the guides.

## [2026-10-16] - Nine retired Azure exams flagged

### Fixed

- Nine Azure guides described exams Microsoft has retired, with no warning: MS-900, DP-100, AI-102, AI-900, AZ-204, AZ-500, PL-200, DP-203 and PL-100. Each README now reads "RETIRED" with the date and a source link, and each fact sheet carries `exam-version:` and `exam-retires:`. The generated status in `docs/certs.json` and the provider tables now shows Retired (the certification total is unchanged, as for the retired AWS certs). Dates come from Microsoft Learn's retired-exams page, except DP-203, which comes from Microsoft Q&A and third-party posts. AI-900's note points to its live successor AI-901.

## [2026-10-14] (5) - Flagged keys checked against vendor docs; Vertex AI renamed

### Fixed

- About 70 practice-question keys flagged as stale or wrong were checked against official vendor documentation. 18 keys or questions were corrected (for example AWS Lambda timeout, AWS Patch Manager rollback, Cloud Run's 8 vCPU job limit, Azure Blueprints and classic CDN retirement, Hyperopt, Copilot Knowledge Bases), others were confirmed or reworded to remove ambiguity. Outcome and sources: [docs/practice-question-key-review.md](./docs/practice-question-key-review.md).
- Google renamed Vertex AI to the Gemini Enterprise Agent Platform (2026-04-22) and its current exam guides use the new names. About 480 mentions across the GCP exam folders, resources, topics and practice banks now use Google's names from its 56-row rename table, with "(formerly Vertex AI)" on the first mention in each file. Names the table does not list were left unchanged. Glossary entry updated.

## [2026-10-14] (4) - Practice questions: length tell removed, distractors reviewed

After the answer letters were balanced, the correct option was still the longest of the four in 88% of questions (2,651 of 3,015). A first rewrite pass removed that but overshot: the correct option became the shortest in 38% of questions overall, and in 80% or more in about 20 banks. A second pass assigned each question a target length rank (shortest / second / third / longest, balanced to 25% each) and checked it with a script.

### Fixed

- All 150 banks now carry no length tell: the correct option is the longest or shortest in at most 45% of any bank's questions (`balance-answer-positions.py --check-length`), and every per-question target is met.
- A review pass over every question looked for a second arguably-correct option, invented products and stale facts. About 350 questions had option meanings changed (for example options that were also valid, made-up AWS and Azure features, retired products) and the matching explanations corrected.
- 76 questions with "all of the above" / "both A and B" options were rewritten as independent single-answer options.
- `gcp-workspace-administrator` Q27 had the wrong key (a bug in my own generator); fixed.
- `offensive-security-oscp.md` (a 4-question stub that duplicated `oscp-pen-200`) deleted. Header question counts corrected where wrong.

### Added

- `--check-length` in `.github/scripts/balance-answer-positions.py`, and both checks in `structure-validate.yml`.
- [docs/practice-question-key-review.md](./docs/practice-question-key-review.md): about 70 keys the reviewers believe are stale or wrong, left unchanged for a human to verify against vendor documentation.

## [2026-10-14] (3) - Practice-question answer positions balanced repo-wide

An audit of `resources/practice-questions` found the correct answer was B in most banks: 64 of 152 banks had B correct for 90% or more of their questions (52 of them for every question). A learner could score well by always choosing B.

### Fixed

- 150 banks (2,904 questions) rebalanced so each letter is correct about equally often. Letter references in explanations (`(A)`, `Option B`) and every answer-key table were remapped. Checked against git HEAD: correct-option text identical for every question, 1,112 remapped references each point at the same option text as before, and 520 answer-key rows match their questions.
- 76 questions whose options refer to other options ("all of the above", "both A and B") or whose explanation refers to letters in a form the tool cannot remap were left in place.

### Added

- `.github/scripts/balance-answer-positions.py` with `--check` and `--write`, and authoring rules in `resources/practice-questions/template.md`.

### Found, not fixed

- The correct option is the longest of the four in 88% of questions (2,651 of 3,015). Needs rewriting by hand; see TODO.md.

## [2026-10-14] (2) - Cloud Architect brought up to the current exam guide

### Fixed

- **Section weights and structure.** README and fact sheet carried an older weighting. Now ~25 / 17.5 / 17.5 / 15 / 12.5 / 12.5, with section 6 as solution and operations excellence.
- **Case studies.** The notes taught Mountkirk Games, TerramEarth, Helicopter Racing League and Dress4Win. The current guide uses Altostrat Media, Cymbal Retail, EHR Healthcare and KnightMotives Automotive. Strategy, practice plan (week 8), README and fact sheet now point at the new four; the old four are marked retired.
- **Practice questions: every answer was B.** All 40 existing questions had B as the correct option. Options are shuffled, and the explanations' (A)/(B) references remapped.
- **Dead exam-guide link** (`certification/guides/professional-cloud-architect`) replaced.

### Added

- `notes/case-studies.md` - own-words summaries of the four cases, requirement-to-design tables, traps, cross-case patterns, links to Google's PDFs.
- `notes/ai-gemini-and-agent-platform.md` - Vertex AI to Agent Platform rename, AI decision ladder, Google AI APIs, Model Garden, grounding and RAG, Gemini Enterprise and NotebookLM, AI Hypercomputer, Model Armor, Sensitive Data Protection, Gemini Cloud Assist, Migration Center.
- `notes/well-architected-and-operations.md` - the six pillars (sustainability added), section 4 processes and DR patterns, programmatic access and emulators, observability, chaos / pen / load testing, VMware Engine, Chrome Enterprise Premium.
- 26 questions (66 total) on the case studies, AI and operations; 6 scenarios (14 total); sustainability pillar in the Well-Architected resource page.

## [2026-10-14] - Workspace Administrator re-levelled to Associate and rebuilt; Cloud Architect gap list

Checked both GCP exams against Google's current official exam guides (read from the PDFs).

### Fixed

- **`exams/gcp/workspace-administrator` described the wrong exam.** It was filed as a Professional exam with five domains at $200 and a 2-year validity. Google's current exam is the **Associate Google Workspace Administrator**: six sections (~20/23/15/20/10/13%), $125, 2 hours, 50-60 questions, English and Japanese, no published validity. README, fact sheet, strategy, practice plan, `certs.json` and the `exams/gcp` table now say so. The folder slug is unchanged so links keep working.
- **The old notes taught commands that do not exist** (`gcloud identity users create ...`, about 60 lines). Users, OUs and groups are managed in the Admin console, the Directory API, GCDS or an IdP.

### Added

- Seven notes, one per exam section, replacing the three old ones: users and Directory, core services, Gemini and AppSheet, governance, security and access, browsers and endpoints, troubleshooting. New topics: Gemini controls, AppSheet vs Apps Script, Drive Labels, target audiences, trust rules, Chrome Browser Cloud Management, Email Log Search, Admin Toolbox, HAR files.
- A 243-card `flashcards.csv` (the deck was missing), 23 scenarios (was 6), and 45 practice questions (was 15) with shuffled answer positions.

### Found, not yet fixed

- `exams/gcp/cloud-architect` was written for an older Professional Cloud Architect guide. See TODO.md for the gap list.

---

## [2026-09-28] - CompTIA A+, every page gets its own search snippet, and search engines hear about changes

GitHub's traffic view for the 14 days to 2026-09-28 showed Google sending 5 visits to a site of 2,041 pages. ChatGPT sent 10. The published site had three defects that explain part of that.

### Fixed

- **All 2,041 pages shared one meta description**, the site-wide `site_description`. Google treats a repeated description as boilerplate and writes its own snippet. `.github/scripts/site_hooks.py` now gives each page its own: the first prose paragraph, or for cert landing pages, fact sheets, study plans, scenarios and strategy pages a summary built from `docs/certs.json` (those open with fact lists, and they are what people search for by exam code). Result: 2,041 distinct descriptions.
- **Titles ended in the 45-character site name**, so "AWS Certified Solutions Architect - Associate (SAA-C03) - Cloud, Data, AI, and Security - Zero to Hero" was cut off in results. Titles are now the page's H1, with the exam code appended inside a cert directory ("Core Data Concepts - DP-900") and a short "| Zero to Hero" suffix only when it fits. Cert landing pages read "... Study Guide".
- **No search engine was ever told the site existed.** Deploys now send the changed page URLs to IndexNow (`notify-indexnow.py`). Google reads the sitemap instead; its Search Console property is a manual step, listed in TODO.md, and `mkdocs.yml` has an `extra.google_site_verification` slot for the token.

### Added

- **CompTIA A+ (220-1201 and 220-1202)**, the most-searched entry-level IT certification and the repo's first A+ coverage: README, fact sheet, study plan, scenarios, strategy, nine notes (Core 1 domains 1-5, Core 2 domains 1-4, 16 Mermaid diagrams) and 20 original [practice questions](./resources/practice-questions/comptia-a-plus-220-1201-1202.md). Exam facts were checked against CompTIA's V15 pages on 2026-09-28; the voucher price could not be read from an official page and the fact sheet says so. The repo is now at 149 certifications.
- schema.org **BreadcrumbList** JSON-LD on every page, and **WebSite** on the home page.
- `noindex` on working files published for transparency (`TODO.md`, `CLAUDE.md`, the roadmap and link-rot reports).
- A new home-page description that names the certifications people search for (AWS, Azure, GCP, Kubernetes, CompTIA, CISSP).

---

## [2026-09-18] - All 783 dead links repaired, and three kinds of dead link instead of one

The first real sweep had only counted 404s. This one also catches **soft 404s** (a 200 response on a "page not found" page, which no status-code checker can see, lychee included) and **deep links lost to a redirect** (a URL that now forwards to a homepage, a search page or a login wall). That raised the count from 685 known-dead to **783**.

### Fixed

- **303 dead URLs repaired, 449 citations.** No replacement was accepted on a similarity score. Candidates came from each vendor's own navigation tree (Google, Oracle, Microsoft and NVIDIA render the whole product nav server-side), sitemaps (Databricks, Snowflake) and Microsoft Learn's search API. Each one was chosen by reading the candidates against the citation's own link text, then fetched and title-checked. The scores alone were not safe: they matched Snowflake to its separate Open Catalog product, Cosmos DB for NoSQL to the Cassandra and Gremlin APIs, and one Catalyst switch to a different one because both URLs ended in `series.html`. All of those were rejected.
- **37 moved links re-pointed, 87 citations.** Dead hosts with a known new home (`home.pearsonvue.com` to `www.pearsonvue.com`, `spec.modelcontextprotocol.io` to `modelcontextprotocol.io/specification`, Forseti to its archived repo), plus links that only still worked through a redirect: AWS doc indexes, and Vertex AI docs now served as Gemini Enterprise Agent Platform.
- Where IBM retired a service and names a successor (Log Analysis to Cloud Logs, Cloud Functions to Code Engine, Certificate Manager to Secrets Manager), the citation now points at the successor. The link text still names the old product, and the report lists every such substitution.

### Then the last 480, by hand

- **480 URLs whose pages were removed outright, 610 link occurrences.** An earlier pass on the same day had left these listed rather than point a specific citation at a generic landing page. They are now repaired one by one: the link text was read and the closest live page on the same subject chosen, usually the renamed or merged page (Azure OpenAI pages into Microsoft Foundry, Cloud DLP into Sensitive Data Protection, Dataproc into Managed Service for Apache Spark, GCP docs onto `docs.cloud.google.com`, Architecture Center articles into the Well-Architected Framework pillars, LUIS into conversational language understanding, retired exam pages into their successor exams). All 418 distinct targets were fetched and returned 200 with a matching title and no redirect to a homepage.
- **6 Amazon QLDB links point at pinned Internet Archive snapshots.** QLDB is retired with nothing that covers its journal, verification or PartiQL reference, and AWS now redirects every QLDB page to Aurora. `web.archive.org` is excluded from the weekly check, since a pinned snapshot cannot change.
- **The author's own blog post is gone** (the blog was removed from patrickwiloak.com on 2026-09-05). Its two README mentions were dropped; the site footer links to the homepage instead.
- [docs/link-rot-2026-09-17.md](./docs/link-rot-2026-09-17.md) is now the record of every replacement, old URL to new, so one that looks wrong can be traced.

---

## [2026-09-17] - The link checker that never ran, and the data pillar

An audit of the repo against its own claims. Every validator was green and had been for weeks, which turned out to be part of the problem: one of them was green because it was not running, and the numbers GitHub shows about this project are not files, so nothing checked them.

### Fixed

- **The external link check had never checked a link.** `link-check.yml` passed `--exclude-mail` to lychee. Lychee removed that flag (it is `--include-mail` now, and mail is excluded by default), so the binary aborted on argument parsing, walked zero URLs, and exited non-zero - which `fail: false` swallowed into a green step in 0.2 seconds. Every weekly report artifact since the job was written is 147 bytes: one link, no results. The "open an issue on failure" step could not fire either, because it was gated on `failure()`, and `fail: false` guarantees that is never true.

  Both are fixed, and both now have a guard, because the failure mode was silence rather than error: the job fails loudly if lychee's exit code is anything but 0 (clean) or 2 (ran, found breakage), and again if a "successful" report contains no link total. A check that cannot run must not be able to pass.

- **701 dead vendor links, cited 903 times.** What the sweep found once it ran: 8,591 unique external URLs, 8.2% of them returning 404. Concentrated in the vendors who reorganized their documentation this year - Google Cloud (234), Microsoft Learn (152), Oracle (89), Databricks (27). The full list, with the file citing each one, is in [docs/link-rot-2026-09-17.md](./docs/link-rot-2026-09-17.md) and tracked in TODO.md. The most-cited ones are repaired here; the tail needs a successor page found per link, which is editorial work, not a rewrite rule - mechanical transformations (host moves, locale variants, trailing slashes) resolved 2 of 1,389 candidates.

- **The repository description was 26 certs and 5 providers out of date.** It read "122+ certs across 22 providers, 37 plain-English concepts" against a tree at 148 / 27 / 53. It is the first sentence anyone reads about this project - in search results, in the sidebar, in every link preview - and `check-readme-counts.py` could never have caught it, because a repository description is not a file. New `check-repo-metadata.py` generates the description from `docs/certs.json` and checks it, the homepage, the topics and the social preview in CI. `--fix` patches it, and deliberately only works locally: the Actions token cannot write repository settings.

- **`learn/README.md` advertised its own concept-page count**, outside `CLAIMS` and therefore unguarded. Adding seven pages left it reading 46 against 53. `check-readme-counts.py` now guards a list of files rather than just `README.md`, and caught it on the first run.

### Added

- **Seven data-engineering concept pages**, closing the weakest of the four subjects in the repo's own name. "Data and Databases" in the learn pillar was three pages, two of which are really distributed-systems topics, while the exam notes carried the material in depth (Parquet appears in 111 files, lakehouse in 75) with no plain-English entry point: [warehouses, lakes and lakehouses](https://data.noblerworks.com/learn/concepts/warehouses-lakes-lakehouses/), [ETL vs ELT](https://data.noblerworks.com/learn/concepts/etl-vs-elt/), [batch vs streaming](https://data.noblerworks.com/learn/concepts/batch-vs-streaming/), [data modeling for analytics](https://data.noblerworks.com/learn/concepts/data-modeling-for-analytics/), [file formats and partitioning](https://data.noblerworks.com/learn/concepts/file-formats-and-partitioning/), [data pipelines and orchestration](https://data.noblerworks.com/learn/concepts/data-pipelines-and-orchestration/), [data quality and lineage](https://data.noblerworks.com/learn/concepts/data-quality-and-lineage/).

- **[`topics/data-engineering.md`](https://data.noblerworks.com/topics/data-engineering/)**, the 14th cross-pillar hub. `topics/README.md` had named data engineering as a subject with no index; that line is now retired.

- **Open Graph and Twitter card tags on the site**, via `.github/site-overrides/main.html`. Material ships none, so all 2,034 pages previewed in Slack, X and LinkedIn as a bare URL. Static tags against one committed card rather than the `social` plugin, which needs Cairo and Pillow on the runner and can fail a build.

- **The social preview card itself**, at `assets/brand/social-preview-1280x640.png`, generated by `build-social-card.py` in the site's own design language and real Geist. It carries **no counts** on purpose: an image with "148 certs" baked into it is a number nothing can check, which is the exact failure this release fixes elsewhere. Uploading it to GitHub's social preview is the one step here that stays manual, because the REST API does not expose that field.

- **`SECURITY.md` and `CODE_OF_CONDUCT.md`**, both written for what this repo actually is. The security policy asks for reports about insecure code samples and hijacked link targets, and says plainly that a dead link is a content bug rather than a vulnerability.

- **`.github/dependabot.yml`**, monthly, for Actions and the docs toolchain. Major bumps of mkdocs and mkdocs-material are excluded, because `.github/site-overrides/` now holds copies of two of Material's templates.

### Changed

- **Every GitHub Action bumped**, between two and six major versions each: checkout v4 to v7, upload-artifact v4 to v7, setup-python v5 to v7, upload-pages-artifact v3 to v5, deploy-pages v4 to v5, cspell-action v6 to v9, create-issue-from-file v5 to v6, markdownlint-cli2-action v18 to v24. Actions had been warning on every run that the Node 20 runtime these targeted is deprecated.

- **MD060 disabled in `.markdownlint.json`**, which is what unblocked the markdownlint bump. The rule fires 17,207 times across the repo and nothing else fires at all; it checks table pipe padding, which changes no rendered output. Normalising every table instead would have been a 17,000-line diff across a thousand content files, burying everything else in this release. This resolves the open question recorded in the 2026-08-09 notes.

---

## [2026-08-14] - The site adopts the gitGood design language

The monochrome pass from earlier today still read like a styled README. This pass ports gitGood.dev's actual design system - extracted from its source, not eyeballed - so the two Nobler Works sites share a language: pure-black dark mode plus a single green accent (`#22c55e`; `#15803d` for text on white), Geist and Geist Mono, and gitGood's signature card hover of accent border, accent-tinted shadow, and a 2px lift at 200ms.

### Changed

- **One accent instead of monochrome.** Links, the primary button, active nav entries, provider-chip counts, card icons, kickers, the practice-answer reveal border, focus rings and scrollbar thumbs now carry the accent. Underlines move to hover only, since colour carries the signal again. Cards keep the page-colour background - gitGood cards are not raised surfaces; separation is a 1px hairline until hover.
- **Fixed two dark-mode defects the monochrome palette shipped.** Material's outlined buttons draw from `--md-primary-fg-color`, which was `#000000` - so on the black landing page two of the three hero buttons were invisible and the primary rendered as bare text. And Material dims `h1` to the secondary text colour, which washed out every page's title; headings are now full-strength and bold (Material defaults them to weight 300).
- **The hero is centred and staggered** - gitGood's fadeInUp entrance, 0.6s ease-out at 100ms steps, disabled under `prefers-reduced-motion`. The landing page's section headings drop their emoji and gain accent eyebrow kickers instead.
- **Content-page headings drop their leading emoji on the site only** - `strip_heading_emoji()` in `build-site.py`, a fence-aware transform over the staged copy, so the repo's markdown keeps its house style on GitHub. Anchors cannot move: the repo's ~960 inbound anchor links were written against GitHub's slugs, where the emoji leaves a leading hyphen, so each stripped heading pins its original slug as an explicit attr_list id computed with the same pymdownx slugifier the toc uses. The `[📖 ...]` body-link convention is untouched, and the sidebar's section and provider landmarks are nav labels, not headings, so they stay.
- **The header's repo widget is hidden.** The truncated slug plus star/fork counts was the most GitHub element on the page. `repo_url` stays for the edit links; the footer still links the repo.
- **Geist replaces Inter, Geist Mono replaces JetBrains Mono** - gitGood's faces, served from Google Fonts as before.

---

## [2026-08-14] - Monochrome theme, a single left sidebar, and a gitGood promo

Presentation pass over the newly published site, plus the first promotion of [gitGood.dev](https://gitgood.dev) from this repo.

### Changed

- **Monochrome palette, Nobler Works house style.** `mkdocs.yml` sets `primary: custom` and `accent: custom`, which opts out of Material's built-in colour palettes entirely; the values live in `.github/site/extra.css`. All three palette entries need the setting, not just light and dark - the "auto" entry is what renders before the palette JS runs, so leaving it unset kept serving Material's default indigo regardless of the other two. With links no longer distinguishable by colour, prose links carry underlines that thicken on hover; navigation, tab and table links stay plain.
- **Dark mode is true `#000000`.** Both banners on the site are flattened PNGs on pure black, so a near-black page (`#0d0d0d`) framed each one in a visible rectangle. The header gains an explicit bottom border, since a black bar on a black page stops reading as a bar.
- **Navigation is on the left on every page.** `navigation.tabs` is off: with tabs, the left sidebar shows only the active tab's subtree, so Home - a root page with no children - rendered an almost empty left column while a cert page rendered a deep one, and the sidebar changed shape depending on where you stood. It is now the same full site tree everywhere, with the current branch expanded.
- **The page table of contents folds into that sidebar** (`toc.integrate`), so there is no second column on the right.

### Added

- **`.github/site-overrides/partials/nav-item.html`** - the upstream Material partial with one marked `LOCAL ADDITION`. `toc.integrate` alone is not safe with `navigation.indexes`: Material emits the integrated ToC from the `nav_item == page` branch, which fires for leaf pages only, so a section-index page - every cert landing page plus every generated directory index - matched no branch and rendered no table of contents at all. The override restores it.
- **A gitGood.dev promo** in the README header and on the landing page, with `assets/brand/gitgood-banner.png`. gitGood ships no marketing banner, only a loading splash carrying a progress bar and an "84%" label; the banner is that splash cropped to the brand lockup, measured rather than eyeballed, and padded to 2.6:1.

### Notes

- The Material pin in `requirements-docs.txt` is now load-bearing twice over. After a version bump, re-copy the overridden partial and re-apply the marked block, then check a cert landing page by eye - a `--strict` build will not flag a drifted template, because a missing table of contents is not an error.
- Promo copy names 21 role-targeted learning paths and the certification banks by exam code, because the README is also the site's indexed home page and those codes are what people search. The README's role, certification and feature lists sit inside a collapsed `<details>`: the height comes off the visible page, the text stays in the HTML.

---

## [2026-08-14] - The site gets a landing page, and the README's provider table comes back under CI

The published site opened on the repo's `README.md`, because MkDocs treats a directory's README as its index. That is the right front page for GitHub and the wrong one for a website: a visitor arrived at a banner image, five social badges, a count-badge row, a repository-structure tree, and "star this repo" before reaching anything they could read.

### Added

- **`.github/site/home.md`** - a site-only landing page: a hero with three entry points, a counts strip, the four pillars as cards, a two-column "jump to what you need" list, all 27 providers as chips, and the three most recent release notes. `build-site.py` renders it over the staged copy of `README.md`, so the repo's README is untouched, no page is duplicated, and no link changes.
- **Landing-page styling in `.github/site/extra.css`** - scoped to classes that appear only on that page.
- **The README's "Browse Certifications" table is now generated**, by `build-provider-indexes.py`, from `docs/certs.json` and between markers - the same treatment the `STUDY-HUB.md` table already had. The "Highlights" blurb is a single curated string per provider, shared by both tables so they cannot describe a provider differently, and the script refuses to run when a provider has no highlight or icon. A new provider now fails CI rather than quietly missing a row.
- **CLAIMS coverage for the "Repository Statistics" block** and the repository-structure comments - 17 numbers that nothing checked.

### Fixed

- **The README's per-provider table was stale in 8 of 22 rows and missing 5 providers entirely.** Kubernetes/CNCF read 7 against 12, Azure 23 against 26, CompTIA 2 against 4, Oracle 5 against 7, and AWS, Cisco, Salesforce and ISC2 were each one or two low. ISACA, Offensive Security, Palo Alto Networks, ServiceNow and VMware had no row at all, five days after the Tier 1 batch added them. The badge counts were right the whole time, because they are generated - the table was not. It is now.
- **Four curated "Highlights" lines were describing half a provider**, and were feeding `STUDY-HUB.md` while they did: Kubernetes/CNCF listed 7 of 12 exams, ISC2 omitted CC, Oracle omitted both OCI AI certs, and AWS omitted the GenAI Developer professional. A count that changes without its description changing is the failure mode a generated count column cannot catch on its own.
- **`Concept pages: 37`** against 46, **`Topic indexes: 8`** against 13, and **`Compliance guides: 5`** against 8, in the statistics block.

### Notes

- No number is typed into `home.md`. Each is a token filled from `certs.json` and from `check-readme-counts.py`'s `gather()`, the same counting code CI runs against the README, so the two pages cannot disagree. The "What's new" bullets are extracted from the README at build time for the same reason.
- Every counted claim in the README now has exactly one owner: `build-certs-index.py` for the index, `build-provider-indexes.py` for the two provider tables, `check-readme-counts.py` for everything else. The provider-table check that briefly lived in `check-readme-counts.py` was removed when the table became generated - two scripts able to rewrite the same rows is a way to make one of them wrong.
- Editing `README.md` no longer changes the site's home page. See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md#the-home-page-is-not-the-readme).

---

## [2026-08-14] - Published as a searchable website on GitHub Pages

The repo's 3.0M words were only navigable through GitHub's file listing, with no search. Every page is now also published as a MkDocs Material site at **[cloud.noblerworks.com](README.md)** with full-text search, dark mode, and mobile navigation.

The markdown tree is unchanged and remains the source of truth. The site is generated from it at build time rather than the tree being restructured for the generator, so there is no second copy of any page and reading the repo on GitHub is unaffected.

### Added

- **`.github/scripts/build-site.py`** - stages the markdown tree, generates landing pages for directories that lack a `README.md`, rewrites the ~1,200 directory-style links (`](../notes/)`) to resolve as URLs, and generates all 2,032 navigation entries from the tree using `docs/certs.json` for cert and provider labels. Cert levels sort by exam progression; files within a cert sort in study order.
- **`mkdocs.yml`** - hand-maintained theme and extension config, deliberately without a `nav` key.
- **`.github/workflows/docs-site.yml`** - builds with `--strict` as a blocking check on every PR; deploys to GitHub Pages on push to `main`.
- **`requirements-docs.txt`** - fully pinned toolchain.
- **`.github/site/extra.css`** - site-only styling: wider content column for the comparison tables, and styled answer reveals for the 154 practice question banks.

### Fixed

Three classes of pre-existing defect that the strict site build surfaced. All were broken on GitHub too:

- **An unclosed code fence in `exams/gcp/cloud-architect/notes/compute-containers.md`** silently swallowed ~130 lines, including four headings, rendering them as a code block. A stray duplicate fence in the same file compounded it. A repo-wide scan found no other instance.
- **14 broken heading anchors** in `resources/community-resources.md` (11), `README.md`, `docs/improvement-roadmap.md`, and one AWS note. Most were links that omitted the leading hyphen an emoji heading produces.
- **Links into `.templates/`** now resolve on the site; the directory is staged as `provider-resources/` because MkDocs skips dot-directories and reserves a root `templates/`.

### Notes

- **One-time setup:** Settings > Pages > Build and deployment > Source must be set to **GitHub Actions** before the first deploy succeeds.
- Heading anchors use GitHub's exact slug algorithm (`pymdownx.slugs.slugify(case="lower")`), so `#section-name` behaves identically in both places and the build can validate all ~960 anchor links.
- The build fails if any page is unreachable from the navigation, so a new top-level directory cannot silently vanish from the site.

---

## [2026-08-11] - Anthropic Claude certification program: 4 official certs covered, Anthropic becomes the 27th certification provider

Anthropic launched an official Claude certification program in 2026 (Architect - Foundations in March, then Associate, Developer, and Architect - Professional in July, all via Pearson VUE). This repo previously carried 4 fictional self-directed Anthropic "study tracks"; this pass replaces them with real coverage of the actual program. Repo totals move from 144 certifications / 26 providers / 6 study tracks to **148 certifications / 27 providers / 3 study tracks** (151 cert directories).

### Added

- **`exams/anthropic/claude-certified-associate-foundations/`** - complete new guide for the Claude Certified Associate - Foundations exam (CCAO-F, $99, 60 questions): README, fact-sheet, 7 domain notes, practice-plan, 10 scenarios, strategy, plus a 15-question practice bank at `resources/practice-questions/anthropic-claude-associate-foundations.md`.
- **Blueprint-gap notes** - CCAR-P gains `notes/08-governance-safety-and-risk-management.md` and `notes/09-stakeholder-communication-and-lifecycle-management.md`; CCDV-F gains `notes/08-model-selection-and-optimization.md`, `notes/09-agents-and-workflows.md`, and `notes/10-security-safety-claude-code-and-evals.md`.

### Changed

- **`claude-certified-architect-advanced/` renamed to `claude-certified-architect-professional/`** and retargeted to the real CCAR-P exam ($175, 63 questions, 7 official domains); its practice bank renamed and updated to match.
- **`claude-application-developer/` renamed to `claude-certified-developer-foundations/`** and retargeted to the real CCDV-F exam ($125, 53 questions, 8 official domains); its practice bank renamed and updated to match.
- **`claude-certified-architect-foundations/`** converted from a study track to the real CCAR-F exam guide (launched March 12, 2026; $125, 60 questions, 5 official domains) with corrected code, delivery, validity, and cost.
- **All four guides** now carry official domain blueprints with weights, Pearson VUE delivery, 720/1000 passing score, 12-month validity with free on-time renewal, retake policy, and Anthropic Partner Academy registration steps.
- **Anthropic promoted to a certification provider** in `build-certs-index.py` / `build-provider-indexes.py` (previously a "(study tracks)" pseudo-provider appended after the totals row). The Claude Prompt Engineering Specialist track remains the sole Anthropic study track, since the program has no prompt engineering exam.
- **Counts regenerated everywhere** - `docs/certs.json`, all 27 provider indexes, STUDY-HUB provider table, freshness ledger, lab map, flashcards (now 105 decks / 9,660 cards), README and STUDY-HUB badges and stats.

### Notes

- CCAO-F and CCAR-P domain weights are sourced from Pearson VUE plus secondary exam guides; official exam guide PDFs sit behind the Anthropic Partner Academy login. Flagged in `TODO.md` for verification.

---

## [2026-07-29] - Gap-analysis pass: fixed 383 broken links, generated cert index + navigation, drafted notes for all 10 outline-stage certs, added flashcards / lab map / freshness rotation

A full pass against the repo-wide gap analysis in [docs/improvement-roadmap.md](./docs/improvement-roadmap.md). Twelve commits, all on `main`. Ended with 0 broken internal links (3,133 checked), 0 structure-validator warnings, and 0 orphaned pages.

### Added

- **`docs/improvement-roadmap.md`** - a measured, evidence-backed gap analysis of the whole repo (what is broken, what is missing, what would raise the bar), and a matching four-phase backlog in `TODO.md`.
- **`docs/certs.json`** - a generated, machine-readable index of all 137 cert directories (exam code, level, status, duration, cost, passing score, notes count, standard files present, last-updated). Built by `.github/scripts/build-certs-index.py`; the single source of truth for every count and table. Fields that cannot be parsed are `null`, never guessed.
- **Per-provider index READMEs for all 27 providers**, generated from `docs/certs.json` by `.github/scripts/build-provider-indexes.py`. The 6 hand-written provider READMEs keep their editorial content; only a marked block is regenerated. Closes the 21 provider directories that previously landed on a bare GitHub file listing.
- **Drafted topic notes for the 10 outline-stage certs** - CompTIA CySA+ (4) and Network+ (5), Cisco CCNP ENCOR (6), ISACA CISA (5) and CISM (4), Offensive Security OSCP (6), Palo Alto PCNSA (4 + scenarios + strategy), Salesforce PD2 (6 + strategy), ServiceNow CSA (6 + scenarios + strategy), VMware VCP-DCV (6). ~50 new note files of original cert content, written to each exam's published blueprint. All 10 flipped from `outline` to `active`; no cert remains at outline stage.
- **`aws/professional/genai-developer-aip-c01`** completed with `practice-plan.md`, `scenarios.md`, and `strategy.md` - the last outstanding structure-validator warning.
- **Per-cert `flashcards.csv`** (Anki-importable) in each cert dir, generated by `.github/scripts/build-flashcards.py`: 90 decks, 8,484 cards. Cards are extracted, not invented - exam logistics from `docs/certs.json`, term-definition cards from the `- **Term** - definition` lines the notes already use. Certs below a 15-card threshold get no deck rather than a thin one.
- **Lab-to-cert mapping**, generated by `.github/scripts/build-lab-map.py`: each hands-on project declares the certs it exercises in frontmatter, producing a lab-to-cert table in the projects index and a reverse index at `resources/hands-on-projects/labs-by-cert.md` (46 of 137 certs have a matching lab).
- **`.github/scripts/check-internal-links.py`** - offline, code-fence-aware internal-link checker, now a blocking CI job.
- **`.github/scripts/check-cert-freshness.py`** - assigns each provider a review month so re-verification spreads across the year instead of all falling due on one date, and warns ahead of exam revisions via optional `exam-version:` / `exam-retires:` frontmatter (seeded on the 4 retired AWS certs).

### Changed

- **Diagram standard: Mermaid is now the documented default**, PNG the exception for diagrams too dense to read inline. Updated `CLAUDE.md`, `docs/ARCHITECTURE.md`, `CONTRIBUTING.md`, and `assets/diagrams/README.md`. This matches what the repo actually does (89 pages use Mermaid, no PNG was ever added), so the documented standard no longer has zero instances.
- **Cert counts corrected across the front door.** README and STUDY-HUB advertised "122+ certifications across 22 providers"; actual is **131 certifications + 6 self-directed study tracks across 137 directories, spanning 26 certification providers**. Badges, prose, and the STUDY-HUB provider table (which was missing 5 providers and undercounted 3) all updated and now generated from `docs/certs.json`.
- **The AWS AI Practitioner moved into the tier structure**: `exams/aws/genai` → `exams/aws/foundational/ai-practitioner-aif-c01/`, with all inbound links repointed. The Azure and GCP GenAI directories were reclassified as self-directed study tracks (they are not single exams) and are no longer counted as certifications.
- **Cert discovery fixed in the validator and ledger.** Both previously found certs by looking for a `notes/` subdirectory, silently skipping the 10 certs whose notes were undrafted. Both now key off `fact-sheet.md`, so all 137 are checked (previously 127).
- **`link-check.yml` split into two jobs**: a blocking internal-link check and an advisory external-URL (lychee) check with the existing weekly issue-filing. Previously lychee ran with `fail: false` and nothing enforced internal link integrity, which is how 383 broken links had accumulated.
- **`.claude/settings.json` pruned** - removed absolute paths from a previous machine and replaced the blanket `Bash(*)` allow with the commands this repo actually uses.
- **`.github/AUTOMATION.md`** documents all the new scripts and their CI wiring.

### Fixed

- **383 broken internal links → 0.** 191 in `docs/freshness.md` (a path-prefix bug in `build-freshness-ledger.sh`, since the ledger renders one directory below the repo root), 87 absolute `/exams/...` links in the roadmap resources (a leading slash resolves to the GitHub domain root), 77 links to notes that were never written (delinked and marked `_(planned)_`, then restored as the notes were drafted), and 28 stale paths from an older directory layout.
- **`check-orphan-links.sh` wired into CI as advisory** and the one real orphan (`docs/tag-taxonomy.md`) linked from CONTRIBUTING. Orphans are now 0.

---

## [2026-05-03] - Senior-tier scenarios + strategy, 20 architecture/networking diagrams, 4 new topic indexes, glossary autolink, orphan-checker fix, tier-aware structure validator, repo governance scaffolding, decision matrices + postmortems + persona playlists, Day-One expansion, cspell, practice-question expansion

A large day of structural quality work. Eight themed batches, all on `main`.

### Added

- **Three decision matrices** in `resources/`: `decision-matrix-vector-database.md` (Pinecone / Weaviate / Qdrant / Milvus / pgvector / OpenSearch / Bedrock KB / Vertex Vector Search), `decision-matrix-iac-tool.md` (Terraform / OpenTofu / Pulumi / CloudFormation / Bicep / CDK), `decision-matrix-llm-serving.md` (vLLM / TGI / SGLang / llama.cpp / TensorRT-LLM / hosted). Each scores criteria, names a default pick, and explains when to pick something else.
- **Three postmortem study guides** in `resources/`: `postmortem-aws-s3-2017.md`, `postmortem-cloudflare-regex-2019.md`, `postmortem-gcp-networking-2019.md`. Each maps a real incident to relevant cert exam domains.
- **Four persona playlists** in `resources/`: `playlist-ai-engineer-30min.md`, `playlist-cloud-security-1hour.md`, `playlist-data-engineer-1hour.md`, `playlist-sre-1hour.md`. Reading sequences across existing concept / comparison / reference pages.
- **Four new Day-One beginner pages**: `learn/day-one/ssh-basics.md`, `package-managers.md`, `networking-troubleshooting.md`, `what-is-an-api-call.md`. Day-One went from 5 to 9 pages.
- **Per-topic Mermaid diagrams** added to 6 of 11 topic indexes (databases, iam, kubernetes, networking, observability, security). 10 of 11 topics now have a "topic at a glance" diagram.
- **Per-term glossary anchors** via new `.github/scripts/glossary-add-anchors.py`: 278 `<a id="term-slug"></a>` anchors added to `learn/glossary.md`. New `.github/scripts/glossary-upgrade-existing-links.py` upgraded 38 prior section-level links to per-term anchors. Autolink now prefers per-term anchors when available.
- **cspell workflow** at `.github/workflows/cspell.yml` (non-strict initial run while the dictionary tunes) plus `.cspell.json` with a 150+ word custom dictionary covering cloud + AI proper nouns (Anthropic, vLLM, Pinecone, ExpressRoute, Kerberoasting, etc.).
- **Scenarios + strategy on all 47 senior-tier certs.** Every cert classified senior (AWS Pro / Specialty, Azure Expert / Specialty, GCP Professional, Kubernetes CKS, ISC2 / ISACA, CompTIA mid-senior, Cisco CCNP+, HashiCorp / Databricks / Snowflake "professional" / "advanced", FinOps Professional, VMware VCP, Anthropic Architect Advanced, OSCP, IBM Cloud Security Engineer) now has both `scenarios.md` (6-8 worked exam-style scenarios with options + analysis + takeaway) and `strategy.md` (cert-specific traps, time math, day-of logistics, pattern map). 49 new files, ~50,000 words of original cert-content. Scenarios are illustrative patterns based on each exam's published blueprint - not real exam questions. Files committed in 5 provider-grouped batches (AWS, Azure, GCP, security, other).
- **20 new Mermaid diagrams** across 16 architecture-pattern files (microservices, event-driven, serverless API, multi-region active-active, CQRS / event sourcing, data pipeline ETL, lakehouse, data mesh, ai-ml-pipeline, disaster recovery, hybrid cloud connectivity, zero trust, cell-based, chaos engineering, strangler fig, api gateway) and all 4 networking-deep-dives (DNS hierarchy, hybrid connectivity options, L4 vs L7 load balancing, multi-cloud networking).
- **4 new topic indexes**: `topics/ai-ml-systems.md`, `topics/serverless.md`, `topics/sre-and-reliability.md`, `topics/finops.md`. Each follows the established Learn / Compare / Reference / Build / Certify pattern. `topics/README.md` updated to list all 11 topics.
- **Glossary auto-link script** at `.github/scripts/glossary-autolink.py`. Parses `learn/glossary.md` for bolded terms (335 found) and links the first occurrence in concept + hands-on pages. Caps at 5 links per file; skips code blocks, headings, existing links. Applied: 38 links across 18 files.
- **Repo governance scaffolding**: `.github/PULL_REQUEST_TEMPLATE.md` (matches CONTRIBUTING.md "in scope / out of scope" framing), `.github/ISSUE_TEMPLATE/{bug_report,content_suggestion,cert_request}.md`, root-level `CODEOWNERS`, root-level `.editorconfig`.

### Changed

- **Practice-question banks expanded** for 4 sparse certs from 15 to 25 questions: `kubernetes-cka.md`, `aws-ai-practitioner.md`, `hashicorp-terraform-associate.md`, `isc2-cissp.md`. Same scenario / four-option / analysis / takeaway shape as existing banks.
- **`validate-frontmatter.sh` scope expanded** to also scan `learn/day-one/`, `topics/`, `resources/architecture-patterns/`, `resources/networking-deep-dives/`, decision-matrix / postmortem / playlist files. Backfilled `last-updated` on those file groups.
- **README.md surfaces new content shapes** - decision matrices, postmortem study guides, persona playlists each get a section in the resource navigation; freshness ledger linked from the front door.
- **Tier-aware cert-structure validator.** `validate-cert-structure.sh` now classifies each cert as `senior` or `junior` and only recommends `scenarios.md` + `strategy.md` for senior tiers. Senior = path contains `/professional/`, `/specialty/`, `/expert/`, OR matches a curated cert-basename list (GCP professional certs, Azure expert / specialty, K8s pro, ISC2 / ISACA / OSCP, Cisco CCNP+, HashiCorp / Databricks / Snowflake "professional" / "advanced", FinOps Certified Professional, VMware VCP, Anthropic Architect Advanced, CompTIA mid-senior). Cuts validator warnings from 70 → 0 once senior-cert content was authored.
- **Orphan-link checker root-cause fix.** Two bugs: root-level markdown (README.md, STUDY-HUB.md, CHANGELOG.md, CONTRIBUTING.md, CLAUDE.md) wasn't in the haystack so anything they linked appeared orphan. Cert `notes/*.md` files were considered orphan even when their parent cert directory was referenced. Result: 310 false-positive orphans → 0 true orphans, 289 covered-by-subtree.
- **Glossary autolink + orphan checker** wired up. Test scripts pass cleanly against the current tree.
- **`assets/diagrams/_src/` placeholder cleanup.** Removed `test.drawio` and `test.png` left from initial setup.
- **Three thin certs filled to baseline structure**: `servicenow/csa/practice-plan.md`, `palo-alto-networks/pcnsa/practice-plan.md`, `offensive-security/oscp-pen-200/{fact-sheet,practice-plan,scenarios,strategy}.md`. Real content based on each exam's existing README / blueprint, not boilerplate.

---

## [2026-05-03] - 100% concept-page diagram coverage

### Changed

- **Twelve more Mermaid diagrams** added to the remaining concept pages without one. Every content concept page (36 / 36) now has at least one diagram.
  - Networking / cloud foundations: `cdn-explained` (multi-PoP cache hit/miss with origin), `dns-explained` (sequence diagram of recursive resolution), `regions-and-availability-zones` (single-AZ vs multi-AZ vs multi-region), `iaas-paas-saas` (responsibility layering across all four service models including on-prem), `what-is-cloud-computing` (pre-cloud vs cloud workflow side-by-side).
  - AI / LLM systems: `context-windows-and-management` (stacked context budget with cached vs live tokens), `inference-servers` (continuous batching: clients → queue → batched forward pass → GPU), `multimodal-models` (text + image + audio + video → shared embedding space → LLM), `prompt-engineering` (test-driven iteration loop), `structured-outputs` (prompt + schema → constrained decoder → guaranteed-valid JSON), `evals-for-llms` (dataset + grader + runner → aggregate score → CI).
  - DevOps: `terraform-explained` (code → init/plan/apply with state file as central truth).
- The two ASCII diagrams in `cdn-explained` and `dns-explained` were upgraded to Mermaid for better rendering and accessibility.

---

## [2026-05-03] - Frontmatter scale-out, six more concept diagrams

### Changed

- **Frontmatter backfill on the remaining 123 cert fact-sheets**. Every cert in the freshness ledger now shows a real `last-updated` date instead of "unknown". `validate-frontmatter.sh` goes from 123 warnings to 0.
- **Six new Mermaid diagrams** added to concept pages that previously had no visual: `cicd-explained.md` (pipeline stages with delivery vs deployment branch), `fine-tuning-vs-rag.md` (decision tree: knowledge vs behavior problem), `embeddings-and-vector-search.md` (query → embedding → cosine-similarity ranking), `shared-responsibility-model.md` (IaaS/PaaS/SaaS layered with you-vs-provider color coding), `serverless-explained.md` (sequence diagram of cold start vs warm), `tls-and-https.md` (sequence diagram of TLS handshake including CA chain verification).

---

## [2026-05-03] - Freshness backfill, hands-on index, automation guards

### Added

- **`resources/hands-on-projects/README.md`** - index for all 15 builds with time estimates, "what you'll have at the end" summaries, and a "how to pick" guide. Closes the discoverability gap where projects were only browsable via directory listing.
- **`.github/scripts/validate-frontmatter.sh`** - validates YAML frontmatter on concept pages, top-level learn pages, hands-on projects, and cert fact-sheets. Fails on malformed YAML or bad date format; warns on missing or stale (>180d) `last-updated`. Wired into `structure-validate.yml`.
- **`.github/scripts/check-orphan-links.sh`** - lists `.md` files with no inbound links from other markdown. Manual one-shot, not a workflow gate.
- **Mermaid diagrams** added to `kubernetes-in-10-minutes.md` (control plane + workers + service routing), `iam-explained.md` (authn/authz request flow), `containers-vs-vms.md` (VM vs container layering).

### Changed

- **`last-updated: 2026-05-03` frontmatter backfilled** on the 21 concept pages, 10 hands-on builds, and 12 high-traffic cert fact-sheets (AWS SAA-C03, SAP-C02, CLF-C02, DVA-C02; Azure AZ-104, AZ-900, AZ-305; GCP Cloud Architect, Cloud Engineer; K8s CKA, CKAD, CKS) plus 4 top-level learn pages (ai-from-scratch, cloud-from-scratch, glossary, youtube) that previously had none.
- **`build-freshness-ledger.sh`** now scans concept pages, top-level learn pages, and hands-on projects in addition to cert fact-sheets. Output split into four sections.
- **`docs/freshness.md`** regenerated. Concepts and hands-on sections now show real dates (not "unknown"); cert section still partially "unknown" by design (only top-traffic backfilled this pass).
- **`structure-validate.yml`** workflow renamed to "Structure and frontmatter validate", expanded to trigger on `learn/**` and `resources/hands-on-projects/**`, and now runs the new frontmatter validator.
- **`README.md`** - "I'm here to..." table now points to the new hands-on index (with a "with time estimates" hint) and adds a row for `learn/youtube.md` ("Learn from videos").

---

## [2026-05-03] - Round out the four-pillar repo

Major build-out across all four pillars (Learn / Build / Certify / Reference) to bring the AI side to parity with the cloud side, plus CI automation and a topic-based cross-pillar index.

### Added

- **15 new concept pages** in `learn/concepts/`. AI: tool-use-and-function-calling, mcp-explained, agentic-loops, context-windows-and-management, structured-outputs, multimodal-models, quantization-and-distillation, inference-servers, prompt-caching, guardrails-and-safety. Cloud: iam-explained, queues-vs-streams, observability-basics, eventual-consistency, idempotency-explained. Each is 5-10 min, frontmatter, Mermaid where it adds clarity, cross-links to comparisons / topics / certs.
- **4 AI service comparisons** in `resources/`: vector-databases (Pinecone, Weaviate, Qdrant, Milvus, pgvector, OpenSearch, Azure AI Search, Vertex Vector Search, Bedrock Knowledge Bases, Chroma), genai-platforms (Anthropic, OpenAI, Bedrock, Azure OpenAI, Vertex, Together, Fireworks, Groq), agent-frameworks (Claude Agent SDK, LangGraph, CrewAI, Autogen, OpenAI Agents SDK, Mastra, Semantic Kernel), llm-observability (LangSmith, Langfuse, Helicone, Phoenix, Braintrust, OpenLLMetry, Datadog).
- **5 AI hands-on builds** in `resources/hands-on-projects/`: build-rag-pipeline (pgvector + Anthropic), build-claude-agent-with-mcp (Claude + filesystem MCP + custom sqlite MCP), run-llama-on-single-gpu (vLLM, OpenAI-compatible endpoint), set-up-eval-harness (golden set, regression detection, CI integration), fine-tune-with-lora (Llama 3.2 3B + peft).
- **`topics/` cross-pillar index** - 8 pages (README + iam, networking, databases, llms-and-genai, observability, security, kubernetes). Each topic links across Learn + Compare + Reference + Build + Certify so a non-cert visitor can navigate by subject.
- **CI automation** under `.github/`:
  - `link-check.yml` - lychee link checker (PR, push, weekly Mondays). Opens an issue automatically on weekly failure.
  - `markdown-lint.yml` - markdownlint-cli2 against `.markdownlint.json`.
  - `structure-validate.yml` - runs `validate-cert-structure.sh`. Fails on missing README.md; warns on missing fact-sheet, practice-plan, scenarios, strategy.
  - Local-runnable scripts: `validate-cert-structure.sh`, `build-freshness-ledger.sh`.
- **`docs/freshness.md`** - per-cert "last verified" ledger generated from `last-updated` frontmatter. Initial state: 136 cert dirs, all "unknown" pending opportunistic backfill.
- **Mermaid diagrams** added to `learn/concepts/llm-basics.md` and `learn/concepts/vpc-explained.md` (the prior pages without one).

### Changed

- **README.md front-door reframe** - four-pillar grid promoted above the cert tables. New "I'm here to..." quick-nav with explicit non-cert paths. Per-provider deep-dive sections cut (now in STUDY-HUB only) since they were duplicated. "What's new" callout linking CHANGELOG. Stat counts updated for new concepts, comparisons, builds, topics.
- **STUDY-HUB.md** - quick-nav adds `topics/` and the freshness ledger. Service comparisons split Cloud / AI. Hands-on Projects line updated to 15 builds.
- **`learn/concepts/README.md`** - all 15 new pages indexed across new sub-categories (AI foundations / building / operations; cloud now has IAM, observability, eventual consistency, idempotency, queues vs streams sections).
- **`assets/diagrams/README.md`** - documents that `_src/` is tracked in git (was untracked).
- **`CONTRIBUTING.md`** - documents the local validator scripts and CI workflows.
- **`CLAUDE.md`** - adds an Automation section pointing to the validator scripts and freshness ledger.
- **`.markdownlint.json`** + **`.lycheeignore`** - new config files at repo root.

---

## [2026-05-03] - Scope expansion: cloud + AI learning, not just certs

### Added

- **`learn/concepts/` AI pages** - 8 promised but missing concept files: llm-basics, transformer-architecture, embeddings-and-vector-search, prompt-engineering, rag-explained, fine-tuning-vs-rag, agents-explained, evals-for-llms. Each is a 5-10 minute plain-English explanation.
- **`learn/day-one/`** - strict beginner on-ramp for people who have never opened a terminal. 5 pages: README, terminal-basics, git-basics, http-and-apis, what-is-a-server.
- **`assets/diagrams/`** - canonical home for PNG diagrams (draw.io exports), organized by topic.
- **Mermaid diagrams** seeded in 3 high-ROI pages: `learn/cloud-from-scratch.md` (region/AZ/subnet topology), `learn/ai-from-scratch.md` (RAG pipeline), `resources/architecture-patterns/web-app-3-tier.md` (3-tier flow). Plus inline mermaid in transformer-architecture.md, rag-explained.md, agents-explained.md, what-is-a-server.md.
- **Visual content standards** in `docs/ARCHITECTURE.md` and `CLAUDE.md`: PNG via draw.io MCP is canonical, Mermaid is an acceptable inline fallback.
- **YAML frontmatter convention** documented in `docs/ARCHITECTURE.md` (`last-updated`, optional `applies-to`, `difficulty`, `reading-time`). Backfill is opportunistic.
- **YouTube tie-in convention** documented in `CONTRIBUTING.md` for connecting topic pages to companion videos on @patrickwiloak.

### Changed

- **README.md repositioned** as cloud + AI learning resource (zero to hero), not cert-only. New hero, new "Four Pillars" section (Learn / Build / Certify / Reference), reordered "What's Inside" to lead with `learn/`. The "122+ certifications" social proof is preserved as the second sentence.
- **STUDY-HUB.md repositioned** as "Cloud + AI Learning Hub" with a new "Not chasing a certification?" section pointing to `learn/`. Cert decision tree is preserved.
- **CLAUDE.md (project)** rewritten to reflect 4-pillar scope, new directory structure, visual content standards, and frontmatter convention.
- **CONTRIBUTING.md** updated with `learn/` contribution rules, diagram expectations, frontmatter expectations, and YouTube tie-in convention.
- **`docs/ARCHITECTURE.md`** - "At a glance" tree updated to include `learn/` and `assets/diagrams/`. New sections: Visual content standards, Frontmatter convention. Repo description broadened.
- **2 career roadmaps retrofit** with "Foundation Concepts" + "Hands-on builds" cross-link sections (cloud-engineer, ai-ml-engineer). Rest are deferred to a follow-up pass. Body content untouched.
- **`learn/README.md`** - reordered to lead with Day One on-ramp, then Concepts, then structured paths. "Coming soon" markers removed - concept pages are shipped.
- **`learn/concepts/README.md`** - added a Day One callout for absolute beginners.

---

## [2026-04-27] - Gap fix and provider expansion

### Added

- **AWS Certified Data Engineer - Associate (DEA-C01)** - full Associate-tier scaffold (README, fact-sheet, 6 notes, practice-plan, scenarios, strategy). The current AWS data-engineering credential, replacing the retired DAS-C01 and DBS-C01.
- **Red Hat certifications** - new provider section with two starter certs:
  - **RHCSA (EX200)** - Red Hat Certified System Administrator
  - **OpenShift Administrator (EX280)** - Red Hat Certified Specialist in OpenShift Administration
- **Cisco CCNA (200-301)** - new provider section with foundational networking cert
- **Azure Microsoft Fabric Data Engineer (DP-700)** - newer Azure cert
- **Azure Network Engineer Associate (AZ-700)** - missing Azure networking cert
- **Microsoft 365 Fundamentals (MS-900)** - foundational M365 cert
- **Salesforce Administrator (ADX-201)** - new provider section, foundational admin cert
- **Salesforce Platform Developer I (DEX-450)** - developer cert
- **Practice question banks** for 10 previously-uncovered popular certs: CKA, Terraform Associate, CISSP, Databricks DE Associate, FinOps Practitioner, AWS AI Practitioner, AWS MLA-C01, Azure AI-102, Snowflake SnowPro Core, RHCSA + CCNA
- **Cloud Practitioner fact-sheet** (was missing despite existing notes and practice-plan)
- **`.templates/resources-{aws,azure,gcp}.md`** - centralized study-resources hub pages referenced from many cert dirs
- **CONTRIBUTING.md** - contribution scope, cert template, link format, retirement workflow, PR checklist
- **CHANGELOG.md** - this file
- **docs/ARCHITECTURE.md** - repo-structure and conventions doc for contributors

### Changed

- **Anthropic certs relabeled as study tracks**. Anthropic does not currently run an official certification program; the four guides under `exams/anthropic/` are now framed as self-directed Claude proficiency tracks.
- **AWS Quantum Practitioner relabeled as anticipated study track**. AWS has not formally announced QPC-C01.
- **Azure GenAI dir relabeled as cross-cert GenAI study track** (was confusingly framed as a specific AI-102/AI-900 variant)
- **GCP GenAI dir relabeled as cross-cert GenAI study track** (was framed as Professional ML Engineer; that cert lives in `exams/gcp/machine-learning-engineer/`)
- **GCP Professional Cloud Architect dirs deduplicated** - merged `exams/gcp/pca/` into `exams/gcp/cloud-architect/`. Cert count dropped from 13 to 12 GCP certs.
- **Counts in README, STUDY-HUB, and CLAUDE.md updated** to reflect actual contents (now 117+ certs across 21 providers, plus 4 vendor study tracks)
- **Roadmap files updated** to reference current AWS certs:
  - `certification-roadmap-cloud-engineer.md` - SOA-C02 → SOA-C03; MLS-C01 → MLA-C01; added DEA-C01
  - `certification-roadmap-ai-ml-engineer.md` - MLS-C01 → MLA-C01
  - `certification-roadmap-solutions-architect.md` - MLS-C01 retired note
  - `certification-roadmap-database-specialist.md` - DBS-C01 retired note + DEA-C01 as replacement
- **Heavy-offender README files rewritten** to match files actually on disk (Oracle x5, IBM x5, Azure AZ-305, AWS SAP-C02, AWS/Azure/GCP GenAI dirs)
- **All 317 broken internal links repaired** through a combination of new files (templates, missing fact-sheets) and corrected references
- **Provider integration into roadmaps**: Red Hat added to platform engineer roadmap; Cisco CCNA added as networking foundation in cloud engineer roadmap
- **STUDY-HUB decision tree, study tracks, and provider table** updated to include Red Hat / Cisco / DEA-C01 / Anthropic study-track separation

### Marked as retired

The following AWS specialty exams were retired by AWS but the study material is preserved for credential holders. Each now has a consistent `RETIRED [DATE]` banner on README and fact-sheet pointing to the modern replacement:

- **AWS Data Analytics Specialty (DAS-C01)** - retired April 8, 2024 → DEA-C01
- **AWS Database Specialty (DBS-C01)** - retired April 29, 2024 → DEA-C01
- **AWS Machine Learning Specialty (MLS-C01)** - retired April 15, 2025 → MLA-C01
- **AWS SysOps Administrator (SOA-C02)** - retired Sept 29, 2025 → SOA-C03 CloudOps Engineer

### Removed

- `exams/gcp/pca/` directory (merged into `exams/gcp/cloud-architect/`); 4 internal roadmap link references updated

### Documentation

- All retired-cert references in active roadmap files now have RETIRED banners
- Anthropic is now consistently presented as study tracks (not certifications) across README, STUDY-HUB, all 4 cert dirs
- Provider count corrected in README, STUDY-HUB, and CLAUDE.md from 19 to 21
- Cert count corrected from 118+ to accurate 117+ + 4 study tracks
- README structure section updated to reflect the new dir layout
- Internal link audit: 0 broken links remain (verified with code-block-aware scanner across all 700+ markdown files)

---

## [2026-04 prior] - Project state before this changelog

The repository existed prior to this entry. Before 2026-04-27, the catalog claimed:

- 118+ certifications across 19 providers
- 12 cross-cloud service comparisons
- 9 CLI cheat sheets
- 17 architecture patterns
- 11 certification roadmaps
- 10 hands-on projects
- 6 interview prep guides
- 5 compliance and 5 migration guides

That state had documentation drift: a duplicate GCP PCA dir, Anthropic certs framed as official, several AWS specialties listed as active despite being retired, broken internal links in dozens of cert READMEs, and a missing CONTRIBUTING.md referenced from the main README. The 2026-04-27 work above resolved those issues.

---

## How to update this changelog

When making user-visible or operationally-significant changes:

1. Add a dated section at the top using `## [YYYY-MM-DD] - Brief description`.
2. Group entries under: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**.
3. Link to the cert dir or resource file affected.
4. Keep entries concise (one line per item); link out for detail.
5. New cert additions, retirements, schema changes, and provider sections are always logged here.
6. Typo fixes and minor link repairs do not need a changelog entry.
