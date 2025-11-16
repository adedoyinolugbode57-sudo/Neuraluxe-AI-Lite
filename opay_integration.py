"""
Neuraluxe-AI Opay Integration
-----------------------------
Handles payment processing and premium subscription unlocking.
Simulated for now with auto-unlock. Ready for live Opay API hooks.
"""

from config import (
    OPAY_ACCOUNT_NUMBER,
    OPAY_ACCOUNT_NAME,
    OPAY_CURRENCY,
    SUBSCRIPTION_AMOUNT_NGN,
    AUTO_UNLOCK,
    REQUIRE_PROOF,
    record_payment,
    is_premium,
    unlock_subscription
)

import datetime

# -----------------------------
# Payment Simulation
# -----------------------------
def simulate_payment(user_email, amount_ngn):
    """
    Simulate a user payment.
    In production, connect here to Opay API or webhook.
    """
    print(f"Simulating payment of {amount_ngn} {OPAY_CURRENCY} from {user_email}...")
    
    # Record the payment
    record_payment(user_email, amount_ngn)
    
    # Auto-unlock if enabled
    if AUTO_UNLOCK:
        print("Auto-unlock enabled. Granting premium access...")
    else:
        print("Payment recorded, waiting for manual verification.")
    
    return True

# -----------------------------
# Check Subscription Status
# -----------------------------
def check_user_subscription(user_email):
    """
    Returns True if user has premium access, False otherwise.
    """
    premium = is_premium(user_email)
    if premium:
        print(f"✅ {user_email} has premium access.")
    else:
        print(f"❌ {user_email} does NOT have premium access.")
    return premium

# -----------------------------
# Manual Unlock Option
# -----------------------------
def manual_unlock(user_email):
    """
    For admin use: manually grant premium access.
    """
    success = unlock_subscription(user_email)
    if success:
        print(f"✅ {user_email} manually unlocked for premium access.")
    else:
        print(f"❌ No payment record found for {user_email}.")
    return success

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter user email: ").strip()
    check_user_subscription(email)
    
    choice = input("Do you want to simulate payment now? (y/n): ").strip().lower()
    if choice == "y":
        simulate_payment(email, SUBSCRIPTION_AMOUNT_NGN)
        check_user_subscription(email)
    
    admin_choice = input("Do you want to manually unlock subscription? (y/n): ").strip().lower()
    if admin_choice == "y":
        manual_unlock(email)
        check_user_subscription(email)