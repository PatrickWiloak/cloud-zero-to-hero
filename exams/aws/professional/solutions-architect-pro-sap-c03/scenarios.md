---
last-updated: 2026-11-07
---

# AWS Certified Solutions Architect - Professional (SAP-C03) - Trade-off Scenarios

Original scenarios showing how constraints select the answer. They are not vendor exam questions.

## Domain 1: Architecture

### Many microservices, many accounts, minimal operations
**Scenario:** A company runs 40 services across 12 accounts on ECS and Lambda. Teams want service-to-service calls with authentication policies and request metrics, and no sidecars to manage.
**Analysis:** the constraint is "no sidecars, many accounts and VPCs". **VPC Lattice** provides service networks with auth policies across VPCs and accounts. A self-run mesh adds operations; Service Connect is limited to ECS services in a namespace.

### Hybrid DNS
**Scenario:** On-premises servers must resolve private hosted zone names, and VPC workloads must resolve corp.example names.
**Analysis:** Route 53 Resolver **inbound** endpoint for on-premises to AWS, **outbound** endpoint with a forwarding rule for AWS to on-premises.

## Domain 2: Security

### Third-party vendor access
**Scenario:** A SaaS vendor must read cost data in your account. You must prevent another customer of the vendor from tricking the vendor into assuming your role.
**Analysis:** a cross-account role with an **external ID** condition in the trust policy (confused deputy protection), with a least-privilege policy.

### Region guardrail
**Scenario:** The compliance team requires that no resources be created outside two Regions, even by account administrators.
**Analysis:** an **SCP** with a Deny on requests where `aws:RequestedRegion` is not in the approved list, excluding global services. An IAM policy inside each account could be removed by that account's admins.

## Domain 3: Cost

### Hidden transfer charge
**Scenario:** Private-subnet workloads move 30 TB a month to and from S3, and the NAT gateway data processing line is the largest networking cost.
**Analysis:** add an S3 **gateway VPC endpoint** (no charge), routing S3 traffic around the NAT gateway.

## Domain 4: Resilience

### Matching DR to numbers
**Scenario:** An application needs an RTO of 15 minutes and an RPO of 1 minute, but the budget excludes running full capacity in a second Region.
**Analysis:** **warm standby**: continuous replication (RPO) plus a scaled-down running environment that scales up on failover (RTO). Pilot light's longer startup may miss 15 minutes; active/active exceeds the budget.

## Domain 5: Operations

### Safe automated remediation
**Scenario:** An alarm triggers a Lambda function that restarts instances. During a regional dependency outage it restarts hundreds of instances repeatedly and worsens the problem.
**Analysis:** add safety constraints: **rate limits**, a **circuit breaker** that stops remediation when failures persist, and limits on the blast radius per run.
