# Run Provenance — Frozen Parameters (Replication-Availability Coding)

These parameters are **pinned**. Every run — SocSci (remaining + re-fixes) and the future ASR
adapter — MUST use exactly these. Changing any of them requires bumping `PROMPT_VERSION` and
recording the change here.

| Parameter | Frozen value | Where it is fixed |
|-----------|--------------|-------------------|
| **Model** | `claude-opus-4-8` | Workflow sub-agents inherit the session main-loop model (no per-agent override in the script). Verified from run logs: 16,513 `"model":"claude-opus-4-8"` records, no other model. |
| **Workflow / agent spec** | `agent.toml` **v2.0.0** | `artifacts/output/package_avai/agent.toml` header (`version = "2.0.0"`). |
| **Prompt version — scope/data/code** | `socsci-avail-prompt-v3.0-2026-08-14` | `PROMPT_VERSION` in the main pipeline script. Produces `in_scope`/`qualitative`/`data`/`code`/`submission_date`. Unchanged since v3.0 — the v3.1/v3.2 refinements were to `data_gated` only, which is now a separate pass (below). |
| **Prompt version — data_gated/apply_at** | `socsci-gated-recheck-v3.2-2026-08-18` | `PROMPT_VERSION` in the gated-determiner script `scratchpad/gated_recheck.js`. Produces the FINAL `data_gated` + `data_source_apply_at` for every in-scope paper. Aligned to `codebook.md` **v3.2**. |
| **Codebook** | **v3.2** (`codebook.md`) | The whole coding rubric. Final `data_gated` values in all deliverables come from the v3.2 determiner. |
| **Temperature — pinned protocol value** | **`temperature = 0`** | The value every run of this protocol MUST use (future ASR adapter, any re-run). See the constraint note below for how it is enforced today vs. going forward. |
| **Temperature — actually used for the current 413-article dataset** | **platform default (NOT `0`)** | The Workflow harness does **not** expose a temperature parameter, so the existing dataset was produced at the platform default, not at the pinned value. None is recorded in any run log. See the note below. |

## Coding is a two-component process (both prompts frozen)

**1. Main pipeline** — `~/.claude/projects/-Users-apple-program-research-repli/9e569dc5-69dc-4493-804e-c20b797c3318/workflows/scripts/six-agent-availability-wf_2da24288-8e4.js`
- `PROMPT_VERSION = 'socsci-avail-prompt-v3.0-2026-08-14'` (frozen).
- The `RULES` string + the five stage prompts (Scope → Locate → LocVerify/CoverageVerify →
  Execute → ExecVerify) produce `in_scope` / `qualitative` / `data` / `code` /
  `submission_date` (and a preliminary `data_gated`).
- The run start logs one line stamping model + workflow + prompt version + temperature.

**2. Gated determiner** — `scratchpad/gated_recheck.js`
- `PROMPT_VERSION = 'socsci-gated-recheck-v3.2-2026-08-18'` (frozen).
- Run as a second pass over every in-scope paper to produce the FINAL `data_gated` +
  `data_source_apply_at` under the tightened codebook-v3.2 rule (data is gated whenever it is
  not freely/publicly available — restricted / confidential / proprietary / institutional /
  register / IRB — even with no external route; only genuinely public sources or authors' own
  simulation outputs are `N`).

Editing either prompt requires bumping its `PROMPT_VERSION` and adding a changelog row here.

## Temperature — important constraint

**The protocol pins `temperature = 0`, but this is a specification, not a description of how the
current dataset was produced.** The two must be read separately:

- **Pinned protocol value = `0`.** Every run of this coding protocol is *required* to use
  `temperature = 0`, to minimise sampling randomness and maximise reproducibility. This is the
  standard the ASR adapter and any re-run must meet.
- **Actually used for the current 413-article SocSci dataset = platform default (NOT `0`).**
  Temperature is **not a knob** in the current Workflow-based pipeline: the harness that spawns
  the sub-agents does not accept a temperature argument, so `0` could not be enforced within this
  architecture. The existing dataset therefore ran at the platform default. This is recorded, not
  chosen — **do not read the pinned `0` as the value that produced these numbers.**

To actually *enforce* `temperature = 0`, the pipeline must be re-implemented directly on the
Anthropic Messages API/SDK (where `temperature` is a request parameter). That is a larger change
and is **deferred**; when done, this note should be updated to state that the data was produced at
`0`. Note that even `temperature = 0` does not guarantee byte-identical LLM outputs (floating-point
/ batching / routing non-determinism) — it minimises, not eliminates, run-to-run variation.

Decisions on record: (2026-08-14) stay on the current architecture and document the default;
(2026-08-19) pin `temperature = 0` as the protocol value going forward, while keeping the honest
record that the current dataset used the platform default.

## Prompt changelog

| PROMPT_VERSION | Date | Change |
|----------------|------|--------|
| `socsci-gated-recheck-v3.2-2026-08-18` | 2026-08-18 | **codebook v3.2** — `data_gated` = Y whenever data is not freely/publicly available (restricted/confidential/proprietary/institutional/register/IRB), **even with no external route** (apply_at explains why); N only for genuinely public sources or authors' own simulation. Supersedes the v3.1 "must have an application route" reading. Applied as a dedicated determiner pass over all in-scope papers. |
| `socsci-gated-recheck-v3.1-2026-08-18` | 2026-08-18 | **codebook v3.1** — first tightening: `data_gated` = Y only if data needs a special application/access route; "mere non-provision" → N. Superseded same day by v3.2. |
| `socsci-avail-prompt-v3.0-2026-08-14` | 2026-08-14 | Main pipeline aligned to `codebook.md` v3.0: `?` → flag entire row for human review; data pointer to public archive (incl. ICPSR/IPUMS/GSS/NLSY/NBER) is never a deposit; "available upon request" → data=N; NA leaves data_gated blank; "do not code past your own note." (This prompt covers scope/data/code; unchanged in v3.1/v3.2.) |
| (prior, untagged) | 2026-08-03 | Batch-3 prompt: moved `data_gated` + `data_source/apply_at` extraction into Execute, verified by Exec-Verify. |
