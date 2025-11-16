"""
Neuraluxe-AI Insight Analyzer
-----------------------------
- Analyze text, habits, and user input
- Lightweight and premium-rich
- Free vs Paid user logic
- Recent insights and summaries
- Quick tips and logging
"""

import json
import os
from datetime import datetime
from random import choice, randint
from session_manager import FREE_USER_EMAIL, is_free_user

# -----------------------------
# Configurations
# -----------------------------
INSIGHTS_JSON = "insights.json"

# Sample insight templates
INSIGHT_TEMPLATES = [
    "Your recent activity shows consistent engagement in {}.",
    "You tend to focus on {} more often.",
    "A pattern suggests improvement in {} over the last week.",
    "Your favorite topics seem to be {}.",
    "You might want to explore {} for better results."
]

TOPICS = [
    "AI learning", "novel reading", "creative writing", "productivity",
    "mindfulness", "coding practice", "language learning", "gaming",
    "music", "brain teasers"
]

# -----------------------------
# Helper Functions
# -----------------------------
def load_insights():
    if not os.path.exists(INSIGHTS_JSON):
        with open(INSIGHTS_JSON, "w") as f:
            json.dump({}, f)
    with open(INSIGHTS_JSON, "r") as f:
        return json.load(f)

def save_insights(data):
    with open(INSIGHTS_JSON, "w") as f:
        json.dump(data, f, indent=2)

def log_activity(user_email, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} - {user_email} - {action}")

# -----------------------------
# Generate Insight
# -----------------------------
def generate_insight(user_email, full_access_user):
    topic = choice(TOPICS)
    template = choice(INSIGHT_TEMPLATES)

    insight_text = template.format(topic)
    if is_free_user(user_email) and not full_access_user:
        # Limit free users to preview only
        insight_text = insight_text[:50] + "..."
    
    # Save insight
    data = load_insights()
    user_data = data.setdefault(user_email, [])
    user_data.append({
        "insight": insight_text,
        "topic": topic,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_insights(data)
    log_activity(user_email, f"Generated insight on '{topic}'")
    print(f"\n💡 Insight: {insight_text}\n")

# -----------------------------
# Recent Insights
# -----------------------------
def view_recent_insights(user_email):
    data = load_insights()
    user_data = data.get(user_email, [])
    print("\n📊 Recent Insights:")
    if not user_data:
        print("- No insights generated yet.")
        return
    for idx, insight in enumerate(user_data[-5:], 1):
        print(f"{idx}. [{insight['timestamp']}] {insight['insight']}")
    print()

# -----------------------------
# Quick Tips
# -----------------------------
def display_quick_tips():
    tips = [
        "Generate insights to track your AI habits.",
        "Free users get limited insight previews.",
        "Use patterns from insights to improve productivity.",
        "Check recent insights regularly to spot trends.",
        "Combine with Novel Hub for content analysis.",
        "Focus on a topic to get detailed analysis."
    ]
    print("\n✨ Insight Analyzer Tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    print()

# -----------------------------
# Insight Analyzer Main UI
# -----------------------------
def insight_analyzer_ui(user_email):
    full_access_user = (user_email == FREE_USER_EMAIL or not is_free_user(user_email))
    
    print("\n==============================")
    print("      INSIGHT ANALYZER        ")
    print("==============================\n")

    display_quick_tips()
    view_recent_insights(user_email)

    while True:
        print("Options:")
        print("1. Generate Insight")
        print("2. View Recent Insights")
        print("3. Exit Insight Analyzer")
        choice = input("Select option: ").strip()

        if choice == "1":
            generate_insight(user_email, full_access_user)
        elif choice == "2":
            view_recent_insights(user_email)
        elif choice == "3":
            log_activity(user_email, "Closed Insight Analyzer")
            print("Exiting Insight Analyzer...\n")
            break
        else:
            print("Invalid option. Try again.")

# -----------------------------
# Standalone Test
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    insight_analyzer_ui(email)