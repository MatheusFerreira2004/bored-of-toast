#!/usr/bin/env python3
"""Editorial review, lote 6: photos and voice.

1. baked-cinnamon-apples: the rawpixel image showed rawpixel watermarks. It is replaced by a
   watermark-free Pexels photo whose description names the dish:
     Pexels 8551537 "A close-up of a baked apple and nut dessert on a rustic wooden table." (Dasha Klimova)
   Pexels license: free to use, attribution not required (credit kept anyway). The recipe is a baked apple
   filled with oats and walnuts, which matches. Portrait 2:3 source, centre-cropped to the site's 4:3.
   Watermarks are never removed digitally; the image is replaced.
2. Voice: removes the repetitive adverb "quietly" ("quietly carries a good amount of protein",
   "quietly does a lot of nutritional work"...) from recipes.json and guides_legal.json. Two known phrases
   get specific wording; elsewhere the adverb is dropped. Every change is listed in
   _src/reports/039_voice.md; any occurrence that cannot be fixed safely is listed for manual review.

Nothing is written unless the photo downloads. Idempotent: a second run changes nothing.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import batchlib as B  # noqa: E402  (sets stderr to stdout)

P = lambda *n: os.path.join(HERE, *n)

RID = 'baked-cinnamon-apples'
PHOTO = {
    'id': 8551537,
    'photographer': 'Dasha Klimova',
    'photographer_url': 'https://www.pexels.com/@doraklimova/',
    'photo_url': 'https://www.pexels.com/photo/cooked-food-on-black-ceramic-bowl-8551537/',
    'source': 'Pexels',
    'alt': 'A baked apple with a nut filling in a dark bowl on a rustic wooden table.',
}

RULES = [
    (re.compile(r'\bquietly does a lot of nutritional work\b'), 'adds protein without changing the flavor much'),
    (re.compile(r'\bquietly carries a good amount of protein\b'), 'adds a useful amount of protein'),
    (re.compile(r'\bQuietly\s+(\w)'), lambda m: m.group(1).upper()),
    (re.compile(r'\bquietly\s+(?=\w)'), ''),
]
LEFT = re.compile(r'\bquietly\b', re.I)


def indent_of(raw):
    m = re.match(r'[\[{]\s*\n([ \t]+)\S', raw)
    return len(m.group(1)) if m else None


def write_json(name, raw, data):
    with open(P(name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent_of(raw))
        f.write('\n')


# ------------------------------------------------------------------ 1. photo
recipes_raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(recipes_raw)
by_id = {r['id']: r for r in recipes}
if RID not in by_id:
    print(f'ERROR: {RID} not found in recipes.json. Nothing was saved.')
    sys.exit(1)

credits_raw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(credits_raw)
report = []

if credits.get(RID, {}).get('photo_url') == PHOTO['photo_url']:
    print(f'- already applied: {RID} photo')
else:
    try:
        im = B.fetch_photo(PHOTO)
    except Exception as ex:
        print(f'ERROR: could not download or open the {RID} photo ({ex}). Nothing was saved.')
        sys.exit(1)
    wb = B.webp_under(im, 1200, 900)
    if not wb:
        print(f'ERROR: {RID} photo is still over 200 KB. Nothing was saved.')
        sys.exit(1)
    og = B._jpg(B.cover(im, 1200, 630))
    pin = B._jpg(B.make_pin(im, by_id[RID]['title']))
    for f in os.listdir(B.IMG):
        if re.fullmatch(re.escape(RID) + r'-\d+w\.webp', f):
            os.remove(os.path.join(B.IMG, f))
    open(os.path.join(B.IMG, f'{RID}.webp'), 'wb').write(wb)
    open(os.path.join(B.IMG, 'og', f'{RID}.jpg'), 'wb').write(og)
    open(os.path.join(B.IMG, 'pins', f'{RID}.jpg'), 'wb').write(pin)
    subprocess.check_call([sys.executable, P('make_images.py')])
    credits[RID] = {k: PHOTO[k] for k in ('photographer', 'photographer_url', 'photo_url', 'source', 'alt')}
    write_json('credits.json', credits_raw, credits)
    msg = f'{RID}: new photo Pexels 8551537 by Dasha Klimova ({len(wb) // 1024} KB webp, og and pin regenerated)'
    print('- ' + msg)
    report.append(msg)

# ------------------------------------------------------------------ 2. voice
changes, leftovers = [], []


def fix(s):
    out = s
    for rx, rep in RULES:
        out = rx.sub(rep, out)
    return out


def walk(o, path):
    if isinstance(o, str):
        n = fix(o)
        if n != o:
            i = LEFT.search(o)
            a = max(0, (i.start() if i else 0) - 40)
            changes.append(f'{path}: "...{o[a:a + 120]}..." -> "...{n[a:a + 110]}..."')
        for m in LEFT.finditer(n):
            leftovers.append(f'{path}: "...{n[max(0, m.start() - 50): m.end() + 50]}..."')
        return n
    if isinstance(o, list):
        return [walk(v, f'{path}[{i}]') for i, v in enumerate(o)]
    if isinstance(o, dict):
        return {k: walk(v, f'{path}.{k}') for k, v in o.items()}
    return o


recipes = json.loads(open(P('recipes.json'), encoding='utf-8').read())
before = len(changes)
new_recipes = [walk(r, r.get('id', '?')) for r in recipes]
if len(changes) > before:
    write_json('recipes.json', recipes_raw, new_recipes)

guides_raw = open(P('guides_legal.json'), encoding='utf-8').read()
guides = json.loads(guides_raw)
before = len(changes)
new_guides = walk(guides, 'guides_legal')
if len(changes) > before:
    write_json('guides_legal.json', guides_raw, new_guides)

for c in changes:
    print('- voice: ' + c)
for l in leftovers:
    print('- left for manual review: ' + l)
if not changes:
    print('- already applied: voice (no "quietly" left to trim)')

# The report is written only when something changed, so a second run leaves the repository untouched.
if report or changes:
    out = ['# Lote 6: photos and voice', '', '## Photos'] + (['- ' + r for r in report] or ['- none this run'])
    out += ['', '## Voice: "quietly" removed'] + (['- ' + c for c in changes] or ['- none this run'])
    out += ['', '## Left for manual review'] + (['- ' + l for l in leftovers] or ['- none'])
    out += ['', '## Not changed in this lote (needs visual confirmation)',
            '- smoky chickpea and black bean chili: check whether black beans are visible',
            '- smoked salmon bagel halves: optional swap for an open-faced half (aesthetic only)',
            '- sheet-pan salmon, baked cod, ginger egg drop soup, frozen yogurt bars: keep unless a review shows a real problem']
    os.makedirs(P('reports'), exist_ok=True)
    with open(P('reports', '039_voice.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
print('Done.')
