---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 9 min
---

# 05 - Observability

**Domain 5: Observability (15%)**

Curriculum competencies: analyzing network health using metrics; troubleshooting end-to-end network performance with tracing; auditing traffic with logs.

Nothing here was run: no cluster was available. YAML was syntax-checked only. The documented sources used are Cilium and Hubble, Istio, and CoreDNS.

---

## Network health with metrics

Where network metrics come from, by layer:

| Source | What it tells you | How exposed |
|---|---|---|
| CoreDNS | DNS health and latency | The `prometheus` plugin serves `:9153/metrics` (default Corefile) |
| Cilium agent and Hubble | Datapath, flows, drops, DNS, TCP, ICMP | `prometheus.enabled=true`; `hubble.metrics.enabled` list |
| Istio proxies | Request rate, errors, latency, bytes, mTLS | Standard Istio metrics scraped from the sidecars |
| kube-proxy / nodes | Service programming health | The exam environment's node and proxy metrics |

### Cilium and Hubble

From the Cilium metrics page:

- Cilium agent metrics: `prometheus.enabled=true` (prefix `cilium_`). The operator's metrics are on by default.
- Hubble: `hubble.enabled=true` and list the metrics in `hubble.metrics.enabled`; add `hubble.metrics.enableOpenMetrics=true` to use OpenMetrics (supports exemplars). The `http` metric is deprecated in favor of `httpV2`, and the two cannot be enabled together.
- Ports: cilium-agent 9962, cilium-envoy 9964, cilium-operator 9963, Hubble 9965 (`hubble.metrics.port`).

```bash
helm install cilium cilium/cilium --version 1.20.4 \
  --namespace kube-system \
  --set prometheus.enabled=true \
  --set operator.prometheus.enabled=true \
  --set hubble.enabled=true \
  --set hubble.metrics.enableOpenMetrics=true \
  --set hubble.metrics.enabled="{dns,drop,tcp,flow,port-distribution,icmp,httpV2:exemplars=true}"
```

Example metrics: `hubble_flows_processed_total` (labels `protocol`, `type`, `subtype`, `verdict`) and `hubble_drop_total` (labels `reason`, `protocol`). Both appear only if their metric group is listed in `hubble.metrics.enabled`.

**[📖 Cilium and Hubble metrics](https://docs.cilium.io/en/stable/observability/metrics/)** - enabling, ports, examples

### Istio metrics

Istio's standard metrics (reference for Istio 1.31):

| Metric | Type | Measures |
|---|---|---|
| `istio_requests_total` | Counter | Requests handled by a proxy (HTTP, HTTP/2, gRPC) |
| `istio_request_duration_milliseconds` | Distribution | Request duration |
| `istio_request_bytes`, `istio_response_bytes` | Distribution | Body sizes |
| `istio_tcp_sent_bytes_total`, `istio_tcp_received_bytes_total` | Counter | TCP bytes |
| `istio_tcp_connections_opened_total`, `istio_tcp_connections_closed_total` | Counter | TCP connections |

Useful labels: `reporter` (`source` or `destination`), source and destination workload, namespace, app and principal, `destination_service`, `response_code` (HTTP only), `response_flags`, and `connection_security_policy` (`mutual_tls` when reported by the destination). Labels can be suppressed or added with the Telemetry resource's `metricsOverrides`.

The questions you answer with them: error rate (`istio_requests_total` split by `response_code`), latency (the duration distribution), and whether traffic is encrypted (`connection_security_policy`).

**[📖 Istio standard metrics](https://istio.io/latest/docs/reference/config/metrics/)** - metric names, types and labels

---

## End-to-end performance with tracing

A trace follows one request across services. In a mesh the proxies create spans automatically, but the Istio docs are explicit that this is not enough on its own: "Although Istio proxies can automatically send spans, extra information is needed to join those spans into a single trace."

What the application must do: "collect headers from each incoming request and forward the headers to all outgoing requests triggered by that incoming request." The headers to forward:

- `x-request-id`, `traceparent`, `tracestate`
- For Zipkin, also the B3 set: `x-b3-traceid`, `x-b3-spanid`, `x-b3-parentspanid`, `x-b3-sampled`, `x-b3-flags`

Backends: Istio's extension providers in `MeshConfig` are OpenTelemetry, Zipkin, SkyWalking, Datadog and Stackdriver; Jaeger has its own setup page. Most backends accept the OpenTelemetry protocol. The Telemetry API configures the provider, sampling rate and header modification (the overview page gives no YAML).

How to use a trace to find a network problem: look for the span with the unexpected duration and note the **gap** between the client span's end and the server span's start (time spent in the network, a proxy, or a queue), then correlate with Hubble drops and DNS metrics for the same time window. Broken traces (separate root spans) mean header propagation failed; see the [OTCA scenario](../../otca/scenarios.md) on trace context.

**[📖 Istio distributed tracing](https://istio.io/latest/docs/tasks/observability/distributed-tracing/overview/)** - span generation, headers, backends

---

## Auditing traffic with logs

### Istio access logs

Envoy writes one line per request to standard output. The Telemetry API turns it on:

```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: mesh-default
  namespace: istio-system
spec:
  accessLogging:
    - providers:
      - name: envoy
```

The alternative is `meshConfig.accessLogFile: /dev/stdout` (or `istioctl install ... --set meshConfig.accessLogFile=/dev/stdout`); `accessLogEncoding` is `JSON` or `TEXT` and `accessLogFormat` sets a custom format. The `demo` profile enables access logging by default. Read the logs from the proxy container:

```bash
kubectl logs -l app=curl -c istio-proxy
kubectl logs -l app=httpbin -c istio-proxy
```

The same request appears in both the client's and the server's proxy logs, with method, path, protocol, response code, timing and upstream details. For an egress gateway, use `kubectl logs -l istio=egressgateway -c istio-proxy -n istio-system` to confirm which external hosts were reached.

**[📖 Istio access logs](https://istio.io/latest/docs/tasks/observability/logs/access-log/)** - Telemetry API, meshConfig, reading logs

### Hubble flow logs

`hubble observe` shows network flows and is the fastest way to see policy drops:

```bash
hubble observe --pod deathstar --protocol http
hubble observe --pod deathstar --verdict DROPPED
```

Other filters from the CLI page: `--encrypted` and `--unencrypted` (flows encrypted with WireGuard or IPsec or not), `--reply` and `--not-reply`. A flow line shows timestamp, source and destination as `namespace/pod:port`, an arrow (`->` request, `<-` response, `<>` denied connection attempt), the event type, the verdict (`FORWARDED` or `DROPPED`) and details. Run `hubble status` to confirm you can reach the Hubble API (and `cilium status` first to confirm Cilium and Hubble are running).

A policy debugging loop: reproduce the failure, run `hubble observe --verdict DROPPED` for the source Pod, read which policy event dropped it, fix the NetworkPolicy, and watch the verdict flip to `FORWARDED`.

**[📖 Hubble CLI](https://docs.cilium.io/en/stable/observability/hubble/hubble-cli/)** - observe filters and flow format

### Kubernetes audit logs

API-level audit (who created a NetworkPolicy or Gateway) is covered in [CNPE note 05](../../cnpe/notes/05-security-and-policy-enforcement.md).

---

## Key terms

- **Hubble** - Cilium's observability layer that records and exposes network flows and metrics.
- **Flow** - one observed network connection or packet event, with source, destination and verdict.
- **Verdict** - the outcome Hubble records for a flow, such as FORWARDED or DROPPED.
- **Prometheus metrics endpoint** - an HTTP path, usually `/metrics`, that Prometheus scrapes.
- **OpenMetrics** - a metrics exposition format that supports exemplars.
- **Exemplar** - a sample trace ID attached to a metric data point, linking metrics to traces.
- **Span** - one timed operation within a trace.
- **Trace context propagation** - forwarding headers such as `traceparent` so spans join into one trace.
- **Access log** - a per-request log line written by a proxy.
- **Telemetry API (Istio)** - the resource that configures metrics, tracing and access logging.
