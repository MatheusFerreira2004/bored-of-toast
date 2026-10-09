#!/usr/bin/env python3
"""Align the Nourished page (storefront.py) with the real PDFs.

Main guide 60 pages, 28-Day Meal Plan 9 pages (Weeks 1-4), Recipe Pack Vol. 2 14 pages,
Printable Pack 12 pages. Safe to re-run: changes already applied are skipped.
Run from the project root: python3 _src/fix_nourished_counts.py
"""
import os, sys

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storefront.py')
s = open(p, encoding='utf-8').read()

pairs = [
    ("a shopping list for each week.',26),", "a shopping list for each week.',9),"),
    ("side suggestions and substitutions.',18),", "side suggestions and substitutions.',14),"),
    ("Weeks 1-2 are in the main guide. Weeks 3-4 are in the 28-Day Meal Plan.",
     "Weeks 1-2 are in the main guide. The 28-Day Meal Plan brings all four weeks together, with a shopping list for each week."),
]

for old, new in pairs:
    if new in s:
        print(f'- already applied: {new[:70]}')
    elif s.count(old) == 1:
        s = s.replace(old, new)
        print(f'- OK: {new[:70]}')
    else:
        sys.exit(f'ERROR: text not found exactly once in storefront.py (nothing was saved):\n{old}')

open(p, 'w', encoding='utf-8').write(s)
print('storefront.py updated.')
