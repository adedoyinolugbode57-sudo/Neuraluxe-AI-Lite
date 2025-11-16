"""
Neuraluxe-AI TTS Logic
----------------------
- Lightweight Text-to-Speech simulation
- Premium/free access management
- Voice selection, caching, and logging
"""

from cache_manager import get_cache, set_cache
from session_manager import is_free_user
import time

AVAILABLE_VOICES = ["polite_male", "cheerful_female", "neutral", "robotic", "soft_female", "deep_male"]

# -------------------------
# TTS Engine Simulation
# -------------------------
def speak_text(user_email, text, voice="polite_male"):
    if voice not in AVAILABLE_VOICES:
        voice = "polite_male"

    if is_free_user(user_email):
        # Free users hear a limited preview
        text = text[:50] + "..." if len(text) > 50 else text

    # Cache recent TTS output for performance
    cache_key = f"tts:{user_email}:{text[:30]}"
    cached_audio = get_cache(cache_key)
    if cached_audio:
        print(f"[TTS] Playing cached audio: '{cached_audio}'")
        return cached_audio

    # Simulate TTS processing
    audio_sim = f"[{voice.upper()} TTS] {text}"
    time.sleep(0.05 * len(text.split()))  # simulate processing
    set_cache(cache_key, audio_sim, ttl=3600)
    print(f"[TTS] {audio_sim}")
    return audio_sim

# -------------------------
# Voice Management
# -------------------------
def list_available_voices(user_email):
    if is_free_user(user_email):
        # Limit free users to 2 voices
        return AVAILABLE_VOICES[:2]
    return AVAILABLE_VOICES

def select_voice(user_email, voice_name):
    voices = list_available_voices(user_email)
    if voice_name in voices:
        print(f"[TTS] {user_email} selected voice '{voice_name}'")
        return voice_name
    print(f"[TTS] Voice '{voice_name}' not available for {user_email}")
    return voices[0]

# -------------------------
# TTS Logging
# -------------------------
def log_tts_usage(user_email, text, voice):
    print(f"[TTS LOG] {user_email} used voice '{voice}' for text: {text[:50]}...")

# -------------------------
# Batch TTS
# -------------------------
def batch_speak(user_email, texts, voice="polite_male"):
    results = []
    for t in texts:
        res = speak_text(user_email, t, voice)
        results.append(res)
        log_tts_usage(user_email, t, voice)
    return results

# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    email = input("Enter email: ").strip()
    voice = select_voice(email, "cheerful_female")
    speak_text(email, "Welcome to Neuraluxe-AI, your premium AI assistant!", voice)
    batch_speak(email, ["Mini-games ready!", "Analytics loaded!", "Enjoy your session!"], voice)