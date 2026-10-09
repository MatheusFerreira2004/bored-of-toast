#!/usr/bin/env python3
"""Round 2 content fixes for the small-plates update.

1. "High Protein" tag only on the 10 focus recipes (removes it from pasta, French toast, tacos...).
2. About page: new values (Protein first / Small and often / Gentle on hard days / Real food)
   and a note in the contact text.

Nothing is saved unless every change is found. Safe to re-run.
Run from the project root: python3 _src/fix_round2.py
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)

# ------------------------------------------------------------------ 1. High Protein tag
build_src = open(P('build.py'), encoding='utf-8').read()
m = re.search(r'FOCUS_IDS = (\[.*?\])', build_src)
if not m:
    sys.exit('ERROR: FOCUS_IDS not found in build.py. Run content_update.py first. Nothing was saved.')
FOCUS = json.loads(m.group(1))

recipes_raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(recipes_raw)
removed = []
for r in recipes:
    if r['id'] not in FOCUS and 'high-protein' in r.get('tags', []):
        r['tags'].remove('high-protein')
        removed.append(r['id'])
kept = [r['id'] for r in recipes if 'high-protein' in r.get('tags', [])]

# ------------------------------------------------------------------ 2. About page
APOS = "(?:'|\\\\'|\u2019|&#x27;|&#39;)"

def rx(s):
    """Regex for s that accepts any apostrophe encoding."""
    return ''.join(APOS if ch == "'" else re.escape(ch) for ch in s)

VALUES = [
    ('Real food', 'Fresh ingredients and real flavor, nothing overly processed.',
     'Protein first', 'Start with the protein, before fullness kicks in.'),
    ('Simple cooking', 'Clear steps and honest timing, so you are never left guessing.',
     'Small and often', 'A small plate you finish beats a big one you don\u2019t.'),
    ('Quality ingredients', 'Better ingredients make better meals, and they are easy to find.',
     'Gentle on hard days', 'Cold, mild and soft options for when nothing sounds good.'),
    ('Everyday joy', 'Food brings people together. That is the best part.',
     'Real food', 'Everyday ingredients from a regular grocery store.'),
]
CONTACT_OLD = "Use the form to prepare a draft, then send it from your email app."
CONTACT_NEW = ("Use the form to prepare a draft, then send it from your email app. "
               "We can\u2019t give personal medical or nutrition advice, but we\u2019re always happy to help with a recipe.")

files = {}
for name in ['build.py', 'guides_legal.json']:
    if os.path.exists(P(name)):
        files[name] = open(P(name), encoding='utf-8').read()

def apply_once(label, pattern, repl, done_marker):
    """Replace exactly one occurrence across the source files."""
    if any(done_marker in s for s in files.values()):
        print(f'- already applied: {label}')
        return
    hits = [(n, len(re.findall(pattern, s, flags=re.S))) for n, s in files.items()]
    total = sum(c for _, c in hits)
    if total != 1:
        sys.exit(f'ERROR: "{label}" found {total} times ({hits}). Nothing was saved.')
    name = next(n for n, c in hits if c == 1)
    files[name] = re.sub(pattern, repl, files[name], count=1, flags=re.S)
    print(f'- OK ({name}): {label}')

print('About page:')
for old_t, old_d, new_t, new_d in VALUES:
    pattern = '(' + rx(old_t) + ')(.{0,400}?)(' + rx(old_d) + ')'
    apply_once(f'{old_t} -> {new_t}', pattern,
               lambda mm, nt=new_t, nd=new_d: nt + mm.group(2) + nd, new_d)
apply_once('contact note', rx(CONTACT_OLD) + '(?! We can)', lambda mm: CONTACT_NEW, 'happy to help with a recipe')

# ------------------------------------------------------------------ save (only reached if everything matched)
for name, s in files.items():
    open(P(name), 'w', encoding='utf-8').write(s)

m = re.match(r'\[\s*\n([ \t]+)\{', recipes_raw)
indent = len(m.group(1)) if m else None
with open(P('recipes.json'), 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=indent)
    f.write('\n')

print('\nHigh Protein tag removed from: ' + (', '.join(removed) or 'none'))
print('High Protein tag now on: ' + ', '.join(kept))
print('\nDone.')
