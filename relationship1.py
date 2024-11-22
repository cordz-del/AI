import pyttsx3
import openai
import speech_recognition as sr
import random
import time

# Set your OpenAI API Key
openai.api_key = 'your_openai_api_key_here'

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Filters for inappropriate content
FORBIDDEN_TOPICS = ["race", "religion", "violence", "hate", "insult", "offensive"]

# Quit keywords
QUIT_KEYWORDS = ["goodbye", "exit", "leave", "quit", "bye"]

# Prompts categorized for interaction
CATEGORIES = {
    "empathy": [
        "How do you think your friend felt during a situation?",
        "Can you think of a time when you felt truly understood?",
        "What would you say to someone feeling sad to cheer them up?"
    ],
    "ethics": [
        "What would you do if you found someone’s wallet?",
        "Why is it important to be honest even when no one is watching?",
        "Can you think of a time when you had to make a tough but right choice?"
    ],
    "conflict_resolution": [
        "How could you solve a disagreement with a friend peacefully?",
        "What’s one thing you could do to make up with someone you’ve argued with?",
        "How do you think we can prevent arguments from happening?"
    ],
    "critical_thinking": [
        "If you could change one rule at school, what would it be and why?",
        "What would you do if you saw someone being unfairly treated?",
        "Why do you think teamwork is important?"
    ],
    "creativity": [
        "If you could design a new game, what would it be like?",
        "Imagine you’re an inventor. What would you create?",
        "If you could paint a picture of your favorite day, what would it look like?"
    ]
}

PREVIOUS_STATEMENTS = set()

# Set voice to maximum volume
def set_voice_settings():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Default voice
    engine.setProperty('volume', 1.0)  # Max volume

def speak(text):
    print(f"Chatbot: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            speak("I didn't understand that. Could you try again?")
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Could you repeat?")
        return ""

def check_quit_command(user_input):
    return any(keyword in user_input.lower() for keyword in QUIT_KEYWORDS)

def contains_inappropriate_content(user_input):
    return any(topic in user_input.lower() for topic in FORBIDDEN_TOPICS)

def deduplicate_response(user_input):
    if user_input in PREVIOUS_STATEMENTS:
        speak("You've mentioned that before. Can you tell me something new?")
        return False
    PREVIOUS_STATEMENTS.add(user_input)
    return True

def select_random_prompt():
    category = random.choice(list(CATEGORIES.keys()))
    return random.choice(CATEGORIES[category])

def decision_loop():
    while True:
        speak("Would you like to try another scenario or exit?")
        decision = listen()
        if decision and "yes" in decision.lower():
            return True
        elif decision and "no" in decision.lower():
            return False
        speak("I didn't catch that. Please say 'yes' or 'no'.")

def chatbot():
    set_voice_settings()
    speak("Hello! Let's have a great conversation.")
    conversation_log = []

    while True:
        user_input = listen()
        if check_quit_command(user_input):
            speak("Goodbye! It was great chatting with you.")
            break
        if contains_inappropriate_content(user_input):
            speak("Let's keep our conversation kind and positive.")
            continue
        if not deduplicate_response(user_input):
            continue

        # Dynamic scenario selection
        prompt = select_random_prompt()
        response = f"Thank you for sharing! {prompt}"
        conversation_log.append({"user": user_input, "chatbot": response})
        speak(response)

        # Check if the user wants to continue
        if not decision_loop():
            speak("Goodbye! I hope we can chat again soon.")
            break

    # Save conversation log
    with open("conversation_log.txt", "w") as file:
        for entry in conversation_log:
            file.write(f"User: {entry['user']}\nChatbot: {entry['chatbot']}\n")

if __name__ == "__main__":
    chatbot()
