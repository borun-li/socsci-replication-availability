---
name: project-or-lab-site
description: The data (and sometimes code) live on a named research project's or lab's own website — its download/data page — rather than with an individual author. Step-by-step to identify the lab, reach its data page, and download the package.
---

# Source: project / lab website

## When you get routed here
SOP §4: data collected by a **named lab or project** are often hosted on that
organization's own site, not an author's page or a generic repository. (a27's package was
on the Eviction Lab's own download page.) Reach here when the paper names a data-collection
project, center, or lab — **most often you arrive from a code repo**: the SUPPLEMENTAL
MATERIAL tab links a GitHub/OSF package for the *code*, and that package's **README gives the
link + instructions for downloading the *data* from the project's own portal** (see the PSID
worked example). Follow that README link here.

## Step-by-step: LOCATE
1. From the paper/abstract, identify the **named project or lab** that produced the data
   (e.g. "Eviction Lab", a survey/panel's home institution, a data-collection center).
2. Find the project's official site: search `<project name> data` / `<project name> download`.
   Prefer the project's own domain over mirrors.
3. On the site, open **Data**, **Downloads**, **Methods**, or **Resources**; the dataset for
   this paper is usually a named release with its own page.
4. Check whether the paper's **code** is also there (some labs post replication code beside
   the data) or only the data (then code routes back to `github-repository-and-pages` /
   `author-homepage`).

## Step-by-step: DOWNLOAD
5. If the download is **open**, pull the released files/zip into `_scratch/<paper_id>/`,
   extract, list the tree.
6. If it requires **registration, a data-use agreement, or a non-robot (CAPTCHA) check**
   (common for panel portals like PSID's Simba, which returns 403 to bots), the agent **must
   not** register, sign, or solve the CAPTCHA → flag `needs_review: on_request_gated_data`,
   record the exact **`apply_at` URL** (the portal's sign-up/download page), and tell the user
   where to apply — still a real, located package.

## Gotchas
- The project's *current* release may differ from the **version/vintage** used in the paper —
  note the exact wave/year; a newer release is not identical provenance.
- Many project portals are **registration- or non-robot-gated** (login / agreement / CAPTCHA,
  → HTTP 403 to an automated fetch) → record the landing link + `apply_at` and flag
  `on_request_gated_data`; do not assert the contents you couldn't download.
- The project hosts the **data**; don't assume the **code** is there too — code often lives on
  GitHub/OSF/the author's page (verify separately, as in the PSID example below).

## Worked example (from corpus) — pathways-independence-dynamics (v12-33-833)
Article: *"Pathways to Independence: The Dynamics of Parental Support in the Transition to
Adulthood"* — Ramina Sotoudeh & Ginevra Floridi. Verified live 2026-07-04. **Workflow:
SUPPLEMENTAL MATERIAL tab → GitHub repo package → (README's data link) → project site.**
1. **Tab → GitHub repo package.** The article page
   `sociologicalscience.com/articles-v12-33-833/` SUPPLEMENTAL MATERIAL tab: *"Replication
   code for this article can be accessed here:
   `https://github.com/raminasotoudeh/pathways_to_independence/tree/main`"* → route to
   `github-repository-and-pages`, clone it (4 `.R` scripts; the README names the paper →
   provenance ✓). **That repo holds the code AND the instructions + link for getting the
   data.**
2. **README → the project's own data portal.** The repo README states: *"Link to download
   the data: `https://simba.isr.umich.edu/Zips/ZipMain.aspx`"* — the **PSID (Panel Study of
   Income Dynamics)** Data Center ("Simba"), the named panel's **own** download portal (not
   GitHub/OSF/Dataverse). Follow that link **here** (project-or-lab-site).
3. **Gate: registration + non-robot check → NOTE IT FOR THE USER with the link.** The PSID
   portal is **not open** — it returns HTTP 403 to a bot and requires a **free account + a
   non-robot (CAPTCHA) test** to download. The agent **must not** register or solve the
   CAPTCHA → flag `needs_review: on_request_gated_data`, **tell the user the data is behind a
   non-robot/registration check**, and give them the exact access link: record **`apply_at`**
   = `https://simba.isr.umich.edu/Zips/ZipMain.aspx` (PSID registration/download).
4. **Version provenance.** The paper uses the **PSID Transition to Adulthood (TAS) 2005–2021**
   waves — note the exact vintage; a newer PSID release is not identical provenance.
5. **Record location** for the xlsx — split by role: code = `SUPPLEMENTAL MATERIAL → GitHub`
   (`github.com/raminasotoudeh/pathways_to_independence`); data = `README → PSID project site`
   (`simba.isr.umich.edu`, registration-gated). Code is in hand; data is a located-but-gated find.

> Archetype from the SOP (a27): the **Eviction Lab** posts a paper's dataset on its **own**
> download page — same shape (named project hosts the data on its own site), open rather than
> registration-gated.

## After download → `calibration-honesty`
Confirm the release is the **version** the paper used (provenance ≠ just "same project"), open
the tree, and record any registration/non-robot gate with its `apply_at` URL. (Sorting into
`/code` & `/data` is DEFERRED — see `agent.toml [verdict]`.)
