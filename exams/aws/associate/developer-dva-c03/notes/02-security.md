---
last-updated: 2026-11-07
difficulty: intermediate
reading-time: 30 min
---

# Domain 2: Security (26%)

## Overview

Security stays at 26 percent in C03. The domain has three tasks: **2.1** authentication and authorization, **2.2** encryption and sensitive data, and **2.3** (new) identifying and mitigating security risks of using AI services in applications. C03 merged the old encryption and sensitive-data tasks (13 skills) into one task of 7 skills, and added presigned URLs as an explicit skill.

**[📖 Exam guide: Content Domain 2](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-03/developer-associate-03-domain2.html)** - The official skills list

## Task 2.1: Authentication and authorization

### IAM principals, roles and policies

An IAM **principal** (user, role, service) is allowed to do things by **policies**. Applications running on AWS should use **roles**, which supply short-lived credentials, never long-lived access keys. The identity-based policy is attached to the principal; a **resource-based policy** (an S3 bucket policy, a Lambda resource policy, a KMS key policy) is attached to the resource and can name principals from other accounts. Evaluation starts from an implicit deny; an explicit `Deny` always wins.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::example-app-bucket/uploads/*"
    }
  ]
}
```

Least privilege means naming exact actions and resources, as above, rather than `s3:*` on `*`.

### Assuming a role and calling services

AWS **STS** issues temporary credentials. `AssumeRole` returns an access key, secret key and session token valid for a limited time (skill 2.1.7). Cross-account access works when the target role's trust policy names the caller and the caller's own policy allows `sts:AssumeRole`.

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::111122223333:role/ReadOnlyAudit \
  --role-session-name audit-session \
  --duration-seconds 3600
```

Programmatic access (2.1.3) is the SDK/CLI credential chain; make authenticated calls (2.1.5) by letting the SDK sign requests with SigV4 rather than hand-rolling signatures. MFA can be required by adding the `aws:MultiFactorAuthPresent` condition key to a policy.

### Federation for application users

**Amazon Cognito** has two parts. A **user pool** is a user directory that authenticates users (sign-up, sign-in, MFA, social and SAML/OIDC federation) and issues JSON Web Tokens. An **identity pool** exchanges a token from a user pool or another identity provider for temporary AWS credentials so the client can call AWS services directly. API Gateway can use a Cognito user pool authorizer to validate tokens. For workforce identity federation (skill 2.1.1) use IAM Identity Center or SAML 2.0/OIDC identity providers in IAM.

### Presigned URLs (new explicit skill)

A **presigned URL** grants time-limited access to a specific object using the credentials of the principal that created it, so the holder needs no AWS credentials of their own. Typical use: let a browser upload or download one S3 object.

```bash
aws s3 presign s3://example-app-bucket/reports/q3.pdf --expires-in 900
```

The URL stops working when it expires, and it carries only the permissions of its creator, so a role with limited permissions yields a limited URL. For CloudFront (skill 2.1.4) the equivalent is **signed URLs** and **signed cookies**.

**[📖 Sharing objects with presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)** - Creating and using presigned URLs
**[📖 Amazon Cognito user pools and identity pools](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)** - The two components and how they differ

## Task 2.2: Encryption and sensitive data

- **At rest and in transit** (2.2.1): S3, EBS, RDS, DynamoDB and most services encrypt at rest with AWS KMS keys; in transit, use TLS (HTTPS endpoints). You can require TLS on an S3 bucket with a bucket policy that denies requests when `aws:SecureTransport` is `false`.
- **Server-side versus client-side** (2.2.3): in server-side encryption the service encrypts after receiving your plaintext. In client-side encryption you encrypt before sending, so the service never sees plaintext.
- **Keys** (2.2.4): AWS KMS holds **KMS keys**. Direct `Encrypt` handles small payloads (up to 4 KB). For larger data use **envelope encryption**: ask KMS for a data key with `GenerateDataKey`, encrypt the data locally with the plaintext data key, discard the plaintext key and store the encrypted data key alongside the ciphertext. To decrypt, send the encrypted data key to KMS `Decrypt`.

```bash
aws kms generate-data-key --key-id alias/app-key --key-spec AES_256
```

- **Certificates** (2.2.2, 2.2.5): AWS Certificate Manager provisions and renews public TLS certificates for integrated services such as CloudFront and load balancers; AWS Private CA issues private certificates for internal use. Generating a key pair or certificate for development is done locally, for example `ssh-keygen -t ed25519`, but never reuse development keys in production.
- **Sensitive data** (2.2.6): identify, mask and limit access to PII and PHI with services such as Amazon Macie (finds sensitive data in S3), fine-grained IAM and data masking in your application code and logs.
- **Secrets** (2.2.7): store credentials in **AWS Secrets Manager** (rotation built in, charged per secret) or **Systems Manager Parameter Store** (hierarchical names, `SecureString` encrypted by KMS, lower cost, no built-in rotation). Retrieve at run time rather than baking into code or environment variables in source control.

```bash
aws secretsmanager get-secret-value --secret-id prod/app/db --query SecretString --output text
aws ssm get-parameter --name /prod/app/api-key --with-decryption --query Parameter.Value --output text
```

**[📖 AWS KMS concepts: envelope encryption](https://docs.aws.amazon.com/kms/latest/developerguide/kms-cryptography.html)** - Data keys and key hierarchy
**[📖 AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)** - Storing, rotating and retrieving secrets

## Task 2.3 (new): Security risks of AI services

This task is new in C03 and has five skills. It is about the developer's responsibilities when an application calls AI services, not about training models.

1. **Request and manage access to AI services (2.3.1).** Access to AI features is governed by IAM like any service. Grant a role only the specific invoke actions and resources it needs (for Bedrock, for example, `bedrock:InvokeModel` on named models), and check the service documentation for any model access or agreement step that applies to your account.
2. **Data privacy controls (2.3.2).** The guide's example is using **VPC endpoints** (AWS PrivateLink) to reach the AI service over private connectivity, and ensuring inputs and outputs are not used to train models. Know the pattern: private connectivity keeps traffic off the public internet; the provider's data-use terms and settings determine whether your data is used for training.
3. **Filter and control model inputs and outputs (2.3.3).** The guide lists content filtering, sensitive-information detection, PII/PHI redaction, denied-topic policies and protection against **prompt injection** and manipulation. On AWS, Amazon Bedrock Guardrails is the feature that applies these policies to inputs and outputs. Validate and sanitize model output before using it, as you would any untrusted input.
4. **Secure AI agent interactions (2.3.4).** Agents that call tools need **tool-use authorization** (least privilege per tool), **session isolation** (one user's context never leaks into another's), and **human-in-the-loop approval** for sensitive actions such as payments or deletions.
5. **Protect sensitive content in monitoring logs (2.3.5).** Prompts and responses can contain personal data; if you log them for debugging, mask or exclude sensitive fields and restrict access to those logs.

**[📖 Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)** - Content filters, denied topics and sensitive information filters
**[📖 Amazon Bedrock and interface VPC endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html)** - Private connectivity to the service

## What changed from C02 in this domain

- **Added:** all of task 2.3 (AI security) and presigned URLs as a named skill (2.1.4).
- **Merged:** C02 tasks 2.2 (encryption, 6 skills) and 2.3 (sensitive data, 7 skills) became the single C03 task 2.2 (7 skills).
- **Weight:** unchanged at 26 percent.

## Key terms

- **IAM role** - an identity with permissions that is assumed temporarily, providing short-lived credentials.
- **Trust policy** - the resource policy on an IAM role that defines who may assume it.
- **STS AssumeRole** - the API that returns temporary credentials for a role.
- **Cognito user pool** - a user directory that authenticates application users and issues tokens.
- **Cognito identity pool** - a service that exchanges identity tokens for temporary AWS credentials.
- **Presigned URL** - a URL that grants time-limited access to a specific S3 object using its creator's permissions.
- **Envelope encryption** - encrypting data with a data key and then encrypting that data key under a KMS key.
- **GenerateDataKey** - the KMS operation that returns a plaintext data key and a copy encrypted under a KMS key.
- **AWS Secrets Manager** - a service that stores and automatically rotates secrets such as database credentials.
- **Parameter Store SecureString** - a Systems Manager parameter type whose value is encrypted with KMS.
- **AWS Certificate Manager** - a service that provisions and renews public TLS certificates for integrated AWS services.
- **AWS Private CA** - a managed private certificate authority for issuing internal certificates.
- **Prompt injection** - an attack in which input text manipulates a model into ignoring its instructions.
- **Bedrock Guardrails** - Amazon Bedrock policies that filter content, deny topics and redact sensitive information on model inputs and outputs.
- **Session isolation** - keeping each user's agent session and context separate so data cannot leak between users.
- **Human-in-the-loop approval** - requiring a person to approve a sensitive action proposed by an AI agent before it runs.
