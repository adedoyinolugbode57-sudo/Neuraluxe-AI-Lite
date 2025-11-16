# chat_cache.py
# -----------------------------
# Lightweight in-memory caching for chat responses
# Prevents recomputation for repeated messages
# TTL support for automatic expiration
# -----------------------------
import time

CHAT_CACHE = {}

def set_chat_cache(user_email, message, response, ttl=300):
    """Cache a response for a user message"""
    key = f"{user_email}:{message}"
    expire_at = time.time() + ttl
    CHAT_CACHE[key] = {"response": response, "expire_at": expire_at}
    # Optional debug
    # print(f"[CHAT CACHE] Cached '{message}' for {user_email} with TTL={ttl}s")

def get_chat_cache(user_email, message):
    """Retrieve cached response if valid"""
    key = f"{user_email}:{message}"
    entry = CHAT_CACHE.get(key)
    if entry:
        if time.time() < entry["expire_at"]:
            # print(f"[CHAT CACHE] Hit for '{message}'")
            return entry["response"]
        else:
            del CHAT_CACHE[key]
            # print(f"[CHAT CACHE] Expired '{message}'")
    return None

def cleanup_chat_cache():
    """Remove expired entries"""
    now = time.time()
    keys_to_remove = [k for k, v in CHAT_CACHE.items() if v["expire_at"] <= now]
    for k in keys_to_remove:
        del CHAT_CACHE[k]
    # print(f"[CHAT CACHE] Cleanup done, removed {len(keys_to_remove)} expired items")

def chat_cache_info():
    """Quick debug info"""
    total = len(CHAT_CACHE)
    expired = sum(1 for v in CHAT_CACHE.values() if v["expire_at"] <= time.time())
    return {"total_keys": total, "expired_keys": expired}