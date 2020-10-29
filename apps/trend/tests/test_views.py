from pprint import pprint

import pytest


@pytest.mark.django_db
def test_invest_trend_data():
    from apps.trend.view_helpers import investor_trend_get_data
    test_data = investor_trend_get_data(market = '1', from_date = '2020-10-26', to_date = '2020-10-26')
    pprint(test_data)

    assert test_data['labels'][0] == '2020-10-26'
    assert test_data['datasets']['personal'][0] == -112653
    assert test_data['datasets']['foreigner'][0] == -143711
