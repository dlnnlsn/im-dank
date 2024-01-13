import markdown

extensions = [
    'pymdownx.arithmatex',
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
