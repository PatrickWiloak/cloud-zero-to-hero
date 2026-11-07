---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 13 min
---

# 05 - Security and Policy Enforcement

**Domain 5: Security and Policy Enforcement (15%)**

Curriculum competencies: configuring secure service-to-service communication; applying RBAC and security controls across platform resources; generating audit trails and enforcing policy compliance (SBOM, compliance reports and so on); using policy engines and admission controllers for governance; integrating security scanning and compliance checks into deployment pipelines.

Tools named in the curriculum: Istio, Linkerd, Kyverno, OPA, Gatekeeper. YAML was syntax-checked only, never applied.

---

## Secure service-to-service communication (mTLS)

Mutual TLS means both sides of a connection prove their identity with certificates and the traffic is encrypted. The curriculum lists two meshes.

### Istio PeerAuthentication

`PeerAuthentication` (`security.istio.io/v1`) sets the mTLS requirement for incoming connections. Modes:

| Mode | Behavior |
|---|---|
| `UNSET` | Inherits from the parent scope; with no parent it acts as `PERMISSIVE` |
| `DISABLE` | The connection is not tunneled |
| `PERMISSIVE` | Accepts plaintext or an mTLS tunnel |
| `STRICT` | Requires an mTLS tunnel; the client must present a certificate |

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: foo
spec:
  mtls:
    mode: STRICT
```

Scopes: **mesh-wide** (put it in the root namespace of your Istio installation; workload selectors are ignored there), **namespace-wide** (as above, no `selector`), **workload** (add `spec.selector.matchLabels`), and **per port** with `portLevelMtls`, which applies only with a workload selector and uses the workload's container port, not the Service port. A common migration path is `PERMISSIVE` first (so non-mesh clients keep working) and `STRICT` after everything is meshed.

**[📖 Istio PeerAuthentication](https://istio.io/latest/docs/reference/config/security/peer_authentication/)** - modes and scopes

For the full mesh picture see the [ICA guide](../../ica/).

### Linkerd automatic mTLS

Linkerd enables mTLS for "all TCP traffic between meshed pods" with no extra configuration. Proxy certificates last 24 hours and rotate automatically; a proxy's identity is its Kubernetes ServiceAccount. The default trust anchor from `linkerd install` expires after 365 days and must be rotated manually (use cert-manager for automatic issuer rotation). Exceptions: traffic to or from non-meshed pods (such as Kubernetes health checks), traffic on skip ports, and plaintext from non-meshed sources, which is accepted by default unless authorization policies disable it.

**[📖 Linkerd automatic mTLS](https://linkerd.io/2/features/automatic-mtls/)** - identity, certificates, exceptions

---

## RBAC and security controls

RBAC grants permissions through Roles and bindings. From the Kubernetes docs:

- A **Role** grants permissions within one namespace. A **ClusterRole** is cluster-scoped and can grant namespaced permissions (through a RoleBinding in one namespace, or a ClusterRoleBinding across all), access to cluster-scoped resources such as nodes, and non-resource endpoints such as `/healthz`.
- A **RoleBinding** grants a Role or ClusterRole to subjects (users, groups, ServiceAccounts) within one namespace; it can reference a ClusterRole to reuse it. A **ClusterRoleBinding** grants cluster-wide.
- **Permissions are purely additive. There are no deny rules.**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

A Role does nothing until it is bound:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

*The RoleBinding was marked in the fetched excerpt as taken from the upstream Kubernetes docs; the Role is from the fetched page. Neither was applied.*

Platform-level pattern: give each team a ClusterRole defined once and bind it with a RoleBinding **per namespace**, so the same role is reused without granting cluster-wide access. Platform controllers (Argo CD, Flux, Crossplane) have their own service accounts, so check what those can create.

**[📖 Using RBAC authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)** - Roles, bindings, scope

---

## Audit trails and compliance evidence

### Kubernetes audit logging

Auditing records a chronological sequence of actions in the cluster, produced in the kube-apiserver. Key points:

- **Stages:** `RequestReceived`, `ResponseStarted` (only long-running requests such as watches), `ResponseComplete`, `Panic`.
- **Levels:** `None`, `Metadata` (user, timestamp, resource, verb; no bodies), `Request` (adds the request body), `RequestResponse` (adds the response body). Rules are checked in order and the **first match** sets the level.
- **Policy file:** `--audit-policy-file`; if omitted, no events are logged. A policy must have `rules`.
- **Backends:** log (JSON Lines file, `--audit-log-path`; `-` is stdout; rotation flags `--audit-log-maxage`, `--audit-log-maxbackup`, `--audit-log-maxsize`) and webhook. If the API server runs as a Pod, mount a `hostPath` for the policy and log files.

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - "RequestReceived"
rules:
  - level: RequestResponse
    resources:
    - group: ""
      resources: ["pods"]
  - level: Metadata
    resources:
    - group: ""
      resources: ["secrets", "configmaps"]
  - level: Metadata
```

*Shortened from the docs' example policy. Rule order matters: the last rule is the catch-all.*

**[📖 Auditing](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/)** - stages, levels, backends, example policy

### SBOMs and scan reports

An SBOM (software bill of materials) lists the components inside an image. Trivy generates them in CycloneDX and SPDX:

```bash
trivy image --format cyclonedx --output result.json IMAGE
trivy image --format spdx-json --output result.json alpine:3.15
trivy sbom ./sbom.spdx
```

CycloneDX output has no vulnerability data by default; add `--scanners vuln` to include it. `trivy sbom` scans an existing SBOM file. Trivy is not on the curriculum's tool list, which only says "SBOM, compliance reports, etc.," so treat this as one way to produce the artifact; the exam environment's own tools take precedence.

**[📖 Trivy SBOM](https://trivy.dev/latest/docs/supply-chain/sbom/)** - formats and commands

Policy engines also produce compliance evidence: Kyverno policy reports (`wgpolicyk8s.io`) and Gatekeeper audit results list which existing resources violate policy (see below).

---

## Policy engines and admission controllers

Kubernetes admission control is where governance is enforced. Two policy engines are on the tool list; the [KCA guide](../../kca/) covers Kyverno in depth.

### Kyverno in one paragraph

A Kyverno policy is a Kubernetes resource with rules that **validate, mutate, generate, clean up or verify images**. `Enforce` blocks a violating resource at admission; `Audit` allows it and records the violation in a policy report. Background scans check existing resources and never block. See [KCA note 05](../../kca/notes/05-writing-policies.md).

### Gatekeeper (OPA)

Gatekeeper is OPA's Kubernetes admission integration. It has two resource types.

A **ConstraintTemplate** (`templates.gatekeeper.sh/v1`) defines the policy: `spec.crd` declares the Constraint's kind and parameter schema, and `spec.targets` holds the Rego for the `admission.k8s.gatekeeper.sh` target.

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("you must provide labels: %v", [missing])
        }
```

A **Constraint** (`constraints.gatekeeper.sh/v1beta1`) activates it:

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: ns-must-have-gk
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
  parameters:
    labels: ["gatekeeper"]
```

- `match` selects scope (`kinds`, `namespaces`, `excludedNamespaces`, `labelSelector`, `namespaceSelector`, `name`). An empty `match` matches everything.
- `parameters` appear in Rego as `input.parameters`; the API server rejects parameters that do not match the template schema.
- **`enforcementAction`** is `deny` by default; `dryrun` and `warn` are also supported. Gatekeeper's audit mode evaluates existing resources and reports violations.
- `kubectl get constraints` lists constraints.

**[📖 Gatekeeper: how to use](https://open-policy-agent.github.io/gatekeeper/website/docs/howto/)** - templates, constraints, enforcement

### Kyverno versus Gatekeeper

| | Kyverno | Gatekeeper |
|---|---|---|
| Policy language | Kubernetes-style YAML (plus CEL types) | Rego in a ConstraintTemplate |
| Mutation and generation | Built in | Mutation policies exist (separate); generation is not part of the page read |
| Dry-run-first rollout | `Audit` | `enforcementAction: dryrun` or `warn` |

Pick whichever the exam environment has installed; the skill transfers.

---

## Security scanning and compliance in pipelines

The competency is "integrating security scanning and compliance checks into deployment pipelines." Combine earlier domains:

1. **In the Tekton pipeline** (note 02), add a Task that scans the built image and generates an SBOM; make the Task fail the pipeline on findings (a failed Task sets its TaskRun to `Succeeded: False`).
2. **Use `finally`** to publish reports whether or not earlier Tasks passed.
3. **At admission**, a policy engine enforces what the scan decided (for example, only signed images from an approved registry; see Kyverno `verifyImages` in the KCA guide).
4. **Before merge**, run `kyverno apply` or `kyverno test` in CI to reject manifests that would be blocked later.
5. **In the cluster**, audit logs and policy reports are the evidence.

---

## Key terms

- **mTLS** - mutual TLS, where both client and server authenticate with certificates.
- **PeerAuthentication** - the Istio resource that sets mTLS requirements for incoming connections.
- **STRICT / PERMISSIVE** - Istio mTLS modes: require mTLS versus accept plaintext or mTLS.
- **Trust anchor** - the root certificate that a mesh's workload certificates chain to.
- **RBAC** - role-based access control, with additive Roles and bindings.
- **ServiceAccount** - the Kubernetes identity used by Pods and controllers.
- **Audit policy** - the file that decides which API server events are recorded and at what level.
- **SBOM** - a software bill of materials listing the components in a build artifact.
- **CycloneDX / SPDX** - two common SBOM formats.
- **Admission controller** - code in the API server that intercepts requests before persistence.
- **ConstraintTemplate** - a Gatekeeper resource that defines a policy and its parameter schema in Rego.
- **Constraint** - a Gatekeeper resource that applies a template to selected resources with parameters.
- **enforcementAction** - the Gatekeeper setting that chooses deny, warn or dryrun.
- **Policy report** - a Kubernetes resource listing policy results for current cluster resources.
