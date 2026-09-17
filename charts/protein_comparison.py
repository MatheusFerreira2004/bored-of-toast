"""Plant protein, per cup and per calorie.

Published protein charts almost all rank by protein per cooked cup, which
quietly flatters legumes: a cup of cooked lentils weighs close to 200 g,
while a cup of tofu weighs less and a cup of edamame less again. Ranked
by weight or by calorie the order changes, and soy foods move well ahead.

Neither ranking is wrong. They answer different questions, so both
columns are in the first table. The per-calorie column is the one that
matters if the portion is what is fixed, which is usually the case in a
bowl or a salad.

Protein and calorie figures are USDA FoodData Central values for cooked,
unsalted preparations, rounded to the nearest gram. Protein per 100
calories is computed from those two figures and rounded to one decimal.
"""

SLUG = 'plant-protein-comparison'

PAGE = dict(
    title='Plant Protein Comparison',
    h1='Which of these actually has the protein.',
    dek='Lentils win per cup. Tofu and tempeh win per calorie. Which of '
        'those matters depends on whether you are filling a bowl or '
        'counting a day.',
    description='Protein in cooked legumes, soy foods and grains, compared '
                'per cup, per 100 grams and per 100 calories, with pairings '
                'for complete protein.',
    intro=[
        'Almost every protein chart ranks plants by grams per cooked cup. '
        'That is the number you want when you are building a bowl, but it '
        'hides something: a cup of cooked lentils weighs nearly 200 grams, '
        'a cup of shelled edamame about 155. Same measuring cup, very '
        'different amount of food.',
        'Rank the same list by weight, or by calorie, and soy foods move '
        'clearly ahead of the pulses. Neither ranking is more honest than '
        'the other. They answer different questions, so both are below.',
        'The practical version: if you are adding a scoop to a salad, read '
        'the per-cup column. If the portion is fixed and you are trying to '
        'get more protein into it without more food, read the per-calorie '
        'column.',
    ],
    rule=dict(
        eyebrow='THE SHORT VERSION',
        items=[
            ('Cooked pulses', '15 to 18 g protein per cup'),
            ('Soy foods', 'Roughly double that, gram for gram'),
            ('Complete on their own', 'Soy, quinoa, hemp, buckwheat'),
        ],
        example='A cup of cooked lentils gives 18 g of protein for 230 '
                'calories. A cup of firm tofu gives about 39 g for 320. Per '
                'cup the tofu wins outright; per calorie it is still ahead, '
                'but the lentils bring 15 g of fibre that the tofu does not.',
    ),
    tables=[dict(
        heading='Pulses, cooked',
        note='Values are for beans and lentils cooked without salt and '
             'drained. Canned versions carry the same protein; the '
             'difference is sodium, which draining and rinsing cuts by '
             'roughly 40 per cent.',
        caption='One cup cooked, drained. Protein per 100 calories in the '
                'highlighted column.',
        headers=['Pulse', 'Protein per cup', 'Calories',
                 'Protein per 100 cal', 'Fibre per cup'],
        highlight=3,
        rows=[
            ['Lentils, brown or green', '18 g', '230', '7.8 g', '16 g'],
            ['White beans, cannellini', '17 g', '249', '6.8 g', '11 g'],
            ['Split peas', '16 g', '231', '6.9 g', '16 g'],
            ['Black beans', '15 g', '227', '6.6 g', '15 g'],
            ['Chickpeas', '15 g', '269', '5.6 g', '12 g'],
            ['Kidney beans, red', '15 g', '225', '6.7 g', '13 g'],
            ['Pinto beans', '15 g', '245', '6.1 g', '15 g'],
            ['Navy beans', '15 g', '255', '5.9 g', '19 g'],
            ['Green peas', '8 g', '134', '6.0 g', '9 g'],
        ],
    ), dict(
        heading='Soy foods',
        note='These are the plant proteins that behave like animal protein '
             'on a nutrition label: complete amino acid profile, and far '
             'more protein per gram than any pulse. Tofu protein varies a '
             'lot with firmness, so the label on the block beats any chart.',
        caption='Protein density is where soy separates from the pulses.',
        headers=['Food', 'Protein per 100 g', 'Protein per cup',
                 'Protein per 100 cal', 'Note'],
        highlight=1,
        rows=[
            ['Tempeh', '20 g', 'About 34 g', '10.6 g',
             'Highest of the three, fermented'],
            ['Tofu, extra firm', '17 to 19 g', 'About 39 g', '12.0 g',
             'Check the block, brands vary widely'],
            ['Tofu, firm', '17 g', 'About 35 g', '12.0 g',
             'Calcium-set blocks are also high in calcium'],
            ['Edamame, shelled', '12 g', '18 g', '9.5 g',
             'Most fibre of the soy foods'],
            ['Tofu, silken', '5 to 8 g', 'About 15 g', '9.0 g',
             'Much lower, it is mostly water'],
            ['Soybeans, mature, cooked', '17 g', '29 g', '9.3 g',
             'The whole bean, rarely used directly'],
        ],
    ), dict(
        heading='Grains, seeds and pantry add-ons',
        note='None of these carry a meal on their own, but a couple of '
             'tablespoons of the denser ones close the gap on a bowl that is '
             'short on protein. Hemp and pumpkin seeds do the most per '
             'spoonful.',
        caption='What a realistic portion adds.',
        headers=['Food', 'Portion', 'Protein', 'Complete?'],
        highlight=2,
        rows=[
            ['Seitan', '100 g', '25 g', 'No, low in lysine'],
            ['Hemp seeds, hulled', '3 tbsp', '10 g', 'Yes'],
            ['Peanut butter', '2 tbsp', '7 g', 'No'],
            ['Pumpkin seeds', '\u00bc cup', '9 g', 'No'],
            ['Nutritional yeast', '2 tbsp', '8 g', 'Yes'],
            ['Quinoa, cooked', '1 cup', '8 g', 'Yes'],
            ['Buckwheat, cooked', '1 cup', '6 g', 'Yes'],
            ['Tahini', '2 tbsp', '5 g', 'No'],
            ['Whole wheat pasta, cooked', '1 cup', '7 g', 'No'],
            ['Brown rice, cooked', '1 cup', '5 g', 'No'],
        ],
    )],
    exceptions=[
        ('Per cup is the wrong lens for tofu',
         ['A measuring cup of cubed tofu and a measuring cup of cooked '
          'lentils are not comparable portions of food. The lentils are '
          'denser and heavier, which is why they look competitive in '
          'per-cup charts and fall behind in per-gram ones.',
          'If you are swapping one for the other in a recipe, match by '
          'weight rather than volume. Around 150 g of tofu replaces a '
          'drained can of beans reasonably closely on protein, though not '
          'on fibre.']),
        ('Complete protein matters less than it sounds',
         ['Pulses are low in methionine and grains are low in lysine, which '
          'is where the old advice to combine them at every meal came from. '
          'That advice has since been relaxed: what matters is the range '
          'over a day, not the pairing on a single plate.',
          'It is still a reason the classic combinations work. Beans with '
          'rice, chickpeas with couscous, lentils with bread, hummus with '
          'pita \u2014 all of them cover both gaps, and all of them predate '
          'anyone knowing why.']),
        ('Canned and dried carry the same protein',
         ['Canning does not meaningfully change protein content. A drained '
          '15 oz can of chickpeas gives about 1\u00bd cups, so roughly 22 g '
          'of protein, the same as cooking \u2154 cup dried.',
          'The differences are sodium, which rinsing cuts by around 40 per '
          'cent, and texture. Cost favours dried by a wide margin.']),
        ('Sprouting and fermenting change absorption, not the number',
         ['Pulses contain phytates and tannins that bind minerals and '
          'slightly reduce how much protein the body takes up. Soaking, '
          'sprouting and fermenting all reduce them.',
          'This is part of why tempeh sits well with people who find beans '
          'heavy. The protein figure on the label does not move, but more of '
          'it becomes available.']),
    ],
    safety=None,
    sources=[
        ('Legumes and Legume Products', 'USDA FoodData Central',
         'https://fdc.nal.usda.gov/',
         'Protein, calorie and fibre values for every cooked pulse in the '
         'first table.'),
        ('Nutrients: Protein', 'USDA National Agricultural Library',
         'https://www.nal.usda.gov/sites/default/files/page-files/Protein.pdf',
         'Per-serving protein reference used to cross-check the pulse and '
         'tofu figures.'),
        ('Legume Nutrition Comparison', 'Food & Nutrition Magazine',
         'https://foodandnutrition.com/legume-nutrition-comparison/',
         'Cooked cup weights, which are the basis for the per-cup versus '
         'per-gram discrepancy.'),
        ('Protein Sources Reference', 'Food & Nutrition Magazine',
         'https://foodandnutrition.com/protein-sources-reference/',
         'Half-cup figures for firm tofu and tempeh, and the caution against '
         'reading per-cup charts as a density ranking.'),
        ('Tofu vs Tempeh vs Edamame', 'Nextrient',
         'https://nextrient.com/blog/tofu-vs-tempeh-vs-edamame',
         'Per 100 g protein, calories and fibre for the three soy foods, and '
         'the completeness of their amino acid profiles.'),
        ('Plant-Based Protein Chart', 'ProteinCalc',
         'https://myproteincalc.com/learn/food-protein-charts/plant-proteins',
         'Seitan, hemp seed and nutritional yeast figures in the third '
         'table.'),
    ],
    related=[
        ('/recipes/mediterranean-warm-green-lentils/',
         'Mediterranean warm green lentils'),
        ('/recipes/smashed-cucumber-edamame-bowl/',
         'Smashed cucumber and edamame bowl'),
        ('/recipes/lemon-white-bean-skillet/', 'Lemon white bean skillet'),
        ('/recipes/lemon-chickpea-salad/', 'Lemon chickpea salad'),
        ('/kitchen-notes/bean-cooking-chart/',
         'Bean cooking and conversion chart'),
    ],
)
