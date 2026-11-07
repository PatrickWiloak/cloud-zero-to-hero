---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 6 min
---

# Datadog Fundamentals High-Yield Scenarios

---

## Scenario 1: A new host never appears

**Scenario**: The Agent is installed and the service is active, but the host is not in the Infrastructure List.

**Solution Pattern**:
- Run `datadog-agent status` and read the forwarder section for key errors
- Check the site setting matches the site your organization uses
- Test outbound HTTPS to Datadog and check any proxy settings
- Confirm the canonical hostname with `datadog-agent hostname`

**Key Takeaway**: A valid key sent to the wrong site looks exactly like no data.

---

## Scenario 2: An automation script cannot create monitors

**Scenario**: A script using only an API key can submit metrics but fails to create a monitor.

**Solution Pattern**:
- Reading and managing objects needs the application key as well as the API key
- Send both in the `DD-API-KEY` and `DD-APPLICATION-KEY` headers
- Check the owner of the application key has permission

**Key Takeaway**: API key lets data in; both keys let you act on the account.

---

## Scenario 3: Custom metrics never show up

**Scenario**: An application in a container sends metrics with a DogStatsD client, but nothing arrives.

**Solution Pattern**:
- Check the DogStatsD counters in `datadog-agent status`
- Remember it listens on UDP 8125; `localhost` in a container is the container itself
- Point the client at the node's Agent address or socket
- Look for the metric in the Metrics Summary by exact name

**Key Takeaway**: Missing custom metrics are usually an address problem, not a Datadog problem.

---

## Scenario 4: An integration check is not running

**Scenario**: A database integration was configured but its metrics are absent.

**Solution Pattern**:
- Confirm `conf.yaml` (not only the example) exists in the integration's `conf.d` folder
- Run `configcheck`, then `datadog-agent check <name>` to see the error
- Fix YAML indentation or credentials, then restart the Agent

**Key Takeaway**: Status shows if it is loaded; check shows why it fails.

---

## Scenario 5: Average latency looks fine but users complain

**Scenario**: A dashboard averages per-host p95 latency across the fleet.

**Solution Pattern**:
- Percentiles do not average meaningfully across hosts
- Submit latency as a distribution so percentiles are computed globally
- Graph the global percentile instead

**Key Takeaway**: Histogram percentiles are per Agent; distribution percentiles are global.

---

## Scenario 6: A tag blew up the bill

**Scenario**: A developer added a `user_id` tag to a custom metric and the number of timeseries exploded.

**Solution Pattern**:
- Each distinct tag value creates a new timeseries
- Remove the unbounded tag and use bounded keys such as env, service and team
- Put identifiers in logs or traces

**Key Takeaway**: Keep tag cardinality bounded.

---

## Scenario 7: Nobody was told the Agent died

**Scenario**: A host stopped sending data and its CPU monitor stayed quiet.

**Solution Pattern**:
- A metric monitor needs a no-data setting to notify when data stops
- Add a host-reporting monitor for Agent health
- Group by host so the alert names the host

**Key Takeaway**: Silence is a state you must monitor for explicitly.
