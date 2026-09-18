"""Presentation polish pass over dist/.

Runs after postbuild.py and postbuild_reference.py. Every fix here came out
of a full-site audit and is purely presentational: colour tokens, a stray
panel, numbering, and two stale cross-references.

Why this is a separate file: postbuild.py is around 1200 lines and cannot be
rewritten safely from a remote editing session without risking silent loss.
These transforms belong there and should be folded in the next time that file
is edited properly in a local checkout.

Every pattern here is written against HTML that was read back off the live
site, not against assumed markup. Three of these transforms previously
matched nothing while still reporting success, so each one now says whether
it found its target and main() exits non-zero when a scoped transform finds
nothing on the page it was written for.

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
# matches the site instead of contradicting it.
WRONG_THEME_COLOUR = '#124de3'
BRAND_INK = '#2B3A30'

# Marker attributes keep every transform safe to run twice.
EMPTY_STATE_MARKER = 'data-empty-hidden'
REFERENCE_ANCHOR_ID = 'reference-charts'
SERIES_MARKER = 'data-reference-series'

# Text that identifies the empty-results panel on the recipe index.
EMPTY_STATE_PHRASES = (
    'No recipes in this category yet',
    'This section will grow as the recipe collection expands',
)

# The chickpea cross-reference predates the pillar page. It promised three
# ways and linked to the unfiltered recipe index.
CHICKPEA_TARGET = '/kitchen-notes/chickpeas-five-ways/'

CHICKPEA_TEXT_FIXES = (
    ('three ways to use chickpeas', 'five ways to use chickpeas'),
    ('three ways with chickpeas', 'five ways with chickpeas'),
    ('explores three ways', 'explores five ways'),
    ('One can, three directions', 'One can, five directions'),
)


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

    The panel exists for a filter that matches nothing, but it is emitted
    unconditionally, so it sat under all ten recipes telling the reader the
    category was empty.

    The first attempt used the hidden attribute. That was the wrong tool: any
    class-based display rule in the stylesheet beats it, and this panel is a
    styled section. An inline display:none sits high enough in the cascade to
    win, and the filter script can still reveal the panel by writing its own
    inline display later.
    """
    if EMPTY_STATE_MARKER in html:
        return html, False
    if not any(phrase in html for phrase in EMPTY_STATE_PHRASES):
        return html, False

    phrase = next(p for p in EMPTY_STATE_PHRASES if p in html)
    position = html.find(phrase)

    # Walk back to the nearest containing section or div, preferring a
    # container over the paragraph holding the copy so the icon and heading
    # disappear with it.
    opens = list(re.finditer(r'<(section|div)\b[^>]*>', html[:position], re.I))
    if not opens:
        return html, False

    target = opens[-1]
    tag = target.group(0)

    if 'display:none' in tag.replace(' ', ''):
        return html, False

    if 'style="' in tag:
        patched = tag.replace('style="', 'style="display:none;', 1)
        patched = patched[:-1] + f' {EMPTY_STATE_MARKER}>'
    else:
        patched = tag[:-1] + f' style="display:none" {EMPTY_STATE_MARKER}>'

    return html[:target.start()] + patched + html[target.end():], True


# ---------------------------------------------------------------------------
# Kitchen note numbering
# ---------------------------------------------------------------------------

def fix_padded_numbering(html):
    """Stop zero-padding double-digit index numbers.

    The listing pads every index to two characters, so the tenth note onward
    rendered as 010, 011, 012. Only single digits should be padded.

    The pattern requires a three-digit run starting with a zero, immediately
    followed by the separator used in the eyebrow, so an ordinary label such
    as the section number 01 is left alone.
    """
    pattern = re.compile(r'(>|\s)0(1\d|2\d)(\s*(?:/|<))')
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

def fix_chickpea_reference(html):
    """Point the chickpea mention at the pillar page and correct the count.

    Written before Chickpeas, Five Ways existed, so it advertised three ways
    and sent the reader to the unfiltered recipe index.

    The first version keyed off the anchor text and required the word
    "chickpea" in it. The real link reads "One can, three directions", so it
    was skipped every time. The fix is to work from the section instead: find
    the block that talks about chickpeas, then retarget the one anchor inside
    it that still points at a listing route.

    Requiring a listing href is what keeps this off the recipe cards. An
    anchor already pointing at a specific recipe is left alone, which is why
    the roasted chickpeas card is safe.
    """
    changed = False

    for old, new in CHICKPEA_TEXT_FIXES:
        if old in html:
            html = html.replace(old, new)
            changed = True

    # Find each section, then act only on those mentioning chickpeas.
    sections = list(re.finditer(r'<section\b[^>]*>.*?</section>', html, re.I | re.S))
    if not sections:
        return html, changed

    listing_routes = ('/recipes/', '/kitchen-notes/')

    for section in reversed(sections):
        block = section.group(0)
        if 'chickpea' not in _strip_tags(block).lower():
            continue
        if CHICKPEA_TARGET in block:
            continue

        def retarget(match):
            opening, href, rest, body = match.groups()
            if href.rstrip('/') + '/' not in listing_routes:
                return match.group(0)
            return f'{opening}{CHICKPEA_TARGET}{rest}{body}</a>'

        pattern = re.compile(r'(<a[^>]*href=")([^"]*)("[^>]*>)(.*?)</a>', re.I | re.S)
        new_block = pattern.sub(retarget, block)

        if new_block != block:
            html = html[:section.start()] + new_block + html[section.end():]
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

    The first version looked for href="...?series=..." because that is how a
    filtered view would be built. The grid actually links to in-page anchors
    such as #texture-school, so nothing matched. The pattern now follows the
    real markup, and the new card points at the charts anchor for the same
    reason: it works without depending on the filter script.
    """
    if SERIES_MARKER in html:
        return html, False

    # Theme cards are anchors whose href is a bare in-page fragment.
    cards = list(re.finditer(
        r'<a\b[^>]*href="#[a-z0-9-]+"[^>]*>.*?</a>',
        html,
        re.I | re.S,
    ))

    # Ignore a skip link or any other fragment anchor that is not part of the
    # grid. The theme cards are the run of them that sit next to each other.
    cards = [c for c in cards if len(_strip_tags(c.group(0))) > 20]

    if not cards:
        return html, False

    last = cards[-1]
    clone = _clone_card(
        last.group(0),
        f'#{REFERENCE_ANCHOR_ID}',
        [
            'Reference',
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
SCOPED = {
    'empty state hidden': ('recipes',),
    'hero number': ('',),
    'chickpea reference': ('kitchen-notes',),
    'reference anchor': ('kitchen-notes',),
    'reference series card': ('kitchen-notes',),
}

# A scoped transform that never fires is a broken pattern, not a no-op. These
# are the ones worth failing the build over, because each one was written for
# a specific page that is known to contain its target.
MUST_MATCH = (
    'theme colour',
    'empty state hidden',
    'reference anchor',
    'reference series card',
)


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
        print(f'    {key}: {value if value else "no match"}')

    missed = [name for name in MUST_MATCH if counts.get(name, 0) == 0]
    if missed:
        print()
        print('postbuild_polish: FAILED')
        print('  These transforms matched nothing. Each was written against')
        print('  markup read off the live site, so a miss means the pattern')
        print('  is wrong or the generated markup changed:')
        for name in missed:
            print(f'    - {name}')
        return 1

    print('postbuild_polish: done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
