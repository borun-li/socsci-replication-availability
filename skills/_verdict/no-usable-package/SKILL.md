---
name: no-usable-package
description: A "package" was located but it contains no runnable code and no real dataset — only the manuscript, appendix, figures, or a pre-analysis plan. Use to classify these as NEITHER / not-posted.
---

# Scenario: NEITHER — no usable code or data (not posted)

Something was downloaded and filed under `code/` or `data/`, but on inspection it holds
no runnable code and no actual dataset — just the manuscript, an appendix, figure images,
or a pre-analysis plan. This is the SOP §4 "Not posted" case: phrase the verdict as
"didn't find," not "doesn't exist."

## How to recognize it
- `code/` and `data/` contain only `.docx` / `.pdf` manuscripts, appendices, or `.png` /
  `.pdf` figures — no `.do` / `.R` / `.py` scripts, no `.dta` / `.csv` / `.rda` data.
- An automated note may misread a manuscript or figure bundle as "contains data."

## Examples from this corpus
- **gender-flexibility-not** — the package is only the manuscript
  (`Dernberger & Pepin_future families_SocArXiv.docx/.pdf`). No code, no data.
- **feasible-peer-effects** — only an appendix (`Appendix.docx`), a tables/figures doc,
  figure images (`Figure2.png`), and a pre-analysis plan PDF. No runnable code, no dataset.

## Handling steps
1. **Open the file tree** (SOP §5) and confirm every file is a document/figure, not code
   or data. Do not infer contents from folder names or an automated note.
2. Before finalizing, run the SOP §2 search order once (article PDF, each author's site by
   role, project/lab sites, repos) to be sure a real package isn't posted elsewhere.
3. Distinguish from the *structural* case: if data are confidential by nature
   (interviews, identifiable networks, licensed/register data), note that reason instead.

## Status classification
`NEITHER` — `code_availability: no`, `data_availability: no`. Note "not posted / didn't find."

## Replication implication
Not replicable. There is nothing to run and nothing to load.
