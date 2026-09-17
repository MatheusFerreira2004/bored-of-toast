"""Reference pages: charts, conversions and comparison tables.

A third content format alongside recipes and kitchen notes. These pages
carry no cooking method, so they need no licensed food photography, which
is the bottleneck on new recipes. They also make strong Pinterest assets:
a table delivers its value inside the pin itself.

Structure per page:
    header -> intro -> rule block -> tables -> exceptions -> safety -> sources

Rendering only uses classes already defined in reference.css and the
existing stylesheets, so a reader cannot tell this is a new page type.

Schema is Article, not Recipe. These are not recipes, and marking them as
such would be incorrect structured data.
"""
from html import escape as esc

# ---------------------------------------------------------------------------
# Page data
# ---------------------------------------------------------------------------

PAGES = {}

PAGES['oven-to-air-fryer-conversion'] = dict(
    title='Oven to Air Fryer Conversion',
    h1='Oven to air fryer, without the guesswork.',
    dek='Lower the temperature, shorten the time, and start checking earlier '
        'than you think. The rule is simple. The exceptions are where most '
        'recipes go wrong.',
    description='Convert any oven recipe to an air fryer: reduce the '
                'temperature by 25°F and the time by about 20%, then start '
                'checking at three quarters of the way through.',
    intro=[
        'An air fryer is a small convection oven. A fan sits close to the '
        'food and moves hot air fast, which means two things: surfaces brown '
        'sooner, and moisture leaves quicker. That is why a recipe run '
        'straight from oven settings comes out dark outside and underdone in '
        'the middle.',
        'The fix is not complicated. Drop the temperature so the outside has '
        'time to catch up with the inside, and cut the time because the '
        'circulating air does more work per minute.',
    ],
    rule=dict(
        eyebrow='THE RULE',
        items=[
            ('Temperature', 'Reduce by 25°F, or about 15°C'),
            ('Time', 'Reduce by 20%, then check earlier'),
            ('First check', 'At 75% of the converted time'),
        ],
        example='A recipe calling for 400°F for 30 minutes becomes 375°F for '
                '24 minutes in an air fryer — and you open the basket at the '
                '18 minute mark to look.',
    ),
    tables=[dict(
        heading='Conversion table',
        note='Converted figures are a starting point. Air fryers vary more '
             'between models than ovens do, so the check column matters more '
             'than the time column.',
        caption='Oven setting on the left, air fryer equivalent on the right.',
        headers=['Oven temp', 'Air fryer temp', 'Oven time',
                 'Air fryer time', 'Start checking at'],
        highlight=4,
        rows=[
            ['325°F / 160°C', '300°F / 150°C', '20 min', '16 min', '12 min'],
            ['325°F / 160°C', '300°F / 150°C', '30 min', '24 min', '18 min'],
            ['350°F / 175°C', '325°F / 160°C', '15 min', '12 min', '9 min'],
            ['350°F / 175°C', '325°F / 160°C', '25 min', '20 min', '15 min'],
            ['350°F / 175°C', '325°F / 160°C', '40 min', '32 min', '24 min'],
            ['375°F / 190°C', '350°F / 175°C', '20 min', '16 min', '12 min'],
            ['375°F / 190°C', '350°F / 175°C', '35 min', '28 min', '21 min'],
            ['400°F / 200°C', '375°F / 190°C', '15 min', '12 min', '9 min'],
            ['400°F / 200°C', '375°F / 190°C', '25 min', '20 min', '15 min'],
            ['400°F / 200°C', '375°F / 190°C', '30 min', '24 min', '18 min'],
            ['425°F / 220°C', '400°F / 200°C', '20 min', '16 min', '12 min'],
            ['425°F / 220°C', '400°F / 200°C', '30 min', '24 min', '18 min'],
            ['450°F / 230°C', '425°F / 220°C', '15 min', '12 min', '9 min'],
            ['450°F / 230°C', '425°F / 220°C', '25 min', '20 min', '15 min'],
        ],
    )],
    exceptions=[
        ('Your oven is already a convection oven',
         ['If the recipe was written for a convection or fan oven, most of '
          'the adjustment is already built in. Reduce by 10 to 15°F rather '
          'than the full 25°F, and keep the time reduction closer to 10%.',
          'Recipes that mention a fan setting, or give two temperatures, were '
          'almost certainly written this way.']),
        ('Basket models run hotter than oven-style models',
         ['A basket air fryer sits the food directly in the airflow. An '
          'oven-style model with racks behaves more like a small convection '
          'oven and heats less aggressively.',
          'With a basket, take the full 20% off the time. With an oven-style '
          'model, start at 10 to 15% and adjust from there.']),
        ('A crowded basket needs longer, not hotter',
         ['Air fryers work by moving air around the food. Fill the basket and '
          'the air has nowhere to go, so the pieces steam instead of crisping.',
          'If you cannot leave gaps, add 3 to 5 minutes and shake halfway '
          'through. Do not raise the temperature to compensate — the outside '
          'will darken while the middle stays soft.']),
        ('Frozen food keeps its package temperature',
         ['Instructions on frozen packaging are usually written for a '
          'conventional oven, but frozen food behaves differently: it starts '
          'far below room temperature and releases water as it thaws.',
          'Keep the temperature on the package and cut the time by about 20%. '
          'Do not lower the heat as well, or the surface will never dry '
          'enough to crisp.']),
    ],
    safety=dict(
        heading='Cook to temperature, not to the clock',
        intro='Conversion charts estimate time. Only a thermometer confirms '
              'that food is safely cooked. The USDA minimum internal '
              'temperatures are:',
        items=[
            ('Poultry, whole or ground', '165°F / 74°C'),
            ('Ground meats other than poultry', '160°F / 71°C'),
            ('Beef, pork, lamb and veal, whole cuts',
             '145°F / 63°C, then rest 3 minutes'),
            ('Fish and shellfish', '145°F / 63°C'),
            ('Leftovers and casseroles', '165°F / 74°C'),
        ],
        outro='Check the thickest part, away from bone.',
    ),
    sources=[
        ('Air Fryer Conversion Chart', 'Taste of Home',
         'https://www.tasteofhome.com/article/air-fryer-conversion-chart/',
         'Basis for the 25°F and 20% reduction, and the distinction between '
         'basket and oven-style models.'),
        ('How to Use an Air Fryer', 'Serious Eats',
         'https://www.seriouseats.com/how-to-use-an-air-fryer-11685276',
         'On why crowding the basket prevents browning.'),
        ('Safe Minimum Internal Temperatures',
         'USDA Food Safety and Inspection Service',
         'https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart',
         'Source for every temperature in the safety block.'),
        ('Air Fryer Cooking Times', 'Bon Appétit',
         'https://www.bonappetit.com/story/air-fryer-cooking-times',
         'Cross-checked the converted times for vegetables and legumes.'),
    ],
    related=[
        ('/recipes/oven-roasted-crispy-chickpeas/',
         'Oven-roasted crispy chickpeas'),
        ('/recipes/crispy-sheet-pan-gnocchi/', 'Crispy sheet-pan gnocchi'),
    ],
)

PAGES['bean-cooking-chart'] = dict(
    title='Bean Cooking & Conversion Chart',
    h1='Every bean, and how long it actually takes.',
    dek='Soaking times, cooking times, and what a cup of dried beans really '
        'gives you once cooked. Plus the conversion nobody agrees on.',
    description='Cooking and soaking times for 15 beans and legumes, plus '
                'dried-to-cooked yields and how much dried bean equals one '
                'can.',
    intro=[
        'Dried beans cost a fraction of canned and taste better, but the '
        'timing is the part that stops people. Cooking times published '
        'online vary wildly, largely because they depend on how old the '
        'beans are and how hard your water is.',
        'The ranges below are wide on purpose. Start checking at the low end.',
    ],
    rule=dict(
        eyebrow='THE CONVERSION',
        items=[
            ('1 cup dried', 'Yields 2½ to 3 cups cooked'),
            ('One 15 oz can', 'Gives about 1½ cups drained'),
            ('To replace a can', 'Cook ⅔ cup dried beans'),
        ],
        example='Sources disagree on this last figure, quoting anywhere from '
                '½ to 1 cup. The arithmetic settles it: if a can yields 1½ '
                'cups drained and a cup of dried yields 2½ cups cooked, you '
                'need roughly ⅔ cup dried. Use ½ cup if your beans are fresh '
                'and swell well, ¾ cup if they are older.',
    ),
    tables=[dict(
        heading='Cooking times',
        note='Times assume an overnight soak unless the bean is listed as '
             'no-soak. Older beans take longer, sometimes much longer. Salt '
             'the water — it seasons the bean itself and does not toughen the '
             'skin.',
        caption='Stovetop times, simmered gently with the lid ajar.',
        headers=['Bean or legume', 'Soak', 'Stovetop', 'Pressure cooker',
                 'Notes'],
        highlight=2,
        rows=[
            ['Black beans', 'Overnight', '60–90 min', '20–25 min',
             'Hold their shape well'],
            ['Black-eyed peas', 'Not needed', '45–60 min', '10–15 min',
             'Cook faster than most'],
            ['Cannellini', 'Overnight', '60–90 min', '25–30 min',
             'Skins split if boiled hard'],
            ['Chickpeas', 'Overnight', '90–120 min', '35–40 min',
             'Longest of the common beans'],
            ['Cranberry beans', 'Overnight', '60–75 min', '20–25 min',
             'Lose their markings when cooked'],
            ['Fava beans, dried', 'Overnight', '60–90 min', '25–30 min',
             'Peel after soaking for a smoother result'],
            ['Great Northern', 'Overnight', '75–90 min', '25–30 min',
             'Mild and creamy'],
            ['Kidney beans, red', 'Overnight, required', '60–90 min',
             '25–30 min', 'See the safety note below'],
            ['Lentils, brown or green', 'Not needed', '20–30 min',
             '8–10 min', 'Keep some bite for salads'],
            ['Lentils, red or yellow', 'Not needed', '15–20 min', '5–7 min',
             'Break down into a purée'],
            ['Lentils, Puy or black', 'Not needed', '25–30 min', '8–10 min',
             'Best at holding their shape'],
            ['Lima beans', 'Overnight', '60–75 min', '15–20 min',
             'Starchy, foam heavily'],
            ['Navy beans', 'Overnight', '75–90 min', '25–30 min',
             'Cook down to a thick liquid'],
            ['Pinto beans', 'Overnight', '75–90 min', '25–30 min',
             'Standard for refried beans'],
            ['Split peas', 'Not needed', '45–60 min', '12–15 min',
             'Collapse completely, as intended'],
        ],
    ), dict(
        heading='Dried to cooked yields',
        note='Yields are for beans cooked and drained. A cup of dried beans '
             'is roughly 6 to 7 ounces by weight, which is why volume '
             'measurements vary between sources.',
        caption='What a cup of dried beans becomes.',
        headers=['Dried amount', 'Cooked yield', 'Equivalent in cans'],
        highlight=1,
        rows=[
            ['⅓ cup', 'About ¾ cup', 'Half a 15 oz can'],
            ['⅔ cup', 'About 1½ cups', 'One 15 oz can'],
            ['1 cup', '2½ to 3 cups', 'Just under two cans'],
            ['1½ cups', '4 to 4½ cups', 'About three cans'],
            ['1 lb / 450 g', '6 to 7 cups', 'About four cans'],
        ],
    )],
    exceptions=[
        ('Old beans may never soften',
         ['Dried beans keep for years but do not stay the same. After about '
          'two years the skins harden and no amount of simmering fully '
          'reverses it.',
          'If beans are still firm an hour past the upper end of their range, '
          'the beans are the problem, not the method.']),
        ('Hard water and acid both slow things down',
         ['Calcium in hard water strengthens the bean skin. So does acid, '
          'which is why tomatoes, vinegar and lemon should go in after the '
          'beans are tender, not before.',
          'A pinch of baking soda in the cooking water counteracts hard '
          'water. Use very little — too much turns beans slippery.']),
        ('Salting early is fine, and better',
         ['The old advice to salt only at the end has not held up. Salted '
          'soaking and cooking water seasons the bean throughout and, if '
          'anything, helps the skin stay intact.',
          'Roughly a tablespoon of salt per quart of water is a reasonable '
          'starting point.']),
        ('A quick soak works when you forgot',
         ['Cover the beans with water, bring to a boil for two minutes, then '
          'take the pot off the heat and leave it covered for an hour. It '
          'gets you close to an overnight soak.',
          'Cooking time may still run slightly longer.']),
    ],
    safety=dict(
        heading='Red kidney beans must be boiled',
        intro='Raw and undercooked red kidney beans contain '
              'phytohaemagglutinin, which causes severe stomach upset. Slow '
              'cookers do not always reach a high enough temperature to '
              'destroy it.',
        items=[
            ('Soak', 'At least 5 hours, then discard the soaking water'),
            ('Boil', 'A full rolling boil for at least 10 minutes'),
            ('Then', 'Simmer until tender as usual'),
            ('Slow cooker', 'Boil on the stovetop first, then transfer'),
        ],
        outro='Canned kidney beans are already cooked and need none of this.',
    ),
    sources=[
        ('How to Cook Beans', 'Serious Eats',
         'https://www.seriouseats.com/how-to-cook-beans',
         'Cooking ranges, and the case for salting the water early.'),
        ('Bean Cooking Chart', "Bush's Beans",
         'https://www.bushbeans.com/en_US/article/bean-cooking-chart',
         'Dried-to-cooked yields and the 1½ cups per can figure.'),
        ('Dry Beans, Peas and Lentils', 'USDA FoodData Central',
         'https://fdc.nal.usda.gov/',
         'Drained weights used to check the yield arithmetic.'),
        ('Red Kidney Bean Poisoning', 'UK Food Standards Agency',
         'https://www.food.gov.uk/safety-hygiene/beans-and-pulses',
         'Source for the boiling requirement in the safety block.'),
    ],
    related=[
        ('/recipes/lemon-chickpea-salad/', 'Lemon chickpea salad'),
        ('/recipes/lemon-white-bean-skillet/', 'Lemon white bean skillet'),
        ('/recipes/mediterranean-warm-green-lentils/',
         'Mediterranean warm green lentils'),
        ('/recipes/5-minute-blender-hummus/', '5-minute blender hummus'),
    ],
)

PAGES['can-to-cup-conversions'] = dict(
    title='Can to Cup Conversions',
    h1='What is actually inside that can.',
    dek='How much a can of beans, tomatoes or coconut milk gives you in cups '
        'and grams — and why the same recipe calls for three different can '
        'sizes depending on where it was written.',
    description='Can to cup conversions for beans, tomatoes, coconut milk, '
                'broth and corn, with drained and undrained yields in cups, '
                'ounces and grams.',
    intro=[
        'Recipes call for a can. Cans are not standard. A can of chickpeas '
        'runs anywhere from 15 to 19 ounces depending on the brand, and the '
        'weight printed on the label includes the liquid, which you usually '
        'pour away.',
        'These tables give both figures: what the can weighs, and what you '
        'actually get once it is drained.',
    ],
    rule=dict(
        eyebrow='THE SHORT VERSION',
        items=[
            ('One 15 oz can beans', '1½ cups drained, about 240 g'),
            ('One 14.5 oz can tomatoes', '1¾ cups undrained'),
            ('One 13.5 oz can coconut milk', '1⅔ cups'),
        ],
        example='If a recipe gives a weight rather than a can, use the '
                'drained figure. A recipe asking for 240 g of chickpeas wants '
                'the contents of one drained can, not 240 g of the can as '
                'sold.',
    ),
    tables=[dict(
        heading='Beans and legumes',
        note='Drained yields assume rinsing. The liquid in the can, '
             'sometimes called aquafaba in chickpeas, is worth keeping for '
             'thickening.',
        caption='Standard US cans, drained and rinsed.',
        headers=['Can size', 'Drained yield', 'Drained weight',
                 'Undrained yield'],
        highlight=1,
        rows=[
            ['8 oz / 227 g', 'About ¾ cup', 'About 125 g', 'About 1 cup'],
            ['15 oz / 425 g', '1½ cups', 'About 240 g', 'Just under 2 cups'],
            ['15.5 oz / 439 g', '1½ cups', 'About 250 g', 'About 2 cups'],
            ['19 oz / 540 g', 'About 2 cups', 'About 310 g',
             'About 2⅓ cups'],
            ['28 oz / 794 g', 'About 3 cups', 'About 470 g',
             'About 3½ cups'],
            ['Europe, 400 g', 'About 1⅓ cups', 'About 240 g',
             'About 1¾ cups'],
        ],
    ), dict(
        heading='Tomatoes',
        note='Tomato products are used with their liquid, so the undrained '
             'figure is the one that matters. This is where conversions go '
             'wrong most often.',
        caption='Five formats, and what each one gives.',
        headers=['Product and can', 'Yield', 'Weight', 'Substitution note'],
        highlight=1,
        rows=[
            ['Diced, 14.5 oz', 'About 1¾ cups', '411 g',
             'The standard US can'],
            ['Diced, 28 oz', 'About 3½ cups', '794 g',
             'Equals two 14.5 oz cans'],
            ['Crushed, 28 oz', 'About 3½ cups', '794 g',
             'Thicker than diced, same volume'],
            ['Whole peeled, 28 oz', 'About 3½ cups', '794 g',
             'Roughly 10 to 12 whole tomatoes'],
            ['Purée, 29 oz', 'About 3½ cups', '822 g',
             'Thinner than paste, no seeds'],
            ['Paste, 6 oz', 'About ⅔ cup', '170 g',
             '1 tbsp paste is about 1 oz'],
            ['Sauce, 8 oz', '1 cup', '227 g', 'Already seasoned in some brands'],
            ['Europe, 400 g', 'About 1¾ cups', '400 g',
             'Close to the 14.5 oz can'],
        ],
    ), dict(
        heading='Coconut milk, broth and other staples',
        note='Coconut milk separates in the can. Shake it before opening, '
             'unless the recipe specifically asks for the thick cream on top.',
        caption='Common pantry cans.',
        headers=['Product and can', 'Yield', 'Weight', 'Note'],
        highlight=1,
        rows=[
            ['Coconut milk, 13.5 oz', 'About 1⅔ cups', '400 ml',
             'Shake before opening'],
            ['Coconut cream, 5.4 oz', 'About ⅔ cup', '160 ml',
             'Thicker, much richer'],
            ['Broth or stock, 14.5 oz', 'About 1¾ cups', '411 ml',
             'Two cans make about a quart'],
            ['Broth, 32 oz carton', '4 cups', '946 ml',
             'The standard quart'],
            ['Corn, 15 oz', 'About 1½ cups drained', 'About 250 g',
             'Frozen corn substitutes one for one'],
            ['Pumpkin purée, 15 oz', 'About 1¾ cups', '425 g',
             'Not pumpkin pie filling'],
            ['Condensed milk, 14 oz', 'About 1¼ cups', '397 g',
             'Sweetened, not the same as evaporated'],
            ['Evaporated milk, 12 oz', 'About 1½ cups', '354 ml',
             'Unsweetened'],
        ],
    )],
    exceptions=[
        ('"One can" is not a measurement',
         ['Chickpea cans sold in the US range from 15 to 19 ounces. That is a '
          'difference of nearly half a cup drained, which changes the balance '
          'of a salad or a dip noticeably.',
          'When precision matters, weigh the drained contents. Recipes on '
          'this site give both the can and the drained weight for that '
          'reason.']),
        ('Italian recipes usually mean the big can',
         ['A recipe written in Italy or the UK calling for "a tin of '
          'tomatoes" almost always means 400 g. American recipes calling for '
          '"a can" usually mean 14.5 ounces, which is close enough to swap.',
          'But Italian-American recipes for sauce frequently specify 28 '
          'ounces, which is double. Check the yield before assuming.']),
        ('Drained weight is not printed on every label',
         ['US labels show net weight, which includes the liquid. Some brands '
          'also print drained weight, and it is typically 55 to 60% of the '
          'net figure for beans.',
          'If only net weight is given, multiplying by 0.57 gets you close.']),
        ('Rinsing removes more than salt',
         ['Draining and rinsing canned beans cuts sodium by around 40%, and '
          'also removes some of the starch that makes canned beans taste '
          'flat.',
          'The exception is when the starch is useful: in soups and stews it '
          'thickens the liquid.']),
    ],
    safety=None,
    sources=[
        ('Can Sizes and Equivalents', 'The Spruce Eats',
         'https://www.thespruceeats.com/can-sizes-for-recipes-4077057',
         'Reference for US can sizes and their cup equivalents.'),
        ('Bean Cooking Chart', "Bush's Beans",
         'https://www.bushbeans.com/en_US/article/bean-cooking-chart',
         'Drained yield of 1½ cups per 15 oz can.'),
        ('Legumes and Legume Products', 'USDA FoodData Central',
         'https://fdc.nal.usda.gov/',
         'Drained weights used to convert cups to grams.'),
        ('Sodium Reduction by Rinsing Canned Beans',
         'Journal of Food Science research summary',
         'https://www.canneddemo.com/',
         'Basis for the approximate 40% sodium reduction figure.'),
    ],
    related=[
        ('/kitchen-notes/bean-cooking-chart/',
         'Bean cooking and conversion chart'),
        ('/recipes/lemon-chickpea-salad/', 'Lemon chickpea salad'),
        ('/recipes/5-minute-blender-hummus/', '5-minute blender hummus'),
    ],
)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _table(data):
    highlight = data.get('highlight')

    head = ''
    for index, label in enumerate(data['headers']):
        cls = ' class="col-highlight"' if index == highlight else ''
        head += f'<th scope="col"{cls}>{esc(label)}</th>'

    body = ''
    for row in data['rows']:
        cells = ''
        for index, value in enumerate(row):
            if index == 0:
                cells += f'<th scope="row">{esc(value)}</th>'
            else:
                cls = ' class="col-highlight"' if index == highlight else ''
                cells += f'<td{cls}>{esc(value)}</td>'
        body += f'<tr>{cells}</tr>'

    note = data.get('note')
    note_html = (
        f'<p class="reference-table-note">{esc(note)}</p>' if note else ''
    )

    return (
        f'<section class="reference-table-block">'
        f'<h2>{esc(data["heading"])}</h2>'
        f'{note_html}'
        f'<div class="reference-table-scroll">'
        f'<table class="reference-table">'
        f'<caption>{esc(data["caption"])}</caption>'
        f'<thead><tr>{head}</tr></thead>'
        f'<tbody>{body}</tbody>'
        f'</table></div>'
        f'<p class="reference-swipe-hint">Swipe to see all columns \u2192</p>'
        f'</section>'
    )


def _rule(data):
    rows = ''
    for label, value in data['items']:
        rows += f'<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>'
    return (
        f'<section class="reference-rule">'
        f'<p class="eyebrow">{esc(data["eyebrow"])}</p>'
        f'<dl>{rows}</dl>'
        f'<p class="rule-example">{esc(data["example"])}</p>'
        f'</section>'
    )


def _exceptions(items):
    if not items:
        return ''
    blocks = ''
    for index, (heading, paragraphs) in enumerate(items, start=1):
        body = ''.join(f'<p>{esc(p)}</p>' for p in paragraphs)
        blocks += (
            f'<div class="reference-exception">'
            f'<span class="step-num" aria-hidden="true">0{index}</span>'
            f'<div><h3>{esc(heading)}</h3>{body}</div>'
            f'</div>'
        )
    return (
        f'<section>'
        f'<p class="eyebrow">WHERE THE RULE BENDS</p>'
        f'<h2>Four exceptions worth knowing.</h2>'
        f'<div class="reference-exceptions">{blocks}</div>'
        f'</section>'
    )


def _safety(data):
    if not data:
        return ''
    items = ''.join(
        f'<li><strong>{esc(label)}:</strong> {esc(value)}</li>'
        for label, value in data['items']
    )
    outro = data.get('outro')
    outro_html = f'<p style="margin-top:14px">{esc(outro)}</p>' if outro else ''
    return (
        f'<section class="reference-safety">'
        f'<h2>{esc(data["heading"])}</h2>'
        f'<p>{esc(data["intro"])}</p>'
        f'<ul>{items}</ul>'
        f'{outro_html}'
        f'</section>'
    )


def _sources(items):
    entries = ''
    for title, publisher, url, note in items:
        entries += (
            f'<li><a href="{esc(url, quote=True)}" target="_blank" '
            f'rel="noopener nofollow">{esc(title)}</a>, {esc(publisher)}'
            f'<span class="source-note">{esc(note)}</span></li>'
        )
    return (
        f'<section class="reference-sources">'
        f'<h2>Sources consulted</h2>'
        f'<ol>{entries}</ol>'
        f'</section>'
    )


def _related(items):
    if not items:
        return ''
    links = ''.join(
        f'<li><a class="kn-recipe-link" href="{esc(url, quote=True)}">'
        f'{esc(label)} \u2197</a></li>'
        for url, label in items
    )
    return (
        f'<section class="kn-related">'
        f'<p class="eyebrow">PUT IT TO WORK</p>'
        f'<h2>Recipes that use this.</h2>'
        f'<ul>{links}</ul>'
        f'</section>'
    )


def body(slug):
    """Full <main> content for one reference page."""
    data = PAGES[slug]

    intro = ''.join(f'<p>{esc(p)}</p>' for p in data['intro'])
    tables = ''.join(_table(t) for t in data['tables'])

    ad = '<div class="ad-slot" data-ad-slot="reference-mid" aria-hidden="true"></div>'

    return (
        f'<div class="reference-page">'
        f'<nav class="breadcrumb" aria-label="Breadcrumb">'
        f'<a href="/kitchen-notes/">Kitchen Notes</a>'
        f'<span aria-hidden="true"> / </span>'
        f'<span>{esc(data["title"])}</span>'
        f'</nav>'
        f'<header class="reference-header">'
        f'<p class="eyebrow">REFERENCE</p>'
        f'<h1>{esc(data["h1"])}</h1>'
        f'<p class="reference-dek">{esc(data["dek"])}</p>'
        f'</header>'
        f'<section class="reference-intro">{intro}</section>'
        f'{_rule(data["rule"])}'
        f'{tables}'
        f'{ad}'
        f'{_exceptions(data["exceptions"])}'
        f'{_safety(data.get("safety"))}'
        f'{_related(data.get("related"))}'
        f'{_sources(data["sources"])}'
        f'</div>'
    )


def article_jsonld(slug, base_url=''):
    """Article schema. These pages are not recipes."""
    data = PAGES[slug]
    url = f'{base_url}/kitchen-notes/{slug}/' if base_url else f'/kitchen-notes/{slug}/'
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': data['title'],
        'description': data['description'],
        'url': url,
        'datePublished': '2026-09-17',
        'dateModified': '2026-09-17',
        'publisher': {'@type': 'Organization', 'name': 'Bored of Toast'},
        'isAccessibleForFree': True,
    }


def index_cards():
    """Cards for the kitchen notes listing."""
    cards = ''
    for slug, data in PAGES.items():
        cards += (
            f'<a class="kn-card" href="/kitchen-notes/{esc(slug, quote=True)}/">'
            f'<span class="kn-card-eyebrow">REFERENCE</span>'
            f'<span class="kn-card-title">{esc(data["title"])}</span>'
            f'<span class="kn-card-dek">{esc(data["dek"][:120])}\u2026</span>'
            f'</a>'
        )
    return cards
