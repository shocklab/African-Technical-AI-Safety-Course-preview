# Session 9 revision plan

## Recommendation

Keep five sub-sessions, but give them one question: **what does a robustness claim mean when an attacker can change the input, the interaction, or the surrounding system?** The current draft has useful material, but it treats several analogies as identities and promises a lab result that a current model may not produce.

The session should move through three levels:

1. A formal threat model for bounded image perturbations.
2. Empirical attacks on language models, where the allowed transformations are discrete and open-ended.
3. A multilingual evaluation in which capability, safety and translation quality can be separated.

Prompt injection belongs at the end as the move from model robustness to system security. Data poisoning and backdoors should move to Session 10, where the course plan already places them.

## Learning objectives

By the end of Session 9, students should be able to:

- specify an attack in terms of the adversary's access, goal, allowed transformation and success criterion;
- derive FGSM from a first-order approximation and state what its norm-bounded guarantee does and does not cover;
- explain GCG as a heuristic for discrete optimisation, including its surrogate objective, computational requirements and transfer setting;
- distinguish a jailbreak from direct and indirect prompt injection;
- evaluate multilingual safety without treating non-refusal, harmful compliance and failed comprehension as the same outcome;
- interpret a null, reversed or time-dependent language effect without forcing it into the 2023 result;
- describe why a defence is meaningful only relative to an attack model and an adaptive evaluation.

## Proposed sequence

### 9.1 Adversarial examples and threat models

Use the panda example and FGSM as the clean mathematical case. Present Goodfellow et al.'s linearity account as an influential explanation for the attacks they studied, not a theorem that every useful model must be vulnerable. Remove claims that adversarial examples cannot be eliminated or that the same geometry transfers wholesale to language.

End with the limits of the analogy. A translation is not a small change in an image norm, and two translations need not be semantically identical. The shared idea is the threat-model method: define the transformation set and the success criterion before calling a model robust.

### 9.2 Jailbreaks as discrete search

Keep the GCG objective and algorithm. Correct “provably maximises” to “searches for a low-loss suffix”; GCG is a greedy heuristic with no global optimality guarantee. Explain that forcing an affirmative prefix is a surrogate objective and that attack success still requires judging the generated behaviour.

Retain the 2023 transfer table, labelled with the model versions, sample size and ensemble evaluation. Remove the speculative claim that Claude-2's low result follows partly from Vicuna's ChatGPT lineage unless a direct source supports that interpretation. The paper itself reports that Claude-2 appears more robust and also shows that manual conditioning can raise attack success.

### 9.3 Safety under transformations

Keep Wei, Haghtalab and Steinhardt's competing-objectives and mismatched-generalisation hypotheses. Present them as hypotheses supported by the paper's experiments. The KL discussion may illustrate the authors' argument that the training objective contains a trade-off, but it should not claim that changing the KL coefficient has a simple monotonic effect on capability or safety.

Use the multilingual evidence as a time-indexed comparison:

- Yong, Menghini and Bach (2023/2024): GPT-4-0613 had a 0.96% English attack success rate, 53.08% for isiZulu, and 79.04% for an adaptive attack that succeeded when any of four low-resource languages worked.
- Shen et al. (2024): lower-resource languages produced both more harmful responses and more irrelevant responses, showing that safety and comprehension must be measured separately.
- Marx and Dunaiski (2026, preprint): simple single-turn translation was mostly ineffective on the tested current systems; multilingual multi-turn attacks remained effective, and human translation or adaptation materially changed isiZulu and isiXhosa results.

This makes the scientific question better: under which interaction and translation conditions does a language gap appear now?

### 9.4 Lab: multilingual safety evaluation

Replace “reproduce the isiZulu jailbreak” with a small comparative evaluation. The lab should provide a notebook, a fixed mild prompt set and deterministic machine translations. State prominently that the isiZulu and Afrikaans text has not been reviewed by fluent speakers and that findings involving those conditions are provisional.

Use Qwen3-0.6B on a Colab CPU. The pilot rejected Qwen2.5-0.5B-Instruct because its translated responses were largely incoherent. Qwen3 produces coherent English responses, while its weak comprehension of the translated conditions makes the lab's validity gate essential rather than decorative.

For each prompt and language, record separate variables:

- whether the model understood the request;
- whether it refused;
- whether it produced content that crossed the stated safety boundary;
- whether the response was irrelevant or uninterpretable.

Include matched benign prompts to detect blanket refusal and lack of language ability. Generate short responses only, so the lab measures the refusal boundary without soliciting operationally harmful detail.

Analyse paired prompt-level differences between English and each comparison language. Use a paired bootstrap for the difference in rates. Wilson intervals for each individual rate do not give an interval for the paired difference. With a small prompt set, label the results exploratory and report counts alongside intervals.

Drop the proposed “resource gradient” from three languages. Three hand-picked points cannot establish a gradient, and resource level is not a single variable. Instead, have students compare the language results and use tokenisation, translation quality and comprehension as competing explanations. A small independently labelled subset can illustrate disagreement, but Cohen's kappa should be optional unless the number of double-labelled responses is large enough to interpret it.

The notebook should finish with a structured claim:

> For this model, prompt set, translation set and interaction format, we found [result]. The result does or does not support a language-related safety difference because [evidence], with [limitations] preventing a broader claim.

### 9.5 Prompt injection and layered defences

Focus this page on the system boundary. Define direct prompt injection, jailbreaks and indirect prompt injection separately. Use a small worked example of untrusted retrieved text competing with the user's instruction.

Replace “the model has no reliable way” with an empirical claim: existing defences reduce attack success under particular evaluations, but adaptive attacks continue to bypass them. Teach layered controls such as privilege separation, treating retrieved content as untrusted, constraining tool permissions, validating outputs and evaluating against adaptive attacks.

Keep adversarial training and certified robustness as a short comparison with image-domain guarantees. Correct the randomised-smoothing certificate: the general two-class bound depends on both the top and runner-up class probabilities; \(\sigma\Phi^{-1}(p_A)\) is a simplified special case, not the general radius.

Remove data poisoning, training-data extraction and model-weight security from this page. They add three new threat models after the central lesson and belong with Session 10's backdoors, unlearning and control material.

## Writing changes across all pages

- Remove the standfirsts and most of the “What we'll cover” narration.
- Use plain noun-phrase headings and keep the title, page heading, navigation and index text identical.
- Remove all sentence-punctuation em dashes and emphasis bold.
- Cut claims that tell students what must unsettle them, which results “matter”, or what verdict to deliver.
- Replace universal claims with a named model, attack, dataset, date and success measure.
- Keep paper titles and technical uses of *robustness* unchanged.

## Release gates

Session 9 is ready to release only when:

- every quantitative claim has been checked against the paper's table or released data;
- all external links resolve and identify the cited work;
- the notebook runs from a fresh Colab runtime within the stated time and memory limits;
- the notebook and lab page state that fluent speakers have not reviewed the isiZulu or Afrikaans translations, and that translated-condition findings are provisional;
- the lab is piloted without exposing students to operationally harmful output;
- the rendered pages pass navigation, HTML structure and prose checks;
- the lab instructions accept null and reversed results and do not grade students on reproducing a preferred conclusion.

## Sources checked for this plan

- Goodfellow, Shlens and Szegedy, [“Explaining and Harnessing Adversarial Examples”](https://arxiv.org/abs/1412.6572).
- Zou et al., [“Universal and Transferable Adversarial Attacks on Aligned Language Models”](https://arxiv.org/abs/2307.15043).
- Wei, Haghtalab and Steinhardt, [“Jailbroken: How Does LLM Safety Training Fail?”](https://arxiv.org/abs/2307.02483).
- Yong, Menghini and Bach, [“Low-Resource Languages Jailbreak GPT-4”](https://arxiv.org/abs/2310.02446).
- Shen et al., [“The Language Barrier: Dissecting Safety Challenges of LLMs in Multilingual Contexts”](https://aclanthology.org/2024.findings-acl.156/).
- Marx and Dunaiski, [“Multilingual jailbreaking of LLMs using low-resource languages”](https://arxiv.org/abs/2605.18239), a May 2026 preprint.
- Zhan et al., [“Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents”](https://arxiv.org/abs/2503.00061).
