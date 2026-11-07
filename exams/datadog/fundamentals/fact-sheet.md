---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 5 min
---

# Datadog Fundamentals Fact Sheet

## Exam Overview

**Exam Code:** Not stated on the Datadog pages read
**Exam Name:** Datadog Fundamentals
**Level:** Foundational (Datadog calls it its "foundational certification offering")
**Duration:** Maximum seat time of 2 hours
**Format:** Multiple choice, one correct response; remote with a live proctor over webcam, or in person at a testing center
**Questions:** 75 scored plus 15 unscored pre-test questions (exam guide dated July 2022)
**Passing Score:** Not publicly disclosed by Datadog
**Cost:** USD 100 per exam (listed 2026-11-07)
**Valid For:** 3 years from the date of certification; renew by retaking the exam
**Prerequisites:** None formally; the guide targets entry-level Datadog users who understand observability principles
**Languages:** English, Japanese, Korean, Brazilian Portuguese, French, Spanish

### Verified facts and sources (checked 2026-11-07)

| Fact | Value | Source |
|------|-------|--------|
| Price, delivery, validity, retakes, passing score, languages | As above; retakes need separate payment, limited to three attempts in a 180-day period | [Datadog certification overview](https://www.datadoghq.com/certification/overview/) |
| Seat time, question types, question counts, content outline | 2 hours, multiple choice, 75 scored plus 15 pre-test, six domains | [Datadog Fundamentals Exam Guide (PDF)](https://www.datadoghq.com/pdf/Datadog_Fundamentals_Exam_Guide.pdf), created July 2022 |
| Domain weights | Not published; the outline lists domains and subdomains only | Exam guide |
| Registration | Datadog's Webassessor site | Certification overview |

> **Verify before booking.** The exam guide PDF is dated 2022 while the overview page is current; the guide's question counts and outline may have changed. Prices and policies change. Confirm on the official pages. Items marked "not stated" or "not disclosed" were not on the pages read, so this guide does not guess them.

## Exam Domains (from the exam guide, no weights published)

| # | Domain | Subdomains | Notes |
|---|--------|------------|-------|
| 1 | Computer Fundamentals | config file modification, operating systems, programming languages, hardware concepts, shell, metadata, networking | [01](./notes/01-computer-fundamentals.md) |
| 2 | Infrastructure Development | Agent installation, API key, application key, running the Agent, Agent hostname | [02](./notes/02-infrastructure-and-agent-install.md) |
| 3 | Networking & Agent Configuration | Datadog ports, Datadog IP addresses, Auto-discovery | [03](./notes/03-networking-and-agent-configuration.md) |
| 4 | Data Collection | DogStatsD, crawlers, Agent integrations, API endpoints, tagging best practices, metrics and timeseries | [04](./notes/04-data-collection.md) |
| 5 | Troubleshooting Datadog | Agent commands, Agent logs, Agent config files | [05](./notes/05-troubleshooting-datadog.md) |
| 6 | Data Visualization & Utilization | Host Map, dashboards, using metrics, using tags, monitors and alerts | [06](./notes/06-data-visualization-and-utilization.md) |

## Topics the guide says the exam validates

Computer fundamentals such as CPUs, RAM and storage; Linux basics; YAML, JSON, Python and shell scripts; networking basics including IP addresses and HTTP, TCP and UDP; installing and configuring the Agent in several environments; installing and configuring integrations; troubleshooting; aggregating and visualizing data; searching and filtering events, logs and metrics with tags and facets; creating monitors with targeted notifications; familiarity with the Datadog API.

Out of scope per the guide (non-exhaustive): programming, systems architecture, testing.

## Study materials named by the guide

Courses: Intro to Datadog: Dev + SRE, Introduction to Monitoring, Introduction to Integrations. Documentation: Getting Started, Datadog Agent, Metrics, Infrastructure List, API and Application Keys, Integrations, Docker Daemon, Query to the graph, Docker Agent, Metrics API, Monitor types, DogStatsD, ddtrace, Canonical Hostnames.

## Other Datadog exams (listed on the overview page, no guide here)

Log Management Fundamentals, APM and Distributed Tracing Fundamentals, Cloud SIEM for AWS Fundamentals, Database Monitoring Fundamentals.

## Related

- [Datadog provider page](../README.md)
