"""
Neuraluxe-AI Assets Hub Logic
-----------------------------
- Handles wallpapers, fonts, and asset data
- Lightweight JSON storage
- Preview, download, add new assets
"""

import json
from session_manager import FREE_USER_EMAIL, is_free_user

ASSETS_FILE = "assets_data.json"
WALLPAPERS_FILE = "wallpapers.json"
FONTS_FILE = "fonts.json"

# -------------------------
# Load / Save Assets
# -------------------------
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# List Assets
# -------------------------
def list_assets(user_email, full_access_user):
    assets = load_json(ASSETS_FILE)
    if not assets:
        print("No assets available.")
        return
    print("\n--- Available Assets ---")
    for idx, (name, info) in enumerate(assets.items(), 1):
        print(f"{idx}. {name} - {info.get('type','Unknown')}")

# -------------------------
# Preview Asset
# -------------------------
def preview_asset(user_email, full_access_user):
    assets = load_json(ASSETS_FILE)
    if not assets:
        print("No assets to preview.")
        return
    names = list(assets.keys())
    for idx, name in enumerate(names, 1):
        print(f"{idx}. {name}")
    try:
        choice = int(input("Select asset number to preview: ").strip())
        selected = names[choice - 1]
    except:
        print("Invalid selection.")
        return

    if is_free_user(user_email) and not full_access_user:
        print(f"Preview limited for free users: {selected}")
    else:
        print(f"\nPreviewing Asset: {selected}")
        print(f"Type: {assets[selected].get('type','Unknown')}")
        print(f"Description: {assets[selected].get('description','No description')}")
        print(f"URL/Path: {assets[selected].get('path','No path')}")

# -------------------------
# Download Asset
# -------------------------
def download_asset(user_email, full_access_user):
    assets = load_json(ASSETS_FILE)
    if not assets:
        print("No assets to download.")
        return
    names = list(assets.keys())
    for idx, name in enumerate(names, 1):
        print(f"{idx}. {name}")
    try:
        choice = int(input("Select asset number to download: ").strip())
        selected = names[choice - 1]
    except:
        print("Invalid selection.")
        return

    if is_free_user(user_email) and not full_access_user:
        print("Free users cannot download assets. Upgrade for full access.")
    else:
        print(f"Downloading Asset: {selected} ... Done!")

# -------------------------
# Add New Asset
# -------------------------
def add_asset(user_email, full_access_user):
    if not full_access_user:
        print("Free users cannot add assets. Upgrade for full access.")
        return

    name = input("Enter asset name: ").strip()
    asset_type = input("Enter asset type (wallpaper/font/icon/etc): ").strip()
    path = input("Enter URL or file path: ").strip()
    description = input("Enter short description: ").strip()

    assets = load_json(ASSETS_FILE)
    if name in assets:
        print("Asset already exists.")
        return

    assets[name] = {
        "type": asset_type,
        "path": path,
        "description": description
    }

    save_json(ASSETS_FILE, assets)
    print(f"Asset '{name}' added successfully! 🎉")