// Initialize Lucide Icons
lucide.createIcons();

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Navbar Scroll Effect
const navbar = document.getElementById('mainNavbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Scroll Reveal Animation
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-up');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.service-card, .about-content, h2, p').forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
});

// Cookie Banner Logic
const cookieBanner = document.querySelector('.cookie-banner');
const acceptCookies = document.getElementById('acceptCookies');

if (cookieBanner && !localStorage.getItem('cookiesAccepted')) {
    setTimeout(() => {
        cookieBanner.classList.add('show');
    }, 2000);
}

if (acceptCookies) {
    acceptCookies.addEventListener('click', () => {
        localStorage.setItem('cookiesAccepted', 'true');
        cookieBanner.classList.remove('show');
    });
}


// Chat Widget Logic
const chatWidgetHTML = `
    <div class="chat-widget">
        <button class="chat-button">
            <i data-lucide="bot"></i>
        </button>
        <div class="chat-window">
            <div class="chat-header">
                <div class="chat-avatar">
                    <img src="Criar_um_foto_profssional_porfavor_202605051827 (1).jpeg" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
                </div>
                <div class="chat-info">
                    <div class="chat-name">Mark I.A</div>
                    <div class="chat-status">Online agora</div>
                </div>
                <button class="chat-close" id="closeChat"><i data-lucide="x"></i></button>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message bot">
                    Olá. Sou o assistente inteligente da Splink. Como posso ajudar a escalar seu negócio hoje?
                </div>
            </div>
            <div class="chat-input">
                <input type="text" placeholder="Digite sua mensagem..." id="chatInput">
                <button id="sendMessage">
                    <i data-lucide="send"></i>
                </button>
            </div>
        </div>
    </div>
`;

document.body.insertAdjacentHTML('beforeend', chatWidgetHTML);
lucide.createIcons();

const chatButton = document.querySelector('.chat-button');
const chatWindow = document.querySelector('.chat-window');
const chatInput = document.getElementById('chatInput');
const sendMessage = document.getElementById('sendMessage');
const chatMessages = document.getElementById('chatMessages');

let step = 0;
let leadData = { name: '', phone: '' };

if (chatButton) {
    chatButton.addEventListener('click', () => {
        chatWindow.classList.toggle('show');
    });
}

const closeChat = document.getElementById('closeChat');
if (closeChat) {
    closeChat.addEventListener('click', () => {
        chatWindow.classList.remove('show');
    });
}

const addMessage = (text, type) => {
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    msg.textContent = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
};

const handleBotResponse = (userText) => {
    setTimeout(() => {
        if (step === 0) {
            addMessage("Compreendido. Para que eu possa te passar as melhores informações sobre nossas automações e IA, qual o seu nome?", "bot");
            step = 1;
        } else if (step === 1) {
            leadData.name = userText;
            addMessage(`Prazer, ${leadData.name}. Qual o seu melhor WhatsApp (com DDD) para enviarmos o material detalhado?`, "bot");
            step = 2;
        } else if (step === 2) {
            leadData.phone = userText;
            addMessage("Anotado. Para agilizar seu atendimento e garantir sua licença, clique no botão abaixo para validar seus dados via WhatsApp.", "bot");
            
            const waBtn = document.createElement('button');
            waBtn.className = 'btn btn-primary';
            waBtn.style.marginTop = '12px';
            waBtn.style.width = '100%';
            waBtn.innerHTML = '<i data-lucide="message-circle"></i> Finalizar via WhatsApp';
            waBtn.onclick = () => {
                const msg = `Protocolo de Escala - Lead Chatbot\n\nNome: ${leadData.name}\nWhatsApp: ${leadData.phone}\nInteresse: Atendimento via Site`;
                window.open(`https://wa.me/5511999999999?text=${encodeURIComponent(msg)}`, '_blank');
            };
            chatMessages.appendChild(waBtn);
            lucide.createIcons();
            
            console.log("Lead Capturado:", leadData);
            step = 3;
        } else {
            addMessage("Entendido. Nosso time tático já foi alertado. Algo mais?", "bot");
        }
    }, 1000);
};

if (sendMessage) {
    sendMessage.addEventListener('click', () => {
        const text = chatInput.value.trim();
        if (text) {
            addMessage(text, 'user');
            chatInput.value = '';
            handleBotResponse(text);
        }
    });
}

if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage.click();
    });
}

// --- GLOBAL CYBERPUNK THEME LOGIC ---

// 1. Matrix Rain Canvas (Inject if not present)
if (!document.getElementById('matrixCanvas')) {
    const canvas = document.createElement('canvas');
    canvas.id = 'matrixCanvas';
    canvas.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.4; pointer-events: none;';
    document.body.prepend(canvas);
    
    if (!document.querySelector('.glow-bg')) {
        const glow = document.createElement('div');
        glow.className = 'glow-bg';
        glow.style.cssText = 'top: -200px; left: -200px; background: radial-gradient(circle, rgba(0, 212, 255, 0.05) 0%, transparent 70%); z-index: -2; position: fixed; width: 100vw; height: 100vh;';
        document.body.prepend(glow);
    }
}

const matrixCanvas = document.getElementById('matrixCanvas');
if (matrixCanvas) {
    const ctx = matrixCanvas.getContext('2d');
    matrixCanvas.width = window.innerWidth;
    matrixCanvas.height = window.innerHeight;
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$#@&%*";
    const fontSize = 14;
    let columns = matrixCanvas.width / fontSize;
    const drops = [];
    for (let x = 0; x < columns; x++) drops[x] = 1;

    let matrixSpeed = 300; 
    let lastDrawTime = 0;
    
    // Evita múltiplas instâncias se o script rodar mais de uma vez
    if (window.matrixAnimId) cancelAnimationFrame(window.matrixAnimId);

    function drawMatrix(timestamp) {
        window.matrixAnimId = requestAnimationFrame(drawMatrix);
        
        if (timestamp - lastDrawTime < matrixSpeed) return;
        lastDrawTime = timestamp;

        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);
        for (let i = 0; i < drops.length; i++) {
            const text = letters.charAt(Math.floor(Math.random() * letters.length));
            ctx.fillStyle = Math.random() > 0.9 ? '#ffffff' : '#00d4ff';
            ctx.font = fontSize + 'px monospace';
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > matrixCanvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
        
        if (matrixSpeed > 33) {
            matrixSpeed -= 2; 
        }
    }
    window.matrixAnimId = requestAnimationFrame(drawMatrix);
    window.addEventListener('resize', () => {
        matrixCanvas.width = window.innerWidth;
        matrixCanvas.height = window.innerHeight;
        columns = matrixCanvas.width / fontSize;
    });
}

// 2. Cinematic Shutter Transition Overlay
if (!document.getElementById('warp-overlay')) {
    const overlay = document.createElement('div');
    overlay.id = 'warp-overlay';
    overlay.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 9999; pointer-events: none; display: flex; flex-direction: column; justify-content: space-between;';
    overlay.innerHTML = `
        <div id="shutter-top" style="width: 100%; height: 50%; background: #050506; transition: height 0.6s cubic-bezier(0.86, 0, 0.07, 1); border-bottom: 2px solid var(--accent);"></div>
        <div id="shutter-bottom" style="width: 100%; height: 50%; background: #050506; transition: height 0.6s cubic-bezier(0.86, 0, 0.07, 1); border-top: 2px solid var(--accent);"></div>
    `;
    document.body.appendChild(overlay);
    
    // Animação de saída se estiver carregando uma nova página
    function openShutters() {
        const top = document.getElementById('shutter-top');
        const bottom = document.getElementById('shutter-bottom');
        if(top && bottom) {
            top.style.height = '0%';
            bottom.style.height = '0%';
        }
    }

    window.addEventListener('load', () => {
        const isHome = window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.endsWith('/');
        
        if (!sessionStorage.getItem('splinkFirstVisit') && isHome) {
            // Cria a tela de Boot Inicial Automática
            const bootScreen = document.createElement('div');
            bootScreen.id = 'boot-screen';
            bootScreen.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 10000; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--accent); font-family: monospace; transition: opacity 0.5s ease;';
            
            bootScreen.innerHTML = `
                <div id="boot-terminal-window" style="width: 90%; max-width: 600px; background: rgba(5,5,6,0.95); border: 1px solid var(--accent); border-radius: 8px; overflow: hidden; box-shadow: 0 0 30px rgba(0,212,255,0.15);">
                    <div style="background: rgba(0,212,255,0.1); border-bottom: 1px solid var(--accent); padding: 10px; display: flex; gap: 8px; align-items: center;">
                        <div style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f56; opacity: 0.8;"></div>
                        <div style="width: 12px; height: 12px; border-radius: 50%; background: #ffbd2e; opacity: 0.8;"></div>
                        <div style="width: 12px; height: 12px; border-radius: 50%; background: #27c93f; opacity: 0.8;"></div>
                        <div style="flex: 1; text-align: center; color: var(--accent); font-size: 12px; letter-spacing: 2px;">ROOT@SPLINK_SYS:~</div>
                    </div>
                    <div style="padding: 20px; font-size: 14px; line-height: 1.6; min-height: 220px; display: flex; flex-direction: column;">
                        <div id="boot-logs" style="color: #ccc; flex: 1;"></div>
                        
                        <div id="boot-progress-container" style="display: none; margin-top: 20px;">
                            <div style="margin-bottom: 8px; color: var(--accent); text-transform: uppercase; letter-spacing: 1px;">Protocolo Hacking I.A Business...</div>
                            <div style="width: 100%; height: 2px; background: rgba(0,212,255,0.2); position: relative; overflow: hidden;">
                                <div id="boot-progress-bar" style="position: absolute; top: 0; left: 0; height: 100%; width: 0%; background: var(--accent); box-shadow: 0 0 10px var(--accent);"></div>
                            </div>
                            <div id="boot-percentage" style="text-align: right; margin-top: 5px; font-size: 12px; color: var(--accent);">0%</div>
                        </div>

                        <div id="boot-success" style="display: none; color: #10b981; font-weight: bold; font-size: 18px; margin-top: 20px; text-shadow: 0 0 10px rgba(16,185,129,0.5); letter-spacing: 2px;">ACESSO LIBERADO_</div>
                    </div>
                </div>
            `;
            document.body.appendChild(bootScreen);

            // Tenta iniciar a música automaticamente (pode ser bloqueado pelo browser)
            if(typeof startBgAudio === 'function') startBgAudio();
            
            const logsContainer = document.getElementById('boot-logs');
            const progressContainer = document.getElementById('boot-progress-container');
            const progressBar = document.getElementById('boot-progress-bar');
            const progressText = document.getElementById('boot-percentage');
            const successMsg = document.getElementById('boot-success');
            
            const bootLogs = [
                "Inicializando sistema base...",
                "Bypass de segurança firewalls locais...",
                "Sincronizando Módulo de I.A...",
                "Estabelecendo conexão segura..."
            ];
            
            let logIndex = 0;
            const printLog = () => {
                if (logIndex < bootLogs.length) {
                    logsContainer.innerHTML += `<div>> ${bootLogs[logIndex]}</div>`;
                    if(typeof playClickSound === 'function') playClickSound();
                    logIndex++;
                    setTimeout(printLog, Math.random() * 80 + 30);
                } else {
                    // Iniciar barra de progresso
                    progressContainer.style.display = 'block';
                    let progress = 0;
                    const fillBar = setInterval(() => {
                        progress += Math.floor(Math.random() * 30) + 20;
                        if (progress > 100) progress = 100;
                        progressBar.style.width = progress + '%';
                        progressText.innerText = progress + '%';
                        
                        if (progress === 100) {
                            clearInterval(fillBar);
                            if(typeof playClickSound === 'function') playClickSound();
                            successMsg.style.display = 'block';
                            
                            setTimeout(() => {
                                bootScreen.style.opacity = '0';
                                setTimeout(() => {
                                    bootScreen.remove();
                                    sessionStorage.setItem('splinkFirstVisit', 'true');
                                    openShutters();
                                }, 500);
                            }, 1000);
                        }
                    }, 100);
                }
            };
            
            setTimeout(printLog, 300);

        } else {
            // Fluxo normal
            setTimeout(openShutters, 100);
        }
    });
}

// Interatividade Dinâmica dos Blocos de Status
setInterval(() => {
    const scanners = document.querySelectorAll('.scanning-text');
    scanners.forEach(scanner => {
        if (scanner.innerText.includes('msg/h') || scanner.innerText.match(/[0-9]/)) {
            const base = 10400;
            const random = Math.floor(Math.random() * 99);
            scanner.innerText = '10.' + (400 + random) + ' msg/h';
        } else if (scanner.innerText.includes('RUNNING') || scanner.innerText.includes('SCANNING')) {
            scanner.innerText = Math.random() > 0.5 ? 'RUNNING...' : 'SCANNING...';
        } else if (scanner.innerText.includes('ENCRYPTED') || scanner.innerText.includes('SECURE')) {
            scanner.innerText = Math.random() > 0.8 ? 'SECURE' : 'ENCRYPTED';
        }
    });
}, 400);

// 3. Cybernetic Click Sound
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
function playClickSound() {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    oscillator.type = 'square';
    oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.1);
    gainNode.gain.setValueAtTime(0.05, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    oscillator.start();
    oscillator.stop(audioCtx.currentTime + 0.1);
}

// 4. Continuous Audio Logic
const bgAudio = new Audio('hitslab-cyberpunk-futuristic-cyberpunk-industrial-music-474697.mp3');
bgAudio.loop = true;
const isHome = window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.endsWith('/');
bgAudio.volume = isHome ? 0.15 : 0.10;

const savedTime = sessionStorage.getItem('splinkAudioTime');
if (savedTime) bgAudio.currentTime = parseFloat(savedTime);

let audioStarted = false;
const startBgAudio = () => {
    if(audioStarted && !bgAudio.paused) return;
    bgAudio.play().then(() => {
        audioStarted = true;
    }).catch(e => {
        console.log("Browser bloqueou autoplay. Aguardando interação.");
    });
};

// Força o play imediato
startBgAudio();

// Fallback: se o browser bloquear, tenta no primeiro clique/scroll
['click', 'touchstart', 'scroll'].forEach(evt => {
    document.body.addEventListener(evt, startBgAudio, { once: true });
});

setInterval(() => {
    if (!bgAudio.paused) sessionStorage.setItem('splinkAudioTime', bgAudio.currentTime);
}, 500);

// 5. Global Click Interception
document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    const isServiceOrBtn = e.target.closest('.option-card, .service-card, .btn') || (link && !link.getAttribute('href').startsWith('#'));
    
    if (isServiceOrBtn) playClickSound();

    if (link && link.getAttribute('href') && !link.getAttribute('href').startsWith('#') && !link.getAttribute('target')) {
        e.preventDefault();
        const targetUrl = link.getAttribute('href');
        
        // Ativa o Shutter Cinematográfico
        const top = document.getElementById('shutter-top');
        const bottom = document.getElementById('shutter-bottom');
        if (top && bottom) {
            top.style.height = '50%';
            bottom.style.height = '50%';
        }
        
        sessionStorage.setItem('splinkAudioTime', bgAudio.currentTime);
        setTimeout(() => window.location.href = targetUrl, 500); // Mais rápido para parecer cena de filme
    }
});
