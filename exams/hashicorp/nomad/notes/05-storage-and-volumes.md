# Storage and Volumes

Workloads need persistent storage. Nomad supports ephemeral disk, host volumes (pre-declared on clients), and CSI volumes (Container Storage Interface plugins for cloud block storage and network storage).

## Ephemeral Disk

Every task group gets some ephemeral disk on the client's host. The allocation directory (`/opt/nomad/data/alloc/<alloc-id>/`) contains:

- `alloc/`: shared across tasks in the group
- `<task>/local/`: per-task writable
- `<task>/secrets/`: per-task tmpfs (cleared on shutdown, not persisted)
- `<task>/tmp/`: tmpfs

Configure:

```hcl
group "web" {
  ephemeral_disk {
    sticky  = true
    migrate = true
    size    = 500      # MiB
  }
}
```

Attributes:

- **sticky:** try to reuse the same client's disk when the allocation restarts
- **migrate:** copy disk contents when allocation moves (requires sticky)
- **size:** reservation in MiB

Use for app caches, temp files, build artifacts. Not for databases (data loss risk).

## Host Volumes

Pre-declared directories on client nodes that jobs can mount.

### Client Configuration

```hcl
# /etc/nomad.d/client.hcl
client {
  enabled = true

  host_volume "postgres-data" {
    path      = "/opt/postgres"
    read_only = false
  }

  host_volume "shared-config" {
    path      = "/etc/shared"
    read_only = true
  }
}
```

The path must exist and be accessible by the task's user.

### Jobspec Consumption

```hcl
group "db" {
  volume "data" {
    type      = "host"
    source    = "postgres-data"
    read_only = false
  }

  constraint {
    attribute = "${meta.has_postgres_data}"
    value     = "true"
  }

  task "postgres" {
    driver = "docker"
    config { image = "postgres:16" }

    volume_mount {
      volume      = "data"
      destination = "/var/lib/postgresql/data"
      read_only   = false
    }
  }
}
```

Caveats:

- Only nodes that declared this host volume can host the allocation
- If one node declares the volume, only that node will run it (effective 1-replica)
- Combine with `distinct_hosts` constraint if multiple nodes have the same volume name

## CSI Volumes

CSI (Container Storage Interface) plugins allow Nomad to use cloud block storage (AWS EBS, Azure Disk, GCP PD), network storage (NFS, Ceph), and SAN arrays dynamically.

### CSI Plugin Types

- **controller:** runs on servers/clients; talks to the storage backend API
- **node:** runs on each client; mounts volumes into tasks
- **monolith:** combined controller + node

Deploy CSI plugins as Nomad jobs:

```hcl
job "ebs-csi" {
  type = "system"

  group "nodes" {
    task "plugin" {
      driver = "docker"

      config {
        image = "public.ecr.aws/ebs-csi-driver/aws-ebs-csi-driver:v1.28.0"
        args = [
          "node",
          "--endpoint=unix:///csi/csi.sock",
        ]
        privileged = true
      }

      csi_plugin {
        id        = "aws-ebs0"
        type      = "node"
        mount_dir = "/csi"
      }
    }
  }
}
```

### Registering a CSI Volume

Two modes:

- **Dynamic:** use `nomad volume create` to provision new storage
- **Register existing:** use `nomad volume register` for pre-existing storage

```hcl
# volume.hcl
id           = "postgres-ebs"
name         = "postgres-ebs"
type         = "csi"
plugin_id    = "aws-ebs0"
external_id  = "vol-0abc123"      # existing EBS volume ID
capacity_min = "10GiB"
capacity_max = "10GiB"

capability {
  access_mode     = "single-node-writer"
  attachment_mode = "file-system"
}

mount_options {
  fs_type = "ext4"
}
```

```
nomad volume register volume.hcl
```

### Jobspec Consumption

```hcl
group "db" {
  volume "data" {
    type            = "csi"
    source          = "postgres-ebs"
    attachment_mode = "file-system"
    access_mode     = "single-node-writer"
  }

  task "postgres" {
    volume_mount {
      volume      = "data"
      destination = "/var/lib/postgresql/data"
    }
  }
}
```

## Access Modes

| Mode | Meaning |
|------|---------|
| single-node-reader-only | 1 node, read-only |
| single-node-writer | 1 node, read-write |
| multi-node-reader-only | many nodes, read-only |
| multi-node-single-writer | many readers, one writer |
| multi-node-multi-writer | many readers and writers (rare; depends on storage) |

EBS supports single-node-writer. EFS supports multi-node-multi-writer. Choose based on your storage backend's capabilities.

## Attachment Modes

- **file-system:** mount as a filesystem path (common)
- **block-device:** raw block device (for apps that manage their own filesystem)

## Volume Lifecycle

```
nomad volume status           # list volumes
nomad volume status <id>      # detail
nomad volume register file.hcl
nomad volume create file.hcl  # dynamic provisioning
nomad volume deregister <id>
nomad volume delete <id>      # deletes underlying storage (dynamic)
```

When a job claims a volume, Nomad attaches it to the chosen node. On allocation termination, Nomad detaches.

## Volume Claim Concurrency

`single-node-writer` CSI volumes can only be mounted by one node at a time. If you scale to multiple allocations, placement serializes or fails. Plan accordingly:

- For stateful singletons (database primaries): count=1 with constraint
- For shared access: use multi-node capable storage (EFS, GlusterFS, Ceph)

## Volumes Across Restarts

When an allocation restarts on the same node:

- Host volumes: same path, no remount needed
- CSI volumes: Nomad re-attaches; minor delay possible
- Ephemeral disk: sticky flag keeps contents if set

When an allocation moves to a different node:

- Host volumes: placement fails unless target node has the volume declared
- CSI volumes: detach from old, attach to new (seconds to minutes)
- Ephemeral disk: migrate flag copies contents over if enabled

## Secrets vs Persistent Data

Never store long-lived secrets on a volume. Use Vault + `template` for secrets. Volumes are for data: databases, queues, caches.

## Common Volume Patterns

### Stateful Singleton (Postgres primary)

```hcl
group "postgres" {
  count = 1
  volume "data" { type = "host"; source = "postgres-data" }
  constraint {
    attribute = "${meta.has_postgres}"
    value     = "true"
  }
}
```

### Replicated with CSI (e.g., MongoDB replica set with per-replica volumes)

Each replica as a separate group or separate job, each claiming its own CSI volume:

```hcl
job "mongo-0" {
  group "replica" {
    volume "data" {
      type   = "csi"
      source = "mongo-0-volume"
      access_mode = "single-node-writer"
    }
  }
}

job "mongo-1" { ... source = "mongo-1-volume" ... }
```

### Shared Read Across Nodes

Use EFS or similar with `multi-node-reader-only`:

```hcl
volume "shared" {
  type            = "csi"
  source          = "shared-efs"
  access_mode     = "multi-node-reader-only"
  attachment_mode = "file-system"
}
```

## Plugin Health

```
nomad plugin status
nomad plugin status aws-ebs0
```

CSI plugins must be healthy before volumes attach. Common issues:

- Wrong IAM permissions (cloud plugins)
- Missing kernel modules (for local filesystem plugins)
- Networking between plugin and storage backend

## Alternatives to Nomad-Managed Volumes

Sometimes it's simpler to bypass Nomad's volume abstraction:

- Application-level replication (e.g., Consul, etcd, Cassandra) without needing shared storage
- Mount manually via task config (Docker `volumes = ["/host/path:/container/path"]`)
- External stateful systems (RDS, ElastiCache) with Nomad only running stateless apps

## Exam-Ready Checklist

- [ ] Understand ephemeral disk and sticky/migrate flags
- [ ] Can configure and consume a host volume
- [ ] Understand CSI plugin types (controller, node, monolith)
- [ ] Can write a volume registration HCL
- [ ] Know access modes and which storage supports which
- [ ] Understand attachment modes
- [ ] Know the volume lifecycle commands
