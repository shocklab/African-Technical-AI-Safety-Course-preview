# Writing conventions — what to avoid

The course grades students on thinking clearly and checking claims against sources. The prose should
model that. This file is the course-specific layer; the global canon at `~/.claude/writing-tells.md`
still applies underneath it.

The fix is almost always **subtraction**: cut the word, keep the sentence. If a flagged word is the
right word, keep it — this is a prior, not a ban.

## Work in this order

AI-writing tells stack in layers, and readers notice them in roughly this order:

1. **Formatting density** — em-dashes, bold. Visible before a word is read.
2. **Headings and structure** — what the section titles promise, the shape of every page.
3. **Sentence-level constructions** — contrastive reframes, self-labelling.
4. **Vocabulary** — the banned-word list.

The first sweep (2026-06-25) did layer 4 first and reported success; a reader still found the LLM-isms
"quite intense and distracting." Layer 4 is the layer a reader least consciously notices. **Do 1 and 2
before 3 and 4.**

---

## 0. Headings name things; they do not editorialise

A heading says what the section contains. It does not preview the argument, tease the twist, or tell
the reader what to feel. If a heading needs a comma-and clause, that clause belongs in the prose.

Kill these four families:

| Family | Example (real) | Instead |
|---|---|---|
| **"X, and Y"** compound | "The results, and the caveat that matters" | "Transfer results" |
| **"X — editorial gloss"** | "Reading what a model knows — and the refutation" | "Reading what a model knows" |
| **"X, not Y"** | "Two gaps, not one" · "Calibrated, not tribal" | "Two gaps" |
| **"honest/honesty"** headings | "Defences, and the honest verdict" | "What the defences deliver" |

**Minimise `What…` / `Why…` / `How…` openers** where a noun phrase will do ("Why exact unlearning is
infeasible" → "Exact unlearning"; "What the attack costs" → "The cost of the attack"). Not a ban — the
Wh- form is sometimes the clearest label — but it should be the exception, not the default.

**Keep** dash-*labels*, where the dash separates a label from its content rather than adding
commentary: `Step 3 — Scale by √d_head`, `Task 1 — the English baseline`, `Anthropic — RSP`,
`Failure mode 2 — mismatched generalisation`, `Trusted monitoring — 62% / 97%`.

**The pre-summary lead line.** 44% of section headings are followed by a `<p class="lead">` that
summarises the paragraph below it. That is a narrator standing outside the material telling you what
you are about to read. Use it sparingly — where it genuinely orients — not as the default under every
heading.

### The title layer counts, and it is not `index.html`

These rules govern `<h1>`, `<title>` and the contents-page link text, not only
`<h2 class="section-title">`. The de-slop sweep protected the title zone on the false theory that it
cascaded into nav (nav is regenerated from `docs/index.html`), so the titles kept every tell the sweep
stripped from the prose underneath them. Eighteen renames on 2026-07-17 (`01b7c94`) cleared the four
families above plus a fifth: **vague tails that name nothing** — "& the frontier", "& its limits",
"& the African angle".

**Census the `<h1>`s. `docs/index.html` is an abbreviation of the site, not a description of it.**
Seven pages carried a longer or different `<h1>` than the index advertised, and two confident diagnoses
built off the index were simply wrong: 10.3's "the frontier" is really "the safety/usefulness frontier"
(a genuine Pareto frontier from the control literature), and 7.3's dangling "its" was the index's own
invention, absent from the page. The index was the artefact being fixed, which made it the worst
available source on what to fix.

**Check a word's usage across the whole corpus before calling it a tell.** "The African angle" in
16.4's title looked like an own-goal, because 18.1 refuses a "manufactured angle". It was not. *Angle*
is this course's term of art: `The African-lens angle:` is a recurring section heading (Sessions 9, 10,
13), and the positive uses are everywhere — "the one strong angle here, backed by a verified result",
"the thinnest African angle in the course", "the (thin but real) sovereignty angle". The pejorative is
*manufactured* angle, not *angle*. Acting on the single grep hit cost a subtitle rewrite that silently
broke a deliberate echo between 16.3 and 16.4, and had to be reverted. **One hit is not a usage
pattern.** The 16.4 title was still worth changing — it was a three-item compound, and 16.3's own prose
already called the page "interpretability and sovereignty" — but for that reason, not this one.

**Three zones must agree:** `<title>` == `<h1>` == contents-page link. Since the 2026-07-18
adjudication (all pages agree), two policies Jonathan set govern the winner: **"and" over "&"** in
titles, and **the contents page carries the full title**, never an abbreviation (the abbreviations are
what made the index lie; see above). Adjudication rule when zones disagree: apply §0 to the FULLEST
form, then use the winner in all three zones. Residue Jonathan has not yet ruled on: ~20 older titles
still use "&" (13 sub-sessions, 7 session groups); they were internally consistent so never surfaced.

## 1. Density budgets, measured — not per-paragraph rules

The old rule was "em-dash ≤ 1 per paragraph, or one genuine paired parenthetical." Every page passed
every check, and the site still had **1,539 em-dashes in 118,619 words (13.0 per 1,000)**, with 58% of
paragraphs containing one. A per-paragraph cap cannot control global density: 1,633 compliant
paragraphs still produce 1,539 dashes.

Budget against the whole corpus, and measure it:

| Signal | Was | Budget |
|---|---|---|
| em-dashes | 13.0 / 1k words | **zero** — a comma, colon, semicolon, full stop or parentheses always serves |
| `<strong>` | 12.9 / 1k words | **≤ 3 / 1k** — bold only to introduce a technical term on first use, **never for emphasis** |
| "X, not Y" contrasts | 2.2 / 1k | **delete-test floor** — measured 1.5/1k after the 2026-07-18 triage; see below |
| inline-header list items (`<li><strong>Label.</strong> …`) | 462 | convert to prose where the label adds nothing |

**Why zero, and not "a few".** Jonathan's voice profile has always said no em-dashes, in any register
(spaced hyphen informally, parentheses in papers). Zero is also the only version of this rule that
greps cleanly: no denominator to argue about, no threshold to creep toward. "≤2 per 1,000" is exactly
the species of rule that drifted to 13.

Two guards when counting. Do not accept the **evasions**: an en-dash or a spaced hyphen doing an
em-dash's job as sentence punctuation is the same tell in a false moustache. And do not flag
**en-dashes in ranges or compound names** (`0.1–8 Wh`, `pp. 610–623`, `Bradley–Terry`,
`Mori–Zwanzig`); those are correct typography, and flagging them is a false positive.

**≤3/1k is a prior, not an arithmetic target.** A page that is structurally an enumerated taxonomy
(8.4's Gabriel-six-targets and Arrow-four-conditions blocks; 13.2's feature definitions) will exceed
it legitimately, because every bold there is a technical term at first use, which is exactly the
sanctioned carve-out. De-bolding definitions to satisfy a grep would delete the only job bold is
still allowed to do. The number to drive to zero is **emphasis bold**; the carve-out is not a leak.

**The bold budget governs prose only; site furniture is exempt.** These are template conventions, not
emphasis, and changing any of them is a **site-wide decision, never a per-page one** — de-bolding four
pages desyncs them from seventy. Exempt:

- **Reading-list citations** (`<strong>Author (year), "Title"</strong>` inside `.resource-placeholder`).
  A bibliographic convention with CSS built to support it: `.resource-placeholder a{font-weight:400}`
  exists precisely so links don't double-bold inside it. ~139 instances site-wide.
- **The `ai-notice` `<strong>Note:</strong>`** boilerplate, identical on all 78 pages.
- **Next-box sub-session cross-refs** (`<strong>10.2</strong>`).
- **`<td><strong>` table row-labels**, which are row headers doing `<th scope="row">`'s job. (The
  correct fix is the HTML, not the bold; that's a separate structural job.)

In **running prose** the target is effectively zero: bold only to introduce a technical term on first
use, never for emphasis.

Measure with `node tools/score-pages.js docs` (vendored detector) and the census script. The detector's
*score* floors out on academic prose, so ignore it; its `em-dash` and `low-ttr` flags are the useful part.

## 2. The dominant sentence-level tell: telling the reader how to feel

We label our own points as important, clean, strongest, cleanest, the lesson, the headline — instead of
stating the thing and trusting the reader to judge its weight.

Real examples, all to be cut:
- "the single cleanest epistemics unit in the block", "the high-water mark of the evidence"
- "the arc is the lesson", "worth teaching exactly", "the line to put on the slide"
- "load-bearing", "the headline", "the punchline", "the point is", "the move", "the prize", "the catch"

**Rule:** state the claim; delete the label. Also in this family: **pedagogical meta-commentary** ("we
teach this as…", "hold that thought", "in one sentence", "notice that"). Cut the frame, keep the content.

## 3. Contrastive reframes, including the "X, not Y" apposition

"not just X but Y", "not merely X", "it's not X, it's Y", "X isn't Y; it's Z". Rewrite as a direct
statement, or just say what it is.

The commonest form is the bare apposition: "a stage, not a destination", "engagement, not tokenism".
Census 2026-07-18: **244 instances (2.2/1k words)** — a reader meets one every ~450 words, which is
the rhythmic signature Ben felt without naming. Apply the **delete-test** (ruling, 2026-07-18):
delete ", not Y" and see whether the claim survives. "In a week, not a month" dies with the deletion
(the contrast is the content) — keep it. "A stage, not a destination" survives (the contrast was
decoration) — rewrite to state the claim directly. Triage, never purge; the budget is the §1 row.

**Why the floor is ~1.5/1k here, not the ≤0.5 first guessed.** The 2026-07-18 sweep triaged all 244
instances; 74 died as decoration and 170 survived the delete-test, because this course's content IS
distinctions: "suppressed, not removed" (the unlearning finding), "a probability against a specified
attack, not a property of the model" (the control paradigm), "learn from preferences, not
demonstrations" (RLHF's premise). A safety course argues by contrast, so its legitimate density sits
above generic prose. The number to watch is decorative survivors, not the total: if a new page pushes
the corpus above ~1.5/1k, delete-test the additions.

## 4. The course narrating itself

The pattern behind Ben's 2026-07-17 feedback: the course keeps talking about itself — narrating its
own design, labelling its own virtues — instead of teaching. It reads as AI because it is the
drafting model explaining its outline, and it leaves the reader unsure which choices were the
author's ("undermines my trust"). Three surfaces, censused 2026-07-18:

- **Course-as-agent with intent or virtue** (88 hits): "the course moved deliberately from…", "the
  course spent weeks on…", "the kind of manufactured angle this course refuses". Delete the
  meta-commentary or state the content directly ("Weeks 2–8 covered…"). Plain navigation ("this
  session covers X") is fine in moderation; the tell is intent and self-praise, not signposting.
  A synthesis page (S24) legitimately takes the course as its subject — there the cut is the virtue
  language, not the reference.
- **Intentionality and virtue adverbs**: "deliberately" almost always goes; "honest/honestly" per §6.
- **Framing arrows** (~10 of 51 arrows): "Idealised → empirical" as conceptual scaffolding. Write
  the words ("from idealised models to empirical practice"). **Keep pipeline arrows** — "Tokens →
  embeddings", "thresholds → evals → mitigations" are notation, not rhetoric.

## 5. Intensifier filler — cut unless literal

| word | keep only when… |
|---|---|
| exactly | literal ("exactly one fixed point") |
| genuine / genuinely | (almost never — delete) |
| precisely | literal ("precisely when λ = 0") |
| the whole | literal ("the whole matrix") |
| worth (…ing) | rarely; "worth teaching" is meta — cut |
| truly, really, simply, just, actually | delete |

## 6. "honest" / "honestly" — the ethos word, overused

Ruling (2026-07-18): protect **"intellectual honesty"** — a named through-line and a grading
criterion — and honesty as subject matter (model honesty, "why 'be honest' resists SFT"). Kill the
**adjective-badge**: "an honest safety project" → "a safety project"; "the honest position is X" →
state X and let it stand. Cut the reflexive adverb ("it is honestly a modest one"). Not in headings
(§0). The 2026-06 sweep de-honested headings only; the prose carried 180+ residual lexicon hits.

## 7. Essayist tics — replace with plain words

`lands` (figurative), `rhymes with`, `cash out`, `earn(s) its keep`, `the spine / spine of`, `the
wedge`, `the through-line`, `tee up`, `reckoning` → "account", `the uncomfortable X`, `a clean X` /
"clean demonstration", `vivid`, `hold that / hold onto`, `in one sentence / in one line`.

Boundary (per the §0 angle lesson): **"through-line" is also course architecture** — 1.1 names four
through-lines and Session 24 revisits them under that name. Keep those structural references; cut the
word as casual filler elsewhere. "Spine" has no such status (Ben quoted it as a tell); always cut.

Also (from the borrowed lists, and real here): **copula avoidance** — "serves as", "features",
"boasts", "presents" where "is" or "has" would do.

## 8. The global canon still applies

Everything in `~/.claude/writing-tells.md`: delve, leverage, harness, underscore, bolster, foster,
robust (figurative), comprehensive, seamless, intricate, nuanced, multifaceted, holistic, pivotal,
groundbreaking, transformative, testament, realm / landscape (figurative); connective-adverb stacking
(Moreover, Furthermore, Additionally); pseudo-depth openers (At its core, In essence, Fundamentally);
participle fake-depth ("highlighting its importance"); significance adverbs (crucially, notably,
importantly); rule-of-three padding; sentence-case headings; no decorative emoji.

## 9. Keep — legitimate terms that look like tells

- **robustness / robust** — the field's name for the Session 9 subject. Keep as the technical term.
- **honest / honesty** — as **intellectual honesty**, the named through-line, and as subject matter
  (model honesty); never as an adjective-badge (§6).
- **by construction** — legitimate maths phrasing where literally true.
- **necessary but not sufficient** — standard logic phrase.
- **superposition, circuit, feature, induction head, residual stream, …** — technical vocabulary;
  never "vary for elegance". Use the reader's term and reuse it.
- **"drops sharply"** and other literal uses of `sharp`.
- Dash-*labels* in headings (§0), and paper titles quoted verbatim.

## 10. How to apply it

Surgical edits: change the flagged word or phrase, not the surrounding sentence. Never touch text
inside HTML tags, inside MathJax (`\(…\)`, `\[…\]`), or inside code. Preserve every citation, number,
and technical claim verbatim. Don't introduce a new tell while removing an old one. After a pass,
re-run the census and confirm the densities fell.

## 11. Authoring new pages: apply the rules at draft time

Sweeping after the fact costs ten times what writing clean costs. The 2026-07-18 additions (7.5, the
2.4 takeoff section, the 3.4 scheming blocks) were written under these rules and needed no cleanup:

- Whether authoring yourself or briefing an agent, put the binding style rules **inline in the brief**
  (no em-dashes or their evasions; no emphasis bold; factual sentence-case headings; delete-test on
  contrasts; British spelling). Pointing at this file is not enough; paste the constraints.
- **Only pre-verified links.** Verify every URL resolves AND its title matches the work you cite
  before writing the sentence around it, and forbid the agent from adding links you did not supply.
- **Describing an external document means fetching it.** The 7.5 page's account of the OpenAI Model
  Spec is trustworthy because the agent fetched the current spec and the 2024 original; paper claims
  come from the fetched abstract, never from memory. Make this an explicit instruction in every
  authoring brief, and require the agent to report what it verified.
- **Follow sibling conventions, including mirrored furniture** (manifest lines, Next boxes, dash-label
  h4 patterns within a page). A new element should be indistinguishable in register from the page it
  joins; when a page already uses a convention (for example its case-study h4 dash-labels), match it
  rather than importing a different one.
- Require a tag-balance check (every tag the page uses, including span and iframe) before the agent
  reports done.

## 12. Alignment with Ben's style guide

Ben edits with his own GOV.UK-based guide
(https://gist.github.com/BenSturgeon/5424796ffd3bd2b0548501d4c1412c88), applied via his tools. It
converges with this file on the load-bearing rules: no emphasis bold, sentence-case headings,
everyday words, no metaphor filler (his list names robust, key, landscape, deep dive). Adopted from
his guide into ours:

- **No orphan jargon.** Every technical term gets a real one-to-two-sentence definition at first
  use, not just an acronym expansion.
- **Breathing room as a prior for new prose.** Shortish paragraphs, subheadings at regular
  intervals, series broken into lists, and never bold as paragraph glue (which is §1's label-bold
  rule from the other side).
- **Every number needs a referent** — units, denominator, comparison. The course already holds
  this; his guide states it well.

Accepted divergences, so neither side "fixes" the other: his 15–20-word sentence cap suits docs
and wikis; this course's textbook register runs longer sentences deliberately, and his edits that
split overlong colon-chains are welcome without adopting the cap globally. His no-question-mark
headings rule yields to §0's allowance for genuine question headings ("Whose constitution?").

## Sources

Borrowed selectively, all MIT: [stop-slop](https://github.com/hardikpandya/stop-slop) (structural
antipatterns; the 5-dimension score), [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)
(53 categories; the detector vendored in `tools/aiwriting-detector/`),
[humanize-writing](https://github.com/jpeggdev/humanize-writing) (the pass order), and fofr's GOV.UK
style gist (front-loading; **no bold for emphasis**). Taken as priors, not gospel — several of their
rules (never use em-dashes at all, no Wh- starters, no adverbs) are too blunt for technical prose.
