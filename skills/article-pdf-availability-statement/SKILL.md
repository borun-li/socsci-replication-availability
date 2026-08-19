---
name: article-pdf-availability-statement
description: FALLBACK source — used only after the article page's SUPPLEMENTAL MATERIAL tab has NO replication package. The package link may be inside the article PDF (a data/code availability statement, a footnote, or the acknowledgments). Only treat a PDF link as the package if the text EXPLICITLY says "replication package/material"; otherwise a bare OSF/DOI link is likely a citation, not the deposit.
---

# Source: the article PDF (data/code statement / footnote / acknowledgments)

## Order of operations (SOP §2 — do NOT skip)
1. **First, check the article page's SUPPLEMENTAL MATERIAL tab** (skill
   `journal-reproducibility-package`). For Sociological Science this is where the package is
   published as a "Reproducibility Package" / "replication materials" line, e.g.
   *"GitHub replication materials: https://github.com/…"*. If it is there → route to the host
   skill and STOP; you do not need the PDF.
2. **Only if the SUPPLEMENTAL MATERIAL tab has no replication package**, come here and read
   the PDF itself.

## When you get routed here
The SUPPLEMENTAL MATERIAL tab showed no package (common for **pre-policy** papers). The
availability statement or repo link may still live in the manuscript.

## Step-by-step: LOCATE
1. Download the article PDF (the "PDF" / "Download" link on the article page) and read it.
2. Search the full text for these cues: `replication package`, `replication material`,
   `data availability`, `code availability`, `available at`, `available upon request`,
   `github`, `osf`, `dataverse`, `zenodo`, `figshare`, `doi.org/10.`.
3. Check specifically: a dedicated **data/code availability** statement, **footnotes /
   endnotes**, the **acknowledgments**, and the **first-page author-note**.
4. Extract every candidate URL/DOI **with the exact sentence around it** — that sentence is
   the provenance and decides whether it is really the package (next rule).

## CRITICAL RULE — do not mistake a citation for the package
**A bare OSF / DOI / database link in the PDF is NOT the replication package unless the
surrounding text explicitly says "replication package", "replication material(s)", or a
clear equivalent ("code/data to replicate this article", "our replication files").**
If nothing near the link says that, **do not** assume an OSF or database link is the deposit —
it is very likely a *citation* (e.g. to guidelines, a prior study, or a dataset the paper
merely cites). Treat it as provenance-`mismatch` and do not record it as the package.

## Step-by-step: DOWNLOAD
5. For a link that DOES pass the rule above, resolve it and hand off to the matching host
   skill (`github-repository-and-pages`, `osf-repository`, `data-repository`).
6. If the statement says "available on request," record the exact **`apply_at`** URL and flag
   `needs_review: on_request_gated_data` — do not mark NEITHER.

## Gotchas
- A **scanned/image PDF** won't be text-searchable — read the acknowledgments and footnotes
  by eye; don't conclude "no statement" from a failed text search alone.
- The statement may name a host without a live link (e.g. "deposited at ICPSR") → search that
  host directly via `data-repository`.
- "Available from the authors" is a real (weak) signal — route to `author-homepage`.

## Worked example (from corpus) — CAUTIONARY: missing-main-effect (v2-20-420, Breznau 2015)
1. **Tab first:** the article page's SUPPLEMENTAL MATERIAL tab DID carry the package —
   *"GitHub replication materials: https://github.com/nbreznau/Replication-Brooks-Manza"* →
   the correct action is to route to `github-repository-and-pages` and download. **The PDF was
   not needed.**
2. **The trap:** scanning the PDF surfaced one OSF link in footnote 9 — `https://osf.io/9f6gx`.
   It is a *real, live* node, but nothing near it says "replication package/material"; on check
   it is the **"Transparency and Openness Promotion (TOP) Guidelines"** — a citation, **not**
   this paper's deposit. Per the CRITICAL RULE, do **not** record it as the package.
3. Lesson: check the tab first; and never promote a bare in-PDF OSF/DOI link to "the package"
   without an explicit "replication material" phrase.

## After download → `calibration-honesty`
A qualifying in-PDF statement ("replication materials at …") is strong path-provenance —
record it. A bare citation link is not; reject it (provenance mismatch).
