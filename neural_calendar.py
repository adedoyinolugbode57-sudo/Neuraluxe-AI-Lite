"""
Neuraluxe-Lite
Premium Calendar & Reminders Tab
---------------------------------
Features:
- Add, view, and delete events
- Set reminders for important tasks
- Free vs Paid user handling
- Recent activity timestamps
- Quick tips
- Logging & timestamps
"""

import json
import os
from datetime import datetime, timedelta

# -----------------------------
# Configurations
# -----------------------------
FREE_USER_EMAIL = "adedoyinolugbode57@gmail.com"
CALENDAR_JSON = "calendar.json"

# -----------------------------
# Helper Functions
# -----------------------------
def load_calendar():
    if not os.path.exists(CALENDAR_JSON):
        with open(CALENDAR_JSON, "w") as f:
            json.dump({}, f)
    with open(CALENDAR_JSON, "r") as f:
        return json.load(f)

def save_calendar(data):
    with open(CALENDAR_JSON, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} - {user_email} - {action}")

def display_quick_tips():
    tips = [
        "Add reminders for important events.",
        "Paid users can set unlimited events.",
        "Free users are limited to 3 events per session.",
        "Check upcoming tasks regularly.",
        "Events are timestamped automatically.",
        "Use the delete option to remove old events."
    ]
    print("\n✨ Calendar Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

# -----------------------------
# Calendar Operations
# -----------------------------
def add_event(user_email, calendar_data):
    full_access = (user_email == FREE_USER_EMAIL)
    user_events = calendar_data.setdefault(user_email, [])

    if not full_access and len(user_events) >= 3:
        print("Free users can only add up to 3 events. Upgrade for full access.")
        return

    title = input("Enter event title: ").strip()
    if not title:
        print("Event title cannot be empty.")
        return
    description = input("Enter event description (optional): ").strip()
    date_str = input("Enter event date (YYYY-MM-DD): ").strip()
    time_str = input("Enter event time (HH:MM, 24h format, optional): ").strip()

    try:
        event_datetime = datetime.strptime(date_str + " " + (time_str or "00:00"), "%Y-%m-%d %H:%M")
    except:
        print("Invalid date/time format.")
        return

    event = {
        "title": title,
        "description": description,
        "datetime": event_datetime.strftime("%Y-%m-%d %H:%M"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    user_events.append(event)
    save_calendar(calendar_data)
    print(f"✅ Event '{title}' added successfully!")
    log_activity(user_email, f"Added event '{title}'")

def view_events(user_email, calendar_data):
    user_events = calendar_data.get(user_email, [])
    if not user_events:
        print("No upcoming events.")
        return

    sorted_events = sorted(user_events, key=lambda e: e["datetime"])
    print("\n📅 Upcoming Events:")
    for idx, ev in enumerate(sorted_events, 1):
        print(f"{idx}. {ev['title']} - {ev['datetime']} | {ev.get('description', '')}")

def delete_event(user_email, calendar_data):
    user_events = calendar_data.get(user_email, [])
    if not user_events:
        print("No events to delete.")
        return

    view_events(user_email, calendar_data)
    choice = input("Enter event number to delete: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(user_events):
        deleted = user_events.pop(int(choice)-1)
        save_calendar(calendar_data)
        print(f"🗑️ Deleted event '{deleted['title']}'")
        log_activity(user_email, f"Deleted event '{deleted['title']}'")
    else:
        print("Invalid selection.")

def upcoming_reminders(user_email, calendar_data):
    now = datetime.now()
    user_events = calendar_data.get(user_email, [])
    reminders = [e for e in user_events if datetime.strptime(e["datetime"], "%Y-%m-%d %H:%M") > now]

    if not reminders:
        print("No upcoming reminders.")
        return

    sorted_reminders = sorted(reminders, key=lambda e: e["datetime"])
    print("\n⏰ Upcoming Reminders:")
    for idx, ev in enumerate(sorted_reminders[:5], 1):
        print(f"{idx}. {ev['title']} at {ev['datetime']}")

# -----------------------------
# Calendar Tab Main
# -----------------------------
def calendar_tab_ui(user_email):
    print("\n==============================")
    print("        CALENDAR TAB          ")
    print("==============================\n")

    log_activity(user_email, "Opened Calendar Tab")
    calendar_data = load_calendar()
    display_quick_tips()
    upcoming_reminders(user_email, calendar_data)

    while True:
        print("\nOptions:")
        print("1. Add Event")
        print("2. View Events")
        print("3. Delete Event")
        print("4. Upcoming Reminders")
        print("5. Exit Calendar Tab")
        choice = input("Select option: ").strip()

        if choice == "1":
            add_event(user_email, calendar_data)
        elif choice == "2":
            view_events(user_email, calendar_data)
        elif choice == "3":
            delete_event(user_email, calendar_data)
        elif choice == "4":
            upcoming_reminders(user_email, calendar_data)
        elif choice == "5":
            log_activity(user_email, "Closed Calendar Tab")
            print("Exiting Calendar Tab...\n")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    calendar_tab_ui(email)