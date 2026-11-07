---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 35 min
---

# Domain 3: Security (18%)

## Overview

This is defensive system hardening: controlling who can log in and what they can do, closing off network exposure, locking down files and services, encrypting data, and proving the system is in a known-good state. Every topic here is something an administrator does to protect a server, not to attack one. The objectives:

- **3.1** Authorization, authentication and accounting methods.
- **3.2** Firewalls.
- **3.3** Operating system hardening.
- **3.4** Account hardening.
- **3.5** Cryptographic concepts and technologies.
- **3.6** Compliance and audit procedures.

**[📖 CompTIA Linux+ XK0-006 Exam Objectives (PDF, version 5.0)](https://lecbyo.files.cmp.optimizely.com/download/90b9ac985c0e11f0b004a2a93c999a21)** - The official list of every topic and tool named in this domain

## 3.1 Authentication, authorization and accounting

**Authentication** proves who you are, **authorization** decides what you may do, and **accounting** records what you did. Linux assembles these from several pieces:

| Component | Role |
|---|---|
| **PAM** (Pluggable Authentication Modules) | A stack of modules, configured in `/etc/pam.d/`, that every login-style program consults. Adds password rules, lockouts, MFA and directory lookups without changing the program |
| **SSSD** (System Security Services Daemon) | Caches identities and credentials from remote sources (LDAP, Kerberos, Active Directory) and provides them to PAM and NSS. `realm` joins a host to a domain; Winbind is the Samba equivalent |
| **LDAP** | A directory protocol for central user and group data (port 389, 636 over TLS) |
| **Kerberos** | Ticket-based authentication; the user proves identity once and gets tickets for services. Requires time to be in sync |
| **Polkit** | Policy toolkit that decides which unprivileged programs may perform privileged actions, such as a desktop user mounting a disk |

### Logging as accounting

On a systemd host, the journal collects logs and is read with `journalctl` (`journalctl -u sshd --since "1 hour ago"`, `journalctl -p err -b` for errors this boot). `rsyslog` writes classic text logs under `/var/log` and can forward them to a central collector. `logrotate` rotates, compresses and expires logs so they do not fill the disk. Authentication events land in `/var/log/secure` (RHEL family) or `/var/log/auth.log` (Debian family).

For stronger accounting, the **Linux Audit** system records security-relevant system calls. `auditd` is the daemon, rules live in `/etc/audit/rules.d/*.rules` (compiled into `audit.rules`), and `auditctl` manages rules at runtime. A rule that watches a file for writes and attribute changes:

```bash
auditctl -w /etc/passwd -p wa -k identity
ausearch -k identity           # search events tagged with that key
```

**[📖 auditctl(8)](https://man7.org/linux/man-pages/man8/auditctl.8.html)** - Watch rules, permissions and keys
**[📖 journalctl(1)](https://man7.org/linux/man-pages/man1/journalctl.1.html)** - Filtering the systemd journal

## 3.2 Firewalls

A firewall decides which packets may reach or leave the host. Under the hood, Linux filters packets with the **Netfilter** kernel framework. You rarely write Netfilter rules directly; you use a front end.

| Front end | Notes |
|---|---|
| **firewalld** | Default on RHEL family. Zone-based, with a runtime and a permanent configuration |
| **ufw** (Uncomplicated Firewall) | Default front end on Ubuntu, simple allow/deny syntax |
| **nftables** | The modern packet filtering framework and `nft` command; replaces iptables |
| **iptables** | The older tool, still widely seen; `ipset` holds large sets of addresses to match |

### firewalld

Interfaces and sources are assigned to **zones**, each with its own trust level and allowed services. The key exam idea is **runtime versus permanent**. A change without `--permanent` takes effect immediately and is lost on reload or reboot. A change with `--permanent` is stored but not active until you reload.

```bash
firewall-cmd --get-active-zones
firewall-cmd --zone=public --add-service=https                 # runtime only
firewall-cmd --zone=public --add-service=https --permanent     # persistent, not yet active
firewall-cmd --reload                                          # apply permanent config
firewall-cmd --zone=public --add-port=8443/tcp --permanent
firewall-cmd --list-all
firewall-cmd --runtime-to-permanent                            # save the current runtime config
firewall-cmd --permanent --zone=public --add-rich-rule='rule family="ipv4" source address="198.51.100.0/24" service name="ssh" accept'
```

A **service** is a named set of ports (`https` is 443/tcp); using a service name is more readable than a bare port. **Rich rules** express conditions such as source address or logging.

**[📖 firewall-cmd manual](https://firewalld.org/documentation/man-pages/firewall-cmd.html)** - Zones, services, rich rules, runtime vs permanent

### ufw

```bash
ufw default deny incoming
ufw allow 22/tcp
ufw allow from 198.51.100.0/24 to any port 443 proto tcp
ufw enable
ufw status verbose
```

### Address translation and forwarding

**NAT** rewrites addresses as packets cross a router. **SNAT** (source NAT) rewrites the source, typically to share one public address among private hosts. **DNAT** (destination NAT) rewrites the destination, to forward a public port to an internal server. **PAT** also translates port numbers so many hosts can share one address. A Linux host only routes packets between interfaces if forwarding is on: `sysctl -w net.ipv4.ip_forward=1` (persist it in `/etc/sysctl.d/`).

A **stateful** firewall tracks connections, so reply traffic for an allowed outbound connection is accepted automatically. A **stateless** one judges every packet on its own, so you must write rules for both directions.

## 3.3 Operating system hardening

### Privilege escalation

Work as a normal user and elevate only when needed. `sudo` runs a single command with privileges, logs it, and is governed by `/etc/sudoers`. Always edit that file with `visudo`, which validates syntax before saving. A bad sudoers file can lock everyone out of root access. Files in `/etc/sudoers.d/` keep additions modular.

```text
# /etc/sudoers.d/webadmins  (edit with: visudo -f /etc/sudoers.d/webadmins)
%webadmins ALL=(root) /usr/bin/systemctl restart nginx, /usr/bin/systemctl reload nginx
deploy     ALL=(root) NOPASSWD: /usr/local/bin/deploy.sh
Defaults   use_pty
```

`NOPASSWD` removes the password prompt for those commands, which is convenient for automation and a risk if the command is broad. `NOEXEC` prevents a permitted program from spawning other programs, which blocks shell escapes from editors. Membership in the `wheel` group (RHEL family) or `sudo` group (Debian family) grants admin rights by default. `sudo -i` starts a root login shell; `su -` switches to root using root's password and environment.

**[📖 sudoers(5)](https://man7.org/linux/man-pages/man5/sudoers.5.html)** - Rule syntax, NOPASSWD, NOEXEC and Defaults

### File permissions

Permissions are three triplets (user, group, other) of read (4), write (2) and execute (1).

```bash
chmod 640 report.txt          # octal: user rw-, group r--, other ---
chmod u+x,g-w,o-rwx script.sh # symbolic
chown alice:developers report.txt
chgrp developers report.txt
umask 027                     # new files 640, new directories 750
```

**Special permissions:**

| Bit | On a file | On a directory |
|---|---|---|
| **setuid** (4000) | Runs with the file owner's privileges (`passwd` is the classic case) | No effect on most systems |
| **setgid** (2000) | Runs with the file group's privileges | New files inherit the directory's group |
| **sticky bit** (1000) | None | Only the file's owner can delete or rename it (as on `/tmp`) |

`chmod 2775 /srv/shared` sets setgid on a shared directory; `chmod +t` sets the sticky bit. Hardening includes finding and removing unnecessary setuid files: `find / -xdev -perm /4000 -type f`. The default **umask** subtracts permissions from newly created files.

**Access control lists** go beyond owner/group/other:

```bash
setfacl -m u:auditor:r-- /srv/data/report.txt
getfacl /srv/data/report.txt
setfacl -b /srv/data/report.txt     # remove all ACL entries
```

A `+` after the permission string in `ls -l` means an ACL exists.

**File attributes** are set with `chattr` and shown with `lsattr`. `chattr +i file` makes a file **immutable**: even root cannot change or delete it until the flag is removed. `chattr +a` makes it **append only**, ideal for logs.

**[📖 setfacl(1)](https://man7.org/linux/man-pages/man1/setfacl.1.html)** - ACL modification syntax
**[📖 chmod(1)](https://man7.org/linux/man-pages/man1/chmod.1.html)** - Octal and symbolic modes, special bits

### SELinux

**SELinux** is mandatory access control: even if standard permissions allow an action, policy can deny it. Every file, process and port has a **context** (user:role:type:level), and policy rules say which process types may touch which file types. Modes are **enforcing** (denies and logs), **permissive** (logs only, useful for diagnosing) and **disabled**.

```bash
getenforce                         # current mode
setenforce 0                       # permissive until reboot
ls -Z /var/www/html                # show file contexts
semanage fcontext -a -t httpd_sys_content_t "/srv/web(/.*)?"   # record the correct context
restorecon -Rv /srv/web            # apply recorded contexts
chcon -t httpd_sys_content_t file  # temporary change, lost on a relabel
getsebool -a | grep httpd
setsebool -P httpd_can_network_connect on   # -P persists across reboot
sealert -a /var/log/audit/audit.log
ausearch -m avc -ts recent | audit2allow    # draft a policy module from denials (review before using)
```

The correct habit when SELinux blocks something is to fix the context or flip the right boolean, not to disable SELinux. `chcon` is temporary; `semanage fcontext` plus `restorecon` is permanent.

### Secure remote access

The Secure Shell daemon (`sshd`) is configured in `/etc/ssh/sshd_config`. Hardening directives named in the objectives:

```text
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
X11Forwarding no
AllowUsers alice bob
AllowGroups sshusers
```

After editing, validate with `sshd -t` and apply with `systemctl reload sshd`. **Key-based authentication** is stronger than passwords because there is no secret to guess or phish: create a pair with `ssh-keygen -t ed25519`, then install the public key with `ssh-copy-id user@host`. The **SSH agent** holds decrypted keys in memory so you type the passphrase once. **SFTP** is file transfer over SSH, and **tunneling** forwards ports through an encrypted connection (`ssh -L 8080:db.internal:5432 bastion`). Lock down the key file: `~/.ssh` should be mode 700 and private keys 600.

**[📖 sshd_config(5)](https://man7.org/linux/man-pages/man5/sshd_config.5.html)** - Every server directive, including PermitRootLogin and AllowUsers

### Other hardening

- **Avoid insecure services.** Telnet, FTP and TFTP send credentials and data in cleartext. Replace them with SSH, SFTP or FTPS.
- **Disable unused filesystems and modules,** for example blacklist rarely needed filesystem drivers so they cannot be loaded.
- **Remove unnecessary SUID permissions** as shown above.
- **fail2ban** watches logs and temporarily bans addresses that fail authentication repeatedly.
- **chroot** confines a process to a subtree of the filesystem.
- **Secure boot** with UEFI verifies that the bootloader and kernel are signed before running them.

## 3.4 Account hardening

Passwords: enforce length and complexity, set expiration with `chage`, prevent reuse by keeping history, and check candidate passwords against **breach lists** so known-compromised passwords are refused. **MFA** adds a second factor and is applied to SSH and sudo through PAM modules. Lockout after repeated failures is handled by PAM (`pam_faillock` on modern systems; `pam_tally2` is the older module the objectives still name). Service accounts get `/sbin/nologin` as a shell so nobody can log in as them. A **restricted shell** such as `rbash` limits what a user may do (no `cd`, no changing `PATH`, no redirecting output). Above all, avoid running as root: log in as a user and use `sudo`.

## 3.5 Cryptography

### Data at rest

- **GPG** encrypts and signs files: `gpg --symmetric file` (passphrase) or `gpg --encrypt --recipient alice@example.com file`.
- **LUKS2** (Linux Unified Key Setup) encrypts a whole block device under the device-mapper layer. Its default key derivation is **Argon2**, designed to resist brute force.

```bash
cryptsetup luksFormat /dev/sdb1           # initialize (destroys existing data)
cryptsetup open /dev/sdb1 secure          # unlock as /dev/mapper/secure
mkfs.ext4 /dev/mapper/secure
mount /dev/mapper/secure /mnt/secure
umount /mnt/secure && cryptsetup close secure
```

**[📖 cryptsetup(8)](https://man7.org/linux/man-pages/man8/cryptsetup.8.html)** - LUKS format, open and close

### Data in transit

**TLS** protects most network services; use current versions (TLS 1.2 and 1.3) and remove weak algorithms and old protocol versions. **OpenSSL** is the common library and CLI (`openssl s_client -connect host:443` inspects a server's certificate), and LibreSSL is a fork. **WireGuard** is a modern, compact VPN built into the kernel.

### Hashing and certificates

A **hash** such as SHA-256 produces a fixed-size fingerprint used to verify integrity (`sha256sum file`). **HMAC** combines a hash with a secret key, so it also proves the sender knew the key. Weak algorithms (MD5, SHA-1, DES) should be removed from configurations.

Certificates tie a public key to an identity and are signed by a certificate authority. Servers should present certificates chained to a **trusted root**, from either a no-cost authority (using the ACME protocol, as Let's Encrypt does) or a commercial one. **Self-signed certificates** should be avoided on production services because clients cannot verify them and users learn to click through warnings.

## 3.6 Compliance and audit

### Detect and respond

Anti-malware scanners and **rootkit hunters** (`rkhunter`) look for known bad software. **Indicators of compromise (IOCs)** are artifacts such as unexpected accounts, odd listening ports, modified binaries or outbound connections to known bad hosts.

### Vulnerability management

A **CVE** is a public identifier for a specific vulnerability. **CVSS** scores its severity from 0 to 10. Scanners (port scanners, protocol analyzers and dedicated vulnerability scanners) find exposed services and misconfigurations. **Backporting** means a distribution applies a security fix to its older package version instead of upgrading to the new upstream release, so the version number alone does not tell you whether a CVE is fixed; check the vendor's advisory or the package changelog (`rpm -q --changelog`, `apt changelog`).

### Standards

**OpenSCAP** scans a system against a security profile and produces a report (`oscap xccdf eval`). The **CIS Benchmarks** are consensus hardening guides per operating system. Together they let you show an auditor that the system meets a defined baseline.

### Integrity and supply chain

**AIDE** (Advanced Intrusion Detection Environment) records file hashes and attributes in a database, then reports differences: `aide --init`, then `aide --check`. Package managers verify installed files against the package database (`rpm -V nginx`, `debsums`) and verify signatures on downloads. A secure **software supply chain** means installing only from trusted, signed sources and pinning versions.

### Secure data destruction and banners

Deleting a file does not erase the data. To destroy it: `shred -vzn 3 file` overwrites a file, `badblocks -w` writes patterns across a whole device, and `dd if=/dev/urandom of=/dev/sdX` overwrites with random data. On encrypted devices, **cryptographic destruction** (destroy the key, so the data is unreadable) is fast and effective. On SSDs, overwriting is unreliable because of wear leveling; prefer the drive's secure erase or cryptographic erase.

Login **banners** are legal notices shown before authentication: `/etc/issue` (local console), `/etc/issue.net` (network logins, referenced by the SSH `Banner` directive) and `/etc/motd` (message of the day after login).

## Common exam traps

- Edit sudoers with `visudo`, never a plain editor.
- A firewalld change without `--permanent` disappears at reload; with `--permanent` it is not live until `--reload`.
- `chcon` does not survive a relabel; `semanage fcontext` plus `restorecon` does.
- Disabling SELinux is almost never the right answer to a denial.
- `setsebool` needs `-P` to persist.
- `chmod -R 777` is never a fix.
- Immutable (`chattr +i`) blocks root too.
- A CVE can be fixed in a package whose version number looks old (backporting).

## Key terms

- **PAM** - Pluggable Authentication Modules, a stack of modules in /etc/pam.d that programs use to authenticate users and enforce account rules.
- **SSSD** - the System Security Services Daemon, which caches and provides identities and credentials from LDAP, Kerberos and Active Directory.
- **Kerberos** - a ticket-based authentication protocol that depends on synchronized clocks.
- **Polkit** - a policy framework that decides which unprivileged programs may perform privileged actions.
- **journalctl** - reads and filters logs collected by the systemd journal.
- **logrotate** - rotates, compresses and expires log files so they do not fill the disk.
- **auditd** - the Linux Audit daemon, which records security-relevant events according to audit rules.
- **Netfilter** - the Linux kernel framework that performs packet filtering and address translation.
- **nftables** - the modern Linux packet filtering framework that replaces iptables.
- **firewalld** - a zone-based firewall manager with separate runtime and permanent configurations, controlled with firewall-cmd.
- **firewall-cmd --permanent** - stores a firewalld change in the permanent configuration without applying it until a reload.
- **Rich rule** - a firewalld rule that matches on conditions such as source address, service and logging.
- **ufw** - the Uncomplicated Firewall, a simple front end for Netfilter used on Ubuntu.
- **SNAT** - source network address translation, which rewrites the source address of outgoing packets.
- **DNAT** - destination network address translation, which rewrites the destination of incoming packets to forward a port to another host.
- **ip_forward** - the net.ipv4.ip_forward kernel setting that must be 1 for the host to route packets between interfaces.
- **Stateful firewall** - a firewall that tracks connections so reply traffic for allowed connections is accepted automatically.
- **visudo** - edits the sudoers file safely by checking its syntax before saving.
- **NOPASSWD** - a sudoers tag that lets a user run the listed commands without entering a password.
- **wheel group** - the group whose members receive sudo rights by default on RHEL-family systems.
- **setuid** - a permission bit that makes an executable run with the privileges of its owner.
- **setgid** - a permission bit that makes an executable run with its group, or makes new files in a directory inherit the directory's group.
- **Sticky bit** - a directory permission bit that lets only a file's owner delete or rename it, as on /tmp.
- **umask** - the mask that removes permissions from newly created files and directories.
- **ACL** - an access control list that grants permissions to specific users or groups beyond owner, group and other.
- **chattr +i** - sets the immutable attribute so a file cannot be changed or deleted, even by root.
- **SELinux** - mandatory access control that restricts processes by security context regardless of ordinary file permissions.
- **Permissive mode** - an SELinux mode that logs policy violations without blocking them.
- **restorecon** - resets file security contexts to the values defined in SELinux policy.
- **semanage fcontext** - records a persistent SELinux file context rule.
- **SELinux boolean** - a policy switch such as httpd_can_network_connect that changes allowed behavior, set persistently with setsebool -P.
- **fail2ban** - watches logs and temporarily blocks addresses with repeated authentication failures.
- **PermitRootLogin** - the sshd_config directive that controls whether root may log in over SSH.
- **AllowUsers** - the sshd_config directive that restricts SSH logins to the listed users.
- **SSH agent** - a program that holds decrypted private keys in memory so the passphrase is typed once.
- **rbash** - a restricted bash shell that blocks actions such as changing directory or modifying PATH.
- **pam_tally2** - an older PAM module that counts failed logins and locks accounts after too many.
- **LUKS2** - the Linux Unified Key Setup format for encrypting block devices.
- **Argon2** - a password-based key derivation function designed to resist brute-force attacks, used by LUKS2.
- **HMAC** - a hashed message authentication code that combines a hash with a secret key to prove integrity and origin.
- **WireGuard** - a modern VPN protocol implemented in the Linux kernel.
- **CVE** - Common Vulnerabilities and Exposures, a public identifier for a specific known vulnerability.
- **CVSS** - the Common Vulnerability Scoring System, which rates a vulnerability's severity from 0 to 10.
- **Backporting** - applying a security fix to an older package version instead of upgrading to a new upstream release.
- **OpenSCAP** - tooling that scans a system against a security profile and reports compliance.
- **CIS Benchmarks** - consensus hardening guides published by the Center for Internet Security for specific systems.
- **AIDE** - Advanced Intrusion Detection Environment, which stores file hashes and reports later changes.
- **shred** - overwrites a file repeatedly so its contents are hard to recover.
- **Cryptographic destruction** - making data unrecoverable by destroying the encryption key.
- **/etc/issue** - the file whose contents are shown as a login banner before authentication on the local console.
- **/etc/motd** - the message of the day shown to users after they log in.
