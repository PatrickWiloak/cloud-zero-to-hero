---
last-updated: 2026-11-18
---

# GCP Professional Cloud Architect (PCA) - Exam Strategy

## Format reminder

- 50-60 questions, 120 minutes
- Pass mark: not published; widely reported as ~70-75% based on community feedback
- Multiple choice + multiple response
- Includes case study questions referencing fictional companies. Current cases: Altostrat Media, Cymbal Retail, EHR Healthcare, KnightMotives Automotive (see notes/case-studies.md)

## Top traps

1. **Spanner vs Cloud SQL vs Firestore vs BigQuery**:
   - Spanner: globally consistent SQL, horizontal scale, ACID across regions
   - Cloud SQL: regional, managed PostgreSQL/MySQL/SQL Server
   - Firestore: document store, regional or multi-region
   - BigQuery: serverless analytics warehouse
   Each has a specific use case; PCA tests the boundary cases.

2. **GCE machine families**: E2 (cost-optimized), N2 (balanced), C3 (latest compute-optimized), M3 (memory-optimized for in-memory DBs and SAP HANA). Pick by workload shape.

3. **CUD vs SUD vs Spot**:
   - SUD: automatic, ~30% discount for sustained running
   - CUD: 1-3 year commitment, up to 70% (resource-based or spend-based)
   - Spot (formerly preemptible): 60-91% discount, can be reclaimed
   Newer CUDs (flexible, spend-based) blur the line with Savings Plans on AWS.

4. **Interconnect tiers**:
   - Dedicated Interconnect: 10 Gbps or 100 Gbps direct
   - Partner Interconnect: 50 Mbps - 50 Gbps via SP
   - HA VPN: over public internet, 99.99% with two tunnels
   - SLAs: 99.9% (single Interconnect) → 99.99% (two metros, single region) → 99.99% (dual region)

5. **GKE Standard vs Autopilot**: Standard for full control + node management; Autopilot for least-ops, pod-based pricing. PCA increasingly favors Autopilot for "minimal operational overhead."

6. **VPC Service Controls vs Private Google Access vs Private Service Connect**:
   - Private Google Access: VMs without public IPs reach Google APIs
   - VPC Service Controls: data exfiltration prevention via service perimeters
   - Private Service Connect: consume Google services or third-party services via private IPs

7. **IAM hierarchy**: Organization → Folders → Projects → Resources. Roles flow down. Org policies are constraints (different from IAM) - they restrict configurations.

8. **Resource hierarchy and billing**: each Project has its own quotas, billing, IAM. Folders for grouping. Org policy constraints at any level.

9. **Cloud Storage classes**: Standard, Nearline (>30 days), Coldline (>90 days), Archive (>365 days). Lifecycle policies for transitions. Multi-region vs Dual-region vs Region location selection.

10. **Network tiers**: Premium (default, Google's global network) vs Standard (cheaper, regional egress through public internet). Premium is the default modern answer.

## Case study tactics

The PCA case studies are published ahead of time (four in the current guide: Altostrat Media, Cymbal Retail, EHR Healthcare, KnightMotives Automotive) - questions for each case study reference specific constraints in the company's Existing Environment and Business Requirements sections. Read the case study once carefully; for each subsequent question, jump back to the relevant constraint.

Common case study traps:
- "Legacy systems will not move" (EHR Healthcare only) - answers that migrate them fail; integrate over hybrid connectivity. Altostrat's legacy is slated to migrate soon, and KnightMotives replaces its legacy gradually
- "Alerts are ignored" - fix routing, ownership and SLO-based alerting, not more email
- "No budget for new equipment" (KnightMotives dealers) - browser-based or SaaS, no on-site hardware
- "Humans must review AI output" (Cymbal) - keep a human-in-the-loop step before writes to the catalog
- "Cannot move data outside the EU" - rules out multi-region us / global Spanner
- "Must minimize cost" - prefer Cloud Run over GKE, Cloud Functions over Cloud Run for spiky
- "Must minimize operational overhead" - prefer fully-managed (Cloud Run, BigQuery, Cloud SQL) over self-managed

## Time management

120 / ~55 = ~2.2 min/question. Pace: half done by minute 60. Leave 15 min for flagged review.

## When stuck

1. **Identify case study constraints** that filter options.
2. **Default to managed > self-managed** when both work.
3. **Default to Google's recommended pattern** - Cloud Service Mesh, GKE Autopilot, Spanner for global, Cloud Run for serverless containers.
4. **Eliminate "build it yourself"** if a Google-managed service does it.

## Day-of logistics

120 min, ~55 questions: bring two IDs. Online proctored available via Kryterion / Pearson VUE.

## After

**Pass:** Cert valid 2 years. Renew by passing again or another GCP Professional cert.

**Fail:** Most failures are on case study questions where missed constraints cost points. Re-read the case studies in the official guide and practice mapping requirements to GCP services.

## PCA patterns

- "Globally consistent SQL with sub-second writes" = Cloud Spanner
- "Multi-region serverless containers" = Cloud Run + Global LB with serverless NEGs
- "Hybrid 99.99%" = two Dedicated Interconnects in two metros
- "GKE with mTLS + observability + minimal ops" = Autopilot + Cloud Service Mesh
- "Steady 24/7 cost optimization" = 3-year CUDs
- "Interruptible cheap compute" = Spot
- "Data exfil prevention" = VPC Service Controls
- "Multi-tenant SaaS data isolation in BigQuery" = dataset IAM + row-level + column policy tags
- "Cross-region DR for stateful app" = Cloud SQL cross-region read replica + MIG scale-to-zero in DR
- "Per-call zero trust between services" = Cloud Service Mesh + AuthorizationPolicy
