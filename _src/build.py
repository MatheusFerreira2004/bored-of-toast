#!/usr/bin/env python3
"""Bored of Toast static site generator.
Content lives in recipes.json and guides_legal.json. Run: python3 build.py
Output goes to ./site (images must already be in ./site/images)."""
import json, os, html, re, datetime, shutil
from storefront import build_storefront, marketing_block, contextual_link, validate_config

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')
SITE_URL = 'https://matheusferreira2004.github.io/bored-of-toast/'   # change when the custom domain is ready
VER = '20261006-journey-1'
EMAIL = 'hello@boredoftoast.com'
INSTAGRAM = '@boredoftoast'
PUBLISHED = '2026-09-28'
MODIFIED = '2026-09-29'   # bump when recipe content changes (Recipe schema dateModified)
GISCUS = None      # e.g. {'repo': 'MatheusFerreira2004/bored-of-toast', 'repo_id': '...', 'category': 'Comments', 'category_id': '...'}
ANALYTICS = None   # e.g. '<script defer data-domain="boredoftoast.com" src="https://plausible.io/js/script.js"></script>'

STOREFRONT = validate_config(json.load(open(os.path.join(HERE, 'storefront.json'))))

RECIPES = json.load(open(os.path.join(HERE, 'recipes.json')))
CREDITS = json.load(open(os.path.join(HERE, 'credits.json')))
GL = json.load(open(os.path.join(HERE, 'guides_legal.json')))
GUIDES = GL['guides']
BY_ID = {r['id']: r for r in RECIPES}

# Responsive images: _src/make_images.py writes images/<name>-<w>w.webp and images/variants.json.
try:
    VARIANTS = json.load(open(os.path.join(HERE, '..', 'images', 'variants.json')))
except FileNotFoundError:
    VARIANTS = {}
# `sizes` per layout slot, from the rendered widths measured at 360-1440px viewports.
SIZES = {
    'avatar': '52px', 'mini': '58px', 'credit': '72px',
    'plan': '(max-width: 520px) 90vw, (max-width: 700px) 110px, 160px',
    'circle': '(max-width: 520px) 88px, (max-width: 760px) 116px, 140px',
    'card': '(max-width: 520px) calc(100vw - 50px), (max-width: 700px) 264px, (max-width: 900px) 350px, (max-width: 1100px) 480px, 366px',
    'guide': '(max-width: 520px) calc(100vw - 50px), (max-width: 700px) 262px, 366px',
    'spot': '(max-width: 900px) calc(100vw - 48px), 640px',
    'step': '(max-width: 1080px) calc(100vw - 110px), 668px',
    'arch': '(max-width: 960px) min(78vw, 340px), 344px',
    'story': '(max-width: 900px) calc(100vw - 48px), 500px',
    'cover': '(max-width: 1000px) calc(100vw - 48px), 952px',
    'bleed': '(max-width: 960px) 100vw, 52vw',
    'cta': '(max-width: 900px) calc(100vw - 48px), 640px',
}

def rimg(root, path, sizes):
    """srcset + sizes attributes for images/<name>.webp when responsive variants exist (else nothing)."""
    v = VARIANTS.get(path)
    if not v or not v['variants']:
        return ''
    parts = [f"{root}{path[:-5]}-{w}w.webp {w}w" for w in v['variants']] + [f"{root}{path} {v['width']}w"]
    return f' srcset="{", ".join(parts)}" sizes="{sizes}"'

def thumb(path):
    """Smallest variant for tiny thumbnails (search overlay)."""
    v = VARIANTS.get(path)
    return f"{path[:-5]}-{v['variants'][0]}w.webp" if v and v['variants'] else path
GUIDE_IMG = {'pantry-staples': 'guide-pantry', 'perfect-rice': 'guide-rice', 'knife-skills': 'guide-knife'}
GUIDE_RELATED = {'pantry-staples': ['tomato-basil-soup', 'creamy-garlic-pasta', 'mediterranean-grain-bowl'],
                 'perfect-rice': ['honey-garlic-chicken-thighs', 'mushroom-risotto', 'beef-tacos'],
                 'knife-skills': ['shakshuka', 'lemon-chicken-orzo-soup', 'harvest-kale-salad']}
NEW_IDS = ['buttermilk-pancakes', 'shakshuka', 'butternut-squash-soup', 'honey-garlic-chicken-thighs', 'avocado-toast-jammy-eggs', 'mushroom-risotto', 'apple-crisp', 'lemon-chicken-orzo-soup']

CATS = [
    ('Beyond Toast', 'Beyond Toast', 'buttermilk-pancakes'),
    ('Main Dishes', 'Main Dishes', 'honey-garlic-chicken-thighs'),
    ('Salads', 'Salads', 'harvest-kale-salad'),
    ('Soups', 'Soups', 'butternut-squash-soup'),
    ('Desserts', 'Desserts', 'apple-crisp'),
    ('quick', 'Quick & Easy', 'creamy-garlic-pasta'),
    ('healthy', 'Healthy', 'mediterranean-grain-bowl'),
]
DIET = {'vegetarian': ('V', 'Vegetarian'), 'vegan': ('VG', 'Vegan'), 'gluten-free': ('GF', 'Gluten-free'), 'dairy-free': ('DF', 'Dairy-free')}
SCHEMA_DIET = {'vegetarian': 'https://schema.org/VegetarianDiet', 'vegan': 'https://schema.org/VeganDiet', 'gluten-free': 'https://schema.org/GlutenFreeDiet'}

e = lambda s: html.escape(str(s), quote=True)

def fmt_time(m):
    if m < 60: return f'{m} min'
    h, mm = divmod(m, 60)
    return f'{h} h {mm} min' if mm else f'{h} h'

def iso(m): return f'PT{m // 60}H{m % 60}M' if m >= 60 else f'PT{m}M'

def fmt_qty(q):
    if q is None: return ''
    whole = int(q + 0.01); frac = q - whole
    if frac < 0.07: return str(whole)
    if frac > 0.9: return str(whole + 1)
    m = [(0.125, '⅛'), (0.25, '¼'), (0.33, '⅓'), (0.5, '½'), (0.67, '⅔'), (0.75, '¾')]
    v, s = min(m, key=lambda t: abs(frac - t[0]))
    if abs(frac - v) > 0.08: return str(round(q, 1))
    return (f'{whole} ' if whole else '') + s

def ing_text(i):
    q = fmt_qty(i.get('q'))
    s = (f"{q} {i['u']} ".replace('  ', ' ') if q else '') + i['n']
    return s.strip() + (f" ({i['note']})" if i.get('note') else '')

ICON = {
 'clock': '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 'chef': '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 13.9A4 4 0 0 1 7 6a5 5 0 0 1 10 0 4 4 0 0 1 1 7.9V20H6z"/><path d="M6 17h12"/></svg>',
 'users': '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/></svg>',
 'arrow': '<svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'down': '<svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
 'search': '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
 'bag': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
 'menu': '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
 'print': '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 9V3h12v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/></svg>',
 'share': '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>',
 'pin': '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.3-5.4s-.3-.7-.3-1.6c0-1.5.9-2.7 2-2.7.9 0 1.4.7 1.4 1.6 0 1-.6 2.4-.9 3.7-.3 1.1.6 2 1.7 2 2 0 3.5-2.1 3.5-5.2 0-2.7-2-4.6-4.8-4.6-3.3 0-5.2 2.5-5.2 5 0 1 .4 2.1.9 2.7.1.1.1.2.1.3l-.3 1.3c-.1.2-.2.3-.4.2-1.5-.7-2.4-2.8-2.4-4.6 0-3.7 2.7-7.2 7.9-7.2 4.1 0 7.3 3 7.3 6.9 0 4.1-2.6 7.4-6.2 7.4-1.2 0-2.4-.6-2.8-1.4l-.8 2.9c-.3 1.1-1 2.4-1.5 3.2A10 10 0 1 0 12 2z"/></svg>',
 'bulb': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/></svg>',
 'box': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M3 7l9-4 9 4-9 4z"/><path d="M3 7v10l9 4 9-4V7M12 11v10"/></svg>',
 'swap': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M7 4 3 8l4 4M3 8h14M17 20l4-4-4-4M21 16H7"/></svg>',
 'check': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="m5 12 5 5L20 7"/></svg>',
 'heart': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
 'bolt': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
 'sun': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 'book': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/></svg>',
 'leaf': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M20 4C10 4 5 9 5 16c0 1.5.3 2.8.8 4"/><path d="M20 4c0 10-5 15-12 15"/><path d="M5 20 13 12"/></svg>',
 'up': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
 'x': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>',
 'instagram': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 'facebook': '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/></svg>',
 'youtube': '<svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12a31 31 0 0 0 .4 3.8 3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-3.8 31 31 0 0 0-.4-3.8zM10 15.1V8.9l5.2 3.1z"/></svg>',
}
WHY_ICONS = [ICON['bolt'], ICON['heart'], ICON['check']]
WAVE = '<svg class="hero-wave" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 40c160 30 320 30 480 10s320-40 480-20 320 40 480 20v20H0z"/></svg>'

# ---------------------------------------------------------------- layout
NAV = [('', 'Home', 'home'), ('recipes/', 'Recipes', 'recipes'), ('guides/', 'Guides', 'guides'), ('meal-plan/', '5 Easy Dinners', 'meal-plan'), ('nourished/', 'Cookbook', 'cookbooks'), ('about/', 'About', 'about')]

def header(root, active):
    links = ''.join(f'<a href="{root}{h}" class="{"active" if k == active else ""}">{l}</a>' for h, l, k in NAV)
    return f'''<header class="site-header" id="site-header">
  <div class="container">
    <a href="{root}" class="brand" aria-label="Bored of Toast home"><img src="{root}images/logo-white.png" alt="Bored of Toast" width="128" height="46"></a>
    <nav class="nav" id="nav" aria-label="Main">{links}</nav>
    <div class="nav-tools">
      <button class="icon-btn" data-open-search aria-label="Search recipes">{ICON['search']}</button>
      <a class="icon-btn" href="{root}shopping-list/" aria-label="Shopping list">{ICON['bag']}<span class="bag-count" data-bag-count hidden>0</span></a>
      <button class="icon-btn menu-toggle" id="menu-toggle" aria-label="Open menu" aria-controls="nav" aria-expanded="false">{ICON['menu']}</button>
    </div>
  </div>
</header>'''

def footer(root):
    cats = ''.join(f'<li><a href="{root}recipes/?cat={e(k)}">{l}</a></li>' for k, l, _ in CATS[:6])
    nav = ''.join(f'<li><a href="{root}{h}">{l}</a></li>' for h, l, _ in NAV)
    nav += f'<li><a href="{root}starter-kit/">Free GLP-1 kit</a></li>'
    socials = ''.join(f'<a href="{e(url)}" aria-label="{name.title()}" target="_blank" rel="noopener">{ICON["pin" if name == "pinterest" else name]}</a>' for name,url in STOREFRONT.get('social_urls', {}).items() if url)
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <a href="{root}" class="brand" aria-label="Bored of Toast home"><img src="{root}images/logo-white.png" alt="Bored of Toast" width="150" height="54" loading="lazy"></a>
      <p class="footer-tagline">Good food without the fuss. Simple, tested recipes for real life.</p>
      {f'<div class="socials">{socials}</div>' if socials else ''}
    </div>
    <div><p class="fh">Explore</p><ul>{nav}</ul></div>
    <div><p class="fh">Recipes</p><ul>{cats}</ul></div>
    <div class="footer-cta"><p class="fh">Can't decide?</p><p>Let us pick something delicious for you.</p><button class="btn btn-yellow" data-random>Surprise me {ICON['arrow']}</button></div>
  </div>
  <div class="container footer-bottom">
    <span>© {datetime.date.today().year} Bored of Toast. All rights reserved.</span>
    <span><a href="{root}privacy/">Privacy</a> · <a href="{root}terms/">Terms</a> · <a href="{root}photo-credits/">Photo credits</a> · <a href="{root}sitemap.xml">Sitemap</a></span>
  </div>
</footer>
<div class="search-overlay" id="search-overlay" hidden>
  <div class="search-panel" role="dialog" aria-modal="true" aria-label="Search">
    <div class="search-field">{ICON['search']}<input type="search" id="search-input" placeholder="Search recipes, ingredients or guides…" autocomplete="off"><button class="icon-btn" data-close-search aria-label="Close search">{ICON['x']}</button></div>
    <div class="search-results" id="search-results"></div>
  </div>
</div>
<button class="to-top no-print" aria-label="Back to top">{ICON['up']}</button>
<div class="toast-msg" id="toast-msg" role="status" aria-live="polite"></div>'''

def page(path, title, desc, body, active='', root='', og='images/og/home.jpg', jsonld=None, head_extra='', body_attr=''):
    canonical = SITE_URL + path
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:site_name" content="Bored of Toast">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}{og}">
  <meta property="og:type" content="{'article' if jsonld else 'website'}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#3f5130">
  <link rel="icon" href="{root}images/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="{root}images/favicon.png">
  <script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__botReady)document.documentElement.classList.add('js-fallback')}},4000)</script>
  <link rel="stylesheet" href="{root}styles.css?v={VER}">
  {ld}{head_extra}{ANALYTICS or ''}
</head>
<body data-root="{root}" data-page="{active}" {body_attr}>
<a class="skip-link" href="#main">Skip to content</a>
{header(root, active)}
<main id="main">
{body}
</main>
{footer(root)}
<script src="{root}search-index.js?v={VER}"></script>
<script src="{root}app.js?v={VER}"></script>
</body>
</html>'''
    doc = '\n'.join(line.rstrip() for line in doc.split('\n'))
    full = os.path.join(OUT, path, 'index.html') if (path == '' or path.endswith('/')) else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(doc)

def stamp(root):
    return f'''<div class="stamp" aria-hidden="true"><svg class="ring" viewBox="0 0 120 120"><defs><path id="circ" d="M60 60m-48 0a48 48 0 1 1 96 0a48 48 0 1 1-96 0"/></defs><text font-family="Inter, sans-serif" font-size="11.5" font-weight="600" letter-spacing="3.2" fill="#f7f2e7"><textPath href="#circ">GOOD FOOD • NO FUSS • TESTED AT HOME •</textPath></text></svg><div class="stamp-core"><img src="{root}images/favicon.png" alt=""></div></div>'''

def hero_bleed(root, img, eyebrow, h1, p, actions='', card='', short=False, trust=''):
    return f'''<section class="hero hero-bleed{' hero-short' if short else ''}">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="hero-lead">{p}</p>
      {f'<div class="hero-actions">{actions}</div>' if actions else ''}
      {trust}
    </div>
    <div class="hero-art art-bleed"><div class="bleed-img" aria-hidden="true"><img src="{root}{img}" alt="" decoding="async"{rimg(root, img, SIZES['bleed'])}></div>{card}</div>
  </div>
  {WAVE}
</section>'''

def float_card(root, r, label):
    return f'''<a class="float-card" href="{root}recipes/{r['id']}/"><img src="{root}{r['img']}" alt="" width="52" height="52"{rimg(root, r['img'], SIZES['avatar'])}><div><small>{label}</small><strong>{e(r['title'])}</strong><span>{fmt_time(r['time'])} · {r['level']}</span></div></a>'''

def diet_badges(r, cls='diet-badges'):
    if not r.get('diet'): return ''
    return f'<span class="{cls}">' + ''.join(f'<span class="diet" title="{DIET[d][1]}">{DIET[d][0]}</span>' for d in r['diet'] if d in DIET) + '</span>'

def card(root, r, desc=True, eager=False):
    text = ' '.join([r['title'], r['desc'], r['category']] + [i['n'] for g in r['ingredients'] for i in g['items']]).lower()
    return f'''<a class="card reveal" href="{root}recipes/{r['id']}/" data-cat="{e(r['category'])}" data-tags="{' '.join(r['tags'])}" data-diet="{' '.join(r.get('diet', []))}" data-text="{e(text)}">
  <div class="card-img"><img src="{root}{r['img']}" alt="{e(r['title'])}" width="600" height="450" {'' if eager else 'loading="lazy"'} decoding="async"{rimg(root, r['img'], SIZES['card'])}><span class="card-badge">{e(r['category'])}</span>{diet_badges(r)}</div>
  <div class="card-body"><h3>{e(r['title'])}</h3>{f'<p class="desc">{e(r["desc"])}</p>' if desc else ''}
    <div class="meta"><span>{ICON['clock']}{fmt_time(r['time'])}</span><span>{ICON['chef']}{r['level']}</span></div></div>
</a>'''

def guide_card(root, g):
    return f'''<a class="guide-card reveal" href="{root}guides/{g['id']}/">
  <div class="guide-img"><img src="{root}images/{GUIDE_IMG[g['id']]}.webp" alt="{e(g['title'])}" loading="lazy" width="700" height="466"{rimg(root, 'images/' + GUIDE_IMG[g['id']] + '.webp', SIZES['guide'])}></div>
  <div class="guide-body"><span class="tag">{e(g['category'])} · {g['readTime']} min read</span><h3>{e(g['title'])}</h3><p>{e(g['subtitle'])}</p><span class="view-all">Read the guide →</span></div>
</a>'''

def credit(key):
    c = CREDITS.get(key)
    if not c: return ''
    return f'<p class="photo-credit">Photo: <a href="{e(c['photo_url'])}" target="_blank" rel="noopener">{e(c['photographer'])}</a> on {c['source']}</p>'

def section_head(title, sub='', link=''):
    return f'<div class="section-head"><div><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>{link}</div>'

def count(key): return sum(1 for r in RECIPES if r['category'] == key or key in r['tags'])

def cats_grid(root):
    return '<div class="categories">' + ''.join(f'''<a class="category reveal" href="{root}recipes/?cat={e(k)}"><div class="circle"><img src="{root}images/{img}.webp" alt="{l}" loading="lazy" width="150" height="150"{rimg(root, 'images/' + img + '.webp', SIZES['circle'])}></div>{l}<small>{count(k)} recipes</small></a>''' for k, l, img in CATS) + '</div>'

# ---------------------------------------------------------------- pages
def build_home():
    root = ''
    wk = BY_ID['creamy-garlic-pasta']
    trust = '<div class="hero-trust">' + ''.join(f'<span>{ICON["check"]}{t}</span>' for t in ['Tested at home', 'Everyday ingredients', 'Step-by-step guides']) + '</div>'
    hero = hero_bleed(root, 'images/avocado-toast-jammy-eggs.webp', 'Recipes · Tips · Inspiration', 'Good food,<br><em>every day.</em>',
        'Simple, delicious recipes made for real life: easy enough for a weekday, special enough for the weekend.',
        f'<a href="{root}recipes/" class="btn btn-yellow">Explore recipes {ICON["arrow"]}</a><button class="btn btn-ghost" data-random>Surprise me</button>',
        float_card(root, wk, 'Recipe of the week'), trust=trust)
    words = ['Fresh ingredients', 'Simple steps', 'Better breakfasts', 'Weeknight dinners', 'Cozy soups', 'Sweet treats', 'No fuss']
    marquee = '<div class="marquee" aria-hidden="true"><div class="marquee-track">' + ''.join(f'<span>{w}</span>' for w in words * 2) + '</div></div>'
    bt = [BY_ID[i] for i in ['buttermilk-pancakes', 'shakshuka', 'avocado-toast-jammy-eggs', 'overnight-oats']]
    fall = [r for r in RECIPES if 'fall' in r['tags']][:4]
    latest = [BY_ID[i] for i in NEW_IDS]
    ing = [i['n'].split(',')[0] for g in wk['ingredients'] for i in g['items'] if i.get('q') is not None][:5]
    body = f'''{hero}{marquee}
<section class="container section" style="padding-bottom:24px">
  {section_head('Browse by category', 'From ten-minute breakfasts to weekend baking projects.', f'<a href="{root}recipes/" class="view-all">All recipes →</a>')}
  {cats_grid(root)}
</section>
{marketing_block(root, 'free')}

<section class="section">
  <div class="container beyond">
    <div class="beyond-copy reveal">
      <span class="tag">Our signature category</span>
      <h2>Bored of toast?<br><em>Good.</em> Start here.</h2>
      <p>Breakfast deserves better than the same slice every morning. Fluffy pancakes, eggs baked in spicy tomato sauce, oats that make themselves overnight, and yes, avocado toast done properly.</p>
      <a href="{root}recipes/?cat=Beyond%20Toast" class="btn btn-dark">See all breakfast recipes {ICON['arrow']}</a>
    </div>
    <div class="beyond-grid">{''.join(card(root, r, desc=False) for r in bt)}</div>
  </div>
</section>

<section class="container section">
  {section_head('Fresh from our kitchen', 'The newest recipes, tested and ready for yours.', f'<a href="{root}recipes/" class="view-all">View all →</a>')}
  <div class="recipe-grid four">{''.join(card(root, r) for r in latest)}</div>
</section>

<section class="section seasonal">
  <div class="container">
    {section_head('Fall favorites <span class="season-leaf">' + ICON['leaf'] + '</span>', 'Cozy, golden and made for sweater weather.', f'<a href="{root}recipes/?cat=fall" class="view-all">All fall recipes →</a>')}
    <div class="recipe-grid four">{''.join(card(root, r) for r in fall)}</div>
  </div>
</section>

<section class="container section">
  <div class="spotlight reveal">
    <div class="spotlight-img"><img src="{root}{wk['img']}" alt="{e(wk['title'])}" loading="lazy"{rimg(root, wk['img'], SIZES['spot'])}><span class="ribbon">Recipe of the week</span></div>
    <div class="spotlight-body">
      <span class="tag">{wk['category']}</span><h2>{e(wk['title'])}</h2><p>{e(wk['subtitle'])}</p>
      <div class="meta" style="margin-bottom:18px"><span>{ICON['clock']}{fmt_time(wk['time'])}</span><span>{ICON['chef']}{wk['level']}</span><span>{ICON['users']}Serves {wk['serves']}</span></div>
      <div class="pills">{''.join(f'<span class="pill">{e(i)}</span>' for i in ing)}</div>
      <div><a href="{root}recipes/{wk['id']}/" class="btn btn-dark">Get the recipe {ICON['arrow']}</a></div>
    </div>
  </div>
</section>

<section class="section bg-paper">
  <div class="container">
    {section_head('Kitchen basics', 'Short, practical guides that make every recipe easier.', f'<a href="{root}guides/" class="view-all">All guides →</a>')}
    <div class="guide-grid">{''.join(guide_card(root, g) for g in GUIDES)}</div>
  </div>
</section>

{marketing_block(root, 'paid')}
<section class="container section">
  <div class="cta reveal">
    <div><span class="tag light">5 easy dinners</span><h2>Less deciding.<br>More cooking.</h2><p>Five dinner ideas, clear recipes and ingredients you can save to your shopping list.</p></div>
    <a href="{root}meal-plan/" class="btn btn-yellow">Explore the five dinners {ICON['arrow']}</a>
  </div>
</section>'''
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": "Bored of Toast", "url": SITE_URL,
           "potentialAction": {"@type": "SearchAction", "target": SITE_URL + "recipes/?q={search_term_string}", "query-input": "required name=search_term_string"}}]
    page('', 'Bored of Toast | Good food, every day', 'Simple, delicious, tested recipes made for real life: easy enough for a weekday, special enough for the weekend.', body, 'home', root, jsonld=ld)

def build_recipes():
    root = '../'
    pick = BY_ID['mediterranean-grain-bowl']
    hero = hero_bleed(root, 'images/mediterranean-grain-bowl.webp', 'The recipe library', 'Explore, cook,<br><em>enjoy.</em>',
        f'{len(RECIPES)} tested recipes for every kind of day, each with step-by-step instructions, tips, swaps and storage notes.',
        f'<button class="btn btn-yellow" data-random>Pick one for me {ICON["arrow"]}</button>', float_card(root, pick, "Editor's pick"), short=True)
    chips = [('all', 'All')] + [(k, l) for k, l, _ in CATS] + [('fall', 'Fall')]
    diets = [('vegetarian', 'Vegetarian'), ('gluten-free', 'Gluten-free'), ('dairy-free', 'Dairy-free')]
    body = f'''{hero}
<div class="container">
  <div class="toolbar">
    <div class="search"><input type="search" id="list-search" placeholder="Search recipes or ingredients…" aria-label="Search recipes">{ICON['search']}</div>
    <div class="chips" id="chips">{''.join(f'<button class="chip" data-key="{e(k)}">{l}</button>' for k, l in chips)}</div>
    <div class="chips diet-chips" id="diet-chips"><span class="chips-label">Diet:</span>{''.join(f'<button class="chip chip-diet" data-diet="{k}"><span class="diet">{DIET[k][0]}</span>{l}</button>' for k, l in diets)}</div>
  </div>
  <h2 class="sr-only">All recipes</h2>
  <p class="results-count" id="results-count"></p>
  <div class="recipe-grid" id="recipe-grid">{''.join(card(root, r, eager=i < 4) for i, r in enumerate(RECIPES))}</div>
  <div class="empty" id="empty"><p>No recipes match those filters yet.</p><button class="btn btn-outline" id="clear-filters">Clear filters</button></div>
  <div class="cta reveal" style="margin-top:72px"><div><h2>Can't decide what to cook?</h2><p>Let us pick a recipe for you. No scrolling required.</p></div><button class="btn btn-yellow" data-random>Surprise me {ICON['arrow']}</button></div>
</div>'''
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE_URL}recipes/{r['id']}/"} for i, r in enumerate(RECIPES)]}]
    page('recipes/', 'All Recipes | Bored of Toast', f'Browse {len(RECIPES)} simple, tested recipes: breakfasts, weeknight dinners, soups, salads and desserts.', body, 'recipes', root, jsonld=ld)

def recipe_ld(r):
    ings = [ing_text(i) for g in r['ingredients'] for i in g['items']]
    steps = []
    for n, s in enumerate(r['steps'], 1):
        st = {"@type": "HowToStep", "name": s['t'], "text": s['d'], "url": f"{SITE_URL}recipes/{r['id']}/#step-{n}"}
        if s.get('img'): st['image'] = SITE_URL + s['img']
        steps.append(st)
    n = r['nutrition']
    ld = {"@context": "https://schema.org", "@type": "Recipe", "name": r['title'], "description": r['subtitle'],
          "image": [f"{SITE_URL}images/og/{r['id']}.jpg", f"{SITE_URL}images/pins/{r['id']}.jpg", SITE_URL + r['img']],
          "author": {"@type": "Organization", "name": "Bored of Toast", "url": SITE_URL},
          "publisher": {"@type": "Organization", "name": "Bored of Toast", "logo": {"@type": "ImageObject", "url": SITE_URL + "images/logo.png"}},
          "datePublished": PUBLISHED, "dateModified": MODIFIED, "prepTime": iso(r['prep']), "cookTime": iso(r['cook'] + r.get('chill', 0)), "totalTime": iso(r['time']),
          "recipeYield": f"{r['serves']} {r.get('servesLabel', 'servings')}", "recipeCategory": r['category'], "recipeCuisine": "American",
          "keywords": ', '.join([r['category']] + r['tags'] + r.get('diet', [])),
          "nutrition": {"@type": "NutritionInformation", "calories": f"{n['calories']} calories", "proteinContent": f"{n['protein']} g",
                        "carbohydrateContent": f"{n['carbs']} g", "fatContent": f"{n['fat']} g", "fiberContent": f"{n['fiber']} g", "servingSize": "1 " + r.get('servesLabel', 'serving').rstrip('s')},
          "recipeIngredient": ings, "recipeInstructions": steps}
    sd = [SCHEMA_DIET[d] for d in r.get('diet', []) if d in SCHEMA_DIET]
    if sd: ld['suitableForDiet'] = sd
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL},
        {"@type": "ListItem", "position": 2, "name": "Recipes", "item": SITE_URL + "recipes/"},
        {"@type": "ListItem", "position": 3, "name": r['title'], "item": f"{SITE_URL}recipes/{r['id']}/"}]}
    return [ld, crumbs]

def build_recipe(r):
    root = '../../'
    url = f"{SITE_URL}recipes/{r['id']}/"
    unit = r.get('servesLabel', 'servings')
    related = sorted([x for x in RECIPES if x['id'] != r['id']], key=lambda x: (x['category'] != r['category'], 'fall' not in x['tags'] if 'fall' in r['tags'] else 0))[:3]
    n = r['nutrition']
    tagline = ' · '.join([r['category']] + (['Quick & Easy'] if 'quick' in r['tags'] else []) + (['Healthy'] if 'healthy' in r['tags'] else []) + (['Fall'] if 'fall' in r['tags'] else []))
    pin_url = f"https://www.pinterest.com/pin/create/button/?url={url}&media={SITE_URL}images/pins/{r['id']}.jpg&description={html.escape(r['title'] + ' | Bored of Toast')}"
    groups = ''.join(f'''<div class="ing-group"><h3>{e(g['group'])}</h3><ul class="ing-list">{''.join(f'<li><label><input type="checkbox"><span>{"<b>" + e(fmt_qty(i["q"]) + (" " + i["u"] if i["u"] else "")) + "</b> " if i.get("q") is not None else ""}{e(i["n"])}{f" <em>({e(i["note"])})</em>" if i.get("note") else ""}</span></label></li>' for i in g['items'])}</ul></div>''' for g in r['ingredients'])
    steps = ''.join(f'''<li class="step" id="step-{k}"><div class="step-num" role="button" tabindex="0" aria-label="Mark step {k} done">{k}</div><div class="step-body"><h3>{e(s['t'])}</h3><p>{e(s['d'])}</p>{f'<figure class="step-img"><img src="{root}{s["img"]}" alt="{e(s["t"])}" loading="lazy" width="1200" height="800"{rimg(root, s["img"], SIZES["step"])}></figure>' if s.get('img') else ''}{f'<div class="step-tip">{ICON["bulb"]}<div><strong>Tip:</strong> {e(s["tip"])}</div></div>' if s.get('tip') else ''}</div></li>''' for k, s in enumerate(r['steps'], 1))
    video = f'<section class="reveal"><h2>Watch how it\'s made</h2><div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{e(r["video"])}" title="{e(r["title"])} video" loading="lazy" allowfullscreen></iframe></div></section>' if r.get('video') else ''
    comments = ''
    if GISCUS:
        comments = f'''<section class="reveal"><h2>Comments & reviews</h2><script src="https://giscus.app/client.js" data-repo="{GISCUS['repo']}" data-repo-id="{GISCUS['repo_id']}" data-category="{GISCUS['category']}" data-category-id="{GISCUS['category_id']}" data-mapping="pathname" data-reactions-enabled="1" data-emit-metadata="0" data-input-position="top" data-theme="light" data-lang="en" crossorigin="anonymous" async></script></section>'''
    rdata = {'id': r['id'], 'title': r['title'], 'serves': r['serves'], 'unit': unit, 'ingredients': r['ingredients'], 'url': f"recipes/{r['id']}/"}
    body = f'''<section class="hero recipe-hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{root}">Home</a> / <a href="{root}recipes/">Recipes</a> / <a href="{root}recipes/?cat={e(r['category'])}">{e(r['category'])}</a></nav>
      <p class="eyebrow">{e(tagline)}</p>
      <h1>{e(r['title'])}</h1>
      <p class="hero-lead">{e(r['subtitle'])}</p>
      {diet_badges(r, 'diet-badges hero-diets')}
      <div class="recipe-facts">
        <div><small>Prep</small><strong>{fmt_time(r['prep'])}</strong></div>
        <div><small>{'Cook + chill' if r.get('chill') else 'Cook'}</small><strong>{fmt_time(r['cook'] + r.get('chill', 0))}</strong></div>
        <div><small>Total</small><strong>{fmt_time(r['time'])}</strong></div>
        <div><small>{'Makes' if r.get('servesLabel') else 'Serves'}</small><strong>{r['serves']}</strong></div>
      </div>
      <div class="hero-actions no-print">
        <a href="#ingredients" class="btn btn-yellow">Jump to recipe {ICON['down']}</a>
        <a href="{e(pin_url)}" target="_blank" rel="noopener" class="btn btn-pin">{ICON['pin']} Save</a>
        <button class="btn btn-ghost" data-print aria-label="Print recipe">{ICON['print']}<span class="btn-label"> Print</span></button>
      </div>
    </div>
    <div class="hero-art">
      <div class="arch"><img src="{root}{r['img']}" alt="{e(r['title'])}" width="360" height="440" fetchpriority="high"{rimg(root, r['img'], SIZES['arch'])}></div>
      {credit(r['id'])}
      {stamp(root)}
      <img src="{root}images/whisk.svg" alt="" class="doodle whisk"><img src="{root}images/sparkle.svg" alt="" class="doodle sparkle"><img src="{root}images/chili.svg" alt="" class="doodle chili">
    </div>
  </div>
  {WAVE}
</section>
<img src="{root}images/pins/{r['id']}.jpg" data-pin-media data-pin-description="{e(r['title'] + ': ' + r['subtitle'])}" alt="{e(r['title'])} recipe pin" class="pin-hidden" loading="lazy" width="1000" height="1500">

<div class="container section">
  <div class="recipe-layout">
    <article class="recipe-main">
      <div class="kitchen-note reveal"><span class="hand">From our kitchen</span><p>{e(r['note'])}</p><span class="sig">The Bored of Toast kitchen ♥</span></div>
      <section class="lead reveal no-print">{''.join(f'<p>{e(p)}</p>' for p in r['intro'])}</section>
      <section class="reveal no-print"><h2>Why you'll love it</h2><div class="why-grid">{''.join(f'<div class="why-card"><div class="icon-circle">{WHY_ICONS[i % 3]}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(r['why']))}</div></section>

      <section id="ingredients" class="ingredients-card reveal">
        <div class="ing-head">
          <h2>Ingredients</h2>
          <div class="ing-controls no-print">
            <div class="seg" role="group" aria-label="Units"><button class="active" data-units="us">US</button><button data-units="metric">Metric</button></div>
            <div class="scaler"><button data-step="-1" aria-label="Fewer">−</button><span id="serves-label">{r['serves']} {e(unit)}</span><button data-step="1" aria-label="More">+</button></div>
          </div>
        </div>
        <p class="print-only" id="print-serves">{r['serves']} {e(unit)} · US measurements</p>
        <p class="ing-note no-print">Tap an ingredient to check it off as you go.</p>
        <div id="ing-groups">{groups}</div>
        <div class="ing-actions no-print">
          <button class="btn btn-dark" id="add-to-list">{ICON['bag']} Add to shopping list</button>
          <button class="btn btn-outline" id="cook-mode" aria-pressed="false">{ICON['sun']} Cook mode: off</button>
        </div>
        <p class="cook-hint no-print">Cook mode keeps your screen awake while you cook.</p>
      </section>

      <section id="method" class="reveal">
        <h2>Instructions</h2>
        <p class="hint no-print">Tap a step number to mark it as done.</p>
        <ol class="steps">{steps}</ol>
      </section>
      {video}
      <section class="callout reveal"><h2>Tips for success</h2><ul>{''.join(f'<li>{e(t)}</li>' for t in r['tips'])}</ul></section>
      <section class="reveal"><h2>Make it your own</h2><div class="two-col">
        <div class="info-card"><h3>{ICON['swap']} Variations</h3><div class="variation-list">{''.join(f'<div class="variation"><div class="icon-circle">{ICON["check"]}</div><div><strong>{e(t)}</strong><span>{e(d)}</span></div></div>' for t, d in r['variations'])}</div></div>
        <div class="info-card"><h3>{ICON['box']} Storage & reheating</h3><p>{e(r['storage'])}</p></div>
      </div></section>
      <section class="faq reveal"><h2>Recipe FAQ</h2>{''.join(f'<details {"open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(r['faq']))}</section>
      {contextual_link(root) if r['id'] in ['overnight-oats', 'tomato-basil-soup', 'lemon-chicken-orzo-soup', 'mediterranean-grain-bowl', 'chicken-avocado-salad'] else ''}
      {comments}
    </article>

    <aside class="sidebar">
      <div class="side-card"><h3>At a glance</h3><div class="glance">
        <div><small>Total time</small><strong>{fmt_time(r['time'])}</strong></div><div><small>Difficulty</small><strong>{r['level']}</strong></div>
        <div><small>{'Makes' if r.get('servesLabel') else 'Serves'}</small><strong>{r['serves']} {e(r.get('servesLabel', ''))}</strong></div><div><small>Category</small><strong>{e(r['category'])}</strong></div>
      </div>{f'<div class="glance-diets">' + ''.join(f'<span class="diet-pill"><span class="diet">{DIET[d][0]}</span>{DIET[d][1]}</span>' for d in r.get('diet', []) if d in DIET) + '</div>' if r.get('diet') else ''}</div>
      <div class="side-card side-toc no-print"><h3>On this page</h3><a href="#ingredients">Ingredients <span>→</span></a><a href="#method">Instructions <span>→</span></a><a href="#nutrition">Nutrition <span>→</span></a></div>
      <div class="side-card" id="nutrition"><h3>Nutrition</h3>
        <div class="nutrition-row"><span>Calories</span><b>{n['calories']} kcal</b></div><div class="nutrition-row"><span>Protein</span><b>{n['protein']} g</b></div>
        <div class="nutrition-row"><span>Carbohydrates</span><b>{n['carbs']} g</b></div><div class="nutrition-row"><span>Fat</span><b>{n['fat']} g</b></div>
        <div class="nutrition-row"><span>Fiber</span><b>{n['fiber']} g</b></div>
        <p class="fine">Per {'item' if r.get('servesLabel') else 'serving'}. Estimated values, for reference only.</p></div>
      <div class="side-card side-actions no-print">
        <a class="btn btn-pin" href="{e(pin_url)}" target="_blank" rel="noopener">{ICON['pin']} Save to Pinterest</a>
        <button class="btn btn-dark" data-print>{ICON['print']} Print recipe</button>
        <button class="btn btn-outline" id="share-btn">{ICON['share']} Share</button>
      </div>
    </aside>
  </div>
</div>
<section class="container related">
  {section_head('You might also like', '', f'<a href="{root}recipes/" class="view-all">All recipes →</a>')}
  <div class="recipe-grid three">{''.join(card(root, x) for x in related)}</div>
</section>
<script type="application/json" id="recipe-json">{json.dumps(rdata, ensure_ascii=False)}</script>'''
    page(f"recipes/{r['id']}/", f"{r['title']} | Bored of Toast", r['subtitle'], body, 'recipes', root, og=f"images/og/{r['id']}.jpg", jsonld=recipe_ld(r), body_attr='data-recipe-page')

def build_guides():
    root = '../'
    hero = hero_bleed(root, 'images/guide-pantry.webp', 'Kitchen basics', 'Cook smarter,<br><em>not harder.</em>',
        'Short, practical guides to the skills and staples behind every good meal. Read one tonight and cook better tomorrow.', short=True)
    body = f'''{hero}<section class="container section"><div class="guide-grid">{''.join(guide_card(root, g) for g in GUIDES)}</div>
<div class="coming reveal"><span class="hand">coming soon</span><p>Next up: how to season like a pro, the only 5 sauces you need, and meal prep without the boring boxes.</p></div></section>'''
    page('guides/', 'Kitchen Guides | Bored of Toast', 'Practical cooking guides: pantry staples, perfect rice every time and knife skills for home cooks.', body, 'guides', root)
    for g in GUIDES:
        build_guide(g)

def build_guide(g):
    root = '../../'
    img = f"images/{GUIDE_IMG[g['id']]}.webp"
    toc = ''.join(f'<a href="#s{i}">{e(s["h"])}</a>' for i, s in enumerate(g['sections'], 1))
    def sec(i, s):
        out = f'<section id="s{i}" class="reveal"><h2>{e(s["h"])}</h2>' + ''.join(f'<p>{e(p)}</p>' for p in s.get('p', []))
        if s.get('list'):
            items = []
            for li in s['list']:
                if ': ' in li and len(li.split(': ')[0]) < 40:
                    a, b = li.split(': ', 1); items.append(f'<li><strong>{e(a)}:</strong> {e(b)}</li>')
                else: items.append(f'<li>{e(li)}</li>')
            out += f'<ul class="prose-list">{"".join(items)}</ul>'
        if s.get('table'):
            t = s['table']
            out += '<div class="table-wrap"><table><thead><tr>' + ''.join(f'<th>{e(h)}</th>' for h in t['head']) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{e(c)}</td>' for c in row) + '</tr>' for row in t['rows']) + '</tbody></table></div>'
        return out + '</section>'
    body = f'''<section class="hero page-hero">
  <div class="container narrow">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{root}">Home</a> / <a href="{root}guides/">Guides</a></nav>
    <p class="eyebrow">{e(g['category'])} · {g['readTime']} min read</p>
    <h1>{e(g['title'])}</h1><p class="hero-lead">{e(g['subtitle'])}</p>
  </div>{WAVE}
</section>
<div class="container guide-cover"><img src="{root}{img}" alt="{e(g['title'])}" width="1400" height="933" fetchpriority="high"{rimg(root, img, SIZES['cover'])}>{credit(GUIDE_IMG[g['id']])}</div>
<div class="container section guide-layout">
  <article class="prose">
    <div class="lead">{''.join(f'<p>{e(p)}</p>' for p in g['intro'])}</div>
    <div class="takeaways reveal"><h2>Key takeaways</h2><ul>{''.join(f'<li>{ICON["check"]}<span>{e(t)}</span></li>' for t in g['takeaways'])}</ul></div>
    {''.join(sec(i, s) for i, s in enumerate(g['sections'], 1))}
    <section class="faq reveal"><h2>Questions</h2>{''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in g.get('faq', []))}</section>
  </article>
  <aside class="sidebar"><div class="side-card side-toc"><h3>In this guide</h3>{toc}</div>
    <div class="side-card"><h3>Put it into practice</h3>{''.join(f'<a class="mini-recipe" href="{root}recipes/{rid}/"><img src="{root}{BY_ID[rid]["img"]}" alt="" loading="lazy" width="64" height="64"{rimg(root, BY_ID[rid]["img"], SIZES["mini"])}><span><strong>{e(BY_ID[rid]["title"])}</strong><small>{fmt_time(BY_ID[rid]["time"])}</small></span></a>' for rid in GUIDE_RELATED[g['id']])}</div></aside>
</div>
<section class="container related">{section_head('More kitchen basics', '', f'<a href="{root}guides/" class="view-all">All guides →</a>')}<div class="guide-grid">{''.join(guide_card(root, x) for x in GUIDES if x['id'] != g['id'])}</div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": g['title'], "description": g['subtitle'], "image": SITE_URL + img,
           "author": {"@type": "Organization", "name": "Bored of Toast"}, "publisher": {"@type": "Organization", "name": "Bored of Toast", "logo": {"@type": "ImageObject", "url": SITE_URL + "images/logo.png"}},
           "datePublished": PUBLISHED, "mainEntityOfPage": f"{SITE_URL}guides/{g['id']}/"}]
    page(f"guides/{g['id']}/", f"{g['title']} | Bored of Toast", g['subtitle'], body, 'guides', root, og='images/og/home.jpg', jsonld=ld)

PLAN = [('Monday', 'honey-garlic-chicken-thighs', 'Open the recipe for the method and serving suggestions. Any rice or other sides are your choice; add their quantities separately.'),
        ('Tuesday', 'beef-tacos', 'Taco Tuesday. Mix the spice blend on Sunday so dinner is on the table in 25 minutes.'),
        ('Wednesday', 'lemon-chicken-orzo-soup', 'Use the recipe page to adjust portions before adding ingredients if you want a smaller batch.'),
        ('Thursday', 'sheet-pan-salmon', 'The shopping list covers the salmon recipe. If you choose a vegetable side, add it to your own shopping notes.'),
        ('Friday', 'creamy-garlic-pasta', 'Comfort food to start the weekend. Twenty minutes, one pan, zero stress.')]
BONUS = [('Saturday breakfast', 'buttermilk-pancakes'), ('Sunday treat', 'apple-crisp')]

def build_meal_plan():
    root = '../'
    days = ''.join(f'''<div class="plan-day reveal"><div class="plan-label"><span>{n}</span><small>Dinner idea</small></div>
  <a class="plan-recipe" href="{root}recipes/{rid}/"><img src="{root}{BY_ID[rid]['img']}" alt="{e(BY_ID[rid]['title'])}" loading="lazy" width="160" height="120"{rimg(root, BY_ID[rid]['img'], SIZES['plan'])}>
  <div><span class="tag">{e(BY_ID[rid]['category'])}</span><h3>{e(BY_ID[rid]['title'])}</h3><div class="meta"><span>{ICON['clock']}{fmt_time(BY_ID[rid]['time'])}</span><span>{ICON['chef']}{BY_ID[rid]['level']}</span><span>{BY_ID[rid]['serves']} {e(BY_ID[rid].get('servesLabel', 'servings'))}</span></div><p class="plan-tip">{ICON['bulb']} {e(tip)}</p><span class="view-all">Open recipe →</span></div></a><div class="dinner-action"><button class="btn btn-outline" data-add-dinner="{rid}" aria-label="Add {e(BY_ID[rid]['title'])} to shopping list">{ICON['bag']} Add this dinner</button></div></div>''' for n, (d, rid, tip) in enumerate(PLAN, 1))
    bonus = ''.join(card(root, BY_ID[rid]) for _, rid in BONUS)
    ids = [rid for _, rid, _ in PLAN]
    pdata = [{'id': rid, 'title': BY_ID[rid]['title'], 'url': f'recipes/{rid}/', 'serves': f"{BY_ID[rid]['serves']} {BY_ID[rid].get('servesLabel', 'servings')}", 'items': [ing_text(i) for g in BY_ID[rid]['ingredients'] for i in g['items']]} for rid in ids]
    hero = hero_bleed(root, 'images/honey-garlic-chicken-thighs.webp', '5 easy dinners', 'Less deciding.<br><em>More cooking.</em>',
        'Five ready-to-use dinner ideas from our free recipes. Cook them in any order, pick a favorite, or save all five to your shopping list.',
        f'<button class="btn btn-yellow" id="add-plan">{ICON["bag"]} Add all 5 dinners</button><a class="btn btn-ghost" href="{root}shopping-list/">View my shopping list →</a>', short=True)
    body = f'''{hero}
<section class="container section">
  <div class="dinner-help"><h2>Start here</h2><ol><li><strong>Choose a dinner.</strong> Open its recipe for the method and adjustable portions.</li><li><strong>Save ingredients.</strong> Add one dinner below or all five above. These buttons use each recipe’s original portions.</li><li><strong>Review your list.</strong> Check your pantry, then copy, share or print the ingredients.</li></ol><p>Your list stays in this browser on this device. Ingredients are grouped by recipe; repeated ingredients are not combined. Side dishes and weekend extras are separate.</p><p id="plan-status" class="dinner-status" role="status" aria-live="polite">Ready when you are. Saved recipes are kept if you add them again.</p><a class="btn btn-dark" href="{root}shopping-list/">Open my shopping list →</a></div>
  {section_head('Your five dinner ideas', 'A flexible dinner collection: choose the order that suits you.')}
  <div class="plan">{days}</div>
</section>
<section class="section bg-paper"><div class="container two-col prep-wrap">
  <div class="reveal"><h2 class="title">A little prep ahead</h2><ul class="prep-list">
    <li>{ICON['check']}<span>Mix the taco spice blend and store it in a jar.</span></li>
    <li>{ICON['check']}<span>Before cooking the soup, chop the onions, carrots and celery.</span></li>
    <li>{ICON['check']}<span>Measure the honey garlic sauce ingredients before you start the chicken.</span></li>
    <li>{ICON['check']}<span>Grate the Parmesan just before making the pasta.</span></li>
    <li>{ICON['check']}<span>Check your pantry before shopping so you only buy what you need.</span></li>
  </ul></div>
  <div class="reveal"><h2 class="title">Optional weekend extras</h2><p class="fine">Not included in “Add all 5 dinners”. Open either recipe to add its ingredients separately.</p><div class="recipe-grid two">{bonus}</div></div>
</div></section>
<script type="application/json" id="plan-json">{json.dumps(pdata, ensure_ascii=False)}</script>'''
    page('meal-plan/', '5 Easy Dinners | Bored of Toast', 'Five free dinner ideas with recipe portions, simple prep tips and ingredients you can save to your shopping list.', body, 'meal-plan', root)

def build_shopping():
    root = '../'
    body = f'''<section class="hero page-hero"><div class="container narrow"><p class="eyebrow">Your shopping list</p><h1>Everything you need,<br><em>in one place.</em></h1><p class="hero-lead">Add ingredients from any recipe or the five dinner ideas. Your list is saved on this device.</p></div>{WAVE}</section>
<section class="container section narrow">
  <div class="list-toolbar no-print">
    <button class="btn btn-dark" id="list-copy">Copy list</button><button class="btn btn-outline" id="list-share">{ICON['share']} Share</button>
    <button class="btn btn-outline" data-print>{ICON['print']} Print</button><button class="btn btn-outline danger" id="list-clear">Clear all</button>
  </div>
  <div id="shopping-list"></div>
  <div class="empty-state" id="list-empty" hidden><img src="{root}images/favicon.png" alt="" width="72" height="72"><h2>Your list is empty</h2><p>Open any recipe and tap “Add to shopping list”, or add the five dinner ideas.</p><div class="hero-actions" style="justify-content:center"><a class="btn btn-dark" href="{root}recipes/">Browse recipes</a><a class="btn btn-outline" href="{root}meal-plan/">Explore 5 easy dinners</a></div></div>
</section>'''
    page('shopping-list/', 'Shopping List | Bored of Toast', 'Your Bored of Toast shopping list.', body, 'shopping', root, head_extra='<meta name="robots" content="noindex">')

def build_about():
    root = '../'
    hero = hero_bleed(root, 'images/tomato-basil-soup.webp', 'About Bored of Toast', 'Our passion is<br><em>good food.</em>',
        "We believe great food doesn't have to be complicated. Bored of Toast is here to make everyday cooking easier, more enjoyable and a little more delicious.",
        f'<a href="#story" class="btn btn-yellow">Read our story {ICON["down"]}</a><a href="#contact" class="btn btn-ghost">Say hello</a>',
        f'<a class="float-card" href="#story"><img src="{root}images/our-story.webp" alt=""{rimg(root, "images/our-story.webp", SIZES["avatar"])}><div><small>Our story</small><strong>It started with toast</strong><span>Read how it began →</span></div></a>', short=True)
    vals = [('leaf', 'Real food', 'Fresh ingredients and real flavor, nothing overly processed.'), ('chef', 'Simple cooking', 'Clear steps and honest timing, so you are never left guessing.'),
            ('heart', 'Quality ingredients', 'Better ingredients make better meals, and they are easy to find.'), ('users', 'Everyday joy', 'Food brings people together. That is the best part.')]
    body = f'''{hero}
<section class="container section" id="story"><div class="story">
  <div class="story-media reveal"><img src="{root}images/our-story.webp" alt="Home cook chopping fresh parsley next to ripe tomatoes" class="main" loading="lazy"{rimg(root, 'images/our-story.webp', SIZES['story'])}><div class="note"><span class="hand">made with love ♥</span></div></div>
  <div class="reveal"><p class="tag">Our story</p><h2>It started with one<br>too many slices of toast.</h2>
    <p>Bored of Toast started with a simple idea: real food, made easy. We were tired of eating the same thing every night, so we started collecting the recipes that got us excited to cook again.</p>
    <p>What began as a small collection of favorites has grown into a place for home cooks, food lovers and anyone who believes that good food makes life better.</p>
    <p>Every recipe here is cooked in a real home kitchen, written in plain language and tested until it works every single time.</p>
    <a href="{root}recipes/" class="btn btn-dark" style="margin-top:10px">Browse our recipes {ICON['arrow']}</a></div>
</div></section>
<section class="section bg-paper"><div class="container">{section_head('What we believe in', 'Four simple ideas behind every recipe we share.')}
  <div class="values">{''.join(f'<div class="value reveal"><div class="icon-circle">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in vals)}</div></div></section>
<section class="container section"><div class="cta cta-photo reveal"><div class="cta-text"><h2>Cooking is a small<br>act of care.</h2><p>And we're here for every meal, big or small.</p></div><img src="{root}images/chicken-avocado-salad.webp" alt="" class="bg" loading="lazy"{rimg(root, 'images/chicken-avocado-salad.webp', SIZES['cta'])}></div></section>
<section class="container section" id="contact" style="padding-top:0"><div class="contact">
  <div class="reveal"><p class="tag">Get in touch</p><h2>Say hello</h2><p>Have a question about a recipe, a dish you'd love to see here, or an idea to work together? Use the form to prepare a draft, then send it from your email app.</p>
    <ul class="contact-list"><li><span class="icon-circle">{ICON['box']}</span>{EMAIL}</li><li><span class="icon-circle">{ICON['instagram']}</span>{INSTAGRAM}</li></ul></div>
  <form id="contact-form" class="reveal" data-email="{EMAIL}"><div class="row"><label>Name<input name="name" required placeholder="Your name"></label><label>Email<input name="email" type="email" required placeholder="you@example.com"></label></div>
    <label>Message<textarea name="message" required placeholder="Tell us what's cooking…"></textarea></label>
    <div><button type="submit" class="btn btn-dark">Open email draft {ICON['arrow']}</button></div><p class="form-note" id="form-note">Your email app should open with a draft. Review and send it there. If it does not open, your text stays in this form.</p></form>
</div></section>'''
    page('about/', 'About | Bored of Toast', "We believe great food doesn't have to be complicated. Meet the kitchen behind Bored of Toast.", body, 'about', root)

def build_legal(key, path):
    root = '../'
    d = GL[key]
    body = f'''<section class="hero page-hero"><div class="container narrow"><p class="eyebrow">Last updated {e(d['updated'])}</p><h1>{e(d['title'])}</h1></div>{WAVE}</section>
<article class="container section narrow prose">{''.join(f'<section><h2>{e(s["h"])}</h2>' + ''.join(f'<p>{e(p)}</p>' for p in s['p']) + '</section>' for s in d['sections'])}</article>'''
    page(path, f"{d['title']} | Bored of Toast", f"{d['title']} for Bored of Toast.", body, '', root)

def build_credits():
    root = '../'
    rows = []
    for r in RECIPES + [{'id': GUIDE_IMG[g['id']], 'title': g['title'], 'img': f"images/{GUIDE_IMG[g['id']]}.webp", 'guide': g['id']} for g in GUIDES]:
        c = CREDITS.get(r['id'])
        if not c: continue
        link = f"{root}guides/{r['guide']}/" if r.get('guide') else f"{root}recipes/{r['id']}/"
        rows.append(f'''<div class="credit-row"><img src="{root}{r['img']}" alt="" loading="lazy" width="72" height="72"{rimg(root, r['img'], SIZES['credit'])}><div><a href="{link}"><strong>{e(r['title'])}</strong></a><small>Photo by <a href="{e(c['photographer_url'])}" target="_blank" rel="noopener">{e(c['photographer'])}</a> · <a href="{e(c['photo_url'])}" target="_blank" rel="noopener">View on {c['source']}</a></small></div></div>''')
    body = f'''<section class="hero page-hero"><div class="container narrow"><p class="eyebrow">Thank you</p><h1>Photo credits</h1><p class="hero-lead">Our main recipe and guide photos come from talented photographers on <a href="https://www.pexels.com" target="_blank" rel="noopener" style="text-decoration:underline">Pexels</a>, shared under the free Pexels License. Step-by-step photos and pins are made by us.</p></div>{WAVE}</section>
<section class="container section narrow"><div class="credit-list">{''.join(rows)}</div></section>'''
    page('photo-credits/', 'Photo Credits | Bored of Toast', 'Credits for the photographers whose work appears on Bored of Toast.', body, '', root)

def build_404():
    root = SITE_URL
    picks = [BY_ID[i] for i in ['buttermilk-pancakes', 'creamy-garlic-pasta', 'apple-crisp']]
    body = f'''<section class="hero page-hero"><div class="container narrow"><p class="eyebrow">Error 404</p><h1>This page is <em>toast.</em></h1><p class="hero-lead">We couldn't find what you were looking for. Try a search, or start with one of these favorites.</p><div class="hero-actions"><button class="btn btn-yellow" data-open-search>{ICON['search']} Search recipes</button><a class="btn btn-ghost" href="{root}">Back home</a></div></div>{WAVE}</section>
<section class="container section"><div class="recipe-grid three">{''.join(card(root, r) for r in picks)}</div></section>'''
    page('404.html', 'Page not found | Bored of Toast', 'Page not found.', body, '', root, head_extra='<meta name="robots" content="noindex">')

def build_redirects():
    stubs = {'recipes.html': 'recipes/', 'about.html': 'about/'}
    for f, to in stubs.items():
        open(os.path.join(OUT, f), 'w').write(f'<!DOCTYPE html><meta charset="utf-8"><title>Redirecting…</title><link rel="canonical" href="{SITE_URL}{to}"><meta http-equiv="refresh" content="0; url={to}"><a href="{to}">Continue</a>')
    open(os.path.join(OUT, 'recipe.html'), 'w').write('''<!DOCTYPE html><meta charset="utf-8"><title>Redirecting…</title><meta name="robots" content="noindex"><script>var id=new URLSearchParams(location.search).get('id');location.replace(id?'recipes/'+encodeURIComponent(id)+'/':'recipes/');</script><noscript><meta http-equiv="refresh" content="0; url=recipes/"></noscript>''')

def build_index_js():
    items = [{'t': r['title'], 'u': f"recipes/{r['id']}/", 'i': thumb(r['img']), 'c': r['category'], 'm': fmt_time(r['time']), 'k': 'recipe',
              's': ' '.join([r['title'], r['category'], r['desc']] + r['tags'] + r.get('diet', []) + [i['n'] for g in r['ingredients'] for i in g['items']]).lower()} for r in RECIPES]
    items += [{'t': g['title'], 'u': f"guides/{g['id']}/", 'i': thumb(f"images/{GUIDE_IMG[g['id']]}.webp"), 'c': 'Guide', 'm': f"{g['readTime']} min read", 'k': 'guide',
               's': (g['title'] + ' ' + g['subtitle'] + ' guide').lower()} for g in GUIDES]
    items += [{'t': '5 Easy Dinners', 'u': 'meal-plan/', 'i': 'images/honey-garlic-chicken-thighs.webp', 'c': 'Dinner ideas', 'm': '5 free recipes', 'k': 'guide', 's': 'five 5 easy dinners meal plan shopping list weeknight'}]
    items += [{'t': 'The GLP-1 Kitchen Starter Kit', 'u': 'starter-kit/', 'i': 'images/commerce/starter-cover.jpg', 'c': 'Free guide', 'm': '9-page PDF', 'k': 'guide', 's': 'free glp-1 starter kit nourish recipes organizer shopping'}, {'t': 'Nourished - The GLP-1 Kitchen Companion', 'u': 'nourished/', 'i': 'images/commerce/nourished-cover.jpg', 'c': 'Cookbook collection', 'm': 'US$20', 'k': 'guide', 's': 'nourished glp-1 cookbook recipes collection meal planning shopping'}]
    open(os.path.join(OUT, 'search-index.js'), 'w').write('window.BOT_INDEX=' + json.dumps(items, ensure_ascii=False) + ';')

def build_sitemap():
    urls = ['', 'recipes/', 'guides/', 'meal-plan/', 'about/', 'privacy/', 'terms/', 'photo-credits/', 'starter-kit/', 'nourished/'] + [f"recipes/{r['id']}/" for r in RECIPES] + [f"guides/{g['id']}/" for g in GUIDES]
    today = datetime.date.today().isoformat()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE_URL}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(xml)
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n')
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')

if __name__ == '__main__':
    shutil.copytree(os.path.join(HERE, 'printables'), os.path.join(OUT, 'printables'), dirs_exist_ok=True)
    for f in ['styles.css', 'app.js']:
        shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
    shutil.copytree(os.path.join(HERE, '..', 'fonts'), os.path.join(OUT, 'fonts'), dirs_exist_ok=True)   # self-hosted fonts live in /fonts
    build_home(); build_recipes()
    for r in RECIPES: build_recipe(r)
    build_guides(); build_meal_plan(); build_shopping(); build_about()
    build_storefront(page, STOREFRONT)
    build_legal('privacy', 'privacy/'); build_legal('terms', 'terms/')
    build_credits(); build_404(); build_redirects(); build_index_js(); build_sitemap()
    print('built', len(RECIPES), 'recipes,', len(GUIDES), 'guides')
