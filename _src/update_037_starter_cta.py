#!/usr/bin/env python3
"""Review lote 4: contextual Starter Kit CTAs and one consistent name.

- One name everywhere: "GLP-1 Kitchen Starter Kit" (short: "Starter Kit"). No more
  "sampler", "free guide" or "free GLP-1 kit".
- The one-page planning sheet is named as a separate sheet, never as the kit.
- New CTA before the footer on the recipe library, single guides and Small-Plate Week.
  It links to the Starter Kit page and does not promise delivery that is not live yet.
- Live-delivery labels checked by journey_checks.py are left untouched.

Idempotent: each replacement is skipped when the new text is already present
(checked first, because some new texts contain the old text, e.g. the import line).
Exits with an error if neither the old nor the new text is found.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
errors = []

def patch(name, pairs, append=None):
    path = os.path.join(HERE, name)
    text = open(path).read()
    orig = text
    for old, new, label in pairs:
        if new in text:
            print(f'already applied ({name}): {label}')
        elif old in text:
            text = text.replace(old, new)
            print(f'OK ({name}): {label}')
        else:
            errors.append(f'{name}: {label}')
            print(f'ERROR ({name}): text not found for: {label}')
    if append:
        marker, block = append
        if marker in text:
            print(f'already applied ({name}): {marker}')
        else:
            text = text.rstrip('\n') + '\n\n' + block
            print(f'OK ({name}): added {marker}')
    return path, orig, text

STARTER_CTA = '''def starter_cta(root, config):
    """update_037: Starter Kit CTA placed before the footer on library, guide and week pages."""
    live = bool(config.get('signup_url') or config.get('download_url'))
    note = ('Free 9-page English PDF. General cooking education.' if live else
            'Full-kit delivery opens soon. The kit page has a separate one-page planning sheet you can open now.')
    return f\'\'\'<section class="container section commerce-promo-wrap" data-starter-cta><div class="commerce-promo commerce-promo-free">
<div class="commerce-promo-art">{picture(root, 'starter-cover', 'Cover of the free GLP-1 Kitchen Starter Kit')}</div>
<div><p class="eyebrow">Free Starter Kit</p>
<h2>Want a few recipes in one file?<br><em>Start with the free Starter Kit.</em></h2>
<p>The GLP-1 Kitchen Starter Kit has three sample recipes from Nourished, a shopping checklist, and a worked example with a blank organizer for planning your own days.</p>
<div class="commerce-actions"><a href="{root}starter-kit/" class="btn btn-dark">See the free Starter Kit</a></div>
<p class="commerce-small">{note}</p></div>
</div></section>\'\'\'
'''

sf = patch('storefront.py', [
    ("'A free taste of Nourished' if free else", "'Free Starter Kit / A taste of Nourished' if free else", 'promo eyebrow'),
    ("{'Explore the free kit' if free else 'Explore the collection - US$20'}", "{'See the free Starter Kit' if free else 'Explore the collection - US$20'}", 'promo button'),
    ('<h3>Explore the free Nourished sampler.</h3>', '<h3>Try the free GLP-1 Kitchen Starter Kit.</h3>', 'recipe-page box title (sampler)'),
    ('Explore the free starter kit →</a></section>', 'See the free Starter Kit →</a></section>', 'recipe-page box link'),
    ('>Try a free planning sheet ↗</a>', '>Open the free one-page planning sheet ↗</a>', 'planning sheet named as a separate sheet'),
    ('<p class="eyebrow">Free guide / By Bored of Toast</p>', '<p class="eyebrow">Free Starter Kit / By Bored of Toast</p>', 'kit page eyebrow'),
    ('<h2>Inside your free sampler.</h2>', '<h2>Inside the free Starter Kit.</h2>', 'kit page section title (sampler)'),
    ('<th scope="col">Free kit</th>', '<th scope="col">Free Starter Kit</th>', 'compare table header'),
    ('>Explore the free kit →</a></div></section>', '>See the free Starter Kit →</a></div></section>', 'compare table link'),
    ('>Preview the free starter kit</a>', '>See the free Starter Kit</a>', 'offer link'),
    ('>explore the 9-page starter kit</a>', '>see the 9-page Starter Kit</a>', 'FAQ link'),
], append=('def starter_cta(', STARTER_CTA))

ADD_CTA = '''def add_starter_cta(path, root, body):
    """update_037: Starter Kit CTA before the footer on the recipe library, single guides and Small-Plate Week."""
    if 'data-starter-cta' in body:
        return body
    if path in ('recipes/', 'meal-plan/') or (path.startswith('guides/') and 'guide-layout' in body):
        return body + starter_cta(root, STOREFRONT)
    return body

'''
PAGE_SIG = "def page(path, title, desc, body, active='', root='', og='images/og/home.jpg', jsonld=None, head_extra='', body_attr=''):\n    canonical = SITE_URL + path"
PAGE_NEW = ADD_CTA + "def page(path, title, desc, body, active='', root='', og='images/og/home.jpg', jsonld=None, head_extra='', body_attr=''):\n    body = add_starter_cta(path, root, body)\n    canonical = SITE_URL + path"

bp = patch('build.py', [
    ('from storefront import build_storefront, marketing_block, contextual_link, validate_config',
     'from storefront import build_storefront, marketing_block, contextual_link, validate_config, starter_cta', 'import starter_cta'),
    (">Free GLP-1 kit</a></li>'", ">Free Starter Kit</a></li>'", 'footer link name'),
    ('class="btn btn-ghost">Get the free starter kit</a>', 'class="btn btn-ghost">See the free Starter Kit</a>', 'hero buttons (home, collections): no delivery promise'),
    (PAGE_SIG, PAGE_NEW, 'CTA hook in page()'),
])

if errors:
    print('ERROR: nothing written. Missing:', '; '.join(errors))
    sys.exit(1)
for path, orig, text in (sf, bp):
    if text != orig:
        open(path, 'w').write(text)
print('Done.')
