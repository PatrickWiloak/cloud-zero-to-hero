---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 5 min
---

# Certified Kubernetes Network Engineer (CKNE)

The CNCF and Linux Foundation certification for Kubernetes networking. CKNE validates "hands-on skills in designing, securing, and troubleshooting Kubernetes networking" (the page's own description): CNI plugins and IPAM, Services, kube-proxy and CoreDNS, the Gateway API, egress and cross-cluster traffic, Network Policies, encryption and observability.

The Linux Foundation page is marked NEW with a publication date of 2026-06-10. It is a performance-based exam like [CKA](../cka/), so you will be at a terminal fixing and building things, not choosing from a list.

The LF FAQ says CKNE assumes CKA-level skills, suggests earning CKA first or alongside, and suggests pairing CKNE with [CCA (Cilium)](../cca/) or [ICA (Istio)](../ica/) for deeper specialization.

## Exam Details (checked 2026-11-07)

- **Exam Code:** Not stated by the Linux Foundation page (it uses CKNE as the purchase SKU)
- **Duration:** 2 hours
- **Questions:** Not stated ("multiple tasks")
- **Passing Score:** Not stated on the Linux Foundation page
- **Cost:** USD 445 exam only; USD 625 with the THRIVE-ONE annual subscription; USD 645 for the Certification Pathway bundle (listed 2026-11-07)
- **Validity:** 2 years
- **Prerequisites:** None required; the FAQ says CKNE assumes CKA-level Kubernetes administration skills
- **Format:** Online, proctored, performance-based: tasks solved in a Linux-based remote desktop using the terminal and web-based interfaces

Full detail and sources in the [fact sheet](./fact-sheet.md).

## Domains

| Domain | Weight | Notes |
|--------|-------:|-------|
| Core Infrastructure and CNI | 15% | [01](./notes/01-core-infrastructure-and-cni.md) |
| Service Networking and DNS | 25% | [02](./notes/02-service-networking-and-dns.md) |
| Advanced Traffic Management | 20% | [03](./notes/03-advanced-traffic-management.md) |
| Network Security and Policy | 25% | [04](./notes/04-network-security-and-policy.md) |
| Observability | 15% | [05](./notes/05-observability.md) |

Service Networking and DNS and Network Security and Policy are a quarter each. Together with Advanced Traffic Management they are 70% of the exam.

## How these notes were built

This is a performance-based exam, so the notes are task-oriented. YAML was syntax-checked with a parser; **nothing was applied to a cluster**, because none was available. The LF page does not say which Kubernetes version the exam uses or which documentation you may open; check the candidate instructions before you book. Domain 3 (advanced traffic management) names no tools on the LF page, so the notes use the documented implementations most closely tied to each competency (Gateway API Inference Extension, Cilium BGP and Cluster Mesh, Istio egress gateways and multicluster). Expect the exam to use whatever the environment installs.

## Study sequence

1. Be fluent in CKA-level Kubernetes first (CKA guide).
2. Services, kube-proxy and CoreDNS: be able to break and fix each.
3. Network Policies and the Gateway API: write them from the docs.
4. CNI and IPAM: know where config lives and how Pod connectivity fails.
5. Encryption, mTLS and authorization.
6. Egress, cross-cluster and LLM traffic.
7. Observability: Hubble, Istio and CoreDNS metrics, logs and traces.

Schedule in the [practice plan](./practice-plan.md).

## Study resources

- **[📖 Linux Foundation CKNE page](https://training.linuxfoundation.org/certification/certified-kubernetes-network-engineer-ckne/)** - registration and logistics
- **[📖 CKNE curriculum](https://github.com/cncf/curriculum)** - the CNCF curriculum repo with `CKNE_Curriculum.pdf`
- **[📖 Kubernetes networking documentation](https://kubernetes.io/docs/concepts/services-networking/)** - Services, DNS, Gateway API, Network Policies
- [Practice questions](../../../resources/practice-questions/cncf-ckne.md) - 30 original questions in this repo

## Related

- [CKA](../cka/) - the Kubernetes administration the exam assumes
- [CCA Cilium](../cca/) - CNI, Hubble, encryption, Cluster Mesh
- [ICA Istio](../ica/) - mesh traffic, mTLS, authorization
- [CNPE Platform Engineer](../cnpe/) - the platform tasks around networking
- [Networking topic](../../../topics/networking.md)
- [Kubernetes topic](../../../topics/kubernetes.md)
