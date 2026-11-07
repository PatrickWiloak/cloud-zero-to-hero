# 03 - Users, Groups, Sudo, Permissions

## User accounts

### Files

- `/etc/passwd` - user info (one line per user)
- `/etc/shadow` - hashed passwords + aging
- `/etc/group` - group membership
- `/etc/gshadow` - group passwords (rare)
- `/etc/login.defs` - default UID range, password aging defaults
- `/etc/skel/` - template home dir contents copied for new users

### Format of `/etc/passwd`

```
username:x:UID:GID:GECOS:home:shell
alice:x:1001:1001:Alice Smith:/home/alice:/bin/bash
```

### Create / modify users

```bash
useradd -m -s /bin/bash alice         # -m creates home dir
passwd alice                           # set password
useradd -u 1500 -G wheel -c 'Bob Jones' bob

usermod -aG developers alice           # add to group (-a APPEND)
usermod -L alice                       # lock account
usermod -U alice                       # unlock
usermod -s /sbin/nologin alice         # disable login

userdel alice                          # delete (keeps home)
userdel -r alice                       # delete WITH home + mail spool
```

### `useradd` defaults

```bash
useradd -D                             # show defaults (from /etc/default/useradd)
useradd -D -s /bin/zsh                 # set default shell for future users
```

---

## Password aging (`chage`)

```bash
chage -l alice                         # list aging info
chage -M 90 alice                      # max days before required change
chage -m 7  alice                      # min days between changes
chage -W 14 alice                      # warning days before expiry
chage -I 30 alice                      # inactivity days after expiry before lock
chage -E 2026-12-31 alice              # account expiration
chage -d 0 alice                       # force password change at next login
```

Defaults are in `/etc/login.defs`:

```
PASS_MAX_DAYS   90
PASS_MIN_DAYS   7
PASS_WARN_AGE   14
```

---

## Groups

```bash
groupadd developers
groupadd -g 5000 ops                   # specific GID
groupmod -n devs developers            # rename
groupdel ops

# Group membership
usermod -aG developers alice           # ALWAYS use -aG (append), not -G alone
groups alice                           # show alice's groups
id alice                               # uid, gid, groups
```

### Primary vs secondary group

- **Primary group** is set with `usermod -g group user` and is the GID of new files the user creates.
- **Secondary groups** are additional memberships set with `-aG`.

---

## Sudo

`sudo` config is in `/etc/sudoers` (edit with `visudo`) and drop-in files in `/etc/sudoers.d/`.

### Common patterns

```
# Allow user full sudo with password
alice  ALL=(ALL)  ALL

# Allow group full sudo with password (the wheel group is conventional)
%wheel  ALL=(ALL)  ALL

# Allow group sudo without password
%developers  ALL=(ALL)  NOPASSWD: ALL

# Allow user only specific commands
bob  ALL=(ALL)  /usr/bin/systemctl restart httpd, /usr/bin/journalctl

# Run as a specific user
mary  ALL=(postgres)  NOPASSWD: /usr/bin/psql
```

**Recommended:** create separate files in `/etc/sudoers.d/`:

```bash
echo 'alice  ALL=(ALL)  NOPASSWD: ALL' > /etc/sudoers.d/alice
chmod 0440 /etc/sudoers.d/alice
visudo -cf /etc/sudoers.d/alice        # validate
```

The `wheel` group is the conventional sudo group on Red Hat. Add users with `usermod -aG wheel alice`.

---

## File permissions

### Symbolic and numeric

```
rwxrwxrwx  =  user/group/other
421421421
```

| Permission | Octal | Symbolic |
|---|---|---|
| read | 4 | `r` |
| write | 2 | `w` |
| execute | 1 | `x` |

Common modes:

| Mode | Meaning |
|---|---|
| 644 | rw-r--r-- (typical file) |
| 755 | rwxr-xr-x (typical directory or executable) |
| 600 | rw------- (private file, e.g., SSH key) |
| 700 | rwx------ (private dir) |
| 750 | rwxr-x--- (group-readable dir) |
| 777 | wide open (avoid) |

### Set permissions

```bash
chmod 644 file
chmod u+x script.sh                    # add execute for owner
chmod g-w file                         # remove write for group
chmod -R 755 /var/www/html             # recursive

chown alice file                       # change owner
chown alice:devs file                  # owner + group
chgrp devs file                        # group only
```

### Special bits

- **SUID** (4): execute as file owner. `chmod u+s` or `chmod 4755`. Visible as `s` in user-execute. Example: `/usr/bin/passwd`.
- **SGID** (2): execute as group, or new files in directory inherit dir's group. `chmod g+s` or `chmod 2755`.
- **Sticky** (1): in a dir, only the file owner can delete files. `chmod +t` or `chmod 1755`. Example: `/tmp`.

---

## Directory inheritance

When a process creates a new file:

```
new_file_perms = (default_perms - umask)
```

Default umask on RHEL: `0022` (so directories are 755, files 644).

```bash
umask                                 # show
umask 0027                            # restrict group + other
```

To make group-collaborative directories:

```bash
mkdir /shared
chgrp devs /shared
chmod 2775 /shared                    # SGID + group write
# Now any file/dir created in /shared inherits group "devs"
```

---

## ACLs (Access Control Lists)

Used when standard u/g/o is too restrictive (e.g., one user needs read on a file owned by another, neither share a group).

```bash
setfacl -m u:bob:r-- /path/file       # give bob read
setfacl -m g:devs:rwx /path/dir       # give devs group rwx
getfacl /path/file                    # view

setfacl -d -m u:bob:rw- /path/dir     # default ACL (inherited by new files)
setfacl -x u:bob /path/file           # remove specific ACL
setfacl -b /path/file                 # remove all ACLs
```

Files with ACLs show a `+` in `ls -l`:

```
-rw-rw-r--+ 1 root root  ...  file
```

---

## Common exam tasks

### Create user with specific UID and home dir, set password to expire in 60 days

```bash
useradd -u 1500 -m -s /bin/bash newuser
passwd newuser
chage -M 60 newuser
```

### Add user to wheel group (sudo)

```bash
usermod -aG wheel alice
groups alice                          # verify
```

### Allow a user to run only specific commands as root, no password

```bash
echo 'alice  ALL=(ALL)  NOPASSWD: /usr/bin/systemctl restart nginx' > /etc/sudoers.d/alice
chmod 0440 /etc/sudoers.d/alice
visudo -cf /etc/sudoers.d/alice
```

### Lock an account

```bash
usermod -L alice
# Verify in /etc/shadow - password field starts with !
```

### Force user to change password at next login

```bash
chage -d 0 alice
```

### Group-collaborative directory

```bash
mkdir /shared/team
chgrp team /shared/team
chmod 2770 /shared/team               # SGID + group rwx, no other
# Now any file created here inherits group "team"
```

### Create a sudo group with passwordless full access

```bash
groupadd ops
echo '%ops  ALL=(ALL)  NOPASSWD: ALL' > /etc/sudoers.d/ops
chmod 0440 /etc/sudoers.d/ops
visudo -cf /etc/sudoers.d/ops
usermod -aG ops alice
```

---

## Verification

After permission / ACL / sudo changes:

- `id <user>` shows expected uid/gid/groups
- `ls -la /path` shows expected permissions and ACL `+`
- `getfacl /path` shows expected ACLs
- `sudo -l -U alice` shows what alice is allowed
- `su - alice` then try the operation - it should succeed (or fail) as expected

## Key terms

- **SUID** - a permission bit that makes an executable run with the file owner's privileges.
- **SGID** - a permission bit that makes new files in a directory inherit its group, or runs an executable with the file's group.
- **Sticky bit** - a directory permission that lets only a file's owner or the directory owner delete or rename files inside.
- **umask** - the mask that removes permission bits from newly created files and directories.
- **Access control list (ACL)** - an extended permission entry that grants access to specific users or groups beyond owner, group and other.
