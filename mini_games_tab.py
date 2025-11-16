"""
Neuraluxe-Lite
Premium Mini Games Tab
---------------------------------
Features:
- Lightweight simulated mini games
- Free vs Paid access
- Recent played games
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
GAMES_JSON = "games.json"

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

def load_games():
    if not os.path.exists(GAMES_JSON):
        default_games = ["Tic-Tac-Toe", "Number Guess", "Word Scramble", "Trivia Challenge", "Rock Paper Scissors"]
        with open(GAMES_JSON, "w") as f:
            json.dump(default_games, f)
    with open(GAMES_JSON, "r") as f:
        return json.load(f)

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

def display_recent_games(user_email, users_data):
    print("\n📁 Recent Played Games:")
    user_data = users_data.get(user_email, {})
    games = user_data.get("recent_games", [])
    if not games:
        print("- No recent games played.")
    else:
        for idx, g in enumerate(games[-5:], 1):
            print(f"{idx}. {g}")
    print()

def add_dummy_games(user_email, users_data):
    user_data = users_data.setdefault(user_email, {})
    recent_games = user_data.setdefault("recent_games", [])
    for _ in range(randint(1,2)):
        recent_games.append(f"Game {randint(100,999)}")
    save_users(users_data)

def display_mini_analytics(user_email, users_data):
    print("\n📊 Mini Games Analytics:")
    user_data = users_data.get(user_email, {})
    games_played = len(user_data.get("recent_games", []))
    print(f"- Total Games Played: {games_played}")
    print(f"- Status: {'Free' if user_email != FREE_USER_EMAIL else 'Full Access'}\n")

def display_quick_tips():
    tips = [
        "Try different games to unlock fun.",
        "Free users may have limited plays.",
        "Switch themes for comfort.",
        "Mini analytics shows your gaming stats.",
        "Combine with Chat Tab for hints.",
        "Recent games are saved automatically.",
        "Enjoy multiple rounds for practice."
    ]
    print("\n✨ Mini Games Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

def simulate_game_play(game_name):
    """Lightweight game simulation"""
    outcomes = ["Victory!", "Try Again!", "Draw", "You Won!", "Better Luck Next Time!"]
    print(f"\n🎮 Playing {game_name}...")
    print(f"Result: {choice(outcomes)}\n")

# -----------------------------
# Mini Games Tab Main
# -----------------------------
def mini_games_tab_ui(user_email):
    print("\n==============================")
    print("        MINI GAMES TAB        ")
    print("==============================\n")

    users_data = load_users()
    add_dummy_games(user_email, users_data)

    log_activity(user_email, "Opened Mini Games Tab")

    theme = theme_selector()
    display_quick_tips()
    display_recent_games(user_email, users_data)
    display_mini_analytics(user_email, users_data)

    games_list = load_games()

    while True:
        print("Available Games:")
        for idx, game in enumerate(games_list, 1):
            print(f"{idx}. {game}")
        print("0. Exit Mini Games Tab")
        choice = input("Select a game to play: ").strip()

        if choice == "0":
            log_activity(user_email, "Closed Mini Games Tab")
            print("Exiting Mini Games Tab...\n")
            break

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(games_list):
            print("Invalid selection. Try again.\n")
            continue

        selected_game = games_list[int(choice)-1]

        # Free vs Paid Limitation
        if user_email != FREE_USER_EMAIL:
            print("⚠️ Free users may have limited game rounds per session.\n")

        # Simulate play
        simulate_game_play(selected_game)

        # Log game
        user_data = users_data.setdefault(user_email, {})
        recent_games = user_data.setdefault("recent_games", [])
        recent_games.append(selected_game)
        save_users(users_data)

        display_mini_analytics(user_email, users_data)

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    mini_games_tab_ui(email)