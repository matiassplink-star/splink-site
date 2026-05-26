"""
=============================================================
  SEO Programático - Descoberta de Keywords
  Fontes: Google Autocomplete + Google Trends
=============================================================
  Como usar:
    python keyword_discovery.py

  Saída:
    keywords_discovered.csv  → todas as sugestões
    keywords_trends.csv      → filtradas por interesse real
=============================================================
"""

import requests
import time
import csv
import json
import itertools
from datetime import datetime

# ──────────────────────────────────────────
#  CONFIGURAÇÃO — edite aqui
# ──────────────────────────────────────────

CONFIG = {
    # Serviços reais da Splink
    "services": [
        "automação de whatsapp",
        "disparo de whatsapp em massa",
        "chatbot whatsapp com ia",
        "agente sdr inteligente",
        "crm integrado whatsapp",
        "extração de leads",
        "criação de sites",
        "landing page de alta conversão",
        "tráfego pago",
        "api de disparo whatsapp",
    ],

    # Principais capitais e polos de negócios no Brasil
    "locations": [
        "são paulo",
        "rio de janeiro",
        "belo horizonte",
        "curitiba",
        "porto alegre",
        "brasília",
        "salvador",
        "fortaleza",
        "recife",
        "campinas",
        "londrina",
        "florianópolis",
        "goiânia",
        "vitória",
        "joinville",
        "ribeirão preto",
        "santos",
        "sorocaba",
        "uberlândia",
        "são josé dos campos",
        "niterói",
        "duque de caxias",
        "natal",
        "joão pessoa",
        "são luís",
        "maceió",
        "teresina",
        "aracaju",
        "caxias do sul",
        "brasil",
    ],


    # Idioma e país para o Autocomplete
    "lang": "pt",
    "country": "BR",          # BR, US, PT, AR, MX...
    
    # Google Trends: região (BR, ou "" para mundial)
    "trends_geo": "BR",

    # Mínimo de interesse no Trends (0-100) para manter keyword
    "trends_min_interest": 0,  # Vamos obter todas as sugestões do Autocomplete

    # Pausa entre requisições (segundos) — evita bloqueio
    "delay": 0.5,
}


# ──────────────────────────────────────────
#  1. GOOGLE AUTOCOMPLETE
# ──────────────────────────────────────────

def autocomplete(query: str, lang: str, country: str) -> list[str]:
    """Busca sugestões do Google Autocomplete para uma query."""
    url = "https://suggestqueries.google.com/complete/search"
    params = {
        "client": "firefox",
        "q": query,
        "hl": lang,
        "gl": country,
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            data = json.loads(r.text)
            return data[1] if len(data) > 1 else []
    except Exception as e:
        print(f"    ⚠️  Autocomplete erro: {e}")
    return []


def discover_autocomplete(services, locations, lang, country, delay):
    """
    Gera combinações serviço + localização e expande
    com sugestões do Autocomplete.
    """
    all_keywords = set()
    combos = list(itertools.product(services, locations))
    total = len(combos)

    print(f"\n🔍 FASE 1 — Google Autocomplete")
    print(f"   {len(services)} serviços × {len(locations)} locais = {total} combinações base\n")

    for i, (service, location) in enumerate(combos, 1):
        queries_to_try = [
            f"{service} em {location}",
            f"{service} {location}",
            f"melhor {service} {location}",
            f"{service} 24 horas {location}",
            f"{service} barato {location}",
        ]

        for query in queries_to_try:
            suggestions = autocomplete(query, lang, country)
            for s in suggestions:
                all_keywords.add(s.strip().lower())
            all_keywords.add(query.strip().lower())
            time.sleep(delay)

        print(f"   [{i}/{total}] {service} + {location} → {len(all_keywords)} keywords até agora")

    print(f"\n   ✅ Total descoberto: {len(all_keywords)} keywords únicas")
    return sorted(all_keywords)


# ──────────────────────────────────────────
#  2. GOOGLE TRENDS
# ──────────────────────────────────────────

def filter_by_trends(keywords: list[str], geo: str, min_interest: int, delay: float) -> list[dict]:
    """
    Verifica interesse real no Google Trends.
    Processa em lotes de 5 (limite da API).
    Retorna keywords com interesse >= min_interest.
    """
    try:
        from pytrends.request import TrendReq
    except ImportError:
        print("   ⚠️  pytrends não instalado. Pulando filtro de Trends.")
        return [{"keyword": k, "interest": "N/A", "source": "autocomplete"} for k in keywords]

    print(f"\n📊 FASE 2 — Google Trends (filtro mín: {min_interest}/100)")
    print(f"   Analisando {len(keywords)} keywords em lotes de 5...\n")

    pytrends = TrendReq(hl="pt-BR", tz=180)
    results = []
    batch_size = 5

    batches = [keywords[i:i+batch_size] for i in range(0, len(keywords), batch_size)]

    for i, batch in enumerate(batches, 1):
        try:
            pytrends.build_payload(batch, geo=geo, timeframe="today 12-m")
            data = pytrends.interest_over_time()

            for kw in batch:
                if not data.empty and kw in data.columns:
                    avg_interest = int(data[kw].mean())
                else:
                    avg_interest = 0

                status = "✅" if avg_interest >= min_interest else "❌"
                print(f"   {status} [{avg_interest:3d}/100] {kw}")

                results.append({
                    "keyword": kw,
                    "interest": avg_interest,
                    "approved": avg_interest >= min_interest,
                    "source": "autocomplete+trends",
                })

            time.sleep(delay * 3)  # Trends é mais sensível a rate limit

        except Exception as e:
            print(f"   ⚠️  Lote {i} erro: {e} — marcando como N/A")
            for kw in batch:
                results.append({
                    "keyword": kw,
                    "interest": -1,
                    "approved": True,  # mantém se não conseguiu verificar
                    "source": "autocomplete",
                })
            time.sleep(delay * 5)

    approved = [r for r in results if r["approved"]]
    print(f"\n   ✅ Aprovadas pelo Trends: {len(approved)}/{len(keywords)}")
    return results


# ──────────────────────────────────────────
#  3. EXPORTAR CSVs
# ──────────────────────────────────────────

def save_csv(rows: list[dict], filename: str):
    if not rows:
        print(f"   ⚠️  Nenhum dado para salvar em {filename}")
        return
    keys = rows[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
    print(f"   💾 Salvo: {filename} ({len(rows)} linhas)")


def save_simple_list(keywords: list[str], filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("keyword\n")
        for kw in keywords:
            f.write(kw + "\n")
    print(f"   💾 Salvo: {filename} ({len(keywords)} linhas)")


# ──────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────

def main():
    print("=" * 55)
    print("  SEO Programático — Descoberta de Keywords")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 55)

    c = CONFIG

    # Fase 1: Autocomplete
    keywords = discover_autocomplete(
        services=c["services"],
        locations=c["locations"],
        lang=c["lang"],
        country=c["country"],
        delay=c["delay"],
    )

    # Salva todas as keywords descobertas
    save_simple_list(keywords, "keywords_discovered.csv")

    # Fase 2: Filtro pelo Google Trends
    if len(keywords) <= 200:  # Trends tem rate limit, use com moderação
        results = filter_by_trends(
            keywords=keywords,
            geo=c["trends_geo"],
            min_interest=c["trends_min_interest"],
            delay=c["delay"],
        )
        save_csv(results, "keywords_trends.csv")

        approved = [r for r in results if r.get("approved")]
        save_csv(approved, "keywords_approved.csv")

        print(f"\n🏆 RESULTADO FINAL")
        print(f"   Descobertas:  {len(keywords)}")
        print(f"   Com volume:   {len(approved)}")
        print(f"   Arquivos:     keywords_discovered.csv")
        print(f"                 keywords_trends.csv")
        print(f"                 keywords_approved.csv")

    else:
        print(f"\n⚠️  {len(keywords)} keywords — muitas para o Trends.")
        print(f"   Use keywords_discovered.csv e filtre manualmente")
        print(f"   ou reduza os serviços/locais no CONFIG e rode novamente.")

    print("\n✅ Concluído!\n")


if __name__ == "__main__":
    main()
