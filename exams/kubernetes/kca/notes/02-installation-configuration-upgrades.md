---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 12 min
---

# 02 - Installation, Configuration, and Upgrades

**Domain 2: Installation, Configuration, and Upgrades (18%)**

Curriculum topics, in order: Helm-based Installation and Configuration, Kyverno Custom Resource Definitions (CRDs), Controller Configuration with Flags, Configuring Kyverno RBAC, roles, and permissions, High Availability Installations, Upgrading Kyverno.

All commands in this note come from the Kyverno docs and were **not run** (no cluster and no Helm binary were available when this guide was written).

---

## Helm-based installation

The installation page calls Helm the recommended method for production. Kyverno "must run in a dedicated namespace" and should not share one with other applications, including system Namespaces such as `kube-system`.

```bash
helm repo add kyverno https://kyverno.github.io/kyverno/helm
helm repo update
helm install kyverno kyverno/kyverno -n kyverno --create-namespace
```

Useful variants from the same page:

| Goal | Command or flag |
|---|---|
| Pre-release builds (alpha, beta, rc) | add `--devel` |
| Optional Reports Server subchart | `--set reportsServer.enabled=true` |
| Pod Security policies as a separate chart | `helm install kyverno-policies kyverno/kyverno-policies -n kyverno` |
| Install from a manifest instead of Helm | `kubectl create -f https://github.com/kyverno/kyverno/releases/download/v1.16.2/install.yaml` (a tagged release; the `main` manifest is for testing only) |

The page does not list Kubernetes version compatibility; it sends you to the Releases page. Check that before installing.

**[📖 Installing Kyverno](https://kyverno.io/docs/installation/methods/)** - Helm, HA and manifest installs

---

## Kyverno CRDs

Kyverno adds its own resource types. The ones you meet in this guide, by API group:

| Group | Kinds |
|---|---|
| `kyverno.io` | `ClusterPolicy`, `Policy`, `PolicyException`, `CleanupPolicy`, `ClusterCleanupPolicy`, `GlobalContextEntry`, `UpdateRequest` |
| `policies.kyverno.io` | `ValidatingPolicy`, `MutatingPolicy`, `GeneratingPolicy`, `ImageValidatingPolicy`, `DeletingPolicy`, `PolicyException` (and `Namespaced...` variants) |
| `wgpolicyk8s.io` | `PolicyReport`, `ClusterPolicyReport` (open report format, not Kyverno-specific) |
| `reports.kyverno.io` | admission and background scan report types (the intermediate reports) |

The upgrade page names the `kyverno.io` CRDs affected by the v1.13 API cleanup: cleanuppolicies, clustercleanuppolicies, clusterpolicies, globalcontextentries, policies, policyexceptions and updaterequests.

CRD handling changes by version, so read it before an upgrade:

- **v1.19:** CRDs are managed through a dedicated `kyverno-api` chart dependency, controlled by the `crds.install` value. If you install CRDs separately or set `crds.install: false`, review your CRD workflow first.
- **v1.13:** deprecated API versions of the CRDs were dropped; the Helm hook migrates stored resources.

**[📖 Upgrading Kyverno](https://kyverno.io/docs/installation/upgrading/)** - CRD handling per version

---

## Controller configuration with flags

Each controller is a Deployment with container arguments (flags). The customization page lists them with a letter for which controllers read them: A = admission, B = background, C = cleanup, R = reports. The ones worth knowing:

| Flag | Default | Purpose |
|---|---|---|
| `enablePolicyException` (ABR) | `false` | Turns on PolicyException support |
| `exceptionNamespace` (ABR) | none | Namespace where exceptions are accepted; `*` accepts all; required when exceptions are enabled |
| `webhookTimeout` (A) | `10` | Webhook timeout in seconds, 1 to 30 |
| `backgroundScanInterval` (R) | `1h` | Time between periodic background scans |
| `backgroundScan` (R) | `true` | Enables background report scans |
| `autoUpdateWebhooks` (A) | `true` | When `false`, Kyverno creates a wildcard webhook and stops managing it |
| `forceFailurePolicyIgnore` (A) | `false` | Forces the webhook failure policy to `Ignore` |
| `tlsKeyAlgorithm` (AC) | `RSA` | Key type for managed certificates: RSA, ECDSA or Ed25519 |
| `renewBefore` (AC) | `360h0m0s` | How early certificates renew |
| `maxBackgroundReports` (BR) | `10000` | Cap on ephemeral reports for background policies |
| `omitEvents` (ABR) | `PolicyApplied,PolicySkipped` | Event types not emitted |

With Helm you do not edit the Deployment by hand; you set chart values and the chart writes the arguments. The page gives examples such as `admissionController.tlsKeyAlgorithm`.

### The `kyverno` ConfigMap

Behavior that is not a flag lives in the `kyverno` ConfigMap `data` keys:

- **`resourceFilters`** - `[kind,namespace,name]` entries the admission webhook skips. Wildcards work. Changes apply at runtime.
- **`excludeGroups`** - default `system:serviceaccounts:kube-system,system:nodes`.
- **`excludeUsernames`** - default `!system:kube-scheduler` (a `!` prefix negates).
- **`webhooks`** - a JSON `namespaceSelector`; by default it excludes `kube-system` and `kyverno`.
- **`defaultRegistry`** - `docker.io` by default.
- **`updateRequestThreshold`** - default `1000`.

**[📖 Customize Kyverno (flags, ConfigMap)](https://kyverno.io/docs/installation/customization/)** - the full flag and ConfigMap tables

---

## RBAC, roles and permissions

Kyverno follows least privilege. Each controller has its own ServiceAccount and ClusterRole: `kyverno:admission-controller`, `kyverno:background-controller`, `kyverno:reports-controller` and `kyverno:cleanup-controller`. These aggregate smaller `:core` ClusterRoles.

When a policy needs access the defaults do not give, **do not edit the default roles** (upgrades can overwrite your changes). Add a new ClusterRole carrying an aggregation label for the controller that needs it:

- `rbac.kyverno.io/aggregate-to-admission-controller`
- `rbac.kyverno.io/aggregate-to-background-controller`
- `rbac.kyverno.io/aggregate-to-reports-controller`
- `rbac.kyverno.io/aggregate-to-cleanup-controller`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kyverno:create-deployments
  labels:
    rbac.kyverno.io/aggregate-to-background-controller: "true"
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["create", "update"]
```

*Built from the page's description of its `kyverno:create-deployments` example; the page names the role, group, verbs and label, and the manifest layout here is standard RBAC. Not applied.*

What each rule type needs, from the same page:

| Policy type | Controller | Permissions it needs |
|---|---|---|
| Mutate existing | background | update, view, list, watch on the targets |
| Generate | background | create, update, delete and read on the generated kind |
| Policy reports | reports | view, list, watch |
| Cleanup | cleanup | delete, view, list, watch |
| ValidatingAdmissionPolicy generation | admission | read, create, update, delete on `validatingadmissionpolicies` and `validatingadmissionpolicybindings` |

Verify aggregation with `kubectl get clusterrole kyverno:background-controller -o yaml`.

For generate rules that create RoleBindings, Kubernetes blocks privilege escalation: the background controller must itself already hold the permissions it is handing out. The generate page's fix is a ClusterRoleBinding that binds `kyverno-background-controller` to the `admin` ClusterRole before the policy is installed.

---

## High availability

Kyverno runs **four controllers, each in its own Deployment**, and HA is set **per controller**. A default install runs one replica of each. The Helm example on the installation page:

```bash
helm install kyverno kyverno/kyverno -n kyverno --create-namespace \
  --set admissionController.replicas=3 \
  --set backgroundController.replicas=2 \
  --set cleanupController.replicas=2 \
  --set reportsController.replicas=2
```

How replicas behave, from the HA page:

| Controller | Leader election | What extra replicas give you |
|---|---|---|
| Admission | Not for webhook requests; needed for certificate and webhook management | Availability and throughput; each replica loads the full policy set |
| Reports | Required (one leader processes reports) | Availability only |
| Background | Required (one leader produces generated and mutated resources) | Availability only; scale with resources or workers (`--genWorkers`) |
| Cleanup | Required for certificate and webhook management, not for cleanup handling | Availability and scale |

**Source discrepancy.** The HA page says "The minimum supported replica count for a highly-available admission controller deployment is three." The installation page says an HA install needs "at least 2 replicas" of the admission controller, and its own example uses 3. For an exam, three is the safe answer; the example sets 3 for admission.

**[📖 High availability](https://kyverno.io/docs/high-availability/)** - replica guidance per controller

---

## Upgrading Kyverno

Rules from the upgrade page:

1. **A tag bump is not an upgrade.** "An upgrade cannot be done by bumping the tag of any image," because new versions often change CRDs and other supporting resources. Use Helm or the release manifest.
2. **Helm upgrades are supported; YAML upgrades are not direct.** "Direct upgrades from previous versions are not supported when using the YAML manifest approach." Remove the old version using the manifest you installed it with, then install the new one.
3. **Pre-1.10 to 1.10+ needs manual steps** (the Helm chart v2 to v3 migration guide).
4. **Do not skip release notes.** "If skipping a minor version, be sure to read the release notes for each minor version in between."
5. **Policy exceptions** stopped being enabled in all Namespaces by default in 1.13 (to address CVE-2024-48921). To keep them on everywhere after upgrading, the page shows: `helm upgrade kyverno kyverno/kyverno -n kyverno --set features.policyExceptions.enabled=true --set features.policyExceptions.namespace="*"`, and recommends limiting them to specific Namespaces instead.
6. **v1.19 deprecations (removal planned for v1.20):** `ClusterPolicy` and `Policy`, `CleanupPolicy` and `ClusterCleanupPolicy`, the legacy `PolicyException` in `kyverno.io/v2`, and the v1alpha1 versions of the `policies.kyverno.io` types.
7. The page does not cover rollback.

---

## Key terms

- **Helm** - the Kubernetes package manager; the recommended way to install Kyverno in production.
- **CRD** - a CustomResourceDefinition, which adds a new resource type such as ClusterPolicy to the API.
- **Admission controller (Kyverno)** - the Kyverno Deployment that serves webhooks and evaluates policies on live requests.
- **Background controller** - the Kyverno Deployment that handles generate and mutate-existing policies through UpdateRequests.
- **Reports controller** - the Kyverno Deployment that builds PolicyReports from admission and background scan reports.
- **Cleanup controller** - the Kyverno Deployment that runs cleanup policies and TTL deletion.
- **Leader election** - a mechanism that lets only one replica of a controller do certain work at a time.
- **Resource filter** - a `[kind,namespace,name]` entry in the `kyverno` ConfigMap that the admission webhook skips.
- **Aggregated ClusterRole** - a ClusterRole whose rules are collected from other ClusterRoles through labels, which is how Kyverno permissions are extended safely.
- **High availability (HA)** - running more than one replica of a controller so a single Pod failure does not stop admission.
