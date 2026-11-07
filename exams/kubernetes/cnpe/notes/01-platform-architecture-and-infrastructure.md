---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 10 min
---

# 01 - Platform Architecture and Infrastructure

**Domain 1: Platform Architecture and Infrastructure (15%)**

Curriculum competencies: applying platform architecture best practices for networking, storage and compute; using cost management solutions for right-sizing and scaling; optimizing multi-tenancy resource usage.

CNPE is a **performance-based** exam: you solve tasks at a terminal and in web interfaces. The curriculum says candidates complete tasks "using unfamiliar tools by relying on help and documentation available in the exam," and that you will not be tested on deep tool-specific knowledge unless it is named in the competencies. Read each section as "what would I do at the keyboard," not "what would I memorize."

YAML in these notes was syntax-checked with a YAML parser only. **Nothing was applied to a cluster**: no cluster was available when this guide was written.

---

## Architecture best practices: networking, storage, compute

The curriculum gives no tool list for this competency, so the exam is about Kubernetes primitives used well. A platform engineer's checklist:

| Area | What you are expected to configure or judge |
|---|---|
| Networking | Services and DNS, NetworkPolicy defaults, ingress or Gateway API exposure, which traffic needs a mesh |
| Storage | StorageClass, PersistentVolumeClaim, who gets which class, retention and reclaim behavior |
| Compute | Requests and limits, autoscaling, node pools, isolating noisy tenants |

Build habits that carry over to any task:

- **Requests and limits on everything.** A ResourceQuota that covers CPU or memory requires every new Pod in the namespace to set a request or limit for that resource, otherwise the control plane may reject the Pod (ResourceQuota page).
- **Defaults via LimitRange**, so teams do not have to repeat them on every Pod.
- **One workload per namespace** is the common practice the multi-tenancy page recommends, "even if multiple workloads are operated by the same tenant."

For networking, storage and DNS depth, see the [CKA guide](../../cka/) and the [Cilium guide](../../cca/). The platform-level goal here is a sensible, repeatable default, not heroic tuning.

---

## Cost management: right-sizing and scaling

### Measuring cost with OpenCost

OpenCost is listed among the curriculum's example tools. Its site describes it as "a vendor-neutral open source project for measuring and allocating cloud infrastructure and container costs," built for "real-time cost monitoring, showback, and chargeback," with a UI that visualizes Kubernetes allocations. Showback means showing a team its cost; chargeback means billing it.

On the exam, expect "find the namespace that costs the most" or "see which workloads are over-provisioned." Use the UI or its allocation data, then act on it with requests, limits and autoscaling.

**[📖 OpenCost documentation](https://opencost.io/docs/)** - what OpenCost measures and how to install it

### Scaling with the Horizontal Pod Autoscaler

The HPA is a resource plus a control loop that adjusts a workload's replica count to match metrics such as average CPU utilization. From the docs:

- The loop runs every **15 seconds** by default (`--horizontal-pod-autoscaler-sync-period` on the controller manager).
- The algorithm is `desiredReplicas = ceil(currentReplicas x currentMetricValue / desiredMetricValue)`.
- Utilization is a percentage of each container's **resource request**: "if containers lack the relevant request, the autoscaler takes no action for that metric."
- Resource metrics come from the `metrics.k8s.io` API, usually provided by **Metrics Server**, which you install separately. Custom and external metrics use `custom.metrics.k8s.io` and `external.metrics.k8s.io`.
- DaemonSets and other unscalable objects are not supported.

A task that says "HPA shows `<unknown>`" almost always means missing Metrics Server or missing CPU requests on the Pods.

**[📖 Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)** - the control loop and algorithm

The cost reference in this repo, [Kubernetes cost optimization](../../../../resources/cost-optimization/kubernetes-cost-optimization.md), covers VPA, Karpenter and Cluster Autoscaler in more depth.

---

## Multi-tenancy resource usage

Multiple teams sharing one cluster is the common platform case. The Kubernetes multi-tenancy page frames two forms: **multiple teams** (some trust exists; RBAC, quotas and network policies keep sharing safe and fair) and **multiple customers** (strong isolation needed). It describes "hard" multi-tenancy as the case where tenants do not trust each other, and says hardness is "better understood as a broad spectrum."

**Namespaces** are the base isolation unit: "Many Kubernetes security policies are scoped to namespaces. For example, RBAC Roles and Network Policies are namespace-scoped resources."

### ResourceQuota

A ResourceQuota is namespace-scoped and caps aggregate consumption or object counts. Violations are rejected with `403 Forbidden`.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: team-a
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
```

*Adapted from the compute-resources quota example on the ResourceQuota page (that page's example uses namespace `myspace` and different values). Not applied.*

Behaviors worth knowing:

- Quota does not affect resources that already exist.
- A Deployment is created successfully even when its Pods would exceed quota; the Pods then fail to be created, so look at the Deployment and ReplicaSet events with `kubectl describe`.
- If the sum of quotas exceeds cluster capacity, contention is resolved first-come, first-served.
- Restrict who can update or delete quotas, for example with a ValidatingAdmissionPolicy, or tenants can lift their own limits.

**[📖 Resource quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)** - compute keys, scopes, LimitRange interaction

**[📖 Multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)** - soft vs hard, namespaces, dedicated clusters

For the strongest isolation the page says it may be "easier or necessary to forgo any cluster-level sharing at all and assign each tenant their dedicated cluster," weighed against the cost of running many clusters.

---

## Key terms

- **Platform engineering** - building the shared infrastructure and self-service tooling that application teams consume.
- **Right-sizing** - matching resource requests and limits to what a workload actually uses.
- **Showback** - reporting a team's cloud cost to it without billing it.
- **Chargeback** - billing a team for the cost it generates.
- **OpenCost** - a vendor-neutral open source project that measures and allocates Kubernetes and cloud costs.
- **ResourceQuota** - a namespace-scoped object that limits aggregate resource use or object counts.
- **LimitRange** - a namespace policy that sets default and boundary requests and limits for containers.
- **HorizontalPodAutoscaler** - a controller that changes replica count to match observed metrics.
- **Metrics Server** - the add-on that provides `metrics.k8s.io` resource metrics to the HPA.
- **Multi-tenancy** - sharing one cluster among multiple teams or customers with isolation between them.
- **Hard multi-tenancy** - isolation strong enough for tenants that do not trust each other.
