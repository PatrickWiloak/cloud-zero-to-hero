---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 45 min
---

# Domain 1: Architecture Design and Implementation Built for the Cloud (25%)

## Overview

Domain 1 replaces C02's "Design Solutions for Organizational Complexity" (26 percent) and absorbs most of "Design for New Solutions" (29 percent). It is the broadest SAP-C03 domain with five tasks: **1.1** architectures built for the cloud, **1.2** (new) integrating AI and ML services, **1.3** hybrid cloud integration, **1.4** network architectures, **1.5** data, storage and database architectures. C03 consolidated several C02 tasks into 1.1 (event routing, stateless design, auto scaling, edge, event-driven design, container orchestration), 1.3 (data synchronization, legacy integration), 1.4 (VPC design, network security) and 1.5 (database scaling).

At professional level every question is a trade-off: several options work, and the right one best meets the stated constraints (latency, cost, operational burden, existing investments, compliance). Read for the constraint words.

**[📖 Exam guide: Content Domain 1](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/solutions-architect-professional-03-domain1.html)** - Official tasks and skills

## Task 1.1: Architectures built for the cloud

### Event-driven design and messaging guarantees

Pick the messaging service by the guarantees you need.

| Need | Choice | Notes |
|---|---|---|
| Buffer work, consumer pulls at its pace | SQS standard | At-least-once delivery, best-effort ordering: consumers must be **idempotent** |
| Strict ordering and deduplication | SQS FIFO | Ordering within a message group; lower throughput than standard unless high-throughput mode is used |
| Fan-out to many subscribers | SNS (optionally with SQS queues per subscriber) | Pairing SNS with queues gives each consumer its own buffer and retry |
| Content-based routing, SaaS and AWS events, schema registry | EventBridge | Rules match event patterns; **event buses** route across accounts and Regions |
| Ordered, replayable high-volume stream | Kinesis Data Streams | The **partition key** sets the shard and so the ordering scope; hot keys create hot shards |

Cross-account and cross-Region event routing (skill 1.1.5) uses EventBridge event buses with resource policies that allow other accounts to put events, and rules that forward events to a bus in another account or Region, so a central operations account can see events from many workload accounts.

### Stateless design and workflows

Stateless applications keep session and state outside the compute (DynamoDB, ElastiCache, S3), so any instance or function can serve any request and scaling or replacing capacity is trivial. For multi-step processes, **AWS Step Functions** provides durable orchestration with retries, error handling and waits; C03 also names **durable Lambda functions** for multi-step workflows with durable execution. Choose Step Functions **Standard** for long-running, auditable workflows (up to one year) and **Express** for high-volume, short-duration workflows.

Serverless data processing (1.1.3): Kinesis Data Streams ingests, AWS Glue transforms and catalogs, Athena queries data in S3 with SQL, and Lambda handles event-by-event processing.

### Containers, service communication and scaling

- **Orchestration** (1.1.6): ECS is AWS's simpler, AWS-native orchestrator; EKS is managed Kubernetes for teams that need Kubernetes APIs or portability; Fargate removes node management from both. Prefer Fargate unless you need specific instance types, GPUs, daemon sets or cost control from dense bin-packing.
- **Service mesh and discovery** (1.1.7, new): **Amazon VPC Lattice** is a managed application networking layer that connects services across VPCs and accounts with consistent auth policies and observability without running sidecars. **ECS Service Connect** gives ECS services service discovery, load balancing and metrics inside a namespace.
- **Image hygiene** (1.1.8, new): Amazon ECR can scan images for vulnerabilities and apply lifecycle policies to expire old images.
- **Auto scaling** (1.1.9): Lambda concurrency; on Kubernetes, the Horizontal Pod Autoscaler scales pods and the Cluster Autoscaler (or Karpenter) scales nodes; ECS service auto scaling and **AWS Application Auto Scaling** scale ECS services, DynamoDB capacity and other resources by target tracking, step or scheduled policies.
- **Ingress** (1.1.10, new): Application Load Balancer for HTTP/HTTPS with path and host routing, Network Load Balancer for TCP/UDP at high throughput and static IPs, the AWS Load Balancer Controller to provision them from Kubernetes Ingress and Service objects, and API Gateway when you need API management (throttling, keys, authorizers, request validation).
- **Edge** (1.1.11): CloudFront Functions for lightweight viewer request manipulation at very low latency; Lambda@Edge for heavier logic at CloudFront edge locations.
- **Real-time** (1.1.12, new): API Gateway **WebSocket APIs** keep a persistent two-way connection for chat and live updates; combine with publish-subscribe backends.
- **Multi-tenant** (1.1.13, new): the central choice is **silo** (separate resources per tenant: strongest isolation, highest cost) versus **pool** (shared resources with logical isolation, such as row-level security keyed by tenant id, tenant-specific encryption keys and tenant context in Cognito tokens: efficient, needs careful isolation controls). Many designs mix the two by tenant tier.

**[📖 What is Amazon VPC Lattice?](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html)** - Service networks, services and auth policies

## Task 1.2 (new): Integrate AI and ML services

The exam asks you to design, not to train. Out-of-scope per the guide: model training, fine-tuning and data science workflows.

- **Generative AI integration** (1.2.1): applications call Amazon Bedrock through its runtime APIs. For multi-account patterns, centralize access in a shared account or provide per-workload roles, and standardize logging and guardrails.
- **AI agents** (1.2.2): Amazon Bedrock AgentCore and Bedrock Knowledge Bases let an agent call tools and retrieve enterprise knowledge. Design for tool authorization and observability from the start.
- **ML inference** (1.2.3): Amazon SageMaker AI endpoints host models for real-time inference; choose real-time, serverless, asynchronous or batch inference by latency, payload size and traffic shape.
- **RAG** (1.2.4): retrieval-augmented generation grounds a model in your data. The pipeline has an **ingestion** side (chunk documents, create embeddings, store them in a vector store) and a **retrieval** side (embed the query, fetch relevant chunks, add them to the prompt). Bedrock knowledge bases manage this with supported vector stores.

**[📖 Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)** - Managed RAG ingestion and retrieval

## Task 1.3: Hybrid cloud integration

- **Connectivity with redundancy** (1.3.1): Direct Connect gives private, consistent-latency links; a Site-to-Site VPN gives an encrypted internet path. A common resilient design is two Direct Connect connections at different locations with VPN as backup, terminating on a **Transit Gateway** to reach many VPCs.
- **Data synchronization** (1.3.2): **DataSync** moves bulk or scheduled data; **Storage Gateway** presents cloud storage to on-premises as file, volume or tape; **Transfer Family** exposes S3 or EFS through SFTP/FTPS/FTP for partners.
- **Legacy integration** (1.3.3): put API Gateway and Lambda in front of old systems to transform data formats; use **Amazon MQ** when applications depend on standard brokers (JMS, AMQP, MQTT) and cannot move to SQS/SNS.
- **Hybrid DNS** (1.3.4): Route 53 Resolver **inbound endpoints** let on-premises resolve AWS private zones; **outbound endpoints** with forwarding rules let VPCs resolve on-premises names (conditional forwarding); private hosted zones plus rules give split-horizon behavior.
- **Hybrid compute** (1.3.5, new): EKS Anywhere and ECS Anywhere run AWS-style orchestration on your hardware; **AWS Outposts** brings AWS infrastructure to your site for low latency or data residency; **Local Zones** put select services near large population centers.

## Task 1.4: Network architectures

- **Multi-VPC connectivity** (1.4.1): VPC peering is simple and non-transitive; Transit Gateway scales hub-and-spoke and handles transitive routing; **PrivateLink** exposes one service privately without opening full network access, and is the answer for overlapping CIDRs. AWS Cloud WAN is now in scope for managing a global network.
- **VPC design** (1.4.2): public and private subnets across Availability Zones, **VPC IP Address Manager (IPAM)** to plan and track CIDRs across accounts, segmentation by workload tier.
- **Network security** (1.4.3): security groups (stateful, instance level), network ACLs (stateless, subnet level), **AWS Network Firewall** for managed inspection and filtering, **Gateway Load Balancer** to insert third-party appliances, AWS WAF for Layer 7 protection, VPC Flow Logs for visibility.
- **IPv6 and dual stack** (1.4.4, new): IPv6 removes address scarcity; dual-stack VPCs run IPv4 and IPv6 together during migration; an egress-only internet gateway gives private-subnet IPv6 workloads outbound-only access.
- **Global routing** (1.4.5): Route 53 policies (latency, geolocation, weighted, failover) steer by DNS; **Global Accelerator** gives static anycast IPs and routes over the AWS backbone with fast health-based failover, independent of DNS caching.

## Task 1.5: Data, storage and databases

- **Data lakes and lakehouses** (1.5.1, new): S3 as the lake, **Lake Formation** for fine-grained access control and governance, **Redshift Spectrum** to query S3 from Redshift, and **Apache Iceberg** table format for ACID tables on S3.
- **Analytics pipelines** (1.5.2, new): batch with EMR or Glue; warehouse with Redshift; streaming ingest with Kinesis or **Amazon MSK** (managed Kafka); SaaS ingest with AppFlow.
- **Database selection** (1.5.3): relational with joins and transactions, RDS or Aurora; key-value at massive scale, DynamoDB; analytics warehouse, Redshift. **Amazon MemoryDB** (new to scope) is a durable Redis-compatible in-memory database.
- **Database scale and availability** (1.5.4): RDS Multi-AZ for failover, read replicas for read scaling, **Aurora Global Database** for cross-Region replication with fast recovery, DynamoDB global tables for multi-Region active-active.
- **Storage** (1.5.5): S3 for objects, EBS for block, EFS for shared POSIX files, FSx for specialized file systems (Windows, Lustre, NetApp ONTAP, OpenZFS).
- **Caching** (1.5.6): ElastiCache, and DAX for DynamoDB.
- **Cataloging and sharing** (1.5.7, new): Glue Data Catalog, Lake Formation cross-account sharing, and **AWS Clean Rooms** for collaborating on combined datasets without exposing raw data.

## What changed from C02 in this domain

- **New tasks and skills:** task 1.2 (AI/ML integration); service mesh, ECR image management, ingress design, WebSocket and multi-tenant patterns (1.1); hybrid compute (1.3.5); IPv6 and dual stack (1.4.4); lakehouse, analytics pipelines and data sharing (1.5).
- **Consolidated into this domain:** VPC design and network security (from C02 1.1 and 1.2), event routing (1.4), stateless and scaling patterns (2.4), edge (3.3), event-driven and containers (4.4), data sync and legacy integration (4.2, 4.4), database scaling (2.4).
- **Removed from scope entirely in this domain's services:** All AWS IoT services and individual AI services (Comprehend, Kendra, Lex, Personalize, Polly, Rekognition, Textract, Transcribe, Translate) were replaced by parent entries for Amazon Bedrock and SageMaker AI.

## Key terms

- **Idempotent consumer** - a message handler that produces the same result when it receives the same message more than once.
- **Event bus** - an EventBridge router that receives events and forwards them to targets by matching rules, including across accounts and Regions.
- **Step Functions Standard workflow** - a long-running, auditable workflow type that can run up to one year.
- **Amazon VPC Lattice** - a managed application networking service that connects, secures and observes services across VPCs and accounts.
- **ECS Service Connect** - an ECS feature for service discovery, load balancing and metrics between services in a namespace.
- **Silo versus pool** - multi-tenant isolation models using separate resources per tenant versus shared resources with logical isolation.
- **WebSocket API** - an API Gateway API type that keeps a persistent two-way connection between client and server.
- **Retrieval-augmented generation** - grounding a model's answer in documents retrieved from your own data store.
- **Transit Gateway** - a regional network hub that connects VPCs and on-premises networks with transitive routing.
- **AWS PrivateLink** - private connectivity to a service across VPCs or accounts without exposing full network access.
- **VPC IPAM** - a service that plans, tracks and monitors IP address allocations across accounts and Regions.
- **Gateway Load Balancer** - a load balancer for deploying and scaling third-party network appliances transparently.
- **Global Accelerator** - a service that provides static anycast IP addresses and routes traffic over the AWS global network.
- **Route 53 Resolver endpoints** - inbound and outbound endpoints that connect VPC DNS with on-premises DNS.
- **AWS Outposts** - AWS-managed infrastructure installed in a customer's own facility.
- **Lake Formation** - a service for building data lakes with fine-grained, centralized access control.
- **Apache Iceberg** - an open table format that brings ACID transactions and schema evolution to files in object storage.
- **Aurora Global Database** - an Aurora configuration that replicates a database across Regions for low-latency reads and fast recovery.
- **AWS Clean Rooms** - a service for analyzing combined datasets with collaborators without sharing the underlying raw data.
