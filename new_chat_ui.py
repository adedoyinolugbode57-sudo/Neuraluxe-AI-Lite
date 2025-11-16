"""
Neuraluxe-AI New Chat UI
------------------------
- Lightweight chat interface
- GPT-style bubbles
- Supports free vs premium users
- 100-message session limit
"""

from ai_engine import ai_response
from session_manager import FREE_USER_EMAIL, is_free_user

MAX_MESSAGES = 100  # Max messages per session for non-premium users

def new_chat_ui(user_email):
    full_access_user = (user_email == FREE_USER_EMAIL)
    message_count = 0

    print("\n--- Welcome to Neuraluxe-AI Chat ---")
    print("Type 'exit' or 'quit' to leave the chat.\n")

    while True:
        if not full_access_user and message_count >= MAX_MESSAGES:
            print("\n⚠️  You have reached 100 messages. Wait 12 hours or upgrade for unlimited access.")
            break

        prompt = input("You: ").strip()
        if prompt.lower() in ["exit", "quit"]:
            print("Exiting Neuraluxe-AI Chat...")
            break

        reply = ai_response(user_email, prompt)
        print("\nNeuraluxe-AI:\n" + reply)
        
        if not full_access_user:
            message_count += 1
            print(f"\nMessages left before lock: {MAX_MESSAGES - message_count}")

# -------------------------
# Standalone test
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    new_chat_ui(email)