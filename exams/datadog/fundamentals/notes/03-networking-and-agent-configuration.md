---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 13 min
---

# 03 - Networking and Agent Configuration

**Exam guide domain 3: Networking & Agent Configuration**

Subdomains in the guide: Datadog ports, Datadog IP addresses, Auto-discovery.

The exam guide lists these three subdomains without weights. The port numbers here are the long-standing defaults from the Datadog "Network traffic" documentation; they can change between Agent versions, so confirm against the page for the version you run. Nothing here was run for this guide.

---

## The shape of Agent networking

Understanding the Agent's networking comes down to separating **two directions of traffic**.

**Outbound** traffic goes from the Agent to Datadog: the metrics, logs, traces and other data. This is by far the most important. The Agent opens connections out to Datadog's endpoints over **HTTPS**, so on a locked-down network the usual task is to allow outbound access to the right addresses and port.

**Local** traffic stays on the machine or its network: your applications sending custom metrics or traces to the Agent, the Agent's own command-line tool talking to its running process, and the optional local web interface. These use **local ports** on the host, mostly bound to the loopback address so that they are not reachable from the network.

If you keep that split in mind, most questions answer themselves. "A firewall blocks inbound traffic; will the Agent still report?" Yes, because the Agent mostly initiates outbound connections. "A containerized application cannot send DogStatsD metrics to the Agent." That is a local-traffic problem, about the address and port the application is pointing at.

**[📖 Datadog docs: Agent network traffic](https://docs.datadoghq.com/agent/configuration/network/)** - ports and destinations

---

## Datadog ports

### Outbound

Data from the Agent to Datadog travels over **TCP port 443** (HTTPS) for metrics, traces, logs, process data and most other products on current Agent versions. Older documentation mentions a separate TCP port for log forwarding; current versions send logs over HTTPS on 443 as well, and a TCP option exists for environments that need it. The practical lesson for firewall questions is "443 outbound" in nearly every case, with the destination domains or addresses coming from the docs.

### Local ports on the Agent host

| Port | Protocol | Purpose |
|---|---|---|
| 8125 | UDP | DogStatsD, the listener for custom metrics |
| 8126 | TCP | APM trace receiver, where tracing libraries send traces |
| 5000 | TCP | the Agent's runtime statistics (expvar) |
| 5001 | TCP | the Agent's internal command channel, used by `datadog-agent` commands |
| 5002 | TCP | the Agent's graphical interface (on platforms that offer it) |
| 6062 / 6162 | TCP | debug endpoints for the process Agent |

Two points to learn from the table. First, **8125 is UDP** and **8126 is TCP**. The same family of numbers with different protocols is an easy slip. Second, ports such as 5001 and 5002 are for the Agent's own tooling and are bound to `localhost`; they should never be exposed to the internet.

You can change these in `datadog.yaml` (for example `dogstatsd_port` and the APM receiver port) when something else on the host already uses them. A "port already in use" error in the Agent logs is the classic symptom, and the `ss -lntu` command shows what is listening where.

### Containers

Inside containers, the Agent listens on the same ports, but the *address* an application should use differs. Applications on the same Docker host reach the Agent either through a **host port mapping** or through an **internal network address**; on Kubernetes the common patterns are the node's host IP, a Unix domain socket mounted into the pod, or a Kubernetes service. In each case the application's configuration needs the Agent's address, and `localhost` inside a container refers to the container itself, not the host. That is the reason DogStatsD "works from the host but not from the app container".

---

## Datadog IP addresses

Some organizations cannot allow outbound traffic to the whole internet, only to named destinations. Datadog supports this by publishing its address ranges.

The ranges are available as **JSON documents** at Datadog's **IP ranges** service, with one list per product (for example, Agent traffic, API, logs, synthetics and webhooks). Each list contains IPv4 and IPv6 prefixes. The point of publishing them as data is that you can **fetch them automatically** and update firewall rules from them, instead of copying a static list that goes stale. Datadog states that the ranges change over time and that the lists carry version and modified-date fields so automation can tell whether anything changed.

Several practical details matter:

- The ranges differ by **site**, so use the one for the site you are on.
- Different **product** categories use different ranges. A firewall allowing only the Agent range will block webhooks coming *from* Datadog to your servers, which come from a different list.
- A **proxy** can simplify rules: send all Agent traffic through one proxy host and allow only that host out. The Agent supports HTTP and HTTPS proxies via configuration.
- Domain names are an alternative to IP addresses where the firewall supports them.

**[📖 Datadog docs: IP ranges](https://docs.datadoghq.com/api/latest/ip-ranges/)** - the endpoint and how to read it

---

## Agent configuration files

Before the third subdomain, a short tour of where configuration lives, because auto-discovery is a configuration feature. (The troubleshooting note covers the files in more detail.)

- **`datadog.yaml`** is the main configuration file. It holds your API key, site, hostname, tags, proxy settings and switches for optional features such as log collection, APM and process monitoring.
- **`conf.d/`** is a directory holding one subdirectory per integration, named `<integration>.d`. Inside is a `conf.yaml` for that integration, and a `conf.yaml.example` showing every option. Each `conf.yaml` has an `init_config` section and an `instances` list; each instance is one thing to monitor, such as one database.
- **`auto_conf.yaml`** files appear inside some integration directories and are the templates used by auto-discovery.

Environment variables can override or provide most `datadog.yaml` settings, using the `DD_` prefix, which is why container deployments seldom edit files at all.

---

## Auto-discovery

On a static server, you can list what to monitor in a file and be done. In a world of containers that start, stop and move, the address of a database might change many times a day, and nobody can keep a file up to date by hand. **Autodiscovery** solves this by letting the Agent watch the orchestrator, notice when containers start or stop, and **apply configuration templates automatically**.

The Agent is told three things by a template:

1. **Which containers** it applies to, using an **identifier** such as the image name or a custom label.
2. **Which integration check** to run on them.
3. **The settings** for the check, using **template variables** in place of values that are only known at runtime, such as the container's IP address and port.

### Template variables

Two are the standard examples:

- `%%host%%` is replaced with the container's IP address.
- `%%port%%` is replaced with the exposed port of the container.

A template for a web server check might therefore say "connect to `%%host%%` on `%%port%%`", and the Agent fills in each new container's real values.

### Where templates come from

The docs describe several **template sources**, and the exam is likely to ask you to match a source with a situation.

| Source | How it works |
|---|---|
| **Integration auto-configuration files** | Built-in `auto_conf.yaml` templates ship with the Agent for popular software, so common images are monitored with no extra setup |
| **Container labels or pod annotations** | You attach labels (Docker) or annotations (Kubernetes) to the container itself, naming the check and its settings, so the configuration travels with the workload |
| **Configuration files** | You place a template file in the Agent's `conf.d` directory with an identifier listing which containers it applies to |
| **Key-value store** | Templates held in a store such as etcd or Consul that the Agent reads |
| **Kubernetes Custom Resources and other newer methods** | Described in the docs for specific orchestrators |

On Kubernetes, annotations on a pod take a name of the form `ad.datadoghq.com/<container-name>.checks`, holding a JSON description of the checks to run. A template file uses `ad_identifiers` to name which container images it applies to. These details are in the docs page named "Autodiscovery"; learn the pattern rather than the exact string.

```yaml
# Illustrative template shape (verify field names against the Autodiscovery docs)
ad_identifiers:
  - nginx
init_config:
instances:
  - nginx_status_url: http://%%host%%:%%port%%/nginx_status
```

The example reads: for any container whose image is identified as `nginx`, run the nginx check against that container's own address and port. The exact field set is documented per integration.

### Why it matters

Autodiscovery is how Datadog's container monitoring stays current without a human. It also explains a common troubleshooting scenario: an integration check does not appear for a new container. The usual causes are an identifier that does not match the image name, a template variable that resolved to nothing, or a label or annotation with a typo. The Agent's `configcheck` command shows which configurations it resolved, and the `status` command shows whether the check is running.

**[📖 Datadog docs: Basic Agent Autodiscovery](https://docs.datadoghq.com/containers/docker/integrations/)** - Docker labels and templates; the Kubernetes version is under the containers section

---

## Putting the three together

A realistic story shows how the subdomains connect. A team deploys the Agent as a DaemonSet in a locked-down cluster. They allow outbound 443 to the Agent address list fetched from the IP ranges service. Application pods send custom metrics to the node's Agent on UDP 8125 using the node's host address. Their NGINX pods carry annotations so that the Agent starts an NGINX check as soon as each pod appears, using `%%host%%` and `%%port%%`. If any link breaks, the symptom is distinct: no data at all from the node suggests outbound traffic, missing custom metrics suggests local port or address problems, and a missing integration suggests a template problem.

---

## Key terms

- **Outbound traffic** - connections the Agent opens to Datadog, normally HTTPS on port 443.
- **Local traffic** - connections between applications or tools and the Agent on the same host or network.
- **Port 8125** - the UDP port where DogStatsD listens for custom metrics.
- **Port 8126** - the TCP port where the APM trace receiver listens.
- **Port 5001** - the local port the Agent's own command line uses to talk to the running Agent.
- **Port 5002** - the local port serving the Agent's graphical interface.
- **IP ranges service** - the Datadog endpoint that publishes address ranges per product as JSON.
- **Proxy configuration** - Agent settings that route outbound traffic through an intermediary host.
- **datadog.yaml** - the Agent's main configuration file.
- **conf.d** - the directory of per-integration configuration folders.
- **conf.yaml** - the configuration file for one integration, containing init_config and instances.
- **Instance** - one thing an integration monitors, such as one database or one web server.
- **Autodiscovery** - the Agent feature that watches an orchestrator and applies check templates to containers automatically.
- **auto_conf.yaml** - a built-in template file that enables a check for a known container image.
- **ad_identifiers** - the setting that names which containers a template file applies to.
- **Template variable** - a placeholder such as %%host%% or %%port%% filled in at runtime.
- **Pod annotation** - a Kubernetes metadata entry that can carry Autodiscovery check configuration.
