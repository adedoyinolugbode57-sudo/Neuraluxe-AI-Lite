"""
Neuraluxe-Lite
Premium Web Search Tab
---------------------------------
Features:
- Lightweight simulated web search
- Free vs Paid access
- Recent searches
- Mini analytics
- Themed interface
- Quick tips
- Logging & timestamps
"""

import json
import os
from datetime import datetime
from random import choice, randint

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

def simulate_web_search(query):
    """Lightweight simulated search results"""
    base_sites = ["https://github.com", "https://stackoverflow.com", "https://wikipedia.org", 
                  "https://news.ycombinator.com", "https://reddit.com", "https://medium.com"]
    results = [f"{choice(base_sites)}/search?q={query.replace(' ','+')}" for _ in range(randint(3,6))]
    return results

def display_recent_searches(user_email, users_data):
    print("\n📁 Recent Searches:")
    user_data = users_data.get(user_email, {})
    searches = user_data.get("recent_searches", [])
    if not searches:
        print("- No recent searches found.")
    else:
        for idx, s in enumerate(searches[-5:], 1):
            print(f"{idx}. {s}")
    print()

def add_dummy_searches(user_email, users_data):
    user_data = users_data.setdefault(user_email, {})
    searches = user_data.setdefault("recent_searches", [])
    for _ in range(randint(1,3)):
        searches.append(f"Example search {randint(100,999)}")
    save_users(users_data)

def display_mini_analytics(user_email, users_data):
    print("\n📊 Web Search Mini Analytics:")
    user_data = users_data.get(user_email, {})
    searches = len(user_data.get("recent_searches", []))
    print(f"- Total Searches: {searches}")
    print(f"- Status: {'Free' if user_email != FREE_USER_EMAIL else 'Full Access'}\n")

def display_quick_tips():
    tips = [
        "Keep your queries short and clear.",
        "Free users have limited searches per session.",
        "Switch themes for comfort.",
        "Check mini analytics to track your searches.",
        "Use simulated search links for inspiration.",
        "Combine with Chat Tab for AI-assisted search.",
        "Recent searches are saved automatically."
    ]
    print("\n✨ Web Search Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

# -----------------------------
# Web Search Tab Main
# -----------------------------
def web_search_tab_ui(user_email):
    print("\n==============================")
    print("        WEB SEARCH TAB        ")
    print("==============================\n")

    users_data = load_users()
    add_dummy_searches(user_email, users_data)

    log_activity(user_email, "Opened Web Search Tab")

    theme = theme_selector()
    display_quick_tips()
    display_recent_searches(user_email, users_data)
    display_mini_analytics(user_email, users_data)

    while True:
        query = input("Enter search query (or type 'exit' to leave): ").strip()

        if query.lower() == "exit":
            log_activity(user_email, "Closed Web Search Tab")
            print("Exiting Web Search Tab...\n")
            break

        if not query:
            print("You typed nothing. Try again.\n")
            continue

        # Free vs Paid limitation
        if user_email != FREE_USER_EMAIL:
            print("⚠️ Free users have limited searches per session.\n")

        # Simulate search
        results = simulate_web_search(query)
        print("\n🔎 Search Results:")
        for idx, res in enumerate(results, 1):
            print(f"{idx}. {res}")
        print()

        # Log search
        user_data = users_data.setdefault(user_email, {})
        searches = user_data.setdefault("recent_searches", [])
        searches.append(query)
        save_users(users_data)

        display_mini_analytics(user_email, users_data)

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    web_search_tab_ui(email)