# Amazon EKS (Elastic Kubernetes Service)

## Service Overview and Purpose

Amazon Elastic Kubernetes Service (EKS) is a fully managed Kubernetes service that makes it easy to run Kubernetes on AWS without needing to install and operate your own Kubernetes control plane. EKS automatically manages the availability and scalability of the Kubernetes control plane nodes responsible for scheduling containers, managing application availability, storing cluster data, and other key tasks.

**Core Purpose:**
- Provide a managed Kubernetes control plane
- Enable container orchestration at enterprise scale
- Integrate Kubernetes with AWS services
- Simplify Kubernetes cluster management and operations
- Support hybrid and multi-cloud deployments

## Key Features and Capabilities

### Core Features
- **Managed Control Plane**: Fully managed Kubernetes masters
- **High Availability**: Multi-AZ control plane deployment
- **Security**: Integration with AWS IAM and VPC
- **Networking**: VPC-native networking with AWS CNI
- **Scaling**: Horizontal Pod Autoscaler and Cluster Autoscaler
- **Monitoring**: Integration with CloudWatch Container Insights
- **Service Mesh**: AWS App Mesh integration ended (end of support 2026-09-30); use an open-source mesh such as Istio or Linkerd (see [Service mesh explained](../../../../../learn/concepts/service-mesh-explained.md))
- **GitOps**: Integration with AWS CodeCommit and third-party tools
- **Fargate Support**: Serverless compute for pods
- **Windows Support**: Windows container workloads

### Kubernetes Version Support
- **Current Versions**: 1.24, 1.25, 1.26, 1.27, 1.28
- **Automatic Updates**: Managed control plane updates
- **Extended Support**: Available for specific versions
- **Add-ons**: Managed add-ons for core components

### Node Group Types

#### Managed Node Groups
- **EC2 Instances**: Self-managed EC2 instances
- **Auto Scaling**: Automatic scaling based on demand
- **Instance Types**: Support for various instance families
- **Spot Instances**: Cost optimization with Spot instances
- **Custom AMIs**: Support for custom Amazon Linux AMIs

#### Fargate
- **Serverless**: No node management required
- **Pod-level Isolation**: Each pod runs in its own compute environment
- **Automatic Scaling**: Scales based on pod requirements
- **Security**: Enhanced security isolation

#### Self-Managed Nodes
- **Full Control**: Complete control over node configuration
- **Custom Requirements**: Special hardware or software needs
- **Existing Infrastructure**: Use existing EC2 instances

## Use Cases and Scenarios

### Primary Use Cases

1. **Microservices Architecture**
   - Container orchestration at scale
   - Service mesh integration
   - Inter-service communication
   - API gateway patterns

2. **CI/CD and DevOps**
   - GitOps workflows
   - Blue/green deployments
   - Canary releases
   - Development environments

3. **Machine Learning Workloads**
   - Distributed training
   - Model serving
   - GPU-accelerated workloads
   - Jupyter notebook environments

4. **Data Processing**
   - Batch processing jobs
   - Stream processing
   - ETL pipelines
   - Apache Spark workloads

5. **Enterprise Applications**
   - Legacy application modernization
   - Multi-tenant applications
   - High-availability systems
   - Compliance requirements

### Detailed Scenarios

#### E-commerce Platform
```
Frontend (React/Angular) → API Gateway → Microservices (Node.js/Java)
                                     ↓
                              Databases (RDS/DynamoDB)
                                     ↓
                              Background Jobs (Queues/Workers)
```

#### ML Training Pipeline
```
Data Ingestion → Data Processing → Model Training → Model Validation → Model Deployment
      ↓                ↓              ↓              ↓              ↓
   S3 Buckets    →  Spark Jobs  →  GPU Nodes  →  Testing Pods →  Inference Service
```

#### GitOps Workflow
```
Git Repository → CI Pipeline → Container Registry → GitOps Operator → EKS Cluster
                     ↓              ↓                    ↓              ↓
                 Build Image  →  Push to ECR  →  Deploy Changes → Update Applications
```

## Pricing Models and Cost Optimization

### Pricing Components

#### Control Plane
- **EKS Cluster**: $0.10 per hour per cluster
- **24/7 Availability**: Includes high availability across multiple AZs
- **No Additional Charges**: For control plane resources

#### Compute Resources

1. **EC2 Instances** (Managed/Self-managed nodes)
   - Standard EC2 pricing
   - On-Demand, Reserved, or Spot instances
   - EBS storage costs

2. **Fargate**
   - Per-second billing for vCPU and memory
   - No infrastructure management overhead
   - Higher per-resource cost but no minimum charges

3. **Additional Services**
   - Load Balancers (ALB/NLB)
   - EBS volumes and snapshots
   - Data transfer costs
   - NAT Gateway charges

### Cost Optimization Strategies

1. **Right-size Workloads**
   - Use resource requests and limits
   - Implement Vertical Pod Autoscaler
   - Monitor resource utilization

2. **Efficient Scaling**
   - Horizontal Pod Autoscaler (HPA)
   - Cluster Autoscaler for nodes
   - KEDA for event-driven scaling

3. **Spot Instances**
   - Use Spot instances for fault-tolerant workloads
   - Mix On-Demand and Spot instances
   - Implement proper pod disruption budgets

4. **Fargate vs EC2 Decision**
   - Fargate: Variable, unpredictable workloads
   - EC2: Steady, long-running workloads
   - Consider workload patterns and resource efficiency

5. **Storage Optimization**
   - Use appropriate storage classes
   - Implement lifecycle policies
   - Optimize container images

## Configuration Details and Best Practices

### Cluster Configuration

#### Basic Cluster Creation
```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: production-cluster
  region: us-west-2
  version: "1.28"

vpc:
  enableDnsHostnames: true
  enableDnsSupport: true

managedNodeGroups:
  - name: worker-nodes
    instanceType: t3.medium
    desiredCapacity: 3
    minSize: 1
    maxSize: 10
    volumeSize: 20
    volumeType: gp3
    ssh:
      allow: true
      publicKeyName: my-key-pair

addons:
  - name: vpc-cni
  - name: coredns
  - name: kube-proxy
  - name: aws-ebs-csi-driver

iam:
  withOIDC: true
  serviceAccounts:
    - metadata:
        name: cluster-autoscaler
        namespace: kube-system
      wellKnownPolicies:
        autoScaler: true
```

#### Advanced Cluster Configuration
```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: advanced-cluster
  region: us-west-2
  version: "1.28"

vpc:
  id: vpc-12345678
  subnets:
    private:
      us-west-2a:
        id: subnet-12345
      us-west-2b:
        id: subnet-67890
    public:
      us-west-2a:
        id: subnet-abcde
      us-west-2b:
        id: subnet-fghij

managedNodeGroups:
  - name: general-purpose
    instanceTypes: ["t3.medium", "t3.large"]
    spot: true
    desiredCapacity: 3
    privateNetworking: true
    labels:
      role: worker
      environment: production
    taints:
      - key: workload-type
        value: general
        effect: NoSchedule

  - name: compute-optimized
    instanceTypes: ["c5.large", "c5.xlarge"]
    desiredCapacity: 2
    labels:
      role: compute
      node-type: cpu-intensive
    taints:
      - key: workload-type
        value: compute
        effect: NoSchedule

fargateProfiles:
  - name: serverless-workloads
    selectors:
      - namespace: fargate-ns
        labels:
          compute-type: serverless

logging:
  enable:
    - api
    - audit
    - authenticator
    - controllerManager
    - scheduler
  logRetentionInDays: 30

cloudWatch:
  clusterLogging:
    enableTypes: ["*"]
```

### Security Best Practices

#### RBAC Configuration
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: developer-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["get", "list", "create", "update", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "create", "update", "delete"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: developer-binding
subjects:
- kind: User
  name: developer-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: developer-role
  apiGroup: rbac.authorization.k8s.io
```

#### Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 8080
```

#### Pod Security Standards
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: secure-namespace
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Application Deployment Best Practices

#### Deployment with Resource Management
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      serviceAccountName: web-app-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: web-app
        image: my-app:v1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
      nodeSelector:
        node-type: general-purpose
      tolerations:
      - key: workload-type
        operator: Equal
        value: general
        effect: NoSchedule
```

#### Horizontal Pod Autoscaler
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
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

## Integration with Other AWS Services

### Core AWS Integrations

1. **Amazon VPC**
   - VPC-native networking
   - Security groups and NACLs
   - Private and public subnets
   - VPC endpoints for AWS services

2. **AWS IAM**
   - Service accounts for workloads
   - OIDC integration
   - Fine-grained permissions
   - Cross-account access

3. **Amazon ECR**
   - Container image registry
   - Vulnerability scanning
   - Image lifecycle policies
   - Private repositories

4. **AWS Load Balancer Controller**
   - Application Load Balancer integration
   - Network Load Balancer integration
   - Ingress controller
   - Service load balancing

5. **Amazon EBS CSI Driver**
   - Persistent volume storage
   - Dynamic provisioning
   - Volume snapshots
   - Encryption support

### Advanced Integrations

1. **AWS App Mesh (retired)**
   - End of support 2026-09-30; do not start new work on it
   - Kept only as history: it taught sidecar-proxy meshes (traffic management, observability)
   - Security policies

2. **Amazon CloudWatch**
   - Container Insights
   - Custom metrics
   - Log aggregation
   - Alerting and dashboards

3. **AWS X-Ray**
   - Distributed tracing
   - Performance analysis
   - Service map visualization
   - Error analysis

4. **Amazon RDS/DynamoDB**
   - Database connectivity
   - Service discovery
   - Connection pooling
   - Secrets management

5. **AWS Systems Manager**
   - Parameter Store integration
   - Secrets Manager integration
   - Session Manager for debugging
   - Patch management

### GitOps and CI/CD Integration

#### ArgoCD Configuration
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/company/k8s-manifests
    targetRevision: HEAD
    path: apps/web-app
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

#### AWS CodePipeline Integration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: buildspec
data:
  buildspec.yml: |
    version: 0.2
    phases:
      pre_build:
        commands:
          - echo Logging in to Amazon ECR...
          - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      build:
        commands:
          - echo Build started on `date`
          - echo Building the Docker image...
          - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
          - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
      post_build:
        commands:
          - echo Build completed on `date`
          - echo Pushing the Docker image...
          - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
          - echo Updating Kubernetes deployment...
          - kubectl set image deployment/web-app web-app=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
```

## Security Considerations

### Cluster Security

1. **Control Plane Security**
   - Private API server endpoints
   - API server access logging
   - Encryption at rest for etcd
   - Network isolation

2. **Node Security**
   - Security group configurations
   - Regular AMI updates
   - Instance metadata service v2
   - SSH key management

3. **Pod Security**
   - Pod Security Standards
   - Security contexts
   - Resource limits
   - Network policies

### Identity and Access Management

1. **Service Accounts**
   - IRSA (IAM Roles for Service Accounts)
   - Fine-grained permissions
   - Token rotation
   - Cross-account access

2. **RBAC (Role-Based Access Control)**
   - Namespace isolation
   - Principle of least privilege
   - User and group management
   - Regular access reviews

### Network Security

1. **VPC Configuration**
   - Private subnets for worker nodes
   - Security groups and NACLs
   - VPC endpoints for AWS services
   - Network segmentation

2. **Service Mesh Security**
   - mTLS between services
   - Traffic encryption
   - Policy enforcement
   - Identity verification

### Compliance and Governance

1. **Security Scanning**
   - Container image scanning
   - Vulnerability assessments
   - Compliance monitoring
   - Security policies

2. **Audit and Monitoring**
   - CloudTrail integration
   - Kubernetes audit logs
   - Runtime security monitoring
   - Anomaly detection

## Monitoring and Troubleshooting

### CloudWatch Container Insights

#### Cluster-Level Metrics
- **ClusterCPUUtilization**: CPU usage across cluster
- **ClusterMemoryUtilization**: Memory usage across cluster
- **ClusterNetworkRxBytes**: Network received bytes
- **ClusterNetworkTxBytes**: Network transmitted bytes
- **ClusterRunningPodCount**: Number of running pods
- **ClusterFailedPodCount**: Number of failed pods

#### Node-Level Metrics
- **NodeCPUUtilization**: CPU usage per node
- **NodeMemoryUtilization**: Memory usage per node
- **NodeNetworkRxBytes**: Network received bytes per node
- **NodeNetworkTxBytes**: Network transmitted bytes per node
- **NodeFilesystemUtilization**: Filesystem usage per node

#### Pod-Level Metrics
- **PodCPUUtilization**: CPU usage per pod
- **PodMemoryUtilization**: Memory usage per pod
- **PodNetworkRxBytes**: Network received bytes per pod
- **PodNetworkTxBytes**: Network transmitted bytes per pod

### Kubernetes-Native Monitoring

#### Resource Monitoring
```bash
# Check cluster nodes
kubectl get nodes

# Check node resource usage
kubectl top nodes

# Check pod resource usage
kubectl top pods --all-namespaces

# Describe node details
kubectl describe node node-name

# Check cluster events
kubectl get events --sort-by=.metadata.creationTimestamp
```

#### Application Monitoring
```bash
# Check deployments
kubectl get deployments --all-namespaces

# Check pod status
kubectl get pods --all-namespaces

# Check service endpoints
kubectl get endpoints --all-namespaces

# Check ingress resources
kubectl get ingress --all-namespaces

# Check horizontal pod autoscalers
kubectl get hpa --all-namespaces
```

### Common Troubleshooting Scenarios

1. **Pod Startup Issues**
   - Image pull failures
   - Resource constraints
   - Configuration errors
   - Network connectivity

2. **Networking Issues**
   - Service discovery problems
   - DNS resolution failures
   - Network policy restrictions
   - Load balancer configuration

3. **Performance Issues**
   - Resource contention
   - Inefficient resource requests/limits
   - Network bottlenecks
   - Storage performance

4. **Scaling Issues**
   - Cluster autoscaler configuration
   - Pod resource requirements
   - Node capacity limits
   - Service quotas

### Debugging Tools and Techniques

#### Pod Debugging
```bash
# Get pod logs
kubectl logs pod-name -c container-name

# Execute commands in pod
kubectl exec -it pod-name -- /bin/bash

# Port forward for debugging
kubectl port-forward pod-name 8080:8080

# Debug with a debug container
kubectl debug pod-name -it --image=busybox
```

#### Network Debugging
```bash
# Test DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup service-name

# Test connectivity
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- ping service-ip

# Check network policies
kubectl get networkpolicies --all-namespaces
```

#### Resource Analysis
```bash
# Check resource quotas
kubectl get resourcequotas --all-namespaces

# Check limit ranges
kubectl get limitranges --all-namespaces

# Analyze resource usage
kubectl top pods --containers --sort-by=cpu
kubectl top pods --containers --sort-by=memory
```

## Exam-Specific Tips and Common Scenarios

### Solutions Architect Associate (SAA-C03)
- **Container Orchestration**: EKS vs ECS comparison
- **Compute Options**: Fargate vs EC2 worker nodes
- **Integration Patterns**: AWS service integration
- **High Availability**: Multi-AZ deployment strategies

### Solutions Architect Professional (SAP-C02)
- **Enterprise Architecture**: Large-scale EKS deployments
- **Hybrid Cloud**: EKS Anywhere and multi-cloud strategies
- **Advanced Networking**: Service mesh and complex networking
- **Cost Optimization**: Advanced cost management strategies

### Developer Associate (DVA-C02)
- **Application Development**: Kubernetes-native application patterns
- **CI/CD Integration**: GitOps and pipeline automation
- **Debugging**: Troubleshooting containerized applications
- **Service Communication**: Inter-service communication patterns

### SysOps Administrator (SOA-C02)
- **Cluster Operations**: Day-to-day cluster management
- **Monitoring Setup**: Comprehensive monitoring strategies
- **Security Management**: Security hardening and compliance
- **Troubleshooting**: Operational issue resolution

### Common Exam Scenarios

1. **Scenario**: Deploy a microservices application
   **Solution**: EKS with service mesh and load balancing

2. **Scenario**: Implement GitOps workflow
   **Solution**: EKS with ArgoCD and AWS CodeCommit

3. **Scenario**: Run ML workloads at scale
   **Solution**: EKS with GPU nodes and Kubeflow

4. **Scenario**: Modernize legacy applications
   **Solution**: Containerize and deploy on EKS with gradual migration

5. **Scenario**: Implement secure multi-tenant environment
   **Solution**: EKS with namespace isolation and RBAC

## Hands-on Examples and CLI Commands

### Cluster Management with eksctl

```bash
# Create cluster with eksctl
eksctl create cluster \
  --name production-cluster \
  --version 1.28 \
  --region us-west-2 \
  --nodegroup-name workers \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 10 \
  --node-type t3.medium \
  --node-volume-size 20 \
  --ssh-access \
  --ssh-public-key my-key-pair \
  --managed

# Create cluster from config file
eksctl create cluster -f cluster-config.yaml

# Update cluster
eksctl update cluster --name production-cluster --approve

# Scale nodegroup
eksctl scale nodegroup \
  --cluster production-cluster \
  --name workers \
  --nodes 5 \
  --nodes-min 2 \
  --nodes-max 15

# Delete cluster
eksctl delete cluster --name production-cluster
```

### AWS CLI Cluster Management

```bash
# Create EKS cluster
aws eks create-cluster \
  --name production-cluster \
  --version 1.28 \
  --role-arn arn:aws:iam::account:role/eks-service-role \
  --resources-vpc-config subnetIds=subnet-12345,subnet-67890,securityGroupIds=sg-12345

# Create managed node group
aws eks create-nodegroup \
  --cluster-name production-cluster \
  --nodegroup-name workers \
  --instance-types t3.medium \
  --ami-type AL2_x86_64 \
  --node-role arn:aws:iam::account:role/NodeInstanceRole \
  --subnets subnet-12345 subnet-67890 \
  --scaling-config minSize=1,maxSize=10,desiredSize=3

# Update kubeconfig
aws eks update-kubeconfig \
  --region us-west-2 \
  --name production-cluster

# List clusters
aws eks list-clusters

# Describe cluster
aws eks describe-cluster --name production-cluster

# List node groups
aws eks list-nodegroups --cluster-name production-cluster

# Describe node group
aws eks describe-nodegroup \
  --cluster-name production-cluster \
  --nodegroup-name workers
```

### Kubernetes Operations

```bash
# Deploy application
kubectl apply -f deployment.yaml

# Create service
kubectl expose deployment web-app \
  --type=LoadBalancer \
  --port=80 \
  --target-port=8080

# Scale deployment
kubectl scale deployment web-app --replicas=5

# Update deployment image
kubectl set image deployment/web-app \
  web-app=my-app:v2.0.0

# Rolling update status
kubectl rollout status deployment/web-app

# Rollback deployment
kubectl rollout undo deployment/web-app

# Check deployment history
kubectl rollout history deployment/web-app
```

### Auto Scaling Setup

```bash
# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Create HPA
kubectl autoscale deployment web-app \
  --cpu-percent=70 \
  --min=3 \
  --max=20

# Get HPA status
kubectl get hpa

# Install cluster autoscaler
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml

# Configure cluster autoscaler
kubectl -n kube-system annotate deployment.apps/cluster-autoscaler \
  cluster-autoscaler.kubernetes.io/safe-to-evict="false"

kubectl -n kube-system edit deployment.apps/cluster-autoscaler
```

### Monitoring and Logging

```bash
# Install CloudWatch Container Insights
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/production-cluster/;s/{{region_name}}/us-west-2/" | kubectl apply -f -

# Check logs
kubectl logs deployment/web-app

# Stream logs
kubectl logs -f deployment/web-app

# Get events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check resource usage
kubectl top nodes
kubectl top pods --all-namespaces
```

### Service Mesh (App Mesh retired)

The App Mesh controller examples that stood here were removed: AWS App Mesh reached end of support on 2026-09-30.

**[📖 App Mesh end of support notice](https://docs.aws.amazon.com/app-mesh/latest/userguide/troubleshooting.html)** - AWS notice

For the concept, see [Service mesh explained](../../../../../learn/concepts/service-mesh-explained.md).

This comprehensive EKS documentation provides detailed coverage for all AWS certification paths, including practical Kubernetes examples and real-world deployment scenarios.