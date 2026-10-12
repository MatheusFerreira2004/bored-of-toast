#!/usr/bin/env python3
"""Review of PR #43 (lotes 3-6), requested after the review of 8f67f2f.

1. Gentle: written criterion = "selected recipes with milder flavors, or a clearly described
   mild variation". Every recipe has a "Make it gentler" section, so that section alone is not
   the criterion. Rule applied to the data: a gentle recipe that lists a heat or strong-smoke
   ingredient (HEAT below) keeps the tag only if its text tells the cook to skip/omit it.
   Otherwise the tag is removed. Nothing is added automatically.
2. Soft texture: note rewritten ("soft base or a clearly described soft variation; toppings
   and sides may differ"). Recipes in the soft filter that are served with crunchy toppings
   or sides get one explicit tip naming what to leave out (SOFT_TIPS).
3. Filter note under the chips rewritten for both labels; neither is presented as medical
   guidance, a texture-modified diet or a guarantee of tolerance.
4. Nourished page (storefront.py):
   - "The site: one recipe at a time" now acknowledges collections, Small-Plate Week and the
     shopping list instead of understating the free site.
   - The section's closing line becomes a positive "Choose Nourished when..." sentence;
     the honest "you do not need it" line stays only in the FAQ.
   - The FAQ answer also names the free tools.
   - "How buying works", while purchasing is closed, says the summary follows the current
     Terms and will be updated if a detail changes (vendor and support email not confirmed).
5. Search index: the Starter Kit entry used the label "Free guide"; it becomes "Free Starter Kit".

Writes _src/reports/review_040.md. Idempotent: a second run changes nothing.
Nothing is written to a file unless every anchor for that file is resolved.
"""
import json, os, re, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *n: os.path.join(HERE, *n)
report = ['# Review 040 (PR #43, lotes 3-6)', '']

# ------------------------------------------------------------------ recipes.json
HEAT = ['red pepper flakes', 'chili flakes', 'chili powder', 'cayenne', 'jalapeño', 'jalapeno',
        'hot sauce', 'chipotle', 'sriracha', 'smoked paprika']
SKIP_WORDS = r'(?:skip|leave out|leave off|omit|without|no)\b'
SOFT_TIPS = {
    'cottage-cheese-scrambled-eggs': 'Soft texture: serve the eggs on their own or with mashed avocado, and skip the toast and salad greens.',
    'greek-yogurt-chia-pudding': 'Soft texture: skip the sliced almonds and top with mashed or soft blueberries instead.',
    'overnight-oats': 'Soft texture: skip the almonds or walnuts and stir the blueberries in so they soften overnight.',
    'butternut-squash-soup': 'Soft texture: skip the toasted pepitas and finish with a swirl of yogurt instead.',
}

raw = open(P('recipes.json'), encoding='utf-8').read()
try:
    recipes = json.loads(raw)
except Exception as ex:
    print(f'ERROR: could not read recipes.json ({ex}). Nothing was saved.')
    sys.exit(1)
by = {r['id']: r for r in recipes}
missing = [i for i in SOFT_TIPS if i not in by]
if missing:
    print(f'ERROR: recipes not found: {missing}. Nothing was saved.')
    sys.exit(1)

changes, gentle_kept, gentle_removed = [], [], []
for r in recipes:
    if 'gentle' not in r.get('tags', []):
        continue
    ings = ' '.join(i.get('n', '') for g in r.get('ingredients', []) for i in g.get('items', [])).lower()
    rest = json.dumps({k: v for k, v in r.items() if k != 'ingredients'}, ensure_ascii=False).lower()
    hits = [w for w in HEAT if w in ings]
    if not hits:
        gentle_kept.append(f"{r['id']}: no heat or strong-smoke ingredient")
        continue
    described = all(re.search(SKIP_WORDS + r'[^.]{0,60}' + re.escape(w), rest) for w in hits)
    if described:
        gentle_kept.append(f"{r['id']}: lists {', '.join(hits)}, and the text says to skip it")
    else:
        r['tags'].remove('gentle')
        gentle_removed.append(f"{r['id']}: lists {', '.join(hits)} with no skip/omit instruction")
        changes.append(f"{r['id']}: - gentle")

soft_report = []
for rid, tip in SOFT_TIPS.items():
    r = by[rid]
    if 'soft' not in r.get('tags', []):
        soft_report.append(f'{rid}: not in the soft filter, tip not added')
        continue
    tips = r.setdefault('tips', [])
    if any(isinstance(t, str) and t.startswith('Soft texture:') for t in tips):
        soft_report.append(f'{rid}: soft-texture tip already present')
        continue
    tips.append(tip)
    changes.append(f'{rid}: + soft-texture tip')
    soft_report.append(f'{rid}: tip added')

if changes:
    m = re.match(r'[\[{]\s*\n([ \t]+)', raw)
    with open(P('recipes.json'), 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')


def apply(path, pairs, label):
    """pairs: (old, new). Each must be found once (old) or already applied (new present)."""
    s = open(path, encoding='utf-8').read()
    out = s
    for old, new in pairs:
        if new in out:
            report.append(f'- {label}: already applied: {new[:70]}...')
        elif out.count(old) == 1:
            out = out.replace(old, new)
            report.append(f'- {label}: OK: {new[:70]}...')
        else:
            print(f'ERROR: {label}: anchor found {out.count(old)} times (nothing saved in {os.path.basename(path)}):\n{old[:140]}')
            sys.exit(1)
    if out != s:
        open(path, 'w', encoding='utf-8').write(out)


# ------------------------------------------------------------------ build.py
OLD_NOTE = ('Gentle: mild flavors, or a gentler swap is listed. Soft texture: smooth, spoonable or sippable. '
            'Neither is a guarantee that a food will suit you; follow your care team\u2019s advice.')
NEW_NOTE = ('Gentle: selected recipes with milder flavors, or a clearly described mild variation. '
            'Soft texture: recipes with a soft base or a clearly described soft variation; toppings and sides may differ. '
            'These are cooking labels, not medical texture guidance or a guarantee that a food will suit you; '
            'follow your care team\u2019s advice.')
report += ['## build.py']
apply(P('build.py'), [(OLD_NOTE, NEW_NOTE)], 'filter note')

b = open(P('build.py'), encoding='utf-8').read()
n_free = b.count("'Free guide'") + b.count('"Free guide"')
if n_free:
    b = b.replace("'Free guide'", "'Free Starter Kit'").replace('"Free guide"', '"Free Starter Kit"')
    open(P('build.py'), 'w', encoding='utf-8').write(b)
    report.append(f'- search label: OK: "Free guide" -> "Free Starter Kit" ({n_free} occurrence(s))')
elif 'Free Starter Kit' in b:
    report.append('- search label: already applied (no "Free guide" left in build.py)')
else:
    print('ERROR: search label "Free guide" not found in build.py and no replacement present. Nothing saved.')
    sys.exit(1)

# ------------------------------------------------------------------ storefront.py
OLD_SITE = ('<h3>The site: one recipe at a time</h3><p>Our recipes, guides and collections are free to read, '
            'and they stay free. They work well when you want one idea for tonight.</p>')
NEW_SITE = ('<h3>The site: free to browse and plan</h3><p>Our recipes, guides, collections and the Small-Plate Week, '
            'with its shopping list, are free to use and they stay free. They work well when you like to browse '
            'and choose as you go.</p>')
OLD_CLOSE = ('If browsing the site already covers what you need, you do not need Nourished. '
             'Buying it does not unlock extra content on the site.')
NEW_CLOSE = ('Choose Nourished when you want recipes, weekly examples and shopping lists organized together '
             'in files you can keep and print. Buying it does not unlock extra content on the site.')
OLD_FAQ = ('The site recipes stay free and work one page at a time. Nourished organizes 36 numbered recipes with '
           'four weeks of meal examples, weekly shopping lists, prep notes and printable sheets in four PDFs. '
           'If browsing the site already covers what you need, you do not need it.')
NEW_FAQ = ('The site recipes, collections and Small-Plate Week stay free. Nourished gathers 36 numbered recipes, '
           'four weeks of meal examples that refer to them, weekly shopping lists, prep notes and printable sheets '
           'in four PDFs. If browsing the site already covers what you need, you do not need it.')
OLD_BUY = 'Purchasing is not open yet. This is how it will work when it opens, as set out in our Terms of Use.'
NEW_BUY = ('Purchasing is not open yet. This summary follows our current Terms of Use, and we will update it '
           'if any detail changes before purchasing opens.')
report += ['', '## storefront.py']
apply(P('storefront.py'), [(OLD_SITE, NEW_SITE), (OLD_CLOSE, NEW_CLOSE), (OLD_FAQ, NEW_FAQ), (OLD_BUY, NEW_BUY)], 'Nourished page')

# ------------------------------------------------------------------ report
report += ['', '## Recipe changes this run'] + (['- ' + c for c in changes] or ['- nothing (already applied)'])
report += ['', '## Gentle criterion',
           'Selected recipes with milder flavors, or a clearly described mild variation. A gentle recipe that lists',
           'a heat or strong-smoke ingredient (' + ', '.join(HEAT) + ') keeps the tag only if its text says to skip it.',
           '', '### Kept'] + ['- ' + x for x in gentle_kept]
report += ['', '### Removed this run'] + (['- ' + x for x in gentle_removed] or ['- none this run'])
report += ['', '## Soft texture tips'] + ['- ' + x for x in soft_report]
report += ['', '## Counts after this run',
           '- gentle: %d' % sum(1 for r in recipes if 'gentle' in r.get('tags', [])),
           '- soft: %d' % sum(1 for r in recipes if 'soft' in r.get('tags', []))]
report += ['', '## Pending (owner decision or files)',
           '- Payment vendor not confirmed; text mirrors the Terms (Lemon Squeezy).',
           '- hello@boredoftoast.com not set up yet (domain not bought).',
           '- Preview images still show old PDF text; needs the PDFs.',
           '- Chili photo: needs visual confirmation before any swap.']
os.makedirs(P('reports'), exist_ok=True)
open(P('reports', 'review_040.md'), 'w', encoding='utf-8').write('\n'.join(report) + '\n')
print('\n'.join(report))
print('Done.')
