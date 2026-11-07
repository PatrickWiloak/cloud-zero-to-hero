---
last-updated: 2026-10-22
applies-to: SOA-C03 exam guide v1.1
---

# Domain 3: Deployment, Provisioning, and Automation

Domain 3 carries **22%** of the scored content. **Task 3.1** is provisioning and maintaining resources: images, infrastructure as code, deployment troubleshooting, sharing across accounts and Regions, deployment strategies and third-party tools. **Task 3.2** is automating the management of what already exists, with Systems Manager and event-driven automation.

The exam guide lists **designing CI/CD pipelines** as out of scope. You still need to recognize what CodePipeline, CodeBuild and CodeDeploy do and to operate deployments safely, but you will not be asked to architect a pipeline from nothing.

> **Retired service:** AWS OpsWorks (Stacks, Chef Automate and Puppet Enterprise) reached **end of life in May 2024** and is no longer available. If an answer option offers OpsWorks for configuration management, it is wrong for current AWS; the replacement is Systems Manager (State Manager, Run Command, Automation, Distributor).

---

## Task 3.1 - Provision and maintain cloud resources

### 3.1.1 Create and manage AMIs and container images (EC2 Image Builder)

#### AMIs by hand, and their operational facts

An **Amazon Machine Image (AMI)** is a template for launching instances: snapshots of the root (and optionally data) volumes, launch permissions and a block device mapping. Facts that come up in operations questions:

- **AMIs are Regional.** To launch in another Region, **copy** the AMI there (`copy-image`). Copying can also add or change encryption.
- **Sharing** an AMI with another account means adding launch permissions. If its snapshots are encrypted with a **customer managed KMS key**, you must also share the key (key policy or grant) or the other account cannot launch it. AMIs encrypted with the **AWS managed key** for EBS cannot be shared; re-encrypt with a customer managed key first.
- **Deprecation and deregistration.** Set a deprecation time so old AMIs stop appearing in default searches; deregister AMIs you no longer want (and delete their snapshots separately to stop paying for storage).
- **Finding the latest AMI.** Reference public Systems Manager parameters such as `/aws/service/ami-amazon-linux-latest/...` in launch templates and CloudFormation rather than hard-coding IDs that differ per Region.

#### EC2 Image Builder

**EC2 Image Builder** is the managed way to build, test and distribute **AMIs and container images** on a schedule, instead of hand-built "golden images" or homemade scripts.

| Building block | What it defines |
|---|---|
| **Component** | A step: build (install software, apply hardening) or test (validate the result). AWS provides managed components; you can write your own in YAML |
| **Image recipe** | Parent image plus components and block device settings, for an AMI |
| **Container recipe** | Base image plus components, producing a container image pushed to **Amazon ECR** |
| **Infrastructure configuration** | Instance type, subnet, security group, instance profile and logging used during the build |
| **Distribution settings** | Which **Regions** and **accounts** (or organizations and OUs) receive the output, launch permissions, AMI naming, launch template updates |
| **Image pipeline** | Ties it together with a **schedule** (cron, or when a dependency such as the parent image updates) |

The pipeline launches a build instance, applies the components, creates an image, launches a **test** instance and runs test components, then distributes. Failures leave logs in S3 or CloudWatch Logs if configured. Common failures are the **instance profile** missing `EC2InstanceProfileForImageBuilder` (and `AmazonSSMManagedInstanceCore`, because Image Builder drives the instance through Systems Manager), no network path from the build subnet to Systems Manager and package repositories, and a component that exits non-zero. Image Builder can also scan output images for vulnerabilities with Amazon Inspector.

#### Container images and Amazon ECR

ECR stores container images in private repositories. Know: **lifecycle policies** that expire untagged or old images; **image scanning** (basic, or enhanced with Amazon Inspector); **tag immutability** so a tag such as `v1.4.2` cannot be overwritten; **cross-Region and cross-account replication**; and that pulling from ECR in a private subnet needs the `ecr.api` and `ecr.dkr` interface endpoints plus the **S3 gateway endpoint** (image layers are stored in S3).

**[📖 What is EC2 Image Builder?](https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html)** - pipelines, recipes, components
**[📖 Manage EC2 Image Builder distribution settings](https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-distribution-settings.html)** - Regions, accounts and launch permissions
**[📖 Share an AMI with specific AWS accounts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sharingamis-explicit.html)** - including encrypted AMIs
**[📖 Copy an AMI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html)** - cross-Region copy and encryption
**[📖 Amazon ECR lifecycle policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html)** - image cleanup

### 3.1.2 Create and manage resources with CloudFormation and the AWS CDK

#### CloudFormation essentials

A **template** (YAML or JSON) declares resources; a **stack** is a deployed instance of it. Sections: `Parameters` (inputs, including `AWS::SSM::Parameter::Value<...>` types that read Parameter Store at deploy time), `Mappings` (static lookups via `Fn::FindInMap`), `Conditions`, `Resources` (the only required section), and `Outputs` (with `Export` for cross-stack references read by `Fn::ImportValue`).

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Parameters:
  Env: { Type: String, AllowedValues: [dev, prod] }
  LatestAmi:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64
Conditions:
  IsProd: !Equals [!Ref Env, prod]
Resources:
  Web:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref LatestAmi
      InstanceType: !If [IsProd, m7i.large, t3.micro]
  Data:
    Type: AWS::EBS::Volume
    DeletionPolicy: Snapshot
    UpdateReplacePolicy: Snapshot
    Properties:
      AvailabilityZone: !GetAtt Web.AvailabilityZone
      Size: 50
Outputs:
  WebId:
    Value: !Ref Web
    Export: { Name: !Sub "${AWS::StackName}-WebId" }
```

Operational features you must know:

- **Change sets** preview what an update will add, modify or **replace**. Replacement of a stateful resource (a database whose name changed) means data loss, so review change sets for production updates.
- **Update behaviors** per property: no interruption, some interruption, or replacement.
- **DeletionPolicy** (`Delete`, `Retain`, `Snapshot`, `RetainExceptOnCreate`) and **UpdateReplacePolicy** protect data when a resource is deleted or replaced.
- **Stack policies** block updates to named resources; **termination protection** blocks stack deletion.
- **Drift detection** compares live resources to the template and reports `IN_SYNC`, `MODIFIED` or `DELETED`.
- **Nested stacks** reuse templates as components; **modules** and **custom resources** (Lambda-backed) extend what CloudFormation can do.
- **Creation policies and wait conditions** with `cfn-signal` make the stack wait until instance bootstrapping succeeds; helper scripts `cfn-init` and `cfn-hup` apply and re-apply configuration from metadata.
- **Service role** - a stack can run with an IAM role you pass, so users need only `iam:PassRole` and CloudFormation permissions, not rights to every resource.
- **Rollback** - on failure, a create rolls back by default; you can choose to **preserve successfully provisioned resources** to debug, and roll back later.

#### AWS CDK

The **AWS CDK** defines infrastructure in TypeScript, Python, Java, C#/.NET or Go and **synthesizes** CloudFormation templates; the deployment engine is still CloudFormation. **Constructs** come in three levels: L1 (one-to-one with CloudFormation resources), L2 (curated with sensible defaults and helper methods such as `bucket.grantRead(role)`), and L3 patterns (several resources wired together). Commands: `cdk bootstrap` (once per account and Region, creates the staging bucket and deployment roles; a missing bootstrap is a common first-deploy error), `cdk synth`, `cdk diff`, `cdk deploy`, `cdk destroy`. **CDK Pipelines** is a construct library for self-updating CodePipeline deployments of CDK apps.

**[📖 What is AWS CloudFormation?](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)** - templates, stacks, change sets
**[📖 Update CloudFormation stacks using change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)** - previewing changes
**[📖 Detect unmanaged configuration changes (drift)](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)** - drift detection
**[📖 DeletionPolicy attribute](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-deletionpolicy.html)** - Retain and Snapshot
**[📖 What is the AWS CDK?](https://docs.aws.amazon.com/cdk/v2/guide/home.html)** - constructs, apps, stacks
**[📖 AWS CDK bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html)** - preparing an environment

### 3.1.3 Identify and remediate deployment issues

The guide names three families: **subnet sizing**, **CloudFormation errors** and **permissions**.

**Subnet sizing.** AWS reserves **five IP addresses in every subnet** (network address, VPC router, DNS, one reserved for future use, broadcast), so a `/28` has 11 usable addresses, not 16. Deployments that consume many IPs fail with "insufficient free addresses": ASGs scaling out, **EKS** (every pod gets a VPC IP with the default VPC CNI), **Lambda in a VPC** (Hyperplane ENIs), interface endpoints, load balancers (an ALB needs free addresses in each subnet to scale). Fixes: larger subnets for new deployments, adding a **secondary CIDR** to the VPC and new subnets, or prefix delegation and custom networking for EKS. A subnet's CIDR cannot be resized after creation.

**CloudFormation errors** and what they mean:

| Status or message | Meaning and fix |
|---|---|
| `CREATE_FAILED` with `ROLLBACK_COMPLETE` | Creation failed and everything rolled back; read the **first** failed event in the Events tab, fix, delete the stack and recreate (a stack in `ROLLBACK_COMPLETE` can only be deleted) |
| `UPDATE_ROLLBACK_FAILED` | A resource could not return to its old state (for example it was changed or deleted outside CloudFormation); fix the resource by hand, then **continue update rollback**, optionally skipping resources |
| `DELETE_FAILED` | Often a non-empty S3 bucket, a security group still in use, or a resource with deletion protection; empty or detach it, or retain it and retry |
| "Resource already exists" | A physical name (bucket, role, log group) collides with an existing resource; let CloudFormation generate names or import the resource |
| Timeout waiting for signal | `cfn-signal` never arrived: bootstrap script failed, no outbound network to the CloudFormation endpoint, or the timeout is too short |
| Limit or quota exceeded | Request a quota increase; check the Service Quotas console |

**Permissions.** "User is not authorized to perform `iam:PassRole`" is the classic deployment error whenever a resource takes a role (EC2 instance profiles, Lambda execution roles, CloudFormation service roles, ECS task roles). Other permission causes: the CloudFormation service role lacks a permission for one resource type; an **SCP** in the organization denies the action or Region; a **KMS key policy** does not allow the deploying principal to use an encrypted AMI, volume or secret. CloudTrail shows the exact denied call, and the error message often contains an encoded authorization message you can decode with `aws sts decode-authorization-message`.

**[📖 Troubleshooting CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html)** - common errors and fixes
**[📖 Continue rolling back an update](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html)** - UPDATE_ROLLBACK_FAILED recovery
**[📖 Subnet CIDR blocks](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html)** - the five reserved addresses
**[📖 Grant a user permissions to pass a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html)** - iam:PassRole

### 3.1.4 Provision and share resources across Regions and accounts (AWS RAM, CloudFormation StackSets)

#### AWS Resource Access Manager (RAM)

**RAM** shares resources you own with other accounts, organizational units or the whole organization, so they do not have to create copies. Commonly shared resources: **VPC subnets** (the basis of shared VPCs, where a central network account owns the VPC and application accounts launch into its subnets), **Transit Gateways**, **Route 53 Resolver rules** (so every account forwards on-premises domains the same way), **prefix lists**, **License Manager configurations**, **Network Firewall policies**, **Capacity Reservations**, and many others.

Within an organization, enable **sharing with AWS Organizations** in RAM and shares are accepted automatically; outside it, the recipient must accept an invitation. Participants in a shared VPC can create and manage their own resources in shared subnets, but cannot modify or delete the subnets, route tables or other resources the owner controls, and cannot see the owner's resources in that VPC.

#### CloudFormation StackSets

A **StackSet** deploys one template as **stack instances** across many accounts and Regions from an administrator account (or a delegated administrator).

- **Self-managed permissions** - you create an administration role in the admin account and an execution role in each target account.
- **Service-managed permissions** - with AWS Organizations, StackSets creates the roles for you, you target **OUs**, and **automatic deployment** adds stack instances when accounts join an OU (and optionally removes them when accounts leave).
- **Deployment options** - maximum concurrent accounts, failure tolerance, and Region order (sequential or parallel) control blast radius.
- **Drift detection** works across stack instances.

Typical uses: an AWS Config rule, an IAM role for central operations, a CloudTrail or GuardDuty setting or a baseline VPC in every account and Region.

**[📖 What is AWS RAM?](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html)** - resource shares and principals
**[📖 Shareable AWS resources](https://docs.aws.amazon.com/ram/latest/userguide/shareable.html)** - the full list
**[📖 Share your VPC with other accounts](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing.html)** - shared VPC rules
**[📖 Managing stacks across accounts and Regions with StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)** - permissions models and options

### 3.1.5 Implement deployment strategies and services

| Strategy | How it works | Downtime / rollback |
|---|---|---|
| **All at once / in-place** | Update every target together | Downtime likely; rollback is a redeploy |
| **Rolling** | Update in batches; capacity drops by one batch | No downtime; slow rollback |
| **Rolling with additional batch** | Launch an extra batch first so capacity stays full | No capacity loss; costs a little more |
| **Immutable** | Launch new instances (new ASG) for the new version, then swap | Fast rollback by discarding new instances |
| **Blue/green** | Full new environment; shift traffic by load balancer, target group or DNS | Instant rollback by shifting back |
| **Canary** | Send a small share of traffic first, then the rest | Limits blast radius |
| **Linear** | Shift traffic in equal steps at intervals | Gradual, alarms can stop it |

Where you meet them on AWS:

- **AWS CodeDeploy** - in-place or blue/green for EC2 and on-premises; canary, linear or all-at-once traffic shifting for **Lambda** (aliases) and **ECS**. The `appspec.yml` file defines lifecycle hooks (`BeforeInstall`, `AfterInstall`, `ApplicationStart`, `ValidateService`, and for Lambda and ECS, `BeforeAllowTraffic`/`AfterAllowTraffic`). Attach **CloudWatch alarms** to a deployment group to stop and **roll back automatically** when an alarm fires.
- **Amazon ECS** - rolling updates controlled by `minimumHealthyPercent` and `maximumPercent`, the **deployment circuit breaker** that rolls back failed deployments, and blue/green deployments.
- **Elastic Beanstalk** - all at once, rolling, rolling with additional batch, immutable, traffic splitting, and blue/green by **swapping environment URLs**.
- **EC2 Auto Scaling instance refresh** - rolling replacement after a launch template change, with checkpoints and automatic rollback.
- **Lambda** - versions and **aliases** with weighted traffic between two versions.
- **Route 53 weighted records** - shift traffic between whole environments.

**[📖 Working with deployment configurations in CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html)** - canary, linear, all-at-once
**[📖 CodeDeploy AppSpec file reference](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file.html)** - lifecycle hooks
**[📖 Elastic Beanstalk deployment policies](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.rolling-version-deploy.html)** - rolling, immutable, traffic splitting
**[📖 Amazon ECS deployment circuit breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html)** - automatic rollback
**[📖 Instance refresh](https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-instance-refresh.html)** - rolling ASG replacement

### 3.1.6 Use and manage third-party tools to automate deployment (Terraform, Git)

**Terraform** (HashiCorp) is declarative infrastructure as code that calls AWS APIs directly through the AWS **provider**, rather than through CloudFormation. Concepts an operator must manage:

- **State** - Terraform records what it created in a state file. Store it remotely in an **S3 backend** (versioned and encrypted bucket) with **state locking** so two people cannot apply at once. Current versions of the S3 backend can lock using a lock file in the bucket; older setups use a DynamoDB table for locking. Never edit state by hand; use `terraform state` and `terraform import`.
- **Workflow** - `terraform init` (download providers, configure backend), `plan` (show changes, the equivalent of a change set), `apply`, `destroy`. Review the plan before applying to production.
- **Credentials** - give Terraform an IAM role (assumed from a CI runner via OIDC, or an instance or task role), never long-lived access keys in code.
- **Drift** - `terraform plan` reveals changes made outside Terraform, much like CloudFormation drift detection.
- **Modules** for reuse and **workspaces** or separate state files per environment.

**Git** is the source of truth for both application and infrastructure code. Operational practices: changes go through branches and pull requests with review; a merge to the main branch triggers the pipeline (CodePipeline connects to GitHub, GitLab and Bitbucket through **CodeConnections**; GitHub Actions or other CI can also deploy with an assumed IAM role). **CloudFormation Git sync** can keep a stack in step with a template file in a repository. Keep secrets out of repositories (use Secrets Manager or Parameter Store references).

**[📖 Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)** - provider documentation
**[📖 Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)** - remote state and locking
**[📖 CloudFormation Git sync](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/git-sync.html)** - stacks from a repository
**[📖 AWS CodeConnections](https://docs.aws.amazon.com/dtconsole/latest/userguide/welcome-connections.html)** - linking Git providers

---

## Task 3.2 - Automate the management of existing resources

### 3.2.1 Use AWS services to automate operational processes (Systems Manager)

Systems Manager manages **managed nodes**: EC2 instances, on-premises servers and edge devices running the **SSM Agent**, with an instance profile that includes `AmazonSSMManagedInstanceCore` (or Default Host Management Configuration), and a network path to the `ssm`, `ssmmessages` and `ec2messages` endpoints (interface endpoints in private subnets). A node missing from Fleet Manager is almost always one of those three: agent, role, network.

| Capability | Use it to |
|---|---|
| **Run Command** | Run a command document across many nodes now, with rate control and output to S3 or CloudWatch Logs |
| **State Manager** | Keep nodes in a desired state on a schedule (for example, "CloudWatch agent installed and configured" or "antivirus running") via associations |
| **Patch Manager** | Scan or install patches according to **patch baselines** (auto-approval rules, approved and rejected lists), grouped by **patch groups** or patch policies, with compliance reporting |
| **Maintenance Windows** | Schedule disruptive tasks (patching, Automation runbooks) in agreed time slots |
| **Automation** | Multi-step runbooks across AWS resources (see [note 01](./01-monitoring-logging.md#123-create-and-run-custom-and-predefined-systems-manager-automation-runbooks)) |
| **Distributor** | Package and install software (including the CloudWatch agent) |
| **Inventory** | Collect installed software, files and configuration from nodes |
| **Session Manager** | Browser or CLI shell with no SSH keys, no bastion and no inbound ports; sessions logged to S3 or CloudWatch Logs |
| **Parameter Store** | Hierarchical configuration and `SecureString` secrets |
| **Quick Setup** | Configure common settings (patching, agent updates, Host Management) across accounts and Regions |

Most of these can target nodes **by tag**, so automation follows the fleet as it changes.

**[📖 AWS Systems Manager capabilities](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html)** - overview
**[📖 Systems Manager State Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-state.html)** - associations
**[📖 Systems Manager Patch Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager.html)** - baselines and compliance
**[📖 Troubleshooting managed node availability](https://docs.aws.amazon.com/systems-manager/latest/userguide/fleet-manager-troubleshooting-managed-nodes.html)** - agent, role, network

### 3.2.2 Implement event-driven automation (Lambda, S3 Event Notifications, EventBridge, AWS DevOps Agent)

**Lambda** is the glue for custom actions: tag resources at creation, revert a risky change, rotate something on a schedule, post to a chat channel. Give each function a minimal execution role and alarm on its `Errors` metric so the automation itself is monitored.

**S3 Event Notifications** fire on object events such as `s3:ObjectCreated:*` and `s3:ObjectRemoved:*`, optionally filtered by prefix and suffix, to **SNS, SQS, Lambda**, or to **EventBridge** (turn on EventBridge delivery for the bucket, then use rules for richer filtering and many targets). Troubleshooting:

- The destination's resource policy must allow `s3.amazonaws.com` to publish or invoke (S3 validates this when you save the configuration).
- Two notification configurations whose prefixes and suffixes **overlap** for the same event type are rejected.
- A Lambda that writes back to the same bucket and prefix it is triggered by causes a **recursive loop**; write to a different bucket or prefix.
- Delivery is at least once, so consumers should be idempotent.

**EventBridge** (see [note 01](./01-monitoring-logging.md#122-use-eventbridge-to-route-enrich-and-deliver-events-and-troubleshoot-event-bus-rules)) routes service events, CloudTrail API events and scheduled events to Lambda, Automation, Step Functions and more. A typical pattern is "EC2 instance launched without the required tag, so stop it and notify the owner".

**AWS DevOps Agent** fits the event-driven picture as an investigator: an alert or ticket starts an automatic investigation, and its findings and mitigation steps are routed to the team's channels. Its preview release-management features can review code changes for production risk before deployment. It does not replace deterministic automation; use it to understand what went wrong, and EventBridge plus Lambda or Automation to apply known fixes.

**[📖 Amazon S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html)** - event types and destinations
**[📖 Using EventBridge with S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html)** - enabling delivery to EventBridge
**[📖 About AWS DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html)** - investigations and release management

---

## Exam traps

- **OpsWorks is end of life** (May 2024). Configuration management answers are Systems Manager.
- **AMIs are Regional**; copy them. Sharing an encrypted AMI also needs the **customer managed KMS key** shared.
- **Image Builder** is the managed answer for scheduled, tested, multi-Region golden images and container images.
- **`ROLLBACK_COMPLETE` stacks** can only be deleted; **`UPDATE_ROLLBACK_FAILED`** needs "continue update rollback".
- **Five reserved IPs per subnet**; subnets cannot be resized.
- **`iam:PassRole`** is the missing permission in many deployment failures.
- **StackSets with service-managed permissions** target OUs and auto-deploy to new accounts.
- **RAM shares subnets, Transit Gateways and Resolver rules** - share instead of duplicating.
- **Terraform state** belongs in a locked, versioned, encrypted S3 backend.
- **SSM managed node missing**: agent, instance profile, or endpoints.
- **S3 to Lambda recursion** - never write to the prefix that triggers the function.

## Key terms

- **EC2 Image Builder** - managed service that builds, tests and distributes AMIs and container images on a schedule
- **Image recipe** - Image Builder definition of a parent image plus build and test components for an AMI
- **Distribution settings** - Image Builder configuration naming the Regions and accounts that receive the output image
- **Change set** - preview of the resources a CloudFormation stack update will add, modify or replace
- **DeletionPolicy** - CloudFormation attribute that retains or snapshots a resource instead of deleting it with the stack
- **Drift detection** - compares live resources with their CloudFormation template and reports modified or deleted resources
- **UPDATE_ROLLBACK_FAILED** - stack state where rollback could not finish; fix the resource and continue update rollback
- **cdk bootstrap** - one-time setup per account and Region that creates the resources the AWS CDK needs to deploy
- **AWS RAM** - Resource Access Manager, shares resources such as subnets, Transit Gateways and Resolver rules with other accounts
- **Service-managed StackSets** - StackSets using AWS Organizations to target OUs and auto-deploy to accounts that join them
- **Blue/green deployment** - run the new version in a separate environment and shift traffic to it, with instant rollback
- **Canary deployment** - shift a small share of traffic to the new version first, then the rest if it is healthy
- **Terraform state** - Terraform's record of managed resources; keep it in a versioned, encrypted, locked S3 backend
- **State Manager association** - keeps managed nodes in a defined state by applying a document on a schedule
- **Patch baseline** - Patch Manager rules that decide which patches are approved or rejected for installation

## Vendor documentation

**[📖 SOA-C03 Domain 3 in the exam guide](https://docs.aws.amazon.com/aws-certification/latest/sysops-administrator-associate-03/sysops-administrator-associate-03-domain3.html)** - official task statements
**[📖 Migrate AWS OpsWorks Stacks to Systems Manager](https://aws.amazon.com/blogs/mt/migrate-your-aws-opsworks-stacks-to-aws-systems-manager/)** - the OpsWorks replacement path
**[📖 AWS CodePipeline user guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)** - stages, actions and artifacts
