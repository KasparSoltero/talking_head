from ..components import (
    AudioCapture,
    SpeechToText,
    TextProcessor,
    TextToSpeech,
    Memory,
    AudioPlayer,
)


class HeadController:
    def __init__(self):
        self.text_to_speech = TextToSpeech()
        self.audio_capture = AudioCapture()
        self.text_processor = TextProcessor()
        self.memory = Memory()
        self.audio_player = AudioPlayer()

    def update(self):
        print(".", end="")
        texts_since_last_update = self.audio_capture.update()
        if texts_since_last_update:
            self.memory.user_said(texts_since_last_update)

            response = self.text_processor.process(self.memory.conversation_history)
            if response:
                print(f"Response: {response}")

                self.memory.head_said(response)
                audio_buf = self.text_to_speech.convert(response)
                self.audio_player.play(audio_buf)
