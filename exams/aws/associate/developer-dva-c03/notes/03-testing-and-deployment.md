---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 30 min
---

# Domain 3: Testing and Deployment (22%)

## Overview

Domain 3 was "Deployment" (24 percent) in C02; it is now **Testing and Deployment** at 22 percent. Three tasks: **3.1** prepare application artifacts, **3.2** implement and automate application testing, **3.3** deploy code with CI/CD services. Testing moved in (unit testing with AWS SAM came from Domain 1) and C03 merged the old "test" and "automate testing" tasks into one with an AI testing skill added. Container image build and deployment are new explicit skills.

**[📖 Exam guide: Content Domain 3](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/developer-associate-03-domain3.html)** - The official skills list

## Task 3.1: Prepare artifacts

**Dependencies and packaging** (3.1.1). A function or service ships with its dependencies. For Lambda, a .zip archive can hold your code and libraries, a **layer** shares libraries across functions, and a **container image** (up to 10 GB) packages larger or custom runtimes. Keep configuration out of the package; read it at run time.

**Container images** (3.1.2, new). Build with a Dockerfile, tag, and push to **Amazon ECR**. Authenticate Docker to your registry with a short-lived token:

```bash
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin 111122223333.dkr.ecr.us-east-1.amazonaws.com
docker build -t myapp:1.4.2 .
docker tag myapp:1.4.2 111122223333.dkr.ecr.us-east-1.amazonaws.com/myapp:1.4.2
docker push 111122223333.dkr.ecr.us-east-1.amazonaws.com/myapp:1.4.2
```

Use **immutable, specific tags** (a version or commit id) rather than relying on `latest`, so a deployment is reproducible and a rollback points at a known image. ECR **lifecycle policies** expire old images by count or age so the registry does not grow without bound:

```json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep the 20 most recent images",
      "selection": {"tagStatus": "any", "countType": "imageCountMoreThan", "countNumber": 20},
      "action": {"type": "expire"}
    }
  ]
}
```

**Code repositories** (3.1.3). Pipelines pull source from a repository (for example GitHub or GitLab). Use AWS CodeArtifact to host and proxy package dependencies.

**Environment-specific configuration** (3.1.4). Use **AWS AppConfig** for validated, gradually deployed feature flags and configuration; **Parameter Store** and **Secrets Manager** for values and secrets; API Gateway **stage variables** and Lambda environment variables for per-environment settings. **API Gateway features** (3.1.5; moved here from C02's "Deployment" task 3.4): an API is deployed to a **stage** (for example `dev`, `prod`), each stage has its own invoke URL, and stages can have custom domain names.

**[📖 Amazon ECR lifecycle policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html)** - Expiring images automatically
**[📖 AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)** - Feature flags and validated configuration deployment

## Task 3.2: Testing

C03 combines testing and test automation into one task of five skills.

- **Develop and validate tests** (3.2.1) with AWS SAM, AWS CDK and CloudFormation. SAM can run a function locally with a test event: `sam local invoke MyFunction --event events/order.json`, and `sam local start-api` serves API Gateway locally.
- **Mock APIs for external dependencies** (3.2.2): API Gateway can return a **mock integration** response with no backend, letting teams test against a dependency that does not exist yet.
- **Test events** (3.2.3): a JSON payload shaped like the real trigger (an SQS record batch, an API Gateway proxy event). In the Lambda console you save test events; in the CLI you invoke with a payload file.

```bash
aws lambda invoke --function-name my-fn --cli-binary-format raw-in-base64-out \
  --payload file://events/order.json response.json
```

- **Application environments** (3.2.4): separate environments are built from **Lambda aliases** (a named pointer to a published version, such as `prod`), container image tags, Amplify branches, Copilot environments and API Gateway stages.
- **AI tools for testing** (3.2.5, new): use AWS AI tools to generate tests and automate repetitive testing (test execution, result analysis, regression automation, coverage). As with generated code, generated tests are reviewed: confirm that they assert real behavior and that coverage means something.

## Task 3.3: Deploy with CI/CD

### Packaging and IaC

**Lambda packaging** (3.3.1): .zip, container image or layers, chosen for deployment efficiency. **Infrastructure as code** (3.3.3): CloudFormation templates, and **AWS SAM**, an extension that makes serverless resources short to declare. The SAM workflow:

```bash
sam build
sam deploy --guided        # first time: asks for stack name, Region, and saves samconfig.toml
sam deploy                 # later deployments reuse the saved settings
```

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  OrdersFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      Runtime: python3.12
      AutoPublishAlias: live
      DeploymentPreference:
        Type: Canary10Percent5Minutes     # CodeDeploy shifts 10% of traffic, waits 5 min, then the rest
```

### Containers

Deploy containerized applications (3.3.2, new) with **Amazon ECS** (a **task definition** describes the containers, CPU, memory, roles and ports; a **service** keeps the desired number of tasks running) on **AWS Fargate** (serverless compute, no instances to manage) or EC2, or with **Amazon EKS** (Kubernetes **manifests**). An ECS service can use a **rolling update** (the `ECS` deployment type): the scheduler replaces running tasks with new ones, within the limits set by `minimumHealthyPercent` and `maximumPercent`.

### CodePipeline, CodeBuild, CodeDeploy

- **CodePipeline** orchestrates stages (source, build, test, approval, deploy) and moves artifacts between them; it can be triggered by a push to a linked repository and can promote a release through multiple environments (3.3.5).
- **CodeBuild** runs the build and tests defined in a `buildspec.yml`.
- **CodeDeploy** deploys revisions to EC2/on-premises, Lambda or ECS (3.3.4). An `appspec` file describes the deployment and its lifecycle hooks.

### Strategies and rollback

| Strategy | How it works | Rollback |
|---|---|---|
| **Rolling** | Replace instances or tasks in batches | Redeploy the previous version; capacity is reduced mid-deployment |
| **Blue/green** | Stand up a full new environment, then shift traffic | Shift traffic back to the old environment |
| **Canary** | Send a small percentage of traffic to the new version first, then the rest after a bake time | Stop and route all traffic back to the old version |
| **Linear** | Shift traffic in equal increments at fixed intervals | Same as canary |
| **All at once** | Replace everything immediately | Redeploy; brief outage risk |

CodeDeploy for Lambda and ECS supports blue/green with canary, linear and all-at-once traffic shifting. **Automatic rollback** (3.3.7) can trigger when a deployment fails or when a CloudWatch alarm fires during the deployment. CloudFormation rolls back a failed stack update automatically, restoring the previous state. Manage versions with Git **labels (tags)** and **branches** (3.3.8). New skill 3.3.9 covers AWS AI tools in CI/CD: automated deployment approvals, environment provisioning and post-deployment validation. Keep a human approval for production and treat AI recommendations as inputs.

**[📖 CodeDeploy for AWS Lambda deployments](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps-lambda.html)** - Traffic shifting and hooks
**[📖 AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)** - Building, testing and deploying serverless applications
**[📖 Amazon ECS deployment types](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html)** - Rolling update and blue/green for services

## What changed from C02 in this domain

- **Added:** container image build and management (3.1.2); container deployment (3.3.2); AI tools for testing (3.2.5) and CI/CD (3.3.9).
- **Merged:** C02's 3.2 (test, 6 skills) and 3.3 (automate testing, 5 skills) became one task of 5 skills.
- **Moved in:** unit testing with SAM (from Domain 1); API Gateway stages and custom domains (from C02's 3.4 to 3.1).
- **Weight:** 24 percent ("Deployment") to 22 percent ("Testing and Deployment").

## Key terms

- **Lambda alias** - a named pointer to a published Lambda function version, used to separate environments and shift traffic.
- **Amazon ECR** - AWS's managed container image registry.
- **ECR lifecycle policy** - rules that automatically expire images by age or count.
- **AWS AppConfig** - a service for deploying validated configuration and feature flags gradually.
- **API Gateway stage** - a named deployment of an API with its own invoke URL and settings.
- **Mock integration** - an API Gateway integration that returns a configured response without calling a backend.
- **AWS SAM** - an extension of CloudFormation with shorthand for serverless resources and a CLI to build, test and deploy them.
- **ECS task definition** - the blueprint that describes the containers, resources and roles for an ECS task.
- **AWS Fargate** - serverless compute for containers that removes the need to manage servers.
- **AWS CodePipeline** - a service that orchestrates the stages of a release process.
- **AWS CodeBuild** - a managed build service that compiles code and runs tests.
- **AWS CodeDeploy** - a service that deploys application revisions to EC2, on-premises servers, Lambda or ECS.
- **Blue/green deployment** - running old and new versions side by side and shifting traffic between them.
- **Canary deployment** - sending a small share of traffic to a new version before shifting all traffic.
- **Rolling deployment** - replacing instances or tasks in batches.
- **Automatic rollback** - reverting a deployment automatically when it fails or an alarm triggers.
