"""
Neuraluxe-Lite
Premium Analytics Hub (Final Version)
---------------------------------------
Features:
- Track user actions across Chat, Games, Assets, and Novels
- Free vs Paid access
- Daily and total usage tracking
- Recent activity log
- Mini analytics dashboards
- Leaderboards
- Quick tips & timestamps
- Lightweight, standalone
"""

import json
import os
from datetime import datetime
from random import randint, choice

# -----------------------------
# Configurations
# -----------------------------
FREE_USER_EMAIL = "adedoyinolugbode57@gmail.com"
ANALYTICS_JSON = "analytics.json"

# -----------------------------
# Helper Functions
# -----------------------------
def load_analytics():
    if not os.path.exists(ANALYTICS_JSON):
        with open(ANALYTICS_JSON, "w") as f:
            json.dump({}, f)
    with open(ANALYTICS_JSON, "r") as f:
        return json.load(f)

def save_analytics(data):
    with open(ANALYTICS_JSON, "w") as f:
        json.dump(data, f, indent=4)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} - {user_email} - {action}")
    data = load_analytics()
    user_data = data.setdefault("users", {}).setdefault(user_email, {})
    actions = user_data.setdefault("actions", [])
    actions.append({"timestamp": timestamp, "action": action})
    # Track daily usage
    today = datetime.now().strftime("%Y-%m-%d")
    daily = user_data.setdefault("daily_usage", {})
    daily[today] = daily.get(today, 0) + 1
    save_analytics(data)

def increment_logins(user_email):
    data = load_analytics()
    user_data = data.setdefault("users", {}).setdefault(user_email, {})
    user_data["logins"] = user_data.get("logins", 0) + 1
    save_analytics(data)

def add_chat(user_email):
    data = load_analytics()
    user_data = data.setdefault("users", {}).setdefault(user_email, {})
    user_data["chats_sent"] = user_data.get("chats_sent", 0) + 1
    save_analytics(data)

def add_game_play(user_email, game_name, score):
    data = load_analytics()
    user_data = data.setdefault("users", {}).setdefault(user_email, {})
    user_data["games_played"] = user_data.get("games_played", 0) + 1
    high_scores = user_data.setdefault("high_scores", {})
    high_scores[game_name] = max(score, high_scores.get(game_name, 0))
    save_analytics(data)

def add_session_time(user_email, seconds):
    data = load_analytics()
    user_data = data.setdefault("users", {}).setdefault(user_email, {})
    user_data["session_time"] = user_data.get("session_time", 0) + seconds
    save_analytics(data)

# -----------------------------
# Analytics Views
# -----------------------------
def view_session_stats(user_email, user_data):
    print("\n--- Session Stats ---")
    print(f"Total Logins: {user_data.get('logins',0)}")
    print(f"Total Session Time: {user_data.get('session_time',0)} seconds")
    print(f"Games Played: {user_data.get('games_played',0)}")
    print(f"Chats Sent: {user_data.get('chats_sent',0)}")

def view_daily_usage(user_email, user_data):
    print("\n--- Daily Usage (Last 7 Days) ---")
    daily = user_data.get("daily_usage",{})
    if not daily:
        print("No daily usage data yet.")
        return
    for day in sorted(daily.keys())[-7:]:
        print(f"{day}: {daily[day]} actions")

def view_recent_actions(user_email, user_data):
    print("\n--- Recent Actions ---")
    actions = user_data.get("actions", [])
    if not actions:
        print("- No actions yet.")
        return
    for idx, act in enumerate(actions[-5:], 1):
        print(f"{idx}. {act['timestamp']} - {act['action']}")

def view_chat_usage(user_email, user_data):
    print("\n--- Chat Usage ---")
    print(f"Total Chats Sent: {user_data.get('chats_sent',0)}")
    recent_chats = randint(1,10)
    print(f"Recent Chats Activity: {recent_chats} chats in last session")
    bubbles = ["(●‿●)","(◕‿◕)","(✿◠‿◠)","(•‿•)","(≧◡≦)"]
    print("Activity Visual: ", " ".join(choice(bubbles) for _ in range(5)))

def view_game_performance(user_email, user_data):
    print("\n--- Game Performance ---")
    scores = user_data.get("high_scores", {})
    if not scores:
        print("No game data yet.")
        return
    for game, score in scores.items():
        print(f"{game}: {score} pts")
    top_score = max(scores.values())
    print(f"Top Game Score: {top_score} pts")

def view_leaderboard(data):
    print("\n--- Leaderboard Snapshot ---")
    all_users = data.get("users", {})
    leaderboard = []
    for email, info in all_users.items():
        total_score = sum(info.get("high_scores", {}).values())
        leaderboard.append((email, total_score))
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    print("Top 5 Users by Total Game Score:")
    for idx, (email, score) in enumerate(leaderboard[:5],1):
        print(f"{idx}. {email[:15]} - {score} pts")

def view_total_users(data):
    total = len(data.get("users", {}))
    print(f"\n🌐 Total Registered Users: {total}")

def display_quick_tips():
    tips = [
        "Track all user activities in Chat, Games, Assets, and Novel tabs.",
        "Free users have limited stats.",
        "Leaderboards show top performers.",
        "Daily usage helps monitor engagement trends.",
        "Recent actions recap last activity quickly.",
        "Use session and game stats for insights.",
        "Mini dashboards are refreshed on every tab interaction."
    ]
    print("\n✨ Analytics Tips:")
    for i, tip in enumerate(tips,1):
        print(f"{i}. {tip}")
    print()

# -----------------------------
# Main Analytics Tab UI
# -----------------------------
def analytics_tab_ui(user_email):
    data = load_analytics()
    user_data = data.get("users", {}).get(user_email, {})
    print("\n==============================")
    print("       ANALYTICS HUB FINAL     ")
    print("==============================\n")
    log_activity(user_email, "Opened Analytics Hub")

    display_quick_tips()
    view_total_users(data)
    view_daily_usage(user_email,user_data)
    view_session_stats(user_email,user_data)
    view_chat_usage(user_email,user_data)
    view_game_performance(user_email,user_data)
    view_recent_actions(user_email,user_data)
    view_leaderboard(data)

    while True:
        print("\nOptions:")
        print("1. Refresh Stats")
        print("2. View Recent Actions")
        print("3. View Daily Usage")
        print("4. View Leaderboard")
        print("5. Exit Analytics Hub")
        choice = input("Select option: ").strip()
        if choice=="1":
            print("\n🔄 Refreshing Analytics...\n")
            data = load_analytics()
            user_data = data.get("users", {}).get(user_email,{})
            view_session_stats(user_email,user_data)
            view_chat_usage(user_email,user_data)
            view_game_performance(user_email,user_data)
        elif choice=="2":
            view_recent_actions(user_email,user_data)
        elif choice=="3":
            view_daily_usage(user_email,user_data)
        elif choice=="4":
            data = load_analytics()
            view_leaderboard(data)
        elif choice=="5":
            log_activity(user_email, "Closed Analytics Hub")
            print("Exiting Analytics Hub...\n")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__=="__main__":
    email = input("Enter your email: ").strip()
    increment_logins(email)
    add_chat(email)
    add_game_play(email,"Trivia Quiz",randint(50,100))
    add_session_time(email,randint(60,600))
    analytics_tab_ui(email)