#!/usr/bin/env python3
"""Regenerate the responsive variants of images/our-story.webp.

update_017 replaced the main About photo, but make_images.py only creates *missing* variants,
so the old 160w/320w/480w files (photo of a person) were kept. This removes them and rebuilds them
from the new photo. A marker file makes the script run only once.
"""
import glob, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.normpath(os.path.join(HERE, '..', 'images'))
MARKER = os.path.join(HERE, 'about_variants_refreshed.txt')

if os.path.exists(MARKER):
    print('Already applied. Nothing to do.')
    sys.exit(0)
if not os.path.exists(os.path.join(HERE, 'update_017_about_photo.py')):
    sys.exit('ERROR: update_017_about_photo.py is missing (nothing was changed).')

old = glob.glob(os.path.join(IMG, 'our-story-*w.webp'))
for f in old:
    os.remove(f)
print(f'- removed {len(old)} old About photo variants')

subprocess.check_call([sys.executable, os.path.join(HERE, 'make_images.py')])
open(MARKER, 'w').write('our-story variants regenerated from the Pexels photo (update_018).\n')
print('OK: About photo variants regenerated.')
