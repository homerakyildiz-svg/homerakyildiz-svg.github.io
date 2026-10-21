#!/usr/bin/env python3
"""Rebuild the static English/Turkish pages. Python 3 standard library only.

In the handover ZIP: python3 source/build.py
In the development folder: python3 source/build.py --output site
The supplied PDFs are retained; the generated CV HTML can also be printed to PDF.
"""
import argparse
import html
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parent
DATA = json.loads((SOURCE / 'content.json').read_text(encoding='utf-8'))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=SOURCE.parent)
ARGS = parser.parse_args()
OUT = ARGS.output.resolve()
BASE_URL = 'https://omer-akyildiz.com'

def esc(value):
    return html.escape(str(value), quote=True)

def head(lang, prefix, cv=False):
    t = DATA['languages'][lang]
    title = DATA['name'] + ' | ' + (t['cv'] if cv else t['role'])
    en_url = BASE_URL + ('/cv/' if cv else '/')
    tr_url = BASE_URL + ('/cv/tr.html' if cv else '/tr/')
    canonical_url = en_url if lang == 'en' else tr_url
    person = {'@context':'https://schema.org','@type':'Person','name':DATA['full_name'],
              'alternateName':DATA['name'],'jobTitle':t['role'],
              'sameAs':[DATA['scholar'],DATA['orcid']],
              'knowsAbout':t['interests']}
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(t['description'])}">
  <meta name="theme-color" content="#513d58">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{BASE_URL}/assets/omer-akyildiz.jpg">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(t['description'])}">
  <meta property="og:locale" content="{'en_GB' if lang == 'en' else 'tr_TR'}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="tr" href="{tr_url}">
  <link rel="alternate" hreflang="x-default" href="{en_url}">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="{prefix}assets/fonts/source-sans-regular.ttf" as="font" type="font/ttf" crossorigin>
  <link rel="preload" href="{prefix}assets/fonts/literata-regular.ttf" as="font" type="font/ttf" crossorigin>
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script src="{prefix}assets/site.js" defer></script>
  <script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>
</head>'''

def profiles(lang, css=''):
    scholar = DATA['scholar'].replace('hl=en', 'hl=' + ('tr' if lang == 'tr' else 'en'))
    return f'''<div class="{css}"><a href="{esc(scholar)}">Google Scholar</a><a href="{esc(DATA['orcid'])}">ORCID</a></div>'''

def rail(lang, prefix):
    t = DATA['languages'][lang]
    home = 'index.html'
    nav = ''.join(f'<a href="#{section}">{esc(label)}</a>' for section, label in zip(
        ['about','research','background','talks','contact'],t['nav']))
    en = f'<a href="{prefix}index.html" lang="en" hreflang="en" '+ ('aria-current="page"' if lang=='en' else 'data-language-link') + '>EN</a>'
    tr = f'<a href="{prefix}tr/index.html" lang="tr" hreflang="tr" '+ ('aria-current="page"' if lang=='tr' else 'data-language-link') + '>TR</a>'
    return f'''<a class="skip-link" href="#main">{esc(t['skip'])}</a>
<aside class="rail">
  <div class="rail-top">
    <a class="wordmark" href="{home}" aria-label="Ömer Akyıldız"><span>Ömer</span><span>Akyıldız</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>
      <svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 5h16M2 10h16M2 15h16"/></svg>{esc(t['menu'])}
    </button>
  </div>
  <p class="rail-role">{esc(t['role'])}</p>
  <nav class="site-nav" id="site-nav" aria-label="{esc(t['nav_label'])}">{nav}</nav>
  <div class="rail-bottom">
    <nav class="language-switch" aria-label="{esc(t['language_label'])}">{en}{tr}</nav>
    {profiles(lang, 'rail-links')}
  </div>
</aside>'''

def publications(items, lang, chapters=False):
    t = DATA['languages'][lang]
    rows = []
    for p in items:
        title = esc(p['title'])
        title_markup = f'<span lang="{p.get("title_lang", "en")}">{title}</span>'
        if p.get('url'):
            title_markup = f'<a class="publication-title-link" href="{esc(p["url"])}">{title_markup}</a>'
        alt = f'<p class="publication-alt" lang="en">{esc(p["english_title"])}</p>' if lang=='en' and p.get('english_title') else ''
        links = []
        if p.get('url'):
            links.append(f'<a href="{esc(p["url"])}">{esc(t["book_link"] if chapters else t["publisher"])}</a>')
        if p.get('doi'):
            links.append(f'<a href="{esc(p["doi"])}">DOI</a>')
        links_markup = '<div class="publication-links">' + ''.join(links) + '</div>' if links else ''
        rows.append(f'''<li class="publication">
  <span class="publication-year">{esc(p['year'])}</span>
  <div><h3>{title_markup}</h3>{alt}
    <p class="publication-meta">{esc(p['authors'])}<br><cite>{esc(p['venue'])}</cite></p>
    {links_markup}
  </div>
</li>''')
    return '<ul class="publication-list">' + '\n'.join(rows) + '</ul>'

def manuscripts(lang, cv=False):
    t = DATA['languages'][lang]
    title_level = 3 if cv else 4
    rows = ''.join(f'''<div class="manuscript"><h{title_level} class="manuscript-title" lang="en">{esc(p['title'])}</h{title_level}><p>{esc(t[p['status']])}</p></div>''' for p in DATA['manuscripts'])
    level = 2 if cv else 3
    return f'<div class="manuscripts"><h{level}>{esc(t["manuscripts"])}</h{level}>{rows}</div>'

def career(items, lang, cv=False):
    level = 3 if cv else 4
    rows = []
    for item in items:
        c = item[lang]
        detail = f'<p class="career-detail">{esc(c["detail"])}</p>' if c.get('detail') else ''
        rows.append(f'''<div class="career-item"><p class="career-date">{esc(item['dates'])}</p><h{level}>{esc(c['title'])}</h{level}><p class="career-place">{esc(c['place'])}</p>{detail}</div>''')
    return ''.join(rows)

def talks(lang, full=False):
    t = DATA['languages'][lang]
    rows = []
    for item in DATA['talks'] + (DATA.get('talks_extra',[]) if full else []):
        c = item[lang]
        link = f'<a href="{esc(item["url"])}">{esc(t["event_link"])}</a>' if item.get('url') else ''
        # An English title retained in a Turkish page keeps its language annotation.
        title_lang = 'en' if lang=='tr' and c['title']==item['en']['title'] else lang
        rows.append(f'''<li class="talk"><time datetime="{esc(item['date'])}">{esc(c['date'])}</time><div><h3 lang="{title_lang}">{esc(c['title'])}</h3><p>{esc(c['event'])}</p>{link}</div></li>''')
    return '<ul class="talk-list">' + ''.join(rows) + '</ul>'

def footer(lang):
    t = DATA['languages'][lang]
    return f'<footer class="page-footer"><p>© 2026 {esc(DATA["name"])}<br>{esc(t["updated_label"])}</p><a href="#top">{esc(t["top"])}</a></footer>'

def section_head(lang, key, extra=''):
    return f'<div class="section-head"><h2>{esc(DATA["languages"][lang][key])}</h2>{extra}</div>'

def home_page(lang):
    t = DATA['languages'][lang]
    prefix = '' if lang=='en' else '../'
    cv = prefix + 'cv/' + ('index.html' if lang=='en' else 'tr.html')
    pdf = prefix + 'assets/Omer-Akyildiz-CV-' + lang.upper() + '.pdf'
    bio = ''.join('<p>' + esc(p) + '</p>' for p in t['bio'])
    interests = ''.join('<li>' + esc(p) + '</li>' for p in t['interests'])
    service = ''.join('<p>' + esc(p) + '</p>' for p in t['service_text'])
    scholar = DATA['scholar'].replace('hl=en','hl='+lang)
    return head(lang,prefix) + f'''
<body id="top">
{rail(lang,prefix)}
<main id="main">
  <section class="intro" id="about" aria-labelledby="name">
    <div class="intro-copy">
      <h1 id="name"><span>Ömer</span> <span>Akyıldız</span></h1>
      <p class="intro-role">{esc(t['role'])}</p>
      <div class="intro-text">{bio}</div>
      <div class="intro-links"><a href="{cv}">{esc(t['cv_view'])}</a><a href="{esc(scholar)}">Google Scholar</a><a href="#contact">{esc(t['contact'])}</a></div>
    </div>
    <figure class="portrait"><img src="{prefix}assets/omer-akyildiz.jpg" alt="{esc(t['portrait_alt'])}" width="3180" height="2300" fetchpriority="high"><figcaption>{esc(t['portrait_caption'])}</figcaption></figure>
  </section>
  <div class="interests"><h2>{esc(t['interest_label'])}</h2><ul class="interest-list">{interests}</ul></div>
  <section class="section" id="research" aria-label="{esc(t['research'])}">
    {section_head(lang,'research',f'<a href="{esc(scholar)}">Google Scholar</a>')}
    <h3 class="research-subtitle">{esc(t['articles'])}</h3>
    {publications(DATA['articles'],lang)}
    {manuscripts(lang)}
    <details class="other-writing"><summary>{esc(t['other'])}</summary>{publications(DATA['chapters'],lang,True)}</details>
  </section>
  <section class="section" id="background" aria-label="{esc(t['background'])}">
    {section_head(lang,'background',f'<a href="{pdf}" download>{esc(t["cv_download"])}</a>')}
    <div class="background-grid"><div><h3 class="subheading">{esc(t['appointments'])}</h3>{career(DATA['appointments'],lang)}</div><div><h3 class="subheading">{esc(t['education'])}</h3>{career(DATA['education'],lang)}</div></div>
  </section>
  <section class="section" id="talks" aria-label="{esc(t['talks'])}">
    {section_head(lang,'talks')}
    <p class="section-intro">{esc(t['talks_note'])}</p>
    {talks(lang)}
    <div class="service"><h3 class="subheading">{esc(t['service'])}</h3>{service}</div>
  </section>
  <section class="section contact-section" id="contact" aria-label="{esc(t['contact'])}">
    {section_head(lang,'contact')}
    <div class="contact-body"><div><p>{esc(t['contact_text'])}</p><div class="email-line"><a class="email-address" href="mailto:{esc(DATA['email'])}">{esc(DATA['email'])}</a><button type="button" class="copy-email" hidden data-copy-email="{esc(DATA['email'])}" data-success="{esc(t['copied'])}" data-failure="{esc(t['copy_failed'])}">{esc(t['copy'])}</button></div><span class="copy-feedback" role="status" aria-live="polite"></span></div>{profiles(lang,'contact-profiles')}</div>
  </section>
  {footer(lang)}
</main>
</body>
</html>
'''

def cv_page(lang):
    t = DATA['languages'][lang]
    home = '../index.html' if lang=='en' else '../tr/index.html'
    other = 'tr.html' if lang=='en' else 'index.html'
    interests = ''.join('<li>'+esc(p)+'</li>' for p in t['interests'])
    service = ''.join('<p>'+esc(p)+'</p>' for p in t['service_text'])
    awards = ''.join('<p>'+esc(p)+'</p>' for p in t['award_text'])
    return head(lang,'../',True) + f'''
<body id="top"><main class="cv-page" id="main">
  <div class="cv-toolbar"><a href="{home}">{esc(t['back'])}</a><a href="{other}" hreflang="{'tr' if lang=='en' else 'en'}" lang="{'tr' if lang=='en' else 'en'}">{'Türkçe' if lang=='en' else 'English'}</a><button type="button" hidden data-print>{esc(t['print'])}</button></div>
  <h1>{esc(DATA['full_name'])}</h1><p class="cv-role">{esc(t['role'])}</p>
  <p class="cv-contact"><a href="mailto:{esc(DATA['email'])}">{esc(DATA['email'])}</a><br><a href="{esc(DATA['scholar'])}">Google Scholar</a> · <a href="{esc(DATA['orcid'])}">ORCID: 0000-0002-2280-3002</a></p>
  <h2>{esc(t['interest_label'])}</h2><ul class="interest-list">{interests}</ul>
  <h2>{esc(t['appointments'])}</h2>{career(DATA['appointments'],lang,True)}
  <h2>{esc(t['education'])}</h2>{career(DATA['education'],lang,True)}
  <h2>{esc(t['articles'])}</h2>{publications(DATA['articles'],lang)}
  {manuscripts(lang,True)}
  <h2>{esc(t['other'])}</h2>{publications(DATA['chapters'],lang,True)}
  <h2>{esc(t['talks'])}</h2>{talks(lang,True)}
  <div class="service"><h2>{esc(t['service'])}</h2>{service}</div>
  <div class="service"><h2>{esc(t['awards'])}</h2>{awards}</div>
  {footer(lang)}
</main></body></html>'''

for filename, markup in [('index.html',home_page('en')),('tr/index.html',home_page('tr')),('cv/index.html',cv_page('en')),('cv/tr.html',cv_page('tr'))]:
    path = OUT / filename
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(markup,encoding='utf-8')
    print(f'Wrote {path}')

# Discovery files use the same durable domain setting as page metadata.
sitemap_urls = ['/', '/tr/', '/cv/', '/cv/tr.html']
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for route in sitemap_urls:
    sitemap += f'  <url><loc>{BASE_URL}{route}</loc></url>\n'
sitemap += '</urlset>\n'
(OUT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n', encoding='utf-8')
