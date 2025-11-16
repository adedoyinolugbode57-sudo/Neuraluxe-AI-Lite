"""
Neuraluxe-Lite
Premium Chat Tab with Online Info
---------------------------------
- Themed interface
- Free vs Paid access
- AI reply simulation with online augmentation
- Recent chat history
- Logging & timestamps
- Mini analytics display
- Quick tips in-chat
- Lightweight & modular
"""

import json, os, time
from datetime import datetime
from random import choice, randint
from urllib.parse import quote_plus
import requests

# -----------------------------
# Configurations
# -----------------------------
THEMES = ["default", "neon", "dark", "light", "blue", "green", "purple", "cyan", "magenta", "orange", "red", "yellow"]
FREE_USER_EMAIL = "adedoyinolugbode57@gmail.com"
USERS_JSON = "users.json"

# -----------------------------
# Helper Functions
# -----------------------------
def load_users():
    if not os.path.exists(USERS_JSON):
        with open(USERS_JSON, "w") as f:
            json.dump({}, f)
    with open(USERS_JSON, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_JSON, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} - {user_email} - {action}")

def theme_selector():
    print("\nAvailable Themes:")
    for idx, t in enumerate(THEMES, 1):
        print(f"{idx}. {t}")
    choice_idx = input("Select theme number (or press Enter to skip): ").strip()
    if choice_idx.isdigit() and 1 <= int(choice_idx) <= len(THEMES):
        theme = THEMES[int(choice_idx)-1]
        print(f"Theme applied: {theme}")
        return theme
    print("Default theme applied.")
    return "default"

# -----------------------------
# Online Info Fetcher
# -----------------------------
def fetch_wiki_summary(query, sentences=2):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}"
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("extract", "No summary found.")[:500]
    except:
        return "Could not fetch online info."
    return "No data available."

def fetch_quote(topic="inspire"):
    try:
        url = f"https://api.quotable.io/random?tags={quote_plus(topic)}"
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            return f'"{data["content"]}" — {data["author"]}'
    except:
        return "No quote available."

def fetch_online_info(message):
    message_lower = message.lower()
    if any(word in message_lower for word in ["what", "who", "when", "where", "how"]):
        return fetch_wiki_summary(message)
    elif any(word in message_lower for word in ["motivate", "inspire", "quote", "advice"]):
        return fetch_quote()
    return None

# -----------------------------
# Chat Cache (Lightweight)
# -----------------------------
CHAT_CACHE = {}

def get_chat_cache(user_email, message):
    key = f"{user_email}:{message}"
    entry = CHAT_CACHE.get(key)
    if entry and entry["expire_at"] > time.time():
        return entry["reply"]
    elif entry:
        del CHAT_CACHE[key]
    return None

def set_chat_cache(user_email, message, reply, ttl=3600):
    key = f"{user_email}:{message}"
    CHAT_CACHE[key] = {"reply": reply, "expire_at": time.time() + ttl}

# -----------------------------
# AI Reply Simulation
# -----------------------------
def simulate_ai_reply(user_input):
    generic_replies = [
        "Interesting! Tell me more.",
        "I see. Can you elaborate?",
        "Hmm… that's thought-provoking.",
        "Absolutely! I agree.",
        "Could you explain that differently?",
        "Fascinating, thanks for sharing!",
        "I'm listening… continue.",
        "That’s great insight!",
        "I didn’t expect that.",
        "Wow! Let's explore this further."
    ]
    if len(user_input) % 2 == 0:
        return choice(generic_replies)
    else:
        return f"You said: {user_input}"

# -----------------------------
# Chat Tab Utilities
# -----------------------------
def display_recent_chats(user_email, users_data):
    print("\n📁 Recent Chats:")
    user_data = users_data.get(user_email, {})
    chats = user_data.get("chats", [])
    if not chats:
        print("- No recent chats found.")
    else:
        for idx, c in enumerate(chats[-5:], 1):
            print(f"{idx}. {c}")
    print()

def add_dummy_chats(user_email, users_data):
    user_data = users_data.setdefault(user_email, {})
    chats = user_data.setdefault("chats", [])
    for _ in range(randint(1,3)):
        chats.append(f"Chat message {randint(100,999)}")
    save_users(users_data)

def display_mini_analytics(user_email, users_data):
    print("\n📊 Chat Tab Mini Analytics:")
    user_data = users_data.get(user_email, {})
    chats = len(user_data.get("chats", []))
    print(f"- Total Chats: {chats}")
    print(f"- Status: {'Free' if user_email != FREE_USER_EMAIL else 'Full Access'}\n")

def display_quick_tips():
    tips = [
        "Keep your messages clear.",
        "Use /help for quick commands.",
        "Switch themes to reduce eye strain.",
        "Check mini analytics often.",
        "Free users may have reply limits.",
        "Explore AI suggestions for inspiration.",
        "Save important chats for reference."
    ]
    print("\n✨ Quick Chat Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

# -----------------------------
# Main Chat Tab UI
# -----------------------------
def chat_tab_ui(user_email):
    print("\n==============================")
    print("          CHAT  TAB           ")
    print("==============================\n")

    users_data = load_users()
    add_dummy_chats(user_email, users_data)
    log_activity(user_email, "Opened Chat Tab")

    theme = theme_selector()
    display_quick_tips()
    display_recent_chats(user_email, users_data)
    display_mini_analytics(user_email, users_data)

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            log_activity(user_email, "Closed Chat Tab")
            print("Exiting Chat Tab...\n")
            break

        if not user_input:
            print("You typed nothing. Try again.\n")
            continue

        if user_email != FREE_USER_EMAIL:
            print("⚠️ Free users have limited replies per session.\n")

        # Check cache first
        cached_reply = get_chat_cache(user_email, user_input)
        if cached_reply:
            reply = cached_reply
        else:
            # Online info augmentation
            online_reply = fetch_online_info(user_input)
            if online_reply:
                reply = online_reply
            else:
                reply = simulate_ai_reply(user_input)
            set_chat_cache(user_email, user_input, reply)

        print(f"Neuraluxe: {reply}\n")

        # Log chat
        user_data = users_data.setdefault(user_email, {})
        chats = user_data.setdefault("chats", [])
        chats.append(user_input)
        save_users(users_data)

        display_mini_analytics(user_email, users_data)

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    chat_tab_ui(email)