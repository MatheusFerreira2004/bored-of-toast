#!/usr/bin/env python3
"""Keeps old rewrite scripts from re-applying themselves.

update_003_breakfasts.py, update_004_soups_bowl.py and update_005_mains.py decide whether a
recipe was already rewritten by comparing its kitchen *note* with the note they wrote. Later
editorial scripts (031, 032, 033) legitimately edit some of those notes, so on every run the old
scripts thought the recipe was new and re-applied their whole original version (title, tips,
note...), which the later scripts then had to fix again. The final file looked stable, but any
edit not re-done by a later script would have been silently lost.

This script runs first (000) and changes that single check in the three files to compare the
short card *desc* instead, a field no later script edits. It touches nothing else and does
nothing if the check is already updated. Safe to re-run.
"""
import os, sys

sys.stderr = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
OLD = "if r.get('note') == fields['note']:"
NEW = "if r.get('desc') == fields['desc']:"
FILES = ['update_003_breakfasts.py', 'update_004_soups_bowl.py', 'update_005_mains.py']

for name in FILES:
    path = os.path.join(HERE, name)
    src = open(path, encoding='utf-8').read()
    if NEW in src and OLD not in src:
        print(f'- already applied: {name}')
        continue
    if src.count(OLD) != 1:
        print(f'ERROR: expected exactly one note check in {name}, found {src.count(OLD)}. Nothing was changed.')
        sys.exit(1)
    open(path, 'w', encoding='utf-8').write(src.replace(OLD, NEW))
    print(f'- OK: {name} now detects applied recipes by desc')
print('Done.')
