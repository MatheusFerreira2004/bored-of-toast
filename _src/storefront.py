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
    return f'<img src="{root}images/commerce/{name}.jpg" alt="{e(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async" width="760" height="{1647 if name.startswith("starter") else 984}">'

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
    return f'<a class="btn btn-dark" href="{root}printables/nourished-weekly-planner-sample.pdf" target="_blank" rel="noopener">Try a free planning sheet ↗</a>'

def kit_note(config):
    if config.get('signup_url'):
        return 'The signup page explains how to receive the 9-page kit and manage your email preferences.'
    if config.get('download_url'):
        return 'Free 9-page English PDF. Follow the download page to save your copy.'
    return 'The full 9-page kit delivery is not open yet. The button opens a separate, one-page Weekly Meal Planner sample from Nourished; no signup is required for that sheet.'

def checkout_action(config):
    if config.get('checkout_url'):
        return action(config, 'checkout', 'Get the full collection', 'btn-yellow')
    return '<a class="btn btn-yellow" href="#print">Try the free planner</a>'

def checkout_note(config):
    return ('One-time purchase. Review checkout for delivery details and any applicable taxes.'
            if config.get('checkout_url') else 'Purchasing is not open yet. Explore the collection or try the free planning sheet below.')

def marketing_block(root, kind):
    free = kind == 'free'
    return f'''<section class="container section commerce-promo-wrap"><div class="commerce-promo {'commerce-promo-free' if free else 'commerce-promo-paid'}">
<div class="commerce-promo-art">{picture(root, 'starter-cover' if free else 'nourished-cover', 'Cover of the free GLP-1 Kitchen Starter Kit' if free else 'Cover of Nourished')}</div>
<div><p class="eyebrow">{'A free taste of Nourished' if free else 'A cookbook collection by Bored of Toast'}</p>
<h2>{'Start with three recipes.<br><em>Make the next step easier.</em>' if free else 'Meet Nourished.<br><em>Your GLP-1 kitchen companion.</em>'}</h2>
<p>{'A free kit for adults using GLP-1 medication: three sample recipes, a shopping checklist and a three-day organizer.' if free else '36 recipes, four weeks of meal examples and practical tools for shopping, preparation and your own planning.'}</p>
<div class="commerce-actions"><a href="{root}{'starter-kit/' if free else 'nourished/'}" class="btn {'btn-dark' if free else 'btn-yellow'}">{'Explore the free kit' if free else 'Explore the collection - US$20'}</a></div>
<p class="commerce-small">{'9-page PDF in English. General cooking education.' if free else 'Main guide + 3 companion PDFs. One collection, US$20.'}</p></div>
</div></section>'''

def contextual_link(root):
    return f'<section class="commerce-context"><p class="tag">Cooking while using GLP-1?</p><h3>Explore the free Nourished sampler.</h3><p>A 9-page English PDF with three sample recipes, a shopping checklist and a three-day organizer.</p><a class="view-all" href="{root}starter-kit/">Explore the free starter kit →</a></section>'

def build_storefront(page, config):
    root = '../'
    cover = picture(root, 'starter-cover', 'Cover of The GLP-1 Kitchen Starter Kit', True)
    body = f'''<section class="commerce-hero"><div class="container commerce-hero-grid"><div>
<p class="eyebrow">Free guide / By Bored of Toast</p><h1>Three recipes.<br><em>A practical first step.</em></h1>
<p class="commerce-lead">For adults using GLP-1 medication: sample three recipes from Nourished, check what to buy and use a blank organizer for your own meals.</p>
<div class="commerce-actions"><a class="btn btn-dark" href="#get-kit">{'Get the free kit' if config.get('signup_url') or config.get('download_url') else 'Explore free sample options'}</a><a class="commerce-text-link" href="{root}nourished/">Compare with Nourished</a></div>
<p class="commerce-small">For adults using GLP-1 medication. 9 pages. English PDF.</p>{'' if config.get('signup_url') or config.get('download_url') else '<p class="commerce-small">Full-kit delivery opens soon. A free printable sample is available below.</p>'}
</div><div class="commerce-cover-stage">{cover}<span class="commerce-seal">A free<br>taste</span></div></div></section>
<section class="container section" id="inside"><div class="section-head"><div><p class="eyebrow">A useful first step</p><h2>Inside your free sampler.</h2></div></div>
<div class="commerce-feature-grid">
<article><span class="commerce-number">01</span><h3>Three ways to cook</h3><p>Overnight Protein Oats, Red Lentil &amp; Carrot Soup, and a Cold Chicken &amp; Avocado Wrap.</p></article>
<article><span class="commerce-number">02</span><h3>Shop with a checklist</h3><p>Quantities for one batch of each recipe, with space to check what is already in your kitchen.</p></article>
<article><span class="commerce-number">03</span><h3>Plan your own days</h3><p>A worked example and a blank organizer to place recipes alongside your other meals, sides and snacks.</p></article></div></section>
<section class="section bg-paper"><div class="container commerce-preview-layout"><a class="commerce-page-preview" href="{root}images/commerce/starter-example.jpg" target="_blank" rel="noopener" aria-label="Open the starter kit planning example at full size">{picture(root,'starter-example','A real page from the kit showing a three-day planning example')}</a><div><p class="eyebrow">A real page from the kit</p><h2>See how the pieces<br><em>fit together.</em></h2><p>Start with one recipe. The worked example shows how to place recipe ideas alongside your other food; the blank organizer is yours to fill in.</p><p>It is a cooking resource, not a complete three-day diet or personalized nutrition plan.</p><a class="view-all" href="{root}nourished/">Meet the full collection →</a></div></div></section>
<section class="container section" id="get-kit"><div class="commerce-signup"><p class="eyebrow">The GLP-1 Kitchen Starter Kit</p><h2>Your first few recipes,<br><em>all in one place.</em></h2><p>One free English PDF: three recipes, a shopping checklist, a worked example and a blank organizer.</p>{kit_action(config,root)}<p class="commerce-small">{kit_note(config)}</p><a class="commerce-text-link" href="{root}nourished/">Explore Nourished</a></div></section>
<section class="container commerce-disclaimer"><p>General cooking education. Choose food and portions for your own needs, and discuss personal nutrition goals with your care team. Check ingredients for allergies.</p></section>'''
    page('starter-kit/','Free GLP-1 Kitchen Starter Kit | Bored of Toast','Try three recipes from Nourished, a shopping checklist and a three-day organizer. A free English PDF for your GLP-1 kitchen.',body,'starter-kit',root,og='images/commerce/starter-cover.jpg')
    previews = ''.join(f'''<article class="commerce-preview-card"><a href="{root}images/commerce/{name}.jpg" target="_blank" rel="noopener" aria-label="Open {title.lower()} preview at full size">{picture(root,name,alt)}</a><h3>{title}</h3><p>{desc}</p><a class="view-all" href="{root}images/commerce/{name}.jpg" target="_blank" rel="noopener">View the page →</a></article>''' for name,title,alt,desc in [
        ('recipe-preview','Recipes to return to','A real Overnight Protein Oats recipe page from Nourished','Ingredients, instructions and calculated nutrition estimates, with practical recipe notes.'),
        ('shopping-preview','Shopping with a purpose','A real Week 1 shopping checklist from Nourished','Recipe amounts and buying notes, so you can check your stock before heading to the store.'),
        ('planning-preview','Your week, organized','A real Week 1 daily meal example from Nourished','Meal examples connected to recipe numbers, shopping and preparation pages.')])
    packs = ''.join(f'<article><span class="commerce-number">{n}</span><h3>{title}</h3><p>{desc}</p><span class="commerce-small">{pages} pages</span></article>' for n,title,desc,pages in [
                ('02','Meal Plan Companion','Continue into Weeks 3–4 with more meal examples, shopping checklists and prep plans.',26),
        ('03','Recipe Pack Volume 2','Add 12 more recipes to your options, with portions, side suggestions and substitutions.',18),
        ('04','Printable Pack','Write your own plans: 11 sheets for meals, shopping, freezer stock and personal records, plus an index.',12)])
    packs = f'<article class="commerce-pack-main"><div>{picture(root, "nourished-cover", "Nourished main guide cover")}</div><div><p class="eyebrow">The main guide / 89 pages</p><h3>Nourished</h3><p>Begin with 24 recipes and Weeks 1–2, then use the shopping, prep and everyday cooking guidance.</p><p class="commerce-small">The main guide is your starting point. The bonuses extend it with more examples, recipes and planning sheets.</p></div></article>' + packs
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in [
        ('Who is Nourished for?','Adults using GLP-1 medication who want practical cooking ideas and tools to organize meals. It does not replace individual care or a personalized nutrition plan.'),
        ('What do I receive?','Four English PDFs: the main guide and three companions. Together they contain 36 recipes, four weeks of meal examples, shopping and preparation pages, and printable planning tools.'),
        ('Where are the four weeks?','Weeks 1-2 are in the main guide. Weeks 3-4 are in the Meal Plan Companion. Recipe numbers continue across the main guide and Recipe Pack Volume 2.'),
        ('Can I use the PDFs on my phone?','Yes, in a PDF reader. Fixed page layouts need zoom for comfortable reading of recipes and tables. Some mobile readers do not open links between PDFs; recipe and page references also let you navigate manually.'),
        ('Can I print the planning sheets?','Yes. Print only the pages you need. Choose A4 or US Letter, Fit to printable area and black-and-white for the planning sheets. The Weekly Meal Planner uses landscape; the other sheets use portrait. You can also write on them in a PDF annotation app. They are static sheets, not interactive form fields.'),
        ('Is this a subscription?','The planned offer is US$20 for the four-PDF collection, as a one-time purchase. Checkout and delivery details will be available when purchasing opens.' if not config.get('checkout_url') else 'The collection is offered as a one-time US$20 purchase. Review the checkout for delivery details and any applicable taxes.'),
        ('Can I try a sample first?',f'Yes. <a href="#print">Open the free Weekly Meal Planner sheet</a> now, or <a href="{root}starter-kit/">explore the 9-page starter kit</a>. The kit page shows its current delivery availability.')])
    body=f'''<section class="commerce-hero commerce-hero-paid"><div class="container commerce-hero-grid"><div><p class="eyebrow">Nourished / By Bored of Toast</p><h1>Your GLP-1 kitchen,<br><em>organized.</em></h1><p class="commerce-lead">A practical cooking collection for adults using GLP-1 medication. Find recipes, check your shopping and plan what to prepare.</p><div class="commerce-price">US$20 <span>one-time purchase / main guide + 3 bonuses</span></div><div class="commerce-actions">{checkout_action(config)}<a class="commerce-text-link" href="#preview">Look inside ↓</a></div><p class="commerce-small">{checkout_note(config)}</p><p class="commerce-small commerce-facts"><span>Four English PDFs</span><span>36 recipes</span><span>4 weeks of meal examples</span><span>Read digitally or print</span></p></div><div class="commerce-cover-stage">{picture(root,'nourished-cover','Cover of Nourished - The GLP-1 Kitchen Companion',True)}<span class="commerce-seal">4 PDFs<br>One set</span></div></div></section>
<section class="container section"><div class="commerce-feature-grid"><article><h3>Find your next recipe</h3><p>Breakfasts, mains, soups and snacks, with ingredients, methods and nutrition estimates.</p></article><article><h3>Plan before you shop</h3><p>Follow recipe references from the meal examples to the shopping quantities and prep notes.</p></article><article><h3>Make the plan your own</h3><p>Use the printable sheets for your meals, shopping notes and freezer stock.</p></article></div></section>
<section class="section bg-paper" id="preview"><div class="container"><div class="section-head"><div><p class="eyebrow">See what you will use</p><h2>Real pages. Practical details.</h2><p>Open any preview for a closer look.</p></div></div><div class="commerce-preview-grid">{previews}</div></div></section>
<section class="container section" id="collection"><p class="eyebrow">One collection / Four useful parts</p><h2>Your guide + three useful bonuses.</h2><div class="commerce-pack-grid">{packs}</div></section>
<section class="section bg-paper" id="print"><div class="container commerce-print-layout"><a class="commerce-print-preview" href="{root}printables/nourished-weekly-planner-sample.pdf" target="_blank" rel="noopener" aria-label="Open the one-page Weekly Meal Planner PDF"><img src="{root}images/commerce/printable-preview.jpg" alt="A blank Weekly Meal Planner from the Printable Pack, with space for meals, portions and additions" width="1000" height="773" loading="lazy" decoding="async"></a><div><p class="eyebrow">On your screen. On your kitchen counter.</p><h2>Print the pages<br><em>you will use.</em></h2><p>Keep the collection on your device, then print a recipe, shopping list or planning sheet when you need it. The Printable Pack includes 11 sheets made for handwriting.</p><p>Try the Weekly Meal Planner now: one free sheet from the full collection, ready for your own meals, portions and additions.</p><div class="commerce-actions"><a class="btn btn-dark" href="{root}printables/nourished-weekly-planner-sample.pdf" target="_blank" rel="noopener">Open printable sample ↗</a><a class="commerce-text-link" href="{root}printables/nourished-weekly-planner-sample.pdf" download>Download the PDF</a></div><p class="commerce-small">1-page PDF · A4 or US Letter · Landscape · Fit to printable area. Open the PDF and use your reader’s Print option. Black-and-white is suitable for this sheet.</p></div></div></section>
<section class="section bg-paper"><div class="container commerce-start"><div><p class="eyebrow">Start with your next week</p><h2>A simple way<br><em>to begin.</em></h2></div><ol><li><strong>Open Start Here.</strong><span>The main guide points you to recipes, weekly examples and planning sheets.</span></li><li><strong>Choose and adapt.</strong><span>Use the examples as a starting point and add food and portions for your needs.</span></li><li><strong>Check stock, then prep.</strong><span>Use the shopping and preparation pages; record your own plan in the Printable Pack.</span></li></ol></div></section>
<section class="container section"><div class="commerce-compare"><p class="eyebrow">Start small or explore the collection</p><h2>Choose your next step.</h2><table><caption class="sr-only">Free starter kit and full Nourished collection comparison</caption><thead><tr><th scope="col">Inside</th><th scope="col">Free kit</th><th scope="col">Nourished</th></tr></thead><tbody><tr><th scope="row">Recipes</th><td>3 samples</td><td>36 recipes</td></tr><tr><th scope="row">Planning</th><td>Example + organizer</td><td>4 weeks of meal examples</td></tr><tr><th scope="row">Shopping</th><td>One sample checklist</td><td>Weekly lists + prep notes</td></tr><tr><th scope="row">Files</th><td>1 PDF</td><td>4 PDFs</td></tr><tr><th scope="row">Price</th><td>Free</td><td>US$20</td></tr></tbody></table><a class="view-all" href="{root}starter-kit/">Explore the free kit →</a></div></section>
<section class="container section commerce-faq"><p class="eyebrow">Before you choose</p><h2>A few useful answers.</h2><div class="faq">{faq}</div></section>
<section class="container section"><div class="commerce-offer"><p class="eyebrow">Nourished - The GLP-1 Kitchen Companion</p><h2>Your next kitchen steps,<br><em>in one collection.</em></h2><p>The main guide and all three bonuses. Four English PDFs, ready to save or print.</p><div class="commerce-price">US$20 <span>One-time purchase</span></div>{checkout_action(config)}<p class="commerce-small">{checkout_note(config)}</p><a class="commerce-text-link" href="{root}starter-kit/">Preview the free starter kit</a></div></section>
<section class="container commerce-disclaimer"><p>General cooking and planning education, not medical advice or a personalized diet. Nutrition values are estimates; brands, substitutions and portions change them. Discuss your individual needs with your care team.</p></section>'''
    page('nourished/','Nourished GLP-1 Kitchen Companion - US$20 | Bored of Toast','Explore 36 recipes, four weeks of meal examples and shopping, preparation and printable tools. Four English PDFs by Bored of Toast, US$20.',body,'cookbooks',root,og='images/commerce/nourished-cover.jpg')
    root='../../'
    body=f'''<section class="container section commerce-thanks"><p class="eyebrow">The GLP-1 Kitchen Starter Kit</p><h1>Your next few<br><em>kitchen decisions.</em></h1><p>Keep the recipe samples and organizer handy when choosing what to make.</p>{action(config,'download','Download the free kit')}<p class="commerce-small">{'9-page PDF in English. Follow the download page to save your copy.' if config.get('download_url') else 'No kit download is connected to this page yet. Check the starter kit page for current delivery options. Visiting this page alone does not confirm an email signup.'}</p>{'' if config.get('download_url') else kit_action({},root)}<a class="commerce-text-link" href="../">Back to the starter kit</a></section>{marketing_block(root,'paid')}'''
    page('starter-kit/thanks/','Your GLP-1 Kitchen Starter Kit | Bored of Toast','Save the free kitchen starter kit and explore Nourished.',body,'starter-kit',root,head_extra='<meta name="robots" content="noindex">',og='images/commerce/starter-cover.jpg')
