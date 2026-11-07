---
last-updated: 2026-11-07
difficulty: intermediate
---

# CompTIA Linux+ (XK0-006) - Practice Questions

20 original scenario questions for Linux+ prep. The count per domain follows the exam weights: System Management 5, Services and User Management 4, Security 4, Automation 3, Troubleshooting 4.

> **Cert page:** [exams/comptia/linux-plus/](../../exams/comptia/linux-plus/)

---

### Question 1
**Scenario:** An administrator extended a logical volume by 20 GiB with lvextend. lvs shows the new size, but df shows the mounted XFS filesystem is unchanged.

A. Unmount the volume and run fsck, because df will read the new size once the filesystem is checked
B. Run xfs_growfs against the mount point to expand the filesystem into the new space
C. Run resize2fs against the logical volume, because that tool expands any filesystem type
D. Run pvresize on the physical volume so LVM reports the larger size to df

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Extending the logical volume does not extend the filesystem. XFS is grown online with xfs_growfs, which takes the mount point. resize2fs works on ext2/3/4, not XFS. pvresize is for physical volumes, and fsck does not change a filesystem's size.
</details>

---

### Question 2
**Scenario:** A server drops to an emergency shell at boot after a new line was added to /etc/fstab for a data disk that is sometimes not attached. The administrator wants the server to boot normally when the disk is absent.

A. Change the last field to 2 so the disk is checked after the root filesystem
B. Add noexec to the options so the missing disk cannot block startup
C. Replace the device name with a UUID and keep the options unchanged
D. Add the nofail option to that line

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** nofail tells the boot process not to treat a missing device as a failure. A UUID prevents device renaming problems but still fails if the disk is absent. The fsck pass number controls check order, and noexec only blocks program execution.
</details>

---

### Question 3
**Scenario:** A host needs to load a driver module along with the modules it depends on, and unload it again later.

A. modprobe to load and modprobe -r to unload
B. depmod to load and lsmod to unload
C. dmesg to load and modinfo to unload
D. insmod to load and rmmod to unload, because they handle dependencies automatically

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** modprobe reads the dependency data produced by depmod and loads prerequisites; modprobe -r removes the module and unused dependencies. insmod loads a single file with no dependency handling. lsmod, dmesg and modinfo only report.
</details>

---

### Question 4
**Scenario:** A Netplan change on a remote Ubuntu server could lock the administrator out if the new address is wrong. Which command applies it with an automatic rollback?

A. netplan generate
B. netplan apply
C. netplan try
D. netplan status

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** netplan try applies the configuration and reverts after a timeout unless the change is confirmed. netplan apply is permanent immediately, status only shows state, and generate only renders backend configuration.
</details>

---

### Question 5
**Scenario:** The backup disk is failing and has unreadable sectors. Which tool is best for copying as much data as possible to a new disk?

A. cpio, which repairs damaged sectors while copying
B. dd with default options, which stops at the first read error
C. ddrescue, which continues past errors and logs the bad areas
D. rsync -a, which copies the block device byte for byte

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** ddrescue is built for failing media: it keeps going after read errors and tracks what it could not read. Default dd aborts on errors, rsync copies files rather than raw blocks, and cpio does not repair sectors.
</details>

---

### Question 6
**Scenario:** An administrator needs to add the user alice to the docker group without removing her existing supplementary groups.

A. usermod -aG docker alice
B. groupmod -a alice docker
C. usermod -g docker alice
D. usermod -G docker alice

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** -a with -G appends to the supplementary group list. -G alone replaces it. -g changes the primary group, and groupmod does not manage membership this way.
</details>

---

### Question 7
**Scenario:** A contractor's access must end completely on a set date, including SSH key logins. Which action achieves that?

A. Delete the user's password hash from /etc/shadow
B. passwd -l contractor
C. usermod -s /bin/bash contractor
D. chage -E with the end date on the account

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** An account expiry date blocks login by any method after that date. Locking the password with passwd -l still allows key-based SSH. Removing the hash can allow an empty password on some configurations and is not a control.
</details>

---

### Question 8
**Scenario:** After a unit file under /etc/systemd/system was edited, systemctl restart still runs the old configuration. What is missing?

A. A reboot is the only way to apply unit file changes
B. systemctl daemon-reload so systemd re-reads unit files
C. systemctl mask to clear the cached unit
D. systemctl isolate multi-user.target

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** systemd caches unit definitions; daemon-reload makes it re-read them. Masking prevents the unit from starting, isolate switches targets, and no reboot is required.
</details>

---

### Question 9
**Scenario:** A Dockerfile sets ENTRYPOINT ["python"] and CMD ["main.py"]. An operator runs docker run myimage other.py. What executes?

A. other.py as the program, because arguments replace ENTRYPOINT
B. The container fails because both instructions are set
C. python main.py, because CMD cannot be overridden
D. python other.py, because the run arguments replace CMD while ENTRYPOINT stays

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** ENTRYPOINT is the fixed program and CMD supplies default arguments that arguments to docker run replace, giving python other.py.
</details>

---

### Question 10
**Scenario:** A firewalld change was made with firewall-cmd --add-service=https and the site worked. After firewall-cmd --reload the site is unreachable. What was the mistake?

A. The service name is wrong; https must be added as port 443
B. The change was runtime-only and was not saved with --permanent
C. firewalld requires a reboot to keep any rule
D. The default zone must be changed to trusted for HTTPS

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Without --permanent a change applies only to the running configuration and a reload discards it. Using firewall-cmd --runtime-to-permanent, or adding --permanent and reloading, keeps it.
</details>

---

### Question 11
**Scenario:** A web application on an SELinux-enforcing server cannot read content in /srv/web although file permissions allow it. What is the correct, persistent fix?

A. semanage fcontext to record the httpd content type for the path, then restorecon
B. chcon on the files, which survives a full filesystem relabel
C. setenforce 0 and leave SELinux permissive
D. chmod -R 777 /srv/web

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Record the context in policy with semanage fcontext and apply it with restorecon. chcon is lost on relabel, permissive mode removes protection, and 777 does not address a context problem.
</details>

---

### Question 12
**Scenario:** Which directive set in /etc/ssh/sshd_config prevents direct root logins over SSH?

A. PasswordAuthentication no
B. X11Forwarding no
C. PermitRootLogin no
D. AllowRoot false

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** PermitRootLogin no refuses root logins. PasswordAuthentication controls passwords for all users, and X11Forwarding controls graphical forwarding. AllowRoot is not an sshd directive.
</details>

---

### Question 13
**Scenario:** An administrator must make a log file append-only so that even root cannot rewrite earlier entries without first removing the flag. Which command does that?

A. chattr +a file
B. setfacl -m u::-w- file
C. chown syslog file
D. chmod 222 file

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** chattr +a sets append-only; the attribute must be cleared with chattr -a before other changes. File permission bits and ACLs do not stop root, and chown only changes ownership.
</details>

---

### Question 14
**Scenario:** An Ansible task runs shell: echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf. Why is this a problem?

A. Ansible only accepts YAML in /etc/ansible
B. Ansible cannot run shell commands
C. Each run appends another line, so the task is not idempotent
D. Appending to sysctl.conf requires a reboot to take effect

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Idempotent automation leaves the system unchanged on repeated runs. A state-declaring module such as sysctl or lineinfile would not duplicate the line.
</details>

---

### Question 15
**Scenario:** In a bash script, which test is true when a variable named name is set to an empty string?

A. [[ -n "$name" ]]
B. [[ -z "$name" ]]
C. [[ -d "$name" ]]
D. [[ -f "$name" ]]

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** -z is true for a zero-length string. -n is true when the string is not empty, and -d and -f test for a directory and a regular file.
</details>

---

### Question 16
**Scenario:** A developer wants to download new commits from the remote without changing the current branch or working files so the changes can be reviewed first. Which command fits?

A. git rebase
B. git reset --hard
C. git pull
D. git fetch

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** git fetch updates remote-tracking branches only. git pull also merges, rebase rewrites history, and reset --hard discards local changes.
</details>

---

### Question 17
**Scenario:** Users report a slow application. uptime shows a load average of 12 on a 4-core server, yet top shows CPU mostly idle and 65 percent wa. What is the most likely cause?

A. A CPU-bound process is saturating all cores
B. Processes are blocked waiting on disk I/O
C. The server has too much free memory
D. The network interface is down

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** High load with idle CPU and high I/O wait indicates tasks blocked on storage. A CPU bottleneck would show high user or system time, and a down interface would not raise iowait.
</details>

---

### Question 18
**Scenario:** A server can ping 198.51.100.10 but cannot ping app.example.com. Which is the best first area to investigate?

A. DNS configuration, such as /etc/resolv.conf and nsswitch.conf
B. The MTU of the interface
C. The physical link status
D. Routing, because the default gateway is missing

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Reaching an address but not its name isolates the problem to name resolution. A missing gateway or down link would break the ping by address too.
</details>

---

### Question 19
**Scenario:** df -h shows 35 percent free on /var, but creating a new file fails with 'No space left on device'. What should be checked next?

A. free -h for available memory
B. ip -s link for dropped packets
C. lsmod for missing drivers
D. df -i for inode exhaustion

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** When blocks are free but files cannot be created, inode exhaustion (or a quota) is the usual cause, and df -i shows it.
</details>

---

### Question 20
**Scenario:** An SLO of 99.9 percent is set for a service. Which statement describes it correctly?

A. It is the list of devices an SNMP agent exposes
B. It is the contractual commitment to customers, with penalties
C. It is the internal target for a measured indicator such as request success rate
D. It is the measurement itself, such as the count of failed requests

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** An SLO is the target set for an SLI (the measurement). The SLA is the contract. A MIB defines SNMP objects.
</details>

---
