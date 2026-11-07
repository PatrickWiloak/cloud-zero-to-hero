---
last-updated: 2026-05-03
difficulty: intermediate
---

# Service Comparison - Containers and Kubernetes

## Overview

This guide compares container orchestration, managed Kubernetes, container registries, and serverless container services across AWS, Azure, and Google Cloud. Understanding the differences helps you select the right platform for your workload and prepare for multi-cloud certification exams.

---

## Managed Kubernetes Services

### EKS vs AKS vs GKE - Quick Comparison

| Feature | AWS EKS | Azure AKS | Google GKE |
|---------|---------|-----------|------------|
| Control Plane Cost | $0.10/hr per cluster | Free | Free (Standard), $0.10/hr (Autopilot) |
| Max Nodes per Cluster | 5,000 | 5,000 | 15,000 |
| Max Pods per Node | 110 (default) | 250 | 110 (default) |
| Kubernetes Version Support | N-3 minor versions | N-3 minor versions | N-3 minor versions |
| Auto-Upgrade | Optional | Optional (default on) | Optional (default on) |
| Managed Node Groups | Yes (Managed, Fargate) | Yes (System/User pools) | Yes (Autopilot, Standard) |
| GPU Support | Yes | Yes | Yes |
| ARM Support | Graviton instances | Ampere Altra | Tau T2A |
| SLA | 99.95% (uptime) | 99.95% (with AZs) | 99.95% (regional) |

### Control Plane Details

| Aspect | AWS EKS | Azure AKS | Google GKE |
|--------|---------|-----------|------------|
| API Server Access | Public/Private endpoint | Public/Private/Authorized IPs | Public/Private/Authorized networks |
| etcd Management | Fully managed | Fully managed | Fully managed |
| Control Plane Logging | CloudWatch integration | Azure Monitor | Cloud Logging |
| Multi-AZ Control Plane | Default (3 AZs) | Default | Default (regional cluster) |
| Maintenance Windows | Configurable | Configurable (planned maintenance) | Configurable (maintenance windows) |

### Networking Models

| Feature | AWS EKS | Azure AKS | Google GKE |
|---------|---------|-----------|------------|
| Default CNI | Amazon VPC CNI | Azure CNI / kubenet | GKE CNI (Dataplane V2) |
| Network Policy | Calico (add-on) | Azure NPM / Calico | Native (Dataplane V2) |
| Service Mesh | ECS Service Connect / Istio | Istio-based (add-on) | Anthos Service Mesh |
| Load Balancer | AWS ALB/NLB | Azure LB / App Gateway | Cloud Load Balancing |
| Ingress Controller | AWS LB Controller | AGIC / NGINX | GKE Ingress Controller |
| IPv6 Support | Dual-stack | Dual-stack | Dual-stack |
| Pod IP Management | VPC secondary CIDRs | Subnet allocation | Alias IP ranges |

### Security Features

| Feature | AWS EKS | Azure AKS | Google GKE |
|---------|---------|-----------|------------|
| RBAC | Native K8s + IAM | Native K8s + Azure AD | Native K8s + IAM |
| Pod Identity | EKS Pod Identity / IRSA | Workload Identity (Azure AD) | Workload Identity |
| Secrets Management | AWS Secrets Manager CSI | Azure Key Vault CSI | Secret Manager CSI |
| Image Scanning | ECR scanning | Defender for Containers | Artifact Analysis |
| Admission Control | OPA Gatekeeper | Azure Policy / OPA | Policy Controller |
| Encryption at Rest | KMS envelope encryption | Azure Key Vault | Cloud KMS |
| Node Security | Bottlerocket OS option | Ubuntu / Azure Linux | Container-Optimized OS / Ubuntu |

### Cluster Add-ons and Ecosystem

| Feature | AWS EKS | Azure AKS | Google GKE |
|---------|---------|-----------|------------|
| Service Mesh | ECS Service Connect, Istio | Istio add-on | Anthos Service Mesh |
| GitOps | Flux (EKS add-on) | Flux (GitOps extension) | Config Sync |
| Monitoring | Container Insights | Container Insights (Azure Monitor) | GKE Dashboard / Cloud Monitoring |
| Cost Management | Kubecost integration | AKS Cost Analysis | GKE Cost Allocation |
| Backup | Velero + EBS snapshots | AKS Backup (Azure Backup) | Backup for GKE |

---

## Container Registries

### ECR vs ACR vs Artifact Registry

| Feature | AWS ECR | Azure ACR | Google Artifact Registry |
|---------|---------|-----------|--------------------------|
| Image Formats | Docker, OCI | Docker, OCI, Helm | Docker, OCI, language packages |
| Geo-Replication | Cross-region replication | Geo-replication (Premium) | Multi-region repositories |
| Vulnerability Scanning | Basic + Enhanced (Inspector) | Defender for Containers | Artifact Analysis (on-demand/auto) |
| Image Signing | Notation/cosign support | Notation (Azure trust policy) | Binary Authorization |
| Lifecycle Policies | Yes (tag/age rules) | Retention policies | Cleanup policies |
| Private Endpoints | VPC endpoints | Private Link | Private Service Connect |
| Pull-through Cache | Yes (public registries) | Limited | Remote repositories |
| Pricing Model | Per GB storage + transfer | Per GB (Basic/Standard/Premium tiers) | Per GB storage + egress |
| Immutable Tags | Yes | Yes | Yes |
| RBAC | IAM policies | Azure RBAC / ACR roles | IAM policies |

### Registry Authentication

| Method | AWS ECR | Azure ACR | Google Artifact Registry |
|--------|---------|-----------|--------------------------|
| Token Auth | `aws ecr get-login-password` | `az acr login` | `gcloud auth configure-docker` |
| Service Account | IAM role (IRSA/Pod Identity) | Managed Identity | Workload Identity |
| Credential Helper | amazon-ecr-credential-helper | acr-credential-helper | gcloud credential helper |
| Token Expiry | 12 hours | 3 hours | 1 hour (configurable) |

---

## Serverless Container Services

### ECS vs ACI vs Cloud Run

| Feature | AWS ECS (Fargate) | Azure Container Instances | Google Cloud Run |
|---------|-------------------|---------------------------|------------------|
| Orchestration Model | Task definitions + services | Container groups | Knative-based services |
| Scaling | Service Auto Scaling | Manual / KEDA | Automatic (0 to N) |
| Scale to Zero | No (min 1 task) | Yes (stop/start) | Yes |
| Max vCPU per Instance | 16 vCPU | 4 vCPU per container | 8 vCPU |
| Max Memory per Instance | 120 GB | 16 GB per container | 32 GB |
| GPU Support | No (use EC2 launch type) | Yes (limited regions) | Yes |
| Startup Time | 30-60 seconds | 15-30 seconds | <1 second (warm) |
| Persistent Storage | EFS integration | Azure Files | Cloud Storage FUSE / NFS |
| VPC Integration | Native VPC | VNet injection | Direct VPC egress |
| Custom Domains | Via ALB | Via Application Gateway | Native mapping |
| Concurrency Control | 1 container = 1 request (default) | N/A | 1-1000 per instance |
| Pricing | Per vCPU-second + GB-second | Per vCPU-second + GB-second | Per vCPU-second + GB-second + requests |

### ECS vs EKS Decision Matrix

| Criteria | Choose ECS | Choose EKS |
|----------|------------|------------|
| Team Experience | Docker familiarity | Kubernetes expertise |
| Portability | AWS-specific | Multi-cloud/hybrid |
| Complexity | Simpler operations | Full K8s ecosystem |
| Compliance | AWS-native controls | K8s policy engines |
| Windows Containers | Supported | Supported |
| Batch Workloads | ECS tasks | K8s Jobs/CronJobs |
| Service Mesh | ECS Service Connect | Istio / Linkerd |

### Serverless Container Comparison - Extended

| Feature | AWS Fargate | Azure Container Apps | Google Cloud Run |
|---------|-------------|----------------------|------------------|
| Base Technology | Proprietary | Kubernetes/Envoy/DAPR | Knative |
| Revision Management | Task definition revisions | Revision-based | Revision-based |
| Traffic Splitting | Via ALB weighted routing | Built-in | Built-in |
| Built-in Auth | No (use ALB + Cognito) | Built-in (Easy Auth) | Built-in (IAM) |
| Dapr Integration | No | Native | No |
| Jobs Support | Standalone tasks | Jobs (preview) | Cloud Run Jobs |
| Multi-container | Sidecar support | Sidecar support | Sidecar support |
| Observability | CloudWatch + X-Ray | Azure Monitor + App Insights | Cloud Trace + Cloud Logging |

---

## Container Networking Comparison

| Feature | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Service Discovery | Cloud Map / ECS Service Discovery | Azure DNS / AKS CoreDNS | Cloud DNS / GKE CoreDNS |
| Internal Load Balancing | Internal ALB/NLB | Internal LB | Internal TCP/UDP LB |
| External Load Balancing | ALB/NLB | Azure LB / App Gateway | Global/Regional LB |
| Network Policies | Security groups + Calico | NSG + Azure NPM / Calico | VPC firewall + Dataplane V2 |
| Service Mesh | ECS Service Connect / Istio | Open Service Mesh / Istio | Anthos Service Mesh |

---

## CI/CD Integration for Containers

| Feature | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Build Service | CodeBuild | Azure Pipelines / ACR Tasks | Cloud Build |
| Deploy Service | CodeDeploy / ECS deploy | Azure Pipelines / AKS | Cloud Deploy |
| Image Build | CodeBuild + Dockerfile | ACR Tasks (quick builds) | Cloud Build |
| GitOps | Flux (EKS add-on) | Flux (Arc extension) | Config Sync |
| Canary/Blue-Green | CodeDeploy | Flagger / Argo Rollouts | Cloud Deploy |
| Pipeline as Code | buildspec.yml | azure-pipelines.yml | cloudbuild.yaml |

---

## Monitoring and Observability

| Feature | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Metrics | CloudWatch Container Insights | Azure Monitor / Prometheus | Cloud Monitoring / Managed Prometheus |
| Logging | CloudWatch Logs (Fluent Bit) | Azure Monitor Logs | Cloud Logging (Fluent Bit) |
| Tracing | AWS X-Ray | Application Insights | Cloud Trace |
| Dashboards | CloudWatch Dashboards | Azure Dashboards / Grafana | Cloud Monitoring / Grafana |
| Alerting | CloudWatch Alarms + SNS | Azure Monitor Alerts | Cloud Alerting |
| Managed Prometheus | Amazon Managed Prometheus | Azure Monitor (Prometheus) | Google Managed Prometheus |
| Managed Grafana | Amazon Managed Grafana | Azure Managed Grafana | N/A (self-hosted or Cloud Monitoring) |

---

## Cost Comparison (Approximate)

### Managed Kubernetes - Monthly Cost Estimate (Small Cluster)

| Component | AWS EKS | Azure AKS | Google GKE |
|-----------|---------|-----------|------------|
| Control Plane | ~$73/month | Free | Free (Standard) |
| 3x Worker Nodes (4 vCPU, 16 GB) | ~$300/month (m6i.xlarge) | ~$280/month (D4s_v5) | ~$270/month (e2-standard-4) |
| Load Balancer | ~$20/month (ALB) | ~$20/month (Standard LB) | ~$20/month (regional LB) |
| NAT Gateway | ~$45/month | ~$45/month | ~$45/month (Cloud NAT) |

### Cost Optimization Strategies

| Strategy | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Spot/Preemptible Nodes | Spot Instances (up to 90% off) | Spot VMs (up to 90% off) | Spot VMs (up to 91% off) |
| Reserved Capacity | Savings Plans / RIs | Reservations | CUDs |
| Right-sizing | Kubecost + Compute Optimizer | AKS Cost Analysis | GKE Cost Allocation |
| Cluster Autoscaler | Karpenter / Cluster Autoscaler | AKS Cluster Autoscaler | GKE Autopilot / Node Auto-provisioning |
| Scale to Zero | Fargate + scheduled scaling | KEDA | Cloud Run / GKE Autopilot |

---

## Certification Exam Focus Areas

### AWS Certifications
- EKS architecture and networking (VPC CNI, Pod Identity)
- ECS task definitions, service auto scaling
- Fargate vs EC2 launch types
- ECR lifecycle policies and cross-region replication

### Azure Certifications
- AKS networking models (kubenet vs Azure CNI)
- ACI use cases and limitations
- ACR tiers and geo-replication
- Azure Container Apps vs AKS decision criteria

### Google Cloud Certifications
- GKE Autopilot vs Standard mode
- Cloud Run concurrency model and cold starts
- Artifact Registry multi-format support
- Binary Authorization and supply chain security

---

## Documentation Links

- AWS EKS: https://docs.aws.amazon.com/eks/latest/userguide/
- AWS ECS: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html
- AWS ECR: https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html
- Azure AKS: https://learn.microsoft.com/en-us/azure/aks/
- Azure ACI: https://learn.microsoft.com/en-us/azure/container-instances/
- Azure ACR: https://learn.microsoft.com/en-us/azure/container-registry/
- Google GKE: https://cloud.google.com/kubernetes-engine/docs
- Google Cloud Run: https://cloud.google.com/run/docs
- Google Artifact Registry: https://cloud.google.com/artifact-registry/docs

---

## Key Takeaways

1. **GKE** is often considered the most mature managed Kubernetes offering with features like Autopilot and native network policies
2. **AKS** provides the best value with a free control plane and deep Azure AD integration
3. **EKS** offers the tightest AWS ecosystem integration but charges for the control plane
4. **Cloud Run** leads in serverless containers with true scale-to-zero and sub-second cold starts
5. **ECS** remains the simplest option for AWS-only container workloads
6. All three providers now support Kubernetes 1.28+ with similar feature parity
7. Container registry capabilities are converging - focus on scanning, signing, and lifecycle management for exams

---

**Related Guides:**
- [Compute Service Comparison](./service-comparison-compute.md)
- [Serverless Service Comparison](./service-comparison-serverless.md)
- [DevOps and CI/CD Comparison](./service-comparison-devops-cicd.md)
- [Observability and Monitoring Comparison](./service-comparison-observability-monitoring.md)
- [Topic: Kubernetes](../topics/kubernetes.md)
