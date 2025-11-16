"""
Neuraluxe-Lite
Premium Create Game Tab
---------------------------------
Features:
- Create and save mini-games
- Free vs Paid access
- Game title, description, type selection
- View all created games
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
GAMES_JSON = "games.json"

GAME_TYPES = ["Puzzle", "Trivia", "Arcade", "Strategy", "Adventure"]

# -----------------------------
# Helper Functions
# -----------------------------
def load_games():
    if not os.path.exists(GAMES_JSON):
        with open(GAMES_JSON, "w") as f:
            json.dump({}, f)
    with open(GAMES_JSON, "r") as f:
        return json.load(f)

def save_games(data):
    with open(GAMES_JSON, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} - {user_email} - {action}")

def display_quick_tips():
    tips = [
        "Free users can create up to 2 games only.",
        "Paid users have full access to create unlimited games.",
        "Games require a title and type selection.",
        "View all created games from this tab.",
        "All games are saved automatically.",
        "Use descriptive titles for better organization."
    ]
    print("\n✨ Create Game Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

def view_games(user_email, games_data):
    user_games = games_data.get(user_email, [])
    print("\n🎮 Your Created Games:")
    if not user_games:
        print("- No games created yet.")
    else:
        for idx, g in enumerate(user_games, 1):
            print(f"{idx}. {g['title']} ({g['type']}) - {g['description']} [{g['timestamp']}]")
    print()

def create_game(user_email, games_data):
    full_access = (user_email == FREE_USER_EMAIL)
    user_games = games_data.setdefault(user_email, [])

    if not full_access and len(user_games) >= 2:
        print("Free users can only create up to 2 games. Upgrade for full access.")
        return

    title = input("Enter game title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    print("\nAvailable Game Types:")
    for idx, t in enumerate(GAME_TYPES, 1):
        print(f"{idx}. {t}")
    type_idx = input("Select game type number: ").strip()
    if not type_idx.isdigit() or int(type_idx) < 1 or int(type_idx) > len(GAME_TYPES):
        print("Invalid type selected. Defaulting to Puzzle.")
        game_type = "Puzzle"
    else:
        game_type = GAME_TYPES[int(type_idx)-1]

    description = input("Enter game description: ").strip()
    if not description:
        description = "No description provided."

    new_game = {
        "title": title,
        "type": game_type,
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    user_games.append(new_game)
    save_games(games_data)
    print(f"✅ Game '{title}' created successfully!")

# -----------------------------
# Create Game Tab Main
# -----------------------------
def create_game_tab_ui(user_email):
    print("\n==============================")
    print("        CREATE GAME TAB       ")
    print("==============================\n")

    log_activity(user_email, "Opened Create Game Tab")
    games_data = load_games()
    display_quick_tips()
    view_games(user_email, games_data)

    while True:
        print("\nOptions:")
        print("1. View Created Games")
        print("2. Create New Game")
        print("3. Exit Create Game Tab")
        choice = input("Select option: ").strip()

        if choice == "1":
            view_games(user_email, games_data)
        elif choice == "2":
            create_game(user_email, games_data)
        elif choice == "3":
            log_activity(user_email, "Closed Create Game Tab")
            print("Exiting Create Game Tab...\n")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    create_game_tab_ui(email)