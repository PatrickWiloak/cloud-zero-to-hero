---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 8 min
---

# CNPE High-Yield Scenarios

Each scenario is a task shaped like the performance-based exam: a situation, the steps you would take at the terminal, and the check that proves it worked.

---

## Scenario 1: Changes made with kubectl keep reverting

**Scenario**: A developer edits a Deployment with `kubectl edit` and the change disappears within minutes.

**Solution Pattern**:
- The workload is managed by Argo CD with `syncPolicy.automated.selfHeal: true` (or by a Flux Kustomization on an `interval`)
- Make the change in Git instead and let the agent reconcile
- If a temporary manual change is genuinely needed, suspend reconciliation deliberately (`suspend: true` on a Flux Kustomization) and resume afterwards

**Verify**: sync status shows the new revision; the live object matches Git.

**Key Takeaway**: Under GitOps, Git is the source of truth.

---

## Scenario 2: Namespace has a quota and Pods will not create

**Scenario**: A team's Deployment shows 0 of 3 ready. The Deployment itself was created fine.

**Solution Pattern**:
- `kubectl describe` the ReplicaSet and read the events: a ResourceQuota that covers CPU or memory rejects Pods that set no request or limit
- Add requests and limits to the Pod template, or add a LimitRange with defaults
- Check the quota's remaining headroom

**Verify**: Pods reach Running; the quota's used values rise.

**Key Takeaway**: Workload objects can exist while their Pods are blocked by quota.

---

## Scenario 3: Roll out a risky change progressively

**Scenario**: A payments service needs a canary: 10 percent, a pause, 20 percent, then a human decision.

**Solution Pattern**:
- Replace the Deployment with an Argo Rollouts `Rollout` using `canary.steps`: `setWeight: 10`, `pause: {duration: 1h}`, `setWeight: 20`, `pause: {}`
- `pause: {}` waits until `kubectl argo rollouts promote <rollout>`
- Or keep the Deployment and add a Flagger `Canary` with `stepWeight`, `maxWeight`, `threshold` and metric checks, so promotion and rollback are automatic

**Verify**: traffic weights follow the steps; a failing metric causes rollback (Flagger) or abort (Rollouts analysis).

**Key Takeaway**: Know both tools and when each wraps the workload.

---

## Scenario 4: Offer developers a database by YAML

**Scenario**: Developers should request a database with three fields and get a managed instance.

**Solution Pattern**:
- Define the API with a Crossplane `CompositeResourceDefinition` (group, names, versions, schema with `spec.region`, size, and so on; `referenceable: true` on the version Compositions use)
- Write a `Composition` in pipeline mode with `compositeTypeRef`, installing the needed `Function`
- Commit an instance of the composite resource to the GitOps repo; Argo CD or Flux applies it
- Read the XR's conditions, then the composed managed resources, when it does not become ready

**Verify**: the XR becomes Ready and the cloud resource exists.

**Key Takeaway**: API (XRD), recipe (Composition), request (XR), delivery (GitOps).

---

## Scenario 5: The alert never fires

**Scenario**: A latency alert is defined but nobody is paged during a slow period.

**Solution Pattern**:
- Check the Prometheus Alerts tab: is it pending? A `for` duration must elapse before firing
- Check the expression returns elements in the expression browser
- Check Prometheus is configured to send to Alertmanager and routes match the labels
- If it flaps, add `keep_firing_for`

**Verify**: the alert goes pending then firing; Alertmanager receives it.

**Key Takeaway**: Prometheus evaluates; Alertmanager delivers.

---

## Scenario 6: Require encrypted traffic between services

**Scenario**: Security requires that services in the `payments` namespace accept only mTLS traffic.

**Solution Pattern**:
- Istio: create a `PeerAuthentication` named `default` in the `payments` namespace with `mtls.mode: STRICT` and no selector
- Start from `PERMISSIVE` if some clients are not yet in the mesh, then tighten
- Linkerd: mTLS is on by default between meshed pods; non-meshed sources are accepted unless authorization policies disable it

**Verify**: a plaintext request from a non-mesh client is rejected under STRICT.

**Key Takeaway**: scope (mesh, namespace, workload, port) decides blast radius.

---

## Scenario 7: Block unlabelled namespaces, safely

**Scenario**: Governance wants every Namespace to carry an owner label. Existing namespaces may violate it.

**Solution Pattern**:
- Gatekeeper: a ConstraintTemplate plus a Constraint with `enforcementAction: dryrun` (or `warn`) first; read audit results for existing violations
- Kyverno: a validate rule in `Audit`, read the policy reports
- Fix violators, then switch to `deny` or `Enforce`

**Verify**: audit shows zero violations; a new unlabelled Namespace is rejected.

**Key Takeaway**: Observe, fix, then enforce.
