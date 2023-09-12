!pip install SpeechRecognition
!pip install pyttsx3
!pip install numexpr
import os
import speech_recognition as sr
import pyttsx3
import numexpr

recognizer = sr.Recognizer()
speech_engine = pyttsx3.init()

def speak_text(text):
    speech_engine.say(text)
    speech_engine.runAndWait()

def listen_to_audio():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

def open_application(app_name):
    os.system(f"start {app_name}")
    speak_text(f"{app_name} opened")

def close_application(app_name):
    os.system(f"taskkill /f /im {app_name}.exe")
    speak_text(f"{app_name} closed")

def perform_calculation(expression):
    try:
        result = numexpr.evaluate(expression)
        speak_text(f"The answer is {result}")
    except Exception as e:
        speak_text("I'm sorry, I couldn't understand your calculation.")

if __name__ == '__main__':
    speak_text("Hello, I am ready.")
    while True:
        user_input = listen_to_audio().lower()
        if user_input == "hello":
            speak_text("Hello, how can I help you?")
        elif user_input == "what is your name":
            speak_text("I am a voice-activated AI assistant.")
        elif "open" in user_input and "chrome" in user_input:
            open_application("chrome")
        elif "close" in user_input and "chrome" in user_input:
            close_application("chrome")
        elif "calculate" in user_input or "what is" in user_input:
            expression = user_input.split("calculate")[-1].split("what is")[-1].strip()
            perform_calculation(expression)
        elif user_input == "goodbye":
            speak_text("Goodbye, have a great day!")
            break



