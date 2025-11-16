# chat_online.py
# -----------------------------
# Lightweight online info fetcher for Neuraluxe-AI
# Uses public APIs or web scraping for quick, small responses
# Minimal dependencies: requests, built-in json
# -----------------------------
import requests
from urllib.parse import quote_plus

def fetch_wiki_summary(query, sentences=2):
    """Fetch a brief Wikipedia summary for a query"""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}"
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("extract", "No summary found.")[:500]
    except:
        return "Could not fetch online info."
    return "No data available."

def fetch_quote(topic="inspire"):
    """Fetch a quick quote from quotable.io"""
    try:
        url = f"https://api.quotable.io/random?tags={quote_plus(topic)}"
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            return f'"{data["content"]}" — {data["author"]}'
    except:
        return "No quote available."

def fetch_online_info(message):
    """
    Lightweight online augmentation:
    - For factual questions, returns wiki summary
    - For motivational/fun prompts, returns quotes
    """
    message_lower = message.lower()
    if any(word in message_lower for word in ["what", "who", "when", "where", "how"]):
        return fetch_wiki_summary(message)
    elif any(word in message_lower for word in ["motivate", "inspire", "quote", "advice"]):
        return fetch_quote()
    return None