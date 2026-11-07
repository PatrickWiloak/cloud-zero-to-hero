---
last-updated: 2026-11-07
---

# CompTIA Linux+ (XK0-006) - High-Yield Scenarios and Patterns

Original administration scenarios in the style of the objectives. Each gives the analysis, the response and how to prevent a repeat. They are not vendor exam questions.

## System Management

### Logical Volume Grew, Filesystem Did Not
**Scenario**: An administrator runs `lvextend -L +20G /dev/vg_data/lv_app`. `lvs` shows the larger volume, but `df -h /srv/app` still shows the old size.

**Analysis**:
- **Clue**: the block device grew, the filesystem did not
- **Cause**: extending an LV does not resize the filesystem on it

**Response**:
1. For XFS: `xfs_growfs /srv/app` (mount point). For ext4: `resize2fs /dev/vg_data/lv_app`
2. Next time use `lvextend -r` to do both at once

**Prevention**: put the `-r` flag in the runbook.

### Server Drops to Emergency Mode After Adding a Disk
**Scenario**: After a line for a new data disk was added to `/etc/fstab` using `/dev/sdb1`, the server boots to an emergency shell. The disk was later replaced and is now `/dev/sdc`.

**Analysis**: a device name changed, and a missing mount stops boot unless told otherwise.

**Response**: fix `fstab` to use the UUID from `blkid`, add `nofail` if the mount is not critical, test with `mount -a`, then reboot.

**Prevention**: always use UUIDs, and run `mount -a` after every `fstab` edit.

### Out of Space With Space Free
**Scenario**: Writes fail with "No space left on device", yet `df -h` shows 40% free.

**Analysis**: either inodes or a quota. `df -i` shows 100% inode use. A mail spool holds millions of tiny files.

**Response**: find the directory (`find /var/spool -xdev -type f | cut -d/ -f1-4 | sort | uniq -c | sort -rn | head`), clean it, and consider recreating the filesystem with more inodes if this recurs.

**Prevention**: monitor inode usage with a threshold alert.

## Services and User Management

### Contractor Account Must End Friday
**Scenario**: A contractor needs access until 2026-12-04 and then none, including SSH keys.

**Response**:
- `chage -E 2026-12-04 contractor` (or `usermod -e`)
- Expiry blocks login by any method, unlike `passwd -l`, which still allows key-based SSH

**Prevention**: set expiry when the account is created.

### Service Starts by Hand but Not at Boot
**Scenario**: `systemctl start app` works. After a reboot the app is down.

**Analysis**: started is not enabled.

**Response**: `systemctl enable app` (or `enable --now`). If the unit file was edited, run `systemctl daemon-reload` first.

### Container Cannot Read a Bind Mount
**Scenario**: A container started with `-v /srv/web:/usr/share/nginx/html` returns 403 on an SELinux-enforcing host, although file permissions are 755.

**Analysis**: SELinux context on `/srv/web` does not permit container access.

**Response**: add the `:Z` option for private relabeling (`-v /srv/web:/usr/share/nginx/html:Z`) or apply the proper label with `semanage fcontext` and `restorecon`.

## Security

### Firewall Rule Disappears After Reload
**Scenario**: `firewall-cmd --add-service=https` made the site reachable. After `firewall-cmd --reload`, it is unreachable again.

**Analysis**: the rule was runtime-only.

**Response**: add it with `--permanent` and reload, or run `firewall-cmd --runtime-to-permanent` right after a verified runtime change.

### Web Server Cannot Reach the Database
**Scenario**: After a new application deploy on an enforcing SELinux host, the web server logs "connection refused" to a remote database, and the database is reachable from other hosts.

**Analysis**: SELinux policy blocks `httpd` from making network connections by default. `ausearch -m avc -ts recent` shows an AVC denial.

**Response**: `setsebool -P httpd_can_network_connect_db on` (or the broader `httpd_can_network_connect` if appropriate). Do not disable SELinux.

### Hardening SSH on an Internet-Facing Host
**Scenario**: Logs show thousands of failed password logins for root.

**Response**:
1. Set `PermitRootLogin no` and `PasswordAuthentication no`, and `AllowGroups sshusers`
2. Confirm key login works from a second session, run `sshd -t`, then `systemctl reload sshd`
3. Add `fail2ban` to ban repeated failures

**Prevention**: restrict the source with the firewall where the access pattern allows.

## Automation

### Playbook Is Not Idempotent
**Scenario**: A task uses `ansible.builtin.shell: echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf`. Each run appends another line.

**Response**: use a module that declares state, for example `ansible.posix.sysctl` with `sysctl_set: true` and `state: present`, or `lineinfile`.

### Script Breaks on a Filename With a Space
**Scenario**: `for f in $(ls); do rm $f; done` deletes the wrong things when a file is named `old report.txt`.

**Response**: quote and avoid parsing `ls`: `for f in *; do rm -- "$f"; done`, or use `find ... -print0 | xargs -0`.

## Troubleshooting

### Slow Server, Low CPU
**Scenario**: Users report a slow application. `uptime` shows a load average of 14 on a 4-core machine, but CPU use in `top` is 10% with 70% `wa`.

**Analysis**: load is high but CPU is idle, so processes are blocked on I/O. `iostat -x 1` shows one device at 100% utilization with long waits.

**Response**: identify the writer with `iotop` or `pidstat -d`, then fix the cause (runaway job, failing disk, swap thrash).

### Name Works on One Host, Fails on Another
**Scenario**: `ping 198.51.100.10` works from a new server, but `ping app.example.com` fails.

**Response**: DNS. Check `/etc/resolv.conf` or `resolvectl status`, confirm `hosts:` in `/etc/nsswitch.conf` includes `dns`, test with `dig @<dns-server> app.example.com`.

### Certificate Warnings After a Clock Reset
**Scenario**: A rebuilt VM reports certificate errors on every HTTPS call.

**Analysis**: the clock is far off, so valid certificates look not-yet-valid or expired. `timedatectl` shows NTP is not active.

**Response**: `timedatectl set-ntp true`, confirm the time sync, retest.
