---
last-updated: 2026-11-07
difficulty: intermediate
---

# HashiCorp Terraform Associate (004) - Practice Questions

32 scenario-based questions for Terraform Associate prep. Questions 1-25 cover the objectives carried over from 003. Questions 26-32 cover content that is new in 004 (lifecycle rules, custom conditions, ephemeral values, HCP Terraform workspaces and projects).

> **Cert page:** [exams/hashicorp/terraform-associate/](../../exams/hashicorp/terraform-associate/)

---

### Question 1
**Scenario:** A new team member runs `terraform plan` and sees changes they didn't make. The state file is in S3. What's most likely?

A. Drift detection is permanent, so plan always reports differences between the code and the cloud
B. Terraform is buggy and reports differences that do not exist in the real infrastructure
C. Someone changed resources outside Terraform
D. The team member's local Terraform CLI is newer than the one that last wrote the state

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** This is **drift** - the actual infrastructure state differs from what Terraform recorded. Manual console changes, other tools modifying resources, or state file corruption can cause this. `terraform plan -refresh-only` (or `apply -refresh-only`) shows and records the drift; the older `terraform refresh` command is deprecated. Avoid manual changes to TF-managed resources.
</details>

---

### Question 2
**Scenario:** You want to share Terraform state across a team and prevent simultaneous applies. What backend feature do you need?

A. Remote state with state locking (for example the S3 backend with locking enabled, or Terraform Cloud)
B. Local state with git
C. Encrypted local state
D. Terraform Cloud only, since open-source Terraform has no way to lock a remote backend

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Remote state (S3, Azure Storage, GCS, Terraform Cloud, Consul) supports state locking. S3 locking is opt-in: `use_lockfile = true`, or the older `dynamodb_table` setting, which is deprecated. Without locking, two simultaneous `apply` operations corrupt state. Local state with git races on commit; not safe.
</details>

---

### Question 3
**Scenario:** What's the difference between `terraform import` and `terraform apply`?

A. They're equivalent
B. `apply` is read-only
C. `import` brings existing infrastructure into Terraform state without modifying it; `apply` modifies infrastructure to match config
D. `import` is destructive

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** `import` adds an existing resource (created outside Terraform) to the state file. You still need to write matching config; `import` doesn't generate config. After import, run `plan` to verify config matches reality.
</details>

---

### Question 4
**Scenario:** A module input variable should be required but no default value should be set. What's the right declaration?

A. Use `sensitive = true`
B. Just declare the variable without a `default` - Terraform will require it
C. Use `validation` block
D. Set `default = null` and check at runtime with a precondition, which makes the variable optional

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A variable without `default` is required. If users don't pass it, Terraform errors out at plan time. `null` default makes it optional with null fallback.
</details>

---

### Question 5
**Scenario:** Sensitive output (e.g., a generated password) should be stored in state but not displayed in plan/apply output. How?

A. Keep the value in a separate state file that only the pipeline can read
B. `sensitive = true` on the output declaration
C. Don't put sensitive data in state, because Terraform never stores outputs after an apply completes
D. Encrypt the entire state file with a customer-managed key before each apply

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** `sensitive = true` on output (or variable) hides it from CLI output. The value is still in state - that's why state files should be in encrypted-at-rest backends. Use Vault for true secret management.
</details>

---

### Question 6
**Scenario:** A `count = 3` resource is replaced with `for_each` over 3 named items. After this change, what happens?

A. Terraform recognizes them as the same three resources and plans no changes at all
B. Terraform errors out because count and for_each cannot be swapped on an existing resource
C. Terraform converts the state addresses automatically during the next plan and keeps the resources
D. Plan to destroy 3 and create 3, because the resource addresses change

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Resource addresses change between `count` and `for_each`. Terraform sees this as destroy+create unless you use `terraform state mv` to remap. For long-lived resources, prefer `for_each` from the start to avoid this churn.
</details>

---

### Question 7
**Scenario:** Provider versions should be pinned for reproducibility. Where?

A. In `terraform { required_providers { ... version = "~> 4.0" } }`
B. In environment variables
C. In the state file, beside the resource attributes that Terraform records after each apply
D. In the backend configuration block, alongside the bucket and key arguments for remote state

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Pin in `required_providers`. `~> 4.0` allows `>= 4.0, < 5.0`. Use `terraform init` to install. The `.terraform.lock.hcl` file (committed to git) records exact versions for reproducibility.
</details>

---

### Question 8
**Scenario:** Workspaces in OSS Terraform vs Terraform Cloud - what's a key difference?

A. They're identical
B. OSS workspaces are state-file-level (one state per workspace, same backend); Cloud workspaces are full execution environments with their own variables and config
C. OSS workspaces require Cloud
D. Cloud workspaces don't have state

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** OSS `terraform workspace` creates separate state files in the same backend - same code, different state. Cloud workspaces are first-class objects with their own variables, run history, RBAC, and execution.
</details>

---

### Question 9
**Scenario:** What does `terraform fmt` do?

A. Validates syntax
B. Generates documentation for each module's inputs and outputs as a README file in the repository
C. Tests the configuration by running its modules against a temporary test environment
D. Formats `.tf` files to canonical style (whitespace, alignment, ordering)

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** `fmt` is a formatter (analogous to `gofmt`). It rewrites files to canonical style. `validate` checks syntax. `terraform-docs` (third-party) generates docs.
</details>

---

### Question 10
**Scenario:** A module is published to the Terraform Registry as `myorg/network/aws`. How do you reference it in a config?

A. `module "net" { source = "registry/myorg/network/aws" version = "1.2.3" }`
B. `module "net" { source = "git::https://registry.terraform.io/myorg/network/aws.git" }`
C. `module "net" { source = "./modules/myorg/network/aws" version = "1.2.3" }`
D. `module "net" { source = "myorg/network/aws" version = "1.2.3" }`

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Public registry modules use `<namespace>/<name>/<provider>` and Terraform implicitly resolves to registry.terraform.io. Versions are highly recommended. A local path, a git URL, or a made-up registry prefix does not reference a registry module this way.
</details>

---

### Question 11
**Scenario:** When does Terraform create an implicit dependency between resources?

A. Never; you must use `depends_on` on every resource, since Terraform cannot infer ordering from attribute references
B. When one resource references another's attribute (e.g., `aws_subnet.id` referenced by `aws_instance`)
C. Only within the same module
D. Only when explicitly declared

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Attribute references create implicit dependencies in the dependency graph. `depends_on` is for cases where there's no attribute reference but ordering still matters (e.g., IAM policy must exist before EC2 launches).
</details>

---

### Question 12
**Scenario:** Backend `partial configuration` with `terraform init -backend-config=...` is useful for what?

A. Merging backend blocks from several modules into one combined state file during apply, so that separate teams share a single backend and a single lock
B. Skipping state locking and state refresh so that init finishes faster in CI pipelines
C. Downloading provider plugins from a private mirror instead of the public registry
D. Supplying backend settings such as the bucket or access keys at init time, keeping secrets out of git and varying them per environment

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Partial config lets you specify backend at init time via `-backend-config="bucket=mybucket"` or a `.hcl` file. Common for: keeping bucket names per-env, keeping access keys out of git, switching prod/staging buckets. It does not merge states, disable locking, or change where providers come from.
</details>

---

### Question 13
**Scenario:** What does `terraform taint` do (still supported but deprecated)?

A. Marks a resource for replacement on next apply
B. Locks the resource
C. Permanently breaks the resource so Terraform stops managing it and drops it from the plan
D. Removes from state

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** `taint` marks a resource for destroy+create on next apply. Modern equivalent: `terraform apply -replace=<resource>` (preferred since 0.15.2). Useful when you've changed an external dependency that Terraform doesn't track.
</details>

---

### Question 14
**Scenario:** A child module needs to expose a value to its caller. How?

A. Output blocks in the module
B. Variables
C. Provider configuration blocks passed through to the module call
D. Resource attributes of the parent module, read directly by the child module at plan time

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Module outputs are the explicit interface for what callers can consume. Caller accesses with `module.<name>.<output_name>`. Variables flow IN; outputs flow OUT.
</details>

---

### Question 15
**Scenario:** What's the order of operations for `terraform apply`?

A. Validate, plan, apply, format
B. Read config, refresh state, plan, prompt for approval, apply, update state
C. Plan, apply, then refresh state from the real infrastructure
D. Apply changes, then plan

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** `apply` reads config + current state, refreshes state from real infra (unless `-refresh=false`), generates plan, prompts unless `-auto-approve`, applies in dependency order, then writes new state.
</details>

---

### Question 16
**Scenario:** Your team uses the S3 backend with the legacy `dynamodb_table` setting. What does the DynamoDB table provide?

A. State locking (preventing concurrent applies)
B. Audit history
C. State storage - DynamoDB holds the state file contents while S3 stores only the lock record
D. Encryption keys for the state file stored in S3 and used to decrypt it

<details><summary>Answer</summary>

**Correct: A**

**Why:** S3 stores the state file; DynamoDB stores a lock entry while an `apply` is running. The lock prevents two engineers from running `apply` simultaneously and corrupting state. DynamoDB-based locking is deprecated; newer configurations use `use_lockfile = true` to keep the lock in S3.
</details>

---

### Question 17
**Scenario:** You need to import an existing AWS resource (e.g., a manually-created S3 bucket) into Terraform management.

A. Manually edit the state file to add an entry for the bucket
B. Run `terraform refresh` so that the existing bucket is detected and added
C. Recreate the bucket via Terraform with the same name after deleting the manually created one
D. `terraform import aws_s3_bucket.b bucket-name`

<details><summary>Answer</summary>

**Correct: D**

**Why:** `terraform import` brings existing resources under management, mapping a real-world resource ID to a TF resource address. You also need the `resource "aws_s3_bucket" "mybucket" {}` block in your config (Terraform 1.5+ supports `import` blocks too).
</details>

---

### Question 18
**Scenario:** Best way to share infrastructure modules across teams:

A. Hardcode in each repo
B. Copy/paste HCL between repos
C. Publish to the public Terraform Registry, a private registry (Terraform Cloud / Enterprise), or a versioned git tag
D. Use raw Bash scripts

<details><summary>Answer</summary>

**Correct: C**

**Why:** Modules are TF's reuse unit. Source from public registry, private registry, git (`git::https://...?ref=v1.2.0`), or local paths. Versioning is critical so consumers don't break on upstream changes.
</details>

---

### Question 19
**Scenario:** What's `count` vs `for_each` for module / resource iteration?

A. They're identical
B. `for_each` is deprecated
C. `count` is for modules only
D. `count` uses an integer (creates N indexed copies); `for_each` uses a map or set of strings (creates one per key)

<details><summary>Answer</summary>

**Correct: D**

**Why:** Use `for_each` when you have a logical key (e.g., per-tenant config); resources are addressed by key. Use `count` when truly indexed (e.g., 3 identical replicas). `count` is fragile to reordering; `for_each` is more robust.
</details>

---

### Question 20
**Scenario:** Sensitive output value (e.g., DB password) needs to be passed to a downstream module.

A. Commit the value to git in a terraform.tfvars file so the downstream module can read it from the repository
B. Mark output as `sensitive = true`; pass to downstream module input variable also marked sensitive
C. Print it to the console in the apply output so that the downstream pipeline job can copy the value by hand
D. Email it

<details><summary>Answer</summary>

**Correct: B**

**Why:** `sensitive = true` masks the value in CLI output and `terraform plan`. Still stored in state (encrypt the backend), but not displayed. The full path: source secret in a manager (Vault, Secrets Manager) and use a data source instead of putting the value through TF at all.
</details>

---

### Question 21
**Scenario:** Workspaces in Terraform - what are they for?

A. Separate state files for one config (dev, staging, prod)
B. Provider versioning - pinning a different provider release for each environment of one configuration
C. Module isolation - hiding the internal resources of a module from the calling configuration
D. Visual editing - a graphical canvas for drawing resources and wiring them together

<details><summary>Answer</summary>

**Correct: A**

**Why:** Workspaces give you multiple state files for the same config. Use case: same module deployed to dev/staging/prod with different vars. Modern best practice prefers separate directories or backend configs over workspaces for production environment isolation.
</details>

---

### Question 22
**Scenario:** A Terraform provider defines:

A. Module syntax
B. State encryption
C. Cloud-specific resource and data source types
D. Backend storage - where state is stored and how locking is performed for the configuration

<details><summary>Answer</summary>

**Correct: C**

**Why:** Providers (`aws`, `azurerm`, `google`, `kubernetes`, `random`, etc.) implement resources and data sources for a target API. Terraform Core handles graph + state; providers handle CRUD against APIs.
</details>

---

### Question 23
**Scenario:** What does `terraform validate` do?

A. Checks syntax and consistency without contacting providers
B. Applies the plan after confirming the configuration against the real infrastructure first
C. Refreshes the state file from the real infrastructure and writes the result back
D. Tests the configuration in production by creating a temporary copy of each resource

<details><summary>Answer</summary>

**Correct: A**

**Why:** `validate` checks HCL syntax and references inside the config. Doesn't talk to provider APIs (so it's fast and offline). Used in CI before `plan`.
</details>

---

### Question 24
**Scenario:** Best way to handle provider version constraints:

A. Pin the version globally in an environment variable set on each engineer's laptop and in the CI runner
B. Edit ~/.terraform.d/
C. Don't pin; use the latest release so the configuration always picks up the newest provider bug fixes automatically
D. Pin in `required_providers` in a `terraform { ... }` block; commit `.terraform.lock.hcl`

<details><summary>Answer</summary>

**Correct: D**

**Why:** Pin major and minor (e.g., `~> 5.0` for AWS provider 5.x). The lock file (`.terraform.lock.hcl`) records exact versions across providers and platforms; commit it for reproducibility.
</details>

---

### Question 25
**Scenario:** Drift - someone changed a resource in the cloud console.

A. Delete state
B. Recreate everything
C. Ignore
D. Run `terraform plan` to see drift; either accept the change into config or `terraform apply` to revert

<details><summary>Answer</summary>

**Correct: D**

**Why:** `plan` shows the difference between config and reality. You then decide: update config to match reality (accept the change) or `apply` to overwrite reality with config (revert). Drift detection should be regular (CI cron, Terraform Cloud).
</details>

---

## Scoring guide

- **22-25:** Ready. Combine with HashiCorp's official prep + a Udemy course for confidence.
- **17-21:** Solid; review weak areas.
- **<17:** Hands-on practice + re-read fact-sheet.

Terraform Associate is multiple-choice and 1 hour long; HashiCorp's page does not state the question count. These reinforce concepts; for full coverage see HashiCorp Learn and the [exams/hashicorp/terraform-associate/](../../exams/hashicorp/terraform-associate/) materials.

### Question 26
**Scenario:** A team replaces an object that has a unique name constraint managed by Terraform. Replacement currently destroys the old object first and creates an outage. They want the new object created first and have used a name prefix to avoid collisions.

A. Set create_before_destroy = true in the resource's lifecycle block
B. Set prevent_destroy = true in the lifecycle block
C. Add ignore_changes = all to the lifecycle block
D. Add depends_on pointing at the old object

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** create_before_destroy reverses the default replace order, creating the replacement before destroying the existing object. depends_on controls ordering between resources, prevent_destroy rejects destroying plans, and ignore_changes suppresses diffs.
</details>

---

### Question 27
**Scenario:** A web instance needs an IAM policy attached before its software boots, but nothing in the instance block references the policy resource, so Terraform sometimes creates them in parallel. What is the correct fix?

A. Wrap the policy in a precondition
B. Move both resources to separate workspaces
C. Add depends_on = [aws_iam_role_policy.app] to the instance
D. Run terraform apply twice

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** depends_on declares a hidden dependency that Terraform cannot infer from references. Applying twice is not a design, a precondition validates assumptions rather than ordering, and splitting workspaces does not create an ordering within one configuration.
</details>

---

### Question 28
**Scenario:** Which statement about a check block is correct?

A. A failed check stops the plan with an error, like a precondition
B. A failed check reports a warning without blocking the run
C. A check block can only be used inside a variable block
D. A check block runs only during terraform init

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Check blocks validate that infrastructure works as expected without blocking operations; failures appear as warnings. Variable validation, preconditions and postconditions do block.
</details>

---

### Question 29
**Scenario:** A module author wants a clear error during planning if the selected AMI is not for the x86_64 architecture, before the instance is created. Which feature fits?

A. terraform fmt
B. An output with sensitive = true
C. A postcondition on the aws_instance
D. A precondition in the aws_instance lifecycle block referencing the AMI data source

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Preconditions are evaluated during planning and verify assumptions before an object is created. A postcondition runs after the object exists, fmt only formats code, and sensitive affects display.
</details>

---

### Question 30
**Scenario:** An engineer wants a generated database password to be used during apply without being stored in the state or plan files. Which approach does this?

A. Write it to a .tfvars file committed to Git
B. Mark the variable sensitive = true
C. Generate it with an ephemeral resource and pass it to a write-only argument
D. Store it in a local value

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Ephemeral resources and write-only arguments are not persisted in state or plan files. sensitive = true hides output but the value is still stored in state, and the other options expose or store the secret.
</details>

---

### Question 31
**Scenario:** After adding a write-only argument such as password_wo to a database resource, the team wants Terraform to apply a new password. Terraform did not store the old value. How is the change signaled?

A. Change the companion version argument, for example increment password_wo_version
B. Delete the state file
C. Terraform detects the change automatically by hashing the password
D. Run terraform refresh

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Because the value is never stored, Terraform cannot compare it. A companion version argument is changed to tell Terraform the value was updated.
</details>

---

### Question 32
**Scenario:** In HCP Terraform, an organization wants to group related workspaces and grant a team access to all of them, and have new workspaces inherit tags. What should they use?

A. A Terraform CLI workspace
B. A variable set
C. A run trigger
D. A project

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Projects group workspaces and carry team permissions and tags that workspaces created inside inherit. CLI workspaces are state files in one directory, variable sets share variables, and run triggers queue runs between workspaces.
</details>

---
