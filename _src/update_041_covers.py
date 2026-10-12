#!/usr/bin/env python3
"""Lote 7a: product covers, a bundle mockup and one Pinterest pin, drawn in code.

No photos and no AI: only the site's own fonts (Fraunces and Inter, SIL Open Font License, already in /fonts)
and the site's colors. Everything is written to _src/covers/, which is outside the published site, so this
script does not change any page. The covers are meant to replace page 1 of each PDF first; the site only
starts using them after the PDFs are updated (see _src/covers/README.md).

Safe to re-run: it skips when _src/covers/VERSION already matches DESIGN_VERSION.
"""
import io, os, subprocess, sys, tempfile

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
OUT = os.path.join(HERE, 'covers')
FONTS = os.path.join(ROOT, 'fonts')
DESIGN_VERSION = 'covers-v1'

vf = os.path.join(OUT, 'VERSION')
if os.path.exists(vf) and open(vf, encoding='utf-8').read().strip() == DESIGN_VERSION:
    print('Already applied. Nothing to do.')
    sys.exit(0)


def need(mod, pkg):
    try:
        __import__(mod)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', pkg])


need('PIL', 'pillow')
need('fontTools', 'fonttools')
need('brotli', 'brotli')
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fontTools.ttLib import TTFont

for name in ('fraunces-normal', 'fraunces-italic', 'inter'):
    if not os.path.exists(os.path.join(FONTS, name + '.woff2')):
        print(f'ERROR: fonts/{name}.woff2 not found. Nothing was saved.')
        sys.exit(1)

GREEN = (63, 81, 48)
GREEN_DARK = (47, 61, 36)
GREEN_SOFT = (86, 105, 63)
YELLOW = (242, 180, 49)
CREAM = (247, 242, 231)
CREAM2 = (239, 232, 216)
PAPER = (255, 253, 248)
INK = (43, 42, 36)
MUTED = (109, 106, 94)
LINE = (226, 218, 199)
SAGE = (150, 173, 110)
TERRA = (204, 112, 74)
HONEY = (219, 170, 96)

TMP = tempfile.mkdtemp()
_ttf, _fonts = {}, {}


def ttf(name):
    if name not in _ttf:
        dst = os.path.join(TMP, name + '.ttf')
        f = TTFont(os.path.join(FONTS, name + '.woff2'))
        f.flavor = None
        f.save(dst)
        _ttf[name] = dst
    return _ttf[name]


def font(name, size, axes=None):
    key = (name, size, tuple(sorted((axes or {}).items())))
    if key in _fonts:
        return _fonts[key]
    f = ImageFont.truetype(ttf(name), size)
    if axes:
        try:
            vals = []
            for a in f.get_variation_axes():
                n = a.get('name', b'')
                n = (n.decode('utf-8', 'ignore') if isinstance(n, bytes) else str(n)).lower()
                v = a.get('default', a.get('minimum'))
                for want_key, want in axes.items():
                    if want_key in n:
                        v = max(a['minimum'], min(a['maximum'], want))
                vals.append(v)
            f.set_variation_by_axes(vals)
        except Exception as ex:
            print(f'- note: could not set axes on {name} ({ex}); default instance used')
    _fonts[key] = f
    return f


def wrap(d, text, f, width):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, name, axes, width, sizes, max_lines):
    for s in sizes:
        f = font(name, s, axes)
        lines = wrap(d, text, f, width)
        if len(lines) <= max_lines and all(d.textlength(l, font=f) <= width for l in lines):
            return f, lines, s
    return None


def spaced(d, cx, cy, text, f, fill, spacing):
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, cy), ch, font=f, fill=fill, anchor='lm')
        x += w + spacing
    return total


TITLE_AX = {'optical': 144, 'weight': 400}
SUB_AX = {'optical': 72, 'weight': 400}
SANS_AX = {'weight': 600}
BODY_AX = {'weight': 500}

COVERS = [
    ('nourished-main-guide-cover', {
        'eyebrow': 'BORED OF TOAST', 'title': 'Nourished', 'subtitle': 'The GLP-1 Kitchen Companion',
        'badge': 'Main guide', 'accent': YELLOW,
        'lines': ['24 small-plate recipes', 'Weeks 1\u20132 of meal examples', 'Shopping and prep guidance']}),
    ('bonus-1-28-day-meal-plan-cover', {
        'eyebrow': 'NOURISHED \u00b7 BONUS 1', 'title': '28-Day Meal Plan', 'subtitle': 'All four weeks in one file',
        'badge': 'Bonus', 'accent': SAGE,
        'lines': ['Weeks 1\u20134 of meal examples', 'A shopping list for each week', 'Ready to print']}),
    ('bonus-2-recipe-pack-vol-2-cover', {
        'eyebrow': 'NOURISHED \u00b7 BONUS 2', 'title': 'Recipe Pack Vol. 2', 'subtitle': '12 more small-plate recipes',
        'badge': 'Bonus', 'accent': TERRA,
        'lines': ['Recipes 25\u201336', 'Grouped by texture', 'Portions and substitutions']}),
    ('bonus-3-printable-pack-cover', {
        'eyebrow': 'NOURISHED \u00b7 BONUS 3', 'title': 'Printable Pack', 'subtitle': 'Planners for your own choices',
        'badge': 'Bonus', 'accent': HONEY,
        'lines': ['11 printable sheets', 'Meals, shopping and freezer stock', 'Space for your own notes']}),
    ('starter-kit-cover', {
        'eyebrow': 'FREE \u00b7 GLP-1 KITCHEN', 'title': 'Starter Kit', 'subtitle': 'A free taste of Nourished',
        'badge': 'Free', 'accent': YELLOW, 'panel': GREEN_SOFT,
        'lines': ['3 sample recipes', 'Shopping checklist', '3-day organizer']}),
]

W, H, PANEL = 1275, 1650, 980   # US Letter at 150 dpi


def make_cover(sp):
    im = Image.new('RGBA', (W, H), CREAM + (255,))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, PANEL), fill=sp.get('panel', GREEN))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((W - 560, -380, W + 240, 420), fill=sp['accent'] + (70,))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    im.alpha_composite(glow.crop((0, 0, W, PANEL)), (0, 0))
    d = ImageDraw.Draw(im)
    cx = W / 2

    ef = font('inter', 30, SANS_AX)
    tw = spaced(d, cx, 170, sp['eyebrow'], ef, CREAM, 7)
    for sx in (-1, 1):
        x0 = cx + sx * (tw / 2 + 28)
        x1 = cx + sx * (tw / 2 + 74)
        d.rectangle((min(x0, x1), 168, max(x0, x1), 172), fill=YELLOW)

    res = fit(d, sp['title'], 'fraunces-normal', TITLE_AX, 1035, range(210, 139, -10), 1) or \
        fit(d, sp['title'], 'fraunces-normal', TITLE_AX, 1035, range(160, 99, -10), 2)
    if not res:
        raise ValueError('title does not fit: ' + sp['title'])
    tf, tlines, ts = res
    y = 320
    for ln in tlines:
        d.text((cx, y), ln, font=tf, fill=CREAM, anchor='mt')
        y += int(ts * 1.04)
    y += 36
    sres = fit(d, sp['subtitle'], 'fraunces-italic', SUB_AX, 1035, range(64, 39, -4), 1)
    if not sres:
        raise ValueError('subtitle does not fit: ' + sp['subtitle'])
    sf, slines, _ = sres
    d.text((cx, y), slines[0], font=sf, fill=YELLOW, anchor='mt')

    # the small plate
    r = 200
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((cx - r + 8, PANEL - r + 22, cx + r + 8, PANEL + r + 22), fill=GREEN_DARK + (80,))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
    d = ImageDraw.Draw(im)
    d.ellipse((cx - r, PANEL - r, cx + r, PANEL + r), fill=PAPER)
    d.ellipse((cx - 165, PANEL - 165, cx + 165, PANEL + 165), outline=LINE, width=4)
    d.ellipse((cx - 105, PANEL - 105, cx + 105, PANEL + 105), fill=sp['accent'])
    d.ellipse((cx - 62, PANEL - 70, cx - 22, PANEL - 30), fill=PAPER + (255,))

    y = PANEL + r + 60
    if sp.get('badge'):
        bf = font('inter', 30, SANS_AX)
        bw = d.textlength(sp['badge'].upper(), font=bf) + 6 * len(sp['badge']) + 64
        d.rounded_rectangle((cx - bw / 2, y - 30, cx + bw / 2, y + 30), radius=30, fill=YELLOW)
        spaced(d, cx, y, sp['badge'].upper(), bf, GREEN_DARK, 6)
        y += 92
    lf = font('inter', 40, BODY_AX)
    for ln in sp['lines']:
        lw = d.textlength(ln, font=lf)
        if lw > 1000:
            raise ValueError('line too long: ' + ln)
        d.text((cx, y), ln, font=lf, fill=INK, anchor='mm')
        d.ellipse((cx - lw / 2 - 30, y - 6, cx - lw / 2 - 18, y + 6), fill=YELLOW)
        y += 62

    d.line((300, 1515, 975, 1515), fill=LINE, width=3)
    d.text((cx, 1572), 'Bored of Toast', font=font('fraunces-normal', 44, SUB_AX), fill=GREEN, anchor='mm')
    return im.convert('RGB')


def card(cover_img, h):
    w = round(cover_img.width * h / cover_img.height)
    c = cover_img.resize((w, h), Image.LANCZOS).convert('RGBA')
    ImageDraw.Draw(c).rounded_rectangle((0, 0, w - 1, h - 1), radius=8, outline=LINE + (255,), width=2)
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=8, fill=255)
    c.putalpha(mask)
    return c


def place(canvas, c, cx, cy, angle):
    w, h = c.size
    pad = 70
    layer = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle((pad + 12, pad + 22, pad + 12 + w, pad + 22 + h), radius=10, fill=GREEN_DARK + (95,))
    layer = layer.filter(ImageFilter.GaussianBlur(20))
    layer.alpha_composite(c, (pad, pad))
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


def make_mockup(covers):
    canvas = Image.new('RGBA', (1600, 1200), (0, 0, 0, 0))
    order = [('bonus-3-printable-pack-cover', 1140, 9), ('bonus-2-recipe-pack-vol-2-cover', 990, 4),
             ('bonus-1-28-day-meal-plan-cover', 830, -2), ('nourished-main-guide-cover', 590, -6)]
    for key, cx, ang in order:
        place(canvas, card(covers[key], 760), cx, 600, ang)
    return canvas


def make_pin(mock):
    pin = Image.new('RGBA', (1000, 1500), CREAM + (255,))
    d = ImageDraw.Draw(pin)
    spaced(d, 500, 92, 'SMALL PLATES \u00b7 BIG PROTEIN', font('inter', 26, SANS_AX), GREEN, 5)
    res = fit(d, 'What to cook when your appetite is small', 'fraunces-normal', {'optical': 72, 'weight': 450}, 860, range(86, 59, -4), 3)
    hf, hl, hs = res
    y = 150
    for ln in hl:
        d.text((500, y), ln, font=hf, fill=INK, anchor='mt')
        y += int(hs * 1.1)
    m = mock.resize((1000, 750), Image.LANCZOS)
    pin.alpha_composite(m, (0, max(y - 10, 360)))
    d = ImageDraw.Draw(pin)
    d.rounded_rectangle((60, 1220, 940, 1400), radius=28, fill=GREEN)
    r1 = fit(d, '36 recipes \u00b7 4 weeks of examples \u00b7 US$20', 'inter', SANS_AX, 800, range(40, 25, -2), 1)
    d.text((500, 1282), r1[1][0], font=r1[0], fill=CREAM, anchor='mm')
    d.text((500, 1346), 'Nourished \u00b7 The GLP-1 Kitchen Companion', font=font('fraunces-italic', 34, SUB_AX), fill=YELLOW, anchor='mm')
    d.text((500, 1455), 'Bored of Toast', font=font('fraunces-normal', 36, SUB_AX), fill=GREEN, anchor='mm')
    return pin.convert('RGB')


try:
    files = {}
    covers = {}
    for key, sp in COVERS:
        img = make_cover(sp)
        covers[key] = img
        b = io.BytesIO(); img.save(b, 'PNG', optimize=True); files[key + '.png'] = b.getvalue()
        b = io.BytesIO(); img.save(b, 'PDF', resolution=150); files[key + '.pdf'] = b.getvalue()
    mock = make_mockup(covers)
    b = io.BytesIO(); mock.save(b, 'PNG', optimize=True); files['nourished-bundle-mockup.png'] = b.getvalue()
    flat = Image.new('RGB', mock.size, CREAM2); flat.paste(mock, (0, 0), mock)
    b = io.BytesIO(); flat.save(b, 'JPEG', quality=86, optimize=True, progressive=True); files['nourished-bundle-mockup.jpg'] = b.getvalue()
    pin = make_pin(mock)
    b = io.BytesIO(); pin.save(b, 'JPEG', quality=86, optimize=True, progressive=True); files['pin-nourished-bundle.jpg'] = b.getvalue()
except Exception as ex:
    print(f'ERROR: could not draw the covers ({ex}). Nothing was saved.')
    sys.exit(1)

os.makedirs(OUT, exist_ok=True)
for name, data in files.items():
    open(os.path.join(OUT, name), 'wb').write(data)
    print(f'- {name}: {len(data) // 1024} KB')
open(vf, 'w', encoding='utf-8').write(DESIGN_VERSION + '\n')
print(f'OK: {len(files)} files written to _src/covers/ ({DESIGN_VERSION}). No site page was changed.')
