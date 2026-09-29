# Bored of Toast

Good food without the fuss. Live site: https://matheusferreira2004.github.io/bored-of-toast/

## How this site is built
The pages are generated from content files by a small Python script, so every recipe has its own fast, SEO-friendly page.

- `_src/recipes.json`: all recipes (ingredients, steps, tips, nutrition, notes)
- `_src/guides_legal.json`: kitchen guides, privacy policy and terms
- `_src/build.py`: the generator (pages, Recipe schema for Google, sitemap, search index)
- `_src/styles.css`, `_src/app.js`: design and interactive features
- `fonts/`: self-hosted WOFF2 fonts (Fraunces, Inter, Caveat, latin subset). No request goes to Google Fonts.

To add a recipe: add an object to `recipes.json`, add its photo to `images/<id>.webp`, run `python3 _src/make_images.py` (creates the responsive sizes), then build:

```
mkdir -p _src/site && cp -r images _src/site/images
python3 _src/build.py          # writes the site to _src/site
# copy everything in _src/site except images/ to the project root, then commit
python3 _src/checks.py         # sanity checks (also run automatically on every pull request)
```

## Responsive images
- `images/<name>.webp` is the original (always the largest size). `_src/make_images.py` (needs `pip install pillow`) writes `images/<name>-<w>w.webp` for 160/320/480/720/1100 px when smaller than the original, and records them in `images/variants.json`.
- `build.py` reads that manifest and adds `srcset` + `sizes` to every photo. The `SIZES` table at the top of `build.py` says how wide each kind of image is drawn (measured at 360-1440 px screens). If you change a layout, update the matching entry, otherwise photos may look soft or download too much.

## Fonts
Fonts are self-hosted in `fonts/` (Fraunces, Inter, Caveat, latin subset), so no request goes to Google. `styles.css` also defines `Fraunces Fallback` and `Inter Fallback`: Arial / Times New Roman resized to the web fonts' dimensions, so text does not jump when the web font loads. If you change fonts, rebuild the site, serve `_src/site` on port 8804 and run `python3 _src/font_metrics.py` to recalculate the values.

## Checks
`.github/workflows/checks.yml` regenerates the site on every push and pull request and fails if it differs from what is committed, then runs `_src/checks.py`: broken links, missing titles / descriptions / single `<h1>` / skip link / `alt`, Recipe structured data fields, no Google Fonts, image (200 KB) and page (80 KB) budgets, and that every responsive image size exists.

## Measuring traffic (UTM)
No analytics is installed yet (the `ANALYTICS` slot in `_src/build.py` is empty). Tag every link you post anyway, so the data is clean the day you turn analytics on:

```
https://matheusferreira2004.github.io/bored-of-toast/recipes/overnight-oats/?utm_source=pinterest&utm_medium=social&utm_campaign=fall-breakfasts&utm_content=oats-pin-01
```

| parameter | use | examples |
|---|---|---|
| `utm_source` | where the click comes from | `pinterest`, `instagram`, `facebook`, `email` |
| `utm_medium` | kind of channel | `social` (organic posts), `email`, `paid` |
| `utm_campaign` | the push it belongs to (short, lowercase, hyphens) | `fall-breakfasts`, `launch` |
| `utm_content` | which pin / post / button | `oats-pin-01`, `carousel-3`, `footer-cta` |

To turn analytics on, put its `<script>` tag in `ANALYTICS` in `_src/build.py`, rebuild, and update the Privacy page (it currently only says analytics may be added in the future).

## Features
Recipe pages with servings scaler, US/metric toggle, cook mode (keeps screen awake), shopping list, step photos, Pinterest pins, print view, search, diet badges, weekly meal plan, guides and a sitemap.
