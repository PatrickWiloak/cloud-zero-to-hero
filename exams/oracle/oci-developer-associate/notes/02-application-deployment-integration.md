# OCI Developer Associate - Application Deployment and Integration

## Table of Contents
- [Application Deployment Strategies](#application-deployment-strategies)
- [Messaging and Streaming](#messaging-and-streaming)
- [Service Mesh](#service-mesh)
- [Application Integration](#application-integration)
- [Exam Tips](#exam-tips)

---

## Application Deployment Strategies

### Blue-Green Deployment

**Pattern**:
```
Production Traffic → Load Balancer
                        ↓
                   Blue Environment (v1.0) ← Current production
                        ↓
                  Deploy Green Environment (v2.0)
                        ↓
                  Test Green Environment
                        ↓
                  Switch traffic to Green
                        ↓
                  Green is now production
                  Blue kept as rollback option
```

**OKE Implementation**:
```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
  labels:
    app: myapp
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: app
        image: phx.ocir.io/namespace/myapp:v1.0
---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
  labels:
    app: myapp
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: phx.ocir.io/namespace/myapp:v2.0
---
# Service (initially points to blue)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change to "green" to switch traffic
  ports:
  - port: 80
    targetPort: 8080
```

**Traffic Switch**:
```bash
# Test green deployment
kubectl port-forward svc/app-green 8080:80

# Switch traffic to green
kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback if needed
kubectl patch service myapp -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Canary Deployment

**Pattern**:
```
Production Traffic → Load Balancer
                        ↓
                   90% → v1.0 (stable)
                   10% → v2.0 (canary)
                        ↓
                   Monitor metrics
                        ↓
                   Gradually increase v2.0
                        ↓
                   100% → v2.0
```

**Implementation with Istio**:
```yaml
# VirtualService for traffic splitting
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - headers:
        user-group:
          exact: "beta-testers"
    route:
    - destination:
        host: myapp
        subset: v2
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 90
    - destination:
        host: myapp
        subset: v2
      weight: 10
---
# DestinationRule
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

### Rolling Deployment

**Default Kubernetes Strategy**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Max pods above desired count
      maxUnavailable: 1  # Max pods unavailable during update

  template:
    spec:
      containers:
      - name: app
        image: myapp:v2.0
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

**Update Process**:
```bash
# Update image
kubectl set image deployment/app app=myapp:v2.0

# Watch rollout
kubectl rollout status deployment/app

# Pause rollout (if issues detected)
kubectl rollout pause deployment/app

# Resume or rollback
kubectl rollout resume deployment/app
kubectl rollout undo deployment/app
```

---

## Messaging and Streaming

### Queue Service

**Queue Patterns**:
```
Producer → Queue → Consumer

Use Cases:
├── Asynchronous processing
├── Decoupling components
├── Load leveling
└── Guaranteed delivery
```

**Creating Queue**:
```terraform
resource "oci_queue_queue" "main" {
  compartment_id = var.compartment_id
  display_name   = "task-queue"

  # Retention period
  retention_in_seconds = 86400  # 24 hours

  # Visibility timeout
  visibility_in_seconds = 30

  # Dead letter queue
  dead_letter_queue_delivery_count = 5

  # Custom metadata
  freeform_tags = {
    "Environment" = "production"
  }
}
```

**Producer (Send Messages)**:
```python
from oci.queue import QueueClient
from oci.queue.models import PutMessagesDetails, PutMessagesDetailsEntry

# Initialize client
queue_client = QueueClient(config)

# Send message
put_messages_response = queue_client.put_messages(
    queue_id="ocid1.queue...",
    put_messages_details=PutMessagesDetails(
        messages=[
            PutMessagesDetailsEntry(
                content="Task data here",
                metadata={
                    "priority": "high",
                    "task_type": "image_processing"
                }
            )
        ]
    )
)

print(f"Message ID: {put_messages_response.data.entries[0].id}")
```

**Consumer (Receive and Process)**:
```python
import time

def process_queue_messages():
    while True:
        # Get messages (up to 20)
        get_messages_response = queue_client.get_messages(
            queue_id="ocid1.queue...",
            visibility_in_seconds=30,  # Visibility timeout
            timeout_in_seconds=10,     # Long polling
            limit=20
        )

        for message in get_messages_response.data.messages:
            try:
                # Process message
                process_task(message.content)

                # Delete message after successful processing
                queue_client.delete_message(
                    queue_id="ocid1.queue...",
                    message_receipt=message.receipt
                )

            except Exception as e:
                print(f"Error processing message: {e}")
                # Message will become visible again after timeout

        if not get_messages_response.data.messages:
            time.sleep(1)  # Wait before next poll
```

### Streaming Service

**Stream Concepts**:
```
Producers → Stream (Partitions) → Consumers

Features:
├── High throughput (MBs/sec per partition)
├── Ordered within partition
├── Configurable retention (24 hours - 7 days)
├── Multiple consumer groups
└── Replay capability
```

**Creating Stream**:
```terraform
resource "oci_streaming_stream" "main" {
  compartment_id = var.compartment_id
  name           = "events-stream"

  # Number of partitions (scale throughput)
  partitions = 3

  # Retention period
  retention_in_hours = 24

  # Stream pool (optional, for organization)
  stream_pool_id = oci_streaming_stream_pool.main.id
}
```

**Producer**:
```python
from oci.streaming import StreamClient
from oci.streaming.models import PutMessagesDetails, PutMessagesDetailsEntry
import json

stream_client = StreamClient(config, service_endpoint=stream_endpoint)

def send_event(event_data, partition_key):
    # Publish message
    put_messages_result = stream_client.put_messages(
        stream_id="ocid1.stream...",
        put_messages_details=PutMessagesDetails(
            messages=[
                PutMessagesDetailsEntry(
                    key=partition_key,  # Determines partition
                    value=json.dumps(event_data).encode('utf-8')
                )
            ]
        )
    )

    return put_messages_result.data.entries[0]

# Send events
send_event({"user_id": 123, "action": "login"}, partition_key="user-123")
send_event({"user_id": 456, "action": "purchase"}, partition_key="user-456")
```

**Consumer (with Cursor)**:
```python
from oci.streaming.models import CreateCursorDetails

def consume_stream():
    # Create cursor (starting point)
    cursor_details = CreateCursorDetails(
        partition="0",
        type="TRIM_HORIZON"  # Start from beginning
        # type="LATEST"      # Start from newest
        # type="AT_OFFSET"   # Start from specific offset
    )

    cursor = stream_client.create_cursor(
        stream_id="ocid1.stream...",
        create_cursor_details=cursor_details
    )

    current_cursor = cursor.data.value

    # Consume messages
    while True:
        get_messages = stream_client.get_messages(
            stream_id="ocid1.stream...",
            cursor=current_cursor,
            limit=100
        )

        # Process messages
        for message in get_messages.data:
            process_event(json.loads(message.value.decode('utf-8')))

        # Update cursor for next batch
        current_cursor = get_messages.headers.get("opc-next-cursor")

        if not get_messages.data:
            time.sleep(1)
```

**Consumer Groups**:
```python
# Multiple consumers in a group share partitions
from oci.streaming.models import CreateGroupCursorDetails

group_cursor = stream_client.create_group_cursor(
    stream_id="ocid1.stream...",
    create_group_cursor_details=CreateGroupCursorDetails(
        group_name="processor-group",
        instance_name="processor-1",
        type="TRIM_HORIZON",
        commit_on_get=True  # Auto-commit offsets
    )
)
```

---

## Service Mesh

### Istio on OKE

**Istio Components**:
```
Istiod (Control Plane)
├── Traffic Management
├── Security (mTLS)
├── Observability
└── Policy Enforcement

Data Plane (Envoy Proxies)
├── Sidecar in each pod
├── Intercepts traffic
└── Enforces policies
```

**Traffic Management**:

**Circuit Breaking**:
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api-circuit-breaker
spec:
  host: api-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        http2MaxRequests: 100
        maxRequestsPerConnection: 2

    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

**Retry Policy**:
```yaml
apiVersion: networking.istio.io/v1beta1
kind:VirtualService
metadata:
  name: api-retry
spec:
  hosts:
  - api-service
  http:
  - route:
    - destination:
        host: api-service
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: 5xx,reset,connect-failure,refused-stream
```

**Timeout**:
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-timeout
spec:
  hosts:
  - api-service
  http:
  - route:
    - destination:
        host: api-service
    timeout: 5s  # Total request timeout
```

### Service Security

**Mutual TLS (mTLS)**:
```yaml
# Enable mTLS for namespace
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # Require mTLS for all services
```

**Authorization Policies**:
```yaml
# Allow only specific services to call API
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/web-service"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

### Observability

**Distributed Tracing**:
```
Request Flow:
Frontend (span 1) → 50ms
    ↓
API Gateway (span 2) → 100ms
    ↓
Service A (span 3) → 200ms
    ├─→ Service B (span 4) → 150ms
    │   └─→ Database (span 5) → 100ms
    └─→ Cache (span 6) → 10ms
    ↓
Total: 610ms
```

**Enabling Tracing**:
```yaml
# Jaeger deployment (for trace visualization)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
spec:
  template:
    spec:
      containers:
      - name: jaeger
        image: jaegertracing/all-in-one:latest
        env:
        - name: COLLECTOR_ZIPKIN_HTTP_PORT
          value: "9411"
```

**Application Instrumentation**:
```python
# Python example with OpenTelemetry
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger import JaegerExporter

# Setup tracing
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Instrument Flask app
FlaskInstrumentor().instrument_app(app)

# Manual span creation
tracer = trace.get_tracer(__name__)

@app.route('/api/data')
def get_data():
    with tracer.start_as_current_span("fetch-data"):
        # Span automatically includes timing
        data = database.query()
        return jsonify(data)
```

---

## Application Integration

### Event-Driven Integration

**Pattern**:
```
Event Sources
├── Object Storage (upload)
├── Database changes
├── User actions (API calls)
└── Scheduled events (cron)
    ↓
Events Service
    ↓
Event Rules (filters)
    ↓
Actions
├── Functions (process)
├── Notifications (alert)
├── Streaming (pipeline)
└── ServiceConnector (route)
```

**Event Rule Example**:
```terraform
resource "oci_events_rule" "process_uploads" {
  compartment_id = var.compartment_id
  display_name   = "process-uploads"
  is_enabled     = true

  # Trigger on object creation in specific bucket
  condition = jsonencode({
    "eventType" : ["com.oraclecloud.objectstorage.createobject"],
    "data" : {
      "compartmentName" : ["production"],
      "bucketName" : ["user-uploads"],
      "resourceName" : {
        "matches" : {
          "pattern" : "*.jpg"
        }
      }
    }
  })

  # Multiple actions
  actions {
    # Trigger function
    actions {
      action_type = "FAAS"
      is_enabled  = true
      function_id = oci_functions_function.image_processor.id
    }

    # Send notification
    actions {
      action_type = "ONS"
      is_enabled  = true
      topic_id    = oci_ons_notification_topic.uploads.id
    }

    # Send to stream
    actions {
      action_type = "OSS"
      is_enabled  = true
      stream_id   = oci_streaming_stream.events.id
    }
  }
}
```

### Service Connector Hub

**Patterns**:

**Logs to Object Storage**:
```terraform
resource "oci_sch_service_connector" "logs_archive" {
  compartment_id = var.compartment_id
  display_name   = "archive-logs"

  source {
    kind = "logging"

    log_sources {
      compartment_id = var.compartment_id
      log_group_id   = "ocid1.loggroup..."
    }
  }

  tasks {
    kind      = "function"
    function_id = oci_functions_function.log_transformer.id
  }

  target {
    kind        = "objectStorage"
    bucket_name = "log-archive"
    namespace   = data.oci_objectstorage_namespace.ns.namespace

    object_name_prefix = "logs/"
    batch_rollover_size_in_mbs = 100
    batch_rollover_time_in_ms  = 600000  # 10 minutes
  }
}
```

**Monitoring to Streaming**:
```terraform
resource "oci_sch_service_connector" "metrics_stream" {
  compartment_id = var.compartment_id
  display_name   = "metrics-to-stream"

  source {
    kind = "monitoring"

    monitoring_sources {
      compartment_id = var.compartment_id
      namespace_details {
        kind = "selected"
        namespaces {
          namespace = "oci_computeagent"
          metrics {
            kind = "all"
          }
        }
      }
    }
  }

  target {
    kind      = "streaming"
    stream_id = oci_streaming_stream.metrics.id
  }
}
```

### Database Integration

**Autonomous Database Access from Applications**:
```python
import cx_Oracle
import os

# Connection using wallet
def connect_to_adb():
    # Wallet location
    os.environ['TNS_ADMIN'] = '/path/to/wallet'

    # Connection string from tnsnames.ora
    dsn = cx_Oracle.makedsn(
        "adb.us-phoenix-1.oraclecloud.com",
        1522,
        service_name="dbname_high"
    )

    # Connect
    connection = cx_Oracle.connect(
        user="ADMIN",
        password=os.environ.get('DB_PASSWORD'),
        dsn=dsn
    )

    return connection

# Using connection pool (recommended)
def create_connection_pool():
    pool = cx_Oracle.SessionPool(
        user="ADMIN",
        password=os.environ.get('DB_PASSWORD'),
        dsn=dsn,
        min=2,
        max=10,
        increment=1,
        threaded=True
    )

    return pool

# Application usage
pool = create_connection_pool()

@app.route('/api/users')
def get_users():
    connection = pool.acquire()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users)
    finally:
        pool.release(connection)
```

---

## Exam Tips

### Critical Concepts

**Deployment Strategies**:
- Blue-Green: Two identical environments, instant switch
- Canary: Gradual rollout, monitor before full deployment
- Rolling: Update pods incrementally, zero downtime

**Messaging**:
- Queue: Point-to-point, guaranteed delivery, async processing
- Streaming: Pub-sub, high throughput, replay capability, multiple consumers

**Service Mesh**:
- Traffic management: Circuit breaker, retry, timeout
- Security: mTLS between services
- Observability: Distributed tracing

**Integration**:
- Events: Event-driven architecture, triggers actions
- Service Connector: Route data between OCI services
- Functions: Serverless event handlers

### Common Scenarios

**Q: Gradual rollout with ability to rollback quickly?**
A: Blue-green or canary deployment

**Q: Decouple producers and consumers?**
A: Queue or Streaming service

**Q: Automatic retry for failed service calls?**
A: Service mesh with retry policy

**Q: Archive logs automatically?**
A: Service Connector Hub (Logging → Object Storage)

**Q: Process events from multiple sources?**
A: Events Service → Functions or Streaming

---

## Summary

**Deployment**: Blue-green, canary, rolling strategies

**Messaging**: Queue (async), Streaming (pub-sub)

**Service Mesh**: Traffic control, security, observability

**Integration**: Events, Service Connector, database access

---

**Next**: DevOps and Monitoring

## Key terms

- **Blue-green deployment** - a release pattern that runs old and new versions side by side and switches traffic between them.
- **Canary deployment** - a release pattern that sends a small share of traffic to the new version before full rollout.
- **OCI Streaming** - the OCI service for ingesting and processing real-time data streams, compatible with Apache Kafka.
- **OCI Queue** - the OCI service for passing messages between application components asynchronously.
- **Service Connector Hub** - the OCI service that moves data between services, such as from Logging to Object Storage.
