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
        return self._invoke('addNote', note=note)

    def addNotes(self, notes):
        return self._invoke('addNotes', notes=notes)
