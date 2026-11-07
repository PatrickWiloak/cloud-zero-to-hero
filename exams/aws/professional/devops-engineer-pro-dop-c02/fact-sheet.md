---
last-updated: 2026-05-03
---

# AWS DevOps Engineer Professional (DOP-C02) - Fact Sheet

## Quick Reference

**Exam Code:** DOP-C02
**Duration:** 180 minutes (3 hours)
**Questions:** 75 questions
**Passing Score:** 750/1000 (estimated ~72%)
**Cost:** $300 USD
**Validity:** 3 years
**Delivery:** Pearson VUE (Testing center or online proctored)
**Difficulty:** ⭐⭐⭐⭐⭐ (Expert-level)

## Exam Domain Breakdown

| Domain | Weight | Key Focus |
|--------|--------|-----------|
| SDLC Automation | 22% | CI/CD pipelines, IaC, testing automation |
| Configuration Management & IaC | 17% | CloudFormation, CDK, Config, SSM |
| Resilient Cloud Solutions | 15% | HA, DR, fault tolerance, monitoring |
| Monitoring & Logging | 15% | CloudWatch, X-Ray, EventBridge, metrics |
| Incident & Event Response | 14% | Automated remediation, rollback, runbooks |
| Security & Compliance | 17% | Secrets, compliance, auditing, encryption |

## Core DevOps Services by Domain

### Domain 1: SDLC Automation (22%)

**CI/CD Pipeline Services:**
- **CodeCommit** - Git repositories, encryption at rest/transit, IAM/federated access
- **CodeBuild** - Managed build service, Docker support, buildspec.yml
  - Build environments: Ubuntu, Amazon Linux 2, Windows
  - Custom Docker images supported
  - Artifacts to S3, caching support
  - [📖 CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/)

- **CodeDeploy** - Automated deployments, blue/green and in-place
  - Compute platforms: EC2/On-premises, Lambda, ECS
  - Deployment configs: OneAtATime, HalfAtATime, AllAtOnce, custom
  - appspec.yml for deployment instructions
  - Automatic rollback on failure
  - [📖 CodeDeploy Documentation](https://docs.aws.amazon.com/codedeploy/)

- **CodePipeline** - Workflow orchestration, multi-stage pipelines
  - Source: CodeCommit, GitHub, S3, ECR
  - Build: CodeBuild, Jenkins
  - Deploy: CodeDeploy, CloudFormation, ECS, S3, Elastic Beanstalk
  - Manual approval gates
  - Cross-region deployments
  - [📖 CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/)

**Testing Automation:**
- **CodeBuild** - Unit tests, integration tests, security scans
- **Device Farm** - Mobile app testing on real devices
- **[📖 Device Farm Documentation](https://docs.aws.amazon.com/devicefarm/)** - Test on real mobile devices
- **Lambda** - Custom test automation
- **[📖 Lambda for Testing](https://docs.aws.amazon.com/lambda/latest/dg/)** - Serverless test functions
- **Step Functions** - Complex test workflows
- **[📖 Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/)** - Workflow orchestration

**Artifact Management:**
- **CodeArtifact** - Artifact repository (Maven, npm, PyPI, NuGet)
- **[📖 CodeArtifact Documentation](https://docs.aws.amazon.com/codeartifact/)** - Package management
- **ECR** - Container registry, vulnerability scanning, lifecycle policies
- **[📖 Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/)** - Container registry
- **S3** - Artifact storage with versioning
- **[📖 S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)** - Version control for artifacts

### Domain 2: Configuration Management & IaC (17%)

**Infrastructure as Code:**
- **CloudFormation** - Declarative IaC, JSON/YAML templates
  - StackSets for multi-account/region deployment
  - Drift detection to identify manual changes
  - Change sets for preview before execution
  - Nested stacks for modularity
  - Custom resources with Lambda
  - [📖 CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/)
  - [📖 CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)

- **CDK (Cloud Development Kit)** - IaC in programming languages
  - Languages: TypeScript, Python, Java, C#, Go
  - Synthesizes to CloudFormation
  - Constructs for reusable components (L1, L2, L3)
  - [📖 CDK Documentation](https://docs.aws.amazon.com/cdk/)

- **Terraform** - Third-party IaC, state management
- **SAM (Serverless Application Model)** - Serverless IaC, extends CloudFormation
- **[📖 AWS SAM](https://docs.aws.amazon.com/serverless-application-model/)** - Serverless framework

**Configuration Management:**
- **Systems Manager (SSM)** - Operational hub
  - **Parameter Store** - Secure configuration storage, hierarchical, versioning
  - **Session Manager** - Secure shell without SSH keys or bastion hosts
  - **Patch Manager** - Automated OS patching
  - **State Manager** - Maintain instance configuration
  - **Automation** - Runbooks for operational tasks
  - **Run Command** - Execute commands at scale
  - [📖 Systems Manager Documentation](https://docs.aws.amazon.com/systems-manager/)

- **AWS Config** - Track resource configuration, compliance rules
  - Config rules: AWS managed (100+) or custom (Lambda)
  - Conformance packs for compliance frameworks
  - Multi-account aggregation
  - Remediation actions (SSM Automation)
  - [📖 Config Documentation](https://docs.aws.amazon.com/config/)

- **OpsWorks** - Chef/Puppet managed configuration, (retired: end of life May 2024; use Systems Manager)
- **[📖 Migrate AWS OpsWorks Stacks to Systems Manager](https://aws.amazon.com/blogs/mt/migrate-your-aws-opsworks-stacks-to-aws-systems-manager/)** - Configuration management
- **AppConfig** - Feature flags and configuration deployment
- **[📖 AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/)** - Application configuration

### Domain 3: Resilient Cloud Solutions (15%)

**High Availability Patterns:**
- **Auto Scaling** - Dynamic capacity management
  - Target tracking (maintain metric target)
  - Step scaling (scale based on alarm thresholds)
  - Simple scaling (single adjustment)
  - Scheduled scaling (predictable patterns)
  - Predictive scaling (ML-powered forecasting)
  - [📖 Auto Scaling Documentation](https://docs.aws.amazon.com/autoscaling/)

- **Elastic Load Balancing** - Distribute traffic
  - ALB (Layer 7): HTTP/HTTPS, host/path routing, Lambda targets
  - NLB (Layer 4): TCP/UDP, ultra-low latency, static IPs
  - Gateway Load Balancer: Third-party appliances
  - [📖 ELB Documentation](https://docs.aws.amazon.com/elasticloadbalancing/)

- **Multi-AZ Deployments** - Synchronous replication within region
- **[📖 Multi-AZ Deployments](https://docs.aws.amazon.com/whitepapers/latest/real-time-communication-on-aws/high-availability-and-scalability-on-aws.html)** - HA architecture
- **Multi-Region Deployments** - Asynchronous cross-region replication
- **[📖 Multi-Region Architectures](https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/multi-region-architectures.html)** - Global applications

**Disaster Recovery:**
- **Backup Strategies:**
  - AWS Backup - Centralized backup across 35+ services
  - Automated backup policies with lifecycle rules
  - Cross-region and cross-account backup copy
  - [📖 Backup Documentation](https://docs.aws.amazon.com/aws-backup/)

- **DR Strategies (RTO/RPO trade-offs):**
  - Backup & Restore: RTO hours-days, RPO hours, lowest cost
  - Pilot Light: RTO 10s of minutes, RPO minutes
  - Warm Standby: RTO minutes, RPO seconds
  - Multi-Region Active-Active: RTO seconds, RPO near-zero, highest cost

- **Elastic Disaster Recovery (DRS)** - Continuous replication, formerly CloudEndure
- **[📖 AWS DRS](https://docs.aws.amazon.com/drs/latest/userguide/)** - Application-level DR
- **Database Replication:**
  - RDS Multi-AZ: Synchronous, automatic failover < 60 sec
  - **[📖 RDS Multi-AZ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)** - Database HA
  - Aurora Global Database: Cross-region, < 1 sec lag
  - **[📖 Aurora Global Database](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html)** - Multi-region database
  - DynamoDB Global Tables: Multi-region active-active
  - **[📖 DynamoDB Global Tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html)** - Global NoSQL

**Chaos Engineering:**
- **AWS Fault Injection Simulator (FIS)** - Controlled fault injection
  - Test resilience by injecting failures
  - Stop/terminate instances, throttle APIs, network latency
  - [📖 FIS Documentation](https://docs.aws.amazon.com/fis/)

### Domain 4: Monitoring & Logging (15%)

**CloudWatch Ecosystem:**
- **CloudWatch Metrics** - Monitor service and custom metrics
  - Standard metrics: 5-minute intervals (free)
  - Detailed monitoring: 1-minute intervals (paid)
  - Custom metrics: High-resolution up to 1-second intervals
  - Metric math for calculations
  - [📖 CloudWatch Metrics Documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)

- **CloudWatch Logs** - Centralized log management
  - Log groups, log streams, retention policies
  - Log Insights: SQL-like query language
  - Metric filters: Extract metrics from logs
  - Subscription filters: Stream to Lambda, Kinesis, Firehose
  - [📖 CloudWatch Logs Documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)

- **CloudWatch Alarms** - Automated responses to metric thresholds
  - Actions: SNS notifications, Auto Scaling, EC2 actions, Systems Manager
  - Composite alarms: AND/OR logic on multiple alarms

- **CloudWatch Dashboards** - Visualize metrics across services/accounts
- **CloudWatch Synthetics** - Canary monitoring for endpoints
- **CloudWatch Application Insights** - Automated application monitoring

**Distributed Tracing:**
- **X-Ray** - End-to-end request tracing
  - Service map visualization
  - Trace analysis with filtering
  - Annotations (indexed, searchable) vs metadata (not indexed)
  - Sampling rules to control trace volume
  - Integration: Lambda, API Gateway, ECS, Elastic Beanstalk, EC2
  - [📖 X-Ray Documentation](https://docs.aws.amazon.com/xray/)

**Event-Driven Monitoring:**
- **EventBridge** - Event bus for monitoring and automation
  - 100+ AWS service event sources
  - Custom applications as event sources
  - Event pattern matching (JSON)
  - Targets: Lambda, Step Functions, SQS, SNS, CodePipeline, etc.
  - [📖 EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/)

**Logging & Auditing:**
- **CloudTrail** - API call auditing (who, what, when, from where)
  - Management events (control plane) vs data events (data plane)
  - Insights for anomaly detection
  - Organization trails for multi-account
  - [📖 CloudTrail Documentation](https://docs.aws.amazon.com/cloudtrail/)

- **VPC Flow Logs** - Network traffic capture (ACCEPT/REJECT)
- **[📖 VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)** - Network monitoring
- **S3 Access Logs** - Bucket access auditing
- **[📖 S3 Server Access Logging](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html)** - S3 access logs
- **ELB Access Logs** - Load balancer request logs
- **[📖 ELB Access Logs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html)** - Load balancer logging

### Domain 5: Incident & Event Response (14%)

**Automated Remediation:**
- **Lambda** - Custom remediation logic
- **[📖 Lambda for Automation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html)** - Event-driven remediation
- **Systems Manager Automation** - Runbooks for common tasks
  - AWS-managed runbooks (100+)
  - Custom runbooks for organization-specific tasks
  - Approval steps for sensitive operations
  - [📖 SSM Automation Documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html)

- **Config Remediation Actions** - Auto-remediate non-compliant resources
- **[📖 Config Remediation](https://docs.aws.amazon.com/config/latest/developerguide/remediation.html)** - Automated compliance fixes
- **EventBridge Rules** - Trigger remediation on events
- **[📖 EventBridge Rules](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rules.html)** - Event-driven automation
- **Step Functions** - Orchestrate complex incident response workflows
- **[📖 Step Functions for Orchestration](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)** - Workflow automation

**Rollback Strategies:**
- **CodeDeploy** - Automatic rollback on deployment failure
  - CloudWatch alarm-based rollback
  - Deployment monitoring with stop and rollback

- **CloudFormation** - Automatic rollback on stack failure
  - Continue rollback on UPDATE_ROLLBACK_FAILED
  - Stack policy to prevent accidental updates

- **Lambda Aliases & Versions** - Traffic shifting and instant rollback
  - Weighted alias routing (e.g., 90% v1, 10% v2)
  - CodeDeploy for Lambda deployments (canary, linear, all-at-once)
  - **[📖 Lambda Deployments](https://docs.aws.amazon.com/lambda/latest/dg/lambda-traffic-shifting-using-aliases.html)** - Gradual rollout

- **ECS/EKS Blue/Green** - Zero-downtime deployments with quick rollback
- **[📖 ECS Blue/Green](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-bluegreen.html)** - Container deployments

**Incident Management:**
- **Systems Manager Incident Manager** - Incident response coordination
  - Incident templates and response plans
  - Automated escalation
  - Post-incident analysis
  - [📖 Incident Manager Documentation](https://docs.aws.amazon.com/incident-manager/)

- **SNS** - Alert notifications (email, SMS, HTTP/HTTPS)
- **[📖 Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/)** - Notification service
- **PagerDuty/Opsgenie Integration** - Third-party incident management
- **Chatbot** - Slack/Chime integration for operational notifications
- **[📖 AWS Chatbot](https://docs.aws.amazon.com/chatbot/latest/adminguide/)** - ChatOps integration

### Domain 6: Security & Compliance (17%)

**Secrets Management:**
- **Secrets Manager** - Automatic rotation, versioning, encryption
  - Native RDS/Aurora rotation (Lambda-based)
  - Custom rotation functions
  - Cross-region replication of secrets
  - Resource-based policies for access control
  - [📖 Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/)

- **Parameter Store** - Secure strings with KMS encryption
  - Standard (10,000 parameters, no additional charge)
  - Advanced (100,000+ parameters, advanced policies)
  - Parameter policies (expiration, change notification)
  - **[📖 Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)** - Configuration management

**Encryption:**
- **KMS (Key Management Service)** - Encryption key management
  - Customer managed keys (CMKs) for control
  - Automatic key rotation (yearly)
  - Key policies and grants for access control
  - CloudHSM integration for hardware security modules
  - [📖 KMS Documentation](https://docs.aws.amazon.com/kms/)

- **ACM (Certificate Manager)** - SSL/TLS certificate management
  - Free public certificates (DV only)
  - Automatic renewal and deployment
  - Private CA for internal certificates
  - **[📖 AWS Certificate Manager](https://docs.aws.amazon.com/acm/)** - SSL/TLS management

**Identity & Access:**
- **IAM** - Fine-grained access control
  - Roles for applications (EC2, Lambda, ECS)
  - Identity-based and resource-based policies
  - Permission boundaries to limit max permissions
  - [📖 IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

- **IAM Identity Center (AWS SSO)** - Centralized workforce identity
- **[📖 IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/)** - SSO for workforce
- **Cognito** - User authentication for applications
- **[📖 Amazon Cognito](https://docs.aws.amazon.com/cognito/)** - User pools and identity
- **Organizations SCPs** - Guardrails across accounts
- **[📖 Service Control Policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)** - Permission boundaries

**Compliance & Governance:**
- **Config** - Continuous compliance monitoring
- **[📖 AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/)** - Resource compliance
- **Security Hub** - Centralized security findings
- **[📖 AWS Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/)** - Security posture
- **GuardDuty** - Threat detection (ML-powered)
- **[📖 Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/)** - Threat detection
- **Macie** - Data discovery and protection (PII/PHI in S3)
- **[📖 Amazon Macie](https://docs.aws.amazon.com/macie/latest/user/)** - Data protection
- **Inspector** - Vulnerability scanning (EC2, ECR, Lambda)
- **[📖 Amazon Inspector](https://docs.aws.amazon.com/inspector/latest/user/)** - Vulnerability management
- **Audit Manager** - Automated audit evidence collection
- **[📖 AWS Audit Manager](https://docs.aws.amazon.com/audit-manager/latest/userguide/)** - Audit automation

## CI/CD Pipeline Patterns

### Pattern 1: Complete AWS-Native Pipeline
```
CodeCommit (Git)
  ↓ (webhook trigger)
CodePipeline
  ↓
CodeBuild (build & test)
  ↓
CodeDeploy (deploy to EC2/Lambda/ECS)
  ↓
CloudWatch (monitoring)
```

### Pattern 2: Multi-Environment Pipeline
```
Source: CodeCommit/GitHub
  ↓
Build: CodeBuild (unit tests, security scan)
  ↓
Dev Environment: Auto deploy
  ↓
Test Environment: Auto deploy + integration tests
  ↓
Manual Approval Gate
  ↓
Prod Environment: Blue/Green deployment
  ↓
Monitoring: CloudWatch + X-Ray
```

### Pattern 3: Containerized Pipeline
```
Source: CodeCommit/GitHub
  ↓
Build: CodeBuild (Docker build, push to ECR)
  ↓
Scan: ECR vulnerability scan
  ↓
Deploy: ECS/EKS with CodeDeploy
  ↓
Health Check: ALB health checks
  ↓
Traffic Shift: Gradual (10%, 50%, 100%)
```

### Pattern 4: Serverless Pipeline
```
Source: CodeCommit
  ↓
Build: SAM build (package Lambda functions)
  ↓
Deploy: CloudFormation (SAM deploy)
  ↓
Test: Lambda invocation tests
  ↓
Alias Shift: CodeDeploy for Lambda (canary/linear)
  ↓
Monitoring: CloudWatch Logs + X-Ray tracing
```

## CloudFormation Advanced Features

### StackSets
- Deploy stacks across multiple accounts and regions
- Central management from master account
- Automatic operations (update, delete) across all stacks
- Use cases: Enforce security baselines, deploy shared infrastructure

### Drift Detection
- Identify resources modified outside CloudFormation
- Detect: Deleted resources, modified properties
- Response: Update template or remediate drift
- [📖 Drift Detection Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)

### Custom Resources
- Extend CloudFormation with Lambda functions
- Provision non-AWS resources
- Custom validation logic
- Integrate third-party services

### Helper Scripts
- **cfn-init** - Retrieve and interpret metadata
- **cfn-signal** - Signal resource creation status
- **cfn-get-metadata** - Retrieve metadata
- **cfn-hup** - Detect and apply metadata changes

## Deployment Strategies Comparison

| Strategy | Downtime | Rollback | Infra Cost | Use Case |
|----------|----------|----------|------------|----------|
| **All-at-once** | Yes (brief) | Slow | $ | Dev/test, non-critical |
| **Rolling** | No | Moderate | $ | Standard workloads |
| **Rolling with batch** | No | Moderate | $ | Larger updates |
| **Immutable** | No | Fast (instant) | $$$ (temporary) | Zero-downtime needed |
| **Blue/Green** | No | Instant | $$$$ (2x infra) | Critical apps, instant rollback |
| **Canary** | No | Automated | $$ | Test with subset of users |
| **Linear** | No | Automated | $$ | Gradual rollout |

### CodeDeploy Deployment Types

**In-Place (Rolling):**
- Instances updated in-place
- Compute: EC2, on-premises only
- Downtime possible during update
- Lower cost (no duplicate infrastructure)

**Blue/Green:**
- New instances provisioned (green)
- Traffic shifted from old (blue) to new (green)
- Compute: EC2, Lambda, ECS
- No downtime, instant rollback
- Higher cost (temporary duplicate infrastructure)

**Lambda Deployment Configs:**
- **Canary10Percent5Minutes** - 10% for 5 min, then 100%
- **Linear10PercentEvery10Minutes** - Add 10% every 10 min
- **AllAtOnce** - Immediate 100% shift

## Monitoring Strategy Matrix

| Metric Type | Service | Use Case | Retention |
|-------------|---------|----------|-----------|
| **Infrastructure** | CloudWatch Metrics | CPU, memory, disk, network | 15 months |
| **Application** | CloudWatch Logs | Application logs, errors | Configurable (never expire to 1 day) |
| **Distributed Tracing** | X-Ray | Request flows, latency, errors | 30 days |
| **API Auditing** | CloudTrail | Who did what, when | 90 days (Event history), unlimited (in S3) |
| **Synthetic Monitoring** | CloudWatch Synthetics | Uptime, functionality | 30 days |
| **Network** | VPC Flow Logs | Network traffic, security | Configurable |
| **User Activity** | CloudTrail Data Events | S3 object access, Lambda invocations | Unlimited (in S3) |

## Security Best Practices

### Secrets Management
✅ **DO:**
- Store secrets in Secrets Manager or Parameter Store (SecureString)
- Enable automatic rotation for database credentials
- Use IAM roles for applications to retrieve secrets
- Encrypt secrets with KMS customer-managed keys
- Use resource-based policies to restrict access
- Enable CloudTrail logging for secret access

❌ **DON'T:**
- Hardcode secrets in code or configuration files
- Store secrets in environment variables (plain text)
- Commit secrets to version control
- Share secrets via email or chat
- Use the same secret across environments

### IAM Least Privilege
- Grant minimum necessary permissions
- Use IAM roles (not users) for applications
- Implement permission boundaries
- Regular access reviews with IAM Access Analyzer
- Use service-specific roles (not broad permissions)

### Encryption
- Enable encryption at rest for all data stores (S3, RDS, EBS, DynamoDB)
- Use TLS/SSL for data in transit
- Customer-managed KMS keys for sensitive data
- Enable CloudTrail log file encryption
- Rotate encryption keys regularly

## Auto Scaling Best Practices

### Target Tracking (Recommended)
- Simplest to configure
- Specify target metric value (e.g., CPU 50%)
- Auto Scaling automatically adjusts
- Supports custom metrics

### Step Scaling
- More granular control
- Different scaling amounts based on alarm thresholds
- Example: Add 1 instance if CPU > 60%, add 3 if CPU > 80%

### Predictive Scaling
- ML-powered forecasting based on historical data
- Schedules capacity changes before predicted load
- Combine with target tracking for optimal results

### Scaling Metrics
- **CPU Utilization** - Most common, but may lag
- **Request Count per Target** - Better for request-based scaling
- **Network In/Out** - For network-intensive applications
- **Custom Metrics** - Application-specific (queue depth, active connections)

## Common Exam Scenarios

### Scenario 1: Automated Compliance Remediation
**Q:** Detect and remediate S3 buckets with public access automatically.
**A:**
- AWS Config rule: `s3-bucket-public-read-prohibited`
- Config remediation action: SSM Automation document
- Lambda function to remove public access policies
- EventBridge rule to trigger on Config non-compliance
- SNS notification to security team

### Scenario 2: Multi-Region DR with RTO < 1 hour
**Q:** Design DR strategy for critical application with strict RTO.
**A:**
- Primary: us-east-1, DR: us-west-2
- Aurora Global Database (< 1 sec lag)
- S3 Cross-Region Replication (CRR)
- Warm standby with reduced capacity in DR region
- Route 53 health checks with automatic failover
- Regular DR testing with runbooks in SSM Automation

### Scenario 3: Zero-Downtime Deployment with Rollback
**Q:** Deploy microservices with zero downtime and instant rollback capability.
**A:**
- ECS with Fargate (serverless containers)
- ALB with target groups (blue/green)
- CodeDeploy for automated blue/green deployment
- CloudWatch alarms to trigger automatic rollback
- X-Ray for distributed tracing
- Gradual traffic shifting (10%, 50%, 100%)

### Scenario 4: Secrets Rotation at Scale
**Q:** Rotate database credentials for 100+ databases automatically.
**A:**
- Secrets Manager with automatic rotation
- Lambda rotation functions (single or multi-user)
- 30-day rotation schedule
- CloudWatch Events to monitor rotation success/failure
- SNS alerts for rotation failures
- RDS/Aurora native integration for seamless rotation

### Scenario 5: Cost-Optimized Pipeline
**Q:** Reduce CI/CD pipeline costs while maintaining quality.
**A:**
- CodeBuild with smaller compute types for simple builds
- Caching dependencies in S3 (Docker layers, npm/pip packages)
- Parallel builds where possible
- On-demand build resources (no reserved capacity)
- S3 Intelligent-Tiering for artifacts
- Auto-terminate test environments after hours
- Use Spot instances for non-critical testing

## Key Service Limits & Numbers

**CodePipeline:**
- 300 pipelines per region (soft limit)
- 50 stages per pipeline (hard limit)
- 50 actions per stage (hard limit)
- 20 parallel actions per stage (hard limit)

**CodeBuild:**
- 60 concurrent builds per region (soft limit, can increase)
- 8 hours max build timeout
- 50 GB max disk space per build

**CodeDeploy:**
- 1,000 applications per region (soft limit)
- 25,000 deployment groups per region (soft limit)
- Blue/green: 48 hours max wait time before termination

**CloudFormation:**
- 200 stacks per region (soft limit)
- 500 resources per stack (soft limit)
- 60 parameters per template (soft limit)
- 200 outputs per template (soft limit)

**Lambda:**
- 15 minutes max execution time
- 10 GB max memory
- 1,000 concurrent executions (soft limit)
- 250 MB deployment package (unzipped)

**Systems Manager:**
- 10,000 parameters per region per account (standard tier)
- 100,000+ parameters (advanced tier)

**Secrets Manager:**
- 500,000 secrets per region (soft limit)
- 65,536 bytes max secret size

## Exam Strategy

### Time Management
- 180 minutes ÷ 75 questions = 2.4 minutes per question
- Scenarios can be long (2-3 paragraphs)
- Don't get stuck on difficult questions
- Flag and move on, return later

### Question Keywords
- **"Most cost-effective"** → Managed services, spot instances, S3 lifecycle
- **"Least operational overhead"** → Managed services, automation, serverless
- **"Secure"** → Secrets Manager, KMS, least privilege IAM, encryption
- **"Automated"** → EventBridge, Lambda, SSM Automation, Config
- **"Zero downtime"** → Blue/green, rolling, canary deployments
- **"Fastest rollback"** → Blue/green deployments, Lambda aliases
- **"Compliance"** → Config, CloudTrail, Security Hub, encryption

### Common Traps
- ❌ Overcomplicating solutions (choose simplest that meets requirements)
- ❌ Ignoring cost considerations
- ❌ Forgetting operational overhead
- ❌ Mixing up service capabilities
- ❌ Not considering security implications

## Essential Documentation & Resources

### AWS Official Documentation
- [📖 DevOps on AWS](https://aws.amazon.com/devops/) - Overview and resources
- [📖 Well-Architected Framework - Operational Excellence Pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)
- [📖 CI/CD on AWS Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/practicing-continuous-integration-continuous-delivery/welcome.html)
- [📖 DevOps Best Practices Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/welcome.html)
- [📖 AWS CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
- [📖 Microservices on AWS](https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/introduction.html)

### Service-Specific Documentation
- [📖 CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/)
- [📖 CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/)
- [📖 CodeDeploy User Guide](https://docs.aws.amazon.com/codedeploy/latest/userguide/)
- [📖 Systems Manager User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/)
- [📖 CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)
- [📖 AWS Config Developer Guide](https://docs.aws.amazon.com/config/latest/developerguide/)

### Hands-on Resources
- [🧪 AWS Workshops - DevOps](https://workshops.aws/categories/DevOps) - Free hands-on labs
- [🧪 AWS Well-Architected Labs - Operational Excellence](https://wellarchitectedlabs.com/operational-excellence/)
- [🎥 AWS re:Invent DevOps Sessions](https://www.youtube.com/results?search_query=aws+reinvent+devops) - Annual conference talks

## Final Exam Checklist

### Knowledge
- [ ] Design complete CI/CD pipelines with AWS services
- [ ] Implement blue/green and canary deployment strategies
- [ ] Create CloudFormation templates with advanced features (StackSets, custom resources)
- [ ] Configure automated remediation with EventBridge, Lambda, SSM
- [ ] Implement comprehensive monitoring with CloudWatch, X-Ray, CloudTrail
- [ ] Design DR solutions with appropriate RTO/RPO
- [ ] Manage secrets and encryption with Secrets Manager and KMS
- [ ] Implement automated compliance with Config
- [ ] Design auto-scaling strategies for various workloads
- [ ] Troubleshoot deployment failures and perform rollbacks

### Experience
- [ ] 2+ years DevOps experience with AWS
- [ ] Built production CI/CD pipelines
- [ ] Deployed applications with zero downtime
- [ ] Implemented monitoring and alerting
- [ ] Managed incidents and performed root cause analysis
- [ ] Automated infrastructure provisioning
- [ ] Implemented security controls and compliance

### Preparation
- [ ] Completed Developer or SysOps Associate (or equivalent)
- [ ] Read DevOps whitepapers
- [ ] Hands-on with all CI/CD services
- [ ] Built CloudFormation templates
- [ ] Practiced deployment strategies
- [ ] Configured monitoring and remediation
- [ ] Practice exams scoring 80%+

---

**Pro Tip:** DOP-C02 emphasizes automation and operational excellence. The exam tests your ability to design fully automated DevOps pipelines with monitoring, security, and incident response. Focus on end-to-end scenarios, not just individual services!

**Good luck!** This certification validates expert-level DevOps skills on AWS. 🚀
