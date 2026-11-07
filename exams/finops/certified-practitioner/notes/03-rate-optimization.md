# Rate Optimization Strategies

**[📖 Rate Optimization](https://www.finops.org/framework/capabilities/rate-optimization/)** - FinOps rate optimization capability
**[📖 Managing Commitment Discounts](https://www.finops.org/framework/capabilities/manage-commitment-based-discounts/)** - Commitment management

## Rate Optimization Overview

Rate optimization focuses on reducing the unit cost of cloud resources by leveraging discounts, commitments, and alternative pricing models. It is one of two optimization approaches in FinOps (the other being usage optimization).

**Key Principle:** Rate optimization is about paying less for the same resource, while usage optimization is about using fewer or more appropriate resources.

## Reserved Instances (RIs)

### How Reserved Instances Work
- Commit to using a specific resource type for 1 or 3 years
- Receive a significant discount compared to on-demand pricing
- The commitment applies whether or not you use the resource
- Available across AWS, Azure (Reserved VM Instances), and GCP (CUDs)

### AWS Reserved Instances

**Standard RIs:**
- Fixed instance type, platform, tenancy, and region
- Cannot change instance family
- Can be sold on the RI Marketplace
- Highest discount (up to 72% off on-demand)

**Convertible RIs:**
- Can change instance family, OS, and tenancy
- Cannot be sold on the RI Marketplace
- Lower discount than Standard (up to 66% off on-demand)
- More flexibility for changing workloads

**Payment Options:**
| Payment Type | Discount Level | Cash Flow Impact |
|-------------|---------------|-----------------|
| All Upfront | Highest discount | Large upfront cost |
| Partial Upfront | Medium discount | Split payment |
| No Upfront | Lowest discount | Monthly payments |

**Scope Options:**
- **Regional:** Applies to any AZ in the region, provides capacity reservation
- **Zonal:** Applies to specific AZ, provides capacity reservation in that AZ

### Azure Reserved VM Instances

- 1-year or 3-year terms
- Up to 72% savings
- Instance size flexibility within same series
- Can be exchanged or refunded (with limitations)
- Shared or single subscription scope

**[📖 Azure Reserved Instances](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations)** - Azure RI documentation

### GCP Committed Use Discounts (CUDs)

**Resource-based CUDs:**
- Commit to specific vCPU and memory amounts
- 1-year (37% discount) or 3-year (55% discount)
- Apply automatically to matching usage
- Cannot be cancelled

**Spend-based CUDs:**
- Commit to minimum hourly spend
- Available for specific services (Cloud SQL, BigQuery)
- More flexible than resource-based
- 25% discount for 1-year, 52% for 3-year

**[📖 GCP Committed Use Discounts](https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview)** - GCP CUD documentation

## Savings Plans (AWS)

**[📖 AWS Savings Plans](https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html)** - AWS Savings Plans documentation

### Compute Savings Plans
- Most flexible option
- Applies across EC2, Lambda, and Fargate
- Any instance family, size, region, OS, or tenancy
- Up to 66% savings
- Best for workloads that may change instance types

### EC2 Instance Savings Plans
- Locked to specific instance family in a region
- Any size, OS, or tenancy within that family
- Up to 72% savings
- Best for stable workloads with known instance families

### SageMaker Savings Plans
- Specific to SageMaker ML instances
- Up to 64% savings
- Any instance family, size, or region

### Savings Plans vs Reserved Instances

| Feature | Savings Plans | Reserved Instances |
|---------|--------------|-------------------|
| Commitment type | Dollar per hour | Specific instance |
| Flexibility | More flexible | Less flexible |
| Instance family changes | Yes (Compute SP) | No (Standard RI) |
| Region changes | Yes (Compute SP) | No |
| Service coverage | EC2, Lambda, Fargate | EC2 only |
| Marketplace resale | No | Yes (Standard RI) |

## Spot and Preemptible Instances

### AWS Spot Instances
- Up to 90% discount vs on-demand
- Can be interrupted with 2-minute warning
- Price fluctuates based on supply and demand
- Use Spot Fleet for managing spot capacity

**Best Practices:**
- Use for fault-tolerant workloads
- Implement graceful shutdown handling
- Diversify across instance types and AZs
- Use Spot Fleet or Auto Scaling with mixed instances

### Azure Spot VMs
- Up to 90% discount
- Can be evicted based on capacity or price
- Set maximum price to control costs
- Available for VM Scale Sets

### GCP Preemptible VMs / Spot VMs
- Up to 91% discount
- Can be preempted with 30-second warning
- Maximum 24-hour runtime (preemptible)
- Spot VMs have no maximum runtime but can be evicted

### Ideal Spot/Preemptible Workloads
- Batch processing and data analytics
- CI/CD pipelines and build systems
- Testing and quality assurance
- Web crawling and data scraping
- Machine learning training
- Rendering and encoding
- Big data processing (EMR, Dataproc)

### Poor Spot/Preemptible Use Cases
- Production web servers (unless behind load balancer with on-demand backup)
- Databases (data loss risk)
- Stateful applications without checkpointing
- Real-time processing with strict SLAs

## Enterprise and Volume Discounts

### Enterprise Discount Programs (EDPs)
- Negotiated directly with cloud providers
- Based on total spend commitment
- Typically require $1M+ annual spend
- Custom discount percentages
- May include additional benefits (support, credits)

### Private Pricing
- Custom pricing for specific services
- Negotiated based on usage volume
- May include custom terms and conditions
- Common for large enterprises

### Marketplace Discounts
- Third-party software through cloud marketplaces
- May count toward EDP commitments
- Consolidated billing through cloud provider
- Sometimes better pricing than direct purchase

## Commitment Planning

### Coverage Analysis
- Identify stable, predictable workloads
- Calculate baseline resource usage
- Determine appropriate commitment level
- Leave headroom for growth and variability

### Risk Assessment
- What happens if workload changes?
- Can commitments be modified or resold?
- What is the financial impact of unused commitments?
- How confident are usage predictions?

### Coverage Targets

| Workload Type | Recommended Coverage | Discount Type |
|--------------|---------------------|---------------|
| Stable production (24/7) | 70-80% with commitments | RIs or Savings Plans |
| Variable production | Baseline with commitments | Compute Savings Plans |
| Development/testing | On-demand or scheduling | Scheduling + spot |
| Experimental | On-demand | No commitments |

### Monitoring Commitment Utilization
- Track RI/SP utilization rates
- Alert on underutilized commitments
- Review coverage quarterly
- Adjust strategy based on utilization data

**[📖 FinOps Landscape](https://www.finops.org/landscape/)** - Tools for commitment management

## Key Exam Tips for This Domain

1. **Know the difference between rate and usage optimization** - Rate is about discounts, usage is about efficiency
2. **Understand all commitment types** - RIs, Savings Plans, CUDs across all providers
3. **Spot is for fault-tolerant workloads only** - Never recommend spot for databases or stateful apps
4. **Savings Plans are more flexible than RIs** - Compute Savings Plans are the most flexible
5. **Coverage should match risk tolerance** - Do not commit 100% of variable workloads
6. **Payment options affect discount level** - All Upfront gives highest discount
7. **1-year vs 3-year tradeoff** - 3-year gives more savings but more risk
8. **Monitor utilization** - Unused commitments are wasted money

## Key terms

- **Reserved Instance (RI)** - a commitment to a specific instance configuration for one or three years in return for a discounted rate.
- **Savings Plan** - an AWS commitment to a consistent hourly spend for one or three years in return for a discounted rate.
- **Compute Savings Plan** - the most flexible AWS Savings Plan, which applies across instance families, Regions and compute services.
- **Spot instance** - spare cloud capacity sold at a deep discount that the provider can reclaim at short notice.
