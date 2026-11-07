# IBM Cloud Advocate (C1000-176): Core Services

## Table of Contents
1. [Compute Services](#compute-services)
2. [Storage Services](#storage-services)
3. [Database Services](#database-services)
4. [Networking Services](#networking-services)
5. [Container Services](#container-services)
6. [Kubernetes and OpenShift](#kubernetes-and-openshift)
7. [Serverless Computing](#serverless-computing)
8. [Service Integration Patterns](#service-integration-patterns)
9. [High Availability and Disaster Recovery](#high-availability-and-disaster-recovery)
10. [Exam Tips](#exam-tips)

---

## Compute Services

### Virtual Servers for VPC

Virtual Servers for VPC provide resizable compute capacity in IBM Cloud's Virtual Private Cloud.

**Key Features:**
- Multiple profiles: Balanced, Compute, Memory, Very High Memory, GPU
- Hourly or monthly billing
- Boot from custom images
- Attached block storage volumes
- Multiple network interfaces
- Security groups for firewall rules

**Instance Profiles:**

```
Balanced Profiles (bx2):
- Balanced CPU-to-memory ratio
- General purpose workloads
- Examples: bx2-2x8, bx2-4x16, bx2-8x32

Compute Profiles (cx2):
- Higher CPU-to-memory ratio
- Compute-intensive workloads
- Examples: cx2-2x4, cx2-4x8, cx2-8x16

Memory Profiles (mx2):
- Higher memory-to-CPU ratio
- Memory-intensive workloads
- Examples: mx2-2x16, mx2-4x32, mx2-8x64

Ultra High Memory Profiles (ux2):
- Very high memory-to-CPU ratio
- In-memory databases, SAP HANA
- Examples: ux2-8x224, ux2-16x448

GPU Profiles (gx2):
- GPU acceleration
- AI/ML, rendering, simulation
- Examples: gx2-8x64x1v100, gx2-16x128x2v100
```

**Provisioning a Virtual Server:**

```bash
# List available instance profiles
ibmcloud is instance-profiles

# Create a virtual server instance
ibmcloud is instance-create my-instance \
  <vpc-id> \
  us-south-1 \
  bx2-2x8 \
  <subnet-id> \
  --image <image-id> \
  --keys <ssh-key-id>

# List instances
ibmcloud is instances

# Get instance details
ibmcloud is instance my-instance

# Start/Stop instance
ibmcloud is instance-stop my-instance
ibmcloud is instance-start my-instance

# Delete instance
ibmcloud is instance-delete my-instance
```

**Use Cases:**
- Web and application servers
- Development and testing environments
- Enterprise applications
- Batch processing
- General purpose computing

### Bare Metal Servers

Single-tenant physical servers offering maximum performance and control.

**Key Features:**
- No hypervisor overhead
- Direct hardware access
- High I/O performance
- Dedicated resources
- Hourly or monthly billing
- RAID configurations

**Server Profiles:**
- **Compute**: High-frequency processors
- **Memory**: Large RAM configurations
- **Storage**: High-capacity storage
- **GPU**: Graphics processing units
- **SAP Certified**: SAP HANA workloads

**Provisioning Bare Metal:**

```bash
# List available bare metal profiles
ibmcloud sl hardware create-options

# Order a bare metal server
ibmcloud sl hardware create \
  --hostname my-bare-metal \
  --domain example.com \
  --datacenter dal13 \
  --server <server-key> \
  --key <ssh-key-id> \
  --os UBUNTU_20_64

# List bare metal servers
ibmcloud sl hardware list

# Get server details
ibmcloud sl hardware detail <server-id>
```

**Use Cases:**
- High-performance computing (HPC)
- Big data analytics
- Large databases
- Regulatory compliance requiring dedicated hardware
- Gaming servers

### Power Systems Virtual Servers

IBM Power Systems infrastructure in the cloud.

**Key Features:**
- AIX, IBM i, and Linux support
- High reliability (99.95% SLA)
- Enterprise-class performance
- Flexible sizing (0.25 to 32 cores)
- Integration with IBM Cloud services

**Advantages:**
- Migrate IBM Power workloads to cloud
- Hybrid cloud for IBM i and AIX
- Disaster recovery for Power Systems
- Development and testing environments

**Use Cases:**
- AIX application hosting
- IBM i (AS/400) modernization
- SAP on Power
- Oracle databases on Power
- Core banking systems

### VMware Solutions

Seamlessly integrate VMware workloads with IBM Cloud.

**Offerings:**

1. **VMware Shared**: Tenant-based VMware infrastructure
2. **VMware Dedicated**: Single-tenant vCenter instances
3. **VMware as a Service**: Fully managed VMware environment

**Key Features:**
- Native VMware tools (vSphere, vCenter, NSX, vSAN)
- Migrate existing VMware workloads
- Hybrid cloud with on-premises VMware
- Disaster recovery capabilities

**Use Cases:**
- VMware workload migration
- Data center extension
- Disaster recovery
- Hybrid cloud architectures

---

## Storage Services

### Cloud Object Storage

Highly scalable and durable object storage for unstructured data.

**Key Features:**
- 99.999999999% (11 9's) durability
- Unlimited scalability
- Multiple storage classes
- Built-in encryption
- Immutable object versioning
- S3 API compatibility

**Storage Classes:**

```
Standard:
- Frequently accessed data
- Low latency access
- Higher cost per GB

Vault:
- Archive and backup
- Infrequent access
- Lower storage cost

Cold Vault:
- Long-term archive
- Rare access
- Lowest storage cost

Smart Tier:
- Automatic tier optimization
- Based on access patterns
- Cost optimization
```

**Regional Options:**
- **Regional**: Single region, highest availability
- **Cross-Region**: Replicated across multiple regions
- **Single Data Center**: Single location, lower cost

**Working with Object Storage:**

```bash
# Install and configure AWS CLI (S3 compatible)
aws configure set aws_access_key_id <access_key>
aws configure set aws_secret_access_key <secret_key>

# Create a bucket
aws s3 mb s3://my-bucket \
  --endpoint-url=https://s3.us-south.cloud-object-storage.appdomain.cloud

# Upload an object
aws s3 cp myfile.txt s3://my-bucket/ \
  --endpoint-url=https://s3.us-south.cloud-object-storage.appdomain.cloud

# List objects
aws s3 ls s3://my-bucket/ \
  --endpoint-url=https://s3.us-south.cloud-object-storage.appdomain.cloud

# Download an object
aws s3 cp s3://my-bucket/myfile.txt ./ \
  --endpoint-url=https://s3.us-south.cloud-object-storage.appdomain.cloud

# Delete an object
aws s3 rm s3://my-bucket/myfile.txt \
  --endpoint-url=https://s3.us-south.cloud-object-storage.appdomain.cloud
```

**Use Cases:**
- Backup and disaster recovery
- Content distribution
- Big data analytics
- Media storage and streaming
- Application data storage
- Regulatory compliance archives

### Block Storage for VPC

High-performance block storage for Virtual Servers for VPC.

**Key Features:**
- Provisioned IOPS
- Multiple profiles (general purpose, 5, 10 IOPS/GB)
- Up to 16 TB per volume
- Encryption at rest
- Volume snapshots
- Boot and data volumes

**Storage Profiles:**

```
General Purpose:
- 3 IOPS per GB
- Balanced performance
- Most workloads

5iops-tier:
- 5 IOPS per GB
- Higher performance
- Database workloads

10iops-tier:
- 10 IOPS per GB
- Highest performance
- High-performance databases

Custom:
- Define exact IOPS (100-48000)
- Fine-grained control
- Specific performance requirements
```

**Managing Block Storage:**

```bash
# Create a block storage volume
ibmcloud is volume-create my-volume \
  10iops-tier \
  us-south-1 \
  --capacity 100

# Attach volume to instance
ibmcloud is instance-volume-attachment-add \
  my-attachment \
  my-instance \
  my-volume

# Create a snapshot
ibmcloud is snapshot-create my-snapshot \
  --source-volume my-volume

# List volumes
ibmcloud is volumes

# Delete volume
ibmcloud is volume-delete my-volume
```

**Use Cases:**
- Boot volumes for virtual servers
- Database storage
- Application data
- High I/O workloads
- Persistent container storage

### File Storage for VPC

NFS-based shared file storage for VPC environments.

**Key Features:**
- NFS v4.1 protocol
- Shared access across multiple instances
- Multiple profiles (3, 5, 10 IOPS/GB)
- Up to 32 TB per share
- Encryption at rest
- Mount targets in different zones

**Storage Profiles:**
- Similar to Block Storage (3, 5, 10 IOPS/GB tiers)
- Choose based on performance requirements

**Managing File Storage:**

```bash
# Create a file share
ibmcloud is share-create my-share \
  dp2 \
  us-south-1 \
  --size 100

# Create mount target
ibmcloud is share-mount-target-create my-target \
  my-share \
  <subnet-id>

# Get mount path
ibmcloud is share-mount-target my-share my-target

# Mount on instance (Linux)
sudo mount -t nfs4 -o sec=sys,vers=4.1 \
  <mount-path> /mnt/myshare
```

**Use Cases:**
- Shared application data
- Content management systems
- Media workflows
- Development environments
- High-performance computing (HPC)

---

## Database Services

### IBM Cloudant

Fully managed NoSQL JSON document database based on Apache CouchDB.

**Key Features:**
- JSON document storage
- HTTP API access
- Built-in replication
- Offline-first sync
- MapReduce and Mango queries
- Multi-master replication
- Global distribution

**Data Model:**
```json
{
  "_id": "user123",
  "_rev": "1-abc123",
  "name": "John Doe",
  "email": "john@example.com",
  "created": "2024-01-01T00:00:00Z",
  "tags": ["developer", "ibm-cloud"]
}
```

**Working with Cloudant:**

```bash
# Create Cloudant instance
ibmcloud resource service-instance-create my-cloudant \
  cloudantnosqldb \
  standard \
  us-south

# Get service credentials
ibmcloud resource service-key-create my-key \
  --instance-name my-cloudant

# HTTP API examples (using curl)
# Create a database
curl -X PUT https://<username>.cloudant.com/mydb \
  -u <username>:<password>

# Insert a document
curl -X POST https://<username>.cloudant.com/mydb \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}' \
  -u <username>:<password>

# Query documents
curl -X GET https://<username>.cloudant.com/mydb/_all_docs \
  -u <username>:<password>

# Find documents with Mango query
curl -X POST https://<username>.cloudant.com/mydb/_find \
  -H "Content-Type: application/json" \
  -d '{"selector":{"name":"John Doe"}}' \
  -u <username>:<password>
```

**Use Cases:**
- Mobile and web applications
- IoT data storage
- Content management
- User profile data
- Offline-first applications
- Multi-region data distribution

### Databases for PostgreSQL

Fully managed PostgreSQL database service.

**Key Features:**
- Latest PostgreSQL versions
- Automated backups
- Point-in-time recovery
- High availability with auto-failover
- Encryption at rest and in transit
- Private endpoints
- Horizontal and vertical scaling

**Plans:**
- **Standard**: Single-zone deployment
- **Enterprise**: Multi-zone deployment with HA

**Provisioning PostgreSQL:**

```bash
# Create PostgreSQL instance
ibmcloud resource service-instance-create my-postgres \
  databases-for-postgresql \
  standard \
  us-south \
  -p '{
    "members_memory_allocation_mb": "4096",
    "members_disk_allocation_mb": "20480"
  }'

# Get connection strings
ibmcloud resource service-key-create my-postgres-key \
  --instance-name my-postgres

# Connect using psql
psql "postgres://username:password@host:port/ibmclouddb?sslmode=verify-full"
```

**Common Operations:**

```sql
-- Create database
CREATE DATABASE myapp;

-- Create table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

-- Query data
SELECT * FROM users WHERE name LIKE 'John%';

-- Create index
CREATE INDEX idx_users_email ON users(email);
```

**Use Cases:**
- Transactional applications
- Data warehousing
- Geospatial applications
- Analytics workloads
- Enterprise applications

### Databases for MySQL

Fully managed MySQL database service.

**Key Features:**
- MySQL 8.0 support
- Automated backups
- High availability
- Read replicas
- Private endpoints
- Monitoring and alerts

**Use Cases:**
- Web applications
- E-commerce platforms
- Content management systems
- SaaS applications

### Databases for MongoDB

Fully managed MongoDB database service.

**Key Features:**
- MongoDB 4.4+ support
- Replica sets for HA
- Automated backups
- Point-in-time recovery
- Horizontal scaling
- Private endpoints

**Working with MongoDB:**

```javascript
// Node.js example
const { MongoClient } = require('mongodb');

const uri = "mongodb://username:password@host:port/admin?ssl=true";
const client = new MongoClient(uri);

async function run() {
  try {
    await client.connect();
    const database = client.db('myapp');
    const collection = database.collection('users');

    // Insert document
    await collection.insertOne({
      name: "John Doe",
      email: "john@example.com",
      created: new Date()
    });

    // Find documents
    const users = await collection.find({ name: "John Doe" }).toArray();
    console.log(users);
  } finally {
    await client.close();
  }
}
```

**Use Cases:**
- Real-time analytics
- Content management
- Mobile applications
- IoT data storage
- Catalog management

### Databases for Redis

Fully managed Redis in-memory data store.

**Key Features:**
- Redis 6.0+ support
- High availability
- Automatic failover
- Persistence options
- Pub/Sub messaging
- Lua scripting

**Common Redis Operations:**

```bash
# Connect to Redis
redis-cli -h <host> -p <port> -a <password> --tls

# Set/Get values
SET user:1 "John Doe"
GET user:1

# Hash operations
HSET user:1 name "John Doe" email "john@example.com"
HGET user:1 name
HGETALL user:1

# List operations
LPUSH mylist "item1" "item2"
LRANGE mylist 0 -1

# Set operations
SADD myset "value1" "value2"
SMEMBERS myset

# Pub/Sub
PUBLISH mychannel "Hello World"
SUBSCRIBE mychannel

# Expire keys
SETEX session:1 3600 "session-data"
```

**Use Cases:**
- Caching layer
- Session storage
- Real-time analytics
- Leaderboards and counting
- Message queuing
- Rate limiting

### Db2 on Cloud

Fully managed Db2 relational database.

**Key Features:**
- Enterprise-grade SQL database
- Oracle compatibility
- High availability
- Automatic backups
- In-memory acceleration
- Multi-version concurrency control

**Use Cases:**
- Enterprise applications
- Data warehousing
- OLTP workloads
- Migration from on-premises Db2
- SAP workloads

---

## Networking Services

### Virtual Private Cloud (VPC)

Isolated network environments in IBM Cloud.

**Key Components:**

1. **VPC**: Isolated network space
2. **Subnets**: Network segments within VPC
3. **Public Gateway**: Internet access for private subnets
4. **Floating IPs**: Static public IP addresses
5. **Security Groups**: Instance-level firewall
6. **Network ACLs**: Subnet-level firewall

**Creating a VPC:**

```bash
# Create VPC
ibmcloud is vpc-create my-vpc \
  --address-prefix-management manual

# Create address prefix
ibmcloud is vpc-address-prefix-create my-prefix \
  my-vpc \
  us-south-1 \
  10.240.0.0/24

# Create subnet
ibmcloud is subnet-create my-subnet \
  my-vpc \
  --ipv4-cidr-block 10.240.0.0/24 \
  --zone us-south-1

# Create public gateway
ibmcloud is public-gateway-create my-pgw \
  my-vpc \
  us-south-1

# Attach public gateway to subnet
ibmcloud is subnet-update my-subnet \
  --public-gateway my-pgw

# Create security group
ibmcloud is security-group-create my-sg my-vpc

# Add security group rule
ibmcloud is security-group-rule-add my-sg \
  inbound tcp \
  --port-min 443 \
  --port-max 443 \
  --remote 0.0.0.0/0
```

**Security Groups vs Network ACLs:**

```
Security Groups:
- Instance level
- Stateful (return traffic automatic)
- Allow rules only
- Applied to network interfaces

Network ACLs:
- Subnet level
- Stateless (must define both directions)
- Allow and deny rules
- Rule priority order
- Applied to entire subnet
```

**Use Cases:**
- Isolated network environments
- Multi-tier applications
- Hybrid cloud connectivity
- Regulatory compliance
- Development/test isolation

### Load Balancers

Distribute traffic across multiple instances.

**Types:**

1. **Application Load Balancer (ALB)**: Layer 7, HTTP/HTTPS
2. **Network Load Balancer (NLB)**: Layer 4, TCP/UDP

**Application Load Balancer Features:**
- SSL/TLS termination
- Cookie-based session affinity
- Health checks
- Multi-zone support
- Private and public options

**Creating a Load Balancer:**

```bash
# Create application load balancer
ibmcloud is load-balancer-create my-alb \
  --type public \
  --subnet <subnet-id> \
  --subnet <subnet-id-zone2>

# Create backend pool
ibmcloud is load-balancer-pool-create my-pool \
  my-alb \
  round_robin \
  http \
  30 \
  --health-monitor-delay 5 \
  --health-monitor-max-retries 2 \
  --health-monitor-timeout 2 \
  --health-monitor-type http

# Add pool members
ibmcloud is load-balancer-pool-member-create \
  my-alb \
  my-pool \
  443 \
  <instance-id>

# Create listener
ibmcloud is load-balancer-listener-create my-alb \
  443 \
  https \
  --default-pool my-pool \
  --certificate-instance <cert-crn>
```

**Use Cases:**
- High availability
- Traffic distribution
- SSL offloading
- Zero-downtime deployments
- Auto-scaling architectures

### Direct Link

Dedicated private connectivity to IBM Cloud.

**Options:**

1. **Direct Link Dedicated**: Single-tenant, 1-10 Gbps
2. **Direct Link Connect**: Multi-tenant via partners, 50 Mbps - 5 Gbps

**Benefits:**
- Low latency
- Higher throughput
- Secure private connection
- Bypass public internet
- Hybrid cloud connectivity

**Use Cases:**
- Hybrid cloud architectures
- Large data transfers
- Latency-sensitive applications
- Regulatory compliance
- Data center extension

### Content Delivery Network (CDN)

Global content distribution for fast delivery.

**Features:**
- Global points of presence
- Dynamic and static content
- SSL/TLS support
- Origin pull
- Purge cache
- Analytics and reporting

**Use Cases:**
- Website acceleration
- Video streaming
- Software distribution
- API acceleration
- Mobile app content

### Transit Gateway

Connect multiple VPCs and on-premises networks.

**Features:**
- Hub-and-spoke topology
- Multi-region connectivity
- Classic infrastructure connection
- Direct Link integration
- Route filtering

**Use Cases:**
- Multi-VPC architectures
- Centralized network management
- Hybrid cloud connectivity
- Microservices networking

---

## Container Services

### IBM Cloud Container Registry

Private container image registry.

**Key Features:**
- Private and public namespaces
- Vulnerability Advisor integration
- Image signing and verification
- Garbage collection
- Geographic regions

**Working with Container Registry:**

```bash
# Install Container Registry plugin
ibmcloud plugin install container-registry

# Login to registry
ibmcloud cr login

# Create a namespace
ibmcloud cr namespace-add my-namespace

# List namespaces
ibmcloud cr namespaces

# Build and push an image
docker build -t us.icr.io/my-namespace/myapp:v1 .
docker push us.icr.io/my-namespace/myapp:v1

# List images
ibmcloud cr images

# Scan for vulnerabilities
ibmcloud cr vulnerability-assessment us.icr.io/my-namespace/myapp:v1

# Delete an image
ibmcloud cr image-rm us.icr.io/my-namespace/myapp:v1
```

**Use Cases:**
- Store application images
- CI/CD pipelines
- Kubernetes deployments
- Security scanning
- Version control

---

## Kubernetes and OpenShift

### IBM Cloud Kubernetes Service (IKS)

Managed Kubernetes service for container orchestration.

**Key Features:**
- Managed control plane
- Worker node pools
- Multi-zone clusters
- Integrated with IBM Cloud services
- Istio service mesh
- Knative serverless
- Built-in monitoring and logging

**Cluster Types:**

```
Free Cluster:
- Single worker node
- 2 vCPU, 4 GB RAM
- 30-day expiration
- Learning and testing

Standard Cluster:
- Multiple worker nodes
- Various profiles available
- Production-ready
- HA control plane (multi-zone)
- Full feature set
```

**Creating a Kubernetes Cluster:**

```bash
# Install Kubernetes Service plugin
ibmcloud plugin install kubernetes-service

# Create a cluster
ibmcloud ks cluster create vpc-gen2 \
  --name my-cluster \
  --zone us-south-1 \
  --version 1.28 \
  --flavor bx2.4x16 \
  --workers 3 \
  --vpc-id <vpc-id> \
  --subnet-id <subnet-id>

# List clusters
ibmcloud ks clusters

# Get cluster details
ibmcloud ks cluster get --cluster my-cluster

# Download cluster config
ibmcloud ks cluster config --cluster my-cluster

# Verify kubectl access
kubectl get nodes
```

**Common Kubernetes Operations:**

```bash
# Deploy an application
kubectl create deployment nginx --image=nginx:latest

# Expose as a service
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Scale deployment
kubectl scale deployment nginx --replicas=5

# Get pods
kubectl get pods

# Get services
kubectl get services

# View logs
kubectl logs <pod-name>

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash

# Delete deployment
kubectl delete deployment nginx
```

**Use Cases:**
- Microservices architectures
- CI/CD deployments
- Stateful applications
- Batch processing
- Machine learning workloads

### Red Hat OpenShift on IBM Cloud

Enterprise Kubernetes platform with developer and operational tools.

**Key Features:**
- Built on Kubernetes
- Integrated CI/CD (Tekton)
- Developer console
- Operator Hub
- Built-in registry
- Service mesh (Istio)
- Serverless (Knative)
- Enterprise security

**OpenShift vs Kubernetes:**

```
OpenShift Advantages:
- Integrated developer tools
- Built-in image registry
- Source-to-Image (S2I)
- Enterprise support
- Security policies
- Operator ecosystem
- Web console

Kubernetes:
- More flexible
- Lighter weight
- Broader ecosystem
- Lower cost
```

**Creating an OpenShift Cluster:**

```bash
# Install OpenShift plugin
ibmcloud plugin install container-service

# Create OpenShift cluster
ibmcloud oc cluster create vpc-gen2 \
  --name my-openshift \
  --zone us-south-1 \
  --version 4.13_openshift \
  --flavor bx2.4x16 \
  --workers 3 \
  --vpc-id <vpc-id> \
  --subnet-id <subnet-id>

# Get cluster configuration
ibmcloud oc cluster config --cluster my-openshift --admin

# Login to OpenShift
oc login --token=<token> --server=<server-url>

# Create a project
oc new-project myapp

# Deploy from source
oc new-app https://github.com/username/myapp.git

# Expose service
oc expose svc/myapp
```

**Use Cases:**
- Enterprise container platform
- DevOps and CI/CD
- Hybrid cloud applications
- Regulated industries
- Multi-tenant environments

---

## Serverless Computing

### IBM Cloud Code Engine

Fully managed serverless platform for containers, batch jobs, and functions.

**Key Features:**
- Auto-scaling to zero
- Pay only when running
- Support for containers and source code
- Batch jobs
- Event-driven architecture
- Built-in CI/CD
- Private and public endpoints

**Code Engine Concepts:**

```
Projects: Isolation boundary for resources

Applications:
- Long-running HTTP services
- Scale based on requests
- Custom domains and TLS

Jobs:
- One-time or scheduled tasks
- Batch processing
- No HTTP endpoint

Builds:
- Build container images from source
- Dockerfile or buildpacks
- Store in Container Registry
```

**Working with Code Engine:**

```bash
# Install Code Engine plugin
ibmcloud plugin install code-engine

# Create a project
ibmcloud ce project create --name my-project

# Select project
ibmcloud ce project select --name my-project

# Deploy application from container
ibmcloud ce application create --name myapp \
  --image us.icr.io/my-namespace/myapp:v1 \
  --min-scale 0 \
  --max-scale 10

# Deploy from source code
ibmcloud ce application create --name myapp \
  --build-source https://github.com/username/myapp.git \
  --strategy buildpacks

# Create a job
ibmcloud ce job create --name myjob \
  --image us.icr.io/my-namespace/batch:v1

# Run a job
ibmcloud ce jobrun submit --job myjob

# List applications
ibmcloud ce application list

# Get application URL
ibmcloud ce application get --name myapp

# View logs
ibmcloud ce application logs --name myapp
```

**Use Cases:**
- Microservices and APIs
- Batch processing
- Event-driven workflows
- CI/CD pipelines
- Data processing
- Scheduled tasks

### IBM Cloud Functions

> **Legacy service:** IBM publishes migration guidance for moving off IBM Cloud Functions (OpenWhisk); its target is IBM Code Engine ([IBM: How to move from IBM Cloud Functions to IBM Code Engine](https://www.ibm.com/products/tutorials/how-to-move-from-ibm-cloud-functions-to-ibm-code-engine)). Treat the Cloud Functions material below as the legacy model.

Event-driven serverless compute based on Apache OpenWhisk.

**Key Features:**
- Function as a Service (FaaS)
- Multiple language support (Node.js, Python, Go, Java, PHP, Ruby, .NET)
- Event triggers
- Sequences and compositions
- API Gateway integration
- Built-in packages

**Cloud Functions Concepts:**

```
Actions: Individual functions
Triggers: Named channels for events
Rules: Connect triggers to actions
Packages: Group related actions
Sequences: Chain actions together
```

**Working with Cloud Functions:**

```bash
# Install Cloud Functions plugin
ibmcloud plugin install cloud-functions

# Create a function (action)
ibmcloud fn action create hello hello.js

# Invoke function
ibmcloud fn action invoke hello --result

# Create function with parameters
ibmcloud fn action invoke hello \
  --param name World \
  --result

# Create trigger
ibmcloud fn trigger create myTrigger

# Create rule (connect trigger to action)
ibmcloud fn rule create myRule myTrigger hello

# Fire trigger
ibmcloud fn trigger fire myTrigger --param name World

# List actions
ibmcloud fn action list

# View activation logs
ibmcloud fn activation list
ibmcloud fn activation logs <activation-id>
```

**Example Function:**

```javascript
// hello.js
function main(params) {
  const name = params.name || 'World';
  return { message: `Hello, ${name}!` };
}
```

**Use Cases:**
- Event processing
- API backends
- Scheduled tasks
- Data transformation
- IoT event handling
- Webhooks

---

## Service Integration Patterns

### Common Integration Patterns

**1. Microservices Architecture:**
```
Frontend (Code Engine/OpenShift)
    ↓
API Gateway
    ↓
Microservices (Kubernetes/Code Engine)
    ↓
Databases (PostgreSQL, MongoDB, Redis)
    ↓
Object Storage (COS)
```

**2. Event-Driven Architecture:**
```
Event Sources
    ↓
Event Streams (Kafka)
    ↓
Cloud Functions / Code Engine
    ↓
Databases / Storage
```

**3. Batch Processing:**
```
Object Storage (input)
    ↓
Code Engine Jobs
    ↓
Databases for PostgreSQL
    ↓
Object Storage (output)
```

### Service Binding

Connect applications to IBM Cloud services.

```bash
# Kubernetes service binding
ibmcloud ks cluster service bind \
  --cluster my-cluster \
  --namespace default \
  --service my-cloudant

# Code Engine service binding
ibmcloud ce application bind --name myapp \
  --service-instance my-postgres

# OpenShift service binding
oc create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secret
```

---

## High Availability and Disaster Recovery

### High Availability Strategies

**1. Multi-Zone Deployment:**
```
Zone 1          Zone 2          Zone 3
App Instance    App Instance    App Instance
    ↓               ↓               ↓
        Load Balancer
              ↓
           Database
         (Primary)    (Replicas)
```

**2. Auto-Scaling:**
- Horizontal Pod Autoscaler (Kubernetes)
- Code Engine auto-scaling
- Virtual Server auto-scale groups

**3. Load Balancing:**
- Application Load Balancer
- Global Load Balancer
- DNS-based load balancing

### Disaster Recovery

**Backup Strategies:**

1. **Database Backups:**
   - Automated daily backups
   - Point-in-time recovery
   - Cross-region replication

2. **Object Storage:**
   - Cross-region buckets
   - Versioning
   - Immutable objects

3. **Virtual Servers:**
   - Image snapshots
   - Block storage snapshots
   - Backup to Object Storage

**Recovery Objectives:**
- **RTO** (Recovery Time Objective): How quickly to recover
- **RPO** (Recovery Point Objective): Acceptable data loss

---

## Exam Tips

### Key Concepts to Master

**Compute:**
- Virtual Server profiles and use cases
- Bare Metal vs Virtual Servers
- Power Systems for AIX/IBM i workloads
- VMware Solutions for migration

**Storage:**
- Object Storage classes and use cases
- Block Storage IOPS profiles
- File Storage for shared access
- When to use each storage type

**Databases:**
- SQL vs NoSQL decision factors
- Cloudant for JSON documents
- PostgreSQL for relational data
- Redis for caching and sessions
- MongoDB for flexible schemas

**Networking:**
- VPC components and architecture
- Security Groups vs Network ACLs
- Load balancer types and features
- Direct Link for hybrid cloud

**Containers:**
- Kubernetes vs OpenShift
- When to use managed Kubernetes
- Container Registry for images
- Multi-zone cluster benefits

**Serverless:**
- Code Engine vs Cloud Functions
- When to use serverless
- Auto-scaling benefits
- Event-driven architectures

### Sample Questions

**Q1:** Which storage service should you use for storing container images?
- A) Object Storage
- **B) Container Registry** ✓
- C) Block Storage
- D) File Storage

**Q2:** What is the minimum number of worker nodes required for a production Kubernetes cluster?
- A) 1
- B) 2
- **C) 3** ✓
- D) 5

**Q3:** Which database service is best for storing JSON documents with HTTP API access?
- A) Databases for PostgreSQL
- **B) IBM Cloudant** ✓
- C) Db2 on Cloud
- D) Databases for MySQL

**Q4:** What is the difference between Security Groups and Network ACLs?
- A) No difference
- B) ACLs are instance-level, Security Groups are subnet-level
- **C) Security Groups are instance-level, ACLs are subnet-level** ✓
- D) Both are the same level

**Q5:** Which service provides serverless container hosting?
- A) Cloud Functions
- **B) Code Engine** ✓
- C) Kubernetes Service
- D) Cloud Foundry

### Hands-On Practice

```bash
# Practice scenario: Deploy a multi-tier application

# 1. Create VPC and networking
ibmcloud is vpc-create demo-vpc
ibmcloud is subnet-create demo-subnet demo-vpc \
  --ipv4-cidr-block 10.240.0.0/24 --zone us-south-1

# 2. Provision database
ibmcloud resource service-instance-create demo-db \
  databases-for-postgresql standard us-south

# 3. Create Kubernetes cluster
ibmcloud ks cluster create vpc-gen2 --name demo-cluster \
  --zone us-south-1 --flavor bx2.4x16 --workers 3

# 4. Deploy application
kubectl create deployment webapp --image=nginx
kubectl expose deployment webapp --port=80 --type=LoadBalancer

# 5. Setup storage
ibmcloud resource service-instance-create demo-storage \
  cloud-object-storage standard global

# Cleanup
kubectl delete deployment webapp
ibmcloud ks cluster rm --cluster demo-cluster
ibmcloud resource service-instance-delete demo-db
ibmcloud is vpc-delete demo-vpc
```

### Final Checklist

- [ ] Understand all compute options and use cases
- [ ] Know storage types and when to use each
- [ ] Familiar with database services and selection criteria
- [ ] Understand VPC networking components
- [ ] Know Security Groups vs Network ACLs
- [ ] Familiar with Kubernetes and OpenShift differences
- [ ] Understand serverless options (Code Engine, Functions)
- [ ] Know high availability patterns
- [ ] Practiced provisioning various services via CLI
- [ ] Understand service integration patterns

---

Success in understanding IBM Cloud's core services requires hands-on practice. Create a free account and experiment with different services to build practical experience. Focus on understanding when to use each service and how they integrate together to build complete solutions.
