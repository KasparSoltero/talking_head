from io import BytesIO
import pygame


class AudioPlayer:

    def play(self, audio_data: BytesIO):
        print(f"Playing audio")
        # Load the audio data into a Sound object
        audio_data.seek(0)
        sound = pygame.mixer.Sound(audio_data)
        channel = sound.play()
        while channel.get_busy():
            pygame.time.Clock().tick(10)
