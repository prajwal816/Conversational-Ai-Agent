class ConversationMemory:
    def __init__(self):
        self.global_context = {}

    def update_context(self, key: str, value: any):
        self.global_context[key] = value

    def get_context(self, key: str) -> any:
        return self.global_context.get(key, None)

    def clear(self):
        self.global_context.clear()
