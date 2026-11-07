# DevOps Engineer Professional - Comprehensive Study Notes

## Quick Reference Guide

### CodePipeline CLI Commands

#### Pipeline Management
```bash
# Create pipeline from JSON definition
aws codepipeline create-pipeline --cli-input-json file://pipeline.json

# Get pipeline structure
aws codepipeline get-pipeline --name my-pipeline

# Update pipeline
aws codepipeline update-pipeline --cli-input-json file://pipeline-v2.json

# Start pipeline execution
aws codepipeline start-pipeline-execution --name my-pipeline

# Get pipeline execution details
aws codepipeline get-pipeline-execution \
  --pipeline-name my-pipeline \
  --pipeline-execution-id exec-id

# List pipeline executions
aws codepipeline list-pipeline-executions \
  --pipeline-name my-pipeline --max-items 10

# Enable/disable transitions between stages
aws codepipeline disable-stage-transition \
  --pipeline-name my-pipeline \
  --stage-name Production \
  --transition-type Inbound \
  --reason "Testing in staging"

aws codepipeline enable-stage-transition \
  --pipeline-name my-pipeline \
  --stage-name Production \
  --transition-type Inbound

# Put approval result
aws codepipeline put-approval-result \
  --pipeline-name my-pipeline \
  --stage-name Production \
  --action-name ManualApproval \
  --token $TOKEN \
  --result status=Approved,summary="Looks good"
```

#### Pipeline Artifacts
```bash
# Get artifact details
aws codepipeline get-pipeline-state --name my-pipeline

# List action executions
aws codepipeline list-action-executions \
  --pipeline-name my-pipeline \
  --filter pipelineExecutionId=exec-id
```

### CodeBuild CLI Commands

#### Project Management
```bash
# Create build project
aws codebuild create-project --cli-input-json file://project.json

# Start build
aws codebuild start-build --project-name my-project

# Start build with overrides
aws codebuild start-build \
  --project-name my-project \
  --environment-variables-override \
    name=ENV,value=production,type=PLAINTEXT \
    name=VERSION,value=1.2.3,type=PLAINTEXT

# Get build details
aws codebuild batch-get-builds --ids build-id

# Stop build
aws codebuild stop-build --id build-id

# List builds for project
aws codebuild list-builds-for-project \
  --project-name my-project \
  --sort-order DESCENDING

# Get build logs
aws codebuild batch-get-builds --ids build-id \
  --query 'builds[0].logs.deepLink' --output text
```

#### Build Caching
```bash
# Enable S3 cache in buildspec.yml
cache:
  paths:
    - '/root/.npm/**/*'
    - '/root/.m2/**/*'
    - 'node_modules/**/*'

# Enable local cache (faster for Docker)
cache:
  type: LOCAL
  modes:
    - LOCAL_SOURCE_CACHE
    - LOCAL_DOCKER_LAYER_CACHE
    - LOCAL_CUSTOM_CACHE
```

### CodeDeploy CLI Commands

#### Application and Deployment Group
```bash
# Create application
aws deploy create-application \
  --application-name MyApp \
  --compute-platform Server  # Server, Lambda, or ECS

# Create deployment group
aws deploy create-deployment-group \
  --application-name MyApp \
  --deployment-group-name Production \
  --service-role-arn arn:aws:iam::123456789012:role/CodeDeployRole \
  --ec2-tag-filters Key=Environment,Value=Production,Type=KEY_AND_VALUE \
  --deployment-config-name CodeDeployDefault.OneAtATime \
  --auto-rollback-configuration enabled=true,events=DEPLOYMENT_FAILURE

# Create deployment
aws deploy create-deployment \
  --application-name MyApp \
  --deployment-group-name Production \
  --s3-location bucket=my-bucket,key=app.zip,bundleType=zip \
  --description "Release v1.2.3"

# Get deployment status
aws deploy get-deployment --deployment-id d-XXXXXXXXX

# Stop deployment
aws deploy stop-deployment \
  --deployment-id d-XXXXXXXXX \
  --auto-rollback-enabled
```

#### Deployment Configurations
```bash
# List deployment configs
aws deploy list-deployment-configs

# Create custom deployment config
aws deploy create-deployment-config \
  --deployment-config-name CustomCanary10Percent5Minutes \
  --traffic-routing-config '{
    "type": "TimeBasedCanary",
    "timeBasedCanary": {
      "canaryPercentage": 10,
      "canaryInterval": 5
    }
  }' \
  --compute-platform Lambda
```

### CloudFormation Advanced Commands

#### Stack Operations
```bash
# Create stack with all bells and whistles
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --parameters file://parameters.json \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
  --role-arn arn:aws:iam::123456789012:role/CloudFormationRole \
  --notification-arns arn:aws:sns:us-east-1:123456789012:cfn-notifications \
  --tags Key=Environment,Value=Production Key=Owner,Value=DevOps \
  --on-failure DO_NOTHING  # or ROLLBACK, DELETE

# Create change set for updates
aws cloudformation create-change-set \
  --stack-name my-stack \
  --change-set-name update-v2 \
  --template-body file://template-v2.yaml \
  --parameters file://parameters.json \
  --capabilities CAPABILITY_IAM

# Describe change set
aws cloudformation describe-change-set \
  --stack-name my-stack \
  --change-set-name update-v2

# Execute change set
aws cloudformation execute-change-set \
  --stack-name my-stack \
  --change-set-name update-v2

# Wait for stack operation to complete
aws cloudformation wait stack-create-complete --stack-name my-stack
aws cloudformation wait stack-update-complete --stack-name my-stack

# Cancel update
aws cloudformation cancel-update-stack --stack-name my-stack

# Continue update rollback
aws cloudformation continue-update-rollback \
  --stack-name my-stack \
  --resources-to-skip LogicalResourceId1,LogicalResourceId2
```

#### StackSets (Multi-Account/Region)
```bash
# Create StackSet
aws cloudformation create-stack-set \
  --stack-set-name security-baseline \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --administration-role-arn arn:aws:iam::123456789012:role/AWSCloudFormationStackSetAdministrationRole \
  --execution-role-name AWSCloudFormationStackSetExecutionRole

# Create stack instances
aws cloudformation create-stack-instances \
  --stack-set-name security-baseline \
  --accounts 111111111111 222222222222 \
  --regions us-east-1 us-west-2 \
  --operation-preferences FailureToleranceCount=1,MaxConcurrentCount=2

# Update StackSet
aws cloudformation update-stack-set \
  --stack-set-name security-baseline \
  --template-body file://template-v2.yaml \
  --operation-preferences \
    FailureTolerancePercentage=25,MaxConcurrentPercentage=50

# List stack instances
aws cloudformation list-stack-instances \
  --stack-set-name security-baseline
```

#### Drift Detection
```bash
# Detect drift on entire stack
aws cloudformation detect-stack-drift --stack-name my-stack

# Get drift detection status
DRIFT_ID=$(aws cloudformation detect-stack-drift \
  --stack-name my-stack --query StackDriftDetectionId --output text)
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id $DRIFT_ID

# Get resource drift details
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-stack \
  --stack-resource-drift-status-filters MODIFIED DELETED

# Detect drift on specific resource
aws cloudformation detect-stack-resource-drift \
  --stack-name my-stack \
  --logical-resource-id MyEC2Instance
```

### ECS/Fargate Deployment Commands

#### Service Management
```bash
# Create ECS service with CodeDeploy
aws ecs create-service \
  --cluster production \
  --service-name web-service \
  --task-definition web:1 \
  --desired-count 3 \
  --launch-type FARGATE \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-xxx", "subnet-yyy"],
      "securityGroups": ["sg-xxx"],
      "assignPublicIp": "ENABLED"
    }
  }' \
  --load-balancers '{
    "targetGroupArn": "arn:aws:elasticloadbalancing:...",
    "containerName": "web",
    "containerPort": 80
  }' \
  --deployment-controller type=CODE_DEPLOY

# Update service (rolling update)
aws ecs update-service \
  --cluster production \
  --service web-service \
  --task-definition web:2 \
  --force-new-deployment

# Update service with deployment circuit breaker
aws ecs update-service \
  --cluster production \
  --service web-service \
  --deployment-configuration '{
    "deploymentCircuitBreaker": {
      "enable": true,
      "rollback": true
    },
    "maximumPercent": 200,
    "minimumHealthyPercent": 100
  }'

# Scale service
aws ecs update-service \
  --cluster production \
  --service web-service \
  --desired-count 10
```

#### Task Definition Management
```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-def.json

# Deregister old task definitions
aws ecs list-task-definitions \
  --family-prefix web \
  --status ACTIVE \
  --query 'taskDefinitionArns[0:-3]' \
  | jq -r '.[]' \
  | xargs -I {} aws ecs deregister-task-definition --task-definition {}

# Run one-off task
aws ecs run-task \
  --cluster production \
  --task-definition migration:1 \
  --launch-type FARGATE \
  --network-configuration file://network.json
```

### EKS Deployment Commands

#### Cluster Management
```bash
# Create EKS cluster
aws eks create-cluster \
  --name production \
  --role-arn arn:aws:iam::123456789012:role/EKSClusterRole \
  --resources-vpc-config subnetIds=subnet-xxx,subnet-yyy,securityGroupIds=sg-xxx

# Update kubeconfig
aws eks update-kubeconfig --name production --region us-east-1

# Create node group
aws eks create-nodegroup \
  --cluster-name production \
  --nodegroup-name standard-workers \
  --scaling-config minSize=2,maxSize=10,desiredSize=3 \
  --subnets subnet-xxx subnet-yyy \
  --instance-types t3.medium \
  --node-role arn:aws:iam::123456789012:role/EKSNodeRole

# Update cluster version
aws eks update-cluster-version \
  --name production \
  --kubernetes-version 1.28

# Get cluster info
aws eks describe-cluster --name production
```

#### Kubernetes Deployments
```bash
# Apply manifests
kubectl apply -f deployment.yaml

# Rolling update
kubectl set image deployment/web web=myapp:v2

# Rollback
kubectl rollout undo deployment/web

# Check rollout status
kubectl rollout status deployment/web

# Scale deployment
kubectl scale deployment/web --replicas=10

# Canary deployment (manual)
kubectl apply -f deployment-canary.yaml
kubectl patch service web -p '{"spec":{"selector":{"version":"canary"}}}'

# Blue/Green with service switching
kubectl apply -f deployment-green.yaml
kubectl patch service web -p '{"spec":{"selector":{"version":"green"}}}'
```

### Systems Manager Automation

#### Runbook Execution
```bash
# Execute automation document
aws ssm start-automation-execution \
  --document-name AWS-RestartEC2Instance \
  --parameters "InstanceId=i-xxx"

# Custom automation document
aws ssm start-automation-execution \
  --document-name Custom-DeployApplication \
  --parameters "Environment=production,Version=1.2.3"

# Execute with targets
aws ssm start-automation-execution \
  --document-name AWS-PatchInstanceWithRollback \
  --targets "Key=tag:PatchGroup,Values=WebServers" \
  --max-concurrency 10 \
  --max-errors 2

# Get execution details
aws ssm describe-automation-executions \
  --filters Key=DocumentName,Values=AWS-RestartEC2Instance

# Stop automation execution
aws ssm stop-automation-execution \
  --automation-execution-id exec-id \
  --type Cancel
```

#### State Manager
```bash
# Create association
aws ssm create-association \
  --name AWS-RunPatchBaseline \
  --targets "Key=tag:Environment,Values=Production" \
  --schedule-expression "cron(0 2 ? * SUN *)" \
  --parameters "Operation=Install"

# List associations
aws ssm list-associations \
  --association-filter-list key=Name,value=AWS-RunPatchBaseline

# Delete association
aws ssm delete-association --association-id assoc-id
```

### Lambda Deployment Patterns

#### SAM Deployment
```bash
# Build Lambda function
sam build

# Deploy with guided prompts
sam deploy --guided

# Deploy to specific environment
sam deploy \
  --stack-name my-app-prod \
  --s3-bucket deployment-bucket \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides Environment=production \
  --no-fail-on-empty-changeset

# Deploy with canary deployment
# In template.yaml:
# AutoPublishAlias: live
# DeploymentPreference:
#   Type: Canary10Percent5Minutes
#   Alarms:
#     - !Ref CanaryErrorsAlarm
```

#### Lambda Alias and Versions
```bash
# Publish new version
VERSION=$(aws lambda publish-version \
  --function-name my-function \
  --description "Release 1.2.3" \
  --query Version --output text)

# Update alias to new version
aws lambda update-alias \
  --function-name my-function \
  --name production \
  --function-version $VERSION

# Weighted alias (traffic shifting)
aws lambda update-alias \
  --function-name my-function \
  --name production \
  --routing-config "AdditionalVersionWeights={\"$VERSION\":0.1}"

# Update to 100% after validation
aws lambda update-alias \
  --function-name my-function \
  --name production \
  --function-version $VERSION \
  --routing-config "AdditionalVersionWeights={}"
```

### Container Registry (ECR)

#### Repository Management
```bash
# Create repository
aws ecr create-repository \
  --repository-name myapp \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=KMS

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build and push image
docker build -t myapp:latest .
docker tag myapp:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:latest

# List images
aws ecr list-images --repository-name myapp

# Describe image scan findings
aws ecr describe-image-scan-findings \
  --repository-name myapp \
  --image-id imageTag=latest

# Set lifecycle policy (cleanup old images)
aws ecr put-lifecycle-policy \
  --repository-name myapp \
  --lifecycle-policy-text file://policy.json

# Example policy.json:
{
  "rules": [{
    "rulePriority": 1,
    "description": "Keep last 10 images",
    "selection": {
      "tagStatus": "any",
      "countType": "imageCountMoreThan",
      "countNumber": 10
    },
    "action": { "type": "expire" }
  }]
}
```

### X-Ray Tracing

#### Enable Tracing
```bash
# Enable on Lambda
aws lambda update-function-configuration \
  --function-name my-function \
  --tracing-config Mode=Active

# Enable on API Gateway
aws apigateway update-stage \
  --rest-api-id api-id \
  --stage-name prod \
  --patch-operations op=replace,path=/tracingEnabled,value=true

# Get trace summaries
aws xray get-trace-summaries \
  --start-time $(date -u -d '1 hour ago' +%s) \
  --end-time $(date -u +%s) \
  --filter-expression 'service("my-service") AND error'

# Get trace details
aws xray batch-get-traces --trace-ids trace-id-1 trace-id-2
```

## Common Troubleshooting Scenarios

### Scenario 1: CodePipeline Stuck at Source Stage

**Symptoms**: Pipeline doesn't trigger on new commits

**Troubleshooting Steps**:
1. Check EventBridge rule (for CodeCommit/S3 sources)
2. Verify webhook configuration (for GitHub/Bitbucket)
3. Check IAM permissions for CodePipeline service role
4. Review CloudTrail for permission denied errors
5. Verify source bucket/repository exists and is accessible
6. Check if branch name matches pipeline configuration

```bash
# Check EventBridge rule
aws events list-rules --name-prefix codepipeline

# Describe rule details
aws events describe-rule --name codepipeline-my-pipeline-rule

# List rule targets
aws events list-targets-by-rule --rule codepipeline-my-pipeline-rule

# Test CodeCommit trigger manually
aws codepipeline start-pipeline-execution --name my-pipeline

# Check CloudTrail for errors
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=my-pipeline \
  --max-results 10 \
  --query 'Events[*].[EventTime,EventName,ErrorCode,ErrorMessage]'
```

### Scenario 2: CodeBuild Build Failing

**Symptoms**: Build fails with unclear error messages

**Common Issues**:

**Issue 1: Insufficient Permissions**
```bash
# Build fails accessing S3/ECR/Secrets Manager
# Solution: Update CodeBuild service role

{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "s3:GetObject",
      "s3:PutObject",
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:PutImage",
      "secretsmanager:GetSecretValue"
    ],
    "Resource": "*"
  }]
}
```

**Issue 2: VPC Configuration Problems**
```bash
# Build hangs or times out
# Solution: Check security groups, NAT gateway, VPC endpoints

# Verify VPC endpoints exist
aws ec2 describe-vpc-endpoints \
  --filters "Name=vpc-id,Values=vpc-xxx" \
  --query 'VpcEndpoints[*].[ServiceName,State]'

# Create S3 VPC endpoint if missing
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxx \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-xxx
```

**Issue 3: Docker Build Issues**
```yaml
# buildspec.yml - Use privileged mode for Docker
version: 0.2
phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
  build:
    commands:
      - docker build -t myapp:$CODEBUILD_RESOLVED_SOURCE_VERSION .
      - docker tag myapp:$CODEBUILD_RESOLVED_SOURCE_VERSION $ECR_REGISTRY/myapp:latest
  post_build:
    commands:
      - docker push $ECR_REGISTRY/myapp:latest

# Ensure project has privileged mode enabled
aws codebuild update-project \
  --name my-project \
  --environment "type=LINUX_CONTAINER,image=aws/codebuild/standard:7.0,computeType=BUILD_GENERAL1_SMALL,privilegedMode=true"
```

### Scenario 3: CodeDeploy Deployment Failures

**Symptoms**: Deployment fails or instances marked as failed

**Common Issues**:

**Issue 1: CodeDeploy Agent Not Running**
```bash
# Check agent status on instance
sudo service codedeploy-agent status

# Start agent
sudo service codedeploy-agent start

# Check agent logs
tail -f /var/log/aws/codedeploy-agent/codedeploy-agent.log

# Reinstall agent (Amazon Linux 2)
sudo yum install -y ruby wget
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
```

**Issue 2: AppSpec.yml Errors**
```yaml
# Common mistakes in appspec.yml
version: 0.0
os: linux
files:
  - source: /
    destination: /var/www/html
    # COMMON ERROR: Destination doesn't exist
    # SOLUTION: Create directory in BeforeInstall hook

hooks:
  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 300
      runas: root
      # COMMON ERROR: Script not executable
      # SOLUTION: chmod +x scripts/*.sh before packaging

  ApplicationStart:
    - location: scripts/start_server.sh
      timeout: 300
      runas: root

  ValidateService:
    - location: scripts/validate_service.sh
      timeout: 300
      # IMPORTANT: Must return exit 0 for success
```

**Issue 3: Load Balancer Health Checks Failing**
```bash
# Check target group health
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:...

# Common fixes:
# 1. Ensure security group allows traffic from load balancer
# 2. Application must be ready before ValidateService hook completes
# 3. Health check path must return 200 OK
# 4. Consider increasing deregistration delay

# Update target group health check
aws elbv2 modify-target-group \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 10 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3 \
  --health-check-path /health
```

### Scenario 4: Blue/Green Deployment Issues

**ECS Blue/Green with CodeDeploy**:

```bash
# Deployment stuck or timing out
# Check ECS events
aws ecs describe-services \
  --cluster production \
  --services web-service \
  --query 'services[0].events[0:5]'

# Common issues:
# 1. Replacement task set not passing health checks
# 2. Insufficient capacity to run both task sets
# 3. Security group blocking health check traffic
# 4. Task definition errors

# Check CodeDeploy deployment
aws deploy get-deployment --deployment-id d-XXX

# Force original task set (rollback)
aws deploy stop-deployment \
  --deployment-id d-XXX \
  --auto-rollback-enabled
```

**EC2 Blue/Green Issues**:
```bash
# Issue: Green instances not receiving traffic
# Check:
# 1. Target group association
# 2. Health check status
# 3. Security groups

# Verify blue and green target groups
aws deploy get-deployment-group \
  --application-name MyApp \
  --deployment-group-name Production \
  --query 'deploymentGroupInfo.blueGreenDeploymentConfiguration'

# Manual traffic shifting (if automatic fails)
aws deploy continue-deployment \
  --deployment-id d-XXX \
  --deployment-wait-type READY_WAIT
```

### Scenario 5: CloudFormation Stack Update Failures

**Issue 1: UPDATE_ROLLBACK_FAILED State**
```bash
# Stack stuck in UPDATE_ROLLBACK_FAILED
# Identify failed resources
aws cloudformation describe-stack-events \
  --stack-name my-stack \
  --query 'StackEvents[?ResourceStatus==`UPDATE_FAILED`]'

# Continue update rollback, skipping problematic resources
aws cloudformation continue-update-rollback \
  --stack-name my-stack \
  --resources-to-skip FailedResource1,FailedResource2

# If resources can't be skipped, manual intervention needed:
# 1. Fix resource manually in console
# 2. Or delete resource manually
# 3. Then retry continue-update-rollback
```

**Issue 2: Resource Already Exists**
```bash
# Error: Resource already exists
# Solution 1: Import existing resource
aws cloudformation create-change-set \
  --stack-name my-stack \
  --change-set-name import-resources \
  --change-set-type IMPORT \
  --resources-to-import file://resources.json \
  --template-body file://template.yaml

# resources.json
[{
  "ResourceType": "AWS::S3::Bucket",
  "LogicalResourceId": "MyBucket",
  "ResourceIdentifier": {
    "BucketName": "existing-bucket-name"
  }
}]

# Solution 2: Use DeletionPolicy: Retain and delete stack
# Then recreate with existing resources
```

**Issue 3: Circular Dependencies**
```yaml
# WRONG - Circular dependency
Resources:
  SecurityGroupA:
    Type: AWS::EC2::SecurityGroup
    Properties:
      SecurityGroupIngress:
        - SourceSecurityGroupId: !Ref SecurityGroupB

  SecurityGroupB:
    Type: AWS::EC2::SecurityGroup
    Properties:
      SecurityGroupIngress:
        - SourceSecurityGroupId: !Ref SecurityGroupA

# CORRECT - Use separate ingress rules
Resources:
  SecurityGroupA:
    Type: AWS::EC2::SecurityGroup

  SecurityGroupB:
    Type: AWS::EC2::SecurityGroup

  SecurityGroupAIngress:
    Type: AWS::EC2::SecurityGroupIngress
    Properties:
      GroupId: !Ref SecurityGroupA
      SourceSecurityGroupId: !Ref SecurityGroupB

  SecurityGroupBIngress:
    Type: AWS::EC2::SecurityGroupIngress
    Properties:
      GroupId: !Ref SecurityGroupB
      SourceSecurityGroupId: !Ref SecurityGroupA
```

### Scenario 6: Container Deployment Issues

**ECS Task Won't Start**:
```bash
# Check stopped tasks
aws ecs list-tasks \
  --cluster production \
  --desired-status STOPPED \
  --max-results 10

# Describe stopped task for error details
aws ecs describe-tasks \
  --cluster production \
  --tasks task-arn \
  --query 'tasks[0].[stoppedReason,stopCode,containers[0].reason]'

# Common issues:
# 1. Image pull errors (ECR permissions)
# 2. Container health check failures
# 3. Insufficient memory/CPU
# 4. Port conflicts
# 5. Missing environment variables or secrets

# Check CloudWatch Logs
aws logs tail /ecs/my-app --follow
```

**EKS Pod Issues**:
```bash
# Check pod status
kubectl describe pod pod-name

# Common issues and solutions:

# 1. ImagePullBackOff
# Solution: Check ECR permissions for node IAM role
aws ecr get-login-password | kubectl create secret docker-registry ecr-secret \
  --docker-server=123456789012.dkr.ecr.us-east-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password)

# 2. CrashLoopBackOff
# Check logs
kubectl logs pod-name --previous

# 3. Insufficient resources
# Check node capacity
kubectl describe nodes
kubectl top nodes

# 4. Volume mount issues
# Verify PVC is bound
kubectl get pvc
```

### Scenario 7: Automated Rollback Not Triggering

**CloudWatch Alarms for Rollback**:
```bash
# Verify alarm is in ALARM state
aws cloudwatch describe-alarms \
  --alarm-names deployment-errors-alarm \
  --query 'MetricAlarms[0].[StateValue,StateReason]'

# Check CodeDeploy alarm configuration
aws deploy get-deployment-group \
  --application-name MyApp \
  --deployment-group-name Production \
  --query 'deploymentGroupInfo.alarmConfiguration'

# Ensure alarms are properly linked
{
  "alarmConfiguration": {
    "enabled": true,
    "ignorePollAlarmFailure": false,
    "alarms": [{
      "name": "deployment-errors-alarm"
    }]
  },
  "autoRollbackConfiguration": {
    "enabled": true,
    "events": ["DEPLOYMENT_FAILURE", "DEPLOYMENT_STOP_ON_ALARM"]
  }
}
```

## Exam Tips and Common Traps

### CI/CD Pipeline Design Patterns

**Multi-Account Pipeline Strategy**:

```
Source (Dev Account)
  ↓
Build (Tools Account)
  ↓
Deploy Dev (Dev Account)
  ↓
Manual Approval
  ↓
Deploy Prod (Prod Account)
```

**Key Concepts**:
- Use cross-account IAM roles
- Share artifacts via S3 with encryption
- KMS key policies must allow both accounts
- Use CloudFormation StackSets for consistency

**Common Trap**:
> Q: Pipeline fails when deploying to another account
>
> **CHECK**:
> - S3 bucket policy allows target account
> - KMS key policy grants target account decrypt permissions
> - Target account has trust relationship with pipeline account
> - CloudFormation/CodeDeploy role exists in target account

### Blue/Green vs Canary vs Rolling Deployments

**Blue/Green**:
- Two identical environments
- Instant traffic switch
- Easy rollback (just switch back)
- Higher cost (double resources temporarily)
- Use for: Critical updates, large changes

**Canary**:
- Gradual traffic shift (10% → 50% → 100%)
- Monitor metrics at each step
- Automatic rollback on errors
- Less risk than blue/green
- Use for: Testing new versions with real traffic

**Rolling**:
- Update instances in batches
- Lowest cost (no extra resources)
- Slower deployment
- Mixed versions during deployment
- Use for: Cost-sensitive deployments, non-critical apps

**Common Trap**:
> Q: Need zero-downtime deployment with immediate rollback capability
>
> **WRONG**: Rolling deployment
>
> **CORRECT**: Blue/Green - instant rollback by routing traffic back

### CloudFormation Advanced Patterns

**Nested Stacks vs StackSets**:

| Feature | Nested Stacks | StackSets |
|---------|--------------|-----------|
| Purpose | Modular templates | Multi-account/region |
| Relationship | Parent-child hierarchy | Independent instances |
| Updates | Via parent stack | Independent updates |
| Use Case | Reusable components | Standardization across accounts |

**Custom Resources with Lambda**:
```yaml
# Use when CloudFormation doesn't support a resource
Resources:
  CustomResource:
    Type: Custom::MyCustomResource
    Properties:
      ServiceToken: !GetAtt CustomResourceFunction.Arn
      Parameter1: Value1

  CustomResourceFunction:
    Type: AWS::Lambda::Function
    Properties:
      Handler: index.handler
      Runtime: python3.11
      Code:
        ZipFile: |
          import json
          import cfnresponse

          def handler(event, context):
              try:
                  if event['RequestType'] == 'Create':
                      # Create resource logic
                      physical_id = 'my-resource-id'
                  elif event['RequestType'] == 'Update':
                      # Update resource logic
                      physical_id = event['PhysicalResourceId']
                  elif event['RequestType'] == 'Delete':
                      # Delete resource logic
                      physical_id = event['PhysicalResourceId']

                  cfnresponse.send(event, context, cfnresponse.SUCCESS,
                                   {'Message': 'Success'}, physical_id)
              except Exception as e:
                  cfnresponse.send(event, context, cfnresponse.FAILED,
                                   {'Message': str(e)})
```

**Common Trap**:
> Q: Need to deploy same infrastructure to 50 AWS accounts
>
> **WRONG**: Use nested stacks
>
> **CORRECT**: Use StackSets - designed for multi-account deployments

### Systems Manager Capabilities

**Run Command vs Automation vs State Manager**:

| Feature | Run Command | Automation | State Manager |
|---------|------------|------------|---------------|
| Use Case | Ad-hoc tasks | Complex workflows | Continuous compliance |
| Approval | No | Yes (optional) | No |
| Multi-step | No | Yes | Yes |
| Scheduled | No | Via EventBridge | Built-in |
| Example | Restart service | Patch + validate + rollback | Ensure config compliance |

**Common Trap**:
> Q: Need to ensure all EC2 instances maintain specific configuration
>
> **WRONG**: Run Command with cron job
>
> **CORRECT**: State Manager association - continuously monitors and enforces

### Container Orchestration Best Practices

**ECS vs EKS Decision Matrix**:

| Factor | Choose ECS | Choose EKS |
|--------|-----------|-----------|
| Team Skill | AWS-focused | Kubernetes experience |
| Portability | AWS-only | Multi-cloud/hybrid |
| Complexity | Lower | Higher |
| Cost | Lower | Higher (control plane cost) |
| Features | AWS-native | Kubernetes ecosystem |

**ECS Deployment Strategies**:
```json
// Rolling update (default)
{
  "deploymentConfiguration": {
    "maximumPercent": 200,
    "minimumHealthyPercent": 100
  }
}

// Blue/Green with CodeDeploy
{
  "deploymentController": {
    "type": "CODE_DEPLOY"
  }
}

// Circuit breaker (automatic rollback)
{
  "deploymentConfiguration": {
    "deploymentCircuitBreaker": {
      "enable": true,
      "rollback": true
    }
  }
}
```

**Common Trap**:
> Q: ECS service deployment hangs at DRAINING state
>
> **CHECK**:
> - Connection draining timeout (default 300s)
> - Long-running requests not completing
> - Application not handling SIGTERM gracefully

### Security and Compliance Automation

**Secrets Management Best Practices**:
```bash
# WRONG - Hardcoded secrets
Environment:
  - Name: DB_PASSWORD
    Value: "password123"

# CORRECT - Use Secrets Manager
Environment:
  - Name: DB_PASSWORD
    ValueFrom: "arn:aws:secretsmanager:us-east-1:123:secret:db-pass"

# Enable automatic rotation
aws secretsmanager rotate-secret \
  --secret-id prod/db/password \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123:function:RotateSecret \
  --rotation-rules AutomaticallyAfterDays=30
```

**AWS Config for Compliance**:
```bash
# Enable Config
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123:role/ConfigRole

aws configservice put-delivery-channel \
  --delivery-channel name=default,s3BucketName=config-bucket

# Deploy conformance pack (pre-built compliance rules)
aws configservice put-conformance-pack \
  --conformance-pack-name operational-best-practices-for-pci-dss \
  --template-s3-uri s3://aws-conformance-packs/OpsWorks-PCI-DSS-3.2.1.yaml

# Query compliance status
aws configservice describe-compliance-by-config-rule \
  --compliance-types NON_COMPLIANT
```

**Common Trap**:
> Q: Need to ensure all S3 buckets have encryption enabled
>
> **WRONG**: Lambda function that checks buckets daily
>
> **CORRECT**: AWS Config rule (s3-bucket-server-side-encryption-enabled) with auto-remediation

### Monitoring and Observability

**CloudWatch vs X-Ray vs CloudTrail**:

| Service | Purpose | Use Case |
|---------|---------|----------|
| CloudWatch | Metrics & Logs | System monitoring, alerts |
| X-Ray | Distributed Tracing | Application performance, bottlenecks |
| CloudTrail | API Auditing | Security, compliance, who did what |

**CloudWatch Logs Insights - Essential Queries**:
```sql
-- Find slow API requests
fields @timestamp, statusCode, @duration
| filter @message like /END RequestId/
| stats avg(@duration), max(@duration), pct(@duration, 99) by statusCode

-- Detect error spikes
fields @timestamp, @message
| filter @message like /ERROR/ or @message like /Exception/
| stats count() as error_count by bin(5m)
| sort @timestamp desc

-- Track deployment issues
fields @timestamp, @message
| filter @message like /deployment/
| filter @message like /failed/ or @message like /error/
| stats count() by bin(1m)
```

**Common Trap**:
> Q: API Gateway requests slow but Lambda metrics show fast execution
>
> **CHECK**: Enable X-Ray tracing to see full request flow
> - Likely issue: API Gateway integration timeout, or downstream service latency

## Pre-Exam Checklist

### Domain 1: SDLC Automation (22%)

#### CI/CD Services Mastery
- [ ] **CodePipeline**: Multi-stage orchestration, cross-account deployments
- [ ] **CodeBuild**: Buildspec.yml structure, caching strategies, VPC builds
- [ ] **CodeDeploy**: Deployment strategies (in-place, blue/green), AppSpec hooks
- [ ] **CodeCommit**: Triggers, approvals, pull request workflows
- [ ] **CodeArtifact**: Artifact repositories, upstream repositories

#### Deployment Strategies
- [ ] Blue/Green deployments (EC2, ECS, Lambda)
- [ ] Canary deployments with traffic shifting
- [ ] Rolling deployments with health checks
- [ ] A/B testing patterns
- [ ] Feature flags and gradual rollouts

#### Container Deployments
- [ ] ECS blue/green with CodeDeploy
- [ ] ECS rolling updates with circuit breakers
- [ ] EKS deployments with kubectl
- [ ] ECR lifecycle policies and scanning

#### Lambda Deployments
- [ ] SAM templates and deployment
- [ ] Lambda versions and aliases
- [ ] Weighted alias traffic shifting
- [ ] Automated rollback with CloudWatch alarms

### Domain 2: Configuration Management and IaC (17%)

#### CloudFormation Deep Dive
- [ ] Change sets for safe updates
- [ ] StackSets for multi-account/region
- [ ] Nested stacks for modularity
- [ ] Custom resources with Lambda
- [ ] Drift detection and remediation
- [ ] Stack policies to prevent updates
- [ ] DeletionPolicy and UpdateReplacePolicy

#### AWS CDK
- [ ] CDK constructs (L1, L2, L3)
- [ ] CDK Pipelines for self-mutating pipelines
- [ ] Synthesizing to CloudFormation
- [ ] CDK vs CloudFormation trade-offs

#### Configuration Management
- [ ] Systems Manager Parameter Store vs Secrets Manager
- [ ] Systems Manager State Manager for compliance
- [ ] OpsWorks for Chef/Puppet (retired 26 May 2024; know the Systems Manager replacement)
- [ ] AWS AppConfig for application configuration
- [ ] Service Catalog for governance

### Domain 3: Resilient Cloud Solutions (15%)

#### High Availability Patterns
- [ ] Multi-AZ architectures
- [ ] Multi-region active-active and active-passive
- [ ] Auto Scaling policies (target tracking, step, scheduled)
- [ ] Load balancer health checks and connection draining
- [ ] Route 53 health checks and failover routing

#### Disaster Recovery
- [ ] Backup strategies (automated, cross-region)
- [ ] RTO and RPO requirements
- [ ] DR patterns: backup/restore, pilot light, warm standby, multi-site
- [ ] Database replication (RDS Multi-AZ, Aurora Global Database, DynamoDB Global Tables)
- [ ] S3 cross-region replication and versioning

#### Chaos Engineering
- [ ] AWS Fault Injection Simulator
- [ ] Testing failure scenarios
- [ ] Automated recovery validation

### Domain 4: Monitoring and Logging (15%)

#### CloudWatch Mastery
- [ ] Custom metrics and dimensions
- [ ] Metric math and composite alarms
- [ ] CloudWatch Logs Insights queries
- [ ] CloudWatch Contributor Insights
- [ ] CloudWatch Synthetics for synthetic monitoring
- [ ] Anomaly detection

#### Distributed Tracing
- [ ] X-Ray instrumentation
- [ ] X-Ray service map and analytics
- [ ] Trace analysis and bottleneck identification

#### Log Aggregation
- [ ] Centralized logging patterns
- [ ] Log retention and archiving
- [ ] Real-time log processing with Kinesis
- [ ] Log analysis with Athena

#### Integration with Third-Party Tools
- [ ] Datadog, New Relic, Splunk integration patterns
- [ ] Custom metrics to CloudWatch

### Domain 5: Incident and Event Response (14%)

#### Automated Incident Response
- [ ] EventBridge rules for event-driven automation
- [ ] Lambda for automated remediation
- [ ] Systems Manager Automation for runbooks
- [ ] Step Functions for complex workflows

#### Incident Management
- [ ] Systems Manager OpsCenter
- [ ] SNS for notifications
- [ ] PagerDuty/VictorOps integration
- [ ] Incident tracking and post-mortems

#### Auto-Healing Architectures
- [ ] Health checks and automated recovery
- [ ] Auto Scaling termination policies
- [ ] Self-healing with Lambda and EventBridge
- [ ] Circuit breakers for cascading failures

### Domain 6: Security and Compliance (17%)

#### IAM Best Practices
- [ ] Least privilege policies
- [ ] Service roles and instance profiles
- [ ] Cross-account access patterns
- [ ] Permission boundaries
- [ ] SCP (Service Control Policies) in Organizations

#### Encryption and Secrets
- [ ] KMS key policies and grants
- [ ] Encryption at rest and in transit
- [ ] Secrets Manager rotation
- [ ] Certificate Manager for SSL/TLS

#### Security Automation
- [ ] Security Hub for aggregated findings
- [ ] GuardDuty for threat detection
- [ ] Config rules for compliance as code
- [ ] Automated remediation of security findings
- [ ] Inspector for vulnerability scanning

#### Network Security
- [ ] Security Groups vs NACLs
- [ ] VPC endpoints (Gateway and Interface)
- [ ] AWS WAF and Shield
- [ ] VPC Flow Logs for network monitoring

## Scenario-Based Study Focus

### Cross-Account Pipeline Scenarios
1. Multi-account pipeline with separate dev/test/prod accounts
2. Artifact sharing across accounts with encryption
3. Cross-account CloudFormation deployments with assume roles
4. Security and audit trail requirements

### High-Availability Deployment Scenarios
1. Zero-downtime deployments with blue/green
2. Gradual rollout with canary deployments
3. Multi-region active-active with Route 53
4. Automated rollback on errors

### Compliance and Security Scenarios
1. Automated compliance checking with Config
2. Secrets rotation without downtime
3. Encryption key management across accounts
4. Security incident automated response

### Performance Optimization Scenarios
1. Build optimization with caching
2. Container image optimization and scanning
3. Lambda performance tuning (memory, VPC, provisioned concurrency)
4. Database connection pooling and retry logic

## Final Tips and Exam Strategy

### Question Keywords to Watch

- **"Most automated solution"**: Minimize manual intervention (State Manager, EventBridge)
- **"Zero downtime"**: Blue/green or canary deployments
- **"Immediate rollback"**: Blue/green with instant traffic switch
- **"Gradual rollout"**: Canary deployment with traffic shifting
- **"Multi-account"**: StackSets, cross-account roles, Organizations
- **"Multi-region"**: Route 53, Global Accelerator, DynamoDB Global Tables
- **"Compliance"**: Config rules, Security Hub, CloudTrail
- **"Least privilege"**: Specific IAM policies, resource-level permissions

### Common Exam Patterns

1. **Pipeline design**: Multi-stage with approval gates, artifacts, cross-account
2. **Deployment strategy**: Choose between blue/green, canary, rolling based on requirements
3. **IaC choice**: CloudFormation vs CDK, when to use StackSets
4. **Monitoring**: Which service for which type of monitoring (CloudWatch vs X-Ray vs CloudTrail)
5. **Automated response**: EventBridge + Lambda, Systems Manager Automation
6. **Security**: KMS for encryption, Secrets Manager for rotation, IAM for access control

### Time Management
- 180 minutes, 75 questions = 2.4 minutes per question
- Complex scenarios may take 3-4 minutes
- Flag uncertain questions and return later
- Don't second-guess yourself excessively

### Day Before Exam
- [ ] Review this study guide
- [ ] Take one final practice exam
- [ ] Review AWS service limits and quotas
- [ ] Quick review of buildspec.yml and appspec.yml structures
- [ ] Review CloudFormation intrinsic functions (Ref, GetAtt, Sub, Join, etc.)
- [ ] Sleep well - mental clarity is crucial

### During Exam
- Read the entire question carefully
- Identify keywords (zero downtime, automated, least privilege, etc.)
- Eliminate obviously wrong answers first
- Consider trade-offs (cost vs complexity, speed vs safety)
- Choose best practices over workarounds
- If unsure, pick the most automated, secure, highly available option

### After Passing
- Celebrate your achievement
- Update your LinkedIn and resume
- Consider specialty certifications (Security, Advanced Networking)
- Share knowledge with your team
- Stay current with AWS innovations

Good luck on your DevOps Engineer Professional certification exam!
