from im_dank.Field import Field
from im_dank.Note import Note
import re


def parse(text, valid_decks=None, model_specs=None):
    """
    Extracts notes from the given text. The text is expected to be in the
    format of a markdown file, with the following additional rules:
    - A line consisting of a single HTML comment of the form
        <!-- Deck: [Deck Name] -->
        will be interpreted as a directive to place all following notes in the
        given deck. If no such directive is given, all notes will be ignored.
    - A line consisting of a single HTML comment of the form
        <!-- !Deck -->
        will be interpreted as a directive to stop using the current deck.
        Any subsequent notes will be ignored unless a new deck is specified.
    - A line consisting of a single HTML comment of the form
        <!-- Model: [Model Name] -->
        will be interpreted as a directive to use the given model for all
        following notes. If no such directive is given, all notes will be
        ignored.
    - A line consisting of a single HTML comment of the form
        <!-- !Model -->
        will be interpreted as a directive to stop using the current model.
        Any subsequent notes will be ignored unless a new model is specified.
    - A line consisting of a single HTML comment of the form
        <!-- Note -->
        will be interpreted as the start of a new note. The note will be added
        to the currently active deck once the <!-- !Note --> directive is
        encountered. If there is no <!-- !Note --> directive, the note will be
        ignored. The model for the note will be the active model when the
        <!-- Note --> directive is reached. If there is no active model,
        the note will be ignored.
    - A line consisting of a single HTML comment of the form
        <!-- !Note -->
        will be interpreted as the end of the current note. The note will be
        added to the deck which was active when then <!-- Note --> directive
        was encountered. If there was no active deck, the note will be ignored.
        The model for the note will be the currently active model. If there is
        no active model, the note will be ignored.
    - A line consisting of a single HTML comment of the form
        <!-- Field: [Field Name] -->
        will be interpreted as a directive to set the currently active field
        to the given field. Any subsequent lines will be appended to the field
        with the given name. Any lines that are encountered when there is no
        acive field will be ignored unless they are directives to take some
        other action.
    - A line consisting of a single HTML comment of the form
        <!-- !Field -->
        will be interpreted as a directive to end the currently active field.
        Any subsequent lines will be ignored unless they are directives to
        take some other action.
    - A line consisting of a single HTML comment of the form
        <!-- Ignore -->
        will be interpreted as a directive to ignore all following lines until
        an <!-- !Ignore --> directive is encountered. This includes lines that
        would otherwise be interpreted as directives.
    - A line consisting of a single HTML comment of the form
        <!-- !Ignore -->
        will be interpreted as a directive to stop ignoring lines.
    """
    current_deck = None
    current_model = None
    current_note = None
    current_field = None
    ignore_lines = False

    notes = []
    for line in text.split('\n'):
        if line.startswith('<!-- !Ignore -->'):
            ignore_lines = False

        if ignore_lines:
            continue

        if line.startswith('<!-- Ignore -->'):
            ignore_lines = True
            continue

        # TODO: Check which characters are allowed in deck names.
        deck_match = re.match(r'<!-- Deck: ([\w() :]+) -->', line)
        if deck_match:
            deck_name = deck_match.group(1)
            if valid_decks is None or deck_name in valid_decks:
                current_deck = deck_name
            else:
                current_deck = None
            continue

        if line.startswith('<!-- !Deck -->'):
            current_deck = None
            continue

        # TODO: Check which characters are allowed in model names.
        model_match = re.match(r'<!-- Model: ([\w() ]+) -->', line)
        if model_match:
            model_name = model_match.group(1)
            if model_specs is None or model_name in model_specs:
                current_model = model_name
            else:
                current_model = None
            continue

        if line.startswith('<!-- !Model -->'):
            current_model = None
            continue

        if line.startswith('<!-- Note -->'):
            if current_deck is None or current_model is None:
                current_note = None
                continue
            current_note = Note(current_deck, current_model)
            continue

        if line.startswith('<!-- !Note -->'):
            if current_note is not None:
                notes.append(current_note)
            current_note = None
            continue

        # TODO: Check which characters are allowed in field names.
        field_match = re.match(r'<!-- Field: ([\w() ]+) -->', line)
        if field_match:
            field_name = field_match.group(1)
            if current_note is None:
                continue
            if model_specs is not None and \
               field_name not in model_specs[current_note.model]:
                continue
            if field_name not in current_note.fields:
                current_note[field_name] = Field(field_name)
            current_field = current_note[field_name]
            continue

        if line.startswith('<!-- !Field -->'):
            current_field = None
            continue

        if current_field is not None:
            current_field.append_line(line)

    return notes
