#!/usr/bin/env python3
"""Editorial review, lote 1b: phrases found by the 031 scan.

Replaces the remaining "complete small plate / counts as a small meal / is enough"
wording with culinary descriptions, and fixes the stuffed-pepper protein boost
(1/2 cup cottage cheese is about 12 g, split across 6 peppers = about 2 g each).
Nothing is saved unless every phrase is found (or already replaced). Safe to re-run.
"""
import json, os, re, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)

RECIPE_FIXES = [
    ('is what makes this a small plate that still feels like a full meal.',
     'is what keeps each bowl small without feeling sparse.'),
    ('each one is a complete small plate, and the cool yogurt sauce',
     'each piece is about 4 oz and easy to finish, and the cool yogurt sauce'),
    ('Bread is optional; the soup is a full meal on its own.',
     'Bread is optional; the soup already has chicken, pasta and vegetables in one bowl.'),
    ('one small glass of this is often enough to get started.',
     'one small glass of this is an easy way to start the day.'),
    ('and it quietly does a lot of nutritional work.',
     'and the split peas and bone broth bring about 15 g protein per bowl.'),
    ('Small-portion tip: 3/4 cup with a small piece of bread is a complete small meal.',
     'Small-portion tip: serve 3/4 cup with a small piece of bread for dipping.'),
    ('Small-portion tip: a mug of this counts as a small meal.',
     'Small-portion tip: serve it in a mug and sip it slowly.'),
    ('Small-portion tip: half a fillet with a spoonful of rice is a complete small plate.',
     'Small-portion tip: start with half a fillet and a spoonful of rice.'),
    ('Small-portion tip: half a pepper with a spoonful of yogurt is enough on low-appetite days.',
     'Small-portion tip: start with half a pepper (about 10 g protein) and a spoonful of yogurt.'),
    ('for about 3 g more protein per pepper.',
     'for about 2 g more protein per pepper.'),
    ('Small-portion tip: a few spoonfuls is enough on hard days; the rest keeps.',
     'Small-portion tip: start with a few spoonfuls on hard days; the rest keeps in the fridge.'),
]
GUIDE_FIXES = [
    ('Are smoothies a replacement for meals?', 'Can a smoothie stand in for a meal?'),
]


def walk(obj, fn):
    if isinstance(obj, dict):
        return {k: walk(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v, fn) for v in obj]
    return fn(obj) if isinstance(obj, str) else obj


def apply(name, fixes, report):
    raw = open(P(name), encoding='utf-8').read()
    data = json.loads(raw)
    hit = {o: 0 for o, _ in fixes}
    done = {o: False for o, _ in fixes}

    def fn(s):
        for o, n in fixes:
            if o in s:
                s = s.replace(o, n); hit[o] += 1
            elif n in s:
                done[o] = True
        return s

    data = walk(data, fn)
    for o, _ in fixes:
        if hit[o]:
            report.append(f'- OK ({name}): {o[:75]}')
        elif done[o]:
            report.append(f'- already applied ({name}): {o[:75]}')
    return raw, data, [o for o in hit if not hit[o] and not done[o]]


def dump(name, raw, data):
    m = re.match(r'[\[{]\s*\n([ \t]+)', raw)
    with open(P(name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')


report = []
r = apply('recipes.json', RECIPE_FIXES, report)
g = apply('guides_legal.json', GUIDE_FIXES, report)
missing = r[2] + g[2]
if missing:
    print('ERROR: these phrases were not found. Nothing was saved.')
    for m_ in missing:
        print('  - ' + m_)
    sys.exit(1)
dump('recipes.json', r[0], r[1])
dump('guides_legal.json', g[0], g[1])
print('Language fixes (2):')
print('\n'.join(report))
print('Done.')
