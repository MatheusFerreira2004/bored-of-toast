#!/usr/bin/env python3
""""You might also like": suggest focus recipes (small-plates tag) first, then same category.

Before: same category first, then fall recipes. So a breakfast could suggest pancakes and French
toast, and a main could suggest creamy pasta and tacos.
After: small-plates recipes first, then same category. Every recipe page suggests focus recipes.

Nothing is saved unless the change is found. Safe to re-run.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'build.py')
b = open(p, encoding='utf-8').read()

OLD = "related = sorted([x for x in RECIPES if x['id'] != r['id']], key=lambda x: (x['category'] != r['category'], 'fall' not in x['tags'] if 'fall' in r['tags'] else 0))[:3]"
NEW = "related = sorted([x for x in RECIPES if x['id'] != r['id']], key=lambda x: ('small-plates' not in x['tags'], x['category'] != r['category']))[:3]"

if NEW in b:
    print('Already applied. Nothing to do.')
    sys.exit(0)
if b.count(OLD) != 1:
    sys.exit('ERROR: related-recipes line not found exactly once in build.py (nothing was saved).')
open(p, 'w', encoding='utf-8').write(b.replace(OLD, NEW))
print('OK: "You might also like" now suggests small-plates recipes first.')
