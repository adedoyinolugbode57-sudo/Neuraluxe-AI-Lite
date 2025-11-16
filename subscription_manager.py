"""
Neuraluxe-AI Subscription Manager
---------------------------------
Handles premium subscriptions, checks, and unlocks.
"""

import json
import os
from datetime import datetime, timedelta

USERS_JSON = "users.json"  # Local storage for demo
PAYMENTS_JSON = "payments.json"  # Records all payments

# -----------------------------
# Subscription Configuration
# -----------------------------
LIFETIME_SUBSCRIPTION = True  # All users get lifetime once unlocked

# -----------------------------
# Load / Save Functions
# -----------------------------
def load_users():
    if not os.path.exists(USERS_JSON):
        with open(USERS_JSON, "w") as f:
            json.dump({}, f)
    with open(USERS_JSON, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_JSON, "w") as f:
        json.dump(users, f, indent=2)

def load_payments():
    if not os.path.exists(PAYMENTS_JSON):
        with open(PAYMENTS_JSON, "w") as f:
            json.dump({}, f)
    with open(PAYMENTS_JSON, "r") as f:
        return json.load(f)

def save_payments(payments):
    with open(PAYMENTS_JSON, "w") as f:
        json.dump(payments, f, indent=2)

# -----------------------------
# Payment Recording
# -----------------------------
def record_payment(user_email, amount_ngn):
    payments = load_payments()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payments[user_email] = {
        "amount_ngn": amount_ngn,
        "timestamp": now,
        "verified": True  # Auto-verified for now
    }
    save_payments(payments)
    print(f"💰 Payment recorded for {user_email} at {now}")
    return True

# -----------------------------
# Unlock Subscription
# -----------------------------
def unlock_subscription(user_email):
    users = load_users()
    payments = load_payments()
    
    if user_email not in payments:
        print("❌ No payment found. Cannot unlock.")
        return False
    
    users[user_email] = users.get(user_email, {})
    users[user_email]["premium"] = True
    if LIFETIME_SUBSCRIPTION:
        users[user_email]["expiry"] = "lifetime"
    else:
        expiry = datetime.now() + timedelta(days=30)
        users[user_email]["expiry"] = expiry.isoformat()
    
    save_users(users)
    print(f"✅ {user_email} has been granted premium access.")
    return True

# -----------------------------
# Check Subscription Status
# -----------------------------
def is_premium(user_email):
    users = load_users()
    user_data = users.get(user_email, {})
    if user_data.get("premium"):
        if user_data.get("expiry") == "lifetime":
            return True
        expiry = datetime.fromisoformat(user_data.get("expiry"))
        if datetime.now() <= expiry:
            return True
        else:
            # Expired subscription
            users[user_email]["premium"] = False
            save_users(users)
            return False
    return False

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter user email: ").strip()
    
    if is_premium(email):
        print(f"✅ {email} already has premium access.")
    else:
        print(f"❌ {email} does not have premium access yet.")
        choice = input("Simulate payment now? (y/n): ").strip().lower()
        if choice == "y":
            from opay_integration import simulate_payment
            simulate_payment(email, 12500)  # NGN approx for $6.99
            unlock_subscription(email)
        elif choice == "n":
            print("No subscription granted.")