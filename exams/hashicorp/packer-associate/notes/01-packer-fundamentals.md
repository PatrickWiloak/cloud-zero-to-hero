# Packer Fundamentals

Packer is HashiCorp's tool for building identical machine images from a single declarative source. Understanding what Packer is (and isn't) is foundational to the Associate exam.

## What Packer Solves

- **Snowflake images:** Hand-built AMIs drift over time and across teams. Packer codifies them.
- **Slow provisioning at boot:** Installing software at EC2 launch wastes minutes per instance. Packer bakes it in.
- **Security baseline enforcement:** Hardening scripts run once at build time, not per instance.
- **Multi-cloud parity:** One template can produce AWS AMIs, Azure images, and GCP images simultaneously.

## What Packer Is Not

- **Not an IaC tool.** Terraform provisions infrastructure. Packer builds images that Terraform later uses.
- **Not a configuration manager.** Ansible, Chef, and Puppet manage running systems over time. Packer runs them once, during build, to bake a snapshot.
- **Not a runtime orchestrator.** Packer finishes and exits. It doesn't maintain the resulting images.

## Packer vs Terraform

| Aspect | Packer | Terraform |
|--------|--------|-----------|
| Output | Machine images (AMI, VHD, Docker image, etc.) | Running infrastructure (VMs, networks, managed services) |
| Lifecycle | Build once, artifact is immutable | Continuous reconciliation with desired state |
| Language | HCL2 | HCL2 |
| Typical runtime | Minutes per build | Minutes to hours per apply |
| State file | None (each build stands alone) | State file required |

They compose: Packer produces an AMI; Terraform provisions instances using that AMI.

## Packer vs Configuration Management

Configuration management tools (Ansible, Chef, Puppet) converge a live system toward desired state on a recurring schedule. Packer runs them once at image build time.

**Benefits of baking over booting:**

- Faster instance startup (no config on boot)
- Deterministic: every instance identical
- Reduced runtime dependency on config management

**Costs:**

- Longer image build time
- New OS packages require a rebuild and redeploy
- Harder to push hotfixes (but hotfixes in pets are a smell anyway)

Modern practice blends both: bake stable components into the AMI, use cloud-init or Ansible at boot for per-instance config.

## The Packer Workflow

```
┌────────────────────────┐
│  1. packer init        │  Download plugins from required_plugins
└────────────────────────┘
           │
┌────────────────────────┐
│  2. packer fmt         │  Format HCL files
└────────────────────────┘
           │
┌────────────────────────┐
│  3. packer validate    │  Syntax + internal consistency
└────────────────────────┘
           │
┌────────────────────────┐
│  4. packer build       │  Create artifacts
└────────────────────────┘
```

## packer build Phases

1. **Parse config:** read all `.pkr.hcl` files, merge variables
2. **Validate:** ensure all references resolve, required vars set
3. **Launch builder:** create a cloud instance, container, or VM per builder
4. **Connect:** SSH or WinRM to the instance
5. **Run provisioners:** in declared order, bail on any failure
6. **Capture artifact:** snapshot the disk, register as AMI, commit container, etc.
7. **Run post-processors:** per source
8. **Clean up:** terminate builder, delete temp security groups, key pairs

Each source in a build runs in parallel by default.

## CLI Overview

```
packer init [DIR]                     # download plugins
packer fmt [DIR]                      # format HCL
packer validate [-var-file] [DIR]     # validate config
packer build [-only] [-except] [DIR]  # execute build
packer inspect [DIR]                  # describe config
packer console [DIR]                  # interactive expression REPL
packer plugins installed              # list installed plugins
packer plugins required [DIR]         # list required per config
packer plugins install SOURCE         # install a plugin
packer hcl2_upgrade file.json         # convert legacy JSON
packer version                        # show version
```

## Installation

**Binary install (recommended)**

- Download from `releases.hashicorp.com/packer/` or install via package manager (brew, choco, apt)
- Place on PATH
- Verify with `packer version`

**Version management**

- `tfenv`-style tools exist for Packer (`pkenv`). Use if juggling multiple versions across projects.
- Pin plugin versions in `required_plugins` for reproducibility

## The required_plugins Block

Every modern Packer config declares which plugins it needs:

```hcl
packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1.3"
    }
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = "~> 1.1"
    }
  }
}
```

Running `packer init` downloads these to `~/.packer.d/plugins/` (or the path set by `PACKER_PLUGIN_PATH`). Without `packer init`, `packer build` fails.

## Plugin Types

1. **Builders:** launch infrastructure, capture image (e.g., `amazon-ebs`, `docker`, `googlecompute`)
2. **Provisioners:** install software and configure (e.g., `shell`, `ansible`, `file`)
3. **Post-processors:** transform or publish artifacts (e.g., `manifest`, `docker-push`, `hcp-packer-registry`)
4. **Data sources:** query external systems during build (e.g., `amazon-ami`, `hcp-packer`)

A plugin package often bundles multiple types. The `amazon` plugin provides `amazon-ebs`, `amazon-chroot`, `amazon-ami` data source, `amazon-import` post-processor, etc.

## HCL2 File Layout

Packer reads all `.pkr.hcl` files in a directory, merging their contents. Common layout:

```
project/
├── packer.pkr.hcl       # required_plugins, provider blocks
├── variables.pkr.hcl    # variable declarations
├── source.pkr.hcl       # source blocks
├── build.pkr.hcl        # build blocks
├── locals.pkr.hcl       # locals
└── production.pkrvars.hcl  # environment-specific values
```

File names are convention; Packer reads all `.pkr.hcl` regardless of name.

## Variables Load Order (precedence high to low)

1. `-var` CLI flag
2. `-var-file` CLI flag
3. `*.auto.pkrvars.hcl` (auto-loaded)
4. Environment variable `PKR_VAR_foo`
5. Default in `variable "foo" { default = ... }`

## Validation Tips

- Run `packer validate` in CI on every PR. Fast, free, catches most errors.
- Use `packer validate -evaluate-datasources` to also resolve data sources (requires credentials).
- Pair with `packer fmt -check` for formatting enforcement.

## Packer as a Build System Citizen

Treat Packer like any other build tool:

- Keep templates in version control
- Never commit credentials
- Sign your releases with the `checksum` post-processor
- Publish artifacts to a central registry (HCP Packer, ECR, Docker Hub)

## Environment Variables Worth Knowing

| Variable | Effect |
|----------|--------|
| `PACKER_LOG=1` | Enable debug logging |
| `PACKER_LOG_PATH=./packer.log` | Log to file |
| `PACKER_CACHE_DIR=/tmp/packer-cache` | Move cache (ISO downloads, etc.) |
| `PACKER_PLUGIN_PATH` | Plugin installation directory |
| `PACKER_CONFIG` | Path to the global config file |
| `PKR_VAR_foo` | Set variable `foo` |
| `CHECKPOINT_DISABLE=1` | Disable version-check |

## Common Early Mistakes

- Forgetting `packer init` after adding a `required_plugins` entry
- Running `packer build` with ambient AWS credentials you didn't realize were set
- Using JSON template syntax inside a `.pkr.hcl` file
- Hardcoding region or AMI IDs instead of using data sources
- Not cleaning up failed builder instances (manually, if Packer crashed)

## Exam-Ready Checklist

- [ ] Can explain Packer's role vs Terraform vs Ansible
- [ ] Know all major CLI subcommands and their effects
- [ ] Understand the build lifecycle end to end
- [ ] Know the plugin types and `required_plugins` syntax
- [ ] Know variable precedence rules
- [ ] Can convert a legacy JSON template to HCL2

## Key terms

- **Packer** - a HashiCorp tool that builds identical machine images for multiple platforms from a single template.
- **Template** - the HCL2 configuration that tells Packer what to build, how to provision it and what to do with the result.
- **Source block** - a block that defines a reusable builder configuration, such as an Amazon EBS or Docker source.
- **Build block** - a block that lists the sources to build, the provisioners to run and the post-processors to apply.
- **Artifact** - the output of a build, such as an AMI ID or a container image.
- **`packer init`** - installs the plugins declared in the `required_plugins` block.
- **`packer validate`** - checks that a template is syntactically valid and correctly configured.
- **`packer fmt`** - rewrites template files into the canonical HCL2 format.
