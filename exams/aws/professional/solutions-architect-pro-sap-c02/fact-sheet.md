---
last-updated: 2026-10-16
exam-version: SAP-C02
exam-retires: 2026-11-16
---

# AWS Solutions Architect Professional (SAP-C02) - Fact Sheet

> ⚠️ **RETIRING November 16, 2026.** The last day to sit SAP-C02 is November 16, 2026. **SAP-C03** registration opened October 27, 2026 and its outline is published: this guide is **superseded by the [SAP-C03 guide](../solutions-architect-pro-sap-c03/README.md)**, which lists what changed. SAP-C03 is in use from November 17, 2026.

## Quick Reference

**Exam Code:** SAP-C02
**Duration:** 180 minutes (3 hours)
**Questions:** 75 questions
**Passing Score:** 750/1000 (estimated ~70%)
**Cost:** $300 USD
**Validity:** 3 years
**Delivery:** Pearson VUE (Testing center or online proctored)
**Difficulty:** ⭐⭐⭐⭐⭐ (Hardest AWS certification)

## Exam Domain Breakdown

| Domain | Weight | Key Focus |
|--------|--------|-----------|
| Design Solutions for Organizational Complexity | 26% | Multi-account, hybrid, enterprise networking |
| Design for New Solutions | 29% | Modern architectures, microservices, data |
| Continuous Improvement for Existing Solutions | 25% | Optimization, reliability, cost, security |
| Accelerate Workload Migration & Modernization | 20% | 7 Rs, migration tools, modernization patterns |

## Critical Services by Domain

### Domain 1: Organizational Complexity (26%)

**Multi-Account Management:**
- **AWS Organizations** - Central management, consolidated billing
- **[📖 AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/)** - Best practices for multi-account
- **Control Tower** - Landing zone automation, guardrails
- **[📖 Control Tower](https://docs.aws.amazon.com/controltower/latest/userguide/)** - Automated multi-account setup
- **Service Control Policies (SCPs)** - Organizational-level permissions
- **[📖 SCPs Guide](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)** - Permission guardrails
- **Resource Access Manager (RAM)** - Cross-account resource sharing
- **[📖 RAM Documentation](https://docs.aws.amazon.com/ram/latest/userguide/)** - Share Transit Gateway, subnets, etc.
- **IAM Identity Center (AWS SSO)** - Centralized access management
- **[📖 IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/)** - SSO setup

**Enterprise Networking:**
- **Transit Gateway** - Hub-and-spoke, VPC interconnection (supports 5,000 VPCs)
- **[📖 Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/)** - Central hub for VPCs and on-premises
- **Direct Connect** - Dedicated 1Gbps-100Gbps connection, private connectivity
- **[📖 Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/)** - Setup and architecture
- **Direct Connect Gateway** - Connect to multiple VPCs in different regions
- **[📖 DX Gateway](https://docs.aws.amazon.com/directconnect/latest/UserGuide/direct-connect-gateways.html)** - Multi-region connectivity
- **VPN** - IPSec, up to 1.25 Gbps per tunnel (ECMP for multiple tunnels)
- **[📖 Site-to-Site VPN](https://docs.aws.amazon.com/vpn/latest/s2svpn/)** - Encrypted hybrid connectivity
- **Cloud WAN** - Global network management
- **[📖 Cloud WAN](https://docs.aws.amazon.com/network-manager/latest/cloudwan/what-is-cloudwan.html)** - SD-WAN on AWS
- **PrivateLink** - Private connectivity to services without internet
- **[📖 AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/)** - VPC endpoint services

**Hybrid Architectures:**
- **Storage Gateway** - Volume (iSCSI), File (NFS/SMB), Tape (VTL)
- **[📖 Storage Gateway](https://docs.aws.amazon.com/storagegateway/)** - On-premises storage integration
- **DataSync** - Fast data transfer, up to 10 Gbps
- **[📖 DataSync](https://docs.aws.amazon.com/datasync/latest/userguide/)** - Accelerated data migration
- **Route 53 Resolver** - Hybrid DNS resolution
- **[📖 Route 53 Resolver](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver.html)** - Hybrid DNS architecture
- **AWS Outposts** - AWS infrastructure on-premises
- **[📖 AWS Outposts](https://docs.aws.amazon.com/outposts/latest/userguide/)** - Extend AWS on-premises

### Domain 2: Design for New Solutions (29%)

**Microservices & Serverless:**
- **Lambda** - Event-driven compute, 15 min max, 10GB memory max
- **[📖 AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/)** - Serverless functions
- **API Gateway** - REST/HTTP/WebSocket, 29 sec timeout, 10MB payload
- **[📖 API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/)** - Managed API service
- **Step Functions** - Workflow orchestration, Standard (1 year max) vs Express (5 min max)
- **[📖 Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/)** - Serverless workflows
- **EventBridge** - Event bus, 400+ AWS sources, custom applications
- **[📖 EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/)** - Event-driven architecture
- **App Runner** - Container deployment without infrastructure management
- **[📖 App Runner](https://docs.aws.amazon.com/apprunner/latest/dg/)** - Deploy containers easily

**Containers:**
- **ECS** - AWS container orchestration, EC2 or Fargate launch types
- **[📖 Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/)** - Container orchestration
- **EKS** - Managed Kubernetes, supports Fargate, EC2, Outposts
- **[📖 Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/)** - Kubernetes on AWS
- **Fargate** - Serverless containers, no server management
- **[📖 AWS Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)** - Serverless compute for containers
- **ECR** - Container registry, public and private
- **[📖 Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/)** - Docker registry

**Advanced Databases:**
- **Aurora Global Database** - Multi-region, < 1 sec cross-region latency, 5 secondary regions max
- **[📖 Aurora Global Database](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html)** - Multi-region replication
- **DynamoDB Global Tables** - Multi-region active-active, automatic replication
- **[📖 DynamoDB Global Tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html)** - Multi-region DynamoDB
- **Redshift** - Petabyte-scale data warehouse, RA3 nodes with managed storage
- **[📖 Amazon Redshift](https://docs.aws.amazon.com/redshift/latest/dg/)** - Data warehouse
- **DocumentDB** - MongoDB-compatible
- **[📖 Amazon DocumentDB](https://docs.aws.amazon.com/documentdb/latest/developerguide/)** - Document database
- **Neptune** - Graph database
- **[📖 Amazon Neptune](https://docs.aws.amazon.com/neptune/latest/userguide/)** - Graph database
- **Timestream** - Time-series database
- **[📖 Amazon Timestream](https://docs.aws.amazon.com/timestream/latest/developerguide/)** - Time-series data
- **QLDB** - Ledger database, immutable transaction log
- **[📖 Amazon QLDB](https://web.archive.org/web/20250810210701/https://docs.aws.amazon.com/qldb/latest/developerguide/)** - Ledger database

**Data & Analytics:**
- **Kinesis Data Streams** - Real-time, shard-based, 1MB/sec or 1,000 records/sec per shard
- **[📖 Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/)** - Real-time streaming
- **Kinesis Data Firehose** - Load streaming data to destinations, near real-time
- **[📖 Kinesis Firehose](https://docs.aws.amazon.com/firehose/latest/dev/)** - Streaming data delivery
- **Kinesis Data Analytics** - SQL/Flink for stream processing
- **[📖 Kinesis Analytics](https://docs.aws.amazon.com/kinesisanalytics/latest/dev/)** - Stream processing
- **MSK (Managed Kafka)** - Apache Kafka managed service
- **[📖 Amazon MSK](https://docs.aws.amazon.com/msk/latest/developerguide/)** - Managed Kafka
- **Glue** - ETL service, serverless, data catalog
- **[📖 AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/)** - ETL and data catalog
- **EMR** - Big data (Hadoop, Spark), EC2 or EKS
- **[📖 Amazon EMR](https://docs.aws.amazon.com/emr/latest/ManagementGuide/)** - Big data processing
- **Athena** - Serverless SQL queries on S3, pay per query
- **[📖 Amazon Athena](https://docs.aws.amazon.com/athena/latest/ug/)** - Serverless SQL

### Domain 3: Continuous Improvement (25%)

**Performance Optimization:**
- **CloudFront** - Global CDN, edge caching, Lambda@Edge (event-driven), CloudFront Functions (lightweight)
- **[📖 Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/)** - CDN and edge computing
- **Global Accelerator** - Static anycast IPs, multi-region failover, health checks
- **[📖 Global Accelerator](https://docs.aws.amazon.com/global-accelerator/)** - Anycast networking
- **ElastiCache** - Redis (advanced features, backup) or Memcached (simple, multi-threaded)
- **[📖 Amazon ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/)** - In-memory caching
- **DAX** - DynamoDB accelerator, microsecond latency, in-memory cache
- **[📖 DynamoDB DAX](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html)** - DynamoDB cache
- **Graviton Processors** - ARM-based, 40% better price/performance
- **[📖 AWS Graviton](https://aws.amazon.com/ec2/graviton/)** - ARM instances

**Cost Optimization:**
- **Savings Plans** - Compute (EC2, Fargate, Lambda), SageMaker, up to 72% savings
- **[📖 Savings Plans](https://docs.aws.amazon.com/savingsplans/latest/userguide/)** - Flexible pricing
- **Reserved Instances** - 1 or 3 year commitment, Standard (best savings) vs Convertible (flexibility)
- **[📖 Reserved Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html)** - EC2 commitment
- **Spot Instances** - Up to 90% discount, 2-minute termination notice
- **[📖 Spot Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html)** - Interruptible compute
- **S3 Intelligent-Tiering** - Automatic lifecycle management, moves objects between tiers
- **[📖 S3 Intelligent-Tiering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering.html)** - Automatic storage optimization
- **Compute Optimizer** - ML-powered recommendations for EC2, EBS, Lambda, ECS
- **[📖 Compute Optimizer](https://docs.aws.amazon.com/compute-optimizer/latest/ug/)** - Rightsizing recommendations
- **Cost Anomaly Detection** - ML-powered spend anomaly identification
- **[📖 Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html)** - Spend alerts

**Operational Excellence:**
- **CloudFormation** - IaC, StackSets for multi-account/region, drift detection
- **[📖 AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)** - Infrastructure as code
- **CDK** - Infrastructure as code in programming languages
- **[📖 AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/)** - Cloud Development Kit
- **Systems Manager** - Operational hub, Parameter Store, Session Manager, Patch Manager
- **[📖 Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/)** - Operations management
- **OpsWorks** - Chef/Puppet managed configuration, (retired: end of life 26 May 2024; use Systems Manager)
- **[📖 Migrate AWS OpsWorks Stacks to Systems Manager](https://aws.amazon.com/blogs/mt/migrate-your-aws-opsworks-stacks-to-aws-systems-manager/)** - Configuration management
- **Service Catalog** - Governed product catalog
- **[📖 Service Catalog](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/)** - Governance

**Reliability:**
- **Auto Scaling** - Target tracking, step scaling, simple scaling, predictive scaling
- **[📖 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/)** - EC2 Auto Scaling
- **Application Auto Scaling** - DynamoDB, ECS, Lambda, AppStream
- **[📖 Application Auto Scaling](https://docs.aws.amazon.com/autoscaling/application/userguide/)** - Service-level scaling
- **AWS Backup** - Centralized backup across services, 35+ services supported
- **[📖 AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/)** - Centralized backup
- **Elastic Disaster Recovery (DRS)** - Continuous replication for DR, formerly CloudEndure
- **[📖 AWS DRS](https://docs.aws.amazon.com/drs/latest/userguide/)** - Disaster recovery

### Domain 4: Migration & Modernization (20%)

**Migration Strategies (7 Rs):**
1. **Rehost** - Lift-and-shift, fastest, AWS MGN
2. **Replatform** - Lift, tinker, shift, minor optimizations (RDS instead of self-managed DB)
3. **Refactor/Re-architect** - Cloud-native, serverless, microservices
4. **Relocate** - VMware Cloud on AWS, hypervisor-level
5. **Retain** - Keep on-premises (for now)
6. **Retire** - Decommission unneeded systems
7. **Repurchase** - Move to SaaS

**Migration Tools:**
- **Application Migration Service (MGN)** - Rehost, continuous replication, formerly CloudEndure
- **[📖 AWS MGN](https://docs.aws.amazon.com/mgn/latest/ug/)** - Lift-and-shift migrations
- **Database Migration Service (DMS)** - Homogeneous and heterogeneous migrations, CDC
- **[📖 AWS DMS](https://docs.aws.amazon.com/dms/latest/userguide/)** - Database migration
- **Schema Conversion Tool (SCT)** - Convert database schemas
- **[📖 AWS SCT](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/)** - Schema conversion
- **DataSync** - Accelerated data transfer, incremental
- **[📖 AWS DataSync](https://docs.aws.amazon.com/datasync/latest/userguide/)** - Fast data transfer
- **Transfer Family** - SFTP/FTPS/FTP to S3 or EFS
- **[📖 Transfer Family](https://docs.aws.amazon.com/transfer/latest/userguide/)** - Managed file transfer
- **Snow Family** - Physical data transfer:
  - **Snowcone** - 8TB usable (HDD) or 14TB (SSD)
  - **Snowball Edge Storage** - 80TB
  - **Snowball Edge Compute** - 42TB + compute
  - **Snowmobile** - 100PB, exabyte-scale
  - **[📖 AWS Snow Family](https://docs.aws.amazon.com/snowball/)** - Physical data migration
- **Migration Hub** - Track migrations, central dashboard
- **[📖 Migration Hub](https://docs.aws.amazon.com/migrationhub/latest/ug/)** - Migration tracking
- **Application Discovery Service** - Agentless or agent-based discovery
- **[📖 Application Discovery](https://docs.aws.amazon.com/application-discovery/latest/userguide/)** - Discover on-premises apps

## Advanced Networking Concepts

### Transit Gateway Deep Dive

**[📖 Transit Gateway Guide](https://docs.aws.amazon.com/vpc/latest/tgw/)**

**Capabilities:**
- Central hub connecting VPCs and on-premises networks
- Up to 5,000 VPC attachments per TGW
- Inter-region peering
- VPN attachments (supports ECMP)
- Direct Connect Gateway attachments
- Multiple route tables for segmentation
- **[📖 TGW Route Tables](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-route-tables.html)** - Routing configuration

**Routing:**
- Static routes
- Dynamic routes (BGP via VPN or DX)
- Route propagation from attachments
- Blackhole routes for blocking traffic
- **[📖 TGW Routing](https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html)** - How routing works

**Use Cases:**
- Hub-and-spoke architecture
- Network segmentation (prod/dev isolation)
- Centralized egress (shared NAT, firewall)
- Multi-region transit gateway peering
- **[📖 TGW Design Best Practices](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-best-design-practices.html)**

### Direct Connect Deep Dive

**[📖 Direct Connect User Guide](https://docs.aws.amazon.com/directconnect/latest/UserGuide/)**

**Connection Types:**
- **Dedicated** - Physical connection (1, 10, 100 Gbps)
- **Hosted** - Shared connection via partner (50 Mbps - 10 Gbps)
- **[📖 DX Connections](https://docs.aws.amazon.com/directconnect/latest/UserGuide/WorkingWithConnections.html)** - Connection types

**Virtual Interfaces (VIFs):**
- **Private VIF** - Connect to VPC via Virtual Private Gateway
- **Public VIF** - Connect to AWS public services (S3, DynamoDB)
- **Transit VIF** - Connect to Transit Gateway
- **[📖 Virtual Interfaces](https://docs.aws.amazon.com/directconnect/latest/UserGuide/WorkingWithVirtualInterfaces.html)** - VIF configuration

**High Availability:**
- Always use 2+ connections for HA
- Different DX locations
- VPN as backup (hybrid)
- LAG (Link Aggregation Group) for bandwidth scaling
- **[📖 DX Resiliency](https://docs.aws.amazon.com/directconnect/latest/UserGuide/resiliency_toolkit.html)** - HA design

**Direct Connect Gateway:**
- Connect to multiple VPCs in different regions
- Private VIF to DX Gateway to VGWs or TGW
- Max 10 VGWs or 3 TGWs per DX Gateway
- **[📖 DX Gateway Guide](https://docs.aws.amazon.com/directconnect/latest/UserGuide/direct-connect-gateways.html)**

### VPC Peering vs Transit Gateway

| Feature | VPC Peering | Transit Gateway |
|---------|-------------|-----------------|
| **Max VPCs** | 125 per VPC | 5,000 per TGW |
| **Transitive** | No | Yes |
| **Routing** | Mesh (manual) | Hub-and-spoke |
| **Cross-region** | Yes | Yes (peering) |
| **Bandwidth** | No limit | 50 Gbps per AZ |
| **Cost** | Data transfer only | Per attachment + data |
| **Use case** | Few VPCs | Many VPCs, complex routing |

## IAM Advanced Concepts

### Policy Types & Evaluation

**[📖 IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)**

**Policy Types:**
1. **Identity-based** - Attached to users, groups, roles
2. **Resource-based** - Attached to resources (S3, SQS, Lambda, etc.)
3. **Permissions boundaries** - Max permissions for identity policies
4. **Service Control Policies (SCPs)** - Organizational-level guardrails
5. **Session policies** - Passed during AssumeRole
6. **Access Control Lists (ACLs)** - Legacy (S3, VPC)
- **[📖 Policy Types](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types)** - Detailed comparison

**Evaluation Logic:**
1. By default, **explicit DENY**
2. Evaluate all policies (identity, resource, SCPs, boundaries, session)
3. **Explicit DENY** always wins
4. If any **explicit ALLOW** (and no deny), allow
5. Otherwise, implicit deny
- **[📖 Policy Evaluation Logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)** - Complete evaluation flow

### Cross-Account Access Patterns

**Pattern 1: IAM Roles (Preferred)**
```
Account A → AssumeRole → Role in Account B → Access resources
```
- Most secure
- Temporary credentials
- MFA support
- CloudTrail logging

**Pattern 2: Resource-Based Policies**
```
S3 bucket in Account B → Bucket policy allows Account A principal
```
- Direct access
- No AssumeRole needed
- Limited to services supporting resource policies

**Pattern 3: AWS Organizations + RAM**
```
Share resources via RAM → Access in member accounts
```
- Centralized sharing
- Transit Gateway, Subnets, License Manager, etc.

## Database Selection Decision Tree

```
Relational needed?
├─ YES → ACID required?
│  ├─ YES → Multi-region active-active?
│  │  ├─ YES → Aurora Global Database
│  │  └─ NO → Aurora Regional
│  └─ NO → Read-heavy workload?
│     ├─ YES → Aurora with Read Replicas
│     └─ NO → RDS (MySQL, PostgreSQL, SQL Server, etc.)
└─ NO → Data model?
   ├─ Key-Value/Document → DynamoDB
   ├─ Wide-Column → Keyspaces (Cassandra)
   ├─ Graph → Neptune
   ├─ Time-Series → Timestream
   ├─ Ledger/Immutable → QLDB
   └─ Document (MongoDB) → DocumentDB
```

## High Availability Patterns

### Multi-AZ vs Multi-Region

**Multi-AZ (Regional HA):**
- Protects against AZ failures
- Synchronous replication (RDS, Aurora)
- Automatic failover (< 60 seconds RDS, < 30 sec Aurora)
- Same region latency (milliseconds)
- **RTO:** Minutes | **RPO:** Zero (sync replication)

**Multi-Region (Geographic HA + DR):**
- Protects against region failures
- Asynchronous replication
- Manual or automated failover
- Cross-region latency (varies by distance)
- **RTO:** Minutes to hours | **RPO:** Seconds to minutes

### Disaster Recovery Strategies

| Strategy | RTO | RPO | Cost | Complexity |
|----------|-----|-----|------|------------|
| **Backup & Restore** | Hours-Days | Hours | $ | Low |
| **Pilot Light** | 10s of minutes | Minutes | $$ | Medium |
| **Warm Standby** | Minutes | Seconds | $$$ | Medium-High |
| **Active-Active Multi-Region** | Seconds | Near-Zero | $$$$ | High |

**Backup & Restore:**
- Periodic backups to S3
- Restore when needed
- Cheapest, longest RTO/RPO

**Pilot Light:**
- Core systems running minimal resources
- Scale up during disaster
- Data replication active (DRS, DMS, S3 CRR)

**Warm Standby:**
- Scaled-down fully functional environment
- Scale up during disaster
- Continuous data replication

**Active-Active:**
- Full production in multiple regions
- Users served from nearest region
- Instant failover (Route 53, Global Accelerator)
- Highest cost, best RTO/RPO

## Caching Strategies

### Multi-Layer Caching

```
User Request
  ↓
CloudFront (Edge Cache - seconds to minutes)
  ↓
API Gateway (Endpoint Cache - seconds to hours)
  ↓
Application (ElastiCache/DAX - milliseconds to seconds)
  ↓
Database (Query Cache - milliseconds)
```

### When to Use Each

**CloudFront:**
- Static content (images, CSS, JS)
- Dynamic content at edge
- Lambda@Edge for personalization
- TTL: seconds to days

**API Gateway Caching:**
- API responses
- Reduce backend calls
- TTL: 0 to 3600 seconds
- Per-stage configuration

**ElastiCache (Redis):**
- Session management
- Complex data structures (sorted sets, lists)
- Pub/sub messaging
- Persistence option
- Backup/restore

**ElastiCache (Memcached):**
- Simple key-value
- Multi-threaded
- Horizontal scaling
- No persistence

**DAX (DynamoDB Accelerator):**
- DynamoDB-specific
- Microsecond latency
- Write-through cache
- Eventually consistent reads only

## Event-Driven Architecture Patterns

### EventBridge Patterns

**Use EventBridge for:**
- Decoupled event routing
- Schema registry and discovery
- Multiple targets per rule (5 targets max)
- SaaS integration (40+ partners)
- Cross-account event delivery
- Archive and replay events

**EventBridge vs SNS vs SQS:**

| Feature | EventBridge | SNS | SQS |
|---------|-------------|-----|-----|
| **Pattern** | Event bus | Pub/sub | Queue |
| **Filtering** | Advanced (JSON patterns) | Basic (attributes) | None (consumer-side) |
| **Targets** | 100+ AWS services | Limited protocols | Pull-based consumers |
| **SaaS** | 40+ integrations | None | None |
| **Schema** | Schema registry | No | No |
| **Replay** | Archive & replay | No | Dead-letter queue |
| **Use case** | Complex event routing | Fan-out notifications | Decoupling, buffering |

### Step Functions Workflow Types

**Standard Workflows:**
- Duration: Up to 1 year
- Execution rate: 2,000/second
- Pricing: Per state transition
- Exactly-once execution
- Use for: Long-running, human approvals, audit

**Express Workflows:**
- Duration: Up to 5 minutes
- Execution rate: 100,000/second
- Pricing: Per execution duration
- At-least-once execution
- Use for: High-volume event processing, IoT, streaming

**Saga Pattern with Step Functions:**
```
Try Operation 1 → Success → Try Operation 2 → Success → Complete
     ↓                            ↓
   Fail                         Fail
     ↓                            ↓
Compensate 1                 Compensate 2 → Compensate 1
```

## Security Services Matrix

| Service | Purpose | Key Features |
|---------|---------|--------------|
| **GuardDuty** | Threat detection | ML-powered, VPC Flow, CloudTrail, DNS logs |
| **Security Hub** | Security posture management | Aggregates findings, compliance checks |
| **Detective** | Security investigation | Graph analysis, root cause |
| **Macie** | Data discovery & protection | PII/PHI detection in S3 |
| **Inspector** | Vulnerability assessment | EC2, ECR, Lambda scanning |
| **Config** | Resource compliance | Track changes, compliance rules |
| **CloudTrail** | API auditing | Who did what, when |
| **IAM Access Analyzer** | Permission analysis | External access, unused permissions |
| **Firewall Manager** | Centralized firewall management | WAF, Shield, Security Groups, Network Firewall |
| **Network Firewall** | Stateful firewall | IPS/IDS, deep packet inspection |
| **WAF** | Web application firewall | Layer 7, rate limiting, geo-blocking |
| **Shield Standard** | DDoS protection | Free, automatic |
| **Shield Advanced** | Enhanced DDoS protection | $3,000/month, 24/7 DRT, cost protection |

## Cost Optimization Strategies

### Compute Savings

**EC2 Savings:**
- **On-Demand:** No commitment, highest cost, $$$$$
- **Reserved (1 yr):** 30-40% savings, $$$$
- **Reserved (3 yr):** 50-60% savings, $$$
- **Savings Plans:** Up to 72% savings, flexible, $$$
- **Spot:** Up to 90% savings, interruptible, $

**Savings Plans Types:**
- **Compute:** EC2, Fargate, Lambda (most flexible)
- **EC2 Instance:** Specific instance family in region
- **SageMaker:** SageMaker workloads

**When to Use:**
- Steady-state workloads → Savings Plans or Reserved
- Predictable but varied → Compute Savings Plans
- Fault-tolerant batch → Spot Instances
- Unpredictable → On-Demand

### Storage Savings

**S3 Storage Classes:**
- **Standard:** $0.023/GB, frequent access
- **Intelligent-Tiering:** Automatic, $0.0025 monitoring fee
- **Standard-IA:** $0.0125/GB, retrieval fee, 30-day minimum
- **One Zone-IA:** $0.01/GB, single AZ, retrieval fee
- **Glacier Instant:** $0.004/GB, millisecond retrieval
- **Glacier Flexible:** $0.0036/GB, 1-5 min or 3-5 hr retrieval
- **Glacier Deep Archive:** $0.00099/GB, 12-48 hr retrieval

**EBS Optimization:**
- **gp3:** General purpose, cheaper than gp2, adjustable IOPS/throughput
- **gp2:** General purpose, legacy, 3 IOPS/GB
- **io2 Block Express:** 256,000 IOPS, 99.999% durability
- **Snapshots:** Incremental, S3-backed, compressed
- **Lifecycle Manager:** Automate snapshot creation/deletion

### Database Savings

**Aurora:**
- Aurora Serverless v2 for variable workloads (scales 0.5 to 128 ACUs)
- Reserved Instances (1 or 3 year)
- Stop/start for dev/test (billing pauses)

**DynamoDB:**
- On-Demand for unpredictable workloads
- Provisioned for steady workloads (cheaper)
- Reserved Capacity (1 or 3 year, 50-75% savings)
- Standard-IA table class for infrequent access

## Migration Large Datasets

### Data Transfer Decision Matrix

| Data Size | Timeline | Internet? | Solution |
|-----------|----------|-----------|----------|
| < 10 TB | Days | Yes, good | Direct upload, DataSync |
| < 10 TB | Days | No/poor | Snowcone (8-14 TB) |
| 10-80 TB | Week | Yes | DataSync over DX |
| 10-80 TB | Week | No | Snowball Edge Storage (80 TB) |
| 80 TB - 1 PB | Weeks | No | Multiple Snowballs |
| > 1 PB | Months | No | Snowmobile (100 PB) |

**Direct Connect + DataSync:**
- Best for ongoing sync
- 1 Gbps DX = 10 TB/day
- 10 Gbps DX = 100 TB/day
- Incremental transfers efficient

**Snowball Edge:**
- Physical device shipped to you
- 80 TB usable (Storage Optimized)
- 42 TB usable + compute (Compute Optimized)
- NFS/S3 interface
- Ships back to AWS
- Import to S3

**Snowmobile:**
- 45-foot shipping container
- 100 PB capacity
- GPS tracked, 24/7 security
- Exabyte-scale migrations
- Trucked to your datacenter

## Common Exam Scenarios & Answers

### Scenario 1: Multi-Account Architecture
**Q:** Company has 100+ AWS accounts. Need centralized networking and security controls.
**A:**
- AWS Organizations with OUs
- Transit Gateway for hub-and-spoke networking
- SCPs for guardrails
- AWS Firewall Manager for security policies
- Centralized logging to dedicated security account

### Scenario 2: Hybrid Connectivity
**Q:** On-premises datacenter needs redundant, high-bandwidth connection to multiple VPCs in multiple regions.
**A:**
- 2 Direct Connect connections (different locations)
- Direct Connect Gateway
- Connect to Transit Gateways in each region
- VPN as backup over internet (hybrid)

### Scenario 3: Multi-Region Active-Active
**Q:** Global application needs active-active deployment with automatic failover.
**A:**
- Aurora Global Database or DynamoDB Global Tables
- S3 Cross-Region Replication
- Route 53 geolocation routing with health checks
- CloudFront for global content delivery
- Global Accelerator for static anycast IPs

### Scenario 4: Cost Optimization at Scale
**Q:** Reduce costs for 1,000+ EC2 instances with varied usage patterns.
**A:**
- Compute Savings Plans for flexible savings
- Spot Instances for fault-tolerant workloads
- Auto Scaling to match demand
- Compute Optimizer for rightsizing
- S3 Intelligent-Tiering for storage
- Cost Anomaly Detection for alerts

### Scenario 5: Large-Scale Migration
**Q:** Migrate 500 TB database with < 1 hour downtime.
**A:**
- DMS for continuous replication (CDC)
- Initial full load via Snowball Edge
- Incremental changes via DMS
- Cut over during maintenance window
- Validation and rollback plan

## Key Numbers to Memorize

**Service Limits:**
- Lambda: 15 min timeout, 10 GB memory, 250 MB deployment (unzipped)
- API Gateway: 29 sec timeout, 10 MB payload
- Step Functions Standard: 1 year max duration
- Step Functions Express: 5 min max duration
- Direct Connect: 1, 10, 100 Gbps dedicated
- Transit Gateway: 5,000 VPC attachments, 50 Gbps per AZ
- VPC Peering: 125 per VPC
- Aurora Global: < 1 sec cross-region latency, 5 secondary regions max
- DynamoDB: 400 KB item size, 25 items per batch

**Timing:**
- RDS Multi-AZ failover: < 60 seconds
- Aurora Multi-AZ failover: < 30 seconds
- S3 eventual consistency: < 1 second (now strong consistency for all ops)
- CloudFront edge locations: 450+
- Regions: 32+, AZs: 100+

## Exam Strategy

### Time Management
- 180 minutes ÷ 75 questions = 2.4 minutes per question
- Scenarios are LONG (1-2 paragraphs)
- First pass: Answer known questions (90 minutes)
- Second pass: Tackle flagged questions (70 minutes)
- Final pass: Review all answers (20 minutes)

### Question Analysis
1. **Read the entire scenario** - Don't skim
2. **Identify the actual question** - Often at the end
3. **Note constraints** - Cost, time, complexity, region, compliance
4. **Eliminate obviously wrong** - Usually 2 options are clearly wrong
5. **Compare remaining options** - Trade-offs between final 2
6. **Choose the BEST** - Not just correct, but most appropriate

### Keywords to Watch
- **"Most cost-effective"** → Savings Plans, Spot, S3 tiers, Savings Plans
- **"Least operational overhead"** → Managed services, serverless, automation
- **"High availability"** → Multi-AZ, Multi-Region, Auto Scaling
- **"Disaster recovery"** → Backup strategy, multi-region, automated failover
- **"Security"** → Least privilege, encryption, isolation, audit logging
- **"Performance"** → Caching, CDN, Global Accelerator, optimized services
- **"Large-scale"** → Organizations, Transit Gateway, automation
- **"Hybrid"** → Direct Connect, Storage Gateway, Route 53 Resolver

### Common Traps
- ❌ Choosing theoretical "best" over practical "most appropriate"
- ❌ Over-engineering simple requirements
- ❌ Ignoring constraints (budget, time, skills)
- ❌ Mixing up service capabilities (timeouts, limits)
- ❌ Not considering operational overhead
- ❌ Forgetting about existing AWS footprint

## Final Exam Checklist

### Knowledge
- [ ] Can design multi-account architectures with Organizations
- [ ] Understand Transit Gateway routing scenarios
- [ ] Know Direct Connect architectures with HA
- [ ] Comfortable with Aurora Global and DynamoDB Global Tables
- [ ] Understand all 7 migration Rs and when to use each
- [ ] Know Step Functions workflow patterns
- [ ] Can design multi-region active-active architectures
- [ ] Understand security services and their purposes
- [ ] Know cost optimization strategies for all service types
- [ ] Familiar with disaster recovery strategies and RTO/RPO trade-offs

### Experience
- [ ] 2+ years hands-on AWS experience
- [ ] Architected multi-account solutions
- [ ] Designed hybrid connectivity
- [ ] Implemented disaster recovery
- [ ] Led cloud migrations
- [ ] Optimized costs at scale

### Preparation
- [ ] Completed SAA-C03 (or equivalent)
- [ ] Read AWS Well-Architected Framework (all 6 pillars)
- [ ] Reviewed 5+ AWS whitepapers
- [ ] Scored 80%+ on multiple practice exams
- [ ] Hands-on with key services (TGW, Aurora Global, Organizations, Step Functions)
- [ ] Comfortable with 180-minute exam duration

---

**Pro Tip:** SAP-C02 tests your ability to make architectural trade-offs. There are often multiple "correct" answers - you need to choose the "most appropriate" considering all constraints (cost, time, complexity, operational overhead). Always justify your choice with specific trade-offs!

**Good luck!** This is the hardest AWS certification, but passing it demonstrates expert-level cloud architecture skills. 🚀
