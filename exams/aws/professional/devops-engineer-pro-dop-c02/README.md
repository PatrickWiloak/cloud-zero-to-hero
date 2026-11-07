# AWS Certified DevOps Engineer - Professional (DOP-C02) Exam Guide

## Exam Overview

The AWS Certified DevOps Engineer - Professional (DOP-C02) exam validates advanced technical skills and experience in provisioning, operating, and managing distributed application systems on the AWS platform. This certification demonstrates expertise in implementing and automating continuous delivery systems and methodologies on AWS.

### Exam Details
- **Exam Code**: DOP-C02
- **Duration**: 180 minutes (3 hours)
- **Format**: Multiple choice and multiple response
- **Number of Questions**: 75 questions
- **Passing Score**: 750/1000
- **Cost**: $300 USD
- **Language**: Available in multiple languages
- **Delivery**: Testing center or online proctoring
- **Validity**: 3 years
- **Prerequisites**: Strong DevOps experience and AWS Associate-level knowledge recommended

## Exam Domains

### Domain 1: SDLC Automation (22% of scored content)
- Implement CI/CD pipelines
- Integrate automated testing into CI/CD pipelines
- Build and manage artifacts
- Implement deployment strategies (blue/green, canary, rolling)

#### Key Focus Areas:
- AWS CodePipeline, CodeBuild, CodeDeploy, CodeCommit
- AWS CodeArtifact and artifact management
- Container registries (ECR)
- Deployment strategies and rollback mechanisms
- Integration with third-party tools (GitHub, Jenkins, Bitbucket)
- Lambda deployment with SAM and CDK
- ECS/EKS blue/green deployments

### Domain 2: Configuration Management and Infrastructure as Code (17% of scored content)
- Define cloud infrastructure using CloudFormation or CDK
- Implement automated configuration management
- Define workload-level configuration

#### Key Focus Areas:
- AWS CloudFormation advanced features (StackSets, nested stacks, change sets)
- AWS CDK for infrastructure as code
- Terraform on AWS
- AWS Systems Manager for configuration management
- OpsWorks for Chef and Puppet (retired: end of life 26 May 2024; use Systems Manager) - know it only to rule it out
- AWS AppConfig for application configuration
- Parameter Store and Secrets Manager
- AWS Service Catalog for governance

### Domain 3: Resilient Cloud Solutions (15% of scored content)
- Implement highly available solutions
- Implement solutions that are tolerant of failures
- Implement disaster recovery strategies

#### Key Focus Areas:
- Multi-AZ and multi-region architectures
- Auto Scaling and load balancing
- RDS Multi-AZ, Aurora Global Database
- DynamoDB Global Tables
- S3 cross-region replication
- Route 53 health checks and failover
- Backup and restore strategies
- Disaster recovery (backup/restore, pilot light, warm standby, multi-site active-active)
- Chaos engineering with AWS Fault Injection Simulator

### Domain 4: Monitoring and Logging (15% of scored content)
- Monitor and log system events
- Implement monitoring and alerting solutions
- Configure log aggregation and analysis
- Implement performance optimization

#### Key Focus Areas:
- CloudWatch metrics, logs, alarms, dashboards
- CloudWatch Logs Insights and CloudWatch Contributor Insights
- X-Ray for distributed tracing
- CloudTrail for API auditing
- VPC Flow Logs for network monitoring
- AWS Config for configuration tracking
- EventBridge for event-driven architectures
- SNS, SQS for notifications
- Third-party monitoring tools integration (Datadog, New Relic, Splunk)

### Domain 5: Incident and Event Response (14% of scored content)
- Troubleshoot issues and determine their root cause
- Automate event management and alerting
- Implement automated healing

#### Key Focus Areas:
- AWS Systems Manager for incident response
- EventBridge for automated response
- Lambda for automated remediation
- SNS for incident notifications
- Step Functions for orchestrating recovery workflows
- AWS Systems Manager OpsCenter for incident management
- Automated rollback strategies
- Health checks and automated recovery

### Domain 6: Security and Compliance (17% of scored content)
- Implement and manage security policies
- Implement data and infrastructure protection strategies
- Perform compliance validation

#### Key Focus Areas:
- IAM policies, roles, and permission boundaries
- KMS for encryption and key management
- AWS Secrets Manager for secrets rotation
- Security Hub for security posture management
- GuardDuty for threat detection
- AWS Config rules for compliance
- Inspector for vulnerability scanning
- VPC security (Security Groups, NACLs, VPC endpoints)
- AWS WAF and Shield for application protection
- Certificate Manager for SSL/TLS
- Compliance frameworks (PCI DSS, HIPAA, SOC 2)

## Key DevOps Services and Tools

### CI/CD Pipeline Services

#### AWS CodePipeline
- Multi-stage pipeline orchestration
- Integration with AWS and third-party tools
- Manual approval gates
- Parallel and sequential actions
- Cross-region and cross-account deployments
- Artifact management
- Pipeline event notifications

#### AWS CodeBuild
- Managed build service
- Docker-based build environments
- Custom build images
- Buildspec.yml configuration
- Caching for faster builds
- Build badges and notifications
- Integration with ECR for container builds

#### AWS CodeDeploy
- Automated application deployments
- EC2, Lambda, and ECS deployments
- Deployment configurations (in-place, blue/green)
- Traffic shifting strategies
- Automatic rollback on failures
- Deployment monitoring and hooks

### Infrastructure as Code

#### AWS CloudFormation
- Template-based infrastructure provisioning
- Stack management and updates
- StackSets for multi-account deployments
- Nested stacks for modular design
- Change sets for preview
- Drift detection
- Custom resources with Lambda
- CloudFormation Registry for third-party resources

#### AWS CDK
- Define infrastructure using programming languages
- High-level constructs (L1, L2, L3)
- AWS Construct Library
- CDK Pipelines for self-mutating pipelines
- TypeScript, Python, Java, C#, Go support
- Synthesize to CloudFormation

### Container Orchestration

#### Amazon ECS
- Fargate for serverless containers
- EC2 launch type for more control
- Service auto-scaling
- Task definitions and task roles
- Service discovery with Cloud Map
- Blue/green deployments with CodeDeploy
- Container Insights for monitoring

#### Amazon EKS
- Managed Kubernetes service
- EKS Anywhere for on-premises
- Fargate for serverless pods
- Node groups and managed node groups
- IRSA (IAM Roles for Service Accounts)
- EKS add-ons (CoreDNS, kube-proxy, VPC CNI)
- GitOps with Flux or ArgoCD

### Configuration and Operations

#### AWS Systems Manager
- Session Manager for secure access
- Run Command for remote execution
- State Manager for configuration compliance
- Patch Manager for OS patching
- Automation for runbooks
- OpsCenter for incident management
- Change Calendar for change windows
- Distributor for package distribution

## Study Strategy

### Phase 1: Foundation (Weeks 1-2)
- Review AWS core services
- Understand DevOps principles and practices
- CI/CD pipeline fundamentals
- Version control with Git

### Phase 2: SDLC Automation (Weeks 3-5)
- Build complete CI/CD pipelines
- Implement automated testing
- Container and serverless deployments
- Deployment strategies

### Phase 3: Infrastructure as Code (Weeks 6-7)
- CloudFormation advanced features
- AWS CDK development
- Configuration management
- Multi-account strategies

### Phase 4: Resilience and Monitoring (Weeks 8-10)
- High availability architectures
- Disaster recovery implementation
- Monitoring and observability
- Performance optimization

### Phase 5: Security and Incident Response (Weeks 11-12)
- Security automation
- Compliance as code
- Automated incident response
- Security best practices

### Phase 6: Review and Practice (Weeks 13-14)
- Complete practice exams
- Hands-on scenario practice
- Review weak areas
- Time management practice

## Common Exam Scenarios

### CI/CD Pipeline Design
- Multi-stage pipeline with approval gates
- Blue/green deployment for zero downtime
- Canary deployments with traffic shifting
- Automated rollback on failures
- Cross-account and cross-region deployments

### Infrastructure as Code
- Multi-account CloudFormation StackSets
- Self-mutating pipelines with CDK
- Configuration management with Systems Manager
- Secrets rotation automation
- Compliance as code with Config rules

### High Availability and DR
- Multi-region active-active architecture
- Automated failover with Route 53
- Database replication strategies
- Backup automation with AWS Backup
- Disaster recovery testing with FIS

### Monitoring and Incident Response
- Centralized logging with CloudWatch
- Distributed tracing with X-Ray
- Automated alerting and remediation
- Performance optimization
- Cost monitoring and optimization

## 📚 Comprehensive Study Resources

**👉 [Complete AWS Study Resources Guide](../../../../.templates/resources-aws.md)**

### Quick Links (DOP-C02 Specific)
- **[DOP-C02 Official Exam Page](https://aws.amazon.com/certification/certified-devops-engineer-professional/)** - Registration
- **[AWS DevOps Skill Builder](https://skillbuilder.aws/)** - FREE DevOps courses
- **[AWS DevOps Blog](https://aws.amazon.com/blogs/devops/)** - Latest DevOps practices
- **[AWS DevOps Documentation](https://docs.aws.amazon.com/)** - Service guides

## Exam Preparation Tips

### Study Approach
1. **Strong AWS Foundation**: Ensure solid understanding of core AWS services
2. **Hands-on DevOps**: Build complete CI/CD pipelines from scratch
3. **Real-world Experience**: 2+ years of DevOps on AWS recommended
4. **Practice Scenarios**: Work through complex multi-service scenarios
5. **Time Management**: Practice with timed exams

### Exam Strategy
1. **Time Allocation**: ~2.4 minutes per question
2. **Scenario Analysis**: Identify requirements, constraints, and trade-offs
3. **Best Practices**: Choose solutions following DevOps best practices
4. **Eliminate Options**: Rule out clearly incorrect answers
5. **Mark for Review**: Flag uncertain questions and return if time permits

## Next Steps After Certification

### Career Advancement
- DevOps architect and consultant roles
- Cloud automation specialist
- Site reliability engineer (SRE)
- Platform engineering leadership
- DevOps training and mentorship

### Continuous Learning
- Advanced container orchestration (Kubernetes)
- GitOps practices and tooling
- Observability and chaos engineering
- Cloud security and compliance automation
- Multi-cloud DevOps strategies
