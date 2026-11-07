---
last-updated: 2026-11-07
difficulty: intermediate
---

# HashiCorp Terraform Associate (004) Certification

## Exam Overview

The HashiCorp Certified: Terraform Associate (004) exam proves foundational Terraform knowledge and skills. HashiCorp describes the audience as a cloud engineer with foundational Terraform knowledge who can identify Terraform Enterprise features and distinguish them from the Community edition. The exam covers infrastructure as code concepts, providers and state, the core workflow, configuration language, modules, state management, maintenance tasks and HCP Terraform.

**Version 004 replaces 003.** HashiCorp's 004 content list names the changes from 003: four new topics (4f lifecycle rules `depends_on` and `create_before_destroy`, 4g custom conditions, 4h ephemeral values and write-only arguments, 8c HCP Terraform workspaces and projects), a test version of Terraform 1.12, and HCP Terraform content. The pages read do not state a retirement date for 003, and the 003 guide's old "last day" date (reported in January 2026 by a search snippet) is not confirmed. If you hold a 003 certification, HashiCorp's renewal section describes your options.

**Exam Code:** Terraform Associate (004)
**Exam Duration:** 1 hour
**Assessment type:** Multiple choice
**Number of Questions:** Not verified (not on the HashiCorp page)
**Passing Score:** Not verified (not on the HashiCorp page)
**Format:** Online proctored
**Cost:** $70.50 USD, plus locally applicable taxes and fees; free retake not included
**Credential Expiration:** 2 years
**Language:** English
**Product version tested:** Terraform 1.12
**Prerequisites:** Basic terminal skills and an understanding of on-premises and cloud architecture. Professional experience is recommended, but you can prepare by practicing the objectives in a personal demo setup

Source (read 2026-11-07): **[📖 Terraform Associate (004) certification page](https://developer.hashicorp.com/certifications/terraform-associate)** - Exam details and objectives

## Exam Objectives

HashiCorp's 004 page lists eight objectives and publishes **no percentage weights**. (The weights that appeared on the 003 outline, such as 20 percent for "Terraform basics", do not apply to 004.) Study all eight; the notes below map to them.

| # | Objective | Sub-objectives | Study notes |
|---|-----------|----------------|-------------|
| 1 | Infrastructure as Code (IaC) with Terraform | 1a what IaC is; 1b advantages; 1c multi-cloud, hybrid cloud and service-agnostic workflows | [IaC concepts](notes/iac-concepts-and-terraform-overview.md) |
| 2 | Terraform fundamentals | 2a install and version providers; 2b how Terraform uses providers; 2c multiple providers; 2d how Terraform uses and manages state | [Providers and resources](notes/providers-and-resources.md), [State](notes/state-management.md) |
| 3 | Core Terraform workflow | 3a workflow; 3b init; 3c validate; 3d plan; 3e apply; 3f destroy; 3g fmt | [Core workflow](notes/core-workflow-and-advanced-features.md) |
| 4 | Terraform configuration | 4a resource and data blocks; 4b references; 4c variables and outputs; 4d complex types; 4e expressions and functions; **4f resource dependencies (`depends_on`, `create_before_destroy`)**; **4g custom conditions**; **4h sensitive data and secrets, including ephemeral values and Vault** | [HCL syntax](notes/hcl-syntax-and-configuration.md), [Dependencies, conditions and ephemeral values](notes/dependencies-conditions-and-ephemeral-values.md) |
| 5 | Terraform modules | 5a sources; 5b variable scope; 5c using modules; 5d versions | [Modules](notes/modules.md) |
| 6 | Terraform state management | 6a local backend; 6b locking; 6c remote state with the backend block; 6d drift and state | [State](notes/state-management.md) |
| 7 | Maintain infrastructure with Terraform | 7a import; 7b inspect state with the CLI; 7c verbose logging | [Core workflow](notes/core-workflow-and-advanced-features.md), [State](notes/state-management.md) |
| 8 | HCP Terraform | 8a create infrastructure; 8b collaboration and governance; **8c workspaces and projects**; 8d integration | [HCP Terraform](notes/hcp-terraform.md) |

Bold items are new in 004. **[📖 Associate exam content list (004)](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004)** - HashiCorp's objective-to-documentation mapping

### What 004 dropped from the 003 outline

The 004 objective list no longer names `terraform taint`/`replace`, CLI `terraform workspace` use cases, `terraform refresh`, remote state data sources or provisioners. Those topics remain valid Terraform knowledge and the notes still cover them, but they are no longer listed as objectives. `terraform refresh` is superseded by `terraform plan -refresh-only`; drift handling (6d) is the objective to study.

## Key Study Areas

### Terraform Configuration Language (HCL)
- **Resources:** Defining infrastructure components
- **Data Sources:** Querying existing infrastructure
- **Variables:** Input, output, and local values
- **Expressions:** Conditional logic, loops, and functions
- **Providers:** Cloud and service provider plugins
- **Provisioners:** Last-resort configuration management

### State Management
- **Local State:** Default file-based storage
- **Remote Backends:** S3, GCS, Azure Blob, Consul, Terraform Cloud
- **State Locking:** Preventing concurrent modifications
- **State Commands:** list, mv, rm, pull, push, import
- **Sensitive Data:** Managing secrets in state files

### Modules
- **Module Structure:** Root and child modules
- **Module Sources:** Local, registry, GitHub, S3
- **Module Registry:** Public and private registries
- **Module Versioning:** Constraining module versions
- **Module Composition:** Building reusable infrastructure patterns

### Core Workflow
- **terraform init:** Initialize working directory, download providers
- **terraform plan:** Preview changes before applying
- **terraform apply:** Execute infrastructure changes
- **terraform destroy:** Remove managed infrastructure
- **terraform fmt:** Format configuration files
- **terraform validate:** Check configuration syntax

### Advanced Features
- **Workspaces:** Managing multiple environments
- **Import:** Bringing existing resources under management
- **Debugging:** Using TF_LOG for troubleshooting
- **Provisioners:** local-exec and remote-exec
- **Dynamic Blocks:** Generating repeated nested blocks

## Hands-On Skills Required

### CLI Proficiency
- **terraform init:** Provider and module initialization
- **terraform plan/apply:** Infrastructure deployment
- **terraform state:** State manipulation commands
- **terraform workspace:** Environment management
- **terraform import:** Importing existing resources

### Configuration Writing
- **Resource definitions and data sources**
- **Variable declarations and type constraints**
- **Output values and expressions**
- **Module calls and composition**
- **Provider configuration and aliasing**

### Infrastructure Patterns
- **Multi-environment deployments (dev/staging/prod)**
- **Modular infrastructure design**
- **Remote state with locking**
- **Provider version constraints**
- **Resource dependency management**

## Study Tips

1. **Hands-On Practice:** Build real infrastructure with Terraform on any cloud provider
2. **Use Free Tiers:** Leverage AWS Free Tier or GCP credits for practice
3. **Read Documentation:** Study the official Terraform documentation thoroughly
4. **Write HCL:** Practice writing configurations from scratch, not just copying
5. **State Management:** Understand how state works - this is heavily tested
6. **Module Design:** Build and publish your own modules for practice
7. **Terraform Cloud:** Set up a free account and practice remote operations
8. **Practice Exams:** Take official HashiCorp practice exams

## Comprehensive Study Resources

### Quick Links (Terraform Associate Specific)
- **[Terraform Associate Exam Page](https://developer.hashicorp.com/certifications/terraform-associate)** - Registration and exam details
- **[Terraform Documentation](https://developer.hashicorp.com/terraform/docs)** - Complete Terraform documentation
- **[Terraform Tutorials](https://developer.hashicorp.com/terraform/tutorials)** - Official hands-on tutorials
- **[Terraform Registry](https://registry.terraform.io/)** - Providers, modules, and policies
- **[Terraform Associate Study Guide](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-study-004)** - Official study guide
- **[Terraform Exam Review](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004)** - Official exam review

### Recommended Courses
- HashiCorp Learn Terraform tutorials (free)
- Bryan Krausen - Terraform Associate on Udemy
- Andrew Brown - Terraform Associate on freeCodeCamp (free)
- KodeKloud Terraform for Beginners

### Practice Resources
- HashiCorp official practice exam
- Bryan Krausen practice tests on Udemy
- Tutorials Dojo Terraform practice exams
- Hands-on labs with Terraform Cloud free tier

## Exam Registration

Register through:
- **Online proctored exam:** book through the certification page (the proctoring vendor is not named on it; check the exam rules before booking)
- **HashiCorp Certification Portal:** [hashicorp.com/certifications](https://www.hashicorp.com/certifications)

## Exam Day Preparation

### Technical Setup (Online Exam)
- Stable internet connection
- Webcam and microphone
- Clean, quiet workspace
- Valid government-issued ID
- Proctoring software or secure browser the exam rules require (check HashiCorp's exam rules; the vendor is not named on the certification page)

### Exam Strategy
1. **Read questions carefully:** Pay attention to exact wording and keywords
2. **Eliminate wrong answers:** Use process of elimination
3. **Flag uncertain questions:** Review flagged questions at the end
4. **Time management:** the exam is 1 hour; keep time at the end to review flagged questions
5. **Practical thinking:** Apply hands-on experience to scenarios

### Common Question Types
- **Concept questions:** IaC benefits, Terraform purpose
- **Configuration questions:** HCL syntax, resource definitions
- **Workflow questions:** Correct command sequences
- **State questions:** Backend configuration, state management
- **Module questions:** Sources, versioning, composition

## Career Benefits

### Job Opportunities
- Cloud Infrastructure Engineer
- DevOps Engineer
- Site Reliability Engineer
- Platform Engineer
- Cloud Solutions Architect

### Professional Development
- Foundation for Terraform Authoring and Operations certifications
- Industry recognition for IaC skills
- Technical credibility with HashiCorp ecosystem
- Multi-cloud infrastructure management expertise

## Next Steps After Certification

### Advanced Certifications
- **Terraform Authoring Associate:** Advanced configuration and patterns
- **Vault Associate:** Secrets management and security
- **Consul Associate:** Service networking and discovery

### Continuous Learning
- Stay updated with new Terraform features and providers
- Contribute to Terraform providers and modules
- Practice multi-cloud infrastructure patterns
- Explore Terraform Cloud and Enterprise features
