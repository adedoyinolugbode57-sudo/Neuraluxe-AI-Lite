"""
Neuraluxe-AI Novel Hub Logic
----------------------------
- Handles novel data
- Read, list, and add novels
- Lightweight storage using JSON
"""

import json
import random
from session_manager import FREE_USER_EMAIL, is_free_user

NOVELS_FILE = "novels.json"

# -------------------------
# Load / Save Novels
# -------------------------
def load_novels():
    try:
        with open(NOVELS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_novels(novels):
    with open(NOVELS_FILE, "w") as f:
        json.dump(novels, f, indent=4)

# -------------------------
# List Novels
# -------------------------
def list_novels(user_email, full_access_user):
    novels = load_novels()
    if not novels:
        print("No novels available.")
        return
    print("\n--- Available Novels ---")
    for idx, (title, content) in enumerate(novels.items(), 1):
        print(f"{idx}. {title} - {len(content)} characters")

# -------------------------
# Read Novel
# -------------------------
def read_novel(user_email, full_access_user):
    novels = load_novels()
    if not novels:
        print("No novels to read.")
        return

    titles = list(novels.keys())
    for idx, title in enumerate(titles, 1):
        print(f"{idx}. {title}")
    try:
        choice = int(input("Select novel number to read: ").strip())
        selected_title = titles[choice - 1]
    except:
        print("Invalid selection.")
        return

    content = novels[selected_title]
    if is_free_user(user_email) and not full_access_user:
        print("\nLimited preview for free users (first 200 chars):")
        print(content[:200] + "...")
    else:
        print(f"\nReading '{selected_title}':\n")
        print(content)

# -------------------------
# Add New Novel
# -------------------------
def add_novel(user_email, full_access_user):
    if not full_access_user:
        print("Free users cannot add novels. Upgrade for full access.")
        return

    title = input("Enter novel title: ").strip()
    content = input("Enter novel content (or paste text): ").strip()
    novels = load_novels()
    if title in novels:
        print("Novel already exists.")
        return
    novels[title] = content
    save_novels(novels)
    print(f"Novel '{title}' added successfully! 🎉")