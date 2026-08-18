export const meta = {
  name: 'gated-determination',
  description: 'Determine data_gated + data_source/apply_at for data=N papers whose analysis data may be restricted (codebook v3.0)',
  phases: [{ title: 'Gated' }],
}

const GP = 'general-purpose'
const PROMPT_VERSION = 'socsci-gated-v3.0-2026-08-18'

const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['paper_id', 'data_gated', 'data_source', 'reason'],
  properties: {
    paper_id: { type: 'string' },
    data_gated: { enum: ['Y', 'N'] },
    data_source: { type: 'string' },
    reason: { type: 'string' },
  },
}

const RULE = `Determine ONLY data_gated (Y/N) and data_source/apply_at for this paper, per codebook v3.0. The paper has NO deposited dataset (data=N); your job is to decide whether the UNDERLYING analysis data is RESTRICTED.
data_gated=Y when the underlying analysis data is restricted: proprietary, IRB/confidential, registration/DUA/application-required, or a restricted register/administrative/microdata source (e.g. GSOEP/SOEP, national registers, Add Health restricted-use, IRS/SSA admin data, confidential interviews, proprietary firm data). It is Y EVEN THOUGH nothing is deposited, because the source itself is access-restricted.
data_gated=N when the analysis data is FREE and PUBLIC (public GSS, public IPUMS/ACS/Census PUMS, public NLSY, public survey archives with open download, public web/administrative data anyone can get without an application). "Available upon request from the authors" WITH restricted underlying data = Y; but merely "results available on request" over public data = N.
When data_gated=Y, data_source MUST name the restricted source AND a concrete apply-at (provider + URL or agreement or email). Examples: "GSOEP/SOEP Core - data-access agreement, DIW Berlin (diw.de/en/diw_01.c.601584.en/data_access.html)"; "Add Health restricted-use - DUA, Carolina Population Center UNC (addhealth.cpc.unc.edu/data/restricted-use-data/)"; "confidential interviews - corresponding author <email>". When data_gated=N, data_source=''.`

async function run(a) {
  const r = await agent(
    `${RULE}\n\nPaper: ${a.paper_id} — "${a.title}" by ${a.authors}. Article page: ${a.url}\nFetch the article page and, if needed, the full PDF end-matter / data section to identify the DATASOURCE used in the analysis. Then decide data_gated and (if Y) the data_source/apply_at. Be strict: public GSS/IPUMS/ACS/Census-PUMS/NLSY = N. Restricted register/admin/microdata/proprietary/IRB/confidential = Y. Return the schema.`,
    { agentType: GP, schema: SCHEMA, label: `gated:${a.paper_id}`, phase: 'Gated' })
  if (!r) return { paper_id: a.paper_id, data_gated: '', data_source: '', reason: 'agent-null' }
  return { paper_id: a.paper_id, data_gated: r.data_gated, data_source: r.data_source, reason: r.reason }
}

const items = Array.isArray(args) ? args : JSON.parse(args)
log(`PROMPT_VERSION=${PROMPT_VERSION} | model=claude-opus-4-8 | gated-determination on ${items.length} data=N papers`)
const results = await parallel(items.map(a => () => run(a)))
return results.filter(Boolean)
