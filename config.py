# config.py
# -----------------------------
# Neuraluxe-AI Lightweight Config Loader
# -----------------------------

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# -----------------------------
# Payment Settings
# -----------------------------
OPAY_ACCOUNT_NUMBER = os.getenv("OPAY_ACCOUNT_NUMBER")
OPAY_ACCOUNT_NAME = os.getenv("OPAY_ACCOUNT_NAME")
OPAY_CURRENCY = os.getenv("OPAY_CURRENCY")
SUBSCRIPTION_AMOUNT_NGN = int(os.getenv("SUBSCRIPTION_AMOUNT_NGN", 12900))
AUTO_UNLOCK = os.getenv("AUTO_UNLOCK", "True") == "True"
REQUIRE_PROOF = os.getenv("REQUIRE_PROOF", "False") == "True"

# -----------------------------
# User & Chat Settings
# -----------------------------
USERS_JSON = os.getenv("USERS_JSON", "users.json")
CHAT_HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", 100))
DAILY_USAGE_LIMIT = int(os.getenv("DAILY_USAGE_LIMIT", 30))

# -----------------------------
# Online Source Endpoints
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT5_API_URL = os.getenv("GPT5_API_URL")
NEURALUXE_KNOWLEDGE_BASE = os.getenv("NEURALUXE_KNOWLEDGE_BASE")
NEWS_API_ENDPOINT = os.getenv("NEWS_API_ENDPOINT")
JOKES_API_ENDPOINT = os.getenv("JOKES_API_ENDPOINT")
QUOTES_API_ENDPOINT = os.getenv("QUOTES_API_ENDPOINT")
WIKIPEDIA_API_ENDPOINT = os.getenv("WIKIPEDIA_API_ENDPOINT")

# -----------------------------
# Misc
# -----------------------------
VOICE_ASSISTANT_MALE = os.getenv("VOICE_ASSISTANT_MALE", "polite_male")
VOICE_ASSISTANT_FEMALE = os.getenv("VOICE_ASSISTANT_FEMALE", "cheerful_female")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", 5))
CACHE_EXPIRY_SECONDS = int(os.getenv("CACHE_EXPIRY_SECONDS", 3600))