"""
Voice Assistant — Beginner Tier
OIB-SIP Task 1

Features:
- Captures voice input via microphone (speech_recognition)
- Responds to "hello" with a greeting
- Tells the current time and date on request
- Performs a web search on a spoken topic
- Handles unrecognized speech gracefully (asks user to repeat)
- Gives text-to-speech feedback for every response
"""

import datetime
import webbrowser

import speech_recognition as sr
import pyttsx3

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text: str) -> None:
    """Convert text to speech and print it, so the user gets both channels."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    """Capture one utterance from the microphone and return it as lowercase text.

    Returns an empty string if speech could not be understood or the
    service could not be reached, so the caller can handle it gracefully.
    """
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return ""

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat it?")
        return ""
    except sr.RequestError:
        speak("I'm having trouble reaching the speech service right now.")
        return ""


# ---------------------------------------------------------------------------
# Command handling
# ---------------------------------------------------------------------------

def handle_command(command: str) -> bool:
    """Process one recognized command. Returns False if the user wants to exit."""
    if not command:
        return True

    if "hello" in command:
        speak("Hello! How can I help you today?")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.")

    elif "search" in command:
        # e.g. "search for python tutorials" -> query = "python tutorials"
        topic = command.replace("search for", "").replace("search", "").strip()
        if topic:
            speak(f"Searching the web for {topic}.")
            webbrowser.open(f"https://www.google.com/search?q={topic}")
        else:
            speak("What would you like me to search for?")

    elif "open" in command:
        # e.g. "open youtube" -> opens youtube.com directly
        known_sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "linkedin": "https://www.linkedin.com",
            "github": "https://github.com",
        }
        matched_site = None
        for site_name, url in known_sites.items():
            if site_name in command:
                matched_site = site_name
                speak(f"Opening {site_name}.")
                webbrowser.open(url)
                break
        if not matched_site:
            speak("I don't know that website yet. I can open YouTube, Google, "
                  "Gmail, LinkedIn, or GitHub.")

    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        return False

    else:
        speak("I can greet you, tell the time or date, search the web, or "
              "open a website. Try one of those, or say 'exit' to quit.")

    return True


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    speak("Voice assistant is ready. Say 'hello', ask for the time or date, "
          "say 'search for <topic>', or say 'exit' to quit.")
    running = True
    while running:
        command = listen()
        running = handle_command(command)


if __name__ == "__main__":
    main()