---
last-updated: 2026-10-22
difficulty: intermediate
---

# HashiCorp Packer - Practice Questions

30 questions for Packer practice across templates, builders, provisioners, post-processors, variables, and HCP Packer.

> **Study track:** [exams/hashicorp/packer/](../../exams/hashicorp/packer/)

---

### Question 1
**Scenario:** What does Packer produce?

A. Machine images (AMIs, VM images, container images) built from a template
B. Kubernetes manifests that describe how the built images should be deployed and scaled in a cluster
C. Terraform state files that record which cloud resources exist and which module created each of them
D. Running infrastructure such as VPCs, load balancers, and instances provisioned directly from the template

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Packer builds artifacts; Terraform provisions infrastructure from them. Keeping that split clear is the point of the immutable infrastructure workflow: bake the image once, then deploy it many times without configuring machines after launch.
</details>

---

### Question 2
**Scenario:** A single template must produce an AWS AMI and an Azure image from the same configuration.

A. Two separate templates, one per cloud, kept in sync by copying changes between them
B. One build block with multiple sources, so each image is produced in parallel from the same provisioners
C. It is not supported, because each template can define only one source and one builder per file
D. Run Packer twice manually with different template files, then compare the results by hand

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A build block can reference several sources, and Packer runs them concurrently through the same provisioning steps. This is what keeps multi-cloud golden images genuinely identical rather than approximately similar.
</details>

---

### Question 3
**Scenario:** Software must be installed into the image during the build.

A. A variable block, which stores the package name and version so the installer can look it up later
B. A post-processor, which runs after the build to install the software into the finished image
C. A provisioner block, such as shell, file, Ansible, or PowerShell
D. A source block, which defines the base image and the builder that starts the temporary instance

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Provisioners run inside the temporary build instance. Post-processors act on the resulting artifact, for example tagging, compressing, or uploading it. Source blocks define what to start from and where to build.
</details>

---

### Question 4
**Scenario:** Which HCL block defines the plugins a template requires?

A. `source`, which names the builder plugin and its settings for one image target, such as an AMI
B. `build`, which lists the sources and the provisioners that run on them
C. `locals`, which holds computed values that are reused elsewhere in the template, like names and tags
D. `packer { required_plugins { ... } }`, with a version constraint per plugin

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Since plugins were split out of the core binary, templates declare what they need with version constraints, and `packer init` installs them. Forgetting this block is the most common first error when moving a template from an older Packer version.
</details>

---

### Question 5
**Scenario:** A secret must be passed into a build without appearing in the template.

A. A comment next to the variable that says the value is secret, so reviewers know not to commit it
B. Hard-code it in the template and restrict who has read access to the repository
C. A sensitive variable supplied from the environment, a var file kept out of git, or Vault
D. A local value in a `locals` block, since locals are never printed in build output

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Marking a variable `sensitive = true` keeps it out of Packer's log output, and sourcing it from the environment or Vault keeps it out of the repository. Anything written into the template is in git history forever.
</details>

---

### Question 6
**Scenario:** Build credentials should not be baked into the image.

A. Remove build-time credentials, SSH keys, and shell history in a final provisioner, and verify the image
B. Encrypt the image only, since an encrypted snapshot hides any credentials stored on its disk from launchers and from the account owner
C. Ignore it, because the cloud provider scrubs credentials from every image as part of registering the AMI in a region
D. They are removed automatically when Packer terminates the temporary instance

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Anything present on disk at snapshot time ships in the image and to everyone who launches it. Cloud-init and sysprep handle some of this, but build artifacts such as temporary keys, package caches, and shell history need explicit removal.
</details>

---

### Question 7
**Scenario:** The same image must be validated before it is published.

A. Nothing is available in Packer, so validation has to wait until instances are launched from the image in production
B. Log in manually to a production instance launched from the published image and check the installed software by eye
C. Only `packer build`, since a successful build already proves the image contents are correct
D. `packer validate` for syntax, plus a test provisioner or a tool such as InSpec or Goss to verify the image

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** `validate` catches template errors before spending build time, but it says nothing about whether the software actually installed. Running a compliance or smoke test as the last provisioner is what turns "the build succeeded" into "the image is correct."
</details>

---

### Question 8
**Scenario:** Build output should be tagged and registered so downstream Terraform can find it.

A. Use `latest` tags on every image so that downstream Terraform always picks up the newest build automatically
B. Copy the ID by hand from the build output into the Terraform variables file after each build
C. A manifest post-processor writing artifact IDs, or HCP Packer registry with channels
D. Hard-code the AMI ID in Terraform and update it by hand

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** HCP Packer tracks image versions and channels, and Terraform's HCP Packer data source resolves a channel such as `production` to a concrete image ID. Hard-coded IDs are how estates end up running images nobody can rebuild.
</details>

---

### Question 9
**Scenario:** A build fails halfway and leaves a running instance.

A. It always cleans up, so a failed build never leaves instances, keys, or security groups behind in the account
B. Nothing can be done; the instance is locked by Packer and can only be removed by cloud provider support
C. Packer normally cleans up on failure; use `-on-error=abort` or `ask` to keep the instance
D. Terminate the whole account and recreate it, which is the only way to remove resources Packer left behind

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The default cleanup is what keeps builds from leaking resources, but it also destroys the evidence. `-on-error=ask` pauses so you can SSH in and see what the provisioner actually hit, which is the fastest way to debug a failing step.
</details>

---

### Question 10
**Scenario:** Multiple similar images differ only in a version number.

A. Use input variables and locals, with `-var` or a `.pkrvars.hcl` file per variant
B. Use separate repositories, one per version
C. Duplicate the template for each variant and change the version
D. Edit the template each time and commit the change, keeping history in git to recover older versions

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Parameterization keeps one template as the source of truth. Duplicated templates drift, and the drift is usually discovered when one variant fails to build months later for a reason the other one already fixed.
</details>

---

### Question 11
**Scenario:** What is the benefit of immutable infrastructure built with Packer?

A. Servers are replaced rather than modified, so drift is eliminated and rollback means redeploying an earlier image
B. No monitoring is needed, because a validated image cannot fail in production
C. Faster networking, because baked images use a dedicated network path
D. Cheaper storage, since immutable images are deduplicated and cost nothing to keep for any length of time or number of versions

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Configuration drift is the thing that makes long-lived servers unreproducible, and replacing rather than patching removes the cause. Rollback also becomes trivial, because the previous image still exists and is known good.
</details>

---

### Question 12
**Scenario:** Build times are long because every build installs the full base software stack.

A. Accept it, because installing the full stack on each build is the only way to keep the image consistent
B. Layer it: build a base image, then build application images from it so common steps run once
C. Remove provisioners and install the software by hand after launch
D. Use a larger instance type only, since build time falls with vCPU count

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A base image rebuilt weekly plus thin application images built on every commit gives fast application builds and a controlled patching cadence for the shared layer. It is the same reasoning as container base images.
</details>

---

### Question 13
**Scenario:** A shell provisioner needs to run as root.

A. Change the source image to one that boots as root, since Packer cannot raise privileges after the build starts
B. `execute_command` with sudo, or the `elevated_user` settings on Windows
C. It cannot be done, because provisioners always run as the unprivileged SSH user that Packer logs in with
D. Run Packer as root locally, so the provisioner inherits the privileges of the workstation shell

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Privilege applies inside the build instance, not on the workstation running Packer. The `execute_command` setting controls how the script is invoked there, and on Windows the elevated user settings serve the same purpose for tasks needing full privileges.
</details>

---

### Question 14
**Scenario:** Golden images must be patched on a regular cadence.

A. Rebuild only when something breaks, so the image changes stay small and every rebuild has a clear cause
B. Ignore patching, because the cloud provider updates the guest operating system on running instances
C. Patch running servers instead, logging in to each one and applying updates in place on a schedule
D. Rebuild images on a schedule in CI, run validation, publish to a channel, and roll instances onto the new version

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** In an immutable model the pipeline is the patching mechanism, which means the rebuild has to be automated and routine or the estate falls behind. Publishing to a channel decouples building the image from adopting it.
</details>

---

### Question 15
**Scenario:** Packer and Terraform in the same workflow.

A. They are alternatives, so a team picks one tool for the whole workflow and never runs them together
B. Packer builds the image, Terraform provisions infrastructure that uses it, passing the ID by data source or variable
C. Packer deploys infrastructure by launching the built images into subnets, load balancers, and scaling groups
D. Terraform builds images by running its own provisioners inside a temporary instance and saving a snapshot

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The separation keeps each tool doing what it is good at: Packer produces an artifact, Terraform manages the lifecycle of resources referencing it. Terraform provisioners exist but are documented as a last resort precisely because baking is the better answer.
</details>

---

### Question 16
**Scenario:** A developer clones a repository with a working Packer template and runs `packer build .` on a fresh laptop. It fails because the `amazon-ebs` source type is unknown. The template has a `required_plugins` block. What should they run first?

A. `packer fmt .`, which also installs any plugins the template is missing
B. `packer init .`, which installs the plugins listed in `required_plugins`
C. `packer validate .`, which downloads plugins as part of its syntax checks
D. `packer build -force .`, which forces Packer to fetch the missing builders

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** `packer init` reads `required_plugins` and installs matching plugin versions, which recent Packer releases need because most plugins are no longer bundled with the binary. `fmt` only rewrites formatting. `validate` checks configuration but does not install plugins. `-force` overwrites existing artifacts and has nothing to do with plugins.

**Key Concept:** Declare plugins in `required_plugins`, then run `packer init` before building. See [packer init](https://developer.hashicorp.com/packer/docs/commands/init).
</details>

---

### Question 17
**Scenario:** A CI pipeline should reject a template change with a syntax error or missing required variable, without launching any cloud instances. Which command should the pipeline run?

A. `packer build -debug .`, stopping after the first step completes
B. `packer inspect .`, which runs each provisioner in dry-run mode
C. `packer console .`, which evaluates the whole template and exits
D. `packer validate .`, which checks syntax and configuration only

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** `packer validate` checks the template's syntax and configuration, including required variables, without creating resources, which makes it a cheap CI gate. `build -debug` still launches instances and pauses between steps. `inspect` lists variables, sources, and provisioners but does not validate a full build. `console` is an interactive expression evaluator, not a validation gate.

**Key Concept:** Gate CI with `packer fmt -check` and `packer validate` before any build. See [packer validate](https://developer.hashicorp.com/packer/docs/commands/validate).
</details>

---

### Question 18
**Scenario:** A template defines `source "amazon-ebs" "ubuntu" { ... }` and a `build` block with `sources = ["source.amazon-ebs.ubuntu"]`. What is the relationship between these blocks?

A. The source configures a builder once, and the build block uses it and adds provisioners
B. The build block replaces the source, so the settings in the source block are ignored
C. The source block runs the provisioners, and the build block only sets the image name
D. They are two separate builds that run in parallel and produce two separate images

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** A `source` block holds reusable builder configuration, and a `build` block references one or more sources and adds provisioners and post-processors to run on them. The build does not discard the source settings. Provisioners belong in the build block. Referencing one source from one build produces one image, not two.

**Key Concept:** Sources say where and how to build; builds say what to do with them. See [build block](https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build).
</details>

---

### Question 19
**Scenario:** An image needs an NGINX configuration file from the repository copied into it before a shell script enables the service. Which provisioner should copy the file?

A. A `shell-local` provisioner, which runs on the image during the build
B. A `breakpoint` provisioner, which uploads the file when the build pauses
C. A `file` provisioner, followed by a `shell` provisioner for the script
D. A `manifest` post-processor, which writes files into the finished image

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The `file` provisioner uploads files or directories to the machine being built, and a following `shell` provisioner can move and enable them. `shell-local` runs on the machine running Packer, not on the image. `breakpoint` pauses the build for debugging. The manifest post-processor writes build metadata to a local file after the build, and does not change the image.

**Key Concept:** Provisioners run in order; upload with `file`, configure with `shell` or a config management tool. See [File provisioner](https://developer.hashicorp.com/packer/docs/provisioners/file).
</details>

---

### Question 20
**Scenario:** A downstream script needs the AMI ID that each Packer build produced, in a machine-readable file, without parsing console output. What should be added to the template?

A. A `shell` provisioner that echoes the AMI ID into the image's root folder
B. A `manifest` post-processor that writes artifact IDs to a JSON file
C. A `breakpoint` provisioner that prints the AMI ID before the build ends
D. A `variable` block named `ami_id` that Packer fills in after the build

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The manifest post-processor writes a JSON file listing each build's artifacts, including their IDs, which scripts can read. A provisioner runs before the image exists, so it cannot know the final AMI ID, and writing it inside the image does not help a script outside it. A breakpoint pauses rather than exports. Input variables are inputs, not outputs filled in after a build.

**Key Concept:** Post-processors act on finished artifacts; the manifest records them. See [Manifest post-processor](https://developer.hashicorp.com/packer/docs/post-processors/manifest).
</details>

---

### Question 21
**Scenario:** One build block uses two sources, `amazon-ebs.web` and `azure-arm.web`. A Windows-specific provisioner must run only on the Azure image. How should it be limited?

A. Put the provisioner in a separate template and build the Azure image twice
B. Wrap the provisioner in a `dynamic` block that checks the cloud name
C. Add a `variable` named `cloud` and set it before each build by hand
D. Add `only = ["azure-arm.web"]` to that provisioner block

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Provisioners and post-processors accept `only` and `except` lists naming sources, so one build block can run source-specific steps. A separate template duplicates configuration and building twice wastes time. `dynamic` blocks generate nested blocks and are not a way to filter by source. A manual variable adds error-prone steps.

**Key Concept:** Use `only` and `except` to tailor steps per source. See [Only and except](https://developer.hashicorp.com/packer/docs/templates/hcl_templates/onlyexcept).
</details>

---

### Question 22
**Scenario:** The `region` variable has a default of `us-east-1`. A `prod.auto.pkrvars.hcl` file sets it to `us-west-2`, `PKR_VAR_region` is set to `eu-west-1`, and the build runs with `-var region=ap-south-1`. Which value is used?

A. `ap-south-1`, from the `-var` flag on the command line
B. `us-west-2`, from the `.auto.pkrvars.hcl` variable file
C. `eu-west-1`, from the `PKR_VAR_region` environment variable
D. `us-east-1`, from the default value set in the variable block

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Later sources override earlier ones: the default first, then `PKR_VAR_` environment variables, then `*.auto.pkrvars.hcl` files, then `-var` and `-var-file` options on the command line, which have the highest priority. So the `-var` value wins. The auto file beats the environment variable but loses to the command line. The default is used only when nothing else sets the value.

**Key Concept:** Command-line values override files, which override environment variables, which override defaults. See [Input variables](https://developer.hashicorp.com/packer/docs/templates/hcl_templates/variables).
</details>

---

### Question 23
**Scenario:** An engineer writes `variable "ami_name" { default = "web-${timestamp()}" }` and Packer rejects it. They want every image name to include the build time. What should they use instead?

A. A `PKR_VAR_ami_name` environment variable containing the text `timestamp()`
B. A `data` block that reads the system clock through the AWS provider
C. A `locals` block that builds the name with `timestamp()` or `formatdate()`
D. A post-processor that renames the image after the build has finished

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A variable's `default` must be a literal value, so it cannot call functions. Locals can use expressions and functions, so `local.ami_name` built with `formatdate` and `timestamp()` works and can be referenced in the source. An environment variable passes the literal text, not a call. There is no clock data source in the AWS plugin. Renaming afterwards is awkward and many clouds do not allow it.

**Key Concept:** Use variables for inputs and locals for computed values. See [Local values](https://developer.hashicorp.com/packer/docs/templates/hcl_templates/locals).
</details>

---

### Question 24
**Scenario:** A provisioner fails near the end of a 40 minute build, and Packer cleans up the instance before the engineer can see why. How can they keep the instance for inspection on the next run?

A. Run `packer build -force`, which skips cleanup when a provisioner fails
B. Run `packer validate -debug` to replay the build with full logging
C. Run `packer build -parallel-builds=0` so the instance stays running
D. Run `packer build -on-error=ask` and choose to leave the instance running

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** `-on-error=ask` pauses on failure and lets the engineer clean up, abort and keep the resources, or retry; `-on-error=abort` keeps them without asking. The default, `cleanup`, deletes them. `-force` overwrites existing artifacts. `validate` does not build anything. `-parallel-builds` controls concurrency, not cleanup.

**Key Concept:** Use `-on-error` and `PACKER_LOG=1` when debugging builds, and remember to delete kept resources. See [Debugging Packer](https://developer.hashicorp.com/packer/docs/debugging).
</details>

---

### Question 25
**Scenario:** Terraform modules should always deploy the image that the platform team has approved for production, without anyone pasting AMI IDs into code. The team uses HCP Packer. What connects the two?

A. A Terraform variable holding the latest AMI ID, updated by hand after each build
B. An HCP Packer channel the team assigns approved versions to, read by Terraform's HCP provider
C. A Packer `manifest` file committed to the Terraform repository after every build
D. The AWS console's AMI catalog, filtered by name in a Terraform data source

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** HCP Packer stores build metadata, and channels such as `production` point to an approved version. Terraform reads the channel through the HCP provider's artifact data source, so promotion is a channel change, not a code change. Hand-edited variables and committed manifests rely on people and lag behind. Name filters can pick up unapproved images.

**Key Concept:** Channels decouple image promotion from infrastructure code. See [HCP Packer channels](https://developer.hashicorp.com/hcp/docs/packer/manage/channel).
</details>

---

### Question 26
**Scenario:** A critical vulnerability is found in a base image version that is tracked in HCP Packer and used by several teams. What should the platform team do in HCP Packer?

A. Revoke the affected version so consumers checking its status stop using it
B. Delete the HCP Packer bucket so that no team can reference the image at all
C. Rename the version in HCP Packer so that teams cannot find it by its old name
D. Leave the registry unchanged and email each team asking them to stop using it

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Revoking a version marks it as unsafe, and builds or Terraform runs that check revocation can refuse it, while a patched version is assigned to channels. Deleting the bucket breaks every consumer, including those on safe versions. Renaming is not a security control. Email depends on every team noticing and acting.

**Key Concept:** Revocation spreads a "do not use" signal through the image supply chain. See [Revoke and restore versions](https://developer.hashicorp.com/hcp/docs/packer/manage/revoke-restore).
</details>

---

### Question 27
**Scenario:** A template builds images for AWS, Azure, and Google Cloud. On a small CI runner, running all three builds at once exhausts memory. What is the simplest fix?

A. Split the template into three files and run them on three separate CI runners
B. Add `sleep` provisioners so the builds start at staggered times on the runner
C. Remove two of the sources and build only one cloud's image on each release
D. Run `packer build -parallel-builds=1 .` so the builds run one at a time

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Packer runs builds in parallel by default, and `-parallel-builds` limits how many run at once, so a value of 1 runs them in sequence on the same runner. Splitting templates duplicates configuration. Sleep provisioners delay steps inside builds but builds still overlap. Dropping clouds removes required images.

**Key Concept:** Control build concurrency from the command line. See [packer build](https://developer.hashicorp.com/packer/docs/commands/build).
</details>

---

### Question 28
**Scenario:** A template contains AWS and Azure sources. A hotfix is needed for the AWS image only. How can the engineer build just that source without editing the template?

A. Comment out the Azure source in the file and remember to restore it later
B. Set `PKR_VAR_azure=false` so that Packer skips the Azure source this time
C. Run `packer build -only='amazon-ebs.*' .` to build only the AWS sources
D. Run `packer build -except='*' .` and then add the AWS source back manually

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The `-only` flag limits a run to matching sources, with glob patterns supported, so no file edits are needed. Commenting out code risks a broken commit. An environment variable does nothing unless the template uses it, and variables cannot remove sources. `-except='*'` excludes everything.

**Key Concept:** Filter builds at run time with `-only` and `-except`. See [packer build](https://developer.hashicorp.com/packer/docs/commands/build).
</details>

---

### Question 29
**Scenario:** A template passes a registry password through a variable, and the password shows up in CI logs when Packer prints the configuration. What change hides it from Packer's output?

A. Set `sensitive = true` on the variable so Packer masks its value
B. Rename the variable to `password` so Packer detects it as secret
C. Add the variable to a `.gitignore` file in the template repository
D. Move the variable's default value into a `locals` block instead

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Variables marked `sensitive = true` have their string values masked in Packer's output. Packer does not guess secrets from variable names. `.gitignore` keeps files out of Git but does not change log output. A local holding the secret is still printed and makes it easier to commit by accident.

**Key Concept:** Mark secrets sensitive and source them from a secret store or environment, never a default. See [Input variables](https://developer.hashicorp.com/packer/docs/templates/hcl_templates/variables).
</details>

---

### Question 30
**Scenario:** A template contains `access_key` and `secret_key` values for AWS so the CI job can build AMIs. Security wants no cloud credentials stored in the template or repository. What should the team do?

A. Move the keys into a `.auto.pkrvars.hcl` file committed next to the template
B. Remove them and let the builder use the CI role's temporary credentials from its environment
C. Encode the keys in base64 inside the template so they are no longer readable
D. Store the keys in the image itself so later builds can read them from there

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The Amazon builders use the standard AWS credential chain, so the CI runner's role or OIDC-issued temporary credentials can be picked up from the environment with no keys in code. A committed variable file is still stored credentials. Base64 is encoding, not encryption. Baking keys into an image leaks them to everyone who uses it.

**Key Concept:** Authenticate builds with short-lived, environment-supplied credentials. See [Amazon EBS builder](https://developer.hashicorp.com/packer/integrations/hashicorp/amazon/latest/components/builder/ebs).
</details>

---

## Where to go deeper

- [Packer Associate cert page](../../exams/hashicorp/packer/) - notes, practice plan, strategy
- [Terraform Associate practice questions](./hashicorp-terraform-associate.md) - the deployment half of the workflow
- [Terraform explained](../../learn/concepts/terraform-explained.md) - IaC in plain English
- **[📖 Packer documentation](https://developer.hashicorp.com/packer/docs)** - primary source
