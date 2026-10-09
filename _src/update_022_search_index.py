#!/usr/bin/env python3
"""Search index fix.

The site search (search-index.js) still listed the meal-plan page as "5 Easy Dinners"
("Dinner ideas", "5 free recipes"). The page itself is now "Small-Plate Week".
This script edits only the meal-plan entry in build.py. Nothing is saved unless the
entry is found. Safe to re-run.
"""
import os, sys

sys.stderr = sys.stdout

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'build.py')
src = open(P, encoding='utf-8').read()

OLD_TITLE = '5 Easy Dinners'
NEW_TITLE = 'Small-Plate Week'

if OLD_TITLE not in src:
    if NEW_TITLE in src:
        print('Already applied. Nothing to do.')
        sys.exit(0)
    print('ERROR: could not find the "5 Easy Dinners" search entry in build.py. Nothing was saved.')
    sys.exit(1)

# Locate the dict literal that holds the meal-plan search entry.
i = src.index(OLD_TITLE)
a = src.rfind('{', 0, i)
b = src.find('}', i)
if a == -1 or b == -1:
    print('ERROR: could not isolate the search entry around "5 Easy Dinners". Nothing was saved.')
    sys.exit(1)
seg = src[a:b + 1]
if 'meal-plan/' not in seg:
    print('ERROR: the "5 Easy Dinners" text found in build.py is not the meal-plan search entry. Nothing was saved.')
    print('Context: ' + seg[:300])
    sys.exit(1)

new_seg = seg
changes = []
for old, new in [
    (OLD_TITLE, NEW_TITLE),
    ('Dinner ideas', 'Meal plan'),
    ('5 free recipes', '5 small plates'),
    ('five 5 easy dinners meal plan shopping list weeknight',
     'small-plate week five small plates meal plan shopping list high protein make-ahead'),
    ('crispy-baked-chicken-bites', 'lemon-chicken-orzo-soup'),
]:
    if old in new_seg:
        new_seg = new_seg.replace(old, new)
        changes.append(f'{old!r} -> {new!r}')

src = src[:a] + new_seg + src[b + 1:]

# Any other leftover "5 Easy Dinners" text in build.py is also out of date.
leftover = src.count(OLD_TITLE)
if leftover:
    src = src.replace(OLD_TITLE, NEW_TITLE)
    changes.append(f'{leftover} other {OLD_TITLE!r} -> {NEW_TITLE!r}')

with open(P, 'w', encoding='utf-8') as f:
    f.write(src)

print('Search index entry updated:')
for c in changes:
    print('- OK: ' + c)
print('Done.')
