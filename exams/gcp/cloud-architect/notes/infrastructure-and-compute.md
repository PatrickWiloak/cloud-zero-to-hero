# Infrastructure and Compute - GCP Professional Cloud Architect

## Overview

Comprehensive guide to infrastructure and compute architecture decisions, covering compute services, storage strategies, network topologies, and infrastructure management for the Professional Cloud Architect certification. This guide provides deep technical insights into designing scalable, resilient, and cost-effective solutions on Google Cloud Platform.

## Key Topics

1. **Compute Service Selection** - Choosing between Compute Engine, GKE, App Engine, Cloud Run, Cloud Functions
2. **Storage Architecture** - Cloud Storage, persistent disks, filestore, data lifecycle management
3. **Network Topology** - VPC design, hybrid connectivity, global load balancing
4. **Infrastructure as Code** - Terraform, Deployment Manager, configuration management
5. **Capacity Planning** - Resource sizing, scaling strategies, performance optimization
6. **Migration Strategies** - Lift-and-shift, re-platform, re-architect patterns
7. **Cost Optimization** - Committed use discounts, sustained use discounts, preemptible instances
8. **High Availability** - Multi-region architectures, disaster recovery, backup strategies

## Compute Engine Architecture

### Overview
Compute Engine provides Infrastructure as a Service (IaaS) with maximum control and flexibility. Understanding machine types, families, and optimization strategies is critical for the Professional Cloud Architect exam.

### Machine Type Families

#### General Purpose (E2, N2, N2D, N1)
**E2 (Cost-Optimized)**:
- Shared-core: e2-micro, e2-small, e2-medium (0.25-2 vCPUs)
- Standard: 2-32 vCPUs, 0.5-8 GB RAM per vCPU
- Best for: Development, testing, light workloads
- Cost: Up to 31% cheaper than N1
- Auto-scaling machine types adjust resources automatically

**N2 (Balanced Performance)**:
- 2-128 vCPUs, 0.5-8 GB RAM per vCPU
- Intel Cascade Lake processors
- Extended memory option: Up to 640 GB (for 80 vCPU)
- Best for: Web servers, app servers, databases, enterprise applications
- Supports custom machine types

**N2D (AMD-Based)**:
- 2-224 vCPUs, 0.5-8 GB RAM per vCPU
- AMD EPYC processors
- Up to 10% lower cost than N2
- Best for: Cost-sensitive workloads requiring balanced resources

**N1 (Previous Generation)**:
- 1-96 vCPUs, 3.75 GB RAM per vCPU (standard)
- Legacy support, still widely used
- Committed use discounts more mature
- Being phased out but important for existing deployments

#### Compute-Optimized (C2, C2D)
**C2 (High-Performance Computing)**:
- 4-60 vCPUs, 4 GB RAM per vCPU
- Intel Cascade Lake processors (3.8 GHz sustained)
- Best for: Compute-intensive workloads, gaming servers, HPC, ad serving
- Highest CPU performance per core

**C2D (AMD High-Performance)**:
- 2-112 vCPUs, 4 GB RAM per vCPU
- AMD EPYC Milan processors
- Up to 10% lower cost than C2
- Best for: High-performance computing, electronic design automation

#### Memory-Optimized (M1, M2, M3)
**M1 (Ultra-High Memory)**:
- 40-160 vCPUs
- 961 GB to 3.8 TB RAM
- Ratio: 24 GB RAM per vCPU
- Best for: SAP HANA, in-memory databases, analytics

**M2 (High Memory)**:
- 208-416 vCPUs
- Up to 11.7 TB RAM
- Best for: Large in-memory databases, real-time analytics

**M3 (Ultra-High Memory, Latest)**:
- 32-128 vCPUs
- Up to 3.8 TB RAM
- Intel Ice Lake processors
- Better price-performance than M2

#### Accelerator-Optimized (A2, A3, G2)
**A2 (NVIDIA GPU)**:
- Includes NVIDIA A100 GPUs (40 or 80 GB)
- 12-96 vCPUs per instance
- 1-16 GPUs per instance
- Best for: ML training, HPC, scientific computing

**A3 (NVIDIA H100 GPU)**:
- Latest generation for AI/ML
- 8 H100 GPUs per instance
- NVLink and NVSwitch for GPU-to-GPU communication
- Best for: Large language models, deep learning

**G2 (NVIDIA L4 GPU)**:
- Cost-effective GPU instances
- 1-8 L4 GPUs
- Best for: ML inference, graphics workloads, video transcoding

### Custom Machine Types

**Configuration**:
```bash
# Create custom machine type
gcloud compute instances create custom-vm \
  --custom-cpu=6 \
  --custom-memory=30GB \
  --zone=us-central1-a

# Extended memory (N2 only, >8GB per vCPU)
gcloud compute instances create extended-memory-vm \
  --machine-type=n2-custom-8-81920 \
  --zone=us-central1-a
```

**Considerations**:
- Custom machine types: 1 vCPU or even number of vCPUs
- Memory: 0.9-6.5 GB per vCPU (general purpose)
- Extended memory: Up to 8 GB per vCPU (N2, N2D)
- Cost: Slightly higher than predefined types
- Use when: Predefined types don't match workload requirements

### Sole-Tenant Nodes

**Architecture**:
```
Organization Sole-Tenant Node Group
└── Node Group (us-central1-a)
    ├── Node 1: n1-node-96-624 (96 vCPUs, 624 GB RAM)
    │   ├── VM Instance 1 (n1-standard-32)
    │   ├── VM Instance 2 (n1-standard-32)
    │   └── VM Instance 3 (n1-standard-32)
    └── Node 2: n1-node-96-624
        └── VM Instances...
```

**Use Cases**:
- Regulatory compliance (data isolation)
- Bring Your Own License (BYOL) - Windows, SQL Server
- Performance (no noisy neighbor)
- Security (physical separation)
- Payment Card Industry (PCI) compliance

**Configuration**:
```bash
# Create node template
gcloud compute sole-tenancy node-templates create node-template-1 \
  --node-type=n1-node-96-624 \
  --region=us-central1

# Create node group
gcloud compute sole-tenancy node-groups create node-group-1 \
  --node-template=node-template-1 \
  --target-size=3 \
  --zone=us-central1-a \
  --maintenance-policy=restart-in-place

# Launch instance on sole-tenant node
gcloud compute instances create vm-on-sole-tenant \
  --machine-type=n1-standard-32 \
  --zone=us-central1-a \
  --node-group=node-group-1
```

**Cost Optimization**:
- Committed use discounts apply to sole-tenant nodes
- Fill nodes completely to maximize utilization
- Use node affinity labels for workload placement
- Maintenance policies: restart-in-place or migrate-within-node-group

### Pricing Models and Cost Optimization

#### 1. Committed Use Discounts (CUD)
**1-Year Commitment**:
- 25% discount on most machine types
- 37% discount on memory-optimized
- Applies automatically to usage in same region

**3-Year Commitment**:
- 52% discount on most machine types
- 55% discount on memory-optimized
- Best for stable, long-term workloads

**Spend-Based Commitments**:
- Commit to spend amount ($25K, $100K, $1M+)
- Flexibility across machine types and regions
- 25-52% discounts based on commitment level

**Purchase Strategy**:
```bash
# Create resource-based commitment
gcloud compute commitments create commitment-1 \
  --plan=12-month \
  --resources=vcpu=100,memory=400GB \
  --region=us-central1

# Create spend-based commitment (via Console)
# Console > Compute Engine > Committed use discounts > Purchase commitment
```

#### 2. Sustained Use Discounts (SUD)
- Automatic discounts for running instances >25% of month
- Up to 30% discount for instances running entire month
- Applied automatically, no commitment required
- Stacks with CUD (use CUD first, then SUD)

#### 3. Preemptible VM Instances
**Characteristics**:
- Up to 80% discount compared to regular instances
- Can be terminated at any time (30-second warning)
- Maximum runtime: 24 hours
- No SLA, no live migration
- Not covered by committed use discounts

**Use Cases**:
- Batch processing jobs
- Fault-tolerant workloads
- Rendering, transcoding
- CI/CD pipelines
- Data analysis, ETL

**Best Practices**:
```bash
# Create preemptible instance
gcloud compute instances create preemptible-vm \
  --preemptible \
  --machine-type=n2-standard-8 \
  --zone=us-central1-a \
  --maintenance-policy=TERMINATE

# Use with managed instance groups for automatic restart
gcloud compute instance-templates create preemptible-template \
  --machine-type=n2-standard-4 \
  --preemptible
```

**Handling Preemption**:
- Monitor instance metadata for preemption signal
- Implement checkpoint/restart logic
- Use managed instance groups for auto-restart
- Store state externally (Cloud Storage, databases)

#### 4. Spot VMs
**Evolution from Preemptible**:
- Similar pricing (60-91% discount)
- No maximum runtime (can run indefinitely if capacity available)
- Dynamic pricing model
- Can be preempted at any time with 30-second warning

**Differences from Preemptible**:
| Feature | Preemptible VMs | Spot VMs |
|---------|----------------|----------|
| Max Runtime | 24 hours | No limit |
| Pricing | Fixed discount | Dynamic pricing |
| Availability | Higher | Varies by demand |
| Use Case | Batch jobs | Fault-tolerant long-running |

```bash
# Create spot VM
gcloud compute instances create spot-vm \
  --provisioning-model=SPOT \
  --instance-termination-action=STOP \
  --machine-type=n2-standard-8 \
  --zone=us-central1-a
```

### High Availability Patterns for Compute Engine

#### Multi-Zone Deployment
```
Region: us-central1
├── Zone A (us-central1-a)
│   ├── Instance Group A (3 instances)
│   └── Regional Persistent Disk (Replica 1)
├── Zone B (us-central1-b)
│   ├── Instance Group B (3 instances)
│   └── Regional Persistent Disk (Replica 2)
└── Zone F (us-central1-f)
    └── Instance Group F (3 instances)

Load Balancer (Regional/Global)
    └── Backend Service
        └── Instance Groups (A, B, F)
```

**Implementation**:
```bash
# Create regional managed instance group
gcloud compute instance-groups managed create regional-mig \
  --base-instance-name=app-server \
  --template=app-template \
  --size=9 \
  --region=us-central1 \
  --target-distribution-shape=EVEN

# Configure autoscaling
gcloud compute instance-groups managed set-autoscaling regional-mig \
  --region=us-central1 \
  --min-num-replicas=3 \
  --max-num-replicas=20 \
  --target-cpu-utilization=0.75 \
  --cool-down-period=90
```

#### Live Migration
- Default for most maintenance events
- VM moves to different host without downtime
- Transparent to applications
- Not available for: Preemptible VMs, GPU instances, local SSDs, some machine types

#### Regional Persistent Disks
**Features**:
- Synchronous replication between two zones
- RPO: 0 (no data loss)
- RTO: Minutes (manual failover)
- Performance: Similar to zonal PD
- Cost: 2x zonal PD cost

**Use Cases**:
- Critical databases requiring zero data loss
- Stateful applications needing zone-level HA
- Applications with aggressive RPO/RTO requirements

```bash
# Create regional persistent disk
gcloud compute disks create regional-disk-1 \
  --size=500GB \
  --type=pd-ssd \
  --region=us-central1 \
  --replica-zones=us-central1-a,us-central1-b

# Attach to instance
gcloud compute instances attach-disk instance-1 \
  --disk=regional-disk-1 \
  --zone=us-central1-a
```

### Compute Engine Decision Matrix

**Use When**:
- Full control over OS and environment required
- Legacy application migration (lift-and-shift)
- Specific licensing requirements (BYOL)
- GPU/TPU workloads for ML/AI
- Custom networking requirements
- Windows workloads
- Long-running stateful applications
- Specific kernel or OS requirements

**Avoid When**:
- Containerized applications (use GKE or Cloud Run)
- Serverless event-driven workloads (use Cloud Functions)
- Stateless HTTP services (use Cloud Run)
- Simple web apps (use App Engine)

**Key Considerations**:
- Manual or automated scaling configuration
- OS patch management (OS Patch Management service available)
- Higher operational overhead vs. managed services
- Most flexible option for custom requirements
- Best cost optimization with committed use discounts

## Google Kubernetes Engine (GKE) Architecture

### Overview
GKE is Google's managed Kubernetes service, offering enterprise-grade container orchestration. Understanding cluster modes, node configurations, and workload management is critical for architect-level decisions.

### Cluster Modes: Standard vs Autopilot

#### Standard Mode
**Architecture**:
```
GKE Standard Cluster
├── Control Plane (Google-Managed)
│   ├── API Server
│   ├── Scheduler
│   ├── Controller Manager
│   └── etcd
└── Node Pools (Customer-Managed)
    ├── Default Node Pool (e2-medium × 3)
    ├── High-Memory Pool (n2-highmem-8 × 2)
    └── GPU Pool (a2-highgpu-1g × 2)
```

**Characteristics**:
- Full control over node configuration
- Manual node pool management
- Flexible machine types and configurations
- Support for Windows Server nodes
- Ability to SSH into nodes
- Node-level customization (taints, labels, affinities)

**Use When**:
- Need specific node configurations
- Running privileged containers
- Custom security requirements
- Windows workloads
- Node-level troubleshooting required
- Specific networking configurations

**Pricing**:
- Cluster management fee: $0.10/hour per cluster
- Node costs: Pay for Compute Engine instances
- Control plane: Free for zonal, $0.10/hour for regional

#### Autopilot Mode
**Architecture**:
```
GKE Autopilot Cluster
├── Control Plane (Google-Managed)
│   └── Fully managed, no configuration
├── Nodes (Google-Managed, Abstracted)
│   ├── Auto-provisioned based on workload
│   ├── Auto-scaled to demand
│   └── Auto-repaired and upgraded
└── Workloads (Customer-Managed)
    ├── Deployments
    ├── StatefulSets
    └── Services
```

**Characteristics**:
- Fully managed nodes (no node pool management)
- Pay-per-pod pricing (not per node)
- Google optimizes node configuration
- Automatic bin-packing for cost efficiency
- Built-in security best practices
- No SSH access to nodes

**Use When**:
- Reduced operational overhead desired
- Standard containerized workloads
- Cost optimization through per-pod pricing
- Security and compliance requirements (CIS benchmarks)
- Development and staging environments
- Teams without deep Kubernetes expertise

**Pricing**:
- No cluster management fee
- Pod-level pricing: vCPU and memory requested
- Includes control plane, nodes, system pods
- Typically 20-30% more expensive per resource, but often cheaper overall

**Comparison Matrix**:
| Feature | Standard | Autopilot |
|---------|----------|-----------|
| Node Management | Manual | Automatic |
| Cluster Fee | $0.10/hr | None |
| Pricing Model | Per-node | Per-pod |
| Node Access | SSH available | No access |
| Machine Types | All types | Optimized selection |
| Windows Nodes | Supported | Not supported |
| Privileged Pods | Allowed | Restricted |
| GPU Support | Full support | Limited |
| Local SSD | Supported | Not supported |

### Node Pool Architecture

#### Node Pool Configuration
```bash
# Create cluster with multiple node pools
gcloud container clusters create production-cluster \
  --region=us-central1 \
  --num-nodes=1 \
  --machine-type=e2-medium \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=10

# Add compute-optimized node pool
gcloud container node-pools create compute-pool \
  --cluster=production-cluster \
  --region=us-central1 \
  --machine-type=c2-standard-8 \
  --num-nodes=0 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=5 \
  --node-taints=workload-type=compute:NoSchedule

# Add GPU node pool
gcloud container node-pools create gpu-pool \
  --cluster=production-cluster \
  --region=us-central1 \
  --machine-type=n1-standard-4 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --num-nodes=0 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=3 \
  --node-taints=workload-type=gpu:NoSchedule
```

#### Node Pool Strategies

**1. Multi-Tier Node Pools**:
```
Cluster Architecture
├── System Node Pool (e2-medium)
│   └── System pods, monitoring, logging
├── Application Node Pool (n2-standard-4)
│   └── General application workloads
├── Memory-Intensive Pool (n2-highmem-8)
│   └── Caching, in-memory databases
└── Batch Processing Pool (e2-standard-4, Spot VMs)
    └── Non-critical batch jobs
```

**2. Node Affinity Example**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: compute-intensive-app
spec:
  template:
    spec:
      nodeSelector:
        workload-type: compute
      tolerations:
      - key: workload-type
        operator: Equal
        value: compute
        effect: NoSchedule
```

**3. Cluster Autoscaler**:
- Automatically adds/removes nodes based on pod resource requests
- Works across multiple node pools
- Respects node pool constraints and taints
- Scale-down delay: 10 minutes default (configurable)
- Considers pod priority and preemption

**Configuration**:
```bash
# Enable cluster autoscaler with custom settings
gcloud container clusters update production-cluster \
  --region=us-central1 \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=20 \
  --autoscaling-profile=optimize-utilization

# Node pool specific autoscaling
gcloud container node-pools update app-pool \
  --cluster=production-cluster \
  --region=us-central1 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=10
```

### Workload Identity

**Traditional Approach (Not Recommended)**:
```
Pod → Service Account Key (JSON) → Google Cloud API
     (Security risk: key in container, rotation issues)
```

**Workload Identity (Recommended)**:
```
Pod → Kubernetes Service Account → Workload Identity → Google Service Account → Google Cloud API
     (No keys, automatic rotation, fine-grained permissions)
```

**Configuration**:
```bash
# Enable Workload Identity on cluster
gcloud container clusters create wi-cluster \
  --region=us-central1 \
  --workload-pool=PROJECT_ID.svc.id.goog

# Create Kubernetes service account
kubectl create serviceaccount app-ksa --namespace=default

# Create Google service account
gcloud iam service-accounts create app-gsa \
  --project=PROJECT_ID

# Bind Kubernetes SA to Google SA
gcloud iam service-accounts add-iam-policy-binding app-gsa@PROJECT_ID.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:PROJECT_ID.svc.id.goog[default/app-ksa]"

# Annotate Kubernetes service account
kubectl annotate serviceaccount app-ksa \
  iam.gke.io/gcp-service-account=app-gsa@PROJECT_ID.iam.gserviceaccount.com \
  --namespace=default
```

**Deployment with Workload Identity**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  serviceAccountName: app-ksa
  containers:
  - name: app
    image: gcr.io/project/app:latest
    # Automatically authenticated to Google Cloud APIs
```

**Benefits**:
- No service account keys in containers
- Automatic credential rotation
- Fine-grained IAM permissions per workload
- Audit logging of which pods access what resources
- Required for GKE security best practices

### Binary Authorization

**Purpose**: Enforce deploy-time security policies that ensure only trusted container images run in GKE.

**Architecture**:
```
Developer → Build Image → Sign Image → Push to Registry
                ↓
        Attestor creates attestation
                ↓
GKE → Binary Authorization → Check attestations → Allow/Deny deployment
```

**Implementation**:
```bash
# Enable Binary Authorization on cluster
gcloud container clusters update production-cluster \
  --region=us-central1 \
  --enable-binauthz

# Create attestor
gcloud container binauthz attestors create prod-attestor \
  --attestation-authority-note=prod-note \
  --attestation-authority-note-project=PROJECT_ID

# Create policy (YAML)
cat > policy.yaml <<EOF
admissionWhitelistPatterns:
- namePattern: gcr.io/PROJECT_ID/*
defaultAdmissionRule:
  requireAttestationsBy:
  - projects/PROJECT_ID/attestors/prod-attestor
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
globalPolicyEvaluationMode: ENABLE
EOF

# Import policy
gcloud container binauthz policy import policy.yaml
```

**Use Cases**:
- Prevent unsigned images from deploying
- Enforce CI/CD pipeline compliance
- Regulatory requirements (SOC 2, PCI-DSS)
- Multi-stage deployments (dev → staging → prod)
- Supply chain security

### GKE Enterprise (Formerly Anthos)

**Components**:
1. **Multi-cluster Management**: Manage GKE clusters across projects, regions, clouds
2. **Config Management**: GitOps-based configuration sync
3. **Service Mesh**: Istio-based traffic management, security, observability
4. **Policy Controller**: OPA-based policy enforcement
5. **Cloud Run for Anthos**: Serverless on GKE

**Architecture**:
```
GKE Enterprise Platform
├── Fleet Management (Hub)
│   ├── GKE Cluster (GCP us-central1)
│   ├── GKE Cluster (GCP europe-west1)
│   ├── Attached Cluster (AWS)
│   └── Attached Cluster (On-prem)
├── Config Sync
│   └── Git Repository → Syncs to all clusters
├── Policy Controller
│   └── Enforce constraints across fleet
└── Service Mesh
    └── Unified service mesh across clusters
```

**Config Management Example**:
```yaml
# config-sync.yaml
apiVersion: configmanagement.gke.io/v1
kind: ConfigManagement
metadata:
  name: config-management
spec:
  clusterName: production-cluster
  git:
    syncRepo: https://github.com/org/config-repo
    syncBranch: main
    secretType: ssh
    policyDir: config/
```

**Use Cases**:
- Multi-cloud Kubernetes deployments
- Hybrid cloud (on-prem + cloud)
- Consistent policy enforcement across clusters
- GitOps workflows
- Service mesh across multiple clusters
- Enterprise-grade security and compliance

### GKE Networking

#### VPC-Native Clusters (Alias IPs)
**Architecture**:
```
VPC Network (10.0.0.0/16)
├── Node Subnet (10.0.1.0/24)
│   └── Node IPs
├── Pod IP Range (10.1.0.0/16)
│   └── Pod IPs (routable within VPC)
└── Service IP Range (10.2.0.0/20)
    └── ClusterIP service IPs
```

**Benefits**:
- Pod IPs are routable within VPC (no NAT)
- Direct connectivity to other GCP resources
- VPC firewall rules apply to pods
- Supports Private Google Access
- Required for Shared VPC

**Configuration**:
```bash
# Create VPC-native cluster
gcloud container clusters create vpc-native-cluster \
  --region=us-central1 \
  --enable-ip-alias \
  --network=my-vpc \
  --subnetwork=gke-subnet \
  --cluster-secondary-range-name=pods \
  --services-secondary-range-name=services
```

#### Private GKE Clusters
**Private Cluster Architecture**:
```
Private GKE Cluster
├── Private Nodes (no external IP)
│   └── Access internet via Cloud NAT
├── Private Control Plane (optional)
│   └── Access via authorized networks or VPN
└── Workloads
    └── Access Google APIs via Private Google Access
```

**Configuration**:
```bash
# Create private cluster
gcloud container clusters create private-cluster \
  --region=us-central1 \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.0/28 \
  --enable-ip-alias \
  --network=my-vpc \
  --subnetwork=gke-subnet \
  --no-enable-basic-auth \
  --no-issue-client-certificate

# Add authorized network for control plane access
gcloud container clusters update private-cluster \
  --region=us-central1 \
  --enable-master-authorized-networks \
  --master-authorized-networks=203.0.113.0/24
```

**Use Cases**:
- Enhanced security posture
- Compliance requirements
- Prevent direct internet exposure
- Controlled access to control plane

### GKE High Availability Patterns

#### Regional Clusters
**Architecture**:
```
Regional GKE Cluster (us-central1)
├── Control Plane Replicas
│   ├── us-central1-a (etcd, API server, scheduler)
│   ├── us-central1-b (etcd, API server, scheduler)
│   └── us-central1-c (etcd, API server, scheduler)
└── Node Pools
    ├── us-central1-a (3 nodes)
    ├── us-central1-b (3 nodes)
    └── us-central1-c (3 nodes)
```

**Benefits**:
- 99.95% SLA (vs 99.5% for zonal)
- Control plane survives zone failure
- Automatic node distribution
- Zero downtime upgrades

**Cost**:
- 3x control plane cost ($0.30/hour vs $0.10/hour)
- Same node costs (regional node pool recommended)

#### Multi-Cluster Architectures

**Pattern 1: Active-Active Multi-Region**:
```
Global Load Balancer (GCLB)
├── Backend: GKE Cluster (us-central1)
│   └── Ingress → Services → Pods
└── Backend: GKE Cluster (europe-west1)
    └── Ingress → Services → Pods

Cloud SQL
├── Primary (us-central1)
└── Read Replica (europe-west1)
```

**Pattern 2: Hub-and-Spoke with GKE Enterprise**:
```
Management Hub
└── Config Sync, Policy Controller

Production Clusters
├── us-central1 (primary traffic)
├── europe-west1 (regional traffic)
└── asia-northeast1 (regional traffic)
```

### GKE Decision Matrix

**Use GKE Standard When**:
- Container-based microservices architecture
- Need Kubernetes ecosystem and portability
- Complex orchestration requirements
- Service mesh needed (Istio, Anthos Service Mesh)
- CI/CD pipelines for containers
- Multi-tenancy within cluster
- Windows workloads
- GPU-intensive workloads

**Use GKE Autopilot When**:
- Reduced operational overhead is priority
- Standard containerized workloads
- Development and staging environments
- Cost optimization through per-pod pricing
- Security-first approach (CIS benchmarks)
- Teams new to Kubernetes

**Avoid GKE When**:
- Simple stateless HTTP services (use Cloud Run)
- Event-driven functions (use Cloud Functions)
- Traditional VMs required (use Compute Engine)
- Simple web applications (use App Engine)

## App Engine Architecture

### Overview
App Engine is Google's original PaaS offering, providing a fully managed platform for web applications with automatic scaling and traffic management. Critical for scenarios requiring versioning and traffic splitting.

### Environment Types

#### Standard Environment
**Architecture**:
```
App Engine Standard
├── Application (Project-level resource)
│   └── Services (formerly modules)
│       ├── Default Service (required)
│       │   ├── Version 1 (20% traffic)
│       │   ├── Version 2 (80% traffic)
│       │   └── Instances (auto-scaled)
│       └── API Service
│           └── Version 1 (100% traffic)
```

**Characteristics**:
- Language-specific runtimes (Python, Java, Node.js, Go, PHP, Ruby)
- Sandboxed environment
- Sub-second startup (no cold start issues)
- Automatic scaling from 0 to thousands of instances
- Free tier available
- Network restrictions (no outbound except via URL Fetch API in older runtimes)

**Scaling Types**:
```yaml
# Automatic Scaling (default)
automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 0
  max_instances: 100
  min_pending_latency: 30ms
  max_pending_latency: automatic
  max_concurrent_requests: 10

# Basic Scaling (stays up after handling requests)
basic_scaling:
  max_instances: 11
  idle_timeout: 10m

# Manual Scaling (fixed number of instances)
manual_scaling:
  instances: 5
```

**Use Cases**:
- Public-facing web applications
- RESTful APIs
- Mobile backends
- Rapid prototyping
- Applications with variable traffic

#### Flexible Environment
**Architecture**:
- Runs in Docker containers on Compute Engine VMs
- More customization than Standard
- Full network access
- Can install dependencies
- Slower instance startup (minutes)

**Characteristics**:
- Custom runtimes (any language via Docker)
- SSH access to instances
- Can write to local disk (ephemeral)
- Access to background threads
- Support for WebSockets
- Minimum 1 instance always running (no scale to zero)

**Comparison**:
| Feature | Standard | Flexible |
|---------|----------|----------|
| Startup Time | Milliseconds | Minutes |
| Scale to Zero | Yes | No (min 1) |
| SSH Access | No | Yes |
| Custom Runtimes | Limited | Any Docker |
| Network Access | Restricted | Full |
| Pricing | Instance hours | vCPU/memory |
| Disk Write | Memory only | Ephemeral disk |
| Free Tier | Yes | No |

### Traffic Management and Splitting

**Traffic Splitting Strategies**:
```bash
# IP-based splitting (sticky by IP address)
gcloud app services set-traffic default \
  --splits=v1=0.2,v2=0.8 \
  --split-by=ip

# Cookie-based splitting (GOOGAPPUID cookie)
gcloud app services set-traffic default \
  --splits=v1=0.2,v2=0.8 \
  --split-by=cookie

# Random splitting
gcloud app services set-traffic default \
  --splits=v1=0.2,v2=0.8 \
  --split-by=random
```

**Deployment Patterns**:

**1. Blue-Green Deployment**:
```
1. Deploy new version (v2) with 0% traffic
2. Test v2 using versioned URL: https://v2-dot-service-dot-project.appspot.com
3. Migrate 100% traffic to v2
4. Keep v1 for rollback
```

```bash
# Deploy v2 without traffic
gcloud app deploy --no-promote

# Migrate all traffic
gcloud app services set-traffic default --splits=v2=1.0 --migrate

# Rollback if needed
gcloud app services set-traffic default --splits=v1=1.0 --migrate
```

**2. Canary Deployment**:
```
1. Deploy v2 with 5% traffic
2. Monitor metrics (errors, latency)
3. Gradually increase: 5% → 25% → 50% → 100%
4. Rollback if issues detected
```

**3. A/B Testing**:
```
1. Deploy v1 and v2 simultaneously
2. Split traffic 50/50 (or custom split)
3. Compare metrics for business KPIs
4. Choose winner based on data
```

### App Engine Configuration

**app.yaml Example (Standard)**:
```yaml
runtime: python39
service: default
instance_class: F2

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 2
  max_instances: 20

handlers:
- url: /static
  static_dir: static
  secure: always

- url: /.*
  script: auto
  secure: always

env_variables:
  DATABASE_URL: postgres://...

inbound_services:
- warmup
```

**Instance Classes**:
| Class | Memory | CPU | Cost Multiplier |
|-------|--------|-----|-----------------|
| F1 | 256 MB | 600 MHz | 1x |
| F2 | 512 MB | 1.2 GHz | 2x |
| F4 | 1 GB | 2.4 GHz | 4x |
| F4_1G | 2 GB | 2.4 GHz | 6x |

### App Engine Decision Matrix

**Use App Engine Standard When**:
- Simple web applications and APIs
- Rapid development/deployment required
- Automatic scaling from zero
- Minimal operational overhead desired
- Traffic splitting and versioning needed
- Supported runtime languages
- Cost optimization (free tier, scale to zero)

**Use App Engine Flexible When**:
- Custom runtime or dependencies required
- Need full network access
- SSH access for debugging
- WebSocket support needed
- Background threads required
- Can tolerate slower startup times

**Avoid App Engine When**:
- Full container orchestration needed (use GKE)
- Stateless HTTP-only services (use Cloud Run)
- Complex microservices architecture (use GKE)
- Need Windows environment

## Cloud Run Architecture

### Overview
Cloud Run is Google's fully managed serverless container platform that automatically scales containers from zero to production. It abstracts away infrastructure management while giving you container flexibility.

### Architecture Models

**Cloud Run (Fully Managed)**:
```
Request → Cloud Run Service → Container Instance
         ↓
    Auto-scaling (0-1000 instances)
         ↓
    Container runs code → Response
```

**Cloud Run for Anthos** (Deprecated, now part of GKE Enterprise):
- Runs on GKE clusters
- On-premises support
- More control over infrastructure

### Key Concepts

#### Container Requirements
- Listens on port defined by $PORT environment variable (default 8080)
- Stateless (no local disk persistence between requests)
- Container image stored in Artifact Registry or Container Registry
- Must respond to requests within timeout period (default 300s, max 3600s)
- Maximum container size: 32 GB memory, 8 vCPU

#### Scaling Behavior
**Concurrency**:
```
Service Configuration
├── Max Concurrency: 80 (default, max 1000)
│   └── Number of requests per container instance
├── Min Instances: 0 (default)
│   └── Keeps warm instances (reduces cold starts)
└── Max Instances: 100 (default 1000)
    └── Limits maximum scale
```

**Auto-scaling Logic**:
```
Current Instances = ceil(Incoming Requests / Max Concurrency per Instance)

Example:
- 400 concurrent requests
- Max concurrency: 80 per instance
- Instances needed: ceil(400/80) = 5 instances
```

**Configuration**:
```bash
# Deploy with custom scaling settings
gcloud run deploy api-service \
  --image=gcr.io/project/api:v1 \
  --region=us-central1 \
  --concurrency=80 \
  --min-instances=2 \
  --max-instances=50 \
  --cpu=2 \
  --memory=1Gi \
  --timeout=900s \
  --no-allow-unauthenticated

# Set minimum instances to reduce cold starts
gcloud run services update api-service \
  --region=us-central1 \
  --min-instances=5
```

### Traffic Management

**Revision Management**:
```
Cloud Run Service: api-service
├── Revision: api-service-v1 (20% traffic)
├── Revision: api-service-v2 (80% traffic)
└── Revision: api-service-v3 (0% traffic, testing)
```

**Traffic Splitting**:
```bash
# Gradual rollout (canary deployment)
gcloud run services update-traffic api-service \
  --region=us-central1 \
  --to-revisions=api-service-v2=10,api-service-v1=90

# Blue-green deployment
gcloud run services update-traffic api-service \
  --region=us-central1 \
  --to-revisions=api-service-v2=100

# Tag-based routing (direct access to specific revision)
gcloud run services update-traffic api-service \
  --region=us-central1 \
  --update-tags=staging=api-service-v3

# Access: https://staging---api-service-abc123-uc.a.run.app
```

### Authentication and Security

#### 1. Public Access (Unauthenticated)
```bash
gcloud run services add-iam-policy-binding api-service \
  --region=us-central1 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

#### 2. Authenticated Access (IAM)
```bash
# Require authentication
gcloud run deploy api-service \
  --no-allow-unauthenticated

# Grant specific user/service account
gcloud run services add-iam-policy-binding api-service \
  --region=us-central1 \
  --member="user:developer@company.com" \
  --role="roles/run.invoker"

# Service-to-service authentication
gcloud run services add-iam-policy-binding api-service \
  --region=us-central1 \
  --member="serviceAccount:frontend@project.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

**Calling with Authentication**:
```bash
# Using gcloud (user credentials)
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  https://api-service-abc123-uc.a.run.app

# Using service account key
curl -H "Authorization: Bearer $(gcloud auth print-identity-token --impersonate-service-account=sa@project.iam.gserviceaccount.com)" \
  https://api-service-abc123-uc.a.run.app
```

### Networking Patterns

#### 1. Default (Public Internet)
```
Internet → Cloud Run Service (public URL)
```

#### 2. Ingress Control
```bash
# Internal only (same project or VPC SC perimeter)
gcloud run deploy api-service \
  --ingress=internal

# Internal and Cloud Load Balancing
gcloud run deploy api-service \
  --ingress=internal-and-cloud-load-balancing
```

#### 3. VPC Connector (Egress)
```
Cloud Run → VPC Connector → VPC Network → Private Resources
                             ├── Cloud SQL
                             ├── Memorystore
                             └── Compute Engine VMs
```

**Configuration**:
```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create connector-1 \
  --region=us-central1 \
  --network=my-vpc \
  --range=10.8.0.0/28

# Deploy with VPC connector
gcloud run deploy api-service \
  --region=us-central1 \
  --vpc-connector=connector-1 \
  --vpc-egress=private-ranges-only
```

#### 4. Global Load Balancing
```
Global External Application Load Balancer
├── Backend: Cloud Run (us-central1)
├── Backend: Cloud Run (europe-west1)
└── Cloud CDN, Cloud Armor
```

### Multi-Region Architecture

**Deployment Pattern**:
```bash
# Deploy to multiple regions
for region in us-central1 europe-west1 asia-northeast1; do
  gcloud run deploy api-service \
    --image=gcr.io/project/api:v1 \
    --region=$region \
    --platform=managed
done

# Create external HTTPS load balancer
gcloud compute backend-services create api-backend \
  --global \
  --load-balancing-scheme=EXTERNAL_MANAGED

# Add serverless NEGs as backends
gcloud compute network-endpoint-groups create api-neg-us \
  --region=us-central1 \
  --network-endpoint-type=SERVERLESS \
  --cloud-run-service=api-service

gcloud compute backend-services add-backend api-backend \
  --global \
  --network-endpoint-group=api-neg-us \
  --network-endpoint-group-region=us-central1
```

### Cloud Run Decision Matrix

**Use Cloud Run When**:
- Stateless HTTP/HTTPS services
- Container-based applications
- Pay-per-request desired (cost optimization)
- Automatic scaling including to zero
- Minimal infrastructure management
- HTTP-triggered workloads
- Microservices architecture
- API backends

**Use Cloud Run for Jobs When**:
- Batch processing
- Scheduled tasks
- Data processing pipelines
- One-time or periodic execution

**Avoid Cloud Run When**:
- Stateful applications requiring persistent local storage
- Long-running background processes (>1 hour)
- WebSocket connections (not supported)
- Non-HTTP protocols (TCP/UDP)
- Need full Kubernetes features (use GKE)

## Cloud Functions Architecture

### Overview
Cloud Functions is Google's Function-as-a-Service (FaaS) platform for event-driven, serverless compute. Understanding the differences between generations is critical for the exam.

### Cloud Functions Generations

#### 1st Generation (Legacy)
**Characteristics**:
- Original Cloud Functions platform
- Limited to Node.js, Python, Go, Java, .NET, Ruby, PHP
- Maximum timeout: 540 seconds (9 minutes)
- Maximum memory: 8 GB
- No minimum instances
- Event-driven only (no direct HTTP invoke for some triggers)

**Architecture**:
```
Event Source → Pub/Sub → Cloud Functions (1st gen) → Execution
             ↓
    Cloud Storage, Firestore, Firebase, HTTP
```

#### 2nd Generation (Recommended)
**Built on Cloud Run**:
```
Cloud Functions 2nd Gen
    ↓ (Powered by)
Cloud Run + Eventarc
    ↓
Enhanced capabilities and flexibility
```

**Improvements over 1st Gen**:
- Longer request timeout: up to 60 minutes (vs 9 minutes)
- Larger instances: up to 16 GB memory, 4 vCPU (vs 8 GB, 2 vCPU)
- Minimum instances: Reduce cold starts
- Concurrency: Handle multiple requests per instance (up to 1000)
- More event sources via Eventarc (90+ event types)
- Traffic splitting and gradual rollouts
- Better integration with Cloud Run features

**Comparison Matrix**:
| Feature | 1st Gen | 2nd Gen |
|---------|---------|---------|
| Max Timeout | 540s | 3600s |
| Max Memory | 8 GB | 16 GB |
| Max vCPU | 2 | 4 |
| Concurrency | 1 | 1-1000 |
| Min Instances | 0 | 0-1000 |
| Traffic Splitting | No | Yes |
| Eventarc | No | Yes |
| Pricing Model | Invocations | Cloud Run |

### Event-Driven Architecture Patterns

#### 1. HTTP Functions
**Use Case**: RESTful APIs, webhooks, HTTP endpoints

```python
# Cloud Functions 2nd Gen (Python)
import functions_framework

@functions_framework.http
def hello_http(request):
    name = request.args.get('name', 'World')
    return f'Hello {name}!'
```

**Deployment**:
```bash
gcloud functions deploy hello-http \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=hello_http \
  --trigger-http \
  --allow-unauthenticated \
  --memory=512MB \
  --timeout=60s \
  --max-instances=100 \
  --min-instances=1
```

#### 2. Cloud Storage Triggers
**Use Case**: File processing, image resizing, data transformation

```
Cloud Storage Event
    ↓ (Object created/deleted/etc)
Eventarc
    ↓
Cloud Function
    ↓
Process file, transform, move to destination
```

**Example**:
```python
import functions_framework
from google.cloud import storage

@functions_framework.cloud_event
def process_file(cloud_event):
    data = cloud_event.data
    bucket_name = data['bucket']
    file_name = data['name']

    print(f'Processing file: {file_name} from bucket: {bucket_name}')
    # Process file logic here
```

**Deployment**:
```bash
gcloud functions deploy process-file \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=process_file \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=my-upload-bucket"
```

#### 3. Pub/Sub Triggers
**Use Case**: Asynchronous message processing, event streaming

```
Publisher → Pub/Sub Topic → Cloud Function (subscriber) → Processing
                                    ↓
                            Acknowledgment after processing
```

**Example**:
```python
import functions_framework
import base64
import json

@functions_framework.cloud_event
def process_pubsub(cloud_event):
    data = base64.b64decode(cloud_event.data['message']['data']).decode()
    message = json.loads(data)

    print(f'Processing message: {message}')
    # Process message logic
```

**Deployment**:
```bash
gcloud functions deploy process-pubsub \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=process_pubsub \
  --trigger-topic=my-topic \
  --retry  # Retry on failure
```

#### 4. Firestore Triggers
**Use Case**: Real-time data synchronization, data validation

```
Firestore Document Change (create/update/delete)
    ↓
Cloud Function
    ↓
Update related documents, send notifications, validate data
```

#### 5. Scheduled Functions (Cron Jobs)
**Use Case**: Periodic tasks, batch processing, data cleanup

```bash
# Create Cloud Scheduler job that triggers function
gcloud functions deploy scheduled-function \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=scheduled_task \
  --trigger-http \
  --no-allow-unauthenticated

# Create Cloud Scheduler job
gcloud scheduler jobs create http scheduled-job \
  --location=us-central1 \
  --schedule="0 2 * * *" \
  --uri="https://us-central1-project.cloudfunctions.net/scheduled-function" \
  --oidc-service-account-email=scheduler@project.iam.gserviceaccount.com
```

### Cold Start Optimization

**Strategies**:

1. **Minimum Instances (2nd Gen)**:
```bash
gcloud functions deploy api-function \
  --gen2 \
  --min-instances=3 \
  --max-instances=100
```

2. **Concurrency (2nd Gen)**:
```bash
# Handle multiple requests per instance
gcloud functions deploy api-function \
  --gen2 \
  --concurrency=80
```

3. **Global Scope Initialization**:
```python
# Initialize outside function (reused across invocations)
from google.cloud import storage
client = storage.Client()  # Reused

@functions_framework.http
def process_request(request):
    # Use pre-initialized client
    bucket = client.bucket('my-bucket')
    # ... rest of logic
```

### Cloud Functions Decision Matrix

**Use Cloud Functions 2nd Gen When**:
- Event-driven workloads
- Simple, single-purpose functions
- Integration with GCP services (Pub/Sub, Storage, Firestore)
- Rapid development and deployment
- Serverless event processing
- Cron jobs and scheduled tasks
- Lightweight API endpoints

**Use Cloud Functions 1st Gen When**:
- Already using 1st gen (migration not urgent)
- Firebase-specific triggers
- Legacy compatibility required

**Avoid Cloud Functions When**:
- Long-running processes (>60 minutes, use Cloud Run Jobs)
- Complex microservices (use Cloud Run or GKE)
- High concurrency per instance critical (use Cloud Run)
- Need traffic splitting and blue-green deployments (use Cloud Run directly)
- Stateful applications

## Storage Architecture Patterns

### Cloud Storage Patterns

**Data Lake Pattern**:
- Raw data in Standard class
- Processed data in separate buckets
- Lifecycle policies for archival
- IAM and ACLs for access control
- Regional for performance, Multi-Regional for availability

**Content Delivery Pattern**:
- Cloud Storage for origin
- Cloud CDN for global distribution
- Signed URLs for private content
- Load balancing for high availability
- Versioning for rollback

**Backup and Archive Pattern**:
- Nearline for monthly access
- Coldline for quarterly access
- Archive for long-term retention
- Object lifecycle management
- Retention policies for compliance

### Persistent Disk Patterns

**Database Storage**:
- SSD for high IOPS requirements
- Standard for sequential workloads
- Snapshots for backup
- Regional PD for HA
- Sizing for performance needs

**Application Storage**:
- Boot disk optimization
- Separate data disks
- Snapshot scheduling
- Local SSD for extreme performance
- Read-only disk sharing

## Network Architecture

### VPC Design Patterns

**Hub-and-Spoke**:
- Central hub VPC for shared services
- Spoke VPCs for workloads
- VPC Peering or VPN connectivity
- Centralized network management
- Reduced complexity

**Mesh Network**:
- Full VPC Peering between all VPCs
- Direct communication paths
- Higher complexity
- Maximum performance
- More interconnections to manage

**Shared VPC**:
- Host project with VPC
- Service projects attached
- Centralized network admin
- Project-level isolation
- Organization-level management

## Load Balancing Architecture

### Overview
Google Cloud offers comprehensive load balancing solutions designed for global scale. Understanding when to use each type is critical for Professional Cloud Architect scenarios.

### Load Balancer Types Decision Matrix

```
Choose Load Balancer Based On:

Traffic Type        Protocol    Scope           Load Balancer Type
─────────────────────────────────────────────────────────────────────
External HTTP(S)    L7/HTTP     Global          External Application LB (HTTP(S))
External HTTP(S)    L7/HTTP     Regional        Regional External Application LB
External TCP/UDP    L4          Global          External Network LB (Premium Tier)
External TCP/UDP    L4          Regional        Regional External Network LB
Internal HTTP(S)    L7/HTTP     Regional        Internal Application LB
Internal HTTP(S)    L7/HTTP     Cross-region    Cross-region Internal Application LB
Internal TCP/UDP    L4          Regional        Internal Network LB (pass-through)
Internal TCP/UDP    L4          Cross-region    Cross-region Internal Network LB
```

### External Application Load Balancer (HTTP(S))

**Architecture**:
```
Global External Application Load Balancer
    ↓
Anycast IP (Single global IP)
    ↓
Google Front End (GFE) - Edge locations worldwide
    ↓
Cloud CDN (Optional)
    ↓
Cloud Armor (Optional - DDoS, WAF)
    ↓
URL Map (Routing rules)
    ├── /api/* → Backend Service 1 (us-central1)
    ├── /images/* → Backend Bucket (Cloud Storage + CDN)
    └── /* → Backend Service 2 (multi-region)
        ├── Instance Group (us-central1) - 60% traffic
        ├── Instance Group (europe-west1) - 30% traffic
        └── NEG - Cloud Run (asia-northeast1) - 10% traffic
```

**Key Features**:
- **Global distribution**: Single anycast IP, routes to nearest healthy backend
- **Layer 7 routing**: Host, path, header-based routing
- **Content-based routing**: Different backends for different URL patterns
- **Cloud CDN integration**: Cache static content at edge locations
- **SSL/TLS termination**: Managed SSL certificates
- **Cloud Armor**: DDoS protection and WAF rules
- **WebSocket support**: Full-duplex communication
- **HTTP/2 and QUIC**: Modern protocols supported

**Configuration Example**:
```bash
# Create backend service
gcloud compute backend-services create web-backend \
  --protocol=HTTP \
  --port-name=http \
  --health-checks=http-health-check \
  --global \
  --enable-cdn \
  --cache-mode=CACHE_ALL_STATIC

# Add instance groups as backends
gcloud compute backend-services add-backend web-backend \
  --instance-group=ig-us-central1 \
  --instance-group-zone=us-central1-a \
  --balancing-mode=UTILIZATION \
  --max-utilization=0.8 \
  --capacity-scaler=1.0 \
  --global

gcloud compute backend-services add-backend web-backend \
  --instance-group=ig-europe-west1 \
  --instance-group-zone=europe-west1-b \
  --balancing-mode=UTILIZATION \
  --max-utilization=0.8 \
  --global

# Create URL map
gcloud compute url-maps create web-map \
  --default-service=web-backend

# Add path rules
gcloud compute url-maps add-path-matcher web-map \
  --path-matcher-name=api-matcher \
  --default-service=web-backend \
  --path-rules="/api/*=api-backend,/static/*=storage-backend"

# Create SSL certificate
gcloud compute ssl-certificates create web-ssl-cert \
  --domains=www.example.com,example.com \
  --global

# Create target HTTPS proxy
gcloud compute target-https-proxies create web-https-proxy \
  --url-map=web-map \
  --ssl-certificates=web-ssl-cert

# Create forwarding rule (creates the anycast IP)
gcloud compute forwarding-rules create web-forwarding-rule \
  --address=web-ip \
  --target-https-proxy=web-https-proxy \
  --global \
  --ports=443
```

**Advanced Routing Patterns**:

**1. Host and Path-Based Routing**:
```yaml
URL Map Rules:
  api.example.com/v1/* → API Backend v1
  api.example.com/v2/* → API Backend v2
  www.example.com/images/* → Cloud Storage Backend + CDN
  www.example.com/* → Web Backend
```

**2. Header-Based Routing**:
```bash
# Route based on custom headers (e.g., API version)
gcloud compute url-maps add-header-action web-map \
  --header-name=X-API-Version \
  --header-value=v2 \
  --backend-service=api-backend-v2
```

**3. Traffic Steering (Weighted Traffic)**:
```bash
# Canary deployment: 90% to stable, 10% to canary
gcloud compute backend-services update web-backend \
  --global \
  --weighted-backend-service=stable-backend=90,canary-backend=10
```

### Cloud CDN Integration

**Architecture**:
```
User Request
    ↓
CDN Edge Location (Cache Hit?)
    ├── Yes → Return Cached Content (< 10ms latency)
    └── No → Forward to Origin (Backend)
            ↓
        Backend processes request
            ↓
        Response cached at edge (TTL-based)
            ↓
        Response returned to user
```

**Configuration**:
```bash
# Enable CDN on backend service
gcloud compute backend-services update web-backend \
  --enable-cdn \
  --cache-mode=CACHE_ALL_STATIC \
  --default-ttl=3600 \
  --max-ttl=86400 \
  --client-ttl=1800 \
  --global

# Configure cache keys
gcloud compute backend-services update web-backend \
  --cache-key-include-protocol \
  --cache-key-include-host \
  --cache-key-include-query-string \
  --global

# Negative caching (cache 404s)
gcloud compute backend-services update web-backend \
  --negative-caching \
  --negative-caching-policy=404=300,500=10 \
  --global
```

**Cache Control Headers**:
```
Prioritization: Response Headers > Backend Configuration
- Cache-Control: public, max-age=3600
- Cache-Control: private, no-store (not cached)
- Cache-Control: no-cache (revalidate every time)
```

**Use Cases**:
- Static content delivery (images, CSS, JavaScript)
- Video streaming (HLS, DASH)
- API responses (with appropriate cache headers)
- Software distribution (downloads)
- Mobile app assets

### Cloud Armor (Security)

**Features**:
- DDoS protection (L3, L4, L7)
- WAF (Web Application Firewall)
- IP allowlist/denylist
- Geo-based access control
- Rate limiting
- Bot management
- Preconfigured WAF rules (OWASP Top 10)

**Configuration**:
```bash
# Create security policy
gcloud compute security-policies create web-security-policy \
  --description="Security policy for web application"

# Add rule to block specific countries
gcloud compute security-policies rules create 1000 \
  --security-policy=web-security-policy \
  --expression="origin.region_code == 'CN' || origin.region_code == 'RU'" \
  --action=deny-403 \
  --description="Block traffic from specific countries"

# Add rate limiting rule
gcloud compute security-policies rules create 2000 \
  --security-policy=web-security-policy \
  --expression="true" \
  --action=rate-based-ban \
  --rate-limit-threshold-count=100 \
  --rate-limit-threshold-interval-sec=60 \
  --ban-duration-sec=600 \
  --description="Rate limit: 100 requests per minute"

# Add SQLi protection (preconfigured rule)
gcloud compute security-policies rules create 3000 \
  --security-policy=web-security-policy \
  --expression="evaluatePreconfiguredExpr('sqli-stable')" \
  --action=deny-403 \
  --description="Block SQL injection attacks"

# Apply to backend service
gcloud compute backend-services update web-backend \
  --security-policy=web-security-policy \
  --global
```

### Internal Application Load Balancer

**Architecture**:
```
VPC Network
    ↓
Internal Application Load Balancer (Regional or Cross-Region)
    ├── Internal IP: 10.1.0.10
    └── Proxy-only Subnet: 10.2.0.0/24
        ↓
    URL Map (Layer 7 routing)
        ├── /api/* → Backend Service 1 (GKE)
        ├── /auth/* → Backend Service 2 (Cloud Run)
        └── /* → Backend Service 3 (Compute Engine)
```

**Use Cases**:
- Microservices communication within VPC
- Internal APIs and services
- Multi-tier applications (web → app → database)
- Service mesh traffic management
- Cross-region internal load balancing

**Configuration**:
```bash
# Create proxy-only subnet (required for internal ALB)
gcloud compute networks subnets create proxy-only-subnet \
  --network=my-vpc \
  --region=us-central1 \
  --range=10.2.0.0/24 \
  --purpose=REGIONAL_MANAGED_PROXY

# Create backend service
gcloud compute backend-services create internal-web-backend \
  --load-balancing-scheme=INTERNAL_MANAGED \
  --protocol=HTTP \
  --region=us-central1 \
  --health-checks=internal-health-check

# Create URL map
gcloud compute url-maps create internal-url-map \
  --default-service=internal-web-backend \
  --region=us-central1

# Create target HTTP proxy
gcloud compute target-http-proxies create internal-http-proxy \
  --url-map=internal-url-map \
  --region=us-central1

# Create forwarding rule (internal IP)
gcloud compute forwarding-rules create internal-lb-rule \
  --load-balancing-scheme=INTERNAL_MANAGED \
  --network=my-vpc \
  --subnet=default \
  --address=10.1.0.10 \
  --target-http-proxy=internal-http-proxy \
  --region=us-central1 \
  --ports=80
```

### Network Load Balancer (TCP/UDP)

**External Network Load Balancer**:
```
Regional External Network Load Balancer
    ↓
Regional External IP
    ↓
Backend Service (Layer 4 - TCP/UDP)
    └── Instance Groups in single region
        ├── Protocol: TCP, UDP, or ESP
        └── Port forwarding rules
```

**Use Cases**:
- Non-HTTP(S) protocols (gaming, streaming, custom protocols)
- TCP/UDP load balancing
- Legacy applications
- IoT device communication
- VoIP and real-time communications

**Configuration**:
```bash
# Create backend service for TCP
gcloud compute backend-services create tcp-backend \
  --protocol=TCP \
  --health-checks=tcp-health-check \
  --region=us-central1 \
  --load-balancing-scheme=EXTERNAL

# Create forwarding rule
gcloud compute forwarding-rules create tcp-lb-rule \
  --region=us-central1 \
  --load-balancing-scheme=EXTERNAL \
  --network-tier=PREMIUM \
  --address=tcp-external-ip \
  --ports=8080-8090 \
  --backend-service=tcp-backend
```

### Internal Network Load Balancer (Pass-through)

**Architecture**:
```
VPC Network
    ↓
Internal Network Load Balancer
    ├── Internal IP: 10.1.0.20
    └── Pass-through (no proxying)
        ↓
    Backend Service (TCP/UDP)
        └── Instance Groups
            ├── Preserve client IP
            └── Protocol: TCP, UDP, L3_DEFAULT
```

**Use Cases**:
- Internal TCP/UDP load balancing
- Database connection pooling
- Message queue load balancing
- Internal microservices (non-HTTP)
- Legacy application support

### Health Checks

**Health Check Types**:
- **HTTP/HTTPS**: Check specific URL path
- **TCP**: Check TCP connection
- **SSL**: Check SSL handshake
- **HTTP/2**: Check HTTP/2 connection
- **gRPC**: Check gRPC health checking protocol

**Configuration**:
```bash
# Create comprehensive HTTP health check
gcloud compute health-checks create http web-health-check \
  --port=80 \
  --request-path=/health \
  --check-interval=10s \
  --timeout=5s \
  --unhealthy-threshold=3 \
  --healthy-threshold=2 \
  --proxy-header=NONE

# Advanced health check with logging
gcloud compute health-checks create https secure-health-check \
  --port=443 \
  --request-path=/api/health \
  --check-interval=15s \
  --timeout=10s \
  --unhealthy-threshold=2 \
  --healthy-threshold=2 \
  --enable-logging \
  --proxy-header=PROXY_V1
```

**Health Check Best Practices**:
- Implement dedicated health check endpoints
- Check interval: 10-30 seconds (balance between quick detection and overhead)
- Timeout: Less than check interval
- Unhealthy threshold: 2-3 (avoid flapping)
- Log health check results for debugging
- Use different health checks for different services

### Multi-Region Load Balancing Patterns

#### Pattern 1: Active-Active with Failover
```
Global Load Balancer (Anycast IP)
├── us-central1 (Primary) - 60% traffic
│   └── Auto-fails to other regions if unhealthy
├── europe-west1 (Secondary) - 30% traffic
│   └── Serves European users primarily
└── asia-northeast1 (Tertiary) - 10% traffic
    └── Serves Asian users primarily

Health Checks detect failures
    ↓
Automatic traffic redistribution
    ↓
RTO: < 30 seconds
```

#### Pattern 2: Geo-Proximity Routing
```
User Location → Nearest Healthy Backend
    ├── US Users → us-central1
    ├── EU Users → europe-west1
    └── Asia Users → asia-northeast1

Benefits:
- Reduced latency (geographic proximity)
- Automatic failover to next-nearest region
- Optimal user experience
```

### Load Balancing Cost Optimization

**Pricing Components**:
1. **Forwarding rules**: $0.025/hour per rule
2. **Data processing**: $0.008-$0.010 per GB (varies by type)
3. **Cloud CDN**: $0.02-$0.04 per GB cache egress (cheaper than origin)
4. **Cross-region egress**: Expensive (minimize with regional backends)

**Cost Optimization Strategies**:
- Use Cloud CDN to reduce origin traffic (70-90% cache hit rate)
- Regional load balancers for regional applications (avoid global when not needed)
- Consolidate forwarding rules (support multiple domains on one IP)
- Internal load balancing for internal traffic (free data processing)
- Premium tier for global, Standard tier for regional (Standard tier cheaper)

## Best Practices

### Compute Best Practices
1. **Right-sizing**: Use machine type recommendations
2. **Preemptible VMs**: Use for batch and fault-tolerant workloads
3. **Committed Use**: Purchase for predictable workloads
4. **Auto-scaling**: Configure based on actual metrics
5. **Regional Distribution**: Deploy across zones for HA
6. **Health Checks**: Implement for all production workloads
7. **Instance Templates**: Use for consistent deployments
8. **Startup Scripts**: Automate instance configuration

### Storage Best Practices
1. **Storage Class Selection**: Match to access patterns
2. **Lifecycle Policies**: Automate class transitions
3. **Regional Placement**: Consider data gravity
4. **Encryption**: Use CMEK for sensitive data
5. **Access Control**: Apply principle of least privilege
6. **Retention Policies**: Implement for compliance
7. **Monitoring**: Track storage usage and costs
8. **Versioning**: Enable for critical data

### Network Best Practices
1. **Subnet Planning**: Adequate IP space, avoid overlap
2. **Firewall Hierarchy**: Use tags and service accounts
3. **Private Google Access**: Enable for secure API access
4. **Cloud NAT**: For private instance internet access
5. **VPC Flow Logs**: Enable for troubleshooting
6. **Load Balancer Health Checks**: Configure appropriately
7. **SSL Certificates**: Use managed certificates
8. **Global Distribution**: Use for worldwide applications

## Migration Strategies

### Overview
Understanding migration patterns is critical for Professional Cloud Architect scenarios. The exam frequently tests knowledge of choosing the right migration strategy based on requirements.

### Migration Strategy Framework

```
Migration Complexity vs. Cloud Benefits

High Cloud Benefits  │        Re-architect        Modernize
                    │        (Cloud-native)      (Containers)
                    │            │                    │
                    │            │                    │
Cloud Benefits      │        Re-platform         Lift-and-shift
                    │        (Minimal changes)   (Rehost)
                    │            │                    │
Low Cloud Benefits  │────────────┼────────────────────┼──────
                         Low            Migration Effort         High
```

### 1. Lift-and-Shift (Rehost)

**Definition**: Move applications to cloud with minimal or no changes.

**Strategy**:
```
On-Premises VM → Compute Engine VM
    ├── Same OS, same configuration
    ├── Use Migrate for Compute Engine
    └── Minimal application changes
```

**Use When**:
- Quick migration needed (tight timeline)
- Applications work well as-is
- Limited resources for refactoring
- Proof of concept or initial cloud adoption
- Need to exit data center quickly
- Application dependencies unclear

**GCP Services**:
- **Migrate for Compute Engine**: Agent-based or agentless migration
- **Compute Engine**: Target platform for VMs
- **Cloud VPN/Interconnect**: Hybrid connectivity during migration
- **Cloud Storage**: Staging area for data

**Implementation**:
```bash
# Install Migrate for Compute Engine
# 1. Create migration manager in GCP
# 2. Deploy migration connector in source environment
# 3. Discover and assess workloads

# Create migration wave
gcloud migration waves create wave-1 \
  --project=PROJECT_ID \
  --description="First migration wave - web servers"

# Add VMs to migration wave
gcloud migration vms add vm-web-01 \
  --wave=wave-1 \
  --target-project=PROJECT_ID \
  --target-zone=us-central1-a \
  --machine-type=n2-standard-4

# Test clone (non-disruptive)
gcloud migration vms create-clone vm-web-01 \
  --wave=wave-1

# Cutover (actual migration)
gcloud migration vms cutover vm-web-01 \
  --wave=wave-1
```

**Challenges**:
- Licensing (BYOL vs. license-included)
- Performance differences
- Network configuration changes
- Limited cloud benefits initially
- Technical debt migrated

**Post-Migration Optimization**:
1. Right-size machine types
2. Use committed use discounts
3. Implement managed instance groups
4. Add load balancing
5. Enable backup and disaster recovery

### 2. Re-platform (Lift-and-Optimize)

**Definition**: Move to cloud with minor optimizations to leverage cloud services.

**Strategy**:
```
On-Premises Architecture → GCP Optimized
    ├── Self-managed DB → Cloud SQL
    ├── File server → Filestore or Cloud Storage
    ├── Load balancer appliance → Cloud Load Balancing
    └── VMs remain, but optimized
```

**Use When**:
- Want some cloud benefits without full re-architecture
- Database can be migrated to managed service
- Application supports external services
- Balance between speed and modernization
- Incremental cloud adoption

**Common Re-platforming Patterns**:

**Pattern 1: Database Migration**:
```
Before: VM with self-managed MySQL
After: Cloud SQL for MySQL
Benefits:
- Automated backups
- High availability
- Read replicas
- Automatic patching
- Reduced operational overhead
```

**Implementation**:
```bash
# Export from source database
mysqldump -u root -p --databases app_db > app_db.sql

# Upload to Cloud Storage
gsutil cp app_db.sql gs://migration-bucket/

# Import to Cloud SQL
gcloud sql import sql cloudsql-instance \
  gs://migration-bucket/app_db.sql \
  --database=app_db

# Update application connection string
# From: localhost:3306
# To: CLOUD_SQL_INSTANCE_IP:3306 or unix socket
```

**Pattern 2: File Storage Migration**:
```
Before: NFS file server
After: Filestore (managed NFS) or Cloud Storage
Benefits:
- Scalable storage
- No server management
- Pay for what you use
- High performance
```

**Pattern 3: Add Managed Services**:
- Self-managed Redis → Memorystore
- Self-managed messaging → Pub/Sub
- Self-managed load balancer → Cloud Load Balancing
- Manual backups → Automated snapshots

### 3. Re-architect (Cloud-Native)

**Definition**: Redesign applications to be cloud-native, leveraging serverless and managed services.

**Strategy**:
```
Monolithic Application → Cloud-Native Architecture
    ├── Monolith → Microservices (GKE/Cloud Run)
    ├── Manual scaling → Auto-scaling
    ├── Self-managed → Fully managed services
    └── Regional → Multi-region HA
```

**Use When**:
- Maximum cloud benefits desired
- Application needs modernization anyway
- Scalability and resilience critical
- Development resources available
- Long-term cloud strategy
- Competitive advantage through technology

**Re-architecture Patterns**:

**Pattern 1: Monolith to Microservices**:
```
Before:
Single Monolithic Application (VM)
    └── All functionality in one codebase

After:
Microservices Architecture
├── API Gateway (Cloud Endpoints/Apigee)
├── User Service (Cloud Run)
├── Product Service (Cloud Run)
├── Order Service (GKE)
├── Payment Service (Cloud Functions)
└── Notification Service (Cloud Functions)

Benefits:
- Independent scaling
- Technology diversity
- Faster deployments
- Better fault isolation
```

**Pattern 2: Event-Driven Architecture**:
```
Before:
Synchronous, tightly-coupled

After:
Event-Driven, loosely-coupled
    ↓
Cloud Storage → Cloud Functions → Pub/Sub → Cloud Run → BigQuery
    ├── Asynchronous processing
    ├── Loose coupling
    ├── Scalable
    └── Resilient
```

**Pattern 3: Serverless**:
```
Before: Always-on VMs

After: Serverless (Cloud Run, Cloud Functions)
Benefits:
- Pay-per-use
- Auto-scaling (including to zero)
- No server management
- Built-in HA
```

### 4. Modernize (Containers)

**Definition**: Containerize applications for portability and orchestration.

**Strategy**:
```
Traditional VMs → Containers → GKE
    ├── Application → Docker container
    ├── Manual deployment → CI/CD pipeline
    ├── Static infrastructure → Dynamic orchestration
    └── Single cloud → Multi-cloud ready
```

**Use When**:
- Application suits containerization
- Need Kubernetes orchestration
- Multi-cloud strategy
- Development team has container skills
- Want portability
- Microservices architecture

**Migrate for Anthos**:
```
On-Premises VM/Application
    ↓ (Automated migration)
Migrate for Anthos
    ├── Discover workloads
    ├── Generate Dockerfile
    ├── Build container image
    └── Generate Kubernetes manifests
        ↓
Deploy to GKE
```

**Implementation**:
```bash
# Install migctl CLI
gcloud components install migctl

# Create migration
migctl migration create my-migration \
  --source-type=vmware \
  --source-name=vcenter-source

# Generate migration plan
migctl migration plan my-migration

# Execute migration
migctl migration execute my-migration

# Deploy to GKE
kubectl apply -f generated-manifests/
```

### Migration Tool Selection

| Source | Target | Tool |
|--------|--------|------|
| VMs (VMware, AWS, Azure) | Compute Engine | Migrate for Compute Engine |
| VMs/Apps | GKE Containers | Migrate for Anthos |
| Databases | Cloud SQL | Database Migration Service |
| On-prem storage | Cloud Storage | Storage Transfer Service |
| AWS S3 | Cloud Storage | Storage Transfer Service |
| Large datasets | Cloud Storage | Transfer Appliance (offline) |
| Continuous sync | Multi-cloud | Cloud Storage Transfer |

### Migration Best Practices

**Pre-Migration**:
1. **Assess**: Inventory applications, dependencies, data
2. **Design**: Target architecture, network design, security
3. **Pilot**: Migrate non-critical application first
4. **Plan**: Migration waves, rollback plans, testing strategy

**During Migration**:
1. **Validate**: Test functionality after migration
2. **Monitor**: Track performance, errors, user experience
3. **Communicate**: Keep stakeholders informed
4. **Document**: Record changes, configurations, lessons learned

**Post-Migration**:
1. **Optimize**: Right-size, enable monitoring, implement best practices
2. **Secure**: Review IAM, firewall rules, encryption
3. **Modernize**: Plan next phase of cloud optimization
4. **Train**: Educate team on cloud operations

## Architecture Decision Scenarios

### Scenario 1: Global E-commerce Platform

**Requirements**:
- 10M+ daily active users globally
- 99.99% availability SLA
- < 100ms latency for 95th percentile
- PCI-DSS compliance
- Peak traffic 10x during sales events
- Real-time inventory management

**Solution Architecture**:
```
Global Architecture
├── External Application Load Balancer (Anycast IP)
│   ├── Cloud CDN (static assets, product images)
│   └── Cloud Armor (DDoS protection, WAF)
│
├── Frontend (Multi-region)
│   ├── Cloud Run (us-central1)
│   ├── Cloud Run (europe-west1)
│   └── Cloud Run (asia-northeast1)
│
├── API Layer (GKE)
│   ├── GKE Cluster (us-central1) - Regional cluster
│   ├── GKE Cluster (europe-west1) - Regional cluster
│   └── GKE Cluster (asia-northeast1) - Regional cluster
│       ├── Workload Identity enabled
│       ├── Binary Authorization for security
│       └── Horizontal Pod Autoscaling
│
├── Database Layer
│   ├── Cloud Spanner (global, strongly consistent)
│   │   └── Multi-region configuration
│   └── Memorystore Redis (regional, per region)
│
├── Inventory Service
│   ├── Cloud Run (event-driven)
│   └── Firestore (real-time sync)
│
└── Payment Processing (PCI-DSS)
    ├── Dedicated VPC (isolated)
    ├── Private GKE cluster
    ├── VPC Service Controls perimeter
    └── Cloud SQL (encrypted, audit logging)
```

**Key Design Decisions**:
1. **Global Load Balancing**: Single anycast IP, routes to nearest healthy backend
2. **Cloud Run for frontend**: Scales to zero during low traffic, rapid scaling during peaks
3. **GKE for API**: Complex business logic, service mesh (Istio), auto-scaling
4. **Cloud Spanner**: Global transactions, strong consistency, 99.999% SLA
5. **Memorystore**: Sub-millisecond latency for frequently accessed data
6. **Cloud CDN**: Offload 80%+ traffic, reduce origin load, lower latency
7. **Cloud Armor**: Rate limiting, geo-restrictions, WAF for OWASP Top 10

**Cost Optimization**:
- Cloud Run: Pay-per-request (cost-effective for variable traffic)
- GKE Autopilot: Per-pod pricing, reduced operational overhead
- Cloud CDN: 75% cache hit rate = 75% cost reduction on egress
- Committed use discounts: 3-year commitment for Spanner, GKE nodes
- **Estimated Monthly Cost**: ~$25,000-$50,000 (depends on traffic)

**Exam Tips for This Scenario**:
- Global Load Balancer with Cloud CDN is key for global latency
- Cloud Spanner for globally distributed transactional data
- PCI-DSS requires VPC Service Controls, private clusters, audit logging
- Auto-scaling is critical for 10x traffic spikes
- Regional Memorystore per region (not global) for low latency

### Scenario 2: Big Data Analytics Platform

**Requirements**:
- Ingest 5TB data per day from multiple sources
- Real-time streaming analytics
- Batch processing nightly
- Data retention: 7 years
- Cost optimization priority
- Support for data science team (ML workloads)

**Solution Architecture**:
```
Data Ingestion
├── Pub/Sub (streaming data ingestion)
│   ├── IoT devices → Pub/Sub
│   ├── Application logs → Pub/Sub
│   └── API events → Pub/Sub
│
├── Dataflow (stream processing)
│   ├── Transformation, enrichment
│   ├── Windowing, aggregation
│   └── Output to BigQuery (real-time)
│
├── Batch Processing
│   ├── Cloud Storage (data lake)
│   │   └── Lifecycle management (Standard → Nearline → Coldline → Archive)
│   ├── Dataproc (Spark jobs) on Preemptible VMs
│   │   └── Scheduled nightly processing
│   └── BigQuery (data warehouse)
│       └── Partitioned and clustered tables
│
├── Machine Learning
│   ├── Agent Platform Workbench (formerly Vertex AI Workbench; Jupyter notebooks)
│   ├── Agent Platform Training (formerly Vertex AI Training; custom models)
│   │   └── A2 instances with GPUs (on-demand)
│   └── Agent Platform Prediction (formerly Vertex AI Prediction; model serving)
│       └── Cloud Run (custom serving)
│
└── Visualization
    ├── BigQuery → Looker/Data Studio
    └── Real-time dashboards
```

**Key Design Decisions**:
1. **Pub/Sub**: Durable, at-least-once delivery, global service, handles spikes
2. **Dataflow**: Fully managed, auto-scaling, exactly-once processing
3. **Cloud Storage lifecycle**: Auto-transition to cheaper tiers (80% cost savings)
4. **Dataproc on Preemptible VMs**: 80% cost savings for batch jobs
5. **BigQuery partitioning**: Query only relevant data, lower costs
6. **Spot VMs for ML training**: 60-90% savings, fault-tolerant training jobs

**Cost Optimization Strategies**:
- Preemptible VMs for Dataproc: $0.01/vCPU-hour vs $0.05 regular
- Cloud Storage lifecycle: $0.020/GB (Standard) → $0.010 (Nearline) → $0.004 (Coldline)
- BigQuery: $5/TB queried (use partitioning/clustering to reduce scanned data)
- Dataflow: Use streaming engine (better resource utilization)
- **Estimated Monthly Cost**: ~$15,000-$30,000

**Exam Tips**:
- Pub/Sub for streaming ingestion (not Cloud Functions for high volume)
- Dataflow for stream processing (not self-managed Spark on GKE)
- BigQuery for analytics (not self-managed database)
- Lifecycle policies critical for long-term storage cost optimization
- Preemptible VMs for batch jobs (with checkpointing)

### Scenario 3: Enterprise SaaS Application (Multi-Tenant)

**Requirements**:
- 500 enterprise customers (multi-tenancy)
- Tenant isolation (data and compute)
- 99.95% SLA per tenant
- Per-tenant customization
- SOC 2 Type II compliance
- Disaster recovery: RPO 1 hour, RTO 2 hours

**Solution Architecture**:
```
Multi-Tenant Architecture
├── Tenant Routing Layer
│   ├── Cloud Load Balancer
│   └── Cloud Endpoints (API Gateway)
│       └── Tenant identification (subdomain/API key)
│
├── Application Layer (GKE Standard)
│   ├── Namespace per tenant (soft isolation)
│   ├── Dedicated node pools for premium tier
│   ├── Network policies for isolation
│   └── Resource quotas per tenant
│
├── Database Layer (Isolation Strategy)
│   ├── Shared Database, Separate Schemas
│   │   └── Cloud SQL with multiple schemas
│   ├── OR Database per Tenant
│   │   └── Cloud SQL instances per tenant (premium tier)
│   └── Backup and HA
│       ├── Automated backups (daily)
│       └── Regional Cloud SQL (synchronous replication)
│
├── Tenant Data Storage
│   ├── Cloud Storage buckets per tenant
│   │   ├── Bucket Lock for compliance
│   │   └── Retention policies
│   └── Customer-Managed Encryption Keys (CMEK)
│       └── Per-tenant encryption keys
│
└── Monitoring and Compliance
    ├── Cloud Logging (per-tenant logs)
    ├── Cloud Monitoring (per-tenant dashboards)
    ├── Access Transparency logs
    └── VPC Service Controls (perimeter)
```

**Tenant Isolation Strategies**:

| Isolation Level | Approach | Use Case | Cost |
|----------------|----------|----------|------|
| Schema-level | Shared DB, separate schemas | Standard tier customers | Low |
| Database-level | Separate Cloud SQL instances | Premium tier customers | Medium |
| Infrastructure-level | Dedicated GKE clusters | Enterprise tier | High |

**Key Design Decisions**:
1. **GKE Namespaces**: Cost-effective isolation for standard tier
2. **Regional Cloud SQL**: 99.95% SLA, synchronous replication, zero data loss
3. **CMEK per tenant**: Compliance, customer control over encryption
4. **VPC Service Controls**: Perimeter protection, prevent data exfiltration
5. **Backup strategy**: Automated daily backups, transaction logs, point-in-time recovery

**Disaster Recovery**:
```
DR Strategy (RPO: 1 hour, RTO: 2 hours)
├── Primary Region: us-central1
│   ├── Regional GKE cluster
│   ├── Regional Cloud SQL (HA)
│   └── Cloud Storage (multi-region)
│
└── DR Region: us-east1
    ├── GKE cluster (standby)
    ├── Cloud SQL replica (read replica)
    └── Cloud Storage (replicated)

Failover Process:
1. Detect primary region failure (Cloud Monitoring)
2. Promote Cloud SQL replica to primary (RTO: 5 minutes)
3. Update DNS to point to DR region (RTO: 10 minutes)
4. Start GKE workloads in DR region (RTO: 30 minutes)
5. Total RTO: < 2 hours
```

**Exam Tips**:
- Multi-tenancy: Balance between cost (shared) and isolation (dedicated)
- Regional Cloud SQL provides 99.95% SLA (meets requirement)
- CMEK required for enterprise compliance (SOC 2, HIPAA)
- VPC Service Controls for data perimeter security
- Backup strategy must meet RPO/RTO SLAs

### Scenario 4: Real-Time Gaming Platform

**Requirements**:
- 1M+ concurrent players
- < 50ms latency (p95)
- Real-time matchmaking
- Game state persistence
- Anti-cheat system
- Seasonal events (10x traffic spike)

**Solution Architecture**:
```
Gaming Platform Architecture
├── Global Load Balancer (Premium Network Tier)
│   └── Anycast IP routing to nearest region
│
├── Game Servers (per region)
│   ├── GKE Standard (regional clusters)
│   │   ├── Dedicated game server pods
│   │   ├── Session affinity (UDP)
│   │   └── Cluster Autoscaler + HPA
│   ├── Or Agones (game server orchestration on GKE)
│   │   └── Fleet autoscaling
│   └── Node pools with local SSDs (low-latency storage)
│
├── Matchmaking Service
│   ├── Cloud Run (HTTP API)
│   ├── Memorystore Redis (matchmaking queue)
│   └── Pub/Sub (match notifications)
│
├── Game State Management
│   ├── Firestore (player profiles, inventory)
│   │   └── Multi-region configuration
│   ├── Cloud SQL (transaction logs)
│   └── Memorystore (in-game cache)
│
├── Analytics and Anti-Cheat
│   ├── Game telemetry → Pub/Sub → Dataflow → BigQuery
│   ├── Agent Platform (formerly Vertex AI; anomaly detection)
│   └── Cloud Functions (flag suspicious behavior)
│
└── Content Delivery
    ├── Cloud Storage (game assets)
    ├── Cloud CDN (game downloads, updates)
    └── Media CDN (video streaming)
```

**Key Design Decisions**:
1. **Premium Network Tier**: Global anycast IP, lowest latency routing
2. **Regional GKE clusters**: Deploy in all major regions (us, eu, asia)
3. **Agones**: Open-source game server management on GKE
4. **Memorystore Redis**: Sub-millisecond latency for matchmaking
5. **Firestore multi-region**: Global player profiles, automatic replication
6. **Local SSDs**: Ultra-low latency for game server storage
7. **Cluster Autoscaler**: Handle seasonal 10x spikes

**Latency Optimization**:
- Deploy game servers in 6-8 regions globally
- Premium Network Tier (Google's global fiber network)
- Memorystore for hot data (< 1ms latency)
- Local SSDs for game server ephemeral storage
- UDP protocol for game traffic (lower overhead than TCP)

**Scaling for Seasonal Events**:
```
Normal: 1M players, 500 game servers
Seasonal Event: 10M players, 5000 game servers

Auto-scaling Strategy:
├── Cluster Autoscaler: Add nodes as needed
├── Horizontal Pod Autoscaler: Scale pods based on player count
├── Agones Fleet Autoscaler: Add/remove game servers
└── Preemptible nodes for non-critical services (cost savings)

Cost Management:
├── Committed use discounts (baseline capacity)
├── On-demand for spike capacity
├── Preemptible VMs for matchmaking services (80% cheaper)
└── Scale down aggressively after event
```

**Exam Tips**:
- Premium Network Tier required for < 50ms global latency
- Agones (GKE) is Google's recommended solution for game servers
- Memorystore for low-latency data (not Cloud SQL for hot path)
- Firestore for player data (global replication, scalable)
- Local SSDs for game server storage (not persistent disks)
- Auto-scaling critical for 10x traffic spikes

### Scenario 5: Healthcare Data Platform (HIPAA Compliance)

**Requirements**:
- HIPAA compliance mandatory
- PHI (Protected Health Information) storage and processing
- 99.99% availability
- Audit logging for all access
- Encryption at rest and in transit
- Data retention: 10 years
- DR: RPO 0, RTO 1 hour

**Solution Architecture**:
```
HIPAA-Compliant Architecture
├── Network Security
│   ├── VPC Service Controls (security perimeter)
│   ├── Private GKE cluster (no public IPs)
│   ├── Cloud NAT (outbound internet)
│   └── Cloud Armor (DDoS protection)
│
├── Application Layer
│   ├── GKE Private Cluster
│   │   ├── Workload Identity (no service account keys)
│   │   ├── Binary Authorization (signed images only)
│   │   └── Shielded GKE nodes
│   └── Cloud Run (private ingress only)
│
├── Data Storage (Encrypted)
│   ├── Cloud SQL
│   │   ├── Customer-Managed Encryption Keys (CMEK)
│   │   ├── Automated backups (encrypted)
│   │   ├── Regional PD (synchronous replication)
│   │   └── Private IP only
│   ├── Cloud Storage
│   │   ├── CMEK encryption
│   │   ├── Retention policies (10 years)
│   │   ├── Bucket Lock (prevent deletion)
│   │   └── Uniform bucket-level access
│   └── Firestore
│       └── CMEK encryption
│
├── Encryption and Key Management
│   ├── Cloud KMS (CMEK)
│   │   ├── Automatic key rotation
│   │   ├── HSM-backed keys (Cloud HSM)
│   │   └── Key access audit logs
│   └── Application-level encryption (AES-256)
│
├── Access Control and Audit
│   ├── IAM (principle of least privilege)
│   ├── VPC Service Controls (data perimeter)
│   ├── Access Context Manager (conditional access)
│   ├── Cloud Logging (all PHI access logged)
│   │   └── Log sink to BigQuery (long-term retention)
│   ├── Access Transparency (Google access logs)
│   └── Cloud Audit Logs (enabled for all services)
│
└── Disaster Recovery (RPO 0, RTO 1 hour)
    ├── Regional Cloud SQL (synchronous replication)
    ├── Cloud Storage (multi-region)
    ├── Cross-region Cloud SQL replica (async)
    └── Automated failover procedures
```

**HIPAA Compliance Checklist**:
- [ ] Sign Google Cloud HIPAA BAA (Business Associate Agreement)
- [ ] Enable VPC Service Controls (security perimeter)
- [ ] Use CMEK for all PHI data encryption
- [ ] Private GKE clusters (no public endpoints)
- [ ] Enable all audit logging (Data Access logs)
- [ ] Implement retention policies (10+ years)
- [ ] Workload Identity (no service account keys)
- [ ] Binary Authorization (trusted images only)
- [ ] Access Transparency enabled
- [ ] Shielded VMs/GKE nodes

**Key Design Decisions**:
1. **VPC Service Controls**: Prevent data exfiltration, define security perimeter
2. **CMEK**: Customer control over encryption keys (compliance requirement)
3. **Private GKE**: No public IPs, Cloud NAT for outbound only
4. **Regional Cloud SQL**: RPO 0 (synchronous replication between zones)
5. **Audit Logging**: Data Access logs enabled (track all PHI access)
6. **Bucket Lock**: Immutable storage for compliance
7. **Workload Identity**: No service account keys (security best practice)

**Cost Considerations**:
- CMEK: Minimal cost ($1/key/month + operations)
- VPC Service Controls: Free
- Private GKE: Same cost as regular GKE
- Cloud HSM: $1/hour per key (~$730/month per key)
- Audit Logging storage: ~$0.50/GB/month in BigQuery
- **Estimated Monthly Cost**: +15-20% vs non-HIPAA architecture

**Exam Tips**:
- HIPAA requires Google Cloud HIPAA BAA + customer responsibilities
- VPC Service Controls mandatory for data perimeter security
- CMEK required for PHI encryption (not Google-managed keys)
- All audit logging must be enabled (especially Data Access logs)
- Private GKE clusters for HIPAA workloads
- Regional Cloud SQL provides RPO 0 (synchronous replication)
- Bucket Lock for immutable storage (compliance)

### Scenario 6: Hybrid Cloud with On-Premises Integration

**Requirements**:
- On-premises data center (legacy systems)
- Burst to cloud for peak capacity
- Low-latency connectivity (< 10ms)
- Shared VPC between on-prem and cloud
- Private IP space (no internet exposure)
- Bandwidth: 10 Gbps

**Solution Architecture**:
```
Hybrid Cloud Architecture
├── On-Premises Data Center
│   ├── Legacy systems (non-migratable)
│   ├── Private IP: 10.0.0.0/16
│   └── Cloud Interconnect endpoint
│
├── Google Cloud
│   ├── Shared VPC (Host Project)
│   │   ├── Subnet: 10.1.0.0/16 (no overlap with on-prem)
│   │   ├── VPC Peering to other VPCs
│   │   └── Hybrid subnets
│   ├── Cloud Interconnect (Dedicated 10 Gbps)
│   │   ├── 99.99% SLA
│   │   ├── Private connectivity (no internet)
│   │   └── VLAN attachments
│   └── Cloud VPN (backup connectivity)
│       └── HA VPN (99.99% SLA)
│
├── Workloads
│   ├── Burst Compute (Compute Engine)
│   │   ├── Managed Instance Groups
│   │   ├── Autoscaling based on on-prem load
│   │   └── Private IPs only
│   ├── Cloud SQL (with Private IP)
│   │   └── Accessible from on-prem
│   └── Internal Load Balancer
│       └── Balance traffic across on-prem and cloud
│
├── Hybrid Load Balancing
│   ├── Internal Application Load Balancer
│   │   ├── Backend: On-prem servers (via NEG)
│   │   └── Backend: Cloud Run/GKE
│   └── Cloud CDN (for static content)
│
└── Management and Monitoring
    ├── Cloud Logging (centralized logs)
    ├── Cloud Monitoring (on-prem + cloud metrics)
    ├── Cloud Trace (distributed tracing)
    └── VPC Flow Logs (network troubleshooting)
```

**Key Design Decisions**:
1. **Dedicated Interconnect**: 10 Gbps, 99.99% SLA, < 10ms latency
2. **Shared VPC**: Centralized network management, project isolation
3. **Private Google Access**: Access GCP APIs without internet
4. **HA VPN backup**: Redundancy if Interconnect fails
5. **Internal Load Balancer**: Distribute traffic between on-prem and cloud
6. **Non-overlapping IP spaces**: Essential for routing

**Connectivity Options Comparison**:
| Option | Bandwidth | Latency | SLA | Cost | Use Case |
|--------|-----------|---------|-----|------|----------|
| Dedicated Interconnect | 10-100 Gbps | 1-10ms | 99.99% | $$$$ | Enterprise, low latency |
| Partner Interconnect | 50 Mbps-10 Gbps | 10-20ms | 99.99% | $$$ | Mid-size, flexible |
| Cloud VPN (HA) | 1.5-3 Gbps/tunnel | 20-50ms | 99.99% | $ | Small, backup |
| Cloud VPN (Classic) | 1.5 Gbps/tunnel | 20-50ms | 99.9% | $ | Legacy, simple |

**Exam Tips**:
- Dedicated Interconnect for < 10ms latency and 10+ Gbps bandwidth
- HA VPN as backup (99.99% SLA requires HA VPN)
- Shared VPC for centralized network management
- Private Google Access for accessing GCP APIs without internet
- Non-overlapping IP spaces critical (plan carefully)
- Internal Load Balancer for hybrid load balancing
- VPC Flow Logs for troubleshooting connectivity issues

## Professional Architect Exam Tips

### Common Architecture Traps

1. **Trap: Using Global Load Balancer when Regional suffices**
   - **Issue**: Higher cost, unnecessary complexity
   - **Fix**: Use Regional Load Balancer for single-region applications
   - **Exam Clue**: "Regional application," "single region users"

2. **Trap: Over-engineering for simple requirements**
   - **Issue**: GKE for simple stateless HTTP service
   - **Fix**: Cloud Run for stateless HTTP, Cloud Functions for events
   - **Exam Clue**: "Simple," "stateless," "minimal management"

3. **Trap: Not considering data residency**
   - **Issue**: Multi-region architecture when data must stay in specific region
   - **Fix**: Regional resources for data residency compliance
   - **Exam Clue**: "GDPR," "data residency," "data sovereignty"

4. **Trap**: Not enabling audit logging for compliance
   - **Issue**: HIPAA/PCI-DSS requires comprehensive audit logs
   - **Fix**: Enable Data Access audit logs, Access Transparency
   - **Exam Clue**: "HIPAA," "compliance," "audit requirements"

5. **Trap: Using external IPs when not needed**
   - **Issue**: Security risk, additional cost
   - **Fix**: Private IPs + Cloud NAT for outbound, Private Google Access for APIs
   - **Exam Clue**: "Security," "private," "no internet exposure"

6. **Trap: Not right-sizing resources**
   - **Issue**: Paying for unused capacity
   - **Fix**: Use autoscaling, committed use discounts, preemptible VMs
   - **Exam Clue**: "Cost optimization," "variable workload"

### Cost Optimization Patterns

**Pattern 1: Variable Workloads**
- Use: Cloud Run, Cloud Functions, GKE Autopilot
- Why: Pay only for usage, scale to zero
- Savings: 60-80% vs always-on VMs

**Pattern 2: Stable Workloads**
- Use: Committed use discounts (1-year or 3-year)
- Why: 25-52% discount for commitment
- Savings: Up to 52% on predictable workloads

**Pattern 3: Batch Processing**
- Use: Preemptible VMs, Spot VMs
- Why: 60-91% discount, fault-tolerant
- Savings: 80% vs regular VMs

**Pattern 4: Storage Tiering**
- Use: Cloud Storage lifecycle policies
- Why: Auto-transition to cheaper tiers
- Savings: 50-95% for infrequently accessed data

**Pattern 5: Network Egress**
- Use: Cloud CDN, regional deployments
- Why: Reduce cross-region/internet egress
- Savings: 70-90% with CDN cache hit

### Design Pattern Recognition

**Pattern: Global Web Application**
- **Components**: Global Load Balancer + Cloud CDN + Multi-region backends
- **Keywords**: "Global users," "low latency worldwide," "high availability"

**Pattern: Event-Driven Processing**
- **Components**: Pub/Sub + Cloud Functions/Dataflow + BigQuery
- **Keywords**: "Asynchronous," "event-driven," "decouple"

**Pattern: Microservices**
- **Components**: GKE + Service Mesh + Internal Load Balancer
- **Keywords**: "Microservices," "independently deployable," "service mesh"

**Pattern: Data Analytics**
- **Components**: Cloud Storage + Dataflow + BigQuery + Looker
- **Keywords**: "Analytics," "data warehouse," "batch processing"

**Pattern: Machine Learning**
- **Components**: Agent Platform (formerly Vertex AI) + Cloud Storage + BigQuery + Agent Platform Workbench
- **Keywords**: "Machine learning," "model training," "predictions"

### Quick Decision Tree

```
Need to run code?
├── Event-driven, simple function → Cloud Functions 2nd Gen
├── Stateless HTTP container → Cloud Run
├── Complex microservices → GKE
├── Simple web app, traffic splitting → App Engine
└── Full control, custom OS → Compute Engine

Need high availability?
├── Regional: Regional resources (99.5-99.95% SLA)
└── Global: Multi-region resources (99.95-99.99% SLA)

Need low latency globally?
├── Yes: Global Load Balancer + Cloud CDN + Multi-region
└── No: Regional resources

Need compliance (HIPAA, PCI-DSS)?
├── VPC Service Controls
├── CMEK encryption
├── Private clusters
├── Audit logging
└── Access controls

Cost optimization priority?
├── Variable workload → Cloud Run, Cloud Functions
├── Stable workload → Committed use discounts
├── Batch processing → Preemptible VMs
└── Storage → Lifecycle policies
```

## Comprehensive gcloud Command Reference

### Compute Engine Commands

```bash
# Instance Management
# Create instance with various options
gcloud compute instances create my-instance \
  --zone=us-central1-a \
  --machine-type=n2-standard-4 \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --boot-disk-type=pd-ssd \
  --tags=web-server,https-server \
  --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y nginx'

# Create preemptible/spot instance
gcloud compute instances create spot-instance \
  --zone=us-central1-a \
  --machine-type=e2-standard-4 \
  --provisioning-model=SPOT \
  --instance-termination-action=STOP

# Create custom machine type
gcloud compute instances create custom-instance \
  --zone=us-central1-a \
  --custom-cpu=8 \
  --custom-memory=32GB

# Create instance with GPU
gcloud compute instances create gpu-instance \
  --zone=us-central1-a \
  --machine-type=n1-standard-4 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --maintenance-policy=TERMINATE \
  --metadata=install-nvidia-driver=True

# Instance Templates
gcloud compute instance-templates create web-template \
  --machine-type=e2-medium \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --tags=web-server \
  --metadata=startup-script-url=gs://my-bucket/startup.sh

# Managed Instance Groups (MIG)
# Create regional MIG
gcloud compute instance-groups managed create web-mig \
  --base-instance-name=web-server \
  --template=web-template \
  --size=3 \
  --region=us-central1 \
  --target-distribution-shape=EVEN

# Configure autoscaling
gcloud compute instance-groups managed set-autoscaling web-mig \
  --region=us-central1 \
  --min-num-replicas=2 \
  --max-num-replicas=10 \
  --target-cpu-utilization=0.75 \
  --cool-down-period=90

# Rolling update
gcloud compute instance-groups managed rolling-action start-update web-mig \
  --region=us-central1 \
  --version=template=web-template-v2 \
  --max-surge=3 \
  --max-unavailable=0

# Persistent Disks
# Create regional persistent disk
gcloud compute disks create my-regional-disk \
  --size=500GB \
  --type=pd-ssd \
  --region=us-central1 \
  --replica-zones=us-central1-a,us-central1-b

# Create snapshot
gcloud compute disks snapshot my-disk \
  --zone=us-central1-a \
  --snapshot-names=my-snapshot \
  --storage-location=us-central1

# Snapshots schedule
gcloud compute resource-policies create snapshot-schedule daily-backup \
  --region=us-central1 \
  --max-retention-days=14 \
  --on-source-disk-delete=keep-auto-snapshots \
  --daily-schedule \
  --start-time=02:00

# Attach snapshot schedule to disk
gcloud compute disks add-resource-policies my-disk \
  --zone=us-central1-a \
  --resource-policies=daily-backup

# SSH and Access
# SSH into instance
gcloud compute ssh my-instance --zone=us-central1-a

# Run command on instance
gcloud compute ssh my-instance --zone=us-central1-a --command="df -h"

# SCP files
gcloud compute scp local-file.txt my-instance:~/remote-file.txt --zone=us-central1-a

# IAP tunneling (for instances without external IP)
gcloud compute ssh my-instance --zone=us-central1-a --tunnel-through-iap
```

### GKE Commands

```bash
# Cluster Creation
# Create standard cluster
gcloud container clusters create production-cluster \
  --region=us-central1 \
  --num-nodes=3 \
  --machine-type=n2-standard-4 \
  --disk-size=50 \
  --disk-type=pd-ssd \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=10 \
  --enable-autorepair \
  --enable-autoupgrade \
  --maintenance-window-start=2023-01-01T00:00:00Z \
  --maintenance-window-duration=4h \
  --maintenance-window-recurrence='FREQ=WEEKLY;BYDAY=SU'

# Create autopilot cluster
gcloud container clusters create-auto autopilot-cluster \
  --region=us-central1

# Create private cluster
gcloud container clusters create private-cluster \
  --region=us-central1 \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.0/28 \
  --enable-ip-alias \
  --network=my-vpc \
  --subnetwork=gke-subnet

# Enable Workload Identity
gcloud container clusters create wi-cluster \
  --region=us-central1 \
  --workload-pool=PROJECT_ID.svc.id.goog

# Or update existing cluster
gcloud container clusters update existing-cluster \
  --region=us-central1 \
  --workload-pool=PROJECT_ID.svc.id.goog

# Node Pool Management
# Create node pool
gcloud container node-pools create high-mem-pool \
  --cluster=production-cluster \
  --region=us-central1 \
  --machine-type=n2-highmem-8 \
  --num-nodes=2 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=5 \
  --disk-size=100 \
  --disk-type=pd-ssd \
  --node-taints=workload-type=memory-intensive:NoSchedule \
  --node-labels=pool=high-memory

# Create GPU node pool
gcloud container node-pools create gpu-pool \
  --cluster=production-cluster \
  --region=us-central1 \
  --machine-type=n1-standard-4 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --num-nodes=0 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=3

# Create spot VM node pool
gcloud container node-pools create spot-pool \
  --cluster=production-cluster \
  --region=us-central1 \
  --machine-type=e2-standard-4 \
  --spot \
  --num-nodes=0 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=10

# Cluster Management
# Get cluster credentials
gcloud container clusters get-credentials production-cluster --region=us-central1

# Upgrade cluster
gcloud container clusters upgrade production-cluster \
  --region=us-central1 \
  --cluster-version=1.27 \
  --master

# Upgrade node pool
gcloud container clusters upgrade production-cluster \
  --region=us-central1 \
  --node-pool=default-pool

# Resize cluster
gcloud container clusters resize production-cluster \
  --region=us-central1 \
  --num-nodes=5 \
  --node-pool=default-pool

# Enable Binary Authorization
gcloud container clusters update production-cluster \
  --region=us-central1 \
  --enable-binauthz

# Enable GKE Enterprise features
gcloud container hub memberships register production-cluster \
  --gke-cluster=us-central1/production-cluster \
  --enable-workload-identity
```

### Cloud Run Commands

```bash
# Deploy Cloud Run service
gcloud run deploy api-service \
  --image=gcr.io/PROJECT_ID/api:v1 \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --max-instances=100 \
  --min-instances=1 \
  --memory=1Gi \
  --cpu=2 \
  --timeout=300 \
  --concurrency=80 \
  --port=8080 \
  --set-env-vars="DB_HOST=10.1.0.5,DB_NAME=mydb" \
  --vpc-connector=my-connector \
  --vpc-egress=private-ranges-only

# Deploy with secrets
gcloud run deploy api-service \
  --image=gcr.io/PROJECT_ID/api:v1 \
  --region=us-central1 \
  --set-secrets="DB_PASSWORD=db-password:latest,API_KEY=api-key:1"

# Traffic management
# Deploy new revision without traffic
gcloud run deploy api-service \
  --image=gcr.io/PROJECT_ID/api:v2 \
  --region=us-central1 \
  --no-promote

# Gradually shift traffic (canary)
gcloud run services update-traffic api-service \
  --region=us-central1 \
  --to-revisions=api-service-v2=10,api-service-v1=90

# Tag-based routing
gcloud run services update-traffic api-service \
  --region=us-central1 \
  --update-tags=staging=api-service-v2

# Service management
# Set IAM policy
gcloud run services add-iam-policy-binding api-service \
  --region=us-central1 \
  --member="serviceAccount:frontend@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.invoker"

# List services
gcloud run services list --region=us-central1

# Describe service
gcloud run services describe api-service --region=us-central1

# Delete service
gcloud run services delete api-service --region=us-central1
```

### Cloud Functions Commands

```bash
# Deploy HTTP function (2nd gen)
gcloud functions deploy hello-http \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=hello_http \
  --trigger-http \
  --allow-unauthenticated \
  --memory=512MB \
  --timeout=60s \
  --max-instances=100 \
  --min-instances=1 \
  --concurrency=80

# Deploy Pub/Sub triggered function
gcloud functions deploy process-pubsub \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=process_message \
  --trigger-topic=my-topic \
  --retry

# Deploy Cloud Storage triggered function
gcloud functions deploy process-file \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=process_file \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=my-upload-bucket"

# Deploy with environment variables and secrets
gcloud functions deploy secure-function \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=main \
  --trigger-http \
  --set-env-vars="ENV=production,LOG_LEVEL=info" \
  --set-secrets="API_KEY=api-key:latest"

# Deploy with VPC connector
gcloud functions deploy vpc-function \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=main \
  --trigger-http \
  --vpc-connector=my-connector \
  --egress-settings=private-ranges-only

# List functions
gcloud functions list --region=us-central1

# Describe function
gcloud functions describe my-function --region=us-central1 --gen2

# Call function (HTTP)
gcloud functions call hello-http --region=us-central1 --gen2 --data='{"name":"World"}'

# Delete function
gcloud functions delete my-function --region=us-central1 --gen2
```

### App Engine Commands

```bash
# Deploy App Engine application
gcloud app deploy app.yaml --project=PROJECT_ID

# Deploy specific service
gcloud app deploy api-service.yaml

# Deploy without promoting (no traffic)
gcloud app deploy --no-promote

# Traffic splitting
gcloud app services set-traffic default \
  --splits=v2=0.8,v1=0.2 \
  --split-by=ip

# Migrate traffic gradually
gcloud app services set-traffic default \
  --splits=v2=1.0 \
  --migrate

# List versions
gcloud app versions list --service=default

# Stop version
gcloud app versions stop v1 --service=default

# Delete version
gcloud app versions delete v1 --service=default

# View logs
gcloud app logs tail -s default

# Open application in browser
gcloud app browse
```

### Load Balancing Commands

```bash
# Create backend service
gcloud compute backend-services create web-backend \
  --protocol=HTTP \
  --port-name=http \
  --health-checks=http-health-check \
  --global \
  --enable-cdn \
  --cache-mode=CACHE_ALL_STATIC

# Add backend (instance group)
gcloud compute backend-services add-backend web-backend \
  --instance-group=web-mig \
  --instance-group-region=us-central1 \
  --balancing-mode=UTILIZATION \
  --max-utilization=0.8 \
  --global

# Add backend (Cloud Run)
gcloud compute backend-services add-backend web-backend \
  --global \
  --network-endpoint-group=cloudrun-neg \
  --network-endpoint-group-region=us-central1

# Create URL map
gcloud compute url-maps create web-map \
  --default-service=web-backend

# Add path matcher
gcloud compute url-maps add-path-matcher web-map \
  --path-matcher-name=path-matcher-1 \
  --default-service=web-backend \
  --path-rules="/api/*=api-backend,/static/*=storage-backend"

# Create SSL certificate (managed)
gcloud compute ssl-certificates create web-ssl-cert \
  --domains=www.example.com,example.com \
  --global

# Create target HTTPS proxy
gcloud compute target-https-proxies create web-https-proxy \
  --url-map=web-map \
  --ssl-certificates=web-ssl-cert

# Reserve static IP
gcloud compute addresses create web-ip \
  --ip-version=IPV4 \
  --global

# Create forwarding rule
gcloud compute forwarding-rules create web-forwarding-rule \
  --address=web-ip \
  --target-https-proxy=web-https-proxy \
  --global \
  --ports=443

# Cloud Armor security policy
gcloud compute security-policies create web-security-policy

# Add rule
gcloud compute security-policies rules create 1000 \
  --security-policy=web-security-policy \
  --expression="origin.region_code == 'CN'" \
  --action=deny-403

# Apply to backend service
gcloud compute backend-services update web-backend \
  --security-policy=web-security-policy \
  --global

# Health checks
gcloud compute health-checks create http http-health-check \
  --port=80 \
  --request-path=/health \
  --check-interval=10s \
  --timeout=5s \
  --unhealthy-threshold=3 \
  --healthy-threshold=2
```

### Networking Commands

```bash
# VPC Management
# Create VPC
gcloud compute networks create my-vpc \
  --subnet-mode=custom \
  --bgp-routing-mode=regional

# Create subnet
gcloud compute networks subnets create my-subnet \
  --network=my-vpc \
  --region=us-central1 \
  --range=10.0.1.0/24 \
  --enable-private-ip-google-access \
  --enable-flow-logs

# Create proxy-only subnet (for Internal Application LB)
gcloud compute networks subnets create proxy-only-subnet \
  --purpose=REGIONAL_MANAGED_PROXY \
  --role=ACTIVE \
  --region=us-central1 \
  --network=my-vpc \
  --range=10.129.0.0/23

# Firewall Rules
# Allow HTTP/HTTPS
gcloud compute firewall-rules create allow-http-https \
  --network=my-vpc \
  --allow=tcp:80,tcp:443 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=web-server

# Allow internal traffic
gcloud compute firewall-rules create allow-internal \
  --network=my-vpc \
  --allow=tcp:0-65535,udp:0-65535,icmp \
  --source-ranges=10.0.0.0/8

# Allow IAP for SSH
gcloud compute firewall-rules create allow-iap-ssh \
  --network=my-vpc \
  --allow=tcp:22 \
  --source-ranges=35.235.240.0/20

# Cloud NAT
gcloud compute routers create nat-router \
  --network=my-vpc \
  --region=us-central1

gcloud compute routers nats create nat-config \
  --router=nat-router \
  --region=us-central1 \
  --nat-all-subnet-ip-ranges \
  --auto-allocate-nat-external-ips

# VPC Peering
gcloud compute networks peerings create peer-vpc-1-to-vpc-2 \
  --network=vpc-1 \
  --peer-project=PROJECT_ID \
  --peer-network=vpc-2 \
  --auto-create-routes

# Shared VPC
# Enable Shared VPC
gcloud compute shared-vpc enable HOST_PROJECT_ID

# Attach service project
gcloud compute shared-vpc associated-projects add SERVICE_PROJECT_ID \
  --host-project=HOST_PROJECT_ID

# VPN (HA VPN)
# Create HA VPN gateway
gcloud compute vpn-gateways create ha-vpn-gateway \
  --network=my-vpc \
  --region=us-central1

# Create Cloud Router
gcloud compute routers create vpn-router \
  --region=us-central1 \
  --network=my-vpc \
  --asn=65001

# Create VPN tunnel
gcloud compute vpn-tunnels create tunnel-1 \
  --peer-gcp-gateway=peer-gateway \
  --region=us-central1 \
  --ike-version=2 \
  --shared-secret=SECRET \
  --router=vpn-router \
  --vpn-gateway=ha-vpn-gateway \
  --interface=0

# Cloud Interconnect
# Create VLAN attachment
gcloud compute interconnects attachments dedicated create my-attachment \
  --region=us-central1 \
  --router=interconnect-router \
  --interconnect=my-interconnect \
  --vlan=100
```

### IAM and Security Commands

```bash
# Service Accounts
# Create service account
gcloud iam service-accounts create my-service-account \
  --display-name="My Service Account"

# Grant IAM role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:my-service-account@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=my-service-account@PROJECT_ID.iam.gserviceaccount.com

# Impersonate service account
gcloud compute instances list \
  --impersonate-service-account=my-service-account@PROJECT_ID.iam.gserviceaccount.com

# VPC Service Controls
# Create access policy
gcloud access-context-manager policies create \
  --title="My Organization Policy"

# Create service perimeter
gcloud access-context-manager perimeters create my-perimeter \
  --title="Production Perimeter" \
  --resources=projects/PROJECT_NUMBER \
  --restricted-services=storage.googleapis.com,bigquery.googleapis.com \
  --policy=POLICY_ID
```

### Monitoring and Logging Commands

```bash
# View logs
gcloud logging read "resource.type=gce_instance AND severity>=ERROR" \
  --limit=50 \
  --format=json

# Create log sink
gcloud logging sinks create my-sink \
  storage.googleapis.com/my-logs-bucket \
  --log-filter='resource.type="gce_instance"'

# Create uptime check
gcloud monitoring uptime-checks create web-check \
  --display-name="Website Uptime" \
  --resource-type=uptime-url \
  --monitored-resource=https://example.com \
  --period=60

# Create alert policy
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High CPU Alert" \
  --condition-display-name="CPU > 80%" \
  --condition-threshold-value=0.8 \
  --condition-threshold-duration=300s

# View metrics
gcloud monitoring time-series list \
  --filter='metric.type="compute.googleapis.com/instance/cpu/utilization"' \
  --format=json
```

## Key Exam Reminders

### Must-Know Concepts
1. **Compute Service Selection**: Right service for the right workload
2. **High Availability**: Regional resources, multi-region architectures
3. **Cost Optimization**: CUDs, preemptible VMs, autoscaling, lifecycle policies
4. **Security**: VPC Service Controls, CMEK, Private clusters, IAM
5. **Compliance**: HIPAA BAA, audit logging, data residency
6. **Load Balancing**: Global vs Regional, Internal vs External
7. **Migration**: Migrate for Compute Engine, Migrate for Anthos
8. **Networking**: VPC design, Shared VPC, Private Google Access

### Time Management Tips
- Read questions carefully for hidden requirements (compliance, latency, cost)
- Eliminate obviously wrong answers first
- Look for keywords: "globally distributed," "compliance," "cost optimization"
- Architecture diagrams often reveal the answer
- Multi-region = higher cost but better availability/latency

### Common Question Types
1. **Service Selection**: Which compute service for this workload?
2. **Architecture Design**: Design a multi-tier application
3. **Cost Optimization**: Reduce costs while maintaining performance
4. **Security/Compliance**: Meet HIPAA/PCI-DSS requirements
5. **Migration Strategy**: Best approach to migrate to GCP
6. **Troubleshooting**: Why isn't this working? (connectivity, IAM, etc.)

## Additional Resources

### Official Documentation
- [Compute Options Comparison](https://cloud.google.com/docs/choosing-a-compute-option)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Load Balancing Overview](https://cloud.google.com/load-balancing/docs/load-balancing-overview)
- [Network Architecture Best Practices](https://cloud.google.com/architecture/best-practices-vpc-design)
- [Security Best Practices](https://cloud.google.com/security/best-practices)

### Architecture Guidance
- [Google Cloud Architecture Center](https://cloud.google.com/architecture)
- [Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [Migration to Google Cloud](https://cloud.google.com/solutions/migration-center)
- [Cost Optimization Best Practices](https://cloud.google.com/architecture/framework/cost-optimization)

### Practice and Labs
- [Qwiklabs GCP Quests](https://www.cloudskillsboost.google/)
- [Coursera - Architecting with Google Cloud](https://www.coursera.org/professional-certificates/gcp-cloud-architect)
- [Linux Academy GCP Learning Paths](https://acloudguru.com/gcp-cloud-training)

### Exam Preparation
- [Official Exam Guide](https://cloud.google.com/certification/cloud-architect)
- [Sample Questions](https://cloud.google.com/certification/sample-questions/cloud-architect)
- [Practice Exam](https://cloud.google.com/certification/practice-exam/cloud-architect)

---

**Last Updated**: 2025-10
**Exam Version**: Professional Cloud Architect (Latest)
**Recommended Study Time**: 40-60 hours for comprehensive preparation
