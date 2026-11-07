---
last-updated: 2026-11-07
---

# CompTIA Linux+ (XK0-006) Study Plan

## 8-Week Schedule

Budget about 8-10 hours a week. Book the exam date early; a date on the calendar keeps the plan honest. Each week lists the topics to understand and the note to read. Nothing here is a timed drill: the aim is to understand how each tool behaves and why.

### Week 1: Boot, filesystem and devices
- [ ] Boot chain, kernel parameters, initrd, PXE
- [ ] Filesystem Hierarchy Standard
- [ ] Kernel modules and hardware inspection tools
- [ ] Notes: `01-system-management.md` (sections 1.1 and 1.2)

### Week 2: Storage
- [ ] Partitions, LVM objects and resizing
- [ ] Filesystem types, `fstab`, mount options, inodes
- [ ] Software RAID and `/proc/mdstat`
- [ ] Notes: `01-system-management.md` (section 1.3)

### Week 3: Network, shell, backup, virtualization
- [ ] NetworkManager, Netplan, name resolution files
- [ ] Network tools and what each answers
- [ ] Redirection, text utilities, backups with tar, rsync and dd
- [ ] KVM, QEMU, libvirt and virtual network types
- [ ] Notes: `01-system-management.md` (sections 1.4 to 1.7)

### Week 4: Users, processes, packages
- [ ] Account files and account management, aging and expiry
- [ ] Processes, signals, priority, cron, at and anacron
- [ ] RPM and dpkg package managers, repositories, signatures
- [ ] Notes: `02-services-and-user-management.md` (sections 2.1 to 2.4)

### Week 5: systemd, containers, firewalls
- [ ] Unit types, enable versus start versus mask, timers
- [ ] Container runtimes, images, Dockerfile instructions, volumes, networks
- [ ] firewalld runtime versus permanent, ufw, NAT and forwarding
- [ ] Notes: `02-services-and-user-management.md` (2.5 and 2.6), `03-security.md` (3.1 and 3.2)

### Week 6: Hardening and cryptography
- [ ] sudo, permissions, special bits, ACLs, attributes
- [ ] SELinux modes, contexts and booleans
- [ ] SSH hardening, account hardening, LUKS2, TLS, hashing
- [ ] Compliance: OpenSCAP, CIS, AIDE, data destruction, banners
- [ ] Notes: `03-security.md` (3.3 to 3.6)

### Week 7: Automation
- [ ] Ansible, Puppet, OpenTofu, Kickstart, cloud-init, CI/CD, GitOps
- [ ] Compose and Kubernetes vocabulary
- [ ] Bash tests, loops, expansion and exit codes
- [ ] Python basics, Git commands, responsible AI use
- [ ] Notes: `04-automation-orchestration-scripting.md`

### Week 8: Troubleshooting and review
- [ ] SLI, SLO, SLA, SNMP, thresholds
- [ ] OS, storage and boot failure symptoms
- [ ] The network layering method and security-related faults
- [ ] Performance: load average, I/O wait, memory pressure
- [ ] Notes: `05-troubleshooting.md`
- [ ] Practice questions across all domains; return to the notes for each miss
- [ ] Re-read [the fact sheet](fact-sheet.md) and [strategy](strategy.md)

## Checkpoint

Before booking the final date, score the [practice questions](../../../resources/practice-questions/comptia-linux-plus-xk0-006.md). If a domain is weak, re-read its note rather than rereading everything.
