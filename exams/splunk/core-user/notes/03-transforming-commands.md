---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 12 min
---

# 03 - Basic Transforming Commands

**Blueprint domain 5.0 Using Basic Transforming Commands (15%)**

Blueprint topics: the `top` command, the `rare` command, the `stats` command.

Syntax follows the Splunk Search Reference. It was not run against live data for this guide.

---

## Why transforming commands exist

Raw events are good for reading one at a time. They are poor for answering questions with numbers in them. "How many?", "which is the most common?", "what is the average?" all need Splunk to read many events and boil them down to a small table. That is the job of a **transforming command**: it takes events in and produces a table of statistical results out.

Three consequences are tested again and again.

First, **the output is a results table, not events.** After a transforming command the Events tab has nothing to show you, because the raw events are gone from the pipeline. The Statistics tab holds the table and the Visualization tab can chart it.

Second, **only fields that the command outputs survive.** If you run `stats count by host` and then try to use `status`, it is gone, because the table has only `host` and `count`.

Third, **a chart or a report with numbers is always built on a transforming command.** If you want to save a visualization as a report or place it on a dashboard, the search behind it must end in one. A search that returns raw events can be saved as a report of events, but it cannot be drawn as a pie chart.

**[📖 Search Manual: About transforming commands](https://docs.splunk.com/Documentation/Splunk/latest/Search/Abouttransformingcommands)** - what they do and which ones exist

---

## top

`top` finds the most common values of a field and reports how often each occurs, as a count and a percentage.

```
index=web | top uri
```

The output has the field you named, a `count` column and a `percent` column. Several defaults are worth owning:

- It returns the **top ten** values unless you set `limit=`. `limit=0` returns every value.
- It computes **percent** against the events that have the field.
- It can group: `top uri by host` gives the top values of `uri` separately for each host.
- It ignores events that do not have the field.
- Useful options include `showperc=f` to hide the percent column and `countfield=` or `percentfield=` to rename those columns.

The exam favors the plain-language form: "which command shows the most common values of a field with percentages". The answer is `top`.

**[📖 Search Reference: top](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Top)** - arguments and examples

---

## rare

`rare` is the mirror image of `top`. It finds the **least common** values of a field.

```
index=web | rare useragent limit=5
```

It takes the same kind of arguments as `top` and shows `count` and `percent`. The practical use is spotting the odd one out: an unusual user agent, an error code that occurs once, a host that logs very little. Remember the pair as one idea. `top` is the most, `rare` is the least, both default to ten and both give percentages.

---

## stats

`stats` is the workhorse. It calculates statistics across events, optionally grouped by one or more fields. It is the command most worth practicing until the form is automatic.

The basic form is `stats <function>(<field>) [AS <name>] [by <fields>]`.

```
index=web | stats count
index=web | stats count by status
index=web | stats avg(bytes) AS avg_bytes, max(bytes) AS max_bytes by host
```

The first line counts all events and returns a single row. The second counts events for each distinct status and returns a row per status. The third calculates two functions for each host and renames the output columns.

### Common functions

| Function | What it returns |
|---|---|
| `count` | number of events (or of events with a given field when written `count(field)`) |
| `dc(field)` | distinct count, the number of different values |
| `sum(field)` | total of numeric values |
| `avg(field)` | mean of numeric values |
| `min(field)`, `max(field)` | smallest and largest values |
| `values(field)` | list of the distinct values, deduplicated and sorted |
| `list(field)` | list of all values in order, including duplicates |
| `earliest(field)`, `latest(field)` | the value from the earliest or latest event |

The trap pairs are `count` versus `dc` and `values` versus `list`. If a question asks how many *different* users logged in, the answer is `dc(user)`, not `count`. If it asks for the set of unique hosts, `values(host)`; for every occurrence, `list(host)`.

### The by clause

`by` splits the calculation into groups, one row per combination. With one field you get a row per value. With two, you get a row per pair.

```
index=web | stats count by host, status
```

If an event is missing any field named in `by`, that event is not counted in the output. That silent drop is why totals sometimes seem small, and the habit of checking that your `by` fields exist on the events is a good one.

### Naming the results

Without `AS` the output column takes the function's name, for example `count` or `avg(bytes)`. Parentheses in field names are awkward to refer to later, so naming with `AS` is the tidy approach. If you rename with a space, put the name in quotation marks.

### stats versus other commands

`stats` produces a table. Related commands that behave similarly for different needs:

- `chart` is like `stats` but is built for charting, with an `over` field for the x-axis and an optional `by` field that splits into series.
- `timechart` is `chart` with time as the x-axis automatically. It is the command behind most "over time" line charts.
- `eventstats` and `streamstats` add statistics as new fields to the existing events instead of replacing them with a table. Both sit beyond this exam, but knowing that `stats` *replaces* the events and `eventstats` *annotates* them clears up many questions.

The Core User blueprint names only `top`, `rare` and `stats`, so the exam leans on those. Meeting `chart` and `timechart` early prepares you for the Power User exam.

**[📖 Search Reference: stats](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Stats)** - syntax and the full function list

---

## Choosing between the three

| You want | Command |
|---|---|
| the most frequent values of one field, with percentages | `top` |
| the least frequent values of one field | `rare` |
| counts, sums, averages or distinct counts, possibly grouped | `stats` |
| a count of events broken out by a field | `stats count by field` (or `top` if you also want percent) |

A frequent confusion: `top` and `stats count by field | sort -count` give similar tables. The differences are that `top` automatically adds the percent column and limits to ten rows, while the `stats` route is open-ended and lets you add more functions. When a question stresses percentages or "the most common", the intended answer is `top`; when it stresses several calculations or grouping, it is `stats`.

---

## The where command, briefly

Although `where` is not named in the blueprint, it often appears beside transforming commands, and one fact about it is a favorite trap. `where` filters results using an expression, and unlike a plain search term, **`where` comparisons on string values are case sensitive** and field names are written without quotes while string values are quoted.

```
index=web | stats count by host | where count > 100
```

This keeps only hosts with more than a hundred events. The reason to use `where` here instead of putting `count>100` in the first segment is that `count` does not exist until `stats` creates it, so it can only be filtered *after* the transforming command.

---

## Reading what the statistics look like in the interface

After a transforming command, the **Statistics** tab shows the table. You can sort columns by clicking headings, but that sorts the displayed table only; it does not change the search. The **Visualization** tab offers chart types (column, bar, line, area, pie, scatter, single value and others) through the **Visualization** and **Format** menus. The type you choose does not change the underlying search, so it can be changed freely, and a chart type is saved with the report.

A sensible habit is to read the Statistics tab first. If the table looks right, the chart will too. If you see a column named `NULL` it is the group of events that did not have the `by` field; `stats` shows it only when you ask with `usenull`. And if the numbers look too low, check for the missing-field drop mentioned above.

---

## Mistakes the exam likes

- Running `top` or `stats` and then looking for events in the Events tab.
- Using `count` when the question needs `dc`.
- Forgetting that `top` defaults to ten rows and `limit=0` removes the cap.
- Forgetting that `by` quietly drops events lacking the field.
- Referring to a field a transforming command did not output.
- Expecting `sort` to be applied automatically after `stats`: `stats` does sort by its `by` field, but not by the count.

---

## Key terms

- **Transforming command** - a command that converts events into a table of statistics.
- **Results table** - the rows and columns a transforming command produces, shown on the Statistics tab.
- **top** - a command that returns the most common values of a field with count and percent.
- **rare** - a command that returns the least common values of a field with count and percent.
- **stats** - a command that calculates statistics over events, optionally grouped with by.
- **count** - a stats function that returns the number of events.
- **dc** - a stats function that returns the number of distinct values of a field.
- **sum** - a stats function that totals numeric values.
- **avg** - a stats function that returns the mean of numeric values.
- **values** - a stats function that returns the distinct values of a field as a sorted list.
- **list** - a stats function that returns every value of a field in order, duplicates included.
- **by clause** - the part of a stats, top or rare command that groups results by one or more fields.
- **limit** - a top and rare argument that sets how many values are returned, with zero meaning all.
- **chart** - a command like stats designed to produce data for a chart with an x-axis field.
- **timechart** - a command like chart that always uses time as the x-axis.
- **eventstats** - a command that adds statistics to each event as a new field instead of replacing events.
- **where** - a command that filters results with an expression, comparing strings case sensitively.
