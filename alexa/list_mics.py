import speech_recognition as sr

if __name__ == "__main__":
    names = sr.Microphone.list_microphone_names() or []
    if not names:
        print("No microphones found.")
    else:
        for i, name in enumerate(names):
            print(f"{i}: {name}")
