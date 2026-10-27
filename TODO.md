# TODO

Working task list for **cloud-zero-to-hero** (Cloud Zero to Hero, https://cloud.noblerworks.com/). Read this at the start of a work session and keep it current as work completes - check items off with a date, add follow-ups as they surface. Stale TODOs are worse than none. Security debt (if any) is tracked separately in `SECURITY-DEBT.md`.

---

## Community (2026-10-27)

- [ ] 2026-10-27 Reply to outside PR #13 (Joehonathon, A+ PBQ resource, open since 2026-10-19) - merge or explain.
- [ ] Link check #12: 28 errors (SAP training, Power Platform blog 404s; GCP "connection failed" is CI-side) - fix real 404s.


## Zero to Hero split (2026-10-21)

- [x] 2026-10-21 Split from cloud-data-ai-security-zero-to-hero on 2026-10-21: data, security and AI content (and their TODO items) moved to data-zero-to-hero, security-zero-to-hero and ai-zero-to-hero; this repo is Cloud Zero to Hero. README, STUDY-HUB, home page, CLAUDE.md, CONTRIBUTING, docs/ARCHITECTURE.md, mkdocs.yml, social card and repo-metadata template rewritten for cloud only.
- [x] 2026-10-21 Repo renamed to `cloud-zero-to-hero`; `check-repo-metadata.py --fix` run (description, homepage).
- [x] 2026-10-27 (custom preview set) Patrick: upload `assets/brand/social-preview-1280x640.png` at GitHub Settings > General > Social preview (no API). Card is the shared Zero to Hero template (`assets/brand/social-preview.html`, 2026-10-21).

---

## Dependabot sweep (2026-10-13)

- [x] 2026-10-13: site toolchain bumped to Pygments 2.21.0, Markdown 3.11, pymdown-extensions 12.1 (#3, #8, #9). Both old and new pins build `--strict` clean; the rendered diff is `&quot;` -> `"` inside code blocks plus small lexer re-tokenisation in 11 pages (shell `case`); no `<em>`/`<strong>` changed despite pymdown 12's BetterEm rewrite.

## Refactor audit (2026-10-01) - found, not started

Read-only fleet audit (9 agents, nothing changed). Each line: effort S (<half day) / M (1-3 days) / L, and the risk of making the fix. 🔴 = a live bug or safety hole.

- [ ] 🟡 `.github/scripts/site_hooks.py` has drifted 360 diff lines from ai-zero-to-hero's port (was genai-research-papers-summarized) - one canonical module both vendor (with a sync check), or record the fork in both. S-M, low.
- [ ] 🟡 Confirm and delete the one-time `glossary-add-anchors.py`, `glossary-autolink.py`, `glossary-upgrade-existing-links.py`. S, low. (checked 2026-10-01, kept: not in CI/hooks, but `.github/AUTOMATION.md` + `CONTRIBUTING.md` document all three as the manual pipeline to re-run on new glossary terms, so they are not one-time migrations. Delete only if that pipeline is retired; roadmap 4.4 covers wiring them.)

## Audit findings (2026-10-02)

- [x] 2026-10-02 🟡 medium - Home page bio hard-coded stale cert counts (`.github/site/home.md:129`, "60 ... 18x"): numbers removed ("multi-cloud certified"); `build-site.py --strict` passes. Goes live on the next push to main (Pages workflow).
- [x] 2026-10-02 🟢 low - README Nobler banner was hotlinked from `Noblerworks/IRONSIGHT`: vendored to `assets/brand/nobler-works-banner.jpg`.
- [ ] 🟢 **Patrick: decide** whether the bio should carry a cert count again. If yes, add a `{{personal_certs}}` token in `build-site.py` fed from one checked-in value, and update it on 2026-10-21 / 2026-11-05 (lapses) - the private career ledger cannot feed CI.
- [ ] 2026-11-05: Database Specialty lapses - `README.md` (lines ~53 and ~409) and `learn/README.md` line 5 go from 19x multi-cloud / 14x AWS / 64 to **18x / 13x / 63**. (2026-10-20: swept 20x / 15x / 65 -> 19x / 14x / 64 for the 2026-10-21 ML Specialty lapse; source `go-to-market/claims.md`.)

## Retired-exam sweep (2026-10-16)

- [x] 2026-10-16 Checked every Azure guide against Microsoft's [retired-exams page](https://learn.microsoft.com/en-us/credentials/support/retired-certification-exams): nine were retired but unflagged. Now marked RETIRED with `exam-retires:` (status flips to Retired in `certs.json` and the provider tables): MS-900 (2026-03-31), DP-100 (06-01), AI-102 (06-30), AI-900 (06-30), AZ-204 (07-31), AZ-500 (08-31), PL-200 (08-31), plus DP-203 (2025-03-31, date from Microsoft Q&A and third-party posts, not the page) and PL-100 (2024-06-30). The only Azure exam on Microsoft's "retiring in 12 months" list is MS-102, which the repo does not cover.
- [ ] **Successors not built or verified.** Third-party posts report AZ-204 -> AI-200; confirm on learn.microsoft.com before writing any guide. Retired guides (MS-900, AZ-204, PL-100, PL-200) still have practice banks, flashcards and `labs-by-cert` entries; decide whether to keep them as reference or prune.
- [x] 2026-10-16 Ran the same check on the other 26 providers (vendor pages, three read-only agents). Flagged: SCS-C02, MLA-C01 and HashiCorp Consul 003 as retired; SAP-C02 (2026-11-16), DVA-C02 (11-30), ANS-C01 (12-31) and CySA+ CS0-003 (12-22) as retiring. Everything below was found but NOT applied, because the evidence is a search snippet or third-party only, or it needs a content rewrite. Confidence in brackets (H = vendor page read, M = vendor page plus search, L = third-party).
- [ ] **Rewrites that wait on new outlines.** AWS SAP-C03 and DVA-C03 (registration opens 2026-10-27; build after the outlines publish), Azure exams with content updates AZ-305 (updated 04-17) and AZ-400 (07-27) [H]. RHCSA EX200 is now based on RHEL 10 and the guide says RHEL 9 [H]; EX280 may be on OpenShift 4.22 vs the guide's 4.14 [M]. **Judge 2026-11-01:** which of these are rebuilt or dated.
- [ ] **Version or code mismatches to confirm, then fix.** HashiCorp Terraform Associate 003 -> 004 (last day for 003 reported as 2026-01-07, from search not the page [M]); Oracle OCI codes -24/-25 are stale (-26 pages exist for Foundations, Architect Associate and Professional [H]; Developer is "Developer Professional" in the catalog [M]); FinOps analyst is "FinOps Certified FOCUS Analyst" and the code "FOCA" is unsourced [L].
- [ ] **Facts that are wrong in the guides.** GitHub: Administration says 3-year validity; GitHub certs are valid 2 years [H]. (Actions and Foundations fixed 2026-10-22.)
- [ ] **Guides that may not describe a real exam.** HashiCorp `nomad-associate` and `packer-associate` have no vendor exam on HashiCorp's lists [M]. The IBM guides pair "IBM Certified ... Cloud v2" titles with codes C1000-170..174 that third-party listings give to other exams (the Advocate code is probably C1000-142) and IBM's pages were unreadable [L]. **Patrick or a fresh session: check ibm.com/training and each of these exam pages by hand before editing.** Also unverified: VMware 2V0-21.23 (Broadcom page unreadable), Salesforce Admin/PD1/PD2, AWS PAS-C01 (not on AWS's landing page).
- [ ] **New-guide candidates found** (verify codes first): Terraform Infrastructure Engineer Pro; CNCF CNPE, CKNE, KCA, CBA; FinOps AI Value and Technology Value; GitHub GH-600 [L].

## Stale cert-page domains (found 2026-10-22, bank expansion)

- [x] 2026-10-22 Cert pages restructured to current guides: GH-200, GH-900, Cloud+, KCNA, SOA-C03, AZ-700, PCNE, Terraform Advanced.
- [ ] 2026-11-15 Verify from-memory details flagged in the 2026-10-22 rewrites: PCNE gcloud flags (`--bgp-bps-*`, `firewall-rules migrate`, PBR next hop, Secure Web Proxy import) and Terraform Advanced OPA Rego sample (`notes/06-hcp-terraform.md`).
- [ ] 2026-11-01 Reconcile README vs fact-sheet domains/weights: IBM Cloud x4 (Advocate code C1000-176 vs -170), OCI x5 (also -24 codes), PL-900; banks follow the fact sheets.
- [ ] 2026-11-01 Check whether VCP-DCV 2V0-21.23 is superseded and Salesforce Administrator is now "Platform Administrator"; fix stale IBM doc links (`account-iamoverview`, `account-costs` 404).
- [x] 2026-10-22 All 39 remaining 15-question banks expanded to 30 (new questions carry Key Concept links; Q1-15 in those banks do not).

## Content backlog (gap review 2026-10-16, ranked)

1. **Outage postmortems** beside the 3 existing ones: CrowdStrike 2024 and the Oct 2025 AWS us-east-1 DNS event.
2. **Cert gaps**: observability (Splunk/Elastic/Datadog), CNCF Backstage and Kyverno associates, plus the Linux+ item below.
3. **Concept pages**: day-one Python still open (DR/RPO-RTO and environment variables shipped 2026-10-21).

## Concept gap fill (2026-10-21)

- [x] 2026-10-21 14 concept pages, 3 day-one pages, 2 projects (landing zone, GitOps with Argo CD) added and wired in; see git log.
- [ ] 2026-11-04 Run `gitops-with-argo-cd.md` end to end on kind and fix any command that fails (written, not executed).
- [ ] 2026-11-04 Dry-run `build-a-landing-zone.md` in a throwaway AWS org (never in NW `791588190257` or a client account); fix commands.
- [ ] 2026-11-04 Add glossary terms the new pages use but `learn/glossary.md` lacks: RPO, RTO, landing zone, SCP, golden path, SPOF.
- [ ] 2026-11-04 App Mesh reached end of support 2026-09-30: drop it from mesh rows in `resources/service-comparison-*.md`, `microservices-architecture.md`, `certification-roadmap-kubernetes-specialist.md`.

## GCP exam refresh (2026-10-14)

- [x] 2026-10-14 Workspace Administrator re-levelled to Associate and rebuilt (7 notes, flashcards, 23 scenarios, 45 questions). Strict site build passes; pushed 2026-10-14.
- [x] 2026-10-14 Cloud Architect refreshed to the current guide: weights, four case studies (own words), AI / Agent Platform note, Well-Architected and operations note, 26 new questions, 6 scenarios, shuffled answer key, dead guide link fixed.
- [ ] **Rename sweep.** The older Cloud Architect notes (and `resources/`) still say "Vertex AI". Google renamed it Gemini Enterprise Agent Platform on 2026-04-22. Sweep once the names settle; the new AI note carries the mapping.
- [x] 2026-10-14 Answer-position skew fixed repo-wide (150 banks, 2,904 questions) with `.github/scripts/balance-answer-positions.py`.
- [x] 2026-10-14 Length tell fixed: the correct option was the longest in 88% of questions; a first fix overshot to the shortest in 38%, so a second pass assigned each question a target length rank. Both `--check` and `--check-length` now run in the structure-validate workflow. The 76 cross-referencing questions were rewritten; the `offensive-security-oscp.md` stub was deleted (duplicate of `oscp-pen-200`).
- [x] 2026-10-14 The ~70 flagged practice-question keys were checked against vendor docs (AWS, Microsoft, Google, Kubernetes, Snowflake, Databricks, GitHub, Confluent and others) by sourced agent review; 18 keys or questions were corrected and the rest confirmed or tightened. Outcome and sources: [docs/practice-question-key-review.md](./docs/practice-question-key-review.md). Still open there: a handful of unverified facts (IBM Cloud Functions end date, "Anthos is GKE Enterprise", Azure AD naming in az-104/204/305) and the judgment-call questions.
- [x] 2026-10-14 Spot-read 24 random AI-rewritten questions across 24 banks: all had exactly one correct option matching the key. That is 0.8% of the bank, a sanity check and not an audit; keep sampling banks you study from.
- [x] 2026-10-14 "Vertex AI" renamed to the Gemini Enterprise Agent Platform names across exams, resources, topics and practice banks (about 480 replacements, using Google's 56-row rename table; first mention in each file reads "(formerly Vertex AI)"). Left as "Vertex AI" because the table has no entry: Vizier, Explainable AI, Hyperparameter Tuning, Metadata, Components and similar (about 88 lines). Anthos wording not changed (rename to GKE Enterprise not confirmed in Google docs).
- [ ] **By 2026-12-01: re-check both exam guides** (Associate Workspace Administrator and Professional Cloud Architect PDFs) for revisions, and update `last-updated`. The PCA guide already mentions products renamed in 2026 (Agent Platform), so expect churn.
- [ ] Scenarios for Workspace (`scenarios.md`) still skew to answer B in places; shuffle when next edited (the analysis text names option letters, so edit by hand).

## Open

### 🔴 Link rot backlog (added 2026-09-17, cleared 2026-09-18)

The external link checker had never run (see CHANGELOG 2026-09-17). Sweeps on 2026-09-17/18
checked every external URL for hard 404s, soft 404s and deep links lost to a redirect: **783 dead,
all 783 now repaired**, each replacement fetched and title-checked. The old-to-new record is
[docs/link-rot-2026-09-17.md](./docs/link-rot-2026-09-17.md).

- [x] ~~Decide what to do with the 480 unrepairable links~~ ✅ done 2026-09-18: each repaired by hand to the
      closest live page on the same subject; 6 Amazon QLDB links point at pinned Internet Archive snapshots.
- [x] ~~Your own blog link is dead~~ ✅ done 2026-09-18: the post went with the blog on 2026-09-05. README
      mentions dropped, site footer now links to patricklukewilson.com.
- [x] **Judge by 2026-09-22**: the first repaired weekly link check runs Monday 06:00 UTC. The after-repair run on
      2026-09-18 counted 895 errors across 21,983 checks before this last batch; expect far fewer. Whatever it still
      opens an issue for should be rate limits and bot walls (the 62 below), not removed pages. Open the issue and
      re-check any real 404 in it.
      ✅ 2026-10-02 judged: **the check works, the expectation half-held.** Scheduled runs 2026-09-21 and 09-28 each
      walked 21,981 links in ~32 min (vs 9-14 s before the repair) and opened issues #6 (348 errors) and #7 (405).
      Of #7's errors: 279 `ERROR` are connection failures, 252 of them `cloud.google.com` (rate limiting); all 44 unique
      `cloud.ibm.com` "404"s answer **200** to a browser user agent (bot wall, false). **29 unique URLs are real 404s**
      (re-checked with curl, browser UA, 2026-10-02) - new rot since the 09-18 sweep: GCP cert guides (cloud-developer,
      cloud-network-engineer, professional-cloud-architect, cloud-devops-engineer) and three migration-to-gcp pages,
      finops.org (2), FOCUS_Spec, isc2 CCSP outline, isaca maintain-cert, OWASP LLM03/LLM06, AWS docs (ecr/ecs/sqs
      guide roots, migration evaluator, prescriptive migration guide, PCI scoping whitepaper), az500 lab site,
      pennylane braket, aws quantum research, terraform cert tutorial, LF Argo APA, litmuschaos docs, two IBM sdk-core
      example trees. Two side findings: the issue body is cut at GitHub's 65,536-char limit (the list is incomplete),
      and each week opens a NEW issue without closing the last (#6 and #7 both open).
- [x] **By 2026-10-12: repair the 29 real 404s** listed in the judge line above (same method as the 09-17 sweep:
      fetch + title-check each replacement), then close issues #6 and #7. Consider: accept IBM (`--exclude
      cloud.ibm.com` or treat as bot wall), make the workflow close/update the previous week's issue, and attach the
      full lychee report as an artifact since the issue body truncates.
      ✅ 2026-10-15 done: **32 repaired** (the 29 plus 3 new in the 10-15 lychee report artifact) across 26 content
      files; each replacement fetched and title-checked, old-to-new list in `docs/link-rot-2026-09-17.md`
      "Follow-up repairs 2026-10-15". `check-internal-links.py`: 5,106 internal links, 0 broken. Issues #6, #7, #10
      and #11 closed. The three workflow ideas above are not done - next line.
- [x] 🟡 `link-check.yml`: close/update the previous week's issue instead of opening a new one each Monday,
      and decide on the 44 `cloud.ibm.com` bot-wall "404"s (exclude or accept). The report artifact already exists
      (`lychee-report`). S.
      ✅ 2026-10-17 `--exclude 'cloud\.ibm\.com'` added to the lychee args; the issue step now looks up the open
      `link-check` issue (`gh issue list`) and passes it to peter-evans as `issue-number`, so the Monday report
      rewrites that issue instead of opening a new one (no open issue -> it opens one). YAML parses; NOT run in
      Actions (nothing pushed).
- [x] ✅ 2026-10-22 judged the 10-19 run: opened #12 (no open issue existed, so the update path is still unrun); 3 real breaks fixed here, the rest moved to data/ai repos in the split.
- [ ] **Judge 2026-10-27:** the 10-26 Monday run rewrites #12 instead of opening #13 (`gh issue list --label link-check`).
- [ ] 🟡 Link-check noise: 130 of #12's 257 errors are `cloud.google.com` refusing the Actions runner ("Connection failed"); lower lychee concurrency for that host or exclude it. S.
- [ ] **Spot-check the retired-product replacements (by 2026-10-31).** These links now reach the successor product,
      but the surrounding notes may still teach the retired one: OpsWorks, IBM Watson and Cloud Foundry
      (`exams/ibm`), AWS SAP specialty exam. The report lists every replacement.
- [ ] **Content checks the sweep surfaced** (links fixed, content may be stale):
  - 15 citations of retired IBM services now point at the official successors (listed in the report); the surrounding IBM notes may describe the retired products.
- [ ] **62 URLs could not be checked** (bot protection or sign-in, mostly vendor cert pages and Cisco docs). Spot-check by hand; listed at the end of the report.

### 🟠 Discoverability (added 2026-08-31, updated 2026-09-17)

- [x] ~~Per-page meta descriptions, shorter titles, BreadcrumbList JSON-LD, IndexNow on deploy~~ ✅ done 2026-09-28
      (CHANGELOG 2026-09-28). Baseline for judging it, GitHub traffic 2026-09-14..28: 248 views / 99 uniques;
      referrers github.com 13, chatgpt.com 10, Bing 6, Google 5, DuckDuckGo 1. 40 stars, 20 forks.
- [x] ~~Google Search Console property~~ ✅ done 2026-09-28: URL-prefix property
      `https://cloud.noblerworks.com/` verified by meta tag
      (`mkdocs.yml` `extra.google_site_verification`) through the Site Verification API as the `nobler-reporting`
      service account (API enabled on project 822136630919 for this). Owners: that SA and pat@noblerworks.com.
      `sitemap.xml` submitted the same day.
- [ ] **2026-11-01 check** (re-dated 2026-10-15 after the FAIL below; was 2026-10-12): Search Console → Sitemaps shows the sitemap as read (not pending) with ~2,000
      discovered URLs, and Pages → Indexed is above zero.
      ✏️ 2026-10-15 judged: 🟠 HALF - the sitemap (submitted 2026-09-29) is still `isPending: true`, never
      downloaded, 0 errors, so Google has discovered none of the 2,066 URLs from it. Indexed IS above zero: the home
      page is "Submitted and indexed" (crawled 2026-09-29), and 1 page had 8 impressions / 1 click 09-15..10-14;
      `/STUDY-HUB/` is "URL is unknown to Google". The sitemap serves fine (200, `application/xml`). Read via the GSC
      API as `nobler-reporting`. Next (Pat, 2026-10-28, browser): resubmit the sitemap and Request indexing on
      `/STUDY-HUB/`; re-check 2026-11-01.
- [ ] **Patrick: unblock site analytics (2 steps, ~3 min), then hand back to Claude.** The site has no analytics
      at all; the only visitor numbers are GitHub's 14-day repo traffic. Plan agreed 2026-09-28: GA4 behind
      Material's cookie consent banner (feeds the Nobler OS dashboard) **plus** Cloudflare Web Analytics
      (cookieless, no banner, the honest full count - GA undercounts EU visitors who decline).
  - **GA4:** the `nobler-reporting` SA is only *Viewer* on the NoblerWorks GA account (403 creating a property).
    Either (a) GA Admin → Account access management → add `nobler-reporting@nobler-os.iam.gserviceaccount.com`
    as **Editor** (then Claude creates this and future properties), or (b) create property "Zero to Hero" with a
    Web stream for the site URL yourself and give Claude the `G-…` ID and the numeric property ID.
  - **Cloudflare:** sign up free at dash.cloudflare.com → Analytics & Logs → Web Analytics → Add a site →
    `patrickwiloak.github.io`, **JavaScript snippet** option (not automatic setup) → give Claude the `token`.
  - **Then Claude:** GA via `extra.analytics` + `extra.consent` in `mkdocs.yml`; Cloudflare beacon in
    `.github/site-overrides/main.html`; add the property to Nobler OS (see nobler-os TODO.md); confirm hits in both.
  - **Then Patrick, one click:** GA Admin → Search Console links → link the property to the Search Console
    property created 2026-09-28 (no API for this).
- [ ] **Patrick: Bing Webmaster Tools** → Import from Google Search Console once the property above exists
      (IndexNow already pings Bing on every deploy; Webmaster Tools shows what it did with them).
- [x] ~~IndexNow first submission~~ ✅ done 2026-09-28: the deploy step got the expected first-run 403
      `SiteVerificationNotCompleted`; `notify-indexnow.py --all` minutes later was accepted (HTTP 200, 2,043 URLs).
- [x] 2026-10-20 ✅ **2026-10-05 check** (✏️ 2026-10-20: run 39078323231, 2026-10-17, prints `IndexNow: 2 URL(s)` / `IndexNow accepted: HTTP 200`): open the next "Docs site" run's "Notify IndexNow" step; it should now say
      `IndexNow accepted`. If it 403s again, the key file at the site root is not being served - check
      `https://cloud.noblerworks.com/<key>.txt` (key in `.github/site/indexnow-key.txt`).
- [ ] **2026-10-28 judge**: re-pull `gh api repos/PatrickWiloak/cloud-zero-to-hero/traffic/popular/referrers`.
      Target: Google + Bing referrals above 11 per 14 days (baseline above), and new pages showing in
      Search Console → Pages → Indexed (if the property exists by then).
- [x] 2026-10-21 Moved to `cloud.noblerworks.com` (Route 53 CNAME, NW) + robots.txt; no redirect needed (never indexed).
- [ ] 2026-10-28 Patrick: Search Console `sc-domain:noblerworks.com` -> submit `https://cloud.noblerworks.com/sitemap.xml`.
- [x] ~~CompTIA A+ (220-1201/1202)~~ ✅ done 2026-09-28 - the biggest-search-volume gap.
- [ ] **By 2026-10-31: confirm the A+ voucher price** on the CompTIA store (US) and replace the "not verified"
      line in `exams/comptia/a-plus/fact-sheet.md` (CompTIA renders prices client-side; no official figure was readable).
- [ ] **Remaining high-search cert gap**: CompTIA **Linux+**.
- [ ] **Patrick: start a fresh Claude session for the next cert guide** - **Linux+**. On 2026-09-29 a Linux+ attempt
      was stopped by the safety check in the
      same session as the CEH stops, most likely carried over from that session's history; nothing was written.
      A new session does not carry that history. Prompt: "add the <cert> study guide to zero to hero, same shape as
      A+ (see TODO.md)". Template is the A+ commit `94bd744` plus follow-up `105cd98` (lab map, flashcards). Do not
      include CEH in that session.
- [ ] **Patrick: distribution** (stars come from here, not from SEO). Submit to awesome lists
      (awesome-certifications, awesome-aws, awesome-azure, awesome-kubernetes); post one
      useful page each to r/AWSCertifications, r/AzureCertification, r/CompTIA, r/kubernetes, linking back.
- [x] ~~Commit and push `LICENSE` (CC BY 4.0) and `LICENSE-CODE` (MIT)~~ ✅ done 2026-08-31 in
      f3b8faf. GitHub reports the repo as CC-BY-4.0.

Backlog derived from the repo-wide gap analysis in
[docs/improvement-roadmap.md](./docs/improvement-roadmap.md) (2026-07-28). See that
document for evidence, counts, and reasoning behind each item.

Add items as `- [ ] task`, grouped by priority or theme. Mark done inline:
`- [x] ~~task~~ ✅ done YYYY-MM-DD`.

### Priority 1 - correctness

- [x] ~~Fix `build-freshness-ledger.sh` path bug, then regenerate `docs/freshness.md`~~ ✅ done 2026-07-29 (cleared 191 broken links)
- [x] ~~Rewrite 87 absolute `/exams/...` links as relative~~ ✅ done 2026-07-29
- [x] ~~Repoint or remove 28 links to the old directory layout~~ ✅ done 2026-07-29
- [x] ~~Update `STUDY-HUB.md` provider table~~ ✅ done 2026-07-29 (added ISACA, Offensive Security, Palo Alto, ServiceNow, VMware; corrected AWS 18, CompTIA 4, Cisco 2, Salesforce 3)
- [x] ~~Update cert/provider badge counts~~ ✅ done 2026-07-29 (133 certs / 26 providers, not 127/27 - see note below)
- [x] ~~Split `link-check.yml` into a blocking internal-link job and an advisory external-URL job~~ ✅ done 2026-07-29
- [x] ~~Fix cert discovery in `validate-cert-structure.sh` and `build-freshness-ledger.sh`~~ ✅ done 2026-07-29

> **Count correction.** The gap analysis first reported 127 certs because both scripts
> discovered cert dirs by looking for a `notes/` subdir, which skipped the 10 certs whose
> notes were never drafted. Counting by `fact-sheet.md` gives 137 cert dirs: 133
> certifications across 26 providers, plus 4 Anthropic study tracks. Both scripts now use
> `fact-sheet.md`, so the validator checks all 137 instead of 127.

### Priority 2 - content substance

- [x] ~~Write notes for the 10 outline-stage certs~~ ✅ done 2026-07-29. All now active with drafted notes, links restored, banners removed. No cert is at outline stage.
  - [x] ~~comptia/cysa-plus~~ (4 notes)
  - [x] ~~comptia/network-plus~~ (5 notes)
  - [x] ~~cisco/ccnp-enterprise-encor-350-401~~ (6 notes)
  - [x] ~~isaca/cisa~~ (5 notes)
  - [x] ~~isaca/cism~~ (4 notes)
  - [x] ~~offensive-security/oscp-pen-200~~ (6 notes)
  - [x] ~~palo-alto-networks/pcnsa~~ (4 notes + scenarios + strategy)
  - [x] ~~salesforce/platform-developer-2~~ (6 notes + strategy)
  - [x] ~~servicenow/csa~~ (6 notes + scenarios + strategy)
  - [x] ~~vmware/vcp-dcv-2v0-21-23~~ (6 notes)
- [x] ~~Resolve the diagram standard~~ ✅ done 2026-07-29 - Mermaid is now the documented default, PNG the exception. Updated `CLAUDE.md`, `docs/ARCHITECTURE.md`, `CONTRIBUTING.md`, `assets/diagrams/README.md`.
- [x] ~~Add index READMEs to the 21 provider directories that lack one~~ ✅ done 2026-07-29 (all 27 now generated from `docs/certs.json`; the 6 hand-written ones kept their editorial content)
- [x] ~~Complete `aws/professional/genai-developer-aip-c01`~~ ✅ done 2026-07-29 - practice-plan, scenarios, strategy written. Structure validator is at zero warnings.
- [x] ~~Move `exams/aws/genai` under `foundational/`; reconcile `azure/genai` and `gcp/genai` placement~~ ✅ done 2026-07-29 (AI Practitioner moved to `exams/aws/foundational/ai-practitioner-aif-c01/`; the Azure and GCP dirs are study tracks, kept in place and now counted as `track` rather than certification)
- [x] ~~Replace the 2 remaining `last-updated: YYYY-MM-DD` placeholders~~ ✅ 2026-07-29 - not applicable. Both live inside ```yaml fenced blocks in `CLAUDE.md` and `CONTRIBUTING.md` that document the frontmatter convention. The original scan did not skip code fences. No stale frontmatter exists.

### Priority 3 - leverage

- [x] ~~Build `docs/certs.json` from fact-sheets; generate the hub table and provider indexes from it~~ ✅ done 2026-07-29 (CI fails if either is stale). Freshness ledger still generates independently - fold it in if it drifts.
- [x] ~~Add practice questions for uncovered certs~~ ✅ done 2026-08-09/10 across PR #1 and follow-ups. Coverage is **151 of 151** cert directories, not the 47 this line claimed until 2026-09-17; `resources/practice-questions/README.md` has said so since August. The item is left here checked rather than deleted because it was the largest single piece of content work in the repo.
- [x] ~~Add Tier 1 certifications~~ ✅ done 2026-08-09. All 13 added: SC-100, SC-300, **SC-401** (SC-400 is retired and was replaced by SC-401 - the roadmap entry was out of date), PL-300, the five CNCF associates (OTCA/CGOA/CAPA/CCA/CNPA), ISC2 CC, Oracle OCI AI Foundations + OCI GenAI Professional, Google Generative AI Leader. 137 → 150 cert directories, each with README, fact-sheet, practice-plan, scenarios, strategy, domain notes, a practice question bank, and a generated flashcard deck.
- [x] ~~Stagger `last-updated` re-verification by provider batch~~ ✅ done 2026-07-29 - `check-cert-freshness.py` assigns each provider a review month and reports what is due. The rotation exists; the re-verification work itself is ongoing (12 certs due in month 7).

### Priority 4 - differentiation

- [x] ~~Per-cert `flashcards.csv` (Anki-importable)~~ ✅ done 2026-07-29 - 80 decks, 6,487 cards. 57 certs fall below the 15-card threshold and get no deck; raising that means writing more `- **Term** - definition` lines in their notes.
- [x] ~~Map labs to the certs they support~~ ✅ done 2026-07-29 - 15 labs mapped to 46 certs, generated both directions. 91 certs still have no lab.
- [x] ~~Add `status:` and `exam-version:` frontmatter plus a revision-warning script~~ ✅ done 2026-07-29 - `status` is derived in `certs.json` rather than hand-declared (no drift). `exam-version:`/`exam-retires:` are optional frontmatter, seeded on the 4 retired AWS certs; `check-cert-freshness.py` warns ahead of a known retirement.
- [x] ~~Wire `check-orphan-links.sh` into CI~~ ✅ done 2026-07-29 - runs advisory (never blocking, since orphan detection is heuristic). Orphans are currently 0.
- [x] ~~Prune `.claude/settings.json`~~ ✅ done 2026-07-29
- [x] ~~Publish the repo as a searchable site~~ ✅ done 2026-08-14 - MkDocs Material on GitHub Pages, generated from the markdown tree by `build-site.py`. See below.

---

## Completed 2026-08-14 - published as a searchable website

The repo's 3.0M words had no search: navigation was GitHub's file listing. Every
page is now also published at
[cloud.noblerworks.com](README.md).

The markdown tree is unchanged and stays the source of truth. `build-site.py`
adapts the tree to MkDocs at build time rather than restructuring the tree for
MkDocs, so there is no second copy of any page.

- [x] `.github/scripts/build-site.py` - staging, generated directory landing
      pages, fence-aware link rewriting, and all 2,032 nav entries generated from
      the tree plus `docs/certs.json`
- [x] `mkdocs.yml` (hand-maintained, no `nav`), `requirements-docs.txt` (fully
      pinned), `.github/site/extra.css`
- [x] `.github/workflows/docs-site.yml` - `--strict` build blocks every PR;
      deploys to Pages on push to main
- [x] Docs updated: README, CONTRIBUTING (local preview), `docs/ARCHITECTURE.md`
      (design + conventions), `.github/AUTOMATION.md`, CHANGELOG

### Defects the strict build surfaced and fixed

All three were broken on GitHub too, and none was catchable by the existing
link checker:

- [x] An unclosed code fence in `exams/gcp/cloud-architect/notes/compute-containers.md`
      swallowed ~130 lines including four headings. A stray duplicate fence in the
      same file compounded it. A repo-wide scan found no other instance.
- [x] 14 broken heading anchors: `resources/community-resources.md` (11 - its
      whole table of contents), `README.md`, `docs/improvement-roadmap.md`, and one
      AWS note. Most omitted the leading hyphen an emoji heading produces.
- [x] Links into `.templates/` had no working site target; it is staged as
      `provider-resources/` and the ~144 inbound links are rewritten.

### Follow-ups closed 2026-08-14 (same day)

- [x] ~~**Pages must be enabled once**: Settings > Pages > Source > **GitHub
      Actions**~~ ✅ enabled via `gh api -X POST .../pages -f build_type=workflow`;
      the previously failing deploy job was re-run and the site is live. Verified
      200 on the homepage, Study Hub, a deep cert page, a generated directory
      index, and the staged `provider-resources/`.
- [x] ~~Theme was Material's default indigo~~ ✅ switched to monochrome (Nobler
      Works house style). `mkdocs.yml` sets `primary: custom` / `accent: custom`
      on **all three** palette entries - the auto entry renders before the palette
      JS runs, so leaving it unset kept showing indigo - and the black/white
      values live in `.github/site/extra.css`. Links carry underlines instead of
      colour, and slate's blue-grey dark surfaces are overridden to neutral black.
      Dark mode is true `#000000` as of the same day: the banners are flattened
      PNGs on pure black, so a near-black page drew a rectangle around each one.
- [x] ~~The themed site still read like a styled README~~ ✅ same day, restyled
      to the gitGood design language, extracted from gitgood.dev's source: green
      accent (`#22c55e`) on links/CTAs/hover borders/glow shadows, Geist + Geist
      Mono, centred staggered hero with accent kickers, card hover = accent
      border + tinted shadow + 2px lift. Also fixed two dark-mode defects the
      monochrome pass shipped (black-on-black hero buttons, washed-out h1),
      hid the header's star/fork repo widget, and stripped leading heading
      emoji on the site only (`strip_heading_emoji()` in build-site.py pins
      each original anchor slug, so no inbound anchor link moved; the repo
      markdown and the sidebar's landmark labels are untouched). See
      CHANGELOG 2026-08-14.
- [x] ~~Both sidebars were rendered, and the populated one appeared to switch
      sides between pages~~ ✅ `navigation.tabs` off, so the left sidebar is the
      same full tree everywhere, and `toc.integrate` folds the page contents into
      it so there is no right column. `toc.integrate` alone drops the ToC on
      every section-index page - Material only emits it for leaf pages - so
      `.github/site-overrides/partials/nav-item.html` overrides that partial.
      **This couples the repo to Material's template internals**: after a version
      bump, re-copy the partial, re-apply the marked block, and check a cert
      landing page by eye. A `--strict` build will not catch a drifted template.
- [x] ~~No promotion of gitGood.dev, the flagship product~~ ✅ promo block in the
      README header and on the landing page, with `assets/brand/gitgood-banner.png`
      cropped from gitGood's loading splash (it ships no marketing banner, and the
      splash carries a progress bar and an "84%" label). Copy names 21
      role-targeted paths and the cert banks by exam code, for search; the long
      lists sit in a collapsed `<details>` so they cost no visible height.
- [x] ~~README counts drifted unnoticed~~ ✅ `check-readme-counts.py` added and
      wired into `structure-validate.yml` as a blocking check. It caught "37
      concept pages" (actually 46), "8 topic indexes" (actually 13), and the
      `2.6M words` figure copied out of the dated `improvement-roadmap.md`
      snapshot (the tree is at 3.0M). Run `--fix` when you add content.
      Then it caught a bug in itself: the first version walked the filesystem
      and counted the `.site-src/` staged copy a local site build leaves behind,
      reporting 6.1M words against a real 3.0M. It now counts via `git ls-files`,
      so no build artifact can inflate a total.
- [x] ~~The site's home page was the repo README~~ ✅ `.github/site/home.md` is
      now rendered over the staged `README.md` by `build-site.py`: hero with
      three entry points, counts strip, four pillars as cards, a two-column jump
      list, 27 provider chips, and the three most recent release notes. GitHub
      keeps its repo front page; the site gets a landing page. No number is typed
      into it - every figure is a token filled from `certs.json` and
      `check-readme-counts.py`, and the release notes are extracted from the
      README, so neither page can drift from the other.
- [x] ~~The README's per-provider table was stale in 8 of 22 rows and missing 5
      providers~~ ✅ Kubernetes/CNCF read 7 against 12, Azure 23 against 26,
      CompTIA 2 against 4, Oracle 5 against 7; ISACA, Offensive Security, Palo
      Alto Networks, ServiceNow and VMware had no row at all, five days after the
      Tier 1 batch added them. The table is now **generated** by
      `build-provider-indexes.py` between markers, like the `STUDY-HUB.md` one,
      so counts and the row set come from `certs.json`.
- [x] ~~The table's "Highlights" column was hand-written and unchecked~~ ✅ It is
      one curated string per provider in `PROVIDER_HIGHLIGHTS`, shared by both
      tables, and the generator refuses to run if a provider has no highlight or
      no `PROVIDER_EMOJI` icon - so a new provider fails CI instead of rendering
      a blank row. Four lines were describing half a provider and were feeding
      STUDY-HUB while they did: Kubernetes/CNCF listed 7 of 12, ISC2 omitted CC,
      Oracle omitted both OCI AI certs, AWS omitted GenAI Developer. All fixed,
      and both tables now say plainly that Highlights is a sample and the Certs
      column is the total.
- [x] ~~Two scripts could rewrite the README's provider rows~~ ✅ The stopgap
      provider-table check in `check-readme-counts.py` was removed once the table
      became generated. Its `--fix` would have corrected a count *inside* a
      generated block, leaving the generator reporting the file stale. One table,
      one owner.
- [x] ~~The "Repository Statistics" block was outside CLAIMS~~ ✅ It still read
      37 concept pages against 46, 8 topic indexes against 13, and 5 compliance
      guides against 8 - the same drift the checker was written to stop, in the
      one section that is nothing but counts. 17 numbers added to `CLAIMS`,
      including the three restated in the repository-structure block.

### Known follow-ups

- The search index is 28 MB uncompressed. It is lazy-loaded and served gzipped,
  but if first-search latency becomes a complaint, the options are splitting the
  index per section or excluding the deepest cert notes from it.
- `check-internal-links.py` and the site build now overlap but are not
  redundant: the former checks the source tree offline, the latter checks
  rendered URLs and heading anchors. Worth folding anchor validation into the
  standalone checker so the failure is reported without a full site build.
- No CI check for unbalanced code fences. The site build catches them only
  indirectly, as missing anchors on the affected page. A direct validator would
  name the file and line.
- `PROVIDER_HIGHLIGHTS` is the last hand-written thing in either provider table.
  Nothing can check that a sample is a *good* sample, only that it exists - so a
  provider that gains a cert can still keep a blurb that does not mention it. The
  blast radius is now one string feeding both tables rather than two that drift
  apart, and both tables state that Highlights is a sample. Worth a look whenever
  a provider's count changes.

---

## Completed 2026-08-09 - content gap expansion

A repo-wide gap analysis found four holes. All four are now closed. Counts below
are measured, not estimated.

### Tier 1 certifications (13 added)

- [x] Microsoft: SC-100, SC-300, SC-401, PL-300
- [x] CNCF: OTCA, CGOA, CAPA, CCA, CNPA
- [x] ISC2 CC - the free, no-prerequisite entry point the "zero to hero" framing
      implied but the repo did not have (the security path started at Security+)
- [x] Oracle: OCI AI Foundations, OCI Generative AI Professional - Oracle had five
      certs here and zero AI ones
- [x] Google: Generative AI Leader
- [x] OTCA also closes the "no observability certification anywhere in exams/" gap,
      and CCA is the only cert in the repo teaching eBPF

### Learn pillar

Was 54k words against 2.17M in `exams/`.

- [x] 8 new concept pages: caching, SQL vs NoSQL, load balancing, secrets
      management, autoscaling, deployment strategies, cloud cost basics, GPUs for AI
- [x] 3 new day-one pages: file permissions, JSON and YAML, reading error messages
- [x] `topics/platform-engineering.md` hub
- [x] Concepts index gained a Data and Databases section; 34 → 46 concept pages

### Practice questions

- [x] 13 new banks, one per new cert. Coverage 34/137 → 47/150

### Housekeeping

- [x] All generated indexes rebuilt: `docs/certs.json`, 27 provider indexes,
      STUDY-HUB table, flashcards (90 → 103 decks, 9,545 cards), lab map, freshness
- [x] Hand-maintained counts corrected in README, STUDY-HUB, CLAUDE.md, learn/README
- [x] `.cspell.json` extended with 100+ legitimate technical terms
- [x] Validators at zero: structure 0 failures / 0 warnings, 4,053 internal links
      0 broken, frontmatter 0 failures, orphans 0

### Known follow-ups

- Practice question banks for the 103 certs that still have none
- 47 certs remain below the 15-card flashcard threshold; raising them means writing
  more `- **Term** - definition` lines in their notes
- `markdownlint` MD060 (table-column-style) fires across the whole repo, including
  files untouched by this work. It is a newer rule than the pinned CI action, so it
  is version drift rather than a content defect. Decide whether to disable it in
  `.markdownlint.json` or reformat every table

---

