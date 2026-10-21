#!/usr/bin/env python3
"""Build the two public academic CVs from content.json (requires reportlab).

Run in the authoring folder or in the unzipped handover folder:
    python3 source/build_cv.py
The script supports both site/assets/ (development) and assets/ (handover).
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "site" / "assets" if (ROOT / "site" / "assets").is_dir() else ROOT / "assets"
DATA = json.loads((ROOT / "source" / "content.json").read_text(encoding="utf-8"))
INK = colors.HexColor("#27232c")
MUTED = colors.HexColor("#69616e")
ACCENT = colors.HexColor("#513d58")
RULE = colors.HexColor("#ded8e2")
WIDTH, HEIGHT = A4
MARGIN = 49
BODY_WIDTH = WIDTH - 2 * MARGIN

for name, filename in [
    ("CVSans", "source-sans-regular.ttf"),
    ("CVSansBold", "source-sans-semibold.ttf"),
    ("CVSerif", "literata-regular.ttf"),
    ("CVSerifBold", "literata-medium.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, str(ASSETS / "fonts" / filename)))
pdfmetrics.registerFontFamily("CVSans", normal="CVSans", bold="CVSansBold")
pdfmetrics.registerFontFamily("CVSerif", normal="CVSerif", bold="CVSerifBold")


def e(text):
    # Plain hyphens keep PDF extraction consistent across viewers.
    return escape(str(text).replace("–", "-").replace("—", "-"))


def link(label, url):
    return '<link href="%s" color="#513d58">%s</link>' % (escape(url, {'"': '&quot;'}), e(label))


STYLES = {
    "name": ParagraphStyle("name", fontName="CVSerif", fontSize=25, leading=32, textColor=INK, spaceAfter=5),
    "role": ParagraphStyle("role", fontName="CVSans", fontSize=11.2, leading=15, textColor=ACCENT, spaceAfter=9),
    "contacts": ParagraphStyle("contacts", fontName="CVSans", fontSize=9.3, leading=14, textColor=MUTED, spaceAfter=10),
    "body": ParagraphStyle("body", fontName="CVSans", fontSize=10.2, leading=14.3, textColor=INK, spaceAfter=7),
    "section": ParagraphStyle("section", fontName="CVSansBold", fontSize=11.7, leading=15, textColor=ACCENT, spaceBefore=16, spaceAfter=9, keepWithNext=True),
    "page_title": ParagraphStyle("page_title", fontName="CVSerif", fontSize=21, leading=28, textColor=INK, spaceAfter=3),
    "page_deck": ParagraphStyle("page_deck", fontName="CVSans", fontSize=9.4, leading=13, textColor=MUTED, spaceAfter=3),
    "entry": ParagraphStyle("entry", fontName="CVSans", fontSize=10.2, leading=13.9, textColor=INK, spaceAfter=2),
    "detail": ParagraphStyle("detail", fontName="CVSans", fontSize=9.6, leading=13.2, textColor=MUTED, spaceAfter=3),
    "small": ParagraphStyle("small", fontName="CVSans", fontSize=8.9, leading=12, textColor=MUTED, spaceAfter=0),
    "date": ParagraphStyle("date", fontName="CVSans", fontSize=9.7, leading=13.9, textColor=MUTED),
    "citation": ParagraphStyle("citation", fontName="CVSans", fontSize=10, leading=13.8, textColor=INK, spaceAfter=3),
}


def p(text, style="body"):
    return Paragraph(text, STYLES[style])


def heading(text):
    return p(e(text), "section")


def dated_entry(dates, title, place, detail=None):
    text = "<b>" + e(title) + "</b><br/>" + e(place)
    if detail:
        text += '<br/><font color="#69616e">' + e(detail) + '</font>'
    table = Table([[p(e(dates), "date"), p(text, "entry")]], colWidths=[77, BODY_WIDTH - 77], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 10),
        ("RIGHTPADDING", (1, 0), (1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def publication(item):
    body = "%s (%s). <b>%s.</b> %s." % (
        e(item["authors"]), e(item["year"]), e(item["title"].rstrip(".")), e(item["venue"].rstrip("."))
    )
    entries = [p(body, "citation")]
    if item.get("doi"):
        entries.append(p(link(item["doi"].replace("https://doi.org/", "doi: "), item["doi"]), "small"))
    elif item.get("url"):
        entries.append(p(link("Publisher’s edition" if LANG == "en" else "Yayınevinin dijital nüshası", item["url"]), "small"))
    entries.append(Spacer(1, 10))
    return KeepTogether(entries)


class CVDocument(BaseDocTemplate):
    def __init__(self, path, lang):
        self.cv_lang = lang
        super().__init__(str(path), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=44, bottomMargin=48, title=DATA["full_name"] + " - " + ("Curriculum vitae" if lang == "en" else "Özgeçmiş"),
                         author=DATA["full_name"], subject="Public academic CV" if lang == "en" else "Akademik özgeçmiş")
        frame = Frame(MARGIN, 48, BODY_WIDTH, HEIGHT - 92, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id="cv", frames=frame, onPage=self.decorate))

    def decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 38, WIDTH - MARGIN, 38)
        canvas.setFont("CVSans", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN, 25, DATA["full_name"])
        updated = "October 2026" if self.cv_lang == "en" else "Ekim 2026"
        canvas.drawRightString(WIDTH - MARGIN, 25, "%s   /   %d" % (updated, doc.page))
        canvas.restoreState()


def build(lang):
    global LANG
    LANG = lang
    ui = DATA["languages"][lang]
    path = ASSETS / ("Omer-Akyildiz-CV-%s.pdf" % lang.upper())
    out = [p(e(DATA["full_name"]), "name"), p(e(ui["role"]), "role")]
    contacts = link(DATA["email"], "mailto:" + DATA["email"]) + "<br/>"
    contacts += link("Google Scholar", DATA["scholar"]) + " &nbsp; / &nbsp; " + link("ORCID 0000-0002-2280-3002", DATA["orcid"])
    out += [p(contacts, "contacts")]
    for bio in ui["bio"]:
        out.append(p(e(bio)))
    out += [heading(ui["interest_label"]), p(" · ".join(e(i) for i in ui["interests"]))]
    out.append(heading(ui["appointments"]))
    for item in DATA["appointments"]:
        out.append(dated_entry(item["dates"], item[lang]["title"], item[lang]["place"]))
    out.append(heading(ui["education"]))
    for item in DATA["education"]:
        out.append(dated_entry(item["dates"], item[lang]["title"], item[lang]["place"], item[lang].get("detail")))
    out.append(heading(ui["awards"]))
    for item in ui["award_text"]:
        out.append(p(e(item), "detail"))

    out += [PageBreak(), p(e(ui["research"]), "page_title")]
    out.append(heading(ui["articles"]))
    for item in DATA["articles"]:
        out.append(publication(item))
    out.append(heading(ui["manuscripts"]))
    for item in DATA["manuscripts"]:
        title = item["title"]
        if not title.endswith((".", "?", "!")):
            title += "."
        out.append(KeepTogether([
            p("<b>" + e(title) + "</b>", "entry"),
            p(e(ui[item["status"]]), "detail"), Spacer(1, 7),
        ]))
    out.append(heading(ui["other"]))
    for item in DATA["chapters"]:
        out.append(publication(item))

    out += [PageBreak(), p(e(ui["talks"]), "page_title"), Spacer(1, 16)]
    for item in DATA["talks"] + DATA["talks_extra"]:
        t = item[lang]
        entries = [p(e(t["date"]), "small"), p("<b>" + e(t["title"].rstrip(".")) + ".</b>", "entry"), p(e(t["event"]), "detail")]
        if item.get("url"):
            entries.append(p(link(ui["event_link"], item["url"]), "small"))
        entries.append(Spacer(1, 12))
        out.append(KeepTogether(entries))
    out.append(heading(ui["service"]))
    for item in ui["service_text"]:
        out.append(p(e(item), "body"))
    CVDocument(path, lang).build(out)
    return path


if __name__ == "__main__":
    for language in ("en", "tr"):
        print(build(language))
