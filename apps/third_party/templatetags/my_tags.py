from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name = 'startswith')
@stringfilter
def startswith(text: str, starts_text: str):
    return text.startswith(starts_text)
