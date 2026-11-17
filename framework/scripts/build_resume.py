#!/usr/bin/env python3
"""Generic resume renderer: layout only, all content from a YAML file.

Renders one docx per lane defined in the content file. Changing positioning
strategy (bullet order, lane inclusion, title/summary wording) is a content
edit, not a code change. Layout matches the recruiter-coached ATS-safe
format: Tahoma, green 12pt section headers with rule, right-tab dates,
justified 10pt bullets, footer for page-two continuity.

Optional content features (all off unless the content file uses them):
  - identity.phone / email / linkedin / linkedin_url render as live links;
    identity.contact_line is the plain-text fallback.
  - a bullet or community item may be {text, link_text, url}: the link_text
    substring becomes a hyperlink.
  - lane `summary` and `competencies` may be omitted.
  - lane `dormant: true` skips the lane unless it is named on the command line.
  - lane `format: text` writes a plain-text paste export (see write_text_export);
    `inherit: <lane>` borrows that lane's bullet orders.
  - SITE HOOK: if `site_extension.py` sits beside this script and defines
    `write_site(content, lane_key, content_path)`, it is called once per lane
    after the normal outputs and may return the Path it wrote (or None). Use
    it for any instance-specific output (a website, a static-site page) so
    this file can stay identical across instances. A lane whose `format` is
    anything other than docx/text is produced only by the hook.

Usage:
  python3 build_resume.py                    # all lanes, content file beside script
  python3 build_resume.py ic                 # one lane
  python3 build_resume.py path/to/content.yml pc

Output files land next to the content file, named by each lane's `output`.
Every build also updates `build_record.yml` beside the content file — per
lane: build timestamp, output name, and a hash of the content file — so
"is any platform-stored copy older than the last build" is a mechanical
compare, not an act of memory.
"""
import hashlib
import importlib.util
import sys
from datetime import datetime
from pathlib import Path

import yaml
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

GREEN = RGBColor(0x00, 0x66, 0x00)
GRAY = RGBColor(0x66, 0x66, 0x66)
FONT = "Tahoma"
MARGIN = Inches(1.0)   # page margin, all four sides; the right tab stop derives from it
BODY = 10


class Builder:
    def __init__(self, content):
        self.c = content
        self.doc = Document()
        sec = self.doc.sections[0]
        sec.page_width = Inches(8.5); sec.page_height = Inches(11)
        sec.top_margin = MARGIN; sec.bottom_margin = MARGIN
        sec.left_margin = MARGIN; sec.right_margin = MARGIN
        # right-aligned tab stop = usable text width. Derived, never hardcoded:
        # a fixed value silently lands outside the text area when margins change.
        self.right_tab = sec.page_width - sec.left_margin - sec.right_margin
        normal = self.doc.styles["Normal"]
        normal.font.name = FONT; normal.font.size = Pt(BODY)
        normal.paragraph_format.space_after = Pt(3)
        normal.paragraph_format.line_spacing = 1.05
        ftr = sec.footer; ftr.is_linked_to_previous = False
        fp = ftr.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fr = fp.add_run(content["identity"]["footer"])
        fr.font.name = FONT; fr.font.size = Pt(8); fr.font.color.rgb = GRAY

    def runp(self, p, text, *, bold=False, size=BODY, color=None, italic=False):
        r = p.add_run(text)
        r.font.name = FONT; r.font.size = Pt(size); r.bold = bold; r.italic = italic
        if color is not None:
            r.font.color.rgb = color
        return r

    def link(self, p, url, text, *, size=BODY, color=None, bold=False, underline=False):
        """Append an external hyperlink run. python-docx has no native support, so
        this builds the w:hyperlink element and its relationship by hand."""
        r_id = p.part.relate_to(url, RT.HYPERLINK, is_external=True)
        h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), r_id)
        r = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
        f = OxmlElement("w:rFonts")
        f.set(qn("w:ascii"), FONT); f.set(qn("w:hAnsi"), FONT); rPr.append(f)
        sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(size * 2))); rPr.append(sz)
        if bold: rPr.append(OxmlElement("w:b"))
        if color is not None:
            col = OxmlElement("w:color"); col.set(qn("w:val"), str(color)); rPr.append(col)
        if underline:
            u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
        r.append(rPr)
        t = OxmlElement("w:t"); t.text = text
        t.set(qn("xml:space"), "preserve"); r.append(t)
        h.append(r); p._p.append(h)

    def para(self, space_after=3, space_before=0):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        return p

    def heading(self, text):
        p = self.para(space_before=8, space_after=3)
        self.runp(p, text, bold=True, size=12, color=GREEN)
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement("w:pBdr"); bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "2"); bottom.set(qn("w:color"), "006600")
        pbdr.append(bottom); pPr.append(pbdr)

    def dateline(self, left_text, right_text):
        p = self.para(space_before=6, space_after=1)
        p.paragraph_format.tab_stops.add_tab_stop(self.right_tab, WD_TAB_ALIGNMENT.RIGHT)
        self.runp(p, left_text, bold=True, size=BODY)
        self.runp(p, "\t" + right_text, bold=False, size=9)

    def bullet(self, item):
        """item is a plain string, or a dict {text, link_text, url} where the
        link_text substring of text becomes a live hyperlink."""
        p = self.doc.add_paragraph(style="List Bullet")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.0
        if isinstance(item, str):
            run = p.add_run(item); run.font.name = FONT; run.font.size = Pt(BODY)
            return
        text, lt, url = item["text"], item.get("link_text"), item.get("url")
        if not (lt and url and lt in text):
            run = p.add_run(text); run.font.name = FONT; run.font.size = Pt(BODY)
            return
        before, after = text.split(lt, 1)
        if before: self.runp(p, before, size=BODY)
        self.link(p, url, lt, size=BODY, color=GREEN)
        if after: self.runp(p, after, size=BODY)

    def build(self, lane_key, out_dir):
        c, lane = self.c, self.c["lanes"][lane_key]
        ident = c["identity"]
        p = self.para(space_after=6)
        p.paragraph_format.tab_stops.add_tab_stop(self.right_tab, WD_TAB_ALIGNMENT.RIGHT)
        self.runp(p, ident["name"], bold=True, size=19, color=GREEN)
        if ident.get("contact_line") and not ident.get("email"):
            # plain-text fallback: contact_line on its own line, no links
            p.paragraph_format.space_after = Pt(1)
            p = self.para(space_after=6)
            self.runp(p, ident["contact_line"], size=9.5)
        else:
            self.runp(p, "\t", size=9.5)
            sep = "  \u00b7  "
            parts = []
            if ident.get("phone"):
                raw = ident["phone"].strip()
                digits = "".join(ch for ch in raw if ch.isdigit())
                # a number written with a leading + keeps its own country code;
                # otherwise assume a 10-digit North American number
                tel = "tel:+" + digits if raw.startswith("+") else "tel:+1" + digits
                parts.append((tel, ident["phone"]))
            if ident.get("email"):
                parts.append(("mailto:" + ident["email"], ident["email"]))
            if ident.get("linkedin") and ident.get("linkedin_url"):
                parts.append((ident["linkedin_url"], ident["linkedin"]))
            for i, (url, label) in enumerate(parts):
                if i:
                    self.runp(p, sep, size=9.5)
                self.link(p, url, label, size=9.5, color=GREEN)

        p = self.para(space_after=1)
        self.runp(p, lane["title_line"], bold=True, size=12, color=GREEN)
        p = self.para(space_after=5)
        self.runp(p, lane["tagline"], bold=True, size=10)
        if lane.get("summary"):
            p = self.para(space_after=2)
            self.runp(p, lane["summary"], size=BODY)

        if lane.get("competencies"):
            self.heading("Core Competencies")
            p = self.para(space_after=3)
            self.runp(p, lane["competencies"], bold=True, size=10)

        self.heading("Technical Skills")
        for group in c["skills"]:
            # Render names only: "item (child, child), item, ...".
            # years / depth / note / canonical are internal ledger metadata,
            # dropped here; context_ledger is never rendered.
            parts = []
            for item in group["items"]:
                s = item["name"]
                kids = item.get("children")
                if kids:
                    s += " (" + ", ".join(k["name"] for k in kids) + ")"
                parts.append(s)
            p = self.para(space_after=2)
            p.paragraph_format.line_spacing = 1.05
            self.runp(p, group["group"] + ": ", bold=True, size=BODY)
            self.runp(p, ", ".join(parts), size=BODY)

        self.heading("Professional Experience")
        for emp in c["employers"]:
            self.dateline(emp["heading"], emp["dates"])
            p = self.para(space_after=2)
            scope = (emp.get("scope") or {}).get(lane_key)
            if scope:
                self.runp(p, emp["title"] + " ", bold=True, size=BODY)
                self.runp(p, scope, size=BODY, italic=True)
            else:
                self.runp(p, emp["title"], bold=True, size=BODY)
            context = (emp.get("context") or {}).get(lane_key)
            if context:
                p = self.para(space_after=2)
                self.runp(p, context, size=BODY, italic=True)
            order = lane.get("orders", {}).get(emp["key"]) or emp["order"]
            for key in order:
                self.bullet(emp["bullets"][key])

        self.heading("Community & Talks")
        for item in c["community"]:
            self.bullet(item)

        self.heading("Education")
        p = self.para(space_after=1)
        self.runp(p, c["education"], size=BODY)

        out = out_dir / lane["output"]
        self.doc.save(out)
        return out


LINKEDIN_LIMIT = 2000   # LinkedIn's per-role description cap

def lane_orders(content, lane):
    """A lane's bullet orders, or the orders of the lane it inherits from.
    `inherit` exists so a paste-export cannot drift from the surface it is
    meant to mirror — change one bullet set, both follow."""
    if lane.get("orders"):
        return lane["orders"]
    parent = lane.get("inherit")
    return content["lanes"][parent].get("orders", {}) if parent else {}


def plain(item):
    """The plain text of a bullet: a string, or the `text` of a {text, ...} dict."""
    return item if isinstance(item, str) else item["text"]


def write_text_export(content, lane_key, content_path):
    """Plain-text experience section for pasting into LinkedIn, application
    forms, and anywhere else that wants bullets without markup. Dash bullets,
    no wrapping, one block per employer."""
    c, lane = content, content["lanes"][lane_key]
    orders = lane_orders(c, lane)
    ref = lane.get("inherit") or lane_key
    out = []
    for emp in c["employers"]:
        company = emp["heading"].split(",")[0].title()
        out += [f"{company} - {emp['title']}", emp["dates"], ""]
        ctx = (emp.get("context") or {}).get(ref) or (emp.get("context") or {}).get("ic")
        if ctx:
            out += [ctx, ""]
        for key in orders.get(emp["key"]) or emp["order"]:
            out.append(f"- {plain(emp['bullets'][key])}")
        out.append("")
    target = content_path.parent / lane["output"]
    target.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")

    # LinkedIn caps a single role description at 2000 characters, and it is the
    # one surface that cannot be generated — so the ceiling has to be visible
    # here or it is discovered by pasting.
    for emp in c["employers"]:
        keys = orders.get(emp["key"]) or emp["order"]
        n = sum(len(plain(emp["bullets"][k])) + 3 for k in keys)
        company = emp["heading"].split(",")[0].title()
        flag = "" if n <= LINKEDIN_LIMIT else f"  <-- OVER by {n - LINKEDIN_LIMIT}"
        print(f"  {company[:34]:<34} {len(keys):>2} bullets  {n:>5}/{LINKEDIN_LIMIT} chars{flag}")
    return target


def load_site_hook():
    """Return write_site from site_extension.py beside this script, or None.
    The file is optional; absent means the builder does nothing extra."""
    path = Path(__file__).resolve().parent / "site_extension.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("site_extension", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "write_site", None)


def write_build_record(content_path, built):
    """Update build_record.yml beside the content file. `built` maps lane
    key -> output Path for the lanes rendered in this run; lanes not
    rebuilt keep their previous record entry."""
    record_path = content_path.parent / "build_record.yml"
    record = {}
    if record_path.exists():
        record = yaml.safe_load(record_path.read_text(encoding="utf-8")) or {}
    content_hash = hashlib.sha256(content_path.read_bytes()).hexdigest()[:16]
    for lane_key, out in built.items():
        record[lane_key] = {
            "built": datetime.now().isoformat(timespec="seconds"),
            "output": out.name,
            "content_sha256_16": content_hash,
        }
    record_path.write_text(yaml.safe_dump(record, sort_keys=False),
                           encoding="utf-8")
    return record_path


def main():
    args = sys.argv[1:]
    content_path = Path(__file__).resolve().parent / "resume_content.yml"
    lanes = None
    for a in args:
        if a.endswith((".yml", ".yaml")):
            content_path = Path(a).resolve()
        else:
            lanes = [a]
    with open(content_path, encoding="utf-8") as f:
        content = yaml.safe_load(f)
    built = {}
    site_hook = load_site_hook()
    default_lanes = [k for k, v in content["lanes"].items() if not v.get("dormant")]
    for lane_key in lanes or default_lanes:
        if lane_key not in content["lanes"]:
            sys.exit(f"Unknown lane '{lane_key}'. "
                     f"Available: {', '.join(content['lanes'])}")
        fmt = content["lanes"][lane_key].get("format")
        out = None
        if fmt == "text":
            out = write_text_export(content, lane_key, content_path)
        elif fmt in (None, "docx"):
            out = Builder(content).build(lane_key, content_path.parent)
        if out:
            built[lane_key] = out
            print("SAVED", out)
        if site_hook:
            site_out = site_hook(content, lane_key, content_path)
            if site_out:
                built.setdefault(lane_key, site_out)
                print("SAVED", site_out)
        elif out is None:
            print(f"SKIPPED lane '{lane_key}': format '{fmt}' needs a site_extension.py")
    prior = set()
    record_path = content_path.parent / "build_record.yml"
    if record_path.exists():
        prev = yaml.safe_load(record_path.read_text(encoding="utf-8")) or {}
        prior = {v.get("content_sha256_16") for v in prev.values()}
    record = write_build_record(content_path, built)
    print("RECORDED", record)
    now = hashlib.sha256(content_path.read_bytes()).hexdigest()[:16]
    if prior and now not in prior:
        print("\nCONTENT CHANGED since the last build."
              "\n  LinkedIn is the one surface that is still hand-maintained —"
              " refresh it from the text-export lane's output (format: text)."
              "\n  Any platform that stores its own copy of the resume is now stale.")


if __name__ == "__main__":
    main()
