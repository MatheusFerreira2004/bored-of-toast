"""Related recipes block.

Self-contained module. Picks related recipes by category overlap, with a
deterministic fallback so every recipe gets a full block even when overlap
is thin.

Pages per session is the cheapest revenue lever available: moving from 1.2
to 1.8 pages per session is roughly 50% more ad revenue with no new traffic.
No recipe on the site currently links to another recipe.

Integration in build.py requires two lines:

    from related_recipes import block as related_block

    # inside the recipe page template, after the sources block:
    related_block(r, recipes)

Also add polish.css and related.css to the stylesheet list copied to dist/.
"""
from html import escape as esc


def pick(current, all_recipes, limit=3):
    """Return up to `limit` related recipes, best match first.

    Scoring:
      +3 per shared category
      +2 same method (no-cook, one-pan, sheet-pan)
      +1 similar total time

    Falls back to filling remaining slots in site order, so the block is
    never partially empty.
    """
    slug = current.get('slug')
    cats = set(current.get('categories', []))
    method = (current.get('method') or '').lower()
    time_bucket = _time_bucket(current)

    scored = []
    for r in all_recipes:
        if r.get('slug') == slug:
            continue
        score = 3 * len(cats & set(r.get('categories', [])))
        if method and (r.get('method') or '').lower() == method:
            score += 2
        if time_bucket and _time_bucket(r) == time_bucket:
            score += 1
        scored.append((score, r))

    # Sort by score, then by site order for stable output between builds
    order = {r.get('slug'): i for i, r in enumerate(all_recipes)}
    scored.sort(key=lambda x: (-x[0], order.get(x[1].get('slug'), 99)))

    picked = [r for score, r in scored if score > 0][:limit]

    # Fill remaining slots so the block always has `limit` cards
    if len(picked) < limit:
        taken = {r.get('slug') for r in picked} | {slug}
        for r in all_recipes:
            if r.get('slug') not in taken:
                picked.append(r)
                taken.add(r.get('slug'))
            if len(picked) == limit:
                break

    return picked[:limit]


def _time_bucket(r):
    """Coarse time grouping. Returns 'quick', 'medium', 'long' or None."""
    raw = (r.get('total_time') or r.get('card_time') or '')
    digits = ''.join(c for c in str(raw) if c.isdigit())
    if not digits:
        return None
    mins = int(digits[:3])
    if mins <= 15:
        return 'quick'
    if mins <= 30:
        return 'medium'
    return 'long'


def _reason(current, other):
    """Short editorial reason why this recipe is being suggested."""
    shared = set(current.get('categories', [])) & set(other.get('categories', []))
    method = (other.get('method') or '')

    if 'no-cook' in method.lower():
        return 'Also no-cook'
    if 'one-pan' in method.lower():
        return 'Also one pan'
    if 'make-ahead' in shared:
        return 'Also make-ahead'
    if 'quick-easy' in shared:
        return 'Also under 25 minutes'
    if 'budget-friendly' in shared:
        return 'Also pantry-friendly'
    if 'protein-forward' in shared:
        return 'Also protein-forward'
    if 'plant-forward' in shared:
        return 'Also plant-forward'
    return 'From the notebook'


def block(current, all_recipes, limit=3):
    """Render the related recipes section. Returns '' if nothing to show."""
    picks = pick(current, all_recipes, limit)
    if not picks:
        return ''

    cards = ''
    for r in picks:
        img = r.get('img', '')
        stem = img.rsplit('.', 1)[0] if img else ''
        src = f'/assets/{stem}-800.webp' if stem else ''
        img_html = (
            f'<img src="{esc(src, quote=True)}" alt="{esc(r.get("alt", ""), quote=True)}" '
            f'width="800" height="600" loading="lazy" decoding="async">'
        ) if src else ''

        meta = ' · '.join(x for x in [
            f'Serves {r.get("serves")}' if r.get('serves') else '',
            r.get('card_time') or r.get('total_time') or '',
            r.get('method') or '',
        ] if x)

        cards += (
            f'<a class="rr-card" href="/recipes/{esc(r.get("slug", ""), quote=True)}/">'
            f'<span class="rr-thumb">{img_html}</span>'
            f'<span class="rr-body">'
            f'<span class="rr-reason">{esc(_reason(current, r))}</span>'
            f'<span class="rr-title">{esc(r.get("title", ""))}</span>'
            f'<span class="rr-meta">{esc(meta)}</span>'
            f'</span></a>'
        )

    return (
        f'<section class="rr-block" aria-labelledby="rr-heading">'
        f'<p class="eyebrow">KEEP GOING</p>'
        f'<h2 id="rr-heading">What to cook next.</h2>'
        f'<div class="rr-grid">{cards}</div>'
        f'</section>'
    )
