#!/usr/bin/env python3
"""Small-Plate Week: status messages say "meals" instead of "dinners" (app.js).

Shown after "Add all 5 meals" / "Add this meal". Behavior is unchanged.
Nothing is saved unless every change is found. Safe to re-run.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'app.js')
s = open(p, encoding='utf-8').read()

CHANGES = [
    ("`${additions.length} dinner${additions.length === 1 ? '' : 's'} added. Open your shopping list below to review ingredients.`",
     "`${additions.length} meal${additions.length === 1 ? '' : 's'} added. Open your shopping list below to review ingredients.`"),
    ("'These dinners are already on your list. Your quantities and checked items have been kept.'",
     "'These meals are already on your list. Your quantities and checked items have been kept.'"),
]

if all(new in s for _, new in CHANGES):
    print('Already applied. Nothing to do.')
    sys.exit(0)
for old, new in CHANGES:
    if new in s:
        continue
    if s.count(old) != 1:
        sys.exit(f'ERROR: text not found exactly once in app.js (nothing was saved):\n{old}')
    s = s.replace(old, new)

open(p, 'w', encoding='utf-8').write(s)
print('OK: meal plan status messages now say "meals".')
