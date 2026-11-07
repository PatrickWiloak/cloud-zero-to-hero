# SRE and Monitoring - GCP Professional Cloud DevOps Engineer

## Overview

Site Reliability Engineering practices, monitoring strategies, SLI/SLO/SLA implementation, incident management, and operational excellence.

## SRE Fundamentals

### Service Level Indicators (SLIs)
**Common SLIs**:
- **Availability**: Successful requests / Total requests
- **Latency**: Request completion time (P50, P95, P99)
- **Throughput**: Requests per second
- **Error Rate**: Failed requests / Total requests
- **Durability**: Data retention success rate

**Example Calculation**:
```sql
# BigQuery query for availability SLI
SELECT
  SUM(IF(status_code < 500, 1, 0)) / COUNT(*) * 100 AS availability_percent
FROM
  `project.dataset.request_logs`
WHERE
  timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY);
```

### Service Level Objectives (SLOs)
**Setting SLOs**:
- **Target**: 99.9% availability over 30 days
- **Error Budget**: 0.1% = ~43 minutes downtime per month
- **Measurement Window**: Rolling 30 days
- **Consequences**: Freeze deployments if budget exhausted

**Example SLO Document**:
```yaml
service: my-api
slis:
  - name: availability
    description: Percentage of successful requests
    implementation: COUNT(status < 500) / COUNT(*)
    target: 99.9
    window: 30d
  - name: latency
    description: P95 request latency
    implementation: PERCENTILE_CONT(latency, 0.95)
    target: 200ms
    window: 7d
```

### Error Budgets
**Purpose**:
- Balance reliability and feature velocity
- Quantify acceptable risk
- Guide deployment decisions
- Align engineering priorities

**Error Budget Policy**:
```
If error budget > 0:
  - Continue with planned deployments
  - Focus on features and velocity

If error budget <= 0:
  - Halt feature deployments
  - Focus on reliability improvements
  - Root cause analysis required
  - Postmortem for incidents
```

## Monitoring Strategy

### Golden Signals
1. **Latency**: Time to serve requests
2. **Traffic**: Demand on the system
3. **Errors**: Rate of failed requests
4. **Saturation**: Resource utilization

**Implementation**:
```python
from google.cloud import monitoring_v3
from google.api_core import retry

def record_request(duration, status_code, resource_utilization):
    client = monitoring_v3.MetricServiceClient()

    # Latency metric
    series = create_time_series(
        "custom.googleapis.com/request_latency",
        duration
    )
    client.create_time_series(name=project_name, time_series=[series])

    # Error rate
    if status_code >= 500:
        series = create_time_series(
            "custom.googleapis.com/errors",
            1
        )
        client.create_time_series(name=project_name, time_series=[series])
```

### Alerting Policies
**Best Practices**:
- Alert on SLO burn rate, not just thresholds
- Use appropriate time windows
- Reduce alert fatigue
- Prioritize actionable alerts
- Document response procedures

**Alert Example**:
```yaml
displayName: "High Error Rate - SLO Risk"
conditions:
  - displayName: "Error rate > 1%"
    conditionThreshold:
      filter: 'metric.type="custom.googleapis.com/error_rate"'
      comparison: COMPARISON_GT
      thresholdValue: 0.01
      duration: 300s
      aggregations:
        - alignmentPeriod: 60s
          perSeriesAligner: ALIGN_RATE
notificationChannels:
  - projects/PROJECT/notificationChannels/CHANNEL_ID
documentation:
  content: |
    Error rate exceeds SLO threshold.
    Runbook: https://wiki.example.com/runbooks/high-error-rate
```

## Incident Management

### Incident Response Process
1. **Detection**: Automated monitoring/alerting
2. **Triage**: Assess severity and impact
3. **Mitigation**: Restore service quickly
4. **Resolution**: Fix root cause
5. **Postmortem**: Learn and improve

### On-Call Management
**Best Practices**:
- Rotation schedule (weekly/bi-weekly)
- Clear escalation path
- Runbooks for common issues
- Incident severity levels
- Response time expectations
- Handoff procedures

**Runbook Template**:
```markdown
# Service X High Latency Runbook

## Symptoms
- P95 latency > 500ms
- User complaints about slow response

## Investigation Steps
1. Check Cloud Monitoring dashboard: [link]
2. Review recent deployments in last 2 hours
3. Check database query performance
4. Verify cache hit rate in Memorystore

## Common Causes
- Database slow queries
- Cache invalidation issues
- Downstream service degradation
- Resource saturation

## Mitigation
- Scale up application instances
- Restart cache if hit rate < 70%
- Roll back recent deployment if correlated

## Escalation
If not resolved in 30 minutes, escalate to:
- Primary: @senior-engineer
- Secondary: @engineering-manager
```

### Postmortem Process
**Blameless Postmortem**:
```markdown
# Postmortem: Service Outage YYYY-MM-DD

## Impact
- Duration: 2 hours 15 minutes
- Affected users: ~5% of traffic
- Error rate: 15% of requests failed
- Revenue impact: $X estimated

## Root Cause
Database connection pool exhausted due to...

## Timeline
- 14:00: Deployment completed
- 14:15: First alerts for increased latency
- 14:30: Incident declared, on-call paged
- 15:45: Root cause identified
- 16:15: Service restored

## What Went Well
- Quick incident detection
- Effective communication
- Rollback procedure worked

## What Went Wrong
- Monitoring didn't catch issue earlier
- Insufficient load testing
- Unclear runbook steps

## Action Items
1. [ ] Add connection pool monitoring (Owner: @eng1, Due: YYYY-MM-DD)
2. [ ] Implement load testing in CI/CD (Owner: @eng2, Due: YYYY-MM-DD)
3. [ ] Update runbook with detailed steps (Owner: @eng3, Due: YYYY-MM-DD)
```

## Toil Reduction

**Toil Definition**:
- Manual, repetitive, automatable work
- No enduring value
- Grows linearly with service growth

**Automation Opportunities**:
- Deployment automation
- Alert response scripts
- Infrastructure provisioning
- Capacity management
- Backup and recovery
- Certificate renewal
- Log analysis and aggregation

**Example Automation**:
```python
# Auto-scaling based on SLO burn rate
def auto_scale_on_slo_burn():
    current_error_rate = get_error_rate()
    target_error_rate = 0.001  # 99.9% SLO

    if current_error_rate > target_error_rate * 2:
        # SLO burning too fast, scale up
        scale_service(replica_count + 2)
        send_alert("Auto-scaled due to SLO burn")
```

## Capacity Planning

**Metrics to Track**:
- CPU utilization trends
- Memory usage patterns
- Disk I/O and storage
- Network bandwidth
- Request volume growth
- Database connections

**Forecasting**:
```python
# Simple linear regression for capacity planning
from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_capacity(historical_usage, days_ahead=90):
    X = np.array(range(len(historical_usage))).reshape(-1, 1)
    y = np.array(historical_usage)

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.array(range(len(historical_usage),
                               len(historical_usage) + days_ahead)).reshape(-1, 1)
    forecast = model.predict(future_X)

    return forecast
```

## Best Practices

### SRE Principles
1. **Embrace Risk**: Perfect reliability isn't goal
2. **Error Budgets**: Quantify acceptable failure
3. **Automation**: Eliminate toil systematically
4. **Simplicity**: Minimize complexity
5. **Monitoring**: Measure what matters
6. **Release Engineering**: Automate deployments
7. **Capacity Planning**: Stay ahead of growth

### Monitoring
1. Use SLIs to measure user experience
2. Set realistic SLOs based on business needs
3. Monitor error budget consumption
4. Alert on symptoms, not causes
5. Reduce false positives
6. Document alert responses
7. Regular dashboard reviews

### Incident Management
1. Blameless postmortems
2. Clear severity levels
3. Documented runbooks
4. Effective communication
5. Focus on mitigation first
6. Learn from every incident
7. Track action item completion

## Common Scenarios

**Scenario**: Service experiencing intermittent errors
**Solution**: Check SLO burn rate, review recent changes, check dependencies, scale if needed, investigate logs and traces

**Scenario**: Error budget exhausted
**Solution**: Halt feature deployments, prioritize reliability work, root cause analysis, implement fixes, validate before resuming features

**Scenario**: On-call engineer paged
**Solution**: Acknowledge alert, assess severity, follow runbook, mitigate impact, escalate if needed, document incident

## Study Tips

1. **Understand SLI/SLO/SLA**: Differences and implementation
2. **Error budget calculation**: How to calculate and use
3. **Monitoring best practices**: Golden signals, alerting
4. **Incident response**: Process and procedures
5. **Postmortem practices**: Blameless, action-oriented
6. **Toil reduction**: Automation opportunities
7. **Capacity planning**: Forecasting and scaling

## Additional Resources

- [Google SRE Books](https://sre.google/books/)
- [Cloud Monitoring Documentation](https://cloud.google.com/monitoring/docs)
- [SRE Workbook](https://sre.google/workbook/table-of-contents/)
- [Incident Management Guide](https://cloud.google.com/architecture/devops/devops-process-incident-management)

## Key terms

- **Service level indicator (SLI)** - a measured quantity of service behaviour, such as the share of requests that succeed.
- **Service level objective (SLO)** - a target value or range for an SLI over a period of time.
- **Error budget** - the amount of unreliability an SLO allows, calculated as 100% minus the SLO target.
- **Toil** - manual, repetitive, automatable work with no lasting value that grows with service size.
- **Blameless postmortem** - a written review of an incident that focuses on causes and fixes rather than on individuals.
- **Cloud Monitoring** - the Google Cloud service for metrics, dashboards, uptime checks and alerting policies.
- **Cloud Logging** - the Google Cloud service that stores, searches and routes log entries.
- **Cloud Trace** - the Google Cloud service that collects latency data to show how requests move through an application.
