---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 6 min
---

# Splunk Core Certified User High-Yield Scenarios

---

## Scenario 1: A search returns nothing for one analyst

**Scenario**: A search works for one colleague and returns no events for another, using the same words and time range.

**Solution Pattern**:
- Check the role of the second user: roles limit which indexes can be read
- Check that the search names the index; the default indexes differ by role
- Check the time range and the user's time zone setting

**Key Takeaway**: Missing results are usually access, index or time, not the data.

---

## Scenario 2: Stats shows fewer rows than expected

**Scenario**: A `stats count by host, status` search seems to be missing hosts.

**Solution Pattern**:
- Events lacking any `by` field are left out of the result
- Check that both fields exist on the events, for example with `status=*`
- Use `fillnull` or fix the extraction if values are missing

**Key Takeaway**: A `by` clause silently drops events missing the field.

---

## Scenario 3: Count of users is too high

**Scenario**: A manager asks how many different users logged in, and `stats count` returns the number of log lines.

**Solution Pattern**:
- Count distinct values with `dc(user)`
- Use `values(user)` to see the list of unique users

**Key Takeaway**: `count` counts events; `dc` counts different values.

---

## Scenario 4: A chart will not draw

**Scenario**: A user wants a pie chart of errors by host from a plain search for errors.

**Solution Pattern**:
- Add a transforming command, for example `stats count by host`
- The Visualization tab then offers the pie chart
- Save the report while that tab is showing

**Key Takeaway**: Charts need a results table, which needs a transforming command.

---

## Scenario 5: A lookup does nothing

**Scenario**: A new CSV lookup was uploaded, but a search using it adds no fields.

**Solution Pattern**:
- Confirm a lookup definition exists, not just the file
- Check sharing on both the file and the definition
- Confirm the input column name matches the event field, using `AS` if the names differ
- Remember matching is case sensitive by default

**Key Takeaway**: File, then definition, then permissions, then field names.

---

## Scenario 6: The alert emails every five minutes

**Scenario**: A failure alert is accurate but floods the team while the problem is being fixed.

**Solution Pattern**:
- Turn on throttling for a suitable period
- Optionally throttle per host or per value of a field
- Consider triggering once, not for each result

**Key Takeaway**: Throttling suppresses repeats after the first firing.

---

## Scenario 7: A dashboard panel does not follow a report change

**Scenario**: An engineer edits a saved report, but the dashboard panel still shows the old search.

**Solution Pattern**:
- Check whether the panel was created from an inline search, which is its own copy
- A panel that references the report picks up edits
- Recreate the panel from the report if it should stay linked

**Key Takeaway**: Inline-search panels are copies; report-based panels stay linked.
