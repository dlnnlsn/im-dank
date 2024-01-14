import pygments
import pygments.lexers
import re
from im_dank.Constants import CLOZE_MARKER
from pygments.lexer import DelegatingLexer, Lexer
from pygments.token import Generic, Other


OPEN_CLOZE_REGEX = CLOZE_MARKER + r'{{c\d+::'
CLOSE_CLOZE_REGEX = CLOZE_MARKER + '}}'
CLOZE_REGEX = '(' + OPEN_CLOZE_REGEX + '|' + CLOSE_CLOZE_REGEX + ')'


class ClozeTokenLexer(Lexer):
    def get_tokens_unprocessed(self, text):
        segments_and_clozes = re.split(CLOZE_REGEX, text)
        segments = segments_and_clozes[::2]
        clozes = segments_and_clozes[1::2] + ['']

        index = 0
        for segment, cloze in zip(segments, clozes):
            if segment:
                yield index, Other, segment
                index += len(segment)
            if cloze:
                yield index, Generic, cloze
                index += len(cloze)


original_get_lexer = pygments.lexers.get_lexer_by_name


def get_lexer_by_name(name, **options):
    root_lexer = original_get_lexer(name, **options)
    return DelegatingLexer(root_lexer.__class__, ClozeTokenLexer)


pygments.lexers.get_lexer_by_name = get_lexer_by_name


def restore_clozes(text):
    text, _ = re.subn(
        r'<span class="g">' + CLOZE_REGEX + '</span>', '\\1', text
    )
    return text
