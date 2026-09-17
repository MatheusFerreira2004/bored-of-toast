"""Fourth reference page: herb substitutions.

Why this is a separate file rather than an entry in reference_content.py:
that module is 29KB, and appending one page would mean rewriting all of
it. Instead this registers the page into reference_content.PAGES at
runtime and calls the existing renderers, so the output is byte-identical
in structure to the three pages already live.

The page itself resolves a real conflict in the sources. Almost every
chart publishes 3 parts fresh to 1 part dried. America's Test Kitchen
says not to substitute dried for tender herbs under any ratio.
CookingCalcs publishes per-herb ratios that contradict 3:1 outright.

They are answering different questions. 3:1 is a moisture ratio and
holds for woody herbs. The refusal is about volatile aromatics, which
tender herbs lose almost entirely in drying. So the page splits the
herbs into two tables and gives fresh alternatives for the second group
instead of a ratio that yields a worse dish.

Runs after postbuild_index.py:
    python build.py && python postbuild.py && python postbuild_index.py \\
        && python postbuild_herbs.py
"""
import json
import re
import sys
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'

SLUG = 'herb-substitution-chart'
SHELL_SOURCE = 'can-to-cup-conversions'
CARD_MARKER = 'data-herb-card'


# ---------------------------------------------------------------------------
# Page data
# ---------------------------------------------------------------------------

PAGE = dict(
    title='Herb Substitution Chart',
    h1='Fresh to dried, and when not to bother.',
    dek='The three-to-one rule works for woody herbs. For parsley, cilantro '
        'and basil the honest answer is to reach for a different fresh herb '
        'instead.',
    description='Fresh to dried herb conversions with per-herb ratios, which '
                'herbs survive drying and which do not, and fresh '
                'alternatives for the ones that do not.',
    intro=[
        'Nearly every conversion chart gives the same rule: three parts fresh '
        'equals one part dried. It is a good rule, and it is also the reason '
        'a lot of dishes end up tasting of dust.',
        'The ratio accounts for water. Drying removes most of the moisture '
        'from a leaf, so the same flavour ends up in a third of the volume. '
        'What the ratio does not account for is aroma. Woody herbs hold their '
        'aromatic compounds when dried. Tender herbs lose most of theirs, '
        'somewhere between 60 and 80 per cent, and no amount of adjusting '
        'the quantity brings them back.',
        'So there are two questions, not one. How much dried do I use, and '
        'should I be using dried at all.',
    ],
    rule=dict(
        eyebrow='THE RULE, AND ITS LIMIT',
        items=[
            ('Woody herbs', '3 parts fresh to 1 part dried, by volume'),
            ('Tender herbs', 'Dried loses 60 to 80% of the aroma'),
            ('Timing', 'Dried goes in early, fresh goes in at the end'),
        ],
        example='A recipe calling for 1 tablespoon of fresh thyme becomes 1 '
                'teaspoon dried, added with the onions rather than at the '
                'end. A recipe calling for a handful of fresh basil does not '
                'convert at all.',
    ),
    tables=[dict(
        heading='Herbs that work dried',
        note='Woody, low-moisture herbs. These hold up in anything with '
             'liquid and twenty minutes or more of cooking. Note that the '
             'ratio is not 3:1 across the board — rosemary concentrates more '
             'than most, sage less.',
        caption='Fresh quantity on the left, dried equivalent on the right.',
        headers=['Herb', 'Fresh', 'Dried', 'Ratio', 'Best used in'],
        highlight=2,
        rows=[
            ['Rosemary', '1 tbsp chopped', '\u00be tsp', '4:1',
             'Roasts, braises, bread'],
            ['Thyme', '1 tbsp chopped', '1 tsp', '3:1',
             'Soups, beans, roasted vegetables'],
            ['Oregano', '1 tbsp chopped', '1 tsp', '3:1',
             'Tomato sauce, marinades'],
            ['Marjoram', '1 tbsp chopped', '1 tsp', '3:1',
             'Sauces, stuffing'],
            ['Sage', '1 tbsp chopped', '1\u00bd tsp', '2:1',
             'Squash, butter sauces, beans'],
            ['Tarragon', '1 tbsp chopped', '1 tsp', '3:1',
             'Cream sauces, chicken'],
            ['Dill, in cooked dishes', '1 tbsp chopped', '1 tsp', '3:1',
             'Braises and soups only'],
            ['Bay leaf', '1 fresh leaf', '2 dried leaves', 'By count',
             'Stocks, stews, beans'],
        ],
    ), dict(
        heading='Herbs that do not',
        note='Tender, high-moisture herbs. A ratio exists for each, and it '
             'is printed below, but the last column is the more useful '
             'answer. Substituting a different fresh herb almost always '
             'beats using the dried version of the right one.',
        caption='What to use instead when the fresh herb is not available.',
        headers=['Herb', 'Dried ratio', 'What dried does to it',
                 'Better substitute'],
        highlight=3,
        rows=[
            ['Basil', '3:1', 'Turns dull and faintly hay-like',
             'Fresh mint, or dried only in sauce cooked 30 min plus'],
            ['Parsley', '2:1', 'Loses nearly all its flavour',
             'Fresh cilantro, celery leaf or chervil'],
            ['Cilantro', '3:1', 'The citrus note disappears entirely',
             'Fresh parsley with a squeeze of lime'],
            ['Chives', 'Not worth it', 'Goes papery, tastes of nothing',
             'Green onion tops, thinly sliced'],
            ['Mint', '3:1', 'Works for tea, not for food',
             'Fresh basil, or fresh parsley for savoury dishes'],
            ['Dill, as a finish', '3:1', 'Loses the bright anise edge',
             'Fresh fennel fronds or tarragon'],
            ['Chervil', '3:1', 'Almost nothing survives',
             'Fresh parsley plus a little tarragon'],
        ],
    ), dict(
        heading='Aromatics',
        note='Garlic, onion and ginger follow their own conversions, and the '
             'powders are far more concentrated than the ratios for leaves '
             'would suggest. Granulated sits between fresh and powder.',
        caption='Fresh aromatics and their dried equivalents.',
        headers=['Fresh', 'Powder', 'Granulated', 'Note'],
        highlight=1,
        rows=[
            ['1 clove garlic, minced', '\u00bc tsp garlic powder',
             '\u00bd tsp', 'About 1 tsp minced fresh'],
            ['1 cup diced onion', '1 tbsp onion powder', '3 tbsp',
             'Powder browns quickly, add late'],
            ['1 tsp grated ginger', '\u00bc tsp ground ginger', '\u2014',
             'Ground is warmer, less bright'],
            ['1 tsp grated horseradish', '\u2014', '\u2014',
             'No dried equivalent worth using'],
            ['1 stalk lemongrass', '\u2014', '\u2014',
             'Use lemon zest plus a little ginger'],
        ],
    )],
    exceptions=[
        ('Ground is stronger than crumbled',
         ['Most charts assume dried leaves, crumbled between your fingers. '
          'Ground herbs have far more surface area and hit harder.',
          'Start at a third of the dried quantity when using ground, so a '
          'teaspoon of dried thyme becomes a third of a teaspoon of ground.']),
        ('Timing matters more than quantity',
         ['Dried herbs need heat and liquid to release what they have left. '
          'Add them with the aromatics at the start, or bloom them in oil for '
          'thirty seconds.',
          'Fresh herbs work the opposite way. Their aroma compounds are '
          'volatile, so anything added at the start is gone by the time the '
          'dish reaches the table. Stir them in off the heat.']),
        ('Dried basil has exactly one good use',
         ['In a tomato sauce simmered for half an hour or more, dried basil '
          'has time to rehydrate and integrate, and it works.',
          'Anywhere it stays raw or barely cooked — on a caprese, over '
          'finished pasta, in a dressing — there is no version of the ratio '
          'that rescues it.']),
        ('Frozen beats dried for tender herbs',
         ['Blend soft herbs with a little olive oil and freeze the paste in '
          'an ice cube tray. It keeps most of the aroma that drying destroys.',
          'It will not work as a garnish, since the texture goes, but for '
          'anything stirred into a dish it is much closer to fresh than the '
          'dried version.']),
    ],
    safety=None,
    sources=[
        ('Substituting Dried Herbs for Fresh', "America's Test Kitchen",
         'https://www.americastestkitchen.com/how_tos/9261-science-substituting-dried-herbs-for-fresh',
         'Basis for splitting the herbs into two groups, and for the advice '
         'not to substitute dried for tender herbs.'),
        ('How to Convert Fresh to Dried Herb Measurements', 'The Spruce Eats',
         'https://www.thespruceeats.com/convert-herb-measurements-1706231',
         'The 3:1 baseline and the sage and ginger conversions.'),
        ('Fresh to Dried Herb Converter', 'CookingCalcs',
         'https://cookingcalcs.com/tools/herb-converter.html',
         'Per-herb ratios that depart from 3:1, including rosemary at 4:1 '
         'and parsley at 2:1.'),
        ('Fresh Herb to Dried Herb Conversion Chart', 'Reluctant Gourmet',
         'https://reluctantgourmet.com/converting-fresh-herbs-to-dried-ratios/',
         'On bay leaves being counted rather than measured, and on ground '
         'versus crumbled.'),
        ('Fresh-to-Dried Herb Conversion Guide', 'Forks Over Knives',
         'https://www.forksoverknives.com/how-tos/fresh-to-dried-herb-conversion-guide-plus-garlic-onion-powder/',
         'Source for the garlic and onion powder equivalents.'),
    ],
    related=[
        ('/kitchen-notes/swapping-herbs/',
         'Swapping herbs without ruining the dish'),
        ('/kitchen-notes/simple-lemon-dressing/',
         'Make a simple lemon dressing'),
        ('/recipes/lemon-chickpea-salad/', 'Lemon chickpea salad'),
        ('/recipes/mediterranean-warm-green-lentils/',
         'Mediterranean warm green lentils'),
    ],
)


# ---------------------------------------------------------------------------
# Page generation by cloning an existing reference page shell
# ---------------------------------------------------------------------------

def build_page():
    """Write the page using a live reference page as the HTML shell.

    Cloning the shell rather than assembling one means the header, footer,
    stylesheet links and font preloads stay identical to the rest of the
    site with no duplication of that markup here.
    """
    try:
        import reference_content as rc
    except Exception as exc:
        print(f'  skip: reference_content not importable ({exc})')
        return False

    shell_path = DIST / 'kitchen-notes' / SHELL_SOURCE / 'index.html'
    if not shell_path.exists():
        print(f'  skip: shell page not found at {shell_path}')
        return False

    # Register so rc.body() and rc.article_jsonld() can find it.
    rc.PAGES[SLUG] = PAGE

    html = shell_path.read_text(encoding='utf-8')

    # Title
    html = re.sub(
        r'<title>.*?</title>',
        f'<title>{esc(PAGE["title"])} \u2014 Bored of Toast</title>',
        html, count=1, flags=re.S,
    )

    # Meta description
    html = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        lambda m: m.group(1) + esc(PAGE['description'], quote=True) + m.group(2),
        html, count=1,
    )

    # Open Graph and Twitter titles and descriptions
    for prop in ('og:title', 'twitter:title'):
        html = re.sub(
            r'(<meta (?:property|name)="' + prop + r'" content=")[^"]*(")',
            lambda m: m.group(1) + esc(PAGE['title'], quote=True) + m.group(2),
            html, count=1,
        )
    for prop in ('og:description', 'twitter:description'):
        html = re.sub(
            r'(<meta (?:property|name)="' + prop + r'" content=")[^"]*(")',
            lambda m: m.group(1) + esc(PAGE['description'], quote=True) + m.group(2),
            html, count=1,
        )

    # Canonical and og:url, only if the build emitted them
    html = html.replace(
        f'/kitchen-notes/{SHELL_SOURCE}/',
        f'/kitchen-notes/{SLUG}/',
    )

    # Body content
    body_html = rc.body(SLUG)
    replaced = re.subn(
        r'(<main[^>]*>)(.*?)(</main>)',
        lambda m: m.group(1) + body_html + m.group(3),
        html, count=1, flags=re.S,
    )
    if replaced[1] == 0:
        print('  warn: <main> not found in shell, page not written')
        return False
    html = replaced[0]

    # Article schema
    schema = json.dumps(rc.article_jsonld(SLUG), ensure_ascii=False)
    html = re.sub(
        r'(<script type="application/ld\+json">)(.*?)(</script>)',
        lambda m: m.group(1) + schema + m.group(3),
        html, count=1, flags=re.S,
    )

    out_dir = DIST / 'kitchen-notes' / SLUG
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'index.html').write_text(html, encoding='utf-8')
    return True


# ---------------------------------------------------------------------------
# Listing card
# ---------------------------------------------------------------------------

def inject_card():
    """Add the card to the kitchen notes grid, matching the existing markup."""
    listing = DIST / 'kitchen-notes' / 'index.html'
    if not listing.exists():
        return False

    html = listing.read_text(encoding='utf-8')
    if CARD_MARKER in html:
        return False

    dek = PAGE['dek']
    if len(dek) > 150:
        dek = dek[:147].rstrip(' ,.;') + '\u2026'

    card = (
        f'<a class="kn-guide-card" {CARD_MARKER} '
        f'href="/kitchen-notes/{SLUG}/">'
        f'<span class="eyebrow">REFERENCE / CHARTS</span>'
        f'<span class="kn-series-badge">Reference</span>'
        f'<h3>{esc(PAGE["title"])}</h3>'
        f'<p>{esc(dek)}</p>'
        f'<span class="text-link">Open the chart \u2197</span>'
        f'</a>'
    )

    match = re.search(r'(<div class="kn-card-grid">)(.*?)(</div>)', html, re.S)
    if not match:
        return False

    cut = match.end(2)
    listing.write_text(html[:cut] + card + html[cut:], encoding='utf-8')
    return True


# ---------------------------------------------------------------------------
# Sitemap
# ---------------------------------------------------------------------------

def add_to_sitemap():
    """Append the new URL, copying the format of the existing entries."""
    path = DIST / 'sitemap.xml'
    if not path.exists():
        return False

    xml = path.read_text(encoding='utf-8')
    if SLUG in xml:
        return False

    # Reuse the shell page's entry so the host and any lastmod match.
    match = re.search(
        r'<url>\s*<loc>([^<]*' + re.escape(SHELL_SOURCE) + r'[^<]*)</loc>.*?</url>',
        xml, re.S,
    )
    if not match:
        return False

    entry = match.group(0).replace(SHELL_SOURCE, SLUG)
    xml = xml.replace(match.group(0), match.group(0) + entry, 1)
    path.write_text(xml, encoding='utf-8')
    return True


# ---------------------------------------------------------------------------

def main():
    if not DIST.exists():
        print('postbuild_herbs: dist/ not found, nothing to do')
        return 0

    print('postbuild_herbs: starting')

    try:
        if build_page():
            print(f'  page written: /kitchen-notes/{SLUG}/')
    except Exception as exc:
        print(f'  warn: page generation failed: {exc}')

    try:
        if inject_card():
            print('  card added to kitchen notes listing')
    except Exception as exc:
        print(f'  warn: card injection failed: {exc}')

    try:
        if add_to_sitemap():
            print('  sitemap entry added')
    except Exception as exc:
        print(f'  warn: sitemap update failed: {exc}')

    print('postbuild_herbs: done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
