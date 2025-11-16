# quiz_module.py
import random

quizzes = {
    "Math": [{"q": "2 + 2 = ?", "a": "4"}],
    "Science": [{"q": "H2O is?", "a": "Water"}]
}

def list_quizzes():
    print("Available Quiz Categories:")
    for idx, cat in enumerate(quizzes.keys(), 1):
        print(f"{idx}. {cat}")

def take_quiz(category):
    questions = quizzes.get(category)
    if not questions:
        print("Category not found.")
        return
    for q in questions:
        answer = input(q["q"] + " ")
        if answer.strip().lower() == q["a"].lower():
            print("✅ Correct!")
        else:
            print(f"❌ Wrong! Answer: {q['a']}")