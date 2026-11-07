# AWS Fargate

## Service Overview and Purpose

AWS Fargate is a serverless compute engine for containers that works with both Amazon Elastic Container Service (ECS) and Amazon Elastic Kubernetes Service (EKS). Fargate eliminates the need to provision and manage servers, allowing you to specify and pay for resources per application, and improving security through application isolation by design.

**Core Purpose:**
- Provide serverless container compute
- Eliminate infrastructure management overhead
- Enable automatic scaling based on application needs
- Improve security through container isolation
- Simplify container deployment and operations

## Key Features and Capabilities

### Core Features
- **Serverless**: No servers to provision or manage
- **Right-sizing**: Pay only for the resources you use
- **Security Isolation**: Each task runs in its own kernel runtime environment
- **VPC Networking**: Native VPC integration with ENI per task
- **Auto Scaling**: Automatic scaling based on demand
- **Integration**: Works with ECS and EKS
- **Monitoring**: Built-in CloudWatch integration
- **Compliance**: SOC, PCI, ISO certifications

### Technical Specifications

#### Resource Configurations
- **CPU**: 0.25 vCPU to 4 vCPU (incremental options)
- **Memory**: 0.5 GB to 30 GB (specific combinations supported)
- **Storage**: 20 GB to 200 GB ephemeral storage
- **Network**: Enhanced networking with up to 10 Gbps
- **Platform Versions**: Linux and Windows containers

#### Supported CPU/Memory Combinations
```
CPU (vCPU) | Memory (GB)
-----------|-------------
0.25       | 0.5, 1, 2
0.5        | 1, 2, 3, 4
1          | 2, 3, 4, 5, 6, 7, 8
2          | 4-16 (1 GB increments)
4          | 8-30 (1 GB increments)
```

### Container Runtime Environment
- **Task Isolation**: Each task runs in its own microVM
- **Network Interface**: Dedicated ENI per task
- **Security Groups**: Applied at task level
- **IAM Roles**: Task-level IAM integration
- **Secrets Management**: Native integration with AWS services
- **Logging**: Container logs sent to CloudWatch

## Use Cases and Scenarios

### Primary Use Cases

1. **Microservices Applications**
   - API backends and web services
   - Event-driven microservices
   - Service-oriented architectures
   - Container-native applications

2. **Batch Processing**
   - Data processing workflows
   - ETL operations
   - Machine learning inference
   - Scheduled task execution

3. **Web Applications**
   - Frontend and backend services
   - Content management systems
   - E-commerce platforms
   - Real-time applications

4. **Development and Testing**
   - CI/CD pipelines
   - Development environments
   - Testing automation
   - Staging deployments

5. **Event-Driven Workloads**
   - Serverless container processing
   - Queue-based processing
   - Stream processing applications
   - Webhook handlers

### Detailed Scenarios

#### Serverless API Backend
```
API Gateway → Fargate Task (ECS) → RDS/DynamoDB
     ↓              ↓                    ↓
 Authentication → Business Logic → Data Storage
```

#### Event-Driven Processing
```
S3 Event → Lambda → ECS Fargate Task → Process File → Store Result
    ↓         ↓           ↓                ↓            ↓
File Upload → Trigger → Start Container → Transform → S3/Database
```

#### Microservices Architecture
```
Load Balancer → User Service (Fargate)
             → Order Service (Fargate)
             → Payment Service (Fargate)
             → Inventory Service (Fargate)
                      ↓
                Shared Database Layer
```

#### CI/CD Pipeline
```
Code Commit → CodeBuild → Fargate Task (Test) → CodeDeploy → Production
     ↓           ↓             ↓                    ↓            ↓
Source Code → Build Image → Run Tests → Deploy → Live Service
```

## Pricing Models and Cost Optimization

### Pricing Structure

#### Fargate Pricing Components
1. **vCPU**: $0.04048 per vCPU per hour
2. **Memory**: $0.004445 per GB per hour
3. **Storage**: $0.000111 per GB per hour (ephemeral)
4. **Data Transfer**: Standard AWS data transfer rates

#### Billing Model
- **Per-second billing**: Minimum 1-minute charge
- **Resource-based**: Pay for allocated CPU and memory
- **No minimum fees**: Pay only when containers run
- **Regional pricing**: Varies by AWS region

### Cost Optimization Strategies

1. **Right-size Resources**
   - Monitor actual CPU and memory usage
   - Choose optimal CPU/memory combinations
   - Use CloudWatch Container Insights for analysis
   - Avoid over-provisioning resources

2. **Efficient Task Design**
   - Optimize container startup time
   - Implement efficient application initialization
   - Use shared resources where possible
   - Minimize idle time between tasks

3. **Scheduling Optimization**
   - Use spot pricing where available
   - Schedule batch jobs during off-peak hours
   - Implement efficient task queuing
   - Optimize task frequency

4. **Fargate vs EC2 Decision Matrix**
   ```
   Choose Fargate when:
   - Variable or unpredictable workloads
   - Short-running tasks
   - Development/testing environments
   - Don't want infrastructure management

   Choose EC2 when:
   - Steady, long-running workloads
   - Need specific instance features
   - Cost optimization for predictable workloads
   - Require custom AMIs or configurations
   ```

5. **Monitoring and Optimization**
   - Use AWS Cost Explorer for analysis
   - Implement resource tagging for cost allocation
   - Set up billing alerts and budgets
   - Regular cost reviews and optimization

## Configuration Details and Best Practices

### ECS with Fargate Configuration

#### Task Definition for Fargate
```json
{
  "family": "web-app-fargate",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "web-app",
      "image": "my-web-app:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/web-app-fargate",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "environment": [
        {
          "name": "ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:db-password"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ],
  "platformVersion": "1.4.0",
  "runtimePlatform": {
    "cpuArchitecture": "X86_64",
    "operatingSystemFamily": "LINUX"
  }
}
```

#### Service Configuration
```json
{
  "serviceName": "web-app-service",
  "cluster": "fargate-cluster",
  "taskDefinition": "web-app-fargate:1",
  "desiredCount": 3,
  "launchType": "FARGATE",
  "platformVersion": "1.4.0",
  "networkConfiguration": {
    "awsvpcConfiguration": {
      "subnets": ["subnet-12345", "subnet-67890"],
      "securityGroups": ["sg-web-app"],
      "assignPublicIp": "ENABLED"
    }
  },
  "loadBalancers": [
    {
      "targetGroupArn": "arn:aws:elasticloadbalancing:region:account:targetgroup/web-app/123",
      "containerName": "web-app",
      "containerPort": 8080
    }
  ],
  "serviceRegistries": [
    {
      "registryArn": "arn:aws:servicediscovery:region:account:service/srv-web-app"
    }
  ],
  "deploymentConfiguration": {
    "maximumPercent": 200,
    "minimumHealthyPercent": 100
  }
}
```

### EKS with Fargate Configuration

#### Fargate Profile
```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: fargate-cluster
  region: us-west-2

fargateProfiles:
  - name: default-fargate-profile
    selectors:
      - namespace: default
      - namespace: kube-system
        labels:
          k8s-app: kube-dns
  - name: app-fargate-profile
    selectors:
      - namespace: production
        labels:
          compute-type: fargate
      - namespace: staging
        labels:
          compute-type: fargate
    tags:
      Environment: production
      Team: platform
```

#### Kubernetes Deployment for Fargate
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
      compute-type: fargate
  template:
    metadata:
      labels:
        app: web-app
        compute-type: fargate
    spec:
      containers:
      - name: web-app
        image: my-web-app:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
        - name: ENV
          value: "production"
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: host
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
```

### Best Practices

#### Container Optimization
1. **Image Optimization**
   - Use minimal base images (Alpine, Distroless)
   - Multi-stage Docker builds
   - Remove unnecessary dependencies
   - Optimize layer caching

2. **Application Design**
   - Fast startup times
   - Graceful shutdown handling
   - Stateless application design
   - Health check endpoints

3. **Resource Management**
   - Set appropriate resource requests and limits
   - Monitor actual resource usage
   - Use efficient programming languages and frameworks
   - Implement connection pooling

#### Security Best Practices
1. **Network Security**
   - Use private subnets when possible
   - Configure security groups with minimal access
   - Implement network policies (EKS)
   - Use VPC endpoints for AWS services

2. **IAM Security**
   - Use task-specific IAM roles
   - Follow least privilege principle
   - Regularly audit permissions
   - Use temporary credentials

3. **Image Security**
   - Scan images for vulnerabilities
   - Use trusted base images
   - Implement image signing
   - Regular security updates

#### Performance Optimization
1. **Cold Start Reduction**
   - Optimize container initialization
   - Use provisioned concurrency patterns
   - Implement efficient health checks
   - Minimize external dependencies

2. **Resource Efficiency**
   - Right-size CPU and memory
   - Use appropriate platform versions
   - Implement efficient logging
   - Optimize database connections

## Integration with Other AWS Services

### Core Service Integrations

1. **Amazon ECS**
   - Task definitions and services
   - Service discovery integration
   - Load balancer integration
   - Auto scaling capabilities

2. **Amazon EKS**
   - Fargate profiles for namespaces
   - Kubernetes native scheduling
   - Pod-level resource allocation
   - Service mesh integration

3. **Application Load Balancer (ALB)**
   - HTTP/HTTPS load balancing
   - Path and host-based routing
   - Target group integration
   - Health check configuration

4. **Amazon VPC**
   - ENI allocation per task
   - Security group assignment
   - Subnet placement control
   - VPC endpoint integration

5. **AWS IAM**
   - Task execution roles
   - Task roles for application access
   - Service-linked roles
   - Cross-account access

### Advanced Integrations

1. **Amazon CloudWatch**
   - Container Insights monitoring
   - Custom metrics publishing
   - Log aggregation and analysis
   - Alerting and dashboards

2. **AWS Secrets Manager**
   - Secure secret storage
   - Automatic secret rotation
   - Task definition integration
   - Runtime secret injection

3. **Amazon ECR**
   - Private container registry
   - Image vulnerability scanning
   - Lifecycle policies
   - Cross-region replication

4. **AWS App Mesh (retired)**
   - End of support 2026-09-30; for ECS use Service Connect
   - Security policies

5. **Amazon EventBridge**
   - Event-driven architectures
   - Task state change events
   - Custom event routing
   - Integration with other services

### CI/CD Integration Patterns

#### CodePipeline with Fargate
```yaml
# buildspec.yml for CodeBuild
version: 0.2
phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker images...
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - echo Writing image definitions file...
      - printf '[{"name":"web-app","imageUri":"%s"}]' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json
artifacts:
  files:
    - imagedefinitions.json
```

#### GitOps with EKS Fargate
```yaml
# ArgoCD Application for Fargate workloads
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-app-fargate
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
  # Ensure pods are scheduled on Fargate
  syncOptions:
  - RespectIgnoreDifferences=true
```

## Security Considerations

### Task-Level Security

1. **Isolation Benefits**
   - Each task runs in its own microVM
   - Hypervisor-level isolation
   - Dedicated kernel runtime
   - Network interface isolation

2. **IAM Integration**
   - Task execution roles for AWS service access
   - Task roles for application permissions
   - Temporary credential management
   - Cross-account access controls

3. **Network Security**
   - VPC native networking
   - Security groups at task level
   - Private subnet deployment
   - VPC endpoints for AWS services

### Data Protection

1. **Encryption**
   - Encryption in transit (TLS)
   - Encryption at rest (EBS/EFS)
   - Secret encryption (KMS)
   - Log encryption (CloudWatch)

2. **Secrets Management**
   - AWS Secrets Manager integration
   - Parameter Store integration
   - Environment variable encryption
   - Runtime secret injection

### Compliance and Governance

1. **Compliance Standards**
   - SOC 1, 2, 3 compliance
   - PCI DSS Level 1
   - ISO 27001, 27017, 27018
   - FedRAMP authorization

2. **Auditing and Monitoring**
   - CloudTrail API logging
   - VPC Flow Logs
   - Container activity monitoring
   - Security event alerting

## Monitoring and Troubleshooting

### CloudWatch Metrics

#### Fargate-Specific Metrics
- **CPUUtilization**: CPU usage percentage
- **MemoryUtilization**: Memory usage percentage
- **NetworkRxBytes**: Network bytes received
- **NetworkTxBytes**: Network bytes transmitted
- **StorageReadBytes**: Storage read operations
- **StorageWriteBytes**: Storage write operations

#### ECS Fargate Metrics
- **RunningTaskCount**: Number of running tasks
- **PendingTaskCount**: Number of pending tasks
- **ActiveServiceCount**: Number of active services
- **CPUReservation**: Reserved CPU percentage
- **MemoryReservation**: Reserved memory percentage

#### EKS Fargate Metrics
- **cluster_failed_request_count**: Failed API requests
- **cluster_node_count**: Number of Fargate nodes
- **namespace_number_of_running_pods**: Running pods per namespace
- **pod_cpu_utilization**: Pod CPU utilization
- **pod_memory_utilization**: Pod memory utilization

### Container Insights Integration

#### Fargate Container Insights
```bash
# Enable Container Insights for ECS cluster
aws ecs put-account-setting \
  --name containerInsights \
  --value enabled

# Enable for specific cluster
aws ecs update-cluster \
  --cluster fargate-cluster \
  --configuration executeCommandConfiguration='{
    "kmsKeyId": "alias/aws/ecs",
    "logging": "DEFAULT"
  }'
```

#### Custom Metrics Publishing
```python
import boto3
import json

cloudwatch = boto3.client('cloudwatch')

def publish_custom_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='Fargate/Application',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Dimensions': [
                    {
                        'Name': 'ServiceName',
                        'Value': 'web-app'
                    },
                    {
                        'Name': 'Environment',
                        'Value': 'production'
                    }
                ]
            }
        ]
    )
```

### Common Troubleshooting Scenarios

1. **Task Startup Issues**
   - Image pull failures from ECR
   - Insufficient task resources
   - Network configuration problems
   - IAM permission issues

2. **Performance Issues**
   - Under-resourced tasks
   - Network bandwidth limitations
   - Storage performance bottlenecks
   - Application inefficiencies

3. **Networking Issues**
   - Security group misconfigurations
   - Subnet capacity limitations
   - DNS resolution problems
   - Load balancer health checks

4. **Cost Issues**
   - Over-provisioned resources
   - Long-running idle tasks
   - Inefficient scaling policies
   - Unnecessary task restarts

### Debugging Tools and Techniques

#### ECS Fargate Debugging
```bash
# Enable ECS Exec for debugging
aws ecs update-service \
  --cluster fargate-cluster \
  --service web-app-service \
  --enable-execute-command

# Execute command in running task
aws ecs execute-command \
  --cluster fargate-cluster \
  --task task-id \
  --container web-app \
  --interactive \
  --command "/bin/bash"

# Get task details
aws ecs describe-tasks \
  --cluster fargate-cluster \
  --tasks task-id

# Check service events
aws ecs describe-services \
  --cluster fargate-cluster \
  --services web-app-service \
  --query 'services[0].events'
```

#### EKS Fargate Debugging
```bash
# Check Fargate profile
kubectl get fargateprofile -A

# Describe pod on Fargate
kubectl describe pod pod-name -n namespace

# Check pod logs
kubectl logs pod-name -c container-name -n namespace

# Execute into Fargate pod
kubectl exec -it pod-name -c container-name -n namespace -- /bin/bash

# Check node information
kubectl get nodes -l eks.amazonaws.com/compute-type=fargate
```

#### Performance Analysis
```bash
# Monitor resource usage
kubectl top pods -n production --containers

# Check resource limits
kubectl describe limits -n production

# Analyze resource quotas
kubectl describe quota -n production

# Check horizontal pod autoscaler
kubectl get hpa -n production
```

## Exam-Specific Tips and Common Scenarios

### Solutions Architect Associate (SAA-C03)
- **Serverless vs Managed**: Fargate vs EC2 decision criteria
- **Cost Optimization**: When to choose Fargate over EC2
- **Integration Patterns**: ALB, VPC, and service integration
- **Scaling Strategies**: Auto scaling with Fargate

### Solutions Architect Professional (SAP-C02)
- **Enterprise Architecture**: Large-scale Fargate deployments
- **Hybrid Solutions**: Integration with on-premises systems
- **Multi-Region**: Cross-region Fargate strategies
- **Cost Management**: Advanced cost optimization techniques

### Developer Associate (DVA-C02)
- **Application Development**: Container-native development
- **CI/CD Integration**: Automated deployment pipelines
- **Debugging**: Troubleshooting containerized applications
- **Performance**: Optimizing application performance

### SysOps Administrator (SOA-C02)
- **Operational Management**: Day-to-day Fargate operations
- **Monitoring Setup**: Comprehensive monitoring strategies
- **Security Operations**: Security best practices
- **Troubleshooting**: Common operational issues

### Common Exam Scenarios

1. **Scenario**: Need to run containers without managing infrastructure
   **Solution**: Use Fargate for serverless container hosting

2. **Scenario**: Variable workload with unpredictable traffic
   **Solution**: Fargate with auto scaling and load balancing

3. **Scenario**: Secure multi-tenant application
   **Solution**: Fargate tasks with VPC isolation and IAM roles

4. **Scenario**: Event-driven container processing
   **Solution**: Lambda triggers with Fargate tasks for processing

5. **Scenario**: Cost-effective development environments
   **Solution**: Fargate for on-demand development containers

## Hands-on Examples and CLI Commands

### ECS Fargate Management

```bash
# Create Fargate cluster
aws ecs create-cluster \
  --cluster-name fargate-cluster \
  --capacity-providers FARGATE FARGATE_SPOT \
  --default-capacity-provider-strategy \
    capacityProvider=FARGATE,weight=1,base=1 \
    capacityProvider=FARGATE_SPOT,weight=4,base=0

# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://fargate-task-definition.json

# Create service
aws ecs create-service \
  --cluster fargate-cluster \
  --service-name web-app-service \
  --task-definition web-app-fargate:1 \
  --desired-count 3 \
  --launch-type FARGATE \
  --platform-version 1.4.0 \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-12345", "subnet-67890"],
      "securityGroups": ["sg-web-app"],
      "assignPublicIp": "ENABLED"
    }
  }'

# Run one-time task
aws ecs run-task \
  --cluster fargate-cluster \
  --task-definition batch-job:1 \
  --launch-type FARGATE \
  --platform-version 1.4.0 \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-12345"],
      "securityGroups": ["sg-batch"],
      "assignPublicIp": "ENABLED"
    }
  }'
```

### EKS Fargate Management

```bash
# Create EKS cluster with Fargate
eksctl create cluster \
  --name fargate-cluster \
  --region us-west-2 \
  --fargate

# Create Fargate profile
eksctl create fargateprofile \
  --cluster fargate-cluster \
  --name production-profile \
  --namespace production \
  --labels environment=production

# Deploy application to Fargate
kubectl apply -f - <<EOF
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
        environment: production
    spec:
      containers:
      - name: web-app
        image: nginx:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
EOF

# Create service
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
  namespace: production
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: web-app
EOF
```

### Monitoring and Debugging

```bash
# Enable Container Insights
aws logs create-log-group \
  --log-group-name /aws/ecs/containerinsights/fargate-cluster/performance

# Get CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=web-app-service Name=ClusterName,Value=fargate-cluster \
  --statistics Average \
  --start-time 2023-01-01T00:00:00Z \
  --end-time 2023-01-01T23:59:59Z \
  --period 3600

# Get task logs
aws logs get-log-events \
  --log-group-name /ecs/web-app-fargate \
  --log-stream-name ecs/web-app/task-id

# Debug with ECS Exec
aws ecs execute-command \
  --cluster fargate-cluster \
  --task task-id \
  --container web-app \
  --interactive \
  --command "/bin/sh"
```

### Cost Monitoring

```bash
# Get Fargate usage with Cost Explorer API
aws ce get-cost-and-usage \
  --time-period Start=2023-01-01,End=2023-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --filter '{
    "Dimensions": {
      "Key": "SERVICE",
      "Values": ["Amazon Elastic Container Service"]
    }
  }'

# Set up billing alert
aws cloudwatch put-metric-alarm \
  --alarm-name "Fargate-High-Cost" \
  --alarm-description "Alert when Fargate costs exceed threshold" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 86400 \
  --threshold 100 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=Currency,Value=USD Name=ServiceName,Value=AmazonECS
```

This comprehensive Fargate documentation covers all aspects needed for AWS certification preparation, providing both theoretical knowledge and practical examples for serverless container management.