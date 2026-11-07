# IBM Cloud Developer (C1000-177): Cloud-Native Development

## Table of Contents
1. [Cloud-Native Fundamentals](#cloud-native-fundamentals)
2. [IBM Cloud Code Engine](#ibm-cloud-code-engine)
3. [IBM Cloud Functions](#ibm-cloud-functions)
4. [IBM Cloud Kubernetes Service](#ibm-cloud-kubernetes-service)
5. [Red Hat OpenShift on IBM Cloud](#red-hat-openshift-on-ibm-cloud)
6. [Container Development](#container-development)
7. [Microservices Architecture](#microservices-architecture)
8. [API Development](#api-development)
9. [Cloud-Native Design Patterns](#cloud-native-design-patterns)
10. [Exam Tips](#exam-tips)

---

## Cloud-Native Fundamentals

### What is Cloud-Native?

Cloud-native is an approach to building and running applications that exploits the advantages of the cloud computing delivery model. Cloud-native applications are designed specifically to run in cloud environments.

**Key Characteristics:**
- **Microservices architecture**: Decompose applications into small, independent services
- **Containerization**: Package applications with dependencies
- **Dynamic orchestration**: Automated deployment and scaling
- **DevOps integration**: Continuous integration and delivery
- **Resilience**: Design for failure and recovery

### The Twelve-Factor App

Methodology for building software-as-a-service applications:

**1. Codebase**: One codebase tracked in version control, many deploys
```bash
# Single Git repository
git clone https://github.com/myapp/myapp.git
# Multiple deployments (dev, staging, production)
```

**2. Dependencies**: Explicitly declare and isolate dependencies
```json
// package.json example
{
  "dependencies": {
    "express": "^4.18.0",
    "pg": "^8.10.0"
  }
}
```

**3. Config**: Store configuration in the environment
```javascript
// Good practice
const dbHost = process.env.DB_HOST;
const dbPassword = process.env.DB_PASSWORD;

// Avoid hardcoding
// const dbHost = "localhost"; // Bad!
```

**4. Backing Services**: Treat backing services as attached resources
```yaml
# Database as attached resource
services:
  - name: my-postgres
    credentials:
      uri: ${DATABASE_URL}
```

**5. Build, Release, Run**: Strictly separate build and run stages
```bash
# Build stage
npm run build
docker build -t myapp:v1.0 .

# Release stage
docker tag myapp:v1.0 registry.io/myapp:v1.0
docker push registry.io/myapp:v1.0

# Run stage
kubectl apply -f deployment.yaml
```

**6. Processes**: Execute the app as one or more stateless processes
```javascript
// Stateless process - store state externally
app.get('/session', async (req, res) => {
  const session = await redis.get(req.sessionId);
  res.json(session);
});
```

**7. Port Binding**: Export services via port binding
```javascript
const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

**8. Concurrency**: Scale out via the process model
```yaml
# Horizontal scaling
replicas: 10
```

**9. Disposability**: Maximize robustness with fast startup and graceful shutdown
```javascript
// Graceful shutdown
process.on('SIGTERM', () => {
  server.close(() => {
    console.log('Server shutting down gracefully');
    process.exit(0);
  });
});
```

**10. Dev/Prod Parity**: Keep development, staging, and production as similar as possible

**11. Logs**: Treat logs as event streams
```javascript
// Write logs to stdout
console.log('User logged in:', userId);
// Don't manage log files
```

**12. Admin Processes**: Run admin/management tasks as one-off processes
```bash
# Run database migration
kubectl run migrate --image=myapp:v1.0 --command -- npm run migrate
```

### Cloud-Native vs Traditional Applications

```
Traditional:
- Monolithic architecture
- Manual scaling
- Long deployment cycles
- Server-centric
- Pet servers (named, maintained)

Cloud-Native:
- Microservices architecture
- Auto-scaling
- Continuous deployment
- Application-centric
- Cattle servers (disposable, replaceable)
```

---

## IBM Cloud Code Engine

### Overview

Code Engine is a fully managed, serverless platform that runs containerized workloads, including web apps, microservices, event-driven functions, and batch jobs.

**Key Features:**
- **Serverless**: No infrastructure management
- **Auto-scaling**: Scale to zero and up based on demand
- **Pay-per-use**: Charged only when running
- **Container support**: Run any container image
- **Source-to-image**: Build from source code
- **Event-driven**: Trigger on events
- **Private and public endpoints**: Control access

### Code Engine Concepts

**1. Projects**: Isolation boundary for resources
```bash
# Create project
ibmcloud ce project create --name myproject

# Select project
ibmcloud ce project select --name myproject

# List projects
ibmcloud ce project list
```

**2. Applications**: Long-running HTTP services
```yaml
apiVersion: codeengine.cloud.ibm.com/v1beta1
kind: Application
metadata:
  name: myapp
spec:
  image: icr.io/namespace/myapp:latest
  minScale: 0
  maxScale: 10
  port: 8080
  env:
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: api-credentials
          key: apikey
```

**3. Jobs**: Run-to-completion workloads
```bash
# Create job
ibmcloud ce job create --name batch-processor \
  --image icr.io/namespace/batch:v1 \
  --cpu 2 \
  --memory 4G \
  --env-from-secret db-credentials

# Submit job run
ibmcloud ce jobrun submit --job batch-processor \
  --arg input.csv \
  --arg output.json
```

**4. Builds**: Create container images from source
```bash
# Build from source
ibmcloud ce build create --name mybuild \
  --source https://github.com/user/repo \
  --strategy buildpacks \
  --size large

# Run build
ibmcloud ce buildrun submit --build mybuild
```

### Deploying Applications to Code Engine

**From Container Image:**
```bash
# Deploy application
ibmcloud ce application create --name webapp \
  --image us.icr.io/namespace/webapp:v1 \
  --min-scale 1 \
  --max-scale 5 \
  --cpu 0.5 \
  --memory 1G \
  --port 8080 \
  --env DATABASE_URL=postgresql://... \
  --env-from-secret api-keys

# Get application URL
ibmcloud ce application get --name webapp

# Update application
ibmcloud ce application update --name webapp \
  --image us.icr.io/namespace/webapp:v2

# View logs
ibmcloud ce application logs --name webapp --follow
```

**From Source Code:**
```bash
# Deploy from GitHub
ibmcloud ce application create --name myapp \
  --build-source https://github.com/user/myapp \
  --build-strategy buildpacks \
  --build-size large \
  --wait

# Deploy from local directory
ibmcloud ce application create --name localapp \
  --build-source . \
  --build-strategy dockerfile \
  --build-dockerfile Dockerfile
```

### Code Engine Scaling

**Auto-Scaling Configuration:**
```bash
# Configure scaling
ibmcloud ce application update --name myapp \
  --min-scale 0 \
  --max-scale 100 \
  --scale-down-delay 60 \
  --concurrency 100 \
  --cpu 1 \
  --memory 2G

# Scale to zero when idle
--min-scale 0 --scale-down-delay 300
```

**Scaling Metrics:**
- **Concurrency**: Requests per instance
- **CPU**: Processor utilization
- **Memory**: RAM usage
- **Custom metrics**: Via application instrumentation

### Code Engine Event Subscriptions

**Periodic Timer:**
```bash
# Create subscription for scheduled job
ibmcloud ce subscription cron create --name daily-job \
  --destination-type job \
  --destination daily-processor \
  --schedule "0 2 * * *" \
  --data '{"action":"process"}'
```

**Object Storage Events:**
```bash
# Subscribe to COS bucket events
ibmcloud ce subscription cos create --name cos-processor \
  --destination-type app \
  --destination file-processor \
  --bucket my-bucket \
  --event-type write
```

**Kafka/Event Streams:**
```bash
# Subscribe to Kafka topic
ibmcloud ce subscription kafka create --name kafka-consumer \
  --destination-type app \
  --destination message-handler \
  --broker kafka-broker:9092 \
  --topic orders \
  --consumer-group myapp
```

### Code Engine Best Practices

**1. Stateless Design:**
```javascript
// Bad - storing state in memory
let counter = 0;
app.get('/increment', (req, res) => {
  counter++;
  res.json({ counter });
});

// Good - use external state store
app.get('/increment', async (req, res) => {
  const counter = await redis.incr('counter');
  res.json({ counter });
});
```

**2. Fast Startup:**
```javascript
// Initialize quickly
const app = express();
app.listen(PORT);

// Lazy load heavy resources
let model;
app.get('/predict', async (req, res) => {
  if (!model) {
    model = await loadModel();
  }
  const result = model.predict(req.body);
  res.json(result);
});
```

**3. Graceful Shutdown:**
```javascript
process.on('SIGTERM', () => {
  console.log('Shutting down gracefully...');
  server.close(() => {
    // Close database connections
    db.end();
    process.exit(0);
  });
});
```

**4. Health Endpoints:**
```javascript
// Liveness probe
app.get('/healthz', (req, res) => {
  res.status(200).send('OK');
});

// Readiness probe
app.get('/ready', async (req, res) => {
  try {
    await db.ping();
    res.status(200).send('Ready');
  } catch (error) {
    res.status(503).send('Not ready');
  }
});
```

### Code Engine Use Cases

**Web Applications:**
- Single-page applications
- API backends
- Microservices
- Mobile backends

**Event Processing:**
- File processing on upload
- Stream processing
- Webhook handlers
- IoT data processing

**Batch Jobs:**
- Data transformation
- Report generation
- Backup operations
- Machine learning training

**Scheduled Tasks:**
- Cleanup jobs
- Data synchronization
- Report generation
- Monitoring checks

---

## IBM Cloud Functions

> **Legacy service:** IBM publishes migration guidance for moving off IBM Cloud Functions (OpenWhisk); its target is IBM Code Engine ([IBM: How to move from IBM Cloud Functions to IBM Code Engine](https://www.ibm.com/products/tutorials/how-to-move-from-ibm-cloud-functions-to-ibm-code-engine)). Treat the Cloud Functions material below as the legacy model.

### Overview

IBM Cloud Functions is a Function-as-a-Service (FaaS) platform based on Apache OpenWhisk. Execute code in response to events without managing servers.

**Key Features:**
- **Event-driven**: Respond to events automatically
- **Pay-per-execution**: Charged only when code runs
- **Multiple languages**: Node.js, Python, Go, Java, PHP, Ruby, .NET, Swift
- **Sequences**: Chain functions together
- **Triggers and rules**: Event routing
- **Built-in packages**: Pre-built integrations

### Cloud Functions Concepts

**Actions**: Individual functions
```javascript
// hello.js
function main(params) {
  const name = params.name || 'World';
  return { message: `Hello, ${name}!` };
}
```

**Triggers**: Named channels for events
```bash
# Create trigger
ibmcloud fn trigger create myTrigger
```

**Rules**: Connect triggers to actions
```bash
# Create rule
ibmcloud fn rule create myRule myTrigger myAction
```

**Packages**: Group related actions
```bash
# Create package
ibmcloud fn package create myPackage
```

### Creating and Invoking Functions

**Node.js Function:**
```javascript
// async-function.js
async function main(params) {
  const response = await fetch('https://api.example.com/data');
  const data = await response.json();

  return {
    statusCode: 200,
    body: data
  };
}

exports.main = main;
```

```bash
# Create action
ibmcloud fn action create fetchData async-function.js \
  --kind nodejs:18 \
  --web true

# Invoke action
ibmcloud fn action invoke fetchData --result

# Invoke with parameters
ibmcloud fn action invoke fetchData \
  --param url https://api.example.com \
  --result

# Invoke as HTTP request
curl https://us-south.functions.cloud.ibm.com/api/v1/web/namespace/default/fetchData
```

**Python Function:**
```python
# process.py
def main(params):
    data = params.get('data', [])

    # Process data
    result = [item * 2 for item in data]

    return {
        'result': result,
        'count': len(result)
    }
```

```bash
# Create action
ibmcloud fn action create processData process.py \
  --kind python:3.11

# Invoke
ibmcloud fn action invoke processData \
  --param data '[1,2,3,4,5]' \
  --result
```

### Web Actions

Expose functions as HTTP endpoints:

```javascript
// web-action.js
function main(params) {
  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    },
    body: {
      message: 'Hello from web action',
      timestamp: new Date().toISOString()
    }
  };
}
```

```bash
# Create web action
ibmcloud fn action create api web-action.js \
  --web true \
  --web-secure <secret>

# Get web action URL
ibmcloud fn action get api --url

# Access via HTTP
curl https://region.functions.cloud.ibm.com/api/v1/web/namespace/default/api
```

### Sequences

Chain multiple actions together:

```javascript
// validate.js
function main(params) {
  if (!params.email || !params.email.includes('@')) {
    return { error: 'Invalid email' };
  }
  return params;
}

// process.js
function main(params) {
  if (params.error) return params;

  return {
    ...params,
    processed: true,
    timestamp: Date.now()
  };
}

// notify.js
function main(params) {
  if (params.error) {
    return { success: false, error: params.error };
  }

  // Send notification
  return { success: true, message: 'User registered' };
}
```

```bash
# Create actions
ibmcloud fn action create validate validate.js
ibmcloud fn action create process process.js
ibmcloud fn action create notify notify.js

# Create sequence
ibmcloud fn action create registerUser \
  --sequence validate,process,notify

# Invoke sequence
ibmcloud fn action invoke registerUser \
  --param email user@example.com \
  --result
```

### Triggers and Rules

**Manual Trigger:**
```bash
# Create trigger
ibmcloud fn trigger create manualTrigger

# Create rule
ibmcloud fn rule create processRule manualTrigger processData

# Fire trigger
ibmcloud fn trigger fire manualTrigger \
  --param data '[1,2,3]'
```

**Periodic Trigger (Alarm):**
```bash
# Create alarm trigger (every 5 minutes)
ibmcloud fn trigger create periodicJob \
  --feed /whisk.system/alarms/alarm \
  --param cron "*/5 * * * *" \
  --param trigger_payload '{"action":"cleanup"}'

# Connect to action
ibmcloud fn rule create cleanupRule periodicJob cleanupAction
```

### Built-in Packages

**Slack Integration:**
```bash
# Bind Slack package
ibmcloud fn package bind /whisk.system/slack mySlack \
  --param url https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Send message
ibmcloud fn action invoke mySlack/post \
  --param text "Hello from IBM Cloud Functions!" \
  --param channel "#general"
```

**Watson Integration:**
```bash
# Use Watson NLU
ibmcloud fn action invoke /whisk.system/watson-translator/translator \
  --param text "Hello World" \
  --param translateFrom "en" \
  --param translateTo "es" \
  --result
```

### Cloud Functions Limits

```
Timeout: 10 minutes (600 seconds) max
Memory: 2048 MB max
Concurrent executions: 1000 per namespace
Payload size: 1 MB (request/response)
Code size: 48 MB
```

---

## IBM Cloud Kubernetes Service

### Kubernetes Fundamentals

**Core Components:**

**Pods**: Smallest deployable units
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: myapp
    image: us.icr.io/namespace/myapp:v1
    ports:
    - containerPort: 8080
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: url
```

**Deployments**: Manage replica sets
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
      - name: myapp
        image: us.icr.io/namespace/myapp:v1
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

**Services**: Network access to pods
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
```

**ConfigMaps**: Configuration data
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    api.url=https://api.example.com
    max.connections=100
  log.level: "INFO"
```

**Secrets**: Sensitive data
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:
  username: admin
  password: secret123
  url: postgresql://db.example.com:5432/mydb
```

### Creating IKS Clusters

**VPC Cluster:**
```bash
# Create VPC cluster
ibmcloud ks cluster create vpc-gen2 \
  --name production-cluster \
  --zone us-south-1 \
  --version 1.28 \
  --flavor bx2.4x16 \
  --workers 3 \
  --vpc-id <vpc-id> \
  --subnet-id <subnet-id> \
  --cos-instance <cos-instance-id>

# Wait for cluster to be ready
ibmcloud ks cluster get --cluster production-cluster

# Download cluster config
ibmcloud ks cluster config --cluster production-cluster

# Verify access
kubectl get nodes
kubectl cluster-info
```

**Multi-Zone Cluster:**
```bash
# Create cluster in multiple zones
ibmcloud ks cluster create vpc-gen2 \
  --name ha-cluster \
  --zone us-south-1 \
  --zone us-south-2 \
  --zone us-south-3 \
  --version 1.28 \
  --flavor bx2.4x16 \
  --workers 2 \
  --vpc-id <vpc-id> \
  --subnet-id <subnet-1-id> \
  --subnet-id <subnet-2-id> \
  --subnet-id <subnet-3-id>
```

### Deploying Applications

**Complete Deployment Example:**
```bash
# Create namespace
kubectl create namespace myapp

# Create secret
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secret \
  --namespace=myapp

# Create configmap
kubectl create configmap app-config \
  --from-file=config.yaml \
  --namespace=myapp

# Apply deployment
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
      - name: myapp
        image: us.icr.io/namespace/myapp:v1
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_USERNAME
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: username
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
        volumeMounts:
        - name: config
          mountPath: /etc/config
      volumes:
      - name: config
        configMap:
          name: app-config
---
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: myapp
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
EOF

# Check status
kubectl get all -n myapp

# Get service URL
kubectl get service myapp -n myapp
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
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
        averageUtilization: 80
```

```bash
# Apply HPA
kubectl apply -f hpa.yaml

# Watch scaling
kubectl get hpa -n myapp --watch
```

### Persistent Storage

**Using IBM Cloud Block Storage:**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-pvc
  namespace: myapp
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
  storageClassName: ibmc-vpc-block-10iops-tier
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database
  namespace: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
      - name: postgres
        image: postgres:15
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: myapp-pvc
```

---

## Red Hat OpenShift on IBM Cloud

### OpenShift vs Kubernetes

**OpenShift Additions:**
- **Routes**: Built-in ingress with SSL
- **ImageStreams**: Track image changes
- **BuildConfigs**: Integrated CI/CD
- **DeploymentConfigs**: Enhanced deployments
- **Projects**: Namespace with additional features
- **Web Console**: Enhanced UI
- **Operators**: Automated operations
- **Security**: Security Context Constraints (SCCs)

### Creating OpenShift Cluster

```bash
# Create OpenShift cluster
ibmcloud oc cluster create vpc-gen2 \
  --name openshift-cluster \
  --zone us-south-1 \
  --version 4.13_openshift \
  --flavor bx2.16x64 \
  --workers 3 \
  --vpc-id <vpc-id> \
  --subnet-id <subnet-id>

# Get cluster config
ibmcloud oc cluster config --cluster openshift-cluster --admin

# Login to OpenShift
oc login --token=<token> --server=<server-url>
```

### OpenShift Projects

```bash
# Create project
oc new-project myapp \
  --display-name="My Application" \
  --description="Production application"

# Switch project
oc project myapp

# View project
oc describe project myapp
```

### Source-to-Image (S2I)

Deploy directly from source code:

```bash
# Deploy from GitHub
oc new-app nodejs~https://github.com/user/nodeapp.git \
  --name=myapp \
  --env DATABASE_URL=postgresql://...

# Create route
oc expose service myapp

# Get route URL
oc get route myapp

# Watch build
oc logs -f bc/myapp

# Trigger new build
oc start-build myapp
```

### OpenShift Routes

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: myapp
  namespace: myapp
spec:
  host: myapp.apps.cluster.example.com
  to:
    kind: Service
    name: myapp
  port:
    targetPort: 8080
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
```

```bash
# Create route
oc create route edge myapp \
  --service=myapp \
  --hostname=myapp.example.com

# Create route with custom certificate
oc create route edge myapp \
  --service=myapp \
  --cert=cert.pem \
  --key=key.pem \
  --ca-cert=ca.pem
```

### OpenShift Operators

```bash
# Install operator via OperatorHub
oc apply -f - <<EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: mongodb-operator
  namespace: openshift-operators
spec:
  channel: stable
  name: mongodb-atlas-kubernetes
  source: operatorhubio-catalog
  sourceNamespace: olm
EOF

# Create MongoDB cluster using operator
oc apply -f - <<EOF
apiVersion: mongodb.com/v1
kind: MongoDBCommunity
metadata:
  name: mongodb
spec:
  members: 3
  type: ReplicaSet
  version: "6.0.0"
EOF
```

---

## Container Development

### Dockerfile Best Practices

**Multi-Stage Build:**
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package*.json ./

# Security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

EXPOSE 8080
CMD ["node", "dist/server.js"]
```

**Optimized Layer Caching:**
```dockerfile
FROM python:3.11-slim

# Install dependencies first (changes less frequently)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (changes more frequently)
COPY app/ /app/
WORKDIR /app

CMD ["python", "server.py"]
```

### Health Checks

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node healthcheck.js || exit 1

CMD ["node", "server.js"]
```

```javascript
// healthcheck.js
const http = require('http');

const options = {
  host: 'localhost',
  port: 8080,
  path: '/healthz',
  timeout: 2000
};

http.get(options, (res) => {
  if (res.statusCode === 200) {
    process.exit(0);
  } else {
    process.exit(1);
  }
}).on('error', (err) => {
  process.exit(1);
});
```

---

## Microservices Architecture

### Design Principles

**1. Single Responsibility**: Each service does one thing well
**2. Loose Coupling**: Minimize dependencies between services
**3. High Cohesion**: Related functionality together
**4. Autonomy**: Independent deployment and scaling
**5. Resilience**: Design for failure

### Service Communication

**Synchronous (REST):**
```javascript
// Service A calling Service B
const axios = require('axios');

async function getUserProfile(userId) {
  try {
    const response = await axios.get(
      `http://user-service:8080/users/${userId}`,
      { timeout: 5000 }
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    // Fallback or circuit breaker
    return null;
  }
}
```

**Asynchronous (Message Queue):**
```javascript
// Producer
const kafka = require('kafka-node');

async function publishOrder(order) {
  const producer = new kafka.Producer(client);
  const message = JSON.stringify(order);

  producer.send([{
    topic: 'orders',
    messages: [message]
  }], (err, data) => {
    if (err) console.error(err);
  });
}

// Consumer
const consumer = new kafka.Consumer(
  client,
  [{ topic: 'orders', partition: 0 }],
  { autoCommit: true }
);

consumer.on('message', async (message) => {
  const order = JSON.parse(message.value);
  await processOrder(order);
});
```

### Circuit Breaker Pattern

```javascript
const circuitBreaker = require('opossum');

// Create circuit breaker
const options = {
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000
};

function callExternalService(data) {
  return axios.post('http://external-service/api', data);
}

const breaker = new circuitBreaker(callExternalService, options);

// Use circuit breaker
breaker.fire(data)
  .then(result => console.log(result))
  .catch(err => console.error('Circuit breaker opened:', err));

// Monitor circuit breaker
breaker.on('open', () => console.log('Circuit opened'));
breaker.on('halfOpen', () => console.log('Circuit half-open'));
breaker.on('close', () => console.log('Circuit closed'));
```

---

## API Development

### REST API Best Practices

**Resource Naming:**
```
GET    /api/v1/users           # List users
GET    /api/v1/users/:id       # Get user
POST   /api/v1/users           # Create user
PUT    /api/v1/users/:id       # Update user
PATCH  /api/v1/users/:id       # Partial update
DELETE /api/v1/users/:id       # Delete user
```

**Express.js API Example:**
```javascript
const express = require('express');
const app = express();

app.use(express.json());

// Versioning
const v1Router = express.Router();

// CRUD endpoints
v1Router.get('/users', async (req, res) => {
  const users = await db.getUsers();
  res.json({ data: users });
});

v1Router.post('/users', async (req, res) => {
  const user = await db.createUser(req.body);
  res.status(201).json({ data: user });
});

app.use('/api/v1', v1Router);

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: {
      message: 'Internal server error',
      code: 'INTERNAL_ERROR'
    }
  });
});

app.listen(8080);
```

---

## Cloud-Native Design Patterns

### Retry Pattern
### Bulkhead Pattern
### Service Mesh
### API Gateway Pattern

---

## Exam Tips

### Key Concepts
- Understand Code Engine vs Functions vs Kubernetes
- Know when to use each platform
- Familiar with container development
- Kubernetes fundamentals (pods, deployments, services)
- OpenShift additional features
- Microservices patterns
- API development best practices

### Sample Questions

**Q1:** What is the main difference between Code Engine applications and jobs?
- A) Applications run once, jobs run continuously
- **B) Applications are long-running HTTP services, jobs are run-to-completion tasks** ✓
- C) No difference
- D) Applications use more CPU

**Q2:** What is the maximum timeout for Cloud Functions?
- A) 1 minute
- B) 5 minutes
- **C) 10 minutes** ✓
- D) 30 minutes

**Q3:** In Kubernetes, what is the purpose of a Service?
- A) Store application data
- **B) Provide network access to a set of pods** ✓
- C) Scale pods automatically
- D) Build container images

---

Success in the IBM Cloud Developer exam requires strong hands-on experience with Code Engine, Kubernetes, and container development. Practice building and deploying applications using different platforms to understand their strengths and use cases.
