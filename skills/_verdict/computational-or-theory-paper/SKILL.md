---
name: computational-or-theory-paper
description: A simulation, agent-based, or formal-theory paper with no empirical dataset. Use to avoid mis-scoring these as empty — code may still be postable, and some are reproducible from in-text parameters alone.
---

# Scenario: Computational / theory / simulation paper

"No empirical dataset" does **not** mean "nothing to share" (SOP §4). A simulation or
agent-based paper has *code* that could be posted even though its inputs are synthetic;
a formal-theory paper may print every input in the text, making it reproducible from the
article alone.

## How to recognize it
- The paper is a simulation, agent-based model, or formal/mathematical theory.
- There is no survey/administrative dataset by design; inputs are synthetic, generated,
  or fully specified parameters/matrices/seeds.

## Handling rules (SOP §4)
- **Simulation code posted** → `CODE ONLY` (or `BOTH` if example/generated data is bundled).
- **Simulation code not posted** → `NEITHER`, but classify as "not posted," **not** as a
  structural negative. (Macy & Evtushenko: simulation code simply not posted.)
- **Formal theory with all inputs printed in the text** (matrices, parameters, seeds) →
  reproducible from the article alone; note this explicitly rather than calling it empty.
  (Friedkin & Proskurnikov was this case.)

## Standing caution (SOP §5)
A **third-party or local reconstruction is not the authors' deposit.** A replication app
someone built, or a generated replication report, is a different claim from "the authors
posted code." Be explicit about what the code column is tracking.

## Status classification
Varies — `CODE ONLY`, `BOTH`, or `NEITHER (not posted)`. Never tag a computational paper
as a *structural* negative; the structural category is for confidential/restricted data,
not for "the model had no external data."

## Replication implication
Often the most reproducible class when code or full parameters are available: rerun the
simulation, or re-implement from the printed inputs, and compare to the paper. Set a seed
and expect exact or near-exact matches.
