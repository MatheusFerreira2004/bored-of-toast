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

Editorial pass:

  9. Removes the "04 / Where to begin" home section. It repeated the category
     grid directly above it and every one of its five cards linked to
     /start-here/, a route that does not exist.
 10. Trims the home category grid from nine cards to five and shortens the
     label descriptions to one short line each.
 11. Reduces the AI-image disclosure to a single mention per page.
 12. Rewrites the About page body.
 13. Removes the duplicated Prep line in swap blocks.
 14. Fixes British spellings and the overnight oats card meta.

Corrective pass:

 15. Related card meta was rendering as "Serves 2 · a". The label/value pairs
     are now parsed with tag-aware splitting and each part is sanitised.
 16. All three related cards showed the same reason. Reasons are now ranked
     per pair and de-duplicated across the block.
 17. Author name stripped from visible markup site-wide.

Reference pages and schema repair:

 18. Generates the reference pages defined in reference_content.py. Each one
     reuses the shell of an existing generated page, so the header, footer,
     fonts and stylesheets match the rest of the site exactly. Three routes
     under /kitchen-notes/, carrying Article schema rather than Recipe.
 19. Repairs suitableForDiet and keywords in the recipe JSON-LD. Both fields
     are stored as plain strings in the data model, and the generator
     iterates them character by character, producing entries such as
     "https://schema.org/V" and a keyword list split into single letters.
     The repair reassembles both. It is written generically, so it also
     covers future recipes stored the same way.

PENDING DECISION: no author name is shown anywhere on the site right now, by
request, while the byline is being decided. The name still exists in the
recipe JSON-LD author field. Visible authorship carries real weight in ad
network review for food content, so a name should be restored before applying.

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
from html import escape as esc, unescape
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'

# Stylesheets that are additive and must load after the existing ones.
# Order matters: later files win in the cascade.
ADDITIVE_CSS = ['related.css', 'polish.css']

# Loaded only on reference pages, in the same way recipe.css is scoped.
REFERENCE_CSS = 'reference.css'

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
    'Short active prep and few steps \u2014 ready in 25 minutes or less. '
    'Overnight resting is noted separately.':
        'Ready in 25 minutes or less.',
    'Meals built around pantry staples and everyday affordable ingredients.':
        'Built on pantry staples.',
    'Vegetables, fruits, grains, and legumes take the lead. '
    'Not necessarily vegan.':
        'Vegetables and legumes take the lead.',
    'Suited to preparing in advance or starting the night before \u2014 '
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

# Full schema.org diet names, used to rebuild truncated URLs.
DIET_NAMES = [
    'DiabeticDiet',
    'GlutenFreeDiet',
    'HalalDiet',
    'HinduDiet',
    'KosherDiet',
    'LowCalorieDiet',
    'LowFatDiet',
    'LowLactoseDiet',
    'LowSaltDiet',
    'VeganDiet',
    'VegetarianDiet',
]

# Reason labels per category, ordered by how distinctive they are as a
# recommendation. "Also quick" says less than "Same ingredient, new direction".
CATEGORY_REASONS = {
    'one-ingredient': 'Same ingredient, new direction',
    'one-ingredient-different-ways': 'Same ingredient, new direction',
    'make-ahead': 'Also make-ahead',
    'protein-forward': 'Also protein-forward',
    'plant-forward': 'Also plant-forward',
    'fresh-lunches': 'Another light lunch',
    'cozy-dinners': 'Another warm dinner',
    'pantry-meals': 'Also from the pantry',
    'budget-friendly': 'Also pantry-friendly',
    'quick-easy': 'Also quick',
}

METHOD_REASONS = {
    'no-cook': 'Also no-cook',
    'one-pan': 'Also one pan',
    'one pan': 'Also one pan',
    'sheet-pan': 'Also sheet-pan',
    'skillet': 'Also a skillet meal',
    'blender': 'Also blender-only',
    'oven': 'Also oven-baked',
    'stovetop': 'Also stovetop',
}

BUCKET_REASONS = {
    'quick': 'Also under 15 minutes',
    'medium': 'Also under 30 minutes',
    'long': 'Also a longer cook',
}

# Labels used in the recipe meta strip. Used to pair label/value text nodes.
META_LABELS = frozenset({'prep', 'cook', 'total', 'method', 'serves', 'yield'})


# ---------------------------------------------------------------------------
# Recipe index, built by reading the generated pages
# ---------------------------------------------------------------------------

def _strip_tags(fragment, sep=' '):
    text = re.sub(r'<[^>]+>', sep, fragment)
    return re.sub(r'\s+', ' ', text).strip()


def _meta_pairs(html):
    """Read the recipe meta strip as label/value pairs.

    The markup nests a label span and a value span per item, so a plain regex
    over the raw HTML picked up stray characters. Splitting on tag boundaries
    and pairing adjacent text nodes is far more robust.
    """
    match = re.search(r'class="recipe-meta[^"]*"[^>]*>(.*?)</p>', html, re.S | re.I)
    if not match:
        return {}

    # Replace every tag with a delimiter so text nodes stay separate.
    raw = re.sub(r'<[^>]+>', '|', match.group(1))
    parts = [p.strip() for p in raw.split('|') if p.strip()]

    pairs = {}
    for index, part in enumerate(parts[:-1]):
        key = part.lower().rstrip(':').strip()
        if key in META_LABELS and key not in pairs:
            pairs[key] = parts[index + 1]
    return pairs


def _clean_meta_part(value):
    """Reject fragments that are clearly parse noise."""
    if not value:
        return ''
    value = _strip_tags(str(value)).strip(' \u00b7|,;')
    if len(value) < 2:
        return ''
    # A value made only of punctuation or a single stray word character.
    if not re.search(r'[A-Za-z0-9]{2,}', value):
        return ''
    return value


def _serves_from_jsonld(html):
    match = re.search(r'"recipeYield"\s*:\s*"([^"]+)"', html)
    if not match:
        return ''
    yield_text = match.group(1).strip()
    digits = re.search(r'(\d+)', yield_text)
    return f'Serves {digits.group(1)}' if digits else yield_text


def collect_recipes():
    try:
        import json
        with open('recipe_models.json', 'r', encoding='utf-8') as f:
            models = json.load(f)
    except Exception:
        models = {}

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

        img = _first(html, r'/assets/([a-z0-9\-]+)-(?:1200|800|480)\.webp')
        cats = re.findall(r'/recipes/\?category=([a-z0-9\-]+)', html)
        pairs = _meta_pairs(html)
        
        model = models.get(slug, {})
        editorial_related = model.get('relatedRecipes')

        recipes.append(dict(
            slug=slug,
            title=unescape(_strip_tags(title)),
            img=img or '',
            alt=_first(html, r'<img[^>]+alt="([^"]*)"[^>]*class="[^"]*hero') or '',
            categories=list(dict.fromkeys(cats)),
            method=_clean_meta_part(pairs.get('method')),
            total_time=_clean_meta_part(pairs.get('total') or pairs.get('prep')),
            serves=_serves_from_jsonld(html),
            editorial_related=editorial_related,
        ))

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

        img = _first(html, r'/assets/([a-z0-9\-]+)-(?:1200|800|480)\.webp')
        cats = re.findall(r'/recipes/\?category=([a-z0-9\-]+)', html)
        pairs = _meta_pairs(html)

        recipes.append(dict(
            slug=slug,
            title=unescape(_strip_tags(title)),
            img=img or '',
            alt=_first(html, r'<img[^>]+alt="([^"]*)"[^>]*class="[^"]*hero') or '',
            categories=list(dict.fromkeys(cats)),
            method=_clean_meta_part(pairs.get('method')),
            total_time=_clean_meta_part(pairs.get('total') or pairs.get('prep')),
            serves=_serves_from_jsonld(html),
        ))

    return recipes


def _first(text, pattern):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------------------
# JSON-LD repair
# ---------------------------------------------------------------------------

def _rebuild_diet(values):
    """Reassemble diet URLs that were split into single characters.

    The data model stores suitable_for_diet as "VegetarianDiet, GlutenFreeDiet"
    and the generator iterates the string, so each character becomes its own
    URL. Joining the fragments back together and matching against the known
    schema.org names recovers the intended list.
    """
    tail = 'https://schema.org/'
    letters = ''
    for value in values:
        if not isinstance(value, str):
            continue
        letters += value[len(tail):] if value.startswith(tail) else value

    # Drop separators the original string carried.
    letters = letters.replace(',', '').replace(' ', '')
    if not letters:
        return []

    found = []
    cursor = 0
    guard = 0
    while cursor < len(letters) and guard < 40:
        guard += 1
        for name in DIET_NAMES:
            if letters.startswith(name, cursor):
                found.append(tail + name)
                cursor += len(name)
                break
        else:
            cursor += 1

    return list(dict.fromkeys(found))


def _looks_fragmented(values):
    """True when a list is mostly single characters, i.e. an iterated string."""
    tail = 'https://schema.org/'
    if not isinstance(values, list) or len(values) < 4:
        return False
    short = 0
    for value in values:
        if not isinstance(value, str):
            return False
        body = value[len(tail):] if value.startswith(tail) else value
        if len(body.strip()) <= 2:
            short += 1
    return short >= len(values) * 0.6


def _repair_node(node):
    """Repair one JSON-LD object in place. Returns True if anything changed."""
    changed = False
    if not isinstance(node, dict):
        return changed

    diets = node.get('suitableForDiet')
    if _looks_fragmented(diets):
        rebuilt = _rebuild_diet(diets)
        if rebuilt:
            node['suitableForDiet'] = rebuilt
            changed = True
        else:
            node.pop('suitableForDiet', None)
            changed = True

    keywords = node.get('keywords')
    if isinstance(keywords, str):
        parts = [p.strip() for p in keywords.split(',')]
        # A fragmented keyword string reads as "c, h, i, c, k...".
        if parts and sum(1 for p in parts if len(p) <= 1) >= len(parts) * 0.6:
            joined = ''.join(parts)
            words = [w.strip() for w in joined.split(',') if w.strip()]
            node['keywords'] = ', '.join(words) if words else joined.strip()
            changed = True

    nutrition = node.get('nutrition')
    if isinstance(nutrition, dict):
        cleaned = {
            k: v for k, v in nutrition.items()
            if not (isinstance(v, str) and not v.strip())
        }
        if len(cleaned) != len(nutrition):
            if len(cleaned) <= 1:
                node.pop('nutrition', None)
            else:
                node['nutrition'] = cleaned
            changed = True

    return changed


def repair_jsonld(html):
    """Rewrite JSON-LD blocks whose list fields were built from a string."""
    if 'suitableForDiet' not in html and '"keywords"' not in html:
        return html, False

    pattern = re.compile(
        r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)',
        re.S | re.I,
    )
    touched = [0]

    def repl(match):
        raw = match.group(2).strip()
        try:
            data = json.loads(raw)
        except Exception:
            return match.group(0)

        nodes = data if isinstance(data, list) else [data]
        changed = False
        for node in nodes:
            if _repair_node(node):
                changed = True

        if not changed:
            return match.group(0)

        touched[0] += 1
        encoded = json.dumps(data, ensure_ascii=False, separators=(', ', ': '))
        return match.group(1) + encoded + match.group(3)

    return pattern.sub(repl, html), touched[0] > 0


# ---------------------------------------------------------------------------
# Reference pages
# ---------------------------------------------------------------------------

def _page_shell():
    """Borrow the shell of a generated page: head, header, footer, scripts.

    Reusing real output guarantees the new pages carry the same fonts,
    stylesheets, navigation and footer as everything else, without this script
    needing to know how build.py assembles a page.
    """
    for candidate in [
        DIST / 'kitchen-notes' / 'index.html',
        DIST / 'about' / 'index.html',
        DIST / 'index.html',
    ]:
        if not candidate.exists():
            continue
        try:
            html = candidate.read_text(encoding='utf-8')
        except Exception:
            continue
        if re.search(r'<main[^>]*>.*?</main>', html, re.S | re.I):
            return html
    return None


def _set_meta(html, title, description, canonical_path):
    html = re.sub(
        r'<title>.*?</title>',
        f'<title>{esc(title)} \u00b7 Bored of Toast</title>',
        html,
        count=1,
        flags=re.S | re.I,
    )

    for attr in ('name="description"', 'property="og:description"',
                 'name="twitter:description"'):
        html = re.sub(
            r'(<meta ' + re.escape(attr) + r' content=")[^"]*(")',
            lambda m: m.group(1) + esc(description, quote=True) + m.group(2),
            html,
        )

    for attr in ('property="og:title"', 'name="twitter:title"'):
        html = re.sub(
            r'(<meta ' + re.escape(attr) + r' content=")[^"]*(")',
            lambda m: m.group(1) + esc(title, quote=True) + m.group(2),
            html,
        )

    def fix_url(match):
        prefix, value, suffix = match.group(1), match.group(2), match.group(3)
        base = re.sub(r'/(kitchen-notes|about|recipes)(/.*)?$', '', value)
        return prefix + base.rstrip('/') + canonical_path + suffix

    html = re.sub(r'(<link rel="canonical" href=")([^"]*)(")', fix_url, html)
    html = re.sub(r'(<meta property="og:url" content=")([^"]*)(")', fix_url, html)

    return html


def build_reference_pages():
    """Write the reference pages defined in reference_content.py."""
    try:
        import reference_content as rc
    except Exception as exc:
        print(f'  skip: reference_content not importable ({exc})')
        return []

    shell = _page_shell()
    if not shell:
        print('  skip: no generated page to use as a shell')
        return []

    # Reference pages load their own stylesheet on top of the shared ones.
    if f'/{REFERENCE_CSS}' not in shell and '</head>' in shell:
        shell = shell.replace(
            '</head>',
            f'<link rel="stylesheet" href="/{REFERENCE_CSS}"></head>',
            1,
        )

    written = []
    for slug in rc.PAGES:
        try:
            data = rc.PAGES[slug]
            html = _set_meta(
                shell,
                data['title'],
                data['description'],
                f'/kitchen-notes/{slug}/',
            )

            html = re.sub(
                r'(<main[^>]*>).*?(</main>)',
                lambda m: m.group(1) + rc.body(slug) + m.group(2),
                html,
                count=1,
                flags=re.S | re.I,
            )

            # Replace any inherited structured data with this page's Article.
            html = re.sub(
                r'<script[^>]*application/ld\+json[^>]*>.*?</script>',
                '',
                html,
                flags=re.S | re.I,
            )
            ld = json.dumps(
                rc.article_jsonld(slug),
                ensure_ascii=False,
                separators=(', ', ': '),
            )
            if '</head>' in html:
                html = html.replace(
                    '</head>',
                    f'<script type="application/ld+json">{ld}</script></head>',
                    1,
                )

            target = DIST / 'kitchen-notes' / slug / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html, encoding='utf-8')
            written.append(slug)
        except Exception as exc:
            print(f'  warn: reference page {slug} failed: {exc}')

    return written


def add_reference_sitemap(written):
    """Add the new routes to sitemap.xml so they are discoverable."""
    if not written:
        return False
    path = DIST / 'sitemap.xml'
    if not path.exists():
        return False
    try:
        xml = path.read_text(encoding='utf-8')
    except Exception:
        return False

    existing = re.search(r'<loc>([^<]*)/kitchen-notes/', xml)
    base = existing.group(1) if existing else ''

    entries = ''
    for slug in written:
        loc = f'{base}/kitchen-notes/{slug}/'
        if loc in xml:
            continue
        entries += f'<url><loc>{loc}</loc><changefreq>monthly</changefreq></url>'

    if not entries or '</urlset>' not in xml:
        return False

    path.write_text(xml.replace('</urlset>', entries + '</urlset>', 1),
                    encoding='utf-8')
    return True


# ---------------------------------------------------------------------------
# Related recipes
# ---------------------------------------------------------------------------

def _time_bucket(r):
    digits = ''.join(c for c in str(r.get('total_time') or '') if c.isdigit())
    if not digits:
        return None
    mins = int(digits[:3])
    return 'quick' if mins <= 15 else ('medium' if mins <= 30 else 'long')


def _reason_candidates(current, other, cat_counts):
    """Rank the ways two recipes relate, most distinctive first.

    A shared rare category is a more interesting recommendation than a shared
    common one, so categories are ordered by how often they appear across the
    site. Returning a list lets the caller pick a reason that has not been
    used elsewhere in the same block.
    """
    candidates = []

    method_current = (current.get('method') or '').lower()
    method_other = (other.get('method') or '').lower()
    if method_other and method_other == method_current:
        label = METHOD_REASONS.get(method_other)
        if not label:
            label = 'Also ' + method_other
        candidates.append(label)

    shared = set(current.get('categories', [])) & set(other.get('categories', []))
    for cat in sorted(shared, key=lambda c: (cat_counts.get(c, 99), c)):
        candidates.append(
            CATEGORY_REASONS.get(cat, 'Also ' + cat.replace('-', ' '))
        )

    bucket = _time_bucket(current)
    if bucket and _time_bucket(other) == bucket:
        candidates.append(BUCKET_REASONS[bucket])

    candidates.append('From the notebook')

    seen = set()
    ordered = []
    for label in candidates:
        if label not in seen:
            seen.add(label)
            ordered.append(label)
    return ordered


def pick_related(current, all_recipes, limit=3):
    slug = current['slug']
    editorial = current.get('editorial_related')
    
    if editorial is not None:
        if not editorial:
            return []
            
        picked = []
        seen = {slug}
        valid = {r['slug']: r for r in all_recipes}
        
        for item in editorial:
            if isinstance(item, dict):
                r_slug = item.get('slug')
                reason = item.get('reason')
            else:
                r_slug = item
                reason = None
                
            if r_slug not in seen and r_slug in valid:
                r_copy = dict(valid[r_slug])
                if reason:
                    r_copy['editorial_reason'] = reason
                picked.append(r_copy)
                seen.add(r_slug)
            elif r_slug not in valid:
                print(f"  warn: invalid related recipe slug '{r_slug}' for '{slug}'")
                
            if len(picked) == limit:
                break
                
        return picked

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

    cat_counts = {}
    for r in all_recipes:
        for cat in r.get('categories', []):
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

    used_reasons = set()
    cards = ''
    for r in picks:
        stem = r.get('img') or ''
        img_html = ''
        if stem:
            img_html = (
                f'<img src="/assets/{esc(stem, quote=True)}-800.webp" '
                f'alt="{esc(r.get("alt") or r["title"], quote=True)}" '
                f'width="400" height="400" loading="lazy" decoding="async">'
            )

        reason = ''
        if r.get('editorial_reason'):
            reason = r['editorial_reason']
        else:
            for label in _reason_candidates(current, r, cat_counts):
                if label not in used_reasons:
                    reason = label
                    break
            if not reason:
                reason = 'From the notebook'
        used_reasons.add(reason)

        meta_parts = [
            _clean_meta_part(r.get('serves')),
            _clean_meta_part(r.get('total_time')),
            _clean_meta_part(r.get('method')),
        ]
        meta = ' \u00b7 '.join(p for p in meta_parts if p)

        meta_html = f'<span class="rr-meta">{esc(meta)}</span>' if meta else ''

        cards += (
            f'<a class="rr-card" href="/recipes/{esc(r["slug"], quote=True)}/">'
            f'<span class="rr-thumb">{img_html}</span>'
            f'<span class="rr-body">'
            f'<span class="rr-reason">{esc(reason)}</span>'
            f'<span class="rr-title">{esc(r["title"])}</span>'
            f'{meta_html}'
            f'</span></a>'
        )

    return (
        f'<section class="rr-block wrap" aria-labelledby="rr-heading">'
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
    reader and to an ad network review: a plain description of how recipes are
    actually produced, a clear point of contact for corrections, and no
    future-tense language about a site that is already live.

    Authorship is deliberately unnamed for now. That is a temporary state and
    should be revisited before applying to an ad network.

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
        'Found something that looks wrong? Tell us \u2197</a></p>'
        '</section>'

        '<section class="wrap section">'
        '<div class="section-top">'
        '<div><p class="eyebrow">WHO WRITES IT</p>'
        '<h2>A small operation.</h2></div>'
        '<p>No test kitchen, no staff of twenty, no sponsored recipes.</p>'
        '</div>'
        '<p>Bored of Toast is independently run. The same hands research, '
        'write and edit everything here, and fix it when something is wrong. '
        'Questions, corrections and suggestions all reach the same inbox, and '
        'they get read.</p>'
        '<p><a class="text-link" href="/contact/">Get in touch \u2197</a></p>'
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
    for name in ADDITIVE_CSS + [REFERENCE_CSS]:
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
        # reference.css is scoped to reference pages, not injected globally.
        if name == REFERENCE_CSS:
            continue
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

    bare = re.compile(r'\bBy\s+' + re.escape(AUTHOR_NAME) + r'\b\s*(\u00b7[^<]*)?')
    html, count = bare.subn('', html)
    if count:
        changed = True

    return html, changed


def strip_author_name(html):
    """Remove the author name from visible markup, leaving JSON-LD intact.

    Authorship is pending a decision. The name is still carried in the recipe
    structured data, so splitting on the JSON-LD blocks keeps the SEO signal
    while clearing the page copy.
    """
    if AUTHOR_NAME not in html:
        return html, False

    chunks = re.split(
        r'(<script[^>]*application/ld\+json[^>]*>.*?</script>)',
        html,
        flags=re.S | re.I,
    )
    changed = False
    for index, chunk in enumerate(chunks):
        if index % 2 == 1:
            continue
        if AUTHOR_NAME in chunk:
            cleaned = chunk.replace(', ' + AUTHOR_NAME + ',', '')
            cleaned = cleaned.replace('by ' + AUTHOR_NAME, '')
            cleaned = cleaned.replace(AUTHOR_NAME, '')
            cleaned = re.sub(r'\s{2,}', ' ', cleaned)
            chunks[index] = cleaned
            changed = True

    return ''.join(chunks), changed


def remove_start_here(html):
    pattern = re.compile(r'<a[^>]*href="/start-here/[^"]*"[^>]*>.*?</a>', re.I | re.S)
    new_html, count = pattern.subn('', html)
    return new_html, count > 0


def remove_where_to_begin(html):
    """Drop the "04 / Where to begin" home section."""
    pattern = re.compile(
        r'<section[^>]*class="[^"]*home-paths[^"]*"[^>]*>.*?</section>',
        re.I | re.S,
    )
    new_html, count = pattern.subn('', html)
    if count:
        return new_html, True

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

    The editorial note is the canonical statement. Image captions repeated it,
    which reads as unease rather than transparency. Runs in stages: strip
    caption-level sentences, then collapse any remaining duplicate paragraphs
    that carry the same disclosure text.
    """
    if not re.search(r'AI[- ]generated', html, re.I):
        return html, False

    changed = False

    # Stage one: caption sentences such as "Image is AI-generated."
    caption = re.compile(
        r'\s*(?:\u00b7\s*)?Images?\s+(?:is|are)\s+AI[- ]generated\.?',
        re.I,
    )
    html, count = caption.subn('', html)
    if count:
        changed = True

    # Stage two: identical disclosure paragraphs, keep the first.
    blocks = list(re.finditer(
        r'<(p|small|span|div)\b[^>]*>((?:(?!</?\1\b).)*?AI[- ]generated(?:(?!</?\1\b).)*?)</\1>',
        html,
        re.I | re.S,
    ))
    if len(blocks) > 1:
        seen_text = set()
        removals = []
        for block in blocks:
            signature = _strip_tags(block.group(2)).lower()
            if signature in seen_text:
                removals.append(block.span())
            else:
                seen_text.add(signature)
        for start, end in reversed(removals):
            html = html[:start] + html[end:]
            changed = True

    # Stage three: a badge plus an editorial note on the same page is still two.
    if len(re.findall(r'AI[- ]generated', html, re.I)) > 1:
        html, count = re.subn(
            r'\s*<span[^>]*class="[^"]*ai-badge[^"]*"[^>]*>.*?</span>',
            '',
            html,
            flags=re.I | re.S,
        )
        if count:
            changed = True

    return html, changed


def remove_development_leftovers(html):
    """Clear the last of the pre-launch labelling."""
    changed = False
    replacements = [
        (r'\s*<span aria-hidden="true">\u00b7</span>\s*Recipe in development', ''),
        (r'\s*\u00b7\s*Recipe in development', ''),
        (r'\s*<span[^>]*class="[^"]*dev-badge[^"]*"[^>]*>.*?</span>', ''),
    ]
    for pattern, repl in replacements:
        html, count = re.subn(pattern, repl, html, flags=re.I | re.S)
        if count:
            changed = True
    return html, changed


def _same_sentence(a, b):
    """Compare two swap notes ignoring punctuation and trailing qualifiers."""
    norm_a = re.sub(r'[^a-z0-9]+', '', a.lower())
    norm_b = re.sub(r'[^a-z0-9]+', '', b.lower())
    if not norm_a or not norm_b:
        return False
    return norm_a.startswith(norm_b) or norm_b.startswith(norm_a)


def dedupe_swap_prep(html):
    """Swap blocks repeated the same sentence under Adjust and Prep.

    The feta swap differed only by two trailing words, so an exact-match check
    left it in place. Prefix comparison catches that case.
    """
    pattern = re.compile(
        r'(<strong>Adjust:</strong>\s*)(.*?)(<br>\s*<strong>Prep:</strong>\s*)(.*?)'
        r'(?=</p>)',
        re.S,
    )

    hits = [0]

    def repl(m):
        adjust = _strip_tags(m.group(2)).strip()
        prep = _strip_tags(m.group(4)).strip()
        if adjust and prep and _same_sentence(adjust, prep):
            hits[0] += 1
            # Keep whichever version carries more detail.
            keep = m.group(2) if len(adjust) >= len(prep) else m.group(4)
            return m.group(1) + keep
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
    """"Serves 1 \u00b7 Chill overnight" hid the five minutes of actual work."""
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
    ('author name', strip_author_name),
    ('jsonld repair', repair_jsonld),
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

    # Reference pages are written before the transform loop so they receive
    # the same stylesheet injection and cleanup as every other page.
    try:
        written = build_reference_pages()
        if written:
            print(f'  reference pages: {", ".join(written)}')
            if add_reference_sitemap(written):
                print('  sitemap updated')
    except Exception as exc:
        print(f'  warn: reference pages failed: {exc}')

    recipes = collect_recipes()
    print(f'  recipes indexed: {len(recipes)}')
    for r in recipes[:3]:
        preview = ' \u00b7 '.join(
            p for p in [r['serves'], r['total_time'], r['method']] if p
        )
        print(f'    {r["slug"]}: {preview or "(no meta)"}')

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
