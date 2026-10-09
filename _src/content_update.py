#!/usr/bin/env python3
"""One-off content update: Bored of Toast -> "Small plates, big protein" (GLP-1 focus).

Edits the _src sources only (build.py, recipes.json and, where the text is found, storefront.py
and guides_legal.json). Layout, CSS, fonts and components are not touched.

Run from the project root:
    python3 _src/content_update.py
    mkdir -p _src/site && cp -r images _src/site/images && python3 _src/build.py
    then copy _src/site/* (except images) to the project root (same as checks.yml asks).

Safe to re-run: exits early if the update was already applied.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)


def log(s):
    print(s)


build_path = P('build.py')
src = open(build_path, encoding='utf-8').read()
if 'FOCUS_IDS' in src:
    log('Content update already applied. Nothing to do.')
    sys.exit(0)

recipes_raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(recipes_raw)
ids = [r['id'] for r in recipes]
burrito = next((i for i in ids if 'burrito' in i), None)

# Recipes that fit the new editorial line (small portions, protein, gentle options).
FOCUS = ['lemon-chicken-orzo-soup', 'sheet-pan-salmon', 'chicken-avocado-salad', 'shakshuka',
         'overnight-oats', 'avocado-toast-jammy-eggs', 'butternut-squash-soup', 'tomato-basil-soup',
         'mediterranean-grain-bowl']
if burrito:
    FOCUS.insert(5, burrito)
missing = [i for i in FOCUS if i not in ids]
if missing:
    sys.exit(f'ERROR: recipe ids not found in recipes.json: {missing}')

log('## Content update report\n')
log(f'Focus recipes: {", ".join(FOCUS)}\n')


# ------------------------------------------------------------------ build.py (required changes)
def req(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        sys.exit(f'ERROR: expected {count} match(es) in build.py, found {n}:\n{old[:160]}')
    src = src.replace(old, new)


# Shared list of focus recipes + new categories
new_cats = '''FOCUS_IDS = %s

CATS = [
    ('high-protein', 'High Protein', 'sheet-pan-salmon'),
    ('small-plates', 'Small Plates', 'avocado-toast-jammy-eggs'),
    ('gentle', 'Gentle', 'tomato-basil-soup'),
    ('make-ahead', 'Make-Ahead', 'overnight-oats'),
    ('Soups', 'Soups', 'butternut-squash-soup'),
    ('Beyond Toast', 'Beyond Toast', 'shakshuka'),
    ('everyday', 'Everyday Favorites', 'creamy-garlic-pasta'),
]''' % json.dumps(FOCUS)
src, n = re.subn(r"CATS = \[\n.*?\n\]", lambda m: new_cats, src, count=1, flags=re.S)
if n != 1:
    sys.exit('ERROR: CATS block not found in build.py')

# Home: hero
req("wk = BY_ID['creamy-garlic-pasta']", "wk = BY_ID['lemon-chicken-orzo-soup']")
req("['Tested at home', 'Everyday ingredients', 'Step-by-step guides']",
    "['Small portions', 'Gentle swaps', 'Everyday ingredients']")
req("'Recipes · Tips · Inspiration', 'Good food,<br><em>every day.</em>',",
    "'High protein · Small plates · Gentle food', 'Small plates,<br><em>big protein.</em>',")
req("'Simple, delicious recipes made for real life: easy enough for a weekday, special enough for the weekend.',",
    "'Simple recipes with the protein counted, in portions you can actually finish. Made for small appetites, busy days and everything in between.',")
req('<button class="btn btn-ghost" data-random>Surprise me</button>',
    '<a href="{root}starter-kit/" class="btn btn-ghost">Get the free starter kit</a>')

# Home: marquee
req("['Fresh ingredients', 'Simple steps', 'Better breakfasts', 'Weeknight dinners', 'Cozy soups', 'Sweet treats', 'No fuss']",
    "['High protein', 'Small portions', 'Cold & gentle', 'Make-ahead', 'No-cook', 'Freezer-friendly']")

# Home: free starter kit moves to right after the hero
req("{marketing_block(root, 'free')}", '')
req('{hero}{marquee}\n', "{hero}{marquee}\n{marketing_block(root, 'free')}\n")

# Home: categories
req("'From ten-minute breakfasts to weekend baking projects.'",
    "'From five-minute breakfasts to freezer-friendly soups.'")

# Home: signature section
fourth = burrito or 'buttermilk-pancakes'
req("['buttermilk-pancakes', 'shakshuka', 'avocado-toast-jammy-eggs', 'overnight-oats']",
    f"['shakshuka', 'avocado-toast-jammy-eggs', 'overnight-oats', '{fourth}']")
req('Breakfast deserves better than the same slice every morning. Fluffy pancakes, eggs baked in spicy tomato sauce, oats that make themselves overnight, and yes, avocado toast done properly.',
    'Breakfast is the easiest place to fit protein in. Eggs that barely need chewing, oats that make themselves overnight, and yes, avocado toast with a jammy egg on top.')

# Home: "latest" grid becomes the focus recipes
req('latest = [BY_ID[i] for i in NEW_IDS]', 'latest = [BY_ID[i] for i in FOCUS_IDS[:8]]')
req("section_head('Fresh from our kitchen', 'The newest recipes, tested and ready for yours.',",
    "section_head('Small plates to start with', 'Smaller portions, protein listed, gentler swaps included.',")

# Home: SEO
req("'Bored of Toast | Good food, every day', 'Simple, delicious, tested recipes made for real life: easy enough for a weekday, special enough for the weekend.'",
    "'Bored of Toast | Small plates, big protein', 'Simple high-protein recipes in small portions, with protein per serving and gentler swaps for low-appetite days.'")

# Recipes page
req("'The recipe library', 'Explore, cook,<br><em>enjoy.</em>',",
    "'The recipe library', 'Find your next<br><em>small plate.</em>',")
req("f'{len(RECIPES)} tested recipes for every kind of day, each with step-by-step instructions, tips, swaps and storage notes.',",
    "f'{len(RECIPES)} recipes with step-by-step instructions, protein per serving and storage notes. Featured recipes add a small-portion tip and a gentler swap.',")
req("f'Browse {len(RECIPES)} simple, tested recipes: breakfasts, weeknight dinners, soups, salads and desserts.'",
    "'High-protein recipes in small portions: breakfasts, soups, small plates and make-ahead meals, with gentler swaps.'")

# Recipe pages: starter-kit link on every focus recipe; stamp text
req("if r['id'] in ['overnight-oats', 'tomato-basil-soup', 'lemon-chicken-orzo-soup', 'mediterranean-grain-bowl', 'chicken-avocado-salad'] else ''",
    "if r['id'] in FOCUS_IDS else ''")
req('GOOD FOOD • NO FUSS • TESTED AT HOME •', 'SMALL PLATES • BIG PROTEIN • NO FUSS •')

# Footer (every page)
req('Good food without the fuss. Simple, tested recipes for real life.',
    'Small plates, big protein. Simple recipes for small appetites.')
req('<span>© {datetime.date.today().year} Bored of Toast. All rights reserved.</span>',
    '<span>© {datetime.date.today().year} Bored of Toast. All rights reserved. General cooking education, not medical or nutrition advice.</span>')

open(build_path, 'w', encoding='utf-8').write(src)
log('build.py: all required text changes applied.\n')

# ------------------------------------------------------------------ recipes.json
GENTLE = {'lemon-chicken-orzo-soup', 'butternut-squash-soup', 'tomato-basil-soup', 'overnight-oats', 'avocado-toast-jammy-eggs'}
MAKE_AHEAD = {'overnight-oats', 'lemon-chicken-orzo-soup', 'butternut-squash-soup', 'tomato-basil-soup', 'mediterranean-grain-bowl'}
if burrito:
    MAKE_AHEAD.add(burrito)

SMALL_TIP = 'Small-portion tip: serve half a portion and save the rest for later. A half bowl still counts.'
SWAPS = {
    'lemon-chicken-orzo-soup': ('Serve it warm rather than hot, and go light on the lemon on unsettled days.',
                                'Stir a spoonful of plain Greek yogurt into your bowl.'),
    'sheet-pan-salmon': ('Serve the salmon at room temperature. Cooler food tends to smell less.',
                         'Serve with a spoonful of plain Greek yogurt mixed with lemon and dill.'),
    'chicken-avocado-salad': ('Shred the chicken instead of slicing it, and leave out raw onion or a strong dressing.',
                              'Add a soft-boiled egg or a handful of shelled edamame.'),
    'shakshuka': ('Use mild paprika instead of chili and let the sauce cool a little before eating.',
                  'Crack in one extra egg, or serve with a spoonful of plain Greek yogurt.'),
    'overnight-oats': ('Already cold and soft. Eat half the jar now and keep the rest for later.',
                       'Swap half of the milk for plain Greek yogurt.'),
    'avocado-toast-jammy-eggs': ('Use one slice instead of two and keep the egg soft and jammy.',
                                 'Spread a spoonful of cottage cheese under the avocado.'),
    'butternut-squash-soup': ('Serve it warm in a mug and sip it slowly.',
                              'Blend in silken tofu, or top with plain Greek yogurt.'),
    'tomato-basil-soup': ('Serve it warm, not hot, and skip extra garlic or chili.',
                          'Blend in a can of rinsed white beans, or top with plain Greek yogurt.'),
    'mediterranean-grain-bowl': ('Serve a half bowl and leave out raw onion.',
                                 'Add extra chickpeas or a soft-boiled egg.'),
}
if burrito:
    SWAPS[burrito] = ('Eat half a burrito at a time and skip hot sauce on queasy days.',
                      'Add extra egg whites to the scramble.')

counts = {}
for r in recipes:
    tags = r.setdefault('tags', [])

    def add(t):
        if t not in tags:
            tags.append(t)
            counts[t] = counts.get(t, 0) + 1

    prot = (r.get('nutrition') or {}).get('protein')
    if isinstance(prot, (int, float)) and prot >= 15:
        add('high-protein')   # same definition as the Nourished guide: 15 g or more per serving
    if r['id'] in FOCUS:
        add('small-plates')
        if r['id'] in GENTLE:
            add('gentle')
        if r['id'] in MAKE_AHEAD:
            add('make-ahead')
        tips = r.setdefault('tips', [])
        if SMALL_TIP not in tips:
            tips.append(SMALL_TIP)
        gentler, boost = SWAPS[r['id']]
        variations = r.setdefault('variations', [])
        variations.append(['Make it gentler', gentler])
        variations.append(['Protein boost', boost])
    else:
        add('everyday')

m = re.match(r'\[\s*\n([ \t]+)\{', recipes_raw)
indent = len(m.group(1)) if m else None
with open(P('recipes.json'), 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=indent)
    f.write('\n')
log('recipes.json: tags added ' + ', '.join(f'{k}={v}' for k, v in sorted(counts.items())) + '\n')


# ------------------------------------------------------------------ optional changes (other files)
def opt(path, pairs, allow_multi=False):
    p = P(path)
    if not os.path.exists(p):
        log(f'- SKIPPED, file not found: {path}')
        return
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        n = s.count(old)
        if n == 1 or (n > 1 and allow_multi):
            s = s.replace(old, new)
            log(f'- OK ({path}, {n}x): {old[:70]}')
        elif n > 1:
            log(f'- SKIPPED, {n} matches ({path}): {old[:70]}')
    open(p, 'w', encoding='utf-8').write(s)


ABOUT = [
    ("We believe great food doesn't have to be complicated. Bored of Toast is here to make everyday cooking easier, more enjoyable and a little more delicious.",
     'Eating less shouldn’t mean eating badly. We make small, high-protein meals simple, practical and still delicious.'),
    ("We believe great food doesn\\'t have to be complicated. Bored of Toast is here to make everyday cooking easier, more enjoyable and a little more delicious.",
     'Eating less shouldn’t mean eating badly. We make small, high-protein meals simple, practical and still delicious.'),
    ("We believe great food doesn't have to be complicated. Meet the kitchen behind Bored of Toast.",
     'Bored of Toast shares small, high-protein recipes for small appetites, with gentle options for harder days.'),
    ("We believe great food doesn\\'t have to be complicated. Meet the kitchen behind Bored of Toast.",
     'Bored of Toast shares small, high-protein recipes for small appetites, with gentle options for harder days.'),
    ('We were tired of eating the same thing every night, so we started collecting the recipes that got us excited to cook again.',
     'Over time, the question changed: what do you cook when your appetite is small but your body still needs protein?'),
    ('What began as a small collection of favorites has grown into a place for home cooks, food lovers and anyone who believes that good food makes life better.',
     'That’s the kitchen we write for now: people eating smaller portions, people on GLP-1 medication, and anyone who has opened the fridge and found that nothing sounds good.'),
    ('Every recipe here is cooked in a real home kitchen, written in plain language and tested until it works every single time.',
     'Every recipe here is written in plain language, with a smaller portion in mind and a gentler option for harder days.'),
    ("And we're here for every meal, big or small.", 'And we’re here for every meal, especially the small ones.'),
    ("And we\\'re here for every meal, big or small.", 'And we’re here for every meal, especially the small ones.'),
    ('Our passion is', 'Good food,'),
    ('<em>good food.</em>', '<em>in smaller bites.</em>'),
]
STORE = [
    ('89 pages', '60 pages'),
    ('26 pages', '9 pages'),
    ('18 pages', '14 pages'),
    ('Continue into Weeks 3–4 with more meal examples, shopping checklists and prep plans.',
     'All four weeks in one file: Weeks 1–4 with daily meal examples and a shopping list for each week.'),
]

log('Optional replacements (only applied where the exact text exists):')
for f in ['build.py', 'guides_legal.json', 'storefront.py']:
    opt(f, ABOUT)
for f in ['storefront.py', 'build.py']:
    opt(f, STORE)
    opt(f, [('Meal Plan Companion', '28-Day Meal Plan')], allow_multi=True)

# ------------------------------------------------------------------ remaining "tested" claims
log('\nRemaining mentions of "tested" in _src (review manually):')
found = False
for name in sorted(os.listdir(HERE)):
    if not name.endswith(('.py', '.json')) or name == 'content_update.py':
        continue
    for i, line in enumerate(open(P(name), encoding='utf-8'), 1):
        if re.search(r'\btested\b', line, re.I):
            found = True
            idx = re.search(r'\btested\b', line, re.I).start()
            log(f'- {name}:{i}: ...{line[max(0, idx - 60):idx + 60].strip()}...')
if not found:
    log('- none')
log('\nDone.')
