<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>E.D.I.T.H Interface</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Styles JARVIS futuristes -->
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background: radial-gradient(circle at top, #112233 0, #02030a 40%, #000000 100%);
            color: #e0f7ff;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        .overlay {
            position: fixed;
            inset: 0;
            background: radial-gradient(circle at center, rgba(0, 255, 255, 0.05), transparent 60%);
            pointer-events: none;
        }

        .container {
            position: relative;
            width: 100%;
            max-width: 480px;
            height: 90vh;
            border-radius: 24px;
            border: 1px solid rgba(0, 255, 255, 0.4);
            background: linear-gradient(135deg, rgba(3, 11, 30, 0.95), rgba(1, 4, 12, 0.98));
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.25);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .hud-top {
            position: relative;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(0, 255, 255, 0.3);
            background: linear-gradient(to right, rgba(0, 0, 0, 0.3), transparent);
        }

        .hud-title {
            font-size: 14px;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: #7ffcff;
        }

        .hud-status {
            font-size: 11px;
            color: #9beeff;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #00ffc8;
            position: relative;
            margin-right: 6px;
        }

        .pulse-dot::after {
            content: "";
            position: absolute;
            inset: -4px;
            border-radius: 50%;
            border: 1px solid rgba(0, 255, 200, 0.5);
            animation: pulse 1.8s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.7); opacity: 1; }
            70% { transform: scale(1.6); opacity: 0; }
            100% { transform: scale(1.6); opacity: 0; }
        }

        .core-visual {
            position: relative;
            padding: 18px 16px 10px 16px;
            border-bottom: 1px solid rgba(0, 255, 255, 0.2);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .core-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 2px solid rgba(0, 255, 255, 0.6);
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.4);
            overflow: hidden;
        }

        .core-circle::before {
            content: "";
            position: absolute;
            inset: 8px;
            border-radius: 50%;
            border: 1px solid rgba(0, 255, 255, 0.4);
        }

        .core-glow {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: radial-gradient(circle, #00fff2 0, #0077ff 40%, transparent 70%);
            animation: corePulse 2.5s infinite alternate;
            opacity: 0.8;
        }

        @keyframes corePulse {
            0% { transform: scale(0.9); opacity: 0.5; }
            100% { transform: scale(1.05); opacity: 1; }
        }

        .core-ring {
            position: absolute;
            width: 170px;
            height: 170px;
            border-radius: 50%;
            border: 1px dashed rgba(0, 255, 255, 0.35);
            animation: spin 18s linear infinite;
        }

        .core-ring:nth-child(2) {
            width: 150px;
            height: 150px;
            animation-duration: 12s;
            animation-direction: reverse;
            opacity: 0.5;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .hud-center-text {
            position: absolute;
            bottom: 10px;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: rgba(173, 238, 255, 0.8);
        }

        .chat-area {
            flex: 1;
            padding: 10px 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: rgba(0, 255, 255, 0.5) transparent;
        }

        .chat-area::-webkit-scrollbar {
            width: 6px;
        }

        .chat-area::-webkit-scrollbar-thumb {
            background: rgba(0, 255, 255, 0.5);
            border-radius: 3px;
        }

        .msg {
            max-width: 85%;
            padding: 8px 10px;
            border-radius: 10px;
            font-size: 13px;
            line-height: 1.4;
            position: relative;
        }

        .msg.user {
            margin-left: auto;
            background: linear-gradient(135deg, #0066ff, #00e0ff);
            color: #eefbff;
            border-bottom-right-radius: 2px;
        }

        .msg.ai {
            margin-right: auto;
            background: rgba(2, 18, 32, 0.95);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-bottom-left-radius: 2px;
        }

        .msg-meta {
            font-size: 9px;
            opacity: 0.7;
            margin-top: 3px;
        }

        .input-area {
            padding: 8px 10px 12px 10px;
            border-top: 1px solid rgba(0, 255, 255, 0.3);
            background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .input-field {
            flex: 1;
            padding: 8px 10px;
            border-radius: 999px;
            border: 1px solid rgba(0, 255, 255, 0.5);
            background: rgba(0, 4, 12, 0.9);
            color: #e0f7ff;
            font-size: 13px;
            outline: none;
        }

        .input-field::placeholder {
            color: rgba(144, 210, 230, 0.7);
        }

        .btn {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 1px solid rgba(0, 255, 255, 0.6);
            background: radial-gradient(circle, rgba(0, 255, 255, 0.2), rgba(0, 0, 0, 0.9));
            color: #9beeff;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 18px;
            cursor: pointer;
            transition: transform 0.1s ease, box-shadow 0.1s ease, background 0.2s;
        }

        .btn:active {
            transform: scale(0.93);
            box-shadow: 0 0 12px rgba(0, 255, 255, 0.7);
            background: radial-gradient(circle, rgba(0, 255, 255, 0.4), rgba(0, 0, 0, 1));
        }

        .btn.disabled {
            opacity: 0.4;
            cursor: default;
        }

        .hud-bottom {
            position: absolute;
            bottom: 52px;
            left: 0;
            width: 100%;
            padding: 4px 12px;
            display: flex;
            justify-content: space-between;
            font-size: 9px;
            color: rgba(144, 210, 230, 0.9);
            text-transform: uppercase;
            letter-spacing: 0.16em;
            pointer-events: none;
        }

        .status-light {
            color: #00ffc8;
        }

        .loading-bar {
            position: absolute;
            top: 0;
            left: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00fff2, #0077ff, transparent);
            animation: loading 2s linear infinite;
            opacity: 0;
        }

        .loading-active {
            opacity: 1;
        }

        @keyframes loading {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        @media (max-width: 500px) {
            .container {
                height: 96vh;
                border-radius: 16px;
            }
        }
    </style>
</head>
<body>
<div class="overlay"></div>

<div class="container">
    <div class="loading-bar" id="loadingBar"></div>

    <div class="hud-top">
        <div>
            <div class="hud-title">E.D.I.T.H SYSTEM</div>
            <div class="hud-status">
                <span class="pulse-dot"></span>
                Lien sécurisé établi
            </div>
        </div>
        <div style="text-align: right; font-size: 10px;">
            <div>MODE: <span style="color:#00ffc8;">ASSISTANT</span></div>
            <div id="timeDisplay"></div>
        </div>
    </div>

    <div class="core-visual">
        <div class="core-ring"></div>
        <div class="core-ring"></div>
        <div class="core-circle">
            <div class="core-glow" id="coreGlow"></div>
        </div>
        <div class="hud-center-text">Protocole J.A.R.V.I.S / E.D.I.T.H</div>
    </div>

    <div class="chat-area" id="chatArea">
        <!-- Messages apparaîtront ici -->
    </div>

    <div class="hud-bottom">
        <div>Canal: PRIVE</div>
        <div class="status-light" id="aiStatus">IA: STANDBY</div>
    </div>

    <div class="input-area">
        <input id="userInput" class="input-field" type="text" placeholder="Donnez un ordre à E.D.I.T.H..." />
        <button id="sendBtn" class="btn">➤</button>
        <!-- Bouton micro (optionnel, pas encore relié à une vraie reco vocale) -->
        <button id="micBtn" class="btn disabled">🎙</button>
    </div>
</div>

<script>
    const API_URL = "https://TON-SERVEUR-EDITH"; // <-- À REMPLACER

    const chatArea = document.getElementById("chatArea");
    const userInput = document.getElementById("userInput");
    const sendBtn = document.getElementById("sendBtn");
    const aiStatus = document.getElementById("aiStatus");
    const loadingBar = document.getElementById("loadingBar");
    const coreGlow = document.getElementById("coreGlow");
    const timeDisplay = document.getElementById("timeDisplay");

    function updateTime() {
        const now = new Date();
        const h = String(now.getHours()).padStart(2, "0");
        const m = String(now.getMinutes()).padStart(2, "0");
        const s = String(now.getSeconds()).padStart(2, "0");
        timeDisplay.textContent = `${h}:${m}:${s}`;
    }
    setInterval(updateTime, 1000);
    updateTime();

    function addMessage(text, from = "ai") {
        const msg = document.createElement("div");
        msg.classList.add("msg");
        msg.classList.add(from === "user" ? "user" : "ai");

        const main = document.createElement("div");
        main.textContent = text;

        const meta = document.createElement("div");
        meta.classList.add("msg-meta");
        const label = from === "user" ? "Vous" : "E.D.I.T.H";
        const now = new Date();
        const h = String(now.getHours()).padStart(2, "0");
        const m = String(now.getMinutes()).padStart(2, "0");
        meta.textContent = `${label} • ${h}:${m}`;

        msg.appendChild(main);
        msg.appendChild(meta);
        chatArea.appendChild(msg);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    function setLoading(isLoading) {
        if (isLoading) {
            loadingBar.classList.add("loading-active");
            aiStatus.textContent = "IA: TRAITEMENT EN COURS";
            coreGlow.style.animationDuration = "1.2s";
        } else {
            loadingBar.classList.remove("loading-active");
            aiStatus.textContent = "IA: STANDBY";
            coreGlow.style.animationDuration = "2.5s";
        }
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        addMessage(text, "user");
        userInput.value = "";
        setLoading(true);

        try {
            const response = await fetch(API_URL + "/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) {
                throw new Error("Erreur réseau");
            }

            const data = await response.json();
            const aiText = data.response || "Erreur: Réponse inattendue du serveur.";

            addMessage(aiText, "ai");
            trySpeak(aiText);

        } catch (err) {
            addMessage("Impossible de contacter le noyau E.D.I.T.H. Vérifiez la connexion au serveur.", "ai");
        } finally {
            setLoading(false);
        }
    }

    function trySpeak(text) {
        if (!("speechSynthesis" in window)) return;
        const synth = window.speechSynthesis;
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = "fr-FR";
        utter.rate = 1.0;
        utter.pitch = 1.05;
        synth.cancel();
        synth.speak(utter);
    }

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    window.addEventListener("load", () => {
        setTimeout(() => {
            addMessage("Systèmes E.D.I.T.H initialisés. Connexion sécurisée au terminal mobile établie. En attente de vos instructions.", "ai");
            trySpeak("Systèmes E.D.I.T.H initialisés. Connexion sécurisée établie. En attente de vos instructions.");
        }, 600);
    });
</script>
</body>
</html>
