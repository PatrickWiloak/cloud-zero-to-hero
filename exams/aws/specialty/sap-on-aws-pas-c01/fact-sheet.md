---
last-updated: 2026-05-03
---

# AWS Certified SAP on AWS - Specialty (PAS-C01) Fact Sheet

## 📋 Exam Overview

**Exam Code:** PAS-C01
**Exam Name:** AWS Certified SAP on AWS - Specialty
**Duration:** 170 minutes (2 hours 50 minutes)
**Questions:** 65 questions
**Question Format:** Multiple choice and multiple response
**Passing Score:** 750/1000 (scaled scoring, approximately 75%)
**Cost:** $300 USD
**Valid For:** 3 years
**Prerequisites:** Recommended AWS Solutions Architect Associate or equivalent experience
**Language:** Available in English, Japanese, Korean, Simplified Chinese
**Delivery:** Pearson VUE (online proctored or testing center)

**📖 [Official Exam Page](https://aws.amazon.com/certification/)** - Registration and details
**📖 [Exam Guide PDF](https://d1.awsstatic.com/training-and-certification/docs-sap-on-aws-specialty/AWS-Certified-SAP-on-AWS-Specialty_Exam-Guide.pdf)** - Detailed exam objectives
**📖 [Sample Questions](https://d1.awsstatic.com/training-and-certification/docs-sap-on-aws-specialty/AWS-Certified-SAP-on-AWS-Specialty_Sample-Questions.pdf)** - Official practice questions

## 🎯 Target Audience

This certification is designed for:
- SAP Basis administrators managing SAP on AWS
- SAP architects designing SAP solutions on AWS
- Cloud architects with SAP workload experience
- SAP consultants implementing AWS migrations
- DevOps engineers managing SAP environments

**Required Experience:**
- 5+ years SAP Basis administration experience
- 1+ years operating SAP workloads on AWS
- AWS infrastructure and services knowledge
- SAP landscape architecture understanding

**📖 [SAP on AWS Overview](https://aws.amazon.com/sap/)** - AWS SAP solutions
**📖 [SAP on AWS Documentation](https://docs.aws.amazon.com/sap/)** - Complete SAP documentation

## 📚 Exam Domains

### Domain 1: Design SAP Workloads on AWS (30%)

This is the largest domain, covering SAP architecture design on AWS.

#### 1.1 SAP Architecture Fundamentals

**SAP System Components:**
- SAP NetWeaver architecture (ABAP, Java)
- SAP HANA database architecture
- SAP application servers (ASCS, PAS, AAS)
- SAP Web Dispatcher
- SAP Router and landscape connectivity

**📖 [SAP on AWS Architecture](https://aws.amazon.com/sap/)** - Reference architectures
**📖 [SAP HANA on AWS](https://aws.amazon.com/sap/)** - HANA deployment
**📖 [SAP NetWeaver on AWS](https://docs.aws.amazon.com/sap/latest/general/arch-guide-architecture-guidelines-and-decisions.html)** - NetWeaver architecture
**📖 [SAP System Requirements](https://docs.aws.amazon.com/sap/latest/general/system-requirements.html)** - Planning requirements

#### 1.2 EC2 Instance Selection for SAP

**SAP-Certified Instance Types:**
- X1, X1e, X2 instances (memory-optimized for HANA)
- R5, R6i, R7i instances (general-purpose SAP)
- U-series instances (high-memory HANA)
- Graviton-based instances (ARM architecture)

**📖 [SAP-Certified EC2 Instances](https://aws.amazon.com/sap/instance-types/)** - Certified instances
**📖 [X2 Instances for SAP HANA](https://aws.amazon.com/ec2/instance-types/x2/)** - High-memory instances
**📖 [High Memory Instances](https://aws.amazon.com/ec2/instance-types/high-memory/)** - Up to 24TB RAM
**📖 [SAP HANA Hardware Directory](https://www.sap.com/dmc/exp/2014-09-02-hana-hardware/enEN/#/solutions?filters=v:deCertified;iaas;ve:23)** - AWS certifications
**📖 [Instance Sizing](https://docs.aws.amazon.com/sap/latest/general/ec2-instances.html)** - Choosing instance types

#### 1.3 Storage Design for SAP

**Storage Options:**
- EBS for SAP HANA data and log volumes
- EBS gp3, io2 for performance requirements
- EFS for SAP transport directories
- S3 for backups and archives
- FSx for NetApp ONTAP for SAP shared storage

**📖 [SAP Storage Best Practices](https://docs.aws.amazon.com/sap/latest/general/storage-config.html)** - Storage configuration
**📖 [EBS for SAP HANA](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-storage-ebs.html)** - HANA storage
**📖 [EBS Performance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)** - Volume types
**📖 [FSx for ONTAP](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/what-is-fsx-ontap.html)** - Shared storage
**📖 [EFS for SAP](https://docs.aws.amazon.com/sap/latest/general/efs-for-sap.html)** - Elastic File System

#### 1.4 Network Design

**VPC Configuration:**
- Multi-AZ architecture for high availability
- Private subnets for SAP workloads
- NAT Gateways for outbound connectivity
- VPN and Direct Connect for hybrid
- Transit Gateway for multi-VPC

**📖 [SAP Network Architecture](https://docs.aws.amazon.com/sap/latest/general/networking.html)** - Network design
**📖 [VPC for SAP](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)** - Virtual private cloud
**📖 [AWS Direct Connect](https://aws.amazon.com/directconnect/)** - Dedicated connectivity
**📖 [Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html)** - Network hub
**📖 [Placement Groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html)** - Low-latency networking

#### 1.5 High Availability and Disaster Recovery

**HA Architecture:**
- Multi-AZ deployments
- SAP HANA System Replication (HSR)
- Pacemaker cluster for failover
- Application Server clustering
- Database replication strategies

**📖 [SAP HA on AWS](https://docs.aws.amazon.com/sap/latest/sap-hana/sap-hana-on-aws-ha-and-dr.html)** - High availability
**📖 [HANA System Replication](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-hsr.html)** - HSR configuration
**📖 [Pacemaker Clustering](https://docs.aws.amazon.com/sap/latest/sap-hana/sap-hana-on-aws-cluster-configuration.html)** - Cluster setup
**📖 [Multi-AZ Architecture](https://docs.aws.amazon.com/sap/latest/general/arch-guide-ha-dr.html)** - DR patterns

**Disaster Recovery:**
- Cross-region replication
- Backup and restore strategies
- Pilot light and warm standby
- RTO and RPO considerations

**📖 [SAP DR Strategies](https://docs.aws.amazon.com/sap/latest/general/disaster-recovery.html)** - DR planning
**📖 [AWS Backup for SAP](https://docs.aws.amazon.com/sap/latest/general/backup-restore.html)** - Backup solutions
**📖 [Cross-Region Replication](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-dr.html)** - DR setup

### Domain 2: Implement SAP Workloads on AWS (30%)

Covers SAP deployment, migration, and configuration.

#### 2.1 SAP Deployment Methods

**Deployment Options:**
- AWS Launch Wizard for SAP
- SAP Cloud Appliance Library (CAL)
- AWS CloudFormation templates
- Manual installation
- SAP Software Provisioning Manager (SWPM)

**📖 [AWS Launch Wizard for SAP](https://docs.aws.amazon.com/launchwizard/latest/userguide/what-is-launch-wizard-sap.html)** - Automated deployment
**📖 [Launch Wizard Guide](https://docs.aws.amazon.com/launchwizard/latest/userguide/launch-wizard-sap-deploying.html)** - Deployment steps
**📖 [SAP Cloud Appliance Library](https://cal.sap.com/)** - SAP CAL
**📖 [CloudFormation for SAP](https://docs.aws.amazon.com/launchwizard/latest/userguide/launch-wizard-sap.html)** - Quick Start templates
**📖 [SAP Installation Guide](https://docs.aws.amazon.com/sap/latest/general/installation.html)** - Manual installation

#### 2.2 SAP HANA Installation

**Installation Steps:**
- Instance preparation and prerequisites
- Storage configuration (data, log, shared)
- HANA database installation
- System replication setup
- Backup configuration

**📖 [SAP HANA Installation](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-install.html)** - Installation guide
**📖 [HANA Prerequisites](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-prereq.html)** - Pre-installation
**📖 [HANA Storage Setup](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-storage-ebs.html)** - Storage configuration
**📖 [HANA Backup Setup](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-backup.html)** - Backup configuration

#### 2.3 SAP NetWeaver Installation

**Application Server Deployment:**
- ASCS/ERS installation
- Database instance configuration
- Primary Application Server (PAS)
- Additional Application Servers (AAS)
- SAP Web Dispatcher configuration

**📖 [SAP NetWeaver on AWS](https://docs.aws.amazon.com/sap/latest/sap-netweaver/netweaver-installation.html)** - NetWeaver deployment
**📖 [ASCS Installation](https://docs.aws.amazon.com/sap/latest/sap-netweaver/netweaver-ascs.html)** - Central services
**📖 [Application Server Setup](https://docs.aws.amazon.com/sap/latest/sap-netweaver/netweaver-app-server.html)** - App servers

#### 2.4 SAP Migration to AWS

**Migration Strategies:**
- Homogeneous system copy (same OS/DB)
- Heterogeneous system copy (different OS/DB)
- SAP Database Migration Option (DMO)
- Classical migration approach
- Lift-and-shift vs re-architecture

**📖 [SAP Migration Guide](https://docs.aws.amazon.com/sap/latest/general/migration-overview.html)** - Migration planning
**📖 [Migration Strategies](https://docs.aws.amazon.com/sap/latest/general/migration-strategies.html)** - Approach comparison
**📖 [SAP DMO](https://docs.aws.amazon.com/sap/latest/general/migration-dmo.html)** - Database Migration Option
**📖 [AWS MGN for SAP](https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html)** - Application Migration Service
**📖 [AWS DMS](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html)** - Database Migration Service

#### 2.5 SAP Landscape Configuration

**Transport Management:**
- Transport directories on EFS
- Transport routes configuration
- Change and transport system (CTS)
- SAP Solution Manager integration

**📖 [SAP Transport Management](https://docs.aws.amazon.com/sap/latest/general/transport-management.html)** - TMS configuration
**📖 [Shared Storage for Transports](https://docs.aws.amazon.com/sap/latest/general/efs-for-sap.html)** - EFS for /sapmnt

**System Landscape:**
- Development, Quality, Production setup
- System landscape directory (SLD)
- SAP router configuration
- Landscape monitoring

**📖 [SAP Landscape Design](https://docs.aws.amazon.com/sap/latest/general/landscape-design.html)** - Multi-system architecture

### Domain 3: Manage and Operate SAP Workloads on AWS (24%)

Covers day-to-day operations, monitoring, and management.

#### 3.1 SAP System Administration on AWS

**Operational Tasks:**
- Starting and stopping SAP systems
- Instance lifecycle management
- System refreshes and copies
- Applying SAP patches and updates
- License management

**📖 [SAP Operations Guide](https://docs.aws.amazon.com/sap/latest/general/operations.html)** - Daily operations
**📖 [Start/Stop Automation](https://docs.aws.amazon.com/sap/latest/general/start-stop-automation.html)** - Automated scheduling
**📖 [System Copy](https://docs.aws.amazon.com/sap/latest/general/system-copy.html)** - Copy procedures
**📖 [SAP Patching](https://docs.aws.amazon.com/sap/latest/general/patching.html)** - Update procedures

#### 3.2 Backup and Recovery

**Backup Strategies:**
- SAP HANA backups (data and log)
- AWS Backup for SAP HANA
- AWS Backint Agent
- Snapshots vs file-based backups
- Backup to S3

**📖 [SAP Backup Strategies](https://docs.aws.amazon.com/sap/latest/general/backup-restore.html)** - Backup planning
**📖 [HANA Backup](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-backup.html)** - HANA-specific backups
**📖 [AWS Backint Agent](https://docs.aws.amazon.com/sap/latest/sap-hana/aws-backint-agent.html)** - Native S3 backup
**📖 [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/working-with-sap-hana.html)** - Managed backup service
**📖 [EBS Snapshots](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)** - Volume snapshots

**Recovery Procedures:**
- Point-in-time recovery
- System restore from backup
- Disaster recovery failover
- Data recovery procedures

**📖 [SAP Recovery](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-recovery.html)** - Recovery procedures
**📖 [DR Testing](https://docs.aws.amazon.com/sap/latest/general/dr-testing.html)** - Testing DR plans

#### 3.3 Monitoring SAP on AWS

**AWS Monitoring Services:**
- CloudWatch for infrastructure metrics
- CloudWatch Logs for SAP logs
- CloudWatch alarms for alerting
- AWS Systems Manager for patch management
- SAP on AWS monitoring dashboard

**📖 [Monitoring SAP on AWS](https://docs.aws.amazon.com/sap/latest/general/monitoring.html)** - Monitoring strategy
**📖 [CloudWatch for SAP](https://docs.aws.amazon.com/sap/latest/general/cloudwatch-monitoring.html)** - CloudWatch integration
**📖 [CloudWatch Agent](https://docs.aws.amazon.com/sap/latest/general/cloudwatch-agent.html)** - Agent configuration
**📖 [Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html)** - Operational management

**SAP Monitoring Tools:**
- SAP Solution Manager
- SAP HANA Cockpit
- SAP Host Agent
- DBA Cockpit
- Transaction codes (SM50, ST22, etc.)

**📖 [SAP Solution Manager on AWS](https://docs.aws.amazon.com/sap/latest/general/solution-manager.html)** - SolMan deployment
**📖 [SAP Host Agent](https://docs.aws.amazon.com/sap/latest/general/host-agent.html)** - Agent configuration

#### 3.4 Performance Optimization

**Performance Tuning:**
- EC2 instance right-sizing
- EBS optimization (IOPS, throughput)
- Network performance (enhanced networking)
- SAP HANA memory management
- Database and application optimization

**📖 [Performance Tuning](https://docs.aws.amazon.com/sap/latest/general/performance.html)** - Optimization guide
**📖 [HANA Performance](https://docs.aws.amazon.com/sap/latest/sap-hana/hana-ops-performance.html)** - HANA tuning
**📖 [Enhanced Networking](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking.html)** - Network optimization
**📖 [EBS Performance Tuning](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-io-characteristics.html)** - Storage optimization

#### 3.5 Cost Optimization

**Cost Management:**
- Reserved Instances for SAP
- Savings Plans
- Spot Instances for non-production
- Auto-scaling for development/test
- Right-sizing recommendations

**📖 [SAP Cost Optimization](https://docs.aws.amazon.com/sap/latest/general/cost-optimization.html)** - Cost strategies
**📖 [Reserved Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/)** - RI pricing
**📖 [Savings Plans](https://aws.amazon.com/savingsplans/)** - Flexible pricing
**📖 [Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)** - Cost analysis

### Domain 4: Secure SAP Workloads on AWS (16%)

Covers security, compliance, and access control.

#### 4.1 SAP Security Best Practices

**Security Layers:**
- Network security (VPC, security groups)
- Operating system hardening
- SAP application security
- Database security
- Data encryption

**📖 [SAP Security on AWS](https://docs.aws.amazon.com/sap/latest/general/security.html)** - Security overview
**📖 [Security Best Practices](https://docs.aws.amazon.com/sap/latest/general/security-best-practices.html)** - Security guidelines
**📖 [SAP Security Notes](https://support.sap.com/en/my-support/knowledge-base/security-notes-news.html)** - SAP security updates

#### 4.2 Identity and Access Management

**IAM for SAP:**
- IAM roles for EC2 instances
- Service accounts for automation
- MFA for administrative access
- Least privilege principle
- Cross-account access

**📖 [IAM for SAP](https://docs.aws.amazon.com/sap/latest/general/iam.html)** - Access management
**📖 [IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)** - Role-based access
**📖 [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)** - Security recommendations

**SAP User Management:**
- SAP user administration
- Integration with Active Directory
- Single Sign-On (SSO)
- Privileged user management

**📖 [SAP Authentication](https://docs.aws.amazon.com/sap/latest/general/authentication.html)** - User authentication

#### 4.3 Data Protection

**Encryption:**
- EBS volume encryption
- S3 encryption for backups
- Encryption in transit (TLS/SSL)
- AWS KMS for key management
- SAP Secure Network Communication (SNC)

**📖 [Data Encryption](https://docs.aws.amazon.com/sap/latest/general/encryption.html)** - Encryption strategies
**📖 [EBS Encryption](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)** - Volume encryption
**📖 [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)** - Key management
**📖 [S3 Encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html)** - Object encryption

#### 4.4 Network Security

**Security Controls:**
- Security groups for SAP components
- Network ACLs
- AWS WAF for web applications
- VPC endpoints for AWS services
- Private connectivity (Direct Connect, VPN)

**📖 [Network Security](https://docs.aws.amazon.com/sap/latest/general/network-security.html)** - Network protection
**📖 [Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)** - Firewall rules
**📖 [AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)** - Web application firewall
**📖 [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)** - Private connections

#### 4.5 Compliance and Governance

**Compliance:**
- SAP-specific compliance requirements
- Data residency and sovereignty
- Audit logging (CloudTrail)
- Compliance certifications
- Shared responsibility model

**📖 [Compliance](https://docs.aws.amazon.com/sap/latest/general/compliance.html)** - Compliance overview
**📖 [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)** - Audit logging
**📖 [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)** - Configuration tracking
**📖 [Shared Responsibility](https://aws.amazon.com/compliance/shared-responsibility-model/)** - Security model

## 🛠️ Key AWS Services for SAP

### Compute
- **EC2**: X1/X2/R5/R6i/R7i instances for SAP
- **Dedicated Hosts**: License compliance
- **Placement Groups**: Low-latency networking

**📖 [EC2 for SAP](https://docs.aws.amazon.com/sap/latest/general/ec2-instances.html)** - Compute options
**📖 [Dedicated Hosts](https://aws.amazon.com/ec2/dedicated-hosts/)** - Licensing support

### Storage
- **EBS**: gp3, io2 for SAP HANA
- **EFS**: Shared file systems
- **FSx for ONTAP**: Enterprise NAS
- **S3**: Backups and archives

**📖 [Storage Options](https://docs.aws.amazon.com/sap/latest/general/storage-config.html)** - Storage architecture

### Networking
- **VPC**: Network isolation
- **Direct Connect**: Hybrid connectivity
- **Transit Gateway**: Multi-VPC networking
- **Route 53**: DNS management

**📖 [Networking for SAP](https://docs.aws.amazon.com/sap/latest/general/networking.html)** - Network design

### Management & Operations
- **AWS Backup**: Centralized backup
- **CloudWatch**: Monitoring and alerting
- **Systems Manager**: Operational tasks
- **AWS Launch Wizard**: Automated deployment

**📖 [Management Tools](https://docs.aws.amazon.com/sap/latest/general/operations.html)** - Operational tools

### Security
- **IAM**: Access control
- **KMS**: Encryption keys
- **CloudTrail**: Audit logging
- **AWS WAF**: Application firewall

**📖 [Security Services](https://docs.aws.amazon.com/sap/latest/general/security.html)** - Security tools

## 📖 Required Reading

### AWS SAP Documentation
**📖 [SAP on AWS General Guide](https://docs.aws.amazon.com/sap/latest/general/what-is-general.html)** - Complete SAP guide
**📖 [SAP HANA on AWS Guide](https://docs.aws.amazon.com/sap/latest/sap-hana/what-is-sap-hana.html)** - HANA-specific guide
**📖 [SAP NetWeaver on AWS Guide](https://docs.aws.amazon.com/sap/latest/sap-netweaver/what-is-netweaver.html)** - NetWeaver guide
**📖 [SAP Architecture Best Practices](https://docs.aws.amazon.com/sap/latest/general/arch-guide.html)** - Architecture whitepaper

### SAP Resources
**📖 [SAP Notes](https://support.sap.com/en/my-support/knowledge-base.html)** - SAP knowledge base
**📖 [SAP on AWS Certification](https://www.sap.com/dmc/exp/2014-09-02-hana-hardware/enEN/#/solutions?filters=v:deCertified;iaas;ve:23)** - SAP certification directory
**📖 [SAP Quick Sizer](https://www.sap.com/about/benchmark/sizing.html)** - System sizing tool

### AWS Whitepapers
**📖 [SAP Workloads on AWS](https://d1.awsstatic.com/whitepapers/sap-on-aws-implementation-and-operations-guide.pdf)** - Implementation guide
**📖 [SAP HANA Best Practices](https://docs.aws.amazon.com/sap/latest/sap-hana/welcome.html)** - Best practices guide

## 💡 Study Strategy

### Recommended Timeline (8-12 weeks, 15-20 hours/week)

**Weeks 1-3: SAP Fundamentals**
- SAP architecture and components
- SAP HANA and NetWeaver basics
- SAP Basis administration concepts
- Study time: 15 hours/week

**Weeks 4-6: AWS Infrastructure for SAP**
- EC2 instance types for SAP
- Storage design (EBS, EFS, FSx)
- Networking (VPC, Direct Connect)
- High availability and DR
- Study time: 18 hours/week

**Weeks 7-9: SAP Deployment and Migration**
- Installation methods
- Migration strategies
- AWS Launch Wizard
- Hands-on deployments
- Study time: 20 hours/week

**Weeks 10-12: Operations and Practice**
- Monitoring and management
- Backup and recovery
- Security and compliance
- Practice exams (aim for 80%+)
- Study time: 15-18 hours/week

### Study Resources

**Official AWS Training:**
**📖 [AWS Training for SAP](https://aws.amazon.com/sap/)** - SAP-specific training
**📖 [SAP on AWS Learning Path](https://aws.amazon.com/sap/)** - Official learning path

**Hands-On Practice:**
- Deploy SAP systems using AWS Launch Wizard
- Set up HANA System Replication
- Configure backups with AWS Backint Agent
- Build HA cluster with Pacemaker
- Practice migration scenarios

**SAP Training:**
- SAP NetWeaver Administration (NW001)
- SAP HANA Administration (HA100)
- SAP Basis Administration courses

## 🎯 Exam Day Tips

### Preparation
- Review SAP-certified EC2 instance types
- Know HANA System Replication configurations
- Understand backup and DR strategies
- Review AWS Launch Wizard capabilities
- Get adequate rest before exam

### During Exam
- Read questions carefully - many are scenario-based
- Pay attention to SAP-specific requirements (HA, performance, sizing)
- Look for keywords: "MOST cost-effective", "LEAST operational overhead"
- Eliminate wrong answers first
- Flag uncertain questions for review
- Manage time: ~2.6 minutes per question

### Common Question Patterns
- Instance type selection for SAP workloads
- Storage configuration for HANA and NetWeaver
- High availability and disaster recovery scenarios
- Migration strategy selection
- Backup and recovery procedures
- Security and compliance requirements
- Cost optimization approaches

### Technical Setup (Online Proctoring)
- Stable internet connection
- Webcam and microphone required
- Clear workspace
- Government-issued photo ID
- Close all applications
- 170 minutes is long - take breaks during review time

**📖 [Exam Prep Resources](https://aws.amazon.com/certification/)** - Official preparation

## 🚀 After Certification

### Career Benefits
- Demonstrates specialized SAP on AWS expertise
- Highly valued in enterprise SAP environments
- Salary premium for SAP+Cloud skills
- Opens SAP migration project opportunities

### Related Certifications
**📖 [AWS Solutions Architect Professional](https://aws.amazon.com/certification/certified-solutions-architect-professional/)** - Advanced architecture
**📖 [AWS Security Specialty](https://aws.amazon.com/certification/certified-security-specialty/)** - Security focus
**📖 [SAP Certifications](https://learning.sap.com/certifications)** - SAP technology certifications

### Continuous Learning
- Follow SAP on AWS blog
- Attend AWS re:Invent SAP sessions
- Join SAP on AWS community
- Stay updated with new instance types
- Practice with latest SAP releases

**📖 [SAP on AWS Blog](https://aws.amazon.com/blogs/awsforsap/)** - Latest updates
**📖 [SAP on AWS YouTube](https://www.youtube.com/c/SAPonAWS)** - Video content

---

## 📊 Quick Reference

### Exam Details at a Glance
- **65 questions** in **170 minutes** = **~2.6 minutes per question**
- **750/1000 to pass** = Approximately **75%**
- **30% SAP design** = ~20 questions
- **30% SAP implementation** = ~20 questions
- **24% SAP operations** = ~16 questions
- **16% SAP security** = ~10 questions

### SAP-Certified EC2 Instance Types

| Instance Family | Use Case | Memory Range |
|-----------------|----------|--------------|
| **X1/X1e** | SAP HANA (legacy) | Up to 3,904 GB |
| **X2idn/X2iedn** | SAP HANA | Up to 2,048 GB |
| **X2iezn** | SAP HANA (high frequency) | Up to 1,536 GB |
| **High Memory (u-*)** | Large SAP HANA | Up to 24 TB |
| **R5/R6i/R7i** | SAP applications | Up to 1,024 GB |

### Key SAP Components

| Component | Purpose | AWS Service |
|-----------|---------|-------------|
| **ASCS/ERS** | Central services | EC2 + Pacemaker |
| **PAS/AAS** | Application servers | EC2 + Auto Scaling |
| **SAP HANA** | Database | EC2 (X2/High Memory) + EBS |
| **Web Dispatcher** | Load balancing | EC2 or ALB |
| **SAP Router** | Network connectivity | EC2 in DMZ |

---

**Good luck with your AWS Certified SAP on AWS - Specialty exam! 🎉**
