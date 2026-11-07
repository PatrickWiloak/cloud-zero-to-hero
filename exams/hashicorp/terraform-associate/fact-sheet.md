---
last-updated: 2026-11-07
---

# HashiCorp Terraform Associate (004) - Fact Sheet

## Quick Reference

**Exam Code:** Terraform Associate (004)
**Duration:** 1 hour
**Questions:** Not verified (not stated on the HashiCorp page)
**Passing Score:** Not verified (not stated on the HashiCorp page)
**Cost:** $70.50 USD, plus locally applicable taxes and fees; free retake not included
**Validity:** 2 years
**Format:** Multiple choice, online proctored, English
**Product version tested:** Terraform 1.12
**Difficulty:** ⭐⭐⭐

### Verified facts and sources (checked 2026-11-07)

| Fact | Value | Source |
|------|-------|--------|
| Current version | 004 (the page title is "HashiCorp Certified: Terraform Associate (004)") | [Terraform Associate page](https://developer.hashicorp.com/certifications/terraform-associate) |
| Duration, format, price, expiration | 1 hour, multiple choice, online proctored, $70.50 USD plus taxes, 2 years | Same page |
| Terraform version tested | 1.12 | Same page |
| Objectives | 8 objectives (list below), no weights published | Same page and [004 content list](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004) |
| New in 004 vs 003 | 4f, 4g, 4h, 8c | 004 content list |
| 003 retirement date | **Not verified.** Not on the pages read. A search snippet reported 2026-01-07 | Check HashiCorp |
| Question count, passing score | **Not verified.** The previous version of this guide listed 57 questions and 70 percent for 003 without a vendor source on the current pages | Check HashiCorp |

## Exam Objectives (004)

| # | Objective | Key Focus |
|---|-----------|-----------|
| 1 | IaC with Terraform | What IaC is, advantages, multi-cloud and hybrid workflows |
| 2 | Terraform fundamentals | Providers (install, version, use, multiple), state |
| 3 | Core Terraform workflow | init, validate, plan, apply, destroy, fmt |
| 4 | Terraform configuration | Resource and data blocks, references, variables and outputs, complex types, expressions and functions, **dependencies and lifecycle rules**, **custom conditions**, **sensitive data, ephemeral values, Vault** |
| 5 | Terraform modules | Sources, variable scope, usage, versions |
| 6 | Terraform state management | Local backend, locking, remote state, drift |
| 7 | Maintain infrastructure | Import, state inspection with the CLI, verbose logging |
| 8 | HCP Terraform | Creating infrastructure, collaboration and governance, **workspaces and projects**, CLI integration |

Bold marks content that is new in 004. Notes: [dependencies, conditions and ephemeral values](notes/dependencies-conditions-and-ephemeral-values.md) and [HCP Terraform](notes/hcp-terraform.md). The sections below are carried over from the 003 guide and were not re-verified line by line; the 004 content list shows objectives 1 to 3, 5 to 7 are largely unchanged.

## Infrastructure as Code Fundamentals

### IaC Key Concepts
- Infrastructure defined in human-readable configuration files
- Version controlled, reusable, shareable
- Declarative approach - describe desired end state
- Idempotent - running multiple times produces the same result
- Terraform uses HCL (HashiCorp Configuration Language)
- **[📖 What is Infrastructure as Code](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/infrastructure-as-code)** - IaC concepts introduction
- **[📖 IaC in Terraform Intro](https://developer.hashicorp.com/terraform/intro)** - Terraform overview and use cases

### IaC Tool Comparison
| Tool | Type | Language | Provider |
|------|------|----------|----------|
| Terraform | Provisioning | HCL | Multi-cloud |
| CloudFormation | Provisioning | JSON/YAML | AWS only |
| Ansible | Configuration | YAML | Multi-platform |
| Pulumi | Provisioning | General-purpose | Multi-cloud |
| ARM Templates | Provisioning | JSON | Azure only |

### Terraform vs Others
- **Multi-cloud support:** Works across AWS, Azure, GCP, and hundreds of providers
- **State management:** Tracks actual infrastructure state
- **Execution plans:** Preview changes before applying
- **Resource graph:** Understands dependencies automatically
- **Provider ecosystem:** a large registry of providers (the count is not stated on the registry page, so no figure here)
- **[📖 Terraform Use Cases](https://developer.hashicorp.com/terraform/intro/use-cases)** - Common Terraform use cases

## HCL Configuration Language

### Configuration File Structure
```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = "example-instance"
  }
}
```

### Block Types
- **terraform:** Settings, required providers, backend configuration
- **provider:** Provider configuration and authentication
- **resource:** Infrastructure objects to create/manage
- **data:** Query existing infrastructure or external data
- **variable:** Input parameters for configurations
- **output:** Return values from configurations
- **locals:** Named expressions for reuse within a module
- **module:** Call reusable child modules
- **[📖 Configuration Language](https://developer.hashicorp.com/terraform/language)** - Complete HCL reference
- **[📖 Resource Blocks](https://developer.hashicorp.com/terraform/language/resources)** - Resource configuration syntax

### Variable Types
```hcl
variable "string_var" {
  type    = string
  default = "hello"
}

variable "number_var" {
  type    = number
  default = 42
}

variable "bool_var" {
  type    = bool
  default = true
}

variable "list_var" {
  type    = list(string)
  default = ["a", "b", "c"]
}

variable "map_var" {
  type    = map(string)
  default = { key = "value" }
}

variable "object_var" {
  type = object({
    name = string
    age  = number
  })
}
```

### Variable Precedence (lowest to highest)
1. Default values in variable block
2. `TF_VAR_<name>` environment variables
3. `terraform.tfvars` file
4. `terraform.tfvars.json` file
5. `*.auto.tfvars` and `*.auto.tfvars.json` files (lexical order)
6. `-var` and `-var-file` options on the command line, in the order given (also variables from HCP Terraform)

- **[📖 Variable definition precedence](https://developer.hashicorp.com/terraform/language/values/variables)** - Official order, checked 2026-11-07

- **[📖 Input Variables](https://developer.hashicorp.com/terraform/language/values/variables)** - Variable definitions and usage
- **[📖 Output Values](https://developer.hashicorp.com/terraform/language/values/outputs)** - Output configuration
- **[📖 Local Values](https://developer.hashicorp.com/terraform/language/values/locals)** - Local named values

### Meta-Arguments
- **depends_on:** Explicit dependency declaration
- **count:** Create multiple instances by count
- **for_each:** Create instances from a map or set
- **provider:** Select non-default provider configuration
- **lifecycle:** Customize resource lifecycle behavior
  - `create_before_destroy`
  - `prevent_destroy`
  - `ignore_changes`
  - `replace_triggered_by`
- **[📖 Meta-Arguments](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on)** - Resource meta-arguments reference

### Built-in Functions (Key Categories)
- **String:** `format`, `join`, `split`, `replace`, `trim`, `upper`, `lower`
- **Collection:** `length`, `merge`, `lookup`, `flatten`, `keys`, `values`
- **Numeric:** `max`, `min`, `ceil`, `floor`, `abs`
- **Filesystem:** `file`, `fileexists`, `templatefile`, `pathexpand`
- **Type Conversion:** `tostring`, `tolist`, `tomap`, `tonumber`, `tobool`
- **Encoding:** `base64encode`, `jsonencode`, `yamlencode`
- **[📖 Built-in Functions](https://developer.hashicorp.com/terraform/language/functions)** - Complete function reference

## Providers and Resources

### Provider Configuration
- Providers are plugins that interact with cloud platforms and services
- Each provider has its own resources and data sources
- Providers are downloaded during `terraform init`
- Version constraints: `=`, `!=`, `>`, `>=`, `<`, `<=`, `~>`
- `~>` (pessimistic constraint) allows only the rightmost version component to increment
- **[📖 Provider Configuration](https://developer.hashicorp.com/terraform/language/providers/configuration)** - Provider setup and versioning
- **[📖 Provider Requirements](https://developer.hashicorp.com/terraform/language/providers/requirements)** - Required providers block
- **[📖 Terraform Registry Providers](https://registry.terraform.io/browse/providers)** - Browse all providers

### Provider Aliases
```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

resource "aws_instance" "west_instance" {
  provider      = aws.west
  ami           = "ami-12345678"
  instance_type = "t3.micro"
}
```

### Resource Behavior
- **Create:** Resources that exist in config but not in state
- **Destroy:** Resources that exist in state but not in config
- **Update in-place:** Resources with changed attributes that can be updated
- **Destroy and re-create:** Resources with changed attributes that require replacement
- **[📖 Resource Behavior](https://developer.hashicorp.com/terraform/language/resources/behavior)** - How Terraform manages resources

### Data Sources
- Read-only queries to existing infrastructure
- Read during planning when possible (deferred to apply if an argument is not yet known)
- Used to reference resources not managed by current configuration
- **[📖 Data Sources](https://developer.hashicorp.com/terraform/language/data-sources)** - Data source configuration

## Core Terraform Workflow

### Command Reference

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `terraform init` | Initialize working directory | `-upgrade`, `-reconfigure`, `-migrate-state` |
| `terraform validate` | Check configuration syntax | (no notable flags) |
| `terraform plan` | Preview changes | `-out`, `-destroy`, `-target`, `-var` |
| `terraform apply` | Apply changes | `-auto-approve`, `-target`, `-var`, `-parallelism` |
| `terraform destroy` | Destroy infrastructure | `-auto-approve`, `-target` |
| `terraform fmt` | Format configuration | `-recursive`, `-check`, `-diff` |
| `terraform show` | Show state or plan | `-json` |
| `terraform output` | Show output values | `-json`, `-raw` |
| `terraform refresh` | Update state to match real resources | (deprecated in favor of plan -refresh-only) |
| `terraform graph` | Generate dependency graph | (outputs DOT format) |

- **[📖 CLI Commands](https://developer.hashicorp.com/terraform/cli/commands)** - Complete CLI reference
- **[📖 Terraform Init](https://developer.hashicorp.com/terraform/cli/commands/init)** - Initialization command
- **[📖 Terraform Plan](https://developer.hashicorp.com/terraform/cli/commands/plan)** - Plan command
- **[📖 Terraform Apply](https://developer.hashicorp.com/terraform/cli/commands/apply)** - Apply command

### Init Details
- Downloads and installs providers
- Initializes backend for state storage
- Downloads referenced modules
- Creates `.terraform` directory and `.terraform.lock.hcl`
- Must be run when: adding providers, changing backends, adding modules
- **[📖 Dependency Lock File](https://developer.hashicorp.com/terraform/language/files/dependency-lock)** - Lock file management

## State Management

### State File Purpose
- Maps configuration to real-world resources
- Tracks metadata and resource dependencies
- Performance optimization for large infrastructures
- Default location: `terraform.tfstate` (local)
- Format: JSON
- Contains sensitive data - must be secured
- **[📖 State](https://developer.hashicorp.com/terraform/language/state)** - State overview
- **[📖 Purpose of State](https://developer.hashicorp.com/terraform/language/state/purpose)** - Why Terraform uses state

### Remote Backends
| Backend | Locking | Encryption | Provider |
|---------|---------|------------|----------|
| S3 | Opt-in: `use_lockfile` (default false); DynamoDB locking is deprecated | Yes (SSE) | AWS |
| GCS | Yes (built-in) | Yes (built-in) | GCP |
| Azure Blob | Yes (built-in) | Yes (built-in) | Azure |
| Consul | Yes (built-in, `lock` option on by default) | Not stated on the backend page | HashiCorp |
| Terraform Cloud | Yes (built-in) | Yes (built-in) | HashiCorp |

- **[📖 Backend Configuration](https://developer.hashicorp.com/terraform/language/backend)** - Backend types and setup
- **[📖 S3 Backend](https://developer.hashicorp.com/terraform/language/backend/s3)** - AWS S3 backend configuration
- **[📖 Remote State](https://developer.hashicorp.com/terraform/language/state/remote)** - Remote state storage

### State Commands
```bash
terraform state list                    # List resources in state
terraform state show <resource>         # Show resource details
terraform state mv <source> <dest>      # Move/rename resource in state
terraform state rm <resource>           # Remove resource from state
terraform state pull                    # Pull remote state to stdout
terraform state push                    # Push local state to remote
terraform state replace-provider        # Replace provider in state
```
- **[📖 State Commands](https://developer.hashicorp.com/terraform/cli/commands/state)** - State manipulation commands

### State Locking
- Prevents concurrent modifications to state
- Automatic for supported backends
- Manual unlock: `terraform force-unlock <LOCK_ID>`
- Not all backends support locking
- **[📖 State Locking](https://developer.hashicorp.com/terraform/language/state/locking)** - Locking mechanism details

## Modules

### Module Structure
```
modules/
  my-module/
    main.tf          # Primary resources
    variables.tf     # Input variables
    outputs.tf       # Output values
    README.md        # Documentation
```

### Module Sources
```hcl
# Local path
module "vpc" {
  source = "./modules/vpc"
}

# Terraform Registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
}

# GitHub
module "vpc" {
  source = "github.com/hashicorp/example"
}

# S3 bucket
module "vpc" {
  source = "s3::https://s3.amazonaws.com/bucket/module.zip"
}
```

- **[📖 Modules Overview](https://developer.hashicorp.com/terraform/language/modules)** - Module concepts
- **[📖 Module Sources](https://developer.hashicorp.com/terraform/language/modules/sources)** - Where to find modules
- **[📖 Terraform Registry Modules](https://registry.terraform.io/browse/modules)** - Browse public modules
- **[📖 Module Composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition)** - Module design patterns
- **[📖 Publishing Modules](https://developer.hashicorp.com/terraform/registry/modules/publish)** - Publishing to the registry

### Module Best Practices
- Use semantic versioning for module versions
- Minimize module inputs - use sensible defaults
- Document all variables and outputs
- Use `validation` blocks for input validation
- Nest modules for complex infrastructure patterns

## Workspaces

### Workspace Commands
```bash
terraform workspace list      # List all workspaces
terraform workspace new dev   # Create new workspace
terraform workspace select dev # Switch to workspace
terraform workspace delete dev # Delete workspace
terraform workspace show      # Show current workspace
```

### Workspace Use Cases
- Managing multiple environments (dev, staging, prod)
- Each workspace has its own state file
- Default workspace cannot be deleted
- State for named workspaces is stored in a separate directory (commonly `terraform.tfstate.d/<workspace>/`, not stated on the pages read: unverified)
- Access current workspace: `terraform.workspace`
- **[📖 Workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)** - Workspace management

## Import and Migration

### Terraform Import
```bash
terraform import aws_instance.example i-1234567890abcdef0
```
- Brings existing infrastructure under Terraform management
- The CLI command only imports into state - it does not generate configuration (import blocks can, via `terraform plan -generate-config-out`)
- Configuration must be written manually (or use `terraform plan -generate-config-out`)
- One resource at a time
- **[📖 Import](https://developer.hashicorp.com/terraform/cli/import)** - Import existing resources

### Import Block (Terraform 1.5+)
```hcl
import {
  to = aws_instance.example
  id = "i-1234567890abcdef0"
}
```
- Declarative import in configuration
- Can generate configuration automatically
- Declare one import block per resource; the CLI command imports one resource per run
- Preview with `terraform plan`

## Provisioners

### Types
- **local-exec:** Run commands on the machine running Terraform
- **remote-exec:** Run commands on the remote resource
- **file:** Copy files to the remote resource

### Key Points
- Provisioners are a last resort - prefer native provider features
- Run right after the resource is created by default
- `when = destroy` runs before the resource is destroyed
- `on_failure = continue` or `on_failure = fail`
- A failed creation-time provisioner taints the resource, so it is recreated on the next apply
- **[📖 Provisioners](https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax)** - Provisioner configuration

## Debugging and Troubleshooting

### TF_LOG Levels
- `TRACE` - Most verbose
- `DEBUG` - Debug information
- `INFO` - General information
- `WARN` - Warning messages
- `ERROR` - Error messages only

### Environment Variables
```bash
export TF_LOG=DEBUG
export TF_LOG_PATH=./terraform.log
export TF_LOG_CORE=TRACE
export TF_LOG_PROVIDER=DEBUG
```
- **[📖 Debugging Terraform](https://developer.hashicorp.com/terraform/internals/debugging)** - Debug logging

## Terraform Cloud and Enterprise

### Terraform Cloud Features
- Remote state management with encryption
- Remote plan and apply execution
- Team management and governance
- Policy as Code with Sentinel
- Private module registry
- VCS integration
- Cost estimation
- **[📖 Terraform Cloud](https://developer.hashicorp.com/terraform/cloud-docs)** - Terraform Cloud documentation

### Cloud Block Configuration
```hcl
terraform {
  cloud {
    organization = "my-org"
    workspaces {
      name = "my-workspace"
    }
  }
}
```

## Exam Tips

- 004 adds `depends_on` and `create_before_destroy`, custom conditions (variable validation, preconditions, postconditions, checks), ephemeral resources and write-only arguments, and HCP Terraform workspaces and projects. See the 004 notes before the exam.
- No weights are published for 004, so cover all eight objectives.

### High-Value Topics

HashiCorp publishes no weights for 004. The 003-era percentage list that used to be here was removed on 2026-11-07. Cover all eight objectives; new in 004 are 4f, 4g, 4h and 8c.

### Common Exam Traps
- Variable precedence order (command-line `-var` and `-var-file` win; environment variables sit just above the default)
- `terraform refresh` is deprecated - use `terraform plan -refresh-only`
- Provisioners are a last resort, not a best practice
- `count` and `for_each` cannot be used together on the same resource
- State locking requires backend support, and on S3 it is opt-in (`use_lockfile`; the DynamoDB table method is deprecated)
- `terraform.workspace` returns "default" in default workspace
- `-auto-approve` skips the interactive approval, not validation
- `terraform init` must be run when changing backend configuration
