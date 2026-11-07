---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 11 min
---

# 01 - Core Infrastructure and CNI

**Domain 1: Core Infrastructure and CNI (15%)**

Curriculum competencies: installing and configuring CNI plugins; managing IPAM and Pod CIDR allocation; using Linux tools (iptables, ip, tcpdump) for packet-level issues; troubleshooting Pod connectivity (DNS, pod-to-pod); configuring multi-interface Pods.

CKNE is a **performance-based** exam: tasks at a terminal in a Linux remote desktop. The Linux Foundation page says CKNE "assumes CKA-level Kubernetes administration skills", so [CKA](../../cka/) is the foundation for this note.

Commands and YAML here are quoted or adapted from vendor docs, and YAML was syntax-checked with a parser. **Nothing was run or applied**: no cluster was available when this guide was written. Where a command comes from general practice and was not on a fetched page, the text says so.

---

## The Kubernetes network model and CNI

Kubernetes clusters need non-overlapping IP addresses for Pods, Services and Nodes. The cluster networking page says who assigns each:

| Object | Assigned by |
|---|---|
| Pod IPs | The network plugin |
| Service IPs | The kube-apiserver |
| Node IPs | The kubelet or the cloud-controller-manager |

A cluster can be IPv4 only, IPv6 only, or dual-stack; for dual-stack, "All components must agree on the configured primary IP family."

The page also says: "The network model is implemented by the container runtime on each node. The most common container runtimes use Container Network Interface (CNI) plugins to manage their network and security capabilities." Kubernetes' four networking problems are container-to-container in a Pod (localhost), Pod-to-Pod, Pod-to-Service and external-to-Service.

**[📖 Cluster networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)** - IP allocation, network types, CNI role

---

## Installing and configuring CNI plugins

Facts from the network plugins page:

- A CNI plugin is required to implement the Kubernetes network model. Plugins must support CNI spec **v0.4.0 or later**; the project recommends **v1.0.0**.
- **The container runtime**, not the kubelet, loads CNI plugins. The kubelet flags `cni-bin-dir` and `network-plugin` were **removed in Kubernetes 1.24**.
- Config and binary directories: the page names `/etc/cni/net.d` (config) and `/opt/cni/bin` (binaries) as defaults in its traffic-shaping section, and says to check your runtime's documentation, since these are not documented as universal.
- The runtime must provide a **loopback interface `lo`** in each sandbox (reuse the CNI loopback plugin or implement your own).
- The CNI plugin must support **`hostPort`**: use the official `portmap` plugin with `portMappings` in the capabilities.
- Traffic shaping (experimental): add the `bandwidth` plugin to the CNI config and annotate Pods with `kubernetes.io/ingress-bandwidth` and `kubernetes.io/egress-bandwidth`.

A CNI config chains plugins. The page's example chains a main plugin (Calico) with `portmap`:

```json
{
  "name": "k8s-pod-network",
  "cniVersion": "0.4.0",
  "plugins": [
    {
      "type": "calico",
      "log_level": "info",
      "datastore_type": "kubernetes",
      "nodename": "127.0.0.1",
      "ipam": { "type": "host-local", "subnet": "usePodCidr" },
      "policy": { "type": "k8s" },
      "kubernetes": { "kubeconfig": "/etc/cni/net.d/calico-kubeconfig" }
    },
    {
      "type": "portmap",
      "capabilities": {"portMappings": true},
      "externalSetMarkChain": "KUBE-MARK-MASQ"
    }
  ]
}
```

Practical install order in a task: pick the plugin the exam environment provides, apply its manifest or Helm chart, wait for the node-level agent to become Ready, and check that nodes move to `Ready`. Nodes stay `NotReady` until a CNI is configured. Each plugin documents its own installation; for Cilium see the [CCA guide](../../cca/).

**[📖 Network plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)** - CNI versions, directories, hostPort, traffic shaping

---

## IPAM and Pod CIDR allocation

IPAM (IP address management) decides which IPs Pods get. The CNI config above shows the idea: `"ipam": { "type": "host-local", "subnet": "usePodCidr" }` hands out addresses from the Pod CIDR assigned to the node.

The Service side is documented in the ClusterIP allocation page:

- ClusterIPs are allocated **dynamically** from the Service range or **statically** by setting `spec.clusterIP`. Each must be unique cluster-wide.
- The range is split into a static band and a dynamic band using `min(max(16, cidrSize / 16), 256)`; dynamic allocation uses the upper band first.
- Example from the page: in `10.96.0.0/16` the static band is `10.96.0.1` to `10.96.1.0` (256 addresses) and the DNS Service is given the static address `10.96.0.10`.

The page does **not** cover Pod CIDR allocation flags such as `--cluster-cidr` and `--allocate-node-cidrs` or `node.spec.podCIDR`. Those are in the kube-controller-manager reference and in your CNI's documentation, which is where to look during a task. Plugins differ: some use the per-node Pod CIDR from the control plane; others (Cilium has several IPAM modes) manage ranges themselves.

Rule of thumb for any IPAM task: Pod range, Service range and Node range must not overlap, and ranges are painful to change on a live cluster, so read what is configured before changing anything.

**[📖 ClusterIP allocation](https://kubernetes.io/docs/concepts/services-networking/cluster-ip-allocation/)** - static and dynamic bands

---

## Linux tools for packet-level issues

The curriculum names `iptables`, `ip` and `tcpdump`. These are standard Linux tools and were **not** among the pages fetched for this guide, so treat the table as general practice and confirm syntax with `--help` or the man page.

| Tool | Use in a networking task |
|---|---|
| `ip addr`, `ip route`, `ip link` | See interfaces, node and Pod routes, whether a veth or bridge exists |
| `iptables -t nat -L -n` (or `iptables-save`) | Inspect the NAT rules kube-proxy writes for Services (iptables mode) |
| `tcpdump -i <iface> -nn host <ip>` | Confirm whether packets arrive, leave, or are dropped |
| `nslookup` / `dig` in a debug Pod | Test DNS from where the failing client lives |

The kube-proxy page notes one caveat: kernel-level rules such as iptables rules "won't get cleaned up, in some cases until you reboot" after changing modes.

Reaching a node or a Pod network namespace is a `kubectl debug` job. The standard forms are `kubectl debug -it <pod> --image=<image> --target=<container>` (ephemeral container) and `kubectl debug node/<node> -it --image=<image>` (node shell, host filesystem under `/host`). The fetched excerpt of the debug page did not show these, so confirm with `kubectl debug --help`.

---

## Troubleshooting Pod connectivity

A fixed order saves time. Test from the failing Pod, working from the inside out:

1. **Pod has an IP?** `kubectl get pod -o wide`. No IP means a CNI problem (check node Ready state, CNI Pods and the runtime logs).
2. **Pod to itself and its node?** Loopback must exist; node-to-Pod traffic should work.
3. **Pod to Pod on the same node, then another node?** Failure across nodes only points to routing or overlay between nodes (MTU, firewall, encapsulation).
4. **Pod to a Service ClusterIP?** Failure here with healthy endpoints points to kube-proxy or the CNI's replacement (domain 2).
5. **Pod to a Service name?** Failure here but IP works points to DNS (domain 2).
6. **Is a NetworkPolicy isolating either end?** A connection needs the source's egress policy and the destination's ingress policy to allow it (domain 4).

The DNS-specific half of the walk is in the next note.

---

## Multi-interface Pods (Multus)

Pods normally have one interface. **Multus** lets a Pod attach to additional networks. From the Multus usage guide:

- A secondary network is defined by a **NetworkAttachmentDefinition** (`k8s.cni.cncf.io/v1`, namespaced, short name `net-attach-def`) whose CNI configuration is in `spec.config`.
- A Pod requests networks with the annotation **`k8s.v1.cni.cncf.io/networks`**: a comma-separated list of NAD names, optionally with a `<namespace>/` prefix and an `@<ifname>` suffix, or a JSON array.

```yaml
apiVersion: k8s.cni.cncf.io/v1
kind: NetworkAttachmentDefinition
metadata:
  name: macvlan-conf-1
spec:
  config: '{
            "cniVersion": "0.3.0",
            "type": "macvlan",
            "master": "eth1",
            "mode": "bridge",
            "ipam": {
                "type": "host-local",
                "ranges": [
                    [ {
                         "subnet": "10.10.0.0/16",
                         "rangeStart": "10.10.1.20",
                         "rangeEnd": "10.10.3.50",
                         "gateway": "10.10.0.254"
                    } ]
                ]
            }
        }'
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-case-03
  annotations:
    k8s.v1.cni.cncf.io/networks: macvlan-conf-1@macvlan1
spec:
  containers:
  - name: pod-case-03
    image: docker.io/centos/tools:latest
    command:
    - /sbin/init
```

Verify with `kubectl exec -it <pod> -- ip -d address`: you should see `eth0` (the default network) plus the secondary interface (named `macvlan1` here because of the `@macvlan1` suffix). Without a name suffix the extra interface is numbered (the page shows `net2`).

**[📖 Multus usage](https://github.com/k8snetworkplumbingwg/multus-cni/blob/master/docs/how-to-use.md)** - NAD, annotation, verification

---

## Key terms

- **CNI** - the Container Network Interface, the plugin standard container runtimes use to set up Pod networking.
- **IPAM** - IP address management, the part of a network plugin that assigns Pod addresses.
- **Pod CIDR** - the address range from which Pod IPs are assigned.
- **ClusterIP** - the virtual IP the API server assigns to a Service.
- **Dual-stack** - a cluster that runs both IPv4 and IPv6.
- **portmap** - the CNI plugin that implements `hostPort`.
- **veth pair** - a virtual Ethernet link connecting a Pod's network namespace to the node.
- **tcpdump** - a packet capture tool used to see whether traffic arrives and leaves an interface.
- **Multus** - a CNI meta-plugin that attaches multiple network interfaces to a Pod.
- **NetworkAttachmentDefinition** - the custom resource that defines a secondary network for Multus.
- **macvlan** - a CNI plugin type that gives a Pod an interface with its own MAC address on a parent interface.
