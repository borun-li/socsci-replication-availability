---
name: code-available-data-restricted
description: Replication code is posted, but the data are available only under a signed agreement, formal application, registration, or an on-site/guest terminal. Use to classify and document gated-data papers as CODE ONLY.
---

# Scenario: CODE ONLY — data gated (on request / agreement)

The authors posted their analysis code, but the underlying data are **not** in the
package because they are restricted. The data could in principle be obtained, but only
through a gate: a data-use agreement, a formal application, paid/registered access, or a
secure on-site / guest terminal.

This is the SOP §4 "On request / gated" case — it is `CODE ONLY` **with a note**, not
`NEITHER`.

## How to recognize it
- `code/` has runnable scripts; `data/` has only a README / data-availability statement.
- The README or paper points to a restricted source: national register, survey data
  provider, or research-data center requiring application.

## Examples from this corpus
- **does-schooling-affect** — SOEP / NEPS data require a signed data access agreement.
- **breaking-barriers-persisting** — data require a formal request to ISTAT
  (`istat.it/en/data/microdata`).
- **hunkering-down-catching** — SOEP data require a special agreement and use of the
  provider's guest terminal.

## Handling steps
1. Confirm the code is genuinely present (open `code/`, list script files).
2. Record the **exact access path** in the notes — which provider, what agreement/form,
   what it costs in time. This is the "why," which SOP §4 says matters more than yes/no.
3. Do **not** downgrade to `NEITHER`; the distinction (gated vs. never-posted) is the point.

## Status classification
`CODE ONLY` — `code_availability: yes`, `data_availability: no`. Annotate the gate.

## Replication implication
Code logic can be read and the pipeline understood, but published numbers **cannot** be
reproduced without first obtaining the restricted data through the documented gate.
Flag as "blocked on data access" rather than failed.
