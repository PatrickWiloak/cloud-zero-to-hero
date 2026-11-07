# OCI Operations Associate - Infrastructure Operations

## Table of Contents
- [Infrastructure Provisioning](#infrastructure-provisioning)
- [Resource Management](#resource-management)
- [Automation](#automation)
- [Backup and Recovery](#backup-and-recovery)
- [Exam Tips](#exam-tips)

---

## Infrastructure Provisioning

### Compute Provisioning

**Instance Lifecycle Management**:
```bash
# Launch instance
oci compute instance launch \
  --availability-domain "Uocm:PHX-AD-1" \
  --compartment-id ocid1.compartment... \
  --shape "VM.Standard.E4.Flex" \
  --shape-config '{"ocpus":2,"memoryInGBs":16}' \
  --subnet-id ocid1.subnet... \
  --image-id ocid1.image... \
  --display-name "app-server-01"

# Start/Stop/Reboot
oci compute instance action \
  --instance-id ocid1.instance... \
  --action STOP

oci compute instance action \
  --instance-id ocid1.instance... \
  --action START

# Terminate
oci compute instance terminate \
  --instance-id ocid1.instance... \
  --preserve-boot-volume true
```

**Bulk Operations**:
```python
# Python script for bulk instance management
import oci

config = oci.config.from_file()
compute = oci.core.ComputeClient(config)

def stop_all_dev_instances(compartment_id):
    instances = compute.list_instances(
        compartment_id=compartment_id,
        lifecycle_state="RUNNING"
    ).data

    for instance in instances:
        if "dev-" in instance.display_name.lower():
            print(f"Stopping {instance.display_name}")
            compute.instance_action(
                instance.id,
                "STOP"
            )

def start_instances_by_tag(compartment_id, tag_key, tag_value):
    instances = compute.list_instances(
        compartment_id=compartment_id,
        lifecycle_state="STOPPED"
    ).data

    for instance in instances:
        if instance.freeform_tags.get(tag_key) == tag_value:
            print(f"Starting {instance.display_name}")
            compute.instance_action(
                instance.id,
                "START"
            )
```

### Network Provisioning

**VCN Creation Template**:
```bash
# Create VCN
VCN_ID=$(oci network vcn create \
  --compartment-id $COMPARTMENT_ID \
  --cidr-block "10.0.0.0/16" \
  --display-name "prod-vcn" \
  --dns-label "prodvcn" \
  --query 'data.id' --raw-output)

# Create Internet Gateway
IGW_ID=$(oci network internet-gateway create \
  --compartment-id $COMPARTMENT_ID \
  --vcn-id $VCN_ID \
  --is-enabled true \
  --display-name "internet-gateway" \
  --query 'data.id' --raw-output)

# Create NAT Gateway
NAT_ID=$(oci network nat-gateway create \
  --compartment-id $COMPARTMENT_ID \
  --vcn-id $VCN_ID \
  --display-name "nat-gateway" \
  --query 'data.id' --raw-output)

# Create Service Gateway
SGW_ID=$(oci network service-gateway create \
  --compartment-id $COMPARTMENT_ID \
  --vcn-id $VCN_ID \
  --services '[{"serviceId":"ocid1.service..."}]' \
  --display-name "service-gateway" \
  --query 'data.id' --raw-output)

# Create public subnet
oci network subnet create \
  --compartment-id $COMPARTMENT_ID \
  --vcn-id $VCN_ID \
  --cidr-block "10.0.1.0/24" \
  --display-name "public-subnet" \
  --route-table-id $PUBLIC_RT_ID \
  --security-list-ids "[\"$PUBLIC_SL_ID\"]"
```

### Storage Provisioning

**Block Volume Operations**:
```bash
# Create volume
oci bv volume create \
  --availability-domain "Uocm:PHX-AD-1" \
  --compartment-id $COMPARTMENT_ID \
  --display-name "data-volume-01" \
  --size-in-gbs 500 \
  --vpus-per-gb 10

# Attach to instance
oci compute volume-attachment attach \
  --instance-id $INSTANCE_ID \
  --volume-id $VOLUME_ID \
  --type iscsi

# Detach volume
oci compute volume-attachment detach \
  --volume-attachment-id $ATTACHMENT_ID

# Resize volume
oci bv volume update \
  --volume-id $VOLUME_ID \
  --size-in-gbs 1000

# Clone volume
oci bv volume create \
  --availability-domain "Uocm:PHX-AD-1" \
  --compartment-id $COMPARTMENT_ID \
  --source-volume-id $SOURCE_VOLUME_ID \
  --display-name "data-volume-clone"
```

**Object Storage Operations**:
```bash
# Create bucket
oci os bucket create \
  --compartment-id $COMPARTMENT_ID \
  --name "application-data" \
  --storage-tier Standard \
  --public-access-type NoPublicAccess

# Upload files
oci os object put \
  --bucket-name "application-data" \
  --file /path/to/file.txt \
  --name "file.txt"

# Bulk upload
oci os object bulk-upload \
  --bucket-name "application-data" \
  --src-dir /path/to/directory

# Download
oci os object get \
  --bucket-name "application-data" \
  --name "file.txt" \
  --file /path/to/download/file.txt

# Bulk download
oci os object bulk-download \
  --bucket-name "application-data" \
  --download-dir /path/to/download
```

---

## Resource Management

### Tagging Strategy

**Tag Namespaces**:
```bash
# Create tag namespace
oci iam tag-namespace create \
  --compartment-id $TENANCY_ID \
  --name "Operations" \
  --description "Operational tags"

# Create tag keys
oci iam tag create \
  --tag-namespace-id $NAMESPACE_ID \
  --name "Environment" \
  --description "Deployment environment"

oci iam tag create \
  --tag-namespace-id $NAMESPACE_ID \
  --name "Owner" \
  --description "Resource owner"

oci iam tag create \
  --tag-namespace-id $NAMESPACE_ID \
  --name "CostCenter" \
  --description "Cost center for billing"
```

**Applying Tags**:
```bash
# Tag instance
oci compute instance update \
  --instance-id $INSTANCE_ID \
  --defined-tags '{
    "Operations": {
      "Environment":"Production",
      "Owner":"TeamA",
      "CostCenter":"Engineering"
    }
  }'

# Bulk tagging script
for instance in $(oci compute instance list \
  --compartment-id $COMPARTMENT_ID \
  --query 'data[].id' --raw-output)
do
  oci compute instance update \
    --instance-id $instance \
    --defined-tags '{"Operations":{"Environment":"Development"}}'
done
```

**Tag Defaults**:
```bash
# Set default tags for compartment
oci iam tag-default create \
  --compartment-id $COMPARTMENT_ID \
  --tag-definition-id $TAG_DEF_ID \
  --value "Development"

# All new resources in compartment get this tag automatically
```

### Resource Quotas

**Viewing Quotas**:
```bash
# List service limits
oci limits service list

# Get specific limit
oci limits value get \
  --service-name compute \
  --scope-type AD \
  --availability-domain "Uocm:PHX-AD-1" \
  --name "standard-a1-core-count"

# List resource availability
oci limits resource-availability get \
  --service-name compute \
  --limit-name "standard-e4-core-count" \
  --compartment-id $COMPARTMENT_ID \
  --availability-domain "Uocm:PHX-AD-1"
```

**Setting Quotas**:
```bash
# Create quota policy
oci limits quota create \
  --compartment-id $COMPARTMENT_ID \
  --name "Dev-Quota" \
  --description "Development environment limits" \
  --statements '[
    "Set compute quotas standard-e4-core-count to 20 in compartment Development",
    "Set storage quotas volume-count to 50 in compartment Development",
    "Set storage quotas total-storage-gb to 5000 in compartment Development"
  ]'
```

### Compartment Management

**Creating Compartment Hierarchy**:
```bash
# Create root-level compartments
PROD_ID=$(oci iam compartment create \
  --compartment-id $TENANCY_ID \
  --name "Production" \
  --description "Production resources" \
  --query 'data.id' --raw-output)

DEV_ID=$(oci iam compartment create \
  --compartment-id $TENANCY_ID \
  --name "Development" \
  --description "Development resources" \
  --query 'data.id' --raw-output)

# Create sub-compartments
oci iam compartment create \
  --compartment-id $PROD_ID \
  --name "Prod-Network" \
  --description "Production networking"

oci iam compartment create \
  --compartment-id $PROD_ID \
  --name "Prod-Compute" \
  --description "Production compute"
```

**Moving Resources**:
```bash
# Move instance to different compartment
oci compute instance update \
  --instance-id $INSTANCE_ID \
  --compartment-id $NEW_COMPARTMENT_ID

# Move volume
oci bv volume update \
  --volume-id $VOLUME_ID \
  --compartment-id $NEW_COMPARTMENT_ID

# Move VCN
oci network vcn update \
  --vcn-id $VCN_ID \
  --compartment-id $NEW_COMPARTMENT_ID
```

---

## Automation

### Resource Manager

**Stack Management**:
```bash
# Create stack from local TF files
zip -r infrastructure.zip *.tf

oci resource-manager stack create \
  --compartment-id $COMPARTMENT_ID \
  --config-source infrastructure.zip \
  --display-name "production-infrastructure" \
  --variables file://variables.json

# Apply stack
APPLY_JOB=$(oci resource-manager job create-apply-job \
  --stack-id $STACK_ID \
  --execution-plan-strategy AUTO_APPROVED \
  --query 'data.id' --raw-output)

# Monitor job
oci resource-manager job get \
  --job-id $APPLY_JOB \
  --query 'data.lifecycle-state'

# View logs
oci resource-manager job get-job-logs \
  --job-id $APPLY_JOB
```

**Drift Detection**:
```bash
# Detect drift
DRIFT_JOB=$(oci resource-manager stack detect-drift \
  --stack-id $STACK_ID \
  --query 'data.id' --raw-output)

# View drift
oci resource-manager job get-job-detailed-log-content \
  --job-id $DRIFT_JOB | jq '.data[] | select(.type=="DRIFT")'
```

### Scheduling Operations

**Instance Scheduling**:
```python
#!/usr/bin/env python3
# Schedule: Run daily via cron or OCI Functions

import oci
from datetime import datetime

config = oci.config.from_file()
compute = oci.core.ComputeClient(config)

def schedule_instances():
    current_hour = datetime.now().hour
    current_day = datetime.now().weekday()  # 0=Monday, 6=Sunday

    # Stop instances after business hours
    if current_hour >= 18 or current_hour < 8 or current_day >= 5:
        action = "STOP"
        tag_value = "scheduled"
    else:
        action = "START"
        tag_value = "scheduled"

    instances = compute.list_instances(
        compartment_id=config["compartment_id"],
        lifecycle_state="RUNNING" if action == "STOP" else "STOPPED"
    ).data

    for instance in instances:
        if instance.defined_tags.get("Operations", {}).get("Schedule") == tag_value:
            print(f"{action}: {instance.display_name}")
            compute.instance_action(instance.id, action)

if __name__ == "__main__":
    schedule_instances()
```

**Automated Backup Script**:
```bash
#!/bin/bash
# Run daily via cron

COMPARTMENT_ID="ocid1.compartment..."
BACKUP_PREFIX="auto-backup-$(date +%Y%m%d)"

# Backup all volumes
for VOLUME_ID in $(oci bv volume list \
  --compartment-id $COMPARTMENT_ID \
  --query 'data[].id' --raw-output)
do
  VOLUME_NAME=$(oci bv volume get \
    --volume-id $VOLUME_ID \
    --query 'data."display-name"' --raw-output)

  echo "Backing up $VOLUME_NAME"
  oci bv backup create \
    --volume-id $VOLUME_ID \
    --display-name "${BACKUP_PREFIX}-${VOLUME_NAME}" \
    --type FULL
done

# Delete backups older than 30 days
CUTOFF_DATE=$(date -d "30 days ago" +%Y-%m-%d)
for BACKUP_ID in $(oci bv backup list \
  --compartment-id $COMPARTMENT_ID \
  --query "data[?\"time-created\"<'${CUTOFF_DATE}'].id" --raw-output)
do
  echo "Deleting old backup $BACKUP_ID"
  oci bv backup delete --backup-id $BACKUP_ID --force
done
```

### Monitoring Automation

**Auto-Remediation Function**:
```python
# OCI Function triggered by alarm
import oci
import json

def handler(ctx, data: io.BytesIO = None):
    """Auto-remediate high CPU by scaling"""
    alarm = json.loads(data.getvalue())

    if alarm["alarmMetaData"][0]["namespace"] == "oci_computeagent":
        instance_id = alarm["alarmMetaData"][0]["dimensions"]["resourceId"]

        # Authenticate
        signer = oci.auth.signers.get_resource_principals_signer()
        compute = oci.core.ComputeClient(config={}, signer=signer)

        # Get current shape
        instance = compute.get_instance(instance_id).data

        # Scale up (add 2 OCPUs)
        if "Flex" in instance.shape:
            current_ocpus = instance.shape_config.ocpus
            new_ocpus = current_ocpus + 2

            compute.update_instance(
                instance_id,
                oci.core.models.UpdateInstanceDetails(
                    shape_config=oci.core.models.UpdateInstanceShapeConfigDetails(
                        ocpus=new_ocpus
                    )
                )
            )

            return {"status": "scaled", "from": current_ocpus, "to": new_ocpus}

    return {"status": "no action"}
```

---

## Backup and Recovery

### Backup Policies

**Volume Backup Policies**:
```bash
# Assign Gold policy (daily, weekly, monthly, yearly)
oci bv volume update \
  --volume-id $VOLUME_ID \
  --backup-policy-id ocid1.volumebackuppolicy.oc1..gold

# Assign Silver policy (weekly)
oci bv volume update \
  --volume-id $VOLUME_ID \
  --backup-policy-id ocid1.volumebackuppolicy.oc1..silver

# Assign Bronze policy (monthly)
oci bv volume update \
  --volume-id $VOLUME_ID \
  --backup-policy-id ocid1.volumebackuppolicy.oc1..bronze

# Custom backup policy
oci bv volume-backup-policy create \
  --compartment-id $COMPARTMENT_ID \
  --display-name "Custom-Daily" \
  --schedules '[{
    "backupType":"FULL",
    "period":"ONE_DAY",
    "retentionSeconds":2592000,
    "timeZone":"UTC"
  }]'
```

**Boot Volume Backups**:
```bash
# Manual backup
oci bv boot-volume-backup create \
  --boot-volume-id $BOOT_VOLUME_ID \
  --display-name "boot-backup-$(date +%Y%m%d)"

# Automatic backups (via policy)
oci bv boot-volume update \
  --boot-volume-id $BOOT_VOLUME_ID \
  --backup-policy-id ocid1.volumebackuppolicy.oc1..gold
```

### Database Backups

**Autonomous Database**:
```bash
# Manual backup
oci db autonomous-database create-backup \
  --autonomous-database-id $ADB_ID \
  --display-name "pre-upgrade-backup"

# List backups
oci db autonomous-database-backup list \
  --autonomous-database-id $ADB_ID

# Restore
oci db autonomous-database restore \
  --autonomous-database-id $ADB_ID \
  --timestamp "2024-10-10T14:30:00Z"
```

**DB Systems**:
```bash
# Configure automatic backups
oci db database update \
  --database-id $DATABASE_ID \
  --db-backup-config '{
    "autoBackupEnabled":true,
    "recoveryWindowInDays":30,
    "autoBackupWindow":"SLOT_TWO"
  }'

# Manual backup
oci db backup create \
  --database-id $DATABASE_ID \
  --display-name "manual-backup"
```

### Disaster Recovery

**Cross-Region Volume Copy**:
```bash
# Backup volume
BACKUP_ID=$(oci bv backup create \
  --volume-id $VOLUME_ID \
  --display-name "dr-backup" \
  --query 'data.id' --raw-output)

# Copy to DR region
oci bv backup copy \
  --backup-id $BACKUP_ID \
  --destination-region "us-ashburn-1" \
  --display-name "dr-backup-copy"
```

**Object Storage Replication**:
```bash
# Enable replication
oci os replication create-replication-policy \
  --bucket-name "production-data" \
  --destination-bucket-name "dr-data" \
  --destination-region "us-ashburn-1" \
  --name "prod-to-dr-replication"
```

---

## Exam Tips

### Critical Concepts

**Provisioning**:
- Instance lifecycle: Launch, start, stop, terminate
- Bulk operations for efficiency
- Network setup: VCN, subnets, gateways
- Storage: Block volumes, Object Storage

**Management**:
- Tagging: Organize and track resources
- Quotas: Limit resource usage
- Compartments: Organize and isolate
- Moving resources between compartments

**Automation**:
- Resource Manager: Infrastructure as Code
- Scheduling: Start/stop instances automatically
- Scripts: Automate repetitive tasks
- Event-driven: Functions triggered by events

**Backup**:
- Volume backup policies: Gold, Silver, Bronze
- Boot volume backups
- Database backups (manual and automatic)
- Cross-region copies for DR

### Common Scenarios

**Q: Automate nightly backups?**
A: Backup policy or scheduled script

**Q: Stop dev instances after hours?**
A: Scheduled script with tagging

**Q: Manage infrastructure as code?**
A: Resource Manager (Terraform)

**Q: Track costs by department?**
A: Tagging with CostCenter tag

**Q: Limit resources in Dev compartment?**
A: Quota policy

---

## Summary

**Provisioning**: Compute, network, storage - automate where possible

**Management**: Tags, quotas, compartments, resource tracking

**Automation**: Resource Manager, scheduling, scripts, event-driven

**Backup**: Policies, manual backups, DR copies, retention

---

**Next**: Monitoring and Troubleshooting

## Key terms

- **Compartment** - a logical container in OCI used to organise resources and control access to them.
- **Tag namespace** - a container for tag keys that lets you apply defined tags to resources for cost tracking and governance.
- **Resource Manager** - the OCI service that provisions infrastructure from Terraform configurations packaged as stacks.
- **Stack** - the Resource Manager unit that holds a Terraform configuration and its variables.
- **Boot volume backup** - a point-in-time copy of an instance boot volume that can be used to restore or clone it.
