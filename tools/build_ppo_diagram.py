#!/usr/bin/env python3
"""Build the PPO / RLHF loop diagram for Session 6.3.

Usage:  python3 tools/build_ppo_diagram.py > docs/assets/img/session-6-3-ppo-loop.svg

Used in 6.3 inside <figure class="wide">, which breaks out of the 880px column.
Re-run after editing any label, then RENDER IT and look at it (rsvg-convert -w 1400),
not just the XML: the first draft validated cleanly and still had four overlaps.

Design intent: students need the LOOP and the leash, not the clipped objective.
So the outer loop is the figure, and PPO's own bookkeeping (the sampling policy
pi_old, the probability ratio, the clip) sits in a separately marked panel that
the caption and the page both tell them they can read past. The three policies
are the specific thing readers confuse, so each is colour-keyed and named once.
"""
import html

NAVY, BLUE, INK, MUTED, RULE, TINT = "#003A70", "#2a5298", "#2c3e50", "#5a6672", "#e4e8ec", "#f5f7f9"
GOLD, WARM = "#8a6d1f", "#fdf7e6"
SERIF = "Source Serif 4, Georgia, 'Times New Roman', serif"
DISPLAY = "Fraunces, Georgia, 'Times New Roman', serif"
MONO = "IBM Plex Mono, ui-monospace, Menlo, Consolas, monospace"
W, H = 1240, 724
o = []
def add(s): o.append(s)
def esc(t): return html.escape(t, quote=False)

def txt(x, y, s, size=12.5, fam=None, fill=INK, anchor="middle", ls=None):
    a = f' letter-spacing="{ls}"' if ls else ""
    add(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam or SERIF}" '
        f'font-size="{size}" fill="{fill}"{a}>{esc(s)}</text>')

def box(x, y, w, h, title, sub=(), stroke=BLUE, fill="#ffffff", extra=None):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="1.6"/>')
    txt(x+w/2, y+28, title, 16.5, DISPLAY, NAVY)
    for i, line in enumerate(sub):
        txt(x+w/2, y+50+i*16, line, 12.5)
    if extra:
        yy = y+50+len(sub)*16+6
        add(f'<line x1="{x+16}" y1="{yy}" x2="{x+w-16}" y2="{yy}" stroke="{RULE}" stroke-width="1"/>')
        for i, line in enumerate(extra):
            txt(x+w/2, yy+18+i*15, line, 11.5, SERIF, GOLD)

def arr(pts, colour=BLUE):
    d = " ".join(("M" if i == 0 else "L") + f"{x} {y}" for i, (x, y) in enumerate(pts))
    add(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="1.6" '
        f'marker-end="url(#ah-{colour.lstrip("#")})"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="{SERIF}">')
add('<defs>')
for c in (BLUE, NAVY, GOLD, MUTED):
    add(f'<marker id="ah-{c.lstrip("#")}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
add('</defs>')
add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

txt(34, 38, "One step of RLHF: the loop, and the leash", 21, DISPLAY, NAVY, "start")
txt(34, 60, "Everything above the dashed line is what the rest of the course uses. "
            "The panel below it is PPO’s own bookkeeping.", 13.5, SERIF, MUTED, "start")

# ---------- outer loop ----------
box(34, 104, 160, 70, "Prompt  x", ["drawn from a prompt set"], stroke=MUTED)
box(234, 96, 200, 88, "πθ   the policy", ["the model being trained,", "started from the SFT model"], stroke=NAVY)
box(474, 104, 190, 70, "Response  y", ["sampled from πθ"], stroke=MUTED)
box(712, 62, 210, 88, "rφ   reward model", ["learned from human", "preferences (6.2)"], stroke=BLUE)
box(712, 186, 210, 88, "πref   frozen SFT", ["never updated; the anchor", "the leash pulls back to"], stroke=GOLD, fill=WARM)
box(968, 96, 232, 148, "Objective", ["rφ(x, y)", "−  β · KL(πθ ‖ πref)"],
    stroke=NAVY, extra=["β is the safety dial: small β", "chases the proxy, large β", "stays close to πref"])

arr([(194, 139), (230, 140)])
arr([(434, 140), (470, 139)])
# split y to both scorers, via a junction so no label sits on a box
add(f'<line x1="664" y1="139" x2="688" y2="139" stroke="{BLUE}" stroke-width="1.6"/>')
add(f'<line x1="688" y1="106" x2="688" y2="230" stroke="{BLUE}" stroke-width="1.6"/>')
arr([(688, 106), (710, 106)])
arr([(688, 230), (710, 230)])
arr([(922, 106), (966, 132)])
arr([(922, 230), (966, 196)])
# update loop, descending clear of the beta callout
arr([(990, 244), (990, 322), (334, 322), (334, 186)], colour=NAVY)
txt(662, 314, "update θ to raise the objective, then repeat", 11.5, MONO, NAVY)

add(f'<line x1="34" y1="352" x2="{W-34}" y2="352" stroke="{RULE}" stroke-width="1.4" stroke-dasharray="7 5"/>')

# ---------- optional panel ----------
PY = 372
add(f'<rect x="34" y="{PY}" width="{W-68}" height="246" rx="8" fill="{TINT}" stroke="{RULE}" '
    f'stroke-width="1.4" stroke-dasharray="7 5"/>')
txt(56, PY+26, "PPO’S BOOKKEEPING · READ PAST THIS ON A FIRST PASS", 10.5, MONO, MUTED, "start", ls=1)
txt(56, PY+49, "Sampling is expensive, so PPO reuses one batch of responses for several gradient "
               "steps. That is the only reason a third policy exists.", 13.5, SERIF, INK, "start")

bx, bw, by, bh = [56, 336, 616, 896], 248, PY+64, 84
box(bx[0], by, bw, bh, "πold   the snapshot", ["a frozen copy of πθ that", "the batch was sampled from"], stroke=MUTED)
box(bx[1], by, bw, bh, "Probability ratio", ["ρ = πθ(y) / πold(y):", "how far θ has drifted"], stroke=MUTED)
box(bx[2], by, bw, bh, "Clip", ["hold ρ inside 1 ± ε so one", "batch cannot move θ far"], stroke=MUTED)
box(bx[3], by, bw, bh, "Advantage  Â", ["was this response better", "than expected?"], stroke=MUTED)
for i in range(3):
    arr([(bx[i]+bw, by+bh/2), (bx[i+1]-2, by+bh/2)], colour=MUTED)
arr([(bx[3]+bw/2, by+bh), (bx[3]+bw/2, by+bh+22), (bx[0]+bw/2, by+bh+22), (bx[0]+bw/2, by+bh+2)], colour=MUTED)
txt(620, by+bh+18, "refresh πold every few steps and go again", 11.5, MONO, MUTED)
txt(56, PY+203, "πold is not πref. πold is refreshed constantly and only keeps the update stable; "
                "πref is frozen for the whole run, and is what the KL penalty measures against.",
    13, SERIF, MUTED, "start")
txt(56, PY+224, "“Better than expected” needs a baseline for what was expected. A second network, the "
                "critic, is trained alongside the policy to supply it.", 13, SERIF, MUTED, "start")

# ---------- legend ----------
txt(34, 658, "THREE POLICIES, ONE JOB EACH", 10.5, MONO, MUTED, "start", ls=1)
for i, (col, sym, s) in enumerate([
        (NAVY, "πθ", "the one being trained"),
        (GOLD, "πref", "frozen; the leash measures distance from it"),
        (MUTED, "πold", "a recent snapshot; PPO detail only")]):
    x = 34 + i*400
    add(f'<rect x="{x}" y="674" width="11" height="11" rx="2" fill="{col}"/>')
    txt(x+19, 684, sym, 12.5, MONO, NAVY, "start")
    txt(x+62, 684, s, 12.5, SERIF, INK, "start")

add('</svg>')
print("\n".join(o))
