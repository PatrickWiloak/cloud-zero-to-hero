---
last-updated: 2026-10-22
difficulty: advanced
---

# HashiCorp Terraform Authoring and Operations Advanced - Practice Questions

30 questions for the Terraform Authoring and Operations Advanced exam (previously listed as Terraform Authoring and Operations Professional), covering module design, state operations, workspaces, testing, and troubleshooting. Questions 16-30 are spread across its six published objectives (resource lifecycle, dynamic configuration, collaborative workflows, modules, providers, and HCP Terraform), which carry no published weights.

This exam is mostly performance-based: four hours of hands-on lab scenarios in a live environment, plus multiple-choice items (objective 6, HCP Terraform, is multiple choice only). These questions reinforce the reasoning behind the tasks rather than substituting for practice at a keyboard.

> **Cert page:** [exams/hashicorp/terraform-authoring-operations-pro/](../../exams/hashicorp/terraform-authoring-operations-pro/)

---

### Question 1
**Scenario:** A resource was created manually and must come under Terraform management without being recreated.

A. Edit the state file by hand to add an entry for the resource, since state is only a JSON document and Terraform will then manage it
B. An `import` block (or `terraform import`), then write configuration that matches the real resource
C. Delete the resource in the console and recreate it from configuration
D. Run `terraform apply` with matching configuration and let Terraform adopt the existing resource by name instead of recreating it

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Import brings the resource into state; the configuration still has to be written to match, and `terraform plan` is what tells you whether it does. Import blocks are preferable to the CLI command because they are reviewable in a plan and can generate configuration.
</details>

---

### Question 2
**Scenario:** A module must create a variable number of similar resources, each identified by a stable name.

A. `count` with an index over a list, so each instance is addressed as `resource[0]`, `resource[1]`
B. Duplicated resource blocks, one per instance, each with a hard-coded name so that every resource is explicit in the configuration
C. A separate child module call for every resource, each wrapping a single resource block
D. `for_each` over a map or set of strings, so each instance is addressed by its key such as `resource["web"]`

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** `for_each` keys resources by name, so removing one element does not shift the others. With `count`, deleting the middle element of a list renumbers everything after it and Terraform plans to destroy and recreate them, which is the classic footgun.
</details>

---

### Question 3
**Scenario:** State must be shared by a team with locking.

A. Email the state file to the next operator before each change, so that whoever applies next starts from the latest copy
B. A shared network drive that every engineer mounts, so everyone reads and writes the same state file in one location
C. A remote backend such as S3 with DynamoDB locking, Azure Storage, GCS, or HCP Terraform
D. Local state committed to git, so the history of every change is kept and teammates pull the latest state before applying

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Locking prevents two concurrent applies corrupting state, and remote backends also keep the state file, which contains sensitive values in plaintext, out of version control. Encryption at rest and restricted access on the backend are part of the requirement.
</details>

---

### Question 4
**Scenario:** A refactor moves a resource into a module without destroying it.

A. Destroy and recreate the resource at its new address in the module, since Terraform cannot track a resource across module boundaries
B. `moved` blocks describing the old and new addresses, so plan and apply move the state entry for every consumer of the module
C. Manual state editing of the JSON file to change the address, then pushing the edited state
D. Rename the resource block only, because Terraform matches infrastructure by its provider ID

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** `moved` blocks are declarative, reviewable, and travel with the configuration, so every consumer of a module gets the refactor applied automatically. `terraform state mv` does the same thing imperatively and has to be run by each operator, which is error-prone across a team.
</details>

---

### Question 5
**Scenario:** A module should expose only a supported interface.

A. Expose all internal resources through outputs so that consumers can reference whichever attributes they need directly
B. No input variables at all, with every value hard-coded inside the module so that consumers cannot configure it incorrectly
C. Define explicit input variables with types, validation, and descriptions, and outputs for what consumers need
D. Use only default values for every input, so that the module behaves the same way for every consumer and never fails validation

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Variable validation blocks catch bad input at plan time with a useful message instead of a provider error later. Precondition and postcondition blocks extend this to runtime assumptions, which is where a professional-level module differs from a beginner one.
</details>

---

### Question 6
**Scenario:** Provider credentials differ per environment while the configuration stays the same.

A. Comment out the sections that differ and uncomment the ones for the target environment before each run
B. Separate workspaces or separate root configurations with distinct variable files and provider configuration from the environment
C. One state file for all environments, switching credentials with environment variables before each plan and apply
D. Hard-code each environment's credentials in the provider block behind a conditional on a variable so that one configuration serves all

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Separate state per environment is the key property, whether achieved with workspaces or with distinct root modules; sharing one state across production and development means one bad apply can affect both. Credentials should come from the environment or a workload identity, never the configuration.
</details>

---

### Question 7
**Scenario:** A plan shows an unexpected replacement of a database.

A. Read the "forces replacement" annotation and add `lifecycle { prevent_destroy = true }` as a guardrail
B. Delete the state file so that Terraform forgets the database and plans a fresh create
C. Ignore the plan output, because replacements shown for a database are only a display artifact and apply performs an in-place update
D. Apply anyway, since the provider will preserve the data in a replaced database through its own snapshot and restore logic

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Terraform states exactly which attribute forces replacement, which usually points at a change that should be made differently or via `ignore_changes`. `prevent_destroy` turns a catastrophic apply into a failed plan, which is the outcome you want on a production database.
</details>

---

### Question 8
**Scenario:** Terraform must not manage a field that another system mutates.

A. Use `-target` on every plan and apply so the changed field is never included in the operation
B. Delete the attribute from state after each apply so that Terraform no longer sees any difference for that field
C. Remove the resource from the configuration and manage the whole resource manually from then on in the cloud console
D. `lifecycle { ignore_changes = [tags["LastScanned"]] }` on the resource, so only that attribute is skipped

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** `ignore_changes` scopes the exception to specific attributes so the rest of the resource stays managed. Broad workarounds such as `-target` on every apply hide drift everywhere else and are explicitly documented as an exceptional tool.
</details>

---

### Question 9
**Scenario:** Module quality must be verified automatically.

A. Manual review only, with a second engineer reading each pull request before the module version is tagged for release
B. Apply to production and see whether the resources come up, treating a successful apply as proof the module is correct
C. Documentation only, with a README that lists the inputs and outputs and an example showing how to call the module
D. The Terraform test framework (`terraform test`) with `run` blocks asserting plan and apply outcomes, plus `fmt` and `validate` in CI

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Native tests can run plan-only assertions cheaply and real apply tests against ephemeral infrastructure where correctness demands it. Combined with `fmt`, `validate`, and a policy check, this is what makes a shared module safe to publish.
</details>

---

### Question 10
**Scenario:** Policy must prevent creating resources without required tags.

A. Policy as code such as Sentinel or OPA, enforced between plan and apply
B. Post-hoc cleanup, with a scheduled script that finds untagged resources after creation and adds the missing tags
C. Code review only, with a required reviewer checking each pull request for the mandatory tags before it is merged
D. A naming convention document that tells engineers which tags are required, published on the internal wiki for every team

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Enforcing at the plan-to-apply gate means the rule applies to every change regardless of who authored it. Review catches what reviewers notice; policy catches everything, and it produces the evidence an auditor asks for.
</details>

---

### Question 11
**Scenario:** A large configuration takes 20 minutes to plan.

A. Split it into smaller root modules by lifecycle and blast radius, sharing values through data sources or a remote state data source
B. Reduce the provider version to an older release, which has fewer resources to load and so shortens the planning phase
C. Use `-target` routinely on every plan and apply so that only the resources being changed are evaluated each time
D. Disable refresh permanently with `-refresh=false` on every run, so Terraform never reads real infrastructure during planning

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Root module size drives both plan time and blast radius, and both improve from splitting along boundaries that change at different rates: networking, platform, application. `-target` is a debugging tool, not an architecture.
</details>

---

### Question 12
**Scenario:** A provider upgrade introduces a breaking change.

A. Never upgrade providers, staying on the version first installed
B. Always use the latest version by leaving the constraint open, so that every run benefits from the newest fixes and features
C. Pin provider versions with constraints, commit the dependency lock file, and upgrade deliberately with a plan review
D. Remove version constraints and the lock file so that Terraform resolves the best match for each operator at init time and in each CI run

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The `.terraform.lock.hcl` file pins exact versions and hashes so every operator and CI run resolves identically. Upgrades then become an explicit, reviewable change rather than something that happens to whoever initializes next.
</details>

---

### Question 13
**Scenario:** A sensitive output must not appear in CI logs.

A. Remove the output from the configuration, then read the value from state with `terraform output` whenever it is needed in a pipeline
B. Mark the output `sensitive = true`
C. Rename the output to something less obvious, so that log scanners and teammates reading the CI output do not recognize it
D. Encode the value with `base64encode` before output, so that the log shows only an encoded string instead of the plain secret

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Sensitive marking suppresses the value in plan and apply output and propagates through expressions that use it. Be clear about the limit: the value is still stored in plaintext in state, so state access control remains the real protection.
</details>

---

### Question 14
**Scenario:** Drift has occurred: someone changed a resource in the console.

A. Delete the state so that Terraform re-reads everything from the provider and no longer reports a difference
B. Import the resource again into the same address, which overwrites state with the console values
C. A refresh-only plan (or scheduled drift run) shows the difference, then revert by applying or adopt by updating the configuration
D. Nothing can be detected until the next apply, because Terraform only compares configuration with state and never queries the provider at any point during planning

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Detecting drift is a scheduled job, not an incident response. The decision afterward is a judgment call: reapply the configuration to revert, or update the configuration if the manual change was correct. Repeated drift usually signals a missing capability in the module.
</details>

---

### Question 15
**Scenario:** State has become corrupted after a failed apply.

A. Restore from the backend's versioning or the local backup, inspect with `terraform state list` and `show`, and repair with targeted state commands
B. Delete all resources with `terraform destroy` and re-apply, so that state and infrastructure begin again from a known point
C. Edit the JSON by hand as a first step on the live remote object, correcting the entries that look wrong
D. Start over with a new empty state and re-import each resource one at a time, discarding the corrupted file

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Versioned remote backends make restore the first option, which is why versioning on the state bucket is not optional. Direct JSON editing is the last resort and should be done on a copy, with `terraform state pull` and `push` rather than editing the remote object in place.
</details>

---

### Question 16
**Scenario:** A VM managed by Terraform has a corrupted disk. Its configuration is unchanged, but the team wants Terraform to destroy and recreate just that one instance in the next run.

A. Edit the state file by hand and delete the instance's `id` attribute so Terraform thinks it is missing
B. Run `terraform state rm` on the instance, then apply so Terraform creates a second copy beside the old one
C. Change an unrelated tag on the instance to force the provider to replace it
D. Run `terraform apply -replace=<address>` for that instance

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** `-replace` plans a destroy and recreate for one resource address and shows it in the plan for review; it replaces the older `taint` workflow. Hand-editing state is risky and unsupported. `state rm` makes Terraform forget the instance, so it creates a new one and leaves the broken one running and unmanaged. Changing a tag usually updates in place and does not force replacement.
</details>

---

### Question 17
**Scenario:** Changing a load balancer's name forces replacement. The service must not go down while the old one is destroyed and the new one is created.

A. Add `prevent_destroy = true` so the old load balancer is never removed during the change
B. Set `create_before_destroy = true` in the resource's `lifecycle` block
C. Run the apply with `-parallelism=1` so the destroy and create happen one after the other
D. Add `depends_on` from the load balancer to itself

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** `create_before_destroy` reverses the default order, so the replacement is created, and dependents can switch to it, before the old one is destroyed. `prevent_destroy` makes the plan fail instead of replacing anything. Parallelism controls how many operations run at once, not the order of a replacement. A resource cannot depend on itself; Terraform rejects the cycle.
</details>

---

### Question 18
**Scenario:** A production database must never be destroyed by an accidental plan, such as a renamed resource or a mistaken `terraform destroy`.

A. Add `prevent_destroy = true` in the database resource's `lifecycle` block
B. Mark every attribute of the database resource as `sensitive` in the configuration
C. Store the database's state in a separate workspace that nobody has write access to
D. Use `ignore_changes = all` on the database resource

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** `prevent_destroy` makes any plan that would destroy the resource fail with an error, which guards against renames and destroys. `sensitive` only hides values in output. A read-only workspace would block every legitimate change too. `ignore_changes = all` stops updates, but a plan can still destroy the resource, for example after a rename.
</details>

---

### Question 19
**Scenario:** A security group needs one ingress rule per entry in a list variable, and the number of entries varies by environment.

A. Write ten ingress blocks and comment out the unused ones per environment before each apply
B. Use `count` on the security group resource so each copy of the group gets one rule
C. Use a `dynamic "ingress"` block that iterates over the list variable
D. Use a `local-exec` provisioner

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A `dynamic` block generates nested blocks, such as `ingress`, from a collection, so the number of rules follows the variable. Commenting out blocks per environment is manual and error-prone. `count` on the resource creates several security groups, not several rules in one group. A provisioner bypasses the provider and leaves the rules out of state.
</details>

---

### Question 20
**Scenario:** A module's `environment` variable must be one of `dev`, `staging` or `prod`, and a bad value should fail with a clear message before any resources are planned.

A. Add a `validation` block to the variable with a `condition` and an `error_message`
B. Use the variable in a `count` expression so a bad value creates zero resources
C. Document the allowed values in the README and trust callers to read it before they set the variable
D. Mark the variable `nullable = false`

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Variable `validation` blocks check the value when it is set and fail with your own error message, before resources are planned. Creating zero resources hides the mistake instead of reporting it. Documentation helps but enforces nothing. `nullable = false` only rejects null, not wrong strings.
</details>

---

### Question 21
**Scenario:** A configuration looks up a machine image with a data source. If the image found is not `x86_64`, the run should stop with an explanation before the instance is created.

A. Add `ignore_changes` on the instance's image attribute so a wrong image is skipped
B. Use a `local-exec` provisioner on the instance that checks the image architecture after the instance is created
C. Put the check in an output value so it is printed at the end of the apply
D. Add a `postcondition` on the data source that checks the architecture and gives an error message

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Custom conditions such as a `postcondition` on the data source run as soon as its result is known and stop the run with a clear message before dependents are created; a `precondition` on the instance is an equally valid placement. `ignore_changes` only affects updates to an existing resource. A provisioner runs after creation, which is too late. An output is evaluated near the end and does not stop resources from being created.
</details>

---

### Question 22
**Scenario:** Two engineers and the CI pipeline get different provider versions from the same configuration, causing plan differences.

A. Delete the `.terraform` directory before every run so the newest provider is always downloaded
B. Commit the `.terraform.lock.hcl` file and update it on purpose with `terraform init -upgrade`
C. Remove the `required_providers` block so Terraform chooses one default version for everyone
D. Copy the provider binaries into the repository

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The dependency lock file records the exact provider versions and checksums chosen, so everyone who runs `init` gets the same ones; upgrades happen on purpose with `init -upgrade` and are reviewed in the diff. Deleting `.terraform` makes versions drift further. Removing `required_providers` loosens constraints and makes things worse. Committing binaries is heavy and platform-specific.
</details>

---

### Question 23
**Scenario:** An application configuration needs the VPC ID and subnet IDs produced by a separate network configuration managed by another team in HCP Terraform.

A. Copy the IDs into the application configuration by hand after each network change
B. Give the application workspace write access to the network workspace's state so it can edit it if needed
C. Read the network workspace's outputs with the `tfe_outputs` data source, or use provider data sources
D. Merge both configurations into one root module

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Reading the producing workspace's outputs, with `tfe_outputs` in HCP Terraform or `terraform_remote_state`, or querying the cloud provider with data sources shares the values without hard-coding them. Hand-copied IDs go stale. Read access to outputs is all that is needed, and write access breaks the ownership boundary. Merging configurations removes the team boundary and grows the blast radius.
</details>

---

### Question 24
**Scenario:** The same configuration is deployed to several environments, each with its own state bucket and key, and the backend block cannot use variables.

A. Leave those settings out of the backend block and pass them with `terraform init -backend-config=<file>`
B. Reference `var.environment` inside the backend block so the bucket name is chosen at runtime
C. Use one shared state file for every environment and separate resources with name prefixes
D. Hard-code the production bucket in the backend block and switch environments by editing the file

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Partial backend configuration leaves environment-specific settings out of the block and supplies them at `init` time from a file or flags, which is the supported way to vary backends. Backend blocks cannot reference variables. A single state for every environment couples them and widens the blast radius. Editing the file per run is error-prone and risky.
</details>

---

### Question 25
**Scenario:** A root module uses a public registry module at version 2.1.0. The team wants bug fixes in later 2.1.x versions but no new minor or major versions.

A. `version = ">= 2.1.0"`
B. Omit the version argument so Terraform installs the latest compatible release
C. `version = "2.1.0"` with `terraform init -upgrade`, which still pulls the newest patch release
D. `version = "~> 2.1.0"`

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** `~> 2.1.0` allows only the rightmost part to increase, so 2.1.x is accepted and 2.2.0 is not. `>= 2.1.0` accepts any newer version, including breaking majors. Omitting the version takes the latest release whatever it is. An exact `2.1.0` stays at that version even with `-upgrade`, so bug fixes never arrive.
</details>

---

### Question 26
**Scenario:** A shared module is consumed by many root modules that deploy to different regions and accounts. Where should the provider configuration live?

A. In the module, with a `provider "aws"` block that hard-codes the region used by most teams
B. In the root modules, with the module declaring only `required_providers`, and aliased providers passed in through `providers`
C. In a separate module that every other module calls to get its provider settings
D. In environment variables only, with no `required_providers` anywhere

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Reusable modules should declare which providers and versions they need in `required_providers` and let the caller configure them, passing aliased providers with the `providers` argument when needed. A provider block inside a module ties every caller to its settings and makes the module hard to remove safely. Modules cannot hand provider configurations to sibling modules that way. Without `required_providers`, the source and version are unclear and may resolve wrongly.
</details>

---

### Question 27
**Scenario:** One configuration must create a bucket in `us-east-1` and its replica in `eu-west-1` with the same provider.

A. Run the configuration twice with a different `AWS_REGION` environment variable each time
B. Create two separate state files and apply one region at a time from two directories
C. Declare a second provider block with an `alias` and set `provider = aws.eu` on the replica
D. Set `region` on each bucket resource instead of on the provider

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** An aliased provider block gives a second configuration of the same provider, and resources select it with the `provider` meta-argument, so both regions are managed in one plan. Running twice with different environment variables would manage only one bucket per run and conflict over state. Splitting into two configurations is possible but does not match "one configuration" and loses the direct reference. Resources choose a provider configuration; for most resources the region is a provider-level setting.
</details>

---

### Question 28
**Scenario:** A plan fails with a vague authentication error from a provider, and the team needs to see the API calls and credential sources the provider is trying.

A. Set `TF_LOG=DEBUG` (or `TF_LOG_PROVIDER`) and optionally `TF_LOG_PATH`, then run the plan again
B. Run `terraform fmt -recursive` to fix the configuration's formatting before planning again
C. Delete the state file and run the plan again so the provider re-authenticates from scratch
D. Downgrade Terraform itself to the oldest release that the provider still supports, then run the same plan again

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** `TF_LOG` turns on detailed logging, `TF_LOG_PROVIDER` focuses on provider plugins, and `TF_LOG_PATH` writes the log to a file, showing the requests and credential chain the provider uses. `fmt` only rewrites layout. Deleting state loses tracking of real resources and has nothing to do with authentication. Downgrading Terraform is guesswork and rarely the cause of a credential error.
</details>

---

### Question 29
**Scenario:** A VCS-connected HCP Terraform workspace should show reviewers the plan for every pull request, without anyone being able to apply from the pull request.

A. Give reviewers permission to run `terraform apply` locally against the workspace's state
B. Turn on auto-apply on the workspace so each pull request is applied to production as soon as a reviewer approves it
C. Use the CLI-driven workflow and ask authors to paste plan output into the pull request
D. Rely on speculative plans, which HCP Terraform runs for pull requests and reports as status checks

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** With the VCS-driven workflow, HCP Terraform runs a plan-only speculative run for each pull request and posts the result as a status check; it can never be applied. Local applies bypass the workspace's controls. Auto-apply applies after merges to the tracked branch, not on pull requests, and is the opposite of plan-only. Pasted output can be edited or stale.
</details>

---

### Question 30
**Scenario:** HCP Terraform workspaces currently hold long-lived cloud access keys as sensitive variables. Security wants them removed.

A. Move the keys into the Terraform configuration as variable defaults marked `sensitive`
B. Configure dynamic provider credentials, so each run gets short-lived credentials through workload identity (OIDC)
C. Rotate the long-lived keys every 90 days and keep storing them as workspace variables
D. Store the keys in a public repository's secrets

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Dynamic provider credentials let HCP Terraform present a signed workload identity token that the cloud provider trusts, and each run receives short-lived credentials, so no static keys are stored. Defaults in code put secrets in version control. Rotation shortens exposure but keeps long-lived keys in place. Secrets in another repository are still static keys, and they cannot be used by HCP Terraform anyway.
</details>

---

## Where to go deeper

- [Terraform Professional cert page](../../exams/hashicorp/terraform-authoring-operations-pro/) - notes, practice plan, strategy
- [Terraform Associate practice questions](./hashicorp-terraform-associate.md) - the prerequisite level
- [Packer Associate practice questions](./hashicorp-packer.md) - the image half of the workflow
- [Terraform explained](../../learn/concepts/terraform-explained.md) - IaC in plain English
- **[📖 Terraform documentation](https://developer.hashicorp.com/terraform/docs)** - primary source
