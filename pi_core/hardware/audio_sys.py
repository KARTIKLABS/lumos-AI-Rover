import logging
import threading

try:
    import pyttsx3
    HAS_TTS = True
except ImportError:
    HAS_TTS = False

class AudioSystem:
    def __init__(self):
        self.engine = None
        if HAS_TTS:
            try:
                self.engine = pyttsx3.init()
            except Exception as e:
                logging.error(f"TTS initialization failed: {e}")
                self.engine = None
        self._lock = threading.Lock()

    def speak(self, text: str):
        if not self.engine:
            logging.warning(f"Audio System (No TTS): {text}")
            return
            
        # Run in a separate thread so it doesn't block the main loop
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()

    def _speak_thread(self, text: str):
        with self._lock:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logging.error(f"TTS speaking error: {e}")

    def play_siren(self):
        # Implementation for playing a siren .wav file via PyAudio or simple aplay command
        logging.info("WEE WOO WEE WOO (Siren Playing)")
