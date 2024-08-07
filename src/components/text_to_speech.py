import os
from google.cloud import texttospeech
from dotenv import load_dotenv
import pygame

class TextToSpeech:
    def __init__(self):
        load_dotenv()
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-AU",
            name="en-AU-Neural2-D",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            effects_profile_id=["large-home-entertainment-class-device"]
        )
        pygame.mixer.init()

    def convert(self, text):
        # ssml_text = f"""
        # <speak>
        #     <prosody rate="80%" pitch="-13st">
        #         <emphasis level="strong">
        #             {text}
        #         </emphasis>
        #     </prosody>
        # </speak>
        # """
        ssml_text = f"""
        <speak>
            <prosody rate="110%">
                {text}
            </prosody>
        </speak>
        """

        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=self.voice,
            audio_config=self.audio_config
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