# Certified Cloud Native Platform Engineer (CNPE) - Practice Questions

30 original questions for CNPE prep, spread across the domains in proportion to their weights.

> **Cert page:** [exams/kubernetes/cnpe/](../../exams/kubernetes/cnpe/)

---

### Question 1
**Scenario:** An Argo CD Application has syncPolicy.automated with prune: true and selfHeal: true. A developer deletes a manifest from Git and also edits a live Deployment with kubectl. What happens?

A. The deleted manifest stays in the cluster and the live edit is kept
B. Both changes are kept, and the Application shows OutOfSync until someone syncs manually
C. Argo CD pauses auto-sync until the live edit is committed to Git
D. The resource removed from Git is deleted, and the live edit is reverted to the Git state

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** prune deletes resources that were removed from Git and selfHeal corrects drift made in the cluster. Without automated sync the Application would simply show OutOfSync.
</details>

---

### Question 2
**Scenario:** Which Argo CD Application field names the Git revision to deploy?

A. spec.destination.revision
B. spec.project.revision
C. spec.source.targetRevision
D. spec.syncPolicy.syncOptions

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** source holds repoURL, targetRevision and path. destination holds the cluster and namespace.
</details>

---

### Question 3
**Scenario:** In Flux, what does a Kustomization use to find the manifests it should apply?

A. A repoURL field inside the Kustomization
B. sourceRef pointing at a source such as a GitRepository
C. A webhook that pushes manifests to the controller
D. An Argo CD Application reference

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A Kustomization does not fetch code itself; sourceRef names a source (GitRepository, OCIRepository, Bucket) whose artifact it builds at path.
</details>

---

### Question 4
**Scenario:** A Flux Kustomization sets targetNamespace: apps, but the namespace does not exist. What happens?

A. Flux creates the namespace automatically
B. The apply fails because the controller does not create the namespace
C. The Kustomization falls back to the default namespace
D. The namespace is created only when prune is true

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** targetNamespace must already exist or be defined in the manifests. Argo CD's CreateNamespace=true is a different tool's option.
</details>

---

### Question 5
**Scenario:** What does dependsOn do on a Flux Kustomization?

A. Waits until the listed Kustomizations are Ready before applying
B. Copies resources from another Kustomization
C. Orders manifests inside one directory
D. Makes the Kustomization read-only

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** dependsOn is a list of other Kustomizations that must be Ready first; circular dependencies must be avoided.
</details>

---

### Question 6
**Scenario:** In a Tekton Pipeline, which field orders two Tasks when no data passes between them?

A. finally
B. workspaces
C. results
D. runAfter

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** runAfter adds ordering without passing data. finally tasks run after all others and cannot use runAfter.
</details>

---

### Question 7
**Scenario:** Which Tekton resource starts a Pipeline and supplies parameter values?

A. TaskRun
B. Task
C. PipelineRun
D. ClusterTask

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A PipelineRun starts a Pipeline at runtime and passes params. A TaskRun records the execution of a Task.
</details>

---

### Question 8
**Scenario:** A notification must be sent whether or not earlier Tasks succeed. Which Tekton construct fits?

A. runAfter
B. results
C. finally
D. retries

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** finally Tasks run in parallel after all tasks finish, whether they succeeded or failed.
</details>

---

### Question 9
**Scenario:** An Argo Rollouts canary has steps setWeight: 10, pause: {}, setWeight: 50. What happens after the first step?

A. It pauses for ten seconds and continues
B. The rollout pauses until it is promoted manually
C. It aborts and rolls back
D. It jumps straight to 100 percent

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** pause with no duration waits until manual promotion, for example kubectl argo rollouts promote <rollout>. A pause with a duration resumes automatically.
</details>

---

### Question 10
**Scenario:** How does Flagger perform a canary on an existing Deployment?

A. A Canary resource targets it; Flagger creates a primary Deployment and shifts traffic by stepWeight up to maxWeight, checking metrics
B. It replaces the Deployment kind with a Rollout
C. It edits the Deployment image tag directly in Git
D. It scales the Deployment to zero and waits

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Flagger creates a <name>-primary Deployment for the stable version and Services for primary and canary, analyses on each interval and rolls back when failed checks reach threshold.
</details>

---

### Question 11
**Scenario:** In a Flagger Canary, what does threshold control?

A. The maximum traffic percentage sent to the canary
B. How often the analysis runs
C. The number of replicas of the primary
D. How many failed metric checks are allowed before rollback

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** threshold is the number of failed checks allowed. maxWeight is the traffic ceiling and interval sets the analysis frequency.
</details>

---

### Question 12
**Scenario:** What must a CRD's metadata.name look like?

A. <kind>.<version>
B. <singular>-<group>
C. Any DNS-valid name
D. <plural>.<group>

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The name must match the spec fields, in the form <plural>.<group>, for example crontabs.stable.example.com.
</details>

---

### Question 13
**Scenario:** A CRD defines two versions. How many may be the storage version?

A. One per served version
B. Any number
C. Exactly one
D. None; storage is chosen by the API server

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** One and only one version must be marked storage: true.
</details>

---

### Question 14
**Scenario:** What happens to existing custom objects when their CRD is deleted?

A. They are kept but become read-only
B. They are deleted with it
C. They are migrated to a ConfigMap
D. They are kept and served from etcd

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Deleting the CRD removes the endpoint and all custom objects stored under it. Recreating the CRD starts empty.
</details>

---

### Question 15
**Scenario:** Which describes a Kubernetes operator?

A. A custom resource definition paired with a controller that acts on those resources
B. A cluster role with permission to edit any resource
C. A Helm chart repository
D. An admission webhook that blocks invalid objects

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Operators are clients of the Kubernetes API that act as controllers for a custom resource; typically a CRD plus a Deployment running the controller.
</details>

---

### Question 16
**Scenario:** In Crossplane, which resource defines the schema of a custom API such as AcmeBucket?

A. CompositeResourceDefinition (XRD)
B. Composition
C. Function
D. ProviderConfig

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The XRD defines the schema. A Composition says which resources to create for it, and a composite resource (XR) is an instance.
</details>

---

### Question 17
**Scenario:** A Crossplane Composition function returns only the resource it generated and omits other desired state it received. What is the consequence?

A. Crossplane merges the missing resources back automatically
B. The composite resource becomes read-only
C. Nothing; omitted resources are kept
D. Crossplane deletes the resources the function omitted

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Functions must copy forward all desired state they receive; otherwise Crossplane deletes the resources they omitted.
</details>

---

### Question 18
**Scenario:** Which Composition setting runs a list of functions in order?

A. mode: Resources with a base field
B. mode: Direct
C. mode: Pipeline with pipeline steps
D. mode: Sequential

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A Composition sets mode: Pipeline and lists steps; each has a step name, functionRef.name and optional input, and each function receives the previous function's result.
</details>

---

### Question 19
**Scenario:** A HorizontalPodAutoscaler targeting CPU utilization shows unknown metrics. Which causes should you check first?

A. The HPA is in the wrong namespace than the Service
B. Metrics Server is installed and the Pods set CPU requests
C. The Deployment has too many replicas
D. The cluster uses IPv6

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Resource metrics come from Metrics Server via metrics.k8s.io, and utilization is a percentage of the container's request, so no request means no action.
</details>

---

### Question 20
**Scenario:** A ResourceQuota covers requests.cpu. A new Pod omits CPU requests and limits. What is the likely result?

A. The Pod is admitted with zero CPU
B. The Pod is rejected unless a LimitRange supplies defaults
C. The quota is ignored for that Pod
D. The Pod is scheduled on any node regardless of quota

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** When a quota covers cpu or memory, every new Pod must set a request or limit; a LimitRange can provide defaults.
</details>

---

### Question 21
**Scenario:** In a Prometheus alerting rule, what does the for field do?

A. Keeps the alert pending until the condition has held that long
B. Sets how often the expression is evaluated
C. Keeps the alert firing after the condition stops
D. Selects the Alertmanager receiver

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** for delays firing; keep_firing_for keeps an alert firing afterwards. Without for the alert fires on first evaluation.
</details>

---

### Question 22
**Scenario:** Which component sends alert notifications to receivers such as email or chat?

A. Prometheus itself
B. Grafana panels
C. Node exporter
D. Alertmanager

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Prometheus evaluates rules and sends alert state to Alertmanager, which handles grouping, rate limiting, silencing and delivery.
</details>

---

### Question 23
**Scenario:** Which of these is a DORA instability metric?

A. Deployment frequency
B. Change lead time
C. Change fail rate
D. Failed deployment recovery time

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** DORA groups change fail rate and deployment rework rate under instability; lead time, frequency and failed deployment recovery time are throughput.
</details>

---

### Question 24
**Scenario:** Which Istio resource requires mutual TLS for incoming connections in a namespace?

A. AuthorizationPolicy with action: ALLOW
B. DestinationRule with tls.mode: SIMPLE
C. PeerAuthentication with mtls.mode: STRICT
D. Gateway with tls.mode: PASSTHROUGH

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** PeerAuthentication sets mTLS requirements for incoming connections; a policy without a selector in a namespace applies to that whole namespace.
</details>

---

### Question 25
**Scenario:** Which Istio PeerAuthentication mode accepts both plaintext and mTLS traffic?

A. STRICT
B. PERMISSIVE
C. DISABLE
D. UNSET only

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** PERMISSIVE accepts either, which makes it the usual stepping stone to STRICT. UNSET inherits from the parent scope and acts as PERMISSIVE if there is none.
</details>

---

### Question 26
**Scenario:** What does Linkerd do by default for traffic between meshed pods?

A. Enables mTLS for TCP traffic automatically, with proxy certificates that rotate every 24 hours
B. Leaves traffic in plaintext until a policy is applied
C. Encrypts only HTTP traffic
D. Requires manually issued certificates for each pod

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Linkerd enables mTLS for all TCP traffic between meshed pods; the default trust anchor from linkerd install expires after 365 days and must be rotated.
</details>

---

### Question 27
**Scenario:** RBAC in Kubernetes is described how?

A. Deny rules take precedence over allow rules
B. Roles can be bound only to users, never ServiceAccounts
C. ClusterRoles can be bound only cluster-wide
D. Permissions are purely additive; there are no deny rules

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** RBAC permissions are additive. A RoleBinding can reference a ClusterRole to reuse it within one namespace.
</details>

---

### Question 28
**Scenario:** Which audit level records the request body but not the response body?

A. Metadata
B. RequestResponse
C. None
D. Request

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Metadata logs no bodies, Request adds the request body, RequestResponse adds both, and the first matching rule in the policy sets the level.
</details>

---

### Question 29
**Scenario:** What is the default enforcementAction of a Gatekeeper Constraint?

A. warn
B. dryrun
C. deny
D. audit

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** enforcementAction is deny by default; dryrun and warn are also supported, which helps with staged rollouts.
</details>

---

### Question 30
**Scenario:** You want to produce an SBOM for a container image with Trivy in CycloneDX format. Which command fits?

A. trivy sbom --create IMAGE
B. trivy image --format cyclonedx --output result.json IMAGE
C. trivy image --sbom-only --xml IMAGE
D. trivy fs --format cyclonedx-xml IMAGE

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Trivy supports CycloneDX and SPDX via --format; XML CycloneDX output is not supported, and vulnerability data needs --scanners vuln.
</details>

---
