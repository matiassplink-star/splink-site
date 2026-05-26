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
                window.open(`https://wa.me/5534999929764?text=${encodeURIComponent(msg)}`, '_blank');
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
