#!/usr/bin/env python3
"""Linkify reading-list references across the course pages.

Two passes, both idempotent and safe to re-run:
  1. arXiv IDs   "arXiv:1234.56789"  -> <a href="https://arxiv.org/abs/1234.56789">arXiv:1234.56789</a>
  2. LINKS dict  literal exact substrings -> wrapped in an anchor to a verified URL.

The LINKS substrings are taken verbatim from the pages (see the per-session reading
sections). A replacement is skipped if the match is already inside a URL/attribute/anchor
(the char immediately before it is one of /  "  =), so re-running never double-wraps.

Run:  python3 linkify_readings.py            (apply)
      python3 linkify_readings.py --check     (report only, no writes)
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).parent / "docs" / "sessions"
CHECK = "--check" in sys.argv

ARXIV = re.compile(r'(?<!/abs/)(?<!">)arXiv:(\d{4}\.\d{4,5}(?:v\d+)?)(?![\dv]|</a>)')
ARXIV_REPL = r'<a href="https://arxiv.org/abs/\1" target="_blank" rel="noopener">arXiv:\1</a>'
# Some pages wrap the ID in <code> (so MathJax skips it): arXiv:<code>1803.04585</code>
ARXIV_CODE = re.compile(r'(?<!">)arXiv:<code>(\d{4}\.\d{4,5}(?:v\d+)?)</code>')
ARXIV_CODE_REPL = r'<a href="https://arxiv.org/abs/\1" target="_blank" rel="noopener">arXiv:<code>\1</code></a>'

A = '<a href="{url}" target="_blank" rel="noopener">'

# Exact substrings present in the pages -> verified destination URL.
# (Confident set; agent-verified entries appended below before the real run.)
LINKS = {
    # --- Session 1 ---
    '<strong>CAIS (2023), "Statement on AI Risk"</strong>': 'https://www.safe.ai/work/statement-on-ai-risk',
    '10.1145/3442188.3445922': 'https://doi.org/10.1145/3442188.3445922',
    '10.5210/fm.v29i4.13636': 'https://doi.org/10.5210/fm.v29i4.13636',
    '<strong>Hoes, E. &amp; Gilardi, F. (2025), "Existential risk narratives about AI do not distract from its immediate harms"</strong>': 'https://doi.org/10.1073/pnas.2419055122',
    # --- Session 2 ---
    'Elhage et al. (2021), "A Mathematical Framework for Transformer Circuits"': 'https://transformer-circuits.pub/2021/framework/index.html',
    'Jay Alammar, "The Illustrated Transformer"': 'https://jalammar.github.io/illustrated-transformer/',
    'github.com/TransformerLensOrg/TransformerLens': 'https://github.com/TransformerLensOrg/TransformerLens',
    'epoch.ai': 'https://epoch.ai/',
    # --- Session 3 ---
    '<strong>Soares, Fallenstein, Yudkowsky &amp; Armstrong (2015), "Corrigibility"</strong>': 'https://intelligence.org/files/Corrigibility.pdf',
    '<strong>Bostrom, N. (2012), "The Superintelligent Will"</strong>': 'https://nickbostrom.com/superintelligentwill.pdf',
    '<strong>Clark &amp; Amodei (2016), "Faulty Reward Functions in the Wild"</strong>': 'https://openai.com/index/faulty-reward-functions/',
    '10.1287/mnsc.1050.0451': 'https://doi.org/10.1287/mnsc.1050.0451',
    # --- Session 5 ---
    '<strong>Sutton, R. (2019), "The Bitter Lesson"</strong>': 'http://www.incompleteideas.net/IncIdeas/BitterLesson.html',
    '<strong>Radford et al. (2019), "Language Models are Unsupervised Multitask Learners"</strong>': 'https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf',
    'github.com/karpathy/nanochat': 'https://github.com/karpathy/nanochat',
    'github.com/karpathy/nanoGPT': 'https://github.com/karpathy/nanoGPT',
    # --- Session 6 ---
    '<strong>Bradley, R. A. &amp; Terry, M. E. (1952), "Rank Analysis of Incomplete Block Designs: I"</strong>': 'https://www.jstor.org/stable/2334029',
    # === AGENT-VERIFIED ENTRIES (Phase B) ===
    # Session 1
    "<strong>Hanna, A. &amp; Bender, E. M. (2023), \"AI Causes Real Harm. Let's Focus on That over the End-of-Humanity Hype\"</strong>": 'https://www.scientificamerican.com/article/we-need-to-focus-on-ais-real-harms-not-imaginary-existential-risks/',
    '<strong>Russell, S. (2019), <em>Human Compatible: Artificial Intelligence and the Problem of Control</em></strong>': 'https://people.eecs.berkeley.edu/~russell/hc.html',
    # Session 2
    '3Blue1Brown, "Neural Networks" video series': 'https://www.3blue1brown.com/topics/neural-networks',
    'Goodfellow, Bengio &amp; Courville, <em>Deep Learning</em>, Ch. 6': 'https://www.deeplearningbook.org/contents/mlp.html',
    '"But what is a GPT?"': 'https://www.3blue1brown.com/lessons/gpt',
    '"Attention in transformers"': 'https://www.3blue1brown.com/lessons/attention',
    # Session 3
    '<strong>Omohundro, S. (2008), "The Basic AI Drives"</strong>': 'https://intelligence.org/files/BasicAIDrives.pdf',
    'Bostrom, N. (2014), <em>Superintelligence</em>, OUP': 'https://global.oup.com/academic/product/superintelligence-9780198739838',
    '<strong>Krakovna et al. (2020), "Specification gaming: the flip side of AI ingenuity"</strong>': 'https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/',
    '<strong>Smith, J. E. &amp; Winkler, R. L. (2006)</strong>': 'https://jimsmith.host.dartmouth.edu/wp-content/uploads/2022/04/The_Optimizers_Curse.pdf',
    '<strong>Galton, F. (1886)</strong>': 'https://galton.org/essays/1880-1889/galton-1886-jaigi-regression-stature.pdf',
    '<strong>Embrechts, P., Klüppelberg, C. &amp; Mikosch, T. (1997)</strong>': 'https://link.springer.com/book/10.1007/978-3-642-33483-2',
    # Session 5
    '<strong>Hugging Face Transformers</strong>': 'https://huggingface.co/docs/transformers/index',
    # Session 6
    '<strong>ARENA</strong>': 'https://www.arena.education/chapter2',
    '<strong>Hugging Face</strong>': 'https://huggingface.co/docs/transformers/index',
    'HH-RLHF preference dataset': 'https://huggingface.co/datasets/Anthropic/hh-rlhf',
    # Session 8
    'Grosse, CSC2547 Lecture 12 "Whose Values?" reading set': 'https://alignment-w2024.notion.site/',
    "Arrow's impossibility theorem": 'https://plato.stanford.edu/entries/arrows-theorem/',
    # Session 12
    '<strong>METR, "Common Elements of Frontier AI Safety Policies"</strong>': 'https://metr.org/common-elements',
    'Anthropic RSP': 'https://www.anthropic.com/responsible-scaling-policy',
    'OpenAI Preparedness': 'https://openai.com/index/updating-our-preparedness-framework/',
    'DeepMind FSF': 'https://deepmind.google/blog/introducing-the-frontier-safety-framework/',
    '<strong>African Union (2024), Continental Artificial Intelligence Strategy</strong>': 'https://au.int/en/documents/20240809/continental-artificial-intelligence-strategy',
    '<strong>Research ICT Africa — "Africa Just AI"</strong>': 'https://researchictafrica.net/research/ria-just-ai-framework-of-inquiry/',
    '<strong>Okolo, C. T. (2023), "AI in the Global South: Opportunities and challenges towards more inclusive governance"</strong>': 'https://www.brookings.edu/articles/ai-in-the-global-south-opportunities-and-challenges-towards-more-inclusive-governance/',
}


def safe_replace(text, key, url):
    """Wrap each free-standing occurrence of `key` in an anchor; skip if already linked."""
    anchor_open = A.format(url=url)
    out, i, n, klen = [], 0, 0, len(key)
    while True:
        j = text.find(key, i)
        if j == -1:
            out.append(text[i:])
            break
        prev = text[j - 1] if j > 0 else ''
        if prev in '/=">':  # inside a URL / attribute / already-wrapped anchor — leave it
            out.append(text[i:j + klen]); i = j + klen; continue
        out.append(text[i:j]); out.append(anchor_open + key + '</a>'); i = j + klen; n += 1
    return ''.join(out), n


def main():
    files = sorted(ROOT.rglob("*.html"))
    arxiv_total = 0
    link_hits = {k: 0 for k in LINKS}
    for f in files:
        txt = f.read_text(encoding="utf-8")
        orig = txt
        txt, nc = ARXIV_CODE.subn(ARXIV_CODE_REPL, txt)
        txt, na = ARXIV.subn(ARXIV_REPL, txt)
        na += nc
        for key, url in LINKS.items():
            txt, nk = safe_replace(txt, key, url)
            link_hits[key] += nk
        if txt != orig:
            changed = na + sum(1 for _ in [0])  # noop to keep flake quiet
            if not CHECK:
                f.write_text(txt, encoding="utf-8")
            print(f"{'(check) ' if CHECK else ''}updated  {f.relative_to(ROOT.parent.parent)}  (+{na} arXiv)")
        arxiv_total += na
    print(f"\narXiv links added: {arxiv_total}")
    missing = [k for k, v in link_hits.items() if v == 0]
    print(f"LINKS applied: {sum(link_hits.values())} across {sum(1 for v in link_hits.values() if v)} keys")
    if missing:
        print("\n!! LINKS keys with NO match (wording mismatch — fix the key):")
        for k in missing:
            print("   -", k[:90])


if __name__ == "__main__":
    main()
