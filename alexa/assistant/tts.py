import pyttsx3

class TTS:
    def __init__(self, rate=150, voice_index=None):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        voices = self.engine.getProperty("voices")
        if voice_index is not None and 0 <= voice_index < len(voices):
            self.engine.setProperty("voice", voices[voice_index].id)

    def say(self, text):
        print("Assistant:", text)
        self.engine.say(text)
        self.engine.runAndWait()
