---
last-updated: 2026-11-25
---

# Google Cloud Professional Cloud Architect - Fact Sheet

## Quick Reference

**Exam Code:** Professional Cloud Architect
**Duration:** 120 minutes (2 hours)
**Questions:** 50-60 questions
**Passing Score:** ~70% (not officially published)
**Cost:** $200 USD
**Validity:** 2 years
**Difficulty:** ⭐⭐⭐⭐⭐ (Most challenging GCP certification)
**Prerequisites:** Recommended 3+ years of industry experience, including 1+ year designing GCP solutions

## Exam Domains

| Section | Weight | Key Focus |
|--------|--------|-----------|
| Designing and planning a cloud solution architecture | ~25% | Business and technical requirements, network/storage/compute and AI design, migration plan |
| Managing and provisioning solution infrastructure | ~17.5% | Hybrid networking, storage, compute, Agent Platform ML workflows, prebuilt APIs |
| Designing for security and compliance | ~17.5% | IAM, hierarchy, CMEK, VPC-SC, remote access, supply chain, securing AI, compliance |
| Analyzing and optimizing technical and business processes | ~15% | SDLC, CI/CD, RCA, DR, stakeholders, change, CapEx/OpEx |
| Managing implementation | ~12.5% | Advising teams, Apigee, programmatic access, emulators, IaC |
| Ensuring solution and operations excellence | ~12.5% | Observability, release management, reliability testing |

Case studies in the current guide: Altostrat Media, Cymbal Retail, EHR Healthcare, KnightMotives Automotive. See [notes/case-studies.md](notes/case-studies.md).

## Core Architecture Principles

### Well-Architected Framework

**[📖 Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)** - Complete architecture framework

**Five Pillars:**
1. **Operational Excellence** - Efficient operations and monitoring
2. **Security, Privacy, and Compliance** - Protection and governance
3. **Reliability** - Availability and fault tolerance
4. **Cost Optimization** - Resource efficiency and financial governance
5. **Performance Optimization** - Efficient resource use and scaling

**Key Resources:**
- **[📖 Architecture Center](https://cloud.google.com/architecture)** - Reference architectures and diagrams
- **[📖 Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)** - Enterprise design patterns
- **[📖 Cloud Architecture Patterns](https://cloud.google.com/architecture/framework/system-design)** - System design patterns
- **[📖 Decision Trees](https://docs.cloud.google.com/architecture/framework)** - Architecture decision guides

## Compute Services - Architecture Deep Dive

### Compute Engine

**Strategic Use Cases:**
- Legacy application migrations (lift-and-shift)
- Custom operating systems or kernels
- GPU/TPU workloads requiring specific configurations
- Per-second billing with sustained use discounts
- **[📖 Compute Engine Overview](https://cloud.google.com/compute/docs/overview)** - Architecture guide
- **[📖 Machine Families](https://cloud.google.com/compute/docs/machine-resource)** - Choosing the right machine type
- **[📖 Instance Templates](https://cloud.google.com/compute/docs/instance-templates)** - Configuration management
- **[📖 Managed Instance Groups](https://cloud.google.com/compute/docs/instance-groups)** - Auto-scaling and load balancing
- **[📖 Sole-Tenant Nodes](https://cloud.google.com/compute/docs/nodes)** - Dedicated hardware for compliance

**Advanced Features:**
- **Custom Machine Types** - Precise resource allocation
- **Preemptible VMs** - Up to 80% cost savings for fault-tolerant workloads
- **Spot VMs** - More flexible than preemptible with longer runtime
- **Committed Use Discounts** - 1 or 3 year commitments for 57% savings
- **Shielded VMs** - Secure boot, vTPM, integrity monitoring
- **[📖 Live Migration](https://cloud.google.com/compute/docs/instances/live-migration)** - Zero-downtime maintenance
- **[📖 Persistent Disk Performance](https://cloud.google.com/compute/docs/disks/performance)** - Storage optimization

### Google Kubernetes Engine (GKE)

**Enterprise Architecture:**
- **Autopilot** - Fully managed, pay-per-pod, optimal configurations
- **Standard** - Node-level control, custom configurations
- **GKE Enterprise** (former tier) - Multi-cluster fleet management, formerly Anthos. Since 2025-09-02 GKE is one offering with no editions: the Enterprise features are in standard GKE or sold as standalone SKUs ([release note](https://docs.cloud.google.com/kubernetes-engine/docs/release-notes))
- **[📖 GKE Architecture](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview)** - Complete overview
- **[📖 Cluster Architecture](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-architecture)** - Control plane and nodes
- **[📖 Multi-Cluster Ingress](https://cloud.google.com/kubernetes-engine/docs/concepts/multi-cluster-ingress)** - Global load balancing
- **[📖 Binary Authorization](https://cloud.google.com/binary-authorization/docs)** - Deploy-time security controls
- **[📖 GKE Networking](https://cloud.google.com/kubernetes-engine/docs/concepts/network-overview)** - VPC-native clusters

**Advanced Patterns:**
- **Workload Identity** - Pod-to-GCP service authentication without keys
- **Config Connector** - Manage GCP resources via Kubernetes
- **Node Auto-Provisioning** - Automatic node pool creation
- **Vertical Pod Autoscaling** - Right-size container resources
- **Multi-cluster Services** - Service discovery across clusters
- **[📖 GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)** - Production guidelines
- **[📖 Security Hardening](https://cloud.google.com/kubernetes-engine/docs/how-to/hardening-your-cluster)** - Security best practices

### Cloud Run

**Serverless Container Architecture:**
- Fully managed compute platform for containers
- Scales to zero, pay only for actual usage
- Auto-scales based on concurrent requests
- **[📖 Cloud Run Documentation](https://cloud.google.com/run/docs)** - Complete guide
- **[📖 Service Identity](https://cloud.google.com/run/docs/securing/service-identity)** - IAM integration
- **[📖 VPC Connectivity](https://cloud.google.com/run/docs/configuring/vpc-direct-vpc)** - Direct VPC egress
- **[📖 Cloud Run Jobs](https://cloud.google.com/run/docs/create-jobs)** - Batch workloads

**Architecture Decisions:**
- **vs App Engine** - More flexibility, custom containers
- **vs GKE** - Simpler operations, less control
- **vs Cloud Functions** - Longer execution time, more memory

### App Engine

**Platform as a Service:**
- **Standard Environment** - Rapid scaling, sandbox runtime, free tier
- **Flexible Environment** - Docker containers, SSH access, custom runtimes
- **[📖 App Engine Architecture](https://cloud.google.com/appengine/docs/the-appengine-environments)** - Environment comparison
- **[📖 Scaling Types](https://docs.cloud.google.com/appengine/docs/standard/how-instances-are-managed)** - Automatic, basic, manual scaling
- **[📖 Traffic Splitting](https://cloud.google.com/appengine/docs/standard/splitting-traffic)** - A/B testing and canary
- **[📖 Migration to Standard 2nd Gen](https://cloud.google.com/appengine/docs/standard/runtimes)** - Modern runtimes

### Cloud Functions

**Event-Driven Serverless:**
- **2nd Generation** - Built on Cloud Run, better performance, longer execution
- Event sources: Cloud Storage, Pub/Sub, HTTP, Firestore, Firebase
- **[📖 Cloud Functions Architecture](https://cloud.google.com/functions/docs/concepts/overview)** - Concepts and patterns
- **[📖 Eventarc Integration](https://cloud.google.com/eventarc/docs)** - Unified eventing
- **[📖 Security Best Practices](https://cloud.google.com/functions/docs/securing)** - Function security

## Storage Architecture

### Cloud Storage

**Global Object Storage:**
- **Storage Classes Decision Matrix:**
  - **Standard** - Hot data, frequent access
  - **Nearline** - < 1/month access, 30-day minimum
  - **Coldline** - < 1/quarter access, 90-day minimum
  - **Archive** - < 1/year access, 365-day minimum
- **[📖 Storage Classes](https://cloud.google.com/storage/docs/storage-classes)** - Detailed comparison
- **[📖 Object Lifecycle Management](https://cloud.google.com/storage/docs/lifecycle)** - Automated tiering
- **[📖 Bucket Locations](https://cloud.google.com/storage/docs/locations)** - Regional, dual-region, multi-region
- **[📖 Object Versioning](https://cloud.google.com/storage/docs/object-versioning)** - Version control
- **[📖 Retention Policies](https://cloud.google.com/storage/docs/bucket-lock)** - Compliance and data governance
- **[📖 Customer-Managed Encryption Keys](https://cloud.google.com/storage/docs/encryption/customer-managed-keys)** - CMEK integration

**Advanced Features:**
- **Requester Pays** - Transfer costs to downloader
- **Object Holds** - Legal and temporary holds
- **Dual-region** - 99.95% SLA with geo-redundancy
- **Turbo Replication** - < 15 minute RPO between regions
- **[📖 Performance Optimization](https://cloud.google.com/storage/docs/request-rate)** - Request rate best practices

### Persistent Disks and Filestore

**Block and File Storage:**
- **Persistent Disk Types:**
  - **Standard (pd-standard)** - HDD, sequential workloads
  - **Balanced (pd-balanced)** - SSD, balanced price/performance
  - **SSD (pd-ssd)** - High-performance SSD
  - **Extreme (pd-extreme)** - Highest performance, configurable IOPS
- **[📖 Disk Types Comparison](https://cloud.google.com/compute/docs/disks)** - Performance and pricing
- **[📖 Regional Persistent Disks](https://cloud.google.com/compute/docs/disks/regional-persistent-disk)** - Synchronous replication
- **[📖 Disk Snapshots](https://cloud.google.com/compute/docs/disks/snapshots)** - Incremental backups
- **[📖 Filestore](https://cloud.google.com/filestore/docs)** - Managed NFS file server
- **[📖 Filestore Instances](https://cloud.google.com/filestore/docs/service-tiers)** - Basic, High Scale, Enterprise tiers

## Database Architecture

### Cloud SQL

**Managed Relational Databases:**
- Supports MySQL, PostgreSQL, SQL Server
- **High Availability Configuration:**
  - Regional HA with synchronous replication
  - Automatic failover (typically 60-120 seconds)
  - Read replicas for read scaling
- **[📖 Cloud SQL Overview](https://cloud.google.com/sql/docs/introduction)** - Architecture guide
- **[📖 High Availability](https://cloud.google.com/sql/docs/mysql/high-availability)** - HA architecture
- **[📖 Replication](https://cloud.google.com/sql/docs/mysql/replication)** - Read replicas and cross-region
- **[📖 Backup and Recovery](https://cloud.google.com/sql/docs/mysql/backup-recovery/backups)** - Backup strategies
- **[📖 Connection Options](https://cloud.google.com/sql/docs/mysql/connect-overview)** - Cloud SQL Proxy, Private IP

### Cloud Spanner

**Globally Distributed Relational Database:**
- Horizontally scalable, strongly consistent
- Global transactions with 99.999% availability SLA
- Multi-region configurations for HA and low latency
- **[📖 Cloud Spanner Overview](https://docs.cloud.google.com/spanner/docs)** - Architecture concepts
- **[📖 Replication](https://cloud.google.com/spanner/docs/replication)** - Multi-region replication
- **[📖 Schema Design Best Practices](https://cloud.google.com/spanner/docs/schema-design)** - Performance optimization
- **[📖 Instance Configurations](https://cloud.google.com/spanner/docs/instance-configurations)** - Regional and multi-regional
- **[📖 Choosing Between Cloud SQL and Spanner](https://docs.cloud.google.com/docs/databases)** - Decision guide

### Firestore and Datastore

**NoSQL Document Databases:**
- **Firestore** - Next-generation, real-time synchronization
- **Datastore Mode** - Server-side applications
- Automatic multi-region replication
- Strong consistency for entity group queries
- **[📖 Firestore Overview](https://cloud.google.com/firestore/docs)** - Complete guide
- **[📖 Choosing Between Firestore Modes](https://cloud.google.com/datastore/docs/firestore-or-datastore)** - Native vs Datastore mode
- **[📖 Data Modeling](https://cloud.google.com/firestore/docs/data-model)** - Document structure
- **[📖 Best Practices](https://cloud.google.com/firestore/docs/best-practices)** - Performance and cost optimization

### Bigtable

**Wide-Column NoSQL:**
- Petabyte-scale, sub-10ms latency
- Ideal for time-series, IoT, financial services
- HBase API compatible
- **[📖 Bigtable Overview](https://cloud.google.com/bigtable/docs/overview)** - Architecture and use cases
- **[📖 Schema Design](https://cloud.google.com/bigtable/docs/schema-design)** - Row key design critical
- **[📖 Replication](https://cloud.google.com/bigtable/docs/replication-overview)** - Multi-cluster replication
- **[📖 Performance Tuning](https://cloud.google.com/bigtable/docs/performance)** - Optimization guide
- **[📖 Choosing Between Bigtable and Other Databases](https://docs.cloud.google.com/bigtable/docs/overview)** - Decision tree

### BigQuery

**Serverless Data Warehouse:**
- Petabyte-scale analytics with standard SQL
- Separation of compute and storage
- Automatic optimization and indexing
- **[📖 BigQuery Architecture](https://cloud.google.com/bigquery/docs/how-to)** - Complete guide
- **[📖 Partitioning and Clustering](https://cloud.google.com/bigquery/docs/partitioned-tables)** - Query optimization
- **[📖 BigQuery BI Engine](https://cloud.google.com/bigquery/docs/bi-engine-intro)** - In-memory analytics
- **[📖 BigQuery ML](https://cloud.google.com/bigquery-ml/docs)** - Machine learning in SQL
- **[📖 Cost Optimization](https://cloud.google.com/bigquery/docs/best-practices-costs)** - Query cost management
- **[📖 Data Transfer Service](https://cloud.google.com/bigquery-transfer/docs)** - Scheduled data imports

### Memorystore

**Managed In-Memory Data Store:**
- **Memorystore for Redis** - Advanced features, persistence
- **Memorystore for Memcached** - Simple caching
- **[📖 Memorystore for Redis](https://cloud.google.com/memorystore/docs/redis)** - Redis architecture
- **[📖 High Availability](https://cloud.google.com/memorystore/docs/redis/high-availability)** - Standard vs basic tier

## Networking Architecture

### Virtual Private Cloud (VPC)

**Network Foundation:**
- Global resource spanning all regions
- Subnets are regional (not zonal)
- No inter-region bandwidth charges within VPC
- **[📖 VPC Overview](https://cloud.google.com/vpc/docs/overview)** - Fundamental concepts
- **[📖 VPC Network Design](https://cloud.google.com/vpc/docs/vpc)** - Best practices
- **[📖 Subnet Configuration](https://cloud.google.com/vpc/docs/subnets)** - IP addressing
- **[📖 Firewall Rules](https://cloud.google.com/vpc/docs/firewalls)** - Traffic control
- **[📖 Routes](https://cloud.google.com/vpc/docs/routes)** - Routing configuration
- **[📖 Alias IP Ranges](https://cloud.google.com/vpc/docs/alias-ip)** - Container and service IPs

**Advanced VPC Patterns:**
- **Shared VPC** - Cross-project networking
- **VPC Peering** - Private connectivity between VPCs
- **VPC Service Controls** - Security perimeters
- **Private Google Access** - Access Google APIs privately
- **Private Service Connect** - Private access to managed services
- **[📖 Shared VPC](https://cloud.google.com/vpc/docs/shared-vpc)** - Multi-project architecture
- **[📖 VPC Peering](https://cloud.google.com/vpc/docs/vpc-peering)** - VPC interconnection
- **[📖 VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs)** - Security perimeter
- **[📖 Private Google Access](https://cloud.google.com/vpc/docs/private-google-access)** - API access without internet
- **[📖 Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)** - Private service access

### Cloud Load Balancing

**Global Load Balancing:**
- Single anycast IP serving globally
- Automatic multi-region failover
- Layer 4 (TCP/UDP) and Layer 7 (HTTP/S) options
- **[📖 Load Balancing Overview](https://cloud.google.com/load-balancing/docs/load-balancing-overview)** - Architecture guide
- **[📖 Choosing a Load Balancer](https://cloud.google.com/load-balancing/docs/choosing-load-balancer)** - Decision tree
- **[📖 External HTTP(S) Load Balancer](https://cloud.google.com/load-balancing/docs/https)** - Global Layer 7
- **[📖 Internal HTTP(S) Load Balancer](https://cloud.google.com/load-balancing/docs/l7-internal)** - Regional Layer 7
- **[📖 Network Load Balancer](https://cloud.google.com/load-balancing/docs/network)** - Regional Layer 4
- **[📖 SSL Policies](https://cloud.google.com/load-balancing/docs/ssl-policies-concepts)** - TLS configuration
- **[📖 Cloud Armor](https://cloud.google.com/armor/docs)** - DDoS protection and WAF

### Cloud CDN

**Content Delivery Network:**
- Global edge network with Google's infrastructure
- Cache-to-cache filling reduces origin load
- Integration with Cloud Load Balancing
- **[📖 Cloud CDN Overview](https://cloud.google.com/cdn/docs/overview)** - Architecture
- **[📖 Caching Best Practices](https://cloud.google.com/cdn/docs/best-practices)** - Performance optimization
- **[📖 Cache Keys and Modes](https://cloud.google.com/cdn/docs/caching)** - Cache control
- **[📖 Signed URLs and Cookies](https://cloud.google.com/cdn/docs/using-signed-urls)** - Content access control

### Hybrid Connectivity

**Connecting to Google Cloud:**
- **Cloud VPN** - IPsec, up to 3 Gbps per tunnel with HA VPN
- **Cloud Interconnect** - Dedicated physical connections
  - **Dedicated** - 10 or 100 Gbps direct connection
  - **Partner** - 50 Mbps to 50 Gbps via partner
- **[📖 Hybrid Connectivity Overview](https://docs.cloud.google.com/network-connectivity/docs/concepts)** - Options comparison
- **[📖 Cloud VPN](https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview)** - VPN architecture
- **[📖 HA VPN](https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview#ha-vpn)** - High availability VPN
- **[📖 Cloud Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/overview)** - Dedicated connectivity
- **[📖 Partner Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/partner-overview)** - Service provider connectivity
- **[📖 Cloud Router](https://cloud.google.com/network-connectivity/docs/router)** - Dynamic BGP routing

**Network Intelligence Center:**
- **[📖 Network Topology](https://cloud.google.com/network-intelligence-center/docs/network-topology/concepts/overview)** - Visualization
- **[📖 Connectivity Tests](https://cloud.google.com/network-intelligence-center/docs/connectivity-tests/concepts/overview)** - Troubleshooting
- **[📖 Performance Dashboard](https://cloud.google.com/network-intelligence-center/docs/performance-dashboard/concepts/overview)** - Monitoring

## Security and Identity

### Identity and Access Management (IAM)

**Principle of Least Privilege:**
- **Who** - Google Account, Service Account, Google Group, Cloud Identity domain
- **What** - Resources (projects, folders, organization)
- **How** - Roles (primitive, predefined, custom)
- **[📖 IAM Overview](https://cloud.google.com/iam/docs/overview)** - Core concepts
- **[📖 IAM Roles](https://cloud.google.com/iam/docs/understanding-roles)** - Role types and hierarchy
- **[📖 Custom Roles](https://cloud.google.com/iam/docs/creating-custom-roles)** - Role creation
- **[📖 IAM Conditions](https://cloud.google.com/iam/docs/conditions-overview)** - Conditional access
- **[📖 IAM Best Practices](https://docs.cloud.google.com/iam/docs/using-iam-securely)** - Security guidelines
- **[📖 Policy Intelligence](https://docs.cloud.google.com/policy-intelligence/docs)** - Policy analysis tools

### Service Accounts

**Application Identity:**
- Default compute service account (not recommended for production)
- User-managed service accounts (recommended)
- Short-lived credentials via Workload Identity Federation
- **[📖 Service Accounts](https://cloud.google.com/iam/docs/service-accounts)** - Complete guide
- **[📖 Best Practices](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts)** - Security patterns
- **[📖 Workload Identity](https://cloud.google.com/iam/docs/workload-identity-federation)** - External identity federation
- **[📖 Service Account Impersonation](https://cloud.google.com/iam/docs/impersonating-service-accounts)** - Delegation patterns

### Encryption

**Data Protection:**
- **Encryption at rest** - Default with Google-managed keys
- **Customer-Managed Encryption Keys (CMEK)** - Cloud KMS integration
- **Customer-Supplied Encryption Keys (CSEK)** - Customer-provided keys
- **[📖 Encryption at Rest](https://cloud.google.com/docs/security/encryption/default-encryption)** - Default encryption
- **[📖 Cloud KMS](https://cloud.google.com/kms/docs)** - Key management service
- **[📖 CMEK](https://cloud.google.com/kms/docs/cmek)** - Customer-managed keys
- **[📖 Cloud HSM](https://cloud.google.com/kms/docs/hsm)** - Hardware security modules
- **[📖 Secret Manager](https://cloud.google.com/secret-manager/docs)** - Secrets storage

### Security Command Center

**Centralized Security Management:**
- Asset discovery and inventory
- Vulnerability scanning
- Threat detection
- Compliance monitoring
- **[📖 Security Command Center](https://cloud.google.com/security-command-center/docs)** - Overview
- **[📖 Asset Discovery](https://docs.cloud.google.com/asset-inventory/docs/asset-inventory-overview)** - Inventory management
- **[📖 Finding Types](https://docs.cloud.google.com/security-command-center/docs/finding-classes)** - Security findings

### Identity-Aware Proxy (IAP)

**Application-Level Access Control:**
- Zero-trust access to applications
- No VPN required
- Context-aware access controls
- **[📖 Identity-Aware Proxy](https://cloud.google.com/iap/docs)** - Architecture guide
- **[📖 IAP TCP Forwarding](https://cloud.google.com/iap/docs/tcp-forwarding-overview)** - SSH/RDP access

## Operations and Observability

### Cloud Monitoring (Operations Suite)

**Monitoring and Alerting:**
- Infrastructure and application metrics
- Custom metrics from applications
- Uptime checks and alerting
- **[📖 Cloud Monitoring](https://cloud.google.com/monitoring/docs)** - Complete guide
- **[📖 Metrics](https://cloud.google.com/monitoring/api/metrics_gcp)** - Available metrics
- **[📖 Alerting](https://cloud.google.com/monitoring/alerts)** - Alert policies
- **[📖 Dashboards](https://cloud.google.com/monitoring/dashboards)** - Visualization
- **[📖 Uptime Checks](https://cloud.google.com/monitoring/uptime-checks)** - Availability monitoring

### Cloud Logging (Operations Suite)

**Centralized Log Management:**
- All GCP service logs automatically collected
- Log sinks to BigQuery, Cloud Storage, Pub/Sub
- Log-based metrics for custom monitoring
- **[📖 Cloud Logging](https://cloud.google.com/logging/docs)** - Architecture overview
- **[📖 Logs Router](https://cloud.google.com/logging/docs/routing/overview)** - Log routing
- **[📖 Log Sinks](https://cloud.google.com/logging/docs/export)** - Export destinations
- **[📖 Logs Explorer](https://cloud.google.com/logging/docs/view/logs-explorer-interface)** - Query interface
- **[📖 Audit Logs](https://cloud.google.com/logging/docs/audit)** - Compliance logging

### Cloud Trace and Profiler

**Application Performance:**
- **Cloud Trace** - Distributed tracing for latency analysis
- **Cloud Profiler** - Continuous CPU and memory profiling
- **Cloud Debugger** - Production debugging without stopping
- **[📖 Cloud Trace](https://cloud.google.com/trace/docs)** - Latency tracking
- **[📖 Cloud Profiler](https://cloud.google.com/profiler/docs)** - Performance profiling
- **[📖 Error Reporting](https://cloud.google.com/error-reporting/docs)** - Error aggregation

## Migration Strategies

### Migration Framework (5 Rs)

**Migration Patterns:**
1. **Rehost** - Lift-and-shift to Compute Engine
2. **Replatform** - Minor optimizations (e.g., Cloud SQL instead of self-managed)
3. **Refactor** - Re-architect for cloud-native (serverless, microservices)
4. **Retire** - Decommission unnecessary systems
5. **Retain** - Keep on-premises temporarily

**Migration Tools:**
- **Migrate for Compute Engine** - VM migration from on-prem or other clouds
- **Database Migration Service** - Continuous replication for minimal downtime
- **Transfer Appliance** - Physical data transfer for large datasets
- **Storage Transfer Service** - Online data transfer
- **[📖 Migration to Google Cloud](https://cloud.google.com/architecture/migration-to-gcp-getting-started)** - Migration framework
- **[📖 Migrate for Compute Engine](https://cloud.google.com/migrate/compute-engine/docs)** - VM migration
- **[📖 Database Migration Service](https://cloud.google.com/database-migration/docs)** - Database migration
- **[📖 Transfer Appliance](https://cloud.google.com/transfer-appliance/docs)** - Offline data transfer
- **[📖 Storage Transfer Service](https://cloud.google.com/storage-transfer/docs)** - Online data transfer

## Cost Optimization

### Compute Cost Optimization

**Cost-Effective Compute:**
- **Committed Use Discounts** - 1 or 3 year, up to 57% savings
- **Sustained Use Discounts** - Automatic discounts for running instances
- **Preemptible VMs** - Up to 80% savings, 24-hour max
- **Spot VMs** - More flexible preemptible alternative
- **Custom Machine Types** - Right-size CPU and memory
- **[📖 Pricing Overview](https://cloud.google.com/pricing)** - GCP pricing model
- **[📖 Committed Use Discounts](https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview)** - Long-term commitments
- **[📖 Resource-Based Pricing](https://cloud.google.com/compute/vm-instance-pricing)** - Per-second billing
- **[📖 Pricing Calculator](https://cloud.google.com/products/calculator)** - Cost estimation

### Storage Cost Optimization

**Storage Classes and Lifecycle:**
- Autoclass for Cloud Storage buckets
- Object lifecycle management
- Nearline/Coldline/Archive for infrequent access
- Regional vs multi-region trade-offs
- **[📖 Storage Cost Optimization](https://cloud.google.com/storage/docs/best-practices#cost-optimization)** - Best practices

### Cost Management Tools

**Visibility and Control:**
- **Cost Management** - Budgets, alerts, reports
- **Recommender** - AI-powered cost and performance recommendations
- **Active Assist** - Proactive optimization recommendations
- **[📖 Cost Management](https://cloud.google.com/cost-management)** - Cost visibility
- **[📖 Billing Reports](https://cloud.google.com/billing/docs/how-to/reports)** - Cost analysis
- **[📖 Budgets and Alerts](https://cloud.google.com/billing/docs/how-to/budgets)** - Cost controls
- **[📖 Recommender](https://cloud.google.com/recommender/docs)** - Optimization recommendations

## High Availability and Disaster Recovery

### Availability Patterns

**Multi-Zonal and Multi-Regional:**
- **Zonal Resources** - Compute Engine instances, persistent disks
- **Regional Resources** - Cloud SQL, regional MIGs, subnets
- **Multi-Regional Resources** - Cloud Storage, Spanner
- **Global Resources** - VPC networks, load balancers, Cloud CDN

### Disaster Recovery Strategies

**RTO and RPO Trade-offs:**

| Strategy | RTO | RPO | Cost | Use Case |
|----------|-----|-----|------|----------|
| **Backup & Restore** | Hours | Hours | $ | Dev/test, non-critical |
| **Pilot Light** | 10s of minutes | Minutes | $$ | Lower-tier production |
| **Warm Standby** | Minutes | Seconds | $$$ | Business-critical |
| **Active-Active Multi-Region** | Seconds | Near-zero | $$$$ | Mission-critical |

**DR Best Practices:**
- Regular backup testing and validation
- Automated failover procedures
- Multi-region replication for critical data
- Documentation and runbooks
- Periodic DR drills

## Compliance and Governance

### Resource Hierarchy

**Organization Structure:**
```
Organization
├── Folder (Business Unit)
│   ├── Folder (Environment)
│   │   ├── Project (Application)
│   │   └── Project (Application)
```

- **[📖 Resource Hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)** - Organization structure
- **[📖 Organization Policies](https://cloud.google.com/resource-manager/docs/organization-policy/overview)** - Centralized constraints
- **[📖 Project Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations#project-structure)** - Project design

### Compliance and Certifications

**Regulatory Compliance:**
- ISO 27001, SOC 2/3, PCI-DSS, HIPAA, GDPR
- Regional data residency controls
- Compliance reports and certifications
- **[📖 Compliance Offerings](https://cloud.google.com/compliance)** - Certifications and reports
- **[📖 Data Residency](https://cloud.google.com/terms/data-residency)** - Location controls

## Common Architecture Patterns

### Pattern 1: Three-Tier Web Application

**Architecture:**
- **Presentation Tier** - Cloud Load Balancer + Cloud CDN
- **Application Tier** - Managed Instance Group (auto-scaling)
- **Data Tier** - Cloud SQL with read replicas

**Key Services:**
- Global HTTP(S) Load Balancer
- Cloud CDN for static assets
- Cloud Armor for DDoS protection
- VPC with private subnets
- Cloud SQL with HA configuration

### Pattern 2: Microservices on GKE

**Architecture:**
- GKE Autopilot or Standard cluster
- Workload Identity for service authentication
- Cloud SQL Proxy for database access
- Anthos Service Mesh for observability

**Key Services:**
- GKE with VPC-native networking
- Cloud Build for CI/CD
- Artifact Registry for container images
- Cloud Monitoring for observability

### Pattern 3: Real-Time Data Pipeline

**Architecture:**
- **Ingestion** - Pub/Sub for event streaming
- **Processing** - Dataflow for stream processing
- **Storage** - BigQuery for analytics
- **Visualization** - Looker or Data Studio

**Key Services:**
- Pub/Sub for decoupling
- Dataflow for ETL
- BigQuery for warehousing
- Dataproc for Hadoop/Spark workloads

### Pattern 4: Serverless Application

**Architecture:**
- Cloud Run or Cloud Functions for compute
- Firestore for NoSQL database
- Cloud Storage for object storage
- API Gateway for API management

**Key Services:**
- Cloud Run with automatic scaling
- Eventarc for event routing
- Secret Manager for credentials
- Cloud CDN for caching

### Pattern 5: Hybrid Cloud with Anthos

**Architecture:**
- GKE clusters on GCP and on-premises
- Anthos Config Management for policy
- Anthos Service Mesh for networking
- Cloud Interconnect for connectivity

**Key Services:**
- Anthos GKE on-prem
- Cloud VPN or Interconnect
- Binary Authorization
- Cloud Operations suite

## Data Engineering Architecture

### Batch Processing

**MapReduce and Spark:**
- **Dataproc** - Managed Hadoop and Spark
- **Dataflow** - Serverless Apache Beam pipelines
- **[📖 Dataproc](https://cloud.google.com/dataproc/docs)** - Managed big data
- **[📖 Dataflow](https://cloud.google.com/dataflow/docs)** - Stream and batch processing

### Stream Processing

**Real-Time Analytics:**
- **Pub/Sub** - Global message queue
- **Dataflow** - Stream processing
- **Bigtable** - High-throughput writes
- **[📖 Pub/Sub](https://cloud.google.com/pubsub/docs)** - Messaging architecture
- **[📖 Streaming Analytics](https://cloud.google.com/solutions/stream-analytics)** - Reference architecture

### Data Warehousing

**BigQuery Architecture:**
- Columnar storage for analytics
- Automatic query optimization
- Federated queries across sources
- **[📖 BigQuery Best Practices](https://cloud.google.com/bigquery/docs/best-practices-performance-overview)** - Performance guide

## Machine Learning and AI

### AI Platform and Agent Platform

**ML Workflow:**
- **Agent Platform (formerly Vertex AI)** - Unified ML platform
- Training with custom or pre-built containers
- Model deployment and serving
- **[📖 Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform)** - ML platform
- **[📖 AutoML](https://cloud.google.com/vertex-ai/docs/beginner/beginners-guide)** - No-code ML

### Pre-Trained APIs

**AI Services:**
- Vision API, Natural Language API, Translation API
- Speech-to-Text, Text-to-Speech
- **[📖 Cloud AI Products](https://cloud.google.com/products/ai)** - AI/ML services

## DevOps and CI/CD

### Cloud Build

**Continuous Integration:**
- Serverless build service
- Container and non-container builds
- Integration with GitHub, Bitbucket, Cloud Source Repositories
- **[📖 Cloud Build](https://cloud.google.com/build/docs)** - CI/CD platform

### Infrastructure as Code

**Deployment Automation:**
- **Deployment Manager** - Native GCP IaC
- **Terraform** - Multi-cloud IaC (popular choice)
- **Config Connector** - Kubernetes-native GCP resource management
- **[📖 Deployment Manager](https://cloud.google.com/deployment-manager/docs)** - GCP native IaC
- **[📖 Terraform on GCP](https://cloud.google.com/docs/terraform)** - Terraform integration

## Exam Scenarios and Solutions

### Scenario 1: High-Traffic Web Application

**Requirements:** Handle millions of requests, global users, cost-effective

**Solution:**
- Global HTTP(S) Load Balancer with Cloud CDN
- Regional Managed Instance Groups with autoscaling
- Cloud SQL with read replicas or Cloud Spanner
- Cloud Storage for static assets
- Cloud Armor for security

**Key Decision:** Cloud Spanner if multi-region writes needed, else Cloud SQL with cross-region read replicas

### Scenario 2: Lift-and-Shift Migration

**Requirements:** Migrate 100+ VMs from on-premises quickly

**Solution:**
- Migrate for Compute Engine
- Phased migration approach
- Cloud VPN or Interconnect for connectivity
- Use Committed Use Discounts for cost savings

**Key Decision:** Start with non-critical workloads, validate, then migrate production

### Scenario 3: Real-Time Analytics

**Requirements:** Ingest millions of events per second, real-time dashboards

**Solution:**
- Pub/Sub for ingestion
- Dataflow for stream processing
- BigQuery for data warehouse
- Bigtable for operational queries
- Looker or Data Studio for visualization

**Key Decision:** BigQuery for ad-hoc analytics, Bigtable for operational low-latency queries

### Scenario 4: Hybrid Cloud

**Requirements:** Keep sensitive data on-premises, use GCP for compute

**Solution:**
- Cloud Interconnect (dedicated) for consistent performance
- Shared VPC for network segregation
- Private Google Access for API calls
- Cloud SQL with private IP
- Anthos if running Kubernetes workloads

**Key Decision:** Dedicated Interconnect vs Partner Interconnect based on bandwidth needs

### Scenario 5: Disaster Recovery

**Requirements:** RPO < 1 hour, RTO < 4 hours

**Solution:**
- Pilot Light strategy
- Cloud SQL automated backups
- Persistent disk snapshots to Cloud Storage
- Infrastructure as Code for rapid deployment
- Runbooks in Cloud Storage

**Key Decision:** Warm Standby if stricter RTO/RPO needed

### Scenario 6: Multi-Tenant SaaS

**Requirements:** Isolate customer data, cost attribution

**Solution:**
- Separate projects per customer (strong isolation)
- OR Shared infrastructure with tagging (cost-effective)
- Folder hierarchy for organization
- Labels for cost allocation
- VPC Service Controls for data exfiltration protection

**Key Decision:** Isolation level vs cost trade-off

## Exam Tips and Strategy

### Keywords to Watch

**Question Patterns:**
- **"Cost-effective"** → Committed use, preemptible, autoscaling, Cloud Functions/Run
- **"Minimize operational overhead"** → Managed services, serverless, GKE Autopilot
- **"High availability"** → Multi-zone, multi-region, load balancing
- **"Low latency"** → Memorystore, CDN, proximity to users, Bigtable
- **"Compliance/regulatory"** → VPC Service Controls, organization policies, audit logs
- **"Real-time"** → Pub/Sub, Dataflow, Bigtable
- **"Big data analytics"** → BigQuery, Dataproc, Dataflow
- **"Secure"** → VPC, IAM, CMEK, Private Google Access

### Service Selection Decision Trees

**Compute Decision:**
```
Stateless application?
├─ YES → Container?
│  ├─ YES → Need Kubernetes?
│  │  ├─ YES → GKE
│  │  └─ NO → Cloud Run
│  └─ NO → Need custom runtime?
│     ├─ YES → App Engine Flexible
│     └─ NO → App Engine Standard
└─ NO → Compute Engine
```

**Database Decision:**
```
Relational needed?
├─ YES → Global transactions?
│  ├─ YES → Cloud Spanner
│  └─ NO → Cloud SQL
└─ NO → Data model?
   ├─ Key-Value/Document → Firestore
   ├─ Wide-Column → Bigtable
   └─ Analytics → BigQuery
```

### Time Management

- 120 minutes ÷ 50 questions = 2.4 minutes per question
- First pass: Answer confident questions (60 minutes)
- Second pass: Tackle difficult questions (45 minutes)
- Final pass: Review flagged questions (15 minutes)

### Common Traps

- ❌ Choosing complex solutions when simple ones suffice
- ❌ Ignoring cost constraints
- ❌ Over-emphasizing technical perfection vs business needs
- ❌ Not considering operational overhead
- ❌ Forgetting about managed service alternatives
- ❌ Mixing up service capabilities and limits

### Study Checklist

**Knowledge Areas:**
- [ ] Can design multi-tier applications on GCP
- [ ] Understand VPC networking, shared VPC, and VPC peering
- [ ] Know when to use each compute option (GCE, GKE, App Engine, Cloud Run, Functions)
- [ ] Can select appropriate database for use case
- [ ] Understand migration strategies and tools
- [ ] Know cost optimization techniques
- [ ] Can design for high availability and disaster recovery
- [ ] Understand IAM, service accounts, and security best practices
- [ ] Know monitoring and logging setup
- [ ] Familiar with hybrid connectivity options

**Preparation:**
- [ ] Hands-on experience with GCP (build actual projects)
- [ ] Review all case studies on exam guide
- [ ] Complete practice exams (80%+ score)
- [ ] Read official GCP Architecture Framework
- [ ] Review common reference architectures
- [ ] Practice with GCP Console and gcloud CLI

---

**Pro Tip:** The Professional Cloud Architect exam tests your ability to make architecture trade-offs based on business requirements. Always consider: cost, operational overhead, performance, security, compliance, and scalability. The "best" answer balances all these factors based on scenario constraints!

**Documentation Count:** This fact sheet contains 100+ embedded documentation links to official Google Cloud documentation.

**Good luck!** This certification demonstrates expert-level cloud architecture skills on Google Cloud Platform.
