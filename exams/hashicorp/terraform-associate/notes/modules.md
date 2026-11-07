# Modules

## Overview

This document covers Terraform modules including creation, usage, versioning, the module registry, and composition patterns. Modules are 004 objective 5 (HashiCorp publishes no weights) and are fundamental to building reusable, maintainable infrastructure configurations.

**[📖 Modules Overview](https://developer.hashicorp.com/terraform/language/modules)** - Module concepts and usage

## Module Concepts

### What is a Module?
- A container for multiple resources that are used together
- Every Terraform configuration is a module (the root module)
- Modules can call other modules (child modules)
- Enables code reuse, organization, and encapsulation
- Can be sourced from local directories, registries, or version control

### Root Module vs Child Module
- **Root module:** The main working directory where you run `terraform` commands
- **Child module:** A module called from within another module using a `module` block
- The root module can call multiple child modules
- Child modules can call their own child modules (nesting)

### Why Use Modules?
- **Reusability:** Write once, use across multiple projects
- **Organization:** Group related resources logically
- **Encapsulation:** Hide implementation details
- **Consistency:** Enforce standards across teams
- **Versioning:** Track and control module changes

## Module Structure

### Standard Module Layout
```
modules/
  my-module/
    main.tf           # Primary resource definitions
    variables.tf      # Input variable declarations
    outputs.tf        # Output value declarations
    README.md         # Documentation
    versions.tf       # Provider version constraints (optional)
    locals.tf         # Local values (optional)
    data.tf           # Data sources (optional)
```

### Minimal Module Example
```hcl
# modules/web-server/variables.tf
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI ID for the instance"
  type        = string
}

variable "name" {
  description = "Name tag for the instance"
  type        = string
}

# modules/web-server/main.tf
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = var.name
  }
}

# modules/web-server/outputs.tf
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

output "public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.web.public_ip
}
```

**[📖 Module Development](https://developer.hashicorp.com/terraform/language/modules/develop)** - Creating modules

## Module Sources

### Local Paths
```hcl
module "web" {
  source = "./modules/web-server"
  # ...
}
```
- Referenced with `./` or `../` prefix
- No version constraint (always uses current files)
- Terraform reads the module from the directory you name; run `terraform init` after adding a module call or changing a module `source`

### Terraform Registry
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  # ...
}
```
- Format: `<NAMESPACE>/<NAME>/<PROVIDER>`
- The `version` argument is optional for registry modules, but HashiCorp recommends constraining it to avoid unexpected changes
- Downloaded during `terraform init`
- Public registry: `registry.terraform.io`

**[📖 Terraform Registry](https://registry.terraform.io/browse/modules)** - Browse public modules

### GitHub
```hcl
module "vpc" {
  source = "github.com/hashicorp/example"
  # ...
}

# With specific ref (branch, tag, or commit)
module "vpc" {
  source = "github.com/hashicorp/example?ref=v1.0.0"
  # ...
}
```

### Generic Git Repository
```hcl
module "vpc" {
  source = "git::https://example.com/module.git?ref=v1.0.0"
  # ...
}

# SSH
module "vpc" {
  source = "git::ssh://git@example.com/module.git"
  # ...
}
```

### S3 Bucket
```hcl
module "vpc" {
  source = "s3::https://s3-eu-west-1.amazonaws.com/bucket/module.zip"
  # ...
}
```

### GCS Bucket
```hcl
module "vpc" {
  source = "gcs::https://www.googleapis.com/storage/v1/bucket/module.zip"
  # ...
}
```

**[📖 Module Sources](https://developer.hashicorp.com/terraform/language/modules/sources)** - All supported source types

## Module Inputs and Outputs

### Passing Inputs to Modules
```hcl
module "web" {
  source = "./modules/web-server"

  instance_type = "t3.small"
  ami_id        = "ami-12345678"
  name          = "production-web"
}
```

- Module inputs correspond to `variable` blocks in the child module
- Required variables must be provided by the calling module
- Default values are used when inputs are not specified

### Accessing Module Outputs
```hcl
# In root module, reference child module outputs
resource "aws_eip" "web" {
  instance = module.web.instance_id
}

output "web_ip" {
  value = module.web.public_ip
}
```

- Outputs from child modules are accessed via `module.<NAME>.<OUTPUT>`
- Only declared outputs are accessible (encapsulation)
- Outputs serve as the module's public interface

### Variable Scope
- Variables declared in a module are scoped to that module
- Child modules cannot access parent module variables directly
- Values must be explicitly passed through module arguments
- Outputs must be explicitly declared to be accessible from outside

**[📖 Module Inputs](https://developer.hashicorp.com/terraform/language/modules#accessing-module-output-values)** - Passing values to and from modules

## Module Versioning

### Version Constraints
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"      # Allows 5.x, not 6.0
}

module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = ">= 5.0, < 6.0"  # Explicit range
}

module "ec2" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "= 5.2.1"     # Exact version
}
```

- Version constraints only work with registry modules
- Local modules do not support version constraints
- Git sources use `?ref=` for version control
- Always pin versions in production environments

### Version Update Process
1. Update version constraint in module block
2. Run `terraform init -upgrade` to download new version
3. Run `terraform plan` to review changes
4. Apply if changes are acceptable

## Module Registry

### Public Registry
- URL: `registry.terraform.io`
- Thousands of community and verified modules
- Verified modules are maintained by HashiCorp partners
- Each module has documentation, inputs, outputs, and examples

### Private Registry
- Available in Terraform Cloud and Enterprise
- Host organization-specific modules
- Version control and access management
- Same source format as public registry

**[📖 Private Registry](https://developer.hashicorp.com/terraform/cloud-docs/registry)** - Terraform Cloud private registry

### Publishing to Public Registry
- Module must be in a public GitHub repository
- Repository name format: `terraform-<PROVIDER>-<NAME>`
- Must have standard module structure (main.tf, variables.tf, outputs.tf)
- Must use semantic versioning via Git tags
- Must have a README.md

**[📖 Publishing Modules](https://developer.hashicorp.com/terraform/registry/modules/publish)** - Publishing to the registry

## Module Composition

### Flat Modules
```hcl
# Single level of modules
module "vpc" { source = "./modules/vpc" }
module "web" { source = "./modules/web-server" }
module "db"  { source = "./modules/database" }
```

### Nested Modules
```hcl
# modules/app-stack/main.tf calls sub-modules
module "network" { source = "./modules/network" }
module "compute" { source = "./modules/compute" }
module "storage" { source = "./modules/storage" }
```

### Passing Providers to Modules
```hcl
module "web_west" {
  source = "./modules/web-server"

  providers = {
    aws = aws.west
  }
}
```

- Required when module needs a non-default provider
- Maps provider configuration from parent to child module

**[📖 Module Composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition)** - Design patterns for modules

## Module Best Practices

### Design Principles
- **Single responsibility:** Each module should do one thing well
- **Sensible defaults:** Minimize required inputs with good defaults
- **Documentation:** Document all variables and outputs
- **Validation:** Use `validation` blocks on input variables
- **Examples:** Include example configurations

### Anti-Patterns
- Wrapping a single resource in a module (unnecessary complexity)
- Deep nesting of modules (hard to debug and maintain)
- Hardcoding values inside modules (reduces reusability)
- Not pinning module versions (leads to unexpected changes)
- Exposing too many internal details through outputs

### Module Testing
- Use `terraform validate` to check syntax
- Use `terraform plan` to verify expected behavior
- Consider Terratest or Terraform's built-in testing framework
- Test with multiple input combinations

## Key Exam Points

### Must-Know Topics
- Module source formats: local, registry, GitHub, S3, GCS
- Version constraints work only with registry modules
- Variable scope - child modules cannot access parent variables directly
- Outputs are the public interface of a module
- `terraform init` downloads modules from remote sources
- `terraform init -upgrade` updates to newer module versions
- Module calls use `module.<NAME>.<OUTPUT>` for references
- The root module is always the working directory

### Common Exam Questions
- What is the correct source format for a Terraform Registry module?
- How do you access outputs from a child module?
- What happens when you change a module source and run terraform init?
- How are providers passed to child modules?
- What is the difference between local and registry module sources?
