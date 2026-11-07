---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 35 min
---

# Domain 2: Services and User Management (20%)

## Overview

This domain is the day-to-day work of running a server: finding and manipulating files, creating and locking user accounts, watching and controlling processes, installing software, running services under systemd, and running applications in containers. Scenario questions here usually give you a symptom ("the service does not start after reboot", "the contractor's account must expire Friday") and ask for the right command or file.

- **2.1** Manage files and directories.
- **2.2** Perform local account management.
- **2.3** Manage processes and jobs.
- **2.4** Configure and manage software.
- **2.5** Manage Linux using systemd.
- **2.6** Manage applications in a container on a Linux server.

**[📖 CompTIA Linux+ XK0-006 Exam Objectives (PDF, version 5.0)](https://lecbyo.files.cmp.optimizely.com/download/90b9ac985c0e11f0b004a2a93c999a21)** - The official list of every topic and tool named in this domain

## 2.1 Files and directories

The core utilities are `ls`, `cd`, `pwd`, `cp`, `mv`, `rm`, `rmdir`, `mkdir`, `touch`, `stat`, `file`, `diff` and `sdiff`. `stat` shows size, permissions, inode and all three timestamps (access, modify, change). `file` identifies content by inspecting it rather than trusting the extension.

### Finding things

`find` walks the tree live and filters on attributes. `locate` queries a prebuilt database, so it is fast but can be stale until `updatedb` runs. `lsof` lists open files, which also covers sockets.

```bash
find /var -type f -size +100M                 # large files
find /home -user alice -name '*.log' -mtime +90   # old files owned by alice
find /srv -type f -perm /4000                 # files with the setuid bit
lsof -i :443                                  # which process has port 443 open
lsof +D /mnt/data                             # what is keeping this mount busy
```

`lsof +D` is the standard answer to "umount says the target is busy".

### Links

A **hard link** is another directory entry pointing at the same inode. It cannot cross filesystems, and deleting one name does not remove the data while another name exists. A **symbolic link** is a small file containing a path. It can cross filesystems and point at directories, and it breaks if the target is removed.

```bash
ln /data/report.txt /data/report-hard.txt        # hard link
ln -s /opt/app-2.4 /opt/app                      # symlink, a common release pattern
```

### Device files

Entries in `/dev` come in kinds, shown by the first character of `ls -l`. A `b` is a **block device** (disks, accessed in blocks and buffered). A `c` is a **character device** (terminals, serial ports, accessed as a stream). Special character devices include `/dev/null` (discards writes), `/dev/zero` (endless zero bytes) and `/dev/urandom` (random bytes).

## 2.2 Local account management

### Files that define accounts

| File | Contents |
|---|---|
| `/etc/passwd` | One line per user: name, `x` placeholder, UID, GID, comment, home, shell. World-readable |
| `/etc/shadow` | Password hashes and aging data. Readable only by root |
| `/etc/group` | Group names, GIDs and members |
| `/etc/skel` | Template files copied into every new home directory |
| `/etc/profile` | System-wide login shell settings |

A **UID** identifies a user, a **GID** identifies a group. The **effective** IDs (EUID, EGID) are the ones the kernel checks for permissions on a running process; they differ from the real IDs when a program is setuid. System and service accounts (daemons) normally use a low UID range and have a shell such as `/sbin/nologin`; ordinary users start at 1000 on most distributions (the range is set in `/etc/login.defs`).

### Add, modify, delete

```bash
useradd -m -s /bin/bash -G developers alice   # create with home directory and a secondary group
passwd alice                                  # set the password
usermod -aG docker alice                      # APPEND a supplementary group (-a is critical)
usermod -s /sbin/nologin svc-backup           # block interactive login
userdel -r alice                              # remove the user and the home directory
groupadd developers
groupmod -n devs developers                   # rename a group
groupdel devs
```

The `-a` in `usermod -aG` is a classic trap. Without it, `-G` replaces the user's supplementary groups. `adduser` and `deluser` are friendlier wrappers on Debian-family systems.

### Locking, expiry and aging

```bash
passwd -l alice            # lock the password (prefixes the hash with !)
usermod -L alice           # same effect
usermod -U alice           # unlock
usermod -e 2026-12-31 contractor   # account expires on a date
chage -l alice             # show aging settings
chage -M 90 -W 14 -m 1 alice   # max age 90 days, warn 14 days ahead, min 1 day between changes
chage -E 2026-12-31 contractor # same as usermod -e
chage -d 0 alice           # force a password change at next login
```

Locking the password does not stop SSH key logins. To fully disable an account, also expire it or change its shell.

**[📖 useradd(8)](https://man7.org/linux/man-pages/man8/useradd.8.html)** - Account creation options and defaults
**[📖 chage(1)](https://man7.org/linux/man-pages/man1/chage.1.html)** - Password aging and account expiry options

### Who is logged in

`id` prints UID, GID and groups. `whoami` prints the effective user. `who` and `w` show current sessions (and `w` shows what each is running). `last` reads login history and `lastlog` shows each account's most recent login. `getent passwd alice` queries every configured name source (local files, LDAP, SSSD), so it finds directory users that `grep alice /etc/passwd` misses. `groups alice` lists group membership.

## 2.3 Processes and jobs

### Looking at processes

Every process has a PID and a parent (PPID). States: **running**, **sleeping** (waiting for an event, the normal idle state), **blocked** (often uninterruptible I/O wait, shown as `D`), **stopped** (suspended with a signal) and **zombie** (finished but not yet reaped by its parent). A zombie uses no CPU or memory beyond its table entry, and you cannot kill it; you fix or restart the parent.

| Tool | Use |
|---|---|
| `ps aux`, `ps -ef` | Snapshot of all processes |
| `pstree` | Parent/child tree |
| `top`, `htop`, `atop` | Live view, sortable |
| `pidstat`, `mpstat` | Per-process and per-CPU statistics over time |
| `/proc/<PID>/` | Raw per-process detail (cmdline, status, fd/) |
| `strace -p <PID>` | Trace the system calls a process makes |
| `lsof -p <PID>` | Files that process holds open |

### Priority and signals

Niceness runs from -20 (highest priority) to 19 (lowest); the default is 0. Ordinary users can only raise niceness.

```bash
nice -n 10 ./batch-job.sh        # start at lower priority
renice -n 5 -p 4321              # change a running process
```

Signals are messages to processes. `kill <PID>` sends SIGTERM (15) by default, which asks the program to shut down cleanly. SIGHUP (1) traditionally means "reload your configuration" for daemons. SIGKILL (9) cannot be caught and gives the process no chance to clean up, so it is the last resort. `killall name` and `pkill pattern` signal by name.

### Foreground, background and persistence

`command &` starts a job in the background. `Ctrl+z` suspends the foreground job, `bg` resumes it in the background, `fg` brings it back and `jobs` lists them. `Ctrl+c` interrupts and `Ctrl+d` sends end-of-input. `nohup command &` keeps a job alive after you log out. `exec` replaces the shell with the command rather than starting a child.

### Scheduling

`cron` runs recurring jobs from a crontab (`crontab -e` edits yours, `crontab -l` lists). Five time fields precede the command: minute, hour, day of month, month, day of week.

```text
# m  h  dom mon dow  command
30 2 * * 0   /usr/local/bin/weekly-backup.sh
*/15 * * * * /usr/local/bin/poll.sh
```

`at` runs a one-time job (`echo "/usr/local/bin/once.sh" | at 23:00`). `anacron` runs periodic jobs on machines that are not always on, catching up missed runs, which is why laptops use it. systemd timers (section 2.5) are the modern alternative.

**[📖 crontab(5)](https://man7.org/linux/man-pages/man5/crontab.5.html)** - Crontab field syntax

## 2.4 Software

### Package managers

| Family | Low level | High level |
|---|---|---|
| RPM (RHEL, Fedora, SUSE) | `rpm` | `dnf` (older `yum`), `zypper` on SUSE |
| dpkg (Debian, Ubuntu) | `dpkg` | `apt` |

```bash
dnf install nginx               apt install nginx
dnf remove nginx                apt remove nginx
dnf update                      apt update && apt upgrade
rpm -qa | grep nginx            dpkg -l | grep nginx
rpm -ql nginx                   dpkg -L nginx
rpm -qf /usr/sbin/nginx         dpkg -S /usr/sbin/nginx
dnf provides '*/semanage'       apt-file search semanage
```

The high-level tool resolves **dependencies** and reports **conflicts**; the low-level tool does not. **Repositories** are enabled or disabled in `/etc/yum.repos.d/` (RPM) or `/etc/apt/sources.list` and `sources.list.d/` (dpkg). Third-party repositories are a trust decision: package and repository **GPG signatures** let the package manager verify that packages came from the key you imported. You can exclude a package from updates (`exclude=` in dnf configuration, `apt-mark hold` on Debian family). Language ecosystems have their own managers: `pip` (Python), `cargo` (Rust), `npm` (Node). On Debian systems `update-alternatives` selects which of several installed implementations a generic command name points to.

Sandboxed application formats (Snap, Flatpak) bundle their dependencies and confine the app, trading disk space for isolation. Installing from source follows the usual `./configure`, `make`, `make install` pattern, but the files are then outside the package manager's records, which is why packages are preferred.

### Basic service configuration

The objectives list the protocols you should be able to configure at a basic level: DHCP, HTTP servers (Apache `httpd` and Nginx), SMTP, IMAP4, DNS and time synchronization (NTP and PTP). For the exam, know the default ports (DHCP 67/68 UDP, HTTP 80, HTTPS 443, SMTP 25, IMAP 143, DNS 53, NTP 123 UDP), where the main config lives (`/etc/nginx/nginx.conf`, `/etc/httpd/conf/httpd.conf`) and that you validate before reload (`nginx -t`, `apachectl configtest`). `chronyd` is the common time daemon on RHEL family, and `timedatectl` reports sync status.

## 2.5 systemd

systemd's building block is the **unit**. Types in the objectives are services (`.service`), timers (`.timer`), mounts (`.mount`) and targets (`.target`, groups of units that act like runlevels).

```bash
systemctl status nginx
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl reload nginx                # ask the service to re-read config without a restart
systemctl enable nginx                # start at boot (creates symlinks)
systemctl enable --now nginx          # enable and start in one step
systemctl disable nginx
systemctl mask nginx                  # link to /dev/null: cannot be started by anything
systemctl unmask nginx
systemctl edit nginx                  # create a drop-in override
systemctl daemon-reload               # re-read unit files after you change them
systemctl get-default                 # default target
systemctl isolate rescue.target       # switch to a different target now
```

Distinguish **enable** (start at boot) from **start** (start now) and **mask** (forbid) from **disable** (just do not start automatically). Unit files in `/usr/lib/systemd/system/` come from packages; put your own overrides in `/etc/systemd/system/` so package updates do not overwrite them, which is exactly what `systemctl edit` does.

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Nightly backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh

# /etc/systemd/system/backup.timer
[Unit]
Description=Run backup nightly

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable the timer, not the service: `systemctl enable --now backup.timer`. `Persistent=true` runs a missed job after the machine was off.

Related utilities: `journalctl -u nginx` for a unit's logs, `systemd-analyze blame` to see which units slowed boot, `hostnamectl` to set the hostname, `timedatectl` for time zone and NTP, `resolvectl` for DNS settings under systemd-resolved and `sysctl` for kernel parameters (`sysctl -w net.ipv4.ip_forward=1` for runtime; a file in `/etc/sysctl.d/` to persist).

**[📖 systemctl](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html)** - Every verb: enable, mask, edit, daemon-reload and more
**[📖 systemd.timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html)** - Calendar and monotonic timers, Persistent=

## 2.6 Containers on Linux

A container is a normal Linux process (or group of processes) isolated with namespaces and limited with cgroups, started from an image. Container **runtimes** named by the objectives: **runC** (the low-level OCI runtime), **containerd** (a daemon that manages containers using runC), **Docker** (a client and daemon built on containerd) and **Podman** (daemonless, can run rootless, and mostly CLI-compatible with Docker).

### Images

```bash
docker pull nginx:1.27                      # image tag after the colon
docker build -t myapp:1.0 .                 # build from the Dockerfile in this directory
docker image ls
docker image prune                          # remove dangling images
```

A **Dockerfile** is a recipe; each instruction adds a **layer**. The instructions the objectives name:

```dockerfile
FROM python:3.12-slim          # base image
COPY app/ /app/
WORKDIR /app
USER 1000                      # run as an unprivileged user, not root
ENTRYPOINT ["python"]          # the fixed executable
CMD ["main.py"]                # default arguments, easily overridden
```

`ENTRYPOINT` is the program that always runs; `CMD` supplies default arguments that `docker run image other.py` replaces.

### Containers and volumes

```bash
docker run -d --name web -p 8080:80 -e APP_ENV=prod -v /srv/web:/usr/share/nginx/html:ro nginx:1.27
docker logs web
docker exec -it web sh
docker inspect web
docker stop web && docker rm web
docker volume create appdata
docker run -d -v appdata:/var/lib/data myapp:1.0
```

`-p host:container` maps a port. `-v` maps a volume or a host directory. On SELinux systems, a bind mount often needs a label option so the container is allowed to read it: `-v /srv/web:/data:Z` relabels the content privately for this container, `:z` shares it among containers. Podman uses the same flag syntax: `podman run -d --name web -p 8080:80 nginx:1.27`.

**[📖 docker container run](https://docs.docker.com/reference/cli/docker/container/run/)** - Run options including -p, -v, -e and --privileged
**[📖 docker system prune](https://docs.docker.com/reference/cli/docker/system/prune/)** - What the command removes by default and what `-a` and `--volumes` add
**[📖 podman-run](https://docs.podman.io/en/latest/markdown/podman-run.1.html)** - Podman's run options, including rootless behavior

### Container networks

| Driver | Behavior |
|---|---|
| **bridge** | The default. Containers on a private virtual switch, reached from outside via port mapping |
| **host** | Shares the host's network stack; no isolation, no port mapping needed |
| **none** | No networking |
| **overlay** | Spans multiple hosts (Swarm or similar) |
| **macvlan** | Gives a container its own MAC address on the physical network |
| **ipvlan** | Like macvlan but containers share the host's MAC address |

`docker network create appnet` makes a user-defined bridge on which containers resolve each other by name.

**Privileged vs unprivileged.** `--privileged` gives a container almost all host capabilities and device access, which largely removes the isolation. Prefer unprivileged containers, a non-root `USER` and, with Podman, rootless mode. Cleaning up: `docker system prune` removes stopped containers, unused networks, dangling images and unused build cache (not volumes; `-a` extends it to all unused images).

## Common exam traps

- `usermod -G` without `-a` replaces groups.
- Locking a password does not block key-based SSH.
- A zombie process cannot be killed; handle the parent.
- `enable` does not start the service now; `start` does not survive a reboot.
- After editing a unit file, run `systemctl daemon-reload`.
- Enable the `.timer`, not the `.service` it triggers.
- `CMD` is overridable; `ENTRYPOINT` is the fixed program.

## Key terms

- **Hard link** - an additional directory entry pointing at the same inode; it cannot cross filesystems.
- **Symbolic link** - a small file holding a path to another file or directory; it can cross filesystems and break if the target is removed.
- **Block device** - a device such as a disk that is read and written in fixed-size blocks.
- **Character device** - a device such as a terminal that is read and written as a stream of bytes.
- **/etc/shadow** - the root-only file holding password hashes and password aging data.
- **/etc/skel** - the directory whose files are copied into the home directory of every new user.
- **UID** - the numeric user identifier the kernel uses to represent an account.
- **EUID** - the effective user identifier, which the kernel checks when deciding what a running process may do.
- **usermod -aG** - appends a user to supplementary groups without removing existing memberships.
- **chage** - displays and changes password aging and account expiry settings.
- **getent** - queries all configured name sources, such as local files, LDAP and SSSD, for entries like passwd and group.
- **Zombie process** - a finished process whose parent has not yet collected its exit status.
- **Niceness** - a value from -20 to 19 that influences scheduling priority; higher values mean lower priority.
- **SIGTERM** - signal 15, a polite request for a process to terminate that it can handle for a clean shutdown.
- **SIGKILL** - signal 9, which terminates a process immediately and cannot be caught or ignored.
- **SIGHUP** - signal 1, traditionally used to make a daemon reload its configuration.
- **nohup** - runs a command so that it keeps going after the terminal session closes.
- **crontab** - the table of scheduled recurring jobs with minute, hour, day of month, month and day of week fields.
- **anacron** - runs periodic jobs on machines that are not always powered on, catching up missed runs.
- **GPG signature** - a cryptographic signature that lets a package manager verify a package or repository came from a trusted key.
- **update-alternatives** - manages which installed implementation a generic command name points to.
- **systemd unit** - a configuration object, such as a service, timer, mount or target, that systemd manages.
- **systemctl mask** - links a unit to /dev/null so it cannot be started manually or by dependencies.
- **systemctl daemon-reload** - makes systemd re-read unit files after they have been changed.
- **systemd timer** - a unit that triggers another unit on a calendar or interval schedule.
- **systemd-analyze blame** - lists units by how long they took to start during boot.
- **runC** - the low-level OCI runtime that actually creates containers.
- **containerd** - a container runtime daemon that manages images and containers using runC.
- **Podman** - a daemonless container engine that can run containers without root and mirrors the Docker CLI.
- **Dockerfile** - a text recipe of instructions such as FROM, COPY, USER, ENTRYPOINT and CMD that builds an image in layers.
- **ENTRYPOINT** - the Dockerfile instruction that sets the fixed program a container runs.
- **CMD** - the Dockerfile instruction that supplies default arguments, which a run command can override.
- **Bridge network** - the default container network where containers share a private virtual switch and are reached through port mapping.
- **macvlan** - a container network driver that gives each container its own MAC address on the physical network.
- **Privileged container** - a container granted nearly all host capabilities and devices, which weakens isolation.
