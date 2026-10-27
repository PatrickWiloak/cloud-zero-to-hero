---
last-updated: 2026-05-03
difficulty: any
reading-time: 4 min
---

# Networking

VPCs, subnets, routing, hybrid connectivity, DNS, load balancing, multi-cloud networking. Networking is the layer everyone forgets until something doesn't connect.

```mermaid
flowchart LR
  U[Internet users] --> CDN[CDN / edge]
  CDN --> LB[Global / regional load balancer]
  LB --> VPC[VPC / VNet:<br/>subnets, route tables, security groups]
  VPC --> APP[App tier]
  APP --> DB[(Private DB)]
  ONP[On-prem] -. VPN / Direct Connect / ExpressRoute / Interconnect .-> VPC
  DNS[DNS:<br/>Route 53 / Cloud DNS / Azure DNS] -.- CDN
  DNS -.- LB
```

---

## Learn

- [VPC explained](../learn/concepts/vpc-explained.md) - private network basics, CIDR, subnets, route tables
- [DNS explained](../learn/concepts/dns-explained.md) - resolution, records, recursion, caching
- [TLS and HTTPS](https://security.noblerworks.com/learn/concepts/tls-and-https/) - what TLS actually does
- [CDN explained](../learn/concepts/cdn-explained.md) - edge caching, origin shielding
- [Regions and availability zones](../learn/concepts/regions-and-availability-zones.md) - the geography of cloud
- [API gateways explained](../learn/concepts/api-gateways-explained.md) - the managed front door for APIs, vs a load balancer
- [Edge computing explained](../learn/concepts/edge-computing-explained.md) - CDN functions, Local Zones, on-premises edge
- [Service mesh explained](../learn/concepts/service-mesh-explained.md) - east-west traffic inside the cluster

---

## Compare

- [Networking services](../resources/service-comparison-networking.md) - VPC, peering, transit, load balancers across clouds

---

## Reference

- [Hybrid connectivity](../resources/networking-deep-dives/hybrid-connectivity.md) - VPN, Direct Connect, ExpressRoute, Interconnect
- [Multi-cloud networking](../resources/networking-deep-dives/multi-cloud-networking.md) - cross-cloud private connectivity
- [DNS deep dive](../resources/networking-deep-dives/dns-deep-dive.md) - delegation, GeoDNS, latency-based routing
- [Load balancing deep dive](../resources/networking-deep-dives/load-balancing-deep-dive.md) - L4 vs L7, health checks, session affinity
- [Architecture pattern: Hybrid cloud connectivity](../resources/architecture-patterns/hybrid-cloud-connectivity.md)

---

## Build

- [Deploy a 3-tier app](../resources/hands-on-projects/deploy-3-tier-app.md) - VPC, subnets, ALB end-to-end
- [Kubernetes cluster setup](../resources/hands-on-projects/kubernetes-cluster-setup.md) - cluster networking, CNI

---

## Certify

**Foundational**
- [AWS Cloud Practitioner](../exams/aws/foundational/cloud-practitioner-clf-c02/)
- [Azure AZ-900](../exams/azure/az-900/)

**Associate**
- [AWS Solutions Architect Associate (SAA-C03)](../exams/aws/associate/solutions-architect-saa-c03/)
- [Azure Administrator (AZ-104)](../exams/azure/az-104/)
- [Azure Network Engineer (AZ-700)](../exams/azure/az-700/)
- [GCP Cloud Engineer](../exams/gcp/cloud-engineer/)

**Cisco / vendor-specific**
- [Cisco CCNA (200-301)](../exams/cisco/ccna-200-301/) - foundational networking, routing, switching
- [Cisco CCNP Enterprise (350-401)](../exams/cisco/ccnp-enterprise-encor-350-401/)
- [CompTIA Network+](../exams/comptia/network-plus/)

**Professional / Specialty**
- [AWS Solutions Architect Professional (SAP-C02)](../exams/aws/professional/solutions-architect-pro-sap-c02/)
- [AWS Advanced Networking Specialty (ANS-C01)](../exams/aws/specialty/advanced-networking-ans-c01/)
- [GCP Cloud Network Engineer](../exams/gcp/cloud-network-engineer/)
- [NVIDIA Networking Professional](https://ai.noblerworks.com/certifications/nvidia/ai-networking-professional/) - data center fabric for AI workloads

**Service mesh and ingress**
- [Istio Certified Associate (ICA)](../exams/kubernetes/ica/)
- [HashiCorp Consul Associate](../exams/hashicorp/consul-associate/)

---

## Roadmap

Networking deep-dive paths live in the **[Cloud Engineer roadmap](../resources/certification-roadmap-cloud-engineer.md)** and the **[Solutions Architect roadmap](../resources/certification-roadmap-solutions-architect.md)**.
