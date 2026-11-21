# Nomad Associate - Real-World Scenarios

## Scenario 1: Rolling Update with Canary

**Question:** You have a web service running 10 instances. You want to deploy v2 safely, testing with 1 instance before promoting. Users should see zero downtime. How do you configure the jobspec?

**Answer:** Use an `update` block with canary:

```hcl
update {
  max_parallel     = 2
  canary           = 1
  min_healthy_time = "30s"
  healthy_deadline = "5m"
  auto_revert      = true
  auto_promote     = false
}
```

Submit the new version. Nomad deploys 1 canary alongside the 10 existing. Check health: `nomad deployment status <id>`. Promote with `nomad deployment promote <id>`. Nomad rolls out in batches of 2 at a time (max_parallel). If health checks fail, auto_revert rolls back.

## Scenario 2: Persistent Storage for PostgreSQL

**Question:** Your PostgreSQL database needs persistent storage that survives allocation restarts. The cluster is on-prem with local disks, not cloud. What do you configure?

**Answer:** Use host volumes. On each client node (or the designated DB host), add to the agent config:

```hcl
client {
  host_volume "postgres-data" {
    path      = "/opt/postgres"
    read_only = false
  }
}
```

In the jobspec:

```hcl
group "db" {
  volume "data" {
    type   = "host"
    source = "postgres-data"
  }

  constraint {
    attribute = "${meta.storage}"
    value     = "nvme"    # ensure it lands on the node with the host volume
  }

  task "postgres" {
    volume_mount {
      volume      = "data"
      destination = "/var/lib/postgresql"
    }
  }
}
```

For cloud with dynamic provisioning, use a CSI plugin (AWS EBS, Azure Disk, GCP PD) instead of host volumes.

## Scenario 3: Run a Daemon on Every Node

**Question:** You need to run a log-collecting agent on every client node. New nodes joining should automatically get the agent. Old nodes leaving should stop it.

**Answer:** Use a `system` job type:

```hcl
job "log-agent" {
  datacenters = ["dc1"]
  type        = "system"

  group "agent" {
    task "fluentbit" {
      driver = "docker"
      config {
        image = "fluent/fluent-bit:latest"
        network_mode = "host"
      }
    }
  }
}
```

`type = "system"` schedules one allocation per client matching datacenters/constraints. Nomad auto-adds to new joiners and cleans up on node removal.

## Scenario 4: Parameterized Job for Data Processing

**Question:** You have a data pipeline that processes files uploaded to S3. Each file needs a one-off processing run. You want to trigger processing on demand with file-specific parameters.

**Answer:** Use a parameterized job:

```hcl
job "process-file" {
  datacenters = ["dc1"]
  type        = "batch"

  parameterized {
    payload       = "optional"
    meta_required = ["file_key", "bucket"]
  }

  group "worker" {
    task "process" {
      driver = "docker"
      config {
        image = "processor:v1"
      }
      env {
        FILE_KEY = "${NOMAD_META_file_key}"
        BUCKET   = "${NOMAD_META_bucket}"
      }
    }
  }
}
```

Register the job once. Dispatch per file:

```
nomad job dispatch -meta file_key=2026/04/data.csv -meta bucket=ingest process-file
```

Each dispatch creates a new job instance that runs to completion.

## Scenario 5: Cross-Region Job Placement

**Question:** Your cluster spans `us-east` and `us-west` regions. A specific job must only run in `us-west`. Another job should run in whichever region has capacity.

**Answer:** For region-specific:

```hcl
job "west-only" {
  region      = "us-west"
  datacenters = ["dc-west-1", "dc-west-2"]
  # ...
}
```

For "either region with capacity": Nomad does not natively load-balance across regions for a single job. You would submit the job to both regions and let scheduling fill each. Alternatively, use a higher-level tool (nomad-pack template, CI logic) to decide which region gets the job based on capacity.

## Scenario 6: Secret Injection from Vault

**Question:** A web service needs a database password stored in Vault. The password must not appear in the jobspec or environment in plaintext in the Nomad API. How?

**Answer:** Use Vault integration:

```hcl
vault {
  policies = ["db-read"]
}

template {
  data = <<EOH
{{ with secret "kv/data/myapp/db" }}
DB_PASSWORD={{ .Data.data.password }}
{{ end }}
EOH
  destination = "secrets/db.env"
  env         = true
  change_mode = "restart"
}
```

Nomad acquires a Vault token for the task, renders the template locally on the client, and exposes it only to the task. Nomad's API shows the jobspec with the Vault path, not the secret value. The template lives in the task's `/secrets` (not `/local`), which is tmpfs.

## Scenario 7: Consul Connect Service Mesh

**Question:** You have two services, `frontend` and `backend`. They must only talk to each other over mTLS. How do you configure them?

**Answer:** Enable Consul Connect sidecars on both:

```hcl
# frontend jobspec
group "frontend" {
  network {
    mode = "bridge"
    port "http" { to = 8080 }
  }

  service {
    name = "frontend"
    port = "http"
    connect {
      sidecar_service {
        proxy {
          upstreams {
            destination_name = "backend"
            local_bind_port  = 9000
          }
        }
      }
    }
  }

  task "app" { driver = "docker"; config { image = "frontend:v1" } }
}
```

Frontend now reaches backend via `localhost:9000`. The Envoy sidecar handles mTLS. Define a Consul intention `frontend -> backend` to authorize the flow.

## Scenario 8: Preventing Co-Location

**Question:** You have a Redis cluster of 3 nodes. All 3 must run on different hosts for availability. How do you configure this?

**Answer:** Use a `distinct_hosts` constraint at the group level:

```hcl
group "redis" {
  count = 3
  constraint {
    operator = "distinct_hosts"
    value    = "true"
  }
  # ...
}
```

Nomad will not place two allocations from this group on the same client. If fewer than 3 eligible nodes, placement stalls.

## Scenario 9: ACL for a Dev Team

**Question:** Your dev team should be able to submit jobs to the `dev` namespace, read logs, but not touch the `prod` namespace or cluster-level operations. Write the ACL policy.

**Answer:**

```hcl
namespace "dev" {
  policy = "write"
  capabilities = ["submit-job", "dispatch-job", "read-logs", "alloc-exec"]
}

namespace "prod" {
  policy = "deny"
}

node {
  policy = "read"
}

agent {
  policy = "deny"
}
```

Create the policy: `nomad acl policy apply dev-team dev-team.hcl`. Create a token with this policy: `nomad acl token create -policy=dev-team`. Distribute the token to the team.

## Scenario 10: Node Drain for Maintenance

**Question:** You need to take a node offline for kernel patching. Allocations must move to other nodes with zero downtime.

**Answer:** Drain the node:

```
nomad node drain -enable -deadline=1h <node-id>
```

Behavior:

- Node marked ineligible for new allocations
- Existing allocations get rescheduled onto other nodes
- Respects `migrate` stanza for service jobs (rolling, not all at once)
- If deadline reached, remaining allocs forcibly stopped

Once drain completes, reboot or patch the node. Re-enable: `nomad node eligibility -enable <node-id>`.

## Scenario 11: Scaling Based on Queue Depth

**Question:** Your worker jobs process messages from an SQS queue. Queue depth varies dramatically. You want Nomad to autoscale workers based on depth.

**Answer:** Deploy the Nomad Autoscaler (separate binary). Configure an APM-based policy:

```hcl
scaling "workers" {
  enabled = true
  min     = 2
  max     = 50

  policy {
    cooldown            = "1m"
    evaluation_interval = "30s"

    check "queue_depth" {
      source = "prometheus"
      query  = "aws_sqs_approximate_number_of_messages_visible{queue=\"work-queue\"}"

      strategy "target-value" {
        target = 10
      }
    }
  }
}
```

Autoscaler queries Prometheus, adjusts the job's count via Nomad API to maintain 10 messages per worker. Set min/max to bound.

## Scenario 12: Migrating from Docker Compose

**Question:** You have a Docker Compose file with 3 services (web, api, db). Migrate to Nomad. What's the equivalent?

**Answer:** A single Nomad job with 3 task groups (or 3 separate jobs depending on lifecycle):

```hcl
job "myapp" {
  datacenters = ["dc1"]

  group "web" {
    count = 2
    network { port "http" { to = 80 } }
    service { name = "web"; port = "http" }
    task "nginx" {
      driver = "docker"
      config { image = "nginx:1.25"; ports = ["http"] }
    }
  }

  group "api" {
    count = 3
    network { port "api" { to = 8080 } }
    service {
      name = "api"
      port = "api"
      connect { sidecar_service {} }
    }
    task "app" {
      driver = "docker"
      config { image = "myapi:v1" }
    }
  }

  group "db" {
    count = 1
    volume "data" { type = "host"; source = "db-data" }
    task "postgres" {
      driver = "docker"
      config { image = "postgres:16" }
      volume_mount { volume = "data"; destination = "/var/lib/postgresql" }
    }
  }
}
```

Prefer separate jobs if lifecycles diverge (e.g., db rarely changes; api deploys hourly).
