#!/usr/bin/env python3
"""Write workflow output rows into a codebook v3.0 SocSci schema xlsx.
Usage: write_v3.py <task_output.json> <existing_batchN_results.xlsx> <out.xlsx>
Block A (SocSci): doi, paper_id, title, authors, published_date, submission_date, article_url
Block B: in_scope, qualitative, data, code, data_and_code, neither, data_gated,
         data_source_apply_at, package_location, path_to_package, coverage_checked, notes
data_and_code / neither are computed here (pipeline code, never an agent judgment).
"""
import sys, json, re, urllib.request, urllib.parse, openpyxl

def find_rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'paper_id' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            r = find_rows(v)
            if r: return r
    if isinstance(o, str):
        try: return find_rows(json.loads(o))
        except Exception: return None
    return None

_doi_cache = {}
def crossref_doi(title, want="Sociological Science"):
    if title in _doi_cache: return _doi_cache[title]
    q = urllib.parse.urlencode({'query.bibliographic': title, 'rows': 5})
    req = urllib.request.Request(f"https://api.crossref.org/works?{q}",
          headers={'User-Agent': 'socsci-availability/1.0 (mailto:borun.li@icloud.com)'})
    doi = ''
    try:
        d = json.load(urllib.request.urlopen(req, timeout=25))
        for it in d.get('message', {}).get('items', []):
            ct = ' '.join(it.get('container-title', []) or [])
            if want.lower() in ct.lower():
                doi = it.get('DOI', ''); break
    except Exception as e:
        doi = ''
    _doi_cache[title] = doi
    return doi

def fu(*vals):
    for x in vals:
        m = re.search(r'https?://[^\s")]+', x or '')
        if m: return m.group(0).strip('.,)')
    return ''

def trim(s, n):
    s = s or ''
    return s if len(s) <= n else s[:n-3] + '...'

def main():
    outj, existing, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    rows = find_rows(json.load(open(outj))) or []
    rows = {r['paper_id']: r for r in rows}
    # bib metadata (published_date, url, title, authors) from the existing results file
    ex = openpyxl.load_workbook(existing, read_only=True)['Borun']
    exhdr = [c.value for c in next(ex.iter_rows(min_row=1, max_row=1))]
    exi = {h: i for i, h in enumerate(exhdr)}
    bib = {}
    for r in ex.iter_rows(min_row=2, values_only=True):
        if r[0]:
            bib[r[0]] = dict(title=r[exi.get('title', 1)], authors=r[exi.get('author(s)', 2)],
                             published=r[exi.get('published_date', 3)], url=r[exi.get('article_url', 4)])
    cols = ['doi','paper_id','title','authors','published_date','submission_date','article_url',
            'in_scope','qualitative','data','code','data_and_code','neither','data_gated',
            'data_source_apply_at','package_location','path_to_package','coverage_checked','notes']
    # MERGE mode: if the target exists, load it and update/append by paper_id (preserves other groups + manual fixes)
    import os
    if os.path.exists(outp):
        wb = openpyxl.load_workbook(outp); ws = wb['availability']
        existing_hdr = [c.value for c in ws[1]]
        assert existing_hdr == cols, f"schema mismatch in {outp}"
        pid_row = {ws.cell(r,2).value: r for r in range(2, ws.max_row+1) if ws.cell(r,2).value}
    else:
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'availability'
        ws.append(cols); pid_row = {}
    ci = {h:i+1 for i,h in enumerate(cols)}
    def yn(v): return v if v in ('Y','N') else ''
    def put(pid, values):
        if pid in pid_row:
            r = pid_row[pid]
            for c,val in enumerate(values, start=1): ws.cell(r,c).value = val
        else:
            ws.append(values)
    for pid in sorted(rows.keys()):
        r = rows[pid]; b = bib.get(pid, {})
        insc = r.get('in_scope','')
        data = yn(r.get('data','')) if insc == 'Y' else ''
        code = yn(r.get('code','')) if insc == 'Y' else ''
        dac = ('Y' if data=='Y' and code=='Y' else 'N') if (data and code) else ''
        neither = ('Y' if data=='N' and code=='N' else 'N') if (data and code) else ''
        gated = yn(r.get('data_gated','')) if insc == 'Y' else ''
        src = (r.get('data_source') or '') if gated == 'Y' else ''
        found = (data == 'Y' or code == 'Y')
        put(pid, [
            crossref_doi(b.get('title') or r.get('title') or pid),
            pid, b.get('title') or r.get('title'), b.get('authors') or r.get('authors'),
            b.get('published'), r.get('submission_date',''), b.get('url'),
            insc, (r.get('qualitative','') if insc=='Y' else ''), data, code, dac, neither, gated,
            trim(src, 900),
            fu(r.get('package_location'), r.get('path_to_package')) if found else '',
            trim(r.get('path_to_package',''), 300), trim(r.get('coverage_checked',''), 2500),
            trim(r.get('notes',''), 2100),
        ])
    wb.save(outp)
    print(f"wrote {len(rows)} rows -> {outp}")
    # quick tally
    ins = [r for r in rows.values() if r.get('in_scope')=='Y']
    av = [r for r in ins if r.get('data')=='Y' or r.get('code')=='Y']
    print(f"in_scope Y={len(ins)}  availability={len(av)}/{len(ins)}  data_gated={sum(1 for r in ins if r.get('data_gated')=='Y')}")

if __name__ == '__main__':
    main()
