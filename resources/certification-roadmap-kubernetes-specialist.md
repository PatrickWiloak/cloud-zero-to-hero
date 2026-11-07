---
last-updated: 2026-05-03
difficulty: intermediate
---

# Certification Roadmap - Kubernetes Specialist

## Overview

This roadmap guides you through Kubernetes and container-focused certifications, from foundational knowledge through advanced cloud-specific Kubernetes expertise. Kubernetes skills are among the most in-demand for cloud engineers, DevOps professionals, and platform engineers.

---

## Recommended Certification Path

### Phase 1 - Foundation (Months 1-3)

| Certification | Provider | Level | Exam Format |
|--------------|----------|-------|-------------|
| KCNA (Kubernetes and Cloud Native Associate) | CNCF/Linux Foundation | Foundational | Multiple choice |
| Docker Certified Associate (DCA) | Mirantis | Associate | Multiple choice |

**Focus Areas:**
- Container fundamentals (images, containers, registries)
- Dockerfile best practices and multi-stage builds
- Kubernetes architecture (control plane, worker nodes)
- Core objects (Pods, Deployments, Services, ConfigMaps, Secrets)
- kubectl basics and YAML manifests
- Container networking and storage fundamentals

### Phase 2 - Kubernetes Core (Months 3-8)

| Certification | Provider | Level | Exam Format |
|--------------|----------|-------|-------------|
| CKA (Certified Kubernetes Administrator) | CNCF/Linux Foundation | Professional | Performance-based (hands-on) |
| CKAD (Certified Kubernetes Application Developer) | CNCF/Linux Foundation | Professional | Performance-based (hands-on) |

**Focus Areas:**

**CKA Topics:**
- Cluster installation and configuration (kubeadm)
- Cluster upgrades and maintenance
- etcd backup and restore
- Networking (CNI, Services, Ingress, DNS, NetworkPolicies)
- Storage (PV, PVC, StorageClasses, CSI)
- Scheduling (taints, tolerations, affinity, nodeSelector)
- Security (RBAC, ServiceAccounts, SecurityContext)
- Troubleshooting (logs, events, cluster components)
- Monitoring and logging basics

**CKAD Topics:**
- Pod design patterns (multi-container, init, sidecar)
- Configuration (ConfigMaps, Secrets, environment variables)
- Observability (readiness, liveness, startup probes)
- Services and networking
- Jobs and CronJobs
- Deployments, rolling updates, rollbacks
- Helm chart basics
- Resource limits and requests
- Custom Resource Definitions (CRDs)

### Phase 3 - Security (Months 8-11)

| Certification | Provider | Level | Exam Format |
|--------------|----------|-------|-------------|
| CKS (Certified Kubernetes Security Specialist) | CNCF/Linux Foundation | Specialist | Performance-based (hands-on) |

**Focus Areas:**
- Cluster hardening (CIS benchmarks, kube-bench)
- Supply chain security (image scanning, admission control)
- Runtime security (Falco, seccomp, AppArmor)
- Network policies and pod-to-pod encryption
- Secrets management (sealed secrets, external secrets)
- Audit logging and monitoring
- OPA Gatekeeper and policy enforcement
- Pod Security Standards (restricted, baseline, privileged)
- mTLS with service mesh

### Phase 4 - Cloud-Specific Kubernetes (Months 11-18)

| Certification | Provider | Level | Exam Code |
|--------------|----------|-------|-----------|
| AWS Solutions Architect Associate | AWS | Associate | SAA-C03 |
| Azure Kubernetes Service Specialty | Microsoft | Specialty | AZ-1005 |
| Google Cloud Professional Cloud Architect | Google | Professional | PCA |

**Focus Areas:**
- EKS architecture, networking (VPC CNI), and IAM integration
- AKS networking (kubenet vs Azure CNI), Entra ID integration
- GKE Autopilot vs Standard, Workload Identity
- Managed node groups, auto-scaling, spot instances
- Cloud-native load balancing and ingress controllers
- Container registry integration (ECR, ACR, Artifact Registry)
- Cloud-specific monitoring and logging integration

---

## Core Knowledge Areas

### Kubernetes Architecture

| Component | Purpose | Key Concepts |
|-----------|---------|-------------|
| API Server | Central management hub | RESTful API, authentication, admission control |
| etcd | Cluster state store | Distributed key-value, backup/restore |
| Scheduler | Pod placement | Resource requests, affinity, taints/tolerations |
| Controller Manager | Desired state reconciliation | Deployment, ReplicaSet, Node controllers |
| kubelet | Node agent | Pod lifecycle, container runtime |
| kube-proxy | Network proxy | Services, iptables/IPVS |
| CoreDNS | Cluster DNS | Service discovery, DNS policies |
| CNI | Container networking | Pod networking, network policies |
| CSI | Container storage | Persistent volumes, dynamic provisioning |

### Workload Types

| Resource | Use Case | Key Features |
|----------|----------|-------------|
| Deployment | Stateless applications | Rolling updates, rollbacks, replicas |
| StatefulSet | Stateful applications | Stable network IDs, ordered deployment, persistent storage |
| DaemonSet | Node-level services | Logging, monitoring agents |
| Job | Batch processing | Run-to-completion, parallelism |
| CronJob | Scheduled tasks | Cron schedule, concurrency policy |
| ReplicaSet | Pod replication | Selector-based (managed by Deployment) |

### Networking Deep Dive

| Concept | Description | Implementation |
|---------|-------------|----------------|
| Pod Networking | Every pod gets unique IP | CNI plugins (Calico, Cilium, Flannel) |
| Service Types | ClusterIP, NodePort, LoadBalancer, ExternalName | kube-proxy (iptables/IPVS) |
| Ingress | HTTP/HTTPS routing | NGINX, Traefik, cloud LB controllers |
| Network Policies | Pod-level firewall rules | CNI-dependent (Calico, Cilium) |
| Service Mesh | Advanced traffic management | Istio, Linkerd, Consul Connect |
| DNS | Service discovery | CoreDNS, headless services |

---

## Cloud-Managed Kubernetes

### EKS vs AKS vs GKE

| Feature | AWS EKS | Azure AKS | Google GKE |
|---------|---------|-----------|------------|
| Control Plane Cost | $0.10/hr | Free | Free (Standard) |
| Managed Nodes | Managed node groups, Fargate | System/User node pools | Autopilot, Standard |
| Networking | VPC CNI | Azure CNI / kubenet | Dataplane V2 (Cilium) |
| Identity | IRSA, Pod Identity | Workload Identity (Entra) | Workload Identity |
| Scaling | Karpenter, Cluster Autoscaler | KEDA, Cluster Autoscaler | Autopilot, Node Auto-provisioning |
| Service Mesh | Istio (App Mesh retired 2026-09-30) | Istio add-on | Anthos Service Mesh |
| GitOps | Flux add-on | Flux (Arc) | Config Sync |
| Policy | OPA Gatekeeper | Azure Policy | Policy Controller |

---

## Exam Preparation

### CKA/CKAD/CKS Exam Tips

| Tip | Details |
|-----|---------|
| Practice in terminal | Exams are hands-on - no multiple choice |
| Know kubectl shortcuts | `kubectl run`, `kubectl create`, `--dry-run=client -o yaml` |
| Bookmark docs | kubernetes.io/docs is allowed during exam |
| Time management | 15-20 tasks in 2 hours - budget 6-7 minutes per task |
| Use aliases | `alias k=kubectl`, `export do="--dry-run=client -o yaml"` |
| Practice under pressure | Use simulators (killer.sh - included with exam registration) |
| YAML generation | Use `kubectl create` and `kubectl run` to generate YAML templates |
| Context switching | Always check and switch kubectl context per question |

### Essential kubectl Commands

| Task | Command |
|------|---------|
| Create deployment | `kubectl create deployment nginx --image=nginx --replicas=3` |
| Expose service | `kubectl expose deployment nginx --port=80 --type=ClusterIP` |
| Generate YAML | `kubectl run nginx --image=nginx --dry-run=client -o yaml` |
| Debug pod | `kubectl logs pod-name`, `kubectl describe pod pod-name` |
| Execute in pod | `kubectl exec -it pod-name -- /bin/sh` |
| Scale | `kubectl scale deployment nginx --replicas=5` |
| Rollback | `kubectl rollout undo deployment nginx` |
| Get all resources | `kubectl get all -n namespace` |
| Apply manifest | `kubectl apply -f manifest.yaml` |
| Delete resource | `kubectl delete -f manifest.yaml` |

---

## Study Resources

### CNCF Certifications

| Resource | Type | Link |
|----------|------|------|
| Kubernetes Documentation | Official docs | https://kubernetes.io/docs/ |
| Kubernetes the Hard Way | Tutorial | https://github.com/kelseyhightower/kubernetes-the-hard-way |
| CKA Curriculum | Exam guide | https://github.com/cncf/curriculum |
| killer.sh | Practice exam | https://killer.sh/ (included with exam) |
| KodeKloud | Interactive labs | https://kodekloud.com/ |

### Cloud-Specific

| Resource | Type | Link |
|----------|------|------|
| EKS Best Practices Guide | Documentation | https://aws.github.io/aws-eks-best-practices/ |
| EKS Workshop | Workshop | https://www.eksworkshop.com/ |
| AKS Documentation | Documentation | https://learn.microsoft.com/en-us/azure/aks/ |
| GKE Documentation | Documentation | https://cloud.google.com/kubernetes-engine/docs |
| GKE Best Practices | Documentation | https://cloud.google.com/kubernetes-engine/docs/best-practices |

---

## Hands-On Practice Labs

| Lab | Certification | Skills |
|-----|---------------|--------|
| Deploy multi-tier app on bare Kubernetes | CKA | Cluster setup, services, networking |
| Implement NetworkPolicies to isolate namespaces | CKA/CKS | Network security |
| Set up Ingress with TLS termination | CKA/CKAD | Ingress, certificates |
| Deploy StatefulSet with persistent storage | CKA/CKAD | Storage, StatefulSets |
| Configure RBAC for multi-team cluster | CKA/CKS | Security, RBAC |
| etcd backup and restore | CKA | Disaster recovery |
| Implement pod security standards | CKS | Security policies |
| Deploy Helm chart and customize values | CKAD | Helm, packaging |
| Set up horizontal pod autoscaler | CKAD | Scaling, metrics |
| Image scanning with Trivy and admission control | CKS | Supply chain security |
| Deploy EKS cluster with Karpenter | EKS | Cloud-specific K8s |
| AKS with Azure CNI and Workload Identity | AKS | Cloud-specific K8s |
| GKE Autopilot with Config Sync | GKE | Cloud-specific K8s |

---

## Study Schedule (24 Weeks)

| Weeks | Focus | Certification Target |
|-------|-------|---------------------|
| 1-3 | Docker/container fundamentals, Kubernetes basics | KCNA |
| 4-6 | Core K8s objects, kubectl mastery, YAML | KCNA exam |
| 7-10 | Cluster admin - networking, storage, scheduling | CKA prep |
| 11-12 | CKA practice exams (killer.sh), troubleshooting | CKA exam |
| 13-15 | Application design patterns, Helm, probes | CKAD prep |
| 16-17 | CKAD practice exams, time management | CKAD exam |
| 18-20 | Kubernetes security, policy engines, runtime security | CKS prep |
| 21-22 | CKS practice exams, hardening exercises | CKS exam |
| 23-24 | Cloud-specific K8s (EKS/AKS/GKE), integration | Cloud cert prep |

---

## Key Exam Tips

1. **CKA/CKAD/CKS are hands-on** - you must be fast and accurate with kubectl and YAML
2. Master imperative commands (`kubectl create`, `kubectl run`) for speed - generate YAML rather than writing from scratch
3. Practice with killer.sh (2 free sessions included with exam registration)
4. Know the Kubernetes docs site structure - you can use it during the exam
5. For CKS, understand the full supply chain from image build to runtime
6. Cloud-specific exams focus on managed service integration rather than raw Kubernetes
7. Set up aliases and environment variables at the start of each exam session
8. Always verify your work after each task before moving on
