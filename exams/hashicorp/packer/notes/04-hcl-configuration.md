# HCL2 Configuration

Packer's HCL2 configuration language is close to Terraform's HCL, with Packer-specific block types (`source`, `build`, `packer`) and a few different idioms.

## Block Types

- `packer {}`: CLI version and required_plugins
- `source "TYPE" "NAME" {}`: declares a builder instance
- `build {}`: references sources, declares provisioners and post-processors
- `variable "NAME" {}`: input variable
- `local "NAME" {}` or `locals { ... }`: computed values
- `data "TYPE" "NAME" {}`: data source

Unlike Terraform, Packer does not have `resource` blocks.

## The packer Block

```hcl
packer {
  required_version = ">= 1.10.0"

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

Only one `packer` block per configuration. Supports CLI version pinning and plugin requirements.

## Variable Declaration

```hcl
variable "region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for the build"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
  validation {
    condition     = contains(["t3.micro", "t3.small"], var.instance_type)
    error_message = "Only t3.micro and t3.small allowed."
  }
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "ami_regions" {
  type    = list(string)
  default = ["us-east-1", "us-west-2"]
}

variable "tags" {
  type = map(string)
  default = {
    Environment = "build"
    Team        = "platform"
  }
}
```

Variable attributes:

- `type`: `string`, `number`, `bool`, `list(X)`, `set(X)`, `map(X)`, `object({...})`, `tuple([...])`
- `default`: default value (optional; without it, variable becomes required)
- `description`: for docs and errors
- `sensitive`: redact from logs
- `validation`: condition + error_message

## Referencing Variables

```hcl
source "amazon-ebs" "ubuntu" {
  region        = var.region
  instance_type = var.instance_type
  tags          = var.tags
}
```

## Locals

For computed values that are reused:

```hcl
locals {
  timestamp      = formatdate("YYYYMMDD-hhmm", timestamp())
  base_name      = "ubuntu-${local.timestamp}"
  common_tags    = merge(var.tags, { BuildDate = local.timestamp })
  owner_alias    = "099720109477"
}

source "amazon-ebs" "ubuntu" {
  ami_name = local.base_name
  tags     = local.common_tags
}
```

Two equivalent syntaxes:

```hcl
local "my_value" {
  expression = "hello"
}

locals {
  my_value = "hello"
}
```

The `local` block form (with `expression`) also supports `sensitive = true` for computed sensitive values.

## Build Block

```hcl
build {
  name    = "ubuntu-base"
  sources = [
    "source.amazon-ebs.ubuntu-us",
    "source.amazon-ebs.ubuntu-eu",
  ]

  provisioner "shell" {
    inline = ["echo hello"]
  }

  post-processor "manifest" {
    output = "manifest.json"
  }
}
```

Multiple build blocks allowed. Use `-only` and `-except` on the build level (`packer build -only='ubuntu-base.*'`) or source level (`packer build -only='amazon-ebs.ubuntu-us'`).

## Functions

Packer HCL2 supports many functions similar to Terraform:

**Numeric:** `abs`, `ceil`, `floor`, `max`, `min`, `log`

**String:** `format`, `formatlist`, `join`, `split`, `replace`, `upper`, `lower`, `trimspace`, `regex`, `regex_replace`

**Collection:** `concat`, `contains`, `distinct`, `element`, `flatten`, `keys`, `values`, `length`, `lookup`, `merge`, `range`, `reverse`, `slice`, `sort`, `zipmap`

**Encoding:** `base64encode`, `base64decode`, `jsonencode`, `jsondecode`, `yamlencode`, `yamldecode`, `csvdecode`

**Filesystem:** `file`, `fileexists`, `fileset`, `filebase64`

**Date/Time:** `timestamp`, `formatdate`, `timeadd`

**Networking:** `cidrhost`, `cidrsubnet`, `cidrnetmask`

**Encoding/Hashing:** `md5`, `sha256`, `sha512`, `uuidv4`, `uuidv5`

**Other:** `env`, `can`, `try`, `coalesce`, `coalescelist`

### Examples

```hcl
locals {
  build_id    = formatdate("YYYYMMDD-hhmm", timestamp())
  config_file = file("${path.root}/config/app.conf")
  scripts     = fileset("${path.root}/scripts", "*.sh")
  api_key     = env("API_KEY")
  manifest    = jsondecode(file("${path.root}/manifest.json"))
}
```

### env() Function

Reads environment variables:

```hcl
variable "api_key" {
  default = env("API_KEY")
}
```

If the env var is unset, returns empty string. Combine with `coalesce` to provide defaults.

### path.root

The working directory where `packer build` was invoked. Use it in `file()` and `fileset()` calls for portability.

## Data Sources

Packer data sources let you query external systems at build time.

```hcl
data "amazon-ami" "ubuntu" {
  filters = {
    name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
    virtualization-type = "hvm"
    root-device-type    = "ebs"
  }
  owners      = ["099720109477"]
  most_recent = true
  region      = var.region
}

source "amazon-ebs" "ubuntu" {
  source_ami = data.amazon-ami.ubuntu.id
  # ...
}
```

Common data sources:

- `amazon-ami`: look up AMIs
- `amazon-secretsmanager`: read AWS Secrets Manager
- `amazon-parameterstore`: read SSM parameters
- `hcp-packer-artifact`: query HCP Packer for an artifact
- `http`: generic HTTP GET

Evaluate with `packer validate -evaluate-datasources .` (requires credentials).

## Variable Files

`.pkrvars.hcl` files provide variable values:

```hcl
# production.pkrvars.hcl
region        = "us-east-1"
instance_type = "t3.medium"
tags = {
  Environment = "production"
  Owner       = "platform"
}
```

Use on CLI:

```
packer build -var-file=production.pkrvars.hcl .
```

Files matching `*.auto.pkrvars.hcl` in the working directory are auto-loaded.

## Sensitive Values in Logs

Variables with `sensitive = true` are masked in logs. Example:

```hcl
variable "api_key" {
  type      = string
  sensitive = true
}

provisioner "shell" {
  environment_vars = ["API_KEY=${var.api_key}"]
  inline           = ["curl -H \"Authorization: $API_KEY\" https://api.example.com"]
}
```

Log output will show `****` instead of the key.

## Dynamic Blocks

Generate repetitive blocks from a variable:

```hcl
variable "launch_block_device_mappings" {
  type = list(object({
    device_name = string
    volume_size = number
    volume_type = string
  }))
  default = [
    { device_name = "/dev/sda1", volume_size = 20, volume_type = "gp3" },
    { device_name = "/dev/sdb",  volume_size = 100, volume_type = "gp3" },
  ]
}

source "amazon-ebs" "ubuntu" {
  # ...
  dynamic "launch_block_device_mappings" {
    for_each = var.launch_block_device_mappings
    content {
      device_name = launch_block_device_mappings.value.device_name
      volume_size = launch_block_device_mappings.value.volume_size
      volume_type = launch_block_device_mappings.value.volume_type
    }
  }
}
```

## Template Files

Use `templatefile()` to render a file with variable substitution:

```hcl
provisioner "file" {
  content     = templatefile("${path.root}/templates/app.conf.tpl", {
    region   = var.region
    port     = 8080
  })
  destination = "/tmp/app.conf"
}
```

## Migrating from Legacy JSON

Old `.json` templates use a different schema:

```json
{
  "variables": {"region": "us-east-1"},
  "builders": [{"type": "amazon-ebs", "region": "{{user `region`}}", ...}],
  "provisioners": [...]
}
```

Run `packer hcl2_upgrade template.json` to convert. Output: `template.json.pkr.hcl`. Review, test, then delete the JSON.

Notable differences:

- JSON uses `{{user `region`}}` interpolation; HCL2 uses `var.region`
- JSON arrays of builders become HCL2 `source` blocks
- JSON flat structure becomes HCL2 nested blocks
- HCL2 requires `required_plugins` declarations

## Comments

- Single-line: `# comment` or `// comment`
- Multi-line: `/* ... */`

## Common Configuration Mistakes

- Mixing JSON and HCL2 syntax in the same file
- Forgetting to quote block labels (`source amazon-ebs ubuntu` instead of `source "amazon-ebs" "ubuntu"`)
- Referencing a variable as `${var.region}` in HCL2 (redundant; just `var.region` works)
- Putting provisioner blocks outside a `build` block
- Using `default` inside a `local` (locals compute; use `variable` for defaults)

## Exam-Ready Checklist

- [ ] Can declare variables with all type constraints
- [ ] Know variable precedence (CLI > var-file > auto.pkrvars > env > default)
- [ ] Can use `locals` and functions effectively
- [ ] Know how to declare `required_plugins`
- [ ] Can write a data source query for AMI lookup
- [ ] Can convert a legacy JSON template to HCL2
- [ ] Know `sensitive = true` behavior
