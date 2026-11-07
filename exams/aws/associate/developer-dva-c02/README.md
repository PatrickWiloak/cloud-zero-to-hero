# AWS Certified Developer - Associate (DVA-C02)

## Important Notice

**The DVA-C02 exam retires on November 30, 2026.** Until then it can still be taken; after that date this guide describes a withdrawn exam. The last day to sit DVA-C02 is November 30, 2026. **DVA-C03** registration opened October 27, 2026 and its outline is published: this guide is **superseded by the [DVA-C03 guide](../developer-dva-c03/README.md)**, which also lists what changed. DVA-C03 is in use from December 1, 2026.

Source: [AWS Certified Developer - Associate](https://aws.amazon.com/certification/certified-developer-associate/)

---

## Exam Overview

The AWS Certified Developer - Associate (DVA-C02) exam validates technical expertise in developing and maintaining applications on the AWS platform. This certification demonstrates proficiency in AWS core services, uses, and basic AWS architecture best practices for developers.

**Exam Details:**
- **Exam Code:** DVA-C02
- **Duration:** 130 minutes
- **Number of Questions:** 65 scored questions
- **Question Types:** Multiple choice and multiple response
- **Passing Score:** 720 out of 1000
- **Cost:** $150 USD
- **Language:** Available in multiple languages
- **Delivery:** Pearson VUE testing center or online proctoring
- **Validity:** 3 years
- **Prerequisites:** None (6+ months hands-on AWS development experience recommended)

## Exam Domains

### Domain 1: Development with AWS Services (32%)
- Develop code for applications hosted on AWS
- Develop code for AWS Lambda
- Use data stores in application development
- Use application programming interfaces (APIs) in application development

**Key Services:**
- AWS Lambda (serverless functions)
- Amazon API Gateway (REST, HTTP, WebSocket APIs)
- Amazon DynamoDB (NoSQL database)
- Amazon S3 (object storage)
- Amazon RDS/Aurora (relational databases)
- AWS SDK (language-specific SDKs)

### Domain 2: Security (26%)
- Implement authentication and/or authorization for applications and AWS services
- Implement encryption using AWS services
- Manage sensitive data in application code

**Key Services:**
- AWS IAM (identity and access management)
- Amazon Cognito (user authentication)
- AWS KMS (key management)
- AWS Secrets Manager (secrets storage)
- AWS Systems Manager Parameter Store
- AWS Certificate Manager (SSL/TLS)

### Domain 3: Deployment (24%)
- Prepare application artifacts to be deployed to AWS
- Test applications in development environments
- Automate deployment testing
- Deploy code using AWS CI/CD services

**Key Services:**
- AWS CodeCommit (Git repositories)
- AWS CodeBuild (build service)
- AWS CodeDeploy (deployment automation)
- AWS CodePipeline (CI/CD orchestration)
- AWS CloudFormation (infrastructure as code)
- AWS Elastic Beanstalk (PaaS)
- AWS SAM (Serverless Application Model)

### Domain 4: Troubleshooting and Optimization (18%)
- Assist in a root cause analysis
- Instrument code for observability
- Optimize applications on AWS

**Key Services:**
- Amazon CloudWatch (monitoring and logging)
- AWS X-Ray (distributed tracing)
- AWS CloudTrail (API auditing)
- Application performance monitoring

## Core AWS Services for Developers

### Compute Services

#### AWS Lambda
- **Event-driven serverless compute**
- Runtime support: Python, Node.js, Java, Go, .NET, Ruby, custom runtimes
- Event sources: S3, DynamoDB, API Gateway, SQS, SNS, EventBridge, etc.
- Execution model: Function handler, context object, event object
- Deployment: Versions, aliases, blue/green deployments
- Configuration: Memory (128 MB - 10 GB), timeout (15 minutes max)
- Performance: Provisioned concurrency, Lambda layers, cold start optimization

#### Amazon API Gateway
- **REST APIs:** Full-featured RESTful APIs with OpenAPI support
- **HTTP APIs:** Lightweight, cost-effective APIs (70% cheaper than REST)
- **WebSocket APIs:** Real-time bidirectional communication
- Authentication: IAM, Cognito, Lambda authorizers, API keys
- Features: Caching, throttling, request/response transformation, CORS
- Integration types: Lambda proxy, HTTP proxy, AWS service proxy

#### AWS Elastic Beanstalk
- **Platform-as-a-Service (PaaS)** for easy application deployment
- Supported platforms: Java, .NET, PHP, Node.js, Python, Ruby, Go, Docker
- Deployment options: All at once, rolling, rolling with batch, immutable, blue/green
- Configuration: .ebextensions, environment properties, managed platform updates
- Monitoring: Integrated CloudWatch metrics and logs

### Data Storage Services

#### Amazon DynamoDB
- **Fully managed NoSQL database**
- Data models: Key-value, document
- Capacity modes: On-demand, provisioned
- Table design: Partition key, sort key, composite keys
- Indexes: Global Secondary Index (GSI), Local Secondary Index (LSI)
- Operations: PutItem, GetItem, UpdateItem, DeleteItem, Query, Scan, BatchGetItem, TransactWriteItems
- Features: DynamoDB Streams, Global Tables, Point-in-Time Recovery, DAX (in-memory cache)
- Best practices: Single-table design, efficient partition key design, avoid hot partitions

#### Amazon S3
- **Object storage service**
- Operations: PUT, GET, DELETE, LIST, HEAD, COPY
- Storage classes: Standard, IA, One Zone-IA, Glacier, Glacier Deep Archive
- Event notifications: Trigger Lambda, SQS, SNS on object events
- Access control: IAM policies, bucket policies, ACLs, pre-signed URLs
- Features: Versioning, lifecycle policies, transfer acceleration, multipart upload
- SDK operations: Upload, download, streaming, pagination

#### Amazon RDS and Aurora
- **Managed relational database service**
- Engines: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server
- Aurora: AWS-proprietary high-performance engine (MySQL/PostgreSQL compatible)
- Connection management: Connection pooling, RDS Proxy (for Lambda)
- Authentication: Password-based, IAM database authentication
- High availability: Multi-AZ deployments, read replicas
- Backup: Automated backups, snapshots, point-in-time recovery

### Application Integration

#### Amazon SQS
- **Fully managed message queue**
- Queue types: Standard (at-least-once, best-effort ordering), FIFO (exactly-once, strict ordering)
- Message lifecycle: Visibility timeout, message retention (up to 14 days)
- Dead letter queues: Handle failed message processing
- Long polling: Reduce empty responses and costs
- Integration: Lambda event source, batch processing

#### Amazon SNS
- **Publish/subscribe messaging**
- Topic types: Standard, FIFO
- Protocols: HTTP/HTTPS, Email, SMS, Lambda, SQS, mobile push
- Message filtering: Attribute-based filtering for subscriptions
- Delivery policies: Retry strategies, exponential backoff
- Fan-out pattern: SNS topic → multiple SQS queues

#### AWS Step Functions
- **Serverless workflow orchestration**
- State machine: JSON-based workflow definition (Amazon States Language)
- State types: Task, Choice, Parallel, Wait, Map, Pass, Fail, Succeed
- Error handling: Retry, Catch, fallback states
- Integration: Native integration with 200+ AWS services
- Use cases: Distributed transactions, ETL pipelines, approval workflows

#### Amazon EventBridge
- **Event bus for application integration**
- Event sources: AWS services, custom applications, SaaS partners
- Event patterns: JSON-based pattern matching
- Targets: Lambda, Step Functions, SQS, SNS, API Gateway, etc.
- Schema registry: Discover and manage event schemas
- Use cases: Event-driven architectures, cross-account events

### Security Services

#### AWS IAM
- **Identity and access management**
- Principals: Users, groups, roles (for applications and services)
- Policies: Identity-based, resource-based, permission boundaries
- Policy evaluation: Deny by default, explicit deny wins
- Best practices: Least privilege, use roles (not access keys), MFA, credential rotation
- For applications: Use IAM roles (EC2 instance profiles, Lambda execution roles, ECS task roles)

#### Amazon Cognito
- **User Pools:** User directory, sign-up/sign-in, MFA, password policies
- **Identity Pools:** Federated identity, temporary AWS credentials
- Authentication flows: SRP, custom authentication with Lambda triggers
- Federation: Social providers (Google, Facebook), SAML, OIDC
- Tokens: ID token (user claims), access token (permissions), refresh token
- Integration: API Gateway authorizers, ALB authentication

#### AWS KMS
- **Key Management Service**
- Key types: Symmetric (AES-256), asymmetric (RSA, ECC)
- Key management: Customer managed keys (CMK), AWS managed keys
- Key policies: Resource-based policies for key access
- Operations: Encrypt, Decrypt, GenerateDataKey, ReEncrypt
- Integration: Native encryption for S3, DynamoDB, RDS, Lambda, etc.
- Envelope encryption: Data keys for data, KMS for data keys

#### AWS Secrets Manager
- **Store and rotate secrets**
- Secret types: Database credentials, API keys, OAuth tokens, custom secrets
- Rotation: Automatic rotation with Lambda functions
- Access: IAM policies, resource-based policies
- Integration: RDS automatic integration
- Versioning: Staging labels (AWSCURRENT, AWSPENDING, AWSPREVIOUS)

### Developer Tools

#### AWS CodeCommit
- **Git-based source control**
- Authentication: HTTPS (IAM), SSH, federated access
- Features: Pull requests, approval rules, merge strategies
- Triggers: SNS notifications, Lambda invocations
- Integration: CodeBuild, CodePipeline

#### AWS CodeBuild
- **Fully managed build service**
- Build specification: buildspec.yml (phases, commands, artifacts)
- Build environments: Standard images (Ubuntu, Amazon Linux), custom Docker images
- Build phases: install, pre_build, build, post_build
- Artifacts: S3 upload, encryption
- Environment variables: Plain text, Systems Manager Parameter Store, Secrets Manager
- Caching: S3 caching for dependencies

#### AWS CodeDeploy
- **Automated deployment service**
- Compute platforms: EC2/On-premises, Lambda, ECS
- Deployment types: In-place (rolling), Blue/green
- Deployment configurations: OneAtATime, HalfAtATime, AllAtOnce, custom
- appspec.yml: Deployment instructions (hooks, resources)
- Deployment hooks: ApplicationStop, BeforeInstall, AfterInstall, ApplicationStart, ValidateService
- Rollback: Automatic rollback on failure, manual rollback

#### AWS CodePipeline
- **Continuous delivery orchestration**
- Pipeline structure: Stages (source, build, test, deploy), actions within stages
- Source providers: CodeCommit, GitHub, S3, ECR
- Build providers: CodeBuild, Jenkins
- Deploy providers: CodeDeploy, CloudFormation, ECS, Elastic Beanstalk, S3
- Approval actions: Manual approval gates
- Artifacts: Passed between stages via S3

#### AWS CloudFormation
- **Infrastructure as Code**
- Template formats: JSON, YAML
- Sections: Parameters, Mappings, Conditions, Resources (required), Outputs
- Intrinsic functions: Ref, GetAtt, Sub, Join, Select, ImportValue
- Stack operations: Create, update, delete, drift detection
- Change sets: Preview changes before execution
- StackSets: Deploy across multiple accounts and regions
- Best practices: Use parameters, outputs, cross-stack references

### Monitoring and Debugging

#### Amazon CloudWatch
- **Metrics:** Standard metrics (CPU, network, disk), custom metrics, metric math
- **Logs:** Log groups, log streams, log retention, log insights queries
- **Alarms:** Metric alarms, composite alarms, alarm actions (SNS, Auto Scaling, EC2)
- **Dashboards:** Customizable monitoring dashboards
- **Events (EventBridge):** Event-driven automation
- **Application Insights:** Automatic application monitoring
- **Synthetics:** Canary monitoring for endpoints
- **Log Insights:** Query language for log analysis

#### AWS X-Ray
- **Distributed tracing**
- Concepts: Traces, segments, subsegments, annotations, metadata
- Integration: Lambda (via Lambda layer or SDK), API Gateway (enable tracing), ECS, Elastic Beanstalk
- Daemon: X-Ray daemon for sending trace data
- Service map: Visual representation of application architecture
- Trace analysis: Filter by annotations, identify bottlenecks, analyze errors
- Sampling: Sampling rules to control trace volume
- SDK: Instrument custom code with X-Ray SDK

## Development Best Practices

### AWS SDK Best Practices
1. **Use IAM roles** instead of access keys for credentials
2. **Implement exponential backoff with jitter** for retries
3. **Use connection pooling** - reuse SDK clients
4. **Set appropriate timeouts** for API calls
5. **Handle throttling** - implement retry logic for rate limiting
6. **Use pagination** for list operations (DynamoDB Scan, S3 ListObjects)
7. **Enable SDK logging** for debugging
8. **Explicitly set regions** - avoid relying on defaults

### Lambda Development Best Practices
1. **Minimize cold starts:**
   - Keep functions small and focused
   - Use Lambda layers for shared dependencies
   - Consider provisioned concurrency for critical functions
2. **Optimize memory allocation** - right-size based on performance tests
3. **Use environment variables** for configuration (encrypt sensitive data)
4. **Implement connection reuse:**
   - Initialize SDK clients outside handler
   - Use database connection pooling (RDS Proxy)
5. **Set appropriate timeouts** - default is 3 seconds, max is 15 minutes
6. **Use Lambda layers** for shared code and dependencies
7. **Implement structured logging** with JSON format
8. **Use Lambda destinations** for async event handling

### DynamoDB Best Practices
1. **Design for access patterns** - know your queries first
2. **Choose effective partition keys:**
   - High cardinality (many distinct values)
   - Uniform access patterns (avoid hot partitions)
   - Use composite keys when needed
3. **Use GSI for alternate access patterns**
4. **Avoid scans** - use Query instead when possible
5. **Implement pagination** for large result sets
6. **Use batch operations** - BatchGetItem, BatchWriteItem (up to 25 items)
7. **Use transactions** for ACID requirements (TransactWriteItems, TransactGetItems)
8. **Enable DynamoDB Streams** for change data capture
9. **Use on-demand billing** for unpredictable workloads

### API Gateway Best Practices
1. **Enable caching** to reduce backend calls
2. **Implement throttling** to protect backend services
3. **Use Lambda proxy integration** for simplified development
4. **Validate requests** at the API Gateway layer
5. **Enable CORS** for cross-origin requests
6. **Use custom domain names** with ACM certificates
7. **Implement API keys and usage plans** for tiered access
8. **Use request/response transformations** when needed
9. **Enable CloudWatch Logs** for debugging

### Security Best Practices
1. **Principle of least privilege** - grant minimum required permissions
2. **Never hardcode credentials** - use IAM roles, Secrets Manager
3. **Encrypt data at rest and in transit** - use KMS, TLS/SSL
4. **Rotate credentials regularly** - automate with Secrets Manager
5. **Validate all inputs** - prevent injection attacks
6. **Use VPCs and security groups** for network isolation
7. **Enable CloudTrail** for audit logging
8. **Implement MFA** for sensitive operations
9. **Use resource-based policies** for cross-account access

## Study Strategy

### Recommended Timeline: 6-8 Weeks

**Week 1-2: Core Development Services**
- Lambda function development
- API Gateway configuration
- DynamoDB operations and design
- S3 integration patterns

**Week 3-4: Security Implementation**
- IAM policies and roles
- Cognito authentication
- KMS encryption
- Secrets management

**Week 5-6: Deployment and CI/CD**
- CodeCommit, CodeBuild, CodeDeploy
- CodePipeline orchestration
- CloudFormation templates
- Elastic Beanstalk deployment

**Week 7-8: Integration and Monitoring**
- SQS/SNS messaging
- Step Functions workflows
- CloudWatch monitoring
- X-Ray tracing

### Hands-on Practice Requirements

**CRITICAL:** This exam requires extensive hands-on experience. You must actually build applications using AWS services, not just read about them.

**Essential Labs:**
1. Build serverless REST API (Lambda + API Gateway + DynamoDB)
2. Implement user authentication (Cognito)
3. Create CI/CD pipeline (CodePipeline + CodeBuild + CodeDeploy)
4. Build event-driven architecture (S3 events + Lambda + SQS)
5. Implement distributed tracing (X-Ray)
6. Deploy with CloudFormation or SAM
7. Configure monitoring and alarms (CloudWatch)
8. Implement encryption (KMS) and secrets management

## Common Exam Scenarios

### Scenario 1: Serverless Application Development
- Question focuses on Lambda + API Gateway + DynamoDB
- Consider: Cold starts, timeout configuration, error handling
- Security: IAM roles, Cognito authorization
- Best practice: Use Lambda proxy integration, implement retry logic

### Scenario 2: CI/CD Pipeline Implementation
- Question about automating deployment
- Services: CodeCommit, CodeBuild, CodeDeploy, CodePipeline
- Consider: Blue/green vs rolling deployments, automated testing
- Best practice: Use CloudFormation for infrastructure, implement approval gates

### Scenario 3: Security and Encryption
- Question about securing application data and credentials
- Services: KMS, Secrets Manager, Parameter Store, IAM
- Consider: Encryption at rest vs in transit, key rotation
- Best practice: Use IAM roles, rotate secrets automatically, encrypt sensitive data

### Scenario 4: Application Integration
- Question about decoupling microservices
- Services: SQS, SNS, EventBridge, Step Functions
- Consider: Async vs sync, message ordering, error handling
- Best practice: Use dead letter queues, implement idempotency

### Scenario 5: Monitoring and Troubleshooting
- Question about debugging performance issues
- Services: CloudWatch, X-Ray, CloudTrail
- Consider: Logs, metrics, traces, service maps
- Best practice: Implement structured logging, enable X-Ray tracing, set up alarms

## Exam Tips

### Question Strategy
1. **Read carefully** - identify key requirements and constraints
2. **Look for AWS best practices** - choose the most "AWS-native" solution
3. **Consider cost optimization** - when multiple solutions work, choose the most cost-effective
4. **Think about scale** - solutions should scale automatically
5. **Eliminate wrong answers** - often 2 choices can be ruled out immediately
6. **Watch for keywords:**
   - "Most cost-effective" → serverless, on-demand pricing
   - "Minimum operational overhead" → managed services
   - "Decoupled" → SQS, SNS, EventBridge
   - "Real-time" → Kinesis, DynamoDB Streams
   - "Secure" → IAM roles, encryption, least privilege

### Common Pitfalls
- Confusing IAM policies (identity-based vs resource-based)
- Not understanding Lambda execution model and limits
- Misunderstanding DynamoDB partition key design
- Forgetting about VPC configuration for Lambda accessing RDS
- Not knowing when to use SQS vs SNS vs EventBridge
- Overlooking CloudFormation intrinsic functions
- Not understanding API Gateway integration types

### Time Management
- 130 minutes for 65 questions = 2 minutes per question
- Flag uncertain questions for review
- Don't spend more than 3 minutes on any single question
- Leave 15-20 minutes for review at the end

## 📚 Comprehensive Study Resources

**👉 [Complete AWS Study Resources Guide](../../../../.templates/resources-aws.md)**

For detailed information on courses, practice tests, hands-on labs, communities, and more, see our comprehensive AWS study resources guide.

### Quick Links (DVA-C02 Specific)
- **[DVA-C02 Official Exam Page](https://aws.amazon.com/certification/certified-developer-associate/)** - Registration and official exam guide
- **[AWS Skill Builder](https://skillbuilder.aws/)** - FREE official exam prep and labs
- **[AWS Documentation](https://docs.aws.amazon.com/)** - Complete service documentation
- **[AWS Free Tier](https://aws.amazon.com/free/)** - 12 months free + always-free services
- **[AWS Samples GitHub](https://github.com/aws-samples)** - Sample code and projects

### Recommended Courses
1. **AWS Skill Builder - DVA-C02 Exam Prep** (FREE)
2. **Stephane Maarek's AWS Certified Developer Associate** (Udemy)
3. **Adrian Cantrill's Developer Associate Course**
4. **A Cloud Guru AWS Certified Developer Associate**

### Practice Exams
1. **Tutorials Dojo** - Highly recommended, detailed explanations
2. **Whizlabs** - Good question bank
3. **AWS Skill Builder Official Practice Exam** - $40, closest to real exam

## Next Steps After Certification

### Career Paths
- AWS Developer
- DevOps Engineer
- Cloud Application Developer
- Solutions Architect
- Full-stack Cloud Developer

### Advanced Certifications
- **AWS Certified Solutions Architect - Professional** - Architecture focus
- **AWS Certified DevOps Engineer - Professional** - Advanced DevOps practices
- **Specialty Certifications** - Security, Machine Learning, Data Analytics, etc.

### Continuous Learning
- Stay updated with AWS re:Invent announcements
- Participate in AWS community forums
- Build and deploy real projects
- Contribute to open-source AWS projects
- Attend AWS meetups and webinars

---

**Good luck with your AWS Certified Developer - Associate certification!** 🚀

Remember: This is a hands-on developer exam. Building real applications with AWS services is essential for success!
