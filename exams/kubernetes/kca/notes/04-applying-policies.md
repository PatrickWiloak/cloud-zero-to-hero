---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 9 min
---

# 04 - Applying Policies

**Domain 4: Applying Policies (10%)**

Curriculum topics, in order: Applying Policy in Cluster, Resource Selection, Common Policy Settings for Kyverno Rules.

YAML here is syntax-checked with a YAML parser but **not applied** to a cluster.

---

## Applying a policy in a cluster

A Kyverno policy is a Kubernetes resource, so applying it is the normal act: `kubectl apply -f policy.yaml` (or let Argo CD or Flux sync it from Git). Nothing special is needed beyond Kyverno being installed.

What happens next, from the architecture page: the Webhook Controller "watches installed policies and configures the webhooks to request only the resources those policies match." Installing a policy that matches Pods therefore causes the API server to start sending Pod admission requests to Kyverno.

Scope decides where a policy reaches:

| Kind | Scope | Use it for |
|---|---|---|
| `ClusterPolicy` | Whole cluster, any Namespace | Platform-wide guardrails |
| `Policy` | Its own Namespace only | A team's own rules |

Two things to remember about timing:

1. **Admission is for new and changed requests.** A newly installed `Enforce` policy does not delete or block objects that already exist.
2. **Existing resources are checked by background scans**, which produce policy reports (note 06). The reports page says scans run "once per hour by default" and "don't block resources, even in Enforce mode."

A safe rollout therefore starts a policy in `Audit`, reads the reports to see what it would have blocked, fixes or excepts those workloads, and only then switches to `Enforce`.

---

## Resource selection: match and exclude

Every rule needs a `match` block. `exclude` carves exceptions out of it. From the match and exclude page:

- Each of `match` and `exclude` takes either `any` (logical OR) or `all` (logical AND), **not both in the same block**.
- A rule needs a `match` with at least one element, and `kinds` is mandatory when you use `resources`.
- A resource is selected only if it satisfies `match` and is not caught by `exclude`.
- Inside one `resources` entry, the fields are ANDed; the values within a list are ORed.

The filters:

| Filter | Selects by |
|---|---|
| `resources.kinds` | Resource kind |
| `resources.names` | Names (wildcards allowed) |
| `resources.namespaces` | Namespaces |
| `resources.operations` | Admission operations such as `CREATE`, `UPDATE`, `DELETE` (omitted means CREATE and UPDATE) |
| `resources.selector` | Labels (`matchLabels` or `matchExpressions`) |
| `resources.namespaceSelector` | Labels on the Namespace |
| `resources.annotations` | Annotations |
| `subjects` | Users, groups, ServiceAccounts |
| `roles`, `clusterRoles` | The requester's roles |

Kinds can be written as `Kind`, `Version/Kind` or `Group/Version/Kind` (for example `networking.k8s.io/v1/NetworkPolicy`). Subresources use `/` or `.` (`Pods/status`).

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: example-selection
spec:
  background: false
  rules:
    - name: restrict-prod-pods
      match:
        any:
          - resources:
              kinds:
                - Pod
              operations:
                - CREATE
                - UPDATE
              namespaceSelector:
                matchLabels:
                  env: production
      exclude:
        any:
          - clusterRoles:
              - cluster-admin
          - subjects:
              - kind: User
                name: John
      validate:
        failureAction: Audit
        message: "Pods in production must set a team label."
        pattern:
          metadata:
            labels:
              team: "?*"
```

*Assembled from the filter fields and the exclude example on the match and exclude page; `?*` is the documented "non-empty value" wildcard. Not applied.*

Limits to know:

- `roles`, `clusterRoles` and `subjects` require `background: false`, because background scans have no requesting user.
- Wildcard kinds (`*`) cannot run in background mode, and do not support `generate` or `verifyImages`.
- Putting resource filters directly under `match` or `exclude` (without `any` or `all`) is deprecated.

**[📖 Match and exclude](https://kyverno.io/docs/policy-types/cluster-policy/match-exclude/)** - fields, kind formats, wildcards

---

## Common policy settings

Settings that sit under `spec`, with defaults from the policy settings page:

| Setting | Default | Meaning |
|---|---|---|
| `background` | `true` | Scan existing resources and produce reports. Set `false` for policies that use request-only data |
| `admission` | `true` | When `false`, the policy runs in background mode only |
| `applyRules` | `All` | `One` stops evaluating further rules after the first one applies |
| `failurePolicy` | `Fail` | What the API server does if the webhook does not respond: `Fail` or `Ignore`. Deprecated in 1.13; use `webhookConfiguration.failurePolicy` |
| `webhookTimeoutSeconds` | `10` (1 to 30) | Time allowed to apply the policy. Deprecated in 1.13; use `webhookConfiguration.timeoutSeconds` |
| `validationFailureAction` | `Audit` | Deprecated in 1.13; use `failureAction` under the validate rule |
| `useServerSideApply` | `false` | For generate rules; use server-side apply so field ownership is visible |

Notes the validate page adds:

- `emitWarning: true` shows audit-mode violations as admission warnings to the user.
- `failureActionOverrides` sets a different action per Namespace, only in ClusterPolicies. A common use is `Enforce` in production and `Audit` in dev.

A subtle one: `failurePolicy: Fail` plus an outage of Kyverno blocks matching requests. That is the safe-by-default choice for security rules, and the reason HA matters (note 02). The `forceFailurePolicyIgnore` flag exists for emergencies.

**[📖 Policy settings](https://kyverno.io/docs/policy-types/cluster-policy/policy-settings/)** - defaults and deprecations

---

## Key terms

- **match** - the rule block that selects which resources a rule evaluates.
- **exclude** - the rule block that removes resources from the matched set.
- **any / all** - logical OR and AND wrappers inside match, exclude and conditions.
- **operations** - the admission operations a rule applies to; CREATE and UPDATE when omitted.
- **namespaceSelector** - a label selector applied to the Namespace of a resource.
- **background** - the policy setting that enables scans of existing resources.
- **failurePolicy** - the setting that decides whether the API server proceeds when the webhook is unreachable.
- **applyRules** - the setting that decides whether all rules or only the first applying rule are evaluated.
- **failureActionOverrides** - a per-Namespace override of Audit or Enforce.
