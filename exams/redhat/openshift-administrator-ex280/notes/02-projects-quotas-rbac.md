# 02 - Projects, Quotas, RBAC, and Identity

## Projects vs Namespaces

A **Project** is an OpenShift extension of a Kubernetes namespace with extra metadata (display name, description, default network policies, default project templates).

```bash
oc new-project myapp \
    --description="Production app" \
    --display-name="My App"

oc projects                                       # list
oc project myapp                                  # switch
oc delete project myapp
```

### Project requests (self-service vs admin-only)

The `self-provisioner` ClusterRole controls who can create projects. To restrict project creation to admins only:

```bash
oc adm policy remove-cluster-role-from-group self-provisioner system:authenticated:oauth
```

To re-enable:

```bash
oc adm policy add-cluster-role-to-group self-provisioner system:authenticated:oauth
```

### Default project template (`projectRequestTemplate`)

You can customize what new projects come with (default NetworkPolicy, default LimitRange, default labels). Edit the cluster `Project` config:

```bash
oc edit project.config.openshift.io/cluster
```

```yaml
spec:
  projectRequestTemplate:
    name: project-request
```

Then `oc apply` your custom template into `openshift-config`.

---

## ResourceQuota

Limits aggregate consumption in a project.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: project-quota
  namespace: myapp
spec:
  hard:
    requests.cpu: '4'
    requests.memory: 8Gi
    limits.cpu: '8'
    limits.memory: 16Gi
    persistentvolumeclaims: '10'
    pods: '20'
    services: '5'
    secrets: '20'
    configmaps: '20'
```

```bash
oc apply -f quota.yaml
oc -n myapp get quota
oc -n myapp describe quota project-quota
```

### Quota scope

You can limit to specific scopes (`Terminating`, `NotTerminating`, `BestEffort`, `NotBestEffort`):

```yaml
spec:
  scopes: [BestEffort]
  hard: { pods: '5' }
```

---

## LimitRange

Sets per-container defaults and limits.

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: project-limits
  namespace: myapp
spec:
  limits:
  - type: Container
    default: { cpu: 500m, memory: 512Mi }              # if not set on container
    defaultRequest: { cpu: 100m, memory: 128Mi }
    max: { cpu: '2', memory: 4Gi }
    min: { cpu: 50m, memory: 64Mi }
  - type: Pod
    max: { cpu: '4', memory: 8Gi }
  - type: PersistentVolumeClaim
    max: { storage: 10Gi }
    min: { storage: 1Gi }
```

`LimitRange` is applied at admission time - resources without requests/limits inherit the defaults.

---

## RBAC

OpenShift uses standard Kubernetes RBAC: Roles + RoleBindings (namespaced) and ClusterRoles + ClusterRoleBindings (cluster-wide).

### Default ClusterRoles

| Role | Permissions |
|---|---|
| `cluster-admin` | Everything |
| `admin` | Full control of namespace (default for project owner) |
| `edit` | Modify most resources except RBAC |
| `view` | Read-only |
| `basic-user` | View own projects, get oauth tokens |
| `self-provisioner` | Create new projects |

### Grant roles

```bash
# Cluster-level
oc adm policy add-cluster-role-to-user cluster-admin alice
oc adm policy add-cluster-role-to-group view system:authenticated

# Namespace-level
oc adm policy add-role-to-user admin alice -n myapp
oc adm policy add-role-to-user edit bob -n myapp
oc adm policy add-role-to-user view charlie -n myapp

# Service account
oc adm policy add-role-to-user view system:serviceaccount:myapp:default -n myapp

# Remove
oc adm policy remove-role-from-user admin alice -n myapp
oc adm policy remove-cluster-role-from-user cluster-admin alice
```

### Verify what someone can do

```bash
oc auth can-i get pods --as=alice -n myapp
oc auth can-i create deployments --as=alice -n myapp
oc adm policy who-can create pods -n myapp                  # who has this permission
oc describe rolebinding -n myapp
```

### Custom Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-debugger
  namespace: myapp
rules:
- apiGroups: [""]
  resources: [pods, pods/log, pods/status]
  verbs: [get, list, watch]
- apiGroups: [""]
  resources: [pods/exec]
  verbs: [create]
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: alice-pod-debugger
  namespace: myapp
subjects:
- kind: User
  name: alice
roleRef:
  kind: Role
  name: pod-debugger
  apiGroup: rbac.authorization.k8s.io
```

---

## Identity providers

OpenShift authenticates via the `OAuth` cluster resource. Multiple identity providers can be configured.

### HTPasswd (most common on the exam)

```bash
# Create htpasswd file
htpasswd -c -B -b users.htpasswd alice secret
htpasswd -B -b users.htpasswd bob secret2

# Create secret in openshift-config
oc create secret generic htpass-secret \
    --from-file=htpasswd=users.htpasswd \
    -n openshift-config
```

Edit `oauth/cluster`:

```bash
oc edit oauth cluster
```

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

After save, OAuth pods restart in `openshift-authentication`. Wait ~30s.

```bash
oc -n openshift-authentication get pods
oc login -u alice -p secret
oc whoami
```

### Update the htpasswd file later

```bash
htpasswd -B -b users.htpasswd charlie secret3
oc create secret generic htpass-secret \
    --from-file=htpasswd=users.htpasswd \
    --dry-run=client -o yaml | oc apply -f -
```

The OAuth operator picks up the change.

### Remove a user

```bash
htpasswd -D users.htpasswd alice
# Re-create the secret as above
oc delete user alice
oc delete identity my_htpasswd:alice
```

---

## Groups

OpenShift groups are first-class:

```bash
oc adm groups new ops alice bob
oc adm groups add-users ops charlie
oc adm groups remove-users ops bob
oc get groups

# Grant a role to a group
oc adm policy add-role-to-group admin ops -n myapp
```

---

## Service accounts

Service accounts are non-human identities used by pods.

```bash
oc create sa myapp-sa
oc adm policy add-role-to-user view system:serviceaccount:myproject:myapp-sa -n myproject
```

In a pod:

```yaml
spec:
  serviceAccountName: myapp-sa
```

---

## Common exam tasks

### "Make alice an admin of project foo"

```bash
oc adm policy add-role-to-user admin alice -n foo
oc auth can-i '*' '*' --as=alice -n foo
```

### "Set up htpasswd identity provider with users alice and bob"

```bash
htpasswd -c -B -b users.htpasswd alice secret
htpasswd -B -b users.htpasswd bob secret2
oc create secret generic htpass-secret --from-file=htpasswd=users.htpasswd -n openshift-config
oc edit oauth cluster
# Add the identityProviders block as above
# Wait 30s
oc login -u alice -p secret
```

### "Create a 4 CPU / 8 GB project quota"

```bash
oc create quota project-quota \
    --hard=requests.cpu=4,requests.memory=8Gi,limits.cpu=8,limits.memory=16Gi \
    -n myapp
```

### "Set default container limits in project"

Apply the LimitRange YAML above with `oc apply -f`.

### "Restrict project creation to cluster admins"

```bash
oc adm policy remove-cluster-role-from-group self-provisioner system:authenticated:oauth
```

---

## Verification

After RBAC / quota / identity changes:

- `oc auth can-i ... --as=<user>` returns expected yes/no
- `oc -n <project> get quota` shows the quota
- `oc -n <project> describe quota` shows current usage vs limit
- `oc login -u <user>` succeeds with correct password
- `oc get user`, `oc get identity` show expected entries

## Key terms

- **Project** - an OpenShift namespace with extra annotations that isolates a set of resources for a user or team.
- **ResourceQuota** - an object that caps the total resources, such as CPU, memory or object counts, that a project can use.
- **LimitRange** - an object that sets default and maximum resource requests and limits for containers in a project.
- **Role binding** - an object that grants the permissions of a role to a user, group or service account within a project.
- **Security context constraint (SCC)** - an OpenShift policy that controls what actions a pod may perform and what it can access.
