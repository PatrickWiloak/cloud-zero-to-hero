#!/usr/bin/env python3
"""Build docs/certs.json - the machine-readable index of every cert in exams/.

This file is the single source of truth for anything that counts or lists certs:
the STUDY-HUB provider table, the per-provider index READMEs, and the badge counts.
Generating those from one index is what stops them drifting apart, which is how
STUDY-HUB ended up advertising 122 certs across 22 providers when there were 133
across 26.

A cert directory is any directory under exams/ containing fact-sheet.md. Discovery
deliberately does not key off a notes/ subdir: a cert whose notes are still outlined
but undrafted is a cert, and is exactly the kind we most want to keep visible.

Fields are parsed from the exam-overview section of each fact-sheet, which comes in
two shapes across the repo:

    **Duration:** 130 minutes                 (bold key-value lines)
    | Duration | 4 hours (240 minutes) |      (a logistics table)

Unparseable fields come back null rather than guessed. Run with --report to see
per-field fill rates and which certs are missing what.

Run:    python3 .github/scripts/build-certs-index.py            # writes docs/certs.json
        python3 .github/scripts/build-certs-index.py --report   # fill-rate summary
        python3 .github/scripts/build-certs-index.py --check    # CI: fail if stale
"""

import json
import os
import re
import sys

EXAMS = "exams"
OUT = "docs/certs.json"

# Headings whose section carries the exam logistics.
OVERVIEW_HEADING = re.compile(
    r"^#{1,4}\s*[^\w\n]*\s*(exam\s+overview|exam\s+logistics|exam\s+details|"
    r"exam\s+facts|quick\s+facts|overview|at\s+a\s+glance)\b",
    re.I | re.M,
)
NEXT_HEADING = re.compile(r"^#{1,4}\s", re.M)

# Field label -> canonical key. Labels are matched lowercased and stripped.
FIELDS = {
    "exam code": "exam_code",
    "code": "exam_code",
    "exam name": "exam_name",
    "duration": "duration",
    "length": "duration",
    "questions": "questions",
    "question count": "questions",
    "number of questions": "questions",
    "passing score": "passing_score",
    "pass score": "passing_score",
    "cost": "cost",
    "cost (usd)": "cost",
    "price": "cost",
    "exam fee": "cost",
    "valid for": "validity",
    "validity": "validity",
    "delivery": "delivery",
    "format": "format",
    "question format": "format",
    "languages": "languages",
    "language": "languages",
    "level": "level",
    "prerequisites": "prerequisites",
}

PROVIDER_NAMES = {
    "anthropic": "Anthropic Claude",
    "aws": "AWS",
    "azure": "Azure",
    "cisco": "Cisco",
    "cloud-security-alliance": "Cloud Security Alliance",
    "comptia": "CompTIA",
    "confluent": "Confluent/Kafka",
    "databricks": "Databricks",
    "datadog": "Datadog",
    "finops": "FinOps Foundation",
    "gcp": "GCP",
    "github": "GitHub",
    "hashicorp": "HashiCorp",
    "ibm": "IBM Cloud",
    "isaca": "ISACA",
    "isc2": "ISC2",
    "kubernetes": "Kubernetes/CNCF",
    "linux-foundation": "Linux Foundation",
    "mongodb": "MongoDB",
    "nvidia": "NVIDIA",
    "offensive-security": "Offensive Security",
    "oracle": "Oracle Cloud (OCI)",
    "palo-alto-networks": "Palo Alto Networks",
    "redhat": "Red Hat",
    "salesforce": "Salesforce",
    "servicenow": "ServiceNow",
    "snowflake": "Snowflake",
    "splunk": "Splunk",
    "vmware": "VMware",
}

STANDARD_FILES = ["README.md", "fact-sheet.md", "practice-plan.md",
                  "scenarios.md", "strategy.md"]


def strip_md(value):
    """Flatten markdown emphasis and links in a field value."""
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = value.replace("**", "").replace("*", "").replace("`", "")
    return " ".join(value.split()).strip(" |")


def overview_section(text):
    """Return the exam-overview section, or the whole doc if no heading matches."""
    match = OVERVIEW_HEADING.search(text)
    if not match:
        return text
    rest = text[match.end():]
    nxt = NEXT_HEADING.search(rest)
    return rest[: nxt.start()] if nxt else rest


def parse_fields(section):
    """Pull known labels out of both the bold and table shapes."""
    found = {}
    for label, value in re.findall(r"^\*\*([^:*]{1,40}):\*\*\s*(.+)$", section, re.M):
        key = FIELDS.get(label.strip().lower())
        if key and key not in found:
            found[key] = strip_md(value)
    for label, value in re.findall(r"^\|\s*([^|]{1,40}?)\s*\|\s*([^|]+?)\s*\|", section, re.M):
        # Labels are often bolded inside the cell (| **Exam Code** | AIP-C01 |),
        # so strip markdown before matching or the lookup silently misses.
        key = FIELDS.get(strip_md(label).lower())
        if key and key not in found:
            cleaned = strip_md(value)
            if cleaned and not set(cleaned) <= {"-", ":"}:
                found[key] = cleaned
    return found


def title_of(path, fallback):
    """First H1, minus a trailing 'Fact Sheet' and any retirement suffix."""
    if not os.path.isfile(path):
        return fallback
    for line in open(path, encoding="utf-8"):
        if line.startswith("# "):
            title = strip_md(line[2:])
            title = re.sub(r"\s*[-–]\s*RETIRED\s*$", "", title, flags=re.I)
            # Page-type suffixes are about the document, not the certification.
            title = re.sub(r"\s*(Fact Sheet|Exam Guide|Certification Exam Guide)\s*$",
                           "", title, flags=re.I)
            return title.strip()
    return fallback


# Vendor exam codes: AZ-900, AI-102, SAA-C03, ANS-C01, PEN-200, 2V0-21.23.
CODE_PATTERN = re.compile(r"\b([A-Z]{2,4}\d?-[A-Z]?\d{2,3}(?:\.\d{2})?)\b")


def derive_exam_code(name, slug):
    """Recover an exam code the fact-sheet did not state outright.

    Two conservative rules, both precision-first. A wrong code is worse than a null:
    it would propagate into every generated table.

      1. A strict vendor code pattern anywhere in the title (AZ-900, MLS-C01).
      2. A parenthesised acronym, but only when it matches the directory slug.
         This accepts (LFCA) for linux-foundation/lfca and (CSA) for servicenow/csa,
         while rejecting (SRE) in "IBM Cloud Site Reliability Engineer (SRE)" and
         (GHAS) in "GitHub Advanced Security (GHAS)", which are abbreviations of the
         product, not exam codes.
    """
    match = CODE_PATTERN.search(name)
    if match:
        return match.group(1)
    slug_letters = slug.replace("-", "").upper()
    for token in re.findall(r"\(([A-Z]{2,6})\)", name):
        if token == slug_letters:
            return token
    return None


TIERS = ("foundational", "associate", "professional", "specialty", "expert")


def classify_level(rel_path, fields, name):
    """Resolve a cert's tier, most reliable signal first.

    Path tier dir (AWS-style) > a level stated in the fact-sheet > the cert's own
    title > the directory slug. The title matters most in practice: Microsoft and
    CNCF encode the tier in the exam name ("Azure Developer Associate", "Kubernetes
    and Cloud Native Associate") while the slug is just a code like az-204 or kcna.
    """
    parts = rel_path.split(os.sep)
    for tier in TIERS:
        if tier in parts:
            return tier

    declared = (fields.get("level") or "").lower()
    for tier in TIERS:
        if tier in declared:
            return tier

    haystack = f"{name} {parts[-1]}".lower()
    if re.search(r"\bfundamental|\bfoundation|\bpractitioner\b|\bdigital leader\b|\bentry\b", haystack):
        return "foundational"
    if re.search(r"\bexpert\b", haystack):
        return "expert"
    if re.search(r"\bspecialty\b|\bspecialist\b", haystack):
        return "specialty"
    if re.search(r"\bassociate\b", haystack):
        return "associate"
    if re.search(r"\bprofessional\b|\badvanced\b|\bpro\b", haystack):
        return "professional"
    if re.search(r"-900$|-90\d$", parts[-1]):
        return "foundational"
    return "unspecified"


def classify_status(cert_dir, notes_count):
    """Derive a cert's status from its README banner and whether notes exist.

      retired      the exam is withdrawn; the guide is kept for credential holders
      anticipated  a track for an exam the vendor has not announced; not real yet
      track        a self-directed study track spanning several exams or none,
                   e.g. the Anthropic tracks and the Azure/GCP GenAI dirs. Counting
                   these as certifications inflates the headline number
      outline      README, fact-sheet, and practice plan exist; notes are undrafted
      active       a real exam with drafted notes
    """
    readme = os.path.join(cert_dir, "README.md")
    head = ""
    if os.path.isfile(readme):
        head = open(readme, encoding="utf-8").read()[:2500].lower()
    if "retired" in head and ("was retired" in head or "- retired" in head):
        return "retired"
    if "anticipated study track" in head or "not a currently-available certification" in head:
        return "anticipated"
    if ("self-directed study track" in head or "study track, not" in head
            or "not a single microsoft certification" in head
            or "not a discrete certification" in head):
        return "track"
    if notes_count == 0:
        return "outline"
    return "active"


def frontmatter(path, key):
    """Read a single scalar key out of the leading YAML frontmatter block."""
    if not os.path.isfile(path):
        return None
    head = open(path, encoding="utf-8").read()[:600]
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", head, re.M)
    return match.group(1) if match else None


def frontmatter_date(path):
    value = frontmatter(path, "last-updated")
    return value if value and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) else None


def build():
    certs = []
    for root, dirs, files in os.walk(EXAMS):
        if "fact-sheet.md" not in files:
            continue
        rel = os.path.relpath(root, EXAMS)
        provider = rel.split(os.sep)[0]
        fact_sheet = os.path.join(root, "fact-sheet.md")
        text = open(fact_sheet, encoding="utf-8").read()
        fields = parse_fields(overview_section(text))

        notes_dir = os.path.join(root, "notes")
        notes = sorted(f for f in os.listdir(notes_dir)) if os.path.isdir(notes_dir) else []
        notes = [n for n in notes if n.endswith(".md")]

        slug = rel.split(os.sep)[-1]
        name = title_of(os.path.join(root, "README.md"), title_of(fact_sheet, slug))
        certs.append({
            "id": rel.replace(os.sep, "/"),
            "provider": provider,
            "provider_name": PROVIDER_NAMES.get(provider, provider),
            "slug": slug,
            "name": name,
            "exam_code": fields.get("exam_code") or derive_exam_code(name, slug),
            "level": classify_level(rel, fields, name),
            "status": classify_status(root, len(notes)),
            "duration": fields.get("duration"),
            "questions": fields.get("questions"),
            "passing_score": fields.get("passing_score"),
            "cost": fields.get("cost"),
            "validity": fields.get("validity"),
            "delivery": fields.get("delivery"),
            "format": fields.get("format"),
            "languages": fields.get("languages"),
            "path": f"{EXAMS}/{rel.replace(os.sep, '/')}",
            "notes_count": len(notes),
            "files": {f: os.path.isfile(os.path.join(root, f)) for f in STANDARD_FILES},
            "last_updated": frontmatter_date(fact_sheet),
            # Optional, declared by hand in the fact-sheet frontmatter. Lets
            # check-cert-freshness.py warn before an exam revision lands.
            "exam_version": frontmatter(fact_sheet, "exam-version"),
            "exam_retires": frontmatter(fact_sheet, "exam-retires"),
        })

    certs.sort(key=lambda c: c["id"])
    providers = {}
    for cert in certs:
        entry = providers.setdefault(cert["provider"], {
            "name": cert["provider_name"], "count": 0, "tracks": 0, "directories": 0,
            "path": f"{EXAMS}/{cert['provider']}/"})
        entry["directories"] += 1
        # "count" is certifications only, so the provider column sums to the
        # certification total. Study tracks are counted separately.
        if cert["status"] == "track":
            entry["tracks"] += 1
        else:
            entry["count"] += 1

    # Study tracks are not exams, so they are excluded from the certification count.
    tracks = [c for c in certs if c["status"] == "track"]
    cert_providers = {c["provider"] for c in certs if c["status"] != "track"}
    return {
        "_comment": "Generated by .github/scripts/build-certs-index.py. Do not edit by hand.",
        "totals": {
            "cert_directories": len(certs),
            "certifications": len(certs) - len(tracks),
            "study_tracks": len(tracks),
            "certification_providers": len(cert_providers),
            "provider_directories": len(providers),
        },
        "providers": dict(sorted(providers.items())),
        "certs": certs,
    }


def report(index):
    certs = index["certs"]
    print(f"{index['totals']['cert_directories']} cert dirs, "
          f"{index['totals']['certifications']} certifications, "
          f"{index['totals']['study_tracks']} study tracks, "
          f"{index['totals']['certification_providers']} cert providers\n")
    print("Field fill rates:")
    for key in ("exam_code", "duration", "questions", "passing_score", "cost",
                "validity", "delivery", "format", "languages"):
        filled = sum(1 for c in certs if c.get(key))
        print(f"  {key:<15} {filled:3d}/{len(certs)}  ({100 * filled // len(certs)}%)")
    print("\nStatus:")
    for status in ("active", "outline", "track", "retired", "anticipated"):
        hits = [c["id"] for c in certs if c["status"] == status]
        print(f"  {status:<12} {len(hits):3d}")
        if status in ("outline", "track", "retired", "anticipated"):
            for h in hits:
                print(f"      {h}")
    missing = [c["id"] for c in certs if not c["exam_code"]]
    if missing:
        print(f"\nNo exam code parsed ({len(missing)}):")
        for m in missing:
            print(f"  {m}")


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    index = build()
    rendered = json.dumps(index, indent=2, ensure_ascii=False) + "\n"

    if "--report" in sys.argv:
        report(index)
        return 0

    if "--check" in sys.argv:
        if not os.path.isfile(OUT):
            print(f"{OUT} is missing. Run: python3 .github/scripts/build-certs-index.py")
            return 1
        if open(OUT, encoding="utf-8").read() != rendered:
            print(f"{OUT} is out of date. Run: python3 .github/scripts/build-certs-index.py")
            return 1
        print(f"{OUT} is up to date ({index['totals']['cert_directories']} certs).")
        return 0

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(rendered)
    print(f"Wrote {OUT}: {index['totals']['cert_directories']} cert dirs, "
          f"{index['totals']['certification_providers']} certification providers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
