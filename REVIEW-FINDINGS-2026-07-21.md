# Full-course review — consolidated findings (2026-07-21)

Eleven parallel reviewers over the complete dev-branch course (eight content blocks, one
corpus-writing pass, one cross-session coherence pass; every reported factual claim verified against
a fetched source by the reviewer, and the two largest single-source claims re-verified by the
orchestrator). Verdict in brief: **the quantitative and scholarly core is overwhelmingly sound** —
dozens of load-bearing numbers (control game, GCG, Chinchilla, IOI, SAE, eval statistics, isiZulu
figures) re-verified verbatim against their papers. The real findings are **currency** (the field
moved during 2025–26), **import seams** (pages ported from the sibling course), **a small number of
genuine errors**, and **assessment logistics**. Severity: high = wrong/misleading as taught;
med = dated or missing something important; low = polish.

Fix workflow: all edits go to the `dev` branch; released weeks reach public main via
`tools/release.py sync` / `release.py N`.

## A. Decisions only Jonathan can make

1. **Week badges (PUBLIC NOW).** Badges currently read W1={S1}, W2={S2,S3,S4} — three sessions in
   one week, contradicting 1.1's "two sessions a week" and 2.5's own "Week 1 summary" text.
   Presumed fix: Week 1 = Sessions 1–2 (relabel Session 2's five badges + 1.1's "Week 2 rebuilds
   the transformer" card). **Confirm the real timetable direction.**
2. **Final-presentation weight.** S23 calls the presentation "assessed" but no page gives it a
   weight or criteria (1.1's table has none; the project rubric has no talk row). Decide: inside
   the project 40% (against what criteria), or required-but-unweighted.
3. **Peer-review logistics.** No page states when papers are due, how review assignments are
   distributed, or when reviews are due (S23 requires completed reviews *before* the session).
   Needs your timetable dates.
4. **Project rubric marks split.** 1.1 promises "an itemised, per-section rubric" but neither
   rubric table allocates marks across the six sections. Equal weights, or a split?
5. **Sentence templates (advisory).** The corpus pass identified repeated sentence shapes the
   census can't see (the "That is X…" demonstrative-verdict close on ~half of pages; the
   "Three details sharpen…" enumerative preamble; the box-carousel pages). Decide whether to
   treat as voice or sweep the worst pages.
6. Still open from before: the ~20 "&"-titles; the per-session student-experiment format;
   S20 mental-health readings.

## B. Public now (Sessions 1–4 + root) — fix and `release.py sync`

- **1.2 [med]** Concrete-Problems mapping sends robustness to "Session 5" → should be Session 9.
- **1.2 [med]** UK/US institute renames: AI Safety Institute → AI Security Institute (Feb 2025);
  US AISI → CAISI (Jun 2025). Add parenthetical renames (also 11.1 hedges this — fix there too).
- **1.3 [low]** "Bostrom's hardware-advantage version appears with 3.2's readings" — unfulfilled
  (that material is Superintelligence ch. 3, not the listed readings). Repoint or drop.
- **1.3 [low-med]** "X, not Y" at ~5.2/1k incl. "calibrated, not tribal" (verbatim in STYLE.md §0's
  kill table) and "advocacy, not education", "a finding, not a failure". Delete-test triage.
- **1.4 [med]** Two "recall from Session 2.2" references are forward references for a Week-1
  student. Rephrase as "Session 2.2 will show…".
- **1.4 [low]** "three to five times as many tokens" is unsourced and dated (Petrov et al. 2023 is
  the natural citation; o200k reduced non-English fertility). Fold into the planned recalibration.
- **2.2 [low]** "vocabulary typically 30k–100k" dated (Llama 3: 128k; GPT-4o ~200k). One clause.
- **2.3 [med]** Chinchilla taught as "the rule" without the overtraining-for-inference reality
  (Llama 3 8B: ~1,875 tok/param, ~75× compute-optimal). One distinguishing sentence.
- **2.4 [med]** Add METR task-completion time horizons (arXiv:2503.14499, ~7-month doubling) as the
  measured *output* pace metric beside compute — it answers the section's own question.
- **2.5 [med]** Lab parts ① and ② name a loss table and the Epoch CSV that are neither provided
  nor linked; part ③ never names the tokenizer. Link/provide before Week 1 ends.
- **2.1 [check]** Verify the Karpathy embed timestamps play the claimed segments (unverified).
- **3.1 [low]** Session-opening box says "four-step skeleton" of 1.3's argument; 1.3 has five
  claims, and the omitted one is 3.3's own topic. Restore the fifth.
- **3.2 [low]** Bostrom quote uses "realised" where the PDF has "realized" — quotes verbatim.
- **3.3 [med]** "As of 2024, partly both…" — editing remnant answering an unasked question; also
  stale date. Rewrite the box opening.
- **3.3 [low]** Link-first candidate: Rob Miles mesa-optimiser videos (both URLs verified) as a
  Core-material box per the 2.1/2.2 pattern.
- **3.4 [med]** Section lead still says "Two 2024 papers" above three case studies. → "Three".
- **3.4 [med]** Add the 2025 alignment-faking follow-up (arXiv:2506.18032: only 5 of 25 models show
  compliance gaps; goal-guarding consistent only in Claude 3 Opus) — one sentence + citation in the
  caveat paragraph, else students read a model-specific result as generic.
- **3.4 [low]** Heading "Training against scheming, and the measurement trap" is a §0 "X, and Y"
  compound (today's own authoring). → "Training against scheming".
- **S4 (all) [high]** SEC climate-disclosure rule taught as in force; it was stayed (2024), defence
  abandoned (Mar 2025), rescission proposed (Jun 2026). Teach the collapse as the fragility example.
- **S4 [med]** Session-3-era residue: 4.2 "(as discussed in 3.1)" → 4.1; 4.1 "3.3 returns to those"
  → 4.2/4.3; 4.4 intro recaps only 4.1+4.2, omitting 4.3.
- **S4 [med]** Ritchie citations conflate her Nov-2024 WEO-2024 post with the 0.5% estimate that
  lives in her 2025 summary; 4.2 juxtaposes 223 TWh (WEO 2024) with IEA 2025's 485→950 as if one
  source. Re-link and re-attribute.
- **S4 [med]** Gallium "~80% from China" → ~94% production / ~98% refined (stated twice).
- **S4 [med]** 4.2 cites the superseded IEA 2024 ~1,000 TWh-by-2026 projection directly above the
  2025 revision — delete or reframe explicitly as projection-revision case study.
- **S4 [med]** Add the 2024–26 China export-control arc (Dec 2024 Ga/Ge/Sb ban; Apr+Oct 2025 rare
  earths; Nov 2025 suspension-as-dial) — the strongest evidence for the page's own thesis.
- **S4 [low]** NVIDIA "1,000× per decade" doesn't match any NVIDIA claim (their marketing says
  45,000–100,000×); re-attribute. "Duman-Keles COLT 2023" → ALT 2023. 4.2 missing "are" (grammar).
- **S4+S8.2/8.3 [med, writing]** The six ported pages are an earlier stylistic generation:
  Title-Case headings + bold at 13.9–19/1k (132 of the corpus's 253 remaining label-bolds on S4's
  three content pages). One restyle pass brings the whole corpus inside budget.
- **Index [low]** gate_index() leaves the dev intro line ("the rest are in preparation" — false)
  alongside the injected release note, and keeps "built" badges on released entries while gated
  plain-text entries lose .soon styling. Tidy the generator.

## C. Ahead of release, by week

**Week 3 (S5–6):**
- **5.3 [high]** Add RLVR as a distinct post-training stage (programmatic rewards; verifier-hacking
  as the new Goodhart surface; compute no longer "comparatively tiny") — Tülu 3 (2411.15124) +
  the elicit-vs-extend debate (2504.13837). Scope 6.1's "RLHF doesn't make the model smarter" box
  to preference-based RLHF; let 6.4 name verifiable rewards as the third oversight-escape route.
- **6.4 [med]** Add the GPT-4o sycophancy rollback (Apr 2025, OpenAI's own postmortems) as the
  production case study of 6.4's exact mechanism.
- **5.4 [med]** nanochat lab: gpt2-vs-Qwen-instruct confounds era with tuning → use Qwen2.5-0.5B
  base vs instruct; and show the messages-format call (raw strings skip the chat template).
- **5.3/6.2–6.3 [med]** Link-first candidate: rlhfbook.com (Lambert, maintained, covers RLVR).

**Week 4 (S7–8):**
- **7.2 [high]** Position-swapping misattributed to Bai et al. — it is Lee et al. 2023 (verified by
  full-text search of both). Also flip 7.3's "same two refinements from 7.2" sentence.
- **7.2 [med]** Claude's production constitution conflated with the paper's ad-hoc Appendix C
  research principles. Separate them.
- **8.3 [high]** Closing "Next session" promises the Gen-AI course's syllabus (authorship, IP,
  privacy) — rewrite to hand off to 8.4.
- **8.2 [high]** Six stale "Sub-Lesson N" cross-refs from the source course; readings scoped to a
  week that doesn't exist here ("six supplementary readings" lists five). Renumber/re-scope.
- **8.2 [med]** The four lenses are never applied to an alignment target (8.4 claims they were).
  Add one alignment-flavoured worked case in the existing four-card format.
- **8.2/8.3 [med]** No "Questions to bring to class" (only pages in the block without them) +
  the restyle in B above.
- **8.1 [low]** Sandwiching: "proposed by Cotra (2021), operationalised by Bowman et al. (2022)"
  (Bowman's own attribution).
- **7.4 [med]** GPT-4-era jailbreak framed present-tense — same calibration as the 1.4/18.2 plan.
- **7.4 [low]** Conitzer cited under a wrong title (8.4 has it right). 7.6 [low]: cut "the lab no
  surveyed course offers"; Task 4 should name the MT tool and the translation-vs-judge confound.
- **7.5 [low]** "Two other structural features" introduces three.

**Week 5 (S9–10):**
- **10.3 [high]** Circuit Breakers citation: wrong table number (5, not 6) AND the data shows the
  opposite direction (undefended Zulu ASR 6.6%/4.6% vs ~50% HRL — lowest, via the comprehension
  confound; the paper explicitly says the Yong et al. pattern does not appear). Rest the monitor
  argument on the general principle; stop citing this table as positive evidence.
- **9.4 [med]** Same data implies the lab's predicted isiZulu refusal-gap is often null/reversed on
  1–3B models — reframe so the confound is the honest expected lesson.
- **9.2/9.5 [med]** Add "beyond GCG": AutoDAN (fluent, survives perplexity filters — resolving the
  page's own open question) and PAIR (black-box, ~20 queries).
- **10.3/10.4 [med]** Add Ctrl-Z / BashBench (2504.10374): agentic control eval, resample protocols
  beating everything 10.3 teaches (58%→7% at 5% cost); soften 10.4's "single testbed".
- **9.1/9.3 [med]** More present-tense isiZulu instances → the recalibration list.
- **9.3 [low]** Wei et al. numbers silently pair two different combinations → 0.93/0.87.
- **9.1 [low]** Szegedy year inconsistent within the page (2013 vs 2014).
- **10.2 [check]** The toy upfront-auditing derivation may peak at ~10% not the paper's 15% — a
  sharp student will notice; present the toy result as approximate (unverified suspicion).

**Week 6 (S11–12):**
- **S12 [high]** "All three frameworks are voluntary" is false since SB 53 (late Sep 2025) and the
  EU AI Act GPAI obligations (in force Aug 2025). Keep the self-graded/verification-gap argument;
  retire "voluntary".
- **S12 [med]** FSF reading points at superseded v1 (now v3.x); METR "Common Elements" now Dec 2025
  (twelve companies) — also softens "the three real frameworks". ASL-3 activation (May 2025) as the
  documented if-then instance. Fix the stale "(Weeks 5 and the Session 22 agents material)"
  parenthetical (confirmed twice). Add a questions section (only non-project session without one).
- **11.2 [med]** Add evaluation awareness as a named threat to eval validity (Schoen et al. +
  Apollo's mission list) — the main 2025–26 development in the sub-session's own topic.
- **11.1 [med]** Apollo does not do "white-box" evals (their own description; the page's own 2×2
  agrees). **11.3 [low]** The Raji children's-book anecdote misdescribes the book (Grover; the
  "Everything Else" door). **11.5 [low]** Vulavula needs a setup line + NLLB-only fallback.

**Weeks 7–8 (S13–16):**
- **15.4/16.3 [med-high]** Add "after SAEs": cross-layer transcoders + attribution graphs
  (transformer-circuits 2025 circuit-tracing + biology posts; the multilingual-circuits result
  feeds 16.4 and 13.4 directly). Update 16.3's "2023 Chinchilla" scale story.
- **13.2 [med]** Sparsity inversion: the paper defines S = P(feature is zero); the page calls
  activation probability p "sparsity" and the class question then teaches the inverted
  association. Rename p, reword the question (confirmed by two reviewers).
- **S14 lab [med]** Single-head ablation prediction contradicts 15.2's backup-heads teaching →
  ablate all top scorers, predict partial degradation, forward-link to 15.2.
- **S14 lab [med]** TransformerLens 3.x has deprecated the legacy API the lab uses (v3.5.1) — pin
  a known-good version and test that attn-only-2l loads under it before Week 7.
- **S14/16.1 [med]** Link the verified learn.arena.education chapter pages (old streamlit URLs are
  dead — sweep for stale ARENA links course-wide).
- **13.1/13.4 [low]** "more like neuroscience" is in quotation marks but is not a quote in either
  cited source. **13.4 [low]** Copying score: define as Σλ/Σ|λ| (magnitude-weighted), note the
  paper's primary evaluator is behavioural. **15.4/16.1 [low]** Two stale-but-working URLs
  (GDM post slug; SAELens moved to decoderesearch).
- **16.2 [med, writing]** The label cluster: "clean win/clean demonstration/cleanest evaluation",
  "high-water mark" (verbatim on STYLE's cut list), "What makes this teachable:". Cut.

**Weeks 9–12 (S17–24, 18/20):**
- **18.4/18.1 [high]** ILINA-exclusivity claims false: AI Safety South Africa (Cape Town,
  frontier register, 13 programmes — verified twice). Rewrite "a standout, not a crowd" and add
  AISSA to the map and project hook. (AI Safety East Africa's site currently fails to resolve.)
- **18 [high]** Add "Toward an African Agenda for AI Safety" (arXiv:2508.13179 — Segun, Adams, …
  Shock, … Abungu; five-point plan incl. an African AI Safety Institute). The convenor's own most
  on-topic paper, currently absent from the course.
- **18.3 [high]** Birhane core-reading link dead at source → https://doi.org/10.2966/scrip.170220.389
  (verified) or arXiv:2008.07087.
- **18.3/18.4 [med]** S12 promises Session 18 covers Kigali/$60bn ambition-vs-infrastructure —
  nothing in S18 does. Add a calibrated passage (or soften S12). Add the Cassava–Nvidia build-out
  sentence (12k GPUs by Nov 2025; why it doesn't yet change the audit argument). RIA "Just AI" is
  led by Pria Chetty (not Gillwald, per RIA's page — NOTE existing memory on the licence issue).
  Indaba founding: credit the eight-organiser team, not only the London pair.
- **18.1/18.4 [med]** More present-tense isiZulu framing for the recalibration ("clearest single
  demonstration"), plus the writing densities: "genuine" ×5 on 18.4, honest-badges, X-not-Y at
  ~7–8/1k with duplicated contrasts across 18.1/18.4.
- **20.1 [med]** The octopus is misdescribed: the human asks for a way to build a weapon; she does
  not send instructions (generating them is what the octopus fails at). **20.3 [med]** "the same
  four from 1.4" — 1.4's checklist has five different items; the four echo 1.1. Repoint.
- **20.1 [low]** "Honesty cuts both ways" lead-badge. **18.4 [low]** Okolo reading names no work
  and has no link (only such reading in the block).
- **S17 [med]** Nanda's 200 Open Problems carries the author's own 2024 deprecation → add his 2025
  "How To Become A Mechanistic Interpretability Researcher" as core (verified); fix the ARENA
  homepage link + the unlinked "Concrete Steps" reading. Add paper length + talk length to the
  kickoff page; reconcile "three weeks" vs "four weeks"; add 11.5's capability control to the
  language-extension track.
- **S24 [high→confirmed twice]** "Weeks 2–4 / 5–16" are session numbers wearing week labels.
  **S24 [med]** BlueDot rebrand (aisafetyfundamentals.com → bluedot.org; restructured) + "drawn on
  throughout" overstates. **S24 [low]** "This sub-session" on a single-page session; "earns its
  place". **S22/S23 [low]** "earns its keep", "make one point land", US "practiced", S17 "the move
  the course has practised".

## D. Corpus writing (beyond the per-page items above)

1. The six-page ported-block restyle (B) is the one structural writing fix.
2. Five §0-violating headings: 3.4 (B), "Arrow's theorem, and a cycle you can check by hand" (8.4),
   "Goodhart, pre-loaded" (6.2), "The calibrated take" (2.4), "The course in one sentence" (S24).
3. Page-level "X, not Y" concentrations for delete-testing: 1.3, 8.3, 18.1/18.4, 9.4-lab, 4.1.
4. Sentence templates (A5, decision): demonstrative-verdict close, enumerative preamble, "sharpen"
   family, colon-verdict, box-carousel pages (S12, S4), the case-study calibration coda in 3.4,
   2.4's three stacked closing info-boxes.
5. Course-as-agent virtue residue (~12 instances listed by the corpus pass).

## E. Verified sound (the reassurance)

All of today's new content (Four Background Claims table, takeoff numbers, all scheming figures,
the whole 7.5 page) verified claim-by-claim by reviewers who did not write it. The control game,
GCG, FGSM, Chinchilla arithmetic, IOI (3.56 / 99.3% / 26 heads / 87%), toy-models, SAE numbers,
eval statistics (re-derived), isiZulu 79%/53.08% chain, Collective CAI details, TESCREAL/AI-Now
quotes, AU strategy claims, Kigali status, assessment arithmetic, all nav chains, and every
internal link (901) and external link (except noted) verified. Colab feasibility of every lab
checked individually. Memory note: RIA Just AI licence ambiguity is already recorded and unchanged.

## F. Unverified suspicions worth a one-off check

10.2's toy-derivation optimum (~10% vs the paper's 15%); the 2.1 Karpathy timestamps; Golden Gate
language list; the 0.3 Wh Google-search figure's 2009 provenance; 4.1's water-household equivalence
and 12–13% cooling split; polysilicon solar-vs-semiconductor grades; Gupta scope claim; Masakhane
founder attribution; whether Grosse's Notion page still carries the Lecture-12 reading set.
