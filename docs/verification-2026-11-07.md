---
last-updated: 2026-11-07
difficulty: n/a
---

# Fact verification pass, pages written 2026-11-07

Method: claims were extracted from each page and checked against the vendor or project page named in the last column (fetched 2026-11-07). VERIFIED means a fetched page supports it. Fixed means it was wrong or unsupported and the page now says what the source supports. Unverifiable means no readable primary source; those claims were softened, removed or are listed below as still open.

## Per-page counts

Counts are claim-level tallies made while reading, approximate to a few claims.

| Page | Verified | Fixed | Unverifiable |
|---|---|---|---|
| resources/troubleshooting/cicd-pipeline-troubleshooting.md | 12 | 3 | 0 |
| resources/troubleshooting/terraform-state-and-drift-troubleshooting.md | 16 | 3 | 0 |
| resources/cost-optimization/kubernetes-cost-optimization.md | 17 | 4 | 1 (Kubecost) |
| resources/interview-prep/kubernetes-cloud-native-interview.md | 9 | 0 | 0 |
| resources/interview-prep/platform-engineer-interview.md | 1 | 1 | 6 (opinion/practice advice, not checkable) |
| learn/concepts/opentofu-vs-terraform.md | 8 | 0 | 0 |
| learn/concepts/service-quotas-and-limits.md | 14 | 1 (clarified) | 1 ("a week" is labeled habit) |
| learn/concepts/ebpf-explained.md | 9 | 1 | 0 |
| learn/concepts/backstage-and-developer-portals.md | 6 | 0 | 0 |
| learn/concepts/webassembly-at-the-edge.md | 12 | 0 | 0 |
| learn/day-one/python-for-cloud.md | 6 | 2 | 0 (boto3 order and azure/google names now sourced) |
| resources/postmortem-crowdstrike-2024.md | 22 | 1 (label) | 0 |
| resources/postmortem-aws-dynamodb-dns-2025.md | 22 | 1 (label) | 0 |
| 18 flashcard decks, Key terms (283 definitions) | 52 fetched, about 215 generic definitions judged correct by reading, not fetched | 4 | see below |

## Fixes

| Page | Old | New | Source |
|---|---|---|---|
| cicd-pipeline-troubleshooting | OIDC permission key "not fetched, confirm there" | `permissions: id-token: write` stated, OIDC reference linked | https://docs.github.com/en/actions/reference/security/oidc |
| cicd-pipeline-troubleshooting | `actions/cache@v4` flagged unverified | `actions/cache@v6` (README examples); note that deprecated old versions fail | https://github.com/actions/cache |
| terraform-state-and-drift | `terraform state rm --dry-run` | `terraform state rm -dry-run` | https://developer.hashicorp.com/terraform/cli/commands/state/rm |
| terraform-state-and-drift | `removed` block "built from syntax" note was vague | Quotes the docs sentence on `destroy = false`; says docs example uses `destroy = true` and do not state the delete-resource-block requirement | https://developer.hashicorp.com/terraform/language/block/removed |
| terraform-state-and-drift | `use_lockfile` "recommended" | Replacement for deprecated `dynamodb_table`; defaults to `false` | https://developer.hashicorp.com/terraform/language/backend/s3 |
| kubernetes-cost-optimization | `kubectl autoscale ... --cpu-percent=50` | `--cpu=50%`; `--cpu-percent` not in the current reference | https://kubernetes.io/docs/reference/kubectl/generated/kubectl_autoscale/ |
| kubernetes-cost-optimization | OpenCost: "Prometheus required / CNCF unknown" | Prometheus is a prerequisite; CNCF incubating project | https://opencost.io/docs/installation/prometheus , https://opencost.io/ |
| kubernetes-cost-optimization | VPA modes "truncated, read the page" | Recreate, InPlaceOrRecreate, InPlace (alpha, VPA 1.7.0, K8s 1.33+), Auto deprecated since VPA 1.4.0 | https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/ |
| kubernetes-cost-optimization | Cluster Autoscaler "not covered" | Scale-down threshold 0.5 on requests, unneeded time 10m, scale-down-disabled annotation | https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md |
| platform-engineer-interview | "the four DORA metrics ... time to restore" | DORA's current five metrics, incl. failed deployment recovery time and deployment rework rate | https://dora.dev/guides/dora-metrics/ |
| service-quotas-and-limits | Bare CLI example with quota L-20F13EBD | Notes it is the docs' sample ("Running Dedicated c5n Hosts") | https://docs.aws.amazon.com/cli/latest/userguide/cli_service-quotas_code_examples.html |
| ebpf-explained | "Cilium replaces kube-proxy / sidecar-free mesh" presented as background fact | Attributed: eBPF page lists a kube-proxy talk; sidecar-free is a vendor claim, not checked | https://ebpf.io/what-is-ebpf/ |
| python-for-cloud | Azure/Google SDK names "general knowledge" | `azure-mgmt-*` and `google-cloud-<service>` patterns sourced | https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-overview , https://docs.cloud.google.com/python/docs/reference |
| postmortem-crowdstrike-2024, postmortem-aws-dynamodb-dns-2025 | Cert mapping table unlabeled | Labeled as editorial judgment; CKA / CKS row called a conceptual stretch | n/a (own judgment) |
| Key terms: OCI Architect Professional | Oracle Kubernetes Engine (OKE) | Oracle Cloud Infrastructure Kubernetes Engine (OKE) | https://docs.oracle.com/en-us/iaas/Content/ContEng/Concepts/contengoverview.htm |
| Key terms: GCP Cloud Developer | Cloud Functions | Cloud Run functions (formerly Cloud Functions) | https://docs.cloud.google.com/functions/docs/concepts/overview |
| Key terms: GCP Cloud Developer | Workload Identity (GKE) | Workload Identity Federation for GKE | https://docs.cloud.google.com/kubernetes-engine/docs/concepts/workload-identity |
| Key terms: PL-900 | Dataset | Semantic model (formerly dataset) | https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-understand |
| Key terms: IBM Cloud Solution Architect | Activity Tracker (the IBM Cloud service that records activity events) | Activity Tracker Event Routing; original service deprecated 28 March 2024 (secondary search summary of IBM docs) | https://cloud.ibm.com/docs/atracker |
| Key terms: IBM Cloud SRE | IBM Cloud Monitoring "powered by Sysdig" | Clause removed (IBM page does not state it) | https://cloud.ibm.com/docs/monitoring |

## Fetched and verified (selection)

CI/CD: debug variables, cache rules (512-char key, 7 days, 10 GB, search order, merge ref, restore-keys), July 15 2026 OIDC subject format. Terraform: force-unlock, plan flags, init flags (-migrate-state, -reconfigure, -upgrade, -backend-config), import and generate-config-out (experimental, errors on existing file), validate (no remote services), S3 LockID. Kubernetes: Deployment defaults (RollingUpdate, 25%/25%, progressDeadlineSeconds 600), QoS classes and eviction order, Karpenter policies and defaults (WhenEmpty, Balanced, WhenEmptyOrUnderutilized, consolidateAfter 0s, expireAfter 720h, 10% budget, UTC). OpenTofu: FAQ founders, Linux Foundation, state compatibility up to 1.5.x, encryption example verbatim. Quotas: AWS terminology, global quota from us-east-1, GCP allocation/rate, midnight Pacific. Backstage, WebAssembly, Cloudflare Workers Wasm limits, eBPF hooks/verifier/JIT/maps. CrowdStrike RCA (checked from the PDF text): 99% vs 1% variance, 7.11, 21 vs 20 inputs, 12 test cases, July 19/25/27 dates, Aug 9 and Aug 19, two third-party vendors, rings and bake-in. AWS DynamoDB summary: all times in the page matched. Key terms: Savings Plans, Direct Connect gateway, Network Firewall, Azure Artifacts, OCI Functions/Fn, Nomad glossary/schedulers/canary, Packer breakpoint and manifest, App Mesh end of support 2026-09-30 (AWS docs).

## Still unverifiable

- Kubecost: no vendor docs fetched; the page already says to check its site. Search results (third-party) say OpenCost is Kubecost's open source core and IBM acquired Kubecost in September 2024; not added to the page.
- About 215 Key terms are generic definitions (Terraform, RHCSA, FinOps, Salesforce, OCI, IBM and similar) where the vendor page was unreadable (Salesforce returned 403, IBM Cloud pages 404 or thin, Google pages redirect) or the term is standard vocabulary; they were read for errors and none found beyond the fixes above. Not fetched: Salesforce Apex async terms, RHCSA/EX280 terms, FinOps Framework phases, Memorystore engines (Redis page fetched; Memcached/Valkey not stated there), Cloud Deploy, Binary Authorization, OCI Service Connector Hub.
- IBM Activity Tracker deprecation dates come from a search summary of IBM documentation, not a fetched IBM page.
- AWS OpsWorks Stacks end of life 26 May 2024 (SAP-C02/DOP-C02 notes, edited earlier today): the AWS blog linked from the notes gives no date; the date is confirmed only via a Terraform provider issue quoting AWS and a re:Post answer citing the AWS FAQ. IBM wording items remain open in TODO.md (Cloud Foundry, Watson, Certificate Manager).
- Platform engineer interview: the answers are practice advice, not product facts; the CNPA exam coverage claim in the Backstage page was not checked against the CNCF curriculum.

## Cert guides pass

Second pass over the cert guides added 2026-11-07: exam logistics re-fetched from each certifier, every question-bank key and distractor checked against vendor docs, and notes claims with numbers, flags or named behavior classified. Counts are approximate claim-level tallies.

| Guide | Verified | Fixed | Unverifiable | Wrong keys | Distractors made unambiguous |
|---|---|---|---|---|---|
| Linux+ XK0-006 | 55 | 2 | 3 | 0 of 20 | 0 |
| AWS DVA-C03 | 70 | 5 | 1 | 0 of 16 | 2 (Q2, Q8) |
| AWS SAP-C03 | 190 | 5 | 1 | 0 | 1 (Q11) |
| Terraform Associate 004 | 75 | 27 | 6 | 0 (4 explanations fixed) | 0 |
| CNCF KCA | 140 | 4 | 2 | 0 of 32 | 0 |
| CNCF CBA | 112 | 4 | 3 | 0 of 31 | 1 (Q31) |
| CNCF CNPE | 75 | 2 | 0 | 0 of 30 | 0 |
| CNCF CKNE | 110 | 6 | 1 | 0 of 30 | 0 |

### Fixes

| Page | Old | New | Source |
|---|---|---|---|
| linux-plus fact-sheet, README | Validity not verified | 3 years, renewable via CE; CEU count still not verified | https://www.comptia.org/en-us/resources/ce/learn/comptia-continuing-education-program-faq/ |
| linux-plus notes/02 | `docker system prune` removes unused containers, networks, images | Stopped containers, unused networks, dangling images, build cache; not volumes | https://docs.docker.com/reference/cli/docker/system/prune/ |
| dva fact-sheet, README | Delivery, languages, validity not verified | Pearson VUE or online; 6 languages; 3 years | https://aws.amazon.com/certification/certified-developer-associate/ |
| dva notes/03 | ECS rolling update is "the default" | "can use"; the page does not say default | https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html |
| dva bank Q2, Q8 | Distractors arguably correct (batch size 1; 4 KB chunks) | Replaced; KMS Encrypt limit of 4,096 bytes stated | https://docs.aws.amazon.com/kms/latest/APIReference/API_Encrypt.html |
| sap fact-sheet, README | Delivery, validity, languages not verified | Filled in | https://aws.amazon.com/certification/certified-solutions-architect-professional/ |
| sap fact-sheet, notes/04 | DR RTO/RPO ranges as fact | Marked unverified | https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html |
| sap bank Q11 | Distractor "move to public subnets" defensible | Scenario and distractors tightened | https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html |
| terraform fact-sheet, hcl notes | Variable precedence had env vars highest | default < env < tfvars < tfvars.json < auto.tfvars < -var/-var-file | https://developer.hashicorp.com/terraform/language/values/variables |
| terraform (many) | S3 backend needs DynamoDB for locking | Opt-in `use_lockfile` (default false); `dynamodb_table` deprecated | https://developer.hashicorp.com/terraform/language/backend/s3 |
| terraform state notes | Local backend no locking; Azure blob lease | Local locks via system APIs; Azure native Blob capabilities | https://developer.hashicorp.com/terraform/language/backend/local |
| terraform notes | 003 domain weights, "3000+ providers", PSI named, "57 questions" | Removed (004 publishes no weights; counts not on pages) | https://developer.hashicorp.com/certifications/infrastructure-automation |
| terraform modules, core-workflow, data sources, provisioners, dependencies | Registry `version` required; `-reconfigure` discards state; condition timings; provisioner claims | Corrected to docs wording | https://developer.hashicorp.com/terraform/language/block/module , https://developer.hashicorp.com/terraform/language/expressions/custom-conditions |
| terraform bank Q1 | `terraform refresh` syncs state | `plan -refresh-only`; refresh deprecated | https://developer.hashicorp.com/terraform/cli/commands/refresh |
| kca notes/03 | `KYVERNO_EXPERIMENTAL=true` | Removed | https://kyverno.io/docs/subprojects/kyverno-cli/ |
| kca notes/05 | Evaluation order match, context, preconditions | match, preconditions, body; context resolves before preconditions | https://kyverno.io/docs/policy-types/cluster-policy/variables/ |
| kca notes/05 | Variables unsupported in patchesJson6902 path (flat) | Docs disagree; both stated | https://kyverno.io/docs/policy-types/cluster-policy/mutate/ |
| kca notes/06 | `kyverno-metrics` ConfigMap keys | Set via Helm `metricsConfig` | https://kyverno.io/docs/monitoring/ |
| cba notes/04 | `yarn new` choices, plugin dir names, default page URL | Only what docs name; rest marked convention | https://backstage.io/docs/frontend-system/building-plugins/index |
| cba bank Q31 | D `createBackstageTheme` possibly valid | `makeBackstageTheme` (legacy status from recollection, not fetched) | https://backstage.io/docs/conf/user-interface/ |
| ckne notes 01-04 | Pod CIDR flags, `kubectl debug`, tcpdump flags, kube-proxy mode, Cilium global annotation, NetworkPolicy semantics "not covered" | Sourced (`service.cilium.io/global`, `--cluster-cidr`, `--node-cidr-mask-size`, `endPort`); tcpdump `-nn` changed to `-n` | https://docs.cilium.io/en/stable/network/clustermesh/global-services/ , https://kubernetes.io/docs/concepts/services-networking/network-policies/ , https://kubernetes.io/docs/reference/kubectl/generated/kubectl_debug/ |
| cnpe notes 02-03 | `dynamicStableScale` needs a traffic router; XRD `scope` without version | Only `setCanaryScale` needs one; `scope` is `apiextensions.crossplane.io/v2` | https://argo-rollouts.readthedocs.io/en/stable/features/canary/ , https://docs.crossplane.io/latest/composition/composite-resource-definitions/ |

Logistics confirmed with no change: KCA, CBA, CNPE, CKNE (LF pages and CNCF curriculum PDFs), SAP-C03 and DVA-C03 numbers and dates, Terraform 1 hour, $70.50, 2 years.

### Still unverifiable

- Linux+: price and delivery (not on the CompTIA page), XK0-006 CEU count, XK0-005 retirement date (third-party), command usage read against man pages only.
- Terraform: question count, passing score and 003 retirement date (not published); `terraform.tfstate.d/` name, plan symbol `<=`, Consul encryption.
- SAP-C03: DR RTO/RPO ranges (whitepaper figure is an image).
- CBA: `createBackstageTheme` legacy status; frontend-plugin `yarn new` choice name; backend dir suffixes.
- KCA: `serviceMonitor.enabled` mechanics, default `exceptionNamespace` and `resourceFilters`.
- CKNE: egress default-deny blocking DNS is practice, not a page quote.
- Generic Key terms in these guides were read for errors, not fetched.
