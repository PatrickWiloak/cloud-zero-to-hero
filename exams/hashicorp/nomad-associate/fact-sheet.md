---
last-updated: 2026-11-21
---

# Nomad - Fact Sheet

> **This is a self-directed study track, not a certification guide.** HashiCorp's [certifications page](https://developer.hashicorp.com/certifications) (checked 2026-11-21) lists no Nomad exam, only Terraform and Vault exams. Earlier versions of this guide quoted a cost, question count, passing score and domain weights for a "Nomad Associate" exam; none of those had a vendor source, so they are removed. The notes, scenarios and labs still teach Nomad as it is used in practice.

## Topic areas

### Domain 1: Architecture and Cluster Concepts

- Servers and clients
- Raft consensus and leader election
- Regions, datacenters, nodes
- Federation (multi-region)
- Gossip protocol
- Scheduler internals (reconciler, planner)
- HCP Nomad vs self-managed

### Domain 2: Job Specifications (HCL)

- Jobs, groups, tasks structure
- Job types: `service`, `batch`, `system`, `sysbatch`
- Task drivers: `docker`, `exec`, `raw_exec`, `java`, `qemu`, `containerd`, `podman`
- Resources: `cpu`, `memory`, `disk`
- `template` stanza (consul-template integration)
- `config` and `env` blocks
- `artifact` stanza (fetch remote files)
- `update` stanza (rolling updates, canaries)
- `reschedule` and `restart` stanzas
- `migrate` stanza (blue/green migrations)
- Constraints and affinities
- Spreads

### Domain 3: Scheduling and Allocations

- Bin-packing (default)
- Spread scheduling
- System jobs (run on all nodes)
- Batch jobs and sysbatch
- Parameterized jobs and dispatch
- Periodic jobs (cron-like)
- `nomad job run`, `plan`, `status`, `stop`
- Allocations, evaluations, deployments
- Preemption
- Task groups and scaling

### Domain 4: Networking and Service Discovery

- Network modes: `host`, `bridge`, `none`, CNI
- Static and dynamic ports
- Expose labels
- Consul service registration
- Nomad-native service discovery (without Consul, 1.3+)
- Check types (http, tcp, script, grpc)
- Consul Connect / service mesh sidecars
- Ingress with Consul or Traefik

### Domain 5: Storage and Volumes

- Ephemeral disk
- Host volumes (pre-declared on the client)
- CSI volumes (Container Storage Interface)
- Volume types (stateful workloads)
- `mount` block in task
- Volume lifecycle: register, create, claim, release

### Domain 6: ACL Security and Federation

- Bootstrap ACL
- Tokens: management, client
- Policies in HCL
- Sentinel integration (Enterprise)
- Workload Identity
- Federation setup between regions
- TLS for agent communication
- Vault integration for secrets

## Key CLI Commands

```
# Agent
nomad agent -dev                                # single-node dev
nomad agent -config=/etc/nomad.d/             # production agent

# Jobs
nomad job init                                  # generate sample jobspec
nomad job run example.nomad                    # submit job
nomad job plan example.nomad                   # dry-run plan
nomad job status [job]
nomad job stop [-purge] [job]
nomad job restart -all-tasks [job]
nomad job revert [job] [version]
nomad job history [job]

# Allocations
nomad alloc status [alloc-id]
nomad alloc logs [-f] [-stderr] [alloc-id] [task]
nomad alloc exec [alloc-id] [task] [cmd]
nomad alloc signal -signal=SIGTERM [alloc-id]
nomad alloc stop [alloc-id]

# Nodes
nomad node status
nomad node drain -enable [-deadline=1h] [node-id]
nomad node eligibility -disable [node-id]

# Namespaces (Enterprise+OSS 1.0+)
nomad namespace list
nomad namespace apply -description="Dev" dev

# ACLs
nomad acl bootstrap
nomad acl token create -policy=dev
nomad acl policy apply dev policy.hcl

# Sentinel (Enterprise)
nomad sentinel apply policy.sentinel

# System
nomad server members
nomad operator raft list-peers
nomad status [job|node|alloc]
```

## Minimal Job Spec

```hcl
job "web" {
  datacenters = ["dc1"]
  type        = "service"

  group "frontend" {
    count = 3

    network {
      port "http" {
        to = 8080
      }
    }

    service {
      name = "web-frontend"
      port = "http"
      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "nginx" {
      driver = "docker"
      config {
        image = "nginx:1.25"
        ports = ["http"]
      }
      resources {
        cpu    = 500
        memory = 256
      }
    }
  }
}
```

## Job Types

| Type | Purpose |
|------|---------|
| `service` | Long-running, auto-restart, count-based |
| `batch` | Run to completion; not auto-restarted |
| `system` | Runs on every node in the targeted set |
| `sysbatch` | Runs to completion on every node (one-off ops) |

## Task Drivers

| Driver | Runs |
|--------|------|
| `docker` | Docker images (default for most) |
| `podman` | Podman containers |
| `containerd` | containerd (Nomad 1.6+ plugin) |
| `exec` | Isolated exec (chroot + cgroups) |
| `raw_exec` | Non-isolated (risky; disabled by default) |
| `java` | JAR files in a JVM |
| `qemu` | KVM virtual machines |
| `nspawn` | systemd-nspawn containers |

## Resources Stanza

```hcl
resources {
  cpu        = 500   # MHz
  memory     = 256   # MiB
  memory_max = 512   # MiB soft limit (Enterprise)
  disk       = 200   # MiB ephemeral disk
}
```

CPU is measured in MHz, not cores. Nomad reserves proportionally.

## Template Stanza

```hcl
template {
  data = <<EOH
DB_HOST={{ key "app/db/host" }}
API_KEY={{ with secret "secret/myapp" }}{{ .Data.data.api_key }}{{ end }}
EOH
  destination = "local/app.env"
  env         = true
  change_mode = "restart"
}
```

Uses consul-template syntax. Supports Consul KV, Vault secrets, env vars. `change_mode`: `restart`, `signal`, `noop`.

## Constraint Examples

```hcl
constraint {
  attribute = "${attr.kernel.name}"
  value     = "linux"
}

constraint {
  attribute = "${meta.environment}"
  value     = "production"
}

constraint {
  attribute = "${attr.cpu.arch}"
  operator  = "set_contains"
  value     = "amd64"
}
```

Operators: `=`, `!=`, `>=`, `<=`, `regexp`, `set_contains`, `distinct_hosts`, `distinct_property`, `semver`, `version`.

## Affinity Example

```hcl
affinity {
  attribute = "${meta.rack}"
  value     = "rack-a"
  weight    = 100
}
```

Affinities are soft preferences, not hard requirements. Weights range -100 to 100.

## Spread Example

```hcl
spread {
  attribute = "${node.datacenter}"
  target "dc1" { percent = 50 }
  target "dc2" { percent = 50 }
}
```

Encourage even distribution across an attribute.

## Service Registration (Consul)

```hcl
service {
  name     = "api"
  port     = "http"
  provider = "consul"     # default; or "nomad" for native
  tags     = ["v1", "canary"]

  check {
    type     = "http"
    path     = "/health"
    interval = "10s"
    timeout  = "2s"
  }

  connect {
    sidecar_service {}
  }
}
```

`provider = "nomad"` uses Nomad's native service catalog (no Consul required).

## Update Block (Rolling / Canary)

```hcl
update {
  max_parallel     = 2
  canary           = 1
  min_healthy_time = "30s"
  healthy_deadline = "5m"
  auto_revert      = true
  auto_promote     = false
  stagger          = "30s"
}
```

Canary = N instances of new version to run alongside old. Promote manually or via `auto_promote = true`.

## Reschedule and Restart Blocks

```hcl
restart {
  attempts = 3
  interval = "5m"
  delay    = "15s"
  mode     = "fail"   # or "delay"
}

reschedule {
  attempts       = 5
  interval       = "1h"
  delay          = "30s"
  delay_function = "exponential"
  max_delay      = "10m"
  unlimited      = false
}
```

`restart` governs task restarts on the same allocation. `reschedule` governs moving to a new allocation.

## Volumes

Host volume usage:

```hcl
group "db" {
  volume "data" {
    type      = "host"
    source    = "postgres-data"
    read_only = false
  }

  task "postgres" {
    volume_mount {
      volume      = "data"
      destination = "/var/lib/postgresql"
    }
  }
}
```

CSI volume:

```hcl
group "db" {
  volume "data" {
    type            = "csi"
    source          = "postgres-ebs"
    attachment_mode = "file-system"
    access_mode     = "single-node-writer"
  }
}
```

## ACL Policy Example

```hcl
namespace "default" {
  policy = "read"
  capabilities = ["submit-job", "read-logs"]
}

node {
  policy = "read"
}

agent {
  policy = "read"
}
```

## Federation

Multi-region Nomad:

- Each region has its own servers, clients
- Servers in different regions are linked via gossip
- Cross-region scheduling: `nomad job run -region=us-west`
- Periodic and parameterized jobs respect region

## Consul Integration

Three levels:

1. **Service registration:** Nomad registers services with Consul automatically
2. **Service mesh:** Consul Connect sidecars injected via `connect {}` stanza
3. **KV templates:** `template` stanza reads Consul KV for config

## Vault Integration

```hcl
vault {
  policies = ["db-read"]
}

template {
  data = "{{with secret \"database/creds/readonly\"}}{{.Data.username}}:{{.Data.password}}{{end}}"
  destination = "local/creds.env"
}
```

Nomad fetches a Vault token for the task, rotates it, revokes on stop.

## Enterprise Features (worth knowing)

- Namespaces (now in OSS 1.0+)
- Sentinel policy integration
- Resource quotas
- Multi-cluster
- Preemption (some scenarios OSS)
- Audit logging
- Autoscaler (separate binary)

## Web UI

Nomad bundles a web UI at `http://<server>:4646/ui/`:

- Browse jobs, allocations, nodes
- Start/stop/restart jobs
- View logs
- Exec into containers

## Default Ports

| Port | Purpose |
|------|---------|
| 4646 | HTTP API and UI |
| 4647 | RPC (server to server, client to server) |
| 4648 | Serf gossip (WAN + LAN) |

## Quick-fire facts

- Raft quorum requires (N/2)+1 servers for an N-server cluster
- Recommended server counts: 3 or 5 (odd numbers)
- Clients can scale to thousands per region
- The scheduler is eventually-consistent; placement can take seconds
- Jobs can target specific `datacenters` and `region`
- `nomad job plan` shows diff without running
- `-purge` flag on job stop removes the job spec entirely
- `nomad alloc logs` tails stdout; `-stderr` for stderr
- Service discovery provider is `consul` by default in service blocks
- Native Nomad services (`provider = "nomad"`) added in 1.3
