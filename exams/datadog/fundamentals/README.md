---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 5 min
---

# Datadog Fundamentals

Datadog's foundational certification. It checks that you can get a machine reporting to Datadog, understand what the Agent sends and how, fix an Agent that is not working, and use metrics, tags, dashboards and monitors. The exam guide describes the candidate as an entry-level Datadog user who understands observability principles and is a frequent user of Datadog's core features.

It is broader than deep: from Linux command line basics to metric visualization strategies, in the guide's own words. The Agent and tags carry the most weight in practice because almost every other topic touches them.

## Exam Details (checked 2026-11-07)

- **Exam Code:** Not stated by Datadog
- **Duration:** maximum seat time of 2 hours
- **Questions:** 75 scored plus 15 unscored pre-test questions (per the exam guide, dated 2022)
- **Passing Score:** Not publicly disclosed
- **Cost:** USD 100 per exam (listed 2026-11-07)
- **Validity:** 3 years from the date of certification
- **Prerequisites:** None formally
- **Format:** Multiple choice; remote proctored or at a testing center

Full detail and sources in the [fact sheet](./fact-sheet.md).

## Domains

Datadog publishes the outline but no weights.

| Domain | Notes |
|--------|-------|
| Computer Fundamentals | [01](./notes/01-computer-fundamentals.md) |
| Infrastructure Development | [02](./notes/02-infrastructure-and-agent-install.md) |
| Networking & Agent Configuration | [03](./notes/03-networking-and-agent-configuration.md) |
| Data Collection | [04](./notes/04-data-collection.md) |
| Troubleshooting Datadog | [05](./notes/05-troubleshooting-datadog.md) |
| Data Visualization & Utilization | [06](./notes/06-data-visualization-and-utilization.md) |

## Study sequence

1. Brush up the computer basics you need to read configs and shells (note 01).
2. Install the Agent in your head: keys, sites, hostnames (note 02).
3. Ports, address ranges and Autodiscovery (note 03).
4. Data collection: the four routes in, metric types, tags (note 04).
5. Troubleshooting commands and logs (note 05).
6. Host Map, dashboards, monitors (note 06).

Schedule in the [practice plan](./practice-plan.md). Reasoning traps are in [scenarios](./scenarios.md) and [strategy](./strategy.md).

## Study resources

- **[📖 Datadog certification overview](https://www.datadoghq.com/certification/overview/)** - exams, price, validity and policies
- **[📖 Datadog Fundamentals exam guide (PDF)](https://www.datadoghq.com/pdf/Datadog_Fundamentals_Exam_Guide.pdf)** - the outline this guide follows
- **[📖 Datadog documentation](https://docs.datadoghq.com/)** - the primary source
- **[📖 Datadog Learning Center](https://learn.datadoghq.com/)** - courses named in the exam guide (some pages need an account)

Datadog offers a free trial; check its current terms for hands-on practice.

## Related

- [Datadog provider page](../README.md)
- [Splunk Core Certified User](../../splunk/core-user/) - ask questions of logs in a different vendor's tool
- [OpenTelemetry Certified Associate](../../kubernetes/otca/) - the open standard for telemetry
- [Prometheus Certified Associate](../../kubernetes/pca/) - metrics, labels and alerting in open source
