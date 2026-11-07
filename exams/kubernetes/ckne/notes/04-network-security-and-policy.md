---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 13 min
---

# 04 - Network Security and Policy

**Domain 4: Network Security and Policy (25%)**

Curriculum competencies: securing traffic with Network Policies; implementing node and Pod level encryption; managing TLS certificates for Gateway API; implementing Pod-level authentication and authorization.

Joint largest domain. YAML below was syntax-checked only and nothing was applied; no cluster was available.

---

## Network Policies

NetworkPolicies control traffic at the IP address or port level (OSI layers 3 and 4) for TCP, UDP and SCTP, for connections where a Pod is at one or both ends. From the Kubernetes docs:

- **They need support from the network plugin.** "Creating a NetworkPolicy resource without a controller that implements it will have no effect." Check that the CNI enforces policy before debugging YAML.
- A Pod is **non-isolated** for a direction by default (all traffic allowed). It becomes **isolated** for a direction when any policy selects it and lists that direction in `policyTypes`.
- **Policies are additive:** "Network policies do not conflict; they are additive." The allowed set is the union of all applicable policies, so order does not matter.
- A connection needs **both** the source Pod's egress policy and the destination Pod's ingress policy to allow it. Reply traffic for an allowed connection is implicitly allowed.
- Traffic to and from the Pod's own node is always allowed (for ingress isolation).
- Peers are identified by `podSelector`, `namespaceSelector` or `ipBlock`. An empty `podSelector` selects all Pods in the namespace.

The page's example policy:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
        except:
        - 172.17.1.0/24
    - namespaceSelector:
        matchLabels:
          project: myproject
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 5978
```

With no policies in a namespace, all ingress and egress is allowed. The page's default-deny-ingress example selects all Pods and allows no ingress:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

A common mistake: an egress default-deny blocks DNS too. If Pods can no longer resolve names after you add it, allow egress to CoreDNS on port 53 (UDP and TCP). Another: `from` entries listed as **separate items** are ORed, while a `namespaceSelector` and `podSelector` inside **one item** are ANDed (the NetworkPolicy page: a single `from` entry with both selectors selects Pods within namespaces; the example policy lists three separate peers under one `from`). Read selector structure carefully when you debug.

`endPort` (stable since Kubernetes 1.25) targets a port range and must be equal to or greater than `port`. FQDN rules and AdminNetworkPolicy were not checked; use the full page if a task needs them. The DNS-blocking caveat above is general practice, not a page quote.

**[📖 Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)** - isolation, additive rules, selectors

---

## Node and Pod level encryption

Traffic between Pods and nodes crosses the underlying network unencrypted unless something encrypts it. Two documented approaches.

### CNI encryption (Cilium)

Cilium can transparently encrypt host traffic and traffic between endpoints using **IPsec**, **WireGuard**, or **ztunnel (Beta)**. The encryption page's settings and limits:

- `encryption.strictMode.egress.enabled` and `encryption.strictMode.egress.cidr` enforce that traffic leaving a node for the set CIDR is always encrypted. The CIDR must be IPv4.
- `encryption.strictMode.ingress.enabled` drops cluster-internal ingress that did not arrive through the WireGuard tunnel. It works with tunnel and native routing, **but not IPsec**.
- Known issue: traffic to remote endpoints Cilium has not learned about yet may be sent unencrypted; use egress policies for outside-cluster traffic or enable egress strict mode.
- Limits: egress strict mode does not protect IPv6; ingress strict mode does not protect node-to-node WireGuard traffic, can be bypassed through interfaces Cilium does not manage, and is not supported when chaining Cilium on another CNI.

The page excerpt did not show the base Helm values to turn encryption on or the verification command, so use the encryption section of the Cilium documentation and `cilium status`. You can check whether flows are encrypted with `hubble observe --encrypted` or `--unencrypted` (Hubble CLI page).

**[📖 Cilium transparent encryption](https://docs.cilium.io/en/stable/security/network/encryption/)** - IPsec, WireGuard, strict mode

### Mesh mTLS

A mesh encrypts at the Pod (workload) level using mTLS: Istio `PeerAuthentication` modes `STRICT`, `PERMISSIVE`, `DISABLE`, and Linkerd's on-by-default mTLS between meshed pods with 24-hour proxy certificates. Details are in [CNPE note 05](../../cnpe/notes/05-security-and-policy-enforcement.md) and the [ICA guide](../../ica/).

Choosing between them: CNI encryption protects all Pod and node traffic regardless of application; mesh mTLS also gives workload **identity**, which you need for authorization (below).

---

## TLS certificates for Gateway API

TLS on a Gateway is configured on its **listeners**. From the Gateway API TLS guide:

- **Terminate:** the Gateway ends the TLS session and uses the certificate in `certificateRefs`. Supported with HTTPS (HTTPRoute), GRPC (GRPCRoute) and TLS (TLSRoute, Extended support).
- **Passthrough:** the encrypted session passes through unchanged, so listener TLS settings have no effect; used with the TLS protocol and TLSRoute.
- **Hostname:** each listener's `hostname` sets which domains its TLS settings apply to. A specific hostname takes priority over a wildcard, so `foo.example.com` gets its own certificate while `*.example.com` covers the rest.
- **Certificates:** `certificateRefs` point to Kubernetes Secrets (the page does not state which Secret type is required).
- **Cross-namespace references:** a Gateway can reference a Secret in another namespace only if a **ReferenceGrant** in the Secret's namespace allows it. Without the grant the reference is invalid.

```yaml
listeners:
- protocol: HTTPS # Other possible value is `TLS`
  port: 443
  tls:
    mode: Terminate # If protocol is `TLS`, `Passthrough` is another possible mode
    certificateRefs:
    - kind: Secret
      group: ""
      name: default-cert
```

**Upstream TLS (Gateway to backend):** a **BackendTLSPolicy** attached to a Service through `targetRefs` sets `hostname` (the SNI the Gateway uses, which must match the backend's certificate) and either `caCertificateRefs` (custom CAs) or `wellKnownCACertificates: "System"`. It does not allow cross-namespace certificate references or wildcard hostnames. For Gateway-side client certificates for backend mTLS use `tls.backend.clientCertificateRef` on the Gateway.

Troubleshooting order for "HTTPS does not work": is the listener `Programmed`; does the Secret exist in the namespace the `certificateRefs` point at (or is there a ReferenceGrant); does the listener `hostname` match the requested host; does a more specific hostname listener override the wildcard.

How certificates get into the Secret (a manual `kubectl create secret tls` or an issuer such as cert-manager) was not covered by the pages fetched for this guide; use what the exam environment provides.

**[📖 Gateway API TLS](https://gateway-api.sigs.k8s.io/guides/tls/)** - listeners, Terminate and Passthrough, ReferenceGrant, BackendTLSPolicy

---

## Pod-level authentication and authorization

**Authentication** answers "who is calling": in a mesh, the workload identity proven by mTLS (an Istio principal looks like `cluster.local/ns/default/sa/sleep`; Linkerd uses the Pod's ServiceAccount). **Authorization** answers "may they": Istio's `AuthorizationPolicy`.

From the AuthorizationPolicy reference:

- Actions: `ALLOW` (the default), `DENY`, `AUDIT` and `CUSTOM`.
- A rule matches when at least one source, one operation and all conditions match; an empty rule matches everything.
- `from.source` fields: `principals` and `namespaces` (both **require mTLS**) and `ipBlocks`. `to.operation` fields: `methods`, `paths`, `ports`.
- **Evaluation order:** CUSTOM first (a deny rejects), then DENY policies (reject), then: if no ALLOW policies apply to the workload, the request is allowed; if any ALLOW policy matches, allowed; otherwise denied.
- With no ALLOW policy on a workload, requests are allowed. An `ALLOW` policy with no rules matches nothing, so it denies all traffic. An empty `spec: {}` denies all requests in the namespace.
- A policy in the root namespace applies mesh-wide; a `selector` narrows it to workloads.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-sleep
  namespace: foo
spec:
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/sleep"]
```

Common task pattern: turn on STRICT mTLS (so identities exist), add a namespace-wide deny-all, then add ALLOW policies per caller and path. Because of the evaluation order above, one ALLOW policy flips a workload from "allow all" to "deny unless matched", so add the full set before enforcing.

Layering to remember: NetworkPolicy is L3 and L4 by IP and label; AuthorizationPolicy can reason about identity, methods and paths. Use both.

**[📖 Istio AuthorizationPolicy](https://istio.io/latest/docs/reference/config/security/authorization-policy/)** - actions, rules, evaluation order

**[📖 Istio PeerAuthentication](https://istio.io/latest/docs/reference/config/security/peer_authentication/)** - mTLS modes and scopes

---

## Key terms

- **NetworkPolicy** - a Kubernetes resource that allows traffic to and from selected Pods at layers 3 and 4, enforced by the network plugin.
- **Isolated (Pod)** - a Pod selected by a policy for a direction, so only explicitly allowed traffic is permitted.
- **ipBlock** - a NetworkPolicy peer defined by a CIDR range with optional exceptions.
- **WireGuard / IPsec** - encryption protocols Cilium can use for transparent node and Pod traffic encryption.
- **Strict mode (Cilium)** - a setting that drops or refuses unencrypted traffic that should have been encrypted.
- **Listener (Gateway)** - the Gateway entry that defines protocol, port, hostname and TLS settings.
- **Terminate / Passthrough** - Gateway TLS modes: end TLS at the Gateway, or pass encrypted traffic through unchanged.
- **ReferenceGrant** - a resource in a namespace that allows references from other namespaces, for example to a certificate Secret.
- **BackendTLSPolicy** - a Gateway API resource that configures TLS from the Gateway to a backend Service.
- **Principal (Istio)** - the identity of a workload, derived from its ServiceAccount, used in AuthorizationPolicy.
- **AuthorizationPolicy** - an Istio resource that allows or denies requests based on identity, operation and conditions.
