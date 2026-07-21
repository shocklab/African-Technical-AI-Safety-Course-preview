#!/usr/bin/env python3
"""Corpus-level density census for STYLE.md families over docs/ .content prose."""
import html as htmlmod
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")

SKIP_TAGS = {"script", "style"}
CODE_TAGS = {"code", "pre"}


class ContentExtractor(HTMLParser):
    """Extract the .content subtree; produce (a) inner HTML, (b) text nodes with
    context (in_heading, in_code, container classes)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0            # depth inside .content (0 = outside)
        self.stack = []           # (tag, classes) inside content
        self.text_nodes = []      # (text, in_heading, in_code, containers frozenset, in_strong)
        self.html_parts = []      # raw-ish reconstruction for tag-context counts
        self.skip = 0
        self.strong_events = []   # (containers_at_open, parent_tag)

    def handle_starttag(self, tag, attrs):
        cls = ()
        for k, v in attrs:
            if k == "class" and v:
                cls = tuple(v.split())
        if self.depth == 0:
            if tag == "div" and "content" in cls:
                self.depth = 1
            return
        self.depth += 1
        if tag in SKIP_TAGS or tag in CODE_TAGS:
            self.skip += 1
        if tag == "strong" and not self.skip:
            containers = set()
            parent = self.stack[-1][0] if self.stack else None
            for t, c in self.stack:
                containers.update(c)
            self.strong_events.append((frozenset(containers), parent))
        self.stack.append((tag, cls))
        self.html_parts.append(f"<{tag} {' '.join(c for c in cls)}>")

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if self.depth == 0:
            return
        self.depth -= 1
        if self.stack:
            t, c = self.stack.pop()
            if t in SKIP_TAGS or t in CODE_TAGS:
                self.skip -= 1
        self.html_parts.append(f"</{tag}>")
        if self.depth == 0:
            self.depth = -1  # done; ignore rest

    def handle_data(self, data):
        if self.depth <= 0 or self.skip:
            return
        tags = [t for t, c in self.stack]
        containers = set()
        for t, c in self.stack:
            containers.update(c)
        in_heading = any(t in ("h1", "h2", "h3", "h4", "h5") for t in tags)
        in_strong = "strong" in tags
        self.text_nodes.append((data, in_heading, in_strong, frozenset(containers)))
        self.html_parts.append(data)


MATH_RE = re.compile(r"\\\((?:.|\n)*?\\\)|\\\[(?:.|\n)*?\\\]")


def extract(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    p = ContentExtractor()
    p.feed(raw)
    return p, raw


def clean_text(nodes, include_headings=True):
    parts = []
    for text, in_h, in_s, containers in nodes:
        if not include_headings and in_h:
            continue
        parts.append(text)
    txt = " ".join(parts)
    txt = MATH_RE.sub(" ", txt)
    txt = re.sub(r"\s+", " ", txt)
    return txt


FURNITURE = {"resource-placeholder", "next-box", "ai-notice", "page-nav", "top-nav"}

FAMILIES = {
    # regex on prose text (headings excluded where noted)
    "emdash": re.compile(r"—"),
    "endash_spaced": re.compile(r"\s–\s"),
    "hyphen_spaced": re.compile(r"[a-zA-Z)\"']\s-\s[a-zA-Z(\"']"),
    "x_not_y": re.compile(r",\s*not\s+[a-z(“\"]", re.I),
    "not_just_but": re.compile(r"\bnot\s+(just|merely|only|simply)\b", re.I),
    "its_not_x_its_y": re.compile(r"\b(is|it'?s|are|was)\s+not\s+[^.;:]{2,40}[;,]\s*(it'?s|it\s+is|they'?re|but)\s", re.I),
    "course_agent": re.compile(r"\b(the|this)\s+course\b", re.I),
    "honest_lex": re.compile(r"\bhonest(ly|y)?\b", re.I),
    "deliberate": re.compile(r"\bdeliberate(ly)?\b", re.I),
    "arrow": re.compile(r"→"),
    "exactly": re.compile(r"\bexactly\b", re.I),
    "genuine": re.compile(r"\bgenuine(ly)?\b", re.I),
    "precisely": re.compile(r"\bprecisely\b", re.I),
    "the_whole": re.compile(r"\bthe whole\b", re.I),
    "worth_ing": re.compile(r"\bworth\s+\w+ing\b", re.I),
    "truly": re.compile(r"\btruly\b", re.I),
    "really": re.compile(r"\breally\b", re.I),
    "simply": re.compile(r"\bsimply\b", re.I),
    "actually": re.compile(r"\bactually\b", re.I),
    "just": re.compile(r"\bjust\b", re.I),
    # essayist tics
    "lands": re.compile(r"\bland(s|ed)?\b", re.I),
    "rhymes": re.compile(r"\brhym\w+\b", re.I),
    "cash_out": re.compile(r"\bcash\w*\s+(that\s+)?out\b|\bcash(es|ed)?\s+out\b", re.I),
    "earn_keep": re.compile(r"\bearn\w*\s+(its|their)\s+keep\b", re.I),
    "spine": re.compile(r"\bspine\b", re.I),
    "wedge": re.compile(r"\bwedge\b", re.I),
    "through_line": re.compile(r"\bthrough-?line\b", re.I),
    "tee_up": re.compile(r"\btee(s|d)?\s+(it\s+|this\s+)?up\b", re.I),
    "reckoning": re.compile(r"\breckoning\b", re.I),
    "uncomfortable": re.compile(r"\b(the|an)\s+uncomfortable\b", re.I),
    "clean_x": re.compile(r"\b(a|the)\s+clean(est)?\s+\w+", re.I),
    "vivid": re.compile(r"\bvivid\w*\b", re.I),
    "hold_that": re.compile(r"\bhold\s+(that|onto|on\s+to)\b", re.I),
    "in_one_sentence": re.compile(r"\bin\s+one\s+(sentence|line)\b", re.I),
    "serves_as": re.compile(r"\bserv(es|e|ed|ing)\s+as\b", re.I),
    "boasts": re.compile(r"\bboast\w*\b", re.I),
    # self-labelling (§2)
    "load_bearing": re.compile(r"\bload-?bearing\b", re.I),
    "headline": re.compile(r"\b(the|a)\s+headline\b", re.I),
    "punchline": re.compile(r"\bpunch\s?line\b", re.I),
    "the_lesson": re.compile(r"\bthe\s+lesson\b", re.I),
    "the_point_is": re.compile(r"\bthe\s+point\s+is\b", re.I),
    "the_move": re.compile(r"\bthe\s+move\b", re.I),
    "the_prize": re.compile(r"\bthe\s+prize\b", re.I),
    "the_catch": re.compile(r"\bthe\s+catch\b", re.I),
    "notice_that": re.compile(r"\bnotice\s+that\b", re.I),
    # banned canon (§8)
    "delve": re.compile(r"\bdelv\w+\b", re.I),
    "leverage": re.compile(r"\bleverag\w+\b", re.I),
    "harness": re.compile(r"\bharness\w*\b", re.I),
    "underscore": re.compile(r"\bunderscor\w+\b", re.I),
    "bolster": re.compile(r"\bbolster\w*\b", re.I),
    "foster": re.compile(r"\bfoster\w*\b", re.I),
    "comprehensive": re.compile(r"\bcomprehensive\w*\b", re.I),
    "seamless": re.compile(r"\bseamless\w*\b", re.I),
    "intricate": re.compile(r"\bintricate\w*\b", re.I),
    "nuanced": re.compile(r"\bnuanc\w+\b", re.I),
    "multifaceted": re.compile(r"\bmultifaceted\b", re.I),
    "holistic": re.compile(r"\bholistic\w*\b", re.I),
    "pivotal": re.compile(r"\bpivotal\b", re.I),
    "groundbreaking": re.compile(r"\bgroundbreaking\b", re.I),
    "transformative": re.compile(r"\btransformative\b", re.I),
    "testament": re.compile(r"\btestament\b", re.I),
    "realm": re.compile(r"\brealm\w*\b", re.I),
    "landscape": re.compile(r"\blandscape\w*\b", re.I),
    "moreover": re.compile(r"\bmoreover\b", re.I),
    "furthermore": re.compile(r"\bfurthermore\b", re.I),
    "additionally": re.compile(r"\badditionally\b", re.I),
    "at_its_core": re.compile(r"\bat\s+its\s+core\b", re.I),
    "in_essence": re.compile(r"\bin\s+essence\b", re.I),
    "fundamentally": re.compile(r"\bfundamentally\b", re.I),
    "crucially": re.compile(r"\bcrucially\b", re.I),
    "notably": re.compile(r"\bnotably\b", re.I),
    "importantly": re.compile(r"\bimportantly\b", re.I),
    "robust_fig": re.compile(r"\brobust\b(?!ness)", re.I),
}


def main():
    pages = []
    for dirpath, dirnames, filenames in os.walk(DOCS):
        if "assets" in dirpath:
            continue
        for fn in sorted(filenames):
            if fn.endswith(".html") and fn not in ("404.html",):
                pages.append(os.path.join(dirpath, fn))
    pages.sort()

    results = {}
    totals = {k: 0 for k in FAMILIES}
    totals_extra = {"words": 0, "strong_prose": 0, "strong_furniture": 0,
                    "strong_td": 0, "li_strong_label": 0, "emdash_heading": 0}

    for path in pages:
        rel = os.path.relpath(path, DOCS)
        p, raw = extract(path)
        if not p.text_nodes:
            continue
        prose = clean_text(p.text_nodes, include_headings=False)
        heading_txt = " ".join(t for t, h, s, c in p.text_nodes if h)
        words = len(prose.split())
        row = {"words": words}
        for k, rx in FAMILIES.items():
            n = len(rx.findall(prose))
            row[k] = n
            totals[k] += n
        # em-dash in headings, separately
        row["emdash_heading"] = len(re.findall(r"—", heading_txt))
        totals_extra["emdash_heading"] += row["emdash_heading"]
        # strong classification
        sp = sf = st = 0
        for containers, parent in p.strong_events:
            if containers & FURNITURE:
                sf += 1
            elif parent == "td":
                st += 1
            else:
                sp += 1
        row["strong_prose"] = sp
        row["strong_furniture"] = sf
        row["strong_td"] = st
        totals_extra["strong_prose"] += sp
        totals_extra["strong_furniture"] += sf
        totals_extra["strong_td"] += st
        # li><strong>Label pattern from raw html
        row["li_strong_label"] = len(re.findall(r"<li>\s*<strong>", raw))
        totals_extra["li_strong_label"] += row["li_strong_label"]
        totals_extra["words"] += words
        results[rel] = row

    out = {"pages": results, "totals": totals, "totals_extra": totals_extra}
    with open(os.path.join(ROOT, "census_out.json"), "w") as f:
        json.dump(out, f, indent=1)

    W = totals_extra["words"]
    print(f"pages={len(results)}  corpus words (prose, ex-headings) = {W}")
    print("\n== corpus totals (per 1k words) ==")
    for k in FAMILIES:
        n = totals[k]
        if n:
            print(f"{k:22s} {n:5d}  {1000*n/W:6.2f}/1k")
    for k in ("strong_prose", "strong_furniture", "strong_td", "li_strong_label", "emdash_heading"):
        n = totals_extra[k]
        print(f"{k:22s} {n:5d}  {1000*n/W:6.2f}/1k")


if __name__ == "__main__":
    main()
