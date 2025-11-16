"""
online_fetcher.py
-----------------
Neuraluxe-AI Online Content Fetcher
- Lightweight, independent module
- Fetches jokes, quotes, and word definitions online
- Can be used in chat or Home tab
"""

import requests
import random

# -------------------------
# Fetch Online JSON
# -------------------------
def fetch_json(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# -------------------------
# Fetch a random joke
# -------------------------
def get_joke():
    data = fetch_json("https://official-joke-api.appspot.com/random_joke")
    if data:
        return f"{data.get('setup','')} ... {data.get('punchline','')}"
    return "Why did the AI cross the road? To compute the other side!"

# -------------------------
# Fetch a random inspirational quote
# -------------------------
def get_quote():
    data = fetch_json("https://type.fit/api/quotes")
    if data and isinstance(data, list):
        choice_quote = random.choice(data)
        return choice_quote.get("text", "Keep learning and stay curious!")
    return "Keep learning and stay curious!"

# -------------------------
# Fetch word definition
# -------------------------
def define_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    data = fetch_json(url)
    if data and isinstance(data, list):
        meanings = data[0].get("meanings", [])
        if meanings:
            definition = meanings[0]["definitions"][0].get("definition", "Definition not found.")
            return f"{word.capitalize()}: {definition}"
    return f"{word.capitalize()}: Definition not found."

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    print("Select an option:")
    print("1. Joke\n2. Quote\n3. Define a word\n4. Exit")
    while True:
        choice = input("Option: ").strip()
        if choice == "1":
            print("🤖 Joke:", get_joke())
        elif choice == "2":
            print("💡 Quote:", get_quote())
        elif choice == "3":
            word = input("Enter word: ").strip()
            print("📖 Definition:", define_word(word))
        elif choice == "4":
            print("Exiting online fetcher...")
            break
        else:
            print("Invalid option.")