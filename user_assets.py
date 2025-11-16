import json
import os
from datetime import datetime
import random

WALLPAPERS_JSON = "wallpapers.json"
FONTS_JSON = "fonts.json"

# -----------------------------
# Helper to load/save JSON
# -----------------------------
def load_json(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({"wallpapers": [], "fonts": []}, f)
    with open(file_path, "r") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# Preload Wallpapers & Fonts
# -----------------------------
def preload_assets():
    wallpapers_data = load_json(WALLPAPERS_JSON)
    fonts_data = load_json(FONTS_JSON)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Preload 200 wallpapers
    for i in range(1, 201):
        wallpaper = {
            "name": f"Wallpaper_{i}",
            "description": f"Awesome Neuraluxe-AI wallpaper #{i}",
            "timestamp": timestamp,
            "ext": "png",
            "added_by": "system"
        }
        wallpapers_data.setdefault("wallpapers", []).append(wallpaper)

    # Preload 100 fonts
    for i in range(1, 101):
        font = {
            "name": f"Font_{i}",
            "description": f"Stylish Neuraluxe-AI font #{i}",
            "timestamp": timestamp,
            "ext": "ttf",
            "added_by": "system"
        }
        fonts_data.setdefault("fonts", []).append(font)

    save_json(WALLPAPERS_JSON, wallpapers_data)
    save_json(FONTS_JSON, fonts_data)
    print("✅ Preloaded 200 wallpapers and 100 fonts.")

# -----------------------------
# Add user assets
# -----------------------------
def add_user_wallpaper(user_email, name, description="No description", ext="png"):
    wallpapers_data = load_json(WALLPAPERS_JSON)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wallpaper = {
        "name": name,
        "description": description,
        "timestamp": timestamp,
        "ext": ext,
        "added_by": user_email
    }
    wallpapers_data.setdefault("wallpapers", []).append(wallpaper)
    save_json(WALLPAPERS_JSON, wallpapers_data)
    print(f"✅ Wallpaper '{name}' added by {user_email}")

def add_user_font(user_email, name, description="No description", ext="ttf"):
    fonts_data = load_json(FONTS_JSON)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    font = {
        "name": name,
        "description": description,
        "timestamp": timestamp,
        "ext": ext,
        "added_by": user_email
    }
    fonts_data.setdefault("fonts", []).append(font)
    save_json(FONTS_JSON, fonts_data)
    print(f"✅ Font '{name}' added by {user_email}")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    preload_assets()  # Preload assets on first run

    email = input("Enter your email: ").strip()
    while True:
        print("\nOptions:\n1. Add Wallpaper\n2. Add Font\n3. Exit")
        choice = input("Select option: ").strip()
        if choice == "1":
            name = input("Wallpaper Name: ").strip()
            desc = input("Description (optional): ").strip()
            add_user_wallpaper(email, name, desc or "No description")
        elif choice == "2":
            name = input("Font Name: ").strip()
            desc = input("Description (optional): ").strip()
            add_user_font(email, name, desc or "No description")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")