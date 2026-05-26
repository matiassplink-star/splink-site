import glob
import os

# ==============================================================================
# INJETOR DE PIXELS DE RASTREAMENTO - SPLINK
# Cole o seu script completo (Meta/Facebook Pixel, Google Tag Manager, TikTok, etc.)
# dentro das aspas triplas abaixo (PIXEL_CODE).
# ==============================================================================

PIXEL_CODE = """<!-- Meta Pixel Code -->
<!-- Substitua este comentário pelo script real do seu Pixel do Facebook ou Google Ads -->
<!-- End Meta Pixel Code -->"""

def install():
    if "Substitua este comentário" in PIXEL_CODE or not PIXEL_CODE.strip():
        print("Aviso: Por favor, edite o arquivo 'install_pixels.py' e insira seu script de Pixel real na variável PIXEL_CODE.")
        return

    # Busca recursivamente todos os arquivos HTML na raiz e no subdiretório de SEO
    html_files = glob.glob('*.html') + glob.glob('seo/*.html')
    updated_count = 0

    # Usamos o início do código como assinatura para evitar duplicações
    signature = PIXEL_CODE.strip()[:30]

    for filepath in html_files:
        # Pula arquivos de bibliotecas do node_modules se houver
        if 'node_modules' in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if signature not in content:
            if '<head>' in content:
                # Insere o Pixel logo no início da tag <head> para garantir carregamento prioritário
                content = content.replace('<head>', f'<head>\n{PIXEL_CODE}')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                print(f"Pixel injetado com sucesso em: {filepath}")

    print(f"\n[OK] Varredura concluída. Rastreamento instalado em {updated_count} páginas!")

if __name__ == "__main__":
    install()
