export const meta = {
  name: 'six-agent-availability',
  description: 'Replication-availability pipeline: Scope -> Locate -> LocVerify (POSITIVE: verify the package; NEGATIVE: independent coverage re-check to catch a MISSED package) -> Execute -> ExecVerify, with iterate-back loops and logged verification catches',
  phases: [
    { title: '1 Scope' },
    { title: '2 Locate' },
    { title: '3 LocVerify' },
    { title: '4 Execute' },
    { title: '5 ExecVerify' },
  ],
}

// Articles are embedded so the run does not depend on how `args` is delivered.
// Override by passing args (array OR JSON string) — parsed defensively below.
const ARTICLES = [
  {"paper_id": "SS287", "title": "The Inequality of Lifetime Pensions", "authors": "Jiaxin Shi, Martin Kolk", "url": "https://sociologicalscience.com/articles-v10-24-667/", "hint": ""},
  {"paper_id": "SS290", "title": "The Refugee Advantage: English-Language Attainment in the Early Twentieth Century", "authors": "Ran Abramitzky, Leah Boustan, Peter Catron, Dylan Connor, Rob Voigt", "url": "https://sociologicalscience.com/articles-v10-27-769/", "hint": ""},
  {"paper_id": "SS293", "title": "Life-Course Differences in Occupational Mobility Between Vocationally and Generally Trained Workers in Germany", "authors": "Viktor Decker, Thijs Bol, Hanno Kruse", "url": "https://sociologicalscience.com/articles-v10-30-857/", "hint": ""},
  {"paper_id": "SS300", "title": "Breaking Barriers or Persisting Traditions? Fertility Histories, Occupational Achievements, and Intergenerational Mobility of Italian Women", "authors": "Filippo Gioachin, Anna Zamberlan", "url": "https://sociologicalscience.com/articles-v11-3-67/", "hint": ""},
  {"paper_id": "SS306", "title": "Bridging the Digital Divide Narrows the Participation Gap: Evidence from a Quasi-Natural Experiment", "authors": "Vincenz Frey, Delia S. Baldassarri, Francesco C. Billari", "url": "https://sociologicalscience.com/articles-v11-9-214/", "hint": ""},
  {"paper_id": "SS308", "title": "The Effect of Workplace Raids on Academic Performance: Evidence from Texas", "authors": "Sofia Avila", "url": "https://sociologicalscience.com/articles-v11-11-258/", "hint": ""},
  {"paper_id": "SS309", "title": "Identity from Symbolic Networks: The Rise of New Hollywood", "authors": "Katharina Burgdorf, Henning Hillmann", "url": "https://sociologicalscience.com/articles-v11-12-297/", "hint": ""},
  {"paper_id": "SS310", "title": "Every Forest Has Its Shadow: The Demographics of Concealment in the United States", "authors": "Maria S. Grigoryeva, Blaine G. Robbins", "url": "https://sociologicalscience.com/articles-v11-13-340/", "hint": ""},
  {"paper_id": "SS311", "title": "Implicit Terror: A Natural Experiment on How Terror Attacks Affect Implicit Bias", "authors": "Filip Olsson", "url": "https://sociologicalscience.com/articles-v11-14-379/", "hint": ""},
  {"paper_id": "SS316", "title": "Colorism Revisited: The Effects of Skin Color on Educational and Labor Market Outcomes in the United States", "authors": "Mauricio Bucca", "url": "https://sociologicalscience.com/articles-v11-19-517/", "hint": ""},
]

// ---- structured-output schemas (force each agent to return validated JSON) ----
const PREP = { type:'object', additionalProperties:false, required:['in_scope','qualitative','reason','submission_date'],
  properties:{ in_scope:{enum:['Y','NA','?']}, qualitative:{enum:['Y','N']}, reason:{type:'string'}, submission_date:{type:'string'} } }
const LOCATE = { type:'object', additionalProperties:false, required:['found','package_location','path_to_package','coverage_checked'],
  properties:{ found:{type:'boolean'}, package_location:{type:'string'}, path_to_package:{type:'string'}, coverage_checked:{type:'string'} } }
const LOCV = { type:'object', additionalProperties:false, required:['live','is_package','ok','reason'],
  properties:{ live:{type:'boolean'}, is_package:{type:'boolean'}, ok:{type:'boolean'}, reason:{type:'string'} } }
const COVV = { type:'object', additionalProperties:false, required:['found_package','package_location','path_to_package','coverage_complete','reason'],
  properties:{ found_package:{type:'boolean'}, package_location:{type:'string'}, path_to_package:{type:'string'}, coverage_complete:{type:'boolean'}, reason:{type:'string'} } }
const EXEC = { type:'object', additionalProperties:false, required:['data','code','data_gated','data_source','notes'],
  properties:{ data:{enum:['Y','N']}, code:{enum:['Y','N']}, data_gated:{enum:['Y','N']}, data_source:{type:'string'}, notes:{type:'string'} } }
const EXECV = { type:'object', additionalProperties:false, required:['data_belongs','code_belongs','data_gated','data_source','ok','provenance','reason'],
  properties:{ data_belongs:{type:'boolean'}, code_belongs:{type:'boolean'}, data_gated:{enum:['Y','N']}, data_source:{type:'string'}, ok:{type:'boolean'}, provenance:{type:'string'}, reason:{type:'string'} } }

const GP = 'general-purpose'
// PROMPT_VERSION is FROZEN: pin it alongside model (claude-opus-4-8) + workflow (agent.toml v2.0.0).
// Any change to RULES or the stage prompts REQUIRES bumping this tag. All runs must record it.
const PROMPT_VERSION = 'socsci-avail-prompt-v3.0-2026-08-14'
const RULES = 'Codebook v3.0: in_scope Y = the paper reports ORIGINAL EMPIRICAL analysis the authors ran (quantitative OR qualitative). NA (nothing to reproduce) applies ONLY to commentary, rejoinder, editorial, or pure theory; when in_scope=NA leave qualitative/data/code/data_gated BLANK. in_scope ? = does not clearly fit either category: FLAG THE ENTIRE ROW FOR HUMAN REVIEW and say why in notes (do not force a Y/NA). qualitative Y = the primary evidence is non-numeric (interviews/ethnography/archival/textual) interpreted directly rather than converted into variables; a QUALITATIVE EMPIRICAL paper IS in scope (in_scope=Y, qualitative=Y), coded on what was deposited; a paper using BOTH qualitative and quantitative evidence = N. data Y = the authors DEPOSITED their analysis dataset in the package (a pointer to an external/public source such as ICPSR/IPUMS/GSS/NLSY/NBER/a public archive is a SOURCE, not a deposit => data=N; if the dataset is not IN the package, data=N). code Y = the authors deposited code that reproduces THIS paper results (a general method or software package, even one the authors wrote, is a TOOL not a package unless it bundles the analysis scripts for THIS paper). AVAILABLE UPON REQUEST: when data is offered only on request to the authors => data=N, data_gated=Y, and data_source/apply_at MUST be a CONCRETE route (a URL or an email address); "contact author" alone is NOT acceptable. THE ONE RULE: a Y means the located materials reproduce THIS paper - not a relevant link, not a tool, not a preprint, not a public source; when your note describes why something is NOT the package, code it N, and do not code past your own note.'

async function run(a) {
  const t = a.paper_id
  const catches = []

  // 1 SCOPE  (merged Download+Prepare — ABSTRACT ONLY, cheap; do NOT read the full/supplement PDF here)
  const prep = await agent(
    `SCOPE agent. Do ONE web fetch of the article page ${a.url} and read the ABSTRACT. Do NOT download the full-text PDF or the supplement PDF — scanning those for a hidden package is the LOCATE stage's job, not yours. ${RULES}\nPaper title: ${a.title}\nFrom the abstract, classify in_scope and qualitative. Do NOT judge by title alone. A qualitative EMPIRICAL paper (interviews/ethnography/archival) IS in scope: in_scope=Y, qualitative=Y. Use NA ONLY for a comment/rejoinder/pure-theory piece with no original empirical analysis. If unsure whether the authors ran their own empirical analysis, lean in_scope=Y. ALSO extract submission_date = the manuscript RECEIVED (or Submitted) date from the article page PROCESS INFO tab/section (sociologicalscience.com prints Received/Accepted/Published dates near the citation block — look for 'Received:'); this is NOT the published date. Return it as printed (e.g. 2019-11-10 or 'November 10, 2019'). If it is genuinely absent from the page, return submission_date=''. (Only if the abstract is genuinely missing/insufficient may you glance at the on-page intro — keep it light.)`,
    { agentType:GP, schema:PREP, label:`scope:${t}`, phase:'1 Scope' })
  if (!prep) return { paper_id:t, error:'scope-null', catches }
  const subdate = prep.submission_date || ''
  if (prep.in_scope === 'NA' || prep.in_scope === '?') {
    return { paper_id:t, submission_date:subdate, in_scope:prep.in_scope, qualitative:'', data:'', code:'', data_gated:'', data_source:'',
      package_location:'', path_to_package:'', coverage_checked:'abstract', notes:prep.reason,
      loc_iterations:0, exec_iterations:0, catches }
  }

  // 2 LOCATE  (the DEEP read: tab -> full PDF end-matter -> SUPPLEMENT PDF body -> homepages)  +  3 LOC-VERIFY (iterate-back, max 3)
  const LOC_PROMPT = `LOCATING agent. Find the replication PACKAGE for '${a.title}' by ${a.authors} (article ${a.url}). ${a.hint||''}
Scan IN ORDER, stop as soon as you find an actual package URL:
  (a) the article page's SUPPLEMENTAL MATERIAL tab / 'Reproducibility Package' / 'replication materials' line;
  (b) the FULL article PDF — read the whole document, especially the END-MATTER: data/code availability section, footnotes, acknowledgments, and appendices (a package link is often buried near the end, not the front). A bare OSF/DOI/Dataverse link counts as the package ONLY if the surrounding text says 'replication package/material'; otherwise it is a citation.
  (c) OPEN AND SCAN THE SUPPLEMENT PDF ITSELF (e.g. *_supp.pdf). A supplement is NOT automatically 'no package': it may contain the package link OR literally PRINT the replication code (look for 'Appendix: Computer Code', 'the following R/Stata code', a do-file, library(, program define, clear all, proc ). Printed code in the supplement counts as a found package.
  (d) Query REPOSITORY APIs directly by author name / title FIRST — these are plain HTTP (WebFetch), NOT keyword web-search, and have NO per-session budget, so prefer them: Harvard Dataverse https://dataverse.harvard.edu/api/search?q=<title-or-author> ; OSF https://api.osf.io/v2/nodes/?filter[title]=<keywords> and https://api.osf.io/v2/users/?filter[full_name]=<author> ; Zenodo https://zenodo.org/api/records?q=<title-or-author> ; GitHub https://api.github.com/search/repositories?q=<keywords> ; figshare https://api.figshare.com/v2/articles/search . Also WebFetch the authors' likely departmental/personal homepage URLs directly.
  (e) ONLY IF (a)-(d) all fail, use AT MOST ONE targeted web_search; if the web-search budget is exhausted, note it and rely on (a)-(d).
Resolve any Dataverse/OSF/Zenodo hit via its DOI/API rather than scraping a JavaScript page. Set found=true only with an actual package URL (or printed code located in a supplement). Record where you looked in coverage_checked. PREFER WebFetch + repository APIs; use keyword web_search sparingly (strict per-session cap).`
  let loc = await agent(LOC_PROMPT, { agentType:GP, schema:LOCATE, label:`loc:${t}`, phase:'2 Locate' })
  let locIter = 0, locv = null
  while (true) {
    if (loc && loc.found) {
      // POSITIVE: independently verify the located package
      locv = await agent(
        `LOC-VERIFICATION agent. You are given ONLY a candidate link; you did NOT find it and must not trust it. Candidate: ${loc.package_location} (reported path: ${loc.path_to_package}). Independently (real web fetch): (1) resolve it - LIVE(200) / dead(404) / auth-walled(login)? (2) does it contain a REAL package (code and/or data files, a file tree, a README, OR printed replication code in a supplement PDF) or is it manuscript-only/empty? Set ok=true ONLY if live AND a real package.`,
        { agentType:GP, schema:LOCV, label:`locv:${t}`, phase:'3 LocVerify' })
      if (!locv) { locv = { live:false, is_package:false, ok:false, reason:'verify-null' }; break }
      if (locv.ok) break
      if (locIter >= 3) { catches.push(`LOC-VERIFY rejected after ${locIter} retries: ${locv.reason}`); break }
      locIter++
      catches.push(`LOC-VERIFY forced iterate #${locIter}: ${locv.reason}`)
      loc = await agent(
        `${LOC_PROMPT}\n\nRETRY: verification rejected your previous candidate ${loc.package_location} because: ${locv.reason}. Try the OTHER sources you have not exhausted. If none truly exists, return found=false.`,
        { agentType:GP, schema:LOCATE, label:`loc-retry${locIter}:${t}`, phase:'2 Locate' })
    } else {
      // NEGATIVE: independent COVERAGE verification of the "not found" (类型三 — verify the search, catch the MISSED package)
      const cov = await agent(
        `COVERAGE-VERIFICATION agent (NEGATIVE check — the risk here is a MISSED package). A locate agent concluded NO replication package exists for '${a.title}' by ${a.authors} (${a.url}). Its claimed coverage: "${loc ? loc.coverage_checked : 'n/a'}". Do NOT trust that — a negative means 'not found', not 'does not exist'. Independently and SKEPTICALLY re-check for a package it may have MISSED: (a) the article page's SUPPLEMENTAL MATERIAL tab / any 'Reproducibility Package'/'replication materials' line; (b) the FULL article PDF END-MATTER — data/code availability section, footnotes, acknowledgments, appendices (packages hide near the end); (c) the SUPPLEMENT PDF body — it may hold a package link OR literally PRINT replication code (Appendix: Computer Code, 'the following R/Stata code', a do-file, library(, program define, proc ); (d) query REPOSITORY APIs directly by author name / title (plain HTTP, NOT keyword web-search, NO budget limit): Harvard Dataverse https://dataverse.harvard.edu/api/search?q= , OSF https://api.osf.io/v2/nodes/?filter[title]= and https://api.osf.io/v2/users/?filter[full_name]= , Zenodo https://zenodo.org/api/records?q= , GitHub https://api.github.com/search/repositories?q= , figshare https://api.figshare.com/v2/articles/search ; and WebFetch each author's constructed departmental/personal homepage URL. Use keyword web_search ONLY as a last resort (strict per-session cap) — if exhausted, rely on the APIs + direct fetches. If you FIND a real package the locate agent missed, set found_package=true with its exact package_location + path_to_package. If after genuinely re-checking EVERY source none exists, set found_package=false and coverage_complete=true. Default to skepticism about the 'not found'.`,
        { agentType:GP, schema:COVV, label:`covv:${t}`, phase:'3 LocVerify' })
      if (cov && cov.found_package && cov.package_location) {
        catches.push(`COVERAGE-VERIFY caught a MISSED package: ${cov.package_location} — ${cov.reason}`)
        loc = { found:true, package_location:cov.package_location, path_to_package:cov.path_to_package || cov.package_location,
          coverage_checked:(loc ? loc.coverage_checked : '') + ' | coverage-verify found a missed package: ' + (cov.reason||'') }
        if (locIter >= 3) { locv = { live:true, is_package:true, ok:true, reason:'adopted coverage-verify find (retry cap)' }; break }
        locIter++
        continue   // re-enter the loop -> the newly found package now gets loc-verified
      } else {
        locv = { live:false, is_package:false, ok:false, reason:'coverage-verify CONFIRMS no package: ' + ((cov && cov.reason) || 'no reason returned') }
        break
      }
    }
  }

  if (!loc || !loc.found || !locv.ok) {
    return { paper_id:t, submission_date:subdate, in_scope:prep.in_scope, qualitative:prep.qualitative, data:'N', code:'N', data_gated:'', data_source:'',
      package_location:(loc && loc.found) ? loc.package_location : '',
      path_to_package: loc ? loc.path_to_package : 'not found',
      coverage_checked: loc ? loc.coverage_checked : 'tab+PDF+supplement+author',
      notes:`No usable package: ${locv.reason}`, loc_iterations:locIter, exec_iterations:0, catches }
  }

  // 4 EXECUTE  +  5 EXEC-VERIFY  (iterate-back, max 3)
  let ex = await agent(
    `EXECUTION agent. A verified package exists at ${loc.package_location} (via ${loc.path_to_package}) for '${a.title}' by ${a.authors}. Open it (real web fetch) and decide: ${RULES} Return data and code Y/N. ALSO set data_gated + data_source: data_gated=Y when the underlying analysis data is RESTRICTED (proprietary / IRB-confidential / registration-DUA-application-required / restricted register or administrative source) EVEN IF code (or derived data) is deposited; also Y when data=N specifically because the source is restricted; N for free public data (public IPUMS/GSS/NLSY) or no restriction. When data_gated=Y, data_source = the restricted source NAME + where/how to apply (provider + URL/agreement, e.g. 'SOEP Core - data-access agreement, DIW Berlin diw.de/soep'; 'Census FSRDC census.gov/fsrdc'; 'confidential interviews - contact author'); when data_gated=N, data_source=''. Add a short evidence note.`,
    { agentType:GP, schema:EXEC, label:`exec:${t}`, phase:'4 Execute' })
  let exIter = 0, exv = null
  while (true) {
    if (!ex) { ex = { data:'N', code:'N', notes:'exec-null' }; exv = { data_belongs:false, code_belongs:false, ok:true, provenance:'', reason:'exec-null' }; break }
    exv = await agent(
      `EXEC-VERIFICATION agent. Independently confirm a deposit claim WITHOUT trusting the claimant. Paper '${a.title}' by ${a.authors}; package ${loc.package_location}; CLAIM data=${ex.data}, code=${ex.code}, data_gated=${ex.data_gated} (source: ${ex.data_source||'none'}). Check (real web fetch): (1) PROVENANCE - owner is one of these authors AND README/title cites THIS paper (RULE4); (2) the files backing each Y are really present (not inferred from a README); (3) NOT a general tool/dependency (RULE2) and NOT a preprint (RULE3). Set data_belongs/code_belongs; ok=true only if the claim as stated is fully supported. ALSO independently verify the data-access gate and RETURN data_gated + data_source: data_gated=Y if the underlying analysis data is RESTRICTED (proprietary/IRB/DUA/registration/restricted-register), even if code is deposited; N for free public sources — correct the execute agent if it over/under-called it. When data_gated=Y, data_source must name the restricted source + a concrete apply-at (provider + URL/agreement); fill/fix if missing or wrong. When data_gated=N, data_source=''.`,
      { agentType:GP, schema:EXECV, label:`exv:${t}`, phase:'5 ExecVerify' })
    if (!exv) { exv = { data_belongs:true, code_belongs:true, ok:true, provenance:'', reason:'verify-null' }; break }
    if (exv.ok) break
    if (exIter >= 3) { catches.push(`EXEC-VERIFY rejected after ${exIter} retries: ${exv.reason}`); break }
    exIter++
    catches.push(`EXEC-VERIFY forced iterate #${exIter}: ${exv.reason}`)
    ex = await agent(
      `EXECUTION agent RETRY. Verification rejected your claim: ${exv.reason}. Re-examine the package at ${loc.package_location} for '${a.title}' and return a corrected data/code assessment. REAL web fetch.`,
      { agentType:GP, schema:EXEC, label:`exec-retry${exIter}:${t}`, phase:'4 Execute' })
  }

  const finalData = (ex.data === 'Y' && exv.data_belongs) ? 'Y' : 'N'
  const finalCode = (ex.code === 'Y' && exv.code_belongs) ? 'Y' : 'N'
  if (ex.data === 'Y' && !exv.data_belongs) catches.push(`EXEC-VERIFY flipped data Y->N: ${exv.reason}`)
  if (ex.code === 'Y' && !exv.code_belongs) catches.push(`EXEC-VERIFY flipped code Y->N: ${exv.reason}`)
  const finalGated = exv.data_gated || ex.data_gated || 'N'
  const finalSource = exv.data_source || ex.data_source || ''
  if (ex.data_gated && exv.data_gated && ex.data_gated !== exv.data_gated) catches.push(`EXEC-VERIFY corrected data_gated ${ex.data_gated}->${exv.data_gated}`)

  return { paper_id:t, submission_date:subdate, in_scope:prep.in_scope, qualitative:prep.qualitative, data:finalData, code:finalCode,
    data_gated:finalGated, data_source:finalSource,
    package_location:loc.package_location, path_to_package:loc.path_to_package,
    coverage_checked:loc.coverage_checked, notes:`${ex.notes} | provenance: ${exv.provenance}`,
    loc_iterations:locIter, exec_iterations:exIter, catches }
}

// defensive args handling: array, JSON string, or fall back to embedded ARTICLES
let items = ARTICLES
if (Array.isArray(args)) items = args
else if (typeof args === 'string' && args.trim()) { try { items = JSON.parse(args) } catch (e) { items = ARTICLES } }

log(`PROMPT_VERSION=${PROMPT_VERSION} | model=claude-opus-4-8 (session-inherited) | workflow=agent.toml v2.0.0 | temperature=platform-default (not settable via Workflow)`)
log(`Running 5-stage availability pipeline (Scope+Locate+LocVerify+Execute+ExecVerify) on ${items.length} article(s)`)
const results = await parallel(items.map(a => () => run(a)))
return results.filter(Boolean)
