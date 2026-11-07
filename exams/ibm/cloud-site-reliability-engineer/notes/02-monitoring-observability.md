# IBM Cloud Site Reliability Engineer (C1000-179) - Monitoring & Observability

## Table of Contents
- [Monitoring Strategy](#monitoring-strategy)
- [IBM Cloud Monitoring](#ibm-cloud-monitoring)
- [Logging and Log Analysis](#logging-and-log-analysis)
- [Distributed Tracing](#distributed-tracing)
- [Alerting and Notifications](#alerting-and-notifications)
- [SLIs, SLOs, and SLAs](#slis-slos-and-slas)

---

## Monitoring Strategy

### Four Golden Signals
1. **Latency**: Time to service requests
2. **Traffic**: Demand on system
3. **Errors**: Rate of failed requests
4. **Saturation**: Resource utilization

### Monitoring Layers
```
┌─────────────────────────────────────┐
│     Business Metrics (KPIs)         │
│  - Order completion rate            │
│  - User sign-ups                    │
│  - Revenue per hour                 │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│     Application Metrics             │
│  - Request rate, latency            │
│  - Error rates                      │
│  - Database query time              │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│     Infrastructure Metrics          │
│  - CPU, memory, disk                │
│  - Network throughput               │
│  - Container restarts               │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│     Platform Metrics                │
│  - Node health                      │
│  - API server latency               │
│  - etcd performance                 │
└─────────────────────────────────────┘
```

---

## IBM Cloud Monitoring

### Sysdig Agent Deployment
```yaml
# sysdig-agent-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: sysdig-agent
  namespace: ibm-observe
spec:
  selector:
    matchLabels:
      app: sysdig-agent
  template:
    metadata:
      labels:
        app: sysdig-agent
    spec:
      serviceAccountName: sysdig-agent
      hostNetwork: true
      hostPID: true
      tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/master
      containers:
      - name: sysdig-agent
        image: quay.io/sysdig/agent:latest
        securityContext:
          privileged: true
        env:
        - name: ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: sysdig-agent
              key: access-key
        - name: COLLECTOR
          value: "ingest.us-south.monitoring.cloud.ibm.com"
        - name: COLLECTOR_PORT
          value: "6443"
        - name: TAGS
          value: "env:production,region:us-south"
        - name: ADDITIONAL_CONF
          value: |
            prometheus:
              enabled: true
              interval: 30
              log_errors: true
            use_container_filter: true
            new_k8s: true
            k8s_cluster_name: prod-cluster
        volumeMounts:
        - mountPath: /host/var/run/docker.sock
          name: docker-sock
        - mountPath: /host/dev
          name: dev
        - mountPath: /host/proc
          name: proc
          readOnly: true
        - mountPath: /host/boot
          name: boot
          readOnly: true
        - mountPath: /host/lib/modules
          name: modules
          readOnly: true
        - mountPath: /host/usr
          name: usr
          readOnly: true
        resources:
          requests:
            memory: "512Mi"
            cpu: "200m"
          limits:
            memory: "1024Mi"
            cpu: "1000m"
      volumes:
      - name: docker-sock
        hostPath:
          path: /var/run/docker.sock
      - name: dev
        hostPath:
          path: /dev
      - name: proc
        hostPath:
          path: /proc
      - name: boot
        hostPath:
          path: /boot
      - name: modules
        hostPath:
          path: /lib/modules
      - name: usr
        hostPath:
          path: /usr
```

### Custom Metrics with StatsD
```javascript
// custom-metrics.js
const StatsD = require('node-statsd');

const statsd = new StatsD({
  host: 'localhost',
  port: 8125,
  prefix: 'myapp.',
  global_tags: ['env:production', 'service:api']
});

// Business metrics
function recordOrder(orderId, amount) {
  statsd.increment('orders.total');
  statsd.histogram('orders.value', amount);
  statsd.gauge('orders.in_progress', getInProgressOrders());
}

// Application metrics
function recordAPICall(endpoint, duration, statusCode) {
  statsd.timing(`api.${endpoint}.response_time`, duration);
  statsd.increment(`api.${endpoint}.requests`, 1, [`status:${statusCode}`]);
  
  if (statusCode >= 500) {
    statsd.increment('api.errors.5xx');
  } else if (statusCode >= 400) {
    statsd.increment('api.errors.4xx');
  }
}

// Database metrics
function recordDatabaseQuery(queryType, duration) {
  statsd.timing(`database.query.${queryType}`, duration);
  statsd.increment(`database.queries.${queryType}`);
}

// Cache metrics
function recordCacheOperation(operation, hit) {
  statsd.increment(`cache.${operation}.total`);
  if (hit) {
    statsd.increment(`cache.${operation}.hits`);
  } else {
    statsd.increment(`cache.${operation}.misses`);
  }
}

// Middleware for Express
function metricsMiddleware(req, res, next) {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    const route = req.route ? req.route.path : 'unknown';
    recordAPICall(route, duration, res.statusCode);
  });
  
  next();
}

module.exports = {
  recordOrder,
  recordAPICall,
  recordDatabaseQuery,
  recordCacheOperation,
  metricsMiddleware
};
```

### Prometheus Integration
```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 30s
      evaluation_interval: 30s
      external_labels:
        cluster: 'prod-cluster'
        region: 'us-south'
    
    scrape_configs:
      - job_name: 'kubernetes-apiservers'
        kubernetes_sd_configs:
        - role: endpoints
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabel_configs:
        - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
          action: keep
          regex: default;kubernetes;https
      
      - job_name: 'kubernetes-nodes'
        kubernetes_sd_configs:
        - role: node
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabel_configs:
        - action: labelmap
          regex: __meta_kubernetes_node_label_(.+)
      
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
        - role: pod
        relabel_configs:
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
          action: keep
          regex: true
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
          action: replace
          target_label: __metrics_path__
          regex: (.+)
        - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
          action: replace
          regex: ([^:]+)(?::\d+)?;(\d+)
          replacement: $1:$2
          target_label: __address__
        - action: labelmap
          regex: __meta_kubernetes_pod_label_(.+)
        - source_labels: [__meta_kubernetes_namespace]
          action: replace
          target_label: kubernetes_namespace
        - source_labels: [__meta_kubernetes_pod_name]
          action: replace
          target_label: kubernetes_pod_name
      
      - job_name: 'application-metrics'
        static_configs:
        - targets: ['api-service:9090', 'worker-service:9090']
          labels:
            service: 'backend'
    
    rule_files:
      - /etc/prometheus/rules/*.yml
    
    alerting:
      alertmanagers:
      - static_configs:
        - targets: ['alertmanager:9093']
```

### Grafana Dashboards
```json
{
  "dashboard": {
    "title": "Application Performance Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{endpoint}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "5xx Errors"
          },
          {
            "expr": "rate(http_requests_total{status=~\"4..\"}[5m])",
            "legendFormat": "4xx Errors"
          }
        ]
      },
      {
        "title": "Database Query Time",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(database_query_duration_seconds_sum[5m]) / rate(database_query_duration_seconds_count[5m])",
            "legendFormat": "{{query_type}}"
          }
        ]
      }
    ]
  }
}
```

---

## Logging and Log Analysis

> **Retired service:** IBM Log Analysis (LogDNA) and IBM Cloud Activity Tracker are retired. IBM Cloud Logs provides replacement functions for both (per [IBM's Cloud Logs announcement](https://www.ibm.com/new/product-blog/ibm-cloud-logs-observability)). Read the Log Analysis material below as the legacy model and map it to IBM Cloud Logs.

### Structured Logging
```javascript
// logger.js
const winston = require('winston');
const { LogDNA } = require('logdna-winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'api-service',
    environment: process.env.NODE_ENV,
    version: process.env.APP_VERSION,
    hostname: process.env.HOSTNAME
  },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    new LogDNA({
      key: process.env.LOGDNA_KEY,
      hostname: process.env.HOSTNAME,
      app: 'api-service',
      env: process.env.NODE_ENV,
      index_meta: true
    })
  ]
});

// Request logging middleware
function requestLogger(req, res, next) {
  const start = Date.now();
  
  // Log request
  logger.info('HTTP Request', {
    method: req.method,
    url: req.url,
    headers: {
      'user-agent': req.get('user-agent'),
      'x-correlation-id': req.get('x-correlation-id')
    },
    query: req.query,
    ip: req.ip
  });
  
  // Log response
  res.on('finish', () => {
    const duration = Date.now() - start;
    
    const logLevel = res.statusCode >= 500 ? 'error' : 
                     res.statusCode >= 400 ? 'warn' : 'info';
    
    logger.log(logLevel, 'HTTP Response', {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration,
      correlationId: req.get('x-correlation-id')
    });
  });
  
  next();
}

// Error logging
function logError(error, context = {}) {
  logger.error('Application Error', {
    error: {
      message: error.message,
      stack: error.stack,
      name: error.name
    },
    ...context
  });
}

// Business event logging
function logBusinessEvent(eventType, data) {
  logger.info('Business Event', {
    eventType,
    data,
    timestamp: new Date().toISOString()
  });
}

module.exports = { logger, requestLogger, logError, logBusinessEvent };
```

### Log Queries (LogDNA/Log Analysis)
```
# Find errors in last hour
level:error timestamp:>now-1h

# Find slow API calls
duration:>1000 service:api

# Find specific user activity
userId:"user-123" action:order_created

# Find database connection errors
message:"database connection failed" service:*

# Aggregate error counts by service
_exists_:error | stats count() by service

# Find 5xx errors with correlation IDs
status:5* | fields correlationId, message, service

# Find high-latency requests
duration:>2000 | stats avg(duration), max(duration), count() by endpoint
```

### Fluentd Configuration
```yaml
# fluentd-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>
    
    <filter kubernetes.**>
      @type kubernetes_metadata
      @id filter_kube_metadata
    </filter>
    
    <filter kubernetes.**>
      @type parser
      key_name log
      <parse>
        @type json
      </parse>
      replace_invalid_sequence true
      emit_invalid_record_to_error false
    </filter>
    
    <filter kubernetes.**>
      @type record_transformer
      <record>
        cluster_name "#{ENV['CLUSTER_NAME']}"
        region "#{ENV['REGION']}"
      </record>
    </filter>
    
    # Send to IBM Log Analysis
    <match kubernetes.**>
      @type logdna
      api_key "#{ENV['LOGDNA_API_KEY']}"
      hostname "#{ENV['HOSTNAME']}"
      app "#{ENV['APP_NAME']}"
      <buffer>
        @type memory
        flush_interval 10s
        chunk_limit_size 5m
        retry_max_times 5
        retry_wait 10s
      </buffer>
    </match>
```

---

## Distributed Tracing

### OpenTelemetry Setup
```javascript
// tracing.js
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { BatchSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');
const { PgInstrumentation } = require('@opentelemetry/instrumentation-pg');
const { RedisInstrumentation } = require('@opentelemetry/instrumentation-redis');

const provider = new NodeTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'api-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: process.env.APP_VERSION,
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV
  })
});

// Jaeger exporter
const jaegerExporter = new JaegerExporter({
  endpoint: process.env.JAEGER_ENDPOINT || 'http://jaeger:14268/api/traces'
});

provider.addSpanProcessor(new BatchSpanProcessor(jaegerExporter));
provider.register();

// Register instrumentations
registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation({
      requestHook: (span, request) => {
        span.setAttribute('http.user_agent', request.headers['user-agent']);
      }
    }),
    new ExpressInstrumentation(),
    new PgInstrumentation(),
    new RedisInstrumentation()
  ]
});

// Get tracer
const tracer = provider.getTracer('api-service');

module.exports = { tracer };
```

### Custom Spans
```javascript
// business-logic.js
const { tracer } = require('./tracing');
const opentelemetry = require('@opentelemetry/api');

async function processOrder(orderId) {
  const span = tracer.startSpan('processOrder');
  span.setAttribute('order.id', orderId);
  span.setAttribute('order.type', 'standard');
  
  try {
    const context = opentelemetry.trace.setSpan(
      opentelemetry.context.active(),
      span
    );
    
    await opentelemetry.context.with(context, async () => {
      // Validate order
      await validateOrder(orderId);
      
      // Process payment
      await processPayment(orderId);
      
      // Update inventory
      await updateInventory(orderId);
      
      // Send notification
      await sendNotification(orderId);
    });
    
    span.setStatus({ code: opentelemetry.SpanStatusCode.OK });
    return { success: true };
    
  } catch (error) {
    span.setStatus({
      code: opentelemetry.SpanStatusCode.ERROR,
      message: error.message
    });
    span.recordException(error);
    throw error;
  } finally {
    span.end();
  }
}

async function validateOrder(orderId) {
  const span = tracer.startSpan('validateOrder', {
    parent: opentelemetry.trace.getActiveSpan()
  });
  
  try {
    // Validation logic
    const order = await db.getOrder(orderId);
    
    if (!order) {
      throw new Error('Order not found');
    }
    
    if (order.total < 0) {
      throw new Error('Invalid order total');
    }
    
    span.addEvent('Order validated', {
      'order.total': order.total,
      'order.items': order.items.length
    });
    
  } finally {
    span.end();
  }
}
```

### Trace Context Propagation
```javascript
// api-client.js
const axios = require('axios');
const opentelemetry = require('@opentelemetry/api');

async function callDownstreamService(url, data) {
  const span = tracer.startSpan('callDownstreamService');
  span.setAttribute('http.url', url);
  
  try {
    // Get current context
    const context = opentelemetry.trace.setSpan(
      opentelemetry.context.active(),
      span
    );
    
    // Inject trace context into headers
    const headers = {};
    opentelemetry.propagation.inject(context, headers);
    
    const response = await axios.post(url, data, { headers });
    
    span.setAttribute('http.status_code', response.status);
    return response.data;
    
  } catch (error) {
    span.recordException(error);
    throw error;
  } finally {
    span.end();
  }
}
```

---

## Alerting and Notifications

### Alert Rules
```yaml
# prometheus-alerts.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-alerts
data:
  alerts.yml: |
    groups:
      - name: application
        interval: 30s
        rules:
          - alert: HighErrorRate
            expr: |
              rate(http_requests_total{status=~"5.."}[5m]) / 
              rate(http_requests_total[5m]) > 0.05
            for: 5m
            labels:
              severity: critical
              team: backend
            annotations:
              summary: "High error rate detected"
              description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.service }}"
          
          - alert: HighLatency
            expr: |
              histogram_quantile(0.95, 
                rate(http_request_duration_seconds_bucket[5m])
              ) > 1
            for: 10m
            labels:
              severity: warning
              team: backend
            annotations:
              summary: "High latency detected"
              description: "P95 latency is {{ $value }}s for {{ $labels.endpoint }}"
          
          - alert: PodCrashLooping
            expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
            for: 5m
            labels:
              severity: critical
              team: platform
            annotations:
              summary: "Pod is crash looping"
              description: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is restarting frequently"
          
          - alert: NodeDiskPressure
            expr: kube_node_status_condition{condition="DiskPressure",status="true"} == 1
            for: 5m
            labels:
              severity: warning
              team: platform
            annotations:
              summary: "Node has disk pressure"
              description: "Node {{ $labels.node }} is experiencing disk pressure"
          
          - alert: DatabaseConnectionPool Exhausted
            expr: database_connection_pool_active / database_connection_pool_max > 0.9
            for: 5m
            labels:
              severity: critical
              team: database
            annotations:
              summary: "Database connection pool nearly exhausted"
              description: "Connection pool is {{ $value | humanizePercentage }} utilized"
```

### PagerDuty Integration
```javascript
// pagerduty.js
const axios = require('axios');

class PagerDutyClient {
  constructor(integrationKey) {
    this.integrationKey = integrationKey;
    this.apiUrl = 'https://events.pagerduty.com/v2/enqueue';
  }
  
  async triggerIncident(summary, details, severity = 'critical') {
    const payload = {
      routing_key: this.integrationKey,
      event_action: 'trigger',
      payload: {
        summary,
        severity,
        source: 'monitoring-system',
        custom_details: details
      }
    };
    
    try {
      const response = await axios.post(this.apiUrl, payload);
      return response.data.dedup_key;
    } catch (error) {
      console.error('Failed to create PagerDuty incident:', error);
      throw error;
    }
  }
  
  async resolveIncident(dedupKey) {
    const payload = {
      routing_key: this.integrationKey,
      event_action: 'resolve',
      dedup_key: dedupKey
    };
    
    await axios.post(this.apiUrl, payload);
  }
  
  async acknowledgeIncident(dedupKey) {
    const payload = {
      routing_key: this.integrationKey,
      event_action: 'acknowledge',
      dedup_key: dedupKey
    };
    
    await axios.post(this.apiUrl, payload);
  }
}

module.exports = PagerDutyClient;
```

### Slack Notifications
```javascript
// slack-notifier.js
const axios = require('axios');

class SlackNotifier {
  constructor(webhookUrl) {
    this.webhookUrl = webhookUrl;
  }
  
  async sendAlert(alert) {
    const color = this.getSeverityColor(alert.severity);
    
    const message = {
      text: `*${alert.severity.toUpperCase()}*: ${alert.summary}`,
      attachments: [{
        color,
        fields: [
          {
            title: 'Description',
            value: alert.description,
            short: false
          },
          {
            title: 'Service',
            value: alert.service,
            short: true
          },
          {
            title: 'Environment',
            value: alert.environment,
            short: true
          },
          {
            title: 'Runbook',
            value: alert.runbookUrl,
            short: false
          }
        ],
        footer: 'Monitoring System',
        ts: Math.floor(Date.now() / 1000)
      }]
    };
    
    try {
      await axios.post(this.webhookUrl, message);
    } catch (error) {
      console.error('Failed to send Slack notification:', error);
    }
  }
  
  getSeverityColor(severity) {
    const colors = {
      critical: '#FF0000',
      warning: '#FFA500',
      info: '#0000FF'
    };
    return colors[severity] || '#808080';
  }
}

module.exports = SlackNotifier;
```

---

## SLIs, SLOs, and SLAs

### Service Level Indicators (SLIs)
```yaml
# sli-definitions.yaml
slis:
  availability:
    description: "Percentage of successful requests"
    query: |
      sum(rate(http_requests_total{status!~"5.."}[30d])) /
      sum(rate(http_requests_total[30d]))
  
  latency:
    description: "95th percentile response time"
    query: |
      histogram_quantile(0.95,
        rate(http_request_duration_seconds_bucket[5m]))
  
  error_rate:
    description: "Percentage of failed requests"
    query: |
      sum(rate(http_requests_total{status=~"5.."}[5m])) /
      sum(rate(http_requests_total[5m]))
  
  throughput:
    description: "Requests per second"
    query: |
      sum(rate(http_requests_total[5m]))
```

### Service Level Objectives (SLOs)
```yaml
# slo-definitions.yaml
slos:
  api_availability:
    sli: availability
    target: 99.9%
    window: 30d
    error_budget: 43m  # 0.1% of 30 days
    
  api_latency:
    sli: latency
    target: 500ms
    percentile: 95
    window: 7d
    
  order_processing_success:
    sli: order_success_rate
    target: 99.5%
    window: 30d
    
  data_freshness:
    sli: data_age
    target: 300s  # 5 minutes
    window: 24h
```

### Error Budget Calculation
```python
# error_budget.py
def calculate_error_budget(slo_target, window_days):
    """
    Calculate error budget based on SLO target
    slo_target: e.g., 0.999 for 99.9%
    window_days: e.g., 30 for 30-day window
    """
    total_minutes = window_days * 24 * 60
    allowed_downtime = total_minutes * (1 - slo_target)
    return allowed_downtime

def error_budget_remaining(actual_availability, slo_target, window_days):
    """
    Calculate remaining error budget
    """
    error_budget = calculate_error_budget(slo_target, window_days)
    total_minutes = window_days * 24 * 60
    actual_downtime = total_minutes * (1 - actual_availability)
    remaining = error_budget - actual_downtime
    
    return {
        'error_budget_minutes': error_budget,
        'consumed_minutes': actual_downtime,
        'remaining_minutes': remaining,
        'percentage_remaining': (remaining / error_budget) * 100
    }

# Example
slo = 0.999  # 99.9%
actual = 0.9985  # 99.85% actual availability
window = 30  # days

result = error_budget_remaining(actual, slo, window)
print(f"Error Budget: {result['error_budget_minutes']:.2f} minutes")
print(f"Consumed: {result['consumed_minutes']:.2f} minutes")
print(f"Remaining: {result['remaining_minutes']:.2f} minutes")
print(f"Percentage Remaining: {result['percentage_remaining']:.2f}%")
```

### SLO Dashboard
```json
{
  "dashboard": {
    "title": "SLO Dashboard",
    "panels": [
      {
        "title": "Availability SLO",
        "type": "gauge",
        "targets": [{
          "expr": "sum(rate(http_requests_total{status!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d]))"
        }],
        "thresholds": [
          { "value": 0.999, "color": "green" },
          { "value": 0.995, "color": "yellow" },
          { "value": 0, "color": "red" }
        ]
      },
      {
        "title": "Error Budget Remaining",
        "type": "graph",
        "targets": [{
          "expr": "1 - ((1 - (sum(rate(http_requests_total{status!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d])))) / (1 - 0.999))"
        }]
      },
      {
        "title": "Latency SLO (P95 < 500ms)",
        "type": "graph",
        "targets": [{
          "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) < 0.5"
        }]
      }
    ]
  }
}
```

### Exam Tips
1. **Monitoring**: Master Sysdig, Prometheus, custom metrics
2. **Logging**: Structured logging, log queries, Fluentd
3. **Tracing**: OpenTelemetry setup, span creation, context propagation
4. **Alerting**: Alert rules, PagerDuty, notification channels
5. **SLOs**: SLI/SLO/SLA definitions, error budget calculations
6. **Dashboards**: Grafana, visualization, business metrics

### Common Scenarios
- Deploy monitoring stack with Prometheus and Grafana
- Implement distributed tracing across microservices
- Create alert rules for Golden Signals
- Calculate error budgets and SLO compliance
- Build comprehensive observability dashboard

## Key terms

- **Four golden signals** - the four metrics to watch for any service: latency, traffic, errors and saturation.
- **Service level indicator (SLI)** - a measured quantity of service behaviour, such as the share of requests that succeed.
- **Service level objective (SLO)** - a target value or range for an SLI over a period of time.
- **Service level agreement (SLA)** - a formal commitment to customers about service levels, usually with consequences if it is missed.
- **Error budget** - the amount of unreliability an SLO allows, calculated as 100% minus the SLO target.
- **OpenTelemetry** - an open source standard and set of tools for generating and collecting traces, metrics and logs.
- **Distributed tracing** - following a single request across services to see where time is spent.
- **IBM Cloud Monitoring** - the IBM Cloud service for collecting metrics and building dashboards and alerts.
