---
last-updated: 2026-11-07
difficulty: intermediate
---

# CompTIA Linux+ (XK0-006)

## Exam Overview

CompTIA Linux+ is a vendor-neutral certification for people who configure, manage, operate and troubleshoot Linux servers. CompTIA describes the successful candidate as having the knowledge and skills to do that "while using security best practices, scripting, containerization, virtualization, and automation," at roughly 12 months of hands-on experience with Linux servers. A+, Network+ or Server+ (or equivalent knowledge) is recommended but not required.

The current exam is **XK0-006 (V8)**, launched July 15, 2025. It is one exam, not a pair. It replaced XK0-005; a third-party guide reports XK0-005 retired on January 13, 2026, but that date is not on the CompTIA pages read for this guide.

**What changed in V8:** the objectives are regrouped into five domains with **Troubleshooting now its own domain at 22%**. Automation has grown to cover infrastructure as code, Python basics, Git, CI/CD ideas and Kubernetes vocabulary, and there is a **new objective on the responsible use of AI** (4.5). Security names SSSD, Polkit, LUKS2 with Argon2, WireGuard and supply-chain topics; System Management adds RISC-V, GPU use cases and `netplan`. I did not diff against the XK0-005 objectives document, so treat the list as "what the V8 document names," not a verified delta.

## Quick Reference

| Item | Value |
|------|-------|
| **Exam code** | XK0-006 (V8) |
| **Duration** | 90 minutes |
| **Questions** | Maximum of 90 |
| **Question types** | Multiple choice and performance-based |
| **Passing score** | 720 on a scale of 100-900 |
| **Launched** | July 15, 2025 |
| **Expected retirement** | Estimated 2028 ("usually three years after launch") |
| **Language** | English |
| **Recommended experience** | 12 months hands-on with Linux servers; A+, Network+, Server+ or similar |
| **Prerequisites** | None |
| **Price** | Not verified (the CompTIA page links to Buy Now with no figure) |
| **Validity** | Not verified for Linux+ on the page read; see [the fact sheet](fact-sheet.md#verified-facts-and-sources-checked-2026-11-07) |

## Exam Domains

| Domain | Topic | Weight | Notes |
|--------|-------|--------|-------|
| 1.0 | System Management | 23% | [01 - System Management](notes/01-system-management.md) |
| 2.0 | Services and User Management | 20% | [02 - Services and User Management](notes/02-services-and-user-management.md) |
| 3.0 | Security | 18% | [03 - Security](notes/03-security.md) |
| 4.0 | Automation, Orchestration, and Scripting | 17% | [04 - Automation, Orchestration, and Scripting](notes/04-automation-orchestration-scripting.md) |
| 5.0 | Troubleshooting | 22% | [05 - Troubleshooting](notes/05-troubleshooting.md) |

## Domain Summary

### Domain 1: System Management (23%)
The boot chain, the Filesystem Hierarchy Standard, kernel modules and hardware inspection tools, storage from partitions through LVM, filesystems, mount options and software RAID, network configuration with NetworkManager and Netplan, shell operations, backup and restore with tar, rsync and dd, and virtualization with KVM, QEMU and libvirt.

### Domain 2: Services and User Management (20%)
File and link management, local accounts and password aging, processes, signals and scheduling, RPM and dpkg package management, systemd units and timers, and containers with Docker and Podman: images, volumes, networks and privileged versus unprivileged.

### Domain 3: Security (18%)
PAM, SSSD, Kerberos and auditing, firewalld, ufw and nftables, sudo, permissions, ACLs, SELinux and SSH hardening, account hardening, LUKS2 and TLS, and compliance with OpenSCAP, CIS Benchmarks and AIDE.

### Domain 4: Automation, Orchestration, and Scripting (17%)
Ansible, Puppet and OpenTofu, Kickstart and cloud-init, CI/CD and GitOps, Compose and Kubernetes vocabulary, bash scripting, Python basics, Git and responsible AI use.

### Domain 5: Troubleshooting (22%)
Monitoring concepts (SLI, SLO, SLA, SNMP), boot, storage and OS failures, a layered network method, SELinux and permission faults, certificates and SSH access, and performance analysis from load average to I/O wait.

## Study Materials

### Notes (study order)
- [01 - System Management](notes/01-system-management.md) - Boot, FHS, devices, LVM, RAID, mounts, networking, shell, backup, virtualization
- [02 - Services and User Management](notes/02-services-and-user-management.md) - Files, accounts, processes, packages, systemd, containers
- [03 - Security](notes/03-security.md) - AAA, firewalls, hardening, SELinux, SSH, cryptography, compliance
- [04 - Automation, Orchestration, and Scripting](notes/04-automation-orchestration-scripting.md) - IaC, shell, Python, Git, AI
- [05 - Troubleshooting](notes/05-troubleshooting.md) - Symptom to cause across monitoring, OS, network, security, performance

### Study Resources
- [Fact Sheet](fact-sheet.md) - Verified exam facts, command tables, file locations
- [Practice Plan](practice-plan.md) - 8-week schedule
- [Scenarios](scenarios.md) - Admin scenarios with analysis and fixes
- [Strategy](strategy.md) - How to approach the exam and PBQs
- [Practice Questions](../../../resources/practice-questions/comptia-linux-plus-xk0-006.md) - 20 original scenario questions

## Official Resources

- **[📖 CompTIA Linux+ Certification](https://www.comptia.org/en-us/certifications/linux/)** - Exam code, question count, duration, passing score and domain weights
- **[📖 CompTIA Linux+ XK0-006 Exam Objectives (PDF, version 5.0)](https://lecbyo.files.cmp.optimizely.com/download/90b9ac985c0e11f0b004a2a93c999a21)** - Every objective, the tools named under each, and the acronym list. A version 3.0 file with the same domain weights also exists; use the highest version number and re-check the CompTIA page

## Recommended Study Time

| Background | Estimated Hours | Calendar Time |
|------------|-----------------|---------------|
| Brand new to Linux | 120-160 hours | 12-16 weeks |
| Some Linux use, no admin work | 80-110 hours | 8-10 weeks |
| Junior sysadmin or DevOps | 40-70 hours | 4-6 weeks |
| Working Linux administrator | 20-40 hours | 2-3 weeks |

These are planning estimates, not CompTIA figures.

## Lab Setup

Linux+ includes performance-based questions at a prompt, so you need a machine where you can break things.

- **Two small VMs** - one RHEL-family (Rocky or AlmaLinux) and one Debian-family (Ubuntu Server), because the exam uses both package families, `firewalld` and `ufw`, `nmcli` and Netplan.
- **Extra virtual disks** - attach two or three 1 GiB disks to practice partitions, LVM, `mdadm` and LUKS.
- **A container engine** - Podman on the RHEL-family VM or Docker on Ubuntu.
- **A Git repository and a Python venv** - for the scripting domain.

## Companion Materials

- **[CompTIA A+ (220-1201 and 220-1202)](../a-plus/README.md)** - Hardware and OS fundamentals
- **[CompTIA Network+ (N10-009)](../network-plus/README.md)** - Networking depth behind Domain 1.4 and 5.3
- **[CompTIA Security+ (SY0-701)](https://security.noblerworks.com/exams/comptia/security-plus/)** - Broader security context
- **[Red Hat Certified System Administrator](../../redhat/rhcsa-ex200/README.md)** - A hands-on, RHEL-specific next step

## After This Cert

### Career Paths
- Linux System Administrator
- Junior DevOps or Platform Engineer
- Cloud Support Engineer
- Site Reliability Engineer (entry)

### Recommended Next Certifications
- **RHCSA** - Practical RHEL administration. See [RHCSA](../../redhat/rhcsa-ex200/README.md).
- **CompTIA Security+** - Security baseline. See [Security+](https://security.noblerworks.com/exams/comptia/security-plus/).
- **Cloud provider associate certifications** - Linux skills are assumed on every cloud exam.

---

**Good luck with your CompTIA Linux+ certification.** The exam rewards people who have typed the commands. Study with a terminal open.
