# Oracle Cloud Infrastructure Architect Associate (1Z0-1072-24)

The OCI Architect Associate certification validates skills in designing and implementing solutions on Oracle Cloud Infrastructure. This certification demonstrates proficiency in architecting scalable, secure, and highly available solutions using OCI services.

## 📋 Quick Links

- [**Fact Sheet**](fact-sheet.md) - Exam logistics and objectives
- [**Practice Plan**](practice-plan.md) - Structured study schedule

## 📚 Study Materials

### Core Notes
- [Architecture Design And Networking](notes/01-architecture-design-and-networking.md)
- [Compute And Storage Solutions](notes/02-compute-and-storage-solutions.md)
- [Database Security Operations](notes/03-database-security-operations.md)
## 🎯 Exam Details

- **Exam Code**: 1Z0-1072-24 (this guide's version). The current exam is **1Z0-1072-26** ([Oracle MyLearn learning path](https://mylearn.oracle.com/ou/learning-path/become-an-oci-architect-associate-2026/162234), read 2026-11-22); question count and passing score for -26 need an Oracle sign-in and were not read
- **Duration**: 90 minutes for 1Z0-1072-26 (MyLearn); the 105 minutes listed here before was for -24 and is unsourced
- **Number of Questions**: 60 questions
- **Passing Score**: 68%
- **Question Types**: Multiple choice, multiple select
- **Cost**: $150 USD
- **Validity**: Recertification required every 2 years
- **Language**: Available in multiple languages
- **Delivery**: Pearson VUE (online proctored or test center)

## 📖 Exam Domains

### 1. Design for Hybrid Cloud Architecture (15%)
- **Hybrid Connectivity**
  - FastConnect: Dedicated private connections (1 Gbps, 10 Gbps)
  - Site-to-Site VPN: IPSec VPN to on-premises
  - FastConnect with VPN backup for redundancy
  - Dynamic Routing Gateway (DRG) for hybrid routing

- **On-Premises Integration**
  - Oracle Cloud VMware Solution
  - Database migration strategies
  - Hybrid networking patterns
  - DNS integration (on-prem + OCI)

- **Multi-Cloud and Migration**
  - OCI integration with Azure, AWS
  - Lift-and-shift vs re-architecture
  - Cloud migration assessment

### 2. Design for Compute and Storage (20%)
- **Compute Design**
  - Shape selection (VM.Standard, VM.DenseIO, BM, GPU)
  - Dedicated VM hosts for licensing requirements
  - Instance pools and autoscaling configuration
  - Placement groups for low latency
  - Capacity reservations

- **Container and Serverless Architecture**
  - OKE cluster design (managed nodes, virtual nodes)
  - OKE networking modes (VCN-native, flannel)
  - Container Registry (OCIR) for image management
  - Functions for event-driven serverless
  - API Gateway integration

- **Storage Architecture**
  - Block Volume: Performance tiers (Basic, Balanced, High Performance, Ultra High)
  - Object Storage: Standard, Infrequent Access, Archive tiers
  - File Storage: NFS for shared storage
  - Backup strategies and retention policies
  - Cross-region replication for objects

### 3. Design for Networking (25%)
- **VCN Design**
  - CIDR planning and subnet design
  - Public vs private subnets
  - Hub-and-spoke topology with DRG
  - VCN peering (local and remote)
  - DNS architecture (public, private zones)

- **Gateways and Routing**
  - Internet Gateway for public internet access
  - NAT Gateway for outbound-only traffic
  - Service Gateway for Oracle services (no internet)
  - DRG for hybrid and VCN-to-VCN routing
  - Route table design and routing policies

- **Security Design**
  - Security Lists (stateful, subnet-level)
  - Network Security Groups (stateful, resource-level)
  - Defense in depth approach
  - Microsegmentation with NSGs
  - Private endpoints for PaaS services

- **Load Balancing and Traffic Management**
  - Load Balancer types (flexible, network)
  - Backend set design and health checks
  - SSL/TLS termination
  - Traffic Management Steering policies
  - DNS failover and geo-steering

### 4. Design for Database Solutions (20%)
- **Autonomous Database Architecture**
  - Serverless vs Dedicated Infrastructure
  - Transaction Processing (ATP) vs Data Warehouse (ADW)
  - Autonomous JSON Database
  - Auto-scaling and performance tuning
  - Autonomous Data Guard for DR

- **DB Systems Design**
  - VM DB vs Bare Metal vs Exadata
  - RAC (Real Application Clusters) for HA
  - Data Guard for disaster recovery
  - Backup configuration and retention
  - Patching and upgrade strategies

- **Other Database Services**
  - MySQL Database Service with HeatWave
  - NoSQL Database Cloud Service
  - Redis-compatible caching
  - Database migration strategies (Zero Downtime Migration)

- **Data Management**
  - Backup strategies across database types
  - Point-in-time recovery
  - Cross-region database replication
  - Data masking and privacy

### 5. Design for Security and Compliance (15%)
- **Identity and Access Management**
  - Compartment strategy for isolation
  - IAM policy design and least privilege
  - Federation with external IdPs (SAML, OAuth)
  - Dynamic groups for resource-based policies
  - MFA enforcement

- **Data Security**
  - Encryption at rest (Oracle-managed vs customer-managed keys)
  - Encryption in transit (TLS/SSL)
  - Vault for key and secrets management
  - Rotate encryption keys
  - Hardware Security Module (HSM)

- **Threat Detection and Response**
  - Cloud Guard for posture management
  - Security Zones for maximum security compartments
  - Vulnerability Scanning Service
  - Web Application Firewall (WAF) policies
  - Bastion service for secure access

- **Compliance and Governance**
  - Regulatory compliance frameworks
  - Audit logging and retention
  - Security best practices
  - Data residency requirements

### 6. Design for Resiliency and High Availability (15%)
- **High Availability Design**
  - Multi-AD deployment strategies
  - Fault domain distribution
  - Load balancer health checks
  - Database HA with RAC and Data Guard
  - Stateful vs stateless application design

- **Disaster Recovery**
  - RTO and RPO requirements
  - Pilot Light vs Warm Standby vs Active-Active
  - Cross-region replication strategies
  - Object Storage cross-region copy
  - Database DR with Data Guard and Autonomous Data Guard

- **Backup and Recovery**
  - Block volume backups (manual and scheduled)
  - Boot volume backups
  - Object Storage versioning
  - Database backup strategies (RMAN, automatic)
  - File Storage snapshots

- **Resilience Patterns**
  - Circuit breaker patterns
  - Retry logic and exponential backoff
  - Graceful degradation
  - Chaos engineering principles

### 7. Design for Monitoring and Observability (10%)
- **Monitoring Architecture**
  - Service metrics and custom metrics
  - Alarms and notification design
  - Dashboards for operational visibility
  - Log Analytics for centralized logging

- **Logging Strategy**
  - Enable logging for audit, service, custom logs
  - Log retention and lifecycle
  - Integration with SIEM tools
  - Compliance logging requirements

- **Application Performance**
  - Application Performance Monitoring (APM)
  - Distributed tracing
  - Service Connector Hub for log aggregation
  - Integration with third-party tools

## 🎓 Prerequisites & Recommended Experience

### Prerequisites
- **OCI Foundations (1Z0-1085-24)** - Strongly recommended but not required
- Understanding of cloud computing concepts
- Basic networking knowledge (TCP/IP, routing, VPN)

### Recommended Experience
- 1-2 years working with OCI
- Experience designing cloud architectures
- Familiarity with infrastructure as code
- Understanding of security and compliance requirements

### Technical Skills
- Design multi-tier application architectures
- Implement hybrid cloud connectivity
- Configure VCN networking and security
- Deploy and manage OCI compute and storage
- Understand database selection criteria
- Apply security best practices

## 🌟 Key Architecture Patterns

### Multi-Tier Application
- Web tier: Load balancer + compute instances in public subnet
- App tier: Compute instances in private subnet
- Database tier: Managed database in private subnet
- Bastion host for administrative access

### Hub-and-Spoke Network
- Hub VCN: Central routing with DRG
- Spoke VCNs: Application workloads
- On-premises: Connected via FastConnect or VPN
- Transit routing through DRG

### High Availability Pattern
- Deploy across multiple ADs (minimum 2)
- Distribute across fault domains within each AD
- Use regional services (Object Storage, IAM)
- Implement health checks and autoscaling

### Disaster Recovery Pattern
- Primary region: Active workloads
- Secondary region: Standby resources
- Cross-region replication: Object Storage, databases
- DNS failover for automatic recovery

## Study Strategy

### Recommended Timeline: 8-10 Weeks

**Weeks 1-2: Foundation Review and Compute Architecture**
- Review OCI Foundations concepts
- Deep dive into compute shapes and use cases
- Instance pools and autoscaling
- Container orchestration with OKE
- Hands-on: Deploy multi-tier application

**Weeks 3-4: Networking Architecture**
- VCN design patterns
- Hybrid connectivity (FastConnect, VPN, DRG)
- Security Lists vs NSGs
- Load balancer configuration
- Hands-on: Build hub-and-spoke network

**Weeks 5-6: Storage and Database Architecture**
- Storage tier selection
- Database service selection (Autonomous vs DB Systems)
- Backup and DR strategies
- Data management and migration
- Hands-on: Configure Autonomous DB with Data Guard

**Weeks 7-8: Security and High Availability**
- IAM policy design
- Encryption and key management
- Multi-AD and fault domain design
- DR planning and RTO/RPO
- Hands-on: Implement security best practices

**Weeks 9-10: Practice and Review**
- Architecture scenarios and case studies
- Practice exams (multiple attempts)
- Review weak areas
- Final hands-on labs

### Essential Hands-on Labs
- Design and implement a hub-and-spoke network topology
- Deploy a highly available web application across multiple ADs
- Configure FastConnect or Site-to-Site VPN
- Set up Autonomous Database with Autonomous Data Guard
- Implement comprehensive IAM policies with compartments
- Configure monitoring, alarms, and logging
- Build a disaster recovery solution with cross-region replication
- Deploy containerized application on OKE

## 📚 Study Resources

### Official Oracle Resources
- **[OCI Architect Associate Learning Path](https://mylearn.oracle.com/ou/learning-path/become-an-oci-architect-associate-2024/136197)** - Official training (FREE)
- **[OCI Architecture Center](https://docs.oracle.com/solutions/)** - Reference architectures
- **[OCI Documentation](https://docs.oracle.com/en-us/iaas/Content/home.htm)** - Service documentation
- **[Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)** - Hands-on practice environment
- **[OCI Architecture Framework](https://docs.oracle.com/en/solutions/oci-best-practices/)** - Design principles

### Recommended Study Materials
1. **Oracle University**: Official OCI Architect Associate course
2. **Practice Tests**: Oracle official practice exam + third-party tests
3. **Architecture Whitepapers**: OCI reference architectures
4. **Hands-on Practice**: Required - use Free Tier extensively

### Community Resources
- OCI Architecture Framework documentation
- Oracle blogs and technical articles
- OCI YouTube channel tutorials
- Oracle Cloud Infrastructure subreddit

## Exam Tips

### Question Strategy
- Scenario-based questions require understanding of trade-offs
- Consider cost, performance, security, and high availability
- Identify requirements vs nice-to-have features
- Look for keywords: "most cost-effective", "highest security", "best performance"
- Multiple correct answers - choose the BEST option

### Common Question Themes
- VCN design and routing decisions
- Compute shape selection for workload requirements
- Storage tier selection based on access patterns
- Database choice (Autonomous vs DB Systems, ATP vs ADW)
- HA design using ADs and fault domains
- IAM policy syntax and compartment design
- Hybrid connectivity options (FastConnect vs VPN)
- Load balancer configuration
- DR strategies and RTO/RPO requirements

### OCI Architecture Best Practices
- **Use availability domains**: Deploy across multiple ADs for HA
- **Leverage fault domains**: Anti-affinity within AD
- **Design compartments**: Logical isolation for projects/environments
- **Implement least privilege**: Fine-grained IAM policies
- **Enable encryption**: At rest and in transit
- **Plan for DR**: Cross-region replication and backups
- **Monitor everything**: Metrics, logs, and alarms
- **Automate**: Use Terraform/Resource Manager

### Time Management
- 105 minutes for 60 questions = 1.75 minutes per question
- Read scenario questions carefully (may be longer)
- Flag uncertain questions for review
- Don't get stuck on difficult questions
- Leave 15-20 minutes for final review

## 📈 Success Criteria

- Design scalable and resilient OCI architectures
- Implement secure networking with VCNs, security lists, and NSGs
- Select appropriate compute, storage, and database services
- Design high availability solutions using ADs and fault domains
- Implement hybrid cloud connectivity with FastConnect/VPN
- Apply security best practices including IAM and encryption
- Design disaster recovery solutions meeting RTO/RPO requirements
- Monitor and troubleshoot OCI infrastructure

## Career Path and Next Steps

### After OCI Architect Associate
1. **OCI Architect Professional** (1Z0-997-24) - Advanced architecture certification
2. **OCI Developer Associate** - Application development on OCI
3. **Specialty Certifications** - Security, Database, Data Management

### Related OCI Certifications
- **OCI Operations Associate** - For operations and management focus
- **OCI Security Professional** - Deep dive into OCI security
- **OCI Multicloud Architect** - Multi-cloud architecture patterns

---

**Build robust, scalable, and secure architectures on OCI!** 🏗️
