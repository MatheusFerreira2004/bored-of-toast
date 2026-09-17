"""How long prepped plant food keeps, fridge and freezer.

Published storage charts are built around meat, dairy and eggs. That is
where the acute risk sits, so it makes sense, but it leaves a
plant-forward kitchen guessing about the things it actually cooks in
batches: pulses, grains, dips, roasted vegetables, dressed salads.

The useful finding while pulling this together is that the ingredient is
often the wrong variable. A cooked chickpea and a dressed chickpea have
very different working lives, and the difference is salt and acid pulling
water out of everything around them. That is a texture failure long
before it is a safety one, which is why the chart splits components from
assembled dishes.

Fridge and freezer figures are FoodSafety.gov and USDA FSIS values for
storage at or below 40 F / 4 C and 0 F / -18 C. Freezer figures are
quality windows, not safety limits; food held at 0 F stays safe
indefinitely.

Note on the safety block: reference_content._safety() reads 'intro' and
'items' (a list of label/value pairs), not free-form paragraphs. Getting
that shape wrong raises inside body() and the page is silently skipped.
"""

SLUG = 'food-storage-chart'

PAGE = dict(
    title='Food Storage Chart',
    h1='How long it actually keeps.',
    dek='Most storage charts are built around meat and dairy. This one '
        'covers what a batch-cooking plant kitchen actually has in the '
        'fridge on Wednesday.',
    description='Fridge and freezer storage times for cooked pulses, '
                'grains, dips, tofu and prepped vegetables, with the '
                'dressed-versus-undressed rule that matters more than the '
                'ingredient.',
    intro=[
        'Search for a food storage chart and you will get meat, poultry, '
        'dairy and eggs. That is where the acute risk lives, so the '
        'emphasis is fair. It is also close to useless if what you have in '
        'the fridge is a container of lentils, a jar of dressing and half '
        'a tray of roasted vegetables.',
        'The thing that turns out to matter most is not which pulse or '
        'which grain. It is whether the food has been dressed. Salt and '
        'acid pull water out of everything they touch, so a bowl that was '
        'crisp on Sunday is sitting in liquid by Tuesday. Same chickpeas, '
        'half the working life.',
        'So the tables below separate plain cooked components from '
        'assembled dishes, and the exceptions section covers the two '
        'genuine safety outliers in a plant kitchen that the generic '
        'charts skip entirely.',
    ],
    rule=dict(
        eyebrow='THE SHORT VERSION',
        items=[
            ('Plain cooked components', '3 to 4 days'),
            ('Dressed and assembled', '1 to 2 days'),
            ('Into the fridge within', '2 hours of cooking'),
        ],
        example='Cooked chickpeas keep 3 to 4 days plain. Dress them with '
                'lemon and salt and you have 1 to 2 days before the '
                'cucumber goes limp and the bowl is sitting in liquid. '
                'Storing the dressing separately and combining at the last '
                'minute is the whole trick.',
    ),
    tables=[dict(
        heading='Cooked components, undressed',
        note='These are the batch-cook staples: cooked plain, drained, '
             'cooled quickly and stored in a shallow covered container. '
             'Freezer figures are quality windows, not safety limits.',
        caption='Stored at or below 40 F / 4 C. Freezer figures assume '
                '0 F / -18 C.',
        headers=['Component', 'Fridge', 'Freezer', 'What fails first'],
        highlight=1,
        rows=[
            ['Beans and lentils, cooked', '3 to 4 days', '6 months',
             'Skins split, texture turns mealy'],
            ['Grains: rice, quinoa, farro', '3 to 4 days', '1 to 2 months',
             'Dries out and hardens; see rice note below'],
            ['Pasta, cooked and plain', '3 to 5 days', '1 to 2 months',
             'Clumps, absorbs any sauce unevenly'],
            ['Roasted vegetables', '3 to 4 days', '10 to 12 months',
             'Loses all crispness within a day'],
            ['Steamed or boiled vegetables', '3 to 4 days', '10 to 12 months',
             'Waterlogs, colour dulls'],
            ['Tofu, opened, in fresh water', '3 to 5 days', '5 months',
             'Sours; change the water daily'],
            ['Tempeh, opened', '5 to 7 days', '4 months',
             'Dark spots are normal, sour smell is not'],
            ['Cooked tofu or tempeh', '3 to 4 days', '2 to 3 months',
             'Texture turns spongy on reheating'],
            ['Hard-boiled eggs, in shell', '1 week', 'Not recommended',
             'Whites turn rubbery; freezing ruins them'],
        ],
    ), dict(
        heading='Assembled and dressed',
        note='Anything with dressing, salt or acid already on it. These '
             'windows are shorter than the sum of their parts, and the '
             'limit is almost always texture rather than safety.',
        caption='Stored at or below 40 F / 4 C. Dressed salads do not '
                'freeze usefully.',
        headers=['Dish', 'Fridge', 'Keeps better if', 'What fails first'],
        highlight=1,
        rows=[
            ['Bean salad, dressed', '1 to 2 days',
             'Dressing stored separately', 'Vegetables weep, bowl waterlogs'],
            ['Grain bowl, dressed', '1 to 2 days',
             'Components kept apart', 'Grains absorb dressing, go soggy'],
            ['Leafy salad, dressed', 'Same day',
             'Dressed at the table', 'Leaves collapse within hours'],
            ['Washed greens, undressed', '3 to 5 days',
             'Dried fully, paper towel in the box', 'Slimy edges'],
            ['Cut fruit', '3 to 5 days',
             'Stored dry, not in its own juice', 'Browning, softening'],
            ['Soups and stews', '3 to 4 days', 'Cooled in shallow layers',
             'Fine for days; flavour often improves'],
            ['Hummus and bean dips, homemade', '3 to 4 days',
             'Thin layer of oil on top', 'Surface dries and darkens'],
            ['Hummus, store-bought, opened', '7 days',
             'Lid on, back of the fridge', 'Watery separation'],
            ['Vinaigrette, homemade', '1 to 2 weeks',
             'No fresh garlic or herbs in it', 'Separates; shake and use'],
            ['Overnight oats', '3 to 4 days',
             'Fruit added the morning of', 'Oats keep absorbing, turn stodgy'],
        ],
    )],
    exceptions=[
        ('Dressed is a different food than undressed', [
            'This is the single most useful thing on the page. Salt and '
            'acid draw water out of cell walls, which is exactly why a '
            'salted cucumber weeps within minutes. In a dressed bowl that '
            'process does not stop in the fridge, it just slows down.',
            'The fix is not a better container. It is storing the dressing '
            'in a separate jar and combining portions as you eat them. '
            'Three to four days becomes genuinely achievable, and the last '
            'portion tastes like the first.',
        ]),
        ('Cooked rice is the real outlier', [
            'Uncooked rice commonly carries Bacillus cereus spores, which '
            'survive cooking. Left at room temperature they germinate and '
            'produce a toxin that reheating does not destroy. This is the '
            'one place in a plant-forward kitchen where the usual '
            'two-hour rule is worth tightening.',
            'Cool cooked rice as fast as you can, ideally into the fridge '
            'within an hour, spread in a shallow layer rather than left in '
            'the pot. Reheat it once, until steaming hot throughout, and '
            'do not reheat a second time.',
        ]),
        ('Garlic in oil needs refrigeration and a short leash', [
            'Fresh garlic held in oil at room temperature is a recognised '
            'botulism risk: the oil excludes oxygen, and garlic carries '
            'the spores. This catches people out because it looks and '
            'smells completely normal.',
            'Refrigerate any oil infused with fresh garlic or fresh herbs, '
            'and use it within four days. Commercial versions are '
            'acidified to be shelf-stable; a jar you made on Sunday is '
            'not. A dressing with garlic in it belongs in the fridge and '
            'on a shorter clock than the 1 to 2 weeks above.',
        ]),
        ('Freezer dates are about quality, not safety', [
            'Food held at a steady 0 F / -18 C stays safe indefinitely. '
            'Every freezer figure in the tables above is the point where '
            'texture and flavour start to noticeably decline, not a point '
            'where the food becomes unsafe.',
            'Cooked pulses freeze genuinely well, which makes them worth '
            'batching. Cooked grains are more fragile; freeze them '
            'slightly undercooked if you can, and they hold up better on '
            'reheating.',
        ]),
        ('Cool it fast, in shallow containers', [
            'A deep container of hot stew can sit in the bacterial danger '
            'zone for hours in the middle even with the fridge door shut. '
            'The two-hour rule assumes the food is actually cooling, not '
            'insulating itself.',
            'Divide large batches into shallow containers before they go '
            'in. It is the difference between food that was refrigerated '
            'and food that merely ended up in a fridge.',
        ]),
    ],
    safety=dict(
        heading='The two-hour rule',
        intro='Bacteria multiply fastest between 40 F and 140 F / 4 C and '
              '60 C, which the USDA calls the danger zone. Cooked food '
              'should not sit in it for more than two hours in total, '
              'counting the time it spent cooling on the counter.',
        items=[
            ('Refrigerate within', '2 hours of cooking'),
            ('Above 90 F / 32 C', '1 hour, not two'),
            ('Fridge temperature', 'At or below 40 F / 4 C'),
            ('Freezer temperature', '0 F / -18 C'),
            ('Cooked rice', 'Into the fridge within 1 hour, reheat once only'),
            ('Garlic or herbs in oil', 'Refrigerated, 4 days maximum'),
        ],
        outro='When in doubt, throw it out. Food that has been mishandled '
              'can look, smell and taste completely normal, and no amount '
              'of reheating destroys a toxin that has already formed. '
              'Check the fridge with a thermometer rather than trusting '
              'the dial.',
    ),
    sources=[
        ('Cold Food Storage Chart', 'FoodSafety.gov, U.S. Department of '
         'Health and Human Services',
         'https://www.foodsafety.gov/food-safety-charts/cold-food-storage-charts',
         'Primary source for the fridge and freezer windows in both '
         'tables.'),
        ('Refrigeration and Food Safety', 'USDA Food Safety and Inspection '
         'Service',
         'https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/refrigeration',
         'Source for the two-hour rule, the danger zone range and the '
         'shallow-container cooling guidance.'),
        ('FoodKeeper', 'USDA and Cornell University',
         'https://www.foodsafety.gov/keep-food-safe/foodkeeper-app',
         'Cross-checked the per-item windows, including opened tofu and '
         'store-bought dips.'),
        ('Reheating rice and Bacillus cereus', 'UK Food Standards Agency',
         'https://www.food.gov.uk/safety-hygiene/cooking-your-food',
         'Source for the cooked rice exception and the reheat-once '
         'guidance.'),
        ('Garlic in oil and botulism risk', 'U.S. Food and Drug '
         'Administration',
         'https://www.fda.gov/food/buy-store-serve-safe-food/refrigerator-thermometers-cold-facts-about-food-safety',
         'Basis for the four-day refrigerated limit on fresh garlic held '
         'in oil.'),
    ],
    related=[
        ('/kitchen-notes/bean-cooking-chart/',
         'Bean cooking and conversion chart'),
        ('/kitchen-notes/can-to-cup-conversions/',
         'Can to cup conversions'),
        ('/recipes/lemon-chickpea-salad/',
         'Lemon chickpea salad, which keeps best undressed'),
        ('/recipes/5-minute-blender-hummus/', 'Five-minute blender hummus'),
        ('/recipes/blueberry-overnight-oats/', 'Blueberry overnight oats'),
    ],
)
