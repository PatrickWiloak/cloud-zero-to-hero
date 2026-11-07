# AWS Certified Solutions Architect - Professional (SAP-C02)

## Important Notice

**The SAP-C02 exam retires on November 16, 2026.** Until then it can still be taken; after that date this guide describes a withdrawn exam. The last day to sit SAP-C02 is November 16, 2026. **SAP-C03** registration opened October 27, 2026 and its outline is published: this guide is **superseded by the [SAP-C03 guide](../solutions-architect-pro-sap-c03/README.md)**, which lists what changed. SAP-C03 is in use from November 17, 2026.

Source: [AWS Certified Solutions Architect - Professional](https://aws.amazon.com/certification/certified-solutions-architect-professional/)

---

## Exam Overview

The AWS Certified Solutions Architect - Professional certification validates advanced technical skills and experience in designing distributed applications and systems on AWS at the enterprise level.

**Exam Details:**
- **Exam Code:** SAP-C02
- **Duration:** 180 minutes (3 hours)
- **Number of Questions:** 75 questions
- **Passing Score:** 750 out of 1000 (estimated 70%)
- **Question Types:** Multiple choice and multiple response
- **Cost:** $300 USD
- **Validity:** 3 years
- **Prerequisites:** SAA-C03 (or equivalent experience) + 2+ years hands-on AWS

## 📋 Quick Links

- [**Fact Sheet**](fact-sheet.md) - Exam logistics and objectives
- [**Practice Plan**](practice-plan.md) - Structured study schedule

## 📚 Study Materials

### Core Notes
- [Architecture Pillars](notes/architecture-pillars.md)
- [Compute Containers](notes/compute-containers.md)
- [Cost Governance](notes/cost-governance.md)
- [Databases](notes/databases.md)
- [Integration Streaming](notes/integration-streaming.md)
- [Networking](notes/networking.md)
- [Observability](notes/observability.md)
- [Security IAM](notes/security-iam.md)
- [Storage](notes/storage.md)
## 🎯 Exam Domains

### Domain 1: Design Solutions for Organizational Complexity (26%)

#### Cross-Account Architectures
- AWS Organizations and multi-account strategies
- Organizational Units (OUs) and account structure
- Service Control Policies (SCPs) and guardrails
- Cross-account IAM roles and resource sharing
- Consolidated billing and cost allocation
- AWS Resource Access Manager (RAM)

#### Hybrid and Multi-Cloud
- Direct Connect and VPN architectures
- Direct Connect with VPN failover (ECMP)
- Hybrid DNS with Route 53 Resolver
- Storage Gateway modes and use cases
- DataSync for hybrid data transfers
- Multi-cloud integration patterns
- AWS Outposts for on-premises AWS

#### Enterprise Networking
- Transit Gateway hub-and-spoke architecture
- Transit Gateway routing and route tables
- VPC peering at scale
- PrivateLink for SaaS and third-party integration
- Advanced routing and traffic management
- Network segmentation and isolation
- AWS Cloud WAN for global networking

### Domain 2: Design for New Solutions (29%)

#### Advanced Architecture Patterns
- Microservices and serverless architectures
- Event-driven architectures with EventBridge
- CQRS (Command Query Responsibility Segregation)
- Event sourcing patterns
- Multi-region active-active architectures
- Saga pattern for distributed transactions
- Circuit breaker and bulkhead patterns

#### Data Architecture
- Aurora Global Database for multi-region
- DynamoDB Global Tables
- S3 Cross-Region Replication (CRR)
- Data lake architectures with Lake Formation
- Redshift RA3 nodes and Spectrum
- Data mesh architecture patterns
- Real-time streaming with Kinesis

#### Application Integration
- EventBridge for complex event routing
- Step Functions for orchestration
- Step Functions saga patterns
- SQS/SNS fan-out patterns
- API Gateway advanced features (custom domains, caching, throttling)
- AppSync for GraphQL APIs
- Managed workflows with MWAA (Apache Airflow)

#### Modern Application Development
- Containerization with ECS and EKS
- Fargate for serverless containers
- Lambda cold start optimization
- Lambda layers and extensions
- App Runner for container deployment
- Amplify for full-stack applications

### Domain 3: Continuous Improvement for Existing Solutions (25%)

#### Performance Optimization
- CloudFront edge optimization and Lambda@Edge
- CloudFront Functions for high-scale transformations
- Database performance tuning (RDS, Aurora, DynamoDB)
- Caching strategies (ElastiCache, DAX, API Gateway)
- Compute optimization (Graviton processors, Savings Plans, Spot)
- Global Accelerator for multi-region performance
- S3 Transfer Acceleration

#### Cost Optimization at Scale
- Reserved Instance and Savings Plans management
- S3 Intelligent-Tiering and storage class optimization
- Compute rightsizing automation with Compute Optimizer
- Cost anomaly detection with Cost Anomaly Detection
- AWS Budgets and Cost Explorer
- Tagging strategies for cost allocation
- Spot Fleet and Spot Instance best practices

#### Operational Excellence
- Infrastructure as Code (CloudFormation, CDK, Terraform)
- CloudFormation StackSets for multi-account
- CI/CD pipelines with CodePipeline
- Blue-green and canary deployments
- Monitoring and observability (CloudWatch, X-Ray)
- Automated remediation with Systems Manager
- Chaos engineering and resilience testing

#### Reliability Improvements
- Auto Scaling and predictive scaling
- Health checks and automated recovery
- Backup and restore automation
- Disaster recovery testing automation
- Multi-AZ and multi-region failover
- Aurora Auto Scaling and failover

### Domain 4: Accelerate Workload Migration and Modernization (20%)

#### Migration Strategies (7 Rs)
- Rehost (lift-and-shift) with AWS MGN
- Replatform (lift, tinker, and shift)
- Refactor (re-architect for cloud-native)
- Relocate (VMware Cloud on AWS)
- Retain (keep on-premises for now)
- Retire (decommission)
- Repurchase (move to SaaS)
- Migration Hub and Application Discovery Service

#### Migration Tools and Services
- AWS Application Migration Service (MGN)
- Database Migration Service (DMS) and SCT
- DataSync for large-scale data transfers
- Transfer Family for SFTP/FTPS/FTP
- Snow family (Snowcone, Snowball, Snowmobile)
- Migration Evaluator for business case
- CloudEndure for continuous replication

#### Modernization Patterns
- Containerization strategies (ECS, EKS)
- Serverless refactoring approaches
- Database modernization (RDS, Aurora, DynamoDB)
- Strangler fig pattern for incremental migration
- Feature toggles and blue-green for risk mitigation
- Application Composer for serverless design

## Key Professional-Level Topics

### Advanced Networking
- Transit Gateway with complex routing scenarios
- Direct Connect gateway and virtual interfaces
- VPC endpoint policies and PrivateLink
- Network ACLs vs. Security Groups at scale
- VPC Flow Logs analysis
- Network Firewall for advanced filtering

### Enterprise Security
- AWS SSO (IAM Identity Center) integration
- Permission boundaries and SCPs
- Secrets Manager rotation automation
- KMS key policies and grants
- GuardDuty, Security Hub, Detective integration
- Macie for data discovery and protection
- Shield Advanced for DDoS protection

### Data & Analytics
- Redshift Spectrum for data lake queries
- Glue DataBrew for data preparation
- Athena federated queries
- EMR on EKS for big data on Kubernetes
- OpenSearch Service for analytics
- QuickSight for BI and dashboards

### High Availability & Disaster Recovery
- Multi-region architectures and patterns
- RTO/RPO requirements and trade-offs
- Pilot Light strategy
- Warm Standby strategy
- Active-Active multi-region
- Automated failover with Route 53
- Backup strategies with AWS Backup

## Study Strategy

### Recommended Timeline: 12-14 Weeks

**Weeks 1-2:** Compute, Containers, and Architecture Patterns
- EC2 advanced features, Auto Scaling
- ECS, EKS, Fargate, App Runner
- Lambda optimization and patterns
- Serverless architectures

**Weeks 3-4:** Advanced Networking
- Transit Gateway architectures
- Direct Connect and hybrid connectivity
- VPC design patterns
- Global networking with Cloud WAN

**Weeks 5-6:** Data Architecture and Analytics
- Aurora Global Database
- DynamoDB advanced features
- Redshift and data warehousing
- Real-time analytics with Kinesis

**Weeks 7-8:** Integration, Messaging, and Orchestration
- EventBridge patterns
- Step Functions workflows
- SQS/SNS integration
- API Gateway advanced features

**Weeks 9-10:** Security, Cost, and Governance
- Multi-account security with Organizations
- IAM advanced policies
- Cost optimization strategies
- Governance with Service Control Policies

**Weeks 11-12:** Migration, Modernization, and DR
- Migration strategies and tooling
- Disaster recovery patterns
- Multi-region architectures
- Application modernization

**Weeks 13-14:** Practice Exams and Review
- Take multiple practice exams
- Review weak areas thoroughly
- Study AWS whitepapers
- Final review and confidence building

### Essential Hands-on Practice
- Build multi-account Organizations with SCPs
- Deploy Transit Gateway hub-and-spoke
- Implement Aurora Global Database
- Create Step Functions workflows with saga pattern
- Design multi-region failover architecture
- Build hybrid connectivity with Direct Connect
- Deploy containerized applications on EKS
- Implement comprehensive monitoring with CloudWatch

## 📚 Study Resources

### Primary Resources
1. **AWS Well-Architected Framework** - Mandatory (all 6 pillars)
2. **AWS Whitepapers** - Migration, Security, Serverless, Containers
3. **Adrian Cantrill's SAP-C02 Course** - $40 (most comprehensive)
4. **Tutorials Dojo Practice Tests** - $15 (6 full exams)
5. **AWS Official Practice Exam** - $40 (take 1-2 weeks before)

### Official AWS Resources
- **[SAP-C02 Exam Page](https://aws.amazon.com/certification/certified-solutions-architect-professional/)**
- **[AWS Skill Builder - Exam Prep](https://skillbuilder.aws/)**
- **[AWS Architecture Center](https://aws.amazon.com/architecture/)**
- **[AWS Whitepapers](https://aws.amazon.com/whitepapers/)**
- **[AWS Free Tier](https://aws.amazon.com/free/)**

**👉 [Complete AWS Study Resources Guide](../../../../.templates/resources-aws.md)**

## Exam Tips

### Question Strategy
- Read entire scenario carefully (questions are long!)
- Identify key requirements and constraints
- Look for keywords indicating specific services
- Eliminate obviously incorrect answers
- Consider cost, performance, and operational complexity
- Think about enterprise scale and multi-account scenarios

### Common Question Themes
- Multi-account architecture with Organizations
- Hybrid connectivity (Direct Connect, VPN)
- Multi-region data replication and failover
- Cost optimization at scale
- Migration strategies for large enterprises
- Advanced networking with Transit Gateway
- Security at organizational level with SCPs

### Time Management
- 180 minutes for 75 questions (~2.4 minutes per question)
- Flag difficult questions and return later
- Don't spend more than 4 minutes on any single question
- Leave time for review (15-20 minutes)

## Prerequisites & Next Steps

### Prerequisites
- **Required**: AWS Certified Solutions Architect - Associate (or equivalent)
- **Experience**: 2+ years hands-on AWS experience
- **Knowledge**: Deep understanding of AWS services and architecture patterns
- **Skills**: Complex problem solving, architectural trade-offs

### Career Path
- **Next Certifications**: DevOps Engineer Professional, Specialty certifications
- **Role Focus**: Senior Solutions Architect, Principal Engineer, Cloud Architect
- **Skills Development**: Enterprise architecture, complex migrations, Well-Architected reviews

## 🎓 Success Criteria

- Design resilient, secure, and cost-optimized architectures for enterprises
- Handle complex organizational and technical requirements
- Navigate trade-offs between competing priorities
- Demonstrate advanced AWS service integration knowledge
- Apply Well-Architected Framework principles to real-world scenarios

---

**Remember**: SAP-C02 is significantly harder than SAA-C03. Questions are long scenarios requiring deep analysis of trade-offs. Focus on understanding WHY certain architectural decisions are made in enterprise contexts, not just WHAT services to use!
