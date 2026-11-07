---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 10 min
---

# 03 - Advanced Traffic Management

**Domain 3: Advanced Traffic Management (20%)**

Curriculum competencies: optimizing LLM traffic; implementing routing to expose networks; configuring egress gateways for cluster exit traffic; implementing cross-cluster service discovery and load balancing.

This is the least standardized domain, and the Linux Foundation page does not list tools for it (it links to "What tools are featured in the CKNE exam?" without the answer being on the page). The sections below use the documented implementations most closely tied to each competency: the Gateway API Inference Extension, Cilium's BGP Control Plane, Istio's egress gateway and multicluster models, and Cilium Cluster Mesh. Expect the exam to use whatever the environment installs.

Nothing here was run: no cluster was available. YAML was syntax-checked only.

---

## Optimizing LLM traffic

Model-serving traffic is different from web traffic: requests are long, expensive and uneven, so round-robin load balancing wastes GPU capacity. The Gateway API Inference Extension is the Kubernetes project aimed at this. From its documentation:

- It is described as an official Kubernetes project (driven by WG-Serving and SIG-Network) for self-hosting generative AI models. It extends gateways that support both Envoy's external processing protocol and Gateway API into **inference gateways** (the page names Envoy Gateway, kgateway and GKE Gateway as examples), with a current focus on large language models.
- An **InferencePool** is a set of endpoints running a model server framework. Gateway routing can target an InferencePool or a Service.
- The **Endpoint Picker (EPP)** is the inference router component. It fetches metrics from the pool's endpoints and tells the gateway which endpoint should get each request. The project ships a lightweight EPP for conformance testing and recommends implementing your own or using an existing one for production.
- **Model-aware routing:** gateways can route by model name instead of only by request path, which works with OpenAI-style APIs and extends to LoRA fine-tuned models. The page also mentions serving priority and incremental model rollouts through traffic splitting.
- The page cites prefix cache status and LoRA adapter availability as example metrics that inform routing.

The page contains no YAML and does not give resource schemas, so read the InferencePool API reference in the exam environment. What you can reason about without it: weighted splitting (previous note) handles gradual model rollouts, and header or model-name matching handles model-aware routing.

**[📖 Gateway API Inference Extension](https://gateway-api-inference-extension.sigs.k8s.io/)** - InferencePool, endpoint picker, model-aware routing

---

## Routing to expose networks

"Implementing routing to expose networks" means making Pod and Service address ranges reachable from outside the cluster, which a datacenter or hybrid network needs when Pod IPs must be routed instead of hidden behind NAT. The documented building block in this repo's tool set is **BGP**.

The Cilium BGP Control Plane documentation says it lets Cilium advertise routes to connected routers using BGP, "which makes Pod networks and/or Services reachable from outside the cluster." Details:

- It does **not** program the datapath, so it is not used for reachability inside the cluster.
- It supports IPv4, IPv6 and dual-stack, advertising only the address family Cilium is configured for.
- Resources: `CiliumBGPClusterConfig`, `CiliumBGPPeerConfig`, `CiliumBGPAdvertisement` and `CiliumBGPNodeConfigOverride`.
- Enable it with the Helm value `bgpControlPlane.enabled=true` and restart the Cilium DaemonSet:

```bash
helm upgrade cilium cilium/cilium --version 1.20.4 \
   --namespace kube-system \
   --reuse-values \
   --set bgpControlPlane.enabled=true
kubectl -n kube-system rollout restart ds/cilium
```

The page did not include a worked cluster configuration, so the peer and advertisement manifests come from the sample configurations section in the exam documentation. For the other half of exposing a network, Services of type `LoadBalancer` need a load balancer from the cloud provider or an on-premises implementation (Service page).

**[📖 Cilium BGP Control Plane](https://docs.cilium.io/en/stable/network/bgp-control-plane/bgp-control-plane/)** - resources and enabling

---

## Egress gateways for cluster exit traffic

An **egress gateway** funnels traffic leaving the mesh through a dedicated, controlled proxy, so external firewalls can allow one known source and teams can audit exits. The Istio egress gateway task shows the pieces:

1. **ServiceEntry** registers the external host. The page warns: "If the resolution is `NONE`, the gateway will direct the traffic to itself in an infinite loop", so use `resolution: DNS`.
2. **Gateway** with the selector `istio: egressgateway` listens for the host.
3. **DestinationRule** defines a subset on the gateway's Service.
4. **VirtualService** has two rules: traffic from the mesh goes to the gateway, and traffic from the gateway goes to the external host.

```yaml
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata:
  name: cnn
spec:
  hosts:
  - edition.cnn.com
  ports:
  - number: 80
    name: http-port
    protocol: HTTP
  resolution: DNS
---
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: istio-egressgateway
spec:
  selector:
    istio: egressgateway
  servers:
  - port: {number: 80, name: http, protocol: HTTP}
    hosts:
    - edition.cnn.com
---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: egressgateway-for-cnn
spec:
  host: istio-egressgateway.istio-system.svc.cluster.local
  subsets:
  - name: cnn
```

- HTTPS uses a `TLS` port 443 ServiceEntry, a Gateway with `tls.mode: PASSTHROUGH` and a VirtualService `tls` block matching `sniHosts`.
- The egress gateway Pod has the label `istio=egressgateway` in `istio-system`; the `demo` profile enables it.
- **Verify** with the gateway logs: `kubectl logs -l istio=egressgateway -c istio-proxy -n istio-system | tail`. The upstream host in a log line confirms the request passed through the gateway.
- **Bypass prevention:** Istio cannot enforce gateway-only egress by itself, per the page. Combine it with Kubernetes NetworkPolicies that allow egress only to the control plane, the gateway and DNS.
- A Gateway API alternative exists (a `Gateway` with `gatewayClassName: istio` plus `HTTPRoute` or `TLSRoute`); the page says it needs experimental CRDs and `PILOT_ENABLE_ALPHA_GATEWAY_API=true`.

**[📖 Istio egress gateway](https://istio.io/latest/docs/tasks/traffic-management/egress/egress-gateway/)** - ServiceEntry, Gateway, VirtualService, verification

---

## Cross-cluster service discovery and load balancing

Two documented models.

### Istio multicluster

- **Single network versus multi-network:** on one network workloads reach each other directly and IPs must not overlap; on multiple networks they reach each other only through Istio gateways, which allows overlapping IP ranges.
- **Primary-remote versus multi-primary:** a primary cluster runs its own control plane; remote clusters have none and get configuration from a primary. In multi-primary setups each primary gets configuration from its own API server, so config changes must be applied to each.
- **Discovery:** "each control plane must observe endpoints from the API Server in every cluster." An administrator generates a **remote secret** (it contains credentials for the cluster's API server) and deploys it to each primary cluster.
- **Load balancing:** by default Istio spreads requests evenly across endpoints in each cluster; locality load balancing keeps traffic in the same zone or region. To prevent cross-cluster balancing, do not exchange remote secrets.
- Cross-network traffic works only for workloads with an Istio proxy. Each consuming cluster needs a DNS entry for the service (a Kubernetes Service or a ServiceEntry plus DNS configuration).

**[📖 Istio deployment models](https://istio.io/latest/docs/ops/deployment/deployment-models/)** - multicluster models and discovery

### Cilium Cluster Mesh

Cluster Mesh connects clusters at the CNI level. Setup requirements from the Cilium docs:

- A **unique cluster name** (at most 32 characters, lowercase alphanumeric with inner dashes) and a **cluster ID from 1 to 255**, set at install with Helm values `cluster.name` and `cluster.id`.
- **Non-overlapping PodCIDRs** across clusters, and node connectivity over their InternalIPs (peering or VPN).
- The same datapath mode, Cilium versions within one minor release of each other, and firewall rules that permit inter-cluster traffic.

```bash
cilium clustermesh enable --context $CLUSTER1
cilium clustermesh enable --context $CLUSTER2
cilium clustermesh connect --context $CLUSTER1 --destination-context $CLUSTER2
cilium clustermesh status --context $CLUSTER1 --wait
```

Run `connect` once; the connection is established in both directions. The setup page links to a separate Load-balancing and Service Discovery page for how a Service becomes global, so read that page for the annotation.

**[📖 Cluster Mesh setup](https://docs.cilium.io/en/stable/network/clustermesh/setup/index.html)** - requirements and commands

---

## Key terms

- **Inference gateway** - a gateway extended to route model-serving traffic based on model and endpoint metrics.
- **InferencePool** - a set of endpoints running a model server framework, targeted by gateway routing.
- **Endpoint Picker (EPP)** - the component that chooses which model endpoint gets each request.
- **BGP** - the Border Gateway Protocol, used to advertise Pod and Service routes to external routers.
- **Egress gateway** - a dedicated proxy through which traffic leaves the mesh or cluster.
- **ServiceEntry** - an Istio resource that registers an external service in the mesh.
- **Remote secret** - an Istio credential that lets a control plane read another cluster's endpoints.
- **Multi-primary** - an Istio multicluster model where each cluster has its own control plane.
- **Locality load balancing** - preferring endpoints close to the caller by zone or region.
- **Cluster Mesh** - Cilium's feature for connecting multiple clusters.
