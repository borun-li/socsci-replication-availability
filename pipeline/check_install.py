#!/usr/bin/env python3
"""Confirm the repository is ready to use (Python 3 present + the dataset is in place).

Usage:
    python3 pipeline/check_install.py
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, os.pardir, "data", "socsci_availability.csv")


def main() -> int:
    if sys.version_info < (3, 0):
        print("Installation FAILED: Python 3 is required.")
        return 1
    if not os.path.exists(CSV):
        print(f"Installation FAILED: dataset not found at {CSV}")
        print("Make sure you are inside the cloned repository folder.")
        return 1
    with open(CSV, newline="", encoding="utf-8") as f:
        n = sum(1 for _ in csv.DictReader(f))
    print(f"Installation succeeded — Python {sys.version_info.major}.{sys.version_info.minor} OK, "
          f"dataset loaded ({n} articles). You're ready.")
    print("Next: python3 pipeline/lookup.py SS004")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
