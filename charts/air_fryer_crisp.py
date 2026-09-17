"""Why food does not crisp in an air fryer.

The common fix is to turn the temperature up, and it is the wrong one.
Crisping is a drying process: water has to leave the surface before
browning can start. Raising the heat browns the outside faster but does
not remove water any faster, so the result is a dark, soft crust.

Everything in this note comes back to two variables the dial does not
control: how wet the surface is when it goes in, and whether air can
reach all of it. Both are fixable without changing the recipe.

Temperatures and times are for basket-style air fryers, which run hotter
at the food than oven-style models because the fan sits closer.
"""

SLUG = 'why-food-does-not-crisp'

PAGE = dict(
    title='Why Food Does Not Crisp in an Air Fryer',
    h1='It is almost never the temperature.',
    dek='Crisping is drying. If the surface is wet or the basket is full, '
        'no amount of extra heat will fix it.',
    description='The four reasons food comes out soft in an air fryer, and '
                'what to change: surface moisture, crowding, coating choice '
                'and fat. With a crowding threshold and a coating table.',
    intro=[
        'An air fryer is a small convection oven with the fan close to the '
        'food. That proximity is the whole point: moving air strips the '
        'humid layer off the surface much faster than still oven air, which '
        'is why a basket browns in fifteen minutes what a sheet pan needs '
        'thirty for.',
        'It also means the machine has one job it does well and one it does '
        'badly. It dries surfaces beautifully. It cannot dry a surface that '
        'is being resupplied with water from underneath, and it cannot dry '
        'a surface the air never touches.',
        'Almost every soft result traces back to one of those two. The '
        'temperature dial is rarely the problem, and turning it up usually '
        'makes things worse: the outside darkens before the inside has '
        'given up its water, so you get colour without crunch.',
    ],
    rule=dict(
        eyebrow='THE SHORT VERSION',
        items=[
            ('Dry the surface', 'Pat with a towel until it stops dampening'),
            ('Single layer', 'Pieces touching is fine, stacked is not'),
            ('A little fat', 'One to two teaspoons per basket, tossed'),
        ],
        example='Chickpeas out of a can hold enough surface water to steam '
                'themselves for the first six or seven minutes. Rolled dry '
                'in a towel first, the same batch at the same temperature '
                'crisps in about two thirds the time.',
    ),
    tables=[dict(
        heading='Where the water is coming from',
        note='These are in the order worth checking. The first two account '
             'for most soft results, and both are fixed before the food '
             'goes in.',
        caption='Fix the source rather than extending the time.',
        headers=['Source', 'What it looks like', 'The fix'],
        highlight=2,
        rows=[
            ['Surface water',
             'Pale, no browning for the first several minutes',
             'Pat dry with a towel until it comes away dry'],
            ['Crowding',
             'Crisp edges, soft middles, uneven colour',
             'Single layer, or cook in two batches'],
            ['Marinade or sauce',
             'Dark patches, sticky rather than crisp',
             'Drain well, or sauce after cooking'],
            ['Frozen with ice glaze',
             'Steam in the first minutes, then slow browning',
             'Cook from frozen, do not thaw, add 3 to 5 minutes'],
            ['High-water vegetables',
             'Shrinks and softens instead of browning',
             'Salt and rest 15 minutes, then pat dry'],
        ],
    ), dict(
        heading='How full is too full',
        note='Crowding is the one that surprises people, because the basket '
             'looks like it has room. What matters is not volume but whether '
             'air can reach every surface. Pieces can touch; they cannot '
             'sit on each other.',
        caption='A rough guide by food type, for a standard basket.',
        headers=['Food', 'Works', 'Does not'],
        highlight=1,
        rows=[
            ['Chickpeas, small beans', 'One loose layer, gaps visible',
             'A heaped layer, even if it fits'],
            ['Cubed vegetables', 'Single layer, pieces touching',
             'Two layers, or piled in the middle'],
            ['Gnocchi', 'Single layer, shaken once',
             'Any stacking, they fuse together'],
            ['Halloumi, tofu', 'Spaced, not touching',
             'Touching, the contact faces stay pale'],
            ['Chips, wedges', 'Loose layer, shaken twice',
             'More than about two thirds full'],
        ],
    ), dict(
        heading='What actually crisps in dry heat',
        note='Wet batter needs immersion in oil to set. In an air fryer it '
             'drips through the basket before it can firm up. Dry coatings '
             'work because they only need to dehydrate, not fry.',
        caption='Coating behaviour is the difference between air frying and '
                'deep frying.',
        headers=['Coating', 'In an air fryer', 'Why'],
        highlight=1,
        rows=[
            ['Cornstarch or potato starch', 'Very good',
             'Dries to a thin glassy shell, no liquid to set'],
            ['Breadcrumbs, panko', 'Good, if pressed on and oiled',
             'Needs a little fat or it stays pale and dusty'],
            ['Semolina or fine polenta', 'Good',
             'Coarse and dry, browns readily'],
            ['Flour alone', 'Poor',
             'Stays raw-tasting and powdery without oil contact'],
            ['Wet batter', 'Does not work',
             'Drips off before it can set, needs immersion'],
            ['Nothing, just oil', 'Good on starchy foods',
             'The food\u2019s own starch is enough on potato or chickpea'],
        ],
    )],
    exceptions=[
        ('Turning the temperature up makes it worse',
         ['Browning and drying are separate processes that happen at '
          'different rates. Higher heat accelerates browning far more than '
          'it accelerates water loss, so the surface reaches the colour you '
          'want while still holding the moisture that keeps it soft.',
          'If something is browning too fast to crisp, the move is down and '
          'longer, not up and shorter. Dropping 25 degrees and adding five '
          'minutes fixes more soft results than any other single change.']),
        ('Preheating matters more here than in an oven',
         ['A cold basket spends its first minutes warming up, and during '
          'that time the food sits in humid air of its own making. Three to '
          'five minutes of preheating removes that window.',
          'This is most noticeable on small pieces with a lot of surface '
          'area \u2014 chickpeas, cubed vegetables, gnocchi \u2014 where the '
          'first few minutes are a large share of the total cook.']),
        ('Fat is not optional, but very little is needed',
         ['Air frying is not fat-free cooking; it is low-fat cooking. Some '
          'fat is needed to conduct heat into the surface and to carry '
          'browning reactions. Entirely dry food goes leathery rather than '
          'crisp.',
          'One to two teaspoons tossed through a whole basket is enough. '
          'Spraying is less effective than tossing, because the spray '
          'settles on the top faces only, and aerosol sprays can degrade '
          'non-stick baskets over time.']),
        ('Basket and oven models are not interchangeable',
         ['Basket models sit the fan a few centimetres from the food and run '
          'effectively hotter than the dial says. Oven-style models have '
          'more space and behave closer to a conventional convection oven.',
          'A recipe written for a basket, run in an oven-style model, '
          'usually needs the original time rather than a reduced one. Times '
          'in this note are for basket models.']),
    ],
    safety=dict(
        eyebrow='WORTH KNOWING',
        intro='Two things that come up often enough to be worth stating '
              'plainly.',
        items=[
            ('Parchment before the food',
             'Loose parchment can lift into the heating element. Put the '
             'food on it first, and only use perforated sheets.'),
            ('Doneness is temperature, not time',
             'Air fryer times vary widely between models. For anything '
             'where doneness matters, use a thermometer rather than the '
             'clock.'),
        ],
        source=('Air Fryer Safety', 'USDA Food Safety and Inspection '
                'Service', 'https://www.fsis.usda.gov/food-safety'),
    ),
    sources=[
        ('How Air Fryers Work', 'Serious Eats',
         'https://www.seriouseats.com/what-is-an-air-fryer',
         'The convection mechanism, and why fan proximity makes basket '
         'models behave hotter than the dial.'),
        ('Air Fryer Tips and Testing', 'America\u2019s Test Kitchen',
         'https://www.americastestkitchen.com/equipment_reviews/1970-air-fryers',
         'Crowding thresholds and the finding that tossing oil beats '
         'spraying it.'),
        ('Air Fryer Mistakes to Avoid', 'Taste of Home',
         'https://www.tasteofhome.com/collection/air-fryer-mistakes/',
         'The preheating window and the behaviour of wet batter in a '
         'perforated basket.'),
        ('Cooking Safely with an Air Fryer',
         'USDA Food Safety and Inspection Service',
         'https://www.fsis.usda.gov/food-safety',
         'Doneness by internal temperature rather than time, and the '
         'parchment caution.'),
    ],
    related=[
        ('/kitchen-notes/oven-to-air-fryer-conversion/',
         'Oven to air fryer conversion'),
        ('/recipes/oven-roasted-crispy-chickpeas/',
         'Oven-roasted crispy chickpeas'),
        ('/recipes/crispy-sheet-pan-gnocchi/', 'Crispy sheet pan gnocchi'),
        ('/kitchen-notes/what-the-pan-tells-you/',
         'What the pan tells you'),
    ],
)
