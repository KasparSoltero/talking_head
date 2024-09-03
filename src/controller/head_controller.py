import io
from typing import Iterator
import time
import os
import random

# from pydub import AudioSegment
from ..components import (
    AudioCapture,
    SpeechToText,
    TextProcessor,
    TextToSpeech,
    Memory,
    AudioPlayer,
    # Audio2FaceController,
    AudioToUnrealMovement,
)

class HeadController:
    def __init__(self):
        self.text_to_speech = TextToSpeech()
        self.audio_capture = AudioCapture()
        self.text_processor = TextProcessor()
        self.memory = Memory()
        self.audio_player = AudioPlayer()
        # self.audio2face = Audio2FaceController()
        self.audio_to_unreal_movement = AudioToUnrealMovement()

        self.last_update_time = time.time()
        # self.default_sentences_dir = "src/data/example_sentences"
        current_dir = os.path.dirname(os.path.realpath(__file__))
        src_dir = os.path.dirname(current_dir)
        self.default_sentences_dir = os.path.join(src_dir, "data", "example_sentences")

    def update(self):
        print("....", end="\r\r\r")
        texts_since_last_update = self.audio_capture.update()
        current_time = time.time()
        if texts_since_last_update:
            self.last_update_time = current_time
            self.memory.user_said(texts_since_last_update)

            response = self.text_processor.process(self.memory.conversation_history)
            if response:
                print(f"Response: {response}")

                self.memory.head_said(response)
                audio_stream = self.text_to_speech.convert(response)
                # self.audio2face.play_animation_from_audio(
                #     consume_byte_iterator(audio_stream)
                # )
                # self.audio2face.play_animation_from_audio_stream(audio_stream)
                # self.audio_player.play(audio_buf)
                self.audio_to_unreal_movement.process_audio_stream(audio_stream)
                self.audio_capture.dont_listen = True
                self.audio_player.play(consume_byte_iterator(audio_stream))
                self.audio_capture.dont_listen = False

        elif current_time - self.last_update_time > 15:
            print("No user input for 30 seconds. Playing default sentence.")
            self.memory.clear()
            self.play_default_sentence()
            self.last_update_time = current_time

    def play_default_sentence(self):
        default_files = [
            f for f in os.listdir(self.default_sentences_dir) if f.endswith(".mp3")
        ]
        if default_files:
            random_file = random.choice(default_files)
            file_path = os.path.join(self.default_sentences_dir, random_file)
            print(f'Playing default sentence: "{file_path}"')

            audio_stream = self.audio_player.get_stream_from_mp3(file_path)
            self.audio_to_unreal_movement.process_audio_stream(audio_stream)
            self.audio_capture.dont_listen = True
            self.audio_player.play(consume_byte_iterator(audio_stream))
            self.audio_capture.dont_listen = False


def consume_byte_iterator(byte_iterator: Iterator[bytes]) -> io.BytesIO:
    audio_data = io.BytesIO()
    # Write the audio data to the BytesIO object
    for chunk in byte_iterator:
        if chunk:
            audio_data.write(chunk)
    # Seek to the beginning of the BytesIO object
    audio_data.seek(0)

    return audio_data
