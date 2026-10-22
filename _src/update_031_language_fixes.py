#!/usr/bin/env python3
"""Editorial review, lote 1.

- Removes wording that reads like a guarantee of food sufficiency
  ("complete small meal", "counts as a small meal", "simple minimum").
- Guide fixes: Protein First wording, no clinical time thresholds in
  "When to Ask for Help", smoothie guide title (slug unchanged), natural US English.
- Nourished: preview caption and alt text mark the weekly page as an illustrative,
  adaptable example; totals describe the example only.
- Writes a scan report of remaining risky phrases to _src/reports/031_scan.txt
  (report only, nothing is changed by the scan).

Nothing is saved unless every required phrase is found (or already replaced).
Safe to re-run.

Later scripts may rewrite a text that this script set. FINAL_VERSIONS lists those
later versions, so this script treats them as "already applied" and never restores
an earlier wording. Example: the congee tip set here ("start with a 3/4-cup bowl...")
is rewritten by update_033 to "start with a smaller bowl..." (no unconfirmed volume).

Sales page: the revised Nourished page (commit 3682e0c) rewrote the preview section.
A storefront phrase that is no longer on the page in either its old or new wording is
reported as "superseded" instead of stopping the build. If the old wording ever comes
back, it is still replaced.
"""
import json, os, re, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)

CONGEE_OLD = 'Small-portion tip: a 3/4-cup bowl with half an egg is a complete small meal.'

RECIPE_FIXES = [
    (CONGEE_OLD,
     'Small-portion tip: start with a 3/4-cup bowl topped with half an egg. It is soft and easy to eat in small spoonfuls; add the other half of the egg if you want more.'),
    ('and this version quietly carries a good amount of protein.',
     'and this version adds finely shredded chicken and a soft egg.'),
    ('It counts as a small meal on nights when dinner does not happen.',
     'Made with ultra-filtered milk, it is mild, lightly sweet and easy to sip slowly.'),
    ('Small-portion tip: a 1/2-cup scoop next to a few bites of protein is a complete small plate.',
     'Small-portion tip: serve a 1/2-cup scoop on its own, or next to a few bites of salmon, chicken or turkey meatballs.'),
    ('and this one does more nutritional work than most.',
     'and blending in cottage cheese gives this one about three times the protein of a plain mash.'),
]

# Later, final versions written by other scripts. If one of these is present,
# the fix counts as applied and nothing is rewritten.
FINAL_VERSIONS = {
    CONGEE_OLD: (
        'Small-portion tip: start with a smaller bowl topped with half an egg.',  # update_033
    ),
}

GUIDE_FIXES = [
    ('helps make sure the part your body needs most does not get left on the plate.',
     'makes it less likely that the protein is left on the plate when fullness arrives early. The rest of the meal still matters; this is only about the order.'),
    ('If you are struggling to eat or drink for more than a day or two, talk to your care team.',
     'If eating or drinking feels hard, or you are worried about how you feel, talk to your care team.'),
    ('You cannot keep food or fluids down for more than a day.',
     'You are having trouble keeping food or fluids down.'),
    ('You have been eating very little for several days in a row.',
     'You are eating much less than usual and feel worried about it.'),
    ('A dessert plate or a mug makes a small portion look like a complete meal.',
     'A dessert plate or a mug makes a small portion look less daunting.'),
    ('Smoothies That Actually Fill You', 'Small Smoothies with Protein'),
    ('sweet, big and not very filling.', 'sweet, big and low in protein.'),
    ('eating past comfortable.', 'eating more than feels comfortable.'),
    ('Appetizers, half portions and sides can make a perfect small meal.',
     'Appetizers, half portions and sides are often the right size.'),
    ('A protein side plus a vegetable side makes a balanced small plate.',
     'A protein side plus a vegetable side makes an easy small plate.'),
    ('or a couple of appetizers, can make a fine meal.',
     'or a couple of appetizers, can work well.'),
    ('They can be a practical option on harder days. If you rely on them often',
     'A smoothie is one easy option on harder days, not a replacement for varied meals. If you rely on them often'),
    ('one 4 oz piece of fish is a full plate.',
     'one 4 oz piece of fish is a good place to start.'),
]

STORE_FIXES = [
    ('Gentle options and a simple minimum for low-appetite days, organized so you can find something quickly.',
     'Gentle options and a short list of easy cooking ideas for low-appetite days, organized so you can find something quickly.'),
    ('A real Week 1 daily meal example from Nourished',
     'An illustrative Week 1 meal example page from Nourished'),
    ('Meal examples connected to recipe numbers, shopping and preparation pages.',
     'Illustrative meal examples to adapt, linked to recipe numbers, shopping and preparation pages. Any daily totals shown describe that example only, not a target for you.'),
]

# Optional: same title may appear hard-coded elsewhere.
OPTIONAL_RAW = [('Smoothies That Actually Fill You', 'Small Smoothies with Protein')]


def walk(obj, fn, path=''):
    if isinstance(obj, dict):
        return {k: walk(v, fn, f'{path}.{k}') for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v, fn, f'{path}[{i}]') for i, v in enumerate(obj)]
    if isinstance(obj, str):
        return fn(obj, path)
    return obj


def apply_json(name, fixes, report):
    raw = open(P(name), encoding='utf-8').read()
    data = json.loads(raw)
    counts = {old: 0 for old, _ in fixes}
    done = {old: False for old, _ in fixes}
    final = {old: False for old, _ in fixes}

    def fn(s, path):
        for old, new in fixes:
            if old in s:
                s = s.replace(old, new)
                counts[old] += 1
            elif new in s:
                done[old] = True
            elif any(f in s for f in FINAL_VERSIONS.get(old, ())):
                done[old] = True
                final[old] = True
        return s

    data = walk(data, fn)
    missing = [old for old in counts if counts[old] == 0 and not done[old]]
    for old, new in fixes:
        if counts[old]:
            report.append(f'- OK ({name}, {counts[old]}x): {old[:70]}')
        elif final[old]:
            report.append(f'- already applied, final version from a later script ({name}): {old[:70]}')
        elif done[old]:
            report.append(f'- already applied ({name}): {old[:70]}')
    return raw, data, missing


def dump(name, raw, data):
    m = re.match(r'[\[{]\s*\n([ \t]+)', raw)
    with open(P(name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')


report = []
r_raw, r_data, r_missing = apply_json('recipes.json', RECIPE_FIXES, report)
g_raw, g_data, g_missing = apply_json('guides_legal.json', GUIDE_FIXES, report)

store = open(P('storefront.py'), encoding='utf-8').read()
s_missing = []
for old, new in STORE_FIXES:
    if old in store:
        store = store.replace(old, new)
        report.append(f'- OK (storefront.py): {old[:70]}')
    elif (new in store or (old == STORE_FIXES[0][0] and 'Sips, spoon foods and soft bites to help you choose what to make.' in store)):
        report.append(f'- already applied (storefront.py): {old[:70]}')
    else:
        # Neither wording is on the page: the revised sales page removed this text.
        report.append(f'- superseded (storefront.py, text no longer on the page): {old[:70]}')

missing = r_missing + g_missing + s_missing
if missing:
    print('ERROR: these phrases were not found. Nothing was saved.')
    for m_ in missing:
        print('  - ' + m_)
    sys.exit(1)

build = open(P('build.py'), encoding='utf-8').read()
for old, new in OPTIONAL_RAW:
    n = build.count(old)
    if n:
        build = build.replace(old, new)
        report.append(f'- OK (build.py, {n}x, optional): {old}')

dump('recipes.json', r_raw, r_data)
dump('guides_legal.json', g_raw, g_data)
open(P('storefront.py'), 'w', encoding='utf-8').write(store)
open(P('build.py'), 'w', encoding='utf-8').write(build)

# ---- Scan report (read-only) ----
RISKY = re.compile(r'(complete (small )?(meal|plate)|counts as a (small )?meal|\benough\b|\bminimum\b|full meal|full plate|'
                   r'meal replacement|replace(ment)? (for )?meals?|fill(s|ing)? you|\bfilling\b|perfect small|'
                   r'quietly|nutritional work|tested|evidence-based)', re.I)
lines = []


def scan(obj, where, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            scan(v, where, f'{path}.{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan(v, where, f'{path}[{i}]')
    elif isinstance(obj, str) and RISKY.search(obj):
        for sent in re.split(r'(?<=[.!?])\s+', obj):
            if RISKY.search(sent):
                lines.append(f'{where}{path}: {sent.strip()}')


for r in r_data:
    scan(r, f"recipe:{r.get('id')}")
scan(g_data.get('guides', []), 'guides')
for fname, text in (('storefront.py', store), ('build.py', build)):
    for i, ln in enumerate(text.splitlines(), 1):
        for mm in RISKY.finditer(ln):
            a, b = max(0, mm.start() - 80), mm.end() + 80
            lines.append(f'{fname}:{i}: ...{ln[a:b].strip()}...')

os.makedirs(P('reports'), exist_ok=True)
with open(P(os.path.join('reports', '031_scan.txt')), 'w', encoding='utf-8') as f:
    f.write('Remaining phrases to review (report only, not changed):\n')
    f.write('\n'.join(lines) + '\n')

print('Language fixes:')
print('\n'.join(report))
print(f'Scan report: {len(lines)} lines written to _src/reports/031_scan.txt')
print('Done.')
