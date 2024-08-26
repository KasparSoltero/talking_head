import py_audio2face as pya2f
import numpy as np


class Audio2FaceController:
    a2f: pya2f.Audio2Face

    def __init__(self):
        self.a2f = pya2f.Audio2Face()
        # self.a2f.init_a2f()

    def process_audio_stream(self, audio_data: np.array):
        # self.a2f.init_a2f()
        self.a2f.stream_audio(audio_data, fps=60)
