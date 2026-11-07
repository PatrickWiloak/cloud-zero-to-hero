---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 30 min
---

# Domain 1: Development with AWS Services (30%)

## Overview

Domain 1 is the largest part of DVA-C03 at 30 percent of scored content (it was 32 percent in DVA-C02). It has three tasks: **1.1** develop code for applications hosted on AWS, **1.2** develop code for AWS Lambda, and **1.3** use data stores during application development. Two skills are new in C03: using AI-assisted development tools (1.1.9) and integrating managed AWS AI services into applications (1.1.10). Moved in from other domains: serializing and deserializing data now sits in 1.1 (skill 1.1.7). Moved out: unit testing with AWS SAM went to Domain 3 and Lambda performance tuning to Domain 4.

**[📖 Exam guide: Content Domain 1](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/developer-associate-03-domain1.html)** - The official skills list for this domain

## Task 1.1: Code for applications hosted on AWS

### Coupling, and synchronous versus asynchronous

A **tightly coupled** system has components that call each other directly, so one slow or failed component stalls its callers. A **loosely coupled** system puts a managed service between them so each side can scale and fail independently. The exam asks you to pick the AWS service that provides the decoupling and to choose between the two call styles:

| Pattern | Service | Use when |
|---|---|---|
| Synchronous request/response | Amazon API Gateway in front of a function or service | The caller needs the answer now |
| Asynchronous queue | Amazon SQS | Work can wait, load is bursty, a consumer should pull at its own pace |
| Fan-out publish/subscribe | Amazon SNS | One event must reach several subscribers (queues, functions, email) |
| Event routing by rules | Amazon EventBridge | Route events from AWS services, SaaS and your apps by pattern, across accounts |
| Ordered, replayable stream | Amazon Kinesis Data Streams | Many records per second, multiple consumers, ordering per partition key |

An SQS consumer receives a message and has until the **visibility timeout** to delete it; if it does not, the message becomes visible again and is retried. After a configured number of receives, a message can be moved to a **dead-letter queue** so one poison message does not block the queue. **Long polling** (`WaitTimeSeconds` up to 20) cuts empty responses and cost.

```python
import json
import boto3

sqs = boto3.client("sqs")
queue_url = "https://sqs.us-east-1.amazonaws.com/111122223333/orders"

sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps({"order_id": "A-1001"}))

resp = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=20)
for msg in resp.get("Messages", []):
    order = json.loads(msg["Body"])          # deserialize the payload
    # ... process the order ...
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])
```

**[📖 Amazon SQS visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)** - How retry and redelivery work

### Fault tolerance in code

Skill 1.1.3 asks for resilient applications, and the guide's examples are **retry with backoff** and **graceful degradation**. AWS SDKs retry throttled and transient errors automatically; for your own calls, retry with **exponential backoff and jitter** so many clients do not retry in lockstep. Degrade gracefully by serving cached or partial data when a dependency is down instead of failing the whole request. Make operations **idempotent** so a retry does not duplicate work (an idempotency key stored in DynamoDB is the usual pattern).

### Using the AWS APIs and SDKs

All services are APIs. The SDKs (boto3 for Python, the AWS SDK for JavaScript, Java and others) sign requests with credentials from the **default credential provider chain**: environment variables, then shared config files, then container or instance role credentials. In deployed code, use the role attached to the compute (Lambda execution role, ECS task role, EC2 instance profile); never embed access keys. The AWS CLI uses the same chain: `aws s3 ls`, `aws lambda invoke --function-name my-fn --payload '{"a":1}' --cli-binary-format raw-in-base64-out out.json`.

**Serialization** (skill 1.1.7) is turning your objects into bytes or text for a service, and back. JSON is the common format. DynamoDB's low-level API wraps values in type descriptors (`{"S": "abc"}`, `{"N": "42"}`); the SDKs' higher-level resource or document interfaces handle that conversion.

### APIs, streaming and events

**API Gateway** lets you create, extend and maintain APIs (skill 1.1.4). Know that it can validate requests against a model and transform requests and responses with mapping templates (REST APIs), and that it offers REST, HTTP and WebSocket API types. Event-driven patterns (skill 1.1.8) combine EventBridge rules, S3 Event Notifications, SQS and SNS: an object lands in S3, the event triggers a Lambda function, which publishes a result to SNS. **Streaming data** (skill 1.1.6) means Kinesis Data Streams for ordered, replayable records and Amazon Data Firehose for delivery to S3 and other destinations without writing consumer code. A Kinesis **partition key** decides which shard holds a record; records with the same key stay in order.

### New in C03: AI-assisted development and AI services

Skill 1.1.9 expects you to use AI-assisted development tools to generate, review and optimize code. The guide's examples are spec-driven code generation, automated code reviews, intelligent completion, refactoring suggestions and security scanning, and its in-scope services list names **Kiro** and Amazon Bedrock among the AI tools. The exam tests this as a developer workflow skill, so the principle matters more than a console click-path: AI output is a draft that you review, test and scan like any other contribution.

Skill 1.1.10 is integrating managed AWS AI services into applications. With Amazon Bedrock, application code calls a model through the Bedrock runtime API. The Converse API gives one request shape across models:

```python
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

response = bedrock.converse(
    modelId="MODEL_ID_FROM_YOUR_ACCOUNT",
    messages=[{"role": "user", "content": [{"text": "Summarize this support ticket in one sentence."}]}],
    inferenceConfig={"maxTokens": 200, "temperature": 0.2},
)
print(response["output"]["message"]["content"][0]["text"])
```

The out-of-scope list for this exam is explicit: selecting foundation models, engineering prompts and designing RAG architectures are not tested. What is tested is calling the service correctly, handling errors and throttling like any other API, and securing the interaction (see Domain 2, task 2.3).

**[📖 Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)** - The unified chat request and response format

## Task 1.2: Code for AWS Lambda

A Lambda function is code plus configuration. The configuration items the guide names (skill 1.2.2) are **memory** (which also scales CPU), **timeout**, **runtime**, **handler**, **environment variables**, **concurrency**, **layers** and **extensions**.

```python
import json
import os

TABLE = os.environ["TABLE_NAME"]          # configuration comes from environment variables

def handler(event, context):
    # event shape depends on the trigger; context holds request id and remaining time
    for record in event.get("Records", []):
        body = json.loads(record["body"])  # an SQS event source delivers a batch of records
        print({"order": body["order_id"], "table": TABLE})
    return {"batchItemFailures": []}       # report no failed items for the batch
```

Points the exam leans on:

- **Private resources** (1.2.1): a function reaches resources inside a VPC (such as an RDS instance) only when configured with VPC subnets and security groups. A function in a VPC loses default internet access unless the subnets route through a NAT gateway or you use VPC endpoints for AWS services.
- **Event lifecycle and errors** (1.2.3): synchronous invocations return errors to the caller. Asynchronous invocations are retried by Lambda, and you can send the outcome to a **destination** (success or failure, to SQS, SNS, EventBridge or another function) or to a **dead-letter queue**. Destinations are the newer, more capable option.
- **Event source mappings** (1.2.4): Lambda polls SQS, Kinesis and DynamoDB Streams on your behalf. Configure batch size, a batching window and, for streams, behavior on failure. For SQS, returning `batchItemFailures` lets only the failed messages return to the queue.
- Package functions as .zip archives or container images, and share dependencies with layers (Domain 3).

**[📖 Lambda event source mappings](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html)** - How Lambda polls queues and streams

## Task 1.3: Data stores during development

Choose the store by access pattern (skill 1.3.2):

| Need | Store |
|---|---|
| Key-value or document access at any scale, single-digit millisecond | Amazon DynamoDB |
| Relational queries, joins, transactions | Amazon RDS or Aurora |
| Objects: files, images, backups, data lake | Amazon S3 |
| Sub-millisecond reads for hot data, session store | Amazon ElastiCache |

**Data lifecycle** (1.3.1): S3 Lifecycle policies move or expire objects by age; DynamoDB **TTL** deletes items whose epoch-timestamp attribute has passed; retention periods apply to logs and backups.

**Caching** (1.3.3): with ElastiCache in front of a database, **lazy loading** (read the cache, on a miss read the database and populate the cache) keeps only requested data but can serve stale data, while **write-through** updates the cache on every write so it stays fresh at the price of more writes. For DynamoDB, DAX is a read-through cache with the same API.

### DynamoDB essentials (one consolidated skill in C03)

C03 folds four separate DynamoDB skills into one (1.3.4): partition key design, consistency models, query versus scan, and keys and indexes.

- **Primary key.** A simple key is a partition key. A composite key adds a sort key. Pick a **high-cardinality partition key** (many distinct values, evenly accessed) so load spreads across partitions; a key like a status flag creates a hot partition.
- **Consistency.** Reads are **eventually consistent** by default; request a **strongly consistent** read when you need the latest write (it costs more and is not available on global secondary indexes).
- **Query versus Scan.** `Query` reads items for a partition key (optionally narrowed by a sort-key condition) and is efficient. `Scan` reads the whole table and filters afterwards, so it is slow and costly on large tables.
- **Indexes.** A **global secondary index (GSI)** gives a different partition and sort key and can be added any time; a **local secondary index (LSI)** shares the table's partition key with a different sort key and must be created with the table.

```bash
aws dynamodb query \
  --table-name Orders \
  --key-condition-expression "CustomerId = :c AND OrderDate >= :d" \
  --expression-attribute-values '{":c": {"S": "C-100"}, ":d": {"S": "2026-01-01"}}'
```

**[📖 DynamoDB Query](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html)** - Key conditions, filters and pagination
**[📖 DynamoDB read consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)** - Eventual versus strong consistency

## What changed from C02 in this domain

- **Added:** AI-assisted development tools (1.1.9) and managed AI service integration (1.1.10).
- **Structure:** C03 has three tasks in this domain. This repo's C02 guide lists a fourth C02 area, using APIs in application development; the C03 outline carries API and SDK skills inside task 1.1 (1.1.4 and 1.1.5).
- **Merged:** four DynamoDB skills became one (1.3.4).
- **Moved:** serialization into 1.1.7; unit testing with SAM to Domain 3; Lambda performance tuning to Domain 4.
- **Weight:** 32 percent to 30 percent.

## Key terms

- **Loose coupling** - a design in which components interact through a managed intermediary so each can scale and fail independently.
- **Visibility timeout** - the period after an SQS message is received during which other consumers cannot receive it.
- **Dead-letter queue** - a queue that receives messages or events that could not be processed successfully after the allowed attempts.
- **Exponential backoff** - increasing the wait between retries, usually with random jitter, to avoid retry storms.
- **Idempotent operation** - an operation that has the same effect whether it is applied once or several times.
- **Kinesis partition key** - the value that determines which shard stores a record and so the ordering scope.
- **Lambda destination** - a target such as SQS, SNS, EventBridge or another function that receives the result of an asynchronous invocation.
- **Event source mapping** - a Lambda resource that polls a queue or stream and invokes the function with batches of records.
- **Lambda layer** - a .zip archive of libraries or other dependencies that functions can share.
- **DynamoDB TTL** - a setting that deletes items automatically after the time stored in a designated attribute.
- **Partition key** - the DynamoDB key attribute whose value determines where an item is stored; high cardinality spreads load.
- **Global secondary index** - a DynamoDB index with its own partition and sort key that can be added after table creation.
- **Strongly consistent read** - a DynamoDB read that returns the result of all prior successful writes, at higher cost.
- **Lazy loading** - a caching pattern that populates the cache only when a read misses.
- **Write-through cache** - a caching pattern that updates the cache whenever the database is written.
- **Bedrock Converse API** - a Bedrock runtime operation that provides one consistent chat request format across supported models.
