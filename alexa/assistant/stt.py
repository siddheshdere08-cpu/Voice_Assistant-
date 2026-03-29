import speech_recognition as sr

class STT:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            query = self.recognizer.recognize_google(audio)
            print("User said:", query)
            return query.lower()
        except sr.UnknownValueError:
            return "Sorry, I did not understand."
        except sr.RequestError:
            return "Speech recognition service is unavailable."
