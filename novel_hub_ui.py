"""
Neuraluxe-AI Novel Hub Tab (Final)
-----------------------------------
- Browse, read, and save novels
- Lightweight, premium-rich
- Full access for adedoyinolugbode57@gmail.com
- Recent activity, search, highlights included
"""

import json
from datetime import datetime
from novel_logic import list_novels, read_novel, add_novel
from session_manager import FREE_USER_EMAIL, is_free_user

NOVELS_FILE = "novels.json"

# -------------------------
# Helper Functions
# -------------------------
def load_novels():
    try:
        with open(NOVELS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_novels(data):
    with open(NOVELS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users_data = load_novels()
    user_logs = users_data.setdefault(user_email, {}).setdefault("activity", [])
    user_logs.append({"action": action, "timestamp": timestamp})
    save_novels(users_data)
    print(f"[LOG] {timestamp} - {user_email} - {action}")

def view_recent_activity(user_email, novels_data):
    print("\n📜 Recent Activity:")
    activities = novels_data.get(user_email, {}).get("activity", [])
    if not activities:
        print("- No recent activity.")
        return
    for act in activities[-5:]:
        print(f"- {act['timestamp']}: {act['action']}")

def search_novels(user_email, novels_data):
    term = input("Enter search term (title/author): ").strip().lower()
    all_novels = novels_data.get(user_email, {}).get("novels", {})
    results = {title: content for title, content in all_novels.items() if term in title.lower() or term in content.lower()}
    print(f"\n🔍 Search Results for '{term}':")
    if not results:
        print("- No matches found.")
        return
    for idx, (title, content) in enumerate(results.items(), 1):
        print(f"{idx}. {title} - {len(content)} characters")

def add_highlight(user_email, novels_data):
    all_novels = novels_data.get(user_email, {}).get("novels", {})
    if not all_novels:
        print("No novels to highlight.")
        return
    titles = list(all_novels.keys())
    for idx, title in enumerate(titles, 1):
        print(f"{idx}. {title}")
    try:
        choice = int(input("Select novel number to add highlight: ").strip())
        novel_title = titles[choice - 1]
    except:
        print("Invalid selection.")
        return
    highlight = input("Enter your highlight or note: ").strip()
    if not highlight:
        print("Highlight cannot be empty.")
        return
    novel_data = novels_data[user_email].setdefault("highlights", {}).setdefault(novel_title, [])
    novel_data.append({"highlight": highlight, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    save_novels(novels_data)
    print(f"✅ Highlight added to '{novel_title}'")
    log_activity(user_email, f"Added highlight to '{novel_title}'")

def read_with_highlights(user_email, full_access_user, novels_data):
    all_novels = novels_data.get(user_email, {}).get("novels", {})
    if not all_novels:
        print("No novels to read.")
        return

    titles = list(all_novels.keys())
    for idx, title in enumerate(titles, 1):
        print(f"{idx}. {title}")
    try:
        choice = int(input("Select novel number to read: ").strip())
        novel_title = titles[choice - 1]
    except:
        print("Invalid selection.")
        return

    content = all_novels[novel_title]
    if is_free_user(user_email) and not full_access_user:
        print("\nLimited preview for free users (first 200 chars):")
        print(content[:200] + "...")
    else:
        print(f"\n--- Reading '{novel_title}' ---")
        print(content)

        # Show highlights
        highlights = novels_data[user_email].get("highlights", {}).get(novel_title, [])
        if highlights:
            print("\n💡 Your Highlights / Notes:")
            for h in highlights[-5:]:
                print(f"- [{h['timestamp']}] {h['highlight']}")

    log_activity(user_email, f"Read novel '{novel_title}'")

# -------------------------
# Novel Hub UI
# -------------------------
def novel_hub_ui(user_email):
    full_access_user = (user_email == FREE_USER_EMAIL or not is_free_user(user_email))
    novels_data = load_novels()
    novels_data.setdefault(user_email, {}).setdefault("novels", {})

    while True:
        print("\n--- Neuraluxe Novel Hub ---")
        print("1. Browse Novels")
        print("2. Read Novel")
        print("3. Add New Novel")
        print("4. Search Novels")
        print("5. View Recent Activity")
        print("6. Add Highlight / Note")
        print("7. Exit Novel Hub")

        choice = input("Select option: ").strip()

        if choice == "1":
            list_novels(user_email, full_access_user)
        elif choice == "2":
            read_with_highlights(user_email, full_access_user, novels_data)
        elif choice == "3":
            add_novel(user_email, full_access_user)
            log_activity(user_email, "Added a new novel")
        elif choice == "4":
            search_novels(user_email, novels_data)
        elif choice == "5":
            view_recent_activity(user_email, novels_data)
        elif choice == "6":
            add_highlight(user_email, novels_data)
        elif choice == "7":
            print("Exiting Novel Hub...")
            break
        else:
            print("Invalid choice. Try again.")

    save_novels(novels_data)

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    novel_hub_ui(email)