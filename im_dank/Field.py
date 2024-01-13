from im_dank.Constants import CLOZE_MARKER
from im_dank.Markdown import converter
import re


class Field:
    def __init__(self, name, lines=None):
        self.name = name
        self._lines = []
        self._open_clozes = 0
        for line in lines or []:
            self.append_line(line)

    def append_line(self, line):
        """
        Append a line to the text content of the  field. If the line contains
        curly braces that Anki would interpret as part of a cloze, a marker is
        inserted so that these braces can be ignored by the syntax highlighter.
        """
        # TODO: This could probably be accomplished with a Preprocessor for the
        #       markdown library instead. They also operate line-wise.
        line_parts = []

        segments_and_clozes = re.split(r'({{c\d+::)', line)
        segments = segments_and_clozes[::2]
        clozes = segments_and_clozes[1::2] + ['']

        for segment, cloze in zip(segments, clozes):
            closing_pairs = segment.count('}}')
            line_parts.append(
                segment.replace('}}', CLOZE_MARKER + '}}', self._open_clozes)
            )
            self._open_clozes = max(self._open_clozes - closing_pairs, 0)

            if cloze:
                line_parts.append(CLOZE_MARKER + cloze)
                self._open_clozes += 1

        self._lines.append("".join(line_parts))

    def markdown(self):
        """
        Convert the field's text content to HTML that can be sent to Anki,
        and restore the cloze markers that were modified by append_line().
        """
        raw_markdown = converter.convert('\n'.join(self._lines))
        raw_markdown, _ = re.subn(
            '<p>' + CLOZE_MARKER + r'({{c\d+::)</p>', '\\1', raw_markdown
        )
        return raw_markdown \
            .replace('<p>' + CLOZE_MARKER + '}}</p>', '}}') \
            .replace(' class="arithmatex"', '') \
            .replace('</anki-mathjax block="true">', '</anki-mathjax>') \
            .replace(CLOZE_MARKER + '{{', '{{') \
            .replace(CLOZE_MARKER + '}}', '}}')
