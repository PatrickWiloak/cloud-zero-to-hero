# IBM Certified Application Developer - Cloud Platform v4 - RETIRED

## Important Notice

**This exam was retired: IBM withdrew the certification on December 31, 2025, and the credential expired on September 30, 2026** ([IBM certification page](https://www.ibm.com/training/certification/ibm-certified-professional-developer-cloud-v6-C9005400), read 2026-11-22). This guide now describes a withdrawn exam and is kept as IBM Cloud background reading; there is no exam to book. This guide's earlier code C1000-171 is not the code on IBM's page.

The IBM Cloud Application Developer certification validates skills in developing, deploying, and managing cloud-native applications on IBM Cloud. This certification demonstrates proficiency in using IBM Cloud development services, APIs, DevOps tools, and best practices for building modern applications.

## 📋 Quick Links

- [**Fact Sheet**](fact-sheet.md) - Exam logistics and objectives
- [**Practice Plan**](practice-plan.md) - Structured study schedule

## 📚 Study Materials

### Core Notes
- [Cloud Native Development](notes/01-cloud-native-development.md)
- [Application Deployment Integration](notes/02-application-deployment-integration.md)
- [Data AI Services Monitoring](notes/03-data-ai-services-monitoring.md)
## 🎯 Exam Details (IBM page, read 2026-11-22)

- **Certification**: IBM Certified Professional Developer - Cloud v6
- **Exam Code**: C1000-166 (IBM Cloud Professional Developer v6)
- **Status**: Withdrawn 2025-12-31; credential expired 2026-09-30
- **Duration**: 90 minutes
- **Number of Questions**: 65
- **Passing Score**: 40 of 65 correct
- **Cost, validity, languages, delivery**: Not stated on the IBM page read

## 📖 Exam Domains

### 1. Cloud Native Application Development (25%)

#### 12-Factor App Methodology
- **Principles**
  - Codebase: One codebase tracked in version control
  - Dependencies: Explicitly declare and isolate dependencies
  - Config: Store config in the environment
  - Backing services: Treat backing services as attached resources
  - Build, release, run: Strictly separate build and run stages
  - Processes: Execute the app as stateless processes
  - Port binding: Export services via port binding
  - Concurrency: Scale out via the process model
  - Disposability: Fast startup and graceful shutdown
  - Dev/prod parity: Keep development, staging, and production similar
  - Logs: Treat logs as event streams
  - Admin processes: Run admin tasks as one-off processes

#### Microservices Architecture
- **Design Patterns**
  - Service decomposition by business capability
  - API Gateway pattern
  - Database per service
  - Event-driven communication
  - Circuit breaker for resilience
  - Service discovery
  - Distributed tracing

- **Communication Patterns**
  - Synchronous (REST, gRPC)
  - Asynchronous (messaging, events)
  - Request-response vs pub-sub
  - Saga pattern for distributed transactions

#### Application Design
- **Stateless Applications**
  - Session state externalization
  - Shared-nothing architecture
  - Horizontal scaling
  - Load balancing considerations

- **RESTful API Design**
  - Resource modeling
  - HTTP methods (GET, POST, PUT, DELETE, PATCH)
  - Status codes and error handling
  - Versioning strategies
  - Pagination and filtering
  - HATEOAS principles

### 2. Application Deployment Platforms (20%)

#### IBM Code Engine
- **Serverless Container Platform**
  - Deploy containerized apps without managing infrastructure
  - Auto-scaling (scale to zero)
  - Event-driven workloads
  - Build from source code or Dockerfile
  - Job execution for batch workloads

- **Code Engine Components**
  - Projects for resource isolation
  - Applications (long-running services)
  - Jobs (run-to-completion workloads)
  - Subscriptions (event triggers)
  - Configmaps and secrets

#### IBM Cloud Functions
- **Serverless Functions (OpenWhisk)**
  - Function-as-a-Service (FaaS)
  - Supported runtimes (Node.js, Python, Go, Java, PHP, Ruby, .NET)
  - Actions, triggers, and rules
  - Sequences and compositions
  - Web actions for HTTP endpoints

- **Event-Driven Development**
  - Trigger types (periodic, manual, event-based)
  - Integration with IBM Cloud services
  - Asynchronous invocation
  - Feed implementations

#### Cloud Foundry

> **Retired platform.** IBM Cloud Foundry is no longer offered; IBM publishes a [Cloud Foundry to Code Engine migration guide](https://cloud.ibm.com/docs/codeengine?topic=codeengine-migrate-cf-ce-getstart). Secondary sources give 30 November 2022 (no new apps) and 1 June 2023 (end of support, instances deleted); no IBM page stating those dates could be read on 2026-11-22. Learn it for older exam items; deploy new apps on Code Engine or Red Hat OpenShift.

- **Platform as a Service**
  - Buildpacks for multiple languages
  - cf CLI for deployment
  - Services binding
  - Manifest files (manifest.yml)
  - Routes and domains
  - Auto-scaling and health management

#### Kubernetes Service (IKS)
- **Container Orchestration**
  - Deploy applications with Deployments
  - Services for networking
  - ConfigMaps and Secrets for configuration
  - Persistent storage with PVCs
  - Ingress for external access
  - Horizontal Pod Autoscaler

#### Red Hat OpenShift on IBM Cloud
- **Enterprise Kubernetes**
  - Source-to-Image (S2I) builds
  - BuildConfigs and ImageStreams
  - DeploymentConfigs
  - Routes for external access
  - Operators for application management
  - OpenShift Pipelines (Tekton)

### 3. DevOps and Continuous Delivery (15%)

#### IBM Continuous Delivery
- **Toolchains**
  - Toolchain templates
  - Tool integrations (Git, Jenkins, Slack, PagerDuty)
  - Delivery Pipeline (Classic and Tekton)
  - DevOps Insights for quality gates

- **Delivery Pipelines**
  - Pipeline stages (build, test, deploy)
  - Jobs within stages
  - Environment properties
  - Deployment strategies (rolling, blue-green, canary)
  - Integration with Kubernetes and OpenShift

- **Tekton Pipelines**
  - Tasks and TaskRuns
  - Pipelines and PipelineRuns
  - Triggers for automation
  - Workspaces for data sharing
  - Pipeline resources

#### Version Control and Collaboration
- **Git Repositories**
  - Git Repos and Issue Tracking service
  - GitHub, GitLab integration
  - Branching strategies (GitFlow, trunk-based)
  - Pull requests and code reviews

#### Infrastructure as Code
- **Schematics (Terraform)**
  - Workspaces for Terraform state
  - Terraform templates
  - Plan, apply, destroy operations
  - Variable management
  - Remote state management

### 4. Data Services and Storage (15%)

#### Database Services
- **IBM Cloud Databases**
  - Databases for PostgreSQL
  - Databases for MongoDB
  - Databases for Redis
  - Databases for MySQL
  - Databases for Elasticsearch
  - High availability and backups

- **Cloudant**
  - NoSQL JSON document database
  - HTTP API for CRUD operations
  - MapReduce views for queries
  - Mango queries (declarative JSON)
  - Replication and conflict resolution
  - Change feed for real-time updates

- **Db2 on Cloud**
  - Managed relational database
  - SQL access and performance
  - JDBC/ODBC connectivity
  - Backup and recovery

#### Object Storage
- **Cloud Object Storage**
  - S3-compatible API
  - SDKs for multiple languages
  - Storage classes (Standard, Vault, Cold Vault)
  - Bucket lifecycle policies
  - Pre-signed URLs
  - Server-side encryption

#### Application Data Patterns
- **Caching**
  - Databases for Redis as cache
  - Session store patterns
  - Cache-aside, write-through strategies

- **File Upload/Download**
  - Direct upload to Object Storage
  - Pre-signed URLs for secure access
  - Multipart uploads for large files

### 5. Integration and Messaging (10%)

#### API Connect
- **API Management**
  - API creation and publishing
  - Plans and subscriptions
  - Rate limiting and quotas
  - API security (OAuth, API keys)
  - Developer portal

#### Event Streams (Kafka)
- **Messaging Platform**
  - Topics and partitions
  - Producers and consumers
  - Consumer groups
  - Kafka Connect for integration
  - Schema Registry

#### IBM MQ on Cloud
- **Message Queuing**
  - Point-to-point messaging
  - Publish-subscribe
  - Guaranteed delivery
  - Transaction support

#### App Connect
- **Integration Platform**
  - Connect applications and data
  - Pre-built connectors
  - Integration flows
  - Event-driven integrations

### 6. Security and Authentication (10%)

#### Identity and Access Management
- **IBM Cloud IAM**
  - Service IDs for application identity
  - API keys for authentication
  - Trusted profiles for compute resources
  - Access policies and roles
  - Resource groups and access groups

#### App ID
- **Application Authentication**
  - User authentication and authorization
  - Social identity providers (Google, Facebook)
  - Enterprise SSO (SAML)
  - Custom authentication
  - User profiles and attributes
  - Multi-factor authentication

#### Secrets Management
- **Key Protect**
  - Encryption key management
  - Wrap and unwrap keys
  - Root keys and data encryption keys
  - Envelope encryption
  - Integration with IBM Cloud services

- **Secrets Manager**
  - Store and manage secrets
  - Secret rotation
  - IAM credentials, certificates, arbitrary secrets
  - Dynamic secrets for databases

#### Application Security
- **Best Practices**
  - Secure credential storage (no hardcoding)
  - Use environment variables for config
  - HTTPS/TLS for all communication
  - Input validation and sanitization
  - OWASP Top 10 awareness
  - Container image scanning

### 7. Monitoring and Logging (5%)

#### IBM Cloud Monitoring
- **Monitoring Service**
  - Metrics collection and visualization
  - Dashboards and alerts
  - Platform metrics (automatic)
  - Custom metrics (application-specific)
  - Integration with Prometheus

#### IBM Log Analysis
- **Centralized Logging**
  - Log aggregation
  - Search and filtering
  - Log views and alerts
  - Retention policies
  - Integration with platforms (Kubernetes, Cloud Foundry)

#### Application Performance Monitoring
- **IBM Cloud Instana**
  - Distributed tracing
  - Application topology discovery
  - Performance metrics
  - Anomaly detection
  - Integration with Kubernetes and OpenShift

## 🎓 Prerequisites & Recommended Experience

### Prerequisites
- **IBM Cloud Advocate** - Recommended foundation
- Programming experience in at least one language
- Understanding of REST APIs and HTTP
- Basic knowledge of containerization
- Familiarity with version control (Git)

### Recommended Experience
- 1-2 years developing cloud applications
- Hands-on with IBM Cloud services
- Experience with microservices or serverless
- Basic DevOps and CI/CD knowledge
- Understanding of databases and storage

### Technical Skills
- Develop cloud-native applications
- Deploy applications to IBM Cloud platforms
- Implement DevOps and CI/CD pipelines
- Integrate with IBM Cloud data services
- Implement authentication and authorization
- Monitor and troubleshoot applications
- Apply security best practices

## Study Strategy

### Recommended Timeline: 8-10 Weeks

**Weeks 1-2: Cloud Native Fundamentals and Deployment Platforms**
- 12-factor app methodology
- Microservices architecture patterns
- Code Engine for serverless containers
- Cloud Functions for FaaS
- Cloud Foundry basics
- Hands-on: Deploy apps to Code Engine and Functions

**Weeks 3-4: Containers and Kubernetes**
- Docker fundamentals
- Kubernetes Service (IKS) deployment
- Red Hat OpenShift features
- Container best practices
- Hands-on: Deploy microservices to IKS/OpenShift

**Weeks 5-6: DevOps, CI/CD, and Data Services**
- Continuous Delivery toolchains
- Delivery pipelines (Classic and Tekton)
- Database services (PostgreSQL, Cloudant, Redis)
- Object Storage integration
- Hands-on: Build CI/CD pipeline, integrate databases

**Weeks 7-8: Security, Integration, and Messaging**
- IAM for applications (Service IDs, API keys)
- App ID for user authentication
- Key Protect and Secrets Manager
- Event Streams (Kafka) and MQ
- Hands-on: Implement authentication, messaging

**Weeks 9-10: Practice and Review**
- Practice exams (multiple attempts)
- Code labs and sample applications
- Review weak areas
- Final hands-on projects

### Essential Hands-on Labs
- Deploy serverless application with Code Engine
- Create and deploy Cloud Function with triggers
- Deploy microservices application to Kubernetes or OpenShift
- Build CI/CD pipeline with Continuous Delivery
- Integrate application with Cloudant or Cloud Databases
- Implement authentication with App ID
- Store and retrieve secrets with Key Protect or Secrets Manager
- Build event-driven application with Event Streams
- Configure monitoring and logging for applications
- Upload and download files with Object Storage

## 📚 Study Resources

### Official IBM Resources
- **[IBM Cloud Documentation](https://cloud.ibm.com/docs)** - Service documentation (ESSENTIAL)
- **[IBM Developer](https://developer.ibm.com/)** - Tutorials, code patterns, articles
- **[IBM Cloud Training](https://www.ibm.com/training/cloud)** - Official learning paths
- **[IBM Cloud Lite Account](https://www.ibm.com/cloud/free)** - Free tier for development
- **[IBM Cloud YouTube Channel](https://www.youtube.com/IBMTechnology)** - Video tutorials

### Recommended Materials
1. **IBM Training**: Official Cloud Application Developer course
2. **IBM Developer Code Patterns**: Real-world examples
3. **Practice Tests**: IBM official practice exam
4. **Hands-on Labs**: Extensive development practice

### Development Tools
- **ibmcloud CLI**: Command-line interface for IBM Cloud
- **kubectl**: Kubernetes command-line tool
- **oc**: OpenShift command-line tool
- **cf**: Cloud Foundry command-line tool
- **Docker Desktop**: Container development
- **VS Code**: Code editor with IBM Cloud extensions

## Exam Tips

### Question Strategy
- Practical, code-oriented questions
- Focus on "how to" implement solutions
- Understand service selection trade-offs
- Best practices for cloud-native development
- DevOps and CI/CD workflow knowledge

### Common Question Themes
- 12-factor app principles application
- Deployment platform selection (Code Engine vs Functions vs Cloud Foundry vs Kubernetes)
- CI/CD pipeline configuration
- Database service selection and usage
- Authentication patterns (IAM, App ID)
- Secrets management (Key Protect, Secrets Manager)
- Event-driven architecture with Event Streams
- Container best practices
- Monitoring and logging setup
- Security best practices for applications

### Developer Best Practices
- **Externalize configuration**: Use environment variables
- **Stateless design**: Enable horizontal scaling
- **Use managed services**: Reduce operational overhead
- **Implement health checks**: Enable auto-healing
- **Log to stdout**: Integrate with platform logging
- **Secure secrets**: Use Key Protect or Secrets Manager
- **API-first design**: Well-defined interfaces
- **Automate everything**: CI/CD for all deployments
- **Monitor and trace**: Observability from the start

### Time Management
- 90 minutes for 60 questions = 1.5 minutes per question
- Don't get stuck on complex scenarios
- Flag uncertain questions for review
- Leave 10-15 minutes for final review

## 📈 Success Criteria

- Develop cloud-native applications following 12-factor principles
- Deploy applications to appropriate IBM Cloud platforms
- Implement CI/CD pipelines for automated delivery
- Integrate applications with IBM Cloud data services
- Implement authentication and authorization
- Secure applications with encryption and secrets management
- Monitor and troubleshoot applications in production
- Apply best practices for cloud application development

## Career Path and Next Steps

### After IBM Cloud Application Developer
1. **IBM Cloud Solution Architect** - Architectural perspective
2. **IBM Cloud Security Engineer** - Security specialization
3. **IBM Cloud SRE** - Operations and reliability
4. **Red Hat Certifications** - OpenShift, Ansible

### Related Certifications
- **IBM Cloud Solution Architect** - Design and architecture
- **Red Hat Certified Specialist in OpenShift Application Development**
- **Certified Kubernetes Application Developer (CKAD)**
- **IBM Cloud for Financial Services** - Industry certification

### Development Career Paths
- **Cloud Application Developer**
- **Full-Stack Developer**
- **DevOps Engineer**
- **Platform Engineer**
- **Solutions Developer**

---

**Build modern, scalable applications on IBM Cloud!** 💻
