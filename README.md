# Bored of Toast

Good food without the fuss. Live site: https://matheusferreira2004.github.io/bored-of-toast/

## How this site is built
The pages are generated from content files by a small Python script, so every recipe has its own fast, SEO-friendly page.

- `_src/recipes.json`: all recipes (ingredients, steps, tips, nutrition, notes)
- `_src/guides_legal.json`: kitchen guides, privacy policy and terms
- `_src/build.py`: the generator (pages, Recipe schema for Google, sitemap, search index)
- `_src/styles.css`, `_src/app.js`: design and interactive features

To add a recipe: add an object to `recipes.json`, add its photo to `images/<id>.webp`, then run `python3 _src/build.py` from a copy of the project.

## Features
Recipe pages with servings scaler, US/metric toggle, cook mode (keeps screen awake), shopping list, step photos, Pinterest pins, print view, search, diet badges, weekly meal plan, guides and a sitemap.
