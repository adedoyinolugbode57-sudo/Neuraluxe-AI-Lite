"""
Neuraluxe-AI: Smart Tasks Module
--------------------------------
- Lightweight, premium-rich task management
- Create, read, update, complete, and delete tasks
- Track timestamps, priority, and history
- Modular and deployable
"""

import json
import os
from datetime import datetime

# -----------------------------
# Config & Storage
# -----------------------------
TASKS_FILE = "tasks_data.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump({}, f)
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(data):
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# Logging
# -----------------------------
def log_task_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[TASKS] {timestamp} - {user_email} - {action}")

# -----------------------------
# Task Management
# -----------------------------
def add_task(user_email, title, description="", priority="Normal"):
    tasks_data = load_tasks()
    user_tasks = tasks_data.setdefault(user_email, [])
    new_task = {
        "title": title,
        "description": description,
        "priority": priority,
        "completed": False,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    user_tasks.append(new_task)
    save_tasks(tasks_data)
    log_task_activity(user_email, f"Added task '{title}'")
    print(f"✅ Task '{title}' added successfully!")

def list_tasks(user_email, show_completed=False):
    tasks_data = load_tasks()
    user_tasks = tasks_data.get(user_email, [])
    if not user_tasks:
        print("No tasks found.")
        return
    print("\n--- Your Tasks ---")
    for idx, task in enumerate(user_tasks, 1):
        if not show_completed and task["completed"]:
            continue
        status = "✅" if task["completed"] else "❌"
        print(f"{idx}. [{status}] {task['title']} (Priority: {task['priority']}) - {task['timestamp']}")
    print()

def mark_task_complete(user_email):
    tasks_data = load_tasks()
    user_tasks = tasks_data.get(user_email, [])
    if not user_tasks:
        print("No tasks to mark complete.")
        return
    list_tasks(user_email)
    choice = input("Enter task number to mark complete: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(user_tasks):
        task = user_tasks[int(choice)-1]
        task["completed"] = True
        save_tasks(tasks_data)
        log_task_activity(user_email, f"Marked task '{task['title']}' complete")
        print(f"✅ Task '{task['title']}' marked complete!")
    else:
        print("Invalid selection.")

def delete_task(user_email):
    tasks_data = load_tasks()
    user_tasks = tasks_data.get(user_email, [])
    if not user_tasks:
        print("No tasks to delete.")
        return
    list_tasks(user_email, show_completed=True)
    choice = input("Enter task number to delete: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(user_tasks):
        task = user_tasks.pop(int(choice)-1)
        save_tasks(tasks_data)
        log_task_activity(user_email, f"Deleted task '{task['title']}'")
        print(f"🗑️ Task '{task['title']}' deleted successfully!")
    else:
        print("Invalid selection.")

def search_tasks(user_email):
    term = input("Enter search term: ").strip().lower()
    tasks_data = load_tasks()
    user_tasks = tasks_data.get(user_email, [])
    results = [t for t in user_tasks if term in t['title'].lower() or term in t['description'].lower()]
    print(f"\n🔍 Search Results for '{term}':")
    if not results:
        print("- No matching tasks found.")
    else:
        for idx, task in enumerate(results, 1):
            status = "✅" if task["completed"] else "❌"
            print(f"{idx}. [{status}] {task['title']} (Priority: {task['priority']}) - {task['timestamp']}")
    print()

def view_recent_tasks(user_email, last_n=5):
    tasks_data = load_tasks()
    user_tasks = tasks_data.get(user_email, [])
    print(f"\n--- Last {last_n} Tasks ---")
    for task in user_tasks[-last_n:]:
        status = "✅" if task["completed"] else "❌"
        print(f"{task['title']} [{status}] - {task['timestamp']}")
    print()

# -----------------------------
# Tips
# -----------------------------
def tasks_tips():
    tips = [
        "Use clear titles for tasks for easy reference.",
        "Set priorities to organize your workflow.",
        "Mark tasks complete to track progress.",
        "Search helps find tasks quickly.",
        "Recent tasks show your latest activity."
    ]
    print("\n💡 Tasks Tips:")
    for idx, tip in enumerate(tips, 1):
        print(f"{idx}. {tip}")
    print()

# -----------------------------
# User Interface
# -----------------------------
def smart_tasks_ui(user_email):
    print("\n==============================")
    print("          SMART TASKS         ")
    print("==============================")
    log_task_activity(user_email, "Opened Smart Tasks")

    tasks_tips()

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task Complete")
        print("4. Search Tasks")
        print("5. Delete Task")
        print("6. View Recent Tasks")
        print("7. Exit Tasks")

        choice = input("Select option: ").strip()

        if choice == "1":
            title = input("Enter task title: ").strip()
            desc = input("Enter task description (optional): ").strip()
            priority = input("Enter priority (Low/Normal/High, default=Normal): ").strip() or "Normal"
            if title:
                add_task(user_email, title, desc, priority)
            else:
                print("Title cannot be empty.")
        elif choice == "2":
            list_tasks(user_email)
        elif choice == "3":
            mark_task_complete(user_email)
        elif choice == "4":
            search_tasks(user_email)
        elif choice == "5":
            delete_task(user_email)
        elif choice == "6":
            view_recent_tasks(user_email)
        elif choice == "7":
            log_task_activity(user_email, "Closed Smart Tasks")
            print("Exiting Smart Tasks...")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    smart_tasks_ui(email)