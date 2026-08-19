---
name: github-repository-and-pages
description: The replication package is on GitHub — usually reached from the journal SUPPLEMENTAL MATERIAL tab's "Reproducibility Package" line, or from a github.io page / the PDF / an author homepage. Workflow to get the repo, read the README for data-access gates, clone it, flag any approved-access/contract requirement to the user, and record the location as SUPPLEMENTAL MATERIAL → GitHub repo (link).
---

# Source: GitHub (repo link / profile / github.io)

## When you get routed here
- **Most often:** the journal **SUPPLEMENTAL MATERIAL** tab's "Reproducibility Package" line
  links a `github.com/...` repo (delegated here from `journal-reproducibility-package`).
- Also: a `github.com` / `github.io` link in the article PDF or on an author homepage, or the
  SOP §2.5 "search repositories properly" step when you must discover the repo yourself.

## Workflow (the steps the agent follows)
1. **Get the repo URL** — directly from the journal SUPPLEMENTAL MATERIAL "Reproducibility
   Package" line / PDF / homepage, or discover it (see LOCATE below).
2. **Open the repo and read `README.md`** — for how the replication is organized and,
   crucially, the **data-access instructions**.
3. **Check for a data-access gate.** If the README says the data require **approved access,
   an application, a signed agreement, or registration** (e.g. Statistics Denmark, SOEP), the
   agent **must NOT** apply, sign, or register → flag `needs_review: on_request_gated_data`,
   record the exact **`apply_at` URL** (the page where the human applies — e.g. Statistics
   Denmark's research-access application), and **notify the user where to apply**.
4. **Clone the repository** to download the package:
   `git clone https://github.com/<user>/<repo>.git` into `_scratch/<paper_id>/`.
5. **Record the location** for the xlsx as the discovery path, e.g.
   **`SUPPLEMENTAL MATERIAL → GitHub repo`** (`https://github.com/<user>/<repo>`).
6. Hand off to `calibration-honesty` for provenance (owner is an author / README cites the
   paper). *(Sorting contents into `/code` & `/data` is DEFERRED — we only find + download.)*

## Step-by-step: LOCATE (only when you must discover the repo)
1. If it is `username.github.io` → strip to `github.com/username` (the pages site's source
   repo, or the profile that hosts the real repo).
2. Open the author's **profile**: `github.com/<username>?tab=repositories`. Scan *pinned +
   all* repos — do NOT rely on GitHub search to surface a named repo.
3. Match a repo to the paper: try the title as a CamelCase/hyphen slug
   (title "Teacher Sorting and Inequalities in Student Achievement" → repo
   `Teacher-Sorting-Achievement`), then paper keywords; open the README and confirm it names
   the paper title or DOI.
4. Check every co-author's account and any lab/org account too (code routes to the
   technical/methods author, SOP §2.2).

## Step-by-step: DOWNLOAD
- **Clone** (preferred — preserves structure):
  `git clone https://github.com/<user>/<repo>.git` into `_scratch/<paper_id>/`.
  Alternative: **Code ▸ Download ZIP**; for a tagged release use the **Releases** page.
- If data are stored via **Git LFS** and blocked (403), note it — LFS pointer files are NOT
  the data. Follow any README link to an external data host → hand off to `data-repository`.
- *(We do NOT sort the cloned contents into `/code` and `/data` at this stage — deferred.)*

## Gotchas
- A repo owned by a **third party** (not an author) may be a reconstruction, not the
  authors' deposit → flag, do not record as the authors' package.
- Private repo (404 / login) → `needs_review: auth_walled_contents`.
- A `username.github.io` that only renders a CV/blog is a pointer, not the package — go to
  the profile and find the actual repo.
- **Data behind approved access** (Statistics Denmark, SOEP, register data) is a gate, not a
  missing package → flag + notify the user; the code repo is still a real, located find.

## Worked example (from corpus) — Teacher Sorting (teacher-sorting-achievement, v13-29-747)
1. Article page `sociologicalscience.com/articles-v13-29-747/` → **SUPPLEMENTAL MATERIAL**
   tab → "Reproducibility Package" → link
   `https://github.com/s-aj-hassan/Teacher-Sorting-Achievement`
   (owner `s-aj-hassan` = author **Said Hassan** → provenance).
2. Opened the repo and read **`README.md`**: it documents the Stata replication code and
   states the **data require approved access through Statistics Denmark**.
3. **Access gate flagged.** Statistics Denmark requires approved access (an application) —
   the agent does **not** apply → flagged `needs_review: on_request_gated_data` with
   **`apply_at`** = Statistics Denmark's research-data access application page (the exact URL
   the README/provider gives), and **notified the user where to apply**.
4. **Cloned** the repo:
   `git clone https://github.com/s-aj-hassan/Teacher-Sorting-Achievement.git` into
   `_scratch/teacher-sorting-achievement/`.
5. **Recorded location** for the xlsx: **`SUPPLEMENTAL MATERIAL → GitHub repo`**
   (`https://github.com/s-aj-hassan/Teacher-Sorting-Achievement`). The package *was* found and
   downloaded — only the Statistics Denmark data is gated.
<!-- DEFERRED — future feature: sorting the cloned repo into /code and /data
     (43 .do files: master.do + covariate/analysis pipeline; README.md; LICENSE; output/). -->

> Second real case: `beyond-text-visual-conjoints` →
> `github.com/kmunger/Housekeeping_SocSci_Replication` (clone the same way).

## After download → `calibration-honesty`
Confirm provenance (owner is an author AND README cites this paper) and note any data-access
gate from the README. (Sorting into `/code` & `/data` and the code/data verdict are DEFERRED
— see `agent.toml [verdict]`.)
