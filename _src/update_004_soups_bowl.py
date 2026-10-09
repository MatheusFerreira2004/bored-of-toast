#!/usr/bin/env python3
"""Recipes 3/4: lemon chicken orzo soup, butternut squash soup, Mediterranean grain bowl.

Same ids, URLs and photos. Smaller portions or lighter bases, more protein, neutral kitchen notes
(no "tested" claims). Steps are merged into the existing step objects, so step photos stay attached.

Nutrition per serving is an ESTIMATE. Reference values (USDA FoodData Central, rounded;
double-check before relying on them):
  olive oil, 1 tbsp (13.5 g): 119 kcal, 13.5 g fat
  dry pasta (orzo), per 100 g: 371 kcal, 13 P, 75 C, 1.5 F, 3.2 fiber
  canned white beans, drained, per 100 g: 114 kcal, 7.3 P, 21.5 C, 0.3 F, 4.8 fiber
  plain nonfat Greek yogurt, per 100 g: 59 kcal, 10.2 P, 3.6 C, 0.4 F
  shelled edamame, per 100 g: 121 kcal, 11.9 P, 8.9 C, 5.2 F, 5.2 fiber
  butternut squash, raw, per 100 g: 45 kcal, 1 P, 11.7 C, 0.1 F, 2 fiber
  pepitas, per 100 g: 559 kcal, 30 P, 10.7 C, 49 F, 6 fiber

Lemon chicken orzo soup (was 6 x 310 kcal / 28 P / 29 C / 9 F / 2 fiber):
  -1 tbsp olive oil, orzo 1 cup -> 2/3 cup (-65 g dry)
  -> 1500 kcal, 159.5 P, 125 C, 39.5 F, 10 fiber / 6 = ~250 kcal, 27 g protein, 21 C, 7 F, 2 fiber
Butternut squash soup: recalculated from scratch, because the old per-serving estimate did not add up
  with its own ingredients. Squash 1100 g, large onion 150 g, apple 180 g, garlic 15 g, olive oil 2 tbsp,
  broth 4 cups (~40 kcal), maple 1 tbsp, white beans 250 g, Greek yogurt 170 g, pepitas 35 g
  -> 1583 kcal, 61.3 P, 258 C, 47.3 F, 43.3 fiber / 6 = ~265 kcal, 10 g protein, 43 C, 8 F, 7 fiber
Mediterranean grain bowl (was 4 x 470 / 16 / 52 / 23 / 11):
  dressing oil 3 -> 2 tbsp, +1 cup shelled edamame (155 g), 5 bowls instead of 4
  -> 1949 kcal, 82.4 P, 221.8 C, 86.6 F, 52.1 fiber / 5 = ~390 kcal, 16 g protein, 44 C, 17 F, 10 fiber

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

# ------------------------------------------------------------------ Lemon chicken orzo soup
NEW['lemon-chicken-orzo-soup'] = {
    'subtitle': 'Tender shredded chicken, a lighter hand of orzo and wilted spinach in a bright lemon-dill broth. About 27 g protein in a 1 1/2-cup bowl.',
    'desc': 'Lemony chicken soup, more chicken than pasta.',
    'serves': 6,
    'intro': [
        'Chicken soup is one of the most familiar foods to reach for when appetite is low: warm, salty, easy to sip. This version keeps the comfort but shifts the balance toward the chicken. It uses a little less orzo and a little less oil than a classic pot, so each bowl carries about 27 g of protein while staying light enough to finish.',
        'Poaching the thighs right in the broth does double duty: the chicken cooks gently, and its juices enrich the soup as it simmers. Keep the heat low, since meat proteins tighten and squeeze out moisture when they are boiled hard, which is what makes chicken stringy. The lemon goes in last, off the heat, because long cooking dulls its bright aroma.'
    ],
    'why': [
        ['About 27 g protein per bowl', 'A pound and a half of chicken thighs shared across six bowls.'],
        ['Light, brothy and bright', 'Less pasta and oil than a classic pot, with lemon and dill to keep it fresh.'],
        ['Made for small portions', 'Easy to reheat a mug or half a bowl at a time.']
    ],
    'ingredients': [
        {'group': 'For the soup', 'items': [
            {'q': 1, 'u': 'tbsp', 'n': 'olive oil'},
            {'q': 1, 'u': '', 'n': 'medium yellow onion', 'note': 'diced (about 1 1/2 cups)', 'g': 200},
            {'q': 2, 'u': '', 'n': 'medium carrots', 'note': 'diced (about 1 cup)', 'g': 130},
            {'q': 2, 'u': '', 'n': 'celery stalks', 'note': 'diced (about 3/4 cup)', 'g': 90},
            {'q': 4, 'u': '', 'n': 'garlic cloves', 'note': 'minced'},
            {'q': 1, 'u': 'tsp', 'n': 'dried oregano'},
            {'q': 8, 'u': 'cups', 'n': 'low-sodium chicken broth'},
            {'q': 2, 'u': '', 'n': 'bay leaves'},
            {'q': 1.5, 'u': 'lb', 'n': 'boneless, skinless chicken thighs', 'note': 'or breasts'},
            {'q': 1, 'u': 'tsp', 'n': 'kosher salt', 'note': 'plus more to taste'},
            {'q': 0.5, 'u': 'tsp', 'n': 'black pepper'},
            {'q': 0.67, 'u': 'cup', 'n': 'orzo', 'g': 125}
        ]},
        {'group': 'To finish', 'items': [
            {'q': 2, 'u': '', 'n': 'lemons', 'note': 'zest of 1 and about 1/3 cup juice total'},
            {'q': 3, 'u': 'cups', 'n': 'baby spinach', 'note': 'roughly chopped', 'g': 90},
            {'q': 0.25, 'u': 'cup', 'n': 'fresh dill', 'note': 'chopped, or parsley', 'g': 8},
            {'q': None, 'u': '', 'n': 'salt and pepper', 'note': 'to taste'}
        ]}
    ],
    'steps': [
        {'t': 'Soften the vegetables',
         'd': 'Heat the olive oil in a large Dutch oven over medium heat until it shimmers. Add the onion, carrots and celery with a pinch of salt and cook for 6 to 8 minutes, stirring occasionally, until the onion is translucent and the carrots begin to soften. Stir in the garlic and oregano and cook for 1 minute, until fragrant.',
         'tip': 'With only a tablespoon of oil, keep the heat at medium and stir often. The salt helps the vegetables release moisture so they soften instead of sticking.'},
        {'t': 'Poach the chicken',
         'd': 'Pour in the broth, add the bay leaves, salt and pepper, and nestle the chicken into the liquid. Bring to a boil over medium-high heat, then lower to a gentle simmer, partially cover and cook for 15 to 18 minutes, until the thickest part of the chicken registers 165°F (74°C).',
         'tip': 'Keep it at a lazy simmer with small bubbles breaking the surface. A hard boil makes the chicken tough and the broth cloudy.'},
        {'t': 'Shred the chicken',
         'd': 'Move the chicken to a cutting board and let it cool for 5 minutes, just enough to handle. Shred it into small, bite-sized pieces with two forks; smaller shreds are easier to eat on low-appetite days. Fish out the bay leaves and discard them.'},
        {'t': 'Cook the orzo',
         'd': 'Bring the broth back to a simmer over medium heat and stir in the orzo. Cook for 8 to 10 minutes, stirring every couple of minutes so it does not stick, until it is tender with a slight bite in the center.',
         'tip': 'The orzo keeps drinking broth as it sits, so pull it off the heat while it still has a little chew.'},
        {'t': 'Add lemon and greens',
         'd': 'Turn off the heat and stir in the shredded chicken, spinach, lemon zest and about two thirds of the lemon juice. Let the pot sit for 1 to 2 minutes, until the spinach has wilted. Stir in the dill, then taste and add more salt, pepper or lemon until the broth tastes bright and well seasoned.',
         'tip': 'Salt and acid work together. If the soup tastes sour but thin, add a pinch of salt rather than more lemon.'},
        {'t': 'Serve small',
         'd': 'Ladle into 1 1/2-cup bowls, or a mug for a lighter serving, and top with extra dill and black pepper. Bread is optional; the soup is a full meal on its own.'}
    ],
    'tips': [
        'Thighs are more forgiving than breasts. Their extra fat and connective tissue keep them juicy even if they simmer a few minutes too long.',
        'If you plan to eat the soup over several days, cook the orzo separately and add a spoonful to each bowl, so it does not soak up all the broth in the fridge.',
        'Zest the lemons before you juice them. The zest carries most of the fragrant oils.',
        SMALL_TIP
    ],
    'storage': 'Refrigerate the soup in airtight containers for up to 4 days. The orzo absorbs broth overnight, so reheat it in a saucepan over medium heat with an extra 1/2 cup of broth, stirring until steaming. To freeze, make the soup without orzo and freeze in 1 1/2-cup portions for up to 3 months, then cook a little fresh orzo when you reheat it.',
    'variations': [
        ['Greek avgolemono style', 'Whisk 2 eggs with the lemon juice, slowly whisk in 2 cups of hot broth to temper, then stir the mixture back into the pot off the heat. It makes the soup silky and adds a little more protein.'],
        ['Use rotisserie chicken', 'Skip the poaching and simmer the broth with the bay leaves for 10 minutes, then add 4 cups of shredded rotisserie chicken with the spinach.'],
        ['Swap the pasta', 'Use 2/3 cup long-grain rice and simmer it for 15 to 18 minutes, or a gluten-free small pasta following the package time.'],
        ['Make it gentler', 'Serve it warm rather than hot, go light on the lemon on unsettled days, and sip the broth from a mug.'],
        ['Protein boost', 'Stir a spoonful of plain Greek yogurt into your bowl, or add a soft-boiled egg.']
    ],
    'nutrition': {'calories': 250, 'protein': 27, 'carbs': 21, 'fat': 7, 'fiber': 2},
    'faq': [
        ['Can I use chicken breasts instead of thighs?', 'Yes. Start checking them at 12 minutes and pull them as soon as they hit 165°F (74°C), since breasts dry out faster than thighs.'],
        ['Why did my soup turn thick?', 'The orzo kept absorbing liquid as it sat. Stir in more broth or water until it loosens, then re-season with salt and lemon.'],
        ['Can I make it ahead?', 'Yes. Make the soup through the chicken step up to 2 days ahead, then reheat, cook the orzo and finish with lemon, spinach and dill just before serving.']
    ],
    'note': 'This pot leans on the chicken rather than the pasta, which is what keeps each bowl high in protein without feeling heavy. On a low-appetite day, start with a mug of the broth and a few shreds of chicken; the rest keeps well for later in the week.',
}

# ------------------------------------------------------------------ Butternut squash soup
NEW['butternut-squash-soup'] = {
    'title': 'Roasted Butternut Squash Soup with White Beans',
    'subtitle': 'Oven-caramelized squash, apple and garlic blended with white beans and finished with Greek yogurt instead of cream. About 10 g protein in a small bowl.',
    'desc': 'Roasted squash soup, creamy without the cream.',
    'serves': 6,
    'intro': [
        'Butternut squash soup is soft, smooth and gently sweet, which makes it easy to eat when nothing else sounds good. The usual version relies on heavy cream and has very little protein. This one blends a can of white beans into the roasted vegetables and finishes with Greek yogurt, so it stays velvety while each bowl carries about 10 g of protein.',
        'Roasting is what gives the soup depth. At 425°F the natural sugars caramelize and the edges brown, creating nutty flavors that boiling cannot. A tart apple and whole garlic cloves roast alongside the squash, and a splash of cider vinegar at the end balances the sweetness.'
    ],
    'why': [
        ['Creamy without heavy cream', 'Blended white beans and Greek yogurt give the soup body and protein.'],
        ['Roasted, not boiled', 'Caramelized edges give the soup real depth and savoriness.'],
        ['Freezes well', 'Freeze the base in small portions and stir in the yogurt when you reheat.']
    ],
    'ingredients': [
        {'group': 'For roasting', 'items': [
            {'q': 1, 'u': '', 'n': 'large butternut squash', 'note': 'about 3 lb, peeled, seeded and cut into 1-inch cubes (about 8 cups)', 'g': 1100},
            {'q': 1, 'u': '', 'n': 'large yellow onion', 'note': 'cut into thick wedges'},
            {'q': 1, 'u': '', 'n': 'tart apple', 'note': 'such as Granny Smith, cored and quartered'},
            {'q': 5, 'u': '', 'n': 'garlic cloves', 'note': 'peeled and left whole'},
            {'q': 2, 'u': 'tbsp', 'n': 'olive oil'},
            {'q': 1.5, 'u': 'tsp', 'n': 'kosher salt'},
            {'q': 0.5, 'u': 'tsp', 'n': 'black pepper'}
        ]},
        {'group': 'For the soup', 'items': [
            {'q': 4, 'u': 'cups', 'n': 'vegetable broth', 'note': 'check the label if you need it gluten-free'},
            {'q': 1, 'u': 'can', 'n': 'cannellini beans', 'note': '15 oz / 425 g, drained and rinsed'},
            {'q': 1, 'u': 'tsp', 'n': 'fresh thyme leaves', 'note': 'or 1/2 tsp dried'},
            {'q': 0.25, 'u': 'tsp', 'n': 'ground nutmeg'},
            {'q': 0.25, 'u': 'tsp', 'n': 'ground cinnamon'},
            {'q': 0.75, 'u': 'cup', 'n': 'plain nonfat Greek yogurt', 'note': '170 g, at room temperature', 'g': 170},
            {'q': 1, 'u': 'tbsp', 'n': 'maple syrup', 'note': 'optional, depending on squash sweetness'},
            {'q': 1, 'u': 'tsp', 'n': 'apple cider vinegar'},
            {'q': None, 'u': '', 'n': 'salt and pepper', 'note': 'to taste'}
        ]},
        {'group': 'To serve', 'items': [
            {'q': 0.25, 'u': 'cup', 'n': 'toasted pepitas', 'g': 35}
        ]}
    ],
    'steps': [
        {'t': 'Prep and season',
         'd': 'Heat the oven to 425°F (220°C) and line two large sheet pans with parchment. Toss the squash, onion, apple and garlic with the olive oil, salt and pepper, then spread in a single layer across both pans with some space between pieces.',
         'tip': 'Crowded vegetables steam in their own moisture and stay pale. Two pans give you browned edges, which is where the flavor lives.'},
        {'t': 'Roast until caramelized',
         'd': 'Roast for 35 to 40 minutes, flipping everything and swapping the pans halfway through, until a fork slides into the squash easily and the edges are deep golden. Pull the garlic early if it starts turning dark brown, since burnt garlic tastes bitter.'},
        {'t': 'Simmer with broth and beans',
         'd': 'Transfer the roasted vegetables to a large pot. Add the broth, drained beans, thyme, nutmeg and cinnamon and bring to a boil over medium-high heat, then reduce to a gentle simmer for 10 minutes, until the apple and beans are very soft.'},
        {'t': 'Blend until silky',
         'd': 'Take the pot off the heat and blend with an immersion blender for 2 minutes, until completely smooth. If using a countertop blender, work in batches no more than half full and leave the lid vent open under a folded towel so steam can escape.',
         'tip': 'Blend longer than you think. The smoother the beans, the creamier the soup tastes.'},
        {'t': 'Temper the yogurt and finish',
         'd': 'Whisk the yogurt in a bowl with a ladle of hot soup, then a second one, until smooth and warm. Stir it back into the pot off the heat with the maple syrup if using and the vinegar. Do not boil the soup once the yogurt is in. If it is too thick, add broth 1/4 cup at a time. Taste and adjust the salt.'},
        {'t': 'Serve small',
         'd': 'Ladle into 1-cup bowls or mugs and top each with a spoonful of toasted pepitas for crunch.'}
    ],
    'tips': [
        'Pre-cut squash saves about 10 minutes of peeling. You need roughly 2 1/2 lb (1.1 kg) of cubes.',
        'Season in stages. Salting the vegetables before roasting helps them brown, and a final taste after the yogurt and vinegar lets you dial it in.',
        'For freezing, stop before the yogurt step. Freeze the blended base and add the tempered yogurt when you reheat a portion.',
        SMALL_TIP
    ],
    'storage': 'Refrigerate in airtight containers for up to 4 days. Reheat gently over medium-low heat without boiling, stirring often. The blended base, before the yogurt goes in, freezes well for up to 3 months; thaw overnight in the fridge and stir in tempered yogurt as it reheats.',
    'variations': [
        ['Dairy-free', 'Skip the yogurt and blend 7 oz (200 g) silken tofu into the soup with the beans.'],
        ['Curried squash', 'Add 2 teaspoons curry powder and a 1-inch piece of grated ginger with the broth, and skip the cinnamon.'],
        ['Smoky chipotle', 'Replace the nutmeg and cinnamon with 1/2 teaspoon smoked paprika and 1 minced chipotle in adobo, then finish with lime instead of vinegar.'],
        ['Make it gentler', 'Skip the pepitas, serve it warm in a mug and sip it slowly.'],
        ['Protein boost', 'Top each bowl with an extra spoonful of Greek yogurt, or serve with a boiled egg on the side.']
    ],
    'nutrition': {'calories': 265, 'protein': 10, 'carbs': 43, 'fat': 8, 'fiber': 7},
    'faq': [
        ['Can I use frozen butternut squash?', 'Yes. Roast it from frozen at the same temperature, spread out well, and expect it to take 10 to 15 minutes longer.'],
        ['Why did the yogurt turn grainy?', 'It was likely added to soup that was boiling, or added cold all at once. Warm it with a couple of ladles of hot soup first and stir it in off the heat.'],
        ['Why does my soup taste flat?', 'It usually needs salt or acid. Add salt a pinch at a time, then a few more drops of vinegar, tasting after each addition.']
    ],
    'note': 'Roasting is still the step that makes this soup, so give the squash the full time and two pans. The beans and yogurt do the work the cream used to do, and add protein along the way. A mug of it, warm rather than hot, is one of the gentlest small meals on the site.',
    'diet': ['vegetarian', 'gluten-free'],
}

# ------------------------------------------------------------------ Mediterranean grain bowl
NEW['mediterranean-grain-bowl'] = {
    'subtitle': 'Quinoa, crunchy roasted chickpeas, edamame, olives and feta with a sharp oregano-lemon dressing. Five smaller bowls, about 16 g protein each.',
    'desc': 'Five smaller bowls, extra edamame for protein.',
    'serves': 5,
    'intro': [
        'Grain bowls are easy to portion and easy to eat cold, which makes them useful for lunches on low-appetite days. This version adds a cup of edamame to the quinoa and roasted chickpeas, uses a little less oil in the dressing and divides everything into five smaller bowls, so each one carries about 16 g of protein.',
        'Texture is what keeps a grain bowl interesting. The trick to crunchy chickpeas is getting the water off the surface before they hit the oven, since any moisture has to evaporate before the outsides can brown. Letting the quinoa rest covered off the heat finishes the grains gently, so they come out separate and fluffy instead of wet.'
    ],
    'why': [
        ['About 16 g protein per bowl', 'Quinoa, chickpeas, edamame and feta in every portion.'],
        ['Five smaller bowls', 'A lunch you can finish, with leftovers ready for the week.'],
        ['Holds up for days', 'Stored undressed, the base and vegetables stay fresh for up to 4 days.']
    ],
    'ingredients': [
        {'group': 'For the base', 'items': [
            {'q': 1, 'u': 'cup', 'n': 'quinoa', 'note': 'rinsed well', 'g': 170},
            {'q': 2, 'u': 'cups', 'n': 'water or vegetable broth'},
            {'q': 1, 'u': 'cup', 'n': 'frozen shelled edamame', 'note': 'thawed', 'g': 155}
        ]},
        {'group': 'For the crispy chickpeas', 'items': [
            {'q': 1, 'u': 'can', 'n': 'chickpeas', 'note': '15 oz / 425 g, drained and dried'},
            {'q': 1, 'u': 'tbsp', 'n': 'olive oil'},
            {'q': 1, 'u': 'tsp', 'n': 'ground cumin'},
            {'q': 0.5, 'u': 'tsp', 'n': 'smoked paprika'}
        ]},
        {'group': 'For the bowl', 'items': [
            {'q': 1, 'u': '', 'n': 'English cucumber', 'note': 'diced'},
            {'q': 1, 'u': 'cup', 'n': 'cherry tomatoes', 'note': 'halved', 'g': 150},
            {'q': 0.5, 'u': '', 'n': 'red onion', 'note': 'thinly sliced, optional'},
            {'q': 0.5, 'u': 'cup', 'n': 'Kalamata olives', 'g': 70},
            {'q': 0.5, 'u': 'cup', 'n': 'crumbled feta', 'g': 75},
            {'q': None, 'u': '', 'n': 'fresh parsley', 'note': 'chopped'}
        ]},
        {'group': 'For the dressing', 'items': [
            {'q': 2, 'u': 'tbsp', 'n': 'extra-virgin olive oil'},
            {'q': 2, 'u': 'tbsp', 'n': 'lemon juice'},
            {'q': 1, 'u': 'tsp', 'n': 'dried oregano'}
        ]}
    ],
    'steps': [
        {'t': 'Roast the chickpeas',
         'd': 'Heat the oven to 425°F (220°C). Toss the well-dried chickpeas with the olive oil, cumin, smoked paprika and a pinch of salt, then spread them in a single layer on a sheet pan. Roast for 20 to 25 minutes, shaking the pan halfway, until deep golden and they rattle when you shake the pan.',
         'tip': 'Roll the chickpeas in a clean kitchen towel and pull off any loose skins. Dry chickpeas and fewer skins mean a crisper result.'},
        {'t': 'Cook the quinoa',
         'd': 'Combine the rinsed quinoa and water or broth with 1/2 teaspoon salt in a saucepan and bring to a boil. Cover, turn the heat to low and simmer for 15 minutes, until the liquid is absorbed. Take the pan off the heat, scatter the thawed edamame on top, cover again and leave for 5 minutes, then fluff everything together with a fork.',
         'tip': 'Rinse the quinoa until the water runs clear. Its natural coating tastes bitter and soapy.'},
        {'t': 'Prep the vegetables',
         'd': 'While everything cooks, dice the cucumber and halve the tomatoes. If using red onion, slice it as thinly as you can and soak it in cold water for 5 minutes, then drain; the soak takes away its harsh bite.'},
        {'t': 'Make the dressing',
         'd': 'Whisk the extra-virgin olive oil, lemon juice and dried oregano with a good pinch of salt and pepper. Taste it on a piece of cucumber: it should be sharp and a little salty, since the quinoa will soften it.'},
        {'t': 'Build five bowls',
         'd': 'Divide the quinoa and edamame among 5 bowls or containers. Top with the cucumber, tomatoes, onion if using, olives and chickpeas, then scatter over the feta and parsley. Drizzle with the dressing just before eating so the chickpeas keep their crunch.',
         'tip': 'Toss a spoonful of dressing into the quinoa itself before topping, so the bottom of the bowl tastes as good as the top.'}
    ],
    'tips': [
        'If your chickpeas soften after a day, give them 5 minutes at 400°F (200°C) to crisp them back up.',
        'For meal prep, pack the dressing in a small separate jar and add the feta on the day, so the vegetables do not go soggy.',
        'Frozen edamame only needs to thaw. Run it under warm water for a minute if you forgot to take it out.',
        SMALL_TIP
    ],
    'storage': 'Store the quinoa, edamame and vegetables, without dressing or chickpeas, in airtight containers in the fridge for up to 4 days. Keep the chickpeas in a loosely covered container at room temperature for up to 2 days so they stay crisp, and the dressing in a jar in the fridge. Eat the bowls cold or at room temperature.',
    'variations': [
        ['Swap in farro', 'Use 1 cup farro instead of quinoa and simmer it in salted water for 25 to 30 minutes until chewy. Note that farro contains gluten.'],
        ['Add chicken or salmon', 'Top each bowl with about 3 ounces of grilled chicken or salmon for a heartier meal.'],
        ['Make it vegan', 'Leave out the feta and add a spoonful of hummus for creaminess.'],
        ['Make it gentler', 'Serve a half bowl, leave out the raw onion and olives, and use a milder dressing with less lemon.'],
        ['Protein boost', 'Add a soft-boiled egg, or a spoonful of hummus on the side.']
    ],
    'nutrition': {'calories': 390, 'protein': 16, 'carbs': 44, 'fat': 17, 'fiber': 10},
    'faq': [
        ['Can I use canned chickpeas straight from the can?', 'Yes, but drain, rinse and dry them thoroughly first. Wet chickpeas steam in the oven and come out soft.'],
        ['Why is my quinoa mushy?', 'Usually too much liquid or skipping the covered rest. Stick to a 1 to 2 ratio and let it sit off the heat for 5 minutes before fluffing.'],
        ['How far ahead can I make it?', 'Cook the quinoa, prep the vegetables and mix the dressing up to 4 days ahead. Roast the chickpeas no more than 2 days ahead.']
    ],
    'note': 'Five bowls instead of four, plus a cup of edamame, is what turns this into a small plate that still counts as a full lunch. Drying the chickpeas properly is the one step worth not rushing; the crunch is what keeps the bowl interesting to eat.',
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
