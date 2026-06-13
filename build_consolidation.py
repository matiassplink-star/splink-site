

# -*- coding: utf-8 -*-
"""
Gera o plano de consolidacao SEO:
  - vercel.json com 301 redirects (variantes -> canonica)
  - seo/sitemap.xml apenas com URLs canonicas
  - consolidation_report.md (revisao humana)
Validacoes: alvo existe, origem != alvo, alvo nunca e origem (sem cadeias).
"""
import glob, os, re, json
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://splinkapp.com.br"

# Servicos canonicos (mais especifico primeiro). api ANTES de disparo.
SERVICES = [
    ("curso-trafego-pago",   [r"curso-(presencial-)?(de-)?trafego-pago"]),
    ("trafego-pago",         [r"trafego-pago", r"gestao-de-trafego-pago", r"gestor-de-trafego"]),
    ("criacao-de-sites",     [r"criacao-de-sites?", r"criacao-de-portais?", r"criacao-de"]),
    ("landing-page",         [r"landing-page(-de-alta-conversao)?"]),
    ("extracao-de-leads",    [r"extracao-de-leads"]),
    ("api-disparo-whatsapp", [r"api-de-disparo-whatsapp", r"api-de-disparo", r"api"]),
    ("disparo-whatsapp",     [r"disparo-de-whatsapp(-em-massa)?", r"disparo-whatsapp"]),
    ("crm-whatsapp",         [r"crm-integrado-whatsapp", r"crm-whatsapp", r"crm"]),
    ("chatbot-ia",           [r"chatbot-whatsapp(-com-ia)?", r"chatbot"]),
    ("automacao-whatsapp",   [r"automacao-de-whatsapp", r"automacao"]),
    ("agente-sdr",           [r"agente-sdr-inteligente", r"agente-de-ia-sdr", r"agente-sdr", r"agentes?-de-ia"]),
]
# Slug "base" canonico de cada servico (para montar a URL canonica preferida)
SERVICE_BASE = {
    "curso-trafego-pago":   "curso-de-trafego-pago",
    "trafego-pago":         "trafego-pago",
    "criacao-de-sites":     "criacao-de-sites",
    "landing-page":         "landing-page-de-alta-conversao",
    "extracao-de-leads":    "extracao-de-leads",
    "api-disparo-whatsapp": "api-de-disparo-whatsapp",
    "disparo-whatsapp":     "disparo-de-whatsapp-em-massa",
    "crm-whatsapp":         "crm-integrado-whatsapp",
    "chatbot-ia":           "chatbot-whatsapp-com-ia",
    "automacao-whatsapp":   "automacao-de-whatsapp",
    "agente-sdr":           "agente-sdr-inteligente",
}
MOD_PREFIX = [r"^melhor-", r"^a-melhor-", r"^agencia-de-", r"^agencia-", r"^empresa-de-",
              r"^empresa-", r"^gestor-de-", r"^gestao-de-", r"^referencia-em-",
              r"^eventos-sobre-", r"^avaliacoes-sobre-", r"^especialista-em-",
              r"^consultoria-de-", r"^consultoria-em-", r"^servico-de-", r"^servicos-de-"]
MOD_INFIX = [r"-24-horas?", r"-barato", r"-barata", r"-profissional", r"-completa?",
             r"-personalizad[oa]", r"-no-brasil"]
MODIFIER_TOKENS = ["melhor", "barato", "barata", "24-horas", "24-hora", "agencia",
                   "empresa", "gestor", "gestao", "referencia", "eventos",
                   "avaliacoes", "especialista", "consultoria", "profissional"]
CONNECTORS = [r"^em-", r"^de-", r"^da-", r"^do-", r"^no-", r"^na-", r"^para-", r"^a-"]
STATE_SUFFIX = re.compile(r"-(ac|al|ap|am|ba|ce|df|es|go|ma|mt|ms|mg|pa|pb|pr|pe|pi|rj|rn|rs|ro|rr|sc|sp|se|to)$")

def strip_mods(slug):
    s, changed = slug, True
    while changed:
        changed = False
        for p in MOD_PREFIX + MOD_INFIX:
            ns = re.sub(p, "", s)
            if ns != s: s, changed = ns, True
    return s

def classify(slug):
    core = strip_mods(slug)
    for key, pats in SERVICES:
        for pat in pats:
            m = re.search(pat, core)
            if m:
                rest = core[m.end():].strip("-")
                prev = None
                while prev != rest:
                    prev = rest
                    rest = rest.lstrip("-")
                    for c in CONNECTORS:
                        rest = re.sub(c, "", rest)
                    rest = rest.strip("-")
                city = STATE_SUFFIX.sub("", rest).strip("-")
                return key, (city or "brasil")
    return None, None

existing = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(BASE, "seo", "*.html"))}
groups = defaultdict(list)
unmatched = []
for slug in sorted(existing):
    svc, city = classify(slug)
    (unmatched if svc is None else groups[(svc, city)]).append(slug if svc is None else slug)
    if svc is not None:
        pass
# rebuild groups properly
groups = defaultdict(list)
unmatched = []
for slug in sorted(existing):
    svc, city = classify(slug)
    if svc is None:
        unmatched.append(slug)
    else:
        groups[(svc, city)].append(slug)

def canonical_score(slug, svc, city):
    """Menor = melhor candidato a canonica."""
    base = SERVICE_BASE[svc]
    score = 0
    for tok in MODIFIER_TOKENS:
        if re.search(rf"(^|-){tok}(-|$)", slug):
            score += 100
    preferred = f"{base}-em-{city}"
    preferred2 = f"{base}-{city}"
    if slug == preferred: score -= 50
    elif slug == preferred2: score -= 40
    elif slug.startswith(base): score -= 10
    score += len(slug) * 0.01  # desempate: mais curto
    return score

redirects = {}   # source_slug -> canonical_slug
canonicals = set()
for (svc, city), slugs in groups.items():
    best = min(slugs, key=lambda s: canonical_score(s, svc, city))
    canonicals.add(best)
    for s in slugs:
        if s != best:
            redirects[s] = best

# Outliers criacao-de-<city> -> canonica de criacao-de-sites daquela cidade
for slug in list(unmatched):
    m = re.match(r"criacao-de-(.+)$", slug)
    if m:
        city = STATE_SUFFIX.sub("", m.group(1)).strip("-")
        # achar canonica de criacao-de-sites para a cidade
        target = None
        for (svc, c), _ in groups.items():
            if svc == "criacao-de-sites" and c == city:
                target = min(groups[(svc, c)], key=lambda s: canonical_score(s, svc, c))
                break
        if target:
            redirects[slug] = target
            unmatched.remove(slug)

# ---- VALIDACOES ----
errors = []
for src, tgt in redirects.items():
    if tgt not in existing: errors.append(f"alvo inexistente: {src} -> {tgt}")
    if src == tgt: errors.append(f"loop: {src}")
    if tgt in redirects: errors.append(f"cadeia: {src} -> {tgt} (que tambem redireciona)")
assert not errors, "ERROS:\n" + "\n".join(errors[:20])

# ---- rel=canonical: cada variante aponta para a canonica do grupo ----
CANON_RE = re.compile(r'(<link\s+rel="canonical"\s+href=")[^"]*(")', re.I)
OGURL_RE = re.compile(r'(<meta\s+property="og:url"\s+content=")[^"]*(")', re.I)
canon_edited = 0
for src, tgt in redirects.items():
    path = os.path.join(BASE, "seo", f"{src}.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    canon_url = f"{SITE}/seo/{tgt}.html"
    new_html, n1 = CANON_RE.subn(rf'\g<1>{canon_url}\g<2>', html)
    new_html, n2 = OGURL_RE.subn(rf'\g<1>{canon_url}\g<2>', new_html)
    if n1 == 0:  # sem tag canonical -> injeta apos <head>
        new_html = new_html.replace("<head>", f'<head>\n    <link rel="canonical" href="{canon_url}">', 1)
    if new_html != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        canon_edited += 1

# Remove vercel.json quebrado (1302 redirects estouraria o limite/deploy)
vjson = os.path.join(BASE, "vercel.json")
if os.path.exists(vjson):
    os.remove(vjson)

# ---- sitemap so com canonicas ----
final_canon = sorted(canonicals)
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for slug in final_canon:
    sm.append(f"  <url>\n    <loc>{SITE}/seo/{slug}.html</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>")
sm.append("</urlset>\n")
with open(os.path.join(BASE, "seo", "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(sm))

print(f"Canonicas (auto-canonical): {len(canonicals)}")
print(f"Variantes com rel=canonical reescrito: {canon_edited} (esperado {len(redirects)})")
print(f"Outliers restantes: {len(unmatched)} -> {unmatched}")
print(f"sitemap.xml regravado com {len(final_canon)} URLs canonicas; vercel.json removido.")
print()
print("=== Exemplo grupo SP / trafego-pago ===")
for (svc, city), slugs in groups.items():
    if svc == "trafego-pago" and city == "sao-paulo":
        best = min(slugs, key=lambda s: canonical_score(s, svc, city))
        print(f"CANONICA: {best}.html")
        for s in sorted(slugs):
            if s != best:
                print(f"  canonical -> {s}.html")
