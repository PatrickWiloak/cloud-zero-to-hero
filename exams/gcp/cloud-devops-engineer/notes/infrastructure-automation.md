# Infrastructure Automation - GCP Professional Cloud DevOps Engineer

## Overview

Infrastructure as Code (IaC), configuration management, and automation practices for managing GCP infrastructure at scale. This guide covers Terraform, Cloud Deployment Manager, Ansible, and comprehensive automation strategies for the Professional Cloud DevOps Engineer exam.

## Infrastructure as Code with Terraform

### Provider Configuration

**Basic Provider Setup**:
```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}
```

**Multi-Project Configuration**:
```hcl
provider "google" {
  alias   = "production"
  project = "prod-project-12345"
  region  = "us-central1"
}

provider "google" {
  alias   = "development"
  project = "dev-project-67890"
  region  = "us-west1"
}

# Use specific provider
resource "google_compute_network" "prod_vpc" {
  provider                = google.production
  name                    = "production-vpc"
  auto_create_subnetworks = false
}
```

**Service Account Impersonation**:
```hcl
provider "google" {
  impersonate_service_account = "terraform@my-project.iam.gserviceaccount.com"
  scopes = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
  ]
}
```

### Terraform Module Structure

**Complete Module Example**:
```hcl
# variables.tf
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Default region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 1
}

variable "labels" {
  description = "Labels to apply to resources"
  type        = map(string)
  default     = {}
}

# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  backend "gcs" {
    bucket = "terraform-state-bucket"
    prefix = "prod"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# VPC Network
resource "google_compute_network" "vpc" {
  name                    = "${var.environment}-vpc"
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"

  lifecycle {
    prevent_destroy = true
  }
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.environment}-subnet-${var.region}"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.4.0.0/14"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.0.32.0/20"
  }

  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Firewall Rules
resource "google_compute_firewall" "allow_internal" {
  name    = "${var.environment}-allow-internal"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = ["10.0.0.0/8"]
}

resource "google_compute_firewall" "allow_ssh_iap" {
  name    = "${var.environment}-allow-ssh-iap"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  # IAP IP ranges
  source_ranges = ["35.235.240.0/20"]
}

# outputs.tf
output "network_name" {
  description = "The name of the VPC network"
  value       = google_compute_network.vpc.name
}

output "network_id" {
  description = "The ID of the VPC network"
  value       = google_compute_network.vpc.id
}

output "subnet_name" {
  description = "The name of the subnet"
  value       = google_compute_subnetwork.subnet.name
}

output "subnet_cidr" {
  description = "The CIDR of the subnet"
  value       = google_compute_subnetwork.subnet.ip_cidr_range
}
```

### Terraform Resource Examples

**Compute Engine Instances**:
```hcl
# Instance Template
resource "google_compute_instance_template" "web_template" {
  name_prefix  = "web-template-"
  machine_type = "e2-medium"
  region       = var.region

  disk {
    source_image = "projects/debian-cloud/global/images/family/debian-11"
    auto_delete  = true
    boot         = true
    disk_size_gb = 20
    disk_type    = "pd-standard"
  }

  network_interface {
    network    = google_compute_network.vpc.id
    subnetwork = google_compute_subnetwork.subnet.id

    access_config {
      // Ephemeral public IP
    }
  }

  metadata = {
    enable-oslogin = "TRUE"
    startup-script = file("${path.module}/scripts/startup.sh")
  }

  service_account {
    email  = google_service_account.instance_sa.email
    scopes = ["cloud-platform"]
  }

  labels = merge(var.labels, {
    environment = var.environment
    managed_by  = "terraform"
  })

  lifecycle {
    create_before_destroy = true
  }
}

# Managed Instance Group
resource "google_compute_region_instance_group_manager" "web_mig" {
  name               = "${var.environment}-web-mig"
  base_instance_name = "web"
  region             = var.region

  version {
    instance_template = google_compute_instance_template.web_template.id
  }

  target_size = var.instance_count

  named_port {
    name = "http"
    port = 8080
  }

  auto_healing_policies {
    health_check      = google_compute_health_check.http_health_check.id
    initial_delay_sec = 300
  }

  update_policy {
    type                         = "PROACTIVE"
    minimal_action               = "REPLACE"
    max_surge_fixed              = 3
    max_unavailable_fixed        = 0
    instance_redistribution_type = "PROACTIVE"
  }
}

# Autoscaler
resource "google_compute_region_autoscaler" "web_autoscaler" {
  name   = "${var.environment}-web-autoscaler"
  region = var.region
  target = google_compute_region_instance_group_manager.web_mig.id

  autoscaling_policy {
    max_replicas    = 10
    min_replicas    = 2
    cooldown_period = 60

    cpu_utilization {
      target = 0.7
    }

    metric {
      name   = "pubsub.googleapis.com/subscription/num_undelivered_messages"
      target = 100
      type   = "GAUGE"
    }
  }
}

# Health Check
resource "google_compute_health_check" "http_health_check" {
  name               = "${var.environment}-http-health-check"
  check_interval_sec = 10
  timeout_sec        = 5

  http_health_check {
    port         = 8080
    request_path = "/health"
  }
}
```

**Google Kubernetes Engine (GKE)**:
```hcl
# GKE Cluster
resource "google_container_cluster" "primary" {
  name     = "${var.environment}-gke-cluster"
  location = var.region

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  # IP allocation for pods and services
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Workload Identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Network Policy
  network_policy {
    enabled  = true
    provider = "CALICO"
  }

  # Master authorized networks
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "10.0.0.0/8"
      display_name = "internal"
    }
  }

  # Private cluster configuration
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  # Maintenance window
  maintenance_policy {
    daily_maintenance_window {
      start_time = "03:00"
    }
  }

  # Logging and monitoring
  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
    managed_prometheus {
      enabled = true
    }
  }

  # Security features
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  resource_labels = var.labels
}

# Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.environment}-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.instance_count

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    preemptible  = false
    machine_type = "e2-standard-4"

    disk_size_gb = 100
    disk_type    = "pd-standard"

    # Google recommends custom service accounts with minimal permissions
    service_account = google_service_account.gke_nodes_sa.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = var.labels

    metadata = {
      disable-legacy-endpoints = "true"
    }

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }

  upgrade_settings {
    max_surge       = 1
    max_unavailable = 0
  }
}
```

**Cloud SQL Instance**:
```hcl
# Cloud SQL Instance
resource "google_sql_database_instance" "postgres" {
  name             = "${var.environment}-postgres-instance"
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    tier              = "db-custom-2-7680"
    availability_type = "REGIONAL"
    disk_type         = "PD_SSD"
    disk_size         = 100
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "02:00"
      transaction_log_retention_days = 7

      backup_retention_settings {
        retained_backups = 30
        retention_unit   = "COUNT"
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
      require_ssl     = true
    }

    maintenance_window {
      day          = 7  # Sunday
      hour         = 3
      update_track = "stable"
    }

    insights_config {
      query_insights_enabled  = true
      query_string_length     = 1024
      record_application_tags = true
      record_client_address   = true
    }

    database_flags {
      name  = "max_connections"
      value = "100"
    }

    database_flags {
      name  = "log_checkpoints"
      value = "on"
    }
  }

  deletion_protection = true
}

# Database
resource "google_sql_database" "database" {
  name     = "application_db"
  instance = google_sql_database_instance.postgres.name
}

# User
resource "google_sql_user" "app_user" {
  name     = "app_user"
  instance = google_sql_database_instance.postgres.name
  password = random_password.db_password.result
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Store password in Secret Manager
resource "google_secret_manager_secret" "db_password" {
  secret_id = "${var.environment}-db-password"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "db_password_version" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}
```

**Cloud Storage Bucket**:
```hcl
resource "google_storage_bucket" "data_bucket" {
  name          = "${var.project_id}-${var.environment}-data"
  location      = var.region
  storage_class = "STANDARD"

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type = "Delete"
    }
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.bucket_key.id
  }

  logging {
    log_bucket = google_storage_bucket.logs_bucket.name
  }

  labels = var.labels
}

# IAM binding for bucket
resource "google_storage_bucket_iam_member" "bucket_admin" {
  bucket = google_storage_bucket.data_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.app_sa.email}"
}
```

### Terraform State Management

**Remote Backend Configuration (GCS)**:
```hcl
terraform {
  backend "gcs" {
    bucket  = "my-terraform-state-bucket"
    prefix  = "terraform/state"

    # Optional: Enable encryption
    encryption_key = "your-kms-key"
  }
}
```

**Backend Initialization**:
```bash
# Initialize backend
terraform init

# Migrate from local to remote
terraform init -migrate-state

# Reconfigure backend
terraform init -reconfigure

# Backend configuration from file
terraform init -backend-config=backend.hcl
```

**Backend Configuration File** (backend.hcl):
```hcl
bucket  = "prod-terraform-state"
prefix  = "prod/network"
```

**State Management Commands**:
```bash
# List resources in state
terraform state list

# Show specific resource
terraform state show google_compute_network.vpc

# Remove resource from state (doesn't delete actual resource)
terraform state rm google_compute_instance.old_instance

# Move resource in state (rename)
terraform state mv google_compute_instance.web google_compute_instance.web_server

# Pull state to local file
terraform state pull > terraform.tfstate

# Push state from local file
terraform state push terraform.tfstate

# Replace provider address (after provider migration)
terraform state replace-provider registry.terraform.io/-/google hashicorp/google
```

**State Locking**:
```hcl
# GCS automatically provides state locking
# No additional configuration needed for basic locking

# To enable encryption and versioning
resource "google_storage_bucket" "terraform_state" {
  name          = "my-terraform-state"
  location      = "US"
  storage_class = "STANDARD"

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      num_newer_versions = 10
    }
    action {
      type = "Delete"
    }
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.terraform_key.id
  }
}

# Grant permissions
resource "google_storage_bucket_iam_member" "terraform_state" {
  bucket = google_storage_bucket.terraform_state.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:terraform@my-project.iam.gserviceaccount.com"
}
```

### Terraform Workspaces

**Workspace Commands**:
```bash
# List workspaces
terraform workspace list

# Create new workspace
terraform workspace new staging

# Select workspace
terraform workspace select production

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete dev
```

**Using Workspaces in Configuration**:
```hcl
locals {
  environment = terraform.workspace

  # Environment-specific configurations
  instance_counts = {
    default    = 1
    dev        = 1
    staging    = 2
    production = 5
  }

  machine_types = {
    default    = "e2-micro"
    dev        = "e2-small"
    staging    = "e2-medium"
    production = "e2-standard-4"
  }
}

resource "google_compute_instance_template" "app" {
  name_prefix  = "${local.environment}-app-"
  machine_type = local.machine_types[local.environment]

  # ...
}

resource "google_compute_region_instance_group_manager" "app" {
  name       = "${local.environment}-app-mig"
  target_size = local.instance_counts[local.environment]

  # ...
}

# Workspace-specific state files
terraform {
  backend "gcs" {
    bucket = "terraform-state-bucket"
    prefix = "env/${terraform.workspace}"
  }
}
```

**Workspace Best Practices**:
- Use workspaces for environment separation (dev, staging, prod)
- Don't rely solely on workspaces for isolation - use separate projects/folders
- Combine with separate state file prefixes
- Document workspace naming conventions

### Terraform Data Sources

**Using Data Sources**:
```hcl
# Get latest image
data "google_compute_image" "debian" {
  family  = "debian-11"
  project = "debian-cloud"
}

# Get existing network
data "google_compute_network" "default" {
  name = "default"
}

# Get project information
data "google_project" "project" {
  project_id = var.project_id
}

# Get service account
data "google_service_account" "default" {
  account_id = "default-sa"
}

# Get secret from Secret Manager
data "google_secret_manager_secret_version" "db_password" {
  secret  = "database-password"
  version = "latest"
}

# Use data sources in resources
resource "google_compute_instance" "web" {
  name         = "web-server"
  machine_type = "e2-medium"

  boot_disk {
    initialize_params {
      image = data.google_compute_image.debian.self_link
    }
  }

  network_interface {
    network = data.google_compute_network.default.id
  }

  service_account {
    email  = data.google_service_account.default.email
    scopes = ["cloud-platform"]
  }

  metadata = {
    db_password = data.google_secret_manager_secret_version.db_password.secret_data
  }
}
```

## Cloud Deployment Manager

### Template Syntax and Structure

**Basic YAML Configuration**:
```yaml
# config.yaml
imports:
- path: network.jinja
- path: instance.py

resources:
- name: production-network
  type: network.jinja
  properties:
    name: prod-vpc
    autoCreateSubnetworks: false
    region: us-central1

- name: web-instance
  type: instance.py
  properties:
    zone: us-central1-a
    machineType: e2-medium
    network: $(ref.production-network.selfLink)

outputs:
- name: networkName
  value: $(ref.production-network.name)
- name: instanceIP
  value: $(ref.web-instance.networkInterfaces[0].accessConfigs[0].natIP)
```

### JINJA2 Templates

**Network Template** (network.jinja):
```jinja
resources:
- name: {{ properties['name'] }}
  type: compute.v1.network
  properties:
    autoCreateSubnetworks: {{ properties['autoCreateSubnetworks'] }}
    routingConfig:
      routingMode: REGIONAL

{% if properties.get('subnetworks') %}
{% for subnet in properties['subnetworks'] %}
- name: {{ properties['name'] }}-subnet-{{ loop.index }}
  type: compute.v1.subnetwork
  properties:
    network: $(ref.{{ properties['name'] }}.selfLink)
    ipCidrRange: {{ subnet['cidrRange'] }}
    region: {{ subnet['region'] }}
    privateIpGoogleAccess: true
    logConfig:
      enable: true
      aggregationInterval: INTERVAL_10_MIN
      flowSampling: 0.5
      metadata: INCLUDE_ALL_METADATA
{% endfor %}
{% endif %}

# Firewall Rules
- name: {{ properties['name'] }}-allow-internal
  type: compute.v1.firewall
  properties:
    network: $(ref.{{ properties['name'] }}.selfLink)
    sourceRanges:
    - 10.0.0.0/8
    allowed:
    - IPProtocol: tcp
      ports: [0-65535]
    - IPProtocol: udp
      ports: [0-65535]
    - IPProtocol: icmp

- name: {{ properties['name'] }}-allow-ssh
  type: compute.v1.firewall
  properties:
    network: $(ref.{{ properties['name'] }}.selfLink)
    sourceRanges:
    - 35.235.240.0/20  # IAP range
    allowed:
    - IPProtocol: tcp
      ports: [22]

outputs:
- name: networkName
  value: $(ref.{{ properties['name'] }}.name)
- name: networkSelfLink
  value: $(ref.{{ properties['name'] }}.selfLink)
```

**Instance Template** (instance.jinja):
```jinja
resources:
- name: {{ properties['name'] }}
  type: compute.v1.instance
  properties:
    zone: {{ properties['zone'] }}
    machineType: zones/{{ properties['zone'] }}/machineTypes/{{ properties['machineType'] }}

    disks:
    - deviceName: boot
      type: PERSISTENT
      boot: true
      autoDelete: true
      initializeParams:
        sourceImage: {{ properties.get('sourceImage', 'projects/debian-cloud/global/images/family/debian-11') }}
        diskSizeGb: {{ properties.get('diskSizeGb', 20) }}
        diskType: zones/{{ properties['zone'] }}/diskTypes/{{ properties.get('diskType', 'pd-standard') }}

    networkInterfaces:
    - network: {{ properties['network'] }}
      {% if properties.get('subnetwork') %}
      subnetwork: {{ properties['subnetwork'] }}
      {% endif %}
      {% if properties.get('externalIP', true) %}
      accessConfigs:
      - name: External NAT
        type: ONE_TO_ONE_NAT
      {% endif %}

    metadata:
      items:
      - key: enable-oslogin
        value: 'TRUE'
      {% if properties.get('startupScript') %}
      - key: startup-script
        value: |
          {{ properties['startupScript'] | indent(10) }}
      {% endif %}

    serviceAccounts:
    - email: {{ properties.get('serviceAccount', 'default') }}
      scopes:
      - https://www.googleapis.com/auth/cloud-platform

    tags:
      items: {{ properties.get('tags', []) }}

    labels:
      environment: {{ properties.get('environment', 'dev') }}
      managed-by: deployment-manager

outputs:
- name: internalIP
  value: $(ref.{{ properties['name'] }}.networkInterfaces[0].networkIP)
{% if properties.get('externalIP', true) %}
- name: externalIP
  value: $(ref.{{ properties['name'] }}.networkInterfaces[0].accessConfigs[0].natIP)
{% endif %}
```

### Python Templates

**Instance Template** (instance.py):
```python
"""Creates a Compute Engine instance."""

def GenerateConfig(context):
    """Generates configuration for a Compute Engine instance."""

    resources = []
    properties = context.properties

    # Instance resource
    instance = {
        'name': context.env['name'],
        'type': 'compute.v1.instance',
        'properties': {
            'zone': properties['zone'],
            'machineType': f"zones/{properties['zone']}/machineTypes/{properties.get('machineType', 'e2-medium')}",
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': properties.get('sourceImage',
                        'projects/debian-cloud/global/images/family/debian-11'),
                    'diskSizeGb': properties.get('diskSizeGb', 20),
                    'diskType': f"zones/{properties['zone']}/diskTypes/pd-standard"
                }
            }],
            'networkInterfaces': [{
                'network': properties['network'],
                'accessConfigs': [{
                    'name': 'External NAT',
                    'type': 'ONE_TO_ONE_NAT'
                }]
            }],
            'metadata': {
                'items': [
                    {
                        'key': 'enable-oslogin',
                        'value': 'TRUE'
                    }
                ]
            },
            'serviceAccounts': [{
                'email': properties.get('serviceAccount', 'default'),
                'scopes': ['https://www.googleapis.com/auth/cloud-platform']
            }],
            'tags': {
                'items': properties.get('tags', [])
            },
            'labels': {
                'environment': properties.get('environment', 'dev'),
                'managed-by': 'deployment-manager'
            }
        }
    }

    resources.append(instance)

    # Add startup script if provided
    if 'startupScript' in properties:
        instance['properties']['metadata']['items'].append({
            'key': 'startup-script',
            'value': properties['startupScript']
        })

    return {
        'resources': resources,
        'outputs': [
            {
                'name': 'internalIP',
                'value': f"$(ref.{context.env['name']}.networkInterfaces[0].networkIP)"
            },
            {
                'name': 'externalIP',
                'value': f"$(ref.{context.env['name']}.networkInterfaces[0].accessConfigs[0].natIP)"
            }
        ]
    }
```

**Complex Python Template with Multiple Resources**:
```python
"""Creates a complete web application infrastructure."""

def GenerateConfig(context):
    """Generates a complete application stack."""

    properties = context.properties
    env = context.env
    resources = []

    # Create instance template
    template_name = f"{env['name']}-template"
    template = {
        'name': template_name,
        'type': 'compute.v1.instanceTemplate',
        'properties': {
            'properties': {
                'machineType': properties.get('machineType', 'e2-medium'),
                'disks': [{
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': 'projects/debian-cloud/global/images/family/debian-11'
                    }
                }],
                'networkInterfaces': [{
                    'network': properties['network'],
                    'subnetwork': properties['subnetwork']
                }],
                'metadata': {
                    'items': [
                        {
                            'key': 'startup-script',
                            'value': properties.get('startupScript', '')
                        }
                    ]
                },
                'serviceAccounts': [{
                    'email': 'default',
                    'scopes': ['https://www.googleapis.com/auth/cloud-platform']
                }],
                'tags': {
                    'items': ['http-server', 'https-server']
                }
            }
        }
    }
    resources.append(template)

    # Create managed instance group
    mig_name = f"{env['name']}-mig"
    mig = {
        'name': mig_name,
        'type': 'compute.v1.regionInstanceGroupManager',
        'properties': {
            'region': properties['region'],
            'baseInstanceName': env['name'],
            'instanceTemplate': f"$(ref.{template_name}.selfLink)",
            'targetSize': properties.get('minReplicas', 2),
            'namedPorts': [{
                'name': 'http',
                'port': 80
            }],
            'autoHealingPolicies': [{
                'healthCheck': properties['healthCheck'],
                'initialDelaySec': 300
            }]
        }
    }
    resources.append(mig)

    # Create autoscaler
    autoscaler = {
        'name': f"{env['name']}-autoscaler",
        'type': 'compute.v1.regionAutoscaler',
        'properties': {
            'region': properties['region'],
            'target': f"$(ref.{mig_name}.selfLink)",
            'autoscalingPolicy': {
                'minNumReplicas': properties.get('minReplicas', 2),
                'maxNumReplicas': properties.get('maxReplicas', 10),
                'coolDownPeriodSec': 60,
                'cpuUtilization': {
                    'utilizationTarget': 0.7
                }
            }
        }
    }
    resources.append(autoscaler)

    return {'resources': resources}
```

### Schema Files

**Template Schema** (network.jinja.schema):
```yaml
info:
  title: VPC Network
  author: DevOps Team
  description: Creates a VPC network with subnets and firewall rules
  version: 1.0

imports:
- path: network.jinja

required:
- name
- region

properties:
  name:
    type: string
    description: Name of the VPC network
    pattern: ^[a-z]([-a-z0-9]*[a-z0-9])?$

  autoCreateSubnetworks:
    type: boolean
    description: Whether to auto-create subnetworks
    default: false

  region:
    type: string
    description: Default region for resources
    enum:
    - us-central1
    - us-east1
    - us-west1
    - europe-west1

  subnetworks:
    type: array
    description: List of subnetworks to create
    items:
      type: object
      required:
      - cidrRange
      - region
      properties:
        cidrRange:
          type: string
          description: CIDR range for the subnet
          pattern: ^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$
        region:
          type: string
          description: Region for the subnet

outputs:
  properties:
    networkName:
      type: string
      description: Name of the created network
    networkSelfLink:
      type: string
      description: Self link of the created network
```

### Composite Types

**Composite Type Definition** (web-app.jinja):
```jinja
resources:
# Load Balancer
- name: {{ env['name'] }}-lb
  type: compute.v1.globalForwardingRule
  properties:
    IPProtocol: TCP
    portRange: 80-80
    target: $(ref.{{ env['name'] }}-proxy.selfLink)

- name: {{ env['name'] }}-proxy
  type: compute.v1.targetHttpProxy
  properties:
    urlMap: $(ref.{{ env['name'] }}-url-map.selfLink)

- name: {{ env['name'] }}-url-map
  type: compute.v1.urlMap
  properties:
    defaultService: $(ref.{{ env['name'] }}-backend.selfLink)

- name: {{ env['name'] }}-backend
  type: compute.v1.backendService
  properties:
    backends:
    - group: {{ properties['instanceGroup'] }}
    healthChecks:
    - $(ref.{{ env['name'] }}-health-check.selfLink)
    protocol: HTTP
    port: 80
    timeoutSec: 30

- name: {{ env['name'] }}-health-check
  type: compute.v1.healthCheck
  properties:
    type: HTTP
    httpHealthCheck:
      port: 80
      requestPath: /health
    checkIntervalSec: 10
    timeoutSec: 5
    unhealthyThreshold: 3
    healthyThreshold: 2
```

### Deployment Operations

**Deploy Configuration**:
```bash
# Create deployment
gcloud deployment-manager deployments create my-deployment \
  --config config.yaml \
  --preview

# Update deployment
gcloud deployment-manager deployments update my-deployment \
  --config config.yaml

# Delete deployment
gcloud deployment-manager deployments delete my-deployment

# Describe deployment
gcloud deployment-manager deployments describe my-deployment

# List deployments
gcloud deployment-manager deployments list

# View deployment manifest
gcloud deployment-manager manifests describe <MANIFEST_NAME> \
  --deployment my-deployment
```

**Preview Mode**:
```bash
# Preview changes
gcloud deployment-manager deployments create my-deployment \
  --config config.yaml \
  --preview

# View preview
gcloud deployment-manager deployments describe my-deployment

# Apply previewed deployment
gcloud deployment-manager deployments update my-deployment

# Cancel preview
gcloud deployment-manager deployments cancel-preview my-deployment
```

**Using Properties Files**:
```bash
# config.yaml with properties file
imports:
- path: network.jinja

resources:
- name: production-network
  type: network.jinja
  properties:
    name: prod-vpc
    autoCreateSubnetworks: false

# Deploy with properties
gcloud deployment-manager deployments create my-deployment \
  --config config.yaml \
  --properties region:us-central1,environment:prod
```

## Ansible on GCP

### Setup and Authentication

**Install Ansible GCP Modules**:
```bash
# Install Ansible
pip install ansible

# Install GCP modules
pip install google-auth requests

# Install Ansible GCP collection
ansible-galaxy collection install google.cloud
```

**Authentication Configuration**:
```yaml
# group_vars/all.yml
gcp_project: my-gcp-project
gcp_cred_file: /path/to/service-account-key.json
gcp_region: us-central1
gcp_zone: us-central1-a
```

### GCP Modules and Playbooks

**Complete Infrastructure Playbook**:
```yaml
---
- name: Provision GCP Infrastructure
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    project_id: "{{ gcp_project }}"
    region: us-central1
    zone: us-central1-a
    network_name: production-vpc
    subnet_name: production-subnet

  tasks:
    # Create VPC Network
    - name: Create VPC network
      google.cloud.gcp_compute_network:
        name: "{{ network_name }}"
        auto_create_subnetworks: false
        routing_config:
          routing_mode: REGIONAL
        project: "{{ project_id }}"
        auth_kind: serviceaccount
        service_account_file: "{{ gcp_cred_file }}"
        state: present
      register: network

    # Create Subnet
    - name: Create subnet
      google.cloud.gcp_compute_subnetwork:
        name: "{{ subnet_name }}"
        region: "{{ region }}"
        network: "{{ network }}"
        ip_cidr_range: 10.0.1.0/24
        private_ip_google_access: true
        log_config:
          enable: true
          aggregation_interval: INTERVAL_10_MIN
          flow_sampling: 0.5
          metadata: INCLUDE_ALL_METADATA
        project: "{{ project_id }}"
        auth_kind: serviceaccount
        service_account_file: "{{ gcp_cred_file }}"
        state: present
      register: subnet

    # Create Firewall Rules
    - name: Create firewall rule - allow internal
      google.cloud.gcp_compute_firewall:
        name: "{{ network_name }}-allow-internal"
        network: "{{ network }}"
        allowed:
          - ip_protocol: tcp
            ports:
              - '0-65535'
          - ip_protocol: udp
            ports:
              - '0-65535'
          - ip_protocol: icmp
        source_ranges:
          - 10.0.0.0/8
        project: "{{ project_id }}"
        auth_kind: serviceaccount
        service_account_file: "{{ gcp_cred_file }}"
        state: present

    - name: Create firewall rule - allow SSH from IAP
      google.cloud.gcp_compute_firewall:
        name: "{{ network_name }}-allow-ssh-iap"
        network: "{{ network }}"
        allowed:
          - ip_protocol: tcp
            ports:
              - '22'
        source_ranges:
          - 35.235.240.0/20
        project: "{{ project_id }}"
        auth_kind: serviceaccount
        service_account_file: "{{ gcp_cred_file }}"
        state: present

    # Create instance template
    - name: Create instance template
      google.cloud.gcp_compute_instance_template:
        name: web-template
        properties:
          machine_type: e2-medium
          disks:
            - auto_delete: true
              boot: true
              initialize_params:
                source_image: projects/debian-cloud/global/images/family/debian-11
                disk_size_gb: 20
          network_interfaces:
            - network: "{{ network }}"
              subnetwork: "{{ subnet }}"
          metadata:
            enable-oslogin: 'TRUE'
            startup-script: |
              #!/bin/bash
              apt-get update
              apt-get install -y nginx
              systemctl start nginx
          tags:
            items:
              - http-server
              - https-server
        project: "{{ project_id }}"
        auth_kind: serviceaccount
        service_account_file: "{{ gcp_cred_file }}"
        state: present
      register: template

    # Create managed instance group
    - name: Create managed instance group
      google.cloud.gcp_compute_region_instance_group_manager:
        name: web-mig
        base_instance_name: web
        region: "{{ region }}"
        instance_template: "{{ template }}"
        target_size: 3
        named_ports:
          - name: http
            port: 80
        project: "{{ project_id }}"
        auth_kind: serviceaccount
        service_account_file: "{{ gcp_cred_file }}"
        state: present

    # Create Cloud SQL instance
    - name: Create Cloud SQL instance
      google.cloud.gcp_sql_instance:
        name: production-postgres
        database_version: POSTGRES_14
        region: "{{ region }}"
        settings:
          tier: db-custom-2-7680
          availability_type: REGIONAL
          backup_configuration:
            enabled: true
            start_time: "02:00"
            point_in_time_recovery_enabled: true
          ip_configuration:
            ipv4_enabled: false
            private_network: "{{ network.selfLink }}"
            require_ssl: true
        project: "{{ project_id }}"
        auth_kind: serviceaccount
        service_account_file: "{{ gcp_cred_file }}"
        state: present

    # Create GKE cluster
    - name: Create GKE cluster
      google.cloud.gcp_container_cluster:
        name: production-gke
        location: "{{ region }}"
        initial_node_count: 1
        remove_default_node_pool: true
        network: "{{ network_name }}"
        subnetwork: "{{ subnet_name }}"
        ip_allocation_policy:
          cluster_secondary_range_name: pods
          services_secondary_range_name: services
        master_auth:
          client_certificate_config:
            issue_client_certificate: false
        private_cluster_config:
          enable_private_nodes: true
          enable_private_endpoint: false
          master_ipv4_cidr_block: 172.16.0.0/28
        project: "{{ project_id }}"
        auth_kind: serviceaccount
        service_account_file: "{{ gcp_cred_file }}"
        state: present
```

### Dynamic Inventory

**GCP Dynamic Inventory Configuration** (gcp.yml):
```yaml
plugin: google.cloud.gcp_compute
projects:
  - my-gcp-project
auth_kind: serviceaccount
service_account_file: /path/to/service-account-key.json

# Filter instances
filters:
  - status = RUNNING

# Group instances
groups:
  production: "'production' in labels.environment"
  staging: "'staging' in labels.environment"
  web_servers: "'web' in tags.items"

# Hostname configuration
hostnames:
  - name

# Keyed groups
keyed_groups:
  - key: labels.environment
    prefix: env
  - key: zone
    prefix: zone

# Compose variables
compose:
  ansible_host: networkInterfaces[0].accessConfigs[0].natIP | default(networkInterfaces[0].networkIP)
  ansible_user: "'ansible'"
```

**Using Dynamic Inventory**:
```bash
# List inventory
ansible-inventory -i gcp.yml --list

# Ping all instances
ansible all -i gcp.yml -m ping

# Run playbook with dynamic inventory
ansible-playbook -i gcp.yml site.yml

# Target specific groups
ansible-playbook -i gcp.yml --limit production playbook.yml
```

**Playbook Using Dynamic Inventory**:
```yaml
---
- name: Configure web servers
  hosts: web_servers
  become: yes

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Deploy application
      copy:
        src: files/app.conf
        dest: /etc/nginx/sites-available/app.conf
      notify: Reload nginx

  handlers:
    - name: Reload nginx
      service:
        name: nginx
        state: reloaded
```

### Ansible Roles for GCP

**Directory Structure**:
```
roles/
  gcp_network/
    tasks/
      main.yml
    vars/
      main.yml
    defaults/
      main.yml
  gcp_compute/
    tasks/
      main.yml
    templates/
      startup-script.sh.j2
```

**Network Role** (roles/gcp_network/tasks/main.yml):
```yaml
---
- name: Create VPC network
  google.cloud.gcp_compute_network:
    name: "{{ network_name }}"
    auto_create_subnetworks: "{{ auto_create_subnetworks }}"
    project: "{{ gcp_project }}"
    auth_kind: serviceaccount
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  register: network_result

- name: Create subnets
  google.cloud.gcp_compute_subnetwork:
    name: "{{ item.name }}"
    region: "{{ item.region }}"
    network: "{{ network_result }}"
    ip_cidr_range: "{{ item.cidr }}"
    private_ip_google_access: true
    project: "{{ gcp_project }}"
    auth_kind: serviceaccount
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  loop: "{{ subnets }}"

- name: Create firewall rules
  google.cloud.gcp_compute_firewall:
    name: "{{ item.name }}"
    network: "{{ network_result }}"
    allowed: "{{ item.allowed }}"
    source_ranges: "{{ item.source_ranges }}"
    project: "{{ gcp_project }}"
    auth_kind: serviceaccount
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  loop: "{{ firewall_rules }}"
```

## Configuration Management

### Cloud Init for VM Startup

**Basic Cloud Init Configuration**:
```yaml
#cloud-config
package_update: true
package_upgrade: true

packages:
  - nginx
  - docker.io
  - git
  - python3-pip

runcmd:
  - systemctl start docker
  - systemctl enable docker
  - docker run -d -p 8080:8080 gcr.io/my-project/myapp:latest
  - systemctl start nginx
  - systemctl enable nginx

write_files:
  - path: /etc/nginx/conf.d/app.conf
    content: |
      server {
        listen 80;
        server_name _;
        location / {
          proxy_pass http://localhost:8080;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
        }
      }
    permissions: '0644'

  - path: /opt/app/config.json
    content: |
      {
        "environment": "production",
        "log_level": "info"
      }
    permissions: '0644'

users:
  - name: appuser
    groups: docker
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh-authorized-keys:
      - ssh-rsa AAAAB3NzaC1yc2E...

final_message: "Cloud init completed after $UPTIME seconds"
```

**Advanced Cloud Init with Metadata**:
```yaml
#cloud-config
package_update: true
package_upgrade: true

write_files:
  - path: /opt/startup/setup.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      # Fetch metadata
      PROJECT_ID=$(curl -H "Metadata-Flavor: Google" \
        http://metadata.google.internal/computeMetadata/v1/project/project-id)

      INSTANCE_NAME=$(curl -H "Metadata-Flavor: Google" \
        http://metadata.google.internal/computeMetadata/v1/instance/name)

      ZONE=$(curl -H "Metadata-Flavor: Google" \
        http://metadata.google.internal/computeMetadata/v1/instance/zone | cut -d'/' -f4)

      # Configure application
      cat > /opt/app/config.json <<EOF
      {
        "project_id": "$PROJECT_ID",
        "instance_name": "$INSTANCE_NAME",
        "zone": "$ZONE"
      }
      EOF

      # Fetch secret from Secret Manager
      DB_PASSWORD=$(gcloud secrets versions access latest \
        --secret="db-password" --project="$PROJECT_ID")

      echo "DB_PASSWORD=$DB_PASSWORD" >> /opt/app/.env

runcmd:
  - /opt/startup/setup.sh
  - systemctl restart application
```

### Startup Scripts

**Bash Startup Script**:
```bash
#!/bin/bash

# Log everything
exec > >(tee -a /var/log/startup-script.log)
exec 2>&1

echo "Starting instance setup at $(date)"

# Update system
apt-get update
apt-get upgrade -y

# Install packages
apt-get install -y \
  nginx \
  docker.io \
  git \
  python3-pip \
  google-cloud-sdk

# Configure Docker
systemctl start docker
systemctl enable docker

# Fetch instance metadata
INSTANCE_NAME=$(curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/name)

PROJECT_ID=$(curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/project/project-id)

ZONE=$(curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/zone | cut -d'/' -f4)

# Fetch custom metadata
APP_VERSION=$(curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/attributes/app-version)

ENVIRONMENT=$(curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/attributes/environment)

# Pull and run application
gcloud auth configure-docker
docker pull gcr.io/${PROJECT_ID}/myapp:${APP_VERSION}
docker run -d \
  --name myapp \
  --restart always \
  -p 8080:8080 \
  -e ENVIRONMENT=${ENVIRONMENT} \
  -e INSTANCE_NAME=${INSTANCE_NAME} \
  gcr.io/${PROJECT_ID}/myapp:${APP_VERSION}

# Configure nginx
cat > /etc/nginx/sites-available/app.conf <<'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /health {
        access_log off;
        return 200 "healthy\n";
    }
}
EOF

ln -s /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl restart nginx

echo "Instance setup completed at $(date)"
```

**Using Startup Script in Terraform**:
```hcl
resource "google_compute_instance" "web" {
  name         = "web-server"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "projects/debian-cloud/global/images/family/debian-11"
    }
  }

  network_interface {
    network = google_compute_network.vpc.id
    access_config {}
  }

  metadata = {
    startup-script = file("${path.module}/scripts/startup.sh")

    # Or inline
    # startup-script = <<-EOF
    #   #!/bin/bash
    #   apt-get update
    #   apt-get install -y nginx
    # EOF

    # Custom metadata
    app-version = "v1.2.3"
    environment = "production"
  }

  metadata_startup_script = file("${path.module}/scripts/startup.sh")
}
```

### OS Config (OS Patch Management)

**OS Policy Assignment**:
```yaml
# os-policy.yaml
osPolicies:
- id: install-ops-agent
  mode: ENFORCEMENT
  resourceGroups:
  - resources:
    - id: install-ops-agent-package
      pkg:
        desiredState: INSTALLED
        apt:
          name: google-cloud-ops-agent

- id: configure-security
  mode: ENFORCEMENT
  resourceGroups:
  - resources:
    - id: ensure-firewall-enabled
      exec:
        validate:
          interpreter: SHELL
          script: |
            #!/bin/bash
            systemctl is-active ufw
        enforce:
          interpreter: SHELL
          script: |
            #!/bin/bash
            apt-get install -y ufw
            ufw enable

- id: patch-management
  mode: ENFORCEMENT
  resourceGroups:
  - resources:
    - id: update-packages
      pkg:
        desiredState: INSTALLED
        apt:
          name: unattended-upgrades
```

**Create Patch Deployment**:
```bash
# Create patch deployment
gcloud compute os-config patch-deployments create weekly-patch \
  --os-filter="os-short-name=debian" \
  --recurring-schedule-weekly="DAY_OF_WEEK_SUNDAY" \
  --recurring-schedule-time="03:00" \
  --patch-config-reboot-config=ALWAYS \
  --rollout-mode=ZONE_BY_ZONE \
  --rollout-disruption-budget-percent=20

# Create one-time patch job
gcloud compute os-config patch-jobs execute \
  --instance-filter-labels=environment=production \
  --async

# List patch deployments
gcloud compute os-config patch-deployments list

# Describe patch job
gcloud compute os-config patch-jobs describe JOB_ID
```

### Instance Metadata

**Accessing Metadata in Scripts**:
```bash
#!/bin/bash

# Base metadata server URL
METADATA_URL="http://metadata.google.internal/computeMetadata/v1"
HEADERS="Metadata-Flavor: Google"

# Get project metadata
PROJECT_ID=$(curl -s -H "$HEADERS" "${METADATA_URL}/project/project-id")
PROJECT_NUMBER=$(curl -s -H "$HEADERS" "${METADATA_URL}/project/numeric-project-id")

# Get instance metadata
INSTANCE_NAME=$(curl -s -H "$HEADERS" "${METADATA_URL}/instance/name")
INSTANCE_ID=$(curl -s -H "$HEADERS" "${METADATA_URL}/instance/id")
ZONE=$(curl -s -H "$HEADERS" "${METADATA_URL}/instance/zone")
MACHINE_TYPE=$(curl -s -H "$HEADERS" "${METADATA_URL}/instance/machine-type")
INTERNAL_IP=$(curl -s -H "$HEADERS" "${METADATA_URL}/instance/network-interfaces/0/ip")
EXTERNAL_IP=$(curl -s -H "$HEADERS" "${METADATA_URL}/instance/network-interfaces/0/access-configs/0/external-ip")

# Get custom metadata
CUSTOM_VALUE=$(curl -s -H "$HEADERS" "${METADATA_URL}/instance/attributes/custom-key")

# Get service account token
TOKEN=$(curl -s -H "$HEADERS" "${METADATA_URL}/instance/service-accounts/default/token")

# Use token for API calls
curl -H "Authorization: Bearer ${TOKEN}" \
  https://storage.googleapis.com/storage/v1/b/my-bucket/o
```

## Immutable Infrastructure

### Golden Images with Packer

**Packer Template for GCP** (packer.json):
```json
{
  "variables": {
    "project_id": "my-gcp-project",
    "zone": "us-central1-a",
    "source_image_family": "debian-11",
    "image_name": "web-server-{{timestamp}}",
    "ssh_username": "packer"
  },
  "builders": [
    {
      "type": "googlecompute",
      "project_id": "{{user `project_id`}}",
      "zone": "{{user `zone`}}",
      "source_image_family": "{{user `source_image_family`}}",
      "ssh_username": "{{user `ssh_username`}}",
      "image_name": "{{user `image_name`}}",
      "image_family": "web-server",
      "image_description": "Web server golden image",
      "disk_size": 20,
      "disk_type": "pd-standard",
      "machine_type": "e2-medium",
      "tags": ["packer"],
      "labels": {
        "environment": "production",
        "created_by": "packer"
      }
    }
  ],
  "provisioners": [
    {
      "type": "shell",
      "inline": [
        "sudo apt-get update",
        "sudo apt-get upgrade -y",
        "sudo apt-get install -y nginx docker.io git python3-pip",
        "sudo systemctl enable nginx",
        "sudo systemctl enable docker"
      ]
    },
    {
      "type": "file",
      "source": "files/nginx.conf",
      "destination": "/tmp/nginx.conf"
    },
    {
      "type": "shell",
      "inline": [
        "sudo mv /tmp/nginx.conf /etc/nginx/nginx.conf",
        "sudo chown root:root /etc/nginx/nginx.conf"
      ]
    },
    {
      "type": "ansible",
      "playbook_file": "ansible/configure.yml",
      "extra_arguments": [
        "--extra-vars",
        "ansible_python_interpreter=/usr/bin/python3"
      ]
    },
    {
      "type": "shell",
      "script": "scripts/cleanup.sh"
    }
  ],
  "post-processors": [
    {
      "type": "manifest",
      "output": "manifest.json",
      "strip_path": true
    }
  ]
}
```

**HCL2 Packer Template** (image.pkr.hcl):
```hcl
variable "project_id" {
  type    = string
  default = "my-gcp-project"
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "image_family" {
  type    = string
  default = "web-server"
}

source "googlecompute" "web_server" {
  project_id          = var.project_id
  zone                = var.zone
  source_image_family = "debian-11"
  ssh_username        = "packer"
  image_name          = "web-server-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  image_family        = var.image_family
  image_description   = "Golden image for web servers"
  disk_size           = 20
  disk_type           = "pd-ssd"
  machine_type        = "e2-medium"

  labels = {
    environment = "production"
    created_by  = "packer"
  }

  tags = ["packer"]
}

build {
  sources = ["source.googlecompute.web_server"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y nginx docker.io git python3-pip google-cloud-ops-agent",
      "sudo systemctl enable nginx",
      "sudo systemctl enable docker",
      "sudo systemctl enable google-cloud-ops-agent"
    ]
  }

  provisioner "file" {
    sources     = ["files/nginx.conf", "files/app.conf"]
    destination = "/tmp/"
  }

  provisioner "shell" {
    scripts = [
      "scripts/configure-nginx.sh",
      "scripts/install-app.sh",
      "scripts/cleanup.sh"
    ]
  }

  provisioner "ansible" {
    playbook_file = "ansible/configure.yml"
    extra_arguments = [
      "--extra-vars",
      "environment=production"
    ]
  }

  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}
```

**Build Image**:
```bash
# Validate template
packer validate image.pkr.hcl

# Build image
packer build image.pkr.hcl

# Build with variables
packer build \
  -var 'project_id=my-project' \
  -var 'zone=us-west1-a' \
  image.pkr.hcl

# Build specific source
packer build -only=googlecompute.web_server image.pkr.hcl
```

### Container Images

**Multi-stage Dockerfile**:
```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine

RUN apk add --no-cache tini curl

WORKDIR /app

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

USER nodejs

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Use tini as init
ENTRYPOINT ["/sbin/tini", "--"]

CMD ["node", "dist/server.js"]
```

**Build and Push to Artifact Registry**:
```bash
# Configure Docker for Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build image
docker build -t us-central1-docker.pkg.dev/my-project/my-repo/myapp:v1.0.0 .

# Tag as latest
docker tag \
  us-central1-docker.pkg.dev/my-project/my-repo/myapp:v1.0.0 \
  us-central1-docker.pkg.dev/my-project/my-repo/myapp:latest

# Push images
docker push us-central1-docker.pkg.dev/my-project/my-repo/myapp:v1.0.0
docker push us-central1-docker.pkg.dev/my-project/my-repo/myapp:latest

# Scan for vulnerabilities
gcloud artifacts docker images scan \
  us-central1-docker.pkg.dev/my-project/my-repo/myapp:v1.0.0
```

### Deployment Strategies

**Blue-Green Deployment with Terraform**:
```hcl
variable "active_version" {
  description = "Active deployment version (blue or green)"
  type        = string
  default     = "blue"
}

locals {
  blue_weight  = var.active_version == "blue" ? 100 : 0
  green_weight = var.active_version == "green" ? 100 : 0
}

# Blue instance group
resource "google_compute_region_instance_group_manager" "blue" {
  name               = "app-mig-blue"
  base_instance_name = "app-blue"
  region             = var.region

  version {
    instance_template = google_compute_instance_template.blue.id
  }

  target_size = var.active_version == "blue" ? var.instance_count : 0
}

# Green instance group
resource "google_compute_region_instance_group_manager" "green" {
  name               = "app-mig-green"
  base_instance_name = "app-green"
  region             = var.region

  version {
    instance_template = google_compute_instance_template.green.id
  }

  target_size = var.active_version == "green" ? var.instance_count : 0
}

# Load balancer backend
resource "google_compute_backend_service" "app" {
  name = "app-backend"

  backend {
    group           = google_compute_region_instance_group_manager.blue.instance_group
    balancing_mode  = "UTILIZATION"
    capacity_scaler = local.blue_weight / 100
  }

  backend {
    group           = google_compute_region_instance_group_manager.green.instance_group
    balancing_mode  = "UTILIZATION"
    capacity_scaler = local.green_weight / 100
  }

  health_checks = [google_compute_health_check.app.id]
}
```

**Canary Deployment**:
```hcl
variable "canary_percentage" {
  description = "Percentage of traffic to route to canary"
  type        = number
  default     = 10
}

resource "google_compute_backend_service" "app" {
  name = "app-backend"

  # Stable version
  backend {
    group           = google_compute_region_instance_group_manager.stable.instance_group
    balancing_mode  = "UTILIZATION"
    capacity_scaler = (100 - var.canary_percentage) / 100
  }

  # Canary version
  backend {
    group           = google_compute_region_instance_group_manager.canary.instance_group
    balancing_mode  = "UTILIZATION"
    capacity_scaler = var.canary_percentage / 100
  }

  health_checks = [google_compute_health_check.app.id]
}
```

## Infrastructure as Code Best Practices

### Module Design

**Reusable Module Structure**:
```
terraform/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── compute/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   └── gke/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── README.md
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       └── backend.tf
└── global/
    ├── iam/
    └── dns/
```

**Module Best Practices**:
1. One responsibility per module
2. Use meaningful variable names with descriptions
3. Define output values for resource references
4. Include README with usage examples
5. Version your modules
6. Use variable validation
7. Implement lifecycle rules for critical resources
8. Include default values where appropriate

### State File Management

**State File Security**:
```hcl
resource "google_storage_bucket" "terraform_state" {
  name          = "${var.project_id}-terraform-state"
  location      = "US"
  storage_class = "STANDARD"

  # Prevent accidental deletion
  force_destroy = false

  # Enable versioning for state file recovery
  versioning {
    enabled = true
  }

  # Uniform bucket-level access
  uniform_bucket_level_access = true

  # Encryption
  encryption {
    default_kms_key_name = google_kms_crypto_key.terraform_key.id
  }

  # Lifecycle rules to manage old versions
  lifecycle_rule {
    condition {
      num_newer_versions = 10
    }
    action {
      type = "Delete"
    }
  }

  # Audit logging
  logging {
    log_bucket        = google_storage_bucket.logs.name
    log_object_prefix = "terraform-state/"
  }
}

# IAM for state bucket
resource "google_storage_bucket_iam_binding" "terraform_state" {
  bucket = google_storage_bucket.terraform_state.name
  role   = "roles/storage.objectAdmin"

  members = [
    "serviceAccount:terraform@${var.project_id}.iam.gserviceaccount.com",
  ]
}
```

**State Isolation Strategies**:
1. Separate state files per environment
2. Use workspaces for similar environments
3. Separate state for different components (network, compute, data)
4. Never commit state files to Git
5. Enable state locking
6. Regular state backups
7. Use remote backends exclusively

### Secrets Handling

**Using Secret Manager in Terraform**:
```hcl
# Create secret
resource "google_secret_manager_secret" "db_password" {
  secret_id = "database-password"

  replication {
    automatic = true
  }
}

# Add secret version
resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}

# Grant access to secret
resource "google_secret_manager_secret_iam_member" "app_access" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app.email}"
}

# Read secret in data source
data "google_secret_manager_secret_version" "db_password" {
  secret  = "database-password"
  version = "latest"
}

# Use secret (marked as sensitive)
resource "google_sql_user" "user" {
  name     = "app_user"
  instance = google_sql_database_instance.main.name
  password = data.google_secret_manager_secret_version.db_password.secret_data

  lifecycle {
    ignore_changes = [password]
  }
}

# Mark outputs as sensitive
output "db_password" {
  value     = data.google_secret_manager_secret_version.db_password.secret_data
  sensitive = true
}
```

**Never Store Secrets in Code**:
```hcl
# BAD - Never do this
resource "google_sql_user" "bad" {
  password = "hardcoded-password-123"  # NEVER DO THIS
}

# GOOD - Use Secret Manager
resource "google_sql_user" "good" {
  password = data.google_secret_manager_secret_version.db_password.secret_data
}

# GOOD - Use random provider
resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}
```

### CI/CD Integration

**Cloud Build Pipeline for Terraform**:
```yaml
# cloudbuild.yaml
steps:
  # Terraform Init
  - name: 'hashicorp/terraform:1.6'
    id: 'terraform-init'
    args:
      - 'init'
      - '-backend-config=bucket=${_STATE_BUCKET}'
      - '-backend-config=prefix=${_ENVIRONMENT}/terraform/state'
    dir: 'terraform'

  # Terraform Validate
  - name: 'hashicorp/terraform:1.6'
    id: 'terraform-validate'
    args:
      - 'validate'
    dir: 'terraform'
    waitFor: ['terraform-init']

  # Terraform Format Check
  - name: 'hashicorp/terraform:1.6'
    id: 'terraform-fmt'
    args:
      - 'fmt'
      - '-check'
      - '-recursive'
    dir: 'terraform'
    waitFor: ['terraform-init']

  # TFLint
  - name: 'ghcr.io/terraform-linters/tflint'
    id: 'tflint'
    args:
      - '--init'
    dir: 'terraform'
    waitFor: ['terraform-init']

  - name: 'ghcr.io/terraform-linters/tflint'
    args:
      - '--format=compact'
    dir: 'terraform'
    waitFor: ['tflint']

  # Terraform Plan
  - name: 'hashicorp/terraform:1.6'
    id: 'terraform-plan'
    args:
      - 'plan'
      - '-var-file=environments/${_ENVIRONMENT}.tfvars'
      - '-out=tfplan'
    dir: 'terraform'
    waitFor: ['terraform-validate', 'terraform-fmt']

  # Save plan for review
  - name: 'gcr.io/cloud-builders/gsutil'
    args:
      - 'cp'
      - 'terraform/tfplan'
      - 'gs://${_STATE_BUCKET}/${_ENVIRONMENT}/plans/${BUILD_ID}.tfplan'
    waitFor: ['terraform-plan']

  # Terraform Apply (only on main branch)
  - name: 'hashicorp/terraform:1.6'
    id: 'terraform-apply'
    args:
      - 'apply'
      - '-auto-approve'
      - 'tfplan'
    dir: 'terraform'
    waitFor: ['terraform-plan']

substitutions:
  _ENVIRONMENT: 'dev'
  _STATE_BUCKET: 'my-terraform-state-bucket'

options:
  logging: CLOUD_LOGGING_ONLY
  machineType: 'N1_HIGHCPU_8'

timeout: '1800s'
```

**GitHub Actions for Terraform**:
```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
    paths:
      - 'terraform/**'
  pull_request:
    branches: [main]
    paths:
      - 'terraform/**'

env:
  TF_VERSION: '1.6.0'
  GOOGLE_CREDENTIALS: ${{ secrets.GCP_SA_KEY }}

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: terraform

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        run: |
          terraform init \
            -backend-config="bucket=${{ secrets.TF_STATE_BUCKET }}" \
            -backend-config="prefix=${{ github.ref_name }}/terraform/state"

      - name: Terraform Format
        run: terraform fmt -check -recursive

      - name: Terraform Validate
        run: terraform validate

      - name: TFLint
        uses: terraform-linters/setup-tflint@v3
        with:
          tflint_version: latest

      - name: Run TFLint
        run: tflint --init && tflint -f compact

      - name: Terraform Plan
        id: plan
        run: |
          terraform plan \
            -var-file=environments/${{ github.ref_name }}.tfvars \
            -no-color \
            -out=tfplan
        continue-on-error: true

      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const output = `#### Terraform Plan \`${{ steps.plan.outcome }}\`

            <details><summary>Show Plan</summary>

            \`\`\`
            ${{ steps.plan.outputs.stdout }}
            \`\`\`

            </details>`;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            })

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve tfplan
```

**Deployment Manager with Cloud Build**:
```yaml
# cloudbuild.yaml
steps:
  # Validate deployment
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'deployment-manager'
      - 'deployments'
      - 'create'
      - '${_DEPLOYMENT_NAME}-${BUILD_ID}'
      - '--config'
      - 'config.yaml'
      - '--preview'

  # Apply deployment (only on main branch)
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'deployment-manager'
      - 'deployments'
      - 'update'
      - '${_DEPLOYMENT_NAME}-${BUILD_ID}'

substitutions:
  _DEPLOYMENT_NAME: 'production-infrastructure'

options:
  logging: CLOUD_LOGGING_ONLY

timeout: '1200s'
```

## gcloud Commands for Infrastructure Automation

### Terraform-related Commands

```bash
# Service Account for Terraform
gcloud iam service-accounts create terraform \
  --display-name="Terraform Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:terraform@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/editor"

# Create key for service account
gcloud iam service-accounts keys create terraform-key.json \
  --iam-account=terraform@PROJECT_ID.iam.gserviceaccount.com

# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable deploymentmanager.googleapis.com
```

### Deployment Manager Commands

```bash
# Create deployment
gcloud deployment-manager deployments create my-deployment \
  --config config.yaml \
  --description "Production infrastructure"

# Create with preview
gcloud deployment-manager deployments create my-deployment \
  --config config.yaml \
  --preview

# Update deployment
gcloud deployment-manager deployments update my-deployment \
  --config config.yaml \
  --delete-policy ABANDON  # or DELETE

# Cancel preview
gcloud deployment-manager deployments cancel-preview my-deployment

# Delete deployment
gcloud deployment-manager deployments delete my-deployment \
  --delete-policy DELETE  # or ABANDON

# List deployments
gcloud deployment-manager deployments list

# Describe deployment
gcloud deployment-manager deployments describe my-deployment

# View manifest
gcloud deployment-manager manifests describe MANIFEST_ID \
  --deployment my-deployment

# List resources in deployment
gcloud deployment-manager resources list \
  --deployment my-deployment

# Describe resource
gcloud deployment-manager resources describe RESOURCE_NAME \
  --deployment my-deployment

# View deployment operations
gcloud deployment-manager operations list

# Describe operation
gcloud deployment-manager operations describe OPERATION_ID
```

### Instance Template Commands

```bash
# Create instance template
gcloud compute instance-templates create web-template \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-standard \
  --network=default \
  --subnet=default \
  --metadata=startup-script='#!/bin/bash
apt-get update
apt-get install -y nginx' \
  --tags=http-server,https-server

# List instance templates
gcloud compute instance-templates list

# Describe instance template
gcloud compute instance-templates describe web-template

# Delete instance template
gcloud compute instance-templates delete web-template
```

## Troubleshooting Scenarios

### Scenario 1: Terraform State Lock Timeout

**Problem**: Terraform operations fail with state lock timeout error.

**Error Message**:
```
Error: Error acquiring the state lock
Error message: 2 errors occurred:
  * writing "gs://bucket/path/default.tflock" failed: googleapi: Error 412
```

**Resolution Steps**:

1. Check if another Terraform operation is running:
```bash
# Check Cloud Build jobs
gcloud builds list --ongoing

# Check for manual terraform processes
ps aux | grep terraform
```

2. Verify state lock file exists:
```bash
# Check for lock file
gsutil ls gs://my-terraform-state-bucket/env/prod/default.tflock
```

3. If lock is stale (no active process), force unlock:
```bash
# Get lock ID from error message
terraform force-unlock LOCK_ID

# Verify unlock
terraform plan
```

4. If problem persists, check bucket permissions:
```bash
# Verify service account has proper access
gcloud storage buckets get-iam-policy gs://my-terraform-state-bucket

# Grant storage.objectAdmin if needed
gcloud storage buckets add-iam-policy-binding \
  gs://my-terraform-state-bucket \
  --member="serviceAccount:terraform@project.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

5. Prevent future issues:
```hcl
# Add timeout configuration
terraform {
  backend "gcs" {
    bucket = "my-terraform-state-bucket"
    prefix = "terraform/state"

    # Add explicit timeout
    lock_timeout = "5m"
  }
}
```

### Scenario 2: Deployment Manager Template Expansion Error

**Problem**: Deployment Manager fails with template expansion error.

**Error Message**:
```
ERROR: Error in Operation: code: INVALID_PROPERTY
message: Invalid value for field 'resource.properties': Value does not match pattern
```

**Resolution Steps**:

1. Validate YAML syntax locally:
```bash
# Install yamllint
pip install yamllint

# Validate YAML
yamllint config.yaml

# Check with Python
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

2. Expand template locally to check for errors:
```bash
# Expand template
gcloud deployment-manager deployments create test-expand \
  --config config.yaml \
  --preview

# View expanded manifest
gcloud deployment-manager manifests describe \
  $(gcloud deployment-manager manifests list --deployment=test-expand --format="value(name)" --limit=1) \
  --deployment=test-expand

# Cancel preview
gcloud deployment-manager deployments cancel-preview test-expand
```

3. Check Jinja2 template syntax:
```python
# test_template.py
from jinja2 import Template, TemplateSyntaxError

try:
    with open('network.jinja', 'r') as f:
        template = Template(f.read())
    print("Template syntax is valid")
except TemplateSyntaxError as e:
    print(f"Template error: {e}")
```

4. Validate property names against API schema:
```bash
# Get resource schema
gcloud deployment-manager types describe compute.v1.instance

# Check property requirements
gcloud deployment-manager types describe container.v1.cluster
```

5. Add debug output to template:
```jinja
# Add to template for debugging
outputs:
- name: debug-properties
  value: {{ properties | tojson }}
```

### Scenario 3: Terraform Resource Drift Detected

**Problem**: Resources were modified outside of Terraform, causing drift.

**Resolution Steps**:

1. Detect drift:
```bash
# Run plan to see differences
terraform plan -detailed-exitcode

# Exit code 2 means changes detected
echo $?
```

2. View specific drift:
```bash
# Show current state
terraform show

# Compare with actual resources
terraform plan -out=tfplan
terraform show -json tfplan | jq '.resource_changes'
```

3. Refresh state to match reality:
```bash
# Update state without modifying resources
terraform refresh

# Verify changes
terraform plan
```

4. Import manually created resources:
```bash
# Import resource into state
terraform import google_compute_instance.web projects/PROJECT/zones/ZONE/instances/INSTANCE_NAME

# Verify import
terraform plan
```

5. Update configuration to match reality:
```hcl
# Option 1: Update HCL to match actual state
resource "google_compute_instance" "web" {
  # Update properties to match actual resource
  machine_type = "e2-standard-4"  # Updated from e2-medium
}

# Option 2: Force replacement
resource "google_compute_instance" "web" {
  # ...
  lifecycle {
    create_before_destroy = true
  }
}
```

6. Implement drift detection in CI/CD:
```yaml
# cloudbuild.yaml
steps:
  - name: 'hashicorp/terraform:1.6'
    args:
      - 'plan'
      - '-detailed-exitcode'
    id: 'drift-detection'
    continueOnError: true

  - name: 'gcr.io/cloud-builders/gcloud'
    script: |
      if [ ${_DRIFT_EXIT_CODE} -eq 2 ]; then
        echo "Drift detected! Sending alert..."
        gcloud pubsub topics publish drift-alerts \
          --message="Drift detected in ${_ENVIRONMENT}"
      fi
```

### Scenario 4: GKE Cluster Creation Fails in Terraform

**Problem**: Terraform fails to create GKE cluster with IP allocation error.

**Error Message**:
```
Error: Error creating Cluster: googleapi: Error 400: IP space exhausted
```

**Resolution Steps**:

1. Check IP ranges:
```bash
# List subnets and IP ranges
gcloud compute networks subnets describe SUBNET_NAME \
  --region=REGION \
  --format="value(ipCidrRange,secondaryIpRanges)"

# Calculate required IPs
# Formula: Pods = nodes * max-pods-per-node
# Default max-pods-per-node = 110
```

2. Fix IP allocation in Terraform:
```hcl
resource "google_compute_subnetwork" "gke_subnet" {
  name          = "gke-subnet"
  ip_cidr_range = "10.0.0.0/20"  # Primary range
  region        = var.region
  network       = google_compute_network.vpc.id

  # Pods - needs /14 for large clusters
  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.4.0.0/14"  # Increased from /16
  }

  # Services - needs /20 minimum
  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.8.0.0/20"
  }
}

resource "google_container_cluster" "primary" {
  # ... other config ...

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Reduce max pods per node if needed
  default_max_pods_per_node = 64  # Default is 110
}
```

3. Verify ranges don't overlap:
```bash
# Check all subnet ranges
gcloud compute networks subnets list \
  --network=VPC_NAME \
  --format="table(name,ipCidrRange,secondaryIpRanges)"
```

4. Apply fix:
```bash
# Plan to verify changes
terraform plan

# Apply changes
terraform apply
```

### Scenario 5: Packer Build Fails with Permission Denied

**Problem**: Packer cannot create VM image due to permission errors.

**Error Message**:
```
Error: Error setting up communicator: ssh: handshake failed: Permission denied
```

**Resolution Steps**:

1. Check service account permissions:
```bash
# List service account permissions
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:packer@*"

# Grant required roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:packer@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/compute.instanceAdmin.v1"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:packer@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

2. Enable OS Login or use SSH keys:
```hcl
// Packer template with OS Login
source "googlecompute" "web" {
  // ...
  use_os_login = true

  // Or use SSH keys
  ssh_username = "packer"

  // Metadata for SSH
  metadata = {
    enable-oslogin = "FALSE"
  }
}
```

3. Check firewall rules:
```bash
# Verify SSH access for Packer
gcloud compute firewall-rules list \
  --filter="allowed[].ports:22"

# Create firewall rule if needed
gcloud compute firewall-rules create allow-packer-ssh \
  --network=default \
  --allow=tcp:22 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=packer
```

4. Update Packer template:
```hcl
source "googlecompute" "web" {
  project_id          = var.project_id
  zone                = var.zone
  source_image_family = "debian-11"
  ssh_username        = "packer"

  // Add network tags for firewall
  tags = ["packer"]

  // Use internal IP if building from GCP
  use_internal_ip = false

  // Enable OS Login
  use_os_login = true
}
```

### Scenario 6: Cloud SQL Private IP Connection Fails

**Problem**: Terraform creates Cloud SQL with private IP but connection fails.

**Error Message**:
```
Error: Error connecting to Cloud SQL instance: connection timeout
```

**Resolution Steps**:

1. Verify VPC peering:
```bash
# Check VPC peering
gcloud compute networks peerings list \
  --network=VPC_NAME

# Check allocated IP ranges
gcloud compute addresses list \
  --global \
  --filter="purpose=VPC_PEERING"
```

2. Create private service connection:
```hcl
# Allocate IP range for private service connection
resource "google_compute_global_address" "private_ip_address" {
  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

# Create private VPC connection
resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

# Cloud SQL with private IP (depends on VPC connection)
resource "google_sql_database_instance" "postgres" {
  name             = "postgres-instance"
  database_version = "POSTGRES_14"
  region           = var.region

  depends_on = [google_service_networking_connection.private_vpc_connection]

  settings {
    tier = "db-custom-2-7680"

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
      require_ssl     = false  # For private IP connections
    }
  }
}
```

3. Enable Service Networking API:
```bash
gcloud services enable servicenetworking.googleapis.com
```

4. Verify connectivity:
```bash
# From a VM in the same VPC
gcloud compute ssh VM_NAME -- \
  psql "host=PRIVATE_IP user=USER dbname=DB password=PASSWORD"
```

### Scenario 7: Terraform Module Version Conflict

**Problem**: Terraform module version constraints cause initialization failure.

**Error Message**:
```
Error: Failed to query available provider packages
Could not retrieve the list of available versions: no matching version found
```

**Resolution Steps**:

1. Check version constraints:
```hcl
# In terraform.tf or main.tf
terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"  # Check this constraint
    }
  }
}
```

2. Update provider versions:
```bash
# Show current providers
terraform providers

# Upgrade providers
terraform init -upgrade

# Lock to specific version if needed
terraform init -upgrade=false
```

3. Fix version constraints:
```hcl
# Be specific with version constraints
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0, < 6.0"  # More explicit
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 5.0, < 6.0"
    }
  }
}
```

4. Generate and commit lock file:
```bash
# Generate lock file
terraform init

# Commit .terraform.lock.hcl to version control
git add .terraform.lock.hcl
git commit -m "Add provider lock file"
```

5. Handle module version conflicts:
```hcl
# Use exact module versions
module "vpc" {
  source  = "terraform-google-modules/network/google"
  version = "= 7.0.0"  # Exact version
  # ...
}

# Or use version range
module "gke" {
  source  = "terraform-google-modules/kubernetes-engine/google"
  version = "~> 28.0"  # Compatible with 28.x
  # ...
}
```

### Scenario 8: Deployment Manager Update Conflicts

**Problem**: Deployment Manager update fails due to resource conflicts.

**Error Message**:
```
ERROR: code: RESOURCE_ERROR
message: The resource 'projects/PROJECT/global/networks/vpc-network' already exists
```

**Resolution Steps**:

1. Check current deployment:
```bash
# Describe deployment
gcloud deployment-manager deployments describe DEPLOYMENT_NAME

# List resources
gcloud deployment-manager resources list \
  --deployment=DEPLOYMENT_NAME
```

2. Update with ABANDON policy for removed resources:
```bash
# Update deployment, abandoning removed resources
gcloud deployment-manager deployments update DEPLOYMENT_NAME \
  --config config.yaml \
  --delete-policy ABANDON

# Or delete specific resources
gcloud deployment-manager deployments update DEPLOYMENT_NAME \
  --config config.yaml \
  --delete-policy DELETE
```

3. Import existing resources into deployment:
```yaml
# config.yaml - reference existing resources
resources:
- name: existing-network
  type: compute.v1.network
  properties:
    # Reference existing resource
    name: vpc-network
    # Use 'external' to reference existing resources
  metadata:
    dependsOn: []
```

4. Use CREATE_OR_ACQUIRE policy:
```yaml
# In template
resources:
- name: vpc-network
  type: compute.v1.network
  properties:
    name: vpc-network
    autoCreateSubnetworks: false
  # This allows using existing resources
  acquisitionPolicy: CREATE_OR_ACQUIRE
```

5. Delete and recreate if necessary:
```bash
# Delete deployment (keep resources)
gcloud deployment-manager deployments delete DEPLOYMENT_NAME \
  --delete-policy ABANDON

# Recreate deployment
gcloud deployment-manager deployments create DEPLOYMENT_NAME \
  --config config.yaml
```

## Tool Selection and Comparison

### Terraform vs Cloud Deployment Manager

| Feature | Terraform | Deployment Manager |
|---------|-----------|-------------------|
| **Multi-cloud** | Yes (AWS, Azure, GCP) | No (GCP only) |
| **State Management** | Remote state with locking | Server-side managed |
| **Template Language** | HCL | YAML/Jinja2/Python |
| **Module Ecosystem** | Large (Terraform Registry) | Limited |
| **Preview Changes** | `terraform plan` | `--preview` flag |
| **Import Resources** | Supported | Limited |
| **Learning Curve** | Moderate | Easy for GCP users |
| **CI/CD Integration** | Excellent | Good |
| **Cost** | Free (Terraform Cloud paid) | Free |
| **GCP Integration** | Excellent | Native |
| **Drift Detection** | Built-in | Manual |
| **Best For** | Multi-cloud, complex infrastructure | GCP-only, simple deployments |

**When to Use Terraform**:
- Multi-cloud infrastructure
- Complex state management needs
- Large module ecosystem required
- Advanced drift detection needed
- Team familiar with HCL

**When to Use Deployment Manager**:
- GCP-only infrastructure
- Integration with GCP workflows
- Team comfortable with YAML/Jinja2
- Simple to moderate complexity
- Native GCP tooling preference

## Exam Tips and Common Pitfalls

### Terraform Exam Tips

1. **State File Management**:
   - Always use remote backends for production
   - Never commit state files to Git
   - GCS provides automatic locking
   - Use separate state files per environment
   - Enable versioning on state buckets

2. **Common Traps**:
   - Forgetting to run `terraform init` after backend changes
   - Not using `-target` flag carefully (affects dependencies)
   - Ignoring `terraform fmt` and `terraform validate`
   - Hardcoding values instead of using variables
   - Not marking sensitive outputs as sensitive

3. **Resource Dependencies**:
   - Use `depends_on` for implicit dependencies
   - Understand `create_before_destroy` lifecycle
   - Know when to use `prevent_destroy`
   - Circular dependencies break execution

4. **Workspaces vs Separate Directories**:
   - Workspaces share same code, different state
   - Separate directories for completely isolated environments
   - Workspaces good for temporary environments
   - Production should use separate state files

### Deployment Manager Exam Tips

1. **Template Best Practices**:
   - Use Jinja2 for dynamic templates
   - Python templates for complex logic
   - Schema files for validation
   - Composite types for reusability

2. **Common Mistakes**:
   - Not using `$(ref.resource.property)` for references
   - Forgetting to use `--preview` before apply
   - Not handling dependencies correctly
   - Improper use of outputs

3. **Update Policies**:
   - `DELETE` - deletes removed resources
   - `ABANDON` - leaves removed resources
   - Know when to use each
   - Preview before updating

### Infrastructure as Code General Tips

1. **Secrets Management**:
   - Never hardcode secrets
   - Use Secret Manager for sensitive data
   - Mark outputs as sensitive
   - Rotate credentials regularly
   - Use service account impersonation

2. **Module Design**:
   - Single responsibility principle
   - Version your modules
   - Document inputs and outputs
   - Include examples
   - Test modules independently

3. **State Management Gotchas**:
   - State lock timeouts during long operations
   - Corrupted state files (use versioning)
   - State drift from manual changes
   - Importing existing resources correctly
   - Moving resources between modules

4. **CI/CD Integration**:
   - Always run `plan` before `apply`
   - Use `-detailed-exitcode` for drift detection
   - Implement approval gates for production
   - Save plan files for audit
   - Automate formatting checks

5. **Common Exam Scenarios**:
   - Choosing between Terraform and Deployment Manager
   - Implementing blue-green deployments
   - Managing secrets securely
   - Handling state file conflicts
   - Implementing drift detection
   - Designing module structures
   - CI/CD pipeline integration

6. **Remember for Exam**:
   - Terraform uses `=` for version constraints
   - `~>` allows rightmost version component to increment
   - GCS backend automatically locks state
   - Deployment Manager keeps history of deployments
   - `terraform import` doesn't generate configuration
   - Use `data` sources for existing resources
   - Workspaces share configuration, not state
   - Private GKE clusters need IP ranges for pods/services

## Additional Resources

- [Terraform on GCP](https://cloud.google.com/docs/terraform)
- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Cloud Deployment Manager](https://cloud.google.com/deployment-manager/docs)
- [IaC Best Practices](https://cloud.google.com/architecture/devops/devops-tech-infrastructure-as-code)
- [Terraform Modules](https://github.com/terraform-google-modules)
- [Packer GCP Builder](https://www.packer.io/plugins/builders/googlecompute)
- [Ansible GCP Collection](https://docs.ansible.com/ansible/latest/collections/google/cloud/index.html)

## Key terms

- **Terraform** - an infrastructure as code tool that provisions resources from declarative configuration files.
- **Config Connector** - a Kubernetes add-on that manages Google Cloud resources through Kubernetes custom resources.
- **Deployment Manager** - the older Google Cloud service that creates resources from YAML templates.
- **Infrastructure as code** - managing infrastructure through versioned, reviewable definition files instead of manual changes.
