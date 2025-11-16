"""
Neuraluxe-AI Premium Chat Tab
-----------------------------
- Full premium-only access
- Lightweight & modular
- Online augmentation for smart replies
"""

import json, os, time
from datetime import datetime
from random import choice, randint
from urllib.parse import quote_plus
import requests
from ai_engine import ai_response
from config import check_premium

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

# -----------------------------
# Chat Cache
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
# Chat Utilities
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

def display_mini_analytics(user_email, users_data):
    print("\n📊 Chat Tab Mini Analytics:")
    user_data = users_data.get(user_email, {})
    chats = len(user_data.get("chats", []))
    print(f"- Total Chats: {chats}")
    print(f"- Status: {'Premium' if check_premium(user_email)[0] else 'Inactive'}\n")

# -----------------------------
# Chat Tab Main UI
# -----------------------------
def chat_tab_ui(user_email):
    # Premium check before opening
    active, msg = check_premium(user_email)
    if not active:
        print("⚠️ Access denied: Premium users only.")
        return

    print("\n=== Neuraluxe-AI Chat Tab ===")
    users_data = load_users()
    log_activity(user_email, "Opened Chat Tab")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            log_activity(user_email, "Closed Chat Tab")
            print("Exiting Chat Tab...\n")
            break

        if not user_input:
            print("You typed nothing. Try again.\n")
            continue

        # Check cache first
        cached_reply = get_chat_cache(user_email, user_input)
        if cached_reply:
            reply = cached_reply
        else:
            online_reply = fetch_online_info(user_input)
            if online_reply:
                reply = online_reply
            else:
                reply = ai_response(user_email, user_input)
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