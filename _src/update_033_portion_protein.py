#!/usr/bin/env python3
"""Editorial review, lote 2: portions and protein.

- When a "Small-portion tip" suggests a reduced portion (half a portion, half a fillet,
  one wrap instead of two...), state the approximate protein of that smaller amount.
  The value is computed from the recipe's own per-serving protein (halved and rounded);
  nothing is invented. Recipes whose protein cannot be read are listed, not changed.
- Muffins and protein bites: add a pairing tip with a defined amount of yogurt or milk,
  using the site's own reference values (1/2 cup nonfat Greek yogurt ~11 g,
  1 cup milk ~8 g), so it is clear they are lighter options.
- Prints every Small-portion tip so the remaining ones can be reviewed.

Nothing is saved if recipes.json cannot be read. Safe to re-run.
"""
import json, os, re, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)

REDUCED = re.compile(r'\b(half|one wrap|one piece|one pepper)\b', re.I)
YOGURT_HALF_CUP = 11   # 1/2 cup plain nonfat Greek yogurt (site reference: 3/4 cup ~17 g)
MILK_CUP = 8           # 1 cup milk (site reference: 7 to 8 g)


def protein_of(r):
    n = r.get('nutrition')
    if isinstance(n, dict):
        for k, v in n.items():
            if 'protein' in str(k).lower():
                m = re.search(r'\d+(?:\.\d+)?', str(v))
                if m:
                    return float(m.group())
    return None


def dump(raw, data):
    m = re.match(r'[\[{]\s*\n([ \t]+)', raw)
    with open(P('recipes.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')


raw = open(P('recipes.json'), encoding='utf-8').read()
try:
    recipes = json.loads(raw)
except Exception as e:
    print(f'ERROR: could not read recipes.json ({e}). Nothing was saved.')
    sys.exit(1)

changed, skipped, review = [], [], []

for r in recipes:
    rid = r.get('id', '?')
    p = protein_of(r)
    tips = r.get('tips') or []
    for i, t in enumerate(tips):
        if not isinstance(t, str) or not t.lower().startswith('small-portion tip'):
            continue
        if re.search(r'\d+\s*g protein', t):
            review.append(f'{rid}: {t}  [already has protein]')
            continue
        if REDUCED.search(t):
            if p is None:
                skipped.append(f'{rid}: protein per serving not found; tip left as is')
                continue
            half = round(p / 2)
            tips[i] = t.rstrip() + f' That smaller amount has about {half} g protein (the full serving has about {round(p)} g).'
            changed.append(f'{rid}: half portion about {half} g (full {round(p)} g)')
        else:
            review.append(f'{rid}: {t}')

    # Pairing tips for lighter options.
    if rid == 'berry-greek-yogurt-muffins' and p is not None:
        if not any('Greek yogurt for about' in str(t) for t in tips):
            tips.append(f'For a breakfast with more protein, pair one muffin with 1/2 cup plain nonfat Greek yogurt for about {round(p) + YOGURT_HALF_CUP} g protein in total.')
            changed.append(f'{rid}: pairing tip added ({round(p)} + {YOGURT_HALF_CUP} g)')
    if rid == 'peanut-butter-protein-bites' and p is not None:
        if not any('cup milk for about' in str(t) for t in tips):
            tips.append(f'These are a small snack, not a meal. Two bites with 1 cup milk come to about {round(2 * p) + MILK_CUP} g protein.')
            changed.append(f'{rid}: pairing tip added (2 x {round(p)} + {MILK_CUP} g)')
    r['tips'] = tips

dump(raw, recipes)

print('Portion protein (lote 2):')
print('\n'.join('- ' + c for c in changed) or '- nothing new to change (already applied)')
if skipped:
    print('Skipped:')
    print('\n'.join('- ' + s for s in skipped))
print('Other Small-portion tips (for manual review):')
print('\n'.join('- ' + x for x in review) or '- none')
print('Done.')
