---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 6 min
---

# Certified Kubernetes Network Engineer (CKNE) Fact Sheet

## Exam Overview

**Exam Code:** Not stated by the Linux Foundation page (it uses CKNE as the purchase SKU)
**Exam Name:** Certified Kubernetes Network Engineer
**Level:** Intermediate experience level (per the LF page)
**Duration:** 2 hours
**Format:** Online, proctored, performance-based: tasks solved in a Linux-based remote desktop using the terminal and web-based interfaces
**Questions:** Not stated ("multiple tasks")
**Passing Score:** Not stated on the Linux Foundation page
**Cost:** USD 445 exam only; USD 625 with the THRIVE-ONE annual subscription; USD 645 for the Certification Pathway bundle (listed 2026-11-07)
**Valid For:** 2 years
**Prerequisites:** None required; the FAQ says CKNE assumes CKA-level Kubernetes administration skills

### Verified facts and sources (checked 2026-11-07)

| Fact | Value | Source |
|------|-------|--------|
| Name, duration, format | Certified Kubernetes Network Engineer, 2 hours, online proctored performance-based in a Linux remote desktop | [LF CKNE page](https://training.linuxfoundation.org/certification/certified-kubernetes-network-engineer-ckne/) |
| Validity | 2 years | LF CKNE page |
| Price | USD 445 exam only; USD 625 with THRIVE-ONE; USD 645 Certification Pathway bundle | LF CKNE page |
| Retake, eligibility | One retake included; 12-month exam eligibility | LF CKNE page |
| Prerequisites | None required; FAQ says CKNE assumes CKA-level skills | LF CKNE page |
| Release | Page labeled NEW, publication date 2026-06-10 in its metadata; no exam launch date stated | LF CKNE page |
| Question count, passing score, exam code, Kubernetes version, allowed docs, featured tools | Not stated | LF CKNE page |
| Domains and weights | 15 / 25 / 20 / 25 / 15 | [CNCF curriculum](https://github.com/cncf/curriculum) (`CKNE_Curriculum.pdf`) and the LF page agree |

> **Verify before booking.** Prices and policies change. Confirm on the official page. Items marked "not stated" were not on the pages read, so this guide does not guess them.

## Exam Domains

### Core Infrastructure and CNI (15%)

- Installing and Configuring CNI Plugins
- Managing IPAM and Pod CIDR Allocation
- Using Linux Tools (iptables, ip, tcpdump) for Packet-level Issues
- Troubleshooting Pod Connectivity (DNS, pod-to-pod)
- Configuring Multi-interface Pods

[Notes 01](./notes/01-core-infrastructure-and-cni.md)

### Service Networking and DNS (25%)

- Configuring L4 Services
- Understanding kube-proxy and CNI Alternatives
- Customizing coreDNS for Services
- Troubleshooting Service Network Traffic
- Configuring Pod Endpoint Availability
- Managing Traffic with the Gateway API (Gateway, HTTPRoutes)

[Notes 02](./notes/02-service-networking-and-dns.md)

### Advanced Traffic Management (20%)

- Optimizing LLM Traffic
- Implementing Routing to Expose Networks
- Configuring Egress Gateways for Cluster Exit Traffic
- Implementing Cross Cluster Service Discovery and Load Balancing

[Notes 03](./notes/03-advanced-traffic-management.md)

### Network Security and Policy (25%)

- Securing Traffic with Network Policies
- Implementing Node and Pod Level Encryption
- Managing TLS Certificates for Gateway API
- Implementing Pod-level Authentication and Authorization

[Notes 04](./notes/04-network-security-and-policy.md)

### Observability (15%)

- Analyzing Network Health Using Metrics
- Troubleshooting End-to-End Network Performance with Tracing
- Auditing Traffic with Logs

[Notes 05](./notes/05-observability.md)

## Quick reference

| Question | Answer |
|---|---|
| Format | Performance-based, 2 hours |
| Who assigns Pod IPs? | The network plugin |
| Who assigns Service IPs? | The kube-apiserver |
| Who loads CNI plugins? | The container runtime (kubelet flags removed in 1.24) |
| Minimum CNI spec | v0.4.0 (v1.0.0 recommended) |
| NodePort default range | 30000-32767 |
| kube-proxy Linux modes | iptables, ipvs, nftables |
| CoreDNS config | `coredns` ConfigMap, `Corefile` key, `kube-system` |
| CoreDNS reload wait | Up to two minutes |
| Pod resolv.conf ndots | 5 |
| Gateway accepts routes from | Its own namespace by default |
| HTTPRoute weight | Proportion of the total; default 1 |
| NetworkPolicy combining | Additive (union) |
| NetworkPolicy needs | A CNI that enforces it |
| Cilium strict ingress mode | WireGuard only, not IPsec |
| Istio AuthorizationPolicy principals | Require mTLS |
| Cluster Mesh cluster ID | 1 to 255 |
| Hubble port | 9965 |

## Related repo material

- [Notes](./notes/)
- [Practice plan](./practice-plan.md)
- [Scenarios](./scenarios.md)
- [Strategy](./strategy.md)
- [Practice questions](../../../resources/practice-questions/cncf-ckne.md)
