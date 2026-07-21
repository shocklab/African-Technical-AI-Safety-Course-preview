#!/usr/bin/env python3
"""Build a Google-Docs-ready review copy of a session's prose.

Usage:  python3 tools/make_review_doc.py 1        > /tmp/week1-review.html
        python3 tools/make_review_doc.py 20 21    > /tmp/weeks-review.html

Extracts each page's .content prose, drops readings / class questions /
figures / nav (reference-checked separately; not part of the prose review),
and strips class attributes so Drive's HTML→Doc conversion produces a clean
document. Upload the output via the Drive connector as text/html with
conversion enabled, titled "ATAS Week N — review copy (Session N)".
The HTML in this repo stays the source of truth; accepted Doc suggestions
are applied back to the pages by hand (or by a Claude session reading the
Doc's comments).
"""
import glob
import re
import sys
import html as H


def page_html(path):
    raw = open(path, encoding="utf-8").read()
    title = H.unescape(re.search(r"<title>(.*?)</title>", raw, re.S).group(1))
    body = re.search(r'<div class="content">(.*?)<!-- PAGE-NAV-START -->',
                     raw, re.S).group(1)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    body = re.sub(r'<h2 class="section-title">(Questions to bring to class|Readings)'
                  r'</h2>.*?(?=<h2 class="section-title">|'
                  r'<div class="intro-text" style="margin-top:50px;">|$)',
                  "", body, flags=re.S)
    body = re.sub(r'<div class="intro-text" style="margin-top:50px;">.*$',
                  "", body, flags=re.S)
    body = re.sub(r"<figure>.*?</figure>", "<p><i>[figure]</i></p>", body, flags=re.S)
    body = re.sub(r"<svg.*?</svg>", "<p><i>[diagram]</i></p>", body, flags=re.S)
    body = re.sub(r'<(div|p|h2|h3|h4|ul|li|table|thead|tbody|tr|td|th|span|a)\s[^>]*>',
                  r"<\1>", body)
    body = re.sub(r"</?div>", "", body)
    body = re.sub(r"</?span>", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return f"<h1>{H.escape(title)}</h1>\n{body.strip()}"


def main():
    sessions = sys.argv[1:]
    if not sessions:
        sys.exit("give session numbers, e.g.: python3 tools/make_review_doc.py 1")
    label = ", ".join(sessions)
    out = [f"<h1>ATAS course — review copy (Session {label})</h1>",
           "<p><i>Review surface for the live pages; the HTML in the dev repo is "
           "the source of truth. Suggest and comment freely; accepted changes are "
           "applied back to the site from this Doc. Readings, class questions and "
           "figures are omitted (reference-checked separately). Maths appears as "
           "raw LaTeX; leave it unless the maths itself is wrong.</i></p>"]
    for s in sessions:
        nn = f"{int(s):02d}"
        pages = sorted(glob.glob(f"docs/sessions/session-{nn}/*.html")) or \
            sorted(glob.glob(f"docs/sessions/session-{nn}-*.html"))

        def session_key(path):
            import re as _re
            raw = open(path, encoding="utf-8").read()
            m = _re.search(r"<title>Session (\d+)\.(\d+)", raw)
            return (int(m.group(1)), int(m.group(2))) if m else (99, 99)
        pages.sort(key=session_key)
        if not pages:
            sys.exit(f"no pages found for session {nn}")
        out += [page_html(p) for p in pages]
    print("\n".join(out))


if __name__ == "__main__":
    main()
