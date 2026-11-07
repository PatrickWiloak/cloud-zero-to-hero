---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 30 min
---

# Domain 4: Automation, Orchestration, and Scripting (17%)

## Overview

XK0-006 gives automation far more weight than the exam it replaced in spirit: you are expected to read and reason about infrastructure as code, unattended installs, CI/CD concepts, shell scripts, basic Python, Git and, new in this version, responsible use of AI. You will mostly read short snippets and decide what they do or what is wrong with them.

- **4.1** Automation and orchestration use cases and techniques.
- **4.2** Shell scripting.
- **4.3** Python basics for system administration.
- **4.4** Version control with Git.
- **4.5** Best practices and responsible use of AI.

**[📖 CompTIA Linux+ XK0-006 Exam Objectives (PDF, version 5.0)](https://lecbyo.files.cmp.optimizely.com/download/90b9ac985c0e11f0b004a2a93c999a21)** - The official list of every topic and tool named in this domain

## 4.1 Automation and orchestration

**Infrastructure as code (IaC)** describes servers and their configuration in files you can review, version and repeat. The goal is that two servers built from the same code are identical, and that a change is a reviewed commit rather than a hand edit.

### Configuration management

| Tool | Model | Key vocabulary |
|---|---|---|
| **Ansible** | Agentless: connects over SSH and runs modules | Inventory (hosts), playbook (YAML tasks), module (unit of work), collection (packaged content), facts (gathered host data), ad hoc command |
| **Puppet** | Usually agent-based: an agent pulls a catalog from a server; agentless modes exist | Manifests, classes, modules, facts, certificates for agent trust |
| **OpenTofu** (and Terraform) | Declarative provisioning of infrastructure through provider APIs | Provider, resource, state, plan before apply |

An Ansible playbook that ensures a package is present and a service runs:

```yaml
- name: Web servers
  hosts: web
  become: true
  tasks:
    - name: Install nginx
      ansible.builtin.package:
        name: nginx
        state: present
    - name: Start and enable nginx
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true
```

Run it with `ansible-playbook -i inventory.ini site.yml`; an ad hoc command is `ansible web -i inventory.ini -m ansible.builtin.ping`. The important property is **idempotence**: running the playbook twice leaves the system in the same state and changes nothing the second time. Shell commands that append lines are not idempotent; modules that declare a desired state are.

### Unattended deployment

- **Kickstart** is the answer file for automated Red Hat-family installs; the installer reads it and asks no questions. Combined with PXE it builds servers with nobody at the console.
- **cloud-init** configures a cloud instance at first boot from user data (users, keys, packages, commands). It is how an image becomes a specific server.

**[📖 cloud-init introduction](https://cloudinit.readthedocs.io/en/latest/explanation/introduction.html)** - What cloud-init does at first boot and which stages it runs

### CI/CD and DevSecOps

**Continuous integration** builds and tests each change automatically; **continuous delivery/deployment** pushes passing builds toward production. A **pipeline** is the ordered set of stages (build, test, scan, deploy). **Version control** is the source of truth, and **GitOps** extends that: the desired state of the environment lives in Git and an automated process makes reality match it. **Shift-left testing** moves testing and security checks earlier in the pipeline, where defects are cheapest to fix. **DevSecOps** builds security checks into every stage rather than adding them at the end. Secrets belong in a secrets manager or vault, never in the repository.

### Container orchestration

Compose files describe multi-container applications for a single host: `docker compose up -d` starts them, `docker compose logs` reads output and `docker compose down` stops and removes them (`podman compose` works the same way). **Docker Swarm** clusters hosts, with **services**, **tasks**, **nodes** and **scale**. **Kubernetes** is the dominant orchestrator; the terms to know are the **pod** (one or more containers sharing network and storage, the smallest deployable unit), **Deployment** (keeps a desired number of pod replicas running and handles rolling updates), **Service** (a stable address in front of pods), **ConfigMap** (non-secret configuration), **Secret** (sensitive configuration) and **volume** (storage attached to a pod).

**[📖 Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/)** - What a pod is and how it is used

## 4.2 Shell scripting

A script starts with an **interpreter directive** (shebang) naming the shell, is made executable with `chmod +x`, and returns an **exit code** (0 for success, nonzero for failure) readable as `$?`.

```bash
#!/usr/bin/env bash
set -euo pipefail            # stop on error, unset variable, or failed pipe stage

LOG_DIR="${1:-/var/log}"     # first argument, default /var/log
THRESHOLD=80

if [[ ! -d "$LOG_DIR" ]]; then
    echo "not a directory: $LOG_DIR" >&2
    exit 2
fi

usage=$(df --output=pcent "$LOG_DIR" | tail -1 | tr -dc '0-9')   # command substitution

if (( usage >= THRESHOLD )); then
    echo "WARNING: $LOG_DIR is ${usage}% full"
    exit 1
fi
echo "OK: ${usage}%"
```

### Variables and expansion

Assign with no spaces (`name=value`), read with `$name` or `${name}`. **Parameter expansion** has forms such as `${var:-default}` (use default if unset). **Command substitution** captures output: `$(date +%F)` (backticks do the same but nest poorly). Positional parameters are `$1`, `$2`, `$@` (all arguments) and `$#` (count). `export` makes a variable visible to child processes; `local` limits it to a function; `unset` removes it; `set` shows or sets shell options and variables. A parenthesized group `(cd /tmp && ls)` runs in a **subshell**, so directory and variable changes inside it do not leak out. `IFS` is the field separator used when splitting words.

### Tests and comparisons

Use `[[ ... ]]` in bash. File tests: `-f` (regular file), `-d` (directory), `-e` (exists), `-n` (string not empty), `-z` (string empty), and `!` negates. String comparison uses `=`, `==`, `!=`; numeric comparison uses `-eq`, `-ne`, `-lt`, `-le`, `-gt`, `-ge`. A common mistake is using `>` for numbers inside `[[ ]]`, which compares strings. Regular expression matching is `[[ $name =~ ^web[0-9]+$ ]]`.

### Control flow

```bash
for host in web1 web2 web3; do
    ssh "$host" uptime
done

while read -r line; do
    echo "line: $line"
done < servers.txt

case "$1" in
    start)  systemctl start myapp ;;
    stop)   systemctl stop myapp ;;
    *)      echo "usage: $0 start|stop" >&2; exit 64 ;;
esac
```

`until` loops until a condition becomes true, the opposite of `while`. Functions group reusable logic: `check() { ... }`, and `return` sets a function's status. Always quote variable expansions (`"$var"`) so spaces in values do not split into extra words.

## 4.3 Python for system administration

Python is the common scripting step above shell once logic or data structures get complicated. The objectives ask for the basics.

- **Virtual environments** isolate a project's dependencies from the system Python: `python3 -m venv .venv`, then `source .venv/bin/activate`, then `pip install requests`. Never install into the system interpreter with `pip` on a distribution-managed Python; the environment keeps the OS safe.
- **Indentation is syntax.** A block is defined by consistent indentation (four spaces by convention), not braces.
- **Data types**: integer, floating point, string, boolean, list (ordered, mutable), and dictionary (key to value).
- **Modules and packages** extend the language. The standard library has many built-ins useful to administrators, such as `os`, `pathlib`, `subprocess`, `shutil`, `json` and `argparse`.
- **PEP 8** is the style guide: four-space indents, snake_case names, readable line length.

```python
#!/usr/bin/env python3
import json
import shutil
from pathlib import Path

def disk_report(paths):
    report = {}
    for p in paths:
        usage = shutil.disk_usage(p)
        report[str(p)] = round(usage.used / usage.total * 100, 1)
    return report

if __name__ == "__main__":
    print(json.dumps(disk_report([Path("/"), Path("/var")]), indent=2))
```

**[📖 venv - creation of virtual environments](https://docs.python.org/3/library/venv.html)** - Creating and activating a virtual environment

## 4.4 Git

Git tracks changes in a repository. The commands to recognize, grouped by job:

| Job | Commands |
|---|---|
| Start | `git init`, `git clone <url>`, `git config user.name "Name"` |
| Record changes | `git add`, `git commit -m "message"`, `git diff`, `git log` |
| Ignore files | list patterns in `.gitignore` (build output, secrets) |
| Branches | `git branch`, `git checkout` (or `switch`), `git merge`, `git tag` |
| Share | `git fetch` (download, no merge), `git pull` (fetch and merge), `git push` |
| Rewrite or park | `git rebase`, `git reset`, `git stash`, squash (combine commits into one) |

The distinction that appears in questions: `fetch` only downloads remote changes; `pull` is `fetch` plus a merge into your current branch. `merge` joins histories with a merge commit; `rebase` replays your commits on top of another branch for a linear history, and should not be done to commits others have already pulled. `reset` moves the branch pointer and can discard work; `stash` temporarily shelves uncommitted changes.

**[📖 git rebase](https://git-scm.com/docs/git-rebase)** - How rebase replays commits and when it is risky

## 4.5 Responsible use of AI

New in this exam version. The objective is about using AI assistants safely in administration work, not about building models.

**Common use cases:** generating scripts or regular expressions, drafting infrastructure as code, documenting code, suggesting compliance improvements, reviewing for security problems, optimizing and linting code.

**Best practices:**

- **Never run unreviewed output.** Read generated commands and code, test them somewhere safe, and understand them before they touch production.
- **Verify the result.** Assistants can produce plausible but wrong syntax, nonexistent options or outdated advice. Check against documentation.
- **Protect data.** Do not paste secrets, credentials, customer data or confidential configuration into a public model. Know whether the model is **private** (self-hosted or under your organization's contract) or **public**, and whether your input may be used for model **training**. A **local model** keeps data on your own hardware.
- **Follow corporate policy** and data governance rules about what may be shared.
- **Prompt engineering:** clear, specific prompts with context, constraints and the expected format produce better results.
- **Keep a human in the loop** for review and accountability.

## Common exam traps

- `fetch` does not change your working files; `pull` does.
- `[[ $a > $b ]]` compares as strings, not numbers.
- `$?` holds the exit status of the last command only; read it immediately.
- A subshell's variable changes disappear when it ends.
- A playbook task that runs a shell command is not automatically idempotent.
- Agentless (Ansible) means no software on managed nodes beyond SSH and Python; Puppet's agent model pulls.
- Secrets go in a vault, never in Git.

## Key terms

- **Infrastructure as code** - describing servers, networks and configuration in versioned files so environments can be reviewed and reproduced.
- **Ansible** - an agentless automation tool that runs idempotent modules from YAML playbooks over SSH.
- **Playbook** - an Ansible YAML file that lists the tasks to run against hosts from the inventory.
- **Inventory** - the Ansible list of managed hosts and groups.
- **Idempotence** - the property that running an operation repeatedly leaves the system in the same state as running it once.
- **Puppet** - a configuration management tool that typically uses an agent to pull a catalog describing desired state from a server.
- **OpenTofu** - an open source infrastructure-as-code tool, compatible with Terraform workflows, that plans and applies changes through providers.
- **Kickstart** - the answer file format that automates installation of Red Hat-family systems.
- **cloud-init** - configures a cloud instance at first boot from user data such as users, keys and packages.
- **CI/CD** - continuous integration and continuous delivery or deployment, the automated build, test and release of changes.
- **GitOps** - managing infrastructure by keeping its desired state in Git and automatically reconciling the environment to match.
- **Shift-left testing** - moving testing and security checks earlier in the development pipeline.
- **DevSecOps** - building security checks into every stage of development and operations.
- **Pod** - the smallest deployable Kubernetes unit, one or more containers sharing network and storage.
- **ConfigMap** - a Kubernetes object that holds non-secret configuration for pods.
- **Compose file** - a YAML file describing a multi-container application started with docker compose up.
- **Docker Swarm** - Docker's built-in clustering and orchestration mode with services, tasks and nodes.
- **Shebang** - the #! interpreter directive on a script's first line naming the program that runs it.
- **Exit status** - the number a command returns, 0 for success and nonzero for failure, available in $?.
- **Command substitution** - replaces $(command) with the command's output inside another command.
- **Subshell** - a child shell, such as a parenthesized group, whose variable and directory changes do not affect the parent.
- **IFS** - the Internal Field Separator, which determines how the shell splits text into words.
- **Virtual environment** - an isolated Python environment with its own packages, created with python3 -m venv.
- **PEP 8** - the Python style guide covering indentation, naming and layout.
- **git fetch** - downloads new remote commits without changing your working files or current branch.
- **git pull** - fetches remote changes and merges them into the current branch.
- **git rebase** - replays commits on top of another base to produce a linear history.
- **git stash** - temporarily shelves uncommitted changes so the working tree is clean.
- **.gitignore** - a file listing patterns Git should not track, such as build output and secrets.
- **Prompt engineering** - writing clear, specific instructions with context and constraints to get better output from an AI model.
- **Local model** - an AI model run on hardware you control, so prompts and data do not leave your environment.
