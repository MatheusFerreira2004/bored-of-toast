#!/usr/bin/env python3
"""Editorial review, lote 1c: remaining food-sufficiency wording.

The second pass of the review found three more phrases that read like a promise that a portion
is enough ("complete breakfast", "full breakfast", "perfectly good start"). They are replaced with
culinary descriptions. A read-only scan of the whole recipes.json and guides_legal.json for similar
wording is written to _src/reports/034_scan.txt (nothing is changed by the scan; culinary uses
such as "enough water to cover" are not flagged).

Phrases that are neither found nor already replaced are reported, not invented. Safe to re-run.
"""
import json, os, re, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *n: os.path.join(HERE, *n)

FIXES = [
    # avocado-toast-jammy-eggs, "why" card
    ('A small, complete breakfast instead of two heavy slices.',
     'A small breakfast instead of two heavy slices.'),
    # overnight-oats, kitchen note
    ('each one is a full breakfast you can actually finish.',
     'each jar is a smaller breakfast that is easier to finish.'),
    # breakfast-burritos, kitchen note
    ('half a burrito and a cup of tea is a perfectly good start.',
     'half a burrito and a cup of tea is an easy way to start.'),
]
SCAN = re.compile(r'\b(complete|full)\s+(small\s+)?(breakfast|lunch|dinner|meal|plate|dessert|snack)\b|'
                  r'perfectly (good|fine)|still counts|counts as|counts toward|\bminimum\b|'
                  r'meal replacement|replace(s|ment)? (for )?(a )?meals?', re.I)


def walk(obj, fn):
    if isinstance(obj, dict):
        return {k: walk(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v, fn) for v in obj]
    return fn(obj) if isinstance(obj, str) else obj


raw = open(P('recipes.json'), encoding='utf-8').read()
try:
    recipes = json.loads(raw)
except Exception as e:
    print(f'ERROR: could not read recipes.json ({e}). Nothing was saved.')
    sys.exit(1)

hit = {o: 0 for o, _ in FIXES}
done = {o: False for o, _ in FIXES}


def fix(s):
    for o, n in FIXES:
        if o in s:
            s = s.replace(o, n); hit[o] += 1
        elif n in s:
            done[o] = True
    return s


recipes = walk(recipes, fix)
report = []
for o, _ in FIXES:
    if hit[o]:
        report.append(f'- OK: {o}')
    elif done[o]:
        report.append(f'- already applied: {o}')
    else:
        report.append(f'- NOT FOUND (left for manual review): {o}')

if any(hit.values()):
    m = re.match(r'[\[{]\s*\n([ \t]+)', raw)
    with open(P('recipes.json'), 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')

# read-only scan
lines = []
for r in recipes:
    rid = r.get('id', '?')
    def sc(s, rid=rid):
        for mm in SCAN.finditer(s):
            lines.append(f'recipe:{rid}: ...{s[max(0, mm.start() - 60): mm.end() + 60]}...')
        return s
    walk(r, sc)
try:
    guides = json.load(open(P('guides_legal.json'), encoding='utf-8'))
    def sg(s):
        for mm in SCAN.finditer(s):
            lines.append(f'guides_legal: ...{s[max(0, mm.start() - 60): mm.end() + 60]}...')
        return s
    walk(guides, sg)
except Exception as e:
    lines.append(f'(guides_legal.json not scanned: {e})')

os.makedirs(P('reports'), exist_ok=True)
with open(P('reports', '034_scan.txt'), 'w', encoding='utf-8') as f:
    f.write('Remaining sufficiency-style wording (report only, not changed):\n')
    f.write('\n'.join(lines) + '\n' if lines else '- none\n')

print('Language fixes (3):')
print('\n'.join(report))
print(f'Scan: {len(lines)} line(s) in _src/reports/034_scan.txt')
print('Done.')
