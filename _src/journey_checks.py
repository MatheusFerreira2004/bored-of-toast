#!/usr/bin/env python3
"""Check visitor destinations and availability across integration states. No external calls."""
from pathlib import Path
from html.parser import HTMLParser
from itertools import product
from urllib.parse import urlsplit, unquote
import json
from storefront import build_storefront, validate_config

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls=[]; self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a':self.urls.append(a.get('href',''))

def parse(text):
    p=Links();p.feed(text);return p

def render(config):
    pages={}
    def page(path,title,desc,body,*args,**kwargs):pages[path]=body
    build_storefront(page,validate_config(config));return pages

states=0
for signup,download,checkout in product([False,True],repeat=3):
    c={k:('https://provider.example/'+k if enabled else None) for k,enabled in zip(['signup_url','download_url','checkout_url'],[signup,download,checkout])}
    pages=render(c);kit=pages['starter-kit/'];paid=pages['nourished/'];thanks=pages['starter-kit/thanks/']
    ku,pu,tu=map(lambda t:parse(t).urls,[kit,paid,thanks])
    assert ('Get the full collection' in paid)==checkout
    assert (c['checkout_url'] in pu)==checkout
    assert ('Purchasing is not open yet' in paid)==(not checkout)
    assert ('Four English PDFs' in paid) and ('US$20' in paid)
    assert ('89 pages' in paid) and ('26 pages' in paid)
    if signup:
        assert c['signup_url'] in ku and 'Get the free starter kit' in kit
    elif download:
        assert c['download_url'] in ku and 'Download the free starter kit' in kit
    else:
        assert 'separate, one-page' in kit and 'delivery is not open yet' in kit
        assert '../printables/nourished-weekly-planner-sample.pdf' in ku
    assert (c['download_url'] in tu)==download
    if not download:assert 'does not confirm an email signup' in thanks
    for text in pages.values():
        p=parse(text)
        for url in p.urls:
            if url.startswith('#'):assert url[1:] in p.ids,(url,p.ids)
    states+=1
for url in ['http://provider.example','javascript:alert(1)','https://user:password@provider.example','https://provider.example/ bad']:
    try:validate_config({'checkout_url':url})
    except ValueError:pass
    else:raise AssertionError('Invalid URL accepted')
validate_config({'social_urls':{'instagram':'https://www.instagram.com/example/'}})
# Check same-page and cross-page fragments on the actual generated site.
root=Path(__file__).resolve().parent.parent
for f in root.rglob('*.html'):
    if '_src' in f.relative_to(root).parts:continue
    p=parse(f.read_text())
    for href in p.urls:
        if href=='#':raise AssertionError(f'{f}: empty placeholder link')
        u=urlsplit(href)
        if u.scheme or u.netloc or not u.fragment:continue
        dest=(f.parent/unquote(u.path)).resolve() if u.path else f
        if dest.is_dir():dest=dest/'index.html'
        assert dest.exists(),(f,href)
        assert unquote(u.fragment) in parse(dest.read_text()).ids,(f,href,'missing fragment')
print(f'Journey checks passed: {states} integration states; generated link fragments and URL validation.')
