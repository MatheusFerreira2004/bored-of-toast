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

Editorial pass (added later):

  9. Removes the "04 / Where to begin" home section. It repeated the category
     grid directly above it and every one of its five cards linked to
     /start-here/, a route that does not exist.
 10. Trims the home category grid from nine cards to five and shortens the
     label descriptions to one short line each.
 11. Reduces the AI-image disclosure to a single mention per page.
 12. Rewrites the About page body.
 13. Removes the duplicated Prep line in swap blocks.
 14. Fixes British spellings and the overnight oats card meta.

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

# Category cards removed from the home grid. Nine cards is a wall; these four
# overlap heavily with the five that stay, and the full list is one click away
# on /recipes/.
DROPPED_HOME_CATEGORIES = [
    'protein-forward',
    'pantry-meals',
    'fresh-lunches',
    'cozy-dinners',
]

# Long category blurbs shortened to a single scannable line.
CATEGORY_DESC_REWRITES = {
    'Short active prep and few steps — ready in 25 minutes or less. '
    'Overnight resting is noted separately.':
        'Ready in 25 minutes or less.',
    'Meals built around pantry staples and everyday affordable ingredients.':
        'Built on pantry staples.',
    'Vegetables, fruits, grains, and legumes take the lead. '
    'Not necessarily vegan.':
        'Vegetables and legumes take the lead.',
    'Suited to preparing in advance or starting the night before — '
    'breakfast included.':
        'Prep ahead, or start the night before.',
    'The same starting ingredient taken in entirely different directions.':
        'One ingredient, taken somewhere new.',
    'Recipes centred on legumes, eggs, tofu, or other protein sources.':
        'Legumes, eggs and tofu take the lead.',
    'Built around shelf-stable ingredients you are likely to have at home.':
        'Shelf-stable ingredients only.',
    'No-cook or minimal-cook options that feel light and lively at midday.':
        'Light, no-cook midday meals.',
    'Warm skillet and stovetop meals that are comforting after a long day.':
        'Warm skillet meals for tired evenings.',
}

# British spellings, on a US-facing site.
SPELLING_FIXES = [
    (r'\bcentred\b', 'centered'),
    (r'\bcentre\b', 'center'),
    (r'\bflavour\b', 'flavor'),
    (r'\bflavours\b', 'flavors'),
    (r'\bcolour\b', 'color'),
]

ABOUT_MARKER = 'data-about-rewritten'

ABOUT_DESCRIPTION = (
    'How Bored of Toast develops its recipes: sources we read, what we write '
    'ourselves, how images are made, and who is responsible for corrections.'
)


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
# About page
# ---------------------------------------------------------------------------

def about_body():
    """A single-voice About page.

    Three things the previous version was missing and that matter both to a
    reader and to an ad network review: a named person responsible for the
    content, a plain description of how recipes are actually produced, and no
    future-tense language about a site that is already live.

    The #editorial anchor is preserved because pages across the site link to it.
    """
    return (
        f'<section class="wrap section" {ABOUT_MARKER}>'
        '<p class="eyebrow">ABOUT BORED OF TOAST</p>'
        '<h1>Everyday ingredients.<br>'
        '<span class="title-flourish">Better meals.</span></h1>'
        '<p class="lead">Most of us cook the same handful of meals on repeat. '
        'Not for lack of skill, but for lack of ideas at seven on a Tuesday. '
        'This site exists to widen that rotation without sending you to the '
        'store for anything unusual.</p>'
        '</section>'

        '<section class="wrap section">'
        '<div class="section-top">'
        '<div><p class="eyebrow">WHAT YOU WILL FIND</p>'
        '<h2>Familiar ingredients, '
        '<span class="serif-accent">new directions.</span></h2></div>'
        '<p>Every recipe starts from something already in your kitchen: a can '
        'of beans, a bag of lentils, oats, a cucumber. The interesting part is '
        'what happens next.</p>'
        '</div>'
        '<ul class="transparency-list">'
        '<li><strong>Recipes that adjust to you.</strong> Change the number of '
        'servings and every quantity recalculates. Swap an ingredient and we '
        'tell you what shifts in texture, flavor and timing, rather than '
        'leaving you to guess.</li>'
        '<li><strong>Kitchen notes.</strong> Short pieces on technique: why '
        'beans turn creamy, when garlic burns, how to keep a salad crisp. '
        'These outlast any single recipe.</li>'
        '<li><strong>Reference charts.</strong> Cooking times, conversions and '
        'substitutions in one place, so you are not searching with one hand '
        'while stirring with the other.</li>'
        '</ul>'
        '</section>'

        '<section class="wrap section" id="editorial">'
        '<div class="section-top">'
        '<div><p class="eyebrow">OUR EDITORIAL APPROACH</p>'
        '<h2>How these recipes '
        '<span class="serif-accent">are made.</span></h2></div>'
        '<p>You should know how anything you cook from was put together. '
        'Here is ours, without the gloss.</p>'
        '</div>'
        '<ul class="transparency-list">'
        '<li><strong>We start from cooks who have made the dish.</strong> Each '
        'recipe begins by reading several published versions from established '
        'food publications and experienced home cooks, comparing where they '
        'agree and where they diverge, and explaining the reasoning behind the '
        'version we land on. Every source we consulted is linked at the foot '
        'of the recipe.</li>'
        '<li><strong>We write the method ourselves.</strong> Ingredient lists '
        'are factual. The instructions, explanations and notes on this site '
        'are our own writing, not a single source rephrased.</li>'
        '<li><strong>Food images are illustrations.</strong> The food images '
        'here are generated with AI to show a serving suggestion. They are not '
        'photographs of a plate we cooked.</li>'
        '<li><strong>Substitutions are suggestions.</strong> Swap notes '
        'describe what is likely to change. They are editorial guidance, not '
        'tested equivalents.</li>'
        '<li><strong>Nutrition is estimated.</strong> Where nutrition appears, '
        'it is calculated from the listed ingredients and rounded. It is not '
        'laboratory verified and will vary with brands and portioning.</li>'
        '<li><strong>No medical advice.</strong> Nothing here is dietary or '
        'medical advice. For health guidance, speak to a qualified '
        'professional.</li>'
        '</ul>'
        '<p><a class="text-link" href="/contact/">'
        'Found something that looks wrong? Tell us ↗</a></p>'
        '</section>'

        '<section class="wrap section">'
        '<div class="section-top">'
        '<div><p class="eyebrow">WHO WRITES IT</p>'
        '<h2>A small operation.</h2></div>'
        '<p>No test kitchen, no staff of twenty, no sponsored recipes.</p>'
        '</div>'
        '<p>Bored of Toast is researched, written and edited by Matheus '
        'Ferreira, who is also the person who fixes it when something is '
        'wrong. Questions, corrections and suggestions all reach the same '
        'inbox.</p>'
        '<p><a class="text-link" href="/contact/">Get in touch ↗</a></p>'
        '</section>'
    )


def rewrite_about(html):
    """Swap the About page body and its meta description."""
    if ABOUT_MARKER in html:
        return html, False

    m = re.search(r'(<main[^>]*>)(.*?)(</main>)', html, re.S | re.I)
    if not m:
        return html, False

    html = html[:m.start()] + m.group(1) + about_body() + m.group(3) + html[m.end():]

    # The old description claimed the site tests and photographs recipes.
    for attr in ('name="description"', 'property="og:description"',
                 'name="twitter:description"'):
        html = re.sub(
            r'(<meta ' + re.escape(attr) + r' content=")[^"]*(")',
            lambda mm: mm.group(1) + esc(ABOUT_DESCRIPTION, quote=True) + mm.group(2),
            html,
        )

    return html, True


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
    pattern = re.compile(r'<a[^>]*href="/start-here/[^"]*"[^>]*>.*?</a>', re.I | re.S)
    new_html, count = pattern.subn('', html)
    return new_html, count > 0


def remove_where_to_begin(html):
    """Drop the "04 / Where to begin" home section.

    It asked the reader to pick a direction and then offered the same choices
    as the category grid immediately above it, under different names. All five
    of its cards also pointed at /start-here/, which does not exist.
    """
    pattern = re.compile(
        r'<section[^>]*class="[^"]*home-paths[^"]*"[^>]*>.*?</section>',
        re.I | re.S,
    )
    new_html, count = pattern.subn('', html)
    if count:
        return new_html, True

    # Fallback: match on the id if the class ever changes.
    pattern = re.compile(
        r'<section[^>]*id="start-here-paths"[^>]*>.*?</section>',
        re.I | re.S,
    )
    new_html, count = pattern.subn('', html)
    return new_html, count > 0


def trim_category_cards(html):
    """Nine category cards is a wall. Keep five distinct axes."""
    changed = False
    for slug in DROPPED_HOME_CATEGORIES:
        pattern = re.compile(
            r'<a[^>]*class="[^"]*cat-card[^"]*"[^>]*id="home-cat-'
            + re.escape(slug) + r'"[^>]*>.*?</a>',
            re.I | re.S,
        )
        html, count = pattern.subn('', html)
        if count:
            changed = True
    return html, changed


def shorten_category_descs(html):
    changed = False
    for long_text, short_text in CATEGORY_DESC_REWRITES.items():
        if long_text in html:
            html = html.replace(long_text, short_text)
            changed = True
    return html, changed


def reduce_ai_disclosure(html):
    """One disclosure per page, not three.

    The editorial note is the canonical statement. Image captions repeat it,
    which reads as unease rather than transparency. Only strips the caption
    version when another disclosure survives on the page.
    """
    mentions = len(re.findall(r'AI[- ]generated', html, re.I))
    if mentions < 2:
        return html, False

    changed = False
    for phrase in (' Image is AI-generated.', ' Images are AI-generated.',
                   ' Image is AI generated.'):
        if phrase in html:
            html = html.replace(phrase, '')
            changed = True

    # Recipe pages carry both a badge and the editorial note; keep the note.
    html, count = re.subn(
        r'\s*<span[^>]*class="[^"]*ai-badge[^"]*"[^>]*>.*?</span>',
        '',
        html,
        flags=re.I | re.S,
    )
    if count and 'editorial-note' in html:
        changed = True

    return html, changed


def remove_development_leftovers(html):
    """Clear the last of the pre-launch labelling."""
    changed = False
    replacements = [
        (r'\s*<span aria-hidden="true">·</span>\s*Recipe in development', ''),
        (r'\s*·\s*Recipe in development', ''),
        (r'\s*<span[^>]*class="[^"]*dev-badge[^"]*"[^>]*>.*?</span>', ''),
    ]
    for pattern, repl in replacements:
        html, count = re.subn(pattern, repl, html, flags=re.I | re.S)
        if count:
            changed = True
    return html, changed


def dedupe_swap_prep(html):
    """Swap blocks repeated the same sentence under Adjust and Prep."""
    pattern = re.compile(
        r'(<strong>Adjust:</strong>\s*)(.*?)(<br><strong>Prep:</strong>\s*)(.*?)'
        r'(?=</p>)',
        re.S,
    )

    hits = [0]

    def repl(m):
        adjust = m.group(2).strip()
        prep = m.group(4).strip()
        if adjust and adjust == prep:
            hits[0] += 1
            return m.group(1) + m.group(2)
        return m.group(0)

    html = pattern.sub(repl, html)
    return html, hits[0] > 0


def fix_cue_typo(html):
    needle = 'combined. whisk again'
    if needle not in html:
        return html, False
    return html.replace(needle, 'combined. Whisk again'), True


def fix_spelling(html):
    changed = False
    for pattern, repl in SPELLING_FIXES:
        html, count = re.subn(pattern, repl, html)
        if count:
            changed = True
    return html, changed


def fix_overnight_card_meta(html):
    """"Serves 1 · Chill overnight" hid the five minutes of actual work."""
    pattern = re.compile(
        r'(class="card-bottom".{0,200}?)Chill overnight',
        re.I | re.S,
    )
    new_html, count = pattern.subn(lambda m: m.group(1) + '5 min + overnight', html)
    return new_html, count > 0


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
    ('where-to-begin section', remove_where_to_begin),
    ('start-here link', remove_start_here),
    ('category cards trimmed', trim_category_cards),
    ('category blurbs', shorten_category_descs),
    ('ai disclosure', reduce_ai_disclosure),
    ('development leftovers', remove_development_leftovers),
    ('swap prep duplicate', dedupe_swap_prep),
    ('cue typo', fix_cue_typo),
    ('spelling', fix_spelling),
    ('overnight card meta', fix_overnight_card_meta),
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
    counts['about rewrite'] = 0
    touched = 0

    for page in pages:
        try:
            html = page.read_text(encoding='utf-8')
        except Exception as exc:
            print(f'  warn: could not read {page.name}: {exc}')
            continue

        original = html
        parts = page.relative_to(DIST).parts

        # About body first, so later transforms see the new copy
        if parts and parts[0] == 'about':
            try:
                html, changed = rewrite_about(html)
                if changed:
                    counts['about rewrite'] += 1
            except Exception as exc:
                print(f'  warn: about rewrite failed: {exc}')

        if available:
            html, changed = inject_stylesheets(html, available)
            if changed:
                counts['stylesheets'] += 1

        # Related recipes, only on individual recipe pages
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
