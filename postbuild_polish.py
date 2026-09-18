"""Presentation polish pass over dist/.

Runs after postbuild.py and postbuild_reference.py. Every fix here came out
of a full-site audit and is purely presentational: colour tokens, stray
panels, numbering, and two stale cross-references.

Why this is a separate file: postbuild.py is around 1200 lines and cannot be
rewritten safely from a remote editing session without risking silent loss.
These transforms belong there and should be folded in the next time that file
is edited properly in a local checkout.

Each transform is independent, idempotent, and wrapped so a miss can never
break a deploy. A transform that finds nothing logs and moves on, because the
underlying markup may legitimately change in build.py.

Run locally with:
    python build.py && python postbuild.py && python postbuild_reference.py \
        && python postbuild_polish.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'

# The generated pages carry a leftover template colour. #2B3A30 is the ink
# already used for headings and the header background, so the browser chrome
# now matches the site instead of contradicting it.
WRONG_THEME_COLOUR = '#124de3'
BRAND_INK = '#2B3A30'

# Marker attributes keep every transform safe to run twice.
EMPTY_STATE_MARKER = 'data-empty-hidden'
REFERENCE_ANCHOR_ID = 'reference-charts'
SERIES_MARKER = 'data-reference-series'

# Text that identifies the empty-results panel on the recipe index.
EMPTY_STATE_PHRASES = [
    'No recipes in this category yet',
    'This section will grow as the recipe collection expands',
]

# The chickpea cross-reference predates the pillar page. It promised three
# ways and linked to the unfiltered recipe index.
CHICKPEA_TARGET = '/kitchen-notes/chickpeas-five-ways/'

# Only a link that currently points at a listing is a candidate for
# retargeting. An anchor already pointing at a specific recipe or note is
# doing its job and must be left alone: an earlier version of this transform
# matched on link text alone and rewrote the roasted chickpeas recipe card,
# which made that recipe unreachable from its own index.
LISTING_HREFS = (
    '/recipes/',
    '/kitchen-notes/',
)

CHICKPEA_TEXT_FIXES = [
    ('three ways to use chickpeas', 'five ways to use chickpeas'),
    ('three ways with chickpeas', 'five ways with chickpeas'),
    ('explores three ways', 'explores five ways'),
]


def _strip_tags(fragment):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', fragment)).strip()


# ---------------------------------------------------------------------------
# Colour token
# ---------------------------------------------------------------------------

def fix_theme_colour(html):
    """Replace the leftover template blue in the theme-color meta tag."""
    if WRONG_THEME_COLOUR not in html:
        return html, False
    return html.replace(WRONG_THEME_COLOUR, BRAND_INK), True


# ---------------------------------------------------------------------------
# Empty state on the recipe index
# ---------------------------------------------------------------------------

def hide_empty_state(html):
    """Hide the empty-results panel that renders below the full grid.

    The panel is meant for a filter that matches nothing, but it is emitted
    unconditionally, so it sat under all ten recipes telling the reader the
    category was empty.

    Hiding with the hidden attribute rather than deleting the node keeps the
    filter behaviour intact: script that sets an inline display still wins
    over the user-agent rule that hidden relies on.
    """
    if EMPTY_STATE_MARKER in html:
        return html, False
    if not any(phrase in html for phrase in EMPTY_STATE_PHRASES):
        return html, False

    phrase = next(p for p in EMPTY_STATE_PHRASES if p in html)
    position = html.find(phrase)

    # Walk back to the opening tag of the block that contains the phrase.
    opens = list(re.finditer(r'<(section|div|p)\b[^>]*>', html[:position], re.I))
    if not opens:
        return html, False

    # Prefer the nearest ancestor that looks like a panel rather than a
    # paragraph, so the whole block is hidden and not just its copy.
    target = None
    for match in reversed(opens):
        if match.group(1).lower() in ('section', 'div'):
            target = match
            break
    if target is None:
        target = opens[-1]

    tag = target.group(0)
    if ' hidden' in tag:
        return html, False

    patched = tag[:-1] + f' hidden {EMPTY_STATE_MARKER}>'
    return html[:target.start()] + patched + html[target.end():], True


# ---------------------------------------------------------------------------
# Kitchen note numbering
# ---------------------------------------------------------------------------

def fix_padded_numbering(html):
    """Stop zero-padding double-digit index numbers.

    The listing pads every index to two characters, so the tenth note onward
    rendered as 010, 011, 012. Only single digits should be padded.

    The pattern is deliberately tight: a zero, then 10 to 29, then the space
    and slash the eyebrow uses. Anything looser starts matching ordinary
    numbers in body copy.
    """
    pattern = re.compile(r'(>|\s)0([12]\d)(\s*/)')
    new_html, count = pattern.subn(
        lambda m: m.group(1) + m.group(2) + m.group(3), html
    )
    return new_html, count > 0


# ---------------------------------------------------------------------------
# Home hero numbering
# ---------------------------------------------------------------------------

def fix_hero_number(html):
    """Remove the 01 from the hero eyebrow.

    The hero read "01 THE EVERYDAY KITCHEN" and the section directly beneath
    it read "01 / THE RECIPE NOTEBOOK". Two different things numbered 01 on
    one screen. The hero is not part of the numbered sequence, so the number
    comes off there.
    """
    pattern = re.compile(
        r'(<p[^>]*class="[^"]*eyebrow[^"]*"[^>]*>)\s*01\s+(?=[A-Z])',
        re.I,
    )
    new_html, count = pattern.subn(lambda m: m.group(1), html, count=1)
    return new_html, count > 0


# ---------------------------------------------------------------------------
# Chickpea cross-reference
# ---------------------------------------------------------------------------

def _is_listing_href(href):
    """True when an href points at a listing rather than a single page."""
    cleaned = href.split('?')[0].split('#')[0]
    return cleaned in LISTING_HREFS


def _retarget_chickpea_anchor(match):
    """Send a listing link about ways to use chickpeas to the pillar page."""
    opening, href, rest, body = match.groups()

    if CHICKPEA_TARGET in href:
        return match.group(0)
    if not _is_listing_href(href):
        return match.group(0)

    text = _strip_tags(body).lower()
    if 'chickpea' not in text:
        return match.group(0)
    if not re.search(r'\b(ways|five|three)\b', text):
        return match.group(0)

    return f'{opening}{CHICKPEA_TARGET}{rest}{body}</a>'


def fix_chickpea_reference(html):
    """Point the chickpea mention at the pillar page and correct the count.

    Written before Chickpeas, Five Ways existed, so it advertised three ways
    and sent the reader to the unfiltered recipe index to find them.
    """
    changed = False

    for old, new in CHICKPEA_TEXT_FIXES:
        if old in html:
            html = html.replace(old, new)
            changed = True

    pattern = re.compile(r'(<a[^>]*href=")([^"]*)("[^>]*>)(.*?)</a>', re.I | re.S)
    new_html = pattern.sub(_retarget_chickpea_anchor, html)
    if new_html != html:
        html = new_html
        changed = True

    return html, changed


# ---------------------------------------------------------------------------
# Reference charts: anchor target and theme card
# ---------------------------------------------------------------------------

def add_reference_anchor(html):
    """Give the first reference card an id so a theme link can jump to it."""
    if f'id="{REFERENCE_ANCHOR_ID}"' in html:
        return html, False
    if 'REFERENCE / CHARTS' not in html:
        return html, False

    position = html.find('REFERENCE / CHARTS')
    opens = list(re.finditer(r'<a\b[^>]*>', html[:position], re.I))
    if not opens:
        return html, False

    target = opens[-1]
    tag = target.group(0)
    if ' id=' in tag:
        return html, False

    patched = tag[:-1] + f' id="{REFERENCE_ANCHOR_ID}">'
    return html[:target.start()] + patched + html[target.end():], True


def _clone_card(card_html, href, texts):
    """Rebuild a sibling card with a new href and new text nodes.

    Cloning real markup rather than writing fresh HTML means the new card
    inherits whatever classes and structure the generator currently emits, so
    it cannot drift out of step with its siblings.
    """
    clone = re.sub(
        r'(href=")[^"]*(")',
        lambda m: m.group(1) + href + m.group(2),
        card_html,
        count=1,
    )
    clone = re.sub(r'\sid="[^"]*"', '', clone)

    queue = list(texts)

    def swap(match):
        body = match.group(1)
        if not queue:
            return match.group(0)
        if len(body.strip()) < 2 or not re.search(r'[A-Za-z]{2,}', body):
            return match.group(0)
        return '>' + queue.pop(0) + '<'

    clone = re.sub(r'>([^<>]+)<', swap, clone)

    # Mark it so the injection is idempotent.
    return clone.replace('<a ', f'<a {SERIES_MARKER} ', 1)


def add_reference_series(html):
    """Add a Reference card to the theme grid, cloned from its siblings.

    Eight charts now sit in the listing with no theme covering them, so a
    reader browsing by theme cannot reach them.

    The card links to an in-page anchor rather than a filtered view, so it
    works without depending on the filter script's data attributes.
    """
    if SERIES_MARKER in html:
        return html, False

    cards = list(re.finditer(
        r'<a\b[^>]*href="[^"]*\?series=[^"]*"[^>]*>.*?</a>',
        html,
        re.I | re.S,
    ))
    if not cards:
        return html, False

    last = cards[-1]
    clone = _clone_card(
        last.group(0),
        f'#{REFERENCE_ANCHOR_ID}',
        [
            'Reference',
            'Charts and conversions',
            'Cooking times, yields, substitutions and storage, '
            'gathered in one place.',
        ],
    )

    return html[:last.end()] + clone + html[last.end():], True


TRANSFORMS = [
    ('theme colour', fix_theme_colour),
    ('empty state hidden', hide_empty_state),
    ('index numbering', fix_padded_numbering),
    ('hero number', fix_hero_number),
    ('chickpea reference', fix_chickpea_reference),
    ('reference anchor', add_reference_anchor),
    ('reference series card', add_reference_series),
]

# Transforms that only make sense on one route, keyed by the first path part.
# The chickpea retarget is scoped to the home page: the stale copy lives
# there, and running it site-wide is what let it rewrite a recipe card.
SCOPED = {
    'empty state hidden': ('recipes',),
    'hero number': ('',),
    'chickpea reference': ('',),
    'reference anchor': ('kitchen-notes',),
    'reference series card': ('kitchen-notes',),
}


def _in_scope(name, parts):
    allowed = SCOPED.get(name)
    if allowed is None:
        return True
    root = parts[0] if len(parts) > 1 else ''
    return root in allowed


def main():
    if not DIST.exists():
        print('postbuild_polish: dist/ not found, nothing to do')
        return 0

    print('postbuild_polish: starting')

    pages = sorted(DIST.rglob('*.html'))
    if not pages:
        print('  no HTML files found')
        return 0

    counts = {name: 0 for name, _ in TRANSFORMS}
    touched = 0

    for page in pages:
        try:
            html = page.read_text(encoding='utf-8')
        except Exception as exc:
            print(f'  warn: could not read {page.name}: {exc}')
            continue

        original = html
        parts = page.relative_to(DIST).parts

        for name, fn in TRANSFORMS:
            if not _in_scope(name, parts):
                continue
            try:
                html, changed = fn(html)
                if changed:
                    counts[name] += 1
            except Exception as exc:
                print(f'  warn: {name} failed on {page.name}: {exc}')

        if html != original:
            try:
                page.write_text(html, encoding='utf-8')
                touched += 1
            except Exception as exc:
                print(f'  warn: could not write {page.name}: {exc}')

    print(f'  pages scanned: {len(pages)}')
    print(f'  pages modified: {touched}')
    for key, value in counts.items():
        if value:
            print(f'    {key}: {value}')
        else:
            print(f'    {key}: no match')
    print('postbuild_polish: done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
