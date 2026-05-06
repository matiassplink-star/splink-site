import glob

replacements = {
    'TECNOLOGIA DE PONTA': 'CORE PERFORMANCE',
    'O Futuro das Vendas é Inteligente.': 'Protocolo de Vendas Inteligente.',
    'O Futuro das Vendas é Inteligente': 'Protocolo de Vendas Inteligente',
    'INVESTIMENTO E ESCALA': 'INFRAESTRUTURA DE ESCALA',
    'SOLUÇÃO COMPLETA': 'PROTOCOLO INTEGRADO',
    'Solicitar Diagnóstico e Contratação': 'INICIAR PROTOCOLO DE ESCALA',
    'Transformando negócios através de automação inteligente': 'Escalando operações através de protocolos de IA',
    'estratégias digitais de alta performance': 'performance massiva de dados',
    'Descubra': 'Acesse',
    'Como Transformamos seu Negócio': 'Estrutura de Escala',
    'Soluções Completas para sua Empresa': 'Ecossistema de Alta Performance',
    'Nossa Metodologia': 'Nosso Protocolo',
    'Passo 1': 'FASE 01',
    'Passo 2': 'FASE 02',
    'Passo 3': 'FASE 03',
    'Passo 4': 'FASE 04',
    'Pronto para escalar?': 'Pronto para o Próximo Nível?',
    'A ferramenta definitiva': 'Infraestrutura Tática',
    'SOFTWARE DESKTOP': 'PROTOCOL DESKTOP',
    'Conexão & Números': 'NÚCLEO DE CONEXÃO',
    'Disparo em Massa': 'DISPARO MASSIVO',
    'Ferramentas': 'MÓDULOS TÁTICOS',
    'IA & Suporte': 'NÚCLEO DE IA',
    'ASSINATURA MENSAL': 'LICENÇA MENSAL',
    'ASSINATURA ANUAL': 'LICENÇA ANUAL',
    'Baixar Versão de Teste': 'ACESSAR PROTOCOLO DE TESTE',
    'Ficou com alguma dúvida': 'Dúvidas técnicas',
    'Falar com Especialista': 'CONTATO TÁTICO',
}

files = glob.glob('*.html')
updated_count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = False
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            modified = True
            
    if modified:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        updated_count += 1
        print(f"Refined copy in: {f}")

print(f"Total files refined: {updated_count}")
