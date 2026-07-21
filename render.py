import re, sys, html as H
raw=open(sys.argv[1]).read()
m=re.search(r'<div class="content">(.*)', raw, re.S)
body=m.group(1) if m else raw
# mark boxes
body=re.sub(r'<div class="([a-z-]+)"[^>]*>', lambda m: f"\n[[BOX:{m.group(1)}]]\n", body)
body=re.sub(r'<h2[^>]*>', "\n\n## ", body)
body=re.sub(r'<h3[^>]*>', "\n\n### ", body)
body=re.sub(r'<h4[^>]*>', "\n\n#### ", body)
body=re.sub(r'<p class="lead"[^>]*>', "\n[LEAD] ", body)
body=re.sub(r'<p[^>]*>', "\n", body)
body=re.sub(r'<li[^>]*>', "\n • ", body)
body=re.sub(r'<script.*?</script>', "", body, flags=re.S)
body=re.sub(r'<[^>]+>', "", body)
body=H.unescape(body)
body=re.sub(r'\n{3,}', "\n\n", body)
print(body.strip()[:30000])
