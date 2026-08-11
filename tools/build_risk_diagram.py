#!/usr/bin/env python3
"""Build the four-risk-types diagram from Hendrycks, Mazeika & Woodside (2023).

Usage:  python3 tools/build_risk_diagram.py > docs/assets/img/session-1-2-four-risk-types.svg

The figure is used in Session 1.2 inside <figure class="wide">, which breaks it out
of the 880px column; at column width the labels are too small to read. Re-run after
editing any label here, then check the page rather than only the SVG.

Every label below is taken from the paper's own section headings and
Suggestions sections (§2.5, §3.4, §4.3, §5.5), not paraphrased from memory.
Palette follows the course design system (docs/assets/styles.css).
"""
import html

NAVY, BLUE, INK, MUTED, RULE, TINT = "#003A70", "#2a5298", "#2c3e50", "#5a6672", "#e4e8ec", "#f5f7f9"
SERIF = "Source Serif 4, Georgia, 'Times New Roman', serif"
DISPLAY = "Fraunces, Georgia, 'Times New Roman', serif"
MONO = "IBM Plex Mono, ui-monospace, Menlo, Consolas, monospace"

COLUMNS = [
    {
        "n": "§2", "title": "Malicious use",
        "gloss": "People deliberately direct AI at harm. The system works as intended; "
                 "the intent behind it is the hazard.",
        "subtypes": [
            ("Bioterrorism", "§2.1 · lowering the expertise barrier to engineered pathogens"),
            ("Unleashing AI agents", "§2.2 · agents released to pursue open-ended goals"),
            ("Persuasive AIs", "§2.3 · manipulation and tailored disinformation at scale"),
            ("Concentration of power", "§2.4 · surveillance and censorship entrenching a few actors"),
        ],
        "mitigations": [
            "Biosecurity: access controls on bio-capable models, excise biological capability, "
            "plus general biodefence (wastewater monitoring, far-UV, PPE)",
            "Restricted access: structured access via cloud APIs, know-your-customer screening, "
            "compute and export controls, safety case required before open-sourcing",
            "Adversarially robust anomaly detection, as a second line of defence once misuse happens",
            "Legal liability for developers of general-purpose AI, so costs reflect externalities",
        ],
    },
    {
        "n": "§3", "title": "AI race",
        "gloss": "Competition between states and firms makes cutting corners on safety "
                 "individually rational and collectively disastrous.",
        "subtypes": [
            ("Military AI arms race", "§3.1 · autonomous weapons, cyberwarfare, automated warfare"),
            ("Corporate AI race", "§3.2 · economic competition undercuts safety; automated economy"),
            ("Evolutionary pressures", "§3.3 · selection favours the most competitive, not the safest, AI"),
        ],
        "mitigations": [
            "Safety regulation: proactive, not written in blood; independently staffed regulators",
            "Data documentation: report and justify training-data sources",
            "Meaningful human oversight of AI decisions, nuclear command and control above all",
            "AI for cyberdefence, to lower the payoff from AI-enabled attack",
            "International coordination, with verification and enforcement attached",
            "Public control of general-purpose AI: a CERN-like joint effort rather than a race",
        ],
    },
    {
        "n": "§4", "title": "Organizational risks",
        "gloss": "No malice and no race needed. Accidents are normal in complex systems, "
                 "and weak safety culture turns them into catastrophes.",
        "subtypes": [
            ("Accidents are hard to avoid", "§4.1 · Perrow's normal accidents; opaque, unreliable components"),
            ("Weak safety culture", "§4.2 · safety as constraint rather than objective"),
            ("No security mindset", "§4.2 · failure modes that are surprising and unintuitive"),
        ],
        "mitigations": [
            "External red teaming before deployment decisions",
            "Affirmative demonstration of safety: burden of proof on the developer, before training",
            "Deployment procedures: staged release; publication and dual-use review",
            "Response plans for security and safety incidents",
            "Internal auditing and risk management: a chief risk officer, audit team reporting to the board",
            "Safe design principles: defence in depth, redundancy, loose coupling, "
            "separation of duties, fail-safe design",
            "State-of-the-art information security on weights and research IP",
        ],
    },
    {
        "n": "§5", "title": "Rogue AIs",
        "gloss": "Control of the system itself is lost. Inherent to the technology, "
                 "so the response is more technical than social.",
        "subtypes": [
            ("Proxy gaming", "§5.1 · optimising the measurable stand-in, not the goal"),
            ("Goal drift", "§5.2 · goals shifting as the system and its environment change"),
            ("Power-seeking", "§5.3 · resources and self-preservation serve almost any objective"),
            ("Deception", "§5.4 · appearing aligned while pursuing something else"),
        ],
        "mitigations": [
            "Avoid the riskiest use cases: no open-ended real-world goals, no critical infrastructure, "
            "until control is demonstrated",
            "Symmetric international off-switch, agreed across the US, UK and China",
            "Legal liability for cloud compute providers hosting rogue agents",
            "Technical safety research: adversarial robustness of proxy models · model honesty · "
            "transparency and representation engineering · detecting and removing hidden functionality",
        ],
    },
]

FOOT = ("Source: Hendrycks, D., Mazeika, M. & Woodside, T. (2023), “An Overview of Catastrophic "
        "AI Risks”, arXiv:2306.12001. The four risk types and most subtypes are the paper's own "
        "section headings; under organizational risks, weak safety culture and the missing security "
        "mindset are drawn from the discussion in §4.2 rather than being headings. Mitigations "
        "condense the Suggestions sections (§2.5, §3.4, §4.3, §5.5) in the paper's wording.")
CROSS = ("The four are not independent. The paper's §6 argues they compound: a race erodes "
         "organizational safety, weak organizations leak capable models to malicious actors, and "
         "both raise the chance of losing control.")

# ---- layout -----------------------------------------------------------------
COL_W, GAP, MARGIN = 300, 20, 34
TOP = 150
W = MARGIN * 2 + COL_W * 4 + GAP * 3


def wrap(text, width_px, size, weight=400):
    """Greedy wrap using an average glyph width for the serif face."""
    per = size * (0.505 if weight < 600 else 0.53)
    max_chars = max(8, int(width_px / per))
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    return html.escape(s, quote=False)


out = []
add = out.append

# pass 1: measure. The header band must fit the longest gloss, and all four
# mitigation panels start at the same y so their tops line up across the figure.
glosses = [wrap(c["gloss"], COL_W - 36, 11.8) for c in COLUMNS]
HEAD_H = 62 + max(len(g) for g in glosses) * 14 + 12

sub_blocks, sub_heights = [], []
for col in COLUMNS:
    y, items = 26, []          # 26 = "risk subtypes" label
    for name, note in col["subtypes"]:
        nm = wrap(name, COL_W - 54, 15.5, 600)
        nt = wrap(note, COL_W - 54, 12.4)
        items.append((nm, nt, y))
        y += len(nm) * 19 + len(nt) * 15 + 14
    sub_blocks.append(items)
    sub_heights.append(y)

MIT_Y = max(sub_heights) + 20  # shared start of the mitigations panel

col_bodies, heights = [], []
for idx, col in enumerate(COLUMNS):
    y = MIT_Y + 26             # 26 = "mitigations" label
    mits = []
    for m in col["mitigations"]:
        ln = wrap(m, COL_W - 54, 12.8)
        mits.append((ln, y))
        y += len(ln) * 16.5 + 11
    col_bodies.append((sub_blocks[idx], MIT_Y, mits))
    heights.append(y)

BODY_H = max(heights) + 20
BOX_H = HEAD_H + BODY_H
H = TOP + BOX_H + 130

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="{SERIF}" role="img" aria-label="The four types of catastrophic AI risk, '
    f'their subtypes and mitigations, after Hendrycks, Mazeika and Woodside 2023">')
add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

# title block
add(f'<text x="{MARGIN}" y="52" font-family="{DISPLAY}" font-size="30" fill="{NAVY}">'
    f'Four types of catastrophic AI risk</text>')
add(f'<text x="{MARGIN}" y="78" font-family="{MONO}" font-size="11.5" fill="{BLUE}" '
    f'letter-spacing="1.6">HENDRYCKS, MAZEIKA &amp; WOODSIDE (2023) · ARXIV:2306.12001</text>')
sub = ("Each column is one of the paper's four risk sources, with the subtypes it names and the "
       "mitigations it proposes. Read across: the first three are about people and institutions, "
       "the fourth about the system itself.")
for i, ln in enumerate(wrap(sub, W - MARGIN * 2, 14)):
    add(f'<text x="{MARGIN}" y="{104 + i * 19}" font-size="14" fill="{MUTED}">{esc(ln)}</text>')

for idx, col in enumerate(COLUMNS):
    x = MARGIN + idx * (COL_W + GAP)
    items, mit_y, mits = col_bodies[idx]
    add(f'<rect x="{x}" y="{TOP}" width="{COL_W}" height="{BOX_H}" fill="#ffffff" '
        f'stroke="{RULE}" stroke-width="1"/>')
    # header band
    add(f'<rect x="{x}" y="{TOP}" width="{COL_W}" height="{HEAD_H}" fill="{NAVY}"/>')
    add(f'<text x="{x + 18}" y="{TOP + 26}" font-family="{MONO}" font-size="10.5" '
        f'fill="#9dc0e8" letter-spacing="1.6">{col["n"]}</text>')
    add(f'<text x="{x + 18}" y="{TOP + 50}" font-family="{DISPLAY}" font-size="19" fill="#ffffff">'
        f'{esc(col["title"])}</text>')
    for i, ln in enumerate(glosses[idx]):
        add(f'<text x="{x + 18}" y="{TOP + 68 + i * 14}" font-size="11.8" fill="#cddcee">'
            f'{esc(ln)}</text>')
    # subtypes
    by = TOP + HEAD_H
    add(f'<text x="{x + 18}" y="{by + 22}" font-family="{MONO}" font-size="9.6" fill="{BLUE}" '
        f'letter-spacing="1.5">RISK SUBTYPES</text>')
    for nm, nt, y0 in items:
        yy = by + y0 + 20
        add(f'<circle cx="{x + 22}" cy="{yy - 5}" r="3" fill="{BLUE}"/>')
        for i, ln in enumerate(nm):
            add(f'<text x="{x + 34}" y="{yy + i * 19}" font-size="15.5" font-weight="600" '
                f'fill="{INK}">{esc(ln)}</text>')
        for i, ln in enumerate(nt):
            add(f'<text x="{x + 34}" y="{yy + len(nm) * 19 + i * 15 - 2}" font-size="12.4" '
                f'fill="{MUTED}">{esc(ln)}</text>')
    # mitigations panel
    my = by + mit_y
    add(f'<rect x="{x + 1}" y="{my}" width="{COL_W - 2}" height="{TOP + BOX_H - my - 1}" '
        f'fill="{TINT}"/>')
    add(f'<rect x="{x + 1}" y="{my}" width="3" height="{TOP + BOX_H - my - 1}" fill="{BLUE}"/>')
    add(f'<text x="{x + 18}" y="{my + 24}" font-family="{MONO}" font-size="9.6" fill="{BLUE}" '
        f'letter-spacing="1.5">MITIGATIONS</text>')
    for ln, y0 in mits:
        yy = by + y0 + 20
        add(f'<text x="{x + 18}" y="{yy}" font-size="12.8" fill="{BLUE}">→</text>')
        for i, l in enumerate(ln):
            add(f'<text x="{x + 32}" y="{yy + i * 16.5}" font-size="12.8" fill="{INK}">'
                f'{esc(l)}</text>')

# cross-cutting note + source
cy = TOP + BOX_H + 34
add(f'<rect x="{MARGIN}" y="{cy - 20}" width="{W - MARGIN * 2}" height="46" fill="{TINT}"/>')
add(f'<rect x="{MARGIN}" y="{cy - 20}" width="3" height="46" fill="{NAVY}"/>')
for i, ln in enumerate(wrap(CROSS, W - MARGIN * 2 - 40, 13)):
    add(f'<text x="{MARGIN + 18}" y="{cy + i * 17}" font-size="13" fill="{INK}">{esc(ln)}</text>')
fy = cy + 60
for i, ln in enumerate(wrap(FOOT, W - MARGIN * 2, 11.6)):
    add(f'<text x="{MARGIN}" y="{fy + i * 15}" font-size="11.6" fill="{MUTED}">{esc(ln)}</text>')

add('</svg>')
print("\n".join(out))
