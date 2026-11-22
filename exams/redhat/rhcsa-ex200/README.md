# Red Hat Certified System Administrator (RHCSA) - EX200

## Overview

The Red Hat Certified System Administrator (RHCSA) is a hands-on, performance-based certification that validates the core skills required to administer Red Hat Enterprise Linux (RHEL) systems. Unlike multiple-choice exams, RHCSA requires you to perform real Linux administration tasks on a live system in a controlled environment.

This cert is the foundation of the Red Hat certification path and a prerequisite for the Red Hat Certified Engineer (RHCE) and many higher-tier Red Hat certifications.

---

## Quick Reference

| Detail | Info |
|---|---|
| **Exam Code** | EX200 |
| **Full Name** | Red Hat Certified System Administrator |
| **Provider** | Red Hat |
| **Format** | Performance-based (hands-on tasks on a live RHEL system) |
| **Duration** | 3 hours |
| **Passing Score** | 210/300 (70%) |
| **Cost** | $500 USD (varies by region) |
| **Validity** | 3 years |
| **Delivery** | Individual exam (in-person testing center) or Remote (RHU Individual Exam) |
| **Current RHEL Version** | RHEL 10 (the EX200 page says the exam "is based on Red Hat Enterprise Linux 10", read 2026-11-22; these notes were written for RHEL 9) |
| **Prerequisites** | None formally; recommended Red Hat System Administration I (RH124) and II (RH134) courses or equivalent |

**[📖 Official RHCSA page](https://www.redhat.com/en/services/certification/rhcsa)**
**[📖 EX200 Exam Objectives](https://www.redhat.com/en/services/training/ex200-red-hat-certified-system-administrator-rhcsa-exam)**

---

## What You Need to Do

The exam tests applied skills across these objective categories:

1. **Understand and use essential tools** - shell, file management, redirection, regex, file searching, archives, vi/vim editor.
2. **Operate running systems** - boot/reboot, runlevels/targets, systemd services, log inspection, processes.
3. **Configure local storage** - partitions, LVM (physical volumes, volume groups, logical volumes), filesystems (ext4, xfs), swap.
4. **Create and configure file systems** - mount/unmount, automount, NFS, network filesystems, ACLs, SELinux contexts.
5. **Deploy, configure, and maintain systems** - kickstart, network config, time sync, firewall (firewalld), selinux modes.
6. **Manage basic networking** - hostnames, IPv4/IPv6, network teams/bonds, routing.
7. **Manage users and groups** - account creation, password aging, group membership, sudoers.
8. **Manage security** - firewalld, SELinux booleans and contexts, basic SSH key setup.
9. **Manage containers** - install Podman, run/manage containers, persistent storage with containers, network with containers, build/deploy with `podman generate systemd` or Quadlet.

The exam is **closed-book during the test**, but you have access to system documentation: `man` pages, `info`, `--help` flags, and files in `/usr/share/doc/`.

---

## Exam Domains and Notes

| # | Domain | Notes File |
|---|---|---|
| 1 | System configuration, boot, services | [01-system-config.md](notes/01-system-config.md) |
| 2 | Storage and filesystems (LVM, partitions, mounts) | [02-storage-filesystems.md](notes/02-storage-filesystems.md) |
| 3 | Users, groups, sudo, permissions | [03-users-groups-permissions.md](notes/03-users-groups-permissions.md) |
| 4 | systemd services, logs, time, processes | [04-services-systemd.md](notes/04-services-systemd.md) |
| 5 | Networking, firewalld, SELinux, SSH | [05-networking-security-selinux.md](notes/05-networking-security-selinux.md) |
| 6 | Containers with Podman | [06-containers-podman.md](notes/06-containers-podman.md) |

---

## Study Materials in This Guide

| File | Description |
|---|---|
| [fact-sheet.md](fact-sheet.md) | Reference with documentation links and high-yield facts |
| [notes/](notes/) | Six numbered topic files |
| [practice-plan.md](practice-plan.md) | 6-week study plan |
| [scenarios.md](scenarios.md) | 15 hands-on scenario tasks (closest analog to the exam format) |

---

## Recommended Study Time

| Background | Estimated Prep Time |
|---|---|
| Experienced Linux sysadmin (5+ years) | 3-4 weeks |
| Some Linux experience (1-2 years), no Red Hat | 6-8 weeks |
| New to Linux (Windows / cloud only) | 10-12 weeks; budget time for RH124 / RH134 fundamentals |

Plan on 1-2 hours of hands-on practice per day in addition to reading.

---

## Lab Setup

You **cannot pass RHCSA without hands-on practice.** Build a lab.

### Free / cheap options

- **Red Hat Developer Subscription** (free) - one production-equivalent RHEL license. [developers.redhat.com](https://developers.redhat.com)
- **AlmaLinux / Rocky Linux** (free, RHEL-compatible) - for additional VMs without subscription.
- **VirtualBox / VMware Workstation Player** (free) - hypervisor on your workstation.
- **kvm/libvirt on a Linux host** - more realistic.

### Recommended lab topology

- One RHEL 9 VM as the primary system under test
- A second RHEL 9 (or AlmaLinux) VM for NFS / network tasks
- 4 GB RAM minimum per VM, 20 GB disk

### Cloud alternative

- **AWS EC2** with Red Hat Enterprise Linux 9 AMI - usable but adds AWS variables to your lab.
- **GCP / Azure** equivalents - similar.

---

## Exam-Day Tips

1. **Read every task fully before starting.** Some have multiple parts.
2. **Make changes persistent.** Many tasks specify "must survive reboot." Verify with `reboot` before declaring done.
3. **Use `man` and `--help`** liberally. The exam is open-documentation.
4. **Save your work often.** Don't lose progress to a moment of inattention.
5. **Watch the clock.** 3 hours total. If a task takes >20 minutes, move on and come back.
6. **Verify each task before moving on.** Re-run `systemctl status`, `mount`, `ls -la`, `getsebool` etc. to confirm.
7. **Reboot at the end.** Many "didn't pass" failures come from ephemeral changes that didn't survive reboot.

---

## After RHCSA

Common next steps:

- **Red Hat Certified Engineer (RHCE) - EX294** - automation with Ansible. RHCSA is a prerequisite.
- **OpenShift Administrator (EX280)** - the modern container platform path.
- **Linux Foundation Certified Engineer (LFCE)** - vendor-neutral parallel.
- **CompTIA Linux+** - vendor-neutral foundational alternative.

---

## Companion Materials in This Repo

- **[Linux Foundation LFCS](../../linux-foundation/lfcs/)** - vendor-neutral Linux admin cert (some objective overlap)
- **[Linux Foundation LFCA](../../linux-foundation/lfca/)** - foundational IT cert that covers some Linux basics
- **[OpenShift Administrator (EX280)](../openshift-administrator-ex280/)** - the natural Red Hat next step
- **[Kubernetes CKA](../../kubernetes/cka/)** - related container orchestration cert
