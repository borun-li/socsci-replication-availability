#!/usr/bin/env python3
"""Reproduce the replication-package-availability table from the shipped dataset.

Usage:
    python3 pipeline/reproduce_table.py

Recomputes, from data/socsci_availability.csv, the same numbers reported in the README
and the professor email:
  - overall availability (data and/or code deposited) among in-scope articles,
  - availability by publication year,
  - the mandatory-policy effect (submitted before vs. on/after 2023-04-01).

Standard library only — no pip install. (This verifies the *published numbers*
from the coded dataset. Re-coding the articles from scratch is a separate,
Claude Code-driven step — see the README "From scratch" section.)
"""
import csv
import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, os.pardir, "data", "socsci_availability.csv")
POLICY = datetime.date(2023, 4, 1)


def parse_date(s):
    s = (s or "").strip()
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    return datetime.date(*map(int, m.groups())) if m else None


def available(r):
    return str(r.get("data")) == "Y" or str(r.get("code")) == "Y"


def pct(a, n):
    return f"{a}/{n} = {a / n * 100:5.1f}%" if n else "n/a"


def main() -> int:
    if not os.path.exists(CSV):
        print(f"ERROR: dataset not found at {CSV}", file=sys.stderr)
        return 2
    with open(CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    insc = [r for r in rows if r.get("in_scope") == "Y"]
    avail = [r for r in insc if available(r)]

    print("Sociological Science — replication-package availability")
    print(f"(recomputed from {os.path.basename(CSV)}: {len(rows)} articles total)\n")
    print(f"In-scope empirical articles : {len(insc)}")
    print(f"Overall availability        : {pct(len(avail), len(insc))}")
    print(f"  data deposited={sum(1 for r in insc if str(r.get('data'))=='Y')}"
          f"  code deposited={sum(1 for r in insc if str(r.get('code'))=='Y')}"
          f"  data access-gated={sum(1 for r in insc if str(r.get('data_gated'))=='Y')}")

    print("\nAvailability by publication year")
    for yr in range(2014, 2027):
        grp = [r for r in insc if str(r.get("published_date")).startswith(str(yr))]
        if grp:
            print(f"  {yr}: {pct(len([r for r in grp if available(r)]), len(grp))}")

    print("\nMandatory-reproducibility policy effect (by submission date vs 2023-04-01)")
    pre = [r for r in insc if (d := parse_date(r.get("submission_date"))) and d < POLICY]
    post = [r for r in insc if (d := parse_date(r.get("submission_date"))) and d >= POLICY]
    print(f"  submitted BEFORE 2023-04-01   : {pct(len([r for r in pre if available(r)]), len(pre))}")
    print(f"  submitted ON/AFTER 2023-04-01 : {pct(len([r for r in post if available(r)]), len(post))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
