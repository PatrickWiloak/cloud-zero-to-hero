---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 6 min
---

# Kyverno Certified Associate (KCA) Fact Sheet

## Exam Overview

**Exam Code:** KCA
**Exam Name:** Kyverno Certified Associate
**Level:** Associate
**Duration:** 90 minutes
**Format:** Online, proctored, multiple choice
**Questions:** Not stated on the Linux Foundation page
**Passing Score:** Not stated on the Linux Foundation page
**Cost:** USD 250 exam only; USD 495 with the THRIVE-ONE annual subscription (listed 2026-11-07)
**Valid For:** 2 years
**Prerequisites:** None
**Scheduling window:** 12 months from purchase to schedule and take the exam

### Verified facts and sources (checked 2026-11-07)

| Fact | Value | Source |
|------|-------|--------|
| Name, duration, format | Kyverno Certified Associate, 90 minutes, online proctored multiple choice | [LF KCA page](https://training.linuxfoundation.org/certification/kyverno-certified-associate-kca/) |
| Validity | 2 years | LF KCA page |
| Price | USD 250 exam only; USD 495 bundled | LF KCA page |
| Experience level | Beginner | LF KCA page |
| Attempts | The page says "Two exam attempts" in one section and "One Retake" in another and does not reconcile them | LF KCA page |
| Question count, passing score | Not stated | LF KCA page |
| "KCA" as a code | The page lists KCA as the SKU, not a separate exam code | LF KCA page |
| Domains and weights | 18 / 18 / 12 / 10 / 32 / 10 | [CNCF curriculum](https://github.com/cncf/curriculum) (`KCA_Curriculum.pdf`) and the LF page agree |

> **Verify before booking.** Prices and policies change. Confirm on the official page. The question count and passing score are not published on the pages read, so this guide does not state them.

## Exam Domains

### Domain 1: Fundamentals of Kyverno (18%)

- Kyverno policies and rules
- YAML manifests
- Admission controllers
- OCI images

[Notes 01](./notes/01-fundamentals-of-kyverno.md)

### Domain 2: Installation, Configuration, and Upgrades (18%)

- Helm-based installation and configuration
- Kyverno Custom Resource Definitions (CRDs)
- Controller configuration with flags
- Configuring Kyverno RBAC, roles, and permissions
- High availability installations
- Upgrading Kyverno

[Notes 02](./notes/02-installation-configuration-upgrades.md)

### Domain 3: Kyverno CLI (12%)

- apply
- test
- jp
- Installing Kyverno CLI

[Notes 03](./notes/03-kyverno-cli.md)

### Domain 4: Applying Policies (10%)

- Applying policy in cluster
- Resource selection
- Common policy settings for Kyverno rules

[Notes 04](./notes/04-applying-policies.md)

### Domain 5: Writing Policies (32%)

- Validation rules
- Preconditions
- Background scans
- Mutation rules
- Generation rules
- VerifyImage rules
- Variables and API calls in policies
- JSON patches
- Autogen rules
- Cleanup policies
- Common Expression Language (CEL)

[Notes 05](./notes/05-writing-policies.md)

### Domain 6: Policy Management (10%)

- Policy reports
- PolicyExceptions
- Kyverno metrics

[Notes 06](./notes/06-policy-management.md)

## Quick reference

| Question | Answer |
|---|---|
| Audit or Enforce blocks? | Enforce blocks; Audit reports |
| Do preconditions block? | No; they decide if the rule applies (report `skip`) |
| Does a background scan block? | Never, even in Enforce |
| Default background scan interval | 1 hour |
| Default webhook timeout | 10 seconds (1 to 30) |
| Metrics port and path | 8000, `/metrics` |
| Are PolicyExceptions on by default? | No; need `enablePolicyException` and `exceptionNamespace` |
| Report API group | `wgpolicyk8s.io/v1alpha2` |
| Autogen controller annotation | `pod-policies.kyverno.io/autogen-controllers` |
| TTL cleanup label | `cleanup.kyverno.io/ttl` |
| HA admission replicas | Three (the HA page's minimum) |

## Related repo material

- [Notes](./notes/)
- [Practice plan](./practice-plan.md)
- [Scenarios](./scenarios.md)
- [Strategy](./strategy.md)
- [Practice questions](../../../resources/practice-questions/cncf-kca.md)
