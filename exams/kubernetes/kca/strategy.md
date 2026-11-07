---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 4 min
---

# KCA Study Strategy

## Follow the weights

| Domain | Weight | Share of study time |
|---|---:|---|
| Writing Policies | 32% | About a third |
| Fundamentals | 18% | A sixth |
| Installation, Configuration, Upgrades | 18% | A sixth |
| Kyverno CLI | 12% | A tenth |
| Applying Policies | 10% | A tenth |
| Policy Management | 10% | A tenth |

## Read the policy, then predict the result

Most knowledge questions about Kyverno come down to reading a short policy and a short resource and saying what happens. Practice that move: for each rule, say which resources `match` selects, whether `exclude` removes any, what the rule body checks, and what the failure action does.

## Distinctions to own

- **Enforce versus Audit**, and that background scans never block.
- **pattern versus deny**: pattern states the good shape, deny states the bad condition.
- **precondition versus deny**: both use conditions, only deny blocks.
- **mutate versus generate**: mutate changes the incoming resource, generate creates other resources.
- **clone versus data**, and what `synchronize` does on each deletion.
- **Admission versus background controller**: live requests versus generate and mutate-existing.
- **Policy versus ClusterPolicy**, and classic versus CEL policy types.

## Expect version drift

The docs are mid-transition from `ClusterPolicy` to CEL policy types. When two pages disagree (the admission replica minimum is two on one page and three on another), learn both and prefer the more specific page.

## Do not over-study

KCA is a beginner-level, knowledge-based exam. You do not need deep Kubernetes internals. You need to read Kyverno YAML fluently and know the install and operations facts in the fact sheet.
