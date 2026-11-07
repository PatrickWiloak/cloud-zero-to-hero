---
last-updated: 2026-05-03
---

# 📖 Cloud Glossary

> **Cloud, DevOps, networking and observability terms, plus the security, data and AI vocabulary cloud work runs into - in plain English.** For depth on those three, see [Security](https://security.noblerworks.com/), [Data](https://data.noblerworks.com/) and [AI](https://ai.noblerworks.com/) Zero to Hero.
>
> Use Ctrl+F. This is a reference doc, not something to read end-to-end.

Categories:
- [Cloud Fundamentals](#cloud-fundamentals)
- [AWS](#aws)
- [Microsoft Azure](#microsoft-azure)
- [Google Cloud (GCP)](#google-cloud-gcp)
- [Networking](#networking)
- [Security & Identity](#security--identity)
- [DevOps & Infrastructure as Code](#devops--infrastructure-as-code)
- [Containers & Kubernetes](#containers--kubernetes)
- [Data & Databases](#data--databases)
- [AI / Machine Learning](#ai--machine-learning)
- [LLMs & Generative AI](#llms--generative-ai)
- [Observability](#observability)

---

## Cloud Fundamentals

<a id="term-availability-zone-az"></a>**Availability Zone (AZ)** - A physically separate datacenter (or cluster) inside a cloud region. AZs in the same region are connected by low-latency links. You spread workloads across AZs to survive a single datacenter failure.

<a id="term-bare-metal"></a>**Bare metal** - A physical server you rent, no hypervisor, no virtualization layer. Used when you need maximum performance or specific hardware.

<a id="term-cloud-computing"></a>**Cloud computing** - On-demand delivery of compute, storage, networking, and software over the internet, billed by usage instead of owned outright.

<a id="term-cold-storage"></a>**Cold storage** - Cheap, slow storage for data you rarely access (archives, backups, compliance retention). Examples: S3 Glacier, Azure Archive Blob, GCS Coldline.

<a id="term-compute"></a>**Compute** - Anything that runs code: VMs, containers, serverless functions, batch jobs.

<a id="term-edge-edge-computing"></a>**Edge / Edge computing** - Compute that runs close to the user (CDN points of presence, local devices) instead of in a central region. Lower latency for end users.

<a id="term-elasticity"></a>**Elasticity** - The ability to automatically scale resources up and down based on demand. Distinguished from "scalability" (which just means "can grow").

<a id="term-hybrid-cloud"></a>**Hybrid cloud** - Mixing on-premises infrastructure with public cloud, with networking and identity that span both.

<a id="term-hypervisor"></a>**Hypervisor** - The software layer that runs VMs on physical hardware. Examples: KVM, Xen, Hyper-V, VMware ESXi.

<a id="term-iaas-infrastructure-as-a-service"></a>**IaaS (Infrastructure as a Service)** - You rent raw VMs, networks, and storage. You manage the OS and everything above it. Examples: EC2, Azure VMs, GCE.

<a id="term-landing-zone"></a>**Landing zone** - The pre-built, governed starting point for a cloud estate: the accounts, identity, networking, logging and guardrails that exist before the first application arrives. See [Multi-account strategy and landing zones](concepts/multi-account-and-landing-zones.md).

<a id="term-multi-cloud"></a>**Multi-cloud** - Using two or more public clouds (AWS + GCP, Azure + AWS, etc.) for workloads. Different from hybrid (which mixes on-prem and cloud).

<a id="term-multi-tenant"></a>**Multi-tenant** - A single instance of software/infrastructure serves many customers, with isolation between them. Most SaaS is multi-tenant.

<a id="term-on-premises-on-prem"></a>**On-premises (on-prem)** - Infrastructure you own and run in your own datacenter (or office closet).

<a id="term-paas-platform-as-a-service"></a>**PaaS (Platform as a Service)** - Provider manages OS, runtime, scaling. You deploy code. Examples: Heroku, Elastic Beanstalk, App Engine, Render.

<a id="term-private-cloud"></a>**Private cloud** - Cloud-style infrastructure dedicated to a single organization, often on-prem or in a colo.

<a id="term-public-cloud"></a>**Public cloud** - Multi-tenant cloud run by a hyperscaler (AWS, Azure, GCP, Oracle, IBM).

<a id="term-region"></a>**Region** - A geographic area (e.g., us-east-1, eu-west-2) containing multiple AZs. Latency between regions is high; you typically deploy per region.

<a id="term-reserved-instance-reservation-committed-use-discount"></a>**Reserved Instance / Reservation / Committed Use Discount** - Pre-pay or commit to using a resource for 1-3 years in exchange for a big discount.

<a id="term-rpo-recovery-point-objective"></a>**RPO (Recovery Point Objective)** - How much data you can afford to lose after a disaster, measured as time back to the last recoverable point. See [Disaster recovery: RPO and RTO](concepts/disaster-recovery-rpo-rto.md).

<a id="term-rto-recovery-time-objective"></a>**RTO (Recovery Time Objective)** - How long you can afford to be down after a disaster before service is restored.

<a id="term-saas-software-as-a-service"></a>**SaaS (Software as a Service)** - You use software over the internet; provider runs everything. Examples: Gmail, Salesforce, Slack, Notion.

<a id="term-serverless"></a>**Serverless** - You write code; the platform runs it on demand and bills per execution. No servers for you to manage. Examples: Lambda, Cloud Functions, Cloud Run, Azure Functions.

<a id="term-shared-responsibility-model"></a>**Shared responsibility model** - The cloud provider secures the cloud; you secure what you put **in** the cloud. Where the line is depends on the service (more services managed = less for you).

<a id="term-spof-single-point-of-failure"></a>**SPOF (Single Point of Failure)** - Anything that, if it breaks, takes the whole system down. Remove them by having more than one of everything that matters. See [High availability and fault tolerance](concepts/high-availability-and-fault-tolerance.md).

<a id="term-spot-preemptible-instance"></a>**Spot / Preemptible Instance** - A cheap VM the provider can reclaim with little notice. Good for fault-tolerant batch work, bad for stateful production.

<a id="term-tenancy"></a>**Tenancy** - Whether your resources share hardware with others (shared tenancy) or run on dedicated hardware (dedicated tenancy).

<a id="term-virtual-machine-vm"></a>**Virtual machine (VM)** - A simulated computer running on shared physical hardware via a hypervisor.

<a id="term-workload"></a>**Workload** - Any application, service, or batch job running in the cloud. Cloud architects love this word.

---

## AWS

<a id="term-alb-application-load-balancer"></a>**ALB (Application Load Balancer)** - Layer 7 (HTTP/HTTPS) load balancer. Routes by path, host, headers.

<a id="term-ami-amazon-machine-image"></a>**AMI (Amazon Machine Image)** - A snapshot/template of a VM disk used to launch EC2 instances.

<a id="term-athena"></a>**Athena** - Serverless SQL queries over data in S3.

<a id="term-aws"></a>**AWS** - Amazon Web Services. The largest public cloud.

<a id="term-cloudformation"></a>**CloudFormation** - AWS's native infrastructure-as-code tool. JSON or YAML templates.

<a id="term-cloudfront"></a>**CloudFront** - AWS's content delivery network (CDN).

<a id="term-cloudtrail"></a>**CloudTrail** - Logs every API call made in your AWS account. Audit trail.

<a id="term-cloudwatch"></a>**CloudWatch** - Metrics, logs, and alarms.

<a id="term-dynamodb"></a>**DynamoDB** - Managed key-value / document NoSQL database. Single-digit-millisecond reads at any scale.

<a id="term-ebs-elastic-block-store"></a>**EBS (Elastic Block Store)** - Block storage volumes attached to EC2 instances. Like a virtual hard drive.

<a id="term-ec2-elastic-compute-cloud"></a>**EC2 (Elastic Compute Cloud)** - AWS's VM service.

<a id="term-ecs-elastic-container-service"></a>**ECS (Elastic Container Service)** - AWS's container orchestrator. Simpler than EKS; AWS-flavored.

<a id="term-eks-elastic-kubernetes-service"></a>**EKS (Elastic Kubernetes Service)** - Managed Kubernetes on AWS.

<a id="term-elasticache"></a>**ElastiCache** - Managed Redis or Memcached.

<a id="term-fargate"></a>**Fargate** - Serverless compute for containers. Run ECS or EKS pods without managing nodes.

<a id="term-iam-identity-and-access-management"></a>**IAM (Identity and Access Management)** - AWS's permissions system. Users, roles, policies.

<a id="term-kinesis"></a>**Kinesis** - Streaming data service. Kinesis Data Streams = Kafka-like; Firehose = ingest to S3/Redshift; Analytics = SQL on streams.

<a id="term-lambda"></a>**Lambda** - AWS's serverless function service.

<a id="term-nlb-network-load-balancer"></a>**NLB (Network Load Balancer)** - Layer 4 (TCP/UDP) load balancer. Faster, fewer features than ALB.

<a id="term-rds-relational-database-service"></a>**RDS (Relational Database Service)** - Managed Postgres, MySQL, MariaDB, SQL Server, Oracle.

<a id="term-route-53"></a>**Route 53** - AWS's DNS service.

<a id="term-s3-simple-storage-service"></a>**S3 (Simple Storage Service)** - Object storage. The most fundamental AWS service.

<a id="term-sns-simple-notification-service"></a>**SNS (Simple Notification Service)** - Pub/sub messaging.

<a id="term-sqs-simple-queue-service"></a>**SQS (Simple Queue Service)** - Message queue.

<a id="term-vpc-virtual-private-cloud"></a>**VPC (Virtual Private Cloud)** - Your own isolated network in AWS.

---

## Microsoft Azure

<a id="term-aks-azure-kubernetes-service"></a>**AKS (Azure Kubernetes Service)** - Managed Kubernetes on Azure.

<a id="term-app-service"></a>**App Service** - PaaS for web apps and APIs. Easier than Kubernetes; less flexible.

<a id="term-arm-azure-resource-manager"></a>**ARM (Azure Resource Manager)** - The deployment and management layer for Azure. Templates are like CloudFormation.

<a id="term-azure"></a>**Azure** - Microsoft's public cloud.

<a id="term-azure-ad-entra-id"></a>**Azure AD / Entra ID** - Microsoft's cloud identity provider. Used for SSO, B2B, B2C, conditional access.

<a id="term-azure-devops"></a>**Azure DevOps** - CI/CD, repos, boards, artifacts. The Azure-flavored GitHub.

<a id="term-azure-functions"></a>**Azure Functions** - Serverless functions on Azure.

<a id="term-bicep"></a>**Bicep** - A friendlier DSL that compiles to ARM templates.

<a id="term-blob-storage"></a>**Blob Storage** - Azure's object storage (equivalent to S3).

<a id="term-cosmos-db"></a>**Cosmos DB** - Globally-distributed multi-model database. NoSQL, document, graph, key-value, all in one.

<a id="term-event-grid-event-hubs-service-bus"></a>**Event Grid / Event Hubs / Service Bus** - Azure's three messaging services. Event Grid = events, Event Hubs = high-throughput streaming, Service Bus = enterprise queues.

<a id="term-resource-group"></a>**Resource Group** - A logical container for related Azure resources. Permissions and lifecycle apply to the group.

<a id="term-subscription"></a>**Subscription** - A billing/permission boundary in Azure. You usually have several (dev, prod, etc.) under a tenant.

<a id="term-synapse-analytics"></a>**Synapse Analytics** - Azure's data warehouse + analytics platform.

<a id="term-tenant"></a>**Tenant** - The top-level identity boundary in Microsoft 365 / Azure (one per organization).

<a id="term-virtual-network-vnet"></a>**Virtual Network (VNet)** - Azure's equivalent of a VPC.

---

## Google Cloud (GCP)

<a id="term-bigquery"></a>**BigQuery** - GCP's serverless data warehouse. Pay per query and storage.

<a id="term-cloud-functions"></a>**Cloud Functions** - GCP's FaaS (function-as-a-service).

<a id="term-cloud-run"></a>**Cloud Run** - Run containers serverlessly on GCP. Scales to zero.

<a id="term-cloud-sql"></a>**Cloud SQL** - Managed Postgres, MySQL, SQL Server.

<a id="term-cloud-storage-gcs"></a>**Cloud Storage (GCS)** - GCP's object storage (equivalent to S3 / Blob).

<a id="term-dataflow"></a>**Dataflow** - Managed Apache Beam (stream + batch processing).

<a id="term-firestore"></a>**Firestore** - Serverless NoSQL document DB. Real-time client SDKs.

<a id="term-gce-google-compute-engine"></a>**GCE (Google Compute Engine)** - GCP's VM service.

<a id="term-gcp"></a>**GCP** - Google Cloud Platform.

<a id="term-gke-google-kubernetes-engine"></a>**GKE (Google Kubernetes Engine)** - Managed Kubernetes on GCP. The original; Google invented Kubernetes.

<a id="term-iam-gcp"></a>**IAM (GCP)** - Same name as AWS, different model. Roles attach to identities and apply to resources.

<a id="term-pubsub"></a>**Pub/Sub** - GCP's globally-distributed pub/sub messaging.

<a id="term-spanner"></a>**Spanner** - Globally-consistent relational database. Distributed but ACID.

<a id="term-vpc-gcp"></a>**VPC (GCP)** - GCP's virtual network. Notably, GCP VPCs are global (not regional like AWS).

<a id="term-vertex-ai"></a>**Vertex AI** - GCP's unified ML platform (training, deployment, AutoML, foundation models). Renamed the **Gemini Enterprise Agent Platform** ("Agent Platform") on 2026-04-22; Google's exam guides now use the new names. See the [rename table](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes).

---

## Networking

<a id="term-api-gateway"></a>**API Gateway** - A managed front door for APIs. Handles auth, rate limiting, routing, transforms.

<a id="term-asn-autonomous-system-number"></a>**ASN (Autonomous System Number)** - The unique ID for a network on the internet (used in BGP).

<a id="term-bgp-border-gateway-protocol"></a>**BGP (Border Gateway Protocol)** - The protocol the internet uses to route between networks.

<a id="term-cdn-content-delivery-network"></a>**CDN (Content Delivery Network)** - Edge cache for static (and sometimes dynamic) content. CloudFront, Cloud CDN, Azure CDN, Cloudflare, Fastly.

<a id="term-cidr-classless-inter-domain-routing"></a>**CIDR (Classless Inter-Domain Routing)** - The notation for IP ranges (e.g., `10.0.0.0/16`). The number after the slash is how many bits are fixed.

<a id="term-dns-domain-name-system"></a>**DNS (Domain Name System)** - Translates names (`example.com`) to IPs (`93.184.216.34`).

<a id="term-egress"></a>**Egress** - Traffic leaving your network/cloud. Often the part that costs money.

<a id="term-firewall"></a>**Firewall** - Filters traffic by rules. Cloud-native versions are usually called security groups, NACLs, or firewall policies.

<a id="term-httphttps"></a>**HTTP/HTTPS** - The protocols the web runs on. HTTPS = HTTP over TLS.

<a id="term-ingress"></a>**Ingress** - Traffic coming into your network. In Kubernetes, also a resource type that exposes services to the internet.

<a id="term-latency"></a>**Latency** - The time it takes a request to round-trip. Measured in milliseconds.

<a id="term-load-balancer"></a>**Load balancer** - Distributes incoming traffic across many backend servers.

<a id="term-nat-network-address-translation"></a>**NAT (Network Address Translation)** - Lets private IPs reach the internet by sharing a public IP.

<a id="term-osi-model"></a>**OSI model** - 7-layer abstraction for networking. Layer 4 = TCP/UDP, Layer 7 = HTTP. Not literally how things work, but useful vocabulary.

<a id="term-peering"></a>**Peering** - A direct network connection between two networks (VPCs, datacenters, ISPs).

<a id="term-private-link-private-endpoint"></a>**Private link / Private endpoint** - A way to access a managed service over a private IP without traversing the public internet.

<a id="term-public-ip"></a>**Public IP** - An IP routable on the internet. Public IPs are scarce (IPv4) and often cost money.

<a id="term-reverse-proxy"></a>**Reverse proxy** - A server that takes inbound requests and forwards them to backend services. Nginx, HAProxy, Envoy.

<a id="term-route-table"></a>**Route table** - Defines where packets go based on destination IP. Each subnet has one.

<a id="term-security-group"></a>**Security group** - A stateful firewall attached to a VM/pod/service. Rules are usually allow-only.

<a id="term-subnet"></a>**Subnet** - A subdivision of a VPC into a smaller IP range, typically scoped to one AZ.

<a id="term-tcpudp"></a>**TCP/UDP** - Transport protocols. TCP = reliable, ordered, connection-based. UDP = best-effort, fast, no connection.

<a id="term-tls-transport-layer-security"></a>**TLS (Transport Layer Security)** - The encryption protocol that powers HTTPS. SSL is the deprecated predecessor.

<a id="term-vpn-virtual-private-network"></a>**VPN (Virtual Private Network)** - Encrypted tunnel between networks (or a user and a network).

<a id="term-vpc-peering"></a>**VPC peering** - Connect two VPCs so they can route to each other. Non-transitive.

---

## Security & Identity

<a id="term-access-key"></a>**Access key** - A pair of credentials (key ID + secret) that authenticates programmatic access. Treat like a password.

<a id="term-acl-access-control-list"></a>**ACL (Access Control List)** - A list of rules saying who can do what to a resource.

<a id="term-api-key"></a>**API key** - A long token used to authenticate API calls. Less powerful than a credential pair; widely used for SaaS.

<a id="term-audit-log"></a>**Audit log** - A record of who did what, when. Required for most compliance frameworks.

<a id="term-authentication-authn"></a>**Authentication (AuthN)** - Proving who you are. (Username/password, MFA, SSO.)

<a id="term-authorization-authz"></a>**Authorization (AuthZ)** - What you're allowed to do once authenticated. (RBAC, ABAC, policies.)

<a id="term-bearer-token"></a>**Bearer token** - Anyone who holds it can use it. JWTs are typically bearer tokens.

<a id="term-certificate"></a>**Certificate** - A signed public key that proves identity. Used by TLS.

<a id="term-cia-triad"></a>**CIA triad** - Confidentiality, Integrity, Availability. The three goals of infosec.

<a id="term-cspm-cloud-security-posture-management"></a>**CSPM (Cloud Security Posture Management)** - Tools that scan your cloud for misconfigurations. Wiz, Prisma, AWS Security Hub.

<a id="term-encryption-at-rest"></a>**Encryption at rest** - Data on disk is encrypted. Decryption happens on read.

<a id="term-encryption-in-transit"></a>**Encryption in transit** - Data over the network is encrypted (typically TLS).

<a id="term-iam-identity-and-access-management"></a>**IAM (Identity and Access Management)** - Generic term for controlling who can do what. Each cloud has its own IAM service.

<a id="term-jwt-json-web-token"></a>**JWT (JSON Web Token)** - A signed JSON blob carrying claims (user ID, expiry, etc.). Common in API auth.

<a id="term-kms-key-management-service"></a>**KMS (Key Management Service)** - Cloud service for managing encryption keys. AWS KMS, Azure Key Vault, GCP KMS.

<a id="term-least-privilege"></a>**Least privilege** - Give an identity only the permissions it needs, no more.

<a id="term-mfa-multi-factor-authentication"></a>**MFA (Multi-Factor Authentication)** - Requires more than just a password (e.g., TOTP, hardware key, SMS).

<a id="term-oauth-20"></a>**OAuth 2.0** - The protocol that powers "Sign in with Google." Authorization framework.

<a id="term-oidc-openid-connect"></a>**OIDC (OpenID Connect)** - Authentication layer on top of OAuth 2.0. Adds identity tokens.

<a id="term-penetration-test-pentest"></a>**Penetration test (pentest)** - Authorized hacking. Hire someone to break in so you can fix it.

<a id="term-rbac-role-based-access-control"></a>**RBAC (Role-Based Access Control)** - Permissions are grouped into roles; you assign roles to users.

<a id="term-scp-service-control-policy"></a>**SCP (Service Control Policy)** - An AWS Organizations policy that sets the maximum permissions accounts can use. It never grants access; a user still needs an IAM allow and no SCP deny.

<a id="term-secret"></a>**Secret** - Sensitive data (passwords, API keys, certificates) stored separately from code.

<a id="term-secrets-manager"></a>**Secrets manager** - A service for storing and rotating secrets. AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, GCP Secret Manager.

<a id="term-service-account"></a>**Service account** - An identity that belongs to a service or app, not a human.

<a id="term-siem-security-information-and-event-management"></a>**SIEM (Security Information and Event Management)** - Aggregates logs and alerts on suspicious patterns. Splunk, Sentinel, Elastic SIEM.

<a id="term-sso-single-sign-on"></a>**SSO (Single Sign-On)** - Log in once, access many apps. Usually SAML or OIDC.

<a id="term-waf-web-application-firewall"></a>**WAF (Web Application Firewall)** - Filters HTTP requests for attacks (SQL injection, XSS, etc.).

<a id="term-zero-trust"></a>**Zero Trust** - Don't trust the network perimeter. Verify every request, regardless of source.

---

## DevOps & Infrastructure as Code

<a id="term-ansible"></a>**Ansible** - Agentless configuration management tool. YAML playbooks, runs over SSH.

<a id="term-artifact"></a>**Artifact** - The output of a build (a JAR, a Docker image, a binary). Stored in an artifact registry.

<a id="term-bluegreen-deployment"></a>**Blue/green deployment** - Two production environments (blue = current, green = new). Switch traffic once green is verified.

<a id="term-canary-deployment"></a>**Canary deployment** - Roll out a new version to a small percentage of users, watch metrics, expand if good.

<a id="term-cd-continuous-deployment"></a>**CD (Continuous Deployment)** - Every commit that passes tests goes to production. Automated end-to-end.

<a id="term-ci-continuous-integration"></a>**CI (Continuous Integration)** - Every commit triggers a build and test run. Catches regressions fast.

<a id="term-cicd-pipeline"></a>**CICD pipeline** - Automated workflow that builds, tests, and deploys code. GitHub Actions, GitLab CI, Jenkins, CircleCI.

<a id="term-docker"></a>**Docker** - The most common container runtime / image format.

<a id="term-drift"></a>**Drift** - When live infrastructure no longer matches what's in code. Bad. IaC tools detect it.

<a id="term-gitops"></a>**GitOps** - Git is the source of truth for infrastructure. Tools like ArgoCD or Flux sync the cluster to git.

<a id="term-golden-path"></a>**Golden path** - The supported, opinionated way to do a common task, such as creating a new service with pipeline, dashboards and alerts included. Also called a paved road. See [Platform engineering explained](concepts/platform-engineering-explained.md).

<a id="term-iac-infrastructure-as-code"></a>**IaC (Infrastructure as Code)** - Define infrastructure in text files, version it, deploy it. Terraform, CloudFormation, Bicep, Pulumi.

<a id="term-idempotent"></a>**Idempotent** - Running the operation multiple times produces the same result. IaC tools rely on this.

<a id="term-immutable-infrastructure"></a>**Immutable infrastructure** - Servers are never modified after deploy. To "update," you replace.

<a id="term-pulumi"></a>**Pulumi** - IaC using real programming languages (TypeScript, Python, Go).

<a id="term-rolling-deployment"></a>**Rolling deployment** - Replace instances gradually rather than all at once.

<a id="term-sre-site-reliability-engineering"></a>**SRE (Site Reliability Engineering)** - Google-coined discipline for running production. SLOs, error budgets, postmortems.

<a id="term-terraform"></a>**Terraform** - The dominant IaC tool. HCL syntax, multi-cloud, state-driven.

<a id="term-terragrunt"></a>**Terragrunt** - A wrapper around Terraform for managing many environments / modules.

---

## Containers & Kubernetes

<a id="term-container"></a>**Container** - A packaged app + dependencies that runs in an isolated process. Lighter than a VM, heavier than a function.

<a id="term-container-registry"></a>**Container registry** - Where Docker images live. Docker Hub, ECR, GCR/Artifact Registry, ACR.

<a id="term-configmap"></a>**ConfigMap** - A Kubernetes object holding non-secret config. Mount as files or env vars.

<a id="term-crd-custom-resource-definition"></a>**CRD (Custom Resource Definition)** - Lets you extend Kubernetes with your own resource types.

<a id="term-deployment"></a>**Deployment** - Kubernetes resource that manages replica sets and rolling updates.

<a id="term-helm"></a>**Helm** - The package manager for Kubernetes. Charts = templated manifests.

<a id="term-image"></a>**Image** - A built container blueprint. You run an image, you get a container.

<a id="term-ingress"></a>**Ingress** - A Kubernetes resource that exposes HTTP services to the outside world. Backed by an ingress controller (Nginx, Traefik, etc.).

<a id="term-kubernetes-k8s"></a>**Kubernetes (K8s)** - Open-source container orchestrator. Schedules pods across nodes, restarts failures, handles networking and storage.

<a id="term-kustomize"></a>**Kustomize** - Built-in Kubernetes templating without Helm. Layer-based overlays.

<a id="term-manifest"></a>**Manifest** - A YAML file describing a Kubernetes resource.

<a id="term-namespace"></a>**Namespace** - A logical partition inside a cluster. Used for tenancy, RBAC, and resource quotas.

<a id="term-node"></a>**Node** - A worker machine in a Kubernetes cluster. Runs pods.

<a id="term-operator"></a>**Operator** - A custom controller that automates managing a stateful app (databases, caches) on Kubernetes.

<a id="term-pod"></a>**Pod** - The smallest deployable unit in Kubernetes. One or more containers sharing network and storage.

<a id="term-replica"></a>**Replica** - One copy of a pod. Deployments manage replicas.

<a id="term-secret-kubernetes"></a>**Secret (Kubernetes)** - Like a ConfigMap but for sensitive data. Base64-encoded by default (not actually encrypted).

<a id="term-service-kubernetes"></a>**Service (Kubernetes)** - A stable network endpoint that routes to pods. ClusterIP, NodePort, LoadBalancer.

<a id="term-service-mesh"></a>**Service mesh** - Layer that adds traffic management, security, and observability to service-to-service calls. Istio, Linkerd, Consul.

<a id="term-statefulset"></a>**StatefulSet** - Like a Deployment but for stateful apps. Stable identities, persistent storage.

<a id="term-sidecar"></a>**Sidecar** - A second container in a pod that augments the main one (logging, proxy, etc.).

---

## Data & Databases

<a id="term-acid"></a>**ACID** - Atomicity, Consistency, Isolation, Durability. The promises of traditional relational databases.

<a id="term-base"></a>**BASE** - Basically Available, Soft state, Eventual consistency. The relaxed promises of many NoSQL systems.

<a id="term-columnar-storage"></a>**Columnar storage** - Data on disk is organized by column, not row. Great for analytics. Used by data warehouses.

<a id="term-data-lake"></a>**Data lake** - A bunch of raw files in object storage. Schema-on-read.

<a id="term-data-lakehouse"></a>**Data lakehouse** - Lake + warehouse hybrid. Open table formats (Delta, Iceberg, Hudi) on object storage with warehouse-like queries.

<a id="term-data-warehouse"></a>**Data warehouse** - Optimized for analytical queries over large datasets. BigQuery, Redshift, Snowflake, Synapse.

<a id="term-document-db"></a>**Document DB** - Stores JSON-like documents. MongoDB, Firestore, DynamoDB (sort of).

<a id="term-etl-elt"></a>**ETL / ELT** - Extract, Transform, Load (transform before loading) vs Extract, Load, Transform (load raw, transform inside the warehouse). ELT is increasingly common.

<a id="term-eventual-consistency"></a>**Eventual consistency** - Reads might be stale right after a write but will eventually catch up.

<a id="term-graph-db"></a>**Graph DB** - Stores nodes and edges. Neo4j, Neptune, ArangoDB.

<a id="term-index"></a>**Index** - A separate data structure that makes queries faster. Costs disk and write speed.

<a id="term-key-value-store"></a>**Key-value store** - Simplest DB model. Get/put by key. Redis, DynamoDB, etcd.

<a id="term-nosql"></a>**NoSQL** - Anything that isn't a traditional SQL relational database. Document, key-value, graph, time-series, etc.

<a id="term-olap-online-analytical-processing"></a>**OLAP (Online Analytical Processing)** - Big aggregate queries over historical data. Warehouses.

<a id="term-oltp-online-transaction-processing"></a>**OLTP (Online Transaction Processing)** - Fast, small transactions. Operational databases.

<a id="term-orm-object-relational-mapper"></a>**ORM (Object-Relational Mapper)** - Library that maps DB rows to objects in your code. SQLAlchemy, Prisma, ActiveRecord.

<a id="term-relational-db"></a>**Relational DB** - Tables with rows and columns, joined via keys. Postgres, MySQL, SQL Server, Oracle.

<a id="term-replica"></a>**Replica** - A read-only copy of a database for scaling reads or disaster recovery.

<a id="term-schema"></a>**Schema** - The structure of your data (tables, columns, types).

<a id="term-sharding"></a>**Sharding** - Splitting a dataset across multiple servers based on a key.

<a id="term-time-series-db"></a>**Time-series DB** - Optimized for timestamped data. InfluxDB, TimescaleDB, Prometheus.

<a id="term-transaction"></a>**Transaction** - A group of operations that succeed or fail together.

<a id="term-vector-database"></a>**Vector database** - Stores high-dimensional vectors (embeddings) for similarity search. Pinecone, Weaviate, pgvector, Qdrant, Milvus.

---

## AI / Machine Learning

<a id="term-algorithm-ml"></a>**Algorithm (ML)** - The recipe used to learn from data. Linear regression, decision trees, neural networks.

<a id="term-bias-ml"></a>**Bias (ML)** - Systematic error from a model. Often means the model unfairly favors some groups.

<a id="term-classification"></a>**Classification** - Predicting a discrete label (spam / not spam).

<a id="term-clustering"></a>**Clustering** - Unsupervised grouping of similar items.

<a id="term-cross-validation"></a>**Cross-validation** - Splitting your training data multiple ways to check that performance generalizes.

<a id="term-dataset"></a>**Dataset** - The collection of examples a model learns from.

<a id="term-deep-learning"></a>**Deep learning** - ML using neural networks with many layers.

<a id="term-epoch"></a>**Epoch** - One pass over the training set.

<a id="term-feature"></a>**Feature** - An input variable used by a model.

<a id="term-feature-engineering"></a>**Feature engineering** - Crafting input variables to make a model learn better.

<a id="term-gpu-graphics-processing-unit"></a>**GPU (Graphics Processing Unit)** - Originally for graphics, now the workhorse of ML training. Massively parallel.

<a id="term-gradient-descent"></a>**Gradient descent** - The optimization algorithm at the core of most neural network training.

<a id="term-hyperparameter"></a>**Hyperparameter** - A setting you choose before training (learning rate, batch size, etc.). Distinguished from learned parameters (weights).

<a id="term-inference"></a>**Inference** - Running a trained model on new data to get predictions. Distinguished from training.

<a id="term-label"></a>**Label** - The correct answer for a training example. Used in supervised learning.

<a id="term-loss-function"></a>**Loss function** - Measures how wrong the model's predictions are. Training minimizes this.

<a id="term-ml-machine-learning"></a>**ML (Machine Learning)** - Algorithms that improve with data, instead of being explicitly programmed.

<a id="term-model"></a>**Model** - The output of training. Takes inputs, gives predictions.

<a id="term-neural-network"></a>**Neural network** - A model loosely inspired by neurons. Weighted connections in layers.

<a id="term-overfitting"></a>**Overfitting** - Model memorizes training data and performs badly on new data.

<a id="term-regression"></a>**Regression** - Predicting a continuous number (price, temperature).

<a id="term-reinforcement-learning"></a>**Reinforcement learning** - Agent learns by acting in an environment and getting rewards. AlphaGo, robotics, game AI.

<a id="term-supervised-learning"></a>**Supervised learning** - Training on labeled examples.

<a id="term-tpu-tensor-processing-unit"></a>**TPU (Tensor Processing Unit)** - Google's custom chip for ML. Comparable to a GPU.

<a id="term-training"></a>**Training** - Adjusting model weights based on data to minimize loss.

<a id="term-underfitting"></a>**Underfitting** - Model is too simple to capture the pattern.

<a id="term-unsupervised-learning"></a>**Unsupervised learning** - Finding structure in unlabeled data (clustering, dimensionality reduction).

<a id="term-validation-set"></a>**Validation set** - Held-out data used during training to tune hyperparameters.

---

## LLMs & Generative AI

<a id="term-agent-ai"></a>**Agent (AI)** - An LLM-powered system that can take actions (call tools, read files, send messages) toward a goal.

<a id="term-attention"></a>**Attention** - The core mechanism in transformers. Lets each token "look at" other tokens when computing its representation.

<a id="term-benchmark"></a>**Benchmark** - A standard test for models. MMLU, HumanEval, SWE-bench, GSM8K, etc.

<a id="term-chain-of-thought-cot"></a>**Chain-of-thought (CoT)** - Asking the model to "think step by step" before answering. Often improves reasoning.

<a id="term-chunking"></a>**Chunking** - Splitting documents into smaller pieces for embedding / retrieval. Bad chunking ruins RAG.

<a id="term-claude"></a>**Claude** - Anthropic's family of LLMs (Haiku, Sonnet, Opus).

<a id="term-context-window"></a>**Context window** - The max number of tokens the model can consider at once. Bigger = more text in, but slower and more expensive.

<a id="term-distillation"></a>**Distillation** - Training a smaller model to mimic a larger one.

<a id="term-embedding"></a>**Embedding** - A vector that represents the meaning of text (or images, audio). Similar meanings = nearby vectors.

<a id="term-eval"></a>**Eval** - Automated test of model quality. Can be deterministic (does it match a regex?) or model-graded.

<a id="term-fine-tuning"></a>**Fine-tuning** - Continuing training of a base model on your own data to specialize it.

<a id="term-foundation-model"></a>**Foundation model** - A large, general-purpose model trained on broad data. GPT, Claude, Gemini, Llama.

<a id="term-function-calling-tool-use"></a>**Function calling / Tool use** - The model returns a structured request to invoke a function, then resumes once the result is fed back in.

<a id="term-generative-ai-genai"></a>**Generative AI (GenAI)** - Models that generate new content (text, images, audio, video) instead of classifying.

<a id="term-gpt"></a>**GPT** - OpenAI's family of LLMs (GPT-3.5, 4, 4o, etc.). The first widely-known LLM.

<a id="term-grounding"></a>**Grounding** - Constraining a model's answers to verified sources (often via RAG).

<a id="term-hallucination"></a>**Hallucination** - When a model confidently makes up something false.

<a id="term-inference-cost"></a>**Inference cost** - Per-token (or per-second) cost of running a model. Often tracked as $/M tokens in/out.

<a id="term-langchain-llamaindex"></a>**LangChain / LlamaIndex** - Frameworks for building LLM apps. LangChain = general orchestration, LlamaIndex = retrieval-focused.

<a id="term-latent-space"></a>**Latent space** - The high-dimensional space embeddings live in.

<a id="term-llm-large-language-model"></a>**LLM (Large Language Model)** - A model trained on huge amounts of text to predict the next token.

<a id="term-lora-low-rank-adaptation"></a>**LoRA (Low-Rank Adaptation)** - Cheap fine-tuning by training only a small adapter, not the whole model.

<a id="term-mcp-model-context-protocol"></a>**MCP (Model Context Protocol)** - Anthropic's open protocol for connecting LLMs to tools and data sources.

<a id="term-multimodal"></a>**Multimodal** - Models that handle multiple input/output types (text + image, text + audio, etc.).

<a id="term-parameter"></a>**Parameter** - One of the learned numbers in a model. GPT-3 had 175B; modern flagship models can have hundreds of billions.

<a id="term-prompt"></a>**Prompt** - The text you give the model.

<a id="term-prompt-caching"></a>**Prompt caching** - Reusing a precomputed prompt prefix to save cost and latency. Anthropic and OpenAI both support it.

<a id="term-prompt-engineering"></a>**Prompt engineering** - The craft of writing prompts that get good outputs reliably.

<a id="term-prompt-injection"></a>**Prompt injection** - An attack where malicious text tells the model to ignore its instructions.

<a id="term-rag-retrieval-augmented-generation"></a>**RAG (Retrieval-Augmented Generation)** - Look up relevant documents, stuff them into the prompt, then generate. Standard pattern for "chat with your docs."

<a id="term-rlhf-reinforcement-learning-from-human-feedback"></a>**RLHF (Reinforcement Learning from Human Feedback)** - Training step where humans rank model outputs to teach it preferences.

<a id="term-reranker"></a>**Reranker** - A second-stage model that re-scores retrieved chunks for relevance.

<a id="term-sampling"></a>**Sampling** - The process of choosing the next token. Temperature, top-p, top-k are sampling parameters.

<a id="term-semantic-search"></a>**Semantic search** - Search by meaning, not keywords. Powered by embeddings.

<a id="term-sft-supervised-fine-tuning"></a>**SFT (Supervised Fine-Tuning)** - Fine-tuning on labeled examples.

<a id="term-system-prompt"></a>**System prompt** - Top-level instructions to the model. Sets the role/behavior.

<a id="term-temperature"></a>**Temperature** - Controls randomness in sampling. 0 = deterministic, higher = more varied.

<a id="term-token"></a>**Token** - The unit a model reads/writes. Usually ~4 characters of English. Costs are per-token.

<a id="term-tokenizer"></a>**Tokenizer** - Splits text into tokens. Different models use different tokenizers.

<a id="term-top-k-top-p-sampling"></a>**Top-k / Top-p sampling** - Restrict the model's choices to the most likely next tokens.

<a id="term-transformer"></a>**Transformer** - The neural network architecture behind nearly all modern LLMs. Introduced in "Attention Is All You Need" (2017).

<a id="term-vibe-coding"></a>**Vibe coding** - Writing software primarily by prompting an AI model rather than editing code yourself. Term popularized in 2025.

---

## Observability

<a id="term-alert"></a>**Alert** - A rule that fires when a metric crosses a threshold. Wakes someone up (or not).

<a id="term-apm-application-performance-monitoring"></a>**APM (Application Performance Monitoring)** - Tools that trace requests through your app and surface slowness. Datadog, New Relic, AppDynamics.

<a id="term-cardinality"></a>**Cardinality** - The number of unique label combinations on a metric. High cardinality = expensive metrics.

<a id="term-distributed-tracing"></a>**Distributed tracing** - Following a single request across many services. OpenTelemetry, Jaeger, Tempo, X-Ray.

<a id="term-error-budget"></a>**Error budget** - The amount of failure tolerated by an SLO. If you blow it, no risky deploys.

<a id="term-log"></a>**Log** - A timestamped text record of an event.

<a id="term-metric"></a>**Metric** - A numeric measurement over time (request count, error rate, latency).

<a id="term-observability"></a>**Observability** - The ability to understand what's happening inside a system from its outputs (logs, metrics, traces).

<a id="term-opentelemetry-otel"></a>**OpenTelemetry (OTel)** - The open standard for instrumenting apps with logs, metrics, and traces.

<a id="term-slo-service-level-objective"></a>**SLO (Service Level Objective)** - The target for a service's reliability (e.g., "99.9% of requests under 500ms").

<a id="term-span"></a>**Span** - One unit of work in a distributed trace.

<a id="term-trace"></a>**Trace** - The full journey of a request across services. Made up of spans.

---

## Want a term added?

Open an issue or PR. See [CONTRIBUTING.md](../CONTRIBUTING.md).
