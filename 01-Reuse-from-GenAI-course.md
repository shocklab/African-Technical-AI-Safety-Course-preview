# Reuse audit — what to lift from the "Gen AI in Research" course

The sibling course (repository `shocklab/Generative-AI-in-research-course`, CC-BY-4.0) is a complete, fact-checked, UCT-branded 12-week course. A surprising amount transfers
directly. Items are ranked by how much they save.

## A. Infrastructure & workflow (lift wholesale — biggest time-saver)

1. **The HTML/CSS design system.** UCT-blue (`#003A70`) inline-CSS template with a full component set
   (`.card-grid`, `.highlight-box`, `.warning-box`, `.comparison-table`, `.case-study`,
   `.decision-framework`, `.step-list`, etc.). Documented in the sibling `CLAUDE.md` and
   `Style guide.rtf`. The new course can use the identical look.
2. **The build pipeline.** `build_weekN.py` generator pattern, the `docs/` GitHub-Pages site, and
   `add_page_nav.py` (auto prev/next nav driven by `index.html` order). Clone the repo skeleton.
3. **The `/verify-references` discipline.** The sibling course's hard rule — verify every URL, citation,
   and statistic against primary sources before a week is "done" — matters *more* here, because safety
   content is citation-dense and AI-drafted text hallucinates statistics. Carry the skill over verbatim.
4. **Licensing + citation precedent.** CC-BY-4.0 under UCT IP Policy clauses 8.2 / 9.2.1; the suggested
   citation format. Reuse the exact pattern.
5. **Three-phase weekly structure** (Pre-Class readings → In-Class → Post-Class) and the AI-transparency
   notice convention.

## B. Content reusable with light reframing

| Source (Gen AI course) | Goes to | Reuse level |
|---|---|---|
| **Week 3 — Environmental Implications** (Cost of Every Prompt · Infrastructure & Rebound · Critical Minerals · Sustainable AI) | **Session 4** (physical substrate / energy) + Session 12 (compute governance) | ~90% verbatim; reframe intro for a safety audience ("compute is the governance lever"). |
| **Week 4 — Ethics** (Four Lenses · Ubuntu & RIA Just AI · Transparency/Authorship · Case Studies · The Broader Landscape) | **Session 8** (whose values), **Session 12** (sociotechnical harms), **Session 20** (skeptics) | High. "Four Lenses" + "Ubuntu" → value-specification ethics; "Broader Landscape" (labour, surveillance, military/dual-use, power concentration, deepfakes) → governance/sociotechnical. |
| **Week 2 — LLM Deep Dive** + "Fine-Tuning, RLHF and Alignment" | **Sessions 5–6** (LLM training) | Strong conceptual scaffold; the new course goes deeper/technical on top. |
| **Week 1 — Foundations** (But what is a neural network · 3B1B Transformers · Lightning tour) | **Session 2** (DL recap) | As *optional pre-reading* for rustier students — honours maths cohort needs less. |
| **Week 9 — Critical Evaluation** (Illusions of Understanding · Three Categories of Failure · Verification Protocols) | **Session 20** (skeptics / over-reliance) | "Illusions of Understanding" (Messeri & Crockett, Nature) is a strong critical-thinking reading. |
| **Week 10 — Agentic AI, RAG & Tools** (What agents are · Failure modes for long-horizon tasks · MCP) | **Session 18** (agentic AI & long-horizon risk / agent governance) | Good base; add the safety framing (control, agent governance). |
| **Week 11 — Future / Africa's Sovereign AI** (Sovereign capacity · Data, Languages & African model-building · Policy/Institutions/Talent) | **Session 12** (governance) + **Session 18** (frontier/Africa) | High. Carries the Global South lens that differentiates this course from Northern ones. |

## C. Patterns & assessment

- **The capstone scaffolding** (structured pitch, self-critique) and the idea of an **assessed
  "ethical framework"** component map onto the safety project + the mid-course failure-mode essay.
- **Model-version genericisation** convention (use family names — "Claude (family)", "GPT (family)" —
  except in historical citations) keeps the material from dating. Carry it over.
- **The African-context emphasis as analytical home base** (Mhlambi, Birhane, Esethu Framework, CARE
  Principles, Marivate/Lelapa/Masakhane) — reuse the source bank for the governance/ethics threads.

## D. What does NOT transfer (must be built fresh)

The entire technical-alignment core is new: the alignment-problem formalism, RLHF mechanics at depth,
scalable oversight, the control agenda, mechanistic interpretability, evals tooling (Inspect), and the
technical-governance taxonomy. Sources for all of these are in `02-Open-source-courses-research.md`.
The sibling course is *research-use* oriented (how to use AI as a researcher); this course is
*safety-research* oriented (how these systems fail and how we'd know) — the framing differs even where
topics overlap.

## E. Practical note on the source folder

The sibling "Course materials" directory name carries a trailing carriage-return that breaks paths;
work through a glob-built `/tmp/cm` symlink (one tool call per message during breakage) — see the
project memory note. The reusable HTML lives at `/tmp/cm/week 3/`, `/tmp/cm/Week 4/`, etc.
