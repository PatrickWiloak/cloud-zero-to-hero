---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 13 min
---

# 05 - Troubleshooting Datadog

**Exam guide domain 5: Troubleshooting Datadog**

Subdomains in the guide: Agent commands, Agent logs, Agent config files.

The exam guide lists these without weights, but lists "common techniques for troubleshooting Datadog" among the topics tested, and the study list names the Agent docs and the Canonical Hostnames page. Commands are from the Datadog Agent documentation and were not run for this guide, since no Agent was installed. Treat the paths as the Linux defaults and confirm Windows and macOS locations in the docs.

---

## A method before the commands

Troubleshooting the Agent is easier when you follow the data from where it starts to where it should arrive. Ask in order:

1. **Is the Agent running?** Service status.
2. **Can the Agent reach Datadog and is it authenticated?** The status report's forwarder section.
3. **Is the check you care about loaded and running?** The status report's checks section.
4. **Is the check producing data without errors?** Run the check by hand.
5. **Is the configuration what you think it is?** Config check and files.
6. **What does the log say?** Agent logs.
7. **If it is still unclear, give Datadog Support a flare.**

Each step has a command, and the commands are the content of the first subdomain.

---

## Agent commands

The Agent installs a command-line tool, `datadog-agent`. On Linux it is normally run with `sudo` because the Agent's files and its control channel need the right permissions. Subcommands you should know:

### status

```bash
sudo datadog-agent status
```

The status report is the most useful single output. It shows:

- **Agent version**, hostname and uptime.
- **Collector section**: each check that is running, with its instances, how many metrics, events and service checks it collected, last run time, and **errors or warnings** if the check failed.
- **Forwarder section**: whether the Agent can send to Datadog, and API key validation. A failure here means the data is not leaving the host.
- **DogStatsD section**: counts of metrics and events received.
- **APM, logs and other sections** when those features are enabled.

If the check you configured is not in the list at all, the Agent did not load it, which points to configuration. If it is listed with an error, the message usually names the cause (connection refused, authentication failed, missing option).

### configcheck

```bash
sudo datadog-agent configcheck
```

This prints the **configurations the Agent has loaded and resolved**, including those produced by Autodiscovery, and lists configurations that failed to load. Use it when you are unsure whether the Agent picked up a file or a template. It answers "what does the Agent think it should be running".

### check

```bash
sudo datadog-agent check <check_name>
```

This runs one check **once, in the foreground**, and prints everything it collects. It is the best way to see what a check would send and to see its errors immediately without waiting for the next scheduled run. Adding verbose logging flags shows more detail. When a check "runs but reports no metrics", this command exposes what it actually returned.

### hostname

```bash
sudo datadog-agent hostname
```

Prints the **canonical hostname** the Agent decided on, which you compare with the Infrastructure List.

### health

```bash
sudo datadog-agent health
```

Reports whether the Agent's internal components are healthy, with a pass or fail.

### config

```bash
sudo datadog-agent config
```

Prints the **runtime configuration** after merging the file, environment variables and defaults. It is the answer to "I set it in the file, but does the Agent see it, or is an environment variable overriding it".

### flare

```bash
sudo datadog-agent flare <case_id>
```

A **flare** collects the Agent's configuration (with secrets obscured), logs, status output and diagnostics into an archive and, on confirmation, sends it to Datadog Support attached to the case. The case ID is optional. Use it when you have worked through the earlier steps and need Support's help. The Agent can also create the archive locally without sending it, so you can inspect it first.

### Service control and version

`sudo systemctl status|start|stop|restart datadog-agent` manage the service; `datadog-agent version` prints the version. Remember that editing `datadog.yaml` or an integration file normally needs a **restart** to take effect.

### diagnose

```bash
sudo datadog-agent diagnose
```

Runs connectivity and configuration diagnostics, including whether the Agent can reach Datadog's endpoints. It is useful when you suspect a firewall or proxy.

**[📖 Datadog docs: Agent commands](https://docs.datadoghq.com/agent/configuration/agent-commands/)** - every subcommand and its platform variants

---

## Agent logs

The Agent writes its own log, separate from any logs it collects for you. On Linux the main file is `/var/log/datadog/agent.log`. There are other logs in the same directory for components such as the trace Agent and the process Agent.

### Reading the log

```bash
sudo tail -n 100 /var/log/datadog/agent.log
sudo tail -f /var/log/datadog/agent.log
sudo grep -i "error" /var/log/datadog/agent.log
```

Each line has a timestamp, a **level** (for example INFO, WARN, ERROR), the component that wrote it, and a message. Start by looking for ERROR and WARN lines around the time you made a change or the time the problem began. Typical messages point to the cause directly: an invalid API key, a connection that timed out reaching Datadog, a check that failed to load because a YAML file could not be parsed, a port that was already in use.

### Log level

The verbosity is set by the `log_level` option in `datadog.yaml` (or `DD_LOG_LEVEL`). The default shows informational messages. Raising it to `debug` produces far more detail and is the standard step when the default log does not explain a problem. **Debug logs are large**, so return to the normal level afterwards. Log rotation limits file growth, with a size cap and a number of kept files that are settable.

### Where to look in other environments

On containers, the Agent logs to the container's standard output, so you read it with `docker logs <container>` or `kubectl logs <pod>`. On Windows, the log lives under the Datadog program data directory. The docs have a table of locations.

### Common log findings

| What the log shows | Likely cause |
|---|---|
| API key invalid or forbidden | wrong key, or key sent to the wrong site |
| Timeouts or connection refused toward Datadog | firewall, proxy or DNS problem on outbound 443 |
| YAML parse errors for a check | indentation or syntax mistake in a config file |
| Check "could not be loaded" | integration file missing, misnamed or in the wrong directory |
| Port in use for DogStatsD or trace Agent | another process on 8125 or 8126; change the port |
| Permission denied reading a file | the Agent's user cannot read the file or socket |

---

## Agent config files

The third subdomain is knowing what each file does and where it is, so you can change the right one.

### The main file

`datadog.yaml` holds the global settings. On Linux it is in `/etc/datadog-agent/`. Typical contents: `api_key`, `site`, `hostname`, `tags`, `proxy` settings, `log_level`, and feature switches such as `logs_enabled`, `apm_config` and `process_config`. Many installations leave nearly everything else commented out at its default.

### Integration files

Each integration has a directory `conf.d/<name>.d/` containing:

- `conf.yaml.example` - a reference file listing every option with comments. Do not edit it.
- `conf.yaml` - **your** configuration. This is the file the Agent reads. If it is missing, the check does not run.
- `auto_conf.yaml` - on some integrations, a template used by Autodiscovery.

Older Agent versions used a flat layout (`conf.d/<name>.yaml`). The directory layout is the current one, and a check will not load from a misplaced file.

### Custom checks

Custom check code sits in `checks.d/` and its configuration in `conf.d/<name>.d/conf.yaml`, with matching names.

### Precedence

The same setting can be given in several places. The rule of thumb is that **environment variables override file values, and file values override defaults**. That is why a setting you changed in `datadog.yaml` can appear to do nothing in a container that has a `DD_*` variable set. The `datadog-agent config` command shows the final result.

### Safe editing routine

1. Copy the file you will change.
2. Edit it, keeping YAML indentation.
3. Validate with `datadog-agent configcheck` or by running `datadog-agent check <name>`.
4. Restart the service.
5. Confirm with `datadog-agent status` and in the web interface.
6. If something broke, restore the copy.

**[📖 Datadog docs: Agent configuration files](https://docs.datadoghq.com/agent/configuration/agent-configuration-files/)** - locations per platform

---

## Worked scenarios

**A new host does not appear in the Infrastructure List.** Run `status`. If the forwarder reports an API key problem, fix the key or site in `datadog.yaml` and restart. If the forwarder reports connection errors, test outbound access with `curl` to the Datadog endpoint and check the proxy. If status is clean, check `hostname` and look for a duplicate name that merged this host into another.

**An integration shows no metrics.** Run `status` to see if the check is listed. If missing, check that `conf.yaml` (not just the example) exists in the right directory and that YAML parses; use `configcheck`. If listed with an error, read it and run `check <name>` for the detail. If it runs clean but returns nothing, the technology may need permission for the monitoring user.

**Custom metrics from an application never arrive.** In `status`, check the DogStatsD section for received counts. If zero, the application is not reaching the Agent: verify the address and the UDP port, and in containers verify the app is not pointing at its own `localhost`. If counts rise but the metric is missing in the web interface, check the metric name and tags in the Metrics Summary.

**Everything stopped after a config edit.** Read the end of `agent.log`, find the parse error, restore the backed-up file and restart.

---

## Key terms

- **datadog-agent status** - the command that reports the Agent's components, checks and forwarder health.
- **configcheck** - the command that shows which configurations the Agent loaded and resolved, including Autodiscovery ones.
- **check command** - the command that runs one check once in the foreground and prints what it collects.
- **health command** - the command that reports whether the Agent's internal components are healthy.
- **config command** - the command that prints the Agent's merged runtime configuration.
- **diagnose command** - the command that runs connectivity and configuration diagnostics.
- **Flare** - an archive of Agent configuration, logs and diagnostics that can be sent to Datadog Support.
- **agent.log** - the main Agent log file, in /var/log/datadog on Linux.
- **log_level** - the setting that controls how verbose the Agent log is.
- **Debug level** - the most detailed log setting, used temporarily for diagnosis.
- **conf.yaml** - the file the Agent reads for an integration's configuration.
- **conf.yaml.example** - the reference file listing every option for an integration, not read by the Agent.
- **checks.d** - the directory where custom check code is placed.
- **Precedence** - the rule that environment variables override file values, which override defaults.
- **Restart** - stopping and starting the Agent service so that configuration edits are loaded.
