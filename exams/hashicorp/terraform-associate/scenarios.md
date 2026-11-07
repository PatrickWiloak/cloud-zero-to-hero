---
last-updated: 2026-11-07
---

# Terraform Associate (004) - High-Yield Scenarios and Patterns

## State Management Scenarios

### Remote State Migration
**Scenario:** Your team has been using local state for a Terraform project. Multiple engineers now need to collaborate, and you need to prevent concurrent modifications. How should you configure remote state with locking?

**Solution Pattern:**
- **Backend:** Configure S3 backend with DynamoDB table for locking
- **Migration:** Run `terraform init -migrate-state` to move state
- **Locking:** DynamoDB table provides automatic state locking
- **Encryption:** Enable server-side encryption on S3 bucket

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

**Common Distractors:**
- Using S3 alone without DynamoDB (wrong - S3 does not provide native state locking)
- Using `terraform state push` to migrate (wrong - use `terraform init -migrate-state`)
- Storing state in version control (wrong - state contains sensitive data, not suitable for VCS)
- Using `terraform init -reconfigure` for migration (wrong - this discards existing state)

### State Drift Detection
**Scenario:** You suspect someone manually modified an AWS security group that Terraform manages. How do you detect and reconcile the drift?

**Solution Pattern:**
- **Detection:** Run `terraform plan -refresh-only` to detect drift
- **Review:** Examine the proposed state changes
- **Reconcile:** Either apply the refresh to update state, or run `terraform apply` to revert to desired configuration
- **Prevention:** Implement policies to prevent manual changes

**Common Distractors:**
- Running `terraform refresh` directly (wrong - deprecated, use `plan -refresh-only`)
- Deleting and reimporting the resource (wrong - unnecessary and disruptive)
- Editing the state file manually (wrong - never edit state files directly)
- Running `terraform taint` on the resource (wrong - taint forces replacement, not reconciliation)

## Module Design Scenarios

### Reusable Multi-Environment Module
**Scenario:** You need to deploy the same infrastructure pattern across dev, staging, and production environments with different configurations for each.

**Solution Pattern:**
- **Module:** Create a reusable module with configurable variables
- **Environments:** Use separate variable files or workspaces
- **Versioning:** Pin module versions for stability
- **Outputs:** Export resource attributes for cross-module references

```hcl
module "app" {
  source = "./modules/app-stack"

  environment   = "production"
  instance_type = "t3.large"
  min_capacity  = 3
  max_capacity  = 10
  enable_waf    = true
}
```

**Common Distractors:**
- Duplicating entire configurations per environment (wrong - violates DRY principle)
- Using count on modules for environments (wrong - workspaces or separate module calls are cleaner)
- Hardcoding values inside modules (wrong - use variables for configurability)
- Using a single workspace for all environments (wrong - environments should be isolated)

### Module Source Selection
**Scenario:** Your organization wants to use a community VPC module but needs to ensure stability. The team wants to control which version is deployed and prevent unexpected breaking changes.

**Solution Pattern:**
- **Source:** Use Terraform Registry with version constraint
- **Constraint:** Use pessimistic version constraint `~>` for minor version flexibility
- **Lock file:** Commit `.terraform.lock.hcl` for reproducible builds
- **Review:** Check module changelog before upgrading

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  # Allows 5.x but not 6.0
}
```

**Common Distractors:**
- Using `latest` as version (wrong - no such syntax, and pins should be explicit)
- Omitting version constraint entirely (wrong - always latest could break builds)
- Copying module source into your repo (wrong - loses upstream updates and community fixes)
- Using exact version `= 5.0.0` always (wrong - misses bug fixes in patch versions)

## Workflow Scenarios

### Failed Apply Recovery
**Scenario:** A `terraform apply` partially completed before failing due to an API rate limit. Some resources were created, others were not. How do you recover?

**Solution Pattern:**
- **State:** Terraform automatically tracks partially created resources in state
- **Re-run:** Simply run `terraform apply` again
- **Idempotent:** Terraform will skip already-created resources and create remaining ones
- **Review:** Run `terraform plan` first to verify expected changes

**Common Distractors:**
- Running `terraform destroy` and starting over (wrong - destroys already-created resources unnecessarily)
- Manually deleting created resources (wrong - causes state drift)
- Editing state to remove failed resources (wrong - dangerous and unnecessary)
- Running `terraform init` again (wrong - init does not fix partial applies)

### Import Existing Infrastructure
**Scenario:** Your team manually created an RDS database in AWS. You need to bring it under Terraform management without downtime or recreation.

**Solution Pattern:**
- **Write config:** Create the resource block in Terraform configuration
- **Import:** Use import block or `terraform import` command
- **Verify:** Run `terraform plan` to ensure no changes detected
- **Adjust:** Modify configuration until plan shows no changes

```hcl
import {
  to = aws_db_instance.main
  id = "my-database-identifier"
}

resource "aws_db_instance" "main" {
  identifier     = "my-database-identifier"
  engine         = "mysql"
  instance_class = "db.t3.medium"
  # ... match existing configuration
}
```

**Common Distractors:**
- Import generates configuration automatically (wrong - you must write or generate-config-out the config)
- Import creates the resource in AWS (wrong - import only adds to state)
- Using `terraform state mv` to import (wrong - mv moves within state, not from external)
- Importing requires downtime (wrong - import is a state-only operation)

## Provider Configuration Scenarios

### Multi-Region Deployment
**Scenario:** You need to deploy resources in both us-east-1 and eu-west-1 using a single Terraform configuration.

**Solution Pattern:**
- **Aliases:** Configure provider aliases for each region
- **Resources:** Specify provider for each resource
- **Modules:** Pass provider configurations to modules using `providers` argument

```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "eu"
  region = "eu-west-1"
}

resource "aws_instance" "us_server" {
  ami           = "ami-0123456789"
  instance_type = "t3.micro"
}

resource "aws_instance" "eu_server" {
  provider      = aws.eu
  ami           = "ami-9876543210"
  instance_type = "t3.micro"
}
```

**Common Distractors:**
- Creating separate configurations per region (wrong - can use aliases in one config)
- Using variables for region in a single provider (wrong - only handles one region at a time)
- Using workspaces for multi-region (wrong - workspaces are for same config different state)
- Omitting the alias attribute (wrong - cannot have two default providers of same type)

### Provider Version Conflict
**Scenario:** After upgrading the AWS provider version, `terraform init` fails with a version constraint error from a module dependency.

**Solution Pattern:**
- **Diagnose:** Check the module's required_providers for version constraints
- **Resolve:** Update the module to a version compatible with the new provider
- **Lock file:** Delete `.terraform.lock.hcl` and re-run `terraform init`
- **Upgrade:** Use `terraform init -upgrade` to update provider versions

**Common Distractors:**
- Editing `.terraform.lock.hcl` manually (wrong - regenerate with init)
- Downgrading provider to match old module (wrong - better to update module)
- Removing the module entirely (wrong - unnecessary, just version mismatch)
- Using `-force` flag on init (wrong - no such flag exists)

## Workspace and Environment Scenarios

### Workspace-Based Environment Management
**Scenario:** You want to use Terraform workspaces to manage dev and prod environments with different instance sizes and counts.

**Solution Pattern:**
- **Workspaces:** Create dev and prod workspaces
- **Variables:** Use `terraform.workspace` to conditionally set values
- **Isolation:** Each workspace maintains separate state

```hcl
locals {
  instance_type = terraform.workspace == "prod" ? "t3.large" : "t3.micro"
  instance_count = terraform.workspace == "prod" ? 3 : 1
}

resource "aws_instance" "app" {
  count         = local.instance_count
  ami           = var.ami_id
  instance_type = local.instance_type

  tags = {
    Environment = terraform.workspace
  }
}
```

**Common Distractors:**
- Using workspaces with Terraform Cloud (wrong - Cloud workspaces work differently than CLI workspaces)
- Storing workspace state in the same file (wrong - each workspace has its own state)
- Deleting the default workspace (wrong - default workspace cannot be deleted)
- Using workspaces for entirely different infrastructure (wrong - intended for same config, different parameters)

## Key Decision Factors

### When to Use Which Approach
1. **Modules vs Workspaces:** Modules for reusable components, workspaces for environment isolation
2. **Count vs For_each:** Count for identical resources, for_each for resources with unique attributes
3. **Local vs Remote state:** Local for individual work, remote for team collaboration
4. **Import block vs CLI import:** Import block for bulk/declarative imports, CLI for one-off imports
5. **Provisioners vs native resources:** Always prefer native provider resources over provisioners

## 004 Additions

### Replacing a Resource Without Downtime
**Scenario:** Changing the name of a load balancer target group forces replacement. Terraform destroys the old one first, and the listener briefly has no target.

**Solution Pattern:**
- **Rule:** set `lifecycle { create_before_destroy = true }` so the new object exists before the old one is removed
- **Constraint:** the name must not collide while both exist, so use `name_prefix` where the resource supports it
- **Note:** Terraform propagates the rule to resources the replaced one depends on

### Rejecting a Bad Input Early
**Scenario:** Engineers sometimes pass an AMI for the wrong CPU architecture, and the failure appears late as a boot problem.

**Solution Pattern:**
- **Input format:** a `validation` block on the variable rejects values that do not start with `ami-`
- **Assumption about a data source:** a `precondition` in the resource's `lifecycle` block checks the architecture during planning
- **Result guarantee:** a `postcondition` on the data source checks the returned tags; use `self`
- **Non-blocking monitoring:** a `check` block warns without stopping the run

### Keeping a Database Password Out of State
**Scenario:** A security review finds the generated database password in the state file.

**Solution Pattern:**
- **Generate it as an `ephemeral` resource** (for example `ephemeral "random_password"`), which is not stored in state or plan files
- **Pass it to a write-only argument** such as `password_wo`, with `password_wo_version` to signal a rotation
- **Still protect state:** `sensitive = true` hides values from output but does not remove them from state

### Splitting a Monolith Across Teams in HCP Terraform
**Scenario:** One huge configuration is managed by three teams who block each other.

**Solution Pattern:**
- **Split** into networking, application and monitoring configurations, one workspace each
- **Group** the workspaces in a project and grant each team access at the project or workspace level
- **Connect** the application workspace to the networking workspace with a run trigger so it queues after a successful networking apply
