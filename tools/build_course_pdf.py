#!/usr/bin/env python3
"""Bind the released lesson pages into one printable PDF.

    python3 tools/build_course_pdf.py            # released sessions, no readings
    python3 tools/build_course_pdf.py --readings # keep the reading lists

Page order comes from docs/index.html, which is the site's own sequence, so a
newly released session joins the book without touching this file. Chrome does
the printing because the pages carry MathJax and inline SVG that a LaTeX route
would mangle.
"""
import html as H, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
KEEP_READINGS = "--readings" in sys.argv

STRIP = [r'<!-- TOP-NAV-START -->.*?<!-- TOP-NAV-END -->',
         r'<nav class="page-nav">.*?</nav>',
         r'<div class="ai-notice">.*?</div>',
         r'<!-- PAGE-NAV-START -->.*?<!-- PAGE-NAV-END -->']
if not KEEP_READINGS:
    STRIP.append(r'<div class="resource-placeholder.*?</div>\s*')

def body_of(p):
    s = p.read_text(encoding="utf-8")
    i = s.find('<div class="content">')
    if i < 0: return None
    b = s[i + len('<div class="content">'):]
    j = b.rfind('</div>')
    b = b[:j] if j > 0 else b
    hdr = re.search(r'<header>(.*?)</header>', s, re.S)
    for pat in STRIP:
        b = re.sub(pat, '', b, flags=re.S)
    b = re.sub(r'src="(?:\.\./)+assets/', f'src="{DOCS}/assets/', b)
    return (hdr.group(1) if hdr else ''), b

idx = (DOCS / "index.html").read_text(encoding="utf-8")
pages = [(m.group(1), H.unescape(m.group(2)).strip())
         for m in re.finditer(r'href="(sessions/session-\d\d/[^"]+)"[^>]*>([^<]*)</a>', idx)]
seen, ordered = set(), []
for href, label in pages:
    if href not in seen:
        seen.add(href); ordered.append((href, label))

parts, toc = [], []
for n, (href, label) in enumerate(ordered, 1):
    got = body_of(DOCS / href)
    if not got:
        print(f"  skipped (no content div): {href}", file=sys.stderr); continue
    hdr, b = got
    anchor = f"pg{n}"
    toc.append(f'<li><a href="#{anchor}">{H.escape(label)}</a></li>')
    parts.append(f'<section class="lesson" id="{anchor}"><header>{hdr}</header>{b}</section>')

css = (DOCS / "assets" / "styles.css").read_text(encoding="utf-8")
out = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>African Technical AI Safety</title>
<script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],processEscapes:true}},svg:{{fontCache:'global'}}}};</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<style>{css}</style>
<style>
  @page {{ size: A4; margin: 18mm 16mm 20mm; }}
  body {{ background:#fff; }}
  .lesson {{ break-before: page; padding: 0; max-width: none; }}
  .lesson:first-of-type {{ break-before: auto; }}
  .titlepage {{ break-after: page; text-align:center; padding-top:60mm; }}
  .titlepage h1 {{ font-size:2.6rem; margin-bottom:6mm; }}
  .contents {{ break-after: page; }}
  .contents ol {{ line-height:1.9; }}
  h1,h2,h3,h4 {{ break-after: avoid; }}
  pre, table, figure, .lab-box, .technical-detail, .case-study, .info-box {{ break-inside: avoid; }}
  img, svg {{ max-width:100%; height:auto; }}
  a {{ color:inherit; text-decoration:none; }}
</style></head><body>
<div class="titlepage">
  <h1>African Technical AI Safety</h1>
  <p style="font-size:1.15rem">Lesson notes, Sessions 1 to 7</p>
  <p style="color:#5a6672">{len(ordered)} sub-sessions{'' if KEEP_READINGS else ' · reading lists omitted'}</p>
</div>
<div class="contents"><h1>Contents</h1><ol>{''.join(toc)}</ol></div>
{''.join(parts)}
</body></html>"""

tmp = ROOT / "docs" / "_course-book.html"
tmp.write_text(out, encoding="utf-8")
pdf = ROOT / "African-Technical-AI-Safety-Sessions-1-7.pdf"
print(f"  {len(ordered)} pages bound -> {tmp.name}")
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=60000", "--no-pdf-header-footer",
                f"--print-to-pdf={pdf}", tmp.as_uri()], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"  -> {pdf.name}  ({pdf.stat().st_size/1e6:.1f} MB)")
