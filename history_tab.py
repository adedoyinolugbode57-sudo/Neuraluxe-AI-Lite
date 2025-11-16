"""
Neuraluxe-Lite
Premium History Tab
---------------------------------
Features:
- View past chats, games, and searches
- Free vs Paid access
- Search & filter history
- Delete or clear history
- Recent activity timestamps
- Quick tips
- Logging & timestamps
"""

import json
import os
from datetime import datetime

# -----------------------------
# Configurations
# -----------------------------
FREE_USER_EMAIL = "adedoyinolugbode57@gmail.com"
USERS_JSON = "users.json"
HISTORY_JSON = "history.json"

# -----------------------------
# Helper Functions
# -----------------------------
def load_history():
    if not os.path.exists(HISTORY_JSON):
        with open(HISTORY_JSON, "w") as f:
            json.dump({}, f)
    with open(HISTORY_JSON, "r") as f:
        return json.load(f)

def save_history(data):
    with open(HISTORY_JSON, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} - {user_email} - {action}")

def display_quick_tips():
    tips = [
        "History shows your past chats, games, and searches.",
        "Free users may have limited history visibility.",
        "Use search to find specific entries quickly.",
        "Clear history if you want to reset data.",
        "Recent activity shows last 5 entries.",
        "History is saved automatically after each action."
    ]
    print("\n✨ History Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

def view_recent_history(user_email, history_data):
    user_history = history_data.get(user_email, {})
    recent_entries = user_history.get("entries", [])
    print("\n📁 Recent History:")
    if not recent_entries:
        print("- No history found.")
    else:
        for idx, entry in enumerate(recent_entries[-5:], 1):
            print(f"{idx}. [{entry['timestamp']}] {entry['type']} - {entry['content']}")
    print()

def search_history(user_email, history_data):
    term = input("Enter search term: ").strip().lower()
    user_history = history_data.get(user_email, {})
    entries = user_history.get("entries", [])
    results = [e for e in entries if term in e['content'].lower()]
    print(f"\n🔍 Search Results for '{term}':")
    if not results:
        print("- No matching entries found.")
    else:
        for idx, entry in enumerate(results, 1):
            print(f"{idx}. [{entry['timestamp']}] {entry['type']} - {entry['content']}")
    print()

def clear_history(user_email, history_data):
    confirm = input("Are you sure you want to clear all history? (y/n): ").strip().lower()
    if confirm == "y":
        history_data[user_email] = {"entries": []}
        save_history(history_data)
        print("✅ History cleared.")
    else:
        print("Cancelled clearing history.")

def add_dummy_history(user_email, history_data):
    """Adds some dummy entries for testing"""
    user_data = history_data.setdefault(user_email, {})
    entries = user_data.setdefault("entries", [])
    for _ in range(2):
        entries.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Chat",
            "content": f"Dummy chat message {len(entries)+1}"
        })
        entries.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Game",
            "content": f"Dummy game {len(entries)+1}"
        })
        entries.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Search",
            "content": f"Dummy search {len(entries)+1}"
        })
    save_history(history_data)

# -----------------------------
# History Tab Main
# -----------------------------
def history_tab_ui(user_email):
    print("\n==============================")
    print("          HISTORY TAB         ")
    print("==============================\n")

    log_activity(user_email, "Opened History Tab")

    history_data = load_history()
    add_dummy_history(user_email, history_data)

    display_quick_tips()
    view_recent_history(user_email, history_data)

    while True:
        print("\nOptions:")
        print("1. View Recent History")
        print("2. Search History")
        print("3. Clear History")
        print("4. Exit History Tab")
        choice = input("Select option: ").strip()

        if choice == "1":
            view_recent_history(user_email, history_data)
        elif choice == "2":
            search_history(user_email, history_data)
        elif choice == "3":
            clear_history(user_email, history_data)
        elif choice == "4":
            log_activity(user_email, "Closed History Tab")
            print("Exiting History Tab...\n")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    history_tab_ui(email)