---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 14 min
---

# 02 - GitOps and Continuous Delivery

**Domain 2: GitOps and Continuous Delivery (25%)**

Curriculum competencies: implementing GitOps workflows for application and infrastructure deployment; building and configuring CI/CD pipelines integrated with Kubernetes; deploying applications using progressive delivery strategies (for example Blue/Green or Canary).

Tools named in the curriculum for this domain: Argo, Flux, Tekton, Flagger (and Istio/Linkerd for traffic shifting). All YAML below was syntax-checked only, never applied.

For GitOps theory and the Argo/Flux vocabulary, the [CGOA](../../cgoa/) and [CAPA](../../capa/) guides go deeper. This note is the keyboard version.

---

## GitOps workflows

GitOps keeps the desired state in Git and has an agent in the cluster pull it and reconcile. Two agents are named in the curriculum.

### Argo CD

An Argo CD **Application** says "take this path from this repo and make this namespace look like it." From the application specification page:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    automated:
      enabled: true
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

Reading the fields the way a task would ask about them:

| Field | Meaning |
|---|---|
| `source.repoURL`, `targetRevision`, `path` | Where the manifests are; `targetRevision` is the Git revision (or chart version) |
| `destination.server` or `name` and `namespace` | Which cluster and namespace to deploy into |
| `syncPolicy.automated` | Auto-sync on; `prune` deletes resources removed from Git; `selfHeal` corrects drift made in the cluster |
| `syncOptions: CreateNamespace=true` | Create the destination namespace if missing |
| `project` | The Argo CD project, used for access boundaries |

Without `automated`, the Application shows OutOfSync until someone syncs it. If a task says "changes made with kubectl keep disappearing," `selfHeal` is why.

**[📖 Argo CD application specification](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/)** - fields and examples

### Flux

Flux splits the job into a **source** and a **Kustomization**. From the Flux Kustomization page:

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: podinfo
  namespace: default
spec:
  interval: 5m
  url: https://github.com/stefanprodan/podinfo
  ref:
    branch: master
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: podinfo
  namespace: default
spec:
  interval: 10m
  targetNamespace: default
  sourceRef:
    kind: GitRepository
    name: podinfo
  path: "./kustomize"
  prune: true
  timeout: 1m
```

- The GitRepository clones the branch and stores the content as an artifact. The Kustomization does not fetch code itself; it uses `sourceRef` to watch the source, builds the manifests at `path`, applies them and re-reconciles when the revision changes.
- `interval` is required (minimum 60 seconds) and also corrects drift. `prune` is required and enables garbage collection of objects removed from the source.
- `dependsOn` makes one Kustomization wait for others to be Ready. `wait: true` health-checks everything reconciled. `suspend: true` pauses new revisions and drift correction.
- `targetNamespace` does not create the namespace; it must already exist or be defined in the manifests.

**[📖 Flux Kustomization](https://fluxcd.io/flux/components/kustomize/kustomizations/)** - fields, dependsOn, health checks

### GitOps for infrastructure

Infrastructure follows the same loop when it is declared as Kubernetes resources, which is what Crossplane gives you (domain 3): a Crossplane composite resource committed to Git is reconciled by Argo CD or Flux like any other manifest. Platform teams use that to provision cloud resources from the same repository workflow as applications.

---

## CI/CD pipelines integrated with Kubernetes: Tekton

Tekton runs pipelines as Kubernetes resources. From the Pipeline page:

| Resource | Role |
|---|---|
| **Task** | A unit of work; each Task in a Pipeline "executes as a Pod" |
| **Pipeline** | Tasks arranged in an order (`spec.tasks`) |
| **PipelineRun** | Starts a Pipeline at runtime and supplies parameter values |
| **TaskRun** | Records one Task's execution |

```yaml
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: pipeline-with-parameters
spec:
  params:
    - name: context
      type: string
      description: Path to context
      default: /some/where/or/other
  tasks:
    - name: build-skaffold-web
      taskRef:
        name: build-push
      params:
        - name: pathToContext
          value: "$(params.context)"
---
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: pipelinerun-with-parameters
spec:
  pipelineRef:
    name: pipeline-with-parameters
  params:
    - name: "context"
      value: "/workspace/examples/microservices/leeroy-web"
```

Key mechanics:

- **`params`** are declared on the Pipeline and referenced as `$(params.<name>)`; the PipelineRun passes them in.
- **`workspaces`** share volumes between Tasks.
- **`runAfter`** orders Tasks without passing data.
- **`results`** pass output: `$(tasks.<task-name>.results.<result-name>)`.
- **`finally`** Tasks run after all others finish, whether they succeeded or failed (good for notifications and cleanup); they cannot use `runAfter`.
- A failed Task sets its TaskRun's `Succeeded` condition to `False`.

CI builds and tests; the hand-off to GitOps is usually "CI updates the image tag in Git, the GitOps agent deploys it." Keep those two jobs separate.

**[📖 Tekton Pipelines](https://tekton.dev/docs/pipelines/pipelines/)** - params, workspaces, runAfter, results, finally

---

## Progressive delivery: canary and blue/green

Progressive delivery limits the blast radius of a bad release by shifting traffic in steps and checking metrics before continuing.

### Argo Rollouts

A **Rollout** replaces a Deployment and adds a strategy. From the canary page:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: example-rollout
spec:
  replicas: 10
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.15.4
          ports:
            - containerPort: 80
  minReadySeconds: 30
  revisionHistoryLimit: 3
  strategy:
    canary:
      maxSurge: '25%'
      maxUnavailable: 0
      steps:
        - setWeight: 10
        - pause:
            duration: 1h
        - setWeight: 20
        - pause: {}
```

- `steps` run when `.spec.template` changes. `setWeight` sets the canary's traffic percentage (approximated with Pod counts when no traffic routing is configured).
- `pause` with a `duration` resumes automatically; **`pause: {}` waits until a human promotes**: `kubectl argo rollouts promote <rollout>`.
- `trafficRouting` hooks in a mesh or ingress. The page says `setCanaryScale` is only available with a traffic router; `dynamicStableScale` (since v1.1) is described in its traffic-routing section. With traffic routing, `maxSurge` and `maxUnavailable` only affect replica math for the basic canary, so the stable ReplicaSet stays at full scale and total Pods can exceed twice `spec.replicas`.
- The page documents `analysis` as a canary-level field that runs background analysis, and an unsuccessful result aborts the rollout. It does not cover blue/green or an abort command, so read the blue/green page and the CLI help in the exam environment.

**[📖 Argo Rollouts canary](https://argo-rollouts.readthedocs.io/en/stable/features/canary/)** - steps, traffic routing, promotion

### Flagger

Flagger automates canary releases with a **Canary** resource that targets an existing Deployment:

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: podinfo
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: podinfo
  service:
    port: 9898
  analysis:
    interval: 1m
    threshold: 10
    maxWeight: 50
    stepWeight: 5
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 1m
```

How it behaves: when the target (or its referenced ConfigMaps and Secrets) changes, Flagger creates a `<name>-primary` Deployment for the stable version plus `<name>`, `<name>-primary` and `<name>-canary` Services. On each `interval` it checks metrics and shifts traffic by `stepWeight` up to `maxWeight`. If failed checks reach `threshold`, it rolls back. The `iterations` field covers A/B and blue/green style analysis. `suspend: true` pauses reconciliation.

**[📖 Flagger: how it works](https://docs.flagger.app/usage/how-it-works)** - Canary resource, analysis, stages

### Choosing

| Choice | Fits when |
|---|---|
| Argo Rollouts | You want the rollout strategy defined on a Rollout object that replaces the Deployment |
| Flagger | You want to keep the Deployment and let a Canary resource wrap it, driven by mesh metrics |
| Plain Deployment rolling update | The change is low risk and you have no traffic-shifting layer |

---

## Key terms

- **GitOps** - managing infrastructure and applications by committing desired state to Git and reconciling it automatically.
- **Argo CD Application** - the resource that maps a Git path to a destination cluster and namespace.
- **selfHeal** - an Argo CD sync option that reverts manual changes in the cluster.
- **prune** - a sync or reconcile option that deletes resources that were removed from Git.
- **GitRepository (Flux)** - a source resource that clones a repository and exposes it as an artifact.
- **Kustomization (Flux)** - a resource that builds and applies manifests from a source on an interval.
- **Tekton Task** - a unit of CI work that runs as a Pod.
- **PipelineRun** - a Tekton resource that executes a Pipeline with given parameters.
- **Progressive delivery** - releasing in steps with automated checks so failures are caught early.
- **Canary release** - sending a small share of traffic to the new version before promoting it.
- **Blue/green** - running old and new versions side by side and switching traffic between them.
- **Rollout (Argo Rollouts)** - a Deployment replacement that supports canary and blue-green strategies.
- **Canary (Flagger)** - the Flagger resource that automates analysis and promotion for a Deployment.
