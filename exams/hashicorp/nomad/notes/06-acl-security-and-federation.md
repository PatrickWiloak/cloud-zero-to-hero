# ACL Security and Federation

Nomad's ACL system controls who can read, write, submit, and inspect resources. Federation connects regions for multi-cluster deployments. This note covers both plus essential security patterns.

## Enabling ACLs

Edit server and client configs:

```hcl
acl {
  enabled = true
  token_ttl = "30m"
  policy_ttl = "30m"
  replication_token = "..."    # only on non-authoritative regions
}
```

Restart agents. Without ACLs, all API access is unauthenticated; with ACLs, everything requires a token.

## Bootstrap

On a fresh cluster:

```
nomad acl bootstrap
```

Output includes a secret ID (the management token). Save it immediately. This token has full permissions and cannot be revoked (only deleted and re-bootstrapped, which resets ACLs).

Use environment variable:

```
export NOMAD_TOKEN=<secret-id>
```

Or pass `-token=<id>` on each command.

## Tokens

Two types:

- **management:** full access to everything
- **client:** scoped by policies

```
nomad acl token create -name="dev-user" -policy=dev-policy
nomad acl token self    # inspect current token
nomad acl token list
nomad acl token delete <accessor-id>
```

Tokens have:

- **accessor ID:** public identifier (logged, shown)
- **secret ID:** the actual bearer token (keep secret)
- **TTL:** optional expiration

## Policies

Policies are HCL documents listing capabilities per resource type.

```hcl
# dev-policy.hcl

namespace "default" {
  policy = "read"
  capabilities = ["submit-job", "read-logs"]
}

namespace "prod" {
  policy = "deny"
}

node {
  policy = "read"
}

agent {
  policy = "read"
}

operator {
  policy = "deny"
}

quota {
  policy = "read"
}

host_volume "*" {
  policy = "read"
}
```

Apply:

```
nomad acl policy apply -description "Dev team" dev-policy dev-policy.hcl
nomad acl policy list
nomad acl policy info dev-policy
```

## Policy Rules by Resource

### namespace

- **deny:** no access
- **read:** see jobs, allocs, logs
- **write:** all of read plus manage jobs
- **capabilities:** granular (`submit-job`, `dispatch-job`, `read-logs`, `alloc-exec`, `alloc-node-exec`, `alloc-lifecycle`, `list-jobs`, `read-job`, `submit-job`)

### node

- **deny, read, write**
- Covers client node management (drain, update eligibility)

### agent

- **deny, read, write**
- Covers agent-level ops (debug, health)

### operator

- **deny, read, write**
- Raft operations, snapshots

### quota

- **deny, read, write**
- Resource quota management

### host_volume

- Per-volume policy; use `"*"` for all

## Workload Identity

Nomad can grant tasks their own identity tokens for accessing external systems (Vault, Consul):

```hcl
task "api" {
  identity {
    env  = true
    file = true
  }

  vault {
    policies = ["api-read"]
  }
}
```

The token is injected as `NOMAD_TOKEN` env var or written to a file. Used when the task needs to call the Nomad API itself.

## Vault Integration

Nomad can request Vault tokens on behalf of tasks:

### Server Configuration

```hcl
vault {
  enabled = true
  address = "https://vault.example.com:8200"

  create_from_role = "nomad-cluster"
  token            = "s.abc..."
}
```

### Task-Level Use

```hcl
vault {
  policies = ["db-read"]
  change_mode = "restart"
}

template {
  data = "{{with secret \"database/creds/readonly\"}}DB_PASS={{.Data.password}}{{end}}"
  destination = "secrets/env.vars"
  env = true
}
```

Nomad obtains a Vault token with the specified policies, renews it, revokes when task stops.

## Consul Integration

Similar pattern for Consul ACLs:

```hcl
consul {
  address = "127.0.0.1:8500"
  token   = "..."
  allow_unauthenticated = false
}
```

Tasks can use Consul tokens for service registration and KV reads.

## TLS

Enable TLS on all agent listeners:

```hcl
tls {
  http = true
  rpc  = true
  ca_file                = "/etc/nomad.d/ca.pem"
  cert_file              = "/etc/nomad.d/cert.pem"
  key_file               = "/etc/nomad.d/key.pem"
  verify_server_hostname = true
  verify_https_client    = true
}
```

Clients and servers require matching TLS config. Use Vault PKI or cert-manager for automation.

## Encryption at Rest

Nomad doesn't encrypt server state by default. For Raft logs and snapshots:

- Use full-disk encryption on servers
- Restrict filesystem access
- Snapshot encryption handled by cloud (S3 SSE-KMS) if you upload snapshots

## Gossip Encryption

Serf gossip uses a shared key:

```hcl
server {
  encrypt = "base64-32-byte-key"
}
```

Generate: `nomad operator keygen`.

All servers and clients in the region must share the same key. Rotate via `nomad operator gossip keyring` commands.

## Sentinel Policies (Enterprise)

Policy-as-code for Nomad:

```
import "nomad" as nomad

main = rule {
  all nomad.job.task_groups as group {
    all group.tasks as task {
      task.resources.memory <= 2048
    }
  }
}
```

Apply at job submission. Enforcement levels: advisory, soft-mandatory, hard-mandatory. Similar to Terraform Sentinel.

## Federation

Regions are independent Nomad clusters. Federation links them for cross-region visibility.

### Setup

1. In the primary region, note the replication token:
```
nomad acl token create -type=management -global=true
```

2. In each secondary region's config:
```hcl
acl {
  enabled = true
  replication_token = "<primary-region-token>"
}
```

3. Join servers across regions via WAN gossip:
```
nomad server join -wan secondary.example.com:4648
```

4. ACL policies and tokens replicate from primary to secondaries (read-only in secondaries).

### Cross-Region Job Submission

```
nomad job run -region=us-west job.nomad
```

or in the jobspec:

```hcl
job "example" {
  region = "us-west"
  # ...
}
```

Nomad routes the request to the specified region.

### Region-Global Endpoints

Some API endpoints are region-aware. Use `?region=us-west` or `-region=us-west`.

## Multi-Cluster (Enterprise)

Nomad Enterprise supports multi-cluster operations with unified views across federated regions:

- Cross-cluster job status
- Aggregated metrics
- Global ACL management

## Namespaces for Multi-Tenancy

Namespaces partition jobs logically within a region:

```
nomad namespace apply -description="Dev" dev
nomad namespace apply -description="Prod" prod
```

Jobspecs specify namespace:

```hcl
job "web" {
  namespace = "prod"
}
```

Or use `-namespace=prod` on submission. ACL policies restrict access per namespace.

## Audit Logging (Enterprise)

```hcl
audit {
  enabled = true
  sink "file" {
    type               = "file"
    format             = "json"
    delivery_guarantee = "enforced"
    path               = "/var/log/nomad/audit.log"
    rotate_bytes       = 104857600
    rotate_max_files   = 5
  }
}
```

Captures API requests and responses with user info. Forward to SIEM.

## Common Security Patterns

### Least-Privilege Tokens

Create narrow policies per role:

- `dev-submit`: submit jobs in dev namespace
- `prod-read`: read-only in prod
- `ops-drain`: drain nodes (operator:write, node:write)

Tokens scoped to a person should encode their role. Use SCIM or automation for lifecycle.

### Break-Glass Management Token

Keep one management token in a safe (physical or Vault). Never commit to git. Rotate periodically.

### Signed Short-Lived Tokens

Use Vault's Nomad secrets engine to issue short-lived tokens:

```
vault read nomad/creds/dev-role
```

Returns a fresh token each call. Combine with Vault auth (OIDC, AppRole) for auditable, revocable access.

### TLS Everywhere

Do not run production without TLS on all listeners. Automate cert rotation.

## Federation vs Multi-Region Active-Active

Federation does not replicate job state. Each region runs its own jobs. "Active-active" across regions means running separate jobs in each (with cross-region service discovery if Consul is federated too).

## Exam-Ready Checklist

- [ ] Can enable ACLs and bootstrap
- [ ] Can write and apply policies
- [ ] Know policy levels (deny, read, write) and capabilities
- [ ] Understand management vs client tokens
- [ ] Can configure Vault integration in agent config and jobspec
- [ ] Know federation setup and cross-region job submission
- [ ] Understand gossip encryption and TLS for agent communication
- [ ] Can describe namespaces for multi-tenancy
