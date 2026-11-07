# CI/CD Pipelines and Deployment Strategies

## Overview
Continuous Integration and Continuous Deployment (CI/CD) pipelines automate building, testing, and deploying code. Azure DevOps Pipelines and GitHub Actions provide comprehensive CI/CD capabilities.

## Build Pipelines (Continuous Integration)

### Pipeline Fundamentals

#### YAML Pipelines
```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
    - main
    - develop
  paths:
    exclude:
    - docs/*
    - README.md

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - task: UseDotNet@2
      inputs:
        version: '6.x'
    
    - script: dotnet build --configuration $(buildConfiguration)
      displayName: 'Build project'
    
    - task: DotNetCoreCLI@2
      inputs:
        command: 'test'
        projects: '**/*Tests.csproj'
      displayName: 'Run tests'
    
    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: '$(Build.ArtifactStagingDirectory)'
        artifactName: 'drop'
```

### Build Triggers

#### Continuous Integration (CI) Trigger
```yaml
trigger:
  batch: true  # Batch changes
  branches:
    include:
    - main
    - releases/*
    exclude:
    - experimental/*
```

#### Pull Request Trigger
```yaml
pr:
  branches:
    include:
    - main
  paths:
    exclude:
    - docs/*
```

#### Scheduled Trigger
```yaml
schedules:
- cron: "0 0 * * *"
  displayName: Nightly build
  branches:
    include:
    - main
  always: true  # Run even if no changes
```

### Build Agents

#### Microsoft-Hosted Agents
- **Ubuntu:** ubuntu-latest, ubuntu-20.04
- **Windows:** windows-latest, windows-2022
- **macOS:** macos-latest, macos-12
- **Limitations:**
  - 60 minute timeout (free tier)
  - No admin access to agent
  - Ephemeral (clean for each run)

#### Self-Hosted Agents
```bash
# Download and configure agent
mkdir myagent && cd myagent
wget https://vstsagentpackage.azureedge.net/agent/version/vsts-agent-linux-x64.tar.gz
tar zxvf vsts-agent-linux-x64.tar.gz
./config.sh

# Run as service
sudo ./svc.sh install
sudo ./svc.sh start
```

**Benefits:**
- Persistent environment
- Custom software/tools
- On-premises resource access
- No time limits
- Cost savings for heavy usage

### Testing in Pipelines

#### Unit Tests
```yaml
- task: DotNetCoreCLI@2
  displayName: 'Run unit tests'
  inputs:
    command: 'test'
    projects: '**/*UnitTests.csproj'
    arguments: '--configuration $(buildConfiguration) --collect:"XPlat Code Coverage"'
```

#### Integration Tests
```yaml
- script: |
    docker-compose up -d
    dotnet test IntegrationTests/ --configuration Release
    docker-compose down
  displayName: 'Run integration tests'
```

#### Code Coverage
```yaml
- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: 'Cobertura'
    summaryFileLocation: '$(System.DefaultWorkingDirectory)/**/coverage.cobertura.xml'
```

#### Quality Gates
```yaml
- task: SonarQubeAnalyze@5

- task: SonarQubePublish@5
  inputs:
    pollingTimeoutSec: '300'

# Fail build if quality gate fails
- script: |
    curl -u $(sonarToken): $(sonarUrl)/api/qualitygates/project_status?projectKey=$(projectKey) | jq -e '.projectStatus.status == "OK"'
  displayName: 'Check quality gate'
```

## Release Pipelines (Continuous Deployment)

### Deployment Stages

#### Multi-Stage Pipeline
```yaml
stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: dotnet build

- stage: DeployDev
  dependsOn: Build
  condition: succeeded()
  jobs:
  - deployment: DeployWeb
    environment: 'dev'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            inputs:
              azureSubscription: 'Azure-Dev'
              appName: 'myapp-dev'

- stage: DeployProd
  dependsOn: DeployDev
  condition: succeeded()
  jobs:
  - deployment: DeployWeb
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            inputs:
              azureSubscription: 'Azure-Prod'
              appName: 'myapp-prod'
```

### Deployment Strategies

#### Blue-Green Deployment
```yaml
strategy:
  blueGreen:
    deploy:
      steps:
      - task: AzureWebApp@1
        inputs:
          deployToSlotOrASE: true
          slotName: 'green'
          
    routeTraffic:
      steps:
      - task: AzureAppServiceManage@0
        inputs:
          action: 'Swap Slots'
          sourceSlot: 'green'
```

**Benefits:**
- Zero downtime
- Instant rollback
- Test in production environment

**Cons:**
- Requires 2x infrastructure
- Database migration complexity

#### Canary Deployment
```yaml
strategy:
  canary:
    increments: [10, 25, 50, 100]
    deploy:
      steps:
      - task: AzureTrafficManager@1
        inputs:
          trafficRoutingMethod: 'Weighted'
          weightPercentage: $(strategy.increment)
```

**Benefits:**
- Gradual rollout
- Risk mitigation
- Real user testing

**Cons:**
- Complex traffic management
- Longer deployment time
- Monitoring overhead

#### Rolling Deployment
```yaml
strategy:
  rolling:
    maxParallel: 2
    deploy:
      steps:
      - task: Kubernetes@1
        inputs:
          command: 'apply'
          arguments: '-f deployment.yaml'
```

**Benefits:**
- No downtime
- Gradual update
- Resource efficient

**Cons:**
- Mixed versions during rollout
- Slower than all-at-once

### Deployment Gates

#### Pre-Deployment Approvals
```yaml
environments:
- name: production
  approvals:
  - type: manual
    approvers:
    - user1@company.com
    - user2@company.com
    minApprovers: 2
    timeout: 24h
```

#### Automated Gates
```yaml
gates:
- task: InvokeRESTAPI@1
  displayName: 'Check service health'
  inputs:
    connectionType: 'connectedServiceName'
    serviceConnection: 'HealthCheck'
    method: 'GET'
    urlSuffix: '/health'
    waitForCompletion: 'true'
    successCriteria: 'eq(root.status, "healthy")'

- task: QueryAzureMonitor@1
  displayName: 'Check error rate'
  inputs:
    query: 'requests | where resultCode >= 500'
    threshold: '5'
```

## Infrastructure as Code

### ARM Templates

#### Template Structure
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  "resources": [
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2021-02-01",
      "name": "[variables('appServicePlanName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "S1",
        "tier": "Standard"
      }
    }
  ]
}
```

#### Deployment Task
```yaml
- task: AzureResourceManagerTemplateDeployment@3
  inputs:
    deploymentScope: 'Resource Group'
    azureResourceManagerConnection: 'Azure-Connection'
    subscriptionId: '$(subscriptionId)'
    action: 'Create Or Update Resource Group'
    resourceGroupName: '$(resourceGroupName)'
    location: 'East US'
    templateLocation: 'Linked artifact'
    csmFile: '$(System.DefaultWorkingDirectory)/template.json'
    csmParametersFile: '$(System.DefaultWorkingDirectory)/parameters.json'
    deploymentMode: 'Incremental'
```

### Terraform

#### Configuration
```hcl
# main.tf
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "myapp-rg"
  location = "East US"
}

resource "azurerm_app_service_plan" "asp" {
  name                = "myapp-asp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku {
    tier = "Standard"
    size = "S1"
  }
}
```

#### Pipeline Integration
```yaml
- task: TerraformInstaller@0
  inputs:
    terraformVersion: '1.3.0'

- task: TerraformTaskV2@2
  displayName: 'Terraform init'
  inputs:
    provider: 'azurerm'
    command: 'init'
    backendServiceArm: 'Azure-Connection'
    backendAzureRmResourceGroupName: 'terraform-state-rg'
    backendAzureRmStorageAccountName: 'tfstate'
    backendAzureRmContainerName: 'tfstate'
    backendAzureRmKey: 'terraform.tfstate'

- task: TerraformTaskV2@2
  displayName: 'Terraform plan'
  inputs:
    provider: 'azurerm'
    command: 'plan'
    environmentServiceNameAzureRM: 'Azure-Connection'

- task: TerraformTaskV2@2
  displayName: 'Terraform apply'
  inputs:
    provider: 'azurerm'
    command: 'apply'
    environmentServiceNameAzureRM: 'Azure-Connection'
```

## Container Builds

### Docker Build

#### Dockerfile
```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["MyApp/MyApp.csproj", "MyApp/"]
RUN dotnet restore "MyApp/MyApp.csproj"
COPY . .
WORKDIR "/src/MyApp"
RUN dotnet build "MyApp.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "MyApp.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:6.0
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

#### Multi-Stage Pipeline
```yaml
- task: Docker@2
  displayName: 'Build Docker image'
  inputs:
    command: 'build'
    repository: '$(dockerRegistry)/myapp'
    dockerfile: '**/Dockerfile'
    tags: |
      $(Build.BuildId)
      latest

- task: Docker@2
  displayName: 'Push Docker image'
  inputs:
    command: 'push'
    repository: '$(dockerRegistry)/myapp'
    tags: |
      $(Build.BuildId)
      latest
```

### Kubernetes Deployment

#### Deployment YAML
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
        image: myregistry.azurecr.io/myapp:$(Build.BuildId)
        ports:
        - containerPort: 80
```

#### Deploy to AKS
```yaml
- task: Kubernetes@1
  displayName: 'Deploy to AKS'
  inputs:
    connectionType: 'Azure Resource Manager'
    azureSubscriptionEndpoint: 'Azure-Connection'
    azureResourceGroup: 'aks-rg'
    kubernetesCluster: 'my-aks-cluster'
    command: 'apply'
    arguments: '-f deployment.yaml'
```

## Security in Pipelines

### Secret Management

#### Azure Key Vault Integration
```yaml
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'Azure-Connection'
    KeyVaultName: 'my-keyvault'
    SecretsFilter: '*'
    RunAsPreJob: true

- script: echo "Connection string: $(db-connection-string)"
  displayName: 'Use secret from Key Vault'
```

#### Variable Groups
```yaml
variables:
- group: Production-Secrets
- group: Production-Config
```

### Security Scanning

#### Dependency Scanning
```yaml
- task: DependencyCheck@1
  inputs:
    scanPath: '$(Build.SourcesDirectory)'
    format: 'HTML'
    additionalArguments: '--enableExperimental'
```

#### Container Scanning
```yaml
- task: AzureContainerSecurity@1
  inputs:
    imageNames: '$(dockerRegistry)/myapp:$(Build.BuildId)'
    severityThreshold: 'HIGH'
```

#### SAST (Static Application Security Testing)
```yaml
- task: CredScan@3
  displayName: 'Run Credential Scanner'

- task: PostAnalysis@1
  inputs:
    AllTools: false
    APIScan: false
    BinSkim: false
    CodesignValidation: false
    CredScan: true
    FortifySCA: false
    FxCop: false
    ModernCop: false
    PoliCheck: false
    RoslynAnalyzers: false
    SDLNativeRules: false
    Semmle: false
    TSLint: false
    ToolLogsNotFoundAction: 'Standard'
```

## Pipeline Optimization

### Caching

#### NuGet Package Caching
```yaml
- task: Cache@2
  inputs:
    key: 'nuget | "$(Agent.OS)" | **/packages.lock.json'
    restoreKeys: |
      nuget | "$(Agent.OS)"
    path: $(NUGET_PACKAGES)
  displayName: 'Cache NuGet packages'
```

#### Docker Layer Caching
```yaml
- task: Docker@2
  inputs:
    command: 'build'
    Dockerfile: '**/Dockerfile'
    buildContext: '.'
    tags: '$(Build.BuildId)'
    arguments: '--cache-from=$(dockerRegistry)/myapp:latest'
```

### Parallel Jobs

```yaml
jobs:
- job: TestWindows
  pool:
    vmImage: 'windows-latest'
  steps:
  - script: dotnet test

- job: TestLinux
  pool:
    vmImage: 'ubuntu-latest'
  steps:
  - script: dotnet test

- job: TestMacOS
  pool:
    vmImage: 'macos-latest'
  steps:
  - script: dotnet test
```

## Best Practices

### Pipeline Design
1. **Fail fast:** Run quick tests first
2. **Parallel execution:** Speed up pipelines
3. **Caching:** Reduce build times
4. **Artifacts:** Store build outputs
5. **Idempotent:** Safe to re-run

### Security
1. **Never hardcode secrets:** Use Key Vault
2. **Scan dependencies:** Regular vulnerability checks
3. **Least privilege:** Minimal pipeline permissions
4. **Audit logs:** Track pipeline executions
5. **Secure agents:** Keep agents updated

### Deployment
1. **Environment strategy:** Dev → Staging → Production
2. **Automated testing:** At each stage
3. **Deployment gates:** Automated and manual checks
4. **Rollback plan:** Quick recovery from failures
5. **Monitoring:** Track deployment metrics

## Study Tips

### Key Concepts
- YAML pipeline syntax
- Triggers (CI, PR, scheduled)
- Build agents (hosted vs self-hosted)
- Deployment strategies (blue-green, canary, rolling)
- Infrastructure as Code (ARM, Terraform)
- Container builds and deployments

### Common Scenarios
1. **Automated testing** → Build pipeline with test tasks
2. **Multi-environment deployment** → Multi-stage pipeline
3. **Zero-downtime deployment** → Blue-green strategy
4. **Gradual rollout** → Canary deployment
5. **Infrastructure provisioning** → IaC with ARM/Terraform

### Remember
- CI = Automate build and test
- CD = Automate deployment
- Blue-Green = Swap environments
- Canary = Gradual percentage rollout
- Gates = Automated checks before deployment
- IaC = Infrastructure in version control

## Key terms

- **Azure Pipelines** - the Azure DevOps service that builds, tests and deploys code using YAML or classic pipelines.
- **Self-hosted agent** - a build agent you install and manage on your own machine instead of using a Microsoft-hosted one.
- **Service connection** - a stored, secured link that lets a pipeline authenticate to an external service such as an Azure subscription.
- **Environment** - a pipeline deployment target that supports approvals, checks and deployment history.
- **Deployment slot** - a live staging instance of an App Service that can be swapped with production.
- **Canary release** - a rollout pattern that sends a small share of traffic to the new version before full release.
- **Variable group** - a shared set of variables, optionally linked to Key Vault, that multiple pipelines can use.
