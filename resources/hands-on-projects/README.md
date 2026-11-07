---
last-updated: 2026-10-21
---

# Hands-on projects

Guided cloud builds. Each has an estimated time, a goal you can articulate to an interviewer, and inline code or commands. Most run on free-tier accounts.

Data, security and AI builds live on the sibling sites: [build a data pipeline](https://data.noblerworks.com/resources/hands-on-projects/build-data-pipeline/) on Data Zero to Hero, [implement zero trust](https://security.noblerworks.com/resources/hands-on-projects/implement-zero-trust/) on Security Zero to Hero, and [RAG, agents, model serving and fine-tuning builds](https://ai.noblerworks.com/build/projects/build-rag-pipeline/) on AI Zero to Hero.

## Cloud builds

| Build | Time | What you'll have at the end |
|---|---|---|
| [Deploy a 3-tier app](./deploy-3-tier-app.md) | 3-4 hours | LB → app servers → DB on AWS, Azure, or GCP |
| [Build a CI/CD pipeline](./build-ci-cd-pipeline.md) | 4-5 hours | Auto-build, test, and deploy on commit |
| [Set up a monitoring stack](./setup-monitoring-stack.md) | 3-4 hours | Prometheus + Grafana + alertmanager wired end-to-end |
| [Set up a Kubernetes cluster](./kubernetes-cluster-setup.md) | 4-5 hours | Production-shaped cluster, ingress, observability |
| [Build infra with Terraform](./terraform-infrastructure.md) | 3-4 hours | VPC + compute + DB declared as code, with state |
| [Build a serverless app](./serverless-application.md) | 3-4 hours | API + queue + function + storage, event-driven |
| [Run a DR drill](./disaster-recovery-drill.md) | 4-6 hours | Tested failover, measured RTO/RPO |
| [Build a landing zone](./build-a-landing-zone.md) | 3-4 hours | Multi-account organization with guardrails, an org audit trail and budgets |
| [GitOps with Argo CD](./gitops-with-argo-cd.md) | 2-3 hours | Deploy, promote and roll back by Git commit, with drift self-healed |

## How to pick

- **First-ever cloud build:** [Deploy a 3-tier app](./deploy-3-tier-app.md). Touches networking, compute, identity, and storage in one project.
- **Interview prep:** [Set up a Kubernetes cluster](./kubernetes-cluster-setup.md), [Build infra with Terraform](./terraform-infrastructure.md), [Build a CI/CD pipeline](./build-ci-cd-pipeline.md). These map to the most common practitioner questions.
- **Cheapest to run:** serverless and Terraform (free-tier friendly); GitOps with Argo CD runs entirely on your laptop.
- **Most production-shaped:** [Run a DR drill](./disaster-recovery-drill.md), [Set up a monitoring stack](./setup-monitoring-stack.md).
- **Platform and governance:** [Build a landing zone](./build-a-landing-zone.md) for multi-account guardrails, [GitOps with Argo CD](./gitops-with-argo-cd.md) for pull-based delivery.
- **Which build backs which exam:** [Labs by certification](./labs-by-cert.md).

## Related

- [Concepts](../../learn/concepts/) - the "why" behind each pattern
- [Architecture patterns](../architecture-patterns/) - reference designs each build follows
- [Topic indexes](../../topics/) - all four pillars per subject

## Which lab for which cert

Each lab maps to the certs it exercises. The reverse index lives in [labs-by-cert.md](./labs-by-cert.md).

<!-- BEGIN GENERATED: lab-cert-map - run .github/scripts/build-lab-map.py -->

| Lab | Certs it supports |
|------|-------------------|
| [Hands-On Project: Build a CI/CD Pipeline](./build-ci-cd-pipeline.md) | [GH-200](../../exams/github/actions/), [AZ-400](../../exams/azure/az-400/), [DOP-C02](../../exams/aws/professional/devops-engineer-pro-dop-c02/), [Google Cloud Professional Cloud DevOps Engineer Certification](../../exams/gcp/cloud-devops-engineer/) |
| [Hands-On Project: Build a Landing Zone](./build-a-landing-zone.md) | [SAP-C02](../../exams/aws/professional/solutions-architect-pro-sap-c02/), [AZ-305](../../exams/azure/az-305/), [Professional Cloud Architect](../../exams/gcp/cloud-architect/) |
| [Hands-On Project: Build a Serverless Application](./serverless-application.md) | [DVA-C02](../../exams/aws/associate/developer-dva-c02/), [AZ-204](../../exams/azure/az-204/), [Google Cloud Professional Cloud Developer Certification](../../exams/gcp/cloud-developer/) |
| [Hands-On Project: Build Infrastructure with Terraform](./terraform-infrastructure.md) | [Terraform Associate (004)](../../exams/hashicorp/terraform-associate/), [HashiCorp Certified: Terraform Authoring and Operations Advanced](../../exams/hashicorp/terraform-authoring-operations-pro/) |
| [Hands-On Project: Deploy a 3-Tier Application](./deploy-3-tier-app.md) | [SAA-C03](../../exams/aws/associate/solutions-architect-saa-c03/), [AZ-104](../../exams/azure/az-104/), [Associate Cloud Engineer](../../exams/gcp/cloud-engineer/), [CV0-004](../../exams/comptia/cloud-plus/) |
| [Hands-On Project: Disaster Recovery Drill](./disaster-recovery-drill.md) | [SAP-C02](../../exams/aws/professional/solutions-architect-pro-sap-c02/), [AZ-305](../../exams/azure/az-305/), [Professional Cloud Architect](../../exams/gcp/cloud-architect/), [CV0-004](../../exams/comptia/cloud-plus/) |
| [Hands-On Project: GitOps with Argo CD](./gitops-with-argo-cd.md) | [CGOA](../../exams/kubernetes/cgoa/), [CAPA](../../exams/kubernetes/capa/), [AZ-400](../../exams/azure/az-400/), [Google Cloud Professional Cloud DevOps Engineer Certification](../../exams/gcp/cloud-devops-engineer/) |
| [Hands-On Project: Set Up a Monitoring Stack](./setup-monitoring-stack.md) | [PCA](../../exams/kubernetes/pca/), [SOA-C03](../../exams/aws/associate/cloudops-engineer-soa-c03/), [Google Cloud Professional Cloud DevOps Engineer Certification](../../exams/gcp/cloud-devops-engineer/) |
| [Hands-On Project: Set Up a Production-Like Kubernetes Cluster](./kubernetes-cluster-setup.md) | [CKA](../../exams/kubernetes/cka/), [CKAD](../../exams/kubernetes/ckad/), [EX280](../../exams/redhat/openshift-administrator-ex280/) |

<!-- END GENERATED: lab-cert-map -->
