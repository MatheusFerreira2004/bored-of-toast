from recipe_adapter import editorial_model
from pilot_recipe import render_editorial_recipe, MODELS
from kitchen_notes import index as render_kitchen_notes_index, guide as render_kitchen_note_guide, GUIDES, home_feature as render_kitchen_home_feature, start as render_kitchen_start
from pathlib import Path
import html
import re
import json

ROOT = Path(__file__).parent
OUT = ROOT / 'dist'
AS = OUT / 'assets'
AS.mkdir(parents=True, exist_ok=True)

FRACTIONS = {
    '½': 0.5,
    '⅓': 1/3,
    '⅔': 2/3,
    '¼': 0.25,
    '¾': 0.75,
    '⅛': 0.125,
    '⅜': 0.375,
    '⅝': 0.625,
    '⅞': 0.875
}

# ---------------------------------------------------------------------------
# Category definitions — single source of truth
# ---------------------------------------------------------------------------
CATEGORIES = [
    dict(
        slug='quick-easy',
        label='Quick & Easy',
        desc='Short active prep and few steps — ready in 25 minutes or less. Overnight resting is noted separately.'
    ),
    dict(
        slug='budget-friendly',
        label='Budget-Friendly',
        desc='Meals built around pantry staples and everyday affordable ingredients.'
    ),
    dict(
        slug='plant-forward',
        label='Plant-Forward',
        desc='Vegetables, fruits, grains, and legumes take the lead. Not necessarily vegan.'
    ),
    dict(
        slug='protein-forward',
        label='Protein-Forward',
        desc='Recipes centred on legumes, eggs, tofu, or other protein sources.'
    ),
    dict(
        slug='make-ahead',
        label='Make-Ahead',
        desc='Suited to preparing in advance or starting the night before — breakfast included.'
    ),
    dict(
        slug='pantry-meals',
        label='Pantry Meals',
        desc='Built around shelf-stable ingredients you are likely to have at home.'
    ),
    dict(
        slug='fresh-lunches',
        label='Fresh Lunches',
        desc='No-cook or minimal-cook options that feel light and lively at midday.'
    ),
    dict(
        slug='cozy-dinners',
        label='Cozy Dinners',
        desc='Warm skillet and stovetop meals that are comforting after a long day.'
    ),
    dict(
        slug='one-ingredient-different-ways',
        label='One Ingredient, Different Ways',
        desc='The same starting ingredient taken in entirely different directions.'
    ),
]

# Lookup helper: slug → label
from constants import CAT_LABEL


def parse_ingredient(text):
    text = text.strip()
    m_mixed = re.match(r'^(\d+)\s+([½⅓⅔¼¾⅛⅜⅝⅞])\s+(.*)$', text)
    if m_mixed:
        whole = int(m_mixed.group(1))
        frac = FRACTIONS[m_mixed.group(2)]
        val = whole + frac
        display = f"{m_mixed.group(1)} {m_mixed.group(2)}"
        return val, display, m_mixed.group(3)

    m_frac = re.match(r'^([½⅓⅔¼¾⅛⅜⅝⅞])\s+(.*)$', text)
    if m_frac:
        frac_char = m_frac.group(1)
        return FRACTIONS[frac_char], frac_char, m_frac.group(2)

    m_num = re.match(r'^(\d+(?:\.\d+)?)\s+(.*)$', text)
    if m_num:
        val = float(m_num.group(1))
        display = m_num.group(1)
        return val, display, m_num.group(2)

    return None, None, text

recipes = [
    dict(
        slug='lemon-chickpea-salad',
        tested=False,
        title='Lemon chickpea salad',
        cat='THE NO-COOK LUNCH',
        categories=['quick-easy', 'budget-friendly', 'protein-forward', 'plant-forward', 'fresh-lunches', 'one-ingredient-different-ways'],
        primary_goal='A no-cook lunch ready in 10 minutes.',
        why_it_works='Chickpeas bring body, cucumber adds crunch, and lemon keeps the bowl bright.',
        img='chickpea.png',
        alt='Illustrated serving suggestion for lemon chickpea salad with cucumber and feta',
        desc='Crunchy cucumber, chickpeas and a lemony dressing. A fresh answer to the same old lunch.',
        serves='2',
        prep_time='10 min prep',
        total_time='10 min total',
        method='No-cook',
        difficulty='Easy',
        time_estimate='10 min prep · 10 min total · No-cook',
        time_glance='~10 mins total',
        card_time='~10 mins',
        ingredients=[
            {'text': '1 can (15 oz / 425 g) chickpeas, drained and rinsed; about 240 g drained', 'swap': 'Try cooked, drained white beans.'},
            '1 cup (150 g) diced cucumber',
            '1 cup (150 g) cherry tomatoes, halved',
            {'text': '⅓ cup (50 g) crumbled feta', 'swap': 'Try diced avocado for a different texture.'},
            {'text': '¼ cup loosely packed chopped flat-leaf parsley', 'swap': 'Dill can replace parsley.'},
            'SECTION: For the dressing',
            '2 tbsp olive oil',
            '2 tbsp lemon juice, plus more to taste',
            'Black pepper and salt, to taste'
        ],
        steps=[
            ('Make the dressing.', 'Whisk the olive oil and lemon juice in a large bowl. Add a few grinds of black pepper.'),
            ('Build the salad.', 'Add the drained chickpeas, cucumber, tomatoes and parsley. Toss until everything is lightly coated.'),
            ('Finish with feta.', 'Fold in the feta. Taste before adding salt: feta and canned chickpeas can already be salty. Divide into portions and serve.')
        ],
        tip='Drain the chickpeas well so the dressing stays bright rather than watery. Add the feta last to keep some distinct pieces.',
        allergens='Contains milk (feta).',
        extra='For a more substantial lunch, serve with bread or tuck a portion into a wrap.',
        related_notes=['keep-salad-crisp', 'simple-lemon-dressing'],
    ),
    dict(
        slug='lemon-white-bean-skillet',
        tested=False,
        title='Lemony white beans & spinach',
        cat='ONE PAN, EVERYDAY INGREDIENTS',
        categories=['quick-easy', 'budget-friendly', 'protein-forward', 'plant-forward', 'pantry-meals', 'cozy-dinners'],
        primary_goal='A warm one-pan skillet in 15 minutes.',
        why_it_works='Garlic kept pale adds fragrance without bitterness. Mashing a few beans thickens the liquid into a light sauce. Lemon goes in off the heat so its brightness stays lively.',
        img='beans.png',
        alt='Illustration of white beans and spinach in a skillet with a light lemony sauce',
        desc='Soft white beans, wilted spinach and a little lemon. Keep some bread nearby for the pan juices.',
        serves='2',
        prep_time='5 min prep',
        total_time='15 min total',
        method='One-pan',
        difficulty='Easy',
        time_estimate='5 min prep · 15 min total · One-pan',
        time_glance='~15 mins total',
        card_time='~15 mins',
        ingredients=[
            '1 tbsp olive oil',
            '2 garlic cloves, thinly sliced',
            '1 can (15 oz / 425 g) white beans, drained and rinsed; about 240 g drained',
            '⅓ cup (80 ml) water',
            '3 packed cups (90 g) baby spinach',
            '1 tbsp lemon juice, plus more to taste',
            '¼ tsp dried oregano',
            'Salt and black pepper, to taste',
            '2 slices of bread, to serve'
        ],
        steps=[
            ('Gently cook the garlic.', 'Warm the oil in a skillet over medium-low heat. Add the garlic and stir for about 1 minute, until fragrant but not browned.'),
            ('Warm the beans.', 'Add the beans, water and oregano. Bring to a gentle simmer and cook for about 5 minutes. Mash a spoonful of beans against the pan to thicken the sauce.'),
            ('Wilt the spinach.', 'Add the spinach in handfuls and stir until wilted. If the pan looks dry, add another splash of water.'),
            ('Add the lemon.', 'Remove from the heat, stir in lemon juice, then taste and season. Divide into portions and serve with bread.')
        ],
        swap='Cannellini, great northern or butter beans all work here. If using larger beans, let their texture guide the warming time.',
        tip='Keep the garlic pale. If it burns, it can make the whole pan taste bitter. Lemon goes in at the end to keep its flavor lively.',
        allergens='Bread may contain wheat and other allergens; check its label.',
        extra='Want more crunch? Top your bowl with a few chopped radishes just before serving.',
        related_notes=['make-beans-creamy', 'simple-lemon-dressing'],
    ),
    dict(
        slug='blueberry-overnight-oats',
        tested=False,
        title='Blueberry overnight oats',
        cat='BREAKFAST, ALREADY STARTED',
        categories=['budget-friendly', 'plant-forward', 'make-ahead'],
        primary_goal='A creamy breakfast you prepare the night before.',
        why_it_works='Rolled oats soak overnight and soften without cooking. Yogurt adds creaminess and a mild tang. Fresh fruit goes on last so it stays bright.',
        img='oats.png',
        alt='Illustration of blueberry overnight oats in a glass jar with banana slices',
        desc='A small evening task that leaves you with a creamy breakfast to finish in the morning.',
        serves='1',
        prep_time='5 min prep',
        total_time='Chill overnight',
        method='Make-ahead',
        difficulty='Very easy',
        time_estimate='5 min prep · Chill overnight',
        time_glance='5 min + overnight',
        card_time='Overnight',
        ingredients=[
            '½ cup (40 g) rolled oats',
            '½ cup (120 ml) milk or an unsweetened plant drink',
            '¼ cup (60 g) plain yogurt',
            '½ cup (75 g) blueberries',
            '½ banana, sliced just before serving',
            'A pinch of cinnamon, optional'
        ],
        steps=[
            ('Mix the base.', 'Stir the oats, milk, yogurt and optional cinnamon in a clean covered container.'),
            ('Refrigerate overnight.', 'Cover and place in the refrigerator overnight so the oats soften. Do not leave the mixture on the counter.'),
            ('Finish in the morning.', 'Stir, adding a splash of milk if you prefer a looser texture. Top with blueberries and freshly sliced banana, then serve.')
        ],
        swap='Use strawberries or diced pear in place of blueberries. Dairy-free yogurt and a plant drink also work, with a different taste and texture.',
        tip='Use rolled oats for a little texture. Steel-cut oats need a different method and are not a direct substitute in this recipe.',
        allergens='Contains milk if made with dairy. Check oats and alternative products for relevant allergen labels.',
        extra='The fruit brings sweetness. Taste the finished bowl before deciding whether it needs anything else.',
        related_notes=[],
    ),
    dict(
        slug='crispy-sheet-pan-gnocchi',
        title='Crispy sheet-pan gnocchi with cherry tomatoes & basil',
        cat='SHEET-PAN · CRISP & TENDER',
        categories=['budget-friendly', 'plant-forward', 'quick-easy', 'cozy-dinners'],
        primary_goal='A sheet-pan dinner with crispy gnocchi and burst tomatoes.',
        why_it_works='Dry-roasting shelf-stable gnocchi draws out moisture so the outside crisps while the centre stays pillowy. Burst tomatoes create a natural pan sauce with no extra effort.',
        img='gnocchi.png',
        alt='Crispy sheet-pan gnocchi with burst cherry tomatoes and torn basil leaves',
        desc='Shelf-stable potato gnocchi roasted dry until crisp outside and pillowy inside, tossed with burst cherry tomatoes and fresh torn basil.',
        serves='2',
        prep_time='5 min prep',
        total_time='25 min total',
        method='Sheet-pan',
        difficulty='Easy',
        time_estimate='5 min prep · 25 min total · Sheet-pan',
        time_glance='~25 mins total',
        card_time='~25 mins',
        tested=False,
        ingredients=[
            '1 package (16 oz / 450 g) shelf-stable potato gnocchi',
            '2 cups (300 g) cherry or grape tomatoes',
            'SECTION: For the dressing',
            '2 tbsp olive oil',
            '2 garlic cloves, smashed',
            '½ tsp dried oregano',
            '½ tsp kosher salt',
            '¼ tsp black pepper',
            '½ cup fresh basil leaves, torn',
            '2 tbsp grated Parmesan or pecorino (optional)'
        ],
        steps=[
            ('Heat the oven and prep pan.', 'Preheat oven to 425°F (220°C). Line a large rimmed baking sheet with parchment paper.'),
            ('Toss directly on the sheet.', 'Add the uncooked gnocchi, whole cherry tomatoes, and smashed garlic cloves directly onto the pan. Drizzle with olive oil, oregano, salt, and black pepper. Toss with hands until evenly glossy, spreading in a single layer.'),
            ('Roast until golden and blistered.', 'Bake for 20 to 25 minutes, tossing once halfway through, until gnocchi are deeply golden and crisp on the edges and tomatoes have burst and released juices.'),
            ('Finish with basil and cheese.', 'Toss in the torn basil right on the hot sheet so it wilts slightly. Sprinkle with grated Parmesan and serve hot straight from the pan.')
        ],
        swap='No basil? Baby arugula or spinach folded in hot adds fresh peppery greens. For extra protein, toss cooked chickpeas or sliced sausage onto the sheet.',
        tip='Do not boil the gnocchi first! Roasting dry shelf-stable gnocchi directly in olive oil creates a delightful crispy skin with a pillowy interior.',
        allergens='Contains wheat (gnocchi). Contains milk if finished with cheese.',
        extra='Leftovers reheat surprisingly well in a dry hot skillet or air fryer for 3 minutes to restore crispness.',
        related_notes=[],
    ),
    dict(
        slug='mediterranean-warm-green-lentils',
        title='15-minute Mediterranean warm green lentils',
        cat='PANTRY PROTEIN · WARM & EARTHY',
        categories=['budget-friendly', 'protein-forward', 'plant-forward', 'quick-easy', 'pantry-meals', 'cozy-dinners'],
        primary_goal='A warming lentil bowl ready in 15 minutes.',
        why_it_works='Cumin and coriander bloom quickly in warm oil, coating the lentils with earthy fragrance. Lemon juice and zest added off the heat keeps the citrus bright against the warm spices.',
        img='lentils.png',
        alt='Warm green lentils with wilted spinach and crumbled goat cheese in a bowl',
        desc='Tender cooked brown lentils warmed with shallots, cumin, lemon zest, baby spinach, and crumbled creamy goat cheese.',
        serves='2',
        prep_time='5 min prep',
        total_time='15 min total',
        method='One-pan',
        difficulty='Easy',
        time_estimate='5 min prep · 15 min total · One-pan',
        time_glance='~15 mins total',
        card_time='~15 mins',
        tested=False,
        ingredients=[
            '1 can (15 oz / 400 g) cooked brown or green lentils, rinsed and drained',
            '1 tbsp olive oil',
            '1 medium shallot, finely chopped',
            '1 garlic clove, minced',
            '½ tsp ground cumin',
            '¼ tsp ground coriander',
            '2 cups (60 g) baby spinach leaves',
            '1 tbsp fresh lemon juice, plus ½ tsp grated lemon zest',
            '⅓ cup (50 g) crumbled goat cheese or feta',
            'Salt and black pepper, to taste'
        ],
        steps=[
            ('Soften the aromatics.', 'Heat olive oil in a medium skillet over medium heat. Add chopped shallot and cook 3 minutes until translucent. Stir in minced garlic, cumin, and coriander for 30 seconds until fragrant.'),
            ('Warm the lentils.', 'Add the drained lentils and 2 tablespoons of water or broth. Simmer gently for 4–5 minutes, stirring occasionally, until hot throughout.'),
            ('Wilt greens and brighten.', 'Stir in the spinach leaves in batches until just wilted (about 1 minute). Remove pan from heat and stir in lemon juice, lemon zest, salt, and pepper.'),
            ('Plate and top.', 'Transfer to warm bowls. Scatter crumbled goat cheese or feta over top and finish with a light drizzle of olive oil.')
        ],
        swap='Swap canned brown lentils with cooked French Puy lentils. Dairy-free? Replace goat cheese with toasted walnuts or pumpkin seeds for richness and crunch.',
        tip='Rinse canned lentils thoroughly under cold water to remove excess sodium and canning brine, then drain well before simmering with olive oil and spices.',
        allergens='Contains milk (goat cheese / feta).',
        extra='Delicious served as a standalone warm lunch with sourdough toast, or spooned over roasted sweet potatoes for dinner.',
        related_notes=[],
    ),
    dict(
        slug='smashed-cucumber-edamame-bowl',
        title='Smashed cucumber, avocado & edamame crunch bowl',
        cat='CRUNCHY NO-COOK · PLANT PROTEIN',
        categories=['protein-forward', 'plant-forward', 'quick-easy', 'fresh-lunches'],
        primary_goal='A bright no-cook bowl with plant protein and crunch.',
        why_it_works='Smashing cucumbers fractures their surface, soaking up the ginger-sesame dressing much faster than clean slices. Avocado folded in last stays creamy and distinct.',
        img='edamame-bowl.png',
        alt='Smashed cucumber, avocado and edamame bowl with toasted sesame seeds',
        desc='Crisp smashed Persian cucumbers, buttery avocado, shelled edamame, and toasted sesame seeds tossed in a ginger-tamari vinaigrette.',
        serves='2',
        prep_time='12 min prep',
        total_time='12 min total',
        method='No-cook',
        difficulty='Very easy',
        time_estimate='12 min prep · 12 min total · No-cook',
        time_glance='~12 mins total',
        card_time='~12 mins',
        tested=False,
        ingredients=[
            '4 Persian mini cucumbers (approx. 300 g)',
            '1 cup (150 g) shelled edamame, thawed',
            '1 ripe avocado, diced',
            '2 scallions, thinly sliced',
            '1 tbsp tamari or low-sodium soy sauce',
            '1 tbsp toasted sesame oil',
            '1 tbsp rice vinegar',
            '½ tsp grated fresh ginger',
            '1 tsp maple syrup or honey',
            '1 tbsp toasted sesame seeds'
        ],
        steps=[
            ('Smash the cucumbers.', 'Place cucumbers on a cutting board. Use the flat side of a heavy chef knife or rolling pin to firmly smack them until split lengthwise. Cut diagonally into bite-sized jagged pieces.'),
            ('Whisk dressing.', 'In a small bowl, whisk together tamari, toasted sesame oil, rice vinegar, grated ginger, and maple syrup until emulsified.'),
            ('Combine bowl ingredients.', 'In a mixing bowl, toss smashed cucumbers, thawed edamame, and sliced scallions with the vinaigrette until well coated.'),
            ('Fold avocado and garnish.', 'Gently fold in diced avocado so it stays intact. Divide into portions, scatter toasted sesame seeds over top, and serve immediately.')
        ],
        swap='Add cold cubed firm tofu for extra protein. Swap rice vinegar for fresh lime juice if you prefer a sharper citrus punch.',
        tip='Smashing cucumbers fractures their cell walls and creates jagged edges, soaking up the ginger-sesame dressing ten times faster than clean slices.',
        allergens='Contains soy (tamari/edamame) and sesame (oil/seeds).',
        extra='Can be served over cold cooked soba noodles, brown rice, or crisp gem lettuce leaves for a heartier meal.',
        related_notes=['keep-salad-crisp'],
    ),
    dict(
        slug='garlic-butter-bean-mushroom-toast',
        title='Garlic butter white bean & mushroom toast',
        cat='COMFORT CLASSIC · SKILLET & TOAST',
        categories=['budget-friendly', 'protein-forward', 'plant-forward', 'pantry-meals', 'cozy-dinners'],
        primary_goal='A satisfying skillet toast with mushrooms and creamy beans.',
        why_it_works='Mushrooms browned dry (no early salt) develop deep caramel flavor. Mashing a third of the beans creates a creamy sauce while the rest stay whole and satisfying.',
        img='mushroom-toast.png',
        alt='Garlic butter white beans and mushrooms spooned over toasted sourdough bread',
        desc='Caramelized cremini mushrooms and buttery cannellini beans simmered in garlic, thyme, and white wine vinegar on thick crusty sourdough.',
        serves='2',
        prep_time='8 min prep',
        total_time='15 min total',
        method='One-pan',
        difficulty='Easy',
        time_estimate='8 min prep · 15 min total · One-pan',
        time_glance='~15 mins total',
        card_time='~15 mins',
        tested=False,
        ingredients=[
            '2 thick slices rustic sourdough bread',
            '1 tbsp unsalted butter or olive oil',
            '8 oz (225 g) cremini or button mushrooms, sliced',
            '2 garlic cloves, finely grated',
            '1 can (15 oz / 425 g) cannellini beans, rinsed and drained',
            '½ cup (120 ml) vegetable stock or water',
            '1 tsp fresh thyme leaves (or ¼ tsp dried thyme)',
            '1 tsp white wine vinegar or lemon juice',
            'Salt and cracked black pepper, to taste',
            '1 tbsp chopped fresh chives or flat-leaf parsley'
        ],
        steps=[
            ('Brown the mushrooms.', 'Melt butter in a large skillet over medium-high heat. Add sliced mushrooms in a single layer without moving for 3 minutes until deeply browned, then stir and cook 2 minutes more.'),
            ('Add garlic and herbs.', 'Turn heat down to medium. Add grated garlic and thyme; stir for 1 minute until fragrant.'),
            ('Simmer the beans.', 'Stir in the drained cannellini beans and stock. Bring to a simmer for 4 minutes. Lightly crush about one third of the beans with the back of a fork to create a creamy sauce.'),
            ('Toast and assemble.', 'Toast the sourdough slices until deeply golden. Stir white wine vinegar, salt, and pepper into the beans. Spoon generously over hot toast and garnish with chopped chives.')
        ],
        swap='Use olive oil instead of butter for a completely dairy-free version. Any hearty beans (butter beans, great northern) work wonderfully.',
        tip='Do not salt the mushrooms until after they have browned in the skillet! Salting early draws out moisture and steams them instead of creating deep caramelized flavor.',
        allergens='Contains wheat (sourdough). Contains milk if butter is used.',
        extra='A poached or fried runny egg on top turns this into a satisfying weekend brunch.',
        related_notes=['make-beans-creamy'],
    ),
    dict(
        slug='spiced-apple-cinnamon-porridge',
        title='Spiced apple & cinnamon porridge',
        cat='WARM MORNINGS · STOVETOP COMFORT',
        categories=['budget-friendly', 'plant-forward', 'make-ahead', 'cozy-dinners'],
        primary_goal='A warming stovetop porridge with spiced apples.',
        why_it_works='Cooking the diced apples in butter and cinnamon first caramelizes their natural sugars before the oats go in, giving the whole bowl a warm bakery depth rather than a plain sweetness.',
        img='porridge.png',
        alt='Spiced apple and cinnamon porridge in a bowl topped with toasted pecans',
        desc='Toasted oats simmered with warm cinnamon, nutmeg, diced crisp apples, and finished with toasted pecans and maple syrup.',
        serves='2',
        prep_time='5 min prep',
        total_time='20 min total',
        method='Stovetop',
        difficulty='Easy',
        time_estimate='5 min prep · 20 min total · Stovetop',
        time_glance='~20 mins total',
        card_time='~20 mins',
        tested=False,
        ingredients=[
            '1 cup (90 g) quick-cooking steel-cut or rolled oats',
            '1 cup (240 ml) water',
            '1 cup (240 ml) whole milk or unsweetened almond milk',
            '1 crisp sweet apple (such as Honeycrisp or Gala), diced',
            '1 tbsp unsalted butter or coconut oil',
            '1 tsp ground cinnamon',
            '⅛ tsp ground nutmeg',
            'Pinch of fine sea salt',
            '2 tbsp pure maple syrup',
            '2 tbsp chopped toasted pecans or walnuts'
        ],
        steps=[
            ('Sauté spiced apples.', 'Melt butter in a medium saucepan over medium heat. Add diced apple and ½ tsp of the cinnamon. Cook for 3–4 minutes until apple starts to soften slightly at edges.'),
            ('Cook the porridge.', 'Add oats, water, milk, remaining ½ tsp cinnamon, nutmeg, and a pinch of salt to the saucepan. Stir well and bring to a gentle bubble.'),
            ('Simmer until thick.', 'Reduce heat to low and simmer, stirring frequently, for 10–12 minutes until oats are tender and porridge is thick and creamy. (5 minutes if using rolled oats).'),
            ('Serve with toppings.', 'Ladle into serving bowls. Drizzle each with maple syrup and finish with chopped toasted pecans for crunch.')
        ],
        swap='Swap diced pears for the apple. In summer, substitute fresh peaches or berries. For extra protein, swirl in a tablespoon of chia seeds or almond butter.',
        tip='Gently cooking the diced apples in melted butter and cinnamon before simmering with the oats caramelizes the natural sugars and infuses the entire bowl with warm bakery aroma.',
        allergens='Contains milk (butter/milk) and tree nuts (pecans) if used. Oats may contain cross-contact gluten unless certified gluten-free.',
        extra='Makes great meal prep: double the batch and reheat portions through the week with an extra splash of warm milk.',
        related_notes=[],
    ),
    dict(
        slug='5-minute-blender-hummus',
        tested=False,
        title='5-Minute Blender Hummus',
        cat='NO TAHINI · FIVE MINUTES',
        categories=['one-ingredient-different-ways', 'budget-friendly', 'quick-easy'],
        primary_goal='Canned chickpeas, one blender, five minutes. No tahini required.',
        why_it_works='Using just a few everyday ingredients and adjusting the water creates a creamy texture without tahini.',
        img='hummus.webp',
        alt='A shallow bowl of creamy blended hummus with a swirl on top, a drizzle of olive oil pooling in the center',
        desc='Canned chickpeas, one blender, five minutes. No tahini required.',
        serves='4',
        prep_time='5 min prep',
        total_time='5 min total',
        method='No-cook',
        difficulty='Very easy',
        time_estimate='5 min prep · 5 min total · No-cook',
        time_glance='~5 mins total',
        card_time='~5 mins',
        ingredients=[
            '1 can (15 oz / 425 g) chickpeas, drained',
            '2 tbsp olive oil',
            '1 garlic clove',
            'Juice of ½ lemon',
            '¼ cup water (adjust to texture)',
            'Salt to taste'
        ],
        steps=[
            ('Blend until smooth.', 'Blend everything until nearly smooth, adding water gradually until you reach the texture you want.'),
            ('Taste and adjust.', 'Taste and adjust salt or lemon before serving.')
        ],
        swap='Add 1 tbsp tahini if you have it — this version skips it on purpose to keep the ingredient list short.',
        tip='Add the water gradually to control how thick or loose the hummus gets.',
        allergens='None standard. Check all ingredient labels.',
        extra='Serve with fresh vegetables or warm pita bread.',
        related_notes=[],
    ),
    dict(
        slug='oven-roasted-crispy-chickpeas',
        tested=False,
        title='Oven-Roasted Crispy Chickpeas',
        cat='OVEN-ROASTED · SAVORY SNACK',
        categories=['one-ingredient-different-ways', 'budget-friendly', 'plant-forward'],
        primary_goal='The same can of chickpeas, crisped in the oven until they snap.',
        why_it_works='Drying the chickpeas thoroughly before roasting removes surface moisture, allowing them to crisp up properly rather than steaming.',
        img='roasted-chickpeas.webp',
        alt='A small bowl of golden, visibly crisp roasted chickpeas with a light dusting of paprika',
        desc='The same can of chickpeas, crisped in the oven until they snap.',
        serves='2',
        prep_time='5 min prep',
        total_time='30 min total',
        method='Oven',
        difficulty='Easy',
        time_estimate='5 min prep · 30 min total · Oven',
        time_glance='~30 mins total',
        card_time='~30 mins',
        ingredients=[
            '1 can (15 oz / 425 g) chickpeas, drained and thoroughly dried',
            '1 tbsp olive oil',
            'Salt to taste',
            'Pinch of paprika (optional)'
        ],
        steps=[
            ('Dry thoroughly.', 'Dry the chickpeas thoroughly before roasting — this is what makes them crisp instead of soft.'),
            ('Roast until crisp.', 'Roast at 425°F/220°C for about 25-30 minutes, shaking the pan halfway through.'),
            ('Season immediately.', 'Season immediately after they come out of the oven, while still hot.')
        ],
        swap='Try smoked paprika, cumin, or a pinch of cayenne for a different flavor profile.',
        tip='The more carefully you dry the chickpeas with a clean towel, the crispier they will become in the oven.',
        allergens='None standard. Check all ingredient labels.',
        extra='Eat them on their own as a snack or scatter them over salads for extra crunch.',
        related_notes=[],
    )
]

BASE_URL = 'https://boredoftoast.com'

def og_meta_tags(title, desc, url, image_url, width=1200, height=900):
    return f'<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(desc, quote=True)}"><meta property="og:url" content="{html.escape(url, quote=True)}"><meta property="og:site_name" content="Bored of Toast"><meta property="og:image" content="{html.escape(image_url, quote=True)}"><meta property="og:image:width" content="{width}"><meta property="og:image:height" content="{height}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title, quote=True)}"><meta name="twitter:description" content="{html.escape(desc, quote=True)}"><meta name="twitter:image" content="{html.escape(image_url, quote=True)}">'

def page(path, title, desc, body, active='', canonical_path=None, jsonld=None, og_img=None):
    nav = ''.join(
        f'<a href="{url}" ' + ('aria-current="page"' if key == active else '') + f'>{label}</a>'
        for key, url, label in [
            ('home', '/', 'Home'),
            ('recipes', '/recipes/', 'Recipes'),
            ('product', '/the-lunch-edit/', 'The Lunch Edit'),
            ('about', '/about/', 'About Us')
        ]
    )
    # Canonical URL
    if canonical_path is None:
        canonical_path = str(path).replace('\\', '/')
    canonical_url = f'{BASE_URL}/{canonical_path}/' if canonical_path else f'{BASE_URL}/'
    canonical_tag = f'<link rel="canonical" href="{html.escape(canonical_url, quote=True)}">'

    # JSON-LD block
    jsonld_tag = ''
    if jsonld:
        jsonld_str = json.dumps(jsonld, ensure_ascii=False).replace('<', '\\u003c')
        jsonld_tag = f'<script type="application/ld+json">{jsonld_str}</script>'

    # Open Graph block
    width, height = 1200, 900
    if og_img:
        image_name = og_img.rsplit('.', 1)[0]
        if (AS / f"{image_name}-1200.webp").exists():
            image_url = f"{BASE_URL}/assets/{image_name}-1200.webp"
        else:
            image_url = f"{BASE_URL}/assets/{og_img}"
    else:
        image_url = f"{BASE_URL}/assets/logo.png"
        width, height = 210, 90

    og_tags = og_meta_tags(title, desc, canonical_url, image_url, width, height)

    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — Bored of Toast</title><meta name="description" content="{html.escape(desc, quote=True)}">{canonical_tag}{og_tags}<meta name="theme-color" content="#124de3"><link rel="icon" href="/assets/mascot.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&family=DM+Sans:wght@400;500;600;700;800&family=DM+Serif+Display:ital@0;1&family=Manrope:wght@500;600;700;800&display=swap"><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/refinements.css"><link rel="stylesheet" href="/recipe.css">{jsonld_tag}</head><body><a class="skip" href="#main">Skip to content</a><header><div class="navwrap"><a class="brand" href="/" aria-label="Bored of Toast home"><img src="/assets/logo.png" alt="Bored of Toast" width="210" height="90"></a><nav aria-label="Main navigation">{nav}</nav><a class="header-note" href="/about/">A little curiosity<br>goes a long way.</a></div></header><main id="main">{body}</main><footer><div class="footer-statement wrap"><img src="/assets/mascot.png" alt="" width="76" height="76" loading="lazy"><p>See you in<br>the kitchen<span>.</span></p><a class="text-link" href="/recipes/">Browse all 10 recipes ↗</a></div><div class="footer-inner"><div><strong>Bored of Toast</strong><p>Everyday ingredients. Better meals.</p></div><div class="footer-links"><a href="/start-here/">Start here</a><a href="/about/">About &amp; editorial approach</a><a href="/the-lunch-edit/">The Lunch Edit</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy Policy</a><a href="/terms/">Terms of Use</a><span>© 2026 Bored of Toast</span></div></div></footer><script src="/recipe-engine.js" defer></script><script src="/site.js" defer></script><script src="/pilot.js" defer></script></body></html>'''
    # Use pre-generated responsive images; building the site needs no image tool.
    def responsive_image(match):
        tag = match.group(0)
        src = re.search(r'src="/assets/([^"/]+)\.png"', tag)
        if not src or not (AS / (src[1] + '-800.webp')).exists():
            return tag
        name = src[1]
        tag = tag.replace(src[0], f'src="/assets/{name}-800.webp"')
        sizes = '(max-width: 700px) calc(100vw - 40px), (max-width: 960px) 46vw, 600px'
        return tag[:-1] + f' srcset="/assets/{name}-480.webp 480w, /assets/{name}-800.webp 800w, /assets/{name}-1200.webp 1200w" sizes="{sizes}" decoding="async">'
    doc = re.sub(r'<img\b[^>]*>', responsive_image, doc)
    dest = OUT / path / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding='utf-8')

def build_recipe_jsonld(r):
    """Build a JSON-LD Recipe object using only confirmed data."""
    model_data = MODELS.get(r['slug']) or {}
    ingredients_raw = r.get('ingredients', [])
    ingredient_list = []
    for item in ingredients_raw:
        text = item['text'] if isinstance(item, dict) else item
        if text.startswith('SECTION:'):
            continue
        ingredient_list.append(text)

    steps_raw = r.get('steps', [])
    instructions = []
    for i, step in enumerate(steps_raw):
        title, action = step if isinstance(step, tuple) else (step.get('title', ''), step.get('action', ''))
        instructions.append({
            '@type': 'HowToStep',
            'name': title,
            'text': action
        })

    img_name = r.get('img', '').replace('.png', '')
    images = []
    for size in ['1200', '800', '480']:
        webp = AS / f'{img_name}-{size}.webp'
        if webp.exists() and webp.stat().st_size > 0:
            images.append(f'{BASE_URL}/assets/{img_name}-{size}.webp')

    ld = {
        '@context': 'https://schema.org',
        '@type': 'Recipe',
        'name': r['title'],
        'description': r['desc'],
        'recipeIngredient': ingredient_list,
        'recipeInstructions': instructions,
        'prepTime': f'PT{r.get("prep_time","").replace(" min prep","").replace("~","").strip()}M' if 'min' in r.get('prep_time', '') else None,
        'totalTime': f'PT{r.get("total_time","").replace(" min total","").replace("~","").strip()}M' if 'min' in r.get('total_time', '') else None,
        'recipeYield': f'Serves {r.get("serves", 2)}',
        'recipeCategory': [CAT_LABEL.get(c, c) for c in r.get('categories', [])[:2]],
        'image': images if images else None,
        'author': {'@type': 'Organization', 'name': 'Bored of Toast'},
        'datePublished': '2026-09-14',
    }
    # Remove None values
    ld = {k: v for k, v in ld.items() if v is not None}
    return ld

def card(r, i, featured=False):
    idx_str = f"0{i}" if i < 10 else str(i)
    if r.get('img'):
        media_html = f'<div class="card-image"><img src="/assets/{r["img"]}" alt="{html.escape(r["alt"], quote=True)}" loading="lazy" width="800" height="600"><span class="number">{idx_str}</span></div>'
    else:
        media_html = f'''<div class="card-image card-placeholder" aria-label="{html.escape(r["alt"], quote=True)}"><div class="placeholder-art"><div class="placeholder-badge"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></div><span class="placeholder-status">IN DEVELOPMENT</span><span class="placeholder-note">Serving illustration in progress</span></div><span class="number">{idx_str}</span></div>'''

    status_tag = '' if r.get('tested', False) else '<span class="dev-badge">Development edition</span>'

    # Primary category label for the card
    cats = r.get('categories', [])
    primary_cat_label = CAT_LABEL.get(cats[0], '') if cats else ''
    primary_cat_slug = cats[0] if cats else ''

    # data-categories attribute for JS filtering (space-separated slugs)
    cats_attr = ' '.join(cats)

    card_class = 'recipe-card'
    featured_label = ''

    # Card meta line
    card_meta = f'<span class="card-meta-cat">{html.escape(primary_cat_label)}</span>' if primary_cat_label else ''

    return f'''<article class="{card_class}" data-categories="{cats_attr}"><a href="/recipes/{r['slug']}/" aria-label="{html.escape(r['title'])}"><div class="card-image-wrap">{media_html}</div><div class="card-copy"><p class="eyebrow">{featured_label}{r['cat']} {status_tag}</p>{card_meta}<h3>{r['title']}</h3><p>{r['desc']}</p><div class="card-bottom"><span>Serves {r['serves']} <span aria-hidden="true">·</span> {r['card_time']} <span aria-hidden="true">·</span> {r['method']}</span><span class="text-link">The recipe <span aria-hidden="true">↗</span></span></div></div></a></article>'''


# ---------------------------------------------------------------------------
# Helper: build category filter pills HTML
# ---------------------------------------------------------------------------
def build_filter_pills():
    pills = '<li><a class="cat-pill is-active" href="/recipes/" id="cat-all" aria-current="true">All recipes</a></li>'
    for c in CATEGORIES:
        count = sum(1 for r in recipes if c['slug'] in r.get('categories', []))
        pills += f'<li><a class="cat-pill" href="/recipes/?category={c["slug"]}" id="cat-{c["slug"]}">{html.escape(c["label"])} <span class="pill-count">({count})</span></a></li>'
    return f'<ul class="cat-filter-list" role="list">{pills}</ul>'


# ---------------------------------------------------------------------------
# Helper: build Home "Find your next meal" category grid
# ---------------------------------------------------------------------------
def build_category_section():
    items = ''
    for c in CATEGORIES:
        count = sum(1 for r in recipes if c['slug'] in r.get('categories', []))
        noun = 'recipe' if count == 1 else 'recipes'
        count_label = f'{count} {noun}' if count > 0 else 'Coming soon'
        items += f'<a class="cat-card" href="/recipes/?category={c["slug"]}" id="home-cat-{c["slug"]}"><span class="cat-card-label">{html.escape(c["label"])}</span><span class="cat-card-desc">{html.escape(c["desc"])}</span><span class="cat-card-count">{count_label}</span></a>'
    return f'''<section class="wrap section cat-browse" id="browse-by-category">
  <div class="section-top">
    <div>
      <p class="eyebrow">03 / FIND YOUR NEXT MEAL</p>
      <h2>Browse by <span class="serif-accent">what you need.</span></h2>
    </div>
    <p>From quick weeknight dinners to make-ahead breakfasts — find the right recipe for right now.</p>
  </div>
  <div class="cat-grid">{items}</div>
  <p class="cat-browse-note"><a class="text-link" href="/recipes/">See all 10 recipes ↗</a></p>
</section>'''

# ---------------------------------------------------------------------------
# Helper: editorial transparency block
# ---------------------------------------------------------------------------
def editorial_transparency(compact=False):
    if compact:
        return '''<p class="editorial-note">Recipe development edition · Tested recipes are marked; new recipes await kitchen testing. Food images are AI-generated serving illustrations. <a href="/about/#editorial">Our editorial approach</a></p>'''
    return '''<section class="transparency-block wrap" aria-label="Editorial transparency">
  <div class="transparency-inner">
    <p class="eyebrow">A NOTE ON HOW THIS SITE WORKS</p>
    <h2>What you should know.</h2>
    <ul class="transparency-list">
      <li><strong>Development recipes.</strong> All ten recipes are in development and await kitchen testing. Times and yields are estimates, not guarantees.</li>
      <li><strong>AI-generated images.</strong> Food photos on this site are illustrative images generated with AI. They do not show tested results.</li>
      <li><strong>Substitutions are suggestions.</strong> Substitution notes describe what may change — they are editorial suggestions, not tested equivalents.</li>
      <li><strong>No nutritional claims.</strong> We do not provide nutritional data, calorie counts, or health claims.</li>
      <li><strong>No medical advice.</strong> Recipes are not medical or dietary advice. Consult a qualified professional for health-related guidance.</li>
    </ul>
    <a class="text-link" href="/about/#editorial">Full editorial approach ↗</a>
  </div>
</section>'''

# ---------------------------------------------------------------------------
# Helper: The Lunch Edit CTA (contextual, post-content)
# ---------------------------------------------------------------------------
def lunch_edit_cta():
    return '''<aside class="lunch-edit-cta" aria-label="About The Lunch Edit">
  <p class="eyebrow">ON THE BACK BURNER</p>
  <h3>The Lunch Edit</h3>
  <p>A digital collection in development: four flexible weeks of lunches, twenty recipes, and coordinated shopping lists. Not available yet — we'll update this page when it's ready.</p>
  <a class="text-link" href="/the-lunch-edit/">A peek at the idea ↗</a>
</aside>'''

# ---------------------------------------------------------------------------
# 0. /recipes/ index page
# ---------------------------------------------------------------------------
def build_recipe_index():
    all_cards = ''.join(card(r, i + 1, featured=(i == 0)) for i, r in enumerate(recipes))
    filter_pills = build_filter_pills()
    body = f'''
<section class="wrap recipe-index-header">
  <div class="recipe-index-top">
    <div>
      <p class="eyebrow">THE RECIPE NOTEBOOK</p>
      <h1>Find your next meal.</h1>
    </div>
    <p class="recipe-index-intro">Ten everyday recipes for fresh lunches, warm skillet dinners and make-ahead mornings. Use the filters to find what suits your day.</p>
  </div>
</section>
<section class="wrap recipe-index-body">
  <nav class="cat-filter" aria-label="Filter recipes by category">
    <p class="cat-filter-label" id="filter-label">Browse by:</p>
    {filter_pills}
  </nav>
  <noscript>
    <p class="noscript-note">Showing all recipes. Enable JavaScript to filter by category without leaving this page.</p>
  </noscript>
  <div class="recipe-index-status" aria-live="polite" aria-atomic="true">
    <p class="active-filter-label" id="active-filter-label">All 10 recipes</p>
    <p class="active-cat-desc" id="active-cat-desc" hidden></p>
  </div>
  <div class="recipe-grid" id="recipe-grid">{all_cards}</div>
  <div class="empty-state" id="empty-state" hidden aria-live="polite">
    <div class="empty-state-inner">
      <span class="empty-state-icon" aria-hidden="true">&#128203;</span>
      <h2>No recipes in this category yet.</h2>
      <p>This section will grow as the recipe collection expands. In the meantime, <a href="/recipes/">browse all 10 recipes</a>.</p>
    </div>
  </div>
  {editorial_transparency(compact=True)}
</section>
'''
    page(
        'recipes',
        'All recipes',
        'Browse all ten everyday recipes. Filter by Quick & Easy, Budget-Friendly, Plant-Forward, Make-Ahead and more.',
        body,
        'recipes',
        canonical_path='recipes'
    )

build_recipe_index()

# ---------------------------------------------------------------------------
# 1. Home page
# ---------------------------------------------------------------------------
page(
    '',
    'Everyday ingredients. Better meals.',
    'Easy everyday recipes, practical kitchen notes, portion adjustments and useful substitutions.',
    f'''
<section class="hero wrap">
  <div class="hero-copy">
    <p class="eyebrow"><span class="edition-mark" aria-hidden="true">01</span> THE EVERYDAY KITCHEN</p>
    <h1>Same kitchen.<br><span class="title-flourish">Fresh ideas.</span></h1>
    <p class="lead">Good food starts with what you have. Simple recipes, a little curiosity, and plenty of reasons to look forward to lunch.</p>
    <a class="button" href="#recipes">Find your next meal <span aria-hidden="true">↘</span></a>
    <p class="hero-note">Familiar ingredients. A different kind of everyday.</p>
  </div>
  <div class="hero-visual">
    <span class="hand-note">A little less "this again?"</span>
    <a class="hero-feature" href="/recipes/lemon-chickpea-salad/">
      <img src="/assets/chickpea.png" alt="Illustrated serving suggestion for lemon chickpea salad" fetchpriority="high" width="900" height="675">
      <div class="feature-label">
        <div>
          <span class="eyebrow">IN THE NOTEBOOK / 01</span>
          <h2>Lemon chickpea salad</h2>
          <p>Crunchy. Lemony. Ready for a fork.</p>
        </div>
        <span class="feature-arrow" aria-hidden="true">↗</span>
      </div>
    </a>
    <span class="hero-stamp">EVERYDAY<br><b>looks good.</b></span>
    <span class="photo-caption">Serving illustration · Recipe in development</span>
  </div>
</section>
<div class="ribbon">
  <span>Everyday ingredients.</span>
  <span aria-hidden="true">✳</span>
  <span>Room to improvise.</span>
  <span aria-hidden="true">✳</span>
  <span>Portion adjustment.</span>
  <span aria-hidden="true">✳</span>
  <span>Room to make it yours.</span>
</div>
<section class="wrap section" id="recipes">
  <div class="section-top">
    <div>
      <p class="eyebrow">01 / THE RECIPE NOTEBOOK</p>
      <h2>What sounds <span class="serif-accent">good?</span></h2>
    </div>
    <p>Ten everyday recipes for fresh lunches, warm skillet dinners, and make-ahead mornings.</p>
  </div>
  <div class="recipe-grid">{''.join(card(r, i + 1) for i, r in enumerate(recipes[:3]))}</div>
  <p><a class="text-link" href="/recipes/">View all 10 recipes ↗</a></p>
  {editorial_transparency(compact=True)}
</section>
{render_kitchen_home_feature()}
{build_category_section()}
<section class="wrap home-paths" id="start-here-paths">
  <div class="section-top">
    <div>
      <p class="eyebrow">04 / WHERE TO BEGIN</p>
      <h2>Start from <span class="serif-accent">where you are.</span></h2>
    </div>
    <p>Choose a direction and find recipes and techniques that fit right now.</p>
  </div>
  <div class="home-paths-grid">
    <a class="home-path-card" href="/start-here/#short-on-time">
      <span class="home-path-icon" aria-hidden="true">⏱</span>
      <strong>I'm short on time</strong>
      <span>No-cook lunches and make-ahead breakfasts.</span>
    </a>
    <a class="home-path-card" href="/start-here/#use-what-you-have">
      <span class="home-path-icon" aria-hidden="true">🥫</span>
      <strong>I want to use what I have</strong>
      <span>Pantry-first recipes built around beans and lentils.</span>
    </a>
    <a class="home-path-card" href="/start-here/#something-different">
      <span class="home-path-icon" aria-hidden="true">🥗</span>
      <strong>I want something different</strong>
      <span>Change the texture or format of familiar ingredients.</span>
    </a>
    <a class="home-path-card" href="/start-here/#more-protein">
      <span class="home-path-icon" aria-hidden="true">💪</span>
      <strong>I want more protein</strong>
      <span>Recipes centred on legumes and plant protein.</span>
    </a>
    <a class="home-path-card" href="/start-here/#more-vegetables">
      <span class="home-path-icon" aria-hidden="true">🥦</span>
      <strong>I want more vegetables</strong>
      <span>Plant-forward meals where vegetables take the lead.</span>
    </a>
  </div>
  <p><a class="text-link" href="/start-here/">All starting points ↗</a></p>
</section>
<section class="future-note wrap">
  <span class="eyebrow">ON THE BACK BURNER</span>
  <div>
    <h2>The Lunch Edit</h2>
    <p>A digital collection in development. Twenty recipes, four flexible weeks, and coordinated shopping lists. Not available yet.</p>
  </div>
  <a class="text-link" href="/the-lunch-edit/">A peek at the idea ↗</a>
</section>
''',
    'home',
    canonical_path='',
    og_img='chickpea.png'
)

# ---------------------------------------------------------------------------
# 2. All recipes use one editorial renderer.
# ---------------------------------------------------------------------------
for r in recipes:
    model = MODELS.get(r['slug']) or editorial_model(r, parse_ingredient)
    jsonld = build_recipe_jsonld(r)
    page(
        f'recipes/{r["slug"]}',
        r['title'],
        r['desc'],
        render_editorial_recipe({**r, 'editorial': model}, ''),
        'recipes',
        canonical_path=f'recipes/{r["slug"]}',
        jsonld=jsonld,
        og_img=r.get('img')
    )

# ---------------------------------------------------------------------------
# 3. Kitchen notes index and reusable technique guides (REMOVED - Diluted into Start Here)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 4. The Lunch Edit
# ---------------------------------------------------------------------------
page(
    'the-lunch-edit',
    'The Lunch Edit',
    'An upcoming digital collection: four flexible lunch weeks, twenty recipes and coordinated shopping lists.',
    '''
<section class="wrap product-hero">
  <div>
    <p class="eyebrow">BORED OF TOAST PRESENTS</p>
    <h1>Lunch, with<br>a little less<br>thinking.</h1>
    <p class="lead">The Lunch Edit brings everyday recipes and the shopping that goes with them into one useful digital collection.</p>
    <div class="price-line">
      <strong>$19</strong>
      <span>USD · planned one-time price</span>
    </div>
    <p class="status">In development · Not available to buy yet</p>
    <a class="button" href="#sample">Read the free sample ↓</a>
  </div>
  <div class="product-poster">
    <p>BORED OF TOAST / VOL. 01</p>
    <h2>THE<br>LUNCH<br>EDIT<span>.</span></h2>
    <div class="poster-bottom">
      <span>4 flexible weeks<br>20 everyday lunches</span>
      <span>A DIGITAL<br>KITCHEN COMPANION</span>
    </div>
  </div>
</section>
<section class="wrap section">
  <div class="section-top">
    <div>
      <p class="eyebrow">WHAT WE'RE PUTTING TOGETHER</p>
      <h2>From "what's for lunch?"<br>to a plan you can use.</h2>
    </div>
  </div>
  <div class="included-grid">
    <div>
      <span>01 / THE FOOD</span>
      <h3>20 lunch recipes</h3>
      <p>Clear ingredients, portions and substitutions, with US and metric measures. Kitchen testing is part of development before release.</p>
    </div>
    <div>
      <span>02 / THE ROUTINE</span>
      <h3>Four flexible weeks</h3>
      <p>Five lunch ideas per week, arranged around overlapping ingredients. Move meals around to suit your day.</p>
    </div>
    <div>
      <span>03 / THE SHOPPING</span>
      <h3>Lists that match</h3>
      <p>Weekly shopping lists separated into fresh ingredients and pantry items, plus a blank page for your own changes.</p>
    </div>
    <div>
      <span>04 / THE FORMAT</span>
      <h3>Easy to keep nearby</h3>
      <p>A PDF designed for phone reading, with simple printable recipe and shopping pages. A single purchase, with no subscription planned.</p>
    </div>
  </div>
</section>
<section class="sample-section" id="sample">
  <div class="wrap">
    <p class="eyebrow">A FREE LOOK AT THE APPROACH</p>
    <h2>Two lunches.<br>One small shop.</h2>
    <p class="sample-intro">This development sample shows how ingredients can overlap. Make one two-serving recipe on each cooking day; it gives two people one lunch, or lets you share the extra portion.</p>
    <div class="sample-grid">
      <div class="sample-day">
        <span>COOKING DAY 01</span>
        <h3>Lemon chickpea salad</h3>
        <p>Chickpeas, cucumber and tomatoes with feta, parsley and lemon.</p>
        <a class="text-link" href="/recipes/lemon-chickpea-salad/">Open the complete recipe ↗</a>
      </div>
      <div class="sample-day">
        <span>COOKING DAY 02</span>
        <h3>Lemony white beans &amp; spinach</h3>
        <p>A warm skillet that reuses the olive oil and lemon from the first lunch.</p>
        <a class="text-link" href="/recipes/lemon-white-bean-skillet/">Open the complete recipe ↗</a>
      </div>
    </div>
    <div class="shopping">
      <div>
        <h3>The shared shopping list</h3>
        <p>For both recipes at their stated two-serving yields. Check your pantry first.</p>
        <button class="button outline" type="button" data-print>Print this sample</button>
      </div>
      <ul>
        <li>1 can chickpeas + 1 can white beans (15 oz / 425 g each)</li>
        <li>150 g cucumber + 150 g cherry tomatoes</li>
        <li>90 g baby spinach + 2 garlic cloves</li>
        <li>50 g feta + ¼ cup chopped parsley</li>
        <li>1–2 lemons, to yield 3 tbsp juice</li>
        <li>2 slices of bread</li>
        <li>Pantry: 3 tbsp olive oil, ¼ tsp oregano, salt and pepper</li>
      </ul>
    </div>
    <p class="small">Sample recipes await kitchen testing. The complete product is still in development; no payment is being collected.</p>
  </div>
</section>
<section class="wrap article-section narrow">
  <h2>Who is it for?</h2>
  <p>Home cooks who want a little more variety at lunch and appreciate having the recipes and shopping worked out together. The planned first edition focuses on vegetable-forward everyday meals.</p>
  <h2>Will the free recipes stay free?</h2>
  <p>Yes. Our website recipes include the ingredients and method. The paid collection will add coordinated weeks, shopping lists and a convenient printable format.</p>
  <h2>When can I buy it?</h2>
  <p>After recipe testing, photography and the finished PDF are complete. We will update this page when it is ready. There is no checkout or pre-order at this stage.</p>
</section>
''',
    'product',
    canonical_path='the-lunch-edit',
    og_img='read-the-recipe.webp'
)

# ---------------------------------------------------------------------------
# 5. About page
# ---------------------------------------------------------------------------
page(
    'about',
    'About & Editorial Approach',
    'How Bored of Toast develops, tests and photographs recipes for everyday cooking.',
    '''
<article class="article wrap">
  <p class="eyebrow">THE MISSION</p>
  <h1>Saving lunches from<br>boring sandwiches.</h1>
  <p class="lead">Bored of Toast was born in the exact moment you look at your kitchen pantry and think: <em>"surely there's something else I can make."</em></p>
  
  <style>
    @keyframes subtleFloat {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-8px); }
    }
  </style>
  <div class="side-note" style="margin-top: 40px; display: flex; gap: 30px; align-items: center; flex-wrap: wrap;">
    <img src="/assets/mascot.png" alt="Bored of Toast Mascot" style="width: 140px; border-radius: 50%; background: #fff; padding: 10px; animation: subtleFloat 4s ease-in-out infinite;">
    <div style="flex: 1; min-width: 250px;">
      <h3 style="margin-bottom: 10px;">Meet the Mascot</h3>
      <p style="margin-bottom: 0;">This is the "Bored Toast". It represents everyone who is tired of eating the exact same meal every single day. We are here to change that expression into a smile, using simple ingredients you already have.</p>
    </div>
  </div>

  <section class="article-section" id="philosophy">
    <h2>Our Philosophy</h2>
    <p>We believe cooking shouldn't be stressful. We don't use 20 pans, and we don't ask you to buy ingredients you will only use once. Our focus is on <strong>pantry staples, speed, and practicality</strong>.</p>
    <p>Breakfast, lunch, and dinner all belong here. Our name is a nudge to try something different—though, of course, a good piece of toast is always welcome.</p>
  </section>

  <section class="article-section" id="editorial">
    <h2>Our editorial approach</h2>
    <p>This is the development edition of the site. All ten recipes are in development and await kitchen testing. We label development status transparently on each recipe card and will update quantities, yields and methods as kitchen testing concludes.</p>
    <p>Food images in this edition are AI-generated serving illustrations. They are not photographs of tested results. The goal for the public recipe collection is to replace them with authentic photographs from kitchen preparation.</p>
    
    <div class="callout" style="margin-top: 30px;">
      <h3 style="margin-bottom: 15px;">What you should know</h3>
      <ul style="margin: 0; padding-left: 20px; line-height: 1.8;">
        <li><strong>Development recipes.</strong> All recipes await kitchen testing. Times, yields, and results may change.</li>
        <li><strong>AI-generated images.</strong> Food photos are illustrative. They are not photographs of tested dishes.</li>
        <li><strong>Substitutions are editorial suggestions.</strong> They describe what may change — they are not tested equivalents.</li>
        <li><strong>No nutritional claims.</strong> We do not provide calorie counts, macronutrient data, or health claims.</li>
        <li><strong>No medical advice.</strong> Content is not medical or dietary advice.</li>
      </ul>
    </div>
  </section>
  <div style="margin-top: 50px;">
    <a class="button" href="/#recipes">Back to the recipes ↗</a>
  </div>
</article>
''',
    'about',
    canonical_path='about',
    og_img='read-the-recipe.webp'
)


# ---------------------------------------------------------------------------
# 7. Contact page
# ---------------------------------------------------------------------------
page(
    'contact',
    'Contact & Kitchen Inquiries',
    'Editorial contact guidelines and development status for Bored of Toast.',
    '''
<article class="article wrap">
  <p class="eyebrow">GET IN TOUCH</p>
  <h1>Contact &amp;<br>kitchen inquiries.</h1>
  <p class="lead">Bored of Toast is currently in active recipe formulation and digital development.</p>

  <section class="article-section">
    <h2>Contact channels in development</h2>
    <p>Bored of Toast is in an early prototype and recipe drafting stage. Public email inboxes (such as <code>editorial@boredoftoast.com</code>) are not yet live or monitored.</p>
    <div style="background:#fefbf2;border:1px solid #eadeb8;padding:20px 24px;border-radius:3px;margin:24px 0;border-left:4px solid var(--yellow);">
      <p style="font-family:'Manrope',sans-serif;font-weight:700;font-size:1.05rem;color:#5a420e;margin:0;">No active inbox during development</p>
      <p style="font-size:0.9rem;color:#675122;margin:6px 0 0;">To prevent missed messages or unfulfilled inquiries, direct inbox reception is disabled until recipes pass kitchen verification. Public contact channels will open alongside the general release.</p>
    </div>

    <h2>Recipe feedback &amp; future kitchen tests</h2>
    <p>When our testing phase opens for home cooks, we will provide a dedicated web feedback form to submit cooking notes, oven calibration observations, and ingredient swap results.</p>

    <h2>Press &amp; partnerships</h2>
    <p>Bored of Toast is independently produced. We do not accept paid product placements or undisclosed sponsored content. Partnership inquiries may be directed to the editorial inbox once it opens.</p>
  </section>

  <a class="button" href="/">Back to home ↗</a>
</article>
''',
    '',
    canonical_path='contact'
)

# ---------------------------------------------------------------------------
# 8. Privacy Policy page
# ---------------------------------------------------------------------------
page(
    'privacy',
    'Privacy Policy',
    'How Bored of Toast handles visitor privacy, session storage, and cookie-free browsing.',
    '''
<article class="article wrap">
  <p class="eyebrow">LEGAL &amp; TRANSPARENCY</p>
  <h1>Privacy policy.</h1>
  <p class="lead">We believe recipes should be simple to read without ad banners, behavioral surveillance, or third-party trackers following you around the web.</p>

  <section class="article-section">
    <h2>Zero third-party tracking</h2>
    <p>Bored of Toast does not use Google Analytics, Facebook Pixels, marketing beacons, or third-party tracking cookies. We do not sell, rent, or trade visitor data under any circumstances.</p>

    <h2>Local browser storage (sessionStorage)</h2>
    <p>Our website provides interactive convenience features designed to help you cook:</p>
    <ul>
      <li><strong>Interactive ingredient checklist:</strong> When you check off an ingredient on a recipe page, your checked state is saved in your browser's temporary <code>sessionStorage</code> so it stays intact if you refresh or switch tabs.</li>
    </ul>
    <p><strong>Crucially:</strong> All of this data stays strictly inside your web browser on your own device. It is never transmitted to our servers or any third party, and it is automatically erased when you close your browser tab.</p>

    <h2>Contact regarding privacy</h2>
    <p>During this prototype phase, no visitor accounts, analytics, or user profiling exist. Dedicated privacy contact channels will open when the site launches publicly.</p>
  </section>

  <a class="button" href="/">Back to home ↗</a>
</article>
''',
    '',
    canonical_path='privacy'
)

# ---------------------------------------------------------------------------
# 9. Terms of Use page
# ---------------------------------------------------------------------------
page(
    'terms',
    'Terms of Use',
    'Terms and conditions for using Bored of Toast recipes, kitchen notes, and content.',
    '''
<article class="article wrap">
  <p class="eyebrow">LEGAL &amp; TRANSPARENCY</p>
  <h1>Terms of use.</h1>
  <p class="lead">By using Bored of Toast, you agree to these simple terms and common-sense kitchen safety guidelines.</p>

  <section class="article-section">
    <h2>Recipe development &amp; kitchen safety</h2>
    <p>Recipes on Bored of Toast are created for culinary inspiration and personal home cooking. While we take great care in developing proportions and methods, cooking times and temperatures are estimates that can vary based on individual cookware, oven calibration, stove power, and ingredient freshness.</p>
    <p>Home cooks are responsible for exercising safe food handling practices, including proper refrigeration, safe cooking temperatures, and thorough hand washing.</p>

    <h2>Allergies &amp; dietary restrictions</h2>
    <p>We list major known allergens (such as dairy, wheat, soy, sesame, and nuts) alongside our recipes as a convenience. However, food manufacturers frequently update formulation and packaging. Always inspect ingredient packaging directly to verify allergens and cross-contamination risks.</p>

    <h2>Intellectual property</h2>
    <p>All written text, recipe methods, graphic layouts, and brand assets on Bored of Toast are copyright © 2026 Bored of Toast. You are warmly welcome to print copies for your own personal home cooking. Republishing our full recipes or selling our digital content without written permission is prohibited.</p>

    <h2>Changes to these terms</h2>
    <p>We may update these terms occasionally to reflect new features or editorial updates. Continued use of the website represents acceptance of current terms.</p>
  </section>

  <a class="button" href="/">Back to home ↗</a>
</article>
''',
    '',
    canonical_path='terms'
)

# ---------------------------------------------------------------------------
# 10. Technical SEO: sitemap.xml and robots.txt
# ---------------------------------------------------------------------------
from kitchen_notes import GUIDES, guide, index
for g in GUIDES:
    slug = g['slug']
    page(
        f'kitchen-notes/{slug}',
        g['title'],
        g['intro'],
        guide(g),
        'kitchen-notes',
        canonical_path=f'kitchen-notes/{slug}',
        og_img=g.get('image')
    )

# Kitchen notes index
page(
    'kitchen-notes',
    'Kitchen Notes',
    'Practical guides for everyday cooking.',
    index(),
    'kitchen-notes',
    canonical_path='kitchen-notes'
)

canonical_routes = [
    '',
    'recipes/',
    'kitchen-notes/',
    'the-lunch-edit/',
    'about/',
    'contact/',
    'privacy/',
    'terms/'
] + [f'recipes/{r["slug"]}/' for r in recipes] + [f'kitchen-notes/{g["slug"]}/' for g in GUIDES]

sitemap_xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]
for route in canonical_routes:
    url = f"{BASE_URL}/{route}"
    priority = '1.0' if route == '' else ('0.9' if route == 'recipes/' else ('0.8' if route.startswith('recipes/') or route.startswith('kitchen-notes/') else '0.7'))
    sitemap_xml_lines.append(
        f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-09-14</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{priority}</priority>\n  </url>'
    )
sitemap_xml_lines.append('</urlset>')

(OUT / 'sitemap.xml').write_text('\n'.join(sitemap_xml_lines), encoding='utf-8')

robots_txt = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
(OUT / 'robots.txt').write_text(robots_txt, encoding='utf-8')

print(f"Successfully generated all content: {len(canonical_routes)} routes, sitemap.xml, and robots.txt.")
