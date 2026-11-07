# Builders and Sources

A builder is the plugin that actually launches infrastructure, runs provisioners, and captures the resulting image. In HCL2, you declare builders inside `source` blocks and reference them in `build` blocks.

## Source Block Anatomy

```hcl
source "amazon-ebs" "ubuntu" {
  ami_name      = "my-ubuntu-${formatdate("YYYYMMDD", timestamp())}"
  instance_type = "t3.micro"
  region        = "us-east-1"
  source_ami    = "ami-0abc123"
  ssh_username  = "ubuntu"
}
```

- First label (`amazon-ebs`): builder type
- Second label (`ubuntu`): local name for referencing
- Body: builder-specific arguments

Reference in a build:

```hcl
build {
  sources = ["source.amazon-ebs.ubuntu"]
}
```

## Common AWS Builders

### amazon-ebs (most common)

Launches an EC2 instance, provisions it, stops it, snapshots the root volume, registers an AMI.

Key arguments:

- `ami_name`: final AMI name; must be unique in the account
- `source_ami` or `source_ami_filter`: which image to start from
- `instance_type`: EC2 instance type
- `region`: primary build region
- `ami_regions`: list of regions to copy AMI to after build
- `ssh_username`: typically `ubuntu`, `ec2-user`, `admin`
- `vpc_id`, `subnet_id`, `security_group_id`: network config (use defaults or pin)
- `tags`: tags applied to AMI
- `run_tags`: tags applied to builder instance
- `encrypt_boot`: encrypt resulting AMI snapshot
- `kms_key_id`: KMS key for encryption

### amazon-chroot

Builds an AMI in place on an already-running EC2 instance. Creates an EBS volume, mounts it, chroots in, provisions, snapshots. No new instance launched.

Use when:
- Build host is already EC2 with required IAM
- Build speed is critical (can be 3x to 5x faster)
- Provisioners do not require networking differences between chroot and host

### amazon-ebssurrogate

Builds an AMI from a detached root volume. Advanced; useful for creating AMIs with custom root partitions or when starting from non-AMI sources.

### amazon-instance

For instance-store backed AMIs. Rarely used today; EBS-backed is standard.

## source_ami_filter

Avoid hardcoding AMI IDs. Use a filter to resolve the latest matching AMI at build time:

```hcl
source_ami_filter {
  filters = {
    name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
    root-device-type    = "ebs"
    virtualization-type = "hvm"
  }
  most_recent = true
  owners      = ["099720109477"]  # Canonical
}
```

Owners by name:
- Canonical (Ubuntu): `099720109477`
- Amazon (Amazon Linux): `amazon`
- Red Hat: `309956199498`

## Multi-Region Distribution

Build once in `region`, copy to others:

```hcl
source "amazon-ebs" "ubuntu" {
  region      = "us-east-1"
  ami_regions = ["us-west-2", "eu-west-1"]
  # ...
}
```

Packer copies the snapshot and registers an AMI in each listed region. All share the same name.

## Azure Builders

### azure-arm

Builds a managed image or a Shared Image Gallery version.

```hcl
source "azure-arm" "ubuntu" {
  subscription_id       = var.subscription_id
  tenant_id             = var.tenant_id
  client_id             = var.client_id
  client_secret         = var.client_secret
  managed_image_name    = "ubuntu-${formatdate("YYYYMMDD", timestamp())}"
  managed_image_resource_group_name = "images"
  location              = "East US"
  vm_size               = "Standard_DS2_v2"
  os_type               = "Linux"
  image_publisher       = "Canonical"
  image_offer           = "0001-com-ubuntu-server-jammy"
  image_sku             = "22_04-lts-gen2"
}
```

Authenticate via service principal (above) or Managed Identity if running on Azure VM.

## GCP Builder

### googlecompute

```hcl
source "googlecompute" "ubuntu" {
  project_id          = "my-project"
  source_image_family = "ubuntu-2204-lts"
  zone                = "us-central1-a"
  image_name          = "ubuntu-${formatdate("YYYYMMDD", timestamp())}"
  machine_type        = "e2-medium"
  ssh_username        = "packer"
}
```

Auth: `GOOGLE_APPLICATION_CREDENTIALS` env var pointing to service account JSON, or workload identity if running on GCP.

## Docker Builder

```hcl
source "docker" "ubuntu" {
  image  = "ubuntu:22.04"
  commit = true      # or `discard = true` for no output
  changes = [
    "EXPOSE 8080",
    "ENTRYPOINT [\"/usr/bin/myapp\"]",
    "USER myapp",
  ]
}
```

- `commit = true`: image is committed, usable by docker-tag/docker-push
- `export_path = "out.tar"`: alternatively export as tarball
- `changes`: Dockerfile-like metadata applied at commit

## VMware and vSphere Builders

### vsphere-iso

Builds from ISO on vSphere:

```hcl
source "vsphere-iso" "ubuntu" {
  vcenter_server       = "vcenter.example.com"
  username             = var.vsphere_user
  password             = var.vsphere_pass
  datacenter           = "dc1"
  cluster              = "cluster1"
  datastore            = "datastore1"
  iso_url              = "https://releases.ubuntu.com/22.04/ubuntu-22.04.3-live-server-amd64.iso"
  iso_checksum         = "sha256:..."
  vm_name              = "ubuntu-template"
  boot_command         = ["..."]
  ssh_username         = "ubuntu"
}
```

Typically paired with `vsphere-template` post-processor to convert the resulting VM to a template.

## Other Builders

- `qemu`: KVM-based; produces qcow2 images
- `virtualbox-iso`: VirtualBox; produces OVA/OVF
- `hyperv-iso`: Hyper-V on Windows
- `oracle-oci`: Oracle Cloud
- `alicloud-ecs`: Alibaba Cloud
- `null`: no instance, provisioner-only workflows

## The null Builder

```hcl
source "null" "example" {
  communicator = "none"
}

build {
  sources = ["source.null.example"]
  provisioner "shell-local" {
    inline = ["echo 'Runs on host only'"]
  }
}
```

No instance is launched. Useful for `shell-local` pipelines, data aggregation, or testing provisioner logic.

## Choosing Between Builders

| Use case | Builder |
|----------|---------|
| Standard AMI build | amazon-ebs |
| Super-fast in-place AMI | amazon-chroot |
| Azure image | azure-arm |
| GCP image | googlecompute |
| Docker container | docker |
| VMware template | vsphere-iso |
| On-prem VM | qemu, virtualbox-iso |
| Provisioner-only workflow | null |

## Builder-Level Settings

Most builders share common fields:

- `communicator`: `ssh`, `winrm`, or `none`
- `ssh_private_key_file`, `ssh_password`, `ssh_keypair_name`
- `pause_before_connecting`: delay before first connection
- `user_data` / `user_data_file`: cloud-init data for first boot
- `temporary_key_pair_type`, `temporary_key_pair_bits`: ephemeral key generation

## Communicators

- **ssh:** Linux/BSD builders, default
- **winrm:** Windows builders
- **none:** null builder, no provisioners use remote connection

For Windows builds you typically set `communicator = "winrm"`, `winrm_username = "Administrator"`, plus user-data to enable WinRM.

## Temporary Resources

Packer creates and cleans up:

- Temporary key pair (SSH)
- Temporary security group (allowing SSH from Packer's IP)
- Temporary subnet assignments if not specified
- IAM instance profile if configured

If Packer crashes, these may leak. Check your cloud account and tag resources with `packer` to find orphans.

## Multiple Sources in One Build

```hcl
source "amazon-ebs" "base" { ... }
source "amazon-ebs" "web"  { ... }

build {
  name    = "multi"
  sources = [
    "source.amazon-ebs.base",
    "source.amazon-ebs.web",
  ]

  provisioner "shell" {
    # runs against both sources in parallel
  }
}
```

Use `only` or `except` to filter at runtime:

```
packer build -only='amazon-ebs.web' .
packer build -except='amazon-ebs.base' .
```

## Dynamic Source Configuration

Use `locals` and `dynamic` blocks to DRY up multi-region or multi-variant builds:

```hcl
locals {
  regions = ["us-east-1", "us-west-2"]
}

source "amazon-ebs" "ubuntu" {
  region      = "us-east-1"
  ami_regions = local.regions
  # ...
}
```

For truly different sources (different OS base images), declare multiple sources rather than trying to parameterize one.

## Exam-Ready Checklist

- [ ] Can author an `amazon-ebs` source with `source_ami_filter`
- [ ] Know when to use `amazon-chroot` vs `amazon-ebs`
- [ ] Understand `ami_regions` for multi-region distribution
- [ ] Can declare Azure, GCP, Docker sources
- [ ] Know what the `null` builder is for
- [ ] Can filter builds with `only` and `except`

## Key terms

- **Builder** - a plugin component that creates a machine, runs the build and produces an image for a specific platform.
- **Communicator** - the mechanism, such as SSH or WinRM, that Packer uses to talk to the machine it is building.
- **HCP Packer** - the HashiCorp Cloud Platform registry that tracks image metadata, versions and channels.
