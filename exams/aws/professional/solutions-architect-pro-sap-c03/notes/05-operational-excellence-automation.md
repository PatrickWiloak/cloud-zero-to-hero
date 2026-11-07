---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 35 min
---

# Domain 5: Operational Excellence and Automation (20%)

## Overview

Domain 5 is new as a domain (20 percent) and collects what C02 scattered across its domains: infrastructure as code, CI/CD, observability and operational automation. Four tasks: **5.1** infrastructure as code, **5.2** CI/CD and DevSecOps pipelines, **5.3** observability and monitoring, **5.4** operational automation and resilient systems. Application code development and debugging are out of scope for the exam.

**[📖 Exam guide: Content Domain 5](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/solutions-architect-professional-03-domain5.html)** - Official tasks and skills

## Task 5.1: Infrastructure as code

- **Declarative versus imperative** (5.1.1): CloudFormation templates are **declarative** (describe the end state, the service works out the changes). The AWS **CDK** is **imperative in authoring** (you write code in a general-purpose language) but synthesizes CloudFormation templates, so you get loops, functions and reuse with CloudFormation's deployment engine. CDK is newly named in the scope list.
- **Policy as code** (5.1.2): enforce standards before and after deployment. **CloudFormation Hooks** run checks before resources are created or updated and can fail the operation; **CDK aspects** visit every construct in an app to validate or modify it; AWS Config rules detect and remediate drift after the fact; SCPs set hard organizational limits.
- **Secrets in IaC** (5.1.3): never put secrets in templates or state. Reference **Secrets Manager** or **Systems Manager Parameter Store** using dynamic references, so the value is resolved at deploy time.

```yaml
Resources:
  Database:
    Type: AWS::RDS::DBInstance
    Properties:
      MasterUsername: appadmin
      MasterUserPassword: '{{resolve:secretsmanager:prod/app/db:SecretString:password}}'
```

- **Multi-account, multi-Region deployment** (5.1.4): **CloudFormation StackSets** deploy one template to many accounts and Regions, with service-managed permissions integrated with Organizations (new accounts in a target OU receive stacks automatically).

**[📖 CloudFormation StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)** - Deploying across accounts and Regions
**[📖 CloudFormation Hooks](https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/what-is-cloudformation-hooks.html)** - Proactive control checks

## Task 5.2: CI/CD and DevSecOps pipelines

- **Pipelines** (5.2.1): **CodePipeline** orchestrates, **CodeBuild** builds and tests, **CodeDeploy** deploys, and a repository (CodeCommit or an external Git provider) holds source.
- **Security scanning and signing** (5.2.2, new): scan dependencies and images in the pipeline (**Amazon Inspector**, **ECR image scanning**) and fail the build on severe findings; sign artifacts so deploy stages accept only trusted builds. This is the "shift security left" principle.
- **Multi-account, multi-Region pipelines** (5.2.3, new): a central pipeline account deploys into workload accounts by assuming a **deployment role** in each (role delegation), and **promotes the same artifact** through dev, test and prod, rather than rebuilding it per environment. CodePipeline supports cross-account deployment actions with artifacts stored in an encrypted S3 bucket whose key policy allows the target accounts.
- **Evaluating AI applications** (5.2.4, new): validate model outputs with **Amazon Bedrock Evaluations** as a pipeline gate before releasing a prompt, model or agent change.
- **Deployment strategies with rollback** (5.2.5): blue/green, canary, rolling. Each needs a defined rollback trigger (failed health check, CloudWatch alarm).

## Task 5.3: Observability and monitoring

- **Standardized instrumentation** (5.3.1): metrics, logs and traces through CloudWatch, **AWS X-Ray** and the **AWS Distro for OpenTelemetry (ADOT)**, a vendor-neutral way to instrument applications once and send telemetry to several backends.
- **Containers** (5.3.2, new): **CloudWatch Container Insights** for ECS and EKS metrics and logs.
- **Multi-account log aggregation** (5.3.3): CloudWatch Logs **subscription filters** stream log events to a destination in a central account (Kinesis Data Streams/Firehose or Lambda), with long-term archival in S3 tiers.
- **Alerting** (5.3.4): CloudWatch alarms (including composite alarms to reduce noise) notify through SNS; Systems Manager can act on alarms.
- **AI/ML workloads** (5.3.5, new): monitor model performance, agent performance, inference latency and **model drift** (the gradual loss of accuracy as real-world data diverges from the training data).
- **User experience** (5.3.6, new): **CloudWatch Synthetics** canaries run scripted checks against endpoints on a schedule (synthetic monitoring); **CloudWatch RUM** (real user monitoring) collects performance data from real browsers.
- **SLOs** (5.3.7): define a service level indicator (for example the share of requests under 300 ms), set an objective (99.9 percent), and alert on **error budget** burn. **CloudWatch Application Signals** supports SLOs for applications.

## Task 5.4: Operational automation and resilient systems

- **Health, capacity and response** (5.4.1): alarms and EventBridge rules trigger automation through Systems Manager; **Service Quotas** monitoring prevents hitting limits unexpectedly.
- **Controlled remediation** (5.4.2, new): automation that fixes problems must not make them worse. Apply safety constraints: **circuit breakers** (stop calling a failing dependency), **rate limits**, **bulkheads** (isolate resources so one failure cannot consume everything) and **retries with exponential backoff and jitter**.
- **Auto scaling** (5.4.3): target tracking (keep a metric near a value), step, scheduled, and **predictive scaling** for Auto Scaling groups with recurring load patterns.
- **Automated failure recovery** (5.4.4): Auto Scaling health checks replace unhealthy instances, ECS replaces failed tasks, Lambda retries asynchronous invocations.
- **Runbooks and incident response** (5.4.5, new): Systems Manager Automation runbooks perform routine operations (patching, remediation, scaling) as reviewed, repeatable, auditable procedures, with approvals for high-risk steps.

```bash
aws ssm start-automation-execution \
  --document-name AWS-RestartEC2Instance \
  --parameters "InstanceId=i-0123456789abcdef0"
```

**[📖 AWS Systems Manager Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html)** - Runbooks for operational tasks
**[📖 Amazon CloudWatch Synthetics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html)** - Canaries for synthetic monitoring

## What changed from C02 in this domain

- **New as a domain:** C02 had no operational excellence domain. IaC (C02 1.4, 2.1, 3.2), CI/CD (2.1), observability (1.4, 3.1, 3.3) and scaling (2.4, 3.1) were consolidated here.
- **New skills:** security scanning and artifact signing, multi-account pipelines, Bedrock Evaluations, Container Insights, AI/ML monitoring, synthetic and real user monitoring, controlled remediation, automated runbooks.
- **Services added to scope:** AWS CDK, AWS CodeCommit, AWS Distro for OpenTelemetry, AWS Application Auto Scaling.

## Key terms

- **AWS CDK** - a framework for defining cloud infrastructure in general-purpose programming languages that synthesizes CloudFormation templates.
- **CloudFormation Hooks** - checks that run before resources are provisioned and can block non-compliant changes.
- **CDK aspects** - code that visits every construct in a CDK app to validate or modify it.
- **Dynamic reference** - a CloudFormation syntax that resolves a secret or parameter value at deployment time.
- **CloudFormation StackSets** - a feature that deploys stacks across multiple accounts and Regions from one template.
- **Artifact promotion** - moving the same built artifact through successive environments instead of rebuilding it.
- **Amazon Bedrock Evaluations** - tooling for assessing the quality of model and application outputs.
- **AWS Distro for OpenTelemetry** - an AWS-supported distribution of OpenTelemetry for collecting traces and metrics.
- **Container Insights** - a CloudWatch feature that collects metrics and logs from containerized applications.
- **Subscription filter** - a CloudWatch Logs feature that streams matching log events to another destination.
- **Model drift** - degradation in model performance as real-world data changes from the data the model was built on.
- **CloudWatch Synthetics** - scripted canaries that test endpoints on a schedule.
- **CloudWatch RUM** - real user monitoring that collects performance data from actual user sessions.
- **Error budget** - the amount of unreliability allowed by a service level objective.
- **Circuit breaker** - a pattern that stops calls to a failing dependency to prevent cascading failure.
- **Bulkhead** - a pattern that isolates resources so a failure in one part cannot exhaust the whole system.
- **Predictive scaling** - Auto Scaling that forecasts load from history and scales ahead of demand.
- **Systems Manager Automation** - a capability that runs documented runbooks to perform operational tasks.
