class Memory:
    def __init__(self):
        self.conversation_history = []

    def user_said(self, text):
        self.conversation_history.append({"role": "user", "content": text})

    def head_said(self, text):
        self.conversation_history.append({"role": "assistant", "content": text})
        self.conversation_history = self.conversation_history[-4:]

    def last_role(self):
        if self.conversation_history:
            return self.conversation_history[-1]["role"]
        else:
            return None