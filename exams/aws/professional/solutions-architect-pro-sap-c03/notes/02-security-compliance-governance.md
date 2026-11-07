---
last-updated: 2026-11-07
difficulty: advanced
reading-time: 40 min
---

# Domain 2: Security, Compliance, and Governance (25%)

## Overview

Security is now a full domain at **25 percent**. It gathers content from C02's organizational-complexity domain (identity, encryption, governance) and its continuous-improvement domain (compliance, monitoring). Five tasks: **2.1** identity security architectures, **2.2** encryption and key management, **2.3** multi-account governance and compliance, **2.4** architectures to meet compliance requirements, **2.5** (new) security and responsible AI controls. The guide's out-of-scope list excludes security incident forensics and detailed threat investigation.

**[📖 Exam guide: Content Domain 2](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/solutions-architect-professional-03-domain2.html)** - Official tasks and skills

## Task 2.1: Identity security architectures

**Federation with standard protocols** (2.1.1). For a workforce, **IAM Identity Center** connects an external identity provider (SAML 2.0 or OIDC) with SCIM provisioning and maps users and groups to permission sets across accounts in an organization. Users sign in once and receive temporary credentials. For application users, **Amazon Cognito** user pools authenticate (OAuth 2.0, OIDC, social, SAML federation) and identity pools exchange tokens for AWS credentials (2.1.2). On Kubernetes, **EKS Pod Identity** gives a pod its own IAM role without node-wide permissions.

**Least privilege across accounts** (2.1.3). The toolkit and when to use each:

| Tool | Purpose |
|---|---|
| IAM role with trust policy | Cross-account access with temporary credentials |
| **External ID** | Protects against the confused-deputy problem when a third party assumes a role in your account |
| **Permissions boundary** | Caps the maximum permissions an identity-based policy can grant (delegated administration) |
| **Session policy** | Further restricts one assumed-role session |
| **ABAC** (attribute-based access control) | Allow by matching tags on principals and resources, so one policy scales across teams |
| **Service control policies (SCPs)** | Organization-wide ceiling on what accounts' principals can do (they never grant) |
| **Resource control policies (RCPs)** | Organization-wide ceiling on what can be done to resources, including by outside principals |

**Data perimeter and external access** (2.1.4). A data perimeter ensures only trusted identities access your resources from expected networks. Use **IAM Access Analyzer** to find resources shared outside the organization and to validate policies, **VPC endpoint policies** to restrict which principals and resources can be reached through an endpoint, and **AWS Verified Access** to give users access to corporate applications on zero-trust principles without a VPN. **Amazon Verified Permissions** (new to scope) externalizes fine-grained application authorization using the Cedar policy language.

**Workload identity outside AWS** (2.1.5, new). **IAM Roles Anywhere** lets workloads running on-premises or in other clouds obtain temporary AWS credentials by presenting an X.509 certificate issued by a trusted certificate authority, removing long-lived access keys.

**[📖 IAM Roles Anywhere](https://docs.aws.amazon.com/rolesanywhere/latest/userguide/introduction.html)** - Temporary credentials for workloads outside AWS

## Task 2.2: Encryption and key management

- **At rest** (2.2.1): use **customer managed KMS keys** when you need control over key policy, grants, rotation and auditing; enable automatic rotation. KMS keys can be single-Region or **multi-Region** keys for replicated data.
- **In transit** (2.2.2): TLS (the guide names TLS 1.3), certificates from **AWS Certificate Manager** for public endpoints, **AWS Private CA** for internal PKI.
- **Dedicated HSMs** (2.2.3): **AWS CloudHSM** when regulation requires single-tenant, customer-controlled hardware security modules. KMS custom key stores can back KMS keys with a CloudHSM cluster.
- **Post-quantum cryptography** (2.2.4, new): the guide's examples are AWS KMS with ML-DSA (Module-Lattice Digital Signature Algorithm) and ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism). The design concern is "harvest now, decrypt later": data with a long confidentiality lifetime may need quantum-resistant key exchange and signatures before large quantum computers exist.

**[📖 AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)** - Keys, policies, rotation and multi-Region keys

## Task 2.3: Multi-account governance and compliance

This task consolidates C02's governance content.

- **Organization structure** (2.3.1): **AWS Organizations** with organizational units (OUs), **AWS Control Tower** to set up a landing zone with guardrails (preventive via SCPs, detective via Config rules) and **Account Factory** for automated account provisioning.
- **Central logging and configuration** (2.3.2): CloudTrail **organization trails**, AWS Config **aggregators**, GuardDuty and Security Hub with delegated administrators, **Amazon Security Lake** to normalize security data into a central lake, CloudWatch Logs. New: include logging of **AI model invocations and responses**.
- **Cross-account sharing** (2.3.3): **AWS RAM** shares resources such as subnets and Transit Gateways without duplicating them.
- **Policy enforcement** (2.3.4): SCPs and RCPs.
- **Automated compliance monitoring** (2.3.5): AWS Config rules and conformance packs; Security Hub cloud security posture management checks.
- **Vulnerability and patch management** (2.3.6): **Amazon Inspector** continuously scans EC2 instances, container images and Lambda functions; **Systems Manager Patch Manager** applies patches on a schedule through patch baselines.

An SCP that prevents anyone in an OU from leaving approved Regions (a typical data-residency guardrail) looks like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyOutsideApprovedRegions",
      "Effect": "Deny",
      "NotAction": ["iam:*", "organizations:*", "route53:*", "cloudfront:*", "support:*"],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {"aws:RequestedRegion": ["us-east-1", "eu-west-1"]}
      }
    }
  ]
}
```

Global services are excluded through `NotAction` because they are not Regional.

**[📖 Service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)** - How SCPs filter permissions
**[📖 AWS Control Tower](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html)** - Landing zones and guardrails

## Task 2.4: Architectures that meet compliance requirements

- **Data protection** (2.4.1): combine encryption, access controls and audit logging.
- **Sovereignty and residency** (2.4.2, 2.4.4): residency controls keep data in specific Regions through Region-specific deployments and **transfer restrictions** (SCPs on Regions, bucket policies, replication rules that exclude other Regions). Sovereignty goes further, concerning who can legally compel access.
- **Audit trails** (2.4.3): CloudTrail with log file validation, S3 Object Lock for tamper-resistant retention, and (new) audit trails for AI services.
- **Evidence and reporting** (2.4.5, new): **AWS Artifact** provides AWS compliance reports and agreements on demand.
- **Risk assessment** (2.4.6, new): threat modeling (identify assets, trust boundaries, threats and mitigations before building) and mitigation strategies.

## Task 2.5 (new): Security and responsible AI controls

- **Content filtering and compliance controls** (2.5.1): **Amazon Bedrock Guardrails** applies configurable filters for harmful content, denied topics, word filters, sensitive information and grounding checks to model inputs and outputs.
- **Access control for AI applications** (2.5.2): **Amazon Bedrock AgentCore Identity** manages identity and access for agents calling tools and services on behalf of users.
- **Human oversight** (2.5.3): design approval steps for consequential AI actions, for example a Step Functions workflow that pauses for human approval before an agent executes a change.

**[📖 Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)** - Safeguards for generative AI applications

## What changed from C02 in this domain

- **New:** workload identity with IAM Roles Anywhere; application authN/authZ (Cognito, Pod Identity); post-quantum cryptography; data residency controls; compliance evidence (Artifact); risk assessment and threat modeling; all of task 2.5; AI logging and audit.
- **Consolidated:** federation, least privilege and data perimeter (C02 1.2) into 2.1; HSMs into 2.2; landing zones, centralized logging, SCP/RCP and automated compliance (C02 1.4, 3.2) into 2.3; sovereignty and audit trails (C02 3.2) into 2.4.
- **Removed from the blueprint text:** "application upgrade path", "delegating to AWS" (C02 domain 2) and "migration-tool security" (C02 domain 4). AWS notes these may still be implicit in other skills.
- **Services added to scope:** Amazon Security Lake, Amazon Verified Permissions, AWS Verified Access, Amazon Bedrock.

## Key terms

- **IAM Identity Center** - AWS's workforce single sign-on service that maps external identities to permission sets across accounts.
- **EKS Pod Identity** - a feature that associates an IAM role with a Kubernetes service account so pods get their own credentials.
- **External ID** - a value a third party must supply when assuming a role, protecting against the confused deputy problem.
- **Permissions boundary** - an IAM feature that sets the maximum permissions an identity-based policy can grant to a role or user.
- **ABAC** - attribute-based access control, which allows access by matching tags on principals and resources.
- **Service control policy** - an Organizations policy that sets the maximum permissions available to accounts in its scope.
- **Resource control policy** - an Organizations policy that sets the maximum permissions available on resources in member accounts.
- **IAM Access Analyzer** - a service that finds resources shared outside your organization and validates policies.
- **AWS Verified Access** - a service that gives users secure access to applications without a VPN, based on identity and device posture.
- **IAM Roles Anywhere** - a service that lets workloads outside AWS obtain temporary credentials using X.509 certificates.
- **AWS CloudHSM** - managed single-tenant hardware security modules that the customer controls.
- **Post-quantum cryptography** - cryptographic algorithms designed to resist attacks by large quantum computers, such as ML-KEM and ML-DSA.
- **AWS Control Tower** - a service that sets up and governs a multi-account landing zone with guardrails.
- **AWS RAM** - Resource Access Manager, which shares AWS resources across accounts without copying them.
- **Amazon Security Lake** - a service that centralizes security data from many sources in a normalized format in a customer-owned data lake.
- **Amazon Inspector** - a service that continuously scans workloads for software vulnerabilities and unintended exposure.
- **Data residency** - a requirement that data be stored and processed only in specified geographic locations.
- **AWS Artifact** - a portal for downloading AWS compliance reports and accepting agreements.
- **Bedrock Guardrails** - configurable safeguards that filter harmful content, denied topics and sensitive information in model inputs and outputs.
- **Amazon Verified Permissions** - a fine-grained authorization service for applications that uses the Cedar policy language.
