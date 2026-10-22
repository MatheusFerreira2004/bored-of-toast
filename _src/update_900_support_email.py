"""Use one support e-mail everywhere on the site: boredoftoast@gmail.com.

The site source still mentions hello@boredoftoast.com (a domain that is not registered yet,
so that inbox does not receive mail). This script replaces it in every source file under _src/
that the build reads (Python, JSON, HTML, Markdown, text, JS and CSS templates).

Test files are skipped on purpose: journey_checks.py asserts that the new address is present
AND that the old one is absent, so rewriting it would turn that check into a contradiction.

Safe to run many times: it only rewrites files that still contain the old address, and it
never fails the build. It prints what it changed so the auto-build summary shows it.
The number 900 keeps it after every earlier update script.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OLD = 'hello@boredoftoast.com'
NEW = 'boredoftoast@gmail.com'
EXTS = {'.py', '.json', '.html', '.md', '.txt', '.js', '.css'}
SKIP_DIRS = {'site', '__pycache__', 'reports', 'notes'}
SKIP_FILES = {pathlib.Path(__file__).name, 'journey_checks.py', 'checks.py'}

changed = []
for path in sorted(ROOT.rglob('*')):
    if not path.is_file() or path.suffix not in EXTS:
        continue
    if path.name in SKIP_FILES:
        continue
    if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError):
        continue
    if OLD in text:
        count = text.count(OLD)
        path.write_text(text.replace(OLD, NEW), encoding='utf-8')
        changed.append(f'{path.relative_to(ROOT)} ({count})')

if changed:
    print('Support e-mail replaced with ' + NEW + ' in:')
    for item in changed:
        print('- ' + item)
else:
    print('Already applied. No source file mentions ' + OLD + '.')
