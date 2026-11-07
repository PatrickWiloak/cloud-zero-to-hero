# Cloud Cost Data and Analytics

**[📖 FinOps Capabilities - Cost Allocation](https://www.finops.org/framework/capabilities/cost-allocation/)** - Cost allocation documentation

## Overview

This document covers cloud cost data, analytics, allocation, and reporting. Understanding how to collect, analyze, and report on cloud cost data is a core FinOps engineering skill tested on the Certified Engineer exam.

## Cost and Usage Data

### Cloud Provider Billing Data
| Provider | Billing Data Source | Format | Granularity |
|----------|-------------------|--------|-------------|
| AWS | Cost and Usage Report (CUR) | CSV/Parquet in S3 | Hourly/Daily |
| Azure | Cost Management exports | CSV in Blob Storage | Daily |
| GCP | Billing export to BigQuery | BigQuery tables | Hourly/Daily |

### AWS Cost and Usage Report (CUR)
- Most detailed billing data available from AWS
- Line-item level detail for every charge
- Includes resource IDs, tags, usage type, pricing
- Exported to S3 in CSV or Parquet format
- Can be queried with Athena, Redshift, or QuickSight
- Updated multiple times per day

**[📖 AWS CUR](https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html)** - CUR documentation

### Azure Cost Management
- Export cost data to Azure Blob Storage
- Integration with Power BI for visualization
- API access for programmatic cost retrieval
- Supports management group, subscription, and resource group scopes
- Amortized and actual cost views

**[📖 Azure Cost Management](https://learn.microsoft.com/en-us/azure/cost-management-billing/)** - Azure billing docs

### GCP Cloud Billing
- Standard export to BigQuery (daily aggregation)
- Detailed export to BigQuery (resource-level, hourly)
- Pricing export to BigQuery (list prices)
- SQL queries for custom cost analysis
- Integration with Data Studio/Looker for dashboards

**[📖 GCP Billing Export](https://cloud.google.com/billing/docs/how-to/export-data-bigquery)** - BigQuery billing export

## Cost Allocation

### Tagging Strategy
- Tags are the foundation of cost allocation
- Consistent tagging enables accurate showback/chargeback
- Minimum tags: team, environment, project, cost-center
- Enforce tagging via policies (AWS Config, Azure Policy, GCP Org Policy)

### Tagging Enforcement
```
# AWS: Tag policy via Organizations
# Azure: Azure Policy for required tags
# GCP: Organization policy constraints

# Example enforcement levels:
1. Advisory: Report untagged resources
2. Preventive: Block resource creation without required tags
3. Corrective: Auto-tag resources based on rules
```

### Shared Costs
| Cost Type | Allocation Method | Example |
|-----------|------------------|---------|
| Shared infrastructure | Proportional split | Kubernetes cluster, networking |
| Support and premium | Even split or proportional | Enterprise support plans |
| Reserved capacity | Applied to matched usage | RI/SP coverage |
| Marketplace | Direct allocation | Third-party licenses |
| Data transfer | Proportional to usage | Cross-region data movement |

### Showback vs Chargeback
| Model | Description | Accountability |
|-------|-------------|---------------|
| Showback | Report costs to teams (informational) | Low - awareness only |
| Chargeback | Bill costs to team budgets | High - financial accountability |
| Hybrid | Showback with chargeback for overages | Medium - balanced approach |

- Start with showback - build awareness before charging
- Chargeback requires mature tagging and allocation
- Shared costs are the hardest to allocate fairly

## Cost Analytics

### Cost Dimensions
| Dimension | Use Case | Example |
|-----------|----------|---------|
| Service | Which cloud services cost most | EC2, RDS, S3 |
| Account/Subscription | Cost by business unit | prod-account, dev-account |
| Region | Geographic cost distribution | us-east-1, eu-west-1 |
| Tag | Cost by team, project, environment | team:platform, env:prod |
| Resource | Individual resource cost | specific EC2 instance ID |
| Time | Cost trends and anomalies | Daily, weekly, monthly |

### Anomaly Detection
- Sudden cost spikes compared to historical baseline
- Unusual resource provisioning patterns
- Unexpected data transfer charges
- New services appearing in billing
- Cost changes not correlated with known deployments

### Cost Forecasting
| Method | Description | Accuracy |
|--------|-------------|----------|
| Linear trend | Extend current trend line | Low (does not account for events) |
| Moving average | Average of recent periods | Medium |
| Seasonal decomposition | Account for repeating patterns | Medium-High |
| ML-based | Machine learning on historical data | High (with sufficient data) |

### Key Reports
1. **Executive summary** - Total spend, month-over-month change, top services
2. **Team breakdown** - Cost per team with trend and budget comparison
3. **Waste report** - Idle resources, unused capacity, optimization opportunities
4. **Commitment utilization** - RI/SP usage rate and coverage
5. **Unit economics** - Cost per transaction, cost per customer

## Unit Economics

### Definition
Unit economics connects cloud costs to business metrics, enabling teams to understand the cost of delivering business value.

### Examples
| Business Metric | Cloud Cost Metric | Unit Cost |
|----------------|------------------|-----------|
| API requests | Compute + networking cost | Cost per 1M requests |
| Active users | Total infrastructure cost | Cost per active user |
| Data processed | Compute + storage cost | Cost per TB processed |
| Orders placed | End-to-end infra cost | Cost per order |

### Calculating Unit Costs
```
Unit Cost = Total Cloud Cost for Service / Number of Business Units

Example:
- Monthly compute cost for order processing: $15,000
- Monthly orders processed: 500,000
- Cost per order: $15,000 / 500,000 = $0.03 per order

Track over time:
- Month 1: $0.03/order
- Month 2: $0.028/order (improved efficiency)
- Month 3: $0.035/order (investigate increase)
```

### Benefits of Unit Economics
- Decouple growth from cost conversation (cost went up because orders went up)
- Enable meaningful comparisons across time periods
- Identify efficiency improvements vs simple cost increases
- Support business case for optimization investments

## FOCUS (FinOps Open Cost and Usage Specification)

### Overview
- Open standard for cloud cost and usage data
- Normalizes billing data across cloud providers
- Common schema for multi-cloud cost analysis
- Supported by FinOps Foundation and major cloud providers

**[📖 FOCUS Spec](https://focus.finops.org/)** - FOCUS specification

### Key FOCUS Columns
| Column | Description | Example |
|--------|-------------|---------|
| BillingAccountId | Billing account identifier | 123456789012 |
| BillingPeriodStart | Start of billing period | 2024-01-01 |
| ServiceName | Cloud service name | Amazon EC2, Azure VMs |
| ResourceId | Unique resource identifier | i-1234567890abcdef0 |
| UsageQuantity | Amount of usage | 730 hours |
| BilledCost | Amount billed | $52.56 |
| EffectiveCost | Cost after discounts/credits | $36.79 |
| Tags | Resource tags | {"team": "platform"} |

## Building Cost Dashboards

### Dashboard Design Principles
1. **Start with the question** - What decision does this data support?
2. **Layer detail** - Executive summary to drill-down detail
3. **Highlight anomalies** - Call attention to unexpected changes
4. **Include context** - Show budget, forecast, and historical comparison
5. **Enable action** - Link to optimization recommendations

### Dashboard Hierarchy
```
Level 1: Executive (total spend, trend, top 5 services)
  Level 2: Team/Business Unit (per-team cost, budget variance)
    Level 3: Service (per-service cost, utilization)
      Level 4: Resource (individual resource cost and metrics)
```

## Key terms

- **FOCUS** - the FinOps Open Cost and Usage Specification, a common format for cloud billing data across providers.
- **Cost allocation** - assigning cloud costs to teams, projects or products, usually by tags or account structure.
- **Unit economics** - cost measured against a business output, such as cost per customer or per transaction.
- **Cost and Usage Report (CUR)** - the detailed AWS billing data export used for cost analysis.
