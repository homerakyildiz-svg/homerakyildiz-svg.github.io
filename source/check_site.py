#!/usr/bin/env python3
"""Check local assets, anchors, language metadata and portable site paths."""
import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.languages = [], [], []
        self.lang, self.h1, self.description = None, 0, False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang')
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'meta' and a.get('name') == 'description': self.description = bool(a.get('content'))
        if tag == 'link' and a.get('hreflang'): self.languages.append(a['hreflang'])
        for key in ('href','src'):
            if a.get(key): self.refs.append(a[key])

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
root = parser.parse_args().root.resolve()
pages = {}
errors = []
for file in root.rglob('*.html'):
    page = Page()
    page.feed(file.read_text(encoding='utf-8'))
    pages[file] = page
    duplicate = [key for key, count in Counter(page.ids).items() if count > 1]
    if duplicate: errors.append(f'{file.relative_to(root)}: duplicate IDs {duplicate}')
    if page.lang not in ('en','tr'): errors.append(f'{file.name}: missing page language')
    if page.h1 != 1: errors.append(f'{file.name}: expected one h1')
    if not page.description: errors.append(f'{file.name}: missing description')
    if not {'en','tr','x-default'}.issubset(set(page.languages)):
        errors.append(f'{file.name}: missing language alternatives')

for file,page in pages.items():
    for ref in page.refs:
        parsed = urlsplit(ref)
        if parsed.scheme or parsed.netloc: continue
        if parsed.path.startswith('/'):
            errors.append(f'{file.name}: root-absolute path prevents project-site portability: {ref}')
            continue
        target = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file
        if target.is_dir(): target /= 'index.html'
        if not target.is_relative_to(root): errors.append(f'{file.name}: path escapes site root: {ref}')
        elif not target.is_file(): errors.append(f'{file.name}: missing local target: {ref}')
        elif parsed.fragment and target.suffix == '.html' and unquote(parsed.fragment) not in pages[target].ids:
            errors.append(f'{file.name}: missing anchor: {ref}')

for css in root.rglob('*.css'):
    for ref in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css.read_text(encoding='utf-8')):
        if not urlsplit(ref).scheme and not (css.parent / ref).is_file():
            errors.append(f'{css.name}: missing CSS asset {ref}')

for expected in ('index.html','tr/index.html','cv/index.html','cv/tr.html','.nojekyll',
                 'assets/Omer-Akyildiz-CV-EN.pdf','assets/Omer-Akyildiz-CV-TR.pdf'):
    if not (root / expected).is_file(): errors.append(f'Missing required file: {expected}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages; all local paths, fragment links, fonts, language metadata and CV PDFs resolve.')
