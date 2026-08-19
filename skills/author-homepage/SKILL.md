---
name: author-homepage
description: The replication package lives on an author's personal, departmental, or Google Sites homepage — a "Research / Code / Data / Software" page or a per-paper page. Step-by-step to find the right author, reach their site, and get to the package. This is where keyword search fails and many packages actually are.
---

# Source: author personal / departmental / Google Sites homepage

## When you get routed here
SOP §3: a large share of packages sit on a personal site and never surface in a keyword
search (a1, a21, a25 were all found this way). Reach here three ways:
- the journal **SUPPLEMENTAL MATERIAL** tab links *out* to the author's homepage (e.g. a
  "NLSY data and Stata code" link pointing at a `homepage.university.edu/<name>/…` page),
- the PDF says "available from the authors", or
- a `google-scholar-profile` hop / routine per-author check.

## Step-by-step: LOCATE
1. **Pick which author to check first, by role** (SOP §2.2): code → technical/methods/junior
   author; data access → survey/administrative-data author. But check *every* author — the
   role hint is a hypothesis, not a certainty.
2. Find each author's page: search `"<full name>" <university>`, plus `<name> replication` /
   `<name> code data`. Prefer the `.edu`/departmental page and any personal domain or
   Google Site.
3. On the site, open the sections most likely to hold packages: **Research**,
   **Publications**, **Code**, **Data**, **Software**, **Replication**, or a **per-paper**
   page. The link is often next to the paper's citation. **A homepage usually lists many
   links — choose the MOST ACCURATE one by reading each link's description**, i.e. the item
   that actually names the replication data + code (e.g. a "… Dataset … & Code" line), not an
   appendix PDF, a response letter, or an unrelated project.
4. Follow any outbound link to a repo/deposit (`github.com`, `osf.io`, Dataverse, Zenodo,
   figshare) → hand off to that host skill.

## Step-by-step: DOWNLOAD
5. If the package is a `.zip`/`.tar.gz` hosted on the site, download into
   `_scratch/<paper_id>/`, extract, list the tree.
6. If it's an outbound repo link, use the matching host skill's download steps.

## Gotchas
- **A "page isn't working" link is often just the wrong scheme — retry `https://`.** Old
  journal tabs link author pages over **`http://`**, and many university servers now refuse
  plain HTTP (connection fails / browser error) while serving the *identical* page over
  **`https://`**. Also try dropping/keeping a host prefix (`www88.homepage.…` ↔
  `homepage.…`). Verified on this corpus case (see worked example). Only after http→https +
  host variants + Wayback all fail is the page truly dead.
- Departmental pages go stale — try the **Wayback Machine** for a dead personal URL before
  concluding nothing is posted.
- A Google Drive folder or auth-walled portal → record the landing link and flag
  `needs_review: auth_walled_contents`; contents are unverified.
- Distinguish a per-paper page for *this* paper from the author's other work (provenance).

## Worked example (from corpus) — incarceration-racial-privilege (v3-10-190)
Article: *"Can Incarceration Really Strip People of Racial Privilege?"* — Lance Hannon &
Robert DeFina (2016, Vol. 3). The package is **hosted on the author's Villanova homepage**,
reached *from the tab*:
1. **Tab first.** The article page `sociologicalscience.com/v3-10-190/` SUPPLEMENTAL MATERIAL
   tab links a `*_supp.pdf` **and** an external line: *"NLSY data and Stata code"* →
   `http://www88.homepage.villanova.edu/lance.hannon/SupplementalMaterial.html`. A personal
   homepage, not GitHub/OSF/Dataverse → route **here**.
   **⚠ The tab's `http://` link is dead** — that host refuses plain HTTP, so a browser shows
   "this page isn't working." **Retry over `https://`** and it loads fine (verified
   2026-07-04): `https://www88.homepage.villanova.edu/lance.hannon/SupplementalMaterial.html`
   (the bare `https://homepage.villanova.edu/…` host also works). Do the http→https upgrade
   *before* concluding the package is gone.
2. **Open the homepage & confirm provenance.** Its heading reads *"Supplemental Material
   Appendix for our 2016 Sociological Science paper"* and the author (`lance.hannon`) is on
   this paper → path-provenance confirmed.
3. **Pick the RIGHT link by its description — the page has several.** This homepage lists many
   items (an AJS response letter `ResponseinAJS.pdf`, "Additional Person-level Figures and
   Tables", "Additional Fixed Effects Results", blog links, etc.). **Read each link's
   description and choose the one that IS the replication package**: here that is the item
   labelled **"NLSY79 Stata Dataset in Person-Years & Code"**, which bundles the two files that
   reproduce the analysis — `Hannon_DeFina.dta` (a 3.66 MB de-identified NLSY79 person-year
   extract) **and** `Hannon_DeFina_prg.do` (the Stata code, ~14 KB). Do **not** grab the
   appendix PDFs or the response letter as "the package" — match on the description.
4. **Download** the dataset + code from that item into
   `_scratch/incarceration-racial-privilege/` (they're plain relative hrefs — resolve against
   the **`https://`** page URL and fetch directly; no zip). Both return HTTP 200 (verified
   2026-07-04). (The `.txt`/`.csv` supplements are extra, not the core replication package.)
5. **Gated-data twist — but NOT an `apply_at` case here.** NLSY79 is normally BLS-gated, yet
   the authors posted a **usable de-identified extract directly on the page (no login/
   registration)** — so the data is *in hand*. Do **not** flag `on_request_gated_data`; the
   openly-posted extract is the deposit. (Contrast the gated cases in `data-repository` /
   `github-repository-and-pages`, where the data really is behind an application.)
6. **Record location** for the xlsx: **`SUPPLEMENTAL MATERIAL → author homepage`**
   (`www88.homepage.villanova.edu/lance.hannon/SupplementalMaterial.html`). Package found and
   downloaded — code **and** an open data extract.

## After download → `calibration-honesty`
Reaching the package *from this author's verified homepage* is path-provenance — confirm the
author is on this paper (rule 5), open the file tree, and catch any access gate. Here there
is none: the data extract is posted openly, so it is a real, in-hand find, not a gated flag.
(Sorting into `/code` & `/data` is DEFERRED — see `agent.toml [verdict]`.)
