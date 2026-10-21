> Repository: https://github.com/homerakyildiz-svg/homerakyildiz-svg.github.io. Publishes from main → /(root) using GitHub Pages. Canonical domain: https://omer-akyildiz.com/. See UPDATE-GUIDE.md for maintenance.

# Ömer Akyıldız academic website

Complete English and Turkish static website, prepared 21 October 2026.

The files are ready to upload. No npm, build service, database, API key or server code is required. Fonts, portrait and public CV PDFs are included locally. The original CV, private address and telephone number are not included.

## Publish on GitHub Pages

1. Extract the ZIP on your computer. Upload the **extracted contents**, not the ZIP itself.
2. In your own GitHub account, create or open the repository for the website. For a personal homepage, name it `YOUR-USERNAME.github.io`, using your actual GitHub username. On GitHub Free, use a public repository.
3. Choose **Add file → Upload files** and upload the files and folders. `index.html`, `assets`, `tr` and `cv` must sit at the repository's top level, rather than inside an extra website folder. Include `source` and this README if you want the editable source in the repository.
4. Include the empty `.nojekyll` file. Finder hides dotfiles; press **Command–Shift–.** to show them. You can also create `.nojekyll` using GitHub's **Add file → Create new file**.
5. Save the uploaded files with **Commit changes**. Open **Settings → Pages**. Under **Build and deployment**, select **Deploy from a branch**, choose **main** and **/(root)**, then **Save**.
6. When GitHub reports that publication has finished, choose **Visit site** on the Pages settings screen. The English homepage is the default; the Turkish page is under `/tr/`.

The same files also work in a project repository such as `academic-website`, under `https://YOUR-USERNAME.github.io/academic-website/`. All site links and assets use relative paths. Navigation and assets remain relative. Canonical and language metadata use https://omer-akyildiz.com in source/build.py.

These steps follow [GitHub's site creation guide](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) and [publishing-source guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), checked 21 October 2026.

## Preview locally

Open `index.html` in your browser. For a local web preview, open a terminal in the extracted folder and run:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000`. Stop the preview with Ctrl+C. Python is only needed for this optional local preview and the optional editing tools; the published site runs as static HTML.

## Edit the website

- `index.html`: English homepage.
- `tr/index.html`: Turkish homepage.
- `cv/index.html` and `cv/tr.html`: printable public CVs.
- `assets/style.css`: colours, type and responsive layout.
- `assets/site.js`: mobile navigation, language-link section retention, copy-email and print controls.
- `assets/omer-akyildiz.jpg`: supplied portrait, unchanged. Replace it and update its dimensions in `source/build.py` if necessary.
- `assets/Omer-Akyildiz-CV-EN.pdf` and `assets/Omer-Akyildiz-CV-TR.pdf`: public CV downloads.
- `source/content.json`: shared academic content and both sets of translated labels.

To keep all four pages consistent, edit `source/content.json`, then run:

```sh
python3 source/build.py
python3 source/check_site.py
```

This uses Python's standard library. It rewrites the four HTML pages, so do not combine direct HTML edits with source generation unless you also transfer those edits to `source/build.py`.

After changing the academic content, update both PDF CVs as well. Print the corresponding CV webpage using **Print / save as PDF**, then replace the PDF file in `assets` with that filename. Alternatively, the included `source/build_cv.py` recreates the typeset PDFs if Python's `reportlab` package is installed:

```sh
python3 source/build_cv.py
```

Fonts are licensed under the SIL Open Font License; their notices are in `assets/fonts`. Publication links lead to journal or publisher pages; no journal PDFs or research datasets are bundled. The website has no analytics, tracking cookies or remote font dependencies.

## GitHub Pages ile yayınlama

1. ZIP dosyasını bilgisayarınızda açın. GitHub'a ZIP dosyasını değil, **içindeki dosya ve klasörleri** yükleyin.
2. Kendi GitHub hesabınızda kişisel ana sayfa için `KULLANICI-ADINIZ.github.io` adlı bir depo oluşturun veya mevcut deponuzu açın. Gerçek GitHub kullanıcı adınızı yazın. GitHub Free kullanıyorsanız depo herkese açık olmalıdır.
3. **Add file → Upload files** yoluyla dosyaları yükleyin. `index.html`, `assets`, `tr` ve `cv` deponun ana dizininde bulunmalıdır. Üstte fazladan bir site klasörü olmamalıdır. Düzenlenebilir kaynakları saklamak için `source` klasörünü ve bu dosyayı da yükleyebilirsiniz.
4. Boş `.nojekyll` dosyasını ekleyin. Mac'te gizli dosyaları görmek için **Command–Shift–.** tuşlarına basın. Bu dosyayı GitHub'da **Add file → Create new file** yoluyla da oluşturabilirsiniz.
5. **Commit changes** ile kaydedin. **Settings → Pages → Build and deployment** bölümünde **Deploy from a branch**, **main** ve **/(root)** seçeneklerini seçip **Save** düğmesine basın.
6. Yayınlama tamamlandığında Pages ayarları ekranındaki **Visit site** bağlantısını kullanın. Varsayılan sayfa İngilizcedir; Türkçe sürüm `/tr/` adresindedir. Dil menüsüyle geçiş yapılabilir.

Aynı paket, farklı adlandırılmış bir proje deposunda da çalışır. Örneğin `academic-website` deposu kullanılırsa site `https://KULLANICI-ADINIZ.github.io/academic-website/` altında açılır. Dosya yollarını değiştirmeniz gerekmez.

## İçeriği güncelleme

Akademik bilgiler ve çeviriler `source/content.json` dosyasında bulunur. Bu dosyayı düzenledikten sonra paketin ana klasöründe `python3 source/build.py` ve ardından `python3 source/check_site.py` komutlarını çalıştırın. Dört HTML sayfası birlikte güncellenir. Kodlama aracı veya paket kurulumu gerekmez.

Özgeçmişteki değişikliklerden sonra PDF dosyalarını da yenileyin. İlgili özgeçmiş sayfasındaki **Yazdır / PDF olarak kaydet** düğmesini kullanıp PDF'yi `assets` klasöründe aynı dosya adıyla kaydedebilirsiniz. `reportlab` kuruluysa `python3 source/build_cv.py` komutu da iki PDF'yi yeniden oluşturur.

İletişim bölümünde akademik e-posta adresi kullanılmıştır. Özgün CV'deki ev adresi ve telefon numarası pakete eklenmemiştir.
