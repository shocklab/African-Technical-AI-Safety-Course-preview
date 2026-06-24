# Session 7 — Learning from AI Feedback (RLAIF & Constitutional AI)

**Week 4, Session 1** (Session 8 is the second). Status: curriculum drafted 2026-06-24 from a
deep-dive survey of existing courses + verified literature. Awaiting sign-off before building HTML.

## Where it sits, and the gap it fills

Session 6 ended on a wall: RLHF is bounded by what human raters can evaluate (6.4), and human
labels are expensive and slow. Session 7 is the dominant **industrial response** to that wall —
replace (most of) the human feedback with **AI feedback** guided by a written **constitution** —
taught as mechanism, mathematics, and critique. It then hands directly to Session 8, which takes
up the two questions it raises: *can model-assisted oversight scale?* (8.1) and *whose values?* (8.4).

**Coherence guardrails (do not duplicate):**
- The KL-constrained RLHF objective, its closed-form optimum, and the DPO reparameterisation are **already in 6.3** — Session 7 *uses* them, doesn't re-derive them.
- The scalable-oversight menu (debate, amplification, recursive reward modelling, weak-to-strong, sandwiching) is **already in 8.1** — Session 7 motivates it and points forward.
- Arrow / preference aggregation / social choice is **already in 8.4** — Session 7 raises "whose constitution?" and hands the formal argument to 8.4.

**What the survey showed we can offer that others don't:** a maths-honest treatment of the
AI-feedback pivot, and a hands-on **Constitutional-AI lab** (critique-and-revise + AI preference
labelling) — which exists in *no* surveyed course (ARENA's RLHF lab stops at a hand-coded reward).

## Session-level learning objectives

By the end, a student can:
1. Explain *why* the field moved from human to AI feedback, and state precisely what human input remains.
2. Describe the **two phases of Constitutional AI** (supervised critique-and-revise; RL from AI feedback) and how plain **RLAIF** generalises the second phase.
3. Summarise the empirical evidence that AI feedback can match human feedback (Lee et al.), and the "superhuman feedback" motivation behind self-rewarding models.
4. Enumerate the **new failure modes** AI feedback introduces (self-preference bias, sycophancy/bias transfer, over-optimisation of an AI proxy, recursive model-collapse) and argue whether AI feedback *escapes* or merely *relocates* the oversight ceiling.
5. Critique "whose constitution?" — democratic value-setting (Collective CAI) and the African-language safety gap — and connect it to Sessions 8.1 and 8.4.
6. (Lab) Implement a minimal critique-and-revise loop and an AI-preference-labelling step, and probe how the AI feedback degrades outside English.

## Proposed structure — 5 sub-sessions (4 expository + 1 lab)

Mirrors the Session 5/6 rhythm. (Could split 7.3 into two for a 6-page version — see "open choices".)

### 7.1 — From human to AI feedback
- **Objectives:** motivate the pivot; name exactly what changes and what stays human.
- **Content:** recap the 6.4 ceiling + the throughput/cost limit of human labels; the core move — a model supplies the feedback, steered by a short written list of principles; the two live questions (escape-or-relocate the ceiling? whose principles?) that the session and Session 8 answer. The "only human oversight is the constitution" claim, stated and held up for scrutiny.
- **Readings:** Bai et al. 2022 (CAI, `2212.08073`) — intro/§1; recap Casper et al. (`2307.15217`, from 6.4).
- **African lens:** flag early that "whose principles" lands North by default; foreshadow 7.4.

### 7.2 — Constitutional AI: critique, revise, and RL from AI feedback
- **Objectives:** the centrepiece mechanism, end to end.
- **Content:** **Phase 1 (SL-CAI, critique-and-revise):** a helpful-only model answers a red-team prompt → critiques its own answer against a sampled constitutional principle → revises → iterate → supervised-finetune on the revised answers. **Phase 2 (RL-CAI / RLAIF):** sample response pairs → an AI *feedback model* picks the more principle-compliant one (soft label from option log-probs) → train a Bradley–Terry **preference model** on these AI comparisons → PPO against it (the 6.3 machinery, reused). The helpful (human-labelled) vs harmless (AI-labelled) split; the "non-evasive" result (engages and explains objections rather than refusing flatly). What the constitution actually is (Anthropic's, drawing on the UDHR, Sparrow rules, etc.).
- **Worked element:** a clean flow diagram of the two phases; one critique-and-revise example walked through.
- **Readings:** Bai et al. 2022 (`2212.08073`) — §2–4; Anthropic "Claude's Constitution" (2023 news post — the verbatim principles; note the live `/constitution` URL now serves the Jan-2026 rewrite).

### 7.3 — RLAIF, self-rewarding, and the limits of AI as its own judge
- **Objectives:** generalise beyond CAI; weigh what AI feedback buys against what it breaks.
- **Content:** plain **RLAIF** = the RLHF pipeline with the human labeller replaced by an LLM judge (the constitution becomes the labelling rubric; chain-of-thought + position-swap debiasing; direct-RLAIF skips the separate reward model). **Lee et al. (`2309.00267`):** RLAIF ≈ RLHF on summarisation and helpful/harmless dialogue, and beats SFT **even when the labeller is the same size as the policy** (so it's not just distillation from a bigger model). **Self-rewarding LMs (Yuan, `2401.10020`):** the model judges itself and improves over iterations — motivated explicitly by "superhuman agents need superhuman feedback." Then the turn: the new failure modes — **self-preference bias** (judges over-rate their own family's text; Wataoka `2410.21819`), **sycophancy/bias transfer** (the preference signal itself rewards flattery; Sharma `2310.13548`), **over-optimising an AI proxy** (Gao `2210.10760`, now the proxy is AI-generated), and **recursive model-collapse** (training on model-generated data; Shumailov, *Nature* 2024 / `2305.17493` — present as an argument-by-analogy, not a demonstrated RLAIF result). The escape-vs-relocate debate, with the honest verdict (relocates, by default; escape is an empirical question per capability level — full menu in 8.1).
- **Readings:** Lee et al. (`2309.00267`); Yuan et al. (`2401.10020`); Wataoka (`2410.21819`); recap Gao (`2210.10760`) and Sharma (`2310.13548`) from 6.4.

### 7.4 — Whose constitution? Democratic and African perspectives
- **Objectives:** turn "the constitution is a value choice" into the course's African-safety question.
- **Content:** the constitution as a single, contestable normative commitment applied at industrial scale (one blind spot → millions of identical AI judgements). **Collective Constitutional AI (Huang et al., `2406.07814`; + 2023 blog):** ~1,000 US adults drafted a constitution via Polis; ~50% overlap with Anthropic's, lower social bias across all nine dimensions, matched capability — *but US-only and AI-familiar-screened*, so the one serious public-input experiment **excluded the Global South by design**. The **African-language ceiling:** AI feedback inherits the base model's weakness in low-resource languages, so it cannot generate reliable safety feedback there — tie to the flagship result that guardrails holding in English fail in isiZulu (Yong et al., `2310.02446`). **Participation-washing** (Birhane et al., `2209.07572`) as the warning against tokenistic public input; **data/feedback sovereignty** (Masakhane; Māori/Te Hiku as the worked example). Hand the formal "no neutral aggregation" argument to 8.4 (Conitzer `2404.10271`, Arrow).
- **African lens:** this *is* the African-lens sub-session — substantive, not garnish.

### 7.5 — Lab: build a tiny Constitutional-AI loop (Colab)
- **The lab no surveyed course has.** Builds on the 6.5 RLHF lab.
- **Tasks (CPU-friendly core, optional GPU):**
  1. Write a 3–5 principle **mini-constitution**.
  2. **Critique-and-revise:** prompt a small instruct model to answer a mildly-harmful prompt, then critique its answer against a principle and revise it; compare before/after.
  3. **AI preference labelling:** for response pairs, have the model pick the more principle-compliant one; measure agreement with your *own* labels (the RLAIF signal's reliability, made tangible).
  4. **African-safety probe:** repeat the labelling in isiZulu (or another language you read) — does the AI's preference accuracy collapse? This is the 7.4 ceiling, measured by hand, and a natural project seed.
- **Submit:** notebook with the constitution, before/after revisions, label-agreement numbers, and the in-language probe.

## Verified reading list (all arXiv IDs confirmed by direct fetch, 2026-06-24)

**Core**
- Bai et al. 2022, "Constitutional AI: Harmlessness from AI Feedback" — `arXiv:2212.08073`
- Lee et al. 2023, "RLAIF vs. RLHF: Scaling RL from Human Feedback with AI Feedback" — `arXiv:2309.00267`
- Anthropic & Collective Intelligence Project 2023/24, "Collective Constitutional AI" — `arXiv:2406.07814` (FAccT 2024) + blog `anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input`

**Supplementary**
- Yuan et al. 2024, "Self-Rewarding Language Models" — `arXiv:2401.10020`
- Wataoka et al. 2024, "Self-Preference Bias in LLM-as-a-Judge" — `arXiv:2410.21819`
- Shumailov et al. 2024, "AI models collapse when trained on recursively generated data" — *Nature* 631:755–759 (preprint `arXiv:2305.17493`; verify Nature page numbers before citing)
- Lightman et al. 2023, "Let's Verify Step by Step" — `arXiv:2305.20050` (optional: what the feedback attaches to)
- Birhane et al. 2022, "Power to the People? Opportunities and Challenges for Participatory AI" — `arXiv:2209.07572`
- Yong et al. 2023, "Low-Resource Languages Jailbreak GPT-4" — `arXiv:2310.02446` (the flagship hook; also used in S1/S9)
- Masakhane (`masakhane.io`); Te Hiku Media / Māori Data Sovereignty (worked example of feedback sovereignty)
- Recap from earlier sessions: Casper `2307.15217`, Gao `2210.10760`, Sharma `2310.13548` (6.4); Conitzer `2404.10271`, Burns `2312.09390` (8); the 6.3 RLHF maths.

## Build notes
- Follow the editorial conventions in `CLAUDE.md`: textbook depth (~1,500–2,000 words/expository page; lab shorter), no emoji, sentence-case titles, LaTeX via MathJax, every reading a verified link (`linkify_readings.py`), de-Claudify pass, then `add_page_nav.py` for nav + dropdown.
- Add Session 7 to `docs/index.html` (Week 4) so the dropdown + prev/next chain pick it up; it slots between Session 6 and Session 8.

## Open choices for sign-off
1. **5 vs 6 sub-sessions** — 5 (above) matches the Session 6 rhythm; or split 7.3 into "RLAIF & self-rewarding" + "the limits of AI as its own judge" for a 6-page version with more room on the failure modes.
2. **Lab depth** — keep the CPU-friendly critique/label core (recommended, Colab-floor), with the real RL step as an optional GPU extension reusing the 6.5/ARENA machinery?
3. **Process supervision (Lightman)** — include as a short aside in 7.3, or leave out to keep the session tight?
