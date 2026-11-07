---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 4 min
---

# CKNE Study Strategy

## Follow the weights

| Domain | Weight | Share of study time |
|---|---:|---|
| Core Infrastructure and CNI | 15% | CNI, IPAM, Linux packet tools, Pod connectivity, Multus |
| Service Networking and DNS | 25% | Services, kube-proxy, CoreDNS, endpoints, Gateway API |
| Advanced Traffic Management | 20% | LLM traffic, exposing networks, egress gateways, cross-cluster |
| Network Security and Policy | 25% | Network Policies, encryption, Gateway TLS, Pod authN/authZ |
| Observability | 15% | Metrics, tracing, logs |

## Work the layers in order

Nearly every networking task is a layer problem. Move one hop at a time: Pod has an IP, Pod reaches its node, Pod reaches another Pod, Pod reaches a Service IP, Pod resolves a Service name, policy allows the path, the Gateway routes it. Say out loud which hop failed before you change anything.

## Find out what is installed first

The environment decides your tools. Before changing anything check the CNI (what is in the CNI config directory and `kube-system`), the kube-proxy mode (or whether kube-proxy exists at all), the DNS setup, and which Gateway or mesh controllers are present. Domain 3 names no tools on the LF page.

## Verify with a test, not a status

A performance-based exam grades behavior. After each change run the request that proves it: `curl` from a Pod, a name lookup from a Pod, a Hubble flow, an access log line. A resource showing `Accepted` is not the same as traffic flowing.

## Distinctions to own

- **Service port versus targetPort versus nodePort.**
- **iptables, ipvs and nftables modes**, and kube-proxy replacement.
- **Pod CIDR, Service CIDR and Node CIDR** must not overlap.
- **Isolated versus non-isolated Pods**, and that policies are additive.
- **Terminate versus Passthrough** TLS on a Gateway listener.
- **PeerAuthentication (who connects) versus AuthorizationPolicy (what they may do).**
- **Primary-remote versus multi-primary** and **single versus multi-network** in Istio.

## Do not over-study

You do not need to master every plugin. Know the Kubernetes primitives well, then be comfortable finding the missing piece in documentation under time pressure.
