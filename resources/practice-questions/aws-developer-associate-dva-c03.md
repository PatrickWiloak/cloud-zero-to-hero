---
last-updated: 2026-11-07
difficulty: intermediate
---

# AWS Certified Developer - Associate (DVA-C03) - Practice Questions

16 original scenario questions for DVA-C03 prep. Domain counts follow the exam weights: Development with AWS Services 5, Security 4, Testing and Deployment 3, Troubleshooting and Optimization 4.

> **Cert page:** [exams/aws/associate/developer-dva-c03/](../../exams/aws/associate/developer-dva-c03/)

---

### Question 1
**Scenario:** An order service must accept orders at bursty rates while a slower billing service processes them at its own pace. A failed order must not block the rest. Which design fits?

A. Call the billing service directly from the order service and retry in a loop
B. Put an Amazon SQS queue between them with a dead-letter queue for repeatedly failing messages
C. Publish each order to an Amazon SNS topic with no subscribers other than billing and drop failures
D. Store orders in an S3 bucket and have billing list the bucket every second

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A queue decouples the two services and absorbs bursts, and a dead-letter queue isolates poison messages. Direct calls keep the services tightly coupled, SNS does not buffer for a consumer's pace the way a queue does, and polling S3 is inefficient and unordered.
</details>

---

### Question 2
**Scenario:** A Lambda function consumes an SQS queue. When one message in a batch of ten fails, the whole batch returns to the queue and the nine good messages are processed again. What reduces the duplicate work?

A. Raise the queue's visibility timeout so that a failed batch stays hidden for longer before it is retried
B. Switch the event source to an asynchronous invocation
C. Increase the function memory
D. Return batchItemFailures identifying only the failed message ids

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Partial batch responses let Lambda delete the successes and return only failed messages to the queue. A longer visibility timeout only delays the retry of the whole batch, more memory does not change retry behavior, and asynchronous invocation is not how an SQS event source mapping works.
</details>

---

### Question 3
**Scenario:** A DynamoDB table uses the order status (five possible values) as its partition key. One partition is throttled while the table has unused capacity. What is the best fix?

A. Change to a high-cardinality partition key such as the order id
B. Switch every read to strongly consistent
C. Replace Query calls with Scan
D. Add a local secondary index on the status attribute to spread reads across more partitions

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Few distinct key values concentrate traffic on a few partitions. A high-cardinality key spreads load. Strong consistency and Scan do not help, and an LSI shares the same partition key.
</details>

---

### Question 4
**Scenario:** An asynchronous Lambda invocation fails after its retries. The team wants the failed event and error details delivered to an SQS queue for analysis. What should they configure?

A. Provisioned concurrency
B. An environment variable holding the queue url that the function code reads when handling errors
C. A Lambda destination for failures that targets the queue
D. A larger function timeout

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Destinations route the result of asynchronous invocations, including failures with details, to a target such as SQS. Timeouts and provisioned concurrency do not capture failed events.
</details>

---

### Question 5
**Scenario:** An application caches product data in ElastiCache and reads it first, loading from the database and storing the result only on a miss. What is the main drawback of this pattern?

A. Reads can never hit the cache
B. Every write is slower because the application must update both the cache and the database each time
C. Cached data can become stale until it expires or is invalidated
D. The cache must hold the entire database

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** This is lazy loading: only requested data is cached, but it can go stale. Updating the cache on every write describes write-through, which is the opposite trade-off.
</details>

---

### Question 6
**Scenario:** A mobile app lets users sign in and then upload photos directly to an S3 bucket using their own temporary AWS credentials. Which combination provides this?

A. A Cognito user pool for sign-in plus an identity pool that exchanges tokens for AWS credentials
B. An S3 bucket policy that allows public writes
C. A single shared role whose access keys are stored in the app resources and rotated with each release
D. An IAM user per app user with access keys embedded in the app

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** User pools authenticate users and issue tokens; identity pools exchange tokens for temporary credentials. Embedded keys and public writes are insecure.
</details>

---

### Question 7
**Scenario:** A web app must let a browser download one private S3 object for the next 10 minutes without giving the user AWS credentials. What should the backend generate?

A. A new IAM user with a console password and a policy that allows reading that one object
B. A public-read ACL on the object
C. A KMS data key for the user
D. A presigned URL with a 600 second expiry

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** A presigned URL grants time-limited access using the creator's permissions. The other options either expose the object publicly or grant more than is needed.
</details>

---

### Question 8
**Scenario:** An application needs to encrypt a 2 GB file with a KMS key. KMS Encrypt accepts only small payloads. What is the correct approach?

A. Call Encrypt once with the whole 2 GB file after raising the payload limit in the KMS key policy
B. Call GenerateDataKey, encrypt the file locally with the data key and store the encrypted key beside it
C. Store the file unencrypted and encrypt the key
D. Use a longer KMS key spec

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Envelope encryption uses a data key for the bulk data and KMS to protect that key. The Encrypt payload limit is fixed by the service (4,096 bytes) and cannot be raised in a key policy, and a longer key spec does not raise it either.
</details>

---

### Question 9
**Scenario:** A developer calls a foundation model from a VPC-based application. The company requires that traffic stay off the public internet. Which control meets this?

A. A longer request timeout
B. Removing the IAM role from the application
C. A NAT gateway so the traffic exits through a fixed address
D. An interface VPC endpoint (AWS PrivateLink) for the service

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Interface VPC endpoints keep traffic on the AWS network. A NAT gateway still uses the internet path, and the other options do not affect routing.
</details>

---

### Question 10
**Scenario:** A team wants a Lambda release where 10 percent of traffic goes to the new version for five minutes, with automatic rollback if an alarm fires, then the rest follows. What should they use?

A. Two functions and a manual DNS switch that moves all users to the new one after testing
B. CodeDeploy with a canary configuration on a Lambda alias and an alarm
C. Replace the function code in place
D. A rolling update on an ECS service

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** CodeDeploy shifts Lambda alias traffic with canary or linear configurations and can roll back on alarms. In-place replacement has no staged traffic shift.
</details>

---

### Question 11
**Scenario:** A pipeline pushes container images to Amazon ECR and the registry fills with thousands of old images. What keeps the repository tidy without manual work?

A. An ECR lifecycle policy that expires images by count or age
B. Tagging every image latest so that each push overwrites and removes the earlier image
C. Deleting the repository weekly
D. Disabling image scanning

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Lifecycle policies expire images automatically. Reusing latest hides history and does not reduce storage.
</details>

---

### Question 12
**Scenario:** Which command runs a Lambda function locally with a saved JSON event using AWS SAM?

A. aws lambda create-function --event events/order.json
B. sam build --invoke events/order.json
C. sam local invoke MyFunction --event events/order.json
D. sam deploy --event events/order.json

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** sam local invoke runs a function locally with an event file. The other commands either deploy, create resources or are not valid usage.
</details>

---

### Question 13
**Scenario:** Lambda errors appear in CloudWatch Logs, and the team wants the 50 most recent messages that contain ERROR. Which tool and approach fit?

A. CloudWatch Logs Insights with a filter on @message and a limit
B. X-Ray annotations
C. AWS Config rules
D. An SNS email subscription on the log group that sends each matching line as it arrives

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Logs Insights queries log groups with filter, sort and limit. X-Ray shows traces, Config tracks configuration and SNS only delivers notifications.
</details>

---

### Question 14
**Scenario:** A request passes through API Gateway, three Lambda functions and DynamoDB, and users report it is slow. Which service shows which hop is slow?

A. AWS Artifact
B. Amazon Route 53
C. AWS X-Ray tracing
D. Amazon Macie

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** X-Ray follows a request across services and shows per-segment latency.
</details>

---

### Question 15
**Scenario:** A Lambda function has noticeable cold-start latency during traffic spikes, and the team is willing to pay to remove it for a latency-sensitive API. What should they configure?

A. A dead-letter queue
B. Provisioned concurrency
C. Reserved concurrency set to zero
D. A larger log retention period

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Provisioned concurrency keeps execution environments initialized. Reserved concurrency of zero stops the function from running.
</details>

---

### Question 16
**Scenario:** Pods in a container service sometimes receive traffic before the application has finished loading its configuration. Which mechanism prevents this?

A. A liveness probe with a shorter interval so that unready Pods are restarted before they receive traffic
B. A larger instance type
C. Disabling health checks
D. A readiness probe that reports ready only after startup completes

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Readiness controls when a container receives traffic. Liveness decides restarts, which would not solve premature routing.
</details>

---
