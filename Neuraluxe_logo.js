// === DYNAMIC STARS ===
const starsContainer = document.querySelector('.stars');
for (let i = 0; i < 60; i++) {
  const s = document.createElement('div');
  s.classList.add('star');
  s.style.width = s.style.height = Math.random() * 2 + 'px';
  s.style.top = Math.random() * 100 + '%';
  s.style.left = Math.random() * 100 + '%';
  s.style.animationDelay = Math.random() * 5 + 's';
  starsContainer.appendChild(s);
}

// === DYNAMIC NEURAL LINES ===
const linesContainer = document.querySelector('.neural-lines');
for (let i = 0; i < 20; i++) {
  const line = document.createElement('div');
  line.classList.add('line');
  line.style.left = Math.random() * 100 + '%';
  line.style.animationDuration = 3 + Math.random() * 2 + 's';
  line.style.animationDelay = Math.random() * 3 + 's';
  linesContainer.appendChild(line);
}

// === BUTTON ACTIONS ===
function goHome() {
  window.location.href = "index.html";
}
function openDocs() {
  window.open("https://neuraluxe-ai-docs.example.com", "_blank");
}
function openSupport() {
  window.open("mailto:support@neuraluxe.ai");
}