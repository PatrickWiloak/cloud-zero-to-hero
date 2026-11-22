# IBM Cloud Professional Architect (C1000-172, retired) - Security, Compliance & Optimization

## Table of Contents
- [Enterprise Security Architecture](#enterprise-security-architecture)
- [Compliance and Governance](#compliance-and-governance)
- [Cost Optimization](#cost-optimization)
- [Performance Optimization](#performance-optimization)
- [Migration Strategies](#migration-strategies)
- [Enterprise Patterns](#enterprise-patterns)

---

## Enterprise Security Architecture

### Zero Trust Architecture
```yaml
# zero-trust-architecture.yaml
zero_trust_principles:
  verify_explicitly:
    - Multi-factor authentication
    - Continuous authentication
    - Risk-based access control
    - Device health validation

  least_privilege_access:
    - Just-in-time access
    - Just-enough-access
    - Time-bound permissions
    - Attribute-based access control

  assume_breach:
    - Micro-segmentation
    - Lateral movement prevention
    - Continuous monitoring
    - Automated threat response

implementation:
  identity:
    service: "IBM Cloud IAM"
    features:
      - Service IDs for applications
      - Access groups for user management
      - Trusted profiles for workloads
      - Context-based restrictions

  network:
    service: "VPC Security Groups + Network ACLs"
    features:
      - Micro-segmentation
      - Private endpoints
      - Virtual Private Endpoints
      - Security Group rules per workload

  data:
    service: "IBM Key Protect / Hyper Protect Crypto Services"
    features:
      - Encryption at rest
      - Encryption in transit
      - Key rotation
      - BYOK/KYOK

  monitoring:
    service: "Security and Compliance Center"
    features:
      - Continuous compliance monitoring
      - Threat detection
      - Vulnerability management
      - Audit logging
```

### Security Layers Architecture
```python
# enterprise_security.py
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import IamIdentityV1, IamAccessGroupsV2
from ibm_vpc import VpcV1
import json

class EnterpriseSecurityArchitecture:
    """
    Implement enterprise security architecture on IBM Cloud
    """

    def __init__(self, api_key):
        authenticator = IAMAuthenticator(api_key)

        self.iam = IamIdentityV1(authenticator=authenticator)
        self.access_groups = IamAccessGroupsV2(authenticator=authenticator)
        self.vpc = VpcV1('2023-12-19', authenticator=authenticator)

    def implement_least_privilege(self, account_id):
        """Implement least privilege access"""

        # Create access groups for different roles
        groups = {
            'developers': {
                'description': 'Development team access',
                'policies': [
                    {
                        'roles': ['Editor'],
                        'resource_attributes': [
                            {'name': 'resourceGroupId', 'value': 'dev-rg'},
                            {'name': 'serviceType', 'value': 'platform_service'}
                        ]
                    }
                ]
            },
            'operators': {
                'description': 'Operations team access',
                'policies': [
                    {
                        'roles': ['Operator', 'Viewer'],
                        'resource_attributes': [
                            {'name': 'resourceGroupId', 'value': 'prod-rg'}
                        ]
                    }
                ]
            },
            'security-auditors': {
                'description': 'Security audit access',
                'policies': [
                    {
                        'roles': ['Viewer', 'Reader'],
                        'resource_attributes': [
                            {'name': 'serviceType', 'value': 'platform_service'}
                        ]
                    }
                ]
            }
        }

        created_groups = {}
        for group_name, config in groups.items():
            # Create access group
            group = self.access_groups.create_access_group(
                account_id=account_id,
                name=group_name,
                description=config['description']
            ).get_result()

            created_groups[group_name] = group['id']

            # Assign policies
            for policy in config['policies']:
                self.create_access_policy(group['id'], account_id, policy)

        return created_groups

    def implement_network_segmentation(self, vpc_id):
        """Implement network micro-segmentation"""

        # Create security groups for different tiers
        security_groups = {
            'web-tier-sg': {
                'rules': [
                    {'direction': 'inbound', 'protocol': 'tcp', 'port_min': 443, 'port_max': 443, 'remote': '0.0.0.0/0'},
                    {'direction': 'inbound', 'protocol': 'tcp', 'port_min': 80, 'port_max': 80, 'remote': '0.0.0.0/0'},
                    {'direction': 'outbound', 'protocol': 'all'}
                ]
            },
            'app-tier-sg': {
                'rules': [
                    {'direction': 'inbound', 'protocol': 'tcp', 'port_min': 8080, 'port_max': 8080, 'remote_sg': 'web-tier-sg'},
                    {'direction': 'outbound', 'protocol': 'all'}
                ]
            },
            'data-tier-sg': {
                'rules': [
                    {'direction': 'inbound', 'protocol': 'tcp', 'port_min': 5432, 'port_max': 5432, 'remote_sg': 'app-tier-sg'},
                    {'direction': 'outbound', 'protocol': 'all'}
                ]
            }
        }

        created_sgs = {}
        for sg_name, config in security_groups.items():
            # Create security group
            sg = self.vpc.create_security_group(
                vpc={'id': vpc_id},
                name=sg_name
            ).get_result()

            created_sgs[sg_name] = sg['id']

            # Add rules
            for rule in config['rules']:
                self.add_security_group_rule(sg['id'], rule)

        return created_sgs

    def implement_data_encryption(self):
        """Implement comprehensive data encryption"""

        encryption_config = {
            'at_rest': {
                'service': 'Key Protect',
                'features': [
                    'Customer-managed keys',
                    'Automatic key rotation',
                    'Envelope encryption',
                    'Dual authorization'
                ]
            },
            'in_transit': {
                'protocols': ['TLS 1.3'],
                'certificate_management': 'IBM Secrets Manager',
                'mutual_tls': 'For service-to-service communication'
            },
            'in_use': {
                'service': 'Hyper Protect Services',
                'features': [
                    'Confidential computing',
                    'Secure enclaves',
                    'Encrypted memory'
                ]
            }
        }

        return encryption_config

# Terraform for enterprise security
security_tf = '''
# enterprise-security.tf

# IAM Access Groups
resource "ibm_iam_access_group" "developers" {
  name        = "Developers"
  description = "Development team access"
}

resource "ibm_iam_access_group_policy" "developer_policy" {
  access_group_id = ibm_iam_access_group.developers.id
  roles           = ["Editor"]

  resources {
    resource_group_id = ibm_resource_group.dev.id
  }
}

# VPC Security Groups
resource "ibm_is_security_group" "web_tier" {
  name = "web-tier-sg"
  vpc  = ibm_is_vpc.enterprise_vpc.id
}

resource "ibm_is_security_group_rule" "web_inbound_https" {
  group     = ibm_is_security_group.web_tier.id
  direction = "inbound"
  remote    = "0.0.0.0/0"
  tcp {
    port_min = 443
    port_max = 443
  }
}

# Key Protect for encryption
resource "ibm_resource_instance" "key_protect" {
  name              = "enterprise-key-protect"
  service           = "kms"
  plan              = "tiered-pricing"
  location          = "us-south"
  resource_group_id = data.ibm_resource_group.default.id
}

resource "ibm_kms_key" "root_key" {
  instance_id  = ibm_resource_instance.key_protect.guid
  key_name     = "root-key"
  standard_key = false
  force_delete = false
}

# Enable encryption for resources
resource "ibm_database" "encrypted_postgres" {
  name              = "encrypted-database"
  plan              = "standard"
  location          = "us-south"
  service           = "databases-for-postgresql"
  resource_group_id = data.ibm_resource_group.default.id

  key_protect_key = ibm_kms_key.root_key.id

  group {
    group_id = "member"
    memory {
      allocation_mb = 4096
    }
  }
}

# Context-based restrictions
resource "ibm_cbr_zone" "enterprise_zone" {
  name        = "enterprise-allowed-zone"
  description = "Zone for enterprise network"
  account_id  = data.ibm_account.account.id

  addresses {
    type  = "ipRange"
    value = "10.0.0.0/8"
  }

  addresses {
    type = "vpc"
    ref  = ibm_is_vpc.enterprise_vpc.crn
  }
}

resource "ibm_cbr_rule" "restrict_access" {
  description      = "Restrict resource access to enterprise zone"
  context_attributes {
    name  = "networkZoneId"
    value = ibm_cbr_zone.enterprise_zone.id
  }

  resources {
    attributes {
      name  = "accountId"
      value = data.ibm_account.account.id
    }
    attributes {
      name  = "serviceType"
      value = "platform_service"
    }
  }

  enforcement_mode = "enabled"
}
'''
```

---

## Compliance and Governance

### Compliance Framework
```yaml
# compliance-framework.yaml
regulatory_requirements:
  financial_services:
    - PCI DSS (Payment Card Industry)
    - SOX (Sarbanes-Oxley)
    - GLBA (Gramm-Leach-Bliley Act)
    ibm_solutions:
      - IBM Cloud for Financial Services
      - Hyper Protect Services
      - Security and Compliance Center

  healthcare:
    - HIPAA (Health Insurance Portability)
    - HITRUST
    ibm_solutions:
      - HIPAA-ready services
      - BAA (Business Associate Agreement)
      - Data encryption and audit logging

  government:
    - FedRAMP
    - FISMA
    - ITAR
    ibm_solutions:
      - FedRAMP authorized services
      - Government-specific regions
      - Enhanced security features

  data_privacy:
    - GDPR (General Data Protection Regulation)
    - CCPA (California Consumer Privacy Act)
    - LGPD (Brazil)
    ibm_solutions:
      - Data residency controls
      - Right to be forgotten
      - Data processing agreements

compliance_controls:
  identity_and_access:
    - Multi-factor authentication
    - Privileged access management
    - Access reviews and recertification
    - Segregation of duties

  data_protection:
    - Encryption (at rest, in transit, in use)
    - Data classification and labeling
    - Data loss prevention
    - Backup and recovery

  monitoring_and_logging:
    - Activity Tracker for audit logs
    - Security and Compliance Center
    - Anomaly detection
    - Incident response

  vulnerability_management:
    - Regular security assessments
    - Vulnerability scanning
    - Patch management
    - Penetration testing
```

### Governance Implementation
```bash
# governance-implementation.sh

# 1. Set up Security and Compliance Center
ibmcloud resource service-instance-create \
  enterprise-scc \
  security-compliance \
  standard \
  us-south

# 2. Create compliance profile
ibmcloud scc profile-create \
  --name "Enterprise Security Profile" \
  --description "Compliance controls for enterprise" \
  --profile-type custom

# 3. Attach compliance profile to account
ibmcloud scc attachment-create \
  --profile-id $PROFILE_ID \
  --name "Account Compliance" \
  --scope-type account \
  --scope-id $ACCOUNT_ID

# 4. Schedule regular scans
ibmcloud scc scan-create \
  --attachment-id $ATTACHMENT_ID \
  --schedule "0 2 * * *"  # Daily at 2 AM

# 5. Configure Activity Tracker for audit logging
ibmcloud resource service-instance-create \
  enterprise-activity-tracker \
  logdnaat \
  7-day \
  us-south

# 6. Route all events to Activity Tracker
ibmcloud atracker route create \
  --name enterprise-audit-route \
  --target-id $TARGET_ID \
  --locations us-south,us-east,eu-de

# 7. Enable Flow Logs for network monitoring
ibmcloud is flow-log-create \
  network-flow-logs \
  --bucket $COS_BUCKET \
  --target $VPC_ID

# 8. Set up Security Advisor
ibmcloud security-advisor findings list
```

---

## Cost Optimization

### Cost Optimization Strategies
```yaml
# cost-optimization.yaml
cost_optimization_pillars:
  right_sizing:
    compute:
      - Profile optimization (CPU/memory ratio)
      - Instance family selection
      - Reserved capacity for predictable workloads
      - Spot instances for fault-tolerant workloads

    storage:
      - Storage class selection (Standard, Smart Tier, Vault, Cold Vault)
      - Lifecycle policies for data archival
      - Compression and deduplication
      - Delete unused volumes and snapshots

    database:
      - Right-size allocations (CPU, memory, disk)
      - Read replicas for scale-out
      - Connection pooling
      - Query optimization

  auto_scaling:
    kubernetes:
      - Horizontal Pod Autoscaler (HPA)
      - Vertical Pod Autoscaler (VPA)
      - Cluster Autoscaler
      - Scheduled scaling

    instances:
      - Auto-scale groups
      - Schedule-based scaling
      - Metric-based scaling
      - Predictive scaling

  purchasing_options:
    on_demand: "Pay as you go"
    reserved: "1-year or 3-year commitments for predictable workloads"
    savings_plans: "Flexible commitment with discounts"
    spot: "Up to 90% discount for interruptible workloads"

  resource_management:
    tagging:
      - Cost center tags
      - Environment tags
      - Owner tags
      - Project tags

    monitoring:
      - Usage dashboards
      - Budget alerts
      - Anomaly detection
      - Cost allocation reports

    governance:
      - Resource quotas
      - Approval workflows
      - Policy enforcement
      - Idle resource detection
```

### Cost Optimization Implementation
```python
# cost_optimizer.py
from datetime import datetime, timedelta
import json

class IBMCloudCostOptimizer:
    """Identify and implement cost optimization opportunities"""

    def __init__(self, usage_data):
        self.usage_data = usage_data

    def identify_idle_resources(self):
        """Find idle and underutilized resources"""
        idle_resources = {
            'instances': [],
            'volumes': [],
            'load_balancers': [],
            'databases': []
        }

        # Analyze compute instances
        for instance in self.usage_data.get('instances', []):
            if instance.get('cpu_utilization', 0) < 5:
                idle_resources['instances'].append({
                    'id': instance['id'],
                    'name': instance['name'],
                    'cost_per_month': instance['cost'],
                    'recommendation': 'Stop or terminate',
                    'potential_savings': instance['cost']
                })
            elif instance.get('cpu_utilization', 0) < 30:
                # Right-size recommendation
                current_profile = instance['profile']
                recommended_profile = self._recommend_smaller_profile(current_profile)
                idle_resources['instances'].append({
                    'id': instance['id'],
                    'name': instance['name'],
                    'cost_per_month': instance['cost'],
                    'recommendation': f'Right-size to {recommended_profile}',
                    'potential_savings': instance['cost'] * 0.5
                })

        # Analyze storage volumes
        for volume in self.usage_data.get('volumes', []):
            if not volume.get('attached_instances'):
                idle_resources['volumes'].append({
                    'id': volume['id'],
                    'name': volume['name'],
                    'size_gb': volume['size'],
                    'cost_per_month': volume['cost'],
                    'recommendation': 'Delete unused volume',
                    'potential_savings': volume['cost']
                })

        return idle_resources

    def optimize_storage_costs(self):
        """Optimize storage costs with lifecycle policies"""
        recommendations = []

        for bucket in self.usage_data.get('cos_buckets', []):
            # Analyze object age
            objects = bucket.get('objects', [])
            old_objects = [o for o in objects
                          if (datetime.now() - o['last_modified']).days > 90]

            if len(old_objects) > len(objects) * 0.3:  # >30% old objects
                total_size_gb = sum(o['size'] for o in old_objects) / (1024**3)
                current_cost = total_size_gb * 0.026  # Standard tier
                archive_cost = total_size_gb * 0.002  # Glacier tier
                savings = (current_cost - archive_cost) * 12  # Annual

                recommendations.append({
                    'bucket': bucket['name'],
                    'recommendation': 'Implement lifecycle policy to archive old objects',
                    'objects_to_archive': len(old_objects),
                    'size_gb': round(total_size_gb, 2),
                    'annual_savings': round(savings, 2)
                })

        return recommendations

    def recommend_reserved_capacity(self):
        """Recommend reserved capacity for predictable workloads"""
        recommendations = []

        # Analyze instance usage patterns
        long_running_instances = []
        for instance in self.usage_data.get('instances', []):
            uptime_days = instance.get('uptime_days', 0)

            if uptime_days > 720:  # Running for 2+ years
                monthly_cost = instance['cost']
                reserved_monthly = monthly_cost * 0.6  # 40% discount
                annual_savings = (monthly_cost - reserved_monthly) * 12

                recommendations.append({
                    'instance': instance['name'],
                    'profile': instance['profile'],
                    'current_monthly_cost': monthly_cost,
                    'reserved_monthly_cost': reserved_monthly,
                    'annual_savings': round(annual_savings, 2),
                    'recommendation': '1-year or 3-year reserved capacity'
                })

        return recommendations

    def generate_cost_report(self):
        """Generate comprehensive cost optimization report"""
        idle = self.identify_idle_resources()
        storage = self.optimize_storage_costs()
        reserved = self.recommend_reserved_capacity()

        total_potential_savings = 0

        # Calculate total savings from idle resources
        for category in idle.values():
            for resource in category:
                total_potential_savings += resource.get('potential_savings', 0)

        # Add storage savings
        for rec in storage:
            total_potential_savings += rec['annual_savings'] / 12

        # Add reserved capacity savings
        for rec in reserved:
            total_potential_savings += rec['annual_savings'] / 12

        return {
            'generated_at': datetime.now().isoformat(),
            'total_monthly_savings': round(total_potential_savings, 2),
            'total_annual_savings': round(total_potential_savings * 12, 2),
            'idle_resources': idle,
            'storage_optimization': storage,
            'reserved_capacity': reserved
        }

# Terraform for cost management
cost_mgmt_tf = '''
# cost-management.tf

# Budget alerts
resource "ibm_billing_budget" "monthly_budget" {
  name        = "Monthly Cloud Budget"
  amount      = 10000
  currency    = "USD"
  time_period = "monthly"
  threshold_percentage = 80

  notifications {
    email_addresses = ["finance@example.com", "cloudops@example.com"]
  }
}

# Resource quotas
resource "ibm_resource_quota" "dev_quota" {
  name              = "Development Environment Quota"
  resource_group_id = ibm_resource_group.dev.id

  quota {
    limit = 5
    resource_type = "instance"
  }

  quota {
    limit = 100
    resource_type = "storage_gb"
  }
}

# Tagging for cost allocation
resource "ibm_resource_tag" "cost_center" {
  resource_id = ibm_is_instance.app_server.id
  tags        = [
    "cost-center:engineering",
    "environment:production",
    "project:customer-portal",
    "owner:team-alpha"
  ]
}
'''
```

---

## Performance Optimization

### Performance Tuning Strategies
```yaml
# performance-optimization.yaml
performance_layers:
  compute:
    strategies:
      - Profile selection (CPU-optimized, memory-optimized, balanced)
      - Auto-scaling for dynamic load
      - Load balancing across zones
      - Reserved capacity for baseline load

  network:
    strategies:
      - CDN for static content
      - Private endpoints for backend communication
      - Transit Gateway for multi-region
      - Direct Link for hybrid connectivity
      - HTTP/2 and HTTP/3 enablement

  storage:
    strategies:
      - Storage class selection (5000 IOPS, 10 IOPS/GB)
      - Read replicas for databases
      - Caching with Redis
      - Object storage for static assets

  application:
    strategies:
      - Connection pooling
      - Async processing
      - Caching strategies
      - Query optimization
      - Code profiling

monitoring_metrics:
  availability:
    - Uptime percentage
    - Error rate
    - Failed requests

  performance:
    - Response time (P50, P95, P99)
    - Throughput (requests/sec)
    - Latency distribution

  capacity:
    - CPU utilization
    - Memory usage
    - Network bandwidth
    - Storage IOPS
```

---

## Migration Strategies

### Cloud Migration Patterns
```yaml
# migration-strategies.yaml
migration_approaches:
  rehost:  # Lift and shift
    description: "Move as-is to cloud"
    effort: "Low"
    benefits: "Fast, low risk"
    use_case: "Legacy apps, quick migration"

  replatform:  # Lift, tinker, and shift
    description: "Minor optimizations"
    effort: "Medium"
    benefits: "Some cloud benefits, manageable risk"
    use_case: "Moderate modernization"

  refactor:  # Re-architect
    description: "Redesign for cloud-native"
    effort: "High"
    benefits: "Maximum cloud benefits, scalability"
    use_case: "Strategic applications"

  repurchase:  # Replace
    description: "Move to SaaS"
    effort: "Variable"
    benefits: "Reduced maintenance"
    use_case: "Standard business functions"

  retire:
    description: "Decommission"
    effort: "Low"
    benefits: "Cost savings"
    use_case: "Obsolete applications"

  retain:
    description: "Keep on-premises"
    effort: "None"
    use_case: "Compliance requirements, not ready"

migration_phases:
  assess:
    activities:
      - Application inventory
      - Dependency mapping
      - Cost analysis
      - Risk assessment
    tools:
      - IBM Cloud Migration Factory
      - Application discovery tools

  plan:
    activities:
      - Migration strategy selection
      - Wave planning
      - Timeline development
      - Resource allocation
    deliverables:
      - Migration roadmap
      - Risk mitigation plan
      - Success criteria

  migrate:
    activities:
      - Infrastructure provisioning
      - Data migration
      - Application deployment
      - Testing and validation
    best_practices:
      - Start with non-critical apps
      - Parallel running period
      - Automated testing
      - Rollback procedures

  optimize:
    activities:
      - Performance tuning
      - Cost optimization
      - Security hardening
      - Operational excellence
    continuous:
      - Monitor and adjust
      - FinOps practices
      - Well-architected review
```

---

## Enterprise Patterns

### Multi-Tenant Architecture
```yaml
# multi-tenancy.yaml
tenancy_models:
  pool:
    description: "All tenants share same infrastructure"
    isolation: "Logical (application-level)"
    cost: "Lowest"
    use_case: "SaaS with many small tenants"

  silo:
    description: "Dedicated infrastructure per tenant"
    isolation: "Physical (separate resources)"
    cost: "Highest"
    use_case: "Enterprise customers, compliance"

  bridge:
    description: "Hybrid approach"
    isolation: "Mix of shared and dedicated"
    cost: "Medium"
    use_case: "Tiered service offerings"

isolation_strategies:
  data:
    - Separate databases per tenant
    - Schema per tenant in shared database
    - Row-level security in shared tables

  compute:
    - Separate clusters per tenant
    - Namespace per tenant
    - Pod security policies

  network:
    - VPC per tenant
    - Subnet per tenant
    - Security groups per tenant
```

---

## Exam Tips

1. **Security**: Know zero trust principles, encryption options, IAM
2. **Compliance**: Understand regulatory frameworks (PCI DSS, HIPAA, GDPR)
3. **Cost**: Master optimization strategies, pricing models
4. **Performance**: CDN, caching, database optimization
5. **Migration**: Know the 6 R's, migration phases
6. **Governance**: SCC, Activity Tracker, resource tagging

### Common Scenarios

**Scenario 1**: Design compliant healthcare application
- HIPAA-ready services
- Encryption with Key Protect/HPCS
- Activity Tracker for audit logging
- BAA (Business Associate Agreement)
- Data residency controls

**Scenario 2**: Optimize costs for $50K/month bill
- Identify idle resources (savings: 20-30%)
- Right-size instances (savings: 15-25%)
- Reserved capacity for baseline (savings: 30-40%)
- Storage lifecycle policies (savings: 50-70% on archival)
- Auto-scaling to match demand

**Scenario 3**: Migrate 100 applications to cloud
- Assess: Inventory and dependency mapping
- Categorize: 6 R's strategy
- Wave planning: Low-risk apps first
- Execute: Automated migration where possible
- Optimize: Post-migration tuning

### Hands-On Practice

1. Implement zero trust architecture
2. Configure compliance scanning with SCC
3. Perform cost optimization analysis
4. Design multi-tenant SaaS architecture
5. Plan and execute cloud migration
6. Set up comprehensive governance
