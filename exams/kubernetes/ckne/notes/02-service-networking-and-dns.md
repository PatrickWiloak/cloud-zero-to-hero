---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 15 min
---

# 02 - Service Networking and DNS

**Domain 2: Service Networking and DNS (25%)**

Curriculum competencies: configuring L4 Services; understanding kube-proxy and CNI alternatives; customizing CoreDNS for Services; troubleshooting Service network traffic; configuring Pod endpoint availability; managing traffic with the Gateway API (Gateway, HTTPRoutes).

Joint largest domain with network security. YAML below was syntax-checked only; nothing was applied.

---

## L4 Services

A Service gives a changing set of Pods a stable endpoint. From the Service page: it defines "a logical set of endpoints (usually these endpoints are Pods) along with a policy about how to make those pods accessible." The Service controller keeps matching Pods and updates the Service's **EndpointSlices**.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

- `port` is what clients use; `targetPort` is the Pod port (defaults to the same as `port`; it can be a **named** Pod port).
- The default type is **ClusterIP**: a virtual IP allocated by the API server.
- **NodePort:** the control plane allocates a port from the range set by `--service-node-port-range` (default 30000-32767; static band 30000-30085, dynamic band 30086-32767). Every node listens on that port and forwards to ready endpoints. You can request a port with `nodePort: 30007`; if unavailable the API call fails.
- **LoadBalancer:** "Kubernetes does not directly offer a load balancing component; you must provide one, or you can integrate your Kubernetes cluster with a cloud provider."
- **ExternalName:** maps to a `CNAME` record for `externalName`; "No proxying of any kind is set up."
- **Headless:** `.spec.clusterIP: None` means no IP is assigned; DNS returns the Pod IPs (see DNS below).

### Services without selectors

For an external database or a Service in another cluster, create the Service with no `selector` and add the EndpointSlice yourself:

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: my-service-1
  labels:
    kubernetes.io/service-name: my-service
addressType: IPv4
ports:
  - name: http
    appProtocol: http
    protocol: TCP
    port: 9376
endpoints:
  - addresses:
      - "10.4.5.6"
  - addresses:
      - "10.1.2.3"
```

The `kubernetes.io/service-name` label links the slice to the Service. Endpoint IPs must not be loopback or link-local, nor the cluster IPs of other Services. `kubectl port-forward service/<name>` fails for selector-less Services because the API server does not proxy to endpoints not mapped to Pods.

**[📖 Service](https://kubernetes.io/docs/concepts/services-networking/service/)** - types, ports, selector-less Services

---

## kube-proxy and CNI alternatives

kube-proxy on each node programs the rules that make Service IPs work. From the virtual IPs page:

- Linux modes: `iptables`, `ipvs` and `nftables`. Windows uses only `kernelspace`.
- If no mode is chosen, kube-proxy uses the recommended default. The page says that in Kubernetes 1.37 this is `iptables`, but "a future version of Kubernetes will change the default to `nftables`." **Set the mode explicitly** in the config file (`mode`) or with `--proxy-mode` so an upgrade does not change it.
- In iptables mode, "for each endpoint, it installs iptables rules which, by default, select a backend Pod at random." Packets are redirected with destination NAT without rewriting the client IP; traffic through a NodePort or load balancer does alter the client IP.
- Scale: kube-proxy creates "a few iptables rules for every Service, and a few iptables rules for each endpoint IP address," so very large clusters can end up with tens of thousands of rules and slow updates. Sync tuning lives under the `iptables` section (`minSyncPeriod`, `syncPeriod`).
- With NodePorts, `iptables` mode serves all node IPs by default while `nftables` mode serves only the primary IP; `--nodeport-addresses` or `nodePortAddresses` changes it.

```yaml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "nftables"   # or "iptables", "ipvs"
```

*`KubeProxyConfiguration` (`kubeproxy.config.k8s.io/v1alpha1`) is listed in the kube-proxy configuration reference; the `mode` value matches the proxy modes on the virtual IPs page.*

**CNI alternatives** means CNIs that implement Service load balancing themselves instead of kube-proxy (Cilium is the example covered in this repo's [CCA guide](../../cca/)). The practical consequence: when kube-proxy is replaced, `iptables` inspection no longer shows Service rules, and troubleshooting uses the CNI's own tooling. First find out what is running: check for a kube-proxy DaemonSet and its ConfigMap in `kube-system`.

**[📖 Virtual IPs and Service proxies](https://kubernetes.io/docs/reference/networking/virtual-ips/)** - proxy modes, defaults, caveats

---

## Customizing CoreDNS

CoreDNS is the cluster DNS server. Its configuration is a ConfigMap named `coredns` in `kube-system`, under the `Corefile` key. The default from the docs:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
            lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
            ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```

What each plugin does:

| Plugin | Function |
|---|---|
| `kubernetes` | Answers Service and Pod names under `cluster.local`; `ttl` sets response TTL (default 5s, range 0 to 3600s) |
| `forward` | Sends non-cluster queries upstream (here to the node's `/etc/resolv.conf`) |
| `cache` | Frontend cache (30s) |
| `loop` | Detects forwarding loops and halts CoreDNS |
| `reload` | Reloads a changed Corefile automatically |
| `health`, `ready` | Health on `:8080/health`, readiness on port 8181 |
| `prometheus` | Metrics on `:9153/metrics` |
| `loadbalance` | Randomizes the order of A, AAAA and MX records |

**Stub domain** (send one suffix to a different resolver) by adding a server block:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . 172.16.0.1
        cache 30
        loop
        reload
        loadbalance
    }
    consul.local:53 {
        errors
        cache 30
        forward . 10.150.0.1
    }
```

`forward . 172.16.0.1` forces all non-cluster lookups to one upstream. Changes reload automatically through the `reload` plugin; the docs say to **allow up to two minutes**. Do not restart CoreDNS to apply a Corefile edit unless the reload does not happen.

**[📖 Customizing DNS service](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/)** - Corefile, stub domains, upstreams

### DNS names and the Pod resolver

From the DNS for Services and Pods page:

- A Service gets the A/AAAA name `my-svc.my-namespace.svc.cluster-domain.example`. A **headless** Service uses the same name but resolves to the IPs of all selected Pods.
- SRV records exist for named ports: `_port-name._port-protocol.my-svc.my-namespace.svc.cluster-domain.example`.
- Pod `/etc/resolv.conf` is set by the kubelet:

```text
nameserver 10.32.0.10
search <namespace>.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

- A query without a namespace stays in the Pod's own namespace. From `test`, `data` finds nothing in `prod`, but `data.prod` works.
- A Pod gets its own DNS record only when it has `hostname` and `subdomain` set and a headless Service of the same name as the subdomain exists. A Pod must be ready to have a record, unless the Service sets `publishNotReadyAddresses=True`.
- The kubelet `--resolv-conf` flag controls whether Pods inherit DNS config from the node.

**[📖 DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)** - record formats, search path, Pod records

---

## Pod endpoint availability

Which Pods receive Service traffic is decided by EndpointSlices. A Pod that is not ready is not an endpoint, and its DNS record is withheld (unless `publishNotReadyAddresses=True`). Readiness is therefore how you control endpoint availability.

From the probes task page (which shows `tcpSocket` and gRPC probes, `initialDelaySeconds`, `periodSeconds` and startup probes) and general practice:

- A failing **readiness probe** marks the Pod not ready and removes its IP from Service endpoints without restarting the container.
- Probe types: `httpGet`, `tcpSocket`, `exec` and `grpc`; tuning fields include `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `successThreshold` and `failureThreshold`.
- A **startup probe** holds off liveness and readiness checks for slow-starting containers.

For a task like "traffic reaches Pods that are still starting," add or fix the readiness probe. For "a Service has no endpoints," compare the Service `selector` with the Pod labels and check readiness.

---

## Troubleshooting Service network traffic

Work from the client outward and use the symptom to pick the layer.

| Symptom | Likely layer | Checks |
|---|---|---|
| `connection refused` to the Service IP | No ready endpoints, wrong `targetPort` | `kubectl get endpointslices -l kubernetes.io/service-name=<svc>`; compare selector, labels and ports |
| Name does not resolve, IP works | DNS | CoreDNS Pods and logs, the `coredns` ConfigMap, the Pod's `resolv.conf`, namespace in the name |
| Short name works in one namespace, not another | Search path | Use `svc.namespace` or the FQDN |
| ClusterIP times out, Pod IP works | kube-proxy or CNI replacement | Which proxy mode, rules present, kube-proxy Pod healthy |
| NodePort works on some nodes | `nodePortAddresses`, firewall, externalTrafficPolicy | kube-proxy config and cloud firewall |
| Only some Pods answer | Readiness or uneven endpoints | Pod readiness, EndpointSlice contents |
| Works only without a NetworkPolicy | Policy | Domain 4 |

Always ask which of these a given error rules out, then test the next layer, rather than changing things at random.

---

## Gateway API: Gateway and HTTPRoute

Gateway API is a family of resources for routing, installed as an add-on (it is built on custom resources, so it must be installed). All stable kinds use `apiVersion: gateway.networking.k8s.io/v1`. The four stable kinds are **GatewayClass**, **Gateway**, **HTTPRoute** and **GRPCRoute**.

Roles map to owners:

| Resource | Typical owner | What it is |
|---|---|---|
| GatewayClass | Infrastructure provider | A set of gateways with common configuration, managed by a controller (`controllerName`) |
| Gateway | Cluster operator | An instance of traffic-handling infrastructure, with `listeners` |
| HTTPRoute | Application developer | HTTP routing rules from a Gateway listener to backends, usually Services |

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: example-gateway
  namespace: example-namespace
spec:
  gatewayClassName: example-class
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    hostname: "www.example.com"
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: example-httproute
spec:
  parentRefs:
  - name: example-gateway
  hostnames:
  - "www.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /login
    backendRefs:
    - name: example-svc
      port: 8080
```

- A Gateway references exactly one GatewayClass. `parentRefs` attaches a route to a Gateway.
- **By default a Gateway accepts Routes only from its own namespace**; configure `allowedRoutes` for cross-namespace routes. That is the usual reason a route shows as not accepted.
- If `addresses` is unspecified, the implementation assigns an address.
- Gateway API makes header matching and traffic weighting first-class fields, where Ingress needed vendor annotations.

### Weighted routing

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: simple-split
spec:
  rules:
  - backendRefs:
    - name: foo-v1
      port: 8080
      weight: 90
    - name: foo-v2
      port: 8080
      weight: 10
```

`weight` is "a proportional split of traffic (rather than percentage)": each backend's share is its weight divided by the total. It is optional and defaults to 1; a rule with one backend sends 100 percent to it. A header-match rule (for example `traffic=test` to `foo-v2`) is more specific, so test traffic reaches the new version before any production split.

**[📖 Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/)** - resource model, roles, examples

**[📖 Traffic splitting](https://gateway-api.sigs.k8s.io/guides/traffic-splitting/)** - weights and header matches

---

## Key terms

- **Service** - a stable endpoint and policy for reaching a set of Pods.
- **EndpointSlice** - the object listing the ready backend addresses for a Service.
- **ClusterIP** - the default Service type, a virtual IP inside the cluster.
- **NodePort** - a Service type that opens a port on every node.
- **Headless Service** - a Service with `clusterIP: None`, resolved by DNS to Pod IPs.
- **kube-proxy** - the node component that programs rules to make Service IPs work.
- **nftables mode** - a kube-proxy mode that uses nftables rules instead of iptables.
- **CoreDNS** - the cluster DNS server, configured by the `coredns` ConfigMap.
- **Corefile** - CoreDNS's configuration, a list of server blocks and plugins.
- **Stub domain** - a DNS suffix forwarded to a specific resolver.
- **ndots** - the resolver option that decides how many dots make a name "absolute" before the search path is tried.
- **Readiness probe** - a check that decides whether a Pod receives Service traffic.
- **GatewayClass / Gateway / HTTPRoute** - the Gateway API resources for class, entry point and routing rules.
- **parentRefs** - the field that attaches a route to a Gateway.
