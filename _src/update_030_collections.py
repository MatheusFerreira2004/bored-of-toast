#!/usr/bin/env python3
"""Recipe collections: a /collections/ hub and 5 list pages built from existing recipes.

- protein-first-breakfasts, soft-and-gentle, freezer-friendly, sips, small-snacks
- No new photos: each page reuses the photo of a recipe already on the site.
- Links: footer ("Collections"), a short strip on /recipes/ (text links only, the page is already heavy),
  and the GLP-1 Kitchen hub link that pointed to the removed "small-plates" filter.
- The collection code is added to build.py; the pages are written after the main build and added to sitemap.xml.

Nothing is saved unless every collection has at least 4 existing recipes and the required anchors are found.
Safe to re-run.
"""
import json, os, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)

b = open(P('build.py'), encoding='utf-8').read()
if 'COLLECTIONS = ' in b:
    print('Already applied. Nothing to do.')
    sys.exit(0)

COLLECTIONS = [
    {
        'id': 'protein-first-breakfasts',
        'title': 'Protein-First Breakfasts',
        'h1': 'Protein-first<br><em>breakfasts.</em>',
        'subtitle': 'Eggs, yogurt and cottage cheese in small portions, for the easiest meal of the day to fit protein into.',
        'desc': 'Small, protein-first breakfast recipes: eggs, Greek yogurt and cottage cheese in portions you can finish, with estimated protein per serving.',
        'lead': 'Breakfast is often the easiest place to fit protein in. These recipes keep portions small and put eggs, yogurt or cottage cheese first.',
        'intro': ['Several of these can be made ahead, so a small breakfast is ready even on slow mornings. Protein per serving is listed on every recipe as an estimate.'],
        'cover': 'cottage-cheese-scrambled-eggs',
        'ids': ['cottage-cheese-scrambled-eggs', 'greek-yogurt-berry-parfaits', 'strawberry-cottage-cheese-bowl', 'shakshuka',
                'avocado-toast-jammy-eggs', 'spinach-feta-mini-frittata', 'cottage-cheese-pancakes', 'smoked-salmon-bagel-halves',
                'overnight-oats', 'breakfast-burritos', 'savory-cottage-cheese-bowl', 'greek-yogurt-chia-pudding', 'berry-greek-yogurt-muffins'],
    },
    {
        'id': 'soft-and-gentle',
        'title': 'Soft and Gentle Small Plates',
        'h1': 'Soft and gentle<br><em>small plates.</em>',
        'subtitle': 'Smooth soups, soft eggs and spoonable puddings for days when chewing and strong flavors feel like too much.',
        'desc': 'Soft, mild recipes with protein for harder days: congee, smooth soups, soft eggs and puddings, in small portions.',
        'lead': 'For the days when you want food that asks very little of you: soft, mild, warm or cool, and easy to stop halfway.',
        'intro': ['Each recipe includes a gentler swap. For more ideas, read the Soft Foods for Hard Days guide in the GLP-1 Kitchen. If you have trouble swallowing or follow a medical texture plan, follow your care team\'s guidance.'],
        'cover': 'chicken-rice-congee',
        'ids': ['chicken-rice-congee', 'cottage-cheese-mashed-potatoes', 'ginger-egg-drop-soup', 'protein-rice-pudding',
                'greek-yogurt-chia-pudding', 'tomato-basil-soup', 'butternut-squash-soup', 'red-lentil-lemon-soup',
                'split-pea-soup', 'cottage-cheese-scrambled-eggs', 'chocolate-yogurt-mousse-cups', 'overnight-oats'],
    },
    {
        'id': 'freezer-friendly',
        'title': 'Freezer-Friendly Small Plates',
        'h1': 'Freezer-friendly<br><em>small plates.</em>',
        'subtitle': 'Cook once on a good day, freeze in small portions, and reheat one when you need it.',
        'desc': 'Freezer-friendly recipes in small portions: soups, stews, meatballs, burritos and breakfasts that reheat well.',
        'lead': 'Soups, stews, meatballs and breakfasts that freeze well in 1-cup portions, so a ready meal is always waiting.',
        'intro': ['Check the storage notes on each recipe: some parts, like pasta or yogurt toppings, are best added when you reheat. The Freezer Basics guide in the GLP-1 Kitchen covers labeling, thawing and safe reheating.'],
        'cover': 'split-pea-soup',
        'ids': ['split-pea-soup', 'red-lentil-lemon-soup', 'chicken-minestrone', 'tomato-white-bean-stew', 'chickpea-black-bean-chili',
                'turkey-meatballs-tomato-sauce', 'breakfast-burritos', 'butternut-squash-soup', 'tomato-basil-soup',
                'cottage-cheese-pancakes', 'berry-greek-yogurt-muffins'],
    },
    {
        'id': 'sips',
        'title': 'Sips for Low-Appetite Days',
        'h1': 'Sips for<br><em>low-appetite days.</em>',
        'subtitle': 'Small smoothies, a warm latte and a light soup you can sip slowly when solid food is hard.',
        'desc': 'Sippable recipes with protein for low-appetite days: Greek yogurt smoothies, a golden milk latte and ginger egg drop soup.',
        'lead': 'When chewing feels like work, something you can sip slowly may be easier. These are small servings built around protein.',
        'intro': ['The smoothies use Greek yogurt instead of protein powder; powder is an optional boost. The Smoothies That Actually Fill You guide explains the formula.'],
        'cover': 'strawberry-protein-smoothie',
        'ids': ['strawberry-protein-smoothie', 'banana-protein-smoothie', 'mixed-berry-protein-smoothie', 'golden-milk-latte', 'ginger-egg-drop-soup'],
    },
    {
        'id': 'small-snacks',
        'title': 'Small Snacks with Protein',
        'h1': 'Small snacks<br><em>with protein.</em>',
        'subtitle': 'Dips, bites and bars in small portions, for when a full meal is too much.',
        'desc': 'Small snacks with protein: yogurt dips, deviled eggs, edamame, frozen yogurt bars and no-bake protein bites.',
        'lead': 'Small and often works. These snacks keep a little protein within reach between meals.',
        'intro': ['Most of these keep in the fridge or freezer for several days, so you can make a batch and grab one when you need it.'],
        'cover': 'garlic-sesame-edamame',
        'ids': ['garlic-sesame-edamame', 'yogurt-hummus', 'tzatziki-yogurt-dip', 'bacon-deviled-eggs', 'frozen-yogurt-berry-bars', 'peanut-butter-protein-bites'],
    },
]

# ------------------------------------------------------------------ validate against recipes.json
recipes = json.load(open(P('recipes.json'), encoding='utf-8'))
ids = {r['id'] for r in recipes}
for c in COLLECTIONS:
    missing = [i for i in c['ids'] if i not in ids]
    if missing:
        print(f"- note: {c['id']} skips missing recipes {missing}")
    c['ids'] = [i for i in c['ids'] if i in ids]
    if len(c['ids']) < 4:
        print(f"ERROR: collection {c['id']} has only {len(c['ids'])} recipes. Nothing was saved.")
        sys.exit(1)
    if c['cover'] not in ids:
        c['cover'] = c['ids'][0]
    print(f"- {c['id']}: {len(c['ids'])} recipes")

# ------------------------------------------------------------------ code added to build.py
CODE = r'''
# ---------------------------------------------------------------- collections (added by update_030)
COLLECTIONS = __COLL__

def _coll_recipes(c):
    return [BY_ID[i] for i in c['ids'] if i in BY_ID and i not in RECIPE_REDIRECTS]

def collection_card(root, c):
    rs = _coll_recipes(c)
    cov = BY_ID.get(c.get('cover')) or rs[0]
    img = cov['img']
    return ('<a class="guide-card reveal" href="' + root + 'collections/' + c['id'] + '/">'
            '<div class="guide-img"><img src="' + root + img + '" alt="' + e(c['title']) + '" loading="lazy" width="600" height="450"' + rimg(root, img, SIZES['guide']) + '></div>'
            '<div class="guide-body"><span class="tag">Collection · ' + str(len(rs)) + ' recipes</span><h3>' + e(c['title']) + '</h3><p>' + e(c['subtitle']) + '</p><span class="view-all">See the collection →</span></div></a>')

def collections_strip(root):
    links = ''.join('<a class="pill" href="' + root + 'collections/' + c['id'] + '/">' + e(c['title']) + '</a>' for c in COLLECTIONS)
    return ('<section class="section" style="padding-bottom:0">' + section_head('Browse a collection', 'Hand-picked lists for the way you feel today.', '<a href="' + root + 'collections/" class="view-all">All collections →</a>')
            + '<div class="pills">' + links + '</div></section>')

def build_collections():
    root = '../'
    hub = hero_bleed(root, 'images/greek-yogurt-berry-parfaits.webp', 'Recipe collections', 'Small plates,<br><em>sorted for you.</em>',
        'Hand-picked lists from the recipe library: protein-first breakfasts, soft foods for hard days, freezer-friendly meals, sips and small snacks. Every recipe lists estimated protein per serving.',
        '<a href="' + root + 'recipes/" class="btn btn-yellow">All recipes ' + ICON['arrow'] + '</a><a href="' + root + 'starter-kit/" class="btn btn-ghost">Get the free starter kit</a>', short=True)
    body = (hub + '<section class="container section">' + section_head('Pick a collection', 'Each list links to full recipes with small-portion tips and gentler swaps.')
            + '<div class="guide-grid">' + ''.join(collection_card(root, c) for c in COLLECTIONS) + '</div></section>' + marketing_block(root, 'free'))
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE_URL + 'collections/' + c['id'] + '/'} for i, c in enumerate(COLLECTIONS)]}]
    page('collections/', 'Recipe Collections | Bored of Toast', 'Hand-picked recipe collections for small appetites: protein-first breakfasts, soft foods, freezer-friendly meals, sips and small snacks.', body, 'recipes', root, jsonld=ld)
    r2 = '../../'
    for c in COLLECTIONS:
        rs = _coll_recipes(c)
        cov = BY_ID.get(c.get('cover')) or rs[0]
        hero = hero_bleed(r2, cov['img'], 'Collection · ' + str(len(rs)) + ' recipes', c['h1'], e(c['lead']),
            '<a href="#list" class="btn btn-yellow">See the recipes ' + ICON['down'] + '</a><a href="' + r2 + 'collections/" class="btn btn-ghost">All collections</a>', short=True)
        intro = ''.join('<p>' + e(p) + '</p>' for p in c['intro'])
        others = [x for x in COLLECTIONS if x['id'] != c['id']][:3]
        body = (hero + '<section class="container section" id="list"><div class="lead" style="max-width:760px;margin-bottom:28px">' + intro + '</div>'
                + '<div class="recipe-grid">' + ''.join(card(r2, r, eager=i < 4) for i, r in enumerate(rs)) + '</div>'
                + '<p class="fine" style="margin-top:24px">Protein values are estimates per serving. General cooking education, not medical or nutrition advice.</p></section>'
                + marketing_block(r2, 'free')
                + '<section class="container related">' + section_head('More collections', '', '<a href="' + r2 + 'collections/" class="view-all">All collections →</a>')
                + '<div class="guide-grid">' + ''.join(collection_card(r2, x) for x in others) + '</div></section>')
        ld = [{"@context": "https://schema.org", "@type": "ItemList", "name": c['title'], "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE_URL + 'recipes/' + r['id'] + '/'} for i, r in enumerate(rs)]}]
        page('collections/' + c['id'] + '/', c['title'] + ' | Bored of Toast', c['desc'], body, 'recipes', r2, og='images/og/' + cov['id'] + '.jpg', jsonld=ld)

'''.replace('__COLL__', json.dumps(COLLECTIONS))

TAIL = r'''

# ---------------------------------------------------------------- collections pages (added by update_030)
build_collections()
_sm = os.path.join(OUT, 'sitemap.xml')
if os.path.exists(_sm):
    _x = open(_sm, encoding='utf-8').read()
    _urls = ['collections/'] + ['collections/' + c['id'] + '/' for c in COLLECTIONS]
    _add = ''.join('<url><loc>' + SITE_URL + u + '</loc></url>\n' for u in _urls if (SITE_URL + u + '<') not in _x)
    if _add and '</urlset>' in _x:
        open(_sm, 'w', encoding='utf-8').write(_x.replace('</urlset>', _add + '</urlset>'))
print(f'built {len(COLLECTIONS)} collections')
'''

ANCHOR = 'def build_recipes():'
if b.count(ANCHOR) != 1:
    print('ERROR: build_recipes() not found in build.py. Nothing was saved.')
    sys.exit(1)
b = b.replace(ANCHOR, CODE.lstrip('\n') + '\n' + ANCHOR)

CTA = '  <div class="cta reveal" style="margin-top:72px">'
if b.count(CTA) == 1:
    b = b.replace(CTA, '  {collections_strip(root)}\n' + CTA)
    print('- recipes page: collections strip added')
else:
    print('- note: recipes page strip not added (anchor not found)')

FOOT = "    nav += f'<li><a href=\"{root}starter-kit/\">Free GLP-1 kit</a></li>'\n"
if b.count(FOOT) == 1:
    b = b.replace(FOOT, FOOT + "    nav += f'<li><a href=\"{root}collections/\">Collections</a></li>'\n")
    print('- footer: Collections link added')
else:
    print('- note: footer link not added (anchor not found)')

OLD_HUB = "f'<a href=\"{root}recipes/?cat=small-plates\" class=\"view-all\">All small plates →</a>'"
NEW_HUB = "f'<a href=\"{root}collections/\" class=\"view-all\">Browse collections →</a>'"
if b.count(OLD_HUB) == 1:
    b = b.replace(OLD_HUB, NEW_HUB)
    print('- GLP-1 Kitchen hub: link now points to collections')

b = b.rstrip('\n') + '\n' + TAIL
open(P('build.py'), 'w', encoding='utf-8').write(b)
print(f'OK: {len(COLLECTIONS)} collections added.')
