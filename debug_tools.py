"""
Neuraluxe-AI Debug Tools
------------------------
- Safe, automatic logging system
- Auto-creates debug_tools.json if missing
- View, clear, and export logs
- Lightweight and Render-ready
"""

import json
import os
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
DEBUG_FILE = "debug_tools.json"

# Default structure
DEFAULT_DATA = {
    "console_logs_enabled": True,
    "max_entries": 100,
    "logs": []
}

# -----------------------------
# Core Functions
# -----------------------------
def load_debug_data():
    """Load or create the debug JSON file"""
    if not os.path.exists(DEBUG_FILE):
        with open(DEBUG_FILE, "w") as f:
            json.dump(DEFAULT_DATA, f, indent=2)
    with open(DEBUG_FILE, "r") as f:
        return json.load(f)

def save_debug_data(data):
    """Save current debug data"""
    with open(DEBUG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_event(event_type, message):
    """Log an event with timestamp"""
    data = load_debug_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"timestamp": timestamp, "type": event_type, "message": message}

    data["logs"].append(entry)
    if len(data["logs"]) > data.get("max_entries", 100):
        data["logs"] = data["logs"][-data["max_entries"]:]

    save_debug_data(data)
    if data.get("console_logs_enabled", True):
        print(f"[{timestamp}] ({event_type}) {message}")

def clear_logs():
    """Clear all logs"""
    data = load_debug_data()
    data["logs"] = []
    save_debug_data(data)
    print("✅ All debug logs cleared.")

def export_logs(filename="debug_export.json"):
    """Export logs to external file"""
    data = load_debug_data()
    with open(filename, "w") as f:
        json.dump(data["logs"], f, indent=2)
    print(f"📤 Logs exported to {filename}")

def show_recent_logs(limit=10):
    """Show recent logs"""
    data = load_debug_data()
    logs = data.get("logs", [])[-limit:]
    print(f"\n🧠 Recent Logs (last {limit}):")
    for log in logs:
        print(f"[{log['timestamp']}] {log['type']} - {log['message']}")
    print()

# -----------------------------
# Standalone Debug Menu
# -----------------------------
def debug_ui():
    print("\n==============================")
    print("        DEBUG TOOLS MENU      ")
    print("==============================\n")

    while True:
        print("1. Log Test Event")
        print("2. View Recent Logs")
        print("3. Clear Logs")
        print("4. Export Logs")
        print("5. Exit Debug Tools")

        choice = input("Select option: ").strip()
        if choice == "1":
            msg = input("Enter test message: ").strip() or "Test event"
            log_event("INFO", msg)
        elif choice == "2":
            show_recent_logs()
        elif choice == "3":
            clear_logs()
        elif choice == "4":
            export_logs()
        elif choice == "5":
            print("Exiting Debug Tools...\n")
            break
        else:
            print("Invalid option. Try again.\n")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    debug_ui()