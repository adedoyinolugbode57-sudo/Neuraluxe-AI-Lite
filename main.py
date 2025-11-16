"""
Neuraluxe-AI Lite - Fully Premium-Checked
-----------------------------------------
- Lightweight & modular
- Premium-only access enforced
"""

from chat_tab_ui import chat_tab_ui
from mini_games_ui import mini_games_ui
from create_game_ui import create_game_ui
from web_search_ui import web_search_ui
from analytics_tab_ui import analytics_tab_ui
from settings_tab_ui import settings_tab_ui
from history_ui import history_ui
from community_ui import community_ui
from novel_hub_ui import novel_hub_ui
from assets_hub_ui import assets_hub_ui
from voice_assistant import voice_assistant_ui
from login import login
from subscription_manager import is_premium, unlock_subscription, record_payment
from opay_integration import simulate_payment
import sys

def main():
    print("\n=== Welcome to Neuraluxe-AI Lite ===")
    user_info = login()
    email = user_info["email"]

    # -------------------------
    # Premium Check
    # -------------------------
    if not is_premium(email):
        print(f"⚠️ {email} does not have premium access.")
        choice = input("Simulate payment now? (y/n): ").strip().lower()
        if choice == "y":
            # Simulate Opay payment for NGN ~12,500 (~$6.99)
            simulate_payment(email, 12500)
            record_payment(email, 12500)
            unlock_subscription(email)
        else:
            print("❌ Access denied. Only premium users can use Neuraluxe-AI Lite.")
            return
    else:
        print(f"✅ {email} has premium access.")

    # -------------------------
    # Main Menu Loop
    # -------------------------
    while True:
        print("\n--- Main Menu ---")
        print("1. Chat Tab")
        print("2. Mini Games")
        print("3. Create Game")
        print("4. Web Search")
        print("5. Analytics")
        print("6. Settings")
        print("7. History")
        print("8. Community")
        print("9. Novel Hub")
        print("10. Assets Hub")
        print("11. Voice Assistant")
        print("12. Exit Neuraluxe-AI Lite")

        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                chat_tab_ui(email)
            elif choice == "2":
                mini_games_ui(email)
            elif choice == "3":
                create_game_ui(email)
            elif choice == "4":
                web_search_ui(email)
            elif choice == "5":
                analytics_tab_ui(email)
            elif choice == "6":
                settings_tab_ui(email)
            elif choice == "7":
                history_ui(email)
            elif choice == "8":
                community_ui(email)
            elif choice == "9":
                novel_hub_ui(email)
            elif choice == "10":
                assets_hub_ui(email)
            elif choice == "11":
                voice_assistant_ui(email)
            elif choice == "12":
                print("Exiting Neuraluxe-AI Lite... Goodbye!")
                break
            else:
                print("Invalid option. Try again.")
        except Exception as e:
            print(f"⚠️ Error occurred: {e}. Returning to main menu.")

# -------------------------
# Standalone Run
# -------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Neuraluxe-AI Lite... Goodbye!")
        sys.exit(0)