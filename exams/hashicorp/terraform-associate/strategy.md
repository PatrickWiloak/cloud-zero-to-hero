---
last-updated: 2026-11-07
---

# Terraform Associate (004) Study Strategy

> Version 004 publishes eight objectives with no weights. The new content versus 003 is lifecycle rules and `depends_on` (4f), custom conditions (4g), ephemeral values and write-only arguments (4h) and HCP Terraform workspaces and projects (8c). Budget time for those first if you studied from older material.

## Study Approach

### Phase 1: Foundation (2 weeks)
1. **IaC Fundamentals**
   - Understand declarative vs imperative approaches
   - Learn IaC benefits: versioning, consistency, automation
   - Compare Terraform with CloudFormation, Ansible, Pulumi
   - Study Terraform architecture and provider plugin model

2. **HCL and Configuration Basics**
   - Master block types: terraform, provider, resource, data, variable, output
   - Practice variable types and type constraints
   - Write configurations from scratch (avoid copy-paste)
   - Understand expressions, conditionals, and functions

### Phase 2: Core Skills (2-3 weeks)
1. **Workflow and State Mastery**
   - Practice the full init/plan/apply/destroy cycle repeatedly
   - Configure remote backends with state locking
   - Practice state commands: list, show, mv, rm
   - Understand state file format and sensitive data handling

2. **Modules and Advanced Features**
   - Build custom modules with inputs and outputs
   - Use Terraform Registry modules with version constraints
   - Practice workspaces for environment management
   - Import existing resources into Terraform management

### Phase 3: Exam Preparation (1-2 weeks)
1. **Practice Exams**
   - Take HashiCorp official practice exam
   - Use Bryan Krausen or Tutorials Dojo practice tests
   - Target 80%+ before scheduling the real exam
   - Review every incorrect answer thoroughly

2. **Final Review**
   - Review command flags and exact syntax
   - Study variable precedence order
   - Review state backend comparison table
   - Quick review of provisioner caveats and limitations

## Comprehensive Study Resources

### Official Resources
- **[Terraform Associate Study Guide](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-study-004)** - Official study guide from HashiCorp
- **[Terraform Associate Exam Review](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004)** - Official exam review questions
- **[Terraform Documentation](https://developer.hashicorp.com/terraform/docs)** - Complete reference documentation
- **[Terraform Tutorials](https://developer.hashicorp.com/terraform/tutorials)** - Hands-on learning paths
- **[Terraform Registry](https://registry.terraform.io/)** - Providers, modules, and policies

### Recommended Courses
- **Bryan Krausen - Terraform Associate on Udemy** - Highly rated exam-focused course
- **Andrew Brown - Terraform Associate on freeCodeCamp** - Free comprehensive course
- **KodeKloud - Terraform for Beginners** - Interactive hands-on course
- **HashiCorp Learn** - Free official tutorials organized by topic

### Practice Test Platforms
- **HashiCorp Official Practice Exam** - Included with exam registration
- **Bryan Krausen Practice Tests (Udemy)** - Multiple practice exams
- **Tutorials Dojo Terraform Practice Exams** - Scenario-based questions
- **Whizlabs Terraform Practice Tests** - Large question bank

### Hands-On Practice
- **AWS Free Tier** - 12 months free for Terraform practice
- **GCP Free Tier** - $300 credit for 90 days
- **Terraform Cloud Free Tier** - Free for up to 5 users
- **KillerCoda / Katacoda** - Browser-based Terraform labs

## Exam Tactics

### Question Strategy
1. **Read carefully:** Identify exactly what is being asked - concept, command, or configuration
2. **Eliminate first:** Remove obviously incorrect answers before selecting
3. **Watch for keywords:** "best practice," "first step," "most efficient," "recommended"
4. **Command precision:** Know exact command syntax and flag names
5. **Concept clarity:** Understand WHY, not just WHAT

### Time Management
- **~1 minute per question** average (57 questions in 60 minutes)
- **Flag and move:** Do not spend more than 90 seconds on any question
- **Quick wins first:** Answer confident questions immediately
- **Review pass:** Use remaining time for flagged questions
- **Fill-in-blank:** These may take more time, budget accordingly

### Common Patterns on the Exam
- **State management:** Remote backends, locking, state commands
- **Variable precedence:** Know the exact order from lowest to highest priority
- **Provider versioning:** Understand ~> constraint behavior
- **Module sources:** Registry, local, GitHub, S3 formats
- **Workflow commands:** Know flags for init, plan, apply
- **Import behavior:** What import does and does not do

## Common Pitfalls

### Study Mistakes
- Memorizing commands without understanding underlying concepts
- Skipping hands-on practice and only reading documentation
- Not practicing writing HCL from scratch (relying on copy-paste)
- Ignoring state management topics (heavily tested)
- Overlooking provisioner caveats and limitations

### Exam Mistakes
- Confusing `terraform refresh` (deprecated) with `terraform plan -refresh-only`
- Thinking `terraform import` generates configuration automatically
- Not knowing that `count` and `for_each` cannot coexist on the same resource
- Confusing CLI workspaces with Terraform Cloud workspaces
- Assuming all backends support state locking (not all do)
- Forgetting that variable precedence has environment variables as highest priority
- Thinking `terraform validate` checks provider credentials (it does not)
- Confusing `-reconfigure` with `-migrate-state` for backend changes

### Conceptual Misunderstandings
- Terraform is declarative, not imperative - you describe desired state
- State file is the source of truth for what Terraform manages
- Provisioners are a last resort, not a recommended pattern
- `terraform destroy` only destroys resources in the current state
- Modules are containers for multiple resources, not individual resource wrappers

## Progress Tracking

### Weekly Milestones
- **Week 1-2:** Can explain IaC, write HCL configurations, deploy resources
- **Week 3:** Master state management, remote backends, state commands
- **Week 4:** Build and use modules, manage workspaces, import resources
- **Week 5:** Score 70%+ on practice exam, identify and fill gaps
- **Week 6:** Score 80%+ on practice exam, pass certification

### Self-Assessment Questions
- Can I write a complete Terraform configuration from scratch?
- Do I understand the difference between local and remote state?
- Can I explain variable precedence order without looking it up?
- Do I know when to use count vs for_each?
- Can I configure a remote backend with state locking?
- Do I understand the full terraform init/plan/apply workflow?
- Can I create a reusable module with proper inputs and outputs?
