from django import template
from django.template.defaultfilters import stringfilter

from apps.third_party.util.utils import current_year_subtract

register = template.Library()


@register.filter(name = 'startswith')
@stringfilter
def startswith(text: str, starts_text: str):
    return text.startswith(starts_text)


@register.simple_tag
def year_subtract(delta: int):
    return current_year_subtract(delta)
