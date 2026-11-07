# Provisioners and Post-Processors

Provisioners install software and configure the system inside the builder. Post-processors transform or publish the resulting artifact. Together they turn a raw OS into a fully-baked deployable image.

## Provisioners Overview

Provisioners run in the order declared, sequentially per source. Any failure aborts the build for that source (unless `on_error` is set).

```hcl
build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = ["sudo apt-get update"]
  }

  provisioner "file" {
    source      = "app.jar"
    destination = "/tmp/app.jar"
  }

  provisioner "shell" {
    inline = ["sudo mv /tmp/app.jar /opt/app.jar"]
  }
}
```

## The shell Provisioner

Most-used provisioner. Runs shell commands on the builder instance via SSH.

```hcl
provisioner "shell" {
  inline = [
    "sudo apt-get update",
    "sudo apt-get install -y nginx",
  ]
}

provisioner "shell" {
  scripts = [
    "scripts/harden.sh",
    "scripts/install-agents.sh",
  ]
}

provisioner "shell" {
  script            = "scripts/bootstrap.sh"
  environment_vars  = ["APP_VERSION=${var.app_version}"]
  execute_command   = "sudo -E bash '{{ .Path }}'"
}
```

- `inline`: list of commands executed in one shell session
- `script`: single local script uploaded and executed
- `scripts`: multiple scripts run in order
- `environment_vars`: exported before execution
- `execute_command`: custom invocation (useful for `sudo -E`)
- `expect_disconnect`: tolerate the SSH disconnect caused by `reboot`
- `pause_before`, `pause_after`: delays
- `valid_exit_codes`: default is `[0]`; set to allow non-zero exits

## The file Provisioner

Copies files or directories to/from the builder.

```hcl
provisioner "file" {
  source      = "configs/"
  destination = "/tmp/configs/"
}

provisioner "file" {
  source      = "/var/log/custom.log"
  destination = "./local-copy.log"
  direction   = "download"
}
```

- `direction = "upload"` (default) or `"download"`
- The destination must exist or be writable by the SSH user
- Use a staging dir like `/tmp` then `shell` to move with sudo

## The ansible Provisioner

Runs Ansible against the builder from the Packer host. Requires Ansible installed on the host.

```hcl
provisioner "ansible" {
  playbook_file = "playbook.yml"
  user          = "ubuntu"
  extra_arguments = ["-vv", "--extra-vars", "env=build"]
  groups        = ["build"]
}
```

Features:

- Automatic inventory generation
- Support for roles (`ansible.cfg` or `roles_path`)
- Can target Windows via WinRM

## The ansible-local Provisioner

Runs Ansible inside the builder, not on the host. Requires Ansible installed on or installed into the builder.

```hcl
provisioner "ansible-local" {
  playbook_file = "playbook.yml"
  playbook_dir  = "./playbooks"
}
```

Use when:

- Host cannot SSH directly to builder (network constraints)
- Building Windows images where running Ansible from host is awkward
- You want the playbook available inside the image for re-runs

## PowerShell and Windows Provisioners

For Windows builds:

```hcl
provisioner "powershell" {
  inline = [
    "Install-WindowsFeature -Name Web-Server",
    "Set-Service -Name W3SVC -StartupType Automatic",
  ]
}

provisioner "windows-shell" {
  inline = ["net user /add myuser P@ssw0rd"]
}

provisioner "windows-restart" {
  restart_timeout = "10m"
}
```

## Chef and Puppet Provisioners

For teams already using these systems:

- `chef-solo`: runs local cookbooks
- `chef-client`: registers with a Chef server
- `puppet-masterless`: runs manifests locally
- `puppet-server`: registers with PE

Modern practice leans toward `shell` + `ansible`, but existing shops use these.

## The breakpoint Provisioner

Pauses the build for interactive debugging.

```hcl
provisioner "breakpoint" {
  disable = false
  note    = "Inspect after nginx install"
}
```

Packer prints SSH details and waits for you to press enter. Open a second terminal, SSH in, poke around, then continue. Remove before production pipelines.

## The shell-local Provisioner

Runs commands on the host that is running Packer, not on the builder.

```hcl
provisioner "shell-local" {
  inline = [
    "echo Building AMI at $(date)",
    "./scripts/fetch-certs.sh",
  ]
}
```

Useful for:

- Fetching artifacts locally before `file` upload
- Notifying external systems (Slack, Datadog)
- Pre- or post-build housekeeping

## Error Handling

```hcl
provisioner "shell" {
  inline = ["false"]
  on_error = "cleanup"  # cleanup, abort, run-cleanup-provisioner, ask
}
```

- `cleanup` (default): clean up builder resources and exit
- `abort`: leave the instance running for debugging
- `run-cleanup-provisioner`: run the cleanup provisioner first
- `ask`: interactive prompt

CLI flag: `packer build -on-error=abort .`

## Provisioner Filtering

Restrict a provisioner to specific sources using `only` and `except`:

```hcl
provisioner "shell" {
  only   = ["amazon-ebs.prod"]
  inline = ["echo prod-only"]
}
```

## Post-Processors Overview

Post-processors run after the builder produces an artifact. They can chain (the output of one becomes input to the next) using `post-processors` blocks:

```hcl
build {
  # ...

  post-processor "shell-local" {
    inline = ["echo Build complete"]
  }

  post-processors {
    post-processor "manifest" { output = "manifest.json" }
    post-processor "checksum" { checksum_types = ["sha256"] }
  }
}
```

Note the singular `post-processor` for independent runs, plural `post-processors` (a block containing post-processor entries) for chained sequences.

## The manifest Post-Processor

Writes a JSON file describing all artifacts from the build:

```hcl
post-processor "manifest" {
  output     = "manifest.json"
  strip_path = true
  custom_data = {
    build_id = "${formatdate("YYYYMMDD-hhmm", timestamp())}"
  }
}
```

Contents (example):

```json
{
  "builds": [{
    "name": "base",
    "builder_type": "amazon-ebs",
    "build_time": 1690000000,
    "files": null,
    "artifact_id": "us-east-1:ami-abc123",
    "packer_run_uuid": "..."
  }],
  "last_run_uuid": "..."
}
```

Consume in Terraform or pipelines to pick up AMI IDs programmatically.

## The checksum Post-Processor

Generates hashes for output files:

```hcl
post-processor "checksum" {
  checksum_types = ["md5", "sha256", "sha512"]
}
```

Useful for artifacts like qcow2 or OVA files. AMIs do not have a filesystem hash concept.

## The docker Post-Processors

- `docker-tag`: apply tags to a committed image
- `docker-push`: push to a registry
- `docker-save`: save image as tarball
- `docker-import`: import tarball as Docker image

```hcl
post-processors {
  post-processor "docker-tag" {
    repository = "myorg/myapp"
    tag        = ["latest", "${timestamp()}"]
  }
  post-processor "docker-push" {
    login          = true
    login_server   = "registry.example.com"
    login_username = var.registry_user
    login_password = var.registry_pass
  }
}
```

## The amazon-import Post-Processor

Imports a VMDK or OVA file as an AMI. Used with `vsphere-iso` or other non-AWS sources to produce an AMI in AWS.

## The googlecompute-import Post-Processor

Similarly imports a raw disk image into GCP as a Compute image.

## The vagrant Post-Processor

Packages a build as a Vagrant box:

```hcl
post-processor "vagrant" {
  keep_input_artifact = true
  output              = "output/ubuntu-{{.Provider}}.box"
}
```

## The hcp-packer-registry Post-Processor

Registers the artifact as an iteration in HCP Packer:

```hcl
post-processor "hcp-packer-registry" {
  bucket_name = "ubuntu-base"
  description = "Ubuntu 22.04 with hardening"
  bucket_labels = {
    os = "ubuntu-22.04"
  }
  build_labels = {
    build_id = "${formatdate("YYYYMMDD-hhmm", timestamp())}"
  }
}
```

Requires `HCP_CLIENT_ID` and `HCP_CLIENT_SECRET` env vars.

## Chaining Considerations

When chaining post-processors, by default each subsequent post-processor consumes the output of the previous and replaces the artifact. Set `keep_input_artifact = true` to preserve both.

```hcl
post-processors {
  post-processor "compress" {
    keep_input_artifact = true
  }
  post-processor "shell-local" {
    inline = ["upload-to-s3.sh"]
  }
}
```

## Best Practices

- **Idempotency:** scripts should be safe to re-run. Use `apt-get install -y` (idempotent) not `tar xf` on a volatile path.
- **Clean up during build:** `apt-get clean`, remove SSH host keys, zero free space if size matters.
- **Don't leave secrets on disk:** any provisioner that writes secrets must remove them before image capture.
- **Tag and version:** every artifact should be traceable back to a git commit, build timestamp, and pipeline run.
- **Prefer Ansible for complex config:** shell scripts become unwieldy past ~50 lines.

## Common Errors

- `Permission denied`: wrong `ssh_username` for the source AMI
- `dial tcp: i/o timeout`: security group or subnet does not allow SSH from Packer's IP
- `Failed to upload file`: destination directory does not exist or no write permission
- `ansible-playbook: command not found`: Ansible not installed on the Packer host (use `ansible-local` instead)
- `WinRM connection failed`: Windows build missing `user_data` that enables WinRM

## Exam-Ready Checklist

- [ ] Know differences between shell, shell-local, file, ansible, ansible-local
- [ ] Know when to use `breakpoint`
- [ ] Can chain post-processors with `post-processors` blocks
- [ ] Know the most-used post-processors (manifest, checksum, docker-*, hcp-packer-registry)
- [ ] Understand `on_error` options
- [ ] Can filter provisioners with `only` and `except`

## Key terms

- **Provisioner** - a component that installs and configures software on the temporary machine before it is turned into an image.
- **Post-processor** - a component that takes the artifact from a build and processes it further, for example by compressing or tagging it.
- **`shell` provisioner** - runs shell scripts or inline commands on the machine being built.
- **`file` provisioner** - uploads files or directories from the machine running Packer to the machine being built.
- **`breakpoint` provisioner** - pauses a build until you confirm, which helps with debugging.
- **`manifest` post-processor** - writes a JSON file that records the artifacts a build produced.
