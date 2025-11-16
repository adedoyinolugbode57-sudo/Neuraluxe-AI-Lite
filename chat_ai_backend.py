"""
Neuraluxe-AI Chat Backend (Upgraded)
------------------------------------
- Handles multi-turn sessions
- Integrates online AI response simulation
- Tracks free vs premium limits per session
- Supports translation for 100+ languages
- Logs activity and stores persistent chat history
"""

import os
import json
from datetime import datetime
from random import choice
from session_manager import is_free_user, update_login_timestamp
from translation_hub_full import translate_for_user, get_user_language, switch_language
from logger import log_activity

CHAT_HISTORY_DIR = "chat_histories"
REPLY_LIMIT_FREE = 3  # free users per session

os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

# -----------------------------
# Chat History Functions
# -----------------------------
def load_history(user_email):
    path = os.path.join(CHAT_HISTORY_DIR, f"{user_email.replace('@','_')}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"messages": []}

def save_history(user_email, history):
    path = os.path.join(CHAT_HISTORY_DIR, f"{user_email.replace('@','_')}.json")
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

# -----------------------------
# AI Response Simulation
# -----------------------------
def simulate_online_ai_response(user_input, context, user_language):
    """
    Simulate an online AI or web-integrated LLM.
    Can be replaced by real API call.
    """
    generic_replies = [
        "Interesting! Tell me more.",
        "I see, can you elaborate?",
        "Hmm… that's thought-provoking.",
        "Absolutely! I agree.",
        "Could you explain that differently?",
        "Fascinating, thanks for sharing!",
        "I'm listening… continue."
    ]
    # Short inputs: generic reply, longer inputs: fallback web-search hint
    if len(user_input) < 20:
        return choice(generic_replies)
    if "weather" in user_input.lower():
        return f"In {user_language}: The weather is nice today near you."
    return f"I’m not sure—I found this for you: https://www.google.com/search?q={user_input.replace(' ', '+')}"

# -----------------------------
# Message Handler
# -----------------------------
def handle_message(user_email, message, session_context, replies_count):
    """
    Handles a single user message:
    - Updates login timestamp
    - Enforces free user limits
    - Translates message
    - Generates AI response
    - Logs activity
    - Updates history
    """
    update_login_timestamp(user_email)
    user_language = get_user_language(user_email)

    if is_free_user(user_email) and replies_count >= REPLY_LIMIT_FREE:
        return "⚠️ Free user reply limit reached for this session. Upgrade for unlimited chats.", replies_count

    translated_input = translate_for_user(user_email, message)
    ai_response_raw = simulate_online_ai_response(translated_input, session_context, user_language)
    ai_response_translated = translate_for_user(user_email, ai_response_raw)

    # Log
    log_activity(user_email, f"User sent: {message} | AI responded: {ai_response_translated}")

    # Update session context
    session_context.append({"sender": "user", "text": message})
    session_context.append({"sender": "ai", "text": ai_response_translated})

    return ai_response_translated, replies_count + 1

# -----------------------------
# Chat Session
# -----------------------------
def start_chat_session(user_email):
    print("\n=== Neuraluxe-AI Chat ===")
    print(f"Current language: {get_user_language(user_email)}")

    history = load_history(user_email)
    session_context = history["messages"][-5:]  # last 5 messages as context
    replies_count = 0

    while True:
        print("\nOptions:")
        print("1. Send Message")
        print("2. Switch Language")
        print("3. Show Current Language")
        print("4. Show Last 10 Messages")
        print("5. Exit Chat")
        choice = input("Select option: ").strip()

        if choice == "1":
            user_msg = input("You: ").strip()
            if not user_msg:
                print("You typed nothing. Try again.")
                continue
            ai_response, replies_count = handle_message(user_email, user_msg, session_context, replies_count)
            print(f"Neuraluxe ({get_user_language(user_email)}): {ai_response}")

        elif choice == "2":
            switch_language(user_email)
            print(f"Language switched to {get_user_language(user_email)}.")

        elif choice == "3":
            print("Current language:", get_user_language(user_email))

        elif choice == "4":
            print("\n📁 Last 10 messages:")
            for m in session_context[-10:]:
                print(f"{m['sender']}: {m['text']}")

        elif choice == "5":
            log_activity(user_email, "Closed chat session")
            history["messages"].extend(session_context)
            save_history(user_email, history)
            print("Exiting chat...")
            break
        else:
            print("Invalid choice. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    start_chat_session(email)