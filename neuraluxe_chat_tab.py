"""
Neuraluxe‑Lite Premium Chat Tab (Upgraded)
------------------------------------------
Features enhanced:
- Online LLM integration (via dummy API call)
- Session context memory (last n messages)
- Enforced free‑user reply cap per session
- Persistent chat history file storage
- Theme persistence & commands (/theme, /history, /help)
- Web‑search fallback for “unknown” content
"""

import json
import os
import time
from datetime import datetime
from random import choice
from session_manager import is_free_user
from translation_hub_full import translate_for_user, get_user_language, switch_language
from cache_manager import set_cache, get_cache
from logger import log_activity  
# assume logger writes also to file

USERS_JSON = "users.json"
CHAT_HISTORY_DIR = "chat_histories"
FREE_USER_EMAIL = "adedoyinolugbode57@gmail.com"
THEMES = ["default", "neon", "dark", "light", "blue", "green", "purple", "cyan", "magenta", "orange", "red", "yellow"]

# ensure chat history folder
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

REPLY_LIMIT_FREE = 3  # free user replies per session

def load_users():
    if not os.path.exists(USERS_JSON):
        with open(USERS_JSON, "w") as f:
            json.dump({}, f)
    with open(USERS_JSON, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_JSON, "w") as f:
        json.dump(data, f, indent=2)

def theme_selector(user_email):
    print("\nAvailable Themes:")
    for idx, t in enumerate(THEMES,1):
        print(f"{idx}. {t}")
    choice_idx = input("Select theme number (or press Enter to skip): ").strip()
    if choice_idx.isdigit() and 1 <= int(choice_idx) <= len(THEMES):
        theme = THEMES[int(choice_idx)-1]
        users = load_users()
        user_data = users.setdefault(user_email, {})
        user_data["theme"] = theme
        save_users(users)
        print(f"Theme applied: {theme}")
        return theme
    # fallback to stored or default
    users = load_users()
    user_data = users.get(user_email, {})
    return user_data.get("theme", "default")

def simulate_online_ai_reply(user_input, context, user_language):
    # placeholder for real online LLM call
    # we use simple logic plus web‐search fallback
    generic_replies = [
        "Interesting! Tell me more.",
        "I see. Can you elaborate?",
        "Hmm… that’s thought‑provoking.",
        "Absolutely! I agree.",
        "Could you explain that differently?"
    ]
    if len(user_input) < 20:
        return choice(generic_replies)
    if "weather" in user_input.lower():
        return f"In {user_language}: The weather is nice today near you."
    # fallback web‑search hint
    return f"I’m not sure—I found this for you: https://www.google.com/search?q={user_input.replace(' ', '+')}"

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

def chat_tab_ui(user_email):
    print("\n=== Neuraluxe‑Lite Chat Tab ===")
    users = load_users()
    user_data = users.setdefault(user_email, {})
    save_users(users)  # ensure user entry
    theme = user_data.get("theme", "default")
    print(f"Current theme: {theme}")
    new_theme = theme_selector(user_email)

    history = load_history(user_email)
    context = history["messages"][-5:]  # last 5 messages
    replies_count = 0

    log_activity(user_email, "Opened Chat Tab")

    print("Type '/help' for commands. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            log_activity(user_email, "Closed Chat Tab")
            save_history(user_email, history)
            print("Exiting Chat Tab…\n")
            break

        if user_input.startswith("/"):
            # command handling
            cmd = user_input.lower()
            if cmd == "/theme":
                theme = theme_selector(user_email)
                print(f"Theme changed to: {theme}")
            elif cmd == "/history":
                print("\n📁 Chat History:")
                for idx, m in enumerate(history["messages"][-10:],1):
                    print(f"{idx}. {m['sender']}: {m['text']}")
                print()
            elif cmd == "/help":
                print("Commands:\n /theme - change theme\n /history - show recent chats\n exit - quit chat\n")
            else:
                print("Unknown command. Type '/help' for assistance.")
            continue

        # free user limit enforcement
        if is_free_user(user_email) and replies_count >= REPLY_LIMIT_FREE:
            print("⚠️ Free user reply limit reached for this session. Upgrade for unlimited chats.\n")
            continue

        # translation on user message
        user_language = get_user_language(user_email)
        translated_input = translate_for_user(user_email, user_input)

        # AI reply
        ai_reply_raw = simulate_online_ai_reply(translated_input, context, user_language)
        ai_reply_translated = translate_for_user(user_email, ai_reply_raw)

        # log, update history
        log_activity(user_email, f"User said: {user_input} | AI replied: {ai_reply_translated}")
        history["messages"].append({"timestamp": datetime.now().strftime("%Y‑%m‑%d %H:%M:%S"),
                                    "sender": "user", "text": user_input})
        history["messages"].append({"timestamp": datetime.now().strftime("%Y‑%m‑%d %H:%M:%S"),
                                    "sender": "ai", "text": ai_reply_translated})
        save_history(user_email, history)

        # print reply
        print(f"Neuraluxe: {ai_reply_translated}\n")

        # update counters
        replies_count += 1
        context = history["messages"][-5:]  # refresh context window

    # end while

if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    chat_tab_ui(email)