import io
from typing import Iterator
from ..components import (
    AudioCapture,
    SpeechToText,
    TextProcessor,
    TextToSpeech,
    Memory,
    AudioPlayer,
    Audio2FaceController,
)


class HeadController:
    def __init__(self):
        self.text_to_speech = TextToSpeech()
        self.audio_capture = AudioCapture()
        self.text_processor = TextProcessor()
        self.memory = Memory()
        self.audio_player = AudioPlayer()
        self.audio2face = Audio2FaceController()

    def update(self):
        print(".", end="")
        texts_since_last_update = self.audio_capture.update()
        if texts_since_last_update:
            self.memory.user_said(texts_since_last_update)

            response = self.text_processor.process(self.memory.conversation_history)
            if response:
                print(f"Response: {response}")

                self.memory.head_said(response)
                audio_stream = self.text_to_speech.convert(response)
                self.audio2face.play_animation_from_audio(
                    consume_byte_iterator(audio_stream)
                )
                # self.audio2face.play_animation_from_audio_stream(audio_stream)
                # self.audio_player.play(audio_buf)


def consume_byte_iterator(byte_iterator: Iterator[bytes]) -> io.BytesIO:
    audio_data = io.BytesIO()
    # Write the audio data to the BytesIO object
    for chunk in byte_iterator:
        if chunk:
            audio_data.write(chunk)
    # Seek to the beginning of the BytesIO object
    audio_data.seek(0)

    return audio_data
