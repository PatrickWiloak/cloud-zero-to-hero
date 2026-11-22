# Red Hat Certified Specialist in OpenShift Administration (EX280)

## Overview

The Red Hat Certified Specialist in OpenShift Administration validates the skills required to operate Red Hat OpenShift clusters in production. Like RHCSA, this is a **performance-based, hands-on exam** - you'll run actual `oc` commands on a live cluster to complete tasks.

This cert is the canonical credential for OpenShift platform administrators and a step on the path to **Red Hat Certified Architect**.

---

## Quick Reference

| Detail | Info |
|---|---|
| **Exam Code** | EX280 |
| **Full Name** | Red Hat Certified Specialist in OpenShift Administration |
| **Provider** | Red Hat |
| **Format** | Performance-based hands-on tasks on a live OpenShift cluster |
| **Duration** | 3 hours |
| **Passing Score** | 210/300 (70%) |
| **Cost** | $500 USD |
| **Validity** | 3 years |
| **Delivery** | Individual exam (online via Red Hat Remote Exam) or testing center |
| **OpenShift Version** | OpenShift Container Platform 4.22 (EX280 page, read 2026-11-22); notes were written against 4.14 |
| **Prerequisites** | RHCSA strongly recommended; experience with Linux containers |

**[📖 Official EX280 page](https://www.redhat.com/en/services/training/red-hat-certified-openshift-administrator-exam)**

---

## What You'll Do on the Exam

Tasks span the OpenShift admin lifecycle:

1. **Cluster operations** - install / upgrade / configure cluster components, manage cluster nodes, configure cluster authentication.
2. **Project and quota management** - create projects, apply resource quotas and limit ranges, configure default project templates.
3. **Identity and RBAC** - configure identity providers, create users / groups, assign cluster and project roles.
4. **Workload operations** - deploy applications, scale, configure deployment strategies, troubleshoot pods.
5. **Networking** - configure routes, services, network policies, ingress.
6. **Storage** - configure persistent volumes, storage classes, PVCs, storage drivers.
7. **Security and compliance** - SCCs (Security Context Constraints), pod security admission, network policies.
8. **Operators and Operator Lifecycle Manager** - install operators, manage operator subscriptions and channels.
9. **Monitoring and metrics** - configure cluster monitoring, view metrics, create alerts.
10. **Troubleshooting** - logs, events, must-gather, debug pods.

The exam is **closed book** but you have access to:

- The OpenShift web console
- `oc explain` for resource fields
- Pre-installed CLI documentation
- The cluster itself (you can read existing resources)

---

## Study Materials in This Guide

| File | Description |
|---|---|
| [fact-sheet.md](fact-sheet.md) | Reference with `oc` commands, resource shapes, and high-yield facts |
| [notes/01-cluster-install-config.md](notes/01-cluster-install-config.md) | Cluster components, install, machine config, day-2 operations |
| [notes/02-projects-quotas-rbac.md](notes/02-projects-quotas-rbac.md) | Projects, ResourceQuota, LimitRange, RBAC, identity providers |
| [notes/03-networking-routes.md](notes/03-networking-routes.md) | Services, routes, ingress, NetworkPolicy |
| [notes/04-storage-pv-pvc.md](notes/04-storage-pv-pvc.md) | Storage classes, PVs, PVCs, common drivers |
| [notes/05-operators-monitoring.md](notes/05-operators-monitoring.md) | Operators, OLM, monitoring stack, must-gather |
| [practice-plan.md](practice-plan.md) | 6-week study plan |
| [scenarios.md](scenarios.md) | 15 exam-style hands-on tasks |

---

## Recommended Study Time

| Background | Estimated Prep Time |
|---|---|
| OpenShift admin experience (1+ year), holds RHCSA | 4 weeks |
| Kubernetes admin (CKA-equivalent), new to OpenShift | 6 weeks |
| New to containers and Kubernetes | 10-12 weeks; consider RHCSA first |

Plan on heavy hands-on lab time. This is a performance exam.

---

## Lab Setup

You **cannot pass without hands-on practice.** Options:

### Best: Red Hat-provided

- **OpenShift Local (formerly CodeReady Containers / CRC)** - free single-node OpenShift on your laptop. Requires 9+ GB RAM and 4+ vCPUs. [Download](https://developers.redhat.com/products/openshift-local/overview)
- **Developer Sandbox for Red Hat OpenShift** - free 30-day shared cluster. [Sandbox](https://developers.redhat.com/developer-sandbox)
- **Red Hat Learning Subscription Trial** - access to RH364 (Red Hat OpenShift Administration II) labs.

### Realistic alternative: managed OpenShift

- **ROSA** (Red Hat OpenShift on AWS) - paid, but you can keep usage minimal during prep.
- **ARO** (Azure Red Hat OpenShift) - similar.

### Last resort: vanilla Kubernetes

- **kind / minikube / k3s** can teach you concepts but miss OpenShift-specific things (Routes, SCCs, Operators, OperatorHub, oc CLI).

OpenShift Local is the recommended free path.

---

## Key Differences vs. CKA / Vanilla Kubernetes

OpenShift differs from vanilla Kubernetes in important ways the exam tests:

| Area | OpenShift | Vanilla K8s |
|---|---|---|
| CLI | `oc` (superset of `kubectl`) | `kubectl` |
| Namespaces | Called **Projects** (with extra metadata) | Just namespaces |
| Ingress | **Routes** (OpenShift-specific resource) | Ingress |
| Pod security | **SCC (Security Context Constraints)** | PSA (Pod Security Admission) |
| User accounts | First-class **User** and **Group** resources | External (RBAC subjects) |
| App build | **BuildConfig**, **ImageStream**, **DeploymentConfig** (legacy + Deployment) | Just Deployment |
| Operators | **OperatorHub** + OLM built in | Operators are optional |
| Default install | Includes monitoring, logging, registry, console, OAuth | Minimal |

If you come from CKA, focus on Routes, SCCs, OperatorHub, ImageStreams, and Projects.

---

## Exam-Day Tips

1. **Use `oc explain`** when you forget a field name. `oc explain pod.spec.containers.resources` is your friend.
2. **Use the web console** for things faster than typing. The console can generate YAML for resources.
3. **Save YAML to disk** for any complex resource. `oc edit` works but `oc apply -f file.yaml` is more recoverable.
4. **Verify after every change**. `oc get`, `oc describe`, `oc logs`.
5. **Check existing examples** on the cluster. `oc get pod -o yaml` shows you what a working pod's YAML looks like - use as a template.
6. **Don't forget labels and selectors.** Many tasks involve creating a Service or NetworkPolicy that selects on labels.
7. **Read the task fully.** Specific names, namespaces, replica counts matter.

---

## After EX280

Common next steps:

- **Red Hat Certified Specialist in OpenShift Application Development (EX288)** - the developer counterpart
- **Red Hat Certified Specialist in OpenShift Virtualization (EX316)** - VMs on OpenShift
- **Red Hat Certified Specialist in Advanced Cluster Management (EX480)** - multi-cluster
- **Red Hat Certified Architect** - composite credential requiring 5+ specialist certs

Vendor-neutral parallel: **Kubernetes CKA / CKAD / CKS**.

---

## Companion Materials in This Repo

- **[Kubernetes CKA](../../kubernetes/cka/)** - vendor-neutral cluster admin
- **[Kubernetes CKS](https://security.noblerworks.com/exams/kubernetes/cks/)** - K8s security specialist
- **[Containers and Kubernetes service comparison](../../../resources/service-comparison-containers-kubernetes.md)** - cross-cloud
- **[RHCSA](../rhcsa-ex200/)** - Linux foundation often required first
