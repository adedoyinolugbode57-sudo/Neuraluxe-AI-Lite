"""
Neuraluxe-AI Home Interface (Upgraded)
--------------------------------------
- 12-tab management
- 20 decorative/premium features
- Lightweight and deployable
"""

from new_chat_ui import new_chat_ui
from mini_games_ui import mini_games_ui
from analytics_tab_ui import analytics_tab_ui
from web_search_ui import web_search_ui
from settings_tab_ui import settings_tab_ui
from history_ui import history_ui
from community_ui import community_ui
from create_game_ui import create_game_ui
from novel_hub_ui import novel_hub_ui
from assets_hub_ui import assets_hub_ui
from voice_assistant import voice_assistant_ui
from session_manager import login_user, logout_user, is_free_user, FREE_USER_EMAIL
from helpers import generate_id, validate_theme
import random, time, os

# -------------------------
# 20 Decorative/Premium Features
# -------------------------
DECORATIVE_FEATURES = [
    "Colorful Tab Highlights",
    "Animated Loading Bubbles",
    "Random Welcome Messages",
    "User XP Tracking",
    "Daily AI Tips",
    "Mini Confetti Animations",
    "Theme Switcher (Neon/Dark/Light)",
    "Chat Emojis & Symbols",
    "Session Time Tracker",
    "Randomized Greeting Sound Effects",
    "Dynamic Tab Icons",
    "Progress Bars for Games & Chat",
    "Background Animations (ASCII/Neon)",
    "AI Fun Facts Display",
    "Quick Links to Favorites",
    "Customizable Chat Bubble Styles",
    "Random Motivational Quotes",
    "Leaderboard Snapshots",
    "User Badges & Achievements",
    "Shortcut Keys for Tabs"
]

# -------------------------
# Welcome Display
# -------------------------
def display_welcome(user_email):
    print("\n" + "*" * 60)
    print(f"Welcome to Neuraluxe-AI, {user_email}!")
    print(random.choice([
        "Let's make AI fun today! 🤖",
        "Your creativity, now turbocharged with AI! 🌟",
        "Neuraluxe-AI: Where ideas come alive! 💡",
        "Premium AI, lightweight & super fast! 🚀"
    ]))
    print("Decorative Features Active: ", ", ".join(random.sample(DECORATIVE_FEATURES, 5)))
    print("*" * 60 + "\n")

# -------------------------
# Main Home UI
# -------------------------
def home_ui(user_email):
    premium_user = (user_email == FREE_USER_EMAIL or not is_free_user(user_email))
    display_welcome(user_email)
    
    while True:
        print("\n--- Neuraluxe-AI Home ---")
        print("Select a Tab:")
        print("1. New Chat")
        print("2. Mini-Games")
        print("3. Analytics")
        print("4. Web Search")
        print("5. Settings")
        print("6. History")
        print("7. Community")
        print("8. Create Game")
        print("9. Novel Hub")
        print("10. Assets Hub")
        print("11. Voice Assistant")
        print("12. Tutorials & Tips")
        print("13. User Badges & Achievements")
        print("14. Daily Challenges")
        print("15. Favorites")
        print("16. Leaderboard")
        print("17. Quick Shortcuts")
        print("18. AI Fun Facts")
        print("19. Session Stats")
        print("20. Exit")

        choice = input("Enter your choice (1-20): ").strip()
        
        if choice == "1":
            new_chat_ui(user_email)
        elif choice == "2":
            mini_games_ui(user_email)
        elif choice == "3":
            analytics_tab_ui(user_email)
        elif choice == "4":
            web_search_ui(user_email)
        elif choice == "5":
            settings_tab_ui(user_email)
        elif choice == "6":
            history_ui(user_email)
        elif choice == "7":
            community_ui(user_email)
        elif choice == "8":
            create_game_ui(user_email)
        elif choice == "9":
            novel_hub_ui(user_email)
        elif choice == "10":
            assets_hub_ui(user_email)
        elif choice == "11":
            voice_assistant_ui(user_email)
        elif choice == "12":
            print("Tutorials & Tips placeholder")
        elif choice == "13":
            print("User Badges & Achievements placeholder")
        elif choice == "14":
            print("Daily Challenges placeholder")
        elif choice == "15":
            print("Favorites placeholder")
        elif choice == "16":
            print("Leaderboard placeholder")
        elif choice == "17":
            print("Quick Shortcuts placeholder")
        elif choice == "18":
            print("AI Fun Facts placeholder")
        elif choice == "19":
            print("Session Stats placeholder")
        elif choice == "20":
            print("Exiting Neuraluxe-AI Home...")
            break
        else:
            print("Invalid choice. Try again.")

        # Decorative animation: loading bubbles
        animate_loading()

# -------------------------
# Decorative Loading Animation
# -------------------------
def animate_loading():
    bubbles = ["(●‿●)", "(◕‿◕)", "(✿◠‿◠)", "(•‿•)", "(≧◡≦)"]
    print("Loading ", end="")
    for _ in range(5):
        print(random.choice(bubbles), end=" ", flush=True)
        time.sleep(0.2)
    print("\n")

# -------------------------
# Login / Session Simulation
# -------------------------
def login_flow():
    email = input("Enter your email: ").strip()
    login_user(email)
    return email

def logout_flow(user_email):
    logout_user(user_email)

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    user_email = login_flow()
    home_ui(user_email)
    logout_flow(user_email)