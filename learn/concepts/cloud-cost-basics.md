---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 8 min
---

# Cloud Cost Basics

> **8-minute read. Assumes you've read [What is cloud computing?](./what-is-cloud-computing.md).**

## The one-line answer

Cloud turns a capital purchase into a per-second rental, which is enormously flexible and means your bill is now a direct consequence of engineering decisions made by people who never see it.

## What you actually pay for

Almost every cloud bill decomposes into the same five things:

| Dimension | Charged on | Notes |
|---|---|---|
| **Compute** | Instance size multiplied by time it exists | Runs whether or not it is doing anything |
| **Storage** | Gigabytes stored per month | Cheap per GB, and it accumulates forever unless something deletes it |
| **Network egress** | Data leaving the provider or crossing regions | Ingress is usually free; egress is where surprises live |
| **Requests and operations** | Per API call, per million | Individually trivial, occasionally enormous at scale |
| **Managed service premium** | The convenience of not operating it yourself | A managed database costs more than the VM it replaces, and less than the engineer |

The most common surprise on a first serious bill is **egress**, because nothing in a local development environment charges for network traffic and nothing warns you.

## Why bills grow without anyone deciding to spend more

- **Nothing turns itself off.** A development environment left running over a weekend costs the same as production traffic.
- **Storage never shrinks.** Snapshots, old backups, logs at debug level, and orphaned volumes accumulate silently.
- **Autoscaling has no ceiling by default.** A retry storm can scale a fleet into a very large number.
- **Cross-zone and cross-region traffic** is charged, and a chatty microservice architecture spread across zones pays for every internal hop.
- **Idle managed services** still bill: a provisioned database at 2% utilization costs the same as at 80%.
- **Logs and metrics** are charged per GB ingested, and verbose logging at scale can rival compute cost.

## The pricing models

| Model | Discount | Commitment | Fits |
|---|---|---|---|
| **On demand** | None | None | Unpredictable or short-lived workloads |
| **Spot / preemptible** | Very large, often 60-90% | Can be reclaimed with little notice | Fault-tolerant batch, CI, stateless workers |
| **Reserved instances / committed use** | Substantial | 1 or 3 years | Steady baseline load |
| **Savings plans** | Substantial | Spend commitment, flexible across services | Steady spend with changing shape |

The practical pattern: cover your **steady baseline** with a commitment, handle **variable load** on demand, and run **interruptible work** on spot. Committing to your peak wastes money; committing to nothing leaves a large discount unclaimed.

## The levers that actually move a bill

In rough order of impact per unit of effort:

1. **Turn things off.** Non-production environments outside working hours. Frequently 20-30% of a bill with no performance consequence.
2. **Right-size.** Instances are routinely provisioned for a peak that never arrives. Check actual utilization before renewing anything.
3. **Fix storage lifecycle.** Move old objects to cheaper tiers automatically, expire what nobody reads, and delete orphaned volumes and snapshots.
4. **Commit to the baseline.** Once your steady-state usage is understood, a commitment is a discount for work you were going to do anyway.
5. **Reduce egress.** Keep chatty services in the same zone, cache at the edge, and compress.
6. **Trim observability.** Sample traces, filter debug logs before ingestion, tier retention.
7. **Adopt spot** for anything that tolerates interruption.

Notice that the first three cost nothing and require no architectural change.

## Making cost visible

You cannot manage what nobody can see.

**Tagging** is the foundation: every resource labeled with an owner, environment, and cost center. Untagged resources become unattributable spend that nobody feels responsible for, and retroactive tagging is painful, so enforce it at creation with policy.

**Showback** reports each team's spend without billing them. **Chargeback** actually bills them. Showback changes behavior in most organizations; chargeback is heavier and worth it only where the organization genuinely wants teams to feel the price.

**Budgets and alerts** are the cheapest safety net there is. Set them low enough to be noticed, on every account, on the day the account is created.

**Anomaly detection** catches the shape of problem a fixed threshold misses: a service that doubles its spend while remaining under budget.

## Unit economics

A total bill going up is not automatically bad. A bill going up while serving twice the traffic is efficiency improving.

The measure worth tracking is **cost per unit of business value**: cost per order, per active user, per thousand requests, per model inference. It converts a finance conversation into an engineering one and reveals whether growth is profitable.

## Architecture decisions that determine cost

Most of a bill is decided by design, not by procurement:

- **Serverless versus always-on**: scale-to-zero is dramatically cheaper for spiky or low-volume workloads and more expensive at sustained high volume
- **Data locality**: keeping compute next to data avoids cross-region egress entirely
- **Storage tiering**: hot, infrequent access, and archive tiers differ by an order of magnitude
- **Instance family**: ARM-based instances often cost less for the same throughput
- **Multi-region**: doubles a lot of cost, and is sometimes required by the availability target and sometimes just assumed

## FinOps in one paragraph

FinOps is the practice of making cost a shared engineering responsibility rather than a finance report. Three phases repeat: **inform** (visibility, tagging, allocation), **optimize** (right-size, commit, eliminate waste), and **operate** (governance, budgets, continuous improvement). The cultural point is that the people who create cost are the people who can reduce it.

## What to look at next

- **[Autoscaling explained](./autoscaling-explained.md)** - the mechanism that most directly drives compute cost
- **[Serverless explained](./serverless-explained.md)** - the scale-to-zero cost model
- **[Regions and availability zones](./regions-and-availability-zones.md)** - where egress charges come from
- **[FinOps principles](../../resources/cost-optimization/finops-principles.md)** - the practice in depth
- **[FinOps topic](../../topics/finops.md)** - everything in the repo on this subject
- **[AWS](../../resources/cost-optimization/aws-cost-optimization.md)**, **[Azure](../../resources/cost-optimization/azure-cost-optimization.md)**, **[GCP](../../resources/cost-optimization/gcp-cost-optimization.md)** cost guides

## Check yourself

Try these before you move on. Each answer is collapsed; click it to check yourself.

1. Name the five things almost every cloud bill breaks down into.

   <details markdown="1">
   <summary>Answer</summary>

   Compute, storage, network egress, requests and operations, and the managed service premium. See: [What you actually pay for](#what-you-actually-pay-for)

   </details>

2. Why is egress the most common surprise on a first serious bill?

   <details markdown="1">
   <summary>Answer</summary>

   Nothing in a local development environment charges for network traffic and nothing warns you. See: [What you actually pay for](#what-you-actually-pay-for)

   </details>

3. Which pricing model fits a steady baseline, and which fits fault-tolerant batch work?

   <details markdown="1">
   <summary>Answer</summary>

   Reserved instances or committed use (or savings plans) fit the steady baseline. Spot or preemptible fits fault-tolerant batch work, because it can be reclaimed with little notice. See: [The pricing models](#the-pricing-models)

   </details>

4. Why does the page say that a rising total bill is not automatically bad?

   <details markdown="1">
   <summary>Answer</summary>

   If the bill rises while serving twice the traffic, efficiency is improving. Cost per unit of business value, such as cost per order, is the measure to track. See: [Unit economics](#unit-economics)

   </details>
