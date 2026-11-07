---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 5 min
---

# Certified Cloud Native Platform Engineer (CNPE)

The CNCF and Linux Foundation certification for platform engineers. Where [CNPA](../cnpa/) tests whether you understand platform engineering, CNPE tests whether you can **do it**: wire up GitOps and CI/CD, ship progressive delivery, publish platform APIs with CRDs and Crossplane, run observability, and enforce policy and mTLS, all at a terminal with the documentation open.

The curriculum says you will use "unfamiliar tools by relying on help and documentation available in the exam" and will not be tested on deep tool-specific knowledge unless a competency names it. That shapes how to study: practice finding answers fast, and make the Kubernetes fundamentals automatic.

## Exam Details (checked 2026-11-07)

- **Exam Code:** Not stated by the Linux Foundation page (it uses CNPE as the purchase SKU)
- **Duration:** 2 hours
- **Questions:** Not stated for the exam ("multiple tasks"); the exam simulator has 20 questions
- **Passing Score:** Not stated on the Linux Foundation page
- **Cost:** USD 445 exam only; USD 625 with the THRIVE-ONE annual subscription (listed 2026-11-07)
- **Validity:** 2 years
- **Prerequisites:** None; the page lists the experience level as Intermediate and says CNPE pairs well with other credentials (CKA is one of them)
- **Format:** Online, proctored, performance-based: tasks solved in a Linux-based remote desktop using the terminal and web-based interfaces

Full detail and sources in the [fact sheet](./fact-sheet.md).

## Domains

| Domain | Weight | Notes |
|--------|-------:|-------|
| Platform Architecture and Infrastructure | 15% | [01](./notes/01-platform-architecture-and-infrastructure.md) |
| GitOps and Continuous Delivery | 25% | [02](./notes/02-gitops-and-continuous-delivery.md) |
| Platform APIs and Self-Service Capabilities | 25% | [03](./notes/03-platform-apis-and-self-service.md) |
| Observability and Operations | 20% | [04](./notes/04-observability-and-operations.md) |
| Security and Policy Enforcement | 15% | [05](./notes/05-security-and-policy-enforcement.md) |

GitOps and Platform APIs together are half the exam (25% each). Observability is 20%, and architecture and security are 15% each.

## Tools the curriculum says may appear

Argo, Crossplane, Flagger, Flux, Gatekeeper, Grafana, Istio, Jaeger, Kyverno, Linkerd, OPA, OpenCost, OpenTelemetry, Prometheus and Tekton. The curriculum calls these examples of what may be included, and warns you will not be tested on deep tool-specific knowledge unless it is in the competencies.

## A note on how these notes were built

This is a performance-based exam, so the notes are task-oriented. YAML was syntax-checked with a parser; nothing was applied to a cluster, because none was available. Commands are quoted from vendor docs and marked as not run. Which documentation sites the exam lets you open is **not stated** on the LF page; check the candidate instructions before you book.

## Study sequence

1. Make Kubernetes fundamentals fast: CRDs, RBAC, quotas, `kubectl explain`, finding examples in docs.
2. GitOps: one Argo CD Application and one Flux Kustomization from memory.
3. Platform APIs: write a CRD, then read a Crossplane XRD and Composition.
4. Progressive delivery: a canary Rollout and a Flagger Canary.
5. Observability: an alerting rule, a Collector pipeline, the DORA metrics.
6. Security: PeerAuthentication, a Role and binding, an audit policy, one policy engine.
7. Time yourself: the exam gives 2 hours for multiple tasks, and the LF simulator has 20 questions.

Schedule in the [practice plan](./practice-plan.md).

## Study resources

- **[📖 Linux Foundation CNPE page](https://training.linuxfoundation.org/certification/certified-cloud-native-platform-engineer-cnpe/)** - registration, logistics, simulator
- **[📖 CNPE curriculum](https://github.com/cncf/curriculum)** - the CNCF curriculum repo with `CNPE_Curriculum.pdf`
- **[📖 Kubernetes documentation](https://kubernetes.io/docs/)** - the base for every task
- [Practice questions](../../../resources/practice-questions/cncf-cnpe.md) - 30 original questions in this repo

## Related

- [CNPA Platform Engineering Associate](../cnpa/) - the concepts behind the tasks
- [CKA](../cka/) - Kubernetes administration skills the tasks assume
- [CGOA](../cgoa/) and [CAPA](../capa/) - GitOps and Argo depth
- [ICA Istio](../ica/) - service mesh depth
- [PCA](../pca/) and [OTCA](../otca/) - metrics and telemetry depth
- [KCA Kyverno](../kca/) - policy engine depth
- [Platform engineering topic](../../../topics/platform-engineering.md)
