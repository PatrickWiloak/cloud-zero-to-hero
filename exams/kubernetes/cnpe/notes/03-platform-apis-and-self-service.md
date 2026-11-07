---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 14 min
---

# 03 - Platform APIs and Self-Service Capabilities

**Domain 3: Platform APIs and Self-Service Capabilities (25%)**

Curriculum competencies: designing and creating Custom Resource Definitions (CRDs) for platform services; implementing workflows for self-service provisioning using platform APIs; using Kubernetes Operators for platform automation and integration; using automation frameworks for self-service provisioning.

Tool named in the curriculum for this domain: Crossplane (and Argo/Flux for the delivery path). YAML here was syntax-checked only, not applied.

The idea of the domain: a platform team turns "how to get a database" into **a Kubernetes API** that developers use with `kubectl apply` or a Git commit, and a controller does the work.

---

## Designing and creating CRDs

A CustomResourceDefinition adds a new resource type to the Kubernetes API. From the Kubernetes docs:

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                cronSpec:
                  type: string
                image:
                  type: string
                replicas:
                  type: integer
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
```

Rules you will be asked to apply:

- **The CRD name must be `<plural>.<group>`.**
- **One and only one version is the storage version** (`storage: true`); `served: true` makes a version available.
- `scope` is `Namespaced` or `Cluster`.
- Creating the CRD creates an endpoint such as `/apis/stable.example.com/v1/namespaces/*/crontabs/...`, which "may take a few seconds to become available."
- A custom resource then looks like any object:

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "* * * * */5"
  image: my-awesome-cron-image
```

```bash
kubectl apply -f resourcedefinition.yaml
kubectl apply -f my-crontab.yaml
kubectl get crontab
```

- **Deleting a CRD deletes every custom object stored under it.** Deleting a namespace deletes the custom objects in it; CRDs themselves are not namespaced.

The `openAPIV3Schema` is where you design the platform's API surface: a small number of typed fields, with required ones marked, instead of a free-form blob. The docs list validation (including validation rules and defaulting), additional printer columns and subresources as further features; read those sections in the exam environment if a task asks for them.

**[📖 Create a CustomResourceDefinition](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)** - CRD fields, endpoint, deletion behavior

---

## Operators for platform automation

A CRD alone only stores data. An **operator** pairs a CRD with a controller that acts on it. The Kubernetes docs: "Operators are clients of the Kubernetes API that act as controllers for a Custom Resource." The deployment is a CRD for the new kind plus a Deployment running the controller image outside the control plane.

The docs' example is a `SampleDB` resource. When one is created, the operator creates PersistentVolumeClaims, a StatefulSet and a configuration Job; on deletion it takes a snapshot first. Other jobs operators automate: backup and restore, coordinated upgrades, publishing Services, leader election.

You use an operator through its custom resource:

```bash
kubectl get SampleDB                   # find configured databases
kubectl edit SampleDB/example-database # manually change some settings
```

Writing your own is possible in any language that can be a Kubernetes API client; the docs list third-party frameworks including kubebuilder (Go), the Operator Framework, kube-rs (Rust), Kopf (Python) and the Java Operator SDK, and note they are not maintained by the Kubernetes authors. On the exam you are far more likely to **install and use** an operator than to write one.

**[📖 Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)** - controllers, custom resources, frameworks

---

## Self-service provisioning with Crossplane

Crossplane lets a platform team define its own cloud API (for example an `AcmeBucket`) and compose real resources behind it. Concepts from the Crossplane docs (v2.4 pages read on 2026-11-07):

| Concept | Role |
|---|---|
| **CompositeResourceDefinition (XRD)** | Defines the schema of the custom API |
| **Composition** | A template: which composed resources to create for a composite resource |
| **Composite resource (XR)** | An instance of the custom API, which developers create |
| **Function** | A step in a Composition pipeline that produces the desired resources |
| **Managed resource** | The provider-backed resource (for example an S3 bucket) that Crossplane reconciles |

An XRD:

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xdatabases.custom-api.example.org
spec:
  group: custom-api.example.org
  names:
    kind: xDatabase
    plural: xdatabases
  versions:
  - name: v1alpha1
    served: true
    referenceable: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              region:
                type: string
```

Facts from the XRD page: the XRD name must be `<plural>.<group>`; you cannot change group or names after creation (delete and recreate); `referenceable: true` marks the version Compositions use and only one version can be referenceable; `scope` can be `Namespaced` (the default in v2: composite resources live in a namespace and compose resources in that namespace), `Cluster`, or `LegacyCluster` (cluster-scoped with claim support for v1 compatibility).

A Composition in **pipeline mode** (condensed from the Compositions page):

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: example
spec:
  compositeTypeRef:
    apiVersion: custom-api.example.org/v1alpha1
    kind: AcmeBucket
  mode: Pipeline
  pipeline:
  - step: patch-and-transform
    functionRef:
      name: function-patch-and-transform
    input:
      apiVersion: pt.fn.crossplane.io/v1beta1
      kind: Resources
      resources:
      - name: storage-bucket
        base:
          apiVersion: s3.aws.m.upbound.io/v1beta1
          kind: Bucket
          spec:
            forProvider:
              region: "us-east-2"
```

And the function that must be installed first:

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Function
metadata:
  name: function-patch-and-transform
spec:
  package: xpkg.crossplane.io/crossplane-contrib/function-patch-and-transform:v0.8.2
```

How the pieces run: Crossplane runs pipeline steps in order and each function receives the previous function's result. **Functions must copy forward all desired state they receive; otherwise Crossplane deletes the resources they omitted.** Functions do not run when an XR is deleted. `function-auto-ready` marks the XR ready once its composed resources are ready.

The Compositions page did not cover claims, and the XRD page says nothing about claims beyond the `LegacyCluster` scope, so check the composite resource docs in the exam environment for how a developer requests one.

**[📖 Crossplane compositions](https://docs.crossplane.io/latest/composition/compositions/)** - pipeline mode, functions

**[📖 Crossplane composite resource definitions](https://docs.crossplane.io/latest/composition/composite-resource-definitions/)** - XRD fields and scope

---

## Self-service workflows and automation frameworks

The curriculum names two competencies that overlap: "workflows for self-service provisioning using platform APIs" and "automation frameworks for self-service provisioning." In practice that is the chain:

1. **API.** The platform defines a CRD or XRD (a `Database`, an `Environment`, an `AcmeBucket`).
2. **Request.** A developer commits a small YAML instance of it to Git.
3. **Delivery.** Argo CD or Flux syncs the instance to the cluster (note 02).
4. **Fulfillment.** An operator or Crossplane composition creates the real resources.
5. **Status.** The status on the resource tells the developer whether it is ready.

A good platform API has few fields, safe defaults and clear status conditions. A bad one exposes every cloud setting and rebuilds the cloud console in YAML.

The [CNPA guide](../../cnpa/) covers the platform-engineering concepts around this (golden paths, developer portals, internal developer platforms). The [Backstage concept page](../../../../learn/concepts/backstage-and-developer-portals.md) covers portals that put a form in front of these APIs.

---

## Key terms

- **CRD** - a CustomResourceDefinition that adds a new resource type to the Kubernetes API.
- **Custom resource** - an instance of a CRD, stored and served by the API server.
- **Storage version** - the single CRD version in which objects are persisted.
- **Operator** - a controller that manages a custom resource and automates the operations around it.
- **Controller** - a control loop that watches resources and works to match actual state to desired state.
- **Crossplane** - a framework that turns infrastructure and services into Kubernetes APIs.
- **XRD** - a Crossplane CompositeResourceDefinition that defines a custom API's schema.
- **Composition** - a Crossplane template of resources to create for a composite resource.
- **Composite resource (XR)** - an instance of the API an XRD defines.
- **Composition function** - a pipeline step in a Composition that returns desired resources.
- **Managed resource** - a Crossplane resource that represents and reconciles one external cloud resource.
- **Self-service** - letting developers provision what they need through an API without filing a ticket.
