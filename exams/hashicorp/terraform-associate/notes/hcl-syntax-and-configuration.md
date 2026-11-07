# HCL Syntax and Configuration

## Overview

This document covers the HashiCorp Configuration Language (HCL) syntax, configuration structure, variables, expressions, and functions. Understanding HCL is fundamental to 004 objective 4 (HashiCorp publishes no weights for 004).

**[📖 Configuration Language](https://developer.hashicorp.com/terraform/language)** - Complete HCL language reference

## Configuration File Structure

### File Organization
- Terraform reads all `.tf` files in the working directory
- File names are arbitrary but conventions exist:
  - `main.tf` - Primary resource definitions
  - `variables.tf` - Input variable declarations
  - `outputs.tf` - Output value declarations
  - `providers.tf` - Provider configuration
  - `terraform.tf` - Terraform settings block
  - `locals.tf` - Local value definitions
  - `data.tf` - Data source definitions
- `.tf.json` files are also valid (JSON format)
- Files are processed in alphabetical order but order generally does not matter

**[📖 Files and Directories](https://developer.hashicorp.com/terraform/language/files)** - File organization conventions

### Terraform Settings Block
```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "my-state-bucket"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
```

- `required_version` - Constrains which Terraform CLI versions can use this config
- `required_providers` - Specifies provider source and version constraints
- `backend` - Configures state storage location

**[📖 Terraform Settings](https://developer.hashicorp.com/terraform/language/block/terraform)** - Settings block reference

## Variables

### Input Variables
```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
  sensitive   = false

  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Instance type must be t3.micro, t3.small, or t3.medium."
  }
}
```

### Variable Types
- **Primitive:** `string`, `number`, `bool`
- **Collection:** `list(type)`, `set(type)`, `map(type)`
- **Structural:** `object({...})`, `tuple([...])`
- **Special:** `any` (accepts any type)

**[📖 Input Variables](https://developer.hashicorp.com/terraform/language/values/variables)** - Variable configuration reference

### Variable Precedence (lowest to highest)
1. Default values in `variable` block
2. `TF_VAR_<name>` environment variables
3. `terraform.tfvars` file (auto-loaded)
4. `terraform.tfvars.json` file (auto-loaded)
5. `*.auto.tfvars` and `*.auto.tfvars.json` files (auto-loaded, lexical order)
6. `-var` and `-var-file` command line options, in the order given (and variables set in HCP Terraform)

Later sources override earlier ones. Environment variables are the weakest source after the default: any variable file or command-line option overrides them. The exam may test this order.

### Output Values
```hcl
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app.id
  sensitive   = false
}

output "db_password" {
  description = "Database password"
  value       = aws_db_instance.main.password
  sensitive   = true
}
```

- Outputs are displayed after `terraform apply`
- Accessible via `terraform output` command
- Used to pass values between modules
- `sensitive = true` redacts value from CLI output (still in state)

**[📖 Output Values](https://developer.hashicorp.com/terraform/language/values/outputs)** - Output configuration reference

### Local Values
```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }

  name_prefix = "${var.project_name}-${var.environment}"
}
```

- Simplify configurations by naming expressions
- Computed once and referenced multiple times
- Cannot be overridden from outside the module
- Use `local.<name>` to reference (note: singular `local`, not `locals`)

**[📖 Local Values](https://developer.hashicorp.com/terraform/language/values/locals)** - Local values reference

## Expressions

### String Interpolation
```hcl
name = "web-${var.environment}-${count.index}"
```

### Conditional Expressions
```hcl
instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"
```

### For Expressions
```hcl
# List comprehension
upper_names = [for name in var.names : upper(name)]

# Map comprehension
instance_ids = { for instance in aws_instance.app : instance.tags.Name => instance.id }

# Filtering
prod_instances = [for i in var.instances : i if i.environment == "prod"]
```

**[📖 Expressions](https://developer.hashicorp.com/terraform/language/expressions)** - Expression types and syntax

### Dynamic Blocks
```hcl
resource "aws_security_group" "example" {
  name = "example"

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

- Generate repeated nested blocks dynamically
- Iterator defaults to the label of the dynamic block
- Can use custom iterator name with `iterator` argument

**[📖 Dynamic Blocks](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)** - Dynamic block syntax

## Built-in Functions

### String Functions
| Function | Example | Result |
|----------|---------|--------|
| `upper("hello")` | `upper("hello")` | `"HELLO"` |
| `lower("HELLO")` | `lower("HELLO")` | `"hello"` |
| `format("Hello, %s!", "world")` | | `"Hello, world!"` |
| `join("-", ["a", "b", "c"])` | | `"a-b-c"` |
| `split(",", "a,b,c")` | | `["a", "b", "c"]` |
| `replace("hello", "l", "L")` | | `"heLLo"` |
| `trimspace("  hello  ")` | | `"hello"` |
| `substr("hello", 0, 3)` | | `"hel"` |

### Collection Functions
| Function | Purpose |
|----------|---------|
| `length(list)` | Number of elements |
| `merge(map1, map2)` | Combine maps |
| `lookup(map, key, default)` | Map key lookup with default |
| `flatten(list)` | Flatten nested lists |
| `keys(map)` | Get map keys |
| `values(map)` | Get map values |
| `contains(list, value)` | Check list membership |
| `distinct(list)` | Remove duplicates |
| `element(list, index)` | Get element by index |
| `concat(list1, list2)` | Combine lists |

### Filesystem Functions
| Function | Purpose |
|----------|---------|
| `file(path)` | Read file contents |
| `fileexists(path)` | Check if file exists |
| `templatefile(path, vars)` | Render template with variables |
| `pathexpand(path)` | Expand ~ in path |
| `abspath(path)` | Convert to absolute path |

### Type Conversion Functions
| Function | Purpose |
|----------|---------|
| `tostring(value)` | Convert to string |
| `tonumber(value)` | Convert to number |
| `tobool(value)` | Convert to boolean |
| `tolist(value)` | Convert to list |
| `tomap(value)` | Convert to map |
| `toset(value)` | Convert to set |

**[📖 Built-in Functions](https://developer.hashicorp.com/terraform/language/functions)** - Complete function reference

## Resource Configuration

### Resource Syntax
```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.main.id

  tags = local.common_tags
}
```

- First label is resource type (provider_resource)
- Second label is local name (for referencing)
- Arguments configure the resource
- Attributes are computed values available after creation

### Meta-Arguments
```hcl
# count - create multiple identical resources
resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  tags = {
    Name = "web-${count.index}"
  }
}

# for_each - create resources from a map or set
resource "aws_instance" "web" {
  for_each      = toset(["web1", "web2", "web3"])
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  tags = {
    Name = each.key
  }
}
```

- `count` and `for_each` cannot be used together on the same resource
- `count` references: `aws_instance.web[0]`
- `for_each` references: `aws_instance.web["web1"]`

**[📖 Resources](https://developer.hashicorp.com/terraform/language/resources)** - Resource block reference

### Lifecycle Meta-Argument
```hcl
resource "aws_instance" "web" {
  # ...

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
    ignore_changes        = [tags]
    replace_triggered_by  = [null_resource.trigger.id]
  }
}
```

**[📖 Lifecycle Meta-Argument](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)** - Lifecycle customization

## Data Sources

### Data Source Syntax
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
}
```

- Read-only queries to existing infrastructure
- Populated during the plan phase
- Referenced with `data.<type>.<name>.<attribute>`

**[📖 Data Sources](https://developer.hashicorp.com/terraform/language/data-sources)** - Data source configuration

## Key Exam Points

### Common Exam Topics
- Variable precedence order (memorize this)
- Difference between `count` and `for_each`
- When to use `locals` vs `variables`
- Output values and their `sensitive` attribute
- Dynamic blocks for repeated nested configuration
- Data sources vs resources
- String interpolation syntax `${...}`
- The `~>` pessimistic version constraint

### Things That Catch People Off Guard
- `locals` block uses plural, but references use singular `local.name`
- `sensitive = true` on outputs only hides from CLI, value is still in state
- Variables without defaults are required and must be provided
- `terraform.tfvars` is auto-loaded, other `.tfvars` files are not (unless `*.auto.tfvars`)

## Key terms

- **Input variable** - a declared parameter that lets callers customise a configuration or module without editing its code.
- **Output value** - a named value a module or configuration exposes after apply for users or other modules to read.
- **Local value** - a named expression, declared in a `locals` block, that you reuse within a module.
- **Data source** - a read-only block that fetches information defined outside the current configuration.
- **`depends_on`** - a meta-argument that declares an explicit dependency Terraform cannot infer from references.
- **`count` and `for_each`** - meta-arguments that create multiple instances of a resource or module from one block.
- **Sensitive variable** - a variable marked `sensitive = true` so Terraform hides its value in plan and apply output.
