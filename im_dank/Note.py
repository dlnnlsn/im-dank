class Note:
    def __init__(self, deck, model):
        self.deck = deck
        self.model = model
        self.fields = {}
        self.tags = []
        self.id = None
        self._note_start_line = None
        self._updated_note_id = None

    def __getitem__(self, key):
        return self.fields[key]

    def __setitem__(self, key, value):
        self.fields[key] = value

    def __json__(self):
        return {
            'id': self.id,
            'deckName': self.deck,
            'modelName': self.model,
            'fields': self.fields,
            'tags': self.tags
        }
