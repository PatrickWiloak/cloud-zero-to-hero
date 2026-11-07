# 📚 Study Hub - Cloud Zero to Hero

> **Your navigation hub for every cloud certification on this site - AWS, Azure, GCP, OCI, IBM, Kubernetes, HashiCorp, Linux, networking and FinOps - plus the [Learn](./learn/) pillar for non-cert students: bite-size concepts, a beginner on-ramp, and a structured cloud path.**

<!-- markdown="1" lets the documentation site render the markdown inside this
     centered block. GitHub ignores the attribute, so rendering there is unchanged. -->
<div align="center" markdown="1">

**Welcome. Whether you're new to all this or chasing your fifth cloud cert, this is the entry point.**

**[Browse it as a searchable site](https://cloud.noblerworks.com/)** - full-text search across every page, which is faster than this index once you know what you are looking for.

Data, security and AI certifications live on the sibling sites: **[Data](https://data.noblerworks.com/STUDY-HUB/)** · **[Security](https://security.noblerworks.com/STUDY-HUB/)** · **[AI](https://ai.noblerworks.com/)** Zero to Hero.

</div>

---

## 🗺️ Table of Contents

- [Quick Navigation](#-quick-navigation)
- [Not chasing a certification?](#-not-chasing-a-certification)
- [Decision Tree: Find Your Cert](#-decision-tree-find-your-cert)
- [Study Tracks by Career Path](#-study-tracks-by-career-path)
- [Certifications by Provider](#-certifications-by-provider)
- [Most Popular Certifications](#-most-popular-certifications)
- [Study Timeline Estimates](#-study-timeline-estimates)
- [Resource Library](#-resource-library)
- [Cost Planning](#-cost-planning)

---

## 🎯 Quick Navigation

| I Want To... | Go To... |
|--------------|----------|
| 🌅 Start from absolute zero (terminal, git, HTTP) | [Day One](./learn/day-one/) |
| 💡 Look up a concept (VPC, DNS, containers, Kubernetes) | [Concepts](./learn/concepts/) |
| 🗂️ Browse by topic across pillars | [Topic indexes](./topics/) |
| 🎓 Learn cloud without an exam | [Cloud from Scratch](./learn/cloud-from-scratch.md) |
| 🆕 Start my cloud cert journey | [Beginner Fundamentals](#beginner-fundamentals) |
| 🎯 Choose the right cert | [Decision Tree](#-decision-tree-find-your-cert) |
| 🚀 Follow a career path | [Study Tracks](#-study-tracks-by-career-path) |
| ☸️ Specialize in Kubernetes | [Kubernetes Track](#kubernetes-track) |
| 💰 Specialize in FinOps | [FinOps Track](#finops-track) |
| 🌐 Specialize in networking | [Networking Track](#networking-track) |
| 📚 Browse all materials | [Resource Library](#-resource-library) |
| 📅 Per-cert last-verified dates | [Freshness ledger](./docs/freshness.md) |
| 🧪 Find the lab for my cert | [Labs by certification](./resources/hands-on-projects/labs-by-cert.md) |
| 🃏 Flashcards for a cert | `flashcards.csv` in each cert dir (Anki-importable) |
| 🔒 Security, 📊 data or 🤖 AI certs | [Security](https://security.noblerworks.com/STUDY-HUB/) · [Data](https://data.noblerworks.com/STUDY-HUB/) · [AI](https://ai.noblerworks.com/) Zero to Hero |

---

## 🎓 Not chasing a certification?

The **[Learn](./learn/)** pillar is for everyone who wants to understand cloud without an exam date:

- **[Day One](./learn/day-one/)** - terminal, git, HTTP, servers. Strict beginner on-ramp.
- **[Concepts](./learn/concepts/)** - bite-size pages (5-10 min each) on cloud primitives.
- **[Cloud from Scratch](./learn/cloud-from-scratch.md)** - a structured 8-phase path.
- **[Glossary](./learn/glossary.md)** - the vocabulary in plain English.
- **[YouTube curation](./learn/youtube.md)** - filtered videos worth your time.

Come back when you decide to certify. Many do, after using the Learn pillar to figure out which direction.

---

## 🌳 Decision Tree: Find Your Cert

```
What's your starting point?
│
├─ New to IT
│  └─> CompTIA A+ → Network+ | Linux Foundation LFCA
│
├─ New to cloud (0-6 months)
│  └─> AWS Cloud Practitioner | Azure AZ-900 | GCP Cloud Digital Leader | OCI Foundations | IBM Cloud Advocate
│
├─ Have some cloud experience (6-18 months)
│  ├─ Want infrastructure focus → AWS SAA-C03 | Azure AZ-104 | GCP Associate Cloud Engineer | OCI Architect Associate
│  ├─ Want development focus  → AWS DVA-C02 | GCP Cloud Developer | OCI Developer Associate
│  └─ Want operations focus   → AWS CloudOps SOA-C03 | Azure AZ-104 | OCI Operations Associate | RHCSA
│
├─ Senior practitioner (18+ months)
│  ├─ Architecture        → AWS SAP-C02 | Azure AZ-305 | GCP Cloud Architect | OCI Architect Professional
│  ├─ DevOps              → AWS DOP-C02 | Azure AZ-400 | GCP Cloud DevOps Engineer
│  └─ Specialty           → AWS Advanced Networking | AWS SAP on AWS | AWS Quantum | OpenShift EX280
│
└─ Cross-cutting specializations
   ├─ Kubernetes          → KCNA → CKA → CKAD → ICA (Istio) | OpenShift EX280
   ├─ Cloud native        → CAPA (Argo) | CGOA (GitOps) | CCA (Cilium) | PCA (Prometheus) | OTCA (OpenTelemetry) | CNPA
   ├─ Terraform/IaC       → Terraform Associate → Terraform Authoring & Operations Advanced | Packer | Nomad
   ├─ Networking          → Network+ → CCNA → CCNP ENCOR | AWS Adv Networking | GCP Cloud Network Engineer | AZ-700
   ├─ Linux / Platform    → LFCS | RHCSA → OpenShift EX280
   ├─ CI/CD               → GitHub Foundations → GitHub Actions → GitHub Administration
   └─ FinOps              → FinOps Practitioner → Engineer/Analyst → Professional
```

Heading toward security, data or AI? The decision trees for those live on the [Security](https://security.noblerworks.com/STUDY-HUB/), [Data](https://data.noblerworks.com/STUDY-HUB/) and [AI](https://ai.noblerworks.com/) sites.

---

## 🚀 Study Tracks by Career Path

### Cloud Architect Track
**Foundations → Associate → Professional**
1. AWS Cloud Practitioner *or* Azure AZ-900 *or* GCP Cloud Digital Leader
2. AWS Solutions Architect Associate (SAA-C03) *or* Azure AZ-104 *or* GCP Associate Cloud Engineer
3. AWS Solutions Architect Professional (SAP-C02) *or* Azure AZ-305 *or* GCP Cloud Architect
4. Multi-cloud add-on: Terraform Associate, Kubernetes CKA

### DevOps / SRE Track
1. Foundational cloud cert in your primary cloud
2. AWS DVA-C02 *or* GCP Cloud Developer *or* AWS CloudOps SOA-C03
3. AWS DOP-C02 *or* Azure AZ-400 *or* GCP Cloud DevOps Engineer
4. Specialization: Kubernetes CKA → CKAD, Terraform Associate, Prometheus PCA, OpenTelemetry OTCA, IBM Cloud SRE

### Kubernetes Track <a id="kubernetes-track"></a>
1. KCNA (Kubernetes and Cloud Native Associate)
2. CKA (Administrator)
3. CKAD (Application Developer)
4. OpenShift Administrator (EX280) for Red Hat-specific path
5. Specialization: PCA (Prometheus), ICA (Istio), CCA (Cilium), CAPA (Argo), CGOA (GitOps)

### FinOps Track <a id="finops-track"></a>
1. FinOps Certified Practitioner
2. FinOps Certified Engineer *or* FinOps Certified Analyst
3. FinOps Certified Professional (advanced, FOCUS-aware)
4. Cloud-specific: AWS Cost optimization, Azure Cost Management, GCP billing

### Platform Engineering Track
1. Linux Foundation LFCS *or* RHCSA *or* CompTIA Cloud+
2. Cloud associate cert (your primary cloud)
3. Kubernetes CKA + HashiCorp Terraform Associate (or OpenShift EX280 for Red Hat shops)
4. GitHub Actions + Administration certifications
5. Add: Cloud Native Platform Engineering Associate (CNPA), Nomad Associate, Packer Associate

### Networking Track <a id="networking-track"></a>
1. CompTIA Network+ (N10-009) - vendor-neutral networking foundation
2. Cisco CCNA (200-301) - routing and switching
3. AWS Advanced Networking Specialty *or* GCP Cloud Network Engineer *or* Azure AZ-700 (cloud-side)
4. CCNP Enterprise (350-401 ENCOR) for advanced Cisco networking

### Tracks on the sibling sites
- **Security** (Security+, cloud security specialties, CCSP, CISSP) - [Security Zero to Hero](https://security.noblerworks.com/STUDY-HUB/)
- **Data engineering** (AWS DEA-C01, Databricks, Snowflake, Kafka, MongoDB) - [Data Zero to Hero](https://data.noblerworks.com/STUDY-HUB/)
- **AI/ML and generative AI** (AWS AI and ML certs, Azure AI, NVIDIA, Anthropic Claude) - [AI Zero to Hero](https://ai.noblerworks.com/)

---

## 📋 Certifications by Provider

<!-- BEGIN GENERATED: provider-table - edit .github/scripts/build-provider-indexes.py, not this block -->

| Provider | Certs | Highlights | Browse |
|----------|------:|------------|--------|
| **AWS** | 11 | CLF-C02, SAA-C03, SOA-C03, DVA-C02, SAP-C02, DOP-C02, Advanced Networking (ANS-C01), SAP on AWS (PAS-C01), Quantum (QPC-C01); retired SOA-C02 retained | [exams/aws/](./exams/aws/) |
| **Azure** | 10 | AZ-900/104/204/305/400/700, MS-900, PL-100/200/900 | [exams/azure/](./exams/azure/) |
| **GCP** | 7 | Digital Leader, Associate Cloud Engineer, Cloud Architect, Cloud Developer, DevOps, Network Engineer, Workspace Admin | [exams/gcp/](./exams/gcp/) |
| **Kubernetes/CNCF** | 10 | KCNA, CKA, CKAD, plus Argo (CAPA), Cilium (CCA), GitOps (CGOA), Istio (ICA), OpenTelemetry (OTCA), Prometheus (PCA), Platform Engineering (CNPA) | [exams/kubernetes/](./exams/kubernetes/) |
| **HashiCorp** | 5 | Terraform Assoc + Pro, Consul, Packer, Nomad | [exams/hashicorp/](./exams/hashicorp/) |
| **GitHub** | 3 | Foundations, Actions, Administration | [exams/github/](./exams/github/) |
| **Red Hat** | 2 | RHCSA (EX200), OpenShift Administrator (EX280) | [exams/redhat/](./exams/redhat/) |
| **Cisco** | 2 | CCNA (200-301), CCNP Enterprise ENCOR (350-401) | [exams/cisco/](./exams/cisco/) |
| **Salesforce** | 3 | Administrator, Platform Developer I, Platform Developer II | [exams/salesforce/](./exams/salesforce/) |
| **FinOps Foundation** | 4 | Practitioner, Engineer, Analyst, Professional | [exams/finops/](./exams/finops/) |
| **CompTIA** | 4 | A+ (220-1201/1202), Cloud+ (CV0-004), Network+ (N10-009) | [exams/comptia/](./exams/comptia/) |
| **Linux Foundation** | 2 | LFCS, LFCA | [exams/linux-foundation/](./exams/linux-foundation/) |
| **Oracle Cloud (OCI)** | 5 | OCI Foundations, Architect Assoc + Pro, Developer Assoc, Operations Assoc | [exams/oracle/](./exams/oracle/) |
| **IBM Cloud** | 4 | Advocate, Developer, Solution Architect, SRE | [exams/ibm/](./exams/ibm/) |
| **ServiceNow** | 1 | Certified System Administrator | [exams/servicenow/](./exams/servicenow/) |
| **VMware** | 1 | VCP-DCV (2V0-21.23) | [exams/vmware/](./exams/vmware/) |
| **CERTIFICATIONS TOTAL** | **74** | across 16 providers | |

◇ = outline stage: README, fact-sheet, and practice plan are written; topic notes are outlined but not yet drafted. See [TODO.md](https://github.com/PatrickWiloak/cloud-zero-to-hero/blob/main/TODO.md) for the drafting queue.

<!-- END GENERATED: provider-table -->

---

## 🔥 Most Popular Certifications

Top picks based on industry demand and salary impact:

1. [AWS Solutions Architect Associate (SAA-C03)](./exams/aws/associate/solutions-architect-saa-c03/) - the gateway AWS cert
2. [Azure Administrator (AZ-104)](./exams/azure/az-104/) - core Azure operations
3. [GCP Associate Cloud Engineer](./exams/gcp/cloud-engineer/) - foundational GCP
4. [CKA (Certified Kubernetes Administrator)](./exams/kubernetes/cka/) - Kubernetes ops
5. [Terraform Associate](./exams/hashicorp/terraform-associate/) - IaC standard
6. [AWS Solutions Architect Professional (SAP-C02)](./exams/aws/professional/solutions-architect-pro-sap-c02/) - senior architect
7. [Azure DevOps Engineer (AZ-400)](./exams/azure/az-400/) - Azure expert DevOps
8. [AWS DevOps Engineer Professional (DOP-C02)](./exams/aws/professional/devops-engineer-pro-dop-c02/) - senior AWS DevOps
9. [FinOps Certified Practitioner](./exams/finops/certified-practitioner/) - cloud cost discipline
10. [Cisco CCNA (200-301)](./exams/cisco/ccna-200-301/) - foundational networking
11. [Red Hat RHCSA (EX200)](./exams/redhat/rhcsa-ex200/) - Linux administration foundation

---

## ⏱️ Study Timeline Estimates

| Cert Tier | Typical Prep Time | Daily Study | Examples |
|-----------|-------------------|-------------|----------|
| **Fundamentals** | 2-4 weeks | 1-2 hr | CLF-C02, AZ-900, GCP Digital Leader, KCNA |
| **Associate** | 6-10 weeks | 2-3 hr | SAA-C03, AZ-104, CKA, RHCSA, Terraform Associate |
| **Professional** | 10-16 weeks | 2-4 hr | SAP-C02, AZ-305, AZ-400, GCP Cloud Architect |
| **Specialty** | 8-14 weeks | 2-4 hr | AWS Advanced Networking, SAP on AWS, CCNP ENCOR |

### Beginner Fundamentals
First-cert path with no cloud background:
1. Pick one provider you'll use most often
2. Take its foundational cert (4 weeks of evenings)
3. Build a small free-tier project
4. Decide on Associate-level direction

---

## 📚 Resource Library

### Service Comparisons (cross-cloud)
[Compute](./resources/service-comparison-compute.md) · [Storage](./resources/service-comparison-storage.md) · [Networking](./resources/service-comparison-networking.md) · [Containers/K8s](./resources/service-comparison-containers-kubernetes.md) · [DevOps/CI/CD](./resources/service-comparison-devops-cicd.md) · [Observability](./resources/service-comparison-observability-monitoring.md) · [Serverless](./resources/service-comparison-serverless.md)

On the sibling sites: [Databases](https://data.noblerworks.com/resources/service-comparison-databases/) · [Messaging](https://data.noblerworks.com/resources/service-comparison-messaging-queues/) · [Security tools](https://security.noblerworks.com/resources/service-comparison-security-tools/) · [Identity/IAM](https://security.noblerworks.com/resources/service-comparison-identity-iam/) · [Cloud AI/ML services](https://ai.noblerworks.com/tools/comparisons/cloud-ai-ml-services/)

### CLI Cheat Sheets
[AWS](./resources/cli-cheat-sheet-aws.md) · [Azure](./resources/cli-cheat-sheet-azure.md) · [GCP](./resources/cli-cheat-sheet-gcp.md) · [Multi-cloud](./resources/cli-cheat-sheet-comparison.md) · [kubectl](./resources/cli-cheat-sheet-kubectl.md) · [Terraform](./resources/cli-cheat-sheet-terraform.md) · [Docker](./resources/cli-cheat-sheet-docker.md) · [Helm](./resources/cli-cheat-sheet-helm.md) · [GitHub CLI](./resources/cli-cheat-sheet-github-cli.md)

### Architecture Patterns
Multi-cloud patterns covering 3-tier apps, serverless, microservices, event-driven, disaster recovery, multi-region active-active, cell-based, chaos engineering, hybrid cloud and more. [Browse all](./resources/architecture-patterns/)

### Career Roadmaps
[Cloud Engineer](./resources/certification-roadmap-cloud-engineer.md) · [Solutions Architect](./resources/certification-roadmap-solutions-architect.md) · [DevOps/SRE](./resources/certification-roadmap-devops-sre.md) · [Multi-Cloud](./resources/certification-roadmap-multi-cloud.md) · [Kubernetes Specialist](./resources/certification-roadmap-kubernetes-specialist.md) · [Platform Engineer](./resources/certification-roadmap-platform-engineer.md) · [FinOps](./resources/certification-roadmap-finops.md)

On the sibling sites: [Data Engineer](https://data.noblerworks.com/resources/certification-roadmap-data-engineer/) · [Database Specialist](https://data.noblerworks.com/resources/certification-roadmap-database-specialist/) · [Security Engineer](https://security.noblerworks.com/resources/certification-roadmap-security-engineer/) · [AI Engineer](https://ai.noblerworks.com/careers/roles/ai-engineer-roadmap/)

### Deep-Dive Guides
- **Migration:** On-prem to AWS/Azure/GCP, cloud-to-cloud - [resources/migration-guides/](./resources/migration-guides/)
- **Well-Architected:** AWS, Azure, GCP frameworks - [resources/well-architected/](./resources/well-architected/)
- **Cost Optimization:** Per-cloud playbooks + Kubernetes + FinOps principles - [resources/cost-optimization/](./resources/cost-optimization/)
- **Troubleshooting:** AWS, Azure, GCP, Kubernetes, CI/CD, Terraform state - [resources/troubleshooting/](./resources/troubleshooting/)
- **Networking Deep Dives:** Hybrid connectivity, multi-cloud, DNS, load balancing - [resources/networking-deep-dives/](./resources/networking-deep-dives/)
- **Hands-on Projects:** 3-tier app, CI/CD, monitoring, Kubernetes cluster, Terraform infra, serverless, DR drill, landing zone, GitOps with Argo CD - [resources/hands-on-projects/](./resources/hands-on-projects/)
- **Interview Prep:** Solutions Architect, DevOps, Cloud Engineer, SRE, Platform Engineer, Kubernetes - [resources/interview-prep/](./resources/interview-prep/)
- **Compliance** (SOC 2, HIPAA, PCI DSS, GDPR, FedRAMP) - on the [Security site](https://security.noblerworks.com/resources/compliance-guides/)

### Practice & Strategy
- [Practice Question Banks](./resources/practice-questions/) - scenario questions with explained answers, one bank per certification
- [Practice Resources Guide](./resources/practice-resources.md)
- [Free Tier Guides](./resources/free-tier-guide.md)
- [Study Strategies](./resources/study-strategies.md)
- [Exam Day Checklist](./resources/exam-day-checklist.md)
- [Budget Study Plan](./resources/budget-study-plan.md)
- [Community Resources](./resources/community-resources.md)

---

## 💰 Cost Planning

| Item | Typical Cost |
|------|-------------:|
| **All study materials in this repo** | Free |
| **Official documentation** | Free |
| **Free tier sandbox accounts** | Free |
| **Video course (optional)** | $15-50 |
| **Third-party practice tests (optional)** | $15-30 |
| **Exam fee (per cert)** | $100-700 |
| **Total per Associate cert** | $150-300 |
| **Total per Professional cert** | $300-500 |

See the [budget study plan](./resources/budget-study-plan.md) for detailed cost-minimization strategies.

---

## 🤝 Community

- **Reddit:** r/AWSCertifications, r/AZURE, r/googlecloud, r/kubernetes, r/devops, r/sre
- **Discord:** Cloud certification study servers (links in [community-resources.md](./resources/community-resources.md))
- **LinkedIn:** Search for "[Cert name] Study Group"
- **GitHub:** Star this repo and watch for updates

---

## 📝 How to Use This Hub

1. Start at [Decision Tree](#-decision-tree-find-your-cert) to identify your cert
2. Open that cert's directory: `exams/<provider>/<cert>/`
3. Read in order: `README.md` → `fact-sheet.md` → `practice-plan.md` → `notes/` → `scenarios.md` → `strategy.md`
4. Cross-reference with [Resource Library](#-resource-library) for cross-cloud knowledge
5. Take practice exams when consistently scoring 80%+ on practice questions
6. Schedule the real exam when you hit 85%+ twice in a row

---

<div align="center" markdown="1">

**Ready to start? [Browse the AWS catalog](./exams/aws/) · [Browse Azure](./exams/azure/) · [Browse GCP](./exams/gcp/) · [Browse Kubernetes](./exams/kubernetes/)**

*Maintained by [Patrick Wiloak](https://patrickwiloak.com) - Star this repo if it helps you pass.*

</div>
