# IBM Cloud Site Reliability Engineer (SRE) - RETIRED

## Important Notice

**This exam was retired: IBM withdrew the certification on December 31, 2025, and the credential expired on September 30, 2026** ([IBM certification page](https://www.ibm.com/training/certification/ibm-certified-associate-sre-cloud-v2-C9005500), read 2026-11-22). This guide now describes a withdrawn exam and is kept as IBM Cloud background reading; there is no exam to book. The page read is IBM Certified Associate SRE - Cloud v2 (exam C1000-169); IBM's Professional Developer v6 PLUS Professional SRE v2 pairing is also listed as withdrawn.

The IBM Cloud Site Reliability Engineer certification validates skills in operating, monitoring, and ensuring the reliability of production systems on IBM Cloud. This certification demonstrates expertise in implementing SRE practices, automation, observability, incident management, and performance optimization using IBM Cloud services.

## 📋 Quick Links

- [**Fact Sheet**](fact-sheet.md) - Exam logistics and objectives
- [**Practice Plan**](practice-plan.md) - Structured study schedule

## 📚 Study Materials

### Core Notes
- [Infrastructure Operations](notes/01-infrastructure-operations.md)
- [Monitoring Observability](notes/02-monitoring-observability.md)
- [Reliability Performance](notes/03-reliability-performance.md)
## 🎯 Exam Details (IBM page, read 2026-11-22)

- **Certification**: IBM Certified Professional SRE - Cloud v2 (page not read; see notice)
- **Exam Code**: Not confirmed. IBM's Associate SRE - Cloud v2 page gives C1000-169; the Professional SRE v2 page was not read. The C1000-173 and C1000-174 codes this guide used are unsourced
- **Status**: Withdrawn 2025-12-31; credential expired 2026-09-30
- **Duration**: 90 minutes
- **Number of Questions**: 65 (Associate SRE v2)
- **Passing Score**: 45 of 65 correct (Associate SRE v2)
- **Cost, validity, languages, delivery**: Not stated on the IBM page read

## 📖 Exam Domains

### 1. SRE Fundamentals and Culture (15%)

#### SRE Principles
- **Google SRE Practices**
  - DevOps culture and collaboration
  - Share ownership of production
  - Error budgets and risk tolerance
  - Blameless postmortems
  - Toil reduction through automation
  - 50/50 rule (50% ops, 50% engineering)

- **Service Level Objectives (SLOs)**
  - Define Service Level Indicators (SLIs)
  - Set Service Level Objectives (SLOs)
  - Communicate Service Level Agreements (SLAs)
  - Error budget calculation and tracking
  - Error budget policies

- **Reliability Targets**
  - Balance reliability with feature velocity
  - "Everything fails all the time" mindset
  - Design for failure
  - Graceful degradation
  - Progressive rollouts

#### SRE Culture
- **Collaboration**
  - Dev and Ops partnership
  - Shared on-call responsibilities
  - Runbook development and maintenance
  - Knowledge sharing and documentation

- **Continuous Improvement**
  - Postmortem culture (blameless)
  - Actionable postmortem items
  - SLO review and adjustment
  - Toil tracking and reduction

### 2. Observability and Monitoring (25%)

#### Monitoring Strategy
- **IBM Cloud Monitoring**
  - Platform metrics (automatic collection)
  - Custom application metrics
  - Prometheus integration
  - Metric retention and aggregation
  - Dashboards for visibility
  - Alert configuration and routing

- **Key Metrics**
  - Golden signals (latency, traffic, errors, saturation)
  - USE method (Utilization, Saturation, Errors)
  - RED method (Rate, Errors, Duration)
  - Infrastructure metrics (CPU, memory, disk, network)
  - Application metrics (request rate, response time, error rate)

#### Logging and Analysis
- **IBM Log Analysis**
  - Centralized log aggregation
  - Log shipping from multiple sources
  - Structured logging (JSON)
  - Log search and filtering
  - Log-based alerts
  - Log retention and archival

- **Log Analysis Techniques**
  - Identify error patterns
  - Correlation of logs across services
  - Performance analysis from logs
  - Security event detection
  - Compliance logging

#### Distributed Tracing
- **IBM Cloud Instana**
  - Automatic distributed tracing
  - Application topology discovery
  - Request tracing across microservices
  - Performance bottleneck identification
  - Anomaly detection with AI

- **OpenTelemetry**
  - Instrument applications for tracing
  - Trace context propagation
  - Span attributes and events
  - Integration with monitoring backends

### 3. Incident Management and Response (20%)

#### Incident Detection
- **Alerting Best Practices**
  - Actionable alerts (avoid alert fatigue)
  - Severity levels and escalation
  - Alert routing (PagerDuty, Slack, email)
  - Silencing and maintenance windows
  - Alert aggregation and deduplication

- **On-Call Management**
  - On-call rotation schedules
  - Escalation policies
  - Handoff procedures
  - On-call compensation and limits

#### Incident Response
- **Response Procedures**
  - Incident declaration and severity assessment
  - Incident commander role
  - Communication during incidents (status pages)
  - Triage and diagnosis
  - Mitigation strategies
  - Resolution and recovery

- **Runbooks and Playbooks**
  - Document common incidents
  - Step-by-step resolution procedures
  - Diagnostic commands and tools
  - Escalation criteria
  - Rollback procedures

#### Postmortems
- **Blameless Postmortems**
  - Timeline of events
  - Root cause analysis (5 Whys, fishbone)
  - What went well, what didn't
  - Action items with owners
  - Share learnings across organization

- **Continuous Improvement**
  - Track action item completion
  - Update runbooks based on incidents
  - Improve monitoring and alerting
  - Reduce toil through automation

### 4. Automation and Infrastructure as Code (20%)

#### Infrastructure as Code
- **IBM Cloud Schematics (Terraform)**
  - Define infrastructure as code
  - Workspaces for state management
  - Version control for IaC
  - Plan, apply, destroy workflows
  - Drift detection and remediation

- **GitOps Practices**
  - Git as single source of truth
  - Declarative infrastructure
  - Automated reconciliation
  - ArgoCD for Kubernetes GitOps

#### CI/CD Automation
- **IBM Continuous Delivery**
  - Build pipelines for automation
  - Deployment automation
  - Rollback strategies
  - Deployment strategies (blue-green, canary, rolling)
  - Quality gates and testing

- **Tekton Pipelines**
  - Cloud-native CI/CD
  - Reusable tasks and pipelines
  - Triggers for automation
  - Integration with Kubernetes and OpenShift

#### Operational Automation
- **Runbook Automation**
  - Automate repetitive tasks
  - Self-healing systems
  - Auto-remediation with Functions
  - Scheduled maintenance tasks

- **Event-Driven Automation**
  - IBM Cloud Functions for automation
  - Event triggers (alarms, logs, schedules)
  - Automated scaling and remediation
  - Integration with monitoring and alerting

### 5. Kubernetes and Container Operations (15%)

#### Kubernetes Cluster Operations
- **IBM Kubernetes Service (IKS)**
  - Cluster lifecycle management
  - Worker node management and upgrades
  - Add-ons and integrations
  - Cluster autoscaling
  - Resource quotas and limits

- **Red Hat OpenShift Operations**
  - Cluster administration
  - Operator lifecycle management
  - Machine config and node management
  - Monitoring and logging (built-in)
  - OpenShift-specific features

#### Container Reliability
- **Pod Health and Resilience**
  - Liveness and readiness probes
  - Startup probes for slow-starting containers
  - Resource requests and limits
  - Pod disruption budgets
  - Pod anti-affinity for HA

- **Scaling Strategies**
  - Horizontal Pod Autoscaler (HPA)
  - Vertical Pod Autoscaler (VPA)
  - Cluster Autoscaler
  - KEDA for event-driven autoscaling

#### Service Mesh
- **Istio on Kubernetes**
  - Traffic management and routing
  - Circuit breaking and retries
  - Observability (metrics, logs, traces)
  - Security (mTLS, authorization)
  - Chaos engineering with fault injection

### 6. Performance Optimization and Capacity Planning (10%)

#### Performance Tuning
- **Application Performance**
  - Identify bottlenecks with Instana
  - Database query optimization
  - Caching strategies (Redis)
  - CDN and edge caching (CIS)
  - Asynchronous processing patterns

- **Infrastructure Optimization**
  - Right-sizing compute resources
  - Storage performance tuning
  - Network optimization
  - Load balancer tuning
  - Auto-scaling configuration

#### Capacity Planning
- **Demand Forecasting**
  - Historical usage analysis
  - Traffic patterns and trends
  - Seasonal variations
  - Growth projections

- **Resource Planning**
  - Compute capacity planning
  - Storage capacity planning
  - Network bandwidth planning
  - Cost modeling and budgeting
  - Reserved capacity vs on-demand

### 7. Reliability and Resilience Engineering (10%)

#### High Availability
- **Multi-Zone Architecture**
  - Deploy across availability zones
  - Load balancing across zones
  - Database replication and failover
  - Stateless application design

- **Disaster Recovery**
  - RTO and RPO requirements
  - Backup strategies and automation
  - Cross-region replication
  - DR testing and validation
  - Failover automation

#### Resilience Patterns
- **Reliability Patterns**
  - Circuit breaker pattern
  - Retry with exponential backoff
  - Bulkhead pattern for isolation
  - Timeout and deadline propagation
  - Graceful degradation

- **Chaos Engineering**
  - Deliberately inject failures
  - Test system resilience
  - Identify weaknesses before production
  - Game days and disaster recovery drills
  - Chaos tools (Litmus, Chaos Mesh)

### 8. Cost Optimization and FinOps (5%)

#### Cost Management
- **Cost Monitoring**
  - Track resource costs
  - Tag-based cost allocation
  - Budget alerts and thresholds
  - Cost anomaly detection

- **Optimization Strategies**
  - Right-size compute resources
  - Use reserved capacity where appropriate
  - Shutdown non-production environments
  - Object Storage lifecycle policies
  - Autoscaling to match demand

#### FinOps Practices
- **Cost Accountability**
  - Chargeback and showback models
  - Cost per service or team
  - Cost visibility and transparency
  - Cost optimization culture

## 🎓 Prerequisites & Recommended Experience

### Prerequisites
- **IBM Cloud Advocate** or **Developer** - Recommended foundation
- Strong understanding of Linux/Unix administration
- Experience with cloud operations
- Knowledge of DevOps and CI/CD
- Familiarity with monitoring and logging

### Recommended Experience
- 2-3 years in operations or SRE role
- Hands-on with Kubernetes or OpenShift
- Experience with incident management
- Understanding of performance optimization
- Familiarity with IaC (Terraform)

### Technical Skills
- Operate and maintain production systems on IBM Cloud
- Implement comprehensive observability
- Respond to and resolve incidents effectively
- Automate operational tasks
- Optimize performance and capacity
- Design for high availability and resilience
- Apply SRE best practices

## Study Strategy

### Recommended Timeline: 10-12 Weeks

**Weeks 1-2: SRE Fundamentals and Observability**
- SRE principles, SLIs, SLOs, SLAs
- Error budgets and policies
- Monitoring with IBM Cloud Monitoring
- Logging with IBM Log Analysis
- Hands-on: Set up monitoring and logging, define SLOs

**Weeks 3-4: Incident Management**
- Alerting best practices
- On-call management
- Incident response procedures
- Blameless postmortems
- Hands-on: Configure alerts, practice incident response

**Weeks 5-6: Automation and IaC**
- Infrastructure as Code with Schematics
- CI/CD automation with Continuous Delivery
- Runbook automation
- Event-driven automation with Functions
- Hands-on: Implement IaC, automate deployments

**Weeks 7-8: Kubernetes and Container Operations**
- IKS/OpenShift cluster operations
- Pod health and resilience
- Autoscaling strategies
- Service mesh (Istio)
- Hands-on: Operate Kubernetes clusters, implement autoscaling

**Weeks 9-10: Performance, Resilience, and Cost**
- Performance tuning and optimization
- Capacity planning
- High availability and DR
- Chaos engineering
- Cost optimization
- Hands-on: Performance testing, DR drills, cost optimization

**Weeks 11-12: Practice and Review**
- SRE scenarios and case studies
- Practice exams (multiple attempts)
- Review weak areas
- Final hands-on labs and simulations

### Essential Hands-on Labs
- Set up comprehensive monitoring with dashboards and alerts
- Configure centralized logging and create log-based alerts
- Implement distributed tracing with Instana
- Practice incident response with simulated outages
- Automate infrastructure deployment with Schematics
- Build CI/CD pipeline with automated testing and deployment
- Operate Kubernetes cluster (upgrades, scaling, troubleshooting)
- Implement autoscaling (HPA, cluster autoscaler)
- Conduct chaos engineering experiments
- Perform disaster recovery drill
- Optimize costs with rightsizing and lifecycle policies

## 📚 Study Resources

### Official IBM Resources
- **[IBM Cloud Documentation](https://cloud.ibm.com/docs)** - All service documentation
- **[IBM Cloud Architecture Center](https://www.ibm.com/cloud/architecture)** - SRE reference architectures
- **[IBM Cloud Training](https://www.ibm.com/training/cloud)** - Official learning paths
- **[IBM Developer](https://developer.ibm.com/)** - Tutorials and patterns
- **[IBM Cloud Lite Account](https://www.ibm.com/cloud/free)** + paid resources

### Recommended Materials
1. **Google SRE Books** (FREE online) - "Site Reliability Engineering" and "The Site Reliability Workbook"
2. **IBM Training**: Official SRE course
3. **Practice Tests**: IBM official practice exam
4. **Hands-on Labs**: Extensive operational practice

### Industry Resources
- **Google SRE Books**: sre.google (essential reading!)
- **The Phoenix Project**: DevOps novel
- **The DevOps Handbook**: Practical DevOps guidance
- **CNCF SRE Resources**: Cloud-native SRE practices

## Exam Tips

### Question Strategy
- Scenario-based operational questions
- Focus on SRE best practices
- Consider reliability, automation, and toil reduction
- Multiple approaches may work - choose BEST
- Think about scalability and automation

### Common Question Themes
- SLO definition and error budget calculation
- Monitoring and alerting configuration
- Incident response procedures
- Blameless postmortem practices
- Infrastructure as Code best practices
- Kubernetes operations and troubleshooting
- Autoscaling strategies
- High availability and DR design
- Performance optimization techniques
- Cost optimization strategies

### SRE Best Practices
- **Embrace risk**: Balance reliability with innovation
- **Eliminate toil**: Automate repetitive tasks
- **Monitor everything**: Comprehensive observability
- **Blameless culture**: Learn from failures
- **Error budgets**: Data-driven risk decisions
- **Progressive rollouts**: Reduce blast radius
- **Design for failure**: Everything fails eventually
- **Continuous improvement**: Iterate based on learnings

### Time Management
- 90 minutes for 60 questions = 1.5 minutes per question
- Operational scenarios may require more analysis
- Flag uncertain questions for review
- Leave 15 minutes for final review

## 📈 Success Criteria

- Apply SRE principles and practices
- Implement comprehensive observability
- Respond effectively to incidents
- Automate operational tasks and eliminate toil
- Operate Kubernetes/OpenShift clusters reliably
- Optimize performance and capacity
- Design for high availability and resilience
- Manage costs with FinOps practices
- Foster SRE culture and continuous improvement

## Career Impact

### Professional Recognition
- Demonstrates SRE expertise on IBM Cloud
- Valued by organizations adopting SRE practices
- Competitive advantage in DevOps/SRE job market
- Foundation for SRE leadership roles

### Career Roles
- **Site Reliability Engineer (SRE)**
- **DevOps Engineer**
- **Platform Engineer**
- **Cloud Operations Engineer**
- **Production Engineer**
- **Infrastructure Engineer**

### Next Steps
- **Google Professional Cloud DevOps Engineer** - Multi-cloud SRE
- **Certified Kubernetes Administrator (CKA)** - Advanced Kubernetes
- **HashiCorp Certified: Terraform Associate** - IaC expertise
- **AWS Certified DevOps Engineer - Professional** - Multi-cloud DevOps

---

**Build and operate reliable, scalable systems on IBM Cloud!** ⚙️
