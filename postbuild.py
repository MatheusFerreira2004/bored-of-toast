"""Post-build pass over dist/.

Runs after build.py. Applies additive changes to the generated HTML without
touching build.py itself:

  1. Copies additive stylesheets into dist/
  2. Injects their <link> tags last, so the cascade order is correct
  3. Hides the visible byline (kept in JSON-LD for SEO)
  4. Removes the /start-here/ footer link, which 404s
  5. Fixes the lowercase sentence start in the dressing step cue
  6. Drops the leftover "development editions" line from kitchen notes

Every step is wrapped so a failure here can never break a deploy. If a file
or pattern is missing, the script logs and moves on.

Run locally with:
    python build.py && python postbuild.py
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'

# Stylesheets that are additive and must load after the existing ones.
# Order matters: later files win in the cascade.
ADDITIVE_CSS = ['related.css', 'polish.css']

# Author name to strip from the visible page. The name stays in the
# JSON-LD author field, which is what Google reads for E-E-A-T.
AUTHOR_NAME = 'Matheus Ferreira'


def copy_stylesheets():
    """Copy additive stylesheets into dist/."""
    copied = []
    for name in ADDITIVE_CSS:
        src = ROOT / name
        if not src.exists():
            print(f'  skip: {name} not found at repo root')
            continue
        shutil.copy2(src, DIST / name)
        copied.append(name)
    return copied


def inject_stylesheets(html, available):
    """Add <link> tags for the additive stylesheets just before </head>."""
    if '</head>' not in html:
        return html, False

    tags = ''
    for name in available:
        href = f'/{name}'
        if href in html:
            continue  # already linked
        tags += f'<link rel="stylesheet" href="{href}">'

    if not tags:
        return html, False

    return html.replace('</head>', tags + '</head>', 1), True


def add_scroll_progress(html):
    """Wire up the reading progress bar defined in polish.css.

    polish.css draws the bar from a --scroll custom property. Without this
    listener the bar renders at 0% and is invisible, so the script is what
    makes it actually work.
    """
    if '</body>' not in html or 'data-scroll-progress' in html:
        return html, False

    script = (
        '<script data-scroll-progress>'
        '(function(){'
        'var d=document.documentElement,t=0;'
        'function u(){'
        'var h=d.scrollHeight-d.clientHeight;'
        'd.style.setProperty("--scroll",(h>0?(d.scrollTop/h)*100:0)+"%");'
        '}'
        'addEventListener("scroll",function(){'
        'if(t)return;'
        't=requestAnimationFrame(function(){t=0;u();});'
        '},{passive:true});'
        'addEventListener("resize",u,{passive:true});u();'
        '})();'
        '</script>'
    )
    return html.replace('</body>', script + '</body>', 1), True


def remove_visible_byline(html):
    """Remove the visible author byline from the page body.

    The author remains in the Recipe JSON-LD, so structured data and SEO
    signals are unaffected. Only the on-page credit line is removed.

    Matches paragraphs such as:
        <p class="small">By Matheus Ferreira · Published 2026-09-16</p>
    """
    changed = False

    # Any element whose text starts with "By <author>"
    pattern = re.compile(
        r'<(p|span|div)\b[^>]*>\s*By\s+' + re.escape(AUTHOR_NAME) + r'[^<]*</\1>',
        re.I,
    )
    html, count = pattern.subn('', html)
    if count:
        changed = True

    # Fallback: a bare "By <author>" text node left outside a wrapper
    bare = re.compile(r'\bBy\s+' + re.escape(AUTHOR_NAME) + r'\b\s*(·[^<]*)?')
    html, count = bare.subn('', html)
    if count:
        changed = True

    return html, changed


def remove_start_here(html):
    """Remove the footer link to /start-here/, which no longer exists."""
    pattern = re.compile(r'<a[^>]*href="/start-here/"[^>]*>.*?</a>', re.I | re.S)
    new_html, count = pattern.subn('', html)
    return new_html, count > 0


def fix_cue_typo(html):
    """Capitalise the second sentence in the dressing step cue."""
    needle = 'combined. whisk again'
    if needle not in html:
        return html, False
    return html.replace(needle, 'combined. Whisk again'), True


def fix_development_note(html):
    """Replace the leftover development-edition line in kitchen notes.

    CONTEXTO.md no longer treats recipes as development editions, but this
    sentence is hardcoded in kitchen_notes.py and appears on all guides.
    """
    old = ('Linked recipes are development editions and await kitchen testing. '
           'These guides do not change that status.')
    new = 'These guides work with any recipe on the site.'
    if old in html:
        return html.replace(old, new), True

    # Fallback for minor punctuation differences
    pattern = re.compile(
        r'Linked recipes are development editions[^<]*',
        re.I,
    )
    new_html, count = pattern.subn(new, html)
    return new_html, count > 0


TRANSFORMS = [
    ('scroll progress', add_scroll_progress),
    ('visible byline', remove_visible_byline),
    ('start-here link', remove_start_here),
    ('cue typo', fix_cue_typo),
    ('development note', fix_development_note),
]


def main():
    if not DIST.exists():
        print('postbuild: dist/ not found, nothing to do')
        return 0

    print('postbuild: starting')

    available = copy_stylesheets()
    if available:
        print(f'  copied: {", ".join(available)}')

    pages = sorted(DIST.rglob('*.html'))
    if not pages:
        print('  no HTML files found')
        return 0

    counts = {name: 0 for name, _ in TRANSFORMS}
    counts['stylesheets'] = 0
    touched = 0

    for page in pages:
        try:
            html = page.read_text(encoding='utf-8')
        except Exception as exc:
            print(f'  warn: could not read {page.name}: {exc}')
            continue

        original = html

        if available:
            html, changed = inject_stylesheets(html, available)
            if changed:
                counts['stylesheets'] += 1

        for name, fn in TRANSFORMS:
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
    print('postbuild: done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
