---
name: data-repository
description: The package or its data live in a data repository — Harvard Dataverse, ICPSR, Zenodo, figshare — or behind a survey/register data provider (SOEP, UK Data Service, ISTAT, ANES). Step-by-step download mechanics per host, plus how to record gated-access data.
---

# Source: data repositories & data providers

## When you get routed here
A link or named host from the PDF, journal paragraph, README, or author page points to a
formal deposit or a survey/register provider. Covers both **openly downloadable** deposits
and **gated** data that require registration or an agreement.

## Step-by-step: LOCATE
1. Identify the host and its ID:
   - **Harvard Dataverse** — `doi:10.7910/DVN/...` → the dataset landing page.
   - **ICPSR** — study number (`ICPSR #####`); may need the study-level page.
   - **Zenodo** — `doi:10.5281/zenodo.######` (has versions).
   - **figshare** — article/collection ID.
2. If only a host *name* is given (no link), search the host directly for the paper
   title/author — deposits are indexed there even when keyword web search misses them.

## Step-by-step: DOWNLOAD
3. **Dataverse** — "Access Dataset ▸ Download ZIP"; for `.dta`/`.sav` prefer **original
   format** (Dataverse auto-converts to `.tab` otherwise). Accept the terms if prompted.
4. **Zenodo / figshare** — download the version's zip; note the exact version/DOI.
5. **ICPSR** — most datasets need a **free login + agreement**; some are restricted-use
   (secure enclave). Download the delimited/Stata bundle if open.
6. Extract into `_scratch/<paper_id>/`, list the tree.

## Gated data / code — record WHERE TO APPLY, don't discard (SOP §4)
If the data **or** the code require **sign-up / log-in, registration, a data-use agreement,
an application, or an on-site/guest terminal**, the package is still a real, located find.
The agent **must not** register, sign, log in, or apply — but it **MUST explicitly record
the exact place to apply** so the user can act:
- **`apply_at`** = the precise URL/page where the human requests access — **not** just the
  provider name. List one per gated item (data and code can have *different* gates).
- flag `needs_review: on_request_gated_data`, and notify the user **with those URLs**.

Known gates in this corpus (and where to apply):
- **Harvard Dataverse restricted files** — Log In → "Request Access" on the dataset page
  (`outlier-not-birth`: the 3 `.do` files → apply at `https://doi.org/10.7910/DVN/RZVEMI`).
- **CFPS (China)** — microdata application at `https://cfpsdata.pku.edu.cn/` (sign up / log in).
- **SOEP / NEPS** — signed data-access agreement / guest terminal, apply at diw.de.
- **ISTAT** — formal request at `https://www.istat.it/en/data/microdata`.
- **UK Data Service / ANES** — free registration, then download.
- **Statistics Denmark / PSID / CNEF / register data (DK/SE)** — approved-access application.

## Gotchas
- A Dataverse "restricted file" shows a lock → it needs **Request Access** (Log In); treat
  as gated and record the **apply_at** URL. Even the *code* can be restricted, not just data.
- Size alone can't tell real vs synthetic data (`calibration-honesty`).

## Worked example (from corpus) — Outlier or Not? (outlier-not-birth, v12-19-431)
1. Routed from journal SUPPLEMENTAL MATERIAL: code at `https://doi.org/10.7910/DVN/RZVEMI`
   (Harvard Dataverse); data via CFPS application.
2. **LOCATE** — resolved the DOI (via the Dataverse API, since the page is JS-rendered): real
   published deposit *"Replication Data for: Outlier or Not?…"* (RELEASED, CC0). Files:
   `readme.txt` (open) + `clean and reshape.do`, `Birth interval analsis.do`, `analysis.do`.
3. **Both code and data are gated → record where to apply:**
   - the 3 `.do` files are **restricted** on Dataverse → **`apply_at`**: Log In + "Request
     Access" on `https://doi.org/10.7910/DVN/RZVEMI`.
   - the CFPS microdata require an application → **`apply_at`**: `https://cfpsdata.pku.edu.cn/`.
   Agent does **not** log in / apply → flagged `needs_review: on_request_gated_data` and told
   the user **exactly where to apply** (both URLs).
4. Downloaded the open `readme.txt`; recorded location
   **`SUPPLEMENTAL MATERIAL → Harvard Dataverse (https://doi.org/10.7910/DVN/RZVEMI)`**.
   Package located; full download blocked only by the two access gates.

> Contrast (open deposit): `echo-chambers-defined` → figshare `SocScienceCode.zip` +
> `tweet_mentions.csv`, no gate — download the zip + csv directly.

## After download → `calibration-honesty`
Confirm the deposit ties to this paper, and for any gate record the exact **`apply_at`**
URL(s) + notify the user. (Sorting into `/code` & `/data` and the code/data verdict are
DEFERRED — see `agent.toml [verdict]`.)
