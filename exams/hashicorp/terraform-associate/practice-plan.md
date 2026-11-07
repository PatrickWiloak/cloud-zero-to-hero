---
last-updated: 2026-11-07
---

# HashiCorp Terraform Associate (004) Study Plan

## 6-Week Intensive Study Schedule

### Phase 1: Foundation Building (Weeks 1-2)

#### Week 1: IaC Concepts and Terraform Fundamentals
**Focus:** Core IaC concepts, Terraform purpose, and basic setup

#### Day 1-2: Infrastructure as Code Fundamentals
- [ ] Study IaC concepts: declarative vs imperative, idempotency
- [ ] Compare Terraform with CloudFormation, Ansible, Pulumi
- [ ] Read Terraform introduction and use cases documentation
- [ ] Install Terraform CLI and configure editor (VS Code + Terraform extension)
- [ ] **Lab:** Write your first Terraform configuration (local file resource)

#### Day 3-4: Terraform Purpose and Architecture
- [ ] Study Terraform plugin-based architecture
- [ ] Understand provider ecosystem and registry
- [ ] Learn the Write-Plan-Apply workflow
- [ ] Study multi-cloud and provider-agnostic benefits
- [ ] **Practice:** Initialize a project with AWS/GCP/Azure provider

#### Day 5-7: HCL Syntax Basics
- [ ] Study HCL block types: terraform, provider, resource, data
- [ ] Learn variable types: string, number, bool, list, map, object
- [ ] Practice output values and local values
- [ ] Understand type constraints and validation
- [ ] **Lab:** Create configuration with variables, outputs, and data sources

### Week 2: Resources, Providers, and Dependencies

#### Day 1-2: Providers Deep Dive
- [ ] Study provider configuration and authentication
- [ ] Learn version constraints: =, !=, >, >=, <, <=, ~>
- [ ] Understand provider aliases for multi-region deployments
- [ ] Practice required_providers block configuration
- [ ] **Practice:** Configure multiple provider instances with aliases

#### Day 3-4: Resources and Data Sources
- [ ] Study resource arguments, attributes, and meta-arguments
- [ ] Learn count, for_each, depends_on, lifecycle meta-arguments
- [ ] Practice data source queries for existing infrastructure
- [ ] Understand resource behavior: create, update, destroy, replace
- [ ] **Lab:** Deploy multi-resource infrastructure with dependencies

#### Day 5-7: Expressions and Functions
- [ ] Study conditional expressions and ternary operators
- [ ] Learn for expressions and dynamic blocks
- [ ] Practice string, collection, and numeric functions
- [ ] Understand templatefile and file functions
- [ ] **Practice:** Write configurations using complex expressions

### Phase 2: Core Skills (Weeks 3-4)

#### Week 3: Core Workflow and State Management

#### Day 1-2: Core Terraform Workflow
- [ ] Master terraform init: providers, backends, modules
- [ ] Study terraform validate vs terraform fmt
- [ ] Deep dive into terraform plan: flags, saved plans, targeting
- [ ] Master terraform apply: auto-approve, targeting, parallelism
- [ ] **Lab:** Practice full workflow with plan file saving and applying

#### Day 3-4: State Management Fundamentals
- [ ] Study state file purpose, format, and contents
- [ ] Learn local vs remote state storage
- [ ] Understand state locking mechanism
- [ ] Practice state commands: list, show, mv, rm
- [ ] **Practice:** Manipulate state with terraform state commands

#### Day 5-7: Remote Backends
- [ ] Configure S3 backend with DynamoDB locking
- [ ] Study Terraform Cloud backend configuration
- [ ] Learn backend authentication methods
- [ ] Practice backend migration with terraform init -migrate-state
- [ ] **Lab:** Migrate from local to remote backend (S3 or Terraform Cloud)

### Week 4: Modules and Advanced Features

#### Day 1-2: Module Basics
- [ ] Study module structure: main.tf, variables.tf, outputs.tf
- [ ] Learn module sources: local, registry, GitHub, S3
- [ ] Understand module inputs and outputs
- [ ] Practice variable scope within modules
- [ ] **Lab:** Create a reusable VPC module with inputs and outputs

#### Day 3-4: Module Registry and Versioning
- [ ] Explore Terraform Registry modules
- [ ] Study module version constraints
- [ ] Learn private registry publishing
- [ ] Practice using published modules with version pinning
- [ ] **Practice:** Deploy infrastructure using registry modules

#### Day 5-7: Advanced Terraform Features
- [ ] Study workspaces for multi-environment management
- [ ] Learn terraform import for existing resources
- [ ] Practice import blocks (Terraform 1.5+)
- [ ] Study provisioners: local-exec, remote-exec, file
- [ ] **Lab:** Import existing resources and manage with workspaces

### Phase 3: Exam Preparation (Weeks 5-6)

#### Week 5: Deep Dive and Practice

#### Day 1-2: Debugging and Troubleshooting
- [ ] Study TF_LOG levels: TRACE, DEBUG, INFO, WARN, ERROR
- [ ] Practice TF_LOG_PATH for log file output
- [ ] Learn common error messages and resolutions
- [ ] Study terraform plan output interpretation
- [ ] **Practice:** Debug a broken configuration using TF_LOG

#### Day 3-4: HCP Terraform (objective 8)
- [ ] Read [the HCP Terraform note](notes/hcp-terraform.md): workspaces vs CLI workspaces, projects, run triggers, variable sets
- [ ] Read [the 004 additions note](notes/dependencies-conditions-and-ephemeral-values.md)

#### Day 3-4 (continued): Terraform Cloud hands-on
- [ ] Set up Terraform Cloud free account
- [ ] Study remote execution and state management
- [ ] Learn team management and governance features
- [ ] Understand Sentinel policy as code concepts
- [ ] **Lab:** Run plan and apply through Terraform Cloud

#### Day 5-7: Practice Exam Round 1
- [ ] Take HashiCorp official practice exam
- [ ] Review all incorrect answers thoroughly
- [ ] Identify knowledge gaps by domain
- [ ] Re-study weak areas based on results
- [ ] **Review:** Create summary notes for weak areas

### Week 6: Final Review and Exam

#### Day 1-2: Gap Analysis and Review
- [ ] Review objective 4 (Terraform configuration), the largest list of sub-objectives, including the 004 additions (dependencies and lifecycle rules, custom conditions, ephemeral values)
- [ ] Review objectives 1 to 3 (IaC, fundamentals, core workflow)
- [ ] Practice state management scenarios
- [ ] Review module composition patterns
- [ ] **Practice:** Write configurations from memory

#### Day 3-4: Practice Exam Round 2
- [ ] Take second practice exam (Bryan Krausen or Tutorials Dojo)
- [ ] Target 80%+ score before scheduling real exam
- [ ] Review all flagged questions
- [ ] Focus on command flags and exact syntax
- [ ] **Review:** Final review of fact sheet and notes

#### Day 5: Exam Day Preparation
- [ ] Light review of key concepts only
- [ ] Review variable precedence order
- [ ] Review state locking backends table
- [ ] Review terraform commands and key flags
- [ ] Verify PSI system requirements and test connection
- [ ] **Prepare:** Set up quiet workspace, check ID, ensure stable internet

#### Day 6-7: Exam and Post-Exam
- [ ] Take the exam
- [ ] Document questions you were unsure about
- [ ] If needed, plan retake strategy based on score report
- [ ] Celebrate your achievement

## Daily Study Routine

### Recommended Schedule (1.5-2 hours per day)
1. **Review (15 min):** Review previous day's notes
2. **Study (45 min):** New topic reading and documentation
3. **Practice (30 min):** Hands-on lab work
4. **Quiz (15 min):** Self-assessment questions

## Key Milestones

- [ ] **Week 1:** Can explain IaC concepts and write basic HCL
- [ ] **Week 2:** Can deploy multi-resource infrastructure with providers
- [ ] **Week 3:** Can manage state, use remote backends with locking
- [ ] **Week 4:** Can create and use modules, manage workspaces
- [ ] **Week 5:** Score 70%+ on first practice exam
- [ ] **Week 6:** Score 80%+ on practice exam, pass certification
