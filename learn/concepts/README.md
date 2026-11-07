# 💡 Concepts - Bite-Size Topic Pages

> **Single-topic explanations. 5-10 minute reads. No exam scaffolding.**
>
> Read one when you keep seeing a term and want to actually understand it.

---

## How these are organized

Each page covers one concept:
- What it is, in plain English
- Why it exists (the problem it solves)
- A small concrete example
- What to look at next

These are not exam-objective summaries. They're "explain it like I'm a smart engineer who just hasn't been exposed to this yet."

If you want exam coverage, head back to the [Study Hub](../../STUDY-HUB.md).

**Brand new to all of this?** Start with **[Day One](../day-one/)** - terminal, git, HTTP, and servers - then come back here once that vocabulary feels familiar.

**Want a curated path through these?** Try **[Cloud from Scratch](../cloud-from-scratch.md)** or **[AI from Scratch](https://ai.noblerworks.com/learn/start-here/zero-to-hero-path/)**, which order the concepts into 8-phase paths.

**Want them grouped by subject across the whole repo?** See the **[topic indexes](../../topics/)**.

---

## ☁️ Cloud Computing

| Topic | Read when... |
|-------|--------------|
| [What is cloud computing?](./what-is-cloud-computing.md) | You want the foundational mental model |
| [IaaS vs PaaS vs SaaS](./iaas-paas-saas.md) | The three terms keep coming up |
| [Regions and availability zones](./regions-and-availability-zones.md) | You're asking "where does my code actually run?" |
| [Shared responsibility model](https://security.noblerworks.com/learn/concepts/shared-responsibility-model/) | You're wondering "what's AWS's job vs mine?" |
| [VPC explained](./vpc-explained.md) | Networking inside the cloud confuses you |
| [Object, block, and file storage](./object-block-file-storage.md) | You can't tell when to use S3 vs EBS vs EFS |
| [IAM explained](https://security.noblerworks.com/learn/concepts/iam-explained/) | "Roles vs policies vs federation" is fuzzy |
| [Cloud identity basics for builders](./cloud-identity-basics-for-builders.md) | Your code needs cloud credentials and you don't want to paste an access key |
| [Serverless explained](./serverless-explained.md) | You keep hearing "serverless" without a clear definition |
| [CDN explained](./cdn-explained.md) | You see CloudFront/CloudFlare/Akamai and wonder what they do |
| [Caching explained](./caching-explained.md) | You want to know why caches are fast and why they lie |
| [Load balancing explained](./load-balancing-explained.md) | "Layer 4 vs layer 7" keeps coming up and you want specifics |
| [Autoscaling explained](./autoscaling-explained.md) | You want capacity to follow demand without an outage |
| [High availability and fault tolerance](./high-availability-and-fault-tolerance.md) | You want to know what "four nines" costs and where the single points of failure hide |
| [Disaster recovery: RPO and RTO](./disaster-recovery-rpo-rto.md) | Someone asked "how much data can we lose?" and nobody had a number |
| [API gateways explained](./api-gateways-explained.md) | You're deciding between a load balancer and an API gateway |
| [Managed databases explained](./managed-databases-explained.md) | You're weighing RDS or Cloud SQL against running the database yourself |
| [Edge computing explained](./edge-computing-explained.md) | "Run it at the edge" keeps coming up and you want to know where the edge is |
| [WebAssembly at the edge](./webassembly-at-the-edge.md) | Someone said "Wasm" about edge functions and you want the gist |
| [Multi-account strategy and landing zones](./multi-account-and-landing-zones.md) | One account has stopped being enough |
| [Well-Architected explained](./well-architected-explained.md) | You want the shared checklist behind every provider's architecture advice |
| [Cloud cost basics](./cloud-cost-basics.md) | The bill went up and nobody decided to spend more |

## ☸️ Containers and Orchestration

| Topic | Read when... |
|-------|--------------|
| [Containers vs VMs](./containers-vs-vms.md) | You don't know why containers replaced VMs |
| [Kubernetes in 10 minutes](./kubernetes-in-10-minutes.md) | Everyone uses K8s; you want to know why |
| [Service mesh explained](./service-mesh-explained.md) | Istio or Linkerd came up and you want to know if you need one |

## 🛠️ DevOps / Infrastructure

| Topic | Read when... |
|-------|--------------|
| [Terraform explained](./terraform-explained.md) | You want to understand IaC without diving into HCL |
| [Infrastructure as Code explained](./infrastructure-as-code-explained.md) | You want the tool-neutral idea: declarative vs imperative, state, drift |
| [GitOps explained](./gitops-explained.md) | You want to deploy by merging a pull request |
| [Platform engineering explained](./platform-engineering-explained.md) | "Internal developer platform" and "golden paths" need a plain answer |
| [Backstage and developer portals](./backstage-and-developer-portals.md) | You keep hearing "developer portal" next to "platform" |
| [eBPF explained](./ebpf-explained.md) | Cilium, "sidecar-free" and kernel-level tracing keep coming up |
| [OpenTofu vs Terraform](./opentofu-vs-terraform.md) | You need to know why there are two and which to use |
| [Service quotas and limits](./service-quotas-and-limits.md) | A launch failed with a limit error and you want to avoid a repeat |
| [CI/CD explained](./cicd-explained.md) | "Pipelines" is hand-waved everywhere; you want specifics |
| [Observability basics](./observability-basics.md) | "Logs vs metrics vs traces" needs a one-page answer |
| [Idempotency explained](./idempotency-explained.md) | You're worried about retries doing things twice |
| [Eventual consistency](https://data.noblerworks.com/learn/concepts/eventual-consistency/) | A read returned stale data and you want to know why |
| [Queues vs streams](https://data.noblerworks.com/learn/concepts/queues-vs-streams/) | You can't pick between SQS and Kinesis |
| [Message queues and pub/sub](./message-queues-and-pub-sub-for-cloud.md) | You want to decouple services with SQS, Service Bus or Pub/Sub |
| [Deployment strategies](./deployment-strategies.md) | Rolling, blue-green, canary: which and when |

## 🗄️ Data and Databases

| Topic | Read when... |
|-------|--------------|
| [SQL vs NoSQL](https://data.noblerworks.com/learn/concepts/sql-vs-nosql/) | You're choosing a database and the options blur together |
| [Managed databases explained](./managed-databases-explained.md) | You want the cloud provider to run the database for you |
| [Eventual consistency](https://data.noblerworks.com/learn/concepts/eventual-consistency/) | A read returned stale data and you want to know why |
| [Caching explained](./caching-explained.md) | You want to know why caches are fast and why they lie |
| [Warehouses, lakes, and lakehouses](https://data.noblerworks.com/learn/concepts/warehouses-lakes-lakehouses/) | Someone said "lakehouse" and you nodded |
| [ETL vs ELT](https://data.noblerworks.com/learn/concepts/etl-vs-elt/) | You want to know why the transform moved after the load |
| [Batch vs streaming](https://data.noblerworks.com/learn/concepts/batch-vs-streaming/) | You're deciding whether a pipeline needs to be real-time |
| [Data modeling for analytics](https://data.noblerworks.com/learn/concepts/data-modeling-for-analytics/) | A report double-counted and you need to know how |
| [File formats and partitioning](https://data.noblerworks.com/learn/concepts/file-formats-and-partitioning/) | A query is slow or a warehouse bill is high |
| [Data pipelines and orchestration](https://data.noblerworks.com/learn/concepts/data-pipelines-and-orchestration/) | Your cron jobs have started depending on each other |
| [Data quality and lineage](https://data.noblerworks.com/learn/concepts/data-quality-and-lineage/) | A dashboard showed a wrong number and nothing errored |

## 🌐 Networking and Security

| Topic | Read when... |
|-------|--------------|
| [DNS explained](./dns-explained.md) | You want to understand how the internet finds things |
| [TLS and HTTPS](https://security.noblerworks.com/learn/concepts/tls-and-https/) | You want to know what the lock icon actually means |
| [Secrets management](https://security.noblerworks.com/learn/concepts/secrets-management/) | You need credentials in an app without leaving copies everywhere |

## 🤖 AI / Machine Learning - foundations

| Topic | Read when... |
|-------|--------------|
| [LLM basics](https://ai.noblerworks.com/learn/concepts/llm-basics/) | You want to understand what a language model actually does |
| [Transformer architecture](https://ai.noblerworks.com/learn/concepts/transformer-architecture/) | You're ready to look inside the model |
| [Embeddings and vector search](https://ai.noblerworks.com/learn/concepts/embeddings-and-vector-search/) | You want to understand semantic search |
| [Context windows and management](https://ai.noblerworks.com/learn/concepts/context-windows-and-management/) | You're hitting token limits in production |
| [Multimodal models](https://ai.noblerworks.com/learn/concepts/multimodal-models/) | You want to use images / audio / video in prompts |

## 🤖 AI / Machine Learning - building with LLMs

| Topic | Read when... |
|-------|--------------|
| [Prompt engineering](https://ai.noblerworks.com/learn/concepts/prompt-engineering/) | You want to write prompts that actually work |
| [Tool use and function calling](https://ai.noblerworks.com/learn/concepts/tool-use-and-function-calling/) | You want the model to call your code |
| [MCP explained](https://ai.noblerworks.com/learn/concepts/mcp-explained/) | "Model Context Protocol" keeps coming up |
| [Structured outputs](https://ai.noblerworks.com/learn/concepts/structured-outputs/) | You want guaranteed-valid JSON from the model |
| [RAG explained](https://ai.noblerworks.com/learn/concepts/rag-explained/) | "Retrieval-augmented generation" is everywhere |
| [Fine-tuning vs RAG](https://ai.noblerworks.com/learn/concepts/fine-tuning-vs-rag/) | You want to know which one to reach for |
| [AI agents explained](https://ai.noblerworks.com/learn/concepts/agents-explained/) | You're trying to figure out what "agent" really means |
| [Agentic loops](https://ai.noblerworks.com/learn/concepts/agentic-loops/) | You want the deep-dive on the loop, not just the concept |
| [Prompt caching](https://ai.noblerworks.com/learn/concepts/prompt-caching/) | Your input costs are higher than they should be |

## 🤖 AI / Machine Learning - operations

| Topic | Read when... |
|-------|--------------|
| [Evals for LLMs](https://ai.noblerworks.com/learn/concepts/evals-for-llms/) | You're shipping LLM features and wondering how to test them |
| [Guardrails and safety](https://ai.noblerworks.com/learn/concepts/guardrails-and-safety/) | You're worried about prompt injection or unsafe output |
| [Prompt injection explained](https://ai.noblerworks.com/safety/security/prompt-injection-explained/) | You want to know why prompt injection has no clean fix |
| [AI threat modeling](https://ai.noblerworks.com/safety/security/ai-threat-modeling/) | You're designing an AI feature and want to find the risk early |
| [Inference servers](https://ai.noblerworks.com/learn/concepts/inference-servers/) | You're considering self-hosting an open-weights model |
| [Quantization and distillation](https://ai.noblerworks.com/learn/concepts/quantization-and-distillation/) | You want a smaller, faster model |
| [GPUs for AI](https://ai.noblerworks.com/learn/concepts/gpus-for-ai/) | You want to know what VRAM, FLOPS, and bandwidth actually decide |

---

## 🔁 Companion docs

- **[Glossary](../glossary.md)** - 200+ terms, one-line definitions
- **[Cloud from Scratch](../cloud-from-scratch.md)** - structured 8-phase cloud path
- **[AI from Scratch](https://ai.noblerworks.com/learn/start-here/zero-to-hero-path/)** - structured AI/LLM learning path
- **[YouTube curation](../youtube.md)** - videos for visual learners
- **[Topic indexes](../../topics/)** - browse Learn + Build + Compare + Certify by subject

---

## 🤝 Suggest a topic

Missing a concept you keep getting asked about? Open an issue or PR. Criteria for new pages:
- One topic, focused
- 5-10 minute read
- Plain English, no exam framing
- Concrete example included

[Contributing Guide](../../CONTRIBUTING.md)
