# Replication-Package Availability Codebook (Sociological Science)
Version 3.2 · 2026-08-18

*Changelog — v3.2:* clarified `data_gated` — `Y` whenever the underlying analysis data is **not
freely/publicly available** (restricted / confidential / proprietary / institutional-access /
register / IRB / author-collected human-subjects), **even if there is no external application
route**; when no route exists, `data_source_apply_at` **explains why** (e.g. discretionary/
institutional access only). `N` only when the data is **genuinely public** (open archives /
open deposits) or the authors' own **simulation** outputs. The earlier "mere non-provision"
exclusion applies **only** when the underlying source is itself public (a public dataset the
authors simply did not re-post) — not to inherently restricted data.

*Changelog — v3.1:* introduced the special-application framing for `data_gated`
(application/DUA/RDC, paid license, available-on-request email, registration portal).
Superseded by v3.2 for the no-route restricted case.

This document defines how each *Sociological Science* article is coded for **data and code
availability**, and the column structure of the result workbook. It is the authoritative
reference for `Borun_batch_3_result.xlsx`.

Column names below are the **canonical** (snake_case) names used in the pipeline, the CSV
export, and the archive. An Excel presentation copy may use display headers, but the canonical
names govern.

---

## 1. Schema

The schema has two blocks. **Block A** (bibliographic identifiers) is journal-specific.
**Block B** (availability coding) is IDENTICAL across all journals — column names, order,
allowed values, and definitions. Cross-journal comparison of take-up rates depends on
Block B never diverging.

### Block A — bibliographic (journal-specific)

| # | Column | SocSci | ASR | Notes |
|---|--------|--------|-----|-------|
| 1 | `doi` | ✔ | ✔ | **primary key, both journals** |
| 2 | `paper_id` | ✔ | — | SocSci internal ID (e.g. SS287) |
| 3 | `title` | ✔ | ✔ | |
| 4 | `authors` | ✔ | ✔ | |
| 5 | `published_date` | ✔ | ✔ | ASR: `published-online` from Crossref |
| 6 | `submission_date` | ✔ | — | grandfathering only; ASR has no policy date |
| 7 | `article_url` | ✔ | ✔ | ASR: `resource.primary.URL` |
| 8 | `volume` | — | ✔ | |
| 9 | `issue` | — | ✔ | |
| 10 | `accessibility` | — | ✔ | Open / Free / Restricted Access |

A column absent for a journal is omitted from that journal's workbook, never filled with a
placeholder. In the merged archive, absent columns are blank.

### Block B — availability coding (identical across journals)

| # | Column | Filled by | Notes |
|---|--------|-----------|-------|
| 1 | `in_scope` | coder | `Y` / `NA` / `?` |
| 2 | `qualitative` | coder | blank if `in_scope = NA` |
| 3 | `data` | coder | blank if `in_scope = NA` |
| 4 | `code` | coder | blank if `in_scope = NA` |
| 5 | `data_and_code` | **pipeline (auto)** | do not type; not an agent judgment |
| 6 | `neither` | **pipeline (auto)** | do not type; not an agent judgment |
| 7 | `data_gated` | coder | blank if `in_scope = NA` |
| 8 | `data_source_apply_at` | coder | **required when `data_gated = Y`** |
| 9 | `package_location` | coder | URL/file where materials actually live |
| 10 | `path_to_package` | coder | how you got there (discovery path) |
| 11 | `coverage_checked` | coder | where you looked |
| 12 | `notes` | coder | **required on every row** |

§2–§5 define Block B and apply unchanged to every journal. Journal-specific extraction
(where the DAS lives, how the PDF is laid out) belongs in that journal's pipeline
instructions, never in this codebook.

---

## 2. Codebook — field definitions

- **`submission_date`** — If the paper prints a "received"/"submitted" date (footnote or
  masthead), record it. This decides **grandfathering**: submitted **on or after 2023-04-01**
  (boundary inclusive) = policy-required deposit. No separate column records this; the date
  itself draws the line.

- **`in_scope`**
  - `Y` = reports original empirical analysis the authors ran. A qualitative **empirical**
    paper *is* in scope (`Y`, with `qualitative = Y`).
  - `NA` = nothing to reproduce — commentary, rejoinder, editorial, or purely theoretical.
  - `?` = does not fit. **Flag the entire row for human review** and say why in `notes`.
    Denominator inclusion is decided after review, by the resolved `in_scope` value.
  - If `in_scope = NA`, leave `qualitative` / `data` / `code` / `data_gated` **blank**.

- **`qualitative`** — `Y` if primary evidence is non-numeric (interviews, ethnography,
  archival/textual), interpreted directly rather than converted into variables. Papers using
  **both** qual and quant = quantitative (`N`).

- **`data`** — `Y` = the authors **deposited their analysis dataset in the package**. A pointer
  to an external source is never a deposit — this includes public archives (ICPSR, IPUMS, GSS,
  NLSY, NBER). If the dataset is not in the package, `data = N`.

- **`code`** — `Y` = the authors **deposited code that reproduces THIS paper's results**. A
  general method/software package (even one the authors wrote) is a **tool**, not a package,
  unless it bundles the paper's own analysis scripts. See SS091, SS131.

- **`data_and_code` / `neither`** — Generated by pipeline code, never by an agent. Rules:
  - `data_and_code` = `Y` if `data = Y` **and** `code = Y`, else `N`
  - `neither` = `Y` if `data = N` **and** `code = N`, else `N`
  - Both blank whenever `data` / `code` are blank.

- **`data_gated`** — `Y` whenever the underlying analysis data is **not freely/publicly
  available** — restricted, confidential, proprietary, institutional-access-only, a
  register/administrative source, IRB-protected, or author-collected human-subjects data —
  **regardless of whether an external application route exists**. When there **is** a route,
  record it in `data_source_apply_at`; when there is **no** external route, still code `Y` and
  use `data_source_apply_at` to **explain why** (e.g. discretionary or institutional access
  granted only to the authors). `N` only when the data is **genuinely public** (freely
  downloadable open archives / open deposits) or the authors' own **simulation** outputs.
  *Mere non-provision* → `N` applies **only** when the underlying source is itself public (a
  public dataset the authors simply did not re-post), never to inherently restricted data.
  Blank if `in_scope = NA`.

- **`data_source_apply_at`** — Where the gated data lives and how to apply for it.

- **`package_location`** — URL or file where the materials actually live.

- **`path_to_package`** — How you got there: e.g. `supplement note -> author homepage -> osf.io/xxxx`.

- **`coverage_checked`** — Where you looked: e.g. `tab + PDF + author search + Wayback`.

- **`notes`** — **REQUIRED ON EVERY ROW.** What you opened and what was inside it.

### "Available upon request" vs. mere non-provision

The distinction turns on whether a **real access route** exists:

- The article states the data is **available on request** (an actual request mechanism — email
  the author/provider, or apply through a named body): `data = N`, `data_gated = Y`,
  `data_source_apply_at` = a **concrete** route (a URL or an email address; `contact author`
  alone is not acceptable).
- The authors **did not deposit** the data and state **no** access route:
  - if the underlying data is **inherently restricted** (confidential interviews, proprietary,
    institutional, register): `data = N`, `data_gated = Y`, and `data_source_apply_at`
    explains why no external route exists;
  - if the underlying source is **itself public** (they used public data and simply did not
    re-post their extract): `data = N`, `data_gated = N` — this is the only *mere
    non-provision* case. (Publicly posted replication *code* does not change the data status.)

---

## 3. The one rule

> A **Y** means the authors' materials reproduce **THIS** paper. Not a relevant link, not a
> tool they used, not a preprint, not a public data source. When your note describes why
> something is **NOT** the package, code it **N**. **Do not code past your own note.**

---

## 4. Batch-3 changes (vs Batch 2)

1. **New `submission_date` column** — extracted from the article's **PROCESS INFO** tab
   (Received date); if there is no such tab, from the Received/Submitted line on the PDF's
   first page. This is the responsibility of Agent 2 (Scope) in the pipeline.

---

## 5. Execution-layer definitions for the gated-data fields

Operationalization used by the coding pipeline — set by the **Execute** agent, independently
checked by the **Exec-Verify** agent.

- **`data_gated = Y`** when obtaining the underlying analysis data requires a **special
  application / access route** — a concrete, identifiable mechanism requiring a request or
  permission:
  - a formal application / registration / Data Use Agreement / research data center
    (e.g. GSOEP→DIW, NSFG→NCHS RDC, Add Health DUA, a national register via SCB/MONA, IRS/SSA
    restricted files);
  - a paid **license / purchase** from a commercial vendor (e.g. RealtyTrac/ATTOM,
    ThomsonONE/Refinitiv, College Board ASC);
  - an explicit **available-on-request** route (email the author / PI / provider);
  - a **portal / website** you must apply to or register with to download.

  This holds **even if** the code (and sometimes derived data) is deposited, and applies when
  `data = N` because the source itself is access-restricted.

  It also holds when the data is restricted but has **no external route** (discretionary or
  institutional access granted only to the authors, ad-hoc data sharing, or unnamed
  proprietary sources) — still `Y`, with `data_source_apply_at` explaining why no route exists.

  **`N`** only when the data is genuinely public / freely downloadable (public
  IPUMS/GSS/ANES/ACS-PUMS/NLSY, open archives, **open Harvard Dataverse/OSF deposits**, open
  web data), or when the analysis data are the authors' own simulation outputs. *Mere
  non-provision* → `N` applies only when the underlying source is itself public (a public
  dataset not re-posted), not to inherently restricted data.

- **`data_source_apply_at`** — when `data_gated = Y`, name the restricted **source** AND the
  concrete **apply-at** (provider + URL/agreement/email). Examples:
  - `SOEP Core — data-access agreement, DIW Berlin (diw.de)`
  - `Swedish registers — Statistics Sweden / SCB MONA microdata service (scb.se)`
  - `Add Health — restricted-use DUA, Carolina Population Center, UNC-Chapel Hill (addhealth.cpc.unc.edu)`
  - `confidential interviews — corresponding author, <email address from the article>`
  - Blank when `data_gated = N`.

- **Gated but declared packages** — the located package still counts; record the apply-at and
  **never** sign, register, log in, or solve a CAPTCHA to obtain the data.