#!/usr/bin/env python3
"""Guides become the GLP-1 Kitchen hub (same URL: /guides/).

- Three new guides replace pantry staples, perfect rice and knife skills:
  nothing-sounds-good, protein-first, small-portion-meal-prep.
- Old guide URLs become redirect stubs (no broken links):
  pantry-staples -> small-portion-meal-prep, perfect-rice -> protein-first, knife-skills -> /guides/.
- /guides/ becomes the GLP-1 Kitchen hub: guides, free starter kit, focus recipes, Nourished.
  The "coming soon" promise is removed.
- Menu label "Guides" -> "GLP-1 Kitchen"; home section and guide pages renamed.
- checks.py: the three stubs are registered as redirect stubs.

Guides are general cooking education. Protein values are marked as estimates.
Nothing is saved unless every required change is found. Safe to re-run.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)

b = open(P('build.py'), encoding='utf-8').read()
if 'GUIDE_REDIRECTS' in b:
    print('Already applied. Nothing to do.')
    sys.exit(0)

# ------------------------------------------------------------------ guides content
GUIDES = [
    {
        'id': 'nothing-sounds-good',
        'title': 'What to Eat When Nothing Sounds Good',
        'subtitle': 'Gentle, small, mostly no-cook ideas for low-appetite days, and a few habits that make eating a little easier.',
        'category': 'GLP-1 Kitchen',
        'readTime': 5,
        'intro': [
            'Some days, food just does not sound good. Maybe your appetite is smaller than it used to be, maybe smells feel stronger, or maybe you are simply tired. On those days, the goal is not a perfect meal. It is getting something useful in, in a form that feels manageable.',
            'This guide collects the foods and habits we lean on when appetite is low: cooler temperatures, milder flavors, softer textures and portions small enough to finish. It is general cooking education, not medical advice. If you are struggling to eat or drink for more than a day or two, talk to your care team.'
        ],
        'takeaways': [
            'Smaller portions, more often, can feel easier than three full meals.',
            'Cool or warm food usually smells less than hot food.',
            'Start with the protein while your appetite is at its best.',
            'Keep a few no-cook options ready so a hard day needs no cooking.'
        ],
        'sections': [
            {'h': 'Start Small, Then Stop', 'p': [
                'A full plate can feel like a wall on a low-appetite day. Serve half of what you think you can eat, finish it, and go back only if you want to. A half bowl you finish counts for more than a full one you push away.'
            ], 'list': [
                'Use smaller plates and bowls: A dessert plate or a mug makes a small portion look like a complete meal.',
                'Eat at regular times: Small meals every few hours can be easier than waiting until you feel hungry.',
                'Sip between meals: Drinking a lot with a meal can make you feel full sooner, so many people sip between meals instead.'
            ]},
            {'h': 'Cooler, Milder, Softer', 'p': [
                'Temperature and texture make a big difference. Hot food releases more aroma, which can be off-putting when your stomach feels unsettled. Cool or lukewarm food, mild seasoning and soft textures are often easier to face.'
            ], 'table': {'head': ['Instead of', 'Try'], 'rows': [
                ['A steaming bowl of soup', 'Soup served warm, sipped from a mug'],
                ['Spicy or garlicky dishes', 'The same dish with sweet paprika and less garlic'],
                ['Crunchy, dry foods', 'Soft eggs, yogurt, blended soups, flaky fish'],
                ['A big plate of pasta', 'A small bowl with more protein than pasta'],
                ['Fish cooked hot indoors', 'Salmon served at room temperature, or canned tuna']
            ]}},
            {'h': 'No-Cook Options to Keep on Hand', 'p': [
                'On the hardest days, cooking is the barrier. Keep a few of these in the fridge or pantry so there is always something ready. Protein amounts are estimates; check labels.'
            ], 'list': [
                'Plain Greek yogurt: About 17 g protein in a 3/4-cup serving. Add berries or a little honey.',
                'Cottage cheese: About 12 g protein in 1/2 cup. Good with fruit or on a cracker.',
                'Hard-boiled eggs: About 6 g protein each. Make a batch and keep them peeled.',
                'Overnight oats: Cold, soft and already portioned in small jars.',
                'Milk or soy milk: About 7 to 8 g protein per cup, easy to sip slowly.',
                'String cheese and crackers: Small, mild and easy to carry.'
            ]},
            {'h': 'Gentle Recipes From the Site', 'p': [
                'Each of these recipes has a "Make it gentler" variation, with milder seasoning or a cooler way to serve it.'
            ], 'list': [
                'Tomato Basil Soup with White Beans: Smooth, mild and easy to sip from a mug.',
                'Blueberry Vanilla Overnight Oats: Cold, soft and made the night before.',
                'Butternut Squash Soup with White Beans: Gently sweet and velvety.',
                'Lemon Chicken Orzo Soup: Brothy and light. Start with a mug of the broth.'
            ]},
            {'h': 'When to Ask for Help', 'p': [
                'Low appetite is common, but some signs mean it is time to call your doctor or care team rather than adjust your menu.'
            ], 'list': [
                'You cannot keep food or fluids down for more than a day.',
                'You feel dizzy or very weak, or notice signs of dehydration such as very dark urine.',
                'You have severe or persistent stomach pain.',
                'You have been eating very little for several days in a row.'
            ]}
        ],
        'faq': [
            ['Is it okay to eat the same few foods every day?', 'On hard days, yes. Repeating a handful of foods you can manage is a practical way to keep eating. Add variety again as your appetite returns, and talk to a dietitian if your options stay very limited.'],
            ['Should I skip meals if I am not hungry?', 'Many people find small, regular meals easier than waiting for hunger. If you are unsure what is right for you, your care team can help you set a plan.'],
            ['What if smells bother me while cooking?', 'Cook ahead on a better day, open a window, choose no-cook foods, or let food cool before eating. Cooler food usually smells less.']
        ]
    },
    {
        'id': 'protein-first',
        'title': 'Protein First: Easy Ways to Add Protein to Small Meals',
        'subtitle': 'Simple swaps and add-ins that fit more protein into a smaller plate, with estimated amounts for each.',
        'category': 'GLP-1 Kitchen',
        'readTime': 6,
        'intro': [
            'When you eat less, each bite has to do more. Starting a meal with its protein, and choosing ingredients that carry more protein per spoonful, helps make sure the part your body needs most does not get left on the plate.',
            'This guide covers the protein-first habit, a table of easy add-ins with estimated amounts, and swaps that change a familiar recipe without changing how it feels to eat. How much protein you need is personal; your doctor or a registered dietitian can help you set a target.'
        ],
        'takeaways': [
            'Eat the protein on your plate first, while your appetite is at its best.',
            'Swap cream and oil for Greek yogurt, cottage cheese or white beans.',
            'Add a protein to snacks, not just meals.',
            'Protein amounts here are estimates; labels and portions vary.'
        ],
        'sections': [
            {'h': 'Why Protein First', 'p': [
                'Fullness can arrive early when your appetite is small. If you start with toast or pasta, you may be full before you reach the eggs or chicken. Eating the protein first is a simple habit that keeps it from being left behind.',
                'It does not mean skipping everything else. Vegetables, fruit and grains still matter. It just changes the order on the plate.'
            ]},
            {'h': 'Easy Add-Ins and Their Protein', 'p': [
                'These are rough estimates based on typical USDA reference values and package labels. Brands vary, so check the label when it matters.'
            ], 'table': {'head': ['Add-in', 'Amount', 'Protein (estimate)', 'Easy ways to use it'], 'rows': [
                ['Plain nonfat Greek yogurt', '3/4 cup (170 g)', 'about 17 g', 'Oats, soups, dressings, dips'],
                ['Low-fat cottage cheese', '1/2 cup (113 g)', 'about 12 g', 'Toast spread, eggs, fruit bowls'],
                ['Large egg', '1 egg', 'about 6 g', 'Shakshuka, toast, salads'],
                ['Canned tuna, drained', '3 oz (85 g)', 'about 17 to 20 g', 'Salads, wraps, crackers'],
                ['Cooked chicken breast', '3 oz (85 g)', 'about 26 g', 'Soups, bowls, salads'],
                ['Shelled edamame', '1/2 cup (78 g)', 'about 9 g', 'Grain bowls, snacks'],
                ['Canned white beans, drained', '1/2 cup (about 125 g)', 'about 9 g', 'Blended into soups and sauces'],
                ['Milk or soy milk', '1 cup', 'about 7 to 8 g', 'Oats, smoothies, sipping']
            ]}},
            {'h': 'Swaps That Keep the Same Feel', 'p': [
                'You do not need new recipes to eat more protein. Small changes to familiar ones go a long way.'
            ], 'list': [
                'Cream in soups: Blend in a can of white beans, then stir in warmed Greek yogurt off the heat.',
                'Oily dressings: Whisk Greek yogurt with lemon, a little olive oil and water until pourable.',
                'Plain avocado toast: Mash the avocado with cottage cheese before spreading.',
                'Pasta-heavy bowls: Use less pasta and more chicken, beans or edamame.',
                'Pork sausage: Use lean turkey sausage and add egg whites to scrambles.'
            ]},
            {'h': 'Protein for Snacks, Too', 'p': [
                'Small meals leave room for snacks between them. Pairing a snack with a protein makes it count for more.'
            ], 'list': [
                'Apple slices with a spoonful of peanut butter',
                'Cottage cheese with berries',
                'A hard-boiled egg and a few crackers',
                'Greek yogurt with a little granola',
                'Edamame with a pinch of salt'
            ]},
            {'h': 'Recipes Built Around It', 'p': [
                'These recipes put the protein first. Values per serving are estimates.'
            ], 'list': [
                'One-Pan Shakshuka: Two eggs per plate with Greek yogurt, about 20 g protein.',
                'Avocado Cottage Cheese Toast: About 20 g protein on one slice.',
                'Lemon Chicken Orzo Soup: More chicken than pasta, about 27 g protein per bowl.',
                'Grilled Chicken Avocado Salad: About 30 g protein per bowl.'
            ]}
        ],
        'faq': [
            ['How much protein do I need?', 'It depends on your body, health and goals, so there is no single number that fits everyone. Your doctor or a registered dietitian can help you set a target that is right for you.'],
            ['Are protein shakes a good idea?', 'They can be a convenient option for some people, especially on hard days. Check the label for protein and sugar, and ask your care team if you are unsure whether they fit your plan.'],
            ['Why does Greek yogurt sometimes split in hot soup?', 'Its proteins tighten when they hit boiling, acidic liquid. Warm the yogurt with a ladle of soup first, stir it in off the heat and do not boil the soup afterwards.']
        ]
    },
    {
        'id': 'small-portion-meal-prep',
        'title': 'Small-Portion Meal Prep: Cook Once, Eat All Week',
        'subtitle': 'How to cook on a good day and portion food so a small, ready meal is always waiting in the fridge or freezer.',
        'category': 'GLP-1 Kitchen',
        'readTime': 6,
        'intro': [
            'Low-appetite days and low-energy days often arrive together. Meal prep in small portions means you do the cooking when you feel up to it, and on the harder days you only need to reheat a container.',
            'This guide covers what to cook, how to portion it, what freezes well, and how to store and reheat food safely. Pick one or two recipes to start; you do not need to prep the whole week at once.'
        ],
        'takeaways': [
            'Cook on a good day, portion small, and label everything.',
            'Soups, sauces and burritos freeze well; cooked eggs and dressed salads do not.',
            'Cool food quickly and refrigerate it within two hours.',
            'Reheat until steaming, and keep sauces and dressings separate.'
        ],
        'sections': [
            {'h': 'Pick Recipes That Hold Up', 'p': [
                'Some foods taste just as good on day three; others fall apart. These are good places to start.'
            ], 'list': [
                'Soups: Tomato, butternut squash and lemon chicken soups all keep for days. Leave out the pasta or yogurt if you plan to freeze them.',
                'Sauces: Make shakshuka sauce ahead and poach fresh eggs in a single portion.',
                'Breakfasts: Overnight oats in small jars keep for up to 4 days, and breakfast burritos freeze for months.',
                'Grains and proteins: Cooked quinoa, edamame and chicken keep well for grain bowls and salads.'
            ]},
            {'h': 'Portion Small From the Start', 'p': [
                'Portion food into containers right after cooking, in the size you can realistically finish. One cup is a good starting point for soups; a single small burrito or one 4 oz piece of fish is a full plate.',
                'Small containers also cool faster and reheat more evenly than one big pot.'
            ], 'list': [
                'Use 8 to 16 oz containers: Small glass jars and deli containers make portions easy to see.',
                'Label everything: Write the recipe name and date on the lid.',
                'Freeze flat: Lay bags of soup flat to freeze, then stack them like books.'
            ]},
            {'h': 'What Keeps and What Freezes', 'p': [
                'These times match the storage notes on our recipes.'
            ], 'table': {'head': ['Food', 'Fridge', 'Freezer', 'Notes'], 'rows': [
                ['Blended soups, before adding yogurt', 'Up to 4 days', 'Up to 3 months', 'Stir in warmed yogurt when reheating'],
                ['Chicken soup without pasta', 'Up to 4 days', 'Up to 3 months', 'Cook a little fresh pasta when reheating'],
                ['Shakshuka sauce', 'Up to 4 days', 'Up to 3 months', 'Poach the eggs fresh'],
                ['Breakfast burritos', 'Up to 4 days', 'Up to 3 months', 'Reheat straight from frozen'],
                ['Overnight oats', 'Up to 4 days', 'Not recommended', 'Texture suffers once thawed'],
                ['Cooked eggs, dressed salads', '1 to 3 days', 'Not recommended', 'They turn rubbery or soggy']
            ]}},
            {'h': 'Store and Reheat Safely', 'p': [
                'Food safety matters more when you cook ahead. These points follow general USDA food safety guidance.'
            ], 'list': [
                'Cool quickly: Refrigerate cooked food within 2 hours. Shallow containers cool faster.',
                'Keep it cold: Keep your fridge at 40°F (4°C) or below and your freezer at 0°F (-18°C).',
                'Use leftovers within 3 to 4 days: Freeze anything you will not eat in time.',
                'Reheat thoroughly: Heat leftovers to 165°F (74°C), until steaming hot all the way through.',
                'Thaw in the fridge: Move frozen portions to the fridge the night before.'
            ]},
            {'h': 'A Simple Two-Hour Prep Session', 'p': [
                'If you have one good afternoon, this covers most of a week of small meals.'
            ], 'list': [
                'In the oven: Roast the squash for the butternut soup.',
                'On the stove: Simmer the lemon chicken soup without the orzo.',
                'In a bowl: Stir together three jars of overnight oats.',
                'While things cook: Whisk a Greek yogurt dressing and cook a pot of quinoa.',
                'To finish: Blend the squash soup, portion everything into small containers, label, and refrigerate or freeze.'
            ]}
        ],
        'faq': [
            ['Do I need special containers?', 'No. Any airtight container works. Small glass jars and deli containers are inexpensive and make portion sizes easy to see.'],
            ['Can I refreeze thawed soup?', 'Food thawed in the fridge can generally be refrozen, but the texture may suffer. Freezing in single portions means you only thaw what you need.'],
            ['How do I keep prepped meals from getting boring?', 'Prep two or three recipes rather than one, and vary the toppings: a spoonful of yogurt, fresh herbs, a squeeze of lemon or a few toasted seeds.']
        ]
    }
]

gl_path = P('guides_legal.json')
gl = json.load(open(gl_path, encoding='utf-8'))
gl['guides'] = GUIDES

# ------------------------------------------------------------------ build.py
NEW_MAPS = '''GUIDE_IMG = {'nothing-sounds-good': 'tomato-basil-soup', 'protein-first': 'shakshuka', 'small-portion-meal-prep': 'overnight-oats'}
GUIDE_RELATED = {'nothing-sounds-good': ['tomato-basil-soup', 'overnight-oats', 'butternut-squash-soup'],
                 'protein-first': ['shakshuka', 'avocado-toast-jammy-eggs', 'chicken-avocado-salad'],
                 'small-portion-meal-prep': ['lemon-chicken-orzo-soup', 'breakfast-burritos', 'mediterranean-grain-bowl']}
GUIDE_REDIRECTS = {'pantry-staples': 'small-portion-meal-prep', 'perfect-rice': 'protein-first', 'knife-skills': ''}
'''
b, n = re.subn(r"GUIDE_IMG = \{[^\n]*\}\nGUIDE_RELATED = \{.*?\]\}\n", lambda m: NEW_MAPS, b, count=1, flags=re.S)
if n != 1:
    sys.exit('ERROR: GUIDE_IMG / GUIDE_RELATED block not found in build.py (nothing was saved).')

NEW_BUILD_GUIDES = r"""def build_guides():
    root = '../'
    hero = hero_bleed(root, 'images/lemon-chicken-orzo-soup.webp', 'GLP-1 Kitchen', 'Eating less?<br><em>Make every bite count.</em>',
        'Short, practical guides for small appetites: what to eat on harder days, how to fit protein into small meals, and how to cook once for the week. General cooking education, not medical advice.', short=True)
    focus = [BY_ID[i] for i in FOCUS_IDS if i in BY_ID][:6]
    body = f'''{hero}<section class="container section">{section_head('Start with a guide', 'Three short reads, each linked to recipes you can cook this week.')}<div class="guide-grid">{''.join(guide_card(root, g) for g in GUIDES)}</div></section>
{marketing_block(root, 'free')}
<section class="container section">{section_head('Small plates to cook next', 'Smaller portions, protein listed, gentler swaps included.', f'<a href="{root}recipes/?cat=small-plates" class="view-all">All small plates →</a>')}<div class="recipe-grid three">{''.join(card(root, r) for r in focus)}</div></section>
{marketing_block(root, 'paid')}'''
    page('guides/', 'GLP-1 Kitchen: Guides for Small Appetites | Bored of Toast', 'Practical guides for small appetites: what to eat when nothing sounds good, protein-first swaps and small-portion meal prep.', body, 'guides', root)
    for g in GUIDES:
        build_guide(g)
    for old, new in GUIDE_REDIRECTS.items():
        target = f'{new}/' if new else ''
        full = os.path.join(OUT, 'guides', old, 'index.html')
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'w').write(f'<!DOCTYPE html><meta charset="utf-8"><title>Redirecting…</title><link rel="canonical" href="{SITE_URL}guides/{target}"><meta http-equiv="refresh" content="0; url=../{target}"><a href="../{target}">Continue</a>')

"""
b, n = re.subn(r"def build_guides\(\):\n.*?\n(?=def build_guide\(g\):)", lambda m: NEW_BUILD_GUIDES, b, count=1, flags=re.S)
if n != 1:
    sys.exit('ERROR: build_guides() not found in build.py (nothing was saved).')

REQUIRED = [
    ("('guides/', 'Guides', 'guides')", "('guides/', 'GLP-1 Kitchen', 'guides')"),
    ("section_head('Kitchen basics', 'Short, practical guides that make every recipe easier.',",
     "section_head('From the GLP-1 Kitchen', 'Short guides for small appetites and harder days.',"),
    ("section_head('More kitchen basics',", "section_head('More from the GLP-1 Kitchen',"),
]
for old, new in REQUIRED:
    c = b.count(old)
    if c != 1:
        sys.exit(f'ERROR: expected 1 match in build.py, found {c} (nothing was saved):\n{old}')
    b = b.replace(old, new)

CRUMB_OLD = '<a href="{root}guides/">Guides</a></nav>'
if b.count(CRUMB_OLD) == 1:
    b = b.replace(CRUMB_OLD, '<a href="{root}guides/">GLP-1 Kitchen</a></nav>')
    print('- OK: guide breadcrumb')

# ------------------------------------------------------------------ checks.py
c = open(P('checks.py'), encoding='utf-8').read()
STUB_OLD = "REDIRECT_STUBS = {'about.html', 'recipes.html', 'recipe.html'}"
STUB_NEW = ("REDIRECT_STUBS = {'about.html', 'recipes.html', 'recipe.html', 'guides/pantry-staples/index.html', "
            "'guides/perfect-rice/index.html', 'guides/knife-skills/index.html'}")
if STUB_NEW not in c:
    if c.count(STUB_OLD) != 1:
        sys.exit('ERROR: REDIRECT_STUBS not found in checks.py (nothing was saved).')
    c = c.replace(STUB_OLD, STUB_NEW)

# ------------------------------------------------------------------ save
open(P('build.py'), 'w', encoding='utf-8').write(b)
open(P('checks.py'), 'w', encoding='utf-8').write(c)
with open(gl_path, 'w', encoding='utf-8') as f:
    json.dump(gl, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('OK: GLP-1 Kitchen hub, 3 new guides, redirects for the old guide URLs, menu and home renamed.')
