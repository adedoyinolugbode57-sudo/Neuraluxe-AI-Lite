# auth.py
from config import FREE_USER_EMAIL

def is_free_user(email):
    return email != FREE_USER_EMAIL

def is_premium_user(email):
    return email == FREE_USER_EMAIL

def login(email):
    print(f"Logging in: {email}")
    return {"email": email, "premium": is_premium_user(email)}

def logout(user):
    print(f"Logging out: {user['email']}")