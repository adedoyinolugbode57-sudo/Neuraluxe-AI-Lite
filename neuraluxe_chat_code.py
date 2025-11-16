"""
neuraluxe_chat_code.py
----------------------
Neuraluxe-AI Chat Inline Code Generator & Mini Chat Tab
- Inline /code <instruction> command
- Multi-language: Python, JS, Java, C++, C#, Ruby, Go, PHP
- Lightweight & deployable
- Max ~2000 lines simulated
- Fully integrated with chat bubble style
- Premium-ready & modular
"""

import random, time
from helpers import truncate_text, generate_id, current_timestamp

# -------------------------
# Supported Languages
# -------------------------
LANGUAGES = ["python", "javascript", "java", "c++", "c#", "ruby", "go", "php"]

# -------------------------
# Lightweight Code Templates
# -------------------------
CODE_TEMPLATES = {
    "python": "def {func_name}():\n    # {instruction}\n    pass\n",
    "javascript": "function {func_name}() {{\n    // {instruction}\n}}\n",
    "java": "public class {func_name} {{\n    // {instruction}\n}}\n",
    "c++": "void {func_name}() {{\n    // {instruction}\n}}\n",
    "c#": "public class {func_name} {{\n    // {instruction}\n}}\n",
    "ruby": "def {func_name}\n  # {instruction}\nend\n",
    "go": "func {func_name}() {{\n    // {instruction}\n}}\n",
    "php": "<?php\nfunction {func_name}() {{\n    // {instruction}\n}}\n?>"
}

# -------------------------
# Generate Random Name
# -------------------------
def random_name(prefix="func"):
    return f"{prefix}_{random.randint(1000,9999)}"

# -------------------------
# Generate Code Function
# -------------------------
def generate_code(instruction, language=None, max_lines=2000):
    language = language.lower() if language else random.choice(LANGUAGES)
    if language not in LANGUAGES:
        language = "python"

    func_name = random_name()
    template = CODE_TEMPLATES[language]
    code = template.format(func_name=func_name, instruction=instruction)

    # Repeat to simulate multi-line but capped at max_lines
    lines = code.splitlines()
    total_lines = min(max_lines, len(lines)*10)
    code_lines = (lines * (total_lines // len(lines)+1))[:total_lines]

    return language, "\n".join(code_lines)

# -------------------------
# Chat Command Handler
# -------------------------
def handle_chat_command(user_email, message):
    message = message.strip()
    if not message.startswith("/code "):
        return None  # Not a code command

    instruction = message[len("/code "):].strip()
    if not instruction:
        return "❌ Please provide an instruction after /code."

    lang, code = generate_code(instruction)
    display = truncate_text(code, 1500)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] 💻 {lang.upper()} Code Generated:\n```\n{display}\n```"

# -------------------------
# Minimal Chat Tab Integration
# -------------------------
def chat_tab_ui(user_email):
    print("\n==============================")
    print("      NEURALUXE CHAT TAB      ")
    print("==============================\n")
    print("Type messages normally. Use '/code <instruction>' to generate code.\nType 'exit' to quit.\n")

    while True:
        msg = input(f"{user_email}: ").strip()
        if msg.lower() in ["exit", "quit"]:
            print("Exiting Neuraluxe Chat Tab...\n")
            break

        response = handle_chat_command(user_email, msg)
        if response:
            print(f"AI: {response}")
        else:
            # Normal chat placeholder
            print(f"AI: Message received: {truncate_text(msg, 200)}")

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    chat_tab_ui(email)