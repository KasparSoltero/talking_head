from io import BytesIO
import pygame
import os
import io
import random

ffmpeg_path = (
    r"C:\Users\edeet\Downloads\ffmpeg-7.0.2-full_build\ffmpeg-7.0.2-full_build\bin"
)
os.environ["PATH"] += os.pathsep + ffmpeg_path

from pydub import AudioSegment

AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")


class AudioPlayer:
    def __init__(self, speed=1.0):
        self.speed = speed
        self.stop = False
        pygame.mixer.init()

    def play(self, audio_data: BytesIO):
        try:
            print(f"Playing audio")
            audio_data.seek(0)

            # Adjust speed
            if self.speed != 1.0:
                audio_segment = AudioSegment.from_file(audio_data, format="mp3")
                adjusted_frame_rate = int(audio_segment.frame_rate * self.speed)
                audio_segment = audio_segment._spawn(
                    audio_segment.raw_data,
                    overrides={"frame_rate": adjusted_frame_rate},
                )
                # Export to a new BytesIO object
                audio_data = io.BytesIO()
                audio_segment.export(audio_data, format="wav")
                audio_data.seek(0)

            # Load the audio data into a Sound object
            sound = pygame.mixer.Sound(audio_data)
            channel = sound.play()
            while channel.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"error! trying to play audio{e}")

    def waiting(self):
        while not self.stop:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            src_dir = os.path.dirname(current_dir)
            self.default_sentences_dir = os.path.join(src_dir, "data", "waiting_sounds")
            random_file = random.choice(
                [
                    f
                    for f in os.listdir(self.default_sentences_dir)
                    if f.endswith(".mp3")
                ]
            )
            file_path = os.path.join(self.default_sentences_dir, random_file)
            audio_data = self.get_audio_data_from_mp3(file_path)
            self.play(audio_data)
        self.stop = False

    def get_audio_data_from_mp3(self, file_path: str):
        audio = AudioSegment.from_mp3(file_path)
        audio = audio.set_frame_rate(44100).set_channels(1)
        buffer = BytesIO()
        audio.export(buffer, format="mp3")
        buffer.seek(0)
        return buffer

    # def get_stream_from_mp3(self, file_path: str):
    #     audio = AudioSegment.from_mp3(file_path)
    #     audio = audio.set_frame_rate(44100).set_channels(1)
    #     buffer = BytesIO()
    #     audio.export(buffer, format="wav")
    #     buffer.seek(0)

    #     while True:
    #         chunk = buffer.read(1024)
    #         if not chunk:
    #             break
    #         yield chunk
