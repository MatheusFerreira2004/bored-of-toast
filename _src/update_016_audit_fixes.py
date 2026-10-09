#!/usr/bin/env python3
"""Content audit fixes, round 1.

1. Recipe photos whose Pexels description did not name the dish are replaced. Rule: the Pexels title or
   description must name the dish (checked by reading each photo page before choosing):
     tomato-basil-soup         27098516  "Bowl of Tomato Soup": homemade tomato soup, basil, breadstick (Valeria Boltneva)
     overnight-oats            8108215   "A bowl of creamy oatmeal topped with fresh blueberries" (MART PRODUCTION)
     avocado-toast-jammy-eggs  7936964   "Healthy avocado toast topped with poached egg and dill" (Nicola Barts)
     lemon-chicken-orzo-soup   34326231  "Warm Chicken Noodle Soup in White Bowl" (Anhelina Vasylyk)
   No free Pexels photo of chicken orzo soup was found; a chicken noodle soup with herbs is the closest real
   match (small pasta, chicken, broth). The frittata photo is kept: its Pexels description reads "Homemade
   frittata in a skillet, garnished with fresh spinach and cheese".
2. The "Small Plates" chip and category circle are removed: every recipe carries the tag, so it filtered nothing.
   The tag itself stays (used for related recipes and the recipe eyebrow).
3. Home: the breakfast block, "Small plates to start with" and "Make-ahead" no longer repeat each other, and
   the newer recipes are shown. (The original make-ahead line is kept so update_002 still finds it.)
4. Copy: recipes page ("Every recipe includes ...") and Small-Plate Week description ("protein-first" instead of
   "high-protein", since one of the five is under 15 g).
5. The unused "fall" tag is removed from recipes.json.

Nothing is saved unless every change is found and every photo downloads. Safe to re-run.
"""
import glob, io, json, os, re, subprocess, sys, urllib.request

sys.stderr = sys.stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

PHOTOS = {
    'tomato-basil-soup': {
        'id': 27098516, 'photographer': 'Valeria Boltneva', 'photographer_url': 'https://www.pexels.com/@valeriya/',
        'photo_url': 'https://www.pexels.com/photo/bowl-of-tomato-soup-27098516/',
        'alt': 'A bowl of creamy tomato soup with basil and a breadstick on a wooden table.'},
    'overnight-oats': {
        'id': 8108215, 'photographer': 'MART PRODUCTION', 'photographer_url': 'https://www.pexels.com/@mart-production/',
        'photo_url': 'https://www.pexels.com/photo/blue-berries-on-white-ceramic-bowl-8108215/',
        'alt': 'A bowl of creamy oats topped with fresh blueberries.'},
    'avocado-toast-jammy-eggs': {
        'id': 7936964, 'photographer': 'Nicola Barts', 'photographer_url': 'https://www.pexels.com/@nicola-barts/',
        'photo_url': 'https://www.pexels.com/photo/bread-with-avocado-7936964/',
        'alt': 'Avocado toast topped with a soft egg and dill on a gray plate.'},
    'lemon-chicken-orzo-soup': {
        'id': 34326231, 'photographer': 'Anhelina Vasylyk', 'photographer_url': 'https://www.pexels.com/@anhelina-vasylyk-734724285/',
        'photo_url': 'https://www.pexels.com/photo/warm-chicken-noodle-soup-in-white-bowl-34326231/',
        'alt': 'A white bowl of chicken soup with small pasta and fresh herbs.'},
}

# ------------------------------------------------------------------ build.py (validate first, write last)
b = open(P('build.py'), encoding='utf-8').read()
log = []

CAT_LINE = "    ('small-plates', 'Small Plates', 'avocado-toast-jammy-eggs'),\n"
if CAT_LINE in b:
    b = b.replace(CAT_LINE, '')
    log.append('- OK: Small Plates chip and category circle removed')
elif "('small-plates', 'Small Plates'" not in b:
    log.append('- already applied: Small Plates chip removed')
else:
    sys.exit('ERROR: Small Plates category line has an unexpected format (nothing was saved).')

HOME_LATEST = ['lighter-chicken-alfredo', 'turkey-taco-rice-bowls', 'crispy-baked-chicken-bites', 'tuna-white-bean-salad',
               'sheet-pan-salmon', 'chicken-avocado-salad', 'peanut-butter-protein-bites', 'chocolate-yogurt-mousse-cups']
BUILD = [
    ("bt = [BY_ID[i] for i in ['shakshuka', 'avocado-toast-jammy-eggs', 'overnight-oats', 'breakfast-burritos']]",
     "bt = [BY_ID[i] for i in ['cottage-cheese-pancakes', 'spinach-feta-mini-frittata', 'shakshuka', 'avocado-toast-jammy-eggs']]"),
    ("latest = [BY_ID[i] for i in FOCUS_IDS[:8]]",
     "latest = [BY_ID[i] for i in " + repr(HOME_LATEST) + "]\n"
     "    shown = {r['id'] for r in bt + latest} | {wk['id']}\n"
     "    fall = [r for r in RECIPES if 'make-ahead' in r['tags'] and r['id'] not in shown][:4]"),
    ("Featured recipes add a small-portion tip and a gentler swap.",
     "Every recipe includes a small-portion tip and a gentler swap."),
    ("'Five small, high-protein meals for one easy week,",
     "'Five small, protein-first meals for one easy week,"),
]
for old, new in BUILD:
    if new in b:
        log.append(f'- already applied: {new[:70]}')
    elif b.count(old) == 1:
        b = b.replace(old, new)
        log.append(f'- OK: {new[:70]}')
    else:
        sys.exit(f'ERROR: not found exactly once in build.py (nothing was saved):\n{old}')

# ------------------------------------------------------------------ recipes.json
raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(raw)
by_id = {r['id']: r for r in recipes}
missing = [rid for rid in list(PHOTOS) + HOME_LATEST + ['cottage-cheese-pancakes', 'spinach-feta-mini-frittata'] if rid not in by_id]
if missing:
    sys.exit(f'ERROR: recipes not found: {missing} (nothing was saved).')
fall_ids = [r['id'] for r in recipes if 'fall' in r.get('tags', [])]
for r in recipes:
    r['tags'] = [t for t in r.get('tags', []) if t != 'fall']

# ------------------------------------------------------------------ photos (download in memory first)
craw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(craw)
todo = [rid for rid, ph in PHOTOS.items() if credits.get(rid, {}).get('photo_url') != ph['photo_url']]

out = {}
if todo:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'])
        from PIL import Image, ImageDraw, ImageFont

    def cover(im, w, h):
        sw, sh = im.size
        if sw / sh > w / h:
            nw = round(sh * w / h)
            im = im.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh))
        else:
            nh = round(sw * h / w)
            im = im.crop((0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh))
        return im.resize((w, h), Image.LANCZOS)

    def font(size):
        for path in (os.path.join(ROOT, 'fonts', 'fraunces-normal.woff2'),
                     '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
                     '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
        return ImageFont.load_default(size=size)

    def wrap(draw, text, f, width):
        lines, cur = [], ''
        for w in text.split():
            t = (cur + ' ' + w).strip()
            if draw.textlength(t, font=f) <= width or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def make_pin(im, title):
        W, H, PH = 1000, 1500, 1020
        pin = Image.new('RGB', (W, H), (247, 242, 231))
        pin.paste(cover(im, W, PH), (0, 0))
        d = ImageDraw.Draw(pin)
        green = (63, 81, 48)
        small, big = font(30), font(62)
        d.text((W // 2, PH + 62), 'SMALL PLATES · BIG PROTEIN', font=small, fill=green, anchor='mm')
        y = PH + 140
        for ln in wrap(d, title, big, 880)[:3]:
            d.text((W // 2, y), ln, font=big, fill=(34, 34, 34), anchor='mm')
            y += 76
        d.text((W // 2, H - 52), 'Bored of Toast', font=small, fill=green, anchor='mm')
        return pin

    def jpg(im, q=85):
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
        return buf.getvalue()

    for rid in todo:
        ph = PHOTOS[rid]
        url = f"https://images.pexels.com/photos/{ph['id']}/pexels-photo-{ph['id']}.jpeg?auto=compress&cs=tinysrgb&w=2000"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (bored-of-toast site build)'})
        try:
            data = urllib.request.urlopen(req, timeout=60).read()
            im = Image.open(io.BytesIO(data)).convert('RGB')
        except Exception as ex:
            print(f'ERROR: could not download or open the {rid} photo from Pexels ({ex}). Nothing was saved.')
            sys.exit(1)
        main = cover(im, 1200, 900)
        for q in (80, 74, 68, 62, 56):
            buf = io.BytesIO()
            main.save(buf, 'WEBP', quality=q, method=6)
            if buf.tell() <= 195 * 1024:
                break
        else:
            print(f'ERROR: {rid} photo is still over 200 KB. Nothing was saved.')
            sys.exit(1)
        out[rid] = {'webp': buf.getvalue(), 'og': jpg(cover(im, 1200, 630)), 'pin': jpg(make_pin(im, by_id[rid]['title']))}
        print(f"- photo {rid}: {len(out[rid]['webp']) // 1024} KB webp, og and pin generated")

# ------------------------------------------------------------------ write everything
if out:
    for rid, data in out.items():
        for f in os.listdir(IMG):
            if re.fullmatch(re.escape(rid) + r'-\d+w\.webp', f):
                os.remove(os.path.join(IMG, f))
        open(os.path.join(IMG, f'{rid}.webp'), 'wb').write(data['webp'])
        open(os.path.join(IMG, 'og', f'{rid}.jpg'), 'wb').write(data['og'])
        open(os.path.join(IMG, 'pins', f'{rid}.jpg'), 'wb').write(data['pin'])
    subprocess.check_call([sys.executable, P('make_images.py')])
    for rid in out:
        ph = PHOTOS[rid]
        credits[rid] = {'photographer': ph['photographer'], 'photographer_url': ph['photographer_url'],
                        'photo_url': ph['photo_url'], 'source': 'Pexels', 'alt': ph['alt']}
    m = re.match(r'\{\s*\n([ \t]+)"', craw)
    with open(P('credits.json'), 'w', encoding='utf-8') as f:
        json.dump(credits, f, ensure_ascii=False, indent=len(m.group(1)) if m else 1)
        f.write('\n')
    log.append(f"- OK: new photos and credits for {', '.join(out)}")
else:
    log.append('- already applied: recipe photos')

open(P('build.py'), 'w', encoding='utf-8').write(b)

if fall_ids:
    m = re.match(r'\[\s*\n([ \t]+)\{', raw)
    with open(P('recipes.json'), 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')
    log.append(f"- OK: 'fall' tag removed from {', '.join(fall_ids)}")
else:
    log.append("- already applied: no 'fall' tags left")

print('\n'.join(log))
print('Done.')
