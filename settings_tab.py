"""
Neuraluxe-Lite
Premium Settings Tab
---------------------------------
Features:
- Theme selection & customization
- Free vs Paid user handling
- Notification preferences
- Account info display
- Quick tips
- Logging & timestamps
"""

import json
import os
from datetime import datetime

# -----------------------------
# Configurations
# -----------------------------
THEMES = ["default", "neon", "dark", "light", "blue", "green", "purple", "cyan", "magenta", "orange", "red", "yellow"]
FREE_USER_EMAIL = "adedoyinolugbode57@gmail.com"
USERS_JSON = "users.json"
SETTINGS_JSON = "settings.json"

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

def load_settings():
    if not os.path.exists(SETTINGS_JSON):
        with open(SETTINGS_JSON, "w") as f:
            json.dump({}, f)
    with open(SETTINGS_JSON, "r") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_JSON, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} - {user_email} - {action}")

def theme_selector(user_email, settings_data):
    print("\nAvailable Themes:")
    for idx, t in enumerate(THEMES, 1):
        print(f"{idx}. {t}")
    choice_idx = input("Select theme number (or press Enter to skip): ").strip()
    if choice_idx.isdigit() and 1 <= int(choice_idx) <= len(THEMES):
        theme = THEMES[int(choice_idx)-1]
        print(f"Theme applied: {theme}")
        settings_data.setdefault(user_email, {})["theme"] = theme
        save_settings(settings_data)
        return theme
    print("Default theme applied.")
    return "default"

def display_account_info(user_email):
    print("\n📄 Account Info:")
    print(f"- Email: {user_email}")
    print(f"- Status: {'Full Access' if user_email == FREE_USER_EMAIL else 'Free / Paid'}")
    print(f"- Registered On: {datetime.now().strftime('%Y-%m-%d')}")
    print()

def display_notifications_settings(user_email, settings_data):
    user_settings = settings_data.setdefault(user_email, {})
    notifications = user_settings.setdefault("notifications", {"search": True, "games": True, "chat": True})
    print("\n🔔 Notification Preferences:")
    for key, value in notifications.items():
        print(f"- {key.capitalize()}: {'Enabled' if value else 'Disabled'}")
    toggle = input("Type the notification to toggle or press Enter to skip: ").strip().lower()
    if toggle in notifications:
        notifications[toggle] = not notifications[toggle]
        save_settings(settings_data)
        print(f"{toggle.capitalize()} notifications toggled to {'Enabled' if notifications[toggle] else 'Disabled'}")
    print()

def display_quick_tips():
    tips = [
        "Change themes for comfort.",
        "Manage notifications for each tab.",
        "Free users have limited settings access.",
        "Account info shows basic details.",
        "Settings are saved automatically.",
        "Switch themes and see immediate effect.",
        "Use toggles to enable/disable notifications."
    ]
    print("\n✨ Settings Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

# -----------------------------
# Settings Tab Main
# -----------------------------
def settings_tab_ui(user_email):
    print("\n==============================")
    print("         SETTINGS TAB         ")
    print("==============================\n")

    log_activity(user_email, "Opened Settings Tab")

    settings_data = load_settings()
    display_quick_tips()
    display_account_info(user_email)
    theme = theme_selector(user_email, settings_data)
    display_notifications_settings(user_email, settings_data)

    while True:
        print("\nOptions:")
        print("1. Change Theme")
        print("2. Manage Notifications")
        print("3. View Account Info")
        print("4. Exit Settings Tab")
        choice = input("Select option: ").strip()

        if choice == "1":
            theme = theme_selector(user_email, settings_data)
        elif choice == "2":
            display_notifications_settings(user_email, settings_data)
        elif choice == "3":
            display_account_info(user_email)
        elif choice == "4":
            log_activity(user_email, "Closed Settings Tab")
            print("Exiting Settings Tab...\n")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    settings_tab_ui(email)