# African Technical AI Safety — Honours / 4th-year course (UCT, Dept. of Maths & Applied Maths)

> **Repo:** https://github.com/shocklab/African-Technical-AI-Safety-Course (public, CC BY 4.0)
> **Live site:** https://shocklab.github.io/African-Technical-AI-Safety-Course/ (GitHub Pages, `/docs` on `main`)
> Local working folder may differ from the repo name.

A 12-week technical AI safety course, two sessions per week (24 sessions), for fourth-year /
honours students who understand neural networks and can program in Python. Backgrounds will vary,
so the first week levels the ML foundation before the safety content proper.

This folder currently holds **planning documents only** (no lesson pages built yet). The companion
"Generative AI in Research" course (sibling folder) has a complete HTML/CSS design system, a
GitHub-Pages build pipeline, and a reference-verification workflow that this course can reuse
wholesale — see the reuse audit.

## Documents

| File | What it is |
|------|------------|
| [`00-Course-plan.md`](00-Course-plan.md) | The full 12-week / 24-session plan: the high-level shape, the four through-lines, and a proposed assessment scheme. **Start here.** |
| [`03-Detailed-session-plans.md`](03-Detailed-session-plans.md) | Each of the 24 sessions expanded: objectives, pre-class readings, lab/seminar spec, discussion questions, and a build order. |
| [`04-African-AI-safety.md`](04-African-AI-safety.md) | How African AI safety is folded through the whole course (not a single week): the flagship multilingual-jailbreak hook, a session-by-session thread, guest candidates, open Colab-runnable African resources, and integrity caveats. |
| [`01-Reuse-from-GenAI-course.md`](01-Reuse-from-GenAI-course.md) | What can be lifted from the existing "Gen AI in Research" course — ethics, energy, LLM-training, the design system, and the build/verify workflow. |
| [`02-Open-source-courses-research.md`](02-Open-source-courses-research.md) | The open-source technical AI safety curricula surveyed (BlueDot, Hendrycks/CAIS, ARENA, Grosse/Toronto, Stanford, Princeton, Berkeley, Oxford), with links, licences, and what each contributes. |

## Design principles (carried from the sibling course + Jonathan's preferences)

- **Honest about uncertainty.** The field disagrees with itself; a dedicated "steelman the
  skeptics" session is built in, and skeptical readings sit alongside advocacy throughout.
- **Maths-first sequencing.** Idealised, formal models of agency come *before* messy empirical
  alignment (the Grosse two-act structure), because that plays to the cohort's strengths.
- **Hands-on where it counts.** Mechanistic interpretability, evals, and robustness have real
  coding labs (TransformerLens, UK AISI Inspect, ARENA notebooks).
- **African AI safety as a technical through-line.** Not a single week: the anchor is that frontier
  models are *measurably less safe in African languages* (multilingual jailbreaks defeat guardrails in
  isiZulu), making this a robustness/evals problem at the core — plus compute/data sovereignty,
  relational ethics, and the present-harms critique. "Whose safety, whose risks, whose values?" runs
  throughout. See [`04-African-AI-safety.md`](04-African-AI-safety.md).
- **A substantial project.** Roughly the final third is a scoped research/engineering project with
  a short-paper + code deliverable.

## Status / decisions (confirmed 2026-06-11)

- **Intensity:** balanced — ≈1 coding lab/week + paper seminars.
- **Project:** 3–4 weeks.
- **Compute:** Google Colab is the floor; labs are written Colab-friendly and GPU-only labs are marked
  `[GPU — optional/demo]` so nothing graded depends on hardware students may lack.
- **Next:** detailed per-session plans — done, see [`03-Detailed-session-plans.md`](03-Detailed-session-plans.md).

- **African lens wired into assessment** (see `00-Course-plan.md`): a mandatory one-paragraph context
  statement on every project, an African-context track for the failure-mode essay, the isiZulu jailbreak
  flagship project, and peer review of positioning.
- **Session 18 reading list** drafted and reference-checked — `05-reading-lists.md` (verification log included).

### Public site (`docs/` → GitHub Pages, as the GenAI course)

`docs/` is a GitHub-Pages-ready static site mirroring the sibling course's UCT design (shared
`assets/styles.css` rather than per-page inline CSS, since there's no Brightspace target here).

- `docs/index.html` — **the contents page** (single source of truth for session order): all 12 weeks ×
  2 sessions, built lessons linked, rest "coming soon".
- `docs/sessions/` — built lessons so far. **Sessions can have sub-sessions** (own folder, multiple
  pages):
  - **Session 4** (`session-04/`) — physical substrate/energy, 4 sub-sessions: cost of every prompt ·
    infrastructure & rebound · critical minerals · sustainable & sovereign AI.
  - **Session 8** (`session-08/`) — scalable oversight & whose values, 4 sub-sessions: supervision gap ·
    four lenses · Ubuntu/relational ethics · whose values.
  - **Session 12** — technical AI governance (single page).
- **`build_subsessions.py`** ports reused content from the GenAI course (Weeks 3 & 4) *verbatim* into
  Sessions 4.1–4.4, 8.2, 8.3 — preserving its fact-checking — restyled into the shared design system,
  with stale cross-references auto-fixed and the safety framing added. Sessions 8.1 and 8.4 are
  hand-authored. Re-run it to regenerate those ported pages (then re-run `add_page_nav.py`).
- **Prev/Next nav:** every built page carries a "← Previous / ⌂ / Next →" bar injected by
  `add_page_nav.py`, which reads the order from `docs/index.html` and computes correct relative paths
  across sub-session folders. **Re-run `python3 add_page_nav.py` after building/reordering pages**
  (use `--check` for a dry run). It chains only *built* (linked) pages and is idempotent.

**Deployed.** Repo `shocklab/African-Technical-AI-Safety-Course` (public), GitHub Pages serving `/docs`
on `main` at the live URL above. To update: edit `docs/`, run `python3 add_page_nav.py`, commit and push
to `main` — Pages redeploys automatically.

Still open: exact assessment weights vs faculty norms; building the remaining 21 session pages (re-run
`add_page_nav.py` after each batch, then commit/push).
