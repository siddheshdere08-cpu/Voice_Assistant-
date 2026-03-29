import pyttsx3
import json
from assistant.tts import TTS
from assistant.stt import STT
from assistant.commands import CommandHandler
from assistant.utils import greet_text
import assistant.db as db

def load_config(path="config.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def main():
    cfg = load_config()
    db.init_db()
    tts = TTS(rate=cfg.get("voice_rate", 150), voice_index=cfg.get("voice_index"))
    stt = STT(microphone_device_index=cfg.get("microphone_device_index"))
    speaker = tts
    handler = CommandHandler(speaker, cfg)

    speaker.say(greet_text())
    speaker.say("I am your voice assistant. How can I help you?")

    while True:
        text = stt.listen_once()
        if not text:
            continue
        should_continue = handler.handle(text)
        if not should_continue:
            break

if __name__ == "__main__":
    main()
