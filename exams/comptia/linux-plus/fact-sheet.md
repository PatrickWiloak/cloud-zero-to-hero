---
last-updated: 2026-11-07
---

# CompTIA Linux+ (XK0-006) Fact Sheet

## Quick Reference

**Exam Code:** XK0-006 (V8)
**Duration:** 90 minutes
**Questions:** Maximum of 90 (multiple choice and performance-based)
**Passing Score:** 720 (scale of 100-900)
**Cost:** Not verified (no price on the CompTIA page)
**Validity:** Three years, renewable through the CompTIA CE program (see the table below)
**Delivery:** Not verified on the pages read
**Languages:** English

### Verified facts and sources (checked 2026-11-07)

| Fact | Value | Source |
|------|-------|--------|
| Exam code and version | XK0-006, V8 | [CompTIA Linux+ page](https://www.comptia.org/en-us/certifications/linux/) |
| Launch date | July 15, 2025 | CompTIA Linux+ page |
| Questions, length | Maximum of 90, 90 minutes | CompTIA Linux+ page and [objectives PDF v5.0](https://lecbyo.files.cmp.optimizely.com/download/90b9ac985c0e11f0b004a2a93c999a21) |
| Question types | Multiple choice and performance-based | Objectives PDF |
| Passing score | 720 on a scale of 100-900 | CompTIA Linux+ page |
| Domains and weights | 23 / 20 / 18 / 17 / 22 (below) | Objectives PDF (identical weights in v3.0 and v5.0) |
| Recommended experience | 12 months hands-on with Linux servers; A+, Network+, Server+ recommended | Objectives PDF |
| Accreditation | ISO 17024, accredited by ANSI | Objectives PDF |
| Retirement | "Usually three years after launch," estimated 2028 | CompTIA Linux+ page |
| Price | **Not verified.** The page shows Buy Now links with no figure | Check the CompTIA store for your region |
| Validity and renewal | Linux+ is in the CE Program; CE requirements must be met "within three years of earning or renewing your certification." The CEU count for XK0-006 specifically was **not verified**; check your CompTIA Central account | [CompTIA CE Program FAQ](https://www.comptia.org/en-us/resources/ce/learn/comptia-continuing-education-program-faq/) |
| XK0-005 retirement | A third-party guide reports January 13, 2026. **Not verified** on a CompTIA page | Not an official source |

The objectives PDF is published on a CompTIA file host as two documents with different version numbers (3.0 and 5.0), same domain weights. This guide follows version 5.0.

## Exam Domain Breakdown

| Domain | Weight | Focus |
|--------|--------|-------|
| 1.0 System Management | 23% | Boot, FHS, devices, storage and LVM, networking, shell, backup, virtualization |
| 2.0 Services and User Management | 20% | Files, accounts, processes, packages, systemd, containers |
| 3.0 Security | 18% | AAA, firewalls, hardening, SELinux, SSH, cryptography, compliance |
| 4.0 Automation, Orchestration, and Scripting | 17% | IaC, shell scripting, Python, Git, responsible AI |
| 5.0 Troubleshooting | 22% | Monitoring, OS and hardware, network, security, performance |

## Objective Map

| Objective | Topic | Note |
|-----------|-------|------|
| 1.1 | Basic Linux concepts | [01](notes/01-system-management.md) |
| 1.2 | Device management | [01](notes/01-system-management.md) |
| 1.3 | Storage | [01](notes/01-system-management.md) |
| 1.4 | Network services and configuration | [01](notes/01-system-management.md) |
| 1.5 | Shell operations | [01](notes/01-system-management.md) |
| 1.6 | Backup and restore | [01](notes/01-system-management.md) |
| 1.7 | Virtualization | [01](notes/01-system-management.md) |
| 2.1-2.6 | Files, accounts, processes, software, systemd, containers | [02](notes/02-services-and-user-management.md) |
| 3.1-3.6 | AAA, firewalls, OS hardening, account hardening, crypto, compliance | [03](notes/03-security.md) |
| 4.1-4.5 | Automation, shell scripts, Python, Git, AI | [04](notes/04-automation-orchestration-scripting.md) |
| 5.1-5.5 | Monitoring, OS and hardware, network, security, performance | [05](notes/05-troubleshooting.md) |

## Package Manager Equivalents

| Task | RPM family (dnf) | Debian family (apt) |
|------|------------------|---------------------|
| Install | `dnf install pkg` | `apt install pkg` |
| Remove | `dnf remove pkg` | `apt remove pkg` |
| Update all | `dnf upgrade` | `apt update && apt upgrade` |
| List installed | `rpm -qa` | `dpkg -l` |
| Files in a package | `rpm -ql pkg` | `dpkg -L pkg` |
| Package owning a file | `rpm -qf /path` | `dpkg -S /path` |
| Repository config | `/etc/yum.repos.d/` | `/etc/apt/sources.list.d/` |

## Key Files

| Path | Purpose |
|------|---------|
| `/etc/fstab` | Filesystems mounted at boot |
| `/etc/passwd`, `/etc/shadow`, `/etc/group` | Accounts, hashes, groups |
| `/etc/sudoers`, `/etc/sudoers.d/` | sudo rules (edit with `visudo`) |
| `/etc/ssh/sshd_config` | SSH server configuration |
| `/etc/hosts`, `/etc/resolv.conf`, `/etc/nsswitch.conf` | Name resolution |
| `/etc/netplan/` | Netplan YAML (Ubuntu) |
| `/etc/systemd/system/` | Local unit files and overrides |
| `/etc/pam.d/` | PAM stacks |
| `/etc/audit/rules.d/` | Audit rules |
| `/etc/issue`, `/etc/issue.net`, `/etc/motd` | Login banners |
| `/var/log/` | Logs (`secure` or `auth.log` for authentication) |
| `/proc/mdstat`, `/proc/mounts`, `/proc/cmdline` | RAID state, mounts, boot parameters |

## Commands by Task

| Task | Commands |
|------|----------|
| Storage | `lsblk`, `blkid`, `fdisk`, `parted`, `pvcreate`, `vgcreate`, `lvcreate`, `lvextend -r`, `xfs_growfs`, `resize2fs`, `mdadm` |
| Network | `ip`, `ss`, `nmcli`, `netplan try`, `dig`, `tcpdump`, `mtr`, `ethtool` |
| Users | `useradd`, `usermod -aG`, `chage`, `passwd -l`, `id`, `getent` |
| Processes | `ps`, `top`, `pidstat`, `strace`, `nice`, `renice`, `kill`, `crontab` |
| Services | `systemctl enable --now`, `systemctl mask`, `daemon-reload`, `journalctl -u` |
| Security | `firewall-cmd`, `ufw`, `setfacl`, `chattr`, `restorecon`, `setsebool -P`, `auditctl`, `cryptsetup` |
| Containers | `docker run -p -v -e`, `docker exec`, `podman ps`, `docker logs` |
| Performance | `uptime`, `vmstat`, `iostat -x`, `free -h`, `mpstat`, `iperf3` |

## Default Ports to Know

| Port | Service |
|------|---------|
| 22/tcp | SSH, SFTP |
| 25/tcp | SMTP |
| 53 | DNS (UDP and TCP) |
| 67-68/udp | DHCP |
| 80/tcp, 443/tcp | HTTP, HTTPS |
| 123/udp | NTP |
| 143/tcp | IMAP |
| 389/tcp, 636/tcp | LDAP, LDAPS |
| 88 | Kerberos |
| 2049 | NFS |
| 445/tcp | SMB |

**[📖 IANA Service Name and Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)** - The authoritative port list

## Official Resources

- **[📖 CompTIA Linux+ Certification](https://www.comptia.org/en-us/certifications/linux/)** - Exam details
- **[📖 XK0-006 Exam Objectives (PDF, version 5.0)](https://lecbyo.files.cmp.optimizely.com/download/90b9ac985c0e11f0b004a2a93c999a21)** - Full objectives and acronym list
