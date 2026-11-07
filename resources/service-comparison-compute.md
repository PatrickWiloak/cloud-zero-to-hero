---
last-updated: 2026-05-03
difficulty: intermediate
---

# Cloud Service Comparison: Compute Services

## Quick Reference

This guide provides a comprehensive comparison of compute services across AWS, Google Cloud Platform (GCP), and Microsoft Azure. Use this to understand equivalent services when switching cloud providers or studying multiple certifications.

## Virtual Machines (IaaS)

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Service Name** | EC2 (Elastic Compute Cloud) | Compute Engine | Virtual Machines (VMs) |
| **Instance Types** | General Purpose (T, M), Compute Optimized (C), Memory Optimized (R, X), Storage Optimized (I, D), Accelerated (P, G, Inf) | General Purpose (N, E2), Compute Optimized (C2, C3), Memory Optimized (M1, M2, M3), Accelerated (A2, G2) | General Purpose (B, D, DC, DS), Compute Optimized (F, FX), Memory Optimized (E, M), Storage Optimized (L), GPU (N, NC, ND, NV) |
| **Pricing Models** | On-Demand, Reserved, Savings Plans, Spot | On-Demand, Committed Use Discounts, Preemptible, Spot | Pay-as-you-go, Reserved, Spot |
| **Cost Savings** | Reserved: 30-70%, Spot: 70-90% | Committed: 37-55%, Preemptible/Spot: 60-91% | Reserved: 40-72%, Spot: up to 90% |
| **Auto-scaling** | Auto Scaling Groups | Managed Instance Groups (MIG) | Virtual Machine Scale Sets (VMSS) |
| **Load Balancing** | Application Load Balancer (ALB), Network Load Balancer (NLB) | HTTP(S) Load Balancer, Network Load Balancer | Application Gateway, Load Balancer |
| **Metadata Service** | Instance Metadata Service (IMDS) | Metadata server | Instance Metadata Service |
| **User Data** | User data scripts | Startup scripts | Custom data, cloud-init |
| **Image Types** | AMI (Amazon Machine Image) | Images, Snapshots | VM Images, Managed Images |
| **Storage** | EBS (Elastic Block Store) | Persistent Disks | Managed Disks |
| **Temporary Storage** | Instance Store | Local SSD | Temporary Storage |

**Documentation:**
- **[📖 AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)** - Complete EC2 guide
- **[📖 GCP Compute Engine Documentation](https://cloud.google.com/compute/docs)** - Complete Compute Engine guide
- **[📖 Azure Virtual Machines Documentation](https://learn.microsoft.com/en-us/azure/virtual-machines/)** - Complete VM guide

---

## Managed Kubernetes

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Service Name** | EKS (Elastic Kubernetes Service) | GKE (Google Kubernetes Engine) | AKS (Azure Kubernetes Service) |
| **Control Plane Cost** | $0.10/hour per cluster | Free (Standard), Pay-per-use (Autopilot) | Free |
| **Worker Node Management** | Self-managed, Managed Node Groups, Fargate | Standard (self-managed), Autopilot (fully managed) | Node pools, Virtual nodes |
| **Serverless Pods** | Fargate | Autopilot | Virtual Kubelet, Azure Container Instances |
| **Auto-scaling** | Cluster Autoscaler, Karpenter | Cluster Autoscaler (built-in) | Cluster Autoscaler |
| **Networking** | Amazon VPC CNI | VPC-native, GKE Dataplane V2 | Azure CNI, kubenet |
| **Service Mesh** | ECS Service Connect (App Mesh retired 2026-09-30) | Anthos Service Mesh, Cloud Service Mesh | Open Service Mesh |
| **GitOps** | Flux, Argo CD | Config Sync (Anthos) | GitOps with Flux |
| **Multi-cluster** | EKS Anywhere | Anthos, GKE Enterprise | Azure Arc-enabled Kubernetes |
| **Windows Support** | Yes | Yes | Yes |
| **GPU Support** | Yes | Yes | Yes |
| **Upgrading** | Manual, managed node groups | GKE release channels (Regular, Rapid, Stable) | Auto-upgrade with maintenance windows |

**Documentation:**
- **[📖 AWS EKS Documentation](https://docs.aws.amazon.com/eks/)** - Complete EKS guide
- **[📖 GCP GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)** - Complete GKE guide
- **[📖 Azure AKS Documentation](https://learn.microsoft.com/en-us/azure/aks/)** - Complete AKS guide

---

## Serverless Compute (Functions-as-a-Service)

| Feature | AWS Lambda | GCP Cloud Functions | GCP Cloud Run | Azure Functions |
|---------|-----------|-------------------|--------------|----------------|
| **Execution Model** | Event-driven functions | Event-driven functions | Containerized applications | Event-driven functions |
| **Languages** | Node.js, Python, Java, .NET, Go, Ruby, Custom | Node.js, Python, Go, Java, .NET, Ruby, PHP | Any language (containers) | C#, JavaScript, Python, Java, PowerShell, TypeScript |
| **Max Timeout** | 15 minutes | 9 min (1st gen), 60 min (2nd gen) | 60 minutes | 10 min (Consumption), 230 min (Premium) |
| **Max Memory** | 10 GB | 8 GB (1st gen), 32 GB (2nd gen) | 32 GB | 1.5 GB (Consumption), 14 GB (Premium) |
| **Cold Start** | Yes (100ms-1s typical) | Yes (~500ms typical) | Yes (~1s typical) | Yes (varies by language) |
| **Warm Instances** | Provisioned Concurrency | Min instances | Min instances | Premium plan always warm |
| **Pricing Model** | Per request + duration | Per invocation + compute time | Per 100ms + requests + CPU/memory | Per execution + duration |
| **Free Tier** | 1M requests/month, 400K GB-seconds | 2M invocations/month | 2M requests/month, 360K GB-seconds | 1M requests/month |
| **Container Support** | Lambda Container Images | Cloud Run (separate service) | Native container support | Custom handlers |
| **Concurrency** | 1000 (default, can increase) | 1000 (configurable) | 1000 (configurable) | Dynamic (consumption plan) |
| **Event Sources** | 20+ AWS services | Cloud Storage, Pub/Sub, HTTP, Firestore | HTTP, Pub/Sub, Cloud Tasks, Eventarc | 100+ triggers (HTTP, Timer, Queue, Event Grid) |

**Documentation:**
- **[📖 AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)** - Complete Lambda guide
- **[📖 GCP Cloud Functions Documentation](https://cloud.google.com/functions/docs)** - Cloud Functions guide
- **[📖 GCP Cloud Run Documentation](https://cloud.google.com/run/docs)** - Cloud Run guide
- **[📖 Azure Functions Documentation](https://learn.microsoft.com/en-us/azure/azure-functions/)** - Complete Functions guide

---

## Platform-as-a-Service (PaaS)

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Service Name** | Elastic Beanstalk | App Engine | App Service |
| **Languages** | Java, .NET, Node.js, Python, Ruby, Go, PHP, Docker | Python, Java, Node.js, Go, Ruby, PHP (Standard); Any (Flexible) | .NET, Java, Node.js, Python, PHP, Ruby |
| **Environments** | Web Server, Worker | Standard (sandboxed), Flexible (containers) | Windows, Linux, Containers |
| **Auto-scaling** | Yes | Automatic (Standard), Manual (Flexible) | Built-in auto-scale |
| **Deployment** | ZIP, Docker, Git | gcloud, Git, Docker | Git, ZIP, Docker, FTP |
| **Deployment Slots** | Environment cloning | Versions + Traffic Splitting | Deployment slots (Standard tier+) |
| **Custom Domains** | Yes | Yes | Yes |
| **SSL/TLS** | AWS Certificate Manager | Managed SSL certificates | Managed certificates, custom |
| **VNet Integration** | VPC | VPC Connector (Flexible) | VNet integration |
| **Pricing** | EC2 + ALB + other resources | Instance hours | App Service Plan (Basic, Standard, Premium) |

**Documentation:**
- **[📖 AWS Elastic Beanstalk Documentation](https://docs.aws.amazon.com/elasticbeanstalk/)** - Beanstalk guide
- **[📖 GCP App Engine Documentation](https://cloud.google.com/appengine/docs)** - App Engine guide
- **[📖 Azure App Service Documentation](https://learn.microsoft.com/en-us/azure/app-service/)** - App Service guide

---

## Container Services

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Container Registry** | ECR (Elastic Container Registry) | Artifact Registry, Container Registry | ACR (Azure Container Registry) |
| **Container Orchestration** | ECS (Elastic Container Service), EKS | GKE, Cloud Run | AKS, Container Instances, Container Apps |
| **Serverless Containers** | Fargate (ECS/EKS) | Cloud Run, GKE Autopilot | Azure Container Instances, Container Apps |
| **Batch Processing** | AWS Batch | Cloud Run Jobs, GKE Batch | Azure Batch, Container Instances |

**Comparison: Managed Container Orchestration (Non-Kubernetes)**

| Feature | AWS ECS | GCP Cloud Run | Azure Container Instances | Azure Container Apps |
|---------|---------|---------------|------------------------|---------------------|
| **Orchestration** | AWS proprietary | Fully managed | Single containers | Microservices platform |
| **Pricing** | Pay for EC2/Fargate | Pay per 100ms | Pay per second | Pay per usage |
| **Scaling** | Task-based | Request-based | Manual | Event-driven, KEDA |
| **Load Balancing** | ALB, NLB | Built-in | Manual setup | Built-in |
| **Networking** | VPC native | VPC Connector | VNet integration | VNet integration |

**Documentation:**
- **[📖 AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)** - ECS guide
- **[📖 AWS EKS Documentation](https://docs.aws.amazon.com/eks/)** - EKS guide
- **[📖 AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)** - Container registry
- **[📖 GCP Cloud Run Documentation](https://cloud.google.com/run/docs)** - Cloud Run guide
- **[📖 GCP GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)** - GKE guide
- **[📖 Azure Container Instances Documentation](https://learn.microsoft.com/en-us/azure/container-instances/)** - ACI guide
- **[📖 Azure Container Apps Documentation](https://learn.microsoft.com/en-us/azure/container-apps/)** - Container Apps guide

---

## Batch & HPC

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Batch Processing** | AWS Batch | Cloud Run Jobs, Dataflow | Azure Batch |
| **HPC** | ParallelCluster, Batch | Google Cloud HPC Toolkit | CycleCloud, HPC Pack |
| **Job Scheduling** | AWS Batch, Step Functions | Cloud Scheduler, Workflows | Azure Batch, Logic Apps |
| **Spot/Preemptible** | Spot Instances | Spot VMs, Preemptible VMs | Spot VMs |

**Documentation:**
- **[📖 AWS Batch Documentation](https://docs.aws.amazon.com/batch/)** - Batch processing
- **[📖 GCP Cloud Run Jobs Documentation](https://cloud.google.com/run/docs/create-jobs)** - Batch jobs
- **[📖 Azure Batch Documentation](https://learn.microsoft.com/en-us/azure/batch/)** - Batch service

---

## Decision Tree: Which Compute Service?

### When to Use Virtual Machines
- ✅ Need full OS control
- ✅ Legacy applications requiring specific OS configurations
- ✅ Long-running, persistent workloads
- ✅ Licensing requirements (BYOL)
- ❌ Don't want to manage OS patches and updates

### When to Use Kubernetes
- ✅ Microservices architecture
- ✅ Need container orchestration
- ✅ Multi-cloud portability requirements
- ✅ Complex deployment patterns (canary, blue-green)
- ❌ Small, simple applications (overhead too high)

### When to Use Serverless Functions
- ✅ Event-driven workloads
- ✅ Short-running tasks (< 15 minutes)
- ✅ Variable/unpredictable traffic
- ✅ Want zero server management
- ❌ Long-running processes
- ❌ Need persistent connections

### When to Use PaaS
- ✅ Web applications
- ✅ Want minimal infrastructure management
- ✅ Standard language runtime
- ✅ Built-in scaling and load balancing
- ❌ Need custom OS or kernel modules

### When to Use Managed Containers (ECS/Cloud Run/Container Apps)
- ✅ Containerized applications
- ✅ Don't need full Kubernetes complexity
- ✅ Want managed service with less overhead than K8s
- ✅ Simpler deployment models

---

## Cost Comparison (Approximate)

**Example: 2 vCPU, 8 GB RAM, US East/Central region**

| Provider | On-Demand | Reserved/Committed (1 year) | Spot/Preemptible |
|----------|-----------|---------------------------|------------------|
| **AWS** (t3.large) | ~$67/month | ~$40/month (40% savings) | ~$20/month (70% savings) |
| **GCP** (e2-standard-2) | ~$60/month | ~$39/month (35% savings) | ~$18/month (70% savings) |
| **Azure** (D2s v3) | ~$70/month | ~$41/month (41% savings) | ~$21/month (70% savings) |

*Note: Prices vary by region and are subject to change. Always use official pricing calculators.*

**Pricing Calculators:**
- **[📖 AWS Pricing Calculator](https://calculator.aws/)** - AWS cost estimates
- **[📖 GCP Pricing Calculator](https://cloud.google.com/products/calculator)** - GCP cost estimates
- **[📖 Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)** - Azure cost estimates

---

## CLI Command Comparison

### Create a Virtual Machine

**AWS:**
```bash
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-key \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx
```

**GCP:**
```bash
gcloud compute instances create my-instance \
  --machine-type=e2-micro \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --zone=us-central1-a
```

**Azure:**
```bash
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image UbuntuLTS \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys
```

### Create a Kubernetes Cluster

**AWS:**
```bash
eksctl create cluster \
  --name my-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3
```

**GCP:**
```bash
gcloud container clusters create my-cluster \
  --zone us-central1-a \
  --machine-type e2-medium \
  --num-nodes 3
```

**Azure:**
```bash
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --node-vm-size Standard_DS2_v2 \
  --enable-addons monitoring
```

---

## Key Takeaways

### AWS Strengths
- ✅ Most mature and comprehensive service catalog
- ✅ Deepest feature set for EC2 and Lambda
- ✅ Best for enterprise-scale deployments
- ✅ Extensive third-party tool ecosystem

### GCP Strengths
- ✅ Best Kubernetes service (GKE)
- ✅ Live migration for VMs (no downtime updates)
- ✅ Superior networking performance
- ✅ Simplified pricing model
- ✅ Strong in data analytics and ML

### Azure Strengths
- ✅ Best Windows/Microsoft stack integration
- ✅ Hybrid cloud focus (Azure Arc, Azure Stack)
- ✅ Enterprise Active Directory integration
- ✅ Strong in enterprise scenarios
- ✅ Container Apps (best serverless container platform)

---

**Related Guides:**
- [Storage Service Comparison](./service-comparison-storage.md)
- [Database Service Comparison](https://data.noblerworks.com/resources/service-comparison-databases/)
- [Networking Service Comparison](./service-comparison-networking.md)
- [Serverless Service Comparison](./service-comparison-serverless.md)
