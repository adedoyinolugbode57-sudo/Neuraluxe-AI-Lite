"""
analytics_tracker.py
--------------------
Neuraluxe-AI Mini Analytics Tracker
- Lightweight, independent module
- Tracks user activity, sessions, feature usage
- Can be used for Home tab or chat tab analytics
"""

import json
import os
from datetime import datetime

USERS_JSON = "users.json"

# -------------------------
# Load & Save Users
# -------------------------
def load_users():
    if not os.path.exists(USERS_JSON):
        with open(USERS_JSON, "w") as f:
            json.dump({}, f)
    with open(USERS_JSON, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_JSON, "w") as f:
        json.dump(users, f, indent=2)

# -------------------------
# Track feature usage
# -------------------------
def log_feature_usage(email, feature_name):
    users = load_users()
    user = users.setdefault(email, {})
    features = user.setdefault("features", {})
    features[feature_name] = features.get(feature_name, 0) + 1
    save_users(users)
    print(f"[ANALYTICS] {email} used {feature_name}: {features[feature_name]} times")

# -------------------------
# Track chat sessions
# -------------------------
def log_chat_session(email, session_id):
    users = load_users()
    user = users.setdefault(email, {})
    sessions = user.setdefault("sessions", [])
    sessions.append({
        "session_id": session_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_users(users)
    print(f"[ANALYTICS] Logged chat session: {session_id} for {email}")

# -------------------------
# Retrieve mini analytics
# -------------------------
def get_mini_analytics(email):
    users = load_users()
    user = users.get(email, {})
    sessions = user.get("sessions", [])
    features = user.get("features", {})
    analytics = {
        "total_chats": len(sessions),
        "feature_usage": features
    }
    return analytics

# -------------------------
# Display Mini Analytics
# -------------------------
def display_analytics(email):
    analytics = get_mini_analytics(email)
    print(f"\n📊 Mini Analytics for {email}:")
    print(f"- Total Chats: {analytics['total_chats']}")
    if analytics['feature_usage']:
        print("- Feature Usage:")
        for feat, count in analytics['feature_usage'].items():
            print(f"  • {feat}: {count}")
    else:
        print("- Feature Usage: None yet")
    print()

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    test_email = input("Enter email for analytics test: ").strip()
    while True:
        print("\nOptions: 1. Log Feature  2. Log Chat Session  3. Show Analytics  4. Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            feat = input("Enter feature name: ").strip()
            log_feature_usage(test_email, feat)
        elif choice == "2":
            sess = input("Enter session ID: ").strip()
            log_chat_session(test_email, sess)
        elif choice == "3":
            display_analytics(test_email)
        elif choice == "4":
            print("Exiting analytics tracker...")
            break
        else:
            print("Invalid option.")