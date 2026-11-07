---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 5 min
---

# Certified Backstage Associate (CBA)

The CNCF and Linux Foundation certification for Backstage, the open source framework for building developer portals. CBA is about running and extending Backstage itself: build and run a project, deploy it, populate the software catalog, and customize plugins and the React app.

It is a hands-on-flavored knowledge exam for the people who own a portal. If you only use a portal, the [Backstage concept page](../../../learn/concepts/backstage-and-developer-portals.md) is the right length; CBA goes much deeper.

## Exam Details (checked 2026-11-07)

- **Exam Code:** Not stated by the Linux Foundation page (it uses CBA as the purchase SKU)
- **Duration:** 90 minutes
- **Questions:** Not stated on the Linux Foundation page
- **Passing Score:** Not stated on the Linux Foundation page
- **Cost:** USD 250 exam only; USD 495 with the THRIVE-ONE annual subscription (listed 2026-11-07)
- **Validity:** 2 years
- **Prerequisites:** None formally; the page lists the experience level as Beginner and calls a foundation in IT infrastructure, cloud, DevOps and security "essential for success"
- **Format:** Online, proctored, multiple choice

Full detail and sources in the [fact sheet](./fact-sheet.md).

## Domains

| Domain | Weight | Notes |
|--------|-------:|-------|
| Backstage Development Workflow | 24% | [01](./notes/01-development-workflow.md) |
| Backstage Infrastructure | 22% | [02](./notes/02-infrastructure.md) |
| Backstage Catalog | 22% | [03](./notes/03-catalog.md) |
| Customizing Backstage | 32% | [04](./notes/04-customizing-backstage.md) |

Customizing Backstage is the largest domain at 32%. Development workflow, infrastructure and catalog are close to equal at 22% to 24%.

## A version warning

The Backstage docs describe a **new frontend system** and a **legacy** one, and several pages are marked legacy. The notes show both. Check which one the exam targets before you book.

## Study sequence

1. Run an app and learn the layout and ports (3000 and 7007).
2. Configuration files, merge order, `$env`, deployment checklist.
3. Catalog: descriptor format, annotations, locations, providers, troubleshooting.
4. Plugins: frontend versus backend, `yarn new`, themes.
5. Re-read configuration and catalog troubleshooting; they carry the most detail questions.

Schedule in the [practice plan](./practice-plan.md).

## Study resources

- **[📖 Backstage documentation](https://backstage.io/docs/)** - the primary source
- **[📖 CBA curriculum](https://github.com/cncf/curriculum)** - the CNCF curriculum repo with `CBA_Curriculum.pdf`
- **[📖 Linux Foundation CBA page](https://training.linuxfoundation.org/certification/certified-backstage-associate-cba/)** - registration and logistics
- [Practice questions](../../../resources/practice-questions/cncf-cba.md) - 31 original questions in this repo

## Related

- [CNPA Platform Engineering Associate](../cnpa/) - the platform context a portal sits in
- [Backstage and developer portals](../../../learn/concepts/backstage-and-developer-portals.md) - the short concept page
- [Platform engineering topic](../../../topics/platform-engineering.md)
- [KCA Kyverno Associate](../kca/) - another policy and platform guardrail tool
