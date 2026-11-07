# Kyverno Certified Associate (KCA) - Practice Questions

32 original questions for KCA prep, weighted toward Writing Policies (32%) and spread across the other five domains.

> **Cert page:** [exams/kubernetes/kca/](../../exams/kubernetes/kca/)

---

### Question 1
**Scenario:** A team installs a new ClusterPolicy with the validate action set to Enforce. Thousands of Pods already exist that violate it. What happens to those existing Pods?

A. They are deleted by the background controller on its next hourly cycle because Enforce policies remediate violations
B. They are evicted by the kubelet once the webhook configuration is updated to include the new policy
C. They are paused until each owner adds a PolicyException for the violated rule in the exception namespace
D. They remain running; admission applies to new and changed requests, and the background scan only reports them

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Admission controllers act when objects are created, updated or deleted. Background scans check existing resources and write results to policy reports, but they never block or remove anything, even in Enforce mode.
</details>

---

### Question 2
**Scenario:** Which statement about Kubernetes admission control is correct?

A. Validating admission runs first so that invalid objects never reach the mutating webhooks
B. Admission also intercepts get, list and watch requests, which is how policies hide resources
C. Mutating admission runs first, then validating admission, and a rejection in either phase rejects the whole request
D. Admission runs before authentication so that anonymous requests can be rejected by policy

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The Kubernetes docs describe two phases, mutating then validating. Admission runs after authentication and authorization, and it does not intercept reads such as get, list or watch.
</details>

---

### Question 3
**Scenario:** What is a Kyverno rule?

A. A cluster-wide setting stored in the kyverno ConfigMap that controls all policies
B. One named unit inside a policy, with a match block and one of validate, mutate, generate or verifyImages
C. A custom resource that stores the result of evaluating a policy against one resource
D. A separate Deployment that runs one controller of the Kyverno installation

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A policy holds one or more rules in spec.rules. Each rule names itself, selects resources with match and exclude, and has one rule type body.
</details>

---

### Question 4
**Scenario:** What advantage do tags and digests give to image references, and why does verifyImages default mutateDigest to true?

A. A digest can be moved to different content while a tag cannot, so tags are safer for production
B. A tag can be moved to different content while a digest cannot, so rewriting tags to digests makes the reference immutable
C. Tags and digests are identical in meaning; the rewrite only shortens the reference for logging
D. Digests are required by the Kubernetes API, so Pods with tags are rejected without the rewrite

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A digest is a content hash. A tag is a movable label. Converting a verified tag to a digest means the exact verified image is the one that runs.
</details>

---

### Question 5
**Scenario:** Where does Kyverno get its ability to see requests before they are stored?

A. It registers validating and mutating admission webhooks that the API server calls
B. It runs as a kubelet plugin on every node and intercepts container starts
C. It replaces the kube-apiserver binary with a patched version
D. It watches etcd directly and rolls back any object that violates a policy

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Kyverno receives validating and mutating admission webhook callbacks from the API server, and its webhook controller configures the webhooks to request only resources that installed policies match.
</details>

---

### Question 6
**Scenario:** Which Helm command installs Kyverno in its own namespace for a non-production setup?

A. helm install kyverno kyverno/kyverno -n kube-system
B. kubectl create -f https://github.com/kyverno/kyverno/raw/main/config/install-latest-testing.yaml as the production method
C. helm upgrade kyverno kyverno/kyverno --set admissionController.replicas=1
D. helm install kyverno kyverno/kyverno -n kyverno --create-namespace

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The installation page says Kyverno must run in a dedicated namespace and should not share one with system namespaces such as kube-system. The main-branch manifest is for testing only.
</details>

---

### Question 7
**Scenario:** A team needs Kyverno to remain available if one admission Pod fails. What does the Kyverno documentation recommend?

A. Raise the webhookTimeout flag to 30 seconds so the single Pod has more time
B. Set enableDefaultRegistryMutation to false so fewer requests reach the webhook
C. Run multiple replicas of the admission controller (the HA page gives a minimum of three), configured per controller through Helm
D. Run only the background controller with several replicas, since it serves the webhooks

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** HA is configured per controller, since each runs in its own Deployment. The admission controller serves the webhooks. A timeout increase does not add availability.
</details>

---

### Question 8
**Scenario:** A mutate-existing policy needs to update Deployments, but the policy installs with a permissions error. What is the documented way to fix this?

A. Edit the default kyverno:background-controller ClusterRole directly to add the verbs
B. Bind the admission controller ServiceAccount to cluster-admin
C. Create a ClusterRole carrying the label rbac.kyverno.io/aggregate-to-background-controller: "true" with the needed verbs
D. Add the verbs to the kyverno ConfigMap under the key extraPermissions

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Kyverno aggregates extra ClusterRoles by label. The docs warn against editing default roles because upgrades can overwrite the changes.
</details>

---

### Question 9
**Scenario:** Which upgrade statement matches the Kyverno upgrade documentation?

A. Upgrading by changing the image tag is the supported minimal path for patch versions
B. Bumping an image tag is not an upgrade, because new versions often change CRDs and other supporting resources
C. With YAML manifests, direct in-place upgrades are the preferred approach
D. Release notes only need to be read for the target version, never for skipped minor versions

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The page says an upgrade cannot be done by bumping the tag of any image. Direct upgrades from previous versions are not supported with the YAML manifest approach, and skipped minor versions' notes must be read.
</details>

---

### Question 10
**Scenario:** Which kyverno CLI command runs declared expectations from a kyverno-test.yaml file?

A. kyverno test
B. kyverno apply
C. kyverno jp
D. kyverno migrate

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** kyverno test runs test cases from a local folder or git repository, comparing declared results with what Kyverno computes. apply evaluates policies against resources and jp is the JMESPath tool.
</details>

---

### Question 11
**Scenario:** Which command applies a policy file to a resource file and lets you supply variable values from a file?

A. kyverno test policy.yaml -r resource.yaml -v values.yaml
B. kyverno jp query -i resource.yaml policy.yaml
C. kubectl kyverno parse policy.yaml --values values.yaml
D. kyverno apply policy.yaml --resource resource.yaml -f values.yaml

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** apply takes -r or --resource for resource paths and -f or --values-file for variable values. jp evaluates JMESPath queries.
</details>

---

### Question 12
**Scenario:** What does the result field of a kyverno-test.yaml entry accept?

A. allow or deny only
B. true or false only
C. Any string, matched as a regular expression
D. pass, fail, skip or warn

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Each results entry names a policy, rule and resource and sets result to pass, fail, skip or warn. A test passes only if the actual result equals the expected one.
</details>

---

### Question 13
**Scenario:** What is kyverno jp used for?

A. Joining two policies into one merged policy file
B. Producing a JSON patch for a mutate rule from a diff of two files
C. Evaluating and parsing JMESPath expressions, including Kyverno custom functions, to debug policy expressions
D. Publishing policies to an OCI registry

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** jp has the subcommands function, parse and query. It lets you test the expressions you put in variables, preconditions and foreach lists.
</details>

---

### Question 14
**Scenario:** A rule's match block contains both an any list and an all list. What does the documentation say?

A. Both are required, and the rule passes if either evaluates true
B. Each of match and exclude takes either any or all, not both in the same block
C. any is ignored whenever all is present
D. This is the only way to express a logical OR across two kinds

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Within match or exclude you choose any (OR) or all (AND). Fields within one resources entry are ANDed, and values in a list are ORed.
</details>

---

### Question 15
**Scenario:** A policy uses subjects in its match block. What other policy setting is required?

A. background: false
B. admission: false
C. applyRules: One
D. useServerSideApply: true

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** subjects, roles and clusterRoles describe the requesting user, which does not exist in a background scan, so the policy must set background: false.
</details>

---

### Question 16
**Scenario:** What does applyRules: One do?

A. Stops evaluating further rules after the first rule that applies
B. Requires exactly one rule in the policy
C. Applies the policy to only one namespace
D. Runs the policy once at install time and then disables it

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** applyRules defaults to All. With One, Kyverno stops after the first matching rule that was applied.
</details>

---

### Question 17
**Scenario:** An auditor wants to know which pre-existing resources violate a policy without blocking anything. Which setting makes sense?

A. Set the rule to Enforce and set failurePolicy to Ignore
B. Disable the admission controller and run only the cleanup controller
C. Add the cleanup.kyverno.io/ttl label to every resource
D. Leave the rule in Audit and keep background scanning on, then read the policy reports

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Audit allows resources and records violations. Background scans (default hourly) check existing resources and write results into PolicyReports and ClusterPolicyReports.
</details>

---

### Question 18
**Scenario:** What is the difference between pattern and deny in a validate rule?

A. pattern blocks when matched; deny describes the desired shape
B. They are identical; deny is the older spelling
C. pattern describes the desired resource shape; deny blocks when its conditions evaluate to true
D. pattern is only for Pods and deny is only for Namespaces

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A pattern is an overlay of the desired configuration. A deny rule uses key, operator and value conditions under any or all, and a true condition blocks the request.
</details>

---

### Question 19
**Scenario:** A rule has preconditions that evaluate to false for a resource. What happens?

A. The request is denied with the rule message
B. The rule does not apply, and the report records skip; nothing is blocked
C. The rule is applied anyway but downgraded to Audit
D. The policy is disabled until the precondition becomes true

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Preconditions control whether the rule runs. The docs say they do not produce a blocking effect like deny rules, and a result is scored as skip.
</details>

---

### Question 20
**Scenario:** Which anchor adds a field only if it is missing in a mutate patchStrategicMerge?

A. (field)
B. +(field)
C. <(field)
D. X(field)

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** +() is add-if-not-present. () is a conditional anchor, <() is global, and X() is the negation anchor used in validate patterns.
</details>

---

### Question 21
**Scenario:** Which mutation method does not support conditional anchors?

A. patchesJson6902
B. patchStrategicMerge
C. foreach with patchStrategicMerge
D. Mutate existing with targets

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The docs say patchesJson6902 uses RFC 6902 operations and does not support conditional anchors, so use preconditions instead.
</details>

---

### Question 22
**Scenario:** A generate rule clones a Secret into new Namespaces with synchronize: true. A user deletes the source Secret. What happens to the downstream copies?

A. They are kept as orphans
B. They are recreated from the policy
C. They are converted to data sources
D. They are deleted

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** In the deletion table for a clone source with synchronize, deleting the source deletes the downstream resources. Deleting the rule or policy retains them.
</details>

---

### Question 23
**Scenario:** What does orphanDownstreamOnPolicyDelete: true do for a synchronized data-source generate rule?

A. Deletes the generated resources immediately when the trigger changes
B. Prevents the policy from being deleted while downstream resources exist
C. Keeps the generated downstream resources when the policy or rule is deleted
D. Clones the downstream resources into a backup Namespace

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The default is false, which deletes downstream resources when the rule or policy is deleted. true retains them.
</details>

---

### Question 24
**Scenario:** A generate rule for existing Namespaces should also run when the policy is created. Which setting is used?

A. background: true at spec level only
B. synchronize: false
C. generateExisting: true under the generate rule
D. mutateExistingOnPolicyUpdate: true

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** By default generate applies only to new trigger events. generateExisting under rules[*].generate also applies it to existing matching resources; spec.generateExisting is deprecated.
</details>

---

### Question 25
**Scenario:** Which verifyImages attribute rewrites a tag to a digest and which default value does it have?

A. verifyDigest, false by default
B. mutateDigest, true by default
C. required, false by default
D. skipImageReferences, true by default

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** mutateDigest defaults to true and converts tags to digests. verifyDigest checks that matching images use digests, and required defaults to true as well.
</details>

---

### Question 26
**Scenario:** Which context type reads a ConfigMap, and what label makes Kyverno cache it?

A. configMap, with cache.kyverno.io/enabled: "true"
B. apiCall, with cleanup.kyverno.io/ttl
C. imageRegistry, with policies.kyverno.io/cache
D. globalReference, with kyverno.io/cached

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** configMap context reads values at evaluation time. Labeling a ConfigMap cache.kyverno.io/enabled: "true" makes Kyverno cache it and reduces API server calls.
</details>

---

### Question 27
**Scenario:** Autogen did not create rules for Deployments even though the policy targets Pods. Which cause is documented?

A. The policy sets failurePolicy to Fail
B. The policy has a rule name longer than 63 characters
C. Deployments never receive autogenerated rules
D. The match block uses names, selector or annotations, which makes Kyverno skip autogen

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Autogen is skipped if match or exclude uses names, selector or annotations. It is also controlled by the pod-policies.kyverno.io/autogen-controllers annotation, where none disables it.
</details>

---

### Question 28
**Scenario:** How can a resource be deleted after two minutes without writing any cleanup policy?

A. Annotate it with kyverno.io/expire: 2m
B. Set generate.synchronize: true on a clone rule
C. Use a PolicyException with a two minute duration
D. Add the label cleanup.kyverno.io/ttl: 2m

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The reserved label cleanup.kyverno.io/ttl takes an absolute ISO 8601 time or a relative duration. The reconciliation interval defaults to one minute.
</details>

---

### Question 29
**Scenario:** In a Kyverno validate.cel rule, what happens when an expression evaluates to false?

A. The expression is retried until it is true
B. The rule is skipped and a warn result recorded
C. The rule's failureAction is triggered
D. Kyverno mutates the resource until the expression is true

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** For validate.cel, a false expression triggers the failureAction (Audit or Enforce). The expressions can use object, oldObject, request, params, namespaceObject and authorizer.
</details>

---

### Question 30
**Scenario:** What do PolicyException resources require before they take effect in a cluster?

A. Nothing; exceptions are honored cluster-wide by default
B. The enablePolicyException flag set to true and the exceptionNamespace flag set
C. A ClusterPolicy annotated with kyverno.io/allow-exceptions
D. A rule in the ValidatingWebhookConfiguration listing each exception

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** PolicyExceptions are disabled by default. Both container flags are needed, and since 1.13 they are no longer enabled in all namespaces by default.
</details>

---

### Question 31
**Scenario:** Which statement about Kyverno policy reports is correct?

A. They use the wgpolicyk8s.io API and show results for current resources only, with no history
B. They keep a full audit history of every past admission decision
C. They are only produced for validate rules in Enforce mode
D. They are stored in etcd outside the Kubernetes API

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Reports are Kubernetes resources in the open wgpolicyk8s.io/v1alpha2 format. They reflect the current cluster state and entries are removed when the resource is deleted.
</details>

---

### Question 32
**Scenario:** Which port and path serve Kyverno's Prometheus metrics?

A. Port 8000, /metrics
B. Port 443, /healthz
C. Port 9090, /federate
D. Port 10250, /stats

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The monitoring page says metrics are served on port 8000 at /metrics. With an OpenTelemetry Collector the Prometheus endpoint is on 9090, but that is the Collector.
</details>

---
