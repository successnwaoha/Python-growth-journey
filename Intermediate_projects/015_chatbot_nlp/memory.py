# memory.py
class SessionMemory:
    def __init__(self):
        self.last_intent = None
        self.last_entity = None

    def update(self, intent, entities):
        self.last_intent = intent
        if entities:
            self.last_entity = entities[0]  # Store the first entity found

    def get_context(self):
        return self.last_intent, self.last_entity