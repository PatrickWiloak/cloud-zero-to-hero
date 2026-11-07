---
last-updated: 2026-11-07
---

# Serverless Explained

> **5-minute read.**

## The one-line answer

"Serverless" means you write code, the cloud provider runs it, and you don't think about servers. You pay per request (or per millisecond of execution), it scales automatically, and it costs zero when nobody's using it.

There are still servers. You just don't manage them.

## Why this exists

Before serverless, even a tiny side project required:

1. Pick an instance size
2. Provision the VM
3. Install runtime, dependencies
4. Set up auto-scaling rules
5. Pay $5-30/month even when idle

For something like "send me an email when this webhook fires" - this was wildly excessive. Serverless took the bet that for many workloads, you don't need to think about any of that.

## How it works

```mermaid
sequenceDiagram
  autonumber
  participant U as User
  participant P as Platform
  participant R as Runtime instance
  U->>P: Request
  alt Cold start (no warm runtime)
    P->>R: Provision micro-VM<br/>load code (~100-500ms)
    R-->>P: Ready
  else Warm (recent traffic)
    P->>R: Reuse existing runtime
  end
  R->>R: Execute your handler
  R-->>P: Response + execution metrics
  P-->>U: Response
  Note over P,R: Bills for execution<br/>time only (1ms increments)
  Note over R: Idle for 5-15 min →<br/>platform tears it down
```

When a request comes in:

1. The platform spins up a small isolated runtime ("container," "micro-VM," whatever)
2. Loads your code
3. Runs it
4. Returns the response
5. Tears down the runtime (or keeps it warm for the next request)

You're billed for the time your code was actually executing - typically in 1ms or 100ms increments - and the memory it used.

If 1,000 requests arrive at once, the platform spins up 1,000 runtimes. If zero requests arrive for an hour, you pay zero.

## The two main flavors

### Functions (FaaS)

A single function, runs in response to an event. Examples:
- AWS Lambda
- Azure Functions
- GCP Cloud Functions
- Cloudflare Workers

Triggers: HTTP request, queue message, file upload, schedule, database change, etc.

Best for: small, focused tasks. Webhook handlers, scheduled jobs, glue between services.

### Container-based serverless

You bring a container, the platform runs it serverlessly. Examples:
- AWS Fargate, App Runner
- Azure Container Apps
- GCP Cloud Run

Best for: full applications. APIs, web apps, anything that fits a container but you don't want to manage Kubernetes.

## A small concrete example

Webhook that posts to Slack when GitHub creates an issue:

**Old way (VM):**
- Provision EC2 t3.micro: ~$8/month
- Install Node, Express
- Manage TLS, deployments, monitoring
- Pay all month for ~12 webhook calls

**Serverless way (Lambda + API Gateway):**
- Write a 20-line function:
  ```js
  exports.handler = async (event) => {
    const issue = JSON.parse(event.body);
    await fetch(SLACK_WEBHOOK, { ... });
    return { statusCode: 200 };
  };
  ```
- Wire it up to API Gateway
- Cost for 12 calls/month: literally pennies

## Tradeoffs

Serverless isn't free magic. The tradeoffs:

### Cold starts
First request after idle = "cold start." Container needs to spin up + load your code. Latency: 100ms-3s depending on platform and runtime.

For most apps, fine. For latency-sensitive (gaming, trading) - watch out.

### Vendor lock-in
Lambda code with Lambda-specific event shapes won't trivially run on Cloud Functions. There are abstractions (Serverless Framework, SST) but it's never zero work.

### Pricing cliff at scale
At low scale, serverless is cheaper than VMs. At very high steady-state load, the per-request cost adds up. There's a crossover point where renting EC2 instances 24/7 is cheaper than paying per Lambda invocation.

Rough rule: if you'd run >2 small instances steady-state, do the math.

### Stateful is awkward
Functions are ephemeral. State has to live in databases, caches, or queues. WebSockets, long-running tasks, big in-memory datasets - awkward to do serverlessly.

### Limits matter
- Max execution time (Lambda: 15min, Cloud Functions: 9min, Workers: 30s CPU)
- Max memory (Lambda: 10GB, Workers: 128MB)
- Max payload size
- Concurrency limits per region

If your workload approaches any limit, evaluate alternatives.

## When to reach for serverless

Good fits:
- HTTP APIs with bursty or low-volume traffic
- Webhooks
- Scheduled jobs (cron replacement)
- Event-driven processing (file uploaded → resize image, message in queue → process)
- "Glue" between services
- Edge logic (Cloudflare Workers for things at the edge)

Bad fits:
- Steady high-throughput workloads (cheaper on VMs/containers)
- Stateful long-running processes (chat servers, game servers)
- Latency-critical (sub-50ms p99) APIs where cold starts hurt
- Anything that needs >10-15min execution time

## "Serverless" databases

The term has spread. "Serverless databases" (DynamoDB on-demand, Aurora Serverless v2, PlanetScale, Neon, Supabase) bring the same idea to data: pay-per-request, scales to zero, no provisioning.

Pair them with serverless compute and you can build entire apps that idle to near-zero cost.

## What to look at next

- **[IaaS vs PaaS vs SaaS](./iaas-paas-saas.md)** - serverless is a flavor of PaaS
- **[Containers vs VMs](./containers-vs-vms.md)** - serverless platforms run on containers under the hood
- **[Glossary: Serverless, Lambda, Cold start](../glossary.md#cloud-fundamentals)**
- **[Service comparison: Serverless](../../resources/service-comparison-serverless.md)**

## Check yourself

Try these before you move on. Each answer is collapsed; click it to check yourself.

1. What are you billed for in a serverless function, and what happens when nobody uses it?

    <details>
    <summary>Answer</summary>
    You are billed for the time your code actually executes (and the memory it uses). If zero requests arrive, you pay zero. See: <a href="#how-it-works">How it works</a>
    </details>

2. What is a cold start?

    <details>
    <summary>Answer</summary>
    The first request after idle, when the platform must spin up a runtime and load your code. Latency is 100ms to 3s depending on platform and runtime. See: <a href="#cold-starts">Cold starts</a>
    </details>

3. Why can serverless become more expensive than VMs at high steady load?

    <details>
    <summary>Answer</summary>
    Per-request cost adds up, and there is a crossover point where renting instances 24/7 is cheaper. The rough rule is to do the math if you would run more than 2 small instances steady-state. See: <a href="#pricing-cliff-at-scale">Pricing cliff at scale</a>
    </details>

4. Why are long-running stateful processes like game servers a bad fit?

    <details>
    <summary>Answer</summary>
    Functions are ephemeral, so state has to live elsewhere, and execution time limits apply. See: <a href="#tradeoffs">Tradeoffs</a>
    </details>
