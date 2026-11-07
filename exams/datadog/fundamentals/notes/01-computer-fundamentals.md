---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 15 min
---

# 01 - Computer Fundamentals

**Exam guide domain 1: Computer Fundamentals**

Subdomains in the guide: config file modification, operating systems, programming languages, hardware concepts, shell, metadata, networking.

The exam guide publishes no weights, so this domain should be read as a floor: the guide opens its description by saying the exam runs from "Linux command line basics to metric visualization strategies", and lists computer fundamentals, Linux, reading YAML, JSON, Python and shell scripts, and networking basics as the knowledge a candidate should already have. The commands below are standard Linux and were not run for this guide.

---

## Why a monitoring exam starts with a computer

Datadog is a service you talk to over the network, but its center of gravity is a small program, the **Agent**, that you install on machines you want to watch. To install it, configure it, and work out why it is not reporting, you need to be comfortable on the machine itself. That is the reason the very first domain is not about Datadog at all. It tests whether you can read a config file, understand what a process is, and use a shell, because every later domain assumes you can.

The guide's own out-of-scope list helps set the depth: programming, systems architecture and testing are not required. You must be able to **read** YAML, JSON, Python and shell scripts, not write large programs. Think of the depth as "reads a config and a short script without panic".

**[📖 Datadog Fundamentals exam guide](https://www.datadoghq.com/pdf/Datadog_Fundamentals_Exam_Guide.pdf)** - the outline this note follows

---

## Config file modification

Most infrastructure software is configured with text files, and the Agent is no exception. A recurring task is: open a file, change a value without breaking the file's structure, save it, and make the program notice.

Three habits cover most of the risk.

First, **make a backup before you edit**. A copy such as `datadog.yaml.bak` costs nothing and turns a bad edit into a thirty-second repair.

Second, **respect the file format**. The Agent's files are YAML, and YAML is sensitive to indentation and to the difference between a list and a mapping. A single wrong space can change the meaning or make the file unreadable.

Third, **reload or restart after editing**. Changes to the main Agent configuration file are generally read when the Agent starts, so you restart the service for them to take effect. Whether a particular integration file needs a restart or just a check run depends on the integration; the Agent docs say, and in the troubleshooting note you will see commands that let you confirm what the Agent actually loaded.

On Linux you edit files with a terminal editor such as `nano` or `vi`, usually with administrator rights, because the Agent's files are owned by a service account and live under `/etc`. Using `sudo` to edit them is normal, and the file permissions are worth leaving as they were; if the Agent runs as a dedicated user it must still be able to read what you edited.

---

## Operating systems

The Agent runs on Linux, Windows and macOS, and in containers. You are expected to know a few differences.

| Idea | Linux | Windows |
|---|---|---|
| Service manager | `systemd` (`systemctl`) or another init system | the Services console, or PowerShell |
| Config location for the Agent | under `/etc/datadog-agent/` | under `C:\ProgramData\Datadog\` |
| Log location for the Agent | under `/var/log/datadog/` | under `C:\ProgramData\Datadog\logs\` |
| Shell | bash and friends | PowerShell, Command Prompt |
| Path separator | forward slash | backslash |

The Datadog docs list the exact paths for every platform on their "Agent configuration files" page, and the table above gives the shape only. The exam style is "where would you find X on this operating system", so know that Linux keeps system-wide configuration under `/etc`, logs under `/var/log`, and that Windows keeps program data under `ProgramData`.

Two operating system concepts come up beside them. A **process** is a running program, and a **service** (or daemon) is a process managed by the system to start at boot and restart on failure. The Agent is a service. When someone says "the Agent is not running", they mean the service is stopped, failed, or never started. Knowing the difference between **installed**, **enabled at boot** and **currently running** is part of the vocabulary.

A **package manager** (`apt`, `yum`, `dnf`) installs software and its dependencies on Linux, and Datadog publishes repositories for the main ones. Containers are another delivery mode: instead of installing onto the host, you run the Agent as a container with access to the host's resources.

---

## Programming languages

You are not asked to program, but three formats and two languages appear in Datadog work, and you need to recognize each at a glance.

### YAML

YAML is how the Agent and its integrations are configured. It uses indentation to show structure, dashes for list items and `key: value` pairs for settings.

```yaml
api_key: <YOUR_API_KEY>
site: datadoghq.com
hostname: web-01
tags:
  - env:prod
  - team:payments
```

Things to notice: there are no braces; `tags` is a **list** (each item starts with a dash); `api_key` and `site` are **scalars**; lines starting with `#` are comments. Spaces matter and tabs are not allowed for indentation. A colon followed by a space separates key from value. Strings usually need no quotes, though values with special characters may.

### JSON

JSON is how the Datadog **API** exchanges data, and how many dashboards and monitors can be exported. It uses braces for objects, brackets for lists, and double-quoted keys.

```json
{
  "series": [
    { "metric": "custom.queue.depth", "points": [{ "timestamp": 1700000000, "value": 12 }] }
  ]
}
```

JSON is stricter than YAML: no comments, no trailing commas, and keys must be in double quotes. A frequent trap is that YAML can express almost everything JSON can, so a JSON example is valid YAML in most cases, but not the other way around.

### Python and shell

The Agent itself is largely written in Go with Python used for **checks**: the integration code that gathers data from a technology. You are not asked to write one, but you may be shown a short Python snippet that **sends a metric** through a Datadog library, for instance a call to a DogStatsD client, and asked what it does. Read it for the metric name, the value and the tags.

Shell scripts appear as installation one-liners and wrapper scripts. Read them for environment variables, the command they run, and what they pipe into what.

---

## Hardware concepts

The guide names hardware in the form "CPUs, RAM, data storage". These matter because most infrastructure metrics are measurements of them.

- **CPU** does the computing. Metrics describe the share of time spent on user work, system work, waiting on disk (**iowait**), or idle. A **load average** is a count of processes wanting CPU time, not a percentage.
- **RAM** is fast working memory. Metrics describe used and free memory and, on Linux, memory that is **cached** and can be reclaimed. A machine whose "free" memory is low is not necessarily in trouble if most of that is cache.
- **Swap** is disk space used as overflow for RAM. Heavy swap use is usually a warning sign.
- **Storage** is persistent disk. Metrics describe space used and free and the rate of reads and writes. A full disk is the classic cause of strange application failures.
- **Network interfaces** carry traffic. Metrics describe bytes and packets sent and received and errors.

Datadog's host-level checks (CPU, memory, disk, network, load) are included with the Agent without further setup, and those are the metrics you will most often see when you first connect a machine.

An important idea to carry forward: a **percentage** and a **count** behave differently when you aggregate them across many hosts. Averaging a CPU percentage across a fleet is meaningful. Summing it is not. Summing request counts is meaningful. Averaging them across hosts answers a different question (the average per host). This returns when you work with metrics later.

---

## The shell

The **shell** is the text interface to the operating system. The skills the exam draws on are small and practical.

| Task | Typical command |
|---|---|
| Show the current directory | `pwd` |
| List files with details | `ls -l` |
| Read a file | `cat file`, `less file` |
| Follow a growing log | `tail -f file` |
| Search for text | `grep "error" file` |
| Edit a file | `nano file`, `vi file` |
| Run as administrator | `sudo command` |
| Check a service | `systemctl status name` |
| Restart a service | `sudo systemctl restart name` |
| See running processes | `ps aux`, `top` |
| Test a web endpoint | `curl https://example.com` |
| Set a variable for one command | `NAME=value command` |
| Pipe output to another command | `command1 \| command2` |

Two ideas deserve emphasis. **Environment variables** are named values the shell passes to programs. The Agent reads many of its settings from variables whose names start with `DD_`, such as `DD_API_KEY` and `DD_SITE`, and an installation one-liner often sets them on the same line as the install command. And **exit codes**: a command returns `0` when it succeeded and a non-zero number when it did not, which is how scripts and checks know whether something worked.

Reading a shell one-liner is mostly a matter of tokenizing it: variables set first, then the command, then arguments, then pipes. Practice by taking the Datadog install command from the docs and saying aloud what each part does.

**[📖 Datadog docs: Agent installation](https://docs.datadoghq.com/agent/)** - install commands per platform

---

## Metadata

**Metadata** is data about data. For a monitored machine it is the description that is not itself a measurement: the hostname, the operating system and version, the cloud provider and region, the instance type, the tags you attached, the Agent version. In Datadog this information shows up on the **Infrastructure List** and the host's detail panel, and it is what lets you slice and filter measurements.

The exam sub-heading sits in the computer fundamentals domain because metadata starts life on the machine: the operating system reports its name, cloud providers expose instance details through a **metadata service** the Agent can query, and containers carry **labels**. A tag, which you will meet properly in the data collection note, is metadata you attach yourself. A good way to remember it: metrics tell you *how much*; metadata tells you *of what, where and whose*.

---

## Networking

Networking questions at this level are about vocabulary and a few protocols.

- An **IP address** identifies a network interface. IPv4 addresses are four numbers separated by dots. Some ranges are **private** and not reachable from the internet (the well-known private blocks start with 10, 172.16 to 172.31, and 192.168), and `127.0.0.1` is **localhost**, the machine itself.
- A **port** identifies a service on a machine. An address plus a port names a specific listener.
- **DNS** turns names into addresses.
- A **protocol** is an agreed way of talking. **TCP** is connection-oriented and reliable: it sets up a connection, numbers the data and resends what is lost. **UDP** is connectionless and "fire and forget": it is lighter and faster but offers no delivery guarantee. **HTTP** runs on top of TCP and carries requests and responses for the web. **HTTPS** is HTTP over an encrypted connection.
- A **firewall** allows or blocks traffic by address, port and direction. The Agent mostly makes **outbound** connections to Datadog, so firewalls on the host's network usually need to allow outbound traffic to Datadog's endpoints rather than opening inbound ports.
- A **proxy** is an intermediary that outbound traffic passes through. The Agent can be configured to use one.

The reason UDP matters here is that **DogStatsD**, the local metrics listener in the Agent, uses it by default. Sending a metric over UDP to a local port is cheap and cannot block your application, at the price of no confirmation that it arrived. That trade-off is the reason it was designed that way, and the data collection note returns to it.

Useful diagnostics are the same everywhere: `ping` to see if a host answers, `curl` to test an HTTP endpoint, `nc` (netcat) to test whether a port accepts a connection, and `ss` or `netstat` to see which ports a machine is listening on.

---

## Key terms

- **Agent** - the Datadog program installed on a host or run as a container that collects and sends monitoring data.
- **YAML** - an indentation-based text format used for the Agent and integration configuration files.
- **JSON** - a brace-and-bracket data format used by the Datadog API and for exporting objects.
- **Environment variable** - a named value passed to a program by the shell, such as DD_API_KEY.
- **Service** - a process managed by the operating system to start at boot and restart if it fails.
- **Package manager** - a tool such as apt or yum that installs software and its dependencies.
- **CPU** - the component that performs computation, measured by how its time is split between work, waiting and idling.
- **RAM** - fast working memory whose use is reported as used, free and cached.
- **Swap** - disk space used as overflow for RAM.
- **iowait** - the share of CPU time spent waiting for disk or network input and output.
- **Load average** - a count of processes wanting CPU time, not a percentage.
- **Shell** - the text interface to the operating system.
- **sudo** - a command prefix that runs a command with administrator rights.
- **Exit code** - the number a command returns, with zero meaning success.
- **Metadata** - descriptive information about a host or metric, such as hostname, operating system and region.
- **IP address** - a number that identifies a network interface.
- **Port** - a number that identifies a particular service on a machine.
- **TCP** - a reliable, connection-oriented protocol that resends lost data.
- **UDP** - a lightweight connectionless protocol with no delivery guarantee.
- **HTTP** - the web request and response protocol carried over TCP.
- **Firewall** - a control that allows or blocks network traffic by address, port and direction.
- **Proxy** - an intermediary through which outbound traffic can be routed.
