"""Presentation polish pass over dist/.

Runs after postbuild.py and postbuild_reference.py. Every fix here came out
of a full-site audit and is purely presentational: colour tokens, a stray
panel, numbering, and two stale cross-references.

Why this is a separate file: postbuild.py is around 1200 lines and cannot be
rewritten safely from a remote editing session without risking silent loss.
These transforms belong there and should be folded in the next time that file
is edited properly in a local checkout.

Two lessons are baked into this version.

First, a transform that reports success is not the same as a transform that
produced the intended result. The empty-state panel was being hidden with an
inline display rule, which is invisible to any text-based check of the page,
so there was no way to confirm from outside whether it had worked. That panel
is now removed from the markup outright, which is verifiable.

Second, failing the build when a pattern misses was the wrong trade. One
stale selector then blocks every later deploy, including unrelated content.
Misses are now reported loudly and the build continues. Only a genuine
exception is treated as fatal.

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

# Exact strings from the last theme card, read off the live listing. Cloning
# that card and swapping these two strings is deterministic, unlike walking
# text nodes and hoping the right ones come up first.
SERIES_SOURCE_TITLE = 'Day One'
SERIES_SOURCE_BODY = 'For absolute beginners: the bare minimum to get started.'
SERIES_NEW_TITLE = 'Reference'
SERIES_NEW_BODY = (
    'Cooking times, yields, substitutions and storage, gathered in one place.'
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

def remove_empty_state(html):
    """Delete the empty-results panel that renders below the full grid.

    The panel is meant for a filter that matches nothing, but the generator
    emits it unconditionally, so it sat under all ten recipes telling the
    reader the category was empty.

    Two earlier attempts hid it instead: first with the hidden attribute,
    which any class-based display rule in the stylesheet overrides, then with
    an inline display rule, which works in a browser but cannot be confirmed
    from outside the page. Removing the element is both stronger and
    checkable.

    The trade-off: if the client-side filter later matches nothing, the grid
    is simply empty rather than showing an explanation. That is a smaller
    problem than a permanent panel contradicting a full page of recipes, and
    the honest fix belongs in the generator, which should only emit this
    panel when the grid is empty.
    """
    if not any(phrase in html for phrase in EMPTY_STATE_PHRASES):
        return html, False

    phrase = next(p for p in EMPTY_STATE_PHRASES if p in html)
    position = html.find(phrase)

    # Find the innermost section or div that opens before the phrase and
    # closes after it, then drop that whole element.
    best = None
    for match in re.finditer(r'<(section|div)\b[^>]*>', html[:position], re.I):
        tag_name = match.group(1)
        depth = 0
        cursor = match.start()
        pattern = re.compile(rf'<{tag_name}\b[^>]*>|</{tag_name}\s*>', re.I)
        for token in pattern.finditer(html, cursor):
            if token.group(0).startswith('</'):
                depth -= 1
                if depth == 0:
                    end = token.end()
                    if end > position:
                        # Prefer the tightest container around the phrase.
                        if best is None or match.start() > best[0]:
                            best = (match.start(), end)
                    break
            else:
                depth += 1

    if best is None:
        return html, False

    start, end = best
    return html[:start] + html[end:], True


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

    Requiring a listing href is what keeps this off the recipe cards. An
    anchor already pointing at a specific recipe is left alone, which is why
    the roasted chickpeas card is safe.
    """
    changed = False

    for old, new in CHICKPEA_TEXT_FIXES:
        if old in html:
            html = html.replace(old, new)
            changed = True

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


def add_reference_series(html):
    """Add a Reference card to the theme grid.

    Eight charts now sit in the listing with no theme covering them, so a
    reader browsing by theme cannot reach them.

    The previous version cloned the last card and then walked its text nodes,
    replacing the first two that looked like prose. That is guesswork: the
    order of text nodes depends on markup that can change, and a miss is
    silent. This version keys off the two exact strings in the Day One card,
    so either both are found and the swap is correct, or nothing happens and
    the miss is reported.
    """
    if SERIES_MARKER in html:
        return html, False

    if SERIES_SOURCE_TITLE not in html or SERIES_SOURCE_BODY not in html:
        return html, False

    # Locate the anchor that contains both strings.
    cards = list(re.finditer(
        r'<a\b[^>]*href="#[a-z0-9-]+"[^>]*>.*?</a>',
        html,
        re.I | re.S,
    ))

    source = None
    for card in cards:
        block = card.group(0)
        if SERIES_SOURCE_TITLE in block and SERIES_SOURCE_BODY in block:
            source = card
            break

    if source is None:
        return html, False

    clone = source.group(0)
    clone = re.sub(
        r'(href=")#[a-z0-9-]+(")',
        lambda m: m.group(1) + '#' + REFERENCE_ANCHOR_ID + m.group(2),
        clone,
        count=1,
        flags=re.I,
    )
    clone = re.sub(r'\sid="[^"]*"', '', clone)
    clone = clone.replace(SERIES_SOURCE_BODY, SERIES_NEW_BODY)
    clone = clone.replace(SERIES_SOURCE_TITLE, SERIES_NEW_TITLE)
    clone = clone.replace('<a ', f'<a {SERIES_MARKER} ', 1)

    return html[:source.end()] + clone + html[source.end():], True


TRANSFORMS = [
    ('theme colour', fix_theme_colour),
    ('empty state removed', remove_empty_state),
    ('index numbering', fix_padded_numbering),
    ('hero number', fix_hero_number),
    ('chickpea reference', fix_chickpea_reference),
    ('reference anchor', add_reference_anchor),
    ('reference series card', add_reference_series),
]

# Transforms that only make sense on one route, keyed by the first path part.
SCOPED = {
    'empty state removed': ('recipes',),
    'hero number': ('',),
    'chickpea reference': ('kitchen-notes',),
    'reference anchor': ('kitchen-notes',),
    'reference series card': ('kitchen-notes',),
}

# Transforms expected to match somewhere. A miss is a broken selector worth
# shouting about, but it no longer fails the build: one stale pattern should
# not block unrelated content from deploying.
EXPECTED = (
    'theme colour',
    'empty state removed',
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
    errors = []
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
                errors.append((name, page.name, exc))

        if html != original:
            try:
                page.write_text(html, encoding='utf-8')
                touched += 1
            except Exception as exc:
                print(f'  warn: could not write {page.name}: {exc}')

    print(f'  pages scanned: {len(pages)}')
    print(f'  pages modified: {touched}')
    for key, value in counts.items():
        print(f'    {key}: {value if value else "NO MATCH"}')

    missed = [name for name in EXPECTED if counts.get(name, 0) == 0]
    if missed:
        print()
        print('  WARNING: these transforms matched nothing. Each was written')
        print('  against markup read off the live site, so a miss means the')
        print('  pattern is wrong or the generated markup changed:')
        for name in missed:
            print(f'    - {name}')

    if errors:
        print()
        print('postbuild_polish: FAILED')
        for name, page_name, exc in errors:
            print(f'  {name} raised on {page_name}: {type(exc).__name__}: {exc}')
        return 1

    print('postbuild_polish: done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
