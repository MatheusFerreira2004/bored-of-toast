#!/usr/bin/env python3
"""Lighter recipe cards, same look.

The recipe library page grew past the 80 KB HTML budget in checks.py (about 101 KB with 50
recipes). Two things were repeated on every card:
  1. a hidden data-text attribute with title, description and all ingredient names, used only by
     the search box on /recipes/. search-index.js already holds the same words (field "s"), so
     app.js now reads them from there and falls back to the card text.
  2. the full SVG markup of the clock and chef-hat icons. They are now defined once per page as an
     SVG sprite and referenced with <use>. Same drawing, size and color.
VER is bumped so browsers load the new app.js together with the new HTML.

No visual change. Idempotent: running it again changes nothing.
"""
import os, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build.py')
APP = os.path.join(HERE, 'app.js')
b = open(BUILD, encoding='utf-8').read()
a = open(APP, encoding='utf-8').read()
b0, a0 = b, a


def swap(src, old, new, label, count=None):
    if old in src:
        n = src.count(old)
        if count is not None and n != count:
            print(f'ERROR: {label}: expected {count} match(es), found {n}. Nothing was changed.')
            sys.exit(1)
        print(f'- OK: {label} ({n}x)')
        return src.replace(old, new)
    if new in src:
        print(f'- already applied: {label}')
        return src
    print(f'ERROR: {label}: text not found. Nothing was changed.')
    sys.exit(1)


# 1) sprite definitions, right after WHY_ICONS
ANCHOR = "WHY_ICONS = [ICON['bolt'], ICON['heart'], ICON['check']]"
SPRITE_DEF = r'''
# Card meta icons as a sprite (update_035): same drawing as ICON['clock'] and ICON['chef'], defined once per page.
SPR = {'clock': '<svg width="15" height="15" aria-hidden="true"><use href="#i-clock"/></svg>',
       'chef': '<svg width="15" height="15" aria-hidden="true"><use href="#i-chef"/></svg>'}
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
          '<symbol id="i-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>'
          '<symbol id="i-chef" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 13.9A4 4 0 0 1 7 6a5 5 0 0 1 10 0 4 4 0 0 1 1 7.9V20H6z"/><path d="M6 17h12"/></symbol></svg>')'''
if 'SPRITE = (' in b:
    print('- already applied: sprite definitions')
elif b.count(ANCHOR) == 1:
    b = b.replace(ANCHOR, ANCHOR + SPRITE_DEF, 1)
    print('- OK: sprite definitions')
else:
    print('ERROR: WHY_ICONS anchor not found exactly once. Nothing was changed.')
    sys.exit(1)

# 2) include the sprite on pages that use it (right after the skip link)
b = swap(b,
         '<a class="skip-link" href="#main">Skip to content</a>\n{header(root, active)}',
         '<a class="skip-link" href="#main">Skip to content</a>\n{SPRITE if SPR["clock"] in body else ""}{header(root, active)}',
         'sprite included in page()', count=1)

# 3) card meta icons use the sprite
b = swap(b,
         "<span>{ICON['clock']}{fmt_time(r['time'])}</span><span>{ICON['chef']}{r['level']}</span>",
         "<span>{SPR['clock']}{fmt_time(r['time'])}</span><span>{SPR['chef']}{r['level']}</span>",
         'card meta icons')

# 4) cards drop data-text (search reads search-index.js instead)
b = swap(b, ' data-text="{e(text)}">', '>', 'card data-text removed', count=1)

# 5) cache-busting version, so the new app.js arrives with the new HTML
b = swap(b, "VER = '20261006-journey-1'", "VER = '20261012-light-1'", 'asset version bump', count=1)

# 6) app.js: listing search reads words from the search index
JS_OLD = 'const okQ = !q || c.dataset.text.includes(q);'
JS_NEW = 'const okQ = !q || textOf(c).includes(q);'
JS_HELPERS = '\n'.join([
    r"    const SX = {}; INDEX.forEach(x => { if (x.k === 'recipe') SX[x.u] = (x.s || '') + ' ' + x.t.toLowerCase(); });",
    r"    const textOf = c => c.dataset.text || SX[(c.getAttribute('href') || '').replace(/^(\.\.\/)+/, '')] || c.textContent.toLowerCase();",
    '    function apply() {'])
if JS_NEW in a:
    print('- already applied: app.js listing search')
elif a.count(JS_OLD) == 1 and a.count('    function apply() {') == 1:
    a = a.replace(JS_OLD, JS_NEW).replace('    function apply() {', JS_HELPERS, 1)
    print('- OK: app.js listing search reads search-index.js')
else:
    print('ERROR: app.js listing search code not found as expected. Nothing was changed.')
    sys.exit(1)

if b != b0:
    open(BUILD, 'w', encoding='utf-8').write(b)
if a != a0:
    open(APP, 'w', encoding='utf-8').write(a)
print('Done.' if (b != b0 or a != a0) else 'Already applied. Nothing to do.')
