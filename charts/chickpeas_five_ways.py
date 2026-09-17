"""One ingredient, five methods: chickpeas.

A pillar page rather than a chart. The site already has three chickpea
recipes and two legume reference tables, and nothing tying them
together. This is the hub: it explains what changes between methods and
sends the reader to the recipe that matches what they want.

Worth building because it needs no new photography. It reuses recipes
that are already published, which is the bottleneck on everything else.

The useful finding while pulling this together is that the five methods
are not really five recipes. They are three decisions: how much surface
water you remove, whether the skins stay on, and when the acid goes in.
Everything else follows from those.

Contract note: reference_content._safety() reads heading, intro, items
(a list of label/value pairs) and outro. Getting that shape wrong raises
inside body() and the page is skipped. _exceptions() takes a list of
(heading, [paragraphs]) tuples and hardcodes the "Four exceptions"
wording, so give it exactly four.
"""

SLUG = 'chickpeas-five-ways'

PAGE = dict(
    title='Chickpeas, Five Ways',
    h1='One can, five different dinners.',
    dek='The same chickpeas go cold and crunchy, blended smooth, roasted '
        'crisp, warmed in a skillet or simmered soft. What changes is '
        'water, skins and timing.',
    description='Five methods for one can of chickpeas: salad, hummus, '
                'roasted, skillet and simmered. What each method needs, '
                'what it gives you, and which recipe to use.',
    intro=[
        'A can of chickpeas is the most flexible thing in a plant-forward '
        'pantry, and the least interesting if you only ever do one thing '
        'with it. The five methods below all start from the same 15 ounce '
        'can and end somewhere completely different.',
        'They are not really five techniques. They are three decisions. '
        'How much surface water you remove decides whether you get crisp '
        'or soft. Whether the skins stay on decides smooth or textured. '
        'When the acid goes in decides firm or creamy. Everything else '
        'follows from those.',
        'Pick the row that matches the texture you want, not the one that '
        'matches the time you have. The fastest method here takes ten '
        'minutes and the slowest takes forty, and the gap matters less '
        'than getting the texture right.',
    ],
    rule=dict(
        eyebrow='THE THREE DECISIONS',
        items=[
            ('Surface water', 'Dried off means crisp, left on means soft'),
            ('Skins', 'On for texture, off for anything smooth'),
            ('Acid', 'At the end for firm, early for creamy'),
        ],
        example='The same drained can, patted dry and roasted, gives you '
                'something you can eat with your fingers. Left wet and '
                'simmered with lemon from the start, it collapses into a '
                'sauce. Neither is wrong; they are answers to different '
                'questions.',
    ),
    tables=[dict(
        heading='The five methods',
        note='Active time is hands-on work, not total time. The roasted '
             'and air fryer methods are mostly waiting, which makes them '
             'the easiest to run alongside something else.',
        caption='One 15 oz can, drained, as the starting point for all '
                'five.',
        headers=['Method', 'Texture', 'Active time', 'Best for',
                 'Acid goes in'],
        highlight=1,
        rows=[
            ['Cold, in a salad', 'Firm, distinct', '10 min',
             'Lunch you make ahead', 'At the end'],
            ['Blended', 'Smooth, thick', '5 min',
             'Dips, spreads, sauces', 'Early, helps loosen'],
            ['Roasted', 'Crisp outside, soft in', '5 min plus 30 waiting',
             'Snacking, salad topping', 'After, or not at all'],
            ['Skillet, warm', 'Creamy, slightly crushed', '15 min',
             'Dinner on toast or grains', 'Last minute'],
            ['Simmered', 'Soft, starting to break', '25 min',
             'Soups, stews, braises', 'Early, with liquid'],
        ],
    ), dict(
        heading='What to start from',
        note='Canned is the default and there is no shame in it. Dried is '
             'cheaper and better tasting but needs planning. Jarred is a '
             'real upgrade if you can find it and do not mind the price.',
        caption='Same recipe, three starting points.',
        headers=['Form', 'Prep needed', 'Texture', 'Works best for'],
        highlight=2,
        rows=[
            ['Canned', 'Drain, rinse, pat dry', 'Reliable, slightly soft',
             'Any of the five methods'],
            ['Dried, cooked', 'Overnight soak, 90 to 120 min',
             'Firmer, nuttier', 'Salads and roasting, where it shows'],
            ['Jarred, Spanish or Italian', 'Drain only',
             'Creamiest of the three', 'Blending and skillet'],
            ['Dried, pressure cooked', 'Soak, then 35 to 40 min',
             'Close to jarred', 'Anything, if you own one'],
            ['Frozen, cooked', 'Thaw, pat dry', 'Softer, skins loosen',
             'Simmering and blending'],
        ],
    ), dict(
        heading='What goes wrong, by method',
        note='Each method fails in its own predictable way. Most of these '
             'are fixed before the chickpeas are heated at all.',
        caption='The common failure and what causes it.',
        headers=['Method', 'It went wrong if', 'The cause', 'The fix'],
        highlight=3,
        rows=[
            ['Salad', 'Watery by the next day',
             'Dressed too early', 'Keep the dressing separate'],
            ['Blended', 'Grainy, not smooth',
             'Skins left on', 'Peel, or cook 10 minutes longer'],
            ['Roasted', 'Soft, no crunch',
             'Surface water', 'Pat dry until the towel comes away dry'],
            ['Roasted', 'Crisp then soft in an hour',
             'Covered while warm', 'Cool uncovered, store loosely'],
            ['Skillet', 'Bounced around, stayed firm',
             'Pan too crowded to crush', 'Press some against the pan'],
            ['Simmered', 'Still firm after 30 minutes',
             'Acid added too early', 'Add lemon or tomato at the end'],
        ],
    )],
    exceptions=[
        ('The skins are the whole difference between smooth and grainy', [
            'Chickpea skins do not break down in a blender. They tear into '
            'small flat pieces that you feel on the tongue as grit, which '
            'is the single most common reason homemade hummus is not as '
            'smooth as the version in a good restaurant.',
            'Two ways around it. Rub the drained chickpeas between a folded '
            'towel and most of the skins come loose in about a minute, or '
            'simmer the canned chickpeas in water with a pinch of baking '
            'soda for ten minutes, which loosens the skins and softens '
            'the insides at the same time. For every other method on this '
            'page, leave the skins on: they hold the shape.',
        ]),
        ('Acid firms chickpeas, so timing is not optional', [
            'Lemon juice, vinegar and tomato all strengthen the cell walls '
            'of a legume. That is useful when you want the chickpeas to '
            'stay distinct in a salad, and it works against you when you '
            'want them to soften into a sauce.',
            'For anything cold and firm, dress at the end. For anything '
            'simmered and creamy, add the acid with the liquid and give it '
            'time. The one place this bites people is dried chickpeas '
            'cooked in a tomato base, which can stay stubbornly hard for '
            'well over two hours.',
        ]),
        ('Roasted chickpeas lose their crunch faster than anything else', [
            'A roasted chickpea is crisp because its surface is dry. It '
            'sits next to a soft, moist interior, and that water keeps '
            'migrating outward as it sits. Within a couple of hours in a '
            'sealed container the shell has gone leathery.',
            'Cool them completely uncovered, store loosely rather than '
            'airtight, and accept that they are best the day they are '
            'made. If you need them crisp for a salad the next day, five '
            'minutes back in a hot oven restores most of it.',
        ]),
        ('The liquid in the can is worth keeping', [
            'Aquafaba, the starchy liquid chickpeas are packed in, whips '
            'like egg white and thickens like a light roux. It is the one '
            'part of the can most people pour down the sink without '
            'thinking.',
            'Two tablespoons loosens a stiff hummus without thinning the '
            'flavour the way water does. It also holds a vinaigrette '
            'together. Drain it into a jar rather than the drain; it keeps '
            'three or four days in the fridge.',
        ]),
    ],
    safety=dict(
        heading='Raw chickpeas are not edible',
        intro='Unlike some pulses, chickpeas cannot be eaten raw or '
              'sprouted-and-uncooked. Dried chickpeas contain lectins and '
              'oligosaccharides that cause real digestive trouble and are '
              'only broken down by proper cooking. Canned chickpeas are '
              'already fully cooked.',
        items=[
            ('Canned', 'Cooked and ready, rinse and use'),
            ('Dried, soaked', 'Still raw, must be simmered until tender'),
            ('Dried, stovetop', '90 to 120 minutes after an overnight soak'),
            ('Dried, pressure cooker', '35 to 40 minutes after soaking'),
            ('Tender means', 'Crushes easily against the roof of the mouth'),
            ('Aquafaba', 'Only from cooked or canned chickpeas, never raw'),
        ],
        outro='A chickpea that is still firm in the centre is undercooked, '
              'not al dente. Give it more time rather than more heat, and '
              'hold back any acid until it is tender.',
    ),
    sources=[
        ('The Best Hummus Recipe', 'Serious Eats',
         'https://www.seriouseats.com/the-best-smooth-hummus-recipe',
         'Basis for the skin-removal and baking soda method, and why '
         'skins cause grittiness.'),
        ('Crispy Roasted Chickpeas', 'Love and Lemons',
         'https://www.loveandlemons.com/roasted-chickpeas/',
         'Drying the surface before roasting, and why they soften in a '
         'sealed container.'),
        ('How to Cook Beans', 'Serious Eats',
         'https://www.seriouseats.com/how-to-cook-beans',
         'Source for acid firming cell walls and the effect on cooking '
         'time.'),
        ('Chickpeas, mature seeds', 'USDA FoodData Central',
         'https://fdc.nal.usda.gov/',
         'Drained weights and cooked yields used in the starting-point '
         'table.'),
        ('Pulses and lectins', 'UK Food Standards Agency',
         'https://www.food.gov.uk/safety-hygiene/beans-and-pulses',
         'Basis for the note that dried chickpeas require full cooking.'),
    ],
    related=[
        ('/recipes/lemon-chickpea-salad/',
         'Lemon chickpea salad, the cold method'),
        ('/recipes/5-minute-blender-hummus/',
         'Five-minute blender hummus, the blended method'),
        ('/recipes/oven-roasted-crispy-chickpeas/',
         'Oven-roasted crispy chickpeas, the roasted method'),
        ('/kitchen-notes/bean-cooking-chart/',
         'Bean cooking chart, if you are starting from dried'),
        ('/kitchen-notes/can-to-cup-conversions/',
         'Can to cup conversions, for swapping between forms'),
        ('/kitchen-notes/why-food-does-not-crisp/',
         'Why food does not crisp, if the roasted ones came out soft'),
    ],
)
