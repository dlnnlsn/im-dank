from im_dank.Parser import parse
import json
import sys


def main():
    markdown_content = ""
    with open(sys.argv[1]) as markdown_file:
        markdown_content = markdown_file.read()
    if markdown_content == "":
        return
    extracted_notes = parse(markdown_content)
    print(json.dumps(extracted_notes, default=lambda o: o.__json__()))


if __name__ == "__main__":
    main()
