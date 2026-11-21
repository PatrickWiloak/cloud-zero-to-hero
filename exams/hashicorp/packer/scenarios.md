# Packer Associate - Real-World Scenarios

## Scenario 1: Golden AMI Pipeline

**Question:** You work at a company with 200 EC2 instances running Ubuntu. Security scans take hours and reveal the same vulnerabilities across machines. How would you use Packer to solve this?

**Answer:** Build a golden AMI weekly. Author a Packer template with an `amazon-ebs` builder sourced from the latest Ubuntu public AMI. Add a `shell` provisioner that runs `apt-get update && apt-get upgrade -y`, applies CIS hardening scripts, and installs required agents (CloudWatch, SSM, security tools). Add the `manifest` post-processor for provenance. Run in GitHub Actions on a weekly schedule. Downstream Terraform consumers reference the AMI ID via an HCP Packer channel or SSM parameter. New instances automatically get the patched base.

## Scenario 2: Multi-Region AMI Distribution

**Question:** You need the same AMI in `us-east-1`, `us-west-2`, and `eu-west-1`. How do you produce them efficiently?

**Answer:** Use the `ami_regions` argument in a single `amazon-ebs` source:

```hcl
source "amazon-ebs" "ubuntu" {
  region      = "us-east-1"
  ami_regions = ["us-west-2", "eu-west-1"]
  # ...
}
```

Packer builds in `us-east-1` and copies the resulting AMI to the listed regions. Single build, single AMI lineage. Alternative: define three separate sources and build in parallel, but this creates three independent AMIs with different IDs per region.

## Scenario 3: Image Needs Company-Signed Certs

**Question:** The security team requires all images to include a set of internal CA certificates. The certs change quarterly. How do you manage this cleanly?

**Answer:** Store certs in a dedicated Git repo or artifact store. Use the `file` provisioner to upload the cert directory:

```hcl
provisioner "file" {
  source      = "certs/"
  destination = "/tmp/certs"
}

provisioner "shell" {
  inline = [
    "sudo cp /tmp/certs/*.crt /usr/local/share/ca-certificates/",
    "sudo update-ca-certificates",
  ]
}
```

When certs change, bump the version in the certs repo, rebuild, promote through HCP Packer channels.

## Scenario 4: Faster Build with amazon-chroot

**Question:** Your builds take 15 minutes per AMI, mostly waiting for EC2 launch and shutdown. The build host is already an EC2 instance. Can you speed this up?

**Answer:** Use the `amazon-chroot` builder. It builds the AMI in place on the current instance by creating and mounting an EBS volume, provisioning inside a chroot, then snapshotting. No second instance is launched, cutting build time dramatically. Tradeoffs: the host must have appropriate IAM and tooling; debugging is harder. Stick with `amazon-ebs` unless build speed is critical and you have the ops maturity.

## Scenario 5: Secrets in Provisioners

**Question:** Your provisioner needs a database password to seed test data during image creation. How do you handle the secret?

**Answer:** Never hardcode. Options in priority order:

1. Pass via `PKR_VAR_db_password` environment variable (highest automation friendliness)
2. Reference a Vault data source in Packer: `data "vault" { ... }`
3. Use AWS Secrets Manager with `data.amazon-secretsmanager`
4. Use a secure variable file, never committed

Mark the variable `sensitive = true` so it is redacted from logs:

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}
```

## Scenario 6: Converting a JSON Template

**Question:** You inherit a legacy Packer JSON template. How do you modernize it?

**Answer:** Run `packer hcl2_upgrade template.json`. This produces `template.json.pkr.hcl`. Review the output, clean up formatting with `packer fmt`, then delete the JSON file. Add a `required_plugins` block because modern HCL2 requires explicit plugin declaration. Test with `packer validate` then `packer build`.

## Scenario 7: HCP Packer Channels and Rollback

**Question:** You promote iteration v42 to the `production` channel. Users start reporting crashes. How do you roll back with HCP Packer?

**Answer:** Go to HCP Packer > your bucket > Channels > production. Change the channel pointer from iteration v42 back to v41. Consumers reading `data.hcp_packer_artifact` with `channel_name = "production"` will now get v41 on their next Terraform plan. If the crashing instances are already running, terminate them so replacement ASG capacity uses v41. Then revoke v42 (marks it as unfit) and investigate root cause before re-promotion.

## Scenario 8: Parallel Builds Hitting API Limits

**Question:** You build 8 AMIs in parallel across multiple sources. AWS API rate limits throw throttling errors. How do you reduce contention?

**Answer:** Two options:

1. Serialize: `packer build -parallel-builds=2 .` limits concurrency to 2.
2. Stagger: use a CI matrix with max-parallel=2 and separate runs per matrix cell.

Also check for repeated `describe-images` or `describe-instances` calls in provisioners; these are common rate-limit culprits. Add retries in scripts. Use regions that are less congested if possible.

## Scenario 9: Ansible Provisioner vs Ansible-Local

**Question:** You have an Ansible playbook to apply. Should you use `ansible` or `ansible-local`?

**Answer:** Depends on network and bootstrap constraints.

- `ansible`: runs on your Packer host, connects to the builder via SSH. Requires Ansible installed on host. Simpler for most Linux builds.
- `ansible-local`: copies playbooks to the builder and runs Ansible inside. No SSH from host needed. Useful for Windows (over WinRM), air-gapped environments, or when your host cannot reach the builder network directly.

Most cloud builds use `ansible`. On-prem or restricted networks use `ansible-local`.

## Scenario 10: Docker Image Build

**Question:** You want to use Packer to build Docker images instead of Dockerfiles. Why would you, and how?

**Answer:** Reasons: unified pipeline with AMI builds, shared provisioners (Ansible playbooks for containers and VMs), HCP Packer registry for containers. Configuration:

```hcl
source "docker" "ubuntu" {
  image  = "ubuntu:22.04"
  commit = true
  changes = [
    "EXPOSE 8080",
    "ENTRYPOINT [\"/usr/bin/myapp\"]",
  ]
}

build {
  sources = ["source.docker.ubuntu"]
  provisioner "shell" {
    inline = ["apt-get update && apt-get install -y curl"]
  }
  post-processor "docker-tag" {
    repository = "myorg/myapp"
    tag        = ["latest", "${formatdate("YYYYMMDD", timestamp())}"]
  }
  post-processor "docker-push" {
    login          = true
    login_username = var.dockerhub_user
    login_password = var.dockerhub_password
  }
}
```

For most pure Docker use cases, Dockerfile is still simpler. Use Packer when you need cross-format (AMI and container from same provisioner code).

## Scenario 11: Debugging a Failing Build

**Question:** Your build fails during a provisioner with an unhelpful error. How do you debug?

**Answer:**

1. Re-run with `PACKER_LOG=1 packer build . 2>&1 | tee packer.log` for verbose output.
2. Add a `breakpoint` provisioner right before the failing step. This pauses the build; SSH into the instance using the temporary key printed in the log.
3. Run the failing command manually inside the paused instance. Read stderr.
4. Use `-on-error=ask` so that on failure Packer waits and offers to keep the instance running for inspection.
5. For transient network issues, add retries in shell scripts.

## Scenario 12: CI Pipeline That Only Builds on Changes

**Question:** You have 5 Packer templates in a monorepo. You don't want to rebuild all 5 on every commit. How do you selectively rebuild?

**Answer:** Use a CI matrix with a "changed files" filter. In GitHub Actions, use `dorny/paths-filter@v3` to detect which template directories changed, then trigger only those builds:

```yaml
- uses: dorny/paths-filter@v3
  id: filter
  with:
    filters: |
      ubuntu: images/ubuntu/**
      amazon-linux: images/amazon-linux/**

- name: Build Ubuntu
  if: steps.filter.outputs.ubuntu == 'true'
  run: cd images/ubuntu && packer build .
```

Alternative: maintain `only` / `except` lists computed from git diff and pass to `packer build`.
