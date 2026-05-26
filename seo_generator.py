# -*- coding: utf-8 -*-
"""
=============================================================
  SEO Programático — Gerador Estático de Landing Pages
  Desenvolvido para Splink (Cyber-Premium Theme com Sentence Spinning)
=============================================================
  Como usar:
    python -X utf8 seo_generator.py --csv keywords_discovered.csv --output ./seo

  Este script lê a planilha de keywords e cria landing pages
  estáticas ultra-rápidas no estilo hacker/matrix da Splink.
  Cada página tem conteúdo 100% único através de um motor
  de Sentence Spinning determinístico.
=============================================================
"""

import os
import csv
import argparse
import re
from xml.sax.saxutils import escape as xml_escape

# ──────────────────────────────────────────
#  CONFIGURAÇÕES DE MARCA DA SPLINK
# ──────────────────────────────────────────
SITE_CONFIG = {
    "site_name": "SPLINK",
    "base_url": "https://splinkapp.com.br",
    "whatsapp_link": "https://wa.me/5534999929764?text=Ol%C3%A1%21+Vim+do+Google+e+gostaria+de+saber+mais+sobre+automa%C3%A7%C3%A3o.",
    "contact_email": "contato@splinkapp.com.br",
}

# Mapeamento amigável para nomes dos serviços no H1/Título
SERVICE_DISPLAY_NAMES = {
    "automação de whatsapp": "Automação de WhatsApp",
    "disparo de whatsapp em massa": "Disparo de WhatsApp em Massa",
    "chatbot whatsapp com ia": "Chatbot WhatsApp com Inteligência Artificial",
    "agente sdr inteligente": "Agente SDR de IA para WhatsApp",
    "crm integrado whatsapp": "CRM Integrado ao WhatsApp",
    "extração de leads": "Extração de Leads e Contatos",
    "criação de sites": "Criação de Sites Profissionais",
    "landing page de alta conversão": "Landing Pages de Alta Conversão",
    "tráfego pago": "Tráfego Pago e Gestão de Anúncios",
    "api de disparo whatsapp": "API de Disparo e Integração WhatsApp",
}

# FAQs contextualizadas para tornar o conteúdo único para o Google
FAQ_DATA = {
    "automação de whatsapp": [
        {
            "q": "Como funciona a Automação de WhatsApp da Splink em {location}?",
            "a": "Nossa plataforma automatiza seus fluxos de mensagens de forma 100% segura. O sistema se conecta ao seu WhatsApp, permitindo enviar mensagens automáticas de boas-vindas, lembretes de cobrança, confirmação de horários e alertas de envio em {location}."
        },
        {
            "q": "Posso sofrer bloqueios usando a automação em {location}?",
            "a": "Nossa automação utiliza protocolos exclusivos de bypass anti-ban com atraso inteligente entre disparos (delay randômico) e aquecimento de chips, minimizando drasticamente os riscos de suspensão."
        }
    ],
    "disparo de whatsapp em massa": [
        {
            "q": "Qual é a velocidade dos disparos em massa em {location}?",
            "a": "Com nossa tecnologia multicore sync, você consegue disparar milhares de mensagens por hora com alta estabilidade, sendo ideal para campanhas de marketing locais de grande escala em {location}."
        },
        {
            "q": "Preciso deixar o celular conectado para realizar os disparos?",
            "a": "Não! Nossa infraestrutura de servidores em nuvem gerencia as conexões de forma independente. Uma vez configurada a campanha, os disparos continuam rodando 24 horas por dia automaticamente."
        }
    ],
    "chatbot whatsapp com ia": [
        {
            "q": "O chatbot de IA atende como um humano em {location}?",
            "a": "Sim, nossos chatbots são integrados a modelos avançados de IA Generativa. Eles respondem às dúvidas dos seus clientes de {location} com linguagem natural, simpatia e precisão técnica de acordo com seu script."
        },
        {
            "q": "É fácil integrar a IA com o meu negócio?",
            "a": "Com certeza! Nós configuramos toda a base de conhecimento do seu negócio para treinar a inteligência artificial. O chatbot já sai configurado e pronto para converter leads locais."
        }
    ],
    "agente sdr inteligente": [
        {
            "q": "O que faz um Agente SDR de IA em {location}?",
            "a": "Ele qualifica todos os leads frios que chegam no seu WhatsApp em {location}, tirando dúvidas preliminares, fazendo perguntas de filtro e agendando reuniões diretamente na agenda do seu time de vendas."
        },
        {
            "q": "A IA pode fechar vendas sozinha?",
            "a": "Sim! Em negócios transacionais ou de produtos digitais, o robô pode enviar o link de checkout do Mercado Pago ou Pix e consolidar a venda 100% no automático, sem qualquer intervenção humana."
        }
    ],
    "crm integrado whatsapp": [
        {
            "q": "Como o CRM da Splink organiza os leads de {location}?",
            "a": "Ele cria um funil Kanban visual no seu navegador, movendo os leads de {location} automaticamente conforme eles interagem com seus robôs, gerando uma visão clara de ROI e conversão em tempo real."
        },
        {
            "q": "Posso integrar com CRMs externos?",
            "a": "Sim, possuímos integrações nativas via webhooks e ferramentas de workflow (como Make e n8n) para enviar dados de novos clientes de {location} para plataformas como Hubspot, ActiveCampaign e RD Station."
        }
    ],
    "extração de leads": [
        {
            "q": "De quais fontes posso extrair contatos em {location}?",
            "a": "Nossos robôs são especializados em minerar dados públicos de alta conversão do Google Maps, OLX e portais especializados em {location}, reunindo telefone, nome da empresa, e-mail e segmento."
        },
        {
            "q": "Os contatos extraídos são legais e válidos?",
            "a": "Sim, os extratores coletam apenas informações públicas disponíveis na internet. Todos os dados são filtrados e sanitizados em tempo real, fornecendo listas higienizadas prontas para prospecção ativa."
        }
    ],
    "criação de sites": [
        {
            "q": "Quanto tempo demora para meu site estar ativo em {location}?",
            "a": "Desenvolvemos seu site corporativo ou institucional com foco em conversão e velocidade de carregamento em até 10 dias úteis, garantindo presença imediata e autoridade no Google para o mercado de {location}."
        },
        {
            "q": "O site já vem otimizado para celulares?",
            "a": "100%! Criamos layouts totalmente responsivos e mobile-first com nota 100 de performance no Google PageSpeed, o que garante que seus clientes em {location} tenham a melhor experiência de carregamento."
        }
    ],
    "landing page de alta conversão": [
        {
            "q": "Qual é a diferença entre um site comum e uma Landing Page em {location}?",
            "a": "Uma landing page é focada em uma única ação: converter o visitante em lead ou comprador. Removemos distrações desnecessárias para garantir taxas de conversão até 3 vezes maiores em {location}."
        },
        {
            "q": "Vocês criam a copy de vendas da página?",
            "a": "Sim! Escrevemos copy persuasiva baseada em gatilhos mentais fortes específicos para atrair o público de {location}, estruturando títulos marcantes, FAQs locais e botões que incentivam a ação imediata."
        }
    ],
    "tráfego pago": [
        {
            "q": "Como funciona a gestão de anúncios da Splink em {location}?",
            "a": "Gerenciamos estrategicamente seus investimentos de mídia patrocinada no Google Ads e Meta Ads (Instagram/Facebook) segmentados cirurgicamente para as regiões de {location} que concentram seu público-alvo."
        },
        {
            "q": "Qual é o orçamento mínimo para começar a anunciar?",
            "a": "Recomendamos iniciar com pelo menos R$ 20 a R$ 30 por dia para que as ferramentas de inteligência dos anúncios consigam otimizar seu funil de captação de clientes in {location}."
        }
    ],
    "api de disparo whatsapp": [
        {
            "q": "Posso conectar meu ERP ou sistema de vendas de {location} ao WhatsApp?",
            "a": "Com certeza! Nossa API robusta permite integrar qualquer software, e-commerce ou sistema de cobrança local em {location} para disparar mensagens transacionais instantâneas por protocolo HTTP."
        },
        {
            "q": "A API suporta envio de mídias e arquivos?",
            "a": "Sim! A API da Splink permite enviar textos, imagens, áudios gravados na hora (que aparecem como gravados pelo usuário), PDFs, botões interativos e listas estruturadas sem limites."
        }
    ],
}

DEFAULT_FAQ = [
    {
        "q": "Como a Splink ajuda a escalar minhas vendas em {location}?",
        "a": "Implementamos protocolos inteligentes de automação no WhatsApp, disparo de campanhas, extração cirúrgica de contatos e design de páginas de alta conversão para estruturar uma máquina previsível de captação de clientes em {location}."
    },
    {
        "q": "Como posso iniciar meu protocolo de automação?",
        "a": "Basta clicar em qualquer botão desta página para iniciar nossa conversa direta pelo WhatsApp. Nossa equipe analisará seu funil comercial e ativará a automação sob medida."
    }
]

# ──────────────────────────────────────────
#  MOTOR DE SENTENCE SPINNING (CONTEÚDO 100% ÚNICO)
# ──────────────────────────────────────────
def get_spun_content(service, location, idx):
    """
    Retorna variações de títulos, descrições e parágrafos de forma
    determinística baseando-se no índice do loop da página, garantindo que
    cada uma das 1.350+ páginas seja única.
    """
    
    # 4 Variações de H1
    h1_templates = [
        "Protocolo de {service} em <span>{location}</span>",
        "Sistemas de {service} para Empresas em <span>{location}</span>",
        "Ativação de {service} em <span>{location}</span>",
        "Plataforma de {service} de Alta Performance em <span>{location}</span>"
    ]
    
    # 4 Variações de Subtítulo do Hero
    subtitle_templates = [
        "Otimize o atendimento do seu negócio em {location} com nosso protocolo avançado de {service}. Esqueça processos manuais e perdas de leads: a arquitetura de escala da Splink trabalha no piloto automático estruturando seu funil de vendas local.",
        "Procurando alavancar suas conversões de vendas com {service} em {location}? A Splink conecta robôs inteligentes de Inteligência Artificial e automações estáveis diretamente ao seu WhatsApp para qualificar e fechar negócios 24 horas por dia.",
        "Precisa de {service} com alta segurança e sem fricção na região de {location}? Nós da Splink implantamos soluções personalizadas de disparos massivos, SDRs inteligentes e CRM que eliminam gargalos operacionais e multiplicam seu ROI.",
        "Impulsione a captação de novos clientes locais implantando o sistema de {service} em {location}. Nossa tecnologia conecta bots integrados de IA Generativa de forma simples e estável para atender, engajar e receber Pix no automático."
    ]
    
    # 3 Conjuntos de Cards de Diferenciais (Garante estrutura única de benefícios)
    cards_templates = [
        [
            {"title": "⚡ Bypass Anti-Ban", "desc": "Utilizamos atrasos randômicos refinados, mensagens dinâmicas por tag e aquecimento integrado de chips para garantir a segurança da sua conta em {location}."},
            {"title": "🤖 Agentes de IA SDR", "desc": "Robôs treinados que compreendem contexto local de {location}, tiram dúvidas com linguagem natural humana e agendam reuniões no calendário comercial."},
            {"title": "📊 Dashboard em Tempo Real", "desc": "Acompanhe todo o fluxo de mensagens de {location} com painéis Kanban interativos integrados para visualização clara de lucros."}
        ],
        [
            {"title": "🔒 Segurança Militar", "desc": "Protocolos de disparo que respeitam as regras operacionais da Meta, protegendo seu chip em {location} contra bloqueios indesejados."},
            {"title": "💡 IA Generativa Avançada", "desc": "Modelos de linguagem que realizam triagem inteligente de leads em {location}, tirando dúvidas sobre produtos no automático."},
            {"title": "🔗 Integração Webhook e API", "desc": "Sincronize imediatamente seus leads minerados em {location} com sistemas externos como Hubspot, Make, n8n ou RD Station."}
        ],
        [
            {"title": "🚀 Escala e Performance", "desc": "Envie mensagens em massa para listas segmentadas em {location} com tecnologia multicore que processa disparos de forma rápida."},
            {"title": "🎯 Atendimento Híbrido", "desc": "Deixe a inteligência artificial realizar o primeiro contato em {location} e transfira para um atendente humano apenas os leads quentes."},
            {"title": "📈 Otimização de ROI", "desc": "Reduza custos operacionais de suporte em {location} em até 70% e aumente suas taxas de fechamento com fluxos de engajamento."}
        ]
    ]

    h1 = h1_templates[idx % len(h1_templates)].format(service=service, location=location)
    subtitle = subtitle_templates[idx % len(subtitle_templates)].format(service=service, location=location)
    cards = cards_templates[idx % len(cards_templates)]
    
    # Formata os cards
    formatted_cards = []
    for card in cards:
        formatted_cards.append({
            "title": card["title"].format(location=location),
            "desc": card["desc"].format(location=location)
        })
        
    return h1, subtitle, formatted_cards

# ──────────────────────────────────────────
#  AJUDANTES
# ──────────────────────────────────────────
def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[áàâãä]', 'a', text)
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[íìîï]', 'i', text)
    text = re.sub(r'[óòôõö]', 'o', text)
    text = re.sub(r'[úùûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

# ──────────────────────────────────────────
#  GERAÇÃO DO CÓDIGO HTML COM IDENTIDADE SPLINK CYBER-PREMIUM E SPINNING
# ──────────────────────────────────────────
def get_html_template(keyword, service_raw, location_raw, slug, neighbors_links, idx):
    service = SERVICE_DISPLAY_NAMES.get(service_raw, service_raw.title())
    location = location_raw.title()
    
    h1, subtitle, cards = get_spun_content(service, location, idx)
    
    title = f"{service} em {location} | Protocolo de Performance Splink"
    description = f"Otimize seu atendimento com {service} em {location}. Automação inteligente no WhatsApp, robôs SDR, CRM integrado e escala de vendas da Splink."
    canonical_url = f"{SITE_CONFIG['base_url']}/seo/{slug}.html"
    
    # Montar FAQs locais
    faq_list = FAQ_DATA.get(service_raw, DEFAULT_FAQ)
    faq_html = ""
    faq_schema_items = []
    
    for item in faq_list:
        q_formatted = item["q"].format(location=location)
        a_formatted = item["a"].format(location=location)
        
        faq_html += f"""
        <div class="faq-item" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; margin-bottom: 12px; overflow: hidden; transition: all 0.3s ease;">
            <button class="faq-question" style="width: 100%; background: none; border: none; color: white; padding: 20px; text-align: left; font-size: 16px; font-weight: 600; cursor: pointer; display: flex; justify-content: space-between; align-items: center;">
                {q_formatted}
                <i data-lucide="chevron-down" style="color: var(--accent); width: 18px; transition: transform 0.3s ease;"></i>
            </button>
            <div class="faq-answer" style="padding: 0 20px 20px 20px; display: none; color: rgba(255,255,255,0.6); font-size: 14px; line-height: 1.6;">
                <p>{a_formatted}</p>
            </div>
        </div>
        """
        faq_schema_items.append(f"""
        {{
          "@type": "Question",
          "name": "{q_formatted}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{a_formatted}"
          }}
        }}
        """)
        
    faq_schema = ",\n".join(faq_schema_items)

    # Interlinking dinâmico
    links_html = ""
    for name, path in neighbors_links:
        links_html += f'<a href="./{path}" class="btn btn-secondary" style="font-size: 12px; padding: 10px 20px; border-radius: 20px; margin: 6px; letter-spacing: 1px;">{name}</a>\n'

    # Monta os cards HTML
    cards_html = ""
    icons = ["shield-check", "cpu", "bar-chart-3"]
    for i, card in enumerate(cards):
        cards_html += f"""
        <div class="service-card glass" style="width: calc(33.333% - 22px); min-width: 300px; border-radius: 24px;">
            <i data-lucide="{icons[i % len(icons)]}" class="service-icon"></i>
            <h3>{card['title']}</h3>
            <p>{card['desc']}</p>
        </div>
        """

    # Template HTML
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9TRYN4VYKG"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-9TRYN4VYKG');
    </script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <link rel="icon" type="image/png" href="../favicon.png">
    
    <!-- Mobile Browser Theme Color -->
    <meta name="theme-color" content="#000000">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="../automacao-whatsapp-splink.png">

    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <!-- Importação de Estilo Nativo da Splink -->
    <link rel="stylesheet" href="../index.min.css">
    
    <style>
        .hero {{
            position: relative;
            padding: 140px 0 80px;
            text-align: left;
            overflow: hidden;
            background: transparent;
        }}
        .hacker-block:hover {{
            background: rgba(0, 212, 255, 0.08) !important;
            transform: translateY(-5px);
            border-left-color: #fff !important;
        }}
        .hacker-block {{
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            overflow: hidden;
            position: relative;
        }}
        .hacker-block::after {{
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 2px;
            background: rgba(0, 212, 255, 0.2);
            animation: scanline 2s linear infinite;
            pointer-events: none;
        }}
        @keyframes scanline {{
            0% {{ transform: translateY(-100%); }}
            100% {{ transform: translateY(100%); }}
        }}
        .faq-item.active .faq-answer {{
            display: block !important;
        }}
        .faq-item.active i {{
            transform: rotate(180deg);
        }}
        .tag {{
            display: inline-block;
            padding: 4px 12px;
            background: rgba(0, 122, 255, 0.2);
            color: var(--accent);
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 16px;
        }}
        .services-grid {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 32px;
            margin-top: 40px;
        }}
        .service-card {{
            padding: 40px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 100%;
        }}
        .service-icon {{
            width: 48px;
            height: 48px;
            color: var(--accent);
            margin-bottom: 24px;
        }}
        section {{
            padding: 80px 0;
        }}
    </style>
</head>
<body>
    <!-- Fundo Estrelas/Matrix Fixo -->
    <canvas id="matrixCanvas" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.4; pointer-events: none;"></canvas>
    
    <nav class="navbar-landing">
        <a href="../index.html" class="splink-logo logo-large">
            <div class="logo-symbol">
                <i data-lucide="zap"></i>
            </div>
            <div class="logo-text">SPLINK<span>.</span></div>
        </a>
    </nav>

    <!-- Hero Section Segmentado -->
    <section class="hero">
        <div class="container">
            <!-- 3 Status Blocks de Performance -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 50px;">
                <div class="service-card hacker-block" style="padding: 20px; border-left: 3px solid var(--accent); background: rgba(255,255,255,0.02); border-radius: 12px;">
                    <div style="font-size: 11px; opacity: 0.5; margin-bottom: 8px; color: var(--accent); letter-spacing: 2px;">[ STATUS OPERACIONAL ]</div>
                    <div style="font-size: 18px; font-weight: 700; color: white;">ESTRUTURA LOCAL ATIVA</div>
                    <div style="font-size: 12px; color: rgba(255,255,255,0.5); font-family: monospace;">NICHOS: <span style="color: var(--accent);">PRODUÇÃO</span></div>
                </div>
                <div class="service-card hacker-block" style="padding: 20px; border-left: 3px solid var(--accent); background: rgba(255,255,255,0.02); border-radius: 12px;">
                    <div style="font-size: 11px; opacity: 0.5; margin-bottom: 8px; color: var(--accent); letter-spacing: 2px;">[ GEOLOCALIZAÇÃO ]</div>
                    <div style="font-size: 18px; font-weight: 700; color: white;">SERVIDORES {location.upper()}</div>
                    <div style="font-size: 12px; color: rgba(255,255,255,0.5); font-family: monospace;">PING: <span style="color: var(--accent);">12ms (EXCELENTE)</span></div>
                </div>
                <div class="service-card hacker-block" style="padding: 20px; border-left: 3px solid var(--accent); background: rgba(255,255,255,0.02); border-radius: 12px;">
                    <div style="font-size: 11px; opacity: 0.5; margin-bottom: 8px; color: var(--accent); letter-spacing: 2px;">[ SEGURANÇA ]</div>
                    <div style="font-size: 18px; font-weight: 700; color: white;">ROTA CRIPTOGRAFADA</div>
                    <div style="font-size: 12px; color: rgba(255,255,255,0.5); font-family: monospace;">SSL: <span style="color: var(--accent);">SECURE WORK</span></div>
                </div>
            </div>

            <div style="max-width: 900px;">
                <div class="tag">ALTA PERFORMANCE COM IA</div>
                <h1 style="font-family: 'Inter', sans-serif; letter-spacing: -1px; color: white; line-height: 1.1; margin-bottom: 24px;">
                    {h1}
                </h1>
                <p style="max-width: 650px; margin-bottom: 40px; color: rgba(255, 255, 255, 0.6); font-size: 18px; line-height: 1.6;">
                    {subtitle}
                </p>
                <div style="display: flex; gap: 16px; flex-wrap: wrap;">
                    <a href="{SITE_CONFIG['whatsapp_link']}" class="btn btn-primary" style="padding: 18px 40px; font-size: 16px;">ATIVAR NO WHATSAPP</a>
                    <a href="#detalhes" class="btn btn-secondary" style="padding: 18px 40px; font-size: 16px;">Ver Módulos</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Detalhes do Serviço -->
    <section id="detalhes" class="container">
        <div style="text-align: center; margin-bottom: 40px;">
            <div class="tag">DIFERENCIAIS SPLINK</div>
            <h2>Arquitetura Comercial de Ponta</h2>
            <p style="color: rgba(255,255,255,0.6); max-width: 600px; margin: 0 auto;">Nossas ferramentas são programadas com foco exclusivo em escala, estabilidade de chip e alta conversão local.</p>
        </div>
        
        <div class="services-grid">
            {cards_html}
        </div>
    </section>

    <!-- FAQ Accordion -->
    <section class="container" style="max-width: 800px;">
        <div style="text-align: center; margin-bottom: 50px;">
            <div class="tag">CENTRAL DE SUPORTE</div>
            <h2>Dúvidas Frequentes</h2>
            <p style="color: rgba(255,255,255,0.6);">Respostas diretas sobre a implantação comercial do sistema.</p>
        </div>
        
        <div class="faq-container">
            {faq_html}
        </div>
    </section>

    <!-- Interlinking Hub -->
    <section class="container" style="text-align: center;">
        <div style="text-align: center; margin-bottom: 40px;">
            <div class="tag">REDE DE ATENDIMENTO</div>
            <h2>Outras Cidades e Serviços Atendidos</h2>
            <p style="color: rgba(255,255,255,0.6); max-width: 600px; margin: 0 auto 30px;">Disponibilizamos nossos sistemas de alta performance em múltiplos polos comerciais do Brasil.</p>
        </div>
        <div class="glass" style="padding: 30px; border-radius: 24px; display: flex; flex-wrap: wrap; justify-content: center;">
            {links_html}
        </div>
    </section>

    <!-- CTA Final -->
    <section class="container" style="text-align: center; padding-top: 40px;">
        <h2>Pronto para Automatizar sua Operação?</h2>
        <p style="margin-bottom: 30px; color: rgba(255,255,255,0.6);">Fale agora com nosso consultor especialista de {location} e garanta seu cupom de ativação imediata.</p>
        <a href="{SITE_CONFIG['whatsapp_link']}" class="btn btn-primary" style="font-size: 18px; padding: 16px 36px;">Falar com Consultor</a>
    </section>

    <footer class="main-footer">
        <div class="container">
            <div style="display: flex; flex-direction: column; align-items: center; text-align: center; max-width: 600px; margin: 0 auto;">
                <a href="../index.html" class="splink-logo logo-large" style="margin-bottom: 24px;">
                    <div class="logo-symbol">
                        <i data-lucide="zap"></i>
                    </div>
                    <div class="logo-text">SPLINK<span>.</span></div>
                </a>
                <p style="font-size: 14px; line-height: 1.6; margin-bottom: 32px;">Escalando operações através de protocolos de IA e performance massiva de dados desde 2019.</p>
            </div>
            <div class="footer-bottom">
                <div>&copy; 2019-2026 Splink Soluções Digitais. Todos os direitos reservados.</div>
                <div class="footer-legal-links">
                    <a href="../status.html">Status</a>
                    <a href="../privacidade.html">Privacidade</a>
                    <a href="../termos.html">Termos</a>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Inicialização do Lucide Icons
        lucide.createIcons();

        // FAQ Accordion Toggle
        document.querySelectorAll('.faq-question').forEach(button => {{
            button.addEventListener('click', () => {{
                const item = button.parentElement;
                item.classList.toggle('active');
            }});
        }});
        
        // Matrix Falling Rain Effect
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const katakana = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        const alphabet = katakana.split("");

        const fontSize = 16;
        const columns = canvas.width/fontSize;

        const rainDrops = [];

        for( let x = 0; x < columns; x++ ) {{
            rainDrops[x] = 1;
        }}

        const draw = () => {{
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#0f0'; // green text
            ctx.fillStyle = 'rgba(0, 212, 255, 0.35)'; // Cyan matching Splink's theme!
            ctx.font = fontSize + 'px monospace';

            for(let i = 0; i < rainDrops.length; i++) {{
                const text = alphabet[Math.floor(Math.random() * alphabet.length)];
                ctx.fillText(text, i*fontSize, rainDrops[i]*fontSize);

                if(rainDrops[i]*fontSize > canvas.height && Math.random() > 0.975){{
                    rainDrops[i] = 0;
                }}
                rainDrops[i]++;
            }}
        }};

        setInterval(draw, 30);

        window.addEventListener('resize', () => {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }});
    </script>

    <!-- Schema.org Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Service",
      "name": "{service} em {location}",
      "description": "{description}",
      "provider": {{
        "@type": "LocalBusiness",
        "name": "{SITE_CONFIG['site_name']}",
        "url": "{SITE_CONFIG['base_url']}",
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "{location}",
          "addressCountry": "BR"
        }}
      }},
      "areaServed": {{
        "@type": "AdministrativeArea",
        "name": "{location}"
      }}
    }}
    </script>

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {faq_schema}
      ]
    }}
    </script>
</body>
</html>
"""
    return html_content

# ──────────────────────────────────────────
#  GERE TODAS AS PÁGINAS E SITEMAP
# ──────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Gerador de SEO Programático para a Splink")
    parser.add_argument("--csv", default="keywords_discovered.csv", help="Caminho do arquivo CSV de entrada")
    parser.add_argument("--output", default="./seo", help="Diretório de saída para os HTMLs")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    pages_to_generate = []
    if not os.path.exists(args.csv):
        print(f"❌ Arquivo CSV não encontrado: {args.csv}")
        return

    # Lista completa de 30 localizações para correspondência
    locations = [
        "são paulo", "rio de janeiro", "belo horizonte", "curitiba", "porto alegre",
        "brasília", "salvador", "fortaleza", "recife", "campinas", "londrina",
        "florianópolis", "goiânia", "vitória", "joinville", "ribeirão preto",
        "santos", "sorocaba", "uberlândia", "são josé dos campos", "niterói",
        "duque de caxias", "natal", "joão pessoa", "são luís", "maceió",
        "teresina", "aracaju", "caxias do sul", "brasil"
    ]

    # 1. Carrega dados do CSV
    with open(args.csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kw = row.get("keyword")
            if not kw:
                continue
            
            # Identifica qual serviço e qual localidade estão na keyword de forma inteligente
            service_found = None
            location_found = None
            
            for service in SERVICE_DISPLAY_NAMES.keys():
                if service in kw:
                    service_found = service
                    break
            
            for loc in locations:
                if loc in kw:
                    location_found = loc
                    break
            
            # Fallback se não detectar
            if not service_found or not location_found:
                parts = kw.split(" em ")
                if len(parts) == 2:
                    service_found = parts[0]
                    location_found = parts[1]
                else:
                    parts = kw.split(" ")
                    service_found = parts[0]
                    location_found = " ".join(parts[1:]) if len(parts) > 1 else "brasil"

            slug = slugify(kw)
            pages_to_generate.append({
                "keyword": kw,
                "service": service_found,
                "location": location_found,
                "slug": slug,
                "filename": f"{slug}.html"
            })

    total = len(pages_to_generate)
    if total == 0:
        print("⚠️ Nenhuma keyword válida encontrada para geração de páginas.")
        return
        
    print(f"\n📂 Iniciando geração de {total} páginas com interlinking dinâmico e Sentence Spinning...")

    # 2. Geração em loop com interlinking circular (6 vizinhos) e spinning de sentenças
    generated_urls = []
    
    for idx, page in enumerate(pages_to_generate):
        neighbors = []
        for i in range(1, 7):
            neigh_idx = (idx + i) % total
            neigh = pages_to_generate[neigh_idx]
            neigh_service = SERVICE_DISPLAY_NAMES.get(neigh['service'], neigh['service'].title())
            neighbors.append((f"{neigh_service} em {neigh['location'].title()}", neigh['filename']))

        html_code = get_html_template(
            keyword=page["keyword"],
            service_raw=page["service"],
            location_raw=page["location"],
            slug=page["slug"],
            neighbors_links=neighbors,
            idx=idx
        )

        out_path = os.path.join(args.output, page["filename"])
        with open(out_path, "w", encoding="utf-8") as f_out:
            f_out.write(html_code)

        generated_urls.append(f"{SITE_CONFIG['base_url']}/seo/{page['filename']}")

    print(f"✅ {total} arquivos HTML gerados com sucesso em '{args.output}'!")

    # 3. Gerar sitemap.xml
    sitemap_path = os.path.join(args.output, "sitemap.xml")
    
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
    # Inclui a Home principal do site
    sitemap_content += f"""  <url>
    <loc>{SITE_CONFIG['base_url']}/</loc>
    <priority>1.0</priority>
  </url>
"""
    # Inclui todas as geradas
    for url in generated_urls:
        sitemap_content += f"""  <url>
    <loc>{xml_escape(url)}</loc>
    <priority>0.8</priority>
  </url>
"""
    sitemap_content += "</urlset>\n"

    with open(sitemap_path, "w", encoding="utf-8") as s_file:
        s_file.write(sitemap_content)
    
    print(f"💾 sitemap.xml gerado com sucesso em '{sitemap_path}' ({total + 1} URLs)!")

    # 4. Atualizar/Criar robots.txt na pasta de saída
    robots_path = os.path.join(args.output, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as r_file:
        r_file.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_CONFIG['base_url']}/seo/sitemap.xml\n")
    print(f"💾 robots.txt gerado com sucesso em '{robots_path}'!")


if __name__ == "__main__":
    main()
