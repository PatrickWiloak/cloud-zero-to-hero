# Google Cloud Professional Cloud Architect Practice Questions

109 scenario-based questions: the original 40 weighted by exam domain, 26 on the current case studies, AI and operations, and 43 more on the four case studies.

## Exam Domain Breakdown
Weights are from the current exam guide (checked 2026-10-14). Questions 1-40 follow the earlier layout and are grouped under the six sections, and questions 41-66 cover the four current case studies, AI, and operations topics across sections.

| Section | Weight | Questions |
|--------|--------|-----------|
| Design and plan a cloud solution architecture | ~25% | 1-10 |
| Manage and provision cloud solution infrastructure | ~17.5% | 11-16 |
| Design for security and compliance | ~17.5% | 17-23 |
| Analyze and optimize technical and business processes | ~15% | 24-30 |
| Manage implementation | ~12.5% | 31-34 |
| Ensure solution and operations excellence | ~12.5% | 35-40 |
| Case studies, AI and operations (mixed) | - | 41-66 |
| Case studies set 2 (Altostrat, Cymbal, EHR, KnightMotives) | 20-30% of the exam | 67-109 |

> **Cert page:** [exams/gcp/cloud-architect/](../../exams/gcp/cloud-architect/)

---

## Domain 1: Design and Plan a Cloud Solution Architecture (Questions 1-10)

### Question 1
**Scenario:** A global e-commerce company needs to design a solution that provides consistent low latency for users worldwide. Their application requires a relational database that supports strong consistency across regions and automatic failover. Which database solution should they choose?

A. Cloud Spanner with multi-region configuration
B. Cloud Firestore in multi-region mode, a NoSQL document database with strong consistency but no relational schema or SQL joins
C. Cloud SQL with cross-region read replicas and automatic failover
D. BigQuery with regional datasets

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Cloud Spanner provides a globally distributed, strongly consistent relational database with automatic failover. It supports horizontal scaling and maintains strong consistency across regions using TrueTime. Cloud SQL read replicas (C) are asynchronous and don't provide strong consistency across regions. Firestore (B) is NoSQL. BigQuery (D) is for analytics, not transactional workloads.

**Key Concept:** [Cloud Spanner](https://docs.cloud.google.com/spanner/docs)
</details>

### Question 2
**Scenario:** A media company needs to process video uploads. Videos should be transcoded to multiple formats, thumbnails should be generated, and metadata should be stored. The workload is unpredictable with peaks during events. What architecture should they design?

A. Single large Compute Engine instance
B. App Engine standard environment, with one service that handles uploads, transcoding, and thumbnails for all videos
C. Event-driven design: Cloud Storage triggers, Cloud Functions or Cloud Run, and Firestore for metadata
D. VM instances in a managed instance group with manual scaling, resized ahead of each expected event to cover the peak load

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Event-driven architecture handles variable workloads efficiently. Cloud Storage triggers invoke Cloud Functions or Cloud Run when videos are uploaded. Transcoding can use Cloud Run Jobs or Batch for long-running tasks. Firestore stores metadata. Scales to zero when idle and handles peaks automatically. Manual scaling (D) doesn't handle spikes well. Single instance (A) is a bottleneck. App Engine (B) isn't ideal for video processing.

**Key Concept:** [Event-Driven Architecture](https://docs.cloud.google.com/eventarc/docs/overview)
</details>

### Question 3
**Scenario:** A company wants to migrate their monolithic application to GCP. They want to minimize changes initially but position for future modernization. What migration strategy should they use?

A. Immediately containerize everything and deploy it to GKE, splitting the monolith into services before any workload moves
B. Rewrite the application from scratch as microservices on Cloud Run before moving any workload to GCP
C. Lift and shift to Compute Engine, then incrementally modernize using Strangler Fig pattern
D. Use Cloud Functions for the entire application, wrapping each existing module in its own function

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Lift and shift to Compute Engine minimizes initial changes while establishing GCP presence. The Strangler Fig pattern allows incremental modernization - extracting microservices over time while the monolith remains functional. Rewriting (B) is risky and time-consuming. Immediate containerization (A) requires significant changes. Functions (D) aren't suitable for monoliths.

**Key Concept:** [Application Modernization](https://cloud.google.com/solutions/application-modernization)
</details>

### Question 4
**Scenario:** A healthcare company needs to store and analyze patient data. Data must be encrypted, access must be audited, and the solution must comply with HIPAA. They need to run complex analytics queries. What storage and analytics solution should they use?

A. Cloud Bigtable for analytics, with column-level encryption in the application and Cloud Audit Logs on admin activity
B. BigQuery with customer-managed encryption keys (CMEK), IAM, and Cloud Audit Logs
C. Compute Engine with local storage
D. Cloud Storage with default encryption

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** BigQuery provides enterprise data warehouse capabilities for complex analytics. CMEK enables customer-controlled encryption. IAM provides granular access control. Cloud Audit Logs track all data access for compliance. BigQuery can be configured for HIPAA compliance. Default encryption (D) doesn't provide customer control. Bigtable (A) is for operational workloads, not complex analytics.

**Key Concept:** [BigQuery Security](https://docs.cloud.google.com/bigquery/docs/data-governance)
</details>

### Question 5
**Scenario:** A company has a high-traffic website with static content (images, CSS, JS) and dynamic API calls. They want to optimize performance and reduce origin server load. What architecture should they implement?

A. Single Compute Engine instance for all traffic
B. Cloud Storage for static content without a CDN, and a managed instance group behind a load balancer for the API calls
C. Cloud CDN for static content, Cloud Load Balancing with Cloud Run backend for dynamic APIs
D. All content, static and dynamic, served from Cloud Functions behind a single HTTPS endpoint with no caching layer

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Cloud CDN caches static content at edge locations worldwide, reducing latency and origin load. Cloud Load Balancing distributes API traffic. Cloud Run provides auto-scaling container-based backend for APIs. This separation optimizes each content type. Single instance (A) doesn't scale. Storage without CDN (B) lacks edge caching. Functions for everything (D) is expensive for static content.

**Key Concept:** [Cloud CDN](https://cloud.google.com/cdn/docs/overview)
</details>

### Question 6
**Scenario:** A startup is building a real-time multiplayer game. They need sub-100ms latency for game state updates, persistence for player data, and the ability to handle millions of concurrent connections. What architecture should they design?

A. Single VM with in-memory data
B. Cloud Memorystore (Redis) for game state, Cloud Firestore for player data, and Cloud Run with WebSockets or Agones on GKE
C. BigQuery for real-time updates, streaming each game-state change into tables and reading them back per player
D. Cloud SQL for all data

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Memorystore (Redis) provides sub-millisecond latency for game state. Firestore offers real-time sync and automatic scaling for player data. Cloud Run or Agones (game server management on GKE) handles WebSocket connections with auto-scaling. Cloud SQL (D) has higher latency. BigQuery (C) is for analytics. Single VM (A) doesn't scale.

**Key Concept:** [Game Architecture](https://cloud.google.com/solutions/games)
</details>

### Question 7
**Scenario:** A financial services company needs to process streaming transaction data, detect fraud in real-time, and store data for batch analytics. What architecture should they implement?

A. Pub/Sub for ingestion, Dataflow for stream processing and fraud detection, BigQuery for storage and analytics
B. Batch processing only
C. Direct writes to BigQuery from the payment application, with scheduled queries run every few minutes to flag fraud
D. Cloud SQL for all processing

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Pub/Sub provides durable, scalable message ingestion. Dataflow processes streams in real-time with exactly-once semantics - ideal for fraud detection logic. BigQuery stores processed data for batch analytics and reporting. This is the standard streaming architecture on GCP. Batch only (B) has latency. Cloud SQL (D) doesn't handle streaming. Direct BigQuery writes (C) add latency and don't allow real-time processing.

**Key Concept:** [Stream Analytics Architecture](https://cloud.google.com/solutions/stream-analytics)
</details>

### Question 8
**Scenario:** A company has development, staging, and production environments. They want environment isolation, consistent deployments, and the ability to share common resources (like container images). How should they structure their GCP organization?

A. Single project for all environments
B. Separate dev, staging, and prod projects plus a shared services project, grouped in folders
C. Different regions for each environment, all kept inside a single shared project in the organization
D. Separate GCP accounts for each environment, with a copy of the container images pushed into each one by hand

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Separate projects provide resource isolation, IAM boundaries, and billing separation. A shared services project hosts common resources like Container Registry/Artifact Registry. Folders organize projects under the organization with inherited policies. Single project (A) lacks isolation. Separate accounts (D) complicate management. Regions (C) are for geographic distribution.

**Key Concept:** [Resource Hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)
</details>

### Question 9
**Scenario:** A machine learning team needs to train models on large datasets. Training jobs run for hours and require GPUs. They want to minimize cost while maintaining performance. What compute solution should they use?

A. Persistent GPU VMs running continuously on on-demand pricing, so training jobs never wait for capacity
B. Agent Platform Managed Training (formerly Vertex AI Training) with preemptible/spot VMs, or GKE with spot node pools
C. Cloud Functions for ML training
D. Standard VMs without GPUs

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Agent Platform Managed Training manages ML jobs with automatic infrastructure provisioning. Preemptible/spot VMs cost up to 91% less than regular VMs. Training jobs can checkpoint and resume if preempted. GKE with spot node pools provides similar benefits for custom training. Persistent VMs (A) waste money when not training. Functions (C) have time limits and no GPUs. Non-GPU VMs (D) are slower.

**Key Concept:** [Agent Platform Managed Training](https://cloud.google.com/vertex-ai/docs/training/overview)
</details>

## Domain 2: Manage and Provision Cloud Solution Infrastructure (Questions 11-16)

### Question 10
**Scenario:** A company wants to implement a data lake on GCP. They have structured data from databases, semi-structured logs, and unstructured documents. All data should be queryable and governed. What architecture should they implement?

A. Cloud SQL for all data types, with documents and logs loaded into relational tables and indexed
B. Cloud Storage lake, BigQuery analytics, Data Catalog governance, and Dataproc processing
C. Separate systems for each data type, each with its own storage, tooling, and access controls to maintain
D. BigQuery only, loading every structured, log, and document file into tables and governing them with dataset IAM

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Cloud Storage provides cost-effective storage for all data types (data lake). BigQuery queries data in Cloud Storage directly (external tables) and stores processed data. Data Catalog provides metadata management and data governance. Dataproc runs Spark/Hadoop for complex processing. Cloud SQL (A) isn't a data lake. Separate systems (C) create silos. BigQuery only (D) is expensive for raw storage.

**Key Concept:** [Data Lake Architecture](https://cloud.google.com/architecture/build-a-data-lake-on-gcp)
</details>

### Question 11
**Scenario:** A company needs to deploy consistent infrastructure across development, staging, and production environments. Changes should be reviewed before applying, and infrastructure state should be tracked. What approach should they use?

A. Terraform with remote state in Cloud Storage, infrastructure as code in Git with Cloud Build
B. Manual console deployment
C. Scripts without version control, run by hand from an administrator's laptop against each environment
D. Deployment Manager only, with templates kept in the console and previews reviewed by the team before each update

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Terraform provides infrastructure as code with state management. Remote state in Cloud Storage enables team collaboration. Git provides version control and code review. Cloud Build automates deployment with PR-based workflows. Manual deployment (B) causes drift. Deployment Manager (D) is GCP-only and less feature-rich. Scripts without VCS (C) lack reproducibility.

**Key Concept:** [Terraform on GCP](https://cloud.google.com/docs/terraform)
</details>

### Question 12
**Scenario:** A team needs to deploy containers to GCP without managing Kubernetes clusters. They need auto-scaling, HTTPS endpoints, and integration with Cloud SQL. What service should they use?

A. Compute Engine with Docker
B. Cloud Run with Cloud SQL connector
C. Cloud Functions
D. GKE Standard with node auto-provisioning, which scales automatically but leaves the team to upgrade and manage the cluster

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Cloud Run is serverless containers - no cluster management. It auto-scales to zero, provides HTTPS endpoints automatically, and has native Cloud SQL connector support for secure database connections. CE with Docker (A) requires VM management. GKE Standard (D) still leaves the team operating a cluster. Functions (C) aren't containers.

**Key Concept:** [Cloud Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run)
</details>

### Question 13
**Scenario:** A company's application requires instances in multiple zones for high availability. If one zone fails, traffic should automatically route to healthy instances. What configuration is needed?

A. Managed instance group (MIG) with regional configuration and Cloud Load Balancing
B. A single zone deployment with a large instance group and a load balancer in front of it
C. Zone-specific DNS records for each instance, updated by the on-call engineer after a failure
D. Multiple unmanaged instances in one zone, with a load balancer health check routing around any failed one

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Regional MIGs distribute instances across multiple zones with automatic healing. Cloud Load Balancing detects unhealthy instances and routes traffic to healthy ones. Automatic failover between zones. Single zone (B) isn't HA. Unmanaged instances in one zone (D) don't auto-heal and don't survive a zone failure. DNS records (C) require manual failover.

**Key Concept:** [Regional MIGs](https://cloud.google.com/compute/docs/instance-groups/distributing-instances-with-regional-instance-groups)
</details>

### Question 14
**Scenario:** A GKE cluster needs to be updated to a new Kubernetes version. The update should cause no downtime, and the team wants to test the new version before full rollout. What strategy should they use?

A. In-place upgrade of all nodes immediately, relying on the release channel's maintenance window to avoid downtime
B. Blue-green node pool upgrade with surge upgrades
C. Never upgrade, and stay on the current version for as long as it keeps working
D. Delete and recreate the cluster on the new version, then redeploy every workload

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Blue-green upgrades create a new node pool with the new version. Workloads gradually migrate. Surge upgrades add extra capacity during the upgrade. If issues occur, traffic can shift back to the old node pool. In-place (A) risks downtime. Delete/recreate (D) causes major downtime. Never upgrading (C) creates security risks.

**Key Concept:** [GKE Upgrades](https://cloud.google.com/kubernetes-engine/docs/concepts/node-pool-upgrade-strategies)
</details>

### Question 15
**Scenario:** A company needs to provide developers self-service access to create GCP resources within budget limits and approved configurations. What should they implement?

A. No restrictions on what developers can create, with a monthly review of the bill
B. Manual approval for each request by a central cloud team before anything is created
C. Give developers project owner access, with billing budget alerts that email the team when spend reaches 90%
D. Service Catalog with approved Terraform modules and Budget alerts

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Service Catalog provides a curated list of approved solutions (Terraform modules) developers can deploy. Budget alerts notify on spending. This balances self-service with governance. Project owner (C) is too permissive. Manual approval (B) slows development. No restrictions (A) risks cost overruns and non-compliance.

**Key Concept:** [Service Catalog](https://cloud.google.com/service-catalog/docs/overview)
</details>

## Domain 3: Design for Security and Compliance (Questions 17-23)

### Question 16
**Scenario:** A company needs to manage multiple GKE clusters across different environments and regions. They want centralized policy management and consistent security configurations. What should they use?

A. Manage each cluster independently
B. GKE Fleet with Config Sync for policy management
C. Different GCP accounts per cluster
D. A single large cluster for everything, with namespaces and Config Sync used to separate each environment and region

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** GKE Fleet provides centralized multi-cluster management. Config Sync (Anthos Config Management) applies consistent Kubernetes configurations and policies across all clusters from a Git repository. GitOps approach. Independent management (A) causes drift. Single cluster (D) lacks isolation. Different accounts (C) complicate management.

**Key Concept:** [GKE Fleet](https://cloud.google.com/anthos/fleet-management/docs/fleet-overview)
</details>

### Question 17
**Scenario:** A company needs to ensure that all data in Cloud Storage is encrypted with keys they control. They need to rotate keys annually and audit all key usage. What should they configure?

A. No encryption
B. Client-side encryption only, using keys held by the application, with the audit trail kept in the application's logs
C. Default Google-managed encryption
D. Customer-managed encryption keys (CMEK) with Cloud KMS and key rotation policy

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** CMEK in Cloud KMS provides customer-controlled keys for Cloud Storage encryption. Automatic key rotation can be configured (annual or custom). Cloud Audit Logs track all key usage. Default encryption (C) uses Google-managed keys. Client-side (B) is additional, not replacement. No encryption (A) violates requirements.

**Key Concept:** [Cloud KMS](https://docs.cloud.google.com/kms/docs)
</details>

### Question 18
**Scenario:** A company's applications running on GCP need to access Cloud APIs without storing service account keys. Applications run on Compute Engine, GKE, and Cloud Run. What should they use?

A. Store service account keys in the application, in a secrets file that is rotated every 90 days by the build pipeline
B. API keys embedded in each application's configuration file, restricted to the Cloud APIs that the application calls
C. An administrator's user credentials, copied onto each server and refreshed with gcloud whenever they expire
D. Workload Identity (GKE), attached service accounts (Compute Engine), and Cloud Run's service account

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Workload Identity maps Kubernetes service accounts to GCP service accounts - no keys in pods. Compute Engine can attach service accounts to instances. Cloud Run automatically uses the configured service account. No key management required. Stored keys (A) can be leaked. API keys (B) lack fine-grained permissions. User credentials (C) aren't for applications.

**Key Concept:** [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)
</details>

### Question 19
**Scenario:** A company needs to restrict which services can be used in their GCP organization. They want to prevent anyone from creating Compute Engine instances in certain projects while allowing Cloud Run. What should they configure?

A. Delete unwanted services
B. Firewall rules that block the Compute Engine API ports in selected projects while leaving Cloud Run traffic untouched
C. Remove all IAM permissions
D. Organization Policy with resource location constraint and service restriction policies

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Organization Policies provide guardrails. The services constraint (constraints/gcp.restrictServiceUsage) can allow/deny specific services at organization, folder, or project level. This prevents Compute Engine creation while allowing Cloud Run. IAM removal (C) is too broad. Deleting services (A) isn't possible. Firewalls (B) are network, not service restrictions.

**Key Concept:** [Organization Policies](https://cloud.google.com/resource-manager/docs/organization-policy/overview)
</details>

### Question 20
**Scenario:** A company needs to implement zero-trust security for their GKE workloads. Services should only communicate with explicitly allowed services, and all traffic should be encrypted. What should they implement?

A. No security controls
B. Network policies only, with mTLS added by each application itself
C. VPC firewall only
D. Istio service mesh with mutual TLS (mTLS) and authorization policies for each service

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Istio service mesh provides mTLS for encrypted service-to-service communication. Authorization policies define which services can communicate (allow-list). Provides zero-trust within the cluster. Network policies (B) are L3/L4 only, not encrypted. VPC firewall (C) is cluster-external. No controls (A) violates requirements.

**Key Concept:** [Anthos Service Mesh](https://cloud.google.com/service-mesh/docs/overview)
</details>

### Question 21
**Scenario:** A company needs to detect threats and vulnerabilities across their GCP environment, including compromised credentials, cryptomining, and data exfiltration. What should they enable?

A. Cloud Monitoring only
B. Manual log review by the security team, who search the exported audit logs for suspicious entries each week
C. A third-party SIEM only, fed by exported audit logs, with no container runtime or credential-compromise detection
D. Security Command Center Premium with Event Threat Detection and Container Threat Detection

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Security Command Center Premium provides comprehensive threat detection. Event Threat Detection identifies compromised credentials, cryptomining, and suspicious activity. Container Threat Detection finds runtime threats in GKE. Built-in vulnerability scanning. Monitoring (A) is for metrics/logs, not threat detection. Manual review (B) doesn't scale.

**Key Concept:** [Security Command Center](https://cloud.google.com/security-command-center/docs/concepts-security-command-center-overview)
</details>

### Question 22
**Scenario:** A development team needs access to production data for debugging but shouldn't see actual customer PII (names, emails, phone numbers). What should be implemented?

A. Full production access, with query audit logs and a signed policy that forbids reading the PII columns during debugging
B. No debugging access
C. An honor system, with developers trusted not to open the PII columns while they debug production
D. Cloud DLP to de-identify PII in a sanitized dataset or use DLP for on-the-fly redaction

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Cloud DLP (Data Loss Prevention) identifies and de-identifies PII using techniques like masking, tokenization, or generalization. A sanitized dataset can be created for debugging with PII removed. Or use DLP API for on-the-fly redaction. Full access (A) violates privacy requirements. No access (B) blocks debugging. Honor system (C) isn't enforceable.

**Key Concept:** [Cloud DLP](https://docs.cloud.google.com/sensitive-data-protection/docs/sensitive-data-protection-overview)
</details>

## Domain 4: Analyze and Optimize Technical and Business Processes (Questions 24-30)

### Question 23
**Scenario:** A company needs to establish a secure connection between their on-premises network and GCP. The connection should use private IP addresses and not traverse the public internet. They have high bandwidth requirements.

A. Public IP addresses
B. SSH tunnels
C. Cloud VPN, which uses IPsec tunnels with private IP routing and can be scaled by adding tunnels for more bandwidth
D. Dedicated Interconnect with Cloud Router

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Dedicated Interconnect provides private, high-bandwidth (10-200 Gbps) connectivity between on-premises and GCP. Traffic doesn't traverse the public internet. Cloud Router enables dynamic routing with BGP. Cloud VPN (C) uses internet (encrypted). Public IPs (A) traverse internet. SSH tunnels (B) are for specific connections.

**Key Concept:** [Cloud Interconnect](https://cloud.google.com/interconnect/docs/concepts/overview)
</details>

### Question 24
**Scenario:** A company's monthly GCP bill is higher than expected. They need to identify which services, projects, and teams are driving costs and find optimization opportunities. What tools should they use?

A. Cloud Billing reports with cost breakdown, Recommender for optimization suggestions, and budget alerts
B. Ignore costs
C. Manual calculation in a spreadsheet, built by hand from each monthly invoice PDF and sent to the team leads
D. A third-party cost tool only, fed by billing export data and tagged by team, with budget alerts left to the vendor

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Cloud Billing reports show cost breakdown by service, project, and labels (teams). Export to BigQuery enables custom analysis. Recommender provides actionable suggestions like rightsizing VMs or deleting unused resources. Budget alerts notify on spending thresholds. Manual calculation (C) is error-prone. Third-party (D) may miss GCP-specific recommendations.

**Key Concept:** [Cloud Billing](https://cloud.google.com/billing/docs/how-to/reports)
</details>

### Question 25
**Scenario:** A Compute Engine workload runs batch jobs that can tolerate interruption. Jobs take 4 hours to complete and can checkpoint progress. How can they reduce compute costs by up to 91%?

A. Use free tier only
B. Use Spot VMs (preemptible) with checkpointing and automatic restart
C. Run fewer jobs by merging several batches into one large run every night
D. Use larger instances to finish faster, since the shorter runtime cuts the hours billed even at the same hourly rate

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Spot VMs (formerly preemptible) cost up to 91% less than regular VMs. They can be preempted with 30-second warning. Checkpointing saves progress before preemption. Instance groups can automatically restart preempted instances. Ideal for fault-tolerant batch workloads. Larger instances (D) don't reduce unit cost. Free tier (A) has minimal capacity.

**Key Concept:** [Spot VMs](https://cloud.google.com/compute/docs/instances/spot)
</details>

### Question 26
**Scenario:** A company has identified that their Cloud SQL instance is oversized. The instance has 32 vCPUs but CPU utilization averages 10%. What should they do?

A. Add more connections
B. Delete the instance, then create a smaller one and reload the data from the original source
C. Use Active Assist Recommender suggestions to rightsize to appropriate instance size
D. Keep the same size for future growth, because resizing a Cloud SQL instance requires a migration to a new instance

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Active Assist/Recommender analyzes usage patterns and suggests appropriate instance sizes. Rightsizing reduces cost while maintaining performance. Cloud SQL supports live resizing. Keeping oversized (D) wastes money. Deleting (B) loses the database. More connections (A) doesn't address the sizing issue.

**Key Concept:** [VM Rightsizing](https://cloud.google.com/compute/docs/instances/apply-machine-type-recommendations-for-instances)
</details>

### Question 27
**Scenario:** A company's application has variable traffic - high during business hours, low at night. They want to scale down at night to save costs. What should they configure?

A. Fixed capacity 24/7, sized for the daytime peak so that the application never runs short
B. Manual scaling every day by an on-call engineer, who lowers the instance count each evening and raises it again each morning
C. Scheduled scaling or autoscaling based on metrics with scale-down policies
D. Turn off the application every night and start it again when staff arrive in the morning

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Autoscaling with scheduled actions can set minimum instances higher during business hours and lower at night. Metric-based autoscaling adjusts to actual traffic. Scale-down policies control how quickly to reduce capacity. Manual scaling (B) requires daily intervention. Fixed capacity (A) wastes money. Turning off (D) causes downtime.

**Key Concept:** [MIG Autoscaling](https://cloud.google.com/compute/docs/autoscaler/scaling-schedules)
</details>

### Question 28
**Scenario:** A company needs to choose between Cloud Run and GKE for a new microservices application. The team has limited Kubernetes experience, services are HTTP-based, and they want minimal operational overhead. Which should they choose?

A. Cloud Functions
B. Cloud Run, because it runs HTTP containers serverlessly with no clusters or nodes to manage
C. Compute Engine
D. GKE Autopilot for all workloads, since it manages nodes and runs HTTP services

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Cloud Run is serverless containers with zero infrastructure management - ideal for teams without Kubernetes experience. It handles HTTP-based services, auto-scales including to zero, and has per-request pricing. Minimal operational overhead. GKE Autopilot (D) is simpler than standard GKE but still more complex than Cloud Run. CE (C) requires more management.

**Key Concept:** [Cloud Run vs GKE](https://cloud.google.com/blog/topics/developers-practitioners/cloud-run-vs-gke-when-use-which)
</details>

### Question 29
**Scenario:** A BigQuery data warehouse is experiencing slow query performance. Queries scan entire tables even when filtering on specific dates. What optimization should they implement?

A. Implement table partitioning by date and clustering on frequently filtered columns
B. Use smaller tables
C. Export the tables to CSV in Cloud Storage and re-import them under a different table definition
D. Add more slots by buying a reservation, since the queries are slow because the scan work is limited by compute capacity

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Partitioning by date limits scans to relevant partitions (date-filtered queries only scan those dates). Clustering organizes data within partitions by specified columns, improving filter performance. Combined, they dramatically reduce data scanned and improve query speed. More slots (D) add capacity but don't reduce data scanned.

**Key Concept:** [BigQuery Partitioning](https://cloud.google.com/bigquery/docs/partitioned-tables)
</details>

## Domain 5: Manage Implementation (Questions 31-34)

### Question 30
**Scenario:** A company wants to establish SLIs, SLOs, and error budgets for their application. They need to track availability and latency, alert when SLOs are at risk, and make informed decisions about feature velocity vs. reliability.

A. No SLOs
B. Cloud Monitoring SLOs with alerting on burn rate and error budget dashboards
C. Alert on every logged error and page the on-call engineer each time
D. Manual tracking in spreadsheets

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Cloud Monitoring supports defining SLOs with SLIs (availability, latency). Burn rate alerts notify when error budget is being consumed too quickly. Dashboards show remaining error budget for decision-making. This is Google's SRE approach. Spreadsheets (D) aren't automated. No SLOs (A) lacks reliability targets. Every-error alerts (C) cause alert fatigue.

**Key Concept:** [Cloud Monitoring SLOs](https://docs.cloud.google.com/stackdriver/docs/solutions/slo-monitoring)
</details>

### Question 31
**Scenario:** A team needs to plan the migration of 200 VMs from on-premises to GCP. They need to discover VM configurations, dependencies, and estimate GCP costs. What should they use?

A. Migration Center (formerly Migrate for Compute Engine assessment) for discovery, dependency mapping, and TCO analysis
B. Migrate everything at once
C. Guess the requirements from the on-premises hypervisor's allocated sizes and migrate in waves, adjusting later
D. Manual inventory

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Migration Center (formerly part of Migrate for Compute Engine) provides agentless discovery of VM configurations, automatic dependency mapping to identify migration groups, and TCO analysis to estimate GCP costs. Creates a migration plan. Manual inventory (D) is time-consuming and error-prone. Big-bang migration (B) is risky.

**Key Concept:** [Migration Center](https://docs.cloud.google.com/migration-center/docs)
</details>

### Question 32
**Scenario:** A company is migrating their database from on-premises MySQL to Cloud SQL. They need minimal downtime during cutover. What migration approach should they use?

A. Recreate the schema on Cloud SQL and start fresh, leaving the old data behind in the source
B. Database Migration Service with continuous replication and minimal-downtime cutover
C. Export, transfer, import, accepting extended downtime while the dump loads, which preserves exactly the data at export time
D. Keep the database on-premises and connect to it from Google Cloud applications over a VPN

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Database Migration Service (DMS) provides continuous replication from source to Cloud SQL. Data stays synchronized until cutover. The cutover window is minimal (minutes). Supports MySQL, PostgreSQL, and SQL Server. Export/import (C) requires extended downtime. Starting fresh (A) loses data.

**Key Concept:** [Database Migration Service](https://cloud.google.com/database-migration/docs/overview)
</details>

### Question 33
**Scenario:** A development team wants to adopt CI/CD for their GCP deployments. They use GitHub for source control and want to deploy to Cloud Run on every push to main. What should they configure?

A. FTP uploads
B. GitHub Actions only, deploying with a JSON service account key committed to the repository so that no GCP-side trigger is needed
C. Manual deployments
D. Cloud Build triggered by GitHub, with cloudbuild.yaml defining build and deploy steps

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Cloud Build integrates with GitHub via triggers. Push to main triggers a build defined in cloudbuild.yaml. Steps can build container, push to Artifact Registry, and deploy to Cloud Run. Native GCP integration with IAM. GitHub Actions (B) can work with Workload Identity Federation, but committing a long-lived service account key to the repository is a security failure. Manual (C) isn't CI/CD.

**Key Concept:** [Cloud Build](https://cloud.google.com/build/docs/overview)
</details>

## Domain 6: Ensure Solution and Operations Reliability (Questions 35-40)

### Question 34
**Scenario:** A company has a tight deadline for GCP migration. They need to accelerate the project without sacrificing quality. What should they do?

A. Delay the deadline by one quarter, and use the extra time to run the migration at the original pace with the same team
B. Skip testing so that the migration reaches production sooner, and fix any defects afterward
C. Work overtime indefinitely until the migration is done, with the same team and the same plan
D. Engage Google Cloud consulting or a certified partner with migration experience

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Google Cloud consulting and certified partners have migration expertise and can accelerate projects with proven methodologies. They bring experience from similar projects. Professional services can supplement internal teams. Skipping testing (B) causes quality issues. Extended overtime (C) isn't sustainable.

**Key Concept:** [Google Cloud Partners](https://cloud.google.com/partners)
</details>

### Question 35
**Scenario:** A company needs to ensure their application can survive the failure of an entire GCP region. RTO is 30 minutes and RPO is 5 minutes. What architecture should they implement?

A. Backup and restore only
B. Multi-region architecture with Cloud Spanner (or Cloud SQL cross-region replicas), regional load balancing, and Cloud DNS failover
C. An on-premises DR site, with replicated data over Interconnect and servers kept powered on to meet a 30-minute RTO
D. Single region with multiple zones

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Multi-region architecture distributes across regions. Cloud Spanner provides multi-region with automatic failover. For Cloud SQL, cross-region replicas with promotion meet RPO. Global/multi-region load balancing with health checks and Cloud DNS failover routing traffic to healthy region. Meets 30-min RTO and 5-min RPO. Single region (D) doesn't survive regional failure.

**Key Concept:** [Disaster Recovery Planning](https://cloud.google.com/architecture/disaster-recovery)
</details>

### Question 36
**Scenario:** A production system experienced an outage. The team needs to conduct a blameless post-incident review (postmortem) and prevent recurrence. What should they focus on?

A. Punish the responsible team
B. Document timeline, root cause analysis, action items for prevention, and update runbooks
C. Find the individual whose change started the outage so that they can be coached before the next release cycle
D. Ignore the outage and move on to the next project, since the service is back up and the users are calm

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Blameless postmortems focus on systemic improvements, not individual blame. Document what happened (timeline), why it happened (root cause analysis), and how to prevent it (action items). Update runbooks for future incidents. Blame (A, C) discourages reporting. Ignoring (D) leads to repeat incidents.

**Key Concept:** [Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
</details>

### Question 37
**Scenario:** A team needs to automate responses to common production issues, such as restarting unhealthy services or clearing full disks. What should they implement?

A. Manual intervention for all issues
B. Cloud Monitoring alerting policies with notification channels that trigger Cloud Functions for automated remediation
C. Reboot servers daily on a schedule so that memory leaks and full disks are cleared before they cause an outage
D. Ignore alerts

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Alerting policies detect issues (unhealthy service, disk full). Notification channels can trigger Cloud Functions or Pub/Sub. Functions execute remediation (restart service, clean disk, scale up). Automation reduces MTTR. Manual intervention (A) is slow. Ignoring (D) causes outages. Daily reboots (C) are disruptive.

**Key Concept:** [Alerting Policies](https://cloud.google.com/monitoring/alerts)
</details>

### Question 38
**Scenario:** A company wants to implement chaos engineering to test the resilience of their GKE-based application. They want to randomly terminate pods and observe system behavior. What should they use?

A. Chaos engineering tools like Chaos Mesh or LitmusChaos with controlled experiments
B. Production experiments without safeguards, killing pods at random during peak hours so engineers see the true impact
C. Never test failure scenarios
D. Delete production pods manually

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Chaos Mesh and LitmusChaos provide controlled chaos experiments with safeguards. They can terminate pods, inject network latency, and more. Experiments are time-bounded with abort conditions. Results improve resilience. Production without safeguards (B, D) risks uncontrolled outages. Never testing (C) means unknown failure modes.

**Key Concept:** [Chaos Engineering](https://docs.cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-failures)
</details>

### Question 39
**Scenario:** A Cloud Run service is experiencing intermittent 503 errors during traffic spikes. Logs show "instance scaling" messages. What should they investigate and configure?

A. Switch to a VM, since Cloud Run instances cannot scale quickly enough to handle sudden bursts of traffic
B. Reduce traffic
C. Ignore the errors
D. Configure minimum instances to reduce cold starts, review concurrency settings, and optimize container startup time

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** 503 errors during scaling suggest cold start latency or insufficient capacity. Minimum instances keep containers warm. Concurrency settings control requests per instance (too low = more instances needed). Optimizing startup time (smaller images, faster init) reduces cold start impact. Ignoring (C) provides poor UX.

**Key Concept:** [Cloud Run Performance](https://cloud.google.com/run/docs/tips/general)
</details>

### Question 40
**Scenario:** A company needs to create comprehensive documentation for their GCP architecture, including disaster recovery procedures, runbooks, and architectural diagrams. What format and tools should they use?

A. Email chains
B. Paper documents stored in a locked cabinet at each office, with copies of the runbooks printed whenever they change
C. Undocumented knowledge in engineers' heads
D. Version-controlled documentation (Markdown in Git), architecture diagrams (draw.io or Lucidchart), and automated runbooks (Cloud Workflows or Terraform)

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Version-controlled documentation enables collaboration and history. Markdown in Git works with CI/CD. Architecture diagrams visualize systems. Automated runbooks (Cloud Workflows, Terraform) ensure procedures are tested and repeatable. Undocumented (C), paper (B), and email (A) aren't accessible, searchable, or maintainable.

**Key Concept:** [Architecture Documentation](https://docs.cloud.google.com/architecture/framework/operational-excellence)
</details>

## Case Studies, AI and Operations (Questions 41-66)

### Question 41
**Scenario:** EHR Healthcare needs at least 99.9% availability for containerized customer-facing apps while keeping cost and operations low. Which design fits?

A. Active-active clusters in three regions with global database replication
B. Self-managed Kubernetes on Compute Engine in one zone
C. One zonal GKE cluster with nightly snapshots
D. Regional GKE clusters across zones, a global load balancer, and a highly available managed database

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** A multi-zone regional design meets 99.9% without the cost and complexity of multi-region. Active-active across regions is more than the stated target. A single zone cannot meet the target, and self-managed Kubernetes adds the operational burden the case wants to cut.
</details>

### Question 42
**Scenario:** EHR Healthcare's legacy insurer interfaces must stay on-premises but connect securely and with high performance to Google Cloud.

A. Redundant Dedicated or Partner Interconnect with HA VPN as backup
B. Public internet with TLS only, using a different certificate for each insurer interface
C. Move the insurer systems to Compute Engine first, then connect to them with VPC peering once the cutover completes
D. A single Cloud VPN tunnel over the public internet to the insurer's data center

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The case says the legacy systems will not move, so hybrid connectivity is required. Redundant Interconnect gives performance and availability, and HA VPN is a backup path. One tunnel is a single point of failure.
</details>

### Question 43
**Scenario:** EHR Healthcare's monitoring emails are often ignored. They want proactive action on performance.

A. SLO-based alerting policies with severity routing to paging and ticketing in Cloud Monitoring
B. Disable alerts and review dashboards weekly
C. Increase log retention
D. Send more alert emails to a larger group, with a rota so that someone reads each one

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Alerts need thresholds tied to user impact, an owner and the right channel. The volume of email is the problem, not too few emails.
</details>

### Question 44
**Scenario:** EHR Healthcare staff are managed in Microsoft Active Directory. How should they sign in to Google Cloud?

A. Use API keys for people
B. Federate with Cloud Identity (or Workforce Identity Federation) and sync users and groups from AD
C. Share one service account key
D. Create separate Google accounts and passwords for each user, and ask staff to keep them in step with their AD accounts

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Federation keeps one source of truth, reuses existing joiner and leaver processes and avoids extra passwords. Service account keys and API keys are not for people.
</details>

### Question 45
**Scenario:** EHR Healthcare needs consistent log retention for compliance across many projects.

A. Export logs to a developer laptop monthly
B. Aggregated log sinks at the organization or folder to a log bucket or Cloud Storage with a locked retention policy
C. Each team configures logging and retention in its own project, following a written standard that auditors review yearly
D. Rely on the default retention

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Aggregated sinks give one policy for every project, and a retention lock prevents deletion before the period ends.
</details>

### Question 46
**Scenario:** Cymbal Retail wants gen AI to produce product attributes from supplier text and images, but wrong data must never reach the live catalog.

A. Generate attributes in the browser on each page view
B. Use a multimodal Gemini model to propose attributes and add a human review step that approves before writing to the catalog
C. Let the model write straight to the catalog and have a nightly job correct any errors that customers report
D. Train a custom model from scratch on supplier data

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A foundation model handles the multimodal task without custom training, and a human-in-the-loop step controls risk. Writing straight to production fails the requirement.
</details>

### Question 47
**Scenario:** Cymbal Retail customers should find products by describing them in natural language, and the team wants a managed solution.

A. Agent Search for commerce (Discovery AI) behind a conversational agent
B. A custom ranking model on GPUs, trained on click data and served from a self-managed endpoint behind the storefront
C. A custom keyword query against the relational database, with a synonym table kept by hand
D. A Cloud Storage bucket of static product pages that customers browse by category and brand

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The case names Discovery AI. A managed retail search product beats building and tuning a custom ranking model. Keyword SQL is what they have today and it does not understand natural language.
</details>

### Question 48
**Scenario:** Cymbal Retail wants to replace its IVR menus and reduce call-center cost, but customers must still reach a person when needed.

A. Conversational agents for voice and chat with handoff to a human agent
B. Remove the phone line and move every customer to the web chat page without a human option
C. A bigger IVR menu tree, with more levels and spoken options so callers reach the right queue without an agent
D. An FAQ web page that answers the most common questions from callers, with no agent

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Conversational agents understand intent in natural language and can escalate. Removing the phone line hurts customers.
</details>

### Question 49
**Scenario:** Cymbal Retail must move a production MySQL database to Cloud SQL with minimal downtime.

A. Database Migration Service with continuous replication, then a short cutover
B. Rewrite the application for Spanner first, then move the data across into the new schema
C. Copy the database files to Cloud Storage with Storage Transfer Service, then mount them
D. Export a dump nightly and import it over a weekend, with the application stopped while the final import runs

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Database Migration Service replicates continuously and shortens cutover to minutes. Dump and restore needs long downtime, and Spanner would be a redesign.
</details>

### Question 50
**Scenario:** Altostrat Media stores a growing media library with unpredictable access patterns and wants lower storage cost without manual management.

A. Cloud Storage with Autoclass
B. Move all files to Persistent Disk
C. Keep everything in Standard, since retrieval fees in colder classes make unpredictable access cost more overall
D. Delete older assets

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Autoclass moves objects between storage classes based on access, which saves cost without a hand-written lifecycle policy. Deleting media loses assets.
</details>

### Question 51
**Scenario:** Altostrat Media must show that its AI decisions are auditable and can be explained.

A. Use the largest model available, since a bigger model gives answers that are more accurate and so need less auditing
B. Rely on the model's own written explanation of each answer as the only audit record, with no other logs kept
C. Log prompts, responses and model versions, keep audit logs, evaluate models, and keep human review
D. Disable logging to protect privacy

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Auditability comes from records and process. Explainability needs documentation, evaluation and, for custom models, explainability tooling. A bigger model does not make decisions auditable.
</details>

### Question 52
**Scenario:** Altostrat Media needs Kubernetes both on-premises and in Google Cloud, managed centrally with the same policies.

A. One VM per service in each location, with the same policy files copied across by hand
B. GKE Enterprise fleets with Config Sync and Policy Controller
C. Separate manually managed clusters in each location, with the same YAML policies applied by hand after each change
D. Cloud Functions everywhere, with no Kubernetes on the on-premises sites

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Fleets give central visibility and consistent configuration and policy across environments.
</details>

### Question 53
**Scenario:** KnightMotives must meet EU data protection rules and keep control of encryption keys for vehicle data.

A. A US multi-region bucket with default encryption, since Google-managed keys satisfy EU data protection rules for all vehicle data
B. Any region, with encryption in the application only
C. Global Spanner with default settings, replicating the vehicle data automatically to every region it serves worldwide
D. EU regions, Assured Workloads for the EU, a resource-location org policy, and CMEK or External Key Manager

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Residency, key control and policy enforcement address EU rules. A US multi-region breaks residency.
</details>

### Question 54
**Scenario:** KnightMotives wants to monetize data by sharing curated datasets with partners without copying them.

A. Email CSV exports to partners each month, protected with a password sent separately, so every partner gets a copy
B. BigQuery with Analytics Hub listings
C. Public Cloud Storage buckets of CSV exports
D. Give partners project owner access on the data project

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Analytics Hub shares BigQuery datasets as governed listings with access control and without copies. Public buckets and owner roles are unsafe.
</details>

### Question 55
**Scenario:** KnightMotives dealers have no budget for new equipment. What should the new dealer tools use?

A. Browser-based applications with federated sign-in
B. Custom hardware kiosks
C. A native app that needs dedicated devices
D. On-premises servers at each dealership, installed once and managed centrally by the manufacturer's IT team

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** A web or SaaS delivery model needs no new equipment. This is a constraint the answer must respect.
</details>

### Question 56
**Scenario:** KnightMotives needs large GPU or TPU capacity for autonomous driving simulation and training, with planned run windows.

A. A single large VM with local SSD
B. Small general-purpose VMs
C. Cloud Functions
D. GKE or batch on AI Hypercomputer, with reservations or Dynamic Workload Scheduler

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Accelerators are scarce, so use reservations or scheduling to secure capacity, and orchestrate with GKE or batch.
</details>

### Question 57
**Scenario:** A chat assistant must be protected against prompt injection and must not leak card numbers in answers.

A. Longer prompts
B. Model Armor on prompts and responses, with Sensitive Data Protection detection
C. Disable the assistant at night and during maintenance windows, when fewer staff are present to notice abuse
D. A firewall rule

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Model Armor screens both directions for injection, harmful content and sensitive data, and integrates with Sensitive Data Protection.
</details>

### Question 58
**Scenario:** A company wants to extract fields from scanned invoices quickly with no ML team.

A. Document AI processors for invoices
B. BigQuery ML
C. Cloud Natural Language entity analysis on the scanned images
D. Train a custom image model on the company's own invoices, which needs labelled data and an ML team to maintain it

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Document AI is the prebuilt document extraction service. Use the lowest rung of the ladder that meets the need.
</details>

### Question 59
**Scenario:** Answers from a support assistant must reflect company documents that change daily, with citations.

A. Use a larger model with no data
B. Hard-code answers in the prompt
C. Fine-tune the model weekly on the new documents, so the weights reflect the latest company text and its sources
D. Grounding or RAG over an index of the documents

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Retrieval keeps answers current and citable. Tuning is slow and does not keep up with daily changes.
</details>

### Question 60
**Scenario:** A fault-tolerant ML training job should cost as little as possible.

A. A three-year commitment for an occasional job, which gives a discount only if the capacity is used continuously
B. Sole-tenant nodes
C. Spot capacity with regular checkpoints
D. On-demand VMs only, started on request and deleted when the training job ends

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Spot capacity is the cheapest, and a checkpointed job survives preemption.
</details>

### Question 61
**Scenario:** An alert fires and the team wants help finding the root cause across logs, metrics and configuration.

A. Delete the alert policy
B. Gemini Cloud Assist Investigations, which analyzes logs, metrics, and configuration to rank likely causes
C. Increase the alert threshold
D. Export logs to a spreadsheet and have an engineer search them by hand

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Investigations analyses logs, metrics and configuration and ranks observations. It assists the team and does not replace judgment.
</details>

### Question 62
**Scenario:** A data center lease ends soon and the estate is mostly VMware VMs. The team wants minimal change first.

A. Buy new hardware and renew the data center lease
B. Rewrite everything as microservices on GKE, which removes the VMware dependency but needs large application changes first
C. Move every workload to Cloud Run functions
D. Google Cloud VMware Engine

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** VMware Engine runs the same VMware stack on Google Cloud, which suits a deadline-driven lift and shift. Modernize later.
</details>

### Question 63
**Scenario:** Before a migration the team needs inventory, dependency mapping and a cost comparison.

A. Compute Engine rightsizing recommendations, which advise on machine types for VMs already running in Google Cloud
B. Cloud Billing reports
C. Transfer Appliance
D. Migration Center discovery, assessment and TCO reports

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Migration Center is built for discovery, assessment and migration planning, including TCO.
</details>

### Question 64
**Scenario:** The team wants to prove a service degrades gracefully when a zone fails.

A. Wait for a real outage
B. Run a controlled failure-injection (chaos) test, starting in staging with a small blast radius
C. Disable health checks
D. Add more zone health alerts so the team hears quickly when a real zone failure occurs

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Chaos engineering tests resilience on purpose, safely. Start small and have a stop condition.
</details>

### Question 65
**Scenario:** Developers need to test Pub/Sub and Spanner code locally and in CI without cloud cost.

A. Test directly in production
B. Cloud emulators for Pub/Sub and Spanner, run locally and in CI so that tests cost nothing and touch no cloud project
C. Mock nothing
D. Use the BigQuery sandbox, a free project for running queries with no Pub/Sub or Spanner emulation

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Emulators exist for Bigtable, Spanner, Pub/Sub and Firestore, and run locally or in CI.
</details>

### Question 66
**Scenario:** A business needs recovery in about 15 minutes with minimal data loss, but cannot afford active-active.

A. Backup and restore from archives kept in a second region and loaded onto new servers after a failure
B. Warm standby with replicated data and scaled-down compute that scales up on failover
C. Do nothing until an incident happens, then decide on the recovery plan with the team on the day
D. Pilot light with core data replicated but no compute provisioned, so servers are built from images after failover begins

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Warm standby meets a minutes-level RTO at moderate cost. Backup and restore is too slow, a pilot light must build compute after failover so it misses 15 minutes, and active-active costs more than the stated budget.
</details>

## Case Studies Set 2 (Questions 67-109)

Ten or eleven questions per current case study, written against Google's v6.1 case text on 2026-11-18. Each tests one constraint from the case. The same questions are in the interactive case quiz of the AWS to Google Cloud study guide.

### Question 67
**Scenario:** Altostrat keeps original master files of every broadcast. They are read less than once a year but must stay retrievable within seconds when legal asks. Recent content is read constantly. What is the lowest-cost design that keeps availability?

A. Keep masters in Standard class and delete the transcoded copies after one year to cut the total object count
B. Lifecycle rule moving masters to Archive class after 30 days; current content stays Standard
C. Move every object, hot and cold, to Nearline so the whole library has one predictable storage price
D. Copy the masters to Persistent Disk snapshots in a second region and delete them from Cloud Storage

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Archive class costs the least to store and still serves reads in milliseconds. Its 365-day minimum and retrieval fees suit files read about once a year. The access pattern is known, so a lifecycle rule fits (Autoclass is for unpredictable patterns). Keeping masters in Standard pays hot-storage prices for cold data, and Nearline is the wrong price point for both hot and cold data.
</details>

### Question 68
**Scenario:** Altostrat's on-premises ingestion system sends several terabytes of new media to Cloud Storage every day, and the case asks for secure, high-performance hybrid connectivity. What should they use?

A. A single Cloud VPN tunnel from the ingestion site, sized up by adding more media servers behind it
B. Transfer Appliance shipped every week, with uploads queued on-premises between shipments
C. Uploads over the public internet using parallel composite uploads and resumable transfers
D. Redundant Dedicated Interconnect, with HA VPN as backup

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Daily continuous ingestion at TB scale needs a private, high-bandwidth link, and redundancy keeps it reliable (reliability is a top priority). One VPN tunnel caps throughput and is a single point of failure. Transfer Appliance suits one-off bulk moves, not a daily feed.
</details>

### Question 69
**Scenario:** The legacy on-premises archive (about 400 TB) is slated to move to Google Cloud soon. The Interconnect is already busy with daily ingestion. What is the best plan?

A. Leave the archive on-premises indefinitely and give cloud applications access to it over HA VPN
B. Transfer Appliance for the bulk copy, then Storage Transfer Service for changes, into Archive class
C. Rewrite the archive application to run on GKE first, then move the data once the new app is live
D. Copy the files with rsync over the Interconnect from one admin workstation during off-peak hours

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The case says these systems are slated for migration, so keeping them forever is wrong. A bulk offline copy avoids saturating the busy link, and Storage Transfer Service with on-prem agents catches up on changes. Archive class keeps the cost low.
</details>

### Question 70
**Scenario:** Altostrat must automatically detect and filter inappropriate content in uploaded video and audio, with as little custom machine learning as possible.

A. Train a custom moderation model on GPUs from labeled examples of Altostrat's own historical content
B. Have a team of moderators watch every upload before it is published, around the clock
C. Filter on keywords in titles, descriptions and tags supplied by uploaders before publishing
D. Pre-trained detection (Video Intelligence, Gemini safety settings) with humans reviewing borderline cases

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Pre-trained APIs and Gemini safety filters meet the requirement with no model to build. Routing only uncertain cases to people keeps the human cost low. Keyword filtering misses what is actually in the media.
</details>

### Question 71
**Scenario:** Altostrat wants a 24/7 support chatbot that answers questions about its own catalog and policies without inventing facts. What is the right approach?

A. Fine-tune a model each month on all catalog and help content and serve it without retrieval
B. A rule-based decision tree that maps each known question to a fixed answer written by support staff
C. An agent grounded on an Agent Search data store of the catalog and help content
D. Prompt a general-purpose model with a long system prompt describing the company, with no data access

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Grounding (retrieval-augmented generation) keeps answers tied to current company content and cuts hallucination. Fine-tuning alone goes stale and still invents facts. A decision tree does not meet the natural language requirement.
</details>

### Question 72
**Scenario:** Every new podcast or video should get a summary and metadata within minutes of upload, at the scale of the whole library. Which design fits Altostrat's existing environment?

A. Object-finalized event via Eventarc to a Cloud Run function that calls Gemini and writes to BigQuery
B. A nightly cron job on a Compute Engine VM that lists every object in the bucket and processes new ones
C. A Dataproc cluster that runs a Spark job once a week across the whole media library
D. Editors write each summary by hand in a shared spreadsheet that is loaded into BigQuery

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Altostrat already uses Cloud Run functions for event-driven tasks, so this is the least change. It reacts within minutes and scales with uploads. A nightly listing is slow and gets more expensive as the library grows.
</details>

### Question 73
**Scenario:** Altostrat must modernize CI/CD for containers with a centralized management platform, deploying to GKE in the cloud and to on-premises clusters.

A. Install Jenkins separately in each cluster, with each team owning the pipeline for its own cluster
B. Engineers run kubectl apply from their laptops with a shared kubeconfig for every cluster
C. Cloud Build pushes custom VM images to Compute Engine, and instance groups roll them out per site
D. Cloud Build and Artifact Registry, Cloud Deploy across fleet clusters, Binary Authorization

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Cloud Deploy gives one place to define the delivery pipeline and promote releases across targets. Fleet membership lets it reach on-prem clusters too. Binary Authorization adds supply-chain control. Per-cluster Jenkins is the opposite of centralized.
</details>

### Question 74
**Scenario:** Altostrat runs Prometheus on its clusters and Cloud Monitoring elsewhere, with alerts by email. Reliability is a top priority. What should they change first?

A. Keep both systems and send each alert email to a wider distribution list so more people see it
B. Managed Service for Prometheus into Cloud Monitoring, SLO burn-rate alerts that page
C. Add alerts for every CPU spike above 50% on every node so problems are caught earlier
D. Retire Prometheus, stop collecting custom application metrics, and rely only on default metrics

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Managed Service for Prometheus keeps their PromQL and exporters while centralizing the data. SLO burn-rate alerts with paging route the few alerts that matter to someone who acts. More email and noisier alerts make alert fatigue worse.
</details>

### Question 75
**Scenario:** Content strategists want to see which topics are trending across viewing data and AI-extracted metadata, using SQL and dashboards. What should Altostrat use?

A. Export the viewing and metadata tables nightly to Cloud SQL and run the trend queries there
B. Load the data into Bigtable and query it from a spreadsheet through a connector
C. BigQuery with Looker dashboards, plus BigQuery ML or Gemini in BigQuery
D. Build a custom analytics engine on GKE that reads the raw objects from Cloud Storage

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** BigQuery is already their primary warehouse, so this is the least change and needs no servers. Cloud SQL and Bigtable are built for serving transactions and lookups, not ad-hoc analytics at this scale.
</details>

### Question 76
**Scenario:** Altostrat's consumer apps let viewers sign in with Google and with other third-party identity providers. Which service fits customer sign-in?

A. Identity Platform, with Google and third-party identity providers enabled
B. Create a Cloud Identity account for every viewer so the console can manage them centrally
C. Workforce Identity Federation with each third-party provider configured as a workforce pool
D. A dedicated IAM service account per viewer, with keys issued to the mobile and web apps

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Identity Platform is built for an app's end users and supports many external IdPs. Cloud Identity and Workforce Identity Federation are for staff, and service accounts are for workloads.
</details>

### Question 77
**Scenario:** Altostrat wants to simplify infrastructure management for new GKE workloads so that teams deploy fast without tuning node pools. What fits the executive priority of reliability and cost?

A. Self-managed Kubernetes on Compute Engine with Terraform templates shared across teams
B. GKE Autopilot clusters: Google manages nodes, billing is per pod request
C. GKE Standard clusters with large fixed node pools sized for the busiest hour of the year
D. Move each workload to its own Compute Engine VM managed by a managed instance group

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Autopilot removes node management and uses Google's hardening and scaling defaults, and you pay for what pods request instead of idle nodes. Peak-sized fixed pools waste money, and self-managed Kubernetes adds operational work.
</details>

### Question 78
**Scenario:** Cymbal's generated attributes must fit the existing catalog structure: each category has a fixed set of attribute names and allowed values. How should the Gemini call be set up?

A. Ask Gemini for free-text attributes, then parse them into catalog fields with regular expressions
B. Controlled generation with a response schema (enums per category) plus few-shot examples
C. Train a new language model from scratch on Cymbal's existing catalog and supplier feeds
D. Run Vision API label detection on supplier images and store the returned labels as attributes

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A response schema forces valid structured output, so values always match the catalog. Few-shot examples improve accuracy. Free-text parsing is brittle, and labels alone cannot produce category-specific attributes.
</details>

### Question 79
**Scenario:** Cymbal needs product image variations from one base photo: other colors, new backgrounds and text overlays. Which tool fits?

A. Vision API object localization to find the product, then crop it onto stock backgrounds
B. A Gemini text model that writes a description of each variant for the product page
C. Book a studio photo shoot for each color and background variant before the product launches
D. Imagen generation and editing on the Agent Platform

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Imagen supports editing a base image, including background changes and recoloring. The Vision API analyzes images and cannot create them, and new photo shoots are the manual cost the case wants to remove.
</details>

### Question 80
**Scenario:** Associates need a UI to approve, reject or modify gen AI suggestions. Only Cymbal staff may reach it, and the team does not want to build its own login system. What is the best design?

A. A review web app on Cloud Run behind IAP that writes only approved items to the catalog
B. A public web page protected by one shared password that is rotated each quarter
C. Email each batch of suggestions to associates as a CSV, and load their replies into the catalog
D. Let associates edit the production catalog database directly with a SQL client

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** IAP adds identity-based access with no app-side login code, and Cloud Run keeps it serverless. Writing only approved items preserves the human-in-the-loop step. Direct database edits skip both review and audit.
</details>

### Question 81
**Scenario:** Enrichment must run over millions of existing SKUs once, then over each day's new supplier items. Latency does not matter for the backlog. What is the most cost-effective way to call the model?

A. Synchronous online calls from a single Compute Engine VM, processing one item at a time
B. Batch inference jobs, with online calls only for urgent new items
C. Provision dedicated GPUs and host an open model full time for both the backlog and new items
D. Have associates write descriptions for the backlog while the model handles only new items

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Batch inference is cheaper per request and built for large offline jobs, and it avoids online rate limits. Hosting a model full time pays for idle capacity. One-at-a-time calls from one VM do not scale to millions.
</details>

### Question 82
**Scenario:** Cymbal's conversational shopping agent sometimes recommends products that are out of stock or do not exist. What is the best fix?

A. Raise the model temperature so the agent offers a wider variety of products in its answers
B. Remove product names from the agent's answers and link only to category pages
C. Ground the agent on the commerce search index of the live catalog and inventory
D. Fine-tune the model once on last year's full catalog and redeploy it before the holiday season

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Grounding on current catalog data makes the agent recommend only real, available products. A model fine-tuned once goes stale, and a higher temperature makes hallucination worse.
</details>

### Question 83
**Scenario:** Cymbal runs Microsoft SQL Server for order data and wants a managed service with minimal downtime during migration. What should they use?

A. Rewrite the order application for Spanner first, then migrate the data with a custom ETL job
B. Run SQL Server on Compute Engine yourself and copy changes with manual log shipping
C. Export every table to CSV during a weekend outage and import the files into the new database
D. Database Migration Service to Cloud SQL for SQL Server

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Database Migration Service supports SQL Server as a source and Cloud SQL for SQL Server as a target, so the move is managed with little downtime. Rewriting for Spanner is a large change the case does not need. Self-managed keeps the admin cost the case wants to cut.
</details>

### Question 84
**Scenario:** Cymbal's Redis cache holds sessions and hot catalog lookups. What gives the least operational overhead in Google Cloud?

A. Memorystore for Redis
B. Redis on a self-managed Compute Engine VM with a startup script and nightly snapshots
C. Store cache entries as small objects in a regional Cloud Storage bucket
D. A single-node Bigtable instance with one column family for sessions and lookups

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Memorystore is managed, Redis-compatible and offers HA, so the application changes very little. Cloud Storage latency is too high for a cache, and a VM brings back patching and failover work.
</details>

### Question 85
**Scenario:** Suppliers send nightly SFTP files that feed batch ETL, which causes delays and manual error handling. Cymbal cannot force every supplier to change at once. What modernizes the flow with the least disruption?

A. Require every supplier to build and call a streaming API before the next selling season
B. Keep the nightly batch and hire more operations staff to fix failed files each morning
C. Land files in Cloud Storage, trigger processing per object via Eventarc, dead-letter bad files
D. Have suppliers email files to an operations inbox that staff upload into the catalog by hand

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Suppliers keep sending files, but processing becomes event-driven and automatic, and failed files are caught for review instead of breaking the batch. Forcing all suppliers to change at once is unrealistic.
</details>

### Question 86
**Scenario:** Customer chats with virtual agents may contain names, addresses and card numbers. Cymbal wants to analyze the transcripts while meeting security and compliance requirements. What should they do?

A. Store raw transcripts in a bucket readable by the whole analytics team so nothing is lost
B. Turn off all logging of virtual agent conversations so no personal data is ever stored
C. Encrypt the transcripts with a customer-managed key and then destroy the key after 30 days
D. Model Armor on the agent, Sensitive Data Protection de-identification before BigQuery

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** De-identification keeps the analytic value while removing sensitive data. Model Armor guards the live agent against prompt attacks and data leakage. Turning off logging removes the auditability and insight the business needs.
</details>

### Question 87
**Scenario:** Data silos stop Cymbal from seeing the whole customer journey across MySQL, SQL Server and MongoDB. Analysts need near-real-time data. What should they build?

A. Datastream CDC from the operational databases into BigQuery
B. Nightly point-to-point exports between every pair of databases so each has a full copy
C. Consolidate all of the databases into one very large Cloud SQL instance for every workload
D. Load all operational data into Bigtable and use it as the analytics warehouse

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Datastream streams changes with low impact on the sources, and BigQuery joins them for analytics. Point-to-point exports multiply the silos, and a single OLTP database is not an analytics engine.
</details>

### Question 88
**Scenario:** Cymbal monitors with Grafana, Nagios and Elastic and wants proactive monitoring with less tooling to run. Teams like their Grafana dashboards. What should they do?

A. Keep running Grafana, Nagios and Elastic on Compute Engine VMs, managed by the current team
B. Cloud Monitoring and Logging with Managed Service for Prometheus, Grafana kept as a front end
C. Replace live monitoring with a daily email report of system health sent to each team
D. Move Nagios into a GKE cluster so it scales with the number of checks

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** This consolidates the data in managed services and removes self-hosted tools to run, while teams keep the dashboards they know. Moving Nagios to GKE keeps the tool sprawl.
</details>

### Question 89
**Scenario:** The lease on one of EHR's colocation facilities is about to expire. Its workloads are a mix of VMs and containers. What should they do first?

A. Refactor every application to Cloud Run before moving anything, so nothing is moved twice
B. Sign a new multi-year lease on the facility to buy time for a full redesign
C. Move only the databases to Cloud SQL now and leave the applications in the colocation site
D. Lift and shift VMs with Migrate to Virtual Machines and containers to GKE; modernize later

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** The lease sets a hard date, so the fastest low-risk move comes first and modernization follows. Refactoring everything first puts the deadline at risk, and splitting apps from their databases adds latency and risk.
</details>

### Question 90
**Scenario:** EHR must maintain and manage multiple container-based environments (dev, test, prod) consistently, because outages came from misconfigured systems. What should they use?

A. Configure each cluster by hand from a detailed runbook, reviewed by a second engineer
B. Run every environment and every customer in one shared cluster to reduce the number of clusters
C. A fleet with Config Sync from Git and Policy Controller guardrails
D. Use a different Kubernetes distribution for each environment, chosen by each team

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** GitOps with Config Sync makes every cluster match the repository and corrects drift. Policy Controller blocks unsafe configuration before it lands. That addresses the misconfiguration outages in the executive statement directly.
</details>

### Question 91
**Scenario:** EHR wants to onboard new insurance providers as quickly as possible through secure, standard APIs with keys, quotas and analytics. What fits?

A. Apigee API products that each new insurer subscribes to
B. Build a dedicated VPN tunnel and a custom integration for each new insurance provider
C. Issue read-only database credentials to each insurer so they can pull the data they need
D. Exchange files over SFTP and have staff review and load each insurer's files by hand

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Apigee turns onboarding into issuing credentials for an existing API product, and adds security, quotas and usage analytics. Per-insurer custom work is slow, and database credentials are a compliance risk.
</details>

### Question 92
**Scenario:** EHR must create interfaces to ingest and process clinical data from new providers in healthcare formats such as HL7v2 and FHIR. What is the best managed choice?

A. Write a custom parser on a Compute Engine VM for each message format and provider
B. Cloud Healthcare API HL7v2 and FHIR stores, with Pub/Sub notifications
C. Keep the raw messages in Memorystore so downstream services can read them quickly
D. Load the raw messages straight into Cloud SQL tables designed for each provider

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The Healthcare API ingests and stores healthcare standards natively, publishes change notifications, and works with de-identification and BigQuery export. Custom parsers add the administration cost the case wants to reduce.
</details>

### Question 93
**Scenario:** EHR's compliance lead asks what is needed to run protected health information on Google Cloud under HIPAA. What is the best answer?

A. Nothing extra: Google Cloud holds a HIPAA certification, so every workload on it is compliant
B. Encrypt health data with an application-level key stored in the code repository
C. Keep all health data on-premises and move only the non-clinical applications to Google Cloud
D. Sign the BAA, use covered products for PHI, add VPC SC, CMEK, audit logs and least privilege

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** There is no HIPAA certification. Compliance is shared: the BAA covers specific products, and the customer configures the controls. Keeping everything on-premises contradicts the case, which chose Google Cloud to replace colocation.
</details>

### Question 94
**Scenario:** EHR wants to predict industry trends from provider data without exposing patient identities to analysts. What should they do?

A. Grant the analysts read access to the production FHIR store so they work with complete data
B. De-identify into a separate BigQuery dataset, then use BigQuery ML and Looker
C. Email weekly extracts of provider data to the analytics team as encrypted spreadsheets
D. Copy the production data into a personal project where data scientists can build models freely

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** De-identification keeps the trend value and removes identities, and a separate dataset limits who sees what. BigQuery ML lets analysts build predictions in SQL. The other options spread PHI.
</details>

### Question 95
**Scenario:** EHR must reduce latency for customers in several countries while keeping its regional application design. What helps most?

A. A global external Application Load Balancer with regional backends, plus Cloud CDN
B. Move the application to one zonal VM with a much larger machine type and faster disks
C. Ask customers outside the home country to connect through a corporate VPN
D. DNS round-robin across the public IP addresses of servers in several regions

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The global load balancer uses one anycast IP, ends connections at Google's edge, and routes to the nearest healthy backend. Cloud CDN serves static assets from the edge. A bigger VM does nothing for distance.
</details>

### Question 96
**Scenario:** EHR must adapt its disaster recovery plan. The target for patient databases is an RPO of minutes and an RTO under an hour if a region fails, at reasonable cost. What fits?

A. Nightly exports of each database to a Cloud Storage bucket in the same region
B. Active-active multi-region Spanner for every database, including the small internal ones
C. Cloud SQL HA plus a cross-region read replica to promote, and backups
D. No separate DR design, because the 99.9% availability target already covers a regional failure

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** HA covers zone failures, and a cross-region replica gives minute-level RPO and a fast promotion for regional failure. Same-region exports lose the region with the data. Multi-region Spanner everywhere costs far more than these targets need.
</details>

### Question 97
**Scenario:** Outages were caused by systems that were configured differently by hand. EHR also needs to dynamically scale and provision new environments. What practice fits?

A. A wiki page listing the manual steps to build each environment, kept up to date by the platform team
B. Clone production for each new environment by copying its VM disks and editing the settings
C. Let each team create and configure its own projects freely, with a monthly review
D. Terraform modules in a CI pipeline with policy checks, so every environment comes from reviewed code

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Reviewed, repeatable code produces identical environments on demand and stops drift. Policy checks catch unsafe changes before they apply. Manual steps are the cause of the outages in the executive statement.
</details>

### Question 98
**Scenario:** Traffic spikes have caused outages. Customer-facing apps run on GKE. What should EHR add?

A. Horizontal Pod Autoscaling plus the cluster autoscaler (or Autopilot), tuned by load tests
B. Fixed-size clusters sized for average traffic, with an on-call engineer adding nodes during spikes
C. Return errors to some requests during spikes with a rate limit on the load balancer
D. Replace the node pool with a single much larger node to handle the peak

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Pods and nodes then scale with demand, which addresses the capacity outages. Load testing makes sure the scaling settings are right. Sizing for the average fails at the peak.
</details>

### Question 99
**Scenario:** Millions of vehicles send telemetry, but rural connectivity drops for hours. KnightMotives must not lose data. What ingestion design fits?

A. Vehicles call a REST API synchronously and drop readings when the call fails
B. Each vehicle streams directly into BigQuery with no local buffer, retrying three times
C. Buffer on the vehicle, upload to Pub/Sub when connected, Dataflow into Bigtable and BigQuery
D. Send compressed telemetry by SMS to a gateway at headquarters that forwards it to the cloud

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Store and forward on the vehicle survives outages. Pub/Sub absorbs bursts when many cars reconnect at once. Dataflow handles late and out-of-order data, Bigtable serves the high-volume telemetry, and BigQuery holds it for analytics.
</details>

### Question 100
**Scenario:** New in-vehicle AI features must work in real time even in rural areas with no signal. Where should inference run?

A. Only in a Google Cloud region, called from the vehicle over the cellular network
B. On the vehicle with a compact model, updated from the cloud when connected
C. On servers installed at each dealership, reached over the dealer's local network
D. On the mainframe at headquarters, through a new API exposed to the vehicles

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Real-time features cannot depend on a link that is often down, so inference runs at the edge. The cloud trains and distributes models and collects data when a connection exists. Dealers have no budget for equipment.
</details>

### Question 101
**Scenario:** The supply chain runs on an outdated mainframe and the ERP makes promotions hard to launch. KnightMotives wants to modernize gradually. What is the best first step?

A. Rewrite the mainframe in one big-bang project and switch over on a single weekend
B. Freeze all changes to the supply chain until a new ERP has been selected and bought
C. Lift the mainframe workload as-is onto a single large Compute Engine VM
D. Apigee in front of the mainframe and ERP, data to BigQuery, replace functions one at a time

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** An API facade lets new apps use legacy functions now, and data replication unlocks analytics. Pieces can then be replaced one by one (strangler pattern), which matches the requirement to modernize gradually. A big-bang rewrite is the highest risk.
</details>

### Question 102
**Scenario:** The online build-to-order system is unreliable, and dealers in many countries need accurate, consistent inventory and orders. What fits best?

A. A stateless, autoscaled front end on Cloud Run or GKE with Spanner for orders and inventory
B. One Cloud SQL instance in a single zone without HA, with daily backups
C. A shared spreadsheet that dealers and the factory update with each order
D. Separate databases per country, synchronized with each other in a nightly batch

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Spanner gives strongly consistent, highly available transactions across regions, so dealers see the same inventory. The autoscaled front end handles peaks. Nightly sync creates the stale data that strains the dealer relationship.
</details>

### Question 103
**Scenario:** After past data breaches, KnightMotives needs centralized threat detection across its cloud estate and a tested incident response process. What should they adopt?

A. Antivirus and disk encryption on every employee laptop, managed from a central console
B. Security Command Center, Google SecOps SIEM/SOAR playbooks, incident drills and training
C. Turn off Data Access audit logs to reduce noise so analysts can focus on real alerts
D. Add a firewall rule that denies all ingress traffic to every project

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** This covers the case's three security asks: a framework for detection, an incident response plan run through playbooks, and awareness training. Disabling logs removes the evidence needed for detection and response.
</details>

### Question 104
**Scenario:** Data for the emerging autonomous platform must stay in the EU, and no team should be able to create resources elsewhere by mistake. What enforces this?

A. A written data residency policy on the internal wiki that teams must acknowledge
B. A label on each resource that marks it as EU data, checked in a quarterly audit
C. Org policy resource locations constraint (EU only) on the folder, with Assured Workloads
D. Ask engineers to choose an EU region in the console each time they create a resource

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** An organization policy blocks resource creation outside allowed locations for the whole folder, and Assured Workloads adds data-residency and personnel controls. Labels and wiki pages enforce nothing.
</details>

### Question 105
**Scenario:** Manufacturing plants need better connectivity to headquarters and to Google Cloud. Several plants are in places where only carriers reach. What fits?

A. Partner Interconnect per plant, with Network Connectivity Center as the hub
B. A consumer broadband line at each plant, with no backup connection
C. Dedicated Interconnect at every plant, including plants far from any Google facility
D. Ship hard drives from each plant to headquarters every day for upload

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Partner Interconnect works where you cannot reach a Google colocation facility, and Network Connectivity Center joins many sites in a hub-and-spoke design. Dedicated Interconnect needs a physical presence in a supported facility.
</details>

### Question 106
**Scenario:** Some KnightMotives applications already run on another major public cloud and must reach Google Cloud privately at high bandwidth. What should they use?

A. Route all traffic from the other cloud through the headquarters data center and its Interconnect
B. Connect over the public internet with TLS between the two clouds' public endpoints
C. Classic VPN tunnels with static routes between the two clouds
D. Cross-Cloud Interconnect between Google Cloud and the other provider

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Cross-Cloud Interconnect is a dedicated physical link between Google and another cloud, with no on-prem hop. Routing through HQ adds latency and makes HQ a single point of failure.
</details>

### Question 107
**Scenario:** Dealer staff and employees need access to internal web tools from anywhere. After past breaches, KnightMotives wants no broad VPN access and wants device checks. What fits?

A. A shared VPN account for all dealer staff, with the password changed each quarter
B. IAP with context-aware access (Chrome Enterprise Premium), using identity and device posture
C. Publish the tools on the internet and allow only the IP ranges of known dealerships
D. Remote desktop into a hardened jump host at headquarters, then open the tools from there

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Zero-trust access checks each request by user and device, and grants access per application instead of to the whole network. It works in a browser, so dealers need no new equipment. Shared VPN accounts are the kind of weakness that leads to breaches.
</details>

### Question 108
**Scenario:** KnightMotives' data is siloed across plants, vehicles and business units. Before monetizing it, they must know what data exists, who owns it and its quality, with strict privacy. What should they use?

A. Copy every dataset into one bucket with public read access so partners can find it
B. Track datasets, owners and quality in a shared spreadsheet maintained by each business unit
C. Let each business unit keep its own warehouse and sell its own data independently
D. Dataplex catalog, lineage and quality, with Sensitive Data Protection for de-identification

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Governance must come before monetization: Dataplex catalogs and governs data where it already lives, and Sensitive Data Protection finds and masks personal data. A public bucket breaks the security requirement.
</details>

### Question 109
**Scenario:** The autonomous simulation environment runs thousands of independent, restartable simulation jobs. Cost matters, since data monetization must fund new technology. What compute fits best?

A. On-demand VMs reserved for peak capacity all year so simulations never wait
B. Run the simulations on the existing on-premises mainframe during off-peak hours
C. Batch or GKE jobs on Spot VMs (GPUs where needed), with checkpointing
D. One very large VM that runs the simulation jobs one after another

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Independent, restartable jobs suit Spot capacity, which is far cheaper than on-demand. Checkpointing limits lost work when a VM is preempted. Reserving peak capacity all year wastes money.
</details>

---

## Answer Key

| Question | Answer | Domain |
|----------|--------|--------|
| 1 | A | Design/Plan Architecture |
| 2 | C | Design/Plan Architecture |
| 3 | C | Design/Plan Architecture |
| 4 | B | Design/Plan Architecture |
| 5 | C | Design/Plan Architecture |
| 6 | B | Design/Plan Architecture |
| 7 | A | Design/Plan Architecture |
| 8 | B | Design/Plan Architecture |
| 9 | B | Design/Plan Architecture |
| 10 | B | Design/Plan Architecture |
| 11 | A | Manage/Provision |
| 12 | B | Manage/Provision |
| 13 | A | Manage/Provision |
| 14 | B | Manage/Provision |
| 15 | D | Manage/Provision |
| 16 | B | Manage/Provision |
| 17 | D | Security/Compliance |
| 18 | D | Security/Compliance |
| 19 | D | Security/Compliance |
| 20 | D | Security/Compliance |
| 21 | D | Security/Compliance |
| 22 | D | Security/Compliance |
| 23 | D | Security/Compliance |
| 24 | A | Analyze/Optimize |
| 25 | B | Analyze/Optimize |
| 26 | C | Analyze/Optimize |
| 27 | C | Analyze/Optimize |
| 28 | B | Analyze/Optimize |
| 29 | A | Analyze/Optimize |
| 30 | B | Analyze/Optimize |
| 31 | A | Manage Implementation |
| 32 | B | Manage Implementation |
| 33 | D | Manage Implementation |
| 34 | D | Manage Implementation |
| 35 | B | Operations Excellence |
| 36 | B | Operations Excellence |
| 37 | B | Operations Excellence |
| 38 | A | Operations Excellence |
| 39 | D | Operations Excellence |
| 40 | D | Operations Excellence |
| 41 | D | Case study / AI / Ops |
| 42 | A | Case study / AI / Ops |
| 43 | A | Case study / AI / Ops |
| 44 | B | Case study / AI / Ops |
| 45 | B | Case study / AI / Ops |
| 46 | B | Case study / AI / Ops |
| 47 | A | Case study / AI / Ops |
| 48 | A | Case study / AI / Ops |
| 49 | A | Case study / AI / Ops |
| 50 | A | Case study / AI / Ops |
| 51 | C | Case study / AI / Ops |
| 52 | B | Case study / AI / Ops |
| 53 | D | Case study / AI / Ops |
| 54 | B | Case study / AI / Ops |
| 55 | A | Case study / AI / Ops |
| 56 | D | Case study / AI / Ops |
| 57 | B | Case study / AI / Ops |
| 58 | A | Case study / AI / Ops |
| 59 | D | Case study / AI / Ops |
| 60 | C | Case study / AI / Ops |
| 61 | B | Case study / AI / Ops |
| 62 | D | Case study / AI / Ops |
| 63 | D | Case study / AI / Ops |
| 64 | B | Case study / AI / Ops |
| 65 | B | Case study / AI / Ops |
| 66 | B | Case study / AI / Ops |
| 67 | B | Case study: Altostrat Media |
| 68 | D | Case study: Altostrat Media |
| 69 | B | Case study: Altostrat Media |
| 70 | D | Case study: Altostrat Media |
| 71 | C | Case study: Altostrat Media |
| 72 | A | Case study: Altostrat Media |
| 73 | D | Case study: Altostrat Media |
| 74 | B | Case study: Altostrat Media |
| 75 | C | Case study: Altostrat Media |
| 76 | A | Case study: Altostrat Media |
| 77 | B | Case study: Altostrat Media |
| 78 | B | Case study: Cymbal Retail |
| 79 | D | Case study: Cymbal Retail |
| 80 | A | Case study: Cymbal Retail |
| 81 | B | Case study: Cymbal Retail |
| 82 | C | Case study: Cymbal Retail |
| 83 | D | Case study: Cymbal Retail |
| 84 | A | Case study: Cymbal Retail |
| 85 | C | Case study: Cymbal Retail |
| 86 | D | Case study: Cymbal Retail |
| 87 | A | Case study: Cymbal Retail |
| 88 | B | Case study: Cymbal Retail |
| 89 | D | Case study: EHR Healthcare |
| 90 | C | Case study: EHR Healthcare |
| 91 | A | Case study: EHR Healthcare |
| 92 | B | Case study: EHR Healthcare |
| 93 | D | Case study: EHR Healthcare |
| 94 | B | Case study: EHR Healthcare |
| 95 | A | Case study: EHR Healthcare |
| 96 | C | Case study: EHR Healthcare |
| 97 | D | Case study: EHR Healthcare |
| 98 | A | Case study: EHR Healthcare |
| 99 | C | Case study: KnightMotives Automotive |
| 100 | B | Case study: KnightMotives Automotive |
| 101 | D | Case study: KnightMotives Automotive |
| 102 | A | Case study: KnightMotives Automotive |
| 103 | B | Case study: KnightMotives Automotive |
| 104 | C | Case study: KnightMotives Automotive |
| 105 | A | Case study: KnightMotives Automotive |
| 106 | D | Case study: KnightMotives Automotive |
| 107 | B | Case study: KnightMotives Automotive |
| 108 | D | Case study: KnightMotives Automotive |
| 109 | C | Case study: KnightMotives Automotive |
