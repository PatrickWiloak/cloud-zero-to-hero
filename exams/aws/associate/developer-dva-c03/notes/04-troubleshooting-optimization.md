---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 25 min
---

# Domain 4: Troubleshooting and Optimization (22%)

## Overview

This domain rose from 18 percent to **22 percent** in C03. Tasks: **4.1** assist in root cause analysis, **4.2** apply logging, monitoring and observability best practices, **4.3** optimize applications. C03 merged three observability skills and three optimization skills, moved Lambda performance tuning in from Domain 1, and added AI tools for error analysis (4.1.5) and optimization (4.3.6).

**[📖 Exam guide: Content Domain 4](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/developer-associate-03-domain4.html)** - The official skills list

## Task 4.1: Root cause analysis

The method: reproduce or locate the failure, read the **logs, metrics and traces** for the failing request, form a hypothesis, change one thing, and verify.

- **Logs.** Lambda and many services write to **Amazon CloudWatch Logs**, grouped in log groups and streams. **CloudWatch Logs Insights** queries them (skill 4.1.3):

```text
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 50
```

- **Metrics.** CloudWatch metrics show shape: error counts, duration, throttles, queue depth. A rising `Throttles` count on Lambda means concurrency limits; rising `ApproximateAgeOfOldestMessage` on SQS means consumers are not keeping up; DynamoDB `ThrottledRequests` or `ProvisionedThroughputExceededException` means a hot key or too little capacity.
- **Traces.** **AWS X-Ray** follows one request across services and shows which segment was slow or failing (skill 4.1.2).
- **Deployment failures** (4.1.4): read the output logs: CloudFormation stack events (the first `CREATE_FAILED` event states the cause), CodeBuild build logs, CodeDeploy lifecycle event logs and ECS service events.
- **Code and integration defects** (4.1.1): typical causes are a missing IAM permission (`AccessDeniedException`, so check the role, not the code), a function outside a VPC trying to reach a private resource, a timeout shorter than the downstream call, or a payload shape the code did not expect.
- **AI tools** (4.1.5, new): use AWS AI tools to analyze errors and propose fixes. They accelerate diagnosis; confirm any suggestion against logs and documentation before applying it.

## Task 4.2: Logging, monitoring and observability

**Structured logging** (4.2.1) writes each event as JSON with consistent fields (request id, user id, operation, outcome) so Logs Insights can filter and aggregate them. Log what is needed to reconstruct behavior; never log secrets or personal data.

**Custom metrics** (4.2.2). Code can publish metrics with `PutMetricData`, or write log lines in the **embedded metric format (EMF)** and let CloudWatch extract the metric.

```bash
aws cloudwatch put-metric-data --namespace MyApp --metric-name OrdersPlaced --value 1 --unit Count
```

**Alerts** (4.2.3). A CloudWatch **alarm** watches a metric against a threshold and notifies an SNS topic (or triggers an action); EventBridge rules can notify on events such as a deployment completing or a service quota nearing its limit.

**Tracing** (4.2.4). Enable X-Ray for the service (for Lambda, active tracing) and instrument SDK calls so downstream calls appear as subsegments. **Annotations** are indexed key-value pairs you can search; **metadata** is not indexed.

**Health** (4.2.5). Application health checks tell a load balancer or orchestrator whether to send traffic. In containers, a **liveness probe** answers "should this container be restarted?" and a **readiness probe** answers "should it receive traffic yet?". Load balancer target group health checks and ECS container health checks do similar work.

**[📖 CloudWatch Logs Insights query syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)** - fields, filter, stats, sort
**[📖 What is AWS X-Ray?](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)** - Traces, segments and the service map

## Task 4.3: Optimization

- **Concurrency** (4.3.1). Lambda scales out by running more concurrent environments. **Reserved concurrency** caps and guarantees a function's share of the account limit. **Provisioned concurrency** keeps initialized environments ready to remove cold-start latency at a cost. For EC2, **Auto Scaling groups** add and remove instances on metrics. In code, size thread pools and use **connection pooling** so a burst of work does not exhaust a database's connections (for relational databases from Lambda, a proxy such as RDS Proxy pools connections).
- **Memory and compute** (4.3.2). In Lambda, memory sets both memory and proportional CPU, and more memory can shorten duration enough to lower cost; measure with a tool such as AWS Lambda Power Tuning or CloudWatch duration and memory-used data. For Lambda tuning also reuse SDK clients and connections across invocations by creating them outside the handler.
- **Messaging** (4.3.3). Batch SQS reads and writes, use long polling, set the visibility timeout above the function timeout, and use SNS fan-out to deliver one event to many subscribers.
- **Caching** (4.3.4). ElastiCache (Redis or Memcached) for general caching, DynamoDB Accelerator (DAX) for DynamoDB read caching with microsecond reads, CloudFront for caching content at the edge.
- **Bottlenecks** (4.3.5). Use CloudWatch metrics and dashboards to find the saturated resource, then X-Ray to find the slow call.
- **AI tools** (4.3.6, new). Use AWS AI tools to identify optimization opportunities such as bottlenecks, resource usage and code efficiency, then validate the suggestion with measurements.

**[📖 Lambda provisioned concurrency](https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html)** - Pre-initialized execution environments
**[📖 Amazon DynamoDB Accelerator (DAX)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html)** - In-memory caching for DynamoDB

## What changed from C02 in this domain

- **Added:** AI tools for error analysis (4.1.5) and optimization (4.3.6).
- **Merged:** eight observability skills became five; nine optimization skills became six.
- **Moved in:** Lambda performance tuning (from C02 Domain 1).
- **Weight:** 18 percent to 22 percent.

## Key terms

- **CloudWatch Logs Insights** - a query language and tool for searching and aggregating CloudWatch log data.
- **AWS X-Ray** - a service that traces requests across components and shows where time is spent and errors occur.
- **Embedded metric format** - a log format that lets CloudWatch extract custom metrics from structured log lines.
- **CloudWatch alarm** - a rule that evaluates a metric against a threshold and triggers a notification or action.
- **Structured logging** - writing log entries in a consistent machine-readable format such as JSON.
- **Liveness probe** - a check that decides whether a container should be restarted.
- **Readiness probe** - a check that decides whether a container is ready to receive traffic.
- **Reserved concurrency** - a Lambda setting that guarantees and caps the concurrency available to a function.
- **Provisioned concurrency** - a Lambda setting that keeps execution environments initialized to avoid cold starts.
- **Connection pooling** - reusing a set of database connections across requests instead of opening one per request.
- **DynamoDB Accelerator** - an in-memory cache for DynamoDB that serves reads in microseconds.
- **Cold start** - the extra latency when Lambda must create and initialize a new execution environment.
