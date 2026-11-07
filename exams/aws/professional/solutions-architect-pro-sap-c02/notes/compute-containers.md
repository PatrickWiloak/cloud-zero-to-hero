# Compute & Containers

## Overview

Enterprise compute strategies on AWS encompass a wide range of services from traditional EC2 instances to serverless containers and functions. At the professional level, you must design compute architectures that optimize for performance, cost, scalability, and operational overhead while supporting diverse workload types including web applications, batch processing, high-performance computing, microservices, and machine learning.

Professional architects must understand the trade-offs between EC2, ECS, EKS, Lambda, Batch, and specialized compute services while implementing auto-scaling, right-sizing, placement strategies, and container orchestration patterns at enterprise scale.

## Key Concepts

### Amazon EC2 Advanced Concepts

**Instance Families and Types**
- **General Purpose**: t3, t4g, m5, m6i, m6g, m7g (balanced compute, memory, network)
- **Compute Optimized**: c5, c6i, c6g, c7g (high-performance processors for compute-intensive)
- **Memory Optimized**: r5, r6i, r6g, r7g, x1, x2 (large datasets in memory)
- **Storage Optimized**: i3, i4i, d2, h1 (high sequential read/write, local storage)
- **Accelerated Computing**: p3, p4, g4, inf1, trn1 (GPU, FPGA, ML inference)
- **Graviton**: ARM-based processors (t4g, m6g, c6g, r6g) for 40% better price-performance

**Purchasing Options**
- **On-Demand**: Pay per hour/second, no commitment, highest cost
- **Reserved Instances**: 1 or 3-year commitment, up to 72% savings
  - Standard RI: Highest savings, cannot change instance type
  - Convertible RI: Can change instance family, lower savings (up to 54%)
  - Scheduled RI: Reserved for specific time windows (discontinued for new purchases)
- **Savings Plans**: Flexible pricing model, commit to $/hour for 1 or 3 years
  - Compute Savings Plans: Most flexible (EC2, Fargate, Lambda), up to 66% savings
  - EC2 Instance Savings Plans: Specific instance family, up to 72% savings
- **Spot Instances**: Unused capacity, up to 90% savings, can be interrupted (2-min warning)
- **Dedicated Hosts**: Physical server dedicated to you, for licensing compliance (BYOL)
- **Dedicated Instances**: Instances on hardware dedicated to you (not full server control)
- **Capacity Reservations**: Reserve capacity in specific AZ without commitment

**Auto Scaling**
- **Target Tracking**: Maintain metric at target (CPU 50%, ALB requests/target 1000)
- **Step Scaling**: Add/remove instances based on metric thresholds
- **Simple Scaling**: Single adjustment based on alarm (legacy, use step instead)
- **Scheduled Scaling**: Predictable load patterns (scale up at 8 AM, down at 6 PM)
- **Predictive Scaling**: ML-based forecasting of future load
- **Warm Pools**: Pre-initialized instances for faster scaling
- **Lifecycle Hooks**: Custom actions during launch/terminate (backup, log draining)

**Placement Groups**
- **Cluster**: Low latency, high throughput, single AZ (HPC, big data)
- **Partition**: Spread across partitions (Hadoop, Cassandra, Kafka)
- **Spread**: Each instance on different hardware, max 7 per AZ (critical applications)

**Enhanced Networking**
- **Elastic Network Adapter (ENA)**: Up to 100 Gbps, lower latency
- **Elastic Fabric Adapter (EFA)**: HPC, ML, OS-bypass for MPI and NCCL
- **SR-IOV**: Direct access to network adapter

**Nitro System**
- Hypervisor offloaded to dedicated hardware
- Better performance, security, innovation velocity
- All new instance types built on Nitro
- Enables features like EBS encryption by default, 100 Gbps networking

### AWS Lambda

**Architecture Patterns**
- **Event-Driven**: Triggered by S3, DynamoDB, Kinesis, SNS, SQS, EventBridge, API Gateway
- **API Backend**: RESTful APIs with API Gateway, GraphQL with AppSync
- **Stream Processing**: Real-time processing of Kinesis or DynamoDB streams
- **Batch Processing**: Scheduled with EventBridge, process S3 objects
- **Orchestration**: AWS Step Functions for complex workflows

**Performance Optimization**
- **Memory**: 128 MB to 10,240 MB (CPU scales proportionally)
- **Execution Time**: Max 15 minutes (use Step Functions for longer)
- **Cold Starts**: Provisioned Concurrency eliminates cold starts (cost trade-off)
- **Initialization Code**: Outside handler function (reused across invocations)
- **Connection Pooling**: Reuse database connections
- **Layers**: Share code, dependencies (up to 5 layers, 250 MB total)
- **Container Images**: Package as container (up to 10 GB)

**Concurrency**
- **Unreserved Concurrency**: Shared pool across all functions
- **Reserved Concurrency**: Guarantee concurrency, also acts as limit
- **Provisioned Concurrency**: Pre-warmed instances, no cold starts
- Account limit: 1,000 concurrent executions per region (soft limit, can increase)

**Integration Patterns**
- **Synchronous**: API Gateway, ALB, direct invocation (RequestResponse)
- **Asynchronous**: S3, SNS, EventBridge (Event)
- **Stream-Based**: Kinesis, DynamoDB Streams (poll-based)
- **SQS**: Poll-based with batch processing, DLQ for failures

**Advanced Features**
- **Destinations**: Send results to SNS, SQS, EventBridge, another Lambda (success/failure)
- **Function URLs**: Built-in HTTPS endpoint (alternative to API Gateway)
- **SnapStart**: Java cold start reduction (up to 10x faster)
- **Lambda@Edge**: Run at CloudFront edge locations
- **Application Load Balancer Integration**: Lambda as ALB target

### Amazon ECS (Elastic Container Service)

**Launch Types**
- **EC2 Launch Type**: Manage EC2 cluster, more control, use Reserved/Spot instances
- **Fargate Launch Type**: Serverless, AWS manages infrastructure, pay per task

**Core Concepts**
- **Task Definition**: Blueprint for application (Docker image, CPU, memory, IAM role, networking)
- **Task**: Instantiation of task definition (one or more containers)
- **Service**: Maintain desired count of tasks, integrate with ALB/NLB, auto-scaling
- **Cluster**: Logical grouping of tasks and services

**Networking Modes**
- **awsvpc**: Each task gets ENI with private IP (required for Fargate)
- **bridge**: Docker bridge network (EC2 launch type only)
- **host**: Use host's network (EC2 launch type only)

**Storage**
- **Fargate**: Ephemeral storage (20 GB default, up to 200 GB)
- **EC2**: Bind mounts, Docker volumes, EBS volumes
- **Persistent Storage**: EFS for shared persistent storage across tasks

**Auto Scaling**
- **Target Tracking**: CPU, memory, ALB request count
- **Step Scaling**: Based on CloudWatch alarms
- **Scheduled Scaling**: Predictable patterns
- **Cluster Auto Scaling**: EC2 launch type, scale EC2 instances based on capacity

**Deployment Strategies**
- **Rolling Update**: Gradually replace tasks (configurable min/max healthy percent)
- **Blue/Green**: CodeDeploy integration, traffic shifting with validation
- **Circuit Breaker**: Automatically rollback failed deployments

**Service Discovery**
- **AWS Cloud Map**: DNS-based or API-based service discovery
- **Route 53**: Create DNS records for services
- Internal service-to-service communication

### Amazon EKS (Elastic Kubernetes Service)

**Architecture**
- **Control Plane**: Managed by AWS (API server, etcd, controller manager, scheduler)
- **Data Plane**: Worker nodes (EC2, Fargate, or hybrid)
- **Multi-AZ**: Control plane across 3 AZs for high availability

**Node Types**
- **Managed Node Groups**: AWS manages EC2 instances, automated updates
- **Self-Managed Nodes**: Full control, manual management
- **Fargate**: Serverless, pod-level isolation, no node management

**Networking**
- **Amazon VPC CNI**: Native VPC networking, pods get VPC IP addresses
- **Security Groups for Pods**: Fine-grained network security
- **Network Policies**: Calico or Cilium for pod-to-pod communication control

**Storage**
- **EBS CSI Driver**: Dynamic provisioning of EBS volumes
- **EFS CSI Driver**: Shared storage across pods
- **FSx for Lustre CSI Driver**: High-performance storage

**Identity and Access**
- **IAM Roles for Service Accounts (IRSA)**: Map Kubernetes service account to IAM role
- **OIDC Provider**: Enable IRSA
- **Pod Identity**: Fine-grained permissions per pod

**Observability**
- **CloudWatch Container Insights**: Metrics, logs, traces
- **Control Plane Logging**: API server, audit, authenticator, controller manager, scheduler
- **Prometheus and Grafana**: Monitoring and visualization
- **AWS Distro for OpenTelemetry**: Distributed tracing

**Add-ons**
- **CoreDNS**: Cluster DNS
- **kube-proxy**: Network proxy
- **Amazon VPC CNI**: Networking
- **EBS CSI Driver, EFS CSI Driver**: Storage
- **AWS Load Balancer Controller**: ALB and NLB integration
- **Cluster Autoscaler**: Scale worker nodes
- **Karpenter**: Advanced autoscaling with node provisioning

### AWS Batch

**Use Cases**
- Large-scale batch processing (genomics, financial modeling, rendering)
- Scheduled batch jobs
- Dynamic resource provisioning based on job queue

**Components**
- **Job Definition**: Blueprint (Docker image, vCPU, memory, IAM role)
- **Job Queue**: Priority-based queue for jobs
- **Compute Environment**: EC2 or Fargate resources
  - Managed: AWS provisions and scales
  - Unmanaged: You manage EC2 instances
- **Job**: Instance of job definition submitted to queue

**Compute Options**
- **On-Demand**: Reliable, higher cost
- **Spot**: Up to 90% savings, can be interrupted
- **Fargate**: Serverless, no instance management
- **EC2**: More control, Reserved Instances, instance store

**Scheduling**
- **Priority**: Higher priority jobs run first
- **Dependencies**: Job dependencies (run job B after job A completes)
- **Array Jobs**: Large-scale parallel processing (1-10,000 jobs)
- **Multi-node**: MPI jobs across multiple instances

**Integration**
- **EventBridge**: Schedule batch jobs
- **Step Functions**: Orchestrate Batch jobs with other services
- **S3**: Input/output storage
- **ECR**: Container images

### AWS App Runner

**Characteristics**
- Fully managed service for web apps and APIs
- From source code or container image
- Automatic scaling, load balancing, encryption
- Minimal configuration (no VPC, load balancer, auto-scaling setup)

**Use Cases**
- Simple web applications and APIs
- Rapid prototyping
- Microservices without container orchestration complexity
- Migration from Heroku or similar PaaS

**Configuration**
- Source: GitHub, ECR
- Automatic deployments on code push
- Environment variables and secrets
- Custom domain with certificate

### AWS Lightsail

**Characteristics**
- Simplified VPS service
- Fixed-price bundles (CPU, memory, storage, transfer)
- Use cases: Simple websites, dev/test environments, small applications
- Not for enterprise-scale or complex architectures

## AWS Services Reference

### Core Services

**Amazon EC2**
- Virtual servers in the cloud
- Wide selection of instance types
- Multiple purchasing options
- Auto Scaling and placement groups

**AWS Lambda**
- Serverless compute for event-driven applications
- Pay per invocation and duration
- Automatic scaling
- 15-minute max execution time

**Amazon ECS**
- Container orchestration service
- EC2 and Fargate launch types
- Deep AWS integration
- Task definitions and services

**Amazon EKS**
- Managed Kubernetes service
- Multi-AZ control plane
- EC2, Fargate, and hybrid nodes
- CNCF conformant

### Supporting Services

**AWS Batch**
- Managed batch processing
- Dynamic resource provisioning
- Priority-based job queuing
- EC2 and Fargate compute

**AWS Elastic Beanstalk**
- PaaS for deploying applications
- Managed infrastructure (EC2, RDS, ALB, Auto Scaling)
- Multiple languages and frameworks
- Full access to underlying resources

**AWS App Runner**
- Fully managed web app and API service
- From source code or containers
- Automatic scaling and deployment
- Minimal configuration

**AWS Systems Manager**
- Patch Manager: Automated OS patching
- Session Manager: Secure shell without SSH keys
- Run Command: Execute commands at scale
- Parameter Store: Configuration and secrets

**Amazon EC2 Image Builder**
- Automated AMI creation pipeline
- Security and compliance validation
- Version management
- Cross-region distribution

**AWS Compute Optimizer**
- ML-based recommendations for right-sizing
- EC2, EBS, Lambda, ECS on Fargate
- Cost savings and performance insights

## Architecture Patterns

### Pattern 1: Multi-Tier Web Application with Auto Scaling

**Use Case**
- E-commerce website with variable traffic
- High availability across multiple AZs
- Auto-scaling based on demand
- Cost optimization with right-sizing

**Implementation Approach**
1. **Web Tier**: Auto Scaling group of EC2 instances behind ALB
   - t3.medium or c6g.medium instances (Graviton for cost savings)
   - Target tracking scaling: CPU 50% or ALB request count
   - Multi-AZ deployment across 3 AZs
2. **Application Tier**: Auto Scaling group in private subnets
   - m6g.large instances with application code
   - ECS Fargate as alternative for containerized apps
3. **Database Tier**: RDS Multi-AZ or Aurora cluster
4. **Caching**: ElastiCache Redis for session store and database cache
5. **CDN**: CloudFront for static assets
6. **Storage**: S3 for images and media
7. **Monitoring**: CloudWatch dashboards, alarms, Compute Optimizer recommendations

**Pros/Cons**
- Pros: High availability, auto-scaling, cost-effective, proven architecture
- Cons: Requires management of EC2 instances, patching, AMI updates

### Pattern 2: Serverless Microservices with Lambda and ECS

**Use Case**
- Microservices architecture with independent scaling
- Event-driven and API-based services
- Minimize operational overhead
- Cost optimization (pay for actual usage)

**Implementation Approach**
1. **API Gateway**: RESTful APIs with Lambda backend
2. **Lambda Functions**: Business logic for each microservice
   - Provisioned Concurrency for latency-sensitive APIs
   - DLQ for failed invocations
3. **ECS Fargate**: Long-running services or services with complex dependencies
4. **EventBridge**: Event-driven communication between services
5. **SQS**: Decoupling asynchronous processing
6. **DynamoDB**: NoSQL database with on-demand or provisioned capacity
7. **S3**: Object storage for uploads, reports
8. **Step Functions**: Orchestrate complex workflows
9. **API Gateway or ALB**: Frontend routing

**Pros/Cons**
- Pros: Serverless, auto-scaling, cost-effective, independent deployments
- Cons: Debugging complexity, cold starts, 15-min Lambda limit, distributed tracing needed

### Pattern 3: Container Orchestration with EKS

**Use Case**
- Enterprise adopting Kubernetes for multi-cloud strategy
- Microservices with complex networking and storage requirements
- Existing Kubernetes expertise
- Portability across clouds

**Implementation Approach**
1. **EKS Cluster**: Multi-AZ control plane
2. **Worker Nodes**:
   - Managed Node Groups for general workloads (m6g.xlarge)
   - Fargate for serverless pods (stateless services)
   - Spot instances for fault-tolerant workloads
3. **Networking**: Amazon VPC CNI, security groups for pods
4. **Storage**:
   - EBS CSI for StatefulSets (databases)
   - EFS CSI for shared storage (ML training data)
5. **Ingress**: AWS Load Balancer Controller for ALB/NLB
6. **Auto Scaling**:
   - Horizontal Pod Autoscaler (HPA) for pods
   - Karpenter for node provisioning and scaling
7. **Observability**: CloudWatch Container Insights, Prometheus, Grafana
8. **Security**: IRSA for pod-level IAM permissions, Secrets Manager CSI driver
9. **GitOps**: Flux or ArgoCD for declarative deployments

**Pros/Cons**
- Pros: Kubernetes standard, portability, rich ecosystem, advanced networking/storage
- Cons: Complexity, learning curve, higher operational overhead than ECS

### Pattern 4: High-Performance Computing with Batch and Spot

**Use Case**
- Genomics, financial modeling, video rendering
- Large-scale parallel processing
- Cost-sensitive workloads
- Variable workload patterns

**Implementation Approach**
1. **AWS Batch**: Managed job scheduling and compute provisioning
2. **Compute Environment**: Spot instances (up to 90% savings)
   - c6i.32xlarge for CPU-intensive (128 vCPUs)
   - p3.16xlarge for GPU workloads
   - Instance diversification (multiple instance types for Spot reliability)
3. **Job Queue**: Priority-based queuing
4. **Job Definitions**: Docker containers with application code
5. **Storage**:
   - S3 for input/output data
   - FSx for Lustre for high-performance shared storage
   - Instance store for temporary data
6. **Networking**: Placement groups (cluster) for low latency
7. **Orchestration**: Step Functions for multi-stage pipelines
8. **Interruption Handling**: Checkpointing, resume from last checkpoint

**Pros/Cons**
- Pros: Cost-effective (Spot), dynamic scaling, managed service, supports complex dependencies
- Cons: Spot interruptions (mitigate with checkpointing), container-based (learning curve)

### Pattern 5: Hybrid Compute with AWS Outposts

**Use Case**
- Low-latency requirements for on-premises data
- Data residency regulations
- Gradual cloud migration
- Consistent hybrid experience

**Implementation Approach**
1. **AWS Outposts**: AWS infrastructure on-premises (42U rack or 1U/2U servers)
2. **Services**: EC2, EBS, S3, ECS, EKS, RDS on Outposts
3. **Connectivity**: Local Gateway (LGW) for on-premises network integration
4. **Control Plane**: AWS Region (requires internet/Direct Connect connectivity)
5. **Use Cases**:
   - Low-latency local processing (manufacturing, media)
   - Data residency (healthcare, finance)
   - Migration landing zone (lift-and-shift, then optimize in region)
6. **Management**: Same APIs, console, CLI as AWS Regions

**Pros/Cons**
- Pros: Consistent AWS experience, local compute and storage, hybrid integration
- Cons: High cost (hardware purchase/lease), capacity planning, on-premises footprint

### Pattern 6: Spot Fleet for Cost Optimization

**Use Case**
- Fault-tolerant workloads (batch processing, big data)
- Cost optimization (up to 90% savings)
- Highly variable workloads

**Implementation Approach**
1. **Spot Fleet**: Request Spot instances across multiple instance types and AZs
2. **Diversification**: 10+ instance types (c5, c5a, c5n, c6i, c6a, etc.) for availability
3. **Allocation Strategy**:
   - **price-capacity-optimized**: Balance price and capacity (recommended)
   - **capacity-optimized**: Prioritize availability
   - **lowest-price**: Minimize cost (higher interruption risk)
4. **On-Demand Base**: Maintain minimum capacity with On-Demand
5. **Interruption Handling**:
   - 2-minute warning (CloudWatch Events)
   - Graceful shutdown (checkpoint, drain connections)
   - Auto-replace interrupted instances
6. **Integration**: Auto Scaling groups with mixed instances policy
7. **Use Cases**: EMR, ECS, batch processing, rendering, CI/CD

**Pros/Cons**
- Pros: Massive cost savings, automatic instance replacement, diversification reduces interruptions
- Cons: Interruptions (2-min warning), complexity, fault-tolerant architecture required

## Best Practices

### Enterprise-Level Recommendations

**Right-Sizing**
- Use AWS Compute Optimizer for data-driven recommendations
- Monitor CloudWatch metrics (CPU, memory, network)
- Right-size during non-peak hours
- Iterate: Start large, optimize down
- Review quarterly

**Cost Optimization**
- Reserved Instances for predictable, steady-state workloads (databases, base capacity)
- Savings Plans for flexible compute (EC2, Fargate, Lambda)
- Spot Instances for fault-tolerant workloads (batch, big data)
- Graviton instances for 40% better price-performance
- Auto Scaling to match capacity with demand
- Scheduled scaling for predictable patterns
- gp3 volumes instead of gp2 (20% cheaper, better performance)

**High Availability**
- Multi-AZ deployments for production workloads
- Auto Scaling groups span multiple AZs
- ALB/NLB for health checks and traffic distribution
- RDS Multi-AZ or Aurora for databases
- Regular DR drills

**Security**
- IMDSv2 for instance metadata (prevents SSRF)
- IAM roles for EC2/ECS/EKS (no access keys)
- Security groups as primary firewall
- Secrets Manager or Parameter Store for credentials
- Systems Manager Session Manager (no SSH keys)
- EBS encryption by default
- AMI scanning with Inspector

### Performance Tuning

**EC2 Performance**
- EBS-optimized instances for dedicated bandwidth
- Enhanced networking (ENA) enabled
- Placement groups for HPC (cluster) or HA (spread)
- Instance store for temporary, high-IOPS data
- Larger instance types for higher network throughput
- Monitor network performance with CloudWatch

**Lambda Performance**
- Increase memory (CPU scales proportionally)
- Minimize cold starts: Provisioned Concurrency, SnapStart (Java)
- Initialization outside handler (connection pooling)
- Use layers for shared dependencies
- Monitor Duration, Concurrent Executions, Throttles

**Container Performance**
- Right-size task CPU and memory
- Use Fargate Spot for cost savings (fault-tolerant)
- Container image optimization (minimize layers, use multi-stage builds)
- ECS Cluster Auto Scaling (EC2 launch type)
- Monitor task CPU and memory utilization

**EKS Performance**
- Right-size pods and nodes
- Horizontal Pod Autoscaler (HPA) for pods
- Karpenter for intelligent node provisioning
- Use Spot for fault-tolerant pods (batch, ML training)
- Monitor with Container Insights or Prometheus

## Common Scenarios

### Scenario 1: Global E-Commerce Platform with 100M Users

**Context**: High-traffic e-commerce site with 100M users, peak traffic 100K requests/second, global presence

**Architecture**
1. **Global**: CloudFront for static content and edge caching
2. **Multi-Region**: Deployments in us-east-1, eu-west-1, ap-southeast-1
3. **Compute**:
   - ALB in each region
   - Auto Scaling groups with mixed instances (On-Demand base, Spot for overflow)
   - Instance types: c6g.2xlarge (Graviton for cost)
   - Target tracking: 50% CPU, 1000 ALB requests/target
   - Predictive scaling for known traffic patterns (Black Friday)
4. **Containers**: ECS Fargate for microservices (cart, checkout, recommendations)
5. **Database**: Aurora Global Database (primary in us-east-1, read replicas in other regions)
6. **Caching**: ElastiCache Redis (session store, product catalog cache)
7. **Search**: OpenSearch for product search
8. **Storage**: S3 with Cross-Region Replication for product images
9. **Queue**: SQS for order processing, inventory updates
10. **Monitoring**: CloudWatch Synthetics for uptime, RUM for user experience

**Key Considerations**
- Route 53 latency-based routing to nearest region
- Auto Scaling warm pools for faster scale-out
- Reserved Instances for base capacity (30%), Spot for peak (70%)
- Blue/green deployments for zero-downtime updates
- DDoS protection with Shield Advanced and WAF rate limiting

### Scenario 2: Microservices Migration from Monolith

**Context**: Migrating 10-year-old monolithic Java application to microservices

**Architecture**
1. **Strangler Fig Pattern**: Gradually extract microservices
2. **Phase 1**: Containerize monolith (ECS or EKS)
3. **Phase 2**: Extract high-value services (authentication, payments, notifications)
   - Lambda for lightweight services (notifications, email)
   - ECS Fargate for complex services (payments, inventory)
4. **API Gateway**: Route to monolith or microservices based on path
5. **Database**: Start with shared database, gradually split per-service databases
6. **Event-Driven**: EventBridge for service-to-service communication
7. **Observability**: X-Ray for distributed tracing, CloudWatch Logs Insights
8. **CI/CD**: CodePipeline for independent deployments per service

**Key Considerations**
- Start with read-heavy services (easier to extract)
- Database foreign keys complicate separation
- Transactional boundaries (saga pattern for distributed transactions)
- Organizational change (DevOps, team per service)
- Gradual rollout with feature flags

### Scenario 3: Machine Learning Training Pipeline

**Context**: ML team training models on 1 PB of data, weekly retraining

**Architecture**
1. **Data Lake**: S3 with training data (Parquet format)
2. **Training Instances**: p4d.24xlarge (8x A100 GPUs, 320 GB GPU memory)
   - Spot instances for 70% cost savings
   - Capacity Reservations for critical training runs
3. **Storage**: FSx for Lustre linked to S3 (lazy loading, high throughput)
4. **Orchestration**: SageMaker Pipelines or Step Functions
5. **Distributed Training**: EKS with Kubeflow or SageMaker Distributed
6. **Checkpointing**: S3 for fault tolerance (resume from checkpoint on Spot interruption)
7. **Model Registry**: S3 or SageMaker Model Registry
8. **Inference**: SageMaker endpoints or Lambda (smaller models)
9. **Monitoring**: CloudWatch for training metrics, SageMaker Model Monitor

**Key Considerations**
- Spot interruptions: Checkpointing every 15 minutes
- Data loading bottleneck: FSx for Lustre (1 TB/s throughput)
- EFA for multi-node training (NCCL for GPU communication)
- Right-size instance type (GPU memory, network bandwidth)
- Cost: p4d.24xlarge $32/hr On-Demand, $10/hr Spot (70% savings)

### Scenario 4: Genomics Pipeline Processing 10K Samples/Day

**Context**: Research institute processing whole-genome sequencing, 30x coverage, 100 GB per sample

**Architecture**
1. **Ingestion**: S3 Transfer Acceleration for global uploads
2. **Compute**: AWS Batch with Spot instances
   - Job queue: Alignment (CPU), Variant Calling (CPU/GPU)
   - Compute environment: c6i.32xlarge, r6i.32xlarge, diversified Spot fleet
3. **Storage**:
   - S3 Standard for raw FASTQ files
   - FSx for Lustre for intermediate files (BAM, VCF)
   - S3 Glacier Deep Archive for long-term retention
4. **Workflow**: Nextflow or Cromwell on Batch
5. **Reference Data**: EFS or S3 with versioning (human genome reference)
6. **Scaling**: 10K samples * 100 GB = 1 PB/day input
7. **Lifecycle**: Raw data to Glacier after 90 days
8. **Compliance**: HIPAA compliance (PHI data), encryption at rest/transit

**Key Considerations**
- Cost: Spot for 70-90% savings (10K samples * 16 vCPUs * 4 hours = 640K vCPU-hours/day)
- Data transfer: Direct Connect for on-premises uploads (alternative to Transfer Acceleration)
- Checkpointing: Resume variant calling from last completed chromosome
- Data security: VPC endpoints (no internet), encryption, audit logs
- Result delivery: S3 pre-signed URLs for researchers

### Scenario 5: Real-Time Gaming Platform with 1M Concurrent Players

**Context**: Multiplayer game with real-time state synchronization, low latency critical (<50ms)

**Architecture**
1. **Game Servers**: EC2 with Auto Scaling
   - c6gn.16xlarge (64 vCPUs, 100 Gbps network, Graviton3)
   - Placement groups (cluster) for lowest latency
   - Dedicated Hosts for BYOL game engine
2. **Matchmaking**: Lambda with SQS for player queuing
3. **Session Management**: DynamoDB for game state
4. **Real-Time Communication**: ECS Fargate with WebSocket (ALB or API Gateway WebSocket)
5. **Global**: Multi-region deployments (us-east-1, eu-west-1, ap-southeast-1)
6. **Routing**: Route 53 latency-based routing or Global Accelerator (static IPs, global routing)
7. **Storage**: ElastiCache Redis for leaderboards, player sessions
8. **Analytics**: Kinesis Data Streams for game events, Lambda for processing
9. **Anti-Cheat**: Lambda@Edge for request validation

**Key Considerations**
- Latency: Enhanced networking (ENA), placement groups, regional deployments
- Scaling: Auto Scaling based on player count (custom CloudWatch metric)
- Cost: Spot for non-production, Reserved for base capacity
- Game server lifecycle: Graceful shutdown (finish match before terminating)
- DDoS protection: Shield Advanced, WAF rate limiting

## AWS CLI Examples

```bash
# EC2 - Launch instance with IMDSv2 required
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type c6g.xlarge \
  --key-name my-key \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --iam-instance-profile Name=EC2-SSM-Role \
  --metadata-options HttpTokens=required,HttpPutResponseHopLimit=1 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WebServer}]'

# EC2 - Create Auto Scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name web-asg \
  --launch-template LaunchTemplateName=web-template,Version='$Latest' \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 4 \
  --target-group-arns arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/web-tg/1234567890abcdef \
  --health-check-type ELB \
  --health-check-grace-period 300 \
  --vpc-zone-identifier "subnet-11111111,subnet-22222222,subnet-33333333"

# EC2 - Create target tracking scaling policy
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name web-asg \
  --policy-name cpu-target-tracking \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration file://target-tracking.json

# target-tracking.json:
# {
#   "TargetValue": 50.0,
#   "PredefinedMetricSpecification": {
#     "PredefinedMetricType": "ASGAverageCPUUtilization"
#   }
# }

# EC2 - Request Spot Fleet
aws ec2 request-spot-fleet --spot-fleet-request-config file://spot-fleet.json

# spot-fleet.json example:
# {
#   "IamFleetRole": "arn:aws:iam::123456789012:role/aws-ec2-spot-fleet-tagging-role",
#   "AllocationStrategy": "price-capacity-optimized",
#   "TargetCapacity": 100,
#   "SpotPrice": "0.50",
#   "LaunchSpecifications": [
#     {"InstanceType": "c5.2xlarge", "ImageId": "ami-0abcdef1234567890", ...},
#     {"InstanceType": "c5a.2xlarge", "ImageId": "ami-0abcdef1234567890", ...},
#     {"InstanceType": "c6i.2xlarge", "ImageId": "ami-0abcdef1234567890", ...}
#   ]
# }

# Lambda - Create function with container image
aws lambda create-function \
  --function-name my-app \
  --package-type Image \
  --code ImageUri=123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest \
  --role arn:aws:iam::123456789012:role/LambdaExecutionRole \
  --memory-size 2048 \
  --timeout 300 \
  --environment Variables={DB_HOST=db.example.com,ENV=production}

# Lambda - Configure provisioned concurrency
aws lambda put-provisioned-concurrency-config \
  --function-name my-app \
  --provisioned-concurrent-executions 100 \
  --qualifier PROD

# Lambda - Create function URL
aws lambda create-function-url-config \
  --function-name my-app \
  --auth-type AWS_IAM \
  --cors '{"AllowOrigins":["https://example.com"],"AllowMethods":["GET","POST"],"MaxAge":86400}'

# ECS - Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# task-definition.json example:
# {
#   "family": "web-app",
#   "networkMode": "awsvpc",
#   "requiresCompatibilities": ["FARGATE"],
#   "cpu": "1024",
#   "memory": "2048",
#   "containerDefinitions": [{
#     "name": "app",
#     "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/web-app:latest",
#     "portMappings": [{"containerPort": 8080, "protocol": "tcp"}],
#     "environment": [{"name": "ENV", "value": "production"}],
#     "secrets": [{"name": "DB_PASSWORD", "valueFrom": "arn:aws:secretsmanager:..."}],
#     "logConfiguration": {
#       "logDriver": "awslogs",
#       "options": {"awslogs-group": "/ecs/web-app", "awslogs-region": "us-east-1", "awslogs-stream-prefix": "ecs"}
#     }
#   }],
#   "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
#   "taskRoleArn": "arn:aws:iam::123456789012:role/ecsTaskRole"
# }

# ECS - Create service with auto-scaling
aws ecs create-service \
  --cluster my-cluster \
  --service-name web-service \
  --task-definition web-app:1 \
  --desired-count 3 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-11111111,subnet-22222222],securityGroups=[sg-12345678],assignPublicIp=DISABLED}" \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=app,containerPort=8080 \
  --health-check-grace-period-seconds 60

# ECS - Configure service auto-scaling
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/my-cluster/web-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 3 \
  --max-capacity 50

aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/my-cluster/web-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu-scaling \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://ecs-scaling.json

# EKS - Create cluster
aws eks create-cluster \
  --name production-cluster \
  --role-arn arn:aws:iam::123456789012:role/EKSClusterRole \
  --resources-vpc-config subnetIds=subnet-11111111,subnet-22222222,subnet-33333333,securityGroupIds=sg-12345678 \
  --kubernetes-version 1.28 \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'

# EKS - Create managed node group
aws eks create-nodegroup \
  --cluster-name production-cluster \
  --nodegroup-name general-purpose \
  --subnets subnet-11111111 subnet-22222222 subnet-33333333 \
  --instance-types m6g.xlarge m6g.2xlarge \
  --scaling-config minSize=3,maxSize=15,desiredSize=6 \
  --capacity-type ON_DEMAND \
  --node-role arn:aws:iam::123456789012:role/EKSNodeRole \
  --tags Environment=Production,Team=Platform

# EKS - Create Fargate profile
aws eks create-fargate-profile \
  --cluster-name production-cluster \
  --fargate-profile-name serverless-apps \
  --pod-execution-role-arn arn:aws:iam::123456789012:role/EKSFargatePodExecutionRole \
  --subnets subnet-11111111 subnet-22222222 \
  --selectors namespace=serverless

# AWS Batch - Create compute environment
aws batch create-compute-environment \
  --compute-environment-name batch-spot-env \
  --type MANAGED \
  --state ENABLED \
  --compute-resources file://compute-resources.json

# compute-resources.json:
# {
#   "type": "SPOT",
#   "allocationStrategy": "SPOT_CAPACITY_OPTIMIZED",
#   "minvCpus": 0,
#   "maxvCpus": 1000,
#   "desiredvCpus": 100,
#   "instanceTypes": ["c5", "c5a", "c6i", "optimal"],
#   "subnets": ["subnet-11111111", "subnet-22222222"],
#   "securityGroupIds": ["sg-12345678"],
#   "instanceRole": "arn:aws:iam::123456789012:instance-profile/ecsInstanceRole",
#   "bidPercentage": 100,
#   "spotIamFleetRole": "arn:aws:iam::123456789012:role/aws-ec2-spot-fleet-role"
# }

# AWS Batch - Create job queue
aws batch create-job-queue \
  --job-queue-name high-priority-queue \
  --state ENABLED \
  --priority 100 \
  --compute-environment-order order=1,computeEnvironment=batch-spot-env

# AWS Batch - Register job definition
aws batch register-job-definition \
  --job-definition-name genomics-alignment \
  --type container \
  --container-properties file://job-definition.json

# Compute Optimizer - Get EC2 recommendations
aws compute-optimizer get-ec2-instance-recommendations \
  --instance-arns arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0 \
  --query 'instanceRecommendations[0].[instanceArn,finding,currentInstanceType,recommendationOptions[0].instanceType,recommendationOptions[0].estimatedMonthlySavings.value]' \
  --output table

# Systems Manager - Run command on instances
aws ssm send-command \
  --document-name "AWS-RunShellScript" \
  --targets "Key=tag:Environment,Values=Production" \
  --parameters 'commands=["sudo yum update -y","sudo systemctl restart nginx"]' \
  --comment "Patch and restart nginx on production servers"

# Systems Manager - Start session (no SSH required)
aws ssm start-session --target i-1234567890abcdef0
```

## Study Tips

### SAP-C02 Exam Focus Areas

**High-Priority Compute Topics**
- EC2 instance types and use cases (Graviton, GPU, Spot)
- Auto Scaling strategies and policies
- Lambda concurrency, cold starts, integration patterns
- ECS vs. EKS decision-making (when to use each)
- Container orchestration patterns
- AWS Batch for large-scale batch processing
- Cost optimization (Reserved, Savings Plans, Spot)
- Right-sizing with Compute Optimizer

**Scenario-Based Questions**
- Design auto-scaling architecture for variable traffic
- Choose compute service based on workload characteristics
- Optimize costs with purchasing options mix
- Design container platform (ECS vs. EKS)
- High-performance computing architecture
- Serverless vs. server-based trade-offs
- Spot instance integration for fault-tolerant workloads

**Common Decision Points**
- **EC2 vs. Lambda**: Long-running vs. short-duration, predictable vs. event-driven
- **ECS vs. EKS**: Simplicity vs. Kubernetes ecosystem, AWS-native vs. portability
- **Fargate vs. EC2**: Serverless vs. control, cost trade-offs
- **On-Demand vs. Reserved vs. Spot**: Reliability vs. cost, workload characteristics
- **Graviton vs. x86**: Price-performance vs. compatibility
- **Batch vs. EMR vs. ECS**: Batch jobs vs. big data vs. general containers

### Key Differences from SAA-C03

**SAA-C03 Compute Knowledge**
- Basic EC2 instance types
- Simple Auto Scaling
- Lambda basics
- ECS fundamentals

**Additional SAP-C02 Requirements**
- Advanced Auto Scaling (predictive, warm pools, lifecycle hooks)
- EC2 purchasing strategy (mix of On-Demand, Reserved, Savings Plans, Spot)
- Graviton migration and price-performance benefits
- Advanced Lambda (provisioned concurrency, SnapStart, container images, function URLs)
- ECS advanced patterns (service discovery, deployment strategies, circuit breaker)
- EKS architecture (IRSA, Fargate, Karpenter, security groups for pods)
- AWS Batch for large-scale processing
- Container migration strategies
- Compute Optimizer for rightsizing
- Hybrid compute with Outposts

### Complex Scenarios to Master

**Multi-Tier Auto Scaling**
- Web, app, database tiers with independent scaling
- Target tracking vs. step scaling vs. predictive
- Warm pools for faster scaling
- Scheduled scaling for predictable patterns
- Mixed instances policy with Spot

**Microservices Architecture**
- Service mesh (App Mesh retired 2026-09-30; ECS Service Connect on ECS)
- Service discovery with Cloud Map
- Event-driven communication
- Lambda vs. ECS vs. EKS for different services
- API Gateway or ALB for routing

**Container Orchestration**
- ECS task placement strategies
- EKS node provisioning with Karpenter
- Fargate vs. EC2 cost analysis
- Blue/green deployments
- IRSA for pod-level permissions

**HPC and Batch Processing**
- Spot fleet diversification
- FSx for Lustre with S3 integration
- Placement groups and enhanced networking
- Checkpointing for fault tolerance
- Cost optimization with Spot (70-90% savings)

**Cost Optimization**
- Reserved Instances vs. Savings Plans comparison
- Spot integration for fault-tolerant workloads
- Graviton migration strategy
- Right-sizing with Compute Optimizer
- Lambda memory optimization (cost vs. duration)

### Practice Lab Recommendations

1. **Auto Scaling Deep Dive**
   - Create launch template with user data
   - Create Auto Scaling group across 3 AZs
   - Configure target tracking (CPU 50%)
   - Add scheduled scaling
   - Test scale-out and scale-in
   - Monitor with CloudWatch

2. **Lambda Optimization**
   - Create function with different memory settings
   - Compare duration and cost
   - Implement provisioned concurrency
   - Test cold start vs. warm start
   - Use X-Ray for performance analysis

3. **ECS Fargate Deployment**
   - Create task definition with container
   - Create ECS service with ALB
   - Configure service auto-scaling
   - Implement blue/green deployment
   - Monitor with Container Insights

4. **EKS Cluster Setup**
   - Create EKS cluster with eksctl or console
   - Create managed node group
   - Deploy sample app with kubectl
   - Configure HPA for auto-scaling
   - Set up IRSA for pod permissions

5. **Spot Instance Integration**
   - Create Spot Fleet request with diversification
   - Handle Spot interruptions (2-min warning with EventBridge)
   - Compare cost with On-Demand
   - Use in Auto Scaling group with mixed instances policy

6. **AWS Batch Pipeline**
   - Create Batch compute environment with Spot
   - Create job queue
   - Register job definition with Docker image
   - Submit job and monitor execution
   - Review cost savings with Spot

## Additional Resources

### AWS Whitepapers
- Overview of Amazon Web Services
- AWS Compute Services
- Best Practices for EC2
- Serverless Architectures with AWS Lambda
- Amazon ECS Best Practices Guide
- Amazon EKS Best Practices Guide
- Cost Optimization with AWS
- Optimizing Enterprise Economics with Serverless

### Documentation Links
- Amazon EC2: https://docs.aws.amazon.com/ec2/
- AWS Lambda: https://docs.aws.amazon.com/lambda/
- Amazon ECS: https://docs.aws.amazon.com/ecs/
- Amazon EKS: https://docs.aws.amazon.com/eks/
- AWS Batch: https://docs.aws.amazon.com/batch/
- AWS Auto Scaling: https://docs.aws.amazon.com/autoscaling/
- AWS Compute Optimizer: https://docs.aws.amazon.com/compute-optimizer/

### Video Resources
- AWS re:Invent Compute sessions (search "CMP" track)
- Deep Dive on EC2 Instances
- Serverless Patterns and Best Practices
- Amazon EKS Under the Hood
- Optimizing Costs with EC2
