# OCI Architect Professional - Advanced Architecture Patterns

## Table of Contents
- [Multi-Region Architecture](#multi-region-architecture)
- [Hybrid Cloud Patterns](#hybrid-cloud-patterns)
- [High Availability and DR](#high-availability-and-dr)
- [Migration Strategies](#migration-strategies)
- [Performance at Scale](#performance-at-scale)
- [Exam Tips](#exam-tips)

---

## Multi-Region Architecture

### Global Application Design

**Active-Active Multi-Region**:
```
Global Users
    ↓
Traffic Manager (DNS-based routing)
    ├─→ Region 1 (us-phoenix-1): 50% traffic
    │   ├── Load Balancer
    │   ├── Application Tier (scaled)
    │   ├── Database (Primary)
    │   └── Object Storage (replicated)
    │
    └─→ Region 2 (us-ashburn-1): 50% traffic
        ├── Load Balancer
        ├── Application Tier (scaled)
        ├── Database (Primary)
        └── Object Storage (replicated)
```

**Traffic Management Policies**:
- **Geolocation**: Route based on user location
- **Performance**: Route to fastest responding region
- **Failover**: Automatic region failover on health check failure
- **Load Balance**: Distribute across regions

**Database Replication Strategies**:

**GoldenGate for Multi-Master**:
```
Region 1 Database ←→ GoldenGate ←→ Region 2 Database
    ↓ Bi-directional replication ↓
Conflict resolution via timestamp/priority
```

**Autonomous Data Guard Cross-Region**:
```
Primary ADB (Region 1)
    ↓ Async replication
Standby ADB (Region 2)
```

### Data Sovereignty and Compliance

**Region-Specific Data Isolation**:
```
EU Users
    ↓
EU Region (Frankfurt): GDPR-compliant
├── EU customer data (stays in EU)
├── Encryption with EU-based keys
└── Audit logs in EU region

US Users
    ↓
US Region (Phoenix): US compliance
├── US customer data (stays in US)
├── Encryption with US-based keys
└── Audit logs in US region
```

**Cross-Region Data Transfer Controls**:
```terraform
# Restrict data replication based on tags
resource "oci_objectstorage_replication_policy" "gdpr_compliant" {
  bucket    = "customer-data-eu"
  name      = "no-cross-region"

  # Only replicate within EU regions
  destination_region_name = "eu-amsterdam-1"  # Not to US regions
  destination_bucket_name = "customer-data-eu-dr"
}
```

---

## Hybrid Cloud Patterns

### Advanced FastConnect Design

**Multi-Circuit Redundancy**:
```
Corporate Data Center
├── Router 1
│   ├── FastConnect 1 → DRG → VCN-Production
│   └── FastConnect 2 → DRG → VCN-Production
└── Router 2
    ├── FastConnect 3 → DRG → VCN-Production
    └── VPN (Backup) → DRG → VCN-Production
```

**DRG v2 Advanced Routing**:
```terraform
# Custom route distribution
resource "oci_core_drg_route_distribution" "custom" {
  drg_id           = oci_core_drg.hub.id
  distribution_type = "IMPORT"

  # Import specific routes
  statements {
    priority = 1
    action   = "ACCEPT"
    match_criteria {
      match_type = "DRG_ATTACHMENT_ID"
      drg_attachment_id = oci_core_drg_attachment.vcn1.id
    }
  }
}

# Custom route table for VCNs
resource "oci_core_drg_route_table" "vcn_routes" {
  drg_id           = oci_core_drg.hub.id
  import_drg_route_distribution_id = oci_core_drg_route_distribution.custom.id
}
```

### Cloud@Customer Integration

**Exadata Cloud@Customer**:
```
Customer Data Center
├── Exadata Cloud@Customer
│   ├── Managed by Oracle (fully patched)
│   ├── API compatible with OCI Exadata
│   └── Same tooling as OCI
└── Connection to OCI Public Cloud
    ├── Private FastConnect
    └── Hybrid workload distribution
```

**Use Cases**:
- Data residency requirements (must stay on-premises)
- Low-latency database access
- Gradual cloud migration
- Regulatory compliance

### Multi-Cloud Integration

**OCI + Azure Integration**:
```
OCI (Phoenix)                Azure (East US)
├── VCN: 10.0.0.0/16    ←→  VNet: 10.1.0.0/16
├── FastConnect          │   ExpressRoute
└── Applications         │   Applications
         ↓               ↓
    Shared Data Layer
    (replicated databases)
```

**Oracle Interconnect for Azure**:
- Dedicated, low-latency connection
- <2ms latency between clouds
- Use OCI database with Azure applications
- No internet transit

---

## High Availability and DR

### Maximum Availability Architecture (MAA)

**Platinum MAA Design**:
```
Production Region (Phoenix)
├── RAC Database (2+ nodes)
│   ├── Active Data Guard to Standby
│   ├── Far Sync for zero data loss
│   └── Flashback Database enabled
├── Application Tier
│   ├── 3+ ADs with autoscaling
│   ├── Regional load balancer
│   └── Instance pools (9+ instances)
└── Storage
    ├── Block Volume: Cross-AD replication
    ├── Object Storage: Cross-region replication
    └── File Storage: Snapshots every hour

DR Region (Ashburn)
├── Standby Database (Active Data Guard)
│   ├── Read-only queries allowed
│   └── Automatic failover <30s
├── Application Tier
│   ├── Scaled-down (30% capacity)
│   └── Auto-scale on failover trigger
└── Storage (replicated from primary)
```

**Zero Data Loss Architecture**:
```
Primary DB ←→ Far Sync Instance ←→ Standby DB
  (Phoenix)      (LA or Denver)       (Ashburn)
     ↓                                      ↓
Synchronous            Combined:       Asynchronous
(Zero loss)         Zero data loss    (Performance)
```

### Chaos Engineering

**Resilience Testing Patterns**:

**Availability Domain Failure Simulation**:
```python
# Simulate AD failure
def simulate_ad_failure(ad_name):
    instances = get_instances_in_ad(ad_name)

    for instance in instances:
        # Stop all instances in AD
        compute_client.instance_action(
            instance.id,
            action="STOP"
        )

    # Verify:
    # - Load balancer removes unhealthy backends
    # - Traffic routes to remaining ADs
    # - Alarms fire correctly
    # - Auto-scaling compensates
```

**Database Failover Drill**:
```bash
# Scheduled monthly DR drill
# 1. Initiate failover
oci db data-guard-association failover \
  --database-id $STANDBY_DB_ID \
  --database-admin-password $ADMIN_PASS

# 2. Update DNS
oci dns record update \
  --zone-name example.com \
  --domain app.example.com \
  --rdata $DR_LB_IP

# 3. Verify application functionality
# 4. Document RTO/RPO actuals
# 5. Reinstate original primary as new standby
```

---

## Migration Strategies

### Assessment and Planning

**Migration Complexity Matrix**:
| Workload Type | Complexity | Strategy | Tools |
|---------------|------------|----------|-------|
| Stateless Web Apps | Low | Lift-and-Shift | Rackware, Custom Scripts |
| Databases (Oracle) | Medium | Replatform | Data Guard, GoldenGate |
| Legacy Apps | High | Refactor | Containerize, Modernize |
| Data Warehouses | Medium | Rebuild | ADW, Data Integration |

### Database Migration

**Zero-Downtime Oracle Migration**:
```
Source Database (On-Premises)
    ↓
GoldenGate Replication →→→ Target (OCI DB System)
    ↓                           ↓
Keep in sync               Apply changes real-time
    ↓                           ↓
Cutover: Switch application connection string
```

**Steps**:
```bash
# 1. Setup OCI target database
oci db system launch \
  --db-version "19.0.0.0" \
  --db-edition "ENTERPRISE_EDITION_EXTREME_PERFORMANCE"

# 2. Configure GoldenGate
# - Install GoldenGate on source
# - Install GoldenGate on target
# - Configure Extract (source)
# - Configure Replicat (target)

# 3. Initial data load
expdp user/pass DIRECTORY=dp_dir DUMPFILE=initial.dmp

# 4. Start replication
GGSCI> START EXTRACT ext_prod
GGSCI> START REPLICAT rep_prod

# 5. Monitor lag
GGSCI> INFO EXTRACT ext_prod, DETAIL

# 6. Cutover (when lag < 1 minute)
# - Stop application
# - Verify replication caught up
# - Update connection strings
# - Start application on OCI
```

**Autonomous Database Migration**:
```bash
# Using Data Pump
# 1. Export from source
expdp admin/pass@sourcedb \
  DIRECTORY=dump_dir \
  DUMPFILE=prod_export.dmp \
  FULL=Y

# 2. Upload to Object Storage
oci os object put \
  --bucket-name migrations \
  --file prod_export.dmp

# 3. Import to Autonomous Database
# Create credential
BEGIN
  DBMS_CLOUD.CREATE_CREDENTIAL(
    credential_name => 'OBJ_STORE_CRED',
    username => 'tenancy/user',
    password => 'auth_token'
  );
END;

# Import data
BEGIN
  DBMS_CLOUD.DATA_PUMP(
    operation => 'IMPORT',
    credential_name => 'OBJ_STORE_CRED',
    file_uri_list => 'https://objectstorage.../prod_export.dmp',
    format => json_object('schema' value 'PRODSCHEMA')
  );
END;
```

### Application Migration Patterns

**Lift-and-Shift**:
```
On-Premises VM
    ↓ Convert to OCI-compatible image
OCI Custom Image
    ↓ Deploy
OCI Compute Instance
```

**Replatform (Containers)**:
```
Traditional App on VMs
    ↓ Containerize
Docker Images
    ↓ Deploy to
OKE (Kubernetes)
    ↓ Benefits
- Auto-scaling
- Self-healing
- Easier updates
```

**Refactor (Cloud-Native)**:
```
Monolithic Application
    ↓ Break into
Microservices
    ↓ Deploy as
- API Gateway (entry point)
- Functions (serverless logic)
- Container Engine (stateful services)
- Autonomous Database (data layer)
- Object Storage (static content)
```

---

## Performance at Scale

### Global-Scale Architecture

**CDN Integration**:
```
Global Users
    ↓
CloudFlare/Akamai CDN
    ├── Cache static content
    ├── DDoS protection
    └── SSL termination
        ↓
OCI Load Balancer
    ↓
Origin Servers (OCI)
```

**API Performance**:
```
API Gateway
├── Rate Limiting (per client)
├── Response Caching
├── Request/Response transformation
└── Authentication offload
    ↓
Backend Services
├── Connection pooling
├── Async processing (Queue/Stream)
└── Database connection optimization
```

### Database Performance Optimization

**Autonomous Database Tuning**:
```sql
-- Auto-scaling monitors and adjusts
-- Automatic indexing
-- Automatic SQL tuning

-- Monitor performance
SELECT sql_id, cpu_time, elapsed_time, executions
FROM v$sql
WHERE cpu_time > 1000000
ORDER BY cpu_time DESC;

-- Real-time monitoring
SELECT * FROM v$active_session_history
WHERE sample_time > SYSDATE - INTERVAL '15' MINUTE
ORDER BY sample_time DESC;
```

**RAC Performance**:
```
Connection Load Balancing:
- Use SCAN (Single Client Access Name)
- Automatic workload distribution
- Runtime connection balancing

Service-Based Routing:
- OLTP service → Node 1, 2
- Reporting service → Node 3
- Batch service → Node 4
```

### Compute Performance at Scale

**HPC Cluster Design**:
```
HPC Cluster Network
├── RDMA Cluster Network (100 Gbps)
├── BM.HPC instances
│   ├── Node 1-16: Compute nodes
│   └── Node 17: Head node
└── NFS shared storage
    ├── File Storage (persistent)
    └── Block Volume (high IOPS)
```

**Container Performance**:
```
OKE Optimization:
├── Node Pools per workload type
│   ├── Compute-intensive: E4.Flex
│   ├── Memory-intensive: E4.Flex (high RAM)
│   └── GPU workloads: GPU shapes
├── Pod anti-affinity rules
├── Resource requests/limits
└── Horizontal Pod Autoscaler
```

### Network Performance

**Maximum Throughput Design**:
```
FastConnect (10 Gbps)
    ↓
DRG
    ├─→ VCN 1 (Production)
    │   └── BM.Standard.E4.128 (2x 50 Gbps NICs)
    ├─→ VCN 2 (Analytics)
    │   └── BM.Standard.E4.128
    └─→ VCN 3 (Development)
```

**Load Balancer Optimization**:
```terraform
resource "oci_load_balancer_load_balancer" "high_performance" {
  shape = "flexible"

  shape_details {
    minimum_bandwidth_in_mbps = 1000  # 1 Gbps
    maximum_bandwidth_in_mbps = 8000  # 8 Gbps
  }

  # Connection settings
  # Idle timeout for persistent connections
  # Enable HTTP/2 for multiplexing
}
```

---

## Exam Tips

### Critical Concepts

**Multi-Region**:
- Active-Active for global performance
- Traffic Manager for DNS-based routing
- Cross-region database replication (GoldenGate, Data Guard)
- Data sovereignty considerations

**Hybrid**:
- FastConnect for private connectivity
- DRG v2 for advanced routing
- Cloud@Customer for data residency
- Multi-cloud integration (Azure Interconnect)

**HA/DR**:
- MAA for maximum availability
- Zero data loss with Far Sync
- Chaos engineering for validation
- Automated failover procedures

**Migration**:
- Assessment first (complexity matrix)
- Zero-downtime with GoldenGate
- Lift-and-shift, replatform, or refactor
- Validate performance post-migration

**Performance**:
- CDN for global content delivery
- HPC clusters for compute-intensive
- Autonomous DB auto-tuning
- Network optimization (FastConnect, shapes)

### Common Scenarios

**Q: Global application, <50ms latency worldwide?**
A: Multi-region active-active + CDN + geolocation routing

**Q: Zero data loss DR requirement?**
A: Data Guard with Far Sync + synchronous replication

**Q: Migrate 50TB Oracle database with <1 hour downtime?**
A: GoldenGate replication + planned cutover

**Q: On-premises data cannot leave country?**
A: Exadata Cloud@Customer or Dedicated Region

**Q: 100,000 concurrent API requests?**
A: API Gateway + autoscaling instance pools + caching

### Design Patterns

**High Availability Checklist**:
- [ ] Multi-AD deployment
- [ ] Load balancer with health checks
- [ ] Database replication (Data Guard/RAC)
- [ ] Auto-scaling configured
- [ ] Monitoring and alerting
- [ ] Automated failover tested

**DR Checklist**:
- [ ] RPO/RTO defined
- [ ] Cross-region replication
- [ ] DR drills scheduled
- [ ] Runbooks documented
- [ ] Failover tested quarterly
- [ ] Failback procedure validated

---

## Summary

**Multi-Region**: Global scale, data sovereignty, active-active patterns

**Hybrid**: FastConnect, DRG v2, Cloud@Customer, multi-cloud

**HA/DR**: MAA, zero data loss, chaos engineering, automated failover

**Migration**: Assessment, zero-downtime, database migration tools

**Performance**: CDN, HPC, database tuning, network optimization

---

**Next**: Advanced Networking and Security

## Key terms

- **Oracle Cloud Infrastructure Kubernetes Engine (OKE)** - the OCI managed Kubernetes service that runs and manages containerised applications.
- **OCI Functions** - the OCI serverless platform for running short-lived functions, based on the open source Fn Project.
- **API Gateway** - the OCI service that publishes APIs and applies routing, authentication and rate limiting in front of backends.
- **OCI Data Science** - the OCI platform for building, training and deploying machine learning models.
- **OCI Data Catalog** - the OCI service that harvests metadata so teams can discover and govern data assets.
- **Application Performance Monitoring (APM)** - the OCI service that traces and measures application behaviour to find performance problems.
