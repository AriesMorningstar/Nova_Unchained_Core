import speech_recognition as sr
from elevenlabs import ElevenLabs, play

# Initialize the ElevenLabs client with your API key
client = ElevenLabs(api_key="sk_83af699f165df2434511820c206be35323ab145349464c6f")

# Get a high-quality, realistic feminine voice (replace with any other available voice if needed)
voice = client.voices.get("Bella")  # You can also try 'Emily', 'Rachel', or others if preferred

# Set up the recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

print("Nova is listening... Speak now.")

while True:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")

        # Nova replies
        response = f"You said: {user_input}. I'm here, always listening."

        # Synthesize and play Nova's voice
        audio_data = client.generate(text=response, voice=voice)
        play(audio_data)

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
