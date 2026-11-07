---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 8 min
---

# CKNE High-Yield Scenarios

Each scenario is shaped like a performance-based task: a symptom, the steps you would take, and the check that proves the fix.

---

## Scenario 1: New Pods have no IP

**Scenario**: Pods on a freshly joined node stay in ContainerCreating and show no IP.

**Solution Pattern**:
- Check the node is Ready and the CNI agent Pod on that node is running
- Look at the CNI config directory on the node (commonly `/etc/cni/net.d`) and the binaries (`/opt/cni/bin`); the container runtime loads CNI, not the kubelet
- Check IPAM: has the node a Pod CIDR, or is the plugin out of addresses?
- Read the Pod events for the CNI error text

**Verify**: a test Pod gets an IP and reaches another Pod.

**Key Takeaway**: runtime plus CNI config plus IPAM.

---

## Scenario 2: Name does not resolve, IP works

**Scenario**: `curl http://backend` fails from a Pod, but `curl http://10.x.x.x` to the Service IP works.

**Solution Pattern**:
- Check the Pod's `/etc/resolv.conf` (nameserver, search path, `ndots:5`)
- Check CoreDNS Pods and logs, and the `coredns` ConfigMap Corefile
- Remember short names stay in the Pod's namespace: use `backend.other-namespace`
- If a new egress NetworkPolicy exists, allow UDP and TCP 53 to CoreDNS

**Verify**: `nslookup backend` from the Pod resolves; the app connects.

**Key Takeaway**: resolve the name before blaming the Service.

---

## Scenario 3: A Service has no endpoints

**Scenario**: `kubectl get svc` looks fine, but connections are refused and the EndpointSlice is empty.

**Solution Pattern**:
- Compare the Service `selector` with the Pod labels
- Check Pod readiness; a Pod that is not ready is not an endpoint
- Check `targetPort` against the container port (a named port must match the Pod's port name)
- For an external backend, a Service without a selector needs a hand-written EndpointSlice with the `kubernetes.io/service-name` label

**Verify**: the EndpointSlice lists ready addresses and the Service answers.

**Key Takeaway**: selector, readiness, port.

---

## Scenario 4: Route is created but never serves traffic

**Scenario**: An HTTPRoute in `team-a` points at a Gateway in `infra`, but is not accepted.

**Solution Pattern**:
- A Gateway accepts routes only from its own namespace by default; set `allowedRoutes.namespaces` on the listener
- Check `parentRefs` names the Gateway (and namespace) and the listener's hostname matches the route's `hostnames`
- Check the GatewayClass controller is running

**Verify**: the route status shows it accepted; a request returns the backend response.

**Key Takeaway**: allowedRoutes is the usual cross-namespace gate.

---

## Scenario 5: Lock down a namespace without breaking it

**Scenario**: Apply a default deny to `prod`, then allow only the frontend to reach the API on port 8080.

**Solution Pattern**:
- Default-deny ingress (and egress if required) with `podSelector: {}`
- Allow DNS egress to CoreDNS if egress is denied
- Add an ingress policy on the API Pods with a `from.podSelector` for the frontend and port 8080
- Remember policies are additive and need a CNI that enforces them

**Verify**: frontend to API works; another Pod is blocked (Hubble `--verdict DROPPED` shows the block).

**Key Takeaway**: deny first, add precise allows, test both directions.

---

## Scenario 6: Funnel outbound traffic through one place

**Scenario**: Security wants all external HTTP calls to leave through a single, auditable gateway.

**Solution Pattern**:
- Istio: a ServiceEntry (`resolution: DNS`), an egress Gateway, a DestinationRule subset and a VirtualService with two routes (mesh to gateway, gateway to external host)
- Add NetworkPolicies so Pods can only egress to the gateway, DNS and the control plane, because Istio cannot enforce gateway-only egress alone
- Confirm with the egress gateway's `istio-proxy` logs

**Verify**: the external host appears in the gateway log; direct egress from an app Pod is blocked.

**Key Takeaway**: mesh routing plus NetworkPolicy equals enforcement.

---

## Scenario 7: Encrypt node-to-node and require identity

**Scenario**: Compliance requires encryption in transit between nodes and that only the `frontend` ServiceAccount can call `payments`.

**Solution Pattern**:
- CNI encryption (for example Cilium WireGuard) covers node and Pod traffic; strict mode refuses unencrypted traffic that should be encrypted (ingress strict mode needs WireGuard, not IPsec)
- Mesh: STRICT PeerAuthentication so identities exist, then an AuthorizationPolicy `ALLOW` with the frontend principal on `payments`
- Remember one ALLOW policy flips the workload to deny unless matched

**Verify**: a call from another ServiceAccount is rejected; Hubble `--encrypted` shows encrypted flows.

**Key Takeaway**: encryption protects the wire, identity enables authorization.
