// =============================
//  TAB SWITCHER
// =============================
function openTab(tabId) {
    const tabs = document.querySelectorAll(".tab-content");
    tabs.forEach(t => t.classList.remove("active"));

    const activeTab = document.getElementById(tabId);
    if (activeTab) {
        activeTab.classList.add("active");
        activeTab.scrollTop = 0;
    }
}

// =============================
//  CHAT SYSTEM
// =============================
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");

function sendMessage() {
    let text = userInput.value.trim();
    if (text === "") return;

    addBubble(text, "user");

    userInput.value = "";
    setTimeout(() => generateAIResponse(text), 300);
}

function addBubble(message, type) {
    const bubble = document.createElement("div");
    bubble.className = type === "user" ? "bubble user-bubble" : "bubble ai-bubble";

    bubble.innerText = message;
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Fake lightweight AI response
function generateAIResponse(prompt) {
    const replies = [
        "Got it! 💡",
        "Interesting… tell me more.",
        "Let’s break that down together.",
        "Noted. What’s next?",
        "Processing that with style…"
    ];

    const reply = replies[Math.floor(Math.random() * replies.length)];
    addBubble(reply, "ai");
}

// Enter key support
document.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
});

// =============================
//  VOICE ASSISTANT
// =============================
function startVoice() {
    if (!("webkitSpeechRecognition" in window)) {
        alert("Voice recognition not supported on this browser.");
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.start();

    recognition.onresult = event => {
        let text = event.results[0][0].transcript;
        addBubble("🎤 " + text, "user");
        setTimeout(() => generateAIResponse(text), 400);
    };

    recognition.onerror = () => {
        addBubble("❌ Voice capture failed.", "ai");
    };
}

// =============================
//  SMALL NEON RIPPLE EFFECT
// =============================
document.addEventListener("click", function(e) {
    const ripple = document.createElement("span");
    ripple.className = "ripple";
    ripple.style.left = e.pageX + "px";
    ripple.style.top = e.pageY + "px";

    document.body.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
});