---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 12 min
---

# Python for Cloud

> **12-minute read. Assumes you've read [Terminal basics](./terminal-basics.md), [Package managers](./package-managers.md) and [JSON and YAML](./json-and-yaml.md).**

## Why this page exists

Cloud work is full of small scripts: list the servers that are too busy, call an API, read a config file, glue two services together. Python is the usual tool because it is readable and every cloud has a Python SDK. This page covers the five things you need to start: a virtual environment, installing packages, running a script, reading JSON, and calling an API or a cloud SDK. It does not teach the language itself.

## How the samples here were checked

Every sample below was run on Python 3.12.14 in a virtual environment outside the repo. That environment was created with `uv venv` and packages were added with `uv pip install`, because the system Python on the test machine could create a venv but had no `pip` inside it. So the plain `python3 -m venv` and `pip` commands in step 1 and 2 are from the Python docs and were **not run here**. The versions used were `requests 2.34.2` and `boto3 1.43.126`. The output shown is real, except that the AWS account number is replaced with a dummy.

## 1. Make a virtual environment

A **virtual environment** is a private folder of packages for one project, so project A's libraries cannot break project B's. Make one per project.

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS and Linux
.venv\Scripts\activate           # Windows
```

Your prompt now shows `(.venv)`. Leave with `deactivate`. The Python tutorial uses these same commands (it names the folder `tutorial-env` and notes `.venv` is a common choice). Add `.venv/` to `.gitignore`: it is rebuilt, never committed.

**[📖 Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html)** - Python docs

## 2. Install packages with pip

```bash
python -m pip install requests boto3
python -m pip freeze > requirements.txt     # save exact versions
python -m pip install -r requirements.txt   # recreate it elsewhere
```

Commit `requirements.txt`. A teammate (or a build server) gets the same versions with the last command. See [Package managers](./package-managers.md) for how this compares to npm and apt.

## 3. Run a script

Save this as `hello.py`:

```python
import os

name = os.environ.get("GREETING_NAME", "world")
print(f"hello, {name}")
```

```bash
$ python hello.py
hello, world
$ GREETING_NAME=Alice python hello.py
hello, Alice
```

The second run sets an environment variable for that one command. `os.environ.get(name, default)` returns the default when the variable is missing. Use `os.environ["NAME"]` when it is required:

```text
$ python -c "import os; os.environ['NOPE']"
KeyError: 'NOPE'
```

A `KeyError` at startup is what you want when config is missing: the script stops at once and names the missing variable. Remember every value is a string. More in [Environment variables and config](./environment-variables-and-config.md).

## 4. Read JSON

Save as `servers.json`:

```json
{"servers": [{"name": "web-1", "region": "us-east-1", "cpu": 12.5}, {"name": "web-2", "region": "eu-west-1", "cpu": 91.0}]}
```

and as `read_json.py`:

```python
import json

with open("servers.json") as f:
    data = json.load(f)

for s in data["servers"]:
    flag = "HOT" if s["cpu"] > 80 else "ok"
    print(f'{s["name"]:8} {s["region"]:10} {s["cpu"]:5.1f}% {flag}')
```

```text
$ python read_json.py
web-1    us-east-1   12.5% ok
web-2    eu-west-1   91.0% HOT
```

`json.load` turns JSON into ordinary Python dictionaries and lists, so `data["servers"]` is a list and each `s` is a dictionary. The `with` line opens the file and closes it afterwards, even if something fails. Python's `json.loads` does the same from a string, which is what you use on an API response body.

## 5. Call an HTTP API

This calls GitHub's public API. Save as `http_call.py`:

```python
import requests

resp = requests.get("https://api.github.com/repos/python/cpython", timeout=10)
resp.raise_for_status()
repo = resp.json()
print(resp.status_code, repo["full_name"], repo["license"]["spdx_id"])
```

```text
$ python http_call.py
200 python/cpython NOASSERTION
```

Three habits worth keeping:

- **Always set `timeout`.** Without it a hung server hangs your script.
- **Call `raise_for_status()`.** It turns a 4xx or 5xx response into an exception, so failures are not silent. Status codes are explained in [What is an API call?](./what-is-an-api-call.md).
- **`resp.json()` parses the body** like `json.loads`.

## 6. Call a cloud SDK

Every cloud has an SDK, which is an API client packaged as a library: `boto3` for AWS, `azure-*` packages for Azure, `google-cloud-*` for Google Cloud. This asks AWS who you are, the safest first call because it changes nothing:

```python
import boto3

sts = boto3.client("sts", region_name="us-east-1")
print(sts.get_caller_identity()["Account"])
```

With credentials configured and `AWS_PROFILE` set:

```text
$ AWS_PROFILE=myprofile python sdk.py
123456789012
```

(The real run printed an actual account number; it is masked here.) Boto3 looks for credentials in a fixed order and stops at the first match: parameters you pass, then environment variables, then role-based providers, then the shared credentials and config files, then container and instance metadata. The profile can be picked with the `AWS_PROFILE` variable or in code with `boto3.Session(profile_name=...)`.

**[📖 Boto3 credentials](https://docs.aws.amazon.com/boto3/latest/guide/credentials.html)** - the full search order

With no credentials anywhere, it fails clearly rather than guessing:

```text
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

That error is the most common first-day failure. Fix it by setting `AWS_PROFILE` or running your cloud's login command, never by pasting keys into the script. Keys in code end up in git. See [Cloud identity basics for builders](../concepts/cloud-identity-basics-for-builders.md).

## Common mistakes

- **Installing into the system Python** instead of a venv, then hitting version conflicts later. Check the `(.venv)` in your prompt.
- **Forgetting to activate** the venv in a new terminal, so `import requests` fails. Each new terminal needs `source .venv/bin/activate`.
- **Hard-coding secrets** in the script.
- **No timeout on requests**, or ignoring the status code.
- **Pointing a script at the wrong account.** Run `get_caller_identity` first when a script will create or delete things.

## What was not run

- `python3 -m venv` plus `pip` (the system Python on the test machine had no pip in its venvs; `uv` was used instead).
- The Windows activation line.
- The Azure and Google Cloud SDK package names are from general knowledge and were not installed or checked against docs.

## Go deeper

- **[📖 Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html)**
- **[📖 Boto3 credentials](https://docs.aws.amazon.com/boto3/latest/guide/credentials.html)**

## What to look at next

- **[Environment variables and config](./environment-variables-and-config.md)**
- **[Reading error messages](./reading-error-messages.md)** - for the tracebacks you will see
- **[Infrastructure as code explained](../concepts/infrastructure-as-code-explained.md)** - when scripts should become declared infrastructure
