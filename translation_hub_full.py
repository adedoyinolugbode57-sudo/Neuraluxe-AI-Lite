"""
translation_hub_full.py
-----------------------
- Full 100-language support
- User-specific language preferences
- Mid-chat dynamic switching
- Lightweight, premium-ready
"""

import json
import os
from googletrans import Translator

# -----------------------------
# Config
# -----------------------------
USER_LANG_FILE = "user_languages.json"
DEFAULT_LANGUAGE = "en"

# 100 supported languages
SUPPORTED_LANGUAGES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de",
    "Chinese (Simplified)": "zh-cn", "Chinese (Traditional)": "zh-tw", "Arabic": "ar",
    "Portuguese": "pt", "Italian": "it", "Russian": "ru", "Japanese": "ja",
    "Korean": "ko", "Turkish": "tr", "Dutch": "nl", "Polish": "pl",
    "Swedish": "sv", "Danish": "da", "Norwegian": "no", "Finnish": "fi",
    "Greek": "el", "Hebrew": "he", "Hindi": "hi", "Thai": "th", "Vietnamese": "vi",
    "Indonesian": "id", "Malay": "ms", "Czech": "cs", "Hungarian": "hu",
    "Romanian": "ro", "Slovak": "sk", "Bulgarian": "bg", "Croatian": "hr",
    "Serbian": "sr", "Lithuanian": "lt", "Latvian": "lv", "Estonian": "et",
    "Filipino": "tl", "Ukrainian": "uk", "Bengali": "bn", "Tamil": "ta",
    "Telugu": "te", "Marathi": "mr", "Gujarati": "gu", "Punjabi": "pa",
    "Malayalam": "ml", "Kannada": "kn", "Sinhala": "si", "Nepali": "ne",
    "Albanian": "sq", "Armenian": "hy", "Azerbaijani": "az", "Basque": "eu",
    "Belarusian": "be", "Bosnian": "bs", "Catalan": "ca", "Estonian": "et",
    "Georgian": "ka", "Haitian Creole": "ht", "Icelandic": "is", "Irish": "ga",
    "Kazakh": "kk", "Kyrgyz": "ky", "Latvian": "lv", "Lithuanian": "lt",
    "Luxembourgish": "lb", "Macedonian": "mk", "Maltese": "mt", "Mongolian": "mn",
    "Pashto": "ps", "Persian": "fa", "Quechua": "qu", "Sindhi": "sd",
    "Sinhala": "si", "Slovenian": "sl", "Somali": "so", "Swahili": "sw",
    "Tajik": "tg", "Turkmen": "tk", "Urdu": "ur", "Uzbek": "uz",
    "Welsh": "cy", "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu",
    "Corsican": "co", "Frisian": "fy", "Hausa": "ha", "Hawaiian": "haw",
    "Javanese": "jv", "Samoan": "sm", "Shona": "sn", "Sindhi": "sd",
    "Tongan": "to", "Tswana": "tn", "Tatar": "tt", "Uyghur": "ug", "Fijian": "fj",
    "Galician": "gl", "Igbo": "ig", "Kinyarwanda": "rw", "Kirundi": "rn"
}

translator = Translator()

# -----------------------------
# User Language Preferences
# -----------------------------
def load_user_languages():
    if not os.path.exists(USER_LANG_FILE):
        with open(USER_LANG_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_LANG_FILE, "r") as f:
        return json.load(f)

def save_user_languages(data):
    with open(USER_LANG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def set_user_language(user_email, lang_code):
    users = load_user_languages()
    users[user_email] = lang_code
    save_user_languages(users)

def get_user_language(user_email):
    users = load_user_languages()
    return users.get(user_email, DEFAULT_LANGUAGE)

# -----------------------------
# Translation
# -----------------------------
def translate_text(text, target_language):
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        print(f"[TRANSLATE ERROR] {e}")
        return text

def translate_for_user(user_email, text):
    lang_code = get_user_language(user_email)
    return translate_text(text, lang_code)

# -----------------------------
# Switch Language Mid-Chat
# -----------------------------
def switch_language(user_email):
    print("\nAvailable languages:")
    for idx, (name, code) in enumerate(SUPPORTED_LANGUAGES.items(), 1):
        print(f"{idx}. {name} ({code})")
    choice = input("Select language number: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(SUPPORTED_LANGUAGES):
        selected_code = list(SUPPORTED_LANGUAGES.values())[int(choice)-1]
        set_user_language(user_email, selected_code)
        print(f"✅ Language switched to {list(SUPPORTED_LANGUAGES.keys())[int(choice)-1]}")
    else:
        print("Invalid selection. Language not changed.")

# -----------------------------
# List Supported Languages
# -----------------------------
def list_supported_languages():
    return SUPPORTED_LANGUAGES

# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    
    while True:
        print("\n--- Neuraluxe Translation Hub ---")
        print("1. Translate Text")
        print("2. Switch Language")
        print("3. Show Current Language")
        print("4. Exit")
        option = input("Choose an option: ").strip()
        
        if option == "1":
            msg = input("Enter text to translate: ")
            print("Translated:", translate_for_user(email, msg))
        elif option == "2":
            switch_language(email)
        elif option == "3":
            print("Current language:", get_user_language(email))
        elif option == "4":
            break
        else:
            print("Invalid option. Try again.")