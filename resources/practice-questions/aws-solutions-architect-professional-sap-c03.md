---
last-updated: 2026-11-07
difficulty: intermediate
---

# AWS Certified Solutions Architect - Professional (SAP-C03) - Practice Questions

20 original scenario questions for SAP-C03 prep. Counts follow the exam weights: Architecture 5, Security and Governance 5, Cost 3, Resilience and Migration 3, Operational Excellence 4.

> **Cert page:** [exams/aws/professional/solutions-architect-pro-sap-c03/](../../exams/aws/professional/solutions-architect-pro-sap-c03/)

---

### Question 1
**Scenario:** A company runs 40 services across 12 AWS accounts and wants authenticated service-to-service calls with consistent policies and request metrics, without operating sidecar proxies. Which service fits best?

A. A self-managed service mesh on EC2
B. Application Load Balancers in every account with shared certificates
C. Amazon VPC Lattice
D. VPC peering between all VPCs with security groups

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** VPC Lattice provides service networks with auth policies and observability across VPCs and accounts without sidecars. Peering gives connectivity but no application-layer policy, and a self-managed mesh adds operations.
</details>

---

### Question 2
**Scenario:** On-premises servers must resolve names in a Route 53 private hosted zone, and VPC workloads must resolve names in the corporate domain. What should be configured?

A. A Route 53 Resolver inbound endpoint and an outbound endpoint with a forwarding rule
B. Public hosted zones for both domains, with the internal records published so on-premises hosts can query them over the internet
C. A Site-to-Site VPN, which automatically shares DNS
D. Copy the private zone records into on-premises hosts files

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Inbound endpoints let on-premises resolvers query VPC DNS; outbound endpoints with forwarding rules send queries for the corporate domain to on-premises servers. A VPN provides connectivity but not DNS forwarding.
</details>

---

### Question 3
**Scenario:** A multi-tenant SaaS has a few large customers needing strict isolation and thousands of small customers where cost matters most. Which design is most appropriate?

A. One AWS account and one dedicated database per tenant for every tenant, including the thousands of small customers that cannot justify the cost
B. A single shared database with no tenant identifiers
C. A separate AWS Region per tenant
D. Pool shared resources with row-level tenant isolation for small tenants and silo dedicated resources for large tenants

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** A tiered model mixes pool and silo according to isolation needs and cost. Per-tenant accounts for thousands of tenants are costly to operate, and no tenant identification provides no isolation.
</details>

---

### Question 4
**Scenario:** Two production VPCs in different accounts both use 10.0.0.0/16. One application in VPC A must call a single API service in VPC B privately. What should be used?

A. Re-address both VPCs immediately
B. AWS PrivateLink exposing the service in VPC B through an endpoint in VPC A
C. VPC peering between the two VPCs
D. A Transit Gateway attachment for each VPC

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** PrivateLink exposes one service privately and works with overlapping CIDRs. Peering and Transit Gateway require non-overlapping address space.
</details>

---

### Question 5
**Scenario:** A team needs a data lake on S3 with centralized fine-grained access control by database, table and column, and the ability to query it from Athena and Redshift Spectrum. Which service provides the governance layer?

A. Amazon Macie
B. AWS Config
C. Amazon Inspector
D. AWS Lake Formation

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Lake Formation provides centralized permissions for data lakes and integrates with Athena and Redshift Spectrum. The others address sensitive-data discovery, configuration compliance and vulnerability scanning.
</details>

---

### Question 6
**Scenario:** A vendor must assume a role in your account to read billing data. You must prevent another customer of that vendor from causing the vendor to assume your role. What should the trust policy include?

A. An external ID condition
B. A permissions boundary
C. A session policy only
D. A higher maximum session duration

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** An external ID defends against the confused deputy problem for third-party access. Boundaries and session policies limit permissions but do not prove which customer is asking.
</details>

---

### Question 7
**Scenario:** Compliance requires that no one in the organization, including account administrators, can create resources outside two approved Regions. Which control enforces this?

A. A CloudWatch alarm on resource creation
B. An S3 bucket policy
C. An SCP that denies actions when aws:RequestedRegion is not an approved Region, excluding global services
D. An IAM policy attached to the administrators in each account that denies any action outside the approved Regions

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** SCPs set organization-wide ceilings that account administrators cannot remove. Account-level IAM policies can be changed by those administrators, and alarms only detect.
</details>

---

### Question 8
**Scenario:** Servers running in another cloud need to call AWS APIs without long-lived access keys. What should be used?

A. Use the root user credentials
B. IAM Roles Anywhere with certificates from a trusted CA
C. Create IAM users and distribute access keys
D. Make the S3 buckets public

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** IAM Roles Anywhere exchanges an X.509 certificate for temporary AWS credentials. Long-lived keys are what the requirement avoids.
</details>

---

### Question 9
**Scenario:** A company must keep data confidential for 20 years and wants to prepare for future quantum-capable adversaries. Which concern does this raise?

A. Increasing log retention to 20 years so that every attacker's access attempt remains available for later review
B. Disabling TLS
C. Moving to larger EBS volumes
D. Using quantum-resistant key encapsulation and signature algorithms such as ML-KEM and ML-DSA where supported

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Long-lived confidentiality needs protection against harvest now, decrypt later attacks, which post-quantum algorithms address. The other options are unrelated.
</details>

---

### Question 10
**Scenario:** A generative AI application must block harmful content and redact personal data in both prompts and responses with centrally managed policy. Which feature applies?

A. VPC Flow Logs
B. Amazon Bedrock Guardrails
C. AWS WAF rate-based rules
D. Security group rules

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Bedrock Guardrails applies configurable content filters, denied topics and sensitive information handling to inputs and outputs. WAF, security groups and flow logs do not inspect model content.
</details>

---

### Question 11
**Scenario:** Private-subnet workloads transfer 30 TB per month to and from S3 through a NAT gateway, and the NAT data processing charge is the largest networking cost. What is the best reduction?

A. Move the workloads to public subnets so that S3 traffic bypasses the NAT gateway entirely
B. Enable S3 Transfer Acceleration
C. Create an S3 gateway VPC endpoint and route S3 traffic to it
D. Add more NAT gateways

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Gateway endpoints for S3 have no hourly or data processing charge and bypass the NAT gateway. More NAT gateways add cost, and public subnets weaken security.
</details>

---

### Question 12
**Scenario:** Usage of a compute fleet is steady 24/7 at a known baseline, and instance families may change over the next three years. Which purchase option best balances discount and flexibility?

A. Compute Savings Plans for the baseline
B. Spot Instances for all capacity
C. On-Demand for all capacity
D. Standard Reserved Instances for a single instance type

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Compute Savings Plans discount steady usage across instance families. Spot suits interruptible work, On-Demand is the most expensive for steady usage, and Standard RIs lock to a configuration.
</details>

---

### Question 13
**Scenario:** A workload accesses logs unpredictably: some objects are read often, many never. The team does not want to analyze access patterns. Which S3 option minimizes cost with little effort?

A. S3 One Zone-IA for all objects
B. S3 Intelligent-Tiering
C. S3 Standard only
D. A Lifecycle rule moving everything to Glacier after one day

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Intelligent-Tiering moves objects between access tiers automatically as patterns change. The other options either cost more or risk retrieval delays and charges for frequently read data.
</details>

---

### Question 14
**Scenario:** An application needs an RTO of 15 minutes and an RPO of 1 minute. The budget does not allow full production capacity in a second Region. Which strategy fits?

A. Backup and restore
B. Multi-site active/active
C. Pilot light with manual rebuild of compute when a disaster is declared in the second Region
D. Warm standby with continuous data replication

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Warm standby keeps a scaled-down running copy that scales up quickly, meeting a short RTO, and replication meets the RPO. Backup and restore is too slow, active/active exceeds budget, and a manual rebuild may miss the RTO.
</details>

---

### Question 15
**Scenario:** A migration team needs to move a production Oracle database to Amazon Aurora PostgreSQL with minimal downtime, keeping the source and target in sync until cutover. What should they use?

A. AWS DMS with schema conversion and change data capture
B. A nightly mysqldump import
C. Copying EBS snapshots to the target
D. Storage Gateway volume sync

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** DMS provides full load plus ongoing replication for a short cutover, and schema conversion handles the engine change. Snapshots and dumps cannot keep systems in sync or convert engines.
</details>

---

### Question 16
**Scenario:** A company wants backups of critical data that a compromised administrator cannot delete during the retention period. What should be used?

A. Longer snapshot schedules
B. Versioning only
C. AWS Backup Vault Lock (and S3 Object Lock for S3 data)
D. IAM policies denying delete to the administrator, applied through a permission boundary

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Vault Lock and Object Lock enforce write-once retention that privileged users cannot override while the lock applies. An IAM deny can be changed by an administrator.
</details>

---

### Question 17
**Scenario:** A team wants to deploy the same template to 60 accounts across two Regions, including accounts created later in a target OU. Which feature fits?

A. AWS Config conformance packs only
B. CloudFormation StackSets with service-managed permissions and automatic deployment
C. A manual stack in each account
D. A Lambda function that runs on a schedule and copies the template into every account it finds

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** StackSets deploy to many accounts and Regions, and service-managed mode integrates with Organizations to include new accounts. Manual work does not scale.
</details>

---

### Question 18
**Scenario:** A pipeline in a tools account must deploy the same tested artifact to dev, test and production accounts. What is the correct approach?

A. Rebuild the code separately in each account
B. Give developers production credentials
C. Copy the source into each account and build it locally there, so that every environment has its own tested build
D. Promote the same built artifact through environments by assuming a deployment role in each account

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Artifact promotion with role delegation ensures what was tested is what is deployed. Rebuilding can produce different artifacts and direct credentials weaken control.
</details>

---

### Question 19
**Scenario:** An automated remediation Lambda restarts instances when a dependency fails. During a dependency outage it restarts hundreds of instances repeatedly and prolongs the outage. What change adds a safety constraint?

A. Add rate limits and a circuit breaker so remediation stops when failures persist
B. Increase the Lambda memory
C. Remove the alarm
D. Run the Lambda in more Regions so that a single Region outage cannot stop the remediation

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Controlled remediation includes rate limits, circuit breakers and bulkheads so automation cannot amplify an outage. Memory, alarms and Regions do not constrain repeated actions.
</details>

---

### Question 20
**Scenario:** A team wants to know whether real users in different countries see slow page loads, in addition to knowing whether the endpoint is up from a scheduled check. Which combination provides both?

A. GuardDuty for real user page loads and Inspector for scheduled endpoint availability checks
B. VPC Flow Logs only
C. CloudWatch RUM for real users and CloudWatch Synthetics canaries for scheduled checks
D. CloudTrail and AWS Config

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** RUM measures real user sessions; Synthetics runs scripted checks on a schedule. The others address auditing, threat detection or network metadata.
</details>

---
