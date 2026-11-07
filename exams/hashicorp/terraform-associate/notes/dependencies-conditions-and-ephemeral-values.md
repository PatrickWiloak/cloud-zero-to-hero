---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 20 min
---

# Dependencies, Custom Conditions and Ephemeral Values (objectives 4f, 4g, 4h)

## Overview

These three topics were added to the Terraform Associate exam in version 004. HashiCorp's 004 content list names them as new: **4f** defining resource dependencies (including `depends_on` and the `create_before_destroy` lifecycle rule), **4g** validating configuration with custom conditions, and **4h** ephemeral values and write-only arguments, within best practices for sensitive data. The exam tests Terraform 1.12, so the features below are all available in that version.

**[📖 Associate exam content list (004)](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004)** - HashiCorp's mapping of each objective to documentation

## 4f: Resource dependencies

Terraform builds a dependency graph. Most dependencies are **implicit**: when one resource refers to another's attribute (`aws_instance.web.id`), Terraform knows the referenced resource must exist first and orders the work accordingly, and creates in parallel anything the graph shows to be independent.

An **explicit** dependency is needed only for hidden relationships. HashiCorp's `depends_on` reference says to use it "to handle hidden resource or module dependencies that Terraform cannot automatically infer": the resource relies on another resource's behavior but does not read any of its data. A typical case is an application that needs an IAM policy to be attached before it starts, even though the application never references the policy.

```hcl
resource "aws_iam_role_policy" "app" {
  role   = aws_iam_role.app.id
  policy = data.aws_iam_policy_document.app.json
}

resource "aws_instance" "app" {
  ami                  = data.aws_ami.al2023.id
  instance_type        = "t3.micro"
  iam_instance_profile = aws_iam_instance_profile.app.name

  # The instance's software calls AWS APIs at boot and needs the policy attached.
  depends_on = [aws_iam_role_policy.app]
}
```

`depends_on` works on any resource block and on module blocks. Use it sparingly: it makes Terraform treat the dependency conservatively, which can produce more changes in a plan than a precise reference would.

**[📖 depends_on meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on)** - When explicit dependencies are needed

### The create_before_destroy lifecycle rule

By default, when an argument cannot be updated in place, Terraform **destroys** the existing object and then **creates** the replacement. The `create_before_destroy` rule reverses that order, so the new object exists before the old one is removed. It is opt-in because many remote objects have unique-name or other constraints that prevent two from existing at once.

```hcl
resource "aws_launch_template" "web" {
  name_prefix   = "web-"      # a prefix avoids a name collision during replacement
  image_id      = var.image_id
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true
  }
}
```

Two exam-relevant details from the lifecycle documentation: Terraform propagates `create_before_destroy` to resources that the protected resource depends on (it enables the behavior implicitly for dependencies, and you cannot set it to `false` on those because that would create a dependency cycle); and a destroy-time provisioner will not run on a resource with `create_before_destroy = true`.

The other `lifecycle` arguments remain in scope for the same objective family: `prevent_destroy = true` makes Terraform reject any plan that would destroy the object (but it does not stop destruction if you simply remove the resource from configuration), and `ignore_changes` lists attributes Terraform should ignore when planning updates.

**[📖 lifecycle meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)** - create_before_destroy, prevent_destroy, ignore_changes and conditions

## 4g: Custom conditions

HashiCorp's validation guide lists four mechanisms. Know which runs when, and whether it blocks.

| Mechanism | Where it goes | Evaluated | Failure blocks the run? |
|-----------|---------------|-----------|------------------------|
| **Input variable validation** | `validation` block inside a `variable` | Immediately, before a plan is generated | Yes |
| **Precondition** | `lifecycle` block of a resource or data source, or inside an `output` | After the plan is generated, before the object is created | Yes |
| **Postcondition** | `lifecycle` block of a resource or data source | After planning and applying changes, or after the data source is read | Yes |
| **Check block** | Top-level `check` block | As the last step of a plan or apply (continuous validation also runs in HCP Terraform) | No, it reports a warning |

Version requirements stated in the guide: input variable validation needs Terraform 0.13 or later, preconditions and postconditions need 1.2 or later, and `check` blocks need 1.5 or later. All are available in 1.12.

```hcl
variable "image_id" {
  type        = string
  description = "The id of the machine image (AMI) to use for the server."

  validation {
    condition     = length(var.image_id) > 4 && substr(var.image_id, 0, 4) == "ami-"
    error_message = "The image_id value must be a valid AMI id, starting with \"ami-\"."
  }
}

resource "aws_instance" "example" {
  instance_type = "t3.micro"
  ami           = data.aws_ami.example.id

  lifecycle {
    precondition {
      condition     = data.aws_ami.example.architecture == "x86_64"
      error_message = "The selected AMI must be for the x86_64 architecture."
    }
  }
}

data "aws_ami" "example" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["myami-*"]
  }

  lifecycle {
    postcondition {
      condition     = self.tags["Component"] == "nomad-server"
      error_message = "tags[\"Component\"] must be \"nomad-server\"."
    }
  }
}
```

A precondition states an assumption about inputs ("this AMI must be x86_64"). A postcondition states a guarantee about results ("what came back must have this tag"), and inside it the object is referred to as `self`. Preconditions take precedence over argument errors raised by providers, which gives the user a clearer message.

**[📖 Validate your configuration](https://developer.hashicorp.com/terraform/language/expressions/custom-conditions)** - Variable validation, preconditions, postconditions and checks

## 4h: Sensitive data, ephemeral values and write-only arguments

The long-standing rule: **sensitive values still end up in state**. Marking a variable `sensitive = true` hides it from CLI output, but the value is written to the state file in plain text, which is why state must be stored in an access-controlled, encrypted backend. The 004 objective adds the newer tools that keep values out of state entirely.

HashiCorp's documentation describes two:

1. **Ephemeral resources**, declared with an `ephemeral` block. They are temporary: "Terraform does not store information about ephemeral resources in state or plan files." Examples are a generated password or a connection to a secrets system. Terraform opens the ephemeral resource when it needs the result, renews it if needed, and closes it after dependent providers finish. You refer to one as `ephemeral.<TYPE>.<LABEL>`, and only in permitted contexts (another ephemeral block, a `variable` or child-module `output` with `ephemeral = true`, and write-only arguments).
2. **Write-only arguments** on managed resources. These arguments are available only during the current operation and are not stored in state or plan files. By convention the provider's argument carries a `_wo` suffix, with a companion `_wo_version` argument you increment to tell Terraform the value changed (Terraform cannot compare a value it never stored).

```hcl
ephemeral "random_password" "db_password" {
  length           = 16
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_db_instance" "example" {
  instance_class      = "db.t3.micro"
  allocated_storage   = "5"
  engine              = "postgres"
  username            = "example"
  skip_final_snapshot = true

  password_wo         = ephemeral.random_password.db_password.result
  password_wo_version = 1
}
```

Per the documentation, Terraform sends the `password_wo` value to the AWS provider, which uses it to create the database, and Terraform then discards the value without ever storing it. Changing the password later means changing the secret and bumping `password_wo_version`.

The best-practice summary for 4h: do not hard-code secrets in configuration or commit them to version control; mark input variables sensitive; read secrets at run time from a secrets manager such as **HashiCorp Vault** through the Vault provider; prefer ephemeral resources and write-only arguments so the secret never reaches state; and protect whatever state still exists with an encrypted remote backend and tight access.

**[📖 Ephemeral values in resources](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/ephemeral)** - Ephemeral resources and write-only arguments
**[📖 ephemeral block reference](https://developer.hashicorp.com/terraform/language/block/ephemeral)** - Lifecycle and where ephemeral values may be referenced

## Common exam traps

- A precondition checks inputs before creation; a postcondition checks results afterwards and uses `self`.
- A `check` block never blocks the run; variable validation, preconditions and postconditions do.
- `sensitive = true` hides output, it does not keep a value out of state. Ephemeral resources and write-only arguments do.
- `create_before_destroy` flips the default replace order and spreads to the resource's dependencies.
- Use `depends_on` only for dependencies Terraform cannot see from references.

## Key terms

- **Implicit dependency** - an ordering Terraform infers from one resource referring to another's attributes.
- **depends_on** - a meta-argument that declares a dependency Terraform cannot infer from references.
- **create_before_destroy** - a lifecycle rule that creates the replacement object before destroying the old one.
- **prevent_destroy** - a lifecycle rule that makes Terraform reject any plan that would destroy the resource.
- **Precondition** - a custom condition checked during planning that must hold before a resource, data source or output is created.
- **Postcondition** - a custom condition checked after a resource or data source is applied or read, referring to the object as self.
- **Check block** - a top-level block that validates infrastructure without blocking the run, reporting failures as warnings.
- **Variable validation** - a validation block on an input variable that rejects values failing its condition.
- **Ephemeral resource** - a temporary resource declared with an ephemeral block whose data is never stored in state or plan files.
- **Write-only argument** - a resource argument whose value is used during the current operation and never stored in state or plan files.
