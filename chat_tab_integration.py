"""
Neuraluxe-AI Chat Integration
-----------------------------
- Handles all chat input
- Premium-only access
- Routes normal messages to AI engine
- Routes /code commands to code generator
- Logs messages and handles errors
"""

import time
from datetime import datetime
from config import check_premium, record_chat
from ai_engine import ai_response
from chat_code_generator import handle_chat_command

# Optional in-memory cache for repeated messages
CHAT_CACHE = {}  # Format: {user_email: {message: (reply, expire_time)}}

CACHE_TTL = 3600  # seconds

def get_cache(user_email, message):
    user_cache = CHAT_CACHE.get(user_email, {})
    entry = user_cache.get(message)
    if entry and entry[1] > time.time():
        return entry[0]
    elif entry:
        del user_cache[message]
    return None

def set_cache(user_email, message, reply):
    user_cache = CHAT_CACHE.setdefault(user_email, {})
    user_cache[message] = (reply, time.time() + CACHE_TTL)

def log_chat(user_email, message, reply):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {user_email} → {message} | Neuraluxe-AI → {reply}")

def process_chat_message(user_email, message):
    """
    Premium-only chat handler.
    Determines whether message is a code command or normal chat,
    returns AI response, caches, logs, and records usage.
    """
    # Strip input
    message = message.strip()
    if not message:
        return "⚠️ Empty message. Please type something."

    # Premium check
    active, msg = check_premium(user_email)
    if not active:
        return "⚠️ Access denied: Premium users only."

    # Check cache first
    cached = get_cache(user_email, message)
    if cached:
        return cached

    try:
        # Determine if message is a code request
        if message.lower().startswith("/code "):
            reply = handle_chat_command(user_email, message)
        else:
            reply = ai_response(user_email, message)

        # Record chat for analytics
        record_chat(user_email)

        # Cache the response
        set_cache(user_email, message, reply)

        # Log message
        log_chat(user_email, message, reply)

        return reply

    except Exception as e:
        err_msg = f"⚠️ An error occurred while processing your message: {e}"
        print(err_msg)
        return err_msg

# -------------------------
# Standalone test
# -------------------------
if __name__ == "__main__":
    user_email = input("Enter your email: ").strip()
    print("Neuraluxe-AI Chat Initialized. Type 'exit' to quit.\n")

    while True:
        user_msg = input("You: ").strip()
        if user_msg.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        reply = process_chat_message(user_email, user_msg)
        print(f"\nNeuraluxe-AI:\n{reply}\n")