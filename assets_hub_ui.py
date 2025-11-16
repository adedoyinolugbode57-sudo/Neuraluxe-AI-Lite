"""
Neuraluxe-AI Assets Hub Tab
---------------------------
- Browse, preview, and download assets
- Wallpapers, fonts, icons
- Lightweight, premium-rich
- Full access for adedoyinolugbode57@gmail.com
- Modular and deployable
"""

import json
from assets_logic import list_assets, preview_asset, download_asset, add_asset
from session_manager import FREE_USER_EMAIL, is_free_user

ASSETS_FILE = "assets_data.json"
WALLPAPERS_FILE = "wallpapers.json"
FONTS_FILE = "fonts.json"

# -------------------------
# Assets Hub UI
# -------------------------
def assets_hub_ui(user_email):
    full_access_user = (user_email == FREE_USER_EMAIL or not is_free_user(user_email))

    while True:
        print("\n--- Assets Hub Tab ---")
        print("1. List Assets")
        print("2. Preview Asset")
        print("3. Download Asset")
        print("4. Add New Asset")
        print("5. Exit Assets Hub")
        choice = input("Select option: ").strip()

        if choice == "1":
            list_assets(user_email, full_access_user)
        elif choice == "2":
            preview_asset(user_email, full_access_user)
        elif choice == "3":
            download_asset(user_email, full_access_user)
        elif choice == "4":
            add_asset(user_email, full_access_user)
        elif choice == "5":
            print("Exiting Assets Hub Tab...")
            break
        else:
            print("Invalid choice. Try again.")

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    assets_hub_ui(email)