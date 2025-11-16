"""
Neuraluxe-AI API Helpers
-------------------------
- Lightweight web search simulation
- Handles query caching
- Returns simulated links
- Modular for Web Search tab
"""

from cache_manager import get_cache, set_cache
import urllib.parse
import time

# -------------------------
# Web Search Simulation
# -------------------------
def search_web(query, user_email=None):
    """
    Returns list of simulated links for a query
    """
    cache_key = f"search:{query}"
    cached = get_cache(cache_key)
    if cached:
        print("[WEB] Returning cached search results")
        return cached

    # Simulate search results
    query_encoded = urllib.parse.quote_plus(query)
    results = [
        f"https://www.google.com/search?q={query_encoded}",
        f"https://www.bing.com/search?q={query_encoded}",
        f"https://github.com/search?q={query_encoded}",
        f"https://stackoverflow.com/search?q={query_encoded}",
        f"https://www.reddit.com/search?q={query_encoded}"
    ]

    # Store in cache for 10 minutes
    set_cache(cache_key, results, ttl=600)
    print(f"[WEB] Cached search results for '{query}'")
    return results

# -------------------------
# Example API Request (Lightweight)
# -------------------------
def fetch_json_placeholder(resource):
    """
    Simulate API JSON fetch without real external request
    """
    time.sleep(0.1)  # simulate latency
    print(f"[API] Fetched resource '{resource}'")
    return {"resource": resource, "data": "Sample Data"}

# -------------------------
# Multi-query Batch Search
# -------------------------
def batch_search(queries, user_email=None):
    all_results = {}
    for q in queries:
        all_results[q] = search_web(q, user_email=user_email)
    return all_results

# -------------------------
# Debug / Standalone Test
# -------------------------
if __name__ == "__main__":
    queries = ["neuraluxe ai", "python tutorials"]
    results = batch_search(queries, user_email="test@example.com")
    for q, r in results.items():
        print(f"\nResults for '{q}':")
        for link in r:
            print(link)