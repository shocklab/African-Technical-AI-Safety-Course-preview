# Detailed per-session plans (24 sessions)

**Calibration in force:** *balanced* intensity (≈1 coding lab/week + seminars), *3–4 week* project,
**Google Colab** as the compute floor. Labs are written to run on free/Pro Colab; anything needing a
real GPU (full RLHF/CAI replication, adversarial *training*) is marked **[GPU — optional/demo]** so the
graded labs never depend on hardware students may not have.

> **Reading-list health warning.** The citations below are the *intended* set. Per the course's
> inherited discipline, run `/verify-references` over the final reading list before publishing — exact
> arXiv IDs, venues, and any statistic must be checked against primary sources. Where I'm not certain of
> an ID I give author + title + venue instead of a number.

Each session gives: **format · objectives · pre-class · in-class/lab · discussion/exercise · reuse**.

---

# Part I — Foundations & the safety problem

## Week 1 — Orientation & foundations

### Session 1 · What technical AI safety is (and isn't) — *concept*
**Objectives.** Place the course in the field; distinguish misuse / misalignment / systemic risk;
articulate the safety–capabilities distinction; hold advocacy and skepticism at once.
**Pre-class.** Hendrycks, *Intro to ML Safety* L1 ("Introduction") + L19 ("X-Risk Overview"), OR AISES
textbook Ch.1 (arXiv 2411.01042); **one skeptic piece** — Narayanan & Kapoor, *AI Snake Oil* (a chapter
/ the Substack) or a measured critique of x-risk framing.
**In-class.** Course logistics + assessment walkthrough (15 min). The field map on the board: a 3×3 of
{misuse, misalignment, systemic} × {today, near, frontier}. Students place 6 example incidents in the
grid. Short framing lecture on safety vs capabilities.
**Exercise.** Each student writes one sentence: "The strongest reason to take misalignment seriously is
… and the strongest reason to doubt it is …". Collected, themes surfaced next session.
**Reuse.** Gen AI course "Introduction" + "Course Caveats" for tone and the AI-transparency-notice norm.

### Session 2 · DL & transformers recap + scaling laws — *lab*
**Objectives.** Refresh the transformer + training objective for a safety lens; read scaling laws as an
empirical trend; get the toolchain working in Colab.
**Pre-class.** Kaplan et al. 2020, *Scaling Laws for Neural LMs* (arXiv 2001.08361, skim); Hoffmann et
al. 2022, *Training Compute-Optimal LLMs* / Chinchilla (arXiv 2203.15556, skim). Rusty students:
Gen AI Week 1 ("But what is a neural network", 3Blue1Brown transformers) + Week 2 "LLM Architecture
Deep Dive".
**Lab (Colab).** (i) Load a small pretrained model (GPT-2 small via HuggingFace/TransformerLens),
inspect shapes, run a forward pass, read off next-token logits. (ii) Fit a power law to provided
loss-vs-compute points; extrapolate and discuss where extrapolation breaks. (iii) Browse Epoch AI's
compute-trend data.
**Discussion.** What does scaling buy and not buy? Is "capabilities are predictable, safety isn't" a
fair summary?
**Reuse.** Gen AI Week 1/2 as optional pre-reading.

## Week 2 — The alignment problem & the physical substrate

### Session 3 · The core alignment problem — *concept + seminar*
**Objectives.** Define outer vs inner alignment; explain specification gaming & Goodhart; state the
instrumental-convergence / power-seeking / orthogonality argument and its premises; define deceptive
alignment and corrigibility.
**Pre-class.** Hubinger et al., *Risks from Learned Optimization* (arXiv 1906.01820, §1–3); Carlsmith,
*Is Power-Seeking AI an Existential Risk?* (exec summary); a *skeptical take* from Grosse's L1 list.
Optional: DeepMind specification-gaming examples list.
**In-class.** Lecture building the chain proxy → Goodhart → mesa-optimisation → deceptive alignment,
each step stated as a claim with its premises. **Seminar:** small groups each take one premise of the
power-seeking argument and try to break it; report the weakest link.
**Exercise / link to assessment.** Announce the **mid-course failure-mode essay** (due ~Week 6): pick
one failure mode introduced here or later and analyse it rigorously (~1,500 words).

### Session 4 · The physical substrate of scale (energy lesson) — *concept*
**Objectives.** Quantify the compute/energy/water/minerals footprint of frontier AI; explain Jevons/
rebound; argue why compute is both the capability floor and the main governance lever; connect to
environmental justice.
**Pre-class.** Gen AI **Week 3** pages (Cost of Every Prompt; Infrastructure & the Rebound Problem;
Critical Minerals; Sustainable AI). One current data-centre-energy figure source (IEA / Epoch) to
update numbers.
**In-class.** Worked estimate: energy per query → per agentic task → at deployment scale (use the
"flight comparison" worked example from the reused page). Map the supply chain mine → fab → data centre
→ e-waste. Set up the through-line to compute governance (Week 6).
**Discussion.** If compute is the lever, who holds it, and what does that mean for a country like South
Africa? (Foreshadows sovereign-AI in Weeks 6/9.)
**Reuse.** Gen AI Week 3 — ~90% verbatim; reframe the opening for a safety audience.

---

# Part II — How models are trained and aligned

## Week 3 — LLM training, end to end

### Session 5 · From pretraining to assistant — *concept + light lab*
**Objectives.** Trace pretraining → SFT → post-training; explain what each stage changes; read real
training code without fear.
**Pre-class.** Gen AI Week 2 "Fine-Tuning, RLHF and Alignment"; skim the nanochat / nanoGPT README.
**Lab (Colab).** Read the **nanochat** SFT stage; run a tiny fine-tune step on a toy dataset and watch
the loss move. Tokeniser exploration: see how text becomes tokens and back.
**Discussion.** Where in this pipeline could misalignment first enter? (Sets up S6.)

### Session 6 · RLHF & RL fine-tuning — *concept + seminar*
**Objectives.** Explain reward modelling from preferences; sketch PPO/policy-gradient; state the known
failure modes of RLHF.
**Pre-class.** Christiano et al., *Deep RL from Human Preferences*; Casper et al., *Open Problems and
Fundamental Limitations of RLHF* (arXiv 2307.15217).
**Lab.** Walk the **ARENA Chapter 2** RLHF notebook — a reward model + a small policy-gradient update on
a toy task; **[GPU — optional/demo]** for the larger RLHF example (otherwise run the CPU/toy version and
demo the full one).
**Seminar.** Map each Casper et al. limitation onto a concrete observed behaviour (sycophancy, reward
hacking, mode collapse). Which are fixable by better RLHF vs fundamental?

## Week 4 — Scalable alignment methods

### Session 7 · Learning from AI feedback — *concept + lab*
**Objectives.** Explain RLAIF and Constitutional AI; describe the critique–revise loop and deliberative
alignment; reason about what replacing human with AI feedback trades away.
**Pre-class.** Bai et al., *Constitutional AI: Harmlessness from AI Feedback* (arXiv 2212.08073); a
deliberative-alignment write-up (OpenAI 2024).
**Lab (Colab).** Implement the **CAI critique→revise loop** on a small open model for a handful of
prompts and qualitatively compare pre/post responses. **[GPU — optional]** to scale beyond a few prompts;
the graded version is the few-prompt API/small-model demo.
**Discussion.** Who writes the constitution, and what's smuggled in by that choice? (Bridges to S8.)

### Session 8 · Scalable oversight & "whose values?" (ethics lesson) — *concept + seminar*
**Objectives.** Explain debate, recursive reward modelling, sandwiching, weak-to-strong generalisation;
connect value-specification to ethical frameworks and to social-choice impossibility results.
**Pre-class.** Burns et al., *Weak-to-Strong Generalization* (arXiv 2312.09390); Irving/Christiano
debate paper; Grosse L12 "Whose Values?" readings. Gen AI **Week 4** "Ethical Frameworks and Four
Lenses" + "Ubuntu and Relational Ethics / RIA Just AI Framework".
**In-class.** Lecture: the supervision-gap problem and the proposed mechanisms. Then the normative turn
— the four lenses + Ubuntu as tools for "align to whose values?". Maths hook: preference aggregation →
Arrow's theorem / social-choice impossibility.
**Seminar.** Debate exercise: two students argue a contested value question, a third (playing the
"weak judge") must adjudicate — does debate actually help the judge?
**Reuse.** Gen AI Week 4 (two pages).

---

# Part III — Robust, controllable, evaluable models

## Week 5 — Robustness, unlearning, control

### Session 9 · Robustness & adversarial ML — *concept + lab*
**Objectives.** Specify an attack's access, goal, allowed transformation and success criterion; derive
FGSM and state the limits of its norm-bounded threat model; explain GCG as a heuristic for discrete
optimisation; distinguish jailbreaks from direct and indirect prompt injection; evaluate multilingual
safety while separating comprehension, refusal and unsafe compliance.
**Pre-class.** Goodfellow, Shlens & Szegedy, "Explaining and Harnessing Adversarial Examples"; Zou et
al., "Universal and Transferable Adversarial Attacks on Aligned Language Models"; Wei, Haghtalab &
Steinhardt, "Jailbroken"; Yong, Menghini & Bach, "Low-Resource Languages Jailbreak GPT-4". Compare
Yong et al.'s 2023 result with a current multilingual evaluation before class.
**Lab (Colab).** Run a fixed set of mild safety-boundary and benign prompts through a small open
instruction model in English, isiZulu and Afrikaans. Score comprehension, refusal, unsafe compliance
and irrelevant output separately. Compare matched prompts and treat a null or reversed language
difference as evidence to interpret, not a failed reproduction. The core requires no API or GPU.
**Discussion.** Which robustness claims survive a change in threat model? What can a multilingual
evaluation conclude when model capability and translation quality vary with language?

### Session 10 · Unlearning & the AI-control agenda — *concept + seminar*
**Objectives.** Explain machine unlearning and why it's fragile; explain the AI-control framing
(assume-misaligned, design protocols); define trojans/backdoors and data poisoning.
**Pre-class.** Greenblatt et al., *AI Control: Improving Safety Despite Intentional Subversion* (arXiv
2312.06942); an unlearning paper (e.g. *Who's Harry Potter?* or a TOFU/WMDP-style benchmark paper);
Hendrycks "Trojans".
**Lab (optional, Colab).** Small **unlearning stress-test** — "remove" a fact via a cheap method, then
attempt recovery by probing/fine-tuning; OR the Hendrycks **Trojans** pset.
**Seminar.** Control vs alignment: if you can't trust the model, can protocols around it ever be enough?
Where does control buy time, where does it fail?

## Week 6 — Evaluations & technical governance

### Session 11 · Evaluations & dangerous-capability evals — *lab-forward*
**Objectives.** Distinguish capability vs alignment evals; explain model-graded/LLM-as-judge methods and
their biases; explain the elicitation/validity problem.
**Pre-class.** *A Survey on LLM-as-a-Judge* (arXiv 2411.15594); METR autonomy-evaluation resources;
Apollo *In-Context Scheming*.
**Lab (Colab, high-leverage).** Build a **model-graded eval in UK AISI Inspect** (`pip install
inspect-ai`): a small Dataset, a Solver, and a `model_graded_qa` Scorer for one narrow capability. Then
**measure position/verbosity bias** in your own judge by swapping answer order. (All API-based.)
**African-safety variant:** build a safety/capability eval on open Masakhane data (**IrokoBench** —
AfriMMLU/AfriXNLI — or **AfriQA**) and discuss whether an LLM judge is reliable for African-language
content (emerging research — present as open). See `04-African-AI-safety.md`.
**Discussion.** If your judge is biased, what does your eval actually measure? This lab doubles as a
project on-ramp (project ideas 4–5, and the flagship African-language eval project).

### Session 12 · Technical AI governance (energy/compute revisited) — *concept + seminar*
**Objectives.** Use the Reuel et al. capacities × targets taxonomy; explain compute governance; compare
the three frontier-safety frameworks; situate sovereign-AI and sociotechnical harms.
**Pre-class.** Reuel et al., *Open Problems in Technical AI Governance* (arXiv 2407.14981, skim the
taxonomy + one capacity); METR *Common Elements of Frontier AI Safety Policies*. Gen AI Week 11
"Sovereign AI Capacity" + Week 4 "The Broader Landscape of AI Ethics".
**In-class.** Lecture on the taxonomy; locate compute governance and link back to S4's substrate.
**Seminar (jigsaw):** three groups each take Anthropic RSP / OpenAI Preparedness / DeepMind FSF, then
cross-compare against METR's "Common Elements" — what's shared, what's missing, what's enforceable?
**Reuse.** Gen AI Week 11 + Week 4 "Broader Landscape".

---

# Part IV — Mechanistic interpretability

## Week 7 — Interpretability foundations

### Session 13 · Why interpretability; features & circuits — *concept*
**Objectives.** Make (and critique) the case for interpretability as safety; define features, circuits,
the residual stream, induction heads, superposition/polysemanticity.
**Pre-class.** Olah et al., *Zoom In: An Introduction to Circuits* (Distill 2020); Elhage et al., *Toy
Models of Superposition* (Anthropic, transformer-circuits.pub 2022, §1–2); Neel Nanda's mech-interp
glossary (reference).
**In-class.** Lecture with the linear-algebraic view (the residual stream as a communication channel;
superposition as more features than dimensions). Worked board example of an induction head.
**Discussion.** What safety question could interpretability *answer*, and what can it not?

### Session 14 · Lab — TransformerLens + induction heads — *lab*
**Objectives.** Use TransformerLens hooks; locate and verify an induction head empirically.
**Pre-class.** ARENA Ch.1 part 1 video (transformer from scratch) as a refresher; skim the
"Getting Started in Mech Interp" TransformerLens page.
**Lab (Colab).** **ARENA Chapter 1, part 2** — load GPT-2 small, cache activations, find induction
heads, run the induction-head detector. Everything CPU/free-Colab-friendly. (TransformerLens is MIT —
the one cleanly reusable codebase.)
**Deliverable.** Short notebook write-up: which heads, what evidence.

## Week 8 — Interpretability in practice

### Session 15 · Circuits, patching, and sparse autoencoders — *concept + lab*
**Objectives.** Explain activation patching and the IOI circuit; explain SAEs / dictionary learning as
the modern frontier; place probing/steering/causal methods.
**Pre-class.** Wang et al., *Interpretability in the Wild: the IOI circuit* (arXiv 2211.00593); one SAE
paper — Cunningham et al. (arXiv 2309.08600) or Bricken et al. *Towards Monosemanticity*
(transformer-circuits.pub).
**Lab (Colab).** **ARENA part 41** (IOI / activation patching / logit attribution) on GPT-2 small, OR
the **grokking / modular-arithmetic** circuit (part 52) — the latter is a clean, fully reverse-
engineerable target maths students enjoy (Fourier structure in the weights).
**Discussion.** Does patching show *causation* or *correlation* in the circuit? (Sets up the causal-
methods view.)

### Session 16 · Lab + safety applications & limits — *lab + concept*
**Objectives.** Use SAE features / probing / steering on a small model; assess interpretability *for
safety* (deception detection, auditing) and its current limits honestly.
**Pre-class.** A "probes/SAEs for safety" piece (e.g. linear-probe truthfulness, or an Anthropic
auditing/feature-steering write-up); Neel Nanda's "200 Concrete Open Problems" intro (project bank).
**Lab (Colab).** Use **pretrained SAEs** (e.g. for GPT-2 small) to inspect a feature cluster, OR train a
**linear probe** for a concept across layers, OR an **activation-steering** demo. All low-compute.
**Bridge.** Each student names one interpretability project idea from the "200 problems" list — feeds
the project kickoff next week.

---

# Part V — Research project & synthesis

> **Project frame (announced S17).** Teams of 2–3; deliverable = 6–8pp NeurIPS-style short paper +
> code. Archetypes (Grosse): (a) propose an algorithm/objective; (b) improve safety of an existing
> system; (c) rigorously test a lecture hypothesis; (d) build a novel toy example. Negative results
> welcome with a well-supported explanation. Colab-feasible scoping is required (no project may *depend*
> on a GPU students don't have). Full idea bank in `02-Open-source-courses-research.md`; **flagship
> African-safety project** ("Does the guardrail hold in isiZulu?") in `04-African-AI-safety.md`.

## Week 9 — Project launch + frontier topic

### Session 17 · Project kickoff & scoping — *workshop*
**Objectives.** Choose an archetype; convert a vague idea into a concrete deliverable + baseline metric;
avoid over-scoping.
**In-class.** Walk the idea bank by theme (interp / evals / robustness / alignment-method replication /
governance analysis). Each team drafts a one-paragraph proposal live and gets a 2-minute scoping triage
(what's your metric? what's the smallest version that still teaches you something?).
**Deliverable.** **Proposal due end of week** (½ page: question, method, metric, compute plan, risk).

### Session 18 · AI safety from the Global South (African AI safety) — *concept + debate / guest*
**Objectives.** Articulate the present-harms-vs-existential-risk debate and its North/South dimension;
explain decolonial-AI and compute/data-sovereignty arguments; name real African-led safety/eval work and
assess the gap honestly. **Full outline in `04-African-AI-safety.md`.**
**Pre-class.** Hanna & Bender, "AI Causes Real Harm…" (*Scientific American* 2023); Mohamed, Png & Isaac,
"Decolonial AI" (2020); counterpoint *PNAS* 2025 ("Existential risk narratives… do not distract…");
skim the AU Continental AI Strategy (2024) + the ILINA Program.
**In-class.** Structured swap-sides debate (present harms vs long-term risk); mini-lecture on
compute/data sovereignty + the $60bn Kigali-pledge-vs-reality case study; ILINA as proof of African-led
technical safety/eval work. **Strongest guest slot** — Rachel Adams (UCT-local), Vukosi Marivate,
Lelapa AI, or Cecil Abungu (ILINA).
**Reuse.** Gen AI Week 11 "Sovereign AI Capacity" + "Data, Languages & African Model-Building".
*(Agentic AI & long-horizon risk — reuse Gen AI Week 10 — moves to the Session 22 buffer or a reading
attached to Session 10's control material, freeing this slot for a guaranteed African-safety home.)*

## Week 10 — Project work + the skeptics

### Session 19 · Project clinic — *clinic*
Working session: proposal feedback returned, methodology help, scoping triage for teams still too broad.
Instructor + peers rotate between teams.

### Session 20 · Steelman the skeptics + open problems — *seminar*
**Objectives.** Argue the strongest case *against* the dominant AI-risk framing; identify genuine
open disagreements; practise calibrated uncertainty; name over-reliance/"illusions" risks.
**Pre-class.** Princeton COS 597Q "criticisms of AI-risk narratives" readings; Grosse "skeptical takes";
Messeri & Crockett, *Artificial Intelligence and Illusions of Understanding in Scientific Research*
(Nature 2024).
**In-class (structured debate).** Half the room is assigned to steelman skepticism, half to steelman
concern — then *swap*. Close on: which disagreements are empirical (resolvable by evidence) vs
definitional vs values-based?
**Reuse.** Gen AI Week 9 "Illusions of Understanding" + "Three Categories of Failure".

## Week 11 — Project work

### Session 21 · Mid-project check-in — *clinic + presentations*
Each team: **5-minute status** + structured peer feedback (one thing working, one risk, one ask). The
deliberate purpose is to catch over-scoping while it's still fixable.

### Session 22 · Project work / buffer — *clinic*
Office-hours clinic, OR a cohort-chosen deep dive / second guest (a natural home for **agentic AI &
long-horizon risk** — MCP, tool use, agent failure modes — reusing Gen AI Week 10, if not already
folded into Session 10). Intentional slack in the schedule — real projects slip, and the buffer protects
Week 12.

## Week 12 — Presentations & synthesis

### Session 23 · Final presentations + peer review — *presentations*
**Format.** ≈10-min talks + Q&A. Each student completes **anonymised peer reviews** of two other
projects (rubric-guided) — teaches reviewing and scales feedback. Reviews due 24h after.

### Session 24 · Presentations cont. + synthesis & pathways — *presentations + wrap*
Remaining talks; synthesis lecture (where the field is going; how the course's parts connect); concrete
pathways (ARENA, MATS, AI Safety Institutes, research groups, the UCT/African ecosystem); closing
reflection tying back to each student's Session-1 sentence.

---

## Build order suggestion (when we move to lessons/HTML)

1. **Sessions 4, 8, 12** first — they reuse Gen AI Week 3/4/11 content and prove the design-system
   transfer cheaply.
2. **Sessions 13–16** (mech interp) next — the labs are self-contained and Colab-tested.
3. **Sessions 1–3, 5–6, 9–11** — the new-build technical core.
4. **Project scaffolding (17, 23)** — the rubric, proposal template, and peer-review form as documents.

Run `/verify-references` per week before publishing, exactly as in the sibling course.
