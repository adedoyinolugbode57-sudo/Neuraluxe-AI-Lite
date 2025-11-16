"""
Neuraluxe-AI Cache Logic
------------------------
- Lightweight caching for improved performance
- TTL (time-to-live) support
- Free vs premium user optimizations
"""

import time

CACHE_STORE = {}

# -------------------------
# Set Cache
# -------------------------
def set_cache(key, value, ttl=3600):
    expire_at = time.time() + ttl
    CACHE_STORE[key] = {"value": value, "expire_at": expire_at}
    print(f"[CACHE] Key '{key}' set with TTL={ttl}s")

# -------------------------
# Get Cache
# -------------------------
def get_cache(key):
    entry = CACHE_STORE.get(key)
    if entry:
        if entry["expire_at"] > time.time():
            print(f"[CACHE] Key '{key}' retrieved")
            return entry["value"]
        else:
            print(f"[CACHE] Key '{key}' expired")
            del CACHE_STORE[key]
    return None

# -------------------------
# Delete Cache
# -------------------------
def delete_cache(key):
    if key in CACHE_STORE:
        del CACHE_STORE[key]
        print(f"[CACHE] Key '{key}' deleted")

# -------------------------
# Clear All Cache
# -------------------------
def clear_cache():
    CACHE_STORE.clear()
    print("[CACHE] All cache cleared")

# -------------------------
# Cache Info
# -------------------------
def cache_info():
    total = len(CACHE_STORE)
    expired = sum(1 for v in CACHE_STORE.values() if v["expire_at"] <= time.time())
    return {"total_keys": total, "expired_keys": expired}

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    set_cache("greeting", "Hello Neuraluxe!", ttl=10)
    print(get_cache("greeting"))
    time.sleep(11)
    print(get_cache("greeting"))
    set_cache("temp", "Test")
    print(cache_info())
    clear_cache()