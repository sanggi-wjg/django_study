from django.http import JsonResponse
from django.shortcuts import render

from apps.third_party.core.viewmixins import HttpViews
from apps.third_party.util.utils import today_dateformat, current_day_subtract
from apps.trend.view_helpers import investor_trend_get_data


class InvestorTrend(HttpViews):
    template_name = 'trend/trend_list.html'

    def get(self, request, *args, **kwargs):
        """
        market 1:KOSPI / 2:KOSDAQ
        """
        market = self.kwargs.get('market', '1')

        return render(request, self.template_name, context = {
            'view_title'    : '{} 투자자 동향'.format({ '1': 'KOSPI', '2': 'KOSDAQ' }.get(market)),
            'market_name'   : { '1': 'KOSPI', '2': 'KOSDAQ' }.get(market),
            'date_condition': (current_day_subtract(30), today_dateformat(time_format = '%Y-%m-%d')),
        })


class InvestorTrendData(HttpViews):

    def post(self, request, *args, **kwargs):
        market = self.kwargs.get('market')
        from_date = self.kwargs.get('from_date')
        to_date = self.kwargs.get('to_date')
        investor_trend_data = investor_trend_get_data(market, from_date, to_date)

        return JsonResponse(investor_trend_data)
