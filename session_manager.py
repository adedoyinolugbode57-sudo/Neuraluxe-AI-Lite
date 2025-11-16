"""
Neuraluxe-AI Session Manager (Optimized for 10k+ users)
--------------------------------------------------------
- Handles user sessions, free vs premium users
- Tracks login timestamps and activity
- Supports multi-login detection
- Lightweight & modular (per-user JSON)
"""

from config import FREE_USER_EMAIL
from datetime import datetime
import json, os

USER_DIR = "users"

# -------------------------
# Helper to Load / Save User
# -------------------------
def load_user(email):
    os.makedirs(USER_DIR, exist_ok=True)
    path = f"{USER_DIR}/{email}.json"
    if not os.path.exists(path):
        return {"email": email, "premium": email == FREE_USER_EMAIL, "sessions": [], "activities": [], "features": {}}
    with open(path, "r") as f:
        return json.load(f)

def save_user(user_data):
    path = f"{USER_DIR}/{user_data['email']}.json"
    with open(path, "w") as f:
        json.dump(user_data, f, indent=2)

# -------------------------
# User Status Checks
# -------------------------
def is_free_user(email):
    return email != FREE_USER_EMAIL

def is_premium_user(email):
    return email == FREE_USER_EMAIL

# -------------------------
# Session Tracking
# -------------------------
def update_login_timestamp(email):
    user = load_user(email)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user["last_login"] = now
    save_user(user)
    print(f"[SESSION] Updated last login for {email}: {now}")

def start_session(email):
    user = load_user(email)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_id = f"{email}-{now}"
    user["sessions"].append({"session_id": session_id, "start": now, "active": True})
    save_user(user)
    print(f"[SESSION] Started session: {session_id}")
    return session_id

def end_session(email, session_id):
    user = load_user(email)
    for s in user["sessions"]:
        if s["session_id"] == session_id:
            s["active"] = False
            s["end"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[SESSION] Ended session: {session_id}")
            break
    save_user(user)

# -------------------------
# Active Session Checks
# -------------------------
def get_active_sessions(email):
    user = load_user(email)
    return [s for s in user["sessions"] if s.get("active")]

def has_multiple_active_sessions(email):
    return len(get_active_sessions(email)) > 1

# -------------------------
# Premium Feature Logic
# -------------------------
def can_access_feature(email, feature_name):
    user = load_user(email)
    if user.get("premium"):
        return True
    features = user.setdefault("features", {})
    usage = features.get(feature_name, 0)
    if usage >= 2:
        print(f"[LIMIT] Free user reached max usage for {feature_name}")
        return False
    features[feature_name] = usage + 1
    save_user(user)
    return True

# -------------------------
# Activity Logging
# -------------------------
def log_activity(email, activity):
    user = load_user(email)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user.setdefault("activities", []).append({"activity": activity, "timestamp": timestamp})
    save_user(user)
    print(f"[ACTIVITY] {email} - {activity} at {timestamp}")

# -------------------------
# Utilities
# -------------------------
def get_last_login(email):
    user = load_user(email)
    return user.get("last_login")

def reset_user_features(email):
    user = load_user(email)
    user["features"] = {}
    save_user(user)
    print(f"[RESET] Reset feature usage for {email}")

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    test_email = input("Enter email for test: ").strip()
    update_login_timestamp(test_email)
    session = start_session(test_email)
    log_activity(test_email, "Test activity")
    print("Active sessions:", get_active_sessions(test_email))
    end_session(test_email, session)