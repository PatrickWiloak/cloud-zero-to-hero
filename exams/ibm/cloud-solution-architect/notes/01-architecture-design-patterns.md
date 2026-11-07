# IBM Cloud Solution Architect (C1000-175) - Architecture & Design Patterns

## Table of Contents
- [Architectural Principles](#architectural-principles)
- [Cloud-Native Architecture Patterns](#cloud-native-architecture-patterns)
- [Microservices Architecture](#microservices-architecture)
- [Event-Driven Architecture](#event-driven-architecture)
- [Multi-Cloud and Hybrid Cloud](#multi-cloud-and-hybrid-cloud)
- [High Availability Architecture](#high-availability-architecture)
- [Exam Tips](#exam-tips)

---

## Architectural Principles

### Well-Architected Framework
```yaml
# ibm-cloud-architecture-principles.yaml
well_architected_pillars:
  operational_excellence:
    - Infrastructure as Code
    - Automated deployments
    - Monitoring and observability
    - Continuous improvement
    - Runbook automation

  security:
    - Zero trust architecture
    - Defense in depth
    - Encryption at rest and in transit
    - Identity and access management
    - Compliance automation

  reliability:
    - High availability design
    - Disaster recovery planning
    - Fault tolerance
    - Auto-scaling
    - Circuit breakers

  performance_efficiency:
    - Right-sizing resources
    - Auto-scaling policies
    - CDN utilization
    - Database optimization
    - Caching strategies

  cost_optimization:
    - Resource tagging
    - Usage monitoring
    - Reserved capacity
    - Spot instances
    - Lifecycle policies

design_principles:
  scalability:
    horizontal: "Scale out with instances"
    vertical: "Scale up with resources"
    auto_scaling: "Dynamic based on metrics"

  resilience:
    redundancy: "Multi-zone deployment"
    fault_tolerance: "Graceful degradation"
    recovery: "Automated failover"

  modularity:
    microservices: "Loosely coupled services"
    apis: "Well-defined interfaces"
    containers: "Portable workloads"

  observability:
    metrics: "Quantitative measurements"
    logs: "Event tracking"
    traces: "Request flows"
    alerting: "Proactive notifications"
```

### Architecture Decision Records (ADR)
```markdown
# ADR-001: Multi-Zone Kubernetes Deployment

## Status
Accepted

## Context
Application requires 99.99% availability SLA and must handle zone failures without service interruption.

## Decision
Deploy Kubernetes workloads across three availability zones in us-south region with zone-aware pod scheduling and cross-zone load balancing.

## Consequences
Positive:
- High availability during zone failures
- Improved fault tolerance
- Better resource distribution
- Geographic redundancy

Negative:
- Increased cross-zone data transfer costs
- Additional complexity in deployment
- Higher infrastructure costs

## Implementation
terraform
resource "ibm_container_vpc_cluster" "multi_zone_cluster" {
  name              = "production-cluster"
  vpc_id            = ibm_is_vpc.vpc.id
  flavor            = "bx2.4x16"
  worker_count      = 3
  zones {
    subnet_id = ibm_is_subnet.zone1.id
    name      = "us-south-1"
  }
  zones {
    subnet_id = ibm_is_subnet.zone2.id
    name      = "us-south-2"
  }
  zones {
    subnet_id = ibm_is_subnet.zone3.id
    name      = "us-south-3"
  }
}
```

---

## Cloud-Native Architecture Patterns

### 12-Factor App Principles
```yaml
# twelve-factor-app-implementation.yaml
twelve_factors:
  1_codebase:
    principle: "One codebase tracked in version control"
    implementation: "Git repository with CI/CD"
    example: "GitHub with IBM Cloud Toolchain"

  2_dependencies:
    principle: "Explicitly declare and isolate dependencies"
    implementation: "Package managers, container images"
    example: "package.json, requirements.txt, Dockerfile"

  3_config:
    principle: "Store config in environment"
    implementation: "ConfigMaps, Secrets, environment variables"
    example: "Kubernetes ConfigMaps for non-sensitive data"

  4_backing_services:
    principle: "Treat backing services as attached resources"
    implementation: "Service binding, connection strings in env"
    example: "IBM Cloud service credentials"

  5_build_release_run:
    principle: "Strictly separate build and run stages"
    implementation: "CI/CD pipeline with stages"
    example: "Tekton/Jenkins pipeline"

  6_processes:
    principle: "Execute app as stateless processes"
    implementation: "Stateless containers, external state storage"
    example: "Redis for session, RDS for data"

  7_port_binding:
    principle: "Export services via port binding"
    implementation: "Container port exposure"
    example: "containerPort: 8080"

  8_concurrency:
    principle: "Scale out via process model"
    implementation: "Horizontal pod autoscaling"
    example: "HPA based on CPU/memory/custom metrics"

  9_disposability:
    principle: "Fast startup and graceful shutdown"
    implementation: "Optimized container images, signal handling"
    example: "SIGTERM handling for graceful shutdown"

  10_dev_prod_parity:
    principle: "Keep dev, staging, prod similar"
    implementation: "Same images, IaC for all environments"
    example: "Terraform workspaces per environment"

  11_logs:
    principle: "Treat logs as event streams"
    implementation: "stdout/stderr to log aggregation"
    example: "LogDNA for centralized logging"

  12_admin_processes:
    principle: "Run admin tasks as one-off processes"
    implementation: "Kubernetes Jobs, CronJobs"
    example: "Database migrations as init containers"
```

### Cloud-Native Application Structure
```python
# cloud_native_app.py
"""
Example cloud-native application following best practices
"""
import os
import logging
import signal
import sys
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import redis
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configuration from environment
class Config:
    # Required configuration
    PORT = int(os.getenv('PORT', 8080))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Backing services
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

    # IBM Cloud services
    WATSON_API_KEY = os.getenv('WATSON_API_KEY')
    WATSON_URL = os.getenv('WATSON_URL')

# Logging setup
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # Logs to stdout for aggregation
)
logger = logging.getLogger(__name__)

# Metrics
request_count = Counter('app_requests_total', 'Total requests')
request_duration = Histogram('app_request_duration_seconds', 'Request duration')

# Flask app
app = Flask(__name__)

# External services (initialized lazily)
redis_client = None
watson_translator = None

def get_redis():
    """Lazy initialization of Redis client"""
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(Config.REDIS_URL)
    return redis_client

def get_watson():
    """Lazy initialization of Watson service"""
    global watson_translator
    if watson_translator is None and Config.WATSON_API_KEY:
        authenticator = IAMAuthenticator(Config.WATSON_API_KEY)
        watson_translator = LanguageTranslatorV3(
            version='2018-05-01',
            authenticator=authenticator
        )
        watson_translator.set_service_url(Config.WATSON_URL)
    return watson_translator

# Health checks
@app.route('/healthz')
def health():
    """Liveness probe - is app running?"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/ready')
def ready():
    """Readiness probe - can app handle traffic?"""
    try:
        # Check backing services
        r = get_redis()
        r.ping()
        return jsonify({'status': 'ready'}), 200
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return jsonify({'status': 'not ready', 'error': str(e)}), 503

# Metrics endpoint
@app.route('/metrics')
def metrics():
    """Prometheus metrics"""
    return generate_latest()

# Business logic
@app.route('/translate', methods=['POST'])
@request_duration.time()
def translate():
    """Example business endpoint"""
    request_count.inc()

    try:
        # Business logic here
        translator = get_watson()
        # ... translation logic ...

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Graceful shutdown
def shutdown_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Received shutdown signal, cleaning up...")

    # Close connections
    if redis_client:
        redis_client.close()

    # Exit
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == '__main__':
    logger.info(f"Starting application on port {Config.PORT}")
    app.run(host='0.0.0.0', port=Config.PORT)
```

---

## Microservices Architecture

### Microservices Design Patterns
```yaml
# microservices-patterns.yaml
patterns:
  decomposition:
    by_business_capability:
      example: "Order Service, Payment Service, Inventory Service"
      benefits: "Clear ownership, independent scaling"

    by_subdomain:
      example: "User Management, Product Catalog, Shopping Cart"
      benefits: "Domain-driven design alignment"

  communication:
    synchronous:
      pattern: "REST API, gRPC"
      use_case: "Request-response, real-time queries"
      example: "API Gateway -> Microservices"

    asynchronous:
      pattern: "Event-driven, Message queues"
      use_case: "Eventual consistency, high throughput"
      example: "Event Streams (Kafka), RabbitMQ"

  data_management:
    database_per_service:
      description: "Each service owns its database"
      benefits: "Loose coupling, independent scaling"
      challenges: "Data consistency, queries across services"

    saga_pattern:
      description: "Distributed transactions"
      types: "Choreography, Orchestration"
      example: "Order -> Payment -> Inventory saga"

    cqrs:
      description: "Command Query Responsibility Segregation"
      benefits: "Optimized read/write models"
      use_case: "High read vs write ratio"

  resiliency:
    circuit_breaker:
      description: "Prevent cascade failures"
      states: "Closed, Open, Half-Open"
      implementation: "Istio, Resilience4j"

    bulkhead:
      description: "Isolate resources"
      example: "Thread pools per service"
      benefit: "Fault isolation"

    retry:
      description: "Retry failed requests"
      strategy: "Exponential backoff with jitter"
      max_retries: 3

    timeout:
      description: "Limit wait time"
      recommended: "Based on SLO requirements"
```

### Microservices on IBM Cloud
```bash
# Deploy microservices architecture on IBM Cloud

# 1. Create OpenShift cluster for microservices
ibmcloud oc cluster create vpc-gen2 \
  --name microservices-cluster \
  --version 4.14_openshift \
  --zone us-south-1 \
  --flavor bx2.8x32 \
  --workers 6 \
  --vpc-id $VPC_ID \
  --subnet-id $SUBNET_ID

# 2. Install Istio service mesh
kubectl create namespace istio-system
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/manifests/profiles/default.yaml

# 3. Deploy microservices with Istio sidecar injection
kubectl label namespace default istio-injection=enabled

# 4. Deploy API Gateway
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: api-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: api-gateway-cert
    hosts:
    - "api.example.com"
EOF

# 5. Configure virtual services for routing
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service-routes
spec:
  hosts:
  - "api.example.com"
  gateways:
  - api-gateway
  http:
  - match:
    - uri:
        prefix: /api/users
    route:
    - destination:
        host: user-service
        port:
          number: 8080
      weight: 90
    - destination:
        host: user-service-v2
        port:
          number: 8080
      weight: 10  # Canary deployment
EOF

# 6. Configure circuit breaker
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: user-service-circuit-breaker
spec:
  host: user-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 40
EOF

# 7. Set up Event Streams for asynchronous communication
ibmcloud resource service-instance-create \
  event-streams-microservices \
  messagehub \
  standard \
  us-south

# Create topics
ibmcloud es topic-create order-events --partitions 3
ibmcloud es topic-create payment-events --partitions 3
ibmcloud es topic-create inventory-events --partitions 3
```

### Terraform Microservices Infrastructure
```hcl
# microservices-infrastructure.tf

# OpenShift cluster for microservices
resource "ibm_container_vpc_cluster" "microservices_cluster" {
  name              = "microservices-cluster"
  vpc_id            = ibm_is_vpc.vpc.id
  flavor            = "bx2.8x32"
  worker_count      = 6
  kube_version      = "4.14_openshift"
  resource_group_id = data.ibm_resource_group.default.id

  zones {
    subnet_id = ibm_is_subnet.zone1.id
    name      = "us-south-1"
  }
  zones {
    subnet_id = ibm_is_subnet.zone2.id
    name      = "us-south-2"
  }
  zones {
    subnet_id = ibm_is_subnet.zone3.id
    name      = "us-south-3"
  }

  kms_config {
    instance_id      = ibm_kms_key_rings.ring.instance_id
    crk_id           = ibm_kms_key.key.key_id
    private_endpoint = true
  }
}

# Event Streams for async communication
resource "ibm_resource_instance" "event_streams" {
  name              = "microservices-event-streams"
  service           = "messagehub"
  plan              = "standard"
  location          = "us-south"
  resource_group_id = data.ibm_resource_group.default.id

  parameters = {
    throughput   = "150"
    storage_size = "2048"
  }
}

# Event Streams topics
resource "ibm_event_streams_topic" "order_events" {
  resource_instance_id = ibm_resource_instance.event_streams.id
  name                 = "order-events"
  partitions           = 3
  config = {
    "retention.ms" = "86400000"  # 24 hours
    "segment.bytes" = "536870912"  # 512 MB
  }
}

resource "ibm_event_streams_topic" "payment_events" {
  resource_instance_id = ibm_resource_instance.event_streams.id
  name                 = "payment-events"
  partitions           = 3
  config = {
    "retention.ms" = "86400000"
  }
}

# Databases for each microservice
resource "ibm_database" "user_service_db" {
  name              = "user-service-postgres"
  plan              = "standard"
  location          = "us-south"
  service           = "databases-for-postgresql"
  resource_group_id = data.ibm_resource_group.default.id

  group {
    group_id = "member"
    memory {
      allocation_mb = 4096
    }
    disk {
      allocation_mb = 20480
    }
  }
}

resource "ibm_database" "order_service_db" {
  name              = "order-service-postgres"
  plan              = "standard"
  location          = "us-south"
  service           = "databases-for-postgresql"
  resource_group_id = data.ibm_resource_group.default.id

  group {
    group_id = "member"
    memory {
      allocation_mb = 8192
    }
    disk {
      allocation_mb = 40960
    }
  }
}

# Redis for caching and sessions
resource "ibm_database" "redis_cache" {
  name              = "microservices-redis"
  plan              = "standard"
  location          = "us-south"
  service           = "databases-for-redis"
  resource_group_id = data.ibm_resource_group.default.id

  group {
    group_id = "member"
    memory {
      allocation_mb = 4096
    }
  }
}

# API Gateway using IBM Cloud Internet Services
resource "ibm_cis" "api_gateway" {
  name              = "microservices-api-gateway"
  plan              = "enterprise-usage"
  resource_group_id = data.ibm_resource_group.default.id
}

resource "ibm_cis_domain" "api_domain" {
  domain = "api.example.com"
  cis_id = ibm_cis.api_gateway.id
}

# Load balancer for microservices
resource "ibm_cis_global_load_balancer" "api_glb" {
  cis_id           = ibm_cis.api_gateway.id
  domain_id        = ibm_cis_domain.api_domain.id
  name             = "api.example.com"
  fallback_pool_id = ibm_cis_origin_pool.backup_pool.id
  default_pool_ids = [ibm_cis_origin_pool.primary_pool.id]
  description      = "API Gateway load balancer"
  proxied          = true
  session_affinity = "cookie"
}

resource "ibm_cis_origin_pool" "primary_pool" {
  cis_id = ibm_cis.api_gateway.id
  name   = "primary-microservices-pool"

  origins {
    name    = "istio-gateway"
    address = data.kubernetes_service.istio_gateway.status.0.load_balancer.0.ingress.0.ip
    enabled = true
  }

  monitor              = ibm_cis_healthcheck.api_health.id
  notification_email   = "ops@example.com"
  enabled              = true
  minimum_origins      = 1
}

# Service discovery with Consul
resource "helm_release" "consul" {
  name       = "consul"
  repository = "https://helm.releases.hashicorp.com"
  chart      = "consul"
  namespace  = "consul"
  create_namespace = true

  values = [
    yamlencode({
      global = {
        datacenter = "us-south"
        domain     = "consul"
      }
      server = {
        replicas = 3
        storage  = "10Gi"
      }
      client = {
        enabled = true
      }
      ui = {
        enabled = true
        service = {
          type = "LoadBalancer"
        }
      }
    })
  ]
}
```

---

## Event-Driven Architecture

### Event-Driven Patterns
```yaml
# event-driven-patterns.yaml
patterns:
  event_sourcing:
    description: "Store all changes as events"
    benefits:
      - Complete audit trail
      - Time-travel debugging
      - Event replay capability
    use_cases:
      - Financial transactions
      - Order processing
      - User activity tracking

  cqrs:
    description: "Separate read and write models"
    components:
      - Command side (writes)
      - Query side (reads)
      - Event store
    benefits:
      - Optimized read/write performance
      - Independent scaling
      - Flexible querying

  saga_pattern:
    description: "Distributed transaction management"
    types:
      choreography:
        description: "Events coordinate without central controller"
        pros: "Loose coupling, simple"
        cons: "Complex to understand, debugging difficult"

      orchestration:
        description: "Central coordinator manages saga"
        pros: "Clear flow, easier debugging"
        cons: "Tight coupling, single point of failure"

  event_notification:
    description: "Notify other systems of state changes"
    characteristics:
      - Fire and forget
      - Eventual consistency
      - Loose coupling

  event_carried_state_transfer:
    description: "Events contain full state"
    benefits:
      - Reduced service coupling
      - No need to query source system
    drawbacks:
      - Larger event payloads
      - Potential data duplication
```

### Event Streams Implementation
```python
# event_driven_microservice.py
from confluent_kafka import Producer, Consumer
import json
import logging
from datetime import datetime
from typing import Dict, Any

class EventProducer:
    def __init__(self, bootstrap_servers: str, api_key: str):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': 'token',
            'sasl.password': api_key,
            'client.id': 'event-producer'
        }
        self.producer = Producer(self.config)
        self.logger = logging.getLogger(__name__)

    def publish_event(self, topic: str, event_type: str, data: Dict[str, Any]):
        """Publish event to Event Streams"""
        event = {
            'event_id': self._generate_event_id(),
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data,
            'version': '1.0'
        }

        try:
            self.producer.produce(
                topic,
                key=event['event_id'],
                value=json.dumps(event),
                callback=self._delivery_report
            )
            self.producer.flush()

            self.logger.info(f"Published event {event['event_id']} to {topic}")
            return event['event_id']

        except Exception as e:
            self.logger.error(f"Failed to publish event: {str(e)}")
            raise

    def _delivery_report(self, err, msg):
        """Delivery callback"""
        if err is not None:
            self.logger.error(f"Message delivery failed: {err}")
        else:
            self.logger.info(
                f"Message delivered to {msg.topic()} [{msg.partition()}]"
            )

    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        import uuid
        return str(uuid.uuid4())


class EventConsumer:
    def __init__(self, bootstrap_servers: str, api_key: str, group_id: str):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': 'token',
            'sasl.password': api_key,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False
        }
        self.consumer = Consumer(self.config)
        self.logger = logging.getLogger(__name__)
        self.handlers = {}

    def register_handler(self, event_type: str, handler):
        """Register event handler"""
        self.handlers[event_type] = handler

    def subscribe(self, topics: list):
        """Subscribe to topics"""
        self.consumer.subscribe(topics)
        self.logger.info(f"Subscribed to topics: {topics}")

    def consume(self):
        """Consume events"""
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    self.logger.error(f"Consumer error: {msg.error()}")
                    continue

                # Process event
                event = json.loads(msg.value().decode('utf-8'))
                event_type = event.get('event_type')

                self.logger.info(
                    f"Received event {event['event_id']} of type {event_type}"
                )

                # Call registered handler
                if event_type in self.handlers:
                    try:
                        self.handlers[event_type](event)
                        # Commit offset after successful processing
                        self.consumer.commit()
                    except Exception as e:
                        self.logger.error(
                            f"Error handling event {event['event_id']}: {str(e)}"
                        )
                        # Don't commit offset, will retry
                else:
                    self.logger.warning(
                        f"No handler registered for event type {event_type}"
                    )
                    self.consumer.commit()  # Commit to avoid reprocessing

        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()


# Example: Order Service using events
class OrderService:
    def __init__(self, event_producer: EventProducer):
        self.event_producer = event_producer

    def create_order(self, order_data: Dict[str, Any]):
        """Create order and publish event"""
        # Business logic to create order
        order_id = self._save_order(order_data)

        # Publish OrderCreated event
        self.event_producer.publish_event(
            topic='order-events',
            event_type='OrderCreated',
            data={
                'order_id': order_id,
                'customer_id': order_data['customer_id'],
                'items': order_data['items'],
                'total_amount': order_data['total_amount']
            }
        )

        return order_id

    def _save_order(self, order_data: Dict[str, Any]) -> str:
        # Database save logic
        import uuid
        return str(uuid.uuid4())


# Example: Payment Service consuming events
class PaymentService:
    def __init__(self, event_producer: EventProducer):
        self.event_producer = event_producer

    def handle_order_created(self, event: Dict[str, Any]):
        """Handle OrderCreated event"""
        order_data = event['data']
        order_id = order_data['order_id']

        # Process payment
        payment_result = self._process_payment(order_data)

        if payment_result['success']:
            # Publish PaymentCompleted event
            self.event_producer.publish_event(
                topic='payment-events',
                event_type='PaymentCompleted',
                data={
                    'order_id': order_id,
                    'payment_id': payment_result['payment_id'],
                    'amount': order_data['total_amount']
                }
            )
        else:
            # Publish PaymentFailed event
            self.event_producer.publish_event(
                topic='payment-events',
                event_type='PaymentFailed',
                data={
                    'order_id': order_id,
                    'reason': payment_result['reason']
                }
            )

    def _process_payment(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Payment processing logic
        import uuid
        return {
            'success': True,
            'payment_id': str(uuid.uuid4())
        }


# Usage
if __name__ == "__main__":
    # Configuration
    BOOTSTRAP_SERVERS = 'kafka-0.mh-eventstreams.us-south.containers.appdomain.cloud:9093'
    API_KEY = 'your-event-streams-api-key'

    # Initialize producer
    producer = EventProducer(BOOTSTRAP_SERVERS, API_KEY)

    # Initialize consumer
    consumer = EventConsumer(BOOTSTRAP_SERVERS, API_KEY, group_id='payment-service')

    # Initialize services
    order_service = OrderService(producer)
    payment_service = PaymentService(producer)

    # Register event handlers
    consumer.register_handler('OrderCreated', payment_service.handle_order_created)

    # Subscribe to topics
    consumer.subscribe(['order-events'])

    # Create order (in another thread/process)
    order_service.create_order({
        'customer_id': 'customer-123',
        'items': [{'id': 'item-1', 'quantity': 2}],
        'total_amount': 99.99
    })

    # Consume events
    consumer.consume()
```

---

## Multi-Cloud and Hybrid Cloud

### Multi-Cloud Architecture Strategy
```yaml
# multi-cloud-strategy.yaml
multi_cloud_patterns:
  cloud_agnostic:
    description: "Application runs on any cloud"
    benefits:
      - Vendor independence
      - Negotiation leverage
      - Risk mitigation
    challenges:
      - Lowest common denominator features
      - Additional abstraction layers
      - Complexity

  best_of_breed:
    description: "Use best services from each cloud"
    example:
      compute: "IBM Cloud Kubernetes"
      analytics: "AWS Redshift"
      ai_ml: "Azure Cognitive Services"
    benefits:
      - Optimize each workload
      - Leverage unique features
    challenges:
      - Integration complexity
      - Multiple vendor management

  cloud_bursting:
    description: "Overflow to public cloud during peaks"
    use_case: "Seasonal traffic spikes"
    primary: "On-premises or IBM Cloud"
    burst_to: "AWS, Azure, GCP"

  disaster_recovery:
    description: "Secondary cloud for DR"
    primary: "IBM Cloud us-south"
    dr: "AWS us-east-1 or Azure East US"
    failover: "DNS-based or Global Load Balancer"

hybrid_cloud_patterns:
  edge_to_cloud:
    description: "Edge computing with cloud backend"
    edge: "IBM Edge Application Manager"
    cloud: "IBM Cloud for analytics, ML"
    use_case: "IoT, retail, manufacturing"

  data_residency:
    description: "Keep data on-premises, compute in cloud"
    data: "On-premises database"
    compute: "IBM Cloud Kubernetes"
    connectivity: "IBM Cloud Direct Link"

  gradual_migration:
    description: "Phased cloud migration"
    phases:
      - "Non-critical workloads first"
      - "Data migration"
      - "Critical applications"
      - "Legacy systems last"
```

### Multi-Cloud Connectivity
```bash
# Multi-cloud connectivity setup

# 1. IBM Cloud Transit Gateway for multi-cloud
ibmcloud tg gateway-create \
  multi-cloud-gateway \
  --location us-south \
  --routing global

# 2. Connect IBM Cloud VPC
ibmcloud tg connection-create $TG_ID \
  --name ibm-vpc-connection \
  --network-type vpc \
  --network-id $IBM_VPC_CRN

# 3. Connect to AWS via Direct Link
ibmcloud dl gateway-create \
  --name aws-direct-link \
  --type dedicated \
  --speed 5000 \
  --bgp-asn 64999 \
  --global true \
  --location us-south \
  --customer-name "AWS Connection"

# 4. Set up VPN for Azure connectivity
ibmcloud is vpn-gateway-create \
  azure-vpn-gateway \
  --subnet $SUBNET_ID

ibmcloud is vpn-gateway-connection-create \
  $VPN_GATEWAY_ID \
  azure-connection \
  --peer-address $AZURE_VPN_IP \
  --psk $PRE_SHARED_KEY \
  --local-cidrs 10.240.0.0/16 \
  --peer-cidrs 10.10.0.0/16

# 5. Global Load Balancer for multi-cloud
ibmcloud cis global-load-balancer-create \
  --name multi-cloud-glb \
  --domain-id $DOMAIN_ID \
  --default-pools $IBM_POOL_ID,$AWS_POOL_ID,$AZURE_POOL_ID \
  --fallback-pool $DR_POOL_ID
```

### Terraform Multi-Cloud Infrastructure
```hcl
# multi-cloud.tf

# IBM Cloud VPC
resource "ibm_is_vpc" "ibm_vpc" {
  name                      = "ibm-cloud-vpc"
  resource_group            = data.ibm_resource_group.default.id
  address_prefix_management = "manual"
}

# AWS VPC (using AWS provider)
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "aws_vpc" {
  cidr_block           = "10.10.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "aws-cloud-vpc"
  }
}

# Azure VNet (using Azure provider)
provider "azurerm" {
  features {}
}

resource "azurerm_virtual_network" "azure_vnet" {
  name                = "azure-cloud-vnet"
  address_space       = ["10.20.0.0/16"]
  location            = "East US"
  resource_group_name = azurerm_resource_group.rg.name
}

# IBM Cloud Transit Gateway for multi-cloud routing
resource "ibm_tg_gateway" "multi_cloud_gateway" {
  name     = "multi-cloud-transit-gateway"
  location = "us-south"
  global   = true
}

# Connect IBM VPC
resource "ibm_tg_connection" "ibm_vpc_connection" {
  gateway      = ibm_tg_gateway.multi_cloud_gateway.id
  network_type = "vpc"
  name         = "ibm-vpc-connection"
  network_id   = ibm_is_vpc.ibm_vpc.crn
}

# Direct Link to AWS
resource "ibm_dl_gateway" "aws_connection" {
  name            = "aws-direct-link"
  type            = "dedicated"
  speed_mbps      = 5000
  global          = true
  bgp_asn         = 64999
  location_name   = "us-south"
  customer_name   = "AWS Connection"
  carrier_name    = "AWS Direct Connect"
}

# VPN to Azure
resource "ibm_is_vpn_gateway" "azure_vpn" {
  name   = "azure-vpn-gateway"
  subnet = ibm_is_subnet.subnet1.id
}

resource "ibm_is_vpn_gateway_connection" "azure_connection" {
  name          = "azure-vpn-connection"
  vpn_gateway   = ibm_is_vpn_gateway.azure_vpn.id
  peer_address  = azurerm_public_ip.vpn_gateway_ip.ip_address
  preshared_key = random_password.vpn_psk.result
  local_cidrs   = ["10.240.0.0/16"]
  peer_cidrs    = ["10.20.0.0/16"]
}

# Multi-cloud Global Load Balancer
resource "ibm_cis_global_load_balancer" "multi_cloud_glb" {
  cis_id           = ibm_cis.instance.id
  domain_id        = ibm_cis_domain.domain.id
  name             = "app.example.com"
  fallback_pool_id = ibm_cis_origin_pool.dr_pool.id
  default_pool_ids = [
    ibm_cis_origin_pool.ibm_pool.id,
    ibm_cis_origin_pool.aws_pool.id,
    ibm_cis_origin_pool.azure_pool.id
  ]
  description      = "Multi-cloud application load balancer"
  proxied          = true
  session_affinity = "ip_cookie"

  # Intelligent routing
  steering_policy = "dynamic_latency"

  # Regional steering
  region_pools {
    region   = "WNAM"  # Western North America
    pool_ids = [ibm_cis_origin_pool.ibm_pool.id]
  }

  region_pools {
    region   = "ENAM"  # Eastern North America
    pool_ids = [ibm_cis_origin_pool.aws_pool.id]
  }

  region_pools {
    region   = "WEU"   # Western Europe
    pool_ids = [ibm_cis_origin_pool.azure_pool.id]
  }
}

# Origin pools for each cloud
resource "ibm_cis_origin_pool" "ibm_pool" {
  cis_id = ibm_cis.instance.id
  name   = "ibm-cloud-pool"

  origins {
    name    = "ibm-origin-1"
    address = ibm_is_lb.app_lb.hostname
    enabled = true
    weight  = 1
  }

  monitor              = ibm_cis_healthcheck.app_health.id
  enabled              = true
  minimum_origins      = 1
  notification_email   = "ops@example.com"
}

resource "ibm_cis_origin_pool" "aws_pool" {
  cis_id = ibm_cis.instance.id
  name   = "aws-cloud-pool"

  origins {
    name    = "aws-origin-1"
    address = aws_lb.app_lb.dns_name
    enabled = true
    weight  = 1
  }

  monitor              = ibm_cis_healthcheck.app_health.id
  enabled              = true
  minimum_origins      = 1
  notification_email   = "ops@example.com"
}

resource "ibm_cis_origin_pool" "azure_pool" {
  cis_id = ibm_cis.instance.id
  name   = "azure-cloud-pool"

  origins {
    name    = "azure-origin-1"
    address = azurerm_lb.app_lb.private_ip_address
    enabled = true
    weight  = 1
  }

  monitor              = ibm_cis_healthcheck.app_health.id
  enabled              = true
  minimum_origins      = 1
  notification_email   = "ops@example.com"
}
```

---

## High Availability Architecture

### HA Design Principles
```yaml
# high-availability-architecture.yaml
availability_tiers:
  tier_1_mission_critical:
    availability_target: "99.99%"
    max_downtime_per_year: "52.56 minutes"
    architecture:
      - Multi-zone deployment (minimum 3 zones)
      - Active-active configuration
      - Automated failover
      - Zero-downtime deployments
      - Real-time data replication

  tier_2_business_critical:
    availability_target: "99.9%"
    max_downtime_per_year: "8.76 hours"
    architecture:
      - Multi-zone deployment (minimum 2 zones)
      - Active-passive configuration
      - Automated failover
      - Blue-green deployments
      - Regular backup and restore testing

  tier_3_standard:
    availability_target: "99.5%"
    max_downtime_per_year: "43.8 hours"
    architecture:
      - Single zone with backup
      - Manual failover procedures
      - Standard deployments
      - Daily backups

ha_patterns:
  load_balancing:
    types:
      - Layer 4 (TCP/UDP)
      - Layer 7 (HTTP/HTTPS)
      - Global (DNS-based)
    algorithms:
      - Round robin
      - Least connections
      - IP hash
      - Weighted
      - Geo-proximity

  health_checks:
    liveness_probe:
      description: "Is the application running?"
      failure_action: "Restart container"
      example: "HTTP GET /healthz"

    readiness_probe:
      description: "Can the application handle traffic?"
      failure_action: "Remove from load balancer"
      example: "HTTP GET /ready"

    startup_probe:
      description: "Has the application started?"
      use_case: "Slow-starting applications"
      example: "HTTP GET /startup"

  redundancy:
    n_plus_one:
      description: "N active + 1 standby"
      example: "3 active servers + 1 standby"

    n_plus_m:
      description: "N active + M standby"
      example: "10 active servers + 2 standby"

    two_n:
      description: "2N fully redundant systems"
      example: "6 servers (3+3) active-active"
```

### HA Kubernetes Deployment
```yaml
# high-availability-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-ha
  labels:
    app: web-app
    tier: frontend
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 0  # Zero downtime

  selector:
    matchLabels:
      app: web-app

  template:
    metadata:
      labels:
        app: web-app
        version: v1
    spec:
      # Anti-affinity to spread across zones
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - web-app
            topologyKey: topology.kubernetes.io/zone

      # Pod disruption budget
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: web-app

      containers:
      - name: web-app
        image: us.icr.io/namespace/web-app:v1
        ports:
        - containerPort: 8080
          name: http
          protocol: TCP

        # Resource requests and limits
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Liveness probe
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # Readiness probe
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2

        # Startup probe for slow-starting apps
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 30  # 5 minutes to start

        # Graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]

---
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800

---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-app-pdb
spec:
  minAvailable: 4  # At least 4 pods must be available
  selector:
    matchLabels:
      app: web-app

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app-ha
  minReplicas: 6
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 75
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 50
        periodSeconds: 30
```

---

## Exam Tips

1. **Architecture Principles**: Know Well-Architected Framework pillars
2. **Design Patterns**: Understand microservices, event-driven, serverless
3. **Multi-Cloud**: Master connectivity options (Transit Gateway, Direct Link, VPN)
4. **High Availability**: Know zone design, load balancing, health checks
5. **Cloud-Native**: Understand 12-factor app, containers, Kubernetes
6. **Resilience**: Circuit breakers, retries, bulkheads, graceful degradation
7. **Service Mesh**: Istio basics, traffic management, security

### Common Exam Scenarios

**Scenario 1**: Design 99.99% available e-commerce platform
- Multi-zone Kubernetes cluster (3+ zones)
- Active-active database replication
- Global Load Balancer with health checks
- Auto-scaling based on traffic
- Zero-downtime deployments

**Scenario 2**: Migrate monolith to microservices
- Identify service boundaries
- Implement API Gateway
- Set up service mesh (Istio)
- Deploy Event Streams for async communication
- Database per service pattern

**Scenario 3**: Multi-cloud architecture for vendor independence
- Deploy on IBM Cloud and AWS
- Transit Gateway for connectivity
- Global Load Balancer for traffic routing
- Unified monitoring across clouds
- Terraform for IaC

### Key Terminology

- **RPO/RTO**: Recovery objectives for DR
- **SLA/SLO/SLI**: Service level agreements and indicators
- **Circuit Breaker**: Prevent cascade failures
- **Service Mesh**: Infrastructure layer for service-to-service communication
- **API Gateway**: Single entry point for microservices
- **Event Sourcing**: Store all changes as events
- **CQRS**: Separate read and write models

### Hands-On Practice

1. Deploy multi-zone Kubernetes cluster
2. Implement microservices with Istio
3. Set up Event Streams for event-driven architecture
4. Configure multi-cloud connectivity
5. Build HA application with auto-scaling
6. Design and implement DR solution
7. Create architectural decision records (ADRs)

## Key terms

- **Twelve-factor app** - a set of twelve principles for building portable, scalable software-as-a-service applications.
- **Architecture decision record (ADR)** - a short document that records an architectural decision, its context and its consequences.
- **Microservices** - an architecture that builds an application from small, independently deployable services.
- **Event-driven architecture** - a design in which components communicate by producing and reacting to events.
- **Circuit breaker pattern** - a pattern that stops calls to a failing service for a while so failures do not cascade.
- **Bulkhead pattern** - a pattern that isolates resources for different parts of a system so a failure in one does not exhaust the others.
- **Multi-cloud** - using cloud services from more than one provider.
- **Well-Architected Framework** - a set of design principles and review questions for judging the quality of a cloud architecture.
