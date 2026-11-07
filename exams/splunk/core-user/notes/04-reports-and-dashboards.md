---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 13 min
---

# 04 - Creating Reports and Dashboards

**Blueprint domain 6.0 Creating Reports and Dashboards (12%)**

Blueprint topics: save a search as a report, edit reports, create reports that display statistics (tables), create reports that display visualizations (charts), create a dashboard, add a report to a dashboard, edit a dashboard.

Menu names are taken from the Splunk documentation. Splunk changes its interface between releases, so confirm labels on the version you practice with. Nothing here was run for this guide.

---

## What a report is

A **report** is a saved search, along with how to present its results. When you save one you are saving the *question* and the *formatting*, not the answer. Each time someone opens the report, Splunk runs the search again (unless it is set to use scheduled, cached results) and shows current data.

Reports matter for three reasons. They save you retyping. They can be **shared** with other people through permissions. And they are the **building blocks of dashboards**, because a dashboard panel is usually a report or a reference to one.

The two flavors the blueprint names are reports that display **statistics** (a table) and reports that display a **visualization** (a chart). The choice depends on whether the search ends in a transforming command and which tab you choose to save from. A report of raw events is also possible; it just lists events.

**[📖 Reporting Manual: Create and edit reports](https://docs.splunk.com/Documentation/Splunk/latest/Report/Createandeditreports)** - the saving and editing steps

---

## Saving a search as a report

The steps, in the interface:

1. Run a search in the Search & Reporting app.
2. Choose **Save As** at the upper right of the search page, then **Report**.
3. Give it a **Title**. Add a **Description** if others will use it.
4. Choose whether to include the **time range picker** in the report. If you do, the viewer can change the time range when they open it. If you do not, the report always uses the range it was saved with.
5. Save.

Splunk then offers a few next steps: **Continue Editing**, **Add to Dashboard**, **View** and **Permissions** (also reachable from the Reports list). The title becomes the identifier shown on the **Reports** page, which you reach from the app's navigation bar.

Two points matter for the exam. **The saved time range is part of the report** unless you let viewers adjust it, so a report saved with "last 24 hours" always means the last 24 hours relative to now when opened. And a report is saved **in an app**. Its visibility starts private to you.

---

## Where a report lives and who can see it

Every saved object in Splunk, reports included, has an **owner**, an **app** and **permissions**. The three standard sharing levels are:

- **Private**: only the owner sees it.
- **This app only** (app level): everyone with access to that app can see it, according to the roles you tick for read and write.
- **All apps** (global): visible across every app.

You set this under **Edit > Edit Permissions** on the report. For each role you can grant **Read** and **Write**. A user needs read access to run a report and write access to change it. Note that the report only works for someone who can also read the **indexes** it searches; permission on the report does not grant access to the data.

If a colleague says they cannot see your report, the first question is its sharing level, not the search.

---

## Editing a report

Open the **Reports** page, find the report, and use the **Edit** dropdown at the right of the row. The choices usually include:

- **Edit Description**
- **Edit Permissions**
- **Edit Schedule** (see the alerts note)
- **Edit Acceleration** (stores precomputed summaries so a report that is run often is faster)
- **Edit Search** (change the search string and time range)
- **Clone**, **Delete** and **Embed** (put the report on another web page; this requires the report to be scheduled and shared)

Changing the **search** changes what the report shows from then on. Changing the **formatting** (columns, chart type, colors) changes how it is drawn. You can edit the search from the report itself with **Open in Search**, which loads it into the search page.

A short but valuable observation: **to change how a visualization looks, open it and use the Format menu**; to change what data it shows, change the search. Beginners often reach for the wrong one.

---

## Reports that display statistics

If the search ends in a transforming command, the **Statistics** tab holds a table. Save the report while that tab is the active one and the report opens as a table. You can control page size and whether row numbers are shown in the **Format** options for the table. Drilldown, which is what happens when a viewer clicks a cell, is set here too; the default drilldown on a table row runs a new search for the clicked value.

Typical examples: a table of the top ten pages by request count, a table of error counts per host, a table of the average response time by day.

---

## Reports that display visualizations

Switch to the **Visualization** tab and choose a chart type from the **Visualization** picker. The families are:

- **Column, bar, line, area**: comparing values or showing trends. Line and area charts are the usual choice for values over time.
- **Pie**: showing proportion of a whole for a small number of categories.
- **Scatter and bubble**: relationship between numeric fields.
- **Single value**: one prominent number, optionally with a trend indicator.
- **Gauges** (radial, filler, marker): a number against a range.
- **Maps** (for example **Choropleth** and **cluster map**): geographic data.

Each visualization expects a particular table shape. A pie chart wants one category column and one value column. A line chart over time wants time first, with series after it. If the chart looks wrong, look at the table beneath it; the shape is usually the culprit. The **Format** menu adjusts titles, axes, legends, stacking and colors without touching the search.

A good rule is to chart with `timechart` when time is the horizontal axis, and with `stats` or `chart` otherwise.

**[📖 Dashboards and Visualizations: Visualization reference](https://docs.splunk.com/Documentation/Splunk/latest/Viz/Visualizationreference)** - chart types and the data shape each needs

---

## What a dashboard is

A **dashboard** is a page of **panels**, each showing a visualization, a table or a single value, usually based on a saved search or report. It exists so that several answers can be seen at once and so that people who do not write searches can still see what they need. Dashboards can also hold **inputs** (a time picker, dropdowns, text boxes) that let viewers change the data shown without editing anything.

Splunk Enterprise has two main authoring routes. **Classic dashboards** are defined in Simple XML and edited with a point-and-click editor or the source. **Dashboard Studio** is the newer builder with a freeform canvas and a JSON definition. The Core User blueprint speaks of creating a dashboard, adding a report and editing a dashboard, which is the same set of ideas on either route, and the documentation describes both. Practice on whichever your instance offers, and read the screen rather than relying on memory of a different version.

**[📖 Dashboards and Visualizations: Create dashboards](https://docs.splunk.com/Documentation/Splunk/latest/Viz/CreateDashboards)** - classic and Dashboard Studio

---

## Creating a dashboard

There are two natural starting points.

**From a search.** Run a search, choose **Save As > Dashboard Panel**, and the dialog asks whether to create a **New** dashboard or add to an **Existing** one. For a new one you give a title, an ID, a description, and a permission level; you also give the panel a title and choose whether the panel is built from the inline search or from a report.

**From the Dashboards page.** Choose **Dashboards** in the app navigation, then **Create New Dashboard**. You give it a title and permissions, choose the builder, and then add panels.

The distinction between a panel based on an **inline search** and a panel that **references a report** is subtle and good exam material. A panel with an inline search is its own copy: changes to the original search do not affect it. A panel that points at a report picks up the report's search, so editing the report updates the panel, and changing the report's permissions can change who sees the panel's data.

---

## Adding a report to a dashboard

From the Reports page, open a report's **Edit** menu or use **Add to Dashboard** after saving. Choose the dashboard and a panel title. In the dashboard editor you can also select **Add Panel** and then **New from Report**, choosing a saved report from the list.

Whatever route you use, notice that the panel's contents follow the report's visualization settings. A report saved as a pie chart appears as a pie chart. If you want the same search drawn differently on a dashboard, you either save a second report or switch the panel's visualization in the dashboard editor.

---

## Editing a dashboard

Open the dashboard, then choose **Edit**. In the classic editor you can:

- **Add panels, inputs and text**.
- **Rearrange panels** by dragging them.
- **Edit each panel's** search, visualization type and drilldown through its menu, and delete it.
- **Edit the source** (Simple XML) for fine control.
- **Edit permissions** and **Save**.

Dashboard Studio has the same logic on a canvas, where you drag visualizations, select data sources and style them.

Inputs, such as a **time range input**, create **tokens**: placeholders like `$time_tok.earliest$` that the dashboard substitutes into searches. You do not need to author tokens for the Core User exam, but you should recognize that an input changes a token and the panels that use the token rerun.

The principle underneath all dashboard editing: **a panel is a search plus a presentation**, so when something is wrong you decide whether the search, the visualization or the sharing is at fault, then fix that one thing.

---

## Things dashboards and reports have in common

| Aspect | Report | Dashboard |
|---|---|---|
| What is saved | a search and its presentation | a layout of panels, each with a search or report |
| Access control | owner, app and role permissions | the same |
| Scheduling | can be scheduled to run and be emailed | panels can use scheduled reports to load quickly |
| Typical consumer | someone who wants one answer | someone who wants an overview |

Dashboards with many heavy real-time panels are slow and expensive. The usual cure is to base panels on **scheduled reports** whose results are cached, which ties into the next note.

---

## Key terms

- **Report** - a saved search together with its presentation settings, re-run when opened.
- **Save As** - the menu on the search page for saving a search as a report, alert, dashboard panel or event type.
- **Reports page** - the page in the app navigation that lists saved reports and lets you edit them.
- **Permissions** - the owner, app and role settings that decide who can read or write a saved object.
- **Private** - a sharing level where only the owner can see the object.
- **Visualization** - a chart, gauge, single value, map or similar graphical presentation of a results table.
- **Format menu** - the control that changes how a table or chart looks without changing the search.
- **Drilldown** - the behavior when a viewer clicks part of a table or chart, usually running a more specific search.
- **Dashboard** - a page of panels that show visualizations or tables built from searches and reports.
- **Panel** - a single block on a dashboard that displays one search result.
- **Input** - a dashboard control such as a time picker or dropdown that lets viewers change the data shown.
- **Token** - a placeholder in a dashboard that an input fills with a value.
- **Dashboard Studio** - the newer Splunk dashboard builder with a canvas and a JSON definition.
- **Simple XML** - the XML format that defines classic dashboards.
- **Report acceleration** - stored precomputed summaries that make a frequently run report faster.
