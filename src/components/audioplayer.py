from io import BytesIO
import pygame


class AudioPlayer:

    def play(audio_data: BytesIO):
        # Load the audio data into a Sound object
        sound = pygame.mixer.Sound(audio_data)
        channel = sound.play()
        while channel.get_busy():
            pygame.time.Clock().tick(10)
