# Scheduling and Allocations

Nomad's scheduler decides where allocations run. Understanding the scheduling model, the evaluation and deployment lifecycle, and how to influence placement is essential.

## Scheduler Basics

For each job submission or update:

1. Nomad creates an **evaluation** (represents "work to do")
2. The scheduler processes the evaluation
3. Scheduler computes **placements** (which clients run which allocations)
4. **Allocations** are created and sent to clients
5. Clients execute the allocations

The scheduler runs on the server leader and is eventually consistent.

## Scheduler Algorithms

### Bin-Packing (default for service, batch)

Minimize the number of nodes used. Fit as many allocations as possible on as few nodes as possible while respecting resources. Improves utilization.

### Spread (via spread block)

Distribute evenly across an attribute (datacenter, rack). Trade utilization for availability.

### System

One allocation per node matching the job's constraints.

## Evaluations

```
nomad eval list            # list all
nomad eval status <id>     # inspect
```

Evaluation states:

- **blocked:** waiting for resources
- **pending:** queued for scheduler
- **complete:** processed
- **failed:** scheduler error
- **cancelled:** superseded by newer eval

Blocked evaluations retry when node capacity changes.

## Allocations

```
nomad alloc status <id>       # detailed info
nomad alloc logs -f <id>      # tail logs
nomad alloc logs -stderr <id>
nomad alloc exec <id> <task> <cmd>
nomad alloc signal -signal=SIGHUP <id>
nomad alloc stop <id>
```

Allocation statuses:

- **pending:** scheduled, not yet started
- **running:** tasks active
- **complete:** batch finished
- **failed:** task failed
- **lost:** client disconnected

## Deployments (Service Jobs)

When a service job updates, Nomad creates a deployment to manage the rollout.

```
nomad deployment list
nomad deployment status <id>
nomad deployment promote <id>    # promote canaries
nomad deployment fail <id>       # mark failed, trigger revert
nomad deployment pause <id>
nomad deployment resume <id>
```

Deployment states:

- **running:** in progress
- **paused:** halted for manual control
- **successful:** all allocations healthy
- **failed:** health checks failed
- **cancelled:** superseded

## Canaries and Rolling Updates

With `canary = 1` in an update block, Nomad:

1. Deploys 1 new-version alloc alongside the existing fleet
2. Waits for `min_healthy_time` with all health checks passing
3. Requires manual `promote` (unless `auto_promote = true`)
4. On promote, replaces remaining old allocs in batches of `max_parallel`
5. If `healthy_deadline` expires, marks deployment failed and triggers `auto_revert` if set

## Blue/Green (via canary = count)

Set `canary = group.count` to deploy a full parallel copy. Promote to switch over.

## System Jobs

System jobs ignore count. They schedule one allocation per node where:

- Node matches job constraints
- Node matches group constraints
- Node's datacenter is in the job's `datacenters` list

When new nodes join, Nomad schedules system job allocations automatically. When nodes leave, allocations clean up.

## Sysbatch Jobs

Like system but run to completion. Useful for one-off cluster tasks (e.g., applying a kernel param across all nodes).

## Batch Jobs

Run to completion and don't restart. Count allocations are independent; each runs its own task execution.

## Preemption (Enterprise plus selected OSS)

Higher-priority jobs can evict lower-priority allocations to free resources. Priority range: 1 to 100 (default 50).

```hcl
job "critical" {
  priority = 90
  # ...
}
```

Preemption is per scheduler:

- System and sysbatch: always preempt lower-priority system jobs
- Service: preempt in OSS as of 1.6+
- Batch: preempt in Enterprise

Preempted allocations are rescheduled if possible.

## Placement Constraints vs Affinities vs Spreads

**Constraints:** must-haves. If no node satisfies, allocation stays pending.

**Affinities:** prefer-haves with weights. Scheduler tries to satisfy, but places anyway if no match.

**Spreads:** distribute across attribute values. Like affinities but target percentages.

Hierarchy of influence:

1. Constraints filter
2. Among remaining, compute score combining bin-pack + affinity + spread
3. Pick highest-scoring node

## Node Attributes

Every client reports attributes:

- `attr.kernel.name`: linux, darwin, windows
- `attr.kernel.version`
- `attr.cpu.arch`: amd64, arm64
- `attr.cpu.numcores`
- `attr.memory.totalbytes`
- `attr.unique.hostname`
- `attr.platform.aws.instance-type`
- `attr.driver.docker`: "1"
- `meta.<custom>`: user-defined

Use in constraints:

```hcl
constraint {
  attribute = "${attr.cpu.arch}"
  value     = "arm64"
}

constraint {
  attribute = "${meta.environment}"
  value     = "production"
}
```

## Node Classes

A simple taxonomy for scheduling:

```hcl
client {
  node_class = "gpu"
}
```

Target via constraint:

```hcl
constraint {
  attribute = "${node.class}"
  value     = "gpu"
}
```

## Node Drain

Gracefully move allocations off a node:

```
nomad node drain -enable -deadline=1h <node-id>
```

Allocations reschedule per their `migrate` stanza. Once drained, the node is ineligible until:

```
nomad node drain -disable <node-id>
nomad node eligibility -enable <node-id>
```

## Node Eligibility

Toggle without draining:

```
nomad node eligibility -disable <node-id>
nomad node eligibility -enable <node-id>
```

Ineligible nodes won't get new allocations but existing ones remain.

## Resource Quotas (Enterprise, OSS from 1.1+)

Limit resource consumption per namespace:

```hcl
quota "default-quota" {
  limit {
    region       = "global"
    region_limit {
      cpu     = 2500
      memory  = 1000
    }
  }
}

nomad quota apply quota.hcl
nomad namespace apply -quota=default-quota dev
```

## Namespaces

Logical partitions for multi-tenancy:

```
nomad namespace apply -description="Dev" dev
nomad job run -namespace=dev example.nomad
```

Jobs, ACL policies, and quotas are all namespace-scoped.

## Job Versioning

Nomad tracks versions of each job:

```
nomad job history example
nomad job revert example <version>
```

Useful for rollback. Each submission increments the version.

## Inspecting Scheduling Decisions

```
nomad job plan example.nomad
```

Shows:
- Diff vs current state
- Placement plan (how many allocs on which nodes)
- Any warnings (constraint misses, etc.)

Exit code indicates changes: 0=no changes, 1=error, 2=changes.

## Spread Across Datacenters

```hcl
spread {
  attribute = "${node.datacenter}"
  target "dc1" { percent = 34 }
  target "dc2" { percent = 33 }
  target "dc3" { percent = 33 }
}
```

Nomad approximates those percentages across count.

## Ephemeral Disk

```hcl
ephemeral_disk {
  sticky  = true      # keep same disk across restarts on same node
  migrate = true      # try to migrate disk to new node on reschedule
  size    = 500       # MiB
}
```

`sticky` is a soft constraint. `migrate` only works if data is under the disk size limit.

## Health Checks Integration

Deployments wait for health checks before marking allocations healthy. With Consul, checks happen at the Consul agent. With native services, Nomad runs the checks.

```hcl
check {
  type     = "http"
  path     = "/health"
  interval = "10s"
  timeout  = "2s"
}
```

Task health signal: task running (status = running, no failures) AND all checks passing for min_healthy_time.

## Allocation Restart vs Reschedule

- **restart:** stay on same alloc, restart the task
- **reschedule:** kill the alloc, create new alloc on a different client

Restart is first; once restarts exhausted, reschedule engages.

## Exam-Ready Checklist

- [ ] Can describe evaluation and deployment flow
- [ ] Know bin-pack vs spread scheduling
- [ ] Understand system and sysbatch semantics
- [ ] Know canary and rolling update patterns
- [ ] Can drain a node and understand migrate behavior
- [ ] Know constraints vs affinities vs spreads
- [ ] Understand `nomad job plan` output

## Key terms

- **Job** - the top-level unit of work that a user submits to Nomad, made up of one or more task groups.
- **Task group** - a set of tasks that are always placed together on the same client node.
- **Allocation** - a mapping of a task group to a client node, created by the scheduler.
- **Evaluation** - the process Nomad uses to decide what changes are needed for a job and to create a plan.
- **Service job** - a long-running job type, such as a web server, that Nomad keeps running.
- **Batch job** - a job type for short-lived tasks that run to completion.
- **System job** - a job type that runs one allocation on every eligible client node.
- **Canary** - a new-version allocation started alongside the old version so it can be checked before a full rollout.
