---
name: download-failed-retrieve-manually
description: The automated harvester could not fetch the package (HTTP 403/404/405/500, OSF/ICPSR/GitHub extraction error, or an auth-walled link). Use to drive a manual retrieval before any availability verdict is finalized.
---

# Scenario: Download failed — retrieve manually

The pipeline found a candidate link but could not download it, so it provisionally set
`code_availability` / `data_availability` to `no`. A failed download is **not** evidence
of absence — it is a retrieval problem to be resolved by hand before any verdict stands.

## How to recognize it
`additional_notes` contains one of:
- `download failed — HTTP 403` — server refused (bot-block / login wall). The package
  very likely exists; the script was blocked.
- `download failed — HTTP 404` — link is dead or wrong (stale DOI / URL).
- `download failed — HTTP 405 / 500` — host-side error.
- `Could not extract OSF node ID` / `Could not extract ICPSR project ID` /
  `Could not parse GitHub repo` — the repo was recognized but its ID/path couldn't be parsed.
- An auth-walled link (Google Drive folder, lab portal) that can't be opened directly.

## Handling steps (SOP §2 search order)
1. **Open the link in a browser.** A 403 usually resolves immediately by hand; download
   the package and file it under `code/` and `data/`.
2. **Read the article PDF itself**, not just the journal page — repository links live in
   acknowledgments, footnotes, and data sections (SOP §2.1).
3. **Check every author, routed by role** — code with the technical/methods/junior author,
   data-access details with the survey/admin-data author (SOP §2.2).
4. **Author personal sites, then project/lab sites** — where keyword search fails (SOP §2.3–4).
5. **Repositories, searched properly** — browse the author's GitHub *profile*, try the
   title as a CamelCase repo slug, check OSF / Dataverse / ICPSR / Zenodo (SOP §2.5).
6. For an **auth-walled** link you cannot open, record the landing URL and label the
   contents **unverified** (SOP §5) — do not assert what's inside.

## Status classification
**Pending** — do not finalize. Re-run the appropriate scenario skill once retrieved. Only
after the SOP §2 search comes up empty is the verdict `NEITHER` / "didn't find" (SOP §5),
unless the data are structurally unshareable.

## Replication implication
Unknown until retrieved. These are the highest-value manual-review targets, since most are
false negatives caused by a 403 or an unparseable repository link.
