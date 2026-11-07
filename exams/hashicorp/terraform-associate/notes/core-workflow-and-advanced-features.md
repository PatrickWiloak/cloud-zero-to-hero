# Core Workflow and Advanced Features

## Overview

This document covers the Terraform core workflow (init, plan, apply, destroy), workspaces, provisioners, debugging, and other advanced features. The core workflow is 004 objective 3 and maintenance tasks are objective 7 (HashiCorp publishes no weights for 004).

**[📖 Core Workflow](https://developer.hashicorp.com/terraform/intro/core-workflow)** - Write, Plan, Apply workflow

## Core Terraform Commands

### terraform init
Initializes the working directory for Terraform operations.

```bash
terraform init                    # Standard initialization
terraform init -upgrade           # Upgrade providers and modules
terraform init -reconfigure       # Reconfigure backend, ignore existing config (no state migration)
terraform init -migrate-state     # Migrate state to new backend
terraform init -backend=false     # Skip backend initialization
terraform init -input=false       # Disable interactive input
```

**What init does:**
- Downloads and installs providers into `.terraform/providers/`
- Downloads modules into `.terraform/modules/`
- Initializes the backend for state storage
- Creates `.terraform.lock.hcl` (dependency lock file)

**When to re-run init:**
- Adding or changing providers
- Adding or changing modules
- Changing backend configuration
- After `terraform init -upgrade` to get newer versions

**[📖 terraform init](https://developer.hashicorp.com/terraform/cli/commands/init)** - Init command reference

### terraform validate
Checks configuration syntax and internal consistency.

```bash
terraform validate               # Validate configuration
terraform validate -json         # Output in JSON format
```

**What validate checks:**
- HCL syntax errors
- Attribute names and types
- Required arguments
- Module references

**What validate does NOT check:**
- Provider credentials or API access
- Remote state accessibility
- Actual cloud resource availability
- Provider-specific validation

**[📖 terraform validate](https://developer.hashicorp.com/terraform/cli/commands/validate)** - Validate command reference

### terraform plan
Creates an execution plan showing what changes will be made.

```bash
terraform plan                    # Standard plan
terraform plan -out=plan.tfplan   # Save plan to file
terraform plan -destroy           # Plan a destroy operation
terraform plan -target=aws_instance.web  # Plan for specific resource
terraform plan -var="key=value"   # Pass variable
terraform plan -var-file=prod.tfvars  # Use variable file
terraform plan -refresh-only      # Only refresh state (no changes)
terraform plan -refresh=false     # Skip state refresh
terraform plan -parallelism=5     # Limit concurrent operations
terraform plan -generate-config-out=gen.tf  # Generate config for imports
```

**Plan output symbols:**
- `+` Create
- `-` Destroy
- `~` Update in-place
- `-/+` Destroy and recreate
- `<=` Read (data source; this symbol is not on the plan command page, unverified)

**[📖 terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)** - Plan command reference

### terraform apply
Executes the changes defined in the plan.

```bash
terraform apply                   # Apply with interactive approval
terraform apply -auto-approve     # Skip approval prompt
terraform apply plan.tfplan       # Apply a saved plan file
terraform apply -target=aws_instance.web  # Apply specific resource
terraform apply -var="key=value"  # Pass variable
terraform apply -parallelism=10   # Concurrent operations limit
terraform apply -replace=aws_instance.web  # Force replacement
```

**Key behaviors:**
- Generates a new plan if no saved plan file is provided
- Prompts for approval by default (unless `-auto-approve`)
- Updates state file after each resource operation
- Partially applied states are saved (operations are not transactional)

**[📖 terraform apply](https://developer.hashicorp.com/terraform/cli/commands/apply)** - Apply command reference

### terraform destroy
Destroys all resources managed by the current configuration.

```bash
terraform destroy                 # Destroy with interactive approval
terraform destroy -auto-approve   # Skip approval prompt
terraform destroy -target=aws_instance.web  # Destroy specific resource
```

- Equivalent to `terraform apply -destroy`
- Destroys resources in reverse dependency order
- Updates state file to reflect destroyed resources
- Only destroys resources tracked in the current state

**[📖 terraform destroy](https://developer.hashicorp.com/terraform/cli/commands/destroy)** - Destroy command reference

### terraform fmt
Formats configuration files to canonical style.

```bash
terraform fmt                     # Format current directory
terraform fmt -recursive          # Format subdirectories too
terraform fmt -check              # Check formatting (exit code 0 if formatted)
terraform fmt -diff               # Show formatting differences
```

**[📖 terraform fmt](https://developer.hashicorp.com/terraform/cli/commands/fmt)** - Format command reference

### terraform show
Displays the current state or a saved plan.

```bash
terraform show                    # Show current state
terraform show plan.tfplan        # Show saved plan
terraform show -json              # Output in JSON format
```

### terraform output
Displays output values from state.

```bash
terraform output                  # Show all outputs
terraform output instance_id      # Show specific output
terraform output -json            # JSON format
terraform output -raw instance_id # Raw value (no quotes)
```

### terraform graph
Generates a visual representation of the dependency graph.

```bash
terraform graph                   # Output DOT format
terraform graph | dot -Tpng > graph.png  # Generate image (requires graphviz)
```

## Workspaces

### Concept
- Workspaces provide separate state files for the same configuration
- Each workspace has its own state, enabling environment isolation
- Default workspace is named "default" and cannot be deleted

### Commands
```bash
terraform workspace list          # List all workspaces
terraform workspace new dev       # Create new workspace
terraform workspace select dev    # Switch to workspace
terraform workspace delete dev    # Delete workspace
terraform workspace show          # Show current workspace
```

### Using Workspaces in Configuration
```hcl
resource "aws_instance" "web" {
  instance_type = terraform.workspace == "prod" ? "t3.large" : "t3.micro"

  tags = {
    Environment = terraform.workspace
  }
}
```

### State File Location
- Default workspace: `terraform.tfstate`
- Named workspaces: the local backend keeps them in a separate directory (in a directory called `terraform.tfstate.d`, per the [workspaces page](https://developer.hashicorp.com/terraform/cli/workspaces))

### CLI Workspaces vs Terraform Cloud Workspaces
| Feature | CLI Workspaces | Cloud Workspaces |
|---------|---------------|-----------------|
| State isolation | Yes | Yes |
| Variable sets | No (use terraform.workspace) | Yes (per-workspace variables) |
| Access control | No | Yes (team permissions) |
| Remote execution | No | Yes |
| VCS integration | No | Yes |

**[📖 Workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)** - Workspace management

### Workspace Limitations
- Not ideal for entirely different infrastructure sets
- Better suited for same config with different parameters
- No built-in variable management per workspace (use conditionals)
- For complex multi-environment setups, consider separate directories or Terraform Cloud

## Provisioners

### What Are Provisioners?
- Execute scripts or commands on local or remote machines
- Used for bootstrapping, configuration, or cleanup
- Considered a last resort by HashiCorp

### local-exec
```hcl
resource "aws_instance" "web" {
  # ...

  provisioner "local-exec" {
    command = "echo ${self.public_ip} >> ip_addresses.txt"
  }
}
```
- Runs on the machine where Terraform is executed
- Access to `self` for resource attributes
- Common use: trigger scripts, update files, call APIs

### remote-exec
```hcl
resource "aws_instance" "web" {
  # ...

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx"
    ]
  }
}
```
- Runs on the remote resource
- Requires `connection` block (SSH or WinRM)
- Supports `inline`, `script`, and `scripts` arguments

### file Provisioner
```hcl
provisioner "file" {
  source      = "conf/app.conf"
  destination = "/etc/app.conf"
}
```
- Copies files from local to remote machine
- Requires `connection` block

**[📖 Provisioners](https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax)** - Provisioner reference

### Provisioner Behavior
- Run only during resource creation by default
- `when = destroy` runs during resource destruction
- `on_failure = continue` allows Terraform to continue on failure
- `on_failure = fail` (default) stops execution on failure
- A failed creation-time provisioner taints the resource, so it is destroyed and recreated on the next apply
- HashiCorp recommends using cloud-init, user_data, or configuration management tools instead

### Why Provisioners Are a Last Resort
- Not captured in the plan
- Cannot be previewed
- Make configurations less predictable
- Break the declarative model
- Prefer: `user_data`, cloud-init, Packer, Ansible, Chef, Puppet

## Debugging and Troubleshooting

### TF_LOG Environment Variable
```bash
export TF_LOG=TRACE       # Most verbose
export TF_LOG=DEBUG       # Debug level
export TF_LOG=INFO        # Informational
export TF_LOG=WARN        # Warnings only
export TF_LOG=ERROR       # Errors only
```

### Log Output
```bash
export TF_LOG_PATH=./terraform.log    # Write logs to file
export TF_LOG_CORE=TRACE              # Core-specific logging
export TF_LOG_PROVIDER=DEBUG          # Provider-specific logging
```

- `TF_LOG` must be set for any logging to be enabled (`TF_LOG_PATH` alone does nothing); how to switch logging off again is not covered on the debugging page
- `TF_LOG_CORE` and `TF_LOG_PROVIDER` take the same levels as `TF_LOG` but only activate a subset of the logs (Terraform core or provider plugins)
- Log files are useful for debugging provider issues and plan failures

**[📖 Debugging](https://developer.hashicorp.com/terraform/internals/debugging)** - Debugging Terraform

### Common Errors and Solutions
| Error | Cause | Solution |
|-------|-------|----------|
| Provider not found | Missing required_providers | Add provider to terraform block |
| Backend initialization required | Changed backend config | Run `terraform init` |
| State lock error | Concurrent operation | Wait or `force-unlock` |
| Resource not found | Resource deleted externally | Run `terraform plan -refresh-only` |
| Cycle detected | Circular dependencies | Remove circular `depends_on` |

## Terraform Replace (formerly taint)

### terraform taint (Deprecated)
```bash
# Legacy approach
terraform taint aws_instance.web
terraform apply  # Will destroy and recreate
```

### terraform apply -replace (Recommended)
```bash
# Modern approach
terraform apply -replace=aws_instance.web
```

- Forces recreation of a specific resource
- `-replace` is preferred over `taint` (taint is deprecated)
- Useful when a resource is in a bad state but attributes have not changed

### terraform untaint
```bash
terraform untaint aws_instance.web
```
- Removes the tainted flag from a resource
- Prevents forced recreation

## Key Exam Points

### Core Workflow
- `terraform init` must run before any other command
- `terraform validate` does not check provider credentials
- `terraform plan -out` saves plan for exact apply later
- `terraform apply` with saved plan does not prompt for approval
- `terraform destroy` only affects resources in current state
- Plan symbols: `+` create, `-` destroy, `~` update, `-/+` replace

### Advanced Features
- Workspaces share configuration but have separate state
- Default workspace cannot be deleted
- CLI workspaces differ from Terraform Cloud workspaces
- Provisioners are a last resort - always prefer native alternatives
- `TF_LOG=TRACE` is the most verbose logging level
- `terraform apply -replace` replaces `terraform taint`
- `terraform plan -refresh-only` replaces `terraform refresh`

## Key terms

- **`terraform init`** - prepares a working directory by installing providers and modules and configuring the backend.
- **`terraform plan`** - compares configuration, state and real infrastructure and shows the changes Terraform would make.
- **`terraform apply`** - carries out the planned changes to create, update or destroy infrastructure.
- **`terraform validate`** - checks that the configuration is syntactically valid and internally consistent without contacting remote services.
- **Provisioner** - a block that runs a script on a local or remote machine as part of resource creation or destruction, and is a last resort.
- **Sentinel** - HashiCorp's policy-as-code framework used in HCP Terraform to enforce rules on runs.
