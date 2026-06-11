#!/usr/bin/env python3
"""
build_subsessions.py — port reused lesson content from the Generative-AI-in-research
course into this course's sub-session pages, in the shared design system.

It takes each source page's inner <div class="content"> body VERBATIM (the source
is already fact-checked), strips the source's own head/header/ai-notice, and wraps
it in this course's template (shared stylesheet, back-nav, new header badge/title).
Per-page regex fixes repair stale cross-references; extra_top/extra_bottom add the
safety framing. After writing, it scans output for any remaining "Week N / this week"
references so they can be tidied.

Run:  python3 build_subsessions.py
Then: python3 add_page_nav.py   (to (re)build prev/next nav)
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = Path("/tmp/cm")  # symlink to the GenAI course "Course materials" dir
OUT = ROOT / "docs" / "sessions"

AI_NOTICE = (
    "<strong>Note:</strong> This page reuses and adapts fact-checked content from the "
    "Generative AI in Research course (CC BY 4.0), restyled and reframed for this course "
    "with Claude (Anthropic's AI assistant). Spot an error? Email jonathan.shock@uct.ac.za."
)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_tag}</title>
    <link rel="stylesheet" href="https://s.brightspace.com/lib/fonts/0.6.1/fonts.css">
    <link rel="stylesheet" href="../../assets/styles.css">
</head>
<body>
<div class="container">
    <div class="back-nav"><a href="../../index.html">← Back to course contents</a></div>
    <div class="ai-notice">{ai_notice}</div>
    <header>
        <div class="week-badge">{badge}</div>
        <h1>{h1}</h1>
        <p>{subtitle}</p>
    </header>
    <div class="content">
{extra_top}{content}
{extra_bottom}    </div>
</div>
</body>
</html>
"""


def extract_content(html: str) -> str:
    open_tag = '<div class="content">'
    start = html.find(open_tag) + len(open_tag)
    body = html.find("</body>")
    container_close = html.rfind("</div>", 0, body)
    content_close = html.rfind("</div>", 0, container_close)
    return html[start:content_close].strip("\n")


# --- framing snippets -------------------------------------------------------
BANNER_S4 = """        <div class="highlight-box">
            <h3>⚡ <span style="color:#ffffff;">Session 4 — the physical substrate of scale</span></h3>
            <p>Capability is bought with compute; compute is bought with energy, water, hardware and minerals. Why a <em>safety</em> course counts kilowatts: <strong>compute is the capability floor</strong>, which makes it the <strong>main governance lever</strong> (Session 12) — and its costs fall unevenly, disproportionately on the Global South.</p>
            <p style="margin-bottom:0;"><strong>This session's sub-sessions:</strong> 4.1 the cost of every prompt · 4.2 infrastructure &amp; the rebound problem · 4.3 critical minerals · 4.4 sustainable &amp; sovereign AI.</p>
        </div>
"""

BRIDGE_S4 = """        <div class="decision-framework">
            <h4>🧭 From substrate to governance</h4>
            <p style="color:#555; line-height:1.8;">Hold onto one chain for Session 12: <strong>capability ← compute ← chips + energy</strong>. Each arrow is a place a governance regime could intervene and <em>verify</em> — which is why "compute governance" is one of the few technical-governance proposals with concrete, measurable hooks. And from an African vantage point: if the levers (chips, fabs, hyperscale data centres) sit elsewhere, "sovereign AI capacity" is first a question about access to this physical substrate.</p>
            <p style="color:#555; margin-top:10px;"><strong>Next (Week 3, Sessions 5–6):</strong> how a frontier model is actually trained — pretraining, SFT, and the RLHF/RL fine-tuning that turns a predictor into an assistant.</p>
        </div>
"""

NOTE_S8 = """        <div class="info-box">
            <h4>💡 Why this sits in a technical safety course</h4>
            <p>Session 8 asks how to oversee a system smarter than us (8.1) and then — its harder half — <em>what to oversee it toward</em>. "Aligned" is a relation to a target, and the target is a values choice. The four lenses below are the tool for reasoning about that choice; 8.3 brings in Ubuntu and relational ethics; 8.4 shows the choice is also a mathematical constraint.</p>
        </div>
"""

# --- jobs -------------------------------------------------------------------
JOBS = [
    dict(
        src=SRC / "week 3" / "The Cost of Every Prompt.html",
        out=OUT / "session-04" / "cost-of-every-prompt.html",
        badge="Week 2 • Session 4.1",
        h1='⚡ <span style="color:#ffffff;">The Cost of Every Prompt</span>',
        subtitle="Energy, water and the agentic multiplier — per interaction and at deployment scale",
        title_tag="Session 4.1 — The Cost of Every Prompt",
        extra_top=BANNER_S4,
        regex_subs=[
            (r"A Note on Numbers Throughout This Week", "A Note on Numbers Throughout This Session"),
            (r"Next session \(Week 3\.2\):", "Next (4.2):"),
        ],
    ),
    dict(
        src=SRC / "week 3" / "Infrastructure, Scale and the Rebound Problem.html",
        out=OUT / "session-04" / "infrastructure-and-rebound.html",
        badge="Week 2 • Session 4.2",
        h1='🏭 <span style="color:#ffffff;">Infrastructure, Scale and the Rebound Problem</span>',
        subtitle="Data centres, grids, embodied carbon, and why efficiency hasn't reduced total demand",
        title_tag="Session 4.2 — Infrastructure, Scale and the Rebound Problem",
        regex_subs=[(r"Next session \(Week 3\.3\):", "Next (4.3):")],
    ),
    dict(
        src=SRC / "week 3" / "Critical Minerals and AI.html",
        out=OUT / "session-04" / "critical-minerals.html",
        badge="Week 2 • Session 4.3",
        h1='⛏️ <span style="color:#ffffff;">Critical Minerals and the Hardware Supply Chain</span>',
        subtitle="From mine to data centre to e-waste — and why concentration is also a governance lever",
        title_tag="Session 4.3 — Critical Minerals and AI",
        regex_subs=[
            (r"Next session \(Week 3\.4\):", "Next (4.4):"),
            (r"We bring the week together", "We bring the session together"),
        ],
    ),
    dict(
        src=SRC / "week 3" / "Sustainable AI - Practices and Possibilities.html",
        out=OUT / "session-04" / "sustainable-and-sovereign-ai.html",
        badge="Week 2 • Session 4.4",
        h1='🌱 <span style="color:#ffffff;">Sustainable &amp; Sovereign AI</span>',
        subtitle="Measuring and reducing your footprint, AI for the environment, policy, and the African substrate",
        title_tag="Session 4.4 — Sustainable & Sovereign AI",
        extra_bottom=BRIDGE_S4,
        regex_subs=[
            (r"📚 Week 3 Summary: Environmental Implications of AI",
             "📚 Session 4 summary: the physical substrate of scale"),
            (r"<p[^>]*><strong>Next week \(Week 4\):</strong>.*?</p>",
             '<p style="margin-top: 20px;"><strong>See the session bridge below</strong> for where this leads in the course.</p>'),
            (r"Across the four sessions this week", "Across the four sub-sessions of Session 4"),
        ],
    ),
    dict(
        src=SRC / "Week 4" / "Ethical Frameworks and Four Lenses.html",
        out=OUT / "session-08" / "ethical-frameworks-four-lenses.html",
        badge="Week 4 • Session 8.2",
        h1='⚖️ <span style="color:#ffffff;">Ethical Frameworks &amp; the Four Lenses</span>',
        subtitle="Four philosophical lenses for reasoning about the alignment target",
        title_tag="Session 8.2 — Ethical Frameworks and the Four Lenses",
        extra_top=NOTE_S8,
        regex_subs=[(r"Readings for This Week", "Readings for this session"),
                    (r"\bthis week\b", "this session"),
                    (r"\bThis week\b", "This session")],
    ),
    dict(
        src=SRC / "Week 4" / "Ubuntu and Relational Ethics.html",
        out=OUT / "session-08" / "ubuntu-relational-ethics.html",
        badge="Week 4 • Session 8.3",
        h1='🤝 <span style="color:#ffffff;">Ubuntu, Relational Ethics &amp; the Just AI Framework</span>',
        subtitle="A relational reframing of the alignment target, grounded in African philosophy",
        title_tag="Session 8.3 — Ubuntu, Relational Ethics and the Just AI Framework",
        regex_subs=[(r"\bthis week\b", "this session"),
                    (r"examined in detail in Week 3", "examined in detail in Session 4")],
    ),
]

STALE = re.compile(r"(Week\s+\d|[Nn]ext week|[Tt]his week)")


def main():
    for job in JOBS:
        html = job["src"].read_text(encoding="utf-8")
        content = extract_content(html)
        content = content.replace("<h2>What We'll Cover</h2>", "<h2>🎯 What We'll Cover</h2>")
        for pat, repl in job.get("regex_subs", []):
            content = re.sub(pat, repl, content, flags=re.DOTALL)
        page = TEMPLATE.format(
            title_tag=job["title_tag"], ai_notice=AI_NOTICE, badge=job["badge"],
            h1=job["h1"], subtitle=job["subtitle"],
            extra_top=job.get("extra_top", ""), content=content,
            extra_bottom=job.get("extra_bottom", ""),
        )
        job["out"].parent.mkdir(parents=True, exist_ok=True)
        job["out"].write_text(page, encoding="utf-8")
        rel = job["out"].relative_to(ROOT)
        imgs = content.count("<img")
        flags = [f"{m.start()}:{m.group(0)}" for m in STALE.finditer(content)]
        print(f"✓ {rel}  ({len(content)} chars, {imgs} img)")
        if flags:
            print(f"    ⚠ stale refs: {flags}")


if __name__ == "__main__":
    main()
