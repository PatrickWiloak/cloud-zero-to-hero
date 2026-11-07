---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 4 min
---

# Datadog Fundamentals Study Strategy

## No weights, so cover the outline evenly

Datadog's guide lists domains and subdomains without percentages. The six domains vary in size: data collection has six subdomains and computer fundamentals seven, while networking has three. Cover every subdomain at least once, then spend extra time where Datadog behavior is least obvious: hostnames, key types, metric types and tags.

## Distinctions to own

- **API key versus application key**: ingest versus read and manage.
- **Agent integration versus crawler**: code on your host versus Datadog pulling from an API.
- **DogStatsD (UDP 8125) versus APM (TCP 8126)**.
- **Count versus gauge**, **rate versus count**, **histogram versus distribution**.
- **`status` versus `configcheck` versus `check`**: what runs, what loaded, why it fails.
- **`conf.yaml` versus `conf.yaml.example`**: only the first is read.
- **Environment variable versus file setting**: variables win.
- **Multi-alert versus simple alert** monitors.
- **Timeboard versus screenboard** layouts.
- **Explicit hostname versus derived hostname**.

## Read the guide's study list

The exam guide names fourteen documentation pages and three courses. The questions are drawn from the same ground, so read those pages once each in full rather than skimming many others.

## Reading the question

Scenario questions describe a symptom. Name the layer first: machine, Agent, network, configuration, data model or display. Then choose the command or setting at that layer. If an option mentions a tool from a different layer, it is usually a distractor.

## Practice honestly

A Datadog trial and a spare VM beat reading. Install the Agent, break a config file on purpose, and recover using only `status`, `configcheck` and the log. The three commands you use most in that exercise are the ones the exam favors.
