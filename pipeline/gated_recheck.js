export const meta = {
  name: 'gated-recheck',
  description: 'Re-decide data_gated under a TIGHTENED definition: Y only if data needs a special application/access route',
  phases: [{ title: 'Recheck' }],
}

const GP = 'general-purpose'
const PROMPT_VERSION = 'socsci-gated-recheck-v3.2-2026-08-18'

const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['paper_id', 'data_gated', 'data_source', 'access_route', 'reason'],
  properties: {
    paper_id: { type: 'string' },
    data_gated: { enum: ['Y', 'N'] },
    data_source: { type: 'string' },
    access_route: { type: 'string' },
    reason: { type: 'string' },
  },
}

const RULE = `Decide data_gated (Y/N) for this paper per codebook v3.2. Read the article's data source.

data_gated = Y whenever the underlying analysis data is NOT freely/publicly available — i.e. it is restricted, confidential, proprietary, institutional-access-only, a register/administrative source, IRB-protected, or author-collected human-subjects data (interviews, ethnography, surveys, experiments) — REGARDLESS of whether an external application route exists.
  - If there IS a route (formal application/DUA/RDC; paid license/purchase; available-on-request email; registration portal), put it in access_route.
  - If there is NO external route (discretionary or institutional access granted only to the authors; ad-hoc data sharing between researchers; unnamed proprietary source; confidential interviews the authors did not deposit), STILL return Y and use access_route to EXPLAIN WHY there is no external route.
  In all Y cases, data_source = the source name; access_route = the route OR the explanation of why none exists.

data_gated = N ONLY when:
  - the data is genuinely PUBLIC / freely downloadable (public GSS, IPUMS, ANES, ACS/Census PUMS, NLSY, open survey archives, OPEN Harvard Dataverse / OSF deposits, open web data); OR
  - the analysis data are the authors' own SIMULATION outputs.
MERE NON-PROVISION -> N applies ONLY when the underlying source is itself PUBLIC (a public dataset the authors simply did not re-post). If the data is inherently restricted/confidential/proprietary, it is Y even with no route.

CRITICAL: author-collected confidential human-subjects data (interviews, ethnography, MTurk/vignette experiments, proprietary firm/institutional data) = RESTRICTED = Y, with access_route explaining the restriction. Return N only for genuinely public sources or simulations.`

async function run(a) {
  const r = await agent(
    `${RULE}\n\nPaper: ${a.paper_id} — "${a.title}" by ${a.authors}. Article page: ${a.url}\nFetch the article page and (if needed) the PDF data/methods + end-matter to identify the data source AND whether a concrete special-access route exists. Then decide data_gated strictly per the tightened rule and return the schema.`,
    { agentType: GP, schema: SCHEMA, label: `recheck:${a.paper_id}`, phase: 'Recheck' })
  if (!r) return { paper_id: a.paper_id, data_gated: '', data_source: '', access_route: '', reason: 'agent-null' }
  return r
}

const items = Array.isArray(args) ? args : JSON.parse(args)
log(`PROMPT_VERSION=${PROMPT_VERSION} | tightened gated re-check on ${items.length} currently-Y papers`)
const results = await parallel(items.map(a => () => run(a)))
return results.filter(Boolean)
