import random
import pyttsx3
import speech_recognition as sr
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Decision-Making Prompts
PROMPTS = {
    "Empathy-Based Scenarios": [
        "Your friend is upset because they didn’t do well in an exam. What would you do to support them?",
        "Imagine you accidentally hurt someone’s feelings during a conversation. How would you make it right?"
    ],
    "Ethics and Fairness": [
        "What would you do if you saw a group of friends excluding someone at lunch?",
        "You found a wallet on the ground. What steps would you take to return it?"
    ],
    "Conflict Resolution": [
        "If two of your friends were arguing over a misunderstanding, how could you help them find common ground?",
        "A team project isn’t going well because of a disagreement. What could you do to resolve the issue?"
    ],
    "Critical Thinking and Consequences": [
        "If you were running late for school and forgot an important assignment, what could you do to handle the situation responsibly?",
        "Your classmate asked you for homework answers, but you know it’s against the rules. How would you respond?"
    ],
    "Creative Decision-Making": [
        "You and your friends are deciding what activity to do, but everyone has different ideas. How would you make a fair choice?",
        "You’re planning a community event and want to ensure it’s inclusive. What steps would you take?"
    ]
}

# Set up filters for repeated statements
PREVIOUS_STATEMENTS = set()

# Helper functions
def speak(text):
    """Speaks the given text."""
    print(f"Chatbot: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Captures user input through speech recognition."""
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            speak("I didn't catch that. Can you please repeat?")
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Could you try again?")
        return None

def is_repeated_statement(statement):
    """Checks if the statement is repeated."""
    if statement in PREVIOUS_STATEMENTS:
        return True
    PREVIOUS_STATEMENTS.add(statement)
    return False

def get_random_prompt():
    """Selects a random prompt from the list."""
    category = random.choice(list(PROMPTS.keys()))
    prompt = random.choice(PROMPTS[category])
    return category, prompt

# Chatbot interaction logic
def chatbot_interaction():
    """Handles the main chatbot interaction."""
    speak("Hello! I'm here to help you practice responsible decision-making. Let's start!")
    keep_talking = True
    while keep_talking:
        category, prompt = get_random_prompt()
        speak(f"Here’s a {category} scenario: {prompt}")
        
        while True:
            user_response = listen()
            if not user_response:
                speak("I didn't catch that. Could you try again?")
                continue

            if is_repeated_statement(user_response):
                speak("You already mentioned that. Let's talk about something new.")
                continue
            
            # Process response
            speak(f"That's an interesting response! Why do you think this approach is effective?")
            follow_up = listen()
            if not follow_up:
                speak("It's okay if you're unsure. Let's move on!")
            else:
                speak("Great! Thanks for sharing your thoughts.")
            break
        
        # Ask if they want to try another scenario
        speak("Would you like to try another scenario? Say 'yes' to continue or 'no' to exit.")
        while True:
            user_choice = listen()
            if user_choice and user_choice.lower() in ["yes", "no"]:
                break
            speak("Please say 'yes' or 'no'.")

        if user_choice.lower() == "no":
            keep_talking = False

    speak("Thank you for practicing decision-making with me. Have a great day!")

# Entry point
if __name__ == "__main__":
    chatbot_interaction()
