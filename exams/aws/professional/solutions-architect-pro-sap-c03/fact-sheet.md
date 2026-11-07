---
last-updated: 2026-11-07
exam-version: SAP-C03
---

# AWS Certified Solutions Architect - Professional (SAP-C03) Fact Sheet

> **Timeline (from AWS):** SAP-C02 is in use until 2026-11-16; SAP-C03 is in use from 2026-11-17.

## Quick Reference

**Exam Code:** SAP-C03
**Duration:** 180 minutes
**Questions:** 75 questions, 65 scored and 10 unscored (multiple choice and multiple response)
**Passing Score:** 720 on a scaled score of 100-1,000
**Cost:** 300 USD
**Validity:** Not verified on the pages read
**Delivery:** Not verified on the pages read

## Exam Domains

| Domain | Weight | Tasks |
|--------|--------|-------|
| 1. Architecture Design and Implementation Built for the Cloud | 25% | 1.1 cloud-built architectures; 1.2 AI/ML integration; 1.3 hybrid; 1.4 network; 1.5 data, storage, database |
| 2. Security, Compliance, and Governance | 25% | 2.1 identity; 2.2 encryption and keys; 2.3 multi-account governance; 2.4 compliance; 2.5 security and responsible AI |
| 3. Cost-Optimized Architecture Design | 15% | 3.1 pricing models; 3.2 data transfer and network; 3.3 allocation and visibility; 3.4 storage and database |
| 4. Resilience, Migration, and Business Continuity | 15% | 4.1 migration; 4.2 disaster recovery; 4.3 business continuity |
| 5. Operational Excellence and Automation | 20% | 5.1 IaC; 5.2 CI/CD and DevSecOps; 5.3 observability; 5.4 operational automation |

## Disaster recovery strategies

| Strategy | RTO / RPO | Cost |
|----------|-----------|------|
| Backup and restore | Hours / hours | Lowest |
| Pilot light | Tens of minutes / minutes | Low |
| Warm standby | Minutes / seconds to minutes | Medium |
| Multi-site active/active | Near zero / near zero | Highest |

## Governance controls compared

| Control | Scope | Grants permissions? |
|---------|-------|--------------------|
| SCP | Principals in member accounts | No, only limits |
| RCP | Resources in member accounts | No, only limits |
| Permissions boundary | One IAM role or user | No, only limits |
| Session policy | One assumed-role session | No, only limits |
| Identity-based policy | Attached principal | Yes |
| Resource-based policy | Attached resource | Yes, including cross-account |

## Connectivity choices

| Need | Choice |
|------|--------|
| Private, consistent-latency link to AWS | Direct Connect (pair across locations for resilience) |
| Quick encrypted path, or backup for Direct Connect | Site-to-Site VPN |
| Many VPCs and sites, transitive routing | Transit Gateway |
| Expose one service privately, overlapping CIDRs | PrivateLink |
| Two VPCs, simple, non-transitive | VPC peering |
| Service-to-service networking with auth policies | VPC Lattice |
| Static anycast IPs, fast failover independent of DNS | Global Accelerator |

## Official Resources

- **[📖 SAP-C03 Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/solutions-architect-professional-03.html)** - Source for all weights and tasks
- **[📖 SAP-C03 in-scope services](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/sap-03-in-scope-services.html)** - Service list
