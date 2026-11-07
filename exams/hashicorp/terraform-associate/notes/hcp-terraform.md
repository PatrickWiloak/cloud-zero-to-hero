---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 20 min
---

# HCP Terraform (objective 8)

## Overview

Objective 8 of the 004 exam is HCP Terraform, HashiCorp's managed service for running Terraform with shared state, remote runs, access control and governance. It has four sub-objectives: **8a** use HCP Terraform to create infrastructure, **8b** describe collaboration and governance features, **8c** describe how to organize and use workspaces and projects (new in 004), and **8d** configure and use HCP Terraform integration. For depth beyond the Associate level, see the [Terraform Authoring and Operations notes on HCP Terraform](../../terraform-authoring-operations-pro/README.md).

**[📖 Associate exam content list (004)](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004)** - The documentation HashiCorp maps to each 8x objective

## 8a: Creating infrastructure with HCP Terraform

HCP Terraform manages each collection of infrastructure as a **workspace**. HashiCorp's documentation states the contrast with local Terraform: where the CLI uses a persistent working directory with configuration, state and variables, HCP Terraform stores those in the workspace, and "separate workspaces function like completely separate working directories."

| Component | Local Terraform | HCP Terraform |
|-----------|-----------------|---------------|
| Configuration | On disk | In a linked version control repository, or uploaded via API/CLI |
| Variable values | `.tfvars`, CLI arguments, environment | In the workspace |
| State | On disk or a remote backend | In the workspace |
| Credentials and secrets | Shell environment or prompts | In the workspace, as sensitive variables |

HCP Terraform also keeps **state versions** (backups of previous state) and **run history** (summaries, logs, what triggered the run, comments). With **remote operations** enabled, which is the default, plans and applies run on HCP Terraform's own disposable virtual machines using the workspace's configuration, variables and state. You can create workspaces through the UI, the API or the CLI integration, and can import existing resources into a workspace.

**[📖 Workspaces](https://developer.hashicorp.com/terraform/cloud-docs/workspaces)** - What a workspace contains and how runs work

## 8b: Collaboration and governance

The 004 content list maps this objective to these capabilities: the private registry, change requests, policy enforcement, projects, health assessments, teams, dynamic provider credentials, drift detection and variable sets.

- **Policy enforcement** checks plans against rules (Sentinel or OPA) before apply, so a non-compliant plan cannot proceed.
- **Teams and permissions** grant users and groups specific access to workspaces and projects.
- **Private registry** shares approved modules and providers within an organization.
- **Health assessments** include **drift detection** (does real infrastructure still match configuration) and **continuous validation** (do the custom conditions in your configuration still pass after provisioning). The documentation notes health assessments require the Standard or Premium edition.
- **Dynamic provider credentials** let runs authenticate to cloud providers with short-lived credentials rather than stored long-lived keys.
- **Variable sets** define variables once and reuse them across workspaces (and Stacks).

## 8c: Workspaces and projects

Do not confuse the two kinds of workspace. HashiCorp's documentation: HCP Terraform workspaces **are required**, hold an entire collection of infrastructure and are a major component of role-based access. **Terraform CLI workspaces** are tied to a working directory and let one configuration keep several state files; the CLI does not require you to create them.

HashiCorp recommends breaking a monolithic configuration into smaller ones, each with its own workspace, so teams can change components in parallel and permissions can be delegated. Its example is separate `networking-prod`, `app1-prod` and `monitoring-prod` workspaces, with the same code reused for `app1-dev`.

A **project** is "a folder containing one or more workspaces, Stacks, or both." Projects organize workspaces into groups and let you assign **project permissions** to teams, scoping access to collections of workspaces by business unit or responsibility. Workspaces created in a project inherit its **tags**. A project name must be unique within the organization.

**Run triggers** connect workspaces: a workspace can designate up to 20 **source workspaces**, and a successful apply in any of them automatically queues a run in the dependent workspace. Use them when one workspace reads infrastructure produced by another, so the dependency is explicit.

**[📖 Manage projects](https://developer.hashicorp.com/terraform/cloud-docs/projects/manage)** - Creating projects, tags and team access
**[📖 Run triggers](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/run-triggers)** - Connecting source workspaces
**[📖 Manage variables and variable sets](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/variables/managing-variables)** - Reusing variables across workspaces

## 8d: Integration with the CLI and state

The CLI talks to HCP Terraform through a `cloud` block in the `terraform` settings, after you authenticate with `terraform login`.

```hcl
terraform {
  cloud {
    organization = "example-org"

    workspaces {
      name = "app1-prod"
    }
  }
}
```

After `terraform login` and `terraform init`, `terraform plan` and `terraform apply` run remotely and stream output to your terminal. Moving existing local state to HCP Terraform is done by adding the `cloud` block and running `terraform init`, which offers to migrate the state. The content list maps 8d to the CLI login command, remote operations and migrating state to HCP Terraform.

## Common exam traps

- HCP Terraform workspaces and CLI workspaces are different things; only the first is required.
- A project groups workspaces and carries team permissions and tags; it is not a Terraform configuration unit.
- Run triggers start a run after a *successful apply* in a source workspace.
- Drift detection and continuous validation belong to health assessments, which depend on the edition.

## Key terms

- **HCP Terraform** - HashiCorp's managed service that runs Terraform with shared state, remote operations, access control and governance.
- **HCP Terraform workspace** - the required unit holding the configuration, variables, state and run history for one collection of infrastructure.
- **CLI workspace** - a named state file within a single working directory, used to reuse one configuration for several environments.
- **Remote operations** - plan and apply runs executed on HCP Terraform's own infrastructure rather than the local machine.
- **Project** - a folder in HCP Terraform that groups workspaces and Stacks and scopes team permissions and tags.
- **Run trigger** - a connection that queues a run in one workspace after a successful apply in a source workspace.
- **Variable set** - a reusable group of variables applied to multiple workspaces.
- **Health assessment** - HCP Terraform checks that include drift detection and continuous validation.
- **Dynamic provider credentials** - short-lived credentials HCP Terraform generates for a run instead of stored static keys.
- **Private registry** - an organization's own catalog of approved modules and providers.
