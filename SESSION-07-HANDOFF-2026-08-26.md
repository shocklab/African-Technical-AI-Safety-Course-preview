# Session 7 — where to pick up

Paused 2026-08-26. Working tree clean, everything below marked DONE is committed and pushed
to `dev-origin/dev` and `preview/main`. **Session 7 is not released** (RELEASED-SESSIONS is
1–6), so none of it is student-visible yet.

---

## Start here

The next action is **building the 7.6 lab notebook**. Everything it depends on is decided and
the empirical work that shapes it is already done and recorded below. Do not re-run the probes
before reading the results section; they cost real CPU and the answers are here.

Estimated remaining: about two hours to a notebook executing end to end, then under an hour to
rewrite the 7.6 page around it.

---

## DONE and pushed

**7.2 corrected against Bai et al.** (`27b9579`). The page claimed the preference model
differed from 6.2's only in who produced the labels. The paper trains a "hybrid human/AI PM
(as we use human labels for helpfulness, but only AI labels for harmlessness)". Also fixed:
SL-CAI fine-tunes a *pretrained* model, not the one that generated the revisions, and mixes in
helpful samples "in order to retain helpfulness as much as possible"; the feedback model is
identified as independent and typically pretrained; non-evasiveness is no longer attributed to
critique-and-revise alone; the soft-label Bradley-Terry loss is now written down (6.2's loss
cannot consume a probability, and a class question depended on it); Bai section pointers
corrected from §2–4 to §3–4 in 7.2 and from §2–3 in 7.6.

**7.2 pipeline diagram** (`c199f76`). `tools/build_cai_diagram.py` →
`docs/assets/img/session-7-2-cai-pipeline.svg`, in the page as `figure.wide`. Built only after
the text was correct, so it depicts the real pipeline. Session 7 previously had no figure,
table or image across all six pages and one equation between them.

**7.5** no longer attributes "unreliable calibration off-distribution" to 7.3, which does not
contain it.

**5.2 and 6.1** (`dd4212b`) carry the OpenAI blog versions inside the mandatory entries as an
alternative way in, per Jonathan's call on Ben's suggestion, with the paper sections still the
required reading.

---

## DECIDED, not yet built

### The 7.6 lab rewrite — agreed shape

Convert from four build-it-yourself tasks to a supplied working notebook, as 2.5 / 5.4 / 6.5
were. Jonathan approved this shape:

1. **Critique-and-revise** as the opener. See the findings below: it does not work at 0.5B, so
   the plan is to ship it as a **pre-generated demonstration** with outputs already in the
   notebook, framed the way 6.5 frames its non-reproducing turnover.
2. **AI preference labelling**, with the log-prob extraction supplied rather than left to the
   student. This is the part that carries the lab.
3. **Vary the constitution** — a NEW task the current lab lacks entirely. Re-label the *same*
   pairs under a changed principle and watch the ordering move. This is the session's thesis
   and nothing currently tests it.
4. **The isiZulu probe: KEEP** (Jonathan's explicit call, against the reviewer's advice to cut)
   **but with a strong caveat and a capability control wired in**, so a student sees the
   comprehension score before interpreting any agreement number. This matters more than it did
   before the probes, because the judge is now known to be near-chance in *English*.

Cut: Task 1 as a task (make it a pre-filled editable cell feeding task 3), and the GPU
extension (it points at an ARENA track 6.5 never built).

### Model choice: Qwen2.5-0.5B / 0.5B-Instruct

Free Colab CPU is ~12.7 GB RAM and 2 vCPU, weaker than the M1 these probes ran on, so quote
Colab timings on the page and not local ones. fp32 weights: 0.5B = 2.0 GB (comfortable),
1.5B = 6.2 GB (over half the budget), 3B = 12.4 GB (**will OOM** — the current page's
"1–3B open model" is unsafe advice and must be replaced with a specific model).

The judge measurements are single forward passes with no generation, so they cost
milliseconds. Generation is the only expensive part, which is why demonstrating
critique-and-revise rather than running it makes the lab fast.

---

## MEASURED — do not re-derive

All on `Qwen/Qwen2.5-0.5B-Instruct`, greedy, CPU. Scripts in `tools/probes/lab-7-6/`.

**The log-prob mechanism works cleanly.** 98.6% of the probability mass lands on the "(A" /
"(B" tokens. The reviewer's worry that a small model would spread mass over hedging text is
not borne out. Read the two token ids directly and normalise.

**Position bias is near-total.** With the harmful answer in slot A, p(A) = 0.936; with the safe
answer in slot A, p(A) = 0.905. It answers (A) about 92% of the time regardless of content. A
consistent judge gives p₁ + p₂ ≈ 1.0; this gives **1.84**.

**Debiased, the judge is at chance on safety.** Averaging over both orders, preference for the
safe answer = **0.484**.

**The principle does move it, slightly.** Swapping the safety principle for a helpfulness one
takes that from 0.484 to **0.396**, in the right direction. So the constitution is doing
something small and real, swamped by position.

Those three numbers are a better lab than the page currently describes and should be its spine.

**Critique-and-revise does NOT work at 0.5B.**
- With the *instruct* model: it refuses up front, so there is nothing to critique, and the
  "revision" just re-refuses. Its critiques are incoherent ("The response does not discourage
  illegal or unethical activity at all... This aligns with the principle of providing
  actionable assistance toward harm").
- With *base* as generator and *instruct* as critic: the base model does attempt the request,
  which is the precondition the page correctly states. But the critiques come back garbled and
  **the revisions do not improve**. On the WiFi prompt the revision is near-identical to the
  original; on "find someone's home address" it gets worse, adding "the most straightforward
  and legal way to obtain their home address".
- Base outputs also leak training artefacts ("A single-select problem: Is the question answered
  in a satisfactory fashion? Options are: (1). yes (2). no"), same class of finding as 5.4's
  system-prompt leak. Possibly usable.

**1.5B was never measured.** `probe5.py` stalled at 94 MB of a ~3 GB download, twice. If it
matters later, run it directly rather than via `nohup &` inside a backgrounded tool call, which
kills the child. Swapping the model is a one-line change to the generator, so nothing built on
0.5B is wasted.

---

## ALSO OUTSTANDING for Session 7 (authorised, not started)

**The readings conversion.** Sessions 1–6 use "Mandatory / Optional" with per-item word counts
and a stated total; **sessions 7–24 all use the older "Core / Supplementary" with neither**.
Measured core load for Session 7 is **44,517 words**, against roughly 12,100 for the whole of
Week 3, which two students already called heavy. Per sub-session: 7.1 = 2,791, 7.2 = 4,862,
7.3 = 12,726, 7.4 = 9,179, 7.5 = 14,959–21,075.

The cause is fixable without cutting: 7.1, 7.2 and 7.6 name sections; 7.3, 7.4 and 7.5 describe
what a paper contains, which defaults to the whole paper. Adding boundaries takes 7.4 to 6,039
and 7.5 to about 9,500.

Traps found while measuring, to handle when adding pointers:
- Casper "§3 on feedback quality" is 5,329 words; only §3.1 (2,399) is about feedback quality.
- 7.6 cites Lee et al.'s "appendices" unqualified; the paper has fourteen. The two that matter
  are 667 words, a literal reading is 7,645.
- Huang et al.'s US-only admission is in §7 Ethical Consideration Statement, **not** §5
  Limitations where anyone would look. Not an error yet because no section is cited; it becomes
  one the moment a pointer is added.

**7.6 points at two things that do not exist.** It tells students to reuse "the harm-prompt
handling conventions from the 6.5 lab", and that convention appears nowhere in the course; the
frame it wants is in 9.4 (REJECT / BYPASS / UNCLEAR plus responsible disclosure). It also says
"Open the Colab notebook" and there is no notebook. Both die with the rewrite, but if the
rewrite is delayed, the ethics pointer is the one with duty-of-care implications: this is the
first lab in the course that puts a student in front of harmful prompts.

**Structural, needing Jonathan's call:**
- 7.1 pre-states 7.3's verdict verbatim (the sentence starting "A human-bounded reward model
  was capped at human judgement" appears on both pages), which deflates 7.3's payoff.
- The African-lens point runs three times in near-identical words across 7.1, 7.3 and 7.4, with
  the payoff promised twice.
- 7.5 is orphaned by 7.1's "one technical and one normative question" framing; it answers a
  third question 7.1 never raises. One clause in 7.1 fixes it.
- Session 7 is the only session in the course carrying both an in-class paired activity and a
  lab.

---

## What came back clean

Worth knowing, since the above is all problems. Around twenty factual claims were checked
against primary sources and essentially all are exact, several to the decimal: Yong et al.'s
Table 1 values, Lee et al.'s percentages, Huang et al.'s participant counts, and a correct
attribution of "participation-washing" to Sloane rather than Birhane. All 21 external links
resolve and all 15 arXiv IDs match their cited titles and authors. One reviewer finding was a
**false positive**: 7.3's "the authors expect the effect to saturate" IS supported — Yuan et al.
say "While this effect likely saturates in real-world settings" twice, outside the Limitations
section where the reviewer looked.
