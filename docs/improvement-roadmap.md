---
last-updated: 2026-07-29
difficulty: n/a
reading-time: 20 min
---

# Improvement roadmap

A repo-wide gap analysis: what is broken, what is missing, and what would raise the
quality bar. Findings are measured against the repo as of 2026-07-28 (1,506 markdown
files, ~2.6M words, 137 cert directories across 27 providers: 133 certifications plus
4 Anthropic self-directed study tracks).

> **These are frozen 2026-07-28 figures, not current ones.** They are kept as the
> baseline the findings below were measured against. Do not quote them anywhere
> else - the `~2.6M words` figure was copied into the README, CHANGELOG and TODO
> on 2026-08-14 as a current fact, by which point the tree had grown to 3.0M. For
> current numbers run `python3 .github/scripts/check-readme-counts.py`.

Every number below was produced by scanning the tree, not estimated. Re-run the
commands in [How the numbers were produced](#how-the-numbers-were-produced) to refresh.

> **Status (2026-07-29).** Phases 1 and 3-4 tooling are complete; Phase 2 is partly done.
> Closed: all 383 broken internal links, the count drift, blocking link CI, the diagram
> standard, cert placement, the last structure warning, `docs/certs.json` and generated
> navigation, per-provider indexes, flashcard decks, the lab-to-cert map, and the
> freshness rotation. Section 1 is kept as the record of what was wrong and why.
>
> **Update (2026-07-29):** all 10 outline-stage certs now have drafted notes and are
> active. No cert remains at outline stage. The flashcard corpus grew to 90 decks and
> 8,484 cards as a result.
>
> **Update (2026-08-09).** Section 3's Tier 1 list is now closed: all 13 certifications
> have been added (137 → 150 cert directories), each with a full file set and a practice
> question bank. One correction to that list: **SC-400 is retired and was replaced by
> SC-401** (Information Security Administrator), so SC-401 was built instead.
>
> The same pass closed two gaps this document did not name. The repo had **no AI security
> material** despite the name: "OWASP LLM Top 10" appeared in one file and "model supply
> chain" in zero, and the compliance guides covered no AI regime. `resources/ai-security/`
> and three AI governance guides now exist. And the **learn pillar** was 54k words against
> 2.17M in `exams/`; it gained 11 pages and a topic hub.
>
> **Still open:** practice questions for the 103 certs that still lack them. Tracked in
> [TODO.md](https://github.com/PatrickWiloak/cloud-zero-to-hero/blob/main/TODO.md).

<!-- -->

> **Correction (2026-07-29).** The first draft of this document reported 127 cert
> directories. That number came from `validate-cert-structure.sh`, which discovered certs
> by looking for a `notes/` subdirectory and therefore skipped the 10 certs whose notes
> were never written. Counting by `fact-sheet.md` gives 137. Both scripts now discover
> certs the same way. The draft also claimed `docs/ARCHITECTURE.md:206` rendered as a
> broken image; it is inside a fenced code block and renders as a code sample.

**Contents**

- [1. Correctness gaps (fix first)](#1-correctness-gaps-fix-first)
- [2. Coverage gaps in existing content](#2-coverage-gaps-in-existing-content)
- [3. Certifications we could add](#3-certifications-we-could-add)
- [4. Structural and experience improvements](#4-structural-and-experience-improvements)
- [5. Suggested sequencing](#5-suggested-sequencing)
- [How the numbers were produced](#how-the-numbers-were-produced)

---

## 1. Correctness gaps (fix first)

These are defects, not missing features. They make the repo look less trustworthy than
the content actually is.

### 1.1 - 383 broken internal links (fixed 2026-07-29)

A scan of every relative markdown link found 383 targets that did not exist on disk.
They fell into four buckets:

| Count | Bucket | Root cause | Resolution |
|------:|--------|------------|------------|
| 191 | `docs/freshness.md` rows | Generator emitted repo-root-relative paths from a file that lives in `docs/`, so `exams/aws/...` resolved to `docs/exams/aws/...` | Fixed in `.github/scripts/build-freshness-ledger.sh`; emitted paths are now prefixed with `../` and the ledger was regenerated |
| 87 | Absolute paths like `/exams/aws/shared/services/compute/ec2.md` | Leading slash resolves to the GitHub domain root, not the repo root. Concentrated in `resources/certification-roadmap-*.md` | Rewritten as relative paths; every rewritten target was verified to exist |
| 77 | Links to `notes/NN-topic.md` files that were never written | Skeleton certs shipped a README and practice-plan promising notes | Delinked and marked `_(planned)_`, preserving the outline. Phase 2 restores real links as notes are drafted |
| 28 | Stale paths from an older directory layout | E.g. `../../cisco/ccna/README.md` (actual: `ccna-200-301`), `../../aws/specialty/security-specialty/` (actual: `security-scs-c02`), `../../axelos/itil-4-foundation/` (provider does not exist) | Repointed; the ITIL 4 reference was unlinked and marked as not yet in the repo |

The 19 remaining unresolved-looking targets are all inside fenced code blocks or inline
code spans: documentation examples in `CLAUDE.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`,
and `assets/diagrams/README.md`, plus regex and Python snippets inside cert notes. The
checker in [1.2](#12---ci-could-not-catch-any-of-this-fixed-2026-07-29) skips code, so these do not register.

### 1.2 - CI could not catch any of this (fixed 2026-07-29)

`link-check.yml` ran lychee with `fail: false`, so a broken-link report was uploaded as an
artifact and the job stayed green. Nothing enforced internal link integrity on a PR, which
is how 383 breaks accumulated unnoticed.

Now split into two jobs:

- **Internal links (blocking)** - `.github/scripts/check-internal-links.py`. Offline, no
  network flake, code-fence aware, exits non-zero on any break. Currently checks 2,799
  links.
- **External URLs (advisory)** - lychee, still `fail: false` with the weekly issue-filing,
  because vendor URL rot is not the contributor's fault.

### 1.3 - Navigation counts had drifted from reality (fixed 2026-07-29)

`STUDY-HUB.md` and `README.md` both advertised "122+ certifications across 22 providers".
Actual: **137 cert directories across 27 provider directories** - 133 certifications plus
the 4 Anthropic study tracks, spanning 26 certification providers.

The provider table in `STUDY-HUB.md` was missing five providers entirely and undercounted
three. All eight rows are now correct, the five missing providers were added, and the
badges and prose counts in both files were updated.

| Provider | Table said | Actually present | Note |
|----------|-----------:|-----------------:|------|
| AWS | 17 | 18 | The AI Practitioner dir was not counted |
| CompTIA | 2 | 4 | Network+ and CySA+ missing from the table |
| Cisco | 1 | 2 | CCNP Enterprise ENCOR missing from the table |
| Salesforce | 2 | 3 | Platform Developer II missing from the table |
| ISACA | absent | 2 | CISA, CISM |
| Offensive Security | absent | 1 | OSCP (PEN-200) |
| Palo Alto Networks | absent | 1 | PCNSA |
| ServiceNow | absent | 1 | CSA |
| VMware | absent | 1 | VCP-DCV |

The content existed and was decent; it was simply undiscoverable from the hub. The five
previously-absent providers are all outline-stage certs, now marked with a diamond in the
hub table so the status is visible rather than implied.

### 1.4 - The documented visual standard has zero instances (fixed 2026-07-29)

`CLAUDE.md` and `docs/ARCHITECTURE.md` previously specified PNG diagrams as canonical,
while `assets/diagrams/` held only a `README.md` and 89 files used Mermaid. The documented
standard had zero instances and the real one was undocumented.

Resolved by promoting Mermaid to the documented default and demoting PNG to the exception
for diagrams too dense to read inline. Updated `CLAUDE.md`, `docs/ARCHITECTURE.md`,
`CONTRIBUTING.md`, and `assets/diagrams/README.md`, and added the guidance Mermaid needs
that PNG does not: no hard-coded colours (light and dark themes), and a caption since
Mermaid has no alt text.

### 1.5 - Frontmatter clustering and the freshness rotation (addressed 2026-07-29)

- At the time of the audit, 326 pages shared the `2026-05-03` stamp, so at the 180-day
  cadence the whole repo would fall due on one day.
- The two apparent `last-updated: YYYY-MM-DD` placeholders were a false positive: both sit
  inside fenced `yaml` blocks documenting the convention. The audit scan did not skip code
  fences.
- `docs/freshness.md` is rebuilt and now covers all 137 certs (previously 127, sharing the
  validator's `notes/` blind spot).

`.github/scripts/check-cert-freshness.py` assigns each provider a review month, so the
work spreads across the year instead of all falling due at once. The re-verification labour
itself remains ongoing, one provider batch at a time, which is the intended steady state
rather than an open defect.

---

## 2. Coverage gaps in existing content

### 2.1 - Ten certs have zero notes (fixed 2026-07-29)

Ten cert directories had a README, fact-sheet, and practice-plan, but an empty `notes/`
directory, and their READMEs linked to notes that did not exist. All ten now have drafted
domain notes (and, where the README promised them, scenarios and strategy pages): CySA+,
Network+, CCNP ENCOR, CISA, CISM, OSCP, PCNSA, Salesforce PD2, ServiceNow CSA, and VMware
VCP-DCV. Every one flipped from `outline` to `active` in the index, and the structure
validator reports zero warnings.

The original table of missing notes is kept below for the record.

| Cert | Missing notes |
|------|--------------:|
| `cisco/ccnp-enterprise-encor-350-401` | 6 |
| `comptia/cysa-plus` | - |
| `comptia/network-plus` | - |
| `isaca/cisa` | - |
| `isaca/cism` | - |
| `offensive-security/oscp-pen-200` | - |
| `palo-alto-networks/pcnsa` | - |
| `salesforce/platform-developer-2` | - |
| `servicenow/csa` | - |
| `vmware/vcp-dcv-2v0-21-23` | - |

A cert with no notes is a stub advertised as a study guide. Either fill them or mark them
"skeleton" in the hub so expectations match reality.

### 2.2 - Practice questions cover 34 of 137 certs

`resources/practice-questions/` has 34 files (plus a template), covering 34 of 137 certs.
AWS and Azure are well served. Nothing exists for NVIDIA (10 certs), HashiCorp beyond Terraform Associate (1 of 7),
FinOps beyond Practitioner (1 of 4), MongoDB, Confluent, GitHub, Oracle, IBM, ISACA,
Anthropic, or any of the newer CNCF exams.

### 2.3 - Twenty-one of 27 provider directories have no index README (fixed 2026-07-29)

Only `cloud-security-alliance`, `isaca`, `isc2`, `offensive-security`,
`palo-alto-networks`, and `servicenow` have one. `STUDY-HUB.md` links to
`exams/aws/`, `exams/azure/`, and so on, and those land on a bare GitHub directory
listing with no ordering, no difficulty signal, and no suggested path.

A short generated index per provider (cert name, code, level, status, link) would fix
this and could be script-generated from the fact-sheets.

### 2.4 - Structural inconsistency in the GenAI directories (fixed 2026-07-29)

`exams/aws/genai`, `exams/azure/genai`, and `exams/gcp/genai` all sat at provider level
while every sibling cert sat under a level directory. Investigating showed they are not
the same kind of thing:

- `exams/aws/genai` was the AWS Certified AI Practitioner (AIF-C01), a real exam in the
  wrong place. Moved to `exams/aws/foundational/ai-practitioner-aif-c01/`, with all
  inbound links repointed.
- `exams/azure/genai` and `exams/gcp/genai` are explicitly self-directed study tracks
  rather than single exams, the same shape as the four Anthropic tracks. They are
  correctly at provider level, but were being counted as certifications.

The index now carries a distinct `track` status, so headline counts separate real exams
from study tracks instead of conflating them.

### 2.5 - One outstanding structure warning

`aws/professional/genai-developer-aip-c01` is classified senior tier but is missing
`practice-plan.md`, `scenarios.md`, and `strategy.md`. It is also one of the two files
flagged as orphaned by `check-orphan-links.sh` (nothing links to it).

---

## 3. Certifications we could add

Grouped by how well they fit the repo's cloud + data + AI + security remit. Exam codes
and availability churn constantly, so **verify every code against the vendor's site
before building a page** - especially the newer AI and CNCF exams.

### Tier 1 - fills a thematic hole the repo already claims to cover

| Provider | Certification | Why it matters here |
|----------|---------------|---------------------|
| Microsoft | **SC-100** Cybersecurity Architect Expert | The repo has SC-200 and SC-900 but stops short of the expert-level security architect exam, which is the capstone of the Microsoft security track |
| Microsoft | **SC-300** Identity and Access Administrator | The repo has an IAM topic page and an identity service comparison but no identity cert on any cloud |
| Microsoft | **SC-400** Information Protection and Compliance | Pairs with the five compliance guides already in `resources/compliance-guides/` |
| Microsoft | **PL-300** Power BI Data Analyst | The single biggest analytics cert by volume; the repo covers DP-600/DP-700 but not the analyst tier |
| GIAC / SANS | **GSEC, GCIH, GCLD, GCSA, GPEN** | An entire security certification ecosystem is absent. GCLD (Cloud Security Essentials) and GCSA (Cloud Automation) are directly on-theme |
| ISC2 | **CC** (Certified in Cybersecurity) | Free, entry-level, and the natural security on-ramp for the "zero to hero" promise. Currently the security path starts at Security+ |
| Oracle | **OCI Generative AI Professional**, **OCI AI Foundations** | Oracle has five OCI certs here and zero AI ones, in an AI-focused repo |
| Google | **Generative AI Leader**, **Associate Data Practitioner** | Two of the newest GCP exams; the repo has 12 GCP certs but neither |
| CNCF | **OTCA** (OpenTelemetry), **CGOA** (GitOps), **CAPA** (Argo), **CCA** (Cilium), **CNPA** (Platform Engineering) | Seven Kubernetes certs are covered but none of the newer CNCF associates, despite the repo having a platform-engineer roadmap and an observability topic page |
| Splunk / Elastic / Datadog | Core certifications | `resources/service-comparison-observability-monitoring.md` and `topics/observability.md` exist, but there is not a single observability certification anywhere in `exams/` |

### Tier 2 - strong fit, high demand

| Provider | Certification |
|----------|---------------|
| Red Hat | **RHCE (EX294)**, **EX188/EX288** containers, **EX380** OpenShift automation |
| CompTIA | **Linux+**, **PenTest+**, **SecurityX (CASP+)**, **Data+** |
| ISACA | **CRISC**, **CDPSE** |
| Cisco | **CyberOps Associate (200-201)**, **DevNet Associate (200-901)** |
| Palo Alto | **PCNSE**, **PCCSE** (Prisma Cloud), **PCDRA** (Cortex XDR) |
| Offensive Security | **OSEP**, **OSWE**, **OSWA** |
| Salesforce | **Platform App Builder**, **AI Associate**, **Agentforce Specialist** |
| Databricks | **Associate Developer for Apache Spark**, **Data Analyst Associate** |
| Snowflake | **SnowPro Associate: Platform**, **Advanced: Data Scientist** |
| HashiCorp | **Vault Operations Professional** |
| Microsoft | **AZ-140** (Azure Virtual Desktop), **AZ-800/801** (Windows Server Hybrid) |
| IBM | **watsonx Generative AI Engineer - Associate** |

### Tier 3 - broadens the repo into adjacent ecosystems

| Area | Candidates |
|------|-----------|
| Data tooling | **dbt Analytics Engineering**, **Astronomer Airflow**, **Confluent Flink**, **Neo4j**, **Redis** |
| Identity and PAM | **Okta** Certified Professional/Administrator, **CyberArk** Defender |
| Network security | **Fortinet NSE**, **Check Point CCSA/CCSE**, **Zscaler ZCCA/ZCCP** (fits the existing zero-trust architecture pattern), **F5 BIG-IP Administrator**, **Juniper JNCIA-Cloud** |
| Service management | **ITIL 4 Foundation** - already referenced by a dangling link in `exams/servicenow/csa/README.md` |
| Architecture | **TOGAF** Foundation/Practitioner |
| Virtualization and hybrid | **Nutanix NCP**, **Veeam VMCE**, additional **VMware VCP** tracks |
| Non-US clouds | **Alibaba Cloud ACA/ACP**, **Huawei HCIA/HCIP Cloud** |
| Linux | **LPIC-1/2**, **SUSE Certified Administrator** |

### A note on scope

At 137 cert directories the marginal value of the next one is lower than the marginal value of
finishing the ten outline-stage certs and adding practice questions to the 103 certs that
lack them. Recommend capping new-cert work at Tier 1 until [section 1](#1-correctness-gaps-fix-first)
and [2.1](#21---ten-certs-have-zero-notes-fixed-2026-07-29) are closed.

---

## 4. Structural and experience improvements

### 4.1 - A machine-readable cert index (done 2026-07-29)

`docs/certs.json` is generated from the fact-sheets by
`.github/scripts/build-certs-index.py`: provider, exam code, name, level, status
(active / outline / retired / anticipated), duration, questions, passing score, cost,
validity, delivery, notes count, which standard files exist, and last-updated.

`.github/scripts/build-provider-indexes.py` generates the STUDY-HUB provider table and
all 27 per-provider index READMEs from it, and CI fails if either is stale. That removes
the drift class documented in
[1.3](#13---navigation-counts-had-drifted-from-reality-fixed-2026-07-29): generated tables
cannot go stale the way hand-maintained ones did.

Parser fill rates against the 137 fact-sheets: exam code 71%, cost 79%, duration 78%,
validity 73%, passing score 72%, questions 62%, delivery 49%, format 26%, languages 16%.
Unparseable fields are `null`, never guessed. The remaining gaps are mostly certs with no
vendor exam code at all (GCP, Databricks, MongoDB, IBM), so the honest ceiling is below
100%. Raising the rest is a matter of normalising fact-sheet frontmatter over time.

### 4.2 - Spaced repetition assets (done 2026-07-29)

`.github/scripts/build-flashcards.py` writes an Anki-importable `flashcards.csv` into each
cert dir: 82 decks, 6,885 cards. Cards are extracted rather than invented. Exam logistics
come from `docs/certs.json`; term-definition cards come from the
`- **Term** - definition` lines the notes already use.

Nothing is generated from headings alone, because "What is Cluster Architecture?" with no
sourced answer is a card that teaches nothing. 55 certs fall below the 15-card threshold
and get no deck rather than a misleading one. Writing more term-definition lines in those
certs' notes is what raises their card count.

### 4.3 - Exam-version tracking

Cert codes rotate (SAA-C03 to C04, SY0-701 to 801). The repo handles retired certs well -
`aws/specialty/data-analytics-das-c01` has a clear retirement notice and points to its
replacement, and the anticipated tracks such as `quantum-practitioner-qpc-c01` are
explicitly labeled as not-yet-real. That discipline is a strength worth extending: add a
`status:` and `exam-version:` field to fact-sheet frontmatter so a script can flag certs
approaching a known revision date.

### 4.4 - Wire the unused automation

`check-orphan-links.sh` exists but is not referenced by any workflow. The glossary scripts
(`glossary-autolink.py`, `glossary-add-anchors.py`, `glossary-upgrade-existing-links.py`)
are likewise manual-only. Either wire them into CI or document in `.github/AUTOMATION.md`
that they are intentionally run by hand.

### 4.5 - Connect labs to certs (done 2026-07-29)

Each hands-on project now declares the certs it exercises in frontmatter, and
`.github/scripts/build-lab-map.py` generates both directions: a lab-to-cert table in the
projects index, and the reverse index at `resources/hands-on-projects/labs-by-cert.md`.

46 of 137 certs have a matching lab. The page says so explicitly rather than implying full
coverage. Adding labs for the uncovered 91 is open work.

### 4.6 - Repo hygiene

- `.claude/settings.json` carries absolute paths from a previous machine
  (`/home/plw/coding/cloud-certification-study-guides/...`) and a broad `Bash(*)` allow.
  Worth pruning to the permissions actually needed.
- `TODO.md` says "None tracked yet" while the CHANGELOG shows active development. The
  items in this document are the natural backlog.

---

## 5. Suggested sequencing

**Phase 1 - credibility (done 2026-07-29)**

1. ~~Fix the `build-freshness-ledger.sh` path bug and regenerate `docs/freshness.md`.~~ Done.
2. ~~Rewrite the 87 absolute `/exams/...` links as relative.~~ Done.
3. ~~Repoint or remove the 28 stale-layout links.~~ Done.
4. ~~Update the `STUDY-HUB.md` provider table and both badge counts.~~ Done: 133 certs / 26
   providers, five providers added, outline-stage certs marked.
5. ~~Make internal link checking a blocking CI job.~~ Done.
6. ~~Fix cert discovery in both scripts.~~ Done: they now key off `fact-sheet.md` rather
   than a `notes/` subdir, so outline-stage certs are validated instead of skipped.

**Phase 2 - substance**

7. Write notes for the ten outline-stage certs. Restore the real links and drop the
   `_(planned)_` markers as each set lands.
8. Resolve the diagram standard: either produce PNGs or promote mermaid and adjust
   `CLAUDE.md` plus `docs/ARCHITECTURE.md` to match reality.
9. Add per-provider index READMEs (21 missing).
10. Complete `aws/professional/genai-developer-aip-c01`, the one remaining structure warning.

**Phase 3 - leverage**

11. ~~Build `docs/certs.json` and generate the hub table and provider indexes from it.~~
    Done 2026-07-29. The freshness ledger still generates independently.
12. Add practice questions for the highest-traffic uncovered certs (103 lack them).
13. Add Tier 1 certifications, starting with SC-100/SC-300, the CNCF associates, and the
    Oracle and Google AI exams.

**Phase 4 - differentiation**

14. Flashcard exports.
15. Lab-to-cert mapping.
16. Exam-version tracking with automated revision warnings.

---

## How the numbers were produced

```bash
# Cert directories and providers. Count by fact-sheet.md, not by notes/ - a cert whose
# notes are not yet drafted is still a cert directory.
find exams -type f -name fact-sheet.md | wc -l          # 137 cert dirs
ls -d exams/*/ | wc -l                                   # 27 provider dirs

# Structure, frontmatter, and internal links
bash .github/scripts/validate-cert-structure.sh
bash .github/scripts/validate-frontmatter.sh
python3 .github/scripts/check-internal-links.py

# Certs with no notes drafted
for d in $(find exams -type f -name fact-sheet.md | sed 's|/fact-sheet.md$||'); do
  [ "$(find "$d/notes" -name '*.md' 2>/dev/null | wc -l)" -eq 0 ] && echo "$d"
done

# Frontmatter coverage
grep -rl '^last-updated:' --include='*.md' . | wc -l
find . -name '*.md' -not -path './.git/*' | wc -l

# Diagram usage
grep -rl '```mermaid' --include='*.md' . | wc -l
find assets -name '*.png' | wc -l
```

Broken internal links are counted by `check-internal-links.py`, which walks every `.md`
file, blanks fenced code blocks and inline code spans, extracts relative markdown link
targets (excluding `http:`, `https:`, `mailto:`, `tel:`, and pure anchors), and tests each
resolved path with `os.path.exists`.
