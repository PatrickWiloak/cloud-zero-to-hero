---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 4 min
---

# CKNE Study Plan

Six weeks at 5-7 hours per week. This is a hands-on exam, so spend most of each week at a terminal on a throwaway cluster you are allowed to break. If you have not passed CKA, expect to need a few extra weeks of Kubernetes fundamentals.

## Week 1: CNI and Pod connectivity

- [ ] Note 01; read your cluster's CNI config directory and Pod CIDR settings
- [ ] Break Pod-to-Pod traffic on purpose and walk the troubleshooting order
- [ ] Optional: attach a second interface with Multus

## Week 2: Services, kube-proxy and DNS

- [ ] Note 02, first half; every Service type, a selector-less Service with an EndpointSlice
- [ ] Find out which kube-proxy mode your cluster uses
- [ ] Edit the `coredns` ConfigMap with a stub domain and watch it reload

## Week 3: Gateway API

- [ ] Install a Gateway API implementation, create a GatewayClass, Gateway and HTTPRoute
- [ ] Weighted split, then a header-match rule
- [ ] Make a cross-namespace route work with `allowedRoutes`

## Week 4: Network security

- [ ] Note 04; default-deny, then allow DNS and one app path
- [ ] HTTPS listener with `certificateRefs`; a cross-namespace Secret with a ReferenceGrant
- [ ] STRICT mTLS and one AuthorizationPolicy, or Cilium encryption

## Week 5: Advanced traffic

- [ ] Note 03; egress gateway walkthrough, multicluster concepts, BGP advertisement concepts
- [ ] Read the Gateway API Inference Extension docs for InferencePool

## Week 6: Observability and review

- [ ] Note 05; Hubble drops, CoreDNS metrics, Istio access logs
- [ ] Take the [30 practice questions](../../../resources/practice-questions/cncf-ckne.md)
- [ ] Timed practice: three broken-network tasks in two hours
