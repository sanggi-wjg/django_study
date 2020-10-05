from django import template

from apps.third_party.util.utils import current_year_subtract, current_month_subtract, current_day_subtract, today_dateformat

register = template.Library()


@register.simple_tag
def request_financial_data_basic_btns(fd_type: str) -> str:
    html = ''

    for tag_value, term in _term_list():
        html += "<button class='list-group-item list-group-item-action' onclick='request_financial_data_image(\"{}\", \"{}\")'>{}</button>".format(fd_type.upper(), term, tag_value)

    return '<div class="list-group list-group-horizontal-sm">' + html + '</div>'


@register.simple_tag
def request_financial_data_sector_btns(sector_id: str) -> str:
    html = ''

    for tag_value, term in _term_list():
        html += "<button class='list-group-item list-group-item-action' onclick='request_financial_data_sector_image(\"{}\", \"{}\")'>{}</button>".format(sector_id, term, tag_value)

    return '<div class="list-group list-group-horizontal-sm">' + html + '</div>'


def _term_list() -> list:
    return [
        ['전체', '1991'],
        ['20년', current_year_subtract(20)],
        ['10년', current_year_subtract(10)],
        ['5년', current_year_subtract(5)],
        ['3년', current_year_subtract(3)],
        ['1년', current_year_subtract(1)],
        ['6개월', current_month_subtract(6)],
        ['3개월', current_month_subtract(3)],
        ['1개월', current_month_subtract(1)],
    ]


@register.simple_tag
def day_subtract(delta: int):
    return current_day_subtract(delta)


@register.simple_tag
def current_date():
    return today_dateformat(time_format = '%Y-%m-%d')
