#!/usr/bin/env python3
"""The closed-checkout button and note are shared by the hero and the final offer.
In the final offer, #collection and "How buying works" are above, so "↓" and "below" were wrong.
Neutral wording for both places. Idempotent; nothing saved unless each anchor resolves."""
import os, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'storefront.py')
s = open(p, encoding='utf-8').read()
PAIRS = [
    ('href="#collection">Purchasing opens soon · see what’s included ↓</a>',
     'href="#collection">Purchasing opens soon · see what’s included</a>'),
    ("else 'Planned as a one-time US$20 purchase. See how buying works below.')",
     "else 'Planned as a one-time US$20 purchase. Details are in How buying works on this page.')"),
]
for old, new in PAIRS:
    if new in s:
        print('already applied:', new[:60])
    elif s.count(old) == 1:
        s = s.replace(old, new)
        print('OK:', new[:60])
    else:
        print(f'ERROR: anchor found {s.count(old)} times: {old[:80]}. Nothing was saved.')
        sys.exit(1)
open(p, 'w', encoding='utf-8').write(s)
print('Done.')
