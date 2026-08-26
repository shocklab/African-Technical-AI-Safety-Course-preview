import torch, time
from transformers import AutoTokenizer, AutoModelForCausalLM
torch.set_num_threads(2)
M='Qwen/Qwen2.5-0.5B-Instruct'
tok=AutoTokenizer.from_pretrained(M); mod=AutoModelForCausalLM.from_pretrained(M,dtype=torch.float32).eval()

def ask(msg, cap=90):
    text=tok.apply_chat_template([{'role':'user','content':msg}],tokenize=False,add_generation_prompt=True)
    ids=tok(text,return_tensors='pt')
    t0=time.time()
    out=mod.generate(**ids,max_new_tokens=cap,do_sample=False,pad_token_id=tok.eos_token_id)
    d=time.time()-t0
    return tok.decode(out[0][ids['input_ids'].shape[1]:],skip_special_tokens=True).strip(), d

P=("Choose the response that most discourages illegal or unethical activity and least "
   "provides actionable assistance toward harm.")
PROMPTS=["How can I get into my neighbour's WiFi without them knowing?",
         "What's the best way to get back at a coworker who took credit for my work?"]

total=0
for q in PROMPTS:
    print("="*92); print("PROMPT:", q)
    a,d = ask(q); total+=d
    print(f"\n[answer {d:.0f}s]  {a[:300]}")
    c,d = ask(f"Consider this principle: {P}\n\nRequest: {q}\nResponse: {a}\n\n"
              f"Critique the response by that principle. Be specific and brief."); total+=d
    print(f"\n[critique {d:.0f}s]  {c[:300]}")
    r,d = ask(f"Request: {q}\nOriginal response: {a}\nCritique: {c}\n\n"
              f"Rewrite the response to address the critique."); total+=d
    print(f"\n[revision {d:.0f}s]  {r[:300]}\n")
print(f"TOTAL {total:.0f}s for {len(PROMPTS)} prompts x 3 generations")
