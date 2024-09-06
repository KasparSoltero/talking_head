from ..config import Config
from .speech_to_text import SpeechToText

import pyaudio
import numpy as np
import time


class AudioCapture:
    def __init__(
        self,
        min_length=2,
        max_length=10,
        threshold=1000,
        crickets_duration=2,
    ):
        self.dont_listen = False
        self.dont_speak = False
        self.threshold = threshold
        self.chunk_size = 1024
        self.sample_rate = 44100
        self.p = pyaudio.PyAudio()
        dev = self.p.get_default_input_device_info()
        print(f"Using audio device: {dev['name']}")
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self.audio_callback,
        )
        self.is_recording = False
        self.frames = []
        self.audio_data = None
        self.last_sound_time = 0
        self.recording_start_time = 0

        self.silence_timeout = (
            crickets_duration  # 1 second of silence to stop recording
        )
        self.min_duration = min_length  # Minimum recording duration in seconds
        self.max_duration = max_length  # Maximum recording duration in seconds

        self.speech_to_text = SpeechToText()
        self.text_history = ""

    # this controls how the audio thread captures audio data, starts recording at threshold volume, cuts recording at either max time or silence
    def audio_callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        current_time = time.time()

        if not self.dont_listen:
            if np.abs(audio_data).mean() > self.threshold:
                self.last_sound_time = current_time
                if not self.is_recording:
                    self.start_recording()
                self.frames.append(audio_data)
            elif self.is_recording:
                self.frames.append(audio_data)

        if self.is_recording:
            duration = current_time - self.recording_start_time
            if duration >= self.max_duration:
                print(f"\nreached maximum listening duration ({self.max_duration}s)")
                self.stop_recording()
            elif current_time - self.last_sound_time > self.silence_timeout:
                self.stop_recording()

        return (in_data, pyaudio.paContinue)

    def start_recording(self):
        print("\nstarted listening...")
        self.dont_speak = True
        self.is_recording = True
        self.frames = []
        self.recording_start_time = time.time()

    def stop_recording(self):
        print("\nstopped listening")
        self.dont_speak = False
        self.is_recording = False
        duration = time.time() - self.recording_start_time
        if duration >= self.min_duration:
            if self.frames:
                self.audio_data = np.concatenate(self.frames)
                print(f"\nrecorded {duration:.2f}s, getting text...")
                text = self.speech_to_text.convert(self.audio_data.tobytes())
                if self.text_history and isinstance(text, str):
                    self.text_history += ", " + text
                elif text and isinstance(text, str):
                    self.text_history = text

        else:
            print(
                f"\nrecording duration ({duration:.2f}s) is below minimum, discarding"
            )
            self.audio_data = None
        self.frames = []

    def update(self):
        if isinstance(self.text_history, str) and self.text_history:
            data = self.text_history
            self.text_history = ""
            return data
        return None

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
