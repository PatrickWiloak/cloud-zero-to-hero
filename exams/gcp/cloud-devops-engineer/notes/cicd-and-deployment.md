# CI/CD and Deployment - GCP Professional Cloud DevOps Engineer

## Overview

Continuous integration, continuous deployment, release management, and deployment automation for cloud-native applications.

## CI/CD Pipeline Architecture

### Cloud Build Pipeline
**Build Configuration**:
```yaml
steps:
  # Unit tests
  - name: 'gcr.io/cloud-builders/npm'
    args: ['install']
  - name: 'gcr.io/cloud-builders/npm'
    args: ['test']

  # Security scanning
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['beta', 'container', 'images', 'scan', 'gcr.io/$PROJECT_ID/app:$COMMIT_SHA']

  # Build and push
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/app:$COMMIT_SHA', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/app:$COMMIT_SHA']

  # Deploy
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
    - run
    - --filename=k8s/
    - --image=gcr.io/$PROJECT_ID/app:$COMMIT_SHA
    - --cluster=production-cluster
    - --location=us-central1

timeout: 1200s
options:
  machineType: 'N1_HIGHCPU_8'
```

### Automated Testing
**Test Stages**:
1. **Unit Tests**: Fast, isolated tests
2. **Integration Tests**: Component interaction tests
3. **Security Scanning**: Vulnerability detection
4. **Performance Tests**: Load and stress testing
5. **Smoke Tests**: Post-deployment validation

### Binary Authorization
**Policy Enforcement**:
```yaml
# Require attestations before deployment
admissionWhitelistPatterns:
- namePattern: gcr.io/my-project/*
defaultAdmissionRule:
  requireAttestationsBy:
  - projects/my-project/attestors/security-attestor
  - projects/my-project/attestors/qa-attestor
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
```

## Deployment Strategies

### Rolling Deployment
**Kubernetes**:
```yaml
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

### Blue-Green Deployment
```bash
# Deploy green environment
kubectl apply -f deployment-green.yaml

# Test green
kubectl port-forward service/app-green 8080:80

# Switch traffic
kubectl patch service app -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback if needed
kubectl patch service app -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Canary Deployment
**Cloud Deploy**:
```yaml
apiVersion: deploy.cloud.google.com/v1
kind: DeliveryPipeline
metadata:
  name: my-pipeline
stages:
- targetId: staging
- targetId: prod-canary
  profiles: [canary]
  strategy:
    canary:
      runtimeConfig:
        kubernetes:
          serviceNetworking:
            service: "my-app"
      canaryDeployment:
        percentages: [25, 50, 100]
        verify: true
```

## Infrastructure as Code

### Terraform
**Example Configuration**:
```hcl
resource "google_container_cluster" "primary" {
  name     = "production-cluster"
  location = "us-central1"

  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_nodes" {
  cluster    = google_container_cluster.primary.name
  location   = "us-central1"
  node_count = 3

  node_config {
    machine_type = "n1-standard-2"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }
}
```

### Cloud Deployment Manager
```yaml
resources:
- name: production-cluster
  type: container.v1.cluster
  properties:
    zone: us-central1-a
    cluster:
      initialNodeCount: 3
      nodeConfig:
        machineType: n1-standard-2
        oauthScopes:
        - https://www.googleapis.com/auth/cloud-platform
```

## Release Management

### GitOps Workflow
1. **Git as Single Source of Truth**: All configs in Git
2. **Pull-Based Deployment**: Agents pull from Git
3. **Automated Sync**: Auto-deploy on Git changes
4. **Rollback via Git**: Revert commits to rollback

**Config Sync (Anthos)**:
```yaml
apiVersion: configmanagement.gke.io/v1
kind: ConfigManagement
metadata:
  name: config-management
spec:
  git:
    syncRepo: https://github.com/myorg/configs
    syncBranch: main
    secretType: none
    policyDir: "/"
```

### Feature Flags
```python
from google.cloud import firestore

db = firestore.Client()

def is_feature_enabled(feature_name, user_id):
    doc = db.collection('features').document(feature_name).get()
    if not doc.exists:
        return False

    config = doc.to_dict()
    if config.get('enabled_for_all'):
        return True

    return user_id in config.get('enabled_users', [])

# Usage
if is_feature_enabled('new_checkout', user.id):
    return new_checkout_flow()
else:
    return old_checkout_flow()
```

## Best Practices

### CI/CD
1. **Fast Feedback**: Quick build and test cycles
2. **Automated Testing**: Comprehensive test coverage
3. **Security Scanning**: Integrate vulnerability scanning
4. **Artifact Management**: Version and store build artifacts
5. **Deployment Automation**: No manual deployment steps
6. **Rollback Capability**: Easy rollback procedures
7. **Environment Parity**: Dev, staging, prod consistency
8. **Audit Trail**: Log all deployments and changes

### Infrastructure as Code
1. **Version Control**: All infrastructure in Git
2. **Modular Design**: Reusable modules
3. **State Management**: Secure remote state storage
4. **Testing**: Validate before apply
5. **Documentation**: Inline comments and README
6. **Drift Detection**: Regular state reconciliation
7. **Review Process**: PR reviews for infrastructure changes

### Deployment
1. **Gradual Rollout**: Canary or blue-green
2. **Health Checks**: Automated health verification
3. **Monitoring**: Real-time deployment monitoring
4. **Rollback Plans**: Documented rollback procedures
5. **Feature Flags**: Decouple deployment from release
6. **Database Migrations**: Backward-compatible changes
7. **Zero Downtime**: Design for continuous availability

## Common Scenarios

**Scenario**: Multi-environment CI/CD pipeline
**Solution**: Cloud Build with branch-based triggers, separate GKE clusters per environment, Cloud Deploy for progressive delivery

**Scenario**: Secure software supply chain
**Solution**: Binary Authorization, Container Analysis, Artifact Registry vulnerability scanning, attestation-based deployments

**Scenario**: GitOps for Kubernetes
**Solution**: Config Sync or Flux, Git as source of truth, automated reconciliation, PR-based changes

**Scenario**: Database migration in CD pipeline
**Solution**: Separate migration step, backward-compatible changes, rollback-safe migrations, automated testing

## Study Tips

1. **Hands-on practice**: Build complete CI/CD pipelines
2. **Deployment strategies**: Implement canary, blue-green, rolling
3. **IaC tools**: Practice with Terraform and Deployment Manager
4. **Binary Authorization**: Understand attestation-based deployments
5. **Cloud Deploy**: Multi-environment progressive delivery
6. **GitOps**: Config Sync and reconciliation
7. **Security integration**: Scanning and attestation in pipeline

## Key Commands

```bash
# Cloud Build
gcloud builds submit --config=cloudbuild.yaml
gcloud builds triggers create github --repo-name=REPO --branch-pattern="^main$"

# Cloud Deploy
gcloud deploy apply --file=clouddeploy.yaml --region=us-central1
gcloud deploy releases create release-001 --delivery-pipeline=my-pipeline --region=us-central1

# Binary Authorization
gcloud beta container binauthz attestors create ATTESTOR_NAME
gcloud beta container binauthz attestations create --artifact-url=ARTIFACT_URL --attestor=ATTESTOR_NAME

# Terraform
terraform init
terraform plan
terraform apply
terraform destroy
```

## Additional Resources

- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Cloud Deploy](https://cloud.google.com/deploy)
- [Binary Authorization](https://cloud.google.com/binary-authorization/docs)
- [Terraform on GCP](https://cloud.google.com/docs/terraform)
- [GitOps with Config Sync](https://cloud.google.com/kubernetes-engine/docs/add-on/config-sync)

## Key terms

- **Cloud Build** - the Google Cloud service that runs builds defined in steps, each run in a container.
- **Artifact Registry** - the Google Cloud service for storing container images and language packages.
- **Cloud Deploy** - the Google Cloud managed delivery service that promotes releases through a defined pipeline of targets.
- **Binary Authorization** - a deploy-time control that allows only container images that carry required attestations.
- **Blue/green deployment** - a release pattern that runs old and new versions side by side and switches traffic between them.
