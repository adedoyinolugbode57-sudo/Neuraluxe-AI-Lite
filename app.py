"""
Neuraluxe-AI Final Flask Entry Point
------------------------------------
Lightweight, production-ready, and tuned for 5k–10k users
Includes environment check endpoint for HostFlare deployment
"""

import os
import psutil
from flask import Flask, jsonify, abort
from translation_hub_full import smart_translate  # existing file
from session_manager import is_free_user  # existing file
import random

app = Flask(__name__)

# ----------------------------
# Safety & Performance Guard
# ----------------------------
@app.before_request
def prevent_overload():
    if psutil.cpu_percent() > 90 or psutil.virtual_memory().percent > 90:
        abort(503, "Server busy. Please try again soon.")

# ----------------------------
# Core Endpoints
# ----------------------------
@app.route('/')
def home():
    return "✨ Neuraluxe-AI is Live and Stable ✨"

@app.route('/health')
def health():
    """Quick uptime and resource check"""
    return jsonify({
        "status": "ok",
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent
    })

@app.route('/translate/<lang>/<text>')
def translate(lang, text):
    """Use your existing translation engine"""
    try:
        translated = smart_translate(text, lang)
        return jsonify({"original": text, "translated": translated})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mode')
def user_mode():
    """Check user tier (Free or Premium)"""
    mode = "Premium" if not is_free_user() else "Free"
    return jsonify({"user_mode": mode})

@app.route('/random')
def random_line():
    """Fun endpoint for testing responsiveness"""
    lines = [
        "Neuraluxe-AI never sleeps.",
        "Elegance in every response.",
        "Designed for 10k users — light as a feather.",
        "Precision, speed, and calm under load."
    ]
    return random.choice(lines)

# ----------------------------
# Environment Check Endpoint
# ----------------------------
@app.route('/env/check')
def env_check():
    """Verify environment variables are loaded correctly"""
    env_vars = {key: os.getenv(key, "Not Set") for key in os.environ.keys()}
    return jsonify({"env_summary": env_vars, "total_vars": len(env_vars)})

# ----------------------------
# Main Entry Point
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)