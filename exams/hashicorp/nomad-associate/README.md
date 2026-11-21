# HashiCorp Nomad Study Track

## About this track

> **This is a self-directed study track, not a certification guide.** HashiCorp's [certifications page](https://developer.hashicorp.com/certifications) (checked 2026-11-21) lists no Nomad exam, only Terraform and Vault exams. Earlier versions of this guide quoted a cost, question count, passing score and domain weights for a "Nomad Associate" exam; none of those had a vendor source, so they are removed. The notes, scenarios and labs still teach Nomad as it is used in practice.

This track builds foundational knowledge and practical skills for deploying, operating, and consuming HashiCorp Nomad. Nomad is a simple and flexible workload orchestrator that runs containers, VMs, Java apps, native binaries, and more, scheduled across a fleet of machines on-prem, in the cloud, or at the edge.

It is aimed at platform engineers, SREs, application developers, and operators who use Nomad to schedule and manage workloads. It covers Nomad's architecture, job specifications in HCL, scheduling and allocations, service discovery and networking, storage and volumes, and ACL-based security.

## Who this is for

- Platform engineers running Nomad clusters (as an alternative to Kubernetes)
- SREs operating mixed workloads (containers + VMs + batch jobs)
- Application developers writing Nomad job specs
- DevOps engineers integrating Nomad with Consul, Vault, and CI/CD
- Engineers on hybrid/edge deployments where Nomad's simplicity shines over Kubernetes

## Topic areas

1. Nomad architecture and cluster concepts
2. Job specification authoring in HCL
3. Scheduling, allocations, and drivers
4. Networking, service discovery, Consul integration
5. Storage and volumes (CSI, host volumes)
6. ACL security, federation, and operations

See `fact-sheet.md` for detailed topics per domain.

## Prerequisites and Recommended Experience

- Linux fundamentals: processes, systemd, file permissions, networking
- Docker basics: images, containers, ports, volumes
- HCL familiarity (Terraform or Packer experience helps)
- Optional but valuable: Consul familiarity for service discovery
- Optional: Vault familiarity for secret integration
- Basic CI/CD knowledge

## Study Path

1. Read `fact-sheet.md` for the topic map.
2. Work through notes in `notes/` sequentially.
3. Follow the week-by-week schedule in `practice-plan.md`.
4. Review `scenarios.md` for real-world problem-solving.
5. Use `strategy.md` for the common traps.

## Hands-on Lab Requirements

Nomad labs are lightweight:

- Nomad 1.7 or newer
- Docker Desktop / Podman for the docker driver
- A 3-node Nomad cluster (Docker Compose or 3 VMs)
- Optional: Consul 1.17+ for service mesh labs
- Optional: Vault 1.15+ for secrets labs
- Cloud: free-tier works; a small Raspberry Pi cluster also fine

`nomad agent -dev` runs a single-node dev cluster in seconds for learning.

## Official Resources

- Nomad documentation: https://developer.hashicorp.com/nomad/docs
- Nomad tutorials: https://developer.hashicorp.com/nomad/tutorials
- Nomad Pack (package manager): https://developer.hashicorp.com/nomad/tools/nomad-pack
- HCP Nomad (if you prefer SaaS): in beta at the time of writing

## Recommended Supplementary Resources

- "Nomad in Action" or the HashiCorp Learn Nomad track
- Nomad's official example jobspecs repo on GitHub
- Community meetup videos on YouTube ("HashiConf" channel)
- Nomad GitHub repo for release notes and issue tracker

## Common Pitfalls to Avoid

- Treating Nomad like Kubernetes. Job spec is simpler but has different semantics.
- Ignoring non-container task drivers. Nomad's value is also running exec, java, qemu.
- Missing Consul integration content. Service discovery is central to real deployments.
- Overlooking constraints and affinities. Scheduling nuances matter in practice.
- Skipping ACL configuration. Production clusters run with ACLs on.

## Time Investment Estimate

- 40 to 60 hours total
- 3 to 4 weeks of part-time study
- At least 15 hours of hands-on labs

## Nomad vs Kubernetes

Quick mental model:

| Aspect | Nomad | Kubernetes |
|--------|-------|------------|
| Scope | Workloads only | Workloads + full platform (ingress, storage, RBAC, etc.) |
| Complexity | One binary, simple operations | Many components, steep learning curve |
| Workload types | Docker, exec, java, qemu, raw_exec | Containers primarily |
| Config | HCL or JSON | YAML |
| Installation | Binary + systemd, 5 minutes | Multi-hour or managed service |
| Edge | Lightweight, single binary | Heavy, often impractical |

Nomad is ideal when you want a scheduler without the platform complexity, or when you need to schedule non-container workloads alongside containers.
