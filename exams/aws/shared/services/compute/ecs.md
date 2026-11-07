# Amazon ECS (Elastic Container Service)

## Service Overview and Purpose

Amazon Elastic Container Service (ECS) is a fully managed container orchestration service that makes it easy to deploy, manage, and scale containerized applications using Docker containers. ECS eliminates the need to install and operate your own container orchestration software, manage and scale a cluster of virtual machines, or schedule containers on those virtual machines.

**Core Purpose:**
- Orchestrate Docker containers at scale
- Provide a managed container platform
- Enable microservices architectures
- Integrate deeply with AWS services
- Offer both serverless (Fargate) and EC2-based hosting options

## Key Features and Capabilities

### Core Features
- **Task Definitions**: Blueprints for your application containers
- **Services**: Maintain desired number of running tasks
- **Clusters**: Logical grouping of compute resources
- **Container Instances**: EC2 instances running ECS agent
- **Fargate**: Serverless container hosting
- **Service Discovery**: Automatic DNS-based service discovery
- **Load Balancing**: Integration with ALB/NLB/CLB
- **Auto Scaling**: Automatic scaling based on metrics
- **Rolling Updates**: Zero-downtime deployments
- **Task Placement**: Control where tasks run

### Launch Types

#### EC2 Launch Type
- Run containers on self-managed EC2 instances
- Full control over infrastructure
- Cost-effective for steady workloads
- Access to underlying EC2 features

#### Fargate Launch Type
- Serverless container hosting
- No infrastructure management
- Pay for resources used
- Automatic scaling and patching

### Container Agent Features
- **Task Management**: Start, stop, and monitor containers
- **Resource Monitoring**: CPU, memory, network metrics
- **Health Checks**: Container and service health monitoring
- **Log Collection**: Integration with CloudWatch Logs
- **Secret Management**: Integration with Systems Manager and Secrets Manager

## Use Cases and Scenarios

### Primary Use Cases

1. **Microservices Architecture**
   - Decompose monolithic applications
   - Independent scaling and deployment
   - Service-to-service communication

2. **Web Applications**
   - Multi-tier web applications
   - API backends
   - Content management systems

3. **Batch Processing**
   - Data processing pipelines
   - ETL operations
   - Machine learning training

4. **CI/CD Workloads**
   - Build and test environments
   - Deployment pipelines
   - Development sandboxes

5. **Legacy Application Modernization**
   - Containerize existing applications
   - Lift and shift to containers
   - Gradual migration strategies

### Detailed Scenarios

#### E-commerce Platform
```
Frontend Service (React) → API Gateway → Backend Services (Node.js/Python)
                                      ↓
                                 Database Services (RDS/DynamoDB)
```

#### Data Processing Pipeline
```
Data Input → SQS → ECS Tasks (Processing) → S3/Database → Notifications
```

#### Microservices with Service Discovery
```
User Service ↔ Order Service ↔ Payment Service ↔ Inventory Service
      ↓              ↓               ↓                ↓
  Load Balancer → Service Discovery ← CloudMap Integration
```

## Pricing Models and Cost Optimization

### Pricing Components

#### EC2 Launch Type
- **EC2 Instances**: Standard EC2 pricing
- **EBS Volumes**: Block storage costs
- **Data Transfer**: Network usage charges
- **Load Balancers**: ALB/NLB pricing

#### Fargate Launch Type
- **vCPU**: Per vCPU per second
- **Memory**: Per GB per second
- **Storage**: Ephemeral storage charges
- **Data Transfer**: Network egress charges

### Cost Optimization Strategies

1. **Right-sizing Resources**
   - Monitor CPU and memory utilization
   - Use appropriate task definitions
   - Implement auto scaling

2. **Fargate vs EC2 Decision**
   - Fargate: Variable, unpredictable workloads
   - EC2: Steady, predictable workloads
   - Consider reserved instances for EC2

3. **Spot Instances for EC2**
   - Use Spot instances for fault-tolerant workloads
   - Mix On-Demand and Spot for cost optimization
   - Implement proper handling for interruptions

4. **Resource Allocation**
   - Share resources across multiple tasks
   - Use task placement strategies efficiently
   - Implement efficient container packing

5. **Monitoring and Optimization**
   - Use AWS Cost Explorer
   - Implement resource tagging
   - Regular cost reviews and optimization

## Configuration Details and Best Practices

### Task Definition Configuration

#### Basic Task Definition
```json
{
  "family": "web-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "web-server",
      "image": "nginx:latest",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/web-app",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Advanced Task Definition
```json
{
  "family": "complex-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["EC2"],
  "placementConstraints": [
    {
      "type": "memberOf",
      "expression": "attribute:ecs.instance-type =~ t3.*"
    }
  ],
  "containerDefinitions": [
    {
      "name": "app-container",
      "image": "my-app:latest",
      "memory": 1024,
      "memoryReservation": 512,
      "cpu": 512,
      "essential": true,
      "environment": [
        {
          "name": "ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "arn:aws:ssm:region:account:parameter/db/password"
        }
      ],
      "mountPoints": [
        {
          "sourceVolume": "efs-volume",
          "containerPath": "/data",
          "readOnly": false
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
  "volumes": [
    {
      "name": "efs-volume",
      "efsVolumeConfiguration": {
        "fileSystemId": "fs-12345678"
      }
    }
  ]
}
```

### Service Configuration

#### Basic Service
```json
{
  "serviceName": "web-service",
  "cluster": "production-cluster",
  "taskDefinition": "web-app:1",
  "desiredCount": 3,
  "launchType": "FARGATE",
  "networkConfiguration": {
    "awsvpcConfiguration": {
      "subnets": ["subnet-12345", "subnet-67890"],
      "securityGroups": ["sg-12345"],
      "assignPublicIp": "ENABLED"
    }
  },
  "loadBalancers": [
    {
      "targetGroupArn": "arn:aws:elasticloadbalancing:region:account:targetgroup/my-targets/1234567890123456",
      "containerName": "web-server",
      "containerPort": 80
    }
  ]
}
```

#### Service with Auto Scaling
```json
{
  "serviceName": "scalable-service",
  "cluster": "production-cluster",
  "taskDefinition": "web-app:1",
  "desiredCount": 2,
  "deploymentConfiguration": {
    "maximumPercent": 200,
    "minimumHealthyPercent": 50
  },
  "placementStrategy": [
    {
      "type": "spread",
      "field": "attribute:ecs.availability-zone"
    }
  ],
  "serviceRegistries": [
    {
      "registryArn": "arn:aws:servicediscovery:region:account:service/srv-12345"
    }
  ]
}
```

### ECS Network Modes

**[📖 ECS Network Modes](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html)** - Comprehensive networking guide

ECS network modes determine how containers within a task communicate with each other, with other services, and with the underlying host network. Each network mode configures the networking environment differently, impacting security, connectivity, and control.

#### 1. None Network Mode

**What it does**: Containers have **no external network connectivity**. They cannot communicate with other containers, services, or the internet.

**Key Characteristics:**
- No external network interfaces assigned
- Port mappings cannot be specified
- Containers can only communicate within the same task via **localhost**
- Maximum network isolation

**Use Cases:**
- Isolated, compute-intensive batch workloads (data processing, rendering)
- Tasks requiring maximum network isolation for security
- Workloads with no external communication needs

**Limitations:**
- No external connectivity limits use for networked applications
- Not suitable for microservices requiring inter-service communication
- Cannot host web servers or APIs

**Example Task Definition:**
```json
{
  "family": "isolated-batch-job",
  "networkMode": "none",
  "containerDefinitions": [
    {
      "name": "batch-processor",
      "image": "my-batch-app:latest",
      "memory": 512,
      "cpu": 256
    }
  ]
}
```

#### 2. Bridge Network Mode

**What it does**: Containers use **Docker's built-in virtual network** (Docker bridge) on the host EC2 instance. Docker manages port mappings to route traffic.

**Key Characteristics:**
- Containers get private IPs within Docker bridge network
- Port mappings required to expose services (e.g., container port 80 → host port 8080)
- Security groups applied at **EC2 instance level**, not per task
- Containers on same host communicate via Docker bridge
- **[📖 Bridge Mode Details](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking-bridge.html)**

**Use Cases:**
- Legacy applications not requiring advanced networking
- Simple workloads without fine-grained network control needs
- Development/testing environments prioritizing simplicity
- Applications where multiple containers share host networking

**Limitations:**
- Limited network isolation (containers share host network stack)
- Security groups apply to entire EC2 instance, not individual tasks
- Complex port management with overlapping ports
- Less secure for multi-tenant or sensitive workloads

**Example Task Definition:**
```json
{
  "family": "web-app-bridge",
  "networkMode": "bridge",
  "containerDefinitions": [
    {
      "name": "web-server",
      "image": "nginx:latest",
      "memory": 512,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 8080,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

#### 3. Host Network Mode

**What it does**: Containers **bypass Docker's virtual network** and directly use the **host EC2 instance's network interface**.

**Key Characteristics:**
- Containers share host's IP address and network stack
- No network abstraction layer
- Port mappings not needed (containers use host ports directly)
- Security groups at **EC2 instance level**
- Cannot run multiple instances of same task on single host (port conflicts)
- **[📖 Host Mode Details](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking-host.html)**

**Use Cases:**
- High-performance applications requiring direct network access
- Low-latency network services (real-time analytics, streaming)
- Single task per host workloads
- Applications where network simplicity outweighs isolation needs

**Limitations:**
- No network isolation between containers and host (security risk)
- Port conflicts prevent multiple task instances per host
- Security groups apply to entire EC2 instance
- Less secure due to shared network stack

**Example Task Definition:**
```json
{
  "family": "high-performance-app",
  "networkMode": "host",
  "containerDefinitions": [
    {
      "name": "streaming-app",
      "image": "my-streaming-app:latest",
      "memory": 1024,
      "cpu": 512
    }
  ]
}
```

#### 4. awsvpc Network Mode (Recommended for Production)

**What it does**: Each ECS task gets its own **Elastic Network Interface (ENI)** with a private IP address in the VPC, providing the same networking capabilities as an EC2 instance.

**Key Characteristics:**
- Each task gets dedicated ENI with private IP
- **Security groups at task level** (fine-grained control)
- Compatible with **VPC Flow Logs** for traffic monitoring
- Containers in same task communicate via **localhost**
- Requires **NetworkConfiguration** (subnets, security groups)
- **Required for Fargate launch type**
- **[📖 awsvpc Mode Details](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking-awsvpc.html)**

**Use Cases:**
- **Production microservices** (recommended for most workloads)
- Applications requiring strong network isolation and security
- Workloads needing task-specific security groups (least privilege)
- Compliance-driven environments requiring network monitoring
- Applications integrating with VPC features (private subnets, route tables)
- **Fargate deployments** (mandatory)

**Security Benefits:**
- **Granular security**: Task-level security groups enable fine-grained traffic control
- **Network monitoring**: Dedicated ENI supports VPC Flow Logs for compliance
- **IAM roles for tasks**: Avoid passing credentials; use temporary credentials
- **Isolation**: Each task in own network namespace

**Limitations:**
- Slightly higher operational complexity (VPC configuration required)
- Consumes ENIs (consider VPC ENI limits for large deployments)
- Not ideal for extremely lightweight workloads

**Example Task Definition:**
```json
{
  "family": "microservice-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "api-service",
      "image": "my-api:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/api-service",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Example Service with NetworkConfiguration:**
```bash
aws ecs create-service \
  --cluster production-cluster \
  --service-name api-service \
  --task-definition microservice-app:1 \
  --desired-count 3 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[subnet-12345,subnet-67890],
    securityGroups=[sg-api-service],
    assignPublicIp=DISABLED
  }" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=api-service,containerPort=3000"
```

#### Network Mode Comparison Table

| Feature | None | Bridge | Host | awsvpc |
|---------|------|--------|------|--------|
| **External Connectivity** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Task-Level Security Groups** | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Network Isolation** | ⭐ Maximum | 🟡 Limited | ❌ None | ⭐ High |
| **ENI per Task** | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **VPC Flow Logs Support** | ❌ No | 🟡 Instance-level | 🟡 Instance-level | ✅ Task-level |
| **Port Mapping** | ❌ Not allowed | ✅ Required | ❌ Not needed | ✅ Optional |
| **Fargate Compatible** | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Operational Complexity** | ⭐ Lowest | 🟡 Medium | 🟡 Medium | 🟢 Higher |
| **Security Level** | 🟡 Isolated | ⚠️ Low | ⚠️ Low | ⭐ High |
| **Best For** | Batch jobs | Legacy apps | High-perf | Production microservices |

#### Exam Scenario: CRM Portal Security

**Scenario**: Company deploying customer-facing CRM portal with strict security requirements. Needs container-level security groups, network monitoring, and secure AWS resource access.

**Why awsvpc is correct:**
1. **Task-level security groups**: Apply least privilege at container level
2. **VPC Flow Logs**: Monitor traffic for compliance
3. **IAM roles for tasks**: Secure AWS resource access without hardcoded credentials
4. **Network isolation**: Each task in own network namespace

**Why other modes are incorrect:**
- **None**: No external connectivity (CRM needs internet access)
- **Bridge**: Security groups at instance level (insufficient granularity)
- **Host**: No task isolation, port conflicts, instance-level security
- **Passing IAM credentials**: Security risk (credentials in logs, misconfiguration)

**Best Practice**: Use **awsvpc + IAM roles for tasks** for secure, production microservices.

### Best Practices

#### Container Design
1. **Single Process**: One process per container
2. **Stateless**: Design stateless containers
3. **Health Checks**: Implement proper health checks
4. **Graceful Shutdown**: Handle SIGTERM signals properly
5. **Resource Limits**: Set appropriate CPU and memory limits

#### Security Best Practices
1. **IAM Roles**: Use task roles for least privilege
2. **Network Security**: Use security groups and NACLs
3. **Image Security**: Scan images for vulnerabilities
4. **Secrets Management**: Use AWS Secrets Manager or Parameter Store
5. **Resource Isolation**: Use appropriate network modes

#### Performance Optimization
1. **Resource Allocation**: Right-size CPU and memory
2. **Placement Strategies**: Optimize task placement
3. **Load Balancing**: Use appropriate load balancer types
4. **Caching**: Implement caching strategies
5. **Connection Pooling**: Reuse database connections

## Integration with Other AWS Services

### Core Integrations

1. **Application Load Balancer (ALB)**
   - HTTP/HTTPS load balancing
   - Path-based and host-based routing
   - Integration with target groups

2. **Network Load Balancer (NLB)**
   - TCP/UDP load balancing
   - High performance and low latency
   - Static IP addresses

3. **Service Discovery (AWS Cloud Map)**
   - DNS-based service discovery
   - Health check integration
   - Service registry management

4. **Auto Scaling**
   - Target tracking scaling
   - Step scaling
   - Scheduled scaling

5. **CloudWatch**
   - Container insights
   - Custom metrics
   - Log aggregation

### Advanced Integrations

1. **AWS Fargate**
   - Serverless container hosting
   - No infrastructure management
   - Automatic scaling

2. **Amazon ECR**
   - Container image registry
   - Vulnerability scanning
   - Lifecycle policies

3. **AWS Systems Manager**
   - Parameter Store integration
   - Session Manager for debugging
   - Patch management

4. **AWS Secrets Manager**
   - Secure secret storage
   - Automatic rotation
   - Integration with task definitions

5. **Amazon EFS**
   - Shared file storage
   - Persistent data storage
   - Multi-AZ availability

### Container Orchestration Patterns

#### Blue/Green Deployment
```
Production Service → ALB → Target Group A (Blue)
                        → Target Group B (Green)
```

#### Canary Deployment
```
Traffic Split → 90% → Stable Version
             → 10% → New Version
```

#### Service Mesh Integration
Use **ECS Service Connect** for service-to-service traffic in ECS. AWS App Mesh reached end of support on 2026-09-30 and AWS recommends migrating to Service Connect.

**[📖 App Mesh end of support notice](https://docs.aws.amazon.com/app-mesh/latest/userguide/troubleshooting.html)** - AWS notice (App Mesh is history, not a current option)

## Security Considerations

### Container Security
1. **Image Security**
   - Use minimal base images
   - Regular vulnerability scanning
   - Image signing and verification
   - Private container registries

2. **Runtime Security**
   - Resource limits and constraints
   - Security contexts
   - Network policies
   - Access controls

### Network Security
1. **VPC Configuration**
   - Private subnets for containers
   - NAT gateways for outbound access
   - Security groups and NACLs
   - VPC endpoints for AWS services

2. **Service-to-Service Communication**
   - Encrypted communication (TLS)
   - Service mesh integration
   - API authentication
   - Network segmentation

### Access Control
1. **IAM Integration**
   - Task execution roles
   - Task roles for application access
   - Cross-account access
   - Temporary credentials

2. **Secrets Management**
   - AWS Secrets Manager integration
   - Parameter Store integration
   - Environment variable encryption
   - Secret rotation

### Compliance and Auditing
1. **Logging and Monitoring**
   - CloudTrail for API calls
   - CloudWatch Logs for containers
   - Container Insights
   - Security monitoring

2. **Compliance Standards**
   - SOC compliance
   - PCI DSS compliance
   - HIPAA compliance
   - FedRAMP compliance

## Monitoring and Troubleshooting

### CloudWatch Metrics

#### Cluster-Level Metrics
- **CPUUtilization**: CPU usage across cluster
- **MemoryUtilization**: Memory usage across cluster
- **ActiveServicesCount**: Number of active services
- **PendingTasksCount**: Tasks waiting to be placed
- **RunningTasksCount**: Currently running tasks

#### Service-Level Metrics
- **CPUUtilization**: Service CPU usage
- **MemoryUtilization**: Service memory usage
- **TaskCount**: Number of running tasks
- **PendingCount**: Tasks waiting to start
- **DeploymentCount**: Number of deployments

#### Task-Level Metrics
- **TaskCPUUtilization**: Individual task CPU
- **TaskMemoryUtilization**: Individual task memory
- **TaskNetworkRxBytes**: Network received bytes
- **TaskNetworkTxBytes**: Network transmitted bytes

### Container Insights

#### Cluster Overview
- Resource utilization trends
- Task and service counts
- Performance metrics
- Cost optimization insights

#### Service Map
- Service dependencies
- Request flow visualization
- Performance bottlenecks
- Error rates and latency

### Common Troubleshooting Scenarios

1. **Task Startup Issues**
   - Image pull failures
   - Insufficient resources
   - Network configuration
   - IAM permission issues

2. **Service Deployment Failures**
   - Health check failures
   - Load balancer configuration
   - Target group registration
   - Rolling update issues

3. **Performance Issues**
   - Resource contention
   - Network bottlenecks
   - Database connection limits
   - Memory leaks

4. **Scaling Issues**
   - Auto scaling configuration
   - Resource availability
   - Service limits
   - Placement constraints

### Debugging Tools and Techniques

#### ECS Exec
```bash
# Enable ECS Exec for debugging
aws ecs execute-command \
  --cluster production-cluster \
  --task task-id \
  --container app-container \
  --interactive \
  --command "/bin/bash"
```

#### CloudWatch Logs Insights
```sql
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20
```

#### Service Discovery Debugging
```bash
# Check service registration
aws servicediscovery list-services

# Check service instances
aws servicediscovery list-instances \
  --service-id srv-12345
```

## Exam-Specific Tips and Common Scenarios

### Solutions Architect Associate (SAA-C03)
- **Container Orchestration**: ECS vs EKS comparison
- **Launch Types**: Fargate vs EC2 decision criteria
- **Load Balancing**: ALB integration patterns
- **Auto Scaling**: Service scaling strategies

### Solutions Architect Professional (SAP-C02)
- **Multi-Region Deployments**: Cross-region service deployment
- **Hybrid Architectures**: On-premises container integration
- **Advanced Networking**: Service mesh and service discovery
- **Cost Optimization**: Large-scale deployment strategies

### Developer Associate (DVA-C02)
- **CI/CD Integration**: CodePipeline with ECS
- **Blue/Green Deployments**: Deployment strategies
- **Debugging**: ECS Exec and logging
- **Application Architecture**: Microservices patterns

### SysOps Administrator (SOA-C02)
- **Monitoring Setup**: CloudWatch and Container Insights
- **Troubleshooting**: Common operational issues
- **Security Configuration**: IAM and network security
- **Performance Tuning**: Resource optimization

### Common Exam Scenarios

1. **Scenario**: Deploy a web application with auto scaling
   **Solution**: ECS Service with ALB and Auto Scaling

2. **Scenario**: Modernize legacy application
   **Solution**: Containerize and deploy on ECS

3. **Scenario**: Process batch jobs at scale
   **Solution**: ECS with Spot instances for cost optimization

4. **Scenario**: Implement microservices architecture
   **Solution**: ECS with Service Discovery and load balancing

5. **Scenario**: Secure container communication
   **Solution**: VPC, security groups, and service mesh

## Hands-on Examples and CLI Commands

### Cluster Management

```bash
# Create cluster
aws ecs create-cluster \
  --cluster-name production-cluster \
  --capacity-providers EC2 FARGATE \
  --default-capacity-provider-strategy \
    capacityProvider=FARGATE,weight=1,base=0

# List clusters
aws ecs list-clusters

# Describe cluster
aws ecs describe-clusters \
  --clusters production-cluster

# Update cluster
aws ecs update-cluster \
  --cluster production-cluster \
  --configuration executeCommandConfiguration='{
    "kmsKeyId": "alias/aws/ecs",
    "logging": "OVERRIDE",
    "logConfiguration": {
      "cloudWatchLogGroupName": "/aws/ecs/cluster/logs"
    }
  }'

# Delete cluster
aws ecs delete-cluster \
  --cluster production-cluster
```

### Task Definition Management

```bash
# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json

# List task definitions
aws ecs list-task-definitions \
  --family-prefix web-app

# Describe task definition
aws ecs describe-task-definition \
  --task-definition web-app:1

# Deregister task definition
aws ecs deregister-task-definition \
  --task-definition web-app:1
```

### Service Management

```bash
# Create service
aws ecs create-service \
  --cluster production-cluster \
  --service-name web-service \
  --task-definition web-app:1 \
  --desired-count 3 \
  --launch-type FARGATE \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-12345", "subnet-67890"],
      "securityGroups": ["sg-12345"],
      "assignPublicIp": "ENABLED"
    }
  }'

# Update service
aws ecs update-service \
  --cluster production-cluster \
  --service web-service \
  --desired-count 5 \
  --task-definition web-app:2

# List services
aws ecs list-services \
  --cluster production-cluster

# Describe services
aws ecs describe-services \
  --cluster production-cluster \
  --services web-service

# Delete service
aws ecs delete-service \
  --cluster production-cluster \
  --service web-service \
  --force
```

### Task Management

```bash
# Run task
aws ecs run-task \
  --cluster production-cluster \
  --task-definition batch-job:1 \
  --launch-type FARGATE \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-12345"],
      "securityGroups": ["sg-12345"],
      "assignPublicIp": "ENABLED"
    }
  }'

# List tasks
aws ecs list-tasks \
  --cluster production-cluster \
  --service-name web-service

# Describe tasks
aws ecs describe-tasks \
  --cluster production-cluster \
  --tasks task-id

# Stop task
aws ecs stop-task \
  --cluster production-cluster \
  --task task-id \
  --reason "Manual stop"
```

### Auto Scaling Configuration

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/production-cluster/web-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/production-cluster/web-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu-scaling-policy \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
    },
    "ScaleOutCooldown": 300,
    "ScaleInCooldown": 300
  }'

# Describe scaling policies
aws application-autoscaling describe-scaling-policies \
  --service-namespace ecs \
  --resource-id service/production-cluster/web-service
```

### Monitoring and Debugging

```bash
# Get service events
aws ecs describe-services \
  --cluster production-cluster \
  --services web-service \
  --query 'services[0].events'

# Execute command in container
aws ecs execute-command \
  --cluster production-cluster \
  --task task-id \
  --container app-container \
  --interactive \
  --command "/bin/bash"

# Get CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=web-service Name=ClusterName,Value=production-cluster \
  --statistics Average \
  --start-time 2023-01-01T00:00:00Z \
  --end-time 2023-01-01T23:59:59Z \
  --period 3600

# Get container logs
aws logs get-log-events \
  --log-group-name /ecs/web-app \
  --log-stream-name ecs/app-container/task-id
```

### Service Discovery

```bash
# Create service discovery service
aws servicediscovery create-service \
  --name web-service \
  --namespace-id ns-12345 \
  --dns-config '{
    "NamespaceId": "ns-12345",
    "RoutingPolicy": "MULTIVALUE",
    "DnsRecords": [
      {
        "Type": "A",
        "TTL": 60
      }
    ]
  }'

# List service discovery services
aws servicediscovery list-services

# Get service instances
aws servicediscovery get-instances-health-status \
  --service-id srv-12345
```

This comprehensive ECS documentation covers all aspects needed for AWS certification preparation, providing both theoretical knowledge and practical examples for hands-on experience.