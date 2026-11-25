---
last-updated: 2026-11-25
applies-to: Professional Cloud Architect exam guide, checked 2026-10-14
difficulty: advanced
---

# AI, Gemini and the Agent Platform for the Architect Exam

The current exam guide adds AI to several sections: designing AI/ML solutions (1.3), end-to-end ML workflows (2.4), prebuilt APIs and models (2.5), securing AI (3.1) and Gemini Cloud Assist (1.2, 5.1). The exam wants the **architect's** view: which service fits a requirement, what the platform provides, and how to secure it. It does not ask you to train models.

**[📖 Professional Cloud Architect exam guide (PDF)](https://services.google.com/fh/files/misc/professional_cloud_architect_exam_guide_english.pdf)** - the sections this note follows.

## Naming (read this first)

Google renamed **Vertex AI** to the **Gemini Enterprise Agent Platform** (announced 2026-04-22), and the exam guide says "Agent Platform". Existing integrations keep working, since the change is mostly names, console and docs. Old names still appear in older study material.

| Older name | Current name (per Google's release notes) |
|---|---|
| Vertex AI (platform) | Gemini Enterprise Agent Platform ("Agent Platform") |
| Vertex AI Model Garden | Model Garden |
| Agent Engine | Agent Runtime |
| Pipelines, endpoints, model registry, custom training | Same capabilities, now under the Agent Platform. No separate new brand name was found |

**[📖 Agent Platform release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes)** - the rename table. Check it before the exam, because names are still settling.

## 1.3 Choosing AI and ML building blocks

### The decision ladder (use the highest rung that meets the requirement)

1. **Prebuilt API** - a trained model behind an API. No ML skill needed.
2. **Foundation model, prompted** - Gemini or another model from Model Garden, with a good prompt.
3. **Foundation model, grounded** - add your data (RAG, search) so answers are factual and current.
4. **Tuned model** - adapt a model with your examples when prompting and grounding are not enough.
5. **Custom model** - train your own on CPUs, GPUs or TPUs when the problem is specialized.

Higher rungs cost more, take longer and need more skill. The exam rewards the lowest rung that meets the stated need.

### Google AI APIs (differentiate them)

| API | Use it for |
|---|---|
| **Vision** | Labels, text in images (OCR), faces, objects, SafeSearch |
| **Video Intelligence** | Shot changes, labels, objects, speech in video. **Deprecated 2026-09-14, shuts down 2027-09-14**; Google points to Gemini models ([deprecations](https://docs.cloud.google.com/video-intelligence/docs/deprecations)) |
| **Speech-to-Text / Text-to-Speech** | Audio to text, text to audio |
| **Natural Language** | Entities, sentiment, syntax, classification |
| **Translation** | Language translation |
| **Document AI** | Extract structured data from forms and documents |
| **Image generation** (Imagen) | Create and edit images from prompts |
| **Search and conversation products** | Retrieval and chat grounded on enterprise data |

If the requirement is "extract text from scanned invoices", the answer is Document AI, not a custom model.

### Gemini models

- **Gemini** - multimodal models (text, image, audio, video, code). Available through the Agent Platform for enterprises, with data governance, IAM, VPC Service Controls and CMEK.
- **Model families** - larger models for harder reasoning, smaller and faster "flash" class models for latency and cost. Pick by quality, latency and price.
- **Open and partner models** - Model Garden also offers open models (for example Gemma, Llama) and partner models. Pick these for control, license or cost reasons.

### Model Garden

- **Model Garden** - the catalog where you discover, test, and deploy models: Google's, partners' and open-source. Deploy to managed endpoints or use serverless API access.
- Use it to integrate a model into a solution without building the serving stack. A requirement like "evaluate several models and deploy the best" points here.

### Grounding and agents

- **Grounding** - connect model answers to trusted sources (your documents, a search index, Google Search) to reduce hallucination and add citations.
- **RAG (retrieval-augmented generation)** - retrieve relevant passages from a vector or search index, add them to the prompt, then generate. Cheaper and faster to update than tuning.
- **Agent Builder tools** - build search, chat and agent experiences over enterprise data, with connectors and no-code or low-code options. Agents can call tools and APIs.
- **Agent Runtime** - managed hosting for agents you build with open frameworks.
- **Conversational agents** - virtual agents for web, app and voice, often replacing an IVR menu.
- **Human in the loop** - a person approves outputs before they change a system of record. Use it for catalogs, medical, financial and legal output.

### Gemini Enterprise, NotebookLM

- **Gemini Enterprise** - Google's workplace AI platform for employees: agents that search across company data and apps, with admin controls. It lets staff use AI agents without building them.
- **NotebookLM** - a source-grounded notebook that answers from documents you upload, with citations. The enterprise edition adds admin and data controls.
- Exam framing: **buy** Gemini Enterprise for employee productivity, **build** on the Agent Platform for a customer-facing or custom workflow.

## 2.4 End-to-end ML workflows

- **Pipelines** - orchestrate the ML life cycle (data prep, train, evaluate, deploy) as repeatable, versioned steps. Based on Kubeflow Pipelines and TFX concepts.
- **Feature store, Model Registry, Experiments, Metadata** - track data, models and runs. A model registry gives versioning and promotion.
- **Data integration** - prepare data in BigQuery, Dataflow or Cloud Storage and read it directly from training jobs. BigQuery ML trains simple models in SQL where data already lives.
- **Serving** - managed endpoints with autoscaling, traffic splitting for canary rollout, batch prediction for large offline jobs.
- **Monitoring** - detect skew and drift, track quality, and trigger retraining.
- **MLOps pattern** - code and pipeline in Git, build with Cloud Build, run pipelines on schedule or on new data, register and deploy models with approval gates.

### AI Hypercomputer

- **AI Hypercomputer** - Google's integrated architecture for AI: accelerators (GPUs and TPUs), high-bandwidth networking, storage, and software (GKE, schedulers, ML frameworks) designed to work together for training and serving at scale.
- **Choose the accelerator:** GPUs for broad framework support and flexibility, TPUs for large-scale training and serving of supported frameworks (JAX, TensorFlow, PyTorch via XLA) at good price/performance.
- **Consumption models** - match capacity to the workload:
  - **On-demand** - pay as you go, no guarantee of capacity.
  - **Committed use / reservations** - guaranteed capacity at a discount for steady need.
  - **Spot** - cheapest, can be preempted. Good for fault-tolerant training with checkpoints.
  - **Dynamic Workload Scheduler** - queue for scarce accelerators, flex-start for short jobs and calendar-style reservation for planned runs.
- **GKE for AI** - orchestrate training and serving with accelerator node pools. **Cloud Run** with GPUs for serverless inference. **Cloud Run functions** for event glue.
- **Data path** - keep data close to compute (same region), use Cloud Storage with high-throughput options and caching for training data.

## 2.5 Prebuilt solutions and APIs

- Use a prebuilt API when the task is common (OCR, translation, speech). Use a foundation model when the task is language reasoning or generation. Use custom training only for specialized needs.
- **Integrate Model Garden models** behind your API with IAM, quotas and logging.

## 3.1 Securing AI

**[📖 Model Armor](https://cloud.google.com/security/products/model-armor)** - screens prompts and responses.

- **Model Armor** - a managed service that screens model **prompts and responses** for prompt injection, jailbreaks, malicious URLs, harmful content and sensitive data leakage. Works with the Agent Platform, Gemini Enterprise and other models. Policies are templates, and floor settings enforce a minimum across a project, folder or organization. Enforcement can be inspect-only or block.
- **Sensitive Data Protection** (formerly Cloud DLP) - find, classify and de-identify PII. Inspect prompts, training data and outputs. Model Armor integrates with it.
- **Secure model deployment** - private endpoints, VPC Service Controls to stop data leaving, CMEK for keys, IAM least privilege for who may call or deploy, audit logs for every call.
- **Data governance for training** - classify and minimize data, de-identify before use, control residency with regions and org policy.
- **Prompt injection** - treat user and retrieved content as untrusted. Validate tool calls, limit agent permissions, and keep humans in the loop for risky actions.
- **Responsible AI** - safety filters, evaluation before launch, logging for audit, and explainability where decisions affect people.
- **Software supply chain** - sign and verify what runs. **Artifact Registry** stores images, **Binary Authorization** enforces attested images only, **Cloud Build** with provenance, vulnerability scanning, and SLSA-style build integrity. Apply this to model-serving containers too.

## 1.2 and 5.1 Gemini Cloud Assist

**[📖 Gemini Cloud Assist overview](https://docs.cloud.google.com/cloud-assist/overview)** - design, troubleshoot, optimize.

- **Gemini Cloud Assist** - the AI assistant for the Google Cloud application life cycle. A chat in the console and embedded in product pages, also reachable as an MCP server from other tools.
- **Design** - turn plain-language goals into an architecture, with Application Design Center and deployable Terraform. Platform teams curate approved templates.
- **Investigations** - a root-cause agent that analyses logs, configuration and metrics to produce ranked observations. It can start from an alerting policy and can become a support case.
- **Optimize** - cost questions and cost anomaly explanations.
- **Code and commands** - generate gcloud, kubectl and Terraform, and help with IAM.
- Status: some features are pre-GA and some need Gemini Code Assist Enterprise. For the exam, know it as an assistant for **design, troubleshooting and optimization**, not a replacement for architecture judgment.

## Migration Center (exam guide 1.4)

**[📖 Migration Center overview](https://docs.cloud.google.com/migration-center/docs/migration-center-overview)** - discovery, assessment, planning.

- **Migration Center** - the single place to discover and assess on-premises and other-cloud estates, group assets into applications, define migration preferences and generate a **TCO** report. Includes dependency discovery and database fit scores (Cloud SQL, AlloyDB).
- **Discovery client** - collects inventory and performance data over days or weeks, or import a VMware export.
- **Output** - sizing recommendations, cost comparison and a prioritized plan. Feed it into wave planning.
- Migration tooling: **Migrate to Virtual Machines** (VMs), **Database Migration Service**, **Storage Transfer Service** and **Transfer Appliance** (data), **Datastream** (change data capture), and **Migrate to Containers**.
- **Workload disposition** (exam guide 1.1) - for each workload decide to build, buy (SaaS), modify (re-platform or refactor) or deprecate.
- **Migration strategies** - rehost (lift and shift), replatform, refactor, repurchase, retire, retain. License implications (BYOL, sole-tenant nodes, Windows and SQL Server licensing) and financial impact (CapEx to OpEx) belong in the plan.

## Exam traps

- **Use the lowest rung of the ladder** that meets the requirement. Prebuilt API beats custom model for common tasks.
- **Grounding or RAG** is the answer to "answers must be based on our documents". Tuning is not.
- **Model Armor** protects prompts and responses. **Sensitive Data Protection** finds and masks PII. **VPC Service Controls** stops exfiltration. They are layers, not alternatives.
- **Spot** capacity is cheap but preemptible. Training needs checkpoints.
- **Gemini Enterprise** is for employees, the **Agent Platform** is for building.
- Names changed in 2026. If an option says Vertex AI and another says Agent Platform for the same capability, they may be the same thing.
- A human approval step is the safe answer for gen AI that writes to a system of record.
