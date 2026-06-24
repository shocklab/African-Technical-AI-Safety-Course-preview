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
| 4 | 7 — RLAIF & Constitutional AI | 🟡 curriculum drafted | `06-session-07-curriculum.md`; awaiting sign-off, then build |
| 4 | 8 — Scalable oversight & "whose values?" | ✅ built · deep | 8.1–8.4 (8.2/8.3 ported) |
| 5 | 9 — Robustness & adversarial ML | ⬜ coming soon | isiZulu-jailbreak flagship |
| 5 | 10 — Unlearning & AI control | ⬜ coming soon | |
| 6 | 11 — Evaluations | ⬜ coming soon | |
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
- **2026-06-24** — Big polish + depth pass. Linked & verified all readings; editorial restyle + de-Claudify sweep across 33 pages; wired figures 2.2a/2.2b into Session 2.2; added About + full AI-disclaimer pages; sticky top nav + per-session dropdown. Deepened **Tier 1** (2.3, 2.4, 8.1, 8.4) and **Tier 2** (6.1–6.4, 2.1, 12) to textbook depth — all flagged thin expository pages now done. Full site audit passed (35 pages, 0 tag/emoji/internal-link issues; fixed 4 dead external links + 5 residual tells). Researched + drafted the Session 7 curriculum (`06-session-07-curriculum.md`) from a survey of existing courses + verified literature; added this BUILD-LOG.
- **2026-06-15** — Week 3 built (Sessions 5 & 6).
- **2026-06-11 → 14** — Site set up; Weeks 1–2 + Sessions 4, 8, 12 built; depth + maths-typesetting + reading-verification rollouts.
