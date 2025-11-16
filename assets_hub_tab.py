"""
Neuraluxe-AI Assets Hub Tab
---------------------------
- Browse, preview, and download assets
- Wallpapers, fonts, icons, themes, audio, stickers, videos
- Lightweight, premium-rich
- Full access for adedoyinolugbode57@gmail.com
- Modular and deployable
"""

import json
from session_manager import FREE_USER_EMAIL, is_free_user

# -------------------------
# File paths
# -------------------------
WALLPAPERS_FILE = "wallpapers.json"
FONTS_FILE = "fonts.json"
ICONS_FILE = "icons.json"
THEMES_FILE = "themes.json"
AUDIO_FILE = "audio.json"
STICKERS_FILE = "stickers.json"
VIDEOS_FILE = "videos.json"

# -------------------------
# Helpers
# -------------------------
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# -------------------------
# List Assets
# -------------------------
def list_assets(user_email, full_access):
    print("\n--- Available Assets ---")
    print(f"Full Access: {full_access}")
    print("1. Wallpapers")
    print("2. Fonts")
    print("3. Icons")
    print("4. Themes")
    print("5. Audio")
    print("6. Stickers")
    print("7. Videos")

# -------------------------
# Preview Asset
# -------------------------
def preview_asset(user_email, full_access):
    category = input("Category: ").strip().lower()
    print(f"Previewing from {category}...")

# -------------------------
# Download Asset
# -------------------------
def download_asset(user_email, full_access):
    if not full_access:
        print("Premium only.")
        return
    category = input("Category: ").strip().lower()
    print(f"Downloading from {category}...")

# -------------------------
# Add Asset
# -------------------------
def add_asset(user_email, full_access):
    if not full_access:
        print("Premium only.")
        return
    category = input("Category: ").strip().lower()
    name = input("Asset name: ").strip()

    if category == "wallpapers":
        data = load_json(WALLPAPERS_FILE)
        data.append({"name": name})
        save_json(WALLPAPERS_FILE, data)

    elif category == "fonts":
        data = load_json(FONTS_FILE)
        data.append({"name": name})
        save_json(FONTS_FILE, data)

    elif category == "icons":
        data = load_json(ICONS_FILE)
        data.append({"name": name})
        save_json(ICONS_FILE, data)

    elif category == "themes":
        data = load_json(THEMES_FILE)
        data.append({"name": name})
        save_json(THEMES_FILE, data)

    elif category == "audio":
        data = load_json(AUDIO_FILE)
        data.append({"name": name})
        save_json(AUDIO_FILE, data)

    elif category == "stickers":
        data = load_json(STICKERS_FILE)
        data.append({"name": name})
        save_json(STICKERS_FILE, data)

    elif category == "videos":
        data = load_json(VIDEOS_FILE)
        data.append({"name": name})
        save_json(VIDEOS_FILE, data)

    print("Asset added successfully.")

# -------------------------
# UI
# -------------------------
def assets_hub_ui(user_email):
    full_access = (user_email == FREE_USER_EMAIL or not is_free_user(user_email))

    while True:
        print("\n--- Assets Hub Tab ---")
        print("1. List Assets")
        print("2. Preview Asset")
        print("3. Download Asset")
        print("4. Add New Asset")
        print("5. Exit Assets Hub")

        ch = input("Select: ").strip()

        if ch == "1":
            list_assets(user_email, full_access)
        elif ch == "2":
            preview_asset(user_email, full_access)
        elif ch == "3":
            download_asset(user_email, full_access)
        elif ch == "4":
            add_asset(user_email, full_access)
        elif ch == "5":
            break
        else:
            print("Invalid")

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter email: ").strip()
    assets_hub_ui(email)