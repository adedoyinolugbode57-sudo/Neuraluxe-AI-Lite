"""
chat_code_generator.py
----------------------
Neuraluxe-AI Chat Inline Code Generator
- Fully integrated into chat tab
- Command: /code <instruction>
- Lightweight & multi-language
- Max ~2000 lines of code
- Inline response in chat bubbles
"""

import random
from helpers import truncate_text

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
# Generate Random Function/Class Name
# -------------------------
def random_name(prefix="func"):
    return f"{prefix}_{random.randint(1000,9999)}"

# -------------------------
# Generate Code
# -------------------------
def generate_code(instruction, language=None, max_lines=2000):
    language = language.lower() if language else random.choice(LANGUAGES)
    if language not in LANGUAGES:
        language = "python"
    
    func_name = random_name()
    template = CODE_TEMPLATES[language]
    code = template.format(func_name=func_name, instruction=instruction)
    
    # Repeat template to simulate multi-line code if needed, but limit lines
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
    return f"💻 Generated {lang} code:\n```\n{display}\n```"

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    print("Neuraluxe-AI Chat Code Generator Initialized")
    print("Type '/code <instruction>' to generate code.\n")
    
    while True:
        msg = input("You: ").strip()
        if msg.lower() in ["exit", "quit"]:
            print("Exiting code generator...")
            break
        response = handle_chat_command("user@example.com", msg)
        if response:
            print("AI:", response)
        else:
            print("AI: Message received (not a code command)")