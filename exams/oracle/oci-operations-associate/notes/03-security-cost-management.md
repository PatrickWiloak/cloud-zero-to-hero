# OCI Operations Associate - Security Operations and Cost Management

## Table of Contents
- [Security Operations](#security-operations)
- [IAM Operations](#iam-operations)
- [Compliance and Auditing](#compliance-and-auditing)
- [Cost Management](#cost-management)
- [Billing and Usage](#billing-and-usage)
- [Exam Tips](#exam-tips)

---

## Security Operations

### Cloud Guard Operations

**Enabling Cloud Guard**:
```bash
# Enable Cloud Guard
oci cloud-guard cloud-guard-configuration update \
  --reporting-region "us-phoenix-1" \
  --status ENABLED

# Create target
oci cloud-guard target create \
  --compartment-id $COMPARTMENT_ID \
  --display-name "Production-Monitoring" \
  --target-resource-id $COMPARTMENT_ID \
  --target-resource-type COMPARTMENT \
  --target-detector-recipes '[{
    "detectorRecipeId":"ocid1.cloudguarddetectorrecipe..."
  }]' \
  --target-responder-recipes '[{
    "responderRecipeId":"ocid1.cloudguardresponderrecipe..."
  }]'
```

**Managing Problems**:
```bash
# List problems
oci cloud-guard problem list \
  --compartment-id $COMPARTMENT_ID \
  --status OPEN \
  --sort-by timeCreated \
  --sort-order DESC

# Get problem details
oci cloud-guard problem get \
  --problem-id $PROBLEM_ID

# Dismiss problem
oci cloud-guard problem-status update \
  --problem-id $PROBLEM_ID \
  --status DISMISSED \
  --comment "False positive - approved configuration"

# Resolve problem
oci cloud-guard problem-status update \
  --problem-id $PROBLEM_ID \
  --status RESOLVED
```

**Common Problems and Remediation**:

**Public Bucket**:
```bash
# Problem: Bucket is public
# Auto-remediation:
oci os bucket update \
  --bucket-name "sensitive-data" \
  --public-access-type NoPublicAccess
```

**Overly Permissive Security List**:
```bash
# Problem: Security list allows 0.0.0.0/0:22
# Manual remediation:
oci network security-list update \
  --security-list-id $SL_ID \
  --ingress-security-rules '[{
    "protocol":"6",
    "source":"203.0.113.0/24",
    "tcpOptions":{"destinationPortRange":{"min":22,"max":22}}
  }]'
```

**Unencrypted Volume**:
```bash
# Problem: Block volume not using customer-managed key
# Cannot encrypt existing volume, must:
# 1. Backup volume
oci bv backup create --volume-id $VOLUME_ID

# 2. Create new encrypted volume from backup
oci bv volume create \
  --backup-id $BACKUP_ID \
  --kms-key-id $KEY_ID
```

### Security Zones Operations

**Creating Security Zone**:
```bash
# Create security zone
oci cloud-guard security-zone create \
  --compartment-id $COMPARTMENT_ID \
  --display-name "PCI-Compliance-Zone" \
  --security-zone-recipe-id ocid1.securityzonerecipe.oc1..maximum
```

**Moving Compartment to Security Zone**:
```bash
# Move compartment (resources must comply first)
oci cloud-guard security-zone update \
  --security-zone-id $ZONE_ID \
  --target-compartment-id $COMPARTMENT_ID
```

**Security Zone Violations**:
```
Common violations and fixes:

1. Public bucket
   Fix: Make bucket private

2. Unencrypted resource
   Fix: Enable encryption

3. Missing audit logs
   Fix: Enable audit logging

4. Overly permissive security rules
   Fix: Tighten security lists/NSGs
```

### Vault Operations

**Key Management**:
```bash
# Create vault
oci kms management vault create \
  --compartment-id $COMPARTMENT_ID \
  --display-name "production-vault" \
  --vault-type VIRTUAL_PRIVATE

# Create master encryption key
oci kms management key create \
  --compartment-id $COMPARTMENT_ID \
  --display-name "volume-encryption-key" \
  --key-shape '{"algorithm":"AES","length":32}' \
  --management-endpoint "https://..."

# Rotate key
oci kms management key create-key-version \
  --key-id $KEY_ID \
  --management-endpoint "https://..."

# Disable key
oci kms management key disable \
  --key-id $KEY_ID \
  --management-endpoint "https://..."
```

**Using Vault Keys**:
```bash
# Create encrypted volume
oci bv volume create \
  --availability-domain "Uocm:PHX-AD-1" \
  --compartment-id $COMPARTMENT_ID \
  --kms-key-id $KEY_ID \
  --size-in-gbs 500

# Create encrypted bucket
oci os bucket create \
  --name "encrypted-data" \
  --compartment-id $COMPARTMENT_ID \
  --kms-key-id $KEY_ID
```

---

## IAM Operations

### User Management

**Creating Users**:
```bash
# Create user
oci iam user create \
  --name "john.doe@example.com" \
  --description "Operations Engineer" \
  --email "john.doe@example.com"

# Enable capabilities
oci iam user update-user-capabilities \
  --user-id $USER_ID \
  --can-use-console-password true \
  --can-use-api-keys true \
  --can-use-auth-tokens true

# Generate initial password
oci iam user create-or-reset-ui-password \
  --user-id $USER_ID
```

**Adding to Groups**:
```bash
# Add user to group
oci iam group add-user \
  --group-id $GROUP_ID \
  --user-id $USER_ID

# Remove from group
oci iam group remove-user \
  --group-id $GROUP_ID \
  --user-id $USER_ID
```

**MFA Enforcement**:
```bash
# Check MFA status
oci iam user get \
  --user-id $USER_ID \
  --query 'data."is-mfa-activated"'

# Users enable MFA via console
# Operations: Verify MFA is enabled for all admin users
```

### Group and Policy Management

**Creating Groups**:
```bash
# Create operational groups
oci iam group create \
  --name "NetworkOperators" \
  --description "Network operations team"

oci iam group create \
  --name "DatabaseOperators" \
  --description "Database operations team"

oci iam group create \
  --name "ReadOnlyUsers" \
  --description "Read-only access for monitoring"
```

**Common Operational Policies**:

**Network Operators**:
```
Allow group NetworkOperators to manage virtual-network-family in compartment Production
Allow group NetworkOperators to manage load-balancers in compartment Production
Allow group NetworkOperators to read all-resources in compartment Production
Allow group NetworkOperators to use network-security-groups in compartment Production
```

**Database Operators**:
```
Allow group DatabaseOperators to manage database-family in compartment Production
Allow group DatabaseOperators to manage autonomous-database-family in compartment Production
Allow group DatabaseOperators to read virtual-network-family in compartment Production
Allow group DatabaseOperators to manage volume-family in compartment Production where any {
  request.operation = 'CreateVolumeBackup',
  request.operation = 'CreateBackup'
}
```

**Read-Only Users**:
```
Allow group ReadOnlyUsers to inspect all-resources in tenancy
Allow group ReadOnlyUsers to read metrics in tenancy
Allow group ReadOnlyUsers to read logs in tenancy
Allow group ReadOnlyUsers to read alarms in tenancy
```

**Incident Response Team**:
```
Allow group IncidentResponse to manage instances in compartment Production where request.operation = 'InstanceAction'
Allow group IncidentResponse to read all-resources in tenancy
Allow group IncidentResponse to manage console-history in compartment Production
Allow group IncidentResponse to read audit-events in tenancy
```

### Dynamic Groups

**Creating Dynamic Groups**:
```bash
# Instance principals for specific compartment
oci iam dynamic-group create \
  --name "prod-instances" \
  --description "Production compute instances" \
  --matching-rule "instance.compartment.id = '$PROD_COMPARTMENT_ID'"

# Function principals
oci iam dynamic-group create \
  --name "automation-functions" \
  --description "Automation functions" \
  --matching-rule "resource.type = 'fnfunc'"
```

**Dynamic Group Policies**:
```
# Allow instances to access Object Storage
Allow dynamic-group prod-instances to read buckets in compartment Production
Allow dynamic-group prod-instances to read objects in compartment Production

# Allow functions to manage resources
Allow dynamic-group automation-functions to manage instances in compartment Production
Allow dynamic-group automation-functions to use virtual-network-family in compartment Production
```

---

## Compliance and Auditing

### Audit Logs

**Viewing Audit Events**:
```bash
# List recent audit events
oci audit event list \
  --compartment-id $COMPARTMENT_ID \
  --start-time "2024-10-10T00:00:00Z" \
  --end-time "2024-10-10T23:59:59Z"

# Find specific operations
oci audit event list \
  --compartment-id $COMPARTMENT_ID \
  --start-time "2024-10-10T00:00:00Z" \
  --end-time "2024-10-10T23:59:59Z" \
  | jq '.data[] | select(.data."event-name" == "LaunchInstance")'

# Find actions by specific user
oci audit event list \
  --compartment-id $COMPARTMENT_ID \
  --start-time "2024-10-10T00:00:00Z" \
  --end-time "2024-10-10T23:59:59Z" \
  | jq '.data[] | select(.data.identity."principal-name" == "john.doe@example.com")'
```

**Audit Log Analysis Queries**:
```
# IAM changes
search "compartment-ocid/audit-logs" |
where data.eventType =~ 'com.oraclecloud.identitycontrolplane.*' |
sort by datetime desc

# Resource deletions
search "compartment-ocid/audit-logs" |
where data.request.operation =~ '.*Delete.*' |
where data.response.status = '200' |
stats count() by data.request.operation, data.identity.principalName

# Failed authentication attempts
search "compartment-ocid/audit-logs" |
where data.message =~ 'authentication failed' |
stats count() as failures by data.identity.principalName, data.request.sourceAddress |
where failures > 5 |
sort by failures desc
```

**Audit Log Archival**:
```bash
# Archive to Object Storage (via Service Connector)
oci sch service-connector create \
  --compartment-id $COMPARTMENT_ID \
  --display-name "audit-log-archival" \
  --source '{
    "kind":"logging",
    "logSources":[{
      "compartmentId":"'$TENANCY_ID'",
      "logId":"'$AUDIT_LOG_ID'"
    }]
  }' \
  --target '{
    "kind":"objectStorage",
    "bucketName":"audit-archive",
    "namespace":"'$NAMESPACE'",
    "objectNamePrefix":"audit-logs/"
  }'
```

### Compliance Reporting

**Generating Compliance Reports**:
```python
#!/usr/bin/env python3
# Generate compliance report

import oci
from datetime import datetime, timedelta

config = oci.config.from_file()

def generate_compliance_report():
    report = {
        "date": datetime.now().isoformat(),
        "findings": []
    }

    # Check 1: All users have MFA
    identity = oci.identity.IdentityClient(config)
    users = identity.list_users(config["tenancy"]).data

    for user in users:
        if not user.is_mfa_activated:
            report["findings"].append({
                "severity": "HIGH",
                "finding": f"User {user.name} does not have MFA enabled",
                "remediation": "Enable MFA in user profile"
            })

    # Check 2: No public buckets
    object_storage = oci.object_storage.ObjectStorageClient(config)
    namespace = object_storage.get_namespace().data

    buckets = object_storage.list_buckets(
        namespace,
        config["compartment_id"]
    ).data

    for bucket in buckets:
        bucket_details = object_storage.get_bucket(namespace, bucket.name).data
        if bucket_details.public_access_type != "NoPublicAccess":
            report["findings"].append({
                "severity": "CRITICAL",
                "finding": f"Bucket {bucket.name} allows public access",
                "remediation": "Set public access to NoPublicAccess"
            })

    # Check 3: All volumes encrypted
    block_storage = oci.core.BlockstorageClient(config)
    volumes = block_storage.list_volumes(config["compartment_id"]).data

    for volume in volumes:
        if not volume.kms_key_id:
            report["findings"].append({
                "severity": "MEDIUM",
                "finding": f"Volume {volume.display_name} not encrypted with customer key",
                "remediation": "Create encrypted volume from backup"
            })

    return report

# Generate report
report = generate_compliance_report()
print(json.dumps(report, indent=2))
```

---

## Cost Management

### Cost Analysis

**Viewing Costs**:
```bash
# Get cost data (requires cost tracking setup)
oci usage-api usage-summary request-summarized-usages \
  --tenant-id $TENANCY_ID \
  --time-usage-started "2024-10-01T00:00:00Z" \
  --time-usage-ended "2024-10-31T23:59:59Z" \
  --granularity DAILY \
  --group-by '["service"]'
```

**Cost by Compartment**:
```bash
oci usage-api usage-summary request-summarized-usages \
  --tenant-id $TENANCY_ID \
  --time-usage-started "2024-10-01T00:00:00Z" \
  --time-usage-ended "2024-10-31T23:59:59Z" \
  --granularity MONTHLY \
  --group-by '["compartmentPath"]'
```

**Cost by Tag**:
```bash
oci usage-api usage-summary request-summarized-usages \
  --tenant-id $TENANCY_ID \
  --time-usage-started "2024-10-01T00:00:00Z" \
  --time-usage-ended "2024-10-31T23:59:59Z" \
  --granularity MONTHLY \
  --group-by '["tags"]'
```

### Budget Management

**Creating Budgets**:
```bash
# Monthly budget with alerts
oci budgets budget create \
  --amount 5000 \
  --reset-period MONTHLY \
  --target-compartment-id $COMPARTMENT_ID \
  --target-type COMPARTMENT \
  --display-name "Production-Monthly-Budget" \
  --description "Monthly budget for production"

# Add alert rules
oci budgets alert-rule create \
  --budget-id $BUDGET_ID \
  --type ACTUAL \
  --threshold 80 \
  --threshold-type PERCENTAGE \
  --recipients '["finance@example.com"]' \
  --display-name "80%-Alert" \
  --message "Production spending at 80% of budget"

oci budgets alert-rule create \
  --budget-id $BUDGET_ID \
  --type FORECAST \
  --threshold 100 \
  --threshold-type PERCENTAGE \
  --recipients '["finance@example.com","ops@example.com"]' \
  --display-name "Forecast-Exceed" \
  --message "Production forecast to exceed budget"
```

### Cost Optimization

**Identifying Unused Resources**:
```python
import oci
from datetime import datetime, timedelta

config = oci.config.from_file()

def find_unused_resources():
    compute = oci.core.ComputeClient(config)
    block_storage = oci.core.BlockstorageClient(config)

    unused = {
        "stopped_instances": [],
        "unattached_volumes": [],
        "old_backups": []
    }

    # Find stopped instances (>30 days)
    instances = compute.list_instances(
        config["compartment_id"],
        lifecycle_state="STOPPED"
    ).data

    cutoff = datetime.now() - timedelta(days=30)
    for instance in instances:
        if instance.time_created < cutoff:
            unused["stopped_instances"].append({
                "name": instance.display_name,
                "id": instance.id,
                "age_days": (datetime.now() - instance.time_created).days
            })

    # Find unattached volumes
    volumes = block_storage.list_volumes(
        config["compartment_id"],
        lifecycle_state="AVAILABLE"
    ).data

    for volume in volumes:
        attachments = compute.list_volume_attachments(
            config["compartment_id"],
            volume_id=volume.id
        ).data

        if not attachments:
            unused["unattached_volumes"].append({
                "name": volume.display_name,
                "id": volume.id,
                "size_gb": volume.size_in_gbs,
                "cost_per_month": volume.size_in_gbs * 0.085
            })

    # Find old backups (>365 days)
    backups = block_storage.list_volume_backups(
        config["compartment_id"]
    ).data

    cutoff = datetime.now() - timedelta(days=365)
    for backup in backups:
        if backup.time_created < cutoff:
            unused["old_backups"].append({
                "name": backup.display_name,
                "id": backup.id,
                "age_days": (datetime.now() - backup.time_created).days
            })

    return unused

# Find and report
unused = find_unused_resources()
print(f"Stopped instances (>30 days): {len(unused['stopped_instances'])}")
print(f"Unattached volumes: {len(unused['unattached_volumes'])}")
print(f"Old backups (>1 year): {len(unused['old_backups'])}")
```

**Right-Sizing Recommendations**:
```python
def analyze_utilization():
    # Get CPU utilization for last 30 days
    monitoring = oci.monitoring.MonitoringClient(config)

    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)

    metrics = monitoring.summarize_metrics_data(
        compartment_id=config["compartment_id"],
        summarize_metrics_data_details=oci.monitoring.models.SummarizeMetricsDataDetails(
            namespace="oci_computeagent",
            query="CpuUtilization[1d].mean()",
            start_time=start_time,
            end_time=end_time
        )
    ).data

    recommendations = []
    for metric in metrics:
        avg_cpu = sum([dp.value for dp in metric.aggregated_datapoints]) / len(metric.aggregated_datapoints)

        if avg_cpu < 20:
            recommendations.append({
                "resource": metric.dimensions["resourceId"],
                "current_usage": f"{avg_cpu:.1f}%",
                "recommendation": "Consider downsizing or stopping"
            })

    return recommendations
```

---

## Billing and Usage

### Usage Reports

**Downloading Usage Reports**:
```bash
# List available reports
oci usage-api usage-summary request-summarized-usages \
  --tenant-id $TENANCY_ID \
  --time-usage-started "2024-10-01T00:00:00Z" \
  --time-usage-ended "2024-10-31T23:59:59Z" \
  --granularity MONTHLY

# Export to CSV
oci usage-api usage-summary request-summarized-usages \
  --tenant-id $TENANCY_ID \
  --time-usage-started "2024-10-01T00:00:00Z" \
  --time-usage-ended "2024-10-31T23:59:59Z" \
  --granularity DAILY \
  --output-file usage-report.json
```

### Cost Allocation

**Tagging for Cost Tracking**:
```bash
# Define cost tracking tags
oci iam tag create \
  --tag-namespace-id $NAMESPACE_ID \
  --name "CostCenter" \
  --description "Cost center for billing"

oci iam tag create \
  --tag-namespace-id $NAMESPACE_ID \
  --name "Project" \
  --description "Project name"

# Apply to resources
oci compute instance update \
  --instance-id $INSTANCE_ID \
  --defined-tags '{
    "Finance": {
      "CostCenter": "Engineering",
      "Project": "WebApp"
    }
  }'

# View costs by tag
oci usage-api usage-summary request-summarized-usages \
  --tenant-id $TENANCY_ID \
  --time-usage-started "2024-10-01T00:00:00Z" \
  --time-usage-ended "2024-10-31T23:59:59Z" \
  --granularity MONTHLY \
  --group-by '["tags"]'
```

---

## Exam Tips

### Critical Concepts

**Security Operations**:
- Cloud Guard: Detect and respond to security issues
- Security Zones: Prevent non-compliant configurations
- Vault: Manage encryption keys
- Audit logs: Track all API activity (90 days)

**IAM**:
- Users, groups, policies
- MFA enforcement for admins
- Dynamic groups for resource principals
- Least privilege principle

**Compliance**:
- Audit logs: Who did what, when
- Compliance reports: Regular checks
- Security zones for high-security compartments
- Tag resources for tracking

**Cost Management**:
- Budgets: Set spending limits
- Tags: Track costs by project/department
- Unused resources: Identify and cleanup
- Right-sizing: Match resources to workload

### Common Scenarios

**Q: Enforce encryption for all resources?**
A: Security Zones with maximum security recipe

**Q: Track who deleted an instance?**
A: Search audit logs for DeleteInstance operation

**Q: Alert when spending reaches $4000?**
A: Budget with 80% threshold alert

**Q: Auto-remediate public buckets?**
A: Cloud Guard responder with auto-action mode

**Q: Find unused volumes?**
A: List volumes with AVAILABLE state and no attachments

---

## Summary

**Security**: Cloud Guard, Security Zones, Vault, audit logs

**IAM**: Users, groups, policies, dynamic groups, MFA

**Compliance**: Audit logs, compliance checks, reporting

**Cost**: Budgets, tags, usage reports, optimization

**Operations**: Automation, monitoring, proactive management

---

**Congratulations on completing OCI Operations Associate study notes!**

## Key terms

- **IAM policy** - a statement that grants a group permission to work with specific resources in a compartment or tenancy.
- **Dynamic group** - a group of compute instances or other resources that match rules, so they can be granted permissions as principals.
- **Audit service** - the OCI service that records API calls made to resources in a tenancy.
- **Budget** - an OCI cost control that sets a spending target for a compartment and sends alerts when it is reached.
- **Cost Analysis** - the OCI tool for viewing and filtering spending by service, compartment or tag.
