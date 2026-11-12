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
         for m in re.finditer(r'href="(sessions/session-\d\d(?:/[^"?#]+|-[^"/?#]+\.html))"[^>]*>(.*?)</a>', idx, re.S)]
seen, ordered = set(), []
for href, label in pages:
    if href not in seen:
        seen.add(href); ordered.append((href, label))

parts, toc, included_sessions, cur = [], [], set(), None
for n, (href, label) in enumerate(ordered, 1):
    got = body_of(DOCS / href)
    if not got:
        print(f"  skipped (no content div): {href}", file=sys.stderr); continue
    hdr, b = got
    included_sessions.add(int(re.search(r'session-(\d\d)', href).group(1)))
    label = re.sub(r'<[^>]+>', '', label).strip()
    sess = re.search(r'session-(\d\d)', href).group(1)
    if sess != cur:
        if cur is not None:
            parts.append('</div>')
        parts.append(f'<div class="session" id="s{sess}">')
        cur = sess
    anchor = f"pg{n}"
    toc.append(f'<li><a href="#{anchor}">{H.escape(label)}</a></li>')
    parts.append(f'<section class="lesson" id="{anchor}"><header>{hdr}</header>{b}</section>')

if cur is not None:
    parts.append('</div>')

css = (DOCS / "assets" / "styles.css").read_text(encoding="utf-8")
if not parts:
    sys.exit("no lesson pages found in docs/index.html")
session_numbers = sorted(included_sessions)
consecutive = session_numbers == list(range(session_numbers[0], session_numbers[-1] + 1))
if len(session_numbers) == 1:
    session_label = f"Session {session_numbers[0]}"
elif consecutive:
    session_label = f"Sessions {session_numbers[0]} to {session_numbers[-1]}"
else:
    session_label = "Sessions " + ", ".join(map(str, session_numbers[:-1])) + f" and {session_numbers[-1]}"
pdf_suffix = (f"{session_numbers[0]}-{session_numbers[-1]}" if consecutive
              else "-".join(map(str, session_numbers)))
out = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>African Technical AI Safety</title>
<script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],processEscapes:true}},svg:{{fontCache:'global'}}}};</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<style>{css}</style>
<style>
  /* Textbook typography: the site CSS above is tuned for screen reading. */
  @page {{ size: A4; margin: 19mm 20mm 20mm; }}
  html, body {{ background:#fff; font-size: 10pt !important; line-height: 1.34 !important;
                padding:0 !important; margin:0 !important; }}
  .container {{ border:none !important; box-shadow:none !important; max-width:none !important; }}
  .content {{ padding:0 !important; max-width:none !important; }}
  p, li {{ line-height:1.34 !important; text-align:justify; hyphens:auto; -webkit-hyphens:auto; }}
  p {{ margin:0 0 4.5pt !important; }}

  .session {{ break-before: page; }}
  .session:first-of-type {{ break-before: auto; }}
  .lesson {{ padding:0; max-width:none; margin-top: 13pt; }}
  .lesson header {{ padding:0 !important; margin:0 0 6pt !important; border-bottom:0.5pt solid #ccd4dc; }}
  .lesson header h1 {{ font-size:15pt !important; margin:0 0 2pt !important; line-height:1.15 !important; }}
  .lesson header p {{ font-size:9.5pt !important; color:#5a6672; margin:0 0 4pt !important; }}
  .week-badge {{ font-size:7.5pt !important; margin:0 0 2pt !important; padding:0 !important;
                 background:none !important; color:#5a6672 !important; letter-spacing:1px; }}

  h2, .section-title {{ font-size:12pt !important; margin:11pt 0 4pt !important; line-height:1.2 !important; }}
  h3 {{ font-size:10.5pt !important; margin:8pt 0 3pt !important; }}
  h4 {{ font-size:10pt !important; margin:0 0 3pt !important; }}
  .intro-text {{ padding:7pt 9pt !important; margin:0 0 8pt !important; }}
  .intro-text h2 {{ font-size:11.5pt !important; margin:0 0 3pt !important; }}
  .intro-text p {{ font-size:10pt !important; line-height:1.34 !important; margin:0 0 3pt !important; }}
  .info-box, .warning-box, .technical-detail, .case-study, .lab-box, .highlight-box, .tool-card {{
      padding:7pt 9pt !important; margin:7pt 0 !important; border-radius:3px !important; }}
  .technical-detail p, .case-study p, .lab-box p, .info-box p {{ line-height:1.34 !important; margin:0 0 3.5pt !important; }}
  ul, ol, .styled-list {{ margin:4pt 0 6pt !important; padding-left:13pt !important; }}
  .styled-list li {{ padding:0 0 0 11pt !important; line-height:1.32 !important; margin-bottom:1.5pt; }}
  li {{ margin-bottom:1.5pt; }}
  .card-grid {{ grid-template-columns:1fr 1fr !important; gap:6pt !important; margin:6pt 0 !important; }}
  .card {{ padding:6pt 8pt !important; border-radius:3px !important; break-inside:avoid; }}
  .card h3 {{ font-size:10pt !important; margin:0 0 2pt !important; }}
  .card p {{ font-size:9.2pt !important; line-height:1.3 !important; margin:0 0 2pt !important; }}
  .resource-placeholder {{ margin:7pt 0 !important; padding:6pt 0 2pt !important; }}
  .formula {{ padding:5pt 8pt !important; margin:6pt 0 !important; font-size:10pt !important; }}
  pre, code {{ font-size:8.2pt !important; line-height:1.3 !important; }}
  pre {{ padding:5pt 7pt !important; margin:5pt 0 !important; }}
  table {{ font-size:9pt !important; }}
  td, th {{ padding:2.5pt 5pt !important; }}
  figure {{ margin:7pt 0 !important; }}
  figure.wide {{ width:100% !important; margin-left:0 !important; transform:none !important; }}
  figcaption {{ font-size:8.5pt !important; margin-top:3pt !important; }}
  img, svg {{ max-width:100%; max-height:105mm; height:auto; }}
  a {{ color:inherit !important; text-decoration:none !important; }}

  .titlepage {{ break-after: page; text-align:center; padding-top:75mm; }}
  .titlepage h1 {{ font-size:26pt !important; margin-bottom:6mm !important; }}
  .contents {{ break-after: page; }}
  .contents h1 {{ font-size:16pt !important; margin-bottom:6pt !important; }}
  .contents ol {{ line-height:1.5 !important; font-size:10pt; columns:2; column-gap:10mm; }}
  h1,h2,h3,h4 {{ break-after: avoid; }}
  pre, table, figure, .formula {{ break-inside: avoid; }}
  p {{ orphans:2; widows:2; }}
</style></head><body>
<div class="titlepage">
  <h1>African Technical AI Safety</h1>
  <p style="font-size:1.15rem">Lesson notes, {session_label}</p>
  <p style="color:#5a6672">{len(toc)} sub-sessions{'' if KEEP_READINGS else ' · reading lists omitted'}</p>
</div>
<div class="contents"><h1>Contents</h1><ol>{''.join(toc)}</ol></div>
{''.join(parts)}
</body></html>"""

tmp = ROOT / "docs" / "_course-book.html"
pdf = ROOT / f"African-Technical-AI-Safety-Sessions-{pdf_suffix}.pdf"
try:
    tmp.write_text(out, encoding="utf-8")
    print(f"  {len(toc)} pages bound -> {tmp.name}")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=60000", "--no-pdf-header-footer",
                f"--print-to-pdf={pdf}", tmp.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
finally:
    tmp.unlink(missing_ok=True)
print(f"  -> {pdf.name}  ({pdf.stat().st_size/1e6:.1f} MB)")
