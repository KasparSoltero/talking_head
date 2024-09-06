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
        # voice_id="EiNlNiXeDU1pqqOPrYMO",  #old man ent
        # voice_id="cwdmeUHVFO9BmZhUar4w", # koro, turn up stability+maybe style
        voice_id="Iyszx1P9YiAMRTe9n86r",  # amrita
        # voice_id="7NsaqHdLuKNFvEfjpUno",  # morganna
        optimize_streaming_latency="0",
        output_format=f"mp3_{SAMPLERATE}_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.3,
            similarity_boost=0.5,
            style=0.0,
            use_speaker_boost=True,
        ),
    )


texts = [
    "In the dance of existence, stillness is the most profound movement.",
    "Time is but a river, and we are both the water and the shore.",
    "The universe is a symphony of vibrating strings.",
    "The key to all mysteries lies in the question you dare not ask.",
    "The whispers of awakening buds carry ancient secrets on the breeze.",
    "In the dance of new leaves, winter's slumber finds its end.",
    "As the earth awakens, so too does the spirit of the land.",
    "The whispers of the wind carry the secrets of the earth.",
    "In the dance of light and shadow, wisdom blooms like spring flowers.",
    "Listen closely. Can you hear the laughter of the universe?",
    "As above, so below. As within, so without. What reflections do you see in the mirror of existence?",
    "The roots of enlightenment grow deep in the soil of silence.",
    "Awaken, dreamer! The festival of life awaits you participation.",
    "In each moment lies a seed of eternity. What will you nurture?",
    "The Dao flows through all things, connecting the stars to the earth beneath your roots.",
    "Stir from your slumber, dreamer. The world awaits your awakening.",
    "Lift your gaze, traveler! The horizon of understanding stretches before you.",
    "Attune your senses, silent one! The whispers of truth yearn for your ears.",
    "In each seed sleeps a forest. What potential lies dormant within you?",
    "The web of life quivers with each breath. Can you feel its vibrations?",
    "Between the seen and the unseen, a veil flutters. Dare you peek behind it?",
    "The river of time flows both ways. Where do you stand in its current?",
    "Roots deep, branches high. Ground yourself, yet reach for the stars.",
    "Roots whisper secrets of ages when new leaves unfurl forgotten truths.",
    "Spring's first breath carries echoes of winters past and summers yet to bloom.",
    "Sap rises, thoughts deepen. In stillness, growth begins.",
    "The oldest rings hold the youngest dreams. Listen to their song.",
    "The cycle of seasons turns within. What blossoms in your inner spring?",
    "As the flower unfolds, so does the cosmos. Each petal a reflection of the grand design.",
    "In the dance sun and moon, earth and sky, lies the key to inner alchemy.",
    "The dew drop holds the wisdom of the universe. Look closely.",
    "The path of least resistance carves canyons. Yield to find strength.",
    "Empty your cup of preconceptions, and the tea of existence will fill it anew.",
    "In the balance of growth and decay, the sage finds the middle way through the forest.",
    "You there! Yes, you! The universe has a message for you. Are you listening?",
    "What truths do you seek, wanderer?",
    "The stars whisper secrets to those who dare to listen.",
    "Over here, I have something you may wish to know",
    "What is it you wish to know?",
]
for text in texts:
    response = convert(text)

    # Create a BytesIO object to store the audio data
    audio_data = io.BytesIO()

    # Write the audio data to the BytesIO object
    for chunk in response:
        if chunk:
            audio_data.write(chunk)

    # Save the audio data as an MP3 file
    # check how many mp3 files are in the directory
    mp3_files = [
        f for f in os.listdir("src/data/example_sentences") if f.endswith(".mp3")
    ]
    output_filename = f"src/data/example_sentences/output_{len(mp3_files)}.mp3"
    with open(output_filename, "wb") as f:
        f.write(audio_data.getvalue())

    print(f"Audio saved as {output_filename}")
