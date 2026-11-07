---
last-updated: 2026-11-07
difficulty: beginner
reading-time: 7 min
---

# Autoscaling Explained

> **7-minute read. Assumes you've read [Load balancing explained](./load-balancing-explained.md).**

## The one-line answer

Autoscaling adds capacity when demand rises and removes it when demand falls, so you pay for roughly what you use instead of permanently paying for your busiest hour.

It is the feature people cite as the reason to move to cloud, and it is also the feature most commonly misconfigured, because scaling *up* is easy and scaling *safely* is not.

## Horizontal and vertical

**Vertical scaling** makes an instance bigger: more CPU, more memory. Simple, and usually requires a restart, so it is rarely automatic for stateful systems. There is also a ceiling: the largest instance available.

**Horizontal scaling** adds more instances. No ceiling in practice, no restart, and it requires the application to be **stateless**, because any instance must be able to handle any request.

Almost all cloud autoscaling means horizontal scaling. The main exception is Kubernetes' Vertical Pod Autoscaler, which right-sizes a workload's resource requests.

## What to scale on

The metric you choose determines whether autoscaling actually helps.

| Metric | Good for | Watch out |
|---|---|---|
| **CPU utilization** | CPU-bound work | Useless for I/O-bound services that sit at 15% CPU while overwhelmed |
| **Memory** | Memory-bound workloads | Memory rarely falls, so scale-in may never trigger |
| **Request rate** | Predictable per-request cost | Breaks when request cost varies widely |
| **Concurrency / in-flight requests** | Most web services | Usually the best proxy for "is it struggling" |
| **Queue depth** | Worker pools | The single best signal for asynchronous work |
| **Custom business metric** | Anything else | Needs a metrics pipeline that stays reliable |

The most common mistake is scaling a queue-backed worker fleet on CPU. Workers waiting on a slow downstream API show low CPU while the backlog grows for hours. **Queue depth** or **message age** is the correct signal.

## The shape of a scaling policy

Four numbers matter more than the algorithm:

- **Minimum instances.** Never zero for latency-sensitive services, or the first user after a quiet period waits for a cold start.
- **Maximum instances.** The cost ceiling and the blast radius limit. Set it deliberately; an unbounded maximum plus a retry storm is an expensive outage.
- **Target value.** Aim below saturation, typically 60-70% CPU rather than 90%, because you need headroom while new capacity starts.
- **Cooldown / stabilization window.** How long to wait before acting again, which prevents flapping.

**Scale out fast, scale in slowly.** Adding capacity you turn out not to need costs a little money. Removing capacity you did need costs an outage. Most sensible configurations are aggressive on scale-out and conservative on scale-in.

## Reactive, scheduled, and predictive

**Reactive** scaling responds to current metrics. It always lags, because it can only react after load has already risen and new instances take time to become useful.

**Scheduled** scaling changes capacity at known times: a batch window, market open, a marketing campaign, a nightly job. When you know the pattern, this beats reactive scaling because it removes the lag entirely.

**Predictive** scaling uses historical patterns to provision ahead of expected demand. Useful for strongly cyclical workloads.

Real systems combine them: a schedule for the known daily shape, reactive policies for the unexpected.

## The startup time problem

Autoscaling only helps if new capacity becomes useful faster than load grows. Total time to useful includes: the scaling decision, instance or container provisioning, application start, dependency connections and cache warm-up, and passing the health check.

If that adds up to five minutes and your traffic doubles in two, autoscaling will not save you. The fixes are all about reducing the number:

- Smaller images and faster application startup
- Pre-warmed pools or a higher minimum
- Provisioned concurrency for serverless
- Cluster overprovisioning in Kubernetes, keeping spare capacity so pods schedule immediately

## Kubernetes specifics

Three autoscalers, addressing different layers:

- **Horizontal Pod Autoscaler (HPA)** changes the number of pod replicas based on metrics.
- **Vertical Pod Autoscaler (VPA)** changes a pod's CPU and memory requests. Do not run it on the same workload as HPA for the same metric; they fight.
- **Cluster Autoscaler** (or Karpenter) adds and removes **nodes** when pods cannot be scheduled.

They compose: HPA adds pods, pods go Pending because no node has room, Cluster Autoscaler adds a node. If you have only HPA and no node autoscaling, scaling silently stops at the cluster's existing capacity.

Note that declaring `replicas` in a manifest managed by GitOps while an HPA manages the same field causes a fight loop. Remove the field or exclude it from reconciliation.

## Serverless

With functions and scale-to-zero container platforms, scaling is the platform's job: concurrency drives instance count automatically, and idle costs nothing.

The trade-offs move rather than disappear: **cold starts** on the first request after idle, **concurrency limits** per account or region, and **downstream pressure**, because a function fleet that scales to a thousand instances can exhaust a database connection pool that was sized for ten.

That last point is the one that bites. Autoscaling the compute tier without considering what it calls simply moves the bottleneck, and often turns a slow service into a failed database.

## Common mistakes

- **Scaling workers on CPU instead of queue depth.**
- **No maximum**, so a retry storm scales into a very large bill.
- **Minimum of zero** on a latency-sensitive service.
- **Target set at 90%**, leaving no headroom while new capacity starts.
- **Aggressive scale-in**, causing capacity to be removed just before the next spike.
- **Forgetting the database.** More application instances means more connections; use a connection pooler.
- **Stateful instances**, where removing one loses in-memory sessions.
- **Never testing it.** Load test the scaling behavior, not just the steady state.

## What to look at next

- **[Load balancing explained](./load-balancing-explained.md)** - what distributes traffic to the instances you added
- **[Serverless explained](./serverless-explained.md)** - where scaling is the platform's problem
- **[Kubernetes in 10 minutes](./kubernetes-in-10-minutes.md)** - the three autoscalers in context
- **[Queues vs streams](https://data.noblerworks.com/learn/concepts/queues-vs-streams/)** - where queue depth as a scaling signal comes from
- **[Cloud cost basics](./cloud-cost-basics.md)** - the bill autoscaling is meant to control

## Check yourself

Try these before you move on. Each answer is collapsed; click it to check yourself.

1. Why is CPU a poor scaling signal for a queue-backed worker fleet, and what is a better one?

   <details markdown="1">
   <summary>Answer</summary>

   Workers waiting on a slow downstream API show low CPU while the backlog grows for hours. Queue depth or message age is the correct signal. See: [What to scale on](#what-to-scale-on)

   </details>

2. Why aim for a target of 60-70% CPU instead of 90%?

   <details markdown="1">
   <summary>Answer</summary>

   You need headroom while new capacity is starting up. A 90% target leaves none. See: [The shape of a scaling policy](#the-shape-of-a-scaling-policy)

   </details>

3. A cluster has an HPA but no node autoscaling. What happens when load keeps rising?

   <details markdown="1">
   <summary>Answer</summary>

   The HPA adds pods, but they go Pending when no node has room, so scaling silently stops at the cluster's existing capacity. See: [Kubernetes specifics](#kubernetes-specifics)

   </details>

4. Why scale out fast and scale in slowly?

   <details markdown="1">
   <summary>Answer</summary>

   Adding capacity you did not need costs a little money, while removing capacity you did need costs an outage. See: [The shape of a scaling policy](#the-shape-of-a-scaling-policy)

   </details>
