# Nomad Architecture

Nomad is a simple, flexible workload orchestrator. A single binary runs in two modes (server or client) and coordinates to schedule tasks across the cluster. Understanding the architecture is the foundation for every other topic.

## Agent: Server or Client

Nomad's single binary (`nomad`) runs in two roles:

- **Server:** part of the control plane. Participates in Raft consensus. Stores cluster state.
- **Client:** part of the data plane. Runs allocations. Reports status.

A single agent can run in either mode, or both (not recommended for production).

```
# Server config
server {
  enabled          = true
  bootstrap_expect = 3
}

# Client config
client {
  enabled = true
  servers = ["server1:4647", "server2:4647", "server3:4647"]
}
```

## Cluster Topology

```
                ┌────────────────────────────────────┐
                │       Nomad Servers (3 or 5)       │
                │         Raft consensus             │
                └─────────────┬──────────────────────┘
                              │ RPC (4647)
                              │ Serf gossip (4648)
                              ▼
               ┌────────────────────────────────┐
               │  Nomad Clients (many)          │
               │  Run allocations (tasks)       │
               └────────────────────────────────┘
```

Servers form a Raft cluster for strong consistency. Clients connect to any server and register.

## Raft Consensus

Raft ensures server cluster agreement on state. Requirements:

- Quorum: (N/2)+1 servers must be available for writes
- Odd numbers preferred (3, 5, 7)
- 3 servers: quorum 2, tolerates 1 failure
- 5 servers: quorum 3, tolerates 2 failures

Leader election happens automatically when the leader fails. A new leader is chosen within seconds.

## Gossip (Serf)

Servers and clients use Serf for membership discovery and failure detection. Two gossip pools:

- **LAN gossip:** within a region (fast, tight)
- **WAN gossip:** across regions, only between servers (for federation)

Port 4648 by default, UDP and TCP.

## Regions and Datacenters

- **Region:** independent Nomad cluster with its own servers. Regions federate via WAN gossip.
- **Datacenter:** a logical partition within a region (e.g., physical DC or AZ).
- **Nodes:** Nomad client agents.

A job can target:

- One or more datacenters (`datacenters = ["dc1", "dc2"]`)
- A specific region (`region = "us-west"`)

Federation allows cross-region job submissions with `-region` flag but scheduling is per-region.

## Scheduler

The scheduler runs on the server leader. Its job: for each submitted job, produce an allocation plan.

Scheduler flow:

1. Job submitted
2. Server creates an evaluation
3. Evaluation consumed by scheduler
4. Scheduler computes placements (bin-packing, spread, etc.)
5. Allocations created and dispatched to clients
6. Clients start the tasks

Nomad has specialized schedulers:

- **service:** optimizes for long-running with bin-packing
- **batch:** similar, but more forgiving
- **system:** runs on every node
- **sysbatch:** runs to completion on every node

## Allocation Lifecycle

```
pending -> running -> complete
                  \-> failed -> restarting / rescheduled
```

- **pending:** scheduled but not yet running
- **running:** task(s) healthy
- **complete:** batch job finished
- **failed:** task failed beyond restart limits

## Tasks, Groups, Jobs

- **Task:** single unit of work (a container, a JVM, a process)
- **Group:** one or more tasks that share network, volumes, placement
- **Job:** one or more groups

Allocations are per-group: each group's count determines how many allocations exist.

## State Storage

Servers store state in Raft (in-memory with persistent log). Clients cache their own allocation state in the data directory for resilience.

Back up by snapshotting the leader:

```
nomad operator snapshot save backup.snap
nomad operator snapshot restore backup.snap
```

## Networking

Server-to-server: RPC on port 4647, encrypted via TLS if configured.

Client-to-server: RPC on 4647.

Gossip: 4648 UDP/TCP.

HTTP API and UI: 4646, TLS optional.

## HCP Nomad (in beta)

HashiCorp's managed Nomad offering. Servers in HCP; clients in your VPC. Reduces operational burden for small teams. Feature parity continues to evolve.

## Enterprise Features

- **Namespaces:** multi-tenancy (now in OSS 1.0+)
- **Resource Quotas:** caps on CPU/memory per namespace
- **Sentinel:** policy as code
- **Multi-Cluster:** unified view of multiple clusters
- **Audit Logging:** detailed compliance logs
- **Preemption:** higher-priority jobs can evict lower

## Bootstrap

Starting a new Nomad cluster:

1. Configure 3 (or 5) server nodes with `bootstrap_expect = 3`
2. Start them; they elect a leader via Raft
3. Configure clients with `servers = [...]`
4. Clients register; leader assigns them
5. If ACLs enabled: `nomad acl bootstrap`

## Configuration File Layout

Nomad supports both HCL and JSON config. Typical layout:

```
/etc/nomad.d/
├── nomad.hcl
└── server.hcl
```

Agent reads all `.hcl` / `.json` files recursively from `-config` directory.

## Example Server Config

```hcl
data_dir  = "/opt/nomad/data"
bind_addr = "0.0.0.0"

advertise {
  http = "10.0.0.1:4646"
  rpc  = "10.0.0.1:4647"
  serf = "10.0.0.1:4648"
}

server {
  enabled          = true
  bootstrap_expect = 3
  encrypt          = "base64-key"
  server_join {
    retry_join = ["server1:4648", "server2:4648", "server3:4648"]
  }
}

acl {
  enabled = true
}

telemetry {
  prometheus_metrics         = true
  disable_hostname           = true
  collection_interval        = "10s"
  publish_allocation_metrics = true
  publish_node_metrics       = true
}
```

## Example Client Config

```hcl
data_dir  = "/opt/nomad/data"
bind_addr = "0.0.0.0"

client {
  enabled = true
  servers = ["server1:4647", "server2:4647", "server3:4647"]

  meta {
    environment = "production"
    rack        = "rack-1"
  }

  host_volume "data" {
    path      = "/opt/data"
    read_only = false
  }

  node_class = "compute"
}

plugin "docker" {
  config {
    allow_privileged = false
  }
}
```

## CLI Discovery

```
nomad server members         # see cluster members
nomad node status            # see client nodes
nomad operator raft list-peers   # inspect Raft cluster
nomad operator api /v1/status/leader   # who is leader
```

## Leader Election and Failure

If the leader crashes, Raft elects a new one within seconds. During election, writes block momentarily; reads can still serve from any server (eventually consistent).

Clients talking to a crashed server reconnect to another server automatically (they try the full list).

## TLS for Agent Communication

Production deployments enable TLS on all ports:

```hcl
tls {
  http = true
  rpc  = true
  ca_file   = "/etc/nomad.d/ca.pem"
  cert_file = "/etc/nomad.d/cert.pem"
  key_file  = "/etc/nomad.d/key.pem"
  verify_server_hostname = true
  verify_https_client    = true
}
```

Use `consul-terraform-sync` or `consul-template` to rotate certs.

## Exam-Ready Checklist

- [ ] Can describe servers vs clients vs agents
- [ ] Know Raft quorum math
- [ ] Understand regions, datacenters, nodes
- [ ] Know default ports 4646 / 4647 / 4648
- [ ] Can read and author a basic agent config
- [ ] Understand allocation lifecycle
- [ ] Know federation between regions via WAN gossip

## Key terms

- **Server agent** - a Nomad agent that maintains cluster state, takes part in Raft and makes scheduling decisions.
- **Client agent** - a Nomad agent that registers with the servers and runs the tasks allocated to its node.
- **Raft** - the consensus protocol Nomad servers use to replicate state and elect a leader.
- **Region** - a Nomad cluster boundary that holds its own servers and state, and can be federated with other regions.
- **Datacenter** - a grouping of client nodes inside a region, used to place jobs.
- **Gossip protocol** - the Serf-based protocol servers use to discover each other and detect failures.
