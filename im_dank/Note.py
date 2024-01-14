class Note:
    def __init__(self, deck, model):
        self.deck = deck
        self.model = model
        self.fields = {}
        self.tags = []

    def __getitem__(self, key):
        return self.fields[key]

    def __setitem__(self, key, value):
        self.fields[key] = value

    def __json__(self):
        return {
            'deckName': self.deck,
            'modelName': self.model,
            'fields': self.fields,
            'tags': self.tags
        }
