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

## Nourished storefront (draft)

The generated site now includes `starter-kit/`, `starter-kit/thanks/`, and `nourished/`, two homepage sections, a Cookbook navigation entry, search entries and contextual kit links on five related recipes. The previews under `images/commerce/` are rendered from the actual product PDFs; they are samples, not the paid files. No full paid PDF is stored in this repository.

`_src/storefront.py` contains the templates and `_src/storefront.json` contains public integration URLs:

- `signup_url`: HTTPS URL of the hosted email signup page. Set the provider's successful-signup redirect to the deployed `starter-kit/thanks/` page.
- `download_url`: HTTPS URL for authorized delivery of the free kit. The thanks page does not provide access control; use provider delivery or access controls if the download must be gated.
- `checkout_url`: HTTPS URL for the US$20 collection checkout. Configure payment, applicable taxes, confirmation and paid-file delivery in the provider.

Leave a value `null` until that destination exists. When a service is not connected, the pages explain its availability and offer the existing free planner sample. A buy button appears only with `checkout_url`; a full-kit button appears only with an actual signup or download destination. There is no pretend form submission, success event, or payment button. Never put passwords, API keys, private download credentials, or the complete paid bundle in this public configuration/repository.

Rebuild the site after changing the URLs. The thanks page is noindex and excluded from the sitemap. Public URLs must be absolute HTTPS URLs; invalid configured URLs stop the build.

Before launch, verify the checkout price and one-time purchase setting, actual signup consent and unsubscribe flow, support address, delivery and purchase conditions, update Privacy/Terms for the selected services, connect the real social profile URLs, add measurement, and choose hosting appropriate for the commercial site. GitHub Pages has restrictions on sites primarily facilitating commercial transactions; a custom domain does not remove those restrictions.

The three integrations are deliberately unconfigured in this draft. The existing recipe site's "tested" and weekly-update statements were not extended to Nourished; their support remains a separate editorial review item.

## Five easy dinners

The existing `meal-plan/` URL is retained, but navigation and copy now describe a fixed collection of five dinner ideas. Visitors can add one or all five original recipe batches, see the portions, and open the shopping list directly. Existing saved recipes retain their adjusted quantities and checked items on repeated additions. Ingredients remain grouped by recipe; optional sides and weekend extras are separate. No complete-day or weekly nutrition claim is made.


## Visitor journey and integration handoff — October 6, 2026

| Entry point | Next action | Availability today |
|---|---|---|
| Home / five related recipes | Explore the free GLP-1 kit | Kit preview and public planner sample; full-kit delivery pending |
| Any page footer | Free GLP-1 kit or Cookbook | Both point to existing pages |
| Starter kit hero | Free sample options | Scrolls to the actual available action |
| Starter kit offer | Open one-page planner sample | Public PDF; clearly distinguished from the nine-page kit |
| Nourished hero / final offer | Try the free planner | Scrolls to the public printable; purchase explicitly pending |
| Nourished previews | Open real corrected-edition page | Images match current product PDFs |
| Signup-return page | Provider's configured kit download | No signup success is inferred from merely opening the page |

The static site does not process payments, send email, control access or establish a paid order. Configure those operations in the chosen provider; this website links to them.

Connect the three destinations separately: `signup_url` for email signup, `download_url` for the kit's delivery destination, and `checkout_url` for the one-time US$20 checkout. If email capture is desired, connect signup first; a direct kit link is shown only when signup is absent and a download destination is available. Configure the provider's return URL as `starter-kit/thanks/`. Use provider-controlled email delivery or authorization for any gated download. The return page is public and cannot prove signup or unlock a purchase.

The main guide and all three bonuses belong in the payment/delivery provider, not in this public repository. Use the current 89/26/18/12-page PDFs. Test a real provider test-mode order, actual receipt and access to every file before turning on the live checkout. No shipping or physical book is offered. Confirm actual support contact, purchase terms and provider privacy information before accepting orders.

`social_urls` accepts the actual Instagram, Pinterest and Facebook profile HTTPS URLs. Until configured, their footer icons are omitted; no `href="#"` placeholder sends visitors to the top of the page. The About-page contact address and handle still need owner confirmation. Its form now explicitly opens an email draft and preserves the entered text; the website does not send or confirm that message.

Run `python3 _src/journey_checks.py` alongside the existing site checks. It checks the rendered experience for missing integrations, signup-first, download-only and checkout-enabled states, and rejects non-HTTPS or credential-bearing URLs. It does not submit forms or payments. Visual mobile checks, physical printing, full-kit signup and a real order remain pending.
