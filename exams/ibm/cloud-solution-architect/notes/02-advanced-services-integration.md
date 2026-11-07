# IBM Cloud Solution Architect (C1000-175) - Advanced Services & Integration

## Table of Contents
- [AI and Watson Services](#ai-and-watson-services)
- [Data and Analytics](#data-and-analytics)
- [Integration Services](#integration-services)
- [DevOps and CI/CD](#devops-and-cicd)
- [Container Orchestration](#container-orchestration)
- [Serverless Computing](#serverless-computing)
- [API Economy](#api-economy)
- [Blockchain and Edge Computing](#blockchain-and-edge-computing)

---

## AI and Watson Services

### Watson AI Services Architecture
```yaml
# watson-ai-architecture.yaml
watson_services:
  watson_assistant:
    use_cases:
      - Customer service chatbots
      - Virtual agents
      - IT helpdesk automation
    key_features:
      - Natural language understanding
      - Dialog management
      - Integration with channels (Slack, web, mobile)
    integration:
      api: "REST API"
      sdk: "Node.js, Python, Java"

  watson_discovery:
    use_cases:
      - Document search and analysis
      - Knowledge extraction
      - Insight generation
    capabilities:
      - Natural language processing
      - Entity extraction
      - Sentiment analysis
      - Custom models

  watson_natural_language_understanding:
    features:
      - Entity recognition
      - Sentiment analysis
      - Emotion analysis
      - Keyword extraction
      - Concept tagging
    integration_pattern: "Microservices API calls"

  watson_speech_to_text:
    use_cases:
      - Call center transcription
      - Voice commands
      - Meeting transcription
    languages: "Multiple language support"

  watson_text_to_speech:
    use_cases:
      - Voice assistants
      - Accessibility features
      - Content narration
    voices: "Neural and concatenative voices"

  watson_visual_recognition:
    capabilities:
      - Image classification
      - Object detection
      - Face detection
      - Custom model training
```

### Watson Integration Example
```python
# watson_ai_integration.py
from ibm_watson import AssistantV2, DiscoveryV2, NaturalLanguageUnderstandingV1
from ibm_watson import SpeechToTextV1, TextToSpeechV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

class WatsonAIOrchestrator:
    """Orchestrate multiple Watson AI services"""

    def __init__(self, api_keys: dict, urls: dict):
        # Initialize Watson Assistant
        self.assistant = AssistantV2(
            version='2021-06-14',
            authenticator=IAMAuthenticator(api_keys['assistant'])
        )
        self.assistant.set_service_url(urls['assistant'])
        self.assistant_id = api_keys['assistant_id']

        # Initialize Watson Discovery
        self.discovery = DiscoveryV2(
            version='2020-08-30',
            authenticator=IAMAuthenticator(api_keys['discovery'])
        )
        self.discovery.set_service_url(urls['discovery'])
        self.project_id = api_keys['project_id']

        # Initialize NLU
        self.nlu = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=IAMAuthenticator(api_keys['nlu'])
        )
        self.nlu.set_service_url(urls['nlu'])

    def intelligent_search(self, user_query: str):
        """Combine Assistant and Discovery for intelligent search"""
        # Step 1: Process query through Assistant
        session_response = self.assistant.create_session(
            assistant_id=self.assistant_id
        ).get_result()
        session_id = session_response['session_id']

        assistant_response = self.assistant.message(
            assistant_id=self.assistant_id,
            session_id=session_id,
            input={'message_type': 'text', 'text': user_query}
        ).get_result()

        # Step 2: Analyze sentiment and entities with NLU
        nlu_response = self.nlu.analyze(
            text=user_query,
            features=Features(
                entities=EntitiesOptions(sentiment=True, limit=10),
                sentiment=SentimentOptions()
            )
        ).get_result()

        # Step 3: Enhanced search with Discovery
        search_query = self._build_search_query(nlu_response)
        discovery_response = self.discovery.query(
            project_id=self.project_id,
            query=search_query
        ).get_result()

        # Step 4: Synthesize results
        return {
            'user_query': user_query,
            'intent': assistant_response.get('output', {}).get('intents', []),
            'sentiment': nlu_response['sentiment']['document'],
            'entities': nlu_response['entities'],
            'search_results': discovery_response['results'][:5],
            'answer': self._synthesize_answer(assistant_response, discovery_response)
        }

    def _build_search_query(self, nlu_response):
        """Build enhanced search query from NLU results"""
        entities = [e['text'] for e in nlu_response.get('entities', [])]
        return ' OR '.join(entities) if entities else ''

    def _synthesize_answer(self, assistant_resp, discovery_resp):
        """Synthesize answer from multiple sources"""
        assistant_text = assistant_resp.get('output', {}).get('generic', [])
        if assistant_text and assistant_text[0].get('text'):
            return assistant_text[0]['text']

        if discovery_resp.get('results'):
            return discovery_resp['results'][0].get('text', [''])[0][:200]

        return "I couldn't find a specific answer."

# Terraform for Watson services
watson_tf = '''
# watson-services.tf
resource "ibm_resource_instance" "watson_assistant" {
  name              = "production-assistant"
  service           = "conversation"
  plan              = "plus"
  location          = "us-south"
  resource_group_id = data.ibm_resource_group.default.id
}

resource "ibm_resource_instance" "watson_discovery" {
  name              = "production-discovery"
  service           = "discovery"
  plan              = "plus"
  location          = "us-south"
  resource_group_id = data.ibm_resource_group.default.id
}

resource "ibm_resource_instance" "watson_nlu" {
  name              = "production-nlu"
  service           = "natural-language-understanding"
  plan              = "standard"
  location          = "us-south"
  resource_group_id = data.ibm_resource_group.default.id
}

resource "ibm_resource_instance" "watson_speech_to_text" {
  name              = "production-stt"
  service           = "speech-to-text"
  plan              = "standard"
  location          = "us-south"
  resource_group_id = data.ibm_resource_group.default.id
}

# Service credentials
resource "ibm_resource_key" "watson_assistant_key" {
  name                 = "assistant-credentials"
  resource_instance_id = ibm_resource_instance.watson_assistant.id
  role                 = "Manager"
}

resource "kubernetes_secret" "watson_credentials" {
  metadata {
    name      = "watson-credentials"
    namespace = "production"
  }

  data = {
    assistant_apikey = ibm_resource_key.watson_assistant_key.credentials["apikey"]
    assistant_url    = ibm_resource_key.watson_assistant_key.credentials["url"]
    discovery_apikey = ibm_resource_key.watson_discovery_key.credentials["apikey"]
    discovery_url    = ibm_resource_key.watson_discovery_key.credentials["url"]
    nlu_apikey       = ibm_resource_key.watson_nlu_key.credentials["apikey"]
    nlu_url          = ibm_resource_key.watson_nlu_key.credentials["url"]
  }
}
'''
```

---

## Data and Analytics

### Data Lake Architecture
```yaml
# data-lake-architecture.yaml
data_lake_layers:
  raw_layer:
    storage: "IBM Cloud Object Storage"
    format: "Original format (JSON, CSV, Parquet)"
    retention: "7 years"
    access: "Limited to data engineers"

  curated_layer:
    storage: "Cloud Object Storage"
    format: "Standardized (Parquet, ORC)"
    transformations: "Data quality, deduplication"
    access: "Data scientists, analysts"

  analytics_layer:
    storage: "Databases for Analytics"
    services:
      - "IBM Db2 Warehouse"
      - "Cloudant for NoSQL"
      - "Elasticsearch for search"
    access: "BI tools, dashboards"

data_ingestion:
  batch:
    tools: "IBM DataStage, Apache Spark"
    schedule: "Daily, hourly"
    volume: "Large datasets"

  streaming:
    tools: "IBM Event Streams (Kafka)"
    latency: "Real-time, sub-second"
    use_cases: "IoT, clickstream, logs"

  change_data_capture:
    tools: "IBM InfoSphere CDC"
    method: "Log-based CDC"
    use_case: "Database replication"

data_processing:
  batch_processing:
    service: "IBM Analytics Engine (Apache Spark)"
    use_cases:
      - ETL pipelines
      - Machine learning training
      - Data aggregation

  stream_processing:
    service: "IBM Streaming Analytics"
    framework: "Apache Flink, Spark Streaming"
    use_cases:
      - Real-time analytics
      - Fraud detection
      - Monitoring

data_governance:
  catalog: "IBM Watson Knowledge Catalog"
  lineage: "Track data sources and transformations"
  quality: "Data quality rules and monitoring"
  security: "Classification, masking, encryption"
```

### Analytics Pipeline Implementation
```python
# analytics_pipeline.py
from ibm_watson import WatsonMachineLearningAPIClient
from ibm_botocore.client import Config
import ibm_boto3
import pandas as pd
from pyspark.sql import SparkSession
import json

class DataAnalyticsPipeline:
    """End-to-end data analytics pipeline on IBM Cloud"""

    def __init__(self, cos_config, wml_config):
        # Cloud Object Storage
        self.cos_client = ibm_boto3.client(
            's3',
            ibm_api_key_id=cos_config['api_key'],
            ibm_service_instance_id=cos_config['instance_id'],
            config=Config(signature_version='oauth'),
            endpoint_url=cos_config['endpoint']
        )

        # Watson Machine Learning
        self.wml_client = WatsonMachineLearningAPIClient(wml_config)

        # Spark session
        self.spark = SparkSession.builder \
            .appName("IBM Cloud Analytics") \
            .config("spark.hadoop.fs.s3a.endpoint", cos_config['endpoint']) \
            .config("spark.hadoop.fs.s3a.access.key", cos_config['access_key']) \
            .config("spark.hadoop.fs.s3a.secret.key", cos_config['secret_key']) \
            .getOrCreate()

    def ingest_data(self, source_bucket, source_key):
        """Ingest data from Cloud Object Storage"""
        # Read from COS
        obj = self.cos_client.get_object(
            Bucket=source_bucket,
            Key=source_key
        )

        # Load into Spark DataFrame
        df = self.spark.read.json(obj['Body'])
        return df

    def transform_data(self, df):
        """Transform data using Spark"""
        from pyspark.sql.functions import col, when, avg, count

        # Data quality checks
        df_clean = df.na.drop(how='any', subset=['customer_id', 'amount'])

        # Feature engineering
        df_features = df_clean.withColumn(
            'amount_category',
            when(col('amount') < 100, 'low')
            .when(col('amount') < 1000, 'medium')
            .otherwise('high')
        )

        # Aggregations
        df_agg = df_features.groupBy('customer_id').agg(
            count('*').alias('transaction_count'),
            avg('amount').alias('avg_amount')
        )

        return df_agg

    def store_curated_data(self, df, bucket, key):
        """Store curated data back to COS"""
        # Write as Parquet for efficiency
        df.write.mode('overwrite').parquet(
            f"s3a://{bucket}/{key}"
        )

    def train_model(self, training_data):
        """Train ML model with Watson Machine Learning"""
        # Define model metadata
        model_metadata = {
            "name": "Customer Segmentation Model",
            "type": "scikit-learn_1.0",
            "software_spec_uid": self.wml_client.software_specifications.get_uid_by_name("scikit-learn_1.0")
        }

        # Train model (example with scikit-learn)
        from sklearn.cluster import KMeans
        import pickle

        # Convert to pandas for sklearn
        pdf = training_data.toPandas()
        X = pdf[['transaction_count', 'avg_amount']]

        model = KMeans(n_clusters=3, random_state=42)
        model.fit(X)

        # Store model
        stored_model = self.wml_client.repository.store_model(
            model=model,
            meta_props=model_metadata,
            training_data=X
        )

        return stored_model.get('metadata', {}).get('id')

    def deploy_model(self, model_id):
        """Deploy model for scoring"""
        deployment_metadata = {
            "name": "Customer Segmentation Deployment",
            "online": {}
        }

        deployment = self.wml_client.deployments.create(
            model_id,
            meta_props=deployment_metadata
        )

        return deployment.get('metadata', {}).get('id')

    def run_pipeline(self, source_bucket, source_key, output_bucket, output_key):
        """Execute full pipeline"""
        print("1. Ingesting data...")
        df = self.ingest_data(source_bucket, source_key)

        print("2. Transforming data...")
        df_transformed = self.transform_data(df)

        print("3. Storing curated data...")
        self.store_curated_data(df_transformed, output_bucket, output_key)

        print("4. Training ML model...")
        model_id = self.train_model(df_transformed)

        print("5. Deploying model...")
        deployment_id = self.deploy_model(model_id)

        print(f"Pipeline complete! Deployment ID: {deployment_id}")
        return deployment_id

# Terraform for Analytics Infrastructure
analytics_tf = '''
# analytics-infrastructure.tf

# Analytics Engine (Spark cluster)
resource "ibm_analytics_engine" "spark_cluster" {
  name              = "analytics-spark-cluster"
  service_plan      = "standard"
  location          = "us-south"
  resource_group_id = data.ibm_resource_group.default.id
}

# Db2 Warehouse for analytics
resource "ibm_database" "db2_warehouse" {
  name              = "analytics-warehouse"
  plan              = "standard"
  location          = "us-south"
  service           = "dashdb-for-transactions"
  resource_group_id = data.ibm_resource_group.default.id

  group {
    group_id = "member"
    memory {
      allocation_mb = 16384
    }
    disk {
      allocation_mb = 102400
    }
    cpu {
      allocation_count = 6
    }
  }
}

# Watson Machine Learning
resource "ibm_resource_instance" "watson_ml" {
  name              = "production-watson-ml"
  service           = "pm-20"
  plan              = "v2-standard"
  location          = "us-south"
  resource_group_id = data.ibm_resource_group.default.id
}

# Cloud Object Storage for data lake
resource "ibm_resource_instance" "data_lake_cos" {
  name              = "data-lake-storage"
  service           = "cloud-object-storage"
  plan              = "standard"
  location          = "global"
  resource_group_id = data.ibm_resource_group.default.id
}

# COS buckets for different data layers
resource "ibm_cos_bucket" "raw_data" {
  bucket_name          = "raw-data-layer"
  resource_instance_id = ibm_resource_instance.data_lake_cos.id
  region_location      = "us-south"
  storage_class        = "standard"

  activity_tracking {
    read_data_events     = true
    write_data_events    = true
    activity_tracker_crn = ibm_resource_instance.activity_tracker.id
  }
}

resource "ibm_cos_bucket" "curated_data" {
  bucket_name          = "curated-data-layer"
  resource_instance_id = ibm_resource_instance.data_lake_cos.id
  region_location      = "us-south"
  storage_class        = "standard"
}

resource "ibm_cos_bucket" "analytics_data" {
  bucket_name          = "analytics-data-layer"
  resource_instance_id = ibm_resource_instance.data_lake_cos.id
  region_location      = "us-south"
  storage_class        = "smart"

  # Lifecycle policy for cost optimization
  archive_rule {
    rule_id = "archive-old-analytics"
    enable  = true
    days    = 90
    type    = "Glacier"
  }

  expire_rule {
    rule_id = "expire-old-data"
    enable  = true
    days    = 730  # 2 years
  }
}
'''
```

---

## Integration Services

### App Connect Integration Patterns
```yaml
# app-connect-patterns.yaml
integration_patterns:
  point_to_point:
    description: "Direct connection between two systems"
    use_case: "Simple integrations"
    example: "Salesforce to Database"
    pros: "Simple, fast to implement"
    cons: "Not scalable, tight coupling"

  hub_and_spoke:
    description: "Central integration hub"
    use_case: "Multiple system integrations"
    example: "App Connect as central hub"
    pros: "Centralized management, reusable flows"
    cons: "Single point of failure"

  event_driven:
    description: "Event-based integration"
    use_case: "Real-time data synchronization"
    example: "Event Streams + App Connect"
    pros: "Loose coupling, real-time"
    cons: "Complexity, eventual consistency"

  api_led:
    description: "API-based integration"
    layers:
      - System APIs (connect to systems)
      - Process APIs (orchestrate business logic)
      - Experience APIs (serve consumers)
    use_case: "Modern integration architecture"

app_connect_capabilities:
  connectors:
    saas_applications:
      - Salesforce
      - ServiceNow
      - Slack
      - Microsoft 365
      - SAP
      - Workday

    databases:
      - IBM Db2
      - PostgreSQL
      - MySQL
      - Oracle
      - SQL Server

    messaging:
      - IBM MQ
      - Kafka
      - RabbitMQ

    files:
      - FTP/SFTP
      - Cloud Object Storage
      - Box
      - Dropbox

  transformation:
    - Data mapping
    - JSON/XML transformation
    - Data enrichment
    - Filtering
    - Aggregation

  error_handling:
    - Retry policies
    - Dead letter queues
    - Error notifications
    - Compensation logic
```

### App Connect Integration Flow
```bash
# IBM App Connect Enterprise integration

# 1. Create App Connect instance
ibmcloud resource service-instance-create \
  production-app-connect \
  appconnect \
  professional \
  us-south

# 2. Deploy integration server
cat <<EOF > integration-server.yaml
apiVersion: appconnect.ibm.com/v1beta1
kind: IntegrationServer
metadata:
  name: salesforce-integration
spec:
  license:
    accept: true
    license: L-APEH-C79J3U
  version: '12.0'
  replicas: 3
  pod:
    containers:
      runtime:
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1024Mi"
            cpu: "1000m"
  configurations:
    - salesforce-config
    - database-config
  barURL: https://cos.us-south.cloud-object-storage.appdomain.cloud/integrations/salesforce-integration.bar
EOF

kubectl apply -f integration-server.yaml

# 3. Create connector configuration
cat <<EOF > salesforce-connector.yaml
apiVersion: appconnect.ibm.com/v1beta1
kind: Configuration
metadata:
  name: salesforce-config
spec:
  type: accounts
  contents: |
    {
      "accountType": "salesforce",
      "name": "Salesforce Production",
      "credentials": {
        "clientId": "$SALESFORCE_CLIENT_ID",
        "clientSecret": "$SALESFORCE_CLIENT_SECRET",
        "username": "$SALESFORCE_USERNAME",
        "password": "$SALESFORCE_PASSWORD",
        "securityToken": "$SALESFORCE_SECURITY_TOKEN"
      }
    }
EOF

kubectl apply -f salesforce-connector.yaml
```

---

## DevOps and CI/CD

### IBM Cloud Toolchain Architecture
```yaml
# toolchain-architecture.yaml
continuous_delivery:
  source_control:
    - GitHub/GitLab
    - IBM Git Repos
    - Bitbucket

  build:
    - Tekton Pipelines
    - Jenkins
    - Travis CI
    - CircleCI

  test:
    - Unit tests
    - Integration tests
    - Security scanning (Vulnerability Advisor)
    - Code quality (SonarQube)

  deploy:
    targets:
      - IBM Cloud Kubernetes Service
      - Red Hat OpenShift on IBM Cloud
      - Cloud Foundry
      - Code Engine
      - Virtual Servers

  monitor:
    - IBM Cloud Monitoring
    - LogDNA
    - Activity Tracker

pipeline_stages:
  commit_stage:
    - Source checkout
    - Dependency installation
    - Unit tests
    - Code quality analysis
    - Build artifact (container image)
    - Push to registry

  acceptance_stage:
    - Deploy to staging
    - Integration tests
    - API tests
    - Performance tests
    - Security scans

  production_stage:
    - Blue-green deployment
    - Canary deployment
    - Feature flag based rollout
    - Automated rollback

  monitoring:
    - Health checks
    - Performance monitoring
    - Log aggregation
    - Alert management
```

### Tekton Pipeline Example
```yaml
# tekton-pipeline.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: build-deploy-pipeline
spec:
  params:
  - name: git-url
    type: string
  - name: git-revision
    type: string
    default: main
  - name: image-name
    type: string
  - name: deployment-name
    type: string

  workspaces:
  - name: shared-workspace

  tasks:
  # Task 1: Git Clone
  - name: fetch-repository
    taskRef:
      name: git-clone
    workspaces:
    - name: output
      workspace: shared-workspace
    params:
    - name: url
      value: $(params.git-url)
    - name: revision
      value: $(params.git-revision)

  # Task 2: Run Tests
  - name: run-tests
    taskRef:
      name: python-test
    runAfter:
    - fetch-repository
    workspaces:
    - name: source
      workspace: shared-workspace

  # Task 3: Build Container Image
  - name: build-image
    taskRef:
      name: buildah
    runAfter:
    - run-tests
    workspaces:
    - name: source
      workspace: shared-workspace
    params:
    - name: IMAGE
      value: $(params.image-name):$(params.git-revision)
    - name: DOCKERFILE
      value: ./Dockerfile

  # Task 4: Security Scan
  - name: security-scan
    taskRef:
      name: vulnerability-advisor
    runAfter:
    - build-image
    params:
    - name: image
      value: $(params.image-name):$(params.git-revision)

  # Task 5: Deploy to Kubernetes
  - name: deploy-to-cluster
    taskRef:
      name: kubectl-deploy
    runAfter:
    - security-scan
    params:
    - name: deployment
      value: $(params.deployment-name)
    - name: image
      value: $(params.image-name):$(params.git-revision)

  # Task 6: Verify Deployment
  - name: verify-deployment
    taskRef:
      name: health-check
    runAfter:
    - deploy-to-cluster
    params:
    - name: service-url
      value: https://$(params.deployment-name).example.com/healthz

---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: kubectl-deploy
spec:
  params:
  - name: deployment
    type: string
  - name: image
    type: string

  steps:
  - name: update-deployment
    image: bitnami/kubectl:latest
    script: |
      #!/bin/bash
      kubectl set image deployment/$(params.deployment) \
        app=$(params.image) \
        --record

      kubectl rollout status deployment/$(params.deployment)

      # Check if rollout was successful
      if [ $? -ne 0 ]; then
        echo "Deployment failed, rolling back..."
        kubectl rollout undo deployment/$(params.deployment)
        exit 1
      fi

---
apiVersion: triggers.tekton.dev/v1beta1
kind: EventListener
metadata:
  name: github-webhook-listener
spec:
  serviceAccountName: tekton-triggers-sa
  triggers:
  - name: github-push-trigger
    interceptors:
    - ref:
        name: github
      params:
      - name: secretRef
        value:
          secretName: github-secret
          secretKey: webhookSecret
      - name: eventTypes
        value: ["push"]
    bindings:
    - ref: github-push-binding
    template:
      ref: pipeline-template
```

---

## Container Orchestration

### OpenShift vs Kubernetes on IBM Cloud
```yaml
# openshift-vs-kubernetes.yaml
kubernetes_service:
  pros:
    - Standard Kubernetes API
    - Lower cost
    - Simple deployment model
    - Good for cloud-native apps
  cons:
    - Requires more DevOps expertise
    - Less built-in security features
    - Manual setup for many features

  use_cases:
    - Microservices applications
    - Startups and SMBs
    - Cost-sensitive projects
    - Pure cloud-native workloads

openshift_on_ibm_cloud:
  pros:
    - Enterprise features out-of-box
    - Built-in CI/CD (Tekton, S2I)
    - Enhanced security (SCC, RBAC)
    - Developer-friendly console
    - Operator framework
    - Service mesh (Istio) integration
  cons:
    - Higher cost
    - More complex
    - Opinionated platform

  use_cases:
    - Enterprise applications
    - Hybrid cloud deployments
    - Regulated industries
    - Teams wanting integrated DevOps

architectural_components:
  kubernetes:
    - Control Plane (managed by IBM)
    - Worker Nodes
    - Ingress Controller
    - Storage Classes
    - Load Balancer

  openshift_additions:
    - OpenShift Router (advanced ingress)
    - Integrated Registry
    - Build configurations (S2I)
    - Developer Console
    - Operator Hub
    - Service Mesh
    - Monitoring stack (Prometheus, Grafana)
```

---

## Serverless Computing

### IBM Cloud Functions Architecture

> **Legacy service:** IBM publishes migration guidance for moving off IBM Cloud Functions (OpenWhisk); its target is IBM Code Engine ([IBM: How to move from IBM Cloud Functions to IBM Code Engine](https://www.ibm.com/products/tutorials/how-to-move-from-ibm-cloud-functions-to-ibm-code-engine)). Treat the Cloud Functions material below as the legacy model.
```yaml
# cloud-functions-architecture.yaml
serverless_patterns:
  event_driven:
    triggers:
      - HTTP requests
      - Cloud Object Storage events
      - Database changes
      - Scheduled (cron)
      - Message queue
    use_cases:
      - File processing
      - API backends
      - Webhooks
      - Scheduled jobs

  orchestration:
    composer: "IBM Cloud Functions Composer"
    capabilities:
      - Sequential execution
      - Parallel execution
      - Conditional logic
      - Error handling
      - Retry logic

  integration:
    - Pre-built packages (Watson, Cloudant, etc.)
    - Custom packages
    - API Gateway integration
    - Event Streams integration

best_practices:
  performance:
    - Cold start optimization
    - Function size < 48 MB
    - Execution time < 10 minutes
    - Concurrent execution limits

  cost_optimization:
    - Right-size memory allocation
    - Minimize execution time
    - Use caching where possible
    - Clean up unused actions

  security:
    - Use namespaces for isolation
    - Secure parameter binding
    - API key management
    - Network isolation with Cloud Foundry Enterprise Environment
```

### Cloud Functions Implementation
```python
# cloud_functions_example.py
import json
import ibm_boto3
from ibm_botocore.client import Config
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(args):
    """
    Cloud Function: Process uploaded document
    Triggered by Cloud Object Storage
    """
    # Get event details
    bucket = args.get('bucket')
    key = args.get('key')

    if not bucket or not key:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing bucket or key'})
        }

    try:
        # Initialize COS client
        cos = ibm_boto3.client(
            's3',
            ibm_api_key_id=args.get('cos_api_key'),
            ibm_service_instance_id=args.get('cos_instance_id'),
            config=Config(signature_version='oauth'),
            endpoint_url=args.get('cos_endpoint')
        )

        # Download file from COS
        obj = cos.get_object(Bucket=bucket, Key=key)
        content = obj['Body'].read().decode('utf-8')

        # Process with Watson
        translator = LanguageTranslatorV3(
            version='2018-05-01',
            authenticator=IAMAuthenticator(args.get('watson_api_key'))
        )
        translator.set_service_url(args.get('watson_url'))

        # Translate document
        translation = translator.translate(
            text=content,
            model_id='en-es'
        ).get_result()

        translated_text = translation['translations'][0]['translation']

        # Store result back to COS
        output_key = f"translated/{key}"
        cos.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=translated_text.encode('utf-8')
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Document processed successfully',
                'output_location': f"{bucket}/{output_key}"
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Deploy Cloud Function
deploy_script = '''
# deploy-function.sh

# Create action
ibmcloud fn action create process-document \
  --kind python:3.9 \
  cloud_functions_example.py \
  --memory 512 \
  --timeout 300000

# Bind parameters
ibmcloud fn action update process-document \
  --param cos_api_key "$COS_API_KEY" \
  --param cos_instance_id "$COS_INSTANCE_ID" \
  --param cos_endpoint "$COS_ENDPOINT" \
  --param watson_api_key "$WATSON_API_KEY" \
  --param watson_url "$WATSON_URL"

# Create COS trigger
ibmcloud fn trigger create cos-upload-trigger \
  --feed /whisk.system/cos/changes \
  --param bucket "documents" \
  --param event_types "write"

# Create rule to connect trigger and action
ibmcloud fn rule create process-on-upload \
  cos-upload-trigger \
  process-document
'''
```

---

## API Economy

### API Management Strategy
```yaml
# api-management.yaml
api_lifecycle:
  design:
    - Define API specification (OpenAPI)
    - Design RESTful resources
    - Version strategy
    - Documentation

  develop:
    - Implement API endpoints
    - Input validation
    - Error handling
    - Testing (unit, integration)

  secure:
    - Authentication (OAuth 2.0, API keys)
    - Authorization (RBAC)
    - Rate limiting
    - IP whitelisting
    - TLS/SSL encryption

  publish:
    - API Gateway deployment
    - Developer portal
    - Documentation publication
    - Client SDK generation

  manage:
    - Analytics and monitoring
    - Usage tracking
    - Performance optimization
    - Deprecation management

  monetize:
    - Usage-based pricing
    - Tiered plans
    - Freemium model
    - Enterprise licensing

api_gateway_features:
  traffic_management:
    - Rate limiting
    - Quota enforcement
    - Spike arrest
    - Caching

  security:
    - API key validation
    - OAuth 2.0 / OIDC
    - JWT validation
    - IP filtering
    - CORS handling

  transformation:
    - Request/response modification
    - Protocol mediation (REST to SOAP)
    - Data formatting (JSON/XML)

  analytics:
    - API usage metrics
    - Performance monitoring
    - Error tracking
    - Consumer behavior analysis
```

---

## Blockchain and Edge Computing

### IBM Blockchain Platform
```yaml
# blockchain-platform.yaml
blockchain_use_cases:
  supply_chain:
    - Track and trace
    - Provenance verification
    - Quality assurance
    - Counterfeit prevention

  financial_services:
    - Cross-border payments
    - Trade finance
    - Securities settlement
    - Digital identity

  healthcare:
    - Medical records sharing
    - Drug traceability
    - Clinical trial data
    - Insurance claims

hyperledger_fabric_components:
  peers:
    - Maintain ledger
    - Execute chaincode
    - Endorse transactions

  orderers:
    - Order transactions
    - Create blocks
    - Distribute to peers

  certificate_authority:
    - Identity management
    - Certificate issuance
    - Access control

  channels:
    - Private communication
    - Data isolation
    - Confidentiality
```

### Edge Application Manager
```yaml
# edge-computing.yaml
edge_patterns:
  edge_analytics:
    - Real-time data processing
    - Reduced latency
    - Bandwidth optimization
    - Local decision making

  edge_ml:
    - Inference at edge
    - Model deployment
    - Federated learning
    - Privacy preservation

  iot_gateway:
    - Device management
    - Protocol translation
    - Data aggregation
    - Local caching

ibm_edge_capabilities:
  deployment:
    - Autonomous agent-based
    - Policy-driven
    - Scalable to thousands of nodes

  management:
    - Centralized control
    - Over-the-air updates
    - Health monitoring
    - Rollback capabilities

  security:
    - Zero-trust architecture
    - Encrypted communication
    - Secure boot
    - Attestation
```

---

## Exam Tips

1. **Watson AI**: Know service capabilities and integration patterns
2. **Data Analytics**: Understand data lake architecture, Spark processing
3. **Integration**: Master App Connect patterns and connectors
4. **DevOps**: Tekton pipelines, toolchains, deployment strategies
5. **Containers**: OpenShift vs Kubernetes decision factors
6. **Serverless**: Cloud Functions triggers, use cases, limitations
7. **API Management**: API lifecycle, security, monetization
8. **Advanced**: Blockchain use cases, Edge computing patterns

### Common Scenarios

**Scenario 1**: Design AI-powered customer service
- Watson Assistant for chatbot
- Watson Discovery for knowledge base
- NLU for sentiment analysis
- Speech-to-Text for voice input
- Integration with CRM via App Connect

**Scenario 2**: Build real-time analytics pipeline
- Event Streams for data ingestion
- Streaming Analytics for processing
- COS for data lake storage
- Watson ML for predictions
- Db2 Warehouse for SQL analytics

**Scenario 3**: Implement enterprise CI/CD
- Tekton pipelines for builds
- Vulnerability Advisor for security
- Blue-green deployment to OpenShift
- Automated testing and quality gates
- Monitoring with Sysdig

### Hands-On Practice

1. Build Watson AI chatbot with backend integration
2. Create data analytics pipeline with Spark
3. Implement App Connect integration flows
4. Design and deploy Tekton CI/CD pipeline
5. Deploy serverless functions with triggers
6. Set up API Gateway with security
7. Explore OpenShift Operators and service mesh

## Key terms

- **IBM Cloud Satellite** - an IBM Cloud service that brings IBM Cloud services to on-premises, edge or other cloud locations.
- **Event Streams** - the IBM Cloud managed Apache Kafka service for streaming events.
- **Key Protect** - the IBM Cloud service for managing encryption keys.
- **Activity Tracker** - the IBM Cloud service that records activity events on resources for auditing.
