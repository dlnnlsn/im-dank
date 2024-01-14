from im_dank.AnkiConnect import AnkiConnect
from im_dank.Parser import parse
import sys


def main():
    markdown_content = ""
    with open(sys.argv[1]) as markdown_file:
        markdown_content = markdown_file.read()
    if markdown_content == "":
        return
    extracted_notes = parse(markdown_content)
    anki_client = AnkiConnect()
    print(anki_client.addNotes(
        [note for note in extracted_notes if note.id is None]
    ))
    print(anki_client.updateNotes(
        [note for note in extracted_notes if note.id is not None]
    ))
    new_content = markdown_content.split('\n')
    for note in extracted_notes:
        if note._updated_note_id is not None:
            new_content[note._note_start_line] = \
                f'<!-- Note Id: {note._updated_note_id} -->'
        else:
            new_content[note._note_start_line] = '<!-- Note -->'
    with open(sys.argv[1], 'w') as markdown_file:
        markdown_file.write('\n'.join(new_content))


if __name__ == "__main__":
    main()
