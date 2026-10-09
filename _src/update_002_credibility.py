#!/usr/bin/env python3
"""Batch 1 (credibility): Terms page, "Fall" leftovers, marquee.

- Terms: remove "We test our recipes" and the visible "About this page / general template" section.
- Home: "Fall favorites" section becomes "Make-ahead for harder days" (make-ahead recipes).
- Recipes page: remove the "Fall" filter chip.
- Recipe pages: eyebrow shows "Small Plates" instead of "Fall".
- Marquee: remove "No-cook" and "Freezer-friendly" (no such categories exist).

Nothing is saved unless every change is found. Safe to re-run.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)

# ------------------------------------------------------------------ build.py
b = open(P('build.py'), encoding='utf-8').read()
BUILD = [
    ("chips = [('all', 'All')] + [(k, l) for k, l, _ in CATS] + [('fall', 'Fall')]",
     "chips = [('all', 'All')] + [(k, l) for k, l, _ in CATS]"),
    ("fall = [r for r in RECIPES if 'fall' in r['tags']][:4]",
     "fall = [r for r in RECIPES if 'make-ahead' in r['tags']][:4]"),
    ("section_head('Fall favorites <span class=\"season-leaf\">' + ICON['leaf'] + '</span>', 'Cozy, golden and made for sweater weather.', f'<a href=\"{root}recipes/?cat=fall\" class=\"view-all\">All fall recipes →</a>')",
     "section_head('Make-ahead for <em>harder days</em>', 'Cook once on a good day, then reheat a small portion when you need it.', f'<a href=\"{root}recipes/?cat=make-ahead\" class=\"view-all\">All make-ahead recipes →</a>')"),
    ("['High protein', 'Small portions', 'Cold & gentle', 'Make-ahead', 'No-cook', 'Freezer-friendly']",
     "['High protein', 'Small portions', 'Gentle swaps', 'Make-ahead', 'Protein first', 'Small and often']"),
    ("(['Fall'] if 'fall' in r['tags'] else [])",
     "(['Small Plates'] if 'small-plates' in r['tags'] else [])"),
]
print('build.py:')
for old, new in BUILD:
    if new in b:
        print(f'- already applied: {new[:70]}')
    elif b.count(old) == 1:
        b = b.replace(old, new)
        print(f'- OK: {new[:70]}')
    else:
        sys.exit(f'ERROR: not found exactly once in build.py (nothing was saved):\n{old}')

# ------------------------------------------------------------------ Terms (guides_legal.json)
gl = json.load(open(P('guides_legal.json'), encoding='utf-8'))
terms = gl['terms']
OLD_TEST = 'We test our recipes and do our best to make them clear and reliable, but results depend on your ingredients, equipment, altitude, and technique.'
NEW_TEST = 'We do our best to make our recipes clear and reliable, but results depend on your ingredients, equipment, altitude, and technique.'
print('\nTerms:')
found = False
for s in terms['sections']:
    for i, p in enumerate(s['p']):
        if OLD_TEST in p:
            s['p'][i] = p.replace(OLD_TEST, NEW_TEST)
            found = True
        elif NEW_TEST in p:
            found = True
if not found:
    sys.exit('ERROR: "We test our recipes" sentence not found in the Terms (nothing was saved).')
print('- OK: "We test our recipes" removed')
before = len(terms['sections'])
terms['sections'] = [s for s in terms['sections'] if s['h'] != 'About this page']
print('- OK: "About this page" section removed' if len(terms['sections']) < before else '- already applied: "About this page" section removed')
terms['updated'] = 'October 9, 2026'

# ------------------------------------------------------------------ save
open(P('build.py'), 'w', encoding='utf-8').write(b)
with open(P('guides_legal.json'), 'w', encoding='utf-8') as f:
    json.dump(gl, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('\nDone.')
