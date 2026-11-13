# Drafts

Pages drafted by the nobler-os `content-z2h-cloud` loop (`scripts/loops/content-refill.mjs`, pilot since
2026-11-13). This folder is **not part of the site**: `build-site.py` stages only its listed content
directories, so nothing here is published. The link checker skips it too.

Each draft sits at `drafts/<section>/<slug>.md`, and its relative links are written for where it will
live once published (`<section>/<slug>.md`), so they only resolve after the move. The loop drafts at
most two pages a week and stops while two are waiting here.

## Publish a draft

Read it first. Every fact should match the vendor docs it cites. Then:

```bash
cd ~/coding/cloud-zero-to-hero
f=drafts/learn/concepts/example.md            # the draft
git mv "$f" "${f#drafts/}"
# link the page from its section's README.md (and a topic index if one fits)
python3 .github/scripts/check-readme-counts.py --fix
python3 .github/scripts/check-internal-links.py
git add -A learn resources README.md STUDY-HUB.md && git commit -m "content: publish <slug> (loop draft)"
ship cloud-zero-to-hero --no-deploy                           # the push deploys the site (docs-site.yml)
```

## Reject a draft

Delete it (`git rm`) and commit. The loop remembers every topic it drafted and will not draft the same
one again.
