#!/usr/bin/env python3
"""Photo review, round 3 (applied earlier; now superseded).

History:
1. tuna-white-bean-salad became "Tuna & Chickpea Salad with Soft Eggs" with Pexels 6632288 (Alesia Kozik).
   That recipe and photo are already in recipes.json / credits.json.
2. baked-cinnamon-apples got a rawpixel image (rawpixel 3282699). The served file carried rawpixel
   watermarks, so update_039 replaces it with a watermark-free Pexels photo.

This script used to re-download its photos whenever credits.json differed from its own URLs. That would
restore the watermarked apple photo on every run, so it now only verifies that its tuna change is in
place and leaves photos to later scripts. Safe to re-run.
"""
import json, os, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)

TUNA = 'tuna-white-bean-salad'
TUNA_TITLE = 'Tuna & Chickpea Salad with Soft Eggs'
TUNA_PHOTO = 'https://www.pexels.com/photo/close-up-photo-of-a-dish-with-chickpeas-and-tuna-6632288/'

recipes = {r['id']: r for r in json.loads(open(P('recipes.json'), encoding='utf-8').read())}
credits = json.loads(open(P('credits.json'), encoding='utf-8').read())

if TUNA not in recipes:
    print(f'ERROR: {TUNA} not found in recipes.json. Nothing was saved.')
    sys.exit(1)
if recipes[TUNA]['title'] != TUNA_TITLE or credits.get(TUNA, {}).get('photo_url') != TUNA_PHOTO:
    print(f'ERROR: the tuna recipe or photo is not the round-3 version. Restore it from git history. Nothing was saved.')
    sys.exit(1)
print('Already applied. Nothing to do (apple photo is handled by update_039).')
