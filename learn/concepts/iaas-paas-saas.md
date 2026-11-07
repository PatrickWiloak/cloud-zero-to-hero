---
last-updated: 2026-11-07
---

# IaaS vs PaaS vs SaaS

> **5-minute read.**

## The one-line answer

Three flavors of cloud service, sorted by how much the provider does for you:

- [**IaaS**](../glossary.md#term-iaas-infrastructure-as-a-service) - rent the building blocks (servers, disks, networks). You set everything up.
- [**PaaS**](../glossary.md#term-paas-platform-as-a-service) - rent the platform. You bring code; the provider runs it.
- [**SaaS**](../glossary.md#term-saas-software-as-a-service) - rent the finished software. You just log in and use it.

## The pizza analogy

The classic visualization:

| You eat... | Make from scratch | Take and bake | Delivery | Dine in |
|-----------|-------------------|---------------|----------|---------|
| Dough     | You               | Provider      | Provider | Provider |
| Sauce     | You               | Provider      | Provider | Provider |
| Toppings  | You               | Provider      | Provider | Provider |
| Oven      | You               | You           | Provider | Provider |
| Plates    | You               | You           | You      | Provider |
| Table     | You               | You           | You      | Provider |
|           | **On-prem**       | [**IaaS**](../glossary.md#term-iaas-infrastructure-as-a-service)      | [**PaaS**](../glossary.md#term-paas-platform-as-a-service) | [**SaaS**](../glossary.md#term-saas-software-as-a-service) |

```mermaid
flowchart TB
  subgraph ONP[On-prem]
    O1[App + data]:::you
    O2[Runtime]:::you
    O3[OS]:::you
    O4[Hypervisor]:::you
    O5[Hardware]:::you
    O6[Datacenter]:::you
  end
  subgraph IAAS[IaaS]
    I1[App + data]:::you
    I2[Runtime]:::you
    I3[OS]:::you
    I4[Hypervisor]:::them
    I5[Hardware]:::them
    I6[Datacenter]:::them
  end
  subgraph PAAS[PaaS]
    P1[App + data]:::you
    P2[Runtime]:::them
    P3[OS]:::them
    P4[Hypervisor]:::them
    P5[Hardware]:::them
    P6[Datacenter]:::them
  end
  subgraph SAAS[SaaS]
    S1[Your data + config]:::you
    S2[App]:::them
    S3[Runtime]:::them
    S4[OS]:::them
    S5[Hypervisor]:::them
    S6[Hardware]:::them
  end
  classDef you fill:#ffd,stroke:#aa0
  classDef them fill:#dde,stroke:#33a
```

Yellow = your responsibility. Blue = provider's. The further right you go, the less you manage - but the less you control.

## IaaS - Infrastructure as a Service

**You get:** virtual machines, virtual disks, virtual networks. Raw building blocks.

**You manage:** OS patches, the runtime, your application, scaling, monitoring.

**Provider manages:** the physical hardware, hypervisor, datacenter, networking fabric.

**Examples:**
- AWS EC2, EBS, VPC
- Azure VMs, Managed Disks, Virtual Networks
- GCP Compute Engine, Persistent Disks, VPC

**Use when:**
- You want maximum control
- You're lifting-and-shifting an existing app
- You have specific OS / kernel / driver requirements
- You're running something the PaaS layer doesn't support

## PaaS - Platform as a Service

**You get:** a platform that runs your code. You hand it a container, a Java app, a Node.js project, etc., and it figures out the rest.

**You manage:** your code and configuration.

**Provider manages:** OS patching, runtime upgrades, scaling, load balancing, sometimes the database.

**Examples:**
- AWS App Runner, Elastic Beanstalk, Lambda (also serverless)
- Azure App Service, Container Apps
- GCP App Engine, Cloud Run
- Heroku (the OG PaaS)
- Vercel, Netlify, Render, Railway

**Use when:**
- You want to ship fast, not manage servers
- Your app fits a standard runtime (web app, API, function)
- You're a small team without ops bandwidth

## SaaS - Software as a Service

**You get:** finished software, accessed through a browser or API.

**You manage:** your own data and users inside it.

**Provider manages:** literally everything else.

**Examples:**
- Gmail, Slack, Notion, Salesforce, GitHub, Figma
- DataDog (monitoring), Auth0 (authentication), Stripe (payments)

**Use when:**
- The problem is already solved by software someone built
- You'd rather pay $X/month than build and maintain it
- (i.e. 99% of business software needs)

## Where serverless fits

"Serverless" is fuzzy - it's marketing-speak that overlaps PaaS. The defining traits:

- You don't think about servers (the platform handles compute capacity)
- You pay per request or per millisecond, not per hour
- It scales to zero when idle (no idle cost)

Serverless examples: AWS Lambda, Azure Functions, GCP Cloud Run, Cloudflare Workers.

It's basically "PaaS with very fine-grained billing." Some people call it FaaS (Function as a Service) when it's specifically functions.

## A real-world stack

A typical modern startup:

| Layer | Choice | Type |
|-------|--------|------|
| User-facing app | Vercel hosting Next.js | PaaS |
| Backend API | AWS Lambda | Serverless / PaaS |
| Database | Supabase or Neon Postgres | SaaS / DBaaS |
| Auth | Clerk or Auth0 | SaaS |
| Email | Postmark or Resend | SaaS |
| Payments | Stripe | SaaS |
| Analytics | PostHog or Mixpanel | SaaS |
| Errors | Sentry | SaaS |
| ML | OpenAI or Anthropic API | SaaS |

Notice: barely any IaaS. A modern small team can build serious products without ever provisioning a VM.

When does IaaS still come up?
- Specialized workloads (GPU training, custom networking, regulated environments)
- Very high scale where managed services are too expensive
- Self-hosting because you want control of data / cost / latency

## What to look at next

- **[Serverless explained](./serverless-explained.md)** - the most common modern PaaS pattern
- **[Containers vs VMs](./containers-vs-vms.md)** - the unit IaaS and PaaS run
- **[Shared responsibility model](https://security.noblerworks.com/learn/concepts/shared-responsibility-model/)** - whose job is security at each layer
- **[Glossary: IaaS, PaaS, SaaS](../glossary.md#cloud-fundamentals)**

## Check yourself

Try these before you move on. Each answer is collapsed; click it to check yourself.

1. In IaaS, what do you manage and what does the provider manage?

   <details markdown="1">
   <summary>Answer</summary>

   You manage the OS patches, runtime, application, scaling and monitoring. The provider manages the physical hardware, hypervisor, datacenter and networking fabric. See: [IaaS - Infrastructure as a Service](#iaas---infrastructure-as-a-service)

   </details>

2. Which of IaaS, PaaS and SaaS fits a small team without ops bandwidth that wants to ship code fast?

   <details markdown="1">
   <summary>Answer</summary>

   PaaS, because you hand over code and the provider handles OS patching, runtime upgrades, scaling and load balancing. See: [PaaS - Platform as a Service](#paas---platform-as-a-service)

   </details>

3. What are the defining traits of serverless?

   <details markdown="1">
   <summary>Answer</summary>

   You do not think about servers, you pay per request or per millisecond, and it scales to zero when idle. See: [Where serverless fits](#where-serverless-fits)

   </details>

4. Why does the modern startup stack in the page contain barely any IaaS?

   <details markdown="1">
   <summary>Answer</summary>

   Most layers (auth, email, payments, database and so on) are available as SaaS or PaaS, so a small team can build serious products without ever provisioning a VM. See: [A real-world stack](#a-real-world-stack)

   </details>
