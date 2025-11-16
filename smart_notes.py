"""
Neuraluxe-Lite
Premium Smart Notes & Highlights Tab
---------------------------------
Features:
- Create, view, edit, and delete notes
- Highlight important parts of text
- Free vs Paid user handling
- Recent activity timestamps
- Quick tips
- Logging & timestamps
"""

import json
import os
from datetime import datetime

# -----------------------------
# Configurations
# -----------------------------
FREE_USER_EMAIL = "adedoyinolugbode57@gmail.com"
NOTES_JSON = "smart_notes.json"

# -----------------------------
# Helper Functions
# -----------------------------
def load_notes():
    if not os.path.exists(NOTES_JSON):
        with open(NOTES_JSON, "w") as f:
            json.dump({}, f)
    with open(NOTES_JSON, "r") as f:
        return json.load(f)

def save_notes(data):
    with open(NOTES_JSON, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} - {user_email} - {action}")

def display_quick_tips():
    tips = [
        "Paid users can create unlimited notes.",
        "Free users are limited to 3 notes per session.",
        "Use highlights to mark key points in your text.",
        "Notes are saved automatically.",
        "Edit and delete notes anytime.",
        "Activity timestamps help track your work."
    ]
    print("\n✨ Notes Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

# -----------------------------
# Notes Operations
# -----------------------------
def create_note(user_email, notes_data):
    full_access = (user_email == FREE_USER_EMAIL)
    user_notes = notes_data.setdefault(user_email, [])

    if not full_access and len(user_notes) >= 3:
        print("Free users can only create up to 3 notes. Upgrade for full access.")
        return

    title = input("Enter note title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    content = input("Enter note content: ").strip()
    if not content:
        print("Content cannot be empty.")
        return

    highlights_input = input("Enter highlights (comma separated, optional): ").strip()
    highlights = [h.strip() for h in highlights_input.split(",")] if highlights_input else []

    note = {
        "title": title,
        "content": content,
        "highlights": highlights,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    user_notes.append(note)
    save_notes(notes_data)
    print(f"✅ Note '{title}' created successfully!")
    log_activity(user_email, f"Created note '{title}'")

def view_notes(user_email, notes_data):
    user_notes = notes_data.get(user_email, [])
    if not user_notes:
        print("No notes found.")
        return

    print("\n📝 Your Notes:")
    for idx, note in enumerate(user_notes, 1):
        print(f"{idx}. {note['title']} [{note['timestamp']}] | Highlights: {', '.join(note['highlights'])}")

def edit_note(user_email, notes_data):
    user_notes = notes_data.get(user_email, [])
    if not user_notes:
        print("No notes to edit.")
        return

    view_notes(user_email, notes_data)
    choice = input("Enter note number to edit: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(user_notes):
        note = user_notes[int(choice)-1]
        new_title = input(f"New title (leave blank to keep '{note['title']}'): ").strip()
        new_content = input("New content (leave blank to keep existing): ").strip()
        new_highlights = input("New highlights (comma separated, leave blank to keep existing): ").strip()

        if new_title:
            note['title'] = new_title
        if new_content:
            note['content'] = new_content
        if new_highlights:
            note['highlights'] = [h.strip() for h in new_highlights.split(",")]

        save_notes(notes_data)
        print(f"✏️ Note '{note['title']}' updated successfully!")
        log_activity(user_email, f"Edited note '{note['title']}'")
    else:
        print("Invalid selection.")

def delete_note(user_email, notes_data):
    user_notes = notes_data.get(user_email, [])
    if not user_notes:
        print("No notes to delete.")
        return

    view_notes(user_email, notes_data)
    choice = input("Enter note number to delete: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(user_notes):
        deleted = user_notes.pop(int(choice)-1)
        save_notes(notes_data)
        print(f"🗑️ Deleted note '{deleted['title']}'")
        log_activity(user_email, f"Deleted note '{deleted['title']}'")
    else:
        print("Invalid selection.")

# -----------------------------
# Notes Tab Main
# -----------------------------
def notes_tab_ui(user_email):
    print("\n==============================")
    print("       SMART NOTES TAB        ")
    print("==============================\n")

    log_activity(user_email, "Opened Notes Tab")
    notes_data = load_notes()
    display_quick_tips()
    view_notes(user_email, notes_data)

    while True:
        print("\nOptions:")
        print("1. Create Note")
        print("2. View Notes")
        print("3. Edit Note")
        print("4. Delete Note")
        print("5. Exit Notes Tab")
        choice = input("Select option: ").strip()

        if choice == "1":
            create_note(user_email, notes_data)
        elif choice == "2":
            view_notes(user_email, notes_data)
        elif choice == "3":
            edit_note(user_email, notes_data)
        elif choice == "4":
            delete_note(user_email, notes_data)
        elif choice == "5":
            log_activity(user_email, "Closed Notes Tab")
            print("Exiting Notes Tab...\n")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    notes_tab_ui(email)