import os
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import re
import random
import time

def load_seo_urls():
    sitemap_path = os.path.join('seo', 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        print("[-] Sitemap de SEO nao encontrado em seo/sitemap.xml. Por favor, gere as paginas primeiro.")
        return []
    
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        # Namespace do sitemap
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = []
        for url in root.findall('sm:url', ns):
            loc = url.find('sm:loc', ns)
            if loc is not None and '/seo/' in loc.text:
                urls.append(loc.text)
        return urls
    except Exception as e:
        print(f"[-] Erro ao ler sitemap: {e}")
        return []

def is_url_indexed(url):
    # Formata a busca: site:URL
    query = f"site:{url}"
    url_encoded = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={url_encoded}&hl=pt-BR"
    
    # Headers para simular um navegador real e evitar bloqueios imediatos
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # Se contiver mensagens de "nao encontrou documentos correspondentes", nao esta indexado
        if "não encontrou nenhum" in html or "did not match any" in html or "Não foram encontrados" in html:
            return False
        
        # Limpa o input do formulário e parâmetros de busca para não dar falso positivo
        cleaned_html = re.sub(r'value="[^"]*"', '', html)
        cleaned_html = re.sub(r'q=site:[^&"]*', '', cleaned_html)
        
        # Se contiver o dominio na resposta limpa, esta indexado
        domain_part = url.replace("https://", "").replace("http://", "")
        if domain_part in cleaned_html:
            return True
            
        return False
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("[-] Google bloqueou a requisicao temporariamente (Too Many Requests / CAPTCHA).")
            return "BLOCKED"
        else:
            print(f"[-] Erro HTTP do Google: {e.code}")
            return "ERROR"
    except Exception as e:
        print(f"[-] Erro na conexao com o Google: {e}")
        return "ERROR"

def main():
    print("=" * 60)
    print("      VERIFICADOR ORGÂNICO DE INDEXAÇÃO DO GOOGLE      ")
    print("=" * 60)
    
    urls = load_seo_urls()
    if not urls:
        print("[-] Nenhuma URL de SEO encontrada para verificar.")
        return
        
    total_urls = len(urls)
    print(f"[+] Total de {total_urls} paginas de SEO detectadas no sitemap.")
    print("[*] Selecionando uma amostra aleatoria de 5 URLs para checagem segura...")
    print("[*] (Para evitar bloqueios de IP / CAPTCHA do Google, verificamos por amostragem)")
    print("-" * 60)
    
    # Amostra aleatoria de 5 URLs
    sample_size = min(5, total_urls)
    sample_urls = random.sample(urls, sample_size)
    
    indexed_count = 0
    blocked_or_error = False
    
    for i, url in enumerate(sample_urls, 1):
        print(f"[{i}/{sample_size}] Checando: {url} ...")
        # Delay amigavel entre chamadas
        if i > 1:
            time.sleep(random.uniform(2, 4))
            
        status = is_url_indexed(url)
        
        if status == "BLOCKED" or status == "ERROR":
            blocked_or_error = True
            break
        elif status is True:
            print("    -> [INDEXADA] Sim, a pagina ja esta ativa no Google!")
            indexed_count += 1
        else:
            print("    -> [PENDENTE] Nao indexada ainda (aguardando rastreamento do robô).")
            
    print("-" * 60)
    if blocked_or_error:
        print("[-] Nao foi possivel completar a checagem orgânica total porque o Google limitou as buscas automáticas do seu IP.")
        print("[*] Dica: Você pode verificar manualmente pesquisando o link com 'site:' direto no navegador.")
    else:
        index_rate = (indexed_count / sample_size) * 100
        print(f"[RESULTADO DA AMOSTRA] Indexacao estimada: {index_rate:.1f}% ({indexed_count} de {sample_size} indexadas).")
        print("[*] Nota: Como o deploy e sitemaps entraram no ar agora, e normal o resultado inicial ser 0%.")
        print("[*] Rode este script nos próximos dias para acompanhar a evolucao orgânica!")
    print("=" * 60)

if __name__ == '__main__':
    main()
