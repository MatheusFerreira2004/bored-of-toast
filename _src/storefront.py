"""Nourished storefront templates. Empty integration URLs render honest coming-soon states."""
from html import escape as e
from urllib.parse import urlparse

def validate_config(config):
    social = config.get('social_urls', {})
    if not isinstance(social, dict) or set(social) - {'instagram', 'pinterest', 'facebook'}:
        raise ValueError('social_urls must contain only instagram, pinterest and facebook')
    urls = {key: config.get(key) for key in ('signup_url', 'download_url', 'checkout_url')}
    urls.update({f'social_urls.{key}': value for key, value in social.items()})
    for key, value in urls.items():
        if value is None:
            continue
        if not isinstance(value, str) or any(c.isspace() for c in value):
            raise ValueError(f'{key} must be null or an absolute public HTTPS URL')
        parsed = urlparse(value)
        if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError(f'{key} must be an absolute HTTPS URL without embedded credentials')
    return config

def picture(root, name, alt, eager=False):
    return f'<img src="{root}images/commerce/{name}.jpg{'?v=20261012-covers' if name.endswith('cover') and not name.startswith('starter') else ''}" alt="{e(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async" width="760" height="{1647 if name.startswith("starter") else 984}">'

def action(config, kind, label, style='btn-dark'):
    url = config.get(kind + '_url')
    if url:
        return f'<a class="btn {style}" href="{e(url, quote=True)}">{e(label)}</a>'
    unavailable = {'signup': 'Email signup opens soon', 'download': 'Download opens soon', 'checkout': 'Purchase opens soon'}[kind]
    return f'<p class="commerce-availability">{unavailable}</p>'

def kit_action(config, root):
    if config.get('signup_url'):
        return action(config, 'signup', 'Get the free starter kit')
    if config.get('download_url'):
        return action(config, 'download', 'Download the free starter kit')
    return f'<a class="btn btn-dark" href="{root}printables/nourished-weekly-planner-sample.pdf" target="_blank" rel="noopener">Open the free one-page planning sheet ↗</a>'

def kit_note(config):
    if config.get('signup_url'):
        return 'The signup page explains how to receive the 9-page kit and manage your email preferences.'
    if config.get('download_url'):
        return 'Free 9-page English PDF. Follow the download page to save your copy.'
    return 'The full 9-page kit delivery is not open yet. The button opens a separate, one-page Weekly Meal Planner sample from Nourished; no signup is required for that sheet.'

def checkout_action(config):
    if config.get('checkout_url'):
        return action(config, 'checkout', 'Get the full collection · US$20', 'btn-yellow')
    return '<a class="btn btn-yellow" href="#collection">Purchasing opens soon · see what’s included ↓</a>'

def checkout_note(config):
    return ('One-time purchase. Review checkout for delivery details and any applicable taxes.'
            if config.get('checkout_url') else 'Planned as a one-time US$20 purchase. See how buying works below.')

def marketing_block(root, kind):
    free = kind == 'free'
    return f'''<section class="container section commerce-promo-wrap"><div class="commerce-promo {'commerce-promo-free' if free else 'commerce-promo-paid'}">
<div class="commerce-promo-art">{picture(root, 'starter-cover' if free else 'nourished-cover', 'Cover of the free GLP-1 Kitchen Starter Kit' if free else 'Cover of Nourished')}</div>
<div><p class="eyebrow">{'Free Starter Kit / A taste of Nourished' if free else 'A cookbook collection by Bored of Toast'}</p>
<h2>{'Start with three recipes.<br><em>Make the next step easier.</em>' if free else 'Meet Nourished.<br><em>Your GLP-1 kitchen companion.</em>'}</h2>
<p>{'A free kit for adults using GLP-1 medication: three sample recipes, a shopping checklist and a three-day organizer.' if free else '36 recipes, four weeks of meal examples and practical tools for shopping, preparation and your own planning.'}</p>
<div class="commerce-actions"><a href="{root}{'starter-kit/' if free else 'nourished/'}" class="btn {'btn-dark' if free else 'btn-yellow'}">{'See the free Starter Kit' if free else 'Explore the collection - US$20'}</a></div>
<p class="commerce-small">{'9-page PDF in English. General cooking education.' if free else 'Main guide + 3 companion PDFs. One collection, US$20.'}</p></div>
</div></section>'''

def contextual_link(root):
    return f'<section class="commerce-context"><p class="tag">Cooking while using GLP-1?</p><h3>Try the free GLP-1 Kitchen Starter Kit.</h3><p>A 9-page English PDF with three sample recipes, a shopping checklist and a three-day organizer.</p><a class="view-all" href="{root}starter-kit/">See the free Starter Kit →</a></section>'

def build_storefront(page, config):
    root = '../'
    cover = picture(root, 'starter-cover', 'Cover of The GLP-1 Kitchen Starter Kit', True)
    body = f'''<section class="commerce-hero"><div class="container commerce-hero-grid"><div>
<p class="eyebrow">Free Starter Kit / By Bored of Toast</p><h1>Three recipes.<br><em>A practical first step.</em></h1>
<p class="commerce-lead">For adults using GLP-1 medication: sample three recipes from Nourished, check what to buy and use a blank organizer for your own meals.</p>
<div class="commerce-actions"><a class="btn btn-dark" href="#get-kit">{'Get the free kit' if config.get('signup_url') or config.get('download_url') else 'Explore free sample options'}</a><a class="commerce-text-link" href="{root}nourished/">Compare with Nourished</a></div>
<p class="commerce-small">For adults using GLP-1 medication. 9 pages. English PDF.</p>{'' if config.get('signup_url') or config.get('download_url') else '<p class="commerce-small">Full-kit delivery opens soon. A free printable sample is available below.</p>'}
</div><div class="commerce-cover-stage">{cover}<span class="commerce-seal">A free<br>taste</span></div></div></section>
<section class="container section" id="inside"><div class="section-head"><div><p class="eyebrow">A useful first step</p><h2>Inside the free Starter Kit.</h2></div></div>
<div class="commerce-feature-grid">
<article><span class="commerce-number">01</span><h3>Three ways to cook</h3><p>Overnight Protein Oats, Red Lentil &amp; Carrot Soup, and a Cold Chicken &amp; Avocado Wrap.</p></article>
<article><span class="commerce-number">02</span><h3>Shop with a checklist</h3><p>Quantities for one batch of each recipe, with space to check what is already in your kitchen.</p></article>
<article><span class="commerce-number">03</span><h3>Plan your own days</h3><p>A worked example and a blank organizer to place recipes alongside your other meals, sides and snacks.</p></article></div></section>
<section class="section bg-paper"><div class="container commerce-preview-layout"><a class="commerce-page-preview" href="{root}images/commerce/starter-example.jpg" target="_blank" rel="noopener" aria-label="Open the starter kit planning example at full size">{picture(root,'starter-example','A real page from the kit showing a three-day planning example')}</a><div><p class="eyebrow">A real page from the kit</p><h2>See how the pieces<br><em>fit together.</em></h2><p>Start with one recipe. The worked example shows how to place recipe ideas alongside your other food; the blank organizer is yours to fill in.</p><p>It is a cooking resource, not a complete three-day diet or personalized nutrition plan.</p><a class="view-all" href="{root}nourished/">Meet the full collection →</a></div></div></section>
<section class="container section" id="get-kit"><div class="commerce-signup"><p class="eyebrow">The GLP-1 Kitchen Starter Kit</p><h2>Your first few recipes,<br><em>all in one place.</em></h2><p>One free English PDF: three recipes, a shopping checklist, a worked example and a blank organizer.</p>{kit_action(config,root)}<p class="commerce-small">{kit_note(config)}</p><a class="commerce-text-link" href="{root}nourished/">Explore Nourished</a></div></section>
<section class="container commerce-disclaimer"><p>General cooking education. Choose food and portions for your own needs, and discuss personal nutrition goals with your care team. Check ingredients for allergies.</p></section>'''
    page('starter-kit/','Free GLP-1 Kitchen Starter Kit | Bored of Toast','Try three recipes from Nourished, a shopping checklist and a three-day organizer. A free English PDF for your GLP-1 kitchen.',body,'starter-kit',root,og='images/commerce/starter-cover.jpg')
    previews = ''.join(f'''<article class="commerce-preview-card"><a href="{root}images/commerce/{name}.jpg" target="_blank" rel="noopener" aria-label="Open {title.lower()} preview at full size">{picture(root,name,alt)}</a><h3>{title}</h3><p>{desc}</p><a class="view-all" href="{root}images/commerce/{name}.jpg" target="_blank" rel="noopener">Read this sample page ↗</a></article>''' for name,title,alt,desc in [
        ('recipe-preview','Recipes to return to','A real Overnight Protein Oats recipe page from Nourished','Ingredients, instructions and calculated nutrition estimates, with practical recipe notes.'),
        ('shopping-preview','Shopping with a purpose','A real Week 1 shopping checklist from Nourished','Recipe amounts and buying notes, so you can check your stock before heading to the store.'),
        ('planning-preview','Your week, organized','An illustrative Week 1 meal example page from Nourished','Illustrative meal examples to adapt, linked to recipe numbers, shopping and preparation pages. Any daily totals shown describe that example only, not a target for you.')])
    products = [
        ('nourished-cover', 'Main guide', 'Nourished', 'Your starting point for smaller plates.', '24 recipes, Weeks 1–2, shopping lists and practical prep guidance.', 60, 'main'),
        ('meal-plan-cover', 'Bonus 1', '28-Day Meal Plan', 'See all four weeks in one place.', 'Four weeks of meal examples to adapt, with a shopping list for each week.', 9, 'blue'),
        ('recipe-pack-cover', 'Bonus 2', 'Recipe Pack Vol. 2', 'Add more variety to your kitchen.', '12 more recipes, numbered 25–36, with portions, side suggestions and substitutions.', 14, 'terracotta'),
        ('printable-pack-cover', 'Bonus 3', 'Printable Pack', 'Make room for your own plans.', '11 printable sheets for meals, shopping, freezer stock and notes, plus an index.', 12, 'sage'),
    ]
    packs = ''.join(f'''<article class="nourished-product nourished-product-{tone}"><div class="nourished-product-art">{picture(root,name,title + ' PDF cover')}</div><div class="nourished-product-copy"><div class="nourished-product-heading"><p class="eyebrow">{label} · {pages} pages</p><h3>{title}</h3></div><div class="nourished-product-details"><p class="nourished-product-benefit">{benefit}</p><p>{desc}</p></div></div></article>''' for name,label,title,benefit,desc,pages,tone in products)
    bundle = '<div class="nourished-bundle" aria-label="Nourished main guide and three included bonus PDFs">' + ''.join(f'<div class="nourished-bundle-item nourished-bundle-{tone}">{picture(root,name,title + " PDF cover",True)}<div class="nourished-bundle-label"><span>{label}</span><strong>{title}</strong></div></div>' for name,label,title,benefit,desc,pages,tone in products) + '</div>'
    offer_covers = '<div class="nourished-offer-covers" aria-hidden="true">' + ''.join(picture(root,name,'') for name,*_ in products) + '</div>'
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in [
        ('Who is Nourished for?','Adults using GLP-1 medication who want practical cooking ideas and tools to organize meals. It does not replace individual care or a personalized nutrition plan.'),
        ('What do I receive?','Four English PDFs: the main guide and three companions. Together they contain 36 recipes, four weeks of meal examples, shopping and preparation pages, and printable planning tools.'),
        ('Where are the four weeks?','Weeks 1-2 are in the main guide. The 28-Day Meal Plan brings all four weeks together, with a shopping list for each week. Recipe numbers continue across the main guide and Recipe Pack Volume 2.'),
        ('Can I use the PDFs on my phone?','Yes, in a PDF reader. Fixed page layouts need zoom for comfortable reading of recipes and tables. Some mobile readers do not open links between PDFs; recipe and page references also let you navigate manually.'),
        ('Can I print the planning sheets?','Yes. Print only the pages you need. Choose A4 or US Letter, Fit to printable area and black-and-white for the planning sheets. The Weekly Meal Planner uses landscape; the other sheets use portrait. You can also write on them in a PDF annotation app. They are static sheets, not interactive form fields.'),
        ('Is this a subscription?','The planned offer is US$20 for the four-PDF collection, as a one-time purchase. Checkout and delivery details will be available when purchasing opens.' if not config.get('checkout_url') else 'The collection is offered as a one-time US$20 purchase. Review the checkout for delivery details and any applicable taxes.'),
        ('What if it is not right for me?',f'Email hello@boredoftoast.com within 14 days of your purchase for a full refund. No reason needed. Details are in our <a href="{root}terms/">Terms of Use</a>.'),
        ('Why pay if the recipes on this site are free?','The site recipes, collections and Small-Plate Week stay free. Nourished gathers 36 numbered recipes, four weeks of meal examples that refer to them, weekly shopping lists, prep notes and printable sheets in four PDFs. If browsing the site already covers what you need, you do not need it.'),
        ('Can I try a sample first?',f'Yes. <a href="#print">Open the free Weekly Meal Planner sheet</a> now, or <a href="{root}starter-kit/">see the 9-page Starter Kit</a>. The kit page shows its current delivery availability.')])
    body=f'''<div class="nourished-sales">
<section class="commerce-hero commerce-hero-paid nourished-hero"><div class="container nourished-hero-grid"><div class="nourished-hero-copy"><p class="eyebrow">The GLP-1 Kitchen Companion / By Bored of Toast</p><h1>Nourished</h1><p class="nourished-subtitle">Know what to cook this week, <em>even when your appetite is small.</em></p><p class="commerce-lead">Small plates, big protein. Recipes, flexible meal examples and shopping lists for adults using GLP-1 medication.</p></div><div class="nourished-bundle-stage">{bundle}<p class="nourished-bundle-caption">One collection. Four PDFs to keep.</p></div><div class="nourished-hero-purchase"><p class="nourished-purchase-benefit">Choose what to cook. Adapt your week. Know what to buy.</p><div class="commerce-price">US$20 <span>One-time purchase · Main guide + 3 bonuses</span></div><div class="commerce-actions">{checkout_action(config)}<a class="commerce-text-link" href="#preview">Look inside ↓</a></div><p class="commerce-small">{checkout_note(config)}</p><div class="nourished-guarantee"><strong>Try it for 14 days.</strong>If Nourished isn’t right for you, email us within 14 days for a full refund. No reason needed.</div></div></div></section>
<div class="nourished-facts"><div class="container"><span>Four English PDFs</span><span>36 small-plate recipes</span><span>4 weeks of meal examples</span><span>14-day refund</span></div></div>
<section class="container nourished-benefits" aria-label="Inside the collection"><article><h2>Small plates, protein first.</h2><p>Breakfasts, mains, soups and snacks, with portions and protein estimates.</p></article><article><h2>Ideas for low-appetite days.</h2><p>Sips, spoon foods and soft bites to help you choose what to make.</p></article><article><h2>A simpler shopping routine.</h2><p>Weekly lists and prep notes connected to the meal examples.</p></article></section>
<section class="section bg-paper" id="preview"><div class="container"><div class="section-head"><div><p class="eyebrow">See what you will use</p><h2>Real pages. Practical details.</h2><p>Explore a recipe, a shopping list and a week of meal examples. Open any page to read it at full size.</p></div></div><div class="commerce-preview-grid">{previews}</div></div></section>
<section class="container section" id="collection"><p class="eyebrow">One collection / Four useful parts</p><h2>Your guide + three useful bonuses.</h2><p class="nourished-section-intro">Start with the guide. Use the included bonuses for more recipe ideas, weekly examples and space to plan your own meals.</p><div class="nourished-product-grid">{packs}</div><p class="nourished-collection-note">All four PDFs are included in the US$20 one-time purchase. Read on your device or print the pages you need.</p></section>
<section class="container section" id="why-nourished"><div class="nourished-why"><div><p class="eyebrow">From browsing to planning</p><h2>Your recipes, weeks<br><em>and shopping, connected.</em></h2><p>The site’s recipes, guides, collections and Small-Plate Week stay free. Nourished brings its 36 numbered recipes, four weeks of meal examples and weekly shopping lists together in files you can keep.</p><a class="commerce-text-link" href="{root}starter-kit/">Prefer a small introduction? See the free Starter Kit →</a></div><ol><li><strong>Choose a recipe.</strong><span>Find ingredients, portions, instructions and nutrition estimates together.</span></li><li><strong>Make the week your own.</strong><span>Use the numbered meal examples as a starting point and adapt them to your own food and portions.</span></li><li><strong>Check your kitchen, then shop.</strong><span>Use the week’s list and prep notes, then write your own plan on a printable sheet.</span></li></ol></div></section>
<section class="container section" id="fit"><div class="section-head"><div><p class="eyebrow">An honest check</p><h2>Is Nourished<br><em>right for you?</em></h2></div></div><div class="commerce-feature-grid"><article><h3>A good fit if you…</h3><ul><li>want ready recipes in smaller portions, with protein estimates</li><li>like having the week planned, with shopping lists already done</li><li>need gentle options for days when your appetite is low</li><li>prefer pages you can print and keep in the kitchen</li></ul></article><article><h3>Probably not for you if…</h3><ul><li>you want a personalized diet or calorie targets</li><li>you are looking for medical or dosing guidance</li><li>you only want an app or interactive tracker</li></ul><p class="commerce-small">For personal nutrition goals, your doctor, dietitian or care team is the right place to start.</p></article></div></section>
<section class="container section" id="buying"><div class="section-head"><div><p class="eyebrow">{'Before you buy' if config.get('checkout_url') else 'When purchasing opens'}</p><h2>How buying<br><em>works.</em></h2>{'' if config.get('checkout_url') else '<p>Purchasing is not open yet. This summary follows our current Terms of Use, and we will update it if any detail changes before purchasing opens.</p>'}</div></div><div class="commerce-feature-grid"><article><h3>Payment</h3><p>Checkout is handled by Lemon Squeezy, our reseller and merchant of record. Prices are in US dollars, and any sales tax or VAT for your location is calculated at checkout.</p></article><article><h3>Your files</h3><p>Lemon Squeezy emails your receipt and download access for the four PDFs. The license covers your own household, so please do not share or resell the files.</p></article><article><h3>Help and refunds</h3><p>For questions, or a refund within 14 days of purchase, email hello@boredoftoast.com. Refunds go back to your original payment method, and no reason is needed. Full details are in our <a href="{root}terms/">Terms of Use</a>.</p></article></div></section>
<section class="container section"><div class="commerce-offer">{offer_covers}<p class="eyebrow">Nourished - The GLP-1 Kitchen Companion</p><h2>Your next kitchen steps,<br><em>in one collection.</em></h2><p>The main guide and all three bonuses. Four English PDFs, ready to save or print.</p><p class="nourished-offer-summary">36 recipes · 4 weeks of meal examples · 11 printable sheets</p><a class="commerce-text-link" href="#collection">See everything included ↑</a><div class="commerce-price">US$20 <span>One-time purchase</span></div>{checkout_action(config)}<p class="commerce-small">{checkout_note(config)}</p><p class="commerce-small"><strong>14-day refund.</strong> If it is not right for you, email us within 14 days for a full refund. No reason needed.</p><a class="commerce-text-link" href="{root}starter-kit/">See the free Starter Kit</a></div></section>
<section class="section bg-paper" id="print"><div class="container commerce-print-layout"><a class="commerce-print-preview" href="{root}printables/nourished-weekly-planner-sample.pdf" target="_blank" rel="noopener" aria-label="Open the one-page Weekly Meal Planner PDF"><img src="{root}images/commerce/printable-preview.jpg" alt="A blank Weekly Meal Planner from the Printable Pack, with space for meals, portions and additions" width="1000" height="773" loading="lazy" decoding="async"></a><div><p class="eyebrow">On your screen. On your kitchen counter.</p><h2>Print the pages<br><em>you will use.</em></h2><p>Keep the collection on your device, then print a recipe, shopping list or planning sheet when you need it. The Printable Pack includes 11 sheets made for handwriting.</p><p>Try the Weekly Meal Planner now: one free sheet from the full collection, ready for your own meals, portions and additions.</p><div class="commerce-actions"><a class="btn btn-outline" href="{root}printables/nourished-weekly-planner-sample.pdf" target="_blank" rel="noopener">Open printable sample ↗</a><a class="commerce-text-link" href="{root}printables/nourished-weekly-planner-sample.pdf" download>Download the PDF</a></div><p class="commerce-small">1-page PDF · A4 or US Letter · Landscape · Fit to printable area. Open the PDF and use your reader’s Print option. Black-and-white is suitable for this sheet.</p></div></div></section>
<section class="container section commerce-faq"><p class="eyebrow">Before you choose</p><h2>A few useful answers.</h2><div class="faq">{faq}</div></section>
<section class="container commerce-disclaimer"><p>General cooking and planning education, not medical advice or a personalized diet. Nutrition values are estimates; brands, substitutions and portions change them. Discuss your individual needs with your care team.</p></section></div>{sticky_bar(config)}'''
    page('nourished/','Nourished GLP-1 Kitchen Companion - US$20 | Bored of Toast','Explore 36 recipes, four weeks of meal examples and shopping, preparation and printable tools. Four English PDFs by Bored of Toast, US$20.',body,'cookbooks',root,og='images/commerce/nourished-cover.jpg')
    root='../../'
    body=f'''<section class="container section commerce-thanks"><p class="eyebrow">The GLP-1 Kitchen Starter Kit</p><h1>Your next few<br><em>kitchen decisions.</em></h1><p>Keep the recipe samples and organizer handy when choosing what to make.</p>{action(config,'download','Download the free kit')}<p class="commerce-small">{'9-page PDF in English. Follow the download page to save your copy.' if config.get('download_url') else 'No kit download is connected to this page yet. Check the starter kit page for current delivery options. Visiting this page alone does not confirm an email signup.'}</p>{'' if config.get('download_url') else kit_action({},root)}<a class="commerce-text-link" href="../">Back to the starter kit</a></section>{marketing_block(root,'paid')}'''
    page('starter-kit/thanks/','Your GLP-1 Kitchen Starter Kit | Bored of Toast','Save the free kitchen starter kit and explore Nourished.',body,'starter-kit',root,head_extra='<meta name="robots" content="noindex">',og='images/commerce/starter-cover.jpg')

def starter_cta(root, config):
    """update_037: Starter Kit CTA placed before the footer on library, guide and week pages."""
    live = bool(config.get('signup_url') or config.get('download_url'))
    note = ('Free 9-page English PDF. General cooking education.' if live else
            'Full-kit delivery opens soon. The kit page has a separate one-page planning sheet you can open now.')
    return f'''<section class="container section commerce-promo-wrap" data-starter-cta><div class="commerce-promo commerce-promo-free">
<div class="commerce-promo-art">{picture(root, 'starter-cover', 'Cover of the free GLP-1 Kitchen Starter Kit')}</div>
<div><p class="eyebrow">Free Starter Kit</p>
<h2>Want a few recipes in one file?<br><em>Start with the free Starter Kit.</em></h2>
<p>The GLP-1 Kitchen Starter Kit has three sample recipes from Nourished, a shopping checklist, and a worked example with a blank organizer for planning your own days.</p>
<div class="commerce-actions"><a href="{root}starter-kit/" class="btn btn-dark">See the free Starter Kit</a></div>
<p class="commerce-small">{note}</p></div>
</div></section>'''

def sticky_bar(config):
    """update_041: mobile-only purchase bar on the Nourished page."""
    url = config.get('checkout_url')
    if url:
        btn = '<a class="btn btn-yellow" href="' + e(url, quote=True) + '">Get it</a>'
    else:
        btn = '<a class="btn btn-yellow" href="#collection">Look inside</a>'
    return ('<div class="nourished-sticky" role="region" aria-label="Nourished purchase">'
            '<div><strong>Nourished</strong><span>US$20 · 14-day refund</span></div>' + btn + '</div>')
