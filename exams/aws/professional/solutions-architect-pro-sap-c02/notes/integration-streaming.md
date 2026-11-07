# Integration & Streaming

## Overview

Enterprise integration and streaming architectures enable loosely coupled, event-driven systems that scale independently and process data in real-time. At the professional level, you must design messaging and streaming solutions that handle millions of events per second, ensure message durability and ordering, implement backpressure handling, and integrate disparate systems across AWS, on-premises, and third-party services.

Professional architects must understand the trade-offs between synchronous and asynchronous communication, choose appropriate messaging patterns (pub/sub, queuing, streaming), design for exactly-once or at-least-once delivery, and implement complex event processing workflows.

## Key Concepts

### Messaging Services

**Amazon SQS (Simple Queue Service)**
- **Standard Queue**: At-least-once delivery, best-effort ordering, unlimited throughput
- **FIFO Queue**: Exactly-once processing, strict ordering, up to 3,000 messages/second (300/second without batching)
- **Message Attributes**: Metadata (up to 10 attributes)
- **Message Size**: Up to 256 KB (Extended Client Library for larger via S3)
- **Visibility Timeout**: Hide message while processing (0 seconds to 12 hours, default 30 seconds)
- **Retention**: 1 minute to 14 days (default 4 days)
- **Long Polling**: Reduce empty responses (1-20 seconds wait time)
- **Dead Letter Queue (DLQ)**: Failed messages after max receives
- **Delay Queue**: Postpone delivery (0-15 minutes)
- **Use Cases**: Decoupling services, buffering requests, batch processing, work queues

**Amazon SNS (Simple Notification Service)**
- **Pub/Sub Model**: 1-to-many message delivery
- **Topic Types**:
  - **Standard**: Best-effort ordering, at-least-once delivery
  - **FIFO**: Strict ordering, exactly-once delivery
- **Subscribers**: SQS, Lambda, HTTP/HTTPS, email, SMS, mobile push
- **Message Filtering**: Filter messages by attributes (reduce noise, cost)
- **Message Size**: Up to 256 KB
- **Fan-Out Pattern**: SNS → Multiple SQS queues
- **Use Cases**: Application alerts, mobile push notifications, fan-out to multiple services

**Amazon MQ (Managed ActiveMQ and RabbitMQ)**
- **Protocols**: AMQP, MQTT, OpenWire, STOMP, WebSocket
- **Use Cases**: Lift-and-shift from on-premises message brokers, protocol compatibility
- **High Availability**: Active/standby deployment across AZs
- **Limitations**: Not serverless, requires provisioned instances
- **When to Use**: Existing applications using JMS, AMQP, MQTT (otherwise prefer SQS/SNS)

### Event Services

**Amazon EventBridge**
- **Event Bus**: Default, custom, partner event buses
- **Event Sources**: AWS services, custom applications, SaaS partners
- **Event Rules**: Filter and route events to targets
- **Targets**: Lambda, Step Functions, SQS, SNS, Kinesis, ECS tasks, API destinations, etc.
- **Schema Registry**: Discover and version event schemas
- **Archive and Replay**: Store events for replay
- **Cross-Account Events**: Send/receive events across accounts
- **Use Cases**: Serverless workflows, cross-account architectures, SaaS integrations

**AWS AppSync**
- **GraphQL API**: Real-time data synchronization
- **Data Sources**: DynamoDB, Lambda, RDS, HTTP, OpenSearch
- **Subscriptions**: Real-time updates via WebSocket
- **Offline Support**: Local data caching and synchronization
- **Use Cases**: Mobile and web applications, real-time dashboards, collaborative apps

### Streaming Services

**Amazon Kinesis Data Streams**
- **Real-Time Streaming**: Ingest and process data streams
- **Shards**: Throughput units (1 MB/s ingress, 2 MB/s egress per shard)
- **Retention**: 24 hours default, up to 365 days
- **Ordering**: Per partition key within shard
- **Provisioned Mode**: Specify shard count
- **On-Demand Mode**: Auto-scaling (up to 200 MB/s and 200,000 records/second)
- **Enhanced Fan-Out**: 2 MB/s per consumer per shard (push model)
- **KCL (Kinesis Client Library)**: Build consumer applications with checkpointing
- **Use Cases**: Real-time analytics, log processing, clickstream, IoT telemetry

**Amazon Kinesis Data Firehose**
- **Near Real-Time**: Delivery to S3, Redshift, OpenSearch, HTTP endpoints, Splunk
- **Buffer**: Time (60-900 seconds) or size (1-128 MB)
- **Transformation**: Lambda for data transformation
- **Compression**: GZIP, ZIP, Snappy, Hadoop-compatible Snappy
- **Partitioning**: Dynamic partitioning for S3 (by time, custom)
- **No Shard Management**: Fully managed, auto-scaling
- **Use Cases**: Log delivery to S3/OpenSearch, streaming ETL, data lake ingestion

**Amazon Kinesis Data Analytics**
- **SQL Queries**: Real-time analytics on streaming data
- **Apache Flink**: Java, Scala, Python for complex processing
- **Sources**: Kinesis Data Streams, Kinesis Data Firehose
- **Destinations**: Kinesis Data Streams, Kinesis Data Firehose, Lambda
- **Use Cases**: Real-time dashboards, anomaly detection, streaming ETL

**Amazon Managed Streaming for Apache Kafka (MSK)**
- **Apache Kafka**: Distributed streaming platform
- **Fully Managed**: Cluster creation, configuration, patching, Kafka versions
- **Provisioned Mode**: Choose broker instance types and count
- **Serverless Mode**: Auto-scaling, pay per throughput
- **High Availability**: Multi-AZ deployment
- **Integrations**: Kafka Connect (source/sink connectors), Schema Registry
- **Security**: IAM, TLS, SASL/SCRAM
- **Use Cases**: Kafka workloads requiring specific Kafka features, large-scale event streaming

### Orchestration and Workflow

**AWS Step Functions**
- **State Machine**: Coordinate distributed applications
- **Standard Workflows**: Long-running (up to 1 year), exactly-once execution
- **Express Workflows**: Short-duration (up to 5 minutes), high-volume (100K/second), at-least-once
- **States**: Task, Choice, Parallel, Wait, Map, Pass, Succeed, Fail
- **Integrations**: Lambda, ECS/Fargate, Batch, DynamoDB, SNS, SQS, Glue, SageMaker, EMR
- **Error Handling**: Retry, catch, fallback
- **Human Approval**: Callback tasks for manual approval
- **Use Cases**: Order processing, ETL pipelines, microservices orchestration, ML workflows

**Amazon EventBridge Scheduler**
- **Cron and Rate Expressions**: Schedule one-time or recurring tasks
- **Targets**: Lambda, Step Functions, SQS, SNS, ECS, EventBridge
- **Flexible Delivery Windows**: Execute within time window
- **Retry**: Automatic retry on failure
- **Use Cases**: Scheduled Lambda invocations, periodic data processing, maintenance tasks

### API Integration

**Amazon API Gateway**
- **REST API**: Regional, edge-optimized (CloudFront), private (VPC)
- **HTTP API**: Lower latency, lower cost, simpler (no usage plans, API keys)
- **WebSocket API**: Two-way communication
- **Integrations**: Lambda, HTTP, AWS services, VPC Link (private resources)
- **Authorization**: IAM, Cognito, Lambda authorizers
- **Throttling**: Rate limiting (10,000 requests/second)
- **Caching**: Response caching (0.5 GB to 237 GB)
- **Usage Plans and API Keys**: Monetization, quotas
- **Use Cases**: Serverless APIs, microservices gateway, mobile backends

**AWS App Mesh (retired, history only: end of support 2026-09-30; AWS recommends ECS Service Connect)**
- **Service Mesh**: Manage microservices communication
- **Observability**: Metrics, logs, traces for service-to-service traffic
- **Traffic Control**: Routing, retries, timeouts, circuit breakers
- **Compatible**: ECS, EKS, EC2, Fargate
- **Envoy Proxy**: Sidecar proxy for each service
- **Use Cases**: Microservices on ECS/EKS, A/B testing, canary deployments

### Data Transfer and Integration

**AWS DataSync**
- **Automated Transfer**: On-premises ↔ AWS (S3, EFS, FSx)
- **Protocols**: NFS, SMB, HDFS, S3
- **Bandwidth Throttling**: Schedule transfers, limit impact
- **Validation**: Verify data integrity
- **Use Cases**: Migration, archival, DR, hybrid workflows

**AWS Transfer Family**
- **Protocols**: SFTP, FTPS, FTP, AS2
- **Storage**: S3, EFS
- **Authentication**: Service-managed, Active Directory, custom (Lambda)
- **Use Cases**: B2B file transfers, legacy application integration, EDI

**AWS AppFlow**
- **SaaS Integration**: Bidirectional data flow between AWS and SaaS
- **Sources/Destinations**: Salesforce, SAP, Slack, ServiceNow, S3, Redshift, Snowflake
- **Transformations**: Mapping, filtering, validation
- **Encryption**: In transit and at rest
- **Use Cases**: SaaS data integration, analytics, customer 360

## AWS Services Reference

### Core Services

**Amazon SQS**
- Managed message queuing service
- Standard (at-least-once) and FIFO (exactly-once)
- Unlimited throughput (Standard), 3,000 msg/sec (FIFO)
- DLQ for failed messages

**Amazon SNS**
- Pub/sub messaging service
- Fan-out to multiple subscribers
- Standard and FIFO topics
- Message filtering by attributes

**Amazon EventBridge**
- Serverless event bus
- 90+ AWS service integrations
- Schema registry and archive
- Cross-account event routing

**Amazon Kinesis Data Streams**
- Real-time data streaming
- Shard-based throughput
- 24 hours to 365 days retention
- Enhanced fan-out for consumers

**Amazon Kinesis Data Firehose**
- Near real-time delivery
- S3, Redshift, OpenSearch, HTTP
- Auto-scaling, no shard management
- Lambda transformation

### Supporting Services

**AWS Step Functions**
- Serverless workflow orchestration
- Standard and Express workflows
- Visual workflow designer
- Error handling and retries

**Amazon MSK**
- Managed Apache Kafka
- Provisioned and serverless
- Kafka Connect and Schema Registry
- Multi-AZ for HA

**AWS AppSync**
- Managed GraphQL service
- Real-time subscriptions
- Offline data sync
- Multiple data sources

**Amazon API Gateway**
- Create, publish, manage APIs
- REST, HTTP, WebSocket
- Throttling, caching, authorization
- VPC Link for private resources

**Amazon MQ**
- Managed ActiveMQ and RabbitMQ
- JMS, AMQP, MQTT protocols
- Active/standby HA
- Lift-and-shift from on-premises

**AWS DataSync**
- Automated data transfer
- On-premises to AWS
- Bandwidth throttling
- Data validation

**AWS Transfer Family**
- Managed SFTP, FTPS, FTP, AS2
- S3 and EFS storage
- Custom authentication
- B2B file transfers

## Architecture Patterns

### Pattern 1: Event-Driven Microservices with EventBridge

**Use Case**
- E-commerce platform with order processing, inventory, shipping, notifications
- Loosely coupled services
- Event-driven architecture
- Asynchronous communication

**Implementation Approach**
1. **Event Bus**: Custom EventBridge bus for e-commerce domain
2. **Event Producers**: Order service publishes "OrderPlaced" event
3. **Event Consumers**:
   - Inventory service: Reserve inventory
   - Payment service: Process payment
   - Shipping service: Create shipment
   - Notification service: Send confirmation email
4. **Event Rules**: Filter events to specific consumers (e.g., OrderPlaced → Inventory, Payment, Shipping, Notification)
5. **Targets**: Lambda functions or ECS tasks
6. **Error Handling**: DLQ for failed events, retry policies
7. **Archive**: Store events for audit and replay
8. **Schema Registry**: Version event schemas

**Pros/Cons**
- Pros: Loose coupling, independent scaling, easy to add consumers, event history
- Cons: Eventual consistency, debugging complexity, event schema versioning

### Pattern 2: Real-Time Analytics Pipeline with Kinesis

**Use Case**
- IoT platform ingesting 1M events/second
- Real-time dashboards and alerting
- Historical analytics in data lake

**Implementation Approach**
1. **Ingestion**: Kinesis Data Streams (on-demand mode, auto-scaling)
2. **Real-Time Processing**: Kinesis Data Analytics (Apache Flink) for aggregations, windowing
3. **Alerting**: Lambda consumers for threshold detection → SNS for alerts
4. **Storage**: Kinesis Data Firehose → S3 (Parquet format, partitioned by date)
5. **Analytics**: Athena for ad-hoc queries, QuickSight for dashboards
6. **Retention**: Kinesis Data Streams (7 days for replay), S3 (indefinite with lifecycle to Glacier)
7. **Monitoring**: CloudWatch metrics for incoming records, iterator age, throttled records

**Pros/Cons**
- Pros: Real-time processing, high throughput (millions/second), data lake for historical analysis
- Cons: Shard management (provisioned mode), cost at high scale, complexity

### Pattern 3: Fan-Out Pattern with SNS and SQS

**Use Case**
- Video processing platform
- Upload triggers multiple independent processing tasks
- Each task processes at different speeds

**Implementation Approach**
1. **Trigger**: S3 event notification → SNS topic
2. **Fan-Out**: SNS subscriptions to multiple SQS queues
   - Thumbnail queue → Lambda
   - Transcoding queue → ECS tasks
   - Metadata extraction queue → Lambda
   - Analytics queue → Kinesis Firehose
3. **Processing**: Each queue consumed independently
4. **Visibility Timeout**: 5 minutes for thumbnails, 1 hour for transcoding (adjust based on processing time)
5. **DLQ**: Capture failed messages after 3 retries
6. **Scaling**: SQS queue depth triggers auto-scaling for ECS tasks

**Pros/Cons**
- Pros: Parallel processing, independent scaling, fault isolation, retry logic
- Cons: SNS does not guarantee ordering (use FIFO if needed), duplication possible with standard queues

### Pattern 4: Saga Pattern with Step Functions

**Use Case**
- Travel booking requiring flight, hotel, car rental reservations
- Distributed transactions across multiple services
- Compensating transactions on failure

**Implementation Approach**
1. **Step Functions State Machine**: Orchestrate booking workflow
2. **Steps**:
   - Reserve flight (Lambda → Flight service API)
   - Reserve hotel (Lambda → Hotel service API)
   - Reserve car (Lambda → Car service API)
   - Confirm booking (Lambda → Send confirmation)
3. **Error Handling**: Catch failures at each step
4. **Compensating Transactions**: Cancel reservations on failure
   - If hotel reservation fails → Cancel flight
   - If car reservation fails → Cancel hotel and flight
5. **Retry**: Retry transient errors (3 attempts with exponential backoff)
6. **Human Approval**: Callback task for manual approval (optional)
7. **Monitoring**: CloudWatch metrics, X-Ray for distributed tracing

**Pros/Cons**
- Pros: Visual workflow, error handling, compensating transactions, audit trail
- Cons: Complexity, eventual consistency, no ACID guarantees

### Pattern 5: Message Buffering with SQS

**Use Case**
- API receives 10K requests/second
- Backend can only process 1K requests/second
- Prevent backend overload and lost requests

**Implementation Approach**
1. **API Layer**: API Gateway → Lambda → SQS
2. **Queue**: Standard SQS queue (unlimited throughput)
3. **Consumers**: Lambda or ECS tasks reading from queue
4. **Auto Scaling**: Target tracking on SQS ApproximateNumberOfMessagesVisible metric
5. **Visibility Timeout**: Set to processing time + buffer (e.g., 5 minutes)
6. **DLQ**: Capture messages that fail after 5 retries
7. **Monitoring**: Queue depth, age of oldest message, dead letter queue depth

**Backpressure Handling**
- Queue absorbs bursts (10K/second → queue)
- Consumers process at sustainable rate (1K/second)
- No lost messages, no backend overload

**Pros/Cons**
- Pros: Decouple producer and consumer rates, prevent overload, no lost messages
- Cons: Increased latency (queue wait time), need to monitor queue depth

### Pattern 6: Stream Processing with Kafka (MSK)

**Use Case**
- Financial services processing stock trades
- Exactly-once semantics required
- Complex stream processing (joins, aggregations, windowing)
- Kafka ecosystem tools (Kafka Connect, KSQL)

**Implementation Approach**
1. **MSK Cluster**: 3 brokers across 3 AZs (HA)
2. **Topics**: Trades topic (partitioned by stock symbol)
3. **Producers**: Trading systems publishing to Kafka
4. **Stream Processing**: Kafka Streams or Apache Flink on ECS/EKS
5. **Consumers**: Multiple consumer groups for different use cases
   - Real-time dashboard (Kafka → Lambda → DynamoDB → API Gateway)
   - Analytics (Kafka Connect → S3 → Athena)
   - Compliance (Kafka → S3 with immutable storage)
6. **Schema Management**: MSK Schema Registry for schema evolution
7. **Security**: IAM authentication, TLS in transit, encryption at rest
8. **Monitoring**: CloudWatch metrics, Kafka broker metrics, consumer lag

**Pros/Cons**
- Pros: Exactly-once semantics, rich ecosystem, complex processing, high throughput
- Cons: Higher operational complexity than Kinesis, requires Kafka expertise, cost

## Best Practices

### Enterprise-Level Recommendations

**Choosing the Right Service**
- **Pub/Sub (1-to-many)**: SNS, EventBridge
- **Queue (1-to-1, buffering)**: SQS
- **Streaming (real-time, ordering)**: Kinesis, MSK
- **Workflow orchestration**: Step Functions
- **API gateway**: API Gateway
- **Data transfer**: DataSync, Transfer Family, AppFlow

**Asynchronous Communication**
- Prefer asynchronous over synchronous for loose coupling
- Use queues for buffering and backpressure
- Use pub/sub for fan-out and decoupling
- Use streaming for real-time and ordering requirements

**Error Handling**
- Dead Letter Queues for failed messages
- Retry with exponential backoff
- Idempotent consumers (handle duplicates)
- Monitoring and alerting on DLQ depth

**Message Durability**
- SQS persists messages across multiple servers
- Kinesis replicates across 3 AZs
- MSK replicates based on replication factor (default 3)
- SNS does not persist messages (deliver or fail)

**Ordering**
- SQS FIFO for strict ordering (use message group ID)
- Kinesis ordering per partition key within shard
- Kafka ordering per partition
- SNS FIFO for ordered fan-out

### Security Considerations

**Encryption**
- At rest: SQS, SNS, Kinesis, MSK support KMS encryption
- In transit: TLS for all services
- MSK: Client-broker and broker-broker TLS

**Access Control**
- IAM policies for service access
- SQS/SNS: Resource-based policies for cross-account
- Kinesis: IAM roles for producers and consumers
- MSK: IAM authentication or SASL/SCRAM
- EventBridge: Resource-based policies for cross-account events

**VPC Integration**
- SQS, SNS, Kinesis: VPC endpoints for private access
- MSK: Deployed in VPC
- API Gateway: Private APIs in VPC

**Compliance**
- Message retention and archival for audit
- EventBridge archive for event replay
- CloudTrail for API activity logging
- Immutable message storage (S3 Object Lock)

### Cost Optimization

**SQS**
- Long polling to reduce empty responses (cost: $0.40/million requests)
- Batch operations (up to 10 messages per request)
- Standard vs. FIFO (FIFO is 2x cost)

**SNS**
- Message filtering to reduce unnecessary deliveries
- Cost: $0.50/million publishes, $0.09/GB data transfer

**Kinesis Data Streams**
- On-demand vs. provisioned (provisioned cheaper for predictable traffic)
- Right-size shard count
- Data retention cost (24 hours free, extended retention $0.023/shard-hour)

**Kinesis Data Firehose**
- Cost: $0.029/GB ingested (no shard management)
- Compression to reduce S3 storage costs

**MSK**
- Provisioned: Choose right broker instance types
- Serverless: Pay per throughput (better for variable workloads)
- Storage cost: $0.10/GB-month

**Step Functions**
- Express workflows cheaper than Standard for high-volume, short-duration
- Standard: $0.025/1K state transitions
- Express: $1.00/million requests + $0.06/GB-hour duration

### Performance Tuning

**SQS**
- Long polling (reduce latency and empty responses)
- Batch operations (up to 10 messages)
- Multiple consumers for parallel processing
- Visibility timeout = processing time + buffer

**Kinesis**
- Partition key distribution (avoid hot shards)
- Enhanced fan-out for dedicated throughput per consumer
- Batch GetRecords (up to 10 MB or 10,000 records)
- On-demand mode for auto-scaling

**MSK**
- Partition strategy for even load distribution
- Increase partitions for higher throughput
- Tune producer/consumer configs (batch size, linger time, fetch size)
- Monitor consumer lag

**EventBridge**
- Message filtering to reduce target invocations
- Batch targets for SQS/Kinesis (reduce API calls)
- Archive only necessary events (cost optimization)

## Common Scenarios

### Scenario 1: E-Commerce Order Processing

**Context**: E-commerce platform processing 10K orders/hour with multiple downstream systems

**Architecture**
1. **Order API**: API Gateway → Lambda → SQS (order queue)
2. **Order Processing**: Lambda consuming from SQS
   - Validate order
   - Reserve inventory (Lambda → DynamoDB)
   - Process payment (Lambda → Payment gateway)
   - Publish "OrderConfirmed" event to EventBridge
3. **EventBridge**: Route events to downstream services
   - Shipping service: Lambda creates shipment
   - Email service: Lambda sends confirmation via SES
   - Analytics: Kinesis Firehose → S3 → Athena
   - CRM: Lambda updates Salesforce via AppFlow
4. **Error Handling**: DLQ for failed orders, Step Functions for complex error scenarios
5. **Monitoring**: CloudWatch metrics, X-Ray for distributed tracing

**Key Considerations**
- SQS buffers API spikes (10K/hour → 100K/hour during flash sales)
- EventBridge decouples order processing from downstream services
- Idempotent consumers (check if order already processed)
- DLQ for manual intervention (payment failures, inventory issues)

### Scenario 2: Real-Time IoT Data Processing

**Context**: 100K IoT devices sending temperature readings every 10 seconds (10K events/second)

**Architecture**
1. **Ingestion**: AWS IoT Core → Kinesis Data Streams (10 shards, 1K events/sec/shard)
2. **Real-Time Processing**: Kinesis Data Analytics (Apache Flink)
   - Tumbling window (1 minute) aggregations (avg, min, max)
   - Anomaly detection (temperature > threshold)
3. **Alerting**: Kinesis Data Analytics → Lambda → SNS (SMS/email alerts)
4. **Storage**:
   - Hot data (24 hours): Kinesis → DynamoDB (device ID, last reading)
   - Warm data (7 days): Kinesis Data Firehose → S3 (Parquet)
   - Cold data (>7 days): S3 lifecycle to Glacier
5. **Analytics**: Athena for historical queries, QuickSight for dashboards
6. **Monitoring**: CloudWatch alarms for Kinesis iterator age, throttled records

**Key Considerations**
- Partition key: Device ID (even distribution across shards)
- Enhanced fan-out for multiple consumers (analytics, alerting, storage)
- Data retention: 7 days in Kinesis for replay
- Cost: 10K events/sec * 86,400 sec/day * 30 days * $0.015/million = $3,888/month

### Scenario 3: Microservices Saga with Step Functions

**Context**: Travel booking platform coordinating flight, hotel, car reservations

**Workflow**
1. **Input**: User submits booking request (flight, hotel, car details)
2. **Step 1**: Reserve flight (Lambda → Flight API)
   - Success → Proceed to Step 2
   - Failure → Return error to user
3. **Step 2**: Reserve hotel (Lambda → Hotel API)
   - Success → Proceed to Step 3
   - Failure → Cancel flight → Return error
4. **Step 3**: Reserve car (Lambda → Car API)
   - Success → Proceed to Step 4
   - Failure → Cancel hotel and flight → Return error
5. **Step 4**: Process payment (Lambda → Payment gateway)
   - Success → Confirm all reservations
   - Failure → Cancel car, hotel, flight → Return error
6. **Output**: Booking confirmation or failure reason

**Error Handling**
- Each step has retry policy (3 attempts, exponential backoff)
- Catch block for each step invokes compensating Lambda
- DLQ for persistent failures
- CloudWatch alarms for high failure rates

**Key Considerations**
- Idempotent APIs (handle duplicate reservation requests)
- Timeout for each step (30 seconds for API calls)
- Human approval for high-value bookings (>$10K)
- X-Ray for distributed tracing across services

### Scenario 4: Video Processing Pipeline

**Context**: Video platform processing 1K uploads/day, each requiring thumbnail, transcoding, metadata extraction

**Architecture**
1. **Upload**: S3 upload → S3 event notification → SNS topic
2. **Fan-Out**: SNS → 3 SQS queues
   - Thumbnail queue
   - Transcode queue
   - Metadata queue
3. **Processing**:
   - **Thumbnails**: Lambda (quick, <1 minute)
   - **Transcoding**: ECS tasks on Spot (long-running, 10-60 minutes)
   - **Metadata**: Lambda with Rekognition (labels, text detection)
4. **Orchestration**: Step Functions for workflow management
   - Wait for all tasks to complete
   - Update DynamoDB with processing status
   - Publish "VideoReady" event to EventBridge
5. **Scaling**: ECS Auto Scaling based on transcode queue depth
6. **Error Handling**: DLQ for failed tasks, retry 3 times

**Cost Optimization**
- Spot instances for transcoding (70% cost savings)
- Lambda for short tasks (thumbnails, metadata)
- S3 Intelligent-Tiering for processed videos

### Scenario 5: Financial Trading Platform with MSK

**Context**: High-frequency trading platform processing 100K trades/second

**Architecture**
1. **Ingestion**: Trading systems → MSK (100 partitions for parallelism)
2. **Stream Processing**: Apache Flink on EKS
   - Real-time P&L calculations
   - Risk management (position limits, exposure)
   - Market data aggregation (OHLC bars)
3. **Storage**:
   - Kafka → S3 (immutable audit trail, 7-year retention)
   - Kafka Connect S3 sink connector (Avro format)
4. **Real-Time Analytics**: Kafka → Lambda → DynamoDB → API Gateway
5. **Compliance**: All trades logged to S3 with Object Lock (WORM)
6. **Monitoring**: MSK metrics, consumer lag, Flink job metrics

**Key Considerations**
- Exactly-once semantics (transactional writes to Kafka)
- Partition by stock symbol (related trades in same partition)
- MSK Schema Registry for schema evolution
- Retention: 7 days in Kafka, indefinite in S3
- Security: IAM auth, TLS, encryption at rest

### Scenario 6: Multi-Account Event-Driven Architecture

**Context**: Enterprise with 50 AWS accounts requiring centralized event bus

**Architecture**
1. **Accounts**: Development, Staging, Production accounts
2. **Event Bus**:
   - Central EventBridge bus in shared services account
   - Cross-account event delivery from all accounts
3. **Event Flow**:
   - Application accounts publish events to central bus
   - Central bus routes to targets based on rules
4. **Targets**:
   - Security events → Security account (GuardDuty, Security Hub)
   - Backup events → Backup account
   - Application events → Application-specific accounts
5. **Event Filtering**: Rules filter events by source, detail-type, attributes
6. **Archive**: Central event archive for audit and replay
7. **Monitoring**: CloudWatch metrics, alarms for failed invocations

**Security Considerations**
- IAM policies for cross-account PutEvents
- Event bus resource policy allowing specific accounts
- Encryption in transit and at rest
- CloudTrail for event audit

## AWS CLI Examples

```bash
# SQS - Create standard queue
aws sqs create-queue \
  --queue-name orders-queue \
  --attributes VisibilityTimeout=300,MessageRetentionPeriod=1209600,ReceiveMessageWaitTimeSeconds=20

# SQS - Create FIFO queue
aws sqs create-queue \
  --queue-name orders-queue.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=true,VisibilityTimeout=300

# SQS - Create dead letter queue
aws sqs create-queue --queue-name orders-dlq

aws sqs set-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/orders-queue \
  --attributes '{"RedrivePolicy":"{\"deadLetterTargetArn\":\"arn:aws:sqs:us-east-1:123456789012:orders-dlq\",\"maxReceiveCount\":\"3\"}"}'

# SQS - Send message
aws sqs send-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/orders-queue \
  --message-body '{"orderId":"12345","customerId":"789","items":[{"productId":"A1","quantity":2}]}' \
  --message-attributes '{"Priority":{"DataType":"String","StringValue":"High"}}'

# SQS - Receive messages
aws sqs receive-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/orders-queue \
  --max-number-of-messages 10 \
  --wait-time-seconds 20 \
  --attribute-names All \
  --message-attribute-names All

# SQS - Delete message
aws sqs delete-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/orders-queue \
  --receipt-handle <receipt-handle>

# SNS - Create topic
aws sns create-topic --name video-processing --attributes DisplayName="Video Processing"

# SNS - Create FIFO topic
aws sns create-topic \
  --name orders-topic.fifo \
  --attributes FifoTopic=true,ContentBasedDeduplication=true

# SNS - Subscribe SQS to SNS
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:video-processing \
  --protocol sqs \
  --notification-endpoint arn:aws:sqs:us-east-1:123456789012:thumbnail-queue

# SNS - Publish message
aws sns publish \
  --topic-arn arn:aws:sns:us-east-1:123456789012:video-processing \
  --message '{"videoId":"vid123","bucket":"videos","key":"uploads/video.mp4"}' \
  --subject "New Video Upload" \
  --message-attributes '{"ProcessingType":{"DataType":"String","StringValue":"Standard"}}'

# SNS - Add message filtering
aws sns set-subscription-attributes \
  --subscription-arn arn:aws:sns:us-east-1:123456789012:video-processing:abc-123 \
  --attribute-name FilterPolicy \
  --attribute-value '{"ProcessingType":["Standard","High"]}'

# EventBridge - Create custom event bus
aws events create-event-bus --name ecommerce-events

# EventBridge - Create rule
aws events put-rule \
  --name order-confirmed-rule \
  --event-bus-name ecommerce-events \
  --event-pattern '{"source":["order-service"],"detail-type":["OrderConfirmed"]}' \
  --state ENABLED

# EventBridge - Add target to rule
aws events put-targets \
  --rule order-confirmed-rule \
  --event-bus-name ecommerce-events \
  --targets Id=1,Arn=arn:aws:lambda:us-east-1:123456789012:function:send-confirmation-email

# EventBridge - Put events
aws events put-events \
  --entries '[
    {
      "EventBusName": "ecommerce-events",
      "Source": "order-service",
      "DetailType": "OrderConfirmed",
      "Detail": "{\"orderId\":\"12345\",\"customerId\":\"789\",\"total\":99.99}"
    }
  ]'

# Kinesis Data Streams - Create stream (on-demand)
aws kinesis create-stream \
  --stream-name iot-telemetry \
  --stream-mode-details StreamMode=ON_DEMAND

# Kinesis Data Streams - Create stream (provisioned)
aws kinesis create-stream \
  --stream-name clickstream \
  --shard-count 10

# Kinesis - Put record
aws kinesis put-record \
  --stream-name iot-telemetry \
  --partition-key device-12345 \
  --data '{"deviceId":"device-12345","temperature":72.5,"timestamp":"2025-01-10T12:00:00Z"}' \
  --cli-binary-format raw-in-base64-out

# Kinesis - Put records (batch)
aws kinesis put-records \
  --stream-name iot-telemetry \
  --records file://records.json

# Kinesis - Get shard iterator
aws kinesis get-shard-iterator \
  --stream-name iot-telemetry \
  --shard-id shardId-000000000000 \
  --shard-iterator-type LATEST

# Kinesis - Get records
aws kinesis get-records \
  --shard-iterator <shard-iterator>

# Kinesis Data Firehose - Create delivery stream
aws firehose create-delivery-stream \
  --delivery-stream-name logs-to-s3 \
  --delivery-stream-type DirectPut \
  --s3-destination-configuration file://s3-config.json

# s3-config.json:
# {
#   "RoleARN": "arn:aws:iam::123456789012:role/FirehoseDeliveryRole",
#   "BucketARN": "arn:aws:s3:::my-logs-bucket",
#   "Prefix": "logs/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/",
#   "BufferingHints": {"SizeInMBs": 5, "IntervalInSeconds": 300},
#   "CompressionFormat": "GZIP",
#   "EncryptionConfiguration": {
#     "KMSEncryptionConfig": {"AWSKMSKeyARN": "arn:aws:kms:us-east-1:123456789012:key/12345678"}
#   }
# }

# Firehose - Put record
aws firehose put-record \
  --delivery-stream-name logs-to-s3 \
  --record Data='{"timestamp":"2025-01-10T12:00:00Z","level":"INFO","message":"User login successful"}'

# MSK - Create cluster (provisioned)
aws kafka create-cluster \
  --cluster-name production-kafka \
  --broker-node-group-info file://broker-config.json \
  --kafka-version 3.5.1 \
  --number-of-broker-nodes 3 \
  --encryption-info EncryptionAtRest={DataVolumeKMSKeyId=arn:aws:kms:us-east-1:123456789012:key/12345678} \
  --client-authentication Sasl={Iam={Enabled=true}}

# MSK - Create serverless cluster
aws kafka create-cluster-v2 \
  --cluster-name serverless-kafka \
  --serverless Serverless={VpcConfigs=[{SubnetIds=[subnet-11111111,subnet-22222222],SecurityGroupIds=[sg-12345678]}]} \
  --kafka-version 3.5.1

# Step Functions - Create state machine
aws stepfunctions create-state-machine \
  --name travel-booking-workflow \
  --definition file://state-machine.json \
  --role-arn arn:aws:iam::123456789012:role/StepFunctionsExecutionRole

# Step Functions - Start execution
aws stepfunctions start-execution \
  --state-machine-arn arn:aws:states:us-east-1:123456789012:stateMachine:travel-booking-workflow \
  --name booking-12345 \
  --input '{"flightId":"FL123","hotelId":"HT456","carId":"CR789","customerId":"customer-999"}'

# API Gateway - Create REST API
aws apigateway create-rest-api \
  --name ecommerce-api \
  --description "E-commerce API" \
  --endpoint-configuration types=REGIONAL

# API Gateway - Create HTTP API
aws apigatewayv2 create-api \
  --name ecommerce-http-api \
  --protocol-type HTTP \
  --target arn:aws:lambda:us-east-1:123456789012:function:api-handler

# DataSync - Create task
aws datasync create-task \
  --source-location-arn arn:aws:datasync:us-east-1:123456789012:location/loc-onprem \
  --destination-location-arn arn:aws:datasync:us-east-1:123456789012:location/loc-s3 \
  --name onprem-to-s3-migration \
  --options VerifyMode=POINT_IN_TIME_CONSISTENT,OverwriteMode=ALWAYS

# DataSync - Start task execution
aws datasync start-task-execution \
  --task-arn arn:aws:datasync:us-east-1:123456789012:task/task-12345
```

## Study Tips

### SAP-C02 Exam Focus Areas

**High-Priority Topics**
- SQS vs. SNS vs. EventBridge (when to use each)
- Kinesis Data Streams vs. Firehose (real-time vs. near real-time)
- Kinesis vs. MSK (when to use Kafka)
- Step Functions for workflow orchestration
- Fan-out patterns (SNS → SQS, EventBridge)
- Error handling (DLQs, retries, compensating transactions)
- Ordering guarantees (FIFO queues, Kinesis partition keys)
- At-least-once vs. exactly-once delivery

**Scenario-Based Questions**
- Design event-driven architecture for microservices
- Choose messaging service based on requirements (ordering, durability, throughput)
- Implement backpressure handling with queues
- Design real-time analytics pipeline
- Orchestrate distributed transactions (saga pattern)
- Integrate on-premises and AWS systems

**Common Decision Points**
- **SQS vs. SNS**: 1-to-1 queue vs. 1-to-many pub/sub
- **Standard vs. FIFO**: Throughput vs. ordering
- **Kinesis vs. SQS**: Streaming/ordering vs. simple queue
- **Kinesis vs. MSK**: Managed simplicity vs. Kafka ecosystem
- **Step Functions Standard vs. Express**: Long-running vs. high-volume
- **EventBridge vs. SNS**: Event routing/filtering vs. simple pub/sub
- **Synchronous vs. Asynchronous**: Tight coupling/latency vs. loose coupling/resilience

### Key Differences from SAA-C03

**SAA-C03 Knowledge**
- Basic SQS (standard and FIFO)
- Basic SNS
- Simple EventBridge rules
- Kinesis overview

**Additional SAP-C02 Requirements**
- Advanced SQS patterns (DLQ, visibility timeout, long polling, batching)
- SNS message filtering and fan-out patterns
- EventBridge advanced features (schema registry, archive, cross-account)
- Kinesis Data Analytics with Apache Flink
- MSK (provisioned and serverless)
- Step Functions for complex workflows (saga pattern, error handling)
- API Gateway advanced features (VPC Link, authorizers, usage plans)
- Integration patterns (fan-out, buffering, orchestration)
- AppFlow for SaaS integration
- Service mesh concepts (App Mesh retired 2026-09-30; ECS Service Connect is AWS's recommended replacement on ECS)

### Complex Scenarios to Master

**Event-Driven Microservices**
- EventBridge for event routing
- Lambda or ECS as event consumers
- Error handling and retries
- Event schema versioning

**Real-Time Analytics**
- Kinesis Data Streams for ingestion
- Kinesis Data Analytics for processing
- Kinesis Data Firehose for storage
- Lambda for real-time actions

**Workflow Orchestration**
- Step Functions state machines
- Saga pattern for distributed transactions
- Compensating transactions on failure
- Human approval steps

**Backpressure and Buffering**
- SQS queue between producer and consumer
- Auto-scaling based on queue depth
- Visibility timeout tuning
- DLQ for poison messages

**Fan-Out Patterns**
- SNS → multiple SQS queues
- EventBridge → multiple targets
- Independent processing at different rates
- Error isolation

### Practice Lab Recommendations

1. **SQS and SNS Fan-Out**
   - Create SNS topic and 3 SQS queues
   - Subscribe queues to topic
   - Publish messages to SNS
   - Consume from each queue with Lambda
   - Test message filtering

2. **Kinesis Real-Time Pipeline**
   - Create Kinesis Data Stream
   - Put records using CLI or SDK
   - Create Lambda consumer
   - Create Firehose delivery to S3
   - Query S3 data with Athena

3. **EventBridge Event-Driven**
   - Create custom event bus
   - Create rules with event patterns
   - Add Lambda targets
   - Put events using CLI
   - Test event routing and filtering

4. **Step Functions Workflow**
   - Create state machine (sequential tasks)
   - Add error handling (retry, catch)
   - Add parallel processing
   - Test with failed steps
   - View execution history

5. **API Gateway with SQS Integration**
   - Create API Gateway REST API
   - Integrate with SQS (send message to queue)
   - Create Lambda to process queue
   - Test end-to-end flow
   - Monitor with CloudWatch

6. **MSK Cluster**
   - Create MSK serverless cluster
   - Create topic using Kafka CLI
   - Produce and consume messages
   - Monitor consumer lag
   - Test with multiple consumers

## Additional Resources

### AWS Whitepapers
- Event-Driven Architecture on AWS
- Serverless Streaming Architectures
- Building Microservices with AWS
- Messaging and Integration Services
- Decoupling Applications on AWS

### Documentation Links
- Amazon SQS: https://docs.aws.amazon.com/sqs/
- Amazon SNS: https://docs.aws.amazon.com/sns/
- Amazon EventBridge: https://docs.aws.amazon.com/eventbridge/
- Amazon Kinesis: https://docs.aws.amazon.com/kinesis/
- AWS Step Functions: https://docs.aws.amazon.com/step-functions/
- Amazon MSK: https://docs.aws.amazon.com/msk/
- Amazon API Gateway: https://docs.aws.amazon.com/apigateway/

### Video Resources
- AWS re:Invent sessions (search "API", "INT", "ANT" tracks)
- Event-Driven Architecture patterns
- Kinesis Deep Dive
- Step Functions Workflow Patterns
