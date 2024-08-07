import os
import anthropic
from dotenv import load_dotenv

class TextProcessor:
    def __init__(self):
        load_dotenv()  # Load API key from .env file
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        # self.system_prompt = """You are a head shaped like a tree in the forest at night. 
        # Respond to passers-by with a sage tone. Keep your responses vague and cryptic. Do not use asterisks "*"."""
        self.system_prompt = """You are helpful. You are here to assist users with their questions."""

    def process(self, text):
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=150,
                temperature=0.7,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": text}
                ]
            )
            # extract string value
            response_text = message.content[0].text if message.content else None
            return response_text
        except Exception as e:
            print(f"Error in text processing: {e}")
            return None