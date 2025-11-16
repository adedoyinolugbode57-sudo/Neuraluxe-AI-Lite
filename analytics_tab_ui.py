"""
Neuraluxe-AI Analytics Tab
--------------------------
- Lightweight, premium-rich
- Tracks user activities, game scores, chat stats
- Full access for adedoyinolugbode57@gmail.com
- Modular and deployable
"""

import json, random, time
from helpers import truncate_text
from session_manager import FREE_USER_EMAIL, is_free_user

# -------------------------
# File Storage
# -------------------------
ANALYTICS_FILE = "analytics.json"

# -------------------------
# Load / Save Analytics
# -------------------------
def load_analytics():
    try:
        with open(ANALYTICS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_analytics(data):
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# Sample Analytics Data Structure
# -------------------------
"""
analytics.json structure:
{
    "users": {
        "user_email": {
            "logins": 10,
            "chats_sent": 50,
            "games_played": 20,
            "high_scores": {
                "Number Guess": 100,
                "Trivia Quiz": 80
            },
            "session_time": 3600
        }
    }
}
"""

# -------------------------
# Analytics UI
# -------------------------
def analytics_tab_ui(user_email):
    full_access_user = (user_email == FREE_USER_EMAIL)
    data = load_analytics()
    if user_email not in data.get("users", {}):
        if "users" not in data:
            data["users"] = {}
        data["users"][user_email] = {
            "logins": 0,
            "chats_sent": 0,
            "games_played": 0,
            "high_scores": {},
            "session_time": 0
        }

    user_data = data["users"][user_email]

    while True:
        print("\n--- Analytics Tab ---")
        print("1. View Session Stats")
        print("2. View Chat Usage")
        print("3. View Game Performance")
        print("4. Leaderboard Snapshot")
        print("5. Exit Analytics")
        choice = input("Select option: ").strip()

        if choice == "1":
            view_session_stats(user_email, user_data)
        elif choice == "2":
            view_chat_usage(user_email, user_data)
        elif choice == "3":
            view_game_performance(user_email, user_data)
        elif choice == "4":
            view_leaderboard(data)
        elif choice == "5":
            print("Exiting Analytics Tab...")
            save_analytics(data)
            break
        else:
            print("Invalid choice. Try again.")

# -------------------------
# Session Stats
# -------------------------
def view_session_stats(user_email, user_data):
    print("\n--- Session Stats ---")
    print(f"Total Logins: {user_data['logins']}")
    print(f"Total Session Time: {user_data['session_time']} seconds")
    print(f"Games Played: {user_data['games_played']}")
    print(f"Chats Sent: {user_data['chats_sent']}")

# -------------------------
# Chat Usage Stats
# -------------------------
def view_chat_usage(user_email, user_data):
    print("\n--- Chat Usage ---")
    print(f"Chats Sent: {user_data['chats_sent']}")
    recent_chats = random.randint(1, 10)
    print(f"Recent Chats Activity: {recent_chats} chats in last session")
    # Decorative bubble for activity
    bubbles = ["(●‿●)", "(◕‿◕)", "(✿◠‿◠)", "(•‿•)", "(≧◡≦)"]
    print("Activity Visual: ", " ".join(random.choices(bubbles, k=5)))

# -------------------------
# Game Performance Stats
# -------------------------
def view_game_performance(user_email, user_data):
    print("\n--- Game Performance ---")
    scores = user_data.get("high_scores", {})
    if not scores:
        print("No game data available yet.")
        return
    for game, score in scores.items():
        print(f"{game}: {score} pts")
    top_score = max(scores.values())
    print(f"Top Game Score: {top_score} pts")

# -------------------------
# Leaderboard Snapshot
# -------------------------
def view_leaderboard(data):
    print("\n--- Leaderboard Snapshot ---")
    all_users = data.get("users", {})
    leaderboard = []
    for email, info in all_users.items():
        total_score = sum(info.get("high_scores", {}).values())
        leaderboard.append((email, total_score))
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    print("Top 5 Users by Total Game Score:")
    for idx, (email, score) in enumerate(leaderboard[:5], 1):
        print(f"{idx}. {truncate_text(email, 15)} - {score} pts")

# -------------------------
# Update Analytics Helpers
# -------------------------
def increment_logins(user_email):
    data = load_analytics()
    if user_email not in data.get("users", {}):
        if "users" not in data:
            data["users"] = {}
        data["users"][user_email] = {
            "logins": 0,
            "chats_sent": 0,
            "games_played": 0,
            "high_scores": {},
            "session_time": 0
        }
    data["users"][user_email]["logins"] += 1
    save_analytics(data)

def add_game_play(user_email, game_name, score):
    data = load_analytics()
    user = data["users"].get(user_email)
    if not user:
        user = {
            "logins": 0,
            "chats_sent": 0,
            "games_played": 0,
            "high_scores": {},
            "session_time": 0
        }
        data["users"][user_email] = user
    user["games_played"] += 1
    user["high_scores"][game_name] = max(score, user["high_scores"].get(game_name, 0))
    save_analytics(data)

def add_chat(user_email):
    data = load_analytics()
    user = data["users"].get(user_email)
    if user:
        user["chats_sent"] += 1
    else:
        data["users"][user_email] = {
            "logins": 0,
            "chats_sent": 1,
            "games_played": 0,
            "high_scores": {},
            "session_time": 0
        }
    save_analytics(data)

def add_session_time(user_email, seconds):
    data = load_analytics()
    user = data["users"].get(user_email)
    if user:
        user["session_time"] += seconds
    else:
        data["users"][user_email] = {
            "logins": 0,
            "chats_sent": 0,
            "games_played": 0,
            "high_scores": {},
            "session_time": seconds
        }
    save_analytics(data)

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    test_email = input("Enter user email for analytics test: ").strip()
    increment_logins(test_email)
    add_chat(test_email)
    add_game_play(test_email, "Number Guess", random.randint(50, 100))
    add_session_time(test_email, random.randint(60, 600))
    analytics_tab_ui(test_email)