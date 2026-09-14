# Technical AI Safety — 12-Week Course Plan (24 sessions)

**Audience:** 4th-year / honours students in Maths & Applied Maths. Comfortable with linear algebra,
probability, and optimisation; understand what a neural network is; can program in Python. Variable
exposure to deep learning specifically — Week 1 levels this.

**Cadence:** two sessions per week × 12 weeks = **24 sessions**. The default rhythm each week is one
**concept/seminar session** and one **lab/working session**, though some weeks run two concept
sessions (the alignment-heavy weeks) and the project weeks run mostly as clinics.

**Through-lines:** (1) the safety-vs-capabilities distinction; (2) idealised models of agency →
empirical LLM alignment (the "two-act" spine from Grosse's Toronto course); (3) a Global South lens
on compute, energy, and governance; (4) intellectual honesty about where the field is uncertain.

---

## 0. Three decisions that shape the build

Before committing to the lab infrastructure and the exact session mix, three forks matter. The plan
below assumes the middle option in each; the alternatives are easy to swing to.

1. **Hands-on intensity.** *Balanced* (assumed): ~1 coding lab/week, paper seminars on the alternate
   session. *Labs-heavy*: ARENA-style notebooks most weeks (needs more GPU/Colab + prep). *Seminar-led*:
   reading-group format with one capstone project (lowest infrastructure).
2. **Project length.** *3–4 weeks* (assumed): real but bounded. *2 weeks*: frees a fortnight for more
   content (e.g. a second mech-interp or governance week). *Full 4 weeks* (the original draft): most
   project depth, least new technical content.
3. **Compute access.** Mech-interp on toy models and most evals work on CPU/free Colab; RLHF/CAI
   replication and adversarial training want a GPU. Confirm whether students get the UCT HPC cluster,
   Colab Pro, or department machines — this decides which labs are graded vs demonstrated.

---

## Part I — Foundations & the safety problem (Weeks 1–2)

### Week 1 — Orientation & foundations

**Session 1 · What technical AI safety is (and isn't).**
Course orientation, expectations, assessment. The map of the field: misuse vs misalignment vs
systemic/structural risk. The **safety–capabilities distinction** and why it's the organising idea.
The case for taking the problem seriously *and* the strongest reasons to doubt it (set the
intellectual-honesty tone from day one). How this course differs from a BlueDot reading group: more
maths, more code, a research project.
- *Readings:* Hendrycks, "X-Risk Overview" (course.mlsafety.org L19) or AISES Ch.1 "Overview of
  Catastrophic AI Risks"; one skeptic piece (e.g. an "AI Snake Oil" chapter / a measured critique) to
  balance it.
- *Reuse:* Gen AI course "Introduction" + "Course Caveats" framing.

**Session 2 · DL & transformers recap + scaling laws.**
Fast, safety-oriented refresher: the transformer, training objective, what "capabilities" are
measured on. **Neural scaling laws** (Kaplan 2020; Chinchilla/Hoffmann 2022) and the **pace of
progress** as empirical trend, not hype. What scaling does and does not buy.
- *Lab/exercise:* fit a simple scaling-law curve to provided loss-vs-compute data; explore Epoch AI's
  compute/parameter trend data. (Light, gets everyone into the toolchain.)
- *Reuse:* Gen AI Week 1 ("But what is a neural network", 3Blue1Brown transformers) + Week 2 ("LLM
  Architecture Deep Dive") as optional pre-reading for the rustier students.

### Week 2 — The alignment problem & the physical substrate

**Session 3 · The core alignment problem.**
The conceptual heart. Outer vs inner alignment; reward misspecification & specification gaming;
**Goodhart's law**; **instrumental convergence**, power-seeking, and the orthogonality thesis;
**corrigibility**; **deceptive alignment / mesa-optimisation**; situational awareness. Framed with the
formal objects maths students like (objectives, optimisers, proxies).
- *Readings:* Hubinger et al., "Risks from Learned Optimization"; Carlsmith, "Is Power-Seeking AI an
  Existential Risk?" (exec summary); Grosse L1–2 reading set. Skeptical counterpoint included.
- *Seminar:* discuss one paper in depth.

**Session 4 · The physical substrate of scale (energy lesson).**
Where capability comes from physically: compute, **energy and water**, **critical minerals**,
data-centre growth, embodied carbon, the **Jevons / rebound** problem. "Compute is the floor" — why
the physical substrate is also the main *governance lever* (foreshadows Week 6). Environmental
justice and the Global South.
- *Reuse:* Gen AI **Week 3 (Environmental Implications)** almost verbatim — "The Cost of Every
  Prompt", "Infrastructure, Scale and the Rebound Problem", "Critical Minerals and AI", "Sustainable
  AI". Reframe the framing paragraph for a safety audience.

---

## Part II — How models are trained and aligned (Weeks 3–4)

### Week 3 — LLM training, end to end

**Session 5 · From pretraining to assistant.**
Self-supervised pretraining → SFT → the full post-training pipeline. What each stage does to model
behaviour. Tokenisation, data, the role of scale (callback to Week 1).
- *Lab:* walk through **nanochat / nanoGPT** — read the SFT stage, run a tiny training step. Students
  see the pipeline they'll later critique.
- *Reuse:* Gen AI Week 2 "Fine-Tuning, RLHF and Alignment" as the conceptual scaffold.

**Session 6 · RLHF & RL fine-tuning.**
Reward modelling from preferences; policy-gradient / **PPO**; RL fine-tuning; KL regularisation. Then
the **limitations of RLHF** (Casper et al., "Open Problems and Fundamental Limitations of RLHF") —
reward hacking, mode collapse, sycophancy as a predictable artefact.
- *Lab:* ARENA Chapter 2 (RL → RLHF) — a reward model + a small policy-gradient step; or run nanochat's
  RL stage. (GPU-dependent — see decision 3.)

### Week 4 — Scalable alignment methods

**Session 7 · Learning from AI feedback.**
**RLAIF**, **Constitutional AI** (Bai et al.), the self-critique-and-revise loop, **deliberative
alignment**. Why labs moved from human to AI feedback; what that trades away.
- *Lab (optional/ambitious):* a CAI mini-replication — the critique→revise stage on a small open
  model, measuring a harmlessness/helpfulness shift.

**Session 8 · Scalable oversight & "whose values?" (ethics lesson).**
How do you supervise a system smarter than you? **Debate**, recursive reward modelling,
**weak-to-strong generalisation**, sandwiching. Then the normative core: alignment to *whose* values?
This is where ethics is load-bearing, not decorative — the **four philosophical lenses** and
**Ubuntu / relational ethics** give the cohort tools to reason about value specification and
preference aggregation (which connects to social-choice impossibility results — a nice maths hook).
- *Readings:* Grosse L12 "Whose Values?"; Christiano et al. debate; Burns et al. weak-to-strong.
- *Reuse:* Gen AI **Week 4** "Ethical Frameworks and Four Lenses" + "Ubuntu and Relational Ethics /
  RIA Just AI Framework".

---

## Part III — Robust, controllable, evaluable models (Weeks 5–6)

### Week 5 — Robustness, unlearning, control

**Session 9 · Robustness & adversarial ML.**
Threat models, adversarial examples, jailbreaks, multilingual safety and indirect prompt injection.
The session distinguishes bounded image perturbations from open-ended language transformations and
asks what evidence a robustness claim supports.
- *Lab:* a CPU-friendly multilingual safety evaluation of a small open instruction model. Students
  score comprehension, refusal and unsafe compliance separately, then compare paired prompts across
  English, isiZulu and Afrikaans without assuming the 2023 language gap will reproduce.
- *Readings:* Goodfellow et al. on adversarial examples; Zou et al. on GCG; Wei et al. on safety-training
  failure; Yong et al. and current multilingual follow-up work.

**Session 10 · Unlearning & the AI-control agenda.**
**Machine unlearning** (and how fragile it is — recovery via fine-tuning/probing). The **AI control**
agenda (Redwood): assume the model may be misaligned and design protocols — monitoring, untrusted-model
deployment, resampling, trusted editing. **Trojans / backdoors** and data poisoning.
- *Lab (optional):* Hendrycks "Trojans" pset, or a small unlearning stress-test.
- *Readings:* Greenblatt et al., "AI Control: Improving Safety Despite Intentional Subversion."

### Week 6 — Evaluations & technical governance

**Session 11 · Evaluations & dangerous-capability evals.**
Capability vs alignment evals. **Model-graded / LLM-as-judge** methods and their **biases** (position,
verbosity, self-enhancement). **METR** autonomy evals; **Apollo** scheming/deception evals; the
elicitation/validity problem (post-training can raise measured capability).
- *Lab (high-leverage):* build a **model-graded eval in UK AISI Inspect** (`inspect-ai`) — dataset →
  solver → model-graded scorer. Reused again as a project option.
- *Readings:* the LLM-as-a-Judge survey (arXiv 2411.15594); METR autonomy resources; Apollo
  in-context scheming.

**Session 12 · Technical AI governance (energy/compute revisited).**
The **Reuel et al. taxonomy** — *capacities* (assessment, access, verification, security,
operationalisation) × *targets* (data, compute, models, deployment). **Compute governance** (callback
to Week 2's substrate). The three frontier-safety frameworks compared — Anthropic RSP, OpenAI
Preparedness, DeepMind FSF — via METR's "Common Elements." **Agent governance.** The sociotechnical
landscape (labour, surveillance, power concentration, dual-use) and **sovereign-AI / African**
governance.
- *Readings:* Reuel et al., "Open Problems in Technical AI Governance" (arXiv 2407.14981); METR
  "Common Elements of Frontier AI Safety Policies."
- *Reuse:* Gen AI Week 4 "The Broader Landscape of AI Ethics" (sociotechnical harms) + Week 11
  "Sovereign AI Capacity / Data, Languages & African Model-Building."

---

## Part IV — Mechanistic interpretability (Weeks 7–8)

### Week 7 — Interpretability foundations

**Session 13 · Why interpretability; features & circuits.**
The case for interpretability as a safety tool (and its limits). Features, **circuits**, the residual
stream, **induction heads**, **superposition / polysemanticity**. The geometric/linear-algebraic view
that suits maths students.
- *Readings:* Olah et al. "Zoom In: Circuits"; Elhage et al. "Toy Models of Superposition"; Neel
  Nanda's mech-interp glossary.

**Session 14 · Lab: TransformerLens + induction heads.**
Hands-on with **TransformerLens** (MIT-licensed). **ARENA Chapter 1, part 2** — hooks, activations,
discovering induction heads in a real small model. The canonical on-ramp.

### Week 8 — Interpretability in practice

**Session 15 · Circuits, patching, and sparse autoencoders.**
**Activation patching** and the **IOI circuit**; **sparse autoencoders / dictionary learning** as the
modern frontier; causal / probing / steering methods (the Stanford CS221M lens).
- *Readings:* Wang et al. IOI; Bricken et al. / Cunningham et al. on SAEs and monosemanticity.

**Session 16 · Lab + safety applications & limits.**
SAE features / probing / activation steering on a toy or small model (ARENA part 33/52/54). Then:
interpretability *for safety* — deception detection, model auditing — and an honest reckoning with how
far it's actually got. Bridges into project ideas.

---

## Part V — Research project & synthesis (Weeks 9–12)

The project is the spine of the final third. Deliverable: a **short paper (6–8 pp, NeurIPS-style) +
code**, in teams of 2–3. Four sanctioned archetypes (after Grosse): (a) propose an algorithm/objective;
(b) improve the safety of an existing ML system; (c) rigorously test a hypothesis raised in lecture;
(d) build a *novel* toy example illustrating a safety idea. Negative results are welcome with a
well-supported explanation.

### Week 9 — Project launch + frontier topic

**Session 17 · Project kickoff & scoping.**
The archetypes; a menu of **scoped project ideas** (interpretability, evals, robustness,
alignment-method replication, governance analysis — see `02-Open-source-courses-research.md` for the
bank). The **over-scoping trap** and how to define a concrete deliverable + baseline metric in week 1.
Proposals due end of week.

**Session 18 · Frontier & sociotechnical topic (flex / guest slot).**
One of: **agentic AI & long-horizon risk** (planning, tool use, MCP, agent failure modes — reuse Gen
AI Week 10) · **AI for science & dual-use** · **Africa's sovereign-AI capacity & the global picture**
(reuse Gen AI Week 11). A natural **guest-lecture** slot.

### Week 10 — Project work + the skeptics

**Session 19 · Project clinic.**
Proposal feedback, methodology help, scoping triage. Working session.

**Session 20 · Steelman the skeptics + open problems.**
Deliberately argue the *strongest case against* the AI-risk framing (Princeton's "criticisms" unit,
Grosse's "skeptical takes"); where the field genuinely disagrees; calibrated uncertainty. Pairs with
the "illusions of understanding" reading (Messeri & Crockett, Nature) on over-reliance.
- *Reuse:* Gen AI Week 9 "Illusions of Understanding" + "Three Categories of Failure."

### Week 11 — Project work

**Session 21 · Mid-project check-in.**
Each team: 5-minute status + structured peer feedback. Catches over-scoping before it's fatal.

**Session 22 · Project work / buffer.**
Office-hours-style clinic, or a cohort-chosen deep dive / second guest. Built-in slack.

### Week 12 — Presentations & synthesis

**Session 23 · Final presentations + peer review.**
Project talks (≈10 min + Q&A) with **structured, anonymised peer review** (students review two peers'
projects — teaches reviewing and adds feedback bandwidth).

**Session 24 · Presentations cont. + synthesis & pathways.**
Remaining talks; course synthesis; where the field is heading; how to keep learning and contribute
(ARENA, MATS, AI Safety Institutes, research groups). Closing reflection.

---

## Proposed assessment

Borrowing from Grosse (project rubric), Stanford CS120 (peer review), and Oxford AISAA (the short
failure-mode essay). Weights are a starting point — adjust to faculty norms (the sibling course used
40/40/20).

| Component | Weight | Notes |
|-----------|-------:|-------|
| Weekly labs / problem sets | 25% | The coding labs above; completion + correctness, resubmission allowed. |
| Paper presentation + written critiques | 15% | Team presents one paper; everyone submits short critiques ahead of the relevant seminar. |
| Failure-mode analysis (mid-course) | 10% | ~1,500 words: pick one alignment failure mode, analyse it rigorously. **One sanctioned track is an African/Global-South-context failure mode** (e.g. guardrail degradation in an African language, eval blind spots, a data-sovereignty harm). Low-stakes de-risker for the project. |
| **Research project** (proposal + paper + code) | 40% | Itemised, per-section rubric (abstract / intro / method / experiments / limitations / creativity) **+ a "Positioning & context" criterion** — see below. |
| Peer review of projects | 10% | Anonymised reviews of two peers' final projects; the review form asks reviewers to assess the positioning/context statement. |

### Wiring the African / Global-South lens into assessment

The lens is graded through the work students already do, not bolted on as a separate mark — avoiding
tokenism while making engagement non-optional:

1. **Mandatory context statement (every project).** One paragraph in every project report: *who does
   this help, whose risk does it address, and how (if at all) does it apply in an African / local
   context?* "Not applicable, because…" is an acceptable, gradable answer for a pure-theory project —
   the point is that the student has *thought* about it. This is the new **"Positioning & context"**
   rubric line (~10% of the project mark, carved from the existing creativity/positioning allocation).
2. **The failure-mode essay** offers an explicit **African-context track** (see table) — students may
   take it or analyse any other failure mode.
3. **The flagship project** ("Does the guardrail hold in isiZulu?", `04-African-AI-safety.md`) sits in
   the menu as a first-class, fully-scoped option — not a remedial alternative.
4. **Peer review** rewards engagement with positioning, so students learn to value it in others' work.

This keeps the requirement *light and universal* (every student reflects on context) while leaving
*depth optional* (those who want an African-safety project have a strong, supported path). Whether to
strengthen #1 from "reflect" to "required African-context project" is a deliberate faculty choice — the
plan defaults to the lighter version.

---

## Mapping to the original draft

| Original draft week | Where it lives now |
|---|---|
| W0 Orientation | Folded into Session 1 |
| W1 ML overview + scaling laws | Sessions 1–2 |
| W2 Core alignment challenge | Session 3 |
| W3 LLM training (nanochat) | Sessions 5–6 |
| W4 Alignment methods (RLAIF/CAI/deliberative) | Sessions 7–8 |
| W5 Robustness, unlearning, control | Sessions 9–10 |
| W6 Technical AI governance / evals | Sessions 11–12 |
| W7–8 Mechanistic interpretability | Sessions 13–16 |
| W9–12 Course project | Sessions 17–24 |
| *(added)* Ethics | Integrated: S4 (environmental), S8 (whose values), S12 (sociotechnical), S20 (skeptics) |
| *(added)* Energy usage | Session 4 + revisited in S12 (compute governance) |

The main change from the draft: ethics and energy are woven into the technical spine at the points
where they're load-bearing, rather than being standalone weeks — and a "steelman the skeptics" session
plus structured peer review are added. Scalable oversight moves from the alignment-challenge week
(draft W2) into the alignment-methods week (S8), where it sits more naturally next to debate and
weak-to-strong.
