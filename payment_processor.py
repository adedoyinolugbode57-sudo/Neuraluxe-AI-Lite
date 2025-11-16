"""
Neuraluxe-AI Payment Processor
-------------------------------
Handles subscription charges via Opay
"""

import os
import requests

# -----------------------------
# Load environment variables
# -----------------------------
SUBSCRIPTION_PRICE = float(os.getenv("SUBSCRIPTION_PRICE", 6.99))
CURRENCY = os.getenv("CURRENCY", "USD")
PAYMENT_GATEWAY_URL = os.getenv("PAYMENT_GATEWAY_URL")
RECIPIENT_PHONE = os.getenv("RECIPIENT_PHONE")
RECIPIENT_NAME = os.getenv("RECIPIENT_NAME")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")  # Opay secret

# -----------------------------
# Payment Function
# -----------------------------
def charge_user(user_email):
    """
    Charge the user for premium subscription
    """
    payload = {
        "email": user_email,
        "amount": SUBSCRIPTION_PRICE,
        "currency": CURRENCY,
        "description": "Neuraluxe-AI Premium Subscription",
        "recipient_phone": RECIPIENT_PHONE,
        "recipient_name": RECIPIENT_NAME
    }

    headers = {
        "Authorization": f"Bearer {PAYMENT_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(PAYMENT_GATEWAY_URL, json=payload, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return True, data
        else:
            return False, {"error": resp.text}
    except Exception as e:
        return False, {"error": str(e)}

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    test_email = input("Enter user email: ").strip()
    success, response = charge_user(test_email)
    if success:
        print(f"✅ Payment successful: {response}")
    else:
        print(f"❌ Payment failed: {response}")