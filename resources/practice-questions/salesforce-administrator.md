---
last-updated: 2026-10-22
difficulty: beginner
---

# Salesforce Certified Platform Administrator - Practice Questions

30 questions across the administrator exam's main areas: configuration and setup, object manager and Lightning App Builder, process automation, data and analytics management, and the sales and service applications.

> **Cert page:** [exams/salesforce/administrator/](../../exams/salesforce/administrator/)

---

### Question 1
**Scenario:** A user must see only their own records on a custom object, while their manager sees the whole team's.

A. Set the object's organization-wide default to Public Read/Write and rely on page layouts to keep other users' records out of view
B. Create a permission set
C. Set the organization-wide default to Private and enable Grant Access Using Hierarchies
D. Use field-level security

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Sharing is built from the most restrictive baseline upward: the organization-wide default sets the floor, and role hierarchy, sharing rules, manual sharing, and teams open it back up. Field-level security controls which fields are visible, not which records.
</details>

---

### Question 2
**Scenario:** A field must be hidden from one group of users but visible to another.

A. Field-level security via profiles or permission sets
B. Record types, assigning one record type to the first group and a different one to the second group
C. Validation rules
D. Page layouts alone, removing the field from the layout assigned to the group that must not see it

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Removing a field from a page layout hides it from that layout only; it remains reachable through reports, the API, and list views. Field-level security is the enforced control, applied at the data layer.
</details>

---

### Question 3
**Scenario:** Additional permissions must be granted to a handful of users without cloning their profile.

A. Change each user's role so that the extra permissions come down through the role hierarchy
B. Assign a permission set, or a permission set group for a bundle of related access, without touching the user's profile
C. Create a new profile that is a copy of the current one and add the extra permissions there
D. Change the organization-wide default

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Permission sets are additive and prevent profile proliferation, which is why Salesforce's guidance is a minimum-access profile plus permission sets. Permission set groups bundle several sets for a persona, with muting available to remove specific permissions from the group.
</details>

---

### Question 4
**Scenario:** Two divisions need different picklist values and page layouts on the same object.

A. Record types, each with its own picklist value sets and page layout assignments
B. Two profiles
C. Field dependencies, which filter a dependent picklist based on the value chosen in a controlling field
D. Two custom objects, one per division, each with its own fields, picklist values, and page layouts

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Record types partition a single object into business variants and drive both layout and picklist behavior per profile. Duplicating the object would split reporting and duplicate every piece of automation.
</details>

---

### Question 5
**Scenario:** Which automation tool should be used for new declarative automation?

A. Process Builder, because it is the most flexible declarative tool for building multi-step record automation
B. Workflow Rules, because they have been available the longest and are the most widely documented
C. Flow Builder, which Salesforce has consolidated automation into
D. Apex triggers

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Workflow Rules and Process Builder are retired for new automation and existing ones should be migrated. Flow covers record-triggered, screen, scheduled, and autolaunched cases, and record-triggered flows split into before-save (fast field updates on the same record) and after-save (related records and external actions).
</details>

---

### Question 6
**Scenario:** A value must be prevented from being saved when it fails a business rule.

A. A formula field that returns an error message whenever the value does not satisfy the business rule
B. A required field on the page layout
C. A validation rule that evaluates to true when the data is invalid
D. A workflow rule with a field update action that clears the value shortly after the record is saved

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** The logic is inverted from how people read it: the rule's formula returning true is what blocks the save and shows the error. Validation rules also fire on API and data loader inserts, which page-layout requirements do not.
</details>

---

### Question 7
**Scenario:** A relationship must cascade delete children when the parent is deleted and support roll-up summaries.

A. An external lookup relationship, which links the child to records held in an external data source
B. A master-detail relationship
C. A hierarchical relationship, a special lookup that links a user to another user
D. A lookup relationship on the child object, with the parent field marked as required on the page layout

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Master-detail children are owned by the parent: they inherit its sharing, have no owner field, and are deleted with it, which is also what makes roll-up summary fields possible. Lookups are loose, optional, and do not cascade.
</details>

---

### Question 8
**Scenario:** Duplicate accounts are being created by users.

A. Duplicate rules with matching rules, set to alert or block on create and edit
B. Data Loader, scheduled to export and de-duplicate the accounts each night after users have created them
C. A report that lists accounts with similar names so that users can check it before creating records
D. A validation rule that checks only the Account Name field for an exact text match with another record

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** A matching rule defines what counts as a duplicate, fuzzy matching included, and the duplicate rule defines what happens when one is found. Alert with a bypass is common for sales teams, since a hard block on a fuzzy match creates its own problem.
</details>

---

### Question 9
**Scenario:** A report must show accounts with no related opportunities.

A. A summary report grouped by account name, built on a report type that only returns accounts with opportunities
B. A joined report with two blocks
C. A standard report
D. A cross filter with "without" on the Opportunities object

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Cross filters express the "with or without related records" question that a plain filter cannot. The report type also matters: `Accounts with Opportunities` returns only accounts that have them, so the base type must include accounts without opportunities.
</details>

---

### Question 10
**Scenario:** 50,000 records must be updated from a spreadsheet.

A. Manual entry through the standard edit pages, working through batches of records one at a time
B. Data Loader, or the Import Wizard under its 50,000-record cap, matching on record IDs or an external ID
C. A report with inline editing turned on, saving the changes to all 50,000 rows at once
D. A flow that loops over the spreadsheet after it is attached to a record as a file, updating each row it finds

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** The Import Wizard handles up to 50,000 records for a subset of objects and does not support deletes; Data Loader handles larger volumes, all objects, and every operation. An external ID field lets you upsert without knowing Salesforce record IDs.
</details>

---

### Question 11
**Scenario:** Sales users must follow a defined selling process with different stages per business line.

A. Path only, configuring different guidance and key fields for each business line
B. One set of stages for everyone, told apart by a picklist field on the opportunity
C. Sales processes tied to record types, each exposing its own subset of opportunity stages, assigned by profile
D. Validation rules

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A sales process selects which stage values a record type offers, and Path then adds guidance and key fields on top for each stage. Path is a user-experience layer, not the control over which stages exist.
</details>

---

### Question 12
**Scenario:** Cases must route to the right support queue automatically.

A. Manual assignment by a support manager who watches the new case list and reassigns each case
B. Case assignment rules with ordered entry criteria, assigning to a queue or user
C. Escalation rules that reassign each case to the correct queue at the moment it is created
D. Auto-response rules that send the right team a notification email about each new case

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Assignment rules evaluate entries in order and stop at the first match, so ordering is the design decision. Escalation rules act on age and inactivity later in the case lifecycle, and auto-response rules only send email.
</details>

---

### Question 13
**Scenario:** A user reports they cannot see a field they were told they have access to.

A. Change the organization-wide default to Public Read/Write so that every user can see all fields and all records in the org
B. Check field-level security on the profile and permission sets, then the page layout for their record type
C. Give them the System Administrator profile to bypass layouts and security
D. Delete and recreate the field with the same API name, then re-add it to the page layouts

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Field visibility is the intersection of field-level security and the assigned layout, so the troubleshooting order is security first, layout second. Granting administrator rights to fix a visibility complaint replaces a small problem with a large one.
</details>

---

### Question 14
**Scenario:** Changes must move from a sandbox to production safely.

A. Edit production directly in Setup, making each change during a quiet window outside business hours
B. Data Loader, exporting the configuration records from the sandbox and importing them into production
C. Rebuild each change by hand in production while reading from a screenshot of the sandbox configuration
D. Change sets, or a source-driven SFDX pipeline with version control for larger teams

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Change sets are declarative and adequate for small changes, but they carry no version history and are one-directional. Source-driven development with a repository is what makes releases reviewable and repeatable as the team grows.
</details>

---

### Question 15
**Scenario:** Data must be recoverable after a bad bulk update.

A. The Recycle Bin for deletes within 15 days, plus your own Data Loader or export backup taken before any update
B. Salesforce Support restores any bulk change at no cost if a case is opened within the same week
C. Nothing can be done once a bulk update commits, because Salesforce keeps no history
D. A Rollback button in Setup that reverts the organization to its state before the bulk job ran

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** The Recycle Bin covers deletes, not overwrites, so a bad update needs your own prior extract to restore from. Taking an export before any bulk operation is the habit that makes this recoverable.
</details>

---

### Question 16
**Scenario:** Call center agents may log in to Salesforce only during their shift, 7 AM to 7 PM on weekdays, and only from the office network.

A. A validation rule on the User object that checks the current time
B. Login hours and login IP ranges on the agents' profile
C. A permission set that removes the API Enabled permission
D. Session timeout set to 12 hours in Session Settings

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Profiles can define login hours and trusted login IP ranges, and Salesforce refuses logins outside them. A validation rule on User only fires when a user record is saved, not at login. Removing API access does not restrict when or where people log in, and a session timeout only limits how long a session lasts.

**Key Concept:** [Data Security: Control Access to the Org](https://trailhead.salesforce.com/content/learn/modules/data_security/data_security_org)
</details>

---

### Question 17
**Scenario:** Opportunities are Private. All opportunities where Region equals West must be visible to every member of the West Sales public group, whoever owns them.

A. Change the opportunity organization-wide default to Public Read Only for all users
B. Ask each owner to share their West opportunities manually
C. Add the West Sales members to the Opportunity record type
D. Create a criteria-based sharing rule for Region equals West shared with the group

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Criteria-based sharing rules open access to records that match field criteria, regardless of owner, to groups or roles. Changing the org-wide default exposes every opportunity to everyone. Manual sharing depends on each owner and does not cover new records, and record types control processes and layouts, not record visibility.

**Key Concept:** [Data Security: Create Sharing Rules](https://trailhead.salesforce.com/content/learn/modules/data_security/data_security_sharing_rules)
</details>

---

### Question 18
**Scenario:** Ten permission sets together make up the Sales Ops job role. Admins want to assign them as one unit, but one member of that role must not get the Delete permission on Accounts that one of the sets includes.

A. A permission set group with a muting permission set
B. A cloned profile for that single user with Delete removed
C. Ten separate permission set assignments for every user
D. A validation rule that blocks deletes for that user

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** A permission set group bundles permission sets for one assignment, and a muting permission set inside a group removes specific permissions from that group's combined set. A cloned profile per exception multiplies maintenance. Assigning ten sets separately is exactly what the team wants to avoid, and validation rules do not run on delete.

**Key Concept:** [Permission Set Groups](https://trailhead.salesforce.com/content/learn/modules/permission-set-groups)
</details>

---

### Question 19
**Scenario:** Users viewing a Contact want to see the parent Account's Industry on the contact record, always current, without anyone entering it twice.

A. A roll-up summary field on Contact counting the Account
B. A custom text field on Contact updated by users when needed
C. A cross-object formula field on Contact referencing Account.Industry
D. A new lookup relationship from Account to Contact

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A cross-object formula can reference fields on a parent through the relationship, so it always shows the Account's current value with no data entry. Roll-up summaries go from children to a master-detail parent, not down to children. A manual text field drifts out of date, and a new lookup from Account to Contact points the wrong direction.

**Key Concept:** [Formulas and Validations](https://trailhead.salesforce.com/content/learn/modules/point_click_business_logic)
</details>

---

### Question 20
**Scenario:** On a Case, the Sub-Type picklist should only offer values relevant to the Type the user selected, such as Billing sub-types only when Type is Billing.

A. One record type per Type value with separate layouts
B. A field dependency with Type controlling Sub-Type
C. A validation rule that rejects invalid combinations
D. A global value set shared by Type and Sub-Type

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A dependent picklist filters its values based on the controlling field's selection, so users only see relevant options. A record type per value multiplies layouts and does not follow changes to Type on the same record. A validation rule reports errors after the fact instead of guiding the choice, and a global value set shares one value list without any dependency.

**Key Concept:** [Picklist Administration: Manage Your Picklist Values](https://trailhead.salesforce.com/content/learn/modules/picklist_admin/picklist_admin_manage)
</details>

---

### Question 21
**Scenario:** On the Opportunity record page, a "Closed Lost Details" component should appear only when Stage equals Closed Lost.

A. Create a separate page layout for Closed Lost opportunities and assign it by profile
B. Write an Apex trigger that hides the component on save
C. Make the component's fields required with a validation rule
D. Set a component visibility filter on Stage in the Lightning App Builder

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** Component visibility filters in the Lightning App Builder show or hide a component on a record page based on field values, permissions, or device, with no code. A page layout is assigned by profile and record type, not by Stage. Triggers run on the server and cannot change how a page renders, and validation rules enforce data, not visibility.

**Key Concept:** [Add Visibility Rules for Dynamic Pages](https://trailhead.salesforce.com/content/learn/modules/lightning_app_builder/add-visibility-rules-for-dynamic-pages-lab)
</details>

---

### Question 22
**Scenario:** A qualified lead from a new company is ready to become a customer opportunity. The rep wants the related records created in one step.

A. Convert the lead, creating an account, a contact, and optionally an opportunity
B. Clone the lead three times and change each clone's record type
C. Create the account, contact, and opportunity by hand, then delete the lead
D. Change the lead's status to Closed Won and let it become an opportunity

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Lead conversion creates (or matches) an account and contact and can create an opportunity, carrying over mapped fields and campaign history. Leads cannot be cloned into other objects. Creating records by hand and deleting the lead loses history and conversion reporting, and lead status alone never creates an opportunity.

**Key Concept:** [Leads and Opportunities for Lightning Experience](https://trailhead.salesforce.com/content/learn/modules/leads_opportunities_lightning_experience)
</details>

---

### Question 23
**Scenario:** Marketing runs a trade show and must track which leads and contacts attended, who responded, and the revenue from opportunities it influenced.

A. A custom checkbox on Lead named Attended Trade Show
B. A public group containing everyone who attended
C. A campaign with campaign members and opportunities linked to it
D. A Chatter group where attendees post comments

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** Campaigns track members (leads and contacts) with statuses such as Sent and Responded, and opportunities associated with the campaign roll up into its revenue fields, which supports ROI reporting. A checkbox records attendance but not responses or revenue. Public groups are for sharing, and a Chatter group is for discussion.

**Key Concept:** [Campaign Basics](https://trailhead.salesforce.com/content/learn/modules/campaign_basics)
</details>

---

### Question 24
**Scenario:** High-priority cases that stay open more than four hours must automatically be reassigned to a senior support queue and the manager notified.

A. An assignment rule on the Case object
B. An escalation rule with time-based actions
C. An auto-response rule for high-priority cases
D. A list view filtered on high-priority open cases

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** Escalation rules evaluate cases against criteria and, after a set time, reassign them and send notifications. Assignment rules route a case when it is created or edited, not after time passes. Auto-response rules email the customer, and a list view only shows cases without acting on them.

**Key Concept:** [Service Cloud: Automated Case Management](https://trailhead.salesforce.com/content/learn/modules/service_lex/service_lex_case_manage)
</details>

---

### Question 25
**Scenario:** Customers email support@ the company. Each email must automatically become a case in Salesforce, with replies threaded on the same case.

A. Email-to-Case routing addresses
B. An email template on the Case object
C. A Chatter email digest for support agents
D. Mass email to all contacts with open cases

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** Email-to-Case turns incoming emails to the routing address into cases and attaches later replies to the same case, keeping the conversation together. Email templates format outgoing messages. Chatter digests summarize feed activity, and mass email sends messages out rather than capturing them.

**Key Concept:** [Service Cloud: Automated Case Management](https://trailhead.salesforce.com/content/learn/modules/service_lex/service_lex_case_manage)
</details>

---

### Question 26
**Scenario:** A sales manager wants to be notified in their feed whenever the Amount or Stage of a key opportunity changes, without building automation.

A. A scheduled report emailed to the manager every Monday
B. A record-triggered flow that emails the manager on every edit of the record
C. A validation rule that blocks changes to Amount and Stage
D. Feed tracking on Opportunity and following the record in Chatter

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** With feed tracking enabled for those fields, changes post to the record's feed, and users who follow the record see them in their own feed. A weekly report is delayed and not tied to the change. A flow works but is automation the manager wanted to avoid, and a validation rule would stop the changes rather than announce them.

**Key Concept:** [Chatter Basics for Users](https://trailhead.salesforce.com/content/learn/modules/chatter_basics_for_users)
</details>

---

### Question 27
**Scenario:** One "My Pipeline" dashboard should show each sales rep only the opportunities they are allowed to see, instead of building a dashboard per rep.

A. A dashboard running as the system administrator
B. A dashboard per rep stored in private folders
C. A dynamic dashboard where the viewer is the running user
D. A report with a filter on the manager's name

<details>
<summary>Answer</summary>

**Correct: C**

**Why:** A dynamic dashboard runs as the logged-in viewer, so each person sees data according to their own access. A dashboard running as an administrator shows everyone the administrator's view of the data. One dashboard per rep is the maintenance the team wants to avoid, and a fixed filter on one manager shows every viewer the same records.

**Key Concept:** [Reports and Dashboards for Lightning Experience](https://trailhead.salesforce.com/content/learn/modules/lex_implementation_reports_dashboards/lex_implementation_reports_dashboards_visualizing_data)
</details>

---

### Question 28
**Scenario:** A report must group accounts into Small, Medium, and Large by Annual Revenue ranges, without creating a new field on Account.

A. A bucket field on Annual Revenue in the report
B. A roll-up summary field on Account
C. A new picklist field populated by Data Loader
D. A formula field on Account with CASE logic

<details>
<summary>Answer</summary>

**Correct: A**

**Why:** A bucket field lives in the report and sorts values into named categories, such as revenue ranges, with no schema change. Roll-up summaries aggregate child records and are fields on the object. A picklist filled by Data Loader and a formula field both add a new field, which the scenario rules out.

**Key Concept:** [Group and Categorize Your Data](https://trailhead.salesforce.com/content/learn/projects/create-reports-and-dashboards-for-sales-and-marketing-managers/group-and-categorize-your-data)
</details>

---

### Question 29
**Scenario:** Whenever an Opportunity is created or edited, its Next Step Due field must be set on the same record, with the best performance and no extra save.

A. An after-save record-triggered flow updating the record
B. A before-save record-triggered flow (fast field updates)
C. A scheduled flow that runs nightly over all opportunities
D. A screen flow that users launch from the record page

<details>
<summary>Answer</summary>

**Correct: B**

**Why:** A before-save flow changes field values on the triggering record before it is written, with no extra DML, which Salesforce documents as much faster than after-save updates. An after-save flow updating the same record performs a second save. A nightly flow leaves values wrong all day, and a screen flow depends on users remembering to run it.

**Key Concept:** [Record-Triggered Flows](https://trailhead.salesforce.com/content/learn/modules/record-triggered-flows)
</details>

---

### Question 30
**Scenario:** Any opportunity discount above 20% must be approved by the rep's manager before the quote can be sent, with the record locked while it waits.

A. A validation rule that blocks any discount above 20% on save
B. A sharing rule that gives managers edit access
C. A report of high discounts reviewed each week
D. An approval process with entry criteria on Discount

<details>
<summary>Answer</summary>

**Correct: D**

**Why:** An approval process routes records that meet entry criteria to an approver, locks them during approval, and runs actions on approval or rejection. A validation rule simply blocks the discount with no approval path. A sharing rule only grants access, and a weekly report finds problems after quotes have gone out.

**Key Concept:** [Business Process Automation](https://trailhead.salesforce.com/content/learn/modules/business_process_automation)
</details>

---

## Where to go deeper

- [Salesforce Administrator cert page](../../exams/salesforce/administrator/) - notes, practice plan, strategy
- [Platform Developer I practice questions](./salesforce-platform-developer-1.md) - the programmatic counterpart
- [IAM explained](https://security.noblerworks.com/learn/concepts/iam-explained/) - profiles and permissions in context
- **[📖 Salesforce Trailhead](https://trailhead.salesforce.com/credentials/administrator)** - official exam guide and study path
