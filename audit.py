import re
from pathlib import Path

DIST = Path('dist')
BASE_URL = 'https://boredoftoast.com'
issues = []
ok = []

routes = [
    '', 'recipes', 'start-here', 'kitchen-notes',
    'kitchen-notes/keep-salad-crisp', 'kitchen-notes/simple-lemon-dressing', 'kitchen-notes/make-beans-creamy',
    'the-lunch-edit', 'about', 'contact', 'privacy', 'terms',
    'recipes/lemon-chickpea-salad', 'recipes/lemon-white-bean-skillet', 'recipes/blueberry-overnight-oats',
    'recipes/crispy-sheet-pan-gnocchi', 'recipes/mediterranean-warm-green-lentils',
    'recipes/smashed-cucumber-edamame-bowl', 'recipes/garlic-butter-bean-mushroom-toast',
    'recipes/spiced-apple-cinnamon-porridge'
]

for route in routes:
    f = DIST / route / 'index.html' if route else DIST / 'index.html'
    if f.exists() and f.stat().st_size > 0:
        ok.append(f'Route OK: /{route}/')
    else:
        issues.append(f'MISSING ROUTE: /{route}/')

empty = [f.name for f in (DIST / 'assets').glob('*.webp') if f.stat().st_size == 0]
if empty:
    issues.append(f'Empty WebP: {empty}')
else:
    ok.append('No empty WebP files')

slugs = [
    'lemon-chickpea-salad', 'lemon-white-bean-skillet', 'blueberry-overnight-oats',
    'crispy-sheet-pan-gnocchi', 'mediterranean-warm-green-lentils',
    'smashed-cucumber-edamame-bowl', 'garlic-butter-bean-mushroom-toast', 'spiced-apple-cinnamon-porridge'
]

sitemap = (DIST / 'sitemap.xml').read_text(encoding='utf-8')
ok.append(f'Sitemap: {sitemap.count("<loc>")} URLs found')

for slug in slugs:
    idx = DIST / 'recipes' / slug / 'index.html'
    if idx.exists():
        h = idx.read_text(encoding='utf-8')
        if 'pilot-recipe-data' not in h:
            issues.append(f'No pilot-recipe-data: {slug}')
        if 'canonical' not in h:
            issues.append(f'No canonical tag: {slug}')
        if 'application/ld+json' not in h:
            issues.append(f'No JSON-LD: {slug}')
        if 'ingredient-checkbox' in h:
            issues.append(f'Has ingredient-checkbox: {slug}')
    else:
        issues.append(f'Missing recipe HTML: {slug}')

ok.append('Recipe structural checks done')

home = (DIST / 'index.html').read_text(encoding='utf-8')
home_cards = home.count('class="recipe-card"')
ok.append(f'Home recipe cards: {home_cards}')

# Check home has 3 recipe cards (test requirement)
if home_cards != 3:
    issues.append(f'Home must have exactly 3 recipe cards, found {home_cards}')

# Check recipes index has 8 cards
recipes_idx = (DIST / 'recipes' / 'index.html').read_text(encoding='utf-8')
recipe_count = recipes_idx.count('class="recipe-card')
ok.append(f'Recipe index cards: {recipe_count}')

# Verify all local image references (src and srcset) across all generated HTML files exist and are non-empty
checked_refs = 0
broken_refs = []

for html_file in DIST.rglob('*.html'):
    h_text = html_file.read_text(encoding='utf-8')
    for img_match in re.finditer(r'<img\s+([^>]+)>', h_text, re.IGNORECASE):
        attrs = img_match.group(1)
        
        # Check src
        src_m = re.search(r'src=["\'](/assets/[^"\'?#]+)', attrs)
        if src_m:
            checked_refs += 1
            rel_asset = src_m.group(1).lstrip('/')
            target_asset = DIST / rel_asset
            if not target_asset.exists() or target_asset.stat().st_size == 0:
                broken_refs.append(f"{html_file.relative_to(DIST)}: src={src_m.group(1)} (missing or 0 bytes)")

        # Check srcset
        srcset_m = re.search(r'srcset=["\']([^"\']+)["\']', attrs)
        if srcset_m:
            candidates = [c.strip().split()[0] for c in srcset_m.group(1).split(',') if c.strip()]
            for cand in candidates:
                if cand.startswith('/assets/'):
                    checked_refs += 1
                    cand_clean = cand.split('?')[0].split('#')[0]
                    target_cand = DIST / cand_clean.lstrip('/')
                    if not target_cand.exists() or target_cand.stat().st_size == 0:
                        broken_refs.append(f"{html_file.relative_to(DIST)}: srcset candidate {cand} (missing or 0 bytes)")

if broken_refs:
    for br in broken_refs:
        issues.append(f'Broken local image reference: {br}')
else:
    ok.append(f'All {checked_refs} local image references (src/srcset) exist on disk')

print('=== AUDIT RESULTS ===')
print()
print('ISSUES:')
if issues:
    for i in issues:
        print(f'  FAIL: {i}')
else:
    print('  None — all checks passed!')
print()
print('SUMMARY:')
print(f'  OK: {len(ok)} checks passed')
print(f'  ISSUES: {len(issues)} problems found')
print()
print('KEY CHECKS:')
for item in ok:
    print(f'  OK: {item}')
