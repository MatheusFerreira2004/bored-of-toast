#!/usr/bin/env python3
"""Nourished sales page: clearer value, 14-day refund, honest fit check.

- Hero: lead tied to the site's positioning; "14-day refund" added to the quick facts.
- Feature grid: benefit-led (small plates, harder days, shopping done).
- New "Is Nourished right for you?" section (good fit / probably not for you).
- Final offer: the four files listed with page counts (value stack) and the refund promise
  next to the buy button.
- FAQ: new "What if it is not right for me?" answer, linking to the Terms.

No invented "worth $X" anchors, testimonials or urgency. Purchase states are unchanged:
checkout still shows "Purchasing is not open yet" until checkout_url is set.
Nothing is saved unless every change is found. Safe to re-run.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'storefront.py')
s = open(p, encoding='utf-8').read()

if 'Is Nourished<br><em>right for you?</em>' in s:
    print('Already applied. Nothing to do.')
    sys.exit(0)

FIT = ('<section class="container section" id="fit"><div class="section-head"><div><p class="eyebrow">An honest check</p>'
       '<h2>Is Nourished<br><em>right for you?</em></h2></div></div><div class="commerce-feature-grid">'
       '<article><h3>A good fit if you\u2026</h3><ul>'
       '<li>want ready recipes in smaller portions, with protein estimates</li>'
       '<li>like having the week planned, with shopping lists already done</li>'
       '<li>need gentle options for days when your appetite is low</li>'
       '<li>prefer pages you can print and keep in the kitchen</li></ul></article>'
       '<article><h3>Probably not for you if\u2026</h3><ul>'
       '<li>you want a personalized diet or calorie targets</li>'
       '<li>you are looking for medical or dosing guidance</li>'
       '<li>you only want an app or interactive tracker</li></ul>'
       '<p class="commerce-small">For personal nutrition goals, your doctor, dietitian or care team is the right place to start.</p></article>'
       '</div></section>\n')

STACK = ('<ul class="commerce-stack">'
         '<li><strong>Nourished main guide</strong> \u00b7 60 pages \u00b7 24 recipes, Weeks 1\u20132, shopping and prep guidance</li>'
         '<li><strong>28-Day Meal Plan</strong> \u00b7 9 pages \u00b7 all four weeks, with a shopping list for each week</li>'
         '<li><strong>Recipe Pack Volume 2</strong> \u00b7 14 pages \u00b7 12 more recipes, with portions and substitutions</li>'
         '<li><strong>Printable Pack</strong> \u00b7 12 pages \u00b7 11 sheets for meals, shopping and freezer stock</li></ul>')

REFUND = ('<p class="commerce-small"><strong>14-day refund.</strong> If it is not right for you, email us within 14 days '
          'for a full refund. No reason needed.</p>')

CHANGES = [
    ('<p class="commerce-lead">A practical cooking collection for adults using GLP-1 medication. Find recipes, check your shopping and plan what to prepare.</p>',
     '<p class="commerce-lead">A practical cooking collection for adults using GLP-1 medication: smaller portions, protein estimates for every recipe, and your week planned before you shop.</p>'),
    ('<span>Read digitally or print</span></p>',
     '<span>Read digitally or print</span><span>14-day refund</span></p>'),
    ('<article><h3>Find your next recipe</h3><p>Breakfasts, mains, soups and snacks, with ingredients, methods and nutrition estimates.</p></article>'
     '<article><h3>Plan before you shop</h3><p>Follow recipe references from the meal examples to the shopping quantities and prep notes.</p></article>'
     '<article><h3>Make the plan your own</h3><p>Use the printable sheets for your meals, shopping notes and freezer stock.</p></article>',
     '<article><h3>Small plates, protein first</h3><p>Breakfasts, mains, soups and snacks in manageable portions, each with ingredients, method and nutrition estimates.</p></article>'
     '<article><h3>A plan for harder days</h3><p>Gentle options and a simple minimum for low-appetite days, organized so you can find something quickly.</p></article>'
     '<article><h3>Shopping already done</h3><p>Weekly shopping lists and prep notes connected to the meal examples, plus printable sheets for your own plan.</p></article>'),
    ('<section class="container section"><div class="commerce-compare">',
     FIT + '<section class="container section"><div class="commerce-compare">'),
    ('<p>The main guide and all three bonuses. Four English PDFs, ready to save or print.</p>',
     '<p>The main guide and all three bonuses. Four English PDFs, ready to save or print.</p>' + STACK),
    ('{checkout_action(config)}<p class="commerce-small">{checkout_note(config)}</p><a class="commerce-text-link" href="{root}starter-kit/">Preview the free starter kit</a>',
     '{checkout_action(config)}<p class="commerce-small">{checkout_note(config)}</p>' + REFUND + '<a class="commerce-text-link" href="{root}starter-kit/">Preview the free starter kit</a>'),
    ("('Can I try a sample first?',",
     "('What if it is not right for me?',f'Email hello@boredoftoast.com within 14 days of your purchase for a full refund. No reason needed. Details are in our <a href=\"{root}terms/\">Terms of Use</a>.'),\n        ('Can I try a sample first?',"),
]

for old, new in CHANGES:
    n = s.count(old)
    if n != 1:
        sys.exit(f'ERROR: expected 1 match in storefront.py, found {n} (nothing was saved):\n{old[:120]}')
    s = s.replace(old, new)

open(p, 'w', encoding='utf-8').write(s)
print('OK: Nourished page updated (lead, refund, benefits, fit check, value stack, refund FAQ).')
