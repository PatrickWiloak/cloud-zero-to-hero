---
last-updated: 2026-10-16
exam-version: DVA-C02
exam-retires: 2026-11-30
---

# AWS Certified Developer - Associate (DVA-C02) Fact Sheet

> ⚠️ **RETIRING November 30, 2026.** The last day to sit DVA-C02 is November 30, 2026. **DVA-C03** registration opened October 27, 2026 and its outline is published: this guide is **superseded by the [DVA-C03 guide](../developer-dva-c03/README.md)**, which also lists what changed. DVA-C03 is in use from December 1, 2026.

## Quick Reference

**Exam Code:** DVA-C02
**Duration:** 130 minutes
**Questions:** 65 scored questions
**Passing Score:** 720/1000
**Cost:** $150 USD
**Validity:** 3 years
**Delivery:** Pearson VUE (Testing center or online proctored)

## Exam Domain Breakdown

| Domain | Weight | Focus |
|--------|--------|-------|
| Development with AWS Services | 32% | Lambda, API Gateway, DynamoDB, S3, SDK |
| Security | 26% | IAM, Cognito, KMS, Secrets Manager |
| Deployment | 24% | CodePipeline, CodeBuild, CodeDeploy, CloudFormation |
| Troubleshooting & Optimization | 18% | CloudWatch, X-Ray, performance tuning |

## Core Services to Master

### Development (32%)
- **AWS Lambda** - Serverless functions, event sources, cold starts
  - **[📖 Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)** - Complete Lambda documentation
  - **[📖 Lambda Function Configuration](https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html)** - Memory, timeout, env vars
  - **[📖 Lambda Event Sources](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html)** - Triggers and integrations
  - **[📖 Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)** - Performance and security
- **API Gateway** - REST/HTTP/WebSocket APIs, authorization
  - **[📖 API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/)** - Complete API Gateway docs
  - **[📖 API Gateway REST APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-rest-api.html)** - RESTful API creation
  - **[📖 API Gateway HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)** - Lower cost, faster
  - **[📖 API Gateway Authorization](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html)** - IAM, Cognito, Lambda authorizers
- **DynamoDB** - NoSQL operations, partition keys, GSI/LSI
  - **[📖 DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/)** - Complete DynamoDB docs
  - **[📖 DynamoDB Core Components](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html)** - Tables, items, attributes
  - **[📖 DynamoDB API Reference](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.API.html)** - Operations reference
  - **[📖 DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)** - Design patterns
- **S3** - Object operations, event notifications, pre-signed URLs
  - **[📖 S3 Developer Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)** - Complete S3 documentation
  - **[📖 S3 API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/)** - Object operations
  - **[📖 S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html)** - Lambda, SQS, SNS triggers
  - **[📖 S3 Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)** - Temporary access
- **AWS SDK** - Best practices, error handling, retries
  - **[📖 AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)** - Python SDK
  - **[📖 AWS SDK for JavaScript](https://docs.aws.amazon.com/sdk-for-javascript/)** - Node.js SDK
  - **[📖 SDK Error Handling](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)** - Retry strategies
  - **[📖 SDK Credentials](https://docs.aws.amazon.com/sdkref/latest/guide/access.html)** - Authentication

### Security (26%)
- **IAM** - Roles, policies, least privilege
  - **[📖 IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/)** - Complete IAM documentation
  - **[📖 IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)** - Role-based access
  - **[📖 IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)** - Policy syntax and evaluation
  - **[📖 IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)** - Security guidelines
- **Cognito** - User Pools, Identity Pools, federation
  - **[📖 Cognito Developer Guide](https://docs.aws.amazon.com/cognito/latest/developerguide/)** - Complete Cognito docs
  - **[📖 Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)** - Authentication
  - **[📖 Cognito Identity Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html)** - AWS resource access
  - **[📖 Cognito Federation](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-identity-federation.html)** - Social and SAML
- **KMS** - Encryption, key management, envelope encryption
  - **[📖 KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)** - Complete KMS documentation
  - **[📖 KMS Key Concepts](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html)** - Keys and aliases
  - **[📖 KMS Envelope Encryption](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#enveloping)** - Data key encryption
  - **[📖 KMS Key Policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)** - Access control
- **Secrets Manager** - Secret storage, rotation
  - **[📖 Secrets Manager User Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/)** - Complete Secrets Manager docs
  - **[📖 Secrets Rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)** - Automatic rotation
  - **[📖 Secrets Manager Best Practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)** - Security guidelines
- **Parameter Store** - Configuration management
  - **[📖 Parameter Store User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)** - SSM parameters
  - **[📖 Parameter Hierarchies](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-hierarchies.html)** - Organize parameters
  - **[📖 Secure String Parameters](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-securestring.html)** - KMS encryption

### Deployment (24%)
- **CodeCommit** - Git repositories
  - **[📖 CodeCommit User Guide](https://docs.aws.amazon.com/codecommit/latest/userguide/)** - Complete CodeCommit docs
  - **[📖 CodeCommit Repositories](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-create-repository.html)** - Repository management
  - **[📖 CodeCommit Triggers](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-notify.html)** - Event notifications
- **CodeBuild** - Build automation, buildspec.yml
  - **[📖 CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/)** - Complete CodeBuild docs
  - **[📖 Build Specification](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)** - buildspec.yml reference
  - **[📖 CodeBuild Environment](https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref.html)** - Docker images and runtimes
- **CodeDeploy** - Deployment strategies, appspec.yml
  - **[📖 CodeDeploy User Guide](https://docs.aws.amazon.com/codedeploy/latest/userguide/)** - Complete CodeDeploy docs
  - **[📖 AppSpec File](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file.html)** - Deployment specification
  - **[📖 Deployment Configurations](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html)** - In-place and blue/green
- **CodePipeline** - CI/CD orchestration
  - **[📖 CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/)** - Complete CodePipeline docs
  - **[📖 Pipeline Structure](https://docs.aws.amazon.com/codepipeline/latest/userguide/pipeline-structure.html)** - Stages and actions
  - **[📖 Pipeline Actions](https://docs.aws.amazon.com/codepipeline/latest/userguide/actions.html)** - Action types reference
- **CloudFormation** - Infrastructure as Code
  - **[📖 CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)** - Complete CloudFormation docs
  - **[📖 Template Anatomy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html)** - Template structure
  - **[📖 Intrinsic Functions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)** - Template functions
  - **[📖 Stack Updates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks.html)** - Change sets and rollback
- **Elastic Beanstalk** - PaaS deployments
  - **[📖 Elastic Beanstalk Developer Guide](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/)** - Complete Beanstalk docs
  - **[📖 Deployment Policies](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.rolling-version-deploy.html)** - Rolling, blue/green, immutable
  - **[📖 Configuration Files](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/ebextensions.html)** - .ebextensions customization

### Troubleshooting (18%)
- **CloudWatch** - Logs, metrics, alarms, insights
  - **[📖 CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/)** - Complete CloudWatch docs
  - **[📖 CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/)** - Log aggregation and analysis
  - **[📖 CloudWatch Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html)** - Custom metrics and alarms
  - **[📖 CloudWatch Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)** - Log query language
- **X-Ray** - Distributed tracing, service maps
  - **[📖 X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/)** - Complete X-Ray docs
  - **[📖 X-Ray Concepts](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html)** - Traces, segments, annotations
  - **[📖 X-Ray SDK](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-nodejs.html)** - Instrument applications
  - **[📖 X-Ray Sampling](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-sampling.html)** - Sampling rules
- **Performance optimization** - Lambda, DynamoDB, API caching
  - **[📖 Lambda Performance](https://docs.aws.amazon.com/lambda/latest/dg/lambda-performance.html)** - Cold starts and optimization
  - **[📖 DynamoDB Performance](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)** - Throughput optimization
  - **[📖 API Gateway Caching](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html)** - Cache configuration
- **Cost optimization** - Right-sizing, serverless patterns
  - **[📖 Lambda Pricing](https://aws.amazon.com/lambda/pricing/)** - Request and compute costs
  - **[📖 DynamoDB Pricing](https://aws.amazon.com/dynamodb/pricing/)** - On-demand vs provisioned
  - **[📖 Cost Optimization](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/)** - Well-Architected pillar

## Service Limits to Know

### Lambda
- **Timeout:** 15 minutes max
- **Memory:** 128 MB - 10 GB
- **Deployment package:** 50 MB (zipped), 250 MB (unzipped)
- **Concurrent executions:** 1,000 (default, can request increase)
- **Environment variables:** 4 KB total
- **Layers:** 5 layers per function

### DynamoDB
- **Item size:** 400 KB max
- **Partition key:** 2,048 bytes max
- **Sort key:** 1,024 bytes max
- **BatchGetItem:** 100 items, 16 MB
- **BatchWriteItem:** 25 items
- **Query result:** 1 MB max per request
- **Transaction:** 100 items, 4 MB

### API Gateway
- **Timeout:** 29 seconds max
- **Payload size:** 10 MB max
- **Header size:** 10 KB total
- **Integration timeout:** 29 seconds
- **Rate limits:** 10,000 requests per second (default)
- **Burst limits:** 5,000 requests

### S3
- **Object size:** 5 TB max
- **Single PUT:** 5 GB max
- **Multipart upload:** Required for > 5 GB
- **Part size:** 5 MB - 5 GB (except last part)
- **Parts:** 10,000 parts max per upload
- **Bucket limit:** 100 buckets per account (default)

## Lambda Event Sources

### Synchronous (Wait for response)
- API Gateway
- Application Load Balancer
- Amazon Cognito
- AWS Step Functions
- Amazon Lex
- Amazon Alexa
- Amazon CloudFront (Lambda@Edge)
- AWS SDK invoke
- **[📖 Lambda Synchronous Invocation](https://docs.aws.amazon.com/lambda/latest/dg/invocation-sync.html)** - Request-response pattern
- **[📖 Lambda with API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)** - REST API integration
- **[📖 Lambda with ALB](https://docs.aws.amazon.com/lambda/latest/dg/services-alb.html)** - Load balancer targets

### Asynchronous (No wait)
- S3
- SNS
- EventBridge (CloudWatch Events)
- AWS CodeCommit
- AWS CodePipeline
- Amazon SES
- AWS Config
- AWS IoT
- **[📖 Lambda Asynchronous Invocation](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html)** - Event-driven pattern
- **[📖 Lambda with S3](https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html)** - S3 event processing
- **[📖 Lambda with SNS](https://docs.aws.amazon.com/lambda/latest/dg/with-sns.html)** - Topic subscriptions

### Stream-based (Poll-based)
- DynamoDB Streams
- Kinesis Data Streams
- Amazon SQS
- Amazon MQ
- Apache Kafka (MSK)
- **[📖 Lambda Event Source Mappings](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html)** - Stream processing
- **[📖 Lambda with DynamoDB Streams](https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html)** - Change data capture
- **[📖 Lambda with SQS](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html)** - Queue processing
- **[📖 Lambda with Kinesis](https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html)** - Stream analytics

## DynamoDB Access Patterns

| Operation | Use Case | Performance |
|-----------|----------|-------------|
| **GetItem** | Retrieve single item by primary key | Fastest, most efficient |
| **BatchGetItem** | Retrieve up to 100 items | Efficient for multiple items |
| **Query** | Items with same partition key | Efficient, use sort key filtering |
| **Scan** | All items in table | Slowest, expensive, avoid if possible |
| **PutItem** | Insert or replace item | Fast |
| **UpdateItem** | Modify specific attributes | Fast, use atomic counters |
| **DeleteItem** | Remove single item | Fast |
| **TransactWriteItems** | ACID transactions (up to 100 items) | Slower, higher cost |

**Documentation:**
- **[📖 DynamoDB Query](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html)** - Query operations
- **[📖 DynamoDB Scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html)** - Scan operations and optimization
- **[📖 DynamoDB BatchOperations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/batch-operation-document-api-java.html)** - Batch reads and writes
- **[📖 DynamoDB Transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html)** - ACID transactions

## IAM Policy Evaluation Logic

1. **By default, deny all** (implicit deny)
2. **Explicit DENY always wins** (cannot be overridden)
3. **Explicit ALLOW overrides implicit deny**
4. **Evaluation order:**
   - Evaluate all applicable policies
   - Check for explicit DENY → if found, deny access
   - Check for explicit ALLOW → if found, allow access
   - If no ALLOW found, implicit deny applies

**Policy Types:**
- **Identity-based** - Attached to users, groups, roles
- **Resource-based** - Attached to resources (S3 buckets, SQS queues, Lambda functions)
- **Permission boundaries** - Maximum permissions for identity-based policies
- **SCPs** - Service Control Policies (organization level)

**Documentation:**
- **[📖 IAM Policy Evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)** - Policy evaluation logic
- **[📖 IAM Policy Types](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)** - Identity vs resource-based
- **[📖 IAM Policy Examples](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_examples.html)** - Common policy patterns
- **[📖 IAM Policy Simulator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html)** - Test policy effects

## CodeDeploy Deployment Types

### In-Place (Rolling)
- **Compute:** EC2, on-premises
- **Traffic:** Gradual shift
- **Rollback:** Redeploy previous version
- **Cost:** Lower (no duplicate infrastructure)
- **Downtime:** Possible during deployment
- **Configs:** OneAtATime, HalfAtATime, AllAtOnce, Custom

### Blue/Green
- **Compute:** EC2, Lambda, ECS
- **Traffic:** All-at-once switch
- **Rollback:** Instant (reroute traffic back)
- **Cost:** Higher (duplicate infrastructure temporarily)
- **Downtime:** None
- **Lambda:** Version aliases
- **ECS:** New task set

## API Gateway Integration Types

| Type | Use Case | Request/Response Transform |
|------|----------|----------------------------|
| **Lambda Proxy** | Simple Lambda integration | No transformation, Lambda receives entire request |
| **Lambda Custom** | Transform request/response | Full control via mapping templates |
| **HTTP Proxy** | Pass-through to HTTP endpoint | No transformation |
| **HTTP Custom** | Transform to HTTP endpoint | Full control via mapping templates |
| **AWS Service** | Direct AWS service integration | Map to service API format |
| **Mock** | Return response without backend | Testing, static responses |

## CloudFormation Intrinsic Functions

| Function | Purpose | Example |
|----------|---------|---------|
| **Ref** | Reference parameter or resource | `!Ref MyParameter` |
| **GetAtt** | Get attribute of resource | `!GetAtt MyBucket.Arn` |
| **Sub** | String substitution | `!Sub 'arn:aws:s3:::${BucketName}'` |
| **Join** | Join strings with delimiter | `!Join ['/', [a, b, c]]` |
| **Select** | Select item from list | `!Select [0, !GetAZs '']` |
| **ImportValue** | Import cross-stack export | `!ImportValue NetworkStackVPC` |
| **Split** | Split string into list | `!Split ['\|', 'a\|b\|c']` |
| **GetAZs** | List of AZs in region | `!GetAZs ''` |
| **FindInMap** | Find value in mappings | `!FindInMap [RegionMap, !Ref AWS::Region, AMI]` |
| **If** | Conditional value | `!If [CreateProd, t3.large, t3.micro]` |

## X-Ray Concepts

- **Trace** - End-to-end journey of a request
- **Segment** - Data about work done by a service
- **Subsegment** - Granular timing within a segment (DB calls, HTTP requests)
- **Annotation** - Key-value pairs for **indexing and filtering** (searchable)
- **Metadata** - Key-value pairs for **additional data** (not searchable)
- **Sampling** - Rules to control which requests are traced
- **Service Map** - Visual representation of application architecture

**Documentation:**
- **[📖 X-Ray Segments](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html#xray-concepts-segments)** - Segment structure
- **[📖 X-Ray Annotations](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-nodejs-segment.html#xray-sdk-nodejs-segment-annotations)** - Indexable metadata
- **[📖 X-Ray Service Map](https://docs.aws.amazon.com/xray/latest/devguide/xray-console.html#xray-console-servicemap)** - Visualize architecture
- **[📖 X-Ray Sampling Rules](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-sampling.html)** - Control tracing rate

## SQS vs SNS vs EventBridge

| Feature | SQS | SNS | EventBridge |
|---------|-----|-----|-------------|
| **Pattern** | Point-to-point (queue) | Pub/sub (topic) | Event bus |
| **Consumers** | One consumer per message | Multiple subscribers | Multiple targets |
| **Message retention** | Up to 14 days | No retention (deliver now) | No retention |
| **Filtering** | Consumer-side | Subscription filter policies | Event patterns (JSON) |
| **Ordering** | FIFO queues | FIFO topics | No guarantee |
| **Use case** | Decouple services, async tasks | Fan-out notifications | Event-driven architecture, rules |
| **Targets** | Polled by consumers | Push to subscribers | 20+ AWS services |

**Documentation:**
- **[📖 SQS Developer Guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/)** - Queue concepts and operations
- **[📖 SQS FIFO Queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html)** - Ordering and deduplication
- **[📖 SNS Developer Guide](https://docs.aws.amazon.com/sns/latest/dg/)** - Topic and subscription management
- **[📖 SNS Message Filtering](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html)** - Subscription filters
- **[📖 EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)** - Event bus and rules
- **[📖 EventBridge Event Patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html)** - Pattern matching

## Exam Tips - Key Concepts

### Lambda Best Practices
- ✅ Use environment variables for config
- ✅ Initialize SDK clients outside handler
- ✅ Use Lambda Layers for shared code
- ✅ Implement exponential backoff for retries
- ✅ Use provisioned concurrency for critical functions
- ❌ Don't store state in Lambda function
- ❌ Don't use recursive calls without limits

### DynamoDB Best Practices
- ✅ Design for access patterns first
- ✅ Use composite partition keys for even distribution
- ✅ Use GSI for alternate access patterns
- ✅ Use Query instead of Scan
- ✅ Use eventually consistent reads (default)
- ❌ Don't use Scan for production queries
- ❌ Don't create hot partitions

### Security Best Practices
- ✅ Use IAM roles, not access keys
- ✅ Encrypt data at rest with KMS
- ✅ Use Secrets Manager for credentials
- ✅ Enable CloudTrail for audit logs
- ✅ Implement least privilege access
- ❌ Never hardcode credentials
- ❌ Don't use root account

### CI/CD Best Practices
- ✅ Automate all deployments
- ✅ Use blue/green for zero-downtime
- ✅ Implement automated testing in pipeline
- ✅ Use CloudFormation for infrastructure
- ✅ Tag resources for cost tracking
- ❌ Don't manually deploy to production
- ❌ Don't skip testing stages

## Common Exam Scenarios

1. **"Most cost-effective solution"** → Serverless (Lambda, DynamoDB on-demand, S3)
2. **"Minimum operational overhead"** → Managed services, Elastic Beanstalk
3. **"Decouple microservices"** → SQS between services
4. **"Fan-out notifications"** → SNS to multiple SQS queues
5. **"Secure API"** → API Gateway + Cognito User Pools
6. **"Store credentials securely"** → Secrets Manager with rotation
7. **"Debug performance issues"** → X-Ray distributed tracing
8. **"Zero-downtime deployment"** → Blue/green with CodeDeploy
9. **"Event-driven processing"** → S3 event → Lambda
10. **"Workflow orchestration"** → Step Functions

## Study Priorities

### High Priority (Must Know)
- Lambda function development and event sources
- DynamoDB operations and design patterns
- API Gateway configuration and authorization
- IAM roles and policies for applications
- Cognito User Pools and Identity Pools
- KMS encryption and envelope encryption
- CodePipeline, CodeBuild, CodeDeploy
- CloudWatch Logs and metrics
- X-Ray tracing implementation

### Medium Priority (Important)
- S3 event notifications and pre-signed URLs
- SQS/SNS messaging patterns
- Step Functions state machines
- Secrets Manager and Parameter Store
- CloudFormation template syntax
- Elastic Beanstalk deployment options
- RDS Proxy for serverless
- EventBridge rules and patterns

### Lower Priority (Good to Know)
- Lambda@Edge and CloudFront integration
- DynamoDB Accelerator (DAX)
- AppSync for GraphQL APIs
- Kinesis Data Streams
- ECS/ECR containerization
- API Gateway caching strategies
- CloudWatch Synthetics
- AWS SAM framework

## Last-Minute Review

**Remember these:**
- Lambda max timeout: 15 minutes
- DynamoDB item max size: 400 KB
- API Gateway timeout: 29 seconds
- IAM policy evaluation: Explicit DENY always wins
- Cognito: User Pools = authentication, Identity Pools = AWS access
- KMS: Envelope encryption for large data
- CodeDeploy: Blue/green = zero downtime
- X-Ray: Annotations are searchable, metadata is not
- SQS visibility timeout: Message hidden during processing
- CloudFormation: Ref for IDs, GetAtt for attributes

**Common gotchas:**
- Lambda in VPC needs NAT gateway for internet access
- DynamoDB Scan reads entire table (expensive)
- API Gateway caching is per stage
- Cognito tokens expire (need refresh token)
- CodeBuild needs buildspec.yml
- CloudFormation rollback on any failure (by default)
- X-Ray daemon must be running
- IAM eventually consistent (except when reading own writes)

---

**Good luck on your exam!** Focus on hands-on practice - build actual applications with these services.
