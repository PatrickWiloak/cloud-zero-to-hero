---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 12 min
---

# 06 - Creating Scheduled Reports and Alerts

**Blueprint domain 8.0 Creating Scheduled Reports and Alerts (5%)**

Blueprint topics: describe scheduled reports, configure scheduled reports, describe alerts, create alerts, view fired alerts.

Menu paths are from the Splunk Alerting Manual and Reporting Manual and were not run for this guide. This is the lightest domain by weight, but it is also the point at which Splunk stops waiting for you and starts working on its own, so the ideas are worth understanding properly.

---

## Why anything runs without you

Until now every search has run because a person pressed a button. That is fine for investigation and useless for monitoring. Nobody can sit and re-run a search every five minutes waiting for a failure. **Scheduling** tells Splunk to run a saved search by itself at set times. **Alerts** add a condition: run the search, and *if the results meet a rule, do something*.

The difference to hold in your head: a **scheduled report** runs on a timetable and delivers results regardless of what they contain. An **alert** runs on a timetable (or continuously) and acts only when its trigger condition is true.

---

## Scheduled reports

A scheduled report is an ordinary report with a schedule attached. You can schedule one when you save it or later through **Edit > Edit Schedule** on the Reports page.

### Configuring the schedule

The dialog asks for:

- **Schedule Report**: tick to turn scheduling on.
- **Schedule**: how often. Common choices are every hour, every day, every week, every month, or a **cron schedule**, a five-field expression for precise timing (for example, minute, hour, day of month, month, day of week).
- **Time Range**: the window of data each run covers, such as the last 24 hours. Note that this is separate from the schedule: running every hour over the last 24 hours is legitimate.
- **Schedule Priority**: how important the run is when the system is busy.
- **Schedule Window**: a period during which Splunk may start the run late if the system is loaded, which helps spread out many reports scheduled for the same moment.
- **Trigger Actions**: what to do when the report runs. For a scheduled report the usual actions are to send an email, run a script or log an event.

A scheduled report can **send email** with results inline, as an attachment (a PDF or CSV), or as a link back to Splunk. This is the standard way to get a weekly summary to people who never log in.

### Why scheduled reports matter beyond email

Scheduled reports are **run in the background and their results are kept**. When a dashboard panel or a report uses that saved result, it loads quickly, because the work was already done. This is how large dashboards stay fast. Scheduling is also required for some features: for example, embedding a report in an external web page depends on it being scheduled.

A scheduled run counts toward resource limits, so avoid scheduling many heavy searches at the same minute. The schedule window and priority settings exist for that reason.

**[📖 Reporting Manual: Schedule reports](https://docs.splunk.com/Documentation/Splunk/latest/Report/Schedulereports)** - frequency, window and priority

---

## Alerts

An **alert** is a saved search that runs on a schedule (or in real time) and **triggers actions when its results meet a condition**. Typical uses: more than a threshold of failed logins in ten minutes, a service that has gone silent, an error rate that jumps.

### Describing the two kinds

Splunk offers two types, distinguished by how the search runs.

| Alert type | How it runs | Typical use |
|---|---|---|
| **Scheduled alert** | runs on a schedule you set, over a defined time range | regular checks where a few minutes of delay is fine |
| **Real-time alert** | runs continuously on live data in a sliding window | conditions that need an immediate response |

Real-time searches are expensive because they stay running, so scheduled alerts are the preferred default. A real-time alert can be set to trigger **per result** (every matching event fires) or **rolling window** (the condition is checked over a moving period of time).

### Trigger conditions

The trigger condition is the rule that decides whether to act. For scheduled alerts the choices are:

- **Number of Results** is greater than, less than, or equal to a value. This is the simplest and most common.
- **Number of Hosts** and **Number of Sources**: the count of distinct hosts or sources in the results.
- **Custom**: a condition you write as a search expression on the results.

Then there is the question of how often to act when the condition stays true. The **Trigger** setting offers **Once**, which fires one time for the whole result set, and **For each result**, which fires once per row.

**Throttling** suppresses repeat alerts for a chosen period after one fires. With a failing system, an alert that emails every five minutes becomes noise, and people begin to ignore it. Throttling is the cure, and a question about "avoid being flooded with the same alert" is pointing at it. The setting is a time period (and can be limited to a field value, so each host is throttled separately).

### Trigger actions

When the condition is met, the alert performs one or more **trigger actions**:

- **Add to Triggered Alerts**: records the alert in a list inside Splunk.
- **Send email**: to named recipients, with a subject and message, optionally including the results.
- **Run a script**: execute a script on the Splunk server.
- **Log events** or **output results to a lookup**.
- **Webhook**: send an HTTP POST to a URL, used to notify chat tools and ticket systems.
- Actions added by apps, such as paging services.

You can attach several actions to one alert and set a **severity** (info, low, medium, high, critical) that appears in the triggered alerts list.

**[📖 Alerting Manual: Getting started with alerts](https://docs.splunk.com/Documentation/Splunk/latest/Alert/AlertWorkflowOverview)** - types, conditions and actions

---

## Creating an alert

The steps, from the search page:

1. Run and test the search. An alert is only as good as its search, so confirm it returns what you expect for both the quiet and noisy cases.
2. Choose **Save As > Alert**.
3. Fill in the **Title** and optional **Description**.
4. Set **Permissions** (private or shared in the app).
5. Choose **Alert type**: scheduled (choose how often) or real-time.
6. Set the **Time Range** for a scheduled alert.
7. Set the **Trigger Conditions**: result count comparison, once or per result, and throttle if wanted.
8. Add **Trigger Actions**.
9. Save.

A useful discipline is to **design the search so the alert condition is simple**. Rather than a complex custom condition, write the search so that it returns rows *only* when something is wrong, and then trigger when the number of results is greater than zero. For example, count failed logins by user in the search, keep only users with more than some threshold, and alert on any result at all.

---

## Viewing fired alerts

If the alert includes **Add to Triggered Alerts**, each firing appears in the **Alerts** page (a tab in the Search & Reporting navigation, or **Activity > Triggered Alerts**). The list shows the alert name, the time it fired, the severity, the app and the owner. Selecting **View results** opens the search that was run at that moment, with the events that caused the trigger, and you can then dig deeper. That works for as long as the job results are retained, so a very old firing may only show that it happened.

You can also review the alert's own **history**: find it on the **Alerts** page (the list of alert definitions, as opposed to the fired list), open its detail, and you will see when it ran and whether it fired. Editing from there lets you change the schedule, conditions or actions.

When an alert does not fire, work through a sequence: did the schedule run (look at the **Jobs** list or the scheduler logs), did the search return results in that window, did the trigger condition evaluate to true, was it throttled, and did the action itself fail (for example, an email server not configured). The exam keeps to the simpler questions: describing what each alert type does and where to see fired alerts.

**[📖 Alerting Manual: Managing triggered alerts](https://docs.splunk.com/Documentation/Splunk/latest/Alert/Managingalerts)** - the triggered alerts list

---

## Scheduled report or alert

| If the person wants | Use |
|---|---|
| a regular summary sent to them, whatever the results | scheduled report |
| to be told only when something crosses a line | alert |
| the result of a heavy search ready when the dashboard opens | scheduled report |
| immediate action on a single event | real-time alert, per result |
| to stop duplicate notifications | alert throttling |

---

## Key terms

- **Scheduled report** - a report set to run automatically on a timetable.
- **Cron schedule** - a time expression with minute, hour, day of month, month and day of week fields for precise scheduling.
- **Schedule window** - a period during which Splunk may delay a scheduled run to ease load.
- **Schedule priority** - a setting that ranks how important a scheduled run is when the system is busy.
- **Alert** - a saved search that triggers actions when its results meet a condition.
- **Scheduled alert** - an alert that runs on a timetable over a set time range.
- **Real-time alert** - an alert whose search runs continuously on live data.
- **Per-result trigger** - a real-time or scheduled setting that fires the alert once for every matching result.
- **Trigger condition** - the rule, such as number of results greater than a value, that decides whether an alert fires.
- **Throttling** - suppressing repeat alerts for a set period after one has fired.
- **Trigger action** - something an alert does when it fires, such as sending email or calling a webhook.
- **Add to Triggered Alerts** - an action that records the firing in the Splunk list of fired alerts.
- **Webhook** - an action that sends an HTTP request to an outside URL when an alert fires.
- **Severity** - a label from info to critical attached to a fired alert.
- **Triggered alerts list** - the page that shows when alerts fired and lets you view their results.
