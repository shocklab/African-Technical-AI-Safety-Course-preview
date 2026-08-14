#!/usr/bin/env python3
"""Render every lab notebook in docs/labs/ to a course-styled HTML page.

Usage:  python3 tools/render_notebooks.py            # render all
        python3 tools/render_notebooks.py 2-5        # render matching ones

The .ipynb stays the thing students download and run; the HTML is so the
notebook can be read on the site without downloading anything. Re-run after
editing a notebook. nbconvert's "basic" template gives us the cell markup
only, which we wrap in the course shell so it matches the lesson pages.
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABS = ROOT / "docs" / "labs"
REPO = "shocklab/African-Technical-AI-Safety-Course"

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="../assets/styles.css">
    <!-- MATHJAX-START -->
    <script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],processEscapes:true}},svg:{{fontCache:'global'}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <!-- MATHJAX-END -->
<style>
  .notebook {{ padding:0 48px 40px; }}
  .notebook .jp-Cell, .notebook .cell {{ margin:0 0 18px; }}
  .notebook pre, .notebook .highlight pre {{ background:#f5f7f9; border:1px solid #e4e8ec; border-left:3px solid #2a5298;
      border-radius:4px; padding:14px 16px; overflow-x:auto; font-family:var(--mono); font-size:0.82rem;
      line-height:1.5; color:#1f2d3a; }}
  .notebook .jp-InputArea-prompt, .notebook .jp-OutputArea-prompt, .notebook .prompt {{ display:none; }}
  .notebook h1 {{ font-family:var(--display); color:var(--navy); font-size:1.9rem; margin:28px 0 10px; }}
  .notebook h2 {{ font-family:var(--display); color:var(--navy); font-size:1.4rem; margin:34px 0 10px;
      padding-top:14px; border-top:1px solid var(--rule); }}
  .notebook h3 {{ font-family:var(--display); color:var(--blue); font-size:1.1rem; margin:24px 0 8px; }}
  .notebook blockquote {{ border-left:3px solid var(--blue); background:var(--tint); margin:18px 0;
      padding:12px 18px; color:var(--ink); }}
  .notebook table {{ border-collapse:collapse; margin:16px 0; }}
  .notebook td, .notebook th {{ border:1px solid var(--rule); padding:6px 10px; font-size:0.9rem; }}
  .notebook img {{ max-width:100%; height:auto; }}
  .nb-actions {{ margin:22px 48px 0; padding:16px 20px; background:var(--tint);
      border-left:3px solid var(--navy); }}
  .nb-actions a {{ color:var(--blue); }}
  .nb-actions p {{ margin:0 0 6px; font-size:0.94rem; }}
  .nb-actions p:last-child {{ margin-bottom:0; }}
  @media (max-width:760px) {{ .notebook {{ padding:0 24px 30px; }} .nb-actions {{ margin:22px 24px 0; }} }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>{heading}</h1>
        <p class="subtitle">{subtitle}</p>
    </div>
    <div class="nb-actions">
        <p><strong>This is a read-only rendering.</strong> To run it:
           <a href="https://colab.research.google.com/github/{repo}/blob/main/docs/labs/{ipynb}"
              target="_blank" rel="noopener">open in Google Colab</a>, or
           <a href="{ipynb}" download>download the .ipynb</a> and upload it yourself.</p>
        <p>The cells have no saved outputs: you run them and keep your own.
           <a href="{back}">Back to the lab page</a>.</p>
    </div>
    <div class="notebook">
{body}
    </div>
    <nav class="page-nav">
        <a class="prev" href="{back}"><span class="nav-label">Return to</span><span class="nav-title">{back_title}</span></a>
        <a class="home" href="../index.html"><span class="nav-title">⌂</span></a>
        <span class="nav-empty"></span>
    </nav>
</div>
</body>
</html>
"""

# which lesson page each notebook belongs to
BACKLINKS = {
    "session-6-5-reward-models":
        ("../sessions/session-06/lab-rlhf.html",
         "6.5 · Lab: reward models &amp; over-optimisation",
         "Session 6.5 — Lab notebook",
         "Reward models and over-optimisation"),
    "session-2-5-scaling-and-transformerlens":
        ("../sessions/session-02/lab-scaling-and-transformerlens.html",
         "2.5 · Lab: scaling laws &amp; a first look inside a model",
         "Session 2.5 — Lab notebook",
         "Scaling laws and a first look inside a model"),
}


def dollars_to_backslash(markup):
    """Rewrite $…$ / $$…$$ into \\(…\\) / \\[…\\] outside code.

    Notebooks use dollar delimiters, which is what Jupyter and Colab render.
    The site's MathJax deliberately does not treat a single $ as a delimiter,
    so currency survives (add_mathjax.py). Converting here means the notebook
    keeps the delimiters its own tools want and the page gets the ones the
    course config wants, with no per-page MathJax exception to maintain.
    """
    parts = re.split(r"(<pre\b.*?</pre>|<code\b.*?</code>)", markup, flags=re.S)
    for i, part in enumerate(parts):
        if part.startswith(("<pre", "<code")):
            continue
        part = re.sub(r"\$\$(.+?)\$\$", r"\\[\1\\]", part, flags=re.S)
        part = re.sub(r"(?<![\\$])\$([^$\n]+?)\$", r"\\(\1\\)", part)
        parts[i] = part
    return "".join(parts)


def render(nb_path):
    stem = nb_path.stem
    out = subprocess.run(
        [sys.executable, "-m", "nbconvert", "--to", "html", "--template", "basic",
         "--stdout", str(nb_path)],
        capture_output=True, text=True, check=True).stdout
    # nbconvert emits empty output wrappers for unexecuted cells; drop them
    out = re.sub(r'<div class="jp-Cell-outputWrapper">\s*</div>', "", out)
    # and pilcrow anchor links on every heading
    out = re.sub(r'<a class="anchor-link"[^>]*>.*?</a>', "", out, flags=re.S)
    # the shell already prints the title, so drop the notebook's own first h1
    out = re.sub(r"<h1[^>]*>.*?</h1>", "", out, count=1, flags=re.S)
    out = dollars_to_backslash(out)
    back, back_title, heading, subtitle = BACKLINKS.get(
        stem, ("../index.html", "Contents", stem, "Lab notebook"))
    page = PAGE.format(title=html.escape(heading), heading=heading, subtitle=subtitle,
                       repo=REPO, ipynb=nb_path.name, back=back, back_title=back_title,
                       body=out)
    dest = nb_path.with_suffix(".html")
    dest.write_text(page, encoding="utf-8")
    return dest, len(page)


def main():
    pats = sys.argv[1:]
    nbs = sorted(p for p in LABS.glob("*.ipynb")
                 if not pats or any(pat in p.name for pat in pats))
    if not nbs:
        sys.exit(f"no notebooks matched in {LABS}")
    for nb in nbs:
        dest, size = render(nb)
        print(f"  ✓ {nb.name} → {dest.name} ({size:,} bytes)")


if __name__ == "__main__":
    main()
