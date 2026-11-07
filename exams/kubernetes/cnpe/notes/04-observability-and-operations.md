---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 11 min
---

# 04 - Observability and Operations

**Domain 4: Observability and Operations (20%)**

Curriculum competencies: implementing monitoring, alerting, logging and tracing solutions; measuring and improving platform efficiency using deployment metrics and performance indicators; diagnosing and remediating platform issue and incident scenarios.

Tools named in the curriculum: Prometheus, Grafana, OpenTelemetry, Jaeger, OpenCost. This repo already has full guides for the two CNCF exams that cover them, so this note gives the task view and links to the deep dives: [PCA](../../pca/) for Prometheus and [OTCA](../../otca/) for OpenTelemetry. The Grafana and Jaeger pages were not fetched for this guide, so this note makes no product claims about them beyond their appearance in the curriculum's tool list.

---

## Monitoring, alerting, logging and tracing

| Signal | Typical tool in this exam's tool list | What a task asks |
|---|---|---|
| Metrics and alerts | Prometheus (with Alertmanager) | Write or fix an alerting rule; find why a target is down |
| Dashboards | Grafana | Build or read a dashboard |
| Traces | OpenTelemetry, Jaeger | Find where a request spends time |
| Logs | The cluster's logging stack | Find the error for a failing Pod |
| Cost | OpenCost | Find an expensive namespace |

### Prometheus alerting rules

Rule files are organized in `groups`. From the Prometheus docs:

```yaml
groups:
- name: example
  labels:
    team: myteam
  rules:
  - alert: HighRequestLatency
    expr: job:request_latency_seconds:mean5m{job="myjob"} > 0.5
    for: 10m
    keep_firing_for: 5m
    labels:
      severity: page
    annotations:
      summary: High request latency
```

- `expr` is PromQL; any resulting element makes the alert active.
- **`for`** keeps the alert **pending** until the condition has held that long. Without `for`, it fires on the first evaluation.
- **`keep_firing_for`** keeps it firing after the condition stops, which prevents flapping.
- `labels` and `annotations` support templating: `$labels`, `$externalLabels`, `$value`, as in `{{ $labels.instance }}`.
- Prometheus evaluates the rules but does **not** deliver notifications. It sends alert state to Alertmanager, which handles grouping, rate limiting and silencing.
- The Alerts page shows pending and firing alerts, and Prometheus writes a synthetic `ALERTS` series with `alertname` and `alertstate` labels.

**[📖 Prometheus alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)** - fields, templating, Alertmanager

### Tracing and telemetry

OpenTelemetry is the vendor-neutral instrumentation layer; a Collector receives, processes and exports telemetry to backends such as Jaeger. The [OTCA notes](../../otca/notes/02-collector.md) cover Collector pipelines, receivers, processors and exporters, and how to debug missing telemetry (the usual order is: instrumentation, propagation, Collector, backend).

---

## Platform efficiency: deployment metrics and indicators

"Measuring and improving platform efficiency using deployment metrics" points at the DORA delivery metrics. The DORA guide lists five, in two groups:

| Group | Metric | Meaning |
|---|---|---|
| Throughput | Change lead time | How long a change takes from commit to production |
| Throughput | Deployment frequency | How often deployments happen |
| Throughput | Failed deployment recovery time | How long it takes to restore service after a deployment fails |
| Instability | Change fail rate | Share of deployments that need immediate intervention (rollback, hotfix) |
| Instability | Deployment rework rate | Share of deployments that are unplanned and triggered by a production incident |

If a task asks you to "improve" these, the levers are the ones in the earlier domains: smaller changes, automated pipelines, progressive delivery with automatic rollback, and fast alerting.

**[📖 DORA metrics](https://dora.dev/guides/dora-metrics/)** - the five software delivery metrics

For efficiency of the platform itself, resource utilization versus requests (note 01) and cost allocation by namespace (OpenCost) are the practical measures.

---

## Diagnosing and remediating incidents

Expect broken-cluster tasks: a workload that will not start, a pipeline stuck, a canary that rolled back, an alert that never fires. A method that works under time pressure:

1. **Scope it.** Which namespace, workload, and when did it change? A Git revision, a sync, a rollout step?
2. **Read status before logs.** `kubectl get` and `kubectl describe` events, conditions and ownerReferences tell you which controller owns the problem.
3. **Walk the chain.** For a GitOps app: Git revision, source artifact, Kustomization or Application status, applied objects, Pods. For a Crossplane XR: the XR conditions, then the composed managed resources, then the provider.
4. **Fix at the source of truth.** Under GitOps, a manual `kubectl` fix is reverted by `selfHeal` or the next reconcile. Fix Git.
5. **Confirm with the signal that alerted.** The metric, the trace or the dashboard should recover, not just the Pod phase.

Common patterns drawn from earlier domains:

| Symptom | First checks |
|---|---|
| Pods rejected on create | ResourceQuota (needs requests and limits), admission policies, LimitRange defaults |
| HPA shows unknown metrics | Metrics Server installed; CPU requests set on Pods |
| Argo CD OutOfSync forever | `automated` sync not enabled, or a diff in a field a controller mutates |
| Flux Kustomization not applying | Source not Ready, `dependsOn` unmet, namespace missing, `suspend: true` |
| Canary rolled back | Metric threshold breached (`threshold`), failed webhook check |
| Alert pending but not firing | `for` duration not yet met |
| Traces broken between services | Context propagation (OTCA scenario 1) |

---

## Key terms

- **Observability** - the ability to understand a system's internal state from the telemetry it emits.
- **PromQL** - the Prometheus query language used in alerting and recording rules.
- **Alertmanager** - the component that receives alerts from Prometheus and handles grouping, silencing and notification.
- **`for` (alert rule)** - the duration a condition must hold before an alert moves from pending to firing.
- **Recording rule** - a Prometheus rule that precomputes an expression into a new series.
- **OpenTelemetry Collector** - a vendor-neutral proxy that receives, processes and exports telemetry.
- **Trace** - the record of a request as it passes through services, made of spans.
- **DORA metrics** - five software delivery performance measures: change lead time, deployment frequency, failed deployment recovery time, change fail rate and deployment rework rate.
- **Showback** - reporting a team's cost to it without billing.
- **Incident** - an unplanned event that degrades a service and needs response.
