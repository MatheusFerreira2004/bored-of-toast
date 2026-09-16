"""Shared recipe renderer; enriched data lives in recipe_models.json."""
from pathlib import Path
import html,json,re
E=html.escape

def inline_amounts(text):
    return re.sub(r'\{\{amount:([\d.]+):([^}]+)\}\}',lambda m:number(float(m[1]))+' '+m[2],text)

MODELS=json.loads(Path(__file__).with_name('recipe_models.json').read_text(encoding='utf-8'))

def resolve_text(text,data):
    names={i['id']:i.get('method_name',i['name']) for i in data['ingredients']}
    return re.sub(r'\{\{(\w+)\}\}',lambda m:names[m.group(1)],inline_amounts(text))

def number(q):
    for v,t in [(1/3,'⅓'),(1/4,'¼'),(.5,'½'),(2/3,'⅔'),(3/4,'¾'),(1/8,'⅛'),(3/8,'⅜'),(5/8,'⅝'),(7/8,'⅞')]:
        if abs(q-v)<.001:return t
    return str(int(q)) if q==int(q) else f'{q:.2f}'.rstrip('0').rstrip('.')

def plain_ingredient(i):
    name = inline_amounts(i['name'])
    if 'qty' not in i:
        return name
    unit = i.get('unit', '')
    metric = f" ({i['metric']} {i.get('metric_unit', 'g')})" if i.get('metric') else ''
    qty = number(i['qty'])
    return ' '.join(p for p in [f"{qty} {unit}{metric}".strip(), name] if p)

def ingredient_text(i):
    if 'qty' not in i:
        return f'<span class="ingredient-name">{E(inline_amounts(i["name"]))}</span>'
    metric=f" ({i['metric']} {i.get('metric_unit','g')})" if i.get('metric') else ''
    unit=i['unit'] if i['unit']=='cup' and i['qty']<1 else (i.get('unit_plural',i['unit']+'s') if i['unit'] in ('cup','clove','slice') and i['qty'] != 1 else i['unit'])
    quantity=E(f"{number(i['qty'])} {unit}{metric}")
    return f'<span class="ingredient-qty"><strong>{quantity}</strong></span> <span class="ingredient-name">{E(inline_amounts(i["name"]))}</span>'

def render_swap_block(sw, iid):
    qty_str = f'{number(sw["qty"])} {sw["unit"]}' if sw.get('qty') else ''
    title = f'{E(sw["name"].capitalize())}'
    if qty_str:
        title += f' (<span data-swap-amount>{qty_str}</span>)'
    
    parts = []
    if sw.get('texture_change'): parts.append(f'<strong>Texture:</strong> {E(sw["texture_change"])}')
    if sw.get('flavor_change'): parts.append(f'<strong>Flavor:</strong> {E(sw["flavor_change"])}')
    if sw.get('how_to_adjust'): parts.append(f'<strong>Adjust:</strong> {E(sw["how_to_adjust"])}')
    if sw.get('change'): parts.append(f'<strong>Changes:</strong> {E(sw["change"])}')
    if sw.get('technique'): parts.append(f'<strong>Prep:</strong> {E(sw["technique"])}')
    
    desc = '<br>'.join(parts) if parts else ''
    note_text = sw.get('note', '')
    if not desc and note_text:
        desc = E(note_text)
        note_text = ''
        
    note_row = f'<p class="swap-note">{E(note_text)}</p>' if note_text else ''
    
    return f'''<details class="ingredient-swap"><summary>Swap option</summary><div class="swap-content swap-content--structured"><div class="swap-header"><h4>{title}</h4></div><div class="swap-changes"><p>{desc}</p></div>{note_row}<button type="button" class="button outline swap-btn" data-use-swap="{iid}">Use in this recipe</button></div></details><span class="applied-swap" data-applied-swap hidden></span><button type="button" class="undo-swap" data-undo-swap="{iid}" hidden>Undo substitution</button>'''

def render_editorial_recipe(r,others):
    d=r.get('editorial') or MODELS[r['slug']]
    rows=[]
    for i in d['ingredients']:
        if i.get('group'):rows.append(f'<li class="ingredient-subheading">{E(i["group"])}</li>')
        sw=i.get('swap')
        extra=''
        if sw:extra=render_swap_block(sw, i['id'])
        rows.append(f'''<li class="editorial-ingredient" data-ingredient-id="{i['id']}"><div class="ingredient-text">{ingredient_text(i)}</div><small class="ingredient-note">{E(i.get('note',''))}</small>{extra}</li>''')
    
    steps=[]
    for n,s in enumerate(d['steps']):
        if s.get('phase'):steps.append(f'<h3 class="method-phase">{E(s["phase"])}</h3>')
        duration=f'<p class="step-duration">{E(s["duration"])}</p>' if s.get('duration') else ''
        
        ai_badge = '<span class="ai-badge">AI-generated</span>' if s.get('is_ai_generated') else ''
        im=f'<figure class="instruction-figure"><img class="instruction-image" src="/assets/{s["image"]}" width="800" height="600" loading="lazy" alt="{E(s["alt"])}">{ai_badge}</figure>' if s.get('image') else ''
        
        check_block = ''
        if s.get('cue'):
            check_block += f'<p class="step-cue"><strong>Look for:</strong> <span data-step-cue>{E(s["cue"])}</span></p>'
        if s.get('care'):
            check_block += f'<details class="step-check" data-step-check><summary>Extra tip</summary><p class="method-care-copy"><span data-step-care>{E(s["care"])}</span></p></details>'
            
        steps.append(f'''<section class="method-step" data-method-step="{n}"><div class="method-title"><span>{n+1:02d}</span><h3>{E(s['title'])}</h3></div>{duration}{im}<p data-step-action>{E(resolve_text(s['action'],d))}</p>{check_block}</section>''')
        
    times=''.join(f'<div><dt>{E(t["label"])}</dt><dd>{E(t["value"])}</dd></div>' for t in d['times'])
    equipment=(f'<p class="equipment"><strong>You\'ll need</strong><br>'+E(' \xb7 '.join(d['equipment']))+'</p>') if d['equipment'] else ''
    
    # Extra new fields
    before_html = f'<div class="before-you-begin"><p class="eyebrow">BEFORE YOU BEGIN</p><p>{E(d["before_prep"])}</p></div>' if d.get('before_prep') else ''
    looks_html = f'<div class="if-yours-looks"><p class="eyebrow">IF YOURS LOOKS...</p><p>{E(d["if_looks"])}</p></div>' if d.get('if_looks') else ''
    batch_html = f'<div class="larger-batch"><p class="eyebrow">FOR A LARGER BATCH</p><p>{E(d["larger_batch"])}</p></div>' if d.get('larger_batch') else ''

    technique=(f'<details><summary>A small technique note</summary><p>'+E(d.get('technique',''))+f'</p></details>') if d.get('technique') else ''
    
    source_html = ''
    if d.get('sources'):
        src_links = ''
        for s in d['sources']:
            note = f" &mdash; {E(s['note'])}" if s.get('note') else ''
            src_links += f'<li><a href="{E(s["url"])}" target="_blank" rel="noopener nofollow">{E(s["title"])}</a> by {E(s["publisher"])}{note}</li>'
        source_html = f'<details id="sources"><summary>Sources & References</summary><ul class="sources-list">{src_links}</ul></details>'
    elif d.get('source'):
        source_html = f'<details><summary>Sources</summary><p><a href="{E(d["source"],quote=True)}" target="_blank" rel="noopener nofollow">Food storage guidance &middot; FDA ↗</a></p></details>'

    faq_html = ''
    if d.get('faq'):
        faqs = ''.join(f'<details class="faq-item"><summary>{E(q["question"])}</summary><p>{E(q["answer"])}</p></details>' for q in d['faq'])
        faq_html = f'<section class="recipe-faq"><h2>Frequently Asked Questions</h2>{faqs}</section>'

    nutrition_html = ''
    if d.get('nutrition'):
        nut = d['nutrition']
        est = '<p class="nutrition-est">These values are automated estimates.</p>' if nut.get('is_estimate') else ''
        rows = f'''
            <div class="nut-row"><span>Calories</span><span>{E(str(nut.get("calories", "")))}</span></div>
            <div class="nut-row"><span>Protein</span><span>{E(str(nut.get("protein_g", "")))}g</span></div>
            <div class="nut-row"><span>Carbs</span><span>{E(str(nut.get("carbs_g", "")))}g</span></div>
            <div class="nut-row"><span>Fat</span><span>{E(str(nut.get("fat_g", "")))}g</span></div>
            <div class="nut-row"><span>Fiber</span><span>{E(str(nut.get("fiber_g", "")))}g</span></div>
            <div class="nut-row"><span>Sodium</span><span>{E(str(nut.get("sodium_mg", "")))}mg</span></div>
        '''
        nutrition_html = f'<section class="recipe-nutrition"><h2>Nutrition Per Serving</h2>{est}<div class="nutrition-table">{rows}</div></section>'

    data_json=json.dumps(d).replace('<','\\u003c')

    why_html = ''
    why = r.get('why_it_works') or d.get('why_it_works', '')
    if why:
        why_html = f'<p class="why-it-works"><strong>Why it works:</strong> {E(why)}</p>'
        
    byline_html = ''
    if d.get('author_name'):
        byline_html = f'''<div class="recipe-byline">
            <div class="byline-avatar"></div>
            <div class="byline-info">
                <span class="byline-name">By {E(d["author_name"])}</span>
                <span class="byline-date">Published {E(d.get("date_published", ""))}</span>
            </div>
        </div>'''
        
    intro_html = f'<p class="recipe-intro">{E(d["intro"])}</p>' if d.get('intro') else f'<p class="lead">{E(r["desc"])}</p>'
    
    ad_content = '<div class="ad-container ad-in-content" aria-hidden="true"><span class="ad-label">Advertisement</span></div>'
    ad_footer = '<div class="ad-container ad-footer" aria-hidden="true"><span class="ad-label">Advertisement</span></div>'
    newsletter = '''<section class="recipe-newsletter">
        <h3>More everyday ideas.</h3>
        <p>Join the newsletter for new recipes and kitchen notes every week.</p>
        <form class="newsletter-form" action="#" method="post">
            <input type="email" placeholder="Your email address" required aria-label="Email address">
            <button class="button" type="submit">Subscribe</button>
        </form>
    </section>'''

    cats = r.get('categories', [])
    from constants import CAT_LABEL
    top_cats = cats[:2]
    bottom_cats = cats[2:]
    
    cat_tags = ''
    if top_cats:
        links = ''.join(f'<a class="recipe-cat-tag" href="/recipes/?category={c}">{E(CAT_LABEL.get(c, c))}</a>' for c in top_cats)
        cat_tags = f'<div class="recipe-cat-tags" aria-label="Recipe categories">{links}</div>'
        
    bottom_cat_tags = ''
    if bottom_cats:
        links = ''.join(f'<a class="recipe-cat-tag" href="/recipes/?category={c}">{E(CAT_LABEL.get(c, c))}</a>' for c in bottom_cats)
        bottom_cat_tags = f'<div class="recipe-cat-tags additional-cats"><p class="eyebrow">MORE CATEGORIES</p>{links}</div>'

    related_notes_html = ''
    related_notes = r.get('related_notes', [])
    if related_notes:
        from kitchen_notes import GUIDES as KN_GUIDES
        kn_map = {g['slug']: g for g in KN_GUIDES}
        note_links = ''
        for slug in related_notes:
            if slug in kn_map:
                g = kn_map[slug]
                note_links += f'<a class="related-note-link" href="/kitchen-notes/{slug}/"><span class="eyebrow">KITCHEN NOTE</span><strong>{E(g["title"])}</strong></a>'
        if note_links:
            related_notes_html = f'<section class="recipe-related-notes"><p class="eyebrow">USEFUL TECHNIQUE</p><h2>Kitchen Notes</h2>{note_links}</section>'

    lunch_cta = '''<aside class="lunch-edit-cta" aria-label="About The Lunch Edit">
  <p class="eyebrow">ON THE BACK BURNER</p>
  <h3>The Lunch Edit</h3>
  <p>A digital collection in development: four flexible weeks of lunches, twenty recipes, and coordinated shopping lists. Not available yet.</p>
  <a class="text-link" href="/the-lunch-edit/">A peek at the idea ↗</a>
</aside>'''

    serve_html = ''
    if d.get('serve'):
        serve_title = d.get('serve_title', 'Serve with')
        serve_html = f'<h2>{E(serve_title)}</h2><p>{E(d["serve"])}</p>'

    return f'''<section class="editorial-recipe wrap" id="pilot-recipe" data-pilot-recipe="{r['slug']}">
    <a class="breadcrumb" href="/recipes/">← All recipes</a>
    <div class="editorial-header-grid">
        <div class="editorial-header-content">
            {cat_tags}
            <h1>{E(r['title'])}</h1>
            {byline_html}
            {intro_html}
                        <dl class="recipe-time-grid" aria-label="Estimated recipe times">{times}</dl>
            <div class="recipe-actions">
                <a class="button" href="#recipe">Ingredients & Method ↓</a>
                <button class="button discreet outline" type="button" data-print>Print</button>
            </div>
            { '<p class="small transparency-note">Development edition &middot; Awaits kitchen testing.</p>' if d.get('status') == 'development' else '' }
        </div>
        <div class="editorial-header-visual">
            <figure>
                <img src="/assets/{r['img']}" alt="{E(r['alt'])}" width="800" height="600">
                { '<span class="ai-badge">AI-generated illustration</span>' if d.get('hero_image', {}).get('is_ai_generated') else '' }
            </figure>
        </div>
    </div>
    <nav class="recipe-local-nav" aria-label="On this recipe">
        <a href="#recipe">Ingredients</a>
        <a href="#method">Method</a>
        <a href="#storage">Storage</a>
    </nav>
    <div class="editorial-body-grid" id="recipe">
        <section class="editorial-ingredients-col">
            <div class="ingredients-header">
                <h2 class="editorial-section-title">Ingredients</h2>
                <div class="people-panel compact">
                    <div class="servings-control" data-default-servings="{d['base_people']}">
                        <span class="servings-label">How many people?</span>
                        <div class="servings-stepper">
                            <button class="servings-btn" type="button" data-servings-step="-1" aria-label="Fewer people">−</button>
                            <output class="servings-count" data-servings-count aria-live="polite">{d['base_people']}</output>
                            <button class="servings-btn" type="button" data-servings-step="1" aria-label="More people">+</button>
                        </div>
                        <button type="button" data-servings-reset class="servings-reset" hidden>Reset</button>
                    </div>
                </div>
            </div>
            {batch_html}
            <p data-yield-note class="small">Estimated to serve {d['base_people']} people as {E(d['meal_role'])}.</p>
            <ul class="editorial-ingredients-list" data-recipe-slug="{r['slug']}">{''.join(rows)}</ul>
            <p class="allergen-note" data-allergen>{E(d['allergen'])}</p>
            <p class="small" aria-live="polite" data-change-status></p>
        </section>
        <section class="editorial-method-col" id="method">
            {ad_content}
            <h2 class="editorial-section-title">Method</h2>
            {equipment}
            {before_html}
            {''.join(steps)}
            {looks_html}
        </section>
    </div>
    <section class="recipe-finish">
        {why_html}
        {serve_html}
        {faq_html}
        {nutrition_html}
        <details><summary>One way to change it up</summary><p>{E(d['variation'])}</p></details>
        {technique}
        <details id="storage"><summary>Storage & Prep ahead</summary><p>{E(d['ahead'])}</p><p>{E(d['storage'])}</p></details>
        {source_html}
    </section>
    {related_notes_html}
    {bottom_cat_tags}
    {lunch_cta}
    {ad_footer}
    {newsletter}
    <script type="application/json" id="pilot-recipe-data">{data_json}</script>
</section>'''
