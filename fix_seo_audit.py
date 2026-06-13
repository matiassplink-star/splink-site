# -*- coding: utf-8 -*-
"""
Correcoes da auditoria SEO (itens seguros):
1. og:image relativo -> URL absoluta nas paginas /seo/
2. Deduplicar seo/sitemap.xml (remove <url> com <loc> repetidos)
"""
import glob
import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://splinkapp.com.br"

# ---------- 1) og:image absoluto nas paginas SEO ----------
old_og = 'property="og:image" content="../automacao-whatsapp-splink.png"'
new_og = f'property="og:image" content="{SITE}/automacao-whatsapp-splink.png"'

og_fixed = 0
for path in glob.glob(os.path.join(BASE, "seo", "*.html")):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if old_og in html:
        html = html.replace(old_og, new_og)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        og_fixed += 1
print(f"[1] og:image corrigido em {og_fixed} paginas SEO")

# ---------- 2) Deduplicar seo/sitemap.xml ----------
sm_path = os.path.join(BASE, "seo", "sitemap.xml")
with open(sm_path, "r", encoding="utf-8") as f:
    sm = f.read()

# Captura cada bloco <url>...</url>
url_blocks = re.findall(r"<url>.*?</url>", sm, flags=re.S)
seen = set()
unique_blocks = []
dups = 0
for block in url_blocks:
    loc_match = re.search(r"<loc>(.*?)</loc>", block, flags=re.S)
    loc = loc_match.group(1).strip() if loc_match else block
    if loc in seen:
        dups += 1
        continue
    seen.add(loc)
    unique_blocks.append(block)

header = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
footer = "\n</urlset>\n"
new_sm = header + "\n".join("  " + b for b in unique_blocks) + footer
with open(sm_path, "w", encoding="utf-8") as f:
    f.write(new_sm)
print(f"[2] sitemap deduplicado: {len(unique_blocks)} URLs unicas, {dups} duplicatas removidas")
