<!--
  Site-only landing page. Rendered over the staged copy of README.md by
  .github/scripts/build-site.py; the repo's own README.md is never touched.

  The two pages have different jobs. README.md is a repo front page: badges,
  repository structure, contributing, "star this repo". This is a website
  landing page: what the site is, who it is for, and the four or five links a
  first-time visitor actually needs.

  Never hard-code a count here. Every number is a double-braced token filled from
  docs/certs.json and from check-readme-counts.py's gather(), which is the same
  counting code CI runs against the README - so a number on this page cannot
  drift away from the tree. Adding a new number means adding a token, not
  typing a figure.

  No `hide: toc` here. With toc.integrate the page's headings fold into the left
  sidebar, and hiding them would make Home the one page whose sections do not
  appear where every other page's do.
-->
<!-- markdownlint-disable MD030 -->
<!-- Material's card grids use `-   ` (three spaces) so the card body lines up at
     a four-space indent and stays part of the list item. MD030 wants one. -->


<div class="home-hero" markdown>

# Cloud, from zero to hero { .home-title }

<p class="home-intro">AWS, Azure, GCP, OCI, Kubernetes, Linux, networking, Terraform, DevOps, SRE and FinOps. Plain-English concepts, hands-on builds, deep references, and a full cloud certification library - free, no signup, nothing gated.</p>

<p class="home-sub">Never opened a terminal, or chasing your fifth cloud cert - both start here. Press <kbd>/</kbd> to search all {{words}} words.</p>

[Start from zero](learn/day-one/){ .md-button .md-button--primary }
[Browse {{certifications}} certifications](STUDY-HUB.md){ .md-button }
[Look up a concept](learn/concepts/){ .md-button }

<div class="stat-strip" markdown>

- **{{certifications}}** certifications
- **{{providers}}** providers
- **{{words}}** words
- **{{doc_links}}** vendor doc links
- **{{concept_pages}}** concept pages
- **{{hands_on_projects}}** hands-on builds

</div>

</div>

<p class="home-kicker">The four pillars</p>

## Four ways in

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Learn**

    ---

    Plain English, no exam scaffolding. A strict-beginner on-ramp, {{concept_pages}} bite-size concept pages, and a structured path from zero to cloud.

    [:octicons-arrow-right-24: Start learning](learn/)

-   :material-hammer-wrench:{ .lg .middle } **Build**

    ---

    {{hands_on_projects}} guided builds with inline code and time estimates, {{architecture_patterns}} architecture patterns, {{cli_cheat_sheets}} CLI cheat sheets.

    [:octicons-arrow-right-24: Build something](resources/hands-on-projects/)

-   :material-certificate-outline:{ .lg .middle } **Certify**

    ---

    {{certifications}} cert guides across {{providers}} providers, each with a fact sheet, practice plan, scenarios, and exam-day strategy.

    [:octicons-arrow-right-24: Find your cert](STUDY-HUB.md)

-   :material-book-search-outline:{ .lg .middle } **Reference**

    ---

    {{service_comparisons}} cross-cloud service comparisons, {{roadmaps}} career roadmaps, plus FinOps, migration, well-architected and troubleshooting deep dives.

    [:octicons-arrow-right-24: Browse reference](resources/)

</div>

<p class="home-kicker">Quick links</p>

## Jump to what you need

<div class="home-links" markdown>

- [Day One](learn/day-one/) - terminal, git, HTTP and servers, assuming nothing
- [Cloud from Scratch](learn/cloud-from-scratch.md) - compute, storage, networking, identity
- [Concepts](learn/concepts/) - {{concept_pages}} five-minute explainers, one cloud idea each
- [Topic indexes](topics/) - {{topic_indexes}} subjects tied across all four pillars
- [Glossary](learn/glossary.md) - the vocabulary, defined once
- [Cross-site learning paths](learn/learning-paths.md) - seven routes that span cloud, data, security and AI
- [Hands-on projects](resources/hands-on-projects/) - {{hands_on_projects}} builds you can finish in a sitting
- [Labs by certification](resources/hands-on-projects/labs-by-cert.md) - which build backs which exam
- [Practice questions](resources/practice-questions/) - scenario banks with explained answers
- [Interview prep](resources/interview-prep/) - {{interview_prep}} role-specific guides
- [Freshness ledger](docs/freshness.md) - what was last verified, and when
- [Curated YouTube](learn/youtube.md) - the videos worth your time
- [Which Zero to Hero site?](learn/which-site.md) - cloud, data, security or AI: pick by goal

</div>

<p class="home-kicker">The library</p>

## Certifications by provider

<div class="provider-grid" markdown>

{{provider_chips}}

</div>

[Full per-provider breakdown](STUDY-HUB.md#-certifications-by-provider){ .md-button }

## What's new

{{whats_new}}

## More Zero to Hero

Cloud is one of four free sites. When your study crosses into another subject, the sibling site covers it in the same depth.

<div class="grid cards" markdown>

-   :material-database-outline:{ .lg .middle } **Data Zero to Hero**

    ---

    Data engineering, databases, streaming and analytics, with Snowflake, Databricks and cloud data certifications.

    [:octicons-arrow-right-24: data.noblerworks.com](https://data.noblerworks.com/)

-   :material-shield-lock-outline:{ .lg .middle } **Security Zero to Hero**

    ---

    Cloud and application security, identity, compliance, and certifications from Security+ to CISSP.

    [:octicons-arrow-right-24: security.noblerworks.com](https://security.noblerworks.com/)

-   :material-robot-outline:{ .lg .middle } **AI Zero to Hero**

    ---

    LLMs, RAG, agents and evals in plain English, AI at work, AI certifications, and landmark papers explained.

    [:octicons-arrow-right-24: ai.noblerworks.com](https://ai.noblerworks.com/)

</div>

All four are free, by [Nobler Works](https://noblerworks.com/). Not sure which to start with? [Pick a site by your goal](learn/which-site.md).

## Who made this

Built by **[Patrick Wiloak](https://patricklukewilson.com)** - ex-AWS Solutions Architect, 10 years in tech, multi-cloud certified.
[YouTube](https://youtube.com/@patrickwiloak) · [LinkedIn](https://www.linkedin.com/in/patricklukewilson/) · [Website](https://patricklukewilson.com) · [Source on GitHub](https://github.com/PatrickWiloak/cloud-zero-to-hero)

We build custom software and products at **[Nobler Works](https://noblerworks.com/)**. Open-source training like this is how we give back - we are nothing without the community that supports us. If you need software built, [get in touch](https://noblerworks.com/).

!!! tip "Want the reps as well as the material?"

    [![gitGood.dev - practice questions, coding challenges, system design and cloud certification practice exams for engineers, data, security, DevOps and product technologists](assets/brand/gitgood-banner.png){ width="300" }](https://gitgood.dev)

    This site gives you the material. **[gitGood](https://gitgood.dev)** gives you the reps, and tells you whether you actually know it. Built for every kind of technologist across 21 role-targeted learning paths - engineering, SRE and DevOps, cloud architecture, security, ML and AI, data science, analytics and engineering, QA, product and TPM, and new grads breaking in.

    1,950+ practice questions across 34 categories · certification practice exams for AWS CLF-C02, SAA-C03 and DVA-C02, Azure AZ-900, AZ-104, AZ-305 and AI-900, Google Cloud Digital Leader and Associate Cloud Engineer, Kubernetes CKA and CKAD, CompTIA Security+ and HashiCorp Terraform Associate - original scenario questions, never brain dumps, with per-domain scoring and a timed simulator · coding challenges · SQL playground · system design walkthroughs · AI mock interviews · AI resume reviews · salary coaching · live job-market pulse.

    A 7-day free trial, then $8/month or $64/year. The free tier needs no card.

## Fine print

Free for educational use with attribution. Every technical claim links to the vendor's own documentation - {{doc_links}} links across the site.

This is an independent educational resource. It is not affiliated with, endorsed by, or sponsored by AWS, Microsoft, Google, Oracle, IBM, or any other vendor referenced. All trademarks belong to their respective owners.

Found something wrong or out of date? [Contributions welcome](CONTRIBUTING.md).
