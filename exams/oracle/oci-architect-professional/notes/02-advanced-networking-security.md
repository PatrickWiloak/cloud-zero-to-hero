# OCI Architect Professional - Advanced Networking and Security

## Table of Contents
- [Advanced Network Architecture](#advanced-network-architecture)
- [Network Security](#network-security)
- [Security Compliance](#security-compliance)
- [Advanced Security Services](#advanced-security-services)
- [Exam Tips](#exam-tips)

---

## Advanced Network Architecture

### Complex VCN Topologies

**Hub-Spoke with Transit Routing**:
```
                    DRG (Hub)
                       |
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
   Hub VCN      Spoke VCN 1      Spoke VCN 2
   (Shared      (Production)     (Development)
   Services)
      |
   ┌──┴──┐
   ↓     ↓
FastConnect  VPN
   |         |
Corporate   Branch
Data Ctr    Offices
```

**DRG Route Table Design**:
```terraform
# Route table for VCNs
resource "oci_core_drg_route_table" "vcn_routes" {
  drg_id = oci_core_drg.main.id

  display_name = "vcn-routes"

  # Import routes from on-premises
  import_drg_route_distribution_id = oci_core_drg_route_distribution.onprem.id
}

# Route table for on-premises connections
resource "oci_core_drg_route_table" "onprem_routes" {
  drg_id = oci_core_drg.main.id

  display_name = "onprem-routes"

  # Import routes from VCNs
  import_drg_route_distribution_id = oci_core_drg_route_distribution.vcn.id
}

# Custom route rules
resource "oci_core_drg_route_table_route_rule" "to_prod" {
  drg_route_table_id = oci_core_drg_route_table.onprem_routes.id

  destination      = "10.1.0.0/16"  # Production VCN
  destination_type = "CIDR_BLOCK"
  next_hop_drg_attachment_id = oci_core_drg_attachment.prod_vcn.id
}
```

**VCN Peering Topologies**:

**Local Peering (Same Region)**:
```
VCN-A (10.0.0.0/16)
    |
    LPG-A ←→ LPG-B
                |
         VCN-B (10.1.0.0/16)

Routing:
VCN-A Route Table:
- 10.1.0.0/16 → LPG-A

VCN-B Route Table:
- 10.0.0.0/16 → LPG-B
```

**Remote Peering (Cross-Region)**:
```
Phoenix Region               Ashburn Region
VCN-A (10.0.0.0/16)     VCN-B (10.1.0.0/16)
    |                           |
    DRG-A                       DRG-B
      |                           |
      RPC-A ←────────────────→ RPC-B
         (Remote Peering Connection)
```

### Advanced Load Balancing

**Multi-Tier Load Balancing**:
```
Internet
    ↓
Public LB (Layer 7)
├── Path /api/* → Backend Set: API Servers
├── Path /app/* → Backend Set: App Servers
└── Path /* → Backend Set: Web Servers
    ↓
Private LB (Layer 7 - Internal)
├── Backend Set: Microservice A
├── Backend Set: Microservice B
└── Backend Set: Microservice C
```

**Load Balancer Advanced Features**:

**SSL Cipher Suites**:
```terraform
resource "oci_load_balancer_listener" "https" {
  load_balancer_id         = oci_load_balancer_load_balancer.main.id
  name                     = "https-listener"
  default_backend_set_name = "web-backend"
  port                     = 443
  protocol                 = "HTTP"

  ssl_configuration {
    certificate_name = "wildcard-cert"

    # Strong cipher suites only
    cipher_suite_name = "oci-modern-ssl-cipher-suite-v1"

    # TLS 1.2 and 1.3 only
    protocols = ["TLSv1.2", "TLSv1.3"]

    # Server order preference
    server_order_preference = "ENABLED"

    verify_peer_certificate = true
    verify_depth           = 3
  }
}
```

**Path Routing with Rules**:
```terraform
resource "oci_load_balancer_rule_set" "security_headers" {
  load_balancer_id = oci_load_balancer_load_balancer.main.id
  name             = "security-headers"

  items {
    action = "ADD_HTTP_RESPONSE_HEADER"
    header = "Strict-Transport-Security"
    value  = "max-age=31536000; includeSubDomains"
  }

  items {
    action = "ADD_HTTP_RESPONSE_HEADER"
    header = "X-Content-Type-Options"
    value  = "nosniff"
  }

  items {
    action = "ADD_HTTP_RESPONSE_HEADER"
    header = "X-Frame-Options"
    value  = "DENY"
  }
}
```

**Backend Health Checks**:
```terraform
resource "oci_load_balancer_backend_set" "advanced" {
  load_balancer_id = oci_load_balancer_load_balancer.main.id
  name             = "advanced-backend"
  policy           = "LEAST_CONNECTIONS"

  health_checker {
    protocol          = "HTTP"
    port              = 8080
    url_path          = "/health/detailed"
    return_code       = 200
    interval_ms       = 10000
    timeout_in_millis = 3000
    retries           = 3

    # Response body regex validation
    response_body_regex = "status.*ok"
  }

  # Session persistence
  session_persistence_configuration {
    cookie_name      = "LB_STICKY"
    disable_fallback = false
  }

  # SSL between LB and backends
  ssl_configuration {
    certificate_name        = "backend-cert"
    verify_peer_certificate = true
  }
}
```

### Traffic Management

**DNS Steering Policies**:

**Geolocation-Based**:
```terraform
resource "oci_dns_steering_policy" "geo_routing" {
  compartment_id = var.compartment_id
  display_name   = "global-geo-routing"
  template       = "CUSTOM"

  rules {
    rule_type = "FILTER"

    # North America to Phoenix
    cases {
      case_condition = "query.client.geoKey in ('na-US', 'na-CA')"
      answer_data {
        answer_condition = "answer.pool == 'phoenix'"
        value            = 100
      }
    }

    # Europe to Frankfurt
    cases {
      case_condition = "query.client.geoKey in ('eu-DE', 'eu-FR', 'eu-GB')"
      answer_data {
        answer_condition = "answer.pool == 'frankfurt'"
        value            = 100
      }
    }

    # Asia to Tokyo
    cases {
      case_condition = "query.client.geoKey in ('asia-JP', 'asia-KR')"
      answer_data {
        answer_condition = "answer.pool == 'tokyo'"
        value            = 100
      }
    }
  }

  # Failover if region unhealthy
  rules {
    rule_type = "HEALTH"

    cases {
      answer_data {
        answer_condition = "answer.isHealthy"
        value            = 100
      }
    }
  }
}
```

**Performance-Based Routing**:
```terraform
resource "oci_dns_steering_policy" "performance" {
  compartment_id = var.compartment_id
  display_name   = "performance-routing"
  template       = "CUSTOM"

  rules {
    rule_type = "WEIGHTED"

    # Route based on health check response time
    default_answer_data {
      answer_condition = "answer.isHealthy"
      value            = "answer.rdata.latency"  # Lower latency = higher priority
    }
  }
}
```

### Private Connectivity

**Private Access Channel**:
```
Corporate Network
    ↓
FastConnect Private Virtual Circuit
    ↓
DRG (with private IP ranges)
    ↓
VCN (no Internet Gateway)
    ↓
Private Endpoints:
├── Autonomous Database (private endpoint)
├── Object Storage (via Service Gateway)
├── APIs (API Gateway with private endpoint)
└── Applications (private subnets only)
```

**Service Gateway Configuration**:
```terraform
resource "oci_core_service_gateway" "private_services" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "service-gateway"

  services {
    # All services in OCI region
    service_id = data.oci_core_services.all_services.services[0].id
  }

  # Route table for service gateway
  route_table_id = oci_core_route_table.service_gateway_routes.id
}

# Route table
resource "oci_core_route_table" "service_gateway_routes" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "sgw-routes"

  # Return traffic to Service Gateway
  route_rules {
    destination       = data.oci_core_services.all_services.services[0].cidr_block
    destination_type  = "SERVICE_CIDR_BLOCK"
    network_entity_id = oci_core_service_gateway.private_services.id
  }
}
```

---

## Network Security

### Micro-Segmentation

**Application-Layer Security**:
```
Frontend NSG (web-nsg)
├── Ingress: 0.0.0.0/0:443 (HTTPS from internet)
└── Egress: app-nsg:8080 (to application tier)

Application NSG (app-nsg)
├── Ingress: web-nsg:8080 (from web tier only)
├── Egress: db-nsg:1521 (to database)
└── Egress: cache-nsg:6379 (to Redis cache)

Database NSG (db-nsg)
├── Ingress: app-nsg:1521 (from app tier only)
└── Egress: backup-nsg:443 (to backup storage)

Cache NSG (cache-nsg)
├── Ingress: app-nsg:6379
└── Egress: None (no outbound)
```

**NSG Implementation**:
```terraform
# Database NSG - strictest security
resource "oci_core_network_security_group" "database" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "database-nsg"
}

# Only allow from application tier
resource "oci_core_network_security_group_security_rule" "db_from_app" {
  network_security_group_id = oci_core_network_security_group.database.id
  direction                 = "INGRESS"
  protocol                  = "6"  # TCP

  source_type = "NETWORK_SECURITY_GROUP"
  source      = oci_core_network_security_group.application.id

  tcp_options {
    destination_port_range {
      min = 1521
      max = 1521
    }
  }

  description = "Allow Oracle SQL*Net from application tier"
}

# Log all denied traffic
resource "oci_core_network_security_group_security_rule" "db_deny_all" {
  network_security_group_id = oci_core_network_security_group.database.id
  direction                 = "INGRESS"
  protocol                  = "all"

  source_type = "CIDR_BLOCK"
  source      = "0.0.0.0/0"

  # This rule is for logging (actual deny is implicit)
  description = "Log all other traffic (implicitly denied)"
}
```

### Network Monitoring

**VCN Flow Logs**:
```terraform
resource "oci_logging_log" "vcn_flow_logs" {
  display_name = "vcn-flow-logs"
  log_group_id = oci_logging_log_group.network.id
  log_type     = "SERVICE"

  configuration {
    source {
      category    = "all"
      resource    = oci_core_subnet.app_subnet.id
      service     = "flowlogs"
      source_type = "OCISERVICE"
    }

    compartment_id = var.compartment_id
  }

  is_enabled         = true
  retention_duration = 30  # days
}
```

**Flow Log Analysis**:
```
Query: Find suspicious SSH attempts
─────────────────────────────────
search "compartment-ocid/network-logs" |
where data.destinationPort == 22 |
where data.action == "REJECT" |
stats count() by data.sourceAddress |
sort by count desc |
limit 20

Query: High bandwidth consumers
───────────────────────────────
search "compartment-ocid/network-logs" |
eval totalBytes = data.bytesIn + data.bytesOut |
stats sum(totalBytes) as bandwidth by data.sourceAddress, data.destinationAddress |
sort by bandwidth desc
```

### DDoS Protection

**Built-in DDoS Protection**:
```
Layer 3/4 DDoS Protection (Automatic):
├── SYN flood protection
├── UDP flood protection
├── ICMP flood protection
└── Automatic mitigation (no configuration needed)
```

**Application-Layer Protection**:
```terraform
# WAF for Layer 7 protection
resource "oci_waf_web_app_firewall" "main" {
  compartment_id              = var.compartment_id
  backend_type                = "LOAD_BALANCER"
  load_balancer_id            = oci_load_balancer_load_balancer.main.id
  web_app_firewall_policy_id = oci_waf_web_app_firewall_policy.main.id
  display_name                = "app-waf"
}

# WAF Policy
resource "oci_waf_web_app_firewall_policy" "main" {
  compartment_id = var.compartment_id
  display_name   = "app-waf-policy"

  # Rate limiting
  request_rate_limiting {
    rules {
      name               = "rate-limit-api"
      condition_language = "JMESPATH"
      condition          = "request.path =~ '/api/.*'"

      configurations {
        period_in_seconds = 60
        requests_limit    = 100  # 100 requests per minute
        action_duration_in_seconds = 60
      }
    }
  }

  # Protection rules
  request_protection {
    rules {
      name               = "block-sql-injection"
      protection_capability {
        key     = "941100"  # SQL Injection
        version = 1
      }
      action_name = "BLOCK"
    }

    rules {
      name = "block-xss"
      protection_capability {
        key     = "941110"  # Cross-Site Scripting
        version = 1
      }
      action_name = "BLOCK"
    }
  }
}
```

---

## Security Compliance

### Regulatory Compliance Architecture

**GDPR Compliance Pattern**:
```
Data Classification:
├── Personal Data (PII)
│   ├── Encryption: Customer-managed keys (Vault)
│   ├── Storage: EU region only
│   ├── Access: Restricted by IAM policies
│   └── Audit: All access logged
├── Sensitive Data
│   ├── Encryption: Oracle-managed keys
│   ├── Storage: Regional with replication
│   └── Access: Role-based
└── Public Data
    ├── Encryption: Optional
    └── Access: Unrestricted (within security guidelines)
```

**Data Residency Controls**:
```terraform
# Enforce EU-only storage
resource "oci_identity_policy" "eu_data_residency" {
  compartment_id = var.tenancy_ocid
  name           = "EU-Data-Residency"
  description    = "Prevent data from leaving EU regions"

  statements = [
    # Block bucket creation in non-EU regions
    "Allow group DataAdmins to manage buckets in compartment GDPR-Data where request.region in ('eu-frankfurt-1', 'eu-amsterdam-1', 'eu-zurich-1')",

    # Block instance creation with data in non-EU
    "Deny group DataAdmins to manage instances in compartment GDPR-Data where request.region not in ('eu-frankfurt-1', 'eu-amsterdam-1', 'eu-zurich-1')",
  ]
}

# Security Zone for GDPR compliance
resource "oci_cloud_guard_security_zone" "gdpr" {
  compartment_id = var.compartment_id
  display_name   = "GDPR-Security-Zone"

  security_zone_recipe_id = oci_cloud_guard_security_zone_recipe.gdpr_recipe.id
}
```

**PCI-DSS Compliance**:
```
Card Data Environment (CDE):
├── Network Isolation
│   ├── Dedicated VCN
│   ├── No internet access (NAT Gateway only)
│   └── Firewall rules (NSGs)
├── Encryption
│   ├── All data encrypted at rest (Vault keys)
│   ├── TLS 1.2+ for all connections
│   └── Key rotation every 90 days
├── Access Control
│   ├── MFA required for all access
│   ├── Least privilege policies
│   └── Regular access reviews
├── Monitoring
│   ├── All access logged (audit logs)
│   ├── Real-time alerting (Cloud Guard)
│   └── Log retention: 1 year minimum
└── Vulnerability Management
    ├── Monthly vulnerability scans
    ├── Quarterly penetration tests
    └── Patch management automation
```

### Encryption Strategy

**Key Management Hierarchy**:
```
Master Encryption Key (Vault)
    ↓ (encrypts)
Data Encryption Keys
    ↓ (encrypts)
Application Data

Key Hierarchy:
├── Root Key (HSM-protected)
│   └── Never exported
├── Master Keys (Vault)
│   ├── Production-Data-Key
│   ├── Backup-Data-Key
│   └── Archive-Data-Key
└── Data Encryption Keys (Generated per resource)
    ├── Block Volume DEKs
    ├── Object Storage DEKs
    └── Database TDE Keys
```

**Key Rotation Strategy**:
```bash
# Automated key rotation
oci kms management key update \
  --key-id ocid1.key.oc1... \
  --management-endpoint "https://..." \
  --auto-key-rotation-details '{
    "rotation-interval-in-days": 90,
    "rotation-mode": "AUTO",
    "time-of-next-rotation": "2024-12-01T00:00:00Z"
  }'

# Rotation impact:
# - New key version created
# - New resources use new key version
# - Existing resources re-encrypted (background)
# - No downtime
```

---

## Advanced Security Services

### Cloud Guard Advanced

**Custom Detector Creation**:
```
Custom Detector: Detect High-Cost Resources
─────────────────────────────────────────
Trigger: Instance launched with shape > 32 OCPUs
Action: Alert security team + Auto-stop if not tagged "Approved"

Detector Recipe:
{
  "detectorType": "CUSTOM",
  "name": "High-Cost-Instance-Detector",
  "trigger": {
    "eventType": "com.oraclecloud.computeapi.launchinstance.end",
    "condition": "resourceConfig.shape.ocpus > 32"
  },
  "severity": "HIGH"
}

Responder Recipe:
{
  "name": "Stop-Unapproved-High-Cost",
  "condition": "target.resource.tag.Approved != 'true'",
  "actions": [
    {
      "type": "STOP_INSTANCE",
      "mode": "AUTOACTION"
    },
    {
      "type": "NOTIFICATION",
      "topicId": "ocid1.onstopic..."
    }
  ]
}
```

**Security Automation with Events + Functions**:
```python
# Function: Auto-remediate security violations
import oci
import json

def handler(ctx, data: dict):
    problem = json.loads(data)

    if problem["problemName"] == "Bucket is Public":
        # Automatically make bucket private
        object_storage = oci.object_storage.ObjectStorageClient(
            oci.auth.signers.get_resource_principals_signer()
        )

        bucket_name = problem["resourceName"]
        namespace = problem["namespace"]

        object_storage.update_bucket(
            namespace,
            bucket_name,
            oci.object_storage.models.UpdateBucketDetails(
                public_access_type="NoPublicAccess"
            )
        )

        return {
            "status": "remediated",
            "action": "Made bucket private",
            "bucket": bucket_name
        }
```

### Security Information and Event Management (SIEM) Integration

**Log Export to SIEM**:
```
OCI Logging
    ↓
Service Connector Hub
    ↓
Streaming
    ↓
Kafka Connect
    ↓
External SIEM (Splunk, QRadar, etc.)
```

**Configuration**:
```terraform
# Stream for SIEM
resource "oci_streaming_stream" "siem" {
  compartment_id     = var.compartment_id
  name               = "siem-stream"
  partitions         = 3
  retention_in_hours = 24
}

# Service Connector: Logs → Stream
resource "oci_sch_service_connector" "logs_to_siem" {
  compartment_id = var.compartment_id
  display_name   = "logs-to-siem"

  source {
    kind = "logging"

    log_sources {
      compartment_id = var.compartment_id
      log_group_id   = oci_logging_log_group.security.id
    }
  }

  target {
    kind      = "streaming"
    stream_id = oci_streaming_stream.siem.id
  }
}
```

---

## Exam Tips

### Critical Concepts

**Networking**:
- DRG v2: Advanced routing with route tables
- Hub-spoke: Transit routing for complex topologies
- VCN peering: Local (same region) vs Remote (cross-region)
- Load balancer: Path routing, SSL termination, health checks

**Security**:
- Micro-segmentation: NSGs per application tier
- Zero trust: Deny by default, allow explicitly
- Encryption: At rest (Vault) and in transit (TLS)
- Cloud Guard: Detection (passive) + Responder (active)

**Compliance**:
- Data residency: Region-specific storage
- GDPR: EU regions, encryption, access controls
- PCI-DSS: Network isolation, encryption, monitoring
- Key rotation: Automated, no downtime

### Common Scenarios

**Q: Complex multi-VCN connectivity with on-premises?**
A: DRG as hub with custom route tables + FastConnect

**Q: Prevent database access except from app tier?**
A: NSGs with source NSG restrictions

**Q: Automatically remediate security violations?**
A: Cloud Guard responders in AUTOACTION mode

**Q: GDPR-compliant architecture?**
A: EU regions + Security Zones + Vault + Audit logs

**Q: DDoS protection?**
A: Built-in L3/4 + WAF for L7 + Rate limiting

---

## Summary

**Networking**: DRG v2, hub-spoke, load balancing, private connectivity

**Security**: Micro-segmentation, zero trust, WAF, DDoS protection

**Compliance**: GDPR, PCI-DSS, data residency, encryption

**Monitoring**: Flow logs, Cloud Guard, SIEM integration

---

**Next**: Advanced Services and Optimization

## Key terms

- **Dynamic Routing Gateway (DRG)** - a virtual router that connects VCNs to each other and to on-premises networks.
- **Local peering gateway (LPG)** - a VCN component that peers two VCNs in the same region.
- **FastConnect** - the OCI service that provides a dedicated private connection between your network and OCI.
- **Network security group (NSG)** - a set of virtual firewall rules applied to chosen resources inside a VCN.
- **Cloud Guard** - the OCI service that detects security problems and misconfigurations and can respond to them.
- **OCI Vault** - the OCI service that manages encryption keys and secrets.
- **Web Application Firewall (WAF)** - an OCI service that filters and blocks malicious web traffic to applications.
