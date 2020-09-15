from django import template

from apps.third_party.util.utils import current_year_subtract

register = template.Library()


@register.simple_tag
def request_financial_data_btns(fd_type: str):
    html = ''
    year_list = {
        '전체' : '1991',
        '20년': current_year_subtract(20),
        '10년': current_year_subtract(10),
        '5년' : current_year_subtract(5),
        '3년' : current_year_subtract(3),
        '1년' : current_year_subtract(1),
    }

    for key, value in year_list.items():
        html += "<button class='list-group-item list-group-item-action' onclick='request_financial_data_image(\"{}\", \"{}\")'>{}</button>".format(fd_type.upper(), value, key)

    return '<div class="list-group list-group-horizontal-sm">' + html + '</div>'
