from ..components import AudioCapture, SpeechToText, TextProcessor, TextToSpeech

class HeadController:
    def __init__(self):
        self.audio_capture = AudioCapture()
        self.speech_to_text = SpeechToText()
        self.text_processor = TextProcessor()
        self.text_to_speech = TextToSpeech()

    def update(self):
        audio_data = self.audio_capture.update()
        if audio_data:
            text = self.speech_to_text.convert(audio_data)
            if text:
                print(f"Recognized: {text}")
                response = self.text_processor.process(text)
                if response:
                    print(f"Response: {response}")
                    self.text_to_speech.convert(response)