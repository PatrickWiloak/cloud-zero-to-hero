---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 4 min
---

# CNPE Study Strategy

## Follow the weights

| Domain | Weight | Share of study time |
|---|---:|---|
| Platform Architecture and Infrastructure | 15% | Networking, storage, compute, cost, multi-tenancy |
| GitOps and Continuous Delivery | 25% | Argo CD, Flux, Tekton, canary and blue/green |
| Platform APIs and Self-Service Capabilities | 25% | CRDs, operators, Crossplane, self-service provisioning |
| Observability and Operations | 20% | Prometheus, OpenTelemetry, DORA metrics, incidents |
| Security and Policy Enforcement | 15% | mTLS, RBAC, audit, SBOM, policy engines, pipeline scanning |

## Practice finding, not remembering

The curriculum says candidates complete tasks "using unfamiliar tools by relying on help and documentation available in the exam." Train the skill the exam tests: given a tool you have never used, find a working example in its documentation, adapt it and verify it. Which documentation sites the exam permits is not stated on the LF page, so confirm in the candidate instructions.

## Time

Two hours for multiple tasks, count not published. Practice triage: do the tasks you can finish fast first, flag the ones that need reading, and never leave a task half applied without noting it.

## Verify every task

A performance-based exam grades the state of the cluster, not your intent. After every change run the check that proves it: `kubectl get`, a status condition, a sync status, a metric. Under GitOps remember that fixes made with `kubectl` can be reverted; change the source.

## Distinctions to own

- **Argo CD `prune` versus `selfHeal`.**
- **Source versus Kustomization** in Flux.
- **Pipeline versus PipelineRun** in Tekton.
- **Rollout versus Canary (Flagger)**: replace the Deployment versus wrap it.
- **CRD versus operator**: schema versus controller.
- **XRD versus Composition versus XR.**
- **PERMISSIVE versus STRICT.**
- **Audit level versus audit stage.**
- **Constraint versus ConstraintTemplate.**

## Do not over-study

You will not be tested on deep tool-specific knowledge unless it is in the competencies. Breadth across the listed tools, with strong Kubernetes fundamentals, beats depth in one.
