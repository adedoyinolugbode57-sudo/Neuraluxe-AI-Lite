"""
Neuraluxe-AI Helpers
--------------------
- General utility functions for all tabs
- Lightweight and premium-ready
"""

import random, string, time

# -------------------------
# Random ID Generator
# -------------------------
def generate_id(prefix="", length=8):
    chars = string.ascii_lowercase + string.digits
    rand_str = ''.join(random.choice(chars) for _ in range(length))
    return f"{prefix}_{rand_str}" if prefix else rand_str

# -------------------------
# Timestamp Helpers
# -------------------------
def current_timestamp():
    return int(time.time())

# -------------------------
# Text Utilities
# -------------------------
def truncate_text(text, max_len=100):
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."

def format_text_list(items):
    return ", ".join(str(i) for i in items)

# -------------------------
# Color & Theme Utilities
# -------------------------
THEMES = ["default", "neon", "dark", "light", "blue", "green", "purple"]

def validate_theme(theme_name):
    return theme_name if theme_name in THEMES else "default"

# -------------------------
# Mini-Game Helpers
# -------------------------
def random_score(min_score=0, max_score=100):
    return random.randint(min_score, max_score)

def random_choice(options):
    return random.choice(options)

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    print("Generated ID:", generate_id("game"))
    print("Current Timestamp:", current_timestamp())
    print("Truncated Text:", truncate_text("This is a very long text that needs truncation.", 30))
    print("Theme Validation:", validate_theme("neon"))
    print("Random Score:", random_score())
    print("Random Choice:", random_choice([1,2,3,4]))