#!/usr/bin/env python3
"""Review lote 3: Nourished sales page.

1. New section "Why pay for Nourished?" answering the objection that the site recipes are free.
   No exclusivity claim: overlap between the site recipes and the PDF recipes was not verified,
   so the text only describes how the collection is organized and says plainly that buyers who
   are happy browsing the site do not need it.
2. The "A simple way to begin" steps become the real sequence used in the PDFs:
   recipe (numbered) -> week example (refers to recipe numbers) -> weekly shopping list -> prep notes.
   Only facts already stated elsewhere on the page are used.
3. New section "How buying works", summarising the Terms of Use (payment by Lemon Squeezy as
   merchant of record, taxes at checkout, receipt and download access by email, household
   license, 14-day refund to the original payment method). While checkout_url is null it says
   purchasing is not open yet and describes how it will work.
4. New FAQ: "Why pay if the recipes on this site are free?"

Authorship is intentionally not touched (pending the owner's decision).
Nothing is saved unless every anchor is found exactly once. Safe to re-run.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'storefront.py')
s = open(p, encoding='utf-8').read()

MARKER = 'id="why-nourished"'
if MARKER in s:
    print('Already applied. Nothing to do.')
    sys.exit(0)

WHY = """<section class="container section" id="why-nourished"><div class="section-head"><div><p class="eyebrow">A fair question</p><h2>The recipes here are free.<br><em>Why pay for Nourished?</em></h2></div></div><div class="commerce-feature-grid"><article><h3>The site: one recipe at a time</h3><p>Our recipes, guides and collections are free to read, and they stay free. They work well when you want one idea for tonight.</p></article><article><h3>Nourished: a week at a time</h3><p>36 numbered recipes connected to four weeks of meal examples, a shopping list for each week and prep notes, so planning starts from one place instead of many open tabs.</p></article><article><h3>Files for your kitchen</h3><p>Four PDFs to keep on your device and print when you need them, plus 11 printable sheets for your own meals, shopping and freezer stock.</p></article></div><p class="commerce-small">If browsing the site already covers what you need, you do not need Nourished. Buying it does not unlock extra content on the site.</p></section>
"""

OLD_STEPS_HEAD = """<p class="eyebrow">Start with your next week</p><h2>A simple way<br><em>to begin.</em></h2>"""
NEW_STEPS_HEAD = """<p class="eyebrow">How the pieces connect</p><h2>From recipe<br><em>to prep.</em></h2>"""

OLD_STEPS = """<li><strong>Open Start Here.</strong><span>The main guide points you to recipes, weekly examples and planning sheets.</span></li><li><strong>Choose and adapt.</strong><span>Use the examples as a starting point and add food and portions for your needs.</span></li><li><strong>Check stock, then prep.</strong><span>Use the shopping and preparation pages; record your own plan in the Printable Pack.</span></li>"""
NEW_STEPS = """<li><strong>Pick a recipe.</strong><span>Each recipe has a number, ingredients, method and nutrition estimates. Numbers continue from the main guide into Recipe Pack Volume 2.</span></li><li><strong>Find it in a week example.</strong><span>The meal examples refer to recipes by number, and each week has its own shopping list. Adapt the example to your own food and portions.</span></li><li><strong>Shop, then prep.</strong><span>Check your stock against the list, use the prep notes to decide what to make ahead, and write your plan on a printable sheet.</span></li>"""

BUYING = """<section class="container section" id="buying"><div class="section-head"><div><p class="eyebrow">{'Before you buy' if config.get('checkout_url') else 'When purchasing opens'}</p><h2>How buying<br><em>works.</em></h2>{'' if config.get('checkout_url') else '<p>Purchasing is not open yet. This is how it will work when it opens, as set out in our Terms of Use.</p>'}</div></div><div class="commerce-feature-grid"><article><h3>Payment</h3><p>Checkout is handled by Lemon Squeezy, our reseller and merchant of record. Prices are in US dollars, and any sales tax or VAT for your location is calculated at checkout.</p></article><article><h3>Your files</h3><p>Lemon Squeezy emails your receipt and download access for the four PDFs. The license covers your own household, so please do not share or resell the files.</p></article><article><h3>Help and refunds</h3><p>For questions, or a refund within 14 days of purchase, email boredoftoast@gmail.com. Refunds go back to your original payment method, and no reason is needed. Full details are in our <a href="{root}terms/">Terms of Use</a>.</p></article></div></section>
"""

FAQ_ANCHOR = "        ('Can I try a sample first?',"
FAQ_NEW = ("        ('Why pay if the recipes on this site are free?','The site recipes stay free and work one page at a time. "
           "Nourished organizes 36 numbered recipes with four weeks of meal examples, weekly shopping lists, prep notes and "
           "printable sheets in four PDFs. If browsing the site already covers what you need, you do not need it.'),\n")

PREVIEW_ANCHOR = '<section class="section bg-paper" id="preview">'
FAQ_SECTION_ANCHOR = '<section class="container section commerce-faq">'

CHANGES = [
    (PREVIEW_ANCHOR, WHY + PREVIEW_ANCHOR),
    (OLD_STEPS_HEAD, NEW_STEPS_HEAD),
    (OLD_STEPS, NEW_STEPS),
    (FAQ_SECTION_ANCHOR, BUYING + FAQ_SECTION_ANCHOR),
    (FAQ_ANCHOR, FAQ_NEW + FAQ_ANCHOR),
]

for old, new in CHANGES:
    n = s.count(old)
    if n != 1:
        print(f'ERROR: expected 1 match in storefront.py, found {n} (nothing was saved):\n{old[:140]}')
        sys.exit(1)
    s = s.replace(old, new)

open(p, 'w', encoding='utf-8').write(s)
print('OK: Nourished page updated (why-pay section, real sequence, buying summary, new FAQ).')
