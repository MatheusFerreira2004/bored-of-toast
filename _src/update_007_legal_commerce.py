#!/usr/bin/env python3
"""Terms of Use and Privacy Policy: digital products (Lemon Squeezy) and email sign-ups (MailerLite).

Terms: purchases, license, 14-day refunds, products are cooking education (not medical advice).
Privacy: email sign-ups via MailerLite, purchases via Lemon Squeezy, third-party cookies.

Nothing is saved unless every section is found. Safe to re-run.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'guides_legal.json')
gl = json.load(open(P, encoding='utf-8'))
DATE = 'October 9, 2026'
MARK = 'Lemon Squeezy, which acts as our reseller and merchant of record'


def find_doc(first_heading):
    for k, v in gl.items():
        if isinstance(v, dict) and isinstance(v.get('sections'), list):
            if any(s.get('h') == first_heading for s in v['sections']):
                return k, v
    sys.exit(f'ERROR: legal page with section "{first_heading}" not found (nothing was saved).')


def sec(doc, h):
    for s in doc['sections']:
        if s.get('h') == h:
            return s
    sys.exit(f'ERROR: section "{h}" not found (nothing was saved).')


def insert_after(doc, after_h, new):
    i = next((n for n, s in enumerate(doc['sections']) if s.get('h') == after_h), None)
    if i is None:
        sys.exit(f'ERROR: section "{after_h}" not found (nothing was saved).')
    for off, s in enumerate(new, 1):
        doc['sections'].insert(i + off, s)


tkey, terms = find_doc('Welcome to Bored of Toast')
pkey, privacy = find_doc('The Short Version')

if any(MARK in p for s in terms['sections'] for p in s.get('p', [])):
    print('Already applied. Nothing to do.')
    sys.exit(0)

# ------------------------------------------------------------------ Terms
sec(terms, 'Welcome to Bored of Toast')['p'] = [
    'These terms apply to your use of the Bored of Toast website and to the digital products you buy from us. By browsing the site or making a purchase, you agree to them. If you do not agree, please do not use the site.',
    'Our recipes and guides are free to read. We also sell downloadable digital products, such as the Nourished cookbook collection. The sections on purchases and refunds below apply to those products.'
]
insert_after(terms, 'Content Ownership and Sharing', [
    {'h': 'Digital Products and Purchases', 'p': [
        'Our digital products are delivered as downloadable PDF files. Prices are shown in US dollars on the product page.',
        'Purchases are processed by Lemon Squeezy, which acts as our reseller and merchant of record. Lemon Squeezy handles payment and any applicable sales tax or VAT, and sends your receipt and download access by email. Its own terms and privacy policy apply to the checkout.',
        'When you buy a product, you receive a personal, non-transferable license to download, read and print it for use in your own household. Please do not share, resell or republish the files, or upload them to other websites.'
    ]},
    {'h': 'Refunds', 'p': [
        'If a product is not right for you, email hello@boredoftoast.com within 14 days of your purchase and we will refund you in full. You do not need to give a reason.',
        'Refunds are returned to your original payment method through Lemon Squeezy. After a refund, please delete your copies of the files.'
    ]}
])
rec = sec(terms, 'Recipe Results, Food Safety, and Allergies')
rec['p'].append('Our digital products, including those written for adults using GLP-1 medication, are general cooking education. They are not medical or nutrition advice and do not replace guidance from your doctor, dietitian or care team.')
nut = sec(terms, 'Nutrition Information')
nut['p'] = [p.replace('calculated with online tools from typical ingredient values', 'calculated from typical ingredient values') for p in nut['p']]
terms['updated'] = DATE

# ------------------------------------------------------------------ Privacy
short = sec(privacy, 'The Short Version')
short['p'][0] = ('Bored of Toast is a small recipe website that also sells downloadable cookbooks. We do not ask you to create an account, '
                 'and we do not sell your personal information. This page explains, in plain English, what information is involved when you '
                 'visit the site, sign up for our emails or buy a product, and what we do with it.')
sec(privacy, 'Information You Choose to Share')['p'] = [
    'Our contact form works by opening your own email app with a pre-filled message to us. We do not store form entries on our servers. When you send that email, we receive your email address, your name if you include it, and whatever you write. We use it only to read and reply to your message.'
]
insert_after(privacy, 'Information You Choose to Share', [
    {'h': 'Email Sign-Ups', 'p': [
        'When you sign up for a free resource such as the GLP-1 Kitchen Starter Kit, you give us your email address and, if you choose, your first name. We use MailerLite to store this information and send our emails.',
        'We use your email to deliver what you asked for and to send occasional recipes, tips and information about our products. Every email includes a link to unsubscribe, and you can ask us to delete your details at any time.',
        'MailerLite may record whether an email is opened or a link is clicked, which helps us understand what is useful. MailerLite\u2019s privacy policy applies to how it processes this data.'
    ]},
    {'h': 'Purchases', 'p': [
        'When you buy a digital product, the checkout is run by Lemon Squeezy, our reseller and merchant of record. Lemon Squeezy collects your name, email address, billing details and payment information to process the order, calculate taxes and deliver your files. We do not see or store your full card details.',
        'Lemon Squeezy shares with us the information we need to support your order, such as your name, email address, the product you bought and the order status. Lemon Squeezy\u2019s privacy policy applies to the checkout.'
    ]}
])
sec(privacy, 'Cookies and Third-Party Services')['p'].append(
    'Our email sign-up and checkout pages are hosted by MailerLite and Lemon Squeezy and may use their own cookies, for example to keep your checkout session working.')
privacy['updated'] = DATE

with open(P, 'w', encoding='utf-8') as f:
    json.dump(gl, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(f'OK: {tkey} (purchases, license, 14-day refunds, product disclaimer) and {pkey} (MailerLite, Lemon Squeezy, cookies) updated.')
