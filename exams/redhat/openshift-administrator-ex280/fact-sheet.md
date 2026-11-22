---
last-updated: 2026-11-22
---

# OpenShift Administrator (EX280) - Fact Sheet

## Quick Reference

**Exam Code:** EX280
**Duration:** 3 hours
**Format:** Performance-based hands-on tasks on a live cluster; the exam page names Red Hat OpenShift Container Platform 4.22 (read 2026-11-22)
**Passing Score:** 210/300 (70%) (not stated on the EX280 page; widely reported)
**Cost:** $500 USD (US list; not stated on the EX280 page, check it)
**Validity:** 3 years (not stated on the EX280 page)
**Objective groups (exam page):** Manage OpenShift Container Platform; Declarative resource management; Deploy applications; Manage authentication and authorization; Configure network security; Enable developer self-service; Manage OpenShift operators; Configure application security
**Open documentation:** `oc explain`, web console, cluster resources

**[📖 Official EX280 page](https://www.redhat.com/en/services/training/red-hat-certified-openshift-administrator-exam)**
**[📖 OpenShift 4.22 Documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.22)**
**[📖 Latest OpenShift Docs](https://docs.openshift.com/)**

---

## Cluster components

| Component | Purpose |
|---|---|
| **Control plane (master) nodes** | etcd, kube-apiserver, kube-controller-manager, kube-scheduler, OpenShift API |
| **Compute (worker) nodes** | Run user workloads |
| **Infrastructure nodes** | Optional dedicated nodes for routers, registry, monitoring |
| **etcd** | Cluster state store |
| **CRI-O** | Container runtime |
| **OVN-Kubernetes** | Default SDN (replaces older OpenShift SDN) |
| **HAProxy router** | Default ingress for Routes |
| **Image registry** | OpenShift internal image registry |
| **Operator Lifecycle Manager (OLM)** | Manages operator installations |
| **Cluster Monitoring Operator** | Prometheus + Alertmanager + Grafana |

---

## High-yield `oc` commands

### Cluster info

```bash
oc whoami                                      # current user
oc whoami --show-server                        # API endpoint
oc whoami --show-token                         # token (sensitive)
oc cluster-info
oc get clusterversion                          # current version
oc get nodes
oc get nodes -L node-role.kubernetes.io/worker
oc describe node <name>
oc get co                                      # cluster operators
oc get clusteroperators -o wide
oc adm top nodes                               # resource usage
oc adm top pods -A
```

### Projects (namespaces)

```bash
oc projects                                    # list
oc project myproject                           # switch
oc new-project myapp --description='...' --display-name='My App'
oc delete project myapp
```

### Workloads

```bash
oc new-app https://github.com/user/repo --name=myapp
oc new-app docker.io/nginx --name=web
oc get all
oc get deployments
oc scale deploy/web --replicas=3
oc rollout status deploy/web
oc rollout undo deploy/web
oc set image deploy/web web=nginx:1.25
oc set env deploy/web FOO=bar
oc set resources deploy/web --limits=cpu=500m,memory=512Mi --requests=cpu=100m,memory=128Mi
oc autoscale deploy/web --min=2 --max=10 --cpu-percent=70
```

### Pods and debugging

```bash
oc get pods
oc get pods -o wide
oc describe pod <name>
oc logs <pod>
oc logs -f <pod>                               # follow
oc logs <pod> -c <container>                   # specific container
oc rsh <pod>                                   # shell into pod
oc exec <pod> -- <command>
oc debug node/<nodename>                       # debug pod on a node
oc debug deploy/web                            # debug a deployment
oc port-forward pod/<pod> 8080:80              # forward
```

### Services and routes

```bash
oc expose deploy/web --port=80                          # creates Service
oc expose svc/web                                       # creates Route
oc expose svc/web --hostname=app.example.com
oc create route edge --service=web --hostname=app.example.com  # TLS-terminated edge route
oc create route passthrough --service=web              # TLS passthrough
oc create route reencrypt --service=web                # TLS reencrypt
oc get routes
oc get svc
```

### Storage

```bash
oc get pv
oc get pvc
oc set volume deploy/web --add --type=pvc --claim-size=1Gi --mount-path=/data
oc set volume deploy/web --remove --name=<volname>
oc get storageclass
oc get sc                                              # alias
```

### Authentication and RBAC

```bash
oc adm policy add-cluster-role-to-user cluster-admin alice
oc adm policy add-role-to-user admin alice -n myproject
oc adm policy remove-role-from-user admin alice -n myproject
oc get clusterrolebinding | grep alice
oc auth can-i create pods --as=alice -n myproject
oc adm policy who-can create pods -n myproject
```

### Secrets and ConfigMaps

```bash
oc create secret generic mysecret --from-literal=password=s3cr3t
oc create secret generic mysecret --from-file=./creds.txt
oc create secret docker-registry myreg --docker-server=... --docker-username=... --docker-password=...
oc create secret tls mytls --cert=cert.pem --key=key.pem

oc create configmap myconfig --from-literal=KEY=value
oc create configmap myconfig --from-file=./app.conf

oc set env deploy/web --from=configmap/myconfig
oc set volume deploy/web --add --type=configmap --configmap-name=myconfig --mount-path=/etc/app
```

### Operators

```bash
oc get csv -A                                          # ClusterServiceVersions
oc get subscription -A
oc get installplan -A
oc get operatorgroup
```

### Must-gather (for support / debug)

```bash
oc adm must-gather                                     # cluster-wide diagnostic
oc adm must-gather --image=registry.redhat.io/<image>  # operator-specific
```

---

## Resource shapes you should be able to write

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: myproject
spec:
  replicas: 3
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
      - name: web
        image: nginx
        resources:
          requests: { cpu: 100m, memory: 128Mi }
          limits: { cpu: 500m, memory: 512Mi }
        ports:
        - containerPort: 80
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector: { app: web }
  ports:
  - port: 80
    targetPort: 80
```

### Route

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: web
spec:
  host: app.example.com
  to: { kind: Service, name: web }
  tls:
    termination: edge                    # edge | passthrough | reencrypt
    insecureEdgeTerminationPolicy: Redirect
```

### PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests: { storage: 5Gi }
  storageClassName: gp3-csi
```

### ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: project-quota
spec:
  hard:
    requests.cpu: '4'
    requests.memory: 8Gi
    limits.cpu: '8'
    limits.memory: 16Gi
    persistentvolumeclaims: '10'
    pods: '20'
```

### LimitRange (default per-container limits)

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: project-limits
spec:
  limits:
  - type: Container
    default:                # if not set on container
      cpu: 500m
      memory: 512Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    max:
      cpu: '2'
      memory: 4Gi
```

### NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-frontend
spec:
  podSelector:
    matchLabels: { app: backend }
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector:
        matchLabels: { app: frontend }
    ports:
    - protocol: TCP
      port: 8080
```

### Role + RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: myproject
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: alice-pod-reader
  namespace: myproject
subjects:
- kind: User
  name: alice
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### Subscription (install operator)

```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: openshift-pipelines-operator
  namespace: openshift-operators
spec:
  channel: latest
  name: openshift-pipelines-operator-rh
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  installPlanApproval: Automatic
```

---

## Identity providers

OpenShift supports multiple identity providers configured via the cluster `OAuth` resource. Common ones:

- **HTPasswd** - flat-file user/password (common on the exam)
- **LDAP** - directory service
- **GitHub / GitLab / Google** - OAuth integrations
- **OpenID Connect** - OIDC providers (Keycloak, Okta, etc.)

### HTPasswd configuration

```bash
htpasswd -c -B -b users.htpasswd alice secret
htpasswd -B -b users.htpasswd bob secret2

oc create secret generic htpass-secret \
    --from-file=htpasswd=users.htpasswd \
    -n openshift-config

oc edit oauth cluster
```

In the OAuth resource:

```yaml
spec:
  identityProviders:
  - name: my_htpasswd
    mappingMethod: claim
    type: HTPasswd
    htpasswd:
      fileData:
        name: htpass-secret
```

After save, the cluster reconfigures the OAuth pods. Wait ~30s, then `oc login -u alice -p secret`.

---

## Security Context Constraints (SCCs)

SCCs are OpenShift's mechanism for controlling which pod security features are allowed. Built-in SCCs (most to least restrictive):

| SCC | Notes |
|---|---|
| `restricted-v2` | Default for non-privileged pods. Most secure. |
| `restricted` | Older default. |
| `nonroot-v2` | Allows nonroot UIDs |
| `anyuid` | Allows any UID (often needed for legacy images) |
| `hostnetwork` | Use host network |
| `hostmount-anyuid` | Mount host paths |
| `privileged` | Almost no restrictions |

### Grant SCC

```bash
oc adm policy add-scc-to-user anyuid -z <serviceaccount> -n <namespace>
oc adm policy add-scc-to-group privileged system:serviceaccounts:<namespace>
```

A pod failing with "unable to validate against any security context constraint" is the canonical SCC error.

---

## Storage classes (common)

| Cloud | Default StorageClass | Type |
|---|---|---|
| ROSA on AWS | `gp3-csi` | EBS gp3 |
| ARO on Azure | `managed-csi` | Azure Disk |
| OpenShift on VMware | `thin-csi` | VMware vSphere |
| OpenShift on bare metal | varies (LVM Operator, ODF, NFS) | many |

**Access modes:**

- `ReadWriteOnce (RWO)` - one node mount
- `ReadOnlyMany (ROX)` - many nodes RO
- `ReadWriteMany (RWX)` - many nodes RW (requires NFS or similar)
- `ReadWriteOncePod (RWOP)` - single pod
- `ReadWriteManyPod` - newer

---

## Monitoring

OpenShift ships a Prometheus-based monitoring stack in the `openshift-monitoring` namespace.

```bash
oc -n openshift-monitoring get pods
oc -n openshift-monitoring get routes prometheus-k8s
oc -n openshift-monitoring get routes alertmanager-main
```

User-defined monitoring (workload metrics) requires enabling:

```bash
oc -n openshift-monitoring edit cm cluster-monitoring-config
# Set:
# data:
#   config.yaml: |
#     enableUserWorkload: true
```

---

## Common exam triggers

- "Allow user alice to admin namespace foo" → `oc adm policy add-role-to-user admin alice -n foo`
- "Pod can't run because of UID" → SCC issue; grant `anyuid` to the SA, or change image to nonroot
- "Expose deployment to public DNS name" → `oc expose svc/X --hostname=...` (or `oc create route edge`)
- "Limit project to 4 CPUs" → ResourceQuota
- "Default request/limit per container in project" → LimitRange
- "Restrict pod-to-pod traffic" → NetworkPolicy
- "Install operator" → Subscription via OperatorHub or YAML
- "Persistent storage for app" → PVC with appropriate storageClass and accessModes
- "Different ingress termination types" → Edge / Passthrough / Reencrypt
- "Add HTPasswd users" → htpasswd file → secret → OAuth resource

---

## Things candidates commonly forget

- After editing `OAuth` for an identity provider, **wait 30s** for the OAuth pods to roll. Then `oc login` works.
- `oc expose svc` creates a Route by default. To get an Ingress, use `oc create -f` with an Ingress YAML.
- `oc adm policy add-scc-to-user` requires `-z <sa>` for service accounts (not just usernames).
- Routes default to HTTP. Use `oc create route edge` for TLS-terminated.
- `oc edit deploy/web` opens an in-place editor. Save and exit applies. Use `oc apply -f file.yaml` for repeatable changes.
- `oc rollout restart deploy/web` is the modern way to restart pods (better than `delete pod`).
- After changing a ConfigMap or Secret used as env vars, **the deployment doesn't auto-reload** - use `oc rollout restart`.

---

## After-pass next steps

| Cert | Why |
|---|---|
| **EX288** - OpenShift Application Development | Dev counterpart |
| **EX316** - OpenShift Virtualization | VMs on OpenShift |
| **EX480** - Advanced Cluster Management | Multi-cluster fleet |
| **CKA** | Vendor-neutral parallel |
| **CKS** | Kubernetes security specialist |
