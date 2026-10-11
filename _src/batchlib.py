#!/usr/bin/env python3
"""Shared helper for content batches (update_0NN_*.py). Not run on its own.

add_recipes(NEW, PHOTOS, new_cat=None, after_cat=None)
  - NEW: {id: recipe dict (without id/img)}
  - PHOTOS: {id: {'id': pexels_id | None, 'src': direct url (optional), 'photographer', 'photographer_url',
             'photo_url', 'source' (default 'Pexels'), 'alt'}}
  - new_cat: optional (key, label, image_id) tuple added to CATS in build.py after the line whose key is after_cat.
Nothing is written unless every photo downloads and every anchor is found. Safe to re-run.
"""
import io, json, os, re, subprocess, sys, urllib.request

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)


def _pil():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'])
        from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont


def cover(im, w, h):
    Image, _, _ = _pil()
    sw, sh = im.size
    if sw / sh > w / h:
        nw = round(sh * w / h)
        im = im.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh))
    else:
        nh = round(sw * h / w)
        im = im.crop((0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh))
    return im.resize((w, h), Image.LANCZOS)


def _font(size):
    _, _, ImageFont = _pil()
    for path in (os.path.join(ROOT, 'fonts', 'fraunces-normal.woff2'),
                 '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
                 '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default(size=size)


def _wrap(draw, text, f, width):
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
    Image, ImageDraw, _ = _pil()
    W, H, PH = 1000, 1500, 1020
    pin = Image.new('RGB', (W, H), (247, 242, 231))
    pin.paste(cover(im, W, PH), (0, 0))
    d = ImageDraw.Draw(pin)
    green = (63, 81, 48)
    small, big = _font(30), _font(62)
    d.text((W // 2, PH + 62), 'SMALL PLATES · BIG PROTEIN', font=small, fill=green, anchor='mm')
    y = PH + 140
    for ln in _wrap(d, title, big, 880)[:3]:
        d.text((W // 2, y), ln, font=big, fill=(34, 34, 34), anchor='mm')
        y += 76
    d.text((W // 2, H - 52), 'Bored of Toast', font=small, fill=green, anchor='mm')
    return pin


def _jpg(im, q=85):
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return buf.getvalue()


def fetch_photo(ph):
    Image, _, _ = _pil()
    url = ph.get('src') or f"https://images.pexels.com/photos/{ph['id']}/pexels-photo-{ph['id']}.jpeg?auto=compress&cs=tinysrgb&w=2000"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (bored-of-toast site build)'})
    data = urllib.request.urlopen(req, timeout=60).read()
    return Image.open(io.BytesIO(data)).convert('RGB')


def webp_under(im, w, h, limit_kb=195):
    main = cover(im, w, h)
    for q in (80, 74, 68, 62, 56, 50):
        buf = io.BytesIO()
        main.save(buf, 'WEBP', quality=q, method=6)
        if buf.tell() <= limit_kb * 1024:
            return buf.getvalue()
    return None


def add_recipes(NEW, PHOTOS, new_cat=None, after_cat=None, label='batch'):
    raw = open(P('recipes.json'), encoding='utf-8').read()
    recipes = json.loads(raw)
    ids = {r['id'] for r in recipes}
    if all(n in ids for n in NEW):
        print('Already applied. Nothing to do.')
        return
    clash = [n for n in NEW if n in ids]
    if clash:
        print(f'ERROR: some new ids already exist: {clash}. Nothing was saved.')
        sys.exit(1)
    missing = [n for n in NEW if n not in PHOTOS]
    if missing:
        print(f'ERROR: no photo defined for {missing}. Nothing was saved.')
        sys.exit(1)

    b = open(P('build.py'), encoding='utf-8').read()
    fm = re.search(r'FOCUS_IDS = (\[.*?\])', b)
    if not fm:
        print('ERROR: FOCUS_IDS not found in build.py. Nothing was saved.')
        sys.exit(1)
    cat_line = None
    if new_cat and f"('{new_cat[0]}'," not in b:
        am = re.search(r"^    \('" + re.escape(after_cat) + r"',[^\n]*\n", b, re.M)
        if not am:
            print(f'ERROR: could not find the {after_cat} line in CATS (build.py). Nothing was saved.')
            sys.exit(1)
        cat_line = (am.end(), f"    ('{new_cat[0]}', '{new_cat[1]}', '{new_cat[2]}'),\n")

    out = {}
    for rid in NEW:
        ph = PHOTOS[rid]
        try:
            im = fetch_photo(ph)
        except Exception as ex:
            print(f'ERROR: could not download or open the {rid} photo ({ex}). Nothing was saved.')
            sys.exit(1)
        if ph.get('crop'):
            l, t, r_, btm = ph['crop']
            W, H = im.size
            im = im.crop((int(l * W), int(t * H), int(r_ * W), int(btm * H)))
        wb = webp_under(im, 1200, 900)
        if not wb:
            print(f'ERROR: {rid} photo is still over 200 KB. Nothing was saved.')
            sys.exit(1)
        out[rid] = {'webp': wb, 'og': _jpg(cover(im, 1200, 630)), 'pin': _jpg(make_pin(im, NEW[rid]['title']))}
        print(f"- photo {rid}: {len(wb) // 1024} KB webp, og and pin generated")

    for rid, bb in out.items():
        open(os.path.join(IMG, f'{rid}.webp'), 'wb').write(bb['webp'])
        open(os.path.join(IMG, 'og', f'{rid}.jpg'), 'wb').write(bb['og'])
        open(os.path.join(IMG, 'pins', f'{rid}.jpg'), 'wb').write(bb['pin'])
    subprocess.check_call([sys.executable, P('make_images.py')])

    craw = open(P('credits.json'), encoding='utf-8').read()
    credits = json.loads(craw)
    for rid, ph in PHOTOS.items():
        if rid in NEW:
            credits[rid] = {'photographer': ph['photographer'], 'photographer_url': ph['photographer_url'],
                            'photo_url': ph['photo_url'], 'source': ph.get('source', 'Pexels'), 'alt': ph['alt']}
    m = re.match(r'\{\s*\n([ \t]+)"', craw)
    with open(P('credits.json'), 'w', encoding='utf-8') as f:
        json.dump(credits, f, ensure_ascii=False, indent=len(m.group(1)) if m else 1)
        f.write('\n')

    if cat_line:
        b = b[:cat_line[0]] + cat_line[1] + b[cat_line[0]:]
        print(f'- added the {new_cat[1]} category')
    fm = re.search(r'FOCUS_IDS = (\[.*?\])', b)
    focus = json.loads(fm.group(1))
    for rid in NEW:
        if rid not in focus:
            focus.append(rid)
    b = b[:fm.start(1)] + json.dumps(focus) + b[fm.end(1):]
    open(P('build.py'), 'w', encoding='utf-8').write(b)

    for rid, data in NEW.items():
        new = {'id': rid}
        new.update(data)
        new['img'] = f'images/{rid}.webp'
        recipes.append(new)
        print(f"- added {rid} ({data['title']}, ~{data['nutrition']['protein']} g protein, ~{data['nutrition']['calories']} kcal per serving)")
    m = re.match(r'\[\s*\n([ \t]+)\{', raw)
    with open(P('recipes.json'), 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')
    print(f'OK: {label} added. The site now has {len(recipes)} recipes.')
