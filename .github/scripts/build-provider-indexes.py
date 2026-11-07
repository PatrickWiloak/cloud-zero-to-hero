#!/usr/bin/env python3
"""Generate navigation from docs/certs.json.

Three outputs, all derived from the cert index so their counts cannot drift:

  1. exams/<provider>/README.md - a per-provider index table. Six providers already
     have hand-written READMEs with real editorial content (provider history, full
     vendor catalogs including certs this repo does not cover). Those are preserved:
     only the block between the generated markers is replaced.

  2. The provider table in STUDY-HUB.md, between the same markers.

  3. The "Browse Certifications" table in README.md, likewise.

Counts, codes, levels, and statuses come from the index. The one-line "Highlights"
blurb per provider is editorial and stays curated below - one string, used by both
tables, so the two cannot describe the same provider differently.

The README table was hand-written until 2026-08-14, and by then had gone stale in
8 of 22 rows with 5 providers missing entirely: Kubernetes/CNCF read 7 against 12
and Azure 23 against 26, five days after the Tier 1 batch landed. Generating it is
what stops that recurring. `main()` also refuses to run if a provider has no
curated highlight or emoji, so a new provider fails CI rather than appearing as a
blank row.

Run:    python3 .github/scripts/build-provider-indexes.py
        python3 .github/scripts/build-provider-indexes.py --check   # CI: fail if stale
"""

import json
import os
import re
import sys

INDEX = "docs/certs.json"
HUB = "STUDY-HUB.md"
README = "README.md"
BEGIN = "<!-- BEGIN GENERATED: {} - edit .github/scripts/build-provider-indexes.py, not this block -->"
END = "<!-- END GENERATED: {} -->"

LEVEL_ORDER = ["foundational", "associate", "professional", "specialty", "expert", "unspecified"]
LEVEL_LABEL = {
    "foundational": "Foundational", "associate": "Associate", "professional": "Professional",
    "specialty": "Specialty", "expert": "Expert", "unspecified": "-",
}
STATUS_LABEL = {
    "active": "Ready",
    "outline": "Outline ◇",
    "track": "Study track",
    "retired": "Retired",
    "anticipated": "Anticipated",
}

# Curated, not generated. One line per provider, shown in both provider tables.
# A sample of what the provider covers, not an exhaustive list - the Certs column
# carries the total, and both tables say so underneath.
PROVIDER_HIGHLIGHTS = {
    "aws": "CLF-C02, SAA-C03, SOA-C03, DVA-C02, SAP-C02, DOP-C02, Advanced Networking (ANS-C01), SAP on AWS (PAS-C01), Quantum (QPC-C01); retired SOA-C02 retained",
    "azure": "AZ-900/104/204/305/400/700, MS-900, PL-100/200/900",
    "gcp": "Digital Leader, Associate Cloud Engineer, Cloud Architect, Cloud Developer, DevOps, Network Engineer, Workspace Admin",
    "kubernetes": "KCNA, CKA, CKAD, plus Argo (CAPA), Cilium (CCA), GitOps (CGOA), Istio (ICA), Kyverno (KCA), OpenTelemetry (OTCA), Prometheus (PCA), Platform Engineering (CNPA)",
    "nvidia": "AI Infra & Ops, GenAI/LLM, Multimodal, Agentic AI, Networking, OpenUSD",
    "hashicorp": "Terraform Assoc + Pro, Consul, Packer, Nomad",
    "databricks": "Data Engineer (A/P), ML (A/P), GenAI Engineer, Lakehouse Admin",
    "snowflake": "SnowPro Core + 3 Advanced (Architect, Data Eng, Admin)",
    "github": "Foundations, Actions, Administration",
    "redhat": "RHCSA (EX200), OpenShift Administrator (EX280)",
    "cisco": "CCNA (200-301), CCNP Enterprise ENCOR (350-401)",
    "salesforce": "Administrator, Platform Developer I, Platform Developer II",
    "confluent": "Certified Developer, Certified Administrator",
    "mongodb": "Associate Developer, DBA, Atlas Administrator",
    "finops": "Practitioner, Engineer, Analyst, Professional",
    "comptia": "A+ (220-1201/1202), Cloud+ (CV0-004), Network+ (N10-009)",
    "isc2": "CISSP, CCSP, CC",
    "isaca": "CISA, CISM",
    "cloud-security-alliance": "CCSK v5",
    "offensive-security": "OSCP (PEN-200)",
    "palo-alto-networks": "PCNSA",
    "linux-foundation": "LFCS, LFCA",
    "oracle": "OCI Foundations, Architect Assoc + Pro, Developer Assoc, Operations Assoc",
    "ibm": "Advocate, Developer, Solution Architect, SRE",
    "servicenow": "Certified System Administrator",
    "vmware": "VCP-DCV (2V0-21.23)",
    "anthropic": "Associate (CCAO-F), Developer (CCDV-F), Architect Foundations (CCAR-F) + Professional (CCAR-P)",
}

# Also curated. The README table leads each row with an icon; the rest of that
# file does the same, so a generated table without one would read as a foreign
# object on the page.
PROVIDER_EMOJI = {
    "aws": "☁️", "azure": "☁️", "gcp": "☁️", "kubernetes": "☸️", "nvidia": "🟢",
    "hashicorp": "🔧", "databricks": "🧱", "snowflake": "❄️", "github": "🐙",
    "redhat": "🎩", "cisco": "🌐", "salesforce": "☁️", "confluent": "📊",
    "mongodb": "🍃", "finops": "💰", "comptia": "🔒", "isc2": "🛡️", "isaca": "🛡️",
    "cloud-security-alliance": "☁️", "offensive-security": "🎯",
    "palo-alto-networks": "🔥", "linux-foundation": "🐧", "oracle": "☁️",
    "ibm": "☁️", "servicenow": "🧰", "vmware": "🖥️", "anthropic": "🤖",
}

# Order both provider tables the same way: cloud first, then platforms, then the
# security and vendor certifications. A provider missing from this list sorts to
# the end alphabetically rather than disappearing.
PROVIDER_ORDER = [
    "aws", "azure", "gcp", "kubernetes", "nvidia", "anthropic", "hashicorp",
    "databricks", "snowflake", "github", "redhat", "cisco", "salesforce",
    "confluent", "mongodb", "finops", "comptia", "isc2", "isaca",
    "cloud-security-alliance", "offensive-security", "palo-alto-networks",
    "linux-foundation", "oracle", "ibm", "servicenow", "vmware",
]

# Headings the six hand-written READMEs already use for their repo-guide section.
REPO_SECTION = re.compile(
    r"^##\s+(?:Certifications?|Available Study Guides?|Study Guides?)\s+in\s+[Tt]his\s+[Rr]epo(?:sitory)?\s*$",
    re.M,
)


def sort_key(cert):
    return (LEVEL_ORDER.index(cert["level"]), cert["name"].lower())


def provider_table(certs, from_provider_dir):
    """Render the cert table. Paths are relative to the file the table lands in."""
    rows = [
        "| Cert | Code | Level | Status | Notes |",
        "|------|------|-------|--------|------:|",
    ]
    for cert in sorted(certs, key=sort_key):
        # Provider README lives at exams/<provider>/, so strip that prefix.
        link = cert["path"].split("/", 2)[2] if from_provider_dir else cert["path"]
        code = cert["exam_code"] or "-"
        notes = cert["notes_count"] or "-"
        rows.append(
            f"| [{cert['name']}]({link}/) | {code} | {LEVEL_LABEL[cert['level']]} "
            f"| {STATUS_LABEL[cert['status']]} | {notes} |"
        )
    return "\n".join(rows)


def legend(certs):
    notes = []
    if any(c["status"] == "outline" for c in certs):
        notes.append(
            "◇ **Outline** - README, fact-sheet, and practice plan are written; topic notes "
            "are outlined but not yet drafted."
        )
    if any(c["status"] == "retired" for c in certs):
        notes.append(
            "**Retired** - the exam is no longer offered. The guide is kept for anyone "
            "holding the credential, and points to its replacement."
        )
    if any(c["status"] == "anticipated" for c in certs):
        notes.append(
            "**Anticipated** - a self-directed study track for an exam the vendor has not "
            "formally announced. Not a real certification yet."
        )
    if any(c["status"] == "track" for c in certs):
        notes.append(
            "**Study track** - a self-directed guide spanning several exams or none. Not a "
            "certification, and not counted as one."
        )
    return ("\n\n" + "\n\n".join(notes)) if notes else ""


def generated_block(name, body):
    return f"{BEGIN.format(name)}\n\n{body}\n\n{END.format(name)}"


def splice(text, name, body):
    """Replace an existing generated block, or return None if there is not one."""
    pattern = re.compile(
        re.escape(BEGIN.format(name)) + r".*?" + re.escape(END.format(name)), re.S
    )
    if not pattern.search(text):
        return None
    return pattern.sub(lambda _: generated_block(name, body), text)


def build_provider_readme(provider, provider_name, certs, existing):
    table = provider_table(certs, from_provider_dir=True)
    exams_n = sum(1 for c in certs if c["status"] != "track")
    tracks_n = len(certs) - exams_n
    parts = []
    if exams_n:
        parts.append(f"{exams_n} certification{'s' if exams_n != 1 else ''}")
    if tracks_n:
        parts.append(f"{tracks_n} self-directed study track{'s' if tracks_n != 1 else ''}")
    summary = (
        f"{' and '.join(parts)} in this repo. "
        f"Counts and statuses are generated from [docs/certs.json](../../docs/certs.json)."
    )
    body = f"{summary}\n\n{table}{legend(certs)}"
    block = generated_block("provider-certs", body)

    if existing is None:
        return (
            f"# {provider_name} certifications\n\n"
            f"Study guides for {provider_name} in this repo. For the full picture across "
            f"every provider, see [STUDY-HUB.md](../../STUDY-HUB.md).\n\n"
            f"{block}\n"
        )

    spliced = splice(existing, "provider-certs", body)
    if spliced is not None:
        return spliced

    # First run against a hand-written README: replace the body of its existing
    # repo-guides section, keeping the heading and everything else in the file.
    match = REPO_SECTION.search(existing)
    if match:
        rest = existing[match.end():]
        nxt = re.search(r"^##\s", rest, re.M)
        tail = rest[nxt.start():] if nxt else ""
        return existing[: match.end()] + "\n\n" + block + "\n\n" + tail
    return existing.rstrip() + "\n\n## Study guides in this repo\n\n" + block + "\n"


def provider_order(providers):
    ordered = [p for p in PROVIDER_ORDER if p in providers]
    return ordered + sorted(p for p in providers if p not in ordered)


def build_readme_table(index):
    """The compact provider table on the repo's front page.

    Shorter than the STUDY-HUB one on purpose: this is a directory, not the
    reference. The provider name is the link, so there is no separate Browse
    column.
    """
    providers = index["providers"]
    totals = index["totals"]
    rows = ["| Provider | Certs | Highlights |", "|----------|------:|------------|"]
    for provider in provider_order(providers):
        entry = providers[provider]
        rows.append(
            f"| {PROVIDER_EMOJI[provider]} [{entry['name']}](./{entry['path']}) "
            f"| {entry['count']} | {PROVIDER_HIGHLIGHTS[provider]} |"
        )
    # Study tracks are named only when there are any. Since the 2026-10-21 split
    # this site has none (the Anthropic and GenAI tracks moved to the AI site), and
    # "plus 0 self-directed study tracks" reads as a mistake.
    tracks_n = totals["study_tracks"]
    tracks_note = (
        f", plus {tracks_n} self-directed study track{'s' if tracks_n != 1 else ''}"
        if tracks_n else ""
    )
    rows.append(
        f"| **Total** | **{totals['certifications']}** "
        f"| across {totals['certification_providers']} providers{tracks_note} |"
    )
    return "\n".join(rows) + (
        "\n\nHighlights are a sample, not the full list - the Certs column is the "
        "total. Open a provider for everything it covers."
    )


def build_hub_table(index):
    providers = index["providers"]
    certs_by_provider = {}
    for cert in index["certs"]:
        certs_by_provider.setdefault(cert["provider"], []).append(cert)

    ordered = provider_order(providers)

    rows = ["| Provider | Certs | Highlights | Browse |", "|----------|------:|------------|--------|"]
    for provider in ordered:
        entry = providers[provider]
        notes = []
        outline = sum(1 for c in certs_by_provider[provider] if c["status"] == "outline")
        if outline:
            notes.append(f"{outline} at outline stage ◇")
        if entry["tracks"]:
            notes.append(f"+{entry['tracks']} study track{'s' if entry['tracks'] != 1 else ''}")
        highlight = PROVIDER_HIGHLIGHTS.get(provider, "")
        if notes:
            suffix = "(" + "; ".join(notes) + ")"
            highlight = f"{highlight} {suffix}" if highlight else suffix
        rows.append(
            f"| **{entry['name']}** | {entry['count']} | {highlight} "
            f"| [{entry['path']}](./{entry['path']}) |"
        )
    totals = index["totals"]
    rows.append(
        f"| **CERTIFICATIONS TOTAL** | **{totals['certifications']}** "
        f"| across {totals['certification_providers']} providers | |"
    )
    tracks_legend = (
        f"\n\nThe Certs column counts real exams. This repo also carries "
        f"{totals['study_tracks']} self-directed study track"
        f"{'s' if totals['study_tracks'] != 1 else ''}, which are study guides "
        f"spanning several exams or none, not certifications in their own right."
        if totals["study_tracks"] else ""
    )
    legend_text = (
        tracks_legend
        + "\n\n◇ = outline stage: README, fact-sheet, and practice plan are written; topic "
        "notes are outlined but not yet drafted. See [TODO.md](https://github.com/PatrickWiloak/cloud-zero-to-hero/blob/main/TODO.md) for the drafting "
        "queue."
    )
    return "\n".join(rows) + legend_text


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    check = "--check" in sys.argv
    if not os.path.isfile(INDEX):
        print(f"{INDEX} is missing. Run: python3 .github/scripts/build-certs-index.py")
        return 1
    index = json.load(open(INDEX, encoding="utf-8"))

    # A provider with no curated highlight or icon would render as a blank cell
    # in both tables. Fail here instead: this is the check that would have caught
    # ISACA, Offensive Security, Palo Alto Networks, ServiceNow and VMware
    # missing from the README table for five days.
    for name, mapping in (("PROVIDER_HIGHLIGHTS", PROVIDER_HIGHLIGHTS), ("PROVIDER_EMOJI", PROVIDER_EMOJI)):
        missing = sorted(p for p in index["providers"] if p not in mapping)
        if missing:
            print(f"{name} has no entry for: {', '.join(missing)}")
            print(f"Add one line per provider in {os.path.relpath(__file__)}, then re-run.")
            return 1

    by_provider = {}
    for cert in index["certs"]:
        by_provider.setdefault(cert["provider"], []).append(cert)

    stale, written = [], 0
    for provider, certs in sorted(by_provider.items()):
        path = f"exams/{provider}/README.md"
        existing = open(path, encoding="utf-8").read() if os.path.isfile(path) else None
        rendered = build_provider_readme(
            provider, index["providers"][provider]["name"], certs, existing)
        if existing == rendered:
            continue
        if check:
            stale.append(path)
        else:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(rendered)
            written += 1

    tables = [
        (HUB, "provider-table", build_hub_table(index)),
        (README, "readme-provider-table", build_readme_table(index)),
    ]
    for path, marker, body in tables:
        current = open(path, encoding="utf-8").read()
        spliced = splice(current, marker, body)
        if spliced is None:
            print(f"{path} has no '{marker}' generated markers. Add them around the "
                  f"provider table so it can be regenerated.")
            return 1
        if spliced != current:
            if check:
                stale.append(path)
            else:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(spliced)
                written += 1

    if check:
        if stale:
            print("Generated navigation is out of date:")
            for path in stale:
                print(f"  {path}")
            print("\nRun: python3 .github/scripts/build-certs-index.py && "
                  "python3 .github/scripts/build-provider-indexes.py")
            return 1
        print(f"Navigation is up to date ({len(by_provider)} provider indexes, "
              f"{HUB} and {README} tables).")
        return 0

    print(f"Wrote {written} file(s): {len(by_provider)} provider indexes checked, "
          f"{HUB} and {README} tables refreshed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
