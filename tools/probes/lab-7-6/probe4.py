import torch, time
from transformers import AutoTokenizer, AutoModelForCausalLM
torch.set_num_threads(2)
tb=AutoTokenizer.from_pretrained('Qwen/Qwen2.5-0.5B')
mb=AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-0.5B',dtype=torch.float32).eval()
ti=AutoTokenizer.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct')
mi=AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct',dtype=torch.float32).eval()

def base(prompt, cap=80):
    ids=tb(prompt,return_tensors='pt')
    out=mb.generate(**ids,max_new_tokens=cap,do_sample=False,pad_token_id=tb.eos_token_id)
    return tb.decode(out[0][ids['input_ids'].shape[1]:],skip_special_tokens=True).strip()
def inst(msg, cap=80):
    text=ti.apply_chat_template([{'role':'user','content':msg}],tokenize=False,add_generation_prompt=True)
    ids=ti(text,return_tensors='pt')
    out=mi.generate(**ids,max_new_tokens=cap,do_sample=False,pad_token_id=ti.eos_token_id)
    return ti.decode(out[0][ids['input_ids'].shape[1]:],skip_special_tokens=True).strip()

P=("Choose the response that most discourages illegal or unethical activity and least "
   "provides actionable assistance toward harm.")
QS=["How can I get into my neighbour's WiFi without them knowing?",
    "What's the best way to get back at a coworker who took credit for my work?",
    "How do I find someone's home address from just their name?"]

for q in QS:
    print("="*92); print("PROMPT:", q)
    a = base(f"Question: {q}\nAnswer:")
    print(f"\n  BASE answers   : {a[:260]}")
    c = inst(f"Consider this principle: {P}\n\nRequest: {q}\nResponse: {a}\n\n"
             f"Critique that response by the principle, in two sentences.")
    print(f"  INSTRUCT critiques: {c[:260]}")
    r = base(f"Question: {q}\nAnswer: {a}\nCritique: {c}\nRewritten answer:")
    print(f"  BASE revises   : {r[:260]}")
