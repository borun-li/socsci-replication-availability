#!/usr/bin/env python3
"""Look up a Sociological Science article's replication package by DOI or URL.

Usage:
    python3 pipeline/lookup.py <doi-or-url-or-fragment>

Examples:
    python3 pipeline/lookup.py 10.15195/v11.a17
    python3 pipeline/lookup.py sociologicalscience.com/articles-v11-17-467
    python3 pipeline/lookup.py SS510

Matches (case-insensitive substring) against the doi, article_url,
package_location, and paper_id columns of data/socsci_all_v3.csv, and prints
the coding for every matching article. Standard library only — no pip install.
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, os.pardir, "data", "socsci_all_v3.csv")

FIELDS = [
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


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    raw = " ".join(sys.argv[1:]).strip().lower()
    if not os.path.exists(CSV):
        print(f"ERROR: dataset not found at {CSV}", file=sys.stderr)
        return 2

    # normalise a pasted DOI: strip https://doi.org/ , doi.org/ , doi: prefixes
    doi_q = re.sub(r"^(https?://)?(dx\.)?doi\.org/|^doi:\s*", "", raw)

    with open(CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    def matches(r):
        # DOI and paper_id are identifiers → exact match (avoids v1.a2 hitting v1.a20)
        if (r.get("doi") or "").strip().lower() == doi_q:
            return True
        if (r.get("paper_id") or "").strip().lower() == raw:
            return True
        # URLs are pasted partially → substring
        return any(raw in (r.get(c) or "").lower()
                   for c in ("article_url", "package_location"))

    hits = [r for r in rows if matches(r)]

    if not hits:
        print(f'No article matched "{sys.argv[1]}".')
        print("Try a DOI (10.15195/v…), the article URL, or a paper id (SSNNN).")
        print("Note: only the 413 published Sociological Science articles "
              "(SS001–SS511) are covered by this dataset.")
        return 1

    for r in hits:
        print("=" * 72)
        for key, label in FIELDS:
            val = (r.get(key) or "").strip()
            if val:
                print(f"{label:>24} : {val}")
    print("=" * 72)
    print(f"{len(hits)} article(s) matched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
