# Sociological Science — Replication-Package Availability (2014–2026)

A complete, DOI-keyed dataset recording **whether every research article published in
*Sociological Science* deposited its data and/or code**, together with the multi-agent
pipeline, codebook, and provenance used to produce it.

**413 articles** (SS001–SS511), the journal's full run from its 2014 founding through
August 2026 (volumes 1–13).

---

## Description

Each in-scope empirical article is coded for whether the authors deposited an
analysis **dataset** and/or **code**, where the package lives (the exact repository link),
and — when the underlying data is access-restricted — how to apply for it. The headline
finding is the effect of the journal's mandatory-reproducibility policy (packages required for
manuscripts submitted on or after **2023-04-01**):

| Manuscripts submitted | n | Availability (data and/or code deposited) |
|-----------------------|---|--------------------------------------------|
| **Before** 2023-04-01 | 278 | **22.7%** |
| **On/after** 2023-04-01 | 119 | **95.0%** |

![Availability by year](data/availability_by_year.png)

Whole-corpus availability is 176 / 397 = 44.3% (held down by the pre-policy decade).

---

## Table of Contents

- [Description](#description)
- [Repository structure](#repository-structure)
- [The dataset](#the-dataset)
- [Prerequisites](#prerequisites)
- [Quick Start (install)](#quick-start-install)
- [Using it](#using-it)
- [Methodology & quality control](#methodology--quality-control)
- [Reproducibility](#reproducibility)
- [Citation](#citation)
- [License](#license)
- [Contributions](#contributions)
- [Contact](#contact)

---

## Repository structure

```
socsci-replication-availability/
├── README.md
├── LICENSE                      # MIT (code) + CC BY 4.0 (data)
├── agent.toml                   # the six-agent specification (references skills/)
├── skills/                      # the 6 search skills agent.toml loads
│   ├── journal-reproducibility-package/   # Locate: supplemental-material tab (checked first)
│   ├── article-pdf-availability-statement/ · author-homepage/
│   └── github-repository-and-pages/ · osf-repository/ · data-repository/  # Execute
├── data/
│   ├── socsci_availability.xlsx        # the full coded dataset (413 rows)
│   ├── socsci_availability.csv         # same, CSV
│   ├── socsci_availability_blank.csv   # blank worklist for re-coding (Scenario 2)
│   └── availability_by_year.png        # the chart above
├── docs/
│   ├── codebook.md              # coding manual — field definitions & rules
│   └── run_provenance.md        # pinned run parameters (model, prompts, workflow)
└── pipeline/
    ├── check_install.py           # confirm Python + dataset are ready
    ├── lookup.py                  # look up a package by DOI/URL/id  ← start here
    ├── reproduce_table.py         # recompute the headline numbers from the dataset
    ├── six-agent-availability.js  # main coding pipeline (Claude Code Workflow script)
    ├── gated_recheck.js           # data_gated determiner
    ├── gated_determination.js     # data_gated determiner (initial variant)
    ├── write_table.py            # write pipeline output into the table schema
    ├── write_inplace.py          # fill coding into an existing table
    └── merge_all.py              # merge per-batch tables into the full dataset
```

---

## The dataset

One row per article. Columns (full definitions in [`docs/codebook.md`](docs/codebook.md)):

**Block A — bibliographic:** `doi` (primary key), `paper_id`, `title`, `authors`,
`published_date`, `submission_date`, `article_url`.

**Block B — availability coding:**
`in_scope` (Y / NA / ?), `qualitative`, `data`, `code`, `data_and_code`, `neither`,
`data_gated`, `data_source_apply_at`, `package_location`, `path_to_package`,
`coverage_checked`, `notes`.

Key definitions:
- **`in_scope` = Y** — original empirical analysis by the authors (a qualitative empirical paper is Y).
- **`data` = Y** — the authors deposited their analysis dataset (a pointer to a public source is *not* a deposit).
- **`code` = Y** — the authors deposited code that reproduces this paper's results.
- **`data_gated` = Y** — the underlying data is not freely/publicly available (restricted / confidential / proprietary / register / IRB); `data_source_apply_at` records how to obtain it.
- **`package_location`** — the actual deposit repository link (OSF / Harvard Dataverse / GitHub / Zenodo / ICPSR …).

---

## Prerequisites

| To do this | You need |
|---|---|
| **Scenario 1** — look up packages (`lookup.py`) | **Python 3** — nothing else |
| Verify the published numbers (`reproduce_table.py`) | **Python 3** — nothing else |
| Regenerate the chart | Python 3 + `pip install matplotlib` |
| **Scenario 2** — independently re-code the articles | Python 3 **and** [Claude Code](https://claude.com/claude-code) with API access (an Anthropic API key or a Claude subscription) + an internet connection |

`git` is optional — you can download the repo as a ZIP instead. Everything except Scenario 2 is
standard-library Python: no `pip install`, no API key, no account.

---

## Quick Start (install)

The two everyday tools — **look up a package** and **reproduce the table** — are plain Python
scripts that read the shipped dataset. They need **only Python 3** (no `pip install`, no API key)
and run the same on **macOS, Linux, and Windows**. (Independently *re-coding* the articles is a
separate, heavier path that needs Claude Code — see Scenario 2.)

**Step 1 — make sure Python 3 is installed.** In a terminal:

```bash
python3 --version
```

You should see `Python 3.x.x`. If it says "command not found":
- **macOS** — `brew install python`  (or install from <https://www.python.org/downloads/>)
- **Ubuntu/Debian Linux** — `sudo apt update && sudo apt install -y python3`
- **Windows** — install from <https://www.python.org/downloads/> and tick **"Add python.exe to
  PATH"**; then use `python` instead of `python3` in the commands below (in PowerShell).

**Step 2 — download this repository.**

```bash
git clone https://github.com/borun-li/socsci-replication-availability.git
cd socsci-replication-availability
```

(No `git`? Use the green **Code → Download ZIP** button on GitHub, unzip it, and `cd` into the
folder.)

**Step 3 — confirm it works.**

```bash
python3 pipeline/check_install.py
```

You should see `Installation succeeded — … dataset loaded (413 articles).` That's it — nothing
else to set up.

---

## Using it

### Scenario 1 — find replication packages (by DOI / URL / id)

Pass a DOI, the article URL, or the paper id to `lookup.py`. It prints whether data and code
were deposited and the **exact repository link**. **One or many** at once:

```bash
# one article — by URL
python3 pipeline/lookup.py https://sociologicalscience.com/articles-v11-17-467/

# or by DOI
python3 pipeline/lookup.py 10.15195/v1.a2

# several at once — mix paper ids, DOIs, and URLs freely
python3 pipeline/lookup.py SS004 SS510 SS458

# a long list — one query per line in a text file (# starts a comment)
python3 pipeline/lookup.py --file my_ids.txt
```

Output is a compact one-line-per-article table:

```
paper   scope data code gate  package / how to obtain
----------------------------------------------------------------------------------------
SS004   Y     Y    Y    N     https://osf.io/4g8f5/
SS510   Y     N    Y    Y     https://osf.io/c34ta/
SS458   Y     N    Y    Y     http://www.thomasleopold.eu

3 article(s) found from 3 query(ies).
```

Columns: `scope` = in-scope, `data`/`code` = deposited?, `gate` = data access-gated? Open the
package link to download. For a **gated** paper with no open package the last column shows
`[gated] <how to apply>`. Add **`--detail`** for the full per-field view (title, authors, and the
verification notes). Coverage is the **413 published articles (SS001–SS511)**; anything outside
that set is listed under "not matched".

### Scenario 2 — reproduce the replication-package-availability table (independent re-coding)

This rebuilds the **replication-package-availability table** yourself: you re-run the coding method
over the articles and compare your table to the shipped one. It is driven by [Claude Code](https://claude.com/claude-code) — the
method is an LLM-agent workflow, not a fixed script — so the output is **comparable, not
byte-identical**: the agents make judgment calls, and re-running never returns an exact copy (see
[`docs/run_provenance.md`](docs/run_provenance.md)). Expect many web requests and API-token cost;
run it in batches. **Prerequisites:** Python 3 + Claude Code with API access
(see [Prerequisites](#prerequisites)).

**Step 1 — clone the repo and open Claude Code inside it.**

```bash
git clone https://github.com/borun-li/socsci-replication-availability.git
cd socsci-replication-availability
claude                      # starts Claude Code in this folder
```

**Step 2 — paste this prompt to Claude Code.** It points Claude at the method plus the blank
worklist and tells it exactly what to produce:

> Read `agent.toml` (the six-agent spec), `docs/codebook.md` (the coding rubric), and every
> `SKILL.md` under `skills/`. Then process `data/socsci_availability_blank.csv` — it has the
> bibliographic columns filled and the coding columns (`in_scope`, `qualitative`, `data`, `code`,
> `data_gated`, `data_source_apply_at`, `package_location`, `notes`) empty. For each article, run
> the method **Scope → Locate → Verify → Execute → Verify**: locate the replication package
> (journal supplemental tab first, then the article-PDF availability statement, the author
> homepage, then OSF / Harvard Dataverse / GitHub / Zenodo), verify it belongs to these authors
> and reproduces this paper, and fill the coding columns strictly per the codebook. Work in
> batches of ~20 articles and pause after each for me to review. Write the filled rows to
> `data/my_recode.csv` with the same columns.

*(Advanced — reuse the exact harness instead of free-form: ask Claude Code to run
`pipeline/six-agent-availability.js` through its Workflow tool with the worklist rows as the input
list, then `pipeline/gated_recheck.js` for `data_gated`, and `pipeline/write_inplace.py` /
`merge_all.py` to assemble the table.)*

**Step 3 — compare your coding to the shipped dataset.** Run the same summary over each file and
check the headline numbers line up:

```bash
python3 pipeline/reproduce_table.py data/my_recode.csv            # your re-coding
python3 pipeline/reproduce_table.py data/socsci_availability.csv  # the shipped dataset
```

For a row-by-row comparison, open both CSVs in a spreadsheet or `diff` them. Because the coding is
model-generated, expect close-but-not-identical agreement, concentrated on borderline judgment calls.

---

**Shortcut — just verify the published numbers** (no re-coding, Python only):

```bash
python3 pipeline/reproduce_table.py
```

It re-derives the overall rate, the by-year table, and the policy before/after split from the
shipped `data/socsci_availability.csv`. (To regenerate the chart as well, `pip install matplotlib`
first.)

### Scenario 3 — code newly published articles (extend coverage)

*Sociological Science* keeps publishing. To locate and code the replication package for **new**
articles with the same workflow (also Claude Code — see [Prerequisites](#prerequisites)):

**Step 1 — make a worklist for the new articles.** Create a CSV with the **same header** as
`data/socsci_availability_blank.csv`, one row per new article. Fill only the bibliographic columns
(`doi`, `paper_id`, `title`, `authors`, `published_date`, `submission_date`, `article_url`) and
leave every coding column empty. `paper_id` can be any unique label (e.g. `SS512`). Save it as,
say, `data/new_articles.csv`. (Tip: copy the header row out of the blank template to start.)

**Step 2 — hand it to Claude Code.** In the repo folder run `claude`, then paste:

> Read `agent.toml`, `docs/codebook.md`, and every `SKILL.md` under `skills/`. For each article in
> `data/new_articles.csv` (bibliographic columns filled, coding columns empty), run the method
> **Scope → Locate → Verify → Execute → Verify**: find the replication package (journal
> supplemental tab, then the article-PDF availability statement, author homepage, then OSF /
> Harvard Dataverse / GitHub / Zenodo), verify it belongs to these authors and reproduces this
> paper, and fill the coding columns strictly per the codebook. Write the filled rows to
> `data/new_articles_coded.csv`.

**Step 3 — use or append the results.** Look them up with
`python3 pipeline/lookup.py --file <your ids>`, or append the coded rows to
`data/socsci_availability.csv` to grow the dataset. Use the pinned parameters in
[`docs/run_provenance.md`](docs/run_provenance.md) so new coding stays consistent with the existing
table.

---

## Methodology & quality control

Each article passes through a five-stage multi-agent pipeline —
**Scope → Locate → Verify → Execute → Verify** — that classifies scope, searches every deposit
channel (journal supplemental tab, article-PDF end-matter, supplement PDF, and repository APIs:
OSF, Harvard Dataverse, GitHub, Zenodo, ICPSR …), and records what was actually inside the
package. A separate determiner then decides `data_gated` and the application route for every
in-scope paper, under the codebook rule.

Quality control:
- **Independent verification** — every positive finding is re-checked by a verifier agent for
  provenance (the repository belongs to these authors and reproduces *this* paper); every
  not-found result is re-checked by a second coverage agent — before it is recorded.
- **Manual sampling** — a random sample from each batch was checked by hand and confirmed.
- **Full-text re-reads** — borderline scope / gated calls were resolved by reading the full PDF.
- **No silent failures** — degraded or interrupted rows are skipped and re-run, never recorded
  as findings.

---

## Reproducibility

All runs use **pinned parameters** — model, prompt version, and workflow spec are frozen and
documented in [`docs/run_provenance.md`](docs/run_provenance.md), against the written
[`docs/codebook.md`](docs/codebook.md). The dataset is keyed by **DOI** and records each
article's exact **`package_location`**, so any package can be located, downloaded, and tested
directly from the table.

---

## Citation

> Li, Borun (2026). *Replication-Package Availability in Sociological Science, 2014–2026.*
> [Dataset & pipeline]. GitHub repository.

(A citable DOI will be minted when the dataset is deposited on Zenodo/OSF.)

---

## License

- **Code** (`pipeline/`, `agent.toml`): [MIT](LICENSE).
- **Dataset** (`data/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — reuse
  freely with attribution (see Citation).

---

## Contributions

Issues and pull requests are welcome — for corrections to individual codings, coverage of newly
published articles, or extensions to other journals. Please:

1. Open an issue describing the article (`doi`) and the proposed change, with evidence
   (the repository link or the article's data-availability statement).
2. For a coding change, keep the codebook rules (see `docs/codebook.md`); note which rule applies.
3. A companion **American Sociological Review (ASR)** adapter is planned, coding ASR under the
   **same codebook** so the two journals are directly comparable.

---

## Contact

Borun Li — borun.li@icloud.com
