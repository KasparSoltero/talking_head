import os
from dotenv import load_dotenv
import pygame
import io

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

class TextToSpeech:
    def __init__(self):
        load_dotenv()
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        pygame.mixer.init()

    def convert(self, text):
        response = self.client.text_to_speech.convert(
            voice_id="cwdmeUHVFO9BmZhUar4w",
            # optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.3,
                similarity_boost=0.5,
                style=0.0,
                use_speaker_boost=True,
            ),
        )
        
        audio_data = io.BytesIO()
        # Write the audio data to the BytesIO object
        for chunk in response:
            if chunk:
                audio_data.write(chunk)
        # Seek to the beginning of the BytesIO object
        audio_data.seek(0)

        # Load the audio data into a Sound object
        sound = pygame.mixer.Sound(audio_data)
        channel = sound.play()
        while channel.get_busy():
            pygame.time.Clock().tick(10)