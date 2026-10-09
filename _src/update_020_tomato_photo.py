#!/usr/bin/env python3
"""Photo review, round 2 (GPT vision review of full-size photos).

The tomato soup photo was flagged as a real problem (high confidence): the soup is chunky, while the recipe
is a smooth, blended soup. It is replaced by a Pexels photo whose description names the dish:
  tomato-basil-soup  14774697  "Delicious creamy tomato soup garnished with basil leaves and served with
                                breadsticks" (Shameel mukkath)

Nothing is saved unless the photo downloads. Safe to re-run.
"""
import io, json, os, re, subprocess, sys, urllib.request

sys.stderr = sys.stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

PHOTOS = {
    'tomato-basil-soup': {
        'id': 14774697, 'photographer': 'Shameel mukkath',
        'photographer_url': 'https://www.pexels.com/@shameel-mukkath-3421394/',
        'photo_url': 'https://www.pexels.com/photo/a-bowl-of-soup-with-bread-and-a-spoon-14774697/',
        'alt': 'A bowl of smooth, creamy tomato soup garnished with basil leaves, with breadsticks on the side.'},
}

recipes = json.loads(open(P('recipes.json'), encoding='utf-8').read())
by_id = {r['id']: r for r in recipes}
missing = [rid for rid in PHOTOS if rid not in by_id]
if missing:
    sys.exit(f'ERROR: recipes not found: {missing} (nothing was saved).')

craw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(craw)
todo = [rid for rid, ph in PHOTOS.items() if credits.get(rid, {}).get('photo_url') != ph['photo_url']]
if not todo:
    print('Already applied. Nothing to do.')
    sys.exit(0)

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


out = {}
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
print(f"- OK: new photo and credit for {', '.join(out)}")
print('Done.')
