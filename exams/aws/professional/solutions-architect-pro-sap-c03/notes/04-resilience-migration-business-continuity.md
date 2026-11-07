---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 35 min
---

# Domain 4: Resilience, Migration, and Business Continuity (15%)

## Overview

C02's "Accelerate Workload Migration and Modernization" (20 percent) became part of this domain, which now sits at **15 percent** and also gathers disaster recovery and business continuity content that was spread across C02's other domains. Three tasks: **4.1** migration strategies by using AWS frameworks, **4.2** disaster recovery architectures, **4.3** business continuity and resiliency.

**[📖 Exam guide: Content Domain 4](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/solutions-architect-professional-03-domain4.html)** - Official tasks and skills

## Task 4.1: Migration strategies

AWS frames migration decisions as the "R" strategies. Know them by what changes:

| Strategy | Meaning | Example |
|---|---|---|
| **Rehost** | Move as-is ("lift and shift") | Replicate servers to EC2 with AWS Application Migration Service (now branded under AWS Transform as **AWS Transform MGN**) |
| **Replatform** | Small changes to use managed services | Move a self-managed database to RDS or Aurora; containers onto ECS |
| **Refactor** | Redesign for cloud-native | Decompose a monolith into microservices or serverless functions |
| Retire / Retain / Relocate | Turn off, keep on premises, move wholesale (for example VMware) | Based on assessment |

- **Discovery and assessment** (4.1.1): inventory servers, map application dependencies and group them into **migration waves** so tightly related systems move together.
- **Rehosting** (4.1.2): continuous block-level replication keeps the AWS copy current, so cutover is a short window after testing.
- **Database and data migration** (4.1.3): **AWS Database Migration Service (DMS)** migrates databases with full load and ongoing change data capture (CDC) to keep source and target in sync until cutover; use the Schema Conversion Tool or DMS Schema Conversion for heterogeneous migrations (for example Oracle to PostgreSQL). **DataSync** moves file data.
- **Replatform** (4.1.4): reduce operational overhead with managed services.
- **Refactor and incremental modernization** (4.1.5): the **strangler fig pattern** places a facade (such as API Gateway or a load balancer) in front of the legacy system and routes individual capabilities to new services one at a time, retiring the old system gradually.
- **Legacy modernization** (4.1.6): mainframes, applications and databases, with AWS Transform for assessment and code transformation.

**[📖 AWS Database Migration Service](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html)** - Full load and change data capture

## Task 4.2: Disaster recovery architectures

Disaster recovery is designed backward from two business numbers: **RTO** (recovery time objective: how long you can be down) and **RPO** (recovery point objective: how much data you can lose). Smaller numbers cost more. AWS describes four strategies:

| Strategy | RTO / RPO | What runs in the recovery Region | Cost |
|---|---|---|---|
| **Backup and restore** | Hours / hours | Nothing; backups are copied | Lowest |
| **Pilot light** | Tens of minutes / minutes | Core data tier replicated; compute off or minimal | Low |
| **Warm standby** | Minutes / seconds to minutes | Full-function but scaled-down copy | Medium |
| **Multi-site active/active** | Near zero / near zero | Full production capacity serving traffic | Highest |

The whitepaper text confirms the cost ordering and that active/active can reach near-zero recovery time; the other ranges are indicative values from its strategy figure, which could not be read as text (unverified). Treat them as ordering, not guarantees.

- **Continuous replication** (4.2.2): **AWS Elastic Disaster Recovery** continuously replicates servers to a low-cost staging area and launches recovery instances when needed.
- **Assessment and procedures** (4.2.3, 4.2.5): **AWS Resilience Hub** assesses an application against RTO/RPO targets and recommends improvements; Systems Manager runbooks codify recovery steps; test the plan regularly, because an untested plan is an assumption.
- **Multi-Region failover** (4.2.4): replicate data (Aurora Global Database, DynamoDB global tables, S3 replication), detect failure with Route 53 health checks, route with Route 53 failover policies or **Global Accelerator**, and use **Amazon Application Recovery Controller** for routing controls and readiness checks that make failover deliberate and safe.
- **Multi-cluster containers** (4.2.6, new): run more than one EKS or ECS cluster across Availability Zones or Regions for availability and DR, with workloads and configuration deployed by pipeline to each.

```bash
aws route53 list-health-checks
aws route53 get-health-check-status --health-check-id 11111111-2222-3333-4444-555555555555
```

**[📖 Disaster recovery of workloads on AWS](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html)** - The four strategies and their trade-offs

## Task 4.3: Business continuity and resiliency

- **Centralized backup governance** (4.3.1): **AWS Backup** with organization-level backup policies and cross-account, cross-Region copies, so a compromised workload account cannot delete its own recovery points.
- **Failover testing and recovery time** (4.3.2): **AWS Fault Injection Service (FIS)** runs controlled fault experiments; Route 53 health checks and recovery tooling measure how long recovery takes.
- **Resilient design** (4.3.3): redundancy across Availability Zones, fault tolerance (no single point of failure) and self-healing (health checks plus automated replacement).
- **Ransomware and accidental deletion** (4.3.4): immutability. **S3 Object Lock** (WORM retention), **EBS snapshot lock**, and **AWS Backup Vault Lock** prevent deletion or alteration for a retention period, even by privileged users, and combine with versioning and MFA delete.
- **Chaos engineering** (4.3.5): define a **steady-state hypothesis** (what normal looks like, measured), inject a controlled failure with an FIS **experiment template**, and compare behavior against the hypothesis, with stop conditions that halt the experiment if it causes real harm.

## What changed from C02 in this domain

- **Consolidated here:** rehosting, refactoring and legacy modernization (C02 4.2, 4.4); multi-Region DR and DR testing (C02 2.2, 3.1); backup governance, failover tests, ransomware protection and chaos engineering (C02 1.4, 3.1, 3.2).
- **New:** multi-cluster container strategies for HA/DR (4.2.6).
- **Removed from the blueprint text:** "migration-tool security" (C02 task 4.2). AWS notes it may still be implicit in other skills.
- **Services added to scope:** AWS Resilience Hub, AWS Fault Injection Service, AWS Transform, Amazon Data Lifecycle Manager, AWS Local Zones.

## Key terms

- **Rehost** - migrate a workload to AWS without changes to the application.
- **Replatform** - migrate with limited changes to take advantage of managed services.
- **Refactor** - redesign an application to be cloud-native.
- **Migration wave** - a group of related applications and servers migrated together.
- **AWS DMS** - Database Migration Service, which migrates databases with full load and ongoing change data capture.
- **Strangler fig pattern** - gradually replacing a legacy system by routing capabilities to new services behind a facade.
- **RTO** - recovery time objective, the maximum acceptable time to restore service.
- **RPO** - recovery point objective, the maximum acceptable amount of data loss measured in time.
- **Pilot light** - a DR strategy that keeps only the core data tier running in the recovery Region.
- **Warm standby** - a DR strategy that keeps a scaled-down but fully functional copy running.
- **Multi-site active/active** - a DR strategy that serves production traffic from multiple Regions at the same time.
- **AWS Elastic Disaster Recovery** - a service that continuously replicates servers and launches recovery instances during a disaster.
- **AWS Resilience Hub** - a service that assesses and tracks an application's resilience against RTO and RPO targets.
- **Amazon Application Recovery Controller** - a service that provides routing controls and readiness checks for safe failover.
- **AWS Backup Vault Lock** - a feature that makes backups immutable for a retention period.
- **S3 Object Lock** - a feature that stores objects in a write-once-read-many model for a retention period.
- **AWS Fault Injection Service** - a service for running controlled fault injection experiments.
- **Steady-state hypothesis** - a measurable statement of normal system behavior that a chaos experiment tests.
