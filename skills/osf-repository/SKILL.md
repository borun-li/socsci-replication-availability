---
name: osf-repository
description: The replication package is on the Open Science Framework (osf.io) — usually reached from the journal SUPPLEMENTAL MATERIAL tab, the PDF, or an author page. Step-by-step to open the OSF node, navigate its files/components, and download the package.
---

# Source: OSF (osf.io)

## When you get routed here
An `osf.io/<node>` link — most often handed over by `journal-reproducibility-package`
(the "Reproducibility Package:" line usually points to OSF), or from the PDF / author page.
SocArXiv preprints are also OSF-hosted, so tell a package project from a preprint.

## Step-by-step: LOCATE
1. Open the node URL; note the short node ID (e.g. `osf.io/rhd8y`). An `/overview` or
   `/files/...` suffix still resolves to the same node.
2. Identify the node type: **Project** (has Files + Components — the package lives here),
   **Preprint** (a manuscript — look for a linked project), or **Registration** (a frozen
   snapshot that may hold the materials).
3. Go to **Files**. Check **OSF Storage** and any linked add-on storage (Google Drive,
   Dropbox, GitHub, Box) shown as separate roots.
4. Expand **Components** (left panel) — code and data are often split across child
   components rather than sitting on the top node.

## Step-by-step: DOWNLOAD
5. Download a whole node/component as a zip via **⋯ / "Download as zip"**, or grab
   individual files. CLI alternative: `osf -p <node_id> clone`.
6. Extract into `_scratch/<paper_id>/`, list the tree; check each component so you don't
   miss code or data hosted in a sibling component.

## READ THE README FIRST — for access instructions and gates
After extracting, open the **README** (`.txt` / `.md`) and read it. The README often
explains *what is in the package and what is not* — in particular, **the data may not be in
the zip**, and it tells you where the data live and how to obtain them. Right now we use this
only to (a) confirm we actually downloaded the package and (b) catch any access gate below —
**we do not sort the contents into `/code` and `/data` at this stage.**

### Contract / DUA-gated data → FLAG, do not attempt (the agent must never sign)
If the README (or the data provider's page) says the data require a **signed contract, a
data-use agreement, registration, or an application** to download, the agent **must not**
sign, accept, or apply — that is a human decision with legal weight. Instead:
- flag `needs_review: on_request_gated_data`,
- record the exact **`apply_at` URL** — the precise page where the human requests access
  (e.g. "SOEP v36 — signed user contract at `https://www.diw.de/.../data_access.html`"), and
- inform the user *where to apply* so they can decide.

<!-- DEFERRED — future feature: sort the extracted files into /code and /data by role.
     Not used at this stage (we only find + download the package). Kept for later:

## Sorting the unzipped files by ROLE (not everything is code or data)
Having read the README, label each item by its role. Do NOT force documentation or
supplements into code/ or data/:
- README / Readme.txt / README.md → the overall guide for how to run the replication and
  where to obtain code & data. Read it FIRST; keep it at the package root; it is NOT data.
- *_supp.pdf / supplemental PDF (e.g. SocSci_v10_830to856_supp.pdf) → the article's
  supplemental material. In practice it holds no runnable code and no usable dataset, so it
  belongs to neither code/ nor data/. It may contain a link to where the package/data can be
  accessed — note that link for later; do not file the PDF as data.
- scripts (.do / .R / .py / .ipynb / …) → code/.
- datasets (.dta / .csv / .rda / …) → data/ (or, per the README, note them as external/gated).
(Classification of the final code/data verdict is deferred — see agent.toml [verdict].)
-->


## Gotchas
- A **private** node returns a login/404 → `needs_review: auth_walled_contents`.
- An add-on storage root (e.g. a linked Google Drive) may be **auth-walled** even when the
  OSF node is public — record it as unverified.
- A **preprint-only** node is a manuscript, not a package → don't record as code/data; look
  for the linked project.

## Worked example (from corpus) — "There's More" (there-s-more, v10-29-830)
1. Journal **SUPPLEMENTAL MATERIAL** tab → `osf.io/rhd8y`.
2. Node was a Project; **Files → "Download as zip"** pulled the whole deposit.
3. **Read `Readme.txt` first.** It states the data are **not** in the package: *"To
   replicate the SOEP analyses, you need to get SOEP data version 36. Further, you need to
   prepare the SOEP data using the CPF-files: https://www.cpfdata.com/"* — so the data are
   external, obtained per the README.
4. **Contract gate flagged.** The README points to SOEP v36 at
   `diw.de/.../data_access.html`, which requires **signing a user contract** to download.
   The agent does **not** sign → flagged `needs_review: on_request_gated_data` with
   **`apply_at`** = `https://www.diw.de/.../data_access.html` (SOEP v36 — signed user
   contract) and informed the user **where to apply**.
5. **Recorded package location** for the xlsx: **`SUPPLEMENTAL MATERIAL → OSF`**
   (`https://osf.io/rhd8y/`). The package *was* found and downloaded — only the SOEP data is
   contract-gated.
<!-- DEFERRED — future feature: sorting the extracted files into /code and /data.
     code = 01_main.do … 04_test_assumptions.do + figures/ + modified_data/ + montecarlo.dta;
     Readme.txt = instructions; SocSci_v10_830to856_supp.pdf = supplement (neither). -->

## After download → `calibration-honesty`
Confirm the node's contributors include an author of this paper and the README/wiki cites
it (provenance), and read the README to catch any contract/DUA gate. (Sorting contents into
`/code` & `/data` and assigning a code/data verdict is DEFERRED — see `agent.toml [verdict]`.)
