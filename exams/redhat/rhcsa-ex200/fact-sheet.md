---
last-updated: 2026-11-22
---

# RHCSA (EX200) - Fact Sheet

## Quick Reference

**Exam Code:** EX200
**Duration:** 3 hours
**Format:** Performance-based hands-on tasks on a live system. The exam page now says the exam "is based on Red Hat Enterprise Linux 10" (read 2026-11-22); these notes were written for RHEL 9, so check each task against the RHEL 10 docs
**Passing Score:** 210 / 300 (70%) (not stated on the EX200 page; widely reported)
**Cost:** $500 USD (US list; the EX200 page prices by region, check it)
**Validity:** 3 years (not stated on the EX200 or RHCSA page)
**Open documentation during exam:** `man`, `info`, `--help`, `/usr/share/doc/`
**Internet access during exam:** No

**[📖 Official RHCSA page](https://www.redhat.com/en/services/certification/rhcsa)**
**[📖 Exam objectives](https://www.redhat.com/en/services/training/ex200-red-hat-certified-system-administrator-rhcsa-exam)**
**[📖 RHEL 10 Documentation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10)**
**[📖 RHEL 9 Documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9)** - what these notes were written against

---

## Exam Objectives (RHEL 9)

The exam is a list of practical tasks with no domain weights published. Red Hat groups objectives into these categories:

1. Understand and use essential tools
2. Operate running systems
3. Configure local storage
4. Create and configure file systems
5. Deploy, configure, and maintain systems
6. Manage basic networking
7. Manage users and groups
8. Manage security
9. Manage containers (Podman)

All categories are tested. Don't skip any.

---

## High-Yield Commands by Category

### Essential tools

| Task | Command |
|---|---|
| Login as different user | `su - username` |
| Become root | `sudo -i` or `sudo su -` |
| Find files | `find / -name 'pattern'` |
| Search file content | `grep -r 'pattern' /path` |
| Archive (tar.gz) | `tar -czvf archive.tar.gz /path` |
| Extract archive | `tar -xzvf archive.tar.gz` |
| Copy file across hosts | `scp file user@host:/path` |
| Sync directories | `rsync -avz src/ user@host:dst/` |
| Check disk usage | `df -h` (free), `du -sh /path` (used) |
| File permissions | `chmod 644 file`, `chown user:group file` |

### Operate running systems

| Task | Command |
|---|---|
| List units | `systemctl list-units` |
| Start/stop/restart/status | `systemctl start \| stop \| restart \| status servicename` |
| Enable on boot | `systemctl enable --now servicename` |
| Disable | `systemctl disable --now servicename` |
| Reboot | `systemctl reboot` or `reboot` |
| Power off | `systemctl poweroff` |
| Default target | `systemctl get-default` / `systemctl set-default multi-user.target` |
| Boot to target | At GRUB menu, edit kernel line and append `systemd.unit=rescue.target` (or emergency, multi-user) |
| Kernel boot params | `cat /proc/cmdline` |
| Reset root password | Boot to emergency mode → `chroot /sysroot` → `passwd root` → `touch /.autorelabel` → reboot |

### Local storage and filesystems

| Task | Command |
|---|---|
| List block devices | `lsblk` |
| List partitions | `fdisk -l` or `parted -l` |
| Create partition (interactive) | `fdisk /dev/sdX` |
| Create filesystem | `mkfs.xfs /dev/sdX1` or `mkfs.ext4 /dev/sdX1` |
| Mount | `mount /dev/sdX1 /mnt/foo` |
| Persistent mount | Add line to `/etc/fstab`, then `systemctl daemon-reload && mount -a` |
| Get UUID | `blkid /dev/sdX1` |
| Make swap | `mkswap /dev/sdX2 && swapon /dev/sdX2` |
| LVM: physical volume | `pvcreate /dev/sdX1` |
| LVM: volume group | `vgcreate vg_data /dev/sdX1 /dev/sdY1` |
| LVM: logical volume | `lvcreate -L 5G -n lv_data vg_data` |
| Extend LV | `lvextend -L +2G /dev/vg_data/lv_data` |
| Resize XFS | `xfs_growfs /mnt/foo` (online) |
| Resize ext4 | `resize2fs /dev/vg_data/lv_data` |
| Reduce LV | shrink filesystem first (`resize2fs`), then `lvreduce` |

### Users and groups

| Task | Command |
|---|---|
| Add user | `useradd -m username` |
| Set password | `passwd username` |
| Add group | `groupadd groupname` |
| Add user to group | `usermod -aG groupname username` |
| Password aging | `chage -M 90 -W 7 username` |
| Lock / unlock | `usermod -L username` / `usermod -U username` |
| Sudo for a group | Add `%groupname ALL=(ALL) ALL` to `/etc/sudoers.d/groupname` |
| Sudo NOPASSWD | `username ALL=(ALL) NOPASSWD: ALL` |

### Networking

| Task | Command |
|---|---|
| Show interfaces | `ip a` or `nmcli device status` |
| Show routes | `ip r` or `nmcli con show CONNAME` |
| Hostname | `hostnamectl set-hostname host1.example.com` |
| Add IP / network | `nmcli connection modify CONN ipv4.addresses 192.0.2.10/24 ipv4.gateway 192.0.2.1 ipv4.dns 8.8.8.8 ipv4.method manual` |
| Apply | `nmcli connection up CONN` |
| Test | `ping -c 3 host` / `ss -tlnp` |
| DNS lookup | `dig +short example.com` / `getent hosts example.com` |
| Time sync | `timedatectl set-timezone America/New_York`; `systemctl enable --now chronyd`; `chronyc sources` |

### Firewall (firewalld)

| Task | Command |
|---|---|
| Status | `firewall-cmd --state` |
| List zones | `firewall-cmd --get-active-zones` |
| Default zone | `firewall-cmd --set-default-zone=public` |
| List services in zone | `firewall-cmd --list-all` |
| Add service permanently | `firewall-cmd --permanent --add-service=http` |
| Add port permanently | `firewall-cmd --permanent --add-port=8080/tcp` |
| Reload | `firewall-cmd --reload` |
| Rich rule example | `firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.0/24" service name="ssh" accept'` |

### SELinux

| Task | Command |
|---|---|
| Current mode | `getenforce` |
| Set mode (runtime) | `setenforce 0` (permissive) / `setenforce 1` (enforcing) |
| Set mode (persistent) | edit `/etc/selinux/config` `SELINUX=enforcing` |
| List contexts | `ls -lZ /path` |
| Change context (one-shot) | `chcon -t httpd_sys_content_t /path/file` |
| Add persistent rule | `semanage fcontext -a -t httpd_sys_content_t '/path(/.*)?'` then `restorecon -Rv /path` |
| List booleans | `getsebool -a` |
| Set boolean | `setsebool -P httpd_can_network_connect on` |
| Audit log | `tail /var/log/audit/audit.log` or `ausearch -m avc -ts recent` |
| Diagnose denial | `sealert -a /var/log/audit/audit.log` |

### Logs and journald

| Task | Command |
|---|---|
| Recent boot logs | `journalctl -b` (current boot), `journalctl -b -1` (previous) |
| Service logs | `journalctl -u servicename` |
| Follow live | `journalctl -f` |
| Specific time | `journalctl --since "2 hours ago"` |
| Persistent journal | `mkdir -p /var/log/journal && systemctl restart systemd-journald` |
| Files in /var/log | `/var/log/messages`, `/var/log/secure`, `/var/log/audit/audit.log`, `/var/log/cron`, `/var/log/maillog` |

### Containers (Podman)

| Task | Command |
|---|---|
| Install | `dnf install -y container-tools` |
| Pull image | `podman pull registry.access.redhat.com/ubi9/ubi:latest` |
| Run | `podman run -d --name web -p 8080:80 docker.io/nginx` |
| List | `podman ps` (running), `podman ps -a` (all) |
| Logs | `podman logs web` |
| Exec | `podman exec -it web /bin/bash` |
| Stop / remove | `podman stop web && podman rm web` |
| Volume mount | `podman run -v /host/path:/container/path:Z` (`Z` sets SELinux private label) |
| Generate systemd unit | `podman generate systemd --new --name web > ~/.config/systemd/user/web.service` |
| User-mode systemd unit | `systemctl --user daemon-reload && systemctl --user enable --now web.service` |
| Enable lingering | `loginctl enable-linger username` (so user services run at boot) |
| Quadlet | Place `*.container` files in `~/.config/containers/systemd/` for declarative units |

---

## High-Yield Reset and Recovery

### Reset root password (RHEL 9)

1. Reboot.
2. At GRUB menu, press `e` to edit the entry.
3. Find the line starting with `linux` and append `rd.break enforcing=0`.
4. Press `Ctrl-X` to boot.
5. At the prompt: `mount -o remount,rw /sysroot`
6. `chroot /sysroot`
7. `passwd root`
8. Set new password.
9. `touch /.autorelabel` (forces SELinux relabel on next boot).
10. `exit; exit` to reboot.
11. After reboot, the system relabels (slow first boot), then comes up normally.

### Boot to emergency / rescue / specific target

At GRUB, press `e`, append `systemd.unit=rescue.target` (or `emergency.target` or `multi-user.target`).

---

## Things candidates commonly forget

- **Persistent fstab.** Don't just `mount` - also add to `/etc/fstab` if "persistent" or "after reboot."
- **systemctl daemon-reload** after editing unit files.
- **firewall-cmd --reload** after `--permanent` changes.
- **setsebool -P** for persistent boolean changes (without `-P`, they reset on reboot).
- **`chage -d 0 username`** to force password change at next login.
- **`useradd -m`** to create home directory; without `-m` no home dir.
- **`umask`** in `/etc/profile` or `/etc/login.defs` for default permissions.
- **Reboot test.** Reboot before declaring you're done with the section.

---

## Useful References During Exam

You can read these files / use these commands during the exam:

- `man <topic>` - the canonical reference. `man -k keyword` searches by keyword.
- `info <topic>`
- `<command> --help`
- `/usr/share/doc/<package>/` for package-specific docs
- `cat /etc/services` for port-to-service mapping
- `cat /etc/passwd`, `cat /etc/group`, `cat /etc/shadow`, `cat /etc/sudoers`

---

## When in doubt

- **Read the task twice.** Many tasks have small details that change the answer (specific user, specific filesystem type, specific permission).
- **Verify with the right command.** `mount` shows mounts. `lsblk` shows block devices and their mount points. `getenforce` shows SELinux mode. `firewall-cmd --list-all` shows current firewall.
- **Be persistent.** Many tasks demand survival across reboot. Reboot to test.

---

## After-pass next steps

| Cert | Why |
|---|---|
| **RHCE (EX294)** - Ansible automation | RHCSA is a prereq |
| **OpenShift Administrator (EX280)** | Container platform on RHEL |
| **Red Hat Certified Specialist** in Containers, Storage, Security, etc. | Specialty paths |
| **CKA** | Vendor-neutral Kubernetes |
