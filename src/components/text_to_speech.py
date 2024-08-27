import os
from dotenv import load_dotenv
import pygame
import io

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

from google.cloud import texttospeech


class TextToSpeech:
    def __init__(self):
        load_dotenv()
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        print(f"ElevenLabs API Key: {elevenlabs_api_key}")
        self.client = ElevenLabs(api_key=elevenlabs_api_key)

        ## google tts init
        # self.client = texttospeech.TextToSpeechClient()
        # self.voice = texttospeech.VoiceSelectionParams(
        #     language_code="en-AU",
        #     name="en-AU-Neural2-D",
        #     ssml_gender=texttospeech.SsmlVoiceGender.MALE
        # )
        # self.audio_config = texttospeech.AudioConfig(
        #     audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        #     effects_profile_id=["large-home-entertainment-class-device"]
        # )
        pygame.mixer.init()

    def convert(self, text):
        return self.client.text_to_speech.convert(
            # voice_id="cwdmeUHVFO9BmZhUar4w",
            voice_id="EiNlNiXeDU1pqqOPrYMO",
            optimize_streaming_latency="0",
            output_format="mp3_44100_32",
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.1,
                similarity_boost=0.2,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        # audio_data = io.BytesIO()
        # # Write the audio data to the BytesIO object
        # for chunk in response:
        #     if chunk:
        #         audio_data.write(chunk)
        # # Seek to the beginning of the BytesIO object
        # audio_data.seek(0)

        # return audio_data

    def convert_google_tts(self, text):
        ssml_text = f"""
        <speak>
            <prosody rate="85%" pitch="-13st">
                <emphasis level="strong">
                    {text}
                </emphasis>
            </prosody>
        </speak>
        """
        # ssml_text = f"""
        # <speak>
        #     <prosody rate="110%">
        #         {text}
        #     </prosody>
        # </speak>
        # """

        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )

        # Save the audio content to a file
        output_file = "output.wav"
        with open(output_file, "wb") as out:
            out.write(response.audio_content)

        # Play the audio
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Clean up the temporary file
        os.remove(output_file)
