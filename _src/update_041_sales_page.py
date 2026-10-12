#!/usr/bin/env python3
"""Nourished sales page, round 2 (keeps the PR #45 layout and the four covers).

1. Main button no longer sends visitors to the free sheet. While checkout_url is null it reads
   "Purchasing opens soon · see what's included" and jumps to #collection. With a checkout URL it
   reads "Get the full collection · US$20" (journey_checks still finds "Get the full collection").
2. Hero subtitle speaks to the problem: "Know what to cook this week, even when your appetite is small."
3. "Purchasing is not open yet" no longer appears under the price (hero and final offer). It stays
   once, in "How buying works" (required by journey_checks and update_040).
4. The free planning-sheet section (#print) moves next to the FAQ, with a lighter outline button,
   so it does not compete with the product.
5. A 14-day guarantee box next to the hero price.
6. Menu, footer and hero eyebrow say "Nourished" instead of "Cookbook" / "The cookbook collection".
7. Mobile-only purchase bar at the bottom of the screen (Nourished · US$20 · button).

No testimonials, urgency, health or weight claims. Price, bonuses, refund and page counts unchanged.
Nothing is written unless every anchor is found once or already applied. Safe to re-run.
"""
import os, re, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *n: os.path.join(HERE, *n)
report = ['# 041 Nourished sales page', '']


def patch_text(text, pairs, label):
    for old, new, name in pairs:
        final_versions = {
            'main button while checkout is closed': 'href="#collection">See what’s included</a>',
            'note under the price (no repeated closed notice)': 'Purchasing opens soon. See <a href="#buying">How buying works</a> for details.',
            'guarantee box in the hero': '<strong>14-day money-back guarantee.</strong>',
            'stylesheet cache version': "'-sales-5' if path == 'nourished/'",
        }
        if new in text or (name in final_versions and final_versions[name] in text):
            report.append(f'- {label}: already applied: {name}')
        elif text.count(old) == 1:
            text = text.replace(old, new)
            report.append(f'- {label}: OK: {name}')
        else:
            print(f'ERROR: {label}: anchor for "{name}" found {text.count(old)} times. Nothing was saved.')
            sys.exit(1)
    return text


GUARANTEE = ('<div class="nourished-guarantee"><strong>Try it for 14 days.</strong>'
             'If Nourished isn’t right for you, email us within 14 days for a full refund. No reason needed.</div>')

STICKY_FN = '''def sticky_bar(config):
    """update_041: mobile-only purchase bar on the Nourished page."""
    url = config.get('checkout_url')
    if url:
        btn = '<a class="btn btn-yellow" href="' + e(url, quote=True) + '">Get it</a>'
    else:
        btn = '<a class="btn btn-yellow" href="#collection">Look inside</a>'
    return ('<div class="nourished-sticky" role="region" aria-label="Nourished purchase">'
            '<div><strong>Nourished</strong><span>US$20 · 14-day refund</span></div>' + btn + '</div>')
'''

# ------------------------------------------------------------------ storefront.py
s = open(P('storefront.py'), encoding='utf-8').read()
s = patch_text(s, [
    ("    return '<a class=\"btn btn-yellow\" href=\"#print\">Try the free planner</a>'",
     "    return '<a class=\"btn btn-yellow\" href=\"#collection\">Purchasing opens soon · see what’s included ↓</a>'",
     'main button while checkout is closed'),
    ("action(config, 'checkout', 'Get the full collection', 'btn-yellow')",
     "action(config, 'checkout', 'Get the full collection · US$20', 'btn-yellow')",
     'main button label when checkout is live'),
    ("else 'Purchasing is not open yet. Explore the collection or try the free planning sheet below.')",
     "else 'Planned as a one-time US$20 purchase. See how buying works below.')",
     'note under the price (no repeated closed notice)'),
    ('<p class="nourished-subtitle">Your GLP-1 kitchen, <em>organized.</em></p>',
     '<p class="nourished-subtitle">Know what to cook this week, <em>even when your appetite is small.</em></p>',
     'hero subtitle'),
    ('<p class="eyebrow">The cookbook collection / By Bored of Toast</p>',
     '<p class="eyebrow">The GLP-1 Kitchen Companion / By Bored of Toast</p>',
     'hero eyebrow'),
    ('<p class="commerce-small">{checkout_note(config)}</p></div></div></section>',
     '<p class="commerce-small">{checkout_note(config)}</p>' + GUARANTEE + '</div></div></section>',
     'guarantee box in the hero'),
    ("Discuss your individual needs with your care team.</p></section></div>'''",
     "Discuss your individual needs with your care team.</p></section></div>{sticky_bar(config)}'''",
     'mobile purchase bar'),
    ('<a class="btn btn-dark" href="{root}printables/nourished-weekly-planner-sample.pdf" target="_blank" rel="noopener">Open printable sample ↗</a>',
     '<a class="btn btn-outline" href="{root}printables/nourished-weekly-planner-sample.pdf" target="_blank" rel="noopener">Open printable sample ↗</a>',
     'lighter button on the free sheet'),
], 'storefront.py')

m = re.search(r'<section class="section bg-paper" id="print">.*?</section>\n', s, re.S)
if not m or 'id="buying"' not in s:
    print('ERROR: storefront.py: #print or #buying section not found. Nothing was saved.')
    sys.exit(1)
if s.index('id="print"') > s.index('id="buying"'):
    report.append('- storefront.py: already applied: free sheet section placed next to the FAQ')
else:
    block = m.group(0)
    s = s.replace(block, '', 1)
    anchor = '<section class="container section commerce-faq">'
    if s.count(anchor) != 1:
        print('ERROR: storefront.py: FAQ section anchor not found once. Nothing was saved.')
        sys.exit(1)
    s = s.replace(anchor, block + anchor)
    report.append('- storefront.py: OK: free sheet section moved next to the FAQ')

if 'def sticky_bar(' in s:
    report.append('- storefront.py: already applied: sticky_bar()')
else:
    s = s.rstrip('\n') + '\n\n' + STICKY_FN
    report.append('- storefront.py: OK: added sticky_bar()')

# ------------------------------------------------------------------ build.py
b = open(P('build.py'), encoding='utf-8').read()
b = patch_text(b, [
    ("('nourished/', 'Cookbook', 'cookbooks')", "('nourished/', 'Nourished', 'cookbooks')", 'menu and footer label'),
    ("{'-sales-2' if path == 'nourished/' else ''}", "{'-sales-3' if path == 'nourished/' else ''}", 'stylesheet cache version'),
], 'build.py')

# ------------------------------------------------------------------ styles.css
CSS_MARK = '/* update_041: Nourished guarantee box and mobile purchase bar */'
CSS = CSS_MARK + '''
.nourished-guarantee{margin-top:14px;padding:12px 14px;border:1px dashed currentColor;border-radius:12px;font-size:.9rem;line-height:1.45}
.nourished-guarantee strong{display:block;margin-bottom:2px}
.nourished-sticky{display:none}
@media (max-width:760px){
.nourished-sticky{display:flex;align-items:center;justify-content:space-between;gap:12px;position:fixed;left:0;right:0;bottom:0;z-index:60;padding:10px 16px calc(10px + env(safe-area-inset-bottom));background:#3f5130;color:#f7f2e7;box-shadow:0 -6px 20px rgba(0,0,0,.18)}
.nourished-sticky div{display:flex;flex-direction:column;line-height:1.2}
.nourished-sticky span{font-size:.8rem;opacity:.85}
.nourished-sticky .btn{padding:10px 18px;white-space:nowrap}
.nourished-sales{padding-bottom:72px}
body:has(.nourished-sticky) .to-top{bottom:84px}
}
@media print{.nourished-sticky{display:none}}
'''
c = open(P('styles.css'), encoding='utf-8').read()
if CSS_MARK in c:
    report.append('- styles.css: already applied')
    c_new = c
else:
    c_new = c.rstrip('\n') + '\n\n' + CSS
    report.append('- styles.css: OK: guarantee box and mobile bar styles')

# ------------------------------------------------------------------ save
open(P('storefront.py'), 'w', encoding='utf-8').write(s)
open(P('build.py'), 'w', encoding='utf-8').write(b)
if c_new != c:
    open(P('styles.css'), 'w', encoding='utf-8').write(c_new)

report += ['', '## Pending (owner)',
           '- Covers shown on the page must also be inside the PDFs before checkout opens.',
           '- Payment vendor and support email not confirmed.',
           '- Visual check on mobile and desktop (prints).']
os.makedirs(P('reports'), exist_ok=True)
open(P('reports', '041_sales_page.md'), 'w', encoding='utf-8').write('\n'.join(report) + '\n')
print('\n'.join(report))
print('Done.')
