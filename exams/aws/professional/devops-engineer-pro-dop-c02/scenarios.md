---
last-updated: 2026-05-03
---

# AWS DevOps Engineer Pro (DOP-C02) - Exam Scenarios

> Eight worked scenarios mirroring DOP-C02 question style. Illustrative, not real exam questions. DOP-C02 leans practical: pipelines, deployments, observability, automated remediation. Questions are shorter than SAP-C02 but pack three or four constraints; missing one means the wrong answer.

## How to use this

Read scenario, attempt your answer, then read the analysis. Note the *deciding constraint* in each - that's how you'll spot the same pattern on exam day.

---

## Scenario 1 - Blue/green deployment for ECS Fargate (Domain 1: 22%)

A team running an API on ECS Fargate behind an Application Load Balancer needs zero-downtime deploys with automatic rollback if the new revision's HTTP 5xx rate exceeds 1% in the first 5 minutes.

Which approach fits with the least custom code?

A. CodeDeploy blue/green for ECS with a CloudWatch alarm on ALB target group 5xx, configured as the rollback alarm.
B. ECS rolling update with min healthy 100% / max 200%; custom Lambda watching CloudWatch metrics and calling UpdateService to roll back.
C. CodeDeploy in-place deployment to ECS; Lambda hook in beforeAllowTraffic for validation.
D. Spin up a parallel ECS service, gradually shift Route 53 weighted records.

**Analysis**

A is right: CodeDeploy has native blue/green for ECS Fargate via the AWS::CodeDeploy::DeploymentGroup with `DeploymentStyle: BLUE_GREEN`, and you can attach an alarm-based automatic rollback config. The TestTraffic / ProdTraffic listeners are managed automatically. B requires custom Lambda. C: in-place rolling is *not* blue/green and doesn't give you instant rollback. D works but moves the rollback contract to DNS TTLs - bad fit for "5xx in 5 minutes."

**Answer:** A

**Key takeaway:** Blue/green for ECS = CodeDeploy with deployment group + CloudWatch alarms = rollback. The exam wants the managed pattern, not custom Lambda glue.

---

## Scenario 2 - Patch management at scale (Domain 6: 17%)

A company has 2,000 EC2 instances across multiple accounts, mixed Linux and Windows, that need monthly OS patches with audit evidence (which patches went on which instance, when). Some instances are in private subnets without internet egress.

Which approach is correct?

A. Systems Manager Patch Manager with a Maintenance Window per OS group; VPC endpoints for SSM, EC2messages, SSM messages so private instances reach SSM without internet.
B. Manual SSH/RDP and run yum update / Windows Update; track in a spreadsheet.
C. AWS OpsWorks for Chef Automate (a retired service); configure scheduled recipes for patching.
D. Third-party patch tool installed via UserData; aggregate logs in CloudWatch Logs.

**Analysis**

A is right: SSM Patch Manager + Maintenance Windows is the AWS-native answer. The three VPC endpoints (ssm, ec2messages, ssmmessages) are the fix for private-subnet SSM agent connectivity without NAT. SSM produces compliance reports per instance for audit. B isn't auditable at scale. C is being deprecated and isn't the right fit anyway. D loses the AWS-native compliance reporting.

**Answer:** A

**Key takeaway:** Patch + audit at scale = SSM Patch Manager. The three endpoints (SSM, EC2messages, SSMmessages) are heavily tested for private-subnet SSM connectivity.

---

## Scenario 3 - Pipeline cross-account deployment (Domain 1: 22%)

A team has a CodePipeline in a tools account that needs to deploy CloudFormation stacks into separate dev / staging / prod accounts. The pipeline must use least privilege and avoid hard-coded credentials.

Which mechanism fits?

A. Cross-account IAM roles in each target account that the pipeline's CodePipeline service role assumes; CodePipeline action with the Role ARN; CodeBuild and CodeDeploy use the same pattern.
B. Long-lived IAM access keys for each target account stored in Secrets Manager; pipeline retrieves and uses them.
C. STS GetSessionToken with MFA; encode tokens into pipeline variables.
D. AWS Organizations SCP grants on a single shared role.

**Analysis**

A is right: cross-account roles + sts:AssumeRole is the AWS-native, least-privilege, no-secret pattern. CodePipeline's action config explicitly accepts a role ARN to assume in the target account. B is the wrong answer to nearly any AWS question (long-lived keys). C is interactive auth. D doesn't grant cross-account permissions; SCPs limit, they don't grant.

**Answer:** A

**Key takeaway:** Cross-account in AWS = AssumeRole. Anytime you see "deploy to multiple accounts," the answer involves IAM roles trusted by the pipeline's service role.

---

## Scenario 4 - Centralized observability across accounts (Domain 4: 15%)

A platform team needs metrics and logs from 50 application accounts visible in one observability account, with alarms in the central account, no agent reconfiguration per account.

Which approach fits?

A. CloudWatch cross-account observability: enable in each application account as source, central account as monitoring account; set up sink + link.
B. Each account ships logs to S3 in the observability account via cross-account bucket policies; rebuild metrics from logs in the central account.
C. Run a custom Fluentd cluster in the observability account, scrape each account via Lambda.
D. Each app account has its own dashboards; the observability account has a runbook listing them.

**Analysis**

A is right: CloudWatch cross-account observability is exactly this pattern (sink in monitoring account, link in source accounts; works across the org). Logs, metrics, and traces all show up in the central account. B loses real-time alerting and requires re-deriving metrics. C is operational burden you don't need. D isn't observability, it's documentation.

**Answer:** A

**Key takeaway:** "Centralized monitoring across many accounts" = CloudWatch cross-account observability (the sink + link feature, GA since 2022). Don't roll your own.

---

## Scenario 5 - Incident response automation (Domain 5: 14%)

A SOC needs automatic response to specific GuardDuty findings: for unauthorized API calls finding type, isolate the EC2 instance (replace its security groups with a deny-all SG), snapshot its EBS volumes for forensics, and create a JIRA ticket.

Which approach fits with least custom code?

A. EventBridge rule on GuardDuty findings → Step Functions state machine that calls EC2 ModifyInstanceAttribute, EBS CreateSnapshot, and a JIRA Lambda integration.
B. GuardDuty findings → SNS → email alert to the SOC who manually responds.
C. Single Lambda subscribed to GuardDuty findings via EventBridge that runs all three actions sequentially.
D. AWS Systems Manager Incident Manager runbook triggered on EventBridge.

**Analysis**

A is right *and* D is also reasonable. The most defensible answer is **D** in modern AWS: Incident Manager is purpose-built for this with native runbooks, ChatOps, paging, and post-incident review. If D isn't an option, A is correct (Step Functions for orchestration with retries and error handling beats one-big-Lambda). B is the manual answer (always wrong). C works but loses retry / error-handling visibility.

**Answer:** D (or A if Incident Manager isn't an option)

**Key takeaway:** Modern incident response on AWS = Systems Manager Incident Manager. Step Functions is the second-best for custom orchestrated runbooks. One-big-Lambda is the third-best.

---

## Scenario 6 - Resilient deployment with canary (Domain 3: 15%)

A consumer app on Lambda needs a deploy strategy where 10% of traffic goes to the new version for 10 minutes, then if no errors, automatically promotes to 100%. Errors should auto-rollback.

Which fits?

A. CodeDeploy Lambda canary deployment (Canary10Percent10Minutes preset) with a CloudWatch alarm on Lambda errors as rollback alarm.
B. Lambda function alias with manual weighted routing updated by CloudWatch alarm action.
C. Two parallel Lambda functions behind API Gateway with stage variables; manually shift traffic.
D. SAM template with AutoPublishAlias and DeploymentPreference; CodeDeploy handles the rest.

**Analysis**

D is right (and A under the hood is what D uses, but D is the cleanest answer). SAM's DeploymentPreference: Canary10Percent10Minutes is exactly the pattern; it generates the CodeDeploy resources for you. A is correct if you're hand-rolling CloudFormation. B is manual and slow. C is duplicative.

**Answer:** D

**Key takeaway:** Lambda canary = SAM DeploymentPreference + AutoPublishAlias, or CodeDeploy directly. The named presets (Canary10Percent10Minutes, Linear10Percent5Minutes, AllAtOnce) are testable.

---

## Scenario 7 - Multi-region drift detection (Domain 2: 17%)

A platform team has CloudFormation StackSets deployed across 5 regions and 30 accounts. They need automated detection if any deployed resource has drifted from the template, with alerts to the platform team.

Which approach fits?

A. Schedule daily DetectStackSetDrift via EventBridge → Lambda → SNS to the platform team if drift > 0.
B. Manually run DetectStackDrift in each account periodically.
C. AWS Config managed rules; one rule per service.
D. Third-party tool (Terraform Cloud, etc.) for drift detection.

**Analysis**

A is right: native CloudFormation supports StackSet-level drift detection; an EventBridge schedule + Lambda is the operational glue. The result is per-stack-instance drift status. B doesn't scale. C is per-resource compliance, not per-stack drift. D introduces new tooling for an AWS-native problem.

**Answer:** A

**Key takeaway:** CloudFormation drift detection is a real feature; for StackSets you have stack-set-level drift detection that operates on every instance. EventBridge scheduling + Lambda is the standard automation pattern.

---

## Scenario 8 - Secret rotation across services (Domain 6: 17%)

An application uses RDS, a third-party API key, and a JWT signing secret. The team wants automated rotation for all three with no app downtime, audit trail, and least operational overhead.

Which approach fits?

A. Secrets Manager: native rotation for RDS using the AWS-provided rotation Lambda; custom rotation Lambda for the API key; KMS-managed key for JWT signing rotated via KMS key rotation.
B. SSM Parameter Store SecureString for all three; Lambda updates them weekly.
C. Encrypt secrets in S3 with KMS; rotate by re-uploading.
D. Hard-code, redeploy when changed.

**Analysis**

A is right: Secrets Manager has native rotation for RDS (and several other AWS services) and supports custom rotation Lambdas for arbitrary secrets. KMS key rotation is the right pattern for signing keys (annual auto-rotation + the key being managed at the KMS layer). B works for static secrets but lacks rotation primitives. C / D are not serious answers.

**Answer:** A

**Key takeaway:** Secret rotation hierarchy: Secrets Manager native rotation (RDS, Redshift, DocumentDB) > Secrets Manager custom Lambda rotation > KMS key rotation for signing keys. Parameter Store is for plain config, not rotating secrets.
