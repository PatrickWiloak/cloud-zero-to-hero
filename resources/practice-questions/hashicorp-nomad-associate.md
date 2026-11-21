---
last-updated: 2026-10-22
difficulty: intermediate
---

# HashiCorp Nomad - Practice Questions

30 questions for Nomad practice across architecture, job specification, scheduling, operations, and integration with Consul and Vault.

> **Study track:** [exams/hashicorp/nomad-associate/](../../exams/hashicorp/nomad-associate/)

---

### Question 1
**Scenario:** What is the hierarchy of objects in a Nomad job specification?

A. A task contains jobs, because the task is the unit users submit and the job is a step within it
B. Job contains groups; groups contain tasks
C. A job contains tasks directly, with groups used only to label tasks and having no placement meaning
D. A group contains jobs, each job holding the tasks that share one node and its network namespace

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A job has one or more task groups, and each group has one or more tasks. The group is the scheduling unit: everything in a group is placed on the same client node and shares its network namespace and ephemeral disk, which is the equivalent of a Kubernetes pod.
</details>

---

### Question 2
**Scenario:** A job must run one instance on every eligible client node.

A. `type = "system"`, no count set
B. `type = "sysbatch"` with a periodic schedule, which keeps one allocation permanently on each node, restarting it as needed
C. `type = "batch"`
D. `type = "service"` with a very high count

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The system scheduler places one allocation per eligible node and automatically covers nodes that join later, which suits log shippers and monitoring agents. Service jobs are long-running with a count, batch jobs run to completion, and sysbatch is the run-once-per-node variant.
</details>

---

### Question 3
**Scenario:** Nomad must run a task that is not a container.

A. Task drivers include Docker, exec, raw_exec, Java, and QEMU
B. Only Docker is supported, since Nomad has no other task drivers built in
C. Convert every workload to a container image first, because the scheduler can only place container-based tasks
D. Use a wrapper container that launches the binary inside a Docker image

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Driver flexibility is Nomad's main differentiator from Kubernetes: legacy Java applications, static binaries, and VMs are first-class workloads. `exec` runs an isolated binary with cgroups and namespaces; `raw_exec` has no isolation and should be enabled deliberately.
</details>

---

### Question 4
**Scenario:** An allocation stays pending with a placement failure message.

A. Increase the count, so the scheduler has more chances to place the job on a node
B. Delete the job and submit it again from the original spec file, in case it is stale
C. Read `nomad job status` and the evaluation's placement failures
D. Restart the client agent on the busiest node so that it re-registers its resources and the scheduler retries

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Nomad reports why placement failed per node class: nodes filtered by constraint, exhausted resources such as CPU or memory, or missing drivers. That output usually names the fix directly, which is faster than guessing at capacity.
</details>

---

### Question 5
**Scenario:** A deployment must roll out gradually and stop if the new version is unhealthy.

A. Stop the job and start it again
B. An `update` block with `max_parallel`, `min_healthy_time`, `healthy_deadline`, and `auto_revert = true`
C. A batch job type, which replaces allocations one at a time and stops itself when a run fails, with the old version kept in place
D. `count = 1`

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The update block controls rolling deployment, and `auto_revert` returns to the last healthy version if the deadline passes without health. Canary counts add an explicit verification stage before the rest of the allocations are replaced.
</details>

---

### Question 6
**Scenario:** A task needs a database password from Vault.

A. Store it in the job spec as a variable default, since job files are only readable by administrators of the cluster
B. Hard-code it
C. Fetch it manually
D. A `vault` block with a policy, and a `template` block rendering the secret to a file or env var

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Nomad obtains a Vault token scoped to the task's policies and the template stanza renders secrets, re-rendering and optionally restarting or signaling the task when they change. Secrets in the job spec end up in the job history and are visible to anyone who can read the job.
</details>

---

### Question 7
**Scenario:** A service registered by Nomad should be discoverable and health-checked.

A. A `service` block with health checks, registered into Consul or Nomad's native discovery
B. A load balancer only, configured with the allocation's address once, since Nomad does not publish service addresses itself
C. Manual registration
D. DNS entries

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The service block declares the port, tags, and checks, and Nomad registers and deregisters as allocations come and go. Consul is the full-featured option; Nomad native service discovery covers simpler cases without running Consul.
</details>

---

### Question 8
**Scenario:** How does Nomad decide which node gets an allocation?

A. Alphabetically
B. Filter by constraints and resources, then score by the configured algorithm (binpack or spread)
C. Random selection among nodes that have free memory, with no scoring step applied to the shortlist of nodes
D. Round robin across all client nodes in turn, skipping nodes only when their agent has stopped responding

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Feasibility checking comes first, then scoring. Binpack concentrates allocations to leave whole nodes free, which suits autoscaling down; spread distributes for resilience. The `spread` block lets you additionally spread across attributes such as datacenter or rack.
</details>

---

### Question 9
**Scenario:** A job must only run on nodes with SSD storage.

A. A comment in the job file
B. A `spread` block over the storage attribute, forcing every allocation onto SSD nodes
C. A `constraint` block matching a node attribute or metadata value, which hard-filters nodes before placement
D. Hope for the best

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Constraints are hard filters, so a job will not be placed if none match. `affinity` is the soft version, expressing preference by weight without preventing placement. Choosing hard versus soft is the design decision worth being explicit about.
</details>

---

### Question 10
**Scenario:** Servers and clients in a Nomad cluster.

A. All agents are identical and each holds cluster state and runs allocations in the same process
B. There is only one agent type
C. Servers hold state via Raft and schedule; clients run allocations and report resources
D. Clients hold state in Raft and make the scheduling decisions, while servers only run the allocations and report usage

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** As with Consul, servers run in an odd-numbered quorum (3 or 5) and clients scale independently. This split is why a Nomad cluster can reach very large client counts while keeping the consensus group small.
</details>

---

### Question 11
**Scenario:** A batch job must run on a schedule.

A. An external cron calling `nomad job run`
B. A service job whose task sleeps between runs, restarted by its restart block
C. A `periodic` block on a batch job with a cron spec, so Nomad launches every run itself without outside help
D. It is not supported

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Periodic jobs are scheduled by Nomad itself with a prohibit-overlap option, so there is no external scheduler to keep available. Parameterized jobs are the related feature for on-demand dispatch with inputs.
</details>

---

### Question 12
**Scenario:** A task must not exceed its memory allocation.

A. Memory is unlimited
B. Set `resources { memory = 512 }`, enforced by the driver with an OOM kill if exceeded
C. Rely on the operating system, whose cgroup defaults will stop any task using more memory than the host has free
D. Set CPU only

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Memory is both a scheduling input and an enforced limit. `memory_max` enables oversubscription, letting a task burst above its reserved value when the node has spare capacity, which improves utilization without changing the scheduling guarantee.
</details>

---

### Question 13
**Scenario:** ACLs are enabled and a user cannot submit jobs.

A. Disable ACLs on the client agents only, since only the clients enforce job submission permissions
B. Restart the servers, since a restart re-reads the policies and clears the denial
C. Use the web UI instead, since the UI skips ACL checks for signed-in users
D. A token with a policy granting `submit-job` on the target namespace

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Nomad ACL policies grant capabilities scoped to namespaces, node, agent, and operator categories. Namespaces are the multi-tenancy boundary, so the policy must name the namespace the job targets, not just the capability.
</details>

---

### Question 14
**Scenario:** A node must be taken out of service for maintenance without killing running work abruptly.

A. Reboot it and let allocations be rescheduled after the client agent re-registers
B. Stop the client agent
C. Delete the node
D. `nomad node drain` with a deadline, migrating allocations away before the node is taken out

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Drain marks the node ineligible and migrates allocations, respecting the `migrate` block's parallelism and health requirements so the service stays up during the move. Stopping the agent outright loses that orchestration.
</details>

---

### Question 15
**Scenario:** Autoscaling is required for a service job based on load.

A. Nomad Autoscaler with a scaling policy referencing a metrics source
B. Nomad scales service jobs automatically by default, adjusting `count` whenever CPU on the clients passes a threshold
C. Manual count changes
D. Only cluster autoscaling exists, so the number of allocations stays fixed while client nodes are added and removed

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The Nomad Autoscaler is a separate component supporting horizontal application autoscaling driven by an APM such as Prometheus, and horizontal cluster autoscaling to add or remove client nodes. Both are needed to scale end to end.
</details>

---

### Question 16
**Scenario:** A company runs Nomad in three locations: `us-east-dc1`, `us-east-dc2`, and `eu-west-dc1`. The US sites have low latency between them; Europe does not. How should regions and datacenters be laid out?

A. One `us` region with two datacenters sharing a server cluster, and a separate federated `eu` region
B. One global region whose server cluster spans all three locations with a single Raft group
C. Three regions, one per datacenter, with no federation configured between any of them
D. One datacenter containing all clients, with servers placed only in the European location

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** A region is a set of servers running one Raft group, and it can schedule onto several datacenters with low latency between them. Regions are federated for cross-region job submission and visibility. Stretching Raft across high-latency links hurts consensus. Three unfederated regions add overhead and lose the shared view. Putting all servers in Europe makes every US scheduling decision cross the ocean.

**Key Concept:** Regions are the consensus and failure boundary; datacenters are placement targets inside a region. See [Nomad architecture](https://developer.hashicorp.com/nomad/docs/architecture).
</details>

---

### Question 17
**Scenario:** A Nomad client running several service allocations loses power. What does Nomad do by default?

A. It waits for an operator to run `nomad node drain` on that node before it takes any action
B. It keeps the allocations marked as running until the client returns
C. It deletes the job, because one of its allocations can no longer be reached
D. Servers mark the node down after missed heartbeats and reschedule its allocations

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Clients heartbeat to the servers; when heartbeats stop, the servers mark the node down, its allocations are marked lost, and the scheduler places replacements on healthy nodes. A drain is for planned maintenance, not failures. Leaving the allocations as running would hide the outage. The job definition remains; only placement changes.

**Key Concept:** Nomad keeps declared job state true by replacing lost allocations. See [How scheduling works](https://developer.hashicorp.com/nomad/docs/concepts/scheduling/how-scheduling-works).
</details>

---

### Question 18
**Scenario:** An operator runs `nomad job run web.nomad.hcl`. What does Nomad create first, before any allocation is placed?

A. A deployment, which is created only after every allocation becomes healthy
B. An evaluation, which a scheduler processes to produce a placement plan
C. A node pool, which the job needs before any of its tasks can run
D. A snapshot, which is taken by the servers before any change is made

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Any change in desired or actual state, such as a job submission, creates an evaluation. A scheduler worker processes it, produces a plan of allocations, and the leader applies the plan. Deployments track rollouts of service jobs but do not come first. Node pools are configured on clients and are not created by jobs. Snapshots are a backup operation.

**Key Concept:** Job submission, evaluation, plan, allocation: the core scheduling flow. See [How scheduling works](https://developer.hashicorp.com/nomad/docs/concepts/scheduling/how-scheduling-works).
</details>

---

### Question 19
**Scenario:** An operator needs to run a short cleanup script once on every client node in the cluster, and it should exit when it is done rather than being restarted. Which job type fits?

A. `service`, with a count equal to the number of nodes in the cluster
B. `batch`, with a constraint naming each node one by one in the job
C. `sysbatch`, which runs a batch task once on every eligible node
D. `system`, which keeps a long-running task on every eligible node

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** `sysbatch` combines system placement, one per eligible node, with batch behaviour, run to completion. `service` jobs are long-running and restart when tasks exit, and a count does not guarantee one per node. A `batch` job with hand-written constraints breaks as nodes change. A `system` job restarts a task that exits, which suits daemons, not one-off scripts.

**Key Concept:** Four job types: service, batch, system, and sysbatch. See [Schedulers](https://developer.hashicorp.com/nomad/docs/concepts/scheduling/schedulers).
</details>

---

### Question 20
**Scenario:** Two engineers might change the same job at once. An engineer wants to preview the changes a job file will make and then submit only if nobody has modified the job since the preview. What workflow does this?

A. Run `nomad job validate` and then submit with `nomad job run` using the `-detach` flag
B. Run `nomad job status` and then edit the job directly in the web UI
C. Run `nomad job inspect` and then submit the job with `nomad job revert`
D. Run `nomad job plan`, then `nomad job run -check-index` with the index it printed

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** `nomad job plan` shows a dry run of the scheduler's decisions and prints a job modify index. Passing that to `nomad job run -check-index` makes the run fail if the job changed since the plan. `validate` only checks syntax, and `-detach` just returns without monitoring. Status and inspect show current state but do not guard the update. `revert` rolls back to an earlier version.

**Key Concept:** Plan, then run with check-index, like a Terraform plan and apply. See [nomad job plan](https://developer.hashicorp.com/nomad/commands/job/plan).
</details>

---

### Question 21
**Scenario:** A task reads its config from a file rendered from Consul KV. When the KV values change, the file should update and the application should reload on SIGHUP without a restart. How should the `template` block be configured?

A. `change_mode = "signal"` with `change_signal = "SIGHUP"`
B. `change_mode = "restart"` with `splay = "0s"` set on it
C. `change_mode = "noop"` with a cron job that sends SIGHUP
D. `change_mode = "script"` that deletes and re-creates the task

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The template block re-renders when its data changes, and `change_mode = "signal"` with `change_signal` sends that signal to the task, so it can reload in place. `restart` restarts the task, which the team wants to avoid. `noop` plus a cron job adds lag and moving parts. A script that re-creates the task is equivalent to a restart, done the hard way.

**Key Concept:** Templates keep config in sync, and change_mode decides how the task reacts. See [template block](https://developer.hashicorp.com/nomad/docs/job-specification/template).
</details>

---

### Question 22
**Scenario:** A service group runs 4 instances. The team wants blue-green deployments: start a full set of new instances alongside the old ones, test them, then switch over. How should the `update` block be set?

A. `max_parallel = 4` with no canaries, so all instances are replaced at once
B. `canary = 4` matching the group count, then promote once checks pass
C. `canary = 1` with `auto_revert = true` and every other setting left as default
D. `stagger = "0s"` with `health_check = "manual"` so updates happen together

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Setting `canary` equal to the group count starts a complete new set alongside the old one, which is a blue-green deployment; promoting the deployment, by hand or with `auto_promote`, then retires the old set. Replacing all four at once is not blue-green, since the old set stops. One canary is a canary deployment, not a full parallel set. Stagger and manual health settings do not create a second set.

**Key Concept:** Canary count less than group count gives canary deployments; equal gives blue-green. See [Blue-green and canary deployments](https://developer.hashicorp.com/nomad/docs/job-declare/strategy/blue-green-canary).
</details>

---

### Question 23
**Scenario:** A service has 6 instances, and the team wants half of them in `dc1` and half in `dc2`, so one datacenter failing does not take out the service. Which job specification block expresses this?

A. A `constraint` that requires the `dc1` datacenter for every instance
B. An `affinity` with a high weight toward the `dc2` datacenter only
C. A `reschedule` block with `unlimited = true` for the whole group
D. A `spread` on `${node.datacenter}` with a 50 percent target for each

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The `spread` block distributes allocations across values of an attribute, such as datacenter or rack, with optional percentage targets. A constraint to `dc1` puts everything in one place. An affinity toward `dc2` pulls instances there rather than balancing them. Rescheduling controls what happens after failures, not initial placement.

**Key Concept:** Spread for failure-domain balance, constraints for hard rules, affinities for preferences. See [spread block](https://developer.hashicorp.com/nomad/docs/job-specification/spread).
</details>

---

### Question 24
**Scenario:** A task crashes occasionally because of a transient dependency. The team wants Nomad to try restarting it on the same node a few times, and only if that fails, place it on a different node. Which blocks control these two behaviours?

A. `update` for local restarts, and `migrate` for moving it to another node
B. `spread` for local restarts, and `affinity` for moving it to another node
C. `restart` for local restarts, and `reschedule` for moving it to another node
D. `lifecycle` for local restarts, and `constraint` for moving it to another node

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The `restart` block controls how many times and how quickly the client restarts a failed task in place. When those attempts are exhausted, the allocation fails and the `reschedule` block controls placing a replacement, typically on another node. `update` governs deployments, and `migrate` governs drains. Spread and affinity influence placement scoring. `lifecycle` orders tasks within a group.

**Key Concept:** Restart is local and handled by the client; reschedule is cluster-wide and handled by the servers. See [restart block](https://developer.hashicorp.com/nomad/docs/job-specification/restart).
</details>

---

### Question 25
**Scenario:** A batch job runs faster on nodes with a newer CPU generation, but it should still run on older nodes when the newer ones are busy. How should this be expressed?

A. An `affinity` on the CPU attribute, with a positive weight toward the newer CPUs
B. A `constraint` on the CPU attribute that requires the newer CPU generation
C. A `spread` on the CPU attribute with 100 percent on the newer CPU generation
D. A separate node pool for newer nodes, with the job restricted to that pool

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Affinities are soft preferences that raise a node's placement score without excluding other nodes. A constraint is a hard filter, so the job would wait when newer nodes are busy. A spread target of 100 percent still steers toward one value and is meant for balancing. Restricting to a dedicated node pool is also a hard limit.

**Key Concept:** Use affinity when you prefer, constraint when you require. See [affinity block](https://developer.hashicorp.com/nomad/docs/job-specification/affinity).
</details>

---

### Question 26
**Scenario:** Three instances of a container that listens on port 8080 must run on the same client node using bridge networking. How should the group's `network` block handle ports?

A. Use `static = 8080` for each instance, so the three share the host port
B. Use a dynamic host port with `to = 8080`, so each instance gets its own host port
C. Use host networking with the same port, and let the OS resolve the clash
D. Remove the `network` block, and Nomad will discover the ports at runtime

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A dynamic port lets Nomad pick a free host port for each allocation, and `to = 8080` maps it to the port the application listens on inside its network namespace. Three allocations cannot all bind static host port 8080 on one node. Host networking with the same port causes bind failures. Without a port declaration, nothing is mapped or registered.

**Key Concept:** Dynamic ports avoid host port clashes; `to` maps them to the app's port. See [network block](https://developer.hashicorp.com/nomad/docs/job-specification/network).
</details>

---

### Question 27
**Scenario:** A small team runs Nomad without Consul. They want services registered with health checks and discoverable by other jobs through templates. What is the simplest approach?

A. Install Consul anyway, because Nomad has no service discovery of its own
B. Write each allocation's IP address and port to a shared file by hand
C. Use Nomad variables to store addresses that each job updates when it starts
D. Use the `service` block with `provider = "nomad"` and look services up in templates

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Nomad has built-in service discovery: a `service` block with `provider = "nomad"` registers services and their checks in Nomad, and templates can query them with the `nomadService` function. Consul adds features such as a mesh but is no longer required for basic discovery. Hand-maintained files and self-updating variables are fragile and miss health status.

**Key Concept:** Native service discovery covers simple clusters; Consul adds mesh and richer features. See [service block](https://developer.hashicorp.com/nomad/docs/job-specification/service).
</details>

---

### Question 28
**Scenario:** A task needs a directory that already exists on certain client nodes, mounted read-only into its container. Which combination is required?

A. A CSI plugin job, a registered CSI volume, and a `volume_mount` in the task
B. A `template` block that copies the files and a `restart` block on change
C. A `host_volume` in the client config, a group `volume` block, and a `volume_mount`
D. An `artifact` block that downloads the directory into the task at start

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Host volumes are declared on the client, requested by the group with a `volume` block of type `host`, and mounted into the task with `volume_mount`, where `read_only` can be set. Groups requesting the volume are only placed on nodes that provide it. CSI is for external storage systems, not local directories. Templates render config files, and artifacts download files rather than mounting existing ones.

**Key Concept:** Declare, request, then mount. See [volume block](https://developer.hashicorp.com/nomad/docs/job-specification/volume).
</details>

---

### Question 29
**Scenario:** A database job needs a persistent cloud block storage volume that follows the allocation if it is rescheduled to another client node. What should the team use?

A. A CSI volume backed by the cloud provider's storage, with its CSI plugin jobs running
B. A host volume on each node, kept in sync with a nightly copy between the nodes
C. The task's ephemeral disk with `sticky = true`, so the data moves to any node
D. A `template` block that writes the database files out of Consul KV at startup

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** CSI volumes are managed by storage plugins, run as Nomad jobs, which can attach the same external volume to whichever node the allocation lands on. Host volumes are local to a node, and a nightly copy loses data. The ephemeral disk with `sticky` tries to reuse the same node, and `migrate` can copy data on a best-effort basis, but neither is durable storage. KV is not a database store.

**Key Concept:** Use CSI for storage that must outlive and follow allocations. See [CSI storage](https://developer.hashicorp.com/nomad/docs/architecture/storage/csi).
</details>

---

### Question 30
**Scenario:** An operator has just enabled ACLs on all Nomad servers and clients. No tokens exist yet. What is the next step?

A. Restart the servers with ACLs disabled, then create tokens through the web UI
B. Run `nomad acl bootstrap` once to create the initial management token
C. Create a client policy first, then attach it to the anonymous token
D. Copy the gossip encryption key, which also acts as the first ACL token

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** `nomad acl bootstrap` creates the first management token, which is then used to write policies and create other tokens; it works once per cluster unless bootstrap is reset. Disabling ACLs to create tokens defeats the purpose. Writing a policy requires a management token, which does not exist yet. The gossip key is unrelated to ACLs.

**Key Concept:** Bootstrap once, store the management token safely, then use least-privilege tokens. See [nomad acl bootstrap](https://developer.hashicorp.com/nomad/commands/acl/bootstrap).
</details>

---

## Where to go deeper

- [Nomad Associate cert page](../../exams/hashicorp/nomad-associate/) - notes, practice plan, strategy
- [Consul Associate practice questions](./hashicorp-consul-associate.md) - the discovery layer Nomad integrates with
- [CKA practice questions](./kubernetes-cka.md) - the other orchestrator, for comparison
- **[📖 Nomad documentation](https://developer.hashicorp.com/nomad/docs)** - primary source
