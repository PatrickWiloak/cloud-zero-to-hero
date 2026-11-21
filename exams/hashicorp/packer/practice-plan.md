# Packer - Practice Plan

A 3-week plan assuming 8 to 10 hours per week. Extend to 4 weeks if new to Packer; compress to 2 weeks if you already build production images regularly.

## Prerequisites Before Week 1

- Packer 1.11 or newer installed locally (`packer version`)
- AWS account with credentials configured (`aws configure`)
- Text editor with HCL syntax highlighting (VS Code + HashiCorp Terraform extension)
- Git repository for storing your practice templates
- Budget alarm set on AWS at $20

## Week 1: Fundamentals, First Build, Plugin Model

**Reading**
- `fact-sheet.md` end to end
- Notes file `01-packer-fundamentals.md`
- Notes file `02-builders-and-sources.md`
- Official tutorial: "Build an Image" for AWS

**Labs**
- Install Packer 1.11
- Author a minimal `aws-ubuntu.pkr.hcl` that builds an Ubuntu AMI
- Run `packer init`, `packer fmt`, `packer validate`, `packer build` in sequence
- Introduce a `source_ami_filter` to dynamically pick the latest Ubuntu
- Add `tags` including a `BuildDate` local with `timestamp()`
- Build a second source for a different region; run both in parallel

**Checkpoint**
- Successful AMI in your AWS account
- You can explain what `packer init` does and why it is required
- You have deleted the AMI and its snapshot (cost hygiene)

## Week 2: Provisioners, Post-Processors, HCL2 Depth

**Reading**
- Notes file `03-provisioners-and-post-processors.md`
- Notes file `04-hcl-configuration.md`
- Official docs: shell provisioner, ansible provisioner, manifest post-processor

**Labs**
- Add a `shell` provisioner that installs nginx and a custom index.html
- Upload the index.html using the `file` provisioner
- Add the `manifest` post-processor to write `manifest.json`
- Add the `checksum` post-processor for SHA256
- Convert the `shell` provisioner to `ansible` with a minimal playbook that installs nginx
- Use `breakpoint` to pause a build and SSH in to inspect

**Docker practice (optional but helpful)**
- Author a Docker builder template
- Run the same Ansible playbook against the container
- Push with `docker-push` to a local registry

**Checkpoint**
- You can choose between shell and ansible provisioners based on use case
- You understand what each post-processor adds to the pipeline
- You can read a `manifest.json` and explain what it contains

## Week 3: HCP Packer, Multi-Cloud, CI/CD

**Reading**
- Notes file `05-multi-cloud-images.md`
- Notes file `06-cicd-integration.md`
- Official docs: HCP Packer registry, GitHub Actions Packer examples

**Labs**
- Create an HCP Packer bucket for your Ubuntu image
- Add the `hcp-packer-registry` post-processor
- Run a build; confirm the iteration appears in HCP Packer
- Create `development` and `production` channels; promote an iteration
- Consume the channel in a minimal Terraform config

**GitHub Actions pipeline**
- Author `.github/workflows/packer.yml` that runs init, fmt, validate, build on PRs
- Use OIDC to get AWS credentials (no long-lived keys)
- Gate `build` to only run on main

**Multi-cloud (if you have time and credits)**
- Add an `azure-arm` or `googlecompute` source to the same build
- Run `packer build` and confirm images in both clouds

**Self-check**
- Take a 60-minute untimed review of `scenarios.md`
- Identify any weak topics from the fact sheet
- Re-read relevant notes files


## Daily Drills (15 minutes during week 3)

- Recite the Packer CLI subcommands from memory
- Name 5 builders, 3 provisioners, 3 post-processors
- Explain variable precedence (CLI > env > var-file > default)
- Explain the difference between `only` and `except`

## Hands-on Lab Environment Checklist

- [ ] `packer version` returns 1.10+
- [ ] AWS credentials work (`aws sts get-caller-identity`)
- [ ] You have built at least one AMI end to end
- [ ] You have used at least 2 provisioners (shell + ansible or file)
- [ ] You have used at least 2 post-processors (manifest + one other)
- [ ] You have registered an image in HCP Packer
- [ ] You have a working CI pipeline that runs validate on PR

## Next steps

Pair this with HashiCorp exams that exist today:

- Terraform Associate or Professional
- Vault Associate (for credential management in build pipelines)

Packer slots naturally between Terraform (infrastructure) and runtime configuration (Ansible/Chef/cloud-init). Understanding the full stack makes each tool more useful.
