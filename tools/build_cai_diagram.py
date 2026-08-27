#!/usr/bin/env python3
"""Build the Constitutional AI pipeline diagram for Session 7.2.

Usage:  python3 tools/build_cai_diagram.py > docs/assets/img/session-7-2-cai-pipeline.svg

Used in 7.2 inside <figure class="wide">. RENDER IT AND LOOK AT IT after any edit
(rsvg-convert -w 1400). The 6.3 PPO diagram validated as clean XML on its first
draft and still had four label-on-box collisions that only appeared on screen.

Design intent, following Jonathan's depth rule for the PPO figure: the reader needs
the two phases, the fact that the Phase-2 judge is NOT the model being trained, and
the two data streams meeting at one preference model. Everything drawn in the muted
style is detail they can pass over.

Every claim here is from Bai et al. (2212.08073), checked rather than recalled:
  - Phase 1 starts from a helpful RLHF model that critiques and revises ITS OWN output
  - SL-CAI finetunes a pretrained model on the revisions, mixed with helpful samples
    "in order to retain helpfulness as much as possible"
  - the Phase-2 judge is "an independent model, called the feedback model
    (typically a pretrained LM)"
  - the PM is a "hybrid human/AI PM": human labels for helpfulness, AI for harmlessness
"""
import html

NAVY, BLUE, INK, MUTED, RULE, TINT = "#003A70", "#2a5298", "#2c3e50", "#5a6672", "#e4e8ec", "#f5f7f9"
GOLD, WARM, GREEN, COOL = "#8a6d1f", "#fdf7e6", "#3f6b52", "#eef4f0"
SERIF = "Source Serif 4, Georgia, 'Times New Roman', serif"
DISPLAY = "Fraunces, Georgia, 'Times New Roman', serif"
MONO = "IBM Plex Mono, ui-monospace, Menlo, Consolas, monospace"
W, H = 1240, 812
o = []
def add(s): o.append(s)
def esc(t): return html.escape(t, quote=False)

def txt(x, y, s, size=12.5, fam=None, fill=INK, anchor="middle", ls=None):
    a = f' letter-spacing="{ls}"' if ls else ""
    add(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam or SERIF}" '
        f'font-size="{size}" fill="{fill}"{a}>{esc(s)}</text>')

def box(x, y, w, h, title, sub=(), stroke=BLUE, fill="#ffffff", dash=None, tsize=15.5):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="1.6"{d}/>')
    txt(x+w/2, y+25, title, tsize, DISPLAY, NAVY)
    for i, line in enumerate(sub):
        txt(x+w/2, y+45+i*15, line, 12, SERIF, INK)

def arr(pts, colour=BLUE, dash=None):
    d = " ".join(("M" if i == 0 else "L") + f"{x} {y}" for i, (x, y) in enumerate(pts))
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="1.6" '
        f'marker-end="url(#ah-{colour.lstrip("#")})"{da}/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{SERIF}">')
add('<defs>')
for c in (BLUE, NAVY, GOLD, MUTED, GREEN):
    add(f'<marker id="ah-{c.lstrip("#")}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
add('</defs>')
add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

txt(34, 38, "Constitutional AI, end to end", 21, DISPLAY, NAVY, "start")
txt(34, 60, "Two phases. The model that judges in Phase 2 is not the model being trained, and the "
            "preference model is fed from two streams.", 13.5, SERIF, MUTED, "start")

# ---------- the constitution, feeding both phases ----------
box(34, 96, 178, 92, "The constitution", ["a short list of written", "principles; one is sampled", "at each step"], stroke=GREEN, fill=COOL)

# ---------- PHASE 1 ----------
add(f'<rect x="238" y="88" width="{W-272}" height="248" rx="8" fill="{TINT}" stroke="{RULE}" stroke-width="1.4"/>')
txt(258, 112, "PHASE 1 · SUPERVISED (SL-CAI)", 10.5, MONO, MUTED, "start", ls=1)

box(258, 126, 168, 88, "Helpful-only model", ["answers a red-team", "prompt, then critiques", "and revises its own answer"], stroke=BLUE)
add(f'<path d="M342 214 L342 238 L300 238 L300 214" fill="none" stroke="{BLUE}" stroke-width="1.6" marker-end="url(#ah-{BLUE.lstrip("#")})"/>')
txt(390, 244, "repeat a few times", 11, MONO, MUTED)

box(470, 126, 158, 68, "Final revisions", ["the harmless answers"], stroke=MUTED)
box(470, 214, 158, 68, "Helpful samples", ["from the same model,", "on ordinary prompts"], stroke=MUTED, dash="5 4")

box(676, 152, 190, 96, "Supervised fine-tuning", ["on both sets, of a", "pretrained model: not", "the one that wrote them"], stroke=NAVY, tsize=14.5)
box(910, 166, 156, 68, "SL-CAI", ["the Phase-1 model"], stroke=NAVY)

arr([(212, 142), (256, 158)], colour=GREEN)
arr([(426, 152), (468, 152)])
arr([(426, 190), (468, 236)])
arr([(628, 158), (674, 184)], colour=MUTED)
arr([(628, 248), (674, 222)], colour=MUTED, dash="5 4")
arr([(866, 200), (908, 200)], colour=NAVY)
txt(739, 312, "the helpful samples are why the result does not collapse into refusing everything", 12, SERIF, MUTED)

# ---------- PHASE 2 ----------
add(f'<rect x="238" y="360" width="{W-272}" height="300" rx="8" fill="{TINT}" stroke="{RULE}" stroke-width="1.4"/>')
txt(258, 384, "PHASE 2 · REINFORCEMENT LEARNING (RL-CAI)", 10.5, MONO, MUTED, "start", ls=1)

box(258, 398, 158, 68, "SL-CAI", ["samples two answers", "to each prompt"], stroke=NAVY)
box(258, 500, 158, 92, "Feedback model", ["a separate model,", "typically a pretrained", "one. Not the trainee."], stroke=GOLD, fill=WARM)
box(470, 442, 176, 78, "Soft label", ["p(A) from the option", "log-probabilities"], stroke=MUTED)

box(694, 398, 196, 72, "AI comparisons", ["harmlessness"], stroke=GOLD, fill=WARM)
box(694, 496, 196, 72, "Human comparisons", ["helpfulness"], stroke=GREEN, fill=COOL)
box(938, 434, 128, 100, "Preference model", ["one hybrid model:", "AI harmlessness,", "human helpfulness"], stroke=NAVY, tsize=13)

arr([(416, 432), (468, 460)], colour=NAVY)
arr([(416, 528), (468, 500)], colour=GOLD)
arr([(212, 150), (224, 150), (224, 546), (256, 546)], colour=GREEN)
arr([(646, 470), (692, 440)], colour=MUTED)
arr([(890, 428), (936, 462)], colour=GOLD)
arr([(890, 526), (936, 500)], colour=GREEN)

add(f'<path d="M1002 534 L1002 618 L248 618 L248 432 L254 432" fill="none" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#ah-{NAVY.lstrip("#")})"/>')
txt(676, 612, "optimise SL-CAI against it with PPO, under the KL leash of 6.3", 11.5, MONO, NAVY)
txt(676, 644, "the constitution does not appear in the RL step itself: it is already inside the reward model", 12, SERIF, MUTED)

# ---------- legend ----------
txt(34, 700, "WHICH MODEL IS WHICH", 10.5, MONO, MUTED, "start", ls=1)
for i, (col, fillc, name, role) in enumerate([
        (BLUE, "#ffffff", "Helpful-only model", "writes and revises in Phase 1"),
        (NAVY, "#ffffff", "The model being trained", "pretrained → SL-CAI → RL-CAI"),
        (GOLD, WARM, "Feedback model", "judges in Phase 2; never trained here"),
        (GREEN, COOL, "Human input", "the constitution and the helpfulness labels")]):
    y = 720 + (i // 2) * 40
    x = 34 + (i % 2) * 600
    add(f'<rect x="{x}" y="{y}" width="13" height="13" rx="2" fill="{fillc}" stroke="{col}" stroke-width="1.8"/>')
    txt(x+22, y+11, name, 12.5, DISPLAY, NAVY, "start")
    txt(x+192, y+11, role, 12.5, SERIF, INK, "start")

add('</svg>')
print("\n".join(o))
