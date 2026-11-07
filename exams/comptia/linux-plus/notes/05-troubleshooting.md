---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 30 min
---

# Domain 5: Troubleshooting (22%)

## Overview

The second-largest domain asks you to diagnose. Questions give symptoms and logs, and you pick the cause or the next command. The skill is a method: define the symptom, find the layer that is failing, check the obvious and cheap things first, change one thing at a time, and confirm the fix. Almost every symptom here maps to something you configured in Domains 1 to 3, so this domain rewards understanding over memorizing.

- **5.1** Monitoring concepts and configurations.
- **5.2** Hardware, storage and OS issues.
- **5.3** Networking issues.
- **5.4** Security issues.
- **5.5** Performance issues.

**[📖 CompTIA Linux+ XK0-006 Exam Objectives (PDF, version 5.0)](https://lecbyo.files.cmp.optimizely.com/download/90b9ac985c0e11f0b004a2a93c999a21)** - The official list of every topic and tool named in this domain

## 5.1 Monitoring

Monitoring is about knowing a service is in trouble before users tell you.

- **SLI** (service-level indicator) is a measurement, such as the fraction of successful requests. **SLO** (objective) is the target for it, such as 99.9% over 30 days. **SLA** (agreement) is the contractual promise to a customer, with consequences if missed. The order to remember: the SLI is measured, the SLO is the internal goal, the SLA is the contract.
- **Data acquisition**: **SNMP** polls devices or receives **traps** (unsolicited alerts); a **MIB** defines the objects a device exposes. Monitoring can be **agent**-based (software on the host sends data) or **agentless** (the monitor polls over SNMP, SSH or an API).
- **Health checks** test that a service answers correctly, for example an HTTP endpoint returning 200. **Webhooks** push event notifications to another system. **Log aggregation** ships logs from many hosts to one searchable place.
- **Thresholds** define when a metric is abnormal; crossing one raises an **alert** or **event** that sends a **notification** (email, chat, pager). Good thresholds are based on a measured baseline, not a guess. Alerts that fire constantly get ignored.

## 5.2 Hardware, storage and OS issues

Work from the symptom to the layer, using the logs and tools from earlier domains.

| Symptom | Likely causes and where to look |
|---|---|
| **Kernel panic** | Bad or missing driver, corrupt initrd, failed hardware, wrong root device. Read the last console lines; boot an earlier kernel from GRUB; rebuild the initrd with `dracut` |
| **Server does not turn on** | Power supply, cable, PDU, out-of-band controller. Check with `ipmitool` or the management console |
| **Server inaccessible** | Network, SSH down, firewall, hung host. Use the console or BMC to see whether the OS is up |
| **GRUB misconfiguration** | Boots to a `grub>` prompt or rescue shell. Reinstall or regenerate the config from a rescue environment |
| **Filesystem will not mount** | Wrong UUID or type in `fstab`, corruption (`fsck` or `xfs_repair` on the unmounted device), missing device. `blkid` shows real UUIDs; `journalctl -b` shows the failure |
| **Filesystem full** | `df -h` finds the full filesystem, `du -xh --max-depth=1 /var \| sort -h` finds the directory; a deleted file still held open by a process keeps its space until the process restarts (`lsof +L1`) |
| **Inode exhaustion** | "No space left" while `df -h` shows free space. `df -i` confirms; find the directory with millions of tiny files |
| **Partition not writable** | Mounted `ro` (often after errors), full, quota, or immutable attribute. Check `mount`, `lsattr` |
| **Quota issues** | User or group at the limit; `quota -u name`, `repquota` |
| **Data or kernel corruption** | Failing disk, abrupt power loss. Check SMART data with `smartctl -a /dev/sdX`; restore from backup |
| **Device failure** | RAID degraded in `/proc/mdstat`; replace the member and let it resync |
| **Missing or disabled driver** | Device absent from `lspci`/`ip link`; `modprobe`, check blacklists in `/etc/modprobe.d/` |
| **Package dependency issues** | Update repositories, resolve with the package manager rather than forcing with `rpm --nodeps` |
| **Systemd unit failure** | `systemctl status unit`, `journalctl -xeu unit`; common causes are a bad config file, a missing dependency or a port in use |
| **Killed processes** | The kernel's out-of-memory killer; `dmesg \| grep -i 'out of memory'` |
| **Segmentation fault** | A program accessed invalid memory: bad build, corrupt library, faulty RAM. Check the package, updates, `dmesg` |
| **Unresponsive process** | `strace -p`, `lsof -p`, last resort `kill -9` |
| **PATH misconfiguration** | "command not found" for an installed program; `echo $PATH`, `which`/`type`, fix `.bashrc` or `/etc/profile` |
| **Memory leak** | A process's resident memory grows steadily over time (`ps`, `top`), until swap or OOM |

Rescue approach for a system that will not boot: boot a rescue target (`systemd.unit=rescue.target` or `emergency.target` on the kernel line) or a live image, mount the root filesystem, check `fstab` and logs, and fix the configuration.

## 5.3 Networking issues

A layered method keeps you out of trouble: **link, address, route, name, service, firewall.**

```bash
ip link show                 # is the interface up, and is there a carrier?
ip -br address               # does it have the expected address?
ip route                     # is there a default route?
ping -c3 192.0.2.1           # can I reach the gateway?
ping -c3 198.51.100.10       # can I reach beyond it by address?
dig example.com              # does name resolution work?
ss -tlnp                     # is the service listening, and on what address?
tracepath example.com        # where does the path stop?
tcpdump -i eth0 port 53      # are packets actually arriving and leaving?
```

| Symptom | Interpretation |
|---|---|
| **Link down** | Cable, switch port, driver or virtual NIC disconnected. `ethtool eth0` shows "Link detected" |
| **Link negotiation issues** | Speed or duplex mismatch causes errors and slowness; `ethtool` shows the negotiated speed |
| **Cannot ping the server** | Down host, no route, firewall dropping ICMP, or wrong subnet. A blocked ping alone does not prove the host is down |
| **Ping by IP works, by name fails** | DNS: check `/etc/resolv.conf`, `resolvectl status`, `/etc/nsswitch.conf` order, and the DNS server itself |
| **Reaches local hosts only** | Missing or wrong default gateway; `ip route` |
| **Wrong subnet mask or gateway** | Host believes remote addresses are local; ARP fails |
| **IP conflict** | Two hosts with one address cause intermittent connectivity; `arping -D` detects it. Fix with a DHCP reservation |
| **DHCP issues** | Interface has a 169.254.x.x address or none; the DHCP server is unreachable or the scope is exhausted |
| **MTU mismatch** | Small packets work, large transfers hang; test with `ping -M do -s 1472 host` |
| **Bonding problems** | Wrong mode or a member link down; `/proc/net/bonding/bond0` |
| **MAC spoofing** | Duplicate or changing MACs, switch port security trips |
| **Dual stack issues** | IPv6 resolves first but is not routed, so connections time out before falling back to IPv4 |
| **Misconfigured firewall** | Service listening but unreachable from outside; check `firewall-cmd --list-all` or `ufw status` |
| **Server unreachable** | Work down the list above, from link upward |

## 5.4 Security issues

| Symptom | Interpretation and fix |
|---|---|
| **SELinux denial** | Application fails but permissions look right. `ausearch -m avc -ts recent` or `sealert` shows the denial. Typical causes: wrong **context** (fix with `semanage fcontext` and `restorecon`), a **boolean** not set (`setsebool -P`), or a missing policy module. Do not disable SELinux |
| **File permission problem** | `ls -l` and `namei -l /full/path` show the mode on every path component; also check **ACLs** (`getfacl`) and **attributes** (`lsattr`) |
| **Account access** | Locked (`passwd -S`), expired (`chage -l`), wrong shell, group membership not yet applied (the user must log in again), or PAM lockout (`faillock --user name`, and `--reset` to clear) |
| **Unpatched vulnerable systems** | Scanner or advisory flags a CVE; update packages, reboot if the kernel changed, confirm with the changelog because of backporting |
| **Exposed or misconfigured services** | `ss -tlnp` shows services listening on `0.0.0.0` that should be local; bind to localhost or firewall them |
| **Remote access issues** | `ssh -v user@host` shows where it fails: key permissions too open, `AllowUsers`, `PermitRootLogin`, wrong key offered, host key changed. On the server, `journalctl -u sshd` states the reason |
| **Certificate issues** | Expired, wrong name, missing intermediate or untrusted issuer. `openssl s_client -connect host:443 -servername host` and `openssl x509 -noout -dates` reveal it. Check the system clock |
| **Misconfigured package repository** | Signature errors, 404s or wrong release in `/etc/yum.repos.d` or `sources.list`; a key that was not imported |
| **Obsolete or insecure protocols and ciphers** | Telnet or FTP running, TLS 1.0 enabled, weak ciphers; **cipher negotiation** fails when client and server share no acceptable suite, so one side needs updating |

## 5.5 Performance issues

Performance work starts from a **baseline** of normal behavior; "slow" only means something compared with normal. Identify the constrained resource first: CPU, memory, disk I/O or network.

| Resource | Symptoms | Tools |
|---|---|---|
| **CPU** | High CPU usage, high load average with high CPU, slow response, CPU bottleneck, high context switching | `top`, `htop`, `mpstat -P ALL`, `pidstat`, `uptime` |
| **Memory** | Swapping, out-of-memory kills, sluggish terminal, slow startup | `free -h`, `vmstat 1`, `top` (sort by memory), `dmesg` |
| **Disk I/O** | High **I/O wait** (`wa` in `top`), high disk latency, blocked processes (state D), slow startup | `iostat -x 1`, `iotop`, `vmstat`, `fio` for benchmarking |
| **Network** | Packet drops, jitter, high latency, low throughput, random timeouts or disconnects | `ip -s link`, `ss -s`, `iperf3`, `mtr`, `ethtool -S` |
| **Remote storage** | Slow response from NFS or SMB mounts | `nfsstat`, `mount` options, network checks to the file server |
| **Security** | High failed log-in attempts | `lastb`, `journalctl -u sshd`; consider `fail2ban` and key-only SSH |

**Reading load average.** The three numbers from `uptime` are the average number of runnable and uninterruptible tasks over 1, 5 and 15 minutes. Compare to the CPU count (`nproc`): a load of 8 on a 4-core machine is oversubscribed. High load with **low** CPU use and high I/O wait means processes are blocked on disk or network, not computing. Swapping (nonzero `si`/`so` in `vmstat`) means the system ran out of RAM and is paging, which makes everything slow.

**A method:** note the symptom and when it started, check `uptime` and `top` for the constrained resource, check `dmesg` and the journal for errors, change a single variable, and compare against the baseline. Hardware errors (`dmesg`, SMART) should be ruled out before tuning software.

## Common exam traps

- A failed ping does not prove a host is down; ICMP may be blocked.
- "No space left on device" with free blocks means inodes (`df -i`) or a quota.
- Deleted-but-open files hold space until the process is restarted.
- Ping by IP working while names fail is a DNS problem.
- Group changes need a new login session.
- High load average with idle CPU points at I/O wait.
- Fix SELinux with context or boolean changes, not by disabling it.

## Key terms

- **Kernel panic** - a fatal kernel error from which the system cannot recover, often caused by drivers, a corrupt initrd or failing hardware.
- **Inode exhaustion** - running out of inodes so no new files can be created even though free space remains.
- **OOM killer** - the kernel mechanism that terminates processes to free memory when the system runs out of RAM and swap.
- **SMART** - disk self-monitoring data, read with smartctl, that can reveal a failing drive.
- **SLI** - a service-level indicator, a measured value such as the share of successful requests.
- **SLO** - a service-level objective, the internal target set for an SLI.
- **SLA** - a service-level agreement, the contractual commitment to a customer about service levels.
- **SNMP** - the Simple Network Management Protocol, used to poll devices or receive alerts called traps.
- **MIB** - a management information base, which defines the objects an SNMP device exposes.
- **Baseline** - a record of normal performance used to judge whether current behavior is abnormal.
- **Health check** - a test that a service responds correctly, such as an HTTP endpoint returning 200.
- **Log aggregation** - collecting logs from many hosts into one searchable location.
- **MTU mismatch** - a difference in maximum packet size along a path that makes small packets work while large transfers hang.
- **Link negotiation** - the speed and duplex agreement between an interface and its switch port; mismatches cause errors.
- **Dual stack** - running IPv4 and IPv6 at the same time, where a broken IPv6 path can cause delays.
- **Load average** - the average number of runnable and uninterruptible tasks over 1, 5 and 15 minutes.
- **I/O wait** - the share of time the CPU sits idle because processes are waiting on disk or network I/O.
- **Swapping** - moving memory pages to disk because RAM is exhausted, which greatly slows the system.
- **Context switching** - the kernel changing the CPU from one task to another; very high rates add overhead.
- **namei -l** - lists the owner and permissions of every component in a path, revealing where access is blocked.
- **faillock** - shows and resets PAM failed-login counters that lock an account.
- **cipher negotiation** - the TLS or SSH step where client and server choose a mutually supported cipher suite.
