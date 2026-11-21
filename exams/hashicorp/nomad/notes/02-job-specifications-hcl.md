# Job Specifications in HCL

Job specs are Nomad's declarative configuration language. This domain is the largest on the exam (roughly 25%). You must be able to read and author jobspecs comfortably, know each block's purpose, and understand the interactions between blocks.

## Top-Level Structure

```hcl
job "<name>" {
  region      = "global"
  datacenters = ["dc1"]
  namespace   = "default"
  type        = "service"
  priority    = 50

  meta {
    owner = "platform"
  }

  group "<name>" {
    count = 3

    network { /* ... */ }
    service { /* ... */ }
    volume "<name>" { /* ... */ }

    task "<name>" {
      driver = "docker"
      config { /* ... */ }
      resources { /* ... */ }
      env { /* ... */ }
      template { /* ... */ }
      artifact { /* ... */ }
      volume_mount { /* ... */ }
    }

    update { /* ... */ }
    restart { /* ... */ }
    reschedule { /* ... */ }
  }

  constraint { /* ... */ }
  affinity { /* ... */ }
  spread { /* ... */ }
}
```

## Job Types

```hcl
type = "service"    # long-running, default
type = "batch"      # run to completion
type = "system"     # one per node in scope
type = "sysbatch"   # run to completion on every node
```

| Type | Restart | count honored | Typical Use |
|------|---------|---------------|-------------|
| service | yes, auto | yes | web servers, APIs |
| batch | no | yes | data processing, one-off |
| system | yes | no (one per node) | agents, exporters |
| sysbatch | no | no (one per node) | cluster-wide tasks |

## Periodic Jobs

Cron-style scheduling for batch jobs:

```hcl
job "cleanup" {
  type = "batch"
  periodic {
    cron             = "0 2 * * *"    # daily at 2 AM
    time_zone        = "UTC"
    prohibit_overlap = true
  }
}
```

`prohibit_overlap = true` prevents a new execution if the previous is still running.

## Parameterized Jobs

Dispatch-style jobs:

```hcl
job "data-processor" {
  type = "batch"
  parameterized {
    payload       = "optional"
    meta_required = ["file"]
    meta_optional = ["format"]
  }
}
```

Register once, dispatch many times:

```
nomad job dispatch -meta file=data.csv data-processor
```

Each dispatch creates a new instance of the job.

## Group Block

A group is a collection of tasks placed on the same client, sharing network and volumes.

```hcl
group "web" {
  count = 5

  ephemeral_disk {
    sticky  = true
    migrate = true
    size    = 500
  }

  migrate {
    max_parallel     = 2
    health_check     = "checks"
    min_healthy_time = "10s"
    healthy_deadline = "5m"
  }
}
```

## Task Block

```hcl
task "nginx" {
  driver = "docker"

  config {
    image = "nginx:1.25"
    ports = ["http"]
    volumes = [
      "local/nginx.conf:/etc/nginx/conf.d/default.conf"
    ]
  }

  env {
    LOG_LEVEL = "info"
  }

  resources {
    cpu    = 500
    memory = 256
  }

  kill_timeout = "30s"
  kill_signal  = "SIGTERM"
  shutdown_delay = "10s"
}
```

## Task Drivers

### Docker

```hcl
driver = "docker"
config {
  image    = "redis:7"
  args     = ["--maxmemory", "256mb"]
  ports    = ["redis"]
  hostname = "redis-${NOMAD_ALLOC_INDEX}"
  command  = "redis-server"
  work_dir = "/data"
  volumes  = ["local/config:/etc/redis"]
}
```

### Exec (isolated)

```hcl
driver = "exec"
config {
  command = "/usr/local/bin/myapp"
  args    = ["--port", "8080"]
}
```

Uses cgroups and chroot for isolation. Linux only.

### Raw Exec

```hcl
driver = "raw_exec"
```

No isolation; process runs as the Nomad agent user. Disabled by default; enable per-client. Use only for trusted workloads.

### Java

```hcl
driver = "java"
config {
  class_path = "/opt/app/*"
  jar_path   = "/opt/app/myapp.jar"
  jvm_options = ["-Xmx512m"]
}
```

### Others

- `qemu`: KVM VMs
- `podman`: Podman containers
- `containerd`: containerd
- `nspawn`: systemd-nspawn containers

## Resources

```hcl
resources {
  cpu    = 1000   # MHz (1 GHz)
  memory = 512    # MiB
  memory_max = 1024   # Enterprise: allow burst
  disk   = 200    # MiB ephemeral
}
```

CPU is MHz, not cores. A 2.4 GHz core = 2400 MHz. Scheduler bin-packs based on these.

## Env Block

```hcl
env {
  NODE_ENV    = "production"
  DB_HOST     = "db.service.consul"
  APP_VERSION = "${NOMAD_JOB_VERSION}"
}
```

Nomad runtime variables available:

- `NOMAD_ALLOC_ID`
- `NOMAD_ALLOC_NAME`
- `NOMAD_ALLOC_INDEX` (0, 1, 2, ... for count)
- `NOMAD_TASK_NAME`
- `NOMAD_JOB_NAME`
- `NOMAD_DC`
- `NOMAD_REGION`
- `NOMAD_IP_<port>`, `NOMAD_PORT_<port>`, `NOMAD_ADDR_<port>`
- `NOMAD_META_<key>`

## Template Block

Rendered on the client using consul-template syntax. Supports Consul, Vault, env vars.

```hcl
template {
  data = <<EOH
{{ range service "api" }}
SERVER {{ .Address }}:{{ .Port }}
{{ end }}
EOH
  destination = "local/upstream.conf"
  change_mode = "restart"
  change_signal = "SIGHUP"
  splay       = "1m"
  perms       = "644"
}
```

- `destination`: relative path. `local/` persists, `secrets/` is tmpfs.
- `env = true`: loads file as environment variables
- `change_mode`: `restart`, `signal`, `noop`
- `splay`: random delay to avoid thundering herd

## Artifact Block

Download files before the task starts:

```hcl
artifact {
  source      = "https://example.com/app.tar.gz"
  destination = "local/"
  mode        = "file"     # or "any", "dir"

  options {
    checksum = "sha256:abc123..."
  }
}
```

Supports http, https, git, s3, gcs protocols.

## Update Block (Deployments)

```hcl
update {
  max_parallel      = 2
  canary            = 1
  min_healthy_time  = "30s"
  healthy_deadline  = "5m"
  progress_deadline = "10m"
  auto_revert       = true
  auto_promote      = false
  stagger           = "30s"
}
```

- `canary`: number of new-version allocs to run alongside old before promote
- `auto_promote`: promote canaries when healthy
- `auto_revert`: rollback on failed health
- `stagger`: only for system jobs, delay between node updates

## Migrate Block

Governs allocation migration during node drains (service jobs only):

```hcl
migrate {
  max_parallel     = 2
  health_check     = "checks"
  min_healthy_time = "10s"
  healthy_deadline = "5m"
}
```

## Restart Block

```hcl
restart {
  attempts = 3
  interval = "5m"
  delay    = "15s"
  mode     = "fail"   # or "delay"
}
```

Mode:
- `fail`: after attempts exhausted, mark task failed
- `delay`: wait `interval` then retry

## Reschedule Block

```hcl
reschedule {
  attempts       = 5
  interval       = "1h"
  delay          = "30s"
  delay_function = "exponential"
  max_delay      = "10m"
  unlimited      = false
}
```

Reschedule moves an alloc to a new node; restart keeps it on the same.

## Constraint

Hard requirements:

```hcl
constraint {
  attribute = "${attr.kernel.name}"
  value     = "linux"
}

constraint {
  attribute = "${node.class}"
  operator  = "!="
  value     = "gpu"
}

constraint {
  operator = "distinct_hosts"
  value    = "true"
}
```

Operators: `=`, `!=`, `>`, `>=`, `<`, `<=`, `regexp`, `set_contains`, `set_contains_all`, `distinct_hosts`, `distinct_property`, `is_set`, `is_not_set`, `semver`, `version`.

## Affinity

Soft preferences:

```hcl
affinity {
  attribute = "${meta.rack}"
  value     = "rack-1"
  weight    = 100   # -100 to 100
}
```

## Spread

Encourage distribution across an attribute:

```hcl
spread {
  attribute = "${node.datacenter}"
  weight    = 100
  target "dc1" { percent = 50 }
  target "dc2" { percent = 50 }
}
```

## Service Block (covered in networking note)

Briefly:

```hcl
service {
  name = "api"
  port = "http"
  tags = ["v1"]
  check {
    type     = "http"
    path     = "/health"
    interval = "10s"
    timeout  = "2s"
  }
}
```

## Vault Block (Enterprise or with config)

```hcl
vault {
  policies       = ["db-read"]
  change_mode    = "restart"
  change_signal  = "SIGHUP"
  env            = true
}
```

Nomad obtains a Vault token for the task, renews it, revokes on stop.

## CSI / Host Volumes (covered in storage note)

## HCL vs JSON

Nomad accepts both HCL and JSON jobspecs. HCL is more readable. Convert: `nomad job run -json job.json` or `-output` flag during plan.

## Variables (HCL2)

Nomad supports HCL2 variable interpolation in jobspecs:

```hcl
variable "image_tag" {
  type    = string
  default = "latest"
}

job "web" {
  group "frontend" {
    task "nginx" {
      config {
        image = "nginx:${var.image_tag}"
      }
    }
  }
}
```

Pass via `-var='image_tag=v2'` or `-var-file=prod.vars.hcl`.

## Exam-Ready Checklist

- [ ] Can author a full jobspec from scratch
- [ ] Know the 4 job types and when to use each
- [ ] Know major task drivers
- [ ] Can use `template`, `artifact`, `vault`, `env`
- [ ] Understand update/canary flow
- [ ] Know constraint operators
- [ ] Know the difference between restart and reschedule
