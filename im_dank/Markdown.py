from im_dank.Pygments import restore_clozes
import markdown

extensions = [
    'pymdownx.arithmatex',
    'pymdownx.highlight',
    'pymdownx.superfences',
]

extension_configs = {
    'pymdownx.arithmatex': {
        'generic': True,
        'tex_inline_wrap': ['', ''],
        'tex_block_wrap': ['', ''],
        'inline_tag': 'anki-mathjax',
        'block_tag': 'anki-mathjax block="true"',
    },
}

converter = markdown.Markdown(
    extensions=extensions,
    extension_configs=extension_configs
)


def convert(markdown):
    return restore_clozes(converter.convert(markdown))


__all__ = ['convert']
