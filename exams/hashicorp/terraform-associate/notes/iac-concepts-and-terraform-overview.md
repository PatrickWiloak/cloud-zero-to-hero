# IaC Concepts and Terraform Overview

## Overview

This document covers Infrastructure as Code (IaC) fundamentals and Terraform's purpose, architecture, and advantages. They map to 004 objective 1 (IaC with Terraform) and parts of objective 2. HashiCorp publishes no weights for 004.

**[📖 Introduction to Terraform](https://developer.hashicorp.com/terraform/intro)** - Official introduction to Terraform and IaC concepts

## Infrastructure as Code (IaC) Concepts

### What is Infrastructure as Code?
- Managing and provisioning infrastructure through machine-readable configuration files
- Replaces manual processes with automated, repeatable deployments
- Infrastructure is versioned, shared, and reused like application code
- Enables consistent environments across development, staging, and production

### Key IaC Principles
- **Declarative:** Describe the desired end state, not the steps to get there
- **Idempotent:** Running the same configuration multiple times produces the same result
- **Version Controlled:** Track changes to infrastructure in source control
- **Self-Documenting:** Configuration files serve as documentation of the infrastructure
- **Reproducible:** Same configuration produces identical environments every time

**[📖 Infrastructure as Code Tutorial](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/infrastructure-as-code)** - Hands-on IaC introduction

### Declarative vs Imperative

| Aspect | Declarative (Terraform) | Imperative (Scripts/Ansible) |
|--------|------------------------|------------------------------|
| Approach | Define desired state | Define step-by-step actions |
| Idempotency | Built-in | Must be implemented manually |
| State | Tracked automatically | Not tracked inherently |
| Readability | High - shows end state | Varies - shows process |
| Example | "There should be 3 servers" | "Create a server, then another, then another" |

### Benefits of IaC
- **Consistency:** Eliminate configuration drift and manual errors
- **Speed:** Deploy infrastructure in minutes instead of days
- **Collaboration:** Teams can review and approve infrastructure changes
- **Auditability:** Full history of who changed what and when
- **Reusability:** Modules and templates reduce duplication
- **Cost Reduction:** Automate teardown of unused resources
- **Disaster Recovery:** Quickly rebuild infrastructure from code

## Terraform Purpose and Architecture

### Why Terraform?
- **Provider agnostic:** Works with AWS, Azure, GCP, and the many providers in the Terraform Registry
- **State management:** Tracks real-world infrastructure state
- **Execution plans:** Preview changes before applying them
- **Resource graph:** Automatic dependency resolution and parallel execution
- **Modularity:** Reusable modules for common infrastructure patterns
- **Community:** Large ecosystem of providers and modules in the registry

**[📖 Terraform Use Cases](https://developer.hashicorp.com/terraform/intro/use-cases)** - Common Terraform scenarios

### Terraform Architecture
```
                    Terraform CLI
                         |
                  Terraform Core
                    /    |    \
              Provider  Provider  Provider
               (AWS)   (Azure)    (GCP)
                |        |         |
              AWS API  Azure API  GCP API
```

- **Terraform Core:** Reads configuration, manages state, builds resource graph
- **Providers:** Plugins that translate Terraform calls to API calls
- **State:** JSON file tracking managed infrastructure
- **Registry:** Repository of providers and modules

**[📖 Terraform Architecture](https://developer.hashicorp.com/terraform/plugin)** - Plugin-based architecture details

### Provider Plugin System
- Providers are distributed separately from Terraform core
- Downloaded during `terraform init`
- Each provider manages a specific set of resources and data sources
- Versioned independently from Terraform
- Can be sourced from HashiCorp, verified partners, or community

**[📖 Provider Documentation](https://developer.hashicorp.com/terraform/language/providers)** - Provider configuration and management

### Terraform Workflow
1. **Write:** Define infrastructure in HCL configuration files
2. **Plan:** Preview what Terraform will change (`terraform plan`)
3. **Apply:** Execute the changes to create/modify infrastructure (`terraform apply`)

This three-step workflow is the foundation of all Terraform operations.

**[📖 Terraform Workflow](https://developer.hashicorp.com/terraform/intro/core-workflow)** - The core Terraform workflow

## IaC Tool Comparison

### Terraform vs CloudFormation
| Feature | Terraform | CloudFormation |
|---------|-----------|----------------|
| Cloud Support | Multi-cloud | AWS only |
| Language | HCL | JSON/YAML |
| State | Managed externally | Managed by AWS |
| Drift Detection | Plan command | Stack drift detection |
| Rollback | Manual | Automatic |
| Learning Curve | Moderate | AWS-specific |

### Terraform vs Ansible
| Feature | Terraform | Ansible |
|---------|-----------|---------|
| Primary Use | Infrastructure provisioning | Configuration management |
| Approach | Declarative | Imperative/procedural |
| State | Yes (state file) | No (stateless) |
| Agents | Agentless | Agentless |
| Best For | Cloud infrastructure | Server configuration |

### Terraform vs Pulumi
| Feature | Terraform | Pulumi |
|---------|-----------|--------|
| Language | HCL (domain-specific) | Python, TypeScript, Go, etc. |
| State | Self-managed or Cloud | Pulumi Cloud or self-managed |
| Testing | Limited native testing | Full programming language testing |
| Learning Curve | Learn HCL | Use existing language skills |

## Terraform Editions

### Terraform Open Source (Community)
- Free and open source
- CLI-driven workflow
- Local or remote state management
- Full provider and module ecosystem

### Terraform Cloud
- SaaS offering with free tier
- Remote state management with encryption
- Remote plan and apply execution
- Team management and access controls
- Private module registry
- VCS integration (GitHub, GitLab, Bitbucket)
- Policy as Code with Sentinel or OPA

**[📖 Terraform Cloud](https://developer.hashicorp.com/terraform/cloud-docs)** - Cloud platform documentation

### Terraform Enterprise
- Self-hosted version of Terraform Cloud
- Air-gapped environment support
- Audit logging and SAML SSO
- Custom concurrency and SLA support

## Key Exam Concepts

### Must-Know for Objective 1 (IaC with Terraform)
- Definition and benefits of IaC
- Declarative vs imperative approaches
- Idempotency and reproducibility
- Version control integration
- How IaC reduces risk and increases speed

### Must-Know for Terraform's Purpose and Workflow
- Multi-cloud and provider-agnostic benefits
- Plugin-based architecture with providers
- State file purpose and importance
- Write-Plan-Apply workflow
- Terraform vs other IaC tools
- Terraform editions (OSS, Cloud, Enterprise)

## Practice Questions to Consider
- What are three benefits of Infrastructure as Code?
- How does Terraform differ from Ansible in its approach to infrastructure management?
- What is the purpose of the Terraform state file?
- Why is Terraform considered provider-agnostic?
- What happens during each phase of the Write-Plan-Apply workflow?
