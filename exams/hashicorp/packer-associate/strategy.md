# Packer - Common Traps

> **This is a self-directed study track, not a certification guide.** HashiCorp's [certifications page](https://developer.hashicorp.com/certifications) (checked 2026-11-21) lists no Packer exam, only Terraform and Vault exams. Earlier versions of this guide quoted a cost, question count, passing score and domain weights for a "Packer Associate" exam; none of those had a vendor source, so they are removed. The notes, scenarios and labs still teach Packer as it is used in practice.

The mistakes people make most often with Packer, and how to tell the options apart.

## Common Trap Patterns

### Wrong Block Names
HCL2 uses `source` and `build`. Legacy JSON uses `builders` and `provisioners`. If a question shows `"builders": [...]`, it is either a legacy template or a trap. Check for `.json` vs `.pkr.hcl`.

### Plugin Source Syntax
Modern plugin blocks use `source = "github.com/hashicorp/amazon"`. Legacy short names (`type = "amazon-ebs"`) still work inside `source` blocks but not in `required_plugins`. Watch for the context.

### Variable Precedence
From highest to lowest:
1. `-var 'foo=bar'` on CLI
2. `-var-file=X.pkrvars.hcl` on CLI
3. `*.auto.pkrvars.hcl` in working directory
4. `PKR_VAR_foo` env var
5. Default in variable block

If two sources set the same variable, the higher one wins.

### only vs except
- `-only=amazon-ebs.ubuntu` runs only that source
- `-except=amazon-ebs.dev` runs everything else
Both target the source address `builder-type.source-name`.

### Builder Selection
- `amazon-ebs`: most common, builds AMI from a running EC2 instance
- `amazon-chroot`: builds AMI in-place using an existing instance (faster, advanced)
- `amazon-ebssurrogate`: builds from a detached root volume
- `amazon-instance`: for instance-store AMIs (rare)

Questions asking "build an AMI without launching a new instance" point to `amazon-chroot`.

### shell vs shell-local
- `shell`: runs on the builder instance
- `shell-local`: runs on the machine running Packer itself

A question asking "download a file to the Packer host before uploading it" points to `shell-local` followed by `file`.

### file Provisioner Direction
By default `file` uploads from local to remote. Set `direction = "download"` to pull from remote. Easy to confuse under time pressure.

### null Builder
Produces no image. Used for provisioner-only flows (e.g., run Ansible against an existing host). If the question describes "run provisioners without producing an artifact", answer is `null`.

### breakpoint Provisioner
Pauses the build for SSH debugging. Only active when `PACKER_LOG` debugging is enabled. Remove before production pipelines.

### HCP Packer Channels
A channel is a named pointer to an iteration (like a git branch pointing to a commit). Promoting = reassigning the pointer. Consumers reference channels, not iteration IDs directly.

## Syntax Traps

**required_plugins goes inside a packer block**
```hcl
packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1.3"
    }
  }
}
```

**sources are referenced by type.name in builds**
```hcl
build {
  sources = ["source.amazon-ebs.ubuntu"]
}
```

**Variables reference as var.X, locals as local.Y**
Don't confuse with Terraform conventions (same here actually, but watch for subtle differences).

**Functions that look similar**
- `timestamp()` returns RFC 3339
- `formatdate(format, timestamp)` formats it
- `file(path)` reads a file
- `fileset(path, pattern)` lists files matching glob

