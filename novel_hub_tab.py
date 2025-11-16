import json
import os
from datetime import datetime
from session_manager import FREE_USER_EMAIL, is_free_user

NOVELS_JSON = "novels.json"
ANALYTICS_JSON = "analytics.json"

# -----------------------------
# Helper Functions
# -----------------------------
def load_novels():
    if not os.path.exists(NOVELS_JSON):
        with open(NOVELS_JSON, "w") as f:
            json.dump({}, f)
    with open(NOVELS_JSON, "r") as f:
        return json.load(f)

def save_novels(data):
    with open(NOVELS_JSON, "w") as f:
        json.dump(data, f, indent=2)

def load_analytics():
    if not os.path.exists(ANALYTICS_JSON):
        with open(ANALYTICS_JSON, "w") as f:
            json.dump({}, f)
    with open(ANALYTICS_JSON, "r") as f:
        return json.load(f)

def save_analytics(data):
    with open(ANALYTICS_JSON, "w") as f:
        json.dump(data, f, indent=2)

def log_novel_action(user_email, action_type, novel_title):
    data = load_analytics()
    user = data.setdefault("users", {}).setdefault(user_email, {})
    user.setdefault("novels_read", 0)
    user.setdefault("novels_added", 0)
    user.setdefault("recent_novels", [])
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if action_type == "read":
        user["novels_read"] += 1
    elif action_type == "add":
        user["novels_added"] += 1
    
    user["recent_novels"].append({"title": novel_title, "timestamp": timestamp})
    if len(user["recent_novels"]) > 5:
        user["recent_novels"] = user["recent_novels"][-5:]
    
    save_analytics(data)

# -----------------------------
# Novel Hub Functions
# -----------------------------
def display_quick_tips():
    tips = [
        "Free users limited to 2 novel additions.",
        "Premium users can add and read unlimited novels.",
        "Recent novel activity is tracked automatically.",
        "Use search to find novels quickly.",
        "Recent activity shows last 5 novels accessed."
    ]
    print("\n✨ Novel Hub Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

def view_recent_novels(user_email, novels_data):
    user_novels = novels_data.get(user_email, [])
    print("\n📚 Your Recent Novels:")
    if not user_novels:
        print("- No novels accessed yet.")
    else:
        for idx, novel in enumerate(user_novels[-5:], 1):
            print(f"{idx}. {novel['title']} by {novel['author']} [{novel['timestamp']}]")
    print()

def read_novel(user_email, novels_data):
    user_novels = novels_data.get(user_email, [])
    if not user_novels:
        print("No novels to read.")
        return
    view_recent_novels(user_email, novels_data)
    idx = input("Enter novel number to read: ").strip()
    if idx.isdigit() and 1 <= int(idx) <= len(user_novels):
        novel = user_novels[int(idx)-1]
        print(f"\n--- Reading: {novel['title']} ---")
        print(novel['content'])
        print("\n--- End of Novel ---")
        log_novel_action(user_email, "read", novel['title'])
        print(f"✅ Logged reading activity for '{novel['title']}'")
    else:
        print("Invalid selection.")

def add_novel(user_email, novels_data):
    full_access = not is_free_user(user_email)
    user_novels = novels_data.setdefault(user_email, [])

    if not full_access and len(user_novels) >= 2:
        print("Free users can only add up to 2 novels. Upgrade for full access.")
        return

    title = input("Enter novel title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    author = input("Enter author name: ").strip() or "Unknown Author"
    content = input("Enter novel content (can paste long text): ").strip()
    if not content:
        print("Content cannot be empty.")
        return

    new_novel = {
        "title": title,
        "author": author,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    user_novels.append(new_novel)
    save_novels(novels_data)
    log_novel_action(user_email, "add", title)
    print(f"✅ Novel '{title}' added and logged successfully!")

def search_novels(user_email, novels_data):
    term = input("Enter search term: ").strip().lower()
    user_novels = novels_data.get(user_email, [])
    results = [n for n in user_novels if term in n['title'].lower() or term in n['author'].lower()]
    print(f"\n🔍 Search Results for '{term}':")
    if not results:
        print("- No matching novels found.")
    else:
        for idx, novel in enumerate(results, 1):
            print(f"{idx}. {novel['title']} by {novel['author']} [{novel['timestamp']}]")
    print()

# -----------------------------
# Novel Hub Tab UI
# -----------------------------
def novel_hub_tab_ui(user_email):
    print("\n==============================")
    print("         NOVEL HUB TAB        ")
    print("==============================\n")

    display_quick_tips()
    novels_data = load_novels()
    view_recent_novels(user_email, novels_data)

    while True:
        print("\nOptions:")
        print("1. View Recent Novels")
        print("2. Read Novel")
        print("3. Add New Novel")
        print("4. Search Novels")
        print("5. Exit Novel Hub Tab")
        choice = input("Select option: ").strip()

        if choice == "1":
            view_recent_novels(user_email, novels_data)
        elif choice == "2":
            read_novel(user_email, novels_data)
        elif choice == "3":
            add_novel(user_email, novels_data)
        elif choice == "4":
            search_novels(user_email, novels_data)
        elif choice == "5":
            print("Exiting Novel Hub Tab...\n")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    novel_hub_tab_ui(email)