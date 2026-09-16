"""Reference pages: conversion charts and lookup tables.

Self-contained module following the same pattern as kitchen_notes.py.
Content stays readable without JavaScript.

Integration in build.py requires three lines:

    from reference_pages import PAGES as REFERENCE_PAGES, page as render_reference_page

    for p in REFERENCE_PAGES:
        write(f'kitchen-notes/{p["slug"]}/index.html',
              page(title=p['title'] + ' — Bored of Toast',
                   desc=p['meta_desc'],
                   body=render_reference_page(p),
                   css='reference',
                   jsonld=article_jsonld(p)))

Also copy reference.css to dist/ alongside the other stylesheets.
"""
from html import escape as esc

AUTHOR = 'Matheus Ferreira'


# ---------------------------------------------------------------------------
# Page definitions
# ---------------------------------------------------------------------------

PAGES = [
    dict(
        slug='oven-to-air-fryer-conversion',
        title='Oven to Air Fryer Conversion',
        eyebrow='04 / THE REFERENCE SHELF',
        dek='Two numbers change. Everything else stays the same.',
        meta_desc='Convert any oven recipe to the air fryer. Reduce the temperature by 25°F and the time by 20%, with a full chart and the exceptions that matter.',
        date_published='2026-09-16',
        date_modified='2026-09-16',
        intro=[
            'Most air fryer disappointment starts with a recipe written for an oven. The instructions are not wrong — they are just describing a different machine. An air fryer is a small convection oven with a powerful fan very close to the food, which means it heats faster, browns sooner, and dries surfaces more aggressively than a full-size oven ever will.',
            'The fix is two adjustments, not a new recipe. Lower the temperature so the outside does not race ahead of the inside, and shorten the time because the heat is arriving faster. Everything else in the recipe stays as written.',
            'Below is the chart, the arithmetic behind it, and the four situations where the standard rule does not apply.',
        ],
        rule=dict(
            eyebrow='THE RULE',
            items=[
                ('Temperature', 'Reduce by 25°F (about 15°C)'),
                ('Time', 'Reduce by 20%'),
            ],
            example='A recipe calling for 400°F for 30 minutes becomes 375°F for 24 minutes. For the time, multiply by 0.8: forty minutes becomes 32, sixty becomes 48.',
        ),
        tables=[
            dict(
                heading='Temperature',
                note='Round to the nearest setting your machine offers. A five-degree difference will not change the result.',
                caption='Oven to air fryer, Fahrenheit and Celsius',
                headers=['Oven (°F)', 'Oven (°C)', 'Air fryer'],
                highlight=2,
                rows=[
                    ['300°F', '150°C', '275°F / 135°C'],
                    ['325°F', '160°C', '300°F / 150°C'],
                    ['350°F', '175°C', '325°F / 165°C'],
                    ['375°F', '190°C', '350°F / 175°C'],
                    ['400°F', '200°C', '375°F / 190°C'],
                    ['425°F', '220°C', '400°F / 200°C'],
                    ['450°F', '230°C', '425°F / 220°C'],
                ],
            ),
            dict(
                heading='Time',
                note='The third column is 75% of the converted time. Air fryers vary more between models than ovens do, and the difference shows up in the last few minutes.',
                caption='Oven time converted, with a checkpoint',
                headers=['Oven time', 'Air fryer time', 'Start checking at'],
                highlight=2,
                rows=[
                    ['10 min', '8 min', '6 min'],
                    ['15 min', '12 min', '9 min'],
                    ['20 min', '16 min', '12 min'],
                    ['25 min', '20 min', '15 min'],
                    ['30 min', '24 min', '18 min'],
                    ['40 min', '32 min', '24 min'],
                    ['45 min', '36 min', '27 min'],
                    ['60 min', '48 min', '36 min'],
                ],
            ),
        ],
        exceptions_heading='When the rule does not apply',
        exceptions=[
            ('Your recipe was written for a fan oven',
             ['A fan oven is already doing what an air fryer does, just at a larger scale. Reduce the temperature by only 10 to 15°F instead of 25°F. Keep the 20% time reduction.']),
            ('Basket style versus oven style',
             ['Basket air fryers sit closer to the heating element and circulate air in a smaller space. Reduce time by 20%.',
              'Oven-style air fryers have more room and slightly gentler circulation. Reduce time by 15% instead.']),
            ('The basket is full',
             ['Air needs a path around the food. When the basket is crowded, add 3 to 5 minutes and shake halfway through.',
              'If you find yourself adding much more than that, cook in two batches — the second batch will still finish faster than one crowded one.']),
            ('Frozen food',
             ['Keep the temperature printed on the package. Reduce the time by 25 to 40%, and check early.',
              'Frozen items carry surface ice that has to evaporate before browning begins, so the first few minutes are doing a different job than the last few.']),
        ],
        safety=dict(
            heading='Temperature is the test, not the clock',
            intro='Temperature and time are a guide. Doneness is a temperature, not a clock reading. For anything where undercooking matters, use a thermometer rather than the chart.',
            items=[
                ('Poultry', '165°F / 74°C'),
                ('Ground meat', '160°F / 71°C'),
                ('Whole cuts of beef, pork and lamb', '145°F / 63°C, with a three-minute rest'),
                ('Fish', '145°F / 63°C'),
            ],
            outro='Vegetables, legumes and baked goods are judged by texture and color, not internal temperature.',
        ),
        related_intro='The chart is the starting point. These recipes are already converted.',
        related=[
            ('oven-roasted-crispy-chickpeas', 'Oven-roasted crispy chickpeas'),
        ],
        sources=[
            ('Air Fryer Conversion Chart', 'Air Fryer Converter',
             'https://airfryconverter.com/air-fryer-conversion-chart/',
             'Temperature table in Fahrenheit and Celsius, and the guidance to check at 75% of the time.'),
            ('Air Fryer Calculator', 'Calculator Academy',
             'https://calculator.academy/air-fryer-calculator/',
             'The inverse formula and the 10°F adjustment for convection ovens.'),
            ('Oven to Air Fryer Conversion', 'Savor + Savvy',
             'https://savorandsavvy.com/oven-to-air-fryer-conversion/',
             'Food-specific times and the guidance to check at the halfway point.'),
            ('Safe Minimum Internal Temperature Chart', 'USDA',
             'https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart',
             'Minimum safe internal cooking temperatures.'),
        ],
    ),

    dict(
        slug='bean-cooking-chart',
        title='Bean Cooking and Conversion Chart',
        eyebrow='05 / THE REFERENCE SHELF',
        dek='Dried, canned, cooked. The numbers that connect them.',
        meta_desc='Cooking times for dried beans and lentils, plus how to convert between dried, canned and cooked. With the soaking rules that actually matter.',
        date_published='2026-09-16',
        date_modified='2026-09-16',
        intro=[
            'Recipes rarely agree on beans. One calls for a can, another for a cup of dried, a third for cooked weight in grams. They are describing the same thing at three different stages, and converting between them is where most home cooks give up and buy the can.',
            'The conversion is simple once you see it written down. A standard can of beans, drained, gives you about one and a half cups. Getting to that same amount from dried takes roughly two thirds of a cup and some patience.',
            'Below are the cooking times for the legumes worth keeping in a pantry, the conversion table between dried, canned and cooked, and the two rules about salt and acid that change the result more than any timing chart will.',
        ],
        rule=dict(
            eyebrow='THE CONVERSION',
            items=[
                ('One can drained', 'About 1½ cups cooked beans'),
                ('From dried', 'About ⅔ cup (130 g)'),
                ('One cup dried', 'Yields 2½ to 3 cups cooked'),
            ],
            example='A recipe calling for two cans of chickpeas needs about 1⅓ cups dried. Start the soak the night before.',
        ),
        tables=[
            dict(
                heading='Cooking times',
                note='Times assume soaked legumes where soaking is listed. Age matters more than most charts admit — beans that have been in the cupboard for two years can take twice as long, and some never soften at all.',
                caption='Dried legumes, soak and cook times',
                headers=['Legume', 'Soak', 'Stovetop', 'Pressure', 'Yield from 1 cup dry'],
                highlight=2,
                rows=[
                    ['Red lentils (split)', 'No soak', '10–15 min', '5–7 min', '2–2½ cups'],
                    ['Yellow lentils (split)', 'No soak', '15 min', '5–7 min', '2–2½ cups'],
                    ['Brown lentils', 'No soak', '20–30 min', '7–9 min', '2–2½ cups'],
                    ['Green lentils', 'No soak', '30–40 min', '7–9 min', '2–2½ cups'],
                    ['French green / beluga', 'No soak', '25–35 min', '8–10 min', '2–2½ cups'],
                    ['Split peas', 'No soak', '30–45 min', '8–10 min', '2 cups'],
                    ['Black-eyed peas', 'No soak', '45–60 min', '9–11 min', '2¼ cups'],
                    ['Adzuki', '4 h', '45–55 min', '5–9 min', '3 cups'],
                    ['Black beans', '4–8 h', '60–90 min', '8–11 min', '2¼ cups'],
                    ['Navy beans', '6–8 h', '45–60 min', '7–9 min', '2⅔ cups'],
                    ['Great Northern', '4–8 h', '60 min', '8–10 min', '2¼ cups'],
                    ['Cannellini', '8 h', '60–90 min', '10–12 min', '2¼ cups'],
                    ['Pinto beans', '4–8 h', '90 min', '5–7 min', '2¼ cups'],
                    ['Kidney beans', '6–8 h', '60 min', '10–12 min', '2¼ cups'],
                    ['Chickpeas', '8–12 h', '90–120 min', '12–20 min', '2–3 cups'],
                ],
            ),
            dict(
                heading='Conversions',
                note='Weigh rather than measure by volume when the yield needs to be exact.',
                caption='Between canned, dried and cooked',
                headers=['If the recipe says', 'Drained volume', 'Dried equivalent', 'Cooked weight'],
                highlight=3,
                rows=[
                    ['1 can (15 oz / 425 g)', '1½ cups', '⅔ cup (130 g)', 'about 250 g'],
                    ['2 cans', '3 cups', '1⅓ cups (260 g)', 'about 500 g'],
                    ['1 cup dried', '2½–3 cups', '1 cup (200 g)', 'about 480 g'],
                    ['1 cup cooked', '1 cup', 'scant ½ cup (85 g)', 'about 165 g'],
                ],
            ),
        ],
        note_block=dict(
            heading='Why sources disagree on this',
            paragraphs=[
                'Serious Eats puts the dried equivalent of one can at three quarters of a cup. Earth to Veg and Rustic Roots Living both say half a cup. Reluctant Gourmet says a full cup.',
                'They are not contradicting each other so much as measuring different things. Half a cup of dried beans yields roughly a cup and a quarter cooked, which is slightly short of a drained can. A full cup of dried yields close to three cups, which is nearly two cans.',
                'Two thirds of a cup sits where the arithmetic actually lands, and it is the number used in the table above. If a recipe is forgiving, any of these will work.',
            ],
        ),
        exceptions_heading='The two mistakes that cost the most',
        exceptions=[
            ('Adding acid too early',
             ['Lemon, vinegar and tomatoes firm up bean skins. Added at the start, they can keep beans tough well past the point where they should have softened — sometimes indefinitely. Cook the beans until tender first, then add anything acidic.',
              'This is why a bean and tomato stew that simmers from cold so often has chalky beans at the end.']),
            ('Salting at the wrong moment',
             ['The old advice to never salt the cooking water has been overturned. Salt in the water from the start seasons the bean itself rather than just the liquid around it, and softens the skin rather than toughening it.',
              'The texture difference between beans salted at the start and beans salted at the end is the single biggest improvement available to anyone cooking dried beans.']),
        ],
        safety=dict(
            heading='Kidney beans need a hard boil',
            intro='Raw and undercooked kidney beans contain a natural toxin that causes severe nausea and vomiting within hours. Slow cooking alone does not reach a temperature high enough to destroy it — beans cooked at low temperature can be more dangerous than raw ones.',
            items=[
                ('Soak', 'At least five hours, then discard the soaking water'),
                ('Boil', 'Hard boil for at least 10 minutes in fresh water'),
                ('Then', 'Reduce to a simmer until tender'),
                ('Never', 'Cook raw kidney beans in a slow cooker without boiling first'),
            ],
            outro='This applies to red kidney beans in particular, and to a lesser degree to white kidney beans and cannellini. Lentils, chickpeas and black beans do not carry the same risk. Discard soaking water for all beans regardless.',
        ),
        related_intro='The chart is the starting point. These are what to do next.',
        related=[
            ('lemon-chickpea-salad', 'Lemon chickpea salad'),
            ('lemon-white-bean-skillet', 'Lemony white beans & spinach'),
            ('mediterranean-warm-green-lentils', 'Mediterranean warm green lentils'),
            ('5-minute-blender-hummus', '5-minute blender hummus'),
        ],
        sources=[
            ('Can I Substitute Dried Beans for Canned?', 'Serious Eats',
             'https://www.seriouseats.com/is-there-a-ratio-for-converting-between-dried',
             'Base ratio of drained can to dried volume.'),
            ('Cooking Times for Beans, Lentils and Peas', 'Heal With Food',
             'https://www.healwithfood.org/chart/beans-cooking-times.php',
             'Comparative times for stovetop and pressure cooking.'),
            ('How to Cook Dried Beans and Lentils', 'Freistyle',
             'https://www.frei-style.com/en/how-to-cook-dried-beans-and-lentils',
             'Rules on salt and acid, and the hard boil requirement for kidney beans.'),
            ('Dry Beans and Legumes Cooking Chart', 'Andrea Meyers',
             'https://andreasrecipes.com/dry-beans-and-legumes-cooking-chart/',
             'Yields per dry cup and soak times by variety.'),
            ('Beans Conversion Calculator', 'Earth to Veg',
             'https://earthtoveg.com/calc/beans/',
             'The alternative conversion that prompted the editorial note above.'),
        ],
    ),
]

PAGES_BY_SLUG = {p['slug']: p for p in PAGES}


def url(p):
    return '/kitchen-notes/' + p['slug'] + '/'


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _rule(r):
    items = ''.join(
        f'<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>'
        for label, value in r['items']
    )
    return (
        f'<section class="reference-rule">'
        f'<p class="eyebrow">{esc(r["eyebrow"])}</p>'
        f'<dl>{items}</dl>'
        f'<p class="rule-example">{esc(r["example"])}</p>'
        f'</section>'
    )


def _table(t):
    hi = t.get('highlight')
    headers = ''.join(
        f'<th scope="col"{" class=\'col-highlight\'" if hi == i else ""}>{esc(h)}</th>'
        for i, h in enumerate(t['headers'])
    )
    rows = ''
    for row in t['rows']:
        cells = f'<th scope="row">{esc(row[0])}</th>'
        cells += ''.join(
            f'<td{" class=\'col-highlight\'" if hi == i + 1 else ""}>{esc(c)}</td>'
            for i, c in enumerate(row[1:])
        )
        rows += f'<tr>{cells}</tr>'
    return (
        f'<section class="reference-table-block">'
        f'<h2>{esc(t["heading"])}</h2>'
        f'<p class="reference-table-note">{esc(t["note"])}</p>'
        f'<div class="reference-table-scroll">'
        f'<table class="reference-table">'
        f'<caption>{esc(t["caption"])}</caption>'
        f'<thead><tr>{headers}</tr></thead>'
        f'<tbody>{rows}</tbody>'
        f'</table></div>'
        f'<p class="reference-swipe-hint">Swipe to see all columns →</p>'
        f'</section>'
    )


def _note_block(n):
    paras = ''.join(f'<p>{esc(p)}</p>' for p in n['paragraphs'])
    return (
        f'<section class="reference-safety">'
        f'<h2>{esc(n["heading"])}</h2>{paras}'
        f'</section>'
    )


def _exceptions(heading, items):
    blocks = ''
    for i, (title, paras) in enumerate(items, 1):
        body = ''.join(f'<p>{esc(p)}</p>' for p in paras)
        blocks += (
            f'<div class="reference-exception">'
            f'<span class="step-num">{i:02}</span>'
            f'<div><h3>{esc(title)}</h3>{body}</div>'
            f'</div>'
        )
    return (
        f'<section><h2>{esc(heading)}</h2>'
        f'<div class="reference-exceptions">{blocks}</div></section>'
    )


def _safety(s):
    items = ''.join(
        f'<li><strong>{esc(label)}:</strong> {esc(value)}</li>'
        for label, value in s['items']
    )
    return (
        f'<section class="reference-safety">'
        f'<h2>{esc(s["heading"])}</h2>'
        f'<p>{esc(s["intro"])}</p>'
        f'<ul>{items}</ul>'
        f'<p style="margin-top:14px;margin-bottom:0">{esc(s["outro"])}</p>'
        f'</section>'
    )


def _related(p):
    links = ''.join(
        f'<a class="kn-recipe-link" href="/recipes/{slug}/">{esc(title)}'
        f'<span aria-hidden="true"> ↗</span></a>'
        for slug, title in p.get('related', [])
    )
    if not links:
        return ''
    return (
        f'<section class="kn-related">'
        f'<p class="eyebrow">FROM NOTEBOOK TO TABLE</p>'
        f'<h2>Put it to work.</h2>'
        f'<p>{esc(p["related_intro"])}</p>{links}'
        f'</section>'
    )


def _sources(items):
    entries = ''.join(
        f'<li><a href="{esc(u, quote=True)}" rel="noopener nofollow" target="_blank">'
        f'{esc(title)}</a> — {esc(publisher)}'
        f'<span class="source-note">{esc(note)}</span></li>'
        for title, publisher, u, note in items
    )
    return (
        f'<section class="reference-sources">'
        f'<h2>Sources</h2><ol>{entries}</ol>'
        f'</section>'
    )


def page(p):
    """Render a full reference page."""
    intro = ''.join(f'<p>{esc(t)}</p>' for t in p['intro'])
    tables = ''.join(_table(t) for t in p['tables'])
    note = _note_block(p['note_block']) if p.get('note_block') else ''
    exceptions = _exceptions(p['exceptions_heading'], p['exceptions'])

    return f'''<article class="reference-page">
<a class="breadcrumb" href="/kitchen-notes/">← All kitchen notes</a>
<header class="reference-header">
<p class="eyebrow">{esc(p['eyebrow'])}</p>
<h1>{esc(p['title'])}</h1>
<p class="reference-dek">{esc(p['dek'])}</p>
<p class="small">By {esc(AUTHOR)} · Updated {esc(p['date_modified'])}</p>
</header>
<section class="reference-intro">{intro}</section>
{_rule(p['rule'])}
<div class="ad-slot" data-ad-slot="reference-top" aria-hidden="true"></div>
{tables}
{note}
{exceptions}
{_safety(p['safety'])}
{_related(p)}
<div class="ad-slot" data-ad-slot="reference-bottom" aria-hidden="true"></div>
{_sources(p['sources'])}
</article>'''


def article_jsonld(p, base_url=''):
    """Article schema. Not Recipe, not HowTo — these are reference pages."""
    page_url = (base_url.rstrip('/') + url(p)) if base_url else url(p)
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': p['title'],
        'description': p['meta_desc'],
        'author': {'@type': 'Person', 'name': AUTHOR, 'url': '/about/'},
        'datePublished': p['date_published'],
        'dateModified': p['date_modified'],
        'mainEntityOfPage': {'@type': 'WebPage', '@id': page_url},
        'publisher': {'@type': 'Organization', 'name': 'Bored of Toast'},
    }


def index_cards():
    """Cards for the kitchen notes index, to sit alongside the guides."""
    return ''.join(
        f'<a class="kn-guide-card" href="{url(p)}">'
        f'<span class="eyebrow">{esc(p["eyebrow"])}</span>'
        f'<h3>{esc(p["title"])}</h3>'
        f'<p>{esc(p["dek"])}</p>'
        f'<span class="text-link">Open the chart ↗</span></a>'
        for p in PAGES
    )
