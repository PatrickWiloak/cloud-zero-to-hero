# OCI Developer Associate - DevOps and Monitoring

## Table of Contents
- [DevOps Service](#devops-service)
- [Resource Manager](#resource-manager)
- [Application Performance Monitoring](#application-performance-monitoring)
- [Logging and Observability](#logging-and-observability)
- [Exam Tips](#exam-tips)

---

## DevOps Service

### DevOps Project Setup

**Creating DevOps Project**:
```terraform
resource "oci_devops_project" "main" {
  compartment_id = var.compartment_id
  name           = "my-application"
  description    = "DevOps project for My Application"

  notification_config {
    topic_id = oci_ons_notification_topic.devops.id
  }
}
```

### Code Repository

**Creating Repository**:
```bash
# Create repository
oci devops repository create \
  --project-id ocid1.devopsproject... \
  --name "my-app-repo" \
  --repository-type HOSTED

# Clone repository
git clone https://devops.scmservice.us-phoenix-1.oci.oraclecloud.com/namespaces/namespace/projects/project/repositories/my-app-repo

# Add code and push
git add .
git commit -m "Initial commit"
git push origin main
```

### Build Pipeline

**Build Spec (build_spec.yaml)**:
```yaml
version: 0.1
component: build
timeoutInSeconds: 600

env:
  variables:
    APP_NAME: "my-app"
    DOCKER_REGISTRY: "phx.ocir.io"

  exportedVariables:
    - IMAGE_TAG

steps:
  - type: Command
    name: "Install dependencies"
    command: |
      npm install

  - type: Command
    name: "Run tests"
    command: |
      npm test

  - type: Command
    name: "Build application"
    command: |
      npm run build

  - type: Command
    name: "Build Docker image"
    command: |
      export IMAGE_TAG=$(git rev-parse --short HEAD)
      docker build -t ${DOCKER_REGISTRY}/${TENANCY_NAMESPACE}/${APP_NAME}:${IMAGE_TAG} .

  - type: Command
    name: "Push to OCIR"
    command: |
      docker push ${DOCKER_REGISTRY}/${TENANCY_NAMESPACE}/${APP_NAME}:${IMAGE_TAG}

outputArtifacts:
  - name: app_image
    type: DOCKER_IMAGE
    location: ${DOCKER_REGISTRY}/${TENANCY_NAMESPACE}/${APP_NAME}:${IMAGE_TAG}

  - name: kubernetes_manifest
    type: KUBERNETES_MANIFEST
    location: k8s/deployment.yaml
```

**Build Pipeline Configuration**:
```terraform
resource "oci_devops_build_pipeline" "main" {
  project_id     = oci_devops_project.main.id
  display_name   = "build-pipeline"
  description    = "Build and test application"

  build_pipeline_parameters {
    items {
      name          = "ENVIRONMENT"
      default_value = "production"
      description   = "Deployment environment"
    }
  }
}

# Build stage
resource "oci_devops_build_pipeline_stage" "build" {
  build_pipeline_id = oci_devops_build_pipeline.main.id
  display_name      = "Build and Test"
  build_pipeline_stage_type = "BUILD"

  build_pipeline_stage_predecessor_collection {
    items {
      id = oci_devops_build_pipeline.main.id
    }
  }

  build_spec_file = "build_spec.yaml"
  image           = "OL7_X86_64_STANDARD_10"  # Build runner image

  build_source_collection {
    items {
      connection_type = "DEVOPS_CODE_REPOSITORY"
      repository_id   = oci_devops_repository.main.id
      branch          = "main"
    }
  }
}

# Deliver artifact stage
resource "oci_devops_build_pipeline_stage" "deliver" {
  build_pipeline_id = oci_devops_build_pipeline.main.id
  display_name      = "Deliver Artifacts"
  build_pipeline_stage_type = "DELIVER_ARTIFACT"

  build_pipeline_stage_predecessor_collection {
    items {
      id = oci_devops_build_pipeline_stage.build.id
    }
  }

  deliver_artifact_collection {
    items {
      artifact_name = "app_image"
      artifact_id   = oci_devops_deploy_artifact.image.id
    }
  }
}
```

### Deployment Pipeline

**Deployment Artifact**:
```terraform
resource "oci_devops_deploy_artifact" "image" {
  project_id              = oci_devops_project.main.id
  display_name            = "app-image"
  deploy_artifact_type    = "DOCKER_IMAGE"

  deploy_artifact_source {
    deploy_artifact_source_type = "OCIR"

    image_uri      = "${var.region}.ocir.io/${var.namespace}/my-app"
    image_digest   = "${var.image_digest}"  # From build pipeline
  }
}

resource "oci_devops_deploy_artifact" "k8s_manifest" {
  project_id           = oci_devops_project.main.id
  display_name         = "k8s-deployment"
  deploy_artifact_type = "KUBERNETES_MANIFEST"

  deploy_artifact_source {
    deploy_artifact_source_type = "INLINE"

    base64encoded_content = base64encode(templatefile(
      "k8s/deployment.yaml",
      {
        image = "${var.region}.ocir.io/${var.namespace}/my-app:$${IMAGE_TAG}"
      }
    ))
  }
}
```

**Deployment Pipeline**:
```terraform
resource "oci_devops_deploy_pipeline" "main" {
  project_id   = oci_devops_project.main.id
  display_name = "deploy-pipeline"
  description  = "Deploy to OKE"

  deploy_pipeline_parameters {
    items {
      name          = "NAMESPACE"
      default_value = "production"
    }
  }
}

# Deploy to OKE stage
resource "oci_devops_deploy_stage" "oke_deploy" {
  deploy_pipeline_id = oci_devops_deploy_pipeline.main.id
  display_name       = "Deploy to OKE"
  deploy_stage_type  = "OKE_DEPLOYMENT"

  deploy_stage_predecessor_collection {
    items {
      id = oci_devops_deploy_pipeline.main.id
    }
  }

  oke_cluster_deploy_environment_id = oci_devops_deploy_environment.oke.id

  kubernetes_manifest_deploy_artifact_ids = [
    oci_devops_deploy_artifact.k8s_manifest.id
  ]

  namespace = "${var.namespace}"

  rollback_policy {
    policy_type = "AUTOMATED_STAGE_ROLLBACK_POLICY"
  }
}

# Approval stage (optional)
resource "oci_devops_deploy_stage" "approval" {
  deploy_pipeline_id = oci_devops_deploy_pipeline.main.id
  display_name       = "Production Approval"
  deploy_stage_type  = "MANUAL_APPROVAL"

  deploy_stage_predecessor_collection {
    items {
      id = oci_devops_deploy_stage.oke_deploy.id
    }
  }

  approval_policy {
    approval_policy_type         = "COUNT_BASED_APPROVAL"
    number_of_approvals_required = 1
  }
}
```

### Triggers

**Trigger on Push to Main**:
```terraform
resource "oci_devops_trigger" "main_push" {
  project_id     = oci_devops_project.main.id
  display_name   = "trigger-on-main-push"
  trigger_source = "DEVOPS_CODE_REPOSITORY"

  repository_id = oci_devops_repository.main.id

  actions {
    type                = "TRIGGER_BUILD_PIPELINE"
    build_pipeline_id   = oci_devops_build_pipeline.main.id

    filter {
      trigger_source = "DEVOPS_CODE_REPOSITORY"

      events = ["PUSH"]

      include {
        head_ref = "refs/heads/main"
      }
    }
  }
}
```

---

## Resource Manager

### Terraform Configuration

**Provider Configuration**:
```hcl
# provider.tf
terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
  }
}

provider "oci" {
  region = var.region
  # Authentication via instance principal, resource principal, or config file
}
```

**Variables**:
```hcl
# variables.tf
variable "compartment_id" {
  description = "Compartment OCID"
  type        = string
}

variable "region" {
  description = "OCI region"
  type        = string
  default     = "us-phoenix-1"
}

variable "instance_shape" {
  description = "Compute instance shape"
  type        = string
  default     = "VM.Standard.E4.Flex"
}

variable "instance_ocpus" {
  description = "Number of OCPUs"
  type        = number
  default     = 2
}
```

**Resources**:
```hcl
# main.tf
resource "oci_core_vcn" "main" {
  compartment_id = var.compartment_id
  display_name   = "app-vcn"
  cidr_blocks    = ["10.0.0.0/16"]
  dns_label      = "appvcn"
}

resource "oci_core_subnet" "public" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "public-subnet"
  cidr_block     = "10.0.1.0/24"
  route_table_id = oci_core_route_table.public.id
  dns_label      = "public"
}

resource "oci_core_instance" "app" {
  compartment_id      = var.compartment_id
  availability_domain = data.oci_identity_availability_domain.ad1.name
  display_name        = "app-server"
  shape               = var.instance_shape

  shape_config {
    ocpus         = var.instance_ocpus
    memory_in_gbs = var.instance_ocpus * 8
  }

  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.oracle_linux.images[0].id
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.public.id
    assign_public_ip = true
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key
  }
}
```

**Outputs**:
```hcl
# outputs.tf
output "instance_public_ip" {
  description = "Public IP of instance"
  value       = oci_core_instance.app.public_ip
}

output "vcn_id" {
  description = "VCN OCID"
  value       = oci_core_vcn.main.id
}
```

### Resource Manager Stack

**Creating Stack**:
```bash
# Create zip of Terraform files
zip -r terraform.zip *.tf

# Create stack
oci resource-manager stack create \
  --compartment-id ocid1.compartment... \
  --display-name "app-infrastructure" \
  --config-source terraform.zip \
  --variables file://variables.json
```

**Stack Operations**:
```bash
# Plan
oci resource-manager job create-plan-job \
  --stack-id ocid1.ormstack... \
  --display-name "plan-job"

# Apply
oci resource-manager job create-apply-job \
  --stack-id ocid1.ormstack... \
  --display-name "apply-job" \
  --execution-plan-strategy AUTO_APPROVED

# Destroy
oci resource-manager job create-destroy-job \
  --stack-id ocid1.ormstack... \
  --display-name "destroy-job" \
  --execution-plan-strategy AUTO_APPROVED
```

**Drift Detection**:
```bash
# Detect drift (changes outside Terraform)
oci resource-manager stack detect-drift \
  --stack-id ocid1.ormstack... \
  --display-name "drift-detection"

# View drift
oci resource-manager job get-job-detailed-log-content \
  --job-id ocid1.ormjob...
```

---

## Application Performance Monitoring

### APM Setup

**Creating APM Domain**:
```terraform
resource "oci_apm_apm_domain" "main" {
  compartment_id = var.compartment_id
  display_name   = "app-apm"
  description    = "APM for application monitoring"
  is_free_tier   = false
}

# Data keys for different services
resource "oci_apm_data_key" "frontend" {
  apm_domain_id = oci_apm_apm_domain.main.id
  name          = "frontend-key"
  type          = "PRIVATE"
}

resource "oci_apm_data_key" "backend" {
  apm_domain_id = oci_apm_apm_domain.main.id
  name          = "backend-key"
  type          = "PRIVATE"
}
```

### Application Instrumentation

**Java Application**:
```bash
# Add APM Java agent
java -javaagent:/path/to/apm-java-agent.jar \
     -Dcom.oracle.apm.agent.service_name=backend-api \
     -Dcom.oracle.apm.agent.data_upload_endpoint=https://apm-domain-endpoint \
     -Dcom.oracle.apm.agent.private_data_key=PRIVATE_KEY \
     -jar application.jar
```

**Python Application**:
```python
# Install OpenTelemetry
# pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup APM tracing
trace.set_tracer_provider(TracerProvider())
otlp_exporter = OTLPSpanExporter(
    endpoint="https://apm-domain-endpoint",
    headers={"authorization": f"Bearer {private_data_key}"}
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Instrument Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
FlaskInstrumentor().instrument_app(app)

# Manual spans
tracer = trace.get_tracer(__name__)

@app.route('/api/users')
def get_users():
    with tracer.start_as_current_span("fetch-users"):
        with tracer.start_as_current_span("db-query"):
            users = database.query("SELECT * FROM users")

        with tracer.start_as_current_span("serialize"):
            result = jsonify(users)

        return result
```

**Node.js Application**:
```javascript
// Install: npm install @opentelemetry/api @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node

const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'https://apm-domain-endpoint/v1/traces',
    headers: {
      'authorization': `Bearer ${process.env.APM_PRIVATE_KEY}`
    }
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  serviceName: 'nodejs-api'
});

sdk.start();

// Application code
const express = require('express');
const app = express();

app.get('/api/data', async (req, res) => {
  // Automatically traced
  const data = await database.query('SELECT * FROM data');
  res.json(data);
});
```

### Synthetic Monitoring

**Creating Synthetic Monitor**:
```terraform
resource "oci_apm_synthetics_monitor" "api_health" {
  apm_domain_id  = oci_apm_apm_domain.main.id
  display_name   = "API Health Check"
  monitor_type   = "REST"
  repeat_interval_in_seconds = 300  # 5 minutes

  configuration {
    config_type = "REST_CONFIG"
    is_redirection_enabled = true
    is_certificate_validation_enabled = true

    req_authentication_details {
      auth_type = "NONE"
    }

    request_method = "GET"
    request_headers = [
      {
        header_name  = "Content-Type"
        header_value = "application/json"
      }
    ]
  }

  vantage_points {
    name = "us-phoenix-1"
  }

  # Alert on failures
  is_run_once = false
  status      = "ENABLED"

  script_parameters {
    param_name  = "endpoint"
    param_value = "https://api.example.com/health"
  }
}
```

---

## Logging and Observability

### Custom Logs

**Creating Log Group**:
```terraform
resource "oci_logging_log_group" "app_logs" {
  compartment_id = var.compartment_id
  display_name   = "application-logs"
}

# Custom log
resource "oci_logging_log" "application" {
  display_name = "app-logs"
  log_group_id = oci_logging_log_group.app_logs.id
  log_type     = "CUSTOM"

  configuration {
    source {
      category    = "custom"
      resource    = oci_functions_application.main.id
      service     = "functions"
      source_type = "OCISERVICE"
    }

    compartment_id = var.compartment_id
  }

  is_enabled         = true
  retention_duration = 30
}
```

**Sending Logs from Application**:
```python
import oci
import json
import time

logging_client = oci.loggingingestion.LoggingClient(config)

def send_log(message, level="INFO"):
    log_entry = oci.loggingingestion.models.LogEntry(
        data=json.dumps({
            "message": message,
            "level": level,
            "timestamp": time.time()
        }),
        id=str(uuid.uuid4()),
        time=datetime.utcnow().isoformat() + 'Z'
    )

    put_logs_details = oci.loggingingestion.models.PutLogsDetails(
        specversion="1.0",
        log_entry_batches=[
            oci.loggingingestion.models.LogEntryBatch(
                entries=[log_entry],
                source="my-application",
                type="custom",
                defaultlogentrytime=datetime.utcnow().isoformat() + 'Z'
            )
        ]
    )

    logging_client.put_logs(
        log_id="ocid1.log...",
        put_logs_details=put_logs_details
    )
```

### Log Analytics

**Log Analytics Queries**:
```
# Find errors in last hour
'Log Source' = 'application-logs' |
where level = 'ERROR' |
where 'Log Time' > now() - 1h |
stats count() by message

# Response time analysis
'Log Source' = 'api-access-logs' |
where 'Response Time' > 1000 |
stats avg('Response Time'), max('Response Time'), count() by endpoint

# User activity tracking
'Log Source' = 'audit-logs' |
where eventType = 'user.login' |
stats count() by user, location
```

### Dashboards

**Creating Custom Dashboard**:
```terraform
resource "oci_management_dashboard" "app_dashboard" {
  compartment_id = var.compartment_id
  display_name   = "Application Dashboard"

  config = jsonencode({
    "widgets": [
      {
        "id": "widget-1",
        "type": "line-chart",
        "title": "Request Rate",
        "query": "CpuUtilization[1m].mean()",
        "namespace": "oci_computeagent"
      },
      {
        "id": "widget-2",
        "type": "bar-chart",
        "title": "Error Count",
        "query": "'Log Source' = 'app' | where level = 'ERROR' | stats count() by type"
      }
    ]
  })
}
```

---

## Exam Tips

### Critical Concepts

**DevOps**:
- Build pipeline: Compile, test, package
- Deployment pipeline: Deploy to environments
- Triggers: Automate on code push
- Approval stages: Manual gates for production

**Resource Manager**:
- Infrastructure as Code (Terraform)
- Stack: Collection of TF files
- Operations: Plan, Apply, Destroy
- Drift detection: Find manual changes

**APM**:
- Distributed tracing: Track requests across services
- Spans: Individual operations
- Instrumentation: Add to application code
- Synthetic monitoring: Proactive health checks

**Logging**:
- Service logs: Automatic (VCN flow, LB access)
- Custom logs: Application-generated
- Log Analytics: Query and analyze logs
- Retention: Configure based on requirements

### Common Scenarios

**Q: Automate deployment on code push?**
A: DevOps trigger + build pipeline + deployment pipeline

**Q: Track request across microservices?**
A: APM with distributed tracing

**Q: Manage infrastructure as code?**
A: Resource Manager (Terraform)

**Q: Find errors in application logs?**
A: Log Analytics with queries

**Q: Detect manual infrastructure changes?**
A: Resource Manager drift detection

---

## Summary

**DevOps**: CI/CD pipelines, automated deployments, triggers

**Resource Manager**: Infrastructure as Code, Terraform, drift detection

**APM**: Distributed tracing, performance monitoring, synthetic checks

**Logging**: Service logs, custom logs, Log Analytics, queries

---

**Congratulations on completing OCI Developer Associate study notes!**

## Key terms

- **OCI DevOps service** - the OCI service that provides code repositories, build pipelines and deployment pipelines.
- **Build pipeline** - an OCI DevOps pipeline that compiles, tests and packages code into artifacts.
- **Deployment pipeline** - an OCI DevOps pipeline that delivers artifacts to environments such as OKE or Functions.
- **Resource Manager** - the OCI service that provisions infrastructure from Terraform configurations packaged as stacks.
- **Log Analytics** - the OCI service for searching, analysing and visualising log data.
- **Synthetic monitoring** - a way to measure application availability and performance by running scripted tests from vantage points.
