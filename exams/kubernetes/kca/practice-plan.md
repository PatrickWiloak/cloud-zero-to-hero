---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 4 min
---

# KCA Study Plan

Four weeks at 4-6 hours per week. Writing Policies is 32% of the exam, so it gets the most time.

## Week 1: Fundamentals and installation

- [ ] Read note 01 and the Kubernetes admission controllers page
- [ ] Read note 02: Helm install, flags, RBAC aggregation, HA, upgrade rules
- [ ] Optional lab on a throwaway cluster: install Kyverno with Helm, list the four Deployments

## Week 2: Writing policies, part 1

- [ ] Validate: pattern, anyPattern, deny, foreach, anchors
- [ ] Preconditions and background mode
- [ ] Mutation: patchStrategicMerge, `+()` anchors, JSON patches

## Week 3: Writing policies, part 2

- [ ] Generate: data, clone, cloneList, synchronize, generateExisting
- [ ] verifyImages: defaults, digests, attestors
- [ ] Variables and context: configMap, apiCall, globalReference
- [ ] Autogen, cleanup policies and TTL labels
- [ ] CEL: `validate.cel` and the `policies.kyverno.io` types

## Week 4: CLI, applying, management, review

- [ ] Note 03: apply, test, jp, install methods
- [ ] Note 04: match and exclude, policy settings
- [ ] Note 06: reports, exceptions, metrics
- [ ] Take the [32 practice questions](../../../resources/practice-questions/cncf-kca.md) and re-read notes for misses
- [ ] Re-read the [scenarios](./scenarios.md)
