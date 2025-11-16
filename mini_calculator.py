"""
Neuraluxe-AI: Mini Calculator Module
------------------------------------
- Lightweight, premium-rich calculator
- Basic arithmetic + advanced operations
- Tracks history and memory for users
- Modular and deployable
"""

import json
import os
from datetime import datetime
import math

# -----------------------------
# Config & Storage
# -----------------------------
CALC_HISTORY_FILE = "calc_history.json"

def load_history():
    if not os.path.exists(CALC_HISTORY_FILE):
        with open(CALC_HISTORY_FILE, "w") as f:
            json.dump({}, f)
    with open(CALC_HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(data):
    with open(CALC_HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# Logging
# -----------------------------
def log_calc_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[CALC] {timestamp} - {user_email} - {action}")

# -----------------------------
# Memory System
# -----------------------------
def save_memory(user_email, key, value):
    data = load_history()
    user_mem = data.setdefault(user_email, {}).setdefault("memory", {})
    user_mem[key] = value
    save_history(data)
    log_calc_activity(user_email, f"Saved memory '{key}' = {value}")

def recall_memory(user_email, key):
    data = load_history()
    return data.get(user_email, {}).get("memory", {}).get(key)

# -----------------------------
# Calculator Functions
# -----------------------------
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Division by zero"

def power(a, b):
    return a ** b

def sqrt(a):
    try:
        return math.sqrt(a)
    except ValueError:
        return "Error: Invalid input"

def factorial(a):
    try:
        return math.factorial(a)
    except ValueError:
        return "Error: Invalid input"

# -----------------------------
# Advanced Functions
# -----------------------------
def percentage(a, b):
    return (a / b) * 100 if b != 0 else "Error: Division by zero"

def log_base(a, base):
    try:
        return math.log(a, base)
    except ValueError:
        return "Error: Invalid input"

def sine(a):
    return math.sin(math.radians(a))

def cosine(a):
    return math.cos(math.radians(a))

def tangent(a):
    try:
        return math.tan(math.radians(a))
    except ValueError:
        return "Error: Invalid input"

# -----------------------------
# History System
# -----------------------------
def add_to_history(user_email, operation, result):
    data = load_history()
    user_hist = data.setdefault(user_email, {}).setdefault("history", [])
    entry = {
        "operation": operation,
        "result": result,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    user_hist.append(entry)
    save_history(data)
    log_calc_activity(user_email, f"Performed '{operation}' = {result}")

def view_history(user_email, last_n=5):
    data = load_history()
    user_hist = data.get(user_email, {}).get("history", [])
    if not user_hist:
        print("No history available.")
        return
    print(f"\n--- Last {last_n} Calculations ---")
    for entry in user_hist[-last_n:]:
        print(f"{entry['timestamp']} | {entry['operation']} = {entry['result']}")
    print()

# -----------------------------
# Quick Tips
# -----------------------------
def calculator_tips():
    tips = [
        "Use parentheses for complex calculations.",
        "You can store results in memory for later use.",
        "Advanced functions include sine, cosine, tangent, log, sqrt, and factorial.",
        "Free users have limited memory slots; premium users have unlimited."
    ]
    print("\n💡 Calculator Tips:")
    for idx, tip in enumerate(tips, 1):
        print(f"{idx}. {tip}")
    print()

# -----------------------------
# User Interface
# -----------------------------
def calculator_ui(user_email):
    print("\n==============================")
    print("        MINI CALCULATOR        ")
    print("==============================")
    log_calc_activity(user_email, "Opened Mini Calculator")

    calculator_tips()

    while True:
        print("\nOptions:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Power")
        print("6. Square Root")
        print("7. Factorial")
        print("8. Sine / Cosine / Tangent")
        print("9. Logarithm")
        print("10. Percentage")
        print("11. View History")
        print("12. Memory Recall")
        print("13. Exit Calculator")

        choice = input("Select option: ").strip()

        if choice == "1":
            a, b = float(input("Enter a: ")), float(input("Enter b: "))
            result = add(a, b)
            add_to_history(user_email, f"{a} + {b}", result)
        elif choice == "2":
            a, b = float(input("Enter a: ")), float(input("Enter b: "))
            result = subtract(a, b)
            add_to_history(user_email, f"{a} - {b}", result)
        elif choice == "3":
            a, b = float(input("Enter a: ")), float(input("Enter b: "))
            result = multiply(a, b)
            add_to_history(user_email, f"{a} * {b}", result)
        elif choice == "4":
            a, b = float(input("Enter a: ")), float(input("Enter b: "))
            result = divide(a, b)
            add_to_history(user_email, f"{a} / {b}", result)
        elif choice == "5":
            a, b = float(input("Enter base: ")), float(input("Enter exponent: "))
            result = power(a, b)
            add_to_history(user_email, f"{a} ** {b}", result)
        elif choice == "6":
            a = float(input("Enter number: "))
            result = sqrt(a)
            add_to_history(user_email, f"sqrt({a})", result)
        elif choice == "7":
            a = int(input("Enter integer: "))
            result = factorial(a)
            add_to_history(user_email, f"factorial({a})", result)
        elif choice == "8":
            a = float(input("Enter degrees: "))
            print(f"Sine: {sine(a)}, Cosine: {cosine(a)}, Tangent: {tangent(a)}")
            add_to_history(user_email, f"sine/cosine/tangent({a})", f"{sine(a)}/{cosine(a)}/{tangent(a)}")
        elif choice == "9":
            a = float(input("Enter number: "))
            base = float(input("Enter base: "))
            result = log_base(a, base)
            add_to_history(user_email, f"log({a}, {base})", result)
        elif choice == "10":
            a, b = float(input("Enter part: ")), float(input("Enter whole: "))
            result = percentage(a, b)
            add_to_history(user_email, f"percentage({a}/{b})", result)
        elif choice == "11":
            view_history(user_email)
        elif choice == "12":
            key = input("Enter memory key: ").strip()
            val = recall_memory(user_email, key)
            print(f"Memory [{key}] = {val}")
        elif choice == "13":
            log_calc_activity(user_email, "Closed Mini Calculator")
            print("Exiting Calculator...")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    user_email = input("Enter your email: ").strip()
    calculator_ui(user_email)