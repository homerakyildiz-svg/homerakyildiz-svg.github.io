# Updating your website

Repository: https://github.com/homerakyildiz-svg/homerakyildiz-svg.github.io, branch main, GitHub Pages from /(root).
English address: https://omer-akyildiz.com/; Turkish: https://omer-akyildiz.com/tr/.

1. Ask Codex to open this dedicated website repository and inspect the current Git state.
2. Change academic text in source/content.json; templates and domain metadata in source/build.py; styling in assets/style.css; interaction in assets/site.js.
3. Run `python3 source/build.py`, `python3 source/check_site.py`, and `python3 source/check_metadata.py`.
4. For CV changes, run `python3 source/build_cv.py` in an environment with ReportLab, and review both PDFs. Private address and telephone must remain omitted.
5. Preview with `python3 -m http.server 8000`. Inspect both languages and CV pages, desktop/tablet/mobile layout, menu, keyboard navigation, language switching, links, portrait, and PDF downloads.
6. Review the diff and publication batch. Approve the exact commit/push before Codex publishes.
7. Verify the Pages deployment and live English/Turkish pages after publication; verify HTTPS and www redirection during initial setup.

Keep .nojekyll, font licenses, public PDFs, CNAME and GitHub verification TXT. Normal content updates do not need DNS or hosting recreation.
For rollback, review `git log`, run `git revert <bad-commit>` and approve/push the revert. Never force-push.

## Türkçe kısa rehber

İçerik ve çeviriler: source/content.json. Sayfa şablonları ve alan adı: source/build.py. Tasarım: assets/style.css. Etkileşim: assets/site.js.
Değişiklikten sonra yukarıdaki derleme ve kontrol komutlarını çalıştırın; özgeçmiş değiştiyse iki PDF’yi de yenileyin. İngilizce/Türkçe sayfaları ve mobil görünümü inceleyin. Yayımlamadan önce değişiklikleri onaylayın. Olağan içerik güncellemelerinde DNS değişmez. Geri alma işlemi normal git revert ile yapılır.
