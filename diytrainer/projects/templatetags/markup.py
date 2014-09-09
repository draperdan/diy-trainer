from django import template

import markdown
from typogrify.filters import typogrify

register = template.Library()


@register.filter
def markup(text):
    """
    Use this filter to convert Markdown syntax used in
    the text to HTML on the template.
    """
    return typogrify(markdown.markdown(
        text,
        lazy_ol=False,
        output_format='html5',
        extensions=[
            'abbr',
            'codehilite',
            'fenced_code',
            'sane_lists',
            'smart_strong'
            ]
        )
    )
