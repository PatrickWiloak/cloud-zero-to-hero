# Rate and Usage Optimization

**[📖 Rate Optimization](https://www.finops.org/framework/capabilities/rate-optimization/)** - Rate optimization capability
**[📖 Usage Optimization](https://www.finops.org/framework/capabilities/workload-optimization/)** - Workload optimization capability

## Overview

This document covers rate optimization (getting better prices) and usage optimization (reducing waste and right-sizing). These are the primary mechanisms for reducing cloud costs and represent core engineering skills for the FinOps Certified Engineer exam.

## Rate Optimization

### Commitment-Based Discounts

#### AWS
| Instrument | Discount | Flexibility | Term |
|-----------|----------|-------------|------|
| Reserved Instances (RI) | 30-72% | Instance-specific or convertible | 1 or 3 years |
| Savings Plans (Compute) | 30-66% | Any instance family, region, OS | 1 or 3 years |
| Savings Plans (EC2) | Up to 72% | Fixed instance family and region | 1 or 3 years |
| Savings Plans (SageMaker) | Up to 64% | SageMaker ML instances | 1 or 3 years |

**[📖 AWS Savings Plans](https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html)** - Savings Plans documentation
**[📖 AWS Reserved Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html)** - RI documentation

#### Azure
| Instrument | Discount | Flexibility | Term |
|-----------|----------|-------------|------|
| Azure Reservations | Up to 72% | Scope flexibility (shared/single) | 1 or 3 years |
| Azure Savings Plans | Up to 65% | Compute service flexibility | 1 or 3 years |

**[📖 Azure Reservations](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/)** - Reservation documentation

#### GCP
| Instrument | Discount | Flexibility | Term |
|-----------|----------|-------------|------|
| Committed Use Discounts (CUD) | Up to 57% | Spend or resource-based | 1 or 3 years |
| Sustained Use Discounts (SUD) | Up to 30% | Automatic, no commitment | Monthly (auto) |

**[📖 GCP CUDs](https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview)** - CUD documentation

### Commitment Strategy
1. **Analyze baseline usage** - Identify steady-state workloads (minimum consistent usage)
2. **Cover baseline with commitments** - Reserved Instances or Savings Plans for predictable usage
3. **Use on-demand for variable** - On-demand for above-baseline peaks
4. **Layer commitments** - Mix of 1-year and 3-year for flexibility
5. **Review quarterly** - Reassess coverage and utilization

### Commitment Metrics
| Metric | Formula | Target |
|--------|---------|--------|
| Coverage | Committed hours / total hours | 60-80% |
| Utilization | Used committed hours / purchased committed hours | > 95% |
| Effective savings rate | Savings from commitments / on-demand equivalent | 25-50% |
| Waste from unused commitments | Unused committed cost / total committed cost | < 5% |

### Spot/Preemptible Instances
| Provider | Name | Discount | Interruption Notice |
|----------|------|----------|-------------------|
| AWS | Spot Instances | Up to 90% | 2 minutes |
| Azure | Spot VMs | Up to 90% | 30 seconds |
| GCP | Preemptible/Spot VMs | Up to 91% | 30 seconds |

**Suitable Workloads:**
- Batch processing and data pipelines
- CI/CD build agents
- Stateless web servers behind load balancers
- Machine learning training (with checkpointing)
- Testing and development environments

**Not Suitable:**
- Stateful databases
- Long-running transactions
- Single-instance critical services
- Workloads that cannot tolerate interruption

## Usage Optimization

### Right-Sizing

#### What is Right-Sizing?
- Matching resource allocation to actual usage
- Most impactful optimization for compute resources
- Analysis of CPU, memory, network, and disk utilization
- Downsizing over-provisioned resources
- Upgrading under-provisioned resources (efficiency improvement)

#### Right-Sizing Process
```
1. Collect metrics (14-30 days minimum)
   - CPU utilization (average, peak, p95)
   - Memory utilization
   - Network throughput
   - Disk I/O

2. Analyze utilization patterns
   - Average utilization < 20% = likely oversized
   - Peak utilization < 40% = candidate for downsizing
   - Consistent high utilization = consider scaling strategy

3. Generate recommendations
   - Match to smaller instance type
   - Consider instance family changes (compute vs memory optimized)
   - Account for burst requirements

4. Implement changes
   - Start with non-production environments
   - Validate performance after change
   - Monitor for 1-2 weeks
```

#### Cloud Provider Recommendations
| Provider | Tool | Scope |
|----------|------|-------|
| AWS | Cost Optimization Hub, Compute Optimizer | EC2, EBS, Lambda, ECS |
| Azure | Azure Advisor | VMs, SQL, App Service |
| GCP | Recommender | Compute Engine, GKE |

### Idle Resource Elimination

#### Common Idle Resources
| Resource | How to Detect | Action |
|----------|--------------|--------|
| Unattached EBS volumes | No attached instance | Delete or snapshot |
| Unused Elastic IPs | No associated instance | Release |
| Idle load balancers | Zero requests over 14+ days | Delete |
| Stopped instances | Stopped for 30+ days | Terminate or snapshot AMI |
| Unused RDS instances | Zero connections | Delete or stop |
| Old snapshots | Created > 90 days, no restore | Delete |
| Unused NAT Gateways | Zero bytes processed | Delete |

#### Automation for Waste Elimination
```
# Policy-based cleanup patterns:
1. Tag unattached volumes with "cleanup-date" = today + 14 days
2. Alert resource owner
3. If no response within 14 days, snapshot and delete
4. Retain snapshot for 30 days as safety net
```

### Auto-Scaling

#### Scaling Strategies
| Strategy | Description | Best For |
|----------|-------------|----------|
| Target tracking | Maintain metric at target value | Predictable workloads |
| Step scaling | Add/remove capacity at thresholds | Variable workloads |
| Scheduled scaling | Scale on time schedule | Known traffic patterns |
| Predictive scaling | ML-based forecasting | Repeating patterns |

#### Scaling Best Practices
1. **Scale in/out, not up/down** - Horizontal scaling is more cost-effective
2. **Set appropriate cooldown periods** - Prevent thrashing
3. **Monitor scaling events** - Ensure scaling matches actual demand
4. **Test failure scenarios** - Verify scale-in does not remove needed capacity
5. **Set minimum and maximum** - Protect against runaway scaling

### Storage Optimization

#### Storage Tiering
```
Data Lifecycle:
Hot (frequent access) --> Warm (monthly) --> Cold (quarterly) --> Archive (yearly)
  S3 Standard             S3 IA              S3 Glacier IA        S3 Glacier Deep

Implement lifecycle policies:
- Move to IA after 30 days
- Move to Glacier IA after 90 days
- Move to Glacier Deep Archive after 365 days
- Delete after 7 years (if compliance allows)
```

#### Storage Optimization Actions
1. **Lifecycle policies** - Automate data tiering based on age
2. **Compression** - Reduce storage volume (Parquet vs CSV)
3. **Deduplication** - Remove redundant data copies
4. **Old snapshot cleanup** - Delete outdated snapshots
5. **Log retention** - Set appropriate retention periods

### Kubernetes Cost Optimization
- **Right-size pods** - Match resource requests to actual usage
- **Cluster autoscaler** - Scale nodes based on pending pods
- **Spot/Preemptible nodes** - Use for fault-tolerant workloads
- **Resource quotas** - Prevent over-provisioning per namespace
- **Vertical Pod Autoscaler** - Auto-adjust pod resource requests

## Optimization Priority Framework

### Impact vs Effort Matrix
| Priority | Impact | Effort | Examples |
|----------|--------|--------|---------|
| 1 (Quick wins) | High | Low | Delete idle resources, right-size obvious cases |
| 2 (Strategic) | High | Medium | Commitment purchases, auto-scaling implementation |
| 3 (Incremental) | Medium | Low | Storage tiering, snapshot cleanup |
| 4 (Long-term) | High | High | Architecture redesign, cloud migration optimization |
| 5 (Low priority) | Low | High | Defer unless required |

### Optimization Cadence
- **Weekly:** Review anomalies and quick wins
- **Monthly:** Right-sizing recommendations and waste elimination
- **Quarterly:** Commitment coverage review and purchasing
- **Annually:** Architecture review and major optimization initiatives

## Key terms

- **Rate optimization** - paying less for the same resources, for example through commitment discounts or spot capacity.
- **Usage optimization** - using fewer or more appropriate resources, for example by rightsizing or removing waste.
- **Rightsizing** - matching resource size to actual demand so you stop paying for unused capacity.
- **Commitment discount** - a lower rate given in return for committing to a level of usage or spend over a fixed term.
