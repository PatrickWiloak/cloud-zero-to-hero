# 05 - Networking, Firewalld, SSH, SELinux

## Networking with NetworkManager (`nmcli`)

RHEL 9 uses NetworkManager. `nmcli` is the canonical CLI.

### Inspect

```bash
nmcli                            # connections + devices
nmcli device status              # device states
nmcli connection show            # connections
nmcli connection show CONN_NAME  # detailed config

ip a                             # show interface addresses (kernel view)
ip r                             # show routes
ip link                          # show interface link state
```

### Configure

```bash
# Static IP, gateway, DNS
nmcli connection modify CONN_NAME \
    ipv4.method manual \
    ipv4.addresses 192.0.2.10/24 \
    ipv4.gateway 192.0.2.1 \
    ipv4.dns "8.8.8.8 1.1.1.1" \
    ipv4.dns-search example.com

# DHCP
nmcli connection modify CONN_NAME ipv4.method auto

# Apply
nmcli connection up CONN_NAME
```

### Create a new connection

```bash
nmcli connection add type ethernet con-name eth1 ifname eth1 \
    ipv4.method manual \
    ipv4.addresses 192.0.2.20/24 \
    ipv4.gateway 192.0.2.1 \
    ipv4.dns 8.8.8.8

nmcli connection up eth1
```

### Configuration files

NetworkManager keyfiles: `/etc/NetworkManager/system-connections/<name>.nmconnection`

(The older `/etc/sysconfig/network-scripts/ifcfg-*` files still work but keyfiles are preferred in RHEL 9.)

### Hostname

```bash
hostnamectl                                          # show
hostnamectl set-hostname server1.example.com         # set
```

Edit `/etc/hosts` for static name resolution:

```
192.0.2.10  server1.example.com  server1
```

---

## Bonds and teams

Network teaming combines multiple NICs for HA / bandwidth.

### Bonding

```bash
nmcli connection add type bond con-name bond0 ifname bond0 mode active-backup
nmcli connection add type ethernet con-name bond0-eth0 ifname eth0 master bond0
nmcli connection add type ethernet con-name bond0-eth1 ifname eth1 master bond0
nmcli connection modify bond0 ipv4.addresses 192.0.2.50/24 ipv4.gateway 192.0.2.1 ipv4.method manual
nmcli connection up bond0
```

Modes: `active-backup`, `balance-rr`, `802.3ad` (LACP), etc.

---

## Time and DNS

```bash
timedatectl                              # state
timedatectl set-timezone UTC
timedatectl set-ntp true                 # enable chronyd

cat /etc/chrony.conf                     # NTP config
chronyc sources -v                       # peer status
chronyc tracking                         # current offset
```

DNS resolver: `/etc/resolv.conf` (managed by NetworkManager). Check with `dig +short example.com` or `getent hosts example.com`.

---

## Firewalld

firewalld is the default firewall front-end on RHEL.

### Concepts

- **Zones** group rules. Examples: `public`, `internal`, `trusted`, `dmz`, `home`, `work`, `block`, `drop`.
- Each network connection is bound to a zone.
- Each zone has services and ports it allows.

### Inspect

```bash
firewall-cmd --state                            # is it running
firewall-cmd --get-default-zone
firewall-cmd --get-active-zones
firewall-cmd --list-all                         # default zone, all settings
firewall-cmd --zone=public --list-all
firewall-cmd --get-services                     # list known service names
```

### Add rules (persistent)

```bash
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --add-port=8080/tcp

firewall-cmd --permanent --remove-service=ssh   # careful

firewall-cmd --reload                            # apply persistent
```

### Move connection to a different zone

```bash
firewall-cmd --permanent --zone=internal --change-interface=eth1
firewall-cmd --reload
```

### Rich rules

For more complex logic:

```bash
# Allow SSH only from specific subnet
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.0/24" service name="ssh" accept'

# Block specific source
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="203.0.113.5" reject'

firewall-cmd --reload
```

### Common services

| Service | Port |
|---|---|
| ssh | 22/tcp |
| http | 80/tcp |
| https | 443/tcp |
| ftp | 21/tcp |
| smtp | 25/tcp |
| dns | 53/tcp+udp |
| nfs | 2049/tcp |
| samba | several |

---

## SSH

### Server config: `/etc/ssh/sshd_config`

Common changes:

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers alice bob
Port 22
```

After edits:

```bash
systemctl restart sshd
```

### Key-based authentication

On client:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server
```

`ssh-copy-id` appends the public key to `~/.ssh/authorized_keys` on the server with correct permissions.

Manual equivalent:

```bash
# On server, as the user
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-ed25519 AAAA... user@laptop" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
restorecon -R ~/.ssh                    # restore SELinux contexts
```

### Common issues

- **Permission denied (publickey)** with correct key:
  - Check `~/.ssh` is `700`, `authorized_keys` is `600`
  - SELinux: `restorecon -R ~/.ssh`
  - Wrong user in `AllowUsers`
- **Root denied** but you have the key:
  - `PermitRootLogin no` in `sshd_config`
  - Use a regular user + sudo

---

## SELinux

SELinux is a mandatory access control system. On RHEL, it is **enforcing by default** and this matters for the exam.

### Three modes

- **Enforcing** - SELinux enforces policy. Default.
- **Permissive** - SELinux logs violations but allows them. Useful for diagnosis.
- **Disabled** - SELinux off entirely. Avoid; never the right answer on the exam.

```bash
getenforce                    # current mode
setenforce 0                  # runtime → permissive
setenforce 1                  # runtime → enforcing
```

Persistent: edit `/etc/selinux/config`, set `SELINUX=enforcing` (or `permissive`). Reboot.

### Contexts

Every file/process has an SELinux context: `user:role:type:level`. The **type** (often ending in `_t`) is what you usually deal with.

```bash
ls -lZ /var/www/html
# system_u:object_r:httpd_sys_content_t:s0  index.html

ps -eZ | grep httpd
# system_u:system_r:httpd_t:s0  ...

id -Z                                     # your context
```

### Booleans (toggles)

Some policies have on/off knobs.

```bash
getsebool -a | grep httpd                 # list httpd booleans
setsebool -P httpd_can_network_connect on  # persistent (-P)
```

Common booleans:

- `httpd_can_network_connect` - let Apache connect outbound (e.g., to a backend DB)
- `httpd_enable_homedirs` - serve content from user home dirs
- `samba_enable_home_dirs`
- `nfs_export_all_rw`

### File contexts

When you put files in non-default locations, SELinux often blocks them. Two ways to fix:

#### One-shot

```bash
chcon -t httpd_sys_content_t /custom/web/index.html
```

But `chcon` doesn't survive `restorecon` or filesystem relabel.

#### Persistent (preferred)

```bash
semanage fcontext -a -t httpd_sys_content_t '/custom/web(/.*)?'
restorecon -Rv /custom/web
```

Now the rule is in policy and applies on relabel.

### Diagnose denials

```bash
ausearch -m avc -ts recent
# Or:
sealert -a /var/log/audit/audit.log

# audit2allow shows what policy you'd need to write
ausearch -m avc -ts recent | audit2allow -m mypolicy
```

### Common patterns

#### "Apache serves files from `/srv/www`"

```bash
mkdir -p /srv/www
echo 'hello' > /srv/www/index.html
semanage fcontext -a -t httpd_sys_content_t '/srv/www(/.*)?'
restorecon -Rv /srv/www
```

Then point Apache's `DocumentRoot` to `/srv/www`.

#### "Apache connects to DB on different host"

```bash
setsebool -P httpd_can_network_connect on
```

#### "Service runs on a non-standard port"

```bash
semanage port -a -t http_port_t -p tcp 8080
```

---

## Common networking exam tasks

### Set static IP, gateway, DNS

```bash
nmcli connection modify "System eth0" \
    ipv4.method manual \
    ipv4.addresses 192.0.2.10/24 \
    ipv4.gateway 192.0.2.1 \
    ipv4.dns 8.8.8.8

nmcli connection up "System eth0"
```

### Set hostname

```bash
hostnamectl set-hostname server1.example.com
```

### Add a host entry

```bash
echo '192.0.2.20 db1.example.com db1' >> /etc/hosts
```

### Open HTTP/HTTPS in firewalld

```bash
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

### Allow SSH only from corporate LAN

```bash
firewall-cmd --permanent --remove-service=ssh
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" service name="ssh" accept'
firewall-cmd --reload
```

### Configure SSH key-only login, no root, no passwords

`/etc/ssh/sshd_config`:

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

```bash
systemctl restart sshd
```

### Apache serves from non-default path with SELinux

```bash
semanage fcontext -a -t httpd_sys_content_t '/srv/www(/.*)?'
restorecon -Rv /srv/www
```

---

## Verification

After networking / firewall / SELinux changes:

- `ip a` shows the right IP
- `ping -c 3 8.8.8.8` works
- `firewall-cmd --list-all` shows expected services / ports
- `getenforce` shows expected mode (usually `Enforcing`)
- `getsebool -a | grep <boolean>` shows expected `on`/`off`
- After reboot, all of the above still hold

## Key terms

- **SELinux context** - the user, role, type and level label on a file or process that SELinux uses to decide access.
- **SELinux boolean** - a switch, set with `setsebool`, that turns a policy behaviour on or off at runtime.
- **`restorecon`** - resets a file's SELinux context to the default defined in policy.
- **firewalld zone** - a named set of firewall rules applied to a network interface or source according to its trust level.
- **`nmcli`** - the command-line tool for configuring NetworkManager connections.
