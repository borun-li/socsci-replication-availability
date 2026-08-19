#!/usr/bin/env python3
"""Merge coded new articles into the main dataset (Scenario 3, Step 3).

Appends the rows of a coded worklist (default `data/new_articles.csv`) into the shipped dataset
`data/socsci_availability.csv` (and the .xlsx if openpyxl is available). It is a safe merge:

  - only rows that are actually **coded** (in_scope filled) are added — uncoded rows are skipped,
  - rows whose doi or paper_id already exist in the dataset are skipped as duplicates,
  - merged rows are tagged `batch = new`.

Usage:
    python3 pipeline/merge_new.py                        # merge data/new_articles.csv
    python3 pipeline/merge_new.py path/to/coded.csv      # a different source
    python3 pipeline/merge_new.py --dry-run              # show what would happen, change nothing

Standard library for the CSV update; the .xlsx is updated only if `openpyxl` is installed.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, os.pardir, "data")
CSV = os.path.join(DATA, "socsci_availability.csv")
XLSX = os.path.join(DATA, "socsci_availability.xlsx")


def main() -> int:
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    dry = "--dry-run" in args
    srcs = [a for a in args if a != "--dry-run"]
    src = srcs[0] if srcs else os.path.join(DATA, "new_articles.csv")

    for path, what in ((src, "source worklist"), (CSV, "main dataset")):
        if not os.path.exists(path):
            print(f"ERROR: {what} not found: {path}", file=sys.stderr)
            return 2

    with open(CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        main_cols = reader.fieldnames
        main_rows = list(reader)
    have_doi = {(r.get("doi") or "").strip().lower() for r in main_rows if (r.get("doi") or "").strip()}
    have_pid = {(r.get("paper_id") or "").strip() for r in main_rows}

    with open(src, newline="", encoding="utf-8") as f:
        new_rows = list(csv.DictReader(f))

    add, skipped = [], []
    for r in new_rows:
        pid = (r.get("paper_id") or "").strip()
        doi = (r.get("doi") or "").strip().lower()
        if not (r.get("in_scope") or "").strip():
            skipped.append((pid or doi or "?", "not coded yet (in_scope empty)"))
            continue
        if doi and doi in have_doi:
            skipped.append((pid or doi, "duplicate doi already in dataset"))
            continue
        if pid and pid in have_pid:
            skipped.append((pid, "duplicate paper_id already in dataset"))
            continue
        row = {c: (r.get(c) or "") for c in main_cols}
        if "batch" in main_cols:
            row["batch"] = "new"
        add.append(row)
        have_doi.add(doi); have_pid.add(pid)

    for pid, why in skipped:
        print(f"  skip {pid}: {why}")
    print(f"{len(add)} row(s) to merge, {len(skipped)} skipped.")
    if dry:
        print("(--dry-run: nothing written.)")
        for r in add:
            print(f"  would add {r.get('paper_id')}  {(r.get('title') or '')[:50]}")
        return 0
    if not add:
        print("Nothing to merge.")
        return 1

    # 1) CSV — append in the dataset's exact column order (stdlib)
    with open(CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=main_cols)
        for r in add:
            w.writerow(r)

    # 2) XLSX — best effort (needs openpyxl)
    xlsx_note = ""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(XLSX)
        ws = wb["availability"]
        xcols = [c.value for c in ws[1]]
        for r in add:
            ws.append([r.get(c, "") for c in xcols])
        wb.save(XLSX)
        xlsx_note = f" and {os.path.basename(XLSX)}"
    except ImportError:
        xlsx_note = " (xlsx NOT updated — run `pip install openpyxl` to sync it, or regenerate)"
    except Exception as e:
        xlsx_note = f" (xlsx update failed: {type(e).__name__}: {e})"

    print(f"Merged {len(add)} article(s) into {os.path.basename(CSV)}{xlsx_note}.")
    print("Verify: python3 pipeline/reproduce_table.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
