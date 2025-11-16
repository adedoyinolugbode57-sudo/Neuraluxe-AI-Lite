"""
Neuraluxe-Lite
Premium Voice Assistant Tab
---------------------------------
Features:
- Lightweight TTS simulation
- Free vs Paid user logic
- Recent commands
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

def speak_text(user_email, text):
    """Lightweight TTS simulation"""
    if user_email != FREE_USER_EMAIL:
        print("⚠️ Free users have limited TTS per session.\n")
    timestamp = datetime.now().strftime("%H:%M")
    print(f"[{timestamp}] Neuraluxe speaks: {text}\n")

def display_recent_commands(user_email, users_data):
    print("\n📁 Recent Voice Commands:")
    user_data = users_data.get(user_email, {})
    commands = user_data.get("voice_commands", [])
    if not commands:
        print("- No recent commands found.")
    else:
        for idx, cmd in enumerate(commands[-5:], 1):
            print(f"{idx}. {cmd}")
    print()

def add_dummy_commands(user_email, users_data):
    user_data = users_data.setdefault(user_email, {})
    commands = user_data.setdefault("voice_commands", [])
    for _ in range(randint(1,3)):
        commands.append(f"Command {randint(100,999)}")
    save_users(users_data)

def display_mini_analytics(user_email, users_data):
    print("\n📊 Voice Assistant Mini Analytics:")
    user_data = users_data.get(user_email, {})
    commands = len(user_data.get("voice_commands", []))
    print(f"- Total Commands: {commands}")
    print(f"- Status: {'Free' if user_email != FREE_USER_EMAIL else 'Full Access'}\n")

def display_quick_tips():
    tips = [
        "Keep voice commands clear.",
        "Free users have limited TTS.",
        "Switch themes for comfort.",
        "Check mini analytics regularly.",
        "Try fun phrases to test TTS.",
        "Combine with Chat Tab for best results.",
        "Recent commands are saved automatically."
    ]
    print("\n✨ Voice Assistant Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

# -----------------------------
# Voice Assistant Tab Main
# -----------------------------
def voice_assistant_tab_ui(user_email):
    print("\n==============================")
    print("      VOICE ASSISTANT TAB      ")
    print("==============================\n")

    users_data = load_users()
    add_dummy_commands(user_email, users_data)

    log_activity(user_email, "Opened Voice Assistant Tab")

    theme = theme_selector()
    display_quick_tips()
    display_recent_commands(user_email, users_data)
    display_mini_analytics(user_email, users_data)

    while True:
        print("Options:")
        print("1. Say something")
        print("2. Refresh")
        print("3. Exit Voice Assistant")
        choice = input("Select option: ").strip()

        if choice == "1":
            text = input("Enter text to speak: ").strip()
            if not text:
                print("Nothing entered. Try again.\n")
                continue
            speak_text(user_email, text)

            # Log command
            user_data = users_data.setdefault(user_email, {})
            commands = user_data.setdefault("voice_commands", [])
            commands.append(text)
            save_users(users_data)

            display_mini_analytics(user_email, users_data)

        elif choice == "2":
            print("\n🔄 Refreshing Voice Assistant Tab...\n")
            display_recent_commands(user_email, users_data)
            display_mini_analytics(user_email, users_data)
        elif choice == "3":
            log_activity(user_email, "Closed Voice Assistant Tab")
            print("Exiting Voice Assistant Tab...\n")
            break
        else:
            print("Invalid option. Try again.\n")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    voice_assistant_tab_ui(email)