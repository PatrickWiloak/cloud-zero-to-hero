---
last-updated: 2026-11-07
difficulty: n/a
---

# Content gaps and improvement plan (2026-11-07)

A gap review of cloud.noblerworks.com, done by listing the tree with `git ls-files` and searching it with
`git grep`. A topic is called missing only when the search found nothing (or one passing mention).
`docs/improvement-roadmap.md` (2026-07-28) is the older, mostly closed review. The open items are tracked
in `TODO.md` under "Content gaps (2026-11-07 review)".

## Where the site stands

The cloud site is the most complete of the four: 32 concept pages, 15 day-one pages, 7 topic indexes,
10 projects, 7 service comparisons, 7 roadmaps, 9 CLI cheat sheets and 72 cert guides (the thinnest has
7,600 words). Its gaps are **currency** (retired products, exams waiting on new outlines) and a few
missing pages, not breadth.

## Plan, in order

### Wave 1 - currency (fix before adding)

These are already in TODO; they come first because an out-of-date page costs more trust than a missing one.

- Retired-product rewording (IBM Cloud Functions, Cloud Foundry, Watson services, OpsWorks), 2026-11-22.
- App Mesh is out of support: remove it from the mesh rows.
- README and fact-sheet reconciliation against vendor pages (IBM, OCI, PL-900), 2026-11-22.
- Exams waiting on outlines: SAP-C03, DVA-C03, AZ-204 successor, Terraform 004, OCI -26 codes.
- Vertex AI to Agent Platform rename sweep in the Cloud Architect notes and `resources/`.

### Wave 2 - pages with no coverage

- **Postmortems**: CrowdStrike 2024 (no hits) and the October 2025 AWS us-east-1 DNS event, both from the
  vendors' own writeups.
- **Day-one Python** (the last day-one gap on the TODO list).
- **Interview guides**: platform engineer and Kubernetes / cloud-native. The interview set covers
  4 roles, and the roadmaps cover 7.
- **Troubleshooting**: CI/CD pipeline failures, and Terraform state and drift problems.
- **Kubernetes cost optimisation** beside the three per-cloud cost pages.

### Wave 3 - concept pages for newer topics

Each is mentioned in passing but has no page: **eBPF** (3 mentions), **Backstage / developer portals**
(3), **OpenTofu vs Terraform** (2), **service quotas and limits** (4), **WebAssembly at the edge** (none).

### Wave 4 - certs and study aids (already in TODO)

- Linux+ needs a fresh Claude session (see the TODO note; CEH stays out of that session).
- Observability certs (Splunk, Elastic, Datadog); CNCF Backstage and Kyverno associates; CNPE, CKNE, KCA, CBA.
- Flashcard decks for the 21 guides without one, starting with the high-traffic ones: Terraform Associate,
  RHCSA, AZ-400, AZ-204, ANS-C01, GCP DevOps Engineer.
- Labs for the certs that `labs-by-cert.md` shows with no lab.

## How to do each item

Every new page uses the house style in `CLAUDE.md`. Projects must be run end to end before they ship. Run
`check-readme-counts.py --fix` in the same commit.
