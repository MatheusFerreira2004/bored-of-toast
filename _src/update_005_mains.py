#!/usr/bin/env python3
"""Recipes 4/4: sheet pan salmon, chicken avocado salad, breakfast burritos.

Same ids, URLs and photos. Smaller portions, more protein per calorie, neutral kitchen notes
(no "tested" claims). Steps are merged into the existing step objects, so step photos stay attached.

Nutrition per serving is an ESTIMATE: previous per-recipe estimate x old servings, minus removed
ingredients, plus added ones, divided by new servings. Reference values (USDA FoodData Central and
typical package labels, rounded; double-check before relying on them):
  olive oil, 1 tbsp (13.5 g): 119 kcal, 13.5 g fat
  plain nonfat Greek yogurt, per 100 g: 59 kcal, 10.2 P, 3.6 C, 0.4 F
  russet potato, raw, per 100 g: 79 kcal, 2.1 P, 18 C, 0.1 F, 1.3 fiber
  pork breakfast sausage, raw, per 100 g (typical label): 290 kcal, 14 P, 1 C, 25 F
  lean turkey breakfast sausage, raw, per 100 g (typical label): 160 kcal, 18 P, 1 C, 9 F
  liquid egg whites, per 100 g: 52 kcal, 10.9 P, 0.7 C, 0.2 F
  cheddar, per 100 g: 403 kcal, 24.9 P, 1.3 C, 33.1 F
  flour tortilla, per 100 g: 304 kcal, 8.2 P, 50 C, 7.8 F, 3.5 fiber

Salmon (was 4 x 380 kcal / 34 P / 10 C / 22 F / 0 fiber; same 1 1/2 lb salmon):
  -1 tbsp olive oil, +3/4 cup Greek yogurt (170 g) for the dill sauce, 6 portions instead of 4
  -> 1501 kcal, 153.3 P, 46.1 C, 75.2 F / 6 = ~250 kcal, 26 g protein, 8 C, 13 F, 0 fiber
Chicken avocado salad (was 2 x 520 / 42 / 14 / 34 / 8; same 1 lb chicken and 1 avocado):
  dressing oil 3 -> 1 tbsp, +1/4 cup Greek yogurt (60 g), 3 bowls instead of 2
  -> 837 kcal, 90.1 P, 30.2 C, 41.2 F, 16 fiber / 3 = ~280 kcal, 30 g protein, 10 C, 14 F, 5 fiber
Breakfast burritos (was 8 x 560 / 28 / 42 / 31 / 3):
  potatoes 1 1/2 -> 1 lb, pork -> lean turkey sausage (1 lb), +1 cup egg whites (243 g),
  cheddar 2 -> 1 cup (-113 g), 8 x 10-inch tortillas (560 g) -> 12 x 8-inch (540 g)
  -> 3321 kcal, 234.2 P, 285.3 C, 136.7 F, 20.3 fiber / 12 = ~280 kcal, 20 g protein, 24 C, 11 F, 2 fiber

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

# ------------------------------------------------------------------ Sheet pan salmon
NEW['sheet-pan-salmon'] = {
    'subtitle': 'Small salmon portions brushed with honey, Dijon and garlic, roasted under lemon and herbs, with a cool Greek yogurt dill sauce. About 26 g protein per 4 oz piece.',
    'desc': 'Small glazed portions with a cool dill yogurt.',
    'serves': 6,
    'intro': [
        'Salmon is one of the most protein-dense things you can put on a small plate, and a 4 oz piece is easier to face on a low-appetite day than a full 6 oz fillet. This version cuts a pound and a half of salmon into six smaller portions, uses half the oil in the glaze and adds a cool Greek yogurt and dill sauce on the side for extra protein.',
        'A hot sheet pan is also one of the most forgiving ways to cook fish: no flipping, nothing stuck to a skillet and less lingering smell. The honey in the glaze browns quickly at 400°F, while the Dijon helps the glaze cling to the fish instead of sliding into the pan. Lemon slices laid on top release a little steam, which keeps the center silky.'
    ],
    'why': [
        ['About 26 g protein per piece', 'A 4 oz portion of salmon plus a spoonful of yogurt sauce.'],
        ['Small, even portions', 'Six pieces from one fillet, so each plate is a size you can finish.'],
        ['Mild on harder days', 'Serve it at room temperature with the cool sauce for less aroma.']
    ],
    'ingredients': [
        {'group': 'For the salmon', 'items': [
            {'q': 1.5, 'u': 'lb', 'n': 'salmon fillet', 'note': 'cut into 6 portions, about 4 oz / 113 g each, skin on or off', 'g': 680},
            {'q': 1, 'u': '', 'n': 'lemon', 'note': 'thinly sliced'},
            {'q': None, 'u': '', 'n': 'fresh thyme and dill sprigs'},
            {'q': None, 'u': '', 'n': 'salt and black pepper'}
        ]},
        {'group': 'For the glaze', 'items': [
            {'q': 1, 'u': 'tbsp', 'n': 'olive oil'},
            {'q': 2, 'u': 'tbsp', 'n': 'honey'},
            {'q': 1, 'u': 'tbsp', 'n': 'Dijon mustard'},
            {'q': 2, 'u': '', 'n': 'garlic cloves', 'note': 'minced'}
        ]},
        {'group': 'For the dill yogurt sauce', 'items': [
            {'q': 0.75, 'u': 'cup', 'n': 'plain nonfat Greek yogurt', 'g': 170},
            {'q': 1, 'u': 'tbsp', 'n': 'fresh lemon juice'},
            {'q': 1, 'u': 'tbsp', 'n': 'fresh dill', 'note': 'chopped'},
            {'q': 1, 'u': 'pinch', 'n': 'salt'}
        ]}
    ],
    'steps': [
        {'t': 'Heat the oven',
         'd': 'Preheat the oven to 400°F (200°C) with a rack in the center, and line a rimmed sheet pan with parchment paper. Give the oven the full 15 minutes to heat so the glaze starts sizzling as soon as the pan goes in.'},
        {'t': 'Portion and season',
         'd': 'Cut the salmon into 6 even pieces, about 4 oz each, and pat them very dry with paper towels. Arrange them on the pan with about an inch between them so hot air can circulate, then season both sides with salt and pepper.',
         'tip': 'Cut across the fillet so each piece has a similar thickness. Even pieces finish at the same time, so none of them dry out.'},
        {'t': 'Glaze and make the sauce',
         'd': 'Whisk the olive oil, honey, Dijon and garlic until smooth, about 20 seconds, and brush it over the tops and sides of each piece. In a second bowl, stir together the Greek yogurt, lemon juice, chopped dill and a pinch of salt, then refrigerate it until serving.'},
        {'t': 'Top and roast',
         'd': 'Lay the lemon slices and herb sprigs over the salmon. Roast for 10 to 12 minutes, until the glaze bubbles at the edges, the flesh turns opaque and the thickest part flakes with a fork. An instant-read thermometer should read 125 to 130°F (52 to 54°C) for medium.',
         'tip': 'Smaller pieces cook faster than whole fillets. Start checking at 9 minutes, and pull thin pieces as they finish.'},
        {'t': 'Rest and serve small',
         'd': 'Let the salmon rest on the pan for 2 minutes so the center finishes cooking. Serve one piece per plate with a spoonful of the dill yogurt sauce. A small scoop of rice or some roasted vegetables is optional.'}
    ],
    'tips': [
        'Take the salmon out of the fridge 15 minutes before cooking. A less chilled center cooks at the same pace as the edges.',
        'Seeing white beads on the surface? That is albumin, a protein pushed out as fish overcooks. Next time, pull it a minute sooner.',
        'Skin-on pieces lift cleanly off the parchment, leaving the skin behind.',
        SMALL_TIP
    ],
    'storage': 'Refrigerate leftover salmon in an airtight container for up to 2 days and the yogurt sauce for up to 3 days. Eat the salmon cold, flaked over salad, or reheat it covered at 275°F (135°C) for about 8 minutes so it warms through without drying out.',
    'variations': [
        ['Maple and whole-grain mustard', 'Swap the honey for maple syrup and use whole-grain mustard. The roasting time stays the same.'],
        ['Whole-meal sheet pan', 'Toss asparagus or green beans with a little oil and salt and roast them around the fish in the same 10 to 12 minutes.'],
        ['Dairy-free', 'Skip the yogurt sauce and finish with extra lemon and fresh herbs.'],
        ['Make it gentler', 'Serve the salmon at room temperature, skip the garlic in the glaze and keep the sauce cool. Cooler food tends to smell less.'],
        ['Protein boost', 'Serve over a few spoonfuls of white beans or lentils, or add a second piece on hungrier days.']
    ],
    'nutrition': {'calories': 250, 'protein': 26, 'carbs': 8, 'fat': 13, 'fiber': 0},
    'faq': [
        ['How do I know when salmon is done without a thermometer?', 'Press a fork into the thickest part and twist gently. If it separates into flakes and the center has just turned opaque, it is ready.'],
        ['Can I use frozen salmon?', 'Yes, but thaw it first, ideally overnight in the fridge. Roasting from frozen leaves the outside overdone before the middle cooks.'],
        ['Why did my glaze burn?', 'Honey scorches quickly, especially near the pan edges. Keep the pan on the center rack, use parchment, and check early if your oven runs hot.']
    ],
    'note': 'Cutting the fillet into six smaller pieces is the main change here: each one is a complete small plate, and the cool yogurt sauce adds protein without adding effort. Leftover pieces are good cold the next day, flaked over greens.',
    'diet': ['gluten-free'],
}

# ------------------------------------------------------------------ Chicken avocado salad
NEW['chicken-avocado-salad'] = {
    'subtitle': 'Paprika-rubbed chicken, seared and sliced thin over greens, with avocado and a creamy lemon yogurt dressing. Three smaller bowls, about 30 g protein each.',
    'desc': 'Three smaller bowls, creamy lemon dressing.',
    'serves': 3,
    'intro': [
        'A chicken salad is one of the easiest ways to put a lot of protein on a small plate, as long as the chicken is juicy and the dressing actually clings. This version shares two chicken breasts across three smaller bowls and swaps most of the oil in the dressing for Greek yogurt, so each bowl carries about 30 g of protein at a lighter weight.',
        'The secret to good seared chicken is a dry surface. Patting it with paper towels removes the moisture that would otherwise have to boil off before the browning can start, which is why a wet breast steams and turns gray. A short rest afterwards lets the juices settle back into the meat, so it stays moist when you slice it thin.'
    ],
    'why': [
        ['About 30 g protein per bowl', 'Chicken plus a Greek yogurt dressing in a lighter, smaller bowl.'],
        ['Creamy, not oily', 'Yogurt replaces most of the oil in the dressing and still coats the leaves.'],
        ['Built for meal prep', 'Cook the chicken and whisk the dressing ahead, then assemble a bowl in minutes.']
    ],
    'ingredients': [
        {'group': 'For the chicken', 'items': [
            {'q': 2, 'u': '', 'n': 'boneless, skinless chicken breasts', 'note': 'about 1 lb / 450 g', 'g': 450},
            {'q': 1, 'u': 'tsp', 'n': 'smoked paprika'},
            {'q': 1, 'u': 'tsp', 'n': 'garlic powder'},
            {'q': 0.5, 'u': 'tsp', 'n': 'kosher salt'},
            {'q': 1, 'u': 'tbsp', 'n': 'olive oil'}
        ]},
        {'group': 'For the creamy lemon dressing', 'items': [
            {'q': 0.25, 'u': 'cup', 'n': 'plain nonfat Greek yogurt', 'g': 60},
            {'q': 1, 'u': 'tbsp', 'n': 'extra-virgin olive oil'},
            {'q': 1.5, 'u': 'tbsp', 'n': 'fresh lemon juice'},
            {'q': 1, 'u': 'tsp', 'n': 'honey'},
            {'q': 1, 'u': 'tbsp', 'n': 'water', 'note': 'to loosen'},
            {'q': None, 'u': '', 'n': 'salt and black pepper', 'note': 'to taste'}
        ]},
        {'group': 'For the salad', 'items': [
            {'q': 4, 'u': 'cups', 'n': 'arugula and mixed greens', 'g': 80},
            {'q': 1, 'u': 'cup', 'n': 'cherry tomatoes', 'note': 'halved', 'g': 150},
            {'q': 1, 'u': '', 'n': 'ripe avocado', 'note': 'sliced'},
            {'q': 1, 'u': 'tbsp', 'n': 'sesame seeds', 'note': 'toasted'}
        ]}
    ],
    'steps': [
        {'t': 'Dry and season the chicken',
         'd': 'Pat the chicken breasts thoroughly dry with paper towels. If one end is much thicker, pound it to an even 3/4-inch thickness between two sheets of plastic wrap. Rub all over with the olive oil, then season both sides with the smoked paprika, garlic powder and salt.',
         'tip': 'Even thickness matters most with breasts. A thin tail and a thick middle means one part dries out while the other is still pink.'},
        {'t': 'Sear without touching',
         'd': 'Heat a grill pan or skillet over medium-high heat until a drop of water hisses on contact. Lay in the chicken and leave it alone for 5 to 6 minutes, until it releases easily and the underside is deep golden. Flip and cook another 5 to 6 minutes, until the thickest part reads 165°F (74°C).',
         'tip': 'If the chicken sticks when you try to flip it, wait another minute. Once the crust forms, it releases on its own.'},
        {'t': 'Rest, then slice thin',
         'd': 'Move the chicken to a cutting board and let it rest for 5 minutes. Slice it thinly against the grain, or shred it with two forks; thinner pieces are easier to eat on low-appetite days.'},
        {'t': 'Whisk the dressing',
         'd': 'Whisk the Greek yogurt, olive oil, lemon juice, honey and water with a pinch of salt and pepper until smooth and pourable. Taste and add a little more lemon or salt if it needs brightness.'},
        {'t': 'Build three bowls',
         'd': 'Toss the greens and cherry tomatoes with half the dressing and divide among three bowls. Top with the sliced chicken and avocado, drizzle with the remaining dressing and scatter the toasted sesame seeds over the top.'}
    ],
    'tips': [
        'Salt the chicken up to a day ahead and leave it uncovered in the fridge. It seasons the meat more deeply and dries the surface for a better crust.',
        'Toast the sesame seeds in a dry skillet for 2 to 3 minutes, shaking the pan, until golden and fragrant.',
        'Slice the avocado just before serving and squeeze a little lemon over it to slow browning.',
        SMALL_TIP
    ],
    'storage': 'Keep the cooked chicken, washed greens and dressing in separate airtight containers in the fridge for up to 3 days. Stir the dressing before using, and loosen it with a teaspoon of water if it has thickened. Eat the chicken cold, or warm it in a skillet over medium-low heat for 2 to 3 minutes, and slice the avocado fresh.',
    'variations': [
        ['Dairy-free', 'Replace the yogurt dressing with 2 tablespoons olive oil, 1 tablespoon lemon juice and 1 teaspoon honey shaken in a jar.'],
        ['Use chicken thighs', 'Boneless thighs stay juicier and forgive overcooking. Cook 6 to 7 minutes per side, to 175°F (80°C).'],
        ['Roll it into wraps', 'Chop everything smaller and roll into small tortillas, with the dressing on the side so the wrap stays crisp.'],
        ['Make it gentler', 'Shred the chicken instead of slicing it, use milder lettuce instead of arugula, and go light on the lemon.'],
        ['Protein boost', 'Add a soft-boiled egg or a handful of shelled edamame to each bowl.']
    ],
    'nutrition': {'calories': 280, 'protein': 30, 'carbs': 10, 'fat': 14, 'fiber': 5},
    'faq': [
        ['How do I know the chicken is done without a thermometer?', 'Cut into the thickest part. The juices should run clear and the meat should be opaque all the way through. A thermometer is still the most reliable option for lean breasts.'],
        ['Can I make the dressing ahead?', 'Yes. It keeps in a sealed jar in the fridge for up to 3 days. Stir well before using.'],
        ['Why did my chicken turn out dry?', 'It was likely cooked past 165°F or sliced right away without resting. Pull it as soon as the thickest part hits temperature.']
    ],
    'note': 'Two breasts across three bowls, with a yogurt dressing instead of an oily one, is what makes this a small plate that still feels like a full meal. Resting the chicken before slicing is the step that keeps it juicy, so it is worth the five minutes.',
    'diet': ['gluten-free'],
}

# ------------------------------------------------------------------ Breakfast burritos
NEW['breakfast-burritos'] = {
    'subtitle': 'Twelve smaller burritos with crisp potatoes, lean turkey sausage, soft-scrambled eggs and cheddar, rolled and frozen. About 20 g protein each, ready in two minutes.',
    'desc': 'Twelve smaller burritos, lean sausage, extra eggs.',
    'serves': 12,
    'intro': [
        'A freezer full of breakfast burritos means a warm, savory breakfast is always a couple of minutes away, which helps on mornings when cooking feels like too much. This version makes them smaller and leaner: 8-inch tortillas instead of 10-inch, lean turkey sausage instead of pork, extra egg whites and a lighter hand of cheese. Each burrito carries about 20 g of protein and is a size you can actually finish.',
        'The cooling step matters more than it looks. Warm filling keeps releasing steam inside the wrap, and in the freezer that moisture turns to ice crystals that soak the tortilla when it thaws. Spreading everything on a sheet pan lets the steam escape fast, and pulling the eggs while they are still glossy leaves room for the second cook when you reheat.'
    ],
    'why': [
        ['About 20 g protein per burrito', 'Lean turkey sausage, whole eggs and egg whites in a smaller wrap.'],
        ['Twelve at once', 'One session of cooking covers almost two weeks of breakfasts for one.'],
        ['Straight from the freezer', 'Smaller burritos reheat in about 2 minutes, with no thawing needed.']
    ],
    'ingredients': [
        {'group': 'For the filling', 'items': [
            {'q': 1, 'u': 'lb', 'n': 'russet potatoes', 'note': 'peeled and cut into 1/2-inch cubes (about 3 cups)', 'g': 450},
            {'q': 1, 'u': 'tbsp', 'n': 'olive oil'},
            {'q': 1, 'u': 'lb', 'n': 'lean turkey breakfast sausage', 'note': 'bulk or casings removed'},
            {'q': 1, 'u': '', 'n': 'red bell pepper', 'note': 'finely diced (about 1 cup)', 'g': 150},
            {'q': 12, 'u': '', 'n': 'large eggs'},
            {'q': 1, 'u': 'cup', 'n': 'liquid egg whites', 'g': 243},
            {'q': 2, 'u': 'tbsp', 'n': 'milk'},
            {'q': 1, 'u': 'tbsp', 'n': 'butter'},
            {'q': 4, 'u': '', 'n': 'green onions', 'note': 'thinly sliced'},
            {'q': 0.5, 'u': 'tsp', 'n': 'smoked paprika'},
            {'q': 1.5, 'u': 'tsp', 'n': 'kosher salt', 'note': 'divided'},
            {'q': 0.5, 'u': 'tsp', 'n': 'black pepper'}
        ]},
        {'group': 'For assembly', 'items': [
            {'q': 12, 'u': '', 'n': 'flour tortillas', 'note': '8-inch size'},
            {'q': 1, 'u': 'cup', 'n': 'shredded sharp cheddar', 'note': 'or a Mexican blend', 'g': 113},
            {'q': 0.5, 'u': 'cup', 'n': 'thick salsa', 'note': 'optional, drained if watery'}
        ]}
    ],
    'steps': [
        {'t': 'Steam, then crisp the potatoes',
         'd': 'Heat the olive oil in a large nonstick skillet over medium-high heat. Add the potatoes in an even layer with 1/2 teaspoon salt, cover and cook for 8 minutes. Uncover and cook 5 to 7 minutes more, stirring every couple of minutes, until golden on several sides and a knife slides in easily. Spread on a large sheet pan to cool.',
         'tip': 'Covering the pan first steams the potatoes through, then uncovering drives off the moisture so the outsides can crisp.'},
        {'t': 'Brown the sausage and pepper',
         'd': 'In the same skillet over medium heat, cook the turkey sausage for 6 to 7 minutes, breaking it into small crumbles, until browned with no pink remaining. Add the bell pepper and smoked paprika and cook 2 to 3 minutes, until the pepper softens. Spread the mixture on the sheet pan with the potatoes.',
         'tip': 'Lean turkey sausage releases little fat, so if it starts to stick, add a tablespoon of water and scrape up the browned bits.'},
        {'t': 'Softly scramble the eggs',
         'd': 'Whisk the eggs, egg whites, milk, remaining 1 teaspoon salt and the black pepper until no streaks remain. Wipe out the skillet, melt the butter over medium-low heat until foamy, then add the eggs. Stir slowly for 5 to 6 minutes, pushing the curds from the edges to the center, until just set but still glossy. Fold in the green onions and add to the sheet pan.',
         'tip': 'Pull the eggs while they still look a touch underdone. They finish cooking when you reheat, and fully cooked eggs turn rubbery later.'},
        {'t': 'Cool the filling completely',
         'd': 'Toss everything on the sheet pan together and spread it into a thin, even layer. Let it cool at room temperature for about 15 minutes, until it stops steaming and feels barely warm to the touch. This keeps condensation, the main cause of soggy burritos, out of the wrap.'},
        {'t': 'Warm the tortillas and roll',
         'd': 'Stack the tortillas under a damp paper towel and microwave for 30 seconds, until soft and pliable. Sprinkle each with a little cheese, then spoon about 2/3 cup filling in a log just below the center and add a spoonful of salsa if using. Fold in the sides, then roll up tightly from the bottom.'},
        {'t': 'Wrap and freeze',
         'd': 'Wrap each burrito snugly in foil or parchment, then slide them into large zip-top freezer bags and press out as much air as possible. Label with the date and freeze flat for up to 3 months, or refrigerate for up to 4 days.',
         'tip': 'Choose parchment if you will reheat in the microwave. You can heat the burrito right in its wrapper.'}
    ],
    'tips': [
        'Drain watery salsa in a fine-mesh strainer for 10 minutes before using it. Excess liquid is the second biggest cause of soggy burritos.',
        'Put the cheese down first, directly on the tortilla. It acts as a moisture barrier and melts into glue that holds the roll together.',
        'Check the sausage label. Lean turkey breakfast sausages vary a lot in fat and salt, so taste the filling before adding the last of the salt.',
        'Small-portion tip: eat half a burrito now and wrap the other half for later. Half still counts.'
    ],
    'storage': 'Refrigerate wrapped burritos for up to 4 days or freeze in zip-top freezer bags for up to 3 months. To reheat from frozen, remove any foil, wrap in a damp paper towel or keep in parchment, and microwave for 1 1/2 to 2 minutes, flipping halfway. For a crisper tortilla, bake foil-wrapped burritos straight from frozen at 375°F (190°C) for 25 to 30 minutes.',
    'variations': [
        ['Go vegetarian', 'Swap the sausage for one 15-oz can black beans, rinsed and patted very dry, and add 1/2 teaspoon cumin with the smoked paprika.'],
        ['Add greens', 'Wilt 4 cups baby spinach in the skillet after the sausage, then squeeze it dry in a towel before adding.'],
        ['Gluten-free', 'Use gluten-free tortillas and check the sausage label. Warm the tortillas well so they roll without cracking.'],
        ['Make it gentler', 'Eat half a burrito at a time, skip the salsa and hot sauce on queasy days, and let it cool slightly before eating.'],
        ['Protein boost', 'Serve with a spoonful of plain Greek yogurt instead of sour cream.']
    ],
    'nutrition': {'calories': 280, 'protein': 20, 'carbs': 24, 'fat': 11, 'fiber': 2},
    'faq': [
        ['Can I skip the potatoes?', 'Yes. Add 4 more eggs or another 1/2 lb sausage to keep the filling hearty, and expect about 10 burritos instead of 12.'],
        ['Why are my frozen burritos soggy?', 'The filling was probably still warm when you rolled it, or the salsa was watery. Cool everything until it stops steaming and drain the salsa.'],
        ['Do I need to thaw them before reheating?', 'No. They reheat well straight from frozen. Thawing overnight in the fridge cuts microwave time to about 1 minute.']
    ],
    'note': 'Smaller tortillas, leaner sausage and extra egg whites are what turn these into small plates without losing the comfort. One Sunday batch fills the freezer, and on a slow morning, half a burrito and a cup of tea is a perfectly good start.',
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
