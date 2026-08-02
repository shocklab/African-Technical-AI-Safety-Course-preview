#!/usr/bin/env python3
"""Collect every reading in the course into one linked markdown list.

Usage:  python3 tools/make_readings_doc.py > /tmp/readings.md

Pulls the readings blocks from all 24 sessions in course order, keeping the
Mandatory / Optional split where a page has been restructured and the plain
Readings section where it has not. Emits markdown directly rather than going
through pandoc: the links are the whole point of this document, and an HTML
round-trip is one more place to lose them. Sessions with no readings block
are listed at the end rather than dropped, so a gap stays visible.
"""
import glob
import re
import sys
import html as H


def to_markdown(frag):
    """One readings fragment of HTML -> markdown lines, links intact."""
    frag = re.sub(r"<script.*?</script>", "", frag, flags=re.S)
    frag = re.sub(r"<(h3|h4)[^>]*>(.*?)</\1>", r"\n### \2\n", frag, flags=re.S)
    frag = re.sub(r"</(p|li|div)>", "\n", frag)
    frag = re.sub(r"<li[^>]*>", "- ", frag)
    frag = re.sub(r"<a\s[^>]*?href=\"([^\"]+)\"[^>]*>(.*?)</a>",
                  lambda m: f"[{re.sub(r'<[^>]+>', '', m.group(2)).strip()}]({m.group(1)})",
                  frag, flags=re.S)
    frag = re.sub(r"<(strong|b)>(.*?)</\1>", r"**\2**", frag, flags=re.S)
    frag = re.sub(r"<(em|i)>(.*?)</\1>", r"*\2*", frag, flags=re.S)
    frag = re.sub(r"<code>(.*?)</code>", r"`\1`", frag, flags=re.S)
    frag = re.sub(r"<[^>]+>", "", frag)
    frag = H.unescape(frag)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in frag.split("\n")]
    out = []
    for ln in lines:
        if not ln:
            continue
        if ln.startswith("###"):
            out += ["", ln, ""]
        elif ln.startswith("•"):
            out.append("- " + ln.lstrip("• ").strip())
        elif ln.startswith(("[", "**")) and not ln.startswith("**Total"):
            # ported pages write entries as bare paragraphs, not bullets
            out.append("- " + ln)
        else:
            out.append(ln)
    return "\n".join(out)


def balanced_div(text, start):
    """Inner HTML of the <div> opening at `start`, respecting nesting.

    The ported Session 4 and 8 pages nest divs inside their readings blocks,
    so a non-greedy match to the first </div> runs past the block and drags
    page content in with it."""
    i = text.index(">", start) + 1
    depth, j = 1, i
    for m in re.finditer(r"<div\b|</div>", text[i:]):
        depth += 1 if m.group(0) != "</div>" else -1
        if depth == 0:
            return text[i:i + m.start()], i + m.end()
        j = i + m.end()
    return text[i:j], j


def page_readings(path):
    raw = open(path, encoding="utf-8").read()
    title = H.unescape(re.search(r"<title>(.*?)</title>", raw, re.S).group(1))
    body = re.search(r'<div class="content">(.*?)'
                     r'(?:<!-- PAGE-NAV-START -->|<nav class="page-nav">|</body>)',
                     raw, re.S).group(1)
    blocks, seen = [], set()
    # on unrestructured pages the placeholder divs sit INSIDE a Readings
    # section; take the section and skip the placeholders it contains, or
    # every such page lists its readings twice
    spans = []
    for m in re.finditer(r'<h2 class="section-title">Readings</h2>(.*?)'
                         r'(?=<h2 class="section-title">|'
                         r'<div class="intro-text" style="margin-top:50px;">|$)',
                         body, flags=re.S):
        spans.append((m.start(), m.end()))
        blocks.append(m.group(1))
    for m in re.finditer(r'<div class="resource-placeholder[^"]*">', body):
        if any(a <= m.start() < b for a, b in spans):
            continue
        inner, _ = balanced_div(body, m.start())
        blocks.append(inner)
    md_parts = []
    for b in blocks:
        md = to_markdown(b)
        # a page can carry the same list in both shapes; keep the first
        key = re.sub(r"\W+", "", md)
        if key and key not in seen:
            seen.add(key)
            md_parts.append(md)
    if not md_parts:
        return None, 0
    md = "\n".join(md_parts)
    return f"## {title}\n\n{md}", len(re.findall(r"\]\(https?://", md))


def main():
    out = ["# ATAS course — every reading, with links", "",
           "Mandatory and optional readings for all 24 sessions in course "
           "order, with the annotations and word counts from the pages "
           "themselves. Sessions 1 to 4 carry the Mandatory / Optional split; "
           "later sessions still use a single Readings list, which is the "
           "restructure not yet done. The session pages remain the source of "
           "truth: this document is generated from them.", ""]
    missing, links = [], 0
    for n in range(1, 25):
        nn = f"{n:02d}"
        pages = sorted(glob.glob(f"docs/sessions/session-{nn}/*.html")) or \
            sorted(glob.glob(f"docs/sessions/session-{nn}-*.html"))

        def session_key(path):
            raw = open(path, encoding="utf-8").read()
            m = re.search(r"<title>Session (\d+)\.(\d+)", raw)
            return (int(m.group(1)), int(m.group(2))) if m else (99, 99)
        pages.sort(key=session_key)
        got = []
        for p in pages:
            md, k = page_readings(p)
            if md:
                got.append(md)
                links += k
        if not got:
            missing.append(n)
            continue
        out += [f"# Session {n}", ""] + got + [""]
    if missing:
        out += ["# Sessions with no readings block", "",
                "These are lab, project-work and presentation sessions: "
                + ", ".join(f"Session {m}" for m in missing) + ".", ""]
    print("\n".join(out))
    print(f"{links} links, sessions with no readings: {missing}", file=sys.stderr)


if __name__ == "__main__":
    main()
