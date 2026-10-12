#!/usr/bin/env python3
"""Editorial review, lote 5: filters and categories.

1. Recipe library chips: adds the card families that had no filter (Main Dishes, Salads,
   Desserts) and a new "Soft texture" filter. Chips with no recipes are not shown.
   The home category grid and the footer are unchanged.
2. Overlap without duplicates (filters match category OR tag, see app.js):
   - ginger-egg-drop-soup stays in Sips and gets the "Soups" tag.
   - cottage-cheese-mashed-potatoes moves from Main Dishes to "Side Dishes" (a card label,
     no new filter chip, so no near-empty filter).
3. Gentle vs Soft texture:
   - "soft" tag = smooth, spoonable or sippable texture (explicit list below).
   - "gentle" = mild flavor or a gentler swap listed. tzatziki-yogurt-dip loses "gentle"
     because it is served with crunchy vegetables.
   - A short note under the chips explains both and says neither is a guarantee.
Writes _src/reports/filters_review.md (counts per filter, gentle list for review).
Idempotent: a second run changes nothing.
"""
import json, os, re, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *n: os.path.join(HERE, *n)

SOFT = ['chicken-rice-congee', 'cottage-cheese-mashed-potatoes', 'ginger-egg-drop-soup', 'protein-rice-pudding',
        'greek-yogurt-chia-pudding', 'tomato-basil-soup', 'butternut-squash-soup', 'red-lentil-lemon-soup',
        'split-pea-soup', 'cottage-cheese-scrambled-eggs', 'chocolate-yogurt-mousse-cups', 'overnight-oats',
        'strawberry-protein-smoothie', 'banana-protein-smoothie', 'mixed-berry-protein-smoothie', 'golden-milk-latte']
GENTLE_REMOVE = ['tzatziki-yogurt-dip']
EXTRA_TAGS = {'ginger-egg-drop-soup': ['Soups']}
RECATEGORY = {'cottage-cheese-mashed-potatoes': ('Main Dishes', 'Side Dishes')}

raw = open(P('recipes.json'), encoding='utf-8').read()
try:
    recipes = json.loads(raw)
except Exception as ex:
    print(f'ERROR: could not read recipes.json ({ex}). Nothing was saved.')
    sys.exit(1)
by = {r['id']: r for r in recipes}
missing = [i for i in SOFT + GENTLE_REMOVE + list(EXTRA_TAGS) + list(RECATEGORY) if i not in by]
if missing:
    print(f'ERROR: recipes not found: {missing}. Nothing was saved.')
    sys.exit(1)

changes = []
for rid in SOFT:
    if 'soft' not in by[rid]['tags']:
        by[rid]['tags'].append('soft'); changes.append(f'{rid}: + soft')
for rid in GENTLE_REMOVE:
    if 'gentle' in by[rid]['tags']:
        by[rid]['tags'].remove('gentle'); changes.append(f'{rid}: - gentle (crunchy vegetables)')
for rid, tags in EXTRA_TAGS.items():
    for t in tags:
        if t not in by[rid]['tags']:
            by[rid]['tags'].append(t); changes.append(f'{rid}: + {t}')
for rid, (old, new) in RECATEGORY.items():
    if by[rid]['category'] == old:
        by[rid]['category'] = new; changes.append(f'{rid}: category {old} -> {new}')
    elif by[rid]['category'] != new:
        print(f'ERROR: {rid} category is {by[rid]["category"]!r}, expected {old!r} or {new!r}. Nothing was saved.')
        sys.exit(1)

if changes:
    m = re.match(r'[\[{]\s*\n([ \t]+)', raw)
    with open(P('recipes.json'), 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')

# ---- build.py: chips + note
b = open(P('build.py'), encoding='utf-8').read()
b0 = b
OLD = "    chips = [('all', 'All')] + [(k, l) for k, l, _ in CATS]\n"
NEW = ("    # update_038: library filters (home grid and footer still use CATS)\n"
       "    CHIP_ORDER = [('high-protein', 'High Protein'), ('gentle', 'Gentle'), ('soft', 'Soft texture'), ('make-ahead', 'Make-Ahead'),\n"
       "                  ('Beyond Toast', 'Beyond Toast'), ('Main Dishes', 'Main Dishes'), ('Soups', 'Soups'), ('Salads', 'Salads'),\n"
       "                  ('Sips', 'Sips'), ('Snacks', 'Snacks'), ('Desserts', 'Desserts')]\n"
       "    chips = [('all', 'All')] + [(k, l) for k, l in CHIP_ORDER if count(k) > 0]\n")
if 'CHIP_ORDER = [' in b:
    print('- already applied: library chips')
elif b.count(OLD) == 1:
    b = b.replace(OLD, NEW); print('- OK: library chips')
else:
    print('ERROR: chips line not found exactly once. Nothing was changed in build.py.')
    sys.exit(1)

NOTE = ('<p class="fine filter-note" style="margin:10px 0 0">Gentle: mild flavors, or a gentler swap is listed. '
        'Soft texture: smooth, spoonable or sippable. Neither is a guarantee that a food will suit you; '
        'follow your care team\\'s advice.</p>')
ANCHOR = "for k, l in diets)}</div>\n  </div>"
if 'filter-note' in b:
    print('- already applied: filter note')
elif b.count(ANCHOR) == 1:
    b = b.replace(ANCHOR, "for k, l in diets)}</div>\n    " + NOTE + "\n  </div>"); print('- OK: filter note')
else:
    print('ERROR: diet chips anchor not found exactly once. Nothing was changed in build.py.')
    sys.exit(1)
if b != b0:
    open(P('build.py'), 'w', encoding='utf-8').write(b)

# ---- report
cnt = lambda k: sum(1 for r in recipes if r['category'] == k or k in r['tags'])
keys = ['high-protein', 'gentle', 'soft', 'make-ahead', 'Beyond Toast', 'Main Dishes', 'Soups', 'Salads', 'Sips', 'Snacks', 'Desserts', 'Side Dishes']
out = ['# Filters review (lote 5)', '', '## Changed this run'] + (['- ' + c for c in changes] or ['- nothing (already applied)'])
out += ['', '## Recipes per filter'] + [f'- {k}: {cnt(k)}' for k in keys]
out += ['', '## Categories in use'] + [f'- {c}: {n}' for c, n in sorted({r["category"]: sum(1 for x in recipes if x["category"] == r["category"]) for r in recipes}.items())]
out += ['', '## Recipes tagged gentle (for manual review)'] + ['- ' + r['id'] for r in recipes if 'gentle' in r['tags']]
os.makedirs(P('reports'), exist_ok=True)
open(P('reports', 'filters_review.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
print('Done.')
