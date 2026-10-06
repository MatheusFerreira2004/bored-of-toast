"""Nourished storefront templates. Empty integration URLs render honest coming-soon states."""
from html import escape as e
from urllib.parse import urlparse

def validate_config(config):
    for key in ('signup_url', 'download_url', 'checkout_url'):
        value = config.get(key)
        if value is not None and (not isinstance(value, str) or urlparse(value).scheme != 'https' or not urlparse(value).netloc):
            raise ValueError(f'{key} must be null or an absolute HTTPS URL')
    return config

def picture(root, name, alt, eager=False):
    return f'<img src="{root}images/commerce/{name}.jpg" alt="{e(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async" width="760" height="{1647 if name.startswith("starter") else 984}">'

def action(config, kind, label, style='btn-dark'):
    url = config.get(kind + '_url')
    if url:
        return f'<a class="btn {style}" href="{e(url, quote=True)}">{e(label)}</a>'
    unavailable = {'signup': 'Email signup opens soon', 'download': 'Download opens soon', 'checkout': 'Purchase opens soon'}[kind]
    return f'<span class="commerce-status">{unavailable}</span>'

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
    return f'<section class="commerce-context"><p class="tag">Cooking while using GLP-1?</p><h3>Try a small start from Nourished.</h3><p>Three sample recipes, one shopping checklist and a place to plan.</p><a class="view-all" href="{root}starter-kit/">Explore the free starter kit →</a></section>'

def build_storefront(page, config):
    root = '../'
    cover = picture(root, 'starter-cover', 'Cover of The GLP-1 Kitchen Starter Kit', True)
    body = f'''<section class="commerce-hero"><div class="container commerce-hero-grid"><div>
<p class="eyebrow">Free guide / By Bored of Toast</p><h1>A small start.<br><em>A more organized kitchen.</em></h1>
<p class="commerce-lead">Try three recipes from Nourished, then use a shopping checklist and a three-day organizer to make your next few kitchen decisions easier.</p>
<div class="commerce-actions"><a class="btn btn-dark" href="#get-kit">Explore the free kit</a><a class="commerce-text-link" href="#inside">See what's inside ↓</a></div>
<p class="commerce-small">For adults using GLP-1 medication. 9 pages. English PDF.</p>
</div><div class="commerce-cover-stage">{cover}<span class="commerce-seal">A free<br>taste</span></div></div></section>
<section class="container section" id="inside"><div class="section-head"><div><p class="eyebrow">A useful first step</p><h2>Small enough to start today.</h2></div></div>
<div class="commerce-feature-grid">
<article><span class="commerce-number">01</span><h3>Three ways to cook</h3><p>Overnight Protein Oats, Red Lentil &amp; Carrot Soup, and a Cold Chicken &amp; Avocado Wrap.</p></article>
<article><span class="commerce-number">02</span><h3>Shop with a checklist</h3><p>Quantities for one batch of each recipe, with space to check what is already in your kitchen.</p></article>
<article><span class="commerce-number">03</span><h3>Plan your own days</h3><p>A worked example and a blank organizer to place recipes alongside your other meals, sides and snacks.</p></article></div></section>
<section class="section bg-paper"><div class="container commerce-preview-layout"><a class="commerce-page-preview" href="{root}images/commerce/starter-example.jpg" target="_blank" rel="noopener" aria-label="Open the starter kit planning example at full size">{picture(root,'starter-example','A real page from the kit showing a three-day planning example')}</a><div><p class="eyebrow">A real page from the kit</p><h2>See how the pieces<br><em>fit together.</em></h2><p>This kit is a sample of the full Nourished collection. Start with one recipe, check your stock and use the organizer for the rest of your food.</p><p>It is a cooking resource, not a complete three-day diet or personalized nutrition plan.</p><a class="view-all" href="{root}nourished/">Meet the full collection →</a></div></div></section>
<section class="container section" id="get-kit"><div class="commerce-signup"><p class="eyebrow">The GLP-1 Kitchen Starter Kit</p><h2>Your first few recipes,<br><em>all in one place.</em></h2><p>Three sample recipes, shopping quantities and a practical organizer.</p>{action(config,'signup','Send me the free kit')}<p class="commerce-small">{'Follow the signup page for delivery details and your email preferences.' if config.get('signup_url') else 'We are preparing the free kit delivery. You can explore the collection in the meantime.'}</p><a class="commerce-text-link" href="{root}nourished/">Explore Nourished</a></div></section>
<section class="container commerce-disclaimer"><p>General cooking education. Choose food and portions for your own needs, and discuss personal nutrition goals with your care team. Check ingredients for allergies.</p></section>'''
    page('starter-kit/','Free GLP-1 Kitchen Starter Kit | Bored of Toast','Try three recipes from Nourished, a shopping checklist and a three-day organizer. A free English PDF for your GLP-1 kitchen.',body,'starter-kit',root,og='images/commerce/starter-cover.jpg')
    previews = ''.join(f'''<article class="commerce-preview-card"><a href="{root}images/commerce/{name}.jpg" target="_blank" rel="noopener" aria-label="Open {title.lower()} preview at full size">{picture(root,name,alt)}</a><h3>{title}</h3><p>{desc}</p><a class="view-all" href="{root}images/commerce/{name}.jpg" target="_blank" rel="noopener">View the page →</a></article>''' for name,title,alt,desc in [
        ('recipe-preview','Recipes to return to','A real Overnight Protein Oats recipe page from Nourished','Ingredients, instructions and calculated nutrition estimates, with practical recipe notes.'),
        ('shopping-preview','Shopping with a purpose','A real Week 1 shopping checklist from Nourished','Recipe amounts and buying notes, so you can check your stock before heading to the store.'),
        ('planning-preview','Your week, organized','A real Week 1 daily meal example from Nourished','Meal examples connected to recipe numbers, shopping and preparation pages.')])
    packs = ''.join(f'<article><span class="commerce-number">{n}</span><h3>{title}</h3><p>{desc}</p><span class="commerce-small">{pages} pages</span></article>' for n,title,desc,pages in [
                ('02','Meal Plan Companion','Weeks 3-4, with daily meal examples, shopping checklists and prep plans.',34),
        ('03','Recipe Pack Volume 2','12 more recipes, plus portions, sides and substitutions.',18),
        ('04','Printable Pack','11 printable sheets plus an index: meal planning, shopping, freezer stock and personal records.',12)])
    packs = f'<article class="commerce-pack-main"><div>{picture(root, "nourished-cover", "Nourished main guide cover")}</div><div><p class="eyebrow">The main guide / 93 pages</p><h3>Nourished</h3><p>24 recipes, Weeks 1–2, preparation, shopping and everyday cooking guidance.</p><p class="commerce-small">Start here, then use the three companions below.</p></div></article>' + packs
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in [
        ('Who is Nourished for?','Adults using GLP-1 medication who want practical cooking ideas and tools to organize meals. It does not replace individual care or a personalized nutrition plan.'),
        ('What do I receive?','Four English PDFs: the main guide and three companions. Together they contain 36 recipes, four weeks of meal examples, shopping and preparation pages, and printable planning tools.'),
        ('Where are the four weeks?','Weeks 1-2 are in the main guide. Weeks 3-4 are in the Meal Plan Companion. Recipe numbers continue across the main guide and Recipe Pack Volume 2.'),
        ('Can I use the PDFs on my phone?','Yes, in a PDF reader. Fixed page layouts need zoom for comfortable reading of recipes and tables. Some mobile readers do not open links between PDFs; recipe and page references also let you navigate manually.'),
        ('Can I print the planning sheets?','Yes. The Printable Pack is designed for handwriting or PDF annotation. Its sheets are static, not interactive form fields.'),
        ('Is this a subscription?','The planned offer is US$20 for the four-PDF collection, as a one-time purchase. Checkout and delivery details will be available when purchasing opens.' if not config.get('checkout_url') else 'The collection is offered as a one-time US$20 purchase. Review the checkout for delivery details and any applicable taxes.'),
        ('Can I try a sample first?',f'Yes. Explore the <a href="{root}starter-kit/">free GLP-1 Kitchen Starter Kit</a>, with three recipe samples, a shopping checklist and a planning organizer.')])
    body=f'''<section class="commerce-hero commerce-hero-paid"><div class="container commerce-hero-grid"><div><p class="eyebrow">Nourished / By Bored of Toast</p><h1>Your GLP-1 kitchen,<br><em>with a little more direction.</em></h1><p class="commerce-lead">Recipes, shopping checklists and meal-planning tools to help you decide what to prepare and organize the next steps.</p><div class="commerce-price">US$20 <span>for the full four-PDF collection</span></div><div class="commerce-actions">{action(config,'checkout','Get the full collection','btn-yellow')}<a class="commerce-text-link" href="#preview">Look inside ↓</a></div><p class="commerce-small commerce-facts"><span>36 recipes</span><span>4 weeks of meal examples</span><span>English PDFs</span></p></div><div class="commerce-cover-stage">{picture(root,'nourished-cover','Cover of Nourished - The GLP-1 Kitchen Companion',True)}<span class="commerce-seal">4 PDFs<br>1 collection</span></div></div></section>
<section class="container section"><div class="commerce-feature-grid"><article><h3>Choose what to prepare</h3><p>Browse small recipes and practical options for breakfast, mains, soups and snacks.</p></article><article><h3>Connect meals and shopping</h3><p>Use meal examples with recipe numbers, shopping quantities and preparation notes.</p></article><article><h3>Keep your own records</h3><p>Printable tools help you plan, check freezer stock and record questions for your care team.</p></article></div></section>
<section class="section bg-paper" id="preview"><div class="container"><div class="section-head"><div><p class="eyebrow">See what you will use</p><h2>Real pages. Practical details.</h2><p>Open any preview for a closer look.</p></div></div><div class="commerce-preview-grid">{previews}</div></div></section>
<section class="container section" id="collection"><p class="eyebrow">One collection / Four useful parts</p><h2>Everything works together.</h2><div class="commerce-pack-grid">{packs}</div></section>
<section class="section bg-paper"><div class="container commerce-start"><div><p class="eyebrow">Start with your next week</p><h2>A simple way<br><em>to begin.</em></h2></div><ol><li><strong>Open Start Here.</strong><span>The main guide points you to recipes, weekly examples and planning sheets.</span></li><li><strong>Choose and adapt.</strong><span>Use the examples as a starting point and add food and portions for your needs.</span></li><li><strong>Check stock, then prep.</strong><span>Use the shopping and preparation pages; record your own plan in the Printable Pack.</span></li></ol></div></section>
<section class="container section"><div class="commerce-compare"><p class="eyebrow">Start small or explore the collection</p><h2>Choose your next step.</h2><table><caption class="sr-only">Free starter kit and full Nourished collection comparison</caption><thead><tr><th scope="col">Inside</th><th scope="col">Free kit</th><th scope="col">Nourished</th></tr></thead><tbody><tr><th scope="row">Recipes</th><td>3 samples</td><td>36 recipes</td></tr><tr><th scope="row">Planning</th><td>Example + organizer</td><td>4 weeks of meal examples</td></tr><tr><th scope="row">Shopping</th><td>One sample checklist</td><td>Weekly lists + prep notes</td></tr><tr><th scope="row">Files</th><td>1 PDF</td><td>4 PDFs</td></tr><tr><th scope="row">Price</th><td>Free</td><td>US$20</td></tr></tbody></table><a class="view-all" href="{root}starter-kit/">Explore the free kit →</a></div></section>
<section class="container section commerce-faq"><p class="eyebrow">Before you choose</p><h2>A few useful answers.</h2><div class="faq">{faq}</div></section>
<section class="container section"><div class="commerce-offer"><p class="eyebrow">Nourished - The GLP-1 Kitchen Companion</p><h2>Recipes, planning and prep.<br><em>One place to start.</em></h2><p>Main guide + Meal Plan Companion + Recipe Pack Volume 2 + Printable Pack.</p><div class="commerce-price">US$20</div>{action(config,'checkout','Get the full collection','btn-yellow')}<p class="commerce-small">{'See checkout for delivery details and any applicable taxes.' if config.get('checkout_url') else 'Purchasing is not open yet. Explore the free starter kit while we prepare the collection launch.'}</p><a class="commerce-text-link" href="{root}starter-kit/">Try the free starter kit</a></div></section>
<section class="container commerce-disclaimer"><p>General cooking and planning education, not medical advice or a personalized diet. Nutrition values are estimates; brands, substitutions and portions change them. Discuss your individual needs with your care team.</p></section>'''
    page('nourished/','Nourished GLP-1 Kitchen Companion - US$20 | Bored of Toast','Explore 36 recipes, four weeks of meal examples and shopping, preparation and printable tools. Four English PDFs by Bored of Toast, US$20.',body,'cookbooks',root,og='images/commerce/nourished-cover.jpg')
    root='../../'
    body=f'''<section class="container section commerce-thanks"><p class="eyebrow">The GLP-1 Kitchen Starter Kit</p><h1>Your next few<br><em>kitchen decisions.</em></h1><p>Keep the recipe samples and organizer handy when choosing what to make.</p>{action(config,'download','Download the free kit')}<p class="commerce-small">{'9-page PDF in English. Save it to your device for later.' if config.get('download_url') else 'Kit delivery is not open yet. This page does not confirm an email signup.'}</p><a class="commerce-text-link" href="../">Back to the starter kit</a></section>{marketing_block(root,'paid')}'''
    page('starter-kit/thanks/','Your GLP-1 Kitchen Starter Kit | Bored of Toast','Save the free kitchen starter kit and explore Nourished.',body,'starter-kit',root,head_extra='<meta name="robots" content="noindex">',og='images/commerce/starter-cover.jpg')
