# IBM Cloud Advocate (C1000-142, retired) - 8-Week Practice Plan

## Overview

This 8-week structured study plan is designed to prepare you for the IBM Cloud Advocate (C1000-142, retired) certification exam. The plan combines theoretical study with hands-on labs and practice exercises to ensure comprehensive preparation.

**Exam Details:**
- **Exam Code**: C1000-142 (retired 2025-12-31; see the README notice)
- **Duration**: 90 minutes
- **Questions**: 60-70 questions
- **Passing Score**: ~70%
- **Format**: Multiple choice and multiple select
- **Delivery**: Online proctored or test center

---

## Prerequisites

Before starting this study plan, ensure you have:
- [ ] Created a free IBM Cloud account (Lite tier)
- [ ] Installed IBM Cloud CLI on your workstation
- [ ] Basic understanding of cloud computing concepts
- [ ] Familiarity with command line interfaces
- [ ] Access to a computer with internet connection

---

## Week 1: Cloud Fundamentals and IBM Cloud Platform

### Learning Objectives
- Understand cloud computing fundamentals
- Learn IBM Cloud platform architecture
- Explore account management and structure
- Navigate the IBM Cloud Console

### Study Materials
- **Study Notes**: 01-cloud-fundamentals-and-ibm-cloud-overview.md (sections 1-5)
- **IBM Cloud Docs**: [Getting Started with IBM Cloud](https://cloud.ibm.com/docs/overview)
- **IBM Cloud Docs**: [Account Setup](https://cloud.ibm.com/docs/account)

### Hands-On Labs (Week 1)

#### Lab 1.1: Account Setup and Navigation (1 hour)
```bash
# Objectives:
# - Create IBM Cloud account
# - Navigate the IBM Cloud Console
# - Explore the catalog

Tasks:
1. Sign up for IBM Cloud Lite account
2. Complete account verification
3. Tour the IBM Cloud Console
4. Browse the service catalog
5. View account settings and profile
```

#### Lab 1.2: IBM Cloud CLI Basics (2 hours)
```bash
# Install IBM Cloud CLI
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh

# Login to IBM Cloud
ibmcloud login

# Explore basic commands
ibmcloud account list
ibmcloud account show
ibmcloud regions
ibmcloud catalog search

# Install essential plugins
ibmcloud plugin install vpc-infrastructure
ibmcloud plugin install kubernetes-service
ibmcloud plugin install container-registry

# List available services
ibmcloud catalog service-marketplace
```

#### Lab 1.3: Resource Groups and Organization (1.5 hours)
```bash
# Create resource group
ibmcloud resource group-create dev-environment

# Target resource group
ibmcloud target -g dev-environment

# View current target
ibmcloud target

# List all resource groups
ibmcloud resource groups

# Tag resources for organization
ibmcloud resource tag-attach \
  --resource-name my-service \
  --tag-names env:dev,team:engineering
```

### Study Checklist (Week 1)
- [ ] Understand IaaS, PaaS, and SaaS models
- [ ] Know public, private, and hybrid cloud deployment models
- [ ] Familiar with IBM Cloud account types (Lite, Pay-As-You-Go, Subscription)
- [ ] Understand IBM Cloud regions and availability zones
- [ ] Know how to navigate IBM Cloud Console
- [ ] Installed and configured IBM Cloud CLI
- [ ] Created resource groups
- [ ] Applied tags to resources

### Practice Questions (Week 1)
1. What are the five characteristics of cloud computing?
2. What is the difference between a Multi-Zone Region (MZR) and a single-zone data center?
3. Which account type allows you to use IBM Cloud services without a credit card?
4. What is the purpose of resource groups in IBM Cloud?
5. How many availability zones are in an IBM Cloud MZR?

---

## Week 2: Compute and Storage Services

### Learning Objectives
- Understand IBM Cloud compute options
- Learn about storage services
- Practice provisioning virtual servers
- Explore object and block storage

### Study Materials
- **Study Notes**: 02-core-services.md (sections 1-2)
- **IBM Cloud Docs**: [VPC Infrastructure](https://cloud.ibm.com/docs/vpc)
- **IBM Cloud Docs**: [Cloud Object Storage](https://cloud.ibm.com/docs/cloud-object-storage)

### Hands-On Labs (Week 2)

#### Lab 2.1: Virtual Private Cloud (VPC) Setup (2 hours)
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

# Attach gateway to subnet
ibmcloud is subnet-update my-subnet \
  --public-gateway my-pgw

# List VPC resources
ibmcloud is vpcs
ibmcloud is subnets
ibmcloud is public-gateways
```

#### Lab 2.2: Virtual Server Instance (2.5 hours)
```bash
# List available instance profiles
ibmcloud is instance-profiles

# Get SSH key (create if needed)
ibmcloud is keys

# Create SSH key
ibmcloud is key-create my-key @~/.ssh/id_rsa.pub

# Create security group
ibmcloud is security-group-create my-sg my-vpc

# Add SSH rule
ibmcloud is security-group-rule-add my-sg \
  inbound tcp \
  --port-min 22 \
  --port-max 22 \
  --remote 0.0.0.0/0

# Add HTTP rule
ibmcloud is security-group-rule-add my-sg \
  inbound tcp \
  --port-min 80 \
  --port-max 80 \
  --remote 0.0.0.0/0

# Get image ID
ibmcloud is images --visibility public | grep ubuntu

# Create instance
ibmcloud is instance-create my-instance \
  my-vpc \
  us-south-1 \
  bx2-2x8 \
  my-subnet \
  --image <image-id> \
  --keys my-key \
  --security-groups my-sg

# Wait for instance to be running
ibmcloud is instance my-instance

# Create and associate floating IP
ibmcloud is floating-ip-reserve my-ip \
  --zone us-south-1

ibmcloud is instance-network-interface-floating-ip-add \
  my-instance \
  <network-interface-id> \
  my-ip

# SSH to instance
ssh root@<floating-ip>
```

#### Lab 2.3: Cloud Object Storage (2 hours)
```bash
# Create COS instance
ibmcloud resource service-instance-create my-cos \
  cloud-object-storage standard global

# Create service credentials
ibmcloud resource service-key-create my-cos-key \
  --instance-name my-cos \
  --role Writer

# Get credentials
ibmcloud resource service-key my-cos-key

# Install AWS CLI (S3 compatible)
pip install awscli

# Configure AWS CLI with COS credentials
aws configure set aws_access_key_id <access_key_id>
aws configure set aws_secret_access_key <secret_access_key>

# Create bucket
aws s3 mb s3://my-unique-bucket-name \
  --endpoint-url=https://s3.us-south.cloud-object-storage.appdomain.cloud

# Upload file
echo "Hello IBM Cloud" > test.txt
aws s3 cp test.txt s3://my-unique-bucket-name/ \
  --endpoint-url=https://s3.us-south.cloud-object-storage.appdomain.cloud

# List objects
aws s3 ls s3://my-unique-bucket-name/ \
  --endpoint-url=https://s3.us-south.cloud-object-storage.appdomain.cloud

# Download object
aws s3 cp s3://my-unique-bucket-name/test.txt downloaded.txt \
  --endpoint-url=https://s3.us-south.cloud-object-storage.appdomain.cloud
```

### Study Checklist (Week 2)
- [ ] Understand virtual server instance profiles
- [ ] Know when to use bare metal vs virtual servers
- [ ] Familiar with VPC networking concepts
- [ ] Understand security groups vs network ACLs
- [ ] Know Cloud Object Storage use cases and storage classes
- [ ] Understand block storage profiles
- [ ] Provisioned a VPC and subnet
- [ ] Created a virtual server instance
- [ ] Used Cloud Object Storage

### Practice Questions (Week 2)
1. What is the difference between security groups and network ACLs?
2. Which instance profile would you choose for memory-intensive workloads?
3. What are the three storage classes available in Cloud Object Storage?
4. When would you use bare metal servers instead of virtual servers?
5. What is a floating IP in IBM Cloud VPC?

---

## Week 3: Databases and Networking

### Learning Objectives
- Learn about IBM Cloud database services
- Understand advanced networking concepts
- Practice database provisioning
- Configure load balancers

### Study Materials
- **Study Notes**: 02-core-services.md (sections 3-4)
- **IBM Cloud Docs**: [Databases](https://cloud.ibm.com/docs/cloud-databases)
- **IBM Cloud Docs**: [VPC Networking](https://cloud.ibm.com/docs/vpc?topic=vpc-about-networking-for-vpc)

### Hands-On Labs (Week 3)

#### Lab 3.1: IBM Cloudant (NoSQL Database) (2 hours)
```bash
# Create Cloudant instance (Lite plan)
ibmcloud resource service-instance-create my-cloudant \
  cloudantnosqldb lite us-south

# Create credentials
ibmcloud resource service-key-create my-cloudant-key \
  --instance-name my-cloudant \
  --role Manager

# Get connection details
ibmcloud resource service-key my-cloudant-key

# Using curl to interact with Cloudant
# Create database
curl -X PUT https://<username>.cloudantnosqldb.appdomain.cloud/testdb \
  -u <username>:<password>

# Insert document
curl -X POST https://<username>.cloudantnosqldb.appdomain.cloud/testdb \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","age":30}' \
  -u <username>:<password>

# Query all documents
curl -X GET https://<username>.cloudantnosqldb.appdomain.cloud/testdb/_all_docs?include_docs=true \
  -u <username>:<password>

# Create index
curl -X POST https://<username>.cloudantnosqldb.appdomain.cloud/testdb/_index \
  -H "Content-Type: application/json" \
  -d '{"index":{"fields":["name"]},"name":"name-index","type":"json"}' \
  -u <username>:<password>

# Find documents
curl -X POST https://<username>.cloudantnosqldb.appdomain.cloud/testdb/_find \
  -H "Content-Type: application/json" \
  -d '{"selector":{"name":"John Doe"}}' \
  -u <username>:<password>
```

#### Lab 3.2: PostgreSQL Database (1.5 hours)
```bash
# Create PostgreSQL instance (trial plan if available)
ibmcloud resource service-instance-create my-postgres \
  databases-for-postgresql standard us-south \
  -p '{
    "members_memory_allocation_mb": "2048",
    "members_disk_allocation_mb": "10240"
  }'

# Create credentials
ibmcloud resource service-key-create my-postgres-key \
  --instance-name my-postgres \
  --role Administrator

# Get connection string
ibmcloud resource service-key my-postgres-key

# Install PostgreSQL client (if needed)
# Ubuntu/Debian: sudo apt-get install postgresql-client
# macOS: brew install postgresql

# Connect to PostgreSQL
psql "postgres://username:password@host:port/ibmclouddb?sslmode=verify-full"

# Inside psql:
-- Create table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data
INSERT INTO users (name, email) VALUES
  ('Alice', 'alice@example.com'),
  ('Bob', 'bob@example.com');

-- Query data
SELECT * FROM users;

-- Exit
\q
```

#### Lab 3.3: Load Balancer Configuration (2 hours)
```bash
# Prerequisite: Create multiple virtual server instances (Lab 2.2)

# Create application load balancer
ibmcloud is load-balancer-create my-alb \
  --type public \
  --subnet <subnet-id>

# Wait for load balancer to be active
ibmcloud is load-balancer my-alb

# Create backend pool
ibmcloud is load-balancer-pool-create my-pool \
  my-alb \
  round_robin \
  http \
  30 \
  --health-monitor-delay 5 \
  --health-monitor-max-retries 2 \
  --health-monitor-timeout 2 \
  --health-monitor-type http \
  --health-monitor-url /health

# Add pool members (your virtual server instances)
ibmcloud is load-balancer-pool-member-create \
  my-alb \
  my-pool \
  80 \
  <instance1-id>

ibmcloud is load-balancer-pool-member-create \
  my-alb \
  my-pool \
  80 \
  <instance2-id>

# Create listener
ibmcloud is load-balancer-listener-create my-alb \
  80 \
  http \
  --default-pool my-pool

# Get load balancer hostname
ibmcloud is load-balancer my-alb

# Test load balancer
curl http://<load-balancer-hostname>
```

### Study Checklist (Week 3)
- [ ] Understand SQL vs NoSQL database use cases
- [ ] Know when to use Cloudant vs PostgreSQL
- [ ] Familiar with database backup and recovery
- [ ] Understand load balancer types (ALB vs NLB)
- [ ] Know load balancing algorithms
- [ ] Created and used Cloudant database
- [ ] Connected to PostgreSQL database
- [ ] Configured a load balancer

### Practice Questions (Week 3)
1. When would you choose Cloudant over PostgreSQL?
2. What is the purpose of a load balancer health check?
3. What is the difference between an Application Load Balancer and Network Load Balancer?
4. How does IBM Cloud handle database backups?
5. What connection protocol does IBM Cloud enforce for databases?

---

## Week 4: Containers and Kubernetes

### Learning Objectives
- Understand container concepts
- Learn Kubernetes fundamentals
- Practice with IBM Cloud Kubernetes Service
- Explore Container Registry

### Study Materials
- **Study Notes**: 02-core-services.md (sections 5-6)
- **IBM Cloud Docs**: [Kubernetes Service](https://cloud.ibm.com/docs/containers)
- **IBM Cloud Docs**: [Container Registry](https://cloud.ibm.com/docs/Registry)

### Hands-On Labs (Week 4)

#### Lab 4.1: Container Registry (1.5 hours)
```bash
# Install Container Registry plugin
ibmcloud plugin install container-registry

# Login to registry
ibmcloud cr login

# Create namespace
ibmcloud cr namespace-add my-namespace

# List namespaces
ibmcloud cr namespaces

# Build sample Docker image
cat > Dockerfile <<EOF
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

cat > index.html <<EOF
<html>
<body>
<h1>Hello from IBM Cloud!</h1>
</body>
</html>
EOF

# Build image
docker build -t us.icr.io/my-namespace/hello-nginx:v1 .

# Push to registry
docker push us.icr.io/my-namespace/hello-nginx:v1

# List images
ibmcloud cr images

# Scan for vulnerabilities
ibmcloud cr vulnerability-assessment us.icr.io/my-namespace/hello-nginx:v1

# Pull image
docker pull us.icr.io/my-namespace/hello-nginx:v1
```

#### Lab 4.2: Free Kubernetes Cluster (2 hours)
```bash
# Install Kubernetes Service plugin
ibmcloud plugin install kubernetes-service

# Create free cluster (note: limited to 1 per account, expires after 30 days)
ibmcloud ks cluster create classic \
  --name my-free-cluster

# Wait for cluster to be ready (10-20 minutes)
ibmcloud ks cluster get --cluster my-free-cluster

# Download cluster configuration
ibmcloud ks cluster config --cluster my-free-cluster

# Verify kubectl access
kubectl version
kubectl get nodes

# View cluster info
kubectl cluster-info
kubectl get namespaces
```

#### Lab 4.3: Deploy Application to Kubernetes (2.5 hours)
```bash
# Create deployment YAML
cat > deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-nginx
  template:
    metadata:
      labels:
        app: hello-nginx
    spec:
      containers:
      - name: nginx
        image: us.icr.io/my-namespace/hello-nginx:v1
        ports:
        - containerPort: 80
EOF

# Create service YAML
cat > service.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: hello-nginx
spec:
  type: NodePort
  selector:
    app: hello-nginx
  ports:
  - port: 80
    targetPort: 80
EOF

# Apply configuration
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# View pod logs
kubectl logs <pod-name>

# Scale deployment
kubectl scale deployment hello-nginx --replicas=3

# Get service details
kubectl describe service hello-nginx

# Access application (for free cluster, use NodePort)
ibmcloud ks worker ls --cluster my-free-cluster
# Access via http://<worker-public-ip>:<node-port>

# Update deployment
kubectl set image deployment/hello-nginx nginx=us.icr.io/my-namespace/hello-nginx:v2

# Rollback deployment
kubectl rollout undo deployment/hello-nginx

# Delete resources
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
```

### Study Checklist (Week 4)
- [ ] Understand Docker and container concepts
- [ ] Know Kubernetes architecture (pods, deployments, services)
- [ ] Familiar with kubectl commands
- [ ] Understand Container Registry features
- [ ] Know free vs standard Kubernetes clusters
- [ ] Built and pushed Docker image
- [ ] Created Kubernetes cluster
- [ ] Deployed application to Kubernetes

### Practice Questions (Week 4)
1. What is the difference between a Docker image and a container?
2. What is a Kubernetes pod?
3. What is the purpose of a Kubernetes service?
4. How does IBM Cloud Container Registry scan for vulnerabilities?
5. What are the limitations of a free Kubernetes cluster?

---

## Week 5: Serverless and Watson AI

### Learning Objectives
- Understand serverless computing
- Learn about Code Engine and Cloud Functions
- Explore Watson AI services
- Practice with Watson APIs

### Study Materials
- **Study Notes**: 02-core-services.md (section 7) and 03-ai-devops-and-security.md (sections 1-2)
- **IBM Cloud Docs**: [Code Engine](https://cloud.ibm.com/docs/codeengine)
- **IBM Cloud Docs**: [Watson Services](https://cloud.ibm.com/docs/watson)

### Hands-On Labs (Week 5)

#### Lab 5.1: Code Engine Application (2 hours)
```bash
# Install Code Engine plugin
ibmcloud plugin install code-engine

# Create project
ibmcloud ce project create --name my-project

# Select project
ibmcloud ce project select --name my-project

# Deploy application from container image
ibmcloud ce application create --name hello-app \
  --image icr.io/codeengine/hello \
  --min-scale 0 \
  --max-scale 5 \
  --cpu 0.25 \
  --memory 0.5G

# Get application URL
ibmcloud ce application get --name hello-app

# Test application
curl <application-url>

# View logs
ibmcloud ce application logs --name hello-app

# Update application
ibmcloud ce application update --name hello-app \
  --min-scale 1 \
  --max-scale 10

# Create job
cat > job.sh <<'EOF'
#!/bin/bash
echo "Starting batch job..."
for i in {1..10}; do
  echo "Processing item $i"
  sleep 1
done
echo "Batch job complete!"
EOF

# Build job image (requires Dockerfile)
cat > Dockerfile <<'EOF'
FROM alpine:latest
COPY job.sh /job.sh
RUN chmod +x /job.sh
CMD ["/job.sh"]
EOF

# Build and push
docker build -t us.icr.io/my-namespace/batch-job:v1 .
docker push us.icr.io/my-namespace/batch-job:v1

# Create Code Engine job
ibmcloud ce job create --name batch-job \
  --image us.icr.io/my-namespace/batch-job:v1

# Run job
ibmcloud ce jobrun submit --job batch-job

# View job runs
ibmcloud ce jobrun list

# View job logs
ibmcloud ce jobrun logs --jobrun <jobrun-name>
```

#### Lab 5.2: Watson Assistant (2 hours)
```bash
# Create Watson Assistant instance (Lite plan)
ibmcloud resource service-instance-create my-assistant \
  conversation lite us-south

# Create service credentials
ibmcloud resource service-key-create my-assistant-key \
  --instance-name my-assistant \
  --role Manager

# Get credentials
ibmcloud resource service-key my-assistant-key --output json

# Install Watson SDK (Python example)
pip install ibm-watson

# Create Python script
cat > watson_assistant_test.py <<'EOF'
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Replace with your credentials
authenticator = IAMAuthenticator('YOUR_API_KEY')
assistant = AssistantV2(
    version='2023-06-15',
    authenticator=authenticator
)
assistant.set_service_url('YOUR_SERVICE_URL')

# Create session
session = assistant.create_session(
    assistant_id='YOUR_ASSISTANT_ID'
).get_result()
print(f"Session ID: {session['session_id']}")

# Send message
response = assistant.message(
    assistant_id='YOUR_ASSISTANT_ID',
    session_id=session['session_id'],
    input={
        'message_type': 'text',
        'text': 'Hello'
    }
).get_result()

print(f"Response: {response['output']['generic'][0]['text']}")

# Delete session
assistant.delete_session(
    assistant_id='YOUR_ASSISTANT_ID',
    session_id=session['session_id']
)
EOF

# Note: Configure assistant through web UI first
# https://cloud.ibm.com/services/conversation/my-assistant
```

#### Lab 5.3: Watson NLU (1.5 hours)
```bash
# Create Watson NLU instance (Lite plan)
ibmcloud resource service-instance-create my-nlu \
  natural-language-understanding free us-south

# Create credentials
ibmcloud resource service-key-create my-nlu-key \
  --instance-name my-nlu \
  --role Manager

# Get credentials
ibmcloud resource service-key my-nlu-key --output json

# Create Python script
cat > watson_nlu_test.py <<'EOF'
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Replace with your credentials
authenticator = IAMAuthenticator('YOUR_API_KEY')
nlu = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)
nlu.set_service_url('YOUR_SERVICE_URL')

# Analyze text
text = """
IBM Cloud is a suite of cloud computing services from IBM that offers
both platform as a service (PaaS) and infrastructure as a service (IaaS).
With IBM Cloud, you can build, deploy, and manage applications securely
across multiple regions worldwide.
"""

response = nlu.analyze(
    text=text,
    features=Features(
        entities=EntitiesOptions(sentiment=True, limit=5),
        keywords=KeywordsOptions(sentiment=True, limit=5),
        sentiment=SentimentOptions()
    )
).get_result()

print("Overall Sentiment:", response['sentiment']['document']['label'])
print("\nEntities:")
for entity in response['entities']:
    print(f"- {entity['text']} ({entity['type']})")

print("\nKeywords:")
for keyword in response['keywords']:
    print(f"- {keyword['text']} (relevance: {keyword['relevance']})")
EOF

python watson_nlu_test.py
```

### Study Checklist (Week 5)
- [ ] Understand serverless computing benefits
- [ ] Know difference between Code Engine and Cloud Functions
- [ ] Familiar with Watson AI service categories
- [ ] Understand Watson Assistant concepts
- [ ] Know Watson NLU capabilities
- [ ] Deployed Code Engine application
- [ ] Created and ran Code Engine job
- [ ] Used Watson Assistant API
- [ ] Analyzed text with Watson NLU

### Practice Questions (Week 5)
1. What is the main benefit of serverless computing?
2. When would you use Code Engine vs Cloud Functions?
3. Which Watson service would you use to build a chatbot?
4. What types of insights can Watson NLU extract from text?
5. What does "scale to zero" mean in Code Engine?

---

## Week 6: DevOps and Infrastructure as Code

### Learning Objectives
- Understand DevOps practices
- Learn Infrastructure as Code with Terraform
- Explore IBM Cloud Schematics
- Practice CI/CD concepts

### Study Materials
- **Study Notes**: 03-ai-devops-and-security.md (sections 3-5)
- **IBM Cloud Docs**: [Schematics](https://cloud.ibm.com/docs/schematics)
- **IBM Cloud Docs**: [Continuous Delivery](https://cloud.ibm.com/docs/ContinuousDelivery)

### Hands-On Labs (Week 6)

#### Lab 6.1: Terraform Basics (2 hours)
```bash
# Install Terraform (if not already installed)
# macOS: brew install terraform
# Linux: Download from terraform.io

# Create Terraform configuration
mkdir terraform-lab
cd terraform-lab

cat > main.tf <<'EOF'
terraform {
  required_providers {
    ibm = {
      source = "IBM-Cloud/ibm"
      version = "~> 1.58"
    }
  }
}

provider "ibm" {
  region = "us-south"
  ibmcloud_api_key = var.ibmcloud_api_key
}

variable "ibmcloud_api_key" {
  description = "IBM Cloud API Key"
  type        = string
  sensitive   = true
}

variable "resource_group_id" {
  description = "Resource Group ID"
  type        = string
}

# Create Object Storage instance
resource "ibm_resource_instance" "cos" {
  name              = "my-terraform-cos"
  service           = "cloud-object-storage"
  plan              = "lite"
  location          = "global"
  resource_group_id = var.resource_group_id
}

# Output instance details
output "cos_instance_id" {
  value = ibm_resource_instance.cos.id
}
EOF

cat > terraform.tfvars <<EOF
ibmcloud_api_key = "YOUR_API_KEY"
resource_group_id = "YOUR_RESOURCE_GROUP_ID"
EOF

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply configuration
terraform apply

# View state
terraform show

# Destroy resources
terraform destroy
```

#### Lab 6.2: IBM Cloud Schematics (2 hours)
```bash
# Create GitHub repository with Terraform config or use existing one

# Create Schematics workspace
ibmcloud schematics workspace new \
  --name my-workspace \
  --location us-south \
  --resource-group default \
  --github-url https://github.com/IBM-Cloud/terraform-provider-ibm/tree/master/examples/ibm-resource-instance \
  --terraform-version 1.5

# Get workspace ID
ibmcloud schematics workspace list

# Pull latest from Git
ibmcloud schematics workspace update --id <workspace-id>

# Generate plan
ibmcloud schematics plan --id <workspace-id>

# Check plan status
ibmcloud schematics workspace get --id <workspace-id>

# Apply plan
ibmcloud schematics apply --id <workspace-id>

# View outputs
ibmcloud schematics workspace output --id <workspace-id>

# View state
ibmcloud schematics state list --id <workspace-id>

# Destroy resources
ibmcloud schematics destroy --id <workspace-id>

# Delete workspace
ibmcloud schematics workspace delete --id <workspace-id>
```

#### Lab 6.3: Simple CI/CD Pipeline (1.5 hours)
```bash
# Create a simple Node.js application
mkdir myapp
cd myapp

cat > package.json <<'EOF'
{
  "name": "myapp",
  "version": "1.0.0",
  "description": "Simple app for CI/CD",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "test": "echo \"Running tests...\" && exit 0"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
EOF

cat > server.js <<'EOF'
const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

app.get('/', (req, res) => {
  res.send('Hello from IBM Cloud CI/CD!');
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
EOF

# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Create repository on GitHub/GitLab
# Push code to repository

# Create toolchain in IBM Cloud Console
# https://cloud.ibm.com/devops/create
# Select "Develop a Kubernetes app" template
# Configure Git repository
# Configure delivery pipeline
# Deploy to Code Engine or Kubernetes
```

### Study Checklist (Week 6)
- [ ] Understand Infrastructure as Code benefits
- [ ] Know Terraform basics (resources, providers, state)
- [ ] Familiar with Schematics features
- [ ] Understand CI/CD pipeline stages
- [ ] Know DevOps best practices
- [ ] Created Terraform configuration
- [ ] Used Schematics to deploy infrastructure
- [ ] Explored toolchain creation

### Practice Questions (Week 6)
1. What is Infrastructure as Code (IaC)?
2. What is the purpose of Terraform state?
3. How does IBM Cloud Schematics differ from running Terraform locally?
4. What are the typical stages in a CI/CD pipeline?
5. Why is version control important in DevOps?

---

## Week 7: Security and Compliance

### Learning Objectives
- Understand IAM concepts
- Learn about encryption and key management
- Explore security services
- Practice access control

### Study Materials
- **Study Notes**: 03-ai-devops-and-security.md (sections 6-8)
- **IBM Cloud Docs**: [IAM](https://cloud.ibm.com/docs/account?topic=account-iamoverview)
- **IBM Cloud Docs**: [Key Protect](https://cloud.ibm.com/docs/key-protect)

### Hands-On Labs (Week 7)

#### Lab 7.1: IAM Users and Access Groups (2 hours)
```bash
# Create service ID
ibmcloud iam service-id-create my-app-service \
  --description "Service ID for my application"

# Create API key for service ID
ibmcloud iam service-api-key-create my-app-key my-app-service \
  --description "API key for CI/CD" \
  --file service-key.json

# View service IDs
ibmcloud iam service-ids

# Create access group
ibmcloud iam access-group-create developers \
  --description "Developer access group"

# Add user to access group
ibmcloud iam access-group-user-add developers your-email@example.com

# Add service ID to access group
ibmcloud iam access-group-service-id-add developers my-app-service

# Create policy for access group
ibmcloud iam access-group-policy-create developers \
  --roles Viewer,Operator \
  --resource-group-name development

# Create resource-specific policy
ibmcloud iam access-group-policy-create developers \
  --roles Editor \
  --service-name kubernetes \
  --resource-group-name development

# List policies
ibmcloud iam access-group-policies developers

# View access group details
ibmcloud iam access-group developers

# Remove user from access group
ibmcloud iam access-group-user-remove developers your-email@example.com
```

#### Lab 7.2: Key Protect (1.5 hours)
```bash
# Create Key Protect instance
ibmcloud resource service-instance-create my-key-protect \
  kms tiered-pricing us-south

# Get instance ID
KP_INSTANCE_ID=$(ibmcloud resource service-instance my-key-protect --output json | jq -r '.[0].guid')

# Install Key Protect plugin
ibmcloud plugin install key-protect

# Create root key
ibmcloud kp create my-root-key \
  --instance-id $KP_INSTANCE_ID \
  --description "Root key for encryption"

# List keys
ibmcloud kp list --instance-id $KP_INSTANCE_ID

# Get key ID
KEY_ID=$(ibmcloud kp list --instance-id $KP_INSTANCE_ID --output json | jq -r '.[0].id')

# Wrap (encrypt) a data encryption key
DEK=$(echo "my-secret-data-encryption-key" | base64)
ibmcloud kp wrap $KEY_ID \
  --instance-id $KP_INSTANCE_ID \
  --plaintext $DEK

# Rotate key
ibmcloud kp rotate $KEY_ID \
  --instance-id $KP_INSTANCE_ID

# Enable key for deletion (requires 4 authorizations in production)
ibmcloud kp enable-delete $KEY_ID \
  --instance-id $KP_INSTANCE_ID
```

#### Lab 7.3: Secrets Manager (1.5 hours)
```bash
# Create Secrets Manager instance
ibmcloud resource service-instance-create my-secrets-manager \
  secrets-manager trial us-south

# Get instance ID
SM_INSTANCE_ID=$(ibmcloud resource service-instance my-secrets-manager --output json | jq -r '.[0].guid')

# Install Secrets Manager plugin
ibmcloud plugin install secrets-manager

# Set target instance
ibmcloud secrets-manager config set instance-id $SM_INSTANCE_ID

# Create arbitrary secret
ibmcloud secrets-manager secret-create \
  --secret-type arbitrary \
  --name "database-password" \
  --description "Production database password" \
  --secret-data '{"password":"super-secret-password"}'

# Create IAM credentials (dynamic)
ibmcloud secrets-manager secret-create \
  --secret-type iam_credentials \
  --name "dynamic-api-key" \
  --description "Dynamic API key for application" \
  --service-id <service-id>

# List secrets
ibmcloud secrets-manager secrets

# Get secret value
ibmcloud secrets-manager secret \
  --secret-type arbitrary \
  --id <secret-id>

# Update secret
ibmcloud secrets-manager secret-update \
  --secret-type arbitrary \
  --id <secret-id> \
  --secret-data '{"password":"new-password"}'

# Delete secret
ibmcloud secrets-manager secret-delete \
  --secret-type arbitrary \
  --id <secret-id>
```

### Study Checklist (Week 7)
- [ ] Understand IAM users, service IDs, and access groups
- [ ] Know platform vs service roles
- [ ] Familiar with Key Protect and encryption concepts
- [ ] Understand Secrets Manager use cases
- [ ] Know compliance certifications
- [ ] Created service IDs and API keys
- [ ] Created access groups and policies
- [ ] Used Key Protect for encryption
- [ ] Managed secrets in Secrets Manager

### Practice Questions (Week 7)
1. What is the difference between a user and a service ID?
2. What are the four platform access roles in IBM Cloud IAM?
3. What is the purpose of IBM Cloud Key Protect?
4. What types of secrets can Secrets Manager store?
5. What compliance certification is required for payment card processing?

---

## Week 8: Monitoring, Review, and Practice Exam

### Learning Objectives
- Learn monitoring and logging
- Review all topics
- Take practice exams
- Identify weak areas

### Study Materials
- **Study Notes**: All sections (review)
- **IBM Cloud Docs**: [Monitoring](https://cloud.ibm.com/docs/monitoring)
- **IBM Cloud Docs**: [Logging](https://cloud.ibm.com/docs/cloud-logs)

### Hands-On Labs (Week 8)

#### Lab 8.1: Monitoring Setup (1.5 hours)
```bash
# Create Monitoring instance
ibmcloud resource service-instance-create my-monitoring \
  sysdig-monitor graduated-tier us-south

# Configure platform metrics
ibmcloud ob monitoring config create \
  --instance my-monitoring

# Access monitoring dashboard
ibmcloud ob monitoring dashboard open --instance my-monitoring

# Explore:
# - Default dashboards
# - Kubernetes metrics (if cluster deployed)
# - Custom dashboards
# - Alerts configuration
```

#### Lab 8.2: Logging Setup (1.5 hours)
```bash
# Create Logging instance
ibmcloud resource service-instance-create my-logging \
  logdna 7-day us-south

# Configure platform logs
ibmcloud ob logging config create \
  --instance my-logging

# Access logging dashboard
ibmcloud ob logging dashboard open --instance my-logging

# Explore:
# - Log sources
# - Search and filtering
# - Views creation
# - Alerts setup
```

#### Lab 8.3: Comprehensive Review Exercise (3 hours)

Deploy a complete multi-tier application:

```bash
# 1. Create VPC infrastructure
# 2. Deploy PostgreSQL database
# 3. Create Kubernetes cluster
# 4. Build and push container image
# 5. Deploy application to Kubernetes
# 6. Configure load balancer
# 7. Set up IAM policies
# 8. Enable encryption with Key Protect
# 9. Configure monitoring and logging
# 10. Create backup strategy

# This exercise combines all concepts from previous weeks
# Refer to individual lab exercises for specific commands
```

### Review Schedule (Week 8)

**Monday-Tuesday: Topic Review**
- Review all study notes
- Focus on weak areas identified
- Practice CLI commands
- Review hands-on lab exercises

**Wednesday-Thursday: Practice Exams**
- Take online practice exams
- Review incorrect answers
- Understand reasoning behind correct answers
- Note recurring topics

**Friday: Final Review**
- Review exam tips from study notes
- Memorize key concepts
- Practice sample questions
- Review IBM Cloud documentation

**Weekend: Rest and Light Review**
- Light review of notes
- Relax and prepare mentally
- Ensure exam environment is ready
- Review exam logistics

### Study Checklist (Week 8)
- [ ] Understand monitoring and logging services
- [ ] Know Activity Tracker purpose
- [ ] Reviewed all study notes
- [ ] Completed all hands-on labs
- [ ] Took practice exams
- [ ] Identified and studied weak areas
- [ ] Memorized key concepts
- [ ] Ready for exam

### Comprehensive Review Questions

**Cloud Fundamentals:**
1. List the five characteristics of cloud computing
2. Compare IaaS, PaaS, and SaaS with examples
3. What is the difference between public, private, and hybrid cloud?

**IBM Cloud Platform:**
4. What are the advantages of Multi-Zone Regions?
5. Name three IBM Cloud differentiators
6. What account type offers committed spending with discounts?

**Compute:**
7. When would you choose bare metal over virtual servers?
8. List three virtual server instance profile types
9. What is IBM Cloud Satellite used for?

**Storage:**
10. What are the three Cloud Object Storage classes?
11. When would you use File Storage over Block Storage?
12. What IOPS profile should you use for high-performance databases?

**Databases:**
13. When would you choose Cloudant over PostgreSQL?
14. What protocol must be used for database connections?
15. How does IBM Cloud handle database backups?

**Networking:**
16. What is the difference between Security Groups and Network ACLs?
17. What are the two types of load balancers in IBM Cloud?
18. What is Direct Link used for?

**Containers:**
19. What is the minimum worker node count for production Kubernetes?
20. What is the difference between IKS and OpenShift?
21. How does Container Registry scan images?

**Serverless:**
22. What does "scale to zero" mean in Code Engine?
23. When would you use Code Engine vs Cloud Functions?
24. What is the difference between a Code Engine app and job?

**Watson AI:**
25. Which Watson service would you use for a chatbot?
26. What can Watson NLU extract from text?
27. What is Watson Discovery used for?

**DevOps:**
28. What is Infrastructure as Code?
29. What are the benefits of using Schematics over local Terraform?
30. Name three stages of a typical CI/CD pipeline

**Security:**
31. What is the difference between a user and a service ID?
32. List the four platform access roles
33. What is Key Protect used for?
34. What types of secrets can Secrets Manager store?

**Monitoring:**
35. What is the difference between Monitoring and Logging?
36. What is Activity Tracker used for?
37. What type of data does Activity Tracker record?

---

## Additional Resources

### Official IBM Resources
- **IBM Cloud Documentation**: https://cloud.ibm.com/docs
- **IBM Cloud Blog**: https://www.ibm.com/cloud/blog
- **IBM Cloud Architecture Center**: https://www.ibm.com/cloud/architecture
- **IBM Developer**: https://developer.ibm.com/
- **IBM Cloud YouTube Channel**: Search "IBM Cloud" on YouTube

### Training Courses
- IBM Cloud Essentials (Free)
- IBM Cloud Technical Advocate (Free)
- Cloud Core certification prep
- Service-specific courses on IBM Skills Network

### Practice Exams
- IBM Cloud certification practice tests
- Online quiz platforms
- Study group practice questions

### Community
- IBM Cloud Community forums
- Stack Overflow (tag: ibm-cloud)
- Reddit: r/IBMCloud
- LinkedIn IBM Cloud groups
- Local IBM Cloud meetups

### Books and Guides
- IBM Cloud Architecture Center guides
- IBM Redbooks
- Service-specific documentation

---

## Exam Day Preparation

### One Week Before
- [ ] Confirm exam date and time
- [ ] Test computer and internet connection (for online proctored)
- [ ] Prepare identification documents
- [ ] Review exam policies
- [ ] Do final review of weak areas

### Day Before
- [ ] Light review only (avoid cramming)
- [ ] Get good sleep
- [ ] Prepare exam environment
- [ ] Gather required materials

### Exam Day
- [ ] Eat a good meal
- [ ] Arrive early (test center) or log in early (online)
- [ ] Read questions carefully
- [ ] Manage time (90 minutes for 60-70 questions)
- [ ] Flag uncertain questions for review
- [ ] Review all answers if time permits

### During Exam
- Read each question completely
- Eliminate obviously wrong answers
- Look for keywords in questions
- Don't overthink simple questions
- Manage your time wisely
- Stay calm and confident

---

## Post-Exam

### If You Pass
- Celebrate your achievement!
- Download digital badge
- Update LinkedIn profile
- Share on social media
- Consider next certification

### If You Don't Pass
- Don't be discouraged
- Review exam report
- Identify weak areas
- Study those specific topics
- Retake when ready

---

## Final Tips

1. **Hands-on practice is crucial** - Don't just read, do the labs
2. **Use the free tier extensively** - Real experience is invaluable
3. **Focus on understanding concepts** - Not just memorization
4. **Practice with CLI** - Many questions involve CLI commands
5. **Know when to use each service** - Use cases are important
6. **Understand IBM Cloud differentiators** - What makes IBM Cloud unique
7. **Review exam objectives** - Ensure you cover all topics
8. **Join study groups** - Learn from others
9. **Stay updated** - Cloud services evolve rapidly
10. **Believe in yourself** - You've got this!

---

Good luck with your IBM Cloud Advocate certification exam! Remember, this certification is just the beginning of your IBM Cloud journey. Continue learning, practicing, and exploring the platform even after you pass the exam.
