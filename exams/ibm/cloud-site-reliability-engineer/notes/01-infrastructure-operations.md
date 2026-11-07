# IBM Cloud Site Reliability Engineer (C1000-179) - Infrastructure & Operations

## Table of Contents
- [Infrastructure as Code](#infrastructure-as-code)
- [VPC Management](#vpc-management)
- [Compute Resource Management](#compute-resource-management)
- [Storage Operations](#storage-operations)
- [Container Orchestration](#container-orchestration)
- [Automation and Scripting](#automation-and-scripting)
- [Cost Optimization](#cost-optimization)

---

## Infrastructure as Code

### Terraform Fundamentals
```hcl
# main.tf - Multi-tier infrastructure
terraform {
  required_providers {
    ibm = {
      source  = "IBM-Cloud/ibm"
      version = "~> 1.60"
    }
  }
  
  backend "s3" {
    bucket = "terraform-state"
    key    = "production/terraform.tfstate"
    region = "us-south"
  }
}

provider "ibm" {
  ibmcloud_api_key = var.ibmcloud_api_key
  region           = var.region
}

# Resource Group
resource "ibm_resource_group" "prod" {
  name = "production"
}

# VPC with multiple zones
resource "ibm_is_vpc" "prod_vpc" {
  name                      = "prod-vpc"
  resource_group            = ibm_resource_group.prod.id
  address_prefix_management = "manual"
  tags                      = ["production", "terraform"]
}

resource "ibm_is_vpc_address_prefix" "zone_prefixes" {
  count = 3
  vpc   = ibm_is_vpc.prod_vpc.id
  zone  = "us-south-${count.index + 1}"
  cidr  = "10.24${count.index}.0.0/16"
}

# Subnets per zone
resource "ibm_is_subnet" "web_tier" {
  count           = 3
  name            = "web-tier-zone-${count.index + 1}"
  vpc             = ibm_is_vpc.prod_vpc.id
  zone            = "us-south-${count.index + 1}"
  ipv4_cidr_block = "10.24${count.index}.0.0/24"
  public_gateway  = ibm_is_public_gateway.gateways[count.index].id
}

resource "ibm_is_public_gateway" "gateways" {
  count = 3
  name  = "gateway-zone-${count.index + 1}"
  vpc   = ibm_is_vpc.prod_vpc.id
  zone  = "us-south-${count.index + 1}"
}

# Load Balancer
resource "ibm_is_lb" "app_lb" {
  name    = "prod-alb"
  subnets = ibm_is_subnet.web_tier[*].id
  type    = "public"
  profile = "network-fixed"
  
  logging {
    datapath = true
  }
}

# Auto Scale Group
resource "ibm_is_instance_template" "web_template" {
  name    = "web-server-template"
  image   = data.ibm_is_image.ubuntu.id
  profile = "bx2-2x8"
  
  primary_network_interface {
    subnet          = ibm_is_subnet.web_tier[0].id
    security_groups = [ibm_is_security_group.web_sg.id]
  }
  
  vpc  = ibm_is_vpc.prod_vpc.id
  zone = "us-south-1"
  keys = [ibm_is_ssh_key.deployer_key.id]
  
  user_data = file("${path.module}/scripts/web-init.sh")
}

resource "ibm_is_instance_group" "web_group" {
  name              = "web-instance-group"
  instance_template = ibm_is_instance_template.web_template.id
  instance_count    = 3
  subnets           = ibm_is_subnet.web_tier[*].id
  load_balancer     = ibm_is_lb.app_lb.id
  load_balancer_pool = ibm_is_lb_pool.web_pool.id
  
  application_port = 443
}

resource "ibm_is_instance_group_manager" "web_manager" {
  name                 = "web-autoscale-manager"
  aggregation_window   = 90
  instance_group       = ibm_is_instance_group.web_group.id
  cooldown             = 300
  manager_type         = "autoscale"
  enable_manager       = true
  max_membership_count = 10
  min_membership_count = 3
}

resource "ibm_is_instance_group_manager_policy" "cpu_policy" {
  instance_group         = ibm_is_instance_group.web_group.id
  instance_group_manager = ibm_is_instance_group_manager.web_manager.manager_id
  metric_type            = "cpu"
  metric_value           = 70
  policy_type            = "target"
}

# Databases
resource "ibm_database" "postgresql" {
  name              = "prod-postgresql"
  plan              = "standard"
  location          = "us-south"
  service           = "databases-for-postgresql"
  resource_group_id = ibm_resource_group.prod.id
  
  adminpassword = var.db_admin_password
  
  group {
    group_id = "member"
    members {
      allocation_count = 3
    }
    memory {
      allocation_mb = 4096
    }
    disk {
      allocation_mb = 20480
    }
    cpu {
      allocation_count = 6
    }
  }
  
  backup_schedule {
    start_time = "02:00"
    frequency  = "daily"
  }
  
  point_in_time_recovery {
    enabled = true
  }
}

# Cloud Object Storage
resource "ibm_resource_instance" "cos" {
  name              = "prod-cos"
  service           = "cloud-object-storage"
  plan              = "standard"
  location          = "global"
  resource_group_id = ibm_resource_group.prod.id
}

resource "ibm_cos_bucket" "prod_bucket" {
  bucket_name          = "prod-application-data"
  resource_instance_id = ibm_resource_instance.cos.id
  region_location      = "us-south"
  storage_class        = "standard"
  
  object_versioning {
    enable = true
  }
  
  retention_rule {
    default   = 90
    maximum   = 365
    minimum   = 30
    permanent = false
  }
}
```

### Terraform Modules
```hcl
# modules/vpc/main.tf
variable "name" {}
variable "resource_group_id" {}
variable "zones" { default = 3 }

resource "ibm_is_vpc" "vpc" {
  name                      = var.name
  resource_group            = var.resource_group_id
  address_prefix_management = "manual"
}

resource "ibm_is_vpc_address_prefix" "prefixes" {
  count = var.zones
  vpc   = ibm_is_vpc.vpc.id
  zone  = "us-south-${count.index + 1}"
  cidr  = "10.24${count.index}.0.0/16"
}

output "vpc_id" {
  value = ibm_is_vpc.vpc.id
}

output "vpc_crn" {
  value = ibm_is_vpc.vpc.crn
}
```

---

## VPC Management

### CLI Operations
```bash
# Create VPC with all tiers
ibmcloud is vpc-create prod-vpc --resource-group-name production

# Create subnets across zones
for zone in 1 2 3; do
  ibmcloud is subnet-create web-tier-zone-$zone \
    $VPC_ID us-south-$zone \
    --ipv4-cidr-block 10.24${zone}.0.0/24
    
  ibmcloud is subnet-create app-tier-zone-$zone \
    $VPC_ID us-south-$zone \
    --ipv4-cidr-block 10.24${zone}.1.0/24
    
  ibmcloud is subnet-create data-tier-zone-$zone \
    $VPC_ID us-south-$zone \
    --ipv4-cidr-block 10.24${zone}.2.0/24
done

# Create public gateways
for zone in 1 2 3; do
  ibmcloud is public-gateway-create gateway-zone-$zone \
    $VPC_ID us-south-$zone
done

# Attach gateways to web tier subnets
ibmcloud is subnet-update web-tier-zone-1 --public-gateway-id $GW_ID

# View VPC details
ibmcloud is vpc $VPC_ID --output json | jq

# List all VPC resources
ibmcloud is subnets --vpc $VPC_ID
ibmcloud is instances --vpc $VPC_ID
ibmcloud is lbs --vpc $VPC_ID
```

### Python SDK for VPC Operations
```python
# vpc_operations.py
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_vpc import VpcV1

authenticator = IAMAuthenticator(api_key)
vpc_service = VpcV1(authenticator=authenticator)
vpc_service.set_service_url('https://us-south.iaas.cloud.ibm.com/v1')

def list_vpc_resources(vpc_id):
    # List instances
    instances = vpc_service.list_instances(vpc_id=vpc_id).get_result()
    print(f"Instances: {len(instances['instances'])}")
    
    # List subnets
    subnets = vpc_service.list_subnets(vpc_id=vpc_id).get_result()
    print(f"Subnets: {len(subnets['subnets'])}")
    
    # List load balancers
    lbs = vpc_service.list_load_balancers(vpc_id=vpc_id).get_result()
    print(f"Load Balancers: {len(lbs['load_balancers'])}")
    
    return {
        'instances': instances['instances'],
        'subnets': subnets['subnets'],
        'load_balancers': lbs['load_balancers']
    }

def get_instance_health(instance_id):
    instance = vpc_service.get_instance(id=instance_id).get_result()
    return {
        'status': instance['status'],
        'health': instance.get('health_state', 'unknown'),
        'cpu': instance['vcpu']['count'],
        'memory': instance['memory']
    }
```

---

## Compute Resource Management

### VSI Management
```bash
# Create instance with monitoring
ibmcloud is instance-create web-server-1 \
  $VPC_ID us-south-1 bx2-2x8 \
  $SUBNET_ID \
  --image $IMAGE_ID \
  --keys $SSH_KEY_ID \
  --security-groups $SG_ID \
  --resource-group-name production \
  --user-data @init-script.sh

# Update instance
ibmcloud is instance-update web-server-1 --name web-server-prod-1

# Resize instance (requires stop)
ibmcloud is instance-stop web-server-1
ibmcloud is instance-update web-server-1 --profile bx2-4x16
ibmcloud is instance-start web-server-1

# Create instance snapshot
ibmcloud is instance-volume-attachment-add web-server-1 \
  --volume $VOLUME_ID
ibmcloud is snapshot-create web-server-snapshot \
  --source-volume $VOLUME_ID

# Instance console access
ibmcloud is instance-console web-server-1

# Bulk operations
for i in {1..5}; do
  ibmcloud is instance-create web-server-$i \
    $VPC_ID us-south-1 bx2-2x8 $SUBNET_ID \
    --image $IMAGE_ID --keys $SSH_KEY_ID &
done
wait

# List and filter instances
ibmcloud is instances --output json | \
  jq '.[] | select(.status=="running") | {name, id, status}'
```

### Instance Groups and Auto-Scaling
```bash
# Create instance template
ibmcloud is instance-template-create web-template \
  --image $IMAGE_ID \
  --profile bx2-2x8 \
  --vpc $VPC_ID \
  --subnet $SUBNET_ID \
  --security-groups $SG_ID

# Create instance group
ibmcloud is instance-group-create web-group \
  --instance-template $TEMPLATE_ID \
  --subnet $SUBNET_1,$SUBNET_2,$SUBNET_3 \
  --membership-count 3 \
  --load-balancer $LB_ID \
  --load-balancer-pool $POOL_ID

# Create autoscale manager
ibmcloud is instance-group-manager-create web-group \
  --manager-type autoscale \
  --max-membership-count 10 \
  --min-membership-count 3 \
  --cooldown 300

# Add scaling policy
ibmcloud is instance-group-manager-policy-create \
  web-group $MANAGER_ID \
  --metric-type cpu \
  --metric-value 70 \
  --policy-type target

# Manual scaling
ibmcloud is instance-group-update web-group \
  --membership-count 5
```

### Kubernetes Management
```bash
# Create IKS cluster
ibmcloud ks cluster create vpc-gen2 \
  --name prod-cluster \
  --version 1.28 \
  --zone us-south-1 \
  --vpc-id $VPC_ID \
  --subnet-id $SUBNET_ID \
  --flavor bx2.4x16 \
  --workers 3

# Add worker pool
ibmcloud ks worker-pool create vpc-gen2 \
  --name app-pool \
  --cluster prod-cluster \
  --flavor bx2.8x32 \
  --size-per-zone 2 \
  --vpc-id $VPC_ID

# Enable autoscaling
ibmcloud ks cluster autoscale-set \
  --cluster prod-cluster \
  --enable \
  --min 3 \
  --max 10

# Upgrade cluster
ibmcloud ks cluster master update \
  --cluster prod-cluster \
  --version 1.29

# Replace worker nodes
ibmcloud ks worker replace \
  --cluster prod-cluster \
  --worker $WORKER_ID

# Get cluster config
ibmcloud ks cluster config --cluster prod-cluster

# Manage add-ons
ibmcloud ks cluster addon enable vpc-block-csi-driver \
  --cluster prod-cluster
```

---

## Storage Operations

### Block Storage
```bash
# Create volume with snapshot
ibmcloud is volume-create data-volume-1 \
  --profile general-purpose \
  --capacity 500 \
  --zone us-south-1 \
  --resource-group-name production \
  --encryption-key $KEY_CRN

# Attach to instance
ibmcloud is instance-volume-attachment-add \
  web-server-1 \
  --volume data-volume-1 \
  --auto-delete true

# Create snapshot
ibmcloud is snapshot-create backup-snapshot-1 \
  --source-volume data-volume-1

# Create volume from snapshot
ibmcloud is volume-create restored-volume \
  --snapshot backup-snapshot-1 \
  --profile general-purpose

# Update volume size (expand only)
ibmcloud is volume-update data-volume-1 --capacity 1000
```

### Object Storage Operations
```bash
# Create bucket with lifecycle policy
ibmcloud cos bucket-create backup-bucket \
  --ibm-service-instance-id $COS_ID \
  --region us-south \
  --class standard

# Enable versioning
ibmcloud cos bucket-versioning-put \
  --bucket backup-bucket \
  --versioning-configuration Status=Enabled

# Set lifecycle policy
cat > lifecycle.json << 'LIFECYCLE'
{
  "Rules": [{
    "Status": "Enabled",
    "Filter": {"Prefix": "logs/"},
    "Transition": {"Days": 30, "StorageClass": "GLACIER"},
    "Expiration": {"Days": 90}
  }]
}
LIFECYCLE
ibmcloud cos bucket-lifecycle-put \
  --bucket backup-bucket \
  --lifecycle-configuration file://lifecycle.json

# Upload with multipart
ibmcloud cos upload --bucket backup-bucket \
  --key database-backup.tar.gz \
  --file backup.tar.gz \
  --part-size 100

# Sync directory
ibmcloud cos sync ./logs/ s3://backup-bucket/logs/
```

---

## Container Orchestration

### Kubernetes Operations
```yaml
# deployment-with-hpa.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
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
                  - api
              topologyKey: kubernetes.io/hostname
      containers:
      - name: api
        image: us.icr.io/namespace/api:latest
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
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
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
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 1
        periodSeconds: 60
```

### Persistent Storage
```yaml
# persistent-volume.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: ibmc-vpc-block-general-purpose
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
spec:
  serviceName: postgresql
  replicas: 3
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:15
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: ibmc-vpc-block-general-purpose
      resources:
        requests:
          storage: 100Gi
```

---

## Automation and Scripting

### Bash Automation
```bash
#!/bin/bash
# infrastructure-health-check.sh

VPC_ID="vpc-12345"
SLACK_WEBHOOK="https://hooks.slack.com/services/XXX"

check_instances() {
    echo "Checking instance health..."
    instances=$(ibmcloud is instances --vpc $VPC_ID --output json)
    
    unhealthy=$(echo "$instances" | jq -r '.[] | select(.status!="running") | .name')
    
    if [ -n "$unhealthy" ]; then
        echo "Unhealthy instances: $unhealthy"
        notify "Warning: Unhealthy instances detected: $unhealthy"
    fi
}

check_load_balancers() {
    echo "Checking load balancers..."
    lbs=$(ibmcloud is lbs --vpc $VPC_ID --output json)
    
    for lb in $(echo "$lbs" | jq -r '.[] | @base64'); do
        _jq() {
            echo ${lb} | base64 --decode | jq -r ${1}
        }
        
        lb_id=$(_jq '.id')
        lb_name=$(_jq '.name')
        
        pools=$(ibmcloud is lb-pools $lb_id --output json)
        
        for pool in $(echo "$pools" | jq -r '.[] | @base64'); do
            pool_health=$(echo ${pool} | base64 --decode | jq -r '.health_monitor.health')
            
            if [ "$pool_health" != "ok" ]; then
                notify "Warning: LB $lb_name pool unhealthy"
            fi
        done
    done
}

check_vpn_status() {
    echo "Checking VPN connections..."
    vpns=$(ibmcloud is vpn-gateways --output json)
    
    for vpn in $(echo "$vpns" | jq -r '.[] | @base64'); do
        _jq() {
            echo ${vpn} | base64 --decode | jq -r ${1}
        }
        
        vpn_id=$(_jq '.id')
        connections=$(ibmcloud is vpn-gateway-connections $vpn_id --output json)
        
        for conn in $(echo "$connections" | jq -r '.[] | @base64'); do
            status=$(echo ${conn} | base64 --decode | jq -r '.status')
            
            if [ "$status" != "up" ]; then
                conn_name=$(echo ${conn} | base64 --decode | jq -r '.name')
                notify "Critical: VPN connection $conn_name is down"
            fi
        done
    done
}

notify() {
    message=$1
    curl -X POST $SLACK_WEBHOOK \
        -H 'Content-Type: application/json' \
        -d "{\"text\": \"$message\"}"
}

# Run checks
check_instances
check_load_balancers
check_vpn_status

echo "Health check complete"
```

### Python Automation
```python
# auto_remediation.py
import time
from ibm_vpc import VpcV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class InfrastructureMonitor:
    def __init__(self, api_key):
        authenticator = IAMAuthenticator(api_key)
        self.vpc_service = VpcV1(authenticator=authenticator)
        self.vpc_service.set_service_url('https://us-south.iaas.cloud.ibm.com/v1')
    
    def check_instance_health(self, vpc_id):
        instances = self.vpc_service.list_instances(vpc_id=vpc_id).get_result()
        
        for instance in instances['instances']:
            if instance['status'] != 'running':
                self.remediate_instance(instance)
    
    def remediate_instance(self, instance):
        instance_id = instance['id']
        status = instance['status']
        
        print(f"Instance {instance['name']} is {status}")
        
        if status == 'stopped':
            # Attempt to start
            self.vpc_service.create_instance_action(
                instance_id=instance_id,
                type='start'
            )
            print(f"Started instance {instance['name']}")
            
        elif status == 'failed':
            # Create alert
            self.create_alert(f"Instance {instance['name']} failed")
    
    def check_load_balancer_health(self, vpc_id):
        lbs = self.vpc_service.list_load_balancers().get_result()
        
        for lb in lbs['load_balancers']:
            pools = self.vpc_service.list_load_balancer_pools(
                load_balancer_id=lb['id']
            ).get_result()
            
            for pool in pools['pools']:
                if pool['health'] != 'ok':
                    self.remediate_pool(lb, pool)
    
    def remediate_pool(self, lb, pool):
        # Check pool members
        members = self.vpc_service.list_load_balancer_pool_members(
            load_balancer_id=lb['id'],
            pool_id=pool['id']
        ).get_result()
        
        for member in members['members']:
            if member['health'] != 'ok':
                # Remove and re-add member
                self.vpc_service.delete_load_balancer_pool_member(
                    load_balancer_id=lb['id'],
                    pool_id=pool['id'],
                    id=member['id']
                )
                
                # Wait for deletion
                time.sleep(30)
                
                # Re-add member
                self.vpc_service.create_load_balancer_pool_member(
                    load_balancer_id=lb['id'],
                    pool_id=pool['id'],
                    port=member['port'],
                    target={'id': member['target']['id']}
                )
    
    def create_alert(self, message):
        # Send to monitoring system
        print(f"ALERT: {message}")

# Run monitor
monitor = InfrastructureMonitor(api_key)
while True:
    monitor.check_instance_health(vpc_id)
    monitor.check_load_balancer_health(vpc_id)
    time.sleep(300)  # Check every 5 minutes
```

---

## Cost Optimization

### Resource Right-Sizing
```bash
# Analyze instance usage
ibmcloud is instances --output json | jq -r '
  .[] | 
  select(.status=="running") | 
  {name, profile: .profile.name, vcpu: .vcpu.count, memory: .memory}
'

# Find underutilized instances (requires monitoring data)
# Downsize instances
ibmcloud is instance-stop web-server-1
ibmcloud is instance-update web-server-1 --profile bx2-2x8
ibmcloud is instance-start web-server-1

# Remove unused resources
ibmcloud is instances --output json | \
  jq -r '.[] | select(.status=="stopped") | .id' | \
  xargs -I {} ibmcloud is instance-delete {} --force

# Cleanup old snapshots
ibmcloud is snapshots --output json | \
  jq -r '.[] | select(.created_at < "2024-01-01") | .id' | \
  xargs -I {} ibmcloud is snapshot-delete {}
```

### Cost Monitoring
```python
# cost_analysis.py
from ibm_platform_services import UsageReportsV4

def get_account_usage(account_id, month):
    usage_service = UsageReportsV4(authenticator=authenticator)
    
    usage = usage_service.get_account_usage(
        account_id=account_id,
        billingmonth=month
    ).get_result()
    
    resources = usage['resources']
    
    total_cost = sum(r['billable_cost'] for r in resources)
    
    print(f"Total cost for {month}: ${total_cost:.2f}")
    
    # Top 10 expensive resources
    sorted_resources = sorted(
        resources, 
        key=lambda x: x['billable_cost'], 
        reverse=True
    )[:10]
    
    for resource in sorted_resources:
        print(f"{resource['resource_name']}: ${resource['billable_cost']:.2f}")
    
    return total_cost

# Generate cost report
get_account_usage(account_id, '2024-01')
```

### Exam Tips
1. **IaC**: Master Terraform for VPC, compute, storage
2. **Automation**: Know bash and Python SDK for operations
3. **Scaling**: Understand autoscaling, instance groups
4. **Storage**: Know block vs object storage use cases
5. **K8s**: Master IKS operations, HPA, StatefulSets
6. **Cost**: Resource right-sizing, cleanup strategies

### Common Scenarios
- Deploy multi-zone infrastructure with Terraform
- Implement auto-scaling based on CPU/memory
- Automate health checks and remediation
- Optimize costs by right-sizing resources
- Manage Kubernetes workloads at scale

## Key terms

- **Infrastructure as code** - managing infrastructure through versioned, reviewable definition files instead of manual changes.
- **Terraform** - an infrastructure as code tool that provisions resources from declarative configuration files.
- **Virtual server instance (VSI)** - an IBM Cloud VPC virtual machine.
- **Instance group** - a set of identical VSIs managed together, which can scale automatically.
