---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 6 min
---

# Certified Cloud Native Platform Engineer (CNPE) Fact Sheet

## Exam Overview

**Exam Code:** Not stated by the Linux Foundation page (it uses CNPE as the purchase SKU)
**Exam Name:** Certified Cloud Native Platform Engineer
**Level:** Intermediate experience level (per the LF page)
**Duration:** 2 hours
**Format:** Online, proctored, performance-based: tasks solved in a Linux-based remote desktop using the terminal and web-based interfaces
**Questions:** Not stated for the exam ("multiple tasks"); the exam simulator has 20 questions
**Passing Score:** Not stated on the Linux Foundation page
**Cost:** USD 445 exam only; USD 625 with the THRIVE-ONE annual subscription (listed 2026-11-07)
**Valid For:** 2 years
**Prerequisites:** None; the page lists the experience level as Intermediate and says CNPE pairs well with other credentials (CKA is one of them)

### Verified facts and sources (checked 2026-11-07)

| Fact | Value | Source |
|------|-------|--------|
| Name, duration, format | Certified Cloud Native Platform Engineer, 2 hours, online proctored performance-based in a Linux remote desktop | [LF CNPE page](https://training.linuxfoundation.org/certification/certified-cloud-native-platform-engineer-cnpe/) |
| Validity | 2 years | LF CNPE page |
| Price | USD 445 exam only; USD 625 bundled | LF CNPE page |
| Retake, eligibility | One retake included; 12-month exam eligibility | LF CNPE page |
| Simulator | Two Killer.sh simulation attempts; the simulation has 20 questions and gives graded results | LF CNPE page |
| Prerequisites | None; CKA is suggested as a complement, not required | LF CNPE page |
| Question count, passing score, exam code, Kubernetes version, allowed docs | Not stated | LF CNPE page |
| Domains and weights | 15 / 25 / 25 / 20 / 15 | [CNCF curriculum](https://github.com/cncf/curriculum) (`CNPE_Curriculum.pdf`) and the LF page agree |

> **Verify before booking.** Prices and policies change. Confirm on the official page. Items marked "not stated" were not on the pages read, so this guide does not guess them.

## Exam Domains

### Platform Architecture and Infrastructure (15%)

- Applying Platform Architecture Best Practices for Networking, Storage, and Compute
- Using Cost Management Solutions for Right-Sizing and Scaling
- Optimizing Multi-Tenancy Resource Usage

[Notes 01](./notes/01-platform-architecture-and-infrastructure.md)

### GitOps and Continuous Delivery (25%)

- Implementing GitOps Workflows for Application and Infrastructure Deployment
- Building and Configuring CI/CD Pipelines Integrated with Kubernetes
- Deploying Applications Using Progressive Delivery Strategies (e.g., Blue/Green or Canary)

[Notes 02](./notes/02-gitops-and-continuous-delivery.md)

### Platform APIs and Self-Service Capabilities (25%)

- Designing and Creating Custom Resource Definitions (CRDs) for Platform Services
- Implementing Workflows for Self-Service Provisioning Using Platform APIs
- Using Kubernetes Operators for Platform Automation and Integration
- Using Automation Frameworks for Self-Service Provisioning

[Notes 03](./notes/03-platform-apis-and-self-service.md)

### Observability and Operations (20%)

- Implementing Monitoring, Alerting, Logging, and Tracing Solutions
- Measuring and Improving Platform Efficiency Using Deployment Metrics and Performance Indicators
- Diagnosing and Remediating Platform Issue and Incident Scenarios

[Notes 04](./notes/04-observability-and-operations.md)

### Security and Policy Enforcement (15%)

- Configuring Secure Service-to-Service Communication
- Applying RBAC and Security Controls Across Platform Resources
- Generating Audit Trails and Enforcing Policy Compliance (SBOM, Compliance Reports, etc.)
- Using Policy Engines and Admission Controllers for Governance
- Integrating Security Scanning and Compliance Checks into Deployment Pipelines

[Notes 05](./notes/05-security-and-policy-enforcement.md)

## Quick reference

| Question | Answer |
|---|---|
| Format | Performance-based, 2 hours, terminal plus web interfaces |
| Biggest domains | GitOps and CD 25%, Platform APIs and Self-Service 25% |
| Argo CD auto-fix drift | `syncPolicy.automated.selfHeal: true` |
| Argo CD delete removed resources | `syncPolicy.automated.prune: true` |
| Flux Kustomization minimum interval | 60 seconds |
| Tekton ordering without data | `runAfter` |
| Tekton always-run tasks | `finally` |
| Rollout waits for a human | `pause: {}` then `kubectl argo rollouts promote` |
| CRD name format | `<plural>.<group>` |
| Storage versions per CRD | Exactly one |
| Crossplane function rule | Copy forward all desired state or resources are deleted |
| Istio strict mTLS | `PeerAuthentication` with `mtls.mode: STRICT` |
| Linkerd proxy cert lifetime | 24 hours, rotated automatically |
| Alert pending until | The `for` duration has elapsed |
| Audit level that logs request bodies | `Request` (and `RequestResponse` adds responses) |
| Gatekeeper default enforcement | `deny` |

## Related repo material

- [Notes](./notes/)
- [Practice plan](./practice-plan.md)
- [Scenarios](./scenarios.md)
- [Strategy](./strategy.md)
- [Practice questions](../../../resources/practice-questions/cncf-cnpe.md)
