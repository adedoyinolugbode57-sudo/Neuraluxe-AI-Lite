"""
Neuraluxe-AI AI Engine (Online-enabled)
---------------------------------------
- Lightweight and premium-rich
- Pulls jokes, quotes, definitions online
- Sharp responses, coding support (~2000 lines)
- GPT-style chat bubbles
- Free vs premium user behavior
"""

import random
import requests
import re
from helpers import truncate_text
from session_manager import FREE_USER_EMAIL, is_free_user

# -------------------------
# Local fallback knowledge
# -------------------------
knowledge_base = {
    "python": "Python is a high-level, interpreted programming language known for readability.",
    "ai": "AI simulates human intelligence in machines that can think like humans.",
    "neural network": "Algorithms that detect relationships in data.",
    "flask": "Lightweight Python web framework.",
    "api": "Allows communication between software applications."
}

# -------------------------
# Helper to fetch online data
# -------------------------
def fetch_online_json(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# -------------------------
# Chat formatting
# -------------------------
def format_response(user_email, text, is_code=False):
    bubble_style = "🟦" if is_free_user(user_email) else "🟩"
    lines = text.split("\n")
    formatted = "\n".join([f"{bubble_style} {truncate_text(line, 80)}" for line in lines])
    return formatted

# -------------------------
# AI Response Generation
# -------------------------
def ai_response(user_email, prompt):
    # Free-user limited knowledge
    if is_free_user(user_email) and user_email != FREE_USER_EMAIL:
        limited_knowledge = {k: knowledge_base[k] for k in list(knowledge_base)[:3]}
        knowledge = limited_knowledge
    else:
        knowledge = knowledge_base

    response = None

    # Check local knowledge
    for key, val in knowledge.items():
        if key.lower() in prompt.lower():
            response = val
            break

    # Check for code generation
    if "code" in prompt.lower() or "program" in prompt.lower():
        code_lines = ["# Example Neuraluxe-AI code snippet"]
        for i in range(20):
            code_lines.append(f"print('Line {i+1}: Neuraluxe-AI code engine')")
        response = "\n".join(code_lines)

    # Online jokes
    if "joke" in prompt.lower():
        joke_data = fetch_online_json("https://official-joke-api.appspot.com/random_joke")
        if joke_data:
            response = f"{joke_data.get('setup','')} ... {joke_data.get('punchline','')}"
        else:
            response = "Why did the AI cross the road? To compute the other side!"

    # Online quotes
    if "quote" in prompt.lower():
        quote_data = fetch_online_json("https://type.fit/api/quotes")
        if quote_data:
            choice = random.choice(quote_data)
            response = choice.get("text", "Keep learning and stay curious!")

    # Online definitions
    if "define" in prompt.lower():
        word = prompt.lower().replace("define", "").strip()
        dictionary_data = fetch_online_json(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if dictionary_data and isinstance(dictionary_data, list):
            meanings = dictionary_data[0].get("meanings", [])
            if meanings:
                definition = meanings[0]["definitions"][0].get("definition", "Definition not found.")
                response = f"{word.capitalize()}: {definition}"
        else:
            response = f"{word.capitalize()}: Definition not found."

    # Default fallback
    if not response:
        fallback = [
            "That's interesting! Can you tell me more?",
            "I think I understand. Let's dive deeper.",
            f"Hmm… analyzing '{prompt}' carefully.",
            f"Here's a thought: {prompt[:50]}"
        ]
        response = random.choice(fallback)

    return format_response(user_email, response, is_code="code" in prompt.lower())

# -------------------------
# Add knowledge
# -------------------------
def add_knowledge(user_email, keyword, content):
    if is_free_user(user_email) and user_email != FREE_USER_EMAIL:
        print("Free users cannot add knowledge. Upgrade for full access.")
        return
    knowledge_base[keyword] = content
    print(f"Knowledge '{keyword}' added successfully!")

# -------------------------
# Standalone test
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    while True:
        prompt = input("\nYou: ").strip()
        if prompt.lower() in ["exit", "quit"]:
            print("Exiting Neuraluxe-AI engine...")
            break
        reply = ai_response(email, prompt)
        print("\nNeuraluxe-AI:\n" + reply)