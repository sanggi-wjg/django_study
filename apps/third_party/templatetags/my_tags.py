from datetime import datetime, timedelta

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name = 'startswith')
@stringfilter
def startswith(text: str, starts_text: str):
    return text.startswith(starts_text)


@register.simple_tag
def delta_year(delta):
    current_year = datetime.today().strftime('%Y')
    date = datetime.strptime(current_year, '%Y') - timedelta(days = (int(delta) * 365))
    return date.strftime('%Y')
