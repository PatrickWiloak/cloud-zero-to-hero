---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 16 min
---

# 04 - Data Collection

**Exam guide domain 4: Data Collection**

Subdomains in the guide: DogStatsD, crawlers, Agent integrations, API endpoints, tagging best practices, metrics and timeseries.

This is the longest outline in the guide (six subdomains) and the one closest to everyday Datadog work, so give it the most time. The guide publishes no weights. The syntax below follows the Datadog documentation and was not run for this guide.

---

## The ways data gets into Datadog

There are four routes in, and every subdomain in this domain is one of them or a concept about what comes through them.

| Route | Who gathers the data | Typical use |
|---|---|---|
| **Agent integrations** (checks) | The Agent, by connecting to a technology on or near the host | databases, web servers, queues, system metrics |
| **DogStatsD** | Your application sends numbers to the Agent's local listener | custom application metrics |
| **Crawlers** | Datadog itself calls a service's API using credentials you supply | cloud providers and SaaS products |
| **The API** | Your own code or scripts call Datadog's HTTP API | automation, one-off submissions, anything the other routes do not cover |

A quick test for choosing: if the technology runs where you can install an Agent, use an integration. If it is your own code and you decide what to count, use DogStatsD or a tracing/logging library. If it is a hosted service where you cannot install anything, use a crawler. If nothing else fits, use the API.

---

## Metrics and timeseries

A **metric** is a named measurement collected over time, such as `system.cpu.user` or `nginx.net.request_per_s`. A **timeseries** is a metric for one specific combination of tags, as a list of timestamped values. `system.cpu.user` on host `web-01` is one timeseries; on host `web-02` it is another. When you hear "how many timeseries does this metric have", it means how many distinct tag combinations exist.

### Anatomy of a data point

A data point has a **metric name**, a **value**, a **timestamp**, and a set of **tags**. Metric names use dots to group related metrics: the namespace comes first (`system.`, `nginx.`, or your own prefix), then the measurement. Custom metrics should have a prefix that makes their owner clear.

### Metric types

The **type** says how Datadog should interpret what was submitted, and affects how values are aggregated and displayed. The submission types are:

| Type | What it represents | Example |
|---|---|---|
| **Count** | the number of events during an interval; submitted values are added together | requests served in the last ten seconds |
| **Rate** | a count divided by the interval, per second | requests per second |
| **Gauge** | a value at a moment; the last value in the interval is kept | memory in use, queue depth, temperature |
| **Histogram** | a distribution of values over the interval, summarized by the Agent into count, average, median, maximum and percentiles | request durations |
| **Distribution** | like a histogram, but aggregated globally across hosts on the Datadog side, so percentiles are over all data | latency across a fleet |

The central contrast is **count versus gauge**. A count adds up; a gauge is a snapshot. Total requests handled is a count. Current connections is a gauge. Treating a gauge as a count produces nonsense when you sum it over time. The second contrast is **histogram versus distribution**: a histogram's percentiles are computed on each Agent, so a percentile averaged across hosts is a poor answer; a distribution sends the raw values so the platform can compute true fleet-wide percentiles.

### Aggregation and rollup

When you graph a metric, Datadog applies two kinds of aggregation. **Space aggregation** combines timeseries across tags: average, sum, minimum or maximum across hosts, optionally grouped "by" a tag. **Time aggregation** or **rollup** combines the points inside each time bucket on the graph, because a month of ten-second data cannot be drawn point by point. The default rollup method depends on the metric type, and you can set it explicitly. Choosing the right space aggregation is the most common step where graphs go wrong, for example summing a percentage across hosts.

### Query shape

A metric query reads like this:

```
avg:system.cpu.user{env:prod} by {host}
```

The parts are: the **aggregator** (`avg`), the **metric**, the **scope** in braces (which tags to include), and an optional **group by**. Reading a query aloud in that order is a skill the exam draws on, and you meet it again in the visualization note.

**[📖 Datadog docs: Metrics types](https://docs.datadoghq.com/metrics/types/)** - count, rate, gauge, histogram and distribution

---

## Agent integrations

An **integration** connects Datadog to a technology. Most are delivered as **Agent checks**: Python code, shipped with the Agent, that connects to a service and reports metrics, events and service status. There are hundreds, from system and network checks to databases, web servers, message queues and orchestrators.

### Using an integration

The steps follow a pattern:

1. **Install the Agent** on a host that can reach the technology.
2. **Create the integration's configuration**: copy `conf.yaml.example` in the integration's `conf.d/<name>.d/` directory to `conf.yaml` and edit it with the connection details (host, port, and a credential if needed).
3. **Prepare the technology**, if it needs it, for example creating a read-only monitoring user in a database.
4. **Restart the Agent** so that it loads the new configuration.
5. **Validate** with `datadog-agent status`, which lists the check under "Running Checks" and shows any errors.
6. **Check the Datadog site**: the integration tile reports the status, and the metrics appear under the integration's name.

A `conf.yaml` has two top-level sections. `init_config` holds settings that apply to the whole check. `instances` is a list, each item describing one target. One check can therefore monitor several databases or servers from one file.

```yaml
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: <PASSWORD>
```

The shape is illustrative. The real option names differ by integration, and the `conf.yaml.example` file in the Agent is the authoritative list.

### Which integrations ship with the Agent

The core Agent bundle includes common checks. Additional integrations can be installed with a command (`datadog-agent integration install`) as separate packages, and **custom checks** let you write your own Python code and place it in the Agent's `checks.d` directory with a matching config file. Writing one is beyond this exam, but knowing that the extension point exists is within reach.

### Integration tiles

In the web interface the **Integrations** page shows a tile for each integration, with installation steps, the metrics it collects and a place to enable it. For crawler-type integrations, the tile is where you enter credentials.

**[📖 Datadog docs: Integrations](https://docs.datadoghq.com/integrations/)** - the catalog and the setup pattern

---

## Crawlers

A **crawler** integration is one where **Datadog pulls the data from the other service's API** rather than the Agent gathering it. You give Datadog permission, usually a role, a key or a token with read access, and Datadog polls that service on a schedule.

The classic examples are the integrations for **cloud providers** (account-level data such as managed database metrics, load balancer statistics and cloud resource inventories) and for **SaaS products** (version control, chat, incident and ticketing systems). Nothing is installed on a host.

The contrasts with Agent-based integrations are the heart of the exam subdomain.

| | Agent integration | Crawler integration |
|---|---|---|
| Where code runs | on your host, in the Agent | on Datadog's side |
| What you install | the Agent | nothing; you grant access |
| Credentials | local connection settings | a role, key or token for the service's API |
| Data freshness | collected frequently by the Agent | pulled at a polling interval, typically slower |
| Best for | things you host | things someone else hosts |

Because crawlers poll, their data often **lags** Agent data by a few minutes, and they are limited by the target service's own API rate limits. Giving a crawler the **least privilege** it needs (read-only permissions) is a standing security recommendation.

A small point that helps with questions: a cloud provider's *virtual machines* are best monitored by installing the Agent on them, for depth, while the provider integration supplies the surrounding services that cannot run an Agent. Many deployments use both, and Datadog merges them under the same host when the names align, which loops back to the hostname discussion.

---

## DogStatsD

**DogStatsD** is the metrics server built into the Agent. It listens on a local **UDP port (8125)** for small text messages from your applications and forwards them to Datadog. It is an extension of the older StatsD protocol, adding **tags**, **histograms**, **distributions**, **events** and **service checks**.

### Why UDP

The application sends a packet and moves on. It does not wait for a reply and it cannot be slowed down or broken by a monitoring problem. That is a deliberate trade: metrics are cheap to emit and safe to emit often, at the price of possible loss if the packet never arrives. For monitoring counters and gauges, a rare lost packet is acceptable. A Unix domain socket option exists as an alternative transport.

### The message format

```
<METRIC_NAME>:<VALUE>|<TYPE>|@<SAMPLE_RATE>|#<TAG_KEY>:<TAG_VALUE>,<TAG_2>
```

The type codes are `c` for count, `g` for gauge, `h` for histogram, `d` for distribution, `ms` for timing (a histogram of milliseconds) and `s` for set (the number of unique values). The sample rate and tags are optional. A shell test might send a gauge with netcat:

```bash
echo -n "custom.queue.depth:12|g|#env:dev,team:payments" | nc -w 1 -u 127.0.0.1 8125
```

Reading it: the metric `custom.queue.depth` has the value 12, of type gauge, with two tags, sent by UDP (`-u`) to the Agent on localhost port 8125.

### Client libraries

Almost nobody writes the packet by hand. Datadog provides **client libraries** for common languages. In Python, for instance, a client offers calls such as `increment`, `gauge`, `histogram`, `distribution` and `timing`:

```python
from datadog import statsd

statsd.increment("web.page_views", tags=["env:prod", "page:home"])
statsd.gauge("queue.depth", 12, tags=["env:prod"])
```

The first call adds one to a count; the second records a gauge value. The libraries send to the local Agent by default.

### Things to know

- DogStatsD must be **enabled and reachable**; it is on by default in a host install, but in containers the application must point at the right address.
- The **sample rate** reduces traffic by sending only a fraction of events and letting Datadog scale the result back up.
- Metrics sent this way are **custom metrics**. They are billed by the number of distinct timeseries, so tags with unbounded values create cost. See the tagging section.

**[📖 Datadog docs: DogStatsD](https://docs.datadoghq.com/developers/dogstatsd/)** - protocol, transports and clients

---

## API endpoints

Datadog exposes an **HTTP API** for almost everything the web interface can do. Requests go to a base address that depends on your site, with a version in the path (`/api/v1/` and `/api/v2/` coexist), and every request carries the credentials in headers.

```bash
curl -X GET "https://api.datadoghq.com/api/v1/validate" \
  -H "DD-API-KEY: ${DD_API_KEY}"
```

That call checks that an API key is valid. A request that reads data or manages objects adds `-H "DD-APPLICATION-KEY: ${DD_APP_KEY}"`.

### What the exam expects

You should recognize the main uses and be able to read a request:

- **Submit metrics**: a POST to the metrics series endpoint with a JSON body of metric names, points and tags. Needs an API key.
- **Query metrics**: a GET to the query endpoint with a time window and a query string like the one earlier. Needs both keys.
- **Manage monitors, dashboards, downtimes, users**: create, read, update and delete through the matching endpoints. Needs both keys.
- **Post events**: record something that happened, such as a deployment.
- **Validate** a key.

HTTP verbs follow convention: GET reads, POST creates, PUT replaces or updates, DELETE removes. A response status in the 200s means success; a 403 indicates a credential or permission problem; a 429 means you have been rate limited and should slow down. Using the wrong **site** in the base address is the same trap as with the Agent.

Datadog also provides **official API client libraries** in several languages, and a command-line tool, which wrap the same endpoints. **Terraform** has a Datadog provider for managing monitors and dashboards as code.

**[📖 Datadog docs: API reference](https://docs.datadoghq.com/api/latest/)** - endpoints, parameters and examples

---

## Tagging best practices

**Tags** are labels attached to data, written as `key:value`, that let you filter, group and aggregate. They are the connective tissue of Datadog: monitors, dashboards, the Host Map and every query use them. The exam has a named subdomain for tagging best practices, so know the rules.

### Format

- Tags are written **`key:value`**. A tag with no colon is a simple label.
- Tags are **lowercased** automatically.
- They should **start with a letter** and use letters, numbers, underscores, minus signs, colons, periods and slashes. Other characters are converted to underscores.
- There is a **maximum length**; the docs state it on the tagging page.
- Datadog treats some **reserved keys** specially, including `host`, `device` and `source`, and the unified service tagging keys below.

### Where tags come from

| Source | Example |
|---|---|
| Set in `datadog.yaml` or `DD_TAGS` | host-level tags such as `env:prod` |
| Inherited from the cloud provider or orchestrator | availability zone, instance type, Kubernetes labels |
| Set in an integration's `conf.yaml` | tags for that instance |
| Sent with a DogStatsD or API submission | `tags=["page:home"]` |
| Added in the web interface | host tags |

### Unified service tagging

Datadog recommends three standard tags on everything so that metrics, traces and logs can be pivoted between: **`env`**, **`service`** and **`version`**. In containers they are set with `DD_ENV`, `DD_SERVICE` and `DD_VERSION`. Using them consistently means that from a latency graph you can jump to the traces and logs of the same service and environment.

### Good practice

- **Choose a small set of keys and use them everywhere**, with documented values. `env:prod` in one team and `environment:production` in another defeats grouping.
- **Keep values bounded.** Tagging with a user ID, a request ID or a timestamp creates a new timeseries for each value, which hurts performance and increases cost for custom metrics. Put high-cardinality identifiers in logs or traces instead.
- **Tag at the source** where you can, so the data is labelled for everyone.
- **Do not put secrets or personal data in tags.**
- **Prefer `key:value` over bare words** so you can group by the key.

The word to remember is **cardinality**: the number of distinct values a tag takes. Low cardinality (a handful of environments) is healthy; unbounded cardinality is the thing to avoid.

**[📖 Datadog docs: Getting started with tags](https://docs.datadoghq.com/getting_started/tagging/)** - format, assignment and unified service tagging

---

## Key terms

- **Metric** - a named measurement collected over time, such as system.cpu.user.
- **Timeseries** - the values of one metric for one combination of tags over time.
- **Count** - a metric type whose submitted values are summed over an interval.
- **Rate** - a metric type showing a count divided by the interval, per second.
- **Gauge** - a metric type that records a value at a moment, keeping the last value in each interval.
- **Histogram** - a metric type that summarizes the distribution of values on the Agent, giving count, average, median, maximum and percentiles.
- **Distribution** - a metric type that sends raw values so percentiles are computed globally across hosts.
- **Space aggregation** - combining timeseries across tags, for example averaging across hosts.
- **Rollup** - combining the points inside each time bucket when a graph is drawn.
- **Integration** - a connection between Datadog and a technology, usually an Agent check.
- **Check** - the code, usually Python, that the Agent runs to collect data from a technology.
- **init_config** - the section of an integration configuration that holds settings for the whole check.
- **instances** - the section of an integration configuration listing each target to monitor.
- **Custom check** - a check you write and place in the Agent's checks.d directory.
- **Crawler** - an integration where Datadog pulls data from another service's API using credentials you supply.
- **DogStatsD** - the Agent's built-in metrics server that listens for StatsD-style messages on UDP port 8125.
- **StatsD** - the original protocol for sending application metrics over UDP, extended by DogStatsD with tags and more types.
- **Sample rate** - the fraction of events a client sends, which Datadog scales back up.
- **Client library** - a language package that sends metrics, such as increment and gauge calls, to DogStatsD.
- **DD-API-KEY** - the request header that carries the API key.
- **DD-APPLICATION-KEY** - the request header that carries the application key.
- **Tag** - a key:value label attached to data to filter, group and aggregate it.
- **Unified service tagging** - the practice of setting env, service and version tags consistently across metrics, traces and logs.
- **Cardinality** - the number of distinct values a tag takes, which should stay bounded.
- **Custom metric** - a metric you submit yourself, billed by distinct timeseries.
