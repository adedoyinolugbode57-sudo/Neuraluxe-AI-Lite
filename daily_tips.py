"""
daily_tips.py
-------------
Neuraluxe-AI Daily Tips & Suggestions
- Lightweight and independent
- Generates daily actionable tips for users
- Can be integrated into Home tab or Chat
"""

import json
import os
import random
from datetime import datetime

TIPS_JSON = "user_tips.json"

# -------------------------
# Load & Save Tips
# -------------------------
def load_user_tips():
    if not os.path.exists(TIPS_JSON):
        with open(TIPS_JSON, "w") as f:
            json.dump({}, f)
    with open(TIPS_JSON, "r") as f:
        return json.load(f)

def save_user_tips(data):
    with open(TIPS_JSON, "w") as f:
        json.dump(data, f, indent=2)

# -------------------------
# Default Tip Pool
# -------------------------
DEFAULT_TIPS = [
    "Try asking the AI for a motivational quote today.",
    "Check the mini games and play your favorite.",
    "Review your recent chats for insights.",
    "Explore Novel Hub and start a story.",
    "Update your profile settings for better personalization.",
    "Test voice assistant with a fun command.",
    "Explore analytics trends for today.",
    "Visit Assets Hub for creative inspiration.",
    "Connect with community members.",
    "Create a new game idea in 'Create Game' tab."
]

# -------------------------
# Generate Daily Tip
# -------------------------
def generate_daily_tip(user_email):
    tips_data = load_user_tips()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Check if user already has a tip for today
    user_daily = tips_data.get(user_email, {})
    if user_daily.get("date") == today_str:
        return user_daily.get("tip")
    
    # Pick a new tip randomly
    tip = random.choice(DEFAULT_TIPS)
    tips_data[user_email] = {"date": today_str, "tip": tip}
    save_user_tips(tips_data)
    return tip

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    tip = generate_daily_tip(email)
    print(f"💡 Daily Tip for {email}:\n{tip}")