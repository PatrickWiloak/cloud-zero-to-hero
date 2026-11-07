---
last-updated: 2026-05-03
---

# Playlist - SRE, 1 hour

Seven reads in order, ~60 minutes. By the end you have working mental models for what SRE actually does day-to-day: define SLOs, detect incidents, contain blast radius, design for resilience, automate toil away.

## The reads, in order

1. **[Observability basics](../learn/concepts/observability-basics.md)** (~7 min)
   Logs, metrics, traces - the three pillars and what each is for. The foundation of SRE.

2. **[Idempotency explained](../learn/concepts/idempotency-explained.md)** (~6 min)
   Retry-safe operations. The single design property that makes incident response (and resilient systems) possible.

3. **[Eventual consistency](https://data.noblerworks.com/learn/concepts/eventual-consistency/)** (~7 min)
   Why distributed systems sometimes show stale data, and why "make it strongly consistent" is rarely the right answer in production.

4. **[Architecture pattern: disaster recovery](./architecture-patterns/disaster-recovery-patterns.md)** (~12 min)
   The four DR archetypes (backup/restore, pilot light, warm standby, multi-site active-active) with RTO/RPO mapping.

5. **[Architecture pattern: chaos engineering](./architecture-patterns/chaos-engineering-patterns.md)** (~10 min)
   The discipline of injecting failures to verify resilience holds. Hypothesis → measure steady state → inject → observe → fix.

6. **[Architecture pattern: multi-region active-active](./architecture-patterns/multi-region-active-active.md)** (~8 min)
   The "always-on" shape. When to use it, when it's overkill.

7. **[Architecture pattern: cell-based architecture](./architecture-patterns/cell-based-architecture.md)** (~8 min)
   Blast-radius reduction. The architectural answer to "why did one bad deploy take everything down?"

## What you can do after this playlist

- Define an SLO and explain what its error budget governs.
- Pick a DR pattern given an RTO/RPO target and cost constraint.
- Articulate why idempotent operations are the prerequisite for safe retries.
- Identify single-point-of-failure shapes in an architecture diagram.
- Discuss when chaos engineering is worth the operational risk and when it isn't.

## Postmortem case studies for context

Read these alongside the playlist:

- [AWS S3 us-east-1 outage 2017](./postmortem-aws-s3-2017.md) - blast radius and tooling guardrails
- [Cloudflare regex outage 2019](./postmortem-cloudflare-regex-2019.md) - canary deploys and CPU SLOs
- [GCP networking outage 2019](./postmortem-gcp-networking-2019.md) - configuration changes are production changes
- [CrowdStrike content update 2024](./postmortem-crowdstrike-2024.md) - configuration is code; staged rollout
- [AWS DynamoDB DNS event 2025](./postmortem-aws-dynamodb-dns-2025.md) - race conditions and recovery overload

## Next steps

**If you want to build:**
- [Set up a monitoring stack](./hands-on-projects/setup-monitoring-stack.md) - Prometheus + Grafana + Alertmanager
- [Run a DR drill](./hands-on-projects/disaster-recovery-drill.md) - tested failover, measured RTO/RPO

**If you want to go deeper:**
- [SRE and reliability topic index](../topics/sre-and-reliability.md) - everything in one place
- [Service comparison: observability + monitoring](./service-comparison-observability-monitoring.md)
- [Troubleshooting guides](./troubleshooting/) - per-cloud and Kubernetes

**If you want a cert:**
- [GCP Cloud DevOps Engineer (PDOE)](../exams/gcp/cloud-devops-engineer/) - the most SRE-flavored cloud cert
- [AWS DevOps Engineer Pro (DOP-C02)](../exams/aws/professional/devops-engineer-pro-dop-c02/)
- [Azure DevOps Engineer Expert (AZ-400)](../exams/azure/az-400/)
- [Kubernetes CKA](../exams/kubernetes/cka/) - if you operate on K8s
- [DevOps / SRE roadmap](./certification-roadmap-devops-sre.md)

## Required reading outside this repo

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/) - the foundational text
- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) - the practical companion

## Related playlists

- [AI engineer in 30 min](https://ai.noblerworks.com/learn/start-here/ai-engineer-path/)
- [Cloud security in 1 hour](https://security.noblerworks.com/resources/playlist-cloud-security-1hour/)
- [Data engineer in 1 hour](https://data.noblerworks.com/resources/playlist-data-engineer-1hour/)
