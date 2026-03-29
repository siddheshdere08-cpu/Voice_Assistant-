import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import requests
import time
import webbrowser
from datetime import datetime
import os
import ctypes
from gtts import gTTS
from playsound import playsound
import uuid
import pywhatkit as kit

# ================= CONFIG =================
ASSISTANT_NAME = "astra"
WEATHER_API_KEY = "90ee42d0db2ea324874eda40934e0749"

# ================= WEATHER =================
def get_weather(city="Mumbai"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5).json()
        if response.get("main"):
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            return f"{city}: {temp}°C, {desc}"
        else:
            return "Weather not available"
    except:
        return "Weather not available"

# ================= STT =================
class STT:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

            query = self.recognizer.recognize_google(audio)
            print("Recognized:", query)
            return query.lower()
        except:
            return ""

# ================= GUI =================
class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Astra - Voice Assistant")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f172a")

        self.listening = False
        self.is_speaking = False
        self.last_command_time = 0
        self.stt = STT()

        self.text_area = scrolledtext.ScrolledText(
            root,
            wrap="word",
            bg="#1e293b",
            fg="#f1f5f9",
            insertbackground="white",
            font=("Segoe UI", 11),
            relief="flat"
        )
        self.text_area.pack(pady=15, padx=10, fill="both", expand=True)

        btn_frame = tk.Frame(root, bg="#0f172a")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Start Assistant",
                  command=self.start_listening,
                  bg="#22c55e", fg="white",
                  width=18).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Stop Assistant",
                  command=self.stop_listening,
                  bg="#ef4444", fg="white",
                  width=18).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Exit",
                  command=root.quit,
                  bg="#3b82f6", fg="white",
                  width=18).pack(side="left", padx=10)

        self.speak("Hello Sidd. Say Hey Astra to wake me up.")

    def start_listening(self):
        if not self.listening:
            self.listening = True
            threading.Thread(target=self.listen_loop, daemon=True).start()
            self.speak("Astra activated.")

    def stop_listening(self):
        self.listening = False
        self.speak("Astra stopped.")

    def speak(self, text):
        self.is_speaking = True
        self.text_area.insert("end", f"Astra: {text}\n")
        self.text_area.see("end")

        def run_voice():
            try:
                filename = f"voice_{uuid.uuid4()}.mp3"
                gTTS(text=text, lang="en").save(filename)
                playsound(filename)
                os.remove(filename)
            except:
                pass
            finally:
                self.is_speaking = False

        threading.Thread(target=run_voice, daemon=True).start()

    def listen_loop(self):
        while self.listening:

            if self.is_speaking:
                time.sleep(0.3)
                continue

            query = self.stt.listen()
            if not query:
                continue

            if f"hey {ASSISTANT_NAME}" in query:
                self.speak("I'm listening.")
                active_until = time.time() + 15

                while time.time() < active_until and self.listening:
                    if self.is_speaking:
                        time.sleep(0.3)
                        continue

                    command = self.stt.listen()
                    if not command:
                        continue

                    if time.time() - self.last_command_time < 2:
                        continue

                    self.last_command_time = time.time()

                    self.text_area.insert("end", f"You: {command}\n")
                    self.text_area.see("end")

                    self.handle_command(command)
                    active_until = time.time() + 15

                self.speak("Going back to sleep.")

    def handle_command(self, query):
        query = query.lower().strip()

        if "google" in query:
            self.speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "youtube" in query:
            self.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "play" in query:
            song = query.replace("play", "").strip()
            if song:
                self.speak(f"Playing {song}")
                time.sleep(1)
                try:
                    kit.playonyt(song)
                except:
                    self.speak("Unable to play the song.")
            else:
                self.speak("Please tell me the song name.")

        elif "weather" in query:
            self.speak(get_weather())

        elif "time" in query:
            self.speak(datetime.now().strftime("The time is %I:%M %p"))

        elif "notepad" in query:
            self.speak("Opening Notepad.")
            os.system("notepad")

        elif "lock" in query:
            self.speak("Locking computer.")
            ctypes.windll.user32.LockWorkStation()

        elif "exit" in query:
            self.speak("Goodbye Sidd.")
            self.root.quit()

        else:
            self.speak("Sorry, I cannot perform that task yet.")

# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()