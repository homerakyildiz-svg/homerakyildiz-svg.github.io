#!/usr/bin/env python3
"""Check public URL metadata and discovery files against the configured domain."""
import ast
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
module = ast.parse((ROOT / 'source/build.py').read_text())
BASE = next(ast.literal_eval(n.value) for n in module.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'BASE_URL' for t in n.targets))
class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals, self.alternates, self.meta = [], {}, {}
        self.local_navigation = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and a.get('rel') == 'canonical': self.canonicals.append(a.get('href'))
        if tag == 'link' and a.get('hreflang'): self.alternates[a['hreflang']] = a.get('href')
        if tag == 'meta' and a.get('property'): self.meta[a['property']] = a.get('content')
        if tag in ('a', 'img', 'script'):
            ref = a.get('href', a.get('src', ''))
            if ref.startswith(BASE): self.local_navigation.append(ref)

routes = {'index.html':'/', 'tr/index.html':'/tr/', 'cv/index.html':'/cv/', 'cv/tr.html':'/cv/tr.html'}
for file, route in routes.items():
    p = Head(); p.feed((ROOT / file).read_text())
    expected = BASE + route
    assert p.canonicals == [expected], (file, 'canonical')
    assert p.meta.get('og:url') == expected, (file, 'og:url')
    assert p.meta.get('og:image') == BASE + '/assets/omer-akyildiz.jpg', (file, 'og:image')
    cv = file.startswith('cv/')
    assert p.alternates == {'en': BASE + ('/cv/' if cv else '/'), 'tr': BASE + ('/cv/tr.html' if cv else '/tr/'), 'x-default': BASE + ('/cv/' if cv else '/')}, (file, 'language alternatives')
    assert not p.local_navigation, (file, 'navigation/assets should remain relative')
urls = [n.text for n in ElementTree.parse(ROOT / 'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls) == 4 and set(urls) == {BASE + p for p in routes.values()}, 'sitemap'
assert (ROOT / 'robots.txt').read_text() == f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n', 'robots.txt'
print('PASS: canonicals, matching language alternatives, social metadata, sitemap, robots.txt and relative navigation.')
