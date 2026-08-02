#!/usr/bin/env python3
"""Build a Google-Docs-ready review copy of a session's prose.

Usage:  python3 tools/make_review_doc.py 1        > /tmp/week1-review.html
        python3 tools/make_review_doc.py 20 21    > /tmp/weeks-review.html
        python3 tools/make_review_doc.py 3 --full > /tmp/s3-editing.html

--full keeps the readings blocks and class questions and stamps each page
with its source path: the editing-copy format (Jonathan's own private Docs,
2026-08-02), as opposed to the prose-only review copies shared with Ben.
Editing copies are converted with `pandoc -f html -t gfm`, then either
uploaded through the Drive connector (create_file, contentMimeType
text/markdown) or converted to .docx and dragged into Drive by hand -- the
connector needs the whole text inline, so hand-upload is far cheaper for a
batch. Harvesting edits back: diff the Doc's exported markdown against the
extract this script regenerates from the same commit; the source-path line
under each heading says which file each block belongs to.

Extracts each page's .content prose, drops readings / class questions /
figures / nav (reference-checked separately; not part of the prose review),
and strips class attributes so Drive's HTML→Doc conversion produces a clean
document. Upload the output via the Drive connector as text/html with
conversion enabled, titled "ATAS Week N — review copy (Session N)".
The HTML in this repo stays the source of truth; accepted Doc suggestions
are applied back to the pages by hand (or by a Claude session reading the
Doc's comments).

HARD RULE, learned 2026-07-21: before replacing the Doc's content, ALWAYS
diff its CURRENT content against the previous upload (readDocument, or
File -> Version history). Reviewers edit directly, leaving no comments or
suggestions, and an in-place replace destroys their edits silently -- Ben's
first two review edits were nearly lost this way (recovered via version
history). Harvest collaborator edits first, apply them to the pages, then
regenerate and replace.
"""
import glob
import re
import sys
import html as H


def page_html(path):
    full = FULL
    raw = open(path, encoding="utf-8").read()
    title = H.unescape(re.search(r"<title>(.*?)</title>", raw, re.S).group(1))
    # most pages end their prose at the nav marker; appendix pages carry no
    # marker and end at <nav class="page-nav"> or </body>
    body = re.search(r'<div class="content">(.*?)'
                     r'(?:<!-- PAGE-NAV-START -->|<nav class="page-nav">|</body>)',
                     raw, re.S).group(1)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    if not full:
        body = re.sub(r'<h2 class="section-title">(Questions to bring to class|Readings)'
                      r'</h2>.*?(?=<h2 class="section-title">|'
                      r'<div class="intro-text" style="margin-top:50px;">|$)',
                      "", body, flags=re.S)
        # readings now live as standalone blocks after the intro (Mandatory/
        # Optional restructure, 2026-07-23) -- strip them wherever they sit
        body = re.sub(r'<div class="resource-placeholder[^"]*">.*?</div>\s*',
                      "", body, flags=re.S)
    body = re.sub(r'<div class="intro-text" style="margin-top:50px;">.*$',
                  "", body, flags=re.S)
    body = re.sub(r"<figure>.*?</figure>", "<p><i>[figure]</i></p>", body, flags=re.S)
    body = re.sub(r"<svg.*?</svg>", "<p><i>[diagram]</i></p>", body, flags=re.S)
    body = re.sub(r'<(div|p|h2|h3|h4|ul|li|table|thead|tbody|tr|td|th|span|a)\s[^>]*>',
                  r"<\1>", body)
    body = re.sub(r"</?div>", "", body)
    body = re.sub(r"</?span>", "", body)
    if full:
        # keep inline/display LaTeX verbatim through the markdown conversion:
        # as bare text pandoc escapes every backslash and bracket
        body = re.sub(r"\\\((.*?)\\\)", lambda m: "<code>" + m.group(1).strip() + "</code>",
                      body, flags=re.S)
        body = re.sub(r"\\\[(.*?)\\\]", lambda m: "<code>" + m.group(1).strip() + "</code>",
                      body, flags=re.S)
    body = re.sub(r"\n{3,}", "\n\n", body)
    src = f"<p>source: {H.escape(path)}</p>\n" if full else ""
    return f"<h1>{H.escape(title)}</h1>\n{src}{body.strip()}"


FULL = False


def main():
    global FULL
    args = sys.argv[1:]
    FULL = "--full" in args
    sessions = [a for a in args if not a.startswith("--")]
    if not sessions:
        sys.exit("give session numbers, e.g.: python3 tools/make_review_doc.py 1\n"
                 "  --full  keep readings and class questions (editing copy)")
    label = ", ".join(sessions)
    if FULL:
        out = [f"<h1>ATAS course — editing copy (Session {label})</h1>",
               "<p><i>Private editing copy. Edit the prose here directly; a Claude "
               "session harvests the changes back into the HTML pages, which stay "
               "the source of truth. Each page below carries its source path. "
               "Diagrams appear as [diagram] placeholders and maths as raw LaTeX; "
               "leave both unless the content itself is wrong. Editing a reading's "
               "word count means the page total needs recomputing, so flag those "
               "rather than adjusting them by hand.</i></p>"]
    else:
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
