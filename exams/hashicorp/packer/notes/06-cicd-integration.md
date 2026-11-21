# CI/CD Integration and Security

Running Packer manually from a laptop works for labs. Running in production requires CI/CD pipelines, credential management, and observability. Expect exam questions on these areas.

## The Pipeline Anatomy

A solid Packer pipeline has:

1. **Lint and validate:** `packer fmt -check`, `packer validate`
2. **Build:** `packer init && packer build`
3. **Test:** smoke tests against the resulting artifact
4. **Publish:** to HCP Packer or a registry
5. **Promote:** via channel change after tests pass
6. **Notify:** success or failure to Slack/Teams

## GitHub Actions Example

```yaml
name: Build AMI
on:
  push:
    branches: [main]
  pull_request:
    paths: ['packer/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-packer@main
        with:
          version: 1.11.2
      - run: packer fmt -check -recursive packer/
      - run: packer init packer/
      - run: packer validate packer/

  build:
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      id-token: write    # OIDC to AWS
      contents: read
    env:
      HCP_CLIENT_ID: ${{ secrets.HCP_CLIENT_ID }}
      HCP_CLIENT_SECRET: ${{ secrets.HCP_CLIENT_SECRET }}
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/packer-builder
          aws-region: us-east-1
      - uses: hashicorp/setup-packer@main
      - run: packer init packer/
      - run: packer build packer/
```

Key patterns:

- OIDC for AWS auth (no static keys)
- HCP Packer credentials as GitHub Actions secrets
- Separate validate and build jobs
- PRs trigger validate only; merges trigger build

## GitLab CI Example

```yaml
stages: [validate, build]

variables:
  PACKER_LOG: 1

validate:
  stage: validate
  image: hashicorp/packer:1.11.2
  script:
    - packer fmt -check -recursive packer/
    - packer init packer/
    - packer validate packer/

build:
  stage: build
  image: hashicorp/packer:1.11.2
  only: [main]
  script:
    - packer init packer/
    - packer build packer/
```

For AWS, use GitLab's AWS OIDC integration or IAM keys from a dedicated runner.

## Jenkins Pipeline

```groovy
pipeline {
  agent { label 'packer' }
  environment {
    HCP_CLIENT_ID     = credentials('hcp-client-id')
    HCP_CLIENT_SECRET = credentials('hcp-client-secret')
  }
  stages {
    stage('Validate') {
      steps {
        sh 'packer fmt -check -recursive .'
        sh 'packer init .'
        sh 'packer validate .'
      }
    }
    stage('Build') {
      when { branch 'main' }
      steps {
        withAWS(role: 'packer-builder', region: 'us-east-1') {
          sh 'packer build .'
        }
      }
    }
  }
}
```

## Credential Management

**Never hardcode credentials.** Options in preference order:

1. **OIDC / workload identity:** short-lived, no secrets on disk
2. **IAM roles on the build host:** if CI runs on EC2, use instance profile
3. **Secret manager integration:** Vault, AWS Secrets Manager, GitHub Secrets
4. **Environment variables from CI secrets:** last resort for on-prem

Specifically for Packer:

- AWS: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` or use profile
- Azure: service principal env vars or `az login` with managed identity
- GCP: `GOOGLE_APPLICATION_CREDENTIALS` pointing to JSON, or workload identity
- HCP Packer: `HCP_CLIENT_ID`, `HCP_CLIENT_SECRET`

## Vault Integration

For truly secure credential handling, pull from Vault at build time:

```hcl
data "vault" "aws_creds" {
  path = "aws/creds/packer-builder"
}

source "amazon-ebs" "ubuntu" {
  access_key = data.vault.aws_creds.access_key
  secret_key = data.vault.aws_creds.secret_key
  # ...
}
```

Vault generates short-lived AWS credentials on demand. Combine with a Vault auth method appropriate for CI (AppRole, JWT, or cloud-specific).

## Sensitive Variable Handling

Mark variables `sensitive = true` to redact from logs. Still, treat logs as public: do not `echo $SECRET` in shell provisioners.

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

provisioner "shell" {
  environment_vars = ["DB_PASS=${var.db_password}"]
  inline = [
    # use $DB_PASS in a script that does not echo it
    "echo 'secret available to script as DB_PASS'",
  ]
}
```

## Image Signing and Provenance

- Use the `checksum` post-processor to generate SHA256s for portable artifacts
- Use HCP Packer for chain-of-custody metadata
- For container images, use `cosign` or Docker Content Trust after `docker-push`
- Sign the Git commit that triggered the build for end-to-end provenance

## Secret-Free Image Capture

Ensure no secrets end up in the captured image:

- Clean up `/tmp` and bash history before capture
- Remove SSH host keys; cloud-init will regenerate
- Scrub log files: `sudo shred -u /var/log/auth.log`
- If using API keys during build, unset them and remove any files they were in

```hcl
provisioner "shell" {
  inline = [
    "sudo rm -f /tmp/*.key /tmp/*.pem",
    "rm -f ~/.bash_history",
    "sudo find /var/log -type f -exec truncate -s 0 {} +",
  ]
}
```

## Smoke Testing Images

After build, verify the image works:

- **Terratest (Go):** launch an EC2 from the new AMI, assert it reaches health check
- **InSpec:** connect and run compliance profiles
- **Custom scripts:** `aws ec2 run-instances`, curl the app port, `terminate-instances`

Integrate as a CI stage after build, before HCP Packer promotion.

## Channel Promotion Gate

Never auto-promote to `production`. Typical flow:

1. Build completes; iteration registered in HCP Packer
2. Auto-promote to `development` channel
3. Smoke tests run against `development`
4. Manual approval (GitHub environment, Jenkins input step, HCP API call) promotes to `staging`
5. Soak tests run against `staging`
6. Another manual approval promotes to `production`

```
curl -X PATCH https://api.cloud.hashicorp.com/packer/2023-01-01/... \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"iteration_id":"...", "channel_name":"production"}'
```

## Observability

Log key events:

- Build start and end timestamps (diff for duration tracking)
- AMI IDs (for post-build cleanup)
- HCP iteration IDs (for promotion tracking)
- Cost (EC2 builder usage)

Push metrics to Datadog, CloudWatch, or Prometheus. Alert on:

- Build duration exceeding threshold
- Repeated failures of a specific template
- Channels pointing to old iterations (staleness)

## Multi-Template Monorepos

A common layout:

```
packer/
├── ubuntu-base/
│   ├── source.pkr.hcl
│   ├── build.pkr.hcl
│   └── variables.pkr.hcl
├── amazon-linux-base/
│   └── ...
├── windows-base/
│   └── ...
└── common/
    └── scripts/
        └── harden.sh
```

Each template directory is self-contained. CI detects which templates changed and rebuilds selectively.

```yaml
- uses: dorny/paths-filter@v3
  id: filter
  with:
    filters: |
      ubuntu: packer/ubuntu-base/**
      windows: packer/windows-base/**

- if: steps.filter.outputs.ubuntu == 'true'
  run: packer build packer/ubuntu-base/
```

## Common CI/CD Mistakes

- Running Packer locally then pushing only the template to Git (untested, non-reproducible)
- Using a shared IAM user across pipelines (blast radius)
- Committing `manifest.json` to git (it should be a build artifact)
- Not tagging builder instances with the run ID (makes cleanup hard)
- Skipping `packer init` in CI (pipeline fails on first plugin use)
- Allowing parallel builds to share temporary resources (races, collisions)

## Security Hardening Summary

1. Use OIDC or Vault, never static keys
2. Scope IAM roles to minimum permissions (EC2 instance launch, AMI registration, tag, snapshot)
3. Run Packer in an isolated account or subscription
4. Enable CloudTrail (AWS) / Activity Log (Azure) on the build account
5. Rotate HCP service principal credentials quarterly
6. Pin plugin versions in `required_plugins`
7. Pin Packer CLI version in CI
8. Review and lint templates on every PR

## Exam-Ready Checklist

- [ ] Can configure a GitHub Actions pipeline with OIDC to AWS
- [ ] Know `HCP_CLIENT_ID`, `HCP_CLIENT_SECRET` for HCP Packer auth
- [ ] Understand smoke test integration in the pipeline
- [ ] Know channel promotion patterns
- [ ] Can explain sensitive variable handling and log redaction
- [ ] Understand IAM scoping for Packer builders
