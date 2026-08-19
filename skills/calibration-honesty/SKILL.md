---
name: calibration-honesty
description: Cross-cutting verification discipline for the package-FINDING agent — how not to fool yourself when deciding whether a replication package was really found. Consult during the Verify phase for every candidate and every negative. Covers reading the README to catch access gates, never signing a contract/DUA/registration for gated data, provenance, and honest abstention. Distilled from SOP §5–6 + package-inspection lessons. (/code vs /data categorization is deferred — see the commented rule.)
---

# Skill: calibration & honesty (verification discipline)

This is a **method** skill, not an outcome skill. The seven outcome skills say *how to
classify a situation you have already confirmed*; this one says *how to confirm it at all*
without overclaiming. It is the heart of the finding agent's tailored verification — apply
it in the Verify phase to every positive candidate and every "didn't find" negative.

## Standing rules (SOP §5–6 + package-inspection lessons)

1. **"Didn't find" ≠ "doesn't exist."** A negative may only stand as *"didn't find after
   covering N sources."* The one exception is a **structural** negative — the data type
   makes a package impossible by nature (confidential qualitative interviews; identifiable
   network data; licensed/proprietary data; restricted administrative registers;
   FERPA-protected records). Name the specific structural reason or it is just "not posted."

2. **Open the file tree; never infer contents from the README.** We mischaracterized the
   `ineqReSample` package twice by reading the description instead of listing `data/` and
   `R/`. Always download, list the tree, and check `code/` vs `data/` separately. File
   *size* tells you scale but not provenance — a multi-MB `.rda` rules out "toy example"
   but cannot distinguish real de-identified data from synthetic data. Settle it with row
   counts / ID format against the paper's tables, or mark **completeness uncertain**.

3. **A reconstruction — or a third-party TOOL — is not the authors' deposit.** A replication
   app someone built locally, or a generated replication report, is a *different claim* from
   "the authors posted code" (SOP a19). **Likewise a link to a general-purpose tool the authors
   merely USED is not their replication package** — e.g. `github.com/ajdamico/asdfree` (a public
   utility for importing survey data) cited in SS091 is NOT that paper's deposit. Before
   recording a repo as the package, confirm it is the **authors' own replication materials for
   THIS paper** (owner is an author, README/title names this paper), not a cited tool/library.

4. **Auth-walled contents are UNVERIFIED.** Google Drive folders and some lab portals can't
   be opened directly (SOP a21, a27). Record the landing link and label the contents
   *unverified* rather than asserting what's inside → this is a `needs_review` case, not a
   confirmed positive.

5. **Verify independently — don't trust pre-filled flags or local paths.** Pre-entered
   Yes/No values and any `/Users/.../` paths are working notes, not confirmed facts, and the
   agent can't see local files. Re-check online every time. Provenance (does this package
   belong to THIS paper?) is required for every positive — a live link with real code that
   belongs to a *different* paper is a false positive, not a find.

<!-- DEFERRED — future feature: using the README to classify /code & /data. Not applied at
     this stage (we only find + download the package). Kept for later:
6-DEFERRED. Read the README to classify /code & /data — but confirm presence by the tree.
   The README (.txt/.md) is the authority for what a package contains and where the data
   live; it often states the data are external (obtained from a provider) rather than
   bundled. An empty-looking data/ may mean "external, get it per the README," not "no data."
   The tree tells you what IS present; the README tells you what is NOT present and how to
   obtain it. Never upgrade "README says data are available" into "data in hand" without the tree.
-->

6. **The agent must never sign a contract, DUA, registration, or application — and must show
   WHERE to apply.** If obtaining the data *or code* requires a signed data-use agreement, a
   user contract, sign-up/log-in, registration, or a formal application (e.g. SOEP v36's user
   contract at diw.de; Harvard Dataverse "Request Access"; CFPS at cfpsdata.pku.edu.cn;
   Statistics Denmark approved access), that is a human legal decision — do **not** sign,
   accept, log in, or apply. Flag `needs_review: on_request_gated_data` and record the
   **exact `apply_at` URL(s)** — the precise page where the human requests access, not just
   the provider name — one per gated item, then inform the user. The *package* is still a
   real, located find (record its location); only the gated part is blocked.

## How to apply it (Verify-phase checklist)

- Positive candidate → run liveness → **open the tree** (rule 2) → **read the README to catch
  access gates** (rule 6) → **prove provenance** (rule 5) → **adversarially try to refute**
  it (rules 3–4). Only a candidate that survives becomes a VERIFIED positive.
- Contract/DUA/registration required to get the data → **never sign** (rule 6); flag and
  tell the user, but still record the located package and its discovery path.
- **Before ANY negative — READ the supplement PDF for printed code.** A tab showing only a
  `SocSci_..._supp.pdf` is NOT sufficient grounds for "no package": the supplement often prints
  the replication code (an "Appendix: Computer Code", *"the following R code yields the …
  estimates"*, or an inline do-file). Open it and grep for `computer code` / `following .*code`
  / `replication code` / `do-file` / `library(` / `program define` / `clear all` / `proc `. If
  code is printed there, it is a **found package**, not a negative (this rule exists because
  SS084 and SS074 were first mis-scored N by noting only the tab link, not reading the PDF).
- **"results / data / details available on request" ≠ "replication package available on
  request."** The former only offers to email some outputs → **complete negative** (no package
  exists). Only an explicit offer of the *replication package / code* on request is an
  on-request-package case. (SS037/SS046/SS051: "results on request" → N.)
- **DATA-ONLY DEPOSIT IS NOT A PACKAGE — availability = No (professor-confirmed, RULE A).** If
  the authors deposited their OWN data but **no analysis code** (.do/.R/.py/.sps/…), the package
  is **not available** → code_availability = No, and flag **`data_only_no_code = "Y"`**. Code is
  REQUIRED for a Yes; data alone never suffices. This flag is ONLY for the authors' own data
  deposit lacking code — merely *using* a public/restricted source (GSS/ATUS/ELS/CHIP/NLSY) is a
  plain not-posted negative, **not** a data-only deposit. (SS016 kurzman.unc.edu .txt; SS027 OSF
  Brashears772 .sav + questionnaire; SS043 INGO .xlsx — all data-only → **No**.)
- **NOTHING TO SHARE → EXCLUDE FROM THE DENOMINATOR (professor-confirmed, RULE B).** When a paper
  has **no underlying code or data to provide at all**, flag **`no_code_or_data_to_share = "Y"`**
  and **exclude it from the availability denominator** (it is neither a Yes nor a No). Two kinds:
  (1) **commentary** — a comment / rejoinder / reply / methodological essay with no empirical
  analysis (mentioning statistics/p-values in the *argument* does NOT make it empirical: read the
  abstract — SS029 "Defending the Decimals", SS032 Comment & Rejoinder, SS063 Weakliem "A Comment");
  (2) **qualitative with unshareable data** — confidential interviews / ethnography / field notes
  that cannot be deposited by their nature, a *structural* impossibility, not "not-posted" (SS007
  confidential longitudinal PE interviews). NOTE: a data-only deposit (RULE A) is NOT this — it
  has data to share, so it stays a **No inside the denominator**, never excluded.
  Apply RULE B at the **[verdict] step, AFTER the search** (post-Verify). (An abstract-triage
  early-exit was prototyped to save tokens but is **PARKED/DISABLED** — the abstract only hints at
  paper TYPE not package presence, and the LLM's self-rated confidence is uncalibrated, so gating a
  denominator exclusion on it is unsafe. Rework it with observable signals — journal Comment/Reply
  metadata + quoted abstract evidence + a tab glance — before re-enabling. RULE A, data-only, cannot
  be triaged early regardless: the deposit must be found first.)
- Negative → run the coverage check; if every SOP §2 source was visited, classify
  `structural` / `not-posted` / `on-request` (rule 1). Never assert "doesn't exist."
- Any residual doubt → **abstain**: flag `needs_review` with the reason and the provenance
  trail. Honest abstention is a first-class output, never a penalty.

## Why this matters

Miscalibration here corrupts the whole corpus: a false positive attributes a package to the
wrong paper; a careless negative inflates the field's "no-package" rate. The calibration
cost of one wrong confident verdict is far higher than the cost of one honest `needs_review`.
