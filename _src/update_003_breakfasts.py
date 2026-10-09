#!/usr/bin/env python3
"""Recipes 2/4: breakfast rewrites (shakshuka, avocado toast, overnight oats).

Same ids, URLs and photos. Smaller portions, more protein, neutral kitchen notes (no "tested" claims).
Steps are merged into the existing step objects, so step photos stay attached.

Nutrition per serving is an ESTIMATE: previous per-recipe estimate x old servings, minus removed
ingredients, plus added ones, divided by new servings. Reference values (USDA FoodData Central,
rounded; double-check before relying on them):
  large egg (50 g): 72 kcal, 6.3 g protein, 0.4 g carbs, 4.8 g fat
  olive oil, 1 tbsp (13.5 g): 119 kcal, 13.5 g fat
  plain nonfat Greek yogurt, per 100 g: 59 kcal, 10.2 g protein, 3.6 g carbs, 0.4 g fat
  low-fat (2%) cottage cheese, per 100 g: 84 kcal, 11 g protein, 4.3 g carbs, 2.3 g fat
  avocado flesh, per 100 g: 160 kcal, 2 g protein, 8.5 g carbs, 14.7 g fat, 6.7 g fiber
  maple syrup, 1 tbsp (20 g): 52 kcal, 13.4 g carbs

Shakshuka (was 4 x 290 kcal / 14 P / 17 C / 17 F / 4 fiber):
  +2 eggs, -1 tbsp olive oil, +120 g Greek yogurt -> 1256 kcal, 80.8 P, 73.1 C, 64.5 F, 16 fiber
  / 4 servings = ~314 kcal, 20 g protein, 18 g carbs, 16 g fat, 4 g fiber
Avocado toast (was 2 x 490 / 15 / 42 / 30 / 8; large avocado assumed ~200 g flesh):
  +113 g cottage cheese, -2 tsp olive oil (80 kcal, 9 g fat), -100 g avocado
  -> 835 kcal, 40.4 P, 80.4 C, 38.9 F, 9.3 fiber / 2 = ~418 kcal, 20 g protein, 40 g carbs, 19 g fat, 5 g fiber
Overnight oats (was 2 x 390 / 17 / 62 / 8 / 8):
  +120 g Greek yogurt, -1/2 tbsp maple syrup -> 825 kcal, 46.2 P, 121.6 C, 16.5 F, 16 fiber
  / 3 servings = ~275 kcal, 15 g protein, 41 g carbs, 6 g fat, 5 g fiber

Run automatically by Auto build. Safe to re-run.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)
SMALL_TIP = 'Small-portion tip: serve half a portion and save the rest for later. A half bowl still counts.'

raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(raw)
BY = {r['id']: r for r in recipes}


def merge_steps(old, new):
    out = []
    for i, s in enumerate(new):
        base = dict(old[i]) if i < len(old) else {}
        base.pop('tip', None)
        base.update(s)
        out.append(base)
    return out


def set_tag(r, tag, on=True):
    tags = r.setdefault('tags', [])
    if on and tag not in tags:
        tags.append(tag)
    if not on and tag in tags:
        tags.remove(tag)


NEW = {}

# ------------------------------------------------------------------ Shakshuka
NEW['shakshuka'] = {
    'subtitle': 'Eggs gently poached in a smoky tomato and pepper sauce, finished with feta and a spoonful of Greek yogurt. Two eggs per small plate, about 20 g protein.',
    'desc': 'Two eggs, smoky tomato sauce, a spoon of yogurt.',
    'serves': 4,
    'intro': [
        'Shakshuka is a dish loved across North Africa and the Middle East: eggs cooked right in a pan of spiced tomato and pepper sauce. It is soft, warm and easy to portion, which makes it a good fit for small appetites. This version uses eight eggs instead of six, so each plate gets two, and finishes with a spoonful of Greek yogurt for extra protein and a cool, mild contrast.',
        'Most of the flavor comes from blooming the spices. Cumin and smoked paprika hold much of their aroma in fat-soluble compounds, so a minute in hot oil releases far more flavor than stirring them into the tomatoes. That means you can use less oil than usual and still get a deep, rounded sauce. Covering the pan at the end traps steam, which sets the tops of the eggs while the yolks stay soft.'
    ],
    'why': [
        ['About 20 g protein per plate', 'Two eggs, feta and Greek yogurt in one small serving.'],
        ['One pan, few dishes', 'Sauce and eggs cook in the same skillet, which goes right to the table.'],
        ['Sauce freezes well', 'Make a double batch of sauce and poach fresh eggs in a small portion whenever you need it.']
    ],
    'ingredients': [
        {'group': 'For the sauce', 'items': [
            {'q': 1, 'u': 'tbsp', 'n': 'extra-virgin olive oil'},
            {'q': 1, 'u': '', 'n': 'medium yellow onion', 'note': 'diced'},
            {'q': 1, 'u': '', 'n': 'red bell pepper', 'note': 'seeded and diced'},
            {'q': 3, 'u': 'cloves', 'n': 'garlic', 'note': 'minced'},
            {'q': 1, 'u': 'tsp', 'n': 'ground cumin'},
            {'q': 1, 'u': 'tsp', 'n': 'smoked paprika'},
            {'q': 0.25, 'u': 'tsp', 'n': 'red pepper flakes', 'note': 'optional'},
            {'q': 1, 'u': 'can', 'n': 'crushed tomatoes', 'note': '28 oz (794 g)'},
            {'q': 1, 'u': 'tsp', 'n': 'granulated sugar', 'note': 'optional, to balance acidity'},
            {'q': 0.75, 'u': 'tsp', 'n': 'kosher salt', 'note': 'plus more to taste'},
            {'q': None, 'u': '', 'n': 'black pepper', 'note': 'to taste'}
        ]},
        {'group': 'For the eggs and topping', 'items': [
            {'q': 8, 'u': '', 'n': 'large eggs'},
            {'q': 0.33, 'u': 'cup', 'n': 'crumbled feta cheese', 'g': 50},
            {'q': 0.5, 'u': 'cup', 'n': 'plain nonfat Greek yogurt', 'g': 120},
            {'q': 2, 'u': 'tbsp', 'n': 'fresh cilantro or parsley', 'note': 'chopped'},
            {'q': None, 'u': '', 'n': 'bread or pita', 'note': 'optional, to serve; use gluten-free bread if needed'}
        ]}
    ],
    'steps': [
        {'t': 'Soften the onion and pepper',
         'd': 'Heat the olive oil in a 12-inch skillet over medium heat until it shimmers. Add the onion and bell pepper with a pinch of salt and cook, stirring occasionally, for 7 to 8 minutes, until soft and the onion is translucent. The salt draws out moisture so the vegetables soften instead of scorching, which matters when you are using less oil.'},
        {'t': 'Bloom the spices',
         'd': 'Add the garlic, cumin, smoked paprika and red pepper flakes if using, and stir constantly for about 1 minute, until the oil turns rusty red and smells toasty. Keep everything moving so the garlic softens without browning.',
         'tip': 'If the spices start to smell sharp or look dark, add the tomatoes right away. They cool the pan instantly and stop any scorching.'},
        {'t': 'Simmer the sauce',
         'd': 'Stir in the crushed tomatoes, sugar if using, salt and a few grinds of black pepper. Bring to a gentle simmer and cook for 8 to 10 minutes, stirring now and then, until a spoon dragged through the sauce leaves a trail for a second or two. Taste and adjust the salt.'},
        {'t': 'Nestle in the eggs',
         'd': 'Use the back of a spoon to press 8 small wells into the sauce, in pairs if you can, so each serving is easy to lift out. Crack an egg into each well and season lightly with salt and pepper. A thick sauce holds the eggs in place, while a thin one lets the whites run.',
         'tip': 'Crack each egg into a small cup first, then slide it into its well. The yolks stay whole and any stray shell is easy to fish out.'},
        {'t': 'Cover and cook gently',
         'd': 'Reduce the heat to medium-low, cover the pan and cook for 6 to 9 minutes, until the whites are opaque and set but the yolks still jiggle when you gently shake the pan. With eight eggs the pan is fuller, so start checking at 6 minutes. If you prefer firmer yolks, cook 2 to 3 minutes longer.'},
        {'t': 'Finish and serve small',
         'd': 'Take the skillet off the heat and scatter the feta and herbs over the top. Lift two eggs with some sauce onto each plate and add a spoonful of Greek yogurt. Bread or pita is optional; a small piece is enough for scooping.'}
    ],
    'tips': [
        'If the whites set slowly while the yolks race ahead, spoon a little hot sauce over the whites before covering.',
        'Make the sauce up to 3 days ahead. Reheat only the amount you need in a small pan and poach two eggs in it for a single serving.',
        'Use a lid that fits well. Trapped steam cooks the tops of the eggs, and a loose lid means longer cooking and firmer yolks.',
        SMALL_TIP
    ],
    'storage': 'Refrigerate leftover sauce on its own in an airtight container for up to 4 days, or freeze it in 1-cup portions for up to 3 months. Cooked eggs turn rubbery when reheated, so warm a portion of sauce in a small skillet until simmering and poach fresh eggs in it.',
    'variations': [
        ['Green shakshuka', 'Replace the tomatoes and pepper with 1 lb chopped chard or spinach and a diced zucchini, wilted with the onion. Add 1/4 cup broth so the eggs have something to poach in.'],
        ['Add white beans', 'Stir a drained 15 oz can of cannellini beans into the sauce before the eggs for more protein and fiber.'],
        ['Make it gentler', 'Skip the red pepper flakes, use sweet paprika instead of smoked, and let the plate cool a little before eating.'],
        ['Protein boost', 'Add a third egg to your plate, or a larger spoonful of Greek yogurt.']
    ],
    'nutrition': {'calories': 310, 'protein': 20, 'carbs': 18, 'fat': 16, 'fiber': 4},
    'faq': [
        ['How do I know when the eggs are done?', 'The whites should be fully opaque with no clear, glassy patches, while the yolks still wobble when you shake the pan. They firm up a little more off the heat.'],
        ['Can I make just one serving?', 'Yes. Warm about 1 cup of the sauce in a small skillet, make two wells and poach two eggs, covered, for 4 to 6 minutes.'],
        ['My sauce is too thin and the eggs spread. What happened?', 'The sauce needed more time to reduce before the eggs went in. Simmer until a spoon leaves a visible trail, and it will hold neat wells.']
    ],
    'note': 'The easiest way to make this a small plate is to think in pairs: two eggs, a ladle of sauce and a spoonful of yogurt. Keep the extra sauce in the fridge, and on a day when cooking feels like too much, poach two eggs in a single portion in a small pan.',
}

# ------------------------------------------------------------------ Avocado toast
NEW['avocado-toast-jammy-eggs'] = {
    'title': 'Avocado Cottage Cheese Toast with Jammy Eggs',
    'subtitle': 'One slice of crisp sourdough, avocado whipped with cottage cheese and a soft-centered egg. About 20 g protein in a small breakfast.',
    'desc': 'One slice, a creamy protein spread, a jammy egg.',
    'serves': 2,
    'intro': [
        'Avocado toast is easy to eat, but on its own it is mostly bread and avocado. This version mashes a smaller avocado with cottage cheese, which keeps the spread creamy and green while roughly doubling the protein, then tops one slice of toast with a jammy egg. It is a small breakfast that still feels like a treat.',
        'The jammy yolk comes down to timing and a cold start. Egg whites set at a higher temperature than yolks, so a short, exact boil firms the white while the yolk stays soft and spoonable. The ice bath stops the cooking and helps the shell peel away cleanly.'
    ],
    'why': [
        ['About 20 g protein per slice', 'Cottage cheese in the spread plus a jammy egg on top.'],
        ['One slice is the serving', 'A small, complete breakfast instead of two heavy slices.'],
        ['Creamy and mild', 'The cottage cheese softens the avocado into a smooth, gentle spread.']
    ],
    'ingredients': [
        {'group': 'For the jammy eggs', 'items': [
            {'q': 2, 'u': '', 'n': 'large eggs', 'note': 'straight from the fridge'}
        ]},
        {'group': 'For the avocado spread', 'items': [
            {'q': 1, 'u': '', 'n': 'small ripe avocado', 'note': 'about 3.5 oz / 100 g flesh'},
            {'q': 0.5, 'u': 'cup', 'n': 'low-fat cottage cheese', 'g': 113},
            {'q': 1, 'u': 'tbsp', 'n': 'fresh lemon juice', 'note': 'about half a lemon'},
            {'q': 0.25, 'u': 'tsp', 'n': 'kosher salt', 'note': 'plus more to taste'},
            {'q': 0.25, 'u': 'tsp', 'n': 'red pepper flakes', 'note': 'optional'}
        ]},
        {'group': 'For the toast and topping', 'items': [
            {'q': 2, 'u': '', 'n': 'slices sourdough bread', 'note': 'about 1/2 inch (1.5 cm) thick'},
            {'q': 1, 'u': 'tsp', 'n': 'extra-virgin olive oil'},
            {'q': None, 'u': '', 'n': 'flaky sea salt and black pepper', 'note': 'to taste'},
            {'q': None, 'u': '', 'n': 'fresh chives', 'note': 'optional, for topping'}
        ]}
    ],
    'steps': [
        {'t': 'Boil the water',
         'd': 'Fill a small saucepan with enough water to cover the eggs by an inch and bring it to a full boil over high heat. Fill a bowl with ice and cold water and set it beside the stove.'},
        {'t': 'Cook the jammy eggs',
         'd': 'Lower the cold eggs into the boiling water with a slotted spoon and set a timer for 6 minutes 30 seconds. Turn the heat down slightly so the water holds a lively simmer instead of a violent boil, which can crack the shells.',
         'tip': 'For a runnier yolk, go 6 minutes. For a firmer yolk, go 7 minutes. Keep the same pan and number of eggs and your timing will stay consistent.'},
        {'t': 'Shock and peel',
         'd': 'Move the eggs straight into the ice bath and leave them for at least 3 minutes. Tap each egg all over on the counter to crack the shell, then peel under a trickle of cold water, starting at the wide end.'},
        {'t': 'Whip the avocado spread',
         'd': 'Scoop the avocado into a bowl and add the cottage cheese, lemon juice, salt and red pepper flakes if using. Mash with a fork until mostly smooth; for a silkier spread, blend it for a few seconds with a stick blender. Taste and add a pinch more salt or lemon if it seems flat.',
         'tip': 'Cottage cheese curds blend almost completely into the avocado. If you dislike the texture, a quick blitz makes it fully smooth.'},
        {'t': 'Toast the bread',
         'd': 'Brush the bread on both sides with the olive oil and toast it in a skillet over medium heat for 2 to 3 minutes per side, until golden and crisp. A toaster works too; brush with the oil afterwards.'},
        {'t': 'Assemble and serve',
         'd': 'Spread the avocado mixture over each slice, right to the edges. Halve an egg onto each toast and finish with flaky salt, black pepper and chives if using. Eat right away while the toast still crunches.'}
    ],
    'tips': [
        'Cook the eggs straight from the fridge. The timing assumes a cold egg.',
        'Make the eggs up to 3 days ahead and keep them peeled in the fridge. Warm them for 1 minute in hot tap water before slicing.',
        'The spread keeps for a day in the fridge with plastic wrap pressed onto its surface, so you can make it the night before.',
        SMALL_TIP
    ],
    'storage': 'The toast is best eaten right away. Peeled jammy eggs keep in an airtight container in the fridge for up to 3 days. Leftover avocado spread keeps for 1 day in a small container with plastic wrap pressed directly onto its surface.',
    'variations': [
        ['Dairy-free', 'Skip the cottage cheese and use the whole large avocado, then add a second egg to each toast to keep the protein up.'],
        ['Everything bagel style', 'Sprinkle the eggs with 1 teaspoon everything bagel seasoning and go lighter on the flaky salt.'],
        ['Gluten-free toast', 'Use gluten-free bread and toast it over slightly lower heat, since it browns faster.'],
        ['Make it gentler', 'Skip the chili, use a softer sandwich bread and cook the egg 7 minutes for a firmer, milder yolk.'],
        ['Protein boost', 'Add a second jammy egg, or a few slices of smoked salmon under the egg.']
    ],
    'nutrition': {'calories': 420, 'protein': 20, 'carbs': 40, 'fat': 19, 'fiber': 5},
    'faq': [
        ['Can I taste the cottage cheese?', 'Only a little. Blended with avocado, lemon and salt it reads as a creamy, slightly tangy spread. Start with 1/4 cup if you are unsure.'],
        ['Why will my eggs not peel cleanly?', 'Very fresh eggs stick to their shells, so use eggs that are at least a week old if you can, and do not rush the ice bath.'],
        ['How do I keep the spread from turning brown?', 'The lemon juice slows browning, and pressing plastic wrap onto the surface keeps out the air.']
    ],
    'note': 'Whipping cottage cheese into the avocado is the one change that makes the biggest difference here: same green spread, about twice the protein. One slice with one egg is a complete small breakfast; if you are still hungry, add the second egg rather than a second slice.',
    'diet': ['vegetarian'],
}

# ------------------------------------------------------------------ Overnight oats
NEW['overnight-oats'] = {
    'subtitle': 'Rolled oats soaked overnight with plenty of Greek yogurt, chia and vanilla, topped with blueberries. Three small jars, about 15 g protein each.',
    'desc': 'Three small jars, made the night before.',
    'serves': 3,
    'intro': [
        'Overnight oats are one of the easiest breakfasts to eat on a low-appetite morning: they are cold, soft and already portioned. This version doubles the Greek yogurt and divides the batch into three smaller jars, so each one carries about 15 g of protein without feeling heavy.',
        'Rolled oats have been steamed and flattened, so they soften fully in cold liquid given enough hours. Chia seeds form a gel as they absorb liquid, which thickens everything, and the extra yogurt makes the texture closer to a creamy pudding. A little less maple syrup keeps it from tasting too sweet once the blueberries release their juice.'
    ],
    'why': [
        ['About 15 g protein per jar', 'A full cup of Greek yogurt in the batch, plus milk, oats and chia.'],
        ['Small jars, no morning effort', 'Three ready portions that you can eat cold, straight from the fridge.'],
        ['Meal-prep friendly', 'The jars keep for up to 4 days, so one session covers most of the week.']
    ],
    'ingredients': [
        {'group': 'For the oats', 'items': [
            {'q': 1, 'u': 'cup', 'n': 'old-fashioned rolled oats', 'note': 'use certified gluten-free oats if needed', 'g': 90},
            {'q': 1, 'u': 'cup', 'n': 'milk', 'note': 'dairy or unsweetened soy milk, about 240 ml'},
            {'q': 1, 'u': 'cup', 'n': 'plain nonfat Greek yogurt', 'g': 240},
            {'q': 1, 'u': 'tbsp', 'n': 'chia seeds', 'g': 12},
            {'q': 1, 'u': 'tbsp', 'n': 'maple syrup', 'note': 'or honey, adjust to taste'},
            {'q': 1, 'u': 'tsp', 'n': 'vanilla extract'},
            {'q': 1, 'u': 'pinch', 'n': 'fine salt'},
            {'q': 0.5, 'u': 'tsp', 'n': 'lemon zest', 'note': 'optional'}
        ]},
        {'group': 'For the blueberries', 'items': [
            {'q': 1, 'u': 'cup', 'n': 'fresh or frozen blueberries', 'note': 'divided', 'g': 150},
            {'q': None, 'u': '', 'n': 'sliced almonds or chopped walnuts', 'note': 'optional, for topping'}
        ]}
    ],
    'steps': [
        {'t': 'Stir the base',
         'd': 'In a medium bowl, stir together the oats, milk, Greek yogurt, chia seeds, maple syrup, vanilla, salt and lemon zest if using. Mix for about 30 seconds, until the yogurt is fully blended and no dry oats float on top.',
         'tip': 'Stir well now. Chia seeds clump the moment they hit liquid, and a thorough mix at the start means an even texture in the morning.'},
        {'t': 'Fold in the berries',
         'd': 'Gently fold in about two-thirds of the blueberries, saving the rest for topping. Frozen berries can go in straight from the freezer; they thaw overnight.'},
        {'t': 'Portion into small jars',
         'd': 'Divide the mixture between three 8 to 12 oz jars or airtight containers, leaving a little room at the top for stirring. Seal tightly so the oats do not pick up fridge odors.'},
        {'t': 'Chill overnight',
         'd': 'Refrigerate for at least 6 hours, and ideally 8 hours or overnight, until thick, creamy and spoonable.',
         'tip': 'Short on time? Four hours will do, though the oats will be a bit chewier.'},
        {'t': 'Top and serve',
         'd': 'In the morning, stir a jar and add a splash of milk if it feels too stiff. Top with a few of the remaining blueberries and nuts if using. Eat cold, or microwave for 45 to 60 seconds, stirring halfway, until just warm.'}
    ],
    'tips': [
        'Use old-fashioned rolled oats. Quick oats turn to mush overnight, and steel-cut oats stay too hard without cooking.',
        'Sweeten lightly at night and adjust in the morning. The blueberries release juice as they sit, so the oats taste sweeter after soaking.',
        'With more yogurt the mixture is thicker. Add milk a tablespoon at a time in the morning until it is as loose as you like.',
        SMALL_TIP
    ],
    'storage': 'Keep sealed jars in the fridge for up to 4 days. The oats keep thickening, so loosen them with a splash of milk before eating, and add nuts just before serving so they stay crisp.',
    'variations': [
        ['Peanut butter and banana', 'Swap the blueberries for sliced banana, added in the morning, and stir 2 teaspoons of peanut butter into each jar.'],
        ['Dairy-free', 'Use unsweetened soy milk and a high-protein plant yogurt. Plant yogurts are often thinner and lower in protein, so check the label.'],
        ['Raspberry lemon', 'Use raspberries instead of blueberries and increase the lemon zest to 1 teaspoon.'],
        ['Make it gentler', 'Already cold and soft. Eat half a jar now and keep the rest for later.'],
        ['Protein boost', 'Stir 1 tablespoon of unflavored protein powder into each jar with a splash of extra milk, or top with a spoonful of Greek yogurt.']
    ],
    'nutrition': {'calories': 275, 'protein': 15, 'carbs': 41, 'fat': 6, 'fiber': 5},
    'faq': [
        ['Can I use steel-cut or quick oats?', 'Stick with rolled oats. Quick oats go mushy and steel-cut oats stay hard without cooking.'],
        ['Are overnight oats eaten cold?', 'Traditionally, yes. If you prefer warm, microwave a jar for 45 to 60 seconds, stirring halfway, with a splash of milk.'],
        ['Why are my oats too thick or too runny?', 'Yogurt and chia brands absorb differently. If too thick, stir in milk a tablespoon at a time. If runny, give it a few more hours, or add a teaspoon more chia next time.']
    ],
    'note': 'Three smaller jars instead of two big ones is the whole idea: each one is a full breakfast you can actually finish. The pinch of salt is worth keeping, since it makes the vanilla and blueberries taste sweeter with less syrup.',
}

# ------------------------------------------------------------------ apply
done = 0
for rid, fields in NEW.items():
    r = BY.get(rid)
    if r is None:
        sys.exit(f'ERROR: recipe {rid} not found. Nothing was saved.')
    if r.get('note') == fields['note']:
        print(f'- already applied: {rid}')
        continue
    fields = dict(fields)
    fields['steps'] = merge_steps(r.get('steps', []), fields['steps'])
    r.update(fields)
    set_tag(r, 'high-protein', fields['nutrition']['protein'] >= 15)
    print(f"- OK: {rid} -> {r['title']} ({fields['serves']} servings, ~{fields['nutrition']['protein']} g protein, ~{fields['nutrition']['calories']} kcal per serving)")
    done += 1

if done:
    m = re.match(r'\[\s*\n([ \t]+)\{', raw)
    indent = len(m.group(1)) if m else None
    with open(P('recipes.json'), 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=indent)
        f.write('\n')
print('Done.')
