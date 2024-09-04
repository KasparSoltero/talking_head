import io
from typing import Iterator
import time
import os
import random
import argparse
import itertools
import sys

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
        args = self.parse_args()
        self.text_to_speech = TextToSpeech(voice_idx=args.voice, regenerate_defaults=args.regenerate_defaults)
        self.audio_capture = AudioCapture(
            min_length=args.listen_min_length,
            max_length=args.listen_max_length,
            threshold=args.listen_threshold,
            crickets_duration=args.listen_crickets_duration,
        )
        self.text_processor = TextProcessor()
        self.memory = Memory(memory_length=args.memory_length)
        self.audio_player = AudioPlayer(speed=args.speed)

        self.is_deaf = args.deaf
        self.is_mute = args.mute
        self.play_default_sentence_timeout = args.default_time

        self.last_update_time = time.time()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        src_dir = os.path.dirname(current_dir)
        self.default_sentences_dir = os.path.join(src_dir, "data", "example_sentences")

        self.spinner = itertools.cycle(['.   ', '..  ', '... ', '....'])

    def parse_args(self):
        parser = argparse.ArgumentParser(description="talking head description")
        parser.add_argument('--listen_threshold', type=int, default=600,
                            help='Set the listen threshold value (default: 600)')
        parser.add_argument('--listen_max_length', type=int, default=20,
                            help='Set the listen max length listening value (default: 20)')
        parser.add_argument('--listen_min_length', type=int, default=3,
                            help='Set the listen min length listening value (default: 2)')
        parser.add_argument('--listen_crickets_duration', type=int, default=2,
                            help='Set the listen crickets duration value (default: 2)')
        parser.add_argument('--memory_length', type=int, default=4,
                            help='Set the memory length (default: 4)')
        parser.add_argument('--default_time', type=int, default=30,
                            help='Set the default sentence timeout (default: 30)')
        parser.add_argument('--voice', type=int, default=0,
                            help='Set the voice index (default: 0)')
        parser.add_argument('--deaf', type=bool, default=False,
                            help='Set the deaf mode (default: False)')
        parser.add_argument('--mute', type=bool, default=False,
                            help='Set the mute mode (default: False)')
        parser.add_argument('--speed', type=float, default=1.0,
                            help='Set the speed of the audio (default: 1.0)')
        parser.add_argument('--regenerate_defaults', type=bool, default=False,
                            help='Set the regenerate defaults mode (default: False)')
        args = parser.parse_args()
        return args

    def update(self):
        sys.stdout.write('\rWaiting for input' + next(self.spinner))
        
        # get the latest audio data from the microphone (captured in internal thread)
        if not self.is_deaf:
            texts_since_last_update = self.audio_capture.update()
        else:
            texts_since_last_update = []
        
        if texts_since_last_update:
            self.last_update_time = time.time()
            self.memory.user_said(texts_since_last_update)

            response = self.text_processor.process(self.memory.conversation_history)
            if response:
                self.memory.head_said(response)
                audio_stream = self.text_to_speech.convert(response)
                audio_data = consume_byte_iterator(audio_stream)
                
                if not self.is_mute:
                    self.audio_capture.dont_listen = True
                    self.audio_player.play(audio_data)
                    self.last_update_time = time.time()
                    self.audio_capture.dont_listen = False

        elif time.time() - self.last_update_time > self.play_default_sentence_timeout:
            self.memory.clear()
            self.play_default_sentence()
            self.last_update_time = time.time()

    def play_default_sentence(self):
        default_files = [
            f for f in os.listdir(self.default_sentences_dir) if f.endswith(".mp3")
        ]
        if default_files:
            random_file = random.choice(default_files)
            file_path = os.path.join(self.default_sentences_dir, random_file)
            print(f"Nothing heard for {self.play_default_sentence_timeout} seconds. Choosing {random_file}")
            audio_data = self.audio_player.get_audio_data_from_mp3(file_path)

            if not self.is_mute:
                self.audio_capture.dont_listen = True
                self.audio_player.play(audio_data)
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
