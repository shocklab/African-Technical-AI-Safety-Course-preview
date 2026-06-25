# Part V curriculum — Research project & synthesis (Sessions 17–24)

Scope decision (signed off 2026-06-25): **two content sessions deep (S18, S20), S17 substantial, the rest as focused single-page scaffolds.** Part V scaffolds the 40%-weighted research project defined in Session 1.1 (proposal → 6–8pp paper + code, small teams, per-section rubric, anonymised peer review).

## Structure

| S | Title | Format | Content |
|---|-------|--------|---------|
| 17 | Project kickoff & scoping | substantial single page | what makes a good safety project; the rubric; timeline; project-idea menu by track; teams/proposal/reproducibility; the African context statement |
| 18 | AI safety from the Global South | **deep, 4 sub-pages** | the two framings + honest stance; the multilingual gap as a frontier vulnerability; sovereignty + decolonial AI; the African ecosystem & what Global-South-led safety looks like |
| 19 | Project clinic | scaffold single page | baselines, the S11 statistics callback, debugging, scoping-down, reproducibility checklist |
| 20 | Steelman the skeptics + open problems | **deep, 3 sub-pages** | the present-harms & meaning critiques; the political-economy critique; the open technical problems + holding calibrated belief |
| 21 | Mid-project check-in | scaffold single page | structured progress review; the "kill or pivot" decision; common failure modes at the midpoint |
| 22 | Project work / buffer | scaffold single page | working-session structure; a writing-the-paper guide (the per-section rubric as a writing target) |
| 23 | Final presentations + peer review | scaffold single page | presentation format; the anonymised peer-review rubric; how to give a useful review |
| 24 | Synthesis & pathways | substantial single page | the four through-lines revisited; calibrated takeaways; pathways into the field incl. African entry points; further reading |

Build order = session order (the nav injector chains prev/next from `index.html`). Single-page sessions use a direct `<a>` in `index.html` (like S12/S14); S18 and S20 are `session-group` + `subsession-list` blocks.

## Coherence guardrails
- **The two capstones.** S18 is the capstone of the *African technical AI safety* through-line; S20 is the capstone of the *intellectual honesty* through-line (both named in 1.1). Frame them that way.
- **Honest African angle (course principle).** S18 must not oversell. Say plainly that the centre of gravity is present-harms/fairness/governance, and carry the "safety" weight on the two genuine bridges (ILINA; the low-resource jailbreak as a frontier vulnerability invisible from English). Flag that "AI safety" in the AU Strategy and the UCT Hub means governance/peace-and-security, not frontier alignment.
- **Callbacks.** S18 ← 1.4 (isiZulu anchor), 2.2 (tokenisation tax), 4/12 (compute & data sovereignty), 8.3 (Ubuntu/relational ethics), 9 & 11 (the isiZulu labs). S20 ← 1.3 (the case & its critics), 8 (ethics), and the "false assurance" / construct-validity threads from 11 & 16. S24 ties all four through-lines together.
- **Project hooks.** S17's idea menu draws on every prior lab; S18 and S20 each end with a project hook so the content sessions feed the project.

## S17 — sections (single page)
Intro (the project is 40%; this sets you up) → what makes a good safety project (tractable, falsifiable, Colab-feasible, honestly scoped; the 1.4 reading checklist turned inward) → the rubric expanded (abstract / method / experiments / limitations / creativity + positioning & context) → the timeline (proposal S17 → clinic S19 → mid-check S21 → work S22 → presentations S23–24) → **the project-idea menu by track**, each idea = question · method · Colab-feasibility · which session it builds on · African-context hook:
- Robustness / multilingual (← S9 lab): refusal degradation in another African language; test a cheap defence.
- Evaluations (← S11 lab): build an in-language safety eval; a construct-validity study of a public benchmark.
- Interpretability (← S13–16 + the 16.4 brief): replicate an induction-head/IOI finding; probe/steer an SAE feature; a mini auditing-game.
- Alignment methods (← S6/S7): a tiny RLHF or Constitutional-AI loop; a reward-hacking demonstration.
- Control / unlearning (← S10): a trusted-monitor variant; an unlearning-evaluation study.
- Governance / compute (← S4/S12): a compute-threshold or sovereignty analysis; an eval→commitment mapping.
- Conceptual / critique (← S1.3/S20): a steelman + rebuttal of a safety claim; a construct-validity critique.
→ teams, proposal format, reproducibility (pre-register the question; seeds; honest error bars from S11) → the African context statement ("not applicable, because…" is a full-credit answer for pure theory) → readings (ARENA project ideas; Neel Nanda's "concrete steps / 200 open problems"; the course's own labs) → Next: S18.

## S18 — sub-pages + VERIFIED sources
- **18.1 Two framings, one honest stance** — present-harms vs frontier-risk; "whose safety, whose risks, whose values?"; the defensible stance (centre of gravity = present harms/governance; two real bridges to frontier safety).
- **18.2 The multilingual safety gap as a frontier vulnerability** — Yong et al. and Deng et al. generalised; the tokenisation tax (← 2.2); why this is a frontier-safety problem invisible from English, not a fairness footnote.
- **18.3 Sovereignty & the decolonial critique** — compute/data/talent sovereignty (← 4/12); data colonialism; the decolonial-AI literature.
- **18.4 The African ecosystem & Global-South-led safety** — the orgs, honest about what "safety" means in each; ILINA as the real frontier actor; project hook.

Verified (primary-source) — full log in the agent run; key items:
- **Yong, Menghini & Bach (2023)** arXiv:2310.02446 — AdvBench, low-resource translation jailbreak: English 0.96% → **LRL-combined 79.04%**; **isiZulu alone ≈53%**. (79% is the *combined* figure, not isiZulu alone.)
- **Deng et al. (2023/24)** arXiv:2310.06474 — MultiJail; *unintentional* unsafe rate ≈3× from high- to low-resource (GPT-4 3.60%→10.16%); *intentional* up to 80.92% (ChatGPT)/40.71% (GPT-4). Keep the two scenarios distinct.
- **Masakhane** — leaderless participatory African-NLP collective (masakhane.io); not a company, no single founder.
- **Lelapa AI** (lelapa.ai; CEO Pelonomi Moiloa, CTO Jade Abbott) — **InkubaLM-0.4B = 0.422B params, 5 languages** (Swahili, Yoruba, Hausa, isiZulu, isiXhosa). A small LM, *not* "Africa's first LLM".
- **ILINA Program** (ilinaprogram.org; coordinator Cecil Abungu, Nairobi) — genuinely **African-led, frontier/x-risk-oriented** AI-safety org (research + fellowship). The one real bridge to frontier safety.
- **Research ICT Africa — "Africa Just AI"** (researchictafrica.net/project/africa-just-ai/; Alison Gillwald, Pria Chetty) — a 3-year IDRC/SIDA **research PROJECT, not a "framework"**. ⚠ correction needed in existing pages (see below).
- **Deep Learning Indaba** (2017; co-founders Shakir Mohamed & Ulrich Paquet) — annual African-ML conference + charity.
- **African Hub on AI Safety, Peace and Security** (ai.uct.ac.za; UCT AI Initiative + Global Center on AI Governance) — "safety" here = governance/peace-and-security/societal harms, **not** frontier alignment. (Jonathan is on the team.)
- **AU Continental AI Strategy** — endorsed **18–19 July 2024**, Accra (Executive Council, 45th Ordinary Session); five focus areas incl. "minimising risks". (The "20240809" in the URL is the posting date, not adoption.)
- Decolonial literature: **Mohamed, Png & Isaac (2020)** "Decolonial AI", *Philosophy & Technology* 33(4) (Png = Oxford OII, not DeepMind; all three equal); **Birhane (2020)** "Algorithmic Colonization of Africa" (*SCRIPTed* 17(2)) + **Birhane (2021)** "Algorithmic injustice: a relational ethics approach" (*Patterns*); **Sambasivan et al. (2021)** "Re-imagining Algorithmic Fairness in India and Beyond" (FAccT); **Couldry & Mejias (2019)** "data colonialism"; **Okolo** (AI in the Global Majority). 

## S20 — sub-pages + VERIFIED sources
- **20.1 "It doesn't understand", and the present harms** — the meaning critique + the documented near-term harms.
- **20.2 The political economy of the x-risk frame** — TESCREAL, AI-as-normal-technology, the incumbents/power critique.
- **20.3 The open problems, and how to hold a belief** — the genuinely unsolved technical questions + calibrated uncertainty (the 1.1/1.3 capstone).

Verified — key items + traps:
- **Bender & Koller (2020)** "Climbing towards NLU" (ACL) — the octopus; form ≠ meaning *in principle*.
- **"On the Dangers of Stochastic Parrots" (FAccT 2021)** — Bender, Gebru (joint-first), McMillan-Major, **"Shmargaret Shmitchell" = Margaret Mitchell** (affiliation "The Aether"). Four bylined authors (not six); pp. 610–623; title carries the 🦜. Present harms (cost/bias/opacity/illusion-of-meaning), **no x-risk argument**.
- **Gebru & Torres (2024)** "The TESCREAL bundle…" *First Monday* 29(4). Order is **Gebru & Torres**; coauthor **Émile P. Torres**.
- **Narayanan & Kapoor** — *AI Snake Oil* (Princeton, 2024) + **"AI as Normal Technology"** (Knight First Amendment Institute, 2025): skeptical of *both* hype and doom; AI diffuses over decades; pursue resilience.
- **AI Now Institute — *Artificial Power: 2025 Landscape Report*** (Brennan, Kak & Myers West) — "the AGI mythology"; x-risk inevitability narratives advance incumbents. (The capture argument is the 2025 report, **not** the 2023 one; avoid the literal phrase "regulatory capture".) Whittaker's on-point lines are **interviews** (Slate 2023) — cite as such.
- Optional internal skeptic-of-doom: **Belrose & Pope (2023)** "AI is easy to control" (optimists.ai); **Melanie Mitchell (2021)** "Why AI is Harder Than We Think" (arXiv:2104.12871) — *Melanie*, Santa Fe, **not** Margaret Mitchell.
- Open problems (anchored): **Bowman et al. (2022)** scalable oversight arXiv:2211.03540; **Sharkey, Chughtai et al. (2025)** "Open Problems in Mechanistic Interpretability" arXiv:2501.16496; **Raji et al. (2021)** "AI and the Everything in the Whole Wide World Benchmark" arXiv:2111.15366 (construct validity); **Hubinger et al. (2024)** "Sleeper Agents" arXiv:2401.05566 (deception persists; adversarial training hides not removes).

## RIA "Just AI" — checked, NO correction needed (2026-06-25)
On inspection the flag was a false alarm, and making the "fix" would have introduced an error. There are **two distinct RIA artifacts**: "**Africa Just AI**" is the umbrella research project (researchictafrica.net/project/africa-just-ai/, IDRC/SIDA) — described correctly in S18.4 as a project; the "**RIA Just AI Framework of Inquiry**" (Chetty & Sey 2025; researchictafrica.net/research/ria-just-ai-framework-of-inquiry/; nine inquiries; CC BY-NC-SA) is a genuine published framework, which is what **S8.3** teaches and cites (its licence was already verified in the S1–8 audit, commit 750c4e7). So S8.3's title, about.html's "RIA Just AI framework", and 1.4's "Just AI governance work" are all accurate. No page changed. (The S18 research agent conflated the project with the framework-of-inquiry; its own note confirmed "Framework of Inquiry" is a real RIA artifact.)

## Source-verification status
S18 + S20 load-bearing sources verified full-text / primary-source by two research agents 2026-06-25 (attribution traps logged above). Re-confirm any NEW citation added during authoring before publishing, per [[source-grounding-verify-full-text]].
