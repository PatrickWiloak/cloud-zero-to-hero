# 04 - systemd Services, Logs, and Processes

## systemd basics

systemd is the init system and service manager. Everything that needs to run is a "unit."

### Unit types

| Type | Suffix | What it represents |
|---|---|---|
| Service | `.service` | A daemon |
| Socket | `.socket` | A socket activation point |
| Target | `.target` | A grouping of units (like "graphical.target") |
| Timer | `.timer` | A scheduled trigger |
| Mount | `.mount` | A mount point |
| Path | `.path` | A path watcher |
| Device | `.device` | A device |

### Unit file locations

| Path | Purpose |
|---|---|
| `/etc/systemd/system/` | Local admin overrides (highest precedence) |
| `/run/systemd/system/` | Runtime, ephemeral |
| `/usr/lib/systemd/system/` | Vendor-shipped (default location for installed packages) |

Drop-in overrides go in `/etc/systemd/system/<unit>.d/<override>.conf`.

---

## Manage services

```bash
systemctl status servicename
systemctl start servicename
systemctl stop servicename
systemctl restart servicename
systemctl reload servicename            # send SIGHUP, often re-reads config
systemctl reload-or-restart servicename

systemctl enable servicename            # start on boot
systemctl disable servicename
systemctl enable --now servicename      # enable AND start now
systemctl disable --now servicename     # disable AND stop now

systemctl is-active servicename         # for scripts
systemctl is-enabled servicename
systemctl mask servicename              # prevent it from being started even manually
systemctl unmask servicename
```

### List units

```bash
systemctl list-units                    # currently loaded
systemctl list-units --type=service     # services only
systemctl list-units --state=failed     # failed units
systemctl list-unit-files               # all installed unit files (loaded or not)
systemctl list-dependencies servicename # what depends on / requires what
```

---

## Editing units (drop-in overrides)

```bash
systemctl edit servicename              # creates /etc/systemd/system/servicename.service.d/override.conf
```

Type only the changed sections:

```ini
[Service]
Restart=always
RestartSec=5
```

Then:

```bash
systemctl daemon-reload
systemctl restart servicename
```

To edit the full unit (rarely needed):

```bash
systemctl edit --full servicename
```

---

## Sample service unit file

`/etc/systemd/system/myapp.service`:

```ini
[Unit]
Description=My App
After=network.target
Requires=postgresql.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/myapp --config /etc/myapp.conf
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Reload + enable:

```bash
systemctl daemon-reload
systemctl enable --now myapp
```

---

## Timers (cron replacement)

systemd timers replace cron jobs in modern Red Hat.

`/etc/systemd/system/backup.service`:

```ini
[Unit]
Description=Daily backup job

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

`/etc/systemd/system/backup.timer`:

```ini
[Unit]
Description=Run backup daily

[Timer]
OnCalendar=daily
Persistent=true            # run if missed (e.g., system off at scheduled time)

[Install]
WantedBy=timers.target
```

```bash
systemctl daemon-reload
systemctl enable --now backup.timer
systemctl list-timers
```

`OnCalendar` examples:

- `daily` (= `*-*-* 00:00:00`)
- `hourly`
- `Mon..Fri 09:00`
- `*-*-* 02:30:00` (every day 2:30am)
- `2026-01-01 00:00:00` (one-time)

---

## Crond (still supported)

If using cron instead of timers:

```bash
crontab -e                              # user crontab
crontab -l
crontab -r                              # remove

# Format: min hour day month dayofweek command
# Example: every day at 2:30 AM
30 2 * * * /usr/local/bin/backup.sh
```

Files:

- `/etc/crontab` - system-wide
- `/etc/cron.d/` - drop-in
- `/etc/cron.{hourly,daily,weekly,monthly}/` - run on schedule
- `/etc/cron.allow`, `/etc/cron.deny` - allowlist/denylist users

Restrict cron to specific users:

```bash
echo 'alice' >> /etc/cron.allow         # only alice can use cron
```

`/etc/cron.allow` takes precedence over `/etc/cron.deny`.

---

## Logs (journalctl + /var/log)

### journald

systemd's binary log database. Replaces / supplements `/var/log` files.

```bash
journalctl                              # all logs
journalctl -b                           # current boot
journalctl -b -1                        # previous boot
journalctl -b -1 -p err                 # priority error or worse, previous boot
journalctl -u nginx                     # specific service
journalctl -u nginx -f                  # follow live
journalctl --since "2 hours ago"
journalctl --since "2026-04-26 08:00" --until "2026-04-26 10:00"
journalctl _PID=1234                    # by PID
journalctl _UID=1001                    # by user
journalctl -n 50                        # last 50 lines
journalctl -k                           # kernel messages (dmesg-like)
journalctl --disk-usage
```

### Persistent journal

By default RHEL keeps logs only for the current boot. Make persistent:

```bash
mkdir -p /var/log/journal
systemctl restart systemd-journald
```

Or set `Storage=persistent` in `/etc/systemd/journald.conf` and restart.

### Traditional log files (`/var/log/`)

Still populated by rsyslog, which reads from journald.

| File | Contains |
|---|---|
| `/var/log/messages` | General system messages |
| `/var/log/secure` | Auth, sudo, ssh |
| `/var/log/cron` | Cron job activity |
| `/var/log/maillog` | Mail server |
| `/var/log/audit/audit.log` | SELinux + audit subsystem |
| `/var/log/dnf.log`, `/var/log/dnf.rpm.log` | Package manager |
| `/var/log/boot.log` | Boot messages |
| `/var/log/lastlog`, `wtmp`, `btmp` | Login history |

Useful tools:

```bash
last                          # show login history (from wtmp)
lastb                         # failed logins (from btmp)
who                           # current logins
w                             # who and what they're doing
```

---

## Process management

### View processes

```bash
ps aux                        # all processes, BSD format
ps -ef                        # all processes, System V format
ps -ef | grep ssh
pstree                        # tree view
top                           # interactive
htop                          # nicer top (install: dnf install -y htop)
```

### Find by name

```bash
pgrep ssh                     # PIDs matching ssh
pgrep -u alice                # PIDs by user
```

### Kill processes

```bash
kill 1234                     # SIGTERM (graceful)
kill -9 1234                  # SIGKILL (forced)
kill -HUP 1234                # SIGHUP (reload)
killall nginx                 # by name
pkill -u alice                # all alice's processes
```

### Process priority

```bash
nice -n 10 mycommand          # start with niceness 10 (lower priority)
renice -n 5 -p 1234           # change running process
```

Niceness range: -20 (highest) to 19 (lowest priority). Only root can lower nice value (raise priority).

### Foreground / background

```bash
command &                     # start in background
jobs                          # list backgrounded jobs in current shell
fg %1                         # bring job 1 to foreground
bg %1                         # send job 1 to background
nohup command &               # survives shell logout
disown %1                     # detach from current shell
```

### Resource use

```bash
free -h                       # memory
uptime                        # load averages
vmstat 1                      # virtual memory + I/O stats
iostat -xz 1                  # I/O per device
sar                           # historical perf data (requires sysstat)
```

---

## Common exam tasks

### Configure a service to start on boot and start it now

```bash
systemctl enable --now servicename
systemctl status servicename
```

### Override a unit to restart on failure

```bash
systemctl edit servicename
# Type:
# [Service]
# Restart=on-failure
# RestartSec=5
systemctl daemon-reload
systemctl restart servicename
```

### Schedule a script to run daily at 3am

```bash
# Option A: systemd timer
cat > /etc/systemd/system/myscript.service <<EOF
[Service]
Type=oneshot
ExecStart=/usr/local/bin/myscript.sh
EOF

cat > /etc/systemd/system/myscript.timer <<EOF
[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now myscript.timer
systemctl list-timers myscript

# Option B: cron
echo '0 3 * * * root /usr/local/bin/myscript.sh' > /etc/cron.d/myscript
```

### Diagnose why a service won't start

```bash
systemctl status servicename
journalctl -u servicename -n 100 --no-pager
journalctl -xe                  # latest with hints
```

### Show last 50 entries of nginx logs and follow live

```bash
journalctl -u nginx -n 50 -f
```

---

## Verification

After service / timer changes:

- `systemctl status servicename` shows `active (running)` and `enabled`
- `systemctl list-timers` shows the timer with next-run time
- `journalctl -u servicename -b` shows the service started cleanly
- After reboot, all of the above still hold

## Key terms

- **systemd unit** - a configuration file that describes a service, socket, mount, timer or other resource managed by systemd.
- **Target** - a systemd unit that groups other units and defines a system state, such as `multi-user.target`.
- **`systemctl enable`** - makes a unit start automatically at boot.
- **`journalctl`** - the command that reads logs collected by the systemd journal.
