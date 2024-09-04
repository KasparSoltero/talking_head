class Memory:
    def __init__(self, memory_length=4):
        self.conversation_history = []
        self.memory_length = memory_length

    def user_said(self, text):
        self.conversation_history.append({"role": "user", "content": text})
        print(f'\nuser said: {text}')

    def head_said(self, text):
        self.conversation_history.append({"role": "assistant", "content": text})
        self.conversation_history = self.conversation_history[-self.memory_length:]
        print(f'\nhead said: {text}')

    def last_role(self):
        if self.conversation_history:
            return self.conversation_history[-1]["role"]
        else:
            return None
        
    def clear(self):
        self.conversation_history = []