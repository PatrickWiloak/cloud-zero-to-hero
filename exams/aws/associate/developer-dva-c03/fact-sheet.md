---
last-updated: 2026-11-07
exam-version: DVA-C03
---

# AWS Certified Developer - Associate (DVA-C03) Fact Sheet

> **Timeline (from AWS):** registration for DVA-C03 opened 2026-10-27; last day to sit DVA-C02 is 2026-11-30; DVA-C03 is in use from 2026-12-01.

## Quick Reference

**Exam Code:** DVA-C03
**Duration:** 130 minutes
**Questions:** 65 questions, 50 scored and 15 unscored (multiple choice and multiple response)
**Passing Score:** 720 on a scaled score of 100-1,000
**Cost:** 150 USD
**Validity:** 3 years; recertify by passing the latest exam or earning DevOps Engineer - Professional ([AWS certification page](https://aws.amazon.com/certification/certified-developer-associate/))
**Delivery:** Pearson VUE testing center or online proctored exam
**Languages:** English, Japanese, Korean, Portuguese (Brazil), Simplified Chinese, Spanish (Latin America)

## Exam Domains

| Domain | Weight | Tasks |
|--------|--------|-------|
| 1. Development with AWS Services | 30% | 1.1 code for hosted applications; 1.2 Lambda; 1.3 data stores |
| 2. Security | 26% | 2.1 authn/authz; 2.2 encryption and sensitive data; 2.3 AI security (new) |
| 3. Testing and Deployment | 22% | 3.1 artifacts; 3.2 testing; 3.3 CI/CD |
| 4. Troubleshooting and Optimization | 22% | 4.1 root cause; 4.2 observability; 4.3 optimization |

## In-scope services (from the exam guide)

- **Analytics:** Athena, Data Firehose, Kinesis, OpenSearch Service
- **Application integration:** EventBridge, SNS, SQS, Step Functions
- **Compute and containers:** EC2, Elastic Beanstalk, Lambda; ECR, ECS, EKS
- **Database:** Aurora, DynamoDB, ElastiCache, RDS
- **Developer tools:** Amplify, CloudShell, CodeArtifact, CodeBuild, CodeDeploy, CodePipeline, X-Ray
- **ML and AI:** Bedrock, Bedrock AgentCore, Amazon Quick, Kiro
- **Management and governance:** AppConfig, CDK, CloudFormation, CloudTrail, CloudWatch, CloudWatch Logs, CLI, SAM, Systems Manager
- **Networking:** API Gateway, CloudFront, ELB, PrivateLink, Route 53, VPC
- **Security:** ACM, Cognito, IAM, KMS, Private CA, Secrets Manager, STS, WAF
- **Storage:** EBS, EFS, S3, S3 Glacier

**Out of scope** includes SageMaker AI, Strands Agents, Rekognition, Polly, Connect, Shield, Storage Gateway, Snow Family, Transfer Family and QuickSight.

**[📖 DVA-C03 in-scope services](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/dva-03-in-scope-services.html)** and **[📖 out-of-scope services](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/dva-03-out-of-scope-services.html)** - Source lists

## High-yield comparisons

| Pair | Difference |
|------|------------|
| SQS vs SNS vs EventBridge | Queue (pull, buffer) vs pub/sub fan-out vs rules-based event router |
| Cognito user pool vs identity pool | Authenticates users and issues tokens vs exchanges tokens for AWS credentials |
| Secrets Manager vs Parameter Store | Built-in rotation, per-secret cost vs hierarchical config, free standard tier, no built-in rotation |
| Reserved vs provisioned concurrency | Guarantee and cap vs pre-initialized environments |
| GSI vs LSI | Any key pair, add any time vs same partition key, create with table |
| Query vs Scan | Efficient by key vs whole-table read |
| Lambda destination vs DLQ | Success and failure targets for async invocation vs failure-only queue/topic |
| Canary vs linear vs all-at-once | Small slice first vs equal increments vs immediate |
| Presigned URL vs CloudFront signed URL | S3 object access by creator's permissions vs CloudFront content access |
