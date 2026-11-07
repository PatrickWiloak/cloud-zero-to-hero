---
last-updated: 2026-11-07
exam-version: DVA-C03
difficulty: intermediate
---

# AWS Certified Developer - Associate (DVA-C03)

## Important Notice

**DVA-C03 is the current exam version from December 1, 2026.** AWS's exam guide states that registration for DVA-C03 opened October 27, 2026, that the last day to take DVA-C02 is November 30, 2026, and that DVA-C03 "is in use beginning December 1, 2026". If you are studying from the [DVA-C02 guide](../developer-dva-c02/README.md), read [what changed](#what-changed-from-dva-c02) first. This guide supersedes the C02 guide.

Sources (read 2026-11-07): **[📖 AWS Certified Developer - Associate](https://aws.amazon.com/certification/certified-developer-associate/)** - Exam details; **[📖 DVA-C03 Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/developer-associate-03.html)** - Official content outline

## Exam Overview

DVA-C03 validates the ability to develop, test, deploy and debug AWS cloud applications, now including AI-assisted development tools. The target candidate has 1 or more years of hands-on experience developing and maintaining applications on AWS, and is proficient in at least one high-level programming language.

| Item | Value | Source |
|------|-------|--------|
| **Exam code** | DVA-C03 | Exam guide |
| **Duration** | 130 minutes | AWS certification page |
| **Questions** | 65 total: 50 scored plus 15 unscored | AWS certification page (65) and exam guide (50 scored, 15 unscored) |
| **Question types** | Multiple choice and multiple response | Exam guide |
| **Scoring** | Scaled 100-1,000; minimum passing score 720; compensatory (pass the exam overall, not each section) | Exam guide |
| **Cost** | 150 USD (additional costs may apply) | AWS certification page |
| **Delivery** | Pearson VUE testing center or online proctored exam | AWS certification page |
| **Validity** | 3 years; recertify by passing the latest exam version or earning DevOps Engineer - Professional | AWS certification page |

## Exam Domains

| Domain | Weight (scored content) | C02 weight | Notes |
|--------|------------------------|------------|-------|
| 1. Development with AWS Services | 30% | 32% | [01 - Development with AWS Services](notes/01-development-with-aws-services.md) |
| 2. Security | 26% | 26% | [02 - Security](notes/02-security.md) |
| 3. Testing and Deployment | 22% | 24% ("Deployment") | [03 - Testing and Deployment](notes/03-testing-and-deployment.md) |
| 4. Troubleshooting and Optimization | 22% | 18% | [04 - Troubleshooting and Optimization](notes/04-troubleshooting-optimization.md) |

## What changed from DVA-C02

From AWS's own comparison page (**[📖 Comparison of DVA-C02 and DVA-C03](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/dva-03-comparison.html)**):

**New content**
- A whole new task, **2.3**: identify and mitigate security risks of using and integrating AI services (access, data privacy, input and output filtering, agent interactions, log protection).
- **1.1**: AI-assisted development tools (generate, review and optimize code) and integrating managed AWS AI services.
- **2.1**: presigned URLs for secure, time-limited access (S3, CloudFront).
- **3.1**: build and manage container images (ECR, Dockerfiles, tagging, lifecycle policies).
- **3.2**: AWS AI tools to generate tests and automate testing workflows.
- **3.3**: deploy containerized applications (ECS task definitions, EKS manifests, Fargate launch types, rolling updates) and AI tools in CI/CD.
- **4.1** and **4.3**: AI tools for error analysis and optimization.

**Moved between domains** (same scope, different place): unit testing with SAM (1 to 3), Lambda performance tuning (1 to 4), serializing and deserializing data (task 1.3 to 1.1), API Gateway stages and custom domains (3.4 to 3.1), IaC templates (stays in 3.3).

**Consolidated:** four DynamoDB skills became one; encryption plus sensitive data (13 skills) became one task of 7; test plus test automation (11) became one task of 5; observability 8 to 5; optimization 9 to 6. AWS states this does not reduce emphasis on essential skills.

**Not named in C03's list of removals:** AWS's comparison page lists no deleted topics for DVA, only additions, moves and consolidations.

**Explicitly out of scope** (exam guide): designing architectures, designing CI/CD pipelines, administering IAM users and groups, administering servers, selecting foundation models, engineering prompts and designing RAG, designing AI safety frameworks, ETL pipelines and AWS networking infrastructure.

## Study Materials

### Notes (study order)
- [01 - Development with AWS Services](notes/01-development-with-aws-services.md) - Decoupling, SDKs, Lambda, DynamoDB, caching, AI services
- [02 - Security](notes/02-security.md) - IAM, STS, Cognito, presigned URLs, KMS, secrets, AI security
- [03 - Testing and Deployment](notes/03-testing-and-deployment.md) - Artifacts, containers, SAM, CI/CD, deployment strategies
- [04 - Troubleshooting and Optimization](notes/04-troubleshooting-optimization.md) - Logs, metrics, traces, concurrency, caching

### Study Resources
- [Fact Sheet](fact-sheet.md) - Verified facts and in-scope services
- [Practice Plan](practice-plan.md) - 6-week schedule
- [Practice Questions](../../../../resources/practice-questions/aws-developer-associate-dva-c03.md) - 16 original scenario questions

## Official Resources

- **[📖 DVA-C03 Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/developer-associate-03.html)** - Domains, tasks and skills
- **[📖 In-scope AWS services](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/dva-03-in-scope-services.html)** - Services and features that may appear
- **[📖 Out-of-scope AWS services](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/dva-03-out-of-scope-services.html)** - Services that will not appear

## After This Cert

- **[AWS Certified DevOps Engineer - Professional](../../professional/devops-engineer-pro-dop-c02/README.md)** - Deeper CI/CD and operations
- **[AWS Certified Solutions Architect - Associate](../solutions-architect-saa-c03/README.md)** - Architecture design, which this exam deliberately leaves out of scope
