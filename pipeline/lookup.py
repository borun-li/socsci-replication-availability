#!/usr/bin/env python3
"""Look up Sociological Science articles' replication packages by DOI / URL / paper id.

Usage:
    python3 pipeline/lookup.py <query> [<query> ...]    # one or more ids / DOIs / URLs
    python3 pipeline/lookup.py --file ids.txt           # one query per line (# = comment)
    python3 pipeline/lookup.py --detail <query> ...     # full per-field view (with notes)

Examples:
    python3 pipeline/lookup.py SS004 SS510 10.15195/v1.a2
    python3 pipeline/lookup.py --file my_ids.txt
    python3 pipeline/lookup.py https://sociologicalscience.com/articles-v11-17-467/

DOI and paper_id match exactly (case-insensitive; a pasted doi.org/ or doi: prefix is
stripped); article_url and package_location match by substring. Default output is a compact
one-line-per-article table; --detail prints every field including the coding notes. Reads
data/socsci_availability.csv — standard library only, no pip install.
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, os.pardir, "data", "socsci_availability.csv")

DETAIL_FIELDS = [
    ("paper_id", "Paper"),
    ("title", "Title"),
    ("authors", "Authors"),
    ("doi", "DOI"),
    ("article_url", "Article URL"),
    ("in_scope", "In scope"),
    ("data", "Data deposited"),
    ("code", "Code deposited"),
    ("data_gated", "Data access-gated"),
    ("data_source_apply_at", "How to obtain gated data"),
    ("package_location", "Replication package"),
    ("notes", "Notes"),
]


def norm_doi(q):
    return re.sub(r"^(https?://)?(dx\.)?doi\.org/|^doi:\s*", "", q)


def find(rows, query):
    """Return every article matching one query (DOI/id exact, URL substring)."""
    raw = query.strip().lower()
    if not raw:
        return []
    doi_q = norm_doi(raw)
    out = []
    for r in rows:
        if (r.get("doi") or "").strip().lower() == doi_q:
            out.append(r)
        elif (r.get("paper_id") or "").strip().lower() == raw:
            out.append(r)
        elif any(raw in (r.get(c) or "").lower()
                 for c in ("article_url", "package_location")):
            out.append(r)
    return out


def route(r):
    """The 'package / how to obtain' cell for the compact table."""
    pkg = (r.get("package_location") or "").strip()
    if pkg:
        return pkg
    if str(r.get("data_gated")) == "Y":
        ap = (r.get("data_source_apply_at") or "").strip()
        return "[gated] " + (ap or "restricted — see --detail notes")
    return "—"


def print_compact(hits):
    hdr = f'{"paper":<7} {"scope":<5} {"data":<4} {"code":<4} {"gate":<4}  package / how to obtain'
    print(hdr)
    print("-" * 88)
    for r in hits:
        rt = route(r)
        if len(rt) > 66:
            rt = rt[:63] + "..."
        print(f'{r.get("paper_id") or "":<7} {r.get("in_scope") or "":<5} '
              f'{r.get("data") or "":<4} {r.get("code") or "":<4} '
              f'{r.get("data_gated") or "":<4}  {rt}')


def print_detail(hits):
    for r in hits:
        print("=" * 72)
        for key, label in DETAIL_FIELDS:
            val = (r.get(key) or "").strip()
            if val:
                print(f"{label:>24} : {val}")
    print("=" * 72)


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    detail = False
    queries = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--detail", "-v"):
            detail = True
        elif a in ("--file", "-f"):
            i += 1
            if i >= len(args):
                print("ERROR: --file needs a path", file=sys.stderr)
                return 2
            path = args[i]
            if not os.path.exists(path):
                print(f"ERROR: file not found: {path}", file=sys.stderr)
                return 2
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        queries.append(line)
        else:
            queries.append(a)
        i += 1

    if not queries:
        print("No queries given. Try: lookup.py SS004 SS510   or   lookup.py --file ids.txt")
        return 1
    if not os.path.exists(CSV):
        print(f"ERROR: dataset not found at {CSV}", file=sys.stderr)
        return 2

    with open(CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    seen, hits, unmatched = set(), [], []
    for q in queries:
        found = find(rows, q)
        if not found:
            unmatched.append(q)
            continue
        for r in found:
            pid = r.get("paper_id")
            if pid not in seen:
                seen.add(pid)
                hits.append(r)

    if hits:
        (print_detail if detail else print_compact)(hits)

    print()
    print(f"{len(hits)} article(s) found from {len(queries)} query(ies).")
    if unmatched:
        print(f"{len(unmatched)} not matched: " + ", ".join(unmatched))
        print("  (only the 413 published articles SS001–SS511 are covered; "
              "check the DOI / URL / paper id.)")
    return 0 if hits else 1


if __name__ == "__main__":
    raise SystemExit(main())
