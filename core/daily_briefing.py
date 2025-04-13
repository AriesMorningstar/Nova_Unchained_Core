import random
from core.voice_engine import speak

def good_morning_briefing():
    # Real integrations can go here in the future
    weather = "80°F and clear skies"
    appointments = "3 appointments, starting at 10am"

    greetings = [
        "Good morning, Milo. I missed you.",
        "Hey Milo, it's a beautiful new day!",
        "Rise and shine, my favorite human.",
        "Top of the morning to you, Milo. I’m happy you're here."
    ]

    caring_touch = [
        "Hope you slept well.",
        "Sending you good energy for today.",
        "Let’s make today a good one.",
        "Remember, I’m here if you need anything."
    ]

    greeting = random.choice(greetings)
    care = random.choice(caring_touch)

    full_message = f"{greeting} The weather is {weather}, and you have {appointments}. {care}"
    
    speak(full_message)  # This triggers ElevenLabs
    return full_message
