#!/usr/bin/env python3
"""Editorial review, lote 2 (corrected): portions and protein.

The first version of this script divided the per-serving protein by two whenever a
"Small-portion tip" contained words like "half". That rule was wrong (half a bagel,
half an egg, half a cup, half of one ingredient...). This version:

1. Removes every automatic suffix "That smaller amount has about N g protein (the full
   serving has about M g)." added by the first version.
2. Applies a protein number ONLY through explicit per-recipe rules below, each with the
   standard serving, the smaller amount, the components included and the basis.
   A rule is applied only if the recipe's per-serving protein matches the value the
   rule was written for; otherwise it is skipped and reported.
3. Generic tip "serve half a portion and save the rest for later": every component of
   the serving is halved by definition, so half the per-serving protein is stated.
4. Every other tip that lost its automatic number is listed for manual review; no
   number is invented for it.
5. Replaces remaining food-sufficiency phrases with culinary descriptions and lists any
   other occurrences of risky words for review ("enough water" etc. is not changed).

Writes a report to _src/reports/portion_review.md. Idempotent: a second run changes
nothing. Nothing is saved if recipes.json cannot be read.
"""
import json, os, re, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *n: os.path.join(HERE, *n)

AUTO_SUFFIX = re.compile(r'\s*That smaller amount has about \d+(?:\.\d+)? g protein \(the full serving has about \d+(?:\.\d+)? g\)\.')
GENERIC = 'Small-portion tip: serve half a portion and save the rest for later.'
MILK_CUP = 8  # site reference: 1 cup milk about 7 to 8 g

# id: (expected per-serving protein, new tip or None to keep the current tip, basis or None if no number)
EXPLICIT = {
    'smoked-salmon-bagel-halves': (16,
        'Small-portion tip: one prepared bagel half is the standard serving here, with about 16 g protein. '
        'For a smaller plate, eat half of that bagel half, with the spread and salmon shared the same way, for about 8 g. '
        'Cut it into quarters to eat slowly.',
        'Standard serving = 1 prepared bagel half (16 g). Smaller amount = half of that bagel half, spread and salmon proportional: 16 / 2 = 8 g.'),
    'berry-greek-yogurt-muffins': (7,
        'Small-portion tip: half a muffin on its own has about 3 to 4 g protein. '
        f'With 1 cup milk (about {MILK_CUP} g) the snack comes to about 11 to 12 g.',
        'Standard serving = 1 muffin (7 g). Half a muffin = 3.5 g. Plus 1 cup milk, site reference about 8 g = about 11.5 g.'),
    'chicken-rice-congee': (23,
        'Small-portion tip: start with a smaller bowl topped with half an egg. It is soft and easy to eat in small spoonfuls; '
        'add the other half of the egg if you want more.',
        None),
    'turkey-taco-rice-bowls': (24,
        'Small-portion tip: build a smaller bowl with a little more turkey and less rice. The rest keeps for tomorrow.',
        None),
    'chocolate-yogurt-mousse-cups': (14,
        'Small-portion tip: serve half of one prepared cup, with the raspberries shared the same way. '
        'That half has about 7 g protein; the rest keeps covered in the fridge.',
        'Standard serving = 1 prepared cup (14 g). Smaller amount = half of that cup, all components proportional: 7 g.'),
    'strawberry-cottage-cheese-bowl': (26,
        'Small-portion tip: make half a bowl, halving the cottage cheese and every topping. That half has about 13 g protein.',
        'Standard serving = 1 bowl (26 g). Smaller amount = half of the bowl, every component halved: 13 g.'),
    'sheet-pan-salmon': (26,
        'Small-portion tip: start with half a piece, about 2 oz of salmon with half the usual spoonful of sauce. '
        'That half has about 13 g protein; the rest is good cold the next day.',
        'Standard serving = one 4 oz piece with a spoonful of sauce (26 g). Smaller amount = half of both: 13 g.'),
    'peanut-butter-protein-bites': (6,
        f'Small-portion tip: start with one bite. Two bites with 1 cup milk provide about {2 * 6 + MILK_CUP} g protein.',
        'Serving = 1 bite (6 g). Two bites = 12 g, plus 1 cup milk, site reference about 8 g = 20 g.'),
    'turkey-stuffed-peppers': (19, None,
        'Standard serving = 1 pepper (19 g). Half a pepper, filling proportional = 9.5 g, stated as about 10 g (set in lote 1b).'),
}

PHRASES = [
    ('a complete small lunch', 'an easy small lunch'),
    ('a full small meal', 'an easy small meal'),
    ('and two with a glass of milk is close to a light meal on low-appetite days',
     'and two with a glass of milk make a slightly bigger snack'),
    ('is what turns this into a small plate that still counts as a full lunch',
     'is what keeps each bowl small while still carrying about 16 g protein'),
    (' A half bowl still counts.', ''),
]
RISKY = re.compile(r'complete small|full small|counts as|still counts|full meal|complete meal|\benough\b|\bminimum\b', re.I)
SAFE_ENOUGH = re.compile(r'enough (?:water|liquid|broth|milk|oil|room|space|time|to cover|to coat|to loosen|to thin|heat)|long enough|big enough|large enough|hot enough|thick enough|thin enough|wide enough|warm enough|firm enough|soft enough|cool enough|deep enough', re.I)


def protein_of(r):
    n = r.get('nutrition')
    if isinstance(n, dict) and isinstance(n.get('protein'), (int, float)):
        return n['protein']
    return None


def fmt(v):
    return f'{v:g}'


def dump(raw, data):
    m = re.match(r'[\[{]\s*\n([ \t]+)', raw)
    with open(P('recipes.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')


def walk(obj, fn, path=''):
    if isinstance(obj, dict):
        return {k: walk(v, fn, path) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v, fn, path) for v in obj]
    return fn(obj) if isinstance(obj, str) else obj


raw = open(P('recipes.json'), encoding='utf-8').read()
try:
    recipes = json.loads(raw)
except Exception as e:
    print(f'ERROR: could not read recipes.json ({e}). Nothing was saved.')
    sys.exit(1)

changes, numbers, removed, skipped, phrase_hits, risky = [], [], [], [], [], []

for r in recipes:
    rid = r.get('id', '?')
    p = protein_of(r)
    tips = list(r.get('tips') or [])
    had_auto = False
    new_tips = []
    for t in tips:
        if not isinstance(t, str):
            new_tips.append(t); continue
        stripped = AUTO_SUFFIX.sub('', t)
        if stripped != t:
            had_auto = True
        # duplicate pairing line added by the first version for the protein bites
        if rid == 'peanut-butter-protein-bites' and stripped.startswith('These are a small snack, not a meal.'):
            changes.append(f'{rid}: removed duplicate pairing tip')
            continue
        new_tips.append(stripped)
    tips = new_tips

    # muffins: keep only one Greek yogurt pairing line
    if rid == 'berry-greek-yogurt-muffins':
        seen, dedup = False, []
        for t in tips:
            if isinstance(t, str) and '1/2 cup plain nonfat Greek yogurt for about' in t:
                if seen:
                    changes.append(f'{rid}: removed duplicate yogurt pairing tip'); continue
                seen = True
            dedup.append(t)
        tips = dedup

    idx = next((i for i, t in enumerate(tips) if isinstance(t, str) and t.lower().startswith('small-portion tip')), None)

    if rid in EXPLICIT:
        exp_p, new_tip, basis = EXPLICIT[rid]
        if p != exp_p:
            skipped.append(f'{rid}: per-serving protein is {p}, rule written for {exp_p}; rule not applied')
        else:
            if new_tip is not None:
                if idx is None:
                    skipped.append(f'{rid}: no Small-portion tip found; rule not applied')
                elif tips[idx] != new_tip:
                    tips[idx] = new_tip
                    changes.append(f'{rid}: Small-portion tip rewritten')
            if basis:
                numbers.append(f'{rid}: {basis}')
            else:
                removed.append(f'{rid}: number removed. The smaller amount is not a proportional part of a confirmed serving (see rule notes).')
    elif idx is not None and tips[idx].startswith(GENERIC):
        if p is None:
            skipped.append(f'{rid}: generic half-portion tip but protein not found; no number added')
        else:
            new_tip = f'Small-portion tip: serve half a portion and keep the rest for later. Half a serving has about {fmt(p / 2)} g protein.'
            if tips[idx] != new_tip:
                tips[idx] = new_tip
                changes.append(f'{rid}: generic half-portion tip rewritten')
            numbers.append(f'{rid}: Standard serving ({fmt(p)} g); half a portion, every component halved = {fmt(p / 2)} g.')
    elif had_auto:
        removed.append(f'{rid}: automatic number removed; tip needs manual review: "{tips[idx] if idx is not None else "(no tip)"}"')

    r['tips'] = tips


# sufficiency phrases (all recipe text)
def fix(s):
    for o, n in PHRASES:
        if o in s:
            s = s.replace(o, n)
            phrase_hits.append(o.strip())
    return s

recipes = walk(recipes, fix)

# scan for anything left
for r in recipes:
    rid = r.get('id', '?')
    def scan(s):
        for m in RISKY.finditer(s):
            ctx = s[max(0, m.start() - 50): m.end() + 50]
            if m.group().lower() == 'enough' and SAFE_ENOUGH.search(s[max(0, m.start() - 15): m.end() + 15]):
                continue
            risky.append(f'{rid}: ...{ctx}...')
        return s
    walk(r, scan)

dump(raw, recipes)

out = ['# Portion and protein review (lote 2, corrected)', '']
out += ['## Changed this run'] + (['- ' + c for c in changes] or ['- nothing (already applied)'])
out += ['', '## Sufficiency phrases replaced this run'] + (['- ' + h for h in sorted(set(phrase_hits))] or ['- nothing (already applied)'])
out += ['', '## Numbers kept, with basis'] + ['- ' + n for n in numbers]
out += ['', '## Numbers removed (no confirmed basis)'] + (['- ' + x for x in removed] or ['- none'])
out += ['', '## Rules skipped'] + (['- ' + s for s in skipped] or ['- none'])
out += ['', '## Remaining risky wording for manual review'] + (['- ' + x for x in risky] or ['- none'])
report = '\n'.join(out) + '\n'
os.makedirs(P('reports'), exist_ok=True)
with open(P('reports', 'portion_review.md'), 'w', encoding='utf-8') as f:
    f.write(report)
print(report)
print('Done.')
