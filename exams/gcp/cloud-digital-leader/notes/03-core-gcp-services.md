# Core Google Cloud Platform Services

> **Cloud Digital Leader Focus:** This section covers GCP services from a BUSINESS perspective - understanding WHAT services do, WHY to choose them, and WHEN to use them for business value. Focus on business outcomes, cost optimization, and strategic decision-making.

## Compute Services Overview

Compute services form the foundation of your cloud infrastructure. The key business question is: **How much operational responsibility do you want?**

**Business Decision Framework:**
- **Full control needed?** Choose Compute Engine (IaaS)
- **Focus on code, not infrastructure?** Choose App Engine (PaaS)
- **Containerized applications?** Choose GKE or Cloud Run
- **Event-driven, short tasks?** Choose Cloud Functions
- **Serverless containers?** Choose Cloud Run

## Compute Services

### Compute Engine (IaaS)
**What it is:** Virtual machines running in Google's data centers - maximum control and flexibility

**Business Value:**
- **Cost optimization:** Custom machine types prevent over-provisioning (only pay for exact resources needed)
- **Legacy migration:** Easiest path for "lift-and-shift" migrations from on-premises
- **No vendor lock-in:** Standard VMs work like any server environment
- **Business continuity:** Live migration means zero downtime during maintenance
- **Budget control:** Sustained use discounts (up to 30%) automatic, no upfront commitment

**Key Business Features:**
- **Custom machine types:** Tailor CPU and memory to your needs - optimize costs by avoiding oversized instances
- **Preemptible instances:** Up to 80% cost savings for fault-tolerant workloads (batch processing, rendering)
- **Live migration:** Zero-downtime maintenance - Google moves VMs between hosts transparently
- **Sustained use discounts:** Automatic discounts (up to 30%) for long-running instances - no commitment required
- **Committed use discounts:** 57% savings for 1-year, 70% for 3-year commitments
- **Global load balancing:** Distribute traffic across regions for performance and reliability

**When to Choose Compute Engine (Business Perspective):**
- Migrating existing applications with minimal changes (lift-and-shift strategy)
- Applications requiring specific OS configurations or licensed software
- Need full control over the operating system and environment
- Running workloads where you want to optimize every aspect of cost and performance
- Legacy applications that cannot be easily containerized or refactored

**Business Use Cases:**
- Web servers and application hosting for traditional architectures
- Development and testing environments that need various configurations
- High-performance computing (HPC) for research, financial modeling, rendering
- SAP, Oracle, and enterprise applications requiring specific configurations
- Disaster recovery infrastructure (cost-effective with preemptible instances)

**Cost Considerations:**
- Most flexible pricing with per-second billing (1-minute minimum)
- Sustained use discounts automatic - good for always-on workloads
- Preemptible VMs for 80% savings on non-critical workloads
- Custom machine types prevent waste from oversized instances
- Budget visibility: easy to track and forecast costs

**Pricing Model:** Pay per second with a 1-minute minimum; automatic discounts for sustained use

### App Engine (PaaS)
**What it is:** Platform for building and hosting web applications - focus on code, Google manages infrastructure

**Business Value:**
- **Faster time-to-market:** Developers focus on business logic, not infrastructure management
- **Automatic cost optimization:** Scale to zero when idle, no paying for unused capacity
- **Reduced operational overhead:** No need for DevOps team to manage servers, patching, scaling
- **Traffic management:** Built-in A/B testing and gradual rollouts reduce deployment risk
- **Developer productivity:** Integrated services (caching, task queues, authentication) accelerate development

**Key Business Features:**
- **Automatic scaling:** Scale to zero (pay nothing when idle) or handle traffic spikes automatically
- **Multiple language support:** Java, Python, PHP, Go, Node.js, .NET, Ruby - use your team's expertise
- **Integrated services:** Built-in services for common needs (reduce third-party service costs)
- **Version management:** Deploy multiple versions and split traffic for A/B testing and safe rollouts
- **No server management:** Eliminate operational overhead - no patching, no capacity planning

**When to Choose App Engine (Business Perspective):**
- Startups and small teams without dedicated operations staff
- Applications with unpredictable or variable traffic (scales automatically)
- Rapid application development and prototyping (fastest path to production)
- Web applications and APIs that fit standard patterns
- When reducing operational costs and complexity is the priority

**Business Use Cases:**
- Web applications with variable traffic (e-commerce sites, campaign landing pages)
- RESTful APIs for mobile and web applications
- Microservices architecture for agile development
- Rapid prototyping and MVP development for startups
- Internal business applications with intermittent usage

**Cost Considerations:**
- Pay only for actual usage - scales to zero when idle
- No infrastructure management costs (staff time savings)
- Standard environment: Lower cost, faster scaling, more restrictions
- Flexible environment: Higher cost, more flexibility, slower scaling
- Good for variable workloads that benefit from auto-scaling

**Environments:**
- **Standard:** Preconfigured runtime environments, fastest scaling, lowest cost, some restrictions
- **Flexible:** Docker containers with more flexibility, slower scaling, higher cost

### Google Kubernetes Engine (GKE)
**What it is:** Managed Kubernetes service for containerized applications - enterprise-grade container orchestration

**Business Value:**
- **Application portability:** Avoid vendor lock-in with industry-standard Kubernetes
- **Multi-cloud strategy:** Run same applications on GCP, on-premises, or other clouds (with Anthos)
- **Operational efficiency:** Google manages Kubernetes complexity, your team focuses on applications
- **Resource optimization:** Bin-packing and autoscaling maximize infrastructure utilization
- **Enterprise security:** Built-in compliance, security scanning, and identity management

**Key Business Features:**
- **Managed Kubernetes:** Google manages the control plane (no management overhead, 99.95% SLA)
- **Auto-scaling:** Horizontal pod autoscaling and cluster autoscaling optimize costs and performance
- **Security:** Workload Identity, Binary Authorization, vulnerability scanning reduce security risk
- **Integrated monitoring:** Built-in logging and monitoring provide operational visibility
- **Multi-cloud:** Anthos enables consistent deployment across clouds and on-premises

**When to Choose GKE (Business Perspective):**
- Containerized applications requiring complex orchestration
- Multi-cloud or hybrid cloud strategy (avoid vendor lock-in)
- Microservices architecture with many independent services
- Teams with Kubernetes expertise or investment
- Applications requiring high availability and sophisticated deployment patterns

**Business Use Cases:**
- Enterprise microservices platforms requiring scalability and resilience
- Hybrid deployments connecting cloud and on-premises data centers
- CI/CD pipelines for automated testing and deployment
- SaaS platforms requiring tenant isolation and resource management
- Applications requiring gradual rollouts, blue-green deployments

**Cost Considerations:**
- Pay for worker nodes (VMs) running your containers
- Control plane is free for standard clusters, charged for Autopilot
- Autopilot mode: Google manages nodes, you pay only for pod resources (simplified billing)
- Standard mode: You manage nodes, more control, more complexity
- Spot nodes available for 80% savings on fault-tolerant workloads

**Node Types:**
- **Standard nodes:** Traditional VMs for containers - full control
- **Spot nodes:** Preemptible instances for 80% cost savings on batch/fault-tolerant workloads

### Cloud Functions (Serverless)
**What it is:** Event-driven serverless compute platform - pay only for execution time

**Business Value:**
- **Zero infrastructure cost:** No servers to manage or pay for when idle
- **Instant scalability:** Handle traffic spikes automatically without capacity planning
- **Rapid development:** Simple deployment model accelerates time-to-market
- **Event-driven architecture:** React to business events in real-time
- **Cost efficiency:** Sub-second billing, pay only for actual execution

**Key Business Features:**
- **Event-driven:** Triggered by events from GCP services (automate business processes)
- **Auto-scaling:** Scale from zero to handle traffic (no wasted capacity)
- **Pay-per-use:** Only pay for execution time (sub-100ms billing increments)
- **Multiple triggers:** HTTP, Cloud Storage, Pub/Sub, Firestore (integrate with existing systems)
- **Language support:** Node.js, Python, Go, Java, .NET, Ruby, PHP (use existing skills)

**When to Choose Cloud Functions (Business Perspective):**
- Simple, single-purpose functions responding to events
- Glue code connecting different services and APIs
- Workloads with unpredictable, sporadic usage patterns
- Real-time data processing pipelines
- Budget-conscious projects requiring minimal infrastructure cost

**Business Use Cases:**
- API backends and webhooks for integrations (Slack bots, payment webhooks)
- Data processing and ETL (process files uploaded to Cloud Storage)
- IoT data processing (respond to sensor data in real-time)
- Real-time file processing (image thumbnails, document conversion)
- Scheduled tasks and automation (data exports, cleanup jobs)

**Cost Considerations:**
- Extremely low cost for low-volume workloads (generous free tier)
- Pay only for execution time (to nearest 100ms)
- No cost when functions are not running
- Best for short-lived tasks (max 9 minutes execution)
- Invocations are also metered (very low cost per million)

**Trigger Types:**
- **HTTP triggers:** Direct HTTP requests (webhooks, APIs)
- **Background triggers:** Cloud events from storage, database, messaging services

### Cloud Run
**What it is:** Fully managed serverless platform for containerized applications - serverless + containers

**Business Value:**
- **Application portability:** Use standard containers, avoid vendor lock-in
- **Developer flexibility:** Run any language, any library, any binary
- **Cost efficiency:** Scale to zero, pay only for actual requests and compute time
- **Fast deployment:** Deploy containers in seconds without infrastructure management
- **No Kubernetes complexity:** Get container benefits without Kubernetes overhead

**Key Business Features:**
- **Container-based:** Deploy any containerized application (Docker, etc.) - ultimate flexibility
- **Automatic scaling:** Scale to zero (no cost when idle) or handle traffic spikes instantly
- **Request-based billing:** Pay only for requests and compute time (to the nearest 100ms)
- **Portable:** Standard container runtime - migrate easily to other platforms
- **Integrated security:** Built-in TLS, DDoS protection, IAM integration

**When to Choose Cloud Run (Business Perspective):**
- Containerized applications needing serverless benefits (cost, scaling)
- Applications using languages or libraries not supported by App Engine
- Existing containerized applications you want to run serverless
- Teams already using containers but wanting to avoid Kubernetes complexity
- Web applications and APIs requiring fast, automatic scaling

**Business Use Cases:**
- Containerized web applications and REST APIs
- Microservices that need to scale independently
- Batch processing jobs that run on-demand
- Event-driven applications processing business events
- Migration of containerized apps from other platforms (preserving investments)

**Cost Considerations:**
- Pay only for requests and compute time (100ms billing increments)
- Scales to zero - no cost when idle
- More expensive per request than always-on VMs, but cheaper for variable workloads
- No cluster management costs (unlike GKE)
- Free tier includes 2 million requests per month

**Cloud Run vs. GKE Decision:**
- **Choose Cloud Run:** Simpler applications, variable traffic, want zero operational overhead
- **Choose GKE:** Complex orchestration needs, multi-cloud portability, sophisticated deployment patterns

## Storage Services Overview

Storage is often the largest cloud cost after compute. The key business question is: **How frequently will you access this data?**

**Business Decision Framework:**
- **Unstructured data (files, images, videos)?** Choose Cloud Storage
- **VM disk storage?** Choose Persistent Disks
- **Shared file storage across VMs?** Choose Filestore
- **Access frequency determines cost:** Standard > Nearline > Coldline > Archive

## Storage Services

### Cloud Storage (Object Storage)
**What it is:** Scalable object storage for unstructured data - unlimited capacity, global availability

**Business Value:**
- **Cost optimization:** Pay only for what you use, no capacity planning, automatic lifecycle management
- **99.999999999% durability:** Data is virtually never lost (11 nines of durability)
- **Global reach:** Serve content globally with low latency through Google's network
- **No infrastructure management:** No storage arrays, no capacity planning, no administration
- **Seamless scaling:** Store exabytes without performance degradation

**Storage Classes (Critical for Cost Optimization):**
- **Standard:** Frequently accessed data (>1x/month) - highest cost, no retrieval fees, best for hot data
- **Nearline:** Infrequently accessed data (1x/month) - 50% cheaper, small retrieval fee, 30-day minimum
- **Coldline:** Rarely accessed data (1x/quarter) - 70% cheaper, higher retrieval fee, 90-day minimum
- **Archive:** Long-term archival (1x/year) - 90% cheaper, highest retrieval fee, 365-day minimum

**Key Business Features:**
- **Global accessibility:** Access from anywhere on the internet via API, console, or command line
- **Automatic redundancy:** Data replicated across multiple locations automatically (no extra cost)
- **Lifecycle management:** Automatic data class transitions based on age or access patterns (optimize costs automatically)
- **Security:** Encryption at rest and in transit by default, granular access controls
- **Integration:** Works seamlessly with all GCP services (BigQuery, Dataflow, Agent Platform (formerly Vertex AI))
- **Versioning:** Keep multiple versions of objects for data protection and compliance

**When to Choose Cloud Storage (Business Perspective):**
- Storing unstructured data (files, images, videos, backups, logs)
- Need unlimited storage without capacity planning
- Serving content globally to users or applications
- Building data lakes for analytics (BigQuery can query directly)
- Long-term data retention for compliance (cheaper than tape)

**Business Use Cases:**
- Website content and media files (images, videos, downloads)
- Data backup and archival (replace tape backups, 11 nines durability)
- Data lake for analytics (store raw data, query with BigQuery)
- Content distribution for global applications
- Disaster recovery storage (off-site backup location)
- Machine learning training datasets (integrates with Agent Platform)
- Log storage and compliance archives

**Cost Considerations:**
- Choose storage class based on access frequency (biggest cost factor)
- Standard: $0.020/GB/month, no retrieval costs
- Nearline: $0.010/GB/month, $0.01/GB retrieval
- Coldline: $0.004/GB/month, $0.02/GB retrieval
- Archive: $0.0012/GB/month, $0.05/GB retrieval
- Lifecycle policies automate transitions to cheaper classes
- Egress charges apply when data leaves GCP

**Cost Optimization Strategy:**
- Use Standard for frequently accessed data (active data)
- Automatically transition to Nearline after 30 days (monthly access)
- Move to Coldline after 90 days (quarterly access)
- Archive for compliance and long-term retention (annual access)
- Object Lifecycle Management automates this (set it and forget it)

### Persistent Disks
**What it is:** High-performance block storage for virtual machines - like hard drives for your VMs

**Business Value:**
- **Performance options:** Match disk performance to application needs, control costs
- **Data protection:** Automatic encryption and snapshot backups protect business data
- **High availability:** Regional disks provide automatic replication across zones
- **Flexibility:** Resize disks without downtime as business needs grow
- **Reliability:** 99.999% annual uptime for regional persistent disks

**Types (Choose Based on Performance Needs):**
- **Standard persistent disks:** HDD-based storage - lowest cost, good for sequential access (file storage, backups)
- **SSD persistent disks:** High-performance SSD storage - balanced price/performance (most databases, applications)
- **Extreme persistent disks:** Highest performance for demanding workloads (SAP HANA, high-transaction databases)

**Key Business Features:**
- **Encryption:** Encrypted by default at no extra cost (compliance requirement)
- **Snapshots:** Point-in-time backups for disaster recovery and data protection
- **Resizing:** Resize disks without downtime (adapt to changing business needs)
- **Regional disks:** Replicated across zones for high availability (99.999% SLA vs 99.9% for zonal)

**When to Choose Persistent Disks (Business Perspective):**
- VM-based applications requiring block storage
- Databases running on Compute Engine
- Applications requiring high IOPS and low latency
- Business-critical applications needing high availability

**Business Use Cases:**
- Database storage for SQL Server, Oracle, MySQL on VMs
- File systems for application servers
- Boot disks for virtual machines
- Development and test environments

**Cost Considerations:**
- Pay for provisioned capacity (not usage)
- Standard: $0.040/GB/month (lowest cost)
- SSD: $0.170/GB/month (4x more, much faster)
- Extreme: $0.290/GB/month (highest performance)
- Snapshots charged separately ($0.026/GB/month)
- Regional disks cost 2x zonal but provide replication

### Filestore
**What it is:** Fully managed Network File System (NFS) for applications - shared file storage across VMs

**Business Value:**
- **Application compatibility:** Supports legacy applications requiring shared file systems
- **No management overhead:** Fully managed NFS service, no file server administration
- **High performance:** Enterprise-grade performance for demanding applications
- **Simplified migration:** Easy lift-and-shift for applications needing shared storage
- **Automatic backups:** Built-in data protection for business continuity

**Key Business Features:**
- **High performance:** Up to 16 GB/s throughput, low latency for demanding workloads
- **POSIX compliance:** Standard file system interface, works with existing applications
- **Automatic backups:** Scheduled and on-demand backups for data protection
- **Integration:** Works seamlessly with GKE and Compute Engine
- **Scaling:** Scale capacity independently of performance

**When to Choose Filestore (Business Perspective):**
- Migrating applications that require shared file storage
- Multiple VMs or containers need to access the same files
- Applications requiring NFS protocol support
- High-performance file operations (media rendering, data analytics)

**Business Use Cases:**
- Application migration requiring shared storage (lift-and-shift)
- Content management systems with shared assets
- Media processing and rendering workloads
- Data analytics workloads with shared datasets
- Developer environments requiring shared code/data

**Cost Considerations:**
- Pay for provisioned capacity (minimum 1TB)
- Basic tier: $0.20/GB/month (1TB minimum, up to 60 MB/s per TB)
- High Scale tier: $0.30/GB/month (10TB minimum, up to 120 MB/s per TB)
- Enterprise tier: $0.30/GB/month (1TB minimum, highest performance)
- More expensive than Cloud Storage but provides file system semantics

## Database Services Overview

Choosing the right database is critical for business success. The key question is: **What type of data and what scale?**

**Business Decision Framework:**
- **Relational data, regional scale?** Choose Cloud SQL
- **Relational data, global scale?** Choose Cloud Spanner
- **Document data for mobile/web apps?** Choose Firestore
- **Massive analytical workloads?** Choose BigQuery
- **IoT or time-series data?** Choose Bigtable

**Database Selection Matrix:**
| Requirement | Service | Why |
|-------------|---------|-----|
| Traditional SQL app | Cloud SQL | Easiest migration, lowest cost |
| Global SQL application | Cloud Spanner | Global consistency, unlimited scale |
| Mobile/web app data | Firestore | Real-time sync, offline support |
| Analytics/reporting | BigQuery | Serverless, petabyte-scale |
| IoT/time-series | Bigtable | High throughput, low latency |

## Database Services

### Cloud SQL
**What it is:** Fully managed relational database service - MySQL, PostgreSQL, SQL Server without the operational overhead

**Business Value:**
- **Zero database administration:** No patching, backups, replication management (reduce IT overhead)
- **Cost predictability:** Pay for what you provision, no licensing complexity for MySQL/PostgreSQL
- **Fast migration:** Compatible with on-premises databases, minimal code changes
- **High availability:** Automatic failover, 99.95% SLA reduces business disruption
- **Focus on business logic:** Developers build features, not manage databases

**Supported Engines:**
- **MySQL:** Open-source relational database - no licensing costs, broad ecosystem
- **PostgreSQL:** Advanced open-source database - enterprise features without cost
- **SQL Server:** Microsoft's relational database - familiar to Windows shops, bring-your-own-license or included

**Key Business Features:**
- **Automatic backups:** Point-in-time recovery up to 7 days (protects against data loss)
- **High availability:** Multi-zone deployments with automatic failover (99.95% SLA)
- **Security:** Encryption at rest/transit, IAM integration, private IP (compliance ready)
- **Scaling:** Read replicas for read-heavy workloads, vertical scaling for growth
- **Maintenance:** Automatic updates and patches during maintenance windows (no downtime)
- **Connection pooling:** Efficient connection management reduces resource waste

**When to Choose Cloud SQL (Business Perspective):**
- Migrating existing MySQL, PostgreSQL, or SQL Server databases
- Traditional web and business applications
- Applications requiring ACID transactions and relational data
- Regional applications (single region or nearby regions)
- Teams with SQL expertise, wanting managed operations

**Business Use Cases:**
- E-commerce platforms and shopping carts (transactional integrity)
- Content management systems (WordPress, Drupal)
- ERP and CRM applications (business data with relationships)
- Customer databases and user management
- Inventory management systems

**Cost Considerations:**
- Pay for instance size (CPU/RAM) + storage + network egress
- MySQL/PostgreSQL: No licensing fees (major cost savings vs commercial databases)
- SQL Server: License included or BYOL (bring your own license)
- Shared-core instances for dev/test (start at ~$10/month)
- High availability costs ~2x (worth it for production)
- Read replicas add cost but improve performance

### Cloud Spanner
**What it is:** Globally distributed, strongly consistent relational database - SQL at global scale

**Business Value:**
- **Global business reach:** Serve customers worldwide with low latency from single database
- **No trade-offs:** Get both global scale AND strong consistency (revolutionary capability)
- **Unlimited growth:** Scale horizontally without limits (add capacity as business grows)
- **Mission-critical SLA:** 99.999% availability (5 nines = 5 minutes downtime per year)
- **Future-proof architecture:** Built for global, always-on applications

**Key Business Features:**
- **Global scale:** Horizontal scaling across regions - serve billions of transactions
- **Strong consistency:** ACID transactions globally (no eventual consistency workarounds)
- **SQL interface:** Standard SQL queries (use existing SQL skills)
- **High availability:** 99.999% SLA (five nines) - essentially always available
- **Automatic sharding:** Transparent data distribution (Google handles complexity)
- **No downtime scaling:** Add/remove capacity without maintenance windows

**When to Choose Cloud Spanner (Business Perspective):**
- Global applications serving customers worldwide
- Financial services requiring strong consistency (banking, payments)
- Applications outgrowing regional databases
- Mission-critical systems requiring 99.999% availability
- When you need both SQL and global scale (unique combination)

**Business Use Cases:**
- Global financial services (payments, trading, banking)
- Gaming leaderboards and player data (worldwide players)
- Supply chain management across regions
- Global retail platforms
- SaaS applications with worldwide customers

**Cost Considerations:**
- Premium service with premium pricing (most expensive GCP database)
- Pay for node capacity + storage (minimum 1 node = ~$750/month per region)
- Regional config: 1 region, lower cost, 99.99% SLA
- Multi-region config: 3+ regions, higher cost, 99.999% SLA
- Only choose when global scale and consistency are required
- Consider Cloud SQL first - migrate to Spanner when you outgrow it

### Firestore
**What it is:** NoSQL document database for mobile and web applications - real-time, offline-capable

**Business Value:**
- **Faster app development:** Real-time sync and offline support built-in (reduce development time)
- **Better user experience:** Apps work offline, sync automatically when online
- **Global reach:** Multi-region replication serves users worldwide with low latency
- **Scales automatically:** From zero to millions of users without capacity planning
- **Mobile-first:** Purpose-built for modern mobile and web applications

**Key Business Features:**
- **Real-time synchronization:** Live updates to all connected clients (collaborative features built-in)
- **Offline support:** Local caching and automatic sync when online (works anywhere)
- **Multi-region replication:** Data replicated globally for low-latency access
- **Security rules:** Declarative security at document level (protect user data)
- **ACID transactions:** Strong consistency guarantees when needed
- **Flexible data model:** Document structure adapts as business needs change

**When to Choose Firestore (Business Perspective):**
- Mobile applications requiring offline capability
- Real-time collaborative applications
- Applications with unpredictable, variable traffic
- Rapid prototyping and MVP development
- When you want serverless, zero-ops database

**Business Use Cases:**
- Mobile applications (iOS, Android apps)
- Real-time chat and messaging applications
- Collaborative tools (shared documents, project management)
- Social media platforms (user profiles, feeds, likes)
- Gaming applications (player state, matchmaking)

**Cost Considerations:**
- Pay for document reads, writes, deletes (not storage primarily)
- Generous free tier (50K reads, 20K writes, 20K deletes per day)
- Good for mobile apps with many inactive users
- Can be expensive for write-heavy workloads
- Storage: $0.18/GB/month (relatively expensive for large data)

### Cloud Bigtable
**What it is:** NoSQL wide-column database for large analytical and operational workloads - petabyte-scale, low latency

**Business Value:**
- **Handle massive scale:** Billions of rows, millions of operations per second
- **Consistent performance:** Single-digit millisecond latency at any scale
- **Cost-effective at scale:** Cheaper than traditional databases for large data volumes
- **IoT-ready:** Purpose-built for time-series and high-throughput data
- **Real-time insights:** Process massive data streams for immediate business intelligence

**Key Business Features:**
- **High throughput:** Millions of operations per second (handle any traffic)
- **Low latency:** Single-digit millisecond latency (real-time applications)
- **Petabyte-scale:** Store and process petabytes of data efficiently
- **Integration:** Works with Hadoop, Spark, Dataflow, and HBase APIs
- **Automatic replication:** Multi-cluster replication for global applications

**When to Choose Bigtable (Business Perspective):**
- IoT applications collecting massive sensor data
- Time-series data (financial tick data, monitoring metrics)
- High-throughput operational workloads
- Real-time analytics on large datasets
- When you have consistently large workloads (minimum scale requirements)

**Business Use Cases:**
- Time-series data (stock prices, sensor readings, application metrics)
- IoT applications (connected devices, telemetry)
- Financial services (trading data, fraud detection)
- AdTech and MarTech (user behavior tracking, personalization)
- Real-time analytics and monitoring

**Cost Considerations:**
- Minimum cluster size: 1 node (~$650/month) - not cost-effective for small workloads
- Cost-effective at scale (petabytes of data)
- Pay for node capacity + storage (SSD or HDD)
- Storage is cheap: $0.17/GB/month for SSD
- Only economical for consistently large workloads
- Consider Firestore or Cloud SQL for smaller datasets

### BigQuery (Data Warehouse)
**What it is:** Serverless, petabyte-scale data warehouse - analytics without infrastructure

**Business Value:**
- **Business intelligence without infrastructure:** No servers, no database administration
- **Analyze all your data:** Petabyte-scale - analyze your entire business data in one place
- **Real-time insights:** Stream data and query immediately for timely business decisions
- **Democratize data:** Standard SQL enables business analysts to query data themselves
- **Built-in ML:** Business analysts can build ML models without data science expertise

**Key Business Features:**
- **Serverless:** Zero infrastructure management, automatic scaling (focus on insights, not operations)
- **SQL interface:** Standard SQL queries (use existing skills, broad tool compatibility)
- **Real-time analytics:** Stream data for immediate insights (milliseconds from event to query)
- **BigQuery ML:** Build machine learning models using SQL (democratize ML)
- **Data sharing:** Secure data sharing across organizations (collaborate with partners)
- **Separation of compute and storage:** Query performance independent of data size

**When to Choose BigQuery (Business Perspective):**
- Business intelligence and reporting needs
- Data warehousing without infrastructure management
- Ad-hoc analysis of large datasets
- Real-time dashboards and analytics
- When you want analysts querying data directly (self-service analytics)

**Business Use Cases:**
- Business intelligence and executive dashboards
- Customer analytics and segmentation
- Marketing attribution and campaign analysis
- Log analysis and security monitoring
- Financial reporting and forecasting
- Supply chain analytics

**Cost Considerations:**
- Two pricing models: On-demand or flat-rate (capacity reservations)
- On-demand: $5 per TB queried (pay per query)
- Storage: $0.02/GB/month for active data (first 10GB free)
- Flat-rate: $2,000/month per 100 slots (predictable cost for heavy users)
- Free tier: 1TB queries, 10GB storage per month
- Cost optimization: Partition tables, cluster columns, use appropriate data types

## Networking Services Overview

Networking affects both user experience (performance) and security. Key business considerations: global reach, performance, and cost.

**Business Decision Framework:**
- **Private network isolation?** VPC is foundational
- **Global application?** Cloud Load Balancing for traffic distribution
- **Improve website performance?** Cloud CDN for content caching
- **Connect to on-premises?** Cloud VPN (encrypted) or Cloud Interconnect (dedicated)

## Networking Services

### Virtual Private Cloud (VPC)
**What it is:** Software-defined networking for GCP resources - your private network in the cloud

**Business Value:**
- **Security and isolation:** Private network protects business resources
- **Global infrastructure:** Single network spans all GCP regions (simplifies architecture)
- **Cost savings:** Private Google Access reduces egress costs
- **Compliance:** Network isolation helps meet regulatory requirements
- **Hybrid connectivity:** Securely extend on-premises network to cloud

**Key Business Features:**
- **Global scope:** Single VPC spans all regions (unlike AWS regional VPCs)
- **Firewall rules:** Control traffic to/from instances (security)
- **Private Google Access:** Access Google services without external IPs (reduce egress costs)
- **VPC peering:** Connect VPCs privately (multi-project, multi-organization networking)
- **Shared VPC:** Centralized network management across projects (enterprise governance)

**When to Choose VPC (Business Perspective):**
- Every GCP deployment needs VPC (foundational service)
- Multi-tier applications requiring network segmentation
- Compliance requirements for network isolation
- Hybrid cloud connecting on-premises and cloud
- Multi-project environments needing centralized networking

**Business Use Cases:**
- Secure multi-tier applications (web, app, database tiers)
- Hybrid cloud with on-premises data center connectivity
- Multi-environment deployments (dev, test, prod isolation)
- Compliance-driven architectures requiring network controls
- Multi-project organizations needing centralized networking

**Cost Considerations:**
- VPC itself is free (no charge for the network)
- Pay for resources in VPC (VMs, load balancers, etc.)
- Egress charges when data leaves Google network
- Private Google Access reduces egress costs

### Cloud Load Balancing
**What it is:** Distribute incoming traffic across multiple backend instances - global scale, built-in redundancy

**Business Value:**
- **Global reach with single IP:** Serve users worldwide from one endpoint
- **High availability:** Automatic failover to healthy instances reduces downtime
- **Performance:** Route users to nearest/fastest backend (better user experience)
- **Scalability:** Handle traffic spikes automatically (Black Friday, viral events)
- **Cost optimization:** Distribute load efficiently, auto-scale backends

**Types (Choose Based on Application Needs):**
- **Global HTTP(S):** Web applications - global reach, SSL termination, URL-based routing
- **Global SSL Proxy:** Non-HTTP SSL traffic - global reach for SSL applications
- **Global TCP Proxy:** Non-HTTP TCP traffic - global reach for custom protocols
- **Regional Network:** Regional TCP/UDP - high throughput, preserve source IP
- **Regional Internal:** Internal load balancing - private traffic within VPC

**Key Business Features:**
- **Global reach:** Single anycast IP serves globally (simplify DNS, best performance)
- **Auto-scaling:** Scale backends automatically based on traffic (handle demand spikes)
- **Health checks:** Route traffic only to healthy instances (improve reliability)
- **SSL termination:** Handle SSL/TLS encryption (offload work from backends)
- **Content-based routing:** Route traffic based on URL, headers (support microservices)

**When to Choose Load Balancing (Business Perspective):**
- Applications requiring high availability (minimize downtime)
- Global applications serving users worldwide
- Applications with variable traffic patterns
- Multi-region deployments for disaster recovery
- Microservices needing intelligent traffic routing

**Business Use Cases:**
- Global web applications and e-commerce sites
- API gateways for mobile and web applications
- Multi-region deployments for performance and reliability
- SaaS platforms serving global customers
- Applications requiring zero-downtime deployments (blue-green, canary)

**Cost Considerations:**
- Pay for ingress traffic processed and instance hours
- Global load balancers: ~$25/month + $0.008-$0.012 per GB
- Regional load balancers: ~$18/month + per-GB charges
- Premium tier networking (default): Better performance, higher cost
- Standard tier: Lower cost, no global load balancing

### Cloud CDN
**What it is:** Global content delivery network - cache content close to users for fast delivery

**Business Value:**
- **Improved user experience:** Faster page loads and content delivery (higher conversion rates)
- **Reduced costs:** Cache hits reduce backend load and egress charges
- **Global reach:** 200+ edge locations worldwide serve content locally
- **Higher capacity:** Offload traffic from origin servers (handle more users)
- **Better SEO:** Page speed affects search rankings

**Key Business Features:**
- **Global edge locations:** 200+ locations cache content close to users
- **Integration:** Works seamlessly with Cloud Load Balancing
- **Cache control:** Programmatic cache invalidation and management
- **Security:** DDoS protection and SSL support included
- **Analytics:** Detailed logs and metrics on cache performance

**When to Choose Cloud CDN (Business Perspective):**
- Websites with global audience (improve international performance)
- Media-heavy sites (images, videos consume bandwidth)
- High-traffic websites (reduce origin server load)
- E-commerce sites (faster pages = higher conversions)
- APIs serving static or cacheable content

**Business Use Cases:**
- Website acceleration (faster page loads worldwide)
- Video streaming and media delivery
- Software and file distribution (downloads, updates)
- E-commerce sites (product images, static content)
- Mobile app backends (reduce latency, data costs)

**Cost Considerations:**
- Pay for cache egress and HTTP/HTTPS requests
- Cache egress cheaper than origin egress ($0.04-$0.08/GB vs $0.08-$0.23/GB)
- Cache hit ratio determines savings (80%+ hit ratio = significant savings)
- Typical savings: 50-90% reduction in egress costs
- Also reduces origin infrastructure costs (less load)

### Cloud Interconnect and VPN
**What it is:** Hybrid connectivity options - connect on-premises infrastructure to GCP

**Business Value:**
- **Hybrid cloud:** Leverage existing on-premises investments while moving to cloud
- **Data sovereignty:** Keep sensitive data on-premises while using cloud for other workloads
- **Migration path:** Gradual migration with connectivity to legacy systems
- **Lower costs:** Reduce egress charges (Interconnect) for large data transfers
- **Better performance:** Lower latency for hybrid applications

**Cloud VPN (IPsec over Internet):**
- **Site-to-site VPN:** Connect on-premises network to GCP VPC
- **IPsec encryption:** Secure tunnel over public internet
- **High availability:** 99.9% SLA with redundant gateways
- **Cost-effective:** ~$0.05/hour per tunnel + egress charges
- **Quick setup:** Days to deploy, not months

**Cloud Interconnect (Dedicated Connection):**
- **Dedicated Interconnect:** Direct physical connection to Google (10/100 Gbps)
- **Partner Interconnect:** Connection through service provider (50 Mbps - 50 Gbps)
- **Higher bandwidth:** Up to 200 Gbps (multiple connections)
- **Lower latency:** Direct connection to Google network (no internet hops)
- **Reduced egress costs:** Egress discounts for large data transfers

**When to Choose Each (Business Perspective):**
- **Cloud VPN:** Small data transfers, quick setup, budget-conscious, test/dev
- **Dedicated Interconnect:** Large data transfers (10+ Gbps), lowest latency, predictable performance
- **Partner Interconnect:** Medium bandwidth needs, don't have own facility near Google

**Business Use Cases:**
- Hybrid cloud architecture (workloads split between on-premises and cloud)
- Disaster recovery (replicate data to/from cloud)
- Gradual cloud migration (maintain connectivity during transition)
- Burst to cloud (handle peak loads in cloud, regular workloads on-premises)
- Access on-premises data from cloud applications

**Cost Considerations:**
- **Cloud VPN:** $0.05/hour per tunnel (~$36/month) + standard egress
- **Dedicated Interconnect:** Port fee ($1,700-$27,000/month) + reduced egress
- **Partner Interconnect:** Service provider fee + Google fee + reduced egress
- **Egress savings:** Interconnect can reduce egress from $0.08/GB to $0.02/GB
- **Break-even:** Calculate based on data transfer volume (Interconnect better for >10TB/month)

## AI and Machine Learning Services Overview

AI/ML enables business innovation without requiring deep technical expertise. The key question: **Build custom models or use pre-trained?**

**Business Decision Framework:**
- **Standard AI tasks (vision, language, speech)?** Use Pre-trained APIs (fastest, cheapest)
- **Custom ML models needed?** Use Agent Platform AutoML (no ML expertise required)
- **Advanced custom models?** Use Agent Platform Managed Training (custom training) (ML expertise required)
- **SQL-based ML for analysts?** Use BigQuery ML (democratize ML)

## AI and Machine Learning Services

### Agent Platform
**What it is:** Unified ML platform for building, deploying, and scaling ML models - Google's comprehensive ML solution

**Business Value:**
- **Competitive advantage:** Build custom AI capabilities unique to your business
- **Democratize ML:** AutoML enables business analysts to build models without data scientists
- **Faster time-to-value:** Pre-built components and workflows accelerate ML projects
- **MLOps built-in:** Production-grade model deployment and management
- **Reduce ML complexity:** Unified platform eliminates tool sprawl and integration challenges

**Key Business Features:**
- **AutoML:** Build custom models without coding (business analysts can use)
- **Custom training:** Train models with your own code (for data scientists)
- **Model deployment:** Serve models with managed endpoints (no infrastructure management)
- **MLOps:** End-to-end workflow management (from training to production)
- **Explainable AI:** Understand model predictions (regulatory compliance, trust)

**When to Choose Agent Platform (Business Perspective):**
- Pre-trained APIs don't fit your specific use case
- Need custom models trained on your proprietary data
- Building competitive advantage through unique ML capabilities
- Require explainability for regulatory or business reasons
- Have data science team or want to develop ML capabilities

**Business Use Cases:**
- Custom computer vision (product defect detection, medical imaging)
- Personalized recommendations unique to your business
- Fraud detection tailored to your transaction patterns
- Custom natural language models for industry-specific terminology
- Predictive maintenance based on your equipment data

**Cost Considerations:**
- Pay for training compute, prediction compute, and storage
- AutoML: Higher cost but no data science team needed
- Custom training: Lower cost but requires ML expertise
- Prediction costs: Batch predictions cheaper than real-time
- Consider total cost: service cost + staff cost

### Pre-trained AI APIs (Quick Wins for Business)
**What they are:** Ready-to-use AI services requiring no ML expertise - call an API, get results

**Business Value:**
- **Immediate ROI:** Deploy AI capabilities in days, not months
- **No ML expertise required:** Developers use simple APIs
- **Google-quality AI:** Leverage Google's AI research and infrastructure
- **Pay-per-use:** No upfront costs, scale from zero
- **Focus on business problems:** Build solutions, not train models

### Vision AI
**What it is:** Image and video analysis through simple API calls

**Key Business Features:**
- **Image analysis:** Detect objects, faces, text, inappropriate content in images
- **Video analysis:** Analyze video content, detect scene changes, extract metadata
- **Optical Character Recognition (OCR):** Extract text from images and documents
- **Product Search:** Visual search for retail applications

**Business Use Cases:**
- Content moderation (filter inappropriate user-generated content)
- Retail product search (customers upload photos to find products)
- Accessibility (generate image descriptions for visually impaired)
- Quality control (detect defects in manufacturing)
- Insurance claims processing (analyze damage photos)

**Cost Considerations:**
- Pay per image analyzed (first 1,000 images/month free)
- $1.50 per 1,000 images for most features
- Custom models via AutoML Vision more expensive
- Much cheaper than building own computer vision system

### Natural Language AI
**What it is:** Text analysis and translation through API calls

**Key Business Features:**
- **Sentiment analysis:** Determine positive, negative, neutral sentiment in text
- **Entity extraction:** Identify people, organizations, locations, dates in text
- **Content classification:** Categorize content by topic
- **Translation API:** Translate text between 100+ languages

**Business Use Cases:**
- Customer feedback analysis (analyze support tickets, reviews, surveys)
- Content localization (translate website, apps, documents)
- Email routing (automatically categorize and route customer emails)
- Social media monitoring (track brand sentiment)
- Compliance monitoring (flag sensitive content)

**Cost Considerations:**
- Sentiment analysis: $1 per 1,000 text records
- Entity extraction: $1 per 1,000 text records
- Translation: $20 per million characters
- Very cost-effective compared to manual analysis

### Speech-to-Text and Text-to-Speech
**What they are:** Convert between audio and text through API calls

**Key Business Features:**
- **Speech-to-Text:** Convert audio to text with 125+ language support
- **Text-to-Speech:** Convert text to natural-sounding speech
- **Real-time streaming:** Process audio streams in real-time
- **Speaker diarization:** Identify different speakers in conversation

**Business Use Cases:**
- Call center analytics (transcribe and analyze customer calls)
- Voice assistants and IVR systems (interactive voice response)
- Accessibility (closed captions, screen readers)
- Meeting transcription and note-taking
- Voice-controlled applications

**Cost Considerations:**
- Speech-to-Text: $0.006 per 15 seconds of audio
- Text-to-Speech: $4-$16 per million characters
- Significant savings compared to manual transcription
- Enables previously impossible use cases (analyze 100% of calls)

### Document AI
**What it is:** Extract structured data from documents through AI

**Key Business Features:**
- **Document parsing:** Extract data from invoices, receipts, contracts
- **Form processing:** Process structured and unstructured forms
- **Custom extractors:** Build custom parsers for your document types
- **Pre-trained parsers:** Ready-to-use for common document types

**Business Use Cases:**
- Invoice and receipt processing (accounts payable automation)
- Contract analysis and data extraction
- ID document verification (KYC processes)
- Medical records digitization
- Loan application processing

**Cost Considerations:**
- Pay per page processed
- Pre-trained parsers: $0.01-$0.10 per page depending on type
- Significant labor savings (reduce manual data entry)
- Faster processing = better customer experience

### BigQuery ML
**What it is:** Build and deploy ML models using SQL queries in BigQuery

**Business Value:**
- **Democratize ML:** Business analysts can build models using SQL (no Python/coding)
- **Data stays in place:** No data movement (faster, more secure)
- **Familiar tools:** Use existing BI tools and SQL knowledge
- **Serverless:** No infrastructure to manage
- **Integrated workflow:** From data to insights to predictions in one platform

**Business Use Cases:**
- Customer churn prediction (identify at-risk customers)
- Sales forecasting (predict future revenue)
- Product recommendations (cross-sell, upsell opportunities)
- Demand forecasting (inventory optimization)
- Customer lifetime value prediction

**Cost Considerations:**
- Pay for BigQuery query processing ($5 per TB)
- Model training and prediction queries charged like normal queries
- Much cheaper than separate ML platform (no data movement, no separate infrastructure)
- Enables business analysts to build models (no data science team cost)

## Data Analytics Services (Supporting Business Intelligence)

### Pub/Sub
**What it is:** Messaging service for event-driven systems and real-time data pipelines

**Business Value:**
- **Real-time insights:** Process business events as they happen
- **Reliable messaging:** Never lose important business events (guaranteed delivery)
- **Scalability:** Handle millions of messages per second
- **Decouple systems:** Connect services without tight integration
- **Foundation for streaming:** Enable real-time analytics and processing

**Business Use Cases:**
- Real-time data ingestion for analytics
- Event-driven microservices architecture
- IoT data collection and processing
- Streaming data to BigQuery for real-time dashboards
- Order processing and notification systems

### Dataflow
**What it is:** Fully managed stream and batch data processing service

**Business Value:**
- **Real-time and batch processing:** One service for both use cases
- **Serverless:** No infrastructure management
- **Auto-scaling:** Handle variable data volumes automatically
- **Unified programming model:** Apache Beam open standard (avoid lock-in)

**Business Use Cases:**
- Real-time ETL (extract, transform, load) pipelines
- Stream processing for real-time analytics
- Batch data processing for reporting
- Data enrichment and cleansing
- Real-time fraud detection

## Operations and Monitoring (Observability)

**Business Value of Observability:**
- **Reduce downtime:** Detect and fix issues before customers notice
- **Faster troubleshooting:** Find root cause quickly (reduce MTTR)
- **Performance optimization:** Identify bottlenecks and inefficiencies
- **Cost optimization:** Identify waste and unused resources
- **SLA compliance:** Prove you're meeting service level agreements

### Cloud Monitoring
**What it is:** Infrastructure and application monitoring service - visibility into your systems

**Key Business Features:**
- **Metrics collection:** System and custom business metrics
- **Alerting:** Proactive notifications prevent downtime
- **Dashboards:** Visual displays for stakeholders and operations teams
- **Uptime monitoring:** Website and API availability tracking (SLA reporting)
- **Integration:** Works with third-party tools (ServiceNow, PagerDuty)

**Business Value:**
- Early problem detection reduces customer impact
- SLA tracking and reporting for contracts
- Capacity planning through trend analysis
- Cost optimization by identifying unused resources

### Cloud Logging
**What it is:** Centralized logging service for applications and infrastructure - audit trail and troubleshooting

**Key Business Features:**
- **Log ingestion:** Collect logs from all sources (applications, infrastructure, audit)
- **Search and filter:** Query logs for troubleshooting and compliance
- **Export:** Send logs to BigQuery for analysis, Cloud Storage for archival
- **Retention:** Configurable policies for compliance requirements

**Business Value:**
- Compliance and audit requirements (maintain audit trail)
- Security investigation and forensics
- Troubleshooting and root cause analysis
- Business intelligence (analyze user behavior from logs)

### Cloud Trace
**What it is:** Distributed tracing system for application performance analysis

**Business Value:**
- Improve user experience by identifying slow operations
- Optimize costs by finding inefficient operations
- Troubleshoot performance issues in complex microservices
- Capacity planning based on actual usage patterns

### Error Reporting
**What it is:** Real-time error monitoring and alerting - know about errors before customers complain

**Business Value:**
- Proactive error detection improves customer satisfaction
- Prioritize fixes based on error frequency and impact
- Faster time to resolution with detailed error information
- Reduce support costs by fixing issues proactively

## Business Scenarios: Choosing the Right Services

### Scenario 1: E-commerce Startup (Cost-Conscious, Fast Time-to-Market)
**Requirements:** Build online store quickly, minimal operational overhead, unpredictable traffic

**Recommended Services:**
- **Compute:** App Engine (auto-scaling, no infrastructure management)
- **Database:** Firestore (serverless, real-time sync for cart, product catalog)
- **Storage:** Cloud Storage (product images, Standard class)
- **CDN:** Cloud CDN (fast image delivery worldwide)
- **Analytics:** BigQuery (analyze sales data, customer behavior)
- **AI:** Vision AI for product search, Recommendations AI for cross-selling

**Why:** Serverless services minimize operational overhead and cost. Pay only for what you use. Auto-scaling handles traffic spikes during sales events.

### Scenario 2: Global Enterprise (Multi-Region, High Availability)
**Requirements:** Global customer base, 99.99%+ uptime, strong consistency, compliance

**Recommended Services:**
- **Compute:** GKE with multi-region clusters (portability, high availability)
- **Database:** Cloud Spanner (global consistency, 99.999% SLA)
- **Storage:** Cloud Storage multi-region buckets
- **Network:** Global Load Balancing, Cloud CDN, Cloud Armor (security)
- **Analytics:** BigQuery (global analytics)
- **Operations:** Full observability stack (Monitoring, Logging, Trace)

**Why:** Global reach with consistent low latency. High availability architecture meets enterprise SLAs. Compliance through audit logging and monitoring.

### Scenario 3: Data Analytics Company (Process Massive Datasets)
**Requirements:** Analyze petabytes of data, real-time and batch processing, business intelligence

**Recommended Services:**
- **Data Warehouse:** BigQuery (serverless, petabyte-scale)
- **Data Lake:** Cloud Storage (Nearline/Coldline for historical data)
- **Real-time Processing:** Pub/Sub + Dataflow (streaming data pipelines)
- **Batch Processing:** Dataflow (batch ETL jobs)
- **ML:** BigQuery ML (SQL-based models for analysts)
- **BI Tools:** Looker, Data Studio (visualization)

**Why:** Serverless architecture eliminates infrastructure management. Separation of compute and storage optimizes costs. Analysts can work independently with SQL.

### Scenario 4: Healthcare Provider (Compliance, Security, Hybrid Cloud)
**Requirements:** HIPAA compliance, data sovereignty, integrate with on-premises systems

**Recommended Services:**
- **Compute:** Compute Engine in private VPC (full control for compliance)
- **Database:** Cloud SQL with private IP (regional, compliance-friendly)
- **Storage:** Cloud Storage with customer-managed encryption keys
- **Networking:** Cloud VPN or Interconnect (secure hybrid connectivity)
- **AI:** Healthcare API (HIPAA-compliant document processing)
- **Operations:** Cloud Logging for audit trails, VPC Service Controls

**Why:** Full control and visibility for compliance. Hybrid connectivity maintains integration with on-premises systems. Healthcare-specific APIs designed for regulated environments.

### Scenario 5: Mobile Gaming Company (Global Players, Real-Time)
**Requirements:** Global mobile game, real-time leaderboards, player data sync, scale to millions

**Recommended Services:**
- **Backend:** Cloud Run (containerized game services, auto-scaling)
- **Database:** Firestore (real-time sync, offline support for mobile)
- **Leaderboards:** Cloud Spanner (global consistency for leaderboard integrity)
- **Player Data:** Cloud Storage (game assets, saved games)
- **Analytics:** BigQuery (player behavior analysis, game metrics)
- **AI:** Recommendations AI (personalized offers, game suggestions)

**Why:** Real-time sync keeps all players in sync. Global infrastructure provides low latency worldwide. Auto-scaling handles player spikes during events.

### Scenario 6: Financial Services (Regulated, High Security)
**Requirements:** Financial transactions, regulatory compliance, audit trails, strong consistency

**Recommended Services:**
- **Compute:** GKE with binary authorization (control what runs)
- **Database:** Cloud Spanner (ACID transactions globally, audit logging)
- **Storage:** Cloud Storage with retention policies (compliance)
- **Security:** VPC Service Controls, Cloud Armor, Security Command Center
- **Analytics:** BigQuery (fraud detection, regulatory reporting)
- **AI:** Fraud Detection AI, Explainable AI (regulatory compliance)

**Why:** Strong consistency essential for financial accuracy. Comprehensive audit logging for compliance. Advanced security controls protect sensitive data.

### Scenario 7: IoT Manufacturing (High Volume, Time-Series Data)
**Requirements:** Millions of sensors, time-series data, predictive maintenance, real-time monitoring

**Recommended Services:**
- **Data Ingestion:** Pub/Sub (collect sensor data at scale)
- **Data Processing:** Dataflow (real-time processing for alerts)
- **Database:** Bigtable (time-series data, high throughput)
- **Analytics:** BigQuery (historical analysis, reporting)
- **ML:** Agent Platform (predictive maintenance models)
- **Visualization:** Data Studio (real-time dashboards for operations)

**Why:** Pub/Sub handles millions of messages per second. Bigtable optimized for time-series data. Real-time processing enables immediate alerts for anomalies.

### Scenario 8: Media Streaming Platform (High Bandwidth, Global Audience)
**Requirements:** Video streaming worldwide, high bandwidth, low latency, cost efficiency

**Recommended Services:**
- **Storage:** Cloud Storage (video files, lifecycle management for old content)
- **CDN:** Cloud CDN (cache video close to users globally)
- **Compute:** Cloud Run (transcode videos on-demand)
- **Networking:** Premium tier for consistent performance
- **Analytics:** BigQuery (viewer analytics, content performance)
- **AI:** Video Intelligence API (content moderation, metadata extraction); deprecated 2026-09-14 and shutting down 2027-09-14, so new builds use Gemini models for video understanding

**Why:** Cloud CDN reduces origin load and egress costs. Cloud Storage lifecycle management archives old content. Global infrastructure serves viewers worldwide with low latency.

## Service Selection Decision Framework

### Quick Selection Guide

**For Compute:**
1. **Lift-and-shift migration?** Compute Engine
2. **Zero infrastructure management?** App Engine
3. **Containers + simplicity?** Cloud Run
4. **Containers + complex orchestration?** GKE
5. **Event-driven, short tasks?** Cloud Functions

**For Storage:**
1. **Unstructured data (files, images)?** Cloud Storage (choose class by access frequency)
2. **VM disk storage?** Persistent Disks
3. **Shared file storage?** Filestore

**For Database:**
1. **Relational, regional?** Cloud SQL
2. **Relational, global?** Cloud Spanner
3. **Document, mobile/web?** Firestore
4. **Analytics/data warehouse?** BigQuery
5. **Time-series, IoT?** Bigtable

**For AI/ML:**
1. **Standard AI tasks (vision, language)?** Pre-trained APIs
2. **Custom models, no ML expertise?** Agent Platform AutoML
3. **Advanced custom models?** Agent Platform Managed Training (custom training)
4. **SQL-based ML for analysts?** BigQuery ML

## Cloud Digital Leader Exam Tips

### Service Questions Patterns

**Pattern 1: "Choose the right service"**
- Focus on business requirements, not technical implementation
- Key factors: cost, operational overhead, time-to-market, scale
- Remember: serverless = lower operational overhead = faster time-to-market

**Pattern 2: "Cost optimization"**
- Serverless services often more cost-effective for variable workloads
- Storage classes: choose based on access frequency
- Preemptible/Spot instances: 80% savings for fault-tolerant workloads
- Sustained use and committed use discounts for predictable workloads

**Pattern 3: "Global scale requirements"**
- Cloud Spanner for global SQL
- Global Load Balancing for global web apps
- Cloud CDN for global content delivery
- Multi-region Cloud Storage for global data access

**Pattern 4: "Compliance and security"**
- Audit logging available on all services
- Private IP options for databases
- Customer-managed encryption keys available
- VPC Service Controls for additional security perimeter

**Pattern 5: "Migration scenarios"**
- Lift-and-shift: Compute Engine
- Replatform: Cloud SQL, managed services
- Refactor: Serverless (App Engine, Cloud Run, Cloud Functions)
- Database migration: Database Migration Service

### Key Exam Concepts

**Compute Services:**
- Understand the trade-off: control vs. operational overhead
- IaaS (Compute Engine) = most control, most operational work
- PaaS (App Engine) = less control, less operational work
- Serverless (Cloud Run, Cloud Functions) = least control, zero operational work
- Know when to choose each based on business needs

**Storage Services:**
- Storage class selection is critical for cost optimization
- Understand minimum storage duration for Nearline, Coldline, Archive
- Cloud Storage for unstructured data (objects)
- Persistent Disks for VM storage (block storage)
- Filestore for shared file systems (NFS)

**Database Services:**
- Match database type to use case (relational, document, time-series, analytics)
- Cloud SQL: regional relational (start here for most use cases)
- Cloud Spanner: global relational (premium service, higher cost)
- Firestore: document database for mobile/web (real-time sync)
- BigQuery: analytics and data warehouse (serverless, petabyte-scale)
- Bigtable: time-series and IoT (high throughput, requires scale)

**Networking Services:**
- VPC is foundational (every deployment uses VPC)
- Global Load Balancing enables global applications with single IP
- Cloud CDN reduces costs and improves performance
- Cloud VPN for quick hybrid connectivity
- Cloud Interconnect for high-bandwidth hybrid connectivity

**AI/ML Services:**
- Pre-trained APIs: fastest path to AI capabilities (no ML expertise needed)
- Agent Platform AutoML: custom models without ML expertise
- BigQuery ML: democratize ML for SQL users
- Focus on business value, not technical details

**Data Analytics:**
- BigQuery is the central service (data warehouse + analytics + ML)
- Pub/Sub for real-time data ingestion
- Dataflow for data processing (ETL)
- Know when to use real-time vs. batch processing

### Common Exam Traps

1. **Don't over-engineer:** Choose simplest service that meets requirements
2. **Serverless usually wins for cost:** Unless you have consistent 24/7 load
3. **Global doesn't always mean Cloud Spanner:** Consider multi-region Cloud SQL
4. **Not everything needs Kubernetes:** Cloud Run often simpler choice
5. **Pre-trained APIs before custom ML:** Don't build what already exists
6. **Consider total cost:** Include operational overhead, not just service cost
7. **Time-to-market matters:** Managed services accelerate delivery

### Key Success Factors for Exam

- **Think like a business leader:** Focus on outcomes, not technical details
- **Cost optimization:** Always consider cost implications
- **Operational overhead:** Serverless reduces operational complexity
- **Time-to-market:** Managed services enable faster delivery
- **Scalability:** Cloud services scale automatically
- **Global reach:** Google's global infrastructure is a key advantage
- **Business value:** Always connect technical capabilities to business outcomes

### Remember: Cloud Digital Leader is Business-Focused

The exam tests business understanding of cloud services:
- WHAT services do for business
- WHY choose one service over another
- WHEN to use each service based on business requirements
- Business outcomes (cost, time-to-market, scalability, etc.)

NOT testing:
- HOW to implement technically
- Command-line syntax or console navigation
- Deep technical architecture details
- Coding or scripting