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
│   ├── socsci_all_v3.xlsx       # the full dataset (413 rows)
│   ├── socsci_all_v3.csv        # same, CSV
│   └── availability_by_year.png # the chart above
├── docs/
│   ├── codebook.md              # coding manual (v3.2) — field definitions & rules
│   └── run_provenance.md        # pinned run parameters (model, prompts, workflow)
└── pipeline/
    ├── lookup.py                  # look up one article's package by DOI/URL/id  ← start here
    ├── reproduce_table.py         # recompute the availability table from the dataset
    ├── six-agent-availability.js  # main coding pipeline (Claude Code Workflow script)
    ├── gated_recheck.js           # data_gated determiner (codebook v3.2)
    ├── gated_determination.js     # data_gated determiner (initial variant)
    ├── write_v3.py               # write pipeline output into the v3 schema
    ├── write_inplace.py          # fill coding into an existing v3 table
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

## Quick Start (install)

The two everyday tools — **look up a package** and **reproduce the table** — are plain Python
scripts that read the shipped dataset. They need **only Python 3** (no `pip install`, no API key)
and run the same on **macOS, Linux, and Windows**. (Re-coding articles *from scratch* is a
separate, heavier path that needs Claude Code — see "From scratch" at the end.)

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

**Step 3 — confirm it works.** Run the reproduction tool:

```bash
python3 pipeline/reproduce_table.py
```

If you see the availability table print (ending with `submitted ON/AFTER 2023-04-01 : 113/119 =
95.0%`), the install is good. You're done — nothing else to set up.

---

## Using it

### Scenario 1 — find replication packages (by DOI / URL / id)

Pass a DOI, the article URL, or the paper id to `lookup.py`. It prints whether data and code
were deposited and the **exact repository link**. **One or many** at once:

```bash
# one article
python3 pipeline/lookup.py 10.15195/v1.a2
python3 pipeline/lookup.py https://sociologicalscience.com/articles-v11-17-467/

# several at once — mix ids, DOIs, and URLs freely
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

### Scenario 2 — reproduce the availability table

Recompute every headline number (overall rate, by-year, and the policy before/after split)
directly from the dataset — no arguments needed:

```bash
python3 pipeline/reproduce_table.py
```

This reads `data/socsci_all_v3.csv` and re-derives the figures in this README, so you can verify
them yourself. To regenerate the **chart** (`data/availability_by_year.png`) as well, install
matplotlib first (`pip install matplotlib`) — the numbers above need no extra packages.

---

### From scratch (re-code articles) — requires Claude Code

The figures above come from a coded dataset; **producing that coding** is a multi-agent workflow,
not a one-command script. `pipeline/six-agent-availability.js` and `gated_recheck.js` are **Claude
Code Workflow scripts** (they call the agent-orchestration API and drive the `skills/` above), and
`agent.toml` is their spec. Re-running them needs [Claude Code](https://claude.com/claude-code)
with API access, and — per [`docs/run_provenance.md`](docs/run_provenance.md) — is inherently
non-deterministic (the coding is model-generated). The `pipeline/*.py` files are the plain-Python
writers/mergers that assemble the coded outputs into the final table. This path is for extending
coverage or auditing the method, not for everyday use.

---

## Methodology & quality control

Each article passes through a five-stage multi-agent pipeline —
**Scope → Locate → Verify → Execute → Verify** — that classifies scope, searches every deposit
channel (journal supplemental tab, article-PDF end-matter, supplement PDF, and repository APIs:
OSF, Harvard Dataverse, GitHub, Zenodo, ICPSR …), and records what was actually inside the
package. A separate determiner then decides `data_gated` and the application route for every
in-scope paper, under the codebook v3.2 rule.

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
2. For a coding change, keep the codebook v3.2 rules (see `docs/codebook.md`); note which rule applies.
3. A companion **American Sociological Review (ASR)** adapter is planned, coding ASR under the
   **same codebook** so the two journals are directly comparable.

---

## Contact

Borun Li — borun.li@icloud.com
