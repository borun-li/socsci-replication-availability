#!/usr/bin/env python3
"""Fill Block B (+ submission_date) into an existing v3.2-schema input table, by paper_id.
Leaves Block A (doi, title, authors, published_date, article_url) untouched.
Skips degraded rows ('no reason returned' / error). data_and_code / neither computed here.
Usage: write_inplace.py <task_output.json> <target_v3.2.xlsx>
"""
import sys, json, re, openpyxl

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

def fu(*vals):
    for x in vals:
        m = re.search(r'https?://[^\s")]+', x or '')
        if m: return m.group(0).strip('.,)')
    return ''

def trim(s, n):
    s = s or ''
    return s if len(s) <= n else s[:n-3] + '...'

def main():
    outj, target = sys.argv[1], sys.argv[2]
    res = {r['paper_id']: r for r in (find_rows(json.load(open(outj))) or [])}
    wb = openpyxl.load_workbook(target); ws = wb['availability']
    col = {c.value: i+1 for i, c in enumerate(ws[1])}
    def yn(v): return v if v in ('Y', 'N') else ''
    written, skipped = [], []
    for row in range(2, ws.max_row+1):
        pid = ws.cell(row, col['paper_id']).value
        r = res.get(pid)
        if not r: continue
        note = r.get('notes') or ''
        if r.get('error') or 'no reason returned' in note:
            skipped.append(pid); continue
        insc = r.get('in_scope', '')
        data = yn(r.get('data', '')) if insc == 'Y' else ''
        code = yn(r.get('code', '')) if insc == 'Y' else ''
        dac = ('Y' if data == 'Y' and code == 'Y' else 'N') if (data and code) else ''
        neither = ('Y' if data == 'N' and code == 'N' else 'N') if (data and code) else ''
        gated = yn(r.get('data_gated', '')) if insc == 'Y' else ''
        src = (r.get('data_source') or '') if gated == 'Y' else ''
        found = (data == 'Y' or code == 'Y')
        ws.cell(row, col['submission_date']).value = r.get('submission_date', '') or None
        ws.cell(row, col['in_scope']).value = insc
        ws.cell(row, col['qualitative']).value = (r.get('qualitative', '') if insc == 'Y' else '') or None
        ws.cell(row, col['data']).value = data or None
        ws.cell(row, col['code']).value = code or None
        ws.cell(row, col['data_and_code']).value = dac or None
        ws.cell(row, col['neither']).value = neither or None
        ws.cell(row, col['data_gated']).value = gated or None
        ws.cell(row, col['data_source_apply_at']).value = (trim(src, 900) if gated == 'Y' else None)
        ws.cell(row, col['package_location']).value = (fu(r.get('package_location'), r.get('path_to_package')) if found else '') or None
        ws.cell(row, col['path_to_package']).value = trim(r.get('path_to_package', ''), 300) or None
        ws.cell(row, col['coverage_checked']).value = trim(r.get('coverage_checked', ''), 2500) or None
        ws.cell(row, col['notes']).value = trim(note, 2100) or None
        written.append(pid)
    wb.save(target)
    print(f"written {len(written)} | skipped(degraded) {len(skipped)}: {sorted(skipped)}")

if __name__ == '__main__':
    main()
