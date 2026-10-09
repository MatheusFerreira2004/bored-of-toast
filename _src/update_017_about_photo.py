#!/usr/bin/env python3
"""About page photo: replace the stock photo of a person chopping parsley with a food-only Pexels photo.

Photo: "Fresh Tomatoes and Herbs on a Kitchen Table" by Salva Amin Azad (Pexels, free license)
       https://www.pexels.com/photo/fresh-tomatoes-and-herbs-on-a-kitchen-table-37314037/

- Keeps the same file name (images/our-story.webp) and the same width/height as the current image,
  so the layout does not change (center crop to the current aspect ratio).
- Regenerates responsive variants with make_images.py.
- Updates the alt text in build.py and adds a visible credit under the About photo.
- Adds the credit to credits.json (shown on /photo-credits/).

Nothing is saved unless the download succeeds. Safe to re-run.
"""
import io, json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images', 'our-story.webp')
P = lambda n: os.path.join(HERE, n)

PHOTO = {
    'id': 37314037,
    'photographer': 'Salva Amin Azad',
    'photographer_url': 'https://www.pexels.com/@salva-amin-azad-736234677/',
    'photo_url': 'https://www.pexels.com/photo/fresh-tomatoes-and-herbs-on-a-kitchen-table-37314037/',
    'alt': 'Fresh tomatoes and herbs on a kitchen table.',
}
OLD_ALT = 'Home cook chopping fresh parsley next to ripe tomatoes'
NEW_ALT = 'Fresh tomatoes and herbs on a kitchen table'
NOTE = '<div class="note"><span class="hand">made with love ♥</span></div>'
CREDIT = (f'<p class="photo-credit">Photo: <a href="{PHOTO["photo_url"]}" target="_blank" rel="noopener">'
          f'{PHOTO["photographer"]}</a> on Pexels</p>')

credits_raw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(credits_raw)
if 'our-story' in credits:
    print('Already applied. Nothing to do.')
    sys.exit(0)

b = open(P('build.py'), encoding='utf-8').read()
if OLD_ALT not in b:
    sys.exit('ERROR: About photo alt text not found in build.py. Nothing was saved.')
if not os.path.exists(IMG):
    sys.exit('ERROR: images/our-story.webp not found. Nothing was saved.')

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'])
    from PIL import Image

# ------------------------------------------------------------------ download and process (in memory)
tw, th = Image.open(IMG).size
url = f"https://images.pexels.com/photos/{PHOTO['id']}/pexels-photo-{PHOTO['id']}.jpeg?auto=compress&cs=tinysrgb&w=2000"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (bored-of-toast site build)'})
try:
    data = urllib.request.urlopen(req, timeout=60).read()
except Exception as ex:
    sys.exit(f'ERROR: could not download the About photo from Pexels ({ex}). Nothing was saved.')
im = Image.open(io.BytesIO(data)).convert('RGB')
w, h = im.size
target = tw / th
if w / h > target:
    nw = round(h * target)
    im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
else:
    nh = round(w / target)
    im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
im = im.resize((tw, th), Image.LANCZOS)
for q in (80, 74, 68, 62, 56):
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=q, method=6)
    if buf.tell() <= 195 * 1024:
        break
else:
    sys.exit('ERROR: About photo is still over 200 KB after compression. Nothing was saved.')
print(f'- downloaded About photo: {tw}x{th}, {buf.tell() // 1024} KB (quality {q})')

# ------------------------------------------------------------------ write image + variants
open(IMG, 'wb').write(buf.getvalue())
subprocess.check_call([sys.executable, P('make_images.py')])

# ------------------------------------------------------------------ build.py (alt text + visible credit)
b = b.replace(OLD_ALT, NEW_ALT)
if NOTE in b and CREDIT not in b:
    b = b.replace(NOTE, NOTE + CREDIT, 1)
    print('- added visible credit under the About photo')
else:
    print('- note: visible credit not added (layout snippet not found); credit is still listed on /photo-credits/')
open(P('build.py'), 'w', encoding='utf-8').write(b)

# ------------------------------------------------------------------ credits.json
credits['our-story'] = {k: PHOTO[k] for k in ('photographer', 'photographer_url', 'photo_url')}
credits['our-story']['source'] = 'Pexels'
credits['our-story']['alt'] = PHOTO['alt']
m = re.match(r'\{\s*\n([ \t]+)"', credits_raw)
indent = len(m.group(1)) if m else 1
with open(P('credits.json'), 'w', encoding='utf-8') as f:
    json.dump(credits, f, ensure_ascii=False, indent=indent)
    f.write('\n')

print('OK: About photo replaced with a credited Pexels food photo (no people).')
