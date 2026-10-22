"""update_901: align the site with the final Nourished PDFs and the chosen checkout.

1. Page counts and features match the PDFs built in nourished-product:
   main 57, 28-Day 15, Recipe Pack 18, Printable 14 (104 total), Starter Kit 10.
   No fillable fields are promised (the PDFs do not have them).
2. Lemon Squeezy / MailerLite are replaced by Payhip (store, delivery, emails) + Stripe (cards)
   on the Nourished page, Terms and Privacy.
3. The four new covers from PR #45 (commit f420bf06) are restored in images/commerce/,
   because a later commit put the old illustrated cover back.
4. storefront.json download_url is cleared: the old 9-page starter PDF in printables/ no longer
   matches the final 10-page kit. Delivery returns when the Payhip free product link is added.

Idempotent: already-applied text is reported and skipped. Test files are never edited.
"""
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / '_src'
SKIP = {'checks.py', 'journey_checks.py'}

PINNED = ('https://raw.githubusercontent.com/MatheusFerreira2004/bored-of-toast/'
          'f420bf065f07757bd2f1b5c2d4066d74c0d6e64a/images/commerce/')
COVERS = ['nourished-cover.jpg', 'meal-plan-cover.jpg', 'recipe-pack-cover.jpg', 'printable-pack-cover.jpg']

# (old, new). Longer phrases first so shorter ones do not break them.
REPLACEMENTS = [
    # --- Nourished page: counts and features ---
    ("storage notes and flexible planning guidance.', 64, 'main')", "storage notes and flexible planning guidance.', 57, 'main')"),
    ("prep routines and leftovers guidance.', 26, 'blue')", "prep routines and leftovers guidance.', 15, 'blue')"),
    ("substitutions and storage guidance.', 16, 'terracotta')", "substitutions and storage guidance.', 18, 'terracotta')"),
    ("11 planning tools, an index and a getting-started page. Selected sheets include 105 fillable fields.', 13, 'sage')",
     "11 planning tools, an index and a getting-started page, ready to print or annotate.', 14, 'sage')"),
    ("4 digital PDFs · 119 pages · Read, print or fill selected sheets", "4 digital PDFs · 104 pages · Read or print"),
    ("Four English PDFs, 119 pages, ready to save or print, with selected fillable sheets.", "Four English PDFs, 104 pages, ready to save or print."),
    ("Together they contain 119 pages:", "Together they contain 104 pages:"),
    ("36 recipes · 4 weeks of meal examples · 11 planning tools · Selected fillable sheets",
     "36 recipes · 4 weeks of meal examples · 11 printable planning tools"),
    ("<span>11 planning tools · Selected fillable sheets</span>", "<span>11 printable planning tools</span>"),
    ("The 26-page 28-Day Meal Plan", "The 15-page 28-Day Meal Plan"),
    ("You can also write on them in a PDF annotation app. The Weekly Meal Planner, Symptom &amp; Food Log and Master Shopping List also have fillable fields. Use a PDF reader that supports forms and save a copy; the other tools remain printable or can be annotated.",
     "You can also write on a copy in a PDF annotation app."),
    ("clearer references and selected fillable sheets.", "clearer references and one consistent design throughout."),
    ("prep notes and printable or selected fillable sheets in four PDFs", "prep notes and printable sheets in four PDFs"),
    (" The weekly planner, food log and shopping checklist also have fields you can type into.", ""),
    ("9-page", "10-page"),
    ("9 pages. English PDF", "10 pages. English PDF"),
    ("?v=20261013-revised", "?v=20261022-covers"),
    # --- Nourished page: checkout ---
    ("Checkout is handled by Lemon Squeezy, our reseller and merchant of record. Prices are in US dollars, and any sales tax or VAT for your location is calculated at checkout.",
     "Checkout is handled by Payhip, with card payments processed by Stripe. Prices are in US dollars, and any sales tax or VAT that applies to your location is shown at checkout."),
    ("Lemon Squeezy emails your receipt and download access for the four PDFs.",
     "Payhip emails your receipt and download access for the four PDFs."),
    # --- Terms ---
    ("Purchases are processed by Lemon Squeezy, which acts as our reseller and merchant of record. Lemon Squeezy handles payment and any applicable sales tax or VAT, and sends your receipt and download access by email. Its own terms and privacy policy apply to the checkout.",
     "Purchases are made through Payhip, our online store platform, and card payments are processed by Stripe. Payhip shows any applicable sales tax or VAT at checkout and sends your receipt and download access by email. The terms and privacy policies of Payhip and Stripe apply to the checkout."),
    ("Refunds are returned to your original payment method through Lemon Squeezy.",
     "Refunds are returned to your original payment method through Payhip."),
    # --- Privacy ---
    ("We use MailerLite to store this information and send our emails.",
     "We use Payhip, the platform that delivers the kit, to store this information and send our emails."),
    ("MailerLite may record whether an email is opened or a link is clicked, which helps us understand what is useful. MailerLite’s privacy policy applies to how it processes this data.",
     "Payhip may record whether an email is opened or a link is clicked, which helps us understand what is useful. Payhip’s privacy policy applies to how it processes this data."),
    ("When you buy a digital product, the checkout is run by Lemon Squeezy, our reseller and merchant of record. Lemon Squeezy collects your name, email address, billing details and payment information to process the order, calculate taxes and deliver your files.",
     "When you buy a digital product, the checkout is run by Payhip, and card payments are processed by Stripe. Payhip and Stripe collect your name, email address, billing details and payment information to process the order, calculate taxes and deliver your files."),
    ("Lemon Squeezy shares with us the information we need to support your order, such as your name, email address, the product you bought and the order status. Lemon Squeezy’s privacy policy applies to the checkout.",
     "Payhip shares with us the information we need to support your order, such as your name, email address, the product you bought and the order status. The privacy policies of Payhip and Stripe apply to the checkout."),
    ("Our email sign-up and checkout pages are hosted by MailerLite and Lemon Squeezy",
     "Our email sign-up and checkout pages are hosted by Payhip"),
]
# Optional: applied when found, never an error.
OPTIONAL = [("Last updated October 9, 2026", "Last updated October 22, 2026")]


def candidates():
    files = []
    for p in sorted(SRC.glob('*.py')) + sorted(SRC.glob('*.json')):
        if p.name in SKIP or p.name.startswith('update_'):
            continue
        files.append(p)
    return files


def apply_text():
    files = {p: p.read_text(encoding='utf-8') for p in candidates()}
    original = dict(files)
    missing = []
    for old, new in REPLACEMENTS:
        hit = [p for p, t in files.items() if old in t]
        if hit:
            for p in hit:
                files[p] = files[p].replace(old, new)
            print(f'- OK: {old[:70]}')
        elif new and any(new in t for t in files.values()):
            print(f'- already applied: {old[:70]}')
        elif not new:
            print(f'- already applied (removed): {old[:70]}')
        else:
            missing.append(old)
    for old, new in OPTIONAL:
        for p, t in files.items():
            if old in t:
                files[p] = t.replace(old, new)
                print(f'- OK (optional): {old}')
    if missing:
        print('ERROR: these phrases were not found. Nothing was saved.')
        for m in missing:
            print('  - ' + m[:160])
        sys.exit(1)
    for p, t in files.items():
        if t != original[p]:
            p.write_text(t, encoding='utf-8')
    leftovers = [p.name for p, t in files.items() if 'Lemon Squeezy' in t or 'MailerLite' in t]
    print('Leftover Lemon Squeezy/MailerLite mentions in: ' + (', '.join(leftovers) if leftovers else 'none'))


def clear_download_url():
    path = SRC / 'storefront.json'
    cfg = json.loads(path.read_text(encoding='utf-8'))
    if cfg.get('download_url'):
        cfg['download_url'] = None
        path.write_text(json.dumps(cfg, indent=2) + '\n', encoding='utf-8')
        print('- OK: download_url cleared (old 9-page starter PDF no longer matches the kit)')
    else:
        print('- already applied: download_url is empty')


def restore_covers():
    dest_dir = ROOT / 'images' / 'commerce'
    for name in COVERS:
        data = urllib.request.urlopen(PINNED + name, timeout=30).read()
        if len(data) < 5000:
            print(f'ERROR: pinned cover {name} looks empty ({len(data)} bytes)')
            sys.exit(1)
        dest = dest_dir / name
        if dest.exists() and dest.read_bytes() == data:
            print(f'- already applied: {name} is the new cover')
        else:
            dest.write_bytes(data)
            print(f'- OK: {name} restored from commit f420bf06 ({len(data) // 1024} KB)')


if __name__ == '__main__':
    apply_text()
    clear_download_url()
    restore_covers()
    print('Done.')
