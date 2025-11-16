"""
Neuraluxe-AI Create Game Tab
---------------------------
- Allows users to create mini-games
- Lightweight, premium-rich
- Games are saved in games.json
- Full access for adedoyinolugbode57@gmail.com
- Modular and deployable
"""

import json
import random
import time
from helpers import truncate_text
from session_manager import FREE_USER_EMAIL, is_free_user

GAMES_FILE = "games.json"

# -------------------------
# Load / Save Games
# -------------------------
def load_games():
    try:
        with open(GAMES_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_games(games):
    with open(GAMES_FILE, "w") as f:
        json.dump(games, f, indent=4)

# -------------------------
# Create Game UI
# -------------------------
def create_game_ui(user_email):
    full_access_user = (user_email == FREE_USER_EMAIL or not is_free_user(user_email))
    games = load_games()

    while True:
        print("\n--- Create Game Tab ---")
        print("1. Create New Game")
        print("2. List All Games")
        print("3. Exit Create Game Tab")
        choice = input("Select option: ").strip()

        if choice == "1":
            create_game(user_email, games, full_access_user)
        elif choice == "2":
            list_games(games)
        elif choice == "3":
            print("Exiting Create Game Tab...")
            save_games(games)
            break
        else:
            print("Invalid choice. Try again.")

# -------------------------
# Create New Game
# -------------------------
def create_game(user_email, games, full_access_user):
    if not full_access_user:
        print("Free users cannot create games. Upgrade for full access.")
        return

    name = input("Enter game name: ").strip()
    if name in games:
        print("Game already exists.")
        return

    description = input("Enter game description or rules: ").strip()

    # Optional sample data
    sample_data = []
    for i in range(3):
        sample_question = input(f"Enter sample content/question {i+1}: ").strip()
        sample_answer = input(f"Enter answer for sample content {i+1}: ").strip()
        sample_data.append({"question": sample_question, "answer": sample_answer})

    games[name] = {
        "description": description,
        "sample_data": sample_data
    }

    print(f"Game '{name}' created successfully! 🎉")
    save_games(games)

# -------------------------
# List All Games
# -------------------------
def list_games(games):
    if not games:
        print("No games available.")
        return
    print("\n--- Available Games ---")
    for idx, (name, info) in enumerate(games.items(), 1):
        print(f"{idx}. {truncate_text(name, 25)} - {truncate_text(info.get('description',''), 40)}")

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    create_game_ui(email)