---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 25 min
---

# 05 - Writing Policies

**Domain 5: Writing Policies (32%)**

Curriculum topics, in order: Validation Rules, Preconditions, Background Scans, Mutation Rules, Generation Rules, VerifyImage Rules, Variables & API Calls in Policies, JSON Patches, Autogen Rules, Cleanup Policies, Common Expression Language (CEL).

This is a third of the exam. Study it hardest. YAML in this note was syntax-checked with a YAML parser; none of it was applied to a cluster or run through the Kyverno CLI.

---

## Validation rules

A validate rule checks a resource and either blocks it or reports it. Every rule has a **`message`** (shown to the user on failure) and one of these checks.

### pattern

A pattern is an overlay of the desired state. Fields must exist and match; fields you do not mention are ignored. Wildcards: `*` matches zero or more characters, `?` one character, `?*` a non-empty value. Operators include `>=`, `|`, `&`, ranges with `-`, and `!`.

**Anchors** add conditions inside a pattern:

| Anchor | Syntax | Meaning |
|---|---|---|
| Conditional | `(field)` | Only check the sibling fields if this field exists and matches |
| Equality | `=(field)` | If the field exists, it must match |
| Existence | `^(list)` | At least one list element must match |
| Negation | `X(field)` | The field must not exist |
| Global | `<(field)` | If the condition is true, the rest of the pattern is applied |

### anyPattern

A logical OR across a list of patterns: the resource passes if it matches any one. A rule cannot declare both `pattern` and `anyPattern`.

```yaml
validate:
  failureAction: Enforce
  message: 'Running as root is not allowed.'
  anyPattern:
    - spec:
        securityContext:
          runAsNonRoot: true
    - spec:
        containers:
          - securityContext:
              runAsNonRoot: true
```

### deny with conditions

`deny` blocks when its conditions are true. Conditions use `key`, `operator` and `value`, nested under `any` or `all`. This policy (from the docs) blocks deletes of Kyverno-managed resources except by cluster-admins:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: deny-deletes
spec:
  background: false
  rules:
    - name: block-deletes-for-kyverno-resources
      match:
        any:
          - resources:
              selector:
                matchLabels:
                  app.kubernetes.io/managed-by: kyverno
      exclude:
        any:
          - clusterRoles:
              - cluster-admin
      validate:
        failureAction: Enforce
        message: 'Deleting {{request.oldObject.kind}}/{{request.oldObject.metadata.name}} is not allowed'
        deny:
          conditions:
            any:
              - key: '{{request.operation}}'
                operator: Equals
                value: DELETE
```

Pattern says what good looks like; deny says what bad looks like. Use deny when you cannot express the rule as a shape (for example, "any DELETE").

### foreach

Iterates over a list with a JMESPath expression (written without braces). Each iteration exposes the current item as `element`.

```yaml
validate:
  failureAction: Enforce
  message: 'unknown registry'
  foreach:
    - list: 'request.object.spec.containers'
      pattern:
        image: 'trusted-registry.io/*'
```

### Other validate subrules

- **`podSecurity`** applies a Pod Security Standards profile (`baseline` or `restricted`) with a `version`, optionally excluding controls.
- **`manifests`** verifies Sigstore signatures on YAML manifests.
- **`cel`** uses Common Expression Language (see the CEL section).

**[📖 Validate rules](https://kyverno.io/docs/policy-types/cluster-policy/validate/)** - patterns, anchors, deny, foreach, podSecurity

---

## Preconditions

A **precondition** is an extra gate checked **after** a resource has matched. It can test fields, context variables and JMESPath expressions, which `match` and `exclude` cannot do. Syntax is `any` (OR) and/or `all` (AND), with `key`, `operator`, `value`.

Operators: `Equals`, `NotEquals`; set operators `AnyIn`, `AllIn`, `AnyNotIn`, `AllNotIn`; numeric and quantity comparisons `GreaterThan`, `GreaterThanOrEquals`, `LessThan`, `LessThanOrEquals`; and duration versions (`DurationGreaterThan` and so on).

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: any-all-preconditions
spec:
  background: false
  rules:
    - name: any-all-rule
      match:
        any:
          - resources:
              kinds:
                - Deployment
      preconditions:
        any:
          - key: "{{ request.object.metadata.labels.color || '' }}"
            operator: Equals
            value: blue
          - key: "{{ request.object.metadata.labels.app || '' }}"
            operator: Equals
            value: busybox
      validate:
        failureAction: Enforce
        message: 'Busybox must be used based on this label combination.'
        pattern:
          spec:
            template:
              spec:
                containers:
                  - name: '*busybox*'
```

Two exam points:

1. **Preconditions do not block.** The docs say they "do not produce a blocking effect similar to deny rules." If they fail, the rule is not applicable, and a report records `skip`.
2. **The `|| ''` fallback** keeps a missing optional field from raising an error.

**[📖 Preconditions](https://kyverno.io/docs/policy-types/cluster-policy/preconditions/)** - any/all, operators, skip behavior

---

## Background scans

Background mode checks resources that **already exist**. It is controlled by `spec.background` (default `true`) and produces policy reports. Facts from the reports page:

- Scans run periodically, once per hour by default (`backgroundScanInterval`).
- They check `validate` and `verifyImages` rules.
- They never block anything, even in `Enforce` mode.
- `background: false` turns scanning off for a policy.

Policies that use **request-only data** must set `background: false`, because there is no request in a scan. That covers `request.userInfo`, roles, ServiceAccount variables, and `subjects`, `roles` and `clusterRoles` in match. The variables page says the role and ServiceAccount variables are unavailable when `background: true`.

---

## Mutation rules

Mutation changes a resource before validation. Mutate rules use `patchStrategicMerge` or `patchesJson6902`. Kubernetes blocks changes to `name`, `namespace`, `uid`, `kind` and `apiVersion`.

### patchStrategicMerge and anchors

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: set-image-pull-policy
spec:
  rules:
    - name: set-image-pull-policy
      match:
        any:
          - resources:
              kinds:
                - Pod
      mutate:
        patchStrategicMerge:
          spec:
            containers:
              # match images which end with :latest
              - (image): '*:latest'
                imagePullPolicy: 'IfNotPresent'
```

Mutation anchors:

| Anchor | Behavior |
|---|---|
| `()` conditional | Applies only if the tag exists and matches the value |
| `+()` add if not present | Adds the field only if it is missing |
| `<()` global | When the condition is true, applies the rest of the pattern |

Conditional anchors are evaluated first; plain fields and `+()` fields apply afterwards. Conditional anchors work only with `patchStrategicMerge`.

```yaml
mutate:
  patchStrategicMerge:
    spec:
      securityContext:
        +(runAsNonRoot): true
        +(runAsUser): 1000
```

`+(...)` sets a default but never overrides a value the user already chose.

### foreach in mutation

Applies a patch to each element of a list, with `element` available (and `elementIndex` for JSON patches).

### Mutate existing

Mutate rules normally touch the resource in the request. **Mutate existing** changes resources already in the cluster: the trigger is defined in `match`, the objects to change in `mutate.targets`. The background controller applies it asynchronously and often needs extra RBAC (note 02). `mutateExistingOnPolicyUpdate: true` also runs it when the policy is created or updated, and then `targets` is required. Omitting `name` or `namespace` in a target acts as a wildcard, so set them explicitly.

**[📖 Mutate rules](https://kyverno.io/docs/policy-types/cluster-policy/mutate/)** - anchors, foreach, mutate existing, targets

---

## JSON patches

`patchesJson6902` uses RFC 6902 operations (`add`, `replace`, `remove`) with JSON Pointer paths. It does not support conditional anchors, so use preconditions instead.

```yaml
mutate:
  patchesJson6902: |-
    - path: "/metadata/labels/purpose"
      op: remove
```

Path details from the docs: append to an array by ending the path with `/-`; escape `/` in a key as `~1` and `~` as `~0`. Variables are not supported in `patchesJson6902.path`.

When to choose which: `patchStrategicMerge` reads like the resource and supports anchors; `patchesJson6902` is exact and can remove fields, which a merge patch cannot do cleanly.

---

## Generation rules

Generate rules create new resources in response to events, such as creating a Namespace.

| Source | Meaning |
|---|---|
| `data` | The downstream resource's contents are written in the rule |
| `clone` | Copy one existing resource (Kyverno does not modify the content) |
| `cloneList` | Copy several kinds from one source Namespace, optionally filtered by `selector` |

`data` and `clone` are mutually exclusive in a rule.

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: default
spec:
  rules:
    - name: deny-all-traffic
      match:
        any:
          - resources:
              kinds:
                - Namespace
      generate:
        kind: NetworkPolicy
        apiVersion: networking.k8s.io/v1
        name: deny-all-traffic
        namespace: '{{request.object.metadata.name}}'
        data:
          spec:
            podSelector: {}
            policyTypes:
              - Ingress
              - Egress
```

**`synchronize: true`** keeps the downstream resource tied to its source: manual edits are reverted, source changes propagate, and if the trigger is deleted the downstream resource is deleted.

| Action | Data source, sync | Clone source, sync |
|---|---|---|
| Delete downstream | Recreated | Recreated |
| Delete rule or policy | Deleted unless orphaned | Retained |
| Delete source | Not applicable | Downstream deleted |
| Delete trigger | Downstream deleted | Downstream deleted |

- **`orphanDownstreamOnPolicyDelete`** (default `false`, data source with sync): `true` keeps downstream resources when the policy goes away.
- **`generateExisting: true`** also applies the rule to resources that already exist when the policy is created. It now lives under `rules[*].generate`; `spec.generateExisting` is deprecated.
- **RBAC.** The background controller needs permissions for whatever it generates. For RoleBindings, Kubernetes anti-escalation means the controller must already hold the permissions it grants.

**[📖 Generate rules](https://kyverno.io/docs/policy-types/cluster-policy/generate/)** - data, clone, synchronize, generateExisting

---

## VerifyImage rules

`verifyImages` checks image signatures and attestations (supply chain security). Supported signature types are Sigstore Cosign and Notary.

| Attribute | Default | Meaning |
|---|---|---|
| `imageReferences` | none | Image patterns to match (static values only, no variables) |
| `required` | `true` | Matching images must carry the verified marker |
| `mutateDigest` | `true` | Rewrites tags to digests so the reference is immutable |
| `verifyDigest` | `true` | Checks matching images use digests |
| `attestors` | none | Who must have signed; `count` sets how many entries must verify |
| `attestations` | none | Signed metadata checked with `conditions` on its JSON |

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-images-production
spec:
  rules:
    - name: verify-image
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages:
        - imageReferences:
            - 'registry.example.com/production/*'
          attestors:
            - entries:
                - keys:
                    publicKeys: |
                      -----BEGIN PUBLIC KEY-----
                      ...
                      -----END PUBLIC KEY-----
```

*Adapted from the docs example (the docs version also sets `imageRegistryCredentials`, which needs Kyverno 1.18 for namespaced secrets).*

Execution order: the mutation webhook runs the rule after other mutation rules and before validation, so the digest can be inserted; the validation webhook re-runs the `required` and `verifyDigest` checks. Successful verifications are cached by default with a 60-minute TTL (maximum 1000 keys), so changes in the registry are not seen until the entry expires.

**[📖 verifyImages rules](https://kyverno.io/docs/policy-types/cluster-policy/verify-images/)** - attributes, order, cache

---

## Variables and API calls

Variables are written `{{ ... }}` and hold JMESPath. Built-ins from the variables page:

- `request.object`, `request.oldObject`, `request.operation`, `request.namespace`, `request.userInfo`
- `serviceAccountName`, `serviceAccountNamespace`, `request.roles`, `request.clusterRoles`
- `images` (registry, path, name, tag, digest, reference, referenceWithTag)

Evaluation order: **match, then context, then preconditions, then the rule body.** Variables are not supported in `match`, `exclude` or `patchesJson6902.path`. Escape with a leading backslash to stop substitution. `$( ... )` references another field inside the same policy.

### context: where outside data comes from

Declared under a rule's `context:` and evaluated in order (a later entry can use an earlier one).

| Type | Source |
|---|---|
| `variable` | A value or JMESPath expression, with optional `default` |
| `configMap` | A ConfigMap, read at evaluation time |
| `apiCall` | The Kubernetes API (`urlPath`) or an external service (`service`), optionally with `method`, `data`, `jmesPath`, `default` |
| `imageRegistry` | OCI image metadata for a reference |
| `globalReference` | A cluster-wide `GlobalContextEntry` cache |

```yaml
context:
  - name: podCount
    apiCall:
      urlPath: '/api/v1/namespaces/{{request.namespace}}/pods'
      jmesPath: 'items | length(@)'
```

`service` and `urlPath` are mutually exclusive, and service responses must be JSON. A `GlobalContextEntry` wraps either a `kubernetesResource` (kept current by informers) or an `apiCall` fetched every `refreshInterval` (can be stale between refreshes). Labeling a ConfigMap `cache.kyverno.io/enabled: "true"` caches it to reduce API server calls.

**[📖 Variables](https://kyverno.io/docs/policy-types/cluster-policy/variables/)** - built-ins, JMESPath, escaping

**[📖 External data sources](https://kyverno.io/docs/policy-types/cluster-policy/external-data-sources/)** - configMap, apiCall, imageRegistry, globalReference

---

## Autogen rules

Most people write policies for Pods, but Pods are rarely created directly. **Autogen** takes a rule written for Pods and generates equivalent rules for the controllers that create them: Deployment, DaemonSet, StatefulSet, Job and CronJob (and ReplicaSet and ReplicationController).

- Generated rules are prefixed `autogen-`; the CronJob version is `autogen-cronjob-` because its Pod template sits under `jobTemplate`.
- The annotation `pod-policies.kyverno.io/autogen-controllers` chooses which controllers: `Deployment,Job` limits it, `none` disables it.
- Autogen is **skipped** if `match` or `exclude` uses `names`, `selector` or `annotations`, if the kinds are broader than Pod, and for Pod mutate rules that use a JSON patch.
- Patterns on Pod metadata, such as `metadata.namespace`, translate wrongly into the template; disable autogen and write explicit rules.

This is why a PolicyException must list autogenerated rule names as well as the original (note 06).

**[📖 Autogen rules](https://kyverno.io/docs/policy-types/cluster-policy/autogen/)** - controllers, annotation, limitations

---

## Cleanup policies

Cleanup deletes resources on a schedule. `CleanupPolicy` (namespaced) and `ClusterCleanupPolicy` (cluster-scoped) have `match`/`exclude`, optional `conditions` (referencing the resource as `target.*`), and a cron `schedule`.

```yaml
apiVersion: kyverno.io/v2
kind: ClusterCleanupPolicy
metadata:
  name: cleandeploy
spec:
  match:
    any:
      - resources:
          kinds:
            - Deployment
          selector:
            matchLabels:
              canremove: 'true'
  conditions:
    any:
      - key: '{{ target.spec.replicas }}'
        operator: LessThan
        value: 2
  schedule: '*/5 * * * *'
```

- `subjects`, `roles` and `clusterRoles` are not allowed in match; `operations` is ignored because only the schedule triggers cleanup.
- `deletionPropagationPolicy` accepts `Foreground`, `Background` or `Orphan`.
- The cleanup controller follows least privilege and may need extra RBAC (note 02).
- **TTL label:** add `cleanup.kyverno.io/ttl` to any resource Kyverno can delete, with an ISO 8601 time or a relative duration like `5m`, `4h`, `1d`, and it is deleted with no policy at all. The check interval is the `ttlReconciliationInterval` flag, default `1m`.
- **Deprecation:** the docs say `CleanupPolicy` and `ClusterCleanupPolicy` are deprecated as of v1.19 and will be removed in v1.20; the CEL-based **DeletingPolicy** (`policies.kyverno.io/v1`, with `schedule`, `matchConstraints`, `conditions`, `deletionPropagationPolicy`) replaces them.

**[📖 Cleanup policies](https://kyverno.io/docs/policy-types/cleanup-policy/)** - schedule, TTL label, deprecation

---

## Common Expression Language (CEL)

CEL is the expression language Kubernetes itself uses for ValidatingAdmissionPolicy. Kyverno supports it two ways.

**1. Inside a classic rule: `validate.cel`.** A false expression triggers the failure action. Variables include `object`, `oldObject`, `request`, `params`, `namespaceObject` and `authorizer`. Kyverno can generate Kubernetes ValidatingAdmissionPolicies from `cel` rules.

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-deployment-replicas
spec:
  background: false
  rules:
    - name: check-deployment-replicas
      match:
        any:
          - resources:
              kinds:
                - Deployment
      validate:
        failureAction: Enforce
        cel:
          expressions:
            - expression: 'object.spec.replicas < 4'
              message: 'Deployment spec.replicas must be less than 4.'
```

**2. As dedicated policy types** in `policies.kyverno.io/v1`, marked Stable in v1.19 in the docs for `ValidatingPolicy`, `MutatingPolicy`, `ImageValidatingPolicy` and `DeletingPolicy`:

```yaml
apiVersion: policies.kyverno.io/v1
kind: ValidatingPolicy
metadata:
  name: check-labels
spec:
  validationActions:
    - Deny
  matchConstraints:
    resourceRules:
      - apiGroups: ['']
        apiVersions: [v1]
        operations: [CREATE, UPDATE]
        resources: [pods]
  validations:
    - message: label 'environment' is required
      expression: "'environment' in object.metadata.?labels.orValue([])"
```

Mapping between the two worlds:

| Classic (`kyverno.io/v1`) | CEL type (`policies.kyverno.io/v1`) |
|---|---|
| `validate` rule, `Enforce` or `Audit` | `ValidatingPolicy`, `validationActions: [Deny]` or `[Audit]` |
| `mutate` rule | `MutatingPolicy`, `patchType: ApplyConfiguration` or `JSONPatch` |
| `verifyImages` | `ImageValidatingPolicy` |
| `CleanupPolicy` | `DeletingPolicy` |
| `match` / `exclude` | `matchConstraints` and `matchConditions` |

`ValidatingPolicy` also has `variables` (named CEL expressions), `evaluation.background.enabled` and `evaluation.admission.enabled`, and `webhookConfiguration.timeoutSeconds` (default 10, range 1 to 30).

**[📖 ValidatingPolicy](https://kyverno.io/docs/policy-types/validating-policy/)** - fields, example, status

**[📖 MutatingPolicy](https://kyverno.io/docs/policy-types/mutating-policy/)** - ApplyConfiguration, JSONPatch, mutateExisting

**[📖 DeletingPolicy](https://kyverno.io/docs/policy-types/deleting-policy/)** - scheduled deletion in CEL

---

## Key terms

- **Pattern** - an overlay describing the desired resource shape, checked field by field.
- **Anchor** - a decorated field name such as `(field)`, `+(field)` or `<(field)` that adds a condition or default behavior.
- **anyPattern** - a list of patterns where matching any one passes.
- **deny** - a validate form that blocks the request when its conditions evaluate to true.
- **foreach** - a loop over a JMESPath list that exposes each item as `element`.
- **Precondition** - an extra check after matching that decides whether a rule applies; it never blocks by itself.
- **patchStrategicMerge** - a mutation method that merges a partial resource into the request.
- **patchesJson6902** - a mutation method using RFC 6902 add, replace and remove operations.
- **Mutate existing** - a mutate rule that changes resources already in the cluster, using `targets`.
- **synchronize** - a generate setting that keeps the downstream resource in line with its source.
- **cloneList** - a generate source that copies several kinds from one Namespace.
- **verifyImages** - a rule type that checks image signatures and attestations.
- **Attestor** - the entity (key, certificate or keyless identity) whose signature must verify.
- **Context** - rule-level declarations that load outside data into variables.
- **GlobalContextEntry** - a cluster-wide cache of resources or API results that policies reference by name.
- **Autogen** - automatic generation of Pod-controller rules from a Pod rule.
- **TTL label** - the `cleanup.kyverno.io/ttl` label that deletes a resource after a time.
- **CEL** - Common Expression Language, used in ValidatingAdmissionPolicy and Kyverno's newer policy types.
- **ValidatingPolicy** - the CEL-based validating policy type in `policies.kyverno.io/v1`.
- **DeletingPolicy** - the CEL-based scheduled deletion policy type that replaces cleanup policies.
