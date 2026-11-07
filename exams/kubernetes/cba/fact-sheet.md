---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 6 min
---

# Certified Backstage Associate (CBA) Fact Sheet

## Exam Overview

**Exam Code:** Not stated by the Linux Foundation page (it uses CBA as the purchase SKU)
**Exam Name:** Certified Backstage Associate
**Level:** Associate
**Duration:** 90 minutes
**Format:** Online, proctored, multiple choice
**Questions:** Not stated on the Linux Foundation page
**Passing Score:** Not stated on the Linux Foundation page
**Cost:** USD 250 exam only; USD 495 with the THRIVE-ONE annual subscription (listed 2026-11-07)
**Valid For:** 2 years
**Prerequisites:** None formally; the page lists the experience level as Beginner and calls a foundation in IT infrastructure, cloud, DevOps and security "essential for success"

### Verified facts and sources (checked 2026-11-07)

| Fact | Value | Source |
|------|-------|--------|
| Name, duration, format | Certified Backstage Associate, 90 minutes, online proctored multiple choice | [LF CBA page](https://training.linuxfoundation.org/certification/certified-backstage-associate-cba/) |
| Validity | 2 years | LF CBA page |
| Price | USD 250 exam only; USD 495 bundled | LF CBA page |
| Attempts | The page says "Two exam attempts" in one section and "One Retake" in another | LF CBA page |
| Question count, passing score, exam code | Not stated (CBA is the purchase SKU) | LF CBA page |
| Domains and weights | 24 / 22 / 22 / 32 | [CNCF curriculum](https://github.com/cncf/curriculum) (`CBA_Curriculum.pdf`) and the LF page agree |

> **Verify before booking.** Prices and policies change. Confirm on the official page. Items marked "not stated" were not on the pages read, so this guide does not guess them.

## Exam Domains

### Backstage Development Workflow (24%)

- Build and run Backstage projects locally
- Understand local development workflows
- Compile a Backstage project with TypeScript
- Download and install dependencies with NPM/Yarn
- Use Docker to build a container image of a Backstage project

[Notes 01](./notes/01-development-workflow.md)

### Backstage Infrastructure (22%)

- Understand the Backstage framework
- Configure Backstage
- Deploy Backstage to production
- Understand Backstage client-server architecture

[Notes 02](./notes/02-infrastructure.md)

### Backstage Catalog (22%)

- Understand how and why to use the Backstage Catalog
- Populate the Backstage Catalog
- Using annotations
- Working with manually registered entity locations
- Troubleshooting entity ingestion
- Working with automated ingestion

[Notes 03](./notes/03-catalog.md)

### Customizing Backstage (32%)

- Understand frontend versus backend plugins
- Customizing Backstage plugins
- Make changes to React code in Backstage App
- Using Material UI components

[Notes 04](./notes/04-customizing-backstage.md)

## Quick reference

| Question | Answer |
|---|---|
| Frontend dev server port | 3000 |
| Backend port | 7007 |
| Preferred production database | PostgreSQL (SQLite for tests) |
| Only required config file | `app-config.yaml` |
| Which config wins? | Local files, loaded last |
| Default config visibility | Backend-only |
| Default ingested kinds | Component, API, Location |
| Orphan annotation | `backstage.io/orphan: 'true'` |
| Frontend plugin install | `yarn --cwd packages/app add ...` |
| Backend plugin install | `yarn --cwd packages/backend add ...` |
| Plugin scaffolder | `yarn new` |
| Container build | Host build: `yarn install --immutable`, `yarn tsc`, `yarn build:backend`, then `docker image build` |

## Related repo material

- [Notes](./notes/)
- [Practice plan](./practice-plan.md)
- [Scenarios](./scenarios.md)
- [Strategy](./strategy.md)
- [Practice questions](../../../resources/practice-questions/cncf-cba.md)
