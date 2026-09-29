#!/usr/bin/env python3
"""Calibrate the fallback @font-face overrides (size-adjust / ascent / descent) in styles.css.

Why measure in a browser: Fraunces has an optical-size axis, so at heading sizes it is much narrower than
its default instance. We therefore measure the real rendered width of the site's own headings/body copy
in Chromium (with the self-hosted web fonts) and compare it with the advance widths of the reference
fallbacks (Arial / Times New Roman, from the standard Helvetica / Times AFM tables; Liberation Sans/Serif
and Arimo/Tinos are metric-compatible).

    python3 _src/font_metrics.py            # prints the CSS values (needs: playwright + fonttools, site served)
Serve the built site first, e.g.:  (cd _src/site && python3 -m http.server 8804)
"""
import json, os, sys
from fontTools.ttLib import TTFont
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8804/'

# --- reference advance widths (per 1000 em) ---------------------------------------------------------------
def table(lower, upper, digit, punct):
    d = dict(zip('abcdefghijklmnopqrstuvwxyz', lower))
    d.update(dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', upper)))
    d.update({c: digit for c in '0123456789'})
    d.update(punct)
    return d
ARIAL = table(
    [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500],
    [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611],
    556, {' ': 278, '.': 278, ',': 278, ':': 278, '-': 333, '&': 667, '!': 278, '?': 556, '(': 333, ')': 333})
TIMES = table(
    [444,500,444,500,444,333,500,500,278,278,500,278,778,500,500,500,500,333,389,278,500,500,722,500,500,444],
    [722,667,667,722,611,556,722,722,333,389,722,611,889,722,722,556,722,667,556,611,722,722,944,722,722,611],
    500, {' ': 250, '.': 250, ',': 250, ':': 278, '-': 333, '&': 778, '!': 333, '?': 444, '(': 333, ')': 333})
TIMES_I = table(
    [500,500,444,500,444,278,500,500,278,278,444,278,722,500,500,500,500,389,389,278,500,444,667,444,444,389],
    [611,611,667,722,611,611,722,722,333,444,667,556,833,667,722,611,722,611,500,556,722,611,833,611,556,556],
    500, {' ': 250, '.': 250, ',': 250, ':': 333, '-': 333, '&': 778, '!': 333, '?': 500, '(': 333, ')': 333})

def ref_width(text, tab, size):
    return sum(tab[c] for c in text) / 1000 * size

def clean(text, tab):
    return ''.join(c for c in text if c in tab)

# --- sample text from the site itself ---------------------------------------------------------------------
recipes = json.load(open(os.path.join(HERE, 'recipes.json'), encoding='utf8'))
gl = json.load(open(os.path.join(HERE, 'guides_legal.json'), encoding='utf8'))
headings = [r['title'] for r in recipes] + [g['title'] for g in gl['guides']] + [
    "Why you'll love it", 'Tips for success', 'Make it your own', 'Recipe FAQ', 'Browse by category', 'Fresh from our kitchen',
    'Kitchen basics', "Dinner is planned. You're welcome.", 'Sunday prep, 45 minutes']
italics = ['every day.', 'enjoy.', 'not harder.', 'planned.', 'good food.', 'Good.', 'Start here.']
body = [r['desc'] for r in recipes] + [r['subtitle'] for r in recipes if r.get('subtitle')]
body = [b for b in body][:40]

MEASURE = """([texts, fam, size, weight, style]) => texts.map(t => { const s = document.createElement('span');
  s.style.cssText = `position:absolute;visibility:hidden;white-space:nowrap;font-family:${fam};font-size:${size}px;font-weight:${weight};font-style:${style}`;
  s.textContent = t; document.body.appendChild(s); const w = s.getBoundingClientRect().width; s.remove(); return w; })"""

def calibrate(pg, texts, tab, fam, sizes, weight, style):
    texts = [clean(t, tab) for t in texts]; texts = [t for t in texts if t]
    web = ref = 0.0
    for size in sizes:
        ws = pg.evaluate(MEASURE, [texts, fam, size, weight, style])
        web += sum(ws)
        ref += sum(ref_width(t, tab, size) for t in texts)
    return web / ref

def vertical(path):
    f = TTFont(path); upm = f['head'].unitsPerEm; h = f['hhea']
    return h.ascent / upm, -h.descent / upm, h.lineGap / upm

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 900})
    pg.goto(BASE, wait_until='networkidle'); pg.evaluate('document.fonts.ready')
    # make sure each face is really loaded before measuring
    pg.evaluate("Promise.all([document.fonts.load('400 30px Fraunces'), document.fonts.load('italic 400 30px Fraunces'), document.fonts.load('400 16px Inter')])")
    res = {
        'fraunces_normal': calibrate(pg, headings, TIMES, "'Fraunces'", [28, 37, 46, 54], 400, 'normal'),
        'fraunces_italic': calibrate(pg, italics, TIMES_I, "'Fraunces'", [37, 46, 54], 400, 'italic'),
        'inter': calibrate(pg, body, ARIAL, "'Inter'", [15, 16, 17], 400, 'normal'),
    }
    b.close()
fonts = os.path.join(HERE, '..', 'fonts')
out = {}
for key, path in [('fraunces_normal', 'fraunces-normal.woff2'), ('fraunces_italic', 'fraunces-italic.woff2'), ('inter', 'inter.woff2')]:
    a, d, g = vertical(os.path.join(fonts, path)); sa = res[key]
    out[key] = dict(size_adjust=round(sa * 100, 2), ascent=round(a / sa * 100, 2), descent=round(d / sa * 100, 2), gap=round(g / sa * 100, 2))
    print(key, out[key])
json.dump(out, open(os.path.join(HERE, 'font_metrics.json'), 'w'), indent=1)
