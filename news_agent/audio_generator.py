from gtts import gTTS
import os

class AudioGenerator:
    def __init__(self, lang='en'):
        self.lang = lang

    def generate_audio(self, text, output_file="summary.mp3"):
        """Generates audio from text and saves it to a file."""
        if not text:
            print("No text to generate audio from.")
            return None

        try:
            tts = gTTS(text=text, lang=self.lang)
            tts.save(output_file)
            print(f"Audio saved to {output_file}")
            return output_file
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None
