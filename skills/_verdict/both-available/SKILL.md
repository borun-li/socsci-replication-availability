---
name: both-available
description: Both replication code and the underlying data are publicly posted and have been downloaded. Use when a package contains runnable scripts AND real datasets, so the paper can be reproduced end-to-end.
---

# Scenario: BOTH (code + data in hand)

The replication package (or a combination of package + external link) provides both
runnable code and the actual datasets, and you have successfully downloaded both.

## How to recognize it
- `code/` contains runnable scripts (`.do`, `.R`, `.py`, `.ipynb`, `.sas`, …).
- `data/` contains real datasets (`.dta`, `.csv`, `.rda`, `.npy`, raw data files), not
  just the manuscript, figures, or a README.
- Data may live in the package directly, **or** behind a link named in the README /
  paper that you were able to retrieve (sometimes after free registration).

## Examples from this corpus
- **stereotypical-gender-associations** — code is the author's GitHub repo
  (`.ipynb` + `.py`); data are the HistWords word embeddings
  (`eng-all_sgns.zip`, `*-w.npy` / `*-vocab.pkl`) downloaded from the
  `snap.stanford.edu` link given in the README.
- **bridging-digital-divide** — code is Stata `.do` (`FBB_SocSci23`); data are the
  ANES 2012 Time Series files downloaded after free registration
  (`anes_timeseries_2012_rawdata.txt`, `…web_laptop_flag.csv`).

## Handling steps
1. **Open the actual file tree — do not trust the README** (SOP §5). List `code/` and
   `data/` separately and confirm both contain real artifacts.
2. **Confirm provenance, not just size** (SOP §5). Check row counts / ID formats against
   the paper's tables (`dim()`, `head()` in R; `describe` in Stata) to confirm the
   bundled data is the real (de-identified) data, not a toy/synthetic sample.
3. Note the exact data source and any registration step needed to obtain it.

## Status classification
`BOTH` — `code_availability: yes`, `data_availability: yes`.

## Replication implication
Fully replicable. Proceed to environment setup and run the package; compare output to
the published figures/tables. This is the only scenario where full numeric reproduction
is expected.
