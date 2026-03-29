import wikipedia
import pywhatkit
import os
import datetime
import assistant.db as db
from . import db



class CommandHandler:
    def __init__(self, tts, config=None):
        self.tts = tts
        self.config = config or {}

    def handle(self, query: str):
        query = query.lower()

        if "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.tts.speak(f"The time is {current_time}")

        elif "wikipedia" in query:
            topic = query.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(topic, sentences=2)
                self.tts.speak(result)
            except:
                self.tts.speak("Sorry, I could not find that on Wikipedia.")

        elif query.startswith("play"):
            song = query.replace("play", "").strip()
            self.tts.speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif "search" in query:
            search_query = query.replace("search", "").strip()
            self.tts.speak(f"Searching {search_query} on Google")
            pywhatkit.search(search_query)

        elif "open notepad" in query:
            self.tts.speak("Opening Notepad")
            os.system("notepad")

        elif "exit" in query or "stop" in query:
            self.tts.speak("Goodbye!")
            return True  # tells GUI to stop

        else:
            self.tts.speak("I did not understand that.")
        
        return False
