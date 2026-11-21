# Multi-Cloud Images and HCP Packer

One of Packer's selling points is producing equivalent images across multiple clouds from a single codebase. HCP Packer is HashiCorp's managed registry that tracks, promotes, and audits those images.

## One Template, Many Clouds

A single build block can reference multiple sources across different providers. All run in parallel.

```hcl
packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1.3"
    }
    azure = {
      source  = "github.com/hashicorp/azure"
      version = "~> 2.0"
    }
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = "~> 1.1"
    }
  }
}

source "amazon-ebs" "ubuntu" {
  region        = "us-east-1"
  instance_type = "t3.micro"
  ami_name      = "ubuntu-${local.timestamp}"
  # ...
}

source "azure-arm" "ubuntu" {
  managed_image_name = "ubuntu-${local.timestamp}"
  location           = "East US"
  vm_size            = "Standard_DS2_v2"
  # ...
}

source "googlecompute" "ubuntu" {
  project_id   = var.gcp_project
  zone         = "us-central1-a"
  image_name   = "ubuntu-${local.timestamp}"
  # ...
}

build {
  name = "ubuntu-multi-cloud"
  sources = [
    "source.amazon-ebs.ubuntu",
    "source.azure-arm.ubuntu",
    "source.googlecompute.ubuntu",
  ]

  provisioner "shell" {
    inline = ["sudo apt-get update && sudo apt-get install -y nginx"]
  }
}
```

One `packer build` produces three images. The same provisioner runs on each. Fast and DRY.

## Challenges in Multi-Cloud Builds

- **Different usernames per AMI:** Ubuntu on AWS is `ubuntu`; on Azure may be any set user; on GCP may be `packer` or any user.
- **Different package availability:** cloud-specific agents (cloud-init, SSM, Azure Linux Agent) vary.
- **Different default disk layouts:** first boot behavior differs.
- **Different networking:** VPCs, VNets, VPC Networks all behave slightly differently.
- **Quotas and regions:** each cloud has its own capacity limits.

Keep provisioners cloud-agnostic where possible. Use conditionals or `only` / `except` filters for cloud-specific steps:

```hcl
provisioner "shell" {
  only = ["amazon-ebs.ubuntu"]
  inline = ["sudo yum install -y amazon-ssm-agent"]
}
```

## Multi-Region Within One Cloud

For a single cloud, multi-region is often handled by builder-specific arguments (e.g., `ami_regions` for AWS) rather than separate sources. This produces a single AMI lineage replicated across regions, with the same ID semantics.

For GCP, images are global by default. For Azure, images can be global via Shared Image Galleries.

## HCP Packer Overview

HCP Packer is HashiCorp Cloud Platform's managed image registry. It tracks:

- **Buckets:** logical containers for image lineages (e.g., "ubuntu-base")
- **Iterations:** individual builds; each tagged with metadata
- **Artifacts:** the actual cloud-side images within an iteration (per region, per platform)
- **Channels:** named pointers to iterations (e.g., "production" -> iteration 42)

Think git analogy: bucket is a repo, iterations are commits, channels are branches or tags.

## Authenticating to HCP Packer

Create an HCP service principal, grab its client ID and secret, set env vars:

```
export HCP_CLIENT_ID=xxx
export HCP_CLIENT_SECRET=yyy
```

Optionally `export HCP_PROJECT_ID=zzz` if multiple projects.

## The hcp-packer-registry Post-Processor

```hcl
post-processor "hcp-packer-registry" {
  bucket_name = "ubuntu-base"
  description = "Ubuntu 22.04 LTS base image"
  bucket_labels = {
    "os"      = "ubuntu-22.04"
    "maintained_by" = "platform-team"
  }
  build_labels = {
    "build-timestamp" = local.timestamp
    "build-commit"    = var.git_commit
  }
}
```

Behavior:

- Creates the bucket if it doesn't exist (on first run)
- Creates a new iteration for this build
- Records artifacts per source (AMI IDs, Azure image IDs, GCP images)
- Records provenance metadata (who built, when, from what commit)

## Channels

Channels are pointers to iterations. They are how downstream consumers resolve "the current production Ubuntu image" without hardcoding iteration IDs.

Typical channels:

- `latest`: automatically follows the most recent successful iteration (opt-in)
- `development`: manually set by dev team
- `staging`: set after QA
- `production`: set after approval

Promotion is a single API call or UI click: change the channel's pointer to a new iteration.

## Consuming HCP Packer in Terraform

```hcl
data "hcp_packer_artifact" "ubuntu" {
  bucket_name  = "ubuntu-base"
  channel_name = "production"
  platform     = "aws"
  region       = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = data.hcp_packer_artifact.ubuntu.external_identifier
  instance_type = "t3.micro"
}
```

At plan time, Terraform queries HCP Packer for the artifact pointed to by the `production` channel. Promote a new iteration and the next Terraform plan picks up the new AMI.

## Iteration Statuses

- **Scheduled:** created, build not started
- **Running:** build in progress
- **Cancelled:** manually cancelled
- **Failed:** build failed
- **Done:** build succeeded
- **Revoked:** marked unfit for use; consumers may refuse to deploy

Revocation is used to flag a vulnerable or broken image without deleting it. Consumers can opt to fail if they resolve to a revoked iteration.

## Restoring a Revoked Iteration

If revocation was wrong (false alarm), restore via UI or API. The iteration returns to `done` status.

## Image Immutability

HCP Packer does not prevent you from deleting the underlying AMI in AWS. If you delete the AMI, consumers pointing to that iteration will fail. Use AWS AMI deregistration protection or Glue code that keeps iterations and AMIs in sync.

## Ancestry

HCP Packer tracks parent-child relationships: if your build uses a base image from another HCP Packer bucket (via `data.hcp-packer-artifact` in Packer), it records the lineage. The UI shows ancestry graphs for audit.

## Compliance Views

HCP Packer Plus includes a "compliance" view showing which channels reference which iterations across buckets, helping you audit whether production is running approved images.

## No-Code Patterns for Image Consumption

Pair HCP Packer with Terraform's no-code modules:

1. A module uses `data.hcp_packer_artifact` with parameterized `channel_name`
2. Mark the module as "no-code ready" in the private registry
3. Consumers launch workspaces via UI, selecting a channel
4. End result: a VM provisioned from the latest approved image without writing HCL

## Artifacts vs External Identifiers

Within HCP Packer:

- `artifact_id`: HCP's internal ID
- `external_identifier`: the cloud provider's ID (AMI ID, Azure image resource ID, GCP image self-link)

Consumers almost always use `external_identifier`.

## Alternatives to HCP Packer

- **AWS Systems Manager Parameter Store:** store AMI IDs under a path; consumers read via data source. Simple, but no channels, ancestry, or compliance.
- **Custom database or git repo:** same idea with a home-grown registry. Maintenance cost.
- **AMI tagging conventions:** tag AMIs with `Environment=production`; consumers filter. Works for simple cases.

HCP Packer's value is the full audit trail and channel-based promotion flow. For basic use cases, parameter store may be enough.

## Multi-Cloud Pipelines in Practice

A mature pipeline typically:

1. Builds images for each target cloud in parallel
2. Tags and registers with HCP Packer
3. Runs smoke tests (Terratest, InSpec) against each artifact
4. On pass, promotes to `staging` channel
5. After acceptance tests, promotes to `production`
6. Old iterations marked revoked after N days

## Exam-Ready Checklist

- [ ] Can author a build with multiple cloud sources
- [ ] Know when to use `only` / `except` for cloud-specific provisioners
- [ ] Understand HCP Packer buckets, iterations, channels, artifacts
- [ ] Can configure `hcp-packer-registry` post-processor
- [ ] Can consume HCP Packer in Terraform via `data.hcp_packer_artifact`
- [ ] Understand revocation and ancestry
- [ ] Know `HCP_CLIENT_ID` and `HCP_CLIENT_SECRET` for auth
