# Monitoring and Deployment - GCP Professional Cloud Developer

## Overview

Comprehensive guide to application monitoring, observability, logging, debugging, CI/CD pipelines, deployment strategies, and traffic management for cloud-native applications on Google Cloud Platform.

## Application Monitoring

### Cloud Monitoring API Integration

**Complete Monitoring Setup**:
```python
from google.cloud import monitoring_v3
import time
from typing import Dict, Any

class CloudMonitoring:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{project_id}"

    def write_custom_metric(self, metric_type: str, value: float,
                           labels: Dict[str, str] = None):
        """Write custom metric to Cloud Monitoring"""
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{metric_type}"
        series.resource.type = "global"

        # Add labels
        if labels:
            for key, val in labels.items():
                series.metric.labels[key] = val

        # Add point
        point = series.points.add()
        point.value.double_value = value
        now = time.time()
        point.interval.end_time.seconds = int(now)
        point.interval.end_time.nanos = int((now - int(now)) * 10**9)

        self.client.create_time_series(
            name=self.project_name,
            time_series=[series]
        )

    def write_business_metric(self, metric_name: str, value: float,
                             user_id: str = None, region: str = None):
        """Write business KPI metric"""
        labels = {}
        if user_id:
            labels['user_id'] = user_id
        if region:
            labels['region'] = region

        self.write_custom_metric(
            metric_type=f"business/{metric_name}",
            value=value,
            labels=labels
        )

    def record_request_latency(self, endpoint: str, latency_ms: float,
                               status_code: int):
        """Record API endpoint latency"""
        self.write_custom_metric(
            metric_type="api/request_latency",
            value=latency_ms,
            labels={
                'endpoint': endpoint,
                'status_code': str(status_code)
            }
        )

    def record_queue_depth(self, queue_name: str, depth: int):
        """Record queue depth for monitoring"""
        self.write_custom_metric(
            metric_type="queue/depth",
            value=float(depth),
            labels={'queue_name': queue_name}
        )

# Usage in application
monitoring = CloudMonitoring(project_id="my-project")

# Record business metrics
monitoring.write_business_metric(
    metric_name="order_total",
    value=299.99,
    user_id="user123",
    region="us-central1"
)

# Record API latency
monitoring.record_request_latency(
    endpoint="/api/products",
    latency_ms=125.5,
    status_code=200
)
```

**Node.js Monitoring Integration**:
```javascript
const monitoring = require('@google-cloud/monitoring');

class CloudMonitoring {
  constructor(projectId) {
    this.projectId = projectId;
    this.client = new monitoring.MetricServiceClient();
    this.projectPath = this.client.projectPath(projectId);
  }

  async writeCustomMetric(metricType, value, labels = {}) {
    const dataPoint = {
      interval: {
        endTime: {
          seconds: Date.now() / 1000,
        },
      },
      value: {
        doubleValue: value,
      },
    };

    const timeSeries = {
      metric: {
        type: `custom.googleapis.com/${metricType}`,
        labels: labels,
      },
      resource: {
        type: 'global',
        labels: {
          project_id: this.projectId,
        },
      },
      points: [dataPoint],
    };

    const request = {
      name: this.projectPath,
      timeSeries: [timeSeries],
    };

    await this.client.createTimeSeries(request);
  }

  async recordUserAction(action, userId, duration) {
    await this.writeCustomMetric('user/action_duration', duration, {
      action: action,
      user_id: userId,
    });
  }

  async recordCacheHitRate(cacheName, hitRate) {
    await this.writeCustomMetric('cache/hit_rate', hitRate, {
      cache_name: cacheName,
    });
  }
}

// Middleware for automatic request monitoring
function monitoringMiddleware(monitoring) {
  return async (req, res, next) => {
    const startTime = Date.now();

    res.on('finish', async () => {
      const duration = Date.now() - startTime;
      await monitoring.writeCustomMetric('http/request_duration', duration, {
        method: req.method,
        path: req.path,
        status: res.statusCode.toString(),
      });
    });

    next();
  };
}

// Express app integration
const express = require('express');
const app = express();
const monitor = new CloudMonitoring('my-project');

app.use(monitoringMiddleware(monitor));
```

### Custom Metrics Design Patterns

**Resource Monitoring Pattern**:
```python
from google.cloud import monitoring_v3
import psutil
import threading
import time

class ResourceMonitor:
    def __init__(self, project_id: str, interval: int = 60):
        self.project_id = project_id
        self.client = monitoring_v3.MetricServiceClient()
        self.interval = interval
        self.running = False

    def start_monitoring(self):
        """Start background resource monitoring"""
        self.running = True
        thread = threading.Thread(target=self._monitor_loop)
        thread.daemon = True
        thread.start()

    def _monitor_loop(self):
        while self.running:
            self._record_resources()
            time.sleep(self.interval)

    def _record_resources(self):
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self._write_metric("system/cpu_usage", cpu_percent)

        # Memory usage
        memory = psutil.virtual_memory()
        self._write_metric("system/memory_usage", memory.percent)

        # Disk usage
        disk = psutil.disk_usage('/')
        self._write_metric("system/disk_usage", disk.percent)

    def _write_metric(self, metric_type: str, value: float):
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{metric_type}"
        series.resource.type = "gce_instance"

        point = series.points.add()
        point.value.double_value = value
        point.interval.end_time.seconds = int(time.time())

        try:
            self.client.create_time_series(
                name=f"projects/{self.project_id}",
                time_series=[series]
            )
        except Exception as e:
            print(f"Failed to write metric: {e}")

# Start monitoring
monitor = ResourceMonitor(project_id="my-project", interval=60)
monitor.start_monitoring()
```

### Distributed Tracing with Cloud Trace

**Complete Trace Integration**:
```python
from google.cloud import trace_v1
from google.cloud.trace_v1 import types
import time
import uuid
from contextlib import contextmanager

class CloudTracer:
    def __init__(self, project_id: str, service_name: str):
        self.project_id = project_id
        self.service_name = service_name
        self.client = trace_v1.TraceServiceClient()
        self.project_name = f"projects/{project_id}"

    @contextmanager
    def span(self, span_name: str, parent_span_id: str = None):
        """Context manager for creating trace spans"""
        trace_id = str(uuid.uuid4().hex)
        span_id = str(uuid.uuid4().int)[:16]

        start_time = time.time()

        try:
            yield {
                'trace_id': trace_id,
                'span_id': span_id
            }
        finally:
            end_time = time.time()
            self._write_span(
                trace_id=trace_id,
                span_id=span_id,
                span_name=span_name,
                start_time=start_time,
                end_time=end_time,
                parent_span_id=parent_span_id
            )

    def _write_span(self, trace_id: str, span_id: str, span_name: str,
                    start_time: float, end_time: float,
                    parent_span_id: str = None):
        """Write span to Cloud Trace"""
        span = types.TraceSpan()
        span.span_id = int(span_id)
        span.name = span_name

        # Set timestamps
        span.start_time.seconds = int(start_time)
        span.start_time.nanos = int((start_time - int(start_time)) * 10**9)
        span.end_time.seconds = int(end_time)
        span.end_time.nanos = int((end_time - int(end_time)) * 10**9)

        if parent_span_id:
            span.parent_span_id = int(parent_span_id)

        trace = types.Trace()
        trace.project_id = self.project_id
        trace.trace_id = trace_id
        trace.spans.append(span)

        try:
            self.client.patch_traces(
                project_id=self.project_id,
                traces=types.Traces(traces=[trace])
            )
        except Exception as e:
            print(f"Failed to write trace: {e}")

# Usage in application
tracer = CloudTracer(project_id="my-project", service_name="api-service")

def process_order(order_id: str):
    with tracer.span("process_order") as parent_span:
        # Validate order
        with tracer.span("validate_order", parent_span['span_id']):
            validate_order_details(order_id)

        # Process payment
        with tracer.span("process_payment", parent_span['span_id']):
            process_payment(order_id)

        # Ship order
        with tracer.span("ship_order", parent_span['span_id']):
            ship_order(order_id)
```

**OpenTelemetry Integration** (Recommended):
```python
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Set up Cloud Trace exporter
trace.set_tracer_provider(TracerProvider())
cloud_trace_exporter = CloudTraceSpanExporter()
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(cloud_trace_exporter)
)

# Auto-instrument libraries
RequestsInstrumentor().instrument()

# Flask app instrumentation
from flask import Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Manual instrumentation
tracer = trace.get_tracer(__name__)

@app.route('/api/products/<product_id>')
def get_product(product_id):
    with tracer.start_as_current_span("get_product") as span:
        span.set_attribute("product_id", product_id)

        # Database call
        with tracer.start_as_current_span("db_query"):
            product = db.get_product(product_id)

        # Cache call
        with tracer.start_as_current_span("cache_check"):
            cached = cache.get(f"product:{product_id}")

        span.set_attribute("cache_hit", cached is not None)
        return product
```

### Error Reporting Integration

**Comprehensive Error Handling**:
```python
from google.cloud import error_reporting
import logging
import traceback
import sys

class ErrorReporter:
    def __init__(self, project_id: str, service_name: str):
        self.client = error_reporting.Client(project=project_id)
        self.service_name = service_name

    def report_error(self, error: Exception, user_id: str = None,
                    http_context: dict = None):
        """Report error to Cloud Error Reporting"""
        try:
            self.client.report_exception(
                http_context=http_context,
                user=user_id
            )
        except Exception as e:
            logging.error(f"Failed to report error: {e}")

    def report_with_context(self, error: Exception, **context):
        """Report error with custom context"""
        error_message = f"{type(error).__name__}: {str(error)}\n"
        error_message += f"Context: {context}\n"
        error_message += traceback.format_exc()

        try:
            self.client.report(error_message)
        except Exception as e:
            logging.error(f"Failed to report error: {e}")

# Flask integration
from flask import Flask, request, g
import functools

app = Flask(__name__)
error_reporter = ErrorReporter(
    project_id="my-project",
    service_name="api-service"
)

def report_errors(f):
    """Decorator to automatically report errors"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            http_context = {
                'method': request.method,
                'url': request.url,
                'user_agent': request.headers.get('User-Agent'),
                'remote_ip': request.remote_addr
            }

            error_reporter.report_error(
                error=e,
                user_id=g.get('user_id'),
                http_context=http_context
            )
            raise

    return wrapper

@app.route('/api/orders', methods=['POST'])
@report_errors
def create_order():
    # Application logic
    order = process_order_request(request.json)
    return {'order_id': order.id}
```

**Node.js Error Reporting**:
```javascript
const {ErrorReporting} = require('@google-cloud/error-reporting');

const errors = new ErrorReporting({
  projectId: 'my-project',
  reportMode: 'production',
  serviceContext: {
    service: 'api-service',
    version: '1.0.0',
  },
});

// Express middleware
function errorReportingMiddleware(err, req, res, next) {
  errors.report(err, {
    user: req.user?.id,
    httpRequest: {
      method: req.method,
      url: req.url,
      userAgent: req.headers['user-agent'],
      remoteIp: req.ip,
      statusCode: res.statusCode,
    },
  });

  next(err);
}

app.use(errorReportingMiddleware);

// Manual error reporting
async function processOrder(orderId) {
  try {
    await validateOrder(orderId);
    await chargePayment(orderId);
  } catch (err) {
    errors.report(err, {
      user: orderId,
      context: {
        step: 'payment_processing',
        order_id: orderId,
      },
    });
    throw err;
  }
}
```

## Logging Best Practices

### Structured Logging

**Python Structured Logging**:
```python
import logging
import json
import uuid
from google.cloud import logging as cloud_logging
from datetime import datetime

class StructuredLogger:
    def __init__(self, project_id: str, service_name: str):
        self.client = cloud_logging.Client(project=project_id)
        self.client.setup_logging()
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)

    def log(self, level: str, message: str, **context):
        """Log structured message with context"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'severity': level.upper(),
            'service': self.service_name,
            'message': message,
            **context
        }

        if level == 'info':
            self.logger.info(json.dumps(log_entry))
        elif level == 'warning':
            self.logger.warning(json.dumps(log_entry))
        elif level == 'error':
            self.logger.error(json.dumps(log_entry))
        elif level == 'debug':
            self.logger.debug(json.dumps(log_entry))

    def log_request(self, method: str, path: str, status_code: int,
                   latency_ms: float, user_id: str = None):
        """Log HTTP request with standard fields"""
        self.log('info', 'HTTP request processed',
                method=method,
                path=path,
                status_code=status_code,
                latency_ms=latency_ms,
                user_id=user_id,
                log_type='http_request')

    def log_business_event(self, event_type: str, **details):
        """Log business event"""
        self.log('info', f'Business event: {event_type}',
                event_type=event_type,
                log_type='business_event',
                **details)

# Usage
logger = StructuredLogger(
    project_id="my-project",
    service_name="api-service"
)

logger.log_request(
    method="POST",
    path="/api/orders",
    status_code=201,
    latency_ms=145.2,
    user_id="user123"
)

logger.log_business_event(
    event_type="order_created",
    order_id="order-456",
    total_amount=299.99,
    currency="USD"
)
```

### Correlation IDs and Request Tracking

**Request Correlation Pattern**:
```python
import uuid
from flask import Flask, request, g
import logging

app = Flask(__name__)

@app.before_request
def before_request():
    """Generate or extract correlation ID"""
    correlation_id = request.headers.get('X-Correlation-ID')
    if not correlation_id:
        correlation_id = str(uuid.uuid4())

    g.correlation_id = correlation_id
    g.request_start_time = time.time()

@app.after_request
def after_request(response):
    """Add correlation ID to response headers"""
    response.headers['X-Correlation-ID'] = g.correlation_id
    return response

class CorrelationFilter(logging.Filter):
    """Add correlation ID to all logs"""
    def filter(self, record):
        record.correlation_id = getattr(g, 'correlation_id', 'no-correlation-id')
        record.user_id = getattr(g, 'user_id', 'anonymous')
        return True

# Configure logging
logger = logging.getLogger(__name__)
logger.addFilter(CorrelationFilter())

# Custom formatter
formatter = logging.Formatter(
    '{"timestamp":"%(asctime)s","severity":"%(levelname)s",'
    '"correlation_id":"%(correlation_id)s","user_id":"%(user_id)s",'
    '"message":"%(message)s"}'
)

@app.route('/api/orders', methods=['POST'])
def create_order():
    logger.info(f"Processing order creation",
               extra={'order_data': request.json})

    try:
        order = process_order(request.json)
        logger.info(f"Order created successfully",
                   extra={'order_id': order.id})
        return {'order_id': order.id}, 201
    except Exception as e:
        logger.error(f"Order creation failed: {e}",
                    extra={'error_type': type(e).__name__})
        raise
```

**Node.js Correlation Tracking**:
```javascript
const {Logging} = require('@google-cloud/logging');
const express = require('express');
const {v4: uuidv4} = require('uuid');

const logging = new Logging({projectId: 'my-project'});
const log = logging.log('api-service');

// Middleware for correlation ID
function correlationMiddleware(req, res, next) {
  req.correlationId = req.headers['x-correlation-id'] || uuidv4();
  res.setHeader('X-Correlation-ID', req.correlationId);
  next();
}

// Structured logging helper
function logStructured(severity, message, metadata = {}) {
  const entry = log.entry({
    resource: {type: 'global'},
    severity: severity.toUpperCase(),
  }, {
    message,
    correlation_id: req.correlationId,
    user_id: req.user?.id,
    timestamp: new Date().toISOString(),
    ...metadata,
  });

  log.write(entry);
}

app.use(correlationMiddleware);

app.post('/api/orders', async (req, res) => {
  logStructured('info', 'Processing order', {
    order_data: req.body,
  });

  try {
    const order = await processOrder(req.body);
    logStructured('info', 'Order created', {
      order_id: order.id,
    });
    res.status(201).json({order_id: order.id});
  } catch (err) {
    logStructured('error', 'Order creation failed', {
      error: err.message,
      stack: err.stack,
    });
    res.status(500).json({error: 'Internal server error'});
  }
});
```

### Log-Based Metrics

**Creating Log-Based Metrics**:
```bash
# Create counter metric from logs
gcloud logging metrics create order_errors \
  --description="Count of order processing errors" \
  --log-filter='resource.type="cloud_run_revision"
    severity="ERROR"
    jsonPayload.event_type="order_processing"'

# Create distribution metric for latency
gcloud logging metrics create api_latency \
  --description="API endpoint latency distribution" \
  --log-filter='resource.type="cloud_run_revision"
    jsonPayload.log_type="http_request"' \
  --value-extractor='EXTRACT(jsonPayload.latency_ms)'

# Create metric with labels
gcloud logging metrics create http_requests_by_status \
  --description="HTTP requests by status code" \
  --log-filter='resource.type="cloud_run_revision"
    jsonPayload.log_type="http_request"' \
  --value-extractor='EXTRACT(jsonPayload.status_code)'
```

**Python Log-Based Metrics Creation**:
```python
from google.cloud import logging_v2

def create_log_based_metrics(project_id: str):
    client = logging_v2.MetricsServiceV2Client()
    project_name = f"projects/{project_id}"

    # Error count metric
    metric = {
        'name': f'{project_name}/metrics/application_errors',
        'description': 'Count of application errors',
        'filter': 'severity>=ERROR',
        'metric_descriptor': {
            'metric_kind': 'DELTA',
            'value_type': 'INT64',
        }
    }

    client.create_log_metric(parent=project_name, metric=metric)

    # Latency distribution metric
    latency_metric = {
        'name': f'{project_name}/metrics/request_latency',
        'description': 'Request latency distribution',
        'filter': 'jsonPayload.latency_ms>0',
        'value_extractor': 'EXTRACT(jsonPayload.latency_ms)',
        'metric_descriptor': {
            'metric_kind': 'DELTA',
            'value_type': 'DISTRIBUTION',
        }
    }

    client.create_log_metric(parent=project_name, metric=latency_metric)
```

## Debugging

### Cloud Debugger

**Debugger Integration**:
```python
import googleclouddebugger

# Enable Cloud Debugger
googleclouddebugger.enable(
    project_id='my-project',
    project_number='123456789',
    service='api-service',
    version='v1.0.0'
)

# Application code - debugger allows setting breakpoints
# and logpoints without code changes
def process_payment(order_id: str, amount: float):
    # Can set snapshot here to inspect variables
    payment_method = get_payment_method(order_id)

    # Can set logpoint here to log without redeploying
    charge_result = charge_payment(payment_method, amount)

    return charge_result
```

**Using Debugger Snapshots** (via gcloud):
```bash
# List debug targets
gcloud debug targets list

# Create snapshot (breakpoint)
gcloud debug snapshots create \
  --target=api-service \
  --location=main.py:42 \
  --condition="order_total > 1000"

# Create logpoint
gcloud debug logpoints create \
  --target=api-service \
  --location=payment.py:25 \
  --log-format="Processing payment for order {order_id} amount {amount}"

# List snapshots
gcloud debug snapshots list --target=api-service

# View snapshot details
gcloud debug snapshots describe SNAPSHOT_ID
```

### Cloud Profiler Integration

**Complete Profiler Setup**:
```python
import googlecloudprofiler
import logging

def setup_profiler(project_id: str, service_name: str, version: str):
    """Initialize Cloud Profiler"""
    try:
        googlecloudprofiler.start(
            service=service_name,
            service_version=version,
            project_id=project_id,
            verbose=3,  # Set to 3 for debugging
            # Profile CPU and heap
            disable_cpu_profiling=False,
            disable_heap_profiling=False,
            # Sampling configuration
            period_ms=1000,  # Sample every second
        )
        logging.info("Cloud Profiler started successfully")
    except Exception as e:
        logging.error(f"Failed to start Cloud Profiler: {e}")

# Start profiler at application startup
setup_profiler(
    project_id="my-project",
    service_name="api-service",
    version="v1.0.0"
)

# CPU-intensive function that will show in profiler
def calculate_recommendations(user_id: str):
    # This function's performance will be visible in Cloud Profiler
    user_data = fetch_user_data(user_id)
    recommendations = []

    for item in user_data.history:
        similarity_scores = calculate_similarity(item)
        recommendations.extend(similarity_scores)

    return sorted(recommendations, reverse=True)[:10]
```

**Node.js Profiler Setup**:
```javascript
const profiler = require('@google-cloud/profiler');

// Start profiler
profiler.start({
  projectId: 'my-project',
  serviceContext: {
    service: 'api-service',
    version: '1.0.0',
  },
  // Profile time and heap
  disableTime: false,
  disableHeap: false,
  // Sampling configuration
  timeIntervalMicros: 1000,
  heapIntervalBytes: 512 * 1024,
}).catch((err) => {
  console.error(`Failed to start profiler: ${err}`);
});
```

## CI/CD Pipelines

### Cloud Build Configuration

**Basic cloudbuild.yaml**:
```yaml
# cloudbuild.yaml - Simple build and deploy
steps:
  # Build Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '-t'
      - 'gcr.io/$PROJECT_ID/myapp:latest'
      - '.'

  # Push image to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'

  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'

images:
  - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
  - 'gcr.io/$PROJECT_ID/myapp:latest'

timeout: '1200s'
```

**Advanced CI/CD Pipeline with Testing**:
```yaml
# cloudbuild.yaml - Complete CI/CD pipeline
steps:
  # Install dependencies
  - name: 'python:3.9'
    entrypoint: 'pip'
    args:
      - 'install'
      - '-r'
      - 'requirements.txt'
      - '--user'

  # Run unit tests
  - name: 'python:3.9'
    entrypoint: 'python'
    args:
      - '-m'
      - 'pytest'
      - 'tests/unit'
      - '--cov=app'
      - '--cov-report=xml'
      - '--junitxml=test-results.xml'
    env:
      - 'PYTHONPATH=/workspace'

  # Run linting
  - name: 'python:3.9'
    entrypoint: 'python'
    args:
      - '-m'
      - 'pylint'
      - 'app/'
      - '--output-format=json'
      - '--reports=y'

  # Security scan
  - name: 'aquasec/trivy'
    args:
      - 'fs'
      - '--security-checks'
      - 'vuln,config'
      - '--severity'
      - 'HIGH,CRITICAL'
      - '.'

  # Build Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '-t'
      - 'gcr.io/$PROJECT_ID/myapp:$SHORT_SHA'
      - '-t'
      - 'gcr.io/$PROJECT_ID/myapp:latest'
      - '--build-arg'
      - 'VERSION=$TAG_NAME'
      - '--cache-from'
      - 'gcr.io/$PROJECT_ID/myapp:latest'
      - '.'

  # Scan container image
  - name: 'aquasec/trivy'
    args:
      - 'image'
      - '--severity'
      - 'HIGH,CRITICAL'
      - '--exit-code'
      - '1'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'

  # Push image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '--all-tags'
      - 'gcr.io/$PROJECT_ID/myapp'

  # Deploy to staging
  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'deploy-staging'
    args:
      - 'run'
      - 'deploy'
      - 'myapp-staging'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--tag'
      - 'staging-$SHORT_SHA'
      - '--no-traffic'

  # Run integration tests against staging
  - name: 'python:3.9'
    entrypoint: 'python'
    args:
      - '-m'
      - 'pytest'
      - 'tests/integration'
      - '--base-url=https://staging-$SHORT_SHA---myapp-staging-uc.a.run.app'
    env:
      - 'PYTHONPATH=/workspace'

  # Deploy to production with traffic split
  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'deploy-production'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--tag'
      - 'prod-$SHORT_SHA'
      - '--no-traffic'

  # Gradual rollout - 10% traffic
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'services'
      - 'update-traffic'
      - 'myapp'
      - '--to-revisions'
      - 'prod-$SHORT_SHA=10'
      - '--region'
      - 'us-central1'

substitutions:
  _DEPLOY_REGION: 'us-central1'

options:
  machineType: 'N1_HIGHCPU_8'
  logging: 'CLOUD_LOGGING_ONLY'

timeout: '1800s'
```

**Multi-Stage Build with Artifacts**:
```yaml
# cloudbuild.yaml - Multi-stage with artifact management
steps:
  # Stage 1: Build and test
  - name: 'node:16'
    id: 'install'
    entrypoint: 'npm'
    args: ['ci']

  - name: 'node:16'
    id: 'test'
    entrypoint: 'npm'
    args: ['test']
    waitFor: ['install']

  - name: 'node:16'
    id: 'build'
    entrypoint: 'npm'
    args: ['run', 'build']
    waitFor: ['install']

  # Stage 2: Create production image
  - name: 'gcr.io/cloud-builders/docker'
    id: 'docker-build'
    args:
      - 'build'
      - '-f'
      - 'Dockerfile.prod'
      - '-t'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '.'
    waitFor: ['build']

  # Stage 3: Upload artifacts
  - name: 'gcr.io/cloud-builders/gsutil'
    args:
      - 'cp'
      - '-r'
      - 'dist/*'
      - 'gs://$PROJECT_ID-artifacts/builds/$BUILD_ID/'
    waitFor: ['build']

  # Stage 4: Push image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA']
    waitFor: ['docker-build']

  # Stage 5: Deploy
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
    waitFor: ['push']

artifacts:
  objects:
    location: 'gs://$PROJECT_ID-artifacts/builds/$BUILD_ID/'
    paths:
      - 'test-results/**'
      - 'coverage/**'
      - 'dist/**'

options:
  machineType: 'E2_HIGHCPU_8'
```

### Build Triggers

**Creating Build Triggers**:
```bash
# Trigger on push to main branch
gcloud builds triggers create github \
  --repo-name=myapp \
  --repo-owner=myorg \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --description="Deploy to production on main push"

# Trigger on pull request
gcloud builds triggers create github \
  --repo-name=myapp \
  --repo-owner=myorg \
  --pull-request-pattern="^.*$" \
  --build-config=cloudbuild-pr.yaml \
  --description="Run tests on pull request" \
  --comment-control=COMMENTS_ENABLED

# Trigger on tag
gcloud builds triggers create github \
  --repo-name=myapp \
  --repo-owner=myorg \
  --tag-pattern="v.*" \
  --build-config=cloudbuild-release.yaml \
  --description="Release on version tag"

# Trigger with substitutions
gcloud builds triggers create github \
  --repo-name=myapp \
  --repo-owner=myorg \
  --branch-pattern="^develop$" \
  --build-config=cloudbuild.yaml \
  --substitutions=_ENVIRONMENT=staging,_REGION=us-central1
```

**cloudbuild.yaml with Substitutions**:
```yaml
# cloudbuild.yaml - Using substitutions
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/${_SERVICE_NAME}:$COMMIT_SHA'
      - '--build-arg'
      - 'ENVIRONMENT=${_ENVIRONMENT}'
      - '.'

  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - '${_SERVICE_NAME}-${_ENVIRONMENT}'
      - '--image'
      - 'gcr.io/$PROJECT_ID/${_SERVICE_NAME}:$COMMIT_SHA'
      - '--region'
      - '${_REGION}'
      - '--set-env-vars'
      - 'ENVIRONMENT=${_ENVIRONMENT},VERSION=$SHORT_SHA'

substitutions:
  _SERVICE_NAME: 'myapp'
  _ENVIRONMENT: 'production'
  _REGION: 'us-central1'

# Default substitutions can be overridden by trigger
```

## Deployment Strategies

### Blue-Green Deployment

**App Engine Blue-Green**:
```bash
# Deploy new version without traffic
gcloud app deploy --no-promote --version=v2

# Test new version
curl https://v2-dot-myapp.appspot.com

# Switch traffic
gcloud app services set-traffic default --splits=v2=1.0

# Rollback if needed
gcloud app services set-traffic default --splits=v1=1.0
```

**Cloud Run Blue-Green with Traffic Split**:
```bash
# Deploy blue (current) version
gcloud run deploy myapp \
  --image gcr.io/project/myapp:blue \
  --tag blue \
  --region us-central1

# Deploy green (new) version without traffic
gcloud run deploy myapp \
  --image gcr.io/project/myapp:green \
  --tag green \
  --no-traffic \
  --region us-central1

# Test green version
curl https://green---myapp-uc.a.run.app

# Switch all traffic to green
gcloud run services update-traffic myapp \
  --to-revisions LATEST=100 \
  --region us-central1

# Or gradual switch
gcloud run services update-traffic myapp \
  --to-tags green=100 \
  --region us-central1
```

**GKE Blue-Green with Services**:
```yaml
# blue-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
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
        image: gcr.io/project/myapp:v1
        ports:
        - containerPort: 8080
---
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
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
        image: gcr.io/project/myapp:v2
        ports:
        - containerPort: 8080
---
# service.yaml - Switch between blue and green
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Change to 'green' to switch traffic
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### Canary Deployment

**Cloud Run Canary**:
```bash
# Deploy canary revision
gcloud run deploy myapp \
  --image gcr.io/project/myapp:canary \
  --tag canary \
  --no-traffic \
  --region us-central1

# Gradual rollout - 10%
gcloud run services update-traffic myapp \
  --to-tags stable=90,canary=10 \
  --region us-central1

# Monitor metrics, then increase to 50%
gcloud run services update-traffic myapp \
  --to-tags stable=50,canary=50 \
  --region us-central1

# Full rollout
gcloud run services update-traffic myapp \
  --to-tags canary=100 \
  --region us-central1

# Promote canary to stable
gcloud run services update-traffic myapp \
  --update-tags stable=LATEST \
  --region us-central1
```

**Automated Canary with Cloud Build**:
```yaml
# cloudbuild-canary.yaml
steps:
  # Build and push
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '.'

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA']

  # Deploy canary with 10% traffic
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--tag'
      - 'canary-$SHORT_SHA'
      - '--no-traffic'
      - '--region'
      - 'us-central1'

  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'services'
      - 'update-traffic'
      - 'myapp'
      - '--to-revisions'
      - 'canary-$SHORT_SHA=10'
      - '--region'
      - 'us-central1'

  # Wait and monitor (in practice, use Cloud Monitoring)
  - name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        sleep 300
        # Check error rate from Cloud Monitoring
        ERROR_RATE=$(gcloud monitoring time-series list \
          --filter='metric.type="run.googleapis.com/request_count" AND metric.label.response_code_class="5xx"' \
          --format='value(point.value.int64Value)')

        if [ "$ERROR_RATE" -gt 10 ]; then
          echo "Error rate too high, rolling back"
          exit 1
        fi

  # If successful, increase to 50%
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'services'
      - 'update-traffic'
      - 'myapp'
      - '--to-revisions'
      - 'canary-$SHORT_SHA=50'
      - '--region'
      - 'us-central1'
```

### Rolling Deployment (GKE)

**Rolling Update Strategy**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Max pods above desired count
      maxUnavailable: 1  # Max pods unavailable during update
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: gcr.io/project/myapp:v2
        ports:
        - containerPort: 8080
        # Health checks are critical for rolling updates
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 3
```

**Controlled Rolling Update**:
```bash
# Update deployment
kubectl set image deployment/myapp app=gcr.io/project/myapp:v2

# Watch rollout status
kubectl rollout status deployment/myapp

# Pause rollout
kubectl rollout pause deployment/myapp

# Resume rollout
kubectl rollout resume deployment/myapp

# Rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=2

# View rollout history
kubectl rollout history deployment/myapp
```

## Testing Strategies

### Unit Testing

**Python Unit Tests with pytest**:
```python
# tests/unit/test_order_service.py
import pytest
from unittest.mock import Mock, patch
from app.services.order_service import OrderService

@pytest.fixture
def order_service():
    return OrderService()

@pytest.fixture
def mock_db():
    with patch('app.services.order_service.db') as mock:
        yield mock

def test_create_order_success(order_service, mock_db):
    """Test successful order creation"""
    order_data = {
        'user_id': 'user123',
        'items': [{'sku': 'PROD-001', 'quantity': 2}],
        'total': 299.99
    }

    mock_db.insert.return_value = {'id': 'order-456'}

    result = order_service.create_order(order_data)

    assert result['id'] == 'order-456'
    mock_db.insert.assert_called_once()

def test_create_order_invalid_data(order_service):
    """Test order creation with invalid data"""
    invalid_data = {'user_id': 'user123'}  # Missing required fields

    with pytest.raises(ValueError):
        order_service.create_order(invalid_data)

def test_calculate_order_total(order_service):
    """Test order total calculation"""
    items = [
        {'price': 100.00, 'quantity': 2},
        {'price': 50.00, 'quantity': 1}
    ]

    total = order_service.calculate_total(items)

    assert total == 250.00
```

**Node.js Unit Tests with Jest**:
```javascript
// tests/unit/orderService.test.js
const OrderService = require('../../src/services/orderService');
const db = require('../../src/db');

jest.mock('../../src/db');

describe('OrderService', () => {
  let orderService;

  beforeEach(() => {
    orderService = new OrderService();
    jest.clearAllMocks();
  });

  test('creates order successfully', async () => {
    const orderData = {
      userId: 'user123',
      items: [{sku: 'PROD-001', quantity: 2}],
      total: 299.99,
    };

    db.insert.mockResolvedValue({id: 'order-456'});

    const result = await orderService.createOrder(orderData);

    expect(result.id).toBe('order-456');
    expect(db.insert).toHaveBeenCalledTimes(1);
  });

  test('throws error for invalid data', async () => {
    const invalidData = {userId: 'user123'};

    await expect(
      orderService.createOrder(invalidData)
    ).rejects.toThrow('Invalid order data');
  });

  test('calculates order total correctly', () => {
    const items = [
      {price: 100.00, quantity: 2},
      {price: 50.00, quantity: 1},
    ];

    const total = orderService.calculateTotal(items);

    expect(total).toBe(250.00);
  });
});
```

### Integration Testing

**Integration Test with Cloud Services**:
```python
# tests/integration/test_order_workflow.py
import pytest
import requests
from google.cloud import firestore, pubsub_v1

@pytest.fixture
def api_base_url():
    return "https://myapp-staging-uc.a.run.app"

@pytest.fixture
def db_client():
    return firestore.Client(project='my-project')

@pytest.fixture
def pubsub_client():
    return pubsub_v1.SubscriberClient()

def test_create_order_workflow(api_base_url, db_client):
    """Test complete order creation workflow"""
    # Create order via API
    order_data = {
        'user_id': 'test-user',
        'items': [{'sku': 'TEST-001', 'quantity': 1}],
        'total': 99.99
    }

    response = requests.post(
        f"{api_base_url}/api/orders",
        json=order_data,
        headers={'Authorization': 'Bearer test-token'}
    )

    assert response.status_code == 201
    order_id = response.json()['order_id']

    # Verify order in database
    doc = db_client.collection('orders').document(order_id).get()
    assert doc.exists
    assert doc.to_dict()['user_id'] == 'test-user'

    # Cleanup
    db_client.collection('orders').document(order_id).delete()

def test_order_notification_flow(api_base_url, pubsub_client):
    """Test order creates notification message"""
    subscription_path = pubsub_client.subscription_path(
        'my-project', 'order-notifications-test'
    )

    # Create order
    order_data = {
        'user_id': 'test-user',
        'items': [{'sku': 'TEST-001', 'quantity': 1}],
        'total': 99.99
    }

    response = requests.post(f"{api_base_url}/api/orders", json=order_data)
    order_id = response.json()['order_id']

    # Pull message from Pub/Sub
    response = pubsub_client.pull(
        subscription=subscription_path,
        max_messages=1,
        timeout=10
    )

    assert len(response.received_messages) == 1
    message = response.received_messages[0]
    assert message.message.data.decode('utf-8') == order_id

    # Acknowledge message
    pubsub_client.acknowledge(
        subscription=subscription_path,
        ack_ids=[message.ack_id]
    )
```

### End-to-End Testing

**E2E Test with Playwright**:
```python
# tests/e2e/test_order_flow.py
from playwright.sync_api import sync_playwright
import pytest

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

def test_complete_order_flow(browser):
    """Test complete user order flow"""
    page = browser.new_page()

    # Navigate to app
    page.goto("https://myapp.example.com")

    # Login
    page.click("text=Login")
    page.fill("input[name=email]", "test@example.com")
    page.fill("input[name=password]", "testpass123")
    page.click("button[type=submit]")

    # Wait for dashboard
    page.wait_for_selector("text=Dashboard")

    # Add product to cart
    page.click("text=Products")
    page.click("button[data-product=PROD-001]")
    page.click("text=Add to Cart")

    # Checkout
    page.click("text=Cart")
    page.click("text=Checkout")

    # Fill payment info
    page.fill("input[name=card_number]", "4242424242424242")
    page.fill("input[name=exp_date]", "12/25")
    page.fill("input[name=cvv]", "123")

    # Submit order
    page.click("button[type=submit]")

    # Verify success
    page.wait_for_selector("text=Order confirmed")
    order_id = page.locator("[data-order-id]").inner_text()

    assert len(order_id) > 0
```

### Load Testing

**Locust Load Test**:
```python
# tests/load/locustfile.py
from locust import HttpUser, task, between
import random

class OrderUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        """Login user"""
        response = self.client.post("/api/auth/login", json={
            "email": f"user{random.randint(1, 1000)}@example.com",
            "password": "testpass123"
        })
        self.token = response.json()['token']

    @task(3)
    def browse_products(self):
        """Browse products - most common action"""
        self.client.get("/api/products",
                       headers={"Authorization": f"Bearer {self.token}"})

    @task(2)
    def view_product(self):
        """View specific product"""
        product_id = random.choice(['PROD-001', 'PROD-002', 'PROD-003'])
        self.client.get(f"/api/products/{product_id}",
                       headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def create_order(self):
        """Create order - less frequent but important"""
        order_data = {
            "items": [
                {
                    "sku": random.choice(['PROD-001', 'PROD-002']),
                    "quantity": random.randint(1, 3)
                }
            ]
        }
        self.client.post("/api/orders",
                        json=order_data,
                        headers={"Authorization": f"Bearer {self.token}"})

# Run: locust -f locustfile.py --host=https://myapp.example.com
```

**Cloud Build Load Test Pipeline**:
```yaml
# cloudbuild-loadtest.yaml
steps:
  # Deploy to staging
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'myapp-staging'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--region'
      - 'us-central1'

  # Run load test
  - name: 'locustio/locust'
    args:
      - '-f'
      - 'tests/load/locustfile.py'
      - '--host=https://myapp-staging-uc.a.run.app'
      - '--users=100'
      - '--spawn-rate=10'
      - '--run-time=5m'
      - '--headless'
      - '--only-summary'

  # Check performance metrics
  - name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        # Query Cloud Monitoring for p99 latency
        P99=$(gcloud monitoring time-series list \
          --filter='metric.type="run.googleapis.com/request_latencies"' \
          --format='value(point.value.distributionValue.bucketOptions)')

        if [ "$P99" -gt 500 ]; then
          echo "P99 latency exceeds 500ms"
          exit 1
        fi
```

### Chaos Engineering

**Chaos Test with Litmus**:
```yaml
# chaos-experiment.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: myapp-chaos
  namespace: default
spec:
  appinfo:
    appns: default
    applabel: 'app=myapp'
    appkind: deployment
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'
            - name: CHAOS_INTERVAL
              value: '10'
            - name: FORCE
              value: 'false'
```

**Python Chaos Test**:
```python
# tests/chaos/test_resilience.py
import requests
import time
import random
from google.cloud import compute_v1

def test_instance_failure_resilience():
    """Test app resilience during instance failures"""
    compute_client = compute_v1.InstancesClient()
    project = 'my-project'
    zone = 'us-central1-a'
    instance_group = 'myapp-ig'

    # Get healthy instance count before chaos
    instances = compute_client.list(project=project, zone=zone)
    healthy_count = len([i for i in instances if i.status == 'RUNNING'])

    # Make baseline requests
    success_count = 0
    for _ in range(100):
        try:
            response = requests.get('https://myapp.example.com/health')
            if response.status_code == 200:
                success_count += 1
        except:
            pass

    baseline_success_rate = success_count / 100
    assert baseline_success_rate > 0.95

    # Inject chaos - delete random instance
    instances_list = list(instances)
    victim = random.choice(instances_list)
    compute_client.delete(project=project, zone=zone, instance=victim.name)

    # Continue making requests during chaos
    chaos_success_count = 0
    for _ in range(100):
        try:
            response = requests.get('https://myapp.example.com/health')
            if response.status_code == 200:
                chaos_success_count += 1
        except:
            pass
        time.sleep(0.5)

    chaos_success_rate = chaos_success_count / 100

    # Assert system remains available (>90% success)
    assert chaos_success_rate > 0.90

    # Verify auto-healing
    time.sleep(60)
    instances = compute_client.list(project=project, zone=zone)
    recovered_count = len([i for i in instances if i.status == 'RUNNING'])
    assert recovered_count == healthy_count
```

## Health Checks

### Liveness Probes

**Python Flask Liveness Endpoint**:
```python
from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/healthz')
def liveness():
    """Liveness probe - is the application running?"""
    # Check critical dependencies
    try:
        # Verify app can still process requests
        health_status = {
            'status': 'healthy',
            'timestamp': time.time()
        }
        return jsonify(health_status), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

@app.route('/healthz/detailed')
def detailed_liveness():
    """Detailed health check for debugging"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()

        health = {
            'status': 'healthy',
            'timestamp': time.time(),
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_mb': memory.available / 1024 / 1024
        }

        # Check if system is under extreme load
        if cpu_percent > 95 or memory.percent > 95:
            health['status'] = 'degraded'
            return jsonify(health), 200

        return jsonify(health), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503
```

### Readiness Probes

**Python Readiness Check**:
```python
from flask import Flask, jsonify
from google.cloud import firestore
from redis import Redis
import requests

app = Flask(__name__)

@app.route('/ready')
def readiness():
    """Readiness probe - can the application serve traffic?"""
    checks = {
        'database': check_database(),
        'cache': check_cache(),
        'external_api': check_external_api()
    }

    all_ready = all(checks.values())

    response = {
        'status': 'ready' if all_ready else 'not ready',
        'checks': checks,
        'timestamp': time.time()
    }

    status_code = 200 if all_ready else 503
    return jsonify(response), status_code

def check_database():
    """Check database connectivity"""
    try:
        db = firestore.Client()
        # Try to read a test document
        doc_ref = db.collection('health').document('check')
        doc_ref.get(timeout=2)
        return True
    except Exception as e:
        app.logger.error(f"Database check failed: {e}")
        return False

def check_cache():
    """Check Redis connectivity"""
    try:
        redis_client = Redis(host='redis-host', port=6379, socket_timeout=2)
        redis_client.ping()
        return True
    except Exception as e:
        app.logger.error(f"Cache check failed: {e}")
        return False

def check_external_api():
    """Check external API availability"""
    try:
        response = requests.get(
            'https://api.example.com/health',
            timeout=2
        )
        return response.status_code == 200
    except Exception as e:
        app.logger.error(f"External API check failed: {e}")
        return False
```

**Node.js Health Checks**:
```javascript
const express = require('express');
const {Firestore} = require('@google-cloud/firestore');
const redis = require('redis');
const axios = require('axios');

const app = express();
const db = new Firestore();
const redisClient = redis.createClient({
  host: 'redis-host',
  port: 6379,
});

// Liveness probe
app.get('/healthz', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
  });
});

// Readiness probe
app.get('/ready', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    cache: await checkCache(),
    externalApi: await checkExternalApi(),
  };

  const allReady = Object.values(checks).every(check => check);

  res.status(allReady ? 200 : 503).json({
    status: allReady ? 'ready' : 'not ready',
    checks,
    timestamp: new Date().toISOString(),
  });
});

async function checkDatabase() {
  try {
    await db.collection('health').doc('check').get();
    return true;
  } catch (err) {
    console.error('Database check failed:', err);
    return false;
  }
}

async function checkCache() {
  return new Promise((resolve) => {
    redisClient.ping((err, result) => {
      if (err) {
        console.error('Cache check failed:', err);
        resolve(false);
      } else {
        resolve(result === 'PONG');
      }
    });
  });
}

async function checkExternalApi() {
  try {
    const response = await axios.get('https://api.example.com/health', {
      timeout: 2000,
    });
    return response.status === 200;
  } catch (err) {
    console.error('External API check failed:', err);
    return false;
  }
}
```

### Startup Probes

**GKE Configuration with All Probes**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: gcr.io/project/myapp:v1
        ports:
        - containerPort: 8080

        # Startup probe - for slow-starting applications
        startupProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 10
          failureThreshold: 30  # 5 minutes to start
          successThreshold: 1

        # Liveness probe - restart if unhealthy
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
          failureThreshold: 3
          successThreshold: 1
          timeoutSeconds: 5

        # Readiness probe - remove from service if not ready
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 3
          successThreshold: 1
          timeoutSeconds: 3

        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**Cloud Run Health Checks**:
```yaml
# cloud-run-service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        # Startup timeout
        run.googleapis.com/startup-cpu-boost: 'true'
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
      - image: gcr.io/project/myapp:v1
        ports:
        - containerPort: 8080
        # Liveness probe
        livenessProbe:
          httpGet:
            path: /healthz
          initialDelaySeconds: 10
          periodSeconds: 10
        # Startup probe
        startupProbe:
          httpGet:
            path: /healthz
          initialDelaySeconds: 0
          periodSeconds: 1
          failureThreshold: 3
        resources:
          limits:
            memory: 512Mi
            cpu: '1'
```

## Traffic Management

### Load Balancing

**Cloud Run Traffic Split**:
```bash
# Split traffic between revisions
gcloud run services update-traffic myservice \
  --to-revisions=myservice-v1=50,myservice-v2=50 \
  --region=us-central1

# Split with tags
gcloud run services update-traffic myservice \
  --to-tags=stable=80,canary=20 \
  --region=us-central1

# Route based on URL
gcloud run services update-traffic myservice \
  --to-revisions=myservice-v1=100 \
  --tag=stable \
  --region=us-central1

# Access via: https://stable---myservice-uc.a.run.app
```

**GKE with Istio Traffic Management**:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp.example.com
  http:
  # Route beta users to v2
  - match:
    - headers:
        cookie:
          exact: "version=beta"
    route:
    - destination:
        host: myapp
        subset: v2
      weight: 100

  # Route specific users to canary
  - match:
    - headers:
        x-user-id:
          prefix: "test-"
    route:
    - destination:
        host: myapp
        subset: canary
      weight: 100

  # Default traffic split
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
apiVersion: networking.istio.io/v1alpha3
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
  - name: canary
    labels:
      version: canary
```

## Best Practices

### Monitoring Best Practices

1. **Implement Comprehensive Observability**
   - Use Cloud Monitoring for metrics
   - Implement Cloud Trace for distributed tracing
   - Use Cloud Logging for structured logs
   - Set up Cloud Error Reporting for error tracking
   - Enable Cloud Profiler for performance analysis

2. **Custom Metrics Strategy**
   - Create business KPI metrics (orders, revenue, conversions)
   - Monitor application-specific metrics (cache hit rate, queue depth)
   - Use metric labels for dimensional data
   - Set up log-based metrics for derived data

3. **Alerting and SLOs**
   - Define SLIs (Service Level Indicators)
   - Set SLOs (Service Level Objectives)
   - Create alerting policies with appropriate thresholds
   - Use error budgets for release decisions
   - Implement notification channels (email, Slack, PagerDuty)

4. **Logging Standards**
   - Use structured logging (JSON format)
   - Include correlation IDs in all logs
   - Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)
   - Avoid logging sensitive data (PII, credentials)
   - Use sampling for high-volume logs

5. **Observability in Code**
   - Add tracing to all microservices
   - Include context propagation across services
   - Monitor external API calls
   - Track database query performance
   - Record custom metrics for business events

### Deployment Best Practices

1. **CI/CD Pipeline**
   - Automate all builds and deployments
   - Run tests in pipeline (unit, integration, e2e)
   - Perform security scans (Trivy, Snyk)
   - Use artifact repositories (GCR, Artifact Registry)
   - Implement approval gates for production

2. **Deployment Strategies**
   - Use blue-green for major changes
   - Use canary for gradual rollouts
   - Use rolling updates for minor changes
   - Implement feature flags for controlled releases
   - Always have rollback procedures

3. **Environment Management**
   - Separate dev, staging, production environments
   - Use infrastructure as code (Terraform, Deployment Manager)
   - Environment-specific configurations
   - Isolate production data
   - Use least privilege IAM for each environment

4. **Version Control**
   - Tag releases with semantic versioning
   - Use GitOps for deployment automation
   - Maintain deployment history
   - Document rollback procedures
   - Use branching strategy (GitFlow, trunk-based)

5. **Testing Strategy**
   - Run unit tests on every commit
   - Run integration tests before deployment
   - Perform load testing before major releases
   - Conduct chaos engineering in staging
   - Use canary deployments as production tests

### Performance Best Practices

1. **Application Performance**
   - Profile with Cloud Profiler regularly
   - Optimize database queries
   - Implement caching (Memorystore, CDN)
   - Use async processing for long tasks
   - Optimize container images (multi-stage builds)

2. **Resource Management**
   - Right-size compute resources
   - Use autoscaling appropriately
   - Implement connection pooling
   - Use regional resources for low latency
   - Monitor and optimize costs

3. **API Performance**
   - Implement rate limiting
   - Use API Gateway for centralized management
   - Cache frequently accessed data
   - Use pagination for large datasets
   - Implement request compression

## Deployment Scenarios

### Scenario 1: Zero-Downtime Production Deployment

**Challenge**: Deploy new version to production without any downtime or user impact.

**Solution**:
```yaml
# cloudbuild-zero-downtime.yaml
steps:
  # Build and test
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA', '.']

  - name: 'python:3.9'
    entrypoint: 'python'
    args: ['-m', 'pytest', 'tests/']

  # Deploy to Cloud Run with no traffic
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--tag'
      - 'rev-$SHORT_SHA'
      - '--no-traffic'
      - '--region'
      - 'us-central1'

  # Smoke test new revision
  - name: 'gcr.io/cloud-builders/curl'
    args:
      - '-f'
      - 'https://rev-$SHORT_SHA---myapp-uc.a.run.app/health'

  # Gradual traffic migration
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'services'
      - 'update-traffic'
      - 'myapp'
      - '--to-revisions'
      - 'rev-$SHORT_SHA=100'
      - '--region'
      - 'us-central1'
```

**Key Points**:
- Deploy with `--no-traffic` first
- Test new revision before routing traffic
- Use instant traffic switch (100% to new)
- Keep old revision for quick rollback

### Scenario 2: Canary Deployment with Automated Rollback

**Challenge**: Deploy new version gradually, automatically rollback if error rate increases.

**Solution**:
```yaml
# cloudbuild-canary.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA', '.']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA']

  # Deploy canary
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--tag'
      - 'canary'
      - '--no-traffic'
      - '--region'
      - 'us-central1'

  # 10% traffic to canary
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'services'
      - 'update-traffic'
      - 'myapp'
      - '--to-tags'
      - 'stable=90,canary=10'
      - '--region'
      - 'us-central1'

  # Monitor for 5 minutes
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        sleep 300
        ERROR_RATE=$(gcloud monitoring time-series list \
          --filter='metric.type="run.googleapis.com/request_count"
            AND metric.label.response_code_class="5xx"
            AND metric.label.service_name="myapp"' \
          --format='value(point.value.int64Value)' \
          --interval-start="$(date -u -d '5 minutes ago' '+%Y-%m-%dT%H:%M:%SZ')" \
          | awk '{sum+=$1} END {print sum}')

        TOTAL_REQUESTS=$(gcloud monitoring time-series list \
          --filter='metric.type="run.googleapis.com/request_count"
            AND metric.label.service_name="myapp"' \
          --format='value(point.value.int64Value)' \
          --interval-start="$(date -u -d '5 minutes ago' '+%Y-%m-%dT%H:%M:%SZ')" \
          | awk '{sum+=$1} END {print sum}')

        ERROR_PERCENTAGE=$(echo "scale=2; $ERROR_RATE * 100 / $TOTAL_REQUESTS" | bc)

        if (( $(echo "$ERROR_PERCENTAGE > 1.0" | bc -l) )); then
          echo "Error rate $ERROR_PERCENTAGE% exceeds threshold, rolling back"
          gcloud run services update-traffic myapp \
            --to-tags stable=100 \
            --region us-central1
          exit 1
        fi

  # Increase to 50%
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'services'
      - 'update-traffic'
      - 'myapp'
      - '--to-tags'
      - 'stable=50,canary=50'
      - '--region'
      - 'us-central1'

  # Monitor again
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - 'sleep 300 && # monitoring logic repeated'

  # Full rollout
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'services'
      - 'update-traffic'
      - 'myapp'
      - '--to-tags'
      - 'canary=100'
      - '--region'
      - 'us-central1'

  # Update stable tag
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'services'
      - 'update-traffic'
      - 'myapp'
      - '--update-tags'
      - 'stable=LATEST'
      - '--region'
      - 'us-central1'
```

### Scenario 3: Multi-Region Deployment

**Challenge**: Deploy application to multiple regions with proper monitoring and failover.

**Solution**:
```yaml
# cloudbuild-multiregion.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA', '.']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA']

  # Deploy to us-central1
  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'deploy-us-central1'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'

  # Deploy to us-east1
  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'deploy-us-east1'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--region'
      - 'us-east1'
      - '--platform'
      - 'managed'

  # Deploy to europe-west1
  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'deploy-europe-west1'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--region'
      - 'europe-west1'
      - '--platform'
      - 'managed'

  # Update global load balancer
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'compute'
      - 'backend-services'
      - 'update'
      - 'myapp-backend'
      - '--global'

  # Verify all regions
  - name: 'gcr.io/cloud-builders/curl'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        for region in us-central1 us-east1 europe-west1; do
          echo "Testing $region"
          curl -f "https://myapp-$region-uc.a.run.app/health" || exit 1
        done
```

### Scenario 4: Database Migration with Zero Downtime

**Challenge**: Deploy application with database schema changes without downtime.

**Solution**:
```yaml
# cloudbuild-db-migration.yaml
steps:
  # Build new version
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA', '.']

  # Run database migration
  - name: 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
    entrypoint: 'python'
    args:
      - '-m'
      - 'alembic'
      - 'upgrade'
      - 'head'
    env:
      - 'DB_HOST=${_DB_HOST}'
      - 'DB_NAME=${_DB_NAME}'

  # Deploy new version (compatible with old schema)
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'myapp'
      - '--image'
      - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
      - '--region'
      - 'us-central1'

  # Wait for deployment to stabilize
  - name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - 'sleep 60'

  # Verify application health
  - name: 'gcr.io/cloud-builders/curl'
    args: ['-f', 'https://myapp-uc.a.run.app/health']

  # Clean up old schema (if needed)
  - name: 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
    entrypoint: 'python'
    args:
      - '-m'
      - 'scripts.cleanup_old_schema'
    env:
      - 'DB_HOST=${_DB_HOST}'
      - 'DB_NAME=${_DB_NAME}'

substitutions:
  _DB_HOST: 'cloudsql-proxy:5432'
  _DB_NAME: 'production'
```

**Migration Strategy**:
1. Make schema changes backward compatible
2. Deploy code that works with both old and new schema
3. Run migration to add new columns/tables
4. Deploy code that uses new schema
5. Remove old columns/tables in later migration

### Scenario 5: Feature Flag Rollout

**Challenge**: Deploy new feature behind feature flag, gradually enable for users.

**Python Feature Flag Implementation**:
```python
# app/feature_flags.py
from google.cloud import firestore
import functools

class FeatureFlags:
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)
        self.cache = {}

    def is_enabled(self, flag_name: str, user_id: str = None) -> bool:
        """Check if feature flag is enabled for user"""
        # Check cache first
        cache_key = f"{flag_name}:{user_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Get flag configuration
        flag_doc = self.db.collection('feature_flags').document(flag_name).get()
        if not flag_doc.exists:
            return False

        flag_config = flag_doc.to_dict()

        # Check if globally enabled
        if flag_config.get('enabled', False):
            return True

        # Check rollout percentage
        rollout_pct = flag_config.get('rollout_percentage', 0)
        if user_id:
            # Consistent hashing for user
            user_hash = hash(user_id) % 100
            enabled = user_hash < rollout_pct
            self.cache[cache_key] = enabled
            return enabled

        return False

    def require_flag(self, flag_name: str):
        """Decorator to require feature flag"""
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                user_id = kwargs.get('user_id') or getattr(g, 'user_id', None)
                if not self.is_enabled(flag_name, user_id):
                    return {'error': 'Feature not available'}, 403
                return f(*args, **kwargs)
            return wrapper
        return decorator

# Usage
from flask import Flask, g
app = Flask(__name__)
flags = FeatureFlags(project_id='my-project')

@app.route('/api/new-feature', methods=['POST'])
@flags.require_flag('new_checkout_flow')
def new_feature():
    # New feature implementation
    return {'result': 'success'}
```

**Feature Flag Configuration** (Firestore):
```json
{
  "feature_flags/new_checkout_flow": {
    "enabled": false,
    "rollout_percentage": 10,
    "description": "New checkout flow with improved UX",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

### Scenario 6: Rollback Procedure

**Challenge**: Quickly rollback a problematic deployment.

**Cloud Run Rollback**:
```bash
# List revisions
gcloud run revisions list --service=myapp --region=us-central1

# Identify working revision
PREVIOUS_REVISION=$(gcloud run revisions list \
  --service=myapp \
  --region=us-central1 \
  --format='value(name)' \
  --sort-by='~metadata.creationTimestamp' \
  --limit=2 | tail -1)

# Rollback to previous revision
gcloud run services update-traffic myapp \
  --to-revisions=$PREVIOUS_REVISION=100 \
  --region=us-central1

# Verify rollback
curl https://myapp-uc.a.run.app/health
```

**GKE Rollback**:
```bash
# Check rollout history
kubectl rollout history deployment/myapp

# Rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=3

# Monitor rollback
kubectl rollout status deployment/myapp
```

**Automated Rollback on High Error Rate**:
```python
# scripts/auto_rollback.py
from google.cloud import monitoring_v3, run_v2
import time

def check_error_rate(project_id: str, service_name: str) -> float:
    """Check error rate from Cloud Monitoring"""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Query for error rate
    interval = monitoring_v3.TimeInterval({
        "end_time": {"seconds": int(time.time())},
        "start_time": {"seconds": int(time.time() - 300)},  # Last 5 min
    })

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type="run.googleapis.com/request_count" '
                     f'AND metric.label.response_code_class="5xx" '
                     f'AND resource.label.service_name="{service_name}"',
            "interval": interval,
        }
    )

    error_count = sum([point.value.int64_value
                      for result in results
                      for point in result.points])

    # Get total requests
    total_results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type="run.googleapis.com/request_count" '
                     f'AND resource.label.service_name="{service_name}"',
            "interval": interval,
        }
    )

    total_count = sum([point.value.int64_value
                       for result in total_results
                       for point in result.points])

    if total_count == 0:
        return 0

    return (error_count / total_count) * 100

def rollback_service(project_id: str, service_name: str, region: str):
    """Rollback to previous revision"""
    client = run_v2.ServicesClient()

    # Get current service
    service_path = f"projects/{project_id}/locations/{region}/services/{service_name}"
    service = client.get_service(name=service_path)

    # Get previous revision
    revisions = list(service.traffic)
    if len(revisions) < 2:
        print("No previous revision to rollback to")
        return

    previous_revision = revisions[1].revision

    # Update traffic to previous revision
    service.traffic = [{
        "revision": previous_revision,
        "percent": 100
    }]

    client.update_service(service=service)
    print(f"Rolled back to {previous_revision}")

# Monitor and auto-rollback
if __name__ == "__main__":
    project_id = "my-project"
    service_name = "myapp"
    region = "us-central1"

    while True:
        error_rate = check_error_rate(project_id, service_name)
        print(f"Current error rate: {error_rate:.2f}%")

        if error_rate > 5.0:  # 5% threshold
            print("Error rate exceeds threshold, initiating rollback")
            rollback_service(project_id, service_name, region)
            break

        time.sleep(60)  # Check every minute
```

### Scenario 7: A/B Testing Deployment

**Challenge**: Deploy two versions for A/B testing with proper tracking.

**Cloud Run A/B Setup**:
```bash
# Deploy version A (control)
gcloud run deploy myapp \
  --image gcr.io/project/myapp:version-a \
  --tag version-a \
  --region us-central1

# Deploy version B (variant)
gcloud run deploy myapp \
  --image gcr.io/project/myapp:version-b \
  --tag version-b \
  --no-traffic \
  --region us-central1

# Split traffic 50/50
gcloud run services update-traffic myapp \
  --to-tags version-a=50,version-b=50 \
  --region us-central1
```

**A/B Testing with Header Routing** (Istio):
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp-ab-test
spec:
  hosts:
  - myapp.example.com
  http:
  - match:
    - headers:
        x-ab-test:
          exact: "variant-b"
    route:
    - destination:
        host: myapp
        subset: version-b
  - route:
    - destination:
        host: myapp
        subset: version-a
      weight: 50
    - destination:
        host: myapp
        subset: version-b
      weight: 50
```

**Tracking A/B Test Results**:
```python
# app/ab_testing.py
from google.cloud import monitoring_v3
import hashlib

def get_ab_variant(user_id: str) -> str:
    """Consistently assign user to A/B test variant"""
    hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    return 'b' if hash_value % 2 == 0 else 'a'

def track_conversion(user_id: str, variant: str, conversion_value: float):
    """Track conversion for A/B test"""
    monitoring = CloudMonitoring(project_id='my-project')
    monitoring.write_custom_metric(
        metric_type=f"ab_test/conversion",
        value=conversion_value,
        labels={
            'variant': variant,
            'user_id': user_id
        }
    )

# Usage in endpoint
@app.route('/api/checkout', methods=['POST'])
def checkout():
    user_id = g.user_id
    variant = get_ab_variant(user_id)

    if variant == 'b':
        result = new_checkout_flow(request.json)
    else:
        result = old_checkout_flow(request.json)

    if result['success']:
        track_conversion(user_id, variant, result['order_total'])

    return result
```

### Scenario 8: Microservices Deployment Orchestration

**Challenge**: Deploy multiple microservices with dependencies in correct order.

**Solution**:
```yaml
# cloudbuild-microservices.yaml
steps:
  # Build all services in parallel
  - name: 'gcr.io/cloud-builders/docker'
    id: 'build-auth'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/auth:$COMMIT_SHA', './services/auth']
    waitFor: ['-']

  - name: 'gcr.io/cloud-builders/docker'
    id: 'build-orders'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/orders:$COMMIT_SHA', './services/orders']
    waitFor: ['-']

  - name: 'gcr.io/cloud-builders/docker'
    id: 'build-payments'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/payments:$COMMIT_SHA', './services/payments']
    waitFor: ['-']

  - name: 'gcr.io/cloud-builders/docker'
    id: 'build-notifications'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/notifications:$COMMIT_SHA', './services/notifications']
    waitFor: ['-']

  # Push all images
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/auth:$COMMIT_SHA']
    waitFor: ['build-auth']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/orders:$COMMIT_SHA']
    waitFor: ['build-orders']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/payments:$COMMIT_SHA']
    waitFor: ['build-payments']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/notifications:$COMMIT_SHA']
    waitFor: ['build-notifications']

  # Deploy in dependency order: auth first (no dependencies)
  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'deploy-auth'
    args:
      - 'run'
      - 'deploy'
      - 'auth-service'
      - '--image'
      - 'gcr.io/$PROJECT_ID/auth:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
    waitFor: ['push-auth']

  # Deploy services that depend on auth
  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'deploy-orders'
    args:
      - 'run'
      - 'deploy'
      - 'orders-service'
      - '--image'
      - 'gcr.io/$PROJECT_ID/orders:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--set-env-vars'
      - 'AUTH_SERVICE_URL=https://auth-service-uc.a.run.app'
    waitFor: ['deploy-auth']

  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'deploy-payments'
    args:
      - 'run'
      - 'deploy'
      - 'payments-service'
      - '--image'
      - 'gcr.io/$PROJECT_ID/payments:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--set-env-vars'
      - 'AUTH_SERVICE_URL=https://auth-service-uc.a.run.app'
    waitFor: ['deploy-auth']

  # Deploy notifications last (depends on orders)
  - name: 'gcr.io/cloud-builders/gcloud'
    id: 'deploy-notifications'
    args:
      - 'run'
      - 'deploy'
      - 'notifications-service'
      - '--image'
      - 'gcr.io/$PROJECT_ID/notifications:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--set-env-vars'
      - 'ORDERS_SERVICE_URL=https://orders-service-uc.a.run.app'
    waitFor: ['deploy-orders']

  # Run integration tests
  - name: 'python:3.9'
    entrypoint: 'python'
    args:
      - '-m'
      - 'pytest'
      - 'tests/integration/test_microservices.py'
    env:
      - 'AUTH_URL=https://auth-service-uc.a.run.app'
      - 'ORDERS_URL=https://orders-service-uc.a.run.app'
    waitFor: ['deploy-notifications']
```

## Exam Tips

### Monitoring and Observability Questions

1. **Custom Metrics**
   - Know how to create custom metrics using Cloud Monitoring API
   - Understand metric types: GAUGE, DELTA, CUMULATIVE
   - Remember to use labels for dimensional data
   - Metric naming convention: `custom.googleapis.com/metric_name`

2. **Distributed Tracing**
   - Prefer OpenTelemetry over native Cloud Trace API
   - Auto-instrumentation for common frameworks (Flask, Express)
   - Context propagation across microservices
   - Span attributes for filtering and analysis

3. **Error Reporting**
   - Automatic error grouping by stack trace
   - HTTP context for web applications
   - User context for tracking affected users
   - Integration with logging and monitoring

4. **Log-Based Metrics**
   - Create metrics from structured logs
   - Use for derived metrics not available in Cloud Monitoring
   - Support for counter and distribution metrics
   - Filter expressions for log selection

### CI/CD Pipeline Questions

1. **Cloud Build**
   - `cloudbuild.yaml` is the default configuration file
   - Built-in substitutions: `$PROJECT_ID`, `$COMMIT_SHA`, `$SHORT_SHA`, `$TAG_NAME`
   - Custom substitutions start with underscore: `$_ENVIRONMENT`
   - Use `waitFor` to control step dependencies
   - `waitFor: ['-']` means run in parallel

2. **Build Triggers**
   - Can trigger on push, tag, or pull request
   - Branch patterns use regex: `^main$`, `^feature/.*$`
   - Tag patterns for releases: `^v.*`
   - Substitutions can be overridden per trigger

3. **Container Registry**
   - GCR (Container Registry) vs Artifact Registry
   - Artifact Registry is preferred for new projects
   - Images: `gcr.io/PROJECT_ID/IMAGE:TAG`
   - Vulnerability scanning available

4. **Testing in Pipeline**
   - Unit tests should run before building container
   - Integration tests after deployment to staging
   - Load tests before production deployment
   - Security scans (Trivy, Snyk) on container images

### Deployment Strategy Questions

1. **Blue-Green Deployment**
   - Two identical environments (blue and green)
   - Switch traffic instantly between versions
   - Easy rollback by switching back
   - Cloud Run: Use `--no-traffic` then switch
   - App Engine: Use `--no-promote` then `set-traffic`

2. **Canary Deployment**
   - Gradual rollout to subset of users
   - Monitor metrics at each stage
   - Typically: 10% → 50% → 100%
   - Cloud Run: Use traffic splitting by percentage
   - Automated rollback based on error rate

3. **Rolling Deployment**
   - Used in GKE with Deployments
   - `maxSurge`: Extra pods during update
   - `maxUnavailable`: Pods down during update
   - Health checks are critical
   - Automatic rollback on failed health checks

4. **Traffic Splitting**
   - Cloud Run: By revision or tag
   - App Engine: By version
   - GKE with Istio: By headers, cookies, or percentage
   - Use tags for persistent URLs: `tag---service-region.a.run.app`

### Health Check Questions

1. **Liveness Probe**
   - Should the container be restarted?
   - Simple check: Can the app respond?
   - Don't check dependencies (use readiness for that)
   - Failed liveness → container restart

2. **Readiness Probe**
   - Can the container serve traffic?
   - Check all dependencies (database, cache, APIs)
   - Failed readiness → removed from load balancer
   - Container not restarted

3. **Startup Probe**
   - For slow-starting applications
   - Disables liveness/readiness until startup succeeds
   - Prevents premature restarts during initialization
   - Use longer `failureThreshold` for startup time

4. **Probe Configuration**
   - `initialDelaySeconds`: Wait before first check
   - `periodSeconds`: How often to check
   - `failureThreshold`: Failures before action
   - `successThreshold`: Successes to recover
   - `timeoutSeconds`: Probe timeout

### Common Exam Patterns

1. **Choose the right deployment strategy**
   - Zero downtime required → Blue-green or Canary
   - Gradual rollout with monitoring → Canary
   - Testing new version with subset → A/B testing
   - GKE with limited resources → Rolling update
   - Database migration → Blue-green with compatible changes

2. **Monitoring integration**
   - Business metrics → Custom metrics
   - Request tracing → Cloud Trace
   - Error tracking → Error Reporting
   - Performance analysis → Cloud Profiler
   - Log analysis → Log-based metrics

3. **CI/CD troubleshooting**
   - Build fails: Check dependencies, test, image size
   - Deployment fails: Check IAM permissions, quotas
   - Tests fail: Check environment variables, test data
   - Slow builds: Use caching, parallel steps

4. **Traffic management**
   - Header-based routing → Istio VirtualService
   - Percentage-based split → Cloud Run traffic split
   - A/B testing → Header routing or consistent hashing
   - Multi-region → Global Load Balancer

### Quick Reference

**Cloud Run Deployment**:
```bash
gcloud run deploy SERVICE --image IMAGE --region REGION
```

**Traffic Split**:
```bash
gcloud run services update-traffic SERVICE --to-revisions=REV1=50,REV2=50
```

**Build Trigger**:
```bash
gcloud builds triggers create github --repo-name=REPO --branch-pattern=PATTERN
```

**Rollback**:
```bash
kubectl rollout undo deployment/NAME
```

## Additional Resources

- [Cloud Monitoring Documentation](https://cloud.google.com/monitoring/docs)
- [Cloud Trace Documentation](https://cloud.google.com/trace/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Deployment Best Practices](https://cloud.google.com/architecture/application-deployment-and-testing-strategies)
- [Cloud Run Deployment](https://cloud.google.com/run/docs/deploying)
- [GKE Deployment Strategies](https://cloud.google.com/kubernetes-engine/docs/concepts/deployment)
- [OpenTelemetry on GCP](https://cloud.google.com/learn/what-is-opentelemetry)

## Key terms

- **Cloud Monitoring** - the Google Cloud service for metrics, dashboards, uptime checks and alerting.
- **Cloud Trace** - the Google Cloud service that collects latency data to show how requests move through an application.
- **Error Reporting** - the Google Cloud service that groups and surfaces application errors and exceptions.
- **Cloud Profiler** - the Google Cloud service that continuously profiles CPU and memory use in production applications.
- **Log-based metric** - a metric that Cloud Logging computes from the log entries that match a filter.
- **Structured logging** - writing log entries as JSON so fields can be filtered and queried.
