# Dependency Management, Security, and Monitoring

## Dependency Management Strategy

### Package Management Tools

#### Azure Artifacts
- **Universal packages:** Generic package format
- **NuGet:** .NET packages
- **npm:** JavaScript/Node.js packages
- **Maven:** Java packages
- **Python:** PyPI packages

**Creating a Feed:**
```bash
# Create feed
az artifacts universal publish \
  --organization https://dev.azure.com/myorg \
  --feed myfeed \
  --name mypackage \
  --version 1.0.0 \
  --description "My package" \
  --path ./package
```

#### GitHub Packages
- Package registry integrated with GitHub
- Supports Docker, npm, Maven, NuGet, RubyGems
- Access control via GitHub permissions

### Package Versioning

#### Semantic Versioning (SemVer)
**Format:** MAJOR.MINOR.PATCH
- **MAJOR:** Breaking changes
- **MINOR:** New features, backward compatible
- **PATCH:** Bug fixes, backward compatible

**Examples:**
- 1.0.0 → 1.0.1 (bug fix)
- 1.0.1 → 1.1.0 (new feature)
- 1.1.0 → 2.0.0 (breaking change)

### Dependency Security

#### Vulnerability Scanning
```yaml
# GitHub Dependabot
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10

# Azure DevOps WhiteSource Bolt
- task: WhiteSource@21
  inputs:
    cwd: '$(System.DefaultWorkingDirectory)'
    projectName: 'MyProject'
```

#### License Compliance
- Scan for incompatible licenses
- Generate software bill of materials (SBOM)
- Policy enforcement (e.g., no GPL in commercial products)

## Application Monitoring

### Azure Monitor

#### Application Insights
**Instrumentation:**
```csharp
// ASP.NET Core
services.AddApplicationInsightsTelemetry(Configuration["ApplicationInsights:InstrumentationKey"]);

// Log custom events
telemetryClient.TrackEvent("UserLoggedIn");
telemetryClient.TrackMetric("OrderValue", orderAmount);
```

**Key Metrics:**
- Request rate and response times
- Failure rates
- Dependency performance
- Custom metrics and events
- User and session counts

#### Log Analytics
```kusto
// Query failed requests
requests
| where success == false
| summarize count() by resultCode
| order by count_ desc

// Query exceptions
exceptions
| where timestamp > ago(1h)
| summarize count() by type
```

### Infrastructure Monitoring

#### Azure Monitor for VMs
- Performance counters
- Process and dependency tracking
- Health monitoring
- Alert on anomalies

#### Container Monitoring
```yaml
# Enable Container Insights for AKS
az aks enable-addons \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --addons monitoring
```

## Continuous Feedback

### Monitoring Dashboards

#### Azure Dashboards
```json
{
  "properties": {
    "lenses": {
      "0": {
        "order": 0,
        "parts": {
          "0": {
            "position": {"x": 0, "y": 0, "rowSpan": 4, "colSpan": 6},
            "metadata": {
              "type": "Extension/Microsoft_OperationsManagementSuite_Workspace/PartType/LogsDashboardPart",
              "settings": {
                "content": {
                  "Query": "requests | summarize count() by bin(timestamp, 5m)"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

#### Power BI Integration
- Connect to Application Insights
- Create custom reports
- Share with stakeholders

### Alerting

#### Metric Alerts
```bash
az monitor metrics alert create \
  --name HighErrorRate \
  --resource-group myResourceGroup \
  --scopes /subscriptions/{subscription-id}/resourceGroups/myResourceGroup/providers/Microsoft.Web/sites/myapp \
  --condition "avg requests/failed > 10" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action-group myActionGroup
```

#### Log Alerts
```kusto
exceptions
| where timestamp > ago(5m)
| where type == "System.OutOfMemoryException"
| count
```

### User Feedback Collection

#### Application Feedback
- In-app feedback forms
- User satisfaction surveys
- Feature requests tracking
- Bug reports

#### Integration
```yaml
# Send feedback to Azure DevOps
- task: CreateWorkItem@1
  inputs:
    workItemType: 'Bug'
    title: '$(feedbackTitle)'
    assignedTo: '$(teamEmail)'
    areaPath: 'MyProject\Feedback'
    fieldMappings: |
      Description=$(feedbackDescription)
      Priority=2
```

## Best Practices

### Dependency Management
1. **Pin versions** in production
2. **Regular updates** for security
3. **Test updates** before production
4. **Use private feeds** for internal packages
5. **Scan for vulnerabilities** automatically

### Monitoring
1. **Monitor key metrics:** Error rate, latency, saturation
2. **Set meaningful alerts:** Avoid alert fatigue
3. **Track business metrics:** Revenue, user engagement
4. **Correlate logs and metrics**
5. **Regular dashboard reviews**

### Continuous Improvement
1. **Post-incident reviews:** Learn from failures
2. **Track MTTR** (Mean Time To Recovery)
3. **Automate remediation** where possible
4. **Regular performance reviews**
5. **Iterate based on feedback**

## Study Tips

### Key Concepts
- Package management strategies
- Semantic versioning
- Vulnerability scanning
- Application Insights capabilities
- Alert configuration
- Dashboard creation

### Common Scenarios
1. **Security vulnerability found** → Automated scanning and PR
2. **High error rate** → Metric alert triggers
3. **Performance degradation** → Application Insights investigation
4. **User feedback** → Create work items automatically

### Remember
- Azure Artifacts = Package management
- Application Insights = App monitoring
- Log Analytics = Log querying
- Alerts = Proactive notifications
- Dashboards = Visualize metrics
- Continuous feedback = Improve based on data

## Key terms

- **Azure Artifacts** - the Azure DevOps service for hosting NuGet, npm, Maven and Python packages in feeds.
- **Application Insights** - the Azure Monitor feature that collects application telemetry such as requests, dependencies and exceptions.
- **Log Analytics workspace** - the store where Azure Monitor collects log data that you query with KQL.
- **KQL** - the Kusto Query Language used to query logs in Azure Monitor.
