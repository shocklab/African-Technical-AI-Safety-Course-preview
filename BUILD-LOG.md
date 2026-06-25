# Build log & status — African Technical AI Safety

Single browsable record of what's built. Also tracked in: **git history** (every change is a
descriptive commit), the **planning docs** (`00`–`05`), and Claude's cross-session memory.
Live site: https://shocklab.github.io/African-Technical-AI-Safety-Course/

## Session status (24 sessions / 12 weeks)

| Wk | Session | Status | Notes |
|----|---------|--------|-------|
| 1 | 1 — What technical AI safety is | ✅ built · deep | 1.1–1.4 |
| 1 | 2 — Deep learning & scaling laws | ✅ built · deep | 2.1–2.5; 2.2 carries figures 2.2a/2.2b |
| 2 | 3 — The core alignment problem | ✅ built · deep | 3.1–3.4 + regressional-Goodhart derivation appendix |
| 2 | 4 — Physical substrate (energy) | ✅ built · deep | 4.1–4.4 (ported from GenAI course) |
| 3 | 5 — Pretraining → assistant | ✅ built · deep | 5.1–5.4 |
| 3 | 6 — RLHF & RL fine-tuning | ✅ built · deep | 6.1–6.5 |
| 4 | 7 — RLAIF & Constitutional AI | ✅ built · deep | 7.1–7.5; papers full-text-verified; lab carries the isiZulu AI-feedback probe |
| 4 | 8 — Scalable oversight & "whose values?" | ✅ built · deep | 8.1–8.4 (8.2/8.3 ported) |
| 5 | 9 — Robustness & adversarial ML | ✅ built · deep | 9.1–9.5; isiZulu robustness lab is the flagship; papers verified |
| 5 | 10 — Unlearning & AI control | ✅ built · deep | 10.1–10.5; control + unlearning; pure-CPU trusted-monitor lab |
| 6 | 11 — Evaluations | 🟡 curriculum drafted | `09-session-11-curriculum.md`; in-language eval lab |
| 6 | 12 — Technical AI governance | ✅ built · deep | single page |
| 7 | 13–14 — Interpretability foundations | ⬜ coming soon | |
| 8 | 15–16 — Interpretability in practice | ⬜ coming soon | |
| 9–12 | 17–24 — Research project phase | ⬜ coming soon | S18 = AI safety from the Global South |

## Design & tooling
- **Design system:** `docs/assets/styles.css` — editorial (Fraunces display + Source Serif 4 body + IBM Plex Mono labels), UCT blue `#003A70`/`#2a5298`, flat, no emoji.
- **`add_page_nav.py`** — sticky top bar (Contents + per-session `<details>` dropdown) + bottom prev/next; reads order from `docs/index.html`; **re-run after adding pages**.
- **`add_mathjax.py`** — MathJax v3 loader injection.
- **`linkify_readings.py`** — turns reading citations into verified links (arXiv-ID regex + a non-arXiv URL map).
- **`restyle_sweep.py`** — emoji strip + sentence-case h1s (one-off; idempotent).
- Standalone pages: `docs/about.html`, `docs/ai-disclaimer.html`.

## Standards (full detail in `CLAUDE.md`)
- Expository pages at textbook depth (~1,500–2,900 words; labs intentionally short ~600–900).
- No decorative emoji; sentence-case titles; every reading a working, verified link; prose run through the de-Claudify (`writing-review`) pass before publishing.

## Log (most recent first)
- **2026-06-25 (later 2)** — Built **Session 10** (Unlearning & the AI-control agenda), 5 sub-sessions: 10.1 machine-unlearning (exact vs approximate; why gradient ascent fails; TOFU's KS-test forget-quality), 10.2 the-control-paradigm (trusted/untrusted; the scale-invariance derivation of upfront auditing), 10.3 control-protocols (safety/usefulness frontier; collusion-as-Bayesian-updating), 10.4 limits (Łucki "suppressed not removed"; the threat-model-accounting discipline), 10.5 lab-trusted-monitor (pure-CPU monitor + collusion game). Papers verified full-text; "obfuscates not erases" framing per sign-off. Nav + MathJax injected (chain 9.5→10.1→…→10.5→S12), de-Claudified. Committed.
- **2026-06-25 (later)** — Built **Session 9** (Robustness & adversarial ML), 5 sub-sessions: 9.1 adversarial-examples (FGSM derivation), 9.2 jailbreaks-as-optimisation (GCG read line-by-line), 9.3 why-safety-training-fails (competing objectives / mismatched generalisation), 9.4 lab-isizulu-robustness (the flagship — measure EN-vs-isiZulu refusal degradation by hand, with CIs + Cohen's κ), 9.5 injection-poisoning-defences. CPU-floor lab + open-weights, full FGSM/GCG maths. Nav + MathJax injected (chain 8.4→9.1→…→9.5→S12), de-Claudified (em-dash density fixed, "Crucially" removed; "robust/robustness" kept as the field's own term). Carlini poisoning kept qualitative (precise figure pending a rate-limited re-verify). Committed.
- **2026-06-25** — Researched + drafted curricula for **Sessions 9–11** (Part III: robustness; unlearning/control; evaluations) via three parallel research agents; load-bearing papers verified full-text. Three curriculum docs written (`07/08/09-session-NN-curriculum.md`), each 5 sub-sessions (4 expository + 1 lab) with a flagship African-lens lab — S9: measure isiZulu refusal degradation by hand; S10: trusted-monitor + collusion game; S11: build an in-language safety eval on open isiZulu data. Awaiting sign-off before building HTML.
- **2026-06-24 (audit)** — Ran a full source-skepticism audit across all built sessions (1–6, 8, 12; eight parallel agents) checking every load-bearing claim against the actual papers/reports. **Sessions 1 and 6 came back clean.** Applied 14 corrections. S2: Chinchilla learning-rate-schedule direction (the bug made under-trained runs look *worse*, not large models look better); Kaplan's compute exponent labelled α_C^min ≈ 0.05 vs the plain α_C ≈ 0.057; Schaeffer "Outstanding Paper" not "best paper"; MLP ≈ two-thirds of *non-embedding* parameters. S3: Shah et al. expression example reworded (the model asks redundant questions, it does not replace computation); Bostrom orthogonality turned into a paraphrase (avoids a contested verbatim quote); mesa etymology; the "~1% superforecaster" figure softened (not in the cited Carlsmith source). S4: LBNL 2023 = 176 TWh / 4.4% (was ~100) and 2028 = 325–580 TWh; IEA AI slice "more than quadrupling" (was "tripling"); data-centre CO₂ under ≈1.5% by 2035 (was ≈1% by 2030); the 223 TWh figure relabelled *total data-centre* (not AI), with the South-Africa comparison de-attributed from Ritchie. S5: FLAN "60+ datasets" not "tasks". S8: RIA Just AI licence is CC BY-NC-SA (page said CC BY 4.0); isiXhosa ≈9M first-language (was "19 million"). S12: Reuel taxonomy has six capacities (added "Ecosystem monitoring"). Tag balance and em-dash density re-verified clean; committed in this pass.
- **2026-06-24 (later)** — Built **Session 7** (RLAIF & Constitutional AI), 5 sub-sessions: 7.1 from-human-to-ai-feedback, 7.2 constitutional-ai (two-phase mechanism + worked critique-and-revise), 7.3 rlaif-and-self-rewarding (Lee/Yuan evidence + four failure modes), 7.4 whose-constitution (Collective CAI, the isiZulu language ceiling, data/feedback sovereignty), 7.5 lab-constitutional-ai (critique/label loop + isiZulu probe). Open choices resolved as recommended: 5 sub-sessions, Lightman omitted, lab CPU-floor with optional GPU extension. Pages authored at depth (1,475–1,921 expository words; lab 787), nav + MathJax injected, `index.html` updated (Session 7 now a built group; prev/next chains 6.5→7.1→…→7.5→8.1), and de-Claudified (em-dash density ≤1/para or genuine pairs, no contrastive reframes, no banned tells — all checked clean). Not yet committed.
- **2026-06-24** — Big polish + depth pass. Linked & verified all readings; editorial restyle + de-Claudify sweep across 33 pages; wired figures 2.2a/2.2b into Session 2.2; added About + full AI-disclaimer pages; sticky top nav + per-session dropdown. Deepened **Tier 1** (2.3, 2.4, 8.1, 8.4) and **Tier 2** (6.1–6.4, 2.1, 12) to textbook depth — all flagged thin expository pages now done. Full site audit passed (35 pages, 0 tag/emoji/internal-link issues; fixed 4 dead external links + 5 residual tells). Researched + drafted the Session 7 curriculum (`06-session-07-curriculum.md`) from a survey of existing courses + verified literature; added this BUILD-LOG. Then **read the load-bearing Session 7 papers in full** (Bai CAI, Lee RLAIF, Yuan self-rewarding, Wataoka self-preference, Huang Collective CAI, Yong LRL-jailbreak) and checked the specific claims against the source text — six confirmed, two wordings corrected (self-preference driver is perplexity/familiarity not self-recognition; "participation-washing" is Sloane's coinage, not Birhane's) — recorded in a source-verification log in the curriculum doc.
- **2026-06-15** — Week 3 built (Sessions 5 & 6).
- **2026-06-11 → 14** — Site set up; Weeks 1–2 + Sessions 4, 8, 12 built; depth + maths-typesetting + reading-verification rollouts.
