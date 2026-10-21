# Website maintenance

This is Ömer Akyıldız’s static English/Turkish academic website.

## Publishing configuration
- Repository: https://github.com/homerakyildiz-svg/homerakyildiz-svg.github.io (public).
- Branch: main; GitHub Pages publishing source: Deploy from a branch, /(root).
- Canonical domain: https://omer-akyildiz.com/; English /, Turkish /tr/. Domain ownership verified and repository bound.
- GitHub Pages diagnostic URL: https://homerakyildiz-svg.github.io/ (redirects to the custom domain).
- Cloudflare DNS: four GitHub Pages apex A records (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153), www CNAME to homerakyildiz-svg.github.io; all DNS only, TTL 300. Retain the account verification TXT.
- Nameservers: denver.ns.cloudflare.com and rosalyn.ns.cloudflare.com. No migration needed. Check HTTPS/redirect status live when maintaining the site.

## Sources and commands
- Academic content and translations: source/content.json.
- HTML templates and BASE_URL domain metadata: source/build.py. It also generates sitemap.xml and robots.txt.
- Styling: assets/style.css. Behaviour: assets/site.js.
- PDF CV generation: source/build_cv.py, using ReportLab and bundled fonts.
- Build with python3 source/build.py; validate with python3 source/check_site.py and python3 source/check_metadata.py.
- Rebuild both PDF CVs after content changes with python3 source/build_cv.py. Do not edit only generated HTML.
- Preview with python3 -m http.server 8000, then inspect /, /tr/, /cv/, and /cv/tr.html at desktop, tablet, and narrow mobile widths. Check menu, keyboard access, language switching, portrait, no horizontal scrolling, and PDF downloads.

## Content and publication controls
Preserve the design and supplied academic content. Keep three journal articles separate from manuscripts and presentations. Preserve Abdülhamit Kırmızı’s coauthorship. Do not call the 2025–2026 UConn appointment current without owner confirmation. Never add the private CV, home address, telephone, secrets, setup prompt, screenshots, or account exports.

Inspect Git status, diff, remote, branch, and existing remote work before changes. Prepare updates and preview first; obtain owner approval of the exact publication batch before commits/pushes or account/DNS changes. Reuse approvals within scope. Never force-push or discard unrelated work.

Keep .nojekyll, font licenses, and public PDFs. CNAME contains omer-akyildiz.com; preserve it. Domain verification and initial domain setup were approved and completed. Keep GitHub verification TXT and existing DNS records. Ordinary content updates require no DNS changes.

After approval, commit and push the reviewed update, verify Pages deployment and both language URLs, HTTPS and www redirect. Revert a bad release with a reviewed normal git revert, never a force-push.
