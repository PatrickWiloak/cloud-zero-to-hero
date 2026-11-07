---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 12 min
---

# 05 - Creating and Using Lookups

**Blueprint domain 7.0 Creating and Using Lookups (6%)**

Blueprint topics: describe lookups, examine a lookup file example, create a lookup file and create a lookup definition, configure an automatic lookup, use the lookup in searches.

This is the smallest weighted domain except for scheduled reports and alerts, but its steps come in a fixed order and questions about the order are easy marks. The syntax is from the Splunk Knowledge Manager Manual and the Search Reference. Nothing here was run on a live instance.

---

## The problem lookups solve

Events record what happened, usually with identifiers instead of names. A web log might say `status=404` and `product_id=A1043`. A security log might say `user=jsmith` and `dest=10.4.2.17`. The people reading the results want "Not Found" instead of 404, "Blue Widget" instead of A1043, and "Finance" instead of a username.

You could store those descriptions in every event, but they would bloat the data and could never be corrected afterwards. A **lookup** is the cleaner answer: a small table kept separately, which Splunk consults at search time to **add fields to events** by matching a value that the event already has. The event holds the identifier; the lookup holds the meaning.

In the language of the blueprint, a lookup *enriches* your data. The moment of enrichment is search time, which means that when you correct a lookup file, the correction applies to old and new events alike. That is a real advantage over writing descriptions into the data.

**[📖 Knowledge Manager Manual: About lookups](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutlookupsandfieldactions)** - the concept and the lookup types

---

## Lookup types

The most common kind, and the one the Core User exam is about, is the **file-based lookup**, a CSV file. Other kinds exist and are worth recognizing by name.

| Type | What it is |
|---|---|
| File-based (CSV) | A comma-separated file uploaded to Splunk; the first row names the columns |
| KV Store | A database-like collection that can be updated by searches and apps |
| External | A script that Splunk calls to get values, for example a DNS lookup |
| Geospatial | A file mapping coordinates to regions for map visualizations |

If a question describes "a table of values in a spreadsheet that you upload", it means the file-based type. If it describes something that can be changed by a running search without re-uploading, it points to KV Store.

---

## Examining a lookup file

A lookup file is plain CSV. The first line holds the column names, which become field names. Every other line is a row.

```
status,status_description,severity
200,OK,info
404,Not Found,warning
500,Internal Server Error,critical
```

The first column here, `status`, is the **input field**: the value you match against a field in the event. The other columns, `status_description` and `severity`, are the **output fields**: the new fields you get added to the matching events. A lookup can have more than one input column, and the match requires all of them.

Details worth remembering:

- Column names must match what you intend to use as field names. They are case sensitive in the definition.
- Each row represents one combination of inputs. If two rows share the same input, only one will normally be used for the match, so keep the input column unique.
- Matching is **exact** by default and, in the default configuration, **case sensitive**. A lookup row for `Error` does not match an event field value of `error` unless case sensitivity is relaxed in the definition's advanced options.
- A matching **wildcard** can be configured in the definition, but you have to ask for it.

The exam may show a small file and ask which column is the input, or ask what field a search will gain. Read the header line first.

---

## Creating a lookup file and a lookup definition

There are two objects to create, and the difference between them is a favorite question. In **Settings > Lookups** you will see both.

The **lookup table file** is the CSV itself. You upload it through **Settings > Lookups > Lookup table files > New Lookup Table File**, choose the destination app, browse to the file and give it a **destination filename** (it must end in `.csv`). After upload, the file lives in the Splunk deployment, and its permissions control who can use it.

The **lookup definition** is a named configuration that points at a lookup file (or other source) and holds the rules for using it. You create it through **Settings > Lookups > Lookup definitions > Add new**. You choose the app, a **name**, the **type** (file-based) and the **lookup file**. The definition is what you refer to in searches and in automatic lookups. Optional settings include time-based lookups, a **minimum and maximum number of matches**, a **default value** for events that do not match, case sensitivity and wildcard matching.

Why two objects? Because the definition adds the *rules* around the data, and because other source types (KV Store and external) have no file at all but still need a name to be used. For file-based lookups, the `lookup` command can in fact use the CSV filename directly, but best practice and the exam both lean on the definition.

**Permissions are separate for each object.** Both the file and the definition must be shared with whoever needs to use the lookup. A very common cause of "my lookup does nothing" is that the file or definition is private to the owner or lives in a different app than the search.

The order to remember: **create the file, then create the definition, then (optionally) make it automatic, then search with it.**

**[📖 Knowledge Manager Manual: Define a CSV lookup](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/DefineaCSVlookup)** - file upload and definition steps

---

## Using a lookup in a search

Once the definition exists, the `lookup` command applies it.

```
index=web | lookup status_codes status OUTPUT status_description, severity
```

Reading it: use the lookup definition named `status_codes`; take the event field named `status` as input and match it against the lookup's `status` column; add `status_description` and `severity` to each event. The syntax has the shape `lookup <definition> <lookup-field> [AS <event-field>] OUTPUT <fields>`.

When the field name in the event differs from the column name in the lookup, use `AS`:

```
index=web | lookup products product_id AS pid OUTPUT product_name
```

This matches the event's `pid` against the lookup's `product_id` column. Without `AS`, Splunk assumes the event has a field with the same name as the column.

`OUTPUT` and `OUTPUTNEW` differ. `OUTPUT` **overwrites** a field of the same name already present in the event. `OUTPUTNEW` **fills only if the field is absent or empty**. If neither is given, all the lookup's non-input columns are added. A question may describe a field that is being unexpectedly replaced; `OUTPUT` is the clue.

Two related commands are good to know by name. `inputlookup` **reads the lookup file as search results** (no events needed), which is how you look at what is in a lookup or use it as a list. `outputlookup` **writes search results into a lookup file**, which is how you build or update a lookup from data.

```
| inputlookup status_codes
```

Note the leading pipe: `inputlookup` is a generating command, so it starts the search rather than following one.

**[📖 Search Reference: lookup](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Lookup)** - syntax, OUTPUT and OUTPUTNEW

---

## Automatic lookups

Typing `| lookup ...` in every search is tedious, and people forget. An **automatic lookup** applies the lookup to every matching event for you, so the new fields appear as if they were always part of the data.

You configure one under **Settings > Lookups > Automatic lookups > Add new**. The settings are:

- The **destination app** and a **name**.
- The **lookup table** (the definition to use).
- The **apply to** choice: it applies to a **sourcetype**, a **source** or a **host**, and you name which. This ties the lookup to a kind of data.
- The **lookup input fields**, mapping event fields to lookup columns.
- The **lookup output fields**, naming which columns become event fields and optionally what to call them.
- **Overwrite field values**, a checkbox deciding whether existing event fields can be replaced.

After saving, set permissions so searchers can use it. Then in a plain search over the chosen sourcetype, the output fields exist and can be used in a comparison, a `stats ... by`, or a table, with no `lookup` command at all.

The things to watch: the automatic lookup runs at search time, only for the data it was scoped to, and only for users who can read it. If the new fields do not appear, check the **apply to** scope first, then permissions, then whether the input field exists in the events, then the search mode (fast mode can skip them).

---

## Worked example

A team wants the web dashboard to show service names instead of port numbers. They have a spreadsheet with columns `port`, `service`. They save it as CSV, upload it as a lookup table file, create a lookup definition named `port_services`, and give both global read permission. In a search, `lookup port_services port OUTPUT service` adds a `service` field and then `stats count by service` gives a readable report. To avoid retyping, they configure an automatic lookup for the `firewall` sourcetype using the `dest_port` field as input. From then on, every firewall search has `service` available.

---

## Key terms

- **Lookup** - a table of values that Splunk consults at search time to add fields to events.
- **File-based lookup** - a lookup stored as a CSV file uploaded to Splunk.
- **KV Store lookup** - a lookup stored in a database-like collection that searches and apps can update.
- **External lookup** - a lookup whose values come from a script Splunk runs.
- **Input field** - the lookup column matched against a field in the event.
- **Output field** - a lookup column whose value is added to matching events.
- **Lookup table file** - the uploaded CSV that holds the lookup data.
- **Lookup definition** - a named configuration that points at a lookup source and sets rules for using it.
- **lookup command** - the search command that applies a lookup definition to events.
- **OUTPUT** - the lookup argument that adds output fields and overwrites existing fields of the same name.
- **OUTPUTNEW** - the lookup argument that adds output fields only where the field is absent.
- **inputlookup** - a generating command that returns the rows of a lookup as search results.
- **outputlookup** - a command that writes search results into a lookup file.
- **Automatic lookup** - a lookup configured to apply to every event of a sourcetype, source or host without a lookup command.
- **Enrichment** - adding meaning to events from outside the event, such as names for identifiers.
