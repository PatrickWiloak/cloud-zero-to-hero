# 02 - Storage and Filesystems

## Block devices

```bash
lsblk                  # tree view of disks, partitions, mounts
fdisk -l               # detailed partition table
blkid                  # UUID + filesystem type
```

Common naming: `/dev/sda`, `/dev/nvme0n1`, `/dev/vdb` (virtio).

---

## Partitions

### MBR (legacy) vs GPT

- **MBR** - max 4 primary partitions, 2 TB limit. Use for legacy BIOS systems.
- **GPT** - many partitions, no size limit. Default on modern UEFI systems.

### Create a partition with `fdisk`

```bash
fdisk /dev/sdb
# n  - new partition
# p  - primary (or e for extended)
# 1  - partition number
# (Enter)  - default first sector
# +5G  - size
# t  - change type
# 8e - Linux LVM (or 82 for swap, 83 for filesystem)
# w  - write
```

After creating partitions:

```bash
partprobe /dev/sdb     # rescan partition table
```

### Or with `parted` (scriptable)

```bash
parted /dev/sdb mklabel gpt
parted /dev/sdb mkpart primary xfs 0% 5GB
```

---

## Filesystems

| Filesystem | Best for |
|---|---|
| **xfs** | Default RHEL 9 root and data; can grow but **cannot shrink** |
| **ext4** | Mature, can shrink; good for older workloads |
| **vfat** | EFI partition / cross-platform USB |
| **swap** | Swap space (not a real filesystem) |
| **iso9660** | DVD / ISO images |

### Create a filesystem

```bash
mkfs.xfs /dev/sdb1
mkfs.ext4 -L mylabel /dev/sdb2
mkswap /dev/sdb3
```

---

## Mounting

### Manual mount

```bash
mkdir -p /mnt/data
mount /dev/sdb1 /mnt/data
```

### Persistent mount (`/etc/fstab`)

Format:

```
<device>    <mount_point>    <fstype>    <options>    <dump>    <fsck>
```

Example:

```
UUID=abc-123    /mnt/data    xfs    defaults    0    0
/dev/vg_data/lv_data    /var/lib/postgres    ext4    defaults,noatime    0    2
LABEL=swap1    none    swap    defaults    0    0
```

**Always use UUID** (or LABEL) instead of device name (`/dev/sdX1`) - device names can change between reboots.

Get UUID:

```bash
blkid /dev/sdb1
# /dev/sdb1: UUID="..." BLOCK_SIZE="512" TYPE="xfs" PARTUUID="..."
```

After editing fstab, **always test before reboot**:

```bash
systemctl daemon-reload   # if any systemd-managed mounts
mount -a                  # mounts everything in fstab not already mounted
```

If `mount -a` errors, fix fstab before rebooting - otherwise the system may fail to boot.

---

## LVM (Logical Volume Manager)

LVM gives you flexible storage that can grow / shrink without re-partitioning.

### Layers

```
Physical disk(s)  →  Physical Volume (PV)  →  Volume Group (VG)  →  Logical Volume (LV)  →  Filesystem
```

### Create LVM stack

```bash
# Mark partitions as LVM (type 8e via fdisk)
pvcreate /dev/sdb1 /dev/sdc1
pvs                                       # list PVs

vgcreate vg_data /dev/sdb1 /dev/sdc1
vgs                                       # list VGs

lvcreate -L 5G -n lv_data vg_data         # 5 GB logical volume
lvcreate -l 100%FREE -n lv_logs vg_data   # use all remaining space
lvs                                       # list LVs

mkfs.xfs /dev/vg_data/lv_data
mkdir -p /mnt/data
mount /dev/vg_data/lv_data /mnt/data
```

Then add to fstab using UUID.

### Extend an LV (online, no downtime)

```bash
# Add space to VG first if needed
vgextend vg_data /dev/sdd1

# Extend LV
lvextend -L +2G /dev/vg_data/lv_data

# Or grow to use all free VG space
lvextend -l +100%FREE /dev/vg_data/lv_data

# Resize the filesystem
xfs_growfs /mnt/data         # XFS (online)
resize2fs /dev/vg_data/lv_data  # ext4 (online)
```

### Reduce an LV (ext4 only - XFS cannot shrink)

```bash
umount /mnt/data
e2fsck -f /dev/vg_data/lv_data
resize2fs /dev/vg_data/lv_data 4G
lvreduce -L 4G /dev/vg_data/lv_data
mount /mnt/data
```

---

## Stratis (RHEL 9)

Stratis is a higher-level storage manager built on LVM and XFS. The exam touches it lightly.

```bash
dnf install -y stratis-cli stratisd
systemctl enable --now stratisd

stratis pool create mypool /dev/sdb /dev/sdc
stratis filesystem create mypool myfs

# Mount path:
mount /dev/stratis/mypool/myfs /mnt/strat
```

Persistent mount uses `/dev/stratis/<pool>/<fs>` and the `xfs` filesystem with `x-systemd.requires=stratisd.service` option.

---

## Swap

### Create a swap partition

```bash
mkswap /dev/sdb3
swapon /dev/sdb3
swapon --show
```

Add to fstab:

```
UUID=...  none  swap  defaults  0  0
```

### Create a swap file

```bash
dd if=/dev/zero of=/swapfile bs=1M count=2048
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile  none  swap  defaults  0  0' >> /etc/fstab
```

---

## NFS (network filesystem)

### Server side (not always asked)

```bash
dnf install -y nfs-utils
echo '/srv/share  192.168.1.0/24(rw,sync,no_root_squash)' >> /etc/exports
systemctl enable --now nfs-server
exportfs -rav
firewall-cmd --permanent --add-service=nfs --add-service=mountd --add-service=rpc-bind
firewall-cmd --reload
```

### Client side (more often tested)

```bash
dnf install -y nfs-utils
mkdir -p /mnt/nfs
mount -t nfs server:/srv/share /mnt/nfs
```

Persistent in `/etc/fstab`:

```
server:/srv/share   /mnt/nfs   nfs   defaults,_netdev   0   0
```

`_netdev` ensures the mount waits for network availability at boot.

### Automounting NFS

`autofs` mounts on access and unmounts on idle.

```bash
dnf install -y autofs
systemctl enable --now autofs
```

`/etc/auth.master.d/share.autofs`:

```
/-  /etc/auto.share
```

`/etc/auto.share`:

```
/mnt/share  -fstype=nfs,rw  server:/srv/share
```

---

## ACLs (Access Control Lists)

Standard Unix permissions limit you to user/group/other. ACLs allow per-user / per-group rules.

```bash
# Set ACL
setfacl -m u:alice:rw- /path/file
setfacl -m g:devs:rwx /path/dir

# View ACLs
getfacl /path/file

# Default ACL on dir (applied to new children)
setfacl -d -m u:alice:rw- /path/dir

# Remove
setfacl -x u:alice /path/file

# Remove all ACLs
setfacl -b /path/file
```

Files with ACLs show a `+` in `ls -l`:

```
-rw-rw-r--+ 1 root root  ...  file
```

---

## Common tasks and patterns

### Add a 5 GB partition, format ext4, mount at /var/log/app, persistent

```bash
# 1. Create partition
fdisk /dev/sdb     # n, default size +5G, type 83, w
partprobe

# 2. Create filesystem
mkfs.ext4 -L applogs /dev/sdb1

# 3. Get UUID
blkid /dev/sdb1

# 4. Add to /etc/fstab
echo 'UUID=<uuid>  /var/log/app  ext4  defaults  0  2' >> /etc/fstab

# 5. Test
mkdir -p /var/log/app
mount -a
df -h | grep applogs

# 6. Reboot to verify
reboot
```

### Add a 5 GB LV in vg_data, mount at /opt/myapp

```bash
lvcreate -L 5G -n lv_myapp vg_data
mkfs.xfs /dev/vg_data/lv_myapp
mkdir -p /opt/myapp
echo '/dev/vg_data/lv_myapp  /opt/myapp  xfs  defaults  0  2' >> /etc/fstab
mount -a
df -h | grep lv_myapp
```

### Extend an existing logical volume to use all remaining space in VG

```bash
lvextend -l +100%FREE /dev/vg_data/lv_data
xfs_growfs /mnt/data
df -h
```

### Configure a swap file of 1 GB

```bash
dd if=/dev/zero of=/swapfile bs=1M count=1024
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile  none  swap  defaults  0  0' >> /etc/fstab
swapon --show
```

---

## Verification checklist

- `lsblk` shows the new device with the right mount point
- `df -h` shows the filesystem
- `mount` shows mount options as expected
- `cat /proc/swaps` for swap
- After reboot, all of the above still hold

## Key terms

- **Physical volume (PV)** - a disk or partition initialised for use by LVM.
- **Volume group (VG)** - a pool of storage made from one or more physical volumes.
- **Logical volume (LV)** - a flexible block device carved out of a volume group and used like a partition.
- **`/etc/fstab`** - the file that lists filesystems to mount at boot.
- **UUID** - a unique identifier for a filesystem, preferred over device names in fstab because it does not change.
- **Swap** - disk space the kernel uses as overflow when physical memory is full.
