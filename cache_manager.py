"""
Neuraluxe-AI Enhanced Cache Manager
-----------------------------------
- Thread-safe cache operations
- TTL-based expiry
- Automatic background cleanup
- Feature usage tracking
- Full debug and inspection tools
"""

import time
import threading

# -------------------------
# Cache Stores & Lock
# -------------------------
cache_store = {}
expiry_store = {}
lock = threading.Lock()
cleanup_interval = 60  # seconds for auto cleanup

# -------------------------
# Core Cache Functions
# -------------------------
def set_cache(key, value, ttl=None):
    """Set a cache key with optional TTL (seconds)."""
    with lock:
        cache_store[key] = value
        if ttl:
            expiry_store[key] = time.time() + ttl
        elif key in expiry_store:
            del expiry_store[key]
    print(f"[CACHE] Set key '{key}' with ttl={ttl}")

def get_cache(key):
    with lock:
        if key in expiry_store and time.time() > expiry_store[key]:
            delete_cache(key)
            print(f"[CACHE] Key '{key}' expired")
            return None
        return cache_store.get(key)

def delete_cache(key):
    with lock:
        cache_store.pop(key, None)
        expiry_store.pop(key, None)
    print(f"[CACHE] Deleted key '{key}'")

def clear_cache():
    with lock:
        cache_store.clear()
        expiry_store.clear()
    print("[CACHE] Cleared all cache")

# -------------------------
# Feature Usage Tracking
# -------------------------
def increment_feature_usage(user_email, feature_name):
    key = f"{user_email}:{feature_name}"
    current = get_cache(key) or 0
    set_cache(key, current + 1, ttl=86400)  # daily reset
    return current + 1

def get_feature_usage(user_email, feature_name):
    key = f"{user_email}:{feature_name}"
    return get_cache(key) or 0

def can_use_feature(user_email, feature_name, limit=2):
    usage = get_feature_usage(user_email, feature_name)
    if usage >= limit:
        print(f"[LIMIT] {user_email} reached {limit} uses for {feature_name}")
        return False
    increment_feature_usage(user_email, feature_name)
    return True

# -------------------------
# Cache Cleanup
# -------------------------
def cleanup_expired():
    """Remove expired keys safely."""
    with lock:
        now = time.time()
        keys_to_delete = [k for k, v in expiry_store.items() if now > v]
        for k in keys_to_delete:
            delete_cache(k)
    print(f"[CACHE] Cleanup done, {len(keys_to_delete)} keys removed")

def start_auto_cleanup(interval=cleanup_interval):
    """Start background thread for automatic cleanup."""
    def run_cleanup():
        while True:
            time.sleep(interval)
            cleanup_expired()
    t = threading.Thread(target=run_cleanup, daemon=True)
    t.start()
    print(f"[CACHE] Auto cleanup thread started (interval={interval}s)")

# -------------------------
# Debug & Inspection
# -------------------------
def show_cache():
    with lock:
        print("\n[CACHE STORE]")
        for k, v in cache_store.items():
            exp = expiry_store.get(k, "Permanent")
            print(f"{k}: {v} (expires: {exp})")

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    start_auto_cleanup()
    set_cache("greeting", "Hello Neuraluxe!", ttl=5)
    print("Retrieved:", get_cache("greeting"))
    time.sleep(6)
    print("After TTL:", get_cache("greeting"))
    set_cache("temp", {"data": 123})
    print("Feature Usage Test:", can_use_feature("user@example.com", "New Chat", limit=2))
    show_cache()