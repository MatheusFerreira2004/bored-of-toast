#!/usr/bin/env python3
""""5 Easy Dinners" becomes "Small-Plate Week" (same URL: /meal-plan/).

- Menu label, hero, page title and description.
- Five focus recipes: lemon chicken orzo soup, shakshuka, sheet pan salmon,
  chicken avocado salad, butternut squash soup.
- Extras: overnight oats and breakfast burritos (make-ahead).
- Prep list rewritten for the new recipes.
- Home call-to-action and shopping-list intro updated.
Shopping-list behavior is unchanged.

Nothing is saved unless every required change is found. Safe to re-run.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'build.py')
b = open(p, encoding='utf-8').read()

if "'Small-Plate Week', 'meal-plan'" in b:
    print('Already applied. Nothing to do.')
    sys.exit(0)

NEW_PLAN = '''PLAN = [('Monday', 'lemon-chicken-orzo-soup', 'Make the full pot on Monday. It reheats well, so a few small bowls are ready for later in the week.'),
        ('Tuesday', 'shakshuka', 'Two eggs per plate. Keep the extra sauce and poach fresh eggs in a single portion another day.'),
        ('Wednesday', 'sheet-pan-salmon', 'Six small pieces from one fillet. Leftovers are good cold the next day, flaked over greens.'),
        ('Thursday', 'chicken-avocado-salad', 'Cook the chicken and whisk the dressing ahead, then build a bowl in about five minutes.'),
        ('Friday', 'butternut-squash-soup', 'Roast the squash while you do something else, and freeze the base in 1-cup portions for harder days.')]
BONUS = [('Make-ahead breakfast', 'overnight-oats'), ('Freezer breakfast', 'breakfast-burritos')]'''

b, n = re.subn(r"PLAN = \[.*?\]\nBONUS = \[.*?\]", lambda m: NEW_PLAN, b, count=1, flags=re.S)
if n != 1:
    sys.exit('ERROR: PLAN/BONUS block not found in build.py (nothing was saved).')

NEW_PREP = '''<ul class="prep-list">
    <li>{ICON['check']}<span>Chop the onion, carrots and celery for the orzo soup ahead of time.</span></li>
    <li>{ICON['check']}<span>Make the shakshuka sauce up to 3 days ahead, then poach the eggs fresh.</span></li>
    <li>{ICON['check']}<span>Whisk the salmon's dill yogurt sauce and the salad's lemon dressing at the same time.</span></li>
    <li>{ICON['check']}<span>Peel and cube the squash, or buy it pre-cut.</span></li>
    <li>{ICON['check']}<span>Check your pantry before shopping so you only buy what you need.</span></li>
  </ul>'''
b, n = re.subn(r'<ul class="prep-list">.*?</ul>', lambda m: NEW_PREP, b, count=1, flags=re.S)
if n != 1:
    sys.exit('ERROR: prep list not found in build.py (nothing was saved).')

REQUIRED = [
    ("('meal-plan/', '5 Easy Dinners', 'meal-plan')", "('meal-plan/', 'Small-Plate Week', 'meal-plan')"),
    ("hero_bleed(root, 'images/honey-garlic-chicken-thighs.webp', '5 easy dinners', 'Less deciding.<br><em>More cooking.</em>',",
     "hero_bleed(root, 'images/lemon-chicken-orzo-soup.webp', 'Small-Plate Week', 'Five small plates.<br><em>One easy week.</em>',"),
    ("'Five ready-to-use dinner ideas from our free recipes. Cook them in any order, pick a favorite, or save all five to your shopping list.',",
     "'Five recipes in smaller portions, with protein listed and gentler swaps on every page. Cook them in any order, pick a favorite, or save all five to your shopping list.',"),
    ('Add all 5 dinners</button>', 'Add all 5 meals</button>'),
    ('<li><strong>Choose a dinner.</strong> Open its recipe for the method and adjustable portions.</li><li><strong>Save ingredients.</strong> Add one dinner below or all five above.',
     '<li><strong>Choose a meal.</strong> Open its recipe for the method and adjustable portions.</li><li><strong>Save ingredients.</strong> Add one meal below or all five above.'),
    ('Side dishes and weekend extras are separate.', 'Side dishes and the make-ahead extras are separate.'),
    ("section_head('Your five dinner ideas', 'A flexible dinner collection: choose the order that suits you.')",
     "section_head('Your five small plates', 'A flexible week of smaller portions: choose the order that suits you.')"),
    ('<small>Dinner idea</small>', '<small>Small plate</small>'),
    ('Add this dinner</button>', 'Add this meal</button>'),
    ('<h2 class="title">Optional weekend extras</h2><p class="fine">Not included in “Add all 5 dinners”. Open either recipe to add its ingredients separately.</p>',
     '<h2 class="title">Make-ahead extras</h2><p class="fine">Breakfasts you can prepare once and eat all week. Not included in “Add all 5 meals”; open either recipe to add its ingredients separately.</p>'),
    ("page('meal-plan/', '5 Easy Dinners | Bored of Toast', 'Five free dinner ideas with recipe portions, simple prep tips and ingredients you can save to your shopping list.',",
     "page('meal-plan/', 'Small-Plate Week | Bored of Toast', 'Five small, high-protein meals for one easy week, with prep tips and ingredients you can save to your shopping list.',"),
    ('<span class="tag light">5 easy dinners</span><h2>Less deciding.<br>More cooking.</h2><p>Five dinner ideas, clear recipes and ingredients you can save to your shopping list.</p>',
     '<span class="tag light">Small-Plate Week</span><h2>Five small plates.<br>One easy week.</h2><p>Five smaller, protein-first meals, with prep tips and ingredients you can save to your shopping list.</p>'),
    ('Explore the five dinners {ICON[\'arrow\']}</a>', 'See the week {ICON[\'arrow\']}</a>'),
]
for old, new in REQUIRED:
    c = b.count(old)
    if c != 1:
        sys.exit(f'ERROR: expected 1 match in build.py, found {c} (nothing was saved):\n{old[:140]}')
    b = b.replace(old, new)

# Optional: shopping-list intro (only if the exact text exists)
OPT_OLD = 'Add ingredients from any recipe or the five dinner ideas.'
if OPT_OLD in b:
    b = b.replace(OPT_OLD, 'Add ingredients from any recipe or the Small-Plate Week.')
    print('- OK: shopping-list intro')

open(p, 'w', encoding='utf-8').write(b)
print('OK: "5 Easy Dinners" is now "Small-Plate Week" (menu, hero, 5 focus recipes, extras, prep list, home CTA).')
