"""
Neuraluxe-AI Web Search Tab
---------------------------
- Lightweight, premium-rich
- Search links, quotes, jokes, word definitions
- Works without API keys
- Full access for adedoyinolugbode57@gmail.com
- Deployable and modular
"""

import json, random, time
from helpers import truncate_text
from session_manager import FREE_USER_EMAIL, is_free_user

# -------------------------
# File Storage
# -------------------------
CACHE_FILE = "web_cache.json"

# -------------------------
# Load / Save Cache
# -------------------------
def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

# -------------------------
# Simulated Search Data
# -------------------------
SAMPLE_LINKS = [
    "https://github.com",
    "https://stackoverflow.com",
    "https://wikipedia.org",
    "https://python.org",
    "https://realpython.com"
]

SAMPLE_QUOTES = [
    "Innovation distinguishes between a leader and a follower. – Steve Jobs",
    "The best way to predict the future is to invent it. – Alan Kay",
    "Dream big. Work hard. Stay focused.",
    "AI is the new electricity. – Andrew Ng",
    "Creativity is intelligence having fun. – Albert Einstein"
]

SAMPLE_JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs! 😅",
    "Why do Python programmers wear glasses? Because they can't C#!",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem."
]

SAMPLE_DEFINITIONS = {
    "Python": "Python is a high-level, interpreted programming language known for readability.",
    "AI": "Artificial Intelligence (AI) is intelligence demonstrated by machines.",
    "API": "Application Programming Interface allows communication between software components.",
    "JSON": "JSON is a lightweight data-interchange format."
}

# -------------------------
# Web Search UI
# -------------------------
def web_search_ui(user_email):
    full_access_user = (user_email == FREE_USER_EMAIL or not is_free_user(user_email))
    cache = load_cache()

    while True:
        print("\n--- Web Search Tab ---")
        print("1. Search Links")
        print("2. Get Quote")
        print("3. Get Joke")
        print("4. Word Definition")
        print("5. Exit Web Search")
        choice = input("Select option: ").strip()

        if choice == "1":
            search_links(user_email, cache)
        elif choice == "2":
            get_quote(user_email, cache)
        elif choice == "3":
            get_joke(user_email, cache)
        elif choice == "4":
            get_definition(user_email, cache)
        elif choice == "5":
            print("Exiting Web Search Tab...")
            save_cache(cache)
            break
        else:
            print("Invalid choice. Try again.")

# -------------------------
# Search Links
# -------------------------
def search_links(user_email, cache):
    query = input("Enter search query (keywords): ").strip().lower()
    if is_free_user(user_email):
        print("Limited search access for free users.")
    print("\nSearch Results:")
    results = random.sample(SAMPLE_LINKS, min(3, len(SAMPLE_LINKS)))
    for idx, link in enumerate(results, 1):
        print(f"{idx}. {truncate_text(link, 40)}")
    cache[query] = results

# -------------------------
# Get Random Quote
# -------------------------
def get_quote(user_email, cache):
    quote = random.choice(SAMPLE_QUOTES)
    print("\nQuote of the Moment:")
    print(quote)
    cache["last_quote"] = quote

# -------------------------
# Get Random Joke
# -------------------------
def get_joke(user_email, cache):
    joke = random.choice(SAMPLE_JOKES)
    print("\nHere's a Joke:")
    print(joke)
    cache["last_joke"] = joke

# -------------------------
# Word Definition
# -------------------------
def get_definition(user_email, cache):
    word = input("Enter word to define: ").strip()
    definition = SAMPLE_DEFINITIONS.get(word, "Definition not found in lightweight cache.")
    print(f"\n{word}: {definition}")
    cache[word] = definition

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    web_search_ui(email)