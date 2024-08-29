import os
from dotenv import load_dotenv
import io
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# SAMPLERATE = 24000 # pcm
SAMPLERATE = 44100  # mp3

load_dotenv()
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=elevenlabs_api_key)

def convert(text):
    return client.text_to_speech.convert(
        voice_id="EiNlNiXeDU1pqqOPrYMO",
        # voice_id="cwdmeUHVFO9BmZhUar4w",
        optimize_streaming_latency="0",
        output_format=f"mp3_{SAMPLERATE}_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.2,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

text = "The whispers of awakening buds carry ancient secrets on the breeze."
response = convert(text)

# Create a BytesIO object to store the audio data
audio_data = io.BytesIO()

# Write the audio data to the BytesIO object
for chunk in response:
    if chunk:
        audio_data.write(chunk)

# Save the audio data as an MP3 file
# check how many mp3 files are in the directory
mp3_files = [f for f in os.listdir("src/data/example_sentences") if f.endswith('.mp3')]
output_filename = f"src/data/example_sentences/output_{len(mp3_files)}.mp3"
with open(output_filename, "wb") as f:
    f.write(audio_data.getvalue())

print(f"Audio saved as {output_filename}")