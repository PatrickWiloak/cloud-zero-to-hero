---
last-updated: 2026-11-25
difficulty: n/a
---

# Content gaps and improvement plan (2026-11-25)

**Scope:** the cert guides (`exams/`), learn pages, resources and the one waiting draft of cloud.noblerworks.com.
**Input:** a Gemini (Antigravity CLI) audit Patrick pasted on 2026-11-25, used as leads only.
**Method:** every figure re-measured from `git ls-files` (never a filesystem walk; `.site-src/` is a staged copy),
searched with `git grep`, and checked against `docs/certs.json`, `TODO.md` and `QUEUE.md`. Exam facts were read on
the vendor's own pages on 2026-11-25. A topic is called a gap only when the search shows the content is absent,
not merely in a different file. The older review is [content-gaps-2026-11-07.md](./content-gaps-2026-11-07.md).

**Freshness is not planned here.** The 180-day re-verification queue is driven by
`check-cert-freshness.py` (provider review months) and the nobler-os `exam-watch-z2h-cloud` loop, with
[freshness.md](./freshness.md) as the ledger. Overdue fact-sheets are listed below only as a checked claim.

## Gemini claims checked

19 claims: **12 confirmed, 5 overstated, 2 false.**

| Claim | Verdict | Measured figure |
|---|---|---|
| 35 fact-sheets last updated 2026-05-03 (over 180 days), incl. OCI, GitHub Admin, Salesforce PD1/PD2, LFCA/LFCS, ServiceNow CSA, Network+ | confirmed | 35 of 81 fact-sheets dated 2026-05-03 (206 days). `check-cert-freshness.py` reports the same 35 as overdue. Only 4 of the 5 OCI guides: Architect Associate was updated 2026-11-22. Driven by the freshness tooling, not this plan. |
| OCI guides use -24/-25 codes where Oracle now has -26 | overstated | No `-25` code anywhere (`git grep -E '1Z0-[0-9]+-25'`: 0 hits). The guides use `-24`; Architect Associate already names `1Z0-1072-26`. Already in TODO ("Reconcile README vs fact-sheet", 2026-12-06). |
| PL-900 needs a rewrite to the July 2026 outline | confirmed | Already in TODO (2026-12-19). Notes are the thinnest of any active guide (2,846 words). |
| AZ-204 successor (AI-200?) unconfirmed | overstated | Microsoft Learn has a live AI-200 study guide, "Developing AI Cloud Solutions on Azure" (Microsoft Certified: Azure AI Cloud Developer Associate). The page does not say it replaces AZ-204, so only the succession is unconfirmed. See wave 3. |
| Terraform Associate has 003-era sections to re-verify | confirmed | Already in TODO (2026-12-13). |
| IBM retired-product wording still open | confirmed | Already in TODO (2026-11-22 and 2026-12-06 lines). |
| Draft `drafts/learn/concepts/cloud-egress-and-data-transfer-costs.md` is unpublished | confirmed | Only `drafts/README.md` and this draft are tracked under `drafts/`. Verdict below. |
| Labs `gitops-with-argo-cd.md` and `build-a-landing-zone.md` not run live | confirmed | Both already in TODO (kind not installed; landing zone needs a throwaway AWS account). |
| 58 of 81 certs have no lab in `labs-by-cert.md` | overstated | The figure is right (23 mapped, `build-lab-map.py --check` clean), but 13 of the 58 are retired (10), study tracks (2) or not yet announced (1), and many of the 45 active ones are non-hands-on exams (four FinOps, three Salesforce, ServiceNow, AZ-900, CLF-C02, Cloud Digital Leader). See wave 5. |
| 15 active certs lack `scenarios.md` and 19 lack `strategy.md`, incl. "all 5 OCI" | overstated | File counts confirmed (15 and 19). But 4 of 5 OCI guides lack `strategy.md`, not 5 (`oci-foundations` has one), and most of these guides carry scenario and strategy sections in other files: AZ-104 has 14 scenario headings, GCP ACE 58, GCP Developer 19, CCNA 16. Only DVA-C03, CLF-C02 and Network+ have no scenario heading at all. See wave 2. |
| Thin notes (under 5,000 words): CNCF CAPA, CCA, CGOA, OTCA, CNPA, PCA, ICA, CBA; Azure PL-900, AZ-400, MS-900 | confirmed | All 11 are under 5,000 notes words (CAPA 3,508 to CBA 4,947; active median is 7,443). Whole guides are 6,900+ words. MS-900 is retired and AZ-400 retires 2027-02-01, so neither is worth deepening. Gemini missed FinOps Certified Analyst (4,549), EX280 (4,916) and Salesforce PD1 (4,943). |
| Missing cert: Splunk | overstated | `exams/splunk/core-user/` exists. The next Splunk exam (Power User) is QUEUE Q-004. |
| Missing cert: Elastic observability | confirmed | No `exams/elastic/`. Already QUEUE Q-005. |
| Missing cert: RHCE EX294 | confirmed | No guide; `git grep EX294` finds only passing mentions (RHCSA README and fact-sheet, `docs/improvement-roadmap.md`). Red Hat's page now titles it "Red Hat Certified Advanced System Administrator in Ansible Exam". See wave 3. |
| Missing cert: Terraform Professional | **false** | `exams/hashicorp/terraform-authoring-operations-pro/` is the Advanced exam, which HashiCorp previously named "Professional"; its README says so. The separate Infrastructure Engineer Professional exam has no guide, by choice (TODO 2026-11-21: wait for Search Console demand). |
| No FinOps interview guide | confirmed | `resources/interview-prep/` has 6 guides (cloud engineer, DevOps, Kubernetes, platform engineer, solutions architect, SRE), none for FinOps. See wave 4. |
| No multi-tool CLI cheat sheet (az/aws/gcloud/OpenTofu/Flux) | **false** | `resources/cli-cheat-sheet-comparison.md` is a 458-line aws / gcloud / az side-by-side. What is missing is narrower: no `tofu` or `flux` commands in any cheat sheet. Low value; not waved. |
| No BGP / multi-cloud networking lab | confirmed | None of the 9 projects under `resources/hands-on-projects/` is a networking lab; BGP is covered only in reading pages (`networking-deep-dives/hybrid-connectivity.md`, `multi-cloud-networking.md`). See wave 5. |
| Only 2 of 81 certs have `cram-1p.md` | confirmed | SAA-C03 and OCI Foundations. `cram-1p.md` is not part of the house cert shape in `CLAUDE.md`, so it is not waved. |

### Found here, missed by Gemini

- **AZ-400 retires 2027-02-01.** Microsoft's AZ-400 study guide (read 2026-11-25) says the cert, exam and renewal
  retire on February 1, 2027; the successor is **AZ-401**, Microsoft Certified: Agentic DevOps Engineer Expert
  (Tech Community post 2026-10-15: in beta, general availability planned for December). `git grep -i -E
  'AZ-401|2027-02-01'` finds nothing in the repo.
- **The AZ-400 README lists 10 domains; Microsoft lists 5.** `exams/azure/az-400/README.md` "Exam Domains" has ten
  headings (lines 18-156, e.g. "6. Implement Continuous Integration (10-15%)"). Skills measured as of 2026-07-27 are
  five: processes and communications (10-15%), source control (10-15%), build and release pipelines (50-55%),
  security and compliance plan (10-15%), instrumentation (5-10%).
- **DVA-C02 retires 2026-11-30** (5 days). Already flagged by `check-cert-freshness.py` and the exam-watch loop; the
  C03 guide is the one that needs study aids (wave 2).
- **`docs/freshness.md` is stale.** Last build 2026-10-22: it shows `oci-architect-associate` at 2026-05-03 while
  the fact-sheet says 2026-11-22, and has no row for `developer-dva-c03`.

## Plan, in order

Each item names the target, what is missing and the evidence. Items already in TODO or QUEUE are not repeated.

### Wave 1 - currency (fix before adding)

1. **AZ-400: mark retiring and fix the domain list.** Targets: `exams/azure/az-400/fact-sheet.md` (add
   `exam-retires: 2027-02-01`), `exams/azure/az-400/README.md` (a retirement notice linking the AZ-400 study guide
   and the AZ-401 announcement; replace the ten "Exam Domains" headings with Microsoft's five and their weights),
   then `build-certs-index.py` and `build-provider-indexes.py`. Evidence: `git grep -i -E 'AZ-401|2027-02-01'` 0 hits;
   README domain headings 1-10 above. Overlap: this replaces the TODO "restructure AZ-400" ask (in "Rewrites that
   wait on new outlines") with a minimal fix, since the exam has about ten weeks left. Do not deepen the notes.
   Source: learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-400.
2. **Regenerate `docs/freshness.md`.** `bash .github/scripts/build-freshness-ledger.sh > docs/freshness.md`.
   Evidence above (OCI Architect Associate row, missing DVA-C03 row). Small, mechanical.

### Wave 2 - study aids where a guide has none at all

3. **DVA-C03 `scenarios.md` and `strategy.md`.** Target: `exams/aws/associate/developer-dva-c03/`. Evidence: neither
   file is tracked, and `git grep -i -E '^#+ .*(scenario|strategy)'` in the guide finds only a "Strategies and
   rollback" note heading. From 2026-12-01 this is the only Developer Associate guide (DVA-C02 retires 2026-11-30).
   Follow the shape of `exams/aws/associate/solutions-architect-saa-c03/`.
4. **CLF-C02 and Network+ `scenarios.md`.** Targets: `exams/aws/foundational/cloud-practitioner-clf-c02/`,
   `exams/comptia/network-plus/`. Evidence: no `scenarios.md`, and 0 scenario headings anywhere in either guide.
   Both already have strategy sections (2 and 4 headings), so `strategy.md` is lower value.
5. **AZ-900 `scenarios.md` and `strategy.md`.** Target: `exams/azure/az-900/`. Evidence: neither file; 1 scenario
   heading and 1 strategy heading in the whole guide.

The other guides in the 15/19 counts (AZ-104, GCP ACE, GCP Developer, CDL, PL-900, CCNA, RHCSA, EX280, Salesforce)
already carry this content in fact-sheets and notes. A standalone file there would be a reshuffle, not a gap. The
5 OCI guides wait for the -26 reconciliation in TODO.

### Wave 3 - new guides on exams the vendor lists today

6. **AI-200 (Microsoft Certified: Azure AI Cloud Developer Associate).** Target: `exams/azure/ai-200/`. Evidence: no
   guide (`git grep -i 'AI-200'` finds only the TODO line), and `ai-zero-to-hero` covers only AI-102 and AI-900.
   The study guide lists four domains: containerized solutions (20-25%), AI solutions using Azure data management
   services (25-30%), connect to and consume Azure services (20-25%), secure, monitor and troubleshoot (20-25%).
   Write that Microsoft does not state it replaces AZ-204. Overlap: closes the "confirm on learn.microsoft.com"
   half of the TODO "Successors not built or verified" line.
7. **AZ-401 (Agentic DevOps Engineer Expert).** Target: `exams/azure/az-401/`. Evidence: no guide, no mention. The
   study guide is live: processes and communications (15-20%), source control (10-15%), build and release
   pipelines (35-40%), security and compliance plan (15-20%), instrumentation (15-20%). The cert also needs GH-300
   or AZ-104: link the AI site's GitHub Copilot guide (`ai-zero-to-hero` `certifications/github/copilot`) and the
   AZ-104 guide; do not build GH-300 here. Build after general availability (planned December 2026), or mark
   every logistics value "beta, not final".
8. **EX294 (Red Hat Certified Advanced System Administrator in Ansible).** Target: `exams/redhat/ex294/` in the shape
   of `exams/redhat/rhcsa-ex200/`. Evidence: no guide; Red Hat's EX294 page title uses the new name. Take
   objectives, version and logistics from that page only.

### Wave 4 - depth and one missing interview guide

9. **Deepen the thinnest CNCF notes, heaviest domain first.** Notes words against an active-guide median of 7,443:
   ICA 4,523 (traffic management 715, observability 660), CAPA 3,508 (Argo Workflows, 36% of the exam, has 1,024),
   PCA 4,422 (PromQL, 28%, has 1,032), CCA 3,822, CGOA 3,831, OTCA 4,080, CNPA 4,190, CBA 4,947. Targets: the
   named `exams/kubernetes/<cert>/notes/*.md` files. Each item should name the domain and the curriculum page it
   follows; in-depth prose, not bullet lists.
10. **FinOps interview guide.** Target: `resources/interview-prep/finops-interview.md`, linked from its README and
    `topics/finops.md`. Evidence: 6 interview guides, none FinOps, while the site has 4 FinOps cert guides,
    `topics/finops.md`, `resources/certification-roadmap-finops.md` and 5 cost-optimization pages to draw on. Run
    `check-readme-counts.py --fix`.

### Wave 5 - labs (need a live run, so not for the queue loop)

House rule: a project is run end to end before it ships. These need tools or accounts the loop does not have.

11. **A local BGP lab** (for example two FRR routers in containers peering over eBGP), backing CCNA, ENCOR,
    PCNE, AZ-700 and ANS-C01 (all without a lab). Target: `resources/hands-on-projects/`, mapped by `certs:`
    frontmatter. Needs Docker and a session that runs every command.
12. **kind-based labs for CCA (Cilium), ICA (Istio), KCA (Kyverno), PCA (Prometheus).** All four are hands-on
    topics with no lab. Blocked on the same `kind` install as the Argo CD run in TODO.

## The waiting draft: cloud egress and data transfer costs

`drafts/learn/concepts/cloud-egress-and-data-transfer-costs.md` (loop draft, 2026-11-13). No published page
covers this: `learn/concepts/cloud-cost-basics.md` gives egress one table row and two sentences. All ten relative
links resolve once the page moves to `learn/concepts/`. Every cited vendor page was fetched on 2026-11-25.

**Verdict: publish after these fixes.**

1. **AWS "charged in each direction" is cited to the wrong page.** The architecture blog (2021-06-30) says
   cross-AZ traffic incurs charges but not "each direction". The EC2 On-Demand pricing page does ("charged at
   $0.01/GB in each direction"). Add that page as a citation; keep the page free of prices.
2. **"Leaving a provider" is wrong for AWS.** It says "Do not assume any fee will be reduced." AWS waives data
   transfer out to the internet for customers moving all their data off AWS, on request to AWS Support (AWS News
   Blog, 2024-03-05, "Free data transfer out to internet when moving out of AWS"), and already gives 100 GB a
   month free to the internet. State the AWS waiver with that link, and tell readers to check Google Cloud's and
   Azure's own exit terms (not verified here).
3. **The Azure bullet sends readers to a page that does not answer.** The bandwidth page lists "Data transfer within
   same Availability Zone: Free" and has no row for traffic between availability zones. Say exactly that. Also fix
   the link description "rules by zone": on that page "Zone" is a billing geography, which it says is different
   from an availability zone.
4. **Google same-zone wording (minor).** The pricing page makes same-zone traffic free for internal IPv4 or any IPv6
   addresses within the same VPC network. Add "in the same VPC network".

Confirmed as written: AWS same-AZ transfer free, NAT gateway billed per hour and per GB processed, gateway
endpoints for S3 and DynamoDB at no additional charge, interface endpoints billed hourly per AZ and per GB;
Google inter-zone and inter-region charges, Premium versus Standard Tier routing; Azure inbound free.

To publish, follow `drafts/README.md` and add the page to `learn/concepts/README.md`. The TODO line of 2026-11-13
already covers this; it is Patrick's call.
