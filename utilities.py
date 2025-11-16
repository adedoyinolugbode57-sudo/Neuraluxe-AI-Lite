# utilities.py
import os

def ensure_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("{}")
        print(f"[UTIL] Created file: {file_path}")

def safe_input(prompt, default=""):
    response = input(prompt).strip()
    return response if response else default