from im_dank.json import serialize
import requests


class AnkiConnect:
    def __init__(self, host='127.0.0.1', port=8765):
        self.host = host
        self.port = port

    def _invoke(self, action, **params):
        request_json = serialize({
            'action': action, 'params': params, 'version': 6
        })
        response = requests.get(
            f'http://{self.host}:{self.port}', data=request_json
        ).json()
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']

    def getDeckNames(self):
        return self._invoke('deckNames')

    def addNote(self, note):
        note_id = self._invoke('addNote', note=note)
        note._updated_note_id = note_id
        return note_id

    def addNotes(self, notes):
        note_ids = self._invoke('addNotes', notes=notes)
        for note_id, note in zip(note_ids, notes):
            note._updated_note_id = note_id
        return note_ids

    def cardsForNote(self, note_id):
        return self.cardsForNotes([note_id])

    def cardsForNotes(self, note_ids):
        return self.findCards(f'nid:{",".join(map(str, note_ids))}')

    def changeDeck(self, card_ids, deck):
        return self._invoke('changeDeck', cards=card_ids, deck=deck)

    def deleteNotes(self, note_ids):
        return self._invoke('deleteNotes', notes=note_ids)

    def findCards(self, query):
        return self._invoke('findCards', query=query)

    def findNotes(self, query):
        return self._invoke('findNotes', query=query)

    def updateNote(self, note):
        """
        Update the fields and tags of the note with a specific ID.
        Does not change the deck or model of the note.
        """
        if note.id is None:
            raise Exception('Can only update notes with an ID')
        note_data = {
            'id': note.id,
            'fields': note.fields,
            'tags': note.tags,
        }
        return self._invoke('updateNote', note=note_data)

    def updateNotes(self, notes):
        """
        Updates the fields and tags of all of the notes in a given list.
        Recreates the cards for any notes whose model has changed.
        Moves all of the cards for a note to a new deck if the note's deck has
        changed since it was last added to Anki.
        """
        note_ids = [note.id for note in notes if note.id is not None]
        existing_note_info = self._invoke('notesInfo', notes=note_ids)
        note_models = {
            note['noteId']: note['modelName']
            for note in existing_note_info if note != {}
        }
        changed_models = [
            note for note in notes
            if note.id not in note_models or note.model != note_models[note.id]
        ]
        changed_models_ids = [note.id for note in changed_models]
        self.deleteNotes(changed_models_ids)
        changed_models_new_ids = self.addNotes(changed_models)
        new_decks = {}
        new_note_ids = []
        index = 0
        for note in notes:
            if note.id not in note_models \
            or note.model != note_models[note.id]:
                new_note_ids.append(changed_models_new_ids[index])
                note._updated_note_id = changed_models_new_ids[index]
                index += 1
            else:
                self.updateNote(note)
                note._updated_note_id = note.id
                new_note_ids.append(note._updated_note_id)
                card_ids = self.cardsForNote(note.id)
                new_decks.setdefault(note.deck, []).extend(card_ids)
        for deck, card_ids in new_decks.items():
            self.changeDeck(card_ids, deck)

        return new_note_ids
