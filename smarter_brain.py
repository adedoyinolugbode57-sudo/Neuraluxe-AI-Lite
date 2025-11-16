"""
Neuraluxe-AI: Smarter Brain Module
----------------------------------
- Lightweight reasoning engine
- Predictions, suggestions, and context-based insights
- Premium-ready features
- Modular for integration with Neuraluxe-AI ecosystem
"""

import random
import json
import os
from datetime import datetime

# -----------------------------
# Config & Storage
# -----------------------------
BRAIN_DATA_FILE = "smarter_brain.json"

def load_brain_data():
    if not os.path.exists(BRAIN_DATA_FILE):
        with open(BRAIN_DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(BRAIN_DATA_FILE, "r") as f:
        return json.load(f)

def save_brain_data(data):
    with open(BRAIN_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# Activity Logging
# -----------------------------
def log_brain_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[BRAIN] {timestamp} - {user_email} - {action}")

# -----------------------------
# Context & Knowledge
# -----------------------------
KNOWLEDGE_BASE = {
    "greetings": ["Hello!", "Hi there!", "Greetings!", "Hey! How’s it going?"],
    "farewells": ["Goodbye!", "See you later!", "Catch you soon!", "Take care!"],
    "tips": [
        "Break big tasks into smaller ones.",
        "Stay hydrated while working.",
        "Organize your day for focus.",
        "Always review your previous work."
    ],
    "fun_facts": [
        "Octopuses have three hearts.",
        "Bananas are berries but strawberries aren't.",
        "AI can simulate reasoning patterns.",
        "Honey never spoils."
    ]
}

# -----------------------------
# Predictive Functions
# -----------------------------
def predict_next_action(context_list):
    """
    Lightweight prediction based on previous context
    """
    possible_actions = ["search", "summarize", "analyze", "suggest", "recommend"]
    if context_list:
        weighted_actions = [action for action in possible_actions for _ in range(len(context_list))]
        choice = random.choice(weighted_actions)
    else:
        choice = random.choice(possible_actions)
    return choice

def quick_insight(user_input):
    """
    Generates a short insight or suggestion from input
    """
    insights = [
        "Did you know?", "Consider this:", "A thought:", "Tip:", "Fun fact:"
    ]
    fact = random.choice(KNOWLEDGE_BASE["fun_facts"])
    return f"{random.choice(insights)} {user_input[:50]}... → {fact}"

# -----------------------------
# Conversation Handlers
# -----------------------------
def respond_to_greeting():
    return random.choice(KNOWLEDGE_BASE["greetings"])

def respond_to_farewell():
    return random.choice(KNOWLEDGE_BASE["farewells"])

def offer_random_tip():
    return random.choice(KNOWLEDGE_BASE["tips"])

# -----------------------------
# Memory System
# -----------------------------
def remember_fact(user_email, key, value):
    data = load_brain_data()
    user_memory = data.setdefault(user_email, {}).setdefault("memory", {})
    user_memory[key] = value
    save_brain_data(data)
    log_brain_activity(user_email, f"Remembered '{key}'")

def recall_fact(user_email, key):
    data = load_brain_data()
    return data.get(user_email, {}).get("memory", {}).get(key, None)

# -----------------------------
# Pattern Analysis (lightweight)
# -----------------------------
def simple_pattern_analysis(text):
    """
    Analyzes text for basic patterns: length, vowels, repeated words
    """
    words = text.split()
    word_count = len(words)
    vowels = sum(1 for c in text.lower() if c in "aeiou")
    repeated_words = set([w for w in words if words.count(w) > 1])
    return {
        "word_count": word_count,
        "vowel_count": vowels,
        "repeated_words": list(repeated_words)
    }

# -----------------------------
# Simulation Engine
# -----------------------------
def simulate_brain_decision(context):
    """
    Simulates a reasoning decision based on context and knowledge
    """
    decision_score = random.randint(0, 100)
    action = predict_next_action(context)
    insight = quick_insight(action)
    return {
        "action": action,
        "score": decision_score,
        "insight": insight
    }

# -----------------------------
# Premium Helper Functions
# -----------------------------
def generate_smart_suggestion(user_email, topic):
    """
    Combines memory recall, tips, and pattern analysis
    """
    memory_fact = recall_fact(user_email, topic)
    if memory_fact:
        suggestion = f"Based on your previous note on '{topic}': {memory_fact}"
    else:
        suggestion = f"New insight on '{topic}': {quick_insight(topic)}"
    return suggestion

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    user = input("Enter email: ").strip()

    log_brain_activity(user, "Started Smarter Brain session")

    print("\n[Greeting] ", respond_to_greeting())
    print("[Tip] ", offer_random_tip())

    text_input = input("\nEnter text for pattern analysis: ").strip()
    analysis = simple_pattern_analysis(text_input)
    print("\nPattern Analysis:", analysis)

    context = ["task1", "task2"]
    decision = simulate_brain_decision(context)
    print("\nSimulated Brain Decision:", decision)

    topic = input("\nEnter topic for smart suggestion: ").strip()
    suggestion = generate_smart_suggestion(user, topic)
    print("\nSmart Suggestion:", suggestion)

    remember_fact(user, topic, suggestion)
    recall = recall_fact(user, topic)
    print("\nMemory Recall:", recall)

    print("\n[Farewell] ", respond_to_farewell())