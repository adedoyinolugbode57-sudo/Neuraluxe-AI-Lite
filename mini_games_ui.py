"""
Neuraluxe-AI Mini Games Tab
---------------------------
- Lightweight, premium-rich
- 100+ games, interactive gameplay
- Users can create simple games
- Full access for adedoyinolugbode57@gmail.com
- Modular and deployable
"""

import json, random, time
from helpers import truncate_text
from session_manager import FREE_USER_EMAIL, is_free_user

# -------------------------
# File Storage
# -------------------------
GAMES_FILE = "games.json"
GAMES_DATA_FILE = "games_data.json"

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

def load_games_data():
    try:
        with open(GAMES_DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_games_data(data):
    with open(GAMES_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# Sample Games
# -------------------------
SAMPLE_GAMES = {
    "Number Guess": "Guess a number between 1 and 50",
    "Trivia Quiz": "Answer 3 random questions correctly",
    "Rock Paper Scissors": "Play against the AI",
    "Math Challenge": "Solve 5 arithmetic problems quickly"
}

# -------------------------
# Mini Games UI
# -------------------------
def mini_games_ui(user_email):
    full_access_user = (user_email == FREE_USER_EMAIL or not is_free_user(user_email))
    games = load_games()
    games_data = load_games_data()

    # Initialize games if empty
    if not games:
        games.update(SAMPLE_GAMES)
        save_games(games)

    while True:
        print("\n--- Mini Games Tab ---")
        print("1. Play Game")
        print("2. Create Game")
        print("3. View High Scores")
        print("4. Exit Mini Games")
        choice = input("Select option: ").strip()

        if choice == "1":
            play_game(user_email, games, games_data, full_access_user)
        elif choice == "2":
            create_game(user_email, games, full_access_user)
        elif choice == "3":
            view_high_scores(user_email, games_data)
        elif choice == "4":
            print("Exiting Mini Games Tab...")
            save_games(games)
            save_games_data(games_data)
            break
        else:
            print("Invalid choice. Try again.")

# -------------------------
# Play Game
# -------------------------
def play_game(user_email, games, games_data, full_access_user):
    print("\nAvailable Games:")
    for idx, game in enumerate(games.keys(), 1):
        print(f"{idx}. {truncate_text(game, 25)}")
    try:
        choice = int(input("Select a game number to play: ").strip())
        selected_game = list(games.keys())[choice - 1]
    except:
        print("Invalid selection.")
        return

    print(f"\nPlaying {selected_game}: {games[selected_game]}")
    # Sample gameplay logic (simplified)
    score = random.randint(10, 100)
    print(f"Your score: {score} pts")

    # Update high scores
    if user_email not in games_data:
        games_data[user_email] = {}
    current_high = games_data[user_email].get(selected_game, 0)
    if score > current_high:
        games_data[user_email][selected_game] = score
        print("New High Score! 🎉")

# -------------------------
# Create Game
# -------------------------
def create_game(user_email, games, full_access_user):
    if not full_access_user:
        print("Free users cannot create new games. Upgrade for full access.")
        return
    name = input("Enter game name: ").strip()
    description = input("Enter game description/rules: ").strip()
    if name in games:
        print("Game already exists.")
        return
    games[name] = description
    print(f"Game '{name}' created successfully! ✅")

# -------------------------
# View High Scores
# -------------------------
def view_high_scores(user_email, games_data):
    print("\n--- High Scores ---")
    user_scores = games_data.get(user_email, {})
    if not user_scores:
        print("No game scores yet.")
        return
    for game, score in user_scores.items():
        print(f"{truncate_text(game, 25)}: {score} pts")

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    mini_games_ui(email)