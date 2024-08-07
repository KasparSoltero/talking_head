import os
from google.cloud import speech
from dotenv import load_dotenv

class SpeechToText:
    def __init__(self):
        load_dotenv()  # Load api key (google_speech_to_text_service.json) from .env file
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US",
        )

    def convert(self, audio_data):
        # Configure the audio settings
        audio = speech.RecognitionAudio(content=audio_data)

        # Perform the speech recognition
        response = self.client.recognize(config=self.config, audio=audio)

        # Extract the recognized text
        text = ""
        for result in response.results:
            text += result.alternatives[0].transcript

        return text if text else None