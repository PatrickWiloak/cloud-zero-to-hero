---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 5 min
---

# Kyverno Certified Associate (KCA)

The CNCF and Linux Foundation certification for Kyverno, the Kubernetes-native policy engine. KCA covers what Kyverno is, how to install and run it, the CLI, and above all how to write validate, mutate, generate and image-verification policies.

Kyverno is a good first policy engine because its policies are plain Kubernetes YAML. Knowing it gives you the vocabulary (admission, audit versus enforce, exceptions, reports) that transfers to OPA Gatekeeper and to Kubernetes' own ValidatingAdmissionPolicy.

## Exam Details (checked 2026-11-07)

- **Exam Code:** KCA (the page uses it as the purchase SKU)
- **Duration:** 90 minutes
- **Questions:** Not stated on the page
- **Passing Score:** Not stated on the page
- **Cost:** USD 250 exam only, USD 495 with the THRIVE-ONE annual subscription (as listed on 2026-11-07)
- **Validity:** 2 years
- **Prerequisites:** None; the page lists the experience level as Beginner
- **Format:** Online, proctored, multiple choice

Full detail and sources in the [fact sheet](./fact-sheet.md).

## Domains

| Domain | Weight | Notes |
|--------|-------:|-------|
| Fundamentals of Kyverno | 18% | [01](./notes/01-fundamentals-of-kyverno.md) |
| Installation, Configuration, and Upgrades | 18% | [02](./notes/02-installation-configuration-upgrades.md) |
| Kyverno CLI | 12% | [03](./notes/03-kyverno-cli.md) |
| Applying Policies | 10% | [04](./notes/04-applying-policies.md) |
| Writing Policies | 32% | [05](./notes/05-writing-policies.md) |
| Policy Management | 10% | [06](./notes/06-policy-management.md) |

Writing Policies is a third of the exam. Add Installation and Fundamentals and you are at two thirds.

## A version warning

The Kyverno documentation read on 2026-11-07 marks `ClusterPolicy`, `Policy`, `CleanupPolicy` and the legacy `PolicyException` as deprecated as of v1.19, with removal planned for v1.20, in favor of CEL-based types (`ValidatingPolicy`, `MutatingPolicy`, `ImageValidatingPolicy`, `DeletingPolicy`). The curriculum still lists classic topics such as preconditions, autogen and JSON patches beside CEL. These notes teach both. Confirm the Kyverno version the exam targets before you rely on one style.

## Study sequence

1. Fundamentals: policy, rule, admission, Audit versus Enforce.
2. Writing policies: validate first, then mutate, generate, verifyImages.
3. Installation, HA and RBAC.
4. CLI: `apply`, `test`, `jp`.
5. Reports, exceptions, metrics.

Schedule in the [practice plan](./practice-plan.md).

## Study resources

- **[📖 Kyverno documentation](https://kyverno.io/docs/)** - the primary source
- **[📖 KCA curriculum](https://github.com/cncf/curriculum)** - the CNCF curriculum repo with `KCA_Curriculum.pdf`
- **[📖 Linux Foundation KCA page](https://training.linuxfoundation.org/certification/kyverno-certified-associate-kca/)** - registration and logistics
- [Practice questions](../../../resources/practice-questions/cncf-kca.md) - 32 original questions in this repo

## Related

- [CKA](../cka/) - the Kubernetes administration skills Kyverno builds on
- [CNPA Platform Engineering Associate](../cnpa/) - platform guardrails in context
- [CGOA GitOps Associate](../cgoa/) - policies are managed as code in Git
- [Kubernetes topic](../../../topics/kubernetes.md)
