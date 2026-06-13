# -*- coding: utf-8 -*-
"""
Analisa as 1.654 paginas /seo/ e agrupa por (servico, cidade) para
identificar variantes redundantes (canibalizacao) -> plano de 301.
NAO escreve nada. Apenas gera relatorio.
"""
import glob, os, re, json
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))

# Servicos canonicos. Ordem importa: padroes mais especificos primeiro.
# Cada servico = (chave_canonica, [regex de nucleo do slug])
SERVICES = [
    ("curso-trafego-pago",      [r"curso-(presencial-)?(de-)?trafego-pago"]),      # EDUCACIONAL (intencao separada)
    ("trafego-pago",            [r"trafego-pago", r"gestao-de-trafego-pago", r"gestor-de-trafego"]),
    ("criacao-de-sites",        [r"criacao-de-sites?", r"criacao-de-portais?"]),
    ("landing-page",            [r"landing-page(-de-alta-conversao)?"]),
    ("extracao-de-leads",       [r"extracao-de-leads"]),
    ("disparo-whatsapp",        [r"disparo-de-whatsapp(-em-massa)?", r"disparo-whatsapp"]),
    ("crm-whatsapp",            [r"crm-integrado-whatsapp", r"crm-whatsapp", r"crm"]),
    ("chatbot-ia",              [r"chatbot-whatsapp(-com-ia)?", r"chatbot"]),
    ("automacao-whatsapp",      [r"automacao-de-whatsapp", r"automacao"]),
    ("api-disparo-whatsapp",    [r"api-de-disparo-whatsapp", r"api-de-disparo", r"api"]),
    ("agente-sdr",              [r"agente-sdr-inteligente", r"agente-de-ia-sdr", r"agente-sdr", r"agentes?-de-ia"]),
]

# Modificadores (adjetivos/sinonimos) = MESMA intencao -> consolidar.
MOD_PREFIX = [r"^melhor-", r"^a-melhor-", r"^agencia-de-", r"^agencia-", r"^empresa-de-",
              r"^empresa-", r"^gestor-de-", r"^gestao-de-", r"^referencia-em-",
              r"^eventos-sobre-", r"^avaliacoes-sobre-", r"^especialista-em-",
              r"^consultoria-de-", r"^consultoria-em-", r"^servico-de-", r"^servicos-de-"]
MOD_INFIX = [r"-24-horas?", r"-barato", r"-barata", r"-profissional", r"-completa?",
             r"-personalizad[oa]", r"-de-alta-conversao", r"-inteligente",
             r"-em-massa", r"-com-ia", r"-integrado-whatsapp", r"-no-brasil"]

CONNECTORS = [r"^em-", r"^de-", r"^da-", r"^do-", r"^no-", r"^na-", r"^para-", r"^a-"]
STATE_SUFFIX = re.compile(r"-(ac|al|ap|am|ba|ce|df|es|go|ma|mt|ms|mg|pa|pb|pr|pe|pi|rj|rn|rs|ro|rr|sc|sp|se|to)$")

def strip_mods(slug):
    s = slug
    changed = True
    while changed:
        changed = False
        for p in MOD_PREFIX:
            ns = re.sub(p, "", s)
            if ns != s: s, changed = ns, True
        for p in MOD_INFIX:
            ns = re.sub(p, "", s)
            if ns != s: s, changed = ns, True
    return s

def classify(slug):
    core = strip_mods(slug)
    for key, pats in SERVICES:
        for pat in pats:
            m = re.search(pat, core)
            if m:
                # cidade = tudo depois do nucleo do servico
                rest = core[m.end():]
                for c in CONNECTORS:
                    rest = re.sub(c, "", rest)
                # repete remocao de conector
                prev=None
                while prev!=rest:
                    prev=rest
                    for c in CONNECTORS:
                        rest = re.sub(c, "", rest)
                city = rest.strip("-")
                city = STATE_SUFFIX.sub("", city)  # natal-rn -> natal
                city = city.strip("-")
                if not city:
                    city = "brasil"
                return key, city
    return None, None

groups = defaultdict(list)
unmatched = []
for path in sorted(glob.glob(os.path.join(BASE, "seo", "*.html"))):
    slug = os.path.basename(path)[:-5]  # remove .html
    svc, city = classify(slug)
    if svc is None:
        unmatched.append(slug)
    else:
        groups[(svc, city)].append(slug)

# Estatisticas
total_pages = sum(len(v) for v in groups.values()) + len(unmatched)
multi = {k:v for k,v in groups.items() if len(v) > 1}
canonical_count = len(groups)
redirect_count = sum(len(v)-1 for v in groups.values())

print(f"Total paginas classificadas: {total_pages}")
print(f"Nao classificadas (outliers): {len(unmatched)}")
print(f"Grupos (servico+cidade) unicos = paginas CANONICAS: {canonical_count}")
print(f"Variantes redundantes para 301: {redirect_count}")
print()
print("=== Por servico: grupos x variantes ===")
by_svc = defaultdict(lambda: [0,0])
for (svc,city),v in groups.items():
    by_svc[svc][0]+=1
    by_svc[svc][1]+=len(v)
for svc,(g,p) in sorted(by_svc.items(), key=lambda x:-x[1][1]):
    print(f"  {svc:24} canonicas={g:4}  paginas_totais={p:4}  redirects={p-g}")
print()
print("=== 8 grupos com MAIS variantes (exemplos de canibalizacao) ===")
for (svc,city),v in sorted(multi.items(), key=lambda x:-len(x[1]))[:8]:
    print(f"\n[{svc} | {city}] -> {len(v)} URLs:")
    for s in sorted(v):
        print(f"    {s}.html")
print()
print("=== Amostra de outliers nao classificados ===")
for s in unmatched[:25]:
    print(f"    {s}.html")
