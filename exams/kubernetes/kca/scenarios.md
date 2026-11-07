---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 7 min
---

# KCA High-Yield Scenarios

---

## Scenario 1: Roll out a new guardrail safely

**Scenario**: The platform team wants to require a `team` label on every Pod. Hundreds of Pods already exist, and teams ship all day.

**Solution Pattern**:
- Install the policy with the validate action set to `Audit`
- Let the background scan run (hourly by default) and read `kubectl get policyreport -A` for `fail` results
- Have teams fix their manifests, or write PolicyExceptions for justified cases
- Switch to `Enforce` once the failures are gone; optionally use `failureActionOverrides` to keep non-production Namespaces in Audit

**Common Distractors**:
- Install in Enforce and expect existing Pods to be removed (admission does not touch existing objects)
- Rely on Enforce to produce reports of existing resources (scans report them, but never block)

**Key Takeaway**: Audit first, read the reports, then Enforce.

---

## Scenario 2: A policy works on Pods but not on Deployments

**Scenario**: A rule written for `Pod` blocks bare Pods, yet a Deployment with the same bad template is admitted.

**Solution Pattern**:
- Admission checks the Deployment object itself, and Pods are created later by the ReplicaSet
- Autogen normally creates `autogen-` rules for Deployment, DaemonSet, StatefulSet, Job and CronJob
- Check whether autogen was disabled by `pod-policies.kyverno.io/autogen-controllers: none` or skipped because `match` or `exclude` uses `names`, `selector` or `annotations`
- Remove the blocker or write explicit controller rules

**Key Takeaway**: Autogen explains most "works on Pods only" questions, and its skip conditions explain the rest.

---

## Scenario 3: A new Namespace needs defaults

**Scenario**: Every new Namespace should get a default-deny NetworkPolicy and a copy of the `regcred` pull Secret. Someone edits the NetworkPolicy by hand in one Namespace.

**Solution Pattern**:
- Use a `generate` rule matching `Namespace`, with `data` for the NetworkPolicy and `clone` for the Secret
- Set `synchronize: true` so manual edits are reverted and source changes propagate
- Ensure the background controller has RBAC for the kinds it generates
- Use `generateExisting: true` (under the rule) to cover Namespaces that already exist

**Key Takeaway**: data or clone, synchronize for drift control, background controller RBAC.

---

## Scenario 4: One Pod needs to break the rule

**Scenario**: A vendor monitoring agent legitimately needs `hostNetwork`. The policy blocks it for everyone.

**Solution Pattern**:
- Do not weaken the policy
- Enable exceptions with `enablePolicyException=true` and `exceptionNamespace=<ns>`
- Create a PolicyException naming the policy and its rules, including `autogen-` rule names, with a `match` limited to that agent
- Confirm the report shows `skip` for that Pod

**Common Distractors**:
- Add the Namespace to the policy's `exclude` for all time (broader than needed and hidden in the policy)
- Create the exception in any Namespace (honored only in the configured exception Namespace)

**Key Takeaway**: narrow, auditable exception; do not forget the autogen rule names.

---

## Scenario 5: Admission is slow and a Kyverno outage blocks deploys

**Scenario**: Deploys fail with webhook timeouts when the single Kyverno admission Pod restarts.

**Solution Pattern**:
- Run the admission controller with three replicas (HA is per controller; background, reports and cleanup are separate Deployments)
- Remember `failurePolicy: Fail` means no webhook response blocks matching requests
- Check `webhookTimeout` (default 10, range 1 to 30) and slow `apiCall` context entries
- Watch `kyverno_admission_review_duration_seconds` to see latency

**Key Takeaway**: HA replicas, failure policy, and metrics together.

---

## Scenario 6: Pipeline gate before merge

**Scenario**: Platform wants manifests rejected in CI before they reach the cluster.

**Solution Pattern**:
- Install the Kyverno CLI in the pipeline
- Run `kyverno apply policies/ --resource manifests/`
- Add `kyverno test .` with a passing and a failing resource for every rule
- Use `-f` or `--set` for variables, and `-u` to simulate a user for role-based rules

**Key Takeaway**: `apply` for real manifests, `test` for the policies themselves.
