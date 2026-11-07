---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 30 min
---

# Domain 3: Cost-Optimized Architecture Design (15%)

## Overview

Cost is now its own domain at **15 percent**. In C02 cost was spread across "Design for New Solutions" and "Continuous Improvement for Existing Solutions" (including a cost control task). Four tasks: **3.1** architectures based on AWS pricing models, **3.2** data transfer and network costs, **3.3** cost allocation and visibility, **3.4** storage and database costs. The recurring exam skill is choosing the cheapest option that still meets the stated performance, availability and durability requirements.

**[📖 Exam guide: Content Domain 3](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/solutions-architect-professional-03-domain3.html)** - Official tasks and skills

## Task 3.1: Pricing models and cost-optimized architectures

**Purchase options** (3.1.1). Match the commitment to the predictability of the usage:

| Option | Fit | Trade-off |
|---|---|---|
| On-Demand | Spiky, new or short workloads | Highest unit price, no commitment |
| **Savings Plans** | Steady usage across instance families (Compute Savings Plans also cover Fargate and Lambda) | One- or three-year dollars-per-hour commitment; flexible |
| **Reserved Instances** (listed in the C03 in-scope services) | Steady usage of a specific instance configuration | Less flexible; Standard vs Convertible classes |
| **Spot Instances** | Fault-tolerant, interruptible work (batch, stateless workers, CI) | Up to large discounts but can be reclaimed with a short notice |
| Provisioned/reserved capacity for databases | Predictable database load | Commitment for lower price |

**Architecture choices that cut cost** (3.1.2). **Graviton** (AWS Arm-based processors) typically provides better price-performance when the software supports Arm. Pick the Step Functions workflow type by pattern: **Express** for high-volume short workflows is billed by requests and duration and is far cheaper per execution than **Standard**, which is billed per state transition and suits long, auditable workflows. Serverless (Lambda) removes idle cost for spiky workloads but can cost more than reserved instances for sustained high-throughput work.

**Rightsizing and scaling** (3.1.3). **AWS Compute Optimizer** recommends instance types, EBS volumes and Lambda memory from measured utilization. Scale to demand with scheduled scaling (known patterns), target tracking (hold a metric at a target) and **Fargate Spot** for interruptible containers.

**AI/ML cost** (3.1.4, new). Select the right service tier for the workload, **batch** requests that do not need real-time responses, and cache repeated prompts or responses. In Bedrock terms this means matching on-demand versus provisioned throughput and batch inference to the traffic shape; in SageMaker AI it means choosing among real-time, serverless, asynchronous and batch inference.

## Task 3.2: Data transfer and network costs

Data transfer is a classic hidden cost. The principles: data entering AWS from the internet is free; data leaving AWS to the internet, moving between Regions, and in many cases moving between Availability Zones is charged.

- **Content delivery** (3.2.1): CloudFront caches at the edge, reducing origin load and egress; **Origin Shield** adds a central caching layer to reduce origin requests; origin failover supports availability.
- **Private connectivity and Regional traffic** (3.2.2): **gateway VPC endpoints** for S3 and DynamoDB are free and avoid NAT gateway data processing charges; interface endpoints (PrivateLink) avoid internet egress for AWS services. A NAT gateway charges per GB processed, so heavy S3 traffic from private subnets through a NAT gateway is a typical waste. Keep chatty components in the same Availability Zone where availability allows (**AZ-aware architectures**).
- **Replication** (3.2.3): S3 Cross-Region Replication and DynamoDB global tables multiply storage and transfer cost; replicate only what recovery or latency requires.
- **Network architecture pricing** (3.2.4): Transit Gateway charges per attachment hour and per GB processed; PrivateLink charges per endpoint hour and per GB. At low volume and few VPCs, peering can be cheaper; at scale, Transit Gateway's operational benefits win.
- **AI/ML transfer** (3.2.5, new): **cross-Region inference routing** lets a Bedrock request be served from another Region for capacity; consider its transfer and compliance implications.

## Task 3.3: Cost allocation and visibility

- **Tagging strategy** (3.3.1): tag by business unit, project, environment and owner; activate **cost allocation tags** in Billing so they appear in cost data.
- **Reporting** (3.3.2): **Cost Explorer** for interactive analysis, **Cost and Usage Reports** for detailed line-item data (delivered to S3 and queried with Athena).
- **Enforce tagging** (3.3.3): tag policies in Organizations, SCPs that deny creating resources without required tags, and AWS Config rules that flag non-compliant resources.
- **Chargeback and showback** (3.3.4): showback reports cost to teams for awareness; chargeback bills them. **Cost Categories** group costs by rules into business-meaningful buckets; **split cost allocation data** attributes shared-cluster costs (for example EKS) to workloads; for generative AI, monitor Bedrock **token usage** per application or team.
- **Monitoring and alerting** (3.3.5): **AWS Budgets** alerts on actual or forecast thresholds; **Cost Anomaly Detection** uses machine learning to flag unusual spend.

## Task 3.4: Storage and database costs

- **Storage tiering** (3.4.1): S3 **Intelligent-Tiering** moves objects between access tiers automatically (good for unknown or changing access patterns); S3 Lifecycle policies transition and expire on a schedule; S3 Glacier storage classes for archives (retrieval time and minimum duration are the trade-offs); EFS lifecycle moves infrequently accessed files to cheaper classes.
- **Block storage** (3.4.2): **gp3** volumes decouple IOPS and throughput from size and are usually cheaper than gp2 for the same performance; use Provisioned IOPS (io1/io2) only when the workload needs sustained IOPS beyond what gp3 provides.
- **Databases** (3.4.3): DynamoDB **on-demand** capacity for unpredictable traffic versus **provisioned** with auto scaling (and reserved capacity) for predictable traffic; RDS reserved DB instances; Aurora Serverless for variable load; **Aurora I/O-Optimized** for I/O-heavy workloads where I/O charges dominate; Database Savings Plans.
- **Backup and DR retention** (3.4.4): AWS Backup plans with retention matched to requirements, and Amazon Data Lifecycle Manager for snapshot schedules and expiry. Keeping backups forever is a cost; keeping too few is a risk.
- **Observability cost** (3.4.5, new): control log volume with filtering, aggregate metrics, set retention periods and archive older logs to cheaper storage.

```bash
aws s3api put-bucket-lifecycle-configuration --bucket example-logs --lifecycle-configuration '{
  "Rules": [{
    "ID": "tier-then-expire",
    "Status": "Enabled",
    "Filter": {"Prefix": "logs/"},
    "Transitions": [{"Days": 30, "StorageClass": "GLACIER"}],
    "Expiration": {"Days": 365}
  }]
}'
```

**[📖 AWS Cost Management documentation](https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html)** - Cost Explorer, Budgets, Cost Categories and anomaly detection
**[📖 Amazon S3 Intelligent-Tiering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering.html)** - Access tiers and when to use them

## What changed from C02 in this domain

- **Structure:** C02 had no standalone cost domain; cost lived in "Design for New Solutions" (2.5, 2.6) and "Continuous Improvement" (3.5 cost control). C03 gathers it into four tasks.
- **New:** AI/ML cost optimization (3.1.4), AI/ML data transfer (3.2.5) and cost-aware observability (3.4.5); Bedrock token-usage monitoring for chargeback.
- **Services added to scope:** Reserved Instances (named), AWS Cost Categories, AWS Data Transfer Terminal, Amazon Data Lifecycle Manager.

## Key terms

- **Savings Plan** - a pricing model that gives lower rates in exchange for a committed dollars-per-hour spend for one or three years.
- **Spot Instance** - spare EC2 capacity offered at a discount that AWS can reclaim with short notice.
- **AWS Graviton** - AWS-designed Arm-based processors that often provide better price-performance.
- **Compute Optimizer** - a service that recommends resource configurations based on measured utilization.
- **Gateway VPC endpoint** - a no-charge endpoint type for S3 and DynamoDB that keeps traffic on the AWS network.
- **NAT gateway data processing charge** - a per-GB fee for traffic that passes through a NAT gateway.
- **CloudFront Origin Shield** - an additional caching layer that reduces the number of requests reaching the origin.
- **Cost allocation tag** - a tag activated in Billing so its values appear in cost reports.
- **Showback** - reporting costs to teams for visibility without billing them.
- **Chargeback** - billing teams or business units for the costs they incur.
- **Cost Categories** - rules that group AWS costs into custom business-meaningful categories.
- **AWS Budgets** - a service that alerts when actual or forecast spend crosses thresholds.
- **Cost Anomaly Detection** - a service that uses machine learning to identify unusual spending.
- **S3 Intelligent-Tiering** - an S3 storage class that moves objects between access tiers automatically based on usage.
- **gp3** - an EBS general purpose SSD volume type that lets IOPS and throughput be set independently of size.
- **Aurora I/O-Optimized** - an Aurora configuration with no separate I/O charges, suited to I/O-intensive workloads.
