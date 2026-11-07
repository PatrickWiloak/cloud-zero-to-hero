# Certified Kubernetes Network Engineer (CKNE) - Practice Questions

30 original questions for CKNE prep, spread across the domains in proportion to their weights.

> **Cert page:** [exams/kubernetes/ckne/](../../exams/kubernetes/ckne/)

---

### Question 1
**Scenario:** Who assigns IP addresses to Pods, Services and Nodes in a Kubernetes cluster?

A. All three by the kube-controller-manager
B. Pods by the kubelet from the node CIDR, Services by CoreDNS, and Nodes by kube-proxy once it registers them with the API server
C. All three by the container runtime
D. Pods by the network plugin, Services by the kube-apiserver, Nodes by the kubelet or cloud controller

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The cluster networking page lists those three sources. The ranges must not overlap.
</details>

---

### Question 2
**Scenario:** Which component is responsible for loading CNI plugins in modern Kubernetes?

A. The kubelet through the network-plugin flag
B. kube-proxy
C. The container runtime
D. The kube-apiserver

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The kubelet flags cni-bin-dir and network-plugin were removed in Kubernetes 1.24. The container runtime is configured to load the CNI plugins.
</details>

---

### Question 3
**Scenario:** A CNI configuration must provide which interface in every pod sandbox?

A. A bridge named cni0
B. Loopback (lo)
C. A VLAN interface
D. A tunnel named tun0

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The runtime must provide a loopback interface in each sandbox; the CNI loopback plugin can be reused.
</details>

---

### Question 4
**Scenario:** Which CNI plugin supports hostPort when you add portMappings to the capabilities?

A. bandwidth
B. portmap
C. macvlan
D. host-local

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The official portmap plugin implements hostPort. bandwidth is for experimental traffic shaping and host-local is an IPAM plugin.
</details>

---

### Question 5
**Scenario:** Within the 10.96.0.0/16 Service range, how are static and dynamic ClusterIP bands arranged?

A. A static band of 256 addresses at the start; dynamic allocation uses the upper band first
B. A single band across the whole /16; all allocations are dynamic and picked at random by the allocator
C. The upper half is static and the lower half dynamic
D. Static addresses are drawn only from the last /24

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The band size is min(max(16, cidrSize/16), 256), giving 256 for a /16, and dynamic allocation uses the upper band first.
</details>

---

### Question 6
**Scenario:** Which annotation requests an additional network interface for a Pod when Multus is installed?

A. kubernetes.io/extra-network
B. cni.projectcalico.org/extra
C. network.k8s.io/attach
D. k8s.v1.cni.cncf.io/networks

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Pods request secondary networks with k8s.v1.cni.cncf.io/networks, listing NetworkAttachmentDefinition names, optionally with @ifname.
</details>

---

### Question 7
**Scenario:** A Pod with a Multus annotation macvlan-conf-1@macvlan1 is running. What would ip -d address show?

A. Only eth0, because secondary networks are hidden from ip commands inside the Pod network namespace
B. An interface named net0 only
C. eth0 for the default network plus an interface named macvlan1
D. A bridge named macvlan1 on the node only

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The @macvlan1 suffix names the secondary interface; without a suffix the interface is numbered, such as net2.
</details>

---

### Question 8
**Scenario:** A Service of type ClusterIP has targetPort omitted. What is used?

A. Port 80
B. The first containerPort of the first Pod
C. The same value as port
D. A random port in 30000-32767

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** If targetPort is omitted it defaults to the same value as port.
</details>

---

### Question 9
**Scenario:** Which NodePort statement is correct?

A. NodePorts are allocated from 1024-29999, which is the range the API server reserves for Services by default
B. The port comes from --service-node-port-range (default 30000-32767) and every node listens on it
C. Only the node running the Pods listens on the NodePort
D. NodePorts bypass kube-proxy entirely

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The control plane allocates from the configured range and every node forwards the port to ready endpoints.
</details>

---

### Question 10
**Scenario:** How do you point a Service at an external database IP with no Pods?

A. Create the Service without a selector and add an EndpointSlice labeled kubernetes.io/service-name
B. Set type: ExternalIP on the Service and list the database address in spec.externalIPs for kube-proxy to route
C. Create an Ingress with the IP
D. Add the IP to the kube-proxy ConfigMap

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Without a selector Kubernetes does not create EndpointSlices; you add one with the service-name label and the external addresses.
</details>

---

### Question 11
**Scenario:** What does an ExternalName Service do?

A. Proxies traffic to the external host through kube-proxy using a cluster-local virtual IP address
B. Creates a NodePort for the external host
C. Allocates a ClusterIP for the external host
D. Returns a CNAME record for the external hostname; no proxying is set up

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** ExternalName maps the Service to the externalName field with a DNS CNAME and no proxying of any kind.
</details>

---

### Question 12
**Scenario:** What does the kube-proxy documentation recommend about the proxy mode?

A. Always rely on the default so upgrades are automatic, since the project promises it will stay stable
B. Use ipvs because iptables is deprecated on Linux
C. Disable kube-proxy on all Linux clusters
D. Set it explicitly, because the default may change in a future version

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The page says the default is iptables in 1.37 and a future version will change it to nftables, so clusters should state the mode explicitly.
</details>

---

### Question 13
**Scenario:** Which kube-proxy mode is the only one used on Windows?

A. iptables
B. ipvs
C. kernelspace
D. nftables

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Windows uses kernelspace, which configures packet forwarding rules in the Windows kernel.
</details>

---

### Question 14
**Scenario:** Where is the CoreDNS configuration stored in a typical cluster?

A. A file in /etc/coredns on each node
B. A ConfigMap named coredns in kube-system, under the Corefile key
C. A Secret named coredns in kube-public, mounted into the CoreDNS Pods as a file
D. Inline in the kubelet configuration

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Administrators edit the coredns ConfigMap; the reload plugin applies changes, and the docs say to allow up to two minutes.
</details>

---

### Question 15
**Scenario:** You want queries for consul.local to go to 10.150.0.1. What is the correct CoreDNS change?

A. Add a consul.local:53 server block with forward . 10.150.0.1
B. Change the kubernetes plugin line to include consul.local
C. Add 10.150.0.1 to the Pod resolv.conf for every Pod manually
D. Set ndots to 0 in the Corefile so that consul.local is sent to the upstream resolver

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** A stub domain is a separate server block in the Corefile that forwards the suffix to the chosen resolver.
</details>

---

### Question 16
**Scenario:** From a Pod in namespace test, which name resolves a Service data in namespace prod?

A. data.prod
B. data
C. data.test
D. prod.data

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** A query without a namespace stays in the Pod's own namespace, so data would look in test. data.prod works through the search path.
</details>

---

### Question 17
**Scenario:** What is the default ndots value in a Pod's resolv.conf set by the kubelet?

A. 1
B. 0
C. 2
D. 5

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The documented resolv.conf has options ndots:5 and a search list starting with the Pod's namespace.
</details>

---

### Question 18
**Scenario:** A headless Service's DNS name resolves to what?

A. A single virtual IP
B. A CNAME to the cluster domain
C. The IPs of all selected Pods
D. Nothing; headless Services have no DNS records

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A headless Service uses the same name as a normal one but resolves to the set of Pod IPs.
</details>

---

### Question 19
**Scenario:** In Gateway API, who typically owns a GatewayClass?

A. The application developer
B. The infrastructure provider
C. The cluster operator
D. The end user

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Gateway API is role oriented: infrastructure providers own GatewayClass, cluster operators own Gateways, and application developers own routes.
</details>

---

### Question 20
**Scenario:** An HTTPRoute in namespace team-a cannot attach to a Gateway in namespace infra. What is the most likely default cause?

A. HTTPRoutes can never reference a Gateway in another namespace under any listener configuration or ReferenceGrant
B. The Gateway accepts Routes only from its own namespace unless allowedRoutes allows others
C. The Gateway needs a GRPCRoute in the same namespace
D. The route needs a BackendTLSPolicy

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** By default a Gateway accepts Routes only from its own namespace; set allowedRoutes on the listener for cross-namespace attachment.
</details>

---

### Question 21
**Scenario:** An HTTPRoute backendRefs list foo-v1 weight 90 and foo-v2 weight 10. How is traffic split?

A. In proportion to the weights, 90 to 10
B. Always 50/50 because weights are ignored
C. 90 percent to foo-v2
D. Only to foo-v1 because it is listed first

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Weight is a proportional split, not a percentage: share equals weight divided by the total. Weight defaults to 1.
</details>

---

### Question 22
**Scenario:** Which statement about Kubernetes NetworkPolicies is correct?

A. They are enforced by kube-proxy on every cluster
B. A deny rule in one policy overrides an allow in another, so the policy that was applied first decides the outcome
C. They apply at layer 7 to HTTP paths
D. They have no effect unless the network plugin implements them, and multiple policies are additive

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The docs say creating a NetworkPolicy without a controller that implements it has no effect, and policies do not conflict, they are additive. They operate at layers 3 and 4.
</details>

---

### Question 23
**Scenario:** For traffic from Pod A to Pod B to be allowed under NetworkPolicies, what must be true?

A. Only B's ingress policy matters
B. Only A's egress policy matters
C. Both A's egress policy and B's ingress policy must allow it
D. Neither; policies apply only to Services and are evaluated by the Service's kube-proxy rules

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A connection needs both the source Pod's egress policy and the destination Pod's ingress policy to allow it.
</details>

---

### Question 24
**Scenario:** Which Cilium encryption setting requires WireGuard and is not supported with IPsec?

A. Egress strict mode
B. Any encryption
C. Ingress strict mode (encryption.strictMode.ingress.enabled)
D. Strict mode egress CIDR

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Ingress strict mode drops cluster-internal ingress that did not arrive through the WireGuard tunnel and does not work with IPsec.
</details>

---

### Question 25
**Scenario:** Which Gateway listener TLS mode lets the encrypted session pass through unchanged?

A. Terminate
B. Passthrough
C. Offload
D. Mutual

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** In Terminate mode the Gateway ends TLS using certificateRefs; Passthrough passes the encrypted session unchanged so listener TLS settings have no effect.
</details>

---

### Question 26
**Scenario:** A Gateway listener references a TLS Secret in another namespace. What is required?

A. A ReferenceGrant in the Secret's namespace
B. A NetworkPolicy allowing the Secret
C. The Secret must be copied to kube-system
D. Nothing; cross-namespace references always work

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Without a ReferenceGrant in the Secret's namespace, the reference is invalid.
</details>

---

### Question 27
**Scenario:** Where does an Istio AuthorizationPolicy source principals match, and what does it require?

A. to.operation.principals, which work without mTLS
B. when.principals, which require JWT only
C. metadata.principals, set by the API server
D. from.source.principals, which require mTLS

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** principals and namespaces under from.source require mTLS, because identity comes from the mTLS certificate.
</details>

---

### Question 28
**Scenario:** An ALLOW AuthorizationPolicy with no rules is applied to a workload. What happens?

A. All requests are allowed
B. Only requests that originate inside the mesh are allowed, because no rule matches external sources
C. The policy is ignored
D. It matches nothing, so all requests to the workload are denied

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** An ALLOW policy with no rules matches nothing; once any ALLOW policy applies to a workload, requests not matched by one are denied.
</details>

---

### Question 29
**Scenario:** Which Hubble command shows only dropped flows for a pod?

A. hubble status --drops
B. cilium monitor --pod <name> --json, filtered with jq to events whose verdict is dropped
C. hubble observe --pod <name> --verdict DROPPED
D. hubble get drops <name>

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** hubble observe supports --pod and --verdict DROPPED; run hubble status to confirm access to the Hubble API.
</details>

---

### Question 30
**Scenario:** For Istio tracing to join proxy spans into one trace, what must the application do?

A. Nothing; the proxy does everything
B. Forward the tracing headers such as traceparent from incoming to outgoing requests
C. Open a direct connection to the tracing backend and send its own spans with the proxy's trace ID
D. Disable the sidecar

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Istio's docs say the proxies can send spans, but extra information is needed to join them: applications must collect headers from each incoming request and forward them to all outgoing requests it triggers.
</details>

---
