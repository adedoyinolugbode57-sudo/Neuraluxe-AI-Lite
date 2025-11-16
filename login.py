"""
Neuraluxe-AI Login Module
-------------------------
- Handles user login
- Checks subscription status
- Supports premium flow ($6.99)
"""

import os
from getpass import getpass
from subscription_manager import check_subscription, activate_subscription

# Dummy users database (replace with your actual users.json or DB)
USERS_DB = {
    "user@example.com": {"password": "password123", "tier": "free"},
    "premium@example.com": {"password": "premium456", "tier": "premium"}
}

def login():
    print("\n=== Neuraluxe-AI Login ===")
    email = input("Email: ").strip()
    password = getpass("Password: ").strip()

    user = USERS_DB.get(email)
    if not user or user["password"] != password:
        print("❌ Invalid email or password.")
        return login()  # Retry login

    # Check subscription status
    active, msg = check_subscription(email)
    if not active:
        print(f"⚠️ {msg}")
        choice = input("Activate premium subscription for $6.99? (y/n): ").strip().lower()
        if choice == "y":
            success, msg = activate_subscription(email)
            if success:
                print(f"✅ {msg}")
                USERS_DB[email]["tier"] = "premium"
        else:
            print("Continuing with free tier.")

    print(f"✅ Logged in as {email} (Tier: {USERS_DB[email]['tier']})")
    return {"email": email, "tier": USERS_DB[email]["tier"]}

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    user_info = login()
    print(f"Welcome {user_info['email']}! Tier: {user_info['tier']}")