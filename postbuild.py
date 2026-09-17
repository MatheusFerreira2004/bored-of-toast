"""Post-build pass over dist/.

Runs after build.py. Applies additive changes to the generated HTML without
touching build.py itself:

  1. Copies additive stylesheets into dist/
  2. Injects their <link> tags last, so the cascade order is correct
  3. Adds the reading progress script
  4. Injects the related recipes block on recipe pages
  5. Hides the visible byline (kept in JSON-LD for SEO)
  6. Removes the /start-here/ footer link, which 404s
  7. Fixes the lowercase sentence start in the dressing step cue
  8. Drops the leftover "development editions" line from kitchen notes

Every step is wrapped so a failure here can never break a deploy. If a file
or pattern is missing, the script logs and moves on.

Note on scope: this file is the fast lane. Presentation fixes belong here;
data and schema logic belongs in build.py. Migrate anything that proves
stable and structural back into the generator over time.

Run locally with:
    python build.py && python postbuild.py
"""
import json
import re
import shutil
import sys
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'

# Stylesheets that are additive and must load after the existing ones.
# Order matters: later files win in the cascade.
ADDITIVE_CSS = ['related.css', 'polish.css']

# Author name to strip from the visible page. The name stays in the
# JSON-LD author field, which is what Google reads for E-E-A-T.
AUTHOR_NAME = 'Matheus Ferreira'


# ---------------------------------------------------------------------------
# Recipe index, built by reading the generated pages
# ---------------------------------------------------------------------------

def collect_recipes():
    """Read dist/recipes/*/index.html and extract card data.

    Parsing the output rather than importing build.py keeps this script
    independent of the generator's internals.
    """
    recipes = []
    base = DIST / 'recipes'
    if not base.exists():
        return recipes

    for page in sorted(base.glob('*/index.html')):
        slug = page.parent.name
        try:
            html = page.read_text(encoding='utf-8')
        except Exception:
            continue

        title = _first(html, r'<h1[^>]*>(.*?)</h1>')
        if not title:
            continue

        # Pull the hero image stem from the og:image or the first asset
        img = _first(html, r'/assets/([a-z0-9\-]+)-(?:1200|800|480)\.webp')

        # Categories come from the filter links in the header
        cats = re.findall(r'/recipes/\?category=([a-z0-9\-]+)', html)

        meta = _first(html, r'<p class="recipe-meta[^"]*">(.*?)</p>') or ''

        recipes.append(dict(
            slug=slug,
            title=re.sub(r'<[^>]+>', '', title).strip(),
            img=img or '',
            alt=_first(html, r'<img[^>]+alt="([^"]*)"[^>]*class="[^"]*hero') or '',
            categories=list(dict.fromkeys(cats)),
            method=_first(html, r'Method\s*</?[^>]*>?\s*([A-Za-z\-]+)') or '',
            total_time=_first(html, r'Total\s*</?[^>]*>?\s*(~?\s*\d+\s*min)') or '',
            serves=_first(html, r'[Ss]erve[s]?\s+(\d+)') or '',
            meta_line=re.sub(r'<[^>]+>', '', meta).strip(),
        ))

    return recipes


def _first(text, pattern):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------------------
# Related recipes
# ---------------------------------------------------------------------------

def _time_bucket(r):
    digits = ''.join(c for c in str(r.get('total_time') or '') if c.isdigit())
    if not digits:
        return None
    mins = int(digits[:3])
    return 'quick' if mins <= 15 else ('medium' if mins <= 30 else 'long')


def _reason(current, other):
    shared = set(current.get('categories', [])) & set(other.get('categories', []))
    method = (other.get('method') or '').lower()

    if 'no-cook' in method:
        return 'Also no-cook'
    if 'one-pan' in method:
        return 'Also one pan'
    if 'make-ahead' in shared:
        return 'Also make-ahead'
    if 'quick-easy' in shared:
        return 'Also under 25 minutes'
    if 'budget-friendly' in shared:
        return 'Also pantry-friendly'
    if 'protein-forward' in shared:
        return 'Also protein-forward'
    if 'plant-forward' in shared:
        return 'Also plant-forward'
    return 'From the notebook'


def pick_related(current, all_recipes, limit=3):
    """Score by category overlap, method and time, with a stable fallback."""
    slug = current['slug']
    cats = set(current.get('categories', []))
    method = (current.get('method') or '').lower()
    bucket = _time_bucket(current)

    order = {r['slug']: i for i, r in enumerate(all_recipes)}
    scored = []
    for r in all_recipes:
        if r['slug'] == slug:
            continue
        score = 3 * len(cats & set(r.get('categories', [])))
        if method and (r.get('method') or '').lower() == method:
            score += 2
        if bucket and _time_bucket(r) == bucket:
            score += 1
        scored.append((score, r))

    scored.sort(key=lambda x: (-x[0], order.get(x[1]['slug'], 99)))
    picked = [r for score, r in scored if score > 0][:limit]

    if len(picked) < limit:
        taken = {r['slug'] for r in picked} | {slug}
        for r in all_recipes:
            if r['slug'] not in taken:
                picked.append(r)
                taken.add(r['slug'])
            if len(picked) == limit:
                break

    return picked[:limit]


def render_related(current, all_recipes, limit=3):
    picks = pick_related(current, all_recipes, limit)
    if not picks:
        return ''

    cards = ''
    for r in picks:
        stem = r.get('img') or ''
        img_html = ''
        if stem:
            img_html = (
                f'<img src="/assets/{esc(stem, quote=True)}-800.webp" '
                f'alt="{esc(r.get("alt") or r["title"], quote=True)}" '
                f'width="800" height="600" loading="lazy" decoding="async">'
            )

        meta = r.get('meta_line') or ' · '.join(
            x for x in [
                f'Serves {r["serves"]}' if r.get('serves') else '',
                r.get('total_time') or '',
                r.get('method') or '',
            ] if x
        )

        cards += (
            f'<a class="rr-card" href="/recipes/{esc(r["slug"], quote=True)}/">'
            f'<span class="rr-thumb">{img_html}</span>'
            f'<span class="rr-body">'
            f'<span class="rr-reason">{esc(_reason(current, r))}</span>'
            f'<span class="rr-title">{esc(r["title"])}</span>'
            f'<span class="rr-meta">{esc(meta)}</span>'
            f'</span></a>'
        )

    return (
        f'<section class="rr-block" aria-labelledby="rr-heading">'
        f'<p class="eyebrow">KEEP GOING</p>'
        f'<h2 id="rr-heading">What to cook next.</h2>'
        f'<div class="rr-grid">{cards}</div>'
        f'</section>'
    )


def inject_related(html, slug, all_recipes):
    """Place the related block at the end of the recipe article."""
    if 'rr-block' in html:
        return html, False

    current = next((r for r in all_recipes if r['slug'] == slug), None)
    if not current:
        return html, False

    block = render_related(current, all_recipes)
    if not block:
        return html, False

    # Prefer inserting just before the closing </main>
    if '</main>' in html:
        return html.replace('</main>', block + '</main>', 1), True
    if '</article>' in html:
        idx = html.rfind('</article>')
        return html[:idx] + block + html[idx:], True
    return html, False


# ---------------------------------------------------------------------------
# Generic transforms
# ---------------------------------------------------------------------------

def copy_stylesheets():
    copied = []
    for name in ADDITIVE_CSS:
        src = ROOT / name
        if not src.exists():
            print(f'  skip: {name} not found at repo root')
            continue
        shutil.copy2(src, DIST / name)
        copied.append(name)
    return copied


def inject_stylesheets(html, available):
    if '</head>' not in html:
        return html, False
    tags = ''
    for name in available:
        href = f'/{name}'
        if href not in html:
            tags += f'<link rel="stylesheet" href="{href}">'
    if not tags:
        return html, False
    return html.replace('</head>', tags + '</head>', 1), True


def add_scroll_progress(html):
    if '</body>' not in html or 'data-scroll-progress' in html:
        return html, False
    script = (
        '<script data-scroll-progress>'
        '(function(){'
        'var d=document.documentElement,t=0;'
        'function u(){'
        'var h=d.scrollHeight-d.clientHeight;'
        'd.style.setProperty("--scroll",(h>0?(d.scrollTop/h)*100:0)+"%");'
        '}'
        'addEventListener("scroll",function(){'
        'if(t)return;'
        't=requestAnimationFrame(function(){t=0;u();});'
        '},{passive:true});'
        'addEventListener("resize",u,{passive:true});u();'
        '})();'
        '</script>'
    )
    return html.replace('</body>', script + '</body>', 1), True


def remove_visible_byline(html):
    """Remove the on-page author credit. JSON-LD author is untouched."""
    changed = False
    pattern = re.compile(
        r'<(p|span|div)\b[^>]*>\s*By\s+' + re.escape(AUTHOR_NAME) + r'[^<]*</\1>',
        re.I,
    )
    html, count = pattern.subn('', html)
    if count:
        changed = True

    bare = re.compile(r'\bBy\s+' + re.escape(AUTHOR_NAME) + r'\b\s*(·[^<]*)?')
    html, count = bare.subn('', html)
    if count:
        changed = True

    return html, changed


def remove_start_here(html):
    pattern = re.compile(r'<a[^>]*href="/start-here/"[^>]*>.*?</a>', re.I | re.S)
    new_html, count = pattern.subn('', html)
    return new_html, count > 0


def fix_cue_typo(html):
    needle = 'combined. whisk again'
    if needle not in html:
        return html, False
    return html.replace(needle, 'combined. Whisk again'), True


def fix_development_note(html):
    old = ('Linked recipes are development editions and await kitchen testing. '
           'These guides do not change that status.')
    new = 'These guides work with any recipe on the site.'
    if old in html:
        return html.replace(old, new), True
    pattern = re.compile(r'Linked recipes are development editions[^<]*', re.I)
    new_html, count = pattern.subn(new, html)
    return new_html, count > 0


TRANSFORMS = [
    ('scroll progress', add_scroll_progress),
    ('visible byline', remove_visible_byline),
    ('start-here link', remove_start_here),
    ('cue typo', fix_cue_typo),
    ('development note', fix_development_note),
]


def main():
    if not DIST.exists():
        print('postbuild: dist/ not found, nothing to do')
        return 0

    print('postbuild: starting')

    available = copy_stylesheets()
    if available:
        print(f'  copied: {", ".join(available)}')

    recipes = collect_recipes()
    print(f'  recipes indexed: {len(recipes)}')

    pages = sorted(DIST.rglob('*.html'))
    if not pages:
        print('  no HTML files found')
        return 0

    counts = {name: 0 for name, _ in TRANSFORMS}
    counts['stylesheets'] = 0
    counts['related block'] = 0
    touched = 0

    for page in pages:
        try:
            html = page.read_text(encoding='utf-8')
        except Exception as exc:
            print(f'  warn: could not read {page.name}: {exc}')
            continue

        original = html

        if available:
            html, changed = inject_stylesheets(html, available)
            if changed:
                counts['stylesheets'] += 1

        # Related recipes, only on individual recipe pages
        parts = page.relative_to(DIST).parts
        if len(parts) == 3 and parts[0] == 'recipes' and parts[2] == 'index.html':
            try:
                html, changed = inject_related(html, parts[1], recipes)
                if changed:
                    counts['related block'] += 1
            except Exception as exc:
                print(f'  warn: related block failed on {parts[1]}: {exc}')

        for name, fn in TRANSFORMS:
            try:
                html, changed = fn(html)
                if changed:
                    counts[name] += 1
            except Exception as exc:
                print(f'  warn: {name} failed on {page.name}: {exc}')

        if html != original:
            try:
                page.write_text(html, encoding='utf-8')
                touched += 1
            except Exception as exc:
                print(f'  warn: could not write {page.name}: {exc}')

    print(f'  pages scanned: {len(pages)}')
    print(f'  pages modified: {touched}')
    for key, value in counts.items():
        if value:
            print(f'    {key}: {value}')
    print('postbuild: done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
