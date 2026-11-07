# GCP Compute & Containers - Professional Cloud Architect Guide

## Table of Contents
1. [Compute Engine Deep Dive](#compute-engine-deep-dive)
2. [Google Kubernetes Engine (GKE)](#google-kubernetes-engine-gke)
3. [Container Optimization](#container-optimization)
4. [Kubernetes on GKE](#kubernetes-on-gke)
5. [Hybrid and Multi-Cloud (Anthos)](#hybrid-and-multi-cloud-anthos)
6. [Architecture Patterns](#architecture-patterns)
7. [Cost Optimization Strategies](#cost-optimization-strategies)
8. [Architecture Scenarios](#architecture-scenarios)
9. [Exam Tips & Strategies](#exam-tips--strategies)

---

## Compute Engine Deep Dive

### What is Compute Engine?
Google Cloud's Infrastructure-as-a-Service (IaaS) offering providing virtual machines (VMs) running on Google's global infrastructure with per-second billing, live migration, and extensive customization options.

### Machine Families & Types - Complete Overview

#### General Purpose Machine Families
| Series | Processor | vCPU Range | Memory Range | Use Cases | Key Differentiators |
|--------|-----------|------------|--------------|-----------|---------------------|
| **E2** | Intel/AMD mix | 2-32 vCPUs | 0.5-128 GB | Development, testing, web servers | Lowest cost, automatic platform selection |
| **N1** | Intel Skylake/Broadwell/Haswell | 1-96 vCPUs | 0.6-624 GB | General workloads, databases | Proven reliability, wide availability |
| **N2** | Intel Cascade Lake | 2-128 vCPUs | 0.5-864 GB | High-performance apps | Better price/performance than N1 |
| **N2D** | AMD EPYC Rome | 2-224 vCPUs | 0.5-896 GB | Cost-sensitive workloads | Best price/performance for general purpose |
| **Tau T2D** | AMD EPYC Milan | 1-60 vCPUs | 0.5-240 GB | Scale-out workloads | Optimized for horizontal scaling |
| **Tau T2A** | Ampere Altra (ARM) | 1-48 vCPUs | 1-192 GB | Web servers, containerized apps | Arm architecture, energy efficient |

#### Compute-Optimized Machine Families
| Series | Processor | vCPU Range | Memory Range | Performance | Use Cases |
|--------|-----------|------------|--------------|-------------|-----------|
| **C2** | Intel Cascade Lake | 4-60 vCPUs | 16-240 GB | 3.8 GHz sustained | Gaming servers, HPC, CPU-bound apps |
| **C2D** | AMD EPYC Milan | 2-112 vCPUs | 4-896 GB | 3.4 GHz sustained | High-compute batch jobs, scientific modeling |
| **H3** | Intel Sapphire Rapids | 88 vCPUs | 352 GB | High memory bandwidth | Memory-bound HPC workloads |

#### Memory-Optimized Machine Families
| Series | Processor | vCPU Range | Memory Range | Memory per vCPU | Use Cases |
|--------|-----------|------------|--------------|-----------------|-----------|
| **M1** | Intel Skylake | 40-160 vCPUs | 961-3844 GB | 24 GB per vCPU | Ultra-large in-memory databases (SAP HANA) |
| **M2** | Intel Cascade Lake | 2-128 vCPUs | 16-864 GB | 8-12 GB per vCPU | In-memory analytics, SAP HANA |
| **M3** | Intel Ice Lake | 32-128 vCPUs | 976-3904 GB | 28-32 GB per vCPU | Next-gen in-memory databases |

#### Accelerator-Optimized Machine Families
| Series | GPU Type | GPU Count | vCPUs | Memory | Use Cases |
|--------|----------|-----------|-------|--------|-----------|
| **A2** | NVIDIA A100 | 1-16 GPUs | 12-96 | 85-1360 GB | ML training, HPC, inference |
| **A3** | NVIDIA H100 | 8 GPUs | 208 vCPUs | 1872 GB | Large-scale ML training |
| **G2** | NVIDIA L4 | 1-8 GPUs | 4-96 | 16-384 GB | AI inference, graphics workloads |

### Custom Machine Types

#### Configuration Guidelines
```
Memory-to-vCPU Ratios:
- E2: 0.5 GB to 8 GB per vCPU
- N1: 0.9 GB to 6.5 GB per vCPU
- N2/N2D: 0.5 GB to 8 GB per vCPU
- C2: 4 GB per vCPU (fixed)

vCPU Options:
- Must be even numbers (except 1 vCPU for some series)
- E2: 2-32 vCPUs
- N1: 1-96 vCPUs
- N2: 2-128 vCPUs
- N2D: 2-224 vCPUs
```

#### Custom Machine Type Creation
```bash
# Create custom N2 machine with 8 vCPUs and 32 GB memory
gcloud compute instances create custom-vm-1 \
  --machine-type=n2-custom-8-32768 \
  --zone=us-central1-a

# Create custom machine with extended memory
gcloud compute instances create custom-vm-2 \
  --custom-cpu=4 \
  --custom-memory=32GB \
  --custom-extensions \
  --zone=us-central1-a

# Create custom machine with extended memory (up to 624 GB on N1)
gcloud compute instances create memory-intensive-vm \
  --machine-type=n1-custom-16-163840 \
  --zone=us-central1-a
```

#### When to Use Custom Machine Types
- **Right-sizing**: Workload needs 12 GB RAM but predefined types offer 8 GB or 16 GB
- **Cost optimization**: Save 20-40% compared to oversized predefined types
- **Legacy migration**: Match on-premises VM specifications exactly
- **Specific ratios**: Applications with unusual memory requirements

### Sole-Tenant Nodes

#### What are Sole-Tenant Nodes?
Physical Compute Engine servers dedicated to hosting only your project's VMs, providing physical isolation for compliance, licensing, and performance requirements.

#### Key Features
| Feature | Description | Use Case |
|---------|-------------|----------|
| **Physical Isolation** | VMs run only on your dedicated hardware | Regulatory compliance (HIPAA, PCI-DSS) |
| **License Management** | Bring-your-own-license (BYOL) support | Windows Server, SQL Server licenses |
| **Node Affinity** | Control VM placement on specific nodes | Performance consistency |
| **Node Groups** | Manage multiple nodes as a unit | High availability, maintenance windows |
| **Maintenance Policies** | Control when nodes are maintained | Minimal disruption scheduling |

#### Sole-Tenant Node Configuration
```bash
# Create node template
gcloud compute sole-tenancy node-templates create my-node-template \
  --node-type=n1-node-96-624 \
  --region=us-central1

# Create node group
gcloud compute sole-tenancy node-groups create my-node-group \
  --node-template=my-node-template \
  --target-size=3 \
  --zone=us-central1-a

# Create VM on sole-tenant node
gcloud compute instances create vm-on-sole-tenant \
  --machine-type=n1-standard-4 \
  --node-group=my-node-group \
  --zone=us-central1-a

# Create VM with node affinity labels
gcloud compute instances create vm-with-affinity \
  --machine-type=n1-standard-8 \
  --node-affinity-labels=workload=production,compliance=hipaa \
  --zone=us-central1-a
```

#### Cost Comparison
```
Sole-Tenant Node (n1-node-96-624):
- Node cost: ~$4.75/hour for entire node
- Can run up to 96 vCPUs worth of VMs
- Break-even: ~12-16 n1-standard-4 instances

Regular VMs:
- n1-standard-4: ~$0.38/hour per instance
- More flexible but no physical isolation
```

### Committed Use Discounts (CUDs)

#### Overview
Committed use contracts for predictable workloads offering up to 57% discount for 1-year or 3-year commitments.

#### CUD Types
| Type | Commitment | Flexibility | Discount | Use Case |
|------|------------|-------------|----------|----------|
| **Resource-based** | Specific vCPU, memory, GPU | Tied to specific resources | Up to 57% | Known workloads with fixed requirements |
| **Spend-based** | Dollar amount commitment | Flexible across resources | Up to 55% | Variable workloads, multi-project |

#### Resource-Based CUD Configuration
```bash
# Purchase 1-year commitment for 100 N2 vCPUs
gcloud compute commitments create n2-commitment-1y \
  --region=us-central1 \
  --plan=12-month \
  --resources=vcpu=100,memory=400GB \
  --type=COMPUTE_OPTIMIZED_C2

# Purchase 3-year commitment for GPU
gcloud compute commitments create gpu-commitment-3y \
  --region=us-central1 \
  --plan=36-month \
  --resources=accelerator-type=nvidia-tesla-v100,accelerator-count=10

# View active commitments
gcloud compute commitments list --filter="status=ACTIVE"
```

#### Spend-Based CUD Configuration
```bash
# Purchase spend-based commitment
gcloud billing accounts commitments create \
  --billing-account=01234-56789A-BCDEF0 \
  --plan=12-month \
  --amount=10000 \
  --region=us-central1
```

#### CUD Strategy Matrix
| Scenario | Recommended Type | Duration | Expected Savings |
|----------|------------------|----------|------------------|
| Stable production workload | Resource-based | 3-year | 55-57% |
| Growing startup | Spend-based | 1-year | 25-35% |
| Seasonal with baseline | Resource-based + on-demand | 1-year | 30-40% |
| Multi-environment | Spend-based | 1-year | 25-35% |
| Legacy migration | Resource-based | 3-year | 55-57% |

### Preemptible and Spot VMs

#### Comparison Matrix
| Feature | Preemptible VMs | Spot VMs | Regular VMs |
|---------|-----------------|----------|-------------|
| **Discount** | Up to 80% | Up to 91% | 0% |
| **Maximum Runtime** | 24 hours | No limit | No limit |
| **Termination Notice** | 30 seconds | 30 seconds | N/A |
| **Availability** | No SLA | No SLA | 99.99% SLA (with MIG) |
| **API Differences** | Separate flag | Spot provisioning model | Standard |
| **Recommended For** | Legacy workloads | New workloads | Production |

#### Spot VM Provisioning Model
```bash
# Create Spot VM
gcloud compute instances create spot-vm-1 \
  --provisioning-model=SPOT \
  --instance-termination-action=STOP \
  --zone=us-central1-a \
  --machine-type=n2-standard-4

# Create Spot VM with deletion on termination
gcloud compute instances create spot-vm-2 \
  --provisioning-model=SPOT \
  --instance-termination-action=DELETE \
  --zone=us-central1-a \
  --machine-type=n2-standard-8

# Create instance with max price (Spot)
gcloud compute instances create spot-vm-with-max-price \
  --provisioning-model=SPOT \
  --max-price=0.50 \
  --zone=us-central1-a \
  --machine-type=n2-standard-4
```

#### Preemptible VM (Legacy)
```bash
# Create preemptible VM
gcloud compute instances create preemptible-vm-1 \
  --preemptible \
  --zone=us-central1-a \
  --machine-type=n2-standard-4

# Create managed instance group with preemptible VMs
gcloud compute instance-groups managed create preemptible-mig \
  --base-instance-name=preempt-vm \
  --template=my-instance-template \
  --size=10 \
  --zone=us-central1-a
```

#### Handling Preemption
```bash
# Startup script to handle preemption
cat > startup-script.sh << 'EOF'
#!/bin/bash

# Check if instance is being preempted
is_preempted() {
  curl -H "Metadata-Flavor: Google" \
    http://metadata.google.internal/computeMetadata/v1/instance/preempted \
    -sf || echo "FALSE"
}

# Graceful shutdown handler
shutdown_handler() {
  echo "Preemption detected - saving state..."
  # Save application state to Cloud Storage
  gsutil cp /var/app/state gs://my-bucket/state/$(hostname).state
  # Notify monitoring system
  curl -X POST https://monitoring-api/preemption-event \
    -d "instance=$(hostname)&time=$(date -u +%s)"
}

# Install shutdown handler
trap shutdown_handler SIGTERM

# Poll for preemption notice
while true; do
  if [ "$(is_preempted)" = "TRUE" ]; then
    shutdown_handler
    break
  fi
  sleep 1
done &

# Start main application
/usr/bin/start-application
EOF
```

#### Use Cases for Spot/Preemptible VMs
| Workload Type | Suitability | Implementation Pattern |
|---------------|-------------|------------------------|
| **Batch processing** | Excellent | Checkpointing, job queues |
| **CI/CD pipelines** | Excellent | Stateless, short-lived |
| **Data processing** | Good | Apache Spark, Hadoop with checkpointing |
| **ML training** | Good | Checkpoint every N epochs |
| **Web servers** | Poor | Use with careful load balancing |
| **Databases** | Not recommended | State loss unacceptable |
| **Rendering farms** | Excellent | Frame-by-frame checkpointing |

### Managed Instance Groups (MIGs)

#### Zonal vs Regional MIGs
| Feature | Zonal MIG | Regional MIG |
|---------|-----------|--------------|
| **Availability** | Single zone | Multiple zones (3+) |
| **SLA** | None | 99.99% |
| **Failover** | Manual | Automatic |
| **Cost** | Lower | Slightly higher (cross-zone traffic) |
| **Use Case** | Dev/test, cost-sensitive | Production, HA required |

#### Creating MIGs
```bash
# Create instance template
gcloud compute instance-templates create web-server-template \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-standard \
  --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y nginx
    systemctl start nginx' \
  --tags=http-server,https-server \
  --scopes=https://www.googleapis.com/auth/cloud-platform

# Create regional MIG with autoscaling
gcloud compute instance-groups managed create web-server-mig \
  --base-instance-name=web-server \
  --template=web-server-template \
  --size=3 \
  --region=us-central1 \
  --health-check=http-health-check \
  --initial-delay=300

# Configure autoscaling
gcloud compute instance-groups managed set-autoscaling web-server-mig \
  --region=us-central1 \
  --max-num-replicas=10 \
  --min-num-replicas=3 \
  --target-cpu-utilization=0.75 \
  --cool-down-period=60

# Add named ports for load balancing
gcloud compute instance-groups managed set-named-ports web-server-mig \
  --region=us-central1 \
  --named-ports=http:80,https:443
```

#### Rolling Updates and Canary Deployments
```bash
# Start rolling update
gcloud compute instance-groups managed rolling-action start-update web-server-mig \
  --region=us-central1 \
  --version=template=new-web-server-template \
  --max-surge=3 \
  --max-unavailable=0

# Canary deployment (10% on new version)
gcloud compute instance-groups managed rolling-action start-update web-server-mig \
  --region=us-central1 \
  --version=template=stable-template \
  --canary-version=template=canary-template,target-size=10%

# Monitor rollout status
gcloud compute instance-groups managed describe web-server-mig \
  --region=us-central1 \
  --format="yaml(status)"
```

## Cloud Functions (Serverless)

### What are Cloud Functions?
Event-driven serverless compute platform that automatically scales based on demand.

### Key Characteristics
- **Event-driven**: Triggered by HTTP requests, Cloud Storage, Pub/Sub
- **Automatic scaling**: From 0 to thousands of instances
- **No server management**: Google handles infrastructure
- **9-minute timeout**: Maximum execution time (1st gen), 60 minutes (2nd gen)
- **Stateless**: Each invocation is independent

### Supported Runtimes
- **Node.js**: JavaScript runtime
- **Python**: Popular for data processing and automation
- **Go**: High-performance applications
- **Java**: Enterprise applications
- **.NET**: Microsoft stack
- **Ruby**: Web development
- **PHP**: Web applications

### Trigger Types
- **HTTP(S)**: Direct HTTP requests
- **Cloud Storage**: File upload/delete/update
- **Pub/Sub**: Message queue triggers
- **Firestore**: Database changes
- **Firebase**: Authentication, real-time database
- **Cloud Scheduler**: Cron-like scheduling

### Generations Comparison
| Feature | 1st Gen | 2nd Gen |
|---------|---------|---------|
| **Timeout** | 9 minutes | 60 minutes |
| **Instances** | 1000 concurrent | 1000+ concurrent |
| **Memory** | Up to 8GB | Up to 32GB |
| **CPU** | Shared | Dedicated available |
| **Traffic Allocation** | Limited | Advanced |

## Cloud Run (Containers)

### What is Cloud Run?
Fully managed serverless platform for running containerized applications that automatically scales to zero.

### Key Features
- **Container-based**: Run any containerized application
- **Serverless**: No infrastructure management
- **Scale to zero**: Pay only when handling requests
- **Portable**: Standard containers work anywhere
- **HTTP/HTTPS**: RESTful APIs and web applications

### Cloud Run vs Cloud Functions
| Feature | Cloud Run | Cloud Functions |
|---------|-----------|-----------------|
| **Runtime** | Any container | Specific runtimes |
| **Languages** | Any language | Supported runtimes only |
| **Deployment** | Container images | Source code |
| **Concurrency** | Up to 1000 per instance | 1 per instance (1st gen) |
| **Cold Start** | Generally faster | Varies by runtime |
| **Use Case** | Web apps, APIs | Event processing |

### Cloud Run Services vs Jobs
| Type | Purpose | Execution | Use Case |
|------|---------|-----------|----------|
| **Services** | Handle requests | On-demand | Web applications, APIs |
| **Jobs** | Run to completion | Scheduled/triggered | Batch processing, data pipelines |

---

## Google Kubernetes Engine (GKE)

### What is GKE?
Google Kubernetes Engine is a managed, production-ready Kubernetes platform that provides a fully managed control plane, automatic upgrades, built-in security features, and integrated monitoring. GKE runs certified Kubernetes ensuring portability across clouds and on-premises.

### GKE Architecture Components

#### Control Plane (Managed by Google)
| Component | Purpose | SLA |
|-----------|---------|-----|
| **API Server** | Kubernetes API endpoint | 99.95% (zonal), 99.99% (regional) |
| **etcd** | Cluster state storage | Automatically replicated |
| **Controller Manager** | Reconciliation loops | Highly available |
| **Scheduler** | Pod placement decisions | Highly available |
| **Cloud Controller Manager** | GCP integration | Automatic |

#### Node Components (Your Responsibility in Standard)
| Component | Purpose | Configurable |
|-----------|---------|--------------|
| **kubelet** | Node agent | Version via node pool |
| **kube-proxy** | Network proxy | IP tables/IPVS mode |
| **Container Runtime** | containerd | Default, no alternatives |
| **Node OS** | Container-Optimized OS, Ubuntu | Selectable |

### Cluster Types - Deep Dive

#### Standard Mode
**Full control over cluster configuration and node management**

```bash
# Create Standard GKE cluster with custom configuration
gcloud container clusters create production-standard \
  --region=us-central1 \
  --node-locations=us-central1-a,us-central1-b,us-central1-c \
  --machine-type=n2-standard-4 \
  --num-nodes=2 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=5 \
  --enable-autorepair \
  --enable-autoupgrade \
  --maintenance-window-start=2023-01-01T00:00:00Z \
  --maintenance-window-duration=4h \
  --maintenance-window-recurrence="FREQ=WEEKLY;BYDAY=SU" \
  --enable-stackdriver-kubernetes \
  --enable-ip-alias \
  --network=custom-vpc \
  --subnetwork=gke-subnet \
  --cluster-secondary-range-name=pods \
  --services-secondary-range-name=services \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.0/28 \
  --enable-master-authorized-networks \
  --master-authorized-networks=10.0.0.0/8 \
  --addons=HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver \
  --workload-pool=PROJECT_ID.svc.id.goog \
  --enable-shielded-nodes \
  --shielded-secure-boot \
  --shielded-integrity-monitoring \
  --release-channel=regular \
  --enable-network-policy \
  --logging=SYSTEM,WORKLOAD \
  --monitoring=SYSTEM,WORKLOAD
```

**Standard Mode Best For:**
- Stateful applications requiring specific node configurations
- GPU/TPU workloads
- DaemonSets with specific requirements
- Windows Server containers
- Cost optimization through custom node sizing
- Legacy applications with specific kernel requirements

#### Autopilot Mode
**Google manages nodes, you deploy workloads**

```bash
# Create Autopilot GKE cluster
gcloud container clusters create-auto production-autopilot \
  --region=us-central1 \
  --network=custom-vpc \
  --subnetwork=gke-subnet \
  --cluster-secondary-range-name=pods \
  --services-secondary-range-name=services \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.0/28 \
  --release-channel=regular \
  --workload-pool=PROJECT_ID.svc.id.goog \
  --enable-master-authorized-networks \
  --master-authorized-networks=10.0.0.0/8
```

**Autopilot Restrictions:**
- No SSH access to nodes
- No DaemonSets (except approved list)
- No privileged pods (unless approved)
- No hostPath or hostNetwork
- No GPUs (currently)
- No Windows nodes

**Autopilot Best For:**
- Microservices architectures
- Cloud-native applications
- Teams wanting minimal operations
- Predictable workloads
- Development and staging environments
- Startups optimizing for speed

#### Standard vs Autopilot - Detailed Comparison

| Aspect | Standard Mode | Autopilot Mode |
|--------|---------------|----------------|
| **Node Management** | Manual provisioning, scaling, upgrades | Fully automated by Google |
| **Pricing Model** | Pay for all provisioned nodes (even if idle) | Pay only for requested pod resources |
| **Minimum Cost** | 3 x node cost (typically $50-100/month) | $0 with no workloads |
| **Compute Classes** | Any machine type (E2, N1, N2, C2, M1, etc.) | Balanced (N2D), Scale-out (T2D), General Purpose |
| **Security** | Manual configuration required | Hardened by default (Shielded GKE, Workload Identity) |
| **Node Access** | SSH access available | No SSH access |
| **Cluster Autoscaling** | Configure Cluster Autoscaler | Automatic, no configuration |
| **Vertical Pod Autoscaler** | Optional add-on | Enabled by default |
| **Binary Authorization** | Optional | Enabled by default |
| **Network Policy** | Optional (Calico or built-in) | Dataplane V2 with eBPF |
| **Pod Security** | Manual PSP/PSS configuration | Pod Security Standards enforced |
| **Node OS** | COS, Ubuntu, Windows | Container-Optimized OS only |
| **Node Pools** | Multiple pools with different configs | Single logical pool, auto-configured |
| **GPU/TPU Support** | Full support | Limited (expanding) |
| **Windows Containers** | Supported | Not supported |
| **Spot/Preemptible** | Configure per node pool | Configure per pod via nodeSelector |
| **Best For** | Custom requirements, GPU, Windows, cost optimization | Simplicity, security, fast deployment |

### GKE Networking

#### Network Models

**VPC-Native Clusters (Alias IP)**
```bash
# Create VPC-native cluster with custom IP ranges
gcloud container clusters create vpc-native-cluster \
  --region=us-central1 \
  --enable-ip-alias \
  --network=my-vpc \
  --subnetwork=gke-subnet \
  --cluster-ipv4-cidr=/14 \
  --services-ipv4-cidr=/20 \
  --cluster-secondary-range-name=pods-range \
  --services-secondary-range-name=services-range
```

**IP Range Planning:**
```
Cluster Sizing:
- Small (< 100 nodes): /21 for pods, /24 for services
- Medium (100-1000 nodes): /18 for pods, /22 for services
- Large (1000+ nodes): /14 for pods, /20 for services

Nodes per Subnet:
- Max pods per node (default): 110
- IP addresses per node: 110 + 2 (node IP + reserved)
- Subnet size for 100 nodes: /20 (4096 IPs)
```

#### Private GKE Clusters
```bash
# Create private cluster
gcloud container clusters create private-cluster \
  --region=us-central1 \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.0/28 \
  --enable-ip-alias \
  --enable-master-authorized-networks \
  --master-authorized-networks=10.0.0.0/8,192.168.1.0/24
```

**Private Cluster Options:**
| Configuration | Public Endpoint | Private Endpoint | Use Case |
|---------------|-----------------|------------------|----------|
| **Public Cluster** | Yes | No | Development, demos |
| **Private Nodes** | Yes (control plane) | Yes (nodes) | Standard production |
| **Fully Private** | No | Yes | High security environments |

### Node Pools - Advanced Configuration

#### Multiple Node Pool Strategy
```bash
# System node pool (small, on-demand)
gcloud container node-pools create system-pool \
  --cluster=production-cluster \
  --zone=us-central1-a \
  --machine-type=e2-standard-2 \
  --num-nodes=2 \
  --node-taints=dedicated=system:NoSchedule \
  --node-labels=pool=system

# Application node pool (autoscaling)
gcloud container node-pools create app-pool \
  --cluster=production-cluster \
  --zone=us-central1-a \
  --machine-type=n2-standard-4 \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=20 \
  --node-labels=pool=application,workload=general

# Spot node pool (cost-optimized)
gcloud container node-pools create spot-pool \
  --cluster=production-cluster \
  --zone=us-central1-a \
  --spot \
  --machine-type=n2-standard-4 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=50 \
  --node-labels=pool=spot,workload=batch \
  --node-taints=spot=true:NoSchedule

# High-memory node pool
gcloud container node-pools create memory-pool \
  --cluster=production-cluster \
  --zone=us-central1-a \
  --machine-type=n2-highmem-8 \
  --num-nodes=2 \
  --node-labels=pool=memory,workload=cache \
  --node-taints=dedicated=memory:NoSchedule

# GPU node pool
gcloud container node-pools create gpu-pool \
  --cluster=production-cluster \
  --zone=us-central1-a \
  --machine-type=n1-standard-4 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --num-nodes=2 \
  --node-labels=pool=gpu,accelerator=tesla-t4 \
  --node-taints=nvidia.com/gpu=present:NoSchedule
```

#### Node Pool Design Patterns

**Multi-Pool Strategy:**
| Pool Type | Machine Type | Scaling | Taints | Use Case |
|-----------|-------------|---------|--------|----------|
| **System** | e2-standard-2 | Fixed (2-3 nodes) | dedicated=system | kube-system pods, monitoring |
| **General** | n2-standard-4 | Autoscale (3-20) | None | Stateless applications |
| **Memory** | n2-highmem-8 | Autoscale (0-10) | dedicated=memory | Caches, in-memory processing |
| **Compute** | c2-standard-8 | Autoscale (0-10) | dedicated=compute | CPU-intensive workloads |
| **Spot** | n2-standard-4 | Autoscale (0-50) | spot=true | Batch jobs, fault-tolerant apps |
| **GPU** | n1-standard-4 + T4 | Fixed (2-4) | nvidia.com/gpu | ML inference, training |

### Workload Identity - Secure GCP Access

#### What is Workload Identity?
Recommended way for pods to authenticate to Google Cloud services using Kubernetes service accounts mapped to Google Cloud service accounts.

#### Configuration Steps
```bash
# 1. Enable Workload Identity on cluster
gcloud container clusters update production-cluster \
  --region=us-central1 \
  --workload-pool=PROJECT_ID.svc.id.goog

# 2. Enable on node pool
gcloud container node-pools update default-pool \
  --cluster=production-cluster \
  --region=us-central1 \
  --workload-metadata=GKE_METADATA

# 3. Create Kubernetes Service Account
kubectl create serviceaccount my-app-ksa \
  --namespace=production

# 4. Create Google Service Account
gcloud iam service-accounts create my-app-gsa \
  --display-name="My App Service Account"

# 5. Grant GCP permissions to GSA
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:my-app-gsa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# 6. Bind KSA to GSA
gcloud iam service-accounts add-iam-policy-binding \
  my-app-gsa@PROJECT_ID.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:PROJECT_ID.svc.id.goog[production/my-app-ksa]"

# 7. Annotate Kubernetes Service Account
kubectl annotate serviceaccount my-app-ksa \
  --namespace=production \
  iam.gke.io/gcp-service-account=my-app-gsa@PROJECT_ID.iam.gserviceaccount.com
```

#### Using Workload Identity in Pods
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: workload-identity-test
  namespace: production
spec:
  serviceAccountName: my-app-ksa
  containers:
  - name: app
    image: google/cloud-sdk:slim
    command: ["sleep", "infinity"]
```

**Without Workload Identity (NEVER DO THIS):**
```yaml
# BAD: Downloading service account keys
- env:
  - name: GOOGLE_APPLICATION_CREDENTIALS
    value: /secrets/service-account-key.json
  volumeMounts:
  - name: sa-key
    mountPath: /secrets
volumes:
- name: sa-key
  secret:
    secretName: gcp-key-secret
```

### Binary Authorization

#### What is Binary Authorization?
Deploy-time security control ensuring only trusted container images are deployed to GKE.

#### Configuration
```bash
# Enable Binary Authorization on cluster
gcloud container clusters update production-cluster \
  --region=us-central1 \
  --enable-binauthz

# Create attestor
gcloud container binauthz attestors create prod-attestor \
  --attestation-authority-note=prod-note \
  --attestation-authority-note-project=PROJECT_ID

# Create policy requiring attestation
cat > policy.yaml << EOF
admissionWhitelistPatterns:
- namePattern: gcr.io/google_containers/*
- namePattern: k8s.gcr.io/*
- namePattern: gke.gcr.io/*
defaultAdmissionRule:
  requireAttestationsBy:
  - projects/PROJECT_ID/attestors/prod-attestor
  evaluationMode: REQUIRE_ATTESTATION
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
globalPolicyEvaluationMode: ENABLE
EOF

# Import policy
gcloud container binauthz policy import policy.yaml
```

#### Attestation in CI/CD Pipeline
```bash
# In CI/CD pipeline after image build and scan
IMAGE_DIGEST=$(gcloud container images describe \
  gcr.io/PROJECT_ID/app:v1.0.0 \
  --format='get(image_summary.digest)')

# Create attestation
gcloud container binauthz attestations sign-and-create \
  --artifact-url="gcr.io/PROJECT_ID/app@${IMAGE_DIGEST}" \
  --attestor=prod-attestor \
  --attestor-project=PROJECT_ID \
  --keyversion=projects/PROJECT_ID/locations/global/keyRings/binauthz/cryptoKeys/attestor-key/cryptoKeyVersions/1
```

### GKE Security Best Practices

#### Cluster Hardening Checklist
| Security Control | Configuration | Why It Matters |
|------------------|---------------|----------------|
| **Private Cluster** | `--enable-private-nodes` | Nodes not exposed to internet |
| **Authorized Networks** | `--enable-master-authorized-networks` | Restrict API access |
| **Workload Identity** | `--workload-pool=PROJECT_ID.svc.id.goog` | No service account keys |
| **Binary Authorization** | `--enable-binauthz` | Only trusted images deploy |
| **Shielded Nodes** | `--enable-shielded-nodes` | Boot integrity verification |
| **Network Policy** | `--enable-network-policy` | Pod-to-pod traffic control |
| **Pod Security Standards** | Admission controller | Prevent privileged pods |
| **Secrets Encryption** | `--database-encryption-key` | Encrypt secrets at rest |
| **Audit Logging** | `--enable-cloud-logging` | Security forensics |
| **VPC Flow Logs** | On subnet | Network monitoring |
| **GKE Dataplane V2** | `--enable-dataplane-v2` | eBPF-based networking |
| **Vulnerability Scanning** | Artifact Registry | Scan images for CVEs |

#### Network Policy Example
```yaml
# Deny all ingress by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
# Allow specific ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

### GKE Enterprise (formerly Anthos)

#### Features
| Feature | Description | Use Case |
|---------|-------------|----------|
| **Multi-cluster Management** | Manage GKE + on-prem clusters | Hybrid/multi-cloud |
| **Config Management** | GitOps for policies | Configuration drift prevention |
| **Service Mesh** | Istio-based service mesh | Microservices observability |
| **Cloud Run for Anthos** | Serverless on GKE | Developer productivity |
| **Policy Controller** | OPA-based policies | Compliance enforcement |

#### Config Management Setup
```bash
# Enable Config Management
gcloud beta container fleet config-management enable

# Register cluster
gcloud container fleet memberships register production-cluster \
  --gke-cluster=us-central1/production-cluster \
  --enable-workload-identity

# Configure Config Sync
cat > config-management.yaml << EOF
apiVersion: configmanagement.gke.io/v1
kind: ConfigManagement
metadata:
  name: config-management
spec:
  clusterName: production-cluster
  git:
    syncRepo: https://github.com/org/config-repo
    syncBranch: main
    secretType: none
    policyDir: config
  policyController:
    enabled: true
    templateLibraryInstalled: true
EOF

kubectl apply -f config-management.yaml
```

---

## Container Optimization

### Container Best Practices

#### Multi-Stage Builds
```dockerfile
# BAD: Single-stage build (large image)
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["node", "dist/server.js"]
# Result: 1.2 GB image

# GOOD: Multi-stage build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
EXPOSE 3000
USER node
CMD ["node", "dist/server.js"]
# Result: 180 MB image
```

#### Distroless Images
```dockerfile
# Option 1: Google Distroless (recommended for Go)
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/server /server
EXPOSE 8080
USER nonroot:nonroot
CMD ["/server"]
# Result: 25 MB image, minimal attack surface

# Option 2: Distroless for Java
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM gcr.io/distroless/java17-debian12
COPY --from=builder /app/target/app.jar /app.jar
EXPOSE 8080
CMD ["/app.jar"]
# Result: 250 MB vs 600 MB with full JDK
```

#### Layer Optimization
```dockerfile
# BAD: Layers not optimized
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
# Every code change rebuilds dependencies

# GOOD: Optimize layer caching
FROM python:3.11-slim
WORKDIR /app

# Install dependencies first (changes rarely)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (changes frequently)
COPY . .

# Run as non-root
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
```

#### Security Scanning Configuration
```bash
# Enable vulnerability scanning in Artifact Registry
gcloud artifacts repositories create my-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository" \
  --enable-vulnerability-scanning

# Scan specific image
gcloud artifacts docker images scan gcr.io/PROJECT_ID/app:latest \
  --location=us-central1

# List vulnerabilities
gcloud artifacts docker images list-tags gcr.io/PROJECT_ID/app \
  --format="table(tag,vulnerabilities.severity)"

# Get detailed vulnerability report
gcloud artifacts docker images describe \
  gcr.io/PROJECT_ID/app:latest \
  --show-occurrences \
  --format=json
```

#### Container Image Optimization Matrix
| Technique | Size Reduction | Build Time | Security | Complexity |
|-----------|----------------|------------|----------|------------|
| **Multi-stage builds** | 60-80% | Slightly longer | Better | Low |
| **Distroless base** | 70-90% | Same | Much better | Low |
| **Alpine Linux** | 50-70% | Same | Good | Medium (musl libc) |
| **Layer optimization** | 10-30% | Faster rebuilds | Same | Low |
| **Compression** | 20-40% | Longer | Same | Low |
| **Remove build tools** | 40-60% | Same | Better | Medium |

### Dockerfile Best Practices for GKE

```dockerfile
# Complete production-ready Dockerfile
FROM node:18-alpine AS base
WORKDIR /app

# Install dependencies for building native modules
RUN apk add --no-cache python3 make g++

# Development dependencies
FROM base AS dependencies
COPY package*.json ./
RUN npm ci --only=production
RUN cp -R node_modules /tmp/node_modules
RUN npm ci

# Build application
FROM dependencies AS build
COPY . .
RUN npm run build
RUN npm run test

# Production image
FROM node:18-alpine AS production
WORKDIR /app

# Install dumb-init to handle signals properly
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

# Copy production dependencies
COPY --from=dependencies /tmp/node_modules ./node_modules

# Copy built application
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist
COPY --from=build --chown=nodejs:nodejs /app/package*.json ./

# Security hardening
RUN chmod -R 555 /app && \
    chmod -R 555 /app/node_modules

USER nodejs

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

EXPOSE 3000

# Use dumb-init to properly handle SIGTERM
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

---

## Kubernetes on GKE

### Deployment Patterns

#### Basic Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
    version: v1
spec:
  replicas: 3
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: web-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: web-app
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: web-app-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: web-app
        image: gcr.io/PROJECT_ID/web-app:v1.2.3
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        envFrom:
        - configMapRef:
            name: app-config
        resources:
          requests:
            cpu: 250m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 30
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
        - name: cache
          mountPath: /app/cache
      volumes:
      - name: config
        configMap:
          name: app-config
      - name: cache
        emptyDir:
          sizeLimit: 500Mi
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web-app
              topologyKey: kubernetes.io/hostname
```

#### StatefulSet for Stateful Applications
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-cluster
  namespace: production
spec:
  serviceName: redis-cluster
  replicas: 3
  selector:
    matchLabels:
      app: redis-cluster
  template:
    metadata:
      labels:
        app: redis-cluster
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - redis-cluster
            topologyKey: kubernetes.io/hostname
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
          name: client
        - containerPort: 16379
          name: gossip
        command:
        - redis-server
        - "--appendonly"
        - "yes"
        - "--cluster-enabled"
        - "yes"
        - "--cluster-config-file"
        - "/data/nodes.conf"
        - "--cluster-node-timeout"
        - "5000"
        volumeMounts:
        - name: data
          mountPath: /data
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: pd-ssd
      resources:
        requests:
          storage: 10Gi
```

#### DaemonSet Example
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-gcp
  namespace: kube-system
  labels:
    app: fluentd-gcp
spec:
  selector:
    matchLabels:
      app: fluentd-gcp
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  template:
    metadata:
      labels:
        app: fluentd-gcp
    spec:
      serviceAccountName: fluentd-gcp
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule
      containers:
      - name: fluentd-gcp
        image: gcr.io/google-containers/fluentd-gcp:latest
        env:
        - name: FLUENTD_ARGS
          value: --no-supervisor -q
        resources:
          limits:
            memory: 500Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

### Service Types and Ingress

#### ClusterIP Service (Internal)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    protocol: TCP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

#### LoadBalancer Service (External)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: production
  annotations:
    cloud.google.com/neg: '{"ingress": true}'
    cloud.google.com/backend-config: '{"ports": {"80":"backend-config"}}'
spec:
  type: LoadBalancer
  loadBalancerIP: 34.56.78.90  # Reserved static IP
  selector:
    app: frontend
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  - name: https
    port: 443
    targetPort: 8080
    protocol: TCP
```

#### Ingress with Google Cloud Load Balancer
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: "gce"
    kubernetes.io/ingress.global-static-ip-name: "web-static-ip"
    networking.gke.io/managed-certificates: "main-cert"
    kubernetes.io/ingress.allow-http: "false"
spec:
  rules:
  - host: www.example.com
    http:
      paths:
      - path: /api/*
        pathType: ImplementationSpecific
        backend:
          service:
            name: api-service
            port:
              number: 8080
      - path: /*
        pathType: ImplementationSpecific
        backend:
          service:
            name: frontend-service
            port:
              number: 80
---
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: main-cert
  namespace: production
spec:
  domains:
  - www.example.com
  - example.com
```

### ConfigMaps and Secrets

#### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  # Simple values
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"

  # Configuration files
  app.conf: |
    server {
      port = 8080
      timeout = 30s
      max_connections = 100
    }

  nginx.conf: |
    user nginx;
    worker_processes auto;
    error_log /var/log/nginx/error.log warn;
    pid /var/run/nginx.pid;

    events {
      worker_connections 1024;
    }

    http {
      include /etc/nginx/mime.types;
      default_type application/octet-stream;

      log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

      access_log /var/log/nginx/access.log main;
      sendfile on;
      keepalive_timeout 65;

      include /etc/nginx/conf.d/*.conf;
    }
```

#### Secret (use with caution - consider Secret Manager)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
stringData:
  database-url: "postgresql://user:pass@db.example.com:5432/prod"
  api-key: "sk-1234567890abcdef"
---
# Better: Use External Secrets Operator with Secret Manager
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: gcpsm-secret-store
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-url
    remoteRef:
      key: database-url
  - secretKey: api-key
    remoteRef:
      key: api-key
```

### Autoscaling - Complete Guide

#### Horizontal Pod Autoscaler (HPA)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 100
  metrics:
  # CPU-based scaling
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Memory-based scaling
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  # Custom metric (requests per second)
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 5
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 10
        periodSeconds: 30
      selectPolicy: Max
```

#### Vertical Pod Autoscaler (VPA)
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-app-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  updatePolicy:
    updateMode: "Auto"  # Off, Initial, Recreate, Auto
  resourcePolicy:
    containerPolicies:
    - containerName: web-app
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2000m
        memory: 4Gi
      controlledResources: ["cpu", "memory"]
      mode: Auto
```

#### Cluster Autoscaler Configuration
```bash
# Enable cluster autoscaler on node pool
gcloud container node-pools update default-pool \
  --cluster=production-cluster \
  --region=us-central1 \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=50

# Configure autoscaler profile
gcloud container clusters update production-cluster \
  --region=us-central1 \
  --autoscaling-profile=optimize-utilization

# Available profiles:
# - balanced: Default balance between resource optimization and latency
# - optimize-utilization: Prioritize cluster resource usage
```

#### Autoscaling Decision Matrix
| Autoscaler | What It Scales | When to Use | Limitations |
|------------|----------------|-------------|-------------|
| **HPA** | Pod replicas | CPU/memory/custom metrics exceed threshold | Requires resource requests, can't go below 1 pod |
| **VPA** | Pod resource requests/limits | Right-size individual pods | May restart pods, conflicts with HPA on CPU/memory |
| **Cluster Autoscaler** | Number of nodes | Pods pending due to insufficient resources | Startup delay (2-5 min), cost of additional nodes |
| **Multidimensional Pod Autoscaler (MPA)** | Both replicas and resources | Complex scaling requirements | Alpha feature, limited support |

---

## Hybrid and Multi-Cloud (Anthos)

### Anthos Overview

#### Components
| Component | Purpose | Deployment Target |
|-----------|---------|-------------------|
| **GKE** | Managed Kubernetes on GCP | Google Cloud |
| **GKE on VMware** | Kubernetes on VMware infrastructure | On-premises |
| **GKE on AWS** | Kubernetes on AWS infrastructure | AWS |
| **GKE on Azure** | Kubernetes on Azure infrastructure | Azure |
| **GKE on Bare Metal** | Kubernetes on physical servers | On-premises |
| **Anthos Config Management** | GitOps configuration sync | All clusters |
| **Anthos Service Mesh** | Istio-based service mesh | All clusters |
| **Cloud Run for Anthos** | Serverless on Kubernetes | GKE clusters |
| **Anthos Policy Controller** | OPA-based policy enforcement | All clusters |

### Anthos Service Mesh (ASM)

#### Installation
```bash
# Download asmcli
curl https://storage.googleapis.com/csm-artifacts/asm/asmcli > asmcli
chmod +x asmcli

# Install ASM on GKE cluster
./asmcli install \
  --project_id PROJECT_ID \
  --cluster_name production-cluster \
  --cluster_location us-central1 \
  --fleet_id PROJECT_ID \
  --output_dir ./asm-output \
  --enable_all \
  --ca mesh_ca

# Enable sidecar injection for namespace
kubectl label namespace production istio-injection=enabled
```

#### Service Mesh Configuration
```yaml
# Virtual Service for traffic routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews-route
  namespace: production
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        user-agent:
          regex: ".*Mobile.*"
    route:
    - destination:
        host: reviews
        subset: v2
      weight: 100
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10
---
# Destination Rule for load balancing
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews-destination
  namespace: production
spec:
  host: reviews
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

---

## Architecture Patterns

### Microservices Pattern
```yaml
# API Gateway (Kong/Ambassador)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: kong
        image: kong:3.4
        env:
        - name: KONG_DATABASE
          value: "postgres"
        - name: KONG_PG_HOST
          value: "postgres-service"
        ports:
        - containerPort: 8000
          name: proxy
        - containerPort: 8443
          name: proxy-ssl
        - containerPort: 8001
          name: admin
```

### Sidecar Pattern
```yaml
# Main application with logging sidecar
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-sidecar
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      # Main application
      - name: application
        image: gcr.io/PROJECT_ID/myapp:v1
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: logs
          mountPath: /var/log

      # Sidecar for log shipping
      - name: log-shipper
        image: fluent/fluent-bit:latest
        volumeMounts:
        - name: logs
          mountPath: /var/log
          readOnly: true
        - name: fluent-bit-config
          mountPath: /fluent-bit/etc/

      volumes:
      - name: logs
        emptyDir: {}
      - name: fluent-bit-config
        configMap:
          name: fluent-bit-config
```

### Ambassador Pattern
```yaml
# Ambassador proxy for external service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-ambassador
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      # Main application (connects to localhost)
      - name: application
        image: gcr.io/PROJECT_ID/myapp:v1
        env:
        - name: EXTERNAL_API_URL
          value: "http://localhost:8081"

      # Ambassador proxy (handles auth, rate limiting, etc.)
      - name: ambassador
        image: gcr.io/PROJECT_ID/ambassador-proxy:v1
        ports:
        - containerPort: 8081
        env:
        - name: UPSTREAM_URL
          value: "https://external-api.example.com"
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: api-credentials
              key: api-key
```

### Adapter Pattern
```yaml
# Adapter for metric transformation
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-adapter
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      # Main application (outputs custom metrics)
      - name: application
        image: gcr.io/PROJECT_ID/legacy-app:v1
        ports:
        - containerPort: 8080

      # Adapter (converts metrics to Prometheus format)
      - name: metrics-adapter
        image: gcr.io/PROJECT_ID/metrics-adapter:v1
        ports:
        - containerPort: 9090
          name: metrics
```

---

## App Engine (Platform-as-a-Service)

### What is App Engine?
Fully managed serverless platform for deploying applications with automatic scaling and traffic management.

### Environments
| Environment | Language Support | Flexibility | Use Case |
|-------------|------------------|-------------|----------|
| **Standard** | Specific runtimes | Limited | Simple web apps, APIs |
| **Flexible** | Any runtime in container | More flexible | Complex applications |

### Standard Environment Features
- **Automatic scaling**: Scale to zero or handle traffic spikes
- **Free tier**: Generous free quotas
- **Sandboxed**: Secure runtime environment
- **Fast startup**: Quick instance startup times
- **Integrated services**: Built-in integration with Google services

### Flexible Environment Features
- **Custom runtimes**: Any language or framework
- **SSH access**: Debug running instances
- **Docker containers**: Custom container images
- **More resources**: Higher memory and CPU limits
- **Local disk**: Persistent local storage

## Container Registry & Artifact Registry

### Container Registry (Legacy)
- **Purpose**: Store and manage Docker container images
- **Storage**: Built on Cloud Storage
- **Status**: Being replaced by Artifact Registry

### Artifact Registry (Current)
- **Purpose**: Universal package manager for containers and language packages
- **Formats**: Docker, Maven, npm, Python, Go modules
- **Features**: Regional storage, IAM integration, vulnerability scanning
- **Security**: Container analysis, binary authorization

## Service Comparison & Decision Tree

### When to Choose What?

#### Compute Engine vs App Engine vs Cloud Run vs Cloud Functions
```
Need full OS control? → Compute Engine
Traditional web application? → App Engine
Containerized application? → Cloud Run
Event-driven function? → Cloud Functions
```

#### Container Orchestration Decision
```
Need Kubernetes features? → GKE
Want Google to manage everything? → GKE Autopilot
Simple container deployment? → Cloud Run
Traditional PaaS approach? → App Engine
```

#### Serverless Options
```
HTTP API/web app? → Cloud Run or App Engine
Event processing? → Cloud Functions
Scheduled jobs? → Cloud Run Jobs
Batch processing? → Cloud Functions or Cloud Run Jobs
```

## Practical Examples

### Web Application Architecture
- **Frontend**: App Engine or Cloud Run
- **API**: Cloud Run or Cloud Functions
- **Background Jobs**: Cloud Functions or Cloud Run Jobs
- **Static Assets**: Cloud Storage + Cloud CDN

### Microservices on GKE
- **Container Platform**: GKE Autopilot
- **Service Mesh**: Istio (available as GKE add-on)
- **Load Balancing**: Google Cloud Load Balancer
- **Monitoring**: Google Cloud Operations

### Event-Driven Processing
- **Trigger**: Cloud Storage file upload
- **Processing**: Cloud Functions
- **Queue**: Pub/Sub for complex workflows
- **Storage**: Cloud Storage or Firestore

### Batch Processing
- **Orchestration**: Cloud Composer (Airflow)
- **Processing**: Cloud Run Jobs or Compute Engine
- **Data**: Cloud Storage for input/output
- **Monitoring**: Cloud Monitoring

---

## Architecture Scenarios

### Scenario 1: E-Commerce Platform with Microservices

**Requirements:**
- High availability across multiple regions
- Traffic spikes during sales events (10x normal load)
- PCI-DSS compliance for payment processing
- Real-time inventory management
- Cost optimization during off-peak hours

**Solution:**
```
Architecture:
├── Frontend: Cloud Run (auto-scales, global)
├── API Gateway: API Gateway with Cloud Armor
├── Microservices:
│   ├── User Service: GKE Autopilot (regional)
│   ├── Product Service: GKE Autopilot (regional)
│   ├── Order Service: GKE Autopilot (regional)
│   └── Payment Service: GKE Standard on sole-tenant nodes (PCI-DSS)
├── Databases:
│   ├── User DB: Cloud SQL (multi-region)
│   ├── Product DB: Firestore (global)
│   └── Order DB: Cloud Spanner (global, ACID)
├── Caching: Memorystore Redis (regional)
├── Event Processing: Pub/Sub → Cloud Functions
└── Background Jobs: Cloud Run Jobs + Spot VMs

Key Decisions:
1. GKE Autopilot for most services: Auto-scaling, minimal ops
2. GKE Standard + Sole-tenant for payment: PCI-DSS compliance
3. Cloud Run for frontend: Global edge caching, instant scale
4. Spot VMs for batch jobs: 90% cost savings
5. Regional MIGs with cross-region load balancing: HA
```

**Cost Estimate:**
- Normal load: $3,000/month
- Peak load: $4,500/month (50% increase, not 10x due to efficient scaling)
- Savings: 60% vs. always-provisioned for peak

### Scenario 2: Machine Learning Training Pipeline

**Requirements:**
- Train large models weekly (100+ GPU hours)
- Cost-sensitive (startup budget)
- Inference serving with <100ms latency
- Experiment tracking and reproducibility

**Solution:**
```
Training Pipeline:
├── Orchestration: Cloud Composer (Airflow)
├── Data Prep: Dataflow (batch processing)
├── Training:
│   ├── Primary: GKE Standard with A100 GPUs (spot instances)
│   ├── Fallback: Compute Engine with T4 GPUs (on-demand)
│   └── Checkpointing: Cloud Storage (every 10 minutes)
├── Model Registry: Artifact Registry
└── Experiment Tracking: Agent Platform Experiments (formerly Vertex AI Experiments)

Inference Serving:
├── High-traffic models: GKE with L4 GPUs
├── Medium-traffic: Cloud Run (CPU inference)
└── Batch inference: Compute Engine Spot VMs

Cost Optimization:
- Use Spot VMs (90% discount) for training
- Automatic failover to on-demand if spot unavailable
- Scale-to-zero for inference during off-hours
- Committed use discount for baseline inference load
```

**Cost Breakdown:**
- Training (spot): $200/week vs $2,000 on-demand
- Inference: $500/month with autoscaling
- Total: ~$1,300/month vs $8,500 without optimization

### Scenario 3: Global Media Streaming Platform

**Requirements:**
- Serve video content to 50M+ users globally
- Content transcoding pipeline
- Regional content restrictions
- 99.95% uptime SLA

**Solution:**
```
Content Delivery:
├── CDN: Cloud CDN + Cloud Storage (multi-region)
├── Origin: Regional GKE clusters (us, eu, asia)
├── API Layer: Cloud Run (multi-region)
└── Load Balancing: Global HTTP(S) Load Balancer

Transcoding Pipeline:
├── Upload: Cloud Storage (nearline for source)
├── Processing: Compute Engine MIGs with Spot VMs
├── Job Queue: Cloud Tasks
├── Output: Cloud Storage (standard for delivery)
└── Monitoring: Cloud Monitoring + Pub/Sub

User Management:
├── Authentication: Identity Platform
├── Session: Memorystore (regional)
├── User DB: Firestore (global)
└── Analytics: BigQuery (streaming inserts)

Key Features:
- Multi-region failover (RTO < 30 seconds)
- Regional content filtering via Cloud Armor
- Spot VMs for transcoding (80% cost savings)
- CDN cache hit ratio >95%
```

**Performance:**
- Global latency: <50ms (p95)
- Transcoding cost: $0.02 per GB vs $0.15 with on-demand
- CDN cost: $0.08 per GB served

### Scenario 4: Hybrid Cloud Application (On-prem + GCP)

**Requirements:**
- Migrate gradually from on-premises to cloud
- Maintain connection to on-prem database
- Unified monitoring and management
- Compliance: Data residency in specific regions

**Solution:**
```
Anthos Deployment:
├── GKE Clusters:
│   ├── GKE on-prem (VMware): Legacy apps
│   ├── GKE Cloud (us-central1): New services
│   └── GKE Cloud (europe-west1): EU services
├── Connectivity:
│   ├── Cloud VPN (encrypted tunnel)
│   └── Cloud Interconnect (dedicated, low-latency)
├── Service Mesh: Anthos Service Mesh (Istio)
│   ├── Cross-cluster service discovery
│   ├── mTLS between all services
│   └── Unified traffic management
├── Config Management:
│   ├── Git repository (single source of truth)
│   ├── Policies applied to all clusters
│   └── Automatic drift correction
└── Observability:
    ├── Cloud Monitoring (unified metrics)
    ├── Cloud Logging (centralized logs)
    └── Cloud Trace (distributed tracing)

Migration Strategy:
1. Phase 1: Deploy new services on GKE Cloud
2. Phase 2: Migrate stateless apps (6 months)
3. Phase 3: Migrate databases (12 months)
4. Phase 4: Decommission on-prem (18 months)
```

### Scenario 5: High-Frequency Trading Platform

**Requirements:**
- Ultra-low latency (<1ms p99)
- Extremely high throughput (1M+ ops/sec)
- Strict consistency requirements
- Regulatory compliance (audit trail)

**Solution:**
```
Compute Layer:
├── Trading Engine:
│   ├── Compute Engine: C2 or C2D (highest single-thread performance)
│   ├── Sole-tenant nodes (performance isolation)
│   ├── Local SSDs (NVMe, <100μs latency)
│   └── Premium tier networking
├── API Servers:
│   ├── Regional MIGs with C2 instances
│   ├── Internal HTTP(S) load balancing
│   └── Sub-millisecond health checks
└── Message Bus:
    ├── Self-managed Kafka on C2 instances
    └── Topic partitioning by trading pair

Data Layer:
├── Hot data: Memorystore Redis (in-memory)
├── Warm data: Cloud Bigtable (SSD, <10ms)
├── Cold data: BigQuery (analytics)
└── Audit logs: Cloud Logging + immutable storage

Key Design Choices:
- No GKE: Orchestration overhead unacceptable
- Compute Engine over serverless: Predictable performance
- Sole-tenant nodes: Noisy neighbor prevention
- Committed use discounts: 3-year (57% savings)
- Regional deployment: Avoid cross-region latency
```

**Performance Metrics:**
- P50 latency: 200μs
- P99 latency: 800μs
- Throughput: 1.5M ops/sec
- Cost: $25,000/month (vs $40,000 on-prem)

### Scenario 6: SaaS Multi-Tenant Platform

**Requirements:**
- Support 10,000+ tenant organizations
- Tenant isolation for security and performance
- Per-tenant customization
- Usage-based billing

**Solution:**
```
Tenant Isolation Strategy:
├── Database: Firestore (collection per tenant)
├── Compute: GKE with namespace per tenant
├── Storage: Cloud Storage (bucket per tenant)
└── Networking: Network policies (tenant isolation)

Application Architecture:
├── Shared Services (GKE Autopilot):
│   ├── API Gateway (tenant routing)
│   ├── Authentication service
│   └── Billing service
├── Tenant Workloads (GKE Standard):
│   ├── Multi-pool strategy:
│   │   ├── Small tenants: Shared node pool
│   │   ├── Medium tenants: Shared node pool (higher spec)
│   │   └── Enterprise: Dedicated node pools
│   └── Resource quotas per namespace
├── Data Layer:
│   ├── Firestore: App data (per-tenant collections)
│   ├── Cloud Storage: File storage (per-tenant buckets)
│   └── BigQuery: Analytics (partitioned by tenant_id)
└── Observability:
    ├── Metrics: Tagged by tenant_id
    ├── Logs: Tenant-specific log sinks
    └── Traces: Tenant context propagation

Billing Implementation:
- Cloud Pub/Sub: Usage events stream
- Cloud Functions: Aggregate usage metrics
- BigQuery: Usage data warehouse
- Cloud Scheduler: Daily billing runs
```

**Scaling Characteristics:**
- Onboard new tenant: <30 seconds
- Handle 10,000+ tenants on same cluster
- Cost per tenant: $5-$50/month based on usage

### Scenario 7: Batch Processing Pipeline (Genomics)

**Requirements:**
- Process 10TB of genomic data daily
- Jobs run 4-8 hours each
- Cost-sensitive research budget
- Need job prioritization

**Solution:**
```
Pipeline Architecture:
├── Job Management:
│   ├── Cloud Composer: Workflow orchestration
│   ├── Cloud Tasks: Job queue
│   └── Priority queues (high/medium/low)
├── Compute:
│   ├── Priority 1: Compute Engine on-demand (C2)
│   ├── Priority 2: Compute Engine Spot (C2)
│   ├── Priority 3: Batch API with Spot VMs
│   └── MIG autoscaling (0-1000 instances)
├── Data Storage:
│   ├── Input: Cloud Storage Nearline
│   ├── Working: Local SSD (ephemeral)
│   ├── Output: Cloud Storage Standard
│   └── Archive: Cloud Storage Archive
└── Monitoring:
    ├── Job progress tracking
    ├── Spot VM preemption handling
    └── Automatic retry logic

Cost Optimization:
- Spot VMs for 90% of jobs (91% discount)
- Checkpointing every 30 minutes
- Automatic restart on preemption
- Use local SSD instead of persistent disks
- Archive old data to Archive storage
```

**Cost Analysis:**
```
Without optimization:
- 1000 n2-standard-16 instances × 8 hours × $0.78/hr = $6,240/day
- Monthly cost: ~$187,000

With optimization:
- 900 Spot instances × 8 hours × $0.07/hr = $504/day
- 100 on-demand (fallback) × 8 hours × $0.78/hr = $624/day
- Monthly cost: ~$34,000 (82% savings)
```

### Scenario 8: IoT Data Ingestion Platform

**Requirements:**
- 1M+ IoT devices sending data
- 10,000 messages/second sustained, 100,000/sec peak
- Real-time alerting
- Historical analytics

**Solution:**
```
Ingestion Layer:
├── Entry Point: Cloud IoT Core (device management)
├── Message Broker: Cloud Pub/Sub (autoscaling)
├── Stream Processing: Dataflow (autoscaling)
└── Real-time Alerts: Cloud Functions (event-driven)

Processing Layers:
├── Hot Path (real-time):
│   ├── Dataflow: Streaming aggregation
│   ├── Cloud Functions: Alert evaluation
│   ├── Pub/Sub: Alert notifications
│   └── Memorystore: Real-time state
├── Warm Path (minutes):
│   ├── Dataflow: Batch aggregation
│   └── Cloud SQL: Time-series data
└── Cold Path (historical):
    ├── BigQuery: Data warehouse
    └── Cloud Storage: Raw data archive

Compute Considerations:
- Cloud Functions: Scale 0 to 10,000+ instances
- Dataflow: Autoscale workers (1-1000)
- No pre-provisioned compute needed
- Pay only for actual usage

Device Management:
- Cloud IoT Core: Device registry, authentication
- Device groups for bulk management
- Firmware updates via device commands
```

**Cost at Scale:**
- Pub/Sub: $40/TB ingested
- Dataflow: $0.10/vCPU-hour (autoscaled)
- Functions: $0.40/million invocations
- Total: ~$5,000/month for 1M devices

### Scenario 9: Disaster Recovery Architecture

**Requirements:**
- RPO: 15 minutes
- RTO: 1 hour
- Primary: us-central1
- DR: us-east1

**Solution:**
```
Primary Region (us-central1):
├── Compute: Regional GKE cluster
├── Database: Cloud SQL (regional, automated backups)
├── Cache: Memorystore (standard tier)
└── Storage: Cloud Storage (multi-region)

DR Region (us-east1):
├── Compute: Regional GKE cluster (minimal size, autoscale ready)
├── Database: Cloud SQL read replica
├── Cache: Memorystore (standby)
└── Storage: Cloud Storage (same multi-region bucket)

Replication:
├── Database: Continuous replication (Cloud SQL replica)
├── Storage: Multi-region buckets (automatic)
├── Configuration: Anthos Config Management (GitOps)
└── Images: Artifact Registry (replicated)

Failover Procedure:
1. Detect failure: Cloud Monitoring alert
2. Update DNS: Point to DR region (Cloud DNS, TTL 60s)
3. Promote replica: Cloud SQL read replica → primary
4. Scale GKE: Increase DR cluster size
5. Validate: Health checks pass
6. Total time: 45-60 minutes
```

Automation:
```bash
# Automated failover script
gcloud sql instances promote-replica DR_INSTANCE

gcloud container clusters update dr-cluster \
  --region=us-east1 \
  --enable-autoscaling \
  --min-nodes=10 \
  --max-nodes=100

gcloud dns record-sets transaction start \
  --zone=production-zone
gcloud dns record-sets transaction add \
  --name=app.example.com \
  --type=A \
  --zone=production-zone \
  --ttl=60 \
  DR_LOAD_BALANCER_IP
gcloud dns record-sets transaction execute \
  --zone=production-zone
```

**Cost:**
- Primary region: $10,000/month
- DR region (standby): $2,000/month
- Total DR overhead: 20%

### Scenario 10: Regulated Financial Services Application

**Requirements:**
- FINRA compliance
- Data encryption at rest and in transit
- Audit trail for all access
- Multi-factor authentication
- Geographic data residency (US only)

**Solution:**
```
Security Architecture:
├── Network:
│   ├── Private GKE cluster (no public IPs)
│   ├── VPC Service Controls (security perimeter)
│   ├── Cloud Armor (DDoS protection, WAF rules)
│   └── Cloud NAT (outbound internet access)
├── Compute:
│   ├── GKE Standard (us-central1 only)
│   ├── Shielded GKE nodes (secure boot, vTPM)
│   ├── Binary Authorization (signed images only)
│   └── Pod Security Standards enforced
├── Data:
│   ├── Cloud SQL with CMEK (customer-managed keys)
│   ├── Secrets in Secret Manager (rotation enabled)
│   ├── Database encryption at rest (AES-256)
│   └── TLS 1.3 for all connections
├── Identity:
│   ├── Workload Identity (no service account keys)
│   ├── Cloud Identity with MFA enforced
│   ├── Context-aware access policies
│   └── Service accounts per application
└── Compliance:
    ├── Cloud Audit Logs (Admin, Data Access)
    ├── Access Transparency (Google access logs)
    ├── Cloud DLP (data classification)
    └── Security Command Center (posture management)

Deployment Constraints:
- US regions only: us-central1, us-east1
- No data egress to non-US regions
- VPC Service Controls perimeter enforced
- All images scanned for vulnerabilities
- Binary Authorization blocks unsigned images

Audit Trail:
- Every API call logged
- Database queries logged
- File access logged
- Logs exported to immutable storage
- 7-year retention requirement
```

**Compliance Checklist:**
- [x] Data encryption at rest (CMEK)
- [x] Data encryption in transit (TLS 1.3)
- [x] MFA enforced for all users
- [x] Audit logs enabled and retained
- [x] Geographic data residency (US only)
- [x] Vulnerability scanning enabled
- [x] Security posture monitoring
- [x] Incident response plan
- [x] Regular penetration testing
- [x] Access reviews quarterly

---

## Cost Optimization Strategies

### Compute Engine Cost Optimization

#### 1. Right-Sizing Strategy
```bash
# Analyze current usage
gcloud compute instances list \
  --format="table(name,zone,machineType,status)"

# Get recommendations
gcloud recommender recommendations list \
  --project=PROJECT_ID \
  --recommender=google.compute.instance.MachineTypeRecommender \
  --location=us-central1

# Apply recommendations
gcloud compute instances stop INSTANCE_NAME --zone=ZONE
gcloud compute instances set-machine-type INSTANCE_NAME \
  --zone=ZONE \
  --machine-type=RECOMMENDED_TYPE
gcloud compute instances start INSTANCE_NAME --zone=ZONE
```

#### 2. Sustained Use and Committed Use Discounts
| Usage Pattern | Recommendation | Discount |
|---------------|----------------|----------|
| **24/7 production** | 3-year CUD | 57% |
| **Business hours only** | 1-year CUD + right-size | 35-40% |
| **Variable workload** | Spend-based CUD | 25-35% |
| **Batch processing** | Spot VMs | 91% |
| **Seasonal** | CUD for baseline + on-demand for peaks | 30-45% |

#### 3. Disk Optimization
```
Disk Type Comparison:
├── pd-standard (HDD): $0.040/GB/month, 500 IOPS/TB
├── pd-balanced (SSD): $0.100/GB/month, 3,000 IOPS/GB
├── pd-ssd (SSD): $0.170/GB/month, 30,000 IOPS/GB
└── pd-extreme (SSD): $0.125/GB/month + provisioned IOPS

Recommendations:
- Boot disks: pd-standard (sufficient for most workloads)
- Application data: pd-balanced (best price/performance)
- Databases: pd-ssd or pd-extreme
- Temporary data: Local SSD (no cost, ephemeral)
```

### GKE Cost Optimization

#### 1. Autopilot vs Standard Decision Matrix
| Criteria | Choose Autopilot | Choose Standard |
|----------|------------------|-----------------|
| **Team size** | Small (< 5 engineers) | Large (DevOps team) |
| **Workload type** | Microservices, stateless | Stateful, GPU, custom |
| **Optimization focus** | Simplicity, security | Cost, performance |
| **Expected utilization** | Variable, unpredictable | High, predictable |
| **Cost** | Pay for pods only | Pay for nodes (can be lower at high utilization) |

#### 2. Node Pool Optimization
```bash
# Create cost-optimized node pool
gcloud container node-pools create optimized-pool \
  --cluster=production-cluster \
  --zone=us-central1-a \
  --machine-type=n2d-standard-4 \  # AMD, better price/perf
  --disk-type=pd-standard \          # HDD for cost savings
  --disk-size=50 \                   # Smaller disk
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=20 \
  --enable-autorepair \
  --enable-autoupgrade \
  --node-labels=pool=cost-optimized,workload=batch \
  --preemptible                      # Or --spot for 91% savings
```

#### 3. Bin Packing and Resource Optimization
```yaml
# Optimize pod resource requests for better bin packing
apiVersion: v1
kind: Pod
metadata:
  name: optimized-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        # Match node allocatable resources
        cpu: "950m"      # n2d-standard-4 has ~3.9 CPU allocatable
        memory: "3.5Gi"  # n2d-standard-4 has ~15 GB allocatable
      limits:
        cpu: "1000m"
        memory: "4Gi"
```

#### 4. Cluster Cost Analysis
```bash
# Install kubecost
kubectl create namespace kubecost
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --set kubecostToken="YOUR_TOKEN"

# View cost breakdown
kubectl port-forward -n kubecost deployment/kubecost-cost-analyzer 9090:9090
# Open http://localhost:9090
```

### Container and Serverless Optimization

#### Cloud Run Cost Optimization
```yaml
# Optimize Cloud Run configuration
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: optimized-service
spec:
  template:
    metadata:
      annotations:
        # CPU allocated only during request processing
        run.googleapis.com/cpu-throttling: "true"
        # Minimum instances to avoid cold starts (cost vs. latency trade-off)
        autoscaling.knative.dev/minScale: "0"  # or "1" for low-traffic
        # Maximum instances to control costs
        autoscaling.knative.dev/maxScale: "100"
        # Concurrent requests per instance (higher = fewer instances)
        autoscaling.knative.dev/target: "80"
    spec:
      containers:
      - image: gcr.io/PROJECT_ID/app:latest
        resources:
          limits:
            # Right-size memory (billed in 128 MB increments)
            memory: "512Mi"  # Not 500Mi (billed as 512Mi anyway)
            # CPU allocated proportionally to memory
            cpu: "1000m"
        ports:
        - containerPort: 8080
      # Faster startup = lower costs
      timeoutSeconds: 300
```

#### Cloud Functions Cost Optimization
```javascript
// Optimize function for cost
const functions = require('@google-cloud/functions-framework');

// Reuse connections (outside handler)
const { Pool } = require('pg');
const pool = new Pool({
  max: 1,  // Cloud Functions = 1 concurrent request per instance
  connectionTimeoutMillis: 5000,
});

functions.http('optimizedFunction', async (req, res) => {
  // Set appropriate memory (billed in 128 MB increments)
  // 256 MB: $0.00000463 per 100ms
  // 512 MB: $0.00000925 per 100ms

  // Optimize execution time
  const startTime = Date.now();

  try {
    // Use connection pooling
    const client = await pool.connect();
    try {
      const result = await client.query('SELECT * FROM table');
      res.json(result.rows);
    } finally {
      client.release();
    }
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('Error');
  }

  // Log execution time for optimization
  console.log(`Execution time: ${Date.now() - startTime}ms`);
});
```

### Storage and Network Cost Optimization

#### Storage Class Selection
| Data Type | Access Pattern | Storage Class | Cost/GB/Month |
|-----------|----------------|---------------|---------------|
| **Active data** | Daily access | Standard | $0.020 |
| **Backups** | Monthly access | Nearline | $0.010 |
| **Archives** | Yearly access | Coldline | $0.004 |
| **Compliance** | Rarely accessed | Archive | $0.0012 |

#### Network Egress Optimization
```
Network Egress Costs:
├── Within zone: Free
├── Between zones (same region): $0.01/GB
├── Between regions (US): $0.01/GB
├── Between regions (intercontinental): $0.05-$0.08/GB
├── To internet (first 1 TB): $0.085-$0.12/GB
└── Via Cloud CDN: $0.04-$0.08/GB (cheaper + faster)

Optimization Strategies:
1. Use multi-region storage for global data
2. Enable Cloud CDN for static content
3. Use Cloud NAT for outbound traffic pooling
4. Compress data before transfer
5. Use Cloud Interconnect for large data transfers (vs. internet)
```

### Cost Monitoring and Alerts

#### Budget Alert Configuration
```bash
# Create budget alert
gcloud billing budgets create \
  --billing-account=01234-56789A-BCDEF0 \
  --display-name="Monthly Budget" \
  --budget-amount=10000 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100 \
  --notification-channels=CHANNEL_ID

# Export billing data to BigQuery
gcloud services enable bigquerydatatransfer.googleapis.com
# Configure in console: Billing > Billing export > BigQuery export
```

#### Cost Anomaly Detection
```sql
-- BigQuery query for cost anomalies
WITH daily_costs AS (
  SELECT
    DATE(usage_start_time) AS date,
    service.description AS service,
    SUM(cost) AS daily_cost
  FROM `project.dataset.gcp_billing_export_v1_XXXXXX`
  WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY date, service
),
avg_costs AS (
  SELECT
    service,
    AVG(daily_cost) AS avg_cost,
    STDDEV(daily_cost) AS stddev_cost
  FROM daily_costs
  GROUP BY service
)
SELECT
  d.date,
  d.service,
  d.daily_cost,
  a.avg_cost,
  (d.daily_cost - a.avg_cost) / a.stddev_cost AS z_score
FROM daily_costs d
JOIN avg_costs a USING (service)
WHERE ABS((d.daily_cost - a.avg_cost) / a.stddev_cost) > 2
ORDER BY date DESC, z_score DESC;
```

---

## Exam Tips & Strategies

### Professional Cloud Architect Compute Questions

#### Common Question Patterns

**1. Compute Service Selection**
```
Question Pattern: "A company needs to run [workload type]. Which compute service should they use?"

Decision Framework:
- Need full OS control? → Compute Engine
- Need managed Kubernetes? → GKE
- Need auto-scaling containers? → Cloud Run
- Event-driven processing? → Cloud Functions
- Legacy app with minimal changes? → App Engine

Exam Tip: Look for keywords:
- "OS-level access" → Compute Engine
- "Kubernetes" → GKE
- "Serverless containers" → Cloud Run
- "Event triggers" → Cloud Functions
- "Automatic scaling with minimal management" → App Engine
```

**2. GKE Mode Selection**
```
Question Pattern: "Should this workload use GKE Standard or Autopilot?"

Choose Standard if question mentions:
- GPU/TPU requirements
- Windows containers
- DaemonSets with specific requirements
- Custom node configuration
- HostPath volumes
- SSH access to nodes

Choose Autopilot if question mentions:
- Simplified operations
- Security by default
- Pay-per-pod billing
- Minimum operational overhead

Exam Tip: If not explicitly mentioned, Autopilot is usually the answer for "recommended" or "best practice" questions.
```

**3. High Availability Questions**
```
Question Pattern: "Design for 99.99% availability"

Required Components:
- Regional resources (not zonal)
- Regional MIGs with min 3 zones
- Regional GKE clusters
- Health checks with auto-healing
- Load balancing across zones
- Graceful degradation

Exam Tip:
- 99.9% = single zone is acceptable
- 99.95% = regional is recommended
- 99.99% = regional is required
- 99.999% = multi-region architecture
```

**4. Cost Optimization Questions**
```
Question Pattern: "Reduce costs without impacting performance"

Check for:
1. Predictable workload? → Committed use discounts (57%)
2. Fault-tolerant? → Spot/Preemptible VMs (91%)
3. Variable traffic? → Autoscaling + scale-to-zero
4. Oversized resources? → Right-sizing recommendations
5. Idle resources? → Scheduled scaling

Exam Tip: Spot VMs are almost always wrong for databases or stateful apps.
```

**5. Security and Compliance**
```
Question Pattern: "Ensure secure access to Google Cloud services from GKE"

Correct Answer: Workload Identity
Wrong Answers:
- Service account keys (security risk)
- Node service accounts (too broad)
- Metadata server (deprecated approach)

Exam Tip: Workload Identity is always the answer for "secure" GKE to GCP access.
```

**6. Scaling Scenarios**
```
Question Pattern: "Application needs to handle traffic spikes"

Scaling Options:
- Predictable spikes (e.g., daily) → Scheduled autoscaling
- Unpredictable spikes → Reactive autoscaling (CPU/memory/custom metrics)
- Very large spikes (100x) → Cloud Run or Cloud Functions (instant scale)
- Gradual growth → MIG autoscaling with warm-up period

Exam Tip: Look for scale-to-zero requirement → Cloud Run or Cloud Functions only
```

### Kubernetes Concepts for the Exam

#### Resource Requests vs Limits
```yaml
resources:
  requests:  # Used for scheduling
    cpu: "250m"
    memory: "512Mi"
  limits:  # Maximum allowed
    cpu: "1000m"
    memory: "1Gi"

Exam Tips:
- Requests without limits: Can use excess capacity (good for batch jobs)
- Limits without requests: Requests defaults to limits (wasteful)
- Requests = Limits: Guaranteed QoS (databases)
- Neither: BestEffort QoS (lowest priority)
```

#### Common Gotchas

1. **Stateful vs Stateless**
   - StatefulSet: Stable network identity, ordered deployment, persistent storage
   - Deployment: Interchangeable pods, any order, ephemeral by default
   - Exam tip: Database or queue? → StatefulSet

2. **Service Types**
   - ClusterIP: Internal only (default)
   - NodePort: Exposes on each node (rarely used on GKE)
   - LoadBalancer: External access via Cloud Load Balancer
   - Exam tip: "External access" usually means LoadBalancer or Ingress

3. **Ingress vs Load Balancer Service**
   - LoadBalancer Service: L4, one load balancer per service (expensive)
   - Ingress: L7, one load balancer for multiple services (cost-effective)
   - Exam tip: Multiple services needing external access → Ingress

### Tricky Scenarios and Solutions

#### Scenario: "Application requires GPU for ML inference"
**Wrong Answer:** GKE Autopilot with GPU node pool
**Correct Answer:** GKE Standard with GPU node pool (Autopilot GPU support is limited)
**Exam Tip:** GPU questions almost always require GKE Standard

#### Scenario: "Windows containers for legacy .NET application"
**Wrong Answer:** GKE Autopilot or Cloud Run
**Correct Answer:** GKE Standard with Windows node pool
**Exam Tip:** Windows = GKE Standard or Compute Engine only

#### Scenario: "Comply with PCI-DSS requiring physical isolation"
**Wrong Answer:** Private GKE cluster
**Correct Answer:** Sole-tenant nodes
**Exam Tip:** "Physical isolation" is the key phrase for sole-tenant nodes

#### Scenario: "Batch job that can tolerate interruptions"
**Wrong Answer:** Preemptible VMs with committed use discount
**Correct Answer:** Spot VMs (higher discount, better availability)
**Exam Tip:** For new workloads, prefer Spot over Preemptible

#### Scenario: "Global application requiring <50ms latency worldwide"
**Wrong Answer:** Multi-region GKE with global load balancer
**Correct Answer:** Cloud Run (multi-region) with Cloud CDN
**Exam Tip:** "Global" + "lowest latency" usually means Cloud Run or CDN

### Key Exam Topics Summary

| Topic | Key Points | Common Wrong Answers |
|-------|------------|---------------------|
| **Machine Types** | Choose based on workload (general/compute/memory/GPU) | Using N1 when N2/N2D would be better |
| **Custom Machines** | Cost optimization for unusual requirements | Using predefined types for all workloads |
| **Spot VMs** | 91% discount, no max runtime, fault-tolerant workloads | Using for databases or stateful apps |
| **Sole-tenant** | Physical isolation for compliance/licensing | Using for standard security requirements |
| **CUDs** | 57% discount for 3-year, predictable workloads | Buying CUDs for variable workloads |
| **GKE Autopilot** | Simplified ops, pay-per-pod, security by default | Using for GPU, Windows, or custom needs |
| **GKE Standard** | Full control, custom configs, all features | Using when Autopilot would suffice |
| **Workload Identity** | Secure GKE→GCP access | Using service account keys |
| **Binary Authorization** | Deploy-time security, signed images only | Not mentioning for high-security scenarios |
| **Network Policies** | Pod-to-pod traffic control | Relying only on firewall rules |
| **Cloud Run** | Serverless containers, scale-to-zero, HTTP only | Using for long-running or event-driven |
| **Cloud Functions** | Event-driven, specific runtimes, 9-min timeout | Using for long-running processes |
| **Anthos** | Hybrid/multi-cloud, unified management | Proposing custom solutions for hybrid |

### Time Management for Compute Questions

**Question Type → Time Allocation:**
- Simple service selection: 30-60 seconds
- Architecture design: 2-3 minutes
- Cost optimization: 1-2 minutes
- Security configuration: 1-2 minutes
- Complex scenario: 3-4 minutes

**Strategy:**
1. Read question completely
2. Identify key requirements (HA, cost, security, performance)
3. Eliminate obviously wrong answers
4. Choose based on keywords and patterns
5. Flag for review if unsure (don't spend >3 minutes)

### Practice Questions

1. **Q:** A startup needs to deploy microservices with minimal operational overhead and optimize costs during low traffic periods.
   **A:** GKE Autopilot (managed nodes, pay-per-pod, scales efficiently)

2. **Q:** Legacy Windows application needs migration to cloud with minimal changes.
   **A:** Compute Engine with Windows Server image (lift-and-shift)

3. **Q:** Batch processing job runs weekly for 10 hours, can tolerate interruptions.
   **A:** Compute Engine with Spot VMs (91% discount, checkpointing strategy)

4. **Q:** Real-time trading application requires <1ms latency.
   **A:** Compute Engine C2/C2D with sole-tenant nodes and local SSDs

5. **Q:** Multi-tenant SaaS application needs tenant isolation.
   **A:** GKE with namespaces per tenant + network policies

6. **Q:** Application needs to handle 100x traffic spikes instantly.
   **A:** Cloud Run (serverless scaling, handles bursts automatically)

7. **Q:** ML training pipeline needs GPU compute at lowest cost.
   **A:** GKE Standard with Spot GPU node pool + checkpointing

8. **Q:** Secure pod access to Cloud Storage without service account keys.
   **A:** Workload Identity (bind KSA to GSA)

9. **Q:** Deploy containers from only verified and signed images.
   **A:** Binary Authorization with attestation pipeline

10. **Q:** Global web application requiring 99.99% availability.
    **A:** Multi-region architecture with Cloud Load Balancer + Health checks

---

## Summary

This guide covered comprehensive compute and container topics for the Google Cloud Professional Cloud Architect exam:

1. **Compute Engine:** Machine families, custom types, sole-tenant nodes, CUDs, Spot VMs, and MIGs
2. **GKE Architecture:** Standard vs Autopilot, node pools, networking, security, and GKE Enterprise
3. **Container Optimization:** Multi-stage builds, distroless images, vulnerability scanning
4. **Kubernetes on GKE:** Deployments, StatefulSets, Services, Ingress, autoscaling
5. **Anthos:** Hybrid cloud, service mesh, multi-cluster management
6. **Architecture Patterns:** Microservices, sidecar, ambassador, adapter patterns
7. **Serverless:** Cloud Run, Cloud Functions, App Engine comparison
8. **Cost Optimization:** Right-sizing, CUDs, Spot VMs, resource optimization
9. **Real-world Scenarios:** 10 comprehensive architecture examples
10. **Exam Strategies:** Question patterns, decision frameworks, common gotchas

**Key Takeaways for Exam Success:**
- Understand when to use each compute service
- Know GKE Standard vs Autopilot trade-offs
- Master Workload Identity for security questions
- Recognize cost optimization opportunities
- Practice architecture scenario questions
- Focus on "best practices" and "recommended" solutions
- Remember: Google often wants the managed, secure, cost-effective solution

Good luck on your Professional Cloud Architect exam!