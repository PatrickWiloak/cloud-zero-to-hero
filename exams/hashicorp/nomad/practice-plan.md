# Nomad - Practice Plan

A 4-week plan at 8 to 10 hours per week. Compress to 3 weeks with existing Nomad experience; extend to 5 to 6 weeks if new to orchestrators.

## Prerequisites Before Week 1

- Nomad 1.7+ CLI installed (`nomad version`)
- Docker Desktop or Podman running
- 3 to 4 GB RAM available for cluster labs
- Optional: Consul 1.17+, Vault 1.15+ installed
- Git repo for your jobspec experiments
- An editor with HCL highlighting

## Week 1: Architecture, First Jobs, CLI Fluency

**Reading**
- `fact-sheet.md` front to back
- Notes file `01-nomad-architecture.md`
- Official Get Started tutorial

**Labs**
- Run `nomad agent -dev -bind=0.0.0.0` (single node for learning)
- Open the web UI at localhost:4646
- Generate a jobspec: `nomad job init` and inspect the generated HCL
- Edit the jobspec to use an nginx image
- Run: `nomad job run example.nomad`
- Check status: `nomad job status example`
- Inspect allocation: `nomad alloc status <alloc-id>`
- Tail logs: `nomad alloc logs -f <alloc-id>`
- Stop and purge: `nomad job stop -purge example`

**Multi-node lab (better)**
- Stand up a 3-server + 3-client cluster using Docker Compose or Vagrant
- Observe leader election: `nomad operator raft list-peers`
- Run a job, see it land on a client
- Drain a node: `nomad node drain -enable <node-id>`; watch allocs move

**Checkpoint**
- You can start a dev agent and submit a job
- You understand servers vs clients
- You know what Raft quorum is

## Week 2: Job Specs in Depth, Scheduling

**Reading**
- Notes file `02-job-specifications-hcl.md`
- Notes file `03-scheduling-and-allocations.md`

**Labs**
- Convert your nginx job to `type = "service"` with `count = 3`
- Add a `check` block with http health check on `/`
- Add `update` stanza with canary = 1, auto_promote = false
- Deploy a new image version; use `nomad deployment list` and `nomad deployment promote`
- Author a `batch` job that runs a one-off script (`alpine` with `sleep 30`)
- Author a `system` job (agent-like, runs on every node)
- Author a `periodic` job (cron-like, every 5 minutes)
- Author a parameterized job and dispatch with `nomad job dispatch`

**Constraints and affinities**
- Tag one node with `meta.type = "prod"`
- Add a constraint to your job requiring that meta
- Add an affinity with weight 50 for a different attribute
- Use `spread` to distribute across datacenters

**Checkpoint**
- You can differentiate service, batch, system, sysbatch job types
- You understand rolling updates and canaries
- You can use constraints and affinities

## Week 3: Networking, Consul, Storage

**Reading**
- Notes file `04-networking-and-service-discovery.md`
- Notes file `05-storage-and-volumes.md`

**Labs**
- Install Consul on your client nodes
- Configure Nomad agent to integrate with Consul
- Register a service via jobspec; observe it in Consul UI
- Add `connect { sidecar_service {} }` to enable service mesh
- Run two services and make them communicate via Consul Connect
- Register a host volume on a client: `client { host_volume "data" { path = "/opt/data" } }`
- Mount in a jobspec and confirm persistence across restart
- (Optional) Deploy an AWS EBS CSI plugin and create a CSI volume
- Use native service discovery: set `provider = "nomad"` on a service block; query via `nomad service list`

**Checkpoint**
- You can register a service with Consul
- You know bridge vs host vs CNI networking
- You can mount a host volume into a task

## Week 4: ACLs, Federation, Ops

**Reading**
- Notes file `06-acl-security-and-federation.md`
- Full `scenarios.md` run

**Labs**
- Enable ACLs on your cluster: `acl { enabled = true }` in server config
- Bootstrap ACLs: `nomad acl bootstrap`
- Create a policy that grants `read` on default namespace
- Create a token using that policy
- Validate: `export NOMAD_TOKEN=<token>`; try submitting a job (should fail if policy is read-only)
- Create namespaces: `dev`, `prod`; restrict policies accordingly
- (Optional) Stand up a second region; federate with `nomad server join -wan`
- Run a job with `region = "us-west"` to test cross-region scheduling

**Vault integration**
- Start a Vault dev server
- Configure Nomad's `vault {}` stanza
- Write a jobspec with `vault { policies = [...] }` and a template that reads a secret

**Self-check**
- Work every scenario in `scenarios.md` before reading answers
- Build 25 flashcards from fact-sheet (drivers, job types, ports, capabilities)
- Review weakest domain in depth

## Daily Drills (week 4, 15 minutes)

- Name all 4 job types and their use cases
- Name 5 task drivers
- Recite Nomad default ports
- Parse 3 constraint or grant strings
- Explain Consul Connect sidecar setup

## Hands-on Lab Environment Checklist

- [ ] `nomad version` shows 1.7+
- [ ] 3-node cluster reachable or dev mode solid
- [ ] Successfully deployed service, batch, and system jobs
- [ ] Consul integrated at least once
- [ ] Native Nomad service discovery tried
- [ ] Host volume mounted and data persists
- [ ] ACL bootstrap done; token-scoped access tested

## Next steps

Natural follow-ups:

- Vault Associate (secrets management for Nomad workloads)
- Terraform Associate (provision Nomad clusters as code)
