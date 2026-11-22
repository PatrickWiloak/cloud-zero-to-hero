# AWS Certified SAP on AWS - Specialty (PAS-C01) Exam Guide - RETIRED

## Important Notice

**The AWS Certified SAP on AWS - Specialty (PAS-C01) exam was retired in April 2024; the last day to take it was April 29, 2024** ([AWS Training and Certification blog](https://aws.amazon.com/blogs/training-and-certification/aws-certification-retirements-and-launches/), read 2026-11-22). No replacement exam was announced. If you hold the certification, AWS says it stays active for three years from the date you earned it, and it cannot be renewed by retaking the exam. Material preserved as reference for SAP on AWS work.

## Exam Overview

The AWS Certified SAP on AWS - Specialty (PAS-C01) exam validates specialized knowledge and skills in designing, implementing, and operating SAP workloads on the AWS Cloud. This certification demonstrates expertise in SAP architecture, migration, deployment, and operations on AWS.

### Exam Details
- **Exam Code**: PAS-C01
- **Duration**: 170 minutes (2 hours 50 minutes)
- **Format**: Multiple choice and multiple response
- **Number of Questions**: 65 questions (15 unscored)
- **Passing Score**: 750/1000
- **Cost**: $300 USD
- **Delivery**: Testing center or online proctoring
- **Validity**: 3 years
- **Prerequisites**: 5+ years SAP experience, 1+ year AWS SAP experience recommended

## Exam Domains

### Domain 1: Design SAP Workloads on AWS
- Design SAP solutions on AWS according to Well-Architected Framework
- Design account structure and connectivity patterns for SAP on AWS
- Design secure solutions for SAP workloads
- Design optimized and cost-effective infrastructure for SAP
- Design highly resilient SAP solutions

#### Key Focus Areas:
- SAP architecture patterns on AWS
- Multi-AZ and multi-region SAP deployments
- SAP HANA sizing and instance selection
- Network design for SAP landscapes
- Storage solutions for SAP (EBS, EFS, FSx)
- Backup and disaster recovery strategies
- Cost optimization for SAP workloads
- SAP licensing considerations

### Domain 2: Deploy SAP Workloads on AWS
- Deploy SAP databases on AWS
- Deploy SAP applications on AWS
- Integrate AWS services with SAP workloads

#### Key Focus Areas:
- SAP HANA installation and configuration
- SAP NetWeaver deployment
- SAP S/4HANA deployment methodologies
- SAP application servers on EC2
- AWS Launch Wizard for SAP
- SAP Fiori deployment
- SAP Solution Manager integration
- AWS Systems Manager for SAP management

### Domain 3: Configure High Availability and Disaster Recovery
- Configure high availability for SAP workloads
- Configure disaster recovery setup for SAP workloads
- Implement backup and restore strategies

#### Key Focus Areas:
- SAP HANA High Availability (HSR)
- SAP application server high availability
- Pacemaker cluster configuration
- Multi-AZ SAP deployments
- Cross-region DR for SAP
- HANA System Replication configuration
- AWS Backup for SAP
- Automated failover testing

### Domain 4: Migrate SAP Workloads to AWS
- Plan SAP migration strategies
- Execute SAP migrations to AWS
- Validate migrated SAP systems

#### Key Focus Areas:
- Migration assessment and planning
- Homogeneous vs heterogeneous migrations
- SAP migration tools (SWPM, DMO, Database Migration Option)
- AWS Application Migration Service
- AWS Database Migration Service for SAP
- Cutover planning and execution
- Post-migration validation and optimization
- SAP Landscape Transformation Replication Server

### Domain 5: Automate and Validate SAP Deployments
- Automate SAP deployments using AWS services
- Validate AWS infrastructure for SAP workloads
- Monitor and optimize SAP on AWS

#### Key Focus Areas:
- Infrastructure as Code for SAP (CloudFormation, Terraform)
- AWS Launch Wizard for SAP automation
- SAP on AWS Quick Start deployments
- AWS Systems Manager for automation
- SAP Early Watch Alert integration
- Performance monitoring and tuning
- Cost monitoring and optimization
- Compliance and governance

## Key AWS Services for SAP Workloads

### Compute Services
- **Amazon EC2**: SAP certified instances (memory-optimized, high-memory, compute-optimized)
- **EC2 Instance Types**: X1, X1e, R5, R6i, M5, M6i, C5, C6i
- **SAP HANA Certified Instances**: Up to 24TB memory single-node
- **Placement Groups**: Cluster placement for low-latency
- **Dedicated Hosts**: For specific licensing requirements
- **EC2 Image Builder**: Automated AMI creation

### Storage Services
- **Amazon EBS**: Primary storage for SAP (io2, gp3 volumes)
- **Amazon EFS**: Shared file systems (SAP transport directory, interfaces)
- **Amazon FSx for Windows File Server**: Windows-based SAP systems
- **Amazon S3**: Backup storage and data lakes
- **AWS Backup**: Centralized backup management
- **EBS Snapshots**: Point-in-time backups

### Database Services
- **SAP HANA on EC2**: Primary database platform
- **Amazon RDS**: For SAP ASE, Oracle, SQL Server
- **Amazon Aurora**: For compatible SAP workloads
- **AWS Database Migration Service**: Migration support

### Networking Services
- **Amazon VPC**: Network isolation for SAP landscapes
- **AWS Direct Connect**: Dedicated connectivity to on-premises
- **AWS Transit Gateway**: Hub for SAP landscape connectivity
- **Route 53**: DNS management for SAP systems
- **Elastic Load Balancing**: Application load distribution
- **VPC Endpoints**: Private connectivity to AWS services

### Management and Operations
- **AWS Systems Manager**: SAP lifecycle management
- **AWS Launch Wizard for SAP**: Automated SAP deployment
- **Amazon CloudWatch**: Monitoring and alerting
- **AWS CloudTrail**: API activity logging
- **AWS Config**: Configuration compliance
- **AWS Service Catalog**: Standardized SAP deployments

### Security and Compliance
- **AWS IAM**: Access management
- **AWS KMS**: Encryption key management
- **AWS Secrets Manager**: Credential management
- **AWS Certificate Manager**: SSL/TLS certificates
- **AWS Security Hub**: Security posture management
- **Amazon GuardDuty**: Threat detection

## SAP Architecture Patterns on AWS

### Three-Tier SAP Architecture
```
Presentation Tier: SAP Fiori, SAP GUI
Application Tier: SAP NetWeaver Application Servers
Database Tier: SAP HANA
```

### High Availability Architecture
- **Multi-AZ Deployment**: Application servers across AZs
- **HANA System Replication (HSR)**: Primary and secondary HANA nodes
- **Pacemaker Cluster**: Automated failover orchestration
- **Application Server Redundancy**: Multiple app servers with load balancing
- **EBS Multi-Attach**: Shared storage for cluster
- **Overlay IP**: Virtual IP for failover

### Disaster Recovery Architecture
- **Primary Site**: Production SAP landscape
- **DR Site**: Secondary region with standby systems
- **HANA System Replication Async**: Cross-region replication
- **Automated Failover**: Route 53 health checks and failover routing
- **RPO/RTO**: Define recovery objectives
- **Regular DR Testing**: Validate failover procedures

### SAP Landscape on AWS
- **Development System (DEV)**: Development and unit testing
- **Quality Assurance (QAS)**: Integration and regression testing
- **Production (PRD)**: Live business operations
- **Sandbox (SBX)**: Training and experimentation
- **Network Segregation**: Separate VPCs or subnets per system
- **Shared Services**: Central services (SAP Solution Manager, SAP Router)

## SAP on AWS Deployment Methods

### 1. AWS Launch Wizard for SAP
- Guided SAP deployment wizard
- Automated infrastructure provisioning
- SAP software installation automation
- Pre-configured best practices
- CloudFormation-based deployment
- Supports SAP NetWeaver and S/4HANA

### 2. SAP on AWS Quick Starts
- Reference deployments on GitHub
- CloudFormation templates
- Comprehensive deployment guides
- Multiple architecture options
- Community contributions

### 3. Manual Deployment
- Custom infrastructure design
- SAP Software Provisioning Manager (SWPM)
- hdblcm for HANA installation
- Full control over configuration
- Suitable for complex requirements

### 4. SAP Cloud Appliance Library (CAL)
- Pre-configured SAP solutions
- Rapid deployment for demos/PoCs
- Pay-as-you-go pricing
- Limited customization

## SAP Migration Strategies

### 1. Lift and Shift (Rehost)
- Move existing SAP system to AWS without changes
- Fastest migration approach
- Maintain current SAP version and OS
- Use AWS Application Migration Service or VM Import/Export

### 2. Database Migration (Replatform)
- Migrate to different database (e.g., AnyDB to HANA)
- Use SAP Database Migration Option (DMO)
- Opportunity for SAP upgrades
- Unicode conversion if needed

### 3. SAP S/4HANA Conversion (Refactor)
- Move to S/4HANA during migration
- Brownfield (conversion) or Greenfield (new implementation)
- Use SAP Software Update Manager (SUM) with DMO
- Business process optimization

### 4. Hybrid Approach
- Phased migration of SAP components
- Keep certain components on-premises initially
- Direct Connect for hybrid connectivity
- Gradual cloud adoption

## SAP-Specific AWS Features

### SAP HANA Backup/Restore on AWS
- **AWS Backint Agent**: Native HANA backup to S3
- **Incremental Backups**: Efficient backup strategy
- **Cross-Region Replication**: S3 CRR for DR
- **Lifecycle Policies**: Automated backup retention
- **Fast Restore**: High-bandwidth S3 access

### SAP Transport Management
- **EFS for Transport Directory**: Shared /usr/sap/trans
- **S3 for Transport Archive**: Long-term storage
- **SAP Transport Management System**: stms configuration
- **Automated Transport**: Scripts and workflows

### SAP Monitoring on AWS
- **Enhanced Monitoring Scripts**: SAP-provided CloudWatch integration
- **Custom CloudWatch Metrics**: SAP-specific KPIs
- **SAP Solution Manager**: Integration with AWS metrics
- **CloudWatch Dashboards**: Unified SAP monitoring
- **Third-Party Tools**: Datadog, Dynatrace, New Relic integration

## Study Strategy

### Prerequisites
- Strong SAP technical knowledge (Basis, HANA)
- Understanding of SAP architecture and components
- AWS foundational knowledge
- Linux/Windows system administration

### Phase 1: SAP on AWS Fundamentals (Weeks 1-2)
- SAP architecture on AWS
- EC2 instance types for SAP
- Storage options for SAP workloads
- Networking design for SAP

### Phase 2: SAP Deployment (Weeks 3-5)
- Launch Wizard for SAP
- Manual SAP HANA installation
- SAP NetWeaver deployment
- Quick Start deployments

### Phase 3: High Availability and DR (Weeks 6-8)
- HANA System Replication
- Pacemaker cluster setup
- Multi-AZ architectures
- Cross-region DR implementation

### Phase 4: Migration (Weeks 9-10)
- Migration planning and assessment
- Migration tools and methodologies
- Cutover strategies
- Post-migration optimization

### Phase 5: Operations and Automation (Weeks 11-12)
- Backup and restore procedures
- Monitoring and alerting
- Automation with Systems Manager
- Cost optimization strategies

### Phase 6: Review and Practice (Weeks 13-14)
- Practice exams
- Hands-on scenarios
- SAP Notes review
- AWS whitepapers

## 📚 Comprehensive Study Resources

**👉 [Complete AWS Study Resources Guide](../../../../.templates/resources-aws.md)**

### Quick Links (PAS-C01 Specific)
- **[PAS-C01 Official Exam Page](https://aws.amazon.com/certification/)** - Registration
- **[SAP on AWS Documentation](https://docs.aws.amazon.com/sap/)** - Complete guides
- **[SAP on AWS Blog](https://aws.amazon.com/blogs/awsforsap/)** - Latest updates
- **[SAP Community on AWS](https://community.sap.com/)** - Community discussions

### SAP-Specific Resources
- **SAP on AWS Quick Start**: https://docs.aws.amazon.com/launchwizard/latest/userguide/launch-wizard-sap.html
- **SAP Notes**: 1656250, 2015404, 2456406 (AWS-specific)
- **AWS Launch Wizard for SAP**: Automated deployment tool
- **SAP on AWS Architecture Guides**: Best practices and reference architectures

## Common Exam Scenarios

### SAP HANA Sizing and Deployment
- Determine correct EC2 instance type based on SAPS requirements
- Choose appropriate storage configuration (EBS types, RAID)
- Design network architecture for SAP landscape
- Implement security best practices

### High Availability Setup
- Configure HANA System Replication (sync/async)
- Set up Pacemaker cluster with Overlay IP
- Implement application server redundancy
- Test automated failover procedures

### SAP Migration Planning
- Assess current SAP landscape
- Choose appropriate migration strategy
- Plan network connectivity (Direct Connect)
- Design DR strategy for migrated systems

### Backup and Recovery
- Implement AWS Backint for HANA backups
- Configure retention policies
- Test restore procedures
- Design cross-region backup strategy

## Exam Preparation Tips

### Hands-on Experience
1. Deploy SAP systems using Launch Wizard
2. Configure HANA System Replication
3. Implement Pacemaker cluster
4. Practice SAP migration scenarios
5. Set up monitoring and backup

### SAP Notes to Review
- **1656250**: SAP on AWS - General information
- **2015404**: SAP HANA on AWS support and deployment
- **2456406**: AWS Launch Wizard for SAP support
- **2927211**: SAP HANA on AWS backup with AWS Backint Agent

### Common Pitfalls
- Not understanding SAP-specific requirements
- Missing SAP certification requirements for instances
- Incorrect HANA System Replication configuration
- Overlooking SAP licensing implications
- Insufficient network bandwidth planning

## Next Steps After Certification

### Career Advancement
- SAP on AWS architect roles
- Cloud migration specialist (SAP focus)
- SAP Basis consultant with cloud expertise
- Enterprise SAP solution architect
- SAP-AWS integration consultant

### Continuous Learning
- Stay updated with new SAP on AWS features
- SAP S/4HANA cloud deployments
- SAP Business Technology Platform (BTP) integration
- Advanced automation and DevOps for SAP
- Multi-cloud SAP strategies
