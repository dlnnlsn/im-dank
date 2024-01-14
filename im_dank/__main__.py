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
    card_ids = anki_client.addNotes(extracted_notes)
    print(card_ids)


if __name__ == "__main__":
    main()
