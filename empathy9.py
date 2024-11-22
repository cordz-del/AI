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
FORBIDDEN_TOPICS = ["race", "religion", "nationality", "violence", "hate", "insult", "offensive"]

# Quit keywords
QUIT_KEYWORDS = ["goodbye", "exit", "leave", "quit", "bye"]

# Categorized prompts for dynamic and engaging interaction
EMPATHY_PROMPTS = [
    "How do you think your friend felt during [specific situation]?",
    "What would you say to make someone feel better if they were having a tough day?",
    "Can you think of a time when you felt like someone really understood you?",
]

CONFLICT_RESOLUTION_PROMPTS = [
    "When we disagree with a friend, what could we say to stay calm and solve the problem together?",
    "How could you let someone know how you feel without hurting their feelings?",
    "What’s one nice thing you could say to help someone feel better in an argument?",
]

CRITICAL_THINKING_PROMPTS = [
    "What would you do if you found someone’s lost item?",
    "If you could solve one big problem in the world, what would it be?",
    "Can you think of a creative way to help a friend who’s feeling down?",
]

CREATIVITY_PROMPTS = [
    "If you could invent something to make life easier, what would it be?",
    "What’s the most creative thing you’ve done recently?",
    "Can you imagine a fun new game you could play with your friends?",
]

ALL_PROMPTS = (
    EMPATHY_PROMPTS
    + CONFLICT_RESOLUTION_PROMPTS
    + CRITICAL_THINKING_PROMPTS
    + CREATIVITY_PROMPTS
)

# Set the voice to Zira and max volume
def set_voice_to_zira():
    voices = engine.getProperty("voices")
    for voice in voices:
        if "zira" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            print(f"Voice set to: {voice.name}")
            break
    engine.setProperty("volume", 1.0)  # Set volume to maximum
    print("Volume set to maximum.")

# Function to speak text and display it
def speak_and_display(text):
    print(f"Chatbot: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)  # Short delay for synchronization

# Function to listen and recognize speech
def get_audio_input(prompt):
    """Capture user input via speech recognition."""
    speak_and_display(prompt)
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
            recognized_text = recognizer.recognize_google(audio)
            print(f"Child: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            speak_and_display("I'm sorry, I didn't catch that. Could you try again?")
            return None
        except sr.WaitTimeoutError:
            speak_and_display("I didn't hear anything. Could you try again?")
            return None
        except sr.RequestError:
            speak_and_display("I'm sorry, there seems to be a problem with the microphone.")
            return None

# Function to check for inappropriate content
def filter_inappropriate_content(user_input):
    if not user_input:
        return False
    for topic in FORBIDDEN_TOPICS:
        if topic in user_input.lower():
            return True
    return False

# Function to recognize quit commands
def is_quit_command(user_input):
    if not user_input:
        return False
    for quit_word in QUIT_KEYWORDS:
        if quit_word in user_input.lower():
            return True
    return False

# Record and log the conversation
def log_conversation(conversation):
    with open("conversation_log.txt", "w") as file:
        for entry in conversation:
            file.write(f"Child: {entry['child']}\n")
            file.write(f"Chatbot: {entry['chatbot']}\n\n")

# Main chatbot function
def chatbot_interaction():
    """Handle interactive chatbot sessions with categorized prompts."""
    set_voice_to_zira()
    conversation_log = []

    # Initial greeting
    speak_and_display("Hi there! How are you today?")
    while True:
        user_input = get_audio_input("Please share your thoughts:")
        if not user_input:
            continue
        if is_quit_command(user_input):
            speak_and_display("Goodbye! It was so nice talking to you!")
            break
        if filter_inappropriate_content(user_input):
            speak_and_display("Let's keep our conversation kind and positive.")
            continue

        # Select prompts dynamically
        if len(conversation_log) < len(ALL_PROMPTS):
            prompt = ALL_PROMPTS[len(conversation_log)]
        else:
            prompt = "What else would you like to share about how you think or feel?"

        speak_and_display(prompt)
        chatbot_response = f"That's a great response! {prompt}"
        conversation_log.append({"child": user_input, "chatbot": chatbot_response})
        speak_and_display(chatbot_response)

        # Decision loop: ask if the user wants to continue
        continue_input = get_audio_input("Would you like to continue? Say 'yes' or 'no'.")
        if continue_input and "no" in continue_input.lower():
            speak_and_display("Thanks for the chat! Have a great day!")
            break

    # Log the conversation after the interaction ends
    log_conversation(conversation_log)

if __name__ == "__main__":
    chatbot_interaction()
