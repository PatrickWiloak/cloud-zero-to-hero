---
last-updated: 2026-05-03
---

# GitHub Administration Certification Fact Sheet

## Exam Overview

**Exam Name:** GitHub Administration
**Duration:** 120 minutes
**Format:** Multiple choice (65 questions)
**Passing Score:** 70%
**Cost:** $99 USD
**Valid For:** 2 years
**Delivery:** Online proctored
**Prerequisites:** None (GitHub Foundations recommended)

**[📖 GitHub Certifications](https://learn.github.com/certifications)** - Registration and exam details
**[📖 GitHub Enterprise Cloud Docs](https://docs.github.com/en/enterprise-cloud@latest)** - Enterprise documentation

## Exam Domains

### Domain 1: Support GitHub Enterprise (15%)

**Enterprise Plans:**
| Plan | Description |
|------|-------------|
| Enterprise Cloud | SaaS-hosted, managed by GitHub |
| Enterprise Server | Self-hosted, on-premises or cloud IaaS |

**[📖 GitHub Enterprise](https://docs.github.com/en/enterprise-cloud@latest/admin/overview/about-github-enterprise-cloud)** - Enterprise overview

### Domain 2: Manage User Identities and Access (20%)

**SAML SSO:**
- Centralized authentication via identity provider (Okta, Azure AD, OneLogin)
- Users authenticate through IdP, then access GitHub
- Organization or enterprise-level configuration
- Recovery codes for emergency access

**SCIM Provisioning:**
- Automated user lifecycle management (create, update, deactivate)
- Syncs user accounts from IdP to GitHub
- Team membership can be synchronized with IdP groups
- Requires SAML SSO as a prerequisite

**Enterprise Managed Users (EMU):**
- Users provisioned and fully controlled by the enterprise
- Cannot create personal repositories or contribute to public repos
- Accounts are namespaced (username_company)
- Full control over all user activity

**Roles:**
| Role | Level | Capabilities |
|------|-------|-------------|
| Owner | Organization | Full admin, billing, settings |
| Member | Organization | Default role, read/write repos |
| Billing Manager | Organization | Billing only |
| Enterprise Owner | Enterprise | All orgs, policies, billing |
| Member | Enterprise | Default enterprise role |

**[📖 SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization)** - SSO configuration
**[📖 SCIM](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-scim-for-organizations)** - User provisioning

### Domain 3: Manage Repositories (15%)

**Branch Protection Rules:**
- Require pull request reviews before merging
- Require status checks to pass
- Require signed commits
- Require linear history
- Restrict who can push to the branch
- Lock branch (read-only)

**Repository Rulesets:**
- More flexible than branch protection rules
- Can target branches and tags
- Support bypass lists for specific actors
- Org-level rulesets apply across all repos
- Enterprise-level rulesets for global policies

**Custom Repository Roles:**
- Define custom permission sets beyond built-in roles
- Combine base role (read, triage, write, maintain, admin) with additional permissions
- Organization-level feature

**[📖 Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)** - Branch rules
**[📖 Repository Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets)** - Rulesets

### Domain 4: Manage GitHub Actions (20%)

**Actions Policies:**
- Control which actions can be used (all, local only, selected)
- Allow specific actions by owner or repository
- Set default GITHUB_TOKEN permissions
- Require approval for fork PR workflows

**Self-Hosted Runners:**
- Runner groups for access control
- Runner labels for capability-based routing
- Auto-scaling with Actions Runner Controller
- Security: never use with public repositories

**[📖 Actions Policies](https://docs.github.com/en/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization)** - Actions management

### Domain 5: Manage GitHub Advanced Security (15%)

**GHAS Features:**
- Code scanning (CodeQL analysis)
- Secret scanning (detect leaked credentials)
- Dependabot (dependency vulnerability alerts and updates)
- Security overview dashboard

**Administration:**
- GHAS licensing (per committer for private repos)
- Enable/disable at org or repo level
- Configure default setup vs advanced setup for code scanning
- Manage secret scanning custom patterns

**[📖 GHAS](https://docs.github.com/en/code-security/getting-started/github-security-features)** - Security features overview

### Domain 6: Enterprise Administration (15%)

**Audit Log:**
- Records all administrative actions
- Searchable by actor, action, and time range
- API access for programmatic querying
- Log streaming to external SIEM systems

**Enterprise Policies:**
- Repository creation policies
- Base permissions for organization members
- Actions usage policies
- Fork policies
- IP allow lists for API and web access

**GitHub Connect:**
- Links Enterprise Server to Enterprise Cloud
- Enables: unified search, unified contributions, Dependabot updates
- Requires outbound HTTPS connection

**[📖 Audit Log](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization)** - Audit logging
**[📖 Enterprise Policies](https://docs.github.com/en/enterprise-cloud@latest/admin/policies)** - Enterprise-level policies

## Exam Tips

1. **Focus on the 20% domains** - User Identity and Actions Management
2. **Know SAML vs SCIM** - SAML handles auth, SCIM handles provisioning
3. **Understand EMU** - Full enterprise control vs standard accounts
4. **Know branch protection vs rulesets** - Rulesets are newer and more flexible
5. **Audit log** - What is logged and how to access it
6. **Enterprise vs Organization** - Which features belong at which level

---

**Key Takeaway:** This exam is about managing GitHub at scale. Know identity management (SAML, SCIM, EMU), Actions policies and runner management, GHAS administration, and enterprise governance (audit logs, policies). Think like an administrator, not a developer.
