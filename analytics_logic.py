"""
Neuraluxe-AI Analytics Logic
----------------------------
- Tracks user activity, usage stats, and tab interactions
- Lightweight JSON-based storage
- Full access for free user adedoyinolugbode57@gmail.com
"""

import json, os, time
from session_manager import is_free_user

ANALYTICS_FILE = "analytics.json"

# -------------------------
# Load & Save
# -------------------------
def load_analytics():
    if not os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, "w") as f:
            json.dump({}, f)
    with open(ANALYTICS_FILE, "r") as f:
        return json.load(f)

def save_analytics(data):
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -------------------------
# User Activity
# -------------------------
def log_user_action(user_email, action):
    data = load_analytics()
    if user_email not in data:
        data[user_email] = []
    data[user_email].append({"action": action, "timestamp": time.time()})
    save_analytics(data)
    print(f"[ANALYTICS] {user_email} performed '{action}'")

def get_user_actions(user_email, limit=10):
    data = load_analytics()
    actions = data.get(user_email, [])
    return actions[-limit:]

# -------------------------
# Tab Analytics
# -------------------------
def log_tab_view(user_email, tab_name):
    log_user_action(user_email, f"Viewed Tab: {tab_name}")

def most_visited_tabs(user_email, top_n=5):
    data = load_analytics()
    actions = data.get(user_email, [])
    tab_count = {}
    for act in actions:
        if "Viewed Tab" in act["action"]:
            tab = act["action"].split(": ")[1]
            tab_count[tab] = tab_count.get(tab, 0) + 1
    return sorted(tab_count.items(), key=lambda x: x[1], reverse=True)[:top_n]

# -------------------------
# Usage Summary
# -------------------------
def get_usage_summary(user_email):
    actions = get_user_actions(user_email, limit=100)
    total_actions = len(actions)
    tabs = [a["action"].split(": ")[1] for a in actions if "Viewed Tab" in a["action"]]
    unique_tabs = set(tabs)
    return {
        "total_actions": total_actions,
        "unique_tabs": list(unique_tabs),
        "top_tabs": most_visited_tabs(user_email)
    }

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter email: ").strip()
    log_tab_view(email, "Mini-Games")
    log_tab_view(email, "New Chat")
    log_tab_view(email, "Mini-Games")
    print("Recent Actions:", get_user_actions(email))
    print("Top Tabs:", most_visited_tabs(email))
    print("Usage Summary:", get_usage_summary(email))