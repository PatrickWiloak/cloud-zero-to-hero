---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 4 min
---

# CNPE Study Plan

Six weeks at 5-7 hours per week. This is a hands-on exam, so most of each week should be at a terminal on a throwaway cluster you can break. Practice reading documentation to find an example, because the curriculum says you will meet unfamiliar tools.

## Week 1: Fast Kubernetes

- [ ] Note 01; write a ResourceQuota and LimitRange from `kubectl explain` and the docs
- [ ] Set up an HPA and see it fail without Metrics Server
- [ ] Write a CRD and a custom resource from the docs example

## Week 2: GitOps

- [ ] Note 02, GitOps part; one Argo CD Application with `automated`, `prune`, `selfHeal`
- [ ] One Flux GitRepository plus Kustomization with `dependsOn`
- [ ] Break something with `kubectl` and watch it get reverted

## Week 3: CI and progressive delivery

- [ ] Tekton Pipeline with params, workspace, `runAfter`, `finally`
- [ ] Argo Rollouts canary with `pause: {}` and promote
- [ ] Flagger Canary with a failing metric and watch the rollback

## Week 4: Platform APIs

- [ ] Note 03; read the Crossplane XRD and Composition pages and describe each field aloud
- [ ] Install an operator from OperatorHub and use its custom resource
- [ ] Design a small platform API (3 to 5 fields) and write its schema

## Week 5: Observability and operations

- [ ] Note 04; write an alerting rule and trigger it
- [ ] Run a Collector locally (see the OTCA guide)
- [ ] Debug three broken-cluster scenarios using the incident method

## Week 6: Security and review

- [ ] Note 05; STRICT mTLS for one namespace, Role plus RoleBinding, an audit policy
- [ ] One Gatekeeper or Kyverno policy in dry-run, then enforce
- [ ] Take the [30 practice questions](../../../resources/practice-questions/cncf-cnpe.md)
- [ ] Do both LF simulator attempts, timed, and review every miss
