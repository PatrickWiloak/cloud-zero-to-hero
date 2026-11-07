---
last-updated: 2026-11-07
exam-version: SAP-C03
difficulty: advanced
---

# AWS Certified Solutions Architect - Professional (SAP-C03)

## Important Notice

**SAP-C03 is the current exam version from November 17, 2026.** AWS's comparison page states that SAP-C02 is "in use until November 16, 2026" and SAP-C03 "in use beginning November 17, 2026". This guide supersedes the [SAP-C02 guide](../solutions-architect-pro-sap-c02/README.md). The domains were restructured, not just updated: do not map C02 notes onto C03 one to one. See [what changed](#what-changed-from-sap-c02).

Sources (read 2026-11-07): **[📖 AWS Certified Solutions Architect - Professional](https://aws.amazon.com/certification/certified-solutions-architect-professional/)** - Exam details; **[📖 SAP-C03 Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/solutions-architect-professional-03.html)** - Official content outline

## Exam Overview

SAP-C03 validates advanced skills designing optimized AWS solutions based on the AWS Well-Architected Framework: architectures built for the cloud with AI/ML integration, security and governance, cost optimization, resilience and migration, and operational excellence and automation. The target candidate has 2 or more years of experience designing and implementing cloud solutions on AWS, including serverless and AI-integrated architectures in multi-account environments.

| Item | Value | Source |
|------|-------|--------|
| **Exam code** | SAP-C03 | Exam guide |
| **Duration** | 180 minutes | AWS certification page |
| **Questions** | 75 total: 65 scored plus 10 unscored | AWS certification page (75) and exam guide (65 scored, 10 unscored) |
| **Question types** | Multiple choice and multiple response | Exam guide |
| **Scoring** | Scaled 100-1,000; minimum passing score 720; compensatory | Exam guide |
| **Cost** | 300 USD | AWS certification page |
| **Delivery** | Pearson VUE testing center or online proctored | AWS certification page |
| **Validity** | 3 years; recertify by passing the latest version | AWS certification page |
| **Languages** | English, Japanese, Korean, Brazilian Portuguese, Simplified Chinese, Latin American Spanish | AWS certification page |

Out of scope per the guide: in-depth operating system knowledge; AI/ML model training, fine-tuning and data science workflows; security incident forensics and detailed threat investigation; application code development and debugging.

## Exam Domains

| Domain | Weight (scored content) | C02 equivalent | Notes |
|--------|------------------------|----------------|-------|
| 1. Architecture Design and Implementation Built for the Cloud | 25% | Parts of 1 (26%) and 2 (29%) | [01](notes/01-architecture-design-built-for-the-cloud.md) |
| 2. Security, Compliance, and Governance | 25% | Parts of 1, 3 | [02](notes/02-security-compliance-governance.md) |
| 3. Cost-Optimized Architecture Design | 15% | Parts of 2, 3 (3 was 25%) | [03](notes/03-cost-optimized-architecture-design.md) |
| 4. Resilience, Migration, and Business Continuity | 15% | Domain 4 (20%) plus DR content | [04](notes/04-resilience-migration-business-continuity.md) |
| 5. Operational Excellence and Automation | 20% | Parts of 1, 2, 3 | [05](notes/05-operational-excellence-automation.md) |

The C02 domains were: 1 Design Solutions for Organizational Complexity (26%), 2 Design for New Solutions (29%), 3 Continuous Improvement for Existing Solutions (25%), 4 Accelerate Workload Migration and Modernization (20%).

## What changed from SAP-C02

From **[📖 Comparison of SAP-C02 and SAP-C03](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/sap-03-comparison.html)**:

**New content**
- Task 1.2: AI and ML integration (Bedrock, AgentCore, Knowledge Bases, SageMaker AI inference, RAG).
- Task 2.5: security and responsible AI controls (Bedrock Guardrails, AgentCore Identity, human oversight workflows); AI logging and audit in 2.3 and 2.4.
- Architecture: service mesh (VPC Lattice, ECS Service Connect), ECR scanning and lifecycle, ingress design, WebSocket and pub/sub, multi-tenancy, hybrid compute (EKS Anywhere, ECS Anywhere, Outposts, Local Zones), IPv6 and dual stack, lakehouse and analytics pipelines, data cataloging and sharing.
- Security: application authN/authZ (Cognito, EKS Pod Identity), IAM Roles Anywhere, post-quantum cryptography, data residency controls, AWS Artifact evidence, threat modeling.
- Cost: AI/ML cost optimization, cross-Region inference routing, cost-effective observability.
- Resilience: multi-cluster container HA and DR.
- Operations: pipeline security scanning and signing, multi-account pipelines, Bedrock Evaluations, Container Insights, AI/ML monitoring, synthetic and real user monitoring, controlled remediation, automated runbooks.

**Removed from the blueprint text:** "Application upgrade path" and "Delegating to AWS" (C02 domain 2), and "Migration-tool security" (C02 domain 4). AWS notes these may still be implicit in other skills.

**Services**
- Added to scope: Amazon Bedrock, Data Lifecycle Manager, MemoryDB, Security Lake, Verified Permissions, VPC Lattice, Application Auto Scaling, CDK, Clean Rooms, Cloud WAN, CodeCommit, Cost Categories, Data Transfer Terminal, Distro for OpenTelemetry, Fault Injection Service, Local Zones, Resilience Hub, Transform, Verified Access, Reserved Instances.
- Removed: all AWS IoT services, End User Computing (AppStream 2.0, WorkSpaces), Media Services (Elastic Transcoder, Kinesis Video Streams), and individual services including CodeGuru, Lightsail, Managed Blockchain, Pinpoint, SES, Amplify, App Runner, Batch, CodeArtifact, Data Exchange, Device Farm, Health Dashboard, License Manager, Proton, Service Catalog and Wavelength. Individual AI services (Comprehend, Kendra, Lex, Personalize, Polly, Rekognition, Textract, Transcribe, Translate) were replaced by Amazon Bedrock and SageMaker AI as parent entries.

**Consolidated:** many granular C02 tasks were merged into broader C03 tasks. AWS states the consolidation does not reduce emphasis on essential skills.

## Study Materials

### Notes (study order)
- [01 - Architecture Design and Implementation Built for the Cloud](notes/01-architecture-design-built-for-the-cloud.md)
- [02 - Security, Compliance, and Governance](notes/02-security-compliance-governance.md)
- [03 - Cost-Optimized Architecture Design](notes/03-cost-optimized-architecture-design.md)
- [04 - Resilience, Migration, and Business Continuity](notes/04-resilience-migration-business-continuity.md)
- [05 - Operational Excellence and Automation](notes/05-operational-excellence-automation.md)

### Study Resources
- [Fact Sheet](fact-sheet.md) - Verified facts, in-scope changes and decision tables
- [Practice Plan](practice-plan.md) - 8-week schedule
- [Scenarios](scenarios.md) - Professional-level trade-off scenarios
- [Strategy](strategy.md) - How to read and answer long scenario questions
- [Practice Questions](../../../../resources/practice-questions/aws-solutions-architect-professional-sap-c03.md) - 20 original scenario questions

The C02 notes under [SAP-C02](../solutions-architect-pro-sap-c02/README.md) (compute, databases, networking, storage, observability and others) remain useful reference for service depth, and some are cited by name in the C03 notes; they are organized by service rather than by the C03 domains.

## Official Resources

- **[📖 SAP-C03 Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/solutions-architect-professional-03.html)** - Domains, tasks and skills
- **[📖 SAP-C03 in-scope services](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/sap-03-in-scope-services.html)** - Services and features that may appear
- **[📖 AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)** - The framework the exam is built on
