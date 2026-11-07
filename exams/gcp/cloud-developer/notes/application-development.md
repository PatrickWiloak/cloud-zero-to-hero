# Application Development - GCP Professional Cloud Developer

## Overview

Comprehensive guide to cloud-native application development on Google Cloud Platform, covering modern application architecture, serverless computing, containers, API development, and professional development practices. This guide is designed for the Professional Cloud Developer certification exam and includes extensive code examples, configuration patterns, and real-world scenarios.

## Key Topics

1. **Application Architecture** - 12-factor apps, microservices, serverless, event-driven, API-first design
2. **Compute Platforms** - App Engine, Cloud Run, Cloud Functions, GKE for developers
3. **Container Development** - Dockerfile optimization, Cloud Build, Artifact Registry, multi-stage builds
4. **API Development** - REST, gRPC, API Gateway, Cloud Endpoints, Apigee, authentication patterns
5. **Development Tools** - Cloud Code, Cloud Shell, gcloud CLI, Skaffold, debugging tools
6. **Testing & Debugging** - Unit/integration testing, Cloud Debugger, Cloud Profiler, Cloud Trace
7. **CI/CD** - Cloud Build pipelines, deployment strategies, testing automation

## Application Architecture Patterns

### 12-Factor App Methodology

The 12-factor app is a methodology for building software-as-a-service applications. Critical for Professional Cloud Developer exam.

**I. Codebase**: One codebase tracked in version control, many deploys
```bash
# Single repo for microservice
my-service/
  /src
  /tests
  Dockerfile
  cloudbuild.yaml
  .gitignore
```

**II. Dependencies**: Explicitly declare and isolate dependencies
```python
# requirements.txt
flask==2.3.0
google-cloud-storage==2.10.0
google-cloud-secret-manager==2.16.0

# Use virtual environments
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**III. Config**: Store config in environment variables
```python
# config.py
import os

class Config:
    PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
    DB_CONNECTION = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'

    # For Cloud Run
    PORT = int(os.environ.get('PORT', 8080))
```

**IV. Backing Services**: Treat backing services as attached resources
```python
# database.py - treat database as attached resource
import os
import sqlalchemy

def get_db_connection():
    db_url = os.environ['DATABASE_URL']
    # Connection can be swapped by changing environment variable
    engine = sqlalchemy.create_engine(db_url)
    return engine
```

**V. Build, Release, Run**: Strictly separate build and run stages
```yaml
# cloudbuild.yaml - separate stages
steps:
  # Build stage
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/app:$COMMIT_SHA', '.']

  # Test stage
  - name: 'gcr.io/$PROJECT_ID/app:$COMMIT_SHA'
    args: ['pytest', 'tests/']

  # Release stage
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/app:$COMMIT_SHA']

  # Run stage - deploy
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'app', '--image', 'gcr.io/$PROJECT_ID/app:$COMMIT_SHA']
```

**VI. Processes**: Execute the app as one or more stateless processes
```python
# Stateless application example
from flask import Flask, session
import redis

app = Flask(__name__)
# Don't store session in process memory
redis_client = redis.Redis(host=os.environ['REDIS_HOST'])

@app.route('/cart', methods=['POST'])
def add_to_cart():
    user_id = request.json['user_id']
    item = request.json['item']
    # Store in Redis, not in-memory
    redis_client.lpush(f'cart:{user_id}', item)
    return {'status': 'added'}
```

**VII. Port Binding**: Export services via port binding
```python
# app.py
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
```

**VIII. Concurrency**: Scale out via the process model
```dockerfile
# Horizontal scaling, not vertical
# Cloud Run handles multiple instances
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

**IX. Disposability**: Maximize robustness with fast startup and graceful shutdown
```python
# graceful_shutdown.py
import signal
import sys

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    # Close database connections
    db.close()
    # Finish current requests
    server.shutdown()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
```

**X. Dev/Prod Parity**: Keep development, staging, and production as similar as possible
```bash
# Use same backing services in dev/prod
# Development
export DATABASE_URL="postgresql://localhost/devdb"

# Production
export DATABASE_URL="postgresql://cloudsql/proddb"
```

**XI. Logs**: Treat logs as event streams
```python
# logging_config.py
import logging
import json

# Write structured logs to stdout (Cloud Logging captures)
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[logging.StreamHandler()]
    )

def log_structured(message, severity='INFO', **kwargs):
    log_entry = {
        'severity': severity,
        'message': message,
        **kwargs
    }
    print(json.dumps(log_entry))

# Usage
log_structured('User logged in', user_id=123, ip='1.2.3.4')
```

**XII. Admin Processes**: Run admin/management tasks as one-off processes
```bash
# Run database migrations as one-off processes
gcloud run jobs create migrate-db \
  --image gcr.io/project/app:latest \
  --command python \
  --args manage.py,migrate
```

### Microservices Architecture

**Core Principles**:
```
Single Responsibility → Each service does one thing well
Decentralized Data → Each service owns its data
Independent Deployment → Deploy services independently
Technology Diversity → Use best tool for each job
Failure Isolation → One service failure doesn't cascade
```

**Service Communication Patterns**:
```python
# 1. Synchronous REST API
import requests

def call_user_service(user_id):
    response = requests.get(
        f'https://user-service.run.app/users/{user_id}',
        headers={'Authorization': f'Bearer {get_token()}'}
    )
    return response.json()

# 2. Asynchronous Pub/Sub
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project-id', 'order-created')

def publish_order_event(order_data):
    message_json = json.dumps(order_data)
    future = publisher.publish(
        topic_path,
        message_json.encode('utf-8'),
        event_type='order.created'
    )
    return future.result()

# 3. gRPC for internal services
import grpc
import user_service_pb2
import user_service_pb2_grpc

def get_user_grpc(user_id):
    with grpc.insecure_channel('user-service:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUser(
            user_service_pb2.GetUserRequest(user_id=user_id)
        )
        return response
```

**Service Mesh with Istio** (GKE):
```yaml
# istio-config.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
  - user-service
  http:
  - match:
    - headers:
        x-api-version:
          exact: v2
    route:
    - destination:
        host: user-service
        subset: v2
  - route:
    - destination:
        host: user-service
        subset: v1
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: user-service
spec:
  host: user-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 2
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

### Event-Driven Architecture

**Event Sourcing Pattern**:
```python
# event_store.py
from google.cloud import firestore
from datetime import datetime

class EventStore:
    def __init__(self):
        self.db = firestore.Client()

    def append_event(self, aggregate_id, event_type, event_data):
        event = {
            'aggregate_id': aggregate_id,
            'event_type': event_type,
            'event_data': event_data,
            'timestamp': datetime.utcnow(),
            'version': self.get_next_version(aggregate_id)
        }
        self.db.collection('events').add(event)
        return event

    def get_events(self, aggregate_id):
        events = self.db.collection('events')\
            .where('aggregate_id', '==', aggregate_id)\
            .order_by('version')\
            .stream()
        return [e.to_dict() for e in events]

    def replay_events(self, aggregate_id, aggregate_class):
        events = self.get_events(aggregate_id)
        aggregate = aggregate_class()
        for event in events:
            aggregate.apply_event(event)
        return aggregate

# order_aggregate.py
class Order:
    def __init__(self):
        self.order_id = None
        self.items = []
        self.status = 'PENDING'

    def apply_event(self, event):
        if event['event_type'] == 'OrderCreated':
            self.order_id = event['event_data']['order_id']
        elif event['event_type'] == 'ItemAdded':
            self.items.append(event['event_data']['item'])
        elif event['event_type'] == 'OrderCompleted':
            self.status = 'COMPLETED'
```

**CQRS Pattern** (Command Query Responsibility Segregation):
```python
# commands.py - Write model
class OrderCommandService:
    def __init__(self, event_store, publisher):
        self.event_store = event_store
        self.publisher = publisher

    def create_order(self, order_data):
        # Validate command
        if not order_data.get('customer_id'):
            raise ValueError('Customer ID required')

        # Create event
        event = self.event_store.append_event(
            aggregate_id=order_data['order_id'],
            event_type='OrderCreated',
            event_data=order_data
        )

        # Publish event for read model update
        self.publisher.publish(
            'order-events',
            json.dumps(event).encode()
        )

# queries.py - Read model
class OrderQueryService:
    def __init__(self):
        self.db = firestore.Client()

    def get_order(self, order_id):
        # Read from optimized read model
        doc = self.db.collection('orders_read_model')\
            .document(order_id).get()
        return doc.to_dict()

    def get_customer_orders(self, customer_id):
        # Denormalized for fast queries
        orders = self.db.collection('orders_read_model')\
            .where('customer_id', '==', customer_id)\
            .order_by('created_at', direction=firestore.Query.DESCENDING)\
            .limit(10).stream()
        return [o.to_dict() for o in orders]

# event_handler.py - Update read model
def handle_order_event(event, context):
    """Cloud Function to update read model"""
    event_data = json.loads(event['data'])

    if event_data['event_type'] == 'OrderCreated':
        # Update read model
        db = firestore.Client()
        db.collection('orders_read_model').document(
            event_data['aggregate_id']
        ).set({
            'order_id': event_data['aggregate_id'],
            'customer_id': event_data['event_data']['customer_id'],
            'items': event_data['event_data']['items'],
            'status': 'PENDING',
            'created_at': event_data['timestamp']
        })
```

**Saga Pattern** (Distributed Transactions):
```python
# saga_orchestrator.py
from google.cloud import pubsub_v1
from enum import Enum

class SagaState(Enum):
    STARTED = 'STARTED'
    PAYMENT_PROCESSING = 'PAYMENT_PROCESSING'
    INVENTORY_RESERVED = 'INVENTORY_RESERVED'
    COMPLETED = 'COMPLETED'
    COMPENSATING = 'COMPENSATING'
    FAILED = 'FAILED'

class OrderSaga:
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.db = firestore.Client()

    def start_order_saga(self, order_data):
        saga_id = order_data['order_id']

        # Save saga state
        self.save_saga_state(saga_id, SagaState.STARTED, order_data)

        # Step 1: Process payment
        self.publish_command('process-payment', {
            'saga_id': saga_id,
            'amount': order_data['total'],
            'customer_id': order_data['customer_id']
        })

    def handle_payment_success(self, event):
        saga_id = event['saga_id']
        saga = self.get_saga(saga_id)

        # Update state
        self.save_saga_state(saga_id, SagaState.PAYMENT_PROCESSING, event)

        # Step 2: Reserve inventory
        self.publish_command('reserve-inventory', {
            'saga_id': saga_id,
            'items': saga['data']['items']
        })

    def handle_inventory_reserved(self, event):
        saga_id = event['saga_id']

        # Update state
        self.save_saga_state(saga_id, SagaState.INVENTORY_RESERVED, event)

        # Step 3: Complete order
        self.publish_command('complete-order', {'saga_id': saga_id})
        self.save_saga_state(saga_id, SagaState.COMPLETED, event)

    def handle_failure(self, event):
        """Compensating transactions"""
        saga_id = event['saga_id']
        saga = self.get_saga(saga_id)

        self.save_saga_state(saga_id, SagaState.COMPENSATING, event)

        # Rollback based on current state
        if saga['state'] in [SagaState.PAYMENT_PROCESSING, SagaState.INVENTORY_RESERVED]:
            self.publish_command('refund-payment', {'saga_id': saga_id})

        if saga['state'] == SagaState.INVENTORY_RESERVED:
            self.publish_command('release-inventory', {'saga_id': saga_id})

        self.save_saga_state(saga_id, SagaState.FAILED, event)
```

### API-First Design

**OpenAPI Specification**:
```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: Order API
  version: 1.0.0
  description: RESTful API for order management
servers:
  - url: https://api.example.com/v1
paths:
  /orders:
    post:
      summary: Create new order
      operationId: createOrder
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: Order created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          description: Invalid request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
    get:
      summary: List orders
      parameters:
        - name: customer_id
          in: query
          schema:
            type: string
        - name: status
          in: query
          schema:
            type: string
            enum: [PENDING, COMPLETED, CANCELLED]
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
        - name: page_token
          in: query
          schema:
            type: string
      responses:
        '200':
          description: List of orders
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderList'
  /orders/{orderId}:
    get:
      summary: Get order by ID
      parameters:
        - name: orderId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Order details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '404':
          description: Order not found
components:
  schemas:
    Order:
      type: object
      properties:
        order_id:
          type: string
        customer_id:
          type: string
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'
        total:
          type: number
        status:
          type: string
          enum: [PENDING, COMPLETED, CANCELLED]
        created_at:
          type: string
          format: date-time
    CreateOrderRequest:
      type: object
      required:
        - customer_id
        - items
      properties:
        customer_id:
          type: string
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'
    OrderItem:
      type: object
      properties:
        product_id:
          type: string
        quantity:
          type: integer
        price:
          type: number
    OrderList:
      type: object
      properties:
        orders:
          type: array
          items:
            $ref: '#/components/schemas/Order'
        next_page_token:
          type: string
    Error:
      type: object
      properties:
        error:
          type: string
        message:
          type: string
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
security:
  - bearerAuth: []
```

## Application Platforms

### App Engine Deep Dive

**Standard vs Flexible Environment**:
```
Standard Environment:
✓ Automatic scaling to zero
✓ Free tier available
✓ Fast cold starts (milliseconds)
✓ Network sandbox (limited outbound)
✓ Fixed runtimes (Python, Java, Node.js, Go, PHP, Ruby)
✓ No SSH access
✓ Max 60-second request timeout

Flexible Environment:
✓ Custom runtimes (Dockerfile)
✓ SSH access to instances
✓ Any language/version
✓ Minimum one instance always running
✓ Longer cold starts (minutes)
✓ No free tier
✓ 60-minute request timeout
```

**app.yaml Configuration** (Standard Environment):
```yaml
# app.yaml - Complete configuration example
runtime: python311
service: default  # or custom service name
instance_class: F2  # F1 (default), F2, F4, F4_1G

# Automatic scaling
automatic_scaling:
  target_cpu_utilization: 0.65
  target_throughput_utilization: 0.6
  max_instances: 10
  min_instances: 0  # Scale to zero
  max_idle_instances: 2
  min_idle_instances: 0
  max_pending_latency: 30ms
  min_pending_latency: 10ms
  max_concurrent_requests: 80

# Environment variables
env_variables:
  DATABASE_URL: "postgresql://..."
  ENABLE_FEATURE_X: "true"

# VPC access for Cloud SQL, Memorystore
vpc_access_connector:
  name: projects/PROJECT_ID/locations/REGION/connectors/CONNECTOR_NAME

# Inbound services
inbound_services:
- warmup  # Enable warmup requests

# Handlers
handlers:
- url: /static
  static_dir: static
  secure: always
  http_headers:
    Cache-Control: "public, max-age=3600"

- url: /api/.*
  script: auto
  secure: always
  redirect_http_response_code: 301

- url: /.*
  script: auto
  secure: always

# Error handlers
error_handlers:
- file: error.html
  error_code: over_quota
- file: error.html
  error_code: dos_api_denial

# Libraries (Python)
libraries:
- name: ssl
  version: latest

# Entrypoint
entrypoint: gunicorn -b :$PORT main:app
```

**app.yaml for Flexible Environment**:
```yaml
# app.yaml - Flexible environment
runtime: custom
env: flex
service: api

# Manual scaling (specific number of instances)
manual_scaling:
  instances: 5

# OR automatic scaling
automatic_scaling:
  min_num_instances: 2
  max_num_instances: 20
  cool_down_period_sec: 120
  cpu_utilization:
    target_utilization: 0.5

# Resources
resources:
  cpu: 2
  memory_gb: 4
  disk_size_gb: 10
  volumes:
  - name: ramdisk1
    volume_type: tmpfs
    size_gb: 0.5

# Network
network:
  instance_tag: app-server
  name: default
  subnetwork_name: default
  session_affinity: true
  forwarded_ports:
  - 8080

# Liveness check
liveness_check:
  path: "/healthz"
  check_interval_sec: 30
  timeout_sec: 4
  failure_threshold: 4
  success_threshold: 2

# Readiness check
readiness_check:
  path: "/ready"
  check_interval_sec: 5
  timeout_sec: 4
  failure_threshold: 2
  success_threshold: 2
  app_start_timeout_sec: 300

# Beta settings
beta_settings:
  cloud_sql_instances: PROJECT:REGION:INSTANCE_NAME
```

**Services and Versions**:
```bash
# App Engine supports multiple services (microservices)
my-app/
  /default-service/
    app.yaml  # service: default
    main.py
  /api-service/
    app.yaml  # service: api
    api.py
  /worker-service/
    app.yaml  # service: worker
    worker.py

# Deploy services
gcloud app deploy default-service/app.yaml
gcloud app deploy api-service/app.yaml

# Deploy specific version without routing traffic
gcloud app deploy --no-promote --version=v2

# List services and versions
gcloud app services list
gcloud app versions list --service=default

# Traffic splitting
gcloud app services set-traffic default \
  --splits=v1=0.9,v2=0.1 \
  --split-by=ip  # or cookie, random

# Gradual rollout
gcloud app services set-traffic default \
  --splits=v2=0.1 \
  --migrate  # Gradually migrate traffic

# Delete old versions
gcloud app versions delete v1 v2 --service=api
```

**dispatch.yaml** (Routing Rules):
```yaml
# dispatch.yaml - Route requests to different services
dispatch:
  # Route API requests to api service
  - url: "*/api/*"
    service: api

  # Route admin requests to admin service
  - url: "*/admin/*"
    service: admin

  # Route static assets to cdn service
  - url: "*.example.com/static/*"
    service: cdn

  # Route mobile API to mobile service
  - url: "mobile-api.example.com/*"
    service: mobile-api

  # Default service
  - url: "*.example.com/*"
    service: default

# Deploy dispatch rules
# gcloud app deploy dispatch.yaml
```

**cron.yaml** (Scheduled Tasks):
```yaml
# cron.yaml - Scheduled jobs
cron:
- description: "Daily backup job"
  url: /tasks/backup
  schedule: every day 02:00
  timezone: America/New_York
  target: worker  # Service name
  retry_parameters:
    min_backoff_seconds: 2.5
    max_backoff_seconds: 300
    max_doublings: 5

- description: "Every 5 minutes data sync"
  url: /tasks/sync
  schedule: every 5 minutes
  target: worker

- description: "Weekly report"
  url: /tasks/weekly-report
  schedule: every monday 09:00
  target: worker

- description: "Cleanup old data"
  url: /tasks/cleanup
  schedule: 1st,15th of month 00:00
  target: worker

# Complex schedules (cron syntax)
- description: "Custom cron schedule"
  url: /tasks/custom
  schedule: 0 */6 * * *  # Every 6 hours
  target: worker

# Deploy cron jobs
# gcloud app deploy cron.yaml
```

**queue.yaml** (Task Queues):
```yaml
# queue.yaml - Task queue configuration
queue:
- name: default
  rate: 100/s
  bucket_size: 100
  max_concurrent_requests: 100
  retry_parameters:
    task_retry_limit: 7
    task_age_limit: 2d
    min_backoff_seconds: 10
    max_backoff_seconds: 200
    max_doublings: 3

- name: email-queue
  rate: 50/s
  max_concurrent_requests: 10
  retry_parameters:
    task_retry_limit: 5

- name: high-priority
  rate: 200/s
  bucket_size: 200
  max_concurrent_requests: 200

# Deploy queue configuration
# gcloud app deploy queue.yaml
```

**App Engine Application Example**:
```python
# main.py - Flask application
from flask import Flask, request, jsonify
from google.cloud import datastore
from google.cloud import storage
from google.cloud import tasks_v2
import os

app = Flask(__name__)

# Configuration
PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']
ds_client = datastore.Client()

@app.route('/')
def index():
    return 'App Engine Application'

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create order and enqueue processing task"""
    order_data = request.get_json()

    # Save to Datastore
    key = ds_client.key('Order')
    entity = datastore.Entity(key=key)
    entity.update({
        'customer_id': order_data['customer_id'],
        'items': order_data['items'],
        'status': 'PENDING'
    })
    ds_client.put(entity)

    # Enqueue task for async processing
    enqueue_order_processing(entity.key.id)

    return jsonify({
        'order_id': entity.key.id,
        'status': 'PENDING'
    }), 201

@app.route('/tasks/process-order', methods=['POST'])
def process_order():
    """Background task handler"""
    # Verify request is from Task Queue
    if request.headers.get('X-AppEngine-QueueName') is None:
        return 'Unauthorized', 401

    order_id = request.get_json()['order_id']

    # Process order
    key = ds_client.key('Order', int(order_id))
    order = ds_client.get(key)
    order['status'] = 'PROCESSING'

    # ... process order logic ...

    order['status'] = 'COMPLETED'
    ds_client.put(order)

    return '', 200

def enqueue_order_processing(order_id):
    """Enqueue task to Cloud Tasks"""
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(PROJECT_ID, 'us-central1', 'default')

    task = {
        'app_engine_http_request': {
            'http_method': tasks_v2.HttpMethod.POST,
            'relative_uri': '/tasks/process-order',
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'order_id': order_id}).encode()
        }
    }

    client.create_task(request={'parent': parent, 'task': task})

@app.route('/_ah/warmup')
def warmup():
    """Warmup handler to initialize resources"""
    # Initialize database connections, load data, etc.
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

### Cloud Run Deep Dive

**Architecture and Features**:
```
Cloud Run Characteristics:
✓ Fully managed serverless containers
✓ Scale to zero (pay only when serving requests)
✓ Automatic HTTPS endpoints
✓ Custom domains with SSL
✓ Gradual rollouts (traffic splitting)
✓ Concurrency up to 1000 requests/container
✓ Max request timeout: 60 minutes (3600s)
✓ Stateless containers (ephemeral filesystem)
✓ Container instances lifecycle managed automatically
```

**Container Lifecycle and Request Flow**:
```
Container Lifecycle:
1. Container Start → Your code initializes
2. Port Binding → Listen on $PORT (required)
3. Ready → Container receives requests
4. Serving → Handle concurrent requests
5. Idle → No requests, container may be kept warm
6. Shutdown → SIGTERM signal (10s grace period)

Request Flow:
User Request → Cloud Load Balancer → Container Instance
  ↓
If no instances ready → Cold Start (new container)
If instances available → Route to existing container
Multiple concurrent requests → Same container (up to concurrency limit)
```

**Concurrency Configuration**:
```yaml
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        # Max concurrent requests per container instance
        autoscaling.knative.dev/maxScale: "100"  # Max instances
        autoscaling.knative.dev/minScale: "0"    # Min instances (0 = scale to zero)
        run.googleapis.com/container-concurrency: "80"  # Concurrent requests
        # CPU allocation
        run.googleapis.com/cpu-throttling: "false"  # Always allocate CPU (not just during requests)
        # Startup CPU boost
        run.googleapis.com/startup-cpu-boost: "true"
    spec:
      containerConcurrency: 80  # Max concurrent requests per instance
      timeoutSeconds: 300  # Request timeout
      serviceAccountName: my-sa@project.iam.gserviceaccount.com
      containers:
      - image: gcr.io/project/image:tag
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          value: "postgresql://..."
        resources:
          limits:
            memory: "512Mi"
            cpu: "1000m"  # 1 CPU
          requests:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
```

**CPU Allocation Strategies**:
```bash
# CPU only during request processing (default, cheaper)
gcloud run deploy myapp \
  --image gcr.io/project/image \
  --cpu 1 \
  --memory 512Mi \
  --cpu-throttling  # Default behavior

# CPU always allocated (better for background work, WebSockets)
gcloud run deploy myapp \
  --image gcr.io/project/image \
  --cpu 1 \
  --memory 512Mi \
  --no-cpu-throttling  # Always allocate CPU

# Startup CPU boost (reduce cold starts)
gcloud run deploy myapp \
  --image gcr.io/project/image \
  --cpu-boost  # Extra CPU during startup
```

**Scaling and Concurrency Best Practices**:
```python
# app.py - Optimized for Cloud Run concurrency
from flask import Flask
import threading
import queue

app = Flask(__name__)

# Thread-safe request processing
request_queue = queue.Queue(maxsize=100)

# Database connection pool (thread-safe)
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    os.environ['DATABASE_URL'],
    poolclass=QueuePool,
    pool_size=10,  # Max connections
    max_overflow=20,  # Extra connections when needed
    pool_pre_ping=True,  # Verify connections
    pool_recycle=3600  # Recycle connections hourly
)

@app.route('/api/data', methods=['GET'])
def get_data():
    """Handle request with connection pooling"""
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM data LIMIT 10")
        return {'data': [dict(row) for row in result]}

# Graceful shutdown
import signal
import sys

def signal_handler(sig, frame):
    print('SIGTERM received, shutting down...')
    # Finish current requests
    # Close database connections
    engine.dispose()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # Listen on PORT environment variable
    port = int(os.environ.get('PORT', 8080))
    # Use production WSGI server
    from waitress import serve
    serve(app, host='0.0.0.0', port=port, threads=80)
```

**Deployment Strategies**:
```bash
# Blue/Green Deployment - Deploy new version, test, switch traffic
# Deploy new revision without traffic
gcloud run deploy myapp \
  --image gcr.io/project/image:v2 \
  --no-traffic \
  --tag=v2

# Test new revision
curl https://v2---myapp-abc123-uc.a.run.app

# Switch 100% traffic to new revision
gcloud run services update-traffic myapp --to-latest

# Canary Deployment - Gradual rollout
# Deploy new revision with 10% traffic
gcloud run deploy myapp \
  --image gcr.io/project/image:v2 \
  --tag=canary

gcloud run services update-traffic myapp \
  --to-revisions=myapp-v1=90,myapp-v2=10

# Monitor metrics, gradually increase
gcloud run services update-traffic myapp \
  --to-revisions=myapp-v1=50,myapp-v2=50

# Full rollout
gcloud run services update-traffic myapp \
  --to-latest

# Rollback
gcloud run services update-traffic myapp \
  --to-revisions=myapp-v1=100
```

**Request Routing and Traffic Splitting**:
```bash
# Tag-based routing (for testing)
gcloud run services update-traffic myapp \
  --to-tags=stable=80,beta=20

# Revision-based routing
gcloud run services update-traffic myapp \
  --to-revisions=myapp-00001-abc=70,myapp-00002-def=30

# URL patterns for tagged revisions:
# https://stable---myapp-hash-uc.a.run.app
# https://beta---myapp-hash-uc.a.run.app
```

**Cloud Run with Cloud SQL**:
```python
# cloudsql_connection.py
import os
import sqlalchemy
from google.cloud.sql.connector import Connector

def get_connection_pool():
    """Create connection pool for Cloud SQL"""
    # Cloud Run provides Unix socket access
    instance_connection_name = os.environ['INSTANCE_CONNECTION_NAME']

    connector = Connector()

    def getconn():
        return connector.connect(
            instance_connection_name,
            "pg8000",
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            db=os.environ['DB_NAME']
        )

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )
    return pool

# Usage
db_pool = get_connection_pool()

@app.route('/users/<int:user_id>')
def get_user(user_id):
    with db_pool.connect() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT * FROM users WHERE id = :id"),
            {"id": user_id}
        )
        user = result.fetchone()
        return jsonify(dict(user))
```

**Cloud Run with VPC Access**:
```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create my-connector \
  --region=us-central1 \
  --subnet=default \
  --min-instances=2 \
  --max-instances=10

# Deploy Cloud Run with VPC access
gcloud run deploy myapp \
  --image gcr.io/project/image \
  --vpc-connector=my-connector \
  --vpc-egress=private-ranges-only  # or all-traffic

# Access private GCP services (Cloud SQL, Memorystore, etc.)
```

**Advanced Cloud Run Configuration**:
```bash
# Complete deployment command
gcloud run deploy myapp \
  --image=gcr.io/project/image:tag \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --service-account=myapp@project.iam.gserviceaccount.com \
  --set-env-vars="ENV=prod,DEBUG=false" \
  --set-secrets="API_KEY=api-key:latest,DB_PASS=db-password:1" \
  --memory=1Gi \
  --cpu=2 \
  --timeout=300 \
  --concurrency=80 \
  --min-instances=1 \
  --max-instances=100 \
  --port=8080 \
  --vpc-connector=my-connector \
  --vpc-egress=private-ranges-only \
  --ingress=all \
  --cpu-boost \
  --no-cpu-throttling \
  --execution-environment=gen2 \
  --labels=app=myapp,env=prod \
  --tag=v2

# Service-to-service authentication
gcloud run deploy backend \
  --no-allow-unauthenticated

# Frontend calls backend with service account
import google.auth.transport.requests
from google.oauth2 import id_token

def call_backend():
    backend_url = "https://backend-xyz.run.app"
    auth_req = google.auth.transport.requests.Request()
    id_token_value = id_token.fetch_id_token(auth_req, backend_url)

    response = requests.get(
        backend_url,
        headers={"Authorization": f"Bearer {id_token_value}"}
    )
    return response.json()
```

### Cloud Functions Complete Guide

**Generation Comparison**:
```
Cloud Functions (1st gen):
- Node.js, Python, Go, Java, .NET, Ruby, PHP
- Max execution: 9 minutes (540s)
- Max memory: 8GB
- Max concurrency: 3000 per function
- Deployed in specific region

Cloud Functions (2nd gen) - Built on Cloud Run:
- Node.js, Python, Go, Java, .NET
- Max execution: 60 minutes (3600s)
- Max memory: 16GB
- Max concurrency: 1000 per instance
- Better cold start times
- More event sources
- Eventarc integration
```

**Complete Trigger Types**:

**1. HTTP Triggers**:
```python
# Python HTTP function
import functions_framework
from flask import Request, jsonify

@functions_framework.http
def hello_http(request: Request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object
    Returns:
        Response object
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'

    return jsonify({'message': f'Hello {name}!'}), 200

# Deploy
# gcloud functions deploy hello_http \
#   --gen2 \
#   --runtime=python311 \
#   --region=us-central1 \
#   --source=. \
#   --entry-point=hello_http \
#   --trigger-http \
#   --allow-unauthenticated
```

```javascript
// Node.js HTTP function
const functions = require('@google-cloud/functions-framework');

functions.http('helloHttp', (req, res) => {
  const name = req.query.name || req.body.name || 'World';
  res.status(200).json({
    message: `Hello ${name}!`
  });
});

// CORS handling
functions.http('corsExample', (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');

  if (req.method === 'OPTIONS') {
    res.set('Access-Control-Allow-Methods', 'GET, POST');
    res.set('Access-Control-Allow-Headers', 'Content-Type');
    res.status(204).send('');
  } else {
    res.status(200).json({ message: 'CORS enabled' });
  }
});
```

**2. Cloud Pub/Sub Triggers**:
```python
# Python Pub/Sub function
import functions_framework
import base64
import json

@functions_framework.cloud_event
def process_pubsub(cloud_event):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        cloud_event: CloudEvent containing Pub/Sub message
    """
    # Decode Pub/Sub message
    pubsub_message = base64.b64decode(
        cloud_event.data["message"]["data"]
    ).decode('utf-8')

    data = json.loads(pubsub_message)

    # Access message attributes
    attributes = cloud_event.data["message"].get("attributes", {})

    print(f"Processing message: {data}")
    print(f"Attributes: {attributes}")

    # Process the message
    process_order(data)

def process_order(order_data):
    """Process order logic"""
    print(f"Processing order: {order_data['order_id']}")
    # Business logic here

# Deploy
# gcloud functions deploy process_pubsub \
#   --gen2 \
#   --runtime=python311 \
#   --region=us-central1 \
#   --source=. \
#   --entry-point=process_pubsub \
#   --trigger-topic=order-events \
#   --retry  # Enable retries on failure
```

```go
// Go Pub/Sub function
package p

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "github.com/GoogleCloudPlatform/functions-framework-go/functions"
    "github.com/cloudevents/sdk-go/v2/event"
)

type MessagePublishedData struct {
    Message PubSubMessage
}

type PubSubMessage struct {
    Data       []byte            `json:"data"`
    Attributes map[string]string `json:"attributes"`
}

func init() {
    functions.CloudEvent("ProcessPubSub", processPubSub)
}

func processPubSub(ctx context.Context, e event.Event) error {
    var msg MessagePublishedData
    if err := e.DataAs(&msg); err != nil {
        return fmt.Errorf("event.DataAs: %v", err)
    }

    // Decode message data
    data := string(msg.Message.Data)
    log.Printf("Processing message: %s", data)

    // Access attributes
    for key, value := range msg.Message.Attributes {
        log.Printf("Attribute %s: %s", key, value)
    }

    return nil
}
```

**3. Cloud Storage Triggers**:
```python
# Python Storage function
import functions_framework
from google.cloud import storage
from google.cloud import vision

@functions_framework.cloud_event
def process_image(cloud_event):
    """Triggered by Cloud Storage when file is uploaded.
    Args:
        cloud_event: CloudEvent containing Storage event data
    """
    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]
    event_type = cloud_event["type"]  # google.cloud.storage.object.v1.finalized

    print(f"Event type: {event_type}")
    print(f"File: gs://{bucket_name}/{file_name}")

    # Ignore deletion events
    if event_type == "google.cloud.storage.object.v1.deleted":
        return

    # Process only images
    if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        print(f"Skipping non-image file: {file_name}")
        return

    # Analyze image with Vision API
    analyze_image(bucket_name, file_name)

def analyze_image(bucket_name, file_name):
    """Analyze image and save results"""
    vision_client = vision.ImageAnnotatorClient()
    storage_client = storage.Client()

    # Get image from Storage
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    image = vision.Image()
    image.source.image_uri = f"gs://{bucket_name}/{file_name}"

    # Detect labels
    response = vision_client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    print(f"Labels: {labels}")

    # Save results to metadata
    blob.metadata = {'labels': ','.join(labels)}
    blob.patch()

# Deploy
# gcloud functions deploy process_image \
#   --gen2 \
#   --runtime=python311 \
#   --region=us-central1 \
#   --source=. \
#   --entry-point=process_image \
#   --trigger-bucket=my-upload-bucket \
#   --retry
```

**4. Firestore Triggers**:
```javascript
// Node.js Firestore function
const functions = require('@google-cloud/functions-framework');
const {Firestore} = require('@google-cloud/firestore');

const firestore = new Firestore();

functions.cloudEvent('processFirestoreEvent', async (cloudEvent) => {
  // Event types:
  // - google.cloud.firestore.document.v1.created
  // - google.cloud.firestore.document.v1.updated
  // - google.cloud.firestore.document.v1.deleted
  // - google.cloud.firestore.document.v1.written (created or updated)

  const eventType = cloudEvent.type;
  const data = cloudEvent.data;

  // Document path: projects/PROJECT/databases/(default)/documents/users/USER_ID
  const documentPath = data.value.name;
  const pathParts = documentPath.split('/');
  const docId = pathParts[pathParts.length - 1];

  console.log(`Event: ${eventType}`);
  console.log(`Document: ${docId}`);

  // New data
  const newValue = data.value.fields;

  // Old data (for update/delete events)
  const oldValue = data.oldValue?.fields;

  if (eventType.includes('created')) {
    console.log('New document created:', newValue);
    await handleUserCreated(docId, newValue);
  } else if (eventType.includes('updated')) {
    console.log('Document updated');
    console.log('Old:', oldValue);
    console.log('New:', newValue);
    await handleUserUpdated(docId, oldValue, newValue);
  } else if (eventType.includes('deleted')) {
    console.log('Document deleted:', oldValue);
    await handleUserDeleted(docId, oldValue);
  }
});

async function handleUserCreated(userId, userData) {
  // Send welcome email
  console.log(`Sending welcome email to ${userId}`);
  // ... email logic
}

async function handleUserUpdated(userId, oldData, newData) {
  // Check if email changed
  if (oldData.email !== newData.email) {
    console.log(`Email changed for ${userId}`);
    // ... notification logic
  }
}

async function handleUserDeleted(userId, userData) {
  // Cleanup user data
  console.log(`Cleaning up data for ${userId}`);
  // ... cleanup logic
}

// Deploy
// gcloud functions deploy processFirestoreEvent \
//   --gen2 \
//   --runtime=nodejs20 \
//   --region=us-central1 \
//   --source=. \
//   --entry-point=processFirestoreEvent \
//   --trigger-event-filters="type=google.cloud.firestore.document.v1.written" \
//   --trigger-event-filters="database=(default)" \
//   --trigger-event-filters-path-pattern="document=users/{userId}"
```

**5. Firebase Authentication Triggers**:
```python
# Python Firebase Auth function
import functions_framework
from google.cloud import firestore

@functions_framework.cloud_event
def on_user_create(cloud_event):
    """Triggered when new user is created in Firebase Auth.
    Args:
        cloud_event: CloudEvent with user data
    """
    data = cloud_event.data

    uid = data.get('uid')
    email = data.get('email')
    display_name = data.get('displayName')
    photo_url = data.get('photoURL')

    print(f"New user created: {uid}")
    print(f"Email: {email}")

    # Create user profile in Firestore
    db = firestore.Client()
    user_ref = db.collection('users').document(uid)
    user_ref.set({
        'email': email,
        'displayName': display_name or '',
        'photoURL': photo_url or '',
        'createdAt': firestore.SERVER_TIMESTAMP,
        'role': 'user',
        'status': 'active'
    })

    # Send welcome email
    send_welcome_email(email, display_name)

    print(f"User profile created for {uid}")

def send_welcome_email(email, name):
    """Send welcome email to new user"""
    # Use SendGrid, Mailgun, or other email service
    print(f"Sending welcome email to {email}")

# Deploy with Eventarc
# gcloud functions deploy on_user_create \
#   --gen2 \
#   --runtime=python311 \
#   --region=us-central1 \
#   --source=. \
#   --entry-point=on_user_create \
#   --trigger-event-filters="type=google.firebase.auth.user.v1.created"
```

**Error Handling and Retries**:
```python
# error_handling.py
import functions_framework
from google.cloud import pubsub_v1
import traceback
import time

@functions_framework.cloud_event
def resilient_function(cloud_event):
    """Function with comprehensive error handling"""
    try:
        # Process event
        process_event(cloud_event)

    except RetryableError as e:
        # Transient error - allow retry
        print(f"Retryable error: {e}")
        raise  # Re-raise to trigger retry

    except FatalError as e:
        # Permanent error - don't retry
        print(f"Fatal error: {e}")
        # Log to error reporting
        log_error(e, cloud_event)
        # Send to DLQ
        send_to_dlq(cloud_event)
        # Don't raise - prevent retry
        return

    except Exception as e:
        # Unknown error - log and decide
        print(f"Unknown error: {e}")
        print(traceback.format_exc())

        # Send to DLQ after multiple attempts
        attempt = cloud_event.data.get("message", {}).get("attributes", {}).get("retry_count", "0")
        if int(attempt) >= 3:
            send_to_dlq(cloud_event)
            return

        raise  # Retry

class RetryableError(Exception):
    """Transient errors that should be retried"""
    pass

class FatalError(Exception):
    """Permanent errors that should not be retried"""
    pass

def process_event(cloud_event):
    """Process event with validation"""
    data = cloud_event.data

    # Idempotency check
    message_id = data.get("message", {}).get("messageId")
    if is_already_processed(message_id):
        print(f"Message {message_id} already processed, skipping")
        return

    # Validate data
    if not validate_data(data):
        raise FatalError("Invalid data format")

    # Process
    result = do_processing(data)

    # Mark as processed
    mark_as_processed(message_id)

    return result

def send_to_dlq(cloud_event):
    """Send failed message to Dead Letter Queue"""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('project-id', 'dlq-topic')

    message_data = str(cloud_event.data).encode('utf-8')
    future = publisher.publish(topic_path, message_data)
    print(f"Sent to DLQ: {future.result()}")

# Deploy with retry configuration
# gcloud functions deploy resilient_function \
#   --gen2 \
#   --runtime=python311 \
#   --region=us-central1 \
#   --source=. \
#   --entry-point=resilient_function \
#   --trigger-topic=events \
#   --retry \
#   --max-retry-attempts=5 \
#   --min-retry-delay=10s \
#   --max-retry-delay=300s
```

**Advanced Configuration**:
```bash
# Complete deployment with all options
gcloud functions deploy my-function \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=main \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=my-sa@project.iam.gserviceaccount.com \
  --set-env-vars="ENV=prod,DEBUG=false" \
  --set-secrets="API_KEY=api-key:latest" \
  --memory=512MB \
  --timeout=300s \
  --min-instances=1 \
  --max-instances=100 \
  --concurrency=80 \
  --vpc-connector=my-connector \
  --ingress-settings=internal-and-gclb \
  --egress-settings=private-ranges-only

# Event-driven function
gcloud functions deploy event-function \
  --gen2 \
  --runtime=nodejs20 \
  --region=us-central1 \
  --source=. \
  --entry-point=handleEvent \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=my-bucket" \
  --trigger-location=us-central1 \
  --retry
```

### GKE for Developers
**Advantages**:
- Full Kubernetes features
- Microservices orchestration
- Service mesh (Istio)
- Complex deployments
- Portability

**Development Tools**:
- Skaffold for local development
- Cloud Code for IDE integration
- Config Connector for GCP resources
- Workload Identity for authentication

## Container Development Best Practices

### Dockerfile Optimization

**Multi-Stage Builds** (Python):
```dockerfile
# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/healthz')"

# Use exec form for proper signal handling
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "app:app"]
```

**Multi-Stage Builds** (Node.js):
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

# Security: Run as non-root
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./

USER nextjs

EXPOSE 8080
ENV NODE_ENV=production
ENV PORT=8080

CMD ["node", "dist/server.js"]
```

**Distroless Images** (Go):
```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build binary with optimizations
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-w -s" \
    -o main .

# Stage 2: Distroless (minimal, secure)
FROM gcr.io/distroless/static-debian11

WORKDIR /app

# Copy only the binary
COPY --from=builder /app/main .

# Distroless runs as non-root by default
USER nonroot:nonroot

EXPOSE 8080

# Must use exec form with distroless
ENTRYPOINT ["/app/main"]
```

**.dockerignore** (Important for build speed):
```
# .dockerignore - Reduce build context size
**/__pycache__
**/*.pyc
**/*.pyo
**/*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.git
.gitignore
.dockerignore
.env
.venv
venv/
ENV/
node_modules/
npm-debug.log
.DS_Store
*.md
!README.md
.pytest_cache
.coverage
htmlcov/
.tox/
.mypy_cache/
.idea/
.vscode/
*.swp
tests/
docs/
examples/
```

**Docker Best Practices**:
```dockerfile
# Complete example with all best practices
FROM python:3.11-slim AS base

# Metadata
LABEL maintainer="team@example.com"
LABEL version="1.0"
LABEL description="Production-ready Python application"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Build stage
FROM base AS builder

COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# Production stage
FROM base AS production

# Copy only Python packages
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')"

# Use exec form for proper signal handling
ENTRYPOINT ["python"]
CMD ["-m", "gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

### Cloud Build CI/CD Pipelines

**Complete Cloud Build Pipeline**:
```yaml
# cloudbuild.yaml - Comprehensive CI/CD pipeline
substitutions:
  _SERVICE_NAME: myapp
  _REGION: us-central1
  _IMAGE_NAME: gcr.io/${PROJECT_ID}/${_SERVICE_NAME}

# Build options
options:
  machineType: 'N1_HIGHCPU_8'
  substitution_option: 'ALLOW_LOOSE'
  logging: CLOUD_LOGGING_ONLY
  dynamic_substitutions: true

steps:
# Step 1: Run linting
- name: 'python:3.11-slim'
  id: 'lint'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      pip install flake8 black
      black --check . || exit 1
      flake8 . || exit 1

# Step 2: Run unit tests
- name: 'python:3.11-slim'
  id: 'test'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      pip install -r requirements.txt
      pip install pytest pytest-cov
      pytest tests/ --cov=. --cov-report=term-missing
  env:
    - 'DATABASE_URL=postgresql://test_db'

# Step 3: Security scanning
- name: 'gcr.io/cloud-builders/gcloud'
  id: 'security-scan'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      pip install bandit safety
      bandit -r . -x ./tests || exit 1
      safety check || exit 1

# Step 4: Build Docker image
- name: 'gcr.io/cloud-builders/docker'
  id: 'build'
  args:
    - 'build'
    - '--build-arg'
    - 'BUILD_DATE=${BUILD_ID}'
    - '--build-arg'
    - 'VCS_REF=${SHORT_SHA}'
    - '-t'
    - '${_IMAGE_NAME}:${SHORT_SHA}'
    - '-t'
    - '${_IMAGE_NAME}:${BRANCH_NAME}'
    - '-t'
    - '${_IMAGE_NAME}:latest'
    - '--cache-from'
    - '${_IMAGE_NAME}:latest'
    - '.'

# Step 5: Run vulnerability scanning
- name: 'gcr.io/cloud-builders/gcloud'
  id: 'vulnerability-scan'
  args:
    - 'container'
    - 'images'
    - 'scan'
    - '${_IMAGE_NAME}:${SHORT_SHA}'
  waitFor: ['build']

# Step 6: Push images to registry
- name: 'gcr.io/cloud-builders/docker'
  id: 'push'
  args:
    - 'push'
    - '--all-tags'
    - '${_IMAGE_NAME}'
  waitFor: ['build', 'vulnerability-scan']

# Step 7: Deploy to Cloud Run (staging)
- name: 'gcr.io/cloud-builders/gcloud'
  id: 'deploy-staging'
  args:
    - 'run'
    - 'deploy'
    - '${_SERVICE_NAME}-staging'
    - '--image=${_IMAGE_NAME}:${SHORT_SHA}'
    - '--region=${_REGION}'
    - '--platform=managed'
    - '--tag=staging'
    - '--no-traffic'
    - '--set-env-vars=ENV=staging'
  waitFor: ['push']

# Step 8: Run integration tests
- name: 'python:3.11-slim'
  id: 'integration-tests'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      pip install pytest requests
      export STAGING_URL=$(gcloud run services describe ${_SERVICE_NAME}-staging \
        --region=${_REGION} --format='value(status.url)')
      pytest integration_tests/ --base-url=$$STAGING_URL
  waitFor: ['deploy-staging']

# Step 9: Deploy to production with gradual rollout
- name: 'gcr.io/cloud-builders/gcloud'
  id: 'deploy-production'
  args:
    - 'run'
    - 'deploy'
    - '${_SERVICE_NAME}'
    - '--image=${_IMAGE_NAME}:${SHORT_SHA}'
    - '--region=${_REGION}'
    - '--platform=managed'
    - '--tag=v${SHORT_SHA}'
  waitFor: ['integration-tests']

# Step 10: Gradual traffic migration
- name: 'gcr.io/cloud-builders/gcloud'
  id: 'traffic-migration'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      # Get latest revision
      NEW_REV=$(gcloud run revisions list \
        --service=${_SERVICE_NAME} \
        --region=${_REGION} \
        --format='value(name)' \
        --limit=1)

      # Get previous revision
      OLD_REV=$(gcloud run revisions list \
        --service=${_SERVICE_NAME} \
        --region=${_REGION} \
        --format='value(name)' \
        --limit=1 \
        --offset=1)

      # Canary: 10% to new version
      gcloud run services update-traffic ${_SERVICE_NAME} \
        --region=${_REGION} \
        --to-revisions=$$OLD_REV=90,$$NEW_REV=10

      # Wait and monitor (in real scenario, check metrics)
      sleep 60

      # Full rollout
      gcloud run services update-traffic ${_SERVICE_NAME} \
        --region=${_REGION} \
        --to-latest
  waitFor: ['deploy-production']

# Store artifacts
images:
  - '${_IMAGE_NAME}:${SHORT_SHA}'
  - '${_IMAGE_NAME}:${BRANCH_NAME}'
  - '${_IMAGE_NAME}:latest'

# Artifacts for later analysis
artifacts:
  objects:
    location: 'gs://${PROJECT_ID}_cloudbuild/logs'
    paths:
      - 'test-results/**'
      - 'coverage/**'

# Timeout
timeout: 1800s  # 30 minutes
```

**Build Triggers**:
```bash
# Create GitHub trigger for main branch
gcloud builds triggers create github \
  --repo-name=my-repo \
  --repo-owner=my-org \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --description="Deploy to production on main branch" \
  --substitutions=_SERVICE_NAME=myapp,_REGION=us-central1

# Create trigger for feature branches
gcloud builds triggers create github \
  --repo-name=my-repo \
  --repo-owner=my-org \
  --branch-pattern="^feature/.*$" \
  --build-config=cloudbuild.yaml \
  --description="Build and test feature branches" \
  --substitutions=_SERVICE_NAME=myapp,_REGION=us-central1

# Create tag-based trigger for releases
gcloud builds triggers create github \
  --repo-name=my-repo \
  --repo-owner=my-org \
  --tag-pattern="^v[0-9]+\.[0-9]+\.[0-9]+$" \
  --build-config=cloudbuild.yaml \
  --description="Release build" \
  --substitutions=_SERVICE_NAME=myapp,_REGION=us-central1

# Pull request trigger (preview environment)
gcloud builds triggers create github \
  --repo-name=my-repo \
  --repo-owner=my-org \
  --pull-request-pattern="^main$" \
  --build-config=cloudbuild-pr.yaml \
  --comment-control=COMMENTS_ENABLED \
  --description="Preview environment for PRs"
```

### Artifact Registry

**Setup and Configuration**:
```bash
# Create Docker repository
gcloud artifacts repositories create my-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker images for my application"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build and push to Artifact Registry
docker build -t us-central1-docker.pkg.dev/PROJECT_ID/my-repo/myapp:v1.0.0 .
docker push us-central1-docker.pkg.dev/PROJECT_ID/my-repo/myapp:v1.0.0

# List images
gcloud artifacts docker images list us-central1-docker.pkg.dev/PROJECT_ID/my-repo

# Set cleanup policy
gcloud artifacts repositories set-cleanup-policies my-repo \
  --location=us-central1 \
  --policy=cleanup-policy.json
```

**cleanup-policy.json**:
```json
{
  "name": "delete-old-images",
  "action": "DELETE",
  "condition": {
    "olderThan": "2592000s",
    "tagState": "UNTAGGED"
  }
}
```

## API Development

### REST API Development

**Complete REST API Example** (Python/Flask):
```python
# api.py - Production-ready REST API
from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from google.cloud import firestore
from google.cloud import logging as cloud_logging
import functools
import jwt
import os

app = Flask(__name__)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per hour", "50 per minute"]
)

# Cloud Logging
logging_client = cloud_logging.Client()
logging_client.setup_logging()

# Firestore client
db = firestore.Client()

# Authentication decorator
def require_auth(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            abort(401, description='Missing or invalid authorization header')

        try:
            token = token.split('Bearer ')[1]
            decoded = jwt.decode(
                token,
                os.environ['JWT_SECRET'],
                algorithms=['HS256']
            )
            request.user_id = decoded['user_id']
        except jwt.ExpiredSignatureError:
            abort(401, description='Token expired')
        except jwt.InvalidTokenError:
            abort(401, description='Invalid token')

        return f(*args, **kwargs)
    return decorated_function

# Health check
@app.route('/healthz', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

# GET /api/v1/users - List users with pagination
@app.route('/api/v1/users', methods=['GET'])
@limiter.limit("100 per hour")
@require_auth
def list_users():
    # Pagination parameters
    page_size = int(request.args.get('page_size', 10))
    page_token = request.args.get('page_token')

    # Filtering
    status = request.args.get('status')

    # Query
    query = db.collection('users')
    if status:
        query = query.where('status', '==', status)

    query = query.limit(page_size)

    if page_token:
        # Resume from last document
        last_doc = db.collection('users').document(page_token).get()
        query = query.start_after(last_doc)

    users = []
    last_doc_id = None

    for doc in query.stream():
        users.append({
            'id': doc.id,
            **doc.to_dict()
        })
        last_doc_id = doc.id

    response = {
        'users': users,
        'page_size': page_size
    }

    if last_doc_id and len(users) == page_size:
        response['next_page_token'] = last_doc_id

    return jsonify(response), 200

# GET /api/v1/users/{user_id} - Get user by ID
@app.route('/api/v1/users/<user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    doc = db.collection('users').document(user_id).get()

    if not doc.exists:
        abort(404, description=f'User {user_id} not found')

    return jsonify({
        'id': doc.id,
        **doc.to_dict()
    }), 200

# POST /api/v1/users - Create user
@app.route('/api/v1/users', methods=['POST'])
@limiter.limit("20 per hour")
@require_auth
def create_user():
    data = request.get_json()

    # Validation
    if not data:
        abort(400, description='Request body is required')

    required_fields = ['email', 'name']
    for field in required_fields:
        if field not in data:
            abort(400, description=f'Missing required field: {field}')

    # Email validation
    import re
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
        abort(400, description='Invalid email format')

    # Create user
    user_ref = db.collection('users').document()
    user_data = {
        'email': data['email'],
        'name': data['name'],
        'status': 'active',
        'created_at': firestore.SERVER_TIMESTAMP,
        'created_by': request.user_id
    }
    user_ref.set(user_data)

    return jsonify({
        'id': user_ref.id,
        **user_data
    }), 201

# PUT /api/v1/users/{user_id} - Update user
@app.route('/api/v1/users/<user_id>', methods=['PUT'])
@require_auth
def update_user(user_id):
    data = request.get_json()

    if not data:
        abort(400, description='Request body is required')

    # Check if user exists
    user_ref = db.collection('users').document(user_id)
    if not user_ref.get().exists:
        abort(404, description=f'User {user_id} not found')

    # Update allowed fields
    update_data = {}
    allowed_fields = ['name', 'status', 'email']
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]

    update_data['updated_at'] = firestore.SERVER_TIMESTAMP
    update_data['updated_by'] = request.user_id

    user_ref.update(update_data)

    updated_doc = user_ref.get()
    return jsonify({
        'id': updated_doc.id,
        **updated_doc.to_dict()
    }), 200

# DELETE /api/v1/users/{user_id} - Delete user
@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
    user_ref = db.collection('users').document(user_id)

    if not user_ref.get().exists:
        abort(404, description=f'User {user_id} not found')

    # Soft delete
    user_ref.update({
        'status': 'deleted',
        'deleted_at': firestore.SERVER_TIMESTAMP,
        'deleted_by': request.user_id
    })

    return '', 204

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad Request',
        'message': str(error.description)
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'error': 'Unauthorized',
        'message': str(error.description)
    }), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': str(error.description)
    }), 404

@app.errorhandler(429)
def rate_limit_exceeded(error):
    return jsonify({
        'error': 'Too Many Requests',
        'message': 'Rate limit exceeded'
    }), 429

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal error: {error}')
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal error occurred'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
```

### gRPC API Development

**Protocol Buffer Definition**:
```protobuf
// user_service.proto
syntax = "proto3";

package user;

option go_package = "github.com/example/user-service/pb";

service UserService {
  // Unary RPC
  rpc GetUser (GetUserRequest) returns (User) {}
  rpc CreateUser (CreateUserRequest) returns (User) {}
  rpc UpdateUser (UpdateUserRequest) returns (User) {}
  rpc DeleteUser (DeleteUserRequest) returns (Empty) {}

  // Server streaming
  rpc ListUsers (ListUsersRequest) returns (stream User) {}

  // Client streaming
  rpc CreateUsers (stream CreateUserRequest) returns (CreateUsersResponse) {}

  // Bidirectional streaming
  rpc Chat (stream ChatMessage) returns (stream ChatMessage) {}
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  string status = 4;
  int64 created_at = 5;
}

message GetUserRequest {
  string id = 1;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
}

message UpdateUserRequest {
  string id = 1;
  string email = 2;
  string name = 3;
  string status = 4;
}

message DeleteUserRequest {
  string id = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
  string status = 3;
}

message CreateUsersResponse {
  int32 count = 1;
}

message ChatMessage {
  string user_id = 1;
  string message = 2;
  int64 timestamp = 3;
}

message Empty {}
```

**gRPC Server Implementation** (Go):
```go
// server.go
package main

import (
    "context"
    "fmt"
    "log"
    "net"
    "time"

    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
    "google.golang.org/grpc/metadata"
    "cloud.google.com/go/firestore"

    pb "github.com/example/user-service/pb"
)

type server struct {
    pb.UnimplementedUserServiceServer
    firestoreClient *firestore.Client
}

// Unary RPC
func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    // Authentication check
    if err := s.authenticate(ctx); err != nil {
        return nil, err
    }

    // Validate request
    if req.Id == "" {
        return nil, status.Error(codes.InvalidArgument, "user ID is required")
    }

    // Get user from Firestore
    doc, err := s.firestoreClient.Collection("users").Doc(req.Id).Get(ctx)
    if err != nil {
        if status.Code(err) == codes.NotFound {
            return nil, status.Errorf(codes.NotFound, "user %s not found", req.Id)
        }
        return nil, status.Error(codes.Internal, "failed to get user")
    }

    var user pb.User
    if err := doc.DataTo(&user); err != nil {
        return nil, status.Error(codes.Internal, "failed to parse user data")
    }

    user.Id = doc.Ref.ID
    return &user, nil
}

// Server streaming RPC
func (s *server) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
    ctx := stream.Context()

    if err := s.authenticate(ctx); err != nil {
        return err
    }

    query := s.firestoreClient.Collection("users").Limit(int(req.PageSize))

    if req.Status != "" {
        query = query.Where("status", "==", req.Status)
    }

    iter := query.Documents(ctx)
    defer iter.Stop()

    for {
        doc, err := iter.Next()
        if err == iterator.Done {
            break
        }
        if err != nil {
            return status.Error(codes.Internal, "failed to iterate users")
        }

        var user pb.User
        if err := doc.DataTo(&user); err != nil {
            continue
        }

        user.Id = doc.Ref.ID

        // Send user to stream
        if err := stream.Send(&user); err != nil {
            return err
        }
    }

    return nil
}

// Client streaming RPC
func (s *server) CreateUsers(stream pb.UserService_CreateUsersServer) error {
    ctx := stream.Context()

    if err := s.authenticate(ctx); err != nil {
        return err
    }

    count := 0
    batch := s.firestoreClient.Batch()

    for {
        req, err := stream.Recv()
        if err == io.EOF {
            // Commit batch
            if _, err := batch.Commit(ctx); err != nil {
                return status.Error(codes.Internal, "failed to create users")
            }

            return stream.SendAndClose(&pb.CreateUsersResponse{
                Count: int32(count),
            })
        }
        if err != nil {
            return err
        }

        // Validate
        if req.Email == "" || req.Name == "" {
            return status.Error(codes.InvalidArgument, "email and name are required")
        }

        // Add to batch
        ref := s.firestoreClient.Collection("users").NewDoc()
        batch.Set(ref, map[string]interface{}{
            "email":      req.Email,
            "name":       req.Name,
            "status":     "active",
            "created_at": time.Now().Unix(),
        })

        count++

        // Commit in batches of 500
        if count%500 == 0 {
            if _, err := batch.Commit(ctx); err != nil {
                return status.Error(codes.Internal, "failed to create users")
            }
            batch = s.firestoreClient.Batch()
        }
    }
}

// Authentication interceptor
func (s *server) authenticate(ctx context.Context) error {
    md, ok := metadata.FromIncomingContext(ctx)
    if !ok {
        return status.Error(codes.Unauthenticated, "missing metadata")
    }

    tokens := md.Get("authorization")
    if len(tokens) == 0 {
        return status.Error(codes.Unauthenticated, "missing authorization token")
    }

    // Validate JWT token
    // ... token validation logic ...

    return nil
}

func main() {
    // Create Firestore client
    ctx := context.Background()
    firestoreClient, err := firestore.NewClient(ctx, "project-id")
    if err != nil {
        log.Fatalf("Failed to create Firestore client: %v", err)
    }
    defer firestoreClient.Close()

    // Create gRPC server
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("Failed to listen: %v", err)
    }

    s := grpc.NewServer(
        grpc.UnaryInterceptor(loggingInterceptor),
    )

    pb.RegisterUserServiceServer(s, &server{
        firestoreClient: firestoreClient,
    })

    log.Printf("Server listening on :50051")
    if err := s.Serve(lis); err != nil {
        log.Fatalf("Failed to serve: %v", err)
    }
}

// Logging interceptor
func loggingInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    start := time.Now()
    resp, err := handler(ctx, req)
    duration := time.Since(start)

    log.Printf("Method: %s, Duration: %v, Error: %v", info.FullMethod, duration, err)

    return resp, err
}
```

### Cloud Endpoints (API Gateway)

**OpenAPI Configuration**:
```yaml
# openapi.yaml for Cloud Endpoints
swagger: "2.0"
info:
  title: User API
  description: User management API
  version: 1.0.0
host: myapi.endpoints.project-id.cloud.goog
schemes:
  - https
produces:
  - application/json
consumes:
  - application/json

# Security definitions
securityDefinitions:
  api_key:
    type: apiKey
    name: key
    in: query
  firebase:
    authorizationUrl: ""
    flow: implicit
    type: oauth2
    x-google-issuer: "https://securetoken.google.com/PROJECT_ID"
    x-google-jwks_uri: "https://www.googleapis.com/service_accounts/v1/metadata/x509/securetoken@system.gserviceaccount.com"
    x-google-audiences: "PROJECT_ID"

# Apply security globally
security:
  - api_key: []
  - firebase: []

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      parameters:
        - name: page_size
          in: query
          type: integer
          default: 10
        - name: page_token
          in: query
          type: string
      responses:
        200:
          description: Successful response
          schema:
            $ref: "#/definitions/UserList"
      x-google-quota:
        metricCosts:
          "read-requests": 1
    post:
      summary: Create user
      operationId: createUser
      parameters:
        - name: body
          in: body
          required: true
          schema:
            $ref: "#/definitions/CreateUserRequest"
      responses:
        201:
          description: User created
          schema:
            $ref: "#/definitions/User"
      x-google-quota:
        metricCosts:
          "write-requests": 1

  /users/{userId}:
    get:
      summary: Get user
      operationId: getUser
      parameters:
        - name: userId
          in: path
          required: true
          type: string
      responses:
        200:
          description: Successful response
          schema:
            $ref: "#/definitions/User"
        404:
          description: User not found
    delete:
      summary: Delete user
      operationId: deleteUser
      parameters:
        - name: userId
          in: path
          required: true
          type: string
      responses:
        204:
          description: User deleted
        404:
          description: User not found

definitions:
  User:
    type: object
    properties:
      id:
        type: string
      email:
        type: string
      name:
        type: string
      status:
        type: string
      created_at:
        type: integer

  CreateUserRequest:
    type: object
    required:
      - email
      - name
    properties:
      email:
        type: string
      name:
        type: string

  UserList:
    type: object
    properties:
      users:
        type: array
        items:
          $ref: "#/definitions/User"
      next_page_token:
        type: string

# API quotas
x-google-management:
  metrics:
    - name: "read-requests"
      displayName: "Read requests"
      description: "Number of read requests"
      valueType: INT64
      metricKind: DELTA
    - name: "write-requests"
      displayName: "Write requests"
      description: "Number of write requests"
      valueType: INT64
      metricKind: DELTA
  quota:
    limits:
      - name: "read-limit"
        metric: "read-requests"
        unit: "1/min/{project}"
        values:
          STANDARD: 1000
      - name: "write-limit"
        metric: "write-requests"
        unit: "1/min/{project}"
        values:
          STANDARD: 100
```

**Deploy Cloud Endpoints**:
```bash
# Deploy OpenAPI spec
gcloud endpoints services deploy openapi.yaml

# Deploy backend (Cloud Run)
gcloud run deploy myapi \
  --image gcr.io/project/myapi:latest \
  --region us-central1 \
  --platform managed

# Configure ESP (Extensible Service Proxy)
gcloud run services update myapi \
  --set-env-vars="ENDPOINTS_SERVICE_NAME=myapi.endpoints.project-id.cloud.goog"
```

### Authentication Patterns

**API Key Authentication**:
```python
# api_key_auth.py
from flask import request, abort
from google.cloud import firestore

db = firestore.Client()

def validate_api_key(api_key):
    """Validate API key against Firestore"""
    doc = db.collection('api_keys').document(api_key).get()

    if not doc.exists:
        return False

    key_data = doc.to_dict()

    # Check if key is active
    if key_data.get('status') != 'active':
        return False

    # Check rate limits
    if key_data.get('requests_today', 0) >= key_data.get('daily_limit', 1000):
        return False

    # Increment usage
    doc.reference.update({
        'requests_today': firestore.Increment(1),
        'last_used': firestore.SERVER_TIMESTAMP
    })

    return True

def require_api_key(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('key')

        if not api_key:
            abort(401, description='API key required')

        if not validate_api_key(api_key):
            abort(403, description='Invalid or expired API key')

        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/data')
@require_api_key
def get_data():
    return {'data': 'Protected resource'}
```

**OAuth 2.0 / Firebase Auth**:
```python
# oauth_auth.py
from firebase_admin import auth, credentials, initialize_app
from flask import request, abort
import functools

# Initialize Firebase Admin
cred = credentials.ApplicationDefault()
initialize_app(cred)

def verify_firebase_token(id_token):
    """Verify Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return None

def require_firebase_auth(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            abort(401, description='Missing authorization header')

        id_token = auth_header.split('Bearer ')[1]
        decoded_token = verify_firebase_token(id_token)

        if not decoded_token:
            abort(401, description='Invalid or expired token')

        # Attach user info to request
        request.user = {
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email'),
            'email_verified': decoded_token.get('email_verified', False)
        }

        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/profile')
@require_firebase_auth
def get_profile():
    return {
        'uid': request.user['uid'],
        'email': request.user['email']
    }
```

**Service-to-Service Authentication** (IAM):
```python
# service_auth.py
import google.auth
import google.auth.transport.requests
from google.oauth2 import id_token
import requests

def call_authenticated_service(service_url, payload=None):
    """Call another Cloud Run service with authentication"""
    # Get default credentials
    auth_req = google.auth.transport.requests.Request()

    # Generate ID token for target service
    token = id_token.fetch_id_token(auth_req, service_url)

    # Make request with token
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    if payload:
        response = requests.post(service_url, json=payload, headers=headers)
    else:
        response = requests.get(service_url, headers=headers)

    return response.json()

# Usage
result = call_authenticated_service(
    'https://backend-service-xyz.run.app/api/process',
    {'data': 'value'}
)
```

## Testing and Debugging

### Unit Testing with Cloud Services

**Testing Cloud Functions Locally**:
```python
# test_function.py
import pytest
from unittest.mock import Mock, patch
from main import process_pubsub_message

def test_process_pubsub_message():
    """Test Cloud Function with mocked Pub/Sub event"""
    # Mock Pub/Sub message
    mock_event = {
        'data': base64.b64encode(json.dumps({
            'user_id': '123',
            'action': 'create'
        }).encode()).decode(),
        'attributes': {
            'event_type': 'user.created'
        }
    }

    # Mock Firestore client
    with patch('main.firestore.Client') as mock_firestore:
        mock_db = Mock()
        mock_firestore.return_value = mock_db

        # Call function
        result = process_pubsub_message(mock_event, None)

        # Assertions
        mock_db.collection.assert_called_once_with('users')
        assert result == 'success'

# Run with: pytest test_function.py
```

**Testing Cloud Run with Flask**:
```python
# test_api.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_create_user(client, mocker):
    """Test user creation with mocked Firestore"""
    # Mock Firestore
    mock_firestore = mocker.patch('app.db')
    mock_collection = mock_firestore.collection.return_value
    mock_doc = mock_collection.document.return_value

    # Mock authentication
    mocker.patch('app.require_auth', lambda f: f)

    response = client.post('/api/v1/users', json={
        'email': 'test@example.com',
        'name': 'Test User'
    })

    assert response.status_code == 201
    assert 'id' in response.json
    mock_collection.document.assert_called_once()

def test_get_user_not_found(client, mocker):
    """Test 404 for non-existent user"""
    mock_firestore = mocker.patch('app.db')
    mock_doc = Mock()
    mock_doc.exists = False
    mock_firestore.collection.return_value.document.return_value.get.return_value = mock_doc

    mocker.patch('app.require_auth', lambda f: f)

    response = client.get('/api/v1/users/nonexistent')
    assert response.status_code == 404
```

**Integration Testing**:
```python
# integration_test.py
import pytest
import requests
import os

BASE_URL = os.environ.get('TEST_URL', 'http://localhost:8080')

@pytest.fixture(scope='module')
def auth_token():
    """Get authentication token for tests"""
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'username': 'test@example.com',
        'password': 'test_password'
    })
    return response.json()['token']

def test_end_to_end_user_workflow(auth_token):
    """Test complete user creation, retrieval, update, delete"""
    headers = {'Authorization': f'Bearer {auth_token}'}

    # Create user
    create_response = requests.post(f'{BASE_URL}/api/v1/users',
        headers=headers,
        json={
            'email': 'newuser@example.com',
            'name': 'New User'
        }
    )
    assert create_response.status_code == 201
    user_id = create_response.json()['id']

    # Get user
    get_response = requests.get(f'{BASE_URL}/api/v1/users/{user_id}',
        headers=headers
    )
    assert get_response.status_code == 200
    assert get_response.json()['email'] == 'newuser@example.com'

    # Update user
    update_response = requests.put(f'{BASE_URL}/api/v1/users/{user_id}',
        headers=headers,
        json={'name': 'Updated Name'}
    )
    assert update_response.status_code == 200
    assert update_response.json()['name'] == 'Updated Name'

    # Delete user
    delete_response = requests.delete(f'{BASE_URL}/api/v1/users/{user_id}',
        headers=headers
    )
    assert delete_response.status_code == 204

    # Verify deletion
    get_after_delete = requests.get(f'{BASE_URL}/api/v1/users/{user_id}',
        headers=headers
    )
    assert get_after_delete.status_code == 404
```

### Cloud Debugger

**Setup and Usage**:
```python
# Enable Cloud Debugger in your application
import googleclouddebugger

googleclouddebugger.enable(
    module='myapp',
    version='v1.0.0'
)

# Your application code
def process_order(order_id):
    order = get_order(order_id)
    # Cloud Debugger can snapshot here without stopping execution
    total = calculate_total(order)
    return total
```

```bash
# View debugger snapshots
gcloud debug snapshots list

# Create snapshot breakpoint
gcloud debug snapshots create \
  --location=main.py:42 \
  --condition="order_id == '12345'"

# List logpoints
gcloud debug logpoints list
```

### Cloud Profiler

**Integration**:
```python
# profiler_setup.py
import googlecloudprofiler

# Enable profiler
try:
    googlecloudprofiler.start(
        service='myapp',
        service_version='1.0.0',
        verbose=3
    )
except (ValueError, NotImplementedError) as exc:
    print(f'Failed to start profiler: {exc}')
```

```go
// Go profiler setup
import (
    "cloud.google.com/go/profiler"
)

func main() {
    cfg := profiler.Config{
        Service:        "myapp",
        ServiceVersion: "1.0.0",
    }

    if err := profiler.Start(cfg); err != nil {
        log.Fatalf("Failed to start profiler: %v", err)
    }

    // Your application code
}
```

### Cloud Trace

**OpenTelemetry Integration**:
```python
# tracing_setup.py
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup tracing
tracer_provider = TracerProvider()
cloud_trace_exporter = CloudTraceSpanExporter()
tracer_provider.add_span_processor(
    BatchSpanProcessor(cloud_trace_exporter)
)
trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer(__name__)

# Use in your code
@app.route('/api/process')
def process_request():
    with tracer.start_as_current_span('process_request'):
        # Your code here
        with tracer.start_as_current_span('database_query'):
            result = db.query('SELECT * FROM users')

        with tracer.start_as_current_span('external_api_call'):
            external_data = requests.get('https://api.example.com/data')

        return result
```

## Developer Tools and Workflows

### Cloud Code

**skaffold.yaml** for local development:
```yaml
# skaffold.yaml
apiVersion: skaffold/v2beta29
kind: Config
metadata:
  name: myapp

build:
  artifacts:
  - image: myapp
    docker:
      dockerfile: Dockerfile
    sync:
      manual:
      - src: "**/*.py"
        dest: /app

deploy:
  cloudrun:
    projectid: my-project
    region: us-central1

profiles:
- name: dev
  activation:
  - env: ENV=dev
  deploy:
    cloudrun:
      projectid: my-dev-project

- name: prod
  activation:
  - env: ENV=prod
  build:
    artifacts:
    - image: gcr.io/my-project/myapp
  deploy:
    cloudrun:
      projectid: my-project
      region: us-central1
```

### Cloud Shell

**Development Setup**:
```bash
# Cloud Shell environment setup
# Install dependencies
pip3 install --user flask google-cloud-firestore

# Set environment variables
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export PORT=8080

# Run application locally
python3 app.py

# Test with Cloud Shell web preview
curl http://localhost:8080/healthz

# Deploy from Cloud Shell
gcloud run deploy myapp \
  --source . \
  --region us-central1
```

## Real-World Development Scenarios

### Scenario 1: E-Commerce Order Processing System

**Architecture**:
```
User → Cloud Run (API) → Cloud SQL (Orders)
                        ↓
                     Pub/Sub (order.created)
                        ↓
                     Cloud Functions (process-order)
                        ↓
                     ├─→ Cloud Functions (charge-payment)
                     ├─→ Cloud Functions (update-inventory)
                     ├─→ Cloud Functions (send-notification)
                        ↓
                     Firestore (order status)
```

**Implementation**:
```python
# order_api.py - Cloud Run service
@app.route('/api/orders', methods=['POST'])
@require_auth
def create_order():
    data = request.get_json()

    # Validate order
    if not data.get('items') or not data.get('customer_id'):
        abort(400, 'Invalid order data')

    # Calculate total
    total = sum(item['price'] * item['quantity'] for item in data['items'])

    # Create order in Cloud SQL
    with db_pool.connect() as conn:
        result = conn.execute(
            sqlalchemy.text("""
                INSERT INTO orders (customer_id, total, status, created_at)
                VALUES (:customer_id, :total, 'PENDING', NOW())
                RETURNING id
            """),
            {
                'customer_id': data['customer_id'],
                'total': total
            }
        )
        order_id = result.fetchone()[0]

        # Insert order items
        for item in data['items']:
            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (:order_id, :product_id, :quantity, :price)
                """),
                {
                    'order_id': order_id,
                    'product_id': item['product_id'],
                    'quantity': item['quantity'],
                    'price': item['price']
                }
            )
        conn.commit()

    # Publish event to Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, 'order-created')
    message_data = json.dumps({
        'order_id': order_id,
        'customer_id': data['customer_id'],
        'total': total,
        'items': data['items']
    }).encode()

    future = publisher.publish(topic_path, message_data)
    future.result()

    return jsonify({'order_id': order_id, 'status': 'PENDING'}), 201

# process_order.py - Cloud Function
@functions_framework.cloud_event
def process_order(cloud_event):
    """Process order asynchronously"""
    message_data = json.loads(base64.b64decode(cloud_event.data['message']['data']))
    order_id = message_data['order_id']

    try:
        # Process payment
        payment_result = process_payment(message_data)

        if payment_result['success']:
            # Update inventory
            update_inventory(message_data['items'])

            # Update order status
            update_order_status(order_id, 'CONFIRMED')

            # Send confirmation email
            send_confirmation_email(message_data)
        else:
            update_order_status(order_id, 'FAILED')
            send_failure_notification(message_data)

    except Exception as e:
        print(f"Error processing order {order_id}: {e}")
        # Retry will be handled by Pub/Sub
        raise
```

### Scenario 2: Real-Time Data Analytics Pipeline

**Architecture**:
```
IoT Devices → Cloud Functions (HTTP) → Pub/Sub (raw-data)
                                          ↓
                                       Dataflow (process)
                                          ↓
                                       BigQuery (analytics)
                                          ↓
                                       Cloud Run (dashboard API)
```

**Implementation**:
```python
# ingest.py - Cloud Function for data ingestion
@functions_framework.http
def ingest_data(request):
    """Ingest IoT device data"""
    data = request.get_json()

    # Validate
    required_fields = ['device_id', 'timestamp', 'metrics']
    if not all(field in data for field in required_fields):
        return 'Invalid data', 400

    # Add metadata
    data['ingestion_time'] = datetime.utcnow().isoformat()

    # Publish to Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, 'iot-raw-data')

    message_json = json.dumps(data)
    future = publisher.publish(
        topic_path,
        message_json.encode('utf-8'),
        device_id=data['device_id']
    )

    try:
        future.result(timeout=5)
        return {'status': 'success', 'message_id': future.result()}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

# analytics_api.py - Cloud Run dashboard API
@app.route('/api/analytics/realtime', methods=['GET'])
@require_auth
def get_realtime_analytics():
    """Get real-time analytics from BigQuery"""
    device_id = request.args.get('device_id')

    query = """
        SELECT
            device_id,
            TIMESTAMP_TRUNC(timestamp, MINUTE) as minute,
            AVG(metrics.temperature) as avg_temp,
            MAX(metrics.temperature) as max_temp,
            MIN(metrics.temperature) as min_temp,
            COUNT(*) as reading_count
        FROM `project.dataset.iot_data`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
    """

    if device_id:
        query += f" AND device_id = '{device_id}'"

    query += """
        GROUP BY device_id, minute
        ORDER BY minute DESC
        LIMIT 100
    """

    from google.cloud import bigquery
    client = bigquery.Client()
    query_job = client.query(query)

    results = []
    for row in query_job:
        results.append({
            'device_id': row.device_id,
            'timestamp': row.minute.isoformat(),
            'avg_temperature': float(row.avg_temp),
            'max_temperature': float(row.max_temp),
            'min_temperature': float(row.min_temp),
            'reading_count': row.reading_count
        })

    return jsonify(results), 200
```

### Scenario 3: Image Processing Service

**Architecture**:
```
User Upload → Cloud Storage (upload bucket)
                 ↓ (trigger)
              Cloud Functions (process-image)
                 ↓
              ├─→ Vision API (analyze)
              ├─→ Cloud Storage (processed bucket)
              └─→ Firestore (metadata)
```

**Implementation**:
```python
# process_image.py
@functions_framework.cloud_event
def process_image(cloud_event):
    """Process uploaded image"""
    from google.cloud import storage, vision, firestore
    from PIL import Image
    import io

    data = cloud_event.data
    bucket_name = data['bucket']
    file_name = data['name']

    print(f"Processing: gs://{bucket_name}/{file_name}")

    # Initialize clients
    storage_client = storage.Client()
    vision_client = vision.ImageAnnotatorClient()
    db = firestore.Client()

    # Download image
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    image_bytes = blob.download_as_bytes()

    # Analyze with Vision API
    image = vision.Image(content=image_bytes)

    # Multiple analyses
    response_label = vision_client.label_detection(image=image)
    response_safe = vision_client.safe_search_detection(image=image)
    response_text = vision_client.text_detection(image=image)

    labels = [label.description for label in response_label.label_annotations]
    safe_search = response_safe.safe_search_annotation
    text = response_text.text_annotations[0].description if response_text.text_annotations else ''

    # Check if image is safe
    if (safe_search.adult == vision.Likelihood.VERY_LIKELY or
        safe_search.violence == vision.Likelihood.VERY_LIKELY):
        print("Image flagged as unsafe, not processing further")
        return

    # Resize image
    pil_image = Image.open(io.BytesIO(image_bytes))

    # Create thumbnail
    pil_image.thumbnail((300, 300))
    thumb_bytes = io.BytesIO()
    pil_image.save(thumb_bytes, format='JPEG')
    thumb_bytes.seek(0)

    # Upload processed images
    processed_bucket = storage_client.bucket(f"{bucket_name}-processed")

    # Original size
    original_blob = processed_bucket.blob(f"original/{file_name}")
    original_blob.upload_from_string(image_bytes, content_type='image/jpeg')

    # Thumbnail
    thumb_blob = processed_bucket.blob(f"thumbnails/{file_name}")
    thumb_blob.upload_from_string(thumb_bytes.read(), content_type='image/jpeg')

    # Save metadata to Firestore
    doc_ref = db.collection('images').document()
    doc_ref.set({
        'file_name': file_name,
        'original_url': original_blob.public_url,
        'thumbnail_url': thumb_blob.public_url,
        'labels': labels,
        'text_detected': text,
        'size_bytes': blob.size,
        'uploaded_at': firestore.SERVER_TIMESTAMP,
        'processed_at': firestore.SERVER_TIMESTAMP
    })

    print(f"Image processed successfully: {doc_ref.id}")
```

## Professional Cloud Developer Exam Tips

### Critical Exam Topics

**1. Platform Selection**:
```
Choose App Engine Standard when:
- Need automatic scaling to zero
- Standard language runtimes sufficient
- Want free tier
- Quick startup time critical

Choose App Engine Flexible when:
- Need custom runtime/Dockerfile
- SSH access required
- Long-running requests (up to 60 min)

Choose Cloud Run when:
- Containerized application
- HTTP/HTTPS only
- Need latest container features
- Scale to zero with fast cold starts

Choose Cloud Functions when:
- Event-driven workloads
- Small, focused functions
- Simplest deployment model

Choose GKE when:
- Complex Kubernetes requirements
- Service mesh needed
- Multiple services orchestration
- Need full container control
```

**2. Common Exam Patterns**:
- Scenario-based questions about choosing the right compute platform
- Configuration questions (app.yaml, cloudbuild.yaml, Dockerfile)
- API design and authentication patterns
- CI/CD pipeline design
- Error handling and retry logic
- Concurrency and scaling configurations
- Security best practices
- Cost optimization strategies

**3. Key Configuration Differences**:
```yaml
# App Engine Standard - app.yaml
runtime: python311
instance_class: F2
automatic_scaling:
  max_instances: 10

# vs Cloud Run - service.yaml
spec:
  template:
    spec:
      containerConcurrency: 80
      containers:
      - image: gcr.io/project/image
```

**4. Common Mistakes to Avoid**:
- Using Cloud Functions for long-running tasks (use Cloud Run instead)
- Not implementing idempotency in event-driven functions
- Forgetting to set --no-traffic for canary deployments
- Missing error handling and retry logic
- Not using connection pooling with Cloud SQL
- Storing state in container filesystem (ephemeral)
- Ignoring cold start optimization
- Not implementing proper health checks

**5. Best Practices for Exam**:
- Know gcloud command syntax for deploy, update, and traffic split
- Understand when to use sync vs async communication
- Remember authentication patterns (API keys, OAuth, service-to-service)
- Know Cloud Build substitution variables
- Understand Dockerfile multi-stage builds
- Know OpenAPI/Swagger specification basics
- Understand event structure for different Cloud Function triggers

**6. Debugging Scenarios**:
```
Problem: High latency
Solutions:
- Add caching (Memorystore)
- Optimize database queries
- Use CDN for static content
- Increase concurrency settings
- Add connection pooling

Problem: Cold starts
Solutions:
- Use min-instances > 0
- Enable CPU boost (Cloud Run)
- Optimize container size
- Use distroless images
- Keep functions warm

Problem: Rate limiting
Solutions:
- Implement exponential backoff
- Use Pub/Sub for async processing
- Add API Gateway quotas
- Use batch operations
```

### Study Checklist

- [ ] Deploy sample app to all platforms (App Engine, Cloud Run, Cloud Functions)
- [ ] Create complete CI/CD pipeline with Cloud Build
- [ ] Implement REST and gRPC APIs
- [ ] Practice Dockerfile multi-stage builds
- [ ] Set up Cloud Endpoints or Apigee
- [ ] Implement all authentication patterns
- [ ] Configure traffic splitting and gradual rollouts
- [ ] Use Cloud Debugger and Cloud Profiler
- [ ] Create event-driven architecture with Pub/Sub
- [ ] Practice app.yaml, cloudbuild.yaml, and OpenAPI configurations

### Time Management
- Professional level expects deeper understanding than Associate
- Scenario questions require architecture knowledge
- Code examples in questions need careful reading
- Practice reading YAML/JSON configurations quickly

## Key Commands Reference

### App Engine Commands
```bash
# Deploy application
gcloud app deploy app.yaml --version=v2 --no-promote

# Deploy multiple services
gcloud app deploy default-service/app.yaml api-service/app.yaml

# List services and versions
gcloud app services list
gcloud app versions list --service=default

# Traffic management
gcloud app services set-traffic default --splits=v1=0.5,v2=0.5 --split-by=ip
gcloud app services set-traffic default --migrate  # Gradual migration

# View logs
gcloud app logs tail --service=default --version=v1

# Manage versions
gcloud app versions stop v1 --service=default
gcloud app versions delete v1 --service=default

# Deploy configuration files
gcloud app deploy cron.yaml
gcloud app deploy dispatch.yaml
gcloud app deploy queue.yaml

# Access instances
gcloud app instances list
gcloud app instances ssh INSTANCE --service=default --version=v1

# Describe application
gcloud app describe
gcloud app browse  # Open in browser
```

### Cloud Run Commands
```bash
# Deploy from image
gcloud run deploy SERVICE \
  --image=gcr.io/PROJECT/IMAGE:TAG \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --memory=1Gi \
  --cpu=2 \
  --timeout=300 \
  --concurrency=80 \
  --min-instances=1 \
  --max-instances=100 \
  --no-cpu-throttling \
  --cpu-boost

# Deploy from source
gcloud run deploy SERVICE --source=. --region=us-central1

# Update service configuration
gcloud run services update SERVICE \
  --set-env-vars="KEY1=value1,KEY2=value2" \
  --set-secrets="SECRET=secret-name:latest" \
  --region=us-central1

# Traffic management
gcloud run services update-traffic SERVICE \
  --to-revisions=REVISION1=50,REVISION2=50 \
  --region=us-central1

gcloud run services update-traffic SERVICE \
  --to-tags=stable=90,canary=10 \
  --region=us-central1

# Manage revisions
gcloud run revisions list --service=SERVICE --region=us-central1
gcloud run revisions describe REVISION --region=us-central1
gcloud run revisions delete REVISION --region=us-central1

# View logs
gcloud run services logs read SERVICE --region=us-central1 --limit=100

# Get service URL
gcloud run services describe SERVICE --region=us-central1 --format='value(status.url)'

# Delete service
gcloud run services delete SERVICE --region=us-central1

# Jobs (2nd gen)
gcloud run jobs create JOB --image=gcr.io/PROJECT/IMAGE --region=us-central1
gcloud run jobs execute JOB --region=us-central1
gcloud run jobs list --region=us-central1
```

### Cloud Functions Commands
```bash
# Deploy HTTP function (2nd gen)
gcloud functions deploy FUNCTION \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=main \
  --trigger-http \
  --allow-unauthenticated \
  --memory=512MB \
  --timeout=300s \
  --min-instances=1 \
  --max-instances=100

# Deploy Pub/Sub function
gcloud functions deploy FUNCTION \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=process_pubsub \
  --trigger-topic=TOPIC \
  --retry

# Deploy Storage function
gcloud functions deploy FUNCTION \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=process_image \
  --trigger-bucket=BUCKET \
  --retry

# Deploy Firestore function
gcloud functions deploy FUNCTION \
  --gen2 \
  --runtime=nodejs20 \
  --region=us-central1 \
  --source=. \
  --entry-point=processFirestoreEvent \
  --trigger-event-filters="type=google.cloud.firestore.document.v1.written" \
  --trigger-event-filters="database=(default)" \
  --trigger-event-filters-path-pattern="document=users/{userId}"

# Call function
gcloud functions call FUNCTION --region=us-central1 --data='{"key":"value"}'

# View logs
gcloud functions logs read FUNCTION --region=us-central1 --limit=100

# List functions
gcloud functions list --region=us-central1

# Describe function
gcloud functions describe FUNCTION --region=us-central1

# Delete function
gcloud functions delete FUNCTION --region=us-central1

# Set environment variables
gcloud functions deploy FUNCTION \
  --set-env-vars=KEY1=value1,KEY2=value2 \
  --region=us-central1
```

### Cloud Build Commands
```bash
# Submit build manually
gcloud builds submit --config=cloudbuild.yaml

# Submit with substitutions
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_SERVICE_NAME=myapp,_REGION=us-central1

# Submit from specific location
gcloud builds submit --config=cloudbuild.yaml gs://bucket/source.tar.gz

# List builds
gcloud builds list --limit=10

# Describe build
gcloud builds describe BUILD_ID

# View build logs
gcloud builds log BUILD_ID

# Stream logs for running build
gcloud builds log BUILD_ID --stream

# Cancel build
gcloud builds cancel BUILD_ID

# Create GitHub trigger
gcloud builds triggers create github \
  --repo-name=REPO \
  --repo-owner=OWNER \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --substitutions=_SERVICE=myapp

# Create tag trigger
gcloud builds triggers create github \
  --repo-name=REPO \
  --repo-owner=OWNER \
  --tag-pattern="^v[0-9]+\.[0-9]+\.[0-9]+$" \
  --build-config=cloudbuild.yaml

# List triggers
gcloud builds triggers list

# Run trigger manually
gcloud builds triggers run TRIGGER_NAME --branch=main

# Delete trigger
gcloud builds triggers delete TRIGGER_ID
```

### Artifact Registry Commands
```bash
# Create repository
gcloud artifacts repositories create REPO \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker images"

# List repositories
gcloud artifacts repositories list --location=us-central1

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build and push image
docker build -t us-central1-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG .
docker push us-central1-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG

# List images
gcloud artifacts docker images list us-central1-docker.pkg.dev/PROJECT/REPO

# List tags
gcloud artifacts docker tags list us-central1-docker.pkg.dev/PROJECT/REPO/IMAGE

# Delete image
gcloud artifacts docker images delete \
  us-central1-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG

# Scan for vulnerabilities
gcloud artifacts docker images scan us-central1-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG

# View vulnerability scan results
gcloud artifacts docker images list-vulnerabilities \
  us-central1-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG
```

### Docker Commands for Development
```bash
# Build image
docker build -t myapp:latest .

# Build with build arguments
docker build --build-arg VERSION=1.0.0 -t myapp:latest .

# Build with target stage
docker build --target production -t myapp:latest .

# Run container locally
docker run -p 8080:8080 -e PORT=8080 myapp:latest

# Run with environment file
docker run --env-file .env -p 8080:8080 myapp:latest

# Run in background
docker run -d -p 8080:8080 --name myapp myapp:latest

# View logs
docker logs myapp
docker logs -f myapp  # Follow logs

# Execute command in container
docker exec -it myapp /bin/bash

# Stop and remove container
docker stop myapp
docker rm myapp

# List containers
docker ps
docker ps -a  # All containers

# List images
docker images

# Remove image
docker rmi myapp:latest

# Prune unused resources
docker system prune -a  # Remove all unused images, containers, networks
```

### Development and Debugging Commands
```bash
# Cloud Debugger
gcloud debug snapshots list
gcloud debug snapshots create --location=main.py:42 --condition="x > 10"
gcloud debug logpoints list

# Cloud Profiler (view in Console)
# Integrated into application via SDK

# Cloud Trace (view in Console)
# Integrated into application via OpenTelemetry

# View application logs
gcloud logging read "resource.type=cloud_run_revision" --limit=100
gcloud logging read "resource.type=cloud_function" --limit=100
gcloud logging read "resource.type=gae_app" --limit=100

# Tail logs
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=myapp"

# Cloud Shell
cloudshell download FILE  # Download file from Cloud Shell
cloudshell upload FILE    # Upload file to Cloud Shell

# Port forwarding (for local development)
gcloud compute ssh INSTANCE -- -L 8080:localhost:8080
```

### IAM and Service Accounts
```bash
# Create service account
gcloud iam service-accounts create SA_NAME --display-name="Display Name"

# Grant roles to service account
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_NAME@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

# Generate key file (for local testing only)
gcloud iam service-accounts keys create key.json \
  --iam-account=SA_NAME@PROJECT_ID.iam.gserviceaccount.com

# Allow service account to invoke Cloud Run
gcloud run services add-iam-policy-binding SERVICE \
  --member="serviceAccount:SA_NAME@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.invoker" \
  --region=us-central1

# Allow allUsers to invoke (public)
gcloud run services add-iam-policy-binding SERVICE \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=us-central1
```

## Additional Resources

### Official Documentation
- [Professional Cloud Developer Exam Guide](https://cloud.google.com/learn/certification/cloud-developer)
- [App Engine Documentation](https://cloud.google.com/appengine/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Artifact Registry Documentation](https://cloud.google.com/artifact-registry/docs)
- [Cloud Endpoints Documentation](https://cloud.google.com/endpoints/docs)
- [gRPC on GCP](https://cloud.google.com/endpoints/docs/grpc)

### Best Practices and Patterns
- [12-Factor App Methodology](https://12factor.net/)
- [Google Cloud Architecture Center](https://cloud.google.com/architecture)
- [Cloud Run Best Practices](https://docs.cloud.google.com/run/docs/tips/general)
- [Container Image Best Practices](https://cloud.google.com/architecture/best-practices-for-building-containers)
- [Microservices on GCP](https://cloud.google.com/learn/what-is-microservices-architecture)

### Code Samples and Labs
- [Google Cloud Code Samples](https://github.com/GoogleCloudPlatform)
- [Codelabs](https://codelabs.developers.google.com/?cat=Cloud)
- [Qwiklabs](https://www.qwiklabs.com/)
- [Cloud Skills Boost](https://www.cloudskillsboost.google/)

### Tools and SDKs
- [Google Cloud SDK](https://cloud.google.com/sdk/docs)
- [Cloud Code IDE Extension](https://cloud.google.com/code)
- [Skaffold](https://skaffold.dev/)
- [OpenTelemetry](https://opentelemetry.io/)
- [Protocol Buffers](https://protobuf.dev/)

### Community Resources
- [GCP Community](https://www.googlecloudcommunity.com/)
- [Stack Overflow - GCP](https://stackoverflow.com/questions/tagged/google-cloud-platform)
- [Google Cloud Blog](https://cloud.google.com/blog/products/application-development)
- [Cloud Run FAQ](https://github.com/ahmetb/cloud-run-faq)

## Key terms

- **Cloud Run** - a Google Cloud service that runs stateless containers and scales them automatically, including down to zero.
- **App Engine** - a Google Cloud platform for running applications without managing servers, in standard and flexible environments.
- **Cloud Run functions** (formerly Cloud Functions) - a Google Cloud serverless service that runs single-purpose functions in response to events or HTTP requests.
- **Cloud Tasks** - a Google Cloud service for queuing and dispatching asynchronous tasks to a worker or HTTP endpoint.
- **Eventarc** - a Google Cloud service that routes events from Google Cloud services and other sources to targets such as Cloud Run.
- **Secret Manager** - a Google Cloud service for storing and versioning secrets such as API keys and passwords.
- **Workload Identity Federation for GKE** - a way to use IAM policies to grant Kubernetes workloads access to Google Cloud APIs without exported keys.
- **Application Default Credentials (ADC)** - a strategy that client libraries use to find credentials automatically from the environment.
