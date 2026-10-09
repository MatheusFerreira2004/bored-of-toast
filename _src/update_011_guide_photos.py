#!/usr/bin/env python3
"""New cover photos for the three GLP-1 Kitchen guides (free Pexels photos, no AI).

- Downloads three photos from Pexels (free license, commercial use allowed, credited on the site).
- Center-crops to 3:2, resizes to 1400 px wide and saves as WebP under 200 KB.
- Removes the old guide photos (pantry jars, rice, knife) and their credits.
- Regenerates responsive variants with make_images.py.
- Points GUIDE_IMG in build.py to the new photos and adds credits in credits.json.

Photos:
  guide-gentle   Foodie Factor        https://www.pexels.com/photo/acai-bowl-with-mixed-berries-566564/
  guide-protein  Natali Yakovleva     https://www.pexels.com/photo/eggs-and-milk-breakfast-preparation-16149475/
  guide-mealprep Julia M Cameron      https://www.pexels.com/photo/food-in-containers-6995259/

Nothing is saved unless every download succeeds. Safe to re-run.
"""
import glob, io, json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

PHOTOS = {
    'guide-gentle': {
        'id': 566564,
        'guide': 'nothing-sounds-good',
        'photographer': 'Foodie Factor',
        'photographer_url': 'https://www.pexels.com/@foodie-factor-162291',
        'photo_url': 'https://www.pexels.com/photo/acai-bowl-with-mixed-berries-566564/',
        'alt': 'A bowl of yogurt topped with fresh blueberries, strawberries and granola.',
    },
    'guide-protein': {
        'id': 16149475,
        'guide': 'protein-first',
        'photographer': 'Natali Yakovleva',
        'photographer_url': 'https://www.pexels.com/@natali-yakovleva-501836818',
        'photo_url': 'https://www.pexels.com/photo/eggs-and-milk-breakfast-preparation-16149475/',
        'alt': 'Fresh eggs and a jug of milk on a rustic wooden kitchen table.',
    },
    'guide-mealprep': {
        'id': 6995259,
        'guide': 'small-portion-meal-prep',
        'photographer': 'Julia M Cameron',
        'photographer_url': 'https://www.pexels.com/@julia-m-cameron',
        'photo_url': 'https://www.pexels.com/photo/food-in-containers-6995259/',
        'alt': 'Meal prep containers filled with broccoli, beans and polenta.',
    },
}
OLD = ['guide-pantry', 'guide-rice', 'guide-knife']

b = open(P('build.py'), encoding='utf-8').read()
if "'nothing-sounds-good': 'guide-gentle'" in b:
    print('Already applied. Nothing to do.')
    sys.exit(0)
if 'GUIDE_REDIRECTS' not in b:
    sys.exit('ERROR: run update_010_glp1_kitchen.py first (nothing was saved).')

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'])
    from PIL import Image

# ------------------------------------------------------------------ download and process (in memory)
out = {}
for name, ph in PHOTOS.items():
    url = f"https://images.pexels.com/photos/{ph['id']}/pexels-photo-{ph['id']}.jpeg?auto=compress&cs=tinysrgb&w=2000"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (bored-of-toast site build)'})
    try:
        data = urllib.request.urlopen(req, timeout=60).read()
    except Exception as ex:
        sys.exit(f'ERROR: could not download {name} from Pexels ({ex}). Nothing was saved.')
    im = Image.open(io.BytesIO(data)).convert('RGB')
    w, h = im.size
    target = 3 / 2
    if w / h > target:
        nw = round(h * target)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w / target)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((1400, 933), Image.LANCZOS)
    for q in (78, 72, 66, 60, 54):
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=q, method=6)
        if buf.tell() <= 195 * 1024:
            break
    else:
        sys.exit(f'ERROR: {name} is still over 200 KB after compression. Nothing was saved.')
    out[name] = buf.getvalue()
    print(f'- downloaded {name}: {len(out[name]) // 1024} KB (quality {q})')

# ------------------------------------------------------------------ write images, remove old ones
for name, blob in out.items():
    open(os.path.join(IMG, f'{name}.webp'), 'wb').write(blob)
removed = 0
for old in OLD:
    for f in glob.glob(os.path.join(IMG, f'{old}.webp')) + glob.glob(os.path.join(IMG, f'{old}-*w.webp')):
        os.remove(f)
        removed += 1
print(f'- removed {removed} old guide image files')

subprocess.check_call([sys.executable, P('make_images.py')])

# ------------------------------------------------------------------ build.py
NEW_IMG = ("GUIDE_IMG = {'nothing-sounds-good': 'guide-gentle', 'protein-first': 'guide-protein', "
           "'small-portion-meal-prep': 'guide-mealprep'}")
b, n = re.subn(r"GUIDE_IMG = \{[^\n]*\}", NEW_IMG, b, count=1)
if n != 1:
    sys.exit('ERROR: GUIDE_IMG not found in build.py.')
open(P('build.py'), 'w', encoding='utf-8').write(b)

# ------------------------------------------------------------------ credits.json
raw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(raw)
for old in OLD:
    credits.pop(old, None)
for name, ph in PHOTOS.items():
    credits[name] = {k: ph[k] for k in ('photographer', 'photographer_url', 'photo_url')}
    credits[name]['source'] = 'Pexels'
    credits[name]['alt'] = ph['alt']
m = re.match(r'\{\s*\n([ \t]+)"', raw)
indent = len(m.group(1)) if m else 1
with open(P('credits.json'), 'w', encoding='utf-8') as f:
    json.dump(credits, f, ensure_ascii=False, indent=indent)
    f.write('\n')

print('OK: 3 new guide photos from Pexels, old guide photos and credits removed, variants regenerated.')
