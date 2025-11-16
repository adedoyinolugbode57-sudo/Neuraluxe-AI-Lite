# optimized_users.py
# -------------------
# Neuraluxe-AI Lightweight User Manager
# Lifetime premium & unlimited chats, lightweight JSON-based storage

import json
import os
from datetime import datetime

USERS_JSON = "users.json"
FREE_USER_EMAIL = "adedoyinolugbode57@gmail.com"
CHAT_HISTORY_LIMIT = 100  # store last 100 chats per user
DAILY_USAGE_LIMIT_DAYS = 90  # keep last 90 days of daily usage

# -----------------------------
# Load / Save Users
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

# -----------------------------
# User Initialization
# -----------------------------
def init_user(email):
    users = load_users()
    if email not in users:
        users[email] = {
            "profile": {
                "is_full_access": True,  # lifetime premium
                "theme": "default",
                "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "analytics": {
                "total_chats": 0,
                "daily_usage": {}
            },
            "chats": [],
            "novels_accessed": []
        }
        save_users(users)
    return users[email]

# -----------------------------
# Update Profile
# -----------------------------
def update_theme(email, theme):
    users = load_users()
    users[email]["profile"]["theme"] = theme
    save_users(users)

def update_last_login(email):
    users = load_users()
    users[email]["profile"]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_users(users)

# -----------------------------
# Chat Handling
# -----------------------------
def add_chat(email, message, reply=None):
    users = load_users()
    user_data = users[email]

    # Append chat
    chats = user_data.setdefault("chats", [])
    chats.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
        "reply_cached": reply
    })

    # Limit chat history
    if len(chats) > CHAT_HISTORY_LIMIT:
        user_data["chats"] = chats[-CHAT_HISTORY_LIMIT:]

    # Update analytics
    user_data["analytics"]["total_chats"] += 1
    today = datetime.now().strftime("%Y-%m-%d")
    daily = user_data["analytics"].setdefault("daily_usage", {})
    daily[today] = daily.get(today, 0) + 1

    # Keep only last 90 days
    if len(daily) > DAILY_USAGE_LIMIT_DAYS:
        oldest_days = sorted(daily.keys())[:-DAILY_USAGE_LIMIT_DAYS]
        for d in oldest_days:
            del daily[d]

    save_users(users)

# -----------------------------
# Novel Hub
# -----------------------------
def add_novel_access(email, novel_id):
    users = load_users()
    user_data = users[email]
    novels = user_data.setdefault("novels_accessed", [])
    novels.append({
        "novel_id": novel_id,
        "last_read": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_users(users)

# -----------------------------
# Analytics
# -----------------------------
def get_mini_analytics(email):
    users = load_users()
    user_data = users[email]
    return {
        "total_chats": user_data["analytics"]["total_chats"],
        "daily_usage": user_data["analytics"]["daily_usage"],
        "status": "Lifetime Premium"
    }

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter user email: ").strip()
    init_user(email)
    add_chat(email, "Hello AI!", "Hi there! 😊")
    add_novel_access(email, "novel_001")
    update_theme(email, "neon")
    update_last_login(email)
    analytics = get_mini_analytics(email)
    print(f"\n📊 Mini Analytics for {email}:")
    print(analytics)