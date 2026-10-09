#!/usr/bin/env python3
"""Recipe rewrite, pilot: Creamy Tomato Basil Soup -> small-plate, higher-protein version.

Same id, URL and photo. Cream is replaced by white beans and Greek yogurt; 6 small servings.

Nutrition per serving is an ESTIMATE: the previous per-recipe estimate (x4 servings), minus the
removed ingredients, plus the added ones, divided by 6. Reference values per 100 g (USDA FoodData
Central, rounded; please double-check before relying on them):
  olive oil 884 kcal / 100 g fat (1 tbsp = 13.5 g)
  heavy cream 340 kcal / 2.8 g protein / 2.8 g carbs / 36.1 g fat (1/3 cup = 80 g)
  canned white beans, drained 114 kcal / 7.3 g protein / 21.5 g carbs / 0.3 g fat / 4.8 g fiber (2 cans = 500 g)
  plain nonfat Greek yogurt 59 kcal / 10.2 g protein / 3.6 g carbs / 0.4 g fat (3/4 cup = 170 g)
  Totals: 840 - 119 - 272 + 570 + 100 = 1119 kcal; protein 16 - 2.3 + 36.3 + 17.3 = 67.3 g;
  carbs 80 - 2.3 + 107.3 + 6.1 = 191 g; fat 56 - 13.5 - 28.9 + 1.5 + 0.7 = 15.8 g; fiber 20 + 24 = 44 g.
  Per serving (/6): 187 kcal, 11 g protein, 32 g carbs, 3 g fat, 7 g fiber.

Safe to re-run. Run from the project root: python3 _src/recipe_pilot_tomato.py
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)
RID = 'tomato-basil-soup'
NEW_TITLE = 'Creamy Tomato Basil Soup with White Beans'

raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(raw)
r = next((x for x in recipes if x['id'] == RID), None)
if r is None:
    sys.exit(f'ERROR: recipe {RID} not found. Nothing was saved.')
if r.get('title') == NEW_TITLE:
    print('Pilot already applied. Nothing to do.')
    sys.exit(0)

r.update({
    'title': NEW_TITLE,
    'subtitle': 'Pantry tomatoes and two cans of white beans blended silky with fresh basil, finished with Greek yogurt instead of cream. About 11 g protein in a small bowl.',
    'desc': 'Silky tomato soup, thickened with white beans.',
    'prep': 10,
    'cook': 30,
    'time': 40,
    'serves': 6,
    'level': 'Easy',
    'intro': [
        'Tomato soup is one of the easiest things to eat when your appetite is small: it is warm, smooth and goes down slowly. The classic version is mostly tomatoes and cream, though, which makes it light on protein. This one swaps the cream for two cans of white beans and a little Greek yogurt, so each small bowl carries about 11 g of protein and still tastes like tomato soup.',
        'The beans disappear when you blend them. Their starch thickens the soup the way cream or flour would, so the texture stays silky. The yogurt goes in last, off the heat and warmed with a little hot soup first, because yogurt proteins tighten and turn grainy if they hit a boiling, acidic pot all at once.'
    ],
    'why': [
        ['About 11 g protein per cup', 'White beans and Greek yogurt replace the cream and keep the soup thick and creamy.'],
        ['Six small bowls from one pot', 'Portion it into 1-cup servings and freeze the extras for harder days.'],
        ['Silky without heavy cream', 'Blended beans give the soup body naturally, with no flour needed.']
    ],
    'ingredients': [
        {'group': 'For the soup', 'items': [
            {'q': 1, 'u': 'tbsp', 'n': 'olive oil'},
            {'q': 1, 'u': '', 'n': 'yellow onion', 'note': 'chopped'},
            {'q': 3, 'u': '', 'n': 'garlic cloves', 'note': 'minced'},
            {'q': 2, 'u': 'cans', 'n': 'whole peeled tomatoes', 'note': '28 oz / 800 g each'},
            {'q': 2, 'u': 'cans', 'n': 'cannellini beans', 'note': '15 oz / 425 g each, drained and rinsed'},
            {'q': 2, 'u': 'cups', 'n': 'vegetable broth', 'note': 'check the label if you need it gluten-free'},
            {'q': 1, 'u': 'tsp', 'n': 'sugar', 'note': 'balances the acidity'},
            {'q': 0.5, 'u': 'cup', 'n': 'fresh basil leaves', 'note': 'packed', 'g': 20}
        ]},
        {'group': 'To finish', 'items': [
            {'q': 0.75, 'u': 'cup', 'n': 'plain nonfat Greek yogurt', 'note': '170 g, at room temperature', 'g': 170},
            {'q': None, 'u': '', 'n': 'salt and black pepper', 'note': 'to taste'}
        ]}
    ],
    'steps': [
        {'t': 'Soften the onion and garlic',
         'd': 'Heat the olive oil in a large pot over medium heat until it shimmers. Add the onion with a pinch of salt and cook, stirring now and then, for 6 to 8 minutes, until soft and translucent but not browned. Add the garlic and stir for 1 minute, just until fragrant.',
         'tip': 'The pinch of salt pulls moisture from the onion so it softens faster and does not scorch.'},
        {'t': 'Simmer the tomatoes and beans',
         'd': 'Pour in the tomatoes with their juices and crush them against the side of the pot with a wooden spoon. Add the drained beans, broth and sugar and bring to a boil over medium-high heat. Lower to a steady simmer and cook uncovered for 15 to 20 minutes, stirring occasionally, until the beans are very soft and the raw edge of the tomatoes is gone.'},
        {'t': 'Blend with the basil',
         'd': 'Take the pot off the heat and add the basil. Blend with an immersion blender for about 2 minutes, until completely smooth. If you use a countertop blender, fill it no more than halfway, work in batches and leave the lid vent open under a folded towel so steam can escape.',
         'tip': 'Blend longer than you think. The smoother the beans, the more the soup tastes like cream.'},
        {'t': 'Temper the yogurt',
         'd': 'Put the yogurt in a bowl and whisk in a ladle of hot soup, then a second one, until smooth and warm. Stir the mixture back into the pot off the heat. Do not let the soup boil again once the yogurt is in.',
         'tip': 'Warming the yogurt gradually is what keeps it from splitting into grainy flecks.'},
        {'t': 'Season and serve small',
         'd': 'Taste and season with salt and pepper; canned tomatoes and broth vary a lot. Ladle into 1-cup portions and finish with torn basil and black pepper.'}
    ],
    'tips': [
        'Buy whole peeled tomatoes rather than diced. Diced tomatoes are often treated with calcium chloride to keep their shape, so they blend less smoothly.',
        'The soup keeps thickening as it cools because of the beans. Loosen it with broth, 1/4 cup at a time, when you reheat it.',
        'For freezing, stop before the yogurt step. Freeze the blended base and add the yogurt when you reheat a portion.',
        'Small-portion tip: serve half a portion and save the rest for later. A half bowl still counts.'
    ],
    'storage': 'Cool the soup and refrigerate in airtight containers for up to 4 days. Reheat gently in a saucepan over medium-low heat, stirring often and without boiling, or microwave in 1-minute bursts. The blended base, before the yogurt goes in, freezes well for up to 3 months; thaw overnight in the fridge and stir in the tempered yogurt as it reheats.',
    'variations': [
        ['Make it dairy-free', 'Skip the yogurt and blend 7 oz (200 g) silken tofu into the soup with the basil. It adds creaminess and some protein.'],
        ['Add roasted red pepper', 'Blend in 1 cup jarred roasted red peppers, drained, with the basil for a smokier, sweeter soup. Add an extra 1/2 cup broth if it gets too thick.'],
        ['Make it gentler', 'Serve it warm, not hot, and skip extra garlic or chili.'],
        ['Protein boost', 'Top each bowl with an extra spoonful of Greek yogurt, or serve it with a boiled egg on the side.']
    ],
    'nutrition': {'calories': 190, 'protein': 11, 'carbs': 32, 'fat': 3, 'fiber': 7},
    'faq': [
        ['Will it taste like beans?', 'Cannellini beans are mild, and once blended with tomatoes and basil they mostly add body. If you are unsure, start with one can; the soup will be thinner and lower in protein.'],
        ['Why did the yogurt turn grainy?', 'It was likely added to soup that was boiling, or added cold all at once. Warm it with a couple of ladles of hot soup first, stir it in off the heat, and do not boil the soup afterwards.'],
        ['Can I use other white beans?', 'Yes. Great Northern or navy beans work the same way. Drain and rinse them first.']
    ],
    'note': 'If you change only one thing about your usual tomato soup, make it the beans. They thicken it the way cream does and add most of the protein. Keep the yogurt step gentle, and on days when a full bowl feels like too much, serve it in a small mug.',
    'diet': ['vegetarian', 'gluten-free'],
})
# Below 15 g per serving, so it stays in Small Plates / Gentle, not High Protein.
if 'high-protein' in r.get('tags', []):
    r['tags'].remove('high-protein')

m = re.match(r'\[\s*\n([ \t]+)\{', raw)
indent = len(m.group(1)) if m else None
with open(P('recipes.json'), 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=indent)
    f.write('\n')

b = open(P('build.py'), encoding='utf-8').read()
b, n = re.subn(r"MODIFIED = '\d{4}-\d{2}-\d{2}'", "MODIFIED = '2026-10-09'", b, count=1)
if n:
    open(P('build.py'), 'w', encoding='utf-8').write(b)

print(f'{NEW_TITLE}: rewritten (6 servings, ~11 g protein, ~190 kcal per serving, estimates).')
print('dateModified bumped.' if n else 'MODIFIED not found in build.py (skipped).')
