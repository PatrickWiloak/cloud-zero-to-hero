# Nomad - Common Traps

> **This is a self-directed study track, not a certification guide.** HashiCorp's [certifications page](https://developer.hashicorp.com/certifications) (checked 2026-11-21) lists no Nomad exam, only Terraform and Vault exams. Earlier versions of this guide quoted a cost, question count, passing score and domain weights for a "Nomad Associate" exam; none of those had a vendor source, so they are removed. The notes, scenarios and labs still teach Nomad as it is used in practice.

The mistakes people make most often with Nomad, and how to tell the options apart.

## Common Trap Patterns

### Job Type Confusion

- `service`: long-running, auto-restart, scalable
- `batch`: run to completion, not restarted
- `system`: one allocation per node in scope (like K8s DaemonSet)
- `sysbatch`: run to completion on every node (one-off cluster ops)

Questions describe behavior, ask for the type. Know all four.

### Driver Selection

- `docker` for container images
- `exec` for chrooted/cgrouped native binaries
- `raw_exec` for untrusted/unsandboxed (disabled by default)
- `java` for JAR files
- `qemu` for KVM VMs
- `podman`, `containerd` as Docker alternatives

Watch for wrong driver assignments (e.g., "java" for a JAR is correct; "exec" is wrong though technically possible).

### Network Modes

- `host`: task shares host network; ports are host ports
- `bridge`: Nomad creates a network namespace with NAT
- `none`: no network
- CNI plugins: custom (calico, etc.)

`bridge` is common and supports port mapping. `host` is high-performance but no isolation.

### Service Provider

- `provider = "consul"` (default): registers with Consul
- `provider = "nomad"` (1.3+): Nomad native catalog

Some questions ask which requires Consul installed. Only the consul provider does.

### Constraints vs Affinities

- **Constraints:** hard requirements; fail to place if unmet
- **Affinities:** soft preferences with weights; scheduler prefers but doesn't require

Questions describing "must" or "required" want constraints. "Prefer" or "should" wants affinities.

### Canary vs Rolling Update

Canary: N new-version instances run alongside old. Promote manually (or via auto_promote) to replace all.
Rolling: no overlap; each old instance replaced one at a time.

### Restart vs Reschedule

- **restart:** task stays on same alloc, Nomad restarts the task
- **reschedule:** alloc itself moves (to a new node) after restart attempts exhausted

Restart first, then reschedule.

### Raft Quorum Math

- 3 servers: quorum 2, tolerates 1 failure
- 5 servers: quorum 3, tolerates 2 failures
- 7 servers: quorum 4, tolerates 3 failures
- Recommended: 3 for small, 5 for large. Never use even numbers.

### System Jobs Don't Honor count

`system` and `sysbatch` jobs run one allocation per node matching constraints. `count` is ignored or implied.

### Default Ports

- 4646: HTTP API and UI
- 4647: RPC
- 4648: Serf gossip

Memorize these.

### Namespace vs Region

- Namespace: logical partition for multi-tenancy
- Region: physical grouping (independent servers)

A job belongs to one region and one namespace.

## Questions worth answering

- Which files are auto-loaded? (Nomad reads `-config` directory recursively)
- What does `nomad job plan` do? (Dry run, shows diff and scheduling result)
- What's the difference between `-purge` and regular stop? (Purge removes job spec from state entirely)
- How do periodic jobs work? (Cron-like `periodic { cron = "..." }`)
- How does service mesh work with Consul Connect? (Sidecar proxy injected per task)
- When is preemption used? (Higher-priority jobs can evict lower-priority)

