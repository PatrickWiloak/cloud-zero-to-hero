# Providers and Resources

## Overview

This document covers Terraform providers, resource management, data sources, and dependency handling. Providers are the bridge between Terraform and cloud APIs, and understanding how they work is essential for the exam. This maps to 004 objectives 2 and 4 (no weights are published for 004).

**[📖 Providers Overview](https://developer.hashicorp.com/terraform/language/providers)** - Provider system documentation

## Providers

### What Are Providers?
- Plugins that enable Terraform to interact with cloud platforms and services
- Each provider offers resources and data sources for a specific platform
- Distributed separately from Terraform core
- Downloaded and cached during `terraform init`
- Examples: aws, azurerm, google, kubernetes, docker, vault

### Provider Configuration
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0, < 4.0"
    }
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = "production"
}
```

**[📖 Provider Configuration](https://developer.hashicorp.com/terraform/language/providers/configuration)** - Provider setup and authentication
**[📖 Provider Requirements](https://developer.hashicorp.com/terraform/language/providers/requirements)** - Required providers block syntax

### Provider Source Addresses
- Format: `<HOSTNAME>/<NAMESPACE>/<TYPE>`
- Default hostname: `registry.terraform.io`
- Examples:
  - `hashicorp/aws` (short for `registry.terraform.io/hashicorp/aws`)
  - `hashicorp/azurerm`
  - `hashicorp/google`
  - `integrations/github`

### Version Constraints
| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Exact version | `= 5.0.0` |
| `!=` | Not equal to | `!= 5.0.0` |
| `>` | Greater than | `> 5.0.0` |
| `>=` | Greater than or equal | `>= 5.0.0` |
| `<` | Less than | `< 6.0.0` |
| `<=` | Less than or equal | `<= 5.9.9` |
| `~>` | Pessimistic constraint | `~> 5.0` (allows 5.x, not 6.0) |

The `~>` operator is critical for the exam:
- `~> 5.0` allows `5.1`, `5.2`, ... but not `6.0`
- `~> 5.0.0` allows `5.0.1`, `5.0.2`, ... but not `5.1.0`
- Only the rightmost version component is allowed to increment

### Provider Aliases
```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

# Use default provider
resource "aws_instance" "east" {
  ami           = "ami-east-12345"
  instance_type = "t3.micro"
}

# Use aliased provider
resource "aws_instance" "west" {
  provider      = aws.west
  ami           = "ami-west-67890"
  instance_type = "t3.micro"
}
```

- Only one default (non-aliased) provider per type
- Aliased providers must be explicitly referenced
- Useful for multi-region or multi-account deployments

**[📖 Provider Aliases](https://developer.hashicorp.com/terraform/language/providers/configuration#alias-multiple-provider-configurations)** - Multiple provider configurations

### Dependency Lock File
- `.terraform.lock.hcl` is created during `terraform init`
- Records exact provider versions and checksums
- Should be committed to version control
- Ensures reproducible builds across team members
- Update with `terraform init -upgrade`

**[📖 Dependency Lock File](https://developer.hashicorp.com/terraform/language/files/dependency-lock)** - Lock file management

## Resources

### Resource Block Structure
```hcl
resource "<PROVIDER>_<TYPE>" "<LOCAL_NAME>" {
  argument1 = "value1"
  argument2 = "value2"

  nested_block {
    key = "value"
  }
}
```

- **Provider type prefix:** The part before the underscore (e.g., `aws` in `aws_instance`)
- **Resource type:** The full type name (e.g., `aws_instance`)
- **Local name:** Used only within the Terraform configuration for references
- **Arguments:** Configuration values you set
- **Attributes:** Values computed by the provider after creation

### Resource Behavior
| State | Config | Action |
|-------|--------|--------|
| Not in state | In config | Create |
| In state | Not in config | Destroy |
| In state | In config (changed, mutable) | Update in-place |
| In state | In config (changed, immutable) | Destroy and re-create |

**[📖 Resource Behavior](https://developer.hashicorp.com/terraform/language/resources/behavior)** - How Terraform manages resource lifecycle

### Meta-Arguments

#### depends_on
```hcl
resource "aws_instance" "web" {
  depends_on = [aws_iam_role_policy.web_policy]
  # ...
}
```
- Declares explicit dependencies
- Used when Terraform cannot infer the dependency automatically
- Takes a list of resource references

**[📖 depends_on](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on)** - Explicit dependencies

#### count
```hcl
resource "aws_instance" "web" {
  count         = var.create_instances ? 3 : 0
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  tags = { Name = "web-${count.index}" }
}
```
- Creates multiple instances of a resource
- `count.index` provides the current iteration number (0-based)
- Resources referenced as `aws_instance.web[0]`, `aws_instance.web[1]`, etc.
- Removing items from the middle causes renumbering and recreation

**[📖 count](https://developer.hashicorp.com/terraform/language/meta-arguments/count)** - Count meta-argument

#### for_each
```hcl
resource "aws_instance" "web" {
  for_each      = toset(["alpha", "beta", "gamma"])
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  tags = { Name = each.key }
}
```
- Creates instances from a map or set of strings
- `each.key` and `each.value` reference current item
- Resources referenced as `aws_instance.web["alpha"]`
- Safe for additions/removals (no renumbering)
- Cannot use `count` and `for_each` together

**[📖 for_each](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)** - For_each meta-argument

#### lifecycle
```hcl
resource "aws_instance" "web" {
  lifecycle {
    create_before_destroy = true   # Create replacement before destroying original
    prevent_destroy       = true   # Prevent accidental destruction
    ignore_changes        = [tags] # Ignore external tag changes
    replace_triggered_by  = [null_resource.trigger.id]
  }
}
```

**[📖 lifecycle](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)** - Lifecycle customization

### count vs for_each Decision Guide

| Criteria | count | for_each |
|----------|-------|----------|
| Resources are identical | Yes | Works but unnecessary |
| Resources have unique attributes | No (use index only) | Yes (use key/value) |
| Adding/removing items | Causes renumbering | Safe, no side effects |
| Conditional creation | `count = condition ? 1 : 0` | Use with filtered map |
| Data type | Number | Set or map |

## Data Sources

### Purpose
- Query existing infrastructure not managed by current configuration
- Read external data for use in resource configuration
- Terraform attempts to read them during planning; the read can be deferred to apply when an argument depends on a value not yet known

```hcl
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["main-vpc"]
  }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
  filter {
    name   = "tag:Tier"
    values = ["private"]
  }
}

resource "aws_instance" "web" {
  subnet_id = data.aws_subnets.private.ids[0]
  # ...
}
```

**[📖 Data Sources](https://developer.hashicorp.com/terraform/language/data-sources)** - Data source configuration

### Data Sources vs Resources
| Aspect | Resource | Data Source |
|--------|----------|-------------|
| Purpose | Create/manage infrastructure | Read existing infrastructure |
| State | Tracked in state file | Tracked in state file |
| Lifecycle | Create, update, destroy | Read-only, refreshed each plan |
| Reference | `<type>.<name>` | `data.<type>.<name>` |

## Dependency Management

### Implicit Dependencies
```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "web" {
  vpc_id     = aws_vpc.main.id  # Implicit dependency on VPC
  cidr_block = "10.0.1.0/24"
}
```
- Terraform automatically detects dependencies through attribute references
- Resources are created in dependency order
- Resources are destroyed in reverse dependency order

### Explicit Dependencies
```hcl
resource "aws_instance" "web" {
  depends_on = [aws_iam_role_policy.web_policy]
}
```
- Used when dependency exists but is not visible through attribute references
- Example: an instance needs an IAM policy but does not reference it directly

### Resource Graph
- Terraform builds a directed acyclic graph (DAG) of all resources
- Determines creation order based on dependencies
- Enables parallel creation of independent resources
- View with `terraform graph` (outputs DOT format)

**[📖 Resource Graph](https://developer.hashicorp.com/terraform/internals/graph)** - Dependency graph internals

## Key Exam Points

### Provider Topics
- Provider source address format and default registry
- Version constraint operators, especially `~>`
- Provider aliases for multi-region deployments
- Lock file purpose and management
- Provider download during `terraform init`

### Resource Topics
- Resource behavior: create, update, replace, destroy
- Meta-arguments: count, for_each, depends_on, lifecycle, provider
- count vs for_each: when to use each
- Implicit vs explicit dependencies
- Data sources vs resources
