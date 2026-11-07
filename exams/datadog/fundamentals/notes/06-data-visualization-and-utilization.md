---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 14 min
---

# 06 - Data Visualization and Utilization

**Exam guide domain 6: Data Visualization & Utilization**

Subdomains in the guide: Host Map, dashboards, using metrics, using tags, monitors and alerts.

The overview page describes this area as dashboards and data use, and the exam guide outline (dated 2022) breaks it into the five subdomains above. The guide's topic list also says the exam covers aggregating and visualizing data, searching and filtering events, logs and metrics with tags and facets, and creating monitors with targeted notifications. Interface names change between releases, so check labels against your own account. Nothing was run for this guide.

---

## From collected data to decisions

Collecting data is only half of monitoring. This domain is the other half: looking at what you collected, narrowing it to what matters, and making Datadog tell you when it changes. The same four ideas repeat across every product: **scope** (which data), **aggregation** (how to combine it), **display** (how to draw it) and **action** (what happens when it crosses a line).

---

## Host Map

The **Host Map** (under Infrastructure) draws every host as a **hexagon** in a map of your infrastructure. Its purpose is to let you see the health of an entire fleet in one glance and to spot the outlier.

Three controls shape it:

- **Filter** narrows the hosts shown using tags, for example `env:prod`.
- **Group by** clusters hexagons by one or more tags, for example by availability zone or by team. Tags are the thing that makes the map useful, which links this subdomain to tagging.
- **Fill** and **Size** choose a metric to represent as color and as hexagon size. A common view colors by CPU utilization and sizes by memory, so a large red hexagon is a big, busy machine.

Clicking a hexagon opens the host's detail panel with its metrics, tags and integrations. The **Container Map** works the same way for containers.

What the exam wants is the reasoning: the Host Map answers "which hosts in this group look different from the others", at a glance, using tag grouping and a metric for color. A related page, the **Infrastructure List**, shows the same hosts as a table you can sort.

**[📖 Datadog docs: Host Map](https://docs.datadoghq.com/infrastructure/hostmap/)** - filter, group, fill and size

---

## Using metrics

### Metrics Explorer and the Metrics Summary

The **Metrics Summary** page lists the metrics Datadog has received, with their type, unit, the tags they carry and how many timeseries they produce. It is where you check that a custom metric arrived and how it is tagged. The **Metrics Explorer** lets you graph a metric quickly by choosing the aggregation, the scope and the grouping, without building a dashboard.

### The query editor

Graph widgets use a query built from the same parts you met earlier:

```
avg:system.cpu.user{env:prod,service:checkout} by {host}
```

In the editor you select: the **metric**, the **scope** ("from" tags to include), the **space aggregation** (avg, sum, min, max) and the **group by**. You can add **functions** to transform the series. The ones named in beginner material include **rate** and **derivative** (turn a running total into change per time), **rollup** (set the time bucket and method), **moving average** and **timeshift** (compare with a previous period), and **arithmetic** to combine queries into a formula, such as errors divided by requests.

### Choosing the aggregation

The aggregation must match the metric's meaning. For percentages and gauges you usually want **average** or **maximum** across hosts. For counts and rates you often want **sum**. Percentiles of latency across a fleet need a **distribution** metric, not an average of per-host percentiles. Many wrong dashboards come from a mismatch here.

### Events and logs

The guide's topic list says you should be able to "search and filter events, logs and metrics using tags and facets". The **Event Explorer** lists events (a deployment, an Agent start, a monitor alert), and **Log Explorer** lists log lines. Both support a search bar with a query syntax, plus a list of **facets** on the left. A **facet** is a field that has been indexed for filtering and grouping, such as `host`, `service` or `status`. Clicking a facet value adds it to the search. Tags are the common vocabulary: `env:prod` works to narrow metrics, events and logs the same way.

---

## Using tags

Tags appear again here as a tool of use, rather than of collection.

- **Scope a query**: the braces in a metric query select by tag.
- **Group a result**: `by {tag}` produces a line per value.
- **Filter views**: the Infrastructure List, Host Map, dashboards and monitors all accept tag filters.
- **Template variables on dashboards**: a dashboard can define a variable bound to a tag key, such as `$env` or `$host`, and a dropdown at the top lets the viewer switch every widget at once.
- **Scope monitors**: a monitor's query uses tags to decide what it watches and whether to alert per group.

A tag that is a different shape on different data (`environment` in one place, `env` in another) breaks all of these. The consistent-tags rule in the data collection note is what makes this note work.

---

## Dashboards

A **dashboard** is a collection of **widgets**, each showing a metric, a log search, a list of events, a note or an image. Dashboards are how teams share a view of a system.

### Layouts

Datadog offers two traditional layouts, described in the docs. A **timeboard** (grid layout) is an automatically arranged grid where every graph shares the same time range, which suits troubleshooting because the graphs line up in time. A **screenboard** (free layout) allows widgets to be placed anywhere, with widgets that can use different time ranges, which suits status displays. The product now presents them as dashboards with a choice of layout, so check the current labels.

### Common widgets

| Widget | Use |
|---|---|
| **Timeseries** | a line, area or bar graph of metrics over time |
| **Query value** | one number, such as current error rate |
| **Top list** | the highest or lowest values, such as busiest hosts |
| **Heat map** | the distribution of a metric over time |
| **Table** | rows of values by group |
| **Host Map** | the map widget embedded in a dashboard |
| **Event stream and log stream** | live lists |
| **Note** | text to explain the dashboard |

### Building one

The usual route is: **create a new dashboard**, choose a layout, **add widgets** by dragging them onto the page, **edit** each to set its query and display options, set the **time range**, and add **template variables** for the tags people will want to switch. Widgets can also be added straight from a Metrics Explorer graph with an **export to dashboard** option.

### Sharing and good practice

Dashboards can be **shared** by link, with restricted access, or as a read-only public URL where appropriate. Good practice is to put the most important information in the top-left, to **title every widget** in plain language, to include a note explaining the purpose, and to avoid dozens of widgets that nobody reads. A dashboard answers a defined question for a defined audience.

**[📖 Datadog docs: Dashboards](https://docs.datadoghq.com/dashboards/)** - layouts, widgets and sharing

---

## Monitors and alerts

A **monitor** watches data and **notifies** when a condition is met. It is how Datadog turns observation into action. Whereas a dashboard needs a person looking, a monitor works unattended.

### Monitor types

The docs list many types. The ones to recognize at this level:

| Type | Watches |
|---|---|
| **Metric** | a metric crossing a threshold, changing, or behaving anomalously |
| **Host** (check) | whether the Agent on a host is reporting at all |
| **Integration** | the status or metrics of an integration, such as a database |
| **Process** | whether a process is running on a host |
| **Log** | the number of logs matching a query |
| **APM** | request rate, error rate or latency for a service |
| **Anomaly, Outlier, Forecast** | unusual behavior, a host differing from its peers, or a predicted breach |
| **Composite** | a combination of other monitors with boolean logic |
| **Event** | events matching a query |

The metric monitor is the one most often tested. It has **detection methods**: a simple **threshold** (alert if above or below a number), **change** (alert if the value moves by a given amount or percent over a period), **anomaly** (alert when behavior departs from the normal pattern) and **outlier** (alert if one member of a group differs from the rest).

### Defining a metric monitor

The creation flow follows a fixed order:

1. **Choose the detection method.**
2. **Define the metric** with the same query editor as dashboards: metric, scope, aggregation and group by.
3. **Set the alert conditions:** the threshold, the direction (above or below), and the **evaluation window** (for example, average over the last five minutes). Optionally add a **warning** threshold below the alert one, and **recovery** thresholds.
4. **Configure no-data behavior:** decide what to do if no data arrives (notify, or not).
5. **Write the notification:** a title and a message.
6. **Choose who to notify** by adding **@-handles** in the message: `@person@example.com`, a team channel in a chat tool, a paging service or a webhook.
7. **Save.**

A monitor with a group by on `host` is a **multi-alert** monitor and creates one alert per host, so the alert tells you which host. A monitor without a group by is a **simple alert** and evaluates the aggregate once.

### States

A monitor is always in a **status**: **OK**, **Warn**, **Alert** or **No Data**. A change of status is what triggers a notification. The evaluation window and a **notify on no data** setting determine how the monitor behaves when the source goes silent, which is important: an Agent that dies stops sending data, and without a no-data alert the monitor would sit quietly at its last status.

### Targeted notifications

The exam guide says monitors with "targeted notifications". The message supports **template variables** such as the host name or the metric value, and **conditional blocks** that show text only in the alert state or the recovery state. Those let one monitor send different messages to different people, for instance paging the on-call engineer on Alert and posting a quieter note to a chat channel on Warn. Tagging the monitor itself lets teams find and filter their monitors.

### Muting

A **downtime** silences notifications for a scope and period, such as during planned maintenance, so that people are not alerted for expected conditions. Downtime stops notifications, but monitors still evaluate.

### Alert design

Good alerts are **actionable**, **specific** and **rare enough to be trusted**. Alert on symptoms users feel (error rate, latency) rather than on every cause, add a warning level before the alert level, and attach a message that says what to check first. Alerts that fire constantly teach people to ignore them.

**[📖 Datadog docs: Monitors](https://docs.datadoghq.com/monitors/)** - types, thresholds and notifications

---

## Bringing it together

A short example shows how the pieces connect. A team tags every host with `env`, `service` and `team`. Their Host Map groups hosts by `service` and colors by CPU, so they notice one `checkout` host in red. They open the host panel, then graph `avg:system.cpu.user{service:checkout} by {host}` and confirm one host stands out. They add the graph to the checkout dashboard with a `$env` template variable. Finally they create a multi-alert metric monitor on the same query, grouped by host, with a warning and an alert threshold, a no-data setting, and a message that tags the team's chat channel. Every step used tags as the shared language.

---

## Key terms

- **Host Map** - a view that draws each host as a hexagon, grouped by tags and colored and sized by metrics.
- **Group by** - a control or query clause that splits data into separate groups by a tag.
- **Fill** - the Host Map setting that chooses the metric shown as hexagon color.
- **Size** - the Host Map setting that chooses the metric shown as hexagon size.
- **Metrics Summary** - the page that lists received metrics with their type, tags and timeseries counts.
- **Metrics Explorer** - the page for quickly graphing a metric with chosen aggregation and scope.
- **Scope** - the part of a query, in braces, that selects data by tag.
- **Function** - a transformation applied to a metric query, such as rate, rollup or timeshift.
- **Facet** - an indexed field in logs or events used to filter and group results.
- **Template variable** - a dashboard control bound to a tag key that changes every widget at once.
- **Dashboard** - a page of widgets that display metrics, logs, events and notes.
- **Timeboard** - a grid dashboard layout where all graphs share one time range.
- **Screenboard** - a free-layout dashboard where widgets can be placed anywhere.
- **Widget** - a single display element on a dashboard, such as a timeseries or top list.
- **Monitor** - a configured check that watches data and sends notifications when a condition is met.
- **Threshold** - the value at which a monitor changes status.
- **Evaluation window** - the time period over which a monitor evaluates its query.
- **Multi-alert** - a monitor grouped by a tag that alerts separately for each group.
- **Simple alert** - a monitor that evaluates one aggregate and sends one alert.
- **No Data** - a monitor status meaning the monitored source has stopped reporting.
- **@-handle** - a mention in a monitor message that notifies a person, channel or service.
- **Downtime** - a scheduled silencing of monitor notifications for a scope and period.
- **Composite monitor** - a monitor that combines other monitors with boolean logic.
