---
last-updated: 2026-10-22
---

# AWS Certified CloudOps Engineer - Associate (SOA-C03) Fact Sheet

## 📋 Exam Overview

**Exam Code:** SOA-C03
**Exam Name:** AWS Certified CloudOps Engineer - Associate (formerly SysOps Administrator - Associate)
**Duration:** 130 minutes
**Questions:** 65 questions (50 scored + 15 unscored)
**Question Format:** Multiple choice and multiple response (no exam labs)
**Passing Score:** 720/1000 (scaled score, compensatory scoring)
**Cost:** $150 USD
**Valid For:** 3 years
**Prerequisites:** None required; AWS recommends 1 year of AWS deployment, management, troubleshooting, networking and security experience plus 1 year in an operations role
**Language:** English, Japanese, Korean, Simplified Chinese
**Delivery:** Pearson VUE (online proctored or testing center)
**Exam guide version:** v1.1 (published 2026-06-01; v1.0 published 2025-09-30)

**📖 [Official Exam Page](https://aws.amazon.com/certification/certified-cloudops-engineer-associate/)** - Registration and details
**📖 [SOA-C03 Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/sysops-administrator-associate-03/sysops-administrator-associate-03.html)** - Official domains, tasks and in-scope services
**📖 [Comparison of SOA-C02 and SOA-C03](https://docs.aws.amazon.com/aws-certification/latest/sysops-administrator-associate-03/sysops-administrator-associate-03-comparison.html)** - What changed from the SysOps exam

The 15 unscored questions are not identified and do not affect your score. Scoring is compensatory: you pass on the overall scaled score, not on each domain separately.

## 🎯 Target Audience

The exam is for CloudOps engineers who deploy, manage and operate workloads on AWS. The exam guide expects the candidate to support workloads according to the AWS Well-Architected Framework, operate through the console and the CLI, implement security controls for compliance, monitor and troubleshoot systems, apply networking concepts (DNS, TCP, IP, firewalls), implement availability and performance requirements, perform business continuity and DR procedures, and identify, classify and remediate incidents.

**Out of scope** (per the guide): designing distributed architectures, designing CI/CD pipelines, designing hybrid and multi-VPC networks, developing software, defining security, compliance or governance requirements, developing ransomware defense strategies, assessing and planning capacity, analyzing costs and TCO, and managing billing and invoicing.

## 🆕 What changed from SOA-C02

- **New name**: SysOps Administrator became **CloudOps Engineer**.
- **No exam labs**: SOA-C03 is multiple choice and multiple response only.
- **Five domains**: performance optimization moved into Domain 1 (Task 1.3) and network cost into Domain 5 (Task 5.1.4). There is no separate cost and performance domain, and cost analysis, TCO and billing are out of scope.
- **Broader services**: containers (ECS, EKS), AI workloads, Amazon Managed Service for Prometheus, EC2 Image Builder, AWS RAM, Terraform and Git, CloudWatch network monitoring.
- **Guide v1.1 additions** (2026-06-01): Amazon Bedrock, AWS DevOps Agent, AWS Health Dashboard, Kiro and AWS Security Agent are in scope, and Amazon S3 Files appears in Task 1.3.4.

## 📚 Exam Domains

| Domain | Weight | Notes |
|---|---|---|
| 1. Monitoring, Logging, Analysis, Remediation, and Performance Optimization | 22% | [01](./notes/01-monitoring-logging.md), [01b](./notes/01b-performance-optimization.md) |
| 2. Reliability and Business Continuity | 22% | [02](./notes/02-reliability-business-continuity.md) |
| 3. Deployment, Provisioning, and Automation | 22% | [03](./notes/03-deployment-automation.md) |
| 4. Security and Compliance | 16% | [04](./notes/04-security-compliance.md) |
| 5. Networking and Content Delivery | 18% | [05](./notes/05-networking.md) |

### Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization (22%)

Tasks: 1.1 metrics, alarms and filters; 1.2 identify and remediate issues; 1.3 performance optimization for compute, storage and databases.

- **EC2 memory and disk space are not standard metrics** - install the CloudWatch agent (configuration in Parameter Store, `CloudWatchAgentServerPolicy` on the role).
- **Metric filters** turn log lines into metrics and do not backfill; **Logs Insights** queries logs after the fact.
- **CloudTrail data events are off by default**; organization trails with log file integrity validation are the audit baseline.
- **Alarm actions**: SNS, Auto Scaling, EC2 stop/terminate/reboot/recover, Lambda, Systems Manager OpsItems and incidents. Everything else (an Automation runbook) goes alarm, then EventBridge.
- **Composite alarms** cut noise; **M of N datapoints** stops flapping; missing-data treatment matters for sparse metrics.
- **Cross-account dashboards**: CloudWatch cross-account observability with a monitoring account.
- **EventBridge troubleshooting**: pattern mismatch, wrong Region (IAM events are in us-east-1), target permissions, `FailedInvocations`.
- **AWS Health** events reach EventBridge as `aws.health`; **DevOps Agent** investigates incidents; **Kiro** writes code fixes.
- **Bedrock** metrics live in `AWS/Bedrock` (`Invocations`, `InvocationLatency`, `InvocationThrottles`, token counts); invocation logging is opt-in.
- **gp3** gives 3,000 IOPS and 125 MiB/s baseline, configurable independently of size; migrate from gp2 with Elastic Volumes.
- **S3**: multipart over 100 MB (required over 5 GB), Transfer Acceleration for distant uploads, DataSync for large or recurring transfers.
- **EFS lifecycle** to IA and Archive; **S3 Files** gives file system access to S3 data.
- **RDS**: Performance Insights (now CloudWatch Database Insights) for wait events and top SQL; RDS Proxy for connection storms.
- **Placement groups**: cluster (latency), spread (isolation, seven per AZ), partition (large distributed systems).

### Domain 2: Reliability and Business Continuity (22%)

Tasks: 2.1 scalability and elasticity; 2.2 highly available and resilient environments; 2.3 backup and restore.

- **Target tracking** is the default scaling policy; scheduled for known times; predictive for recurring patterns.
- **ASG not scaling**: max reached, bad launch template, no subnet IPs, capacity or quota, KMS permissions. Read the activity history.
- **Caching**: CloudFront at the edge, ElastiCache (lazy loading, write-through, TTL), DAX for DynamoDB.
- **DynamoDB**: on-demand for spiky traffic; throttling from hot keys or under-provisioned GSIs.
- **ELB checks failing**: security group, health check path, grace period. Turn on **ELB health checks** in the ASG.
- **Route 53** cannot health-check private IPs; use a CloudWatch alarm-based check.
- **Multi-AZ standby is not a read replica**; NAT gateways are zonal.
- **AWS Backup** plans by tag, cross-Region and cross-account copies, **Vault Lock** for immutability.
- **PITR restores to a new instance or table**; Aurora Backtrack rewinds in place.
- **DR**: backup and restore, pilot light, warm standby, active/active - rising cost, falling RPO and RTO.

### Domain 3: Deployment, Provisioning, and Automation (22%)

Tasks: 3.1 provision and maintain resources; 3.2 automate management of existing resources.

- **EC2 Image Builder** builds, tests and distributes AMIs and container images on a schedule.
- **AMIs are Regional**; sharing encrypted AMIs needs the customer managed KMS key shared.
- **CloudFormation**: change sets, DeletionPolicy, drift detection; `ROLLBACK_COMPLETE` stacks can only be deleted; `UPDATE_ROLLBACK_FAILED` needs continue update rollback.
- **Five reserved IPs per subnet**; `iam:PassRole` is a frequent deployment blocker.
- **AWS RAM** shares subnets, Transit Gateways and Resolver rules; **StackSets** deploy across accounts and Regions, auto-deploying to new OU accounts.
- **Deployment strategies**: rolling, immutable, blue/green, canary, linear; CodeDeploy rolls back on alarms.
- **Terraform** state in a versioned, encrypted, locked S3 backend; Git as the source of truth.
- **Systems Manager**: State Manager, Patch Manager, Run Command, Automation, Session Manager. A missing managed node is agent, role or network.
- **OpsWorks reached end of life in May 2024** - never the current answer.

### Domain 4: Security and Compliance (16%)

Tasks: 4.1 security and compliance tools and policies; 4.2 data and infrastructure protection.

- **Explicit deny wins**; SCPs never grant and do not affect the management account.
- **Troubleshoot access**: CloudTrail (what happened), policy simulator (would it be allowed), Access Analyzer (external, internal, unused access; policy validation).
- **IAM Identity Center** permission sets and assignments for multi-account human access.
- **Trusted Advisor** on Basic support: service limits plus selected security and fault tolerance checks.
- **Config conformance packs** and auto-remediation through Automation; Region restriction with SCPs.
- **Data classification** by tags enforced with tag policies and ABAC; Macie discovers sensitive data in S3.
- **KMS**: key policies are primary; encrypt existing EBS or RDS via encrypted snapshot copy.
- **ACM**: DNS validation renews automatically; imported certificates do not; CloudFront needs us-east-1.
- **Secrets Manager** for rotation; Parameter Store for configuration.
- **Findings**: GuardDuty (threats), Inspector (CVEs), Macie (sensitive data), Config (compliance), Security Hub (aggregation), Security Agent (application reviews and pen testing), routed through EventBridge.

### Domain 5: Networking and Content Delivery (18%)

Tasks: 5.1 networking features and connectivity; 5.2 DNS and content delivery; 5.3 troubleshoot connectivity.

- **Security groups stateful, NACLs stateless** (ephemeral ports); egress-only IGW for IPv6 outbound.
- **Gateway endpoints** (S3, DynamoDB, free) vs **interface endpoints** (PrivateLink, need DNS attributes for private DNS).
- **Peering is not transitive**; Transit Gateway needs association and propagation.
- **Audit**: DNS Firewall associations and actions, WAF web ACL associations and Count vs Block, Shield Advanced protected resources, Network Firewall routing and logs.
- **Network cost**: gateway endpoints instead of NAT for S3/DynamoDB, avoid cross-AZ traffic, CloudFront for egress.
- **Route 53 Resolver** inbound and outbound endpoints, forwarding rules shared with RAM; public query logs in us-east-1.
- **CloudFront vs Global Accelerator**: caching HTTP vs static IPs, TCP/UDP and fast failover.
- **Logs**: flow logs ACCEPT/REJECT, ELB access logs, WAF logs named `aws-waf-logs-*`, CloudFront standard and real-time logs.
- **CloudFront caching**: narrow cache key for hit ratio; invalidate and version file names for staleness.
- **CloudWatch network monitoring**: Network Flow Monitor, Internet Monitor, Network Synthetic Monitor.

## 💡 Study Strategy

See [strategy.md](./strategy.md) for time allocation by weight and [practice-plan.md](./practice-plan.md) for a week-by-week plan.

**📖 [AWS Skill Builder](https://skillbuilder.aws/)** - Official training, practice question sets and the official practice exam

## 🎯 Exam Day Tips

- 130 minutes for 65 questions is about **2 minutes per question**. Flag and move on; aim to leave 15 minutes for review.
- There are **no labs**, but questions are operational: they describe a broken or slow system and ask for the fix with the **least operational overhead**.
- Watch for **"most operationally efficient"** (managed and automated), **"least privilege"**, **"with the least downtime"** and **"automatically"**.
- Multiple-response questions tell you how many answers to choose. There is no penalty for guessing.

## 📊 Quick Reference

- **65 questions** (50 scored, 15 unscored) in **130 minutes**
- **720/1000 to pass**, compensatory scoring
- **22% Monitoring, logging, remediation, performance** - about 11 scored questions
- **22% Reliability and business continuity** - about 11
- **22% Deployment, provisioning, automation** - about 11
- **16% Security and compliance** - about 8
- **18% Networking and content delivery** - about 9

| Category | Core services |
|---|---|
| **Monitoring** | CloudWatch (metrics, Logs, alarms, dashboards, agent), CloudTrail, EventBridge, Managed Service for Prometheus, AWS Health |
| **Remediation** | Systems Manager Automation, Lambda, AWS DevOps Agent |
| **Performance** | Compute Optimizer, EBS, S3, EFS, FSx, S3 Files, RDS Performance Insights, RDS Proxy |
| **Reliability** | Auto Scaling, ELB, Route 53, ElastiCache, AWS Backup, Elastic Disaster Recovery |
| **Deployment** | CloudFormation, CDK, StackSets, RAM, EC2 Image Builder, CodeDeploy, Terraform |
| **Security** | IAM, Identity Center, Organizations, Access Analyzer, Config, KMS, ACM, Secrets Manager, Security Hub, GuardDuty, Inspector, Security Agent |
| **Networking** | VPC, endpoints, Transit Gateway, Route 53 Resolver, DNS Firewall, Network Firewall, WAF, Shield, CloudFront, Global Accelerator, CloudWatch network monitoring |
