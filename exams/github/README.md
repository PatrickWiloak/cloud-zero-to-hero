# GitHub certifications

Study guides for GitHub in this repo. For the full picture across every provider, see [STUDY-HUB.md](../../STUDY-HUB.md).

## Which GitHub exam should I take first?

Pick by the job you do with GitHub today.

- **New to GitHub? Start with [GitHub Foundations (GH-900)](foundations/).** It is the entry-level exam, with seven domains:
  1. Understand Git and GitHub basics - version control, Git versus GitHub, accounts and GitHub Flow.
  2. Work with GitHub repositories - key files, templates, insights and maintenance.
  3. Collaborate using GitHub - issues, pull requests, discussions, notifications, Gists, Wikis and Pages.
  4. Apply modern development practices - Actions at a purpose level, Copilot and Codespaces.
  5. Manage projects with GitHub - Projects layouts, labels, milestones and workflows.
  6. Understand privacy, security, and administration - 2FA, repository and organization roles, visibility and branch protection.
  7. Explore the GitHub community - open source, Sponsors, Marketplace, InnerSource, forks and templates.
- **Write CI/CD or automation? Take [GitHub Actions (GH-200)](actions/).** It is intermediate, with five domains:
  1. Author and manage workflows - triggers, jobs, matrices, contexts and outputs.
  2. Consume and troubleshoot workflows - reading runs, logs, artifacts and templates.
  3. Author and maintain actions - JavaScript, Docker and composite actions, and publishing them.
  4. Manage GitHub Actions for the enterprise - policies, runners at scale, secrets and variables.
  5. Secure and optimize automation - environments, script injection, `GITHUB_TOKEN`, OIDC and SHA pinning.
- **Own a GitHub organization or enterprise? Use the [GitHub Administration guide](administration/).** It covers identity and access, repository administration, Actions management, Advanced Security and enterprise governance.

GitHub rewrote both GH-900 and GH-200 in January 2026 and moved delivery to Microsoft Learn. Book and check the current skills measured there:

- **[📖 GitHub Foundations certification page](https://learn.microsoft.com/en-us/credentials/certifications/github-foundations/)** - GH-900 registration, price, languages and policies
- **[📖 GitHub Actions certification](https://learn.microsoft.com/en-us/credentials/certifications/github-actions/)** - GH-200 registration, logistics and practice assessment

### A suggested order if you want all three

1. **[GH-900 Foundations](foundations/)** - the GH-200 and Administration guides both name Foundations as the sensible or recommended first step, and its domain 6 introduces repository roles, visibility and branch protection that the later guides build on.
2. **[GH-200 Actions](actions/)** - it goes deep on environments, secrets and variables at organization, repository and environment level, and runner groups, which you then need to govern as an administrator.
3. **[Administration](administration/)** - its "Manage GitHub Actions" and "Manage Repositories" domains revisit runners, org-level secrets, branch protection and rulesets from the owner's side, so it is easiest once the other two are done.

<!-- BEGIN GENERATED: provider-certs - edit .github/scripts/build-provider-indexes.py, not this block -->

3 certifications in this repo. Counts and statuses are generated from [docs/certs.json](../../docs/certs.json).

| Cert | Code | Level | Status | Notes |
|------|------|-------|--------|------:|
| [GitHub Foundations (GH-900)](foundations/) | GH-900 | Foundational | Ready | 7 |
| [GitHub Actions Certification (GH-200)](actions/) | GH-200 | - | Ready | 6 |
| [GitHub Administration Certification](administration/) | - | - | Ready | 5 |

<!-- END GENERATED: provider-certs -->
