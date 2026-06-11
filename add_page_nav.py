#!/usr/bin/env python3
"""
add_page_nav.py — inject a "← Previous / Contents / Next →" bar into each built
lesson page (and sub-session page) linked from docs/index.html.

The reading ORDER is read directly from docs/index.html (the contents page is the
single source of truth), so reordering or adding sessions/sub-sessions there and
re-running keeps the nav correct. Only links that point to files that actually
exist are chained — "coming soon" entries are <span>, not <a>, so they are
skipped. Pages may live at any depth under docs/ (e.g. sessions/session-04/4-1.html);
prev/next/contents hrefs are computed as correct relative paths per page.

Idempotent: the block is wrapped in <!-- PAGE-NAV-START/END --> markers and
replaced (not duplicated) on re-run.

Usage:
    python3 add_page_nav.py          # write nav into all linked lesson pages
    python3 add_page_nav.py --check  # dry run: print the detected order, write nothing
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
INDEX = DOCS / "index.html"

NAV_START = "<!-- PAGE-NAV-START -->"
NAV_END = "<!-- PAGE-NAV-END -->"


def strip_tags(s: str) -> str:
    s = re.sub(r'<span class="badge-built">.*?</span>', "", s, flags=re.DOTALL)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def detected_order():
    """Return [(docs_relative_href, title), ...] for built lesson links, in order."""
    html = INDEX.read_text(encoding="utf-8")
    pairs = []
    for m in re.finditer(r'<a[^>]*href="((?:sessions|session)[^"]+\.html)"[^>]*>(.*?)</a>', html, re.DOTALL):
        href, inner = m.group(1), m.group(2)
        if (DOCS / href).exists():
            pairs.append((href, strip_tags(inner)))
    return pairs


def rel(from_dir: Path, to_href: str) -> str:
    """Relative href from a page's directory to a docs-relative target."""
    target = (DOCS / to_href).resolve()
    return os.path.relpath(target, start=from_dir).replace(os.sep, "/")


def nav_cell(kind, href, label, title):
    return (
        f'  <a class="{kind}" href="{href}">'
        f'<span class="nav-label">{label}</span>'
        f'<span class="nav-title">{title}</span></a>'
    )


def build_nav(page_dir, prev, nxt):
    left = (
        nav_cell("prev", rel(page_dir, prev[0]), "← Previous", prev[1])
        if prev else '  <span class="nav-empty"></span>'
    )
    home = f'  <a class="home" href="{rel(page_dir, "index.html")}"><span class="nav-title">⌂</span></a>'
    right = (
        nav_cell("next", rel(page_dir, nxt[0]), "Next →", nxt[1])
        if nxt else '  <span class="nav-empty"></span>'
    )
    return f'{NAV_START}\n<nav class="page-nav">\n{left}\n{home}\n{right}\n</nav>\n{NAV_END}'


def inject(html: str, nav: str) -> str:
    html = re.sub(
        re.escape(NAV_START) + r".*?" + re.escape(NAV_END) + r"\n?",
        "", html, flags=re.DOTALL,
    )
    body_idx = html.find("</body>")
    div_idx = html.rfind("</div>", 0, body_idx)
    if div_idx == -1:
        raise ValueError("no closing </div> before </body>")
    return html[:div_idx] + nav + "\n" + html[div_idx:]


def main():
    check = "--check" in sys.argv
    order = detected_order()

    print(f"Detected {len(order)} built page(s) in index.html order:")
    for i, (href, title) in enumerate(order):
        print(f"  {i + 1}. {title}  [{href}]")
    if not order:
        print("Nothing to do.")
        return
    if check:
        print("\n--check: no files written.")
        return

    for i, (href, _) in enumerate(order):
        prev = order[i - 1] if i > 0 else None
        nxt = order[i + 1] if i < len(order) - 1 else None
        path = DOCS / href
        html = path.read_text(encoding="utf-8")
        path.write_text(inject(html, build_nav(path.parent, prev, nxt)), encoding="utf-8")
        print(f"  ✓ nav written → {href}")


if __name__ == "__main__":
    main()
