#!/usr/bin/env python3
"""Five new GLP-1 Kitchen guides (the hub goes from 3 to 8 guides).

- smoothies-that-fill-you, eating-out-small-appetite, high-protein-grocery-list,
  soft-foods-hard-days, freezer-basics.
- Cover photos: free Pexels photos (no AI), chosen because the Pexels description names the subject.
  Cropped to 3:2, 1400 px, WebP under 200 KB, credited on the guide page and on /photo-credits/.
- Hub copy updated ("Eight short reads"). Home shows the first 3 guides; each guide page shows 3 related guides.
- Guides are general cooking education, not medical advice. Protein values are estimates.

Nothing is saved unless every photo downloads, every related recipe exists and every anchor is found.
Safe to re-run.
"""
import io, json, os, re, subprocess, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from batchlib import fetch_photo, cover  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

gl_path = P('guides_legal.json')
gl = json.load(open(gl_path, encoding='utf-8'))
if any(g['id'] == 'smoothies-that-fill-you' for g in gl['guides']):
    print('Already applied. Nothing to do.')
    sys.exit(0)

PHOTOS = {
    'guide-smoothies': {
        'id': 775032, 'guide': 'smoothies-that-fill-you',
        'photographer': 'Element5 Digital', 'photographer_url': 'https://www.pexels.com/@element5/',
        'photo_url': 'https://www.pexels.com/photo/strawberry-smoothie-on-glass-jar-775032/',
        'alt': 'A fruit smoothie with berries and banana in a glass jar.'},
    'guide-eating-out': {
        'id': 14009280, 'guide': 'eating-out-small-appetite',
        'photographer': 'Bas Linders', 'photographer_url': 'https://www.pexels.com/@studio1345/',
        'photo_url': 'https://www.pexels.com/photo/food-on-table-14009280/',
        'alt': 'Several small tapas plates served on a rustic wooden restaurant table.'},
    'guide-grocery': {
        'id': 28216090, 'guide': 'high-protein-grocery-list',
        'photographer': 'Selma Nigar Baştürk', 'photographer_url': 'https://www.pexels.com/@selma-nigar-basturk-1546567251/',
        'photo_url': 'https://www.pexels.com/photo/a-table-with-various-vegetables-and-eggs-28216090/',
        'alt': 'Fresh groceries, including eggs, pears and greens, laid out on a white table.'},
    'guide-soft': {
        'id': 5440960, 'guide': 'soft-foods-hard-days',
        'photographer': 'Rachel Loughman', 'photographer_url': 'https://www.pexels.com/@rachel-loughman-3513722/',
        'photo_url': 'https://www.pexels.com/photo/mashed-potato-in-a-clear-glass-mini-bowl-5440960/',
        'alt': 'A small glass bowl of smooth mashed potatoes.'},
    'guide-freezer': {
        'id': 30635719, 'guide': 'freezer-basics',
        'photographer': 'Iara Melo', 'photographer_url': 'https://www.pexels.com/@iara-melo-558346607/',
        'photo_url': 'https://www.pexels.com/photo/stack-of-healthy-meal-prep-containers-30635719/',
        'alt': 'A stack of meal prep containers filled with rice and vegetables.'},
}

RELATED = {
    'smoothies-that-fill-you': ['strawberry-protein-smoothie', 'banana-protein-smoothie', 'mixed-berry-protein-smoothie'],
    'eating-out-small-appetite': ['egg-salad-lettuce-wraps', 'lemon-herb-baked-cod', 'chicken-avocado-salad'],
    'high-protein-grocery-list': ['greek-yogurt-berry-parfaits', 'cottage-cheese-scrambled-eggs', 'tuna-white-bean-salad'],
    'soft-foods-hard-days': ['chicken-rice-congee', 'cottage-cheese-mashed-potatoes', 'greek-yogurt-chia-pudding'],
    'freezer-basics': ['split-pea-soup', 'turkey-meatballs-tomato-sauce', 'breakfast-burritos'],
}

NEW_GUIDES = [
    {
        'id': 'smoothies-that-fill-you',
        'title': 'Smoothies That Actually Fill You',
        'subtitle': 'How to build a small, sippable smoothie with real protein in it, and how to keep it from tasting like a chalky shake.',
        'category': 'GLP-1 Kitchen',
        'readTime': 5,
        'intro': [
            'On days when chewing feels like work, a smoothie can be the easiest way to get something useful in. The catch is that many smoothies are mostly fruit and juice: sweet, big and not very filling.',
            'This guide shows a simple formula for a smaller smoothie built around protein, with add-ins and their estimated protein, plus a few fixes for texture and taste. It is general cooking education, not medical or nutrition advice.'
        ],
        'takeaways': [
            'Start with a protein base: Greek yogurt, milk, soy milk or cottage cheese.',
            'Use frozen fruit instead of ice so the smoothie stays thick, not watery.',
            'A 1-cup smoothie you finish counts for more than a big one you abandon.',
            'Sip slowly; you can keep half in the fridge for later.'
        ],
        'sections': [
            {'h': 'The Simple Formula', 'p': [
                'Think of a smoothie as three parts: a protein base, a little fruit for flavor, and a liquid to get the blender moving. Everything else is optional.'
            ], 'list': [
                'Protein base: 1/2 to 3/4 cup plain Greek yogurt or 1/2 cup cottage cheese.',
                'Fruit: 1/2 to 3/4 cup frozen berries, banana or mango.',
                'Liquid: 1/2 cup milk, soy milk or ultra-filtered milk, plus more to thin.',
                'Optional extras: A spoonful of peanut butter, oats, chia seeds or a little honey.'
            ]},
            {'h': 'Add-Ins and Their Protein', 'p': [
                'These are rough estimates based on typical USDA reference values and package labels. Brands vary a lot, especially protein powders and ultra-filtered milks, so check the label.'
            ], 'table': {'head': ['Add-in', 'Amount', 'Protein (estimate)'], 'rows': [
                ['Plain nonfat Greek yogurt', '3/4 cup', 'about 17 g'],
                ['Low-fat cottage cheese', '1/2 cup', 'about 12 g'],
                ['Ultra-filtered milk', '1 cup', 'about 13 g (check label)'],
                ['Milk or soy milk', '1 cup', 'about 7 to 8 g'],
                ['Peanut butter', '1 tablespoon', 'about 4 g'],
                ['Chia seeds', '1 tablespoon', 'about 2 g'],
                ['Protein powder', '1 scoop', 'varies, often 15 to 25 g']
            ]}},
            {'h': 'Fixes for Texture and Taste', 'p': [
                'A smoothie that tastes chalky or separates in the glass is hard to finish. A few small changes help.'
            ], 'list': [
                'Too thin: Add more frozen fruit or a spoonful of yogurt, not ice.',
                'Too thick: Add milk a tablespoon at a time.',
                'Chalky from powder: Use less powder and more Greek yogurt, or blend the powder with the liquid first.',
                'Cottage cheese texture: Blend it alone with the milk until completely smooth before adding fruit.',
                'Too sweet: Skip juice and honey; let ripe banana or berries do the work.'
            ]},
            {'h': 'Smaller Is Fine', 'p': [
                'You do not need a giant glass. Pour a 1-cup serving, refrigerate the rest in a sealed jar, and shake it before drinking later the same day. Smoothies with yogurt are best within 24 hours.'
            ]},
            {'h': 'Smoothies From the Site', 'p': [
                'Each of these uses Greek yogurt as the protein base. Values per serving are estimates.'
            ], 'list': [
                'Strawberry Greek Yogurt Smoothie: About 16 g protein per glass.',
                'Banana Vanilla Protein Smoothie: About 16 g protein per glass.',
                'Mixed Berry Protein Smoothie: About 16 g protein per glass.'
            ]}
        ],
        'faq': [
            ['Do I need protein powder?', 'No. Greek yogurt, cottage cheese and milk can carry a smoothie on their own. Powder is optional; if you use it, check the label for protein and added sugar.'],
            ['Can I make smoothies ahead?', 'Yes, for the same day. Keep them sealed in the fridge and shake well. You can also freeze the fruit and yogurt portions in bags and blend with milk when you want one.'],
            ['Are smoothies a replacement for meals?', 'They can be a practical option on harder days. If you rely on them often, ask your care team or a registered dietitian whether your overall intake meets your needs.']
        ]
    },
    {
        'id': 'eating-out-small-appetite',
        'title': 'Eating Out with a Small Appetite',
        'subtitle': 'How to order, share and pack up at restaurants when a full entree is more than you can eat.',
        'category': 'GLP-1 Kitchen',
        'readTime': 5,
        'intro': [
            'Restaurant portions are often built for big appetites. When yours is smaller, a night out can feel like a choice between leaving most of your plate or eating past comfortable.',
            'There is a middle path. This guide covers how to read a menu for protein, how to order smaller without making a fuss, and how to turn leftovers into tomorrow\'s small plate.'
        ],
        'takeaways': [
            'Look for the protein on the menu first, then build around it.',
            'Appetizers, half portions and sides can make a perfect small meal.',
            'Ask for a to-go box when the food arrives, not at the end.',
            'Go easy on bread baskets and drinks before the meal arrives.'
        ],
        'sections': [
            {'h': 'Read the Menu for Protein', 'p': [
                'Scan for the dish where protein is the main event: grilled fish, chicken, eggs, beans, tofu or lean meat. Dishes built mostly on pasta, fries or bread can fill you up before you get much protein.'
            ], 'list': [
                'Good bets: Grilled fish or chicken, shrimp skewers, egg dishes, chili, lentil or bean soups, poke or rice bowls with extra protein.',
                'Ask for swaps: Extra vegetables or a side salad instead of fries is a common, easy request.',
                'Sauces on the side: Rich sauces add fullness quickly; on the side, you control how much you use.'
            ]},
            {'h': 'Order Smaller Without the Fuss', 'p': [
                'Most restaurants are happy to help, and you do not need to explain why.'
            ], 'list': [
                'Order an appetizer as your meal: Shrimp cocktail, chicken skewers or a cup of soup is often the right size.',
                'Ask about half or lunch portions: Many places offer them even at dinner if you ask.',
                'Share an entree: Split one main and add a side or soup each.',
                'Build from sides: A protein side plus a vegetable side makes a balanced small plate.'
            ]},
            {'h': 'At the Table', 'p': [
                'A few habits make it easier to eat comfortably and enjoy the company.'
            ], 'list': [
                'Box it early: Ask for a to-go container when the food arrives and set aside half right away.',
                'Protein first: Start with the protein on your plate while your appetite is at its best.',
                'Pace yourself: Put your fork down between bites and stop when you are comfortably satisfied.',
                'Sip between bites: Many people find that a lot of liquid with a meal makes them full sooner.'
            ]},
            {'h': 'What to Order by Cuisine', 'table': {'head': ['Cuisine', 'Smaller, protein-forward ideas'], 'rows': [
                ['American diner', 'Two eggs with fruit, a cup of chili, grilled chicken with a side salad'],
                ['Mexican', 'Chicken or shrimp tacos (order two), fajita protein with beans, chicken tortilla soup'],
                ['Italian', 'Minestrone, grilled fish, a half portion of pasta with chicken'],
                ['Japanese', 'Miso soup, edamame, sashimi or a small poke bowl'],
                ['Mediterranean', 'Chicken or falafel plate with hummus, lentil soup, Greek salad with chicken'],
                ['Chinese', 'Egg drop or hot and sour soup, steamed chicken and vegetables, sharing a few dishes']
            ]}},
            {'h': 'Leftovers Are a Bonus', 'p': [
                'Refrigerate leftovers within 2 hours (1 hour if it is very hot out) and eat them within 3 to 4 days. Reheat until steaming. Half a restaurant entree is often a ready-made small plate for the next day.'
            ]}
        ],
        'faq': [
            ['Is it rude to ask for a smaller portion?', 'No. Asking for a half portion, an appetizer as a main or a to-go box is a normal request at most restaurants.'],
            ['What about drinks?', 'Many people find carbonated drinks and large amounts of liquid make them feel full faster. If you drink alcohol, ask your care team whether it fits your situation.'],
            ['What if nothing on the menu works?', 'A cup of soup and a side of vegetables, or a couple of appetizers, can make a fine meal. You can also eat a small protein snack before you go so you are not choosing on an empty stomach.']
        ]
    },
    {
        'id': 'high-protein-grocery-list',
        'title': 'High-Protein Grocery List for Small Appetites',
        'subtitle': 'A practical shopping list of protein-rich foods that keep well, need little cooking and fit into small meals.',
        'category': 'GLP-1 Kitchen',
        'readTime': 6,
        'intro': [
            'When your appetite is small, the easiest meals are the ones that are already in the kitchen. A well-stocked fridge and pantry means you can put together a protein-forward plate in minutes, even on a low-energy day.',
            'This list is organized by where things live in a typical U.S. grocery store, with estimated protein amounts and ideas for using each item. Protein values are estimates based on USDA reference values and common labels.'
        ],
        'takeaways': [
            'Keep a few no-cook proteins on hand: Greek yogurt, cottage cheese, eggs, canned fish.',
            'Canned and frozen proteins are just as useful as fresh, and they last longer.',
            'Buy smaller packages if you often throw food away.',
            'Check labels: protein per serving varies by brand.'
        ],
        'sections': [
            {'h': 'Dairy Case', 'table': {'head': ['Item', 'Typical serving', 'Protein (estimate)', 'Use it for'], 'rows': [
                ['Plain nonfat Greek yogurt', '3/4 cup', 'about 17 g', 'Parfaits, smoothies, dressings, soups'],
                ['Low-fat cottage cheese', '1/2 cup', 'about 12 g', 'Toast, eggs, fruit bowls, mashed potatoes'],
                ['Eggs', '1 large', 'about 6 g', 'Scrambles, frittatas, egg salad'],
                ['Ultra-filtered milk', '1 cup', 'about 13 g (check label)', 'Lattes, oats, smoothies'],
                ['String cheese', '1 stick', 'about 6 to 7 g', 'Snacks'],
                ['Part-skim ricotta', '1/4 cup', 'about 7 g', 'Toast, pasta, pancakes']
            ]}},
            {'h': 'Meat and Seafood Counter', 'list': [
                'Rotisserie chicken: Pull it the day you buy it and portion into small containers. About 25 g protein per 3 oz.',
                'Lean ground turkey: For meatballs, taco bowls and stuffed peppers. About 22 g per cooked 3 oz.',
                'White fish fillets: Cod or tilapia bake in under 15 minutes. About 19 to 20 g per 3 oz.',
                'Salmon: About 22 g per cooked 3 oz; leftovers are good cold.',
                'Shrimp (frozen, peeled): Cooks in minutes. About 20 g per 3 oz.'
            ]},
            {'h': 'Pantry', 'list': [
                'Canned tuna or salmon: About 17 to 20 g per drained 3 oz. Salads, wraps, crackers.',
                'Canned beans and chickpeas: About 6 to 8 g per 1/2 cup. Soups, chili, blended into sauces.',
                'Red lentils: Cook in about 20 minutes and blend into smooth soups.',
                'Peanut butter: About 7 g per 2 tablespoons. Smoothies, toast, apple slices.',
                'Bone broth: Some brands have 8 to 10 g per cup. Check the label.',
                'Oats and chia seeds: Small protein boosts for breakfasts.'
            ]},
            {'h': 'Freezer Aisle', 'list': [
                'Shelled edamame: About 9 g per 1/2 cup. Snacks and grain bowls.',
                'Frozen berries: For smoothies, parfaits and chia pudding.',
                'Frozen fish fillets and shrimp: Thaw overnight in the fridge.',
                'Frozen vegetables: Add to soups and stir-fries without any chopping.'
            ]},
            {'h': 'A Simple Weekly Starter List', 'p': [
                'If you are starting from an empty fridge, this covers several small meals and snacks for one person.'
            ], 'list': [
                '1 large tub plain Greek yogurt',
                '1 tub cottage cheese',
                '1 dozen eggs',
                '1 rotisserie chicken',
                '2 cans tuna or salmon',
                '2 cans beans or chickpeas',
                '1 bag frozen berries',
                '1 bag frozen edamame',
                'Bread, crackers or tortillas you like'
            ]}
        ],
        'faq': [
            ['Is canned or frozen protein less healthy?', 'Not necessarily. Canned fish and beans and frozen seafood are convenient, keep well and are widely used. If you watch sodium, look for low-sodium cans or rinse beans before using.'],
            ['How do I avoid wasting food?', 'Buy smaller containers, freeze portions of cooked chicken or soup right away, and plan two or three recipes that share ingredients.'],
            ['How much protein should I buy for?', 'That depends on your needs. Your doctor or a registered dietitian can help you set a daily target; this list is about having easy options on hand.']
        ]
    },
    {
        'id': 'soft-foods-hard-days',
        'title': 'Soft Foods for Hard Days',
        'subtitle': 'Smooth, mild, easy-to-eat foods with some protein in them, for days when chewing and strong flavors feel like too much.',
        'category': 'GLP-1 Kitchen',
        'readTime': 5,
        'intro': [
            'Some days call for food that asks very little of you: no hard crusts, no strong smells, nothing that takes a lot of chewing. Soft foods can still carry protein if you choose and build them well.',
            'This guide lists soft, mild options, ways to add protein without changing the texture, and recipes from the site that fit. It is general cooking education. If you have trouble swallowing or a medical texture plan, follow your care team\'s guidance.'
        ],
        'takeaways': [
            'Soft does not have to mean low protein: eggs, yogurt, cottage cheese and blended beans are all soft.',
            'Warm or cool food is often easier than hot food.',
            'Blending, mashing and slow cooking turn many foods soft.',
            'Keep portions small and eat slowly.'
        ],
        'sections': [
            {'h': 'Soft, Mild and Protein-Friendly', 'table': {'head': ['Food', 'Why it works', 'Protein (estimate)'], 'rows': [
                ['Scrambled eggs, cooked soft', 'Tender and mild', 'about 12 g for 2 eggs'],
                ['Greek yogurt', 'Cool, smooth, no chewing', 'about 17 g per 3/4 cup'],
                ['Cottage cheese, blended', 'Smooth when blitzed', 'about 12 g per 1/2 cup'],
                ['Congee or rice porridge with chicken', 'Very soft, warm, gentle', 'varies by recipe'],
                ['Blended lentil or bean soup', 'Smooth and filling', 'about 7 to 15 g per cup'],
                ['Flaky baked white fish', 'Breaks apart with a fork', 'about 19 g per 3 oz'],
                ['Chia or rice pudding made with milk and yogurt', 'Spoonable and cool', 'varies by recipe']
            ]}},
            {'h': 'Add Protein Without Changing the Texture', 'list': [
                'Stir warmed Greek yogurt into soups off the heat.',
                'Blend cottage cheese into mashed potatoes or scrambled eggs.',
                'Use milk or ultra-filtered milk instead of water in oatmeal and porridge.',
                'Blend white beans into creamy soups.',
                'Beat an egg into hot broth for an egg drop soup.'
            ]},
            {'h': 'Make Almost Anything Softer', 'list': [
                'Cook longer: Simmer grains and vegetables until very tender.',
                'Blend or mash: Use a blender, immersion blender or potato masher.',
                'Add moisture: A spoonful of broth, milk or sauce makes food easier to swallow.',
                'Cut small: Dice or shred meat and fish finely.',
                'Skip the crust: Remove tough skins and crusts.'
            ]},
            {'h': 'Soft Recipes From the Site', 'list': [
                'Chicken Rice Congee: Warm, soft rice porridge with shredded chicken.',
                'Cottage Cheese Mashed Potatoes: Smooth mash with extra protein.',
                'Greek Yogurt Chia Pudding: Cool and spoonable, made ahead.',
                'Protein Rice Pudding: Soft and gently sweet.',
                'Ginger Egg Drop Soup: Light broth with soft ribbons of egg.'
            ]}
        ],
        'faq': [
            ['Is it fine to eat only soft foods for a few days?', 'On hard days, many people do. If soft foods are all you can manage for more than a few days, or you have pain or trouble swallowing, talk to your doctor or care team.'],
            ['How do I keep soft food from being boring?', 'Change the toppings and temperature: a swirl of yogurt, fresh herbs, a squeeze of lemon, cinnamon on sweet dishes. Rotate between warm and cool options.'],
            ['Can I freeze soft foods?', 'Many soups, congee and mashed potatoes freeze well in small portions. Yogurt-based dishes are better made fresh.']
        ]
    },
    {
        'id': 'freezer-basics',
        'title': 'Freezer Basics: What Keeps and for How Long',
        'subtitle': 'How to freeze, label, thaw and reheat small portions safely, with a simple chart of what freezes well.',
        'category': 'GLP-1 Kitchen',
        'readTime': 5,
        'intro': [
            'A freezer full of small portions is one of the best tools for low-appetite and low-energy days. Cook once on a good day, and there is always a ready meal waiting.',
            'This guide covers how to freeze food so it keeps its quality, a chart of what freezes well, and how to thaw and reheat safely. The safety points follow general USDA food safety guidance.'
        ],
        'takeaways': [
            'Keep your freezer at 0°F (-18°C).',
            'Food kept frozen at 0°F stays safe, but quality is best within a few months.',
            'Freeze in small, labeled, flat portions.',
            'Thaw in the fridge and reheat to 165°F (74°C).'
        ],
        'sections': [
            {'h': 'How to Freeze Well', 'list': [
                'Cool first: Let food cool, then refrigerate within 2 hours before freezing.',
                'Portion small: 1-cup containers or bags match a small plate.',
                'Leave room: Liquids expand; leave about 1/2 inch at the top.',
                'Remove air: Press air out of bags to limit freezer burn.',
                'Freeze flat: Lay bags flat on a tray, then stack once frozen.',
                'Label everything: Name and date on every container.'
            ]},
            {'h': 'What Freezes Well', 'p': [
                'Times below are for best quality, not safety. Food kept frozen at 0°F remains safe longer, but texture and flavor slowly fade.'
            ], 'table': {'head': ['Food', 'Best quality within', 'Notes'], 'rows': [
                ['Soups, stews and chili', '2 to 3 months', 'Freeze without pasta or yogurt; add those when reheating'],
                ['Cooked meatballs in sauce', '2 to 3 months', 'Freeze in single portions'],
                ['Cooked chicken, shredded', '2 to 4 months', 'Add a splash of broth to keep it moist'],
                ['Breakfast burritos', 'Up to 3 months', 'Wrap individually'],
                ['Muffins and pancakes', '1 to 2 months', 'Freeze in a single layer first'],
                ['Cooked rice and grains', '1 to 2 months', 'Freeze flat in small bags'],
                ['Raw fish fillets', '3 to 6 months', 'Thaw overnight in the fridge']
            ]}},
            {'h': 'What Does Not Freeze Well', 'list': [
                'Yogurt-based sauces and dressings: They separate.',
                'Hard-boiled eggs: The whites turn rubbery.',
                'Salad greens and cucumber: They go limp and watery.',
                'Fried foods: They lose their crunch.',
                'Dishes with cream or soft cheese: They may turn grainy.'
            ]},
            {'h': 'Thaw and Reheat Safely', 'list': [
                'In the fridge: The safest method. Move portions the night before.',
                'In cold water: Seal in a bag and change the water every 30 minutes; cook right away.',
                'In the microwave: Use the defrost setting and cook immediately.',
                'Never on the counter: Food can warm into the unsafe range.',
                'Reheat to 165°F (74°C): Until steaming hot all the way through. Stir soups halfway.'
            ]},
            {'h': 'Freezer-Friendly Recipes From the Site', 'list': [
                'Creamy Split Pea Soup',
                'Turkey Meatballs in Tomato Sauce',
                'Freezer-Friendly Breakfast Burritos',
                'Chicken Minestrone (freeze without the pasta)',
                'Turkish-Style Red Lentil Soup'
            ]}
        ],
        'faq': [
            ['Can I refreeze thawed food?', 'Food thawed in the fridge can generally be refrozen, though quality may drop. Food thawed in cold water or the microwave should be cooked before refreezing.'],
            ['Is freezer burn unsafe?', 'No. Freezer burn affects texture and flavor, not safety. Trim off dry spots or use the food in soups.'],
            ['Do I need special containers?', 'No. Freezer bags and airtight containers both work. Small sizes make portioning easier.']
        ]
    },
]

# ------------------------------------------------------------------ validate related recipes
recipes = json.load(open(P('recipes.json'), encoding='utf-8'))
ids = {r['id'] for r in recipes}
missing = [rid for lst in RELATED.values() for rid in lst if rid not in ids]
if missing:
    print(f'ERROR: related recipes not found in recipes.json: {missing}. Nothing was saved.')
    sys.exit(1)

# ------------------------------------------------------------------ build.py edits (in memory)
b = open(P('build.py'), encoding='utf-8').read()
m = re.search(r"^GUIDE_REDIRECTS = [^\n]*\n", b, re.M)
if not m:
    print('ERROR: GUIDE_REDIRECTS line not found in build.py. Nothing was saved.')
    sys.exit(1)
extra = ('GUIDE_IMG.update(' + json.dumps({ph['guide']: name for name, ph in PHOTOS.items()}) + ')\n'
         'GUIDE_RELATED.update(' + json.dumps(RELATED) + ')\n')
b = b[:m.end()] + extra + b[m.end():]

OLD_HUB = "section_head('Start with a guide', 'Three short reads, each linked to recipes you can cook this week.')"
NEW_HUB = "section_head('Start with a guide', 'Eight short reads, each linked to recipes you can cook this week.')"
if b.count(OLD_HUB) != 1:
    print('ERROR: hub section title not found in build.py. Nothing was saved.')
    sys.exit(1)
b = b.replace(OLD_HUB, NEW_HUB)

OLD_DESC = "'Practical guides for small appetites: what to eat when nothing sounds good, protein-first swaps and small-portion meal prep.'"
NEW_DESC = "'Practical guides for small appetites: gentle foods, protein-first swaps, smoothies, eating out, grocery lists, meal prep and freezer basics.'"
if b.count(OLD_DESC) == 1:
    b = b.replace(OLD_DESC, NEW_DESC)
    print('- hub meta description updated')

# Home: show only the first 3 guides
home_re = re.compile(r"(section_head\('From the GLP-1 Kitchen'[^\n]*\n\s*<div class=\"guide-grid\">\{''\.join\(guide_card\(root, g\) for g in )GUIDES\)")
b, n = home_re.subn(lambda mm: mm.group(1) + 'GUIDES[:3])', b, count=1)
print('- home shows 3 guides' if n else '- note: home guide grid not changed (pattern not found)')

# Guide pages: show 3 related guides
OLD_REL = "''.join(guide_card(root, x) for x in GUIDES if x['id'] != g['id'])"
NEW_REL = "''.join(guide_card(root, x) for x in [y for y in GUIDES if y['id'] != g['id']][:3])"
if b.count(OLD_REL) == 1:
    b = b.replace(OLD_REL, NEW_REL)
    print('- guide pages show 3 related guides')

# ------------------------------------------------------------------ photos (in memory)
out = {}
for name, ph in PHOTOS.items():
    try:
        im = fetch_photo(ph)
    except Exception as ex:
        print(f'ERROR: could not download {name} ({ex}). Nothing was saved.')
        sys.exit(1)
    im = cover(im, 1400, 933)
    blob = None
    for q in (78, 72, 66, 60, 54, 48):
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=q, method=6)
        if buf.tell() <= 195 * 1024:
            blob = buf.getvalue()
            break
    if not blob:
        print(f'ERROR: {name} is still over 200 KB. Nothing was saved.')
        sys.exit(1)
    out[name] = blob
    print(f'- photo {name}: {len(blob) // 1024} KB')

# ------------------------------------------------------------------ save
for name, blob in out.items():
    open(os.path.join(IMG, f'{name}.webp'), 'wb').write(blob)
subprocess.check_call([sys.executable, P('make_images.py')])

craw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(craw)
for name, ph in PHOTOS.items():
    credits[name] = {'photographer': ph['photographer'], 'photographer_url': ph['photographer_url'],
                     'photo_url': ph['photo_url'], 'source': 'Pexels', 'alt': ph['alt']}
cm = re.match(r'\{\s*\n([ \t]+)"', craw)
with open(P('credits.json'), 'w', encoding='utf-8') as f:
    json.dump(credits, f, ensure_ascii=False, indent=len(cm.group(1)) if cm else 1)
    f.write('\n')

open(P('build.py'), 'w', encoding='utf-8').write(b)

gl['guides'].extend(NEW_GUIDES)
with open(gl_path, 'w', encoding='utf-8') as f:
    json.dump(gl, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(f"OK: 5 new guides added. The GLP-1 Kitchen now has {len(gl['guides'])} guides.")
