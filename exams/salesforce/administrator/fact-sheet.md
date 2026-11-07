---
last-updated: 2026-11-06
---

# Salesforce Certified Platform Administrator - Fact Sheet

## Quick Reference

**Exam:** Salesforce Certified Platform Administrator
**Code:** Plat-Admn-201
**Cost:** $200 USD ($100 retake)
**Format:** 60 multi-choice + multi-select
**Duration:** 105 minutes
**Passing:** 65%
**Maintenance:** 3 free annual release exams (Spring, Summer, Winter)

**[📖 Credential page](https://trailhead.salesforce.com/credentials/administrator)**
**[📖 Exam Guide PDF](https://trailhead.salesforce.com/help?article=Salesforce-Certified-Administrator-Exam-Guide)**
**[📖 Trailhead Admin Trailmix](https://trailhead.salesforce.com/credentials/platformadministrator)**

---

## Salesforce platform basics

### Editions (top-level)

- **Essentials** - SMB, simplified
- **Professional** - mid-market
- **Enterprise** - most popular for cert prep
- **Unlimited** - largest enterprises with all features
- **Developer** - free, for development; not licensed for production users

### Cloud products (separately licensed)

- **Sales Cloud** - lead/opportunity/account/contact management
- **Service Cloud** - case management, knowledge, omni-channel
- **Marketing Cloud** - email/journey marketing (separate platform)
- **Commerce Cloud** - e-commerce (B2B and B2C)
- **Experience Cloud** - external community sites (formerly Community Cloud)
- **Data Cloud** - customer data platform
- **Field Service Lightning** - mobile field service
- **CRM Analytics** (formerly Tableau CRM / Einstein Analytics)
- **MuleSoft** - integration platform

### Lightning vs Classic

- **Lightning Experience** - modern UI, default since 2018; what's tested
- **Salesforce Classic** - older UI, still supported but not on the exam

---

## Org setup and security

### User types

- **Standard User** - normal Salesforce license
- **Customer Community / Partner Community** - Experience Cloud users
- **Chatter Free / External Apps** - lighter-license users

### User access controls (layered)

```
Org-Wide Defaults (OWD)        ← most restrictive baseline
   ↓ unlock via
Role Hierarchy                 ← grant access to records owned by subordinates
   ↓ unlock via
Sharing Rules                  ← grant access based on criteria/owner
   ↓ unlock via
Manual Sharing / Apex Sharing  ← per-record grants
```

Plus:

- **Profiles** - what users can do (CRUD on objects, field-level security, app/tab access)
- **Permission Sets** - grant additional permissions on top of profile (preferred over creating many profiles)
- **Permission Set Groups** - bundle permission sets

### MFA

Required for all internal users since Feb 2022 (Salesforce-mandated, no opt-out).

### IP restrictions and login hours

Set per profile to restrict login times and source IPs.

### Single Sign-On

- SAML 2.0
- OAuth 2.0
- OpenID Connect
- Connected Apps for OAuth

---

## Objects and fields

### Standard objects

Salesforce out-of-the-box:

- **Account** - companies / B2B customers
- **Contact** - individual people
- **Lead** - unqualified prospect (gets converted to Account + Contact + Opportunity on conversion)
- **Opportunity** - sales deal in progress
- **Case** - customer support ticket
- **Campaign** - marketing campaign
- **Product / Pricebook** - what you sell
- **User** - Salesforce users
- **Activity / Task / Event** - work items, calendar

### Custom objects

Add your own (`__c` suffix):

- Up to 800 custom objects in Enterprise edition
- Have records, fields, page layouts, validation rules, automation, etc.

### Field types

| Type | Notes |
|---|---|
| Text, Text Area, Long Text Area, Rich Text Area | Different size limits |
| Number, Currency, Percent | Numeric |
| Date, DateTime, Time | Temporal |
| Checkbox | Boolean |
| Picklist, Multi-Select Picklist | Dropdown(s) |
| Email, Phone, URL | Validated formats |
| Lookup | Reference another record |
| Master-Detail | Reference + cascade delete + roll-up summary |
| Hierarchical | Lookup specifically for User-to-User |
| Auto Number | Auto-incrementing read-only |
| Formula | Calculated, read-only |
| Roll-Up Summary | Sum/Min/Max/Count of child records (Master-Detail only) |
| Geolocation | Lat/Lon |
| External ID | Unique identifier from external system, indexed |

### Field-Level Security (FLS)

Per-profile / per-permission-set control of which fields a user can read/edit. Combined with object permissions and record access.

### Lookup vs Master-Detail

- **Lookup** = parent can be deleted; child becomes orphan or null
- **Master-Detail** = parent deletion cascades to children; child inherits owner + sharing from parent; supports roll-up summary
- A custom object can have up to **2 master-detail relationships**
- Once converted from Lookup to MD, can't have orphans

### Record Types

Different "flavors" of the same object - different page layouts, picklist values per type. Common pattern: Sales Process A vs B both on Opportunity object.

---

## Data management

### Importing data

| Tool | Use |
|---|---|
| **Data Import Wizard** | Browser-based; up to 50,000 records; supports Account/Contact/Lead/Solution/custom |
| **Data Loader** | Desktop app or CLI; up to 5 million records; all objects; insert/update/upsert/delete |
| **Bulk API** | Programmatic; high-volume; CSV-based |

Data Loader is the most-tested tool.

### Deduplication

- **Duplicate Rules** + **Matching Rules** - prevent or alert on duplicate creation
- Built-in matching rules for Account / Contact / Lead

### Mass operations

- Mass Transfer (records between owners)
- Mass Update (limited)
- Inline edit on list views

### Backup

- Weekly Export (data) - free, weekly schedule, ZIP of CSVs
- **Salesforce Backup & Restore** - paid product for production-grade backup
- **Apex Data Loader CLI** - DIY scripted exports

### Sandboxes

| Type | Refresh interval | Storage |
|---|---|---|
| **Developer** | 1 day | 200 MB |
| **Developer Pro** | 1 day | 1 GB |
| **Partial Copy** | 5 days | 5 GB + sample data |
| **Full** | 29 days | full prod copy |

Use Full for UAT / pre-prod testing; Partial for testing with sample data; Developer for unit/integration.

### Change sets and packages

- **Change Sets** - move metadata between connected orgs (sandbox to prod)
- **Unmanaged Packages** - distributable customizations
- **Managed Packages** - AppExchange products with versioning

---

## Automation tools

### Flow Builder (the modern one)

Salesforce's primary automation tool. Replaces Workflow Rules, Process Builder, and Approval Processes (somewhat).

#### Flow types

- **Screen Flow** - user-facing UI flow (lightning component, custom button)
- **Record-Triggered Flow** - runs before/after a record save (replaces Workflow Rules + Process Builder)
- **Scheduled Flow** - runs on a schedule
- **Auto-Launched Flow** - called from Apex, Process, button
- **Platform Event Flow** - triggered by platform events

#### Common elements

- Get Records, Create Records, Update Records, Delete Records
- Decision (branching), Loop, Assignment, Subflow
- Action (call Apex, send email, post to Chatter, etc.)
- Screen elements (only in Screen Flows)

### Validation Rules

Formula-based rules that block save if condition is true. Display custom error message.

### Approval Processes

Multi-step approvals with submit, approve/reject, escalation, rejection actions.

Slowly being absorbed into Flow Builder (newer Approval features in Flow).

### Lightning App Builder

Drag-drop record page customization. Lightning Components on a page. Per-record-type, per-app, per-profile assignment of pages.

---

## Reports and Dashboards

### Report types

- **Tabular** - simple list (no totals)
- **Summary** - grouped by one or more fields with subtotals
- **Matrix** - rows + columns (cross-tab)
- **Joined** - multiple report blocks on the same canvas

### Report formats

- **Standard report types** - based on standard objects + relationships
- **Custom report types** - admin-defined to enable reporting on custom relationships

### Dashboards

- Up to 12 components per dashboard (varies by edition)
- Component types: chart, gauge, metric, table
- **Dynamic dashboards** - run as logged-in user (limit varies by edition; max 3-10)
- Dashboards refresh on demand or scheduled

### Folder permissions

- Public folders - shared with group/role
- Private folders - owner only
- Folder permissions: View / Edit / Manage

---

## Sales Cloud highlights

- **Lead** management (capture → score → assign → convert)
- **Web-to-Lead** form integration
- **Lead Conversion** - Lead becomes Account + Contact + Opportunity
- **Opportunity Stages** + Sales Process - kanban-style pipeline
- **Forecasting** - territory or hierarchy-based
- **Products and Pricebooks** - what you sell with multiple price lists
- **Quotes** - generate quote PDF from Opportunity
- **Path** - guided steps shown on record page (e.g., Lead Path)

---

## Service Cloud highlights

- **Case management** - email-to-case, web-to-case, console-based work
- **Case assignment rules** - auto-assign by criteria
- **Escalation rules** - auto-escalate based on age/priority
- **Auto-Response rules** - auto-reply to new cases
- **Knowledge** - articles, categories, search
- **Omni-Channel** - route work (cases, chats, calls) to agents based on availability
- **Service Console** - agent UI with split view, related records, macros

---

## Common exam triggers

- "Records are publicly visible to all internal users by default" → OWD = Public Read/Write or Public Read-Only
- "Manager should see records owned by direct reports" → Role Hierarchy + "Grant Access Using Hierarchies"
- "Sales rep can see records meeting criteria" → Criteria-Based Sharing Rule
- "Field hidden on a profile" → Field-Level Security
- "Block save unless field is filled correctly" → Validation Rule
- "Need to roll up child record sums to parent" → Roll-Up Summary on Master-Detail
- "Two flavors of an Account, different page layouts" → Record Types
- "Mass insert 500,000 records" → Data Loader (Wizard caps at 50K)
- "Multi-step approval with manager + finance approval" → Approval Process
- "Run logic when record is saved" → Record-Triggered Flow
- "Display sequenced steps on Opportunity record page" → Path
- "Auto-route case by language and priority" → Omni-Channel Routing
- "Quarterly historical sales report" → Custom Report Type + Summary Report

---

## Highest-yield facts

1. **Sharing model layers**: OWD → Role Hierarchy → Sharing Rules → Manual/Apex Sharing
2. **Profile = baseline access**, **Permission Set = additional permissions** (prefer permission sets to manage many profiles)
3. **MFA mandatory** since Feb 2022
4. **Data Loader for >50K records**, Import Wizard for less
5. **Lookup vs Master-Detail**: MD has cascade delete + roll-up summary; orphan vs no orphan
6. **Flow Builder** is the modern automation tool (Workflow Rules and Process Builder are deprecated for new dev)
7. **Sandbox types**: Developer (1d / 200MB) / Developer Pro / Partial Copy / Full
8. **Reports**: Tabular / Summary / Matrix / Joined
9. **Dashboards limit**: 12 components per dashboard (Enterprise+)
10. **3 free release exams per year** (Spring, Summer, Winter) for cert maintenance
11. **Custom field naming**: `Field_Name__c` (custom suffix `__c`)
12. **Lookup, Master-Detail, Hierarchical** are the three relationship field types
