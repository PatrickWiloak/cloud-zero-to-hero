---
last-updated: 2026-11-07
---

# AWS Certified Solutions Architect - Professional (SAP-C03) Study Strategy

## The shape of the exam

180 minutes for 75 questions (65 scored) is about 2.4 minutes per question. Questions are long scenarios, some with multiple responses where you must select all correct choices (no partial credit). Unanswered questions score as incorrect and there is no guessing penalty, so always answer. The exam is compensatory: you do not need to pass each domain, only the whole.

## Weight your time

| Domain | Weight |
|--------|--------|
| 1. Architecture Design and Implementation Built for the Cloud | 25% |
| 2. Security, Compliance, and Governance | 25% |
| 5. Operational Excellence and Automation | 20% |
| 3. Cost-Optimized Architecture Design | 15% |
| 4. Resilience, Migration, and Business Continuity | 15% |

## Answering scenario questions

1. **Read the last sentence first.** It states what is being asked ("most cost-effective", "least operational overhead", "meets the RTO").
2. **Underline the constraints:** existing investments, deadlines, compliance, team skills, latency, budget.
3. **Eliminate options that break a constraint** before comparing the rest. A technically correct answer that needs a rewrite fails a "minimal changes" constraint.
4. **Prefer managed and native** when the question stresses operational overhead; prefer the most specific service over a generic build.
5. **For multiple response,** verify that each selected option is correct on its own and that together they meet the requirement.

## Pitfalls specific to C03

- AI/ML items test design (which service, which guardrail, how to monitor), not model training.
- Governance questions expect you to know that SCPs, RCPs and permissions boundaries limit but never grant.
- Cost questions often hide the answer in data transfer (NAT gateway processing, cross-Region replication) or in a purchase option mismatch.
- DR questions are RTO/RPO matching exercises: pick the cheapest strategy that meets both.
- Services removed from C03 scope (for example IoT, Amplify, Service Catalog) should not take study time.

## Resources

- [Notes](README.md#notes-study-order) and [Fact Sheet](fact-sheet.md)
- [Practice Questions](../../../../resources/practice-questions/aws-solutions-architect-professional-sap-c03.md)
- **[📖 SAP-C03 Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-03/solutions-architect-professional-03.html)** - Official outline
