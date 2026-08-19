---
name: data-partially-available
description: Code is posted and SOME of the data are available (e.g. in supplemental material), but at least one required dataset is gated. Use for partial-data papers where full reproduction is blocked by the missing piece.
---

# Scenario: CODE ONLY — data partially available

The code is posted and part of the data can be obtained (bundled, anonymised, or printed
in the supplemental material), but one or more datasets needed to reproduce the full
results are gated (email request, separate application). Because complete reproduction is
blocked by the missing piece, the verdict is `data_availability: no` with a note that
some data are present.

## How to recognize it
- `code/` has runnable scripts.
- `data/` has some real material (a supplemental PDF with tables, anonymised transcripts,
  a partial dataset) but **not** every input the code consumes.
- The README/paper indicates a further dataset is available only on request.

## Example from this corpus
- **unreliable-ladder-top** — Stata reproduction code plus anonymised interview
  transcripts and a supplemental-material PDF are included, but one dataset requires an
  email request. Classified `data_availability: no` because that dataset gates full
  reproduction.

## Handling steps
1. Inventory exactly **which** inputs are present and which are missing (map each to the
   code that consumes it).
2. Decide what subset of tables/figures is reproducible from the available portion.
3. Record the access path for the missing dataset (per SOP §4, keep the "why" precise).

## Status classification
`CODE ONLY` — `code_availability: yes`, `data_availability: no` — **with a note** that
data are partially available. (Adjust to `BOTH` only if the missing piece is not actually
required for the headline results.)

## Replication implication
Partial reproduction only: the analyses driven by the available data can be re-run; the
rest is blocked until the gated dataset is obtained.
