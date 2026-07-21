# Shared brief — full-course review, African Technical AI Safety (2026-07-18)

You are one of several reviewers, each assigned a block of sessions. Everything below applies to
every reviewer. Your assignment (which sessions, any extra dimensions) is in your task prompt.

## The course

A 24-session honours course (4th-year Maths/Applied Maths, UCT) on technical AI safety with an
African through-line. Semester starts 2026-07-20; Weeks 1–2 are public, the rest releases weekly,
so improvements to later sessions are cheap to apply before students see them. The tree you are
reading (this directory) is the FULL course (dev branch). READ-ONLY: you report findings; you do
not edit anything.

Standards the course holds itself to: textbook-chapter depth; every reading a working, verified
link; load-bearing claims verified against the actual source; calibrated epistemics (state what a
result does and does not show); an African framing that is honest rather than manufactured; prose
per `STYLE.md` at this directory's root (read it before reporting any writing finding).

## What to review, per page of your assigned sessions (read every page in full)

1. **Factual accuracy.** Anything that looks wrong, overstated, or mis-attributed. Before
   reporting, VERIFY your suspicion against a source (WebFetch the paper/abstract; WebSearch).
   A suspicion you could not verify goes in a separate "unverified suspicions" list, clearly
   labelled. Do not re-check claims that merely sound surprising but match their cited source.
2. **Currency to mid-2026.** Significant developments in this block's topics that the course
   misses or that date its presentation (new canonical results, superseded methods, changed
   institutional facts). Only report with a verified source (fetch it; confirm the title and
   that it says what you claim). The course prefers stable, teachable results over chasing news.
3. **Depth and pedagogy.** Sections below the textbook standard of their siblings; missing worked
   examples where one would carry the idea; class questions that test recall rather than
   judgement; a lab whose instructions have gaps. Compare against the strong pages in your own
   block, and say which page you used as the standard.
4. **Link-first candidates.** The course is moving pages toward "core material: 2–3 superior
   external resources + the page as written reference" where such resources exist (Session 2 is
   the pilot — read 2.1/2.2 in the tree for the pattern). Name pages in your block where a
   clearly superior canonical resource exists, with the verified link.
5. **Writing.** Only NEW findings under STYLE.md's families, respecting its protect-lists and the
   delete-test (do not re-litigate kept "X, not Y" contrasts; do not flag protected vocabulary).
   Density matters more than instances: report a page only if a family visibly exceeds the budgets.
6. **Internal coherence within your block.** Cross-references that point to the wrong place,
   promises ("we return to this in Session N") that nothing fulfils, notation that shifts between
   sub-sessions, duplicated content between pages.

## Known open items — do NOT re-report these

- African-framing recalibration of 1.4/18.2 (isiZulu result is GPT-4-era and much-mitigated;
  planned reframe to the foundational data→alignment question + Anderljung middle-powers reading).
  You MAY report additional instances of dated African-framing claims beyond 1.4/18.2.
- S20 mental-health/emotional-reliance readings (planned, links not yet verified).
- The per-session student-experiment format (open decision).
- ~20 titles still using "&" (open decision).
- The `<p class="lead">` pre-summary lines and "What we'll cover" boxes exist on most pages (a
  known, accepted pattern); report only if a specific instance is actively wrong or redundant.
- Pages self-reporting their limits (info-boxes on caveats) are deliberate, not hedging.

## Output format (return raw data, not prose for a user)

A findings list, each entry:
`{page, type: content-fix | content-add | link-first | writing | coherence | pedagogy,
severity: high | med | low, claim (one sentence), evidence (what you checked and what it said,
with the URL if external), proposed action (one sentence)}`

- severity high = wrong or misleading as taught; med = dated/missing something important;
  low = polish.
- Cap: your ~12 strongest findings, ranked. Then a short "checked and sound" list naming what
  you verified that needs nothing (so silence is distinguishable from not-looked).
- Separate "unverified suspicions" list if any.
