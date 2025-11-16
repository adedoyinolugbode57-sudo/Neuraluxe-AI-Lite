"""
Neuraluxe-AI Voice Assistant Tab (Final Version)
------------------------------------------------
- Lightweight TTS & voice commands
- Global weather with forecasts
- Jokes, facts, time, reminders, mini-tools
- Premium-rich look & feel
- Full access for FREE_USER_EMAIL
- Modular and deployable
"""

import json, time, random, requests
from session_manager import FREE_USER_EMAIL, is_free_user
from tts_logic import speak_text

# -------------------------
# Lightweight Global City Database
# -------------------------
CITIES = {
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6895, 139.6917),
    "paris": (48.8566, 2.3522),
    "nairobi": (-1.2921, 36.8219),
    "sydney": (-33.8688, 151.2093),
    "mumbai": (19.0760, 72.8777),
    "cairo": (30.0444, 31.2357),
    "rio de janeiro": (-22.9068, -43.1729),
    "moscow": (55.7558, 37.6173)
}

# -------------------------
# Fetch Global Weather
# -------------------------
def get_weather(city):
    city_lower = city.lower()
    if city_lower not in CITIES:
        return {"error": "City not found in lightweight database."}
    lat, lon = CITIES[city_lower]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&timezone=auto"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        weather = data.get("current_weather", {})
        daily = data.get("daily", {})
        return {
            "city": city.title(),
            "temperature": weather.get("temperature"),
            "windspeed": weather.get("windspeed"),
            "condition_code": weather.get("weathercode"),
            "max_temp": daily.get("temperature_2m_max", ["N/A"])[0],
            "min_temp": daily.get("temperature_2m_min", ["N/A"])[0],
            "sunrise": daily.get("sunrise", ["N/A"])[0],
            "sunset": daily.get("sunset", ["N/A"])[0]
        }
    except Exception as e:
        return {"error": str(e)}

# -------------------------
# Mini-Assistant Features
# -------------------------
def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the AI break up with its computer? Too many bytes!",
        "I would tell you a UDP joke, but you might not get it."
    ]
    return jokes[int(time.time()) % len(jokes)]

def quick_fact():
    facts = [
        "Honey never spoils.",
        "Bananas are berries, but strawberries aren't.",
        "Octopuses have three hearts."
    ]
    return facts[int(time.time()) % len(facts)]

def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# -------------------------
# Additional Ideas/Features
# -------------------------
def countdown_timer(seconds):
    print(f"⏳ Timer started for {seconds} seconds...")
    time.sleep(seconds)
    print("⏰ Timer finished!")
    return "Timer completed."

def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid calculation."

def suggest_activity():
    activities = [
        "Read a book for 20 minutes.",
        "Take a short walk outside.",
        "Try a 5-minute meditation.",
        "Do 10 push-ups or stretches."
    ]
    return random.choice(activities)

def compliment_user():
    compliments = [
        "You're doing amazing today!",
        "Keep up the great work!",
        "Your efforts are inspiring!",
        "You have a brilliant mind!"
    ]
    return random.choice(compliments)

def motivate_user():
    motivations = [
        "Believe in yourself and all that you are.",
        "Every step forward counts, no matter how small.",
        "Challenges are just opportunities in disguise.",
        "Your potential is limitless."
    ]
    return random.choice(motivations)

def simple_unit_converter():
    meters = float(input("Enter value in meters: "))
    km = meters / 1000
    miles = meters * 0.000621371
    return f"{meters} meters = {km} km = {miles} miles"

def random_number(min_val=0, max_val=100):
    return random.randint(min_val, max_val)

def daily_quote():
    quotes = [
        "Innovation distinguishes between a leader and a follower. – Steve Jobs",
        "The best way to predict the future is to invent it. – Alan Kay",
        "Dream big. Work hard. Stay focused.",
        "AI is the new electricity. – Andrew Ng"
    ]
    return quotes[int(time.time()) % len(quotes)]

def remind_user():
    task = input("Enter task to remind: ").strip()
    delay = int(input("Delay in seconds: ").strip())
    print(f"Reminder set for {task} in {delay} seconds...")
    time.sleep(delay)
    return f"⏰ Reminder: {task}"

def motivational_weather(city):
    weather = get_weather(city)
    if "error" in weather:
        return weather["error"]
    temp = weather["temperature"]
    if temp < 15:
        return f"Bundle up! It's cold in {city.title()} today."
    elif temp > 30:
        return f"Stay cool! It's hot in {city.title()} today."
    else:
        return f"The weather is mild in {city.title()}. Have a great day!"

# -------------------------
# Voice Assistant UI
# -------------------------
def voice_assistant_ui(user_email):
    full_access = (user_email == FREE_USER_EMAIL)

    print("\n=== Neuraluxe-AI Voice Assistant ===")
    while True:
        print("\nOptions:")
        print("1. Speak a text")
        print("2. Get weather (global)")
        print("3. Tell a joke")
        print("4. Quick fact")
        print("5. Get current time")
        print("6. Countdown timer")
        print("7. Simple calculator")
        print("8. Suggest activity")
        print("9. Compliment user")
        print("10. Motivational message")
        print("11. Unit converter (meters to km/miles)")
        print("12. Random number generator")
        print("13. Daily inspirational quote")
        print("14. Set reminder")
        print("15. Motivational weather")
        print("16. Exit Voice Assistant")

        choice = input("Select option: ").strip()

        if choice == "1":
            text = input("Enter text to speak: ").strip()
            if is_free_user(user_email) and not full_access:
                print("⚠️ Free users have limited TTS functionality.")
            speak_text(user_email, text)

        elif choice == "2":
            city = input("Enter city name: ").strip()
            weather = get_weather(city)
            if "error" in weather:
                print(weather["error"])
                speak_text(user_email, weather["error"])
            else:
                msg = (f"Weather in {weather['city']}: {weather['temperature']}°C, "
                       f"Max: {weather['max_temp']}°C, Min: {weather['min_temp']}°C, "
                       f"Wind {weather['windspeed']} km/h, Sunrise: {weather['sunrise']}, Sunset: {weather['sunset']}")
                print(msg)
                speak_text(user_email, msg)

        elif choice == "3":
            joke = tell_joke()
            print(joke)
            speak_text(user_email, joke)

        elif choice == "4":
            fact = quick_fact()
            print(fact)
            speak_text(user_email, fact)

        elif choice == "5":
            now = current_time()
            print(f"Current Time: {now}")
            speak_text(user_email, f"The current time is {now}")

        elif choice == "6":
            sec = int(input("Enter seconds for countdown: "))
            msg = countdown_timer(sec)
            speak_text(user_email, msg)

        elif choice == "7":
            expr = input("Enter expression to calculate: ")
            result = calculator(expr)
            print(f"Result: {result}")
            speak_text(user_email, f"The result is {result}")

        elif choice == "8":
            activity = suggest_activity()
            print(activity)
            speak_text(user_email, activity)

        elif choice == "9":
            comp = compliment_user()
            print(comp)
            speak_text(user_email, comp)

        elif choice == "10":
            mot = motivate_user()
            print(mot)
            speak_text(user_email, mot)

        elif choice == "11":
            conv = simple_unit_converter()
            print(conv)
            speak_text(user_email, conv)

        elif choice == "12":
            rand_num = random_number()
            print(f"Random Number: {rand_num}")
            speak_text(user_email, f"Random number is {rand_num}")

        elif choice == "13":
            quote = daily_quote()
            print(quote)
            speak_text(user_email, quote)

        elif choice == "14":
            reminder = remind_user()
            print(reminder)
            speak_text(user_email, reminder)

        elif choice == "15":
            city = input("Enter city for motivational weather: ").strip()
            msg = motivational_weather(city)
            print(msg)
            speak_text(user_email, msg)

        elif choice == "16":
            print("Exiting Voice Assistant...")
            break

        else:
            print("Invalid option. Try again.")

# -------------------------
# Standalone Run
# -------------------------
if __name__ == "__main__":
    email = input("Enter your email: ").strip()
    voice_assistant_ui(email)