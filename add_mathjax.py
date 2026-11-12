#!/usr/bin/env python3
"""
add_mathjax.py — inject the MathJax v3 loader into every docs/ HTML page (idempotent).

Configured for \\(...\\) inline and \\[...\\] display delimiters; single-$ is NOT a
delimiter (so currency like "$60 billion" is safe), and <code>/<pre> are skipped (so
code, filenames, arXiv IDs and hex colours are never typeset). Re-run any time pages
are added; the block is wrapped in <!-- MATHJAX-START/END --> markers and replaced,
not duplicated.
"""
import re, pathlib

DOCS = pathlib.Path(__file__).resolve().parent / "docs"
BLOCK = (
    "    <!-- MATHJAX-START -->\n"
    "    <script>window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],processEscapes:true},svg:{fontCache:'global'},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>\n"
    '    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>\n'
    "    <!-- MATHJAX-END -->\n"
)

n = 0
for f in sorted(DOCS.rglob("*.html")):
    # Notebook renderings have their own maths configuration.
    if f.is_relative_to(DOCS / "labs"):
        continue
    html = f.read_text(encoding="utf-8")
    html = re.sub(r"[ \t]*<!-- MATHJAX-START -->.*?<!-- MATHJAX-END -->\n?", "", html, flags=re.DOTALL)
    if "</head>" not in html:
        print("  ! no </head>:", f.name); continue
    html = html.replace("</head>", BLOCK + "</head>", 1)
    f.write_text(html, encoding="utf-8")
    n += 1
    print("  ✓", f.relative_to(DOCS))
print(f"MathJax loader written into {n} page(s).")
