---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 14 min
---

# 02 - Using Fields and Search Language Fundamentals

**Blueprint domains 3.0 Using Fields in Searches (20%) and 4.0 Search Language Fundamentals (15%)**

Blueprint topics: understand fields, use fields in searches, use the fields sidebar; review basic search commands and general search practices, examine the search pipeline, specify indexes in searches, use the `table`, `rename`, `fields`, `dedup` and `sort` commands.

The syntax here is quoted from the Splunk Search Reference and Search Manual. It was not run against live data for this guide, so check sample output on your own instance.

---

## What a field is

An event is raw text. A **field** is a name paired with a value pulled out of that text, so that you can search and calculate on parts of an event instead of the whole thing. In a web access log line the client address, the HTTP status, the requested path and the number of bytes sent are all fields. Once they are fields, you can say "show me only status 500" or "add up the bytes by path", which is impossible if all you have is a blob of characters.

Fields come from three places. **Default fields** are added at index time to every event: `host`, `source`, `sourcetype`, `index`, `_time` and `_raw`. **Extracted fields** are discovered at search time from the event text, either automatically (for well-structured data such as key=value pairs or JSON) or because someone defined an extraction. **Calculated or lookup fields** are created by commands or configuration, covered in later notes.

The phrase **search-time extraction** is worth keeping in your head. For most fields, Splunk does not pull the value out when it stores the event. It does the extraction at the moment you search. That is why you can define a new field today and use it on data indexed last year.

**[📖 Knowledge Manager Manual: About fields](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutfields)** - default, extracted and calculated fields

---

## The fields sidebar

On the results page, the **fields sidebar** sits at the left of the event list. It groups fields in two blocks. **Selected fields** are the ones shown with each event; by default these are `host`, `source` and `sourcetype`. **Interesting fields** are fields that appear in at least a fifth of the events in the current results; Splunk surfaces these automatically because they are probably useful. The count beside each field name is the number of distinct values.

Clicking a field name opens a small summary showing the **top values** and how often each appears, the percentage of events that have the field, and the option to run a quick report such as top values, top values by time, or rare values. Clicking a value inside this summary adds it to the search, which is the quickest refinement there is. You can promote an interesting field to a selected field using **All Fields**, a link at the bottom of the sidebar that opens the full list and lets you tick the fields you want shown with each event.

Two details are commonly tested. First, the sidebar is built from the **events in the current results** (and in fast mode it discovers fewer fields, as noted earlier), so a field can be missing from the sidebar simply because of the search mode. Second, the sidebar's counts of distinct values are for the events Splunk looked at, not necessarily the whole dataset.

**[📖 Search Tutorial: Use the fields sidebar](https://docs.splunk.com/Documentation/Splunk/latest/SearchTutorial/Usefieldstosearch)** - selected versus interesting fields

---

## Searching with fields

A field comparison has the shape `fieldname=value`. The rules come in a few small pieces, and the exam checks each of them.

**Field names are case sensitive.** `status=500` and `Status=500` are different fields. **Field values compared with `=` are not case sensitive** in a plain search, so `host=WEB01` matches `web01`. This asymmetry is the most frequently tested fact in the whole domain. (A later `where` command comparing values *is* case sensitive, which is a famous trap discussed in the transforming note.)

You can use comparison operators for numeric and string comparisons: `=`, `!=`, `<`, `>`, `<=`, `>=`. `status!=200` finds events whose status is not 200 *and* where the field exists. That detail matters: it does not return events where the field is missing at all. The alternative `NOT status=200` returns events where status is not 200 and also those where status does not exist. The two are close but not identical, and a question that asks for "events with a status that is not 200" is testing it.

Wildcards work in values: `host=web*`. A leading wildcard such as `host=*web` is legal but slow, because Splunk cannot use its index to jump to a starting point and must scan. You can also test whether a field exists with a wildcard value, `status=*`, which returns events that have any value for status.

Multiple fields combine with the same implied `AND`:

```
index=web status=404 host=web01
```

and `IN` is a tidy way to write an `OR` list for one field:

```
index=web status IN (404, 500, 503)
```

Values with spaces or special characters go in quotation marks: `user="Mary Jones"`. The field name itself never goes in quotes.

**[📖 Search Manual: Use fields to retrieve events](https://docs.splunk.com/Documentation/Splunk/latest/Search/Usefieldstoretrieveevents)** - comparisons and operators

---

## Why `index=` comes first

The `index` field tells Splunk **which repository to read**. If you do not specify one, Splunk searches the default indexes your role allows, which may or may not include the data you wanted and often includes more than you need. Naming the index is both a correctness and a performance habit.

```
index=web sourcetype=access_combined status=404
```

Here the first three terms are all indexed or low-cost filters, so Splunk narrows to a small set of events before doing any other work. Good practice is to put `index`, `sourcetype` and `host`/`source` restrictions at the start of the search along with a tight time range. Splunk's own docs describe the golden rule as filtering as early as you can.

You can search several indexes by repeating or using a wildcard: `index=web OR index=app` or `index=prod_*`. Whether you can see an index at all depends on your role. Internal indexes, whose names begin with an underscore, such as `_internal`, hold Splunk's own logs and are not shown by default in a wildcard unless you name them.

---

## The search pipeline

A Splunk search is a **pipeline**. The first segment, before any pipe character, is the **search** that retrieves events from the index. Each additional segment starts with the **pipe** `|`, followed by a command that takes whatever came out of the previous segment, does something to it, and passes the result on.

```
index=web status=404 | stats count by uri | sort -count | head 10
```

Reading it from left to right: retrieve 404 events from the web index; count them by the `uri` field; sort the counts largest first; keep the top ten rows. The pipe works like a Unix shell pipe, and if you have written shell scripts the idea lands at once.

Two practical points follow from the pipeline model. **Order matters**, because a command only sees what its predecessor emitted. Removing fields with `fields` before running `stats` on one of them would produce nothing. And **commands come in kinds**, which the exam tests by name. **Generating** commands start a search and produce events (the initial search is the commonest). **Streaming** commands operate on each event as it passes, such as `eval`, `rename` and `fields`. **Transforming** commands take the stream of events and turn it into a table of statistics, such as `stats`, `top` and `rare`. After a transforming command you no longer have the raw events; you have a results table. That is the reason the Statistics and Visualization tabs only light up after one.

A pragmatic habit: build a search one pipe at a time. Run the search, look at the results, then add a command and look again. If something looks wrong you know exactly which segment did it.

**[📖 Search Manual: About the search pipeline](https://docs.splunk.com/Documentation/Splunk/latest/Search/Aboutthesearchlanguage)** - commands, arguments, pipes

---

## The five commands the blueprint names

### table

`table` displays the fields you name, in the order you name them, as columns.

```
index=web | table _time, host, status, uri
```

It discards other fields from the *display*. Use it to tidy results for reading or exporting. Commas between field names are optional, and wildcards work (`table *`). Be careful about one thing: `table` is a transforming-style display command that ends the event view, so later commands that need other fields will not have them.

### rename

`rename` gives a field a new name for display, using `AS`.

```
index=web | rename status AS "HTTP Status", uri AS Page
```

New names containing spaces need quotation marks. A renamed field is renamed for the rest of the search, so later commands must use the new name. Renaming is mostly cosmetic for the final report.

### fields

`fields` includes or excludes fields from the results. With no sign or with `+`, it keeps just the listed fields (plus the internal ones). With `-`, it removes the listed ones.

```
index=web | fields + host, status
index=web | fields - _raw
```

The difference from `table` is the output: `fields` leaves you with events (just with fewer fields), while `table` makes a table. Removing fields you do not need early in a search is a performance help because there is less to carry along. A frequent exam question asks which command removes a field from results; the answer is `fields -`.

### dedup

`dedup` removes events that repeat a value of the field(s) you name, keeping the **first** one it sees, which in a default search is the most recent.

```
index=web | dedup host
```

That leaves one event for each distinct host. You can give several fields, and the combination must be unique. `dedup 3 host` keeps the first three events for each host. Events that do not have the field are dropped, which is a gotcha: `dedup` removes events missing the field unless you ask otherwise with `keepempty=true`.

### sort

`sort` orders results by one or more fields. A minus sign before the field means descending, and a plus sign or none means ascending.

```
index=web | stats count by uri | sort -count
index=web | sort - _time, + host
```

Two traps. By default `sort` returns a limited number of results (ten thousand), and you can pass a number to change that, with `sort 0 field` meaning no limit. And `sort` treats numbers and strings differently: a field recognized as numeric sorts numerically, but a string such as "10" and "9" would sort as text, putting "10" first. The `num()` and `str()` helpers can force the interpretation.

**[📖 Search Reference: table, rename, fields, dedup, sort](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Table)** - the command reference starts at `table`; the others sit in the same left-hand list

---

## General search practices

The blueprint also asks you to "review basic search commands and general search practices". The substance is a short list you can hold in your head.

- **Be specific early**: index, sourcetype and a narrow time range first.
- **Put the filtering before the processing**, so later commands handle fewer events.
- **Drop fields you do not need** with `fields -` before heavy commands.
- **Use fields rather than free text** where a field exists; `status=404` is clearer and faster than the word `404`, which could match a byte count.
- **Avoid leading wildcards** and avoid `*` alone.
- **Use `NOT` and `!=` knowingly**, remembering the missing-field difference.
- **Read the job inspector** when a search is slow, to see which stage consumed the time.

A search that follows these habits usually also happens to be easy for the next person to read. The sibling idea is that the **search bar is not a command prompt for the whole machine**: it is a pipeline over events, and everything you do happens to events or to the results table built from them.

---

## Putting it together

A small worked example, described in words so you can rehearse the reasoning rather than memorize text. A support lead asks which ten pages returned the most "not found" errors yesterday, with friendly column names, and wants each page listed once.

The search names the index and the `status=404` condition and narrows the time with `earliest=-1d@d latest=@d`. It then uses `stats count by uri` to count (the next note covers `stats` in depth), sorts descending by the count, keeps ten rows with `head`, and renames `uri` to Page and `count` to Hits. No `dedup` is needed because `stats ... by` already yields one row per page. Spotting that `dedup` would be redundant is the kind of judgment the exam likes.

---

## Key terms

- **Field** - a name and value extracted from an event so it can be searched and calculated on.
- **Default fields** - fields Splunk adds to every event at index time, such as host, source, sourcetype, index, _time and _raw.
- **Selected fields** - fields displayed with each event in the results, host, source and sourcetype by default.
- **Interesting fields** - fields that appear in a substantial share of the events in the current results.
- **Search-time extraction** - pulling field values from event text when the search runs rather than when data is indexed.
- **Field comparison** - a search term of the form fieldname=value, where names are case sensitive and values are not.
- **IN operator** - a shorthand that matches a field against a list of values.
- **Pipe** - the vertical bar that passes the output of one search command to the next.
- **Streaming command** - a command that works on each event as it passes through, such as eval, rename or fields.
- **Transforming command** - a command that turns events into a table of statistics, such as stats, top or rare.
- **table** - a command that shows the named fields as columns in the order given.
- **rename** - a command that gives a field a new name using AS.
- **fields** - a command that keeps (plus) or removes (minus) fields from the results.
- **dedup** - a command that removes events repeating the value of the named field, keeping the first.
- **sort** - a command that orders results, with a minus sign meaning descending.
- **head** - a command that keeps the first N results.
