
# Bored of Toast V4

This is a static Python-generated website (HTML/CSS/JS). No frameworks, no build steps required for production.

## Running Locally

To start a local preview, simply run:
```bash
python serve.py
```
Then visit `http://localhost:8000` in your browser.

## Building the Site

To regenerate all HTML files after changing data or templates, run:
```bash
python build.py
```
This will output everything into the `dist/` folder, which serves as the static root of the site.

## Architecture

- **Data Sources:** `recipe_models.json` (recipes), `kitchen_notes.py` (kitchen guides), `constants.py` (shared dictionaries like categories).
- **Templates / Rendering:** `build.py` (orchestrator), `pilot_recipe.py` (recipe HTML generator), `kitchen_notes.py` (guide HTML generator).
- **Styles:** `dist/style.css`, `dist/recipe.css`, `dist/refinements.css`.
- **Interactions (Client-Side):** `dist/pilot.js` (DOM interactions), `dist/recipe-engine.js` (scaling and substitutions logic).

## Content

Currently, the site generates **30 routes** in total, including:
- **10 Recipes**
- Various Kitchen Notes and index pages

## Testing (Development Only)

Testing is done via NodeJS to simulate a real DOM environment using JSDOM. The published site remains 100% static and does not require Node.

**To setup tests:**
```bash
npm install
```
*(This installs `jsdom` as a devDependency).*

**To run tests:**
```bash
node tests/recipe-engine.cjs
node tests/recipe-dom.cjs
node tests/all-recipes.cjs
```
These tests ensure scaling logic, substitution mechanics, DOM updates, and HTML generation remain unbroken.
