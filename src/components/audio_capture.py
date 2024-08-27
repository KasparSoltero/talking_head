from ..config import Config
from .speech_to_text import SpeechToText

import pyaudio
import numpy as np
import time


class AudioCapture:
    def __init__(self):
        self.threshold = 800
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
        self.silence_timeout = 2.0  # 1 second of silence to stop recording
        self.last_sound_time = 0
        self.recording_start_time = 0
        self.min_duration = 2  # Minimum recording duration in seconds
        self.max_duration = 10.0  # Maximum recording duration in seconds

        self.speech_to_text = SpeechToText()
        self.text_history = ""

    # this controls how the audio thread captures audio data, starts recording at threshold volume, cuts recording at either max time or silence
    def audio_callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        current_time = time.time()

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
                print("10 seconds max recording duration")
                self.stop_recording()
            elif current_time - self.last_sound_time > self.silence_timeout:
                self.stop_recording()

        return (in_data, pyaudio.paContinue)

    def start_recording(self):
        print("listening...")
        self.is_recording = True
        self.frames = []
        self.recording_start_time = time.time()

    def stop_recording(self):
        print("stopped listening")
        self.is_recording = False
        duration = time.time() - self.recording_start_time
        if duration >= self.min_duration:
            if self.frames:
                self.audio_data = np.concatenate(self.frames)
                print(f"Recording duration: {duration:.2f}s, getting text...")
                text = self.speech_to_text.convert(self.audio_data.tobytes())
                print(f"Recognized: {text}")
                if self.text_history is not "":
                    self.text_history += ", " + text
                elif text:
                    self.text_history = text

        else:
            print(f"({duration:.2f}s) is too short, discarding")
            self.audio_data = None
        self.frames = []

    def update(self):
        if self.text_history is not "":
            data = self.text_history
            self.text_history = ""
            return data
        return None

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
