import json
import os
from datetime import datetime

WALLPAPERS_JSON = "wallpapers.json"
FONTS_JSON = "fonts.json"

def load_json(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({"wallpapers": [], "fonts": []}, f)
    with open(file_path, "r") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

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
    email = input("Enter your email: ").strip()
    while True:
        print("\nOptions: 1. Add Wallpaper  2. Add Font  3. Exit")
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