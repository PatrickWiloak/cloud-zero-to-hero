# IBM Cloud Developer (C1000-177) - Application Deployment & Integration

## Table of Contents
- [CI/CD Pipelines](#cicd-pipelines)
- [IBM Cloud Toolchains](#ibm-cloud-toolchains)
- [Container Orchestration](#container-orchestration)
- [Serverless Deployment](#serverless-deployment)
- [Application Integration](#application-integration)
- [Messaging Services](#messaging-services)
- [Event-Driven Architecture](#event-driven-architecture)
- [API Management](#api-management)
- [DevOps Best Practices](#devops-best-practices)

---

## CI/CD Pipelines

### IBM Cloud Continuous Delivery

IBM Cloud Continuous Delivery provides integrated DevOps tools for building, testing, and deploying applications.

#### Key Components

1. **Delivery Pipeline**
   - Build stage
   - Test stage
   - Deploy stage
   - Custom stages

2. **Pipeline Types**
   - Classic pipelines
   - Tekton pipelines (preferred)
   - Jenkins integration

3. **Pipeline Triggers**
   - Git commit
   - Pull request
   - Manual trigger
   - Timer-based

#### Creating a Tekton Pipeline

```yaml
# .tekton/pipeline.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: ibm-cloud-app-pipeline
spec:
  params:
    - name: repository
      description: The git repo URL
    - name: revision
      description: The git revision
      default: main
    - name: registry-namespace
      description: Container registry namespace
    - name: image-name
      description: Image name

  workspaces:
    - name: pipeline-workspace

  tasks:
    - name: git-clone
      taskRef:
        name: git-clone
      params:
        - name: url
          value: $(params.repository)
        - name: revision
          value: $(params.revision)
      workspaces:
        - name: output
          workspace: pipeline-workspace

    - name: unit-tests
      taskRef:
        name: npm-test
      runAfter:
        - git-clone
      workspaces:
        - name: source
          workspace: pipeline-workspace

    - name: build-image
      taskRef:
        name: icr-containerize
      runAfter:
        - unit-tests
      params:
        - name: registry-namespace
          value: $(params.registry-namespace)
        - name: image-name
          value: $(params.image-name)
        - name: path-to-dockerfile
          value: Dockerfile
      workspaces:
        - name: source
          workspace: pipeline-workspace

    - name: vulnerability-scan
      taskRef:
        name: icr-check-va-scan
      runAfter:
        - build-image
      params:
        - name: registry-namespace
          value: $(params.registry-namespace)
        - name: image-name
          value: $(params.image-name)

    - name: deploy-to-kubernetes
      taskRef:
        name: kubernetes-deploy
      runAfter:
        - vulnerability-scan
      params:
        - name: cluster-name
          value: my-iks-cluster
        - name: deployment-file
          value: deployment.yaml
      workspaces:
        - name: source
          workspace: pipeline-workspace
```

#### Tekton Task Definition

```yaml
# .tekton/tasks/npm-test.yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: npm-test
spec:
  workspaces:
    - name: source

  steps:
    - name: install-dependencies
      image: node:16
      workingDir: $(workspaces.source.path)
      script: |
        #!/bin/bash
        npm ci

    - name: run-tests
      image: node:16
      workingDir: $(workspaces.source.path)
      script: |
        #!/bin/bash
        npm test -- --coverage

    - name: run-linter
      image: node:16
      workingDir: $(workspaces.source.path)
      script: |
        #!/bin/bash
        npm run lint
```

#### Creating Pipeline via CLI

```bash
# Install IBM Cloud CLI plugins
ibmcloud plugin install doi
ibmcloud plugin install kubernetes-service

# Create a toolchain
ibmcloud dev toolchain-create --name my-toolchain

# Get toolchain ID
TOOLCHAIN_ID=$(ibmcloud dev toolchain-get my-toolchain --output json | jq -r '.id')

# Create a pipeline
ibmcloud dev pipeline-create \
  --toolchain-id $TOOLCHAIN_ID \
  --name my-pipeline \
  --type tekton

# Create pipeline run
ibmcloud dev pipeline-run \
  --pipeline-id <pipeline-id> \
  --trigger manual
```

### Classic Pipeline Configuration

```yaml
# .bluemix/pipeline.yml
stages:
  - name: BUILD
    inputs:
      - type: git
        branch: main
    triggers:
      - type: commit
    jobs:
      - name: Build
        type: builder
        build_type: shell
        script: |
          #!/bin/bash
          npm install
          npm run build

  - name: TEST
    inputs:
      - type: job
        stage: BUILD
        job: Build
    jobs:
      - name: Unit Tests
        type: tester
        script: |
          #!/bin/bash
          npm test
      - name: Security Scan
        type: tester
        script: |
          #!/bin/bash
          npm audit

  - name: DEPLOY
    inputs:
      - type: job
        stage: BUILD
        job: Build
    triggers:
      - type: stage
    jobs:
      - name: Deploy to Cloud Foundry
        type: deployer
        target:
          region_id: us-south
          organization: my-org
          space: production
        script: |
          #!/bin/bash
          cf push "${CF_APP_NAME}"
```

### Pipeline Environment Variables

```bash
# Set environment variables for pipeline
ibmcloud dev pipeline-property-set \
  --pipeline-id <pipeline-id> \
  --name API_KEY \
  --value $IBM_CLOUD_API_KEY \
  --type secure

ibmcloud dev pipeline-property-set \
  --pipeline-id <pipeline-id> \
  --name REGION \
  --value us-south \
  --type text
```

---

## IBM Cloud Toolchains

### Toolchain Components

1. **Source Control**
   - GitHub
   - GitLab
   - Bitbucket
   - IBM Cloud Git Repos

2. **Build & Deploy**
   - Delivery Pipeline
   - Tekton
   - Jenkins

3. **Testing**
   - Sauce Labs
   - DevOps Insights
   - Custom test tools

4. **Monitoring**
   - PagerDuty
   - Slack
   - IBM Cloud Monitoring

#### Creating a Toolchain

```bash
# Create toolchain from template
ibmcloud dev toolchain-create \
  --name my-complete-toolchain \
  --template "Cloud Native Toolchain"

# Add GitHub integration
ibmcloud dev toolchain-integration-add \
  --toolchain-id $TOOLCHAIN_ID \
  --type githubconsolidated \
  --name my-github \
  --parameters '{
    "repo_url": "https://github.com/myorg/myapp",
    "type": "existing",
    "api_token": "$GITHUB_TOKEN"
  }'

# Add Slack integration
ibmcloud dev toolchain-integration-add \
  --toolchain-id $TOOLCHAIN_ID \
  --type slack \
  --name my-slack \
  --parameters '{
    "api_token": "$SLACK_TOKEN",
    "channel_name": "deployments"
  }'
```

#### Toolchain Template (JSON)

```json
{
  "name": "My Application Toolchain",
  "description": "Complete CI/CD toolchain for Node.js application",
  "required": [
    "repo",
    "pipeline"
  ],
  "services": {
    "repo": {
      "service_id": "githubconsolidated",
      "parameters": {
        "repo_name": "{{toolchain.name}}",
        "repo_url": "https://github.com/myorg/myapp",
        "type": "clone",
        "has_issues": true,
        "enable_traceability": true
      }
    },
    "pipeline": {
      "service_id": "pipeline",
      "parameters": {
        "services": [
          "repo"
        ],
        "name": "{{services.repo.parameters.repo_name}}",
        "type": "tekton",
        "configuration": {
          "content": {
            "$text": "pipeline.yml"
          },
          "env": {
            "REPO": "repo",
            "CF_APP_NAME": "{{form.pipeline.parameters.app-name}}",
            "REGISTRY_NAMESPACE": "{{form.pipeline.parameters.registry-namespace}}",
            "API_KEY": "{{form.pipeline.parameters.api-key}}"
          }
        }
      }
    },
    "devops-insights": {
      "service_id": "draservicebroker"
    },
    "slack": {
      "service_id": "slack",
      "parameters": {
        "api_token": "{{form.slack.parameters.api_token}}",
        "channel_name": "{{form.slack.parameters.channel_name}}"
      }
    }
  }
}
```

### DevOps Insights Integration

```bash
# Install DevOps Insights CLI
npm install -g grunt-idra3

# Publish test results
grunt idra:publishTestResult \
  --file=mocha.json \
  --type=unittest

# Publish code coverage
grunt idra:publishTestResult \
  --file=coverage/coverage.json \
  --type=code

# Publish build record
grunt idra:publishBuildRecord \
  --status=pass \
  --logicalappname="MyApp" \
  --buildnumber=$BUILD_NUMBER

# Evaluate gate policy
grunt idra:evaluateGate \
  --policy="Unit Test Policy" \
  --ruletype=unittest
```

---

## Container Orchestration

### Kubernetes Deployments

#### Deployment Manifest

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  namespace: production
  labels:
    app: myapp
    version: v1
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
        image: us.icr.io/mynamespace/myapp:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
          protocol: TCP
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
      imagePullSecrets:
      - name: icr-secret
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: production
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: "public-iks-k8s-nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls-secret
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

#### Kubernetes CLI Commands

```bash
# Configure kubectl for IKS
ibmcloud ks cluster config --cluster my-cluster

# Create namespace
kubectl create namespace production

# Create image pull secret for IBM Container Registry
kubectl create secret docker-registry icr-secret \
  --docker-server=us.icr.io \
  --docker-username=iamapikey \
  --docker-password=$IBM_CLOUD_API_KEY \
  --namespace=production

# Create secret for database credentials
kubectl create secret generic db-credentials \
  --from-literal=url="postgresql://user:pass@host:5432/db" \
  --namespace=production

# Apply deployment
kubectl apply -f deployment.yaml

# Check deployment status
kubectl rollout status deployment/myapp-deployment -n production

# Scale deployment
kubectl scale deployment/myapp-deployment --replicas=5 -n production

# Update image
kubectl set image deployment/myapp-deployment \
  myapp=us.icr.io/mynamespace/myapp:v2 \
  -n production

# Rollback deployment
kubectl rollout undo deployment/myapp-deployment -n production

# View logs
kubectl logs -f deployment/myapp-deployment -n production

# Execute command in pod
kubectl exec -it deployment/myapp-deployment -n production -- /bin/sh
```

### OpenShift Deployments

#### DeploymentConfig

```yaml
# openshift-deployment.yaml
apiVersion: apps.openshift.io/v1
kind: DeploymentConfig
metadata:
  name: myapp
  namespace: myproject
spec:
  replicas: 3
  selector:
    app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: us.icr.io/mynamespace/myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: NODE_ENV
          value: production
  triggers:
  - type: ConfigChange
  - type: ImageChange
    imageChangeParams:
      automatic: true
      containerNames:
      - myapp
      from:
        kind: ImageStreamTag
        name: myapp:latest
---
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: myapp
spec:
  to:
    kind: Service
    name: myapp
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
```

#### OpenShift CLI Commands

```bash
# Login to OpenShift cluster
oc login --token=$OC_TOKEN --server=https://api.myopenshift.com:6443

# Create new project
oc new-project myproject

# Create app from source code
oc new-app nodejs~https://github.com/myorg/myapp \
  --name=myapp \
  --env NODE_ENV=production

# Create app from Docker image
oc new-app us.icr.io/mynamespace/myapp:latest \
  --name=myapp

# Expose service
oc expose service myapp \
  --hostname=myapp.apps.myopenshift.com

# Start build
oc start-build myapp

# Follow build logs
oc logs -f bc/myapp

# Scale application
oc scale dc/myapp --replicas=5

# Set environment variable
oc set env dc/myapp DATABASE_URL="postgresql://..."

# Create secret
oc create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=secret

# Mount secret as environment
oc set env dc/myapp --from=secret/db-secret

# Rollout latest version
oc rollout latest dc/myapp

# Check rollout status
oc rollout status dc/myapp

# Rollback to previous version
oc rollback myapp
```

### Helm Charts

```yaml
# Chart.yaml
apiVersion: v2
name: myapp
description: My Application Helm Chart
type: application
version: 1.0.0
appVersion: "1.0"

---
# values.yaml
replicaCount: 3

image:
  repository: us.icr.io/mynamespace/myapp
  tag: latest
  pullPolicy: Always

service:
  type: LoadBalancer
  port: 80
  targetPort: 8080

ingress:
  enabled: true
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

env:
  - name: NODE_ENV
    value: "production"

secrets:
  - name: DATABASE_URL
    key: url

---
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: {{ .Values.service.targetPort }}
        env:
        {{- range .Values.env }}
        - name: {{ .name }}
          value: {{ .value | quote }}
        {{- end }}
        {{- range .Values.secrets }}
        - name: {{ .name }}
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: {{ .key }}
        {{- end }}
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
```

```bash
# Install Helm chart
helm install myapp ./myapp-chart \
  --namespace production \
  --create-namespace

# Upgrade release
helm upgrade myapp ./myapp-chart \
  --namespace production \
  --set image.tag=v2

# Rollback release
helm rollback myapp 1 --namespace production

# Uninstall release
helm uninstall myapp --namespace production
```

---

## Serverless Deployment

### IBM Cloud Functions (OpenWhisk)

> **Legacy service:** IBM publishes migration guidance for moving off IBM Cloud Functions (OpenWhisk); its target is IBM Code Engine ([IBM: How to move from IBM Cloud Functions to IBM Code Engine](https://www.ibm.com/products/tutorials/how-to-move-from-ibm-cloud-functions-to-ibm-code-engine)). Treat the Cloud Functions material below as the legacy model.

#### Action Deployment

```javascript
// hello.js
function main(params) {
  const name = params.name || 'World';
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: { message: `Hello, ${name}!` }
  };
}

exports.main = main;
```

```bash
# Create action
ibmcloud fn action create hello hello.js \
  --kind nodejs:16 \
  --web true

# Invoke action
ibmcloud fn action invoke hello \
  --param name "IBM Cloud" \
  --result

# Get action URL
ibmcloud fn action get hello --url

# Update action
ibmcloud fn action update hello hello.js

# Create action with dependencies
zip -r action.zip hello.js package.json node_modules
ibmcloud fn action create hello action.zip \
  --kind nodejs:16 \
  --web true

# Set default parameters
ibmcloud fn action update hello \
  --param apiKey $API_KEY

# Create Docker action
ibmcloud fn action create myaction --docker myimage:latest
```

#### Sequence Actions

```bash
# Create individual actions
ibmcloud fn action create auth auth.js
ibmcloud fn action create process process.js
ibmcloud fn action create respond respond.js

# Create sequence
ibmcloud fn action create processRequest \
  --sequence auth,process,respond

# Invoke sequence
ibmcloud fn action invoke processRequest \
  --param token "abc123" \
  --param data "mydata" \
  --result
```

#### Triggers and Rules

```bash
# Create trigger
ibmcloud fn trigger create myTrigger

# Fire trigger
ibmcloud fn trigger fire myTrigger \
  --param message "Hello"

# Create rule to connect trigger to action
ibmcloud fn rule create myRule myTrigger hello

# Create periodic trigger
ibmcloud fn trigger create everyMinute \
  --feed /whisk.system/alarms/alarm \
  --param cron "* * * * *"

# Create Cloudant trigger
ibmcloud fn trigger create dbTrigger \
  --feed /whisk.system/cloudant/changes \
  --param dbname mydb \
  --param username $USERNAME \
  --param password $PASSWORD
```

#### API Gateway

```bash
# Create API
ibmcloud fn api create /api /hello get hello \
  --response-type json

# List APIs
ibmcloud fn api list

# Get API details
ibmcloud fn api get /api

# Delete API
ibmcloud fn api delete /api
```

### Code Engine

#### Application Deployment

```bash
# Create project
ibmcloud ce project create --name my-project

# Select project
ibmcloud ce project select --name my-project

# Deploy application from container image
ibmcloud ce application create \
  --name myapp \
  --image us.icr.io/mynamespace/myapp:latest \
  --port 8080 \
  --min-scale 0 \
  --max-scale 10 \
  --cpu 0.5 \
  --memory 1G \
  --env NODE_ENV=production \
  --registry-secret myregistry

# Deploy from source code
ibmcloud ce application create \
  --name myapp \
  --build-source . \
  --strategy buildpacks \
  --port 8080

# Update application
ibmcloud ce application update myapp \
  --image us.icr.io/mynamespace/myapp:v2 \
  --env-from-secret db-credentials

# Scale application
ibmcloud ce application update myapp \
  --min-scale 2 \
  --max-scale 20 \
  --concurrency 100

# Get application URL
ibmcloud ce application get --name myapp

# View logs
ibmcloud ce application logs --name myapp --follow
```

#### Batch Jobs

```bash
# Create job
ibmcloud ce job create \
  --name data-processing \
  --image us.icr.io/mynamespace/processor:latest \
  --cpu 2 \
  --memory 4G \
  --array-indices 0-9

# Run job
ibmcloud ce jobrun submit \
  --job data-processing \
  --env INPUT_FILE=data.csv

# Check job status
ibmcloud ce jobrun get --name data-processing-run-1

# View job logs
ibmcloud ce jobrun logs --name data-processing-run-1
```

---

## Application Integration

### App Connect

#### Integration Flow

```json
{
  "name": "Salesforce to Slack Integration",
  "description": "Send Slack notification when new lead is created",
  "trigger": {
    "type": "salesforce",
    "event": "Lead Created",
    "connection": "salesforce-prod",
    "fields": [
      "Id",
      "FirstName",
      "LastName",
      "Email",
      "Company"
    ]
  },
  "actions": [
    {
      "type": "slack",
      "action": "Send Message",
      "connection": "slack-sales",
      "parameters": {
        "channel": "#new-leads",
        "message": "New lead: {{FirstName}} {{LastName}} from {{Company}}"
      }
    },
    {
      "type": "cloudant",
      "action": "Create Document",
      "connection": "cloudant-db",
      "parameters": {
        "database": "leads",
        "document": {
          "salesforceId": "{{Id}}",
          "name": "{{FirstName}} {{LastName}}",
          "email": "{{Email}}",
          "company": "{{Company}}",
          "timestamp": "{{$now}}"
        }
      }
    }
  ]
}
```

### IBM MQ Integration

```javascript
// mq-producer.js
const mq = require('ibmmq');

const connectionOptions = {
  queueManager: 'QM1',
  host: 'mq.example.com',
  port: 1414,
  channel: 'DEV.ADMIN.SVRCONN',
  userId: 'admin',
  password: process.env.MQ_PASSWORD
};

async function sendMessage(message) {
  const mqConn = new mq.MQQueueManager();

  try {
    await mqConn.connect(connectionOptions);

    const queue = await mqConn.openQueue(
      'DEV.QUEUE.1',
      mq.MQC.MQOO_OUTPUT
    );

    const msgObject = {
      type: mq.MQC.MQMT_DATAGRAM,
      format: mq.MQC.MQFMT_STRING,
      messageData: message
    };

    await queue.put(msgObject);
    await queue.close();
    await mqConn.disconnect();

    console.log('Message sent successfully');
  } catch (err) {
    console.error('Error:', err);
  }
}

sendMessage('Hello from IBM Cloud!');
```

---

## Messaging Services

### Event Streams (Kafka)

#### Producer

```javascript
// kafka-producer.js
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: process.env.KAFKA_BROKERS.split(','),
  ssl: true,
  sasl: {
    mechanism: 'plain',
    username: 'token',
    password: process.env.KAFKA_API_KEY
  }
});

const producer = kafka.producer();

async function sendMessage(topic, message) {
  await producer.connect();

  await producer.send({
    topic: topic,
    messages: [
      {
        key: message.key,
        value: JSON.stringify(message.value),
        headers: {
          'correlation-id': message.correlationId
        }
      }
    ]
  });

  await producer.disconnect();
}

// Usage
sendMessage('orders', {
  key: 'order-123',
  value: {
    orderId: '123',
    customer: 'John Doe',
    amount: 99.99,
    timestamp: new Date().toISOString()
  },
  correlationId: 'abc-123'
});
```

#### Consumer

```javascript
// kafka-consumer.js
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: process.env.KAFKA_BROKERS.split(','),
  ssl: true,
  sasl: {
    mechanism: 'plain',
    username: 'token',
    password: process.env.KAFKA_API_KEY
  }
});

const consumer = kafka.consumer({
  groupId: 'order-processor',
  sessionTimeout: 30000
});

async function consumeMessages() {
  await consumer.connect();
  await consumer.subscribe({
    topic: 'orders',
    fromBeginning: false
  });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const order = JSON.parse(message.value.toString());

      console.log({
        topic,
        partition,
        offset: message.offset,
        key: message.key?.toString(),
        order
      });

      // Process order
      await processOrder(order);
    }
  });
}

async function processOrder(order) {
  // Business logic here
  console.log(`Processing order ${order.orderId}`);
}

consumeMessages().catch(console.error);
```

#### Managing Topics

```bash
# Create topic
ibmcloud es topic-create orders \
  --partitions 3 \
  --replication-factor 3

# List topics
ibmcloud es topics

# Update topic configuration
ibmcloud es topic-update orders \
  --config retention.ms=86400000

# Delete topic
ibmcloud es topic-delete orders
```

---

## Event-Driven Architecture

### Event Notifications

```bash
# Create Event Notifications instance
ibmcloud resource service-instance-create \
  my-event-notifications \
  event-notifications \
  standard \
  us-south

# Create topic
ibmcloud event-notifications topic-create \
  --instance-id $INSTANCE_ID \
  --name "order-events" \
  --description "Order processing events"

# Create destination (webhook)
ibmcloud event-notifications destination-create \
  --instance-id $INSTANCE_ID \
  --name "order-webhook" \
  --type webhook \
  --config '{
    "url": "https://myapp.com/webhook",
    "verb": "POST",
    "headers": {
      "Authorization": "Bearer token"
    }
  }'

# Create subscription
ibmcloud event-notifications subscription-create \
  --instance-id $INSTANCE_ID \
  --name "order-subscription" \
  --destination-id $DEST_ID \
  --topic-id $TOPIC_ID
```

### Event Notifications SDK

```javascript
// event-notifications.js
const EventNotificationsV1 = require('@ibm-cloud/event-notifications-node-admin-sdk');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const authenticator = new IamAuthenticator({
  apikey: process.env.EN_API_KEY
});

const eventNotifications = new EventNotificationsV1({
  authenticator,
  serviceUrl: 'https://us-south.event-notifications.cloud.ibm.com'
});

// Send notification
async function sendNotification(instanceId, event) {
  const params = {
    instanceId,
    body: {
      specversion: '1.0',
      id: event.id,
      source: 'myapp',
      type: 'order.created',
      time: new Date().toISOString(),
      data: event.data
    }
  };

  try {
    const response = await eventNotifications.sendNotifications(params);
    console.log('Notification sent:', response.result);
  } catch (err) {
    console.error('Error sending notification:', err);
  }
}

// Usage
sendNotification(process.env.EN_INSTANCE_ID, {
  id: 'order-123',
  data: {
    orderId: '123',
    customer: 'John Doe',
    amount: 99.99,
    status: 'created'
  }
});
```

---

## API Management

### API Connect

#### API Definition (OpenAPI)

```yaml
# api-definition.yaml
openapi: 3.0.0
info:
  title: Orders API
  version: 1.0.0
  description: API for managing orders

servers:
  - url: https://api.example.com/v1

security:
  - ApiKeyAuth: []

paths:
  /orders:
    get:
      summary: List all orders
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  orders:
                    type: array
                    items:
                      $ref: '#/components/schemas/Order'
                  total:
                    type: integer

    post:
      summary: Create a new order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderInput'
      responses:
        '201':
          description: Order created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'

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
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '404':
          description: Order not found

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key

  schemas:
    Order:
      type: object
      properties:
        id:
          type: string
        customerId:
          type: string
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'
        totalAmount:
          type: number
        status:
          type: string
          enum: [pending, processing, completed, cancelled]
        createdAt:
          type: string
          format: date-time

    OrderInput:
      type: object
      required:
        - customerId
        - items
      properties:
        customerId:
          type: string
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'

    OrderItem:
      type: object
      properties:
        productId:
          type: string
        quantity:
          type: integer
        price:
          type: number
```

#### API Policies

```yaml
# policies.yaml
assembly:
  execute:
    - set-variable:
        title: Set CORS Headers
        actions:
          - set: message.headers.Access-Control-Allow-Origin
            value: '*'
          - set: message.headers.Access-Control-Allow-Methods
            value: 'GET, POST, PUT, DELETE, OPTIONS'

    - rate-limit:
        title: Rate Limiting
        rate-limit:
          value: 100
          interval: 60
          time-unit: second
          key: $(request.headers.X-API-Key)

    - validate:
        title: Validate Request
        source: request
        definition: '#/definitions/OrderInput'

    - invoke:
        title: Call Backend
        target-url: $(backend-url)/orders$(request.path)
        verb: $(request.verb)
        cache-response: time-to-live
        cache-ttl: 300

    - map:
        title: Transform Response
        inputs:
          input:
            schema: '#/definitions/BackendResponse'
            variable: message.body
        outputs:
          output:
            schema: '#/definitions/Order'
            variable: message.body
        actions:
          - set: output.id
            from: input.orderId
          - set: output.status
            from: input.orderStatus

    - log:
        title: Log Transaction
        content: 'auto'
        error-content: 'payload'
```

---

## DevOps Best Practices

### Blue-Green Deployment

```bash
# Deploy blue version
kubectl apply -f blue-deployment.yaml

# Test blue version
curl https://blue.example.com/health

# Deploy green version
kubectl apply -f green-deployment.yaml

# Switch traffic to green
kubectl patch service myapp \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Verify green version
kubectl get pods -l version=green

# Remove blue deployment if successful
kubectl delete deployment myapp-blue
```

### Canary Deployment

```yaml
# canary-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-canary
            port:
              number: 80
```

### GitOps with Tekton

```yaml
# gitops-pipeline.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: gitops-deploy
spec:
  params:
    - name: git-url
    - name: git-revision
    - name: image-tag

  workspaces:
    - name: source
    - name: gitops-repo

  tasks:
    - name: clone-app-repo
      taskRef:
        name: git-clone
      params:
        - name: url
          value: $(params.git-url)
        - name: revision
          value: $(params.git-revision)
      workspaces:
        - name: output
          workspace: source

    - name: build-and-push
      taskRef:
        name: kaniko
      runAfter:
        - clone-app-repo
      params:
        - name: IMAGE
          value: us.icr.io/namespace/app:$(params.image-tag)
      workspaces:
        - name: source
          workspace: source

    - name: clone-gitops-repo
      taskRef:
        name: git-clone
      params:
        - name: url
          value: https://github.com/myorg/gitops-repo
        - name: revision
          value: main
      workspaces:
        - name: output
          workspace: gitops-repo

    - name: update-manifest
      taskRef:
        name: yq
      runAfter:
        - build-and-push
        - clone-gitops-repo
      params:
        - name: file
          value: deployment.yaml
        - name: expression
          value: .spec.template.spec.containers[0].image = "us.icr.io/namespace/app:$(params.image-tag)"
      workspaces:
        - name: source
          workspace: gitops-repo

    - name: commit-and-push
      taskRef:
        name: git-cli
      runAfter:
        - update-manifest
      params:
        - name: GIT_USER_NAME
          value: Tekton Pipeline
        - name: GIT_USER_EMAIL
          value: tekton@example.com
        - name: GIT_SCRIPT
          value: |
            git add .
            git commit -m "Update image to $(params.image-tag)"
            git push origin main
      workspaces:
        - name: source
          workspace: gitops-repo
```

### Exam Tips

1. **CI/CD**
   - Know Tekton vs Classic pipelines
   - Understand toolchain components
   - Practice creating pipelines via CLI and YAML
   - Study DevOps Insights integration

2. **Container Orchestration**
   - Master kubectl and oc commands
   - Understand Kubernetes objects (Deployment, Service, Ingress)
   - Know OpenShift-specific resources (Route, DeploymentConfig)
   - Practice Helm chart creation

3. **Serverless**
   - Know Cloud Functions action types
   - Understand triggers and rules
   - Practice Code Engine deployments
   - Study scaling configurations

4. **Integration**
   - Understand Event Streams (Kafka) patterns
   - Know App Connect use cases
   - Study Event Notifications
   - Practice API Connect policies

5. **Deployment Strategies**
   - Know blue-green vs canary deployments
   - Understand GitOps principles
   - Study rollback procedures
   - Practice zero-downtime deployments

### Common Scenarios

**Scenario 1**: Deploy containerized Node.js app to IKS with auto-scaling
```bash
# Solution approach:
# 1. Build and push image to ICR
# 2. Create Deployment with HorizontalPodAutoscaler
# 3. Configure ingress for external access
# 4. Set up monitoring
```

**Scenario 2**: Implement event-driven architecture with Kafka
```bash
# Solution approach:
# 1. Create Event Streams instance
# 2. Create topics for different event types
# 3. Implement producers and consumers
# 4. Handle failures with dead letter queues
```

**Scenario 3**: Set up CI/CD pipeline with automatic deployments
```bash
# Solution approach:
# 1. Create toolchain with GitHub integration
# 2. Configure Tekton pipeline
# 3. Add testing and security scanning stages
# 4. Implement GitOps for deployment
```
