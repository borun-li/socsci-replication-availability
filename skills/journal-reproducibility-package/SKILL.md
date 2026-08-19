---
name: journal-reproducibility-package
description: The replication package link is on the Sociological Science article page under the SUPPLEMENTAL MATERIAL tab, in a "Reproducibility Package:" line that usually points to OSF. Step-by-step to open that tab, extract the link, and download. Start here for any post-policy article.
---

# Source: Sociological Science article page → SUPPLEMENTAL MATERIAL tab

## When you get routed here
This is the **first place to look**. For articles under the journal's Reproducibility
Policy (submissions after 2023-04-01 — check the *Received* date, not the publication date),
the article page carries a **SUPPLEMENTAL MATERIAL** tab with a "Reproducibility Package:"
line linking the deposit (most often OSF).

## Step-by-step: LOCATE
1. Open the article page (`article_url`, e.g. `sociologicalscience.com/articles-v13-9-214/`).
2. Click the **SUPPLEMENTAL MATERIAL** tab (alongside Abstract / PDF).
3. Read the **"Reproducibility Package:"** line. It reads like:
   *"Replication code for this article can be accessed here: https://osf.io/j8ymw/overview."*
   Copy the exact URL and the surrounding sentence (that sentence is the provenance and may
   state what is included — code only, data on request, etc.).
4. If the line says the package is exempt (qualitative-only) or "available on request,"
   record that reason — a policy exemption is not "no package."

## Step-by-step: DOWNLOAD
5. **Read the host of the link and route accordingly** — the "Reproducibility Package:" line
   can point anywhere:
   - `osf.io/...`            → hand off to `osf-repository`
   - `github.com/...`        → hand off to `github-repository-and-pages`
   - Dataverse / Zenodo / figshare / ICPSR → hand off to `data-repository`
   Do not assume OSF just because it is the most common; check the URL and delegate.
6. If it is a directly hosted `.zip`, download into `_scratch/<paper_id>/`, extract, list
   the tree.

## CRITICAL — the `_supp.pdf` is NOT always "just an appendix": READ it for printed code
A tab that shows only a `SocSci_..._supp.pdf` does **NOT** mean "no package." The supplement
PDF frequently **prints the replication code inline** — look for a section titled
**"Appendix: Computer Code"**, *"The following R code yields the … estimates reported in the
paper"*, *"R code to generate all results and figures"*, or a printed Stata do-file. **Always
open the supplement PDF and scan its text for such a code section before concluding a package
is unavailable.** If code is printed there, that IS the authors' code → route to
`calibration-honesty` and record it as a found package (a simulation/estimator script counts,
like any deposit). Do not stop at "the tab only links a `_supp.pdf`."
- Quick check: extract the PDF text and grep for `computer code`, `following .*code`,
  `replication code`, `do-file`, `library(`, `program define`, `clear all`, `proc `.

## Gotchas
- **No SUPPLEMENTAL MATERIAL tab / no line** → the article is likely pre-policy; fall
  through to `article-pdf-availability-statement` and `author-homepage`. **But still open any
  `_supp.pdf` and scan for printed code first (see CRITICAL above).**
- The line usually names **code**; the **data** may be gated or elsewhere — follow the host
  skill and don't assume data are included just because code is.
- The URL is a landing page — always follow through to the deposit and open the tree; never
  record the sentence's wording as the contents.

## Worked example (from corpus) — Early Childhood Investments (v13-9-214)
1. Opened `sociologicalscience.com/articles-v13-9-214/`
   (Maralani, Portier & Özcan — "Early Childhood Investments and Women's Work Outcomes").
2. **SUPPLEMENTAL MATERIAL** tab → line:
   *"Reproducibility Package: Replication code for this article can be accessed here:
   https://osf.io/j8ymw/overview."*
3. Followed `osf.io/j8ymw` → handed off to `osf-repository` → downloaded the package.

## Worked example (from corpus) — CODE PRINTED IN THE SUPPLEMENT (do not miss these)
- **SS084 "Multicollinearity and Model Misspecification" (v3-27-627):** the tab shows only a
  `_supp.pdf`, but its **Appendix B ("Computer Code")** prints the R estimator function
  `bayes(x, y, u)` — *"The following R code yields the Bayes estimates reported in the paper."*
  → the authors' code IS provided (found), even though nothing is on OSF/GitHub.
- **SS074 "Trust and Public Support for Environmental Protection" (v3-17-359):** the 45-page
  `_supp.pdf` item (10) is the **full R replication script** ("R code to generate all results
  and figures … `library(mice)`/`MCMCglmm`; reads public ISSP/Pew/OECD data").
- **Lesson:** both were initially mis-scored "no package" because only the tab link (a
  `_supp.pdf`) was noted and the PDF's contents were **not read**. Reading the supplement PDF
  is mandatory, not optional.

## After download → `calibration-honesty`
The journal-page line is strong path-provenance (the journal's own record for this article).
Confirm the deposit's contents match, open the tree, then let `agent.toml [verdict]` assign
the status.
