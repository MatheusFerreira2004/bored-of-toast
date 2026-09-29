#!/usr/bin/env python3
"""Generate responsive WebP variants for every photo in ../images.

For each images/<name>.webp (the original, always kept as the largest size) this writes
images/<name>-<w>w.webp for every width in WIDTHS that is clearly smaller than the original,
and records them in images/variants.json. build.py reads that manifest to emit srcset/sizes.

Run from the project root after adding or replacing a photo:
    python3 _src/make_images.py            # only creates missing variants
    python3 _src/make_images.py --force    # regenerates everything
Requires Pillow (pip install pillow). The site build itself does not need it.
"""
import glob, json, os, re, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.normpath(os.path.join(HERE, '..', 'images'))
WIDTHS = [160, 320, 480, 720, 1100]
QUALITY = 78
FORCE = '--force' in sys.argv
VARIANT_RE = re.compile(r'-\d+w\.webp$')

manifest = {}
made = 0
for path in sorted(glob.glob(os.path.join(IMG, '*.webp'))):
    name = os.path.basename(path)
    if VARIANT_RE.search(name):
        continue
    with Image.open(path) as im:
        im.load()
        width, height = im.size
        variants = []
        for w in WIDTHS:
            if w > width * 0.9:      # not worth a variant that is almost the original
                continue
            out = path[:-len('.webp')] + f'-{w}w.webp'
            if FORCE or not os.path.exists(out):
                h = round(height * w / width)
                im.resize((w, h), Image.LANCZOS).save(out, 'WEBP', quality=QUALITY, method=6)
                made += 1
            variants.append(w)
    manifest['images/' + name] = {'width': width, 'variants': variants}

with open(os.path.join(IMG, 'variants.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=1, sort_keys=True)
    f.write('\n')
print(f'{len(manifest)} originals, {made} variants created, manifest written')
