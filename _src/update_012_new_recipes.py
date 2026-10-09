#!/usr/bin/env python3
"""Replace the 10 off-focus recipes with 10 new small-plate recipes (free Pexels photos, no AI).

For each new recipe:
- recipe data in recipes.json (same position as the recipe it replaces)
- main photo images/<id>.webp (1200x900), share image images/og/<id>.jpg (1200x630)
  and Pinterest image images/pins/<id>.jpg (1000x1500, photo + title band)
- photo credit in credits.json
Old recipes: images, og/pin images, unused step photos and credits are removed, and the old
URLs become redirect stubs to the closest new recipe (no broken links).
build.py: "Everyday Favorites" category becomes "Snacks", new ids join FOCUS_IDS, and any other
reference to an old id is pointed to its replacement. checks.py registers the redirect stubs.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values and typical
package labels (rounded). Main assumptions per 100 g unless noted:
  egg (50 g each) 72 kcal 6.3 P 0.4 C 4.8 F | liquid egg whites 52 / 10.9 / 0.7 / 0.2
  low-fat cottage cheese 84 / 11 / 4.3 / 2.3 | plain nonfat Greek yogurt 59 / 10.2 / 3.6 / 0.4
  rolled oats 379 / 13.2 / 67.7 / 6.5 / 10.1 fiber | 93% lean ground turkey (raw) 150 / 18.7 / 0 / 8.3
  chicken breast (raw) 120 / 22.5 / 0 / 2.6 | cod (raw) 82 / 17.8 / 0 / 0.7
  canned beans, drained 114 / 7.3 / 21 / 0.4 / 6.4 fiber | jarred marinara 56 / 1.6 / 8.8 / 1.6 / 1.6 fiber
  jasmine rice (dry) 365 / 7.1 / 80 / 0.7 | peanut butter 588 / 25 / 20 / 50 / 6 fiber
  olive oil 1 tbsp = 119 kcal 13.5 F | butter 1 tbsp = 100 kcal 11.4 F
Per-serving totals (recipe total / servings):
  cottage-cheese-pancakes      994 kcal, 72 P, 92 C, 37 F, 10 fib / 4  -> 250, 18, 23, 9, 3
  spinach-feta-omelette        per omelette                            -> 280, 23, 5, 18, 1
  turkey-meatballs-marinara    1830, 157, 87, 95, 12 / 6              -> 305, 26, 15, 16, 2
  turkey-bean-chili            1849, 156, 190, 60, 51 / 6             -> 310, 26, 32, 10, 8
  lemon-herb-baked-cod         501, 81, 2, 17, 0 / 4                  -> 125, 20, 1, 4, 0
  chicken-congee               1235, 130, 123, 21, 3 / 6              -> 205, 22, 20, 4, 0
  southwest-chicken-salad-bowl 1387, 145, 128, 35, 27 / 4             -> 345, 36, 32, 9, 7
  blackberry-yogurt-parfait    447, 40, 57, 8, 9 / 2                  -> 225, 20, 28, 4, 5
  peanut-butter-oat-bites      1587, 72, 168, 79, 25 / 16             -> 100, 5, 11, 5, 2
  cinnamon-baked-apples-pears  880, 31, 130, 33, 22 / 4               -> 220, 8, 32, 8, 5

Run automatically by Auto build. Nothing is saved unless every download succeeds. Safe to re-run.
"""
import glob, io, json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)
SMALL_TIP = 'Small-portion tip: serve half a portion and save the rest for later. A half bowl still counts.'

raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(raw)
ids = [r['id'] for r in recipes]
if 'cottage-cheese-pancakes' in ids:
    print('Already applied. Nothing to do.')
    sys.exit(0)

# old id -> new id (closest match; also used for URL redirects)
MAP = {
    'buttermilk-pancakes': 'cottage-cheese-pancakes',
    'cinnamon-french-toast': 'spinach-feta-omelette',
    'creamy-garlic-pasta': 'turkey-meatballs-marinara',
    'beef-tacos': 'turkey-bean-chili',
    'honey-garlic-chicken-thighs': 'lemon-herb-baked-cod',
    'mushroom-risotto': 'chicken-congee',
    'harvest-kale-salad': 'southwest-chicken-salad-bowl',
    'chocolate-mousse-cake': 'blackberry-yogurt-parfait',
    'chocolate-chip-cookies': 'peanut-butter-oat-bites',
    'apple-crisp': 'cinnamon-baked-apples-pears',
}
missing = [o for o in MAP if o not in ids]
if missing:
    sys.exit(f'ERROR: old recipes not found: {missing}. Nothing was saved.')

PHOTOS = {
    'cottage-cheese-pancakes': (5738531, 'Eva Bronzini', 'https://www.pexels.com/@eva-bronzini',
        'https://www.pexels.com/photo/stacked-pancakes-garnished-with-berries-5738531/',
        'A stack of pancakes topped with strawberries and blueberries.'),
    'spinach-feta-omelette': (4393001, 'Spencer Davis', 'https://www.pexels.com/@spencer',
        'https://www.pexels.com/photo/meal-on-plate-4393001/',
        'A spinach omelette served with greens and toast.'),
    'turkey-meatballs-marinara': (34314421, 'ERIVELTO Martins', 'https://www.pexels.com/@erivas',
        'https://www.pexels.com/photo/delicious-meatballs-in-rich-tomato-sauce-34314421/',
        'Meatballs in tomato sauce garnished with parsley.'),
    'turkey-bean-chili': (15881322, 'Julias Torten und Törtchen', 'https://www.pexels.com/@julias-torten-und-tortchen-434418',
        'https://www.pexels.com/photo/chili-con-carne-stew-15881322/',
        'A bowl of chili with beans and corn, topped with a creamy garnish.'),
    'lemon-herb-baked-cod': (37367757, 'Mahi Mog', 'https://www.pexels.com/@mahimoh',
        'https://www.pexels.com/photo/delicious-baked-fish-with-lemon-and-herbs-37367757/',
        'Baked white fish with lemon and herbs, served with rice.'),
    'chicken-congee': (36340265, 'ivi nnnnnn', 'https://www.pexels.com/@ivi-nnnnnn-129330',
        'https://www.pexels.com/photo/delicious-asian-congee-breakfast-with-tea-set-36340265/',
        'A bowl of creamy congee with spring onions and chicken.'),
    'southwest-chicken-salad-bowl': (37648022, 'Tochukwu Ekeh', 'https://www.pexels.com/@tochukwu-ekeh-2149052634',
        'https://www.pexels.com/photo/fresh-colorful-chicken-salad-with-vegetables-37648022/',
        'A chicken salad bowl with fresh vegetables and crunchy tortilla strips.'),
    'blackberry-yogurt-parfait': (14853978, 'Soumia Photography', 'https://www.pexels.com/@soumia-photography-131641539',
        'https://www.pexels.com/photo/milk-cereals-and-blackberries-14853978/',
        'A glass parfait layered with yogurt, blackberries and granola.'),
    'peanut-butter-oat-bites': (4637456, 'Milan', 'https://www.pexels.com/@milan-3053700',
        'https://www.pexels.com/photo/brown-energy-balls-on-plate-for-dessert-4637456/',
        'Homemade oat energy bites on a glass plate.'),
    'cinnamon-baked-apples-pears': (8551536, 'Dasha Klimova', 'https://www.pexels.com/@doraklimova',
        'https://www.pexels.com/photo/baked-apple-and-pear-slices-with-nuts-8551536/',
        'Baked apple and pear slices with cinnamon and nuts.'),
}


def I(q, u, n, note=None, g=None):
    d = {'q': q, 'u': u, 'n': n}
    if note: d['note'] = note
    if g: d['g'] = g
    return d


def S(t, d, tip=None):
    s = {'t': t, 'd': d}
    if tip: s['tip'] = tip
    return s


NEW = {}

NEW['cottage-cheese-pancakes'] = dict(
    title='Cottage Cheese Protein Pancakes',
    subtitle='Fluffy oat pancakes blended with cottage cheese and eggs, topped with berries and a spoon of Greek yogurt. Three small pancakes, about 18 g protein.',
    desc='Blender pancakes, three small ones per plate.',
    category='Beyond Toast', tags=['healthy', 'small-plates', 'high-protein', 'make-ahead'], diet=['vegetarian'],
    prep=10, cook=15, time=25, serves=4, level='Easy',
    intro=['Pancakes are one of the easiest breakfasts to enjoy on a slow morning, but a classic stack is mostly flour, butter and syrup. This version blends cottage cheese, eggs and rolled oats into a smooth batter, so three small pancakes carry about 18 g of protein and still taste like a weekend breakfast.',
           'The blender does the work. Blitzing the oats turns them into flour, and the cottage cheese curds disappear completely, leaving a batter that cooks up tender and slightly custardy. Letting it rest for five minutes gives the oats time to absorb liquid, which helps the pancakes hold together when you flip them.'],
    why=[['About 18 g protein per plate', 'Cottage cheese, eggs and a spoonful of Greek yogurt with three small pancakes.'],
         ['One blender, no flour', 'Rolled oats become the flour, so the batter comes together in two minutes.'],
         ['Freezer friendly', 'Freeze extras flat and toast them straight from frozen on busy mornings.']],
    ingredients=[{'group': 'For the batter', 'items': [
        I(1, 'cup', 'low-fat cottage cheese', g=226), I(4, '', 'large eggs'),
        I(0.75, 'cup', 'old-fashioned rolled oats', 'use certified gluten-free oats if needed', 68),
        I(1, 'tsp', 'baking powder'), I(1, 'tbsp', 'maple syrup'), I(1, 'tsp', 'vanilla extract'), I(1, 'pinch', 'fine salt')]},
        {'group': 'To cook and serve', 'items': [
        I(2, 'tsp', 'butter', 'for the pan'), I(1, 'cup', 'mixed berries', 'such as strawberries and blueberries', 150),
        I(0.5, 'cup', 'plain nonfat Greek yogurt', g=120)]}],
    steps=[S('Blend the batter', 'Add the cottage cheese, eggs, oats, baking powder, maple syrup, vanilla and salt to a blender. Blend for 45 to 60 seconds, until completely smooth with no visible curds. Let the batter rest for 5 minutes.', 'The rest lets the oats absorb liquid, so the batter thickens slightly and the pancakes are easier to flip.'),
           S('Heat the pan', 'Heat a large nonstick skillet or griddle over medium-low heat. Melt a little butter, then wipe it around with a paper towel so only a thin film remains.'),
           S('Cook small pancakes', 'Pour about 3 tablespoons of batter per pancake, leaving space between them. Cook for 2 to 3 minutes, until small bubbles form on the surface, the edges look set and the underside is golden.', 'Use a lower heat than you would for flour pancakes. Eggs and cottage cheese brown faster.'),
           S('Flip and finish', 'Flip gently and cook for 1 to 2 minutes more, until the center springs back when pressed. Keep finished pancakes warm in a 200°F (95°C) oven while you cook the rest, adding a little more butter to the pan as needed.'),
           S('Serve small', 'Serve three pancakes per plate with berries and a spoonful of Greek yogurt.')],
    tips=['Blend until there are no visible curds. A smooth batter gives a tender, even pancake.',
          'If the batter thickens too much while it rests, stir in a tablespoon of milk.',
          'Keep the pancakes small. This batter is softer than a flour batter, so large pancakes are harder to flip.',
          'Small-portion tip: start with two pancakes and add a third only if you want it.'],
    storage='Cool completely, then refrigerate in an airtight container for up to 3 days, or freeze in a single layer and transfer to a freezer bag for up to 2 months. Reheat in a toaster or a dry skillet over medium-low heat until warmed through.',
    variations=[['Banana and cinnamon', 'Blend half a ripe banana and 1/2 tsp cinnamon into the batter, and skip the maple syrup.'],
                ['Lemon blueberry', 'Add the zest of 1 lemon to the batter and scatter a few blueberries onto each pancake before flipping.'],
                ['Gluten-free', 'Use certified gluten-free rolled oats; the batter has no wheat flour.'],
                ['Make it gentler', 'Skip the berries and serve with a spoonful of yogurt and a little applesauce.'],
                ['Protein boost', 'Serve with an extra spoonful of Greek yogurt, or blend 1/4 cup more cottage cheese into the batter.']],
    nutrition={'calories': 250, 'protein': 18, 'carbs': 23, 'fat': 9, 'fiber': 3},
    faq=[['Can I taste the cottage cheese?', 'Not really. Once blended with oats, eggs and vanilla, it tastes like a mild, slightly tangy pancake.'],
         ['Why are my pancakes falling apart?', 'The heat may be too high or the pancakes too large. Cook small pancakes over medium-low heat and wait until the edges look set before flipping.'],
         ['Can I use quick oats or oat flour?', 'Yes. Use 3/4 cup quick oats, or 2/3 cup oat flour, and blend as written.']],
    note='Small pancakes are the trick here: they cook through before the outside gets too dark and are easier to flip. Three per plate with fruit and yogurt is a complete breakfast; freeze the rest for mornings when you do not feel like cooking.')

NEW['spinach-feta-omelette'] = dict(
    title='Spinach and Feta Omelette',
    subtitle='A soft omelette made with whole eggs and egg whites, folded around wilted spinach and feta. About 23 g protein, ready in 15 minutes.',
    desc='Soft eggs, spinach and feta in 15 minutes.',
    category='Beyond Toast', tags=['healthy', 'quick', 'small-plates', 'high-protein', 'gentle'], diet=['vegetarian', 'gluten-free'],
    prep=5, cook=10, time=15, serves=2, level='Easy',
    intro=['An omelette is one of the quickest ways to put protein on a plate, and its soft texture makes it easy to eat on low-appetite mornings. Mixing whole eggs with a little egg white keeps the omelette tender while adding protein, and wilted spinach with a small amount of feta brings color and flavor without making it heavy.',
           'The secret to a soft omelette is gentle heat. Eggs set at fairly low temperatures, so cooking over medium-low heat and stirring early creates small, creamy curds instead of a dry, rubbery sheet. Wilting the spinach first and pressing out its liquid keeps the filling from making the eggs watery.'],
    why=[['About 23 g protein per omelette', 'Two eggs, egg whites and feta on one small plate.'],
         ['Ready in 15 minutes', 'Wilt the spinach, cook the eggs, fold and serve.'],
         ['Soft and mild', 'Gentle heat keeps the eggs tender and easy to eat.']],
    ingredients=[{'group': 'For the filling', 'items': [
        I(1, 'tsp', 'olive oil'), I(2, 'cups', 'baby spinach', g=60), I(0.25, 'cup', 'crumbled feta', g=38)]},
        {'group': 'For the omelettes', 'items': [
        I(4, '', 'large eggs'), I(0.5, 'cup', 'liquid egg whites', g=122), I(None, '', 'salt and black pepper', 'to taste'),
        I(1, 'tsp', 'olive oil', 'for the pan')]},
        {'group': 'To serve', 'items': [I(0.5, 'cup', 'cherry tomatoes', 'halved, optional', 100)]}],
    steps=[S('Wilt the spinach', 'Heat 1 teaspoon oil in an 8-inch nonstick skillet over medium heat. Add the spinach and stir for 1 to 2 minutes, until just wilted. Transfer to a plate, press with a spoon and pour off the liquid. Wipe the pan.'),
           S('Whisk the eggs', 'Whisk the eggs, egg whites and a pinch of salt and pepper for about 30 seconds, until evenly combined and slightly frothy.'),
           S('Cook the first omelette', 'Heat half of the remaining oil in the skillet over medium-low heat. Pour in half of the egg mixture. Stir gently with a spatula for the first 30 seconds, then let it set undisturbed for 1 to 2 minutes, until the edges are set and the top is barely glossy.', 'If the bottom browns before the top sets, lower the heat.'),
           S('Fill and fold', 'Scatter half of the spinach and half of the feta over one side. Fold the omelette over the filling, cook for 30 seconds more and slide it onto a plate.'),
           S('Repeat and serve', 'Repeat with the remaining oil, eggs and filling. Serve with cherry tomatoes and, if you like, a small piece of toast.')],
    tips=['Use an 8-inch nonstick pan for this size of omelette. A larger pan spreads the eggs too thin and they overcook.',
          'Take the omelette off the heat while the top still looks slightly wet. It finishes cooking from its own heat on the plate.',
          'Squeeze the spinach well. Extra liquid makes the omelette watery.',
          'Small-portion tip: eat half the omelette now and refrigerate the rest for later in the day. Half still counts.'],
    storage='Omelettes are best eaten fresh. Leftovers keep in the refrigerator for up to 1 day; reheat gently in the microwave in 20-second bursts, or eat at room temperature. The wilted spinach can be prepared a day ahead and kept in a covered container.',
    variations=[['Mushroom and Swiss', 'Swap the spinach for 1 cup sliced mushrooms, cooked until browned, and use Swiss cheese instead of feta.'],
                ['Dairy-free', 'Leave out the feta and add chopped fresh herbs for flavor.'],
                ['Breakfast wrap', 'Roll the omelette inside a small tortilla for a breakfast you can carry.'],
                ['Make it gentler', 'Skip the tomatoes and cook the eggs a little longer for a firmer, milder texture.'],
                ['Protein boost', 'Whisk 1/4 cup cottage cheese into the egg mixture, or serve with a side of Greek yogurt.']],
    nutrition={'calories': 280, 'protein': 23, 'carbs': 5, 'fat': 18, 'fiber': 1},
    faq=[['Can I use only whole eggs?', 'Yes. Use 3 eggs per omelette instead of 2 eggs plus egg whites. The protein stays similar and the fat and calories go up slightly.'],
         ['Why is my omelette rubbery?', 'The heat was probably too high, or it cooked too long. Use medium-low heat and take it off while the top is still a little glossy.'],
         ['Can I make it ahead?', 'Omelettes are best fresh, but you can wilt the spinach and whisk the eggs the night before. Keep the eggs covered in the fridge and whisk again before cooking.']],
    note='Medium-low heat and an 8-inch pan make the biggest difference here. Two eggs plus a splash of egg whites keeps the omelette soft and filling without a big portion, and it is ready faster than most toast.')

NEW['turkey-meatballs-marinara'] = dict(
    title='Turkey Meatballs in Marinara',
    subtitle='Small, tender turkey meatballs simmered in tomato sauce. Four meatballs per plate, about 26 g protein, with or without pasta.',
    desc='Small turkey meatballs simmered in tomato sauce.',
    category='Main Dishes', tags=['healthy', 'small-plates', 'high-protein', 'make-ahead'], diet=[],
    prep=15, cook=30, time=45, serves=6, level='Easy',
    intro=['Meatballs are a familiar, comforting meal, and small ones are easy to portion: four make a satisfying plate without a mountain of pasta. Lean ground turkey keeps them light, a little Parmesan and garlic keep them flavorful, and simmering them in marinara keeps them moist.',
           'The panko and milk mixture, called a panade, is what keeps lean meatballs tender. The soaked crumbs hold on to moisture and stop the meat proteins from tightening into a dense ball. Browning the meatballs briefly adds flavor, and finishing them in the sauce lets them cook through gently.'],
    why=[['About 26 g protein per plate', 'Four small turkey meatballs in sauce, before any pasta.'],
         ['Tender, not dry', 'A simple panko and milk panade keeps lean turkey moist.'],
         ['Freezes beautifully', 'Freeze cooked meatballs in sauce in small portions for easy dinners.']],
    ingredients=[{'group': 'For the meatballs', 'items': [
        I(1.5, 'lb', 'lean ground turkey', '93% lean', 680), I(0.33, 'cup', 'panko breadcrumbs', g=30), I(2, 'tbsp', 'milk'),
        I(1, '', 'large egg'), I(0.25, 'cup', 'grated Parmesan', g=25), I(2, '', 'garlic cloves', 'minced'),
        I(1, 'tsp', 'dried Italian seasoning'), I(0.75, 'tsp', 'kosher salt'), I(0.25, 'tsp', 'black pepper')]},
        {'group': 'For cooking and serving', 'items': [
        I(1, 'tbsp', 'olive oil'), I(1, 'jar', 'marinara sauce', '24 oz / 680 g; check the label for sodium and added sugar', 680),
        I(None, '', 'fresh parsley or basil', 'chopped, to serve')]}],
    steps=[S('Make the panade', 'In a large bowl, stir together the panko and milk. Let it sit for 5 minutes, until the crumbs are soft.'),
           S('Mix gently', 'Add the turkey, egg, Parmesan, garlic, Italian seasoning, salt and pepper. Mix with your hands or a fork just until evenly combined.', 'Overmixing makes dense meatballs. Stop as soon as you no longer see streaks of crumbs.'),
           S('Shape small meatballs', 'With damp hands, roll the mixture into 1 1/2-inch balls, about 1 1/2 tablespoons each. You should have about 24.'),
           S('Brown', 'Heat the oil in a large, deep skillet over medium-high heat. Brown the meatballs in batches for 3 to 4 minutes, turning, until golden on a few sides. They do not need to be cooked through yet.'),
           S('Simmer in the sauce', 'Pour off any excess fat and return all the meatballs to the pan. Add the marinara, bring to a gentle simmer, cover and cook for 15 to 20 minutes, until the meatballs reach 165°F (74°C) in the center.'),
           S('Serve small', 'Serve four meatballs with sauce per plate, topped with fresh herbs. Add a small scoop of pasta, zucchini noodles or a piece of bread if you like.')],
    tips=['Wet your hands with cold water before rolling. The mixture will not stick and the meatballs stay round.',
          'Use a thermometer. Ground poultry is safe at 165°F (74°C), and pulling it right at that point keeps it juicy.',
          'Look for a marinara with simple ingredients and less added sugar; brands vary a lot in sodium.',
          SMALL_TIP],
    storage='Refrigerate the meatballs in sauce in airtight containers for up to 4 days. Freeze in single portions for up to 3 months; thaw overnight in the fridge and reheat gently in a covered saucepan until steaming.',
    variations=[['Gluten-free', 'Use gluten-free breadcrumbs or 1/3 cup quick oats, and check the marinara label.'],
                ['Baked meatballs', 'Skip browning and bake on a parchment-lined sheet at 400°F (200°C) for 15 minutes, then simmer in the sauce for 10 minutes.'],
                ['Spinach meatballs', 'Add 1 cup finely chopped baby spinach to the mixture.'],
                ['Make it gentler', 'Use a mild marinara, skip the extra garlic and break the meatballs into smaller pieces in the sauce.'],
                ['Protein boost', 'Serve over a few spoonfuls of white beans, or top with a spoonful of ricotta.']],
    nutrition={'calories': 305, 'protein': 26, 'carbs': 15, 'fat': 16, 'fiber': 2},
    faq=[['Can I use ground chicken?', 'Yes. Ground chicken works the same way. Choose a lean blend and cook to 165°F (74°C).'],
         ['Why did my meatballs fall apart?', 'The mixture may have been too wet, or the meatballs were moved too soon. Chill the shaped meatballs for 10 minutes and let them brown before turning.'],
         ['How many meatballs is a serving?', 'Four small meatballs with sauce. On hungrier days add a fifth, or a small scoop of pasta.']],
    note='Keeping the meatballs small is what makes this a small plate: four is a satisfying portion, and they reheat quickly. Make a full batch on a good day and freeze them in sauce, two or three portions at a time.')

NEW['turkey-bean-chili'] = dict(
    title='Turkey and Bean Chili',
    subtitle='A mild, hearty chili with lean turkey, beans and sweet corn, finished with Greek yogurt instead of sour cream. About 26 g protein in a small bowl.',
    desc='Mild turkey chili with beans, corn and yogurt.',
    category='Soups', tags=['healthy', 'small-plates', 'high-protein', 'make-ahead'], diet=['gluten-free'],
    prep=15, cook=40, time=55, serves=6, level='Easy',
    intro=['Chili tastes even better after a day in the fridge, which makes it perfect for cooking once and eating in small bowls all week. This version uses lean ground turkey, two cans of beans and sweet corn, with a mild spice blend you can turn up or down. A spoonful of Greek yogurt on top replaces sour cream and adds protein.',
           'Blooming the spices in the pan with the browned turkey releases their fat-soluble flavors, so the chili tastes deep after only half an hour of simmering. The beans do double duty: they add protein and fiber, and some of their starch thickens the pot as it cooks.'],
    why=[['About 26 g protein per bowl', 'Lean turkey, beans and a spoonful of Greek yogurt.'],
         ['Mild by default', 'Easy to adjust: add heat at the table rather than in the pot.'],
         ['Even better tomorrow', 'The flavors deepen overnight, and it freezes in single portions.']],
    ingredients=[{'group': 'For the chili', 'items': [
        I(1, 'tbsp', 'olive oil'), I(1, 'lb', 'lean ground turkey', '93% lean', 454), I(1, '', 'yellow onion', 'diced'),
        I(1, '', 'bell pepper', 'diced'), I(3, '', 'garlic cloves', 'minced'), I(2, 'tbsp', 'mild chili powder', 'check the label if you need it gluten-free'),
        I(1, 'tsp', 'ground cumin'), I(1, 'tsp', 'smoked paprika'), I(1, 'can', 'diced tomatoes', '14.5 oz / 411 g'),
        I(2, 'cans', 'kidney or pinto beans', '15 oz / 425 g each, drained and rinsed'), I(1, 'cup', 'frozen corn', g=145),
        I(1.5, 'cups', 'low-sodium chicken broth'), I(0.75, 'tsp', 'kosher salt', 'plus more to taste')]},
        {'group': 'To serve', 'items': [
        I(0.75, 'cup', 'plain nonfat Greek yogurt', g=170), I(None, '', 'cilantro or scallions', 'chopped')]}],
    steps=[S('Brown the turkey', 'Heat the oil in a large pot or Dutch oven over medium-high heat. Add the turkey and cook for 5 to 6 minutes, breaking it up, until no pink remains and some bits are browned.'),
           S('Soften the vegetables', 'Add the onion and bell pepper with a pinch of salt and cook for about 5 minutes, until softened. Stir in the garlic for 1 minute.'),
           S('Bloom the spices', 'Stir in the chili powder, cumin and smoked paprika and cook for 1 minute, until fragrant and coating the meat.', 'Keep everything moving so the spices do not scorch.'),
           S('Simmer', 'Add the tomatoes with their juices, the beans, corn, broth and salt. Bring to a boil, then lower to a gentle simmer, partially cover and cook for 25 to 30 minutes, stirring now and then, until thickened.'),
           S('Season and serve', 'Taste and adjust the salt. Ladle into 1-cup bowls and top each with a spoonful of Greek yogurt and some herbs.')],
    tips=['Chili powder blends vary in heat. Start with a mild one and pass hot sauce at the table.',
          'If the chili gets too thick, add broth 1/4 cup at a time; if it is too thin, simmer uncovered for a few more minutes.',
          'Mash a few spoonfuls of beans against the side of the pot to thicken the chili without flour.',
          SMALL_TIP],
    storage='Refrigerate in airtight containers for up to 4 days, or freeze in 1-cup portions for up to 3 months. Reheat in a saucepan over medium heat, stirring, until steaming, adding a splash of broth if needed. Add the yogurt after reheating.',
    variations=[['Vegetarian', 'Skip the turkey, add a third can of beans and use vegetable broth.'],
                ['Chicken chili', 'Use 1 lb shredded cooked chicken instead of ground turkey, stirred in with the beans.'],
                ['Dairy-free', 'Top with sliced avocado instead of Greek yogurt.'],
                ['Make it gentler', 'Use half the chili powder, skip the smoked paprika and let the bowl cool slightly before eating.'],
                ['Protein boost', 'Add an extra spoonful of Greek yogurt, or a sprinkle of shredded cheese.']],
    nutrition={'calories': 310, 'protein': 26, 'carbs': 32, 'fat': 10, 'fiber': 8},
    faq=[['Is this chili spicy?', 'Not as written. Mild chili powder gives warmth without much heat. Add cayenne or hot sauce if you like it spicier.'],
         ['Can I make it in a slow cooker?', 'Yes. Brown the turkey and vegetables and bloom the spices on the stove, then transfer everything to a slow cooker and cook on low for 6 hours.'],
         ['Can I use dried beans?', 'Yes. Use about 3 cups of cooked beans in place of the two cans.']],
    note='This is a good pot to make on a Sunday. Portion it into 1-cup containers as soon as it cools, and you have a warm, high-protein small meal ready for the week. Add the yogurt only after reheating so it stays cool and creamy.')

NEW['lemon-herb-baked-cod'] = dict(
    title='Lemon Herb Baked Cod',
    subtitle='Mild, flaky cod baked with olive oil, garlic, lemon and fresh herbs. Four-ounce portions, about 20 g protein, ready in about 20 minutes.',
    desc='Mild, flaky cod with lemon and herbs.',
    category='Main Dishes', tags=['healthy', 'quick', 'small-plates', 'high-protein', 'gentle'], diet=['gluten-free', 'dairy-free'],
    prep=10, cook=12, time=22, serves=4, level='Easy',
    intro=['White fish like cod is one of the gentlest proteins to cook and eat: it is mild, soft and flakes apart easily. Baking it with a little olive oil, lemon and fresh herbs keeps the flavor bright without anything heavy, and four-ounce portions are just right for a small plate.',
           'Cod is lean, so it cooks quickly and can dry out if it goes too long. A hot oven, a light coating of oil and pulling the fish as soon as it flakes keep it moist. Adding the lemon juice after baking keeps its flavor fresh, since heat dulls citrus aromas.'],
    why=[['About 20 g protein per portion', 'A 4 oz piece of cod, with very little fat.'],
         ['Mild and gentle', 'Soft, flaky fish with a light lemon flavor and little lingering smell.'],
         ['Ready in about 20 minutes', 'One pan, no flipping, minimal cleanup.']],
    ingredients=[{'group': 'For the cod', 'items': [
        I(1, 'lb', 'cod fillets', 'cut into 4 portions, about 4 oz / 113 g each', 454), I(1, 'tbsp', 'olive oil'),
        I(2, '', 'garlic cloves', 'minced'), I(0.5, 'tsp', 'sweet paprika'), I(0.5, 'tsp', 'kosher salt'), I(0.25, 'tsp', 'black pepper')]},
        {'group': 'To finish', 'items': [
        I(1, '', 'lemon', 'zest and juice, plus slices to serve'), I(2, 'tbsp', 'fresh parsley or dill', 'chopped')]}],
    steps=[S('Heat the oven', 'Heat the oven to 400°F (200°C) and line a baking dish or sheet pan with parchment.'),
           S('Season the fish', 'Pat the cod very dry and place the pieces in the pan with space between them. Mix the oil, garlic, paprika, salt, pepper and lemon zest, and brush it over the fish.'),
           S('Bake', 'Bake for 10 to 12 minutes, until the fish is opaque and flakes easily with a fork. The thickest part should read 145°F (63°C).', 'Thin pieces cook faster. Start checking at 8 minutes.'),
           S('Finish and serve', 'Squeeze lemon juice over the fish and scatter the herbs. Serve one piece per plate with lemon slices, and a small scoop of rice or steamed vegetables if you like.')],
    tips=['Pat the fish dry so the seasoning sticks and the surface does not steam.',
          'Frozen cod works well. Thaw it overnight in the fridge and dry it thoroughly before baking.',
          'Tuck thin tail ends under so each piece is an even thickness and cooks at the same rate.',
          SMALL_TIP],
    storage='Refrigerate leftovers in an airtight container for up to 2 days. Reheat gently, covered, at 275°F (135°C) for about 10 minutes, or flake cold leftovers into a salad or a small bowl of rice.',
    variations=[['Parmesan crumb topping', 'Mix 2 tbsp panko with 1 tbsp grated Parmesan and sprinkle over the fish before baking. This adds gluten and dairy.'],
                ['Other white fish', 'Haddock, pollock or tilapia work the same way; adjust the time to the thickness of the fillets.'],
                ['Sheet-pan dinner', 'Roast green beans or asparagus around the fish in the same pan.'],
                ['Make it gentler', 'Skip the garlic and paprika, use only a little lemon and serve at room temperature.'],
                ['Protein boost', 'Serve with a spoonful of Greek yogurt mixed with lemon and dill, or over a few spoonfuls of white beans.']],
    nutrition={'calories': 125, 'protein': 20, 'carbs': 1, 'fat': 4, 'fiber': 0},
    faq=[['How do I know when cod is done?', 'It turns from translucent to opaque and separates into flakes when pressed with a fork. The thickest part should reach 145°F (63°C).'],
         ['Why is my cod watery?', 'Frozen fish releases water as it bakes. Thaw it fully and pat it very dry before seasoning.'],
         ['What can I serve with it?', 'A small scoop of rice, a few roasted vegetables or a simple green salad. The photo shows it with rice, which is not included in the nutrition estimate.']],
    note='Cod is one of the easiest proteins to eat on a harder day: mild, soft and quick to cook. Keep a bag of frozen fillets in the freezer, thaw one overnight, and you have a small, high-protein dinner in about 20 minutes.')

NEW['chicken-congee'] = dict(
    title='Ginger Chicken Congee',
    subtitle='Silky rice porridge simmered in broth with ginger and shredded chicken, topped with scallions. Soft, warm and about 22 g protein per bowl.',
    desc='Silky rice porridge with ginger and chicken.',
    category='Soups', tags=['healthy', 'small-plates', 'high-protein', 'gentle', 'make-ahead'], diet=['dairy-free'],
    prep=10, cook=60, time=70, serves=6, level='Easy',
    intro=['Congee is a rice porridge eaten across East and Southeast Asia, often as a comforting breakfast or when someone is feeling unwell. It is soft, warm and gently seasoned, which makes it one of the easiest things to eat when your appetite is small. This version poaches chicken breast right in the pot, so each bowl carries about 22 g of protein.',
           'A small amount of rice goes a long way. Simmered in plenty of broth, the grains break down and release their starch, turning the liquid into a silky porridge. Poaching the chicken gently in the same pot flavors the broth and keeps the meat tender enough to shred with a fork.'],
    why=[['About 22 g protein per bowl', 'Chicken breast poached in the porridge and shredded back in.'],
         ['Soft and soothing', 'A mild ginger broth and a smooth texture that is easy to eat.'],
         ['Makes six bowls', 'Reheats well with a splash of broth for the days ahead.']],
    ingredients=[{'group': 'For the congee', 'items': [
        I(0.75, 'cup', 'jasmine rice', 'rinsed', 140), I(8, 'cups', 'low-sodium chicken broth'), I(2, 'cups', 'water'),
        I(1, 'inch', 'fresh ginger', 'thinly sliced'), I(1, 'lb', 'boneless, skinless chicken breasts', g=454),
        I(0.5, 'tsp', 'kosher salt', 'plus more to taste')]},
        {'group': 'To serve', 'items': [
        I(3, '', 'scallions', 'thinly sliced'), I(1, 'tbsp', 'low-sodium soy sauce or tamari'), I(1, 'tsp', 'toasted sesame oil')]}],
    steps=[S('Rinse the rice', 'Rinse the rice in a sieve under cold running water for about 30 seconds, until the water runs mostly clear.'),
           S('Simmer the base', 'Combine the rice, broth, water and ginger in a large pot. Bring to a boil over high heat, then lower to a gentle simmer, partially cover and cook for 30 minutes, stirring every 10 minutes.', 'Scrape along the bottom when you stir. Rice settles and can stick as the porridge thickens.'),
           S('Poach the chicken', 'Add the whole chicken breasts and the salt. Simmer gently for 15 to 20 minutes, until the chicken reaches 165°F (74°C) and the rice has broken down into a thick porridge.'),
           S('Shred and return', 'Lift out the chicken and shred it finely with two forks. Remove the ginger slices if you like, then stir the chicken back in. If the congee is too thick, stir in hot broth or water.'),
           S('Serve', 'Ladle into 1-cup bowls and top with scallions, a few drops of soy sauce and a little sesame oil.')],
    tips=['Jasmine rice breaks down quickly and gives a silky texture, but any long-grain white rice works.',
          'Congee thickens as it sits. Stir in hot broth or water a little at a time until it is as loose as you like.',
          'For an extra-smooth porridge, use an immersion blender for a few seconds before adding the chicken back.',
          SMALL_TIP],
    storage='Refrigerate in airtight containers for up to 4 days. It sets firm in the fridge; reheat in a saucepan over medium-low heat with a splash of broth or water, stirring until smooth and steaming. Freeze in single portions for up to 2 months.',
    variations=[['Turkey congee', 'Use shredded leftover roast turkey, stirred in for the last 5 minutes.'],
                ['Egg drop congee', 'Drizzle a beaten egg into the simmering congee and stir gently until set.'],
                ['Gluten-free', 'Use tamari instead of soy sauce and check the broth label.'],
                ['Make it gentler', 'Skip the soy sauce and sesame oil, serve it warm rather than hot and keep the toppings simple.'],
                ['Protein boost', 'Top each bowl with a soft-boiled egg, or stir in a little extra shredded chicken.']],
    nutrition={'calories': 205, 'protein': 22, 'carbs': 20, 'fat': 4, 'fiber': 0},
    faq=[['Can I make it in a slow cooker or pressure cooker?', 'Yes. In a slow cooker, cook everything except the toppings on low for 6 to 7 hours. In a pressure cooker, cook the rice, broth, water, ginger and chicken for 20 minutes at high pressure and let the pressure release naturally.'],
         ['Why is my congee too thick?', 'Rice keeps absorbing liquid as it sits. Stir in hot broth or water until it loosens.'],
         ['Is congee only for breakfast?', 'Not at all. It is eaten at any time of day and makes a light, warm lunch or dinner.']],
    note='Congee is a quiet, comforting meal that asks very little of you once it is on the stove. Keep the toppings simple on harder days, and loosen each portion with a little broth when you reheat it.')

NEW['southwest-chicken-salad-bowl'] = dict(
    title='Southwest Chicken Salad Bowl',
    subtitle='Seasoned chicken, black beans, corn and crisp vegetables with a creamy Greek yogurt lime dressing and a few crunchy tortilla strips. About 36 g protein per bowl.',
    desc='Chicken, beans and corn with a creamy lime dressing.',
    category='Salads', tags=['healthy', 'small-plates', 'high-protein', 'make-ahead'], diet=['gluten-free'],
    prep=15, cook=15, time=30, serves=4, level='Easy',
    intro=['A colorful salad bowl is an easy way to fit a lot of protein into a lunch you actually want to eat. This one combines seasoned chicken breast and black beans with sweet corn, tomatoes and cucumber, all tossed with a creamy dressing made from Greek yogurt and lime instead of mayonnaise or ranch.',
           'Texture keeps a salad interesting. A small handful of crushed tortilla chips adds crunch without much bulk, while the cool, tangy dressing ties everything together. Cooking the chicken in a hot pan with a quick spice rub gives it flavor in about 12 minutes.'],
    why=[['About 36 g protein per bowl', 'Chicken breast, black beans and a Greek yogurt dressing.'],
         ['Creamy without mayo', 'Greek yogurt, lime and a touch of honey make a light, tangy dressing.'],
         ['Lunch for the week', 'Store the components separately and assemble a bowl in minutes.']],
    ingredients=[{'group': 'For the chicken', 'items': [
        I(1, 'lb', 'boneless, skinless chicken breasts', g=454), I(1, 'tbsp', 'olive oil'), I(1, 'tsp', 'chili powder'),
        I(0.5, 'tsp', 'ground cumin'), I(0.5, 'tsp', 'kosher salt')]},
        {'group': 'For the bowls', 'items': [
        I(4, 'cups', 'chopped romaine', g=188), I(1, 'can', 'black beans', '15 oz / 425 g, drained and rinsed'),
        I(1, 'cup', 'corn', 'thawed if frozen', 145), I(1, 'cup', 'cherry tomatoes', 'halved', 150), I(1, '', 'English cucumber', 'diced'),
        I(0.5, 'cup', 'crushed tortilla chips', 'check the label if you need them gluten-free', 20), I(None, '', 'fresh cilantro', 'chopped')]},
        {'group': 'For the dressing', 'items': [
        I(0.5, 'cup', 'plain nonfat Greek yogurt', g=120), I(2, 'tbsp', 'fresh lime juice'), I(1, 'tsp', 'honey'),
        I(1, 'tbsp', 'water'), I(None, '', 'salt', 'to taste')]}],
    steps=[S('Season the chicken', 'Pat the chicken dry and pound the thicker end to an even 3/4 inch. Rub with the oil, then season both sides with the chili powder, cumin and salt.'),
           S('Cook', 'Heat a skillet over medium-high heat. Cook the chicken for 5 to 6 minutes per side, until it reaches 165°F (74°C). Rest for 5 minutes, then slice thinly or chop.', 'Resting lets the juices settle back into the meat, so it stays moist when sliced.'),
           S('Make the dressing', 'Whisk the yogurt, lime juice, honey, water and a pinch of salt until smooth and pourable.'),
           S('Build the bowls', 'Divide the romaine among four bowls. Top with the beans, corn, tomatoes, cucumber and chicken. Drizzle with the dressing and finish with tortilla chips and cilantro just before eating.')],
    tips=['Rinse the black beans well. It removes the starchy liquid and some of the sodium.',
          'Add the tortilla chips at the last minute so they stay crunchy.',
          'If you are packing lunches, keep the dressing in a small separate jar.',
          SMALL_TIP],
    storage='Store the cooked chicken, beans and corn, chopped vegetables and dressing in separate airtight containers in the fridge for up to 3 days. Keep the tortilla chips at room temperature. Assemble the bowls just before eating.',
    variations=[['Use rotisserie chicken', 'Skip cooking and use 3 cups shredded rotisserie chicken.'],
                ['Add avocado', 'Top each bowl with a few slices of avocado.'],
                ['Vegetarian', 'Replace the chicken with a second can of beans or a cup of shelled edamame.'],
                ['Make it gentler', 'Use a milder lettuce, skip the chili powder and tortilla chips, and go light on the lime.'],
                ['Protein boost', 'Add a soft-boiled egg or a sprinkle of shredded cheese to each bowl.']],
    nutrition={'calories': 345, 'protein': 36, 'carbs': 32, 'fat': 9, 'fiber': 7},
    faq=[['Can I make the dressing ahead?', 'Yes. It keeps in a sealed jar in the fridge for up to 3 days. Stir before using and add a few drops of water if it thickens.'],
         ['Can I use canned corn?', 'Yes. Drain and rinse it. Frozen corn just needs to thaw; you can also char it in a dry skillet for extra flavor.'],
         ['How do I keep the salad from getting soggy?', 'Store the dressing and chips separately and toss everything together just before eating.']],
    note='Prepping the chicken, beans and dressing once gives you several quick lunches. A full bowl is generous, so on smaller-appetite days serve half and keep the rest of the components for the next day.')

NEW['blackberry-yogurt-parfait'] = dict(
    title='Blackberry Greek Yogurt Parfait',
    subtitle='Layers of vanilla Greek yogurt, juicy blackberries and a little granola in a glass. Cold, creamy and about 20 g protein.',
    desc='Layered yogurt, blackberries and granola.',
    category='Snacks', tags=['healthy', 'quick', 'small-plates', 'high-protein', 'gentle'], diet=['vegetarian'],
    prep=5, cook=0, time=5, serves=2, level='Easy',
    intro=['A yogurt parfait is one of the simplest ways to eat a high-protein snack or breakfast without cooking. It is cold, smooth and easy to eat in small spoonfuls, which helps on mornings when warm food does not sound good. Each glass has about 20 g of protein, mostly from plain Greek yogurt.',
           'Layering keeps every spoonful balanced. A little honey and vanilla stirred into the yogurt softens its tang, the blackberries add juicy sweetness, and a small amount of granola goes on last so it stays crunchy.'],
    why=[['About 20 g protein per glass', 'Three-quarters of a cup of Greek yogurt in each parfait.'],
         ['No cooking', 'Five minutes from fridge to spoon.'],
         ['Cold and gentle', 'Smooth, cool layers that are easy to eat in small amounts.']],
    ingredients=[{'group': 'For the yogurt', 'items': [
        I(1.5, 'cups', 'plain nonfat Greek yogurt', g=340), I(2, 'tsp', 'honey', 'or maple syrup'), I(0.5, 'tsp', 'vanilla extract')]},
        {'group': 'For the layers', 'items': [
        I(1, 'cup', 'fresh blackberries', 'or frozen and thawed', 144), I(0.25, 'cup', 'granola', g=30)]}],
    steps=[S('Flavor the yogurt', 'Stir the yogurt, honey and vanilla together until smooth.'),
           S('Layer', 'Spoon a layer of yogurt into two glasses or small jars, then add a layer of blackberries. Repeat, ending with yogurt.'),
           S('Top and serve', 'Sprinkle the granola and a few berries on top just before eating.')],
    tips=['Add the granola right before serving so it stays crunchy.',
          'If your blackberries are tart, lightly crush half of them with a fork and a few drops of honey to make a quick sauce.',
          'Choose a granola with less added sugar, or use a few chopped nuts instead.',
          'Small-portion tip: make the parfaits in small jars and eat half now and half later. A half jar still counts.'],
    storage='Assemble the yogurt and berries up to 1 day ahead and refrigerate, covered. Add the granola just before eating.',
    variations=[['Mixed berry', 'Use any berries you like: raspberries, blueberries and sliced strawberries all work.'],
                ['Peanut butter crunch', 'Swirl 1 tsp peanut butter into each layer of yogurt and top with chopped peanuts.'],
                ['Dairy-free', 'Use a high-protein plant yogurt; check the label, since protein content varies a lot.'],
                ['Make it gentler', 'Skip the granola and use soft, ripe berries or a spoonful of applesauce.'],
                ['Protein boost', 'Stir 1/4 cup cottage cheese into the yogurt, or use a higher-protein yogurt.']],
    nutrition={'calories': 225, 'protein': 20, 'carbs': 28, 'fat': 4, 'fiber': 5},
    faq=[['Can I use flavored yogurt?', 'Yes, but flavored yogurts often have more added sugar and sometimes less protein. Plain Greek yogurt with a little honey gives you more control.'],
         ['Can I use frozen blackberries?', 'Yes. Thaw them in the fridge overnight or for a few minutes in the microwave, and use their juice as a sauce.'],
         ['Is this a breakfast or a snack?', 'Either. One glass makes a light breakfast or a filling snack between small meals.']],
    note='This is one of the easiest protein-first snacks on the site: no stove, no smells and ready in five minutes. Keep the granola separate until the last minute so every spoonful has a little crunch.')

NEW['peanut-butter-oat-bites'] = dict(
    title='Peanut Butter Oat Protein Bites',
    subtitle='No-bake bites made with rolled oats, peanut butter, honey, chia seeds and a scoop of protein powder. Two bites make a snack with about 9 g protein.',
    desc='No-bake snack bites; two make a snack.',
    category='Snacks', tags=['healthy', 'small-plates', 'make-ahead'], diet=['vegetarian'],
    prep=15, cook=0, chill=30, time=45, serves=16, servesLabel='bites', level='Easy',
    intro=['Small snacks between small meals are a practical way to keep eating on low-appetite days, and it helps when they are already made. These no-bake bites take about 15 minutes to roll, keep for a week in the fridge, and two of them make a snack with about 9 g of protein.',
           'Peanut butter and honey hold the oats together, so there is nothing to bake. A short chill firms the mixture enough to roll neatly, and the chia seeds add a little extra fiber. Protein powder boosts the protein; if you prefer not to use it, nonfat dry milk powder works in its place.'],
    why=[['About 9 g protein per two bites', 'Peanut butter, oats and a scoop of protein powder.'],
         ['No baking', 'Stir, chill and roll, with about 15 minutes of hands-on time.'],
         ['Ready all week', 'Keeps in the fridge for a week and in the freezer for three months.']],
    ingredients=[{'group': 'For the bites', 'items': [
        I(1, 'cup', 'old-fashioned rolled oats', 'use certified gluten-free oats if needed', 90),
        I(0.5, 'cup', 'creamy natural peanut butter', g=128), I(0.25, 'cup', 'honey', g=84),
        I(1, 'scoop', 'vanilla protein powder', 'about 30 g, or 1/3 cup nonfat dry milk powder', 30),
        I(2, 'tbsp', 'chia seeds', g=24), I(1, 'tsp', 'vanilla extract'), I(1, 'pinch', 'fine salt')]}],
    steps=[S('Mix', 'In a medium bowl, stir the peanut butter, honey, vanilla and salt until smooth. Add the oats, protein powder and chia seeds and stir until evenly combined.', 'If the mixture is too dry, add milk 1 tablespoon at a time. If it is too sticky, add a tablespoon of oats.'),
           S('Chill', 'Cover and refrigerate for 30 minutes, until firm enough to roll.'),
           S('Roll', 'Scoop level tablespoons of the mixture and roll them between your palms into 16 bites.', 'Slightly damp hands keep the mixture from sticking.'),
           S('Store', 'Transfer the bites to an airtight container and keep them in the fridge.')],
    tips=['Use a drippy natural peanut butter. Very stiff peanut butter makes a crumbly mixture.',
          'Protein powders absorb liquid differently. Adjust with a little milk or extra oats until the mixture holds together when pressed.',
          'A small cookie scoop makes even bites quickly.',
          'Small-portion tip: start with one bite. Two bites make a full snack.'],
    storage='Refrigerate in an airtight container for up to 1 week, or freeze for up to 3 months. Eat straight from the fridge, or let frozen bites sit for 10 minutes before eating.',
    variations=[['Chocolate chip', 'Fold in 2 tbsp mini dark chocolate chips.'],
                ['Nut-free', 'Use sunflower seed butter and check that your protein powder is made in a nut-free facility.'],
                ['No protein powder', 'Use 1/3 cup nonfat dry milk powder instead; each bite will have slightly less protein.'],
                ['Make it gentler', 'Roll smaller bites and skip any chocolate or dried fruit add-ins.'],
                ['Protein boost', 'Serve two bites with a glass of milk or a small cup of Greek yogurt.']],
    nutrition={'calories': 100, 'protein': 5, 'carbs': 11, 'fat': 5, 'fiber': 2},
    faq=[['Can I make these without honey?', 'Yes. Maple syrup works the same way.'],
         ['Why will my mixture not stick together?', 'It is probably too dry. Add milk or a little more peanut butter, a tablespoon at a time.'],
         ['Are these gluten-free?', 'They are if you use certified gluten-free oats and a gluten-free protein powder.']],
    note='These are worth keeping in the fridge for the days when a meal feels like too much. Two bites and a glass of milk is a small, steady snack, and the batch lasts all week.')

NEW['cinnamon-baked-apples-pears'] = dict(
    title='Cinnamon Baked Apples and Pears',
    subtitle='Soft, warm apple and pear slices baked with cinnamon and a little maple, topped with walnuts and served with Greek yogurt. A gentle dessert with about 8 g protein.',
    desc='Warm cinnamon fruit with walnuts and yogurt.',
    category='Snacks', tags=['healthy', 'small-plates', 'gentle', 'make-ahead'], diet=['vegetarian', 'gluten-free'],
    prep=10, cook=30, time=40, serves=4, level='Easy',
    intro=['Baked fruit is a cozy, gentle dessert that feels like apple crisp without the heavy topping. Wedges of apple and pear bake until soft and fragrant with cinnamon, then get a spoonful of Greek yogurt and a few walnuts for protein and crunch.',
           'Baking concentrates the fruit\u2019s natural sweetness as some of its water evaporates, so only a tablespoon of maple syrup is needed for the whole pan. A little melted butter helps the cinnamon cling and the edges caramelize. Serving it warm with cool yogurt makes a nice contrast.'],
    why=[['Soft and warm', 'Tender baked fruit that is easy to eat on harder days.'],
         ['Lightly sweetened', 'Just one tablespoon of maple syrup for the whole pan.'],
         ['About 8 g protein per serving', 'A spoonful of Greek yogurt and a few walnuts on top.']],
    ingredients=[{'group': 'For the fruit', 'items': [
        I(2, '', 'medium apples', 'cored and cut into wedges', 360), I(2, '', 'ripe but firm pears', 'cored and cut into wedges', 356),
        I(1, 'tbsp', 'butter', 'melted'), I(1, 'tbsp', 'maple syrup'), I(1, 'tsp', 'ground cinnamon'), I(1, 'pinch', 'salt')]},
        {'group': 'To serve', 'items': [
        I(0.25, 'cup', 'chopped walnuts', g=30), I(1, 'cup', 'plain nonfat Greek yogurt', g=240)]}],
    steps=[S('Heat the oven', 'Heat the oven to 375°F (190°C).'),
           S('Toss the fruit', 'In a baking dish, toss the apple and pear wedges with the melted butter, maple syrup, cinnamon and salt. Spread them in a single layer.'),
           S('Bake', 'Bake for 25 to 30 minutes, stirring halfway, until the fruit is tender when pierced and the juices bubble. Toast the walnuts on a small tray in the oven for the last 5 minutes.', 'Firmer apples need the full time; check pears a few minutes early.'),
           S('Serve', 'Divide the fruit among four small bowls, add 1/4 cup yogurt to each, scatter the walnuts on top and spoon over the pan juices.')],
    tips=['Use firm baking apples such as Honeycrisp, Gala or Granny Smith so the wedges hold their shape.',
          'Ripe but firm pears work best; very soft pears turn into sauce.',
          'Let the fruit cool for a few minutes before adding the yogurt so it stays creamy.',
          SMALL_TIP],
    storage='Refrigerate the baked fruit in an airtight container for up to 4 days. Warm it gently in the microwave or eat it cold, and add the yogurt and walnuts just before serving.',
    variations=[['Oat crumble topping', 'Sprinkle 1/4 cup rolled oats mixed with 1 tsp melted butter and a pinch of cinnamon over the fruit before baking.'],
                ['Dairy-free', 'Use coconut oil instead of butter and a plant-based yogurt.'],
                ['Spiced pears', 'Use 4 pears and add a pinch of ground ginger and cardamom.'],
                ['Make it gentler', 'Skip the walnuts and bake the fruit a few minutes longer until very soft.'],
                ['Protein boost', 'Use a larger spoonful of Greek yogurt, or stir 1/4 cup cottage cheese into the yogurt.']],
    nutrition={'calories': 220, 'protein': 8, 'carbs': 32, 'fat': 8, 'fiber': 5},
    faq=[['Do I need to peel the fruit?', 'No. The peel softens as it bakes and adds fiber. Peel it if you prefer a softer texture.'],
         ['Can I use only apples?', 'Yes. Use 4 apples, and expect them to take a few minutes longer than pears.'],
         ['Can I make it ahead?', 'Yes. Bake the fruit up to 4 days ahead and warm it gently before serving.']],
    note='Warm fruit and cool yogurt is a simple, comforting end to a small meal. It reheats well, so a batch on Sunday covers a few desserts during the week.')

assert set(NEW) == set(MAP.values()) == set(PHOTOS)

# ------------------------------------------------------------------ images (in memory first)
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'])
    from PIL import Image, ImageDraw, ImageFont


def crop(im, ratio, fy=0.5):
    w, h = im.size
    if w / h > ratio:
        nw = round(h * ratio)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = round(w / ratio)
    y = int((h - nh) * fy)
    return im.crop((0, y, w, y + nh))


def webp_under(im, limit=195 * 1024):
    for q in (80, 74, 68, 62, 56, 50):
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=q, method=6)
        if buf.tell() <= limit:
            return buf.getvalue()
    raise RuntimeError('image still over the size budget')


def jpg(im, q=82):
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return buf.getvalue()


def font(size, serif=True):
    cands = []
    fdir = os.path.join(ROOT, 'fonts')
    if os.path.isdir(fdir):
        pat = '*raunces*' if serif else '*nter*'
        cands += sorted(glob.glob(os.path.join(fdir, pat)))
    cands += ['/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if serif else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for c in cands:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def pin(im, title):
    canvas = Image.new('RGB', (1000, 1500), (247, 242, 231))
    canvas.paste(crop(im, 1000 / 1060).resize((1000, 1060), Image.LANCZOS), (0, 0))
    d = ImageDraw.Draw(canvas)
    green = (63, 81, 48)
    small = font(26, serif=False)
    label = 'SMALL PLATES \u00b7 BIG PROTEIN'
    d.text(((1000 - d.textlength(label, font=small)) / 2, 1100), label, font=small, fill=green)
    size = 68
    while True:
        f = font(size)
        words, lines, cur = title.split(), [], ''
        for wd in words:
            t = (cur + ' ' + wd).strip()
            if d.textlength(t, font=f) <= 880:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        lines.append(cur)
        if len(lines) <= 3 or size <= 44:
            break
        size -= 6
    y = 1160
    for line in lines:
        d.text(((1000 - d.textlength(line, font=f)) / 2, y), line, font=f, fill=green)
        y += int(size * 1.2)
    brand = 'Bored of Toast'
    bf = font(30)
    d.text(((1000 - d.textlength(brand, font=bf)) / 2, 1430), brand, font=bf, fill=green)
    return canvas


files = {}
for rid, (pid, *_rest) in PHOTOS.items():
    url = f'https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=2400'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (bored-of-toast site build)'})
    try:
        data = urllib.request.urlopen(req, timeout=90).read()
        im = Image.open(io.BytesIO(data)).convert('RGB')
        files[f'images/{rid}.webp'] = webp_under(crop(im, 4 / 3).resize((1200, 900), Image.LANCZOS))
        files[f'images/og/{rid}.jpg'] = jpg(crop(im, 1200 / 630).resize((1200, 630), Image.LANCZOS))
        files[f'images/pins/{rid}.jpg'] = jpg(pin(im, NEW[rid]['title']))
    except Exception as ex:
        sys.exit(f'ERROR: could not prepare the photo for {rid} ({ex}). Nothing was saved.')
    print(f'- photo ready: {rid} ({len(files[f"images/{rid}.webp"]) // 1024} KB)')

# ------------------------------------------------------------------ recipes.json
for i, r in enumerate(recipes):
    if r['id'] in MAP:
        nid = MAP[r['id']]
        new = {'id': nid, **NEW[nid], 'img': f'images/{nid}.webp'}
        recipes[i] = new
step_imgs = {s['img'] for r in recipes for s in r.get('steps', []) if s.get('img')}

# ------------------------------------------------------------------ write images, remove old ones
for rel, blob in files.items():
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'wb').write(blob)
removed_keys = set()
for old in MAP:
    for f in [os.path.join(IMG, f'{old}.webp'), os.path.join(IMG, 'og', f'{old}.jpg'), os.path.join(IMG, 'pins', f'{old}.jpg')] + glob.glob(os.path.join(IMG, f'{old}-*w.webp')):
        if os.path.exists(f):
            os.remove(f)
    removed_keys.add(old)
for f in glob.glob(os.path.join(IMG, 'step-*.webp')):
    name = os.path.basename(f)
    base = re.sub(r'-\d+w\.webp$', '.webp', name)
    if f'images/{base}' not in step_imgs:
        os.remove(f)
        removed_keys.add(base[:-5])
subprocess.check_call([sys.executable, P('make_images.py')])

# ------------------------------------------------------------------ credits.json
craw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(craw)
for k in list(credits):
    if k in removed_keys and not os.path.exists(os.path.join(IMG, f'{k}.webp')):
        credits.pop(k)
for rid, (pid, name, purl, url, alt) in PHOTOS.items():
    credits[rid] = {'photographer': name, 'photographer_url': purl, 'photo_url': url, 'source': 'Pexels', 'alt': alt}
m = re.match(r'\{\s*\n([ \t]+)"', craw)
with open(P('credits.json'), 'w', encoding='utf-8') as fh:
    json.dump(credits, fh, ensure_ascii=False, indent=len(m.group(1)) if m else 1)
    fh.write('\n')

# ------------------------------------------------------------------ build.py
b = open(P('build.py'), encoding='utf-8').read()
b, n = re.subn(r"\('everyday', 'Everyday Favorites', '[a-z-]+'\)", "('Snacks', 'Snacks', 'peanut-butter-oat-bites')", b, count=1)
print('- OK: Everyday Favorites category -> Snacks' if n else '- SKIPPED: Everyday Favorites category not found')
m = re.search(r'FOCUS_IDS = (\[.*?\])', b)
if not m:
    sys.exit('ERROR: FOCUS_IDS not found in build.py.')
focus = json.loads(m.group(1)) + [v for v in MAP.values()]
b = b.replace(m.group(0), 'FOCUS_IDS = ' + json.dumps(focus), 1)
for old, new in MAP.items():
    b = b.replace(f"'{old}'", f"'{new}'").replace(f'"{old}"', f'"{new}"')
REDIRECTS = 'RECIPE_REDIRECTS = ' + json.dumps(MAP, indent=4).replace('\n}', '\n}\n') + '\n'
if 'def build_recipes():' not in b:
    sys.exit('ERROR: build_recipes() not found in build.py.')
b = b.replace('def build_recipes():', REDIRECTS + 'def build_recipes():', 1)
GEN = r"""    for old, new in RECIPE_REDIRECTS.items():
        full = os.path.join(OUT, 'recipes', old, 'index.html')
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'w').write(f'<!DOCTYPE html><meta charset="utf-8"><title>Redirecting…</title><link rel="canonical" href="{SITE_URL}recipes/{new}/"><meta http-equiv="refresh" content="0; url=../{new}/"><a href="../{new}/">Continue</a>')
"""
b, n = re.subn(r"(\n    page\('recipes/', 'All Recipes \| Bored of Toast',[^\n]*\n)", lambda mm: mm.group(1) + GEN, b, count=1)
if n != 1:
    sys.exit('ERROR: recipes page call not found in build.py.')
open(P('build.py'), 'w', encoding='utf-8').write(b)

# ------------------------------------------------------------------ storefront.py (any references to old ids)
sp = P('storefront.py')
s = open(sp, encoding='utf-8').read()
for old, new in MAP.items():
    s = s.replace(f"'{old}'", f"'{new}'").replace(f'"{old}"', f'"{new}"')
open(sp, 'w', encoding='utf-8').write(s)

# ------------------------------------------------------------------ checks.py
c = open(P('checks.py'), encoding='utf-8').read()
stubs = ''.join(f"'recipes/{old}/index.html', " for old in MAP)
c, n = re.subn(r'REDIRECT_STUBS = \{', 'REDIRECT_STUBS = {' + stubs, c, count=1)
if n != 1:
    sys.exit('ERROR: REDIRECT_STUBS not found in checks.py.')
open(P('checks.py'), 'w', encoding='utf-8').write(c)

# ------------------------------------------------------------------ save recipes
m = re.match(r'\[\s*\n([ \t]+)\{', raw)
with open(P('recipes.json'), 'w', encoding='utf-8') as fh:
    json.dump(recipes, fh, ensure_ascii=False, indent=len(m.group(1)) if m else None)
    fh.write('\n')

print('OK: 10 new recipes with Pexels photos, share and Pinterest images; old recipes redirect to their replacements.')
