from io import BytesIO
import pygame
import os

ffmpeg_path = (
    r"C:\Users\edeet\Downloads\ffmpeg-7.0.2-full_build\ffmpeg-7.0.2-full_build\bin"
)
os.environ["PATH"] += os.pathsep + ffmpeg_path

from pydub import AudioSegment

AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")


class AudioPlayer:
    def get_stream_from_mp3(self, file_path: str):
        audio = AudioSegment.from_mp3(file_path)
        audio = audio.set_frame_rate(44100).set_channels(1)
        buffer = BytesIO()
        audio.export(buffer, format="wav")
        buffer.seek(0)

        while True:
            chunk = buffer.read(1024)
            if not chunk:
                break
            yield chunk

    def play(self, audio_data: BytesIO):
        print(f"Playing audio")
        # Load the audio data into a Sound object
        audio_data.seek(0)
        sound = pygame.mixer.Sound(audio_data)
        channel = sound.play()
        while channel.get_busy():
            pygame.time.Clock().tick(10)
