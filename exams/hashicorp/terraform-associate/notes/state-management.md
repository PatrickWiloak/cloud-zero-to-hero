# State Management

## Overview

This document covers Terraform state management including backends, locking, import, and state commands. State management accounts for 15% of the exam (Domain 7) and is one of the most critical topics, as state is the foundation of how Terraform tracks and manages infrastructure.

**[📖 State Overview](https://developer.hashicorp.com/terraform/language/state)** - Terraform state documentation

## Purpose of State

### Why Terraform Uses State
- **Resource mapping:** Maps configuration resources to real-world infrastructure objects
- **Metadata tracking:** Stores resource dependencies and provider information
- **Performance:** Caches resource attributes to avoid unnecessary API calls
- **Collaboration:** Enables teams to share infrastructure state

### State File Contents
- JSON format by default
- Contains:
  - Terraform version
  - Serial number (incremented on each change)
  - Resource instances with attributes
  - Provider configurations
  - Output values
  - Dependencies between resources

**[📖 Purpose of State](https://developer.hashicorp.com/terraform/language/state/purpose)** - Why state is needed

### Sensitive Data in State
- State files may contain sensitive data (passwords, keys, tokens)
- Local state is stored in plaintext JSON
- Always use remote backends with encryption for production
- Never commit state files to version control
- Use `sensitive = true` on outputs (hides from CLI but still in state)

**[📖 Sensitive Data in State](https://developer.hashicorp.com/terraform/language/state/sensitive-data)** - Handling sensitive state data

## Local State

### Default Behavior
- State stored in `terraform.tfstate` in the working directory
- Previous state saved as `terraform.tfstate.backup`
- No locking mechanism
- Suitable only for individual use, not team collaboration
- No encryption at rest

### Local Backend Configuration
```hcl
terraform {
  backend "local" {
    path = "relative/path/to/terraform.tfstate"
  }
}
```

## Remote Backends

### Why Remote Backends?
- **Collaboration:** Multiple team members can access shared state
- **Locking:** Prevent concurrent modifications
- **Encryption:** State encrypted at rest and in transit
- **Versioning:** State history and rollback capabilities
- **Security:** Centralized access control

### S3 Backend (AWS)
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "project/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

- State stored in S3 bucket
- Locking requires DynamoDB table (S3 alone does not provide locking)
- Server-side encryption with SSE-S3 or SSE-KMS
- Versioning recommended on the S3 bucket

**[📖 S3 Backend](https://developer.hashicorp.com/terraform/language/backend/s3)** - AWS S3 backend configuration

### GCS Backend (Google Cloud)
```hcl
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "project/state"
  }
}
```

- Built-in state locking
- Built-in encryption
- Object versioning support

### Azure Blob Backend
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstateaccount"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
```

- Built-in state locking via blob leases
- Built-in encryption

### Consul Backend
```hcl
terraform {
  backend "consul" {
    address = "consul.example.com:8500"
    scheme  = "https"
    path    = "full/path"
  }
}
```

- Built-in state locking
- Optional encryption

**[📖 Backend Configuration](https://developer.hashicorp.com/terraform/language/backend)** - Backend types and configuration
**[📖 Remote State](https://developer.hashicorp.com/terraform/language/state/remote)** - Remote state overview

### Terraform Cloud Backend
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

- Built-in locking, encryption, and versioning
- Remote execution capability
- Team access controls
- The `cloud` block replaces the older `remote` backend

**[📖 Terraform Cloud Configuration](https://developer.hashicorp.com/terraform/cli/cloud/settings)** - Cloud integration setup

### Backend Comparison

| Backend | Locking | Encryption | Notes |
|---------|---------|------------|-------|
| Local | No | No | Default, single user only |
| S3 | DynamoDB required | SSE (configurable) | Most common AWS backend |
| GCS | Built-in | Built-in | Most common GCP backend |
| Azure Blob | Built-in (blob lease) | Built-in | Most common Azure backend |
| Consul | Built-in | Optional | HashiCorp service |
| Terraform Cloud | Built-in | Built-in | Recommended for teams |

## State Locking

### How Locking Works
- Prevents concurrent state modifications
- Automatically acquired during operations that write state
- Automatically released when operation completes
- Prevents race conditions in team environments

### Locked Operations
- `terraform apply`
- `terraform destroy`
- `terraform plan` (acquires read lock)
- `terraform state` subcommands that modify state

### Force Unlock
```bash
terraform force-unlock <LOCK_ID>
```
- Use only when automatic unlock fails (e.g., process crash)
- Requires the lock ID from the error message
- Use with caution - could lead to state corruption if lock is legitimately held

**[📖 State Locking](https://developer.hashicorp.com/terraform/language/state/locking)** - State locking mechanism

## State Commands

### terraform state list
```bash
# List all resources in state
terraform state list

# Filter by resource type
terraform state list aws_instance

# Filter by module
terraform state list module.vpc
```

### terraform state show
```bash
# Show detailed information about a resource
terraform state show aws_instance.web

# Show a specific indexed resource
terraform state show 'aws_instance.web[0]'
```

### terraform state mv
```bash
# Rename a resource (update state without destroying/recreating)
terraform state mv aws_instance.old aws_instance.new

# Move resource into a module
terraform state mv aws_instance.web module.app.aws_instance.web

# Move between state files
terraform state mv -state-out=other.tfstate aws_instance.web aws_instance.web
```

### terraform state rm
```bash
# Remove resource from state (does not destroy the actual resource)
terraform state rm aws_instance.web

# Remove an indexed resource
terraform state rm 'aws_instance.web[0]'
```
- Resource continues to exist in the cloud
- Terraform no longer manages it
- Useful when moving resource management to another configuration

### terraform state pull / push
```bash
# Pull remote state to stdout
terraform state pull

# Push local state to remote backend
terraform state push terraform.tfstate
```

**[📖 State Commands](https://developer.hashicorp.com/terraform/cli/commands/state)** - State CLI reference

## Backend Migration

### Migrating Between Backends
```bash
# Change backend configuration in terraform block, then:
terraform init -migrate-state
```

- Terraform detects backend change during init
- Prompts to migrate existing state to new backend
- `-migrate-state` explicitly requests migration
- `-reconfigure` discards existing state (use with caution)

### Migration Scenarios
- **Local to S3:** Add S3 backend config, run `terraform init -migrate-state`
- **S3 to Terraform Cloud:** Change to cloud block, run `terraform init -migrate-state`
- **Backend to backend:** Update backend config, run `terraform init -migrate-state`

## Terraform Import

### CLI Import
```bash
terraform import aws_instance.web i-1234567890abcdef0
```

- Imports one resource at a time
- Requires corresponding resource block in configuration
- Does not generate configuration (you must write it)
- Resource ID format varies by resource type

**[📖 Import Command](https://developer.hashicorp.com/terraform/cli/import)** - Import CLI reference

### Import Block (Terraform 1.5+)
```hcl
import {
  to = aws_instance.web
  id = "i-1234567890abcdef0"
}
```

- Declarative approach to importing
- Can generate configuration with `terraform plan -generate-config-out=generated.tf`
- Supports multiple imports in a single operation
- Preview with `terraform plan`

**[📖 Import Block](https://developer.hashicorp.com/terraform/language/import)** - Import block configuration

### Import Key Points (Exam)
- Import only adds to state - does not create cloud resources
- Import does not automatically generate configuration
- Configuration must match the imported resource exactly
- Run `terraform plan` after import to verify no changes
- Import block is the modern approach (1.5+), CLI import is legacy

## Terraform Refresh

### Behavior
- Updates state to match real-world infrastructure
- Detects drift from manual changes
- Does not modify infrastructure
- **Deprecated as standalone command** - use `terraform plan -refresh-only`

```bash
# Modern approach
terraform plan -refresh-only
terraform apply -refresh-only
```

**[📖 Refresh Command](https://developer.hashicorp.com/terraform/cli/commands/refresh)** - Refresh behavior (deprecated)

### Remote State Data Source
```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "vpc/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "web" {
  subnet_id = data.terraform_remote_state.vpc.outputs.subnet_id
}
```

- Read output values from another Terraform state
- Enables cross-project references
- Read-only access to the remote state

**[📖 Remote State Data Source](https://developer.hashicorp.com/terraform/language/state/remote-state-data)** - Cross-project state references

## Key Exam Points

### High-Priority Topics
- S3 backend requires DynamoDB for locking (not S3 alone)
- `terraform refresh` is deprecated - use `plan -refresh-only`
- `terraform import` does not generate configuration
- State file contains sensitive data and must be secured
- `terraform state rm` removes from state but does not destroy resources
- `-migrate-state` vs `-reconfigure` during backend changes
- Remote state data source for cross-project references
- The `cloud` block replaces the `remote` backend for Terraform Cloud

## Key terms

- **State file** - the `terraform.tfstate` record that maps your configuration to the real infrastructure objects Terraform manages.
- **Remote backend** - a backend that stores state in a shared remote location such as S3 or HCP Terraform instead of on local disk.
- **State locking** - a backend feature that blocks concurrent operations so two runs cannot write the same state at once.
- **`terraform import`** - brings an existing real-world resource under Terraform management by writing it into state.
- **`terraform state rm`** - removes a resource from state without destroying the real infrastructure object.
- **Drift** - a difference between the real infrastructure and what the state and configuration describe.
- **Workspace** - a named, separate state instance that lets one configuration manage multiple environments.
