#!/usr/bin/env python3
"""Add a new Sociological Science article to a coding worklist by URL or DOI.

Give it an article URL or DOI; it fetches the bibliographic metadata and appends a new row with
**Block A filled in automatically** (doi, paper_id, title, authors, published_date, article_url)
and Block B (the coding columns) left empty — ready for the Scenario 2 / 3 coding step.

Usage:
    python3 pipeline/add_article.py <url-or-doi> [<url-or-doi> ...]
    python3 pipeline/add_article.py --out data/new_articles.csv <url-or-doi> ...

Examples:
    python3 pipeline/add_article.py https://sociologicalscience.com/articles-v11-17-467/
    python3 pipeline/add_article.py 10.15195/v11.a17

Block A is read from the article page's citation meta tags (title, authors, date, DOI); a DOI
input is resolved to its page via Crossref first. `paper_id` is auto-assigned as the next SSNNN
after the current dataset. `submission_date` is left blank (it is not in the metadata — the
coding step fills it from the article's "Received" date). Needs an internet connection; standard
library only, no pip install.
"""
import csv
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, os.pardir, "data")
DATASET = os.path.join(DATA, "socsci_availability.csv")
UA = {"User-Agent": "socsci-availability/1.0 (mailto:liborun0811@gmail.com)"}

BLOCK_A = ["doi", "paper_id", "title", "authors", "published_date", "submission_date", "article_url"]
BLOCK_B = ["in_scope", "qualitative", "data", "code", "data_and_code", "neither", "data_gated",
           "data_source_apply_at", "package_location", "path_to_package", "coverage_checked", "notes"]
COLS = BLOCK_A + BLOCK_B


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30
                                  ).read().decode("utf-8", "ignore")


def doi_to_url(doi):
    """Resolve a DOI to its SocSci article page via Crossref."""
    import json
    m = json.loads(get(f"https://api.crossref.org/works/{doi}"))["message"]
    return ((m.get("resource") or {}).get("primary") or {}).get("URL", "")


def flip_name(name):
    """'Breen, Richard' -> 'Richard Breen'; leave 'Given Family' as-is."""
    name = name.strip()
    if "," in name:
        fam, _, giv = name.partition(",")
        return f"{giv.strip()} {fam.strip()}".strip()
    return name


def block_a_from_page(url):
    """Parse Block A from a SocSci article page's citation_* meta tags."""
    html = get(url)

    def meta(key):
        return re.findall(rf'<meta[^>]+name="{key}"[^>]+content="([^"]*)"', html)

    title = (meta("citation_title") or [""])[0].strip()
    authors = ", ".join(flip_name(a) for a in meta("citation_author") if a.strip())
    date = (meta("citation_publication_date") or meta("citation_online_date") or [""])[0].strip()
    date = date.replace("/", "-")  # 2024/04/29 -> 2024-04-29
    doi = (meta("citation_doi") or [""])[0].strip()
    return {"title": title, "authors": authors, "published_date": date, "doi": doi,
            "article_url": url}


def next_paper_id(existing_ids):
    nums = [int(m.group(1)) for pid in existing_ids
            if (m := re.match(r"SS0*(\d+)$", (pid or "").strip()))]
    return f"SS{(max(nums) + 1) if nums else 1:03d}"


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    out = os.path.join(DATA, "new_articles.csv")
    inputs = []
    i = 0
    while i < len(args):
        if args[i] in ("--out", "-o"):
            i += 1
            if i >= len(args):
                print("ERROR: --out needs a path", file=sys.stderr)
                return 2
            out = args[i]
        else:
            inputs.append(args[i])
        i += 1

    # collect existing paper_ids from the dataset + any current worklist (for unique SSNNN)
    existing = []
    for path in (DATASET, out):
        if os.path.exists(path):
            with open(path, newline="", encoding="utf-8") as f:
                existing += [r.get("paper_id", "") for r in csv.DictReader(f)]

    new_rows = []
    for q in inputs:
        q = q.strip()
        try:
            url = q if q.lower().startswith("http") else doi_to_url(q)
            if not url:
                print(f"  SKIP {q}: could not resolve to an article page")
                continue
            a = block_a_from_page(url)
            if not a["title"]:
                print(f"  SKIP {q}: no citation metadata found on the page")
                continue
            pid = next_paper_id(existing + [r["paper_id"] for r in new_rows])
            row = {c: "" for c in COLS}
            row.update({"paper_id": pid, **a})
            new_rows.append(row)
            print(f"  {pid}  {a['title'][:55]}  ({a['doi'] or 'no DOI'})")
        except Exception as e:
            print(f"  SKIP {q}: {type(e).__name__}: {e}")

    if not new_rows:
        print("Nothing added.")
        return 1

    write_header = not os.path.exists(out) or os.path.getsize(out) == 0
    with open(out, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if write_header:
            w.writeheader()
        for r in new_rows:
            w.writerow(r)
    print(f"\nAdded {len(new_rows)} article(s) to {out} — Block A filled, coding columns empty.")
    print("Next: code Block B — open Claude Code and follow README Scenario 3, Step 2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
