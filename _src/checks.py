#!/usr/bin/env python3
"""Sanity checks for the generated site. Run from the project root:  python3 _src/checks.py
Standard library only. Exits with status 1 if anything fails (used by .github/workflows/checks.yml).

Checks
  1. every local href / src / srcset target exists
  2. every page: <html lang>, <title>, meta description, exactly one <h1>, <main id="main">, skip link
  3. every <img> has an alt attribute
  4. Recipe JSON-LD parses and has the required fields (incl. nutrition.servingSize, dateModified)
  5. nothing loads from Google Fonts / gstatic (fonts are self-hosted)
  6. image budget: each .webp <= 200 KB; responsive variants match images/variants.json
  7. weight budget: each HTML page <= 80 KB, styles.css <= 80 KB, app.js <= 40 KB
"""
import glob, json, os, re, sys
from html.parser import HTMLParser
from urllib.parse import unquote

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
os.chdir(ROOT)
errors = []
def fail(msg): errors.append(msg)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.imgs, self.h1 = [], [], 0
        self.lang = self.title = self.desc = None
        self.main = self.skip = False
        self.ld, self._ld = [], None
        self._in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'title': self._in_title = True
        if tag == 'meta' and a.get('name') == 'description': self.desc = a.get('content')
        if tag == 'h1': self.h1 += 1
        if tag == 'main' and a.get('id') == 'main': self.main = True
        if tag == 'a' and 'skip-link' in (a.get('class') or ''): self.skip = True
        if tag == 'img': self.imgs.append(a)
        if tag == 'script' and a.get('type') == 'application/ld+json': self._ld = []
        for k in ('href', 'src'):
            if k in a and a[k]: self.refs.append(a[k])
        if a.get('srcset'):
            for part in a['srcset'].split(','):
                u = part.strip().split(' ')[0]
                if u: self.refs.append(u)
    def handle_endtag(self, tag):
        if tag == 'title': self._in_title = False
        if tag == 'script' and self._ld is not None:
            self.ld.append(''.join(self._ld)); self._ld = None
    def handle_data(self, data):
        if self._in_title: self.title = (self.title or '') + data
        if self._ld is not None: self._ld.append(data)

pages = sorted(p for p in glob.glob('**/*.html', recursive=True) if not p.startswith(('_src/', 'node_modules/')))
REDIRECT_STUBS = {'about.html', 'recipes.html', 'recipe.html'}
for path in pages:
    text = open(path, encoding='utf8').read()
    pg = Page(); pg.feed(text)
    stub = path in REDIRECT_STUBS
    # 1) local references
    for ref in pg.refs:
        if re.match(r'^(https?:|mailto:|tel:|javascript:|data:|#|//)', ref) or '{' in ref:
            continue
        target = unquote(ref.split('#')[0].split('?')[0])
        full = os.path.normpath(os.path.join(os.path.dirname(path), target)) if not target.startswith('/') else target.lstrip('/')
        if os.path.isdir(full): full = os.path.join(full, 'index.html')
        if not os.path.exists(full): fail(f'{path}: broken reference {ref}')
    if not stub:
        # 2) page basics
        if not pg.lang: fail(f'{path}: <html> has no lang')
        if not (pg.title or '').strip(): fail(f'{path}: empty <title>')
        if not pg.desc: fail(f'{path}: missing meta description')
        if pg.h1 != 1: fail(f'{path}: expected exactly one <h1>, found {pg.h1}')
        if not pg.main: fail(f'{path}: missing <main id="main">')
        if not pg.skip: fail(f'{path}: missing skip link')
        # 3) alt text
        for im in pg.imgs:
            if 'alt' not in im: fail(f'{path}: <img> without alt: {im.get("src")}')
        # 5) no third-party font hosts
        if re.search(r'fonts\.googleapis|fonts\.gstatic', text): fail(f'{path}: loads Google Fonts')
        # 7) weight
        if len(text.encode()) > 80 * 1024: fail(f'{path}: HTML is {len(text.encode())//1024} KB (budget 80 KB)')
    # 4) Recipe JSON-LD
    for raw in pg.ld:
        try: d = json.loads(raw)
        except ValueError as e: fail(f'{path}: invalid JSON-LD ({e})'); continue
        if d.get('@type') == 'Recipe':
            for k in ('name', 'image', 'author', 'datePublished', 'dateModified', 'recipeIngredient', 'recipeInstructions', 'recipeYield', 'totalTime'):
                if not d.get(k): fail(f'{path}: Recipe JSON-LD missing {k}')
            n = d.get('nutrition') or {}
            for k in ('calories', 'proteinContent', 'servingSize'):
                if not n.get(k): fail(f'{path}: Recipe nutrition missing {k}')

# 5b) css/js
css = open('styles.css', encoding='utf8').read()
if re.search(r'fonts\.googleapis|fonts\.gstatic|@import\s+url', css): fail('styles.css: external @import / Google Fonts')
if len(css.encode()) > 80 * 1024: fail(f'styles.css is {len(css.encode())//1024} KB (budget 80 KB)')
if os.path.getsize('app.js') > 40 * 1024: fail(f'app.js is {os.path.getsize("app.js")//1024} KB (budget 40 KB)')
for f in glob.glob('fonts/*.woff2'):
    pass
for m in re.findall(r'url\((fonts/[^)]+)\)', css):
    if not os.path.exists(m): fail(f'styles.css: missing font file {m}')

# 6) images
VAR = re.compile(r'-\d+w\.webp$')
originals = sorted(p for p in glob.glob('images/*.webp') if not VAR.search(p))
manifest = json.load(open('images/variants.json')) if os.path.exists('images/variants.json') else {}
if not manifest: fail('images/variants.json missing (run python3 _src/make_images.py)')
for p in glob.glob('images/*.webp'):
    kb = os.path.getsize(p) / 1024
    if kb > 200: fail(f'{p}: {kb:.0f} KB (image budget 200 KB)')
for p in originals:
    entry = manifest.get(p)
    if entry is None: fail(f'{p}: not in images/variants.json (run python3 _src/make_images.py)'); continue
    for w in entry['variants']:
        if not os.path.exists(f'{p[:-5]}-{w}w.webp'): fail(f'{p}: variant {w}w listed in manifest but missing')
for k in manifest:
    if not os.path.exists(k): fail(f'manifest lists {k} but the file does not exist')
for p in glob.glob('images/*-*w.webp'):
    base = re.sub(r'-\d+w\.webp$', '.webp', p)
    w = int(re.search(r'-(\d+)w\.webp$', p).group(1))
    if base not in manifest or w not in manifest[base]['variants']:
        fail(f'{p}: variant not registered in images/variants.json (orphan)')

print(f'checked {len(pages)} pages, {len(originals)} photos')
if errors:
    print(f'\n{len(errors)} problem(s):')
    for e in errors[:60]: print(' -', e)
    sys.exit(1)
print('all checks passed')
