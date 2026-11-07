---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 9 min
---

# 03 - Kyverno CLI

**Domain 3: Kyverno CLI (12%)**

Curriculum topics, in order: apply, test, jp, Installing Kyverno CLI.

The CLI lets you check policies against resources **without a cluster**, which is what makes policy-as-code in CI possible. All commands here come from the CLI reference pages and were **not run**: the Kyverno CLI binary was not available when this guide was written.

---

## Installing the CLI

Methods listed on the CLI page:

| Method | Command |
|---|---|
| Homebrew | `brew install kyverno` |
| Krew (kubectl plugin) | `kubectl krew install kyverno`, then verify with `kubectl kyverno version` |
| Binary | Download the archive from the GitHub releases page, extract it, copy `kyverno` onto your PATH |
| From source | Clone `kyverno/kyverno`, run `make build-cli` (needs Go), move the built binary onto your PATH |

The page also lists an AUR package and a GitHub Actions marketplace installer. The root command's subcommands are `apply`, `completion`, `create`, `docs`, `jp`, `json`, `migrate`, `test` and `version`. Experimental commands need `KYVERNO_EXPERIMENTAL=true`.

**[📖 Kyverno CLI overview](https://kyverno.io/docs/subprojects/kyverno-cli/)** - install methods and examples

---

## `kyverno apply`

Applies policies to resources, from files or from a live cluster. Reference usage: `kyverno apply [flags]`, policy paths as arguments.

```bash
# Apply a policy to a resource file
kyverno apply /path/to/policy.yaml --resource /path/to/resource.yaml

# Apply a policy to all matching resources in the current cluster
kyverno apply /path/to/policy.yaml --cluster

# Pass variables from a values file
kyverno apply /path/to/policy.yaml --resource /path/to/resource.yaml -f /path/to/value.yaml

# Generate a policy report
kyverno apply /path/to/policy.yaml --cluster --policy-report
```

Flags worth knowing:

| Flag | What it does |
|---|---|
| `-r, --resource` | Paths to resource files |
| `-c, --cluster` | Use resources from the current kubeconfig context's cluster |
| `-n, --namespace` | Namespace filter, used with `--cluster` |
| `-s, --set` | Values for required variables |
| `-f, --values-file` | File of values for policy variables |
| `-u, --userinfo` | Admission info (roles, cluster roles, subjects) to simulate a user |
| `-o, --output` | Write mutated or generated resources to a file or directory |
| `-p, --policy-report` | Generate a policy report |
| `-t, --table` | Show results as a table |
| `--audit-warn` | Report audit-mode violations as warnings, not failures |
| `-e, --exception` | Policy exception to consider |
| `--detailed-results` | Show detailed results |
| `--warn-exit-code` | Exit code to use for warnings (failures and errors still exit 1) |
| `--warnings-as-errors` | Treat deprecation warnings as errors |

Think of the exit code as the CI contract: failures exit non-zero, so a pipeline step that runs `kyverno apply` blocks a merge when a manifest breaks a policy. For `mutate` and `generate` policies, `-o` is how you see the result.

**[📖 kyverno apply reference](https://kyverno.io/docs/kyverno-cli/reference/kyverno_apply/)** - every flag

---

## `kyverno test`

Runs declared test cases: you state the result you expect, and Kyverno compares it with what it computes. Usage: `kyverno test [local folder or git repository]... [flags]`. The default file name is `kyverno-test.yaml` (change with `-f, --file-name`).

```bash
# Test a local folder containing test cases
kyverno test .

# Test a git repository containing Kyverno test cases
kyverno test https://github.com/kyverno/policies/pod-security --git-branch main

# Run only selected test cases
kyverno test . --test-case-selector "policy=disallow-latest-tag, rule=require-image-tag, resource=test-require-image-tag-pass"
```

Flags: `--fail-only` (show only failures), `-o, --output-format` (`json`, `yaml`, `markdown` or `junit`), `--require-tests` (error if no tests are found), `-t, --test-case-selector` (default `policy=*,rule=*,resource=*`), `--detailed-results`.

The test file format, from the CLI page:

```yaml
apiVersion: cli.kyverno.io/v1alpha1
kind: Test
metadata:
  name: disallow_latest_tag
policies:
  - disallow_latest_tag.yaml
resources:
  - resource.yaml
results:
  - policy: disallow-latest-tag
    rule: require-image-tag
    resources:
      - myapp-pod
    kind: Pod
    result: pass
```

- `policies` - paths to policy files.
- `resources` - paths to resource files.
- `results` - the expected outcome for each policy, rule and resource. `result` is `pass`, `fail`, `skip` or `warn`. A test passes only when expected equals actual.
- `mutate` and `generate` results also need `patchedResources` or `generatedResource`.

A good test suite has at least one resource that must pass and one that must fail for every rule. A policy with only passing examples can be wrong in the permissive direction and nobody would notice.

**[📖 kyverno test reference](https://kyverno.io/docs/kyverno-cli/reference/kyverno_test/)** - flags and examples

---

## `kyverno jp`

A JMESPath command-line, extended with Kyverno's custom functions. You use it to debug the expressions inside policies before you put them in YAML. Subcommands: `function`, `parse`, `query`.

```bash
# List functions
kyverno jp function

# Evaluate query
kyverno jp query -i object.yaml 'request.object.metadata.name | truncate(@, `9`)'

# Parse expression
kyverno jp parse 'request.object.metadata.name | truncate(@, `9`)'
```

- `function` lists the functions available, including Kyverno's additions.
- `query` evaluates an expression against an input document (`-i`).
- `parse` shows the expression's AST, which helps when a query fails to parse.

Quoting rule from the variables page: wrap plain numbers in backticks and resource quantities or durations in single quotes, as the `` `9` `` above shows.

**[📖 kyverno jp reference](https://kyverno.io/docs/kyverno-cli/reference/kyverno_jp/)** - subcommands and examples

---

## Key terms

- **kyverno apply** - the CLI command that evaluates policies against resource files or a cluster and prints results.
- **kyverno test** - the CLI command that runs declared expectations from a `kyverno-test.yaml` file.
- **kyverno-test.yaml** - the default test manifest, `kind: Test` in `cli.kyverno.io/v1alpha1`, listing policies, resources and expected results.
- **kyverno jp** - the CLI's JMESPath tool with Kyverno's custom functions.
- **JMESPath** - a query language for JSON that Kyverno uses in variables, preconditions and foreach lists.
- **Values file** - a file passed with `-f` that supplies variable values to `apply`.
- **Krew** - the kubectl plugin manager; `kubectl krew install kyverno` installs the CLI as a plugin.
- **Policy report (CLI)** - output of `apply --policy-report`, in the same open report format the cluster uses.
