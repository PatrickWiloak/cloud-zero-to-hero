---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 5 min
---

# Splunk Core Certified User

The entry-level Splunk certification. It checks that you can use Splunk Enterprise or Splunk Cloud Platform as a person who asks questions of data: search it, use fields, build simple statistics, save reports, make a dashboard, enrich events with a lookup and set up a basic alert. You do not install or administer anything.

If you have never seen Splunk, this is the right first step. If you already write `stats` and `timechart` searches daily, you can skim the notes and spend your time on the blueprint's wording.

## Exam Details (checked 2026-11-07)

- **Exam Code:** Not stated by Splunk
- **Duration:** 60 minutes total seat time (includes 3 minutes for the exam agreement)
- **Questions:** 60 multiple choice
- **Passing Score:** Not stated on the pages read
- **Cost:** USD 130 per attempt (listed 2026-11-07)
- **Validity:** Not stated on the pages read
- **Prerequisites:** None
- **Format:** Multiple choice, delivered by Pearson VUE

Full detail and sources in the [fact sheet](./fact-sheet.md).

## Domains

| Domain | Weight | Notes |
|--------|-------:|-------|
| Splunk Basics | 5% | [01](./notes/01-basics-and-basic-searching.md) |
| Basic Searching | 22% | [01](./notes/01-basics-and-basic-searching.md) |
| Using Fields in Searches | 20% | [02](./notes/02-fields-and-search-language.md) |
| Search Language Fundamentals | 15% | [02](./notes/02-fields-and-search-language.md) |
| Using Basic Transforming Commands | 15% | [03](./notes/03-transforming-commands.md) |
| Creating Reports and Dashboards | 12% | [04](./notes/04-reports-and-dashboards.md) |
| Creating and Using Lookups | 6% | [05](./notes/05-lookups.md) |
| Creating Scheduled Reports and Alerts | 5% | [06](./notes/06-scheduled-reports-and-alerts.md) |

Searching, fields and the search language together are 57% of the exam. If your time is short, make those three domains automatic first.

## Study sequence

1. Learn the pipeline of forwarder, indexer and search head, then the search page layout (note 01).
2. Learn field rules, the pipe, and the five named commands (note 02).
3. Learn `top`, `rare` and `stats` until you can pick the right one from a description (note 03).
4. Reports, dashboards, lookups, alerts: the order of the steps matters (notes 04 to 06).

Schedule in the [practice plan](./practice-plan.md). Common mistakes are in [scenarios](./scenarios.md) and [strategy](./strategy.md).

## Study resources

- **[📖 Splunk Core Certified User page](https://www.splunk.com/en_us/training/certification-track/splunk-core-certified-user.html)** - registration and logistics
- **[📖 Test blueprint (PDF)](https://www.splunk.com/en_us/pdfs/training/splunk-test-blueprint-user.pdf)** - the domains and weights this guide follows
- **[📖 Splunk Search Tutorial](https://docs.splunk.com/Documentation/Splunk/latest/SearchTutorial/WelcometotheSearchTutorial)** - hands-on walk-through with sample data
- **[📖 Splunk Search Reference](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/WhatsInThisManual)** - every command

A free way to practice is a Splunk Enterprise trial installed locally or a Splunk Cloud trial; check Splunk's current download page for terms.

## Related

- [Splunk provider page](../README.md)
- [Datadog Fundamentals](../../datadog/fundamentals/) - the same job (ask questions of telemetry) in a different vendor's tool
- [OpenTelemetry Certified Associate](../../kubernetes/otca/) - the open standard that produces much of this data
- [Prometheus Certified Associate](../../kubernetes/pca/) - metrics and alerting in the open source world
